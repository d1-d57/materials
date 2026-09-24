#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Разведка В1, попытка 2: замкнутая форма F_m(x,y;z,q) для произвольных x,y.

Вес площади от старта = потаговый вес: подъём из клетки p стоит q^{p-x},
спуск бесплатен. Значит F_m(x,y) = [(I-zQ)^{-1}]_{y,x} для трёхдиагональной
Q (поддиагональ -z q^{p-1-x}, наддиагональ -z). Правило Якоби—Усмани:

  x<=y:  F = z^d q^{d(d-1)/2} * theta_x * phi_{y+2} / theta_{m+1},   d=y-x
  x>y:   F = z^d             * theta_y * phi_{x+2} / theta_{m+1},   d=x-y

theta_i = theta_{i-1} - z^2 q^{i-2-x} theta_{i-2}  (theta_0 = theta_1 = 1)
phi_j   = phi_{j+1}   - z^2 q^{j-1-x} phi_{j+2}    (phi_{m+2} = phi_{m+1} = 1)
"""
from collections import defaultdict


def q_puti(m, x, y, N):
    dp = [defaultdict(int) for _ in range(m + 1)]
    dp[x][0] = 1
    for _ in range(N):
        nd = [defaultdict(int) for _ in range(m + 1)]
        for p in range(m + 1):
            for a, v in dp[p].items():
                if p:
                    nd[p - 1][a] += v
                if p < m:
                    nd[p + 1][a + (p - x)] += v
        dp = nd
    return dict(dp[y])


def kontinuanty(m, x, dz_max, dq_max):
    """theta_0..theta_{m+1}: каждый {степень z: {степень q: коэф}}."""
    th = [{0: {0: 1}}, {0: {0: 1}}]
    for i in range(2, m + 2):
        cur = defaultdict(lambda: defaultdict(int))
        for dz, poly in th[i - 1].items():
            for dq, c in poly.items():
                cur[dz][dq] += c
        e = i - 2 - x
        for dz, poly in th[i - 2].items():
            if dz + 2 > dz_max:
                continue
            for dq, c in poly.items():
                if dq + e <= dq_max:
                    cur[dz + 2][dq + e] -= c
        th.append({dz: dict(poly) for dz, poly in cur.items() if poly})
    return th


def obratnye(m, x, dz_max, dq_max):
    """phi_1..phi_{m+2}; нужен индекс до hi+2 <= m+2."""
    ph = {m + 2: {0: {0: 1}}, m + 1: {0: {0: 1}}}
    for j in range(m, 0, -1):
        cur = defaultdict(lambda: defaultdict(int))
        for dz, poly in ph[j + 1].items():
            for dq, c in poly.items():
                cur[dz][dq] += c
        e = j - 1 - x
        for dz, poly in ph[j + 2].items():
            if dz + 2 > dz_max:
                continue
            for dq, c in poly.items():
                if dq + e <= dq_max:
                    cur[dz + 2][dq + e] -= c
        ph[j] = {dz: dict(poly) for dz, poly in cur.items() if poly}
    return ph


def delenie(num, den, dz_max, dq_max):
    """num/den как формальный ряд по z (den[0]=1); оба плоские {(dz,dq):c}."""
    by_dz = {}
    for (dz, dq), c in den.items():
        by_dz.setdefault(dz, {})[dq] = c
    F = defaultdict(int)
    for nz in range(dz_max + 1):
        for nq in range(-dq_max - 12, dq_max + 1):
            acc = num.get((nz, nq), 0)
            for k in range(1, nz + 1):
                dpoly = by_dz.get(k)
                if not dpoly:
                    continue
                for (fdz, fdq), fc in list(F.items()):
                    if fdz == nz - k and (nq - fdq) in dpoly:
                        acc -= fc * dpoly[nq - fdq]
            if acc:
                F[(nz, nq)] = acc
    return dict(F)


def umnozhenie(A, B, dz_max, dq_max):
    out = defaultdict(int)
    for (dz1, dq1), c1 in A.items():
        for (dz2, dq2), c2 in B.items():
            if dz1 + dz2 <= dz_max and dq1 + dq2 <= dq_max:
                out[(dz1 + dz2, dq1 + dq2)] += c1 * c2
    return dict(out)


def plosko(P):
    return {(dz, dq): c for dz, poly in P.items() for dq, c in poly.items()}


def formula(m, x, y, dz_max, dq_max):
    th = kontinuanty(m, x, dz_max, dq_max)
    ph = obratnye(m, x, dz_max, dq_max)
    if x <= y:
        d = y - x
        s = d * (d - 1) // 2
        mon = {(dz + d, dq + s): c for (dz, dq), c in plosko(th[x]).items()
               if dz + d <= dz_max and dq + s <= dq_max}
        num = umnozhenie(mon, plosko(ph[y + 2]), dz_max, dq_max)
    else:
        d = x - y
        num = umnozhenie({(dz + d, dq): c for (dz, dq), c in plosko(th[y]).items()
                          if dz + d <= dz_max},
                         plosko(ph[x + 2]), dz_max, dq_max)
    return delenie(num, plosko(th[m + 1]), dz_max, dq_max)


def brutto_poly(m, x, y, dz_max, dq_max):
    out = defaultdict(int)
    for N in range(dz_max + 1):
        for a, c in q_puti(m, x, y, N).items():
            if a <= dq_max:
                out[(N, a)] += c
    return dict(out)


if __name__ == "__main__":
    bad = tested = 0
    for m in range(1, 7):
        for x in range(m + 1):
            for y in range(m + 1):
                got = formula(m, x, y, 10, 30)
                want = brutto_poly(m, x, y, 10, 30)
                tested += 1
                if got != want:
                    bad += 1
                    if bad <= 5:
                        print("РАСХОЖДЕНИЕ m=%d x=%d y=%d" % (m, x, y))
                        for k in sorted(set(got) | set(want))[:14]:
                            if got.get(k, 0) != want.get(k, 0):
                                print("  ", k, "формула:", got.get(k, 0),
                                      "перебор:", want.get(k, 0))
    print("случаев %d, расхождений %d" % (tested, bad))
