"""Проверки головоломок лестницы «Раскраски» (черновик)."""
from itertools import product
from tiling import *

# ---------- Задача 2: квадрат 4x4 на две равные части по линиям сетки
print("== Задача 2: 4x4 на две равные части")
N = 4
cells = [(r, c) for r in range(N) for c in range(N)]
ALL = frozenset(cells)


def connected(S):
    S = set(S)
    if not S:
        return False
    st = [next(iter(S))]; seen = {st[0]}
    while st:
        r, c = st.pop()
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (r + d[0], c + d[1])
            if q in S and q not in seen:
                seen.add(q); st.append(q)
    return len(seen) == len(S)


def isos(cellsS):
    return {norm(o) for o in orientations(list(cellsS), mirror=True)}

from itertools import combinations
parts = set()
for comb in combinations(cells, 8):
    S = frozenset(comb)
    if (0, 0) not in S:
        continue  # чтобы не считать пару дважды
    T = ALL - S
    if connected(S) and connected(T) and norm(list(T)) in isos(S):
        parts.add(S)
print("разбиений (как множеств-пар):", len(parts))


def sym_images(S):
    res = []
    for k in range(8):
        img = set()
        for r, c in S:
            rr, cc = r, c
            if k >= 4:
                cc = N - 1 - cc
            for _ in range(k % 4):
                rr, cc = cc, N - 1 - rr
            img.add((rr, cc))
        res.append(frozenset(img))
    return res

classes = set()
for S in parts:
    T = ALL - S
    key = min(tuple(sorted(x)) for X in (S, T) for x in sym_images(X))
    classes.add(key)
print("с точностью до поворотов/отражений квадрата:", len(classes))
for key in sorted(classes):
    S = set(key)
    print("\n".join("".join("X" if (r, c) in S else "." for c in range(N)) for r in range(N)))
    print()

# ---------- Задача 3: уголок из трёх квадратов 2x2 -> 4 уголка-тримино
print("== Задача 3: уголок из 12 клеток на 4 равные части (уголки по 3 клетки)")
Lbig = {(r, c) for r in range(4) for c in range(4) if not (r < 2 and c >= 2)}
n, ex = count_tilings(Lbig, [L3], want_example=True)
print("разбиений на уголки-тримино:", n)
print(draw(4, 4, ex))
# а на 4 равные части любой формы (по 3 клетки, связные)? -- переберём все тримино
print("на 4 полоски 1x3:", count_tilings(Lbig, [I3]))

# ---------- Задача 4: раскраска 4x4: у чёрной ровно 3 белых соседа, у белой ровно 1 чёрный
print("\n== Задача 4: раскраска 4x4 (чёрная: 3 белых соседа; белая: 1 чёрный сосед)")
sols = []
for bits in product([0, 1], repeat=16):
    g = [bits[4 * r:4 * r + 4] for r in range(4)]
    ok = True
    for r in range(4):
        for c in range(4):
            nb = [g[r + dr][c + dc] for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
                  if 0 <= r + dr < 4 and 0 <= c + dc < 4]
            if g[r][c] == 1 and nb.count(0) != 3:
                ok = False; break
            if g[r][c] == 0 and nb.count(1) != 1:
                ok = False; break
        if not ok:
            break
    if ok:
        sols.append(g)
print("решений:", len(sols))
for g in sols:
    print("\n".join("".join("#" if x else "." for x in row) for row in g)); print()

# ---------- Задача 4-альт: каждая клетка имеет ровно одного закрашенного соседа (по стороне)
print("== Резерв: 4x4, у каждой клетки ровно один закрашенный сосед")
cnt = 0; first = None
for bits in product([0, 1], repeat=16):
    g = [bits[4 * r:4 * r + 4] for r in range(4)]
    if all(sum(g[r + dr][c + dc] for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
               if 0 <= r + dr < 4 and 0 <= c + dc < 4) == 1 for r in range(4) for c in range(4)):
        cnt += 1; first = first or g
print("решений:", cnt)
if first:
    print("\n".join("".join("#" if x else "." for x in row) for row in first))

# ---------- Задача 5: 6x6 на уголки-тримино, никакие два не образуют прямоугольник 2x3
print("\n== Задача 5: 6x6 на уголки, без прямоугольника 2x3 из двух уголков")
region = rect(6, 6)
cellsR = sorted(region); idx = {x: i for i, x in enumerate(cellsR)}
pl = []
for o in orientations(L3):
    a = anchored(o)
    pl.append(a)
by = []
for (r, c) in cellsR:
    lst = []
    for a in pl:
        sh = [(r + dr, c + dc) for dr, dc in a]
        if all(s in idx for s in sh):
            lst.append(frozenset(sh))
    by.append(lst)
rects23 = set()
for r in range(6):
    for c in range(6):
        for h, w in ((2, 3), (3, 2)):
            R = frozenset((r + i, c + j) for i in range(h) for j in range(w))
            if all(x in idx for x in R):
                rects23.add(R)
sol = []
found = []


def rec(covered, tiles):
    if len(covered) == 36:
        found.append(list(tiles)); return
    i = next(k for k in range(36) if cellsR[k] not in covered)
    for t in by[i]:
        if t & covered:
            continue
        if any((t | u) in rects23 for u in tiles):
            continue
        tiles.append(t); rec(covered | t, tiles); tiles.pop()

rec(frozenset(), [])
print("разбиений:", len(found))
if found:
    print(draw(6, 6, found[0]))
# всего разбиений 6x6 на уголки без ограничения
print("(для сравнения: всего разбиений 6x6 на уголки:", count_tilings(rect(6, 6), [L3]), ")")

# ---------- Задача 1: 7x7, в каждой строке и столбце ровно по 3 закрашенных
print("\n== Задача 1: пример 7x7 по три в строке/столбце")
g = [[1 if (c - r) % 7 in (0, 1, 2) else 0 for c in range(7)] for r in range(7)]
assert all(sum(row) == 3 for row in g) and all(sum(g[r][c] for r in range(7)) == 3 for c in range(7))
print("\n".join("".join("#" if x else "." for x in row) for row in g))
