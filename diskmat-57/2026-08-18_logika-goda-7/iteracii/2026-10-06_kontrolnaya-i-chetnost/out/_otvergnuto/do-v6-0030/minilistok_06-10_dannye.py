# -*- coding: utf-8 -*-
"""Мини-листок к уроку 6.10 (7И), v4 по замечаниям владельца 05.10 23:51–23:52: для тех, кто уверен в контрольной (задние парты).
Весь листок уровня △: значков у задач нет, один большой △ у заголовка. 6 задач: три слагаемых, страницы, флаги с ровно одной
белой (синей) полосой — перебор по месту этой полосы, ни на 4, ни на 6, есть обе цифры, полоска 1×n (пришла из △11 КР).
НЕЛЬЗЯ (владелец): C из n по 2, правило произведения с делением пополам, рекуррентные последовательности (Фибоначчи),
ошибка «от нуля» (спойлер ○6 КР). Ошибка «для разбора» допустима только на правило суммы.
Формат: пол-листа (Р209), на A4 вариант А сверху, Б снизу. Ключ — перебором ниже, в assert.
Сборка: python3 minilistok_06-10_dannye.py"""
import os, sys, html
from itertools import product
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from listok_gen import polulist, to_pdf, fit_report, shpargalka

P = {'А': dict(n3=10, D=300, odna=('белая', 0), N=200, d=('1', '2'), kp=8),
     'Б': dict(n3=11, D=270, odna=('синяя', 2), N=300, d=('0', '5'), kp=9)}
META = dict(title='Умный перебор', date='6 октября', klass='7И')

def items(v):
    p = P[v]
    return [
     dict(mark='', num=1, text=f"Сколькими способами можно разложить число {p['n3']} в сумму трёх натуральных слагаемых? Порядок слагаемых не важен.", block=['']),
     dict(mark='', num=2, text=f"Страницы книги пронумерованы подряд, начиная с 1. На всю нумерацию ушло {p['D']} цифр. Сколько страниц в книге?", block=['']),
     dict(mark='', num=3, text=f"Флаг — три горизонтальные полосы, каждая белая, красная или синяя; соседние полосы разного цвета. Сколько существует флагов, у которых ровно одна полоса {p['odna'][0]}?", block=['']),
     dict(mark='', num=4, text=f"Сколько чисел от 1 до {p['N']} не делятся ни на 4, ни на 6?", block=['']),
     dict(mark='', num=5, text=f"Сколько трёхзначных чисел, в записи которых есть и цифра {p['d'][0]}, и цифра {p['d'][1]}?", block=['']),
     dict(mark='', num=6, text=f"В клетки полоски 1×{p['kp']} записывают числа 1, 2, …, {p['kp']}: сначала 1 — в любую клетку, затем 2 — в соседнюю с ней, затем 3 — в клетку, соседнюю с одной из уже занятых, и так далее. Сколькими способами это можно сделать?", block=['']),
    ]

# ---------- ключ: перебор ----------
def kluch(v):
    p = P[v]; T = range(100, 1000)
    r1 = sum(1 for a in range(1, p['n3']) for b in range(a, p['n3']) for c in range(b, p['n3']) if a + b + c == p['n3'])
    s, r2 = 0, None
    for n in range(1, 10000):
        s += len(str(n))
        if s == p['D']: r2 = n; break
    r3 = sum(1 for f in product(range(3), repeat=3) if f[0] != f[1] != f[2] and f.count(p['odna'][1]) == 1)
    r4 = sum(1 for n in range(1, p['N'] + 1) if n % 4 and n % 6)
    r5 = sum(1 for n in T if p['d'][0] in str(n) and p['d'][1] in str(n))
    return r1, r2, r3, r4, r5, polos(p['kp'])
# полоска (ушла сюда из △11 КР): проверка формулы 2^(n-1) перебором для малых n
def polos(n):
    def go(lo, hi):
        if hi - lo + 1 == n: return 1
        return (go(lo - 1, hi) if lo > 0 else 0) + (go(lo, hi + 1) if hi < n - 1 else 0)
    return sum(go(i, i) for i in range(n))
assert [polos(n) for n in range(1, 8)] == [2 ** (n - 1) for n in range(1, 8)]
assert kluch('А') == (8, 136, 8, 133, 52, 128)
assert kluch('Б') == (10, 126, 8, 200, 35, 256)
# числа из решений (в чат владельцу)
assert 900 - (648 + 648 - 448) == 52 and 900 - (729 + 648 - 512) == 35
assert 9 + 180 + 3 * 37 == 300 and 9 + 180 + 3 * 27 == 270
assert 200 - (50 + 33 - 16) == 133 and 300 - (75 + 50 - 25) == 200
assert 2 + 4 + 2 == 8
X = ('.sec{display:none}.page{--abw:23mm;--rowh:6.6mm}.fio{margin:2.5mm 0 5mm}.z{margin-bottom:4.6mm;display:flow-root}'
     '.ab.one .r{grid-template-columns:1fr 8mm}.hd b:after{content:"△";font-size:21pt;font-weight:400;margin-left:3mm;vertical-align:-1.5pt}')
def build():
    return polulist(META, [(v, dict(heading='', items=items(v))) for v in ('А', 'Б')], X)
if __name__ == '__main__':
    p = f'{HERE}/out/MINILISTOK-06-10.html'; open(p, 'w', encoding='utf-8').write(build())
    rows = [(str(i + 1), a, b) for i, (a, b) in enumerate(zip(kluch('А'), kluch('Б')))]
    s = f'{HERE}/out/SHPARGALKA-MINILISTOK-06-10.html'
    open(s, 'w', encoding='utf-8').write(shpargalka('Мини-листок · ответы', '6 октября', [('Мини-листок', ['№', 'А', 'Б'], rows, [])]))
    to_pdf([p, s])
    print('перелив, мм:', fit_report(p))
