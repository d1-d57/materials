from verify_bank import *
from collections import Counter

def tri(t):  # t по убыванию c>b>a
    c, b, a = t
    return a + b > c

def desc_triples(n):
    return [tuple(sorted(c, reverse=True)) for c in combinations(range(1, n + 1), 3)]

# T15 (R6a): палочки 1..7, тройки-треугольники с наибольшей 7. НФ: по убыванию «7 b a»
hand = [(7,6,5), (7,6,4), (7,6,3), (7,6,2), (7,5,4), (7,5,3)]
brute = [t for t in desc_triples(7) if t[0] == 7 and tri(t)]
def succ_7(t):
    # правило: при той же средней уменьшаем меньшую, пока a+b>7; потом средняя -1, меньшая = b-1
    c, b, a = t
    if a - 1 >= 1 and (a - 1) + b > c: return (c, b, a - 1)
    b -= 1
    while b >= 2:
        a = b - 1
        if a + b > c: return (c, b, a)
        b -= 1
    return None
check("T15", 6, hand, brute, key=lambda t: tuple(-x for x in t), succ=succ_7)
allc7 = [t for t in desc_triples(7) if t[0] == 7]
print("  T15 всех троек с наибольшей 7:", len(allc7), "; из них треугольников:", len(brute),
      "; вырожденные (a+b=7):", [t for t in allc7 if t[1] + t[2] == 7])

# T15b (R6b): все тройки из 1..6 — 20 штук, в НФ по возрастанию (как в T10), словарно
hand_all6 = S("123 124 125 126 134 135 136 145 146 156 234 235 236 245 246 256 345 346 356 456")
brute_all6 = ["".join(map(str, c)) for c in combinations(range(1, 7), 3)]
check("T15b", 20, hand_all6, brute_all6, key=int,
      succ=lambda w: (lambda r: None if r is None else "".join(map(str, r)))(succ_comb(tuple(map(int, w)), 6)))
# треугольники среди 1..6 по наибольшей палочке
t6 = [t for t in desc_triples(6) if tri(t)]
hand_t6 = [(4,3,2), (5,4,3), (5,4,2), (6,5,4), (6,5,3), (6,5,2), (6,4,3)]
check("T15c", 7, hand_t6, t6, key=lambda t: (t[0], -t[1], -t[2]))
print("  T15c треугольников из 1..6 по наибольшей:", dict(sorted(Counter(t[0] for t in t6).items())))
t7 = [t for t in desc_triples(7) if tri(t)]
print("  все треугольники из 1..7:", len(t7), "по наибольшей:", dict(sorted(Counter(t[0] for t in t7).items())),
      "; всех троек из 1..7:", len(desc_triples(7)))

# T16 (R6-мост / R3): три натуральных числа с суммой 9, порядок не важен. НФ по убыванию.
hand = [(7,1,1), (6,2,1), (5,3,1), (5,2,2), (4,4,1), (4,3,2), (3,3,3)]
brute = [p for p in partitions(9) if len(p) == 3]
check("T16", 7, hand, brute, key=lambda p: tuple(-x for x in p))
print("  T16 из них «треугольники» (a+b>c, равные стороны можно):", [p for p in hand if p[1] + p[2] > p[0]])
print("  T16 упорядоченных троек (композиций на 3 части):", sum(1 for a in range(1, 8) for b in range(1, 8) if 9 - a - b >= 1))
