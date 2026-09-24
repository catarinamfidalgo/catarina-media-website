#!/usr/bin/env python3
"""Run the whole build, in the order the steps depend on each other.

build_schema.py edits the built pages rather than the source, so it has to run
last — anything that regenerates a page afterwards would strip the structured
data back out. Running the steps by hand in the wrong order is a silent
failure, which is what this exists to prevent.

    python3 assets/build.py
"""
import subprocess, sys, pathlib

STEPS = [
    ("stamp_css.py",    "hash the stylesheet and hero image"),
    ("build_pages.py",  "compose the English pages from source.html"),
    ("build_i18n.py",   "generate pt/ and es/"),
    ("build_blog.py",   "build the blog"),
    ("build_sitemap.py","sitemap.xml and robots.txt"),
    ("build_schema.py", "structured data — must be last"),
]

here = pathlib.Path(__file__).parent
for script, why in STEPS:
    print("\n· %s — %s" % (script, why))
    r = subprocess.run([sys.executable, str(here / script)], cwd=here.parent)
    if r.returncode != 0:
        sys.exit("\n%s failed; stopping so the site is not left half-built." % script)
print("\nBuilt.")
