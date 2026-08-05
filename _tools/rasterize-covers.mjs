#!/usr/bin/env node
// Fallback rasterizer used by rasterize-covers.sh when `rsvg-convert` isn't on
// PATH. Renders each SVG to a 1200px-wide PNG with sharp (already a dependency
// via Astro's image pipeline). Output matches rsvg-convert's dimensions; glyph
// rendering can differ very slightly, so prefer rsvg-convert when it's around.
import { readdir, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const IMAGES = path.join(fileURLToPath(new URL('.', import.meta.url)), '..', 'public', 'assets', 'images');
const dirs = process.argv.slice(2);

for (const dir of dirs.length ? dirs : ['covers', 'projects']) {
  const full = path.join(IMAGES, dir);
  const exists = await stat(full).then(() => true, () => false);
  if (!exists) continue;
  for (const name of (await readdir(full)).filter((f) => f.endsWith('.svg'))) {
    const svg = path.join(full, name);
    const png = svg.replace(/\.svg$/, '.png');
    await sharp(svg, { density: 144 }).resize(1200).png().toFile(png);
    console.log(`rasterized ${dir}/${path.basename(png)}`);
  }
}
