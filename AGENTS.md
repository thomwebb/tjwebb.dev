# AGENTS.md

Guidance for AI coding agents working in this repository.

## Project overview

Source for [tjwebb.dev](https://tjwebb.dev) — TJ Webb's personal portfolio site. It is a **single self-contained `index.html`** with inline CSS and JS, no build step, no dependencies, and no package manifest (`package.json`, `pyproject.toml`, etc. do not exist).

The site has a terminal aesthetic and includes:

- Six switchable color schemes (github-dark, gruvbox, dracula, solarized-dark, monokai, phosphor), defined as CSS custom properties under `[data-theme="..."]` selectors and cycled by a fixed toggle button. Theme choice persists in `localStorage` under the key `tw-theme`; an inline head script applies the saved theme before first paint to avoid a flash.
- A wandering ASCII cat (`<pre id="ascii-cat">` plus its dedicated `#ascii-cat` CSS block and trailing `<script>` block — all three marked with `=== ascii-cat:` banner comments so the feature can be removed as a unit). The cat random-walks the page, may walk over text but never stops on it, and is parked in the bottom-left corner under `prefers-reduced-motion: reduce`.
- Self-hosted JetBrains Mono (`public/fonts/*.woff2`, preloaded) and full SEO/social meta including JSON-LD and an OG card image.

## Repository layout

- `public/index.html` — the entire site (markup, styles, scripts all inline).
- `public/fonts/` — JetBrains Mono Regular/Bold `.woff2`, self-hosted.
- `public/og-card-v2.png` — social share card (1200x630). **Version the filename when it changes** (e.g. `og-card-v3.png`) and update the `og:image` / `twitter:image` meta tags to match, so cached cards are invalidated.
- `public/projects/` — currently empty.
- `tools/og-card.html` — fixed-size (1200x630) HTML source for the OG card; regenerate the PNG by screenshotting it with headless Chrome.
- `preview/` — local-only design variants (`index.html`, `bold.html`, `minimal.html`, `terminal.html`). **Gitignored** — never deploy from or rely on these files.
- `wrangler.jsonc` — Cloudflare Workers static-assets config: serves `./public`, with `tjwebb.dev` and `www.tjwebb.dev` as custom domains.
- `.github/workflows/deploy.yml` — CI deploy pipeline (see below).

## Tech stack and runtime architecture

- Plain HTML/CSS/vanilla JS (ES5-style `var`, no modules, no frameworks). Everything is inlined in `public/index.html`; the only external requests are the two font files.
- Runtime: Cloudflare Workers **static assets** — there is no Worker script (`wrangler.jsonc` has no `main` entry), so requests are served directly from the asset store.

## Build, test, and deploy

- **No build step and no test suite.** Verification is manual: open `public/index.html` in a browser (or serve `public/` with any static server) and check the themes, the theme toggle, and the cat's behavior — including `prefers-reduced-motion` emulation and narrow viewports.
- Local preview with Wrangler: `npx wrangler dev` (serves `public/` per `wrangler.jsonc`).
- Deploy happens by pushing to `main`: GitHub Actions runs `cloudflare/wrangler-action@v3` with `command: deploy`. Manual deploy: `npx wrangler deploy`.
- Wrangler is **pinned to 4.120.1** in the workflow — do not bump blindly; the pin comment notes 4.121.0 depends on an unpublished `miniflare@5.20260804.1-alpha`. Check that this is resolved before upgrading.

## Code style guidelines

- Keep the single-file architecture: new styles go in the existing `<style>` block, new behavior in an existing or clearly-delimited `<script>` block. Do not introduce a bundler, framework, or external CSS/JS files.
- Match the surrounding idioms: 2-space indent, `var`-based vanilla JS wrapped in IIFEs, CSS custom properties for all theme colors.
- All colors must come from the theme variables (`--bg`, `--fg`, `--green`, etc.) so every palette stays coherent — never hardcode a color in component CSS. When adding a theme, update all three places: the `[data-theme]` CSS block, and the `themes`/`colors` tables in **both** inline scripts (head theme-restoration script and body toggle script).
- Respect accessibility conventions already in place: `aria-hidden` on decorative elements, `aria-label` on the theme toggle, focus-visible styles, and `prefers-reduced-motion` handling for all animation.
- Self-contained, clearly-scoped features get banner comments (see the `ascii-cat` blocks) stating what to remove together.

## Security considerations

- No secrets live in this repo. The Cloudflare deploy token is the GitHub Actions secret `CLOUDFLARE_API_TOKEN`; the account ID in the workflow is not sensitive. Do not commit tokens, and do not add them to `wrangler.jsonc`.
- The site is fully static with no backend, forms, or third-party scripts, so the attack surface is minimal — keep it that way (e.g. no external script tags without a clear need).
