from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import json, re, sys
root=Path(__file__).parent
items=json.loads((root/'assets/games.json').read_text())
errors=[]; slugs=set()
for g in items:
 slug=g['slug']; url=g['url']
 if slug in slugs: errors.append('duplicate slug '+slug)
 slugs.add(slug)
 if urlparse(url).scheme not in ('http','https'): errors.append('invalid URL '+slug)
 if not (root/'games'/slug/'index.html').exists(): errors.append('missing detail '+slug)
 if g.get('status')=='files' and not (root/'games'/slug/'index.html').read_text().count('How to play'): errors.append('missing guide '+slug)
for cat in ('childhood','multiplayer','puzzle','arcade','action','creative','strategy'):
 if not (root/'categories'/cat/'index.html').exists(): errors.append('missing category '+cat)
for html in root.rglob('*.html'):
 txt=html.read_text()
 if 'rel="canonical"' not in txt: errors.append('canonical absent '+str(html))
 if 'example.com' in txt: errors.append('placeholder canonical '+str(html))
 if '<h1' not in txt: errors.append('H1 absent '+str(html))
print('Catalog entries:',len(items),'HTML pages:',len(list(root.rglob('*.html'))))
print('Errors:',len(errors))
for e in errors[:30]:print('ERROR',e)
# Deep regression checks: parse all generated links, not only the catalogue.
from urllib.parse import unquote
base_match=re.search(r'window\.NEXPLAY_BASE=("[^"]*")',(root/'index.html').read_text())
base=json.loads(base_match.group(1)) if base_match else ''
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag in ('a','link','script','img'):
   key='href' if tag in ('a','link') else 'src'
   if d.get(key):self.links.append(d[key])
for html in root.rglob('*.html'):
 doc=Links();doc.feed(html.read_text())
 for url in doc.links:
  if not url.startswith('/') or url.startswith('//'):continue
  loc=url.split('#')[0].split('?')[0]
  if base:
   if not loc.startswith(base+'/'):errors.append('missing base '+str(html.relative_to(root))+' '+loc);continue
   loc=loc[len(base):]
   if loc.startswith(base+'/'):errors.append('double base '+str(html.relative_to(root))+' '+loc);continue
  file=root/unquote(loc.lstrip('/'))
  if loc.endswith('/'):file=file/'index.html'
  if not file.is_file():errors.append('broken local link '+str(html.relative_to(root))+' '+url)
for cat in ('puzzle','multiplayer','creative','arcade','action','childhood','strategy'):
 if not any(cat in g.get('categories',[]) for g in items):errors.append('empty category '+cat)
if 'username.github.io' in (root/'index.html').read_text():errors.append('placeholder deploy URL')
print('Deep link errors:',len(errors))
for e in errors[:60]:print('ERROR',e)
sys.exit(bool(errors))
