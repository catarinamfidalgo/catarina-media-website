#!/usr/bin/env python3
"""Add structured data (JSON-LD) to the built pages.

Without it Google sees a page of HTML and has to infer what the site is about.
With it, the facts are stated: a person, named, who does this work, from here,
in these languages, reachable at this address. That is what lets a site be
understood as an entity rather than a document, and it is invisible to readers.

Everything here is already stated in the page copy — nothing is invented, and
nothing is claimed that the site does not say in words.

Run after build_pages.py / build_i18n.py / build_blog.py.

    python3 assets/build_schema.py
"""
import json, pathlib, re

SITE = "https://catarina.media"
PERSON_ID = SITE + "/#catarina"
SITE_ID = SITE + "/#website"

SERVICES = ["Video Editing", "Color Grading", "Motion Graphics & Animation",
            "Sound Design & Mixing", "Subtitling & Localization",
            "Licensed Music & Stock"]

LANGS = {"en": "en", "pt": "pt-PT", "es": "es-ES"}


def person():
    return {
        "@type": "Person",
        "@id": PERSON_ID,
        "name": "Catarina Fidalgo",
        "url": SITE + "/",
        "image": SITE + "/assets/img/catarina-portrait.jpg",
        "jobTitle": "Video Editor",
        "description": ("Video editor and post-production, based in Portugal. "
                        "Commercials, brand films, YouTube, social and corporate "
                        "video, in English, Portuguese and Spanish."),
        "address": {"@type": "PostalAddress", "addressCountry": "PT"},
        # There is another Catarina Fidalgo working in design in Portugal.
        # sameAs is how the two are told apart: it states which accounts
        # belong to this person, so the profiles and the site resolve to one
        # entity rather than to a name that several people share.
        "sameAs": [
            "https://www.youtube.com/@catarinamedia",
            "https://www.instagram.com/catarina.media/",
        ],
        "knowsLanguage": [
            {"@type": "Language", "name": "English", "alternateName": "en"},
            {"@type": "Language", "name": "Portuguese", "alternateName": "pt"},
            {"@type": "Language", "name": "Spanish", "alternateName": "es"},
        ],
        "knowsAbout": SERVICES,
    }


def website(lang):
    return {
        "@type": "WebSite",
        "@id": SITE_ID,
        "url": SITE + "/",
        "name": "Catarina Fidalgo",
        "inLanguage": lang,
        "publisher": {"@id": PERSON_ID},
    }


def service():
    return {
        "@type": "ProfessionalService",
        "name": "Catarina Fidalgo — Video Editing and Post-Production",
        "url": SITE + "/services/",
        "provider": {"@id": PERSON_ID},
        "areaServed": "Worldwide",
        "availableLanguage": ["en", "pt", "es"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Post-production services",
            "itemListElement": [
                {"@type": "Offer",
                 "itemOffered": {"@type": "Service", "name": s}}
                for s in SERVICES
            ],
        },
    }


def graph_for(path, lang):
    nodes = [person(), website(lang)]
    if path.rstrip("/").endswith("services"):
        nodes.append(service())
    return {"@context": "https://schema.org", "@graph": nodes}


def lang_of(path):
    first = path.split("/")[0]
    return LANGS.get(first, "en")


def main():
    root = pathlib.Path(".")
    n = 0
    for f in sorted(root.rglob("index.html")):
        if ".git" in f.parts:
            continue
        path = "" if f.parent == root else str(f.parent).replace("\\", "/")
        html = f.read_text(encoding="utf-8")

        # Replace any previous block so this is safe to re-run.
        html = re.sub(r'\n<script type="application/ld\+json">.*?</script>', "",
                      html, flags=re.S)

        data = json.dumps(graph_for(path, lang_of(path)),
                          ensure_ascii=False, separators=(",", ":"))
        block = '\n<script type="application/ld+json">%s</script>' % data
        html = html.replace("</head>", block + "\n</head>", 1)
        f.write_text(html, encoding="utf-8")
        n += 1

    print("  structured data on %d pages" % n)


if __name__ == "__main__":
    main()
