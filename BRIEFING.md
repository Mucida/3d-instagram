# Briefing — produção de conteúdo @app3dprintflow

Leia isto antes de continuar. Calendário e legendas: `calendario.md`. Pesquisa: `pesquisa/`.

## Fontes de verdade
- **marketing-mcp** do SaaS (`~/imaginario/tools/marketing-mcp`, só leitura, app de teste em `localhost:8083`). Não está registrado nesta pasta; chame com
  `node <scratchpad>/mcpcall.mjs <tool> '<json>' <saida.json>` (cliente stdio; se o scratchpad sumiu, recriar: Client + StdioClientTransport do SDK em `node_modules` do marketing-mcp, command `bin/mcp.sh`, env `MARKETING_OUT_DIR=/home/mucida/3d-instagram/marketing-kit`).
- Respostas já salvas em `marketing-kit/*.json` (brand kit, features, telas, changelog desde 01/08, demo story 6m). Capturas em `marketing-kit/screens/` e copiadas para `pecas/_base/`.
- Regras de marca (afirmações proibidas): `get_brand_kit` → `voz.afirmacoes_proibidas`. Resumo no topo de `calendario.md`.

## Números da Loja Demo usados (fictícios — sempre "loja de demonstração")
- Projeto Par de Bules Arco-íris (`/projetos/4098`): A1 95 W, 330 min, R$ 0,95/kWh; 110 g PLA Silk a R$ 186,58/kg. Filamento 20,52 · energia 0,50 · desgaste 3,63 · mão de obra 2,10 (0,07 h × R$ 30) · risco 1,97 · **total 28,72**. Venda 59,90, lucro estimado 31,18.
- Feira Anime Fest 2ª ed. (`/eventos/24/resultado`): vendido 1.274,20 · comissão/maquininha −142,19 · peças −422,99 · estande −240 · banner −90 · transporte −60 · credencial −40 · **lucro 279,02**. 39 de 50 peças vendidas.
- Novidade v1.24 (20/10/2026): assinatura com Pix, mensal ou anual, sem renovação automática, aviso por e-mail.

## Sistema visual (`pecas/_base/`)
- `brand.css`: tokens (azul #1e88e5, laranja #ff6b1a, ciano, âmbar, noite #070d1f), fontes locais Archivo/Inter/JetBrains Mono, `.bg` (noite com brilho azul em cima e laranja embaixo + grade), `.eyebrow` (pílula mono), `.marca` (ícone `logo-simples.png` + "3D **Print Flow**" laranja), `.phone` (moldura p/ captura), `.card`.
- `carrossel.css`: layout 1080×1350 dos slides (`.slide`, `.rodape`, `.valor`, `.sub`, `.soma`...).
- Logo horizontal `logo.png` NÃO serve em fundo escuro. Mascote `mascote.png` (pose joinha, única que existe).
- Render de estáticos: `node pecas/render-slides.mjs <html> <pasta>` (Playwright do marketing-mcp + Chrome do sistema; cada `.slide[data-nome]` vira PNG).

## Feito
- Carrosséis 01-custo-real (8), 02-markup-margem (6), 03-iniciante (8) em `pecas/carrosseis/`, revisados visualmente.
- `calendario.md` com legendas, roteiros de câmera e plano de stories. Ritmo novo (24/10): 2–3 posts/semana, 4–6 stories/dia, tudo vale pro TikTok @3d.print.flow (`pesquisa/tiktok.md`).
- 14 stories interativos 27/10–09/11 em `pecas/stories/27out-09nov/` (fonte `pecas/stories-27out-09nov.html`, CSS `_base/story.css`). Revisão: `render-slides.mjs ... --guia` + `python3 pecas/prancha.py <pasta> <saida.jpg>`.
- Repo privado github.com/Mucida/3d-instagram. `ROTINA.md` = instruções da rotina diária das 10h (nuvem): tendências + stories do dia em `diario/` e `pecas/stories/AAAA-MM-DD/`.

## Falta
1. **Reels HyperFrames** (projeto base pronto em `pecas/reels/base/`, com `assets/` = fontes, PNGs, `gsap.min.js` local). Copiar `base` para cada reel e escrever `index.html`:
   - **r1-so-filamento** (~15 s): gancho "Se você imprime pra vender / e cobra só o filamento…" (visível em t=0) → pilha de custos entrando linha a linha com total trocando 20,52 → 21,02 → 24,65 → 26,75 → 28,72 (troca por opacidade de spans; não usar contador com onUpdate) → celular com `projetos-4098` subindo → CTA "Calculadora grátis pra sempre · link na bio" + nota "loja de demonstração".
   - **r2-feira** (~15 s): "Voltou da feira com R$ 1.274 vendidos… / e lucrou quanto?" → descontos caindo um a um → "Lucro da feira R$ 279,02" verde → celular com `eventos-24-resultado` → CTA "Eventos · a partir do Starter · 7 dias grátis".
   - ~~r3-pix~~: virou story (`03-novidade-pix.png`).
   - Sem áudio (ele põe áudio em alta no app). Zona segura: texto entre y 168 e 1330, nada sob a coluna de botões à direita.
   - HyperFrames 0.8.193: raiz `#root[data-composition-id=main][data-duration][data-width=1080][data-height=1920]`; cada cena `.clip` com `data-start/-duration/-track-index`; animar filhos, não o `.clip`; `window.__timelines.main = tl` pausada; nada de Math.random/Date/repeat:-1. Comandos: `npx --yes hyperframes@0.8.193 check`, `render -o out.mp4 --quiet`, `snapshot --at N --no-end -o dir`. Ver `pesquisa/hyperframes-setup.md`.
2. Criar a rotina na nuvem se ainda não existir (claude.ai/code/routines; a API daqui deu 401 "Connect your GitHub account").
3. Revisar cada peça com prancha de miniaturas antes de entregar.
