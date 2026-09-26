#!/bin/sh
# Build the site from assets/source.html.
#
# The scripts have to run in this order: pages first, since everything else
# edits what it writes; then the translations; then the blog; then the schema
# and sitemap, which read the finished pages.
#
# This exists because the order used to live in someone's head, and a preview
# reorder once sat in source.html for a day without ever reaching the built
# pages, because the build was never re-run.
#
#     ./build.sh            build
#     ./build.sh --check    build, then fail if anything differs from git
#
# --check is the one to run before committing. Editing a generated index.html
# appears to work and goes live, and then the next build silently deletes it.
# That has happened twice. The check turns it into an error you see at once.
#
# Previews are deliberately not built here: they need the masters in
# assets/video/, which are gigabytes and live only on Catarina's Mac.
# Run assets/build_previews.py directly when an in-point changes.
set -e

for s in pages i18n blog schema sitemap; do
  python3 "assets/build_$s.py"
done
echo "  built"

if [ "$1" = "--check" ]; then
  if ! git diff --quiet; then
    echo
    echo "  MISMATCH: generated files do not match the source."
    echo
    echo "  Either something was edited in a built file instead of the source,"
    echo "  or the source changed and this build had not been run."
    echo
    echo "  Edit assets/source.html, assets/site.css or assets/build_*.py,"
    echo "  then run ./build.sh and commit what changes."
    echo
    git diff --name-only | sed 's/^/    /'
    exit 1
  fi
  echo "  check: generated files match the source"
fi
