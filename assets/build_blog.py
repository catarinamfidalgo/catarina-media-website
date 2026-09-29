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
    "es": {"tag": "Montaje y postproducción", "home": "Inicio", "portfolio": "Portafolio",
           "services": "Servicios", "about": "Sobre mí", "agencies": "Para Agencias",
           "blog": "Blog", "contact": "Contacto", "cta": "Empezar un proyecto",
           "rights": "Todos los derechos reservados", "back": "Todos los artículos",
           "index_title": "Blog", "index_lede": "Notas sobre montaje, postproducción y trabajar con vídeo."}
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
                   "actually helps, what to send originals of, and why music and stock footage "
                   "are not on the list of things you need to find.",
        "pt": {
            "date_label": "Setembro de 2026",
            "title": "O que me mandar para o primeiro corte ficar perto",
            "excerpt": "A maior parte do que atrasa uma montagem decide-se antes de os ficheiros "
                       "serem abertos. O que ajuda mesmo, de que é preciso mandar originais, e "
                       "porque é que a música e o stock não são coisas que tenha de procurar.",
        "body": """
<p class="lede">A maior parte do que atrasa uma montagem decide-se antes de eu abrir os ficheiros.
Depende do que chegou.</p>
<p>Isto não tem que ver com o material ser bom. Tem que ver com virem as coisas certas com ele, e
com algumas que não precisa de mandar de todo.</p>

<h3>Para que serve, antes do que lá está</h3>
<p>Onde vai passar e que duração tem de ter moldam a montagem mais do que o próprio material.</p>
<p>Um filme de noventa segundos para o site e um corte de quinze segundos para redes sociais pagas
são peças diferentes. Começam de maneira diferente. Nas redes tem cerca de um segundo e meio antes
de alguém fazer scroll. No seu site as pessoas dão-lhe mais tempo. Se precisa dos dois, diga-o
logo. Montar um e adaptá-lo depois demora mais e funciona pior.</p>
<p>Se ainda não sabe a duração, diga isso. Muda a forma como eu monto e não é um problema.</p>
<p>Há duas coisas que ficam sempre de fora dos briefings e as duas são baratas no início:</p>
<ul>
  <li><strong>Se tem de funcionar sem som.</strong> Os stands de feiras e os ecrãs de eventos
  passam em loop e sem áudio, e grande parte das redes sociais também. Um vídeo feito para o
  silêncio leva a informação no ecrã em vez de na voz off, e isso muda a montagem, não só os
  títulos. Já fiz peças que nunca iam chegar a ser ouvidas.</li>
  <li><strong>Em que línguas precisa dele.</strong> Legendas ou versões completas em português,
  inglês e espanhol são simples enquanto o projeto está aberto e incómodas depois de estar fechado
  e entregue.</li>
</ul>

<h3>Mande tudo, não só as partes boas</h3>
<p>É isto que custa mais tempo.</p>
<p>É tentador passar os brutos e mandar só as takes de que gostou. As partes de que preciso são
muitas vezes as que cortaria. O segundo antes de alguém começar a falar. A pausa em que baixa os
olhos. Os doze segundos enquanto a câmara assenta.</p>
<p>O mesmo para o b-roll que lhe parece aborrecido. Um corredor vazio não é interessante por si e é
capaz de salvar uma transição.</p>
<p>Mande o cartão todo. O volume não me incomoda.</p>

<h3>Originais, não exportações</h3>
<p>Mande os ficheiros como saíram da câmara. Não uma cópia comprimida, nada que tenha passado pelo
WhatsApp, e de preferência não uma reexportação de outra montagem.</p>
<p>Cada exportação deita dados fora. Não vai notar a ver o ficheiro. Vai notar assim que o plano for
tratado na cor, abrandado ou ampliado para um corte vertical.</p>
<p>Se só existir uma cópia comprimida, dá para trabalhar. Basta dizer-mo cedo.</p>

<h3>O áudio é provavelmente um ficheiro à parte</h3>
<p>Se alguém usou um microfone de lapela, ou se houve boom, essas gravações costumam viver em
ficheiros separados. Mande-os. O áudio da câmara é um backup. O diálogo é o que o público perdoa
menos.</p>
<p>Se não tiver a certeza de que existe áudio separado, pergunte a quem filmou.</p>
<p>Se esteve mais do que uma câmara a gravar, mande todas sem cortes, incluindo as partes em que não
acontece nada. É pelo áudio sobreposto das câmaras que as sincronizo, e os clips já aparados são o
que transforma isso num trabalho manual em vez de automático.</p>

<h3>Coisas da marca</h3>
<p>Cada uma destas leva cinco minutos a mandar e muito mais tempo a reconstruir:</p>
<ul>
  <li><strong>Um logótipo vetorial.</strong> SVG, AI ou EPS. Não um PNG tirado do site.</li>
  <li><strong>As suas fontes</strong>, se a licença permitir partilhá-las, e os códigos de cor ou o
  manual de marca.</li>
  <li><strong>Duas ou três referências</strong>, com uma frase sobre o que gosta nelas. Um link
  sozinho só me diz que gostou.</li>
</ul>
<p>Se houver um estilo que não quer mesmo, diga também. É igualmente útil.</p>
<p>Se forem precisos títulos, oráculos ou uma animação de logótipo, é do manual de marca que saem,
por isso vale a pena mandá-lo mesmo quando parece exagero para um vídeo só.</p>

<h3>A música é comigo</h3>
<p>Não precisa de encontrar uma faixa nem de comprar nenhuma.</p>
<p>Trabalho com bibliotecas premium pagas, por isso a procura é minha e a licença vai junto com a
entrega, válida para as plataformas onde o vídeo vai passar. Só preciso de uma direção, e vaga
chega. "Calma, sem voz, nada corporativo" já dá para trabalhar.</p>
<p>Duas exceções que vale a pena assinalar cedo:</p>
<ul>
  <li><strong>Se já tem uma faixa de que gosta muito</strong>, mande a licença em vez do ficheiro.
  Uma licença comprada para um filme muitas vezes não cobre as versões dele para redes sociais, e
  isso costuma aparecer na semana em que era para publicar.</li>
  <li><strong>Se for música comercial</strong>, daquelas com um nome que reconheceria, parta do
  princípio de que não é licenciável a um preço sensato e diga-me antes o que lhe agrada nela.
  Normalmente consigo chegar perto.</li>
</ul>

<h3>Faltarem planos não é problema</h3>
<p>Há quem adie o envio do material porque falta um plano. Não precisa de segurar nada.</p>
<p>Licencio imagens de stock nas mesmas bibliotecas premium, por isso um plano de estabelecimento
que falta, um aéreo que ninguém tinha orçamento para filmar ou uma cena que nunca chegou a existir
costumam resolver-se. Boa parte do trabalho corporativo que faço é construído sobretudo a partir de
material licenciado e dos materiais que o cliente já tem, sem filmagem nenhuma.</p>
<p>Diga-me o que falta em vez de esperar que passe a existir.</p>

<h3>Quem aprova</h3>
<p>Uma pessoa com a palavra final, ou um grupo que manda as notas em conjunto. Cinco pessoas a
responder à parte, cada uma sobre uma versão diferente, é o que acrescenta dias a um projeto.</p>

<h3>Versão curta</h3>
<ul>
  <li><strong>Tudo</strong>, não uma seleção</li>
  <li><strong>Sem exportar</strong>,direto do cartão</li>
  <li><strong>Áudio separado</strong>, e todas as câmaras, sem cortes</li>
  <li><strong>Um logótipo vetorial</strong>, fontes, cores</li>
  <li><strong>Duração e plataforma</strong>, nem que seja por alto</li>
  <li><strong>Se passa sem som</strong>, e em que línguas</li>
  <li><strong>Duas referências</strong>, com uma frase cada</li>
  <li><strong>Um nome</strong> para as aprovações</li>
</ul>
<p>A música, o stock e o licenciamento de ambos são comigo. Mande o resto e o primeiro corte fica
perto o suficiente para se falar dele a sério.</p>
""",
        },
        "es": {
            "date_label": "Septiembre de 2026",
            "title": 'Qué mandarme para que el primer corte quede cerca',
            "excerpt": 'La mayor parte de lo que ralentiza un montaje se decide antes de abrir los archivos. Lo que de verdad ayuda, de qué hay que mandar originales, y por qué la música y el stock no son cosas que tengas que buscar.',
            "body": """
<p class="lede">La mayor parte de lo que ralentiza un montaje se decide antes de que abra los
archivos. Depende de lo que llegó.</p>
<p>Esto no va de que el material sea bueno. Va de que vengan con él las cosas correctas, y de
algunas que no hace falta que mandes.</p>

<h3>Para qué es, antes de qué hay dentro</h3>
<p>Dónde se publica y cuánto tiene que durar moldean el montaje más que el propio material.</p>
<p>Una película de noventa segundos para tu web y un corte de quince segundos para redes de pago son
piezas distintas. Empiezan de otra manera. En redes tienes alrededor de un segundo y medio antes de
que alguien siga bajando. En tu web la gente te da más tiempo. Si necesitas las dos, dilo al
principio. Montar una y adaptarla después lleva más tiempo y funciona peor.</p>
<p>Si todavía no sabes la duración, dilo. Cambia cómo lo monto y no es un problema.</p>
<p>Hay dos cosas que siempre se quedan fuera de los briefings y las dos son baratas al principio:</p>
<ul>
  <li><strong>Si tiene que funcionar sin sonido.</strong> Los stands de ferias y las pantallas de
  eventos van en bucle y sin audio, y buena parte de las redes también. Un vídeo hecho para el
  silencio lleva la información en pantalla en vez de en la voz en off, y eso cambia el montaje, no
  solo los rótulos. He hecho piezas que nunca iban a escucharse.</li>
  <li><strong>En qué idiomas lo necesitas.</strong> Subtítulos o versiones completas en español,
  inglés y portugués son sencillos mientras el proyecto está abierto e incómodos una vez cerrado y
  entregado.</li>
</ul>

<h3>Manda todo, no solo lo bueno</h3>
<p>Esto es lo que más tiempo cuesta.</p>
<p>Es tentador revisar el bruto y mandar solo las tomas que te gustaron. Las partes que necesito son
muchas veces las que tú cortarías. El segundo antes de que alguien empiece a hablar. La pausa en la
que baja la mirada. Los doce segundos mientras la cámara se asienta.</p>
<p>Lo mismo con el b-roll que te parece aburrido. Un pasillo vacío no es interesante por sí solo y
probablemente salve una transición.</p>
<p>Manda la tarjeta entera. El volumen no me molesta.</p>

<h3>Originales, no exportaciones</h3>
<p>Manda los archivos tal y como salieron de la cámara. No una copia comprimida, nada que haya
pasado por WhatsApp, y a ser posible no una reexportación de otro montaje.</p>
<p>Cada exportación tira datos. No lo vas a notar viendo el archivo. Lo vas a notar en cuanto el
plano se etalone, se ralentice o se amplíe para un recorte vertical.</p>
<p>Si lo único que existe es una copia comprimida, se puede trabajar. Basta con decírmelo pronto.</p>

<h3>El audio es probablemente un archivo aparte</h3>
<p>Si alguien llevaba micrófono de corbata, o hubo pértiga, esas grabaciones suelen vivir en
archivos separados. Mándalos. El audio de cámara es un respaldo. El diálogo es lo que menos perdona
quien mira.</p>
<p>Si no sabes si existe audio separado, pregúntale a quien lo grabó.</p>
<p>Si había más de una cámara, mándalas todas sin recortar, incluidas las partes en las que no pasa
nada. El audio solapado de las cámaras es por donde las sincronizo, y los clips ya recortados son lo
que convierte eso en un trabajo manual en vez de automático.</p>

<h3>Cosas de marca</h3>
<p>Cada una de estas lleva cinco minutos mandar y mucho más tiempo reconstruir:</p>
<ul>
  <li><strong>Un logotipo vectorial.</strong> SVG, AI o EPS. No un PNG sacado de la web.</li>
  <li><strong>Tus tipografías</strong>, si la licencia permite compartirlas, y tus códigos de color
  o el manual de marca.</li>
  <li><strong>Dos o tres referencias</strong>, con una frase sobre qué te gusta de ellas. Un enlace
  solo me dice que te gustó.</li>
</ul>
<p>Si hay un estilo que no quieres, dilo también. Es igual de útil.</p>
<p>Si van a hacer falta rótulos, chyrons o una animación de logotipo, salen del manual de marca, así
que vale la pena mandarlo aunque parezca excesivo para un solo vídeo.</p>

<h3>La música es cosa mía</h3>
<p>No necesitas encontrar una pista ni comprar ninguna.</p>
<p>Trabajo con bibliotecas premium de pago, así que la búsqueda es mía y la licencia va con la
entrega, válida para las plataformas donde vaya a correr el vídeo. Solo necesito una dirección, y
vaga vale. "Tranquila, sin voces, nada corporativo" ya me sirve.</p>
<p>Dos excepciones que conviene avisar pronto:</p>
<ul>
  <li><strong>Si ya tienes una pista a la que le tienes cariño</strong>, manda la licencia en vez
  del archivo. Una licencia comprada para una película muchas veces no cubre sus versiones para
  redes, y eso suele aparecer la semana en la que tocaba publicar.</li>
  <li><strong>Si es música comercial</strong>, de esas con un nombre que reconocerías, da por hecho
  que no se licencia a un precio sensato y cuéntame mejor qué te gusta de ella. Normalmente consigo
  acercarme.</li>
</ul>

<h3>Que falten planos no es un problema</h3>
<p>Hay quien retrasa el envío del material porque falta un plano. No hace falta que frene nada.</p>
<p>Licencio imágenes de stock en las mismas bibliotecas premium, así que un plano de situación que
falta, un aéreo que nadie tenía presupuesto para volar o una escena que nunca se rodó se suelen
resolver. Buena parte del trabajo corporativo que hago está construido sobre todo con material
licenciado y con los materiales que el cliente ya tiene, sin rodaje ninguno.</p>
<p>Dime qué falta en vez de esperar a que exista.</p>

<h3>Quién lo aprueba</h3>
<p>Una persona con la última palabra, o un grupo que manda sus notas juntas. Cinco personas
respondiendo por separado, cada una sobre una versión distinta, es lo que añade días a un
proyecto.</p>

<h3>La versión corta</h3>
<ul>
  <li><strong>Todo</strong>, no una selección</li>
  <li><strong>Sin exportar</strong>, directo de la tarjeta</li>
  <li><strong>Audio separado</strong>, y todas las cámaras, sin recortar</li>
  <li><strong>Un logotipo vectorial</strong>, tipografías, colores</li>
  <li><strong>Duración y plataforma</strong>, aunque sea por encima</li>
  <li><strong>Si va sin sonido</strong>, y en qué idiomas</li>
  <li><strong>Dos referencias</strong>, con una frase cada una</li>
  <li><strong>Un nombre</strong> para las aprobaciones</li>
</ul>
<p>La música, el stock y el licenciamiento de los dos son cosa mía. Manda el resto y el primer corte
quedará lo bastante cerca como para hablar de él en serio.</p>
""",
        },
        "body": """
<p class="lede">Most of what slows an edit down is decided before I open the files. It comes down to
what arrived.</p>

<p>None of this is about the footage being good. It's about the right things coming with it, and
about a few things you don't need to send at all.</p>


<h3>What it's for, before what's in it</h3>

<p>Where it runs and how long it has to be shape the edit more than the material does.</p>

<p>A ninety-second film for your homepage and a fifteen-second cut for paid social are different
pieces. They open differently. On social you have about a second and a half before someone
scrolls. On your own site people will give you longer. If you need both, say so at the start.
Cutting one and adapting it afterwards takes longer and works less well.</p>

<p>If you don't know the length yet, say that. It changes how I assemble and it isn't a problem.</p>

<p>Two things get left out of briefs and both are cheap at the start:</p>

<ul>
  <li><strong>Whether it has to work with no sound.</strong> Trade show booths and event screens
  usually play silent on a loop, and so does most of a social feed. A video built for silence
  carries the information on screen instead of in the voiceover, and that changes the cut, not
  just the titles. I've made pieces that were never going to be heard at all.</li>

  <li><strong>Which languages you need.</strong> Subtitles and full language versions in English,
  Portuguese and Spanish are straightforward while the project is open and awkward once it's
  closed and delivered.</li>

</ul>

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

<p>If more than one camera was running, send all of them untrimmed, including the parts where
nothing is happening. Overlapping camera audio is what I sync them by, and trimmed clips are what
make that a manual job instead of an automatic one.</p>


<h3>Brand things</h3>

<p>Each of these takes five minutes to send and much longer to reconstruct:</p>

<ul>
  <li><strong>A vector logo.</strong> SVG, AI or EPS. Not a PNG pulled off the website.</li>

  <li><strong>Your fonts</strong>, if the license covers sharing them, and your color codes or the
  brand guide.</li>

  <li><strong>Two or three references</strong>, with a sentence about what you like in them. A link
  on its own only tells me you liked it.</li>

</ul>
<p>If there's a style you actively don't want, say that too. It's just as useful.</p>

<p>If titles, lower-thirds or a logo animation are going to be needed, the brand guide is what they
get built from, so it's worth sending even when it feels like overkill for one video.</p>


<h3>Music is my side of it</h3>

<p>You don't need to find a track, and you don't need to buy one.</p>

<p>I work from paid premium libraries, so the searching is mine and the license comes with the
delivery, cleared for the platforms the video is going to run on. All I need is a direction, and
vague is fine. "Calm, no vocals, nothing corporate" is enough to work from.</p>

<p>Two exceptions worth flagging early:</p>

<ul>
  <li><strong>If you already have a track you're attached to</strong>, send the license rather than
  the file. A license bought for one film often doesn't cover the social versions of it, and that
  tends to surface the week you're meant to publish.</li>

  <li><strong>If it's a commercial piece of music</strong>, something with a name you'd recognize,
  assume it isn't clearable at a sensible price and tell me what you like about it instead. I can
  usually get close.</li>

</ul>

<h3>Gaps in the footage are not a problem</h3>

<p>People delay sending material because a shot is missing. It doesn't need to hold anything up.</p>

<p>I license stock footage from the same premium libraries, so a missing establishing shot, an
aerial nobody had the budget to fly, or a scene that was never filmed can usually be covered.
Plenty of the corporate work I do is built mostly from licensed material and the client's own
existing assets, with no shoot at all.</p>

<p>Tell me what's missing rather than waiting until it exists.</p>


<h3>Who signs it off</h3>

<p>One person with final say, or a group who send their notes together. Five people replying
separately, each to a different version, is what adds days to a project.</p>


<h3>The short version</h3>

<ul>
  <li><strong>Everything</strong>, not a selection</li>

  <li><strong>Unexported</strong>, straight off the card</li>

  <li><strong>Separate audio</strong>, and every camera, untrimmed</li>

  <li><strong>A vector logo</strong>, fonts, colors</li>

  <li><strong>Length and platform</strong>, even roughly</li>

  <li><strong>Whether it plays silent</strong>, and in which languages</li>

  <li><strong>A couple of references</strong>, with a sentence each</li>

  <li><strong>One name</strong> for approvals</li>

</ul>
<p>Music, stock and the licensing behind both are mine to deal with. Send the rest and the first
cut will be close enough to talk about properly.</p>
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
                   "job. What cohesion actually means, where separate commissions drift, and the "
                   "formats that get forgotten at the briefing stage.",
        "pt": {
            "date_label": "Setembro de 2026",
            "title": "Uma campanha, várias plataformas: encomende tudo de uma vez",
            "excerpt": "Uma campanha que corre em várias plataformas funciona melhor encomendada como "
                       "um só trabalho. O que é a coerência, onde é que as encomendas separadas "
                       "se desviam, e os formatos que ficam esquecidos no briefing.",
        "body": """
<p class="lede">Uma campanha já não vive num sítio só. A mesma ideia tem de funcionar no seu site,
num feed do LinkedIn, como reel vertical e, às vezes, num ecrã sem som numa feira. São filmes
diferentes. O erro é encomendá-los como trabalhos diferentes.</p>

<p>Encomendados um de cada vez, deixam de parecer a mesma campanha. Primeiro o filme, os reels uns
meses depois, alguma coisa para o stand mais tarde. Três campanhas de três pessoas, que é
normalmente exatamente o que são.</p>

<h3>Como é a incoerência, na prática</h3>

<p>Raramente é dramática. É um desvio.</p>

<p>A cor está um pouco mais quente no segundo lote, porque foi feita seis meses depois noutro
monitor. Os oráculos usam um tipo de letra que não é bem o da marca, porque quem os fez não tinha o
ficheiro. A música é outra faixa, porque a primeira licença cobria um filme e não uma campanha, por
isso os reels parecem de outra empresa.</p>

<p>Ninguém que veja lhe sabe dizer o que está mal. Só não liga as peças umas às outras, o que
significa que cada peça tem de o apresentar do zero. É a repetição que faz uma campanha pegar, e só
há repetição se as pessoas reconhecerem a segunda coisa como pertencendo à primeira.</p>

<h3>Coerente, mas não igual</h3>

<p>É aqui que está a tensão, e é o trabalho todo.</p>

<p>As peças têm de ser reconhecivelmente a mesma campanha: a mesma cor, a mesma tipografia, o mesmo
mundo de música, o mesmo ritmo de montagem. Alguém deve perceber que é sua antes de aparecer o
logótipo.</p>

<p>Mas não podem ser o mesmo filme em durações diferentes. Essa é a outra falha, e é igualmente
comum. Quando as versões curtas são cortadas a partir da longa, a peça de quinze segundos é a de
noventa sem o meio. Quem viu uma viu todas. Pagou quatro peças e publicou uma ideia.</p>

<p>O mesmo aspeto, conteúdos diferentes. Uma abre no CEO. Outra é o produto a ser usado, sem uma
palavra. Outra são trinta segundos de processo. Mesma família, funções diferentes.</p>

<h3>Onde é que as encomendas separadas se desviam</h3>

<p>A coerência é difícil de acrescentar no fim. Decide-se sobretudo em coisas que acontecem antes, e
cada uma delas é barata uma vez e cara duas:</p>

<ul>
  <li><strong>Uma cor, um conjunto de referências.</strong> Igualar uma cor que fez há seis meses a
  partir de outro projeto é adivinhar.</li>
  <li><strong>Uma licença de música</strong> que cubra todos os cortes em todas as plataformas.
  Licencio em bibliotecas premium pagas, por isso isto é comigo e não consigo, mas só resulta se eu
  souber a lista completa de peças no momento em que escolho a faixa. Licenciada a posteriori, um
  corte de cada vez, acaba com uma faixa diferente em cada um sem ninguém ter escolhido isso.</li>
  <li><strong>Um conjunto de elementos animados</strong> (títulos, oráculos, animação de logótipo),
  feito uma vez e reutilizado, em vez de refeito um pouco diferente a cada ronda.</li>
  <li><strong>Material filmado a saber que todos os formatos vinham a caminho.</strong> Uma
  composição 16:9 perde cerca de 60% do enquadramento num corte 9:16, e o que se perde são os
  lados, que é onde a composição costuma estar.</li>
</ul>

<p>É esta última que me chega às mãos. Às vezes consigo reenquadrar plano a plano, aproximando e
acompanhando para manter o sujeito em campo. Funciona quando há resolução a sobrar, custa um dia, e
continua a ler-se como um plano aberto a ser salvo.</p>

<h3>O que fica pronto no fim</h3>

<p>Encomendado como um só trabalho, o mesmo material dá:</p>

<ul>
  <li><strong>O filme de marca</strong>: 60 a 120 segundos, 16:9. O argumento completo.</li>
  <li><strong>O trailer</strong>: 30 a 45 segundos. Condensa o argumento em algo que se aguenta
  sozinho, em vez de um filme encurtado.</li>
  <li><strong>O teaser</strong>: 10 a 15 segundos. Um gancho, feito para fazer alguém olhar.</li>
  <li><strong>Os reels</strong>: três a seis peças verticais, 9:16 ou 4:5, legendadas, feitas para
  funcionar sem som.</li>
  <li><strong>O corte quadrado</strong>: 1:1, para os feeds que ainda o favorecem.</li>
</ul>

<p>Uma campanha de viagens recente saiu como um spot de 30 segundos em horizontal, uma versão
quadrada de 60 segundos e cinco reels verticais, tudo do mesmo material, e a questão toda era
parecerem-se uns com os outros.</p>

<p>Há mais duas que saem quase de graça assim que o material existe, e as duas ficam esquecidas na
fase do briefing:</p>

<ul>
  <li><strong>Um corte sem som para ecrãs.</strong> Os stands de feiras e os monitores de eventos
  passam em loop sem áudio, por isso a informação tem de passar para o ecrã. É uma montagem a sério
  e não carregar em mute, e já construí peças inteiras que só iam passar assim.</li>
  <li><strong>Versões noutras línguas.</strong> Legendas, ou um corte totalmente localizado, em
  português, inglês e espanhol. Feito ao lado do original é um acréscimo pequeno. Feito um ano
  depois obriga a reabrir um projeto de que ninguém se lembra.</li>
</ul>

<p>Fotografias e um bumper de 6 segundos para pré-roll costumam também estar ali à mão.</p>

<h3>O que é comigo e o que não é</h3>

<p>Assim que o material existe, tudo o que vem a seguir é do meu lado: a montagem, a cor, os
grafismos animados, o som, o licenciamento da música e do stock, as legendas, as versões. Se
faltar um plano, normalmente consigo licenciá-lo em vez de o mandar filmar outra vez, que é como
muito do trabalho corporativo se faz.</p>

<p>O que não consigo mudar depois é a forma como as coisas foram filmadas. Vale a pena acertar com
quem faz o material:</p>

<ul>
  <li>Todas as plataformas onde a campanha vai passar. Escreva a lista, porque as óbvias são as que
  ficam esquecidas.</li>
  <li>Que peças, com que durações, em que formatos.</li>
  <li>Se o material é enquadrado a saber que vêm cortes verticais.</li>
  <li>Se alguma coisa tem de se aguentar sem som nenhum.</li>
  <li>Em que línguas tem de existir.</li>
</ul>

<h3>Versão curta</h3>

<p>Se o vídeo só vai viver no seu site, compre um filme. Se vai correr em várias plataformas, e
quase sempre vai, encomende a campanha toda de uma vez. Não para poupar dinheiro, embora costume
poupar, mas porque as coisas que seguram uma campanha escolhem-se no início e não se acrescentam no
fim.</p>

<p>Se está a planear alguma coisa, <a href="../../contact/">diga-me o que tem em mente</a> e eu digo
o que deve pedir, e o que precisaria de ter para construir a campanha toda a partir disso. Essa
parte é <a href="../../services/">comigo</a>.</p>
""",
        },
        "es": {
            "date_label": "Septiembre de 2026",
            "title": 'Una campaña, todas las plataformas: encárgalo todo de una vez',
            "excerpt": 'Una campaña que corre en varias plataformas funciona mejor encargada como un solo trabajo. Qué es la coherencia, dónde se desvían los encargos separados, y los formatos que se olvidan en el briefing.',
            "body": """
<p class="lede">Una campaña ya no vive en un solo sitio. La misma idea tiene que funcionar en tu
web, en un feed de LinkedIn, como reel vertical y, a veces, en una pantalla sin sonido de una
feria. Son películas distintas. El error es encargarlas como trabajos distintos.</p>

<p>Pedidas de una en una, dejan de parecer una sola campaña. Primero la película, los reels unos
meses después, algo para el stand más tarde. Tres campañas de tres personas, que suele ser
exactamente lo que son.</p>

<h3>Cómo es la incoherencia en la práctica</h3>

<p>Rara vez es dramática. Es una deriva.</p>

<p>El etalonaje está algo más cálido en el segundo lote, porque se hizo seis meses después en otro
monitor. Los chyrons usan una tipografía que no es del todo la de la marca, porque quien los hizo
no tenía el archivo. La música es otra pista, porque la primera licencia cubría una película y no
una campaña, así que los reels parecen de otra empresa.</p>

<p>Nadie que lo vea sabría decirte qué está mal. Simplemente no conecta las piezas entre sí, lo que
significa que cada pieza tiene que presentarte desde cero. Es la repetición lo que hace que una
campaña cale, y solo hay repetición si la gente reconoce la segunda cosa como parte de la
primera.</p>

<h3>Coherente, pero no idéntico</h3>

<p>Aquí está la tensión, y es todo el trabajo.</p>

<p>Las piezas tienen que ser reconociblemente la misma campaña: el mismo etalonaje, la misma
tipografía, el mismo mundo musical, el mismo ritmo de montaje. Alguien debería saber que eres tú
antes de que aparezca el logotipo.</p>

<p>Pero no pueden ser la misma película en duraciones distintas. Ese es el otro fallo, y es igual de
común. Cuando las versiones cortas se recortan de la larga, la pieza de quince segundos es la de
noventa sin la parte de en medio. Quien ha visto una las ha visto todas. Pagaste cuatro piezas y
publicaste una idea.</p>

<p>El mismo aspecto, contenidos distintos. Una abre con el CEO. Otra es el producto en uso, sin una
palabra. Otra son treinta segundos de proceso. Misma familia, funciones distintas.</p>

<h3>Dónde se desvían los encargos separados</h3>

<p>La coherencia es difícil de añadir al final. Se decide sobre todo en cosas que pasan antes, y
cada una de ellas es barata una vez y cara dos:</p>

<ul>
  <li><strong>Un etalonaje, un conjunto de referencias.</strong> Igualar un etalonaje que hiciste
  hace seis meses desde otro proyecto es adivinar.</li>
  <li><strong>Una licencia de música</strong> que cubra todos los cortes en todas las plataformas.
  Licencio en bibliotecas premium de pago, así que esto es cosa mía y no tuya, pero solo funciona si
  sé la lista completa de piezas en el momento en que elijo la pista. Licenciada a posteriori, un
  corte cada vez, acabas con una pista distinta en cada uno sin que nadie lo haya elegido.</li>
  <li><strong>Un conjunto de elementos animados</strong> (rótulos, chyrons, animación de logotipo),
  hecho una vez y reutilizado, en vez de rehecho un poco distinto en cada ronda.</li>
  <li><strong>Material rodado sabiendo que venían todos los formatos.</strong> Una composición 16:9
  pierde cerca del 60% del encuadre en un recorte 9:16, y lo que se va son los lados, que es donde
  suele estar la composición.</li>
</ul>

<p>Esta última es la que me llega a mí. A veces puedo reencuadrar plano a plano, acercando y
siguiendo al sujeto para mantenerlo en campo. Funciona cuando sobra resolución, cuesta un día, y
sigue leyéndose como un plano abierto rescatado.</p>

<h3>Con qué te quedas al final</h3>

<p>Encargado como un solo trabajo, el mismo material da:</p>

<ul>
  <li><strong>La película de marca</strong>: 60 a 120 segundos, 16:9. El argumento completo.</li>
  <li><strong>El tráiler</strong>: 30 a 45 segundos. Condensa el argumento en algo que se sostiene
  solo, en vez de una película acortada.</li>
  <li><strong>El teaser</strong>: 10 a 15 segundos. Un gancho, hecho para que alguien mire.</li>
  <li><strong>Los reels</strong>: de tres a seis piezas verticales, 9:16 o 4:5, subtituladas, hechas
  para funcionar sin sonido.</li>
  <li><strong>El corte cuadrado</strong>: 1:1, para los feeds que todavía lo favorecen.</li>
</ul>

<p>Una campaña de viajes reciente salió como un spot de 30 segundos en horizontal, una versión
cuadrada de 60 segundos y cinco reels verticales, todo del mismo material, y la gracia era
precisamente que se parecieran entre sí.</p>

<p>Hay dos más que salen casi gratis en cuanto el material existe, y las dos se olvidan en la fase
de briefing:</p>

<ul>
  <li><strong>Un corte sin sonido para pantallas.</strong> Los stands de ferias y los monitores de
  eventos van en bucle sin audio, así que la información tiene que pasar a la pantalla. Es un
  montaje de verdad y no darle a silenciar, y he construido piezas enteras que solo iban a verse
  así.</li>
  <li><strong>Versiones en otros idiomas.</strong> Subtítulos, o un corte totalmente localizado, en
  español, inglés y portugués. Hecho junto al original es un añadido pequeño. Hecho un año después
  obliga a reabrir un proyecto que ya nadie recuerda.</li>
</ul>

<p>Fotografías y un bumper de 6 segundos para pre-roll suelen estar también ahí al alcance.</p>

<h3>Qué es cosa mía y qué no</h3>

<p>En cuanto el material existe, todo lo que viene después es de mi lado: el montaje, el etalonaje,
los gráficos animados, el sonido, el licenciamiento de la música y del stock, los subtítulos, las
versiones. Si falta un plano, normalmente puedo licenciarlo en vez de mandarte a rodar otra vez,
que es como se hace buena parte del trabajo corporativo.</p>

<p>Lo que no puedo cambiar después es cómo se rodó algo. Vale la pena acordarlo con quien hace el
material:</p>

<ul>
  <li>Todas las plataformas en las que va a correr la campaña. Escribe la lista, porque las obvias
  son las que se olvidan.</li>
  <li>Qué piezas, con qué duraciones, en qué formatos.</li>
  <li>Si el material se encuadra sabiendo que vienen recortes verticales.</li>
  <li>Si algo tiene que sostenerse sin sonido ninguno.</li>
  <li>En qué idiomas tiene que existir.</li>
</ul>

<h3>La versión corta</h3>

<p>Si el vídeo solo va a vivir en tu web, compra una película. Si va a correr en varias plataformas,
y casi siempre va a hacerlo, encarga la campaña entera de una vez. No para ahorrar dinero, aunque
suele ahorrarlo, sino porque las cosas que sostienen una campaña se eligen al principio y no se
añaden al final.</p>

<p>Si estás planeando algo, <a href="../../contact/">cuéntame qué tienes en mente</a> y te digo qué
pedir, y qué necesitaría para construir la campaña entera a partir de ello. Esa parte es <a href="../../services/">cosa mía</a>.</p>
""",
        },
        "body": """
<p class="lede">A campaign doesn't live in one place any more. The same idea has to work on your
homepage, in a LinkedIn feed, as a vertical reel, and sometimes on a silent screen at a trade
show. Those are different films. The mistake is commissioning them as different jobs.</p>


<p>Ordered one at a time, they stop looking like one campaign. The film first, the reels a few
months later, something for the booth after that. Three campaigns by three people, which is
usually exactly what they are.</p>


<h3>What incoherence actually looks like</h3>


<p>It's rarely dramatic. It's drift.</p>


<p>The grade is slightly warmer in the second batch, because it was done six months later on a
different monitor. The lower-thirds use a typeface that isn't quite the brand one, because
whoever made them didn't have the file. The music is a different track, because the first license
covered one film and not a campaign, so the reels feel like they belong to another company.</p>


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


<p>Same look, different content. One opens on the CEO. One is the product being used, no words at
all. One is thirty seconds of process. Same family, different jobs.</p>


<h3>Where separate commissions drift</h3>


<p>Cohesion is hard to add at the end. It is mostly decided by things that happen before, and
each of them is cheap once and expensive twice:</p>


<ul>
  <li><strong>One grade, one set of references.</strong> Matching a grade you did six months ago
  from a different project file is guesswork.</li>

  <li><strong>One music license</strong> covering every cut on every platform. I license from paid
  premium libraries, so this is mine to handle rather than yours, but it only works if I know the
  full list of pieces at the point I choose the track. Licensed after the fact, one cut at a time,
  you end up with a different track on each one for no reason anybody chose.</li>

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

  <li><strong>The square cut</strong>: 1:1, for feeds that still favor it.</li>

</ul>

<p>A recent travel campaign came out as a 30-second landscape spot, a 60-second square version and
five vertical reels, all from one set of material, and the whole point was that they looked like
each other.</p>

<p>Two more come nearly free once the material is there, and both get forgotten at the briefing
stage:</p>

<ul>
  <li><strong>A silent cut for screens.</strong> Trade show booths and event monitors play on a
  loop with no sound, so the information has to move onto the screen. It's a real edit rather than
  a mute button, and I've built whole pieces that were only ever going to run that way.</li>

  <li><strong>Language versions.</strong> Subtitles, or a fully localized cut, in English,
  Portuguese and Spanish. Done alongside the original it's a small addition. Done a year later it
  means reopening a project nobody remembers.</li>

</ul>

<p>Stills and a 6-second pre-roll bumper are usually there for the taking too.</p>


<h3>What's mine and what isn't</h3>


<p>Once the material exists, everything after it is my side: the cut, the grade, the motion
graphics, the sound, the music and stock licensing, the subtitles, the versions. If a shot is
missing I can usually license it rather than send you back out to film it, which is how a lot of
corporate work gets made in the first place.</p>

<p>What I can't do afterwards is change how something was shot. Worth settling with whoever is
making the material:</p>


<ul>
  <li>Every platform this campaign will run on. Write the list, because the obvious ones get
  forgotten.</li>

  <li>Which pieces, at what lengths, in which aspect ratios.</li>

  <li>Whether the material is framed knowing vertical crops are coming.</li>

  <li>Whether anything needs to hold up with no sound at all.</li>

  <li>Which languages it has to exist in.</li>

</ul>

<h3>The short version</h3>


<p>If the video only ever lives on your website, buy one film. If it's going to run across
platforms, and it almost always is, commission the whole campaign at once. Not to save money,
though it usually does, but because the things that hold a campaign together are chosen at the
start and can't be added at the end.</p>


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
<link rel="stylesheet" href="{root}assets/site.css?v=sig4">

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
    pre = "" if lang == "en" else lang + "/"
    # One entry per language the blog is published in. `other` is this page in
    # another language when it exists; anything else falls back to that
    # language's index rather than a URL that is not there.
    def href(code):
        if code == lang:
            return None
        if other and ("/%s/blog/" % code in other or (code == "en" and "/blog/" in other
                                                      and "/pt/" not in other and "/es/" not in other)):
            return other
        return root + ("blog/" if code == "en" else "%s/blog/" % code)
    bits = []
    for code in ("en",) + LANGS:
        label = code.upper()
        h = href(code)
        bits.append('<span class="lang-current" aria-current="true">%s</span>' % label if h is None
                    else '<a href="%s">%s</a>' % (h, label))
    switch = "".join(bits)
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
    pre = "" if lang == "en" else lang + "/"
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


LANGS = ("pt", "es")            # translations, in the order they are offered


def langs_of(post):
    return ["en"] + [l for l in LANGS if l in post]


def hreflang(paths):
    """paths: {lang: url}. Emitted only where a post exists in more than one
    language - claiming a translation that is not there is worse than none."""
    if len(paths) < 2:
        return ""
    codes = {"en": "en", "pt": "pt-PT", "es": "es-ES"}
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
    for lang in ("en",) + LANGS:
        base = "blog" if lang == "en" else os.path.join(lang, "blog")
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
                other = urls["en"] if lang != "en" else next(
                    (urls[l] for l in LANGS if l in urls), None)
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
                lang={"en": "en", "pt": "pt-PT", "es": "es-ES"}[lang],
                alts=hreflang(urls),
                title=html.escape(c["title"], quote=True),
                excerpt=html.escape(c["excerpt"], quote=True),
                canonical=urls[lang], root=root, og_image=og_image,
                header=header(root, lang, other), main=main, footer=footer(root, lang)))

        # index
        root = "../" if lang == "en" else "../../"
        pre = "" if lang == "en" else lang + "/"
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
        for l in LANGS:
            if any(l in p for p in POSTS):
                index_urls[l] = f"{SITE}/{l}/blog/"
        # the switcher points at English from a translation, and at the first
        # translation that exists from English
        other = None
        if len(index_urls) > 1:
            other = index_urls["en"] if lang != "en" else next(
                (index_urls[l] for l in LANGS if l in index_urls), None)
        open(os.path.join(base, "index.html"), "w", encoding="utf-8").write(BANNER + PAGE.format(
            lang={"en": "en", "pt": "pt-PT", "es": "es-ES"}[lang],
            alts=hreflang(index_urls),
            title=nav["index_title"], excerpt=nav["index_lede"],
            canonical=index_urls[lang], root=root, og_image=index_og(posts),
            header=header(root, lang, other), main=main, footer=footer(root, lang)))
        print(f"  built {base}/index.html and {len(posts)} post page(s)")


if __name__ == "__main__":
    build()
