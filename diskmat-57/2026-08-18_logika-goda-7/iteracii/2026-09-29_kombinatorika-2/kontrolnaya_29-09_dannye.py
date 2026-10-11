# -*- coding: utf-8 -*-
"""Контрольная 29.09 (Р195: содержание утверждено, v3). Здесь — только вёрстка через общий генератор.
Формат — пол-листа на человека (Р209): на A4 вариант А сверху, Б снизу, режем и раздаём по вариантам.
Числа и ключ — из kontrolnaya_29-09.py (kontr3.py): перебор внутри. Форма ответа свободная (Р179)."""
import os, sys
import pathlib as _pl
_H = _pl.Path(__file__).resolve().parent
sys.path.insert(0, str(next(p / 'mashina-listka' for p in _H.parents if (p / 'mashina-listka').is_dir())))
HERE = os.path.dirname(os.path.abspath(__file__))
from listok_gen import document, polulist, to_pdf, fit_report
_src = open(f'{HERE}/kontr3.py').read().split('def pole')[0]
_ns = {}; exec(_src, _ns); V, K = _ns['V'], _ns['K']
META = dict(title='Контрольная', date='29 сентября', klass='7И')
def doska(m, n, c=6.0):
    """Доска линиями, а не квадратами: у соседних квадратов стороны накладываются и печатаются толще."""
    L = [f'<line x1="0" y1="{i*c}" x2="{n*c}" y2="{i*c}"/>' for i in range(m + 1)] + [f'<line x1="{j*c}" y1="0" x2="{j*c}" y2="{m*c}"/>' for j in range(n + 1)]
    return (f'<svg viewBox="-.5 -.5 {n*c+1} {m*c+1}" style="width:{n*c+1}mm;height:{m*c+1}mm" role="img" aria-label="клетчатая доска {m} на {n}">'
            f'<g stroke="#1d1d1b" stroke-width=".3" stroke-linecap="square">{"".join(L)}</g></svg>')
def items(v):
    """Правила вёрстки листка (А5, А6): короткий ответ — блок слева, текст справа; картинка справа с обтеканием;
    «выпишите все» — широкое поле, короткий пункт рядом в той же строке."""
    d = V[v]; L = ", ".join(map(str, d['L'][:-1])) + f" и {d['L'][-1]}"; top = max(d['L'])
    return [
        dict(num=1, text=f"Из книги выпала пачка листов. Первая страница пачки имеет номер {d['f']}, последняя — номер {d['l']}. Сколько листов выпало?", block=['']),
        dict(num=2, text=f"Сколько чисел от 1 до {d['N']}<br>(а) делятся на {d['p']}? делятся на {d['q']}? (два числа)<br>(б) не делятся ни на {d['p']}, ни на {d['q']}?", block=['а', 'б']),
        dict(num=3, text=f"Клетчатая доска {d['m']}&thinsp;×&thinsp;{d['n']} клеток.<br>(а) Сколько на ней квадратов любого размера, составленных из целых клеток? Напишите отдельно, сколько квадратов каждого размера.<br>(б) Сколько на ней прямоугольников 1&thinsp;×&thinsp;2 из двух клеток? Напишите отдельно, сколько горизонтальных и сколько вертикальных.",
             block=['а', 'б'], pics=[doska(d['m'], d['n'], 5)], pics_float=True),
        dict(num=4, text=f"Есть семь палочек длиной {L} см. Из трёх палочек можно сложить треугольник, если сумма длин любых двух из них больше длины третьей.<br>(а) Выпишите все тройки палочек, из которых складывается треугольник и в которых самая длинная палочка — {top} см.<br>(б) Сколькими способами можно выбрать из этих семи палочек три так, чтобы сложился треугольник?",
             block=None, strip=['а', 'б'], strip_cols='4fr 1fr', strip_h=16),
    ]
X = 'body{font-size:11.3pt;line-height:1.3}.page{--abw:50mm}.z{margin-bottom:4.2mm}.ab .r{height:9.5mm}.ab.one .r{height:10.5mm}.ab{margin-bottom:3.2mm}'
if __name__ == '__main__':
    h = polulist(META, [(v, dict(heading='', items=items(v))) for v in ('А', 'Б')], X).replace('<div class="sec"></div>', '<div style="height:2.5mm"></div>')
    p = f'{HERE}/out/KONTROLNAYA-29-09.html'; open(p, 'w').write(h); to_pdf([p])
    print('KONTROLNAYA-29-09 (пол-листа: А сверху, Б снизу), перелив половин, мм:', fit_report(p))
    for v in V: print(v, K[v])
