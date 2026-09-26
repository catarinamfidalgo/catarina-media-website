# Working on this repo

Notes for anyone editing this site, human or AI. Written after two changes
were nearly lost, so the first section matters most.

## The site is generated. Do not edit the HTML.

Every `index.html` in this repo is built from `assets/source.html`. Editing one
directly appears to work, and the change even goes live, but the next build
deletes it without a word.

This has happened twice: a portfolio reorder that sat unbuilt for a day, and a
homepage animation that was one build away from disappearing from all three
languages.

**Edit these:**

| File | What it controls |
|------|------------------|
| `assets/source.html` | All page markup, the portfolio data, inline JS |
| `assets/site.css` | All styling |
| `assets/build_*.py` | How pages, translations, blog and metadata are made |
| `assets/i18n_pt.py`, `assets/i18n_es.py` | Translations |

**Then run:**

```sh
./build.sh --check
```

It rebuilds and fails if any generated file differs from what the source
produces. Run it before committing. If it fails, the change went into the
wrong file.

Generated pages open with a banner saying so. If you are editing a file that
starts with `GENERATED FILE`, stop and find the source instead.

## Images

Everything on this site is WebP except the Open Graph image, which has to be
JPEG or PNG because some scrapers will not take WebP.

Before adding an image, check what it weighs. The homepage fairy arrived as a
151KB PNG referenced twice, above the fold, which is 302KB before anything
else loads. The same picture as WebP with its transparency intact is 39KB.

- Give every `<img>` a `width` and `height`, so the page does not jump as it loads
- Anything below the fold gets `loading="lazy"`
- Large images get a `srcset`, as the blog hero does
- Decorative images get `alt=""` and their container `aria-hidden="true"`

## Two purples, and only two

```
--purple-deep  #7259c4     the buttons
--purple-light #a98bef     the hero title
```

Tints are four fixed steps, `--tint-1` to `--tint-4`. Do not introduce a new
purple or a new opacity; use the nearest step.

`--accent` and `--lav-bright` swap in dark mode, which is correct for text but
collapses any gradient built from the pair into a flat fill. For a gradient,
use `--purple-deep` and `--purple-light`, which do not swap.

## Things already handled, so do not undo them

- `prefers-reduced-motion` is respected by the hero drift, the card previews and the fairy
- `header.site` sticks via `.lang-bar + .container`, not the header itself. Its old parent was only as tall as it was, so it had nowhere to travel
- `overflow-x` is `clip`, never `hidden`. `hidden` creates a scroll container and silently disables sticky descendants
- The contact form posts to an Apps Script and falls back to `mailto:`. The address is never in the markup
- `generate_lead` fires only on a confirmed send, not on click. It used to fire on click, which would have reported conversions for enquiries that never arrived

## Ask before changing these

Some things here look like defects and are decisions:

- **The masthead is two rows**, name above, pages beneath, tagline visible. It was made one centred row once, with the tagline hidden to save space. That is not the design.
- **The tagline sits 0.028em right of the wordmark's ink**, not flush. Exact alignment was tried and reads as wrong, because a round `C` has to overshoot to look level.
- **Portfolio cards are square-cornered.** The grid is meant to read as frames on a timeline.
- **Preview in-points are hand-picked** in `build_previews.py`. Scene detection chose them once and put half of them on talking heads.

## Previews and shapes

`assets/build_previews.py` and `assets/build_aspects.py` need the video masters
in `assets/video/`, which are gigabytes and not in the repo. They are run by
hand on Catarina's machine, not from `build.sh`. Their output is committed.
