#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Иллюстрации к научпоп-лекции «Кривая дракона» (30 минут) → SVG-фрагменты для doc-вида.

Источник → генератор → самодостаточный HTML. Вся геометрия СЧИТАЕТСЯ по
последовательности перегибов бумаги, ни одна вершина не поставлена руками:
правка рисунка = правка параметра.

Сквозной приём (требование владельца): углы ломаной скруглены МИНИМАЛЬНО.
Скругление снимает вопрос «касается или пересекается» без единого слова —
в точке двойного захода видно два разных уголка, а не крест.

Примитивы — по `_studio/konvejer/09-illustracii/SLOVAR-primitivov.md`:
  #4 путь-ломаная · #1 узел <circle r=3.4> · #2 отрезок · #10 стрелка · #11 метка
Внутри рисунка только МЕТКА; проза — в figcaption (пишется в *.md).
Цвет — только классом.

    python3 gen_ill.py            # → ill/*.svg
"""
import math
from pathlib import Path

OUT = Path(__file__).parent / "ill"

# ───────────────────────── геометрия дракона ─────────────────────────
# Главная ломаная: z0 = (0,0), z1 = (1,0). Направление k-го сгиба —
# регулярная последовательность перегибов бумаги (нечётная часть k mod 4).

def fold(k):
    while k % 2 == 0:
        k //= 2
    return 1 if k % 4 == 1 else -1


def dragon(n, start=(0, 0), d=(1, 0)):
    """Вершины ломаной дракона ранга n: 2ⁿ звеньев, целые координаты."""
    x, y = start
    dx, dy = d
    pts = [(x, y)]
    N = 2 ** n
    for k in range(1, N + 1):
        x += dx
        y += dy
        pts.append((x, y))
        if k < N:
            dx, dy = (-dy, dx) if fold(k) == 1 else (dy, -dx)
    return pts


def mul1pi(pts):
    """Умножение на (1+i): растяжение в √2 и поворот на 45°."""
    return [(x - y, x + y) for x, y in pts]


def parent_edge(a, b):
    """Родитель звена (a→b) — звено предыдущего ранга, читаемый по геометрии.

    Возвращает (бит, родитель): бит 0 — звено первая половинка уголка
    (горизонталь), бит 1 — вторая (вертикаль). Недостающую координату
    родителя досказывает чётность узла в прежней картинке.
    """
    def div(p):                       # деление на (1+i)
        x, y = p
        return ((x + y) // 2, (y - x) // 2)
    if a[1] == b[1]:                                   # горизонтальное
        w = a
        dx = b[0] - a[0]
        ev = sum(div(w)) % 2 == 0
        dy = (1 if ev else -1) if dx == 1 else (-1 if ev else 1)
        return 0, (w, (w[0] + dx, w[1] + dy))
    w = b                                              # вертикальное
    dy = b[1] - a[1]
    ev = sum(div(w)) % 2 == 0
    dx = (-1 if ev else 1) if dy == 1 else (1 if ev else -1)
    return 1, ((w[0] - dx, w[1] - dy), w)


# ───────────────────────── экранная кухня ─────────────────────────

def bbox(pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def fitter(pts, x, y, w, h, pad=10):
    """Целые вершины → экранные координаты внутри бокса. Возвращает (T, шаг)."""
    x0, y0, x1, y1 = bbox(pts)
    s = min((w - 2 * pad) / max(x1 - x0, 1), (h - 2 * pad) / max(y1 - y0, 1))
    ox = x + pad + ((w - 2 * pad) - s * (x1 - x0)) / 2
    oy = y + pad + ((h - 2 * pad) - s * (y1 - y0)) / 2

    def T(p):
        return (round(ox + (p[0] - x0) * s, 2),
                round(y + h - (oy - y) - (p[1] - y0) * s, 2))
    return T, s


def rpath(P, r, cls="s-line", prec=2, width=None):
    """Примитив #4 со СКРУГЛЁННЫМИ углами. r — радиус в пикселях."""
    if len(P) < 3:
        return '<polyline class="%s" points="%s"/>' % (
            cls, " ".join("%g,%g" % p for p in P))
    f = "%%.%df" % prec
    d = ["M " + f % P[0][0] + "," + f % P[0][1]]
    for i in range(1, len(P) - 1):
        p0, p1, p2 = P[i - 1], P[i], P[i + 1]
        l1 = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        l2 = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        rr = min(r, l1 / 2, l2 / 2)
        if rr <= 0.01:
            d.append("L " + f % p1[0] + "," + f % p1[1])
            continue
        ax = p1[0] + (p0[0] - p1[0]) / l1 * rr
        ay = p1[1] + (p0[1] - p1[1]) / l1 * rr
        bx = p1[0] + (p2[0] - p1[0]) / l2 * rr
        by = p1[1] + (p2[1] - p1[1]) / l2 * rr
        d.append("L " + f % ax + "," + f % ay)
        d.append("Q " + f % p1[0] + "," + f % p1[1] + " " + f % bx + "," + f % by)
    d.append("L " + f % P[-1][0] + "," + f % P[-1][1])
    sw = ' stroke-width="%g"' % width if width else ""
    return '<path class="%s" fill="none"%s d="%s"/>' % (cls, sw, " ".join(d))


def node(p, cls="s-node", r=3.4):
    return '<circle class="%s" cx="%g" cy="%g" r="%g"/>' % (cls, p[0], p[1], r)


def txt(p, s, cls="s-txt", anchor="middle"):
    return '<text class="%s" x="%g" y="%g" text-anchor="%s">%s</text>' % (
        cls, p[0], p[1], anchor, s)


def arrow(p, q, cls="s-ar-m"):
    """Примитив #10: линия + голова явными координатами (без transform)."""
    ln = math.hypot(q[0] - p[0], q[1] - p[1])
    if ln < 1:
        return ""
    ux, uy = (q[0] - p[0]) / ln, (q[1] - p[1]) / ln
    nx, ny = -uy, ux
    base = (q[0] - 9 * ux, q[1] - 9 * uy)
    a = (base[0] + 4 * nx, base[1] + 4 * ny)
    b = (base[0] - 4 * nx, base[1] - 4 * ny)
    return ('<line class="s-thin" x1="%g" y1="%g" x2="%g" y2="%g"/>'
            '<polygon class="%s" points="%g,%g %g,%g %g,%g"/>'
            % (p[0], p[1], base[0], base[1], cls,
               q[0], q[1], a[0], a[1], b[0], b[1]))


def grid(T, s, x0, y0, x1, y1):
    """Тонкая сетка по целым координатам — фон для мелких схем."""
    b = []
    for gx in range(x0, x1 + 1):
        p, q = T((gx, y0)), T((gx, y1))
        b.append('<line class="s-thin" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (p[0], p[1], q[0], q[1]))
    for gy in range(y0, y1 + 1):
        p, q = T((x0, gy)), T((x1, gy))
        b.append('<line class="s-thin" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (p[0], p[1], q[0], q[1]))
    return b


def svg(w, h, body, label):
    return ('<svg viewBox="0 0 %d %d" width="%d" role="img" aria-label="%s">\n%s\n</svg>'
            % (w, h, w, label, body))


def save(name, s):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / (name + ".svg")).write_text(s, encoding="utf-8")
    print("  ill/%s.svg  (%d симв.)" % (name, len(s)))


