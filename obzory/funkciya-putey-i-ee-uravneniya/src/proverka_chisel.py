#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка чисел обзора «Функция путей и её уравнения».
Запуск: python3 proverka_chisel.py
Блоки: 1) d_m(n): перебор против спектральной формулы;
2) формула утверждения 9 против перебора с площадью «клетки под путём»;
3) изображения против перебора и динамики; 4) число m=3, n=60 и его слагаемые."""
from collections import defaultdict
from math import comb, cos, pi, sin


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
    """Спектральная формула (теорема 16)."""
    return 2 / (m + 2) * sum(
        (2 * cos(k * pi / (m + 2))) ** (2 * n) * sin(k * pi / (m + 2)) ** 2
        for k in range(1, m + 2))


def brute_area(m, n):
    """Перебор путей из 0 в 0 высоты <= m длины 2n; площадь — сумма высот
    перед каждым шагом вверх. Возвращает {площадь: число путей}."""
    cnt = defaultdict(int)

    def rec(h, taken, area):
        if taken == 2 * n:
            if h == 0:
                cnt[area] += 1
            return
        for step in (1, -1):
            h_new = h + step
            if 0 <= h_new <= m:
                rec(h_new, taken + 1, area + (h if step == 1 else 0))

    rec(0, 0, 0)
    return dict(cnt)


NMAX = 6


def pmul(A, B):
    out = {}
    for i, a in A.items():
        for j, b in B.items():
            if i + j > NMAX:
                continue
            t = out.setdefault(i + j, {})
            for k, v in a.items():
                for l, w in b.items():
                    t[k + l] = t.get(k + l, 0) + v * w
    return out


def shift_xq(A):
    return dict((n, dict((k + n, v) for k, v in d.items())) for n, d in A.items())


def Am(k):
    """F_k(z,q) = 1/(1 - x*F_{k-1}(xq,q)); F_0 = 1."""
    if k == 0:
        return {0: {0: 1}}
    B = shift_xq(Am(k - 1))
    G = {0: {0: 1}}
    P = {0: {0: 1}}
    for r in range(1, NMAX + 1):
        P = pmul(P, B)
        for i, d in P.items():
            if i + r > NMAX:
                continue
            t = G.setdefault(i + r, {})
            for kk, v in d.items():
                t[kk] = t.get(kk, 0) + v
    return G


def obmotki_formula(M, N, x):
    """W_M(N,x) = сумма C(N,(N+x+jM)/2) по целым j с целым нижним индексом."""
    tot = 0
    for j in range(-(N // M + 3), N // M + 4):
        idx = (N + x + j * M)
        if idx % 2 == 0:
            tot += C(N, idx // 2)
    return tot


def obmotki_spektr(M, N, x):
    """Независимая проверка: (1/M) * сумма собственных чисел цикла в степени N."""
    return sum((2 * cos(2 * pi * k / M)) ** N * cos(2 * pi * k * x / M)
               for k in range(M)) / M


def izobrazheniya(m, n):
    """Знакопеременная сумма изображений со сдвигом m+2."""
    M = m + 2
    rng = range(-(n // M + 3), n // M + 3)
    slagaemye = dict((j, C(2 * n, n - j * M) - C(2 * n, n + 1 - j * M)) for j in rng)
    return sum(slagaemye.values()), slagaemye


if __name__ == "__main__":
    print("== d_m(n): перебор против спектральной формулы ==")
    for m in range(1, 6):
        ryad = []
        for n in range(1, 7):
            p, s = peresbor(m, n), round(spektr(m, n))
            assert p == s, (m, n, p, s)
            ryad.append(p)
        print("m=%d: %s" % (m, ryad))

    print("== формула утверждения 9 против перебора ==")
    F4 = Am(4)
    F3 = Am(3)
    F2 = Am(2)
    F1 = Am(1)
    FS = [None, F1, F2, F3, F4]
    for m in range(1, 5):
        for n in range(1, 6):
            got = FS[m].get(n, {})
            want = brute_area(m, n)
            assert got == want, (m, n, got, want)
    print("совпадает всюду при m<=4, n<=5")

    print("== обмотки: формула против спектра цикла ==")
    for M in range(2, 9):
        for N in range(0, 13):
            for x in range(M):
                f_ = obmotki_formula(M, N, x)
                s_ = round(obmotki_spektr(M, N, x))
                assert f_ == s_, (M, N, x, f_, s_)
    print("совпадает всюду при M<=8, N<=12")

    print("== изображения против перебора и динамики ==")
    for m in range(1, 7):
        for n in range(1, 9):
            s_, _ = izobrazheniya(m, n)
            assert s_ == peresbor(m, n), (m, n, s_)
    print("совпадает всюду при m<=6, n<=8")

    print("== m=3, n=60 ==")
    otvet = peresbor(3, 60)
    summ, slag = izobrazheniya(3, 60)
    assert summ == otvet
    mx_diff = max(abs(v) for v in slag.values())
    mx_binom = C(120, 60)
    print("ответ d_3(60) = %d" % otvet)
    print("наибольшее слагаемое-разность = %d, отношение к ответу = %.3g"
          % (mx_diff, mx_diff / otvet))
    print("наибольший биномиальный коэффициент C(120,60) = %d, "
          "отношение к ответу = %.3g" % (mx_binom, mx_binom / otvet))
