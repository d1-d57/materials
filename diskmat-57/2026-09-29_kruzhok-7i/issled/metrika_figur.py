"""Грубая метрика трудности фигуры для разрезания на k равных частей:
форм — сколько m-мино могут накрыть КАЖДУЮ клетку фигуры хоть одним положением (из скольких форм надо угадать);
узкое — минимум по клеткам числа положений верной формы (1 = есть клетка, где ход вынужден)."""
import json, sys
from tiling import orientations, anchored
from poisk_figur import free_polys
def placements(F, P):
    out = []
    for o in orientations(P):
        for (r, c) in F:
            for (a, b) in o:
                sh = frozenset((r - a + x, c - b + y) for x, y in o)
                if sh <= F: out.append(sh)
    return set(out)
def metr(f):
    F = {tuple(x) for x in f["F"]}; m = len(f["tiles"][0])
    true = [tuple(x) for x in f["tiles"][0]]
    pl = placements(F, true)
    uz = min(sum(x in s for s in pl) for x in F)
    forms = sum(1 for P in free_polys(m) if (lambda S: all(any(x in s for s in S) for x in F))(placements(F, P)))
    return forms, uz
if __name__ == "__main__":
    for spec in sys.argv[1:]:
        fn, i = spec.split(":"); f = json.load(open(fn))[int(i)]
        print(spec, "клеток", len(f["F"]), "форм", *metr(f))
