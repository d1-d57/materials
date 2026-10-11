"""Поиск КОМПАКТНЫХ фигур с единственным разрезанием на k равных частей.
Фигура = прямоугольник h x w, у которого с краёв срезано несколько клеток (без дыр, без «усиков»).
Перебор по всем свободным m-мино (m = площадь / k). Годится: ровно одно разрезание,
часть — не прямоугольник и не полоска. Запуск: python3 poisk_kompakt.py k попыток seed"""
import sys, random, json
from tiling import count_tilings
from poisk_figur import free_polys, has_hole

def conn(S):
    S = set(S); st = [next(iter(S))]; seen = {st[0]}
    while st:
        r, c = st.pop()
        for d in ((1,0),(-1,0),(0,1),(0,-1)):
            q = (r+d[0], c+d[1])
            if q in S and q not in seen: seen.add(q); st.append(q)
    return len(seen) == len(S)

k, N, seed = map(int, sys.argv[1:4])
rnd = random.Random(seed)
POLY = {}
found = []
for t in range(N):
    h, w = rnd.randint(4, 6), rnd.randint(4, 7)
    F = {(r, c) for r in range(h) for c in range(w)}
    for _ in range(rnd.randint(2, 7)):
        edge = [x for x in F if any((x[0]+a, x[1]+b) not in F for a, b in ((1,0),(-1,0),(0,1),(0,-1)))]
        x = rnd.choice(edge); G = F - {x}
        if conn(G): F = G
    if len(F) % k or has_hole(F): continue
    if any(sum((x[0]+a, x[1]+b) in F for a, b in ((1,0),(-1,0),(0,1),(0,-1))) <= 1 for x in F): continue
    m = len(F) // k
    if not 5 <= m <= 8: continue
    if m not in POLY: POLY[m] = [P for P in free_polys(m)
                                  if len({r for r,c in P}) * len({c for r,c in P}) != m]  # не прямоугольник
    tot, ex = 0, None
    for Q in POLY[m]:
        n, e = count_tilings(F, [Q], want_example=True)
        tot += n
        if n: ex = e
        if tot > 1: break
    if tot != 1: continue
    # прямоугольные части тоже считаем: если фигура режется ещё и на прямоугольники — не берём
    from tiling import rect
    rects = [[(r, c) for r in range(a) for c in range(m // a)] for a in range(1, m + 1) if m % a == 0]
    if any(count_tilings(F, [R]) for R in rects): continue
    found.append({"F": sorted(F), "tiles": ex, "k": k, "m": m})
    print("НАЙДЕНО", len(found), "площадь", len(F), "часть", m, flush=True)
    json.dump(found, open(f"kompakt_k{k}_s{seed}.json", "w"))
    if len(found) >= 12: break
json.dump(found, open(f"kompakt_k{k}_s{seed}.json", "w"))
