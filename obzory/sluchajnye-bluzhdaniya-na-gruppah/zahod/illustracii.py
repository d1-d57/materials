#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Иллюстрации вкладки I. Подставляет SVG вместо маркеров <!--ILL:имя--> в 01-poyya-kesten.md.

Дисциплина — SLOVAR-primitivov.md: внутри рисунка только метки, пояснение в figcaption,
фона нет, классы только .s-*. Место считается из viewBox: высота/ширина >= 0,6 -> на поле.
Все четыре рисунка горизонтальные, то есть идут в поток.

Запуск:  python3 _zahod/illustracii.py     (из папки sluchajnye-bluzhdaniya)
"""
import math
import random
import re
import pathlib

MD = pathlib.Path(__file__).resolve().parent.parent / "01-poyya-kesten.md"


def figure(name, w, h, body, caption):
    ratio = h / w
    cls = ' class="mn"' if ratio >= 0.6 else ""
    return (
        '<figure%s>\n<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" '
        'role="img" aria-label="%s">\n%s\n</svg>\n<figcaption>%s</figcaption>\n</figure>'
        % (cls, w, h, name, body, caption)
    )


# ── 1. решётка: три момента времени и растущий масштаб sqrt(n) ───────────────
def ill_reshetka():
    """Три панели бок о бок: чем дольше идём, тем шире круг радиуса sqrt(n).
    Сетку НЕ рисуем: все звенья ломаной осевые, решётка читается и без неё,
    а 60+ линий сетки превратили бы рисунок в миллиметровку."""
    W, H = 720, 286
    step, cy = 8, 128
    panels = [(130, 20), (360, 60), (590, 150)]
    p = []
    for (cx, n) in panels:
        R = step * math.sqrt(n)
        best = None
        for seed in range(6000):
            r = random.Random(seed * 7 + n)
            px, py, pts, far = 0, 0, [(0, 0)], 0
            for _ in range(n):
                dx, dy = r.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                px, py = px + dx, py + dy
                pts.append((px, py))
                far = max(far, math.hypot(px, py))
            # Траектория должна ЗАПОЛНЯТЬ круг и стоять вокруг старта, а не висеть сбоку:
            # первый член тянет край облака к окружности, второй штрафует смещение центра масс.
            mx = sum(a for a, _ in pts) / len(pts)
            my = sum(b for _, b in pts) / len(pts)
            score = abs(far * step - R * 0.93) + 2.4 * math.hypot(mx, my) * step
            if best is None or score < best[0]:
                best = (score, pts)
        pts = best[1]
        poly = " ".join("%.0f,%.0f" % (cx + a * step, cy + b * step) for a, b in pts)
        p.append('<circle class="s-dash" cx="%d" cy="%.0f" r="%.1f" fill="none"/>' % (cx, cy, R))
        p.append('<polyline class="s-line" fill="none" points="%s"/>' % poly)
        p.append('<circle class="s-node s-node-r" cx="%d" cy="%.0f" r="4"/>' % (cx, cy))
        p.append('<text class="s-txt-m" x="%d" y="%d" text-anchor="middle">n = %d</text>'
                 % (cx, H - 14, n))
    return figure(
        "решётка", W, H, "\n".join(p),
        "Блуждание на $\\mathbb Z^2$ за 20, 60 и 150 шагов; пунктиром — окружность радиуса "
        "$\\sqrt n$ в том же масштабе. Траектория растёт вместе с ней, а не быстрее: "
        "внутри круга оказывается порядка $n$ узлов, и на каждый приходится порядка $1/n$ "
        "вероятности.")


# ── 2. дерево свободной группы ───────────────────────────────────────────────
def ill_derevo():
    """H-раскладка: из вершины три ребра по осям (кроме обратного), длина падает вдвое
    с лишним. Радиальная раскладка тут не годится — при сжатии по y ветви пересекаются,
    и дерево перестаёт читаться как дерево. Растяжение по x (KX) аффинно, пересечений
    не создаёт, и уводит рисунок из жёлоба в поток."""
    KX, KY = 1.88, 1.0
    lens = [92, 41, 18]
    DIRS = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    ext = sum(lens)
    cx, cy = ext * KX + 34, ext * KY + 26
    W, H = int(2 * cx), int(2 * cy)
    nodes, edges = [((0, 0), 0)], []

    def grow(pt, came, lvl):
        if lvl >= len(lens):
            return
        for d in DIRS:
            if came is not None and d == (-came[0], -came[1]):
                continue
            q = (pt[0] + d[0] * lens[lvl], pt[1] + d[1] * lens[lvl])
            edges.append((pt, q, lvl))
            nodes.append((q, lvl + 1))
            grow(q, d, lvl + 1)

    grow((0, 0), None, 0)
    ray = [(sum(lens[:k]), 0) for k in range(len(lens) + 1)]

    def S(pt):
        return (cx + KX * pt[0], cy + KY * pt[1])

    p = []
    for (a, b, lvl) in edges:
        cls = "s-line" if lvl <= 1 else "s-thin"
        (x1, y1), (x2, y2) = S(a), S(b)
        p.append('<line class="%s" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
                 % (cls, x1, y1, x2, y2))
    for k in range(len(lens)):
        (x1, y1), (x2, y2) = S(ray[k]), S(ray[k + 1])
        p.append('<line class="s-accent" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
                 % (x1, y1, x2, y2))
    for (pt, lvl) in nodes:
        x, y = S(pt)
        p.append('<circle class="s-node" cx="%.1f" cy="%.1f" r="%.1f"/>'
                 % (x, y, 3.4 if lvl <= 2 else 2.6))
    for pt in ray[1:]:
        x, y = S(pt)
        p.append('<circle class="s-node s-node-a" cx="%.1f" cy="%.1f" r="3.2"/>' % (x, y))
    p.append('<circle class="s-node s-node-r" cx="%.1f" cy="%.1f" r="4.6"/>' % (cx, cy))
    p.append('<text class="s-txt" x="%.1f" y="%.1f">e</text>' % (cx + 8, cy - 9))
    # метку уводим ПОПЕРЁК своего ребра, иначе она ложится на тёмную линию и не читается
    for lab, d, off in (("a", (1, 0), (-17, -12)), ("b", (0, -1), (15, 17))):
        x, y = S((d[0] * lens[0], d[1] * lens[0]))
        p.append('<text class="s-txt-m" x="%.1f" y="%.1f" text-anchor="middle">%s</text>'
                 % (x + off[0], y + off[1], lab))
    return figure(
        "дерево", W, H, "\n".join(p),
        "Граф Кэли свободной группы $F_2$ — четырёхвалентное дерево (рисунок растянут по "
        "горизонтали, длина рёбер убывает только ради места). Из каждой вершины три ребра "
        "уводят прочь и лишь одно ведёт назад, поэтому блуждание сносит наружу со средней "
        "скоростью $1/2$: выделенный луч — типичное направление ухода.")


# ── 3. фонарщик ──────────────────────────────────────────────────────────────
def ill_fonarshchik():
    W, H = 720, 236
    xs = [70 + i * 48 for i in range(13)]
    rows = [
        (46, [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0], 5),
        (128, [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0], 6),
        (210, [0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0], 6),
    ]
    p = []
    # горящий фонарь — залитый узел .s-node-r, потушенный — белый .s-node,
    # фонарщик — акцентный .s-node-a над лентой. Три роли, три вида узла.
    for (y, lamps, pos) in rows:
        p.append('<line class="s-thin" x1="%d" y1="%d" x2="%d" y2="%d"/>'
                 % (xs[0] - 26, y, xs[-1] + 26, y))
        for i, on in enumerate(lamps):
            cls = "s-node s-node-r" if on else "s-node"
            p.append('<circle class="%s" cx="%d" cy="%d" r="5.4"/>' % (cls, xs[i], y))
        p.append('<line class="s-thin" x1="%d" y1="%d" x2="%d" y2="%d"/>'
                 % (xs[pos], y - 20, xs[pos], y - 9))
        p.append('<circle class="s-node s-node-a" cx="%d" cy="%d" r="5"/>' % (xs[pos], y - 25))
    for (y0, y1, lab) in ((46, 128, "t"), (128, 210, "σ")):
        p.append('<line class="s-thin" x1="30" y1="%d" x2="30" y2="%d"/>' % (y0 + 14, y1 - 26))
        p.append('<path class="s-ar-m" d="M 30,%d l4,-9 -8,0 z"/>' % (y1 - 22))
        p.append('<text class="s-txt-a" x="16" y="%d" text-anchor="middle">%s</text>'
                 % ((y0 + y1) // 2, lab))
    return figure(
        "фонарщик", W, H, "\n".join(p),
        "Состояние группы $\\mathbb Z_2\\wr\\mathbb Z$: какие фонари горят и где стоит "
        "фонарщик. Образующая $t$ сдвигает фонарщика, $σ$ переключает фонарь под ним. "
        "Чтобы вернуться в исходное состояние, мало прийти назад — надо ещё погасить всё "
        "зажжённое по дороге.")


# ── 4. множества Фёльнера: квадрат в решётке против шара в дереве ────────────
def ill_folner():
    W, H = 720, 300
    p = []
    # панель А: квадрат 9x9 в решётке
    n, step, x0, y0 = 9, 27, 82, 42
    for i in range(n):
        for j in range(n):
            edge = i in (0, n - 1) or j in (0, n - 1)
            cls = "s-node s-node-a" if edge else "s-node"
            p.append('<circle class="%s" cx="%d" cy="%d" r="3.4"/>'
                     % (cls, x0 + i * step, y0 + j * step))
    for i in range(n):
        p.append('<line class="s-thin" x1="%d" y1="%d" x2="%d" y2="%d"/>'
                 % (x0 + i * step, y0, x0 + i * step, y0 + (n - 1) * step))
        p.append('<line class="s-thin" x1="%d" y1="%d" x2="%d" y2="%d"/>'
                 % (x0, y0 + i * step, x0 + (n - 1) * step, y0 + i * step))
    p.append('<text class="s-txt-m" x="%d" y="%d" text-anchor="middle">32 : 81</text>'
             % (x0 + (n - 1) * step / 2, y0 + (n - 1) * step + 34))
    # панель Б: шар радиуса 2 в четырёхвалентном дереве — H-раскладка, как в ill_derevo
    # (радиальная с угловым разбросом даёт пересечения ветвей и врёт про предмет)
    cx, cy = 530, 150
    L1, L2 = 78, 42
    DIRS = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    nodes, edges, bnd = [(cx, cy)], [], []
    for d in DIRS:
        pt = (cx + d[0] * L1, cy + d[1] * L1)
        edges.append(((cx, cy), pt))
        nodes.append(pt)
        for e in DIRS:
            if e == (-d[0], -d[1]):
                continue
            q = (pt[0] + e[0] * L2, pt[1] + e[1] * L2)
            edges.append((pt, q))
            bnd.append(q)
    for (a, b) in edges:
        p.append('<line class="s-thin" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
                 % (a[0], a[1], b[0], b[1]))
    for pt in nodes:
        p.append('<circle class="s-node" cx="%.1f" cy="%.1f" r="3.4"/>' % pt)
    for pt in bnd:
        p.append('<circle class="s-node s-node-a" cx="%.1f" cy="%.1f" r="3.4"/>' % pt)
    p.append('<circle class="s-node s-node-r" cx="%d" cy="%d" r="4.2"/>' % (cx, cy))
    p.append('<text class="s-txt-m" x="%d" y="%d" text-anchor="middle">12 : 17</text>'
             % (cx, cy + 142))
    return figure(
        "Фёльнер", W, H, "\n".join(p),
        "Слева квадрат $9\\times9$ в $\\mathbb Z^2$: граничных вершин 32 из 81, и с ростом "
        "стороны доля падает как $1/N$. Справа шар радиуса 2 в дереве: граничных 12 из 17, "
        "и сколько шар ни увеличивай, доля границы не падает. Первое — множество Фёльнера, "
        "второго не бывает.")


ILLS = {
    "reshetka": ill_reshetka,
    "derevo": ill_derevo,
    "fonarshchik": ill_fonarshchik,
    "folner": ill_folner,
}

if __name__ == "__main__":
    # Идемпотентно: подставляем и на маркер <!--ILL:имя-->, и поверх уже вставленной
    # фигуры (ищем по aria-label). Иначе перегенерация требовала бы ручного отката.
    txt = MD.read_text(encoding="utf-8")
    done = []
    for name, fn in ILLS.items():
        svg = fn()
        label = re.search(r'aria-label="([^"]+)"', svg).group(1)
        marker = "<!--ILL:%s-->" % name
        pat = re.compile(r'<figure[^>]*>\s*<svg[^>]*aria-label="%s".*?</figure>'
                         % re.escape(label), re.S)
        if marker in txt:
            txt = txt.replace(marker, svg)
            done.append(name)
        elif pat.search(txt):
            txt = pat.sub(lambda _m: svg, txt, count=1)
            done.append(name + " (перерисован)")
    MD.write_text(txt, encoding="utf-8")
    print("подставлено:", ", ".join(done) if done else "ничего")
