# NEXPLAY: GitHub Pages release checklist

1. Create a **public** GitHub repository (for example `nexplay`). Upload the **contents** of this `nexplay-site` folder to its root. Set the main branch to `main`.
2. In **Settings → Pages → Build and deployment**, choose **GitHub Actions**. The included workflow will build and deploy automatically when you push changes.
3. Visit the URL shown by GitHub Pages. For a project repository, it is `https://YOURUSERNAME.github.io/REPO/`. For a repository called `YOURUSERNAME.github.io`, the site is at the domain root.
4. Run the release checks in GitHub Actions; inspect all categories, mobile layout, game launch links, graphics toggle, cover status and UX manually. **A URL returning HTTP 200 does not prove a game plays.**
5. When you buy a domain, add it under **Settings → Pages → Custom domain** and update DNS using GitHub's documented instructions. Set repository **Actions variable** `SITE_URL` to your final origin, e.g. `https://example.org`, then redeploy. Verify HTTPS and sitemap.
6. Do not publish copyrighted game ROMs or screenshots without appropriate rights; review game links and privacy/legal obligations in your country.
7. If you intend to monetize commercially, review GitHub Pages' acceptable-use restrictions. Consider Cloudflare Pages for commercial hosting.
8. Submit sitemap to Google Search Console after deployment. First-page Google rankings are never guaranteed.

Local: `python build.py` then `python -m http.server 8080`.
