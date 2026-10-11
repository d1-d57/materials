# -*- coding: utf-8 -*-
"""R1 · крючки к уроку «Умный перебор» (6.10, 7И).
Каждая задача проверена ПРЯМЫМ перебором (моделируем объекты/события и считаем), формулы — только во вторых assert-ах,
где сверяем, что решение «кусками» даёт то же число. Запуск: python3 r1_proverka.py — все assert проходят, в конце печать ответов."""
from fractions import Fraction as F
from itertools import product, combinations
from math import gcd
import random

OUT = {}

# ---------- 1. Поезда Москва — Владивосток (задача Люка) ----------
def poezda(dney=7):
    """Поезд выходит из Москвы в момент 0 (минуты), идёт dney суток. Из Владивостока поезда выходят каждый день в полдень,
    т. е. в моменты 1440*d. Положение — в минутах пути от Москвы. Встреча: в один момент в одной точке.
    Перебираем все минуты нашего пути и все встречные поезда."""
    T = dney * 1440
    vstrechi = {}
    for d in range(-3 * dney, 3 * dney + 1):           # с запасом: поезда, вышедшие задолго до и после
        for t in range(0, T + 1):                       # каждая минута нашего пути (встречи бывают только в целые полчаса)
            nash = t                                    # мы прошли t минут пути от Москвы
            s = t - 1440 * d                            # сколько минут в пути встречный
            if 0 <= s <= T and T - s == nash:           # встречный сейчас в точке T-s от Москвы
                vstrechi[d] = t
    vsego = len(vstrechi)
    v_puti = sum(1 for t in vstrechi.values() if 0 < t < T)
    return vsego, v_puti, sorted(vstrechi)

v, vp, dni = poezda(7)
assert (v, vp) == (15, 13)
assert dni == list(range(-7, 8))                       # ряд с номерами: от −7 до 7
assert 7 - (-8) == 15 and 7 + 1 + 7 == 15              # куски: вышли раньше нас 7, вместе с нами 1, позже 7
assert poezda(1)[:2] == (3, 1) and poezda(2)[:2] == (5, 3)   # маленькие случаи для доски
OUT['1 поезда'] = (v, vp)

# ---------- 2. Диагональ прямоугольника: через сколько клеток проходит ----------
def kletki(m, n):
    """Прямоугольник m (по горизонтали) × n клеток, диагональ из (0,0) в (m,n). Клетка (i,j) засчитана, если диагональ
    проходит через её ВНУТРЕННОСТЬ: на x∈(i,i+1) высоты диагонали (n·x/m) заходят в (j,j+1) отрезком положительной длины.
    В целых: интервалы (n·i, n·(i+1)) и (m·j, m·(j+1)) пересекаются по отрезку положительной длины."""
    c = 0
    for i in range(m):
        for j in range(n):
            if max(n * i, m * j) < min(n * (i + 1), m * (j + 1)):
                c += 1
    return c

def sobytiya(m, n):
    """Решение «по событиям»: идём по диагонали, считаем пересечения линий сетки ВНУТРИ прямоугольника.
    Вертикальные x=1..m-1, горизонтальные y=1..n-1; узел (x и y целые одновременно) — одно событие, а не два."""
    vert = set(F(x) for x in range(1, m))
    gor = set(F(y * m, n) for y in range(1, n))          # x-координата пересечения с y = const
    return 1 + len(vert) + len(gor) - len(vert & gor)   # 1 стартовая клетка + события (два списка)

assert kletki(5, 8) == 12 == 1 + 4 + 7
assert kletki(3, 2) == 4 and kletki(2, 2) == 2 and kletki(4, 6) == 8
assert kletki(199, 991) == 1189 == 199 + 991 - 1
assert kletki(100, 101) == 200
for m in range(1, 25):
    for n in range(1, 25):
        assert kletki(m, n) == sobytiya(m, n) == m + n - gcd(m, n)
OUT['2 диагональ'] = (kletki(5, 8), kletki(4, 6), kletki(199, 991))

# ---------- 3. Треугольники с целыми сторонами и данным периметром ----------
def treug(p):
    """Все тройки сторон a ≤ b ≤ c (одна запись на треугольник), a+b+c=p, складывается: a+b > c."""
    return [(a, b, c) for a in range(1, p) for b in range(a, p) for c in range(b, p) if a + b + c == p and a + b > c]

T = {p: len(treug(p)) for p in range(3, 21)}
assert [T[p] for p in range(3, 19)] == [1, 0, 1, 1, 2, 1, 3, 2, 4, 3, 5, 4, 7, 5, 8, 7]
assert T[7] == 2 and T[8] == 1 and T[13] == 5 and T[14] == 4
assert treug(13) == [(1, 6, 6), (2, 5, 6), (3, 4, 6), (3, 5, 5), (4, 4, 5)]
assert treug(14) == [(2, 6, 6), (3, 5, 6), (4, 4, 6), (4, 5, 5)]
# разрез по наибольшей стороне: строки
def stroki(p):
    r = {}
    for t in treug(p): r[t[2]] = r.get(t[2], 0) + 1
    return r
assert stroki(13) == {6: 3, 5: 2} and stroki(14) == {6: 3, 5: 1}
OUT['3 треугольники 7/8, 13/14'] = (T[7], T[8], T[13], T[14])

# ---------- 4. Буль: от 1 до 100, вместо чисел, кратных 7 или с цифрой 7, говорят «буль» ----------
bul = [k for k in range(1, 101) if k % 7 == 0 or '7' in str(k)]
krat = [k for k in range(1, 101) if k % 7 == 0]
sem = [k for k in range(1, 101) if '7' in str(k)]
oba = [k for k in range(1, 101) if k % 7 == 0 and '7' in str(k)]
assert len(bul) == 30 and len(krat) == 14 and len(sem) == 19 and oba == [7, 70, 77]
assert 14 + 19 - 3 == 30
# семёрка на месте единиц: 7, 17, …, 97 (10), на месте десятков: 70…79 (10), 77 в обоих
assert len([k for k in range(1, 101) if k % 10 == 7]) == 10 and len([k for k in range(1, 101) if k // 10 == 7]) == 10
# короткая игра до 50: кратные 7 — 7 чисел, с семёркой — 7, 17, 27, 37, 47, общий кусок — только 7
bul50 = [k for k in range(1, 51) if k % 7 == 0 or '7' in str(k)]
assert len(bul50) == 11 == 7 + 5 - 1
OUT['4 буль'] = (len(bul), oba)

# ---------- 5. Скачки на двух кубиках ----------
sposoby = {s: 0 for s in range(1, 13)}
for kr, sin in product(range(1, 7), repeat=2):      # красный и синий кубик — как верх и низ у флага
    sposoby[kr + sin] += 1
assert sposoby[1] == 0 and sposoby[2] == 1 and sposoby[12] == 1 and sposoby[7] == 6
assert [sposoby[s] for s in range(2, 13)] == [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]
assert sum(sposoby.values()) == 1 + 2 + 3 + 4 + 5 + 6 + 5 + 4 + 3 + 2 + 1 == 36
# сама игра: лошадь s делает шаг, когда выпала сумма s; до финиша 5 шагов (для 2 и 12 — 2 шага, «гандикап» не делаем)
random.seed(2026)
pobedy = {s: 0 for s in range(1, 13)}
for _ in range(20000):
    shag = {s: 0 for s in range(1, 13)}
    while True:
        s = random.randint(1, 6) + random.randint(1, 6)
        shag[s] += 1
        if shag[s] == 5: pobedy[s] += 1; break
assert pobedy[1] == 0 and max(pobedy, key=pobedy.get) == 7
assert pobedy[7] > pobedy[6] > pobedy[5] > pobedy[2] and pobedy[7] > pobedy[8] > pobedy[9] > pobedy[12]
OUT['5 скачки: способы 7, лошадь 1'] = (sposoby[7], sposoby[1], round(pobedy[7] / 20000, 2))

# ---------- 6. Квадраты или кубы ----------
def kv(n):
    r = int(n ** 0.5)
    while r * r > n: r -= 1
    while (r + 1) * (r + 1) <= n: r += 1
    return r * r == n
def kub(n):
    r = round(n ** (1 / 3))
    return any((r + e) ** 3 == n for e in (-1, 0, 1))
do1000 = [n for n in range(1, 1001) if kv(n) or kub(n)]
assert len(do1000) == 38
assert len([n for n in range(1, 1001) if kv(n)]) == 31 and len([n for n in range(1, 1001) if kub(n)]) == 10
assert [n for n in range(1, 1001) if kv(n) and kub(n)] == [1, 64, 729]
assert 31 + 10 - 3 == 38
mln = sum(1 for n in range(1, 10 ** 6 + 1) if kv(n) or kub(n))
assert mln == 1000 + 100 - 10 == 1090
OUT['6 квадраты или кубы'] = (len(do1000), mln)

# ---------- 7. Турнир на вылет и шоколадка ----------
random.seed(7)
for n in list(range(1, 60)) + [100, 1000]:
    for _ in range(5):
        igroki = list(range(n)); matchey = 0
        while len(igroki) > 1:                          # в каждом раунде пары случайные, лишний проходит без игры
            random.shuffle(igroki); nov = []
            if len(igroki) % 2: nov.append(igroki.pop())
            while igroki:
                a, b = igroki.pop(), igroki.pop(); matchey += 1
                nov.append(random.choice((a, b)))
            igroki = nov
        assert matchey == n - 1
def raundy(n):
    """По раундам, лишний проходит без игры: сколько матчей в каждом раунде."""
    r = []
    while n > 1: r.append(n // 2); n = n // 2 + n % 2
    return r
assert raundy(37) == [18, 9, 5, 2, 1, 1] and sum(raundy(37)) == 36
def lomaem(m, n):
    """Шоколадка m×n; ломаем случайный кусок по случайной линии, пока все куски не станут дольками."""
    kuski = [(m, n)]; razlomy = 0
    while any(a * b > 1 for a, b in kuski):
        i = random.choice([k for k, (a, b) in enumerate(kuski) if a * b > 1]); a, b = kuski.pop(i)
        if a > 1 and (b == 1 or random.random() < .5):
            x = random.randint(1, a - 1); kuski += [(x, b), (a - x, b)]
        else:
            y = random.randint(1, b - 1); kuski += [(a, y), (a, b - y)]
        razlomy += 1
    return razlomy, len(kuski)
for _ in range(200):
    assert lomaem(6, 8) == (47, 48)
OUT['7 турнир 37 команд, шоколадка 6×8'] = (37 - 1, 47)

# ---------- 8. Гири 1, 3, 9 на двух чашках ----------
def vesa(giri):
    """Груз на левой чашке; каждая гиря: −1 — рядом с грузом, 0 — не участвует, +1 — на правой чашке.
    Вес груза = сумма гирь справа − сумма гирь слева. Перебираем все расстановки."""
    res = {}
    for r in product((-1, 0, 1), repeat=len(giri)):
        w = sum(g * k for g, k in zip(giri, r))
        if w > 0: res.setdefault(w, []).append(r)
    return res
V = vesa((1, 3, 9))
assert sorted(V) == list(range(1, 14))                 # каждый вес от 1 до 13
assert all(len(x) == 1 for x in V.values())            # и ровно одним способом
s9 = sorted(w for w, [r] in V.items() if r[2] == 1)    # строка «девятка справа»
s0 = sorted(w for w, [r] in V.items() if r[2] == 0)    # строка «девятка не нужна»
assert s9 == list(range(5, 14)) and s0 == [1, 2, 3, 4] and 13 - 4 == 9 and 4 + 9 == 13
assert all(r[2] != -1 for [r] in V.values())           # девятка рядом с грузом не бывает
assert sorted(a + 3 * b for a, b in product((-1, 0, 1), repeat=2)) == list(range(-4, 5))   # 1 и 3 дают от −4 до 4
assert sorted(vesa((1, 3, 9, 27))) == list(range(1, 41))
# одна чашка, гири 1, 2, 4, 8: каждый вес 1…15 ровно одним набором
odna = {}
for r in product((0, 1), repeat=4):
    w = sum(g * k for g, k in zip((1, 2, 4, 8), r))
    if w: odna[w] = odna.get(w, 0) + 1
assert sorted(odna) == list(range(1, 16)) and set(odna.values()) == {1}
OUT['8 гири 1,3,9'] = (len(V),)

# ---------- 9. Стрелки часов за сутки ----------
def sovpadeniya():
    """Время t в минутах, шаг 1/11 минуты (все совпадения стрелок попадают на сетку: t = 720k/11).
    Минутная стрелка — t mod 60 «минутных делений», часовая — t/12 mod 60."""
    res = []
    for u in range(0, 24 * 60 * 11):
        t = F(u, 11)
        if t % 60 == (t / 12) % 60: res.append(t)
    return res
S = sovpadeniya()
assert len(S) == 22
po_chasam = [sum(1 for t in S if 60 * h <= t < 60 * h + 60) for h in range(24)]
assert po_chasam == [1] * 11 + [0] + [1] * 11 + [0]   # в каждом часе по разу, кроме 11-го и 23-го
assert 24 - 2 == 22 and 24 - 2 == len(S)             # кругов минутной 24, часовой 2
OUT['9 стрелки'] = (len(S),)

# ---------- 10. Прямоугольники с периметром 1996 и 1998 ----------
def pryam(P):
    return [(a, b) for a in range(1, P) for b in range(a, P) if 2 * (a + b) == P]
assert len(pryam(1996)) == len(pryam(1998)) == 499
assert [a for a, b in pryam(1998)] == list(range(1, 500))   # ряд с номерами: меньшая сторона от 1 до 499
assert len(pryam(20)) == len(pryam(22)) == 5               # маленький случай для доски: 20 и 22
OUT['10 периметр 1996/1998'] = (len(pryam(1996)), len(pryam(1998)))

# ---------- 11. Живые два списка: «встаньте» и «хотя бы сколько в обоих» ----------
random.seed(11)
for _ in range(2000):                                 # случайный класс: формула двух списков всегда верна
    n = random.randint(1, 30)
    A = {k for k in range(n) if random.random() < .6}; B = {k for k in range(n) if random.random() < .5}
    assert len(A | B) == len(A) + len(B) - len(A & B)
A = set(range(20))                                    # 25 человек: 20 любят мороженое (без ограничения — первые 20)
mn = min(sum(1 for k in B if k < 20) for B in combinations(range(25), 18))
assert mn == 13 and 25 - (25 - 20) - (25 - 18) == 13
OUT['11 минимум в обоих (25; 20 и 18)'] = (mn,)

if __name__ == '__main__':
    for k, v in OUT.items(): print(k, '→', v)
    print('ВСЕ ПРОВЕРКИ ПРОШЛИ')
