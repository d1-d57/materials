# -*- coding: utf-8 -*-
"""Все числа статьи «Умный перебор» (урок 1, 6.10) — перебором. Запуск: python3 _sluzhebnoe/proverki.py
Каждое число текста стоит здесь в assert; правка числа в тексте без правки здесь — брак."""
from itertools import product
from collections import Counter

# --- монеты: 10 ₽ монетами 1, 2, 5 (набор = сколько пятёрок, двушек, рублей)
nab = [(f, t, 10 - 5*f - 2*t) for f in range(3) for t in range(6) if 10 - 5*f - 2*t >= 0]
assert len(nab) == 10
po_pyat = Counter(f for f, t, o in nab)
assert (po_pyat[2], po_pyat[1], po_pyat[0]) == (1, 3, 6) and 1 + 3 + 6 == 10
key = lambda s: (s.count(5), s.count(2), s.count(1))
haos = [(5, 5), (2, 2, 2, 2, 2), (5, 2, 2, 1), (5, 1, 1, 1, 1, 1), (2, 5, 1, 2), (2, 2, 2, 2, 1, 1), (1,)*10, (5, 2, 1, 1, 1)]
assert len(haos) == 8 and all(sum(s) == 10 for s in haos)
assert key((2, 5, 1, 2)) == key((5, 2, 2, 1))
haos_set = {key(s) for s in haos}
assert len(haos_set) == 7 and len(set(nab) - haos_set) == 3
# цепочка Васи: каждый раз размениваем самую крупную монету (5 -> 2+2+1, 2 -> 1+1)
s = [5, 5]; cep = [tuple(s)]
while max(s) > 1:
    m = max(s); s.remove(m); s += [2, 2, 1] if m == 5 else [1, 1]; s.sort(reverse=True); cep.append(tuple(s))
vasya = {key(c) for c in cep}
assert len(cep) == 7 and len(vasya) == 7
assert key((2, 2, 2, 2, 2)) not in vasya and key((5, 2, 1, 1, 1)) not in vasya and key((5, 1, 1, 1, 1, 1)) not in vasya
assert all(1 in c for c in cep[1:])            # после первого шага рубль есть всегда

# --- трёхзначные с суммой цифр 5
ds = lambda n: sum(map(int, str(n)))
s5 = [n for n in range(100, 1000) if ds(n) == 5]
assert len(s5) == 15
assert [sum(1 for n in s5 if n // 100 == a) for a in range(1, 6)] == [5, 4, 3, 2, 1]
haos5 = [500, 230, 113, 401, 122, 320, 311, 104, 212, 410, 131, 203, 302, 221, 50]   # 50 = «050»
assert len(haos5) == 15 and set(s5) - set(haos5) == {140} and set(haos5) - set(s5) == {50}

# --- ДЗ 4: двузначные с простой суммой цифр
PR = [2, 3, 5, 7, 11, 13, 17]
kusok = [sum(1 for n in range(10, 100) if ds(n) == p) for p in PR]
assert kusok == [2, 3, 5, 7, 8, 6, 2] and sum(kusok) == 33
assert all(k == (p if p <= 9 else 19 - p) for k, p in zip(kusok, PR))

# --- флаги: три полосы, Б К С, соседние разные; порядок — по верхней, средней, нижней
fl = [''.join(f) for f in product('БКС', repeat=3) if f[0] != f[1] and f[1] != f[2]]
assert len(fl) == 12 == 3 * 2 * 2 and fl[fl.index('БСК') + 1] == 'КБК'

# --- ДЗ 6: первые две цифры разной чётности, сумма цифр делится на 10
d6 = [n for n in range(100, 1000) if (n // 100) % 2 != (n // 10 % 10) % 2 and ds(n) % 10 == 0]
assert len(d6) == 45 == 9 * 5

# --- двузначные с семёркой; нажатия клавиши 7
s7 = [n for n in range(10, 100) if '7' in str(n)]
assert len(s7) == 18 and len(range(70, 80)) == 10 and len([n for n in range(10, 100) if n % 10 == 7]) == 9
assert sum(str(n).count('7') for n in range(10, 100)) == 19 == 10 + 9

# --- ДЗ 5: трёхзначные, кратные 9 или 15
T = range(100, 1000)
k9 = [n // 9 for n in T if n % 9 == 0]; k15 = [n // 15 for n in T if n % 15 == 0]; k45 = [n // 45 for n in T if n % 45 == 0]
assert (k9[0], k9[-1], len(k9)) == (12, 111, 100) and 111 - 11 == 100
assert (k15[0], k15[-1], len(k15)) == (7, 66, 60) and 66 - 6 == 60
assert (k45[0], k45[-1], len(k45)) == (3, 22, 20) and 22 - 2 == 20
assert sum(1 for n in T if n % 9 == 0 or n % 15 == 0) == 140 == 100 + 60 - 20
assert sum(1 for n in T if n % 135 == 0) == 7 and 180 % 9 == 0 and 180 % 15 == 0 and 180 % 135 != 0

# --- ДЗ 3: далматинцы
vse, net, lev, prav = 101, 22, 29, 17
assert vse - net - lev == 50 and 50 - prav == 33 and net + lev + prav + 33 == vse

# --- трёхзначные с пятёркой
s_5 = [n for n in T if '5' in str(n)]
assert len(s_5) == 252 and 999 - 99 == 900 and 8 * 9 * 9 == 648 and 900 - 648 == 252
assert len(range(500, 600)) == 100 and sum(1 for n in T if str(n)[1] == '5') == 90 and sum(1 for n in T if str(n)[2] == '5') == 90
assert 100 + 90 + 90 == 280

# --- от 17 до 23
assert len(range(17, 24)) == 7 == 23 - 16 and 23 - 17 == 6 == len(range(18, 24))

# --- выпавшие листы: на листе k страницы 2k-1 и 2k
list_ = lambda p: (p + 1) // 2
assert list_(36) == 18 and list_(35) == 18 and list_(91) == 46 and list_(92) == 46
assert len(range(18, 47)) == 29 == 46 - 17 and (92 - 34) // 2 == 29

# --- ДЗ 1: этажи; лестница «во сколько раз короче»
assert len(range(2, 6)) == 4 and 60 // 4 == 15 and len(range(2, 11)) == 9 and 9 * 15 == 135 == 2 * 60 + 15
assert len(range(2, 26)) == 24 and 24 // 4 == 6


# --- разложения 6 (раздел «Перебор»)
def parts(n, m=None):
    m = m or n
    if n == 0:
        yield (); return
    for k in range(min(n, m), 0, -1):
        for r in parts(n - k, k): yield (k,) + r
P6 = list(parts(6)); assert len(P6) == 11
def comps(n):
    if n == 0:
        yield (); return
    for k in range(1, n + 1):
        for r in comps(n - k): yield (k,) + r
assert len(list(comps(6))) == 32
haos6 = [(2,4),(1,)*6,(1,2,1,2),(3,3),(1,5),(1,1,2,1,1),(2,3,1),(6,),(1,1,3,1),(2,1,1,2),(2,2,2)]
hs = [tuple(sorted(h, reverse=True)) for h in haos6]
assert len(haos6) == 11 and len(set(hs)) == 10 and set(P6) - set(hs) == {(4,1,1)}
assert sorted((1,2,1,2), reverse=True) == sorted((2,1,1,2), reverse=True) and sorted((1,1,3,1)) != sorted((1,2,1,2))
c = [(6,)]
while c[-1][0] > 1:
    x = list(c[-1]); x[0] -= 1; x.append(1); c.append(tuple(sorted(x, reverse=True)))
assert len(c) == 6 and set(P6) - set(c) == {(4,2),(3,3),(3,2,1),(2,2,2),(2,2,1,1)}
from collections import Counter as C2
dl = C2(len(p) for p in P6); assert dl[3] == 3 and dl[2] == 3
assert [p for p in P6 if len(p) == 3] == [(4,1,1),(3,2,1),(2,2,2)]
assert C2(p[0] for p in P6) == {6:1,5:1,4:2,3:3,2:3,1:1}
assert P6.index((4,1,1)) + 1 == P6.index((3,3)) and P6[P6.index((3,1,1,1)) + 1] == (2,2,2)
# сумма цифр 7: проверки «по возрастанию»
s7_ = [n for n in range(10, 100) if ds(n) == 7]
assert s7_ == [16,25,34,43,52,61,70] and len(range(62, 71)) == 9 and len(range(71, 100)) == 29
# флаги: правило «меняем одну полосу»
adj = {a: [b for b in fl if sum(x != y for x, y in zip(a, b)) == 1] for a in fl}
best = [0]
def dfs(v, seen):
    best[0] = max(best[0], len(seen))
    for w in adj[v]:
        if w not in seen: dfs(w, seen | {w})
for v in fl: dfs(v, {v})
assert best[0] == 11 and C2(f[0] for f in fl) == {'Б':4,'К':4,'С':4}
assert fl == ['БКБ','БКС','БСБ','БСК','КБК','КБС','КСБ','КСК','СБК','СБС','СКБ','СКС'] and 'КББ' not in fl
print('proverki v2: разложения, флаги, сумма 7 — сошлись')
assert 5 + 8 - 1 == 12 and fl[fl.index('КБК') - 1] == 'БСК' and P6[P6.index((3,3)) - 1] == (4,1,1) and 2*2*2 == 8 and 3*4 == 12
print('proverki: все числа статьи сошлись')
assert fl[fl.index('СБК') - 1] == 'КСК' and P6[P6.index((2,2,2)) - 1] == (3,1,1,1) and 36 == 2*18 and 91 == 2*46 - 1 and 9*10 == 90
print('proverki v5: обратные вопросы сошлись')
# v6: таблица «Все разрезы урока»; флаги строкой без умножения
assert 1+1+2+3+3+1 == 11 and [sum(1 for q in P6 if q[0] == k) for k in (6,5,4,3,2,1)] == [1,1,2,3,3,1]
assert 4+4+4 == 12 and [f for f in fl if f[0] == 'Б'] == ['БКБ','БКС','БСБ','БСК'] and 23-16 == 7 and 46-17 == 29
print('proverki v6: таблица разрезов сошлась')
# --- v7: крючок, разрез Васи, фокус
assert [sum(1 for q in P6 if k in q) for k in range(1, 7)] == [7, 5, 3, 2, 1, 1] and 7+5+3+2+1+1 == 19 == len(s7) + 1
assert [q for q in P6 if len(set(q)) == 3] == [(3, 2, 1)] and sum(len(set(q)) - 1 for q in P6) == 8 and 11 + 8 == 19
assert P6.index((3, 2, 1)) + 1 == 6 and P6[9 - 1] == (2, 2, 1, 1) and 1+1+2 == 4 and 1+1+2+3 == 7
P9 = list(parts(9)); assert len(P9) == 30 and [sum(1 for q in P9 if q[0] == k) for k in range(9, 0, -1)] == [1, 1, 2, 3, 5, 6, 7, 4, 1]
assert P9.index((4, 3, 2)) + 1 == 14 == 1+1+2+3+5 + 2 and P9[20 - 1] == (3, 3, 2, 1) and 1+1+2+3+5+6 == 18 and P9[12] == (4, 4, 1) and P9[18] == (3, 3, 3)
assert 1+1+2+3+5+6+7+4+1 == 30
assert 5 - 1 == 4 and 10 - 1 == 9 and 9 * 15 == 135 and 25 - 1 == 24 and 24 // 4 == 6
assert all(sum(1 for n in range(10, 100) if ds(n) == s_) == (s_ if s_ <= 9 else 19 - s_) for s_ in range(1, 19))
print('proverki v7: крючок, разрез Васи, фокус сошлись')
# v8: «Ответ» и мостик
assert sum(range(1, 10)) == 45 == sum(1 for n in range(10, 100) if ds(n) <= 9) and 12 + 6 == 18
print('proverki v8: мостик сошёлся')
# v9: модель 1…90 и подъёмы из подвала
M9 = [n for n in range(1, 91) if n % 9 == 0]; M15 = [n for n in range(1, 91) if n % 15 == 0]
assert len(M9) == 10 and len(M15) == 6 and set(M9) & set(M15) == {45, 90} and len(set(M9) | set(M15)) == 14 == 10 + 6 - 2
assert 15 * 7 == 105 and 15 * 6 == 90 and 15 * 66 == 990 and 9 * 11 == 99 and 9 * 12 == 108 and 45 * 2 == 90 and 45 * 3 == 135 and 45 * 22 == 990
assert sum(1 for n in range(10, 100) if ds(n) == 7) == 7
print('proverki v9: модель делимости сошлась')
# v10: флаги без умножения, номер КСБ
assert fl.index('КСБ') + 1 == 7 == 4 + 3 and [f for f in fl if f[0] == 'К'] == ['КБК', 'КБС', 'КСБ', 'КСК'] and [f for f in fl if f[0] == 'С'] == ['СБК', 'СБС', 'СКБ', 'СКС']
print('proverki v10: флаги сошлись')
