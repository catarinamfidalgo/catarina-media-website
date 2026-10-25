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
        "slug": "ai-video-needs-an-editor",
        "image": "ai-edit",
        "image_alt": "Scattered purple film frames of landscapes flowing into an editing timeline "
                     "with a playhead",
        "date": "2026-10-25",
        "date_label": "October 2026",
        "title": "AI can make the shots. It can't make the video.",
        "excerpt": "Almost every day someone gets in touch after trying to make their video with AI. "
                   "Where it stalls, where it helps, and why a good ad is more than footage that "
                   "looks real.",
        "pt": {
            "date_label": "Outubro de 2026",
            "title": "A IA faz os planos. Não faz o vídeo.",
            "excerpt": "Quase todos os dias alguém me contacta depois de tentar fazer o vídeo com "
                       "IA. Onde emperra, onde ajuda, e porque é que um bom anúncio é mais do que "
                       "imagens com ar real.",
        "body": """
<p class="lede">Quase todos os dias recebo uma mensagem de alguém que tentou primeiro fazer o vídeo
com IA. Uns passaram um fim de semana a escrever prompts e nunca chegaram a um vídeo acabado.
Outros chegaram, e não gostaram do resultado.</p>
<p>Não acho que tenham feito mal em tentar. As ferramentas impressionam, e eu também as uso. Mas as
mensagens descrevem quase sempre o mesmo problema, e não é o que as pessoas esperam.</p>

<h3>Mesmo quando parece real, não funciona</h3>
<p>A maior parte do que me mandam é lixo gerado por IA: caras que mudam de plano para plano, mãos
com dedos a mais, texto que se desfaz em rabiscos, tudo com o mesmo brilho de plástico. É esse o
ponto de partida habitual.</p>
<p>No melhor dos casos, as imagens parecem realistas plano a plano. A luz é boa, as caras aguentam,
o produto está lá. Mas veja-se do princípio ao fim e continua a não acontecer nada. Não há razão para continuar
a ver depois dos primeiros três segundos, a mensagem chega tarde ou não chega, e o fim limita-se a
parar.</p>
<p>Parecer realista nunca foi o que fez um vídeo bom. Um anúncio funciona pelo que fica de fora, pelo
que vem primeiro, pelo tempo que se segura um plano e pelo sítio onde a música muda. São decisões
de montagem. Um gerador dá-lhe um plano bonito. Não faz ideia se esse plano pertence ao seu vídeo,
nem onde.</p>

<h3>Porque é que horas de prompts não chegam lá</h3>
<p>Escrever prompts é uma forma lenta de montar. Cada tentativa sai um pouco diferente, por isso não
dá para ajustar uma coisa e manter o resto. Uma mão muda, um logótipo derrete, alguém que estava
de casaco azul aparece de verde. Corrige um plano e perde outro.</p>
<p>Numa timeline consigo mudar um corte em quatro frames, trocar uma take, mover a música meio
tempo. Esse controlo é o trabalho todo, e é para isso que serve um programa de edição como o
Premiere, o DaVinci Resolve ou o After Effects. Uma caixa de texto não o dá.</p>

<h3>Como eu uso a IA</h3>
<p>Uso-a onde poupa tempo sem decidir nada: limpar áudio, transcrever entrevistas, prolongar um
fundo, gerar um plano que nunca foi filmado quando o stock não o tem.</p>
<p>A diferença é que a uso dentro de uma montagem. Sei do que o vídeo precisa antes de gerar o que
quer que seja, por isso peço um plano concreto em vez de um filme inteiro, e quando sai mal corrijo
na timeline em vez de recomeçar. É saber montar que torna a ferramenta útil.</p>

<h3>Se já tentou</h3>
<p>Mande-me o que tem. Os planos gerados, os prompts que ficaram perto, a versão de que não gosta.
Muitas vezes há bom material ali dentro que só ainda não foi montado, e é mais rápido partir dele
do que começar de novo.</p>
<p>Se ainda não começou, diga-me para que é o vídeo e onde vai passar. Isso decide mais do que
qualquer ferramenta. <a href="../../contact/">Fale comigo</a> e eu digo-lhe o que vale a pena gerar
e o que não vale.</p>
""",
        },
        "es": {
            "date_label": "Octubre de 2026",
            "title": "La IA hace los planos. No hace el vídeo.",
            "excerpt": "Casi todos los días alguien me escribe después de intentar hacer su vídeo "
                       "con IA. Dónde se atasca, dónde ayuda, y por qué un buen anuncio es más que "
                       "imágenes que parecen reales.",
        "body": """
<p class="lede">Casi todos los días me llega un mensaje de alguien que intentó primero hacer su
vídeo con IA. Algunos pasaron un fin de semana escribiendo prompts y nunca llegaron a un vídeo
terminado. Otros llegaron, y no les gustó el resultado.</p>
<p>No creo que se equivocaran al intentarlo. Las herramientas impresionan, y yo también las uso.
Pero los mensajes describen casi siempre el mismo problema, y no es el que la gente espera.</p>

<h3>Aunque parezca real, no funciona</h3>
<p>Casi todo lo que me mandan es basura generada por IA: caras que cambian de un plano a otro,
manos con dedos de más, textos que se deshacen en garabatos, todo con el mismo brillo de plástico.
Ese es el punto de partida habitual.</p>
<p>En el mejor de los casos, las imágenes parecen realistas plano a plano. La luz es buena, las
caras aguantan, el producto está ahí. Pero míralo de principio a fin y sigue sin pasar nada. No hay motivo para seguir mirando
después de los tres primeros segundos, el mensaje llega tarde o no llega, y el final simplemente
se para.</p>
<p>Parecer realista nunca fue lo que hizo bueno a un vídeo. Un anuncio funciona por lo que se deja
fuera, por lo que va primero, por cuánto se sostiene un plano y por dónde cambia la música. Son
decisiones de montaje. Un generador te da un plano bonito. No tiene ni idea de si ese plano
pertenece a tu vídeo, ni de dónde.</p>

<h3>Por qué horas de prompts no llegan</h3>
<p>Escribir prompts es una forma lenta de montar. Cada intento sale un poco distinto, así que no
puedes ajustar una cosa y mantener el resto. Una mano cambia, un logotipo se derrite, alguien que
llevaba chaqueta azul aparece de verde. Arreglas un plano y pierdes otro.</p>
<p>En una línea de tiempo puedo mover un corte cuatro fotogramas, cambiar una toma, desplazar la
música medio tiempo. Ese control es todo el trabajo, y es para lo que sirve un programa de edición
como Premiere, DaVinci Resolve o After Effects. Una caja de texto no te lo da.</p>

<h3>Cómo uso yo la IA</h3>
<p>La uso donde ahorra tiempo sin decidir nada: limpiar audio, transcribir entrevistas, alargar un
fondo, generar un plano que nunca se rodó cuando el stock no lo tiene.</p>
<p>La diferencia es que la uso dentro de un montaje. Sé lo que necesita el vídeo antes de generar
nada, así que pido un plano concreto en lugar de una película entera, y cuando sale mal lo arreglo
en la línea de tiempo en vez de empezar de cero. Saber montar es lo que hace útil la
herramienta.</p>

<h3>Si ya lo has intentado</h3>
<p>Mándame lo que tengas. Los planos generados, los prompts que se acercaron, la versión que no te
gusta. Muchas veces hay buen material ahí dentro que simplemente no se ha montado aún, y es más
rápido partir de él que empezar de nuevo.</p>
<p>Si aún no has empezado, cuéntame para qué es el vídeo y dónde se va a ver. Eso decide más que
cualquier herramienta. <a href="../../contact/">Escríbeme</a> y te digo qué merece la pena generar
y qué no.</p>
""",
        },
        "body": """
<p class="lede">Almost every day I get a message from someone who tried to make their video with AI
first. Some spent a weekend writing prompts and never got to a finished video. Others got one, and
didn't like it.</p>

<p>I don't think they were wrong to try. The tools are impressive, and I use them myself. But the
messages nearly always describe the same problem, and it isn't the one people expect.</p>


<h3>Even when it looks real, it doesn't work</h3>

<p>Most of what people send me is AI slop: faces that drift between shots, hands with too many
fingers, text that melts into nonsense, everything with the same plastic sheen. That's the usual
starting point.</p>

<p>The best case is footage that looks realistic shot by shot. The light is good, the faces hold,
the product is there. Watch it from start to finish and still nothing happens. There's no reason to keep
watching after the first three seconds, the message arrives late or not at all, and the ending
just stops.</p>

<p>Looking realistic was never what made a video good. An ad works because of what's left out, what
comes first, how long a shot is held and where the music turns. Those are editing decisions. A
generator can give you a beautiful shot. It has no idea whether that shot belongs in your video,
or where.</p>


<h3>Why hours of prompts don't get there</h3>

<p>Prompting is a slow way to edit. Every attempt comes back slightly different, so you can't adjust
one thing and keep the rest. A hand changes, a logo melts, someone who was wearing a blue jacket is
now in green. You fix one shot and lose another.</p>

<p>In a timeline I can move a cut by four frames, swap one take, shift the music half a beat. That
control is the whole job, and it's what editing software like Premiere, DaVinci Resolve or After
Effects is for. A text box doesn't give you it.</p>


<h3>How I use AI</h3>

<p>I use it where it saves time without deciding anything: cleaning up audio, transcribing
interviews, extending a background, generating a shot that was never filmed when stock doesn't
have it.</p>

<p>The difference is that I'm using it inside an edit. I know what the video needs before I
generate anything, so I ask for one specific shot rather than a whole film, and when it comes back
wrong I fix it in the timeline instead of starting over. Knowing how to cut is what makes the tool
useful.</p>


<h3>If you've already tried</h3>

<p>Send me what you have. The generated clips, the prompts that got close, the version you're
unhappy with. There's often good material in there that just hasn't been cut yet, and it's quicker
to build from it than to start again.</p>

<p>If you haven't started, tell me what the video is for and where it will run. That decides more
than any tool will. <a href="../../contact/">Get in touch</a> and I'll tell you what's worth
generating and what isn't.</p>
""",
    },
    {
        "slug": "what-to-send-your-editor",
        "image": "what-to-send",
        "image_alt": "A purple set of drawers holding film strips, a waveform, music, "
                     "stills and color swatches",
        "date": "2026-09-28",
        "date_label": "September 2026",
        "title": "What to send me so the first cut is close",
        "excerpt": "Most of what slows an edit down is decided before the files are opened. What "
                   "to send, what to send originals of, and what you don't need to find at all.",
        "pt": {
            "date_label": "Setembro de 2026",
            "title": "O que me mandar para o primeiro corte ficar perto",
            "excerpt": "A maior parte do que atrasa uma montagem decide-se antes de os ficheiros "
                       "serem abertos. O que mandar, de que é preciso mandar originais, e o que "
                       "não precisa de procurar.",
        "body": """
<p class="lede">A maior parte do que atrasa uma montagem decide-se antes de eu abrir os ficheiros.
Depende do que chegou.</p>

<h3>Para que serve</h3>
<p>Onde vai passar e que duração tem de ter moldam a montagem mais do que o material. Um filme de
noventa segundos para o site e um corte de quinze para redes sociais começam de maneira diferente,
por isso, se precisa dos dois, diga-o logo. Se ainda não sabe a duração, diga isso também.</p>
<p>Há duas coisas que costumam ficar de fora: se tem de funcionar sem som, como a maior parte dos
feeds e dos ecrãs de feiras, e em que línguas precisa dele. São baratas de planear e incómodas de
acrescentar depois.</p>

<h3>Mande tudo</h3>
<p>É tentador mandar só as takes de que gostou. As partes de que preciso são muitas vezes as que
cortaria: o segundo antes de alguém falar, a pausa em que baixa os olhos, o b-roll aborrecido que
salva uma transição. Mande o cartão todo. O volume não me incomoda.</p>

<h3>Originais, não exportações</h3>
<p>Mande os ficheiros como saíram da câmara, não uma cópia comprimida nem algo que tenha passado
pelo WhatsApp. Cada exportação deita dados fora, e isso nota-se quando o plano é tratado na cor,
abrandado ou cortado na vertical. Se só existir uma cópia comprimida, dá para trabalhar. Basta
dizer-mo cedo.</p>

<h3>Áudio e câmaras</h3>
<p>Se alguém usou microfone de lapela ou houve boom, esse áudio costuma estar num ficheiro à parte.
Mande-o, porque o diálogo é o que o público perdoa menos. Se esteve mais do que uma câmara a gravar,
mande todas sem cortes. Sincronizo-as pelo som que se sobrepõe, e os clips aparados tornam isso um
trabalho manual.</p>

<h3>Coisas da marca</h3>
<ul>
  <li><strong>Um logótipo vetorial</strong>: SVG, AI ou EPS, não um PNG tirado do site.</li>
  <li><strong>Fontes e cores</strong>, ou o manual de marca, se existir.</li>
  <li><strong>Duas ou três referências</strong>, com uma frase sobre o que gosta em cada uma. Um
  estilo que não quer é igualmente útil.</li>
</ul>

<h3>A música e o stock são comigo</h3>
<p>Não precisa de encontrar nem de comprar uma faixa. Trabalho com bibliotecas premium pagas, por
isso a procura e a licença são do meu lado. Uma direção chega: "calma, sem voz, nada corporativo"
já serve. Se já comprou uma faixa de que gosta, mande a licença, porque pode não cobrir as versões
para redes sociais.</p>
<p>Faltarem planos também não tem de atrasar nada. Licencio stock nas mesmas bibliotecas, por isso
diga-me o que falta em vez de esperar que passe a existir.</p>

<h3>Uma pessoa aprova</h3>
<p>Um nome com a palavra final, ou um grupo que manda as notas em conjunto. Cinco pessoas a
responder em separado, cada uma a uma versão diferente, é o que acrescenta dias.</p>
<p>Mande o resto e o primeiro corte vai ficar perto o suficiente para falarmos a sério.</p>
""",
        },
        "es": {
            "date_label": "Septiembre de 2026",
            "title": "Qué enviarme para que el primer corte se acerque",
            "excerpt": "Casi todo lo que retrasa un montaje se decide antes de abrir los archivos. "
                       "Qué enviar, de qué hacen falta originales, y qué no necesitas buscar.",
        "body": """
<p class="lede">Casi todo lo que retrasa un montaje se decide antes de que abra los archivos.
Depende de lo que haya llegado.</p>

<h3>Para qué es</h3>
<p>Dónde se va a ver y cuánto tiene que durar dan forma al montaje más que el material. Una pieza de
noventa segundos para tu web y un corte de quince para redes empiezan de forma distinta, así que, si
necesitas las dos, dilo desde el principio. Si aún no sabes la duración, dilo también.</p>
<p>Hay dos cosas que suelen quedar fuera: si tiene que funcionar sin sonido, como casi todos los
feeds y las pantallas de ferias, y en qué idiomas lo necesitas. Son baratas de planificar e
incómodas de añadir después.</p>

<h3>Mándalo todo</h3>
<p>Es tentador mandar solo las tomas que te gustaron. Las partes que necesito suelen ser las que
cortarías: el segundo antes de que alguien hable, la pausa en la que baja la mirada, el b-roll
aburrido que salva una transición. Manda la tarjeta entera. El volumen no me molesta.</p>

<h3>Originales, no exportaciones</h3>
<p>Manda los archivos tal como salieron de la cámara, no una copia comprimida ni algo que haya
pasado por WhatsApp. Cada exportación tira datos, y se nota cuando el plano se etalona, se ralentiza
o se recorta en vertical. Si solo existe una copia comprimida, se puede trabajar. Solo dímelo
pronto.</p>

<h3>Audio y cámaras</h3>
<p>Si alguien llevó micrófono de solapa o hubo pértiga, ese audio suele estar en un archivo aparte.
Mándalo, porque el diálogo es lo que menos perdona el público. Si grababa más de una cámara, mándalas
todas sin recortar. Las sincronizo por el sonido que se solapa, y los clips recortados lo convierten
en un trabajo manual.</p>

<h3>Cosas de marca</h3>
<ul>
  <li><strong>Un logotipo vectorial</strong>: SVG, AI o EPS, no un PNG sacado de la web.</li>
  <li><strong>Tipografías y colores</strong>, o el manual de marca si existe.</li>
  <li><strong>Dos o tres referencias</strong>, con una frase sobre qué te gusta de cada una. Un
  estilo que no quieres es igual de útil.</li>
</ul>

<h3>La música y el stock son cosa mía</h3>
<p>No necesitas buscar ni comprar una pista. Trabajo con bibliotecas premium de pago, así que la
búsqueda y la licencia corren de mi parte. Basta con una dirección: "tranquila, sin voz, nada
corporativo" ya sirve. Si ya compraste una pista que te gusta, manda la licencia, porque puede no
cubrir las versiones para redes.</p>
<p>Que falten planos tampoco tiene por qué retrasar nada. Licencio stock en las mismas bibliotecas,
así que dime qué falta en lugar de esperar a que exista.</p>

<h3>Una persona aprueba</h3>
<p>Un nombre con la última palabra, o un grupo que manda las notas juntas. Cinco personas
respondiendo por separado, cada una a una versión distinta, es lo que añade días.</p>
<p>Manda el resto y el primer corte estará lo bastante cerca como para hablar de él en serio.</p>
""",
        },
        "body": """
<p class="lede">Most of what slows an edit down is decided before I open the files. It comes down to
what arrived.</p>


<h3>What it's for</h3>

<p>Where it runs and how long it has to be shape the edit more than the footage does. A
ninety-second homepage film and a fifteen-second social cut open differently, so if you need both,
say so at the start. If you don't know the length yet, say that too.</p>

<p>Two things usually get left out of briefs: whether it has to work with no sound, as most feeds and
trade show screens do, and which languages you need. Both are cheap to plan and awkward to add
later.</p>


<h3>Send everything</h3>

<p>It's tempting to send only the takes you liked. The parts I need are often the ones you'd cut:
the second before someone speaks, the pause where they look down, the boring b-roll that saves a
transition. Send the whole card. I don't mind the volume.</p>


<h3>Originals, not exports</h3>

<p>Send the files as they came off the camera, not a compressed copy or something that's been
through WhatsApp. Every export throws away data, and it shows once a shot is graded, slowed down or
cropped vertical. If a compressed copy is all there is, that's workable. Just tell me early.</p>


<h3>Audio and cameras</h3>

<p>If anyone wore a lav mic or there was a boom, that audio is usually a separate file. Send it,
because dialogue is what viewers forgive least. If more than one camera was running, send all of
them untrimmed. I sync them by their overlapping sound, and trimmed clips turn that into a manual
job.</p>


<h3>Brand things</h3>

<ul>
  <li><strong>A vector logo</strong>: SVG, AI or EPS, not a PNG pulled off the website.</li>

  <li><strong>Fonts and colors</strong>, or the brand guide if there is one.</li>

  <li><strong>Two or three references</strong>, with a sentence on what you like in each. A style
  you don't want is just as useful.</li>

</ul>

<h3>Music and stock are mine</h3>

<p>You don't need to find or buy a track. I work from paid premium libraries, so the searching and
the license are on my side. A direction is enough: "calm, no vocals, nothing corporate" works. If
you've already bought a track you love, send the license, because it may not cover the social
versions.</p>

<p>Missing shots don't need to hold anything up either. I license stock from the same libraries, so
tell me what's missing rather than waiting until it exists.</p>


<h3>One person signs off</h3>

<p>One name with final say, or a group that sends its notes together. Five people replying
separately, each to a different version, is what adds days.</p>

<p>Send the rest and the first cut will be close enough to talk about properly.</p>
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
        "excerpt": "A campaign that runs on several platforms works better commissioned as one job. "
                   "Why separate commissions drift, and the formats that get forgotten in the "
                   "brief.",
        "pt": {
            "date_label": "Setembro de 2026",
            "title": "Uma campanha, várias plataformas: encomende tudo de uma vez",
            "excerpt": "Uma campanha que corre em várias plataformas funciona melhor encomendada "
                       "como um só trabalho. Porque é que as encomendas separadas se desviam, e os "
                       "formatos que ficam esquecidos no briefing.",
        "body": """
<p class="lede">A mesma campanha tem agora de funcionar no seu site, num feed do LinkedIn, como reel
vertical e, às vezes, num ecrã sem som numa feira. São filmes diferentes. O erro é encomendá-los
como trabalhos diferentes.</p>

<h3>Como as encomendas separadas se desviam</h3>
<p>Encomendadas uma de cada vez, as peças deixam de parecer a mesma campanha. A cor está um pouco
mais quente no segundo lote, porque foi feita meses depois noutro monitor. Os títulos usam um tipo
de letra que não é bem o da marca. Os reels têm outra música, porque a primeira licença cobria um
filme só.</p>
<p>Ninguém sabe dizer o que está mal. Só não se ligam as peças umas às outras, e cada uma tem de o
apresentar do zero. Uma campanha pega pela repetição, e isso só funciona se as pessoas reconhecerem
a segunda peça como parte da primeira.</p>

<h3>O mesmo aspeto, filmes diferentes</h3>
<p>O outro erro comum é cortar as versões curtas a partir da longa. A peça de quinze segundos passa
a ser a de noventa sem o meio, e quem viu uma viu todas.</p>
<p>As peças devem partilhar a cor, a tipografia, a música e o ritmo, para que se perceba que é sua
antes de aparecer o logótipo. O que mostram deve mudar. Uma abre com a fundadora, outra é o produto
a ser usado, sem palavras, outra são trinta segundos de processo.</p>

<h3>O que tem de ficar decidido no início</h3>
<ul>
  <li><strong>Uma cor</strong> e um conjunto de referências.</li>
  <li><strong>Uma licença de música</strong> que cubra todos os cortes. Trato eu disso, mas preciso
  da lista completa de peças quando escolho a faixa.</li>
  <li><strong>Um conjunto de títulos</strong> e animação de logótipo, feitos uma vez e
  reaproveitados.</li>
  <li><strong>Material filmado a saber que vem aí a vertical.</strong> Um corte 9:16 perde cerca de
  60% de um enquadramento 16:9, sobretudo dos lados. Consigo reenquadrar plano a plano, mas custa um
  dia e continua a parecer salvo à última hora.</li>
</ul>

<h3>O que sai de um só trabalho</h3>
<ul>
  <li><strong>O filme de marca</strong>, de 60 a 120 segundos</li>
  <li><strong>Um trailer</strong>, de 30 a 45 segundos, que se aguenta sozinho</li>
  <li><strong>Um teaser</strong>, de 10 a 15 segundos</li>
  <li><strong>Três a seis reels</strong>, verticais e legendados para ver sem som</li>
  <li><strong>Um corte quadrado</strong> para os feeds que ainda o preferem</li>
</ul>
<p>Há mais dois que saem quase de graça e costumam ser esquecidos: um corte sem som para ecrãs de
eventos, e versões em português, inglês e espanhol. Feitos junto com o original são pouca coisa.
Feitos um ano depois obrigam a reabrir um projeto de que já ninguém se lembra.</p>

<h3>A versão curta</h3>
<p>Se o vídeo só vai viver no seu site, encomende um filme. Se vai correr em várias plataformas,
encomende a campanha inteira de uma vez. O que a mantém coesa escolhe-se no início e não se
acrescenta no fim.</p>
<p>Se está a planear alguma coisa, <a href="../../contact/">diga-me o que tem em mente</a> e eu
digo-lhe o que pedir. O resto é <a href="../../services/">comigo</a>.</p>
""",
        },
        "es": {
            "date_label": "Septiembre de 2026",
            "title": "Una campaña, todas las plataformas: encárgalo todo de una vez",
            "excerpt": "Una campaña que corre en varias plataformas funciona mejor encargada como "
                       "un solo trabajo. Por qué se desvían los encargos separados, y los formatos "
                       "que se olvidan en el briefing.",
        "body": """
<p class="lede">La misma campaña tiene que funcionar ahora en tu web, en un feed de LinkedIn, como
reel vertical y, a veces, en una pantalla sin sonido de una feria. Son películas distintas. El error
es encargarlas como trabajos distintos.</p>

<h3>Cómo se desvían los encargos separados</h3>
<p>Pedidas de una en una, las piezas dejan de parecer una sola campaña. El etalonaje está algo más
cálido en el segundo lote, porque se hizo meses después en otro monitor. Los títulos usan una
tipografía que no es del todo la de la marca. Los reels llevan otra música, porque la primera
licencia cubría una sola película.</p>
<p>Nadie sabe decir qué falla. Simplemente no se conectan las piezas entre sí, y cada una tiene que
presentarte desde cero. Una campaña cala por repetición, y eso solo funciona si la gente reconoce
la segunda pieza como parte de la primera.</p>

<h3>El mismo aspecto, películas distintas</h3>
<p>El otro error habitual es recortar las versiones cortas a partir de la larga. La pieza de quince
segundos acaba siendo la de noventa sin la parte de en medio, y quien ha visto una las ha visto
todas.</p>
<p>Las piezas deben compartir etalonaje, tipografía, música y ritmo, para que se sepa que eres tú
antes de que aparezca el logotipo. Lo que muestran debe cambiar. Una abre con la fundadora, otra es
el producto en uso, sin palabras, otra son treinta segundos de proceso.</p>

<h3>Lo que hay que decidir al principio</h3>
<ul>
  <li><strong>Un etalonaje</strong> y un conjunto de referencias.</li>
  <li><strong>Una licencia de música</strong> que cubra todos los cortes. Me encargo yo, pero
  necesito la lista completa de piezas cuando elijo la pista.</li>
  <li><strong>Un conjunto de títulos</strong> y animación de logotipo, hechos una vez y
  reutilizados.</li>
  <li><strong>Material rodado sabiendo que viene el vertical.</strong> Un recorte 9:16 pierde cerca
  del 60% de un encuadre 16:9, sobre todo por los lados. Puedo reencuadrar plano a plano, pero cuesta
  un día y sigue pareciendo un rescate.</li>
</ul>

<h3>Lo que sale de un solo trabajo</h3>
<ul>
  <li><strong>La película de marca</strong>, de 60 a 120 segundos</li>
  <li><strong>Un tráiler</strong>, de 30 a 45 segundos, que se sostiene solo</li>
  <li><strong>Un teaser</strong>, de 10 a 15 segundos</li>
  <li><strong>De tres a seis reels</strong>, verticales y subtitulados para verse sin sonido</li>
  <li><strong>Un corte cuadrado</strong> para los feeds que aún lo prefieren</li>
</ul>
<p>Hay dos más que salen casi gratis y suelen olvidarse: un corte sin sonido para pantallas de
eventos, y versiones en español, inglés y portugués. Hechas junto al original son poca cosa. Hechas
un año después obligan a reabrir un proyecto que ya nadie recuerda.</p>

<h3>La versión corta</h3>
<p>Si el vídeo solo va a vivir en tu web, encarga una película. Si va a correr en varias
plataformas, encarga la campaña entera de una vez. Lo que la mantiene unida se elige al principio y
no se puede añadir al final.</p>
<p>Si estás planeando algo, <a href="../../contact/">cuéntame qué tienes en mente</a> y te digo qué
pedir. El resto es <a href="../../services/">cosa mía</a>.</p>
""",
        },
        "body": """
<p class="lede">The same campaign now has to work on your homepage, in a LinkedIn feed, as a vertical
reel and sometimes on a silent screen at a trade show. Those are different films. The mistake is
commissioning them as different jobs.</p>


<h3>How separate commissions drift</h3>

<p>Ordered one at a time, the pieces stop looking like one campaign. The grade is a little warmer in
the second batch, because it was done months later on another monitor. The titles use a typeface
that isn't quite the brand's. The reels have different music, because the first license only
covered one film.</p>

<p>Nobody can say what's wrong. They just don't connect the pieces, so each one has to introduce you
from scratch. A campaign sticks through repetition, and that only works if people recognize the
second piece as part of the first.</p>


<h3>The same look, different films</h3>

<p>The other common mistake is cutting the short versions down from the long one. The
fifteen-second piece becomes the ninety-second one without its middle, and anyone who has seen one
has seen them all.</p>

<p>The pieces should share a grade, typography, music and rhythm, so people know it's you before the
logo appears. What they show should change. One opens on the founder, one is the product in use
with no words, one is thirty seconds of process.</p>


<h3>What has to be decided at the start</h3>

<ul>
  <li><strong>One grade</strong> and one set of references.</li>

  <li><strong>One music license</strong> covering every cut. I handle it, but I need the full list
  of pieces when I choose the track.</li>

  <li><strong>One set of titles</strong> and logo animation, built once and reused.</li>

  <li><strong>Footage shot knowing vertical is coming.</strong> A 9:16 crop loses about 60% of a
  16:9 frame, mostly from the sides. I can reframe shot by shot, but it costs a day and still looks
  rescued.</li>

</ul>

<h3>What you get from one job</h3>

<ul>
  <li><strong>The brand film</strong>, 60 to 120 seconds</li>

  <li><strong>A trailer</strong>, 30 to 45 seconds, that stands on its own</li>

  <li><strong>A teaser</strong>, 10 to 15 seconds</li>

  <li><strong>Three to six reels</strong>, vertical and subtitled for sound off</li>

  <li><strong>A square cut</strong> for feeds that still prefer it</li>

</ul>
<p>Two more come almost free and usually get forgotten: a silent cut for event screens, and versions
in English, Portuguese and Spanish. Done alongside the original they're small. Done a year later
they mean reopening a project nobody remembers.</p>


<h3>The short version</h3>

<p>If the video only lives on your website, buy one film. If it will run across platforms,
commission the whole campaign at once. The things that hold it together are chosen at the start
and can't be added at the end.</p>

<p>If you're planning something, <a href="../../contact/">tell me what you have in mind</a> and I'll
tell you what to ask for. The rest is <a href="../../services/">my department</a>.</p>
""",
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
<link rel="stylesheet" href="{root}assets/site.css?v=sig5">

<!-- Google Analytics (GA4), behind consent. It also measures Google Ads
     conversions (generate_lead, imported into Ads). Analytics sets a cookie,
     so under EU law it may not run until the visitor agrees. Nothing here loads until consent is stored: no script is fetched,
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
      // Consent Mode v2. This only runs after the visitor said yes, so
      // the state is "granted" from the first call. Google Ads in the EU
      // needs ad_user_data and ad_personalization stated explicitly, or it
      // will not count conversions. Personalisation stays denied: ads are
      // measured, never used to follow anyone around the web.
      window.gtag("consent", "default", {{
        analytics_storage: "granted",
        ad_storage: "granted",
        ad_user_data: "granted",
        ad_personalization: "denied"
      }});
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
      else if (window.__gaLoaded && window.gtag) {{
        // Withdrawn after it had loaded: stop it for the rest of this page.
        window.gtag("consent", "update", {{
          analytics_storage: "denied",
          ad_storage: "denied",
          ad_user_data: "denied",
          ad_personalization: "denied"
        }});
      }}
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
