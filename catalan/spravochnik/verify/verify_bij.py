# -*- coding: utf-8 -*-
# Биекция Теоремы 5 (mir2-statya): помеч. путь Дика (парковочная функция) -> помеч. дерево на {0..n}
# Правило: столбец c = отсортированные метки машин с предпочтением c (снизу вверх).
#          Читаем a_0=0, затем метки по столбцам 1..n подряд.
#          Дети a_{c-1} = метки столбца c. (т.е. родитель столбца c — (c-1)-й прочитанный ярлык)
import itertools

def is_parking(f):
    s = sorted(f)
    return all(s[i] <= i + 1 for i in range(len(f)))

def pf_to_tree(f):
    n = len(f)
    cols = {c: sorted([i + 1 for i in range(n) if f[i] == c]) for c in range(1, n + 1)}
    a = [0]
    for c in range(1, n + 1):
        a.extend(cols[c])          # a = [0, метки столбца1, столбца2, ...]
    edges = set()
    for c in range(1, n + 1):
        parent = a[c - 1]
        for child in cols[c]:
            edges.add(frozenset((parent, child)))
    return frozenset(edges), a, cols

def is_tree(edges, n):
    # n рёбер на n+1 вершинах, связный, ациклический
    verts = set(range(n + 1))
    if len(edges) != n:
        return False
    # union-find
    par = {v: v for v in verts}
    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for e in edges:
        u, v = tuple(e)
        ru, rv = find(u), find(v)
        if ru == rv:
            return False          # цикл
        par[ru] = rv
    return len({find(v) for v in verts}) == 1   # связный

ok = True
for n in [3, 4]:
    pfs = [f for f in itertools.product(range(1, n + 1), repeat=n) if is_parking(f)]
    trees = {}
    all_trees_valid = True
    for f in pfs:
        e, a, cols = pf_to_tree(f)
        if not is_tree(e, n):
            all_trees_valid = False
        trees[e] = f
    exp = (n + 1) ** (n - 1)
    inj = (len(trees) == len(pfs))
    print(f"n={n}: парковок {len(pfs)} (ожид {exp}) | различных деревьев {len(trees)} (ожид {exp}) | "
          f"все — деревья: {all_trees_valid} | инъективно: {inj}")
    ok = ok and (len(pfs) == exp) and (len(trees) == exp) and all_trees_valid and inj

# полнота для n=3: получаем ли ВСЕ 16 помеченных деревьев на {0,1,2,3}?
def all_labeled_trees(m):   # деревья на {0..m}, через код Прюфера
    from itertools import product
    verts = list(range(m + 1))
    res = set()
    if m == 0:
        return {frozenset()}
    if m == 1:
        return {frozenset({frozenset((0, 1))})}
    for seq in product(verts, repeat=m - 1):   # код Прюфера длины (m+1)-2 = m-1
        deg = {v: 1 for v in verts}
        for x in seq:
            deg[x] += 1
        edges = set()
        s = seq
        import heapq
        leaves = [v for v in verts if deg[v] == 1]
        heapq.heapify(leaves)
        d = dict(deg)
        for x in s:
            leaf = heapq.heappop(leaves)
            edges.add(frozenset((leaf, x)))
            d[x] -= 1
            if d[x] == 1:
                heapq.heappush(leaves, x)
        u = [v for v in verts if d[v] == 1]
        edges.add(frozenset((u[0], u[1])))
        res.add(frozenset(edges))
    return res

for n in [3, 4]:
    pfs = [f for f in itertools.product(range(1, n + 1), repeat=n) if is_parking(f)]
    got = {pf_to_tree(f)[0] for f in pfs}
    full = all_labeled_trees(n)
    print(f"n={n}: покрыты ВСЕ помеченные деревья на " + "{0.." + str(n) + "}: " + str(got == full))
    ok = ok and (got == full)

e, a, cols = pf_to_tree((1, 3, 1, 1))
print("\nf=(1,3,1,1): столбцы =", {k: v for k, v in cols.items() if v},
      "| чтение a =", a, "| рёбра =", sorted(tuple(sorted(x)) for x in e))
print("ожидалось рёбра = [(0,1),(0,3),(0,4),(2,3)]")

print("\nИТОГ: биекция подтверждена全" if ok else "\nИТОГ: ЕСТЬ ПРОБЛЕМА")
