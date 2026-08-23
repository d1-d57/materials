#!/usr/bin/env python3
"""Проверка чисел обзора «Функция путей и её уравнения».
Запуск: python3 proverka_chisel.py
Печатает: таблицу d_m(n) перебором и по спектральной формуле;
формулу изображений против перебора; число для m=3, n=60 и его слагаемые.
"""
from math import comb, cos, pi


def C(a, b):
    return comb(a, b) if 0 <= b <= a else 0


def peresbor(m, n):
    """d_m(n): пути из 0 в 0 по отрезку {0..m}, длина 2n."""
    dp = [0] * (m + 1)
    dp[0] = 1
    for _ in range(2 * n):
        nd = [0] * (m + 1)
        for x, v in enumerate(dp):
            if v:
                if x - 1 >= 0:
                    nd[x - 1] += v
                if x + 1 <= m:
                    nd[x + 1] += v
        dp = nd
    return dp[0]


def spektr(m, n):
    """Спектральная формула: 2/(m+2) * сумма по k синусоидальных слагаемых."""
    return 2 / (m + 2) * sum(
        (2 * cos(k * pi / (m + 2))) ** (2 * n) * sin(k * pi / (m + 2)) ** 2
        for k in range(1, m + 2))


def izobrazheniya(m, n):
    """Знакопеременная сумма изображений со сдвигом m+2."""
    M = m + 2
    rng = range(-(n // M + 3), n // M + 3)
    slagaemye = {j: C(2 * n, n - j * M) - C(2 * n, n + 1 - j * M) for j in rng}
    return sum(slagaemye.values()), slagaemye


if __name__ == "__main__":
    print("== d_m(n): перебор против спектральной формулы ==")
    for m in range(1, 6):
        ryad = []
        for n in range(1, 7):
            p, s = peresbor(m, n), round(spektr(m, n))
            assert p == s, (m, n, p, s)
            ryad.append(p)
        print(f"m={m}: {ryad}")

    print("== изображения против перебора ==")
    for m in range(1, 7):
        for n in range(1, 9):
            s, _ = izobrazheniya(m, n)
            assert s == peresbor(m, n), (m, n, s)
    print("совпадает всюду при m<=6, n<=8")

    print("== m=3, n=60 ==")
    otvet = peresbor(3, 60)
    summ, slag = izobrazheniya(3, 60)
    assert summ == otvet
    mx_diff = max(abs(v) for v in slag.values())
    mx_binom = C(120, 60)
    print(f"ответ d_3(60) = {otvet}")
    print(f"наибольшее слагаемое-разность = {mx_diff}, отношение к ответу = {mx_diff/otvet:.3g}")
    print(f"наибольший биномиальный коэффициент C(120,60) = {mx_binom}, "
          f"отношение к ответу = {mx_binom/otvet:.3g}")
