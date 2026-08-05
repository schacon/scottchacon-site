import { getCollection, type CollectionEntry } from 'astro:content';

export type ProjectEntry = CollectionEntry<'projects'>;

export interface Project {
  entry: ProjectEntry;
  slug: string;
  url: string;
}

/** All projects in display order (`sort` front matter, then title). */
export async function getAllProjects(): Promise<Project[]> {
  const entries = await getCollection('projects');
  const all = entries.map((entry) => ({
    entry,
    slug: entry.id,
    url: `/projects/${entry.id}/`,
  }));
  all.sort(
    (a, b) =>
      a.entry.data.sort - b.entry.data.sort ||
      a.entry.data.title.localeCompare(b.entry.data.title),
  );
  return all;
}

/** Status → display label + Tailwind color classes, mirroring `categoryMeta()`. */
export interface StatusMeta {
  label: string;
  cls: string;
}

export function statusMeta(status: 'active' | 'archived'): StatusMeta {
  return status === 'active'
    ? {
        label: 'Active',
        cls: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-300',
      }
    : {
        label: 'Archived',
        cls: 'bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400',
      };
}
