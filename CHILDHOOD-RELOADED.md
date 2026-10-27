# Childhood Reloaded (October 2026)

The imported project contains all 142 earlier NEXPLAY game entries, plus 62 new entries: 50 nostalgic console classics and 12 developer/browser-game destinations. The childhood category has 56 entries (50 historical console classics and 6 retro-browser/homebrew destinations); other new discoveries remain in their genre categories.

## Important compatibility/rights distinction

- 50 original cartridge-era games have **Load own ROM**, leading to `https://wasmarcade.games/rom-player/`. This is a shared emulator entry point, **not a one-click playable copy** of each commercial game. NEXPLAY does not include copyrighted ROMs or claim they are free. Users must provide legally obtained compatible game data and are responsible for their local laws.
- New browser-game links are external destinations that are **not confirmed to load into gameplay**. The developer/collection website may require further clicks; for example Nova the Squirrel and Thwaite link to the NES category page, not individual launches. Manually verify these before making claims of instant play.
- Existing original 142 listings remain intact. Several third-party links have not been fully audited for accessibility, legality, or actual playability.
- No game cover images were fabricated. Existing covers (where present) are preserved. Rights to third-party screenshots still need checking.

## How to run

```powershell
cd "D:\nexplay-site"
python build.py
python -m http.server 8080
```

**SEO:** Configure the `SITE_URL` environment variable to your actual domain *before production build* so canonical URLs and the sitemap are valid. Do not advertise old titles as free hosted games. Avoid indexing thin or misleading pages without original information.

## Sources to investigate for legitimate retro-browser games

- https://itch.io/games/free/tag-homebrew/tag-nes
- https://www.crtplay.com/
- https://atlasignal.com/games/platform/nes
- https://wasmarcade.games/rom-player/
- https://www.recompsoftware.com/play/
