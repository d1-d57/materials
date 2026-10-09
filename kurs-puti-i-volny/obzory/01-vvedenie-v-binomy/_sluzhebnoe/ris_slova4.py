"""Рисунок ris/slova4.svg: все 16 слов длины 4, по столбцам — число единиц 0..4.
Запуск из папки _sluzhebnoe: python3 ris_slova4.py"""
from itertools import product
import os
H = os.path.dirname(os.path.abspath(__file__))
cols = {k: [w for w in sorted(product((1, 0), repeat=4), reverse=True) if sum(w) == k] for k in range(5)}
CS, G, CW, RH, TOP = 15, 3, 88, 23, 34
W = 5 * CW; Hh = TOP + 6 * RH + 34
o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" role="img" aria-label="Все шестнадцать слов длины 4 из нулей и единиц, разложенные в пять столбцов по числу единиц: в столбцах 1, 4, 6, 4 и 1 слово" style="color:var(--text,#222)">' % (W, Hh, W)]
for k in range(5):
    cx = k * CW + CW / 2
    o.append('<text x="%.1f" y="22" text-anchor="middle" font-size="19" font-weight="600" fill="currentColor" font-family="var(--sans,sans-serif)">%d</text>' % (cx, k))
    for r, w in enumerate(cols[k]):
        x0 = cx - (4 * CS + 3 * G) / 2; y = TOP + r * RH
        for i, b in enumerate(w):
            o.append('<rect x="%.1f" y="%d" width="%d" height="%d" rx="2" fill="%s" stroke="currentColor" stroke-width="1.2"/>' % (x0 + i * (CS + G), y, CS, CS, 'currentColor' if b else 'none'))
    o.append('<text x="%.1f" y="%d" text-anchor="middle" font-size="19" font-weight="400" fill="currentColor" font-family="var(--sans,sans-serif)">%d</text>' % (cx, Hh - 8, len(cols[k])))
o.append('</svg>')
open(os.path.join(H, 'ris', 'slova4.svg'), 'w').write('\n'.join(o))
print('slova4.svg:', [len(cols[k]) for k in range(5)])
