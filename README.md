# scottchacon.com

The source for [scottchacon.com](https://scottchacon.com) — a static site built
with [Astro](https://astro.build). Blog posts can be written in Markdown, MDX
(with embedded React components), or raw HTML.

## Prerequisites

- **Node.js 22+**
- **pnpm** (the package manager). If you don't have it: `corepack enable` (ships
  with Node), or `npm install -g pnpm`.

## Local development

```bash
pnpm install        # install dependencies (first time only)
pnpm dev            # start the dev server → http://localhost:4321
```

The dev server hot-reloads as you edit. Other commands:

```bash
pnpm build          # production build → dist/
pnpm preview        # serve the built dist/ locally (to sanity-check a build)
```

## Project structure

```
src/
  pages/            # routes
    index.astro           → /
    about, posts, talks, investing, 404   → /about/, /posts/, …
    atom.xml.js           → /atom.xml (RSS feed)
    [...slug].astro       → every post at /YYYY/MM/DD/<slug>/
  posts/            # the blog posts, grouped by category folder
    git/  tech/  life/  languages/
  layouts/          # BaseLayout (pages), PostLayout (articles)
  components/       # SiteHeader, PostCard, PromoBanner, React islands
  lib/posts.ts      # loads/sorts posts, parses date+slug, category metadata
  content.config.ts # content collections (md/mdx + a loader for .html posts)
  styles/global.css # Tailwind v4 + fonts + component classes
public/
  assets/           # served verbatim at /assets/... (images, covers, fonts)
  CNAME  .nojekyll  reports/  favicon.ico  apple-touch-icon.png
_tools/             # dev-only scripts (cover generation); never published
```

## Writing a post

Create a file in `src/posts/<category>/YYYY-MM-DD-your-slug.<ext>`. The **folder
is the category** (`git`, `tech`, `life`, `languages`) and the file's **date +
slug become the URL**: `/YYYY/MM/DD/your-slug/`.

Pick any format:

- **Markdown** — `…-your-slug.md`
- **MDX** — `…-your-slug.mdx` — Markdown plus JSX; import and embed React
  components as interactive islands:
  ```mdx
  import Chart from '../../components/Chart.jsx';

  <Chart client:load />
  ```
- **HTML** — `…-your-slug.html` — raw HTML passed through verbatim (a heavy inline
  `<style>` is preserved). Good for one-off, custom-designed posts.

Every post needs front matter:

```yaml
---
title: "Your Post Title"
image: /assets/images/covers/your-slug.svg
excerpt: "One sentence used on cards, the meta description, and social shares."
---
```

Headings (`##`, `###`) automatically populate the article's "On this page"
table of contents.

## Cover images

Each post has a generated SVG cover in `public/assets/images/covers/`. To make
one, add a scene to `_tools/generate-covers.py`, then:

```bash
python3 _tools/generate-covers.py     # → public/assets/images/covers/*.svg
_tools/rasterize-covers.sh            # → *.png (needed for social cards)
```

See [`AGENTS.md`](./AGENTS.md) for the cover toolkit and category details.

## Deployment

Pushing to `master` runs `.github/workflows/deploy.yml`, which builds the site
and publishes `dist/` to the `gh-pages` branch (served at scottchacon.com). No
manual build/upload needed.
