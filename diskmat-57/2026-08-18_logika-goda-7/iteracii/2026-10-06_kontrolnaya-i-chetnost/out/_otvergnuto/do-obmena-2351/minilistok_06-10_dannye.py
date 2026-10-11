# -*- coding: utf-8 -*-
"""Мини-листок к уроку 6.10 (7И), v2 по замечаниям владельца 05.10 23:43: для тех, кто уверен в контрольной (задние парты).
8 задач лесенкой (страницы и «ни на 4, ни на 6» сняты — не влезли в пол-листа); счётные задачи на идеи урока + задачи на идею (флаги с переворотом, кузнечик, полоска, чётная сумма).
Не повторяет ошибку из ○6 контрольной (там «от нуля»; здесь ошибка Пети — порядок не важен).
Формат: пол-листа (Р209), на A4 вариант А сверху, Б снизу. Ключ — перебором ниже, в assert.
OBMEN=True — вариант с обменом: △7 (возрастающие цифры) уходит в контрольную, сюда приходит полоска 1×n из △11 КР.
Сборка: python3 minilistok_06-10_dannye.py"""
import os, sys, html
from itertools import product
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from listok_gen import polulist, to_pdf, fit_report, shpargalka

P = {'А': dict(n3=10, m=6, pol=8, D=300, fc=3, st=8, k=20, after=189, before=345, N=200, ev='трёхзначных', d=('1', '2'), kp=8),
     'Б': dict(n3=11, m=7, pol=9, D=270, fc=4, st=9, k=30, after=289, before=456, N=300, ev='четырёхзначных', d=('0', '5'), kp=9)}
META = dict(title='Умный перебор', date='6 октября', klass='7И')
CV = {3: 'белая, красная или синяя', 4: 'белая, красная, синяя или зелёная'}

def items(v, obmen=False):
    p = P[v]
    t7 = (dict(mark='△', num=6, text=f"В клетки полоски 1×{p['kp']} записывают числа 1, 2, …, {p['kp']}: сначала 1 — в любую клетку, затем 2 — в соседнюю с ней, затем 3 — в клетку, соседнюю с одной из уже занятых, и так далее. Сколькими способами это можно сделать?", block=[''])
          if obmen else
          dict(mark='△', num=6, text=f"Все трёхзначные числа, цифры которых идут строго по возрастанию (как 147), выписали в порядке возрастания. (а)&nbsp;Какое число стоит {p['k']}-м? (б)&nbsp;Какое идёт сразу после {p['after']}? (в)&nbsp;Какое стоит прямо перед {p['before']}?", block=None, strip=['а', 'б', 'в']))
    return [
     dict(mark='○', num=1, text=f"Сколькими способами можно разложить число {p['n3']} в сумму трёх натуральных слагаемых? Порядок слагаемых не важен.", block=['']),
     dict(mark='○', num=2, text=f"Из {p['m']} учеников выбирают двух дежурных. Петя рассуждает: «Первого дежурного можно выбрать {p['m']} способами, второго — {p['m'] - 1}, всего {p['m'] * (p['m'] - 1)}». (а)&nbsp;В чём ошибка Пети? (б)&nbsp;Сколько способов на самом деле?", block=['б'], rows=[dict(h=8, lab='а')]),
     dict(mark='○', num=3, text=f"Сколько прямоугольников можно найти на клетчатой полоске 1×{p['pol']}? Прямоугольник состоит из целых клеток; квадраты тоже считаются.", block=['']),
     dict(mark='△', num=4, text=f"Флаг — три вертикальные полосы, каждая {CV[p['fc']]}; соседние полосы разного цвета. Флаг можно повесить и задом наперёд, поэтому флаги БКС и СКБ одинаковые. Сколько всего разных флагов?", block=['']),
     dict(mark='△', num=5, text=f"Кузнечик поднимается по лестнице, прыгая каждый раз на одну или на две ступеньки вверх. Сколькими способами он может подняться с пола на {p['st']}-ю ступеньку?", block=['']),
     t7,
     dict(mark='△', num=7, text=f"У скольких {p['ev']} чисел сумма цифр чётная?", block=['']),
     dict(mark='△', num=8, text=f"Сколько трёхзначных чисел, в записи которых есть и цифра {p['d'][0]}, и цифра {p['d'][1]}?", block=['']),
    ]

# ---------- ключ: перебор ----------
def kluch(v, obmen=False):
    p = P[v]; T = range(100, 1000); ds = lambda n: sum(map(int, str(n)))
    r1 = sum(1 for a in range(1, p['n3']) for b in range(a, p['n3']) for c in range(b, p['n3']) if a + b + c == p['n3'])
    r2 = len({frozenset((i, j)) for i in range(p['m']) for j in range(p['m']) if i != j})
    r3 = sum(1 for i in range(p['pol']) for j in range(i, p['pol']))
    s, r4 = 0, None
    for n in range(1, 10000):
        s += len(str(n))
        if s == p['D']: r4 = n; break
    fs = {f for f in product(range(p['fc']), repeat=3) if f[0] != f[1] != f[2]}
    r5 = len({min(f, f[::-1]) for f in fs})
    w = [1, 1]
    for _ in range(p['st'] - 1): w.append(w[-1] + w[-2])
    r6 = w[p['st']]
    if obmen:
        r7 = 2 ** (p['kp'] - 1)
    else:
        inc = [n for n in T if str(n)[0] < str(n)[1] < str(n)[2]]
        r7 = (inc[p['k'] - 1], inc[inc.index(p['after']) + 1], inc[inc.index(p['before']) - 1])
    r8 = sum(1 for n in range(1, p['N'] + 1) if n % 4 and n % 6)
    lo = 100 if p['ev'] == 'трёхзначных' else 1000
    r9 = sum(1 for n in range(lo, 10 * lo) if ds(n) % 2 == 0)
    r10 = sum(1 for n in T if p['d'][0] in str(n) and p['d'][1] in str(n))
    return r1, r2, r3, r5, r6, r7, r9, r10
assert kluch('А') == (8, 15, 36, 9, 34, (157, 234, 289), 450, 52)
assert kluch('Б') == (10, 21, 45, 24, 55, (235, 345, 389), 4500, 35)
# полоска из КР: проверка формулы 2^(n-1) перебором для малых n
def polos(n):
    def go(lo, hi):
        if hi - lo + 1 == n: return 1
        return (go(lo - 1, hi) if lo > 0 else 0) + (go(lo, hi + 1) if hi < n - 1 else 0)
    return sum(go(i, i) for i in range(n))
assert [polos(n) for n in range(1, 8)] == [2 ** (n - 1) for n in range(1, 8)]
# числа из решений (в чат владельцу)
assert 900 - (648 + 648 - 448) == 52 and 900 - (729 + 648 - 512) == 35
assert (12 - 6) // 2 + 6 == 9 and (36 - 12) // 2 + 12 == 24 and 9 * 8 // 2 == 36 and 10 * 9 // 2 == 45

X = ('.sec{display:none}.page{--abw:23mm;--rowh:6.2mm}.fio{margin:1.5mm 0 3mm}.z{margin-bottom:2.6mm;display:flow-root}'
     '.ab .r{grid-template-columns:3.5mm 1fr 8mm}.ab.one .r{grid-template-columns:1fr 8mm}.strip .c{grid-template-columns:4mm 1fr 8mm}')
def build(obmen=False):
    return polulist(META, [(v, dict(heading='', items=items(v, obmen))) for v in ('А', 'Б')], X)
if __name__ == '__main__':
    for ob, suf in ((False, ''), (True, '-OBMEN')):
        p = f'{HERE}/out/MINILISTOK-06-10{suf}.html'; open(p, 'w', encoding='utf-8').write(build(ob))
        A, B = kluch('А', ob), kluch('Б', ob)
        f = lambda x: ', '.join(map(str, x)) if isinstance(x, tuple) else x
        rows = [(str(i + 1), f(a), f(b)) for i, (a, b) in enumerate(zip(A, B))]
        s = f'{HERE}/out/SHPARGALKA-MINILISTOK-06-10{suf}.html'
        open(s, 'w', encoding='utf-8').write(shpargalka('Мини-листок · ответы', '6 октября', [('Мини-листок', ['№', 'А', 'Б'], rows, ['3'])]))
        to_pdf([p, s])
        print(suf or 'основной', 'перелив, мм:', fit_report(p))
