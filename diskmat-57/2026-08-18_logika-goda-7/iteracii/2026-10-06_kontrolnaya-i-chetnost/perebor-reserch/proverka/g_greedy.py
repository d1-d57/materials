"""«Меняем по одному» с СЛУЧАЙНЫМ выбором (ребёнок меняет что попало, лишь бы новое): доля прогонов, обошедших всё."""
import random
from itertools import combinations, product
random.seed(1)
def run(objs, nbrs, trials=5000):
    full = 0; lens = []
    for _ in range(trials):
        cur = random.choice(objs); seen = {cur}
        while True:
            c = [n for n in nbrs(cur) if n not in seen]
            if not c: break
            cur = random.choice(c); seen.add(cur)
        lens.append(len(seen)); full += len(seen) == len(objs)
    return full / trials, sum(lens) / trials, min(lens)
L = "АБВГД"; T = [''.join(c) for c in combinations(L, 3)]
nT = lambda s: [''.join(sorted(s.replace(o, i))) for o in s for i in L if i not in s]
print("K4 тройки из 5, меняем одного человека: доля полных обходов %.2f, в среднем %.1f из 10, минимум %d" % run(T, nT))
F = [''.join(w) for w in product('БКС', repeat=3) if w[0] != w[1] and w[1] != w[2]]
nF = lambda s: [s[:p] + c + s[p+1:] for p in range(3) for c in 'БКС' if c != s[p] and s[:p] + c + s[p+1:] in F]
print("флаги, меняем одну полосу: доля полных обходов %.2f, в среднем %.1f из 12, минимум %d" % run(F, nF))
