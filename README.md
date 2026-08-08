# tjwebb.dev

Source for [tjwebb.dev](https://tjwebb.dev) — TJ Webb's portfolio site.

A single self-contained `index.html` (inline CSS/JS, no build step) with a terminal aesthetic, five switchable color schemes (github-dark, gruvbox, dracula, solarized-dark, monokai), and a wandering ASCII cat (left gutter on desktop, free-roam on mobile).

## Structure

- `public/index.html` — the site
- `public/og-card-v2.png` — social share card (version the filename when it changes)
- `tools/og-card.html` — source for regenerating the card via headless Chrome screenshot
- `wrangler.jsonc` — Cloudflare Workers static-assets config with custom domains
- `.github/workflows/deploy.yml` — auto-deploy on push to main

## Deploy

Push to `main` — GitHub Actions runs `wrangler deploy`. Manually: `wrangler deploy`.

Deployed as a Cloudflare Worker serving static assets, with `tjwebb.dev` and `www.tjwebb.dev` as custom domains.
