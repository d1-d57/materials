"""Численная проверка ядра сюжета «Пути Дика и вес sin^2».
Запуск: python3 proverka.py
Проверяет: утв.3 (ортонормальность), теор.4 (пути = коэффициенты), след.5 (числа Каталана)."""
from math import cos, sin, pi, comb

N_ = 200_000  # узлов численного интегрирования


def chi(k, t):
    return sin((k + 1) * t) / sin(t)


def integ(f):
    """(2/pi) * int_0^pi f(t) sin^2 t dt"""
    s = sum(f((j + 0.5) * pi / N_) * sin((j + 0.5) * pi / N_) ** 2 for j in range(N_))
    return 2 / pi * s * pi / N_


def paths(N, k):
    """число путей длины N из 0 в k, не спускающихся ниже нуля"""
    cur = {0: 1}
    for _ in range(N):
        nxt = {}
        for x, c in cur.items():
            for y in (x - 1, x + 1):
                if y >= 0:
                    nxt[y] = nxt.get(y, 0) + c
        cur = nxt
    return cur.get(k, 0)


print("утв.3 — матрица Грама (ожидается единичная):")
for j in range(4):
    print("  ", [round(integ(lambda t, j=j, k=k: chi(j, t) * chi(k, t)), 4) for k in range(4)])

print("\nтеор.4 — интеграл против прямого счёта путей:")
for N in range(1, 7):
    a = [round(integ(lambda t, k=k, N=N: (2 * cos(t)) ** N * chi(k, t)), 3) for k in range(N + 1)]
    b = [paths(N, k) for k in range(N + 1)]
    assert all(abs(x - y) < 1e-2 for x, y in zip(a, b)), (N, a, b)
    print(f"  N={N}: {b}  ✓")

print("\nслед.5 — числа Каталана:")
for n in range(1, 7):
    val = integ(lambda t, n=n: (2 * cos(t)) ** (2 * n))
    cat = comb(2 * n, n) // (n + 1)
    refl = comb(2 * n, n) - comb(2 * n, n + 1)
    assert abs(val - cat) < 1e-2 and cat == refl
    print(f"  n={n}: интеграл {val:.4f} = C_n {cat} = отражение {refl}  ✓")
