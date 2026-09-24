#!/usr/bin/env python3
# TOOL-CONTRACT: called-by-hand — после svod_4chasa.py; пишет INFOGRAFIKA-4-chasa.svg и .png
"""Инфографика 7И за 4 часа: 15.09 (два листка) + 22.09 (один листок, пара).

Данные — SVOD-4-chasa.json и SVOD-4-chasa-profil.json (их пишет svod_4chasa.py).
Стиль повторяет INFOGRAFIKA-15-09.png, которую видели коллеги.
"""
import json, statistics as st
from html import escape as E
from pathlib import Path
import cairosvg

H = Path(__file__).resolve().parent
D = json.load(open(H / 'SVOD-4-chasa.json', encoding='utf-8'))
PROF = {int(k): v for k, v in json.load(open(H / 'SVOD-4-chasa-profil.json')).items()}
BG, CARD, INK, MUTED, GRID = '#e9eef3', '#ffffff', '#1f2933', '#5b6b7a', '#d5dde5'
BLUE, ORANGE, RED, PALE = '#2a78d6', '#eb6834', '#b04a3a', '#c5d3df'
FONT = 'Liberation Sans, DejaVu Sans, sans-serif'
W = 1600
o = []

def t(x, y, s, size=15, anchor='start', fill=INK, weight='normal', font=FONT):
    o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{fill}" '
             f'font-weight="{weight}" font-family="{font}">{E(str(s))}</text>')

def card(x, y, w, h):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{CARD}"/>')

def head(x, y, cap, sub):
    t(x, y, cap, 15, fill=MUTED, weight='bold'); t(x, y + 26, sub, 16)

fam = lambda n: n.split()[0]
# на странице — только имя и инициал фамилии, как в infografika.py («surnames never reach the page»)
short = lambda n: (lambda p: f'{p[1]} {p[0][0]}.' if len(p) > 1 else p[0])(n.split())
pct = lambda r, a, b: 100 * r[a] / r[b] if r[a] is not None else None
LISTKI = [('Обратный ход · 15.09', 'oh', 'oh_max'), ('Правда, ложь и перебор · 15.09', 'lg', 'lg_max'),
          ('Комбинаторика 1 · 22.09 · весь листок', 'k22', 'k22_max'),
          ('Комбинаторика 1 · 22.09 · обязательная часть', 'k22o', 'k22o_max')]
k22 = [r for r in D if r['k22'] is not None]
both = [r for r in D if None not in (r['oh'], r['lg'], r['k22'])]
cor = lambda a, b: st.correlation([pct(r, *a) for r in both], [pct(r, *b) for r in both])
c1, c2, c3 = cor(('oh', 'oh_max'), ('lg', 'lg_max')), cor(('oh', 'oh_max'), ('k22', 'k22_max')), cor(('lg', 'lg_max'), ('k22', 'k22_max'))
dop = round(100 * sum(r['k22_zony']['d'] for r in k22) / (len(k22) * 20))
obyaz_med = st.median(pct(r, 'k22o', 'k22o_max') for r in k22)
three = [r for r in D if None not in r['perc']]
verh = [r for r in three if min(r['perc']) >= 67]
niz = [r for r in three if max(r['perc']) <= 33]
skachut = sorted([r for r in three if max(r['perc']) - min(r['perc']) >= 60], key=lambda r: -(max(r['perc']) - min(r['perc'])))

y = 60
t(60, y, '7И · 15 и 22 сентября · 4 часа, три листка', 42, weight='bold', font='Liberation Serif, DejaVu Serif, serif')
t(60, y + 38, 'Единица счёта — пункт; зачтено = плюс преподавателя или верный записанный ответ. 15.09 без пунктов: там задача = пункт.', 16, fill=MUTED)
t(60, y + 62, f'22.09 — {len(k22)} работ; четверым, начавшим сразу с треугольников, кружки засчитаны (решение ведущего): '
    'Петр Б., Даниил В., Ярослав Л., Марк Ю.', 16, fill=MUTED)

y = 150
kpi = [(f'{obyaz_med:.0f}%', 'обязательной части 22.09 — медиана'), (f'{dop}%', 'пунктов допзадач 10–19 взято'),
       (f'{min(c1, c2, c3):.2f}–{max(c1, c2, c3):.2f}'.replace('.', ','), 'связь мест в классе между листками'),
       (f'{len(niz)} и {len(verh)}', 'устойчиво снизу и сверху на всех трёх')]
for i, (big, small) in enumerate(kpi):
    x = 60 + i * 375; card(x, y, 355, 110); t(x + 24, y + 58, big, 40, weight='bold'); t(x + 24, y + 90, small, 16, fill=MUTED)

# 1. разброс на каждом листке
y = 290; card(60, y, 1480, 390)
head(84, y + 34, '1 · РАЗБРОС КЛАССА НА КАЖДОМ ЛИСТКЕ', 'Кружок — ребёнок. По горизонтали — доля пунктов листка, которую он взял. Полоса — средняя половина класса, черта — медиана.')
X0, X1 = 520, 1480
xs = lambda p: X0 + (X1 - X0) * p / 100
for p in range(0, 101, 20):
    o.append(f'<line x1="{xs(p)}" y1="{y + 90}" x2="{xs(p)}" y2="{y + 360}" stroke="{GRID}"/>'); t(xs(p), y + 380, f'{p}%', 13, 'middle', MUTED)
for i, (name, a, b) in enumerate(LISTKI):
    yy = y + 115 + i * 66
    vals = sorted(pct(r, a, b) for r in D if r[a] is not None)
    q1, q3, med = vals[len(vals) // 4], vals[(3 * len(vals)) // 4], st.median(vals)
    t(84, yy + 5, name, 15)
    t(84, yy + 24, f'n={len(vals)} · медиана {med:.0f}% · от {vals[0]:.0f} до {vals[-1]:.0f}', 13, fill=MUTED)
    o.append(f'<rect x="{xs(q1)}" y="{yy - 16}" width="{xs(q3) - xs(q1)}" height="32" rx="6" fill="#e3ebf3"/>')
    o.append(f'<line x1="{xs(med)}" y1="{yy - 20}" x2="{xs(med)}" y2="{yy + 20}" stroke="{INK}" stroke-width="2"/>')
    col = ORANGE if a.startswith('k22') else BLUE
    seen = {}
    for v in vals:
        k = round(v); n = seen.get(k, 0); seen[k] = n + 1
        o.append(f'<circle cx="{xs(v)}" cy="{yy - 8 + (n % 3) * 8}" r="6" fill="{col}" fill-opacity="0.75"/>')

# 2. место в классе на трёх листках
y = 700; card(60, y, 900, 700)
head(84, y + 34, '2 · МЕСТО В КЛАССЕ ОТ ЛИСТКА К ЛИСТКУ', 'Линия — ребёнок с тремя листками. Вверху — лучше класса. Цветом — те, кто скачет сильнее всех.')
PX = [220, 520, 820]; PY0, PY1 = y + 120, y + 640
py = lambda p: PY1 - (PY1 - PY0) * p / 100
for x, cap in zip(PX, ['обратный ход', 'логика', 'комбинаторика']):
    o.append(f'<line x1="{x}" y1="{PY0}" x2="{x}" y2="{PY1}" stroke="{GRID}"/>'); t(x, PY1 + 30, cap, 14, 'middle', MUTED)
for p, cap in ((100, 'лучший'), (50, 'середина'), (0, 'последний')):
    t(PX[0] - 20, py(p) + 5, cap, 13, 'end', MUTED)
hl = {fam(r['imya']): c for r, c in zip(skachut[:4], [ORANGE, RED, BLUE, '#7a4fb3'])}
for r in sorted(three, key=lambda r: fam(r['imya']) in hl):
    c = hl.get(fam(r['imya'])); pts = ' '.join(f'{x},{py(p):.1f}' for x, p in zip(PX, r['perc']))
    o.append(f'<polyline points="{pts}" fill="none" stroke="{c or PALE}" stroke-width="{3.5 if c else 1.6}"/>')
    if c:
        t(PX[2] + 14, py(r['perc'][2]) + 5, short(r['imya']), 14, fill=c, weight='bold')

# 3. группы
y = 700; card(980, y, 560, 700)
head(1004, y + 34, '3 · КТО ГДЕ', 'Место в классе на каждом из трёх листков (перцентиль).')
def spisok(yy, cap, col, rows, fmt):
    t(1004, yy, cap, 16, fill=col, weight='bold'); yy += 28
    for r in rows:
        t(1020, yy, fmt(r), 15); yy += 24
    return yy + 14
f3 = lambda r: f"{short(r['imya'])} — {' · '.join(str(p) for p in r['perc'])}"
yy = spisok(y + 110, f'Сверху на всех трёх ({len(verh)})', BLUE, verh, f3)
yy = spisok(yy, f'Снизу на всех трёх ({len(niz)})', RED, niz, f3)
yy = spisok(yy, f'Скачут: разница мест ≥ 60 ({len(skachut)})', ORANGE, skachut, f3)
t(1004, y + 672, 'Перцентиль: ОХ · логика · комбинаторика. Нужны все три листка.', 13, fill=MUTED)

# 4. профиль 22.09
y = 1420; card(60, y, 1480, 405)
head(84, y + 34, '4 · КОМБИНАТОРИКА 1 — ДОЛЯ ВЗЯТЫХ ПУНКТОВ ПО ЗАДАЧАМ', 'Столбик — доля пунктов задачи, взятая классом. После девятой задачи класс не пошёл дальше: поля там в основном пустые, а не с крестами.')
B0, BW = 110, 1400 / 22
for n in range(1, 23):
    a, b = PROF.get(n, [0, 1]); p = 100 * a / b
    col = PALE if n <= 5 else BLUE if n <= 9 else ORANGE if n <= 19 else RED
    x = B0 + (n - 1) * BW; h = 220 * p / 100
    o.append(f'<rect x="{x:.1f}" y="{y + 330 - h:.1f}" width="{BW - 10:.1f}" height="{h:.1f}" fill="{col}"/>')
    t(x + (BW - 10) / 2, y + 322 - h, f'{p:.0f}', 13, 'middle', MUTED); t(x + (BW - 10) / 2, y + 352, n, 14, 'middle')
for i, (cap, col) in enumerate((('кружки 1–5', PALE), ('треугольники 6–9', BLUE), ('доп 10–19 (в А и Б разные)', ORANGE), ('трудные 20–22', RED))):
    o.append(f'<rect x="{110 + i * 330}" y="{y + 366}" width="16" height="16" fill="{col}"/>'); t(134 + i * 330, y + 379, cap, 14, fill=MUTED)

# 5. выводы
y = 1845; card(60, y, 1480, 330)
t(84, y + 36, 'ЧТО ИЗ ЭТОГО СЛЕДУЕТ', 15, fill=MUTED, weight='bold')
V = [('Уровень угадан, траектория — нет.', f'Обязательную часть класс взял на {obyaz_med:.0f}% по медиане, но после кружков пошёл закреплять треугольники, а не в допзадачи: их взято {dop}%.'),
     ('Разброс вырос — ценой времени.', 'Много пунктов в базовых задачах развели класс шире, чем 15.09, но съели урок у всех: хвост листка уезжает на следующее занятие.'),
     ('Место в классе от темы к теме почти не держится.', f'Связь между листками {c1:.2f}, {c2:.2f}, {c3:.2f}. Один замер ничего не говорит о ребёнке; устойчивы только края.'.replace('0.', '0,')),
     ('Края устойчивы.', f"Сверху на всех трёх — {', '.join(short(r['imya']) for r in verh) or 'никто'}; снизу на всех трёх — {', '.join(short(r['imya']) for r in niz)}.")]
for i, (b, s) in enumerate(V):
    yy = y + 76 + i * 62
    o.append(f'<circle cx="92" cy="{yy - 5}" r="5" fill="{ORANGE}"/>'); t(108, yy, b, 17, weight='bold')
    t(108, yy + 24, s, 16, fill=MUTED)
t(60, 2210, 'Данные: SDACHA-15-09_*.csv, SDACHA-22-09_podschety.csv, RAZMETKA-22-09.jsonl; свод — svod_4chasa.py. '
    'Без поправки за кружки на 22.09 Марк Ю. был бы последним, Петр Б. — третьим с конца, Ярослав Л. — в середине.', 13, fill=MUTED)

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="2235" viewBox="0 0 {W} 2235" role="img">'
       f'<title>7И · 15 и 22 сентября · как устроен класс за 4 часа</title><rect width="100%" height="100%" fill="{BG}"/>'
       + ''.join(o) + '</svg>')
(H / 'INFOGRAFIKA-4-chasa.svg').write_text(svg, encoding='utf-8')
cairosvg.svg2png(bytestring=svg.encode(), write_to=str(H / 'INFOGRAFIKA-4-chasa.png'), output_width=2100)
print('ok', len(verh), len(niz), len(skachut), round(c1, 2), round(c2, 2), round(c3, 2), dop, obyaz_med)
