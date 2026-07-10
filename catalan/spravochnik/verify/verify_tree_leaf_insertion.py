#!/usr/bin/env python3
"""
Верификатор древесной версии раздутия (mir1-skelet §1.6, Утверждение 6).
Биекция «вставить/вырезать лист» на полных бинарных деревьях:
  L̂ = {(ПБД с n внутр. вершинами, ребро-слот [2n рёбер + 1 фантом над корнем], сторона∈{лево,право})},
      |L̂| = (2n+1)·2·C_n = (4n+2)·C_n
  R̂ = {(ПБД с n+1 внутр. вершинами, отмеченный лист)}, |R̂| = (n+2)·C_{n+1}
Проверяем, что вставка листа задаёт БИЕКЦИЮ L̂↔R̂ (каждая пара (дерево, лист) получается ровно раз).
Отсюда (4n+2)C_n = (n+2)C_{n+1} — двучленная рекуррента, дающая C_n = C(2n,n)/(n+1).
Приёмка скелета Мира 1, сессия 2 (2026-07-05): подтверждено для n=0..4.
"""
from collections import Counter

def gen(n):
    """Все ПБД с n внутренними вершинами: None=лист, (l,r)=внутренняя."""
    if n == 0:
        return [None]
    res = []
    for k in range(n):
        for l in gen(k):
            for r in gen(n - 1 - k):
                res.append((l, r))
    return res

def norm(t):
    if t is None: return 'L'
    if t == 'M':  return 'M'          # отмеченный (вставленный) лист
    return (norm(t[0]), norm(t[1]))

def insert_all(T):
    """Все вставки листа: 2 фантомных слота над корнем + по 2 стороны на каждое ребро-поддерево."""
    results = [('M', T), (T, 'M')]     # фантомное корневое ребро, 2 стороны
    def walk(node, rebuild):
        results.append(rebuild(('M', node)))   # разрезать ребро над поддеревом S -> (M,S)
        results.append(rebuild((node, 'M')))   #                                 -> (S,M)
        if node is not None:
            l, r = node
            walk(l, lambda ns, rb=rebuild, rr=r: rb((ns, rr)))
            walk(r, lambda ns, rb=rebuild, ll=l: rb((ll, ns)))
    if T is not None:
        l, r = T
        walk(l, lambda ns, rr=r: (ns, rr))
        walk(r, lambda ns, ll=l: (ll, ns))
    return results

def markleaves(t):
    """Все способы пометить ровно один лист дерева t."""
    if t is None: return ['M']
    l, r = t
    return [(ml, r) for ml in markleaves(l)] + [(l, mr) for mr in markleaves(r)]

if __name__ == '__main__':
    C = lambda n: len(gen(n))
    ok_all = True
    for n in range(0, 5):
        L = []
        for T in gen(n):
            ins = insert_all(T)
            assert len(ins) == 4 * n + 2, (n, len(ins))
            L += [norm(x) for x in ins]
        R = [norm(m) for T2 in gen(n + 1) for m in markleaves(T2)]
        cL, cR = Counter(L), Counter(R)
        bij = (cL == cR) and all(v == 1 for v in cR.values()) and all(v == 1 for v in cL.values())
        ok_all &= bij
        print(f"n={n}: C_n={C(n)} C_(n+1)={C(n+1)} | "
              f"|L|=(4n+2)C_n={len(L)}=={(4*n+2)*C(n)} "
              f"|R|=(n+2)C_(n+1)={len(R)}=={(n+2)*C(n+1)} | биекция: {bij}")
    print("\nИТОГ:", "древесная биекция §1.6 ПОДТВЕРЖДЕНА n=0..4" if ok_all else "ПРОВАЛ")
