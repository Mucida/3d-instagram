# HyperFrames: setup e uso para Reels/Stories 1080x1920

Testado em 2026-10-24: hyperframes 0.8.193 (npm `hyperframes`, repo github.com/heygen-com/hyperframes, Apache-2.0). Funcionou de primeira, sem precisar de Chrome especial. Node 22+ e FFmpeg exigidos (Node 23.3 ok).

## Passos que funcionaram
```bash
cd /home/mucida/3d-instagram/hf-teste
export HYPERFRAMES_SKIP_SKILLS=1                 # evita checagem de skills no GitHub no init
npx hyperframes init proj --resolution portrait --non-interactive --skip-skills
cd proj
# editar index.html
npx --yes hyperframes@0.8.193 check              # lint + runtime + layout + contraste; ~15 s
npx --yes hyperframes@0.8.193 preview --no-open  # http://localhost:3002 (--port)
npx --yes hyperframes@0.8.193 render -o ../teste.mp4 --quiet
npx --yes hyperframes@0.8.193 snapshot --at 2.5 --no-end -o ../still   # PNG 1080x1920 (imagem estatica)
```
Nao precisa instalar nada globalmente: `npx` baixa o pacote. `init` cria index.html, package.json (scripts dev/check/render fixados na versao), hyperframes.json, meta.json, AGENTS.md/CLAUDE.md. Presets de `--resolution`: portrait (1080x1920), landscape, square, versoes 4k.

## Modelo
- HTML + CSS + GSAP (timeline pausada). GSAP vem por CDN `<script>` (jsdelivr); tambem ha Lottie, canvas, Three.js (references/runtimes.md).
- Raiz: `<div id="root" data-composition-id="main" data-start="0" data-duration="4" data-width="1080" data-height="1920">`. `data-duration` da raiz = duracao do video. FPS: `data-fps` na raiz ou `render -f 30` (padrao 30; 24-240).
- Elementos temporizados: `class="clip" data-start data-duration` (segundos) e `data-track-index`.
- A timeline GSAP e registrada em `window.__timelines["<composition-id>"] = tl`. O renderer faz seek quadro a quadro (deterministico).
- Sub-composicoes em `compositions/*.html` (dentro de `<template>`), montadas via `data-composition-src`. Assets em `assets/` (caminhos relativos a raiz). Variaveis: `data-var-text`, `--variables '{...}'` no render.
- Formatos de saida: mp4 (padrao), webm/mov (com transparencia), gif, png-sequence, hls. Qualidade: `-q draft|looks(padrao, CRF16)|delivery`.
- Registro com ~450 blocos prontos: `npx hyperframes add <bloco>` / `catalog`. Skills para agentes: `npx hyperframes skills update`.

## Exemplo minimo que renderizou (hf-teste/proj/index.html)
```html
<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
  <meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <style>
    :root { --ground:#0f172a; --ink:#fff; --accent:#f59e0b; --font-display:"Montserrat",sans-serif; }
    *{margin:0;padding:0;box-sizing:border-box}
    html,body{width:1080px;height:1920px;overflow:hidden;background:var(--ground)}
    #root{position:relative;width:100%;height:100%;font-family:var(--font-display);color:var(--ink)}
    #title{position:absolute;left:90px;right:90px;top:700px;font-size:120px;font-weight:900;line-height:1.05}
    #bar{position:absolute;left:90px;top:1060px;width:400px;height:14px;background:var(--accent);transform-origin:left center}
    #sub{position:absolute;left:90px;right:90px;top:1110px;font-size:52px;color:#cbd5e1}
  </style>
</head>
<body>
  <div id="root" data-composition-id="main" data-start="0" data-duration="4" data-width="1080" data-height="1920">
    <h1 id="title" class="clip" data-start="0" data-duration="4" data-track-index="0">Olá, Reels!</h1>
    <div id="bar" class="clip" data-start="0" data-duration="4" data-track-index="1"></div>
    <p id="sub" class="clip" data-start="0" data-duration="4" data-track-index="2">Teste HyperFrames 1080x1920</p>
  </div>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    tl.fromTo("#title",{y:80,scale:.92},{y:0,scale:1,duration:.8,ease:"power4.out"},0);
    tl.fromTo("#bar",{scaleX:0},{scaleX:1,duration:.7,ease:"power3.out"},.6);
    tl.fromTo("#sub",{opacity:0,y:30},{opacity:1,y:0,duration:.6,ease:"power2.out"},1.0);
    window.__timelines["main"] = tl;
    tl.seek(0);
  </script>
</body>
</html>
```

## Resultado
- MP4: /home/mucida/3d-instagram/hf-teste/teste.mp4 (h264, yuv420p, 1080x1920, 30 fps, 4,00 s, 148 KB, sem faixa de audio)
- Render: ~24 s para 4 s de video (120 quadros), incluindo subir Chrome. `check` ~15 s.
- Still PNG 1080x1920: /home/mucida/3d-instagram/hf-teste/still/frame-00-at-2.5s.png

## Pegadinhas
- Chrome do sistema e usado automaticamente (/usr/bin/google-chrome). Aviso "beginFrame unavailable": cai em modo screenshot, mais lento mas funciona. Opcional: `npx @puppeteer/browsers install chrome-headless-shell` e `HYPERFRAMES_BROWSER_PATH`.
- Frame 0 e a thumbnail: o `check` avisa `first_frame_empty` se o titulo entra do nada (opacity 0). Deixe algo visivel em t=0.
- Regras do lint: nada de `Date.now()`, `Math.random()` sem semente, `repeat:-1`, fetch/timers; tudo funcao do tempo da timeline. Nao animar `display/visibility` num `.clip` (anime um filho); nao usar CSS `transform` num elemento que o GSAP anima (use `fromTo`).
- Fontes: so as embutidas resolvem por nome (Inter, Montserrat, Poppins, Oswald, Playfair etc.); as demais exigem `@font-face` com arquivo em `assets/fonts/`. As fontes sao baixadas do Google Fonts na primeira vez (cache em ~/.cache/hyperframes/fonts), entao precisa de internet no primeiro uso, tal como o GSAP via CDN. Para offline, baixe o gsap para `assets/` e referencie localmente (nao testado).
- Zona segura Instagram (guia do proprio framework, vertical.md): nada nos 168 px do topo; texto/produto entre 168 e 1330 px; abaixo disso (legenda, botoes) so decoracao; nada sob a coluna de botoes a direita.
- `init` tenta checar/instalar skills de agente; `--skip-skills` e "temporariamente ignorado", por isso `HYPERFRAMES_SKIP_SKILLS=1`. Existe telemetria anonima de render.
- `npx` imprime ExperimentalWarning do npm no Node 23 (inofensivo).
- Audio: adicionar via `<audio id="..." src="assets/x.mp3" data-start data-duration>` (precisa de `id`, senao fica fora do mix). Nao testado.
- Nao testado: preview no navegador (so a flag), render com audio/video embutido, `--docker`.
