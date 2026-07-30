#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ГЕНЕРАТОР РИСУНКОВ ЛЕКЦИИ — один общий, как требует заход §1а.1.

  python3 src/tools/gen_ill.py            # перегенерировать ВСЕ рисунки в illustrations/
  python3 src/tools/gen_ill.py --list     # какие рисунки он делает и куда кладёт
  python3 src/tools/gen_ill.py cliff-walk domiki   # только названные

Смысл: «сделать треугольник до 10-й строки вместо 7-й» должно быть правкой ОДНОГО
ЧИСЛА, а не перерисовкой файла. Прошлый заход рисовал по точке руками, и каждая
правка владельца стоила полной перерисовки.

Контракт рисунка (СПЕКА-risunkov + SLOVAR-primitivov):
  · цвет ТОЛЬКО классом .s-*; ни hex, ни stroke="black", ни style=
  · внутри рисунка живёт только МЕТКА (число, координата, одна буква) — ни одного слова
  · viewBox обязателен; для дека — preserveAspectRatio и БЕЗ атрибута width
  · никаких id/marker/defs/clipPath: несколько SVG в одном документе делят
    пространство имён и тихо ломают друг друга
  · стрелка — это ЗАЛИВКА наконечника (path l9,4 -9,4 z), а не обводка

Соглашение лекции: орёл = шаг ВВЕРХ, решка = шаг ВНИЗ (РАЗБОР §17.3).
Слово из О и Р задаётся строкой "ОРРОР" или "+--+-" — понимаются обе записи.
"""
import sys
from math import comb
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "illustrations"

DX, DY = 34, 26        # шаг сетки (SLOVAR: x 30–36, y 22–26)
R = 3.4                # радиус узла
PAD = 18               # поля от края viewBox


# ───────────────────────────── примитивы словаря ─────────────────────────────
def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def norm(word):
    """'ОРРО' | '+--+' → '+--+'. Орёл — вверх, решка — вниз."""
    m = {"О": "+", "O": "+", "о": "+", "Р": "-", "P": "-", "р": "-", "+": "+", "-": "-"}
    return "".join(m[c] for c in str(word) if c in m)


def letters(word):
    return norm(word).replace("+", "О").replace("-", "Р")


def line(x1, y1, x2, y2, cls="s-line", dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return '<line class="%s" x1="%g" y1="%g" x2="%g" y2="%g"%s/>' % (cls, x1, y1, x2, y2, d)


def poly(points, cls="s-line"):
    pts = " ".join("%g,%g" % p for p in points)
    return '<polyline class="%s" points="%s"/>' % (cls, pts)


def node(x, y, cls="s-node", r=R):
    return '<circle class="%s" cx="%g" cy="%g" r="%g"/>' % (cls, x, y, r)


def rect(x, y, w, h, cls="s-line"):
    return '<rect class="%s" x="%g" y="%g" width="%g" height="%g"/>' % (cls, x, y, w, h)


def txt(x, y, s, cls="s-txt", anchor="middle"):
    return '<text class="%s" x="%g" y="%g" text-anchor="%s">%s</text>' % (
        cls, x, y, anchor, esc(s))


def arrow(x1, y1, x2, y2, cls="s-ar-m"):
    """Стрелка: тонкое древко + ЗАЛИТЫЙ наконечник (SLOVAR §10, ловушка «полый треугольник»)."""
    dx, dy = x2 - x1, y2 - y1
    ln = (dx * dx + dy * dy) ** 0.5 or 1
    ux, uy = dx / ln, dy / ln
    bx, by = x2 - 9 * ux, y2 - 9 * uy          # основание наконечника
    px, py = -uy, ux                            # нормаль
    thin = "s-thin"
    head = '<path class="%s" d="M %g,%g L %g,%g L %g,%g Z"/>' % (
        cls, x2, y2, bx + 4 * px, by + 4 * py, bx - 4 * px, by - 4 * py)
    return line(x1, y1, bx, by, thin) + head


def svg(w, h, body, label, width=None):
    """Для дека — без атрибута width (иначе SVG уедет за панель); width только для doc-вида."""
    wattr = ' width="%d"' % width if width else ""
    return ('<svg viewBox="0 0 %g %g"%s preserveAspectRatio="xMidYMid meet" '
            'role="img" aria-label="%s">\n%s\n</svg>\n'
            % (w, h, wattr, esc(label), "\n".join(body)))


# ───────────────────────────── ломаная (путь Дика) ─────────────────────────────
def num(v):
    """Метка числа с ТИПОГРАФСКИМ минусом: '−1', а не '-1'. Иначе рисунки разъезжаются
    по знаку — половина через дефис, половина через минус."""
    return str(v).replace("-", "−")


def walk_geom(word, x0, y0, dx=DX, dy=DY, h0=0):
    """Точки ломаной по слову; h0 — высота СТАРТА (нужна отражению: отражённый
    кусок стартует не с нуля, а с −2). Возвращает len(word)+1 точек."""
    w = norm(word)
    pts, h = [(x0, y0 - h0 * dy)], h0
    for i, c in enumerate(w):
        h += 1 if c == "+" else -1
        pts.append((x0 + (i + 1) * dx, y0 - h * dy))
    return pts


def walk(word, *, levels=(0,), cliff=None, letters_below=False, accent_upto=None,
         cut_at=None, mark=(), dx=DX, dy=DY, label="", pad_top=1, pad_bot=1,
         extra_right=0):
    """Ломаная по слову ±1 — главный примитив лекции.

    levels          какие высоты отчертить тонким пунктиром (0 — нулевой уровень)
    cliff           высота обрыва: сплошная черта (обычно −1)
    letters_below   подписать О/Р ПОД рёбрами (РАЗБОР §16.9: «читать удобнее снизу»)
    accent_upto     первые сколько-то рёбер — акцентом (выделенный кусок)
    cut_at          индекс узла, через который идёт пунктирная вертикаль-разрез
    mark            индексы узлов, которые надо залить (.s-node-r)
    """
    w = norm(word)
    hs, h = [0], 0
    for c in w:
        h += 1 if c == "+" else -1
        hs.append(h)
    hi, lo = max(hs), min(hs)
    if cliff is not None:
        lo = min(lo, cliff)
    for lv in levels:
        hi, lo = max(hi, lv), min(lo, lv)

    x0 = PAD + 14
    y0 = PAD + (hi + pad_top) * dy                       # y нулевого уровня
    W = x0 + len(w) * dx + PAD + extra_right
    H = y0 - (lo - pad_bot) * dy + (16 if letters_below else 0)
    Y = lambda k: y0 - k * dy

    b = []
    for lv in levels:
        b.append(line(PAD, Y(lv), W - PAD, Y(lv), "s-thin", "5 4"))
    if cliff is not None:
        b.append(line(PAD, Y(cliff), W - PAD, Y(cliff), "s-line"))
    pts = walk_geom(w, x0, y0, dx, dy)
    if accent_upto:
        b.append(poly(pts[:accent_upto + 1], "s-accent"))
        b.append(poly(pts[accent_upto:], "s-line"))
    else:
        b.append(poly(pts, "s-line"))
    if cut_at is not None:
        cx = pts[cut_at][0]
        b.append(line(cx, Y(hi + pad_top) + 4, cx, Y(lo - pad_bot) - 4, "s-dash"))
    for i, (x, y) in enumerate(pts):
        cls = "s-node-r" if i in mark else ("s-node-a" if i in (0, len(pts) - 1) else "s-node")
        b.append(node(x, y, cls, 4.2 if i in mark else R))
    if letters_below:
        for i, c in enumerate(w):
            b.append(txt(x0 + (i + 0.5) * dx, H - 4,
                         "О" if c == "+" else "Р", "s-txt-m"))
    for lv in levels:
        b.append(txt(PAD - 6, Y(lv) + 4, num(lv), "s-txt-m", "end"))
    if cliff is not None and cliff not in levels:
        b.append(txt(PAD - 6, Y(cliff) + 4, num(cliff), "s-txt-m", "end"))
    return svg(W, H, b, label or "Ломаная траектория из шагов вверх и вниз")


def frac(x, y, num, den, *, cls="s-txt", h=13):
    """Дробь двумя этажами: числитель, черта, знаменатель. §1.7 разбора прямо
    запрещает форму «1/2» текстом, а TeX внутри SVG недоступен — рисуем руками."""
    if den == 1:
        return [txt(x, y + h * 0.36, num, cls)]
    return [txt(x, y - h * 0.18, num, cls),
            line(x - h * 0.52, y + h * 0.10, x + h * 0.52, y + h * 0.10, "s-thin"),
            txt(x, y + h * 1.02, den, cls)]


# ───────────────────────────── треугольник Паскаля ─────────────────────────────
def pascal(rows, *, mode="int", cell_w=None, row_h=26, highlight=(), diagonals=0,
           neighbours=None, half_hint=False, label="", row_sums=False, half_coeff=False):
    """Треугольник Паскаля на `rows` строк — правка одного числа меняет глубину.

    mode        'int' — целые; 'frac' — дроби k/2^n (как на слайде столбцов)
    highlight   набор (n, k) — залить/акцентировать клетки
    diagonals   сколько восходящих диагоналей отчертить пунктиром (сумма — метка слева)
    neighbours  (n, k) — показать двумя стрелками, что клетка = сумма двух над ней
    row_sums    подписать справа сумму каждой строки (1, 2, 4, 8, …)
    """
    cw = cell_w or (36 if mode == "int" else 52)
    W = PAD * 2 + (rows) * cw + (80 if row_sums else 0) + (54 if diagonals else 0)
    H = PAD * 2 + rows * row_h
    left = PAD + (54 if diagonals else 0)
    cx = lambda n, k: left + (rows - 1 - n) * cw / 2 + k * cw + cw / 2
    cy = lambda n: PAD + n * row_h + row_h * 0.72

    b = []
    if diagonals:
        # Восходящая диагональ d — клетки (d−j, j), j = 0…⌊d/2⌋; её сумма и есть
        # число хороших слов. И концы пунктира, и подпись берутся ИЗ ЭТИХ ЖЕ клеток:
        # ручной рисунок, который тут был, подписывал каждую диагональ ПРЕДЫДУЩИМ
        # числом Фибоначчи (1,2,3,5,8 вместо 2,3,5,8,13) и выводил две линии за
        # край треугольника. Пока подпись пишется руками, такое не ловится ничем.
        for d in range(1, diagonals):
            cells = [(d - j, j) for j in range(d // 2 + 1) if d - j <= rows - 1]
            if not cells:
                continue
            (n1, k1), (n2, k2) = cells[0], cells[-1]     # нижний-левый и верхний-правый
            b.append(line(cx(n1, k1) - cw * .34, cy(n1) - 15,
                          cx(n2, k2) + cw * .34, cy(n2) - 15, "s-dash"))
            b.append(txt(left - 12, cy(n1) - 4,
                         sum(comb(n, k) for n, k in cells), "s-txt-m", "end"))
    if half_hint:
        b.append(line(cx(rows - 1, (rows - 1) / 2), PAD - 4,
                      cx(rows - 1, (rows - 1) / 2), PAD + rows * row_h - 6, "s-dash"))
    if neighbours:
        n, k = neighbours
        for kk in (k - 1, k):
            if 0 <= kk <= n - 1:
                b.append(arrow(cx(n - 1, kk), cy(n - 1) + 5, cx(n, k) - 2, cy(n) - 13, "s-ar-a"))
                if half_coeff:                       # ½ у стрелки, В СТОРОНУ от чисел
                    b += frac((cx(n - 1, kk) + cx(n, k)) / 2 + (26 if kk == k else -26),
                              (cy(n - 1) + cy(n)) / 2 - 9, 1, 2, cls="s-txt-m", h=11)
    for n in range(rows):
        for k in range(n + 1):
            v = comb(n, k)
            cls = "s-txt"
            if (n, k) in highlight:
                b.append(node(cx(n, k), cy(n) - 5, "s-node-a", cw * .40))
                cls = "s-txt-w"
            if mode == "int":
                b.append(txt(cx(n, k), cy(n), v, cls))
            else:
                b += frac(cx(n, k), cy(n) - 4, v, 2 ** n, cls=cls)
    if row_sums:
        for n in range(rows):
            b.append(txt(W - PAD, cy(n), 2 ** n, "s-txt-m", "end"))
    return svg(W, H, b, label or "Треугольник Паскаля")


# ───────────────────────────── ряд кружков (слово) ─────────────────────────────
def word_row(word, *, r=9, gap=30, label="", with_letters=False):
    """Слово из О и Р как ряд кружков: залитый = орёл."""
    w = norm(word)
    W = PAD * 2 + (len(w) - 1) * gap + 2 * r
    H = PAD * 2 + 2 * r + (16 if with_letters else 0)
    y = PAD + r
    b = []
    for i, c in enumerate(w):
        x = PAD + r + i * gap
        b.append(node(x, y, "s-node-r" if c == "+" else "s-node", r))
        if with_letters:
            b.append(txt(x, H - 4, "О" if c == "+" else "Р", "s-txt-m"))
    return svg(W, H, b, label or "Слово из букв О и Р рядом кружков")


# ───────────────────────────── маршрут в решётке ─────────────────────────────
def lattice(word, *, cell=30, label=""):
    """Тот же исход как ступенчатый маршрут по решётке: орёл — вправо, решка — вверх."""
    w = norm(word)
    nx, ny = w.count("+"), w.count("-")
    W = PAD * 2 + nx * cell
    H = PAD * 2 + ny * cell
    b = []
    for i in range(nx + 1):
        b.append(line(PAD + i * cell, PAD, PAD + i * cell, PAD + ny * cell, "s-thin"))
    for j in range(ny + 1):
        b.append(line(PAD, PAD + j * cell, PAD + nx * cell, PAD + j * cell, "s-thin"))
    x, y, pts = PAD, PAD + ny * cell, [(PAD, PAD + ny * cell)]
    for c in w:
        if c == "+":
            x += cell
        else:
            y -= cell
        pts.append((x, y))
    b.append(poly(pts, "s-accent"))
    b.append(node(pts[0][0], pts[0][1], "s-node-a"))
    b.append(node(pts[-1][0], pts[-1][1], "s-node-a"))
    return svg(W, H, b, label or "Маршрут по решётке из левого нижнего угла в правый верхний")


# ───────────────────────────── дерево слов ─────────────────────────────
def word_tree(depth, *, ban_double_heads=True, dx=78, dy=28, label=""):
    """Дерево слов из О и Р; при ban_double_heads ветка после О идёт только в Р."""
    levels = [[""]]
    for _ in range(depth):
        nxt = []
        for s in levels[-1]:
            for c in "+-":
                if ban_double_heads and s.endswith("+") and c == "+":
                    continue
                nxt.append(s + c)
        levels.append(nxt)
    H = PAD * 2 + (len(levels[-1]) - 1) * dy
    W = PAD * 2 + depth * dx
    ypos = {}
    for i, s in enumerate(levels[-1]):
        ypos[s] = PAD + i * dy
    for lv in range(len(levels) - 2, -1, -1):
        for s in levels[lv]:
            kids = [t for t in levels[lv + 1] if t[:-1] == s]
            ypos[s] = sum(ypos[t] for t in kids) / len(kids)
    X = lambda s: PAD + len(s) * dx
    b = []
    for lv in range(len(levels) - 1):
        for s in levels[lv]:
            for t in [t for t in levels[lv + 1] if t[:-1] == s]:
                b.append(line(X(s), ypos[s], X(t), ypos[t], "s-line"))
                mx, my = (X(s) + X(t)) / 2, (ypos[s] + ypos[t]) / 2
                b.append(txt(mx, my - 6, "О" if t[-1] == "+" else "Р", "s-txt"))
    for lv, row in enumerate(levels):
        for s in row:
            b.append(node(X(s), ypos[s], "s-node-r" if s == "" else "s-node"))
    return svg(W, H, b, label or "Дерево слов из букв О и Р без двух О подряд")


# ───────────────────────────── «до → после» двумя рядами ─────────────────────────────
def two_rows(top_svg_body, bot_svg_body, gap=90):
    raise NotImplementedError  # ряды собираются функциями ниже напрямую


def compress(word, *, dx=DX, dy=DY, label=""):
    """Домики: сверху хорошее слово длины n с ДОПИСАННОЙ в конец решкой (домики
    выделены), снизу — оно же после сжатия: каждый домик заменён одним шагом ВВЕРХ.
    Длина сжатого ровно n+1−k, букв О в нём столько же — k. Это и есть конструкция §9A.

    ⚠ Две живые ошибки, которые ловит именно эта функция:
      1) §9.0 разбора: в старом рисунке убирали ПОДЪЁМ, и сжатая ломаная всегда шла
         вниз. Верно наоборот — убираем СПУСК после каждого подъёма;
      2) без дописанной в конец решки слово, кончающееся на О, не сжимается, и длина
         выходит n−k вместо n+1−k — то есть картинка перестаёт отвечать формуле
         на слайде. Приписываем решку ВСЕГДА и показываем её на рисунке.
    """
    w = norm(word)
    assert "++" not in w, "слово должно быть хорошим: без двух О подряд"
    w = w + "-"                        # §9A: приписали решку — теперь после каждой О идёт Р
    comp, i = [], 0
    while i < len(w):
        if w[i] == "+" and i + 1 < len(w) and w[i + 1] == "-":
            comp.append("+")           # домик ∧ схлопнулся в один шаг вверх
            i += 2
        else:
            comp.append(w[i])
            i += 1
    comp = "".join(comp)
    k = w.count("+")
    assert len(comp) == len(w) - k, "сжатие обязано укоротить слово ровно на число орлов"
    assert comp.count("+") == k, "число орлов при сжатии не меняется"

    hs, h = [0], 0
    for c in w:
        h += 1 if c == "+" else -1
        hs.append(h)
    hs2, h = [0], 0
    for c in comp:
        h += 1 if c == "+" else -1
        hs2.append(h)

    x0 = PAD + 10
    top_y = PAD + (max(hs) + 1) * dy                  # y нулевого уровня верхнего ряда
    top_letters = top_y + (-min(hs) + 1.4) * dy       # строка букв под верхней ломаной
    bot_y = top_letters + 52 + (max(hs2) + 1) * dy    # y нулевого уровня нижнего ряда
    W = PAD * 2 + len(w) * dx + 10
    H = bot_y + (-min(hs2) + 1.4) * dy + 16

    b = []
    pts = walk_geom(w, x0, top_y, dx, dy)
    b.append(poly(pts, "s-line"))
    for i in range(len(w) - 1):                       # домики ∧ акцентом
        if w[i] == "+" and w[i + 1] == "-":
            b.append(poly(pts[i:i + 3], "s-accent"))
    for i, (x, y) in enumerate(pts):
        b.append(node(x, y, "s-node-a" if i in (0, len(pts) - 1) else "s-node"))
    for i, c in enumerate(w):
        # последняя буква — та самая дописанная решка; она приглушена, чтобы было
        # видно, что её приписали, а не она была в слове
        b.append(txt(x0 + (i + .5) * dx, top_letters,
                     "О" if c == "+" else "Р",
                     "s-txt-m" if i == len(w) - 1 else "s-txt"))
    b.append(arrow(x0 + dx, top_letters + 14, x0 + dx, bot_y - (max(hs2) + 1) * dy - 8))
    pts2 = walk_geom(comp, x0, bot_y, dx, dy)
    b.append(poly(pts2, "s-line"))
    for i, c in enumerate(comp):                      # уцелевшие подъёмы — акцентом
        if c == "+":
            b.append(poly(pts2[i:i + 2], "s-accent"))
    for i, (x, y) in enumerate(pts2):
        b.append(node(x, y, "s-node-a" if i in (0, len(pts2) - 1) else "s-node"))
    for i, c in enumerate(comp):
        b.append(txt(x0 + (i + .5) * dx, H - 4, "О" if c == "+" else "Р", "s-txt"))
    return svg(W, H, b, label or ("Сверху ломаная, где каждый подъём сразу сменяется "
                                  "спуском; снизу она же после сжатия — каждый домик "
                                  "заменён одним шагом вверх, ломаная стала короче"))


def reflect_frames(word, *, dx=DX, dy=DY, label=""):
    """Три кадра отражения: разрез в первом касании −1 · отражённый кусок · склейка.

    ⚠ Геометрия здесь легко делается неверной, и первый заход её и сделал неверной:
    отражение идёт относительно уровня −1, то есть h ↦ −2−h. По шагам это значит
    «поменять О и Р местами», НО отражённый кусок при этом СТАРТУЕТ С −2, а не с нуля.
    Если стартовать с нуля, кусок отражается относительно нуля, конец не сходится
    с хвостом, и картинка врёт про конструкцию. Отсюда параметр h0 у walk_geom.
    """
    w = norm(word)
    hs, h, first = [0], 0, None
    for i, c in enumerate(w):
        h += 1 if c == "+" else -1
        hs.append(h)
        if h == -1 and first is None:
            first = i + 1
    assert first is not None, "путь обязан коснуться −1"
    flip = {"+": "-", "-": "+"}
    refl = "".join(flip[c] for c in w[:first]) + w[first:]
    hs2, h = [-2], -2                       # высоты склеенного пути: старт −2
    for c in refl:
        h += 1 if c == "+" else -1
        hs2.append(h)
    assert hs2[first] == -1, "отражённый кусок обязан прийти в −1"
    assert hs2[-1] == hs[-1], "склейка обязана кончиться там же, где исходный путь"

    hi, lo = max(max(hs), max(hs2)), min(min(hs), min(hs2))
    x0 = PAD + 20
    W = PAD * 2 + len(w) * dx + 20
    bandh = (hi - lo + 2) * dy
    H = PAD * 2 + 3 * bandh + 2 * 26

    b = []
    for f in range(3):
        base = PAD + f * (bandh + 26) + (hi + 1) * dy
        Y = lambda k, base=base: base - k * dy
        for lv in (0, -1, -2):
            b.append(line(PAD + 16, Y(lv), W - PAD, Y(lv), "s-thin", "5 4"))
            b.append(txt(PAD + 10, Y(lv) + 4, num(lv), "s-txt-m", "end"))
        if f == 0:                                    # исходный путь, разрез
            pts = walk_geom(w, x0, base, dx, dy)
            b.append(poly(pts[:first + 1], "s-accent"))
            b.append(poly(pts[first:], "s-line"))
            b.append(line(pts[first][0], Y(hi + 1), pts[first][0], Y(lo - 1), "s-dash"))
        elif f == 1:                                  # исходный кусок бледно + отражённый
            pts0 = walk_geom(w, x0, base, dx, dy)
            b.append(poly(pts0[:first + 1], "s-thin"))
            b.append(poly(pts0[first:], "s-thin"))
            pts = walk_geom(refl, x0, base, dx, dy, h0=-2)
            b.append(poly(pts[:first + 1], "s-accent"))
            b.append(line(PAD + 16, Y(-1), W - PAD, Y(-1), "s-dash"))   # зеркало
        else:                                         # склейка целиком, из −2
            pts = walk_geom(refl, x0, base, dx, dy, h0=-2)
            b.append(poly(pts[:first + 1], "s-accent"))
            b.append(poly(pts[first:], "s-line"))
        for i, (x, y) in enumerate(pts):
            if f == 1 and i > first:
                continue                              # во втором кадре хвост только бледный
            cls = ("s-node-r" if i == first else
                   ("s-node-a" if i in (0, len(pts) - 1) else "s-node"))
            b.append(node(x, y, cls, 4.2 if i == first else R))
        seq = w if f == 0 else refl                   # буквы под звеньями: на втором и
        for i, ch in enumerate(seq):                  # третьем кадре в НАЧАЛЬНОМ куске
            if f == 1 and i > first - 1:              # они уже поменялись местами
                continue
            b.append(txt(x0 + (i + .5) * dx, Y(lo - 1) + 15,
                         "О" if ch == "+" else "Р", "s-txt-m"))
    return svg(W, H, b, label or ("Три кадра: путь разрезан в первом касании уровня минус "
                                  "один; начальный кусок отражён относительно этого уровня "
                                  "и теперь идёт из уровня минус два; склеенный путь целиком "
                                  "идёт из минус двух в ту же конечную высоту"))


def six_walks(words, *, cols=3, dx=30, dy=22, label=""):
    """Панелька из нескольких коротких ломаных — «выпишем их все» (вопрос 10)."""
    n = len(words)
    rows = (n + cols - 1) // cols
    L = len(norm(words[0]))
    cw = L * dx + 46
    ch = 5 * dy + 26
    W = PAD * 2 + cols * cw
    H = PAD * 2 + rows * ch
    b = []
    for i, wd in enumerate(words):
        ox = PAD + (i % cols) * cw + 16
        oy = PAD + (i // cols) * ch + 3 * dy
        b.append(line(ox - 10, oy, ox + L * dx + 10, oy, "s-thin", "5 4"))
        pts = walk_geom(wd, ox, oy, dx, dy)
        b.append(poly(pts, "s-line"))
        for j, (x, y) in enumerate(pts):
            b.append(node(x, y, "s-node-a" if j == 0 else "s-node", 3.0))
    return svg(W, H, b, label or ("Все короткие траектории, ни разу не опускающиеся "
                                  "ниже нулевого уровня, выписаны панельками"))


def row_unroll(n=5, *, r=22, gap=104, label=""):
    """Строка треугольника, РАСКРУЧЕННАЯ из единицы: числа в кружках, между ними
    стрелки, над каждой стрелкой — множитель-дробь. Это та самая выкладка §5C,
    которая была в первой версии текста и пропала при сокращении; разбор просит
    её вернуть («найти её в исходной версии и вернуть»)."""
    vals = [comb(n, k) for k in range(n)]
    W = PAD * 2 + (len(vals) - 1) * gap + 2 * r
    H = PAD * 2 + 2 * r + 34
    y = PAD + 34 + r
    b = []
    for i, v in enumerate(vals):
        x = PAD + r + i * gap
        if i < len(vals) - 1:
            b.append(arrow(x + r + 8, y, x + gap - r - 8, y))
            # множитель: (n−k)/(k+1) — ровно то, что даёт тождество с капитаном
            b.append(txt(x + gap / 2, y - r - 16, "%d/%d" % (n - i, i + 1), "s-txt-m"))
        if i == 0:
            b.append(node(x, y, "s-node-a", r + 5))     # единица, с которой начинаем
        b.append(node(x, y, "s-node", r))
        b.append(txt(x, y + 5, v, "s-txt"))
    return svg(W, H, b, label or ("Строка треугольника Паскаля: числа в кружках связаны "
                                  "стрелками, над каждой стрелкой стоит дробь-множитель; "
                                  "первое число обведено как исходное"))


def row_symmetry(n=4, *, cell=76, label=""):
    """Одна строка треугольника с дугами, связывающими равноудалённые от краёв числа:
    симметрия видна прямо на строке (§5B разбора — «вывести одну строку и показать
    симметрию прямо на ней»)."""
    vals = [comb(n, k) for k in range(n + 1)]
    W = PAD * 2 + len(vals) * cell
    H = PAD * 2 + 96
    y = PAD + 34
    X = lambda i: PAD + (i + 0.5) * cell
    b = [line(X(n / 2), PAD, X(n / 2), PAD + 14, "s-dash"),
         line(X(n / 2), y + 18, X(n / 2), H - PAD, "s-dash")]
    for i, v in enumerate(vals):
        b.append(txt(X(i), y, v, "s-txt"))
    for i in range(n // 2 + (0 if n % 2 else 0)):
        j = n - i
        if i >= j:
            break
        x1, x2 = X(i), X(j)
        dip = y + 30 + (n // 2 - i) * 20
        b.append('<path class="s-thin" d="M %g,%g Q %g,%g %g,%g"/>'
                 % (x1, y + 14, (x1 + x2) / 2, dip, x2, y + 14))
    return svg(W, H, b, label or ("Одна строка треугольника Паскаля; дуги связывают числа, "
                                  "равноудалённые от краёв, посередине пунктирная ось"))


def two_walks(w1, w2, *, dx=DX, dy=DY, gap=70, label=""):
    """Два пути рядом, кончающиеся на ОДНОЙ высоте — тонкая пунктирная горизонталь
    показывает это без единого слова (манера эталона СПЕКИ)."""
    a, b_ = norm(w1), norm(w2)
    def hs(w):
        h, out = 0, [0]
        for c in w:
            h += 1 if c == "+" else -1
            out.append(h)
        return out
    ha, hb = hs(a), hs(b_)
    assert ha[-1] == hb[-1], "пути обязаны кончаться на одной высоте"
    hi, lo = max(max(ha), max(hb)), min(min(ha), min(hb))
    x0 = PAD + 14
    W = PAD * 2 + (len(a) + len(b_)) * dx + gap + 28
    y0 = PAD + (hi + 1) * dy
    H = y0 - (lo - 1) * dy + 20
    Y = lambda k: y0 - k * dy
    b = [line(PAD, Y(0), W - PAD, Y(0), "s-thin", "5 4"),
         line(PAD, Y(ha[-1]), W - PAD, Y(ha[-1]), "s-thin", "5 4")]
    x = x0
    for w, cls in ((a, "s-line"), (b_, "s-accent")):
        pts = walk_geom(w, x, y0, dx, dy)
        b.append(poly(pts, cls))
        for i, (px, py) in enumerate(pts):
            b.append(node(px, py, "s-node-a" if i in (0, len(pts) - 1) else "s-node"))
        x += len(w) * dx + gap
    return svg(W, H, b, label or ("Два пути рядом, оба кончающиеся на одной высоте; "
                                  "уровень показан тонким пунктиром"))


def safe_table(lengths=(2, 4, 6), *, dx=17, dy=13, label=""):
    """Все пути, ни разу не опускающиеся ниже нуля, выписанные ПАНЕЛЬКАМИ по длинам.
    §10 разбора: «начинать не с 2n=4, а с 2n=0, потом 2, 4, 6 — и выписывать»."""
    from itertools import product
    groups = []
    for L in lengths:
        ws = []
        for w in product("+-", repeat=L):
            h, ok = 0, True
            for c in w:
                h += 1 if c == "+" else -1
                if h < 0:
                    ok = False
                    break
            if ok:
                ws.append("".join(w))
        groups.append((L, ws))
    colw = lambda L: L * dx + 20
    cols = [min(len(ws), 10) for _, ws in groups]
    rows = [(len(ws) + c - 1) // c for (_, ws), c in zip(groups, cols)]
    widths = [c * colw(L) for (L, _), c in zip(groups, cols)]
    W = PAD * 2 + sum(widths) + 44 * (len(groups) - 1)
    H = PAD * 2 + max(rows) * (7 * dy)
    b, ox = [], PAD
    for gi, ((L, ws), c) in enumerate(zip(groups, cols)):
        for i, wd in enumerate(ws):
            px = ox + (i % c) * colw(L) + 10
            py = PAD + (i // c) * 7 * dy + 3 * dy
            b.append(line(px - 6, py, px + L * dx + 6, py, "s-thin", "4 3"))
            pts = walk_geom(wd, px, py, dx, dy)
            b.append(poly(pts, "s-line"))
            b.append(node(pts[0][0], pts[0][1], "s-node-a", 2.4))
        b.append(txt(ox + widths[gi] / 2, H - PAD + 6, len(ws), "s-txt"))
        ox += widths[gi] + 44
    return svg(W, H, b, label or ("Все траектории, ни разу не опускающиеся ниже нулевого "
                                  "уровня, выписаны панельками по длинам; под каждой "
                                  "группой стоит их число"))


def ladder(steps=7, *, label=""):
    """Кадр S2, фаза 1: вертикальная пожарная лестница со ступеньками-отметками,
    точка на ней, лестница внизу кончается (шаг с нижней ступеньки — падение)."""
    w_rail, sp = 54, 30
    W = PAD * 2 + w_rail + 40
    H = PAD * 2 + steps * sp + 26
    xl, xr = PAD + 20, PAD + 20 + w_rail
    ytop = PAD
    ybot = PAD + steps * sp
    b = [line(xl, ytop, xl, ybot, "s-line"), line(xr, ytop, xr, ybot, "s-line")]
    for i in range(steps + 1):
        y = ybot - i * sp
        b.append(line(xl, y, xr, y, "s-thin"))
        b.append(txt(xl - 8, y + 4, i, "s-txt-m", "end"))
    b.append(line(xl - 10, ybot + 16, xr + 10, ybot + 16, "s-line"))   # обрыв
    b.append(node((xl + xr) / 2, ybot - 3 * sp, "s-node-r", 6.5))
    return svg(W, H, b, label or ("Вертикальная лестница со ступеньками, пронумерованными "
                                  "снизу вверх; на одной из ступенек стоит точка, под нижней "
                                  "ступенькой лестница кончается сплошной чертой"))


# ───────────────────────────── реестр рисунков дека ─────────────────────────────
def registry():
    """name → (функция без аргументов, к какому слайду). Правка = правка одной строки."""
    return {
        # S2 · пьяница на лестнице (статический дубль канваса — на случай, если канвас не идёт)
        "cliff-ladder": (lambda: ladder(7), "S2"),
        "cliff-walk": (lambda: walk("+-++--+-++--", levels=(0,), cliff=-1,
                                    letters_below=True,
                                    label="Ломаная траектория: время слева направо, "
                                          "положение вверх; под каждым звеном стоит буква "
                                          "О или Р; внизу сплошная черта обрыва"), "S2"),
        # S4 · треугольник Паскаля: дроби и целые
        "pascal-frac": (lambda: pascal(6, mode="frac", neighbours=(4, 2), half_coeff=True, label="Треугольник из дробей: "
                                       "каждое число — вероятность попасть в клетку"), "S4"),
        "pascal-int": (lambda: pascal(8, mode="int", neighbours=(5, 2),
                                      label="Треугольник Паскаля из целых чисел; в одну "
                                            "клетку ведут две стрелки из двух клеток "
                                            "предыдущей строки"), "S4"),
        "pascal-cut": (lambda: walk("+-++-+-+", levels=(0,), letters_below=True,
                                    cut_at=7, accent_upto=7, dx=40,
                                    label="Путь целиком; последнее звено отделено "
                                          "пунктирной вертикалью"), "S4"),
        # S5 · три облика
        "views-walk": (lambda: walk("+--+", levels=(0,), letters_below=True,
                                    label="Исход четырёх бросков как ломаная"), "S5A"),
        "views-word": (lambda: word_row("+--+", with_letters=True,
                                        label="Тот же исход как ряд кружков: залитый "
                                              "кружок — орёл"), "S5A"),
        "views-lattice": (lambda: lattice("+--+",
                                          label="Тот же исход как маршрут по решётке"), "S5A"),
        # S5B · большой треугольник: симметрия и суммы строк
        "tri-sums": (lambda: pascal(7, mode="int", row_sums=True, half_hint=True,
                                    label="Треугольник Паскаля на семь строк; справа от "
                                          "каждой строки стоит её сумма, посередине "
                                          "проведена пунктирная ось симметрии"), "S5B"),
        # S5C · раскрутка строки из единицы
        "team-row": (lambda: row_unroll(5), "S5C"),
        # S5B · симметрия ПРЯМО НА СТРОКЕ (§5B: «вывести одну строку и показать
        # симметрию на ней» — раньше такая строка была и потом пропала)
        "row-symmetry": (lambda: row_symmetry(4), "S5B"),
        "team-diag": (lambda: pascal(7, mode="int", highlight={(3, 3), (4, 3), (5, 3), (6, 3)},
                                     label="Тот же треугольник: выделен столбец, по "
                                           "которому строка раскручивается вдоль "
                                           "диагонали"), "S5C"),
        # S6 · разрез по центру
        "cut-middle": (lambda: walk("+-+++--+--", levels=(0,), letters_below=True,
                                    cut_at=5, accent_upto=5, dx=56, dy=32,
                                    label="Путь длины восемь, разрезанный посередине "
                                          "пунктирной вертикалью; первая половина "
                                          "выделена"), "S6"),
        # S9 · домики (ИСПРАВЛЕННЫЙ рисунок, §9.0)
        "domiki": (lambda: compress("+-+--+-+--", dx=78), "S9A"),
        # 🔴 ban-tree, diagonals, six-paths, final-walk В РЕЕСТР НЕ ВХОДЯТ СОЗНАТЕЛЬНО.
        # Разбор их не назвал плохими, а про дерево слов сказано прямо: «красивое
        # и уместное». Заход: «Рисунки, которые владелец не назвал, не трогай».
        # Генератор их умеет (word_tree / pascal(diagonals=…) / six_walks), но файлы
        # на диске остаются РУЧНЫЕ — иначе первый же прогон молча их перерисует.
        # S11 · ОБЩИЙ плохой путь: касается −1 несколько раз и уходит ниже (§11.4)
        "bad-walk": (lambda: walk("+--+---++-", levels=(0, -1), cliff=None,
                                  letters_below=True, cut_at=3, accent_upto=3, dx=76, dy=34,
                                  label="Путь, который несколько раз опускается ниже "
                                        "нулевого уровня и уходит глубже; вертикаль "
                                        "отмечает первое касание"), "S11"),
        # S12 · отражение
        "reflect3": (lambda: reflect_frames("+--+---++-"), "S12"),
        # S6 · пара путей длины 5, кончившихся на одной высоте (то, во что превратился разрез)
        "pair-heights": (lambda: two_walks("+-++-", "++--+", dx=58, dy=34, gap=120), "S6"),
        # S9B · восходящие диагонали — СВОЙ рисунок вместо ручного: у того подписи
        # диагоналей были сдвинуты на одно число Фибоначчи (1,2,3,5,8 вместо
        # 2,3,5,8,13). Разбор рисунок плохим не называл, но он врёт по числам,
        # и оставить его значило бы вынести ошибку на экран.
        "diagonals": (lambda: pascal(8, mode="int", diagonals=8,
                                     label="Треугольник Паскаля; пунктиром отчерчены "
                                           "восходящие диагонали, слева у каждой стоит "
                                           "сумма её чисел"), "S9B"),
        # S10 · все безопасные пути длин 2, 4 и 6 (§10: «начинать не с 2n=4, а с 2n=0»)
        "safe-table": (lambda: safe_table((2, 4, 6)), "S10"),
        # S12b · строка 10: 252 и 210 — те два числа, из которых складывается 42
        "counts-row": (lambda: pascal(11, mode="int", cell_w=64, row_h=30,
                                      highlight={(10, 5), (10, 6)},
                                      label="Десятая строка треугольника Паскаля; выделены "
                                            "два соседних числа, разность которых и есть "
                                            "ответ"), "S12b"),
        # S6 · разрез по центру и пара путей на одной высоте
        "cut-pair": (lambda: walk("+-++--+-", levels=(0,), letters_below=True,
                                  cut_at=4, accent_upto=4,
                                  label="Путь длины восемь, разрезанный посередине"), "S6"),
    }


def main():
    reg = registry()
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if "--list" in sys.argv:
        for name, (_, slide) in sorted(reg.items()):
            print("  %-16s → illustrations/%s.svg   (%s)" % (name, name, slide))
        return 0
    names = args or sorted(reg)
    unknown = [n for n in names if n not in reg]
    if unknown:
        print("нет таких рисунков: %s" % unknown)
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    for n in names:
        s = reg[n][0]()
        (OUT / (n + ".svg")).write_text(s, encoding="utf-8")
        print("  ✓ %s.svg  (%d Б)" % (n, len(s.encode())))
    print("готово: %d рисунк(ов) в %s" % (len(names), OUT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
