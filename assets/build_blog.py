#!/usr/bin/env python3
"""Render the blog from POSTS below.

Plain HTML out, no build tools, no dependencies - GitHub Pages serves it as-is.
Each post gets its own directory so the URL is /blog/<slug>/ rather than a .html
file, which reads better and is what search engines index.

    python3 assets/build_blog.py
"""
import os, re, html

BANNER = '<!-- GENERATED FILE - DO NOT EDIT.\n     Built from assets/source.html by ./build.sh.\n     Anything written here is deleted the next time the build runs.\n     Edit assets/source.html or assets/site.css, then run ./build.sh. -->\n'

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
        "slug": "what-to-send-your-editor",
        "image": "what-to-send",
        "image_alt": "A purple set of drawers holding film strips, a waveform, music, "
                     "stills and color swatches",
        "date": "2026-09-28",
        "date_label": "September 2026",
        "title": "What to send me so the first cut is close",
        "excerpt": "Most of what slows an edit down is decided before the files are opened. What "
                   "actually helps: everything rather than a selection, originals rather than "
                   "exports, and the handful of things that take five minutes to send.",
        "pt": {
            "date_label": "Setembro de 2026",
            "title": "O que me mandar para o primeiro corte ficar perto",
            "excerpt": "A maior parte do que atrasa uma montagem decide-se antes de os ficheiros "
                       "serem abertos. O que ajuda mesmo: tudo em vez de uma seleção, originais em "
                       "vez de exportações, e as poucas coisas que levam cinco minutos a mandar.",
            "body": """
<p class="lede">A maior parte do que atrasa uma montagem decide-se antes de eu abrir os ficheiros.
Depende do que chegou.</p>
<p>Isto não tem que ver com o material ser bom. Tem que ver com virem as coisas certas com ele.</p>

<h3>Para que serve, antes do que lá está</h3>
<p>Onde vai passar e que duração tem de ter moldam a montagem mais do que o próprio material.</p>
<p>Um filme de noventa segundos para o site e um corte de quinze segundos para redes sociais pagas
são peças diferentes. Começam de maneira diferente. Nas redes tem cerca de um segundo e meio antes
de alguém fazer scroll. No seu site as pessoas dão-lhe mais tempo. Se precisa dos dois, diga-o
logo. Montar um e adaptá-lo depois demora mais e funciona pior.</p>
<p>Se ainda não sabe a duração, diga isso. Muda a forma como eu monto e não é um problema.</p>

<h3>Mande tudo, não só as partes boas</h3>
<p>É isto que custa mais tempo.</p>
<p>É tentador passar os brutos e mandar só as takes de que gostou. As partes de que preciso são
muitas vezes as que cortaria. O segundo antes de alguém começar a falar. A pausa em que baixa os
olhos. Os doze segundos enquanto a câmara assenta.</p>
<p>O mesmo para o b-roll que lhe parece aborrecido. Um corredor vazio não é interessante por si e é
capaz de salvar uma transição.</p>
<p>Mande o cartão todo. O volume não me incomoda.</p>

<h3>Originais, não exportações</h3>
<p>Mande os ficheiros tal como saíram da câmara. Não uma cópia comprimida, não uma coisa que passou
pelo WhatsApp e, de preferência, não uma reexportação de outra montagem.</p>
<p>Cada exportação deita informação fora. Não se vê a olhar para o ficheiro. Vê-se assim que o plano
leva grading, é abrandado ou ampliado para um corte vertical.</p>
<p>Se só existe uma cópia comprimida, dá para trabalhar. Só é preciso dizê-lo cedo.</p>

<h3>O som está provavelmente num ficheiro à parte</h3>
<p>Se alguém levava lapela, ou havia boom, essas gravações costumam viver em ficheiros separados.
Mande-os. O som da câmara é um recurso de emergência. O diálogo é aquilo que se perdoa menos.</p>
<p>Se não tem a certeza de que existe som à parte, pergunte a quem filmou.</p>

<h3>Coisas de marca, e uma palavra sobre música</h3>
<p>Cada uma destas leva cinco minutos a mandar e muito mais a reconstruir:</p>
<ul>
  <li><strong>Um logótipo vetorial.</strong> SVG, AI ou EPS. Não um PNG tirado do site.</li>
  <li><strong>As suas fontes</strong>, se a licença permitir partilhá-las, e os códigos de cor ou o
  manual de marca.</li>
  <li><strong>Alguma indicação sobre música</strong>, mesmo vaga. "Calma, sem vozes, nada
  corporativo" chega perfeitamente. Licencio a partir de bibliotecas pagas, por isso a procura é
  comigo.</li>
  <li><strong>A licença de música que já tenha</strong>, se existir. Uma licença para um filme
  muitas vezes não cobre as versões para redes, e isso costuma aparecer na semana em que era para
  publicar.</li>
  <li><strong>Duas ou três referências</strong>, com uma frase sobre o que gosta nelas. Um link
  sozinho só me diz que gostou.</li>
</ul>
<p>Se houver um estilo que não quer mesmo, diga também. É igualmente útil.</p>

<h3>Quem aprova</h3>
<p>Uma pessoa com a palavra final, ou um grupo que mande as notas em conjunto. Cinco pessoas a
responder em separado, cada uma a uma versão diferente, é o que acrescenta dias a um projeto.</p>

<h3>Em resumo</h3>
<ul>
  <li><strong>Tudo</strong>, não uma seleção</li>
  <li><strong>Sem exportar</strong>, direto do cartão</li>
  <li><strong>Som à parte</strong>, se existir</li>
  <li><strong>Logótipo vetorial</strong>, fontes, cores</li>
  <li><strong>Duração e plataforma</strong>, mesmo por alto</li>
  <li><strong>Duas ou três referências</strong>, com uma frase cada</li>
  <li><strong>Um nome</strong> para as aprovações</li>
</ul>
<p>Faça isso e o primeiro corte fica perto o suficiente para se falar dele a sério.</p>
""",
        },
        "body": """
<p class="lede">Most of what slows an edit down is decided before I open the files. It comes down to
what arrived.</p>
<p>None of this is about the footage being good. It's about the right things coming with it.</p>

<h3>What it's for, before what's in it</h3>
<p>Where it runs and how long it has to be shape the edit more than the material does.</p>
<p>A ninety-second film for your homepage and a fifteen-second cut for paid social are different
pieces. They open differently. On social you have about a second and a half before someone
scrolls. On your own site people will give you longer. If you need both, say so at the start.
Cutting one and adapting it afterwards takes longer and works less well.</p>
<p>If you don't know the length yet, say that. It changes how I assemble and it isn't a problem.</p>

<h3>Send everything, not the good bits</h3>
<p>This is the one that costs the most time.</p>
<p>It's tempting to go through the rushes and send only the takes you liked. The parts I need are
often the ones you'd cut. The second before someone starts speaking. The pause where they look
down. The twelve seconds while the camera settles.</p>
<p>Same with b-roll you think is boring. An empty corridor isn't interesting on its own and it will
probably save a transition.</p>
<p>Send the whole card. I don't mind the volume.</p>

<h3>Originals, not exports</h3>
<p>Send the files as they came off the camera. Not a compressed copy, not something that's been
through WhatsApp, and ideally not a re-export from another edit.</p>
<p>Every export throws away data. You won't see it watching the file. You will see it once the shot
is graded, slowed down, or scaled up for a vertical crop.</p>
<p>If a compressed copy is all that exists, that's workable. Just say so early.</p>

<h3>The audio is probably a separate file</h3>
<p>If anyone wore a lav mic, or there was a boom, those recordings usually live as separate files.
Send them. Camera audio is a backup. Dialogue is what viewers forgive least.</p>
<p>If you're not sure whether separate audio exists, ask whoever shot it.</p>

<h3>Brand things, and a word about music</h3>
<p>Each of these takes five minutes to send and much longer to reconstruct:</p>
<ul>
  <li><strong>A vector logo.</strong> SVG, AI or EPS. Not a PNG pulled off the website.</li>
  <li><strong>Your fonts</strong>, if the license covers sharing them, and your color codes or the
  brand guide.</li>
  <li><strong>Something about music</strong>, even vague. "Calm, no vocals, nothing corporate" is
  enough to work from. I license from paid libraries, so the searching is mine.</li>
  <li><strong>The existing music license</strong>, if there is one. A license for one film often
  doesn't cover the social versions of it, and that tends to surface the week you're meant to
  publish.</li>
  <li><strong>Two or three references</strong>, with a sentence about what you like in them. A link
  on its own only tells me you liked it.</li>
</ul>
<p>If there's a style you actively don't want, say that too. It's just as useful.</p>

<h3>Who signs it off</h3>
<p>One person with final say, or a group who send their notes together. Five people replying
separately, each to a different version, is what adds days to a project.</p>

<h3>The short version</h3>
<ul>
  <li><strong>Everything</strong>, not a selection</li>
  <li><strong>Unexported</strong>, straight off the card</li>
  <li><strong>Separate audio</strong>, if it exists</li>
  <li><strong>A vector logo</strong>, fonts, colors</li>
  <li><strong>Length and platform</strong>, even roughly</li>
  <li><strong>A couple of references</strong>, with a sentence each</li>
  <li><strong>One name</strong> for approvals</li>
</ul>
<p>Do that and the first cut will be close enough to talk about properly.</p>
""",
    },
    {
        "slug": "brand-video-package",
        "image": "one-campaign",
        "image_alt": "An editing timeline in purple with clips and a waveform, "
                     "beside film frames and a color wheel",
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
license covered one film and not a campaign, so the reels feel like they belong to another
company.</p>

<p>Nobody watching could tell you what's wrong. They just don't connect the pieces to each other,
which means every piece has to do the work of introducing you from scratch. Repetition is what
makes a campaign stick, and repetition only happens if people recognize the second thing as
belonging to the first.</p>

<h3>Cohesive, but not identical</h3>

<p>Here's the tension, and it's the whole job.</p>

<p>The pieces have to be recognizably the same campaign: same grade, same typography, same world
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
  <li><strong>One music license</strong> covering every cut on every platform, rather than a new
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
  <li>Whether the music license covers every cut on every platform.</li>
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
<title>{title} - Catarina Fidalgo</title>
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
{og_image}
<link rel="stylesheet" href="{root}assets/site.css?v=blog-hero">

<!-- Google Analytics (GA4), behind consent.
     Analytics sets a cookie, so under EU law it may not run until the visitor
     agrees. Nothing here loads until consent is stored: no script is fetched,
     no cookie is written, no request reaches Google. Declining is remembered
     too, so the bar is not shown again.
     The choice lives in localStorage, not a cookie - storing a consent record
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
</body>
</html>
"""

def header(root, lang, other):
    """Blog chrome. `other` is the URL of this page in the other language, or
    None when it has not been translated - in which case the switcher points
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
    language - claiming a translation that is not there is worse than none."""
    if len(paths) < 2:
        return ""
    codes = {"en": "en", "pt": "pt-PT"}
    out = [f'<link rel="alternate" hreflang="{codes[l]}" href="{u}">'
           for l, u in paths.items()]
    out.append(f'<link rel="alternate" hreflang="x-default" href="{paths["en"]}">')
    return "\n".join(out)



def index_og(posts):
    """The blog index has no picture of its own, so it borrows the newest
    post's. Without this, sharing /blog/ falls back to the site-wide portrait,
    which says nothing about what the page is."""
    for p in posts:
        if p.get("image"):
            img = p["image"]
            return (f'<meta property="og:image" content="{SITE}/assets/img/blog/{img}-og.jpg">\n'
                    f'<meta property="og:image:width" content="1200">\n'
                    f'<meta property="og:image:height" content="630">\n'
                    f'<meta name="twitter:card" content="summary_large_image">\n'
                    f'<meta name="twitter:image" content="{SITE}/assets/img/blog/{img}-og.jpg">')
    return ""


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
            img = p.get("image")
            hero = ""
            og_image = ""
            if img:
                alt = html.escape(p.get("image_alt", ""), quote=True)
                hero = (f"""<figure class="post-hero">
          <img src="{root}assets/img/blog/{img}-1400.webp"
               srcset="{root}assets/img/blog/{img}-640.webp 640w, """
                        f"""{root}assets/img/blog/{img}-900.webp 900w, """
                        f"""{root}assets/img/blog/{img}-1400.webp 1400w"
               sizes="(max-width: 560px) 100vw, 520px"
               width="1672" height="941" alt="{alt}" fetchpriority="high">
        </figure>""")
                og_image = (f'<meta property="og:image" content="{SITE}/assets/img/blog/{img}-og.jpg">\n'
                            f'<meta property="og:image:width" content="1200">\n'
                            f'<meta property="og:image:height" content="630">\n'
                            f'<meta name="twitter:card" content="summary_large_image">\n'
                            f'<meta name="twitter:image" content="{SITE}/assets/img/blog/{img}-og.jpg">')

            main = f"""  <div class="container section">
    <article class="article">
      <div class="article-meta">{c['date_label']}</div>
      <h1>{c['title']}</h1>
      {hero}
      {c['body'].strip()}
      <a class="back-link" href="{root}{'' if lang == 'en' else lang + '/'}blog/">&larr; {nav['back']}</a>
    </article>
  </div>"""
            open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(BANNER + PAGE.format(
                lang="en" if lang == "en" else "pt-PT",
                alts=hreflang(urls),
                title=html.escape(c["title"], quote=True),
                excerpt=html.escape(c["excerpt"], quote=True),
                canonical=urls[lang], root=root, og_image=og_image,
                header=header(root, lang, other), main=main, footer=footer(root, lang)))

        # index
        root = "../" if lang == "en" else "../../"
        pre = "" if lang == "en" else "pt/"
        items = "\n".join(
            f"""        <li class="post-item"><a href="{root}{pre}blog/{p['slug']}/">
          {f'<span class="post-thumb"><img src="{root}assets/img/blog/{p["image"]}-640.webp" width="640" height="360" alt="" loading="lazy"></span>' if p.get("image") else ""}
          <span class="post-text">
            <span class="post-date">{content(p, lang)['date_label']}</span>
            <span class="post-title">{content(p, lang)['title']}</span>
            <span class="post-excerpt">{content(p, lang)['excerpt']}</span>
          </span>
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
        open(os.path.join(base, "index.html"), "w", encoding="utf-8").write(BANNER + PAGE.format(
            lang="en" if lang == "en" else "pt-PT",
            alts=hreflang(index_urls),
            title=nav["index_title"], excerpt=nav["index_lede"],
            canonical=index_urls[lang], root=root, og_image=index_og(posts),
            header=header(root, lang, other), main=main, footer=footer(root, lang)))
        print(f"  built {base}/index.html and {len(posts)} post page(s)")


if __name__ == "__main__":
    build()
