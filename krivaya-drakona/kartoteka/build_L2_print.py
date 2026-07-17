#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сборка печатного мини-листка Л2: шаблон + фигуры из gen_l2_figs.py → L2-print.html.

Зачем скрипт, а не рукопашная вставка SVG (как было на Л1): фигуры правятся чаще
текста, а вклеенный руками SVG после каждой правки надо переклеивать — и легко
забыть, оставив в листке вчерашнюю картинку.

⚠ Грабли WeasyPrint (см. NAVIGATOR): inline-SVG схлопывается при width:auto —
поэтому ширину И высоту считаем из viewBox и ставим в мм явно. Flex внутри
листка разваливает страницу — только inline-block.

    python3 gen_l2_figs.py && python3 build_L2_print.py
    python3 -m weasyprint L2-print.html L2-print.pdf
    pdftoppm -png -r 110 L2-print.pdf preview     # → глазами
"""
from pathlib import Path

HERE = Path(__file__).parent
FIGS = {"<!--RANG4-->": ("L2-fig-rang4.svg", 96), "<!--TREUG-->": ("L2-fig-treug.svg", 40)}


def inject(html):
    for marker, (name, w_mm) in FIGS.items():
        s = (HERE / name).read_text(encoding="utf-8")
        vb = s.split('viewBox="')[1].split('"')[0].split()
        W, H = float(vb[2]), float(vb[3])
        h_mm = round(w_mm * H / W, 1)
        s = s.replace("<svg ", '<svg width="%gmm" height="%gmm" style="display:block" '
                      % (w_mm, h_mm), 1)
        print("  %s: viewBox %g×%g → %g×%g мм" % (name, W, H, w_mm, h_mm))
        html = html.replace(marker, s)
    return html


if __name__ == "__main__":
    src = (HERE / "L2-print-tmpl.html").read_text(encoding="utf-8")
    out = HERE / "L2-print.html"
    out.write_text(inject(src), encoding="utf-8")
    print("→ %s (%d симв.)" % (out.name, len(out.read_text(encoding='utf-8'))))
