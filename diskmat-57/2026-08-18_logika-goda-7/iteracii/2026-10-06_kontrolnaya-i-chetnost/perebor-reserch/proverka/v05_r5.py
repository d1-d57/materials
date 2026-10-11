from verify_bank import *
from collections import defaultdict

def ds(n): return n // 10 + n % 10
PR = {2, 3, 5, 7, 11, 13, 17}
brute = [n for n in range(10, 100) if ds(n) in PR]

# порядок 1: по возрастанию числа
by_num = [11,12,14,16,20,21,23,25,29,30,32,34,38,41,43,47,49,50,52,56,58,61,65,67,70,74,76,83,85,89,92,94,98]
check("T14a", 33, by_num, brute, key=lambda n: n)

# порядок 2: по сумме цифр, внутри — по возрастанию
by_sum = [11,20, 12,21,30, 14,23,32,41,50, 16,25,34,43,52,61,70, 29,38,47,56,65,74,83,92, 49,58,67,76,85,94, 89,98]
check("T14b", 33, by_sum, brute, key=lambda n: (ds(n), n))
groups = defaultdict(list)
for n in by_sum: groups[ds(n)].append(n)
print("  по сумме:", {s: len(v) for s, v in groups.items()}, "сумма:", sum(len(v) for v in groups.values()))
# внутри группы соседние отличаются на 9
print("  внутри групп шаг 9:", all(b - a == 9 for v in groups.values() for a, b in zip(v, v[1:])))

# порядок 3: по первой цифре (то же, что по возрастанию) — сколько в каждой строке
rows = defaultdict(list)
for n in by_num: rows[n // 10].append(n % 10)
print("  по первой цифре (строки):", {d: v for d, v in rows.items()})
print("  длины строк:", {d: len(v) for d, v in rows.items()})

# сетка 9x10: где стоят «простые» клетки
print("  сетка (строка — первая цифра, столбец — вторая 0..9), # = сумма простая:")
for a in range(1, 10):
    print("   ", a, "".join("#" if (a + b) in PR else "." for b in range(10)))

# сколько всего двузначных с суммой s (для проверки «лесенки»)
print("  число двузначных с суммой s:", {s: sum(1 for n in range(10, 100) if ds(n) == s) for s in range(1, 19)})
