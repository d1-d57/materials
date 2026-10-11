# -*- coding: utf-8 -*-
"""КР 6.10 (7И): ключ. Каждый ответ — перебором, assert внутри. python3 kr_dannye.py"""
from itertools import product
def parts(n, mx):
    if n == 0: yield (); return
    for k in range(min(n, mx), 0, -1):
        for r in parts(n-k, k): yield (k,)+r
def flags(k, cols='БКС'):
    return [''.join(f) for f in product(cols, repeat=k) if all(f[i]!=f[i+1] for i in range(k-1))]
K = {}
for V, (g, t, x3, a, b, tot, ch, fo, no, T, fr, carp, inc, d1, d2, dash) in {
    'А': (7, 12, 3, 17, 52, 28, 9, 6, 5, 7, 'БКСК', 71, 75, 6, 10, 75),
    'Б': (6, 15, 4, 23, 64, 30, 11, 7, 4, 8, 'БСБС', 74, 84, 4, 6, 57)}.items():
    k = {}
    # 1 поезд: g-й с головы и t-й с хвоста
    n = g + t - 1; k['1а'] = (n, f'{g}+{t}−1'); assert len(range(1, n+1)) == n and n - t + 1 == g
    k['1б'] = (n - x3 + 1, f'{n}−{x3}+1')
    # 2 от a до b
    ev = [m for m in range(a, b+1) if m % 2 == 0]; k['2а'] = (len(ev), f'{b//2}−{(a-1)//2}'); assert len(ev) == b//2 - (a-1)//2
    m3 = [m for m in range(a, b+1) if m % 3 == 0]; k['2б'] = (len(m3), f'{b//3}−{(a-1)//3}'); assert len(m3) == b//3 - (a-1)//3
    # 3 кружки: всего tot, только шахматы ch, только футбол fo, никуда no
    both = tot - no - ch - fo; assert both > 0
    k['3а'] = (tot - no - ch, f'{tot}−{no}−{ch}'); k['3б'] = (both, f'{tot-no-ch}−{fo}')
    # 4 разложения T на слагаемые ≤3
    P = list(parts(T, 3)); k['4а'] = (len(P), 'таблица по числу троек'); k['4_list'] = ['+'.join(map(str, p)) for p in P]
    from collections import Counter; k['4_rows'] = dict(Counter(p.count(3) for p in P))
    # 5 флаги 4 полосы, словарный порядок Б<К<С
    F = sorted(flags(4), key=lambda s: ['БКС'.index(c) for c in s]); assert len(F) == 24
    k['5а'] = (F[F.index(fr)+1], f'после {fr}')
    first = {'А': 'КБКБ', 'Б': 'СБКБ'}[V]; k['5б'] = (F[F.index(first)-1], f'перед {first}')
    top = {'А': 'Б', 'Б': 'К'}[V]; k['5в'] = (sum(f[0] == top for f in F), f'верхняя {top}: 2·2·2')
    # 6 монеты: Вася «двушек от 0 до q — q способов»
    S = {'А': 12, 'Б': 13}[V]
    true = [(f, d) for f in range(S//5+1) for d in range((S-5*f)//2+1)]
    vas = sum((S-5*f)//2 for f in range(S//5+1))
    k['6а'] = (vas, 'у Васи'); k['6в'] = (len(true), ' + '.join(str((S-5*f)//2+1) for f in range(S//5+1)))
    k['6б'] = ('«от 0 до q» — это q+1 вариант, Вася теряет «без двушек» в каждой строке', '')
    # вверх
    L = (carp + 10) // 3; assert 3*L - 10 == carp; k['В1'] = (L, f'({carp}+10):3')
    m0 = inc // 3 + 1; assert 3*m0 - 3 == inc; k['В2'] = (m0, f'{inc}:3+1')
    nn = sum(1 for m in range(1, 1001) if m % d1 and m % d2)
    l = d1*d2//__import__('math').gcd(d1, d2)
    k['В3'] = (nn, f'1000−{1000//d1}−{1000//d2}+{1000//l}'); assert nn == 1000-1000//d1-1000//d2+1000//l
    sF = [f for f in flags({'А': 4, 'Б': 5}[V]) if f[0] != f[-1]]; k['В4'] = (len(sF), f'{len(flags({"А":4,"Б":5}[V]))} всего')
    # В5: монеты 1, 2, 5, 10 — набрать S5 рублей; разрез по десяткам, затем по пятёркам, двушек «от 0 до q» = q+1
    S5 = {'А': 20, 'Б': 21}[V]
    tr = [(t_, f_, d_) for t_ in range(S5//10+1) for f_ in range((S5-10*t_)//5+1) for d_ in range((S5-10*t_-5*f_)//2+1)]
    k['В5'] = (len(tr), 'сумма по строкам (десятки, пятёрки): ' + ' + '.join(str((S5-10*t_-5*f_)//2+1) for t_ in range(S5//10+1) for f_ in range((S5-10*t_)//5+1)))
    K[V] = k
for V in K:
    print('— вариант', V)
    for q, v in K[V].items(): print(' ', q, v)
assert K['А']['1а'][0] == 18 and K['А']['6а'][0] == 10 and K['А']['6в'][0] == 13 and K['Б']['6а'][0] == 11 and K['Б']['6в'][0] == 14
assert K['А']['В5'][0] == 40 and K['Б']['В5'][0] == 43
print('ключ: все asserts прошли')
# --- v2 (06-10 22:40): ◇ переставлены; ◇11 — полоска из листка 29.09 (никто не решил), n = 8 / 9
def poloska(n):
    cnt = 0
    def rec(lo, hi):
        nonlocal cnt
        if hi - lo + 1 == n: cnt += 1; return
        if lo > 0: rec(lo - 1, hi)
        if hi < n - 1: rec(lo, hi + 1)
    for s in range(n): rec(s, s)
    return cnt
assert poloska(8) == 128 and poloska(9) == 256 and poloska(4) == 8
import sys, pathlib as _pl
_H = _pl.Path(__file__).resolve().parent
sys.path.insert(0, str(_H)); sys.path.insert(0, str(next((q / 'mashina-listka' for q in _H.parents if (q / 'mashina-listka').is_dir()), _H)))
from listok_gen import shpargalka
from itertools import product as _pr
_ds = lambda n: sum(map(int, str(n)))
def zero_sum(t): return sum(1 for n in range(100, 1000) if _ds(n) == t and '0' in str(n))
def ni(a, b, c): return sum(1 for n in range(1, 1001) if n % a and n % b and n % c)
def xo(m, n):
    c = 0
    for bits in _pr((0, 1), repeat=m * n):
        g = [bits[i*n:(i+1)*n] for i in range(m)]
        c += all((g[i][j]+g[i+1][j]+g[i][j+1]+g[i+1][j+1]) % 2 == 0 for i in range(m-1) for j in range(n-1))
    return c
assert [xo(3, 3), xo(3, 4), xo(4, 4)] == [2**5, 2**6, 2**7]          # 2^(m+n-1); 8×8 → 2^15, 7×7 → 2^13 по той же формуле
assert zero_sum(6) == 11 == 6 + 6 - 1 and zero_sum(7) == 13 == 7 + 7 - 1
assert ni(6, 10, 15) == 734 and ni(6, 14, 21) == 1000 - 166 - 71 - 47 + 3*23 - 23
assert 28 - 5 == 23 and 30 - 4 == 26
ROWS = [('1а', K['А']['1а'][0], K['Б']['1а'][0]), ('1б', K['А']['1б'][0], K['Б']['1б'][0]),
        ('2а', K['А']['2а'][0], K['Б']['2а'][0]), ('2б', K['А']['2б'][0], K['Б']['2б'][0]),
        ('3а', 28 - 5, 30 - 4), ('3б', K['А']['3б'][0], K['Б']['3б'][0]),
        ('4', 'таблица; троек 2:1 · 1:3 · 0:4 (8)', 'таблица; троек 2:2 · 1:3 · 0:5 (10)'),
        ('5а', K['А']['5а'][0], K['Б']['5а'][0]), ('5б', K['А']['5б'][0], K['Б']['5б'][0]), ('5в', K['А']['5в'][0], K['Б']['5в'][0]),
        ('6а', K['А']['6а'][0], K['Б']['6а'][0]), ('6б', 'от 0 до q — это q+1', 'от 0 до q — это q+1'), ('6в', 'таблица 7+4+2 = 13', 'таблица 7+5+2 = 14'),
        ('△7', zero_sum(6), zero_sum(7)), ('△8', K['А']['В1'][0], K['Б']['В1'][0]), ('△9', ni(6, 10, 15), ni(6, 14, 21)),
        ('△10', K['А']['В4'][0], K['Б']['В4'][0]), ('△11', poloska(8), poloska(9)), ('△12', 2**15, 2**13)]
open(str(_H / 'out' / 'SHPARGALKA-KR-06-10.html'), 'w', encoding='utf-8').write(shpargalka('Контрольная 6.10 — ответы', '7И · 6 октября', [('Контрольная', ['№', 'А', 'Б'], ROWS, ['6в'])]))
print('\n'.join(f'{a:4} {b} | {c}' for a, b, c in ROWS))
