// @ts-check
import { writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';

/** The Jekyll-era site served posts at /YYYY/MM/DD/slug.html; emit a redirect
 *  stub at each of those paths so old inbound links still work. GitHub Pages
 *  can't send a real 301, but an instant meta refresh plus a canonical link is
 *  treated as a permanent redirect by search engines. */
function htmlRedirects() {
  return {
    name: 'html-redirects',
    hooks: {
      /** @param {{ dir: URL, pages: { pathname: string }[] }} args */
      'astro:build:done': ({ dir, pages }) => {
        const out = fileURLToPath(dir);
        for (const { pathname } of pages) {
          const post = pathname.match(/^(\d{4}\/\d{2}\/\d{2}\/[^/]+)\/?$/);
          if (!post) continue;
          const to = `/${post[1]}/`;
          writeFileSync(
            path.join(out, `${post[1]}.html`),
            `<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<title>Redirecting…</title>
<link rel="canonical" href="https://scottchacon.com${to}">
<meta http-equiv="refresh" content="0; url=${to}">
</head>
<body>
<p>This page has moved to <a href="${to}">https://scottchacon.com${to}</a>.</p>
</body>
</html>
`,
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
  integrations: [mdx(), react(), sitemap(), htmlRedirects()],
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
