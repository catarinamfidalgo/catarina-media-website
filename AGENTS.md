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
- **Bump the `site.css?v=` token whenever site.css changes.** It lives in two
  places, `assets/source.html` and `assets/build_blog.py`, and they must match.
  Forgetting it means the browser keeps the old stylesheet, so a new rule
  simply does not exist: a freshly added element renders unstyled and it looks
  like the CSS is wrong rather than stale. This has already cost one round trip
  over a signature that appeared black and full-size because its rule was in a
  stylesheet nobody had re-fetched.
- **Bump the `site.css?v=` token whenever site.css changes.** It lives in two
  places, `assets/source.html` and `assets/build_blog.py`, and they must match.
  Forgetting it means the browser keeps the old stylesheet, so a new rule
  simply does not exist: a freshly added element renders unstyled and it looks
  like the CSS is wrong rather than stale. This has already cost one round trip
  over a signature that appeared black and full-size because its rule was in a
  stylesheet nobody had re-fetched.
- `generate_lead` fires only on a confirmed send, not on click. It used to fire on click, which would have reported conversions for enquiries that never arrived

## Ask before changing these

Some things here look like defects and are decisions:

- **The masthead is two rows**, name above, pages beneath, tagline visible. It was made one centred row once, with the tagline hidden to save space. That is not the design.
- **The tagline sits 0.028em right of the wordmark's ink**, not flush. Exact alignment was tried and reads as wrong, because a round `C` has to overshoot to look level.
- **Portfolio cards are square-cornered.** The grid is meant to read as frames on a timeline.
- **Preview in-points are hand-picked** in `build_previews.py`. Scene detection chose them once and put half of them on talking heads.

## The fairy

Four of these were real bugs. They are cheap to reintroduce.

**The hover runs on `.hero-fairy`, the flight on `.hero-fairy-figure`.**
Two transform animations on one element do not compose: the later one wins
outright. Put the drift on the figure and the landing is discarded the moment
it starts.

**The dress layer is a second copy of the whole drawing, clipped.** It was
once clipped from 48% across and 39% down, which takes in the extended right
arm and both legs, so moving it moved copies of them and she grew spare limbs.
Clip to the streaming tail only, past the arm and above the knees.

**There is no feet layer, on purpose.** A foot cannot move independently of
the leg it belongs to without tearing at the ankle.

**There is no dust layer, on purpose.** It sat at the destination with no
offset and fired while she was still flying in, so specks glowed over the word
a second before she arrived.

**Every loop pauses when she is off-screen** via `.is-idle` and an
IntersectionObserver, and again when the tab is hidden.
`animation-play-state` holds the frame rather than resetting.

**Clicking the word is a round trip**: poof out where she is, then poof in at
the far right and fly across. The hover is stopped before she leaves and
restarted with a 3.8s delay so it waits for the landing.

**`prefers-reduced-motion` hides her entirely** and disables the click.

**The word is not focusable, deliberately.** The sequence plays on load
without input, so a keyboard user misses nothing, and a tab stop for an easter
egg is an obstacle in front of people for something that tells them nothing.

## Previews and shapes

`assets/build_previews.py` and `assets/build_aspects.py` need the video masters
in `assets/video/`, which are gigabytes and not in the repo. They are run by
hand on Catarina's machine, not from `build.sh`. Their output is committed.
