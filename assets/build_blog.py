#!/usr/bin/env python3
"""Render the blog from POSTS below.

Plain HTML out, no build tools, no dependencies — GitHub Pages serves it as-is.
Each post gets its own directory so the URL is /blog/<slug>/ rather than a .html
file, which reads better and is what search engines index.

    python3 assets/build_blog.py
"""
import os, re, html

SITE = "https://catarina.media"


# Blog chrome, per language. The main site's strings live in assets/i18n_pt.py;
# these are the handful the blog needs, kept here so the blog builds on its own.
NAV = {
    "en": {"tag": "Editing &amp; post-production", "home": "Home", "portfolio": "Portfolio",
           "services": "Services", "about": "About", "agencies": "For Agencies",
           "blog": "Blog", "contact": "Contact", "cta": "Start a project",
           "rights": "All rights reserved", "back": "All posts",
           "index_title": "Blog", "index_lede": "Notes on editing, post-production, and working with video."},
    "pt": {"tag": "Edição e pós-produção", "home": "Início", "portfolio": "Portfólio",
           "services": "Serviços", "about": "Sobre", "agencies": "Para Agências",
           "blog": "Blog", "contact": "Contacto", "cta": "Começar um projeto",
           "rights": "Todos os direitos reservados", "back": "Todos os artigos",
           "index_title": "Blog", "index_lede": "Notas sobre edição, pós-produção e trabalhar com vídeo."},
}

POSTS = [
    {
        "slug": "brand-video-package",
        "date": "2026-09-24",
        "date_label": "September 2026",
        "title": "One film isn't enough: what a brand video package actually includes",
        "excerpt": "Most brands commission a single film, then spend the next month trying to "
                   "cut it into something that works on Instagram. Here's what to ask for "
                   "instead, and why deciding it before the shoot costs less than fixing it after.",
        "body": """
<p class="lede">Most of the work I get asked to rescue starts the same way. A brand commissions
one film. It comes out well. Then someone asks for the Instagram version, and the whole thing
has to be taken apart.</p>

<p>The film was shot to be watched once, in widescreen, with sound. What's needed now is
fifteen seconds, vertical, and legible with the sound off. Those aren't the same film, and no
amount of editing turns one into the other cleanly.</p>

<h3>What actually goes wrong</h3>

<p>It's rarely the edit. It's decisions that were made months earlier, on set, by people who
weren't thinking about a phone screen.</p>

<ul>
  <li><strong>The framing doesn't survive the crop.</strong> A beautifully composed wide shot
  with your product on the left and your founder on the right becomes, in vertical, a shot of
  neither. Cropping to 9:16 throws away three quarters of the frame, and it's never the
  quarter you'd have chosen.</li>
  <li><strong>There's no room to cut.</strong> A 90-second film built as one continuous
  argument has no natural 15-second piece inside it. Every possible cut ends mid-thought.</li>
  <li><strong>It doesn't work silent.</strong> Most social video is watched with the sound off.
  If the message lives in a voiceover and nothing on screen carries it, the film says nothing
  to the majority of people who see it.</li>
  <li><strong>The music licence doesn't cover it.</strong> Track licensed for one film, one
  platform. Now it's on six cuts across three channels, and either the licence is extended or
  everything gets rescored.</li>
</ul>

<p>Each of these is fixable in post. All of them are cheaper to avoid.</p>

<h3>What a package actually is</h3>

<p>A brand video package means deciding, before anyone shoots anything, that you're making
several finished pieces from one production. Usually:</p>

<ul>
  <li><strong>The brand film.</strong> 60 to 120 seconds. The full argument. This is what goes
  on your homepage and gets sent to people who already want to know more.</li>
  <li><strong>A trailer or cutdown.</strong> 15 to 30 seconds. Not a shortened version of the
  film — a different piece with its own shape, made to stop someone scrolling.</li>
  <li><strong>Social cuts.</strong> Three to six vertical pieces, each built around one idea.
  Subtitled, legible silent, sized for where they're going.</li>
</ul>

<p>The word that matters is <em>before</em>. Planned in advance, the same shoot day yields all
of it. Decided afterwards, you're either cropping badly or booking a second day.</p>

<h3>Why it costs less</h3>

<p>People assume a package costs more because it's more deliverables. It usually costs less
than buying the same pieces separately, for reasons that are all about the shoot rather than
the edit:</p>

<ul>
  <li>Shots get framed with the crop in mind — subject centred, space left top and bottom, so
  the vertical version is a real composition rather than a salvage job.</li>
  <li>The interview gets two or three extra questions, specifically to give the short cuts
  something to be about.</li>
  <li>Enough B-roll is shot to cover cuts that don't exist yet.</li>
  <li>Music is licensed once, for everything, at the start.</li>
  <li>The colour and sound work is done once across all the pieces instead of being repeated
  each time something new is ordered.</li>
</ul>

<p>[Catarina — a real example here would carry this whole piece. A project where the package
was planned up front versus one where the social cuts were an afterthought, and what the
difference actually looked like.]</p>

<h3>What to ask for</h3>

<p>If you're commissioning, these are the questions worth asking before the shoot rather than
after:</p>

<ul>
  <li>What are all the places this video will end up? List them, including the ones that feel
  obvious.</li>
  <li>Which pieces do we need, at what lengths and what aspect ratios?</li>
  <li>Will the shoot be framed so vertical crops work?</li>
  <li>Does the music licence cover every cut, on every platform?</li>
  <li>Are subtitles included, and in which languages?</li>
  <li>Who owns the project files if we want more cuts next year?</li>
</ul>

<p>That last one catches more people than it should. [Catarina — worth a line here on how you
handle project files, since it's a real differentiator and most clients never think to ask.]</p>

<h3>The short version</h3>

<p>One film is a deliverable. A package is a plan. The plan costs less, because the expensive
decisions — framing, coverage, music, language — get made while they're still cheap to make.</p>

<p>If you're working out what you actually need, I'm happy to talk it through before anyone
quotes you anything.</p>
"""
    },
]

PAGE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Catarina Fidalgo</title>
<meta name="description" content="{excerpt}">
<link rel="canonical" href="{canonical}">
{alts}
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<!-- Raster sizes too: Google's favicon crawler prefers them, and iOS
     uses the touch icon for a home-screen bookmark. -->
<link rel="icon" href="{root}assets/favicon-96.png" type="image/png" sizes="96x96">
<link rel="icon" href="{root}assets/favicon-48.png" type="image/png" sizes="48x48">
<link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{excerpt}">
<meta property="og:url" content="{canonical}">
<link rel="stylesheet" href="{root}assets/site.css?v=fbe4c606">

<!-- Google Analytics (GA4), behind consent.
     Analytics sets a cookie, so under EU law it may not run until the visitor
     agrees. Nothing here loads until consent is stored: no script is fetched,
     no cookie is written, no request reaches Google. Declining is remembered
     too, so the bar is not shown again.
     The choice lives in localStorage, not a cookie — storing a consent record
     in a cookie you have not yet been allowed to set is its own problem. -->
<script>
  (function () {{
    var GA_ID = "G-DS7JJYXNM5";
    var KEY = "cm-consent";

    function load() {{
      if (!/^G-[A-Z0-9]+$/.test(GA_ID) || window.__gaLoaded) return;
      window.__gaLoaded = true;
      var s = document.createElement("script");
      s.async = true;
      s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
      document.head.appendChild(s);
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () {{ window.dataLayer.push(arguments); }};
      window.gtag("js", new Date());
      window.gtag("config", GA_ID, {{ anonymize_ip: true }});
    }}

    function stored() {{
      try {{ return localStorage.getItem(KEY); }} catch (e) {{ return null; }}
    }}

    // Exposed so the bar and the privacy page can call them.
    window.setConsent = function (yes) {{
      try {{ localStorage.setItem(KEY, yes ? "granted" : "denied"); }} catch (e) {{}}
      var bar = document.getElementById("cookieBar");
      if (bar) bar.hidden = true;
      if (yes) load();
    }};

    window.resetConsent = function () {{
      try {{ localStorage.removeItem(KEY); }} catch (e) {{}}
      var bar = document.getElementById("cookieBar");
      if (bar) bar.hidden = false;
    }};

    if (stored() === "granted") load();

    // Show the bar only when no choice has been made yet.
    document.addEventListener("DOMContentLoaded", function () {{
      if (stored()) return;
      var bar = document.getElementById("cookieBar");
      if (bar) bar.hidden = false;
    }});
  }})();
</script>
<script>
  /* Applied before the page paints, so a dark-theme visitor never sees a
     white flash. An explicit choice is remembered; otherwise the system
     setting decides and nothing is stamped on the element. */
  (function () {{
    try {{
      var t = localStorage.getItem("cm-theme");
      if (t === "dark" || t === "light") document.documentElement.setAttribute("data-theme", t);
    }} catch (e) {{}}
    window.toggleTheme = function () {{
      var el = document.documentElement, cur = el.getAttribute("data-theme");
      if (!cur) {{
        cur = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
      }}
      var next = cur === "dark" ? "light" : "dark";
      el.setAttribute("data-theme", next);
      try {{ localStorage.setItem("cm-theme", next); }} catch (e) {{}}
    }};
  }})();
</script>
</head>
<body>
{header}
{main}
{footer}
  <script>
  function toggleNav(b){{var n=document.getElementById('siteNav');
    var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o);}}
  function closeNav(){{var n=document.getElementById('siteNav'),b=document.querySelector('.nav-toggle');
    if(n)n.classList.remove('open'); if(b)b.setAttribute('aria-expanded','false');}}
  document.addEventListener('click',function(e){{if(!e.target.closest('header.site'))closeNav();}});
  document.addEventListener('keydown',function(e){{if(e.key==='Escape')closeNav();}});
  </script>
</body>
</html>
"""

def header(root, lang, other):
    """Blog chrome. `other` is the URL of this page in the other language, or
    None when it has not been translated — in which case the switcher points
    at that language's blog index rather than a page that does not exist."""
    nav = NAV[lang]
    pre = "" if lang == "en" else "pt/"
    switch = ('<span class="lang-current" aria-current="true">EN</span>'
              '<a href="%s">PT</a>' % (other or (root + "pt/blog/"))) if lang == "en" else \
             ('<a href="%s">EN</a>'
              '<span class="lang-current" aria-current="true">PT</span>' % (other or (root + "blog/")))
    return f"""  <div class="lang-bar">
    <div class="container">
      <div class="lang-switch" aria-label="Language">{switch}</div>
    </div>
  </div>
  <div class="container">
    <header class="site">
      <div class="brand-block">
        <div class="brand"><a href="{root}{pre}">Catarina <i>Fidalgo</i></a></div>
        <span class="brand-tag">{nav['tag']}</span>
      </div>
      <button class="theme-toggle" type="button" onclick="toggleTheme()"
              aria-label="Light or dark" title="Light or dark">
        <svg class="icon-light" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.2 5.2l1.4 1.4M17.4 17.4l1.4 1.4M18.8 5.2l-1.4 1.4M6.6 17.4l-1.4 1.4"/></svg>
        <svg class="icon-dark" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8.2 8.2 0 0 1 9.5 4a8.3 8.3 0 1 0 10.5 10.5z"/></svg>
      </button>
      <button class="nav-toggle" type="button" aria-label="Menu" aria-expanded="false" aria-controls="siteNav" onclick="toggleNav(this)"><span></span><span></span><span></span></button>
      <nav class="main" id="siteNav">
        <a href="{root}{pre}">{nav['home']}</a>
        <a href="{root}{pre}#portfolio">{nav['portfolio']}</a>
        <a href="{root}{pre}services/">{nav['services']}</a>
        <a href="{root}{pre}about/">{nav['about']}</a>
        <a href="{root}{pre}agencies/">{nav['agencies']}</a>
        <a href="{root}{pre}blog/" class="active">{nav['blog']}</a>
        <a href="{root}{pre}contact/">{nav['contact']}</a>
      </nav>
    </header>
  </div>"""

def footer(root, lang):
    nav = NAV[lang]
    pre = "" if lang == "en" else "pt/"
    return f"""  <footer class="site">
    <div class="container">
      <div class="foot-brand">
        <div class="foot-logo">Catarina <i>Fidalgo</i></div>
        <div class="foot-tag">Made in the edit</div>
        <div class="copy">&copy; 2026 Catarina Fidalgo &middot; {nav['rights']}</div>
      </div>
      <div class="foot-cta">
        <a class="btn btn--ghost-light" href="{root}{pre}contact/">{nav['cta']}</a>
      </div>
    </div>
  </footer>"""

def content(post, lang):
    """A post's fields for one language. English lives at the top level; other
    languages sit in a nested dict, absent until the post is translated."""
    return post if lang == "en" else post[lang]


def langs_of(post):
    return ["en"] + [l for l in ("pt",) if l in post]


def hreflang(paths):
    """paths: {lang: url}. Emitted only where a post exists in more than one
    language — claiming a translation that is not there is worse than none."""
    if len(paths) < 2:
        return ""
    codes = {"en": "en", "pt": "pt-PT"}
    out = [f'<link rel="alternate" hreflang="{codes[l]}" href="{u}">'
           for l, u in paths.items()]
    out.append(f'<link rel="alternate" hreflang="x-default" href="{paths["en"]}">')
    return "\n".join(out)


def build():
    for lang in ("en", "pt"):
        base = "blog" if lang == "en" else os.path.join("pt", "blog")
        posts = [p for p in POSTS if lang in langs_of(p)]
        if not posts and lang != "en":
            continue
        os.makedirs(base, exist_ok=True)
        nav = NAV[lang]

        # individual posts
        for p in posts:
            c = content(p, lang)
            d = os.path.join(base, p["slug"])
            os.makedirs(d, exist_ok=True)
            root = "../../" if lang == "en" else "../../../"
            urls = {l: (f"{SITE}/blog/{p['slug']}/" if l == "en"
                        else f"{SITE}/{l}/blog/{p['slug']}/") for l in langs_of(p)}
            other = None
            if len(urls) > 1:
                other = urls["pt"] if lang == "en" else urls["en"]
            main = f"""  <div class="container section">
    <article class="article">
      <div class="article-meta">{c['date_label']}</div>
      <h1>{c['title']}</h1>
      {c['body'].strip()}
      <a class="back-link" href="{root}{'' if lang == 'en' else lang + '/'}blog/">&larr; {nav['back']}</a>
    </article>
  </div>"""
            open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(PAGE.format(
                lang="en" if lang == "en" else "pt-PT",
                alts=hreflang(urls),
                title=html.escape(c["title"], quote=True),
                excerpt=html.escape(c["excerpt"], quote=True),
                canonical=urls[lang], root=root,
                header=header(root, lang, other), main=main, footer=footer(root, lang)))

        # index
        root = "../" if lang == "en" else "../../"
        pre = "" if lang == "en" else "pt/"
        items = "\n".join(
            f"""        <li class="post-item"><a href="{root}{pre}blog/{p['slug']}/">
          <div class="post-date">{content(p, lang)['date_label']}</div>
          <h2 class="post-title">{content(p, lang)['title']}</h2>
          <p class="post-excerpt">{content(p, lang)['excerpt']}</p>
        </a></li>""" for p in posts)
        main = f"""  <div class="container section">
    <h2 class="eyebrow">{nav['index_title']}</h2>
    <p class="copy">{nav['index_lede']}</p>
    <ul class="post-list">
{items}
    </ul>
  </div>"""
        index_urls = {"en": f"{SITE}/blog/"}
        if any("pt" in p for p in POSTS):
            index_urls["pt"] = f"{SITE}/pt/blog/"
        other = (index_urls.get("pt") if lang == "en" else index_urls.get("en")) \
            if len(index_urls) > 1 else None
        open(os.path.join(base, "index.html"), "w", encoding="utf-8").write(PAGE.format(
            lang="en" if lang == "en" else "pt-PT",
            alts=hreflang(index_urls),
            title=nav["index_title"], excerpt=nav["index_lede"],
            canonical=index_urls[lang], root=root,
            header=header(root, lang, other), main=main, footer=footer(root, lang)))
        print(f"  built {base}/index.html and {len(posts)} post page(s)")


if __name__ == "__main__":
    build()
