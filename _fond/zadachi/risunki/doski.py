#!/usr/bin/env python3
"""doski.py — рисунки клеточных досок для листков задач.

Печатает готовые куски SVG, которые вставляются в карточки банка
(`_fond/zadachi/bank/*.md`). Движок листка отдаёт абзац, начинающийся
с `<svg` или `<figure`, как есть — см. `build_listok.py`, функция `v_html`.

Цвет только классами `.s-*`; они определены в STIL движка листка.
Рисовать доски руками нельзя: их много, и правятся они разом отсюда.

    python3 doski.py lenta      — лента шагов разметки для ладьи
    python3 doski.py pustye     — пустые доски 5x5 под зарисовку
    python3 doski.py otvety     — заполненные доски (черепашка, король)
    python3 doski.py reshyotka  — решётка степеней двойки и пятёрки
"""
from __future__ import annotations
import sys
from functools import lru_cache

SH = 30          # сторона клетки
POLE = 14        # поля от края viewBox


def doska(W: int, H: int, krasnye=(), zelyonye=(), novaya=None,
          fishka=None, podpisi=None, nomera=False) -> str:
    """Доска W×H. Координаты — от левого нижнего угла, (0,0) слева внизу."""
    w = W * SH + 2 * POLE
    h = H * SH + 2 * POLE + (14 if nomera else 0)
    def xy(cx, cy):
        return POLE + cx * SH, POLE + (H - 1 - cy) * SH
    ch = [f'<svg viewBox="0 0 {w} {h}" width="{w}" role="img" '
          f'aria-label="доска {W} на {H}, часть клеток закрашена">']
    for cx in range(W):
        for cy in range(H):
            x, y = xy(cx, cy)
            if (cx, cy) in krasnye:
                k = "s-krasnaya"
            elif (cx, cy) in zelyonye:
                k = "s-zelyonaya"
            else:
                k = "s-kletka"
            ch.append(f'<rect class="{k}" x="{x}" y="{y}" width="{SH}" height="{SH}"/>')
    if novaya:
        x, y = xy(*novaya)
        ch.append(f'<rect class="s-novaya" x="{x+1}" y="{y+1}" width="{SH-2}" height="{SH-2}"/>')
    if fishka:
        x, y = xy(*fishka)
        ch.append(f'<circle class="s-fishka" cx="{x+SH/2}" cy="{y+SH/2}" r="5"/>')
    for t, cx, cy in (podpisi or []):
        x, y = xy(cx, cy)
        ch.append(f'<text class="s-txt" x="{x+SH/2}" y="{y+SH/2+4}" '
                  f'text-anchor="middle">{t}</text>')
    ch.append("</svg>")
    return "".join(ch)


def kadr(svg: str, podpis: str) -> str:
    return f'<figure>{svg}<figcaption>{podpis}</figcaption></figure>'


def lenta(kadry: list[str]) -> str:
    return '<figure class="ris"><div class="lenta">' + "".join(kadry) + "</div></figure>"


# ── ладья: ходит влево или вниз на любое расстояние, угол (0,0) — конец ──
def ladya_shagi(N=5):
    """Кадры заполнения: красный угол, зелёные соседи, новая красная, и так далее."""
    kadry = []
    kr, ze = set(), set()
    kr.add((0, 0))
    kadry.append(kadr(doska(N, N, kr, ze, novaya=(0, 0)),
                      "Из угла ходить некуда — тот, чей ход, проиграл. Клетка красная."))
    for c in range(1, N):
        ze |= {(c, 0), (0, c)}
    kadry.append(kadr(doska(N, N, kr, ze),
                      "Из всей нижней строки и левого столбца ладья одним ходом "
                      "доходит до красного угла. Все эти клетки зелёные."))
    kr.add((1, 1))
    kadry.append(kadr(doska(N, N, kr, ze, novaya=(1, 1)),
                      "А отсюда в красное не попасть: и влево, и вниз — только зелёное. "
                      "Новая красная клетка."))
    for c in range(2, N):
        ze |= {(c, 1), (1, c)}
    kadry.append(kadr(doska(N, N, kr, ze),
                      "Её строка и столбец снова становятся зелёными — из них есть ход "
                      "в новую красную."))
    kr.add((2, 2))
    for c in range(3, N):
        ze |= {(c, 2), (2, c)}
    kadry.append(kadr(doska(N, N, kr, ze, novaya=(2, 2)),
                      "Повторяем то же самое на следующей клетке диагонали."))
    kr |= {(3, 3), (4, 4)}
    ze = {(x, y) for x in range(N) for y in range(N)} - kr
    kadry.append(kadr(doska(N, N, kr, ze),
                      "Доска заполнена. Красные — вся диагональ: там, где до обоих краёв "
                      "поровну."))
    return lenta(kadry)


# ── черепашка и хромой король ───────────────────────────────────────────
def razmetka(N, hody):
    @lru_cache(None)
    def w(x, y):
        for dx, dy in hody:
            nx, ny = x + dx, y + dy
            if nx < N and ny < N and not w(nx, ny):
                return True
        return False
    kr = {(x, y) for x in range(N) for y in range(N) if not w(x, y)}
    ze = {(x, y) for x in range(N) for y in range(N)} - kr
    return kr, ze


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


def main():
    """Кладёт все рисунки файлами рядом с собой: движок листка подставляет
    их по маркеру `![ris:имя]`."""
    from pathlib import Path
    tut = Path(__file__).parent
    tochki = reshyotka_tochki()
    faily = {
        "ladya-shagi": ladya_shagi(),
        "doska-pustaya": '<figure class="ris">' + doska(5, 5, fishka=(0, 0))
            + '<figcaption>Доска для раскрашивания. Фишка стоит в левом нижнем углу.'
              '</figcaption></figure>',
        "reshyotka-pustaya": '<figure class="ris">'
            + doska_stupenchataya(tochki)
            + '<figcaption>Каждая клетка — своё число: вправо отложено, сколько взято '
              'двоек, вверх — сколько пятёрок.</figcaption></figure>',
        "reshyotka-otvet": '<figure class="ris">'
            + doska_stupenchataya(tochki, reshyotka_krasnye(tochki))
            + '<figcaption>Красные клетки решётки.</figcaption></figure>',
        # две доски друг под другом: этаж «монетка на столе» и этаж «монетку забрали»
        "dve-doski": '<figure class="ris"><div class="lenta">'
            + kadr(doska(5, 6, fishka=(4, 5)), "Монетка на столе")
            + kadr(doska(5, 6, fishka=(4, 5)), "Монетку уже забрали")
            + '</div><figcaption>Ладья стоит в четырёх клетках от левого края и пяти '
              'от нижнего. Обе доски одинаковые — отличается только то, лежит ли ещё '
              'монетка.</figcaption></figure>',
    }
    for imya, hody, podpis in [
            ("cherepashka-otvet", ((1, 0), (0, 1)), "Черепашка: красные клетки идут в шахматном порядке."),
            ("korol-otvet", ((1, 0), (0, 1), (1, 1)), "Хромой король: красных меньше, и стоят они реже.")]:
        kr, ze = razmetka(5, hody)
        faily[imya] = ('<figure class="ris">' + doska(5, 5, kr, ze, fishka=(0, 0))
                       + f'<figcaption>{podpis}</figcaption></figure>')
    if len(sys.argv) > 1 and sys.argv[1] == "pechat":
        print(faily[sys.argv[2]])
        return
    for imya, svg in faily.items():
        (tut / f"{imya}.svg").write_text(svg, encoding="utf-8")
        print(f"→ {imya}.svg  ({len(svg)} симв.)")


def doska_stupenchataya(tochki, krasnye=(), podpisi=True) -> str:
    W = max(a for a, _ in tochki) + 1
    H = max(b for _, b in tochki) + 1
    w = W * SH + 2 * POLE + 16
    h = H * SH + 2 * POLE + 16
    def xy(cx, cy):
        return POLE + 16 + cx * SH, POLE + (H - 1 - cy) * SH
    ch = [f'<svg viewBox="0 0 {w} {h}" width="{w}" role="img" '
          f'aria-label="ступенчатая фигура из клеток, часть закрашена">']
    for (a, b) in tochki:
        x, y = xy(a, b)
        k = "s-krasnaya" if (a, b) in krasnye else "s-kletka"
        ch.append(f'<rect class="{k}" x="{x}" y="{y}" width="{SH}" height="{SH}"/>')
    if podpisi:
        for a in range(W):
            x, y = xy(a, 0)
            ch.append(f'<text class="s-txt" x="{x+SH/2}" y="{y+SH+13}" '
                      f'text-anchor="middle">{a}</text>')
        for b in range(H):
            x, y = xy(0, b)
            ch.append(f'<text class="s-txt" x="{x-7}" y="{y+SH/2+4}" '
                      f'text-anchor="end">{b}</text>')
    ch.append("</svg>")
    return "".join(ch)


if __name__ == "__main__":
    main()
