# -*- coding: utf-8 -*-
"""Мини-листок к уроку 6.10 (7И): 6 задач лесенкой для тех, кто уверен в контрольной и сидит на задних партах.
Те же идеи, что в контрольной, но задачи другие: перебор таблицей, ошибка «от нуля», разность, два списка,
словарный порядок «что после / что перед», дополнение плюс два списка. Пол-листа (Р209): на A4 вариант А сверху, Б снизу.
Ключ — перебором ниже, в assert. Сборка: python3 minilistok_06-10_dannye.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from listok_gen import polulist, to_pdf, fit_report, shpargalka

P = {'А': dict(n3=10, s=8, mash=28, D=300, N=200, k=20, after=189, before=345, d=('1', '2')),
     'Б': dict(n3=11, s=9, mash=36, D=270, N=300, k=30, after=289, before=456, d=('0', '5'))}
META = dict(title='Умный перебор', date='6 октября', klass='7И')

def items(v):
    p = P[v]
    return [
     dict(mark='○', num=1, text=f"Сколькими способами можно разложить число {p['n3']} в сумму трёх натуральных слагаемых? Порядок слагаемых не важен.", block=['']),
     dict(mark='○', num=2, text=f"Маша считает трёхзначные числа с суммой цифр {p['s']}: «Первая цифра <i>a</i> — от 1 до {p['s']}. Вторая — от 1 до {p['s']} − <i>a</i>, третья по ней определяется: это {p['s']} − <i>a</i> чисел. Всего {p['mash']}». (а)&nbsp;В чём ошибка Маши? (б)&nbsp;Сколько таких чисел на самом деле?", block=['б'], rows=[dict(h=8, lab='а')]),
     dict(mark='○', num=3, text=f"Страницы книги пронумерованы подряд, начиная с 1. На всю нумерацию ушло {p['D']} цифр. Сколько страниц в книге?", block=['']),
     dict(mark='△', num=4, text=f"Сколько чисел от 1 до {p['N']} не делятся ни на 4, ни на 6?", block=['']),
     dict(mark='△', num=5, text=f"Все трёхзначные числа, цифры которых идут строго по возрастанию (как 147), выписали в порядке возрастания. (а)&nbsp;Какое число стоит {p['k']}-м? (б)&nbsp;Какое идёт сразу после {p['after']}? (в)&nbsp;Какое стоит прямо перед {p['before']}?", block=['а', 'б', 'в']),
     dict(mark='△', num=6, text=f"Сколько трёхзначных чисел, в записи которых есть и цифра {p['d'][0]}, и цифра {p['d'][1]}?", block=['']),
    ]

# ---------- ключ: перебор ----------
def kluch(v):
    p = P[v]; T = range(100, 1000); ds = lambda n: sum(map(int, str(n)))
    r1 = sum(1 for a in range(1, p['n3']) for b in range(a, p['n3']) for c in range(b, p['n3']) if a + b + c == p['n3'])
    r2 = sum(1 for n in T if ds(n) == p['s']); assert sum(p['s'] - a for a in range(1, p['s'] + 1)) == p['mash']
    s, r3 = 0, None
    for n in range(1, 10000):
        s += len(str(n))
        if s == p['D']: r3 = n; break
    r4 = sum(1 for n in range(1, p['N'] + 1) if n % 4 and n % 6)
    inc = [n for n in T if str(n)[0] < str(n)[1] < str(n)[2]]
    r5 = (inc[p['k'] - 1], inc[inc.index(p['after']) + 1], inc[inc.index(p['before']) - 1])
    r6 = sum(1 for n in T if p['d'][0] in str(n) and p['d'][1] in str(n))
    return r1, r2, r3, r4, r5, r6
assert kluch('А') == (8, 36, 136, 133, (157, 234, 289), 52)
assert kluch('Б') == (10, 45, 126, 200, (235, 345, 389), 35)
# решения, которые идут в шпаргалку
assert 9 + 180 + 3 * 37 == 300 and 9 + 180 + 3 * 27 == 270
assert 200 - (50 + 33 - 16) == 133 and 300 - (75 + 50 - 25) == 200
assert 900 - (648 + 648 - 448) == 52 and 900 - (729 + 648 - 512) == 35

X = '.sec{display:none}'
if __name__ == '__main__':
    p = f'{HERE}/out/MINILISTOK-06-10.html'
    open(p, 'w', encoding='utf-8').write(polulist(META, [('А', dict(heading='', items=items('А'))), ('Б', dict(heading='', items=items('Б')))], X))
    A, B = kluch('А'), kluch('Б')
    f5 = lambda t: ', '.join(map(str, t))
    rows = [('1', A[0], B[0]), ('2', A[1], B[1]), ('3', A[2], B[2]),
            ('4', A[3], B[3]), ('5', f5(A[4]), f5(B[4])), ('6', A[5], B[5])]
    s = f'{HERE}/out/SHPARGALKA-MINILISTOK-06-10.html'
    open(s, 'w', encoding='utf-8').write(shpargalka('Мини-листок · ответы', '6 октября', [('Мини-листок', ['№', 'А', 'Б'], rows, ['3'])]))
    to_pdf([p, s])
    print('перелив, мм:', fit_report(p))
