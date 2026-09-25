# -*- coding: utf-8 -*-
"""
Поиск ИССЛЕДОВАТЕЛЬСКИХ задач: семейства с параметром n, у которых
ТИП ОТВЕТА меняется от n (единственный / несколько / нет вовсе).
Это то, что владелец назвал верхней целью листка.
"""
from itertools import product

def sep(t):
    print("\n" + "=" * 76); print(t); print("=" * 76)

def tip(mn):
    if len(mn) == 0: return "ОТВЕТА НЕТ"
    if len(mn) == 1: return f"один ответ: {sorted(mn)[0]}"
    return f"НЕСКОЛЬКО: {sorted(mn)}"


# ---- A. n утверждений, k-е гласит «ровно (k-1) из них ложны», k = 1..n
def A(n):
    res = []
    for w in product([1, 0], repeat=n):          # w[i]=истинно ли (i+1)-е
        lozh = n - sum(w)
        if all(w[k - 1] == (1 if lozh == k - 1 else 0) for k in range(1, n + 1)):
            res.append(tuple(k for k in range(1, n + 1) if w[k - 1]))
    return res

# ---- A'. то же, но k-е гласит «ровно k ложных», k = 1..n
def A2(n):
    res = []
    for w in product([1, 0], repeat=n):
        lozh = n - sum(w)
        if all(w[k - 1] == (1 if lozh == k else 0) for k in range(1, n + 1)):
            res.append(tuple(k for k in range(1, n + 1) if w[k - 1]))
    return res

# ---- B. k-е гласит «НЕ МЕНЕЕ k из них ложны», k = 1..n
def B(n):
    res = []
    for w in product([1, 0], repeat=n):
        lozh = n - sum(w)
        if all(w[k - 1] == (1 if lozh >= k else 0) for k in range(1, n + 1)):
            res.append(n - sum(w))
    return sorted(set(res))

# ---- C. круг, «среди двух соседей ровно один рыцарь»
def C(n):
    out = set()
    for w in product([1, 0], repeat=n):
        ok = True
        for i in range(n):
            s = w[(i - 1) % n] + w[(i + 1) % n]
            if w[i] == 1 and s != 1: ok = False; break
            if w[i] == 0 and s == 1: ok = False; break
        if ok: out.add(sum(w))
    return sorted(out)

# ---- D. круг, «мои соседи одного типа»
def D(n):
    out = set()
    for w in product([1, 0], repeat=n):
        ok = True
        for i in range(n):
            odin = 1 if w[(i - 1) % n] == w[(i + 1) % n] else 0
            if w[i] != odin: ok = False; break
        if ok: out.add(sum(w))
    return sorted(out)

# ---- E. i-й островитянин сказал «среди нас ровно i рыцарей», i = 1..n
def E(n):
    out = set()
    for k in range(n + 1):
        rycari = [i for i in range(1, n + 1) if k == i]
        if len(rycari) == k: out.add(k)
    return sorted(out)

# ---- F. ряд из n, каждый НЕ крайний «мои соседи разных типов» — максимум рыцарей
def F(n):
    best = -1
    dp = {(a, b): a + b for a, b in product([1, 0], repeat=2)}
    for i in range(2, n):
        nd = {}
        for (p, c), k in dp.items():
            for nx in (1, 0):
                if c != (1 if p != nx else 0): continue
                key = (c, nx)
                if key not in nd or nd[key] < k + nx: nd[key] = k + nx
        dp = nd
    return max(dp.values()) if dp else None

# ---- G. каждый из n сказал «среди ОСТАЛЬНЫХ лжецов больше, чем рыцарей»
def G(n):
    out = set()
    for k in range(n + 1):                      # k рыцарей
        # для рыцаря: среди остальных n-1 лжецов (n-k) и рыцарей (k-1)
        ist_r = (n - k) > (k - 1)
        # для лжеца: среди остальных лжецов (n-k-1) и рыцарей k
        ist_l = (n - k - 1) > k
        if k > 0 and not ist_r: continue
        if (n - k) > 0 and ist_l: continue
        out.add(k)
    return sorted(out)

# ---- H. каждый из n сказал «рыцарей среди нас чётное число»
def H(n):
    out = set()
    for k in range(n + 1):
        ist = (k % 2 == 0)
        if k > 0 and not ist: continue
        if (n - k) > 0 and ist: continue
        out.add(k)
    return sorted(out)


if __name__ == "__main__":
    sep("A.  n утверждений: k-е гласит «ровно (k−1) из них ложны»  (формулировка владельца)")
    print("    первое: «все истинны», второе: «ровно одно ложно», …, n-е: «ровно n−1 ложных»")
    for n in range(2, 13):
        r = A(n)
        print(f"   n={n:>2}: {tip(r):<40}")

    sep("A'. то же со сдвигом: k-е гласит «ровно k ложных», k = 1..n   (было у нас в пуле)")
    for n in range(2, 13):
        r = A2(n)
        print(f"   n={n:>2}: {tip(r):<40}")

    sep("B.  k-е гласит «НЕ МЕНЕЕ k из них ложны», k = 1..n")
    for n in range(2, 15):
        r = B(n)
        print(f"   n={n:>2}: число ложных -> {tip(r)}")

    sep("C.  круг: «среди двух моих соседей РОВНО ОДИН рыцарь»")
    for n in range(3, 16):
        r = C(n)
        print(f"   n={n:>2}: число рыцарей -> {tip(r)}")

    sep("D.  круг: «мои соседи — ОДНОГО типа»")
    for n in range(3, 16):
        r = D(n)
        print(f"   n={n:>2}: число рыцарей -> {tip(r)}")

    sep("E.  i-й сказал «среди нас ровно i рыцарей», i = 1..n")
    for n in range(2, 13):
        print(f"   n={n:>2}: {tip(E(n))}")

    sep("F.  ряд из n, «мои соседи разных типов» — МАКСИМУМ рыцарей")
    for n in range(3, 22):
        print(f"   n={n:>2}: максимум {F(n):>2}   (⌈2n/3⌉ = {-(-2*n//3)})")

    sep("G.  каждый: «среди ОСТАЛЬНЫХ лжецов больше, чем рыцарей»")
    for n in range(2, 16):
        print(f"   n={n:>2}: {tip(G(n))}")

    sep("H.  каждый: «рыцарей среди нас ЧЁТНОЕ число»")
    for n in range(2, 16):
        print(f"   n={n:>2}: {tip(H(n))}")
