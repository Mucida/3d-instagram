"""Prancha de miniaturas para revisão. Uso: python3 pecas/prancha.py <pasta-de-png> <saida.jpg> [colunas] [largura]"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

pasta, saida = Path(sys.argv[1]), sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 7
w = int(sys.argv[4]) if len(sys.argv) > 4 else 300
pngs = sorted(pasta.glob("*.png"))
ims = [Image.open(p).convert("RGB") for p in pngs]
h = max(round(w * im.height / im.width) for im in ims)
rot = 26
rows = (len(ims) + cols - 1) // cols
folha = Image.new("RGB", (cols * (w + 12) + 12, rows * (h + rot + 12) + 12), (30, 30, 30))
d = ImageDraw.Draw(folha)
for i, (p, im) in enumerate(zip(pngs, ims)):
    x, y = 12 + (i % cols) * (w + 12), 12 + (i // cols) * (h + rot + 12)
    folha.paste(im.resize((w, round(w * im.height / im.width))), (x, y + rot))
    d.text((x, y + 4), p.stem[:40], fill=(220, 220, 220))
folha.save(saida, quality=88)
print(f"{len(ims)} miniaturas em {saida}")
