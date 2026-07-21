#!/usr/bin/env python3
"""ПЕЧАТНАЯ ФИГУРА ЛИСТКА Л4 — ряд кривых дракона рангов 1–5 под определением в шапке.

    python3 kartoteka/gen_l4_figs.py        →  kartoteka/L4-fig-ranks.svg

Зачем она есть. Владелец 19.07: «лучше определить кривую дракона вне задачи и нарисовать
картинки для разных рангов». До этого определение пряталось внутри условия задачи, а слово
«дракон» в курсе было неоднозначным (доказывали для всех способов складывания, а «всегда в одну
сторону» отдельно не вводили). Теперь определение стоит в шапке, и рядом — как оно выглядит.

⚠ ЭТО ПЕЧАТНАЯ ФИГУРА, НЕ doc-ВИД. Цвет и толщина — атрибутами, не классами: в листке нет
   движка со стилями. Размеры в мм заданы явно — во WeasyPrint inline-SVG схлопывается при
   width:auto (грабли Л1/Л2).

Гейты (как у gen_l2_figs.py, оба ловили живые дефекты в прошлых листках):
  1) ПОСАДКА — всё нарисованное внутри рамки; рамка считается по ВСЕМУ, что рисуем,
     включая подписи, а не только по ломаным (на Л2 так молча обрезался треугольник);
  2) МЕТКИ — номера рангов не налезают друг на друга и не садятся на ломаную.
"""
import math, pathlib, sys

W_MM, H_MM = 166, 38          # ширина под поле листка A4 (186 мм) с запасом
RANKS = [1, 2, 3, 4, 5]
VB_W, VB_H = 1660, 380        # 10 единиц вьюбокса на миллиметр
LABEL_Y = 352                 # базовая линия номера ранга
STROKE = 5.4                  # в единицах вьюбокса ≈ 0.54 мм


def flip(s):
    return ''.join('R' if c == 'L' else 'L' for c in reversed(s))


def word(n):
    s = ''
    for _ in range(n):
        s = s + 'L' + flip(s)
    return s


def poly(w):
    """ломаная: старт (0,0), первое звено вправо, повороты по буквам на 90°"""
    x = y = 0.0
    dx, dy = 1.0, 0.0
    pts = [(0.0, 0.0), (dx, dy)]
    for c in w:
        dx, dy = (-dy, dx) if c == 'L' else (dy, -dx)
        x, y = pts[-1]
        pts.append((x + dx, y + dy))
    return pts


def fit(pts, box, pad=16):
    """вписать в бокс (x, y, w, h); экранный y растёт вниз, математический — вверх"""
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    s = min((box[2] - 2 * pad) / max(x1 - x0, 1e-9),
            (box[3] - 2 * pad) / max(y1 - y0, 1e-9))
    ox = box[0] + pad + ((box[2] - 2 * pad) - s * (x1 - x0)) / 2
    oy = box[1] + pad + ((box[3] - 2 * pad) - s * (y1 - y0)) / 2
    return lambda p: (ox + (p[0] - x0) * s, oy + (y1 - p[1]) * s)


def build():
    cw = VB_W / len(RANKS)
    parts, drawn, labels = [], [], []
    for i, n in enumerate(RANKS):
        box = (i * cw, 0, cw, LABEL_Y - 46)
        P = poly(word(n))
        g = fit(P, box)
        S = [g(p) for p in P]
        drawn += S
        d = 'M ' + ' L '.join(f'{x:.1f} {y:.1f}' for x, y in S)
        parts.append(f'<path d="{d}" fill="none" stroke="#000" stroke-width="{STROKE}" '
                     f'stroke-linejoin="round" stroke-linecap="round"/>')
        # точка начала — та же метка «отмеченный конец», что во всех листках курса
        parts.append(f'<circle cx="{S[0][0]:.1f}" cy="{S[0][1]:.1f}" r="{STROKE*1.5:.1f}" fill="#000"/>')
        lx = i * cw + cw / 2
        labels.append((lx, LABEL_Y))
        parts.append(f'<text x="{lx:.1f}" y="{LABEL_Y}" text-anchor="middle" '
                     f'font-family="Georgia, serif" font-size="46" fill="#000">{n}</text>')
    return parts, drawn, labels


def main():
    parts, drawn, labels = build()
    bad = []
    # ГЕЙТ 1 — посадка: считаем по всему, что рисуем, включая подписи
    allpts = drawn + [(x, y - 34) for x, y in labels] + [(x, y + 12) for x, y in labels]
    for x, y in allpts:
        if not (0 <= x <= VB_W and 0 <= y <= VB_H):
            bad.append(f'за рамкой: ({x:.0f}, {y:.0f}) при вьюбоксе {VB_W}×{VB_H}')
    # ГЕЙТ 2 — метки: номера не слипаются между собой и не садятся на ломаную
    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            d = math.hypot(labels[i][0] - labels[j][0], labels[i][1] - labels[j][1])
            if d < 60:
                bad.append(f'номера рангов слиплись: зазор {d:.0f} < 60')
    for lx, ly in labels:
        near = min(math.hypot(lx - x, ly - y) for x, y in drawn)
        if near < 24:
            bad.append(f'номер ранга сел на ломаную: зазор {near:.0f} < 24')
    if bad:
        print('ГЕЙТ ФИГУРЫ ПРОВАЛЕН:\n  ' + '\n  '.join(dict.fromkeys(bad)))
        sys.exit(1)

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VB_W} {VB_H}" '
           f'width="{W_MM}mm" height="{H_MM}mm" role="img" '
           f'aria-label="кривые дракона рангов с первого по пятый">\n  '
           + '\n  '.join(parts) + '\n</svg>\n')
    out = pathlib.Path(__file__).resolve().parent / 'L4-fig-ranks.svg'
    out.write_text(svg)
    zaz = min(min(math.hypot(lx - x, ly - y) for x, y in drawn) for lx, ly in labels)
    print(f'✓ {out.name}: рангов {len(RANKS)}, {len(drawn)} точек, '
          f'минимальный зазор метки до ломаной {zaz:.0f} (порог 24) — ГЕЙТЫ ПРОЙДЕНЫ')


if __name__ == '__main__':
    main()
