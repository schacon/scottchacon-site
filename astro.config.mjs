// @ts-check
import { defineConfig } from 'astro/config';
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
  integrations: [mdx(), react(), sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
  markdown: {
    rehypePlugins: [rehypeSlug],
    shikiConfig: { theme: 'github-light' },
  },
});
