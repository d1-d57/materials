# -*- coding: utf-8 -*-
"""Контрольная 6.10 (7И), v2 по замечаниям владельца 05.10 22:21: вёрстка — общий генератор listok_gen (машина листка),
○ — задачи для всех (по 1 баллу за пункт), ◇ — по желанию, лесенкой до «гроба» (баллы у задачи).
Поля ответа — блоки и строки генератора; места под таблицы — пустые поля без подсказки, сколько строк.
Ключ — kr_kluch.py (перебор, asserts). Сборка: python3 kontrolnaya_06-10_dannye.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from listok_gen import document, to_pdf, fit_report, task
P = {'А': dict(g=7, t=12, x3=3, a=17, b=52, tot=28, ch=9, fo=6, no=5, T=7, after='БКСК', before='КБКБ', top='белой',
               S=12, carp=71, inc=75, d1=6, d2=10, st='четырёх', pol=8),
     'Б': dict(g=6, t=15, x3=4, a=23, b=64, tot=30, ch=11, fo=7, no=4, T=8, after='БСБС', before='СБКБ', top='красной',
               S=13, carp=74, inc=84, d1=4, d2=6, st='пяти', pol=9)}
def pl(n, a, b, c): return a if n % 10 == 1 and n % 100 != 11 else (b if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14 else c)
META = dict(title='Контрольная', date='6 октября', klass='7И')
MON = ('<svg viewBox="0 0 60 64" style="width:13mm;height:14mm;flex:none" role="img" aria-label="одноглазое чудище">'
       '<path d="M8 58 Q4 30 14 18 L10 4 L20 14 Q30 8 40 14 L50 4 L46 18 Q56 30 52 58 L46 52 L40 60 L34 52 L28 60 L22 52 L16 60 L12 52 Z" fill="#fff" stroke="#1d1d1b" stroke-width="2"/>'
       '<circle cx="30" cy="30" r="9" fill="#fff" stroke="#1d1d1b" stroke-width="2"/><circle cx="32" cy="31" r="3.6" fill="#1d1d1b"/>'
       '<path d="M20 45 Q30 51 40 45" fill="none" stroke="#1d1d1b" stroke-width="2"/></svg>')
STOP = ('<div class="stop">' + MON + '<div><b>Стоп. Прежде чем сдать — проверьте себя.</b> Баллов это не даёт, но спасает их. '
        'Ответ «сколько чисел от … до …» проверьте на маленьком случае: от 5 до 5 — одно число, а что даёт ваше выражение? '
        'В переборе: по какому правилу вы выписывали, нет ли одного и того же дважды, не кончился ли список раньше времени?</div></div>')
KB = lambda lab, h: (f'<div class="full fk" style="height:{h}mm"><span class="lb">{lab[0]}</span><div></div>'
                     f'<div class="kb"><span>{lab[1]}</span></div></div>')
def items(v):
    p = P[v]
    return [
     dict(mark='○', num=1, text=f"Петя едет в {p['g']}-м вагоне, если считать от головы поезда, и в {p['t']}-м, если считать от хвоста. Нарисуйте схему. (а)&nbsp;Сколько вагонов в поезде? (б)&nbsp;Вася едет в {p['x3']}-м вагоне от хвоста. Какой это вагон от головы?", block=['а', 'б']),
     dict(mark='○', num=2, text=f"Сколько среди чисел от {p['a']} до {p['b']} (а)&nbsp;чётных; (б)&nbsp;делящихся на 3? Запишите ответ разностью: «сколько таких от 1 до {p['b']}» минус «сколько таких от 1 до …».", block=['а', 'б']),
     dict(mark='○', num=3, text=f"В классе {p['tot']} человек: {p['ch']} ходят только в шахматный кружок, {p['fo']} — только на футбол, {p['no']} никуда не ходят, остальные — и туда и туда. Нарисуйте полосу из {p['tot']} человек и разрежьте её на куски. Сколько человек (а)&nbsp;ходят на футбол; (б)&nbsp;ходят и туда, и туда?", block=['а', 'б']),
     dict(mark='○', num=4, text=f"Число {p['T']} раскладываем в сумму слагаемых, каждое из которых равно 1, 2 или 3; порядок не важен (3+2+2 и 2+3+2 — одно разложение). (а)&nbsp;Придумайте, на какие группы их разбить, нарисуйте таблицу и выпишите в неё все разложения. (б)&nbsp;Сколько их?", block=None, _kb=('аб', 31)),
     dict(mark='○', num=5, text=f"Флаг — четыре горизонтальные полосы, каждая белая (Б), красная (К) или синяя (С), соседние полосы разного цвета; записываем его буквами сверху вниз. Все флаги выписаны в словарном порядке: по верхней полосе (Б, К, С), при одинаковой верхней — по второй, и так далее: БКБК, БКБС, БКСБ, … (а)&nbsp;Какой флаг идёт сразу после {p['after']}? (б)&nbsp;Какой стоит прямо перед {p['before']}? (в)&nbsp;Сколько флагов с {p['top']} верхней полосой?", block=['а', 'б', 'в']),
     dict(mark='○', num=6, text=f"Набираем {p['S']} рублей монетами по 1, 2 и 5 рублей. Вася рассуждает: «Перебираю по числу пятёрок. Если на двушки и рубли осталось m рублей и в них помещается q двушек, то двушек можно взять от 0 до q — это q способов. Остаётся сложить». (а)&nbsp;Сколько способов насчитает Вася? (б)&nbsp;В чём его ошибка? (в)&nbsp;Сколько способов на самом деле? Нарисуйте таблицу.", block=['а'], rows=[dict(h=8, lab='б')], _kb=('в', 22)),
     dict(mark='△', num=7, text=f"<i>2 б.</i> Саша учится с понедельника по пятницу. Он приходит к началу первого урока и после последнего сразу идёт домой. На каждом уроке он съедает 1 карамельку, на каждой перемене между уроками — 2. За неделю в школе он съел {p['carp']} {pl(p['carp'], 'карамельку', 'карамельки', 'карамелек')}. Сколько у Саши уроков в неделю?", block=['']),
     dict(mark='△', num=8, text=f"<i>2 б.</i> Стоит очередь. В каждый промежуток между соседями влез ещё один человек, потом снова в каждый промежуток между соседями — ещё по человеку. Всего очередь выросла на {p['inc']} {pl(p['inc'], 'человека', 'человека', 'человек')}. Сколько людей было в очереди сначала?", block=['']),
     dict(mark='△', num=9, text=f"<i>3 б.</i> Сколько чисел от 1 до 1000 не делятся ни на {p['d1']}, ни на {p['d2']}?", block=['']),
     dict(mark='△', num=10, text=f"<i>3 б.</i> Флаги из {p['st']} полос, как в задаче 5, но вдобавок верхняя и нижняя полосы тоже разного цвета. Сколько таких флагов?", block=['']),
     dict(mark='△', num=11, text=f"<i>4 б.</i> В клетки полоски 1×{p['pol']} записывают числа 1, 2, …, {p['pol']}: сначала 1 — в любую клетку, затем 2 — в соседнюю с ней, затем 3 — в клетку, соседнюю с одной из уже занятых, и так далее. Сколькими способами это можно сделать?", block=['']),
    ]
X = ('body{font-size:10.4pt;line-height:1.24}.page{--abw:21mm;height:281mm;--rowh:6.4mm}.ab.one .r{height:7.5mm}.z{margin-bottom:2.8mm}.fio{margin-bottom:2.5mm}'
     '.ab .r,.ab.one .r{grid-template-columns:4mm 1fr}.ab.one .r{grid-template-columns:1fr}.ab .s,.full .s{display:none}.full{grid-template-columns:1fr}'
     '.fk{position:relative}.kb{position:absolute;right:-1px;bottom:-1px;width:21mm;height:7.5mm;border:1px solid #1d1d1b;background:#fff}.kb span{font-size:8.5pt;padding:1px 0 0 1.2mm;display:block}'
     '.stop{clear:left;display:flex;gap:3mm;align-items:center;border:1.4px dashed #1d1d1b;border-radius:2mm;padding:1.2mm 2.5mm;margin:2mm 0 2.4mm;font-size:9.3pt;line-height:1.22}'
     '.n{font-family:"Liberation Sans","DejaVu Sans",sans-serif}.sec{display:none}')
def build(v):
    Z = items(v)
    for z in Z:
        z.pop('_kb', None)
    h = document(META, v, [dict(heading='', items=Z)], X)
    for z0 in items(v):
        if '_kb' in z0:
            lab, hh = z0['_kb']
            z = {k: x for k, x in z0.items() if k != '_kb'}
            t = task(z); assert h.count(t) == 1
            h = h.replace(t, t[:-6] + KB(lab if len(lab) == 2 else ('', lab), hh) + '</div>')
    t7 = task(Z[6]); assert h.count(t7) == 1
    return h.replace(t7, STOP + t7)
if __name__ == '__main__':
    outs = []
    for v, f in (('А', 'A'), ('Б', 'B')):
        p = f'{HERE}/out/KONTROLNAYA-06-10-{f}.html'; open(p, 'w', encoding='utf-8').write(build(v)); outs.append(p)
    to_pdf(outs)
    for p in outs: print(os.path.basename(p), 'перелив, мм:', fit_report(p))
