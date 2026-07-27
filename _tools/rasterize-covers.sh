#!/usr/bin/env bash
# Rasterize each SVG cover to a PNG for social-share cards (Twitter/OG do not
# render SVG). Output is the same basename with a .png extension, 1200px wide
# (covers are 1200x800, so height stays 800). Re-run after regenerating covers.
set -euo pipefail
cd "$(dirname "$0")/../public/assets/images/covers"
shopt -s nullglob
for svg in *.svg; do
  png="${svg%.svg}.png"
  rsvg-convert -w 1200 "$svg" -o "$png"
  echo "rasterized $png"
done
