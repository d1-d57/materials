#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генератор иллюстраций разбора «Кривая дракона» → SVG-фрагменты для doc-вида.

Источник → генератор → самодостаточный HTML (design-mode). Геометрия дракона
считается, а не рисуется руками: правка = правка параметра, не 92 фигуры.

Примитивы — по `_studio/konvejer/09-illustracii/SLOVAR-primitivov.md`:
  #4 путь-ломаная <polyline> .s-line/.s-accent · #1 узел <circle r=3.4> .s-node/.s-node-r
  #2 отрезок .s-line/.s-thin · #8 ось пунктиром .s-thin · #10 стрелка · #11 метка .s-txt
Правило: внутри рисунка только МЕТКА; проза — в figcaption (пишется в *.md).
Цвет — только классом. id не используем (нет defs/marker) → конфликта имён нет.

    python3 gen_ill.py            # → ill/*.svg  (вставляются в *.md инлайном)
"""
from pathlib import Path

OUT = Path(__file__).parent / "ill"

# ───────────────────────── геометрия дракона ─────────────────────────
def bar(s):
    return "".join("R" if c == "L" else "L" for c in reversed(s))

def word(n, choices=None):
    """Слово ранга n. По умолчанию — Главная ломаная (всегда в одну сторону)."""
    ch = choices or ["L"] * n
    s = ""
    for x in ch[:n]:
        s = s + x + bar(s)
    return s

def poly(w, start=(0, 0), d=(1, 0)):
    """Вершины ломаной по слову. Целые координаты — сетка."""
    x, y = start
    dx, dy = d
    pts = [(x, y), (x + dx, y + dy)]
    x, y = x + dx, y + dy
    for c in w:
        dx, dy = (-dy, dx) if c == "L" else (dy, -dx)
        x, y = x + dx, y + dy
        pts.append((x, y))
    return pts

def rot(pts, k):
    for _ in range(k % 4):
        pts = [(-y, x) for x, y in pts]
    return pts

def bbox(pts):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)

def fit(pts, w, h, pad=18, flip_y=True):
    """Целочисленные вершины → экранные координаты с полями (словарь: поля >= 18px)."""
    x0, y0, x1, y1 = bbox(pts)
    sx = (w - 2 * pad) / max(x1 - x0, 1)
    sy = (h - 2 * pad) / max(y1 - y0, 1)
    s = min(sx, sy)
    ox = pad + ((w - 2 * pad) - s * (x1 - x0)) / 2
    oy = pad + ((h - 2 * pad) - s * (y1 - y0)) / 2
    def T(p):
        X = ox + (p[0] - x0) * s
        Y = (h - oy - (p[1] - y0) * s) if flip_y else (oy + (p[1] - y0) * s)
        return (round(X, 2), round(Y, 2))
    return [T(p) for p in pts], s

def pl(pts, cls="s-line"):
    return '<polyline class="%s" points="%s"/>' % (
        cls, " ".join("%g,%g" % p for p in pts))

def node(p, cls="s-node"):
    return '<circle class="%s" cx="%g" cy="%g" r="3.4"/>' % (cls, p[0], p[1])

def txt(p, s, cls="s-txt", anchor="middle"):
    return '<text class="%s" x="%g" y="%g" text-anchor="%s">%s</text>' % (
        cls, p[0], p[1], anchor, s)

def arrow(p, q, cls="s-ar-m"):
    """Примитив #10: линия + треугольная голова.

    Голова считается ЯВНЫМИ координатами, без transform/rotate: растеризаторы
    (и наш гейт, и часть просмотрщиков) кладут повёрнутый path мимо места —
    прецедент словаря «cairosvg соврёт». Явные точки едут везде одинаково.
    """
    import math
    ang = math.atan2(q[1] - p[1], q[0] - p[0])
    ln = math.hypot(q[0] - p[0], q[1] - p[1])
    if ln < 1:
        return ""
    ux, uy = (q[0] - p[0]) / ln, (q[1] - p[1]) / ln     # вдоль
    nx, ny = -uy, ux                                     # поперёк
    base = (q[0] - 9 * ux, q[1] - 9 * uy)
    a = (base[0] + 4 * nx, base[1] + 4 * ny)
    b = (base[0] - 4 * nx, base[1] - 4 * ny)
    head = '<polygon class="%s" points="%g,%g %g,%g %g,%g"/>' % (
        cls, q[0], q[1], a[0], a[1], b[0], b[1])
    return ('<line class="s-thin" x1="%g" y1="%g" x2="%g" y2="%g"/>%s'
            % (p[0], p[1], base[0], base[1], head))

def svg(w, h, body, label):
    return ('<svg viewBox="0 0 %d %d" width="%d" role="img" aria-label="%s">\n%s\n</svg>'
            % (w, h, w, label, body))

def save(name, s):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / (name + ".svg")).write_text(s, encoding="utf-8")
    print("  ill/%s.svg  (%d симв.)" % (name, len(s)))


# ───────────────────────── 1. полоска → сгибы → ломаная ─────────────────────────
def ill_strip_to_poly():
    """Три ряда: одна и та же полоска, сложенная 1, 2, 3 раза.

    Полоска одной длины во всех рядах (это ОДНА полоска — клетки дробятся);
    ломаная справа вписана в бокс фиксированного размера.
    """
    W, H = 600, 330
    ROW, SL = 106, 240                       # высота ряда, длина полоски
    b = []
    for k, n in enumerate((1, 2, 3)):
        ytop = 34 + k * ROW
        cells = 2 ** n
        cw = SL / cells
        x0 = 44
        b.append('<rect class="s-line s-fillsh" x="%g" y="%g" width="%g" height="18"/>'
                 % (x0, ytop, SL))
        w = word(n)
        for i, c in enumerate(w):
            xc = x0 + cw * (i + 1)
            if c == "L":                     # долина: засечка ВВЕРХ, акцентом
                b.append('<line class="s-accent" x1="%g" y1="%g" x2="%g" y2="%g"/>'
                         % (xc, ytop - 8, xc, ytop + 18))
            else:                            # гора: засечка ВНИЗ
                b.append('<line class="s-line" x1="%g" y1="%g" x2="%g" y2="%g"/>'
                         % (xc, ytop, xc, ytop + 26))
        b.append(txt((x0 - 10, ytop + 13), "n=%d" % n, "s-txt-m", "end"))
        b.append(arrow((x0 + SL + 18, ytop + 9), (x0 + SL + 60, ytop + 9)))
        # ломаная: бокс фиксированного размера, привязан к тому же ряду
        P = poly(w)
        pts, _ = fit(P, 150, 84, pad=8)
        pts = [(x + x0 + SL + 66, y + ytop - 34) for x, y in pts]
        b.append(pl(pts))
        b.append(node(pts[0], "s-node"))
        b.append(node(pts[-1], "s-node"))
        b.append(node(pts[len(pts) // 2], "s-node-r"))    # средняя вершина
    return svg(W, H, "\n".join(b),
               "Одна и та же полоска, сложенная 1, 2 и 3 раза. Слева засечки сгибов: вверх — один тип, вниз — другой. Справа — вид сверху: ломаные дракона рангов 1, 2, 3; залитая точка — средняя вершина")


# ───────────────────────── 2. слово написано на полоске ─────────────────────────
def ill_word_on_strip():
    """Ядро курса: сгиб №k на полоске = поворот №k на ломаной.

    Соответствие несёт ГРАФИКА (цвет сгиба = цвет вершины) + номер как метка.
    Буквы у каждой вершины не пишем: 14 подписей — это шум (правило словаря).
    """
    W, H = 600, 300
    b = []
    n = 3
    w = word(n)
    cw, x0, ytop = 54, 96, 44
    b.append('<rect class="s-line s-fillsh" x="%g" y="%g" width="%g" height="20"/>'
             % (x0, ytop, cw * 2 ** n))
    for i, c in enumerate(w):
        xc = x0 + cw * (i + 1)
        if c == "L":
            b.append('<line class="s-accent" x1="%g" y1="%g" x2="%g" y2="%g"/>'
                     % (xc, ytop - 10, xc, ytop + 20))
        else:
            b.append('<line class="s-line" x1="%g" y1="%g" x2="%g" y2="%g"/>'
                     % (xc, ytop, xc, ytop + 30))
        b.append(txt((xc, ytop + 47), str(i + 1), "s-txt-m"))
    b.append(txt((x0 - 12, ytop + 14), "полоска", "s-txt-m", "end"))

    P = poly(w)
    pts, _ = fit(P, 300, 150, pad=10)
    pts = [(x + 150, y + 130) for x, y in pts]
    b.append(pl(pts))
    b.append(node(pts[0], "s-node"))
    b.append(node(pts[-1], "s-node"))
    for i, c in enumerate(w):
        p = pts[i + 1]
        # тот же цвет, что у засечки: акцент ↔ акцент. Раньше вершина L была тёмной,
        # а засечка L — акцентной, и пара глазом не читалась (поймано на рендере).
        b.append(node(p, "s-node-a" if c == "L" else "s-node"))
        b.append(txt((p[0] + 11, p[1] - 8), str(i + 1), "s-txt-m"))
    b.append(txt((150 - 12, 130 + 84), "ломаная", "s-txt-m", "end"))
    return svg(W, H, "\n".join(b),
               "Сгиб номер k на полоске и поворот номер k на ломаной — это одно и то же. Вершина покрашена в цвет своей засечки")


# ───────────────────────── 3. теорема 1 ─────────────────────────
def ill_theorem1():
    """Ранг 4 = две ломаные ранга 3 под 90° вокруг средней вершины O.

    Правая половина прошлой версии (те же две ломаные по отдельности) выпилена:
    она ничего не добавляла к левой — правило словаря «декоративный рисунок = дефект».
    """
    W, H = 420, 300
    b = []
    P = poly(word(4))
    pts, _ = fit(P, W, H, pad=26)
    half = len(pts) // 2
    b.append(pl(pts[:half + 1], "s-line"))
    b.append(pl(pts[half:], "s-accent"))
    b.append(node(pts[0], "s-node"))
    b.append(node(pts[-1], "s-node"))
    b.append(node(pts[half], "s-node-r"))
    b.append(txt((pts[half][0] + 13, pts[half][1] - 9), "O", "s-txt"))
    return svg(W, H, "\n".join(b),
               "Ломаная дракона ранга 4: две её половины — ломаные ранга 3, переходящие друг в друга поворотом на 90 градусов вокруг средней вершины O")


# ───────────────────────── 4. теорема 2 (удвоение) ─────────────────────────
def ill_theorem2():
    """Удвоение. Слева ранг 2 с треугольниками на звеньях, справа — их катеты = ранг 3.

    Вершины треугольников входят в bbox для fit: иначе фигура вылезала за viewBox
    и низ срезался (поймано глазами на рендере).
    """
    W, H = 600, 250
    b = []
    P = poly(word(2))
    apex = []                                # вершины треугольников — в целых, до масштаба
    for i in range(len(P) - 1):
        a, c = P[i], P[i + 1]
        mx, my = (a[0] + c[0]) / 2, (a[1] + c[1]) / 2
        dx, dy = c[0] - a[0], c[1] - a[1]
        sgn = 1 if i % 2 == 0 else -1
        apex.append((mx - sgn * dy / 2, my + sgn * dx / 2))
    box, _ = fit(P + apex, 260, 210, pad=20)
    pts, ap = box[:len(P)], box[len(P):]
    b.append(pl(pts, "s-line"))
    for p in pts:
        b.append(node(p))
    for i in range(len(pts) - 1):
        b.append(pl([pts[i], ap[i], pts[i + 1]], "s-accent"))
        b.append(node(ap[i], "s-node-a"))     # цвет вершины = цвет катетов
    b.append(arrow((296, 125), (344, 125)))
    q, _ = fit(poly(word(3)), 230, 210, pad=20)
    q = [(x + 360, y) for x, y in q]
    b.append(pl(q, "s-accent"))
    return svg(W, H, "\n".join(b),
               "На каждом звене ломаной ранга 2 как на гипотенузе построен равнобедренный прямоугольный треугольник. Катеты этих треугольников образуют ломаную ранга 3")


# ───────────────────────── 5. большой дракон + спираль концов ─────────────────────────
def ill_big_dragon(n=12):
    W, H = 640, 420
    b = []
    P = poly(word(n))
    pts, _ = fit(P, 620, 400)
    b.append(pl(pts, "s-line"))
    return svg(W, H, "\n".join(b),
               "Ломаная дракона ранга %d — 4096 звеньев, нарисована по правилу, без бумаги" % n)


def ill_spiral():
    """Концы Главной ломаной рангов 1..9 = (1+i)^n — спираль; ранг 9 сонаправлен рангу 1.

    Пунктирный луч O→1→9 (примитив #9) показывает сонаправленность графикой:
    раньше это было только в подписи, и на картинке не читалось.
    """
    W, H = 460, 400
    b = []
    ends, z = [(0, 0)], (1, 1)               # z = (1+i)^1 — конец ранга 1
    for _ in range(9):
        ends.append(z)
        z = (z[0] - z[1], z[0] + z[1])
    pts, _ = fit(ends, W, H, pad=24)
    o = pts[0]
    far = pts[-1]                            # ранг 9 — сонаправлен рангу 1
    b.append('<line class="s-dash" x1="%g" y1="%g" x2="%g" y2="%g"/>'
             % (o[0], o[1], far[0], far[1]))
    b.append(pl(pts[1:], "s-thin"))
    for i, p in enumerate(pts[1:], start=1):
        b.append(node(p, "s-node-r"))
        if i in (1, 2, 3, 8, 9):
            b.append(txt((p[0] + 12, p[1] - 8), str(i), "s-txt-m"))
    b.append(node(o, "s-node"))
    b.append(txt((o[0] - 13, o[1] + 5), "O", "s-txt", "end"))
    return svg(W, H, "\n".join(b),
               "Концы Главной ломаной рангов 1-9, выпущенных из точки O. Пунктирный луч показывает: ранг 9 смотрит туда же, куда ранг 1 — за 8 рангов полный оборот")


# ───────────────────────── 6. четыре дракона из одной точки ─────────────────────────
def ill_four_dragons(n=8):
    W, H = 560, 560
    b = []
    base = poly(word(n))
    allp = []
    fam = [rot(base, k) for k in range(4)]
    for f in fam:
        allp += f
    _, s = fit(allp, 540, 540)
    x0, y0, x1, y1 = bbox(allp)
    def T(p, pad=10):
        return (round(pad + (p[0] - x0) * s, 2), round(H - pad - (p[1] - y0) * s, 2))
    for k, f in enumerate(fam):
        b.append(pl([T(p) for p in f], "s-line" if k % 2 == 0 else "s-accent"))
    b.append(node(T((0, 0)), "s-node-r"))
    return svg(W, H, "\n".join(b),
               "Четыре ломаные дракона ранга %d, выпущенные из одной точки под углами 0, 90, 180, 270 градусов" % n)


# ───────────────────────── 7. правило вставки ─────────────────────────
def ill_insert():
    W, H = 620, 200
    b = []
    w4, w5 = word(4), word(5)
    cw = 36
    x0 = 60
    # ранг 5 — все буквы; чётные места подсвечены (это ранг 4)
    for i, c in enumerate(w5):
        x = x0 + i * (cw / 2.1)
        even = (i % 2 == 1)
        b.append(txt((x, 70), c, "s-txt" if even else "s-txt-m"))
        if even:
            b.append('<line class="s-accent" x1="%g" y1="78" x2="%g" y2="86"/>' % (x, x))
        else:
            b.append('<line class="s-thin" x1="%g" y1="46" x2="%g" y2="54"/>' % (x, x))
    b.append(txt((x0 - 16, 70), "ранг 5", "s-txt-m", "end"))
    # снизу — ранг 4 отдельно
    for i, c in enumerate(w4):
        x = x0 + (2 * i + 1) * (cw / 2.1)
        b.append(txt((x, 130), c, "s-txt"))
    b.append(txt((x0 - 16, 130), "ранг 4", "s-txt-m", "end"))
    for i in range(len(w4)):
        x = x0 + (2 * i + 1) * (cw / 2.1)
        b.append('<line class="s-dash" x1="%g" y1="88" x2="%g" y2="118"/>' % (x, x))
    # (подпись «L R L R …» убрана: читалась как случайный артефакт — это в figcaption)
    return svg(W, H, "\n".join(b),
               "Слово ранга 5: на чётных местах стоит всё слово ранга 4, на нечётных — чередующиеся L R L R")


# ───────────────────────── Л1, преподавателю ─────────────────────────
def ill_l1_halves():
    """Задача 3: раскрашенные половинки. Правило видно глазами, до всякой теории."""
    W, H = 460, 330
    b = []
    P = poly(word(5))
    pts, _ = fit(P, W, H, pad=26)
    half = len(pts) // 2
    b.append(pl(pts[:half + 1], "s-accent"))      # цветная половина полоски
    b.append(pl(pts[half:], "s-line"))            # белая половина
    b.append(node(pts[0], "s-node"))
    b.append(node(pts[-1], "s-node"))
    b.append(node(pts[half], "s-node-r"))
    b.append(txt((pts[half][0] + 13, pts[half][1] - 9), "O", "s-txt"))
    return svg(W, H, "\n".join(b),
               "Ломаная ранга 5 из полоски, у которой одна половина раскрашена: цветная и белая части — две одинаковые ломаные ранга 4, сходящиеся в точке O под прямым углом")


def ill_l1_four_rank4():
    """Задача 8: все четыре неподобные ломаные ранга 4 (представители посчитаны перебором)."""
    reps = ["LLRLLRRLLLRRLRR", "LLRRLRRLLLRLLRR", "LRRLLLRLLRRRLLR", "LRRRLLRLLRRLLLR"]
    CW, CH = 150, 150
    W, H = CW * 4, CH + 22
    b = []
    for i, w in enumerate(reps):
        pts, _ = fit(poly(w), CW, CH, pad=16)
        pts = [(x + i * CW, y) for x, y in pts]
        b.append(pl(pts))
        b.append(node(pts[0], "s-node-r"))
        b.append(txt((i * CW + CW / 2, CH + 16), "абвг"[i], "s-txt-m"))
    return svg(W, H, "\n".join(b),
               "Четыре ломаные дракона ранга 4, не подобные друг другу. Залитая точка — начало полоски")


def ill_l1_touch():
    """Задача 9: касания. У Главной ранга 5 их ровно 4, тройных нет, рёбра не повторяются."""
    W, H = 420, 330
    b = []
    P = poly(word(5))
    pts, _ = fit(P, W, H, pad=26)
    from collections import Counter
    c = Counter(pts)
    b.append(pl(pts))
    for p, k in c.items():
        if k > 1:
            b.append('<circle class="s-dash" cx="%g" cy="%g" r="9"/>' % p)
            b.append(node(p, "s-node-a"))
    b.append(node(pts[0], "s-node"))
    b.append(node(pts[-1], "s-node"))
    return svg(W, H, "\n".join(b),
               "Ломаная дракона ранга 5: обведены все четыре точки, в которые она попадает дважды. Себя она нигде не пересекает")


if __name__ == "__main__":
    print("Генерирую иллюстрации разбора:")
    save("strip-to-poly", ill_strip_to_poly())
    save("word-on-strip", ill_word_on_strip())
    save("theorem1", ill_theorem1())
    save("theorem2", ill_theorem2())
    save("insert", ill_insert())
    save("big-dragon", ill_big_dragon(12))
    save("spiral", ill_spiral())
    save("four-dragons", ill_four_dragons(8))
    save("l1-halves", ill_l1_halves())
    save("l1-four-rank4", ill_l1_four_rank4())
    save("l1-touch", ill_l1_touch())
    print("Готово. SVG инлайнятся в *.md (doc-движок пропускает <svg> верхним уровнем дословно).")
