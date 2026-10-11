"""Задачи ассистента 05.10: (1) 6x6 с 12 закрашенными на 4 равные части по 3 закрашенных;
(2) фигура из 10 клеток на 2 равные части, резать можно по диагоналям клеток (модель: клетка = 4 треугольника)."""
from tiling import *
from poisk_figur import free_polys
# (1)
K = {(0,3),(0,5),(1,3),(1,5),(2,2),(2,4),(3,2),(3,5),(4,1),(4,2),(5,0),(5,1)}
sols = []
for Q in free_polys(9):
    n, _ = count_tilings(rect(6,6), [Q], want_example=False), None
    if not n: continue
    # перебор всех разбиений этой формой с проверкой «по 3 закрашенных»
    pl = [anchored(o) for o in orientations(Q)]
    def rec(free, acc):
        if not free:
            sols.append(list(acc)); return
        r, c = min(free)
        for o in pl:
            sh = [(r+a, c+b) for a, b in o]
            if all(s in free for s in sh) and sum(s in K for s in sh) == 3:
                acc.append(sh); rec(free - set(sh), acc); acc.pop()
    rec(set(rect(6,6)), [])
print("(1) разбиений 6x6 на 4 равные части по 3 закрашенных:", len(sols))
for t in sols[:2]:
    lab = {c: "ABCD"[i] for i, p in enumerate(t) for c in p}
    print("\n".join("".join(lab[(r,c)] for c in range(6)) for r in range(6))); print()

# (2) клетка = 4 треугольника (N, E, S, W) по обеим диагоналям; центр треугольника ×6 — целые координаты
FIG = {(0,0),(0,1),(0,2),(1,2),(1,3),(1,4),(1,5),(2,2),(2,3),(2,4)}
cen = {}
for (r, c) in FIG:
    cen[(r,c,'N')] = (6*c+3, 6*r+1); cen[(r,c,'S')] = (6*c+3, 6*r+5)
    cen[(r,c,'W')] = (6*c+1, 6*r+3); cen[(r,c,'E')] = (6*c+5, 6*r+3)
pos = {v: k for k, v in cen.items()}
T = list(cen)
def sosedi(t):
    r, c, s = t
    out = {'N': [(r,c,'E'),(r,c,'W'),(r-1,c,'S')], 'S': [(r,c,'E'),(r,c,'W'),(r+1,c,'N')],
           'W': [(r,c,'N'),(r,c,'S'),(r,c-1,'E')], 'E': [(r,c,'N'),(r,c,'S'),(r,c+1,'W')]}[s]
    return [u for u in out if u in cen]
def svyaz(S):
    S = set(S); st = [next(iter(S))]; seen = {st[0]}
    while st:
        for u in sosedi(st.pop()):
            if u in S and u not in seen: seen.add(u); st.append(u)
    return len(seen) == len(S)
MS = [((1,0),(0,1)), ((0,-1),(1,0)), ((-1,0),(0,-1)), ((0,1),(-1,0)),
      ((-1,0),(0,1)), ((1,0),(0,-1)), ((0,1),(1,0)), ((0,-1),(-1,0))]
resh = set()
for M in MS:
    ap = lambda p: (M[0][0]*p[0] + M[0][1]*p[1], M[1][0]*p[0] + M[1][1]*p[1])
    ts = {(p[0]-ap(q)[0], p[1]-ap(q)[1]) for p in cen.values() for q in cen.values()}
    for t in ts:
        g = {}
        for k, p in cen.items():
            q = ap(p); q = (q[0]+t[0], q[1]+t[1])
            if q in pos: g[k] = pos[q]
        if (M == MS[0] and t == (0, 0)): continue
        inv = {v: k for k, v in g.items()}
        # цепочки: начала — без прообраза; циклы — отдельно
        A = set(); ok_ = True; seen = set()
        for k in T:
            if k in inv: continue
            chain = [k]
            while chain[-1] in g: chain.append(g[chain[-1]])
            if len(chain) % 2: ok_ = False; break
            A |= set(chain[0::2]); seen |= set(chain)
        if not ok_: continue
        rest = [k for k in T if k not in seen]
        # циклы: оба варианта чередования — перебор по компонентам
        cycles = []; used = set()
        for k in rest:
            if k in used: continue
            cyc = [k]; used.add(k)
            while g[cyc[-1]] != k: cyc.append(g[cyc[-1]]); used.add(cyc[-1])
            if len(cyc) % 2: ok_ = False; break
            cycles.append(cyc)
        if not ok_ or len(cycles) > 22: print("пропуск: циклов", len(cycles)); continue
        from itertools import product
        for ch in product((0, 1), repeat=len(cycles)):
            AA = set(A)
            for cyc, b in zip(cycles, ch): AA |= set(cyc[b::2])
            BB = set(T) - AA
            if len(AA) == len(BB) and svyaz(AA) and svyaz(BB):
                resh.add(frozenset([frozenset(AA), frozenset(BB)]))
po_kletkam = [p for p in resh if all(len({s for (r,c,s) in A if (r,c)==x}) in (0,4) for A in p for x in FIG)]
print("(2) разбиений на 2 равные части (треугольники):", len(resh), "; из них только по сторонам клеток:", len(po_kletkam))
for p in list(resh)[:3]:
    A = next(iter(p)); print(sorted(A))
