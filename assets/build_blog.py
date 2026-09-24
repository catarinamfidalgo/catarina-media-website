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
        "slug": "ai-in-the-edit",
        "date": "2026-09-15",
        "date_label": "September 2026",
        "title": "I use AI in the edit. It doesn't do the editing.",
        "excerpt": "Clients have started asking whether AI can just do this now. "
                   "Here's the honest answer from inside the edit — what it genuinely helps with, "
                   "and the part it can't touch.",
        "body": """
<p class="lede">Clients have started asking me whether AI can just do this now. It's a fair
question and it deserves a straight answer rather than a defensive one, so here it is from
inside the edit.</p>

<p>I do use AI. Most editors I know do. But it does none of the editing, and the distinction
matters if you're the one paying for the result.</p>

<h3>What it's genuinely good at</h3>

<p>The honest list is longer than people who sell editing like to admit:</p>

<ul>
  <li><strong>Transcription.</strong> Two hours of interview becomes searchable text in minutes. This used to be an afternoon.</li>
  <li><strong>Rough selects.</strong> Point it at ten interviews and ask where somebody talks about pricing, and it will find the moments.</li>
  <li><strong>Audio cleanup.</strong> Room tone, hum, a bad lavalier — these are solved problems now.</li>
  <li><strong>Masking and rotoscoping.</strong> Work that was genuinely tedious and is now mostly not.</li>
  <li><strong>Subtitle timing.</strong> Still needs checking, but the first pass is close.</li>
</ul>

<p>Notice what those have in common. They're all <strong>labour</strong>. None of them is a
decision. Every one is a job I was happy to stop doing by hand, and none of them is the reason
a client hires me.</p>

<h3>What it can't do</h3>

<p><strong>Decide what the film is about.</strong> Ten interviews don't contain one story until
somebody chooses which one to tell. That choice isn't in the footage — it comes from
understanding what the client needs the film to achieve, which is usually not what the brief
says.</p>

<p><strong>Know which take carries it.</strong> Two takes can be identical on paper. One of
them lands and the other doesn't. The difference is a half-second of hesitation before an
answer, or an eye-line that reads as honest. A model scoring transcripts picks the clearest
sentence. The clearest sentence is often the least true one.</p>

<p><strong>Hold a pace.</strong> Knowing when to sit on a shot two seconds longer than is
comfortable, and when to cut away before the viewer is ready — that's the whole craft. It's
felt, against a specific audience, in a specific context.</p>

<p><strong>Be accountable.</strong> When a piece goes out under a brand's name, someone has to
have made the calls and be able to defend them.</p>

<h3>Where it actually goes wrong</h3>

<p>The failures are rarely dramatic. Nothing explodes. It's that the tool is confidently
slightly wrong, in ways you only catch if you already know what right looks like.</p>

<p><strong>Transcription outside English.</strong> I work in English, Portuguese and Spanish,
and the gap is obvious. English transcripts come back near-perfect. Portuguese comes back
readable but wrong in the places that matter — names, industry terms, and anything where a
speaker switches languages mid-sentence, which in my work happens constantly. It doesn't flag
uncertainty. It writes a plausible word and moves on. If you cut from the transcript without
watching, you'll cut a sentence the person didn't say.</p>

<p><strong>Selects that optimise for clarity.</strong> Ask a tool for the best answer to a
question and it returns the most articulate one. But in a testimonial, the most articulate
answer is often the most rehearsed, and rehearsed doesn't persuade. The take you want is
usually the one where somebody pauses, corrects themselves, and then says the true thing. On a
transcript that looks like the worse option.</p>

<p><strong>Auto-reframe.</strong> Useful for turning a landscape cut into vertical, right up
until the moment two people are talking and it decides which one matters. It follows movement,
not meaning, so it will drift off the person listening — and in an interview, the reaction is
frequently the shot.</p>

<p><strong>Noise reduction pushed too far.</strong> It's excellent at removing hum. It is also
happy to remove the room, and a voice with no room around it sounds like a voice in a box.
Nobody can say why the video feels cheap; it just does.</p>

<p><strong>Automatic colour matching.</strong> It will make your shots consistent by making
them average. If the look was deliberate — warm, cool, deliberately flat — average is exactly
wrong.</p>

<p>None of this makes the tools bad. It makes them tools. Every one of these is fine when
somebody is watching the output and knows what they're looking for.</p>

<h3>How I use it</h3>

<p>Sparingly, and always pointed at something. A transcript so I can navigate an interview by
text instead of scrubbing. Noise reduction on a take that's otherwise the best one. Never for
the structure, never for the selects, never for the pacing.</p>

<p>The tool is fast at the parts that were slow. It's useless at the parts that were hard.</p>

<h3>If you're the one hiring</h3>

<p>An AI-assembled edit tends to look fine the first time you watch it and hollow the second.
The cuts are on the beat, the information is present, and nothing quite lands. If your video
exists to persuade somebody — to trust a brand, to take a training seriously, to book
something — then pacing <em>is</em> the persuasion, and that's precisely the part nothing has
automated.</p>

<p>Use the tools. Just don't confuse the labour with the work.</p>
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
<link rel="stylesheet" href="{root}assets/site.css?v=b8e000f2">

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
