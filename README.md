# tjwebb.dev

Source for [tjwebb.dev](https://tjwebb.dev) — TJ Webb's portfolio site.

A single self-contained `index.html` (inline CSS/JS, no build step) with a terminal aesthetic and six switchable color schemes (github-dark, gruvbox, dracula, solarized-dark, monokai, solarized-light).

## Structure

- `public/index.html` — the site
- `wrangler.jsonc` — Cloudflare Workers static-assets config with custom domains
- `preview/` — alternate design variants (minimal, bold) kept for reference

## Deploy

```bash
wrangler deploy
```

Deployed as a Cloudflare Worker serving static assets, with `tjwebb.dev` and `www.tjwebb.dev` as custom domains.
