"""Сколькими способами цифры 1..9 разбить на 3 команды с равной суммой?

Две независимые проверки:
  A) перебор подмножеств (combinations) — выбираем команду 1, потом команду 2;
  B) канонический перебор разбиений: каждый элемент кладём либо в уже
     открытую команду, либо в новую (номера команд возрастают -> без дублей).
Оба метода считают НЕУПОРЯДОЧЕННЫЕ разбиения (команды неразличимы).
"""

from itertools import combinations

DIGITS = list(range(1, 10))
TOTAL = sum(DIGITS)          # 45
TARGET = TOTAL // 3          # 15
assert TOTAL % 3 == 0


def method_a():
    """Перебор подмножеств. Каноничность: минимальный элемент каждой команды
    возрастает от команды к команде, поэтому каждое разбиение встречается раз."""
    found = set()
    rest0 = set(DIGITS)
    for size1 in range(1, 8):
        for t1 in combinations(sorted(rest0), size1):
            if sum(t1) != TARGET:
                continue
            if min(t1) != min(rest0):      # команда 1 содержит минимум всего множества
                continue
            rest1 = rest0 - set(t1)
            for size2 in range(1, len(rest1)):
                for t2 in combinations(sorted(rest1), size2):
                    if sum(t2) != TARGET:
                        continue
                    if min(t2) != min(rest1):   # команда 2 содержит минимум остатка
                        continue
                    t3 = tuple(sorted(rest1 - set(t2)))
                    if sum(t3) != TARGET or not t3:
                        continue
                    found.add(tuple(sorted((tuple(sorted(t1)), tuple(sorted(t2)), t3))))
    return found


def method_b():
    """Рекурсивный перебор разбиений в канонической форме."""
    found = set()

    def rec(i, groups):
        if i == len(DIGITS):
            if len(groups) == 3 and all(sum(g) == TARGET for g in groups):
                found.add(tuple(sorted(tuple(sorted(g)) for g in groups)))
            return
        d = DIGITS[i]
        for k in range(len(groups)):          # в существующую команду
            if sum(groups[k]) + d <= TARGET:
                groups[k].append(d)
                rec(i + 1, groups)
                groups[k].pop()
        if len(groups) < 3:                   # открыть новую команду
            groups.append([d])
            rec(i + 1, groups)
            groups.pop()

    rec(0, [])
    return found


def validate(partitions):
    """Каждое разбиение действительно покрывает 1..9 без пересечений, суммы = 15."""
    for p in partitions:
        flat = [x for g in p for x in g]
        assert sorted(flat) == DIGITS, p          # ровно все цифры, без повторов
        assert len(p) == 3 and all(g for g in p), p
        assert all(sum(g) == TARGET for g in p), p


if __name__ == "__main__":
    a, b = method_a(), method_b()
    validate(a)
    validate(b)
    assert a == b, ("методы разошлись", a ^ b)

    print(f"сумма = {TOTAL}, на команду = {TARGET}")
    print(f"метод A: {len(a)}   метод B: {len(b)}   совпали: {a == b}")
    print(f"команды различимы (×3!): {len(a) * 6}")

    equal_size = [p for p in a if all(len(g) == 3 for g in p)]
    print(f"из них с равным размером (3+3+3): {len(equal_size)}")
    print()
    for p in sorted(a, key=lambda q: ([len(g) for g in q], q)):
        print("  " + "  |  ".join(" ".join(map(str, g)) for g in p))
