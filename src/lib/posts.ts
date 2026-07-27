import { getCollection, type CollectionEntry } from 'astro:content';

export type PostEntry = CollectionEntry<'posts'> | CollectionEntry<'htmlPosts'>;

export interface Post {
  entry: PostEntry;
  isHtml: boolean;
  id: string;
  category: string;
  slug: string;
  year: string;
  month: string;
  day: string;
  date: Date;
  url: string;
}

/** Parse an entry id like `git/2011-08-31-github-flow` into date/slug/category/url. */
export function parseEntry(entry: PostEntry, isHtml: boolean): Post {
  const id = entry.id;
  const category = id.includes('/') ? id.split('/')[0] : 'writing';
  const name = id.split('/').pop() as string;
  const m = name.match(/^(\d{4})-(\d{2})-(\d{2})-(.+)$/);
  if (!m) throw new Error(`Post id does not match YYYY-MM-DD-slug: ${id}`);
  const [, year, month, day, slug] = m;
  // Parse as UTC to avoid timezone day-shifts in URLs / published dates.
  const date = new Date(Date.UTC(Number(year), Number(month) - 1, Number(day)));
  return {
    entry,
    isHtml,
    id,
    category,
    slug,
    year,
    month,
    day,
    date,
    url: `/${year}/${month}/${day}/${slug}/`,
  };
}

/** All posts (markdown + html) merged and sorted newest-first. */
export async function getAllPosts(): Promise<Post[]> {
  const md = await getCollection('posts');
  const html = await getCollection('htmlPosts');
  const all = [
    ...md.map((e) => parseEntry(e, false)),
    ...html.map((e) => parseEntry(e, true)),
  ];
  all.sort((a, b) => b.date.getTime() - a.date.getTime());
  return all;
}

/** Category → display tag + Tailwind color classes (ported from post-card.html). */
export interface CategoryMeta {
  tag: string;
  tagcls: string;
}

const CATEGORY_META: Record<string, CategoryMeta> = {
  git: { tag: 'Git', tagcls: 'bg-orange-100 text-orange-700 dark:bg-orange-500/20 dark:text-orange-300' },
  tech: { tag: 'Tech', tagcls: 'bg-indigo-100 text-indigo-700 dark:bg-indigo-500/20 dark:text-indigo-300' },
  life: { tag: 'Life', tagcls: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-300' },
  languages: { tag: 'Languages', tagcls: 'bg-rose-100 text-rose-700 dark:bg-rose-500/20 dark:text-rose-300' },
};

export function categoryMeta(category: string): CategoryMeta {
  return (
    CATEGORY_META[category] ?? {
      tag: 'Writing',
      tagcls: 'bg-zinc-100 text-zinc-700 dark:bg-zinc-700 dark:text-zinc-300',
    }
  );
}

/** "Month D, YYYY" (e.g. "August 31, 2011"). */
export function formatDate(date: Date): string {
  return date.toLocaleDateString('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric',
    timeZone: 'UTC',
  });
}

/** Short date "Aug 31, 2011" for cards. */
export function formatShortDate(date: Date): string {
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    timeZone: 'UTC',
  });
}

/** Build-time relative time, matching the old Jekyll thresholds. */
export function relativeTime(date: Date, now: Date = new Date()): string {
  const d = Math.floor((now.getTime() - date.getTime()) / 1000);
  const yr = Math.floor(d / 31557600);
  if (yr >= 1) return yr === 1 ? 'a year ago' : `${yr} years ago`;
  const mo = Math.floor(d / 2629800);
  if (mo >= 1) return mo === 1 ? 'a month ago' : `${mo} months ago`;
  const da = Math.floor(d / 86400);
  if (da >= 1) return da === 1 ? 'yesterday' : `${da} days ago`;
  return 'today';
}

/** Social share image: covers are authored as .svg, but cards need the .png twin. */
export function shareImage(image: string | undefined): string {
  const img = image ?? '/assets/images/title.png';
  return img.replace(/\.svg$/, '.png');
}
