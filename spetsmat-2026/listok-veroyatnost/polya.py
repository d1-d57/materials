#!/usr/bin/env python3
"""Рычаг «картинки в полях» (К9.7; v19: при масштабе 1,3 картинки вылезли за край листа).

    python3 polya.py листок.pdf [листок-179-pechat.pdf ...]   → rc=1, если где-то чернила за полосой набора.

Полоса набора — от самого левого до самого правого слова во всём PDF (pdftotext -bbox).
Страница растеризуется в 72 dpi (1 пиксель = 1 pt); всё тёмное левее или правее полосы
больше чем на ДОПУСК pt — нарушение: печатается страница, сторона и на сколько pt вылезло.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

DOPUSK = 3      # pt: толщина линий и выносные элементы формул
TEMNOE = 160    # яркость пикселя (0–255), ниже которой считаем чернилами; серая сетка картинок светлее


def polosa(pdf):
    html = subprocess.run(["pdftotext", "-bbox", pdf, "-"], capture_output=True, text=True).stdout
    xs = [(float(a), float(b)) for a, b in re.findall(r'<word xMin="([\d.]+)" yMin="[\d.]+" xMax="([\d.]+)"', html)]
    return min(a for a, _ in xs), max(b for _, b in xs)


def proverit(pdf):
    lev, prav = polosa(pdf)
    plohie = []
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["pdftoppm", "-r", "72", "-gray", pdf, str(Path(d) / "s")], check=True)
        for f in sorted(Path(d).glob("s-*.pgm"), key=lambda p: int(p.stem.split("-")[1])):
            im = Image.open(f)
            w, h = im.size
            px = im.load()
            stolb = [x for x in range(w) if any(px[x, y] < TEMNOE for y in range(h))]
            if not stolb:
                continue
            s = int(f.stem.split("-")[1])
            if stolb[0] < lev - DOPUSK:
                plohie.append("%s, стр. %d: слева за полосой на %.0f pt" % (pdf, s, lev - stolb[0]))
            if stolb[-1] + 1 > prav + DOPUSK:
                plohie.append("%s, стр. %d: справа за полосой на %.0f pt" % (pdf, s, stolb[-1] + 1 - prav))
    return plohie


if __name__ == "__main__":
    vse = [p for f in sys.argv[1:] for p in proverit(f)]
    for p in vse:
        print(p)
    sys.exit(1 if vse else 0)
