#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Рисунки печатного мини-листка Л2. Ч/б, самодостаточный SVG (в листке нет
CSS-классов doc-движка — это отдельный печатный конвейер, FORMAT-LISTKA).
Не путать с ../razbor/gen_ill.py: там doc-вид, классы .s-*, цвет от движка.

Две фигуры:
  L2-fig-rang4.svg  — ломаная дракона ранга 4 с пронумерованными вершинами 0..16.
                      Работает на три задачи: счёт поворотов (13), «четыре подряд»
                      (14) и «каждая вторая вершина» (16). Номера даём готовыми:
                      руками нумеровать 17 вершин — лишняя возня, а не задача.
  L2-fig-treug.svg  — механика теоремы 2 на ранге 1: на каждом звене как на
                      гипотенузе равнобедренный прямоугольный треугольник,
                      соседние — по разные стороны. Показываем на самом
                      маленьком; задача (15) — проделать это на ранге 2.

Гейт: обе фигуры проверены машиной (см. /tmp/p21p34.py, ход 17.07):
теорема 2 даёт ЗАКОННОГО дракона ранга n+1 при обеих сторонах старта
(это ровно П22: «теорема 2 тоже даёт две»), Главную — при одной из них.
Чётные вершины ранга 4 дают ровно слово LLRLLRR = ранг 3; нечётные дают
3 участка, где ломаная идёт прямо, — то есть не дракона.

    python3 gen_l2_figs.py     # → L2-fig-rang4.svg, L2-fig-treug.svg
"""
from pathlib import Path

INK = "#000"


def bar(s):
    return "".join("R" if c == "L" else "L" for c in reversed(s))


def word(n):
    s = ""
    for _ in range(n):
        s = s + "L" + bar(s)
    return s


def verts(w):
    d, out = (1, 0), [(0, 0), (1, 0)]
    for c in w:
        d = (-d[1], d[0]) if c == "L" else (d[1], -d[0])
        p = out[-1]
        out.append((p[0] + d[0], p[1] + d[1]))
    return out


def bbox(pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def seg_dist(p, a, b):
    """Расстояние от точки до отрезка."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0]-a[0])*dx + (p[1]-a[1])*dy) / L2))
    qx, qy = a[0] + t*dx, a[1] + t*dy
    return ((p[0]-qx)**2 + (p[1]-qy)**2) ** 0.5


def place_labels(pts, lab, half_w, half_h):
    """Куда посадить номер каждой вершины.

    Наивное «оттолкнуться от центра фигуры» не годится: у ранга 4 вершины 7 и 11
    — ОДНА И ТА ЖЕ точка (ломаная себя касается), и обе метки садятся друг на
    друга. Поэтому перебираем 8 направлений и берём то, что дальше всего от
    самой ломаной и от уже поставленных меток.
    """
    dirs = [(0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1)]
    placed = []
    for i, p in enumerate(pts):
        best, best_score = None, -1e9
        for dx, dy in dirs:
            n = (dx*dx + dy*dy) ** 0.5
            c = (p[0] + lab*dx/n, p[1] + lab*dy/n)
            d_line = min(seg_dist(c, pts[j], pts[j+1]) for j in range(len(pts)-1))
            d_lab = min((max(abs(c[0]-q[0]) - 2*half_w, abs(c[1]-q[1]) - 2*half_h)
                         for q in placed), default=99.0)
            score = min(d_line, d_lab)
            if score > best_score:
                best, best_score = c, score
        placed.append(best)
    return placed


def fig_rang4():
    """Ранг 4, вершины пронумерованы от отмеченного конца."""
    P = verts(word(4))
    STEP, PAD, LAB = 52.0, 30.0, 16.0
    x0, y0, x1, y1 = bbox(P)
    W = (x1 - x0) * STEP + 2 * PAD
    H = (y1 - y0) * STEP + 2 * PAD
    T = lambda p: (round(PAD + (p[0] - x0) * STEP, 2),
                   round(PAD + (y1 - p[1]) * STEP, 2))
    pts = [T(p) for p in P]

    out = ['<polyline points="%s" fill="none" stroke="%s" stroke-width="2.6" '
           'stroke-linejoin="round" stroke-linecap="round"/>'
           % (" ".join("%g,%g" % p for p in pts), INK)]

    labs = place_labels(pts, LAB, 6.0, 6.0)
    for i, (p, c) in enumerate(zip(pts, labs)):
        out.append('<circle cx="%g" cy="%g" r="2.8" fill="%s"/>' % (p[0], p[1], INK))
        out.append('<text x="%g" y="%g" text-anchor="middle" '
                   'fill="%s" font-family="Georgia, serif" font-size="13">%d</text>'
                   % (round(c[0], 2), round(c[1], 2) + 4.5, INK, i))
    # отмеченный конец — жирная точка, как на листке Л1
    out.append('<circle cx="%g" cy="%g" r="4.8" fill="%s"/>' % (pts[0][0], pts[0][1], INK))

    return svg(W, H, out,
               "Ломаная дракона ранга 4 из шестнадцати звеньев; "
               "её семнадцать вершин пронумерованы от нуля до шестнадцати, "
               "начиная с отмеченного конца", labs + pts)


def fig_treug():
    """Теорема 2, механика: треугольники на звеньях ранга 1.

    ⚠ Рамку считаем по ЛОМАНОЙ И ВЕРШИНАМ ТРЕУГОЛЬНИКОВ. По одной ломаной —
    нижний треугольник вылезал за viewBox и обрезался (поймано гейтом-PNG).
    """
    P = verts(word(1))                       # уголок: 2 звена
    STEP, PAD = 74.0, 26.0
    x0, y0, x1, y1 = bbox(P)
    raw = lambda p: ((p[0] - x0) * STEP, (y1 - p[1]) * STEP)
    pts0 = [raw(p) for p in P]

    tri = []                                 # (a, apex, b) в сырых координатах
    for i in range(len(pts0) - 1):
        a, b = pts0[i], pts0[i + 1]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        dx, dy = b[0] - a[0], b[1] - a[1]
        sgn = 1 if i % 2 == 0 else -1        # соседние — по разные стороны
        tri.append((a, (mx - sgn * dy / 2, my + sgn * dx / 2), b))

    every = pts0 + [t[1] for t in tri]
    ax0, ay0, ax1, ay1 = bbox(every)
    W, H = (ax1 - ax0) + 2 * PAD, (ay1 - ay0) + 2 * PAD
    S = lambda p: (round(p[0] - ax0 + PAD, 2), round(p[1] - ay0 + PAD, 2))
    pts = [S(p) for p in pts0]

    out = []
    for a, apex, b in tri:                   # катеты — тонким пунктиром
        A, X, B = S(a), S(apex), S(b)
        out.append('<polyline points="%g,%g %g,%g %g,%g" fill="none" stroke="%s" '
                   'stroke-width="1.8" stroke-dasharray="5 3" stroke-linejoin="round"/>'
                   % (A[0], A[1], X[0], X[1], B[0], B[1], INK))
        out.append('<circle cx="%g" cy="%g" r="3" fill="#fff" stroke="%s" '
                   'stroke-width="1.5"/>' % (X[0], X[1], INK))
    # исходная ломаная — жирным, поверх
    out.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.8" '
               'stroke-linejoin="round" stroke-linecap="round"/>'
               % (" ".join("%g,%g" % p for p in pts), INK))
    out.append('<circle cx="%g" cy="%g" r="4.4" fill="%s"/>' % (pts[0][0], pts[0][1], INK))

    return svg(W, H, out,
               "На каждом звене ломаной как на гипотенузе построен равнобедренный "
               "прямоугольный треугольник, показанный пунктиром; "
               "на соседних звеньях треугольники смотрят в разные стороны",
               pts + [S(t[1]) for t in tri])


def svg(W, H, body, alt, inside=()):
    """inside — точки, которые ОБЯЗАНЫ лежать внутри рамки. Гейт посадки:
    молча обрезанная фигура выглядит как задумка, поэтому проверяем машиной."""
    for p in inside:
        assert -1 <= p[0] <= W + 1 and -1 <= p[1] <= H + 1, \
            "точка %s вне рамки %gx%g — фигура обрежется" % (p, W, H)
    return ('<svg viewBox="0 0 %g %g" xmlns="http://www.w3.org/2000/svg" role="img" '
            'aria-label="%s">\n%s\n</svg>' % (round(W, 2), round(H, 2), alt, "\n".join(body)))


def gate_labels():
    """Номера не налезают ни на ломаную, ни друг на друга.

    Повод: вершины 7 и 11 ранга 4 — одна точка (ломаная себя касается), и обе
    метки печатались одна поверх другой. Глазами на PNG это выглядит как клякса
    «17»; машиной — считается.
    """
    P = verts(word(4))
    STEP, PAD, LAB = 52.0, 30.0, 16.0
    x0, y0, x1, y1 = bbox(P)
    T = lambda p: (PAD + (p[0]-x0)*STEP, PAD + (y1-p[1])*STEP)
    pts = [T(p) for p in P]
    labs = place_labels(pts, LAB, 6.0, 6.0)

    d_line = min(min(seg_dist(c, pts[j], pts[j+1]) for j in range(len(pts)-1)) for c in labs)
    pairs = [(i, j, max(abs(labs[i][0]-labs[j][0]), abs(labs[i][1]-labs[j][1])))
             for i in range(len(labs)) for j in range(i+1, len(labs))]
    i, j, d_lab = min(pairs, key=lambda t: t[2])

    print("  гейт меток: до ломаной ≥ %.1f (нужно > 6) · ближайшая пара номеров "
          "%d и %d, зазор %.1f (нужно > 13)" % (d_line, i, j, d_lab))
    assert d_line > 6, "номер сидит на ломаной"
    assert d_lab > 13, "номера %d и %d налезают друг на друга" % (i, j)


if __name__ == "__main__":
    here = Path(__file__).parent
    for name, fn in (("L2-fig-rang4.svg", fig_rang4), ("L2-fig-treug.svg", fig_treug)):
        p = here / name
        p.write_text(fn(), encoding="utf-8")
        print("→ %s (%d симв.)" % (p.name, len(p.read_text(encoding="utf-8"))))
    gate_labels()
    print("  гейт посадки: обе фигуры целиком внутри рамки")
