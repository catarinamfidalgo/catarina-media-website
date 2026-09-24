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
        "excerpt": "What a brand video package includes, why cropping a 16:9 film for Instagram "
                   "doesn't work, and what to decide before the shoot. From a video editor who "
                   "gets called in when it wasn't.",
        "body": """
<p class="lede">A brand video package means commissioning the brand film, the short cutdown and
the social versions as one job, before anything is shot. Most people don't. They order the film,
it turns out well, and three weeks later someone asks for the Instagram version.</p>

<p>That's when I usually get the call.</p>

<p>The request sounds small. It isn't. What exists is ninety seconds, 16:9, built around a
voiceover. What's needed is fifteen seconds, 9:16, that works with the sound off. Those aren't
versions of each other. They're different films that happen to share footage.</p>

<h3>Why you can't just crop a brand film for Instagram</h3>

<p>Going from 16:9 to 9:16 throws away about 60% of the frame. Not the edges — the sides, where
most of the composition lives. Your founder sitting slightly off-centre with the product visible
behind her becomes a close-up of her shoulder.</p>

<p>Sometimes I can reframe shot by shot, pushing in and tracking to keep the subject in frame.
It works when there's resolution to spare. It costs a day, and it always looks like what it is:
a wide shot being rescued.</p>

<p>The other problem is sound. Most social video is watched muted, and a film carried by
voiceover says nothing in silence. Subtitles help. They're not the same as a piece that was
built to work without audio in the first place.</p>

<h3>What's included in a brand video package</h3>

<p>When it's planned properly, one shoot produces:</p>

<ul>
  <li><strong>The brand film</strong> — 60 to 120 seconds, 16:9. The full argument. Homepage,
  sales deck, trade show.</li>
  <li><strong>A cutdown</strong> — 15 to 30 seconds. Not the film with the middle removed. Its
  own piece, with its own opening.</li>
  <li><strong>Social cuts</strong> — three to six vertical pieces, 9:16 or 4:5, subtitled,
  usually 10 to 20 seconds each.</li>
</ul>

<p>Some clients also want stills pulled from the footage, or a 6-second bumper for pre-roll. Both
are close to free if you ask before the shoot and expensive afterwards.</p>

<h3>The part almost nobody plans for</h3>

<p>Here's what actually goes wrong, and it isn't the cropping.</p>

<p>When the short cuts are an afterthought, they end up being the same film at three lengths. The
fifteen-second version is the ninety-second version with the middle taken out. Someone who has
seen one has seen all of them — the others just repeat it faster. You paid for three pieces and
published one idea.</p>

<p>Commissioned together, each piece gets to be about something. One opens on the founder. One is
the product being used, no words at all. One is thirty seconds of process, because process
performs and most brands are too polite to show it. Different hooks, different shapes, three
reasons to stop scrolling instead of one reason repeated.</p>

<p>They still have to belong to each other, though. Same grade, same typeface, same world of
music, same rhythm in the cutting. Recognisably yours before the logo appears — but distinct
enough to earn a place in the feed.</p>

<p>That balance can't be found in the edit. Distinct pieces need distinct material, and material
is decided on the shoot day.</p>

<h3>Does a video package cost more?</h3>

<p>Usually less than buying the same pieces separately, and the reason has nothing to do with a
bulk discount. It's that the expensive decisions get made while they're still cheap:</p>

<ul>
  <li>Shots get framed knowing a vertical crop is coming, with headroom and centring built in.</li>
  <li>The interview gets three or four extra questions, asked specifically to give the short cuts
  something to be about.</li>
  <li>Music is licensed once, for every cut and every platform, rather than renegotiated when the
  fourth piece appears.</li>
  <li>Grade and sound are done once across everything instead of being redone each time.</li>
</ul>

<p>Ordering the social cuts six weeks later means a second edit, often a second licence, and
sometimes a second shoot day. That's where the money goes.</p>

<h3>What to ask before the shoot</h3>

<p>If you're commissioning <a href="../../services/">video editing and post-production</a>, these
are worth settling before anyone books a camera:</p>

<ul>
  <li>Every place this video will end up. Write the list down — the obvious ones get forgotten.</li>
  <li>Which pieces, at what lengths, in which aspect ratios.</li>
  <li>Whether the shoot will be framed so vertical crops are compositions rather than rescues.</li>
  <li>Whether the music licence covers every cut on every platform.</li>
  <li>Subtitles: included or not, and in which languages.</li>
</ul>

<p>That last one matters more than people expect if you're running in more than one market. I
work in English, Portuguese and Spanish, and the difference between a subtitle that was
translated and one that was written for the cut is visible.</p>

<h3>So what should you actually commission?</h3>

<p>If the video only ever lives on your website, one film is fine. Buy one film.</p>

<p>If it's going anywhere near social — and it almost always is — decide that now, not in
November. The shoot day is the only moment when adding pieces is cheap.</p>

<p>If you're working out what you need, <a href="../../contact/">tell me what you're planning</a>
and I'll tell you what's worth shooting. That conversation is free and usually saves more than it
costs.</p>
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
