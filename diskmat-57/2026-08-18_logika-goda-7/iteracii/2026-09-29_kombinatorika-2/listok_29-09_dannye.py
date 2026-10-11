# -*- coding: utf-8 -*-
"""Данные листка «Комбинаторика 2», спецмат 7И, 29.09 (Р196–Р199). Сборка: python3 listok_29-09_dannye.py
Условия и ответы кружков/треугольников — listok4.py → out/listok4.json; ромбы и граф карты — romby5.py → out/romby5.json.
"""
import json, os, sys
import pathlib as _pl
_H = _pl.Path(__file__).resolve().parent
sys.path.insert(0, str(next(p / 'mashina-listka' for p in _H.parents if (p / 'mashina-listka').is_dir())))
from listok_gen import shen, map_svg, document, to_pdf, fit_report
HERE = os.path.dirname(os.path.abspath(__file__))
L0 = json.load(open(f'{HERE}/out/listok4.json')); R = json.load(open(f'{HERE}/out/romby5.json'))
T = {t[0]: t for t in R['T']}; ORDER = R['ORDER']; STARS = set(R['STARS'])
META = dict(title='Комбинаторика 2', date='29 сентября', klass='7И')
num = lambda v, t: 9 + ORDER[v].index(t)

def ostrova(cols, rows, cell, pid):
    """Островки по Шеню (Л1 №10): прямоугольник, раздвинутый пустыми рядами и столбцами."""
    cs, x = {}, 0
    for i, w in enumerate(cols):
        for _ in range(w): cs[x] = i; x += 1
        x += 1
    rs, y = {}, 0
    for i, h in enumerate(rows):
        for _ in range(h): rs[y] = i; y += 1
        y += 1
    return shen(y - 1, x - 1, lambda r, c: r in rs and c in cs, cell=cell, pid=pid)
def pic_o2(v):
    z = [z for z in L0['V'][v] if z['n'] == 2][0]; (_, n, k), (_, a, b, c, w), (_, oc, orr) = z['pic']
    wid = (n + 2) + (a + 2) + (sum(oc) + len(oc) + 1)
    cell = min(3.4, 108 / wid)
    o_r, o_c = 1, n - k - 1                          # дырка сдвинута к углу (Р197)
    return [shen(n, n, lambda r, cc: not (o_r <= r < o_r + k and o_c <= cc < o_c + k), cell=cell, pid=f'o2a{v}'),
            shen(b, a, lambda r, cc: not (r < w and cc >= a - c), cell=cell, pid=f'o2b{v}'),
            ostrova(oc, orr, cell, f'o2v{v}')]
def pic_domino(v):
    S = set(); ring = lambda r0, c0: {(r0 + i, c0 + j) for i in range(3) for j in range(3)} - {(r0 + 1, c0 + 1)}
    for r0, c0 in ((0, 0), (0, 5), (5, 0), (5, 5)): S |= ring(r0, c0)
    for c in (3, 4): S.add((1, c)); S.add((6, c))
    for r in (3, 4): S.add((r, 1)); S.add((r, 6))
    return [shen(8, 8, lambda r, c: (r, c) in S, cell=4.0, pid=f'dm{v}')]

def obyazatelnye(v):
    Z = {z['n']: z for z in L0['V'][v]}
    return [
        dict(mark='○', num=1, text=Z[1]['t'], block=None, rows=[dict(h=8)]),
        dict(mark='○', num=2, text=Z[2]['t'], block=None, ugol=True, pics=pic_o2(v), pic_caps=['а', 'б', 'в'], strip=['а', 'б', 'в']),
        dict(mark='○', num=3, text=Z[3]['t'], block=['а', 'б', 'в']),
        dict(mark='○', num=4, text=Z[4]['t'], block=['а', 'б']),
        dict(mark='○', num=5, text=Z[5]['t'], block=None, rows=[dict(h=30)]),
        dict(mark='△', num=6, text=Z[6]['t'], block=None, strip=['']),
        dict(mark='△', num=7, text=Z[7]['t'], block=None, strip=['']),
        dict(mark='△', num=8, text=Z[8]['t'], block=None, strip=[''], na_vsyu=True),
    ]
def dopolnitelnye(v):
    out = []
    for t in ORDER[v]:
        _, _, txt, ps = T[t]
        if t == 'kings':
            a, b = R['KINGS'][v][0][0], R['KINGS'][v][1][0]
            txt = f"Сколькими способами можно поставить белого и чёрного королей так, чтобы они не били друг друга, на доску (а) {a}×{a}; (б) {b}×{b}?"
        z = dict(mark='★' if t in STARS else '', num=num(v, t), text=txt, block=[l for l, _, _ in ps])
        if t == 'domino': z.update(pics=pic_domino(v), pics_float=True)
        # «выпишите все / приведите все» — ребёнок не знает, сколько ответов: поле во всю ширину на две строки (Р206)
        if t in ('orehi', 'samoopis'): z.update(block=None, rows=[dict(h=15)])
        out.append(z)
    return out

# ---- карта: координаты (мм) на колонке 63 × MH; граф — из romby5 (у каждой клетки ровно один выход вверх) ----
MW, MH = 63.0, 176.0
cx = lambda i: 5.6 + i * 8.63
cy = lambda r: 8.5 + (9.0 - r) * 13.2
POS = {'globus': [(0, 1.0), (0, 2.0), (0.15, 3.0)], 'klassy': [(1.55, 1.3)],
       'kings': [(3, 1.5), (3, 2.7)], 'domino': [(4.5, 1.3), (4.5, 2.3)], 'kayuty': [(6, 1.0), (6, 2.0)],
       'robin': [(1.05, 4.05), (1.65, 5.05)], 'uravn': [(2.85, 6.15), (2.85, 7.15)],
       'del235': [(5.25, 3.45), (4.75, 4.75)]}
CAMP = (3, 0.0); PEAK = (3, 8.2)
STAR = [(0.5, 8.65), (1.95, 9.08), (4.05, 9.08), (5.5, 8.65)]
KR = [(0.55, -2.95), (1.35, -2.45), (1.1, -1.6), (1.8, -1.05), (2.35, -0.45)]
TR = [(5.45, -2.9), (4.9, -2.0), (4.1, -1.05)]
BEND = {('globus:в', 'robin:а'): .08, ('klassy:', 'robin:а'): 0, ('kings:б', 'uravn:а'): 0, ('robin:б', 'uravn:а'): .06,
        ('domino:б', 'del235:а'): -.05, ('kayuty:б', 'del235:а'): -.08, ('uravn:б', 'PEAK'): 0, ('del235:б', 'PEAK'): .36}
def karta(v):
    nodes = {}; key = lambda c: c if c.split(':')[1] else c
    for t, ps in POS.items():
        for (l, _, _), p in zip(T[t][3], ps):
            c = f'{t}:{l}'
            sym = 'skull' if c in R['SKULL'] else 'coin' if c in R['COIN'] else None
            nodes[c] = dict(x=cx(p[0]), y=cy(p[1]), kind='romb', label=f'{num(v, t)}{l}', sym=sym)
    stars = [t for t in ORDER[v] if t in STARS]
    for t, p in zip(stars, STAR): nodes[f'{t}:'] = dict(x=cx(p[0]), y=cy(p[1]), kind='romb', label=str(num(v, t)), sym='star')
    for i, p in enumerate(KR): nodes[f'o{i+1}'] = dict(x=cx(p[0]), y=cy(p[1]), kind='circ', label=str(i + 1))
    for i, p in enumerate(TR): nodes[f't{i+6}'] = dict(x=cx(p[0]), y=cy(p[1]), kind='tri', label=str(i + 6))
    E = []
    for a, b in R['OUT'].items(): E.append((a, b, BEND.get((a, b), 0)))
    for t, bd in zip(R['ENTRY'], (.12, .05, 0, -.05, -.12)): E.append(('CAMP', f'{t}:{T[t][3][0][0]}', bd))
    for t in stars: E.append(('PEAK', f'{t}:', 0))
    seqK = [f'o{i}' for i in range(1, 6)] + ['CAMP']; seqT = ['t6', 't7', 't8', 'CAMP']
    for seq in (seqK, seqT):
        for a, b in zip(seq, seq[1:]): E.append((a, b, .1))
    return map_svg(dict(W=MW, H=MH, camp=(cx(CAMP[0]), cy(CAMP[1])), peak=(cx(PEAK[0]), cy(PEAK[1])), nodes=nodes, edges=E,
                        starts=[('o1', 'left'), ('t6', 'right')], seed=7, checkpoints=False))
def RULES(v):
    t3 = next(t for t in ORDER[v] if t not in STARS and len(T[t][3]) == 3)          # пример — настоящий ромб «…в» ЭТОГО варианта
    return f'''<div class="rules"><ul>
<li>Начни с любой тропы, ○ или △. Сдал задачу — закрась её значок. Закрыл всю тропу — ты в лагере.</li>
<li>Из лагеря иди вверх по линиям: ромб можно сдавать, если закрашен ромб под ним (или лагерь). «{num(v, t3)}в» — пункт (в) задачи {num(v, t3)}.</li>
<li>Дошёл до вершины — открыты ромбы <span class="gl">★</span>.</li>
<li>Жизнь одна. Ошибка в ромбе <span class="gl">☠</span> — минус жизнь; без жизни его не сдать. Ромб <span class="gl" style="color:#5c5a55">●</span> — плюс жизнь.</li>
</ul></div>'''


def kanon():
    """Канонические пункты листка по вариантам — вход для svod.py и razmetka.py. Не из разметки, а из данных листка."""
    K = {}
    for v in ('А', 'Б'):
        rows = []
        for z in sorted(L0['V'][v], key=lambda z: z['n']):
            for l, a in z['p']:
                rows.append(dict(punkt=f"{z['n']}{l}", razdel=z['m'], otvet=a, kletka=('o' if z['m'] == '○' else 't') + str(z['n'])))
        for t in ORDER[v]:
            for i, (l, a, d) in enumerate(T[t][3]):
                if t == 'kings': a = R['KINGS'][v][i][1]
                rows.append(dict(punkt=f"{num(v, t)}{l}", razdel='★' if t in STARS else 'доп', otvet=a, kletka=f'{t}:{l}', trudnost=d))
        K[v] = rows
    return dict(punkty=K, karta=dict(OUT=R['OUT'], ENTRY=[f"{t}:{T[t][3][0][0]}" for t in R['ENTRY']], SKULL=R['SKULL'], COIN=R['COIN'],
                baza={'○': [f'o{i}' for i in range(1, 6)], '△': [f't{i}' for i in range(6, 9)]}))

def build(v):
    pages = [dict(heading='Обязательные задачи', items=obyazatelnye(v), side=f'<div class="map">{karta(v)}</div>{RULES(v)}', footer='Ответ записывайте выражением — так, как вы считали.'),
             dict(heading='Дополнительные задачи', items=dopolnitelnye(v), abw='64mm', rowh='8mm')]
    return document(META, v, pages)

if __name__ == '__main__':
    outs = []
    for v, f in (('А', 'A'), ('Б', 'B')):
        p = f'{HERE}/out/LISTOK-29-09-{f}.html'; open(p, 'w').write(build(v)); outs.append(p)
    to_pdf(outs)
    json.dump(kanon(), open(f'{HERE}/out/kanon.json', 'w'), ensure_ascii=False, indent=1)
    for p in outs: print(os.path.basename(p), 'перелив по страницам, мм:', fit_report(p))
