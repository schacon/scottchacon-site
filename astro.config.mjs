// @ts-check
import { copyFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';

/** The Jekyll-era site served posts at /YYYY/MM/DD/slug.html; emit a copy of
 *  each post at that path so old inbound links still work on GitHub Pages,
 *  which has no server-side redirects. The pages carry a canonical link to
 *  the trailing-slash URL. */
function htmlAliases() {
  return {
    name: 'html-aliases',
    hooks: {
      /** @param {{ dir: URL, pages: { pathname: string }[] }} args */
      'astro:build:done': ({ dir, pages }) => {
        const out = fileURLToPath(dir);
        for (const { pathname } of pages) {
          const post = pathname.match(/^(\d{4}\/\d{2}\/\d{2}\/[^/]+)\/?$/);
          if (!post) continue;
          copyFileSync(
            path.join(out, post[1], 'index.html'),
            path.join(out, `${post[1]}.html`),
          );
        }
      },
    },
  };
}
import mdx from '@astrojs/mdx';
import react from '@astrojs/react';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';
import rehypeSlug from 'rehype-slug';

// https://astro.build
export default defineConfig({
  site: 'https://scottchacon.com',
  trailingSlash: 'always',
  build: { format: 'directory' }, // → /path/index.html pretty URLs
  integrations: [mdx(), react(), sitemap(), htmlAliases()],
  vite: {
    plugins: [tailwindcss()],
  },
  markdown: {
    rehypePlugins: [rehypeSlug],
    shikiConfig: {
      theme: 'github-light',
      // ```small — plain text, rendered at a smaller size (see PostLayout's
      // `pre[data-language="small"]` rule). Useful for wide terminal traces.
      langAlias: { small: 'text' },
    },
  },
});
