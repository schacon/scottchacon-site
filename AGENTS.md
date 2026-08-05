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
  content.config.ts       # posts (glob md/mdx) + htmlPosts (custom loader) + projects
  lib/posts.ts            # getAllPosts(), parseEntry(), categoryMeta(), date/relative helpers
  lib/projects.ts         # getAllProjects(), statusMeta()
  layouts/                # BaseLayout.astro, PostLayout.astro, ProjectLayout.astro
  components/             # SiteHeader, PostCard, ProjectCard, PromoBanner,
                          #   ProseStyles + TocScript (shared by both article layouts)
  styles/global.css       # Tailwind v4 (@import "tailwindcss"), @theme fonts, @font-face, component classes
  pages/
    index.astro about.astro posts.astro talks.astro investing.astro 404.astro
    atom.xml.js           # RSS feed → /atom.xml
    [...slug].astro       # dynamic post route → /YYYY/MM/DD/<slug>/
    projects/index.astro  # /projects/ listing
    projects/[slug].astro # /projects/<slug>/
  posts/  git/ tech/ life/ languages/    # posts; folder = category
  projects/               # one md/mdx file per project; filename = slug
public/
  assets/…                # served at /assets/... (images, covers, projects, fonts, talks)
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
Tailwind v4's cascade layers so they don't leak into the chrome). Those prose
styles and the TOC script live in `components/ProseStyles.astro` and
`components/TocScript.astro` so `ProjectLayout` gets the same treatment — edit
them there, not in a layout.

## Projects

`/projects/` lists side projects; each drills into `/projects/<slug>/`. One
`src/projects/<slug>.{md,mdx}` per project — **the filename is the whole slug**
(no date prefix, unlike posts). MDX works the same as it does for posts.

```yaml
---
title: "TicGit"
description: "One sentence; used on the card, the page lede, and social meta."
image: /assets/images/projects/<slug>.svg
year: "2008 → today"     # free text, it's display copy
lang: Rust               # optional
status: active           # active | archived — drives the section and the chip
repo: https://github.com/schacon/ticgit   # optional
site: https://ticgit.dev                  # optional
post: /2020/08/07/hungarian-desks/        # optional, a related post on this site
sort: 11                 # lower first within a section; default 100
---
```

`index.astro` splits on `status` into "Currently" and "The back catalog", and
ends with a hand-maintained `more` array of repos that don't warrant a page.
`ProjectLayout.astro` mirrors `PostLayout.astro` minus the dates and banner,
with repo/site/post links in the right rail (repeated below the article on
narrow screens, where the rail is hidden).

## Cover images

Every post and project gets a bespoke, content-specific **SVG cover**:
`public/assets/images/covers/<slug>.svg` for posts,
`public/assets/images/projects/<slug>.svg` for projects, referenced by `image:`
front matter.

```bash
python3 _tools/generate-covers.py     # writes covers/*.svg and projects/*.svg
_tools/rasterize-covers.sh            # every .svg → .png (for social cards)
_tools/rasterize-covers.sh projects   # just one dir, to avoid churning the other
```

**Posts and projects deliberately look different.** Post covers use the `Cover`
toolkit: soft category-tinted field, faint grid, soft blobs, a detailed flat
illustration and an italic tagline (per-category palette in `PAL`: git=orange,
tech=indigo, life=teal/green, lang=rose). Add one by writing a scene function
and registering it in `SCENES`.

Project covers use the `Poster` toolkit instead: **one flat saturated field, two
or three oversized geometric shapes, and no type at all** (palette in `PP`).
They have to survive as a thumbnail in the grid and as a 240px rail image, so
keep it to a few big primitives — `disc`, `ring`, `bar`, `tri`, `wedge`, `band`,
`half` — and nothing thinner than about 14px. Add one by writing a function that
returns `poster.render(label)` and registering it in the `PROJECT_POSTERS` dict
under the project's slug. Spread the field colours so no two cards that land
next to each other in the grid share one.

Both: self-contained SVG (no external resources or web fonts — they don't load
in an `<img>`), and keep content vertically centered for the 1.91:1 social crop.

**Social cards need PNG** (Twitter/OG don't render SVG), so always re-run
`rasterize-covers.sh` after changing covers — the meta tags point at the `.png`.
It uses `rsvg-convert` when that's on `PATH` (every existing PNG came from it)
and otherwise falls back to `_tools/rasterize-covers.mjs`, which renders with
`sharp`. The two rasterizers differ very slightly, so pass a single directory
rather than re-rendering PNGs you didn't change.

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
