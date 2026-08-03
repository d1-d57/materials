"""Проверка всех чисел обзора «Пути ограниченной высоты и тригонометрия».
Запуск:  python3 obzory/puti-ogranichennoy-vysoty/proverka.py
Ничего не берётся из памяти: каждая таблица считается двумя независимыми способами."""
from math import cos, pi, sin, sqrt

# ---------- 1. перебор ----------
def perebor(N, m):
    """число путей длины N из 0 в 0, шаги +-1, 0 <= высота <= m"""
    cur = {0: 1}
    for _ in range(N):
        nxt = {}
        for x, c in cur.items():
            for y in (x - 1, x + 1):
                if 0 <= y <= m:
                    nxt[y] = nxt.get(y, 0) + c
        cur = nxt
    return cur.get(0, 0)

# ---------- 2. формула теоремы 20 ----------
def spektr(N, m):
    M = m + 2
    return 2 / M * sum((2 * cos(k * pi / M)) ** N * sin(k * pi / M) ** 2
                       for k in range(1, m + 2))

print("=== таблица вступления: перебор против теоремы 20 ===")
print(f"{'m':>4} | {'2n=2':>6}{'4':>6}{'6':>6}{'8':>6}{'10':>6}{'12':>6}   (перебор; формула теоремы 20 сверена по месту)")
for m in range(1, 6):
    a = [perebor(2 * n, m) for n in range(1, 7)]
    b = [round(spektr(2 * n, m), 6) for n in range(1, 7)]
    assert all(abs(x - y) < 1e-6 for x, y in zip(a, b)), (m, a, b)
    print(f"{m:>4} | " + "".join(f"{v:>6}" for v in a) + "   ✓")
print("  ∞  | " + "".join(f"{perebor(2*n, 50):>6}" for n in range(1, 7)) + "   (числа Каталана)")

# ---------- 3. скорость роста, теоремы 14 и пример 15 ----------
print("\n=== скорость роста: отношение соседних против (2cos(pi/(m+2)))^2 ===")
for m in range(1, 6):
    row = [perebor(2 * n, m) for n in range(1, 13)]
    otn = row[-1] / row[-2]
    teor = (2 * cos(pi / (m + 2))) ** 2
    assert abs(otn - teor) < 0.02, (m, otn, teor)
    print(f"  m={m}: отношение {otn:.5f}   теория {teor:.5f}   ✓")
print(f"  золотое сечение phi^2 = {((1+sqrt(5))/2)**2:.5f}  (это строка m=3)")

# ---------- 4. числа Каталана как интеграл, теорема 22 ----------
NODES = 200_000
def integral(N):
    s = sum((2 * cos((j + .5) * pi / NODES)) ** N * sin((j + .5) * pi / NODES) ** 2
            for j in range(NODES))
    return 2 / pi * s * pi / NODES

print("\n=== теорема 22: числа Каталана как интеграл ===")
from math import comb
for n in range(1, 7):
    val, cat = integral(2 * n), comb(2 * n, n) // (n + 1)
    assert abs(val - cat) < 1e-2 and cat == comb(2*n, n) - comb(2*n, n+1)
    print(f"  n={n}: интеграл {val:.4f} = C_n {cat} = отражение {comb(2*n,n)-comb(2*n,n+1)}  ✓")

# ---------- 5. производящие функции, теоремы 2 и 13 ----------
try:
    import sympy as sp
except ImportError:
    print("\n(sympy не установлен — блок производящих функций пропущен)")
else:
    z = sp.symbols('z')
    P = [sp.Integer(1), sp.Integer(1)]
    for _ in range(2, 10):
        P.append(sp.expand(P[-1] - z * P[-2]))
    print("\n=== теоремы 2, 13: ряды G_m и их полюса ===")
    for m in range(1, 6):
        G = sp.series(P[m] / P[m + 1], z, 0, 7).removeO()
        koef = [sp.Poly(G, z).coeff_monomial(z ** n) for n in range(1, 7)]
        assert koef == [perebor(2 * n, m) for n in range(1, 7)], (m, koef)
        polus = min(abs(float(sp.re(s))) for s in sp.solve(P[m + 1], z))
        teor = (2 * cos(pi / (m + 2))) ** 2
        assert abs(1 / polus - teor) < 1e-9
        print(f"  m={m}: ряд {koef}  наим. полюс {polus:.6f}  1/полюс {1/polus:.6f} = теория ✓")

print("\nВсё сошлось.")

# ---------- 6. метод изображений (теорема 25) ----------
print("\n=== теорема 25: метод изображений ===")
def images(n, m):
    M = m + 2
    s = 0
    for j in range(-8, 9):
        a, b = n - j * M, n + 1 - j * M
        if 0 <= a <= 2 * n: s += comb(2 * n, a)
        if 0 <= b <= 2 * n: s -= comb(2 * n, b)
    return s
for m in (1, 2, 3, 4, 5, 8):
    d = [perebor(2 * n, m) for n in range(1, 9)]
    i = [images(n, m) for n in range(1, 9)]
    assert d == i, (m, d, i)
    print(f"  m={m}: {d}  ✓")

# ---------- 7. замечание 27: при m=3 спектральная формула = Бине ----------
print("\n=== замечание 27: m=3 даёт формулу Бине ===")
F = [0, 1]
for _ in range(30): F.append(F[-1] + F[-2])
for n in range(1, 8):
    assert perebor(2 * n, 3) == F[2 * n - 1]
    print(f"  n={n}: путей {perebor(2*n,3):>4} = F_{2*n-1} = {F[2*n-1]:>4}  ✓")
print("\nВсё сошлось.")

# ---------- 8. финал: отрезок = свёрнутая окружность, две формулы двойственны ----------
print("\n=== финал: отрезок = окружность длины 2(m+2), свёрнутая отражением ===")
import numpy as np
def circle_antisym(n, m):
    """антисимметричная часть блуждания по окружности из 2M клеток"""
    M = m + 2; N = 2 * M
    f = np.zeros(N); f[1] = 1; f[N - 1] = -1
    for _ in range(2 * n):
        f = np.roll(f, 1) + np.roll(f, -1)
    return round((f[1] - f[N - 1]) / 2)
for m in (2, 3, 4, 5):
    a = [perebor(2 * n, m) for n in range(1, 8)]
    b = [circle_antisym(n, m) for n in range(1, 8)]
    assert a == b, (m, a, b)
    print(f"  m={m}: полоса и окружность дают одно: {a}  ✓")

print("\n=== матрица синусов: инволюция и формула Верлинде возвращает доску ===")
for M in (5, 6, 7):
    n = M - 1
    S = np.array([[sqrt(2 / M) * sin(pi * (j + 1) * (k + 1) / M) for k in range(n)] for j in range(n)])
    assert np.allclose(S.T @ S, np.eye(n)) and np.allclose(S @ S, np.eye(n))
    A = np.array([[sum(S[1, l] * S[j, l] * S[k, l] / S[0, l] for l in range(n))
                   for j in range(n)] for k in range(n)])
    Adj = np.zeros((n, n))
    for i in range(n - 1): Adj[i, i + 1] = Adj[i + 1, i] = 1
    assert np.allclose(A, Adj, atol=1e-9)
    print(f"  M={M}: S ортогональна, S^2=I, Верлинде даёт матрицу смежности отрезка  ✓")

print("\n=== тепловое ядро на отрезке: сколько членов нужно каждой формуле ===")
L = 1.0
def heat_img(x, y, t, J):
    return sum(exp(-(x - y + 2 * j * L) ** 2 / (4 * t)) - exp(-(x + y + 2 * j * L) ** 2 / (4 * t))
               for j in range(-J, J + 1)) / sqrt(4 * pi * t)
def heat_spec(x, y, t, K):
    return 2 / L * sum(exp(-k * k * pi * pi * t / L ** 2) * sin(k * pi * x / L) * sin(k * pi * y / L)
                       for k in range(1, K + 1))
from math import exp, sqrt
for t in (0.0005, 0.005, 0.05, 0.5):
    x = y = 0.37
    a, b = heat_img(x, y, t, 40), heat_spec(x, y, t, 400)
    assert abs(a - b) < 1e-9
    ni = next(J for J in range(1, 60) if abs(heat_img(x, y, t, J) - a) < 1e-9)
    ns = next(K for K in range(1, 400) if abs(heat_spec(x, y, t, K) - b) < 1e-9)
    print(f"  t={t:<7} значение {a:.10f}  изображений {ni:>3}, спектральных {ns:>3}")
print("  (тождество Якоби: theta(1/t) = sqrt(t) theta(t))")

print("\nВсё сошлось.")
