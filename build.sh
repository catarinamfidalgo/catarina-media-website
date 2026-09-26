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
#     ./build.sh
#
# Previews are deliberately not built here: they need the masters in
# assets/video/, which are gigabytes and live only on Catarina's Mac.
# Run assets/build_previews.py directly when an in-point changes.
set -e
for s in pages i18n blog schema sitemap; do
  python3 "assets/build_$s.py"
done
echo "  built"
