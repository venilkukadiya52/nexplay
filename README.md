# NEXPLAY — cinematic browser-game discovery website

A deployable static site with a responsive cinematic portal, curated game catalogue, original CSS artwork, search, filters, random discovery, favorites, locally stored motion preferences, SEO-ready static pages, sitemap, robots.txt, JSON-LD breadcrumbs, and category landing pages.

## Run locally

From the `nexplay-site` directory:

```bash
python build.py
python -m http.server 8080
```

Visit http://localhost:8080/ . Do **not** open `index.html` using file:// because search fetches `/assets/games.json`.

## Deploy to Cloudflare Pages

- Framework preset: None / Static HTML
- Build command: `python build.py`
- Output directory: `.`
- Alternatively upload the generated directory.

### Important production configuration

**Before public launch:** Set `SITE_URL=https://your-real-domain.com` when building, or change the default in `build.py`, then rerun `python build.py`. This updates canonical URLs, sitemap, metadata and structured data. Do not index the example.com version. Change the placeholder contact address and review the privacy policy after adding any analytics, cookies or advertising. Verify ownership and use Google Search Console to submit sitemap.xml.

This is a game *discovery portal*, not an operator or licensee of external games. Each game launches in a new tab at its own site. Review licenses and external link availability before publishing.

## SEO

- 20 prebuilt HTML pages, crawlable without JavaScript
- Semantic headings, one H1 per page, canonical links, unique descriptions
- Open Graph metadata, sitemap, robots.txt and breadcrumb structured data
- Original descriptions instead of copied keyword-stuffed text
- Category-based architecture and contextual internal linking

See `SEO-STRATEGY.md` for keyword priorities and ongoing actions.

## Known limitations

The homepage now includes a procedural Three.js WebGL energy-core renderer loaded progressively from a CDN, with a CSS 3D/Canvas fallback. This is a real animated 3D effect, but is not yet the complete explorable multi-zone 3D world described in the creative brief. It needs real-device graphics benchmarking. The original art is programmatic to avoid infringing copyrighted cover artwork. There is no paid backend, account sync, multiplayer lobby, ad integration, or verified Google rankings. Game URLs and compatibility need regular live checking.


## Catalogue update (26 October 2026)

132 BitRunLog-visible catalogue entries imported, including duplicate mirrors where the source lists them separately. Game destinations are third-party websites and are not hosted by NEXPLAY. Most game links have **not** been individually play-tested; entries labeled offline or requiring original game files may not launch immediately. Inclusion does not verify copyright licensing, safety or service uptime.

## Import real screenshots for all 132 BitRunLog listings

The catalogue has 132 game entries. The project has a dedicated image-import tool, but
**the ZIP does not yet contain 132 downloaded game screenshots**. Run this once on a
Windows computer with an internet connection:

```powershell
cd "D:\nexplay-site"
python -m pip install requests beautifulsoup4 pillow
python fetch_covers.py
python build.py
python -m http.server 8080
```

This retrieves publicly visible game cover candidates from BitRunLog, matches them
against the 132 game names/links, checks downloaded image dimensions, converts them
to optimized WebP, and inserts them into the generated pages. It writes
`cover-report.json` identifying missing or rejected images and
`assets/cover-provenance.json` with source URLs. When a game has no confirmed cover,
its existing placeholder art remains; no unrelated image is inserted.

**Rights and use:** Public availability does not grant reuse rights. Some screenshots
may include copyright-protected game artwork. Review and license images appropriately
before enabling a commercial site. Do not use a source's bandwidth indefinitely:
locally stored assets are preferable after rights are cleared.

## Audit every external game link and cover

The project includes `audit_site.py`. From PowerShell (with internet access):

```powershell
cd "D:\nexplay-site"
python -m pip install requests beautifulsoup4 pillow
python fetch_covers.py
python build.py
python audit_site.py
```

`site-audit.json` contains a row for every one of the 132 games: the exact configured
external URL, final redirect URL (when reachable), HTTP result, whether the site's
Play button points to the intended address, and whether its local WebP cover exists.
`cover-report.json` explains unavailable images and matching failures.

**Caution:** HTTP 200 does NOT demonstrate actual game playability. Sites may show
login walls, 404-like error messages with HTTP 200, missing assets or WebGL failures.
For every publicly featured game, a human should open the game and confirm it can
actually start, and verify game-file requirements. Similarly, images found on another
site are not automatically licensed for commercial reuse.
