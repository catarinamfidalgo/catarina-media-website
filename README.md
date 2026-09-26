# catarina.media

Source for [catarina.media](https://catarina.media), the site for Catarina Fidalgo,
video editor and post-production, based in Portugal. Static HTML, no framework,
served from GitHub Pages.

## Building

Every page is generated from one master file, `assets/source.html`:

```sh
./build.sh
```

That runs five scripts in the order they depend on:

| Script | What it writes |
|--------|----------------|
| `build_pages.py` | The English pages, each cut from the master |
| `build_i18n.py` | The Portuguese and Spanish translations |
| `build_blog.py` | The blog index and post pages, in both languages |
| `build_schema.py` | JSON-LD structured data on every page |
| `build_sitemap.py` | `sitemap.xml` with hreflang pairs, and `robots.txt` |

Edit `assets/source.html` or `assets/site.css`, run `./build.sh`, commit what changes.
Editing a generated `index.html` directly will not survive the next build.

## Previews

The portfolio cards play a short clip on hover. `assets/build_previews.py` cuts them
from the masters, which are gigabytes and stay out of the repo, so this one is run by
hand rather than from `build.sh`:

```sh
python3 assets/build_previews.py          # skips what already exists
python3 assets/build_previews.py --force  # redo everything
```

Scene detection picks the start point, except where a hand-picked one is listed in
`OVERRIDES`. It finds cuts, but it cannot tell which moment is worth showing.

## Contact form

No backend and no third-party form service. `assets/contact.js` builds a `mailto:`
link from the fields and hands it to the visitor's mail client. The address is stored
base64-encoded and decoded at send time, so it appears nowhere in the markup for a
scraper to read.

## Running locally

```sh
python3 -m http.server 8000   # then open http://localhost:8000
```

## Languages

English, Portuguese and Spanish. The translations live in `assets/build_i18n.py` and
are generated, not maintained as separate files.
