# AGENTS.md

Notes for working on scottchacon.com (a Jekyll site). Focus: blog posts and
their cover images.

## Build & preview

```bash
JEKYLL_ENV=production bundle exec jekyll build   # build to _site/
bundle exec jekyll serve                         # dev server at :4000
```

`_tools/` holds generator scripts and is excluded from the built site
(`exclude:` in `_config.yml`). Nothing in `_tools/` is published.

## Blog posts

Posts live in `_posts/<category>/YYYY-MM-DD-slug.md`. The **folder name is the
category** — currently `git`, `tech`, `life`, and `languages`. To add a new
category, just make a new `_posts/<name>/` folder and add the category to the
places that map categories (see "Categories" below).

Front matter:

```yaml
---
layout: post
title: "The Post Title"
image: /assets/images/covers/<slug>.svg     # the cover (an SVG in covers/)
excerpt: "One-sentence summary; used on cards, the meta description, and social."
---
```

`image` and `excerpt` drive the Writing-page cards (`_includes/post-card.html`),
the article-page sidebar, and the social-share tags. Keep `excerpt` to ~1
sentence. Article section headings (`##` / `###`) auto-populate the sticky
"On this page" table of contents on the article layout.

## Cover images

Every post gets a **bespoke, content-specific SVG cover** — an illustration
that reflects that article's actual topic (e.g. `reset` → Git's three trees,
`hungarian-desks` → a people↔desks matching). They share one visual system
(soft category-tinted background + faint grid + flat gradient vector art) so
they read as a set. Covers are 1200×800 and live in
`assets/images/covers/<slug>.svg`.

### Generating covers

All covers are produced by one script:

```bash
python3 _tools/generate-covers.py     # writes assets/images/covers/*.svg
```

The script is deterministic (no randomness), so re-running reproduces existing
covers byte-for-byte and only adds/changes what you edited.

To add a cover for a **new post**:

1. Open `_tools/generate-covers.py`.
2. Write a scene function using the `Cover` toolkit, e.g.:

   ```python
   def my_post():
       c = Cover("tech")          # category palette: git | tech | life | lang
       p = c.p                    # palette dict: p["a"]..p["f"], p["ink"], p["bg"]
       # ...compose with primitives: c.pill, c.rrect, c.circle, c.ring, c.line,
       #    c.path, c.arrowhead, c.text, c.grad, c.rgrad, c.shadow, c.clip, ...
       c.text(600, 150, "a short caption", 40, p["ink"],
              family="Georgia, serif", weight="700", style="italic")
       save("my-post", c.render("alt text describing the illustration"))
   ```

3. Add the function to the `SCENES` list at the bottom.
4. Run the script, then set the post's `image:` to
   `/assets/images/covers/my-post.svg`.

Design constraints (covers are referenced via `<img>`, so they are isolated):
- **No external resources.** Inline everything; no `<image>`, web fonts, or
  scripts. Text must use generic system families (`Georgia, serif`,
  `'Courier New', monospace`, `sans-serif`) — web fonts won't load in an
  `<img>`-referenced SVG.
- Keep important content roughly centered vertically so a social 1.91:1
  center-crop (see below) doesn't clip it.
- Validate after generating: every file under `covers/` should parse as XML.

### Category palettes

`generate-covers.py` defines a palette per category in `PAL`:

- `git` → warm orange/red, cream background
- `tech` → indigo/blue, light-indigo background
- `life` → teal/green, mint background
- `lang` (the `languages` category) → rose/pink→purple background

Use `Cover("<palette>")` to color a scene. If you add a category, add a matching
palette entry, and give it a tag color in `_includes/post-card.html`.

## Social-share images (rasterize covers to PNG)

Twitter/X, Facebook, and most link-preview scrapers **do not render SVG**. The
article layout's `og:image` / `twitter:image` therefore point at a **PNG**
version of the cover (it swaps `.svg` → `.png`). After generating or changing
any cover, refresh the PNGs:

```bash
_tools/rasterize-covers.sh     # rsvg-convert every covers/*.svg -> covers/*.png (1200px wide)
```

Requires `rsvg-convert` (librsvg). The `.svg` stays the on-site cover (crisp in
browsers); the `.png` is only for social cards. Card type is
`summary_large_image`, and `og:image`/`twitter:image` are emitted as absolute
`https://scottchacon.com/...` URLs (social validators fetch the live URL, so
tags only preview once deployed).

## Categories — where they're referenced

When adding/renaming a category, update:

- `_posts/<category>/` — the folder (source of truth)
- `_includes/post-card.html` — the `case cat` block that maps a category to its
  display tag + Tailwind tag color
- `_tools/generate-covers.py` — `PAL` palette, if the category needs its own look

## Other generators

- `_tools/add-post-frontmatter.py` — one-off helper used to bulk-add
  `image:`/`excerpt:` front matter when importing many posts at once.
- `_tools/generate-hungarian-figures.py` — example of generating **inline body
  illustrations** (not covers) for a specific post; writes standalone SVGs into
  `assets/images/`. Follow this pattern for in-article diagrams: reuse the
  `Cover`-style primitives, but size/save to fit the article column.
