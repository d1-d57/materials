"""Проверка задач листка кружка 29.09 «Построй или докажи, что нельзя» (v3) перебором.
Блоки подписаны номерами задач листка v3; РЕЗЕРВ — задачи, ушедшие из листка в резерв решений.
Каждый блок печатает то, что утверждается в решениях. Запуск: python3 proverka_29-09_konstruktivy.py
"""
from itertools import product, permutations

print("== ЗАДАЧИ 2 и 7(а). сумма = произведение = N (не менее двух натуральных слагаемых)")
def sp(N):
    # ищем мультимножество из >=2 натуральных, сумма = произведение = N
    # достаточно перебрать множители >=2 (единицы добивают сумму)
    res = []
    def rec(rest_prod, start, facs):
        if rest_prod == 1:
            s = sum(facs); ones = N - s
            if ones >= 0 and len(facs) + ones >= 2:
                res.append((tuple(facs), ones))
            return
        for d in range(start, rest_prod + 1):
            if rest_prod % d == 0:
                rec(rest_prod // d, d, facs + [d])
    rec(N, 2, [])
    return res
bad = []
for N in range(1, 301):
    ok = bool(sp(N))
    prime = N > 1 and all(N % p for p in range(2, int(N**0.5) + 1))
    comp = N > 3 and not prime
    if ok != comp: bad.append(N)
print("N=99:", sp(99)[:3], "...")
print("расхождений с «можно ⇔ N составное» до 300:", bad)

print("== РЕЗЕРВ. таблица 3×3")
g = [[5, -3, 5], [-3, 0, -3], [5, -3, 5]]
print("квадраты 2×2:", [g[i][j]+g[i+1][j]+g[i][j+1]+g[i+1][j+1] for i in range(2) for j in range(2)], "всего:", sum(map(sum, g)))

print("== ЗАДАЧА 4. n телефонов, каждый ровно с тремя: круг + противоположный")
def cubic(n):
    m = n // 2
    E = set()
    for i in range(n):
        E.add(frozenset((i, (i+1) % n))); E.add(frozenset((i, (i+m) % n)))
    deg = [sum(1 for e in E if i in e) for i in range(n)]
    return all(d == 3 for d in deg) and all(len(e) == 2 for e in E)
print({n: cubic(n) for n in range(4, 21, 2)})

print("== ЗАДАЧА 6. круг из n, каждый: «оба моих соседа — лжецы»")
for n in range(3, 13):
    s = set()
    for a in product([0, 1], repeat=n):
        if all(a[i] == (a[i-1] == 0 and a[(i+1) % n] == 0) for i in range(n)):
            s.add(sum(a))
    print(n, sorted(s))

print("== РЕЗЕРВ. n-значное число из цифр 1 и 2, делящееся на 2^n: сколько их")
for n in range(1, 15):
    c = [int(''.join(t)) for t in product('12', repeat=n) if int(''.join(t)) % 2**n == 0]
    print(n, len(c), c[0] if c else None)

print("== РЕЗЕРВ. Ася, Бася, Вася: три турнира")
T = [("В", "А", "Б"), ("А", "Б", "В"), ("Б", "В", "А")]
def above(x, y): return sum(t.index(x) < t.index(y) for t in T)
print("А>Б", above("А", "Б"), "Б>В", above("Б", "В"), "В>А", above("В", "А"), "из", len(T))
print("двух турниров мало? проверка всех пар порядков:")
P = list(permutations("АБВ"))
two = any(all(sum(t.index(x) < t.index(y) for t in pair) * 2 > 2 for x, y in [("А","Б"),("Б","В"),("В","А")]) for pair in product(P, repeat=2))
print("с двумя турнирами возможно:", two)

print("== ЗАДАЧА 7(б). Наборы РАЗЛИЧНЫХ натуральных (хотя бы двух), сумма = произведение, все элементы <= 60")
from itertools import combinations
found = []
for k in range(2, 6):
    for c in combinations(range(1, 61), k):
        p = 1
        for x in c: p *= x
        if p == sum(c): found.append(c)
print(found)

print("== ЗАДАЧА 5(а). Правильный треугольник: сетка k×k маленьких (k^2 штук), угловой кусок из (k-1)^2 → 2k кусков")
print({k: k*k - (k-1)**2 + 1 for k in range(3, 6)}, "плюс шаг +3")

print("== ЗАДАЧА 3. ряд из n чисел, сумма соседних > 0, общая < 0: пример −a,(a+1),...,−a при нечётном n")
for n in (9, 11):
    a = n
    r = [(-a if i % 2 == 0 else a+1) for i in range(n)]
    print(n, r[:4], "...", "соседние:", set(r[i]+r[i+1] for i in range(n-1)), "сумма:", sum(r))

print("== ЗАДАЧА 8*. 9 задач, три порядка; отметки А(раньше Б), Б(раньше В), В(раньше А)")
from itertools import permutations as P3
best = {}
for o in P3("АБВ"):
    m = (o.index("А") < o.index("Б")) + (o.index("Б") < o.index("В")) + (o.index("В") < o.index("А"))
    best[o] = m
print("отметок за задачу по порядкам:", best, "максимум:", max(best.values()))
orders = [("А","Б","В")]*3 + [("Б","В","А")]*3 + [("В","А","Б")]*3
cnt = {x: 0 for x in "АБВ"}
for o in orders:
    if o.index("А") < o.index("Б"): cnt["А"] += 1
    if o.index("Б") < o.index("В"): cnt["Б"] += 1
    if o.index("В") < o.index("А"): cnt["В"] += 1
print("пример на 6:", cnt, "; по 7 требует 21 > 9*2 =", 18)

print("== ЗАДАЧА 10*. запутанный турнир (любых двоих кто-то обыграл)")
from itertools import product as PR, combinations as CB
def zaput(n, beats):
    return all(any(beats(z, x) and beats(z, y) for z in range(n) if z not in (x, y)) for x, y in CB(range(n), 2))
for n in range(3, 7):
    pairs = list(CB(range(n), 2)); found = False
    for bits in PR([0, 1], repeat=len(pairs)):
        W = {}
        for (i, j), b in zip(pairs, bits): W[(i, j)] = b; W[(j, i)] = 1 - b
        if zaput(n, lambda a, b: W[(a, b)] == 1): found = True; break
    print(n, "существует:", found)
print(7, "круговой {1,2,4}:", zaput(7, lambda a, b: (b - a) % 7 in (1, 2, 4)))
def klon(n, beats):  # добавить двойника участника 0 с номером n; 0 бьёт двойника
    def nb(a, b):
        a0 = 0 if a == n else a; b0 = 0 if b == n else b
        if {a, b} == {0, n}: return a == 0
        return beats(a0, b0)
    return n + 1, nb
m, B = 7, (lambda a, b: (b - a) % 7 in (1, 2, 4))
for _ in range(5):
    m, B = klon(m, B); print(m, "после клонирования:", zaput(m, B))
