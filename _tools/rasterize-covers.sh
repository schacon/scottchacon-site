#!/usr/bin/env bash
# Rasterize each SVG cover to a PNG for social-share cards (Twitter/OG do not
# render SVG). Output is the same basename with a .png extension, 1200px wide
# (covers are 1200x800, so height stays 800). Re-run after regenerating covers.
#
#   rasterize-covers.sh              # both image dirs
#   rasterize-covers.sh projects     # just one, to avoid churning the others
set -euo pipefail

# rsvg-convert is preferred (it produced every existing PNG), but it's an extra
# brew install; fall back to sharp, which ships with the site's deps already.
if ! command -v rsvg-convert >/dev/null 2>&1; then
  echo "rsvg-convert not found — falling back to sharp"
  exec node "$(dirname "$0")/rasterize-covers.mjs" "$@"
fi

cd "$(dirname "$0")/../public/assets/images"
shopt -s nullglob
# covers/ = post covers, projects/ = /projects/ card + page art.
for dir in "${@:-covers projects}"; do
  [ -d "$dir" ] || continue
  for svg in "$dir"/*.svg; do
    png="${svg%.svg}.png"
    rsvg-convert -w 1200 "$svg" -o "$png"
    echo "rasterized $png"
  done
done
