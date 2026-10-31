# tjwebb.dev

Source for [tjwebb.dev](https://tjwebb.dev) — TJ Webb's portfolio site.

Self-contained static HTML pages (inline CSS/JS, no build step) with a terminal aesthetic, six switchable color schemes (github-dark, gruvbox, dracula, solarized-dark, monokai, phosphor), and a wandering ASCII cat (left gutter on desktop, free-roam on mobile).

## Structure

- `public/index.html` — the portfolio
- `public/blog/index.html` — blog index (empty until the first approved post)
- `public/blog/feed.xml` — RSS feed
- `tools/blog-post-template.html` — placeholder-only article template, not deployed
- `tools/BLOG.md` — draft and publication instructions
- `tests/test_site.py` — dependency-free static checks
- `public/og-card-v2.png` — social share card (version the filename when it changes)
- `tools/og-card.html` — source for regenerating the card via headless Chrome screenshot
- `wrangler.jsonc` — Cloudflare Workers static-assets config with custom domains
- `.github/workflows/deploy.yml` — auto-deploy on push to main

## Deploy

Push to `main` — GitHub Actions runs `wrangler deploy`. Manually: `wrangler deploy`.

Deployed as a Cloudflare Worker serving static assets, with `tjwebb.dev` and `www.tjwebb.dev` as custom domains.

## Blog and checks

See [the authoring guide](tools/BLOG.md). Keep unapproved writing in local, gitignored `drafts/`, never in this public repository or `public/`. Run `python3 -m unittest discover -s tests -v`; PRs run the same checks without deploying.

PR CI also installs pinned Playwright for browser-only checks (not a production dependency), covering mobile/desktop navigation, theme persistence, keyboard access, reduced-motion mode, JS-disabled content, and the article template. To run locally: `python3 -m pip install playwright==1.56.0`, `python3 -m playwright install chromium`, then `python3 tools/check_browser.py`. Screenshots go to gitignored `preview/`.
