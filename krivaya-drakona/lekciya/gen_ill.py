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


# ═════════════════ иллюстрации ═════════════════
R = 0.30            # скругление угла в долях звена: крупное, чтобы в точке
                    # двойного захода читались два уголка, а не перекрёсток


# ───────────────── A. полоска складывается и разворачивается ─────────────────
def ill_strip():
    W, H = 545, 400
    ROW, SL = 96, 250
    b = []
    for row, n in enumerate((1, 2, 3, 4)):
        ytop = 30 + row * ROW
        cw, x0 = SL / 2 ** n, 52
        b.append('<rect class="s-line s-fillsh" x="%g" y="%g" width="%g" height="16"/>'
                 % (x0, ytop, SL))
        for k in range(1, 2 ** n):
            xc = x0 + cw * k
            if fold(k) == 1:
                b.append('<line class="s-accent" x1="%g" y1="%g" x2="%g" y2="%g"/>'
                         % (xc, ytop - 7, xc, ytop + 16))
            else:
                b.append('<line class="s-line" x1="%g" y1="%g" x2="%g" y2="%g"/>'
                         % (xc, ytop, xc, ytop + 23))
        b.append(txt((x0 - 12, ytop + 12), "%d" % n, "s-txt-m", "end"))
        b.append(arrow((x0 + SL + 16, ytop + 8), (x0 + SL + 52, ytop + 8)))
        P = dragon(n)
        T, s = fitter(P, x0 + SL + 62, ytop - 26, 150, 76, pad=11)
        b.append(rpath([T(p) for p in P], s * R, "s-accent", width=1.7))
        b.append(node(T(P[0]), "s-node", 2.8))
    return svg(W, H, "\n".join(b), "Полоска, сложенная 1, 2, 3 и 4 раза, и ломаная, которая получается после разгибания всех сгибов до прямого угла")


def seg(p, q, cls, w=4.2):
    """Одно звено своим цветом, круглые торцы. Для раскрашивания по рёбрам."""
    return ('<line class="%s" stroke-linecap="round" stroke-width="%g" '
            'x1="%g" y1="%g" x2="%g" y2="%g"/>' % (cls, w, p[0], p[1], q[0], q[1]))


# ───────────────── f2. лента в два цвета: две одинаковые половины ─────────────
def ill_halves(n=6):
    W, H = 560, 430
    SL, x0, ytop = 400, 80, 26
    b = [seg((x0, ytop), (x0 + SL / 2, ytop), "s-line", 15),
         seg((x0 + SL / 2, ytop), (x0 + SL, ytop), "s-accent", 15),
         node((x0 + SL / 2, ytop), "s-node", 4.4),
         arrow((W / 2, ytop + 26), (W / 2, ytop + 58))]
    P = dragon(n)
    N = 2 ** n
    T, s = fitter(P, 0, ytop + 68, W, H - ytop - 78, pad=20)
    b += [rpath([T(p) for p in P[:N // 2 + 1]], s * R, "s-line", width=2.2),
          rpath([T(p) for p in P[N // 2:]], s * R, "s-accent", width=2.2),
          node(T(P[N // 2]), "s-node", 4.4)]
    return svg(W, H, "\n".join(b), "Лента, покрашенная в два цвета с середины, и кривая, которая из неё получилась. Половины кривой одинаковы: цветная — это тёмная, повёрнутая на 90 градусов вокруг средней точки")


# ───────────────── f3. ещё одно складывание: рёбра идут парами ────────────────
def ill_pairs(n=3):
    W, H, PW = 620, 250, 200
    A, Bg = dragon(n), dragon(n + 1)
    b = []
    # панель 1: рёбра чередуются по цвету
    T, s = fitter(A, 6, 30, PW - 12, H - 54, pad=16)
    for k in range(len(A) - 1):
        b.append(seg(T(A[k]), T(A[k + 1]), "s-line" if k % 2 == 0 else "s-accent"))
    for a in A:
        b.append(node(T(a), "s-node", 3.0))
    b.append(txt((6 + PW / 2 - 6, 20), "%d складывания" % n, "s-txt-m"))
    # панель 2: то же после ещё одного складывания — цвета идут парами
    T2, s2 = fitter(Bg, 6 + PW, 30, PW - 12, H - 54, pad=16)
    for k in range(len(Bg) - 1):
        b.append(seg(T2(Bg[k]), T2(Bg[k + 1]), "s-line" if (k // 2) % 2 == 0 else "s-accent"))
    for k in range(0, len(Bg), 2):                # границы пар
        b.append(node(T2(Bg[k]), "s-node", 3.0))
    b.append(txt((6 + PW + PW / 2 - 6, 20), "%d складывания" % (n + 1), "s-txt-m"))
    # панель 3: соединили пары обратно
    T3, s3 = fitter(Bg, 6 + 2 * PW, 30, PW - 12, H - 54, pad=16)
    b.append(rpath([T3(p) for p in Bg], s3 * R, "s-thin", width=1.4))
    M = Bg[::2]
    for k in range(len(M) - 1):
        b.append(seg(T3(M[k]), T3(M[k + 1]), "s-line" if k % 2 == 0 else "s-accent"))
    b.append(txt((6 + 2 * PW + PW / 2 - 6, 20), "соединили пары", "s-txt-m"))
    return svg(W, H, "\n".join(b), "Слева кривая после трёх складываний, рёбра покрашены через одно. В середине она же после четвёртого складывания: каждое ребро стало парой рёбер своего цвета. Справа пары соединены обратно — получилась левая кривая, только крупнее и повёрнутая")


# ───────────────── C1. ещё одно складывание гнёт каждое звено ─────────────────
def ill_onefold(n=3):
    W, H, PW = 620, 250, 200
    Q = mul1pi(dragon(n))            # прошлый ранг, растянутый: звенья — диагонали клеток
    P = dragon(n + 1)
    ref = Q + P
    b = []
    for i, (what, lab) in enumerate(((0, "%d складывания" % n), (1, "%d складывания" % (n + 1)), (2, "вместе"))):
        T, s = fitter(ref, 6 + i * PW, 24, PW - 10, H - 46, pad=14)
        if what in (0, 2):
            b.append(rpath([T(p) for p in Q], 0, "s-dash" if what == 2 else "s-line", width=1.6))
        if what in (1, 2):
            b.append(rpath([T(p) for p in P], s * R, "s-accent", width=1.9))
        for p in Q:
            b.append(node(T(p), "s-node-r", 2.7))
        if what == 2:
            for k in range(1, len(P), 2):
                b.append(node(T(P[k]), "s-node", 2.7))
        b.append(txt((6 + i * PW + PW / 2 - 5, 16), lab, "s-txt-m"))
    return svg(W, H, "\n".join(b), "Слева кривая после трёх складываний, в середине после четырёх, справа обе вместе. Каждое звено левой кривой согнулось пополам; тёмные точки — вершины, которые были и раньше, светлые — те, что появились при последнем складывании")


# ───────────────── C2. и та же кривая растёт вперёд ─────────────────
def ill_forward(n=6):
    W, H = 560, 400
    P = dragon(n)
    N = 2 ** n
    T, s = fitter(P, 0, 0, W, H, pad=22)
    b = [rpath([T(p) for p in P[:N // 2 + 1]], s * R, "s-line", width=2.0),
         rpath([T(p) for p in P[N // 2:]], s * R, "s-accent", width=2.0),
         node(T(P[N // 2]), "s-node-a", 4.4),
         node(T(P[0]), "s-node", 3.4), node(T(P[-1]), "s-node", 3.4)]
    return svg(W, H, "\n".join(b), "Ломаная ранга 6. Цветная половина — это тёмная, повёрнутая на 90 градусов вокруг средней вершины. Так кривая растёт вперёд: к готовой ломаной приклеивают её же повёрнутую копию")


# ───────────────── B. ранг 10: забит до отказа ─────────────────
def ill_dense(n=10):
    W, H = 620, 470
    P = dragon(n)
    T, s = fitter(P, 0, 0, W, H, pad=16)
    b = [rpath([T(p) for p in P], s * R, "s-line", prec=1, width=1.5),
         node(T(P[0]), "s-node", 3.0), node(T(P[-1]), "s-node-a", 3.0)]
    return svg(W, H, "\n".join(b), "Ломаная ранга 10: 1024 звена. Углы скруглены — там, где линия подходит к себе вплотную, видно два разных уголка, а не перекрёсток")


# ───────────────── E1. два сорта узлов ─────────────────
def ill_chess(n=4):
    W, H = 560, 340
    P, Q = dragon(n), mul1pi(dragon(n - 1))
    x0, y0, x1, y1 = bbox(P)
    T, s = fitter(P, 0, 0, W, H, pad=34)
    b = grid(T, s, x0, y0, x1, y1)
    b.append(rpath([T(p) for p in Q], 0, "s-dash", width=1.5))
    b.append(rpath([T(p) for p in P], s * R, "s-line", width=2.0))
    for k in range(len(P) - 1):
        p, q = T(P[k]), T(P[k + 1])
        m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        ln = math.hypot(q[0] - p[0], q[1] - p[1])
        ux, uy = (q[0] - p[0]) / ln, (q[1] - p[1]) / ln
        nx, ny = -uy, ux
        bs = (m[0] - 8 * ux, m[1] - 8 * uy)
        b.append('<polygon class="s-ar-a" points="%g,%g %g,%g %g,%g"/>'
                 % (m[0] + 3 * ux, m[1] + 3 * uy, bs[0] + 4.5 * nx, bs[1] + 4.5 * ny,
                    bs[0] - 4.5 * nx, bs[1] - 4.5 * ny))
    for p in dict.fromkeys(P):
        b.append(node(T(p), "s-node-r" if (p[0] + p[1]) % 2 == 0 else "s-node"))
    return svg(W, H, "\n".join(b), "Ломаная ранга 4 со стрелками хода; пунктиром — прошлый ранг. Тёмные узлы имеют чётную сумму координат и лежат ровно на пунктире: это старые вершины. Из каждой тёмной вершины ход идёт вбок, из каждой светлой — вверх или вниз")


# ───────────────── E2. правило строк ─────────────────
def stripes(T, W, y0, y1):
    out = []
    for gy in range(y0, y1 + 1):
        if gy % 2:
            continue
        top, bot = T((0, gy + 0.5))[1], T((0, gy - 0.5))[1]
        out.append('<rect class="s-fillsh" x="0" y="%g" width="%d" height="%g"/>'
                   % (top, W, bot - top))
    return out


def turn_left(a, b, c):
    u = (b[0] - a[0], b[1] - a[1])
    v = (c[0] - b[0], c[1] - b[1])
    return u[0] * v[1] - u[1] * v[0] > 0


def ill_stripes(n=6):
    """Правило поворота. Цветом помечен УГОЛОК, а не вершина: вершины во всех
    картинках значат одно и то же (чёрная точка — старая, кружок — новая),
    и перекрашивать их под другое утверждение нельзя."""
    W, H = 560, 400
    P = dragon(n)
    x0, y0, x1, y1 = bbox(P)
    T, s = fitter(P, 0, 0, W, H, pad=26)
    b = stripes(T, W, y0, y1)
    for k in range(0, len(P) - 2, 2):                    # уголок = два звена
        tri = [T(P[k]), T(P[k + 1]), T(P[k + 2])]
        cls = "s-accent" if turn_left(P[k], P[k + 1], P[k + 2]) else "s-line"
        b.append(rpath(tri, s * R, cls, width=2.4))
    for k in range(0, len(P), 2):
        b.append(node(T(P[k]), "s-node-r", 2.6))         # старая вершина
    for k in range(1, len(P), 2):
        b.append(node(T(P[k]), "s-node", 2.6))           # новая вершина
    return svg(W, H, "\n".join(b), "Ломаная ранга 6, разбитая на уголки. Голубые уголки поворачивают налево, чёрные направо. Строки покрашены через одну, и все голубые уголки ломаются в голубых строках, все чёрные — в белых")


def ill_restore():
    """Две картинки: звено из чёрной вершины в новую и звено из новой в чёрную.
    Больше на картинке нет ничего."""
    W, H = 560, 300
    b = []
    for i, first in enumerate((True, False)):
        ox = i * 280
        T, s = fitter([(-1, -1), (2, 1)], ox, 26, 280, H - 40, pad=26)
        if i == 0:
            bb = stripes(T, W, -1, 1)
        A, Wn = (0, 0), (1, 0)                            # строка A голубая
        up, dn = (1, 1), (1, -1)
        b += grid(T, s, -1, -1, 2, 1)
        if first:                                          # видим A → Wn
            b.append('<line class="s-dash" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (T(Wn) + T(up)))
            b.append('<line class="s-dash" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (T(Wn) + T(dn)))
            b.append(node(T(up), "s-node-r", 2.6))
            b.append(node(T(dn), "s-node-r", 2.6))
            b.append('<line class="s-accent" stroke-width="3" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (T(A) + T(Wn)))
            b.append(arrow(T(A), T(Wn), "s-ar-a"))
            b.append(node(T(A), "s-node-r", 2.6))
            cx, cy = T((1.0, -0.5))
            lab = "видим первую половину"
        else:                                              # видим Wn → up
            b.append('<line class="s-dash" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (T(Wn) + T(A)))
            b.append('<line class="s-dash" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (T(Wn) + T((2, 0))))
            b.append(node(T(A), "s-node-r", 2.6))
            b.append(node(T((2, 0)), "s-node-r", 2.6))
            b.append('<line class="s-accent" stroke-width="3" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (T(Wn) + T(up)))
            b.append(arrow(T(Wn), T(up), "s-ar-a"))
            b.append(node(T(up), "s-node-r", 2.6))
            cx, cy = T((1.5, 0.0))
            lab = "видим вторую половину"
        b.append(node(T(Wn), "s-node", 3.0))
        for u, v in ((-1, -1), (-1, 1)):
            b.append('<line class="s-line" x1="%g" y1="%g" x2="%g" y2="%g"/>'
                     % (cx + 11 * u, cy + 11 * v, cx - 11 * u, cy - 11 * v))
        b.append(txt((ox + 140, 18), lab, "s-txt-m"))
    return svg(W, H, "\n".join(bb + b), "Слева видно звено, идущее из чёрной вершины в новую: уголок продолжится вверх или вниз, и строка голубая, значит вверх. Справа видно звено, идущее из новой вершины в чёрную: уголок начался слева или справа, и та же голубая строка выбирает слева")


def ill_tiling(n=12):
    """Плитка: то же звено, но толщиной в клетку. Два дракона смыкаются без зазора."""
    W, H = 620, 560
    base = dragon(n)
    fam = []
    for r in range(4):
        pts = base
        for _ in range(r):
            pts = [(-y, x) for x, y in pts]
        fam.append(pts)
    T, s = fitter([p for f in fam for p in f], 0, 0, W, H, pad=10)
    s = s / 2
    b = []
    for pts, cls in zip(fam, ("s-line", "s-accent", "s-line", "s-accent")):
        d = ["M %.1f,%.1f" % T(pts[0])] + ["L %.1f,%.1f" % T(p) for p in pts[1:]]
        b.append('<path class="%s" fill="none" stroke-width="%g" stroke-linecap="butt" '
                 'stroke-linejoin="miter" d="%s"/>' % (cls, s, " ".join(d)))
    return svg(W, H, "\n".join(b), "Четыре кривые из одной точки, у каждой звено нарисовано полосой шириной в полклетки. Полосы смыкаются без зазоров и без наложений — линия превратилась в заливку")


def ill_address(n=5, k=13):
    PANEL, W, H = 118, 600, 196
    b = []
    idx, bits, chain = k, [], []
    for lvl in range(n, 0, -1):
        P = dragon(lvl)
        chain.append((lvl, P, idx))
        if lvl == 1:
            break
        bit, _ = parent_edge(P[idx], P[idx + 1])
        bits.append(bit)
        idx //= 2
    for i, (lvl, P, j) in enumerate(chain):
        x = 6 + i * PANEL
        T, s = fitter(P, x, 22, PANEL - 8, 116, pad=13)
        b.append(rpath([T(p) for p in P], s * R, "s-thin", width=1.6))
        b.append('<line class="s-accent" stroke-width="3" x1="%g" y1="%g" x2="%g" y2="%g"/>'
                 % (T(P[j]) + T(P[j + 1])))
        b.append(txt((x + PANEL / 2 - 4, 15), "ранг %d" % lvl, "s-txt-m"))
        if i < len(bits):
            b.append(arrow((x + PANEL - 26, 80), (x + PANEL + 2, 80)))
            b.append(txt((x + PANEL - 12, 72), str(bits[i]), "s-txt-m"))
    b.append(txt((W / 2, 178), "%s  —  номер шага %d" % (" ".join(str(x) for x in bits), k), "s-txt-m"))
    return svg(W, H, "\n".join(b), "Имя одного звена ранга 5 собирается по цифре за складывание")


def ill_four(n=8):
    W, H = 620, 620
    base = dragon(n)
    fam, cls, wid = [], ("s-line", "s-accent", "s-thin", "s-dash"), (1.7, 1.7, 2.4, 1.9)
    for r in range(4):
        pts = base
        for _ in range(r):
            pts = [(-y, x) for x, y in pts]
        fam.append(pts)
    T, s = fitter([p for f in fam for p in f], 0, 0, W, H, pad=14)
    b = [rpath([T(p) for p in f], s * R, cls[r], prec=1, width=wid[r]) for r, f in enumerate(fam)]
    b.append(node(T((0, 0)), "s-node-a", 4.0))
    return svg(W, H, "\n".join(b), "Четыре ломаные дракона ранга 8 из одной точки, повёрнутые на 0, 90, 180 и 270 градусов. Вместе они укладываются в решётку без наложений и без пропусков")


if __name__ == "__main__":
    print("Иллюстрации лекции:")
    save("f1-strip", ill_strip())
    save("f2-halves", ill_halves(6))
    save("f3-pairs", ill_pairs(3))
    save("f4-dense", ill_dense(10))
    save("f5-nodes", ill_chess(4))
    save("f6-rows", ill_stripes(6))
    save("f7-restore", ill_restore())
    save("f9-four", ill_four(8))
    save("f10-tiling", ill_tiling(12))
    print("Готово.")
