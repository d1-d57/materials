#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_models.py — численная сверка Л1-«серии моделей» (заход §3, критерий готовности).
НЕ трогает verify_skelet.py / verify_H.py (оба верны и сверены) — только добавляет.

Закрывает три вещи, на которых стоит движок сцен (sims/lab.core.js) и слайд s13-zeck:
  1) счёт: |A_n|=|B_n|=|C_n|=|F_n|=|H_n(len n+1)| = f_n     (нативные определения листка);
  2) образы-биекции движка (code/subset/perm от замощения) дают РОВНО нативные C_n/B_n/F_n;
  3) рекуррента-по-первому-элементу — корректное разбиение Y≅X_{n-1} ⊔ Z≅X_{n-2} для каждой модели;
  4) биекция Цекендорфа (§3.13, задача 5в): a ↦ 1 + Σ_p (1−a_p)·f_p  — РОВНО {1..f_n} на C_n
     (соглашение: вес позиции p (1..n) = f_p различных Фибоначчи 1,2,3,5,8…; смещение +1 — иначе {0..f_n−1}).

Запуск:  python3 fibonacci/verify_models.py   (чистая stdlib, без сети)
"""
from itertools import permutations


def fib(n):                       # курсовая нумерация: f_0=1,f_1=1,f_2=2,f_3=3,f_4=5,…
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# ───────────────────────── модель-носитель: замощения 1×n ─────────────────────────
def enum_tilings(n):              # квадрат=1, доминошка=2; квадрато-первые впереди (как в JS)
    if n <= 0:
        return [()]
    if n == 1:
        return [(1,)]
    return [(1,) + t for t in enum_tilings(n - 1)] + [(2,) + t for t in enum_tilings(n - 2)]


# образы движка (дословно из sims/lab.core.js) — сверяем, что они дают нативные множества
def code(parts):                  # квадрат→'1', доминошка→'01'
    return "".join('1' if x == 1 else '01' for x in parts)


def subset(parts):                # левые края доминошек (1-based)
    pos, s = 1, []
    for x in parts:
        if x == 2:
            s.append(pos)
        pos += x
    return tuple(s)


def perm(parts):                  # квадрат→неподвижная, доминошка→соседняя транспозиция
    pi, i = [], 1
    for x in parts:
        if x == 1:
            pi.append(i); i += 1
        else:
            pi.append(i + 1); pi.append(i); i += 2
    return tuple(pi)


# ───────────────────────── нативные определения листка (независимо от замощений) ─────────────────────────
def native_C(n):                  # 0/1 длины n, без «00», кончаются на 1
    out = []
    for x in range(2 ** n) if n > 0 else [0]:
        s = "".join(str((x >> i) & 1) for i in range(n))
        if n >= 1 and (s[-1] != '1' or "00" in s):
            continue
        out.append(s)
    return set(out)


def native_B(n):                  # подмножества {1..n−1} без двух соседних
    els = list(range(1, n))
    out = set()
    for mask in range(2 ** len(els)):
        sub = tuple(els[i] for i in range(len(els)) if (mask >> i) & 1)
        if all(sub[i + 1] - sub[i] >= 2 for i in range(len(sub) - 1)):
            out.add(sub)
    return out


def native_F(n):                  # перестановки {1..n}, |π(i)−i| ≤ 1
    return set(p for p in permutations(range(1, n + 1)) if all(abs(p[i] - (i + 1)) <= 1 for i in range(n)))


NEIGH = {1: (2,), 2: (1, 3), 3: (2, 4), 4: (3,)}


def native_H(length):             # строки длины `length` над {1..4}, старт 1, соседние — соседи в P4
    if length <= 0:
        return set()
    res = {(1,)}
    for _ in range(length - 1):
        res = {w + (u,) for w in res for u in NEIGH[w[-1]]}
    return res


# ───────────────────────── проверки ─────────────────────────
def check_counts(NMAX):
    ok = True
    print("n :  f_n | A   C   B   F   H(len n+1)")
    for n in range(0, NMAX + 1):
        fn = fib(n)
        a = len(enum_tilings(n))
        c = len(native_C(n))
        b = len(native_B(n))
        f = len(native_F(n)) if n <= 8 else fn  # n! — считаем нативно до 8
        h = len(native_H(n + 1))
        row_ok = (a == fn and c == fn and b == fn and (n > 8 or f == fn) and h == fn)
        ok = ok and row_ok
        print("%2d : %4d | %-3d %-3d %-3d %-3d %-3d  %s" % (n, fn, a, c, b, f, h, "✓" if row_ok else "✗"))
    return ok


def check_images(NMAX):           # образы движка = нативные множества (биекции корректны)
    ok = True
    for n in range(0, NMAX + 1):
        T = enum_tilings(n)
        img_C = set(code(t) for t in T)
        img_B = set(subset(t) for t in T)
        img_F = set(perm(t) for t in T)
        good = (len(img_C) == len(T) == fib(n) and img_C == native_C(n)
                and len(img_B) == len(T) and img_B == native_B(n)
                and len(img_F) == len(T) and img_F == native_F(n))
        ok = ok and good
    print("образы движка code/subset/perm = нативные C_n/B_n/F_n (n≤%d, инъективно): %s" % (NMAX, "✓" if ok else "✗"))
    return ok


def check_split(NMAX):            # рекуррента-по-первому: Y≅X_{n-1} ⊔ Z≅X_{n-2}
    ok = True
    for n in range(2, NMAX + 1):
        T = enum_tilings(n)
        Y = [t for t in T if t[0] == 1]        # первый — квадрат
        Z = [t for t in T if t[0] == 2]        # первый — доминошка
        recon = (sorted(t[1:] for t in Y) == sorted(enum_tilings(n - 1))
                 and sorted(t[1:] for t in Z) == sorted(enum_tilings(n - 2))
                 and len(Y) + len(Z) == len(T) == fib(n))
        # C_n: '1'+C_{n-1}  ⊔  '01'+C_{n-2}
        C = native_C(n)
        cY = set(s for s in C if s[0] == '1')
        cZ = set(s for s in C if s[:2] == '01')
        c_ok = (cY | cZ == C and len(cY) + len(cZ) == len(C)
                and set(s[1:] for s in cY) == native_C(n - 1)
                and set(s[2:] for s in cZ) == native_C(n - 2))
        ok = ok and recon and c_ok
    print("split «по первому элементу» A и C: Y≅X_{n-1} ⊔ Z≅X_{n-2} (n≤%d): %s" % (NMAX, "✓" if ok else "✗"))
    return ok


def zeck_value(s):                # a ↦ 1 + Σ_p (1−a_p)·f_p ; вес позиции p(1-based) = fib(p) различных Фибоначчи
    return 1 + sum((1 - int(ch)) * fib(p + 1) for p, ch in enumerate(s))


def check_zeck(NMAX):             # задача 5в: биекция C_n → {1..f_n}
    ok = True
    for n in range(1, NMAX + 1):
        vals = sorted(zeck_value(s) for s in native_C(n))
        good = (vals == list(range(1, fib(n) + 1)))
        ok = ok and good
    print("биекция Цекендорфа a↦1+Σ(1−a_p)f_p : C_n → {1..f_n} ровно (n≤%d): %s" % (NMAX, "✓" if ok else "✗"))
    return ok


def main():
    NMAX = 10
    print("──────── verify_models (Л1 серия моделей) ────────")
    r1 = check_counts(NMAX)
    print("-" * 46)
    r2 = check_images(NMAX)
    r3 = check_split(NMAX)
    r4 = check_zeck(NMAX)
    print("-" * 46)
    if r1 and r2 and r3 and r4:
        print("PASS · счёт=f_n, образы-биекции верны, split корректен, Цекендорф = {1..f_n}.")
        return 0
    print("FAIL · см. строки со ✗ выше.")
    return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
