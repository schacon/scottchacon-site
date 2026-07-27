import rss from '@astrojs/rss';
import { experimental_AstroContainer as AstroContainer } from 'astro/container';
import { render } from 'astro:content';
import { getAllPosts } from '../lib/posts';

export async function GET(context) {
  const posts = await getAllPosts();
  const container = await AstroContainer.create();

  const items = [];
  for (const post of posts) {
    let content = post.entry.data.excerpt ?? '';
    try {
      if (post.isHtml) {
        content = post.entry.body ?? content;
      } else {
        const { Content } = await render(post.entry);
        content = await container.renderToString(Content);
      }
    } catch {
      // fall back to the excerpt if a post can't be rendered to a string
    }
    items.push({
      title: post.entry.data.title,
      link: post.url,
      pubDate: post.date,
      description: post.entry.data.excerpt ?? '',
      content,
    });
  }

  return rss({
    title: 'Scott Chacon',
    description: 'Writing from Scott Chacon — Git, languages, technology, and life.',
    site: context.site ?? 'https://scottchacon.com',
    items,
    customData: '<language>en-us</language>',
  });
}
