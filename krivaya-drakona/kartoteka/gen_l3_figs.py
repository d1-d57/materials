#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Рисунок печатного мини-листка Л3. Ч/б, самодостаточный SVG (в листке нет
CSS-классов doc-движка — отдельный печатный конвейер, FORMAT-LISTKA).
Не путать с ../razbor/gen_ill.py: там doc-вид (классы .s-*, цвет от движка,
{{ILL:word-on-strip}}). Здесь ч/б для печати, по образцу gen_l2_figs.py.

Одна фигура:
  L3-fig-word-strip.svg — слово на полоске (задача 17 / П12, ядро курса).
      Сверху — полоска со сгибами: ДОЛИНА = засечка вверх, ГОРА = вниз
      (та же ориентация, что в doc-виде ill_word_on_strip). Снизу — та же
      ломаная ранга 3; вершины пронумерованы 1..7 в том же порядке, что сгибы.
      Тип поворота (налево/направо) НЕ вскрываем: ребёнок читает его сам и
      сопоставляет с типом сгиба — в этом и есть задача. Сгиб №k и поворот
      №k стоят под одним номером — это одно и то же место.

Гейт (в gen_l2_figs.py их два, метод важнее файла):
  посадка — все нарисованные точки внутри рамки (молча обрезанная фигура
            выглядит как задумка; svg() падает ассертом);
  метки   — номера вершин не налезают на ломаную и друг на друга.

    python3 gen_l3_figs.py     # → L3-fig-word-strip.svg
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
    """Куда посадить номер каждой вершины: перебираем 8 направлений и берём
    то, что дальше всего от ломаной и от уже поставленных меток (у ранга 3
    самокасаний нет, но метод тот же, что у Л2 — чтобы номера не липли)."""
    dirs = [(0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1)]
    placed = []
    for p in pts:
        best, best_score = None, -1e9
        for dx, dy in dirs:
            nrm = (dx*dx + dy*dy) ** 0.5
            c = (p[0] + lab*dx/nrm, p[1] + lab*dy/nrm)
            d_line = min(seg_dist(c, pts[j], pts[j+1]) for j in range(len(pts)-1))
            d_lab = min((max(abs(c[0]-q[0]) - 2*half_w, abs(c[1]-q[1]) - 2*half_h)
                         for q in placed), default=99.0)
            score = min(d_line, d_lab)
            if score > best_score:
                best, best_score = c, score
        placed.append(best)
    return placed


def txt(x, y, s, size=12, anchor="middle", italic=False):
    st = ' font-style="italic"' if italic else ""
    return ('<text x="%g" y="%g" text-anchor="%s" fill="%s" '
            'font-family="Georgia, serif" font-size="%g"%s>%s</text>'
            % (round(x, 2), round(y, 2), anchor, INK, size, st, s))


def fig_word_strip():
    n = 3
    w = word(n)                              # LLRLLRR
    CW, SH, PAD, LX = 46.0, 20.0, 22.0, 62.0
    UP, DN = 11.0, 12.0                      # вылет засечки вверх / вниз
    x0 = PAD + LX
    ytop = PAD + UP                          # запас на засечку вверх
    strip_w = CW * 2 ** n
    num_y = ytop + SH + DN + 15              # номера сгибов под полоской

    inside = [(x0, ytop - UP), (x0 + strip_w, ytop + SH + DN)]
    b = ['<rect x="%g" y="%g" width="%g" height="%g" fill="none" stroke="%s" '
         'stroke-width="1.8"/>' % (x0, ytop, strip_w, SH, INK)]
    for i, c in enumerate(w):
        xc = x0 + CW * (i + 1)
        y1, y2 = (ytop - UP, ytop + SH) if c == "L" else (ytop, ytop + SH + DN)
        b.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.8"/>'
                 % (xc, y1, xc, y2, INK))
        b.append(txt(xc, num_y, str(i + 1)))
        inside += [(xc, num_y + 4)]
    b.append(txt(PAD, ytop + SH / 2 + 4, "полоска", 12.5, "start", italic=True))

    P = verts(w)
    STEP = 40.0
    bx0, by0, bx1, by1 = bbox(P)
    px = x0                                  # ломаную выравниваем под левый край полоски
    poly_top = num_y + 26
    T = lambda p: (round(px + (p[0] - bx0) * STEP, 2),
                   round(poly_top + (by1 - p[1]) * STEP, 2))
    pts = [T(p) for p in P]
    b.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.4" '
             'stroke-linejoin="round" stroke-linecap="round"/>'
             % (" ".join("%g,%g" % p for p in pts), INK))
    labs = place_labels(pts, 15.0, 6.0, 6.0)
    for i in range(1, len(pts) - 1):         # повороты 1..7; pts[0] и pts[-1] — концы, без номера
        b.append('<circle cx="%g" cy="%g" r="2.6" fill="%s"/>' % (pts[i][0], pts[i][1], INK))
        b.append(txt(labs[i][0], labs[i][1] + 4, str(i)))
    b.append('<circle cx="%g" cy="%g" r="4.4" fill="%s"/>'    # отмеченный конец
             % (pts[0][0], pts[0][1], INK))
    b.append(txt(PAD, poly_top + 6, "ломаная", 12.5, "start", italic=True))   # у верха ряда, чтобы не липнуть к номеру вершины 7

    inside += pts + labs[1:-1]
    W = max(p[0] for p in inside) + PAD
    H = max(p[1] for p in inside) + PAD
    return svg(W, H, b,
               "Сверху — полоска дракона ранга три со сгибами: засечка вверх — "
               "долина, вниз — гора, всего семь сгибов, пронумерованы слева "
               "направо. Снизу — та же ломаная дракона ранга три; её семь "
               "поворотов пронумерованы в том же порядке. Сгиб номер k и "
               "поворот номер k — одно и то же место", inside)


def svg(W, H, body, alt, inside=()):
    """inside — точки, ОБЯЗАННЫЕ лежать внутри рамки. Гейт посадки: молча
    обрезанная фигура выглядит как задумка, поэтому проверяем машиной."""
    for p in inside:
        assert -1 <= p[0] <= W + 1 and -1 <= p[1] <= H + 1, \
            "точка %s вне рамки %gx%g — фигура обрежется" % (p, W, H)
    return ('<svg viewBox="0 0 %g %g" xmlns="http://www.w3.org/2000/svg" role="img" '
            'aria-label="%s">\n%s\n</svg>' % (round(W, 2), round(H, 2), alt, "\n".join(body)))


def gate_labels():
    """Номера поворотов не сидят на ломаной и не налезают друг на друга."""
    P = verts(word(3))
    CW, SH, PAD, LX, UP, DN = 46.0, 20.0, 22.0, 62.0, 11.0, 12.0
    x0 = PAD + LX
    ytop = PAD + UP
    strip_w = CW * 2 ** 3
    num_y = ytop + SH + DN + 15
    bx0, by0, bx1, by1 = bbox(P)
    px = x0
    poly_top = num_y + 26
    T = lambda p: (px + (p[0] - bx0) * 40.0, poly_top + (by1 - p[1]) * 40.0)
    pts = [T(p) for p in P]
    labs = place_labels(pts, 15.0, 6.0, 6.0)[1:-1]   # только номера поворотов 1..7
    d_line = min(min(seg_dist(c, pts[j], pts[j+1]) for j in range(len(pts)-1)) for c in labs)
    pairs = [(i, j, max(abs(labs[i][0]-labs[j][0]), abs(labs[i][1]-labs[j][1])))
             for i in range(len(labs)) for j in range(i+1, len(labs))]
    i, j, d_lab = min(pairs, key=lambda t: t[2])
    print("  гейт меток: до ломаной ≥ %.1f (нужно > 6) · ближайшая пара номеров "
          "%d и %d, зазор %.1f (нужно > 13)" % (d_line, i + 1, j + 1, d_lab))
    assert d_line > 6, "номер сидит на ломаной"
    assert d_lab > 13, "номера %d и %d налезают друг на друга" % (i + 1, j + 1)


if __name__ == "__main__":
    here = Path(__file__).parent
    p = here / "L3-fig-word-strip.svg"
    p.write_text(fig_word_strip(), encoding="utf-8")
    print("→ %s (%d симв.)" % (p.name, len(p.read_text(encoding="utf-8"))))
    gate_labels()
    print("  гейт посадки: фигура целиком внутри рамки")
