#!/usr/bin/env python3
"""Generate sitemap.xml and robots.txt from the pages that exist.

Google will crawl the site without these, but a sitemap tells it which pages
are canonical and — the part that matters here — which pages are translations
of each other. Without the hreflang pairs, the English, Portuguese and Spanish
homepages look like three near-duplicate pages competing with each other rather
than one page in three languages.

Run after build_pages.py and build_i18n.py.

    python3 assets/build_sitemap.py
"""
import os, pathlib, datetime, re

SITE = "https://catarina.media"
ROOT = pathlib.Path(".")

# Pages that exist in all three languages, keyed by the English path.
TRANSLATED = ["", "services/", "about/", "agencies/", "contact/"]
LANGS = {"en": "", "pt": "pt/", "es": "es/"}

# Rough sense of how often each changes, and how much it matters.
PRIORITY = {"": "1.0", "contact/": "0.8", "services/": "0.8",
            "agencies/": "0.7", "about/": "0.7", "blog/": "0.6"}


def lastmod(path):
    f = ROOT / path / "index.html"
    if not f.exists():
        return None
    return datetime.date.fromtimestamp(f.stat().st_mtime).isoformat()


def url_block(loc, alts=None, priority="0.5"):
    out = ["  <url>", "    <loc>%s</loc>" % loc]
    lm = lastmod(loc[len(SITE):].strip("/"))
    if lm:
        out.append("    <lastmod>%s</lastmod>" % lm)
    for hreflang, href in (alts or []):
        out.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>'
                   % (hreflang, href))
    out.append("    <priority>%s</priority>" % priority)
    out.append("  </url>")
    return "\n".join(out)


def main():
    urls = []

    # The translated pages, each carrying links to its siblings.
    for page in TRANSLATED:
        alts = [("en", "%s/%s" % (SITE, page)),
                ("pt-PT", "%s/pt/%s" % (SITE, page)),
                ("es-ES", "%s/es/%s" % (SITE, page)),
                ("x-default", "%s/%s" % (SITE, page))]
        for code, prefix in LANGS.items():
            path = prefix + page
            if not (ROOT / path / "index.html").exists():
                continue
            prio = PRIORITY.get(page, "0.5")
            if code != "en":          # translations rank below the original
                prio = "%.1f" % max(0.1, float(prio) - 0.1)
            urls.append(url_block("%s/%s" % (SITE, path), alts, prio))

    # Everything else that exists but is English-only — the blog, mainly.
    seen = {prefix + p for p in TRANSLATED for prefix in LANGS.values()}
    for f in sorted(ROOT.rglob("index.html")):
        path = str(f.parent).replace("\\", "/")
        path = "" if path == "." else path + "/"
        if path in seen or path.startswith(".git"):
            continue
        urls.append(url_block("%s/%s" % (SITE, path),
                              priority=PRIORITY.get(path, "0.5")))

    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
           + "\n".join(urls) + "\n</urlset>\n")
    pathlib.Path("sitemap.xml").write_text(xml, encoding="utf-8")

    robots = ("User-agent: *\n"
              "Allow: /\n"
              "\n"
              "Sitemap: %s/sitemap.xml\n" % SITE)
    pathlib.Path("robots.txt").write_text(robots, encoding="utf-8")

    print("  sitemap.xml — %d urls" % len(urls))
    print("  robots.txt")


if __name__ == "__main__":
    main()
