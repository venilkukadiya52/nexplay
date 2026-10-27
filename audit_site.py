"""Audit all NEXPLAY pages, game redirects, and cover files.

Run: python -m pip install requests pillow
     python audit_site.py            # checks public game destinations
     python audit_site.py --offline  # local structure only

The HTTP checks are signals, NOT proof a game starts. Read the report and
manually test JavaScript-heavy sites, game-file requirements, and flagged URLs.
"""
from __future__ import annotations
import argparse, concurrent.futures, json, re, time
from pathlib import Path
from urllib.parse import urlparse
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parent
class A(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.images=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='a' and d.get('href'):self.links.append(d['href'])
  if t=='img' and d.get('src'):self.images.append(d['src'])
def local_check(g):
 slug=g['slug'];page=ROOT/'games'/slug/'index.html';out={'slug':slug,'title':g['title'],'url':g['url'],'local_page_exists':page.is_file(),'cover_exists':False,'cover':'missing','local_link_correct':False,'status_label':g.get('status','unknown')}
 if page.is_file():
  txt=page.read_text('utf8');parser=A();parser.feed(txt)
  out['local_link_correct']=g['url'] in parser.links
 img=ROOT/'assets'/'covers'/(slug+'.webp')
 if img.exists():
  try:
   from PIL import Image
   with Image.open(img) as x:w,h=x.size;x.verify()
   out.update(cover_exists=True,cover=f'{w}x{h}',cover_bytes=img.stat().st_size)
  except Exception as e:out['cover']='invalid: '+str(e)
 return out
def remote_check(item):
 import requests
 from requests.exceptions import RequestException
 headers={'User-Agent':'Mozilla/5.0 (compatible; NEXPLAY-LinkAudit/1.0)'}
 try:
  # GET rather than HEAD: some sites reject HEAD, while GET may execute redirects.
  r=requests.get(item['url'],headers=headers,timeout=(6,14),allow_redirects=True,stream=True)
  final=r.url;status=r.status_code
  item.update(http_status=status,final_url=final,redirect_count=len(r.history),http_check=('responding' if status<400 else 'http_error'))
  if urlparse(final).netloc!=urlparse(item['url']).netloc:item['redirected_to_other_host']=True
  r.close()
 except RequestException as e:item.update(http_status=None,http_check='network_error',error=str(e)[:220])
 return item
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--offline',action='store_true');ap.add_argument('--workers',type=int,default=8);args=ap.parse_args()
 games=json.loads((ROOT/'assets/games.json').read_text('utf8'))
 results=[local_check(g) for g in games]
 if not args.offline:
  with concurrent.futures.ThreadPoolExecutor(max_workers=max(1,min(args.workers,12))) as pool:results=list(pool.map(remote_check,results))
 check={'total':len(results),'local_page_errors':sum(not x['local_page_exists'] for x in results),'incorrect_local_links':sum(not x['local_link_correct'] for x in results),'missing_covers':sum(not x['cover_exists'] for x in results),'invalid_covers':sum(x['cover'].startswith('invalid') for x in results),'http_errors':sum(x.get('http_check')=='http_error' for x in results),'network_errors':sum(x.get('http_check')=='network_error' for x in results),'offline':args.offline}
 report={'summary':check,'games':results,'explanation':'A response code under 400 only shows that the server responded; it does not establish game playability, correctness, or permission to use screenshots.'}
 (ROOT/'site-audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
 print(json.dumps(check,indent=2));print('Saved site-audit.json')
 if args.offline and check['missing_covers']:print('Run fetch_covers.py online, then python build.py and audit again.')
 if check['incorrect_local_links'] or check['local_page_errors']:raise SystemExit(2)
if __name__=='__main__':main()
