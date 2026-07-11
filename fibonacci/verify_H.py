#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_H.py — отдельная численная сверка спицы H (курс «Числа Фибоначчи», Л1).

НЕ трогает verify_skelet.py (тот верен и сверен). Здесь закрываем ТОЛЬКО флаг H_n
из kotly/matematika.md (Утв.8): буквальное определение H_n даёт f_{n-1}, а не f_n.

H_n = блуждания по пути-графу 1—2—3—4 (соседние цифры отличаются на 1), старт в 1.
  • буквально (строки ДЛИНЫ n)      → |H_n| = f_{n-1}   (ошибка индекса листка)
  • исправлено (строки ДЛИНЫ n+1)   → |H_n| = f_n        (H — полноценная спица)

Запуск:  python3 fibonacci/verify_H.py   (чистая stdlib, без сети)
Выход:   таблица + PASS/FAIL по сверке |H_n(испр.)| = f_n на n = 0..12.
"""

NEIGH = {1: (2,), 2: (1, 3), 3: (2, 4), 4: (3,)}  # путь P4: рёбра 1-2, 2-3, 3-4


def fib(n):
    a, b = 1, 1            # f_0 = 1, f_1 = 1 (нумерация курса: f_n = |A_n|)
    for _ in range(n):
        a, b = b, a + b
    return a


def count_walks(length):
    """Число строк заданной ДЛИНЫ над {1,2,3,4}: старт 1, соседние — соседи в P4."""
    if length <= 0:
        return 0
    ways = {1: 1}                       # позиция 0 закреплена в вершине 1
    for _ in range(length - 1):
        nxt = {}
        for v, c in ways.items():
            for u in NEIGH[v]:
                nxt[u] = nxt.get(u, 0) + c
        ways = nxt
    return sum(ways.values())


def H_literal(n):   # листок «как написано»: длина n
    return count_walks(n)


def H_fixed(n):     # исправление §3 захода: длина n+1 → |H_n| = f_n
    return count_walks(n + 1)


def main():
    NMAX = 12
    print("n :   f_n | H_lit(len n)=f_{n-1} | H_fix(len n+1)=f_n")
    ok = True
    for n in range(0, NMAX + 1):
        fn, hl, hf = fib(n), H_literal(n), H_fixed(n)
        lit_ok = (hl == (fib(n - 1) if n >= 1 else 0))
        fix_ok = (hf == fn)
        ok = ok and fix_ok and lit_ok
        mark = "✓" if fix_ok else "✗"
        print("%2d : %5d | %18d | %14d  %s" % (n, fn, hl, hf, mark))
    print("-" * 52)
    if ok:
        print("PASS · H_fix (длина n+1) даёт ровно f_n на n=0..%d; H_lit подтверждает f_{n-1}." % NMAX)
        return 0
    print("FAIL · сверка H не сошлась — проверь определение.")
    return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
