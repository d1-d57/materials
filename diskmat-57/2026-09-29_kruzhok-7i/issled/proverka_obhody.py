"""Проверки: обход 5x5 «хромым королём», жуки, 15/17 доминошек, 10x10 на 1x4, уголки разного размера."""
import sys
from tiling import *
sys.setrecursionlimit(10000)

# ---------- Задача 8: гамильтонов путь по соседним по стороне клеткам 5x5
print("== Задача 8: обход 5x5 по соседним клеткам, каждая клетка по разу")
N = 5


def ham_from(start):
    seen = {start}

    def dfs(v):
        if len(seen) == N * N:
            return True
        r, c = v
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (r + dr, c + dc)
            if 0 <= q[0] < N and 0 <= q[1] < N and q not in seen:
                seen.add(q)
                if dfs(q):
                    return True
                seen.remove(q)
        return False
    return dfs(start)

for r in range(N):
    print(" ".join("да " if ham_from((r, c)) else "нет" for c in range(N)))

# ---------- Задача 9: жуки на 5x5 -- минимальное число пустых клеток после перелёта
# Каждый жук -- на соседнюю клетку. Мин. число пустых = 25 - (макс. число занятых клеток).
# Занятые клетки = образ отображения; максимум образа = размер максимального «покрытия»...
# Проще: проверим, что ровно одну пустую получить можно (перебором с паросочетанием).
print("\n== Задача 9: жуки 5x5")
# Ищем отображение f: клетки -> соседние, у которого образ имеет 24 клетки.
# Эквивалентно: найти паросочетание из 24 рёбер в двудольном графе (клетка-жук -> клетка-место),
# остальные жуки (1 штука) летят куда угодно.
import itertools
cells = [(r, c) for r in range(N) for c in range(N)]
nbr = {v: [(v[0] + dr, v[1] + dc) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
           if 0 <= v[0] + dr < N and 0 <= v[1] + dc < N] for v in cells}


def max_matching():
    match = {}  # место -> жук

    def try_(u, vis):
        for w in nbr[u]:
            if w in vis:
                continue
            vis.add(w)
            if w not in match or try_(match[w], vis):
                match[w] = u
                return True
        return False
    return sum(try_(u, set()) for u in cells)
m = max_matching()
print("максимум занятых клеток:", m, "-> минимум пустых:", N * N - m)

# ---------- Задача 12*: 8x8 доминошки, число вертикальных всегда чётно
print("\n== Задача 12*: распределение числа вертикальных доминошек на 8x8")
from functools import lru_cache
H, W = 8, 8
# профильная ДП по столбцам слева направо: состояние -- маска выступающих горизонталей
from collections import defaultdict


def col_fill(mask_in):
    """mask_in -- занятые клетки текущего столбца (выступы из прошлого).
    возвращает список (mask_out, verticals) для заполнения столбца."""
    res = []

    def go(r, out, v):
        if r == H:
            res.append((out, v)); return
        if mask_in >> r & 1:
            go(r + 1, out, v); return
        # горизонталь выступает в следующий столбец
        go(r + 1, out | (1 << r), v)
        # вертикаль
        if r + 1 < H and not (mask_in >> (r + 1) & 1):
            go(r + 2, out, v + 1)
    go(0, 0, 0)
    return res

dist = {(0, 0): 1}  # (mask, verticals) -> count
for col in range(W):
    nd = defaultdict(int)
    for (mask, v), k in dist.items():
        for out, dv in col_fill(mask):
            nd[(out, v + dv)] += k
    dist = nd
final = defaultdict(int)
for (mask, v), k in dist.items():
    if mask == 0:
        final[v] += k
print("всего замощений:", sum(final.values()))
print("число вертикальных -> число замощений:", dict(sorted(final.items())))
print("бывает ли нечётное число вертикальных:", any(v % 2 for v in final))

# ---------- Резерв: 10x10 на полоски 1x4 (контроль)
print("\n== Резерв: 10x10 на 1x4 и 6x6 на 1x4")
print("6x6 на 1x4:", count_tilings(rect(6, 6), [I4]))
print("10x10 на 1x4:", count_tilings(rect(10, 10), [I4]))

# ---------- Резерв: 5x5 на уголки разных размеров (уголок: две «ножки» >=2 клеток, общая угловая клетка)
print("\n== Резерв: 5x5 на уголки попарно разного числа клеток")


def corners_shapes():
    shapes = []
    for a in range(2, 6):
        for b in range(2, 6):
            sh = [(0, j) for j in range(a)] + [(i, 0) for i in range(1, b)]
            shapes.append(sh)
    return shapes
shapes = corners_shapes()
allpl = []
for sh in shapes:
    for o in orientations(sh):
        allpl.append((len(o), anchored(o)))
cellsR = sorted(rect(5, 5)); idx = {x: i for i, x in enumerate(cellsR)}
by = []
for (r, c) in cellsR:
    lst = []
    for size, a in allpl:
        s = [(r + dr, c + dc) for dr, dc in a]
        if all(x in idx for x in s):
            lst.append((size, frozenset(s)))
    by.append(lst)
found = []


def rec(cov, used, tiles):
    if found:
        return
    if len(cov) == 25:
        found.append(list(tiles)); return
    i = next(k for k in range(25) if cellsR[k] not in cov)
    for size, t in by[i]:
        if size in used or t & cov:
            continue
        tiles.append(t); rec(cov | t, used | {size}, tiles); tiles.pop()
rec(frozenset(), frozenset(), [])
if found:
    print(draw(5, 5, found[0]), "\nразмеры:", sorted(len(t) for t in found[0]))
else:
    print("нет")
