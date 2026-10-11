"""Листок 6.10 «Раскраски и разрезания»: проверка перебором ВСЕХ утверждений разбора
и выгрузка картинок-решений в dannye_6-10.json (из неё строится HTML-обзор).
Запуск: python3 proverka_6-10.py  → печатает проверки, падает на первом расхождении."""
import json, sys
from fractions import Fraction as F
from itertools import combinations
from tiling import *
sys.setrecursionlimit(10000)
D = {}
def ok(cond, msg):
    print(("OK   " if cond else "FAIL ") + msg)
    if not cond: sys.exit(1)
def tiles_json(tiles): return [[list(c) for c in t] for t in tiles]
blk = lambda c: (c[0] + c[1]) % 2 == 0   # цвет угла (0,0) — «чёрный»

# ---- З1. 4x4 на две равные части (по линиям сетки)
def conn(S):
    S = set(S); st = [next(iter(S))]; seen = {st[0]}
    while st:
        r, c = st.pop()
        for d in ((1,0),(-1,0),(0,1),(0,-1)):
            n = (r+d[0], c+d[1])
            if n in S and n not in seen: seen.add(n); st.append(n)
    return len(seen) == len(S)
SYM = [lambda r,c:(r,c), lambda r,c:(c,3-r), lambda r,c:(3-r,3-c), lambda r,c:(3-c,r),
       lambda r,c:(r,3-c), lambda r,c:(3-r,c), lambda r,c:(c,r), lambda r,c:(3-c,3-r)]
cells = [(r,c) for r in range(4) for c in range(4)]
parts = set()
for A in combinations(cells, 8):
    A = frozenset(A); B = frozenset(cells) - A
    if (0,0) not in A or not conn(A) or not conn(B): continue
    if norm(A) in {norm([s(*x) for x in B]) for s in SYM}: parts.add(A)
canon = {}
for A in parts:
    key = min(tuple(sorted(s(*x) for x in (A if (0,0) in [s(*y) for y in A] else frozenset(cells)-A))) for s in SYM)
    canon.setdefault(key, A)
ok(len(parts) == 22, f"З1: разбиений 4x4 на две равные части: {len(parts)} (ждём 22)")
ok(len(canon) == 6, f"З1: с точностью до поворотов/отражений: {len(canon)} (ждём 6)")
D["z1"] = [sorted(list(c) for c in A) for A in canon.values()]
ok(all(frozenset(cells) - A == frozenset((3-r, 3-c) for r, c in A) for A in parts),
   "З1: во всех 22 разбиениях вторая часть — поворот первой на 180° (разрез центрально-симметричен)")

# ---- З2. 8x8 без двух угловых
n_a, ex = count_tilings(rect(8,8) - {(0,0),(0,7)}, [DOMINO], want_example=True)
n_b = count_tilings(rect(8,8) - {(0,0),(7,7)}, [DOMINO])
ok(n_a == 2436304 and n_b == 0, f"З2: углы одной стороны — {n_a} способов, противоположные — {n_b}")
D["z2a"] = tiles_json(ex)

# ---- З3. уголок из трёх квадратов 2x2
UG = {(r,c) for r in range(4) for c in range(4)} - {(0,2),(0,3),(1,2),(1,3)}
TETRO = {"I":[(0,0),(0,1),(0,2),(0,3)], "O":[(0,0),(0,1),(1,0),(1,1)], "L":[(0,0),(1,0),(2,0),(2,1)],
         "T":T4, "S":[(0,1),(0,2),(1,0),(1,1)]}
cnt3 = {k: count_tilings(UG, [p], want_example=True) for k, p in TETRO.items()}
ok(sum(v[0] for v in cnt3.values()) == 1 and cnt3["O"][0] == 1,
   "З3а: на 3 равные части — только три квадрата 2x2: " + str({k:v[0] for k,v in cnt3.items()}))
D["z3a"] = tiles_json(cnt3["O"][1])
c3L = count_tilings(UG, [L3], want_example=True); c3I = count_tilings(UG, [I3])
ok(c3L[0] == 1 and c3I == 0, f"З3б: на 4 части — уголков {c3L[0]} способ, полосок 1x3 — {c3I}")
D["z3b"] = tiles_json(c3L[1])

# ---- З4. доминошки
n4a, ex = count_tilings(rect(5,5) - {(2,2)}, [DOMINO], want_example=True)
ok(n4a == 196, f"З4а: 5x5 без центра — {n4a} способов")
# картинка «кольцами»: внешнее кольцо 16 клеток и внутреннее 8 режутся по кругу
def ring(k, n):
    out = [(k,c) for c in range(k,n-k)] + [(r,n-k-1) for r in range(k+1,n-k)] + \
          [(n-k-1,c) for c in range(n-k-2,k-1,-1)] + [(r,k) for r in range(n-k-2,k,-1)]
    return out
rings = []
for k in (0,1):
    R = ring(k,5); rings += [[R[i], R[i+1]] for i in range(0, len(R), 2)]
ok(sorted(map(sorted, rings)) == sorted(sorted(t) for t in rings) and
   {c for t in rings for c in t} == rect(5,5)-{(2,2)} and
   all(abs(a[0]-b[0])+abs(a[1]-b[1]) == 1 for a,b in rings), "З4а: разрезание «по кольцам» корректно")
D["z4a"] = tiles_json(rings)
ok(count_tilings(rect(5,5), [DOMINO]) == 0, "З4б: вся 5x5 — 0 способов")
res = {k: count_tilings(rect(k,k) - {(0,0)}, [DOMINO]) for k in (3,4,5,6,7)}
ok(res[3] and res[5] and res[7] and not res[4] and not res[6], f"З4в: n x n без угла: {res}")
# пример 5x5 без угла: первая строка горизонтально, остальное вертикально
t = [[(0,1),(0,2)],[(0,3),(0,4)]] + [[(r,c),(r+1,c)] for c in range(5) for r in (1,3)]
ok({x for d in t for x in d} == rect(5,5)-{(0,0)}, "З4в: схема «строка + столбики» для 5x5 верна")
D["z4v"] = tiles_json(t)

# ---- З5. 4x4: у чёрной 3 белых соседа, у белой 1 чёрный
sols = []
for m in range(1 << 16):
    B = {cells[i] for i in range(16) if m >> i & 1}
    good = True
    for (r,c) in cells:
        nb = [(r+a,c+b) for a,b in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=r+a<4 and 0<=c+b<4]
        kb = sum(x in B for x in nb)
        if ((r,c) in B and len(nb)-kb != 3) or ((r,c) not in B and kb != 1): good = False; break
    if good: sols.append(sorted(B))
ok(len(sols) == 2, f"З5: решений {len(sols)} (два, зеркальные)")
D["z5"] = [list(c) for c in sols[0]]

# ---- З6. обход 5x5 по соседним клеткам
N = 5
def ham(start):
    seen = {start}; path = [start]
    def dfs(v):
        if len(path) == 25: return True
        r, c = v
        for d in ((1,0),(-1,0),(0,1),(0,-1)):
            w = (r+d[0], c+d[1])
            if 0<=w[0]<5 and 0<=w[1]<5 and w not in seen:
                seen.add(w); path.append(w)
                if dfs(w): return True
                seen.discard(w); path.pop()
        return False
    return path[:] if dfs(start) else None
can = {(r,c): ham((r,c)) is not None for r in range(5) for c in range(5)}
ok(all(can[x] == blk(x) for x in can) and sum(can.values()) == 13, "З6: начать можно ровно с 13 клеток цвета угла")
snake = [(r, c if r % 2 == 0 else 4-c) for r in range(5) for c in range(5)]
D["z6"] = [list(x) for x in snake]
D["z6map"] = [[r,c] for (r,c),v in can.items() if v]
D["z6reps"] = [[list(x) for x in ham(st)] for st in [(0,2),(1,1),(2,2)]]

# ---- З7. 7x7 по три
L = [(r,(r+k)%7) for r in range(7) for k in range(3)]
ok(all(sum(1 for x in L if x[0]==i)==3 and sum(1 for x in L if x[1]==i)==3 for i in range(7)), "З7: лесенка 7x7 — по 3 в каждой строке и столбце")
D["z7"] = [list(x) for x in L]

# ---- З8. жуки: 13 «чёрных» жуков → 12 белых клеток; ровно одна пустая достижима
def max_match(left, right, adj):
    mt = {}
    def tr(u, vis):
        for v in adj(u):
            if v in right and v not in vis:
                vis.add(v)
                if v not in mt or tr(mt[v], vis): mt[v] = u; return True
        return False
    return sum(tr(u, set()) for u in left)
nbr = lambda u: [(u[0]+a,u[1]+b) for a,b in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=u[0]+a<5 and 0<=u[1]+b<5]
allc = list(rect(5,5))
mm = max_match(allc, set(allc), nbr)
ok(mm == 24, f"З8: наибольшее число занятых клеток после свистка {mm} → пустых минимум 1")

# ---- З9. 6x6 на уголки без прямоугольника 2x3
n9, _ = count_tilings(rect(6,6), [L3], want_example=True)
def all_tilings(region, piece):
    out = []
    cl = sorted(region)
    pl = [anchored(o) for o in orientations(piece)]
    def rec(free, acc):
        if not free: out.append(list(acc)); return
        r, c = min(free)
        for o in pl:
            sh = [(r+a, c+b) for a,b in o]
            if all(s in free for s in sh):
                acc.append(sh); rec(free - set(sh), acc); acc.pop()
    rec(set(region), [])
    return out
T9 = all_tilings(rect(6,6), L3)
def bad(t):
    for a, b in combinations(t, 2):
        U = set(a) | set(b)
        rs = {x[0] for x in U}; cs = {x[1] for x in U}
        if (max(rs)-min(rs)+1)*(max(cs)-min(cs)+1) == 6: return True
    return False
good9 = [t for t in T9 if not bad(t)]
ok(len(T9) == 162 and len(good9) == 2, f"З9: всего разбиений на уголки {len(T9)}, без 2x3 — {len(good9)}")
D["z9"] = tiles_json(good9[0])
rot = lambda t: sorted(sorted((c, 5 - r) for r, c in p) for p in t)
ok(all(rot(t) == sorted(sorted(p) for p in t) for t in good9), "З9: оба годных разбиения переходят в себя при повороте на 90° («вертушка»)")

# ---- З10. какую клетку вырезать из 5x5
ans = {x: count_tilings(rect(5,5) - {x}, [DOMINO]) for x in allc}
ok(all((ans[x] > 0) == blk(x) for x in allc), "З10: годятся ровно 13 клеток цвета угла: " + str(sorted(set(ans.values()))))
# конструкция через змейку: вырезали клетку на нечётном месте змейки → два куска чётной длины
ok(all(blk(x) == (k % 2 == 0) for k, x in enumerate(snake)), "З10: в змейке клетки цвета угла стоят ровно на нечётных местах (1-е, 3-е, …)")
cut = (1,1); k = snake.index(cut)
D["z10"] = {"cut": list(cut), "tiles": tiles_json([[snake[i], snake[i+1]] for i in list(range(0,k,2)) + list(range(k+1,25,2))])}
ok(all(abs(a[0]-b[0])+abs(a[1]-b[1]) == 1 for a,b in D["z10"]["tiles"]), "З10: пример по змейке для клетки (1,1) в нумерации с нуля — доминошки настоящие")
D["z10map"] = [[r,c] for (r,c) in allc if ans[(r,c)] > 0]

# ---- З11. Т-фигурки
n11, ex = count_tilings(rect(4,4), [T4], want_example=True)
ok(n11 == 2 and count_tilings(rect(6,6), [T4]) == 0 and count_tilings(rect(8,8), [T4]) == 84, "З11: 4x4 — 2, 6x6 — 0, 8x8 — 84")
ok(all(sum(blk(c) for c in pl) in (1,3) for o in orientations(T4) for r in range(4) for cc in range(4)
       for pl in [[(r+a, cc+b) for a,b in o]]), "З11: любая Т на шахматной доске накрывает 1 или 3 чёрные клетки")
D["z11"] = tiles_json(ex)

# ---- З12★. Гомори: 8x8 без любых двух клеток разного цвета режется на доминошки
cyc = [(0,c) for c in range(8)]
for c in range(7, 0, -1):
    rows = range(1, 8) if c % 2 == 1 else range(7, 0, -1)
    cyc += [(r, c) for r in rows]
cyc += [(r, 0) for r in range(7, 0, -1)]
ok(len(cyc) == 64 and len(set(cyc)) == 64 and
   all(abs(a[0]-b[0])+abs(a[1]-b[1]) == 1 for a, b in zip(cyc, cyc[1:] + cyc[:1])), "З12: замкнутая змейка 8x8 — цикл через все 64 клетки")
B8 = [x for x in rect(8,8) if blk(x)]; W8 = [x for x in rect(8,8) if not blk(x)]
bad12 = 0
for b in B8:
    for w in W8:
        rest = rect(8,8) - {b, w}
        if max_match([x for x in rest if blk(x)], {x for x in rest if not blk(x)},
                     lambda u: [(u[0]+a,u[1]+c) for a,c in ((1,0),(-1,0),(0,1),(0,-1))]) != 31: bad12 += 1
ok(bad12 == 0, f"З12: все {len(B8)*len(W8)} пар «чёрная + белая» — остаток режется (паросочетание), исключений {bad12}")
D["z12"] = {"cycle": [list(x) for x in cyc], "cut": [[2,3],[5,5]]}
ok(blk((2,3)) != blk((5,5)), "З12: на картинке вырезаны клетки разного цвета")
i, j = sorted((cyc.index((2,3)), cyc.index((5,5))))
ok((j - i - 1) % 2 == 0 and (64 - (j - i) - 1) % 2 == 0, f"З12: змейка рвётся на куски {j-i-1} и {64-(j-i)-1} клеток — оба чётные")

# ---- З13★. парадокс 64 = 65 (координаты: x вправо, y вверх)
sq = {"tri1": [(0,8),(8,8),(0,5)], "tri2": [(8,8),(8,5),(0,5)],
      "tr1": [(0,0),(5,0),(3,5),(0,5)], "tr2": [(5,0),(8,0),(8,5),(3,5)]}
rc = {"tri1": [(0,0),(8,0),(8,3)], "tri2": [(13,5),(5,5),(5,2)],
      "tr1": [(8,0),(13,0),(13,5),(8,3)], "tr2": [(0,0),(5,2),(5,5),(0,5)]}
area = lambda P: abs(sum(F(P[i][0])*P[(i+1)%len(P)][1] - F(P[i+1-len(P)][0])*P[i][1] for i in range(len(P)))) / 2
ok(sum(area(p) for p in sq.values()) == 64, "З13: четыре куска квадрата дают площадь 64")
sides = lambda P: sorted(round(((P[i][0]-P[i-1][0])**2 + (P[i][1]-P[i-1][1])**2) ** .5, 9) for i in range(len(P)))
ok(all(sides(sq[k]) == sides(rc[k]) for k in sq), "З13: куски прямоугольника те же (совпадают длины сторон)")
gap = [(0,0),(8,3),(13,5),(5,2)]
ok(area(gap) == 1 and F(3,8) != F(2,5), "З13: «диагональ» прямоугольника — ломаная (наклоны 3/8 и 2/5), щель-параллелограмм площади 1")
D["z13"] = {"sq": sq, "rc": rc, "gap": gap}

json.dump(D, open("dannye_6-10.json", "w"), ensure_ascii=False)
print("\nвсё сошлось; данные картинок → issled/dannye_6-10.json")

# ================= v2 (после отзыва владельца 05.10 22:48) =================
D2 = {}
from poisk_figur import free_polys
def all_partitions_count(F, m, stop=2):
    tot, ex = 0, None
    for Q in free_polys(m):
        n, e = count_tilings(F, [Q], want_example=True)
        tot += n
        if n: ex = e
        if tot >= stop: break
    return tot, ex
FIG3 = {(0,2),(0,3),(0,4),(1,0),(1,1),(1,2),(1,3),(1,4),(2,0),(2,1),(2,2),(2,3),(2,4),(3,2),(3,3),(3,4),(4,2),(4,3)}
FIG4 = {(0,3),(0,4),(0,5),(1,1),(1,2),(1,3),(1,4),(1,5),(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),
        (3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(4,2),(4,3),(4,4),(4,5)}
n3, ex3 = all_partitions_count(FIG3, 6)
ok(len(FIG3) == 18 and n3 == 1, f"Ф3: фигура из 18 клеток режется на 3 равные части ровно одним способом (перебор по всем 35 гексамино): {n3}")
n4, ex4 = all_partitions_count(FIG4, 6)
ok(len(FIG4) == 24 and n4 == 1, f"Ф4: фигура из 24 клеток режется на 4 равные части ровно одним способом: {n4}")
D2["fig3"] = {"F": sorted(map(list, FIG3)), "tiles": tiles_json(ex3)}
D2["fig4"] = {"F": sorted(map(list, FIG4)), "tiles": tiles_json(ex4)}
# 4x4 пополам: разрез всегда проходит через центр = центральный квадрат 2x2 никогда не лежит в одной части
C4 = {(1,1),(1,2),(2,1),(2,2)}
ok(all(not (C4 <= A) and not (C4 <= frozenset(cells) - A) for A in parts),
   "П4x4: ни в одном из 22 разбиений центральный квадрат 2x2 не лежит целиком в одной части (разрез идёт через центр)")
ring = frozenset(cells) - C4
has22 = lambda S: any({(r,c),(r+1,c),(r,c+1),(r+1,c+1)} <= set(S) for r in range(3) for c in range(3))
ok(not has22(ring), "П4x4: в рамке 4x4 без центра нет ни одного квадрата 2x2 (довод доказательства)")
# уголки n x n
def one_tiling(region, piece):
    pl = [anchored(o) for o in orientations(piece)]
    free = set(region); acc = []
    def rec():
        if not free: return True
        r, c = min(free)
        for o in pl:
            sh = [(r+a, c+b) for a, b in o]
            if all(s in free for s in sh):
                for s in sh: free.discard(s)
                acc.append(sh)
                if rec(): return True
                acc.pop(); free.update(sh)
        return False
    return acc if rec() else None
ok(count_tilings(rect(3,3), [L3]) == 0, "У: 3x3 на уголки — 0 способов")
ok(all(sum(1 for x in [(0,0),(0,2),(2,0),(2,2)] if x in [(r+a, c+b) for a, b in o]) <= 1
       for o in orientations(L3) for r in range(-2,3) for c in range(-2,3)), "У: уголок не накрывает двух углов квадрата 3x3")
t59 = one_tiling(rect(5,9), L3); t99 = one_tiling(rect(9,9), L3)
ok(t59 is not None and t99 is not None, "У: 5x9 и 9x9 режутся на уголки (найден пример)")
# пример 9x9 = 5x9 (найденный) + 4x9 из прямоугольников 2x3, каждый из двух уголков
low = []
for r0 in (5, 7):
    for c0 in (0, 3, 6):
        low += [[(r0,c0),(r0+1,c0),(r0+1,c0+1)], [(r0,c0+1),(r0,c0+2),(r0+1,c0+2)]]
ok({x for t in t59 + low for x in t} == rect(9,9) and len(t59 + low) == 27, "У: 9x9 = 5x9 + шесть прямоугольников 2x3 — корректное разрезание")
D2["u99"] = tiles_json(t59 + low); D2["u59"] = tiles_json(t59)
ok(count_tilings(rect(6, 6), [L3]) > 0, "У: 6x6 режется на уголки")
json.dump(D2, open("dannye_6-10_v2.json", "w"), ensure_ascii=False)
print("v2: всё сошлось → issled/dannye_6-10_v2.json")
# ---- «поровну, но не режется»: самая маленькая такая фигура — из 6 клеток, и она одна
from tiling import DOMINO as _DOM
POR = {(0,1),(1,0),(1,1),(1,2),(1,3),(2,2)}
ok(sum(blk(x) for x in POR) == 3 and count_tilings(POR, [_DOM]) == 0, "П: фигура из 6 клеток — цветов поровну (3+3), на доминошки не режется")
mal = {m: [P for P in free_polys(m) if 2*sum(blk(x) for x in P) == m and count_tilings(set(map(tuple, P)), [_DOM]) == 0] for m in (2, 4, 6)}
ok(not mal[2] and not mal[4] and len(mal[6]) == 1, "П: из 2 и 4 клеток таких фигур нет, из 6 — ровно одна (с точностью до поворотов и отражений)")
D2["por"] = sorted(map(list, POR))
json.dump(D2, open("dannye_6-10_v2.json", "w"), ensure_ascii=False)
print("П: данные дописаны")
