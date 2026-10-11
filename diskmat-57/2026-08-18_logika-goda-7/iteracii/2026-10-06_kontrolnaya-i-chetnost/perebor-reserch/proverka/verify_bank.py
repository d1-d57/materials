"""Проверка банка задач на перебор. Каждая задача: brute() — перебор из определения,
hand — список, как он будет записан в банке (в нормальной форме и порядке),
succ() — «правило следующего», вычисляемое локально (без знания списка), где оно есть.
Проверяем: (1) |hand| = ответ; (2) нет повторов; (3) set(hand) == set(brute);
(4) hand идёт в заявленном порядке; (5) если есть succ — итерация succ от первого даёт ровно hand."""
import sys
from itertools import combinations, permutations, product

RESULTS = {}

def check(tid, answer, hand, brute, key=None, succ=None, note=""):
    ok = True
    msgs = []
    if len(hand) != answer:
        ok = False; msgs.append(f"len(hand)={len(hand)} != {answer}")
    if len(set(hand)) != len(hand):
        ok = False; msgs.append("повторы в hand")
    if set(hand) != set(brute):
        ok = False
        msgs.append(f"hand-brute={sorted(set(hand)-set(brute))} brute-hand={sorted(set(brute)-set(hand))}")
    if len(set(brute)) != answer:
        ok = False; msgs.append(f"brute дал {len(set(brute))}")
    if key is not None and list(hand) != sorted(hand, key=key):
        ok = False; msgs.append("порядок hand не совпадает с ключом")
    if succ is not None:
        seq = [hand[0]]
        while True:
            n = succ(seq[-1])
            if n is None: break
            seq.append(n)
            if len(seq) > 1000: break
        if seq != list(hand):
            ok = False; msgs.append(f"succ-итерация расходится: {seq}")
    RESULTS[tid] = ok
    print(f"[{tid}] {'OK' if ok else 'FAIL'} answer={answer} {note} {'; '.join(msgs)}")
    return ok

def S(s):
    """'13 22 31' -> ['13','22','31']"""
    return s.split()

# ---------- функции-преемники ----------
def succ_partition_desc(p):
    """p: кортеж слагаемых по убыванию; следующее в обратном словарном порядке."""
    p = list(p)
    # убрать хвостовые единицы
    ones = 0
    while p and p[-1] == 1:
        p.pop(); ones += 1
    if not p: return None
    x = p.pop() - 1
    rest = ones + 1
    p.append(x)
    while rest > x:
        p.append(x); rest -= x
    if rest: p.append(rest)
    return tuple(p)

def partitions(n, maxpart=None):
    if maxpart is None: maxpart = n
    if n == 0: yield (); return
    for k in range(min(n, maxpart), 0, -1):
        for r in partitions(n - k, k):
            yield (k,) + r

def succ_comb(c, n):
    """c: возрастающий кортеж из 1..n; следующий в словарном порядке."""
    c = list(c); k = len(c)
    i = k - 1
    while i >= 0 and c[i] == n - (k - 1 - i):
        i -= 1
    if i < 0: return None
    c[i] += 1
    for j in range(i + 1, k): c[j] = c[j - 1] + 1
    return tuple(c)

def succ_odometer(t, alphabets):
    t = list(t)
    for i in range(len(t) - 1, -1, -1):
        a = alphabets[i]; j = a.index(t[i])
        if j + 1 < len(a):
            t[i] = a[j + 1]
            return tuple(t)
        t[i] = a[0]
    return None

def succ_word(w, alphabet):
    """следующая перестановка мультимножества в словарном порядке по alphabet (next_permutation)."""
    idx = [alphabet.index(ch) for ch in w]
    i = len(idx) - 2
    while i >= 0 and idx[i] >= idx[i + 1]: i -= 1
    if i < 0: return None
    j = len(idx) - 1
    while idx[j] <= idx[i]: j -= 1
    idx[i], idx[j] = idx[j], idx[i]
    idx[i + 1:] = reversed(idx[i + 1:])
    return "".join(alphabet[k] for k in idx)

if __name__ == "__main__":
    print("library ok")
