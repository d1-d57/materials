#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Рисунки печатного листка Л1. Ч/б, самодостаточный SVG (в листке нет CSS-классов
doc-движка — это отдельный печатный конвейер, FORMAT-LISTKA).

Рис. 2 рисуем САМИ, а не берём из статьи (решение владельца 2026-07-17: «правую
точно нужно сделать самостоятельно, чтобы выглядело симпатичнее»). Рис. 1 (полоска
ребром на столе) остаётся сканом статьи — переносить разрешено.

Честный масштаб: полоска ОДНА И ТА ЖЕ, поэтому её полная длина во всех четырёх
панелях одинакова, а звено делится пополам с каждым складыванием — ровно так
нарисовано в статье. Что показываем: 1 складывание · 2 · и два РАЗНЫХ исхода
после 3 (проверено перебором: после 1 и 2 складываний ломаная по сути одна,
после 3 их уже две).

    python3 gen_l1_figs.py     # → L1-fig2.svg
"""
from pathlib import Path

STRIP = 200.0                      # полная длина полоски, одинакова во всех панелях
INK, DOT = "#000", "#000"


def bar(s):
    return "".join("R" if c == "L" else "L" for c in reversed(s))


def word(choices):
    s = ""
    for x in choices:
        s = s + x + bar(s)
    return s


def poly(w):
    x = y = 0
    dx, dy = 1, 0
    pts = [(0, 0), (1, 0)]
    x, y = 1, 0
    for c in w:
        dx, dy = (-dy, dx) if c == "L" else (dy, -dx)
        x, y = x + dx, y + dy
        pts.append((x, y))
    return pts


def bbox(pts):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


# панели: (метка, слово, число складываний)
PANELS = [
    ("1",  word(["L"]),                1),
    ("2",  word(["L", "L"]),           2),
    ("3а", word(["L", "L", "L"]),      3),   # всегда в одну сторону
    ("3б", word(["L", "R", "L"]),      3),   # второй существенно иной исход
]


def build():
    CW, CH, PAD, LAB = 150, 150, 12, 20      # ячейка, поля, место под метку
    W, H = CW * len(PANELS), CH + LAB
    out = []
    for i, (label, w, n) in enumerate(PANELS):
        link = STRIP / (2 ** n)              # честно: звено делится пополам
        P = poly(w)
        x0, y0, x1, y1 = bbox(P)
        # центрируем фигуру в своей ячейке; масштаб НЕ подгоняем — он задан длиной звена
        ox = i * CW + (CW - (x1 - x0) * link) / 2 - x0 * link
        oy = PAD + (CH - 2 * PAD - (y1 - y0) * link) / 2 + y1 * link
        T = lambda p: (round(ox + p[0] * link, 2), round(oy - p[1] * link, 2))
        pts = [T(p) for p in P]
        out.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.2" '
                   'stroke-linejoin="round" stroke-linecap="round"/>'
                   % (" ".join("%g,%g" % p for p in pts), INK))
        out.append('<circle cx="%g" cy="%g" r="3.6" fill="%s"/>' % (pts[0][0], pts[0][1], DOT))
        out.append('<text x="%g" y="%g" text-anchor="middle" fill="%s" '
                   'font-family="Georgia, serif" font-size="13" font-style="italic">%s</text>'
                   % (i * CW + CW / 2, CH + 14, INK, label))
    return ('<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" role="img" '
            'aria-label="Ломаные дракона после одного, двух и трёх складываний полоски; '
            'после трёх складываний ломаные бывают двух разных видов">\n%s\n</svg>'
            % (W, H, "\n".join(out)))


if __name__ == "__main__":
    p = Path(__file__).parent / "L1-fig2.svg"
    p.write_text(build(), encoding="utf-8")
    print("→ %s (%d симв.)" % (p.name, len(p.read_text(encoding='utf-8'))))
