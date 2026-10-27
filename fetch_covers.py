"""Import game screenshots for NEXPLAY from publicly available source pages.

Run locally on an internet-connected computer:
    python -m pip install requests beautifulsoup4 pillow
    python fetch_covers.py
    python build.py

This uses BitRunLog solely as an image discovery source; image authors retain rights.
Always check licensing before public/commercial use. The source registry is saved
in assets/cover-provenance.json. No claims of licensing are made by this tool.
"""
import io
import json
import re
import time
import unicodedata
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageOps, UnidentifiedImageError

ROOT = Path(__file__).resolve().parent
DEST = ROOT / 'assets' / 'covers'
DEST.mkdir(exist_ok=True, parents=True)
COVERS_FILE = ROOT / 'assets' / 'cover-provenance.json'
USER_AGENT = 'NEXPLAY-Cover-Curator/1.0 (personal design preview; rights verification required)'
TIMEOUT = 18
SESSION = requests.Session()
SESSION.headers['User-Agent'] = USER_AGENT


def normalize(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode().lower()
    text = re.sub(r'\([^)]*\)|\[[^]]*\]', ' ', text)
    text = re.sub(r'\b(game image|game screenshot|browser launch|in browser|additional listing|alternative port|alternative listing|web online|online|web port|mirror|fan browser game)\b', ' ', text)
    return re.sub(r'[^a-z0-9]+', ' ', text).strip()


def similarities(a, b):
    a, b = normalize(a), normalize(b)
    if not a or not b:
        return 0
    if a == b:
        return 1
    if a in b or b in a:
        return 0.89 if min(len(a), len(b)) >= 8 else 0.65
    return SequenceMatcher(None, a, b).ratio()


def candidates_from_bitrunlog():
    resp = SESSION.get('https://bitrunlog.com/', timeout=TIMEOUT)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    candidates = []
    for img in soup.find_all('img'):
        url = img.get('data-src') or img.get('src') or ''
        if not url or url.startswith('data:'):
            continue
        url = urljoin(resp.url, url)
        alt = re.sub(r'\s*(game image|screenshot|thumbnail)\s*$', '', img.get('alt', ''), flags=re.I).strip()
        block = img
        # Select the closest block containing a title and a play link.
        title = alt
        play_url = ''
        for _ in range(5):
            block = block.parent or block
            heading = block.find(['h2', 'h3', 'h4'])
            if heading and heading.get_text(' ', strip=True):
                title = heading.get_text(' ', strip=True)
            links = [a.get('href', '') for a in block.find_all('a', href=True)]
            matches = [urljoin(resp.url, u) for u in links if 'http' in urljoin(resp.url, u) and 'bitrunlog.com' not in urlparse(urljoin(resp.url, u)).netloc]
            if matches:
                play_url = matches[0]
                break
        candidates.append({'title': title, 'image': url, 'play_url': play_url, 'source_page': resp.url})
    return candidates


def choose(game, entries):
    # Match exact play URL before comparing potentially ambiguous game titles.
    g_url = game['url'].rstrip('/').lower()
    same = [e for e in entries if e['play_url'].rstrip('/').lower() == g_url]
    if same:
        same.sort(key=lambda e: similarities(game['title'], e['title']), reverse=True)
        return same[0], 'exact_play_url'
    # Game names need a high confidence match to avoid wrong artwork.
    ranked = sorted(entries, key=lambda e: similarities(game['title'], e['title']), reverse=True)
    if ranked and similarities(game['title'], ranked[0]['title']) >= 0.85:
        if len(ranked) > 1 and similarities(game['title'], ranked[0]['title']) - similarities(game['title'], ranked[1]['title']) < 0.03:
            return None, 'ambiguous_title'
        return ranked[0], 'title_match'
    return None, 'unmatched'


def save_cover(url, slug):
    response = SESSION.get(url, timeout=TIMEOUT, stream=True)
    response.raise_for_status()
    content = b''
    for chunk in response.iter_content(65536):
        content += chunk
        if len(content) > 14 * 1024 * 1024:
            raise ValueError('image too large')
    im = Image.open(io.BytesIO(content))
    im.load()
    w, h = im.size
    if w < 320 or h < 180:
        raise ValueError(f'image too small: {w}x{h}')
    if max(w / h, h / w) > 5:
        raise ValueError(f'unsupported aspect ratio: {w}x{h}')
    im = ImageOps.exif_transpose(im).convert('RGB')
    # Preserves the native aspect ratio, suitable for cover and game detail layouts.
    im.thumbnail((1280, 960), Image.Resampling.LANCZOS)
    output = DEST / (slug + '.webp')
    im.save(output, format='WEBP', quality=86, method=5)
    return {'path': f'/assets/covers/{slug}.webp', 'width': im.width, 'height': im.height, 'bytes': output.stat().st_size}


def main():
    from catalogue_bitrunlog import make_games
    games = make_games()
    try:
        source_entries = candidates_from_bitrunlog()
    except requests.RequestException as exc:
        print('Cannot reach image source:', exc)
        print('Connect to the internet and try again. Existing covers are unchanged.')
        raise SystemExit(1)
    print(f'Found {len(source_entries)} image candidates for {len(games)} game entries.')
    prev = json.loads(COVERS_FILE.read_text('utf-8')) if COVERS_FILE.exists() else {}
    matched, rejected, unmapped = 0, [], []
    for i, game in enumerate(games, start=1):
        slug = game['slug']
        item, method = choose(game, source_entries)
        if not item:
            unmapped.append({'title': game['title'], 'reason': method})
            continue
        try:
            data = save_cover(item['image'], slug)
            prev[slug] = dict(title=game['title'], image_url=item['image'], source_page=item['source_page'], match_method=method, license='NOT_VERIFIED_FOR_REUSE', attribution='Verify with original rights holder before commercial use', **data)
            matched += 1
        except (requests.RequestException, OSError, ValueError, UnidentifiedImageError) as exc:
            rejected.append({'title': game['title'], 'image_url': item['image'], 'error': str(exc)[:150]})
        if i % 20 == 0:
            print(f'Checked {i}/{len(games)}; downloaded {matched}')
        time.sleep(0.035)
    COVERS_FILE.write_text(json.dumps(prev, ensure_ascii=False, indent=2), encoding='utf-8')
    (ROOT/'cover-report.json').write_text(json.dumps({'total':len(games),'downloaded_this_run':matched,'local_covers':len(list(DEST.glob('*.webp'))),'unmatched':unmapped,'failed':rejected},indent=2),encoding='utf-8')
    print(f'Complete: {matched} downloaded, {len(unmapped)} unmatched, {len(rejected)} rejected. Report: cover-report.json')
    print('Review licenses before using third-party images on a commercial public website.')


if __name__ == '__main__':
    main()
