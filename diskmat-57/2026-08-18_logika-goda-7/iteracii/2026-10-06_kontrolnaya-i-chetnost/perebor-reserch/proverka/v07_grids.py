# проверка сеток учителя: число рабочих клеток = ответ, и клетка однозначно задаёт объект
from verify_bank import *
from itertools import combinations, permutations
g = {}
g["T2"] = sum(1 for i in range(4) for j in range(4) if i < j)
g["T9"] = sum(1 for i in range(5) for j in range(5) if i < j)
g["T6"] = sum(1 for t in "БКС" for m in "БКС" if t != m)            # низ однозначен
g["T8"] = sum(1 for f in (0,1) for d in range(5) if 8 - 5*f - 2*d >= 0)  # рубли = остаток, однозначно
g["T11"] = 3 * 4
g["T14"] = sum(1 for a in range(1,10) for b in range(10) if a + b in {2,3,5,7,11,13,17})
g["T15"] = sum(1 for b in range(2,7) for a in range(1,b) if a + b > 7)
g["T15c"] = sum(1 for c in range(3,7) for b in range(2,c) for a in range(1,b) if a + b > c)
g["T10"] = sum(1 for c in combinations(range(1,6),3))
print(g)
exp = {"T2":6,"T9":10,"T6":6,"T8":7,"T11":12,"T14":33,"T15":6,"T15c":7,"T10":10}
print("all grids OK:", g == exp)
