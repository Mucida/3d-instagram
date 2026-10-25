"""Monta POSTAR/<data-dia>/ com os arquivos e um LEIA.md por dia, a partir de _producao/."""
import re, shutil
from pathlib import Path

R = Path('/home/mucida/3d-instagram')
P = R / '_producao'
cal = (P / 'calendario.md').read_text()

def bloco(titulo_ini):
    """Legenda (linhas '>') da seção ### que começa com titulo_ini."""
    m = re.search(r'^### ' + re.escape(titulo_ini) + r'.*?$(.*?)(?=^#{2,3} )', cal, re.S | re.M)
    return '\n'.join(l[2:] if l.startswith('> ') else l[1:] for l in m.group(1).splitlines() if l.startswith('>')).strip()

def roteiro(n):
    m = re.search(r'\*\*Roteiro ' + str(n) + r'.*?(?=\n\*\*Roteiro|\n> Conferir|\n---)', cal, re.S)
    return m.group(0).strip()

ST = P / 'pecas/stories/27out-09nov'
STK = {
    '27-enquete-energia': 'Enquete: "Sim" / "Nem sei quanto dá"',
    '28-1-quiz-energia': 'Quiz: R$ 0,50 (certa) / R$ 3 / R$ 8',
    '28-2-quiz-energia-resposta': 'Nenhum sticker: é a resposta do quiz. Poste umas horas depois do quiz.',
    '29-caixinha-dor': 'Caixinha de perguntas: "Manda aqui"',
    '30-link-calculadora': 'Link: 3dprintflow.com.br, texto "Calculadora grátis"',
    '31-enquete-primeira-venda': 'Enquete: "Já!" / "Ainda não"',
    '02-slider-planilha': 'Slider com emoji 😩',
    '03-novidade-pix': 'Link: 3dprintflow.com.br, texto "Assinar com Pix"',
    '04-enquete-onde-vende': 'Enquete: "Shopee" / "Mercado Livre" / "Feira" / "Direto"',
    '05-1-quiz-markup': 'Quiz: 100% / 50% (certa) / 25%',
    '05-2-quiz-markup-resposta': 'Nenhum sticker: é a resposta do quiz. Poste umas horas depois do quiz.',
    '06-enquete-feira': 'Enquete: "Vou!" / "Esse ano não"',
    '07-caixinha-feira': 'Caixinha de perguntas: "Cidade e nome da feira"',
    '09-caixinha-o-que-ver': 'Caixinha de perguntas: "Quero ver…"',
}
# dia: (pasta, título, feed, stories, extras)
DIAS = [
    ('2026-10-27-ter', 'Terça 27/10', ('carrossel', '01-custo-real', 'Ter 27/10'), ['27-enquete-energia'], 'Depois de postar o carrossel, compartilhe ele nos stories.'),
    ('2026-10-28-qua', 'Quarta 28/10', None, ['28-1-quiz-energia', '28-2-quiz-energia-resposta'], 'Grave um story de 10 s da sua impressora imprimindo (bastidor).'),
    ('2026-10-29-qui', 'Quinta 29/10', ('reel', 'r1-so-filamento', 'Qui 29/10'), ['29-caixinha-dor'], 'Depois de postar o Reel, compartilhe ele nos stories.'),
    ('2026-10-30-sex', 'Sexta 30/10', None, ['30-link-calculadora'], 'Antes do story de link, poste 2 ou 3 respostas da caixinha de ontem (sem mostrar quem mandou).'),
    ('2026-10-31-sab', 'Sábado 31/10', None, ['31-enquete-primeira-venda'], ''),
    ('2026-11-01-dom', 'Domingo 01/11', None, [], 'Só bastidor: foto ou vídeo curto de uma peça que você imprimiu ou de um carretel novo.'),
    ('2026-11-02-seg', 'Segunda 02/11', ('camera', 1, 'Seg 02/11'), ['02-slider-planilha'], ''),
    ('2026-11-03-ter', 'Terça 03/11', None, ['03-novidade-pix'], ''),
    ('2026-11-04-qua', 'Quarta 04/11', None, ['04-enquete-onde-vende'], ''),
    ('2026-11-05-qui', 'Quinta 05/11', ('carrossel', '02-markup-margem', 'Qui 05/11'), ['05-1-quiz-markup', '05-2-quiz-markup-resposta'], 'Compartilhe o carrossel nos stories antes do quiz.'),
    ('2026-11-06-sex', 'Sexta 06/11', ('reel', 'r2-feira', 'Sex 06/11'), ['06-enquete-feira'], 'Depois de postar o Reel, compartilhe ele nos stories.'),
    ('2026-11-07-sab', 'Sábado 07/11', None, ['07-caixinha-feira'], ''),
    ('2026-11-08-dom', 'Domingo 08/11', ('camera', 2, 'Dom 08/11'), [], 'Depois de postar o vídeo, compartilhe ele nos stories e ponha um sticker de link.'),
    ('2026-11-09-seg', 'Segunda 09/11', None, ['09-caixinha-o-que-ver'], 'Antes da caixinha, um story de resumo da quinzena (print dos posts que mais foram bem).'),
]

out = R / 'POSTAR'
shutil.rmtree(out, ignore_errors=True)
for pasta, titulo, feed, stories, extra in DIAS:
    d = out / pasta; d.mkdir(parents=True)
    L = [f'# {titulo}', '']
    if feed:
        tipo, ref, sec = feed
        if tipo == 'carrossel':
            src = P / 'pecas/carrosseis' / ref
            for f in sorted(src.glob('*.png')):
                shutil.copy(f, d / f'feed-{f.stem}.png')
            L += ['## Feed (Instagram + TikTok em modo foto), às 19h',
                  f'Carrossel: os arquivos `feed-01.png` a `feed-{len(list(src.glob("*.png"))):02d}.png`, nessa ordem.', '',
                  '**Legenda:**', '', bloco(sec), '']
        elif tipo == 'reel':
            mp4 = P / 'pecas/reels' / f'{ref}.mp4'
            if mp4.exists():
                shutil.copy(mp4, d / 'reel.mp4'); st = 'Arquivo: `reel.mp4`.'
            else:
                st = '**Ainda não está pronto.** Eu aviso quando o `reel.mp4` estiver nesta pasta.'
            L += ['## Reel (Instagram + TikTok, o mesmo arquivo), às 19h', st,
                  'No Instagram e no TikTok, escolha um áudio em alta no próprio app, com volume baixo.', '',
                  '**Legenda:**', '', bloco(sec), '']
        else:
            L += ['## Vídeo com você na câmera (Instagram + TikTok)',
                  'Grave no celular, em pé, com a impressora ou os carretéis atrás. Até 30 s. Ponha a legenda na tela, grande.', '',
                  roteiro(ref), '']
    if stories:
        L += ['## Stories (Instagram), nessa ordem', '']
        for i, s in enumerate(stories, 1):
            shutil.copy(ST / f'{s}.png', d / f'story-{i}.png')
            k = STK[s]
            L.append(f'{i}. `story-{i}.png`. ' + (k if k.startswith('Nenhum') else f'Sticker: {k}. Coloque no espaço vazio do meio.'))
        L.append('')
    if extra:
        L += ['## Também', extra, '']
    (d / 'LEIA.md').write_text('\n'.join(L))
res = out / '_reserva-carrossel-03-iniciante'; res.mkdir()
for f in sorted((P / 'pecas/carrosseis/03-iniciante').glob('*.png')):
    shutil.copy(f, res / f'feed-{f.stem}.png')
(res / 'LEIA.md').write_text('# Carrossel reserva: "5 custos desde a 1ª venda"\n\nPronto, guardado para a próxima quinzena.\n\n**Legenda:**\n\n' + bloco('Sáb 31/10') + '\n')
print('\n'.join(sorted(p.name + ': ' + ', '.join(sorted(x.name for x in p.iterdir())) for p in out.iterdir())))
