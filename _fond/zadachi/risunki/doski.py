#!/usr/bin/env python3
"""doski.py — рисунки клеточных досок для листков задач.

Кладёт SVG файлами рядом с собой; движок листка подставляет их
по маркеру `![ris:имя]` (см. `build_listok.py`, `podstavit_risunki`).

Цвет — только классами `.s-*`, они определены в STIL движка листка
и в словаре примитивов (`_illustracii/DISCIPLINA.md`, примитивы #13 и #14).

🔴 На каждой доске обязаны читаться ТРИ вещи (требование владельца 17.09):
   1. откуда стартуют — клетка с обводкой, цвет её ещё неизвестен;
   2. какая клетка заведомо красная — там, где партия кончилась;
      если игра кончается выходом за поле, такие клетки рисуются ЗА краем;
   3. как ходит фигура — стрелками от фишки, поставленной НЕ в углу и НЕ на
      старте, чтобы её не приняли за начальную позицию.
   Без этих трёх опор разметку не с чего начинать, и ученик встаёт.

    python3 doski.py            — перерисовать все файлы
    python3 doski.py pechat ИМЯ — напечатать один в stdout
"""
from __future__ import annotations
import math
import sys
from functools import lru_cache
from pathlib import Path

SH = 32          # сторона клетки
POLE = 16        # поля от края viewBox


def _strelka(x1, y1, x2, y2) -> str:
    a = math.atan2(y2 - y1, x2 - x1)
    L, W = 9, 4.2
    nx, ny = x2 - L * math.cos(a), y2 - L * math.sin(a)
    px, py = -math.sin(a) * W, math.cos(a) * W
    return (f'<line class="s-strelka" x1="{x1:.1f}" y1="{y1:.1f}" '
            f'x2="{nx:.1f}" y2="{ny:.1f}"/>'
            f'<path class="s-ostriyo" d="M{x2:.1f},{y2:.1f} '
            f'L{nx+px:.1f},{ny+py:.1f} L{nx-px:.1f},{ny-py:.1f} Z"/>')


def doska(W, H, krasnye=(), zelyonye=(), start=None, konec=None,
          fishka=None, hody=(), luchi=False, vne=(), nomera=False,
          sh=None, aria="доска с клетками") -> str:
    """Доска W×H, координаты от левого нижнего угла: (0,0) слева внизу."""
    s = sh or SH
    minx = min([v[0] for v in vne] + [0])
    maxx = max([v[0] for v in vne] + [W - 1])
    miny = min([v[1] for v in vne] + [0])
    maxy = max([v[1] for v in vne] + [H - 1])
    otstup = 20 if nomera else 0
    w = (maxx - minx + 1) * s + 2 * POLE + otstup
    h = (maxy - miny + 1) * s + 2 * POLE + otstup

    def xy(cx, cy):
        return POLE + otstup + (cx - minx) * s, POLE + (maxy - cy) * s

    ch = [f'<svg viewBox="0 0 {w} {h}" width="{w}" role="img" aria-label="{aria}">']
    for cx in range(W):
        for cy in range(H):
            x, y = xy(cx, cy)
            k = ("s-krasnaya" if (cx, cy) in krasnye else
                 "s-zelyonaya" if (cx, cy) in zelyonye else "s-kletka")
            ch.append(f'<rect class="{k}" x="{x}" y="{y}" width="{s}" height="{s}"/>')
    for (cx, cy) in vne:
        x, y = xy(cx, cy)
        ch.append(f'<rect class="s-vne" x="{x}" y="{y}" width="{s}" height="{s}"/>')
    if konec:
        x, y = xy(*konec)
        ch.append(f'<rect class="s-krasnaya" x="{x}" y="{y}" width="{s}" height="{s}"/>')
    if start:
        x, y = xy(*start)
        ch.append(f'<rect class="s-start" x="{x+2}" y="{y+2}" '
                  f'width="{s-4}" height="{s-4}"/>')
    if fishka:
        fx, fy = fishka
        x, y = xy(fx, fy)
        cx0, cy0 = x + s / 2, y + s / 2
        for dx, dy in hody:
            if luchi:
                n = 0
                while 0 <= fx + dx * (n + 1) < W and 0 <= fy + dy * (n + 1) < H:
                    n += 1
                for k in range(1, n):
                    tx, ty = xy(fx + dx * k, fy + dy * k)
                    ch.append(f'<circle class="s-dostupno" cx="{tx+s/2}" '
                              f'cy="{ty+s/2}" r="3"/>')
                tx, ty = xy(fx + dx * n, fy + dy * n)
                ch.append(_strelka(cx0 + dx * 12, cy0 - dy * 12, tx + s / 2, ty + s / 2))
            else:
                tx, ty = xy(fx + dx, fy + dy)
                ch.append(_strelka(cx0 + dx * 11, cy0 - dy * 11, tx + s / 2, ty + s / 2))
        ch.append(f'<circle class="s-fishka" cx="{cx0}" cy="{cy0}" r="{s/5.5:.1f}"/>')
    if nomera:
        for cx in range(W):
            x, y = xy(cx, 0)
            ch.append(f'<text class="s-txt" x="{x+s/2}" y="{y+s+14}" '
                      f'text-anchor="middle">{cx}</text>')
        for cy in range(H):
            x, y = xy(0, cy)
            ch.append(f'<text class="s-txt" x="{x-8}" y="{y+s/2+4}" '
                      f'text-anchor="end">{cy}</text>')
    ch.append("</svg>")
    return "".join(ch)


def stupenchataya(tochki, krasnye=(), start=None, vne=(), nomera=True) -> str:
    maxx = max(a for a, _ in list(tochki) + list(vne))
    maxy = max(b for _, b in list(tochki) + list(vne))
    w = (maxx + 1) * SH + 2 * POLE + 20
    h = (maxy + 1) * SH + 2 * POLE + 20

    def xy(cx, cy):
        return POLE + 20 + cx * SH, POLE + (maxy - cy) * SH

    ch = [f'<svg viewBox="0 0 {w} {h}" width="{w}" role="img" '
          f'aria-label="ступенчатое поле из клеток">']
    for (a, b) in tochki:
        x, y = xy(a, b)
        k = "s-krasnaya" if (a, b) in krasnye else "s-kletka"
        ch.append(f'<rect class="{k}" x="{x}" y="{y}" width="{SH}" height="{SH}"/>')
    for (a, b) in vne:
        x, y = xy(a, b)
        ch.append(f'<rect class="s-vne" x="{x}" y="{y}" width="{SH}" height="{SH}"/>')
    if start:
        x, y = xy(*start)
        ch.append(f'<rect class="s-start" x="{x+2}" y="{y+2}" '
                  f'width="{SH-4}" height="{SH-4}"/>')
    if nomera:
        for a in range(maxx + 1):
            x, y = xy(a, 0)
            ch.append(f'<text class="s-txt" x="{x+SH/2}" y="{y+SH+14}" '
                      f'text-anchor="middle">{a}</text>')
        for b in range(maxy + 1):
            x, y = xy(0, b)
            ch.append(f'<text class="s-txt" x="{x-8}" y="{y+SH/2+4}" '
                      f'text-anchor="end">{b}</text>')
    ch.append("</svg>")
    return "".join(ch)


def kadr(svg, podpis):
    return f'<figure>{svg}<figcaption>{podpis}</figcaption></figure>'


def lenta(kadry, podpis=None):
    hvost = f'<figcaption>{podpis}</figcaption>' if podpis else ""
    return ('<figure class="ris"><div class="lenta">' + "".join(kadry)
            + "</div>" + hvost + "</figure>")


def ris(svg, podpis):
    return f'<figure class="ris">{svg}<figcaption>{podpis}</figcaption></figure>'


# ── разметки ────────────────────────────────────────────────────────────
def razmetka(N, hody):
    @lru_cache(None)
    def w(x, y):
        for dx, dy in hody:
            nx, ny = x + dx, y + dy
            if nx < N and ny < N and not w(nx, ny):
                return True
        return False
    kr = {(x, y) for x in range(N) for y in range(N) if not w(x, y)}
    return kr, {(x, y) for x in range(N) for y in range(N)} - kr


def ferz_krasnye(N):
    """Цзяньшицзы: влево, вниз или по диагонали — на любое расстояние."""
    @lru_cache(None)
    def w(a, b):
        if a == 0 and b == 0:
            return False
        for k in range(1, a + 1):
            if not w(a - k, b):
                return True
        for k in range(1, b + 1):
            if not w(a, b - k):
                return True
        for k in range(1, min(a, b) + 1):
            if not w(a - k, b - k):
                return True
        return False
    return {(a, b) for a in range(N) for b in range(N) if not w(a, b)}


def ladya_shagi(N=5):
    kadry = []
    kr, ze = {(0, 0)}, set()
    kadry.append(kadr(doska(N, N, kr, ze, start=(N-1, N-1)),
                      "Угол внизу слева — конец игры: оттуда ходить некуда, "
                      "и тот, чей ход, проиграл. Эта клетка красная всегда. "
                      "Обведена клетка, где мы стартуем."))
    for c in range(1, N):
        ze |= {(c, 0), (0, c)}
    kadry.append(kadr(doska(N, N, kr, ze, start=(N-1, N-1)),
                      "Из всей нижней строки и левого столбца ладья одним ходом "
                      "доходит до красного угла — значит все они зелёные."))
    kr.add((1, 1))
    kadry.append(kadr(doska(N, N, kr, ze, start=(N-1, N-1)),
                      "А отсюда в красное не попасть: и влево, и вниз только "
                      "зелёное. Новая красная клетка."))
    for c in range(2, N):
        ze |= {(c, 1), (1, c)}
    kr.add((2, 2))
    for c in range(3, N):
        ze |= {(c, 2), (2, c)}
    kadry.append(kadr(doska(N, N, kr, ze, start=(N-1, N-1)),
                      "Повторяем то же самое на следующих клетках диагонали."))
    kr |= {(3, 3), (4, 4)}
    ze = {(x, y) for x in range(N) for y in range(N)} - kr
    kadry.append(kadr(doska(N, N, kr, ze),
                      "Доска заполнена. Стартовая клетка оказалась красной — "
                      "значит проигрывает тот, чей ход."))
    return lenta(kadry, "Ладья ходит влево или вниз на сколько угодно клеток.")


def reshyotka_tochki():
    return [(a, b) for a in range(12) for b in range(6) if 2**a * 5**b < 1000]


def reshyotka_krasnye(tochki):
    @lru_cache(None)
    def w(a, b):
        for da, db in ((1, 0), (0, 1)):
            if 2**(a+da) * 5**(b+db) >= 1000:
                return True
            if not w(a+da, b+db):
                return True
        return False
    return {p for p in tochki if not w(*p)}


def reshyotka_vne(tochki):
    est = set(tochki)
    vne = set()
    for a, b in est:
        for da, db in ((1, 0), (0, 1)):
            if (a+da, b+db) not in est:
                vne.add((a+da, b+db))
    return vne


def main():
    tut = Path(__file__).parent
    tochki = reshyotka_tochki()
    N, NF = 5, 13
    faily = {
        "ladya-shagi": ladya_shagi(),

        "cherepashka-pole": ris(
            doska(N, N, start=(0, 0), konec=(N-1, N-1), fishka=(2, 1),
                  hody=((1, 0), (0, 1)),
                  aria="доска пять на пять, фишка со стрелками вправо и вверх"),
            "Черепашка ходит на клетку вправо или вверх. Фишка поставлена для "
            "примера — она может стоять где угодно. Красный угол справа вверху — "
            "конец игры: оттуда ходов нет. Обведена клетка, где фишка стоит "
            "в начале партии."),
        "korol-pole": ris(
            doska(N, N, start=(0, 0), konec=(N-1, N-1), fishka=(2, 1),
                  hody=((1, 0), (0, 1), (1, 1)),
                  aria="доска пять на пять, стрелки вправо, вверх и по диагонали"),
            "Хромой король ходит на клетку вправо, вверх или по диагонали. "
            "Конец игры и старт — те же."),

        "dve-doski": lenta([
            kadr(doska(N, 6, start=(4, 5), fishka=(4, 5),
                       hody=((-1, 0), (0, -1)), luchi=True,
                       aria="доска, ладья в правом верхнем углу, стрелки влево и вниз"),
                 "Монетка на столе. Отсюда партия начинается. Кружки — клетки, "
                 "куда ладья может попасть одним ходом."),
            kadr(doska(N, 6, konec=(0, 0),
                       aria="доска, левый нижний угол закрашен красным"),
                 "Монетку уже забрали. Ладья в углу — ходов нет вовсе, эта "
                 "клетка красная без разметки. С неё и начинайте."),
        ], "Доски одинаковые; отличается только то, лежит ли ещё монетка."),

        "reshyotka-pustaya": ris(
            stupenchataya(tochki, start=(0, 0), vne=reshyotka_vne(tochki)),
            "Поле игры — белые клетки. Красные по краю лежат уже за полем: "
            "попасть туда значит перевалить за тысячу и выиграть, так что для "
            "того, чей ход, они заведомо проигрышные. От них и начинайте. "
            "Обведена клетка, где партия начинается."),
        "reshyotka-otvet": ris(
            stupenchataya(tochki, reshyotka_krasnye(tochki), start=(0, 0),
                          vne=reshyotka_vne(tochki)),
            "Что должно получиться."),

        # цзяньшицзы: в условии — БЕЗ стрелок, фигуру ученик узнаёт сам
        "ferz-setka": ris(
            doska(NF, NF, konec=(0, 0), start=(8, 11), nomera=True, sh=26,
                  aria="пустая доска с осями, левый нижний угол красный"),
            "Клетка — позиция игры: вправо отложено, сколько камней в первой "
            "кучке, вверх — сколько во второй. Красный угол: обе кучки пусты, "
            "ходить нечем, и тот, чей ход, проиграл. Обведена клетка, с которой "
            "начинается партия."),
        "ferz-pole": ris(
            doska(NF, NF, konec=(0, 0), start=(8, 11), fishka=(7, 8),
                  hody=((-1, 0), (0, -1), (-1, -1)), luchi=True, nomera=True,
                  sh=26, aria="доска, фигура с лучами влево, вниз и по диагонали"),
            "Ферзь ходит влево, вниз или наискосок вниз-влево — на сколько "
            "угодно клеток. Красный угол внизу слева: кто поставил туда ферзя, "
            "тот выиграл, сопернику ходить нечем. Обведена клетка, с которой "
            "начинается партия."),
        "ferz-otvet": ris(
            doska(NF, NF, krasnye=ferz_krasnye(NF), start=(8, 11), nomera=True,
                  sh=26, aria="доска с размеченными проигрышными клетками"),
            "Проигрышные клетки и зеркальные им. На диагональ они не ложатся, "
            "и никакой кратности в них нет."),
    }
    for imya, hody, podpis in [
            ("cherepashka-otvet", ((1, 0), (0, 1)),
             "Черепашка: красные клетки идут в шахматном порядке."),
            ("korol-otvet", ((1, 0), (0, 1), (1, 1)),
             "Хромой король: красных меньше, и стоят они реже.")]:
        kr, ze = razmetka(N, hody)
        faily[imya] = ris(doska(N, N, kr, ze, start=(0, 0)), podpis)

    if len(sys.argv) > 2 and sys.argv[1] == "pechat":
        print(faily[sys.argv[2]])
        return
    for imya, svg in faily.items():
        (tut / f"{imya}.svg").write_text(svg, encoding="utf-8")
        print(f"→ {imya}.svg  ({len(svg)} симв.)")


if __name__ == "__main__":
    main()
