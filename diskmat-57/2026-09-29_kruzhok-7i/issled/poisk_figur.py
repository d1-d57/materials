"""Поиск «изогнутых» фигур, которые режутся на k равных частей ЕДИНСТВЕННЫМ способом.
Фигура = объединение k копий случайного m-мино; затем полный перебор: для КАЖДОГО свободного
m-мино считаем разрезания фигуры на его копии (повороты и отражения разрешены).
Годится фигура, у которой во всех формах вместе ровно одно разрезание.
Запуск: python3 poisk_figur.py k m попыток seed"""
import sys, random, json
from tiling import count_tilings, orientations, norm

def free_polys(m):
    cur = {((0, 0),)}
    for _ in range(m - 1):
        nxt = set()
        for p in cur:
            for (r, c) in p:
                for d in ((1,0),(-1,0),(0,1),(0,-1)):
                    q = (r+d[0], c+d[1])
                    if q not in p:
                        nxt.add(min(tuple(o) for o in map(lambda o: norm(o), orientations(list(p) + [q]))))
        cur = nxt
    return [list(p) for p in cur]

def has_hole(F):
    rs = [r for r,c in F]; cs = [c for r,c in F]
    box = {(r,c) for r in range(min(rs)-1, max(rs)+2) for c in range(min(cs)-1, max(cs)+2)}
    out = box - F; st = [min(out)]; seen = {st[0]}
    while st:
        r, c = st.pop()
        for d in ((1,0),(-1,0),(0,1),(0,-1)):
            q = (r+d[0], c+d[1])
            if q in out and q not in seen: seen.add(q); st.append(q)
    return len(seen) != len(out)

def build(P, k, rnd):
    F = set(P)
    for _ in range(k - 1):
        for _try in range(200):
            o = rnd.choice(orientations(P))
            a = rnd.choice(sorted(F)); b = rnd.choice(o); d = rnd.choice(((1,0),(-1,0),(0,1),(0,-1)))
            sh = {(a[0]+d[0]+r-b[0], a[1]+d[1]+c-b[1]) for r, c in o}
            if not (sh & F): F |= sh; break
        else: return None
    return F

if __name__ == '__main__':
    k, m, N, seed = map(int, sys.argv[1:5])
    rnd = random.Random(seed)
    polys = free_polys(m)
    cands = [P for P in polys if len({r for r,c in P}) > 1 and len({c for r,c in P}) > 1]  # не полоска
    found = []
    for t in range(N):
        P = rnd.choice(cands); F = build(P, k, rnd)
        if not F or has_hole(F): continue
        rs = [r for r,c in F]; cs = [c for r,c in F]
        h, w = max(rs)-min(rs)+1, max(cs)-min(cs)+1
        if max(h, w) > 2.2 * min(h, w) or max(h, w) > 8: continue
        F = {(r-min(rs), c-min(cs)) for r, c in F}
        tot, ex = 0, None
        for Q in polys:
            n, e = count_tilings(F, [Q], want_example=True)
            tot += n
            if n: ex = e
            if tot > 1: break
        if tot == 1:
            found.append({"F": sorted(F), "tiles": ex, "h": h, "w": w})
            print("НАЙДЕНО", len(found), "размер", h, "x", w, flush=True)
            if len(found) >= 6: break
    json.dump(found, open(f"figury_k{k}_m{m}_s{seed}.json", "w"))
    print("всего найдено", len(found))
