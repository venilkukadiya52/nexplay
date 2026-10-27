# NEXPLAY public beta test plan (27 October 2026)

## What is validated
- 208 catalogue records, 218 generated pages, Python generator, JavaScript syntax.
- Deployment in both GitHub Pages project-path mode and custom/root-domain mode.
- Automated audit of every generated internal href and linked local asset.
- Source-level hardening of modal search, favorites DOM rendering, motion initialization and copy.

## What remains unverified
- No genuine rendered browser session: Chromium's requests to localhost were blocked by the execution environment.
- 208 third-party game sessions have NOT been manually launched and tested.
- Game cover images: none are locally imported as licensed/verified screenshots. Generated fallback covers remain.
- Low-end phone GPU behavior, battery, Firefox/Safari rendering, keyboard/controller tests, 200% zoom and real Core Web Vitals.
- External port operators may change access terms or close their servers.

## Minimum real-device smoke test
1. Desktop Chrome/Edge: navigate hero, every category, search, favorites, 3D on/off, reload and back navigation.
2. Firefox desktop: verify 3D fallback and search.
3. Android Chrome: scroll, touch targets, filtering, external launch, rotate screen, reduced motion.
4. iPhone Safari: same as Android; focus on safe-area insets and external tabs.
5. Test 20 promoted games first. Confirm the *actual game* reaches its title or gameplay screen, supported inputs, and if a game needs original files label it as such.
6. Check every remaining game and record verified-at UTC date, country, browser, whether any setup/file/account is required, and outcome.
7. Replace fallback covers only with correctly matched screenshots you have permission to use, including attribution where required.
8. Run Lighthouse / PageSpeed Insights against public Pages URL; check CLS, INP, LCP and accessibility; repeat after changing artwork.
9. Configure repo-specific contact details and privacy/legal disclosures before promoting the beta widely.

## Release language
This is a PUBLIC BETA candidate, NOT a validated 208-playable-games guarantee. Pages labelled unverified link to provider websites for availability checks.
