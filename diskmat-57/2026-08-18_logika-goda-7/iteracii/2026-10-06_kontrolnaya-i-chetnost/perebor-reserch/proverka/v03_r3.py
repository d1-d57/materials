from verify_bank import *
from collections import Counter

# T6 (R3): флаг из трёх горизонтальных полос, цвета К,Б,С, все полосы разного цвета
hand = S("БКС БСК КБС КСБ СБК СКБ")   # порядок: по верхней полосе Б<К<С (алфавит), затем по средней
brute = ["".join(p) for p in permutations("КБС")]
check("T6", 6, hand, brute, key=lambda w: w, succ=lambda w: succ_word(w, "БКС"))
# наивное правило: циклический сдвиг
w = "КБС"; seen = []
while w not in seen:
    seen.append(w); w = w[1:] + w[0]
print("  T6 наивно (циклический сдвиг от КБС):", seen, "->", len(seen), "из 6; пропущены:", sorted(set(brute) - set(seen)))
# наивное правило 2: «меняю местами две соседние полосы по очереди» (1-2, 2-3, 1-2, ...)
w = "КБС"; seq = [w]; i = 0
for _ in range(10):
    l = list(w); l[i], l[i+1] = l[i+1], l[i]; w = "".join(l); i = 1 - i
    if w in seq: break
    seq.append(w)
print("  T6 наивно (по очереди меняю соседние 1-2, 2-3):", seq, "->", len(seq), "(обход всех 6 — повезло, но правило «следующего» = нужен счётчик чередования)")

# T7 (R3): разложения 5 в сумму натуральных, порядок слагаемых не важен
hand = [(5,), (4,1), (3,2), (3,1,1), (2,2,1), (2,1,1,1), (1,1,1,1,1)]
brute = list(partitions(5))
check("T7", 7, hand, brute, key=lambda p: tuple(-x for x in p), succ=succ_partition_desc)
# наивно: дети пишут записи с порядком (композиции)
def compositions(n):
    if n == 0: yield (); return
    for k in range(1, n+1):
        for r in compositions(n-k): yield (k,) + r
comp = list(compositions(5))
print("  T7 записей-с-порядком (композиций) 5:", len(comp), "-> различных разложений:", len({tuple(sorted(c)) for c in comp}))
# наивно «по возрастанию первого слагаемого»: группы по первому слагаемому
g = Counter(c[0] for c in comp)
print("  T7 композиций с первым слагаемым k:", dict(sorted(g.items())))

# T8 (R3): набрать 8 рублей монетами 1, 2, 5 (порядок монет не важен)
def coin_ways(total, coins=(5,2,1)):
    res = []
    def rec(rem, i, acc):
        if i == len(coins) - 1:
            res.append(tuple(acc + [coins[i]] * rem)) if rem % coins[i] == 0 else None
            return
        for k in range(rem // coins[i], -1, -1):
            rec(rem - k*coins[i], i+1, acc + [coins[i]]*k)
    rec(total, 0, [])
    return res
hand = [(5,2,1), (5,1,1,1), (2,2,2,2), (2,2,2,1,1), (2,2,1,1,1,1), (2,1,1,1,1,1,1), (1,)*8]
brute = [p for p in partitions(8) if set(p) <= {1,2,5}]
check("T8", 7, hand, brute, key=lambda p: (-p.count(5), -p.count(2)))
cnt = Counter(len(p) for p in brute)
print("  T8 наивно «по числу монет»: число способов с k монетами:", dict(sorted(cnt.items())),
      "-> ничьи при k=", [k for k,v in cnt.items() if v > 1])
