import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';
import type { Loader } from 'astro/loaders';
import matter from 'gray-matter';
import { glob as tinyglob } from 'tinyglobby';
import { readFile } from 'node:fs/promises';

const POSTS_BASE = 'src/posts';

// Shared front-matter schema for every post, regardless of authoring format.
const schema = z.object({
  title: z.string(),
  image: z.string().optional(),
  excerpt: z.string().optional(),
  layout: z.string().optional(),
});

// Markdown / MDX posts use Astro's built-in pipeline (remark/rehype, MDX + React).
const posts = defineCollection({
  loader: glob({ pattern: '**/*.{md,markdown,mdx}', base: `./${POSTS_BASE}` }),
  schema,
});

// Raw-HTML posts: Astro's glob loader doesn't render `.html` bodies, and some of
// these embed a large inline <style> that must survive verbatim (no MDX/JSX
// parsing, no escaping). This loader parses the front matter and stores the raw
// body so the post route can inject it with `set:html`.
function htmlLoader(): Loader {
  return {
    name: 'html-posts',
    async load({ store, parseData, generateDigest }) {
      store.clear();
      const files = await tinyglob('**/*.html', { cwd: POSTS_BASE });
      for (const rel of files) {
        const full = `${POSTS_BASE}/${rel}`;
        const raw = await readFile(full, 'utf8');
        const { data, content } = matter(raw);
        const id = rel.replace(/\.html$/, ''); // e.g. git/2011-07-11-reset
        const parsed = await parseData({ id, data, filePath: full });
        store.set({
          id,
          data: parsed,
          body: content,
          filePath: full,
          digest: generateDigest(raw),
          rendered: { html: content },
        });
      }
    },
  };
}

const htmlPosts = defineCollection({ loader: htmlLoader(), schema });

export const collections = { posts, htmlPosts };
