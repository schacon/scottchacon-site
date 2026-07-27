# AGENTS.md

Notes for working on scottchacon.com. It's an **Astro** site (migrated from
Jekyll). Package manager is **pnpm**; styling is **Tailwind v4** (CSS-first).

## Build & preview

```bash
pnpm install          # once
pnpm dev              # dev server (http://localhost:4321)
pnpm build            # static build → dist/
pnpm preview          # serve the built dist/
```

Node 22+ only — no Ruby/Jekyll anymore. `_tools/` holds dev scripts and is
outside `public/`, so it's never published.

## Project layout

```
astro.config.mjs          # site, trailingSlash:'always', build.format:'directory'
src/
  content.config.ts       # posts collection (glob md/mdx) + htmlPosts (custom loader)
  lib/posts.ts            # getAllPosts(), parseEntry(), categoryMeta(), date/relative helpers
  layouts/                # BaseLayout.astro, PostLayout.astro
  components/             # SiteHeader, PostCard, PromoBanner (+ any React island .jsx/.tsx)
  styles/global.css       # Tailwind v4 (@import "tailwindcss"), @theme fonts, @font-face, component classes
  pages/
    index.astro about.astro posts.astro talks.astro investing.astro 404.astro
    atom.xml.js           # RSS feed → /atom.xml
    [...slug].astro       # dynamic post route → /YYYY/MM/DD/<slug>/
  posts/  git/ tech/ life/ languages/    # posts; folder = category
public/
  assets/…                # served at /assets/... (images, covers, fonts, talks)
  reports/…  favicon.ico  apple-touch-icon.png  CNAME  .nojekyll
```

## Posts

Posts live in `src/posts/<category>/YYYY-MM-DD-slug.<ext>`. The **folder is the
category** (`git`, `tech`, `life`, `languages`). The **URL is
`/YYYY/MM/DD/<slug>/`** (date from filename, slug = filename minus the date
prefix and extension; category is NOT in the URL).

Authoring formats — all first-class:
- **`.md`** — Markdown (the common case). Note: use `.md`, not `.markdown`.
- **`.mdx`** — Markdown + JSX; can import and embed **React components** (islands):
  ```mdx
  import Chart from '../../components/Chart.jsx';
  <Chart client:load />
  ```
- **`.html`** — raw HTML, passed through verbatim (inline `<style>` survives). Use
  this for heavily-designed one-off posts (e.g. the git-wire-protocol-v2 essay).
  Handled by the custom `htmlPosts` loader in `src/content.config.ts`.

Front matter (all formats):
```yaml
---
title: "The Post Title"
image: /assets/images/covers/<slug>.svg
excerpt: "One-sentence summary; used on cards, the meta description, and social."
---
```

`PostLayout.astro` renders each post: per-post OG/Twitter meta (swaps the cover
`.svg` → `.png` for social cards), the git/tech GitButler banner, a build-time
"Month D, YYYY · N years ago" line, a sticky right-rail Table of Contents (built
client-side from `h2`/`h3`; markdown IDs come from `rehype-slug`), and the cover
in the sidebar. Article prose styles are scoped to `.prose-body` (needed under
Tailwind v4's cascade layers so they don't leak into the chrome).

## Cover images

Every post gets a bespoke, content-specific **SVG cover** in
`public/assets/images/covers/<slug>.svg`, referenced by `image:` front matter.

```bash
python3 _tools/generate-covers.py     # writes public/assets/images/covers/*.svg
_tools/rasterize-covers.sh            # rsvg-convert every .svg → .png (for social cards)
```

To add a cover: write a scene function in `_tools/generate-covers.py` using the
`Cover` toolkit (per-category palette in `PAL`: git=orange, tech=indigo,
life=teal/green, lang=rose), register it in `SCENES`, run the script, then run
the rasterize step. Constraints: self-contained SVG (no external resources or web
fonts — they don't load in an `<img>`), keep content vertically centered for the
1.91:1 social crop.

**Social cards need PNG** (Twitter/OG don't render SVG), so always re-run
`rasterize-covers.sh` after changing covers — the meta tags point at the `.png`.

## Categories

Adding/renaming a category means updating:
- `src/posts/<category>/` — the folder (source of truth)
- `src/lib/posts.ts` — `categoryMeta()` map (tag label + Tailwind color classes)
- `_tools/generate-covers.py` — a `PAL` palette, if it needs its own cover look

The git/tech promo banner shows for `category === 'git' || 'tech'` (see
`PostLayout.astro`).

## Deploy

Pushing to `master` triggers `.github/workflows/deploy.yml`: it builds with Astro
(Node + pnpm) and publishes `dist/` to the **`gh-pages`** branch via
`peaceiris/actions-gh-pages`. GitHub Pages is set to deploy from `gh-pages`. The
custom domain (`scottchacon.com`) `CNAME` and `.nojekyll` live in `public/` so
they're copied into every build.

## Other generators

- `_tools/add-post-frontmatter.py` — one-off bulk `image:`/`excerpt:` front-matter
  injector (used when importing many posts).
- `_tools/generate-hungarian-figures.py` — example of generating inline body SVGs
  (writes to `public/assets/images/`), the pattern for in-article diagrams.
