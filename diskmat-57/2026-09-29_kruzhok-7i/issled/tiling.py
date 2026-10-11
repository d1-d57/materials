"""Общий счётчик замощений клетчатых фигур полимино (перебор с мемоизацией по маске).
Фигура -- множество клеток (r,c). Фигурки -- список полимино; берутся все повороты/отражения
(или только повороты, если mirror=False)."""
from functools import lru_cache


def norm(cells):
    mr = min(r for r, c in cells); mc = min(c for r, c in cells)
    return tuple(sorted((r - mr, c - mc) for r, c in cells))


def orientations(piece, mirror=True):
    res = set()
    cur = list(piece)
    for flip in ([False, True] if mirror else [False]):
        p = [(r, -c) for r, c in cur] if flip else cur
        for _ in range(4):
            p = [(c, -r) for r, c in p]
            res.add(norm(p))
    return [list(o) for o in res]


def anchored(o):
    """сдвинуть ориентацию так, чтобы её первая (в порядке строк) клетка была (0,0)"""
    o = sorted(o)
    r0, c0 = o[0]
    return [(r - r0, c - c0) for r, c in o]


def count_tilings(region, pieces, mirror=True, limit=None, want_example=False):
    cells = sorted(region)
    idx = {cell: i for i, cell in enumerate(cells)}
    full = (1 << len(cells)) - 1
    placements = []  # для каждой клетки: список масок, у которых эта клетка -- первая
    for pid, pc in enumerate(pieces):
        for o in orientations(pc, mirror):
            placements.append((pid, anchored(o)))
    by_cell = []
    for (r, c) in cells:
        lst = []
        for pid, o in placements:
            sh = [(r + dr, c + dc) for dr, dc in o]
            if all(s in idx for s in sh):
                m = 0
                for s in sh:
                    m |= 1 << idx[s]
                lst.append((pid, m, tuple(sh)))
        by_cell.append(lst)

    @lru_cache(maxsize=None)
    def f(mask):
        if mask == full:
            return 1
        # первая незанятая клетка
        i = (~mask & (mask + 1)).bit_length() - 1
        tot = 0
        for pid, m, sh in by_cell[i]:
            if not (m & mask):
                tot += f(mask | m)
        return tot

    n = f(0)
    ex = None
    if want_example and n:
        ex = []
        mask = 0
        while mask != full:
            i = (~mask & (mask + 1)).bit_length() - 1
            for pid, m, sh in by_cell[i]:
                if not (m & mask) and f(mask | m):
                    ex.append(sh); mask |= m; break
    f.cache_clear()
    return (n, ex) if want_example else n


def rect(h, w):
    return {(r, c) for r in range(h) for c in range(w)}


def draw(h, w, tiles, holes=()):
    lab = {}
    sym = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    for k, t in enumerate(tiles):
        for cell in t:
            lab[cell] = sym[k % len(sym)]
    out = []
    for r in range(h):
        out.append(" ".join(lab.get((r, c), "#" if (r, c) in holes else ".") for c in range(w)))
    return "\n".join(out)


DOMINO = [(0, 0), (0, 1)]
I3 = [(0, 0), (0, 1), (0, 2)]
I4 = [(0, 0), (0, 1), (0, 2), (0, 3)]
L3 = [(0, 0), (1, 0), (1, 1)]
T4 = [(0, 0), (0, 1), (0, 2), (1, 1)]
