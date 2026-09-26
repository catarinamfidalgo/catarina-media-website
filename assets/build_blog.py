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
        "title": "One campaign, every platform: commission it all at once",
        "excerpt": "A campaign that runs across several platforms works better commissioned as one "
                   "job. What cohesion actually means, where separate commissions drift, and what "
                   "you end up with.",
        "pt": {
            "date_label": "Setembro de 2026",
            "title": "Uma campanha, várias plataformas: encomende tudo de uma vez",
            "excerpt": "Uma campanha que corre em várias plataformas funciona melhor encomendada como "
                       "um só trabalho. O que é a coerência, onde é que as encomendas separadas "
                       "se desviam, e o que fica pronto no fim.",
            "body": """
<p class="lede">Uma campanha já não vive num só sítio. A mesma ideia tem de funcionar no site, no
feed do LinkedIn, como reel vertical e, às vezes, em seis segundos antes de um vídeo no YouTube.
São filmes diferentes. O erro está em encomendá-los como trabalhos diferentes.</p>

<p>Encomendados um de cada vez, deixam de parecer uma campanha. Primeiro o filme, os reels uns
meses depois, qualquer coisa para uma feira mais para a frente. Três campanhas feitas por três
pessoas, que normalmente é exatamente o que são.</p>

<h3>O que é, na prática, uma campanha incoerente</h3>

<p>Raramente é uma coisa evidente. É um desvio lento.</p>

<p>A cor está ligeiramente mais quente no segundo lote, porque o trabalho foi feito seis meses
depois noutro monitor. Os oráculos usam uma tipografia que não é bem a da marca, porque quem os
fez não tinha o ficheiro. A música é outra, porque a licença original cobria um filme e não uma
campanha, e por isso os reels parecem ser de outra empresa qualquer.</p>

<p>Ninguém que veja isto consegue dizer o que está errado. Simplesmente não liga as peças umas às
outras, e o resultado é que cada peça tem de apresentar a marca do zero. É a repetição que faz uma
campanha ficar na memória, e só há repetição se as pessoas reconhecerem a segunda coisa como
pertencendo à primeira.</p>

<h3>Coerentes, mas não iguais</h3>

<p>É aqui que está a tensão, e é nisto que consiste o trabalho.</p>

<p>As peças têm de ser reconhecivelmente da mesma campanha: a mesma cor, a mesma tipografia, o
mesmo mundo sonoro, o mesmo ritmo de montagem. Quem vê deve perceber que é a marca antes sequer
de aparecer o logótipo.</p>

<p>Mas não podem ser o mesmo filme em durações diferentes. Essa é a outra falha, e é igualmente
comum. Quando as versões curtas são cortadas a partir da longa, a peça de quinze segundos é a de
noventa sem o meio. Quem viu uma viu todas. Pagaram-se quatro peças e publicou-se uma ideia.</p>

<p>Coerentes no aspeto, distintas no conteúdo. Uma abre no CEO. Outra mostra o produto a ser
usado, sem uma única palavra. Outra são trinta segundos de processo. A mesma família, funções
diferentes.</p>

<h3>Onde é que as encomendas separadas se desviam</h3>

<p>A coerência dificilmente se acrescenta no fim. Depende sobretudo de decisões tomadas antes, e
cada uma delas é barata à primeira e cara à segunda:</p>

<ul>
  <li><strong>Uma cor só, com as mesmas referências.</strong> Igualar seis meses depois um
  tratamento de cor feito noutro projeto é adivinhar.</li>
  <li><strong>Uma licença de música</strong> que cubra todos os cortes em todas as plataformas,
  em vez de uma faixa nova de cada vez porque a anterior não estava autorizada para aquilo.</li>
  <li><strong>Um conjunto de grafismos</strong> (títulos, oráculos, animação de logótipo), feito
  uma vez e reutilizado, em vez de refeito ligeiramente diferente a cada ronda.</li>
  <li><strong>Material feito a saber que todos os formatos vinham a caminho.</strong> Uma
  composição 16:9 perde cerca de 60% do enquadramento num corte 9:16, e o que se perde são os
  lados, que é onde costuma estar a composição.</li>
</ul>

<p>É por causa deste último que me escrevem. Às vezes consigo reenquadrar plano a plano, a aproximar
e a acompanhar o movimento para manter o sujeito no quadro. Resulta quando sobra resolução, leva
um dia de trabalho, e continua a ler-se como um plano aberto salvo à pressa.</p>

<h3>O que fica pronto</h3>

<p>Encomendado como um só trabalho, o mesmo material dá:</p>

<ul>
  <li><strong>O filme de marca</strong>, ou brand film: 60 a 120 segundos, em 16:9. O argumento
  completo.</li>
  <li><strong>O trailer</strong>: 30 a 45 segundos. Condensa o argumento em qualquer coisa que se
  aguenta sozinha, e não num filme encurtado.</li>
  <li><strong>O teaser</strong>: 10 a 15 segundos. Um só gancho, feito para que alguém olhe.</li>
  <li><strong>Os reels</strong>: três a seis peças verticais, em 9:16 ou 4:5, legendadas, feitas
  para funcionar sem som.</li>
</ul>

<p>Fotografias e um bumper de 6 segundos para pré-roll saem quase de graça, se o material o
permitir.</p>

<h3>O que decidir à partida</h3>

<p>Nada disto é da minha competência, mas é o que decide o que consigo fazer depois. Vale a pena
resolver isto com quem produz o material:</p>

<ul>
  <li>Todas as plataformas onde a campanha vai correr. Convém escrever a lista, porque são sempre
  as óbvias que se esquecem.</li>
  <li>Que peças, com que durações e em que formatos.</li>
  <li>Se o material vai ser enquadrado já a contar com os cortes verticais.</li>
  <li>Se a licença de música cobre todos os cortes em todas as plataformas.</li>
  <li>Legendas: incluídas, e em que línguas.</li>
</ul>

<h3>Em resumo</h3>

<p>Se o vídeo só vai viver no site, encomende um filme e está bem assim. Se vai correr em várias
plataformas, e vai quase sempre, encomende a campanha toda de uma vez. Não por causa do
orçamento, embora normalmente também compense, mas porque a coerência não se acrescenta depois.</p>

<p>Se está a preparar alguma coisa, <a href="../../contact/">diga-me o que tem em mãos</a> e
digo-lhe o que pedir, e o que me faz falta para construir a campanha inteira a partir daí. Essa parte já é <a href="../../services/">comigo</a>.</p>
""",
        },
        "body": """
<p class="lede">A campaign doesn't live in one place any more. The same idea has to work on your
homepage, in a LinkedIn feed, as a vertical reel, and sometimes as six seconds before a YouTube
video. Those are different films. The mistake is commissioning them as different jobs.</p>

<p>Ordered one at a time, they stop looking like one campaign. The film first, the reels a few
months later, something for a trade show after that. Three campaigns by three people, which is
usually exactly what they are.</p>

<h3>What incoherence actually looks like</h3>

<p>It's rarely dramatic. It's drift.</p>

<p>The grade is slightly warmer in the second batch, because it was done six months later on a
different monitor. The lower-thirds use a typeface that isn't quite the brand one, because
whoever made them didn't have the file. The music is a different track, because the original
licence covered one film and not a campaign, so the reels feel like they belong to another
company.</p>

<p>Nobody watching could tell you what's wrong. They just don't connect the pieces to each other,
which means every piece has to do the work of introducing you from scratch. Repetition is what
makes a campaign stick, and repetition only happens if people recognise the second thing as
belonging to the first.</p>

<h3>Cohesive, but not identical</h3>

<p>Here's the tension, and it's the whole job.</p>

<p>The pieces have to be recognisably the same campaign: same grade, same typography, same world
of music, same rhythm in the cutting. Someone should know it's you before the logo appears.</p>

<p>But they can't be the same film at different lengths. That's the other failure, and it's just
as common. When the short versions are cut down from the long one, the fifteen-second piece is
the ninety-second piece with the middle removed. Anyone who has seen one has seen them all. You
paid for four pieces and published one idea.</p>

<p>Cohesive in look, distinct in content. One opens on the CEO. One is the product being used,
no words at all. One is thirty seconds of process. Same family, different jobs.</p>

<h3>Where separate commissions drift</h3>

<p>Cohesion is hard to add at the end. It is mostly decided by things that happen before, and
each of them is cheap once and expensive twice:</p>

<ul>
  <li><strong>One grade, one set of references.</strong> Matching a grade you did six months ago
  from a different project file is guesswork.</li>
  <li><strong>One music licence</strong> covering every cut on every platform, rather than a new
  track each time because the old one wasn't cleared for this.</li>
  <li><strong>One set of motion assets</strong> (titles, lower-thirds, logo animation), built
  once and reused, instead of rebuilt slightly differently each round.</li>
  <li><strong>Material made knowing every format was coming.</strong> A wide 16:9 composition
  loses about 60% of the frame in a 9:16 crop, and it's the sides that go, which is where the
  composition usually lives.</li>
</ul>

<p>That last one is the one that reaches me. Sometimes I can reframe shot by shot, pushing in
and tracking to keep the subject in frame. It works when there's resolution to spare, it costs a
day, and it still reads as a wide shot being rescued.</p>

<h3>What you end up with</h3>

<p>Commissioned as one job, the same material gives:</p>

<ul>
  <li><strong>The brand film</strong>: 60 to 120 seconds, 16:9. The full argument.</li>
  <li><strong>The trailer</strong>: 30 to 45 seconds. Condenses the argument into something that
  stands on its own rather than a shortened film.</li>
  <li><strong>The teaser</strong>: 10 to 15 seconds. One hook, built to make someone look.</li>
  <li><strong>The reels</strong>: three to six vertical pieces, 9:16 or 4:5, subtitled, built to
  work with the sound off.</li>
</ul>

<p>Stills and a 6-second pre-roll bumper come nearly free if the material allows it.</p>

<h3>What to settle up front</h3>

<p>None of this is my department, but it decides what I can do afterwards. Worth settling with
whoever is making the material:</p>

<ul>
  <li>Every platform this campaign will run on. Write the list, because the obvious ones get
  forgotten.</li>
  <li>Which pieces, at what lengths, in which aspect ratios.</li>
  <li>Whether the material is framed knowing vertical crops are coming.</li>
  <li>Whether the music licence covers every cut on every platform.</li>
  <li>Subtitles: included, and in which languages.</li>
</ul>

<h3>The short version</h3>

<p>If the video only ever lives on your website, buy one film. If it's going to run across
platforms, and it almost always is, commission the whole campaign at once. Not to save money,
though it usually does, but because cohesion cannot be retrofitted.</p>

<p>If you're planning something, <a href="../../contact/">tell me what you have in mind</a> and
I'll tell you what to ask for, and what I'd need to build the whole campaign from it. That part is <a href="../../services/">my department</a>.</p>
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
<link rel="icon" href="/favicon.ico?v=3" sizes="any">
<!-- Exact sizes for every surface that asks, so nothing is scaled: 16 and 32
     are the tab at 1x and 2x, which is where a resized 96 looked soft. -->
<link rel="icon" href="/assets/favicon-16.v3.png" type="image/png" sizes="16x16">
<link rel="icon" href="/assets/favicon-32.v3.png" type="image/png" sizes="32x32">
<link rel="icon" href="/assets/favicon-48.v3.png" type="image/png" sizes="48x48">
<link rel="icon" href="/assets/favicon-96.v3.png" type="image/png" sizes="96x96">
<link rel="icon" href="/assets/favicon-192.v3.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.v3.png">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{excerpt}">
<meta property="og:url" content="{canonical}">
<link rel="stylesheet" href="{root}assets/site.css?v=2c535739">

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
    // Browsers remember where you were on a page and put you back there on
    // your next visit. For a one-screen page that means arriving halfway down
    // the contact form with the heading already scrolled past. Turn it off and
    // start at the top unless the URL actually asks for a section.
    if ("scrollRestoration" in history) history.scrollRestoration = "manual";
    if (!location.hash) window.scrollTo(0, 0);
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
<script>
  (function () {{
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
      <button class="theme-toggle" type="button" onclick="toggleTheme()"
              aria-label="Light or dark" title="Light or dark">
        <svg class="icon-light" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.2 5.2l1.4 1.4M17.4 17.4l1.4 1.4M18.8 5.2l-1.4 1.4M6.6 17.4l-1.4 1.4"/></svg>
        <svg class="icon-dark" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8.2 8.2 0 0 1 9.5 4a8.3 8.3 0 1 0 10.5 10.5z"/></svg>
      </button>
    </div>
  </div>
  <div class="container">
    <header class="site">
      <div class="brand-block">
        <div class="brand"><a href="{root}{pre}">Catarina <i>Fidalgo</i></a>
      </div>
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
        <div class="foot-service">Video Editing &amp; Post-Production</div>
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
