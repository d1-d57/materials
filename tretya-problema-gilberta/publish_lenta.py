#!/usr/bin/env python3
"""Публикационная копия ленты: view.html движка → artifact-совместимый HTML.

    python3 publish_lenta.py <view.html> <katex-dist-dir> <выход.html>

Две правки поверх вида, сам вид движка не трогается:
1. KaTeX CSS и шрифты woff2 инлайнятся: CSP артефакта не пускает внешние стили.
2. Оверлей CSS (решения владельца 2026-10-03): убраны шапка-дубль и вкладка; правой колонки
   сносок нет, поля встают в поток, колонка масштабируется вместе с кеглем под ширину окна (рисунки не шире 680px); оглавление по кнопке «содержание».
"""
import re, sys, base64
from pathlib import Path

vid, kdir, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
css = (kdir / "katex.min.css").read_text()
def font(m):
    blk = m.group(0)
    f = re.search(r"url\(fonts/([^)]+\.woff2)\)", blk).group(1)
    b = base64.b64encode((kdir / "fonts" / f).read_bytes()).decode()
    return re.sub(r"src:[^;}]+", 'src:url(data:font/woff2;base64,%s) format("woff2")' % b, blk)
css = re.sub(r"@font-face\{[^}]+\}", font, css)
v = vid.read_text(encoding="utf-8")
link = re.search(r'<link rel="stylesheet" href="https://cdn\.jsdelivr\.net/npm/katex@[^"]+katex\.min\.css"[^>]*>', v)
assert link, "в виде нет ссылки на KaTeX CSS — движок поменялся, проверить"
OVERLAY = """
.doc-head,.tabbar{display:none!important}
.wrap{max-width:none;padding-left:64px;padding-right:64px}
figure svg{max-width:min(100%,680px)}
/* ширина строки и кегль связаны: колонка движка (1090px при кегле 25.76px, ~88 знаков) масштабируется
   целиком через zoom, чтобы на широком экране заполнять ширину, не удлиняя строку в знаках */
@media(min-width:1300px){.wrap{zoom:1.1}}
@media(min-width:1500px){.wrap{zoom:1.25}}
@media(min-width:1700px){.wrap{zoom:1.4}}
@media(min-width:1900px){.wrap{zoom:1.55}}
@media(min-width:2200px){.wrap{zoom:1.75}}
@media(min-width:2500px){.wrap{zoom:2}}
.mn,figure.mn{position:static!important;left:auto;width:auto;margin:1.2em 0}
.stream>p:first-of-type{font-size:1.12em;line-height:1.6}
@media(max-width:520px){.wrap{padding-left:16px;padding-right:16px}}
@media(max-width:900px){details.toc:not(.open){display:none}
details.toc.open{display:block;position:fixed;top:0;left:0;right:0;max-height:80vh;overflow:auto;background:var(--bg);z-index:70;padding:1rem 16px;box-shadow:0 0 26px rgba(0,0,0,.3)}}
"""
v = v.replace(link.group(0), "<style>" + css + "</style>")
# Оверлей — ПОСЛЕДНИМ в <head>: стиль движка идёт после ссылки на KaTeX и иначе перебивает
# оверлей при равной специфичности (так ширина 03.10 не применилась).
assert v.count("</head>") == 1
v = v.replace("</head>", "<style>" + OVERLAY + "</style></head>")
out.write_text(v, encoding="utf-8")
print("ok", out, len(v) // 1024, "KB")
