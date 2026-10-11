from verify_bank import *

# T3 (R2): трёхзначные числа из цифр 1,2,3, каждая по разу
hand = S("123 132 213 231 312 321")
brute = ["".join(p) for p in permutations("123")]
check("T3", 6, hand, brute, key=int, succ=lambda w: succ_word(w, "123"))

# T4 (R2): двузначные с суммой цифр 6
hand = S("15 24 33 42 51 60")
brute = [str(n) for n in range(10, 100) if sum(map(int, str(n))) == 6]
check("T4", 6, hand, brute, key=int)

# T5 (R2): маршруты в квадрате 2x2 (2 шага вправо П, 2 шага вверх В) — по первому шагу, П раньше В
hand = S("ППВВ ПВПВ ПВВП ВППВ ВПВП ВВПП")
brute = {"".join(p) for p in permutations("ППВВ")}
check("T5", 6, hand, list(brute), key=lambda w: w.replace("П", "0").replace("В", "1"), succ=lambda w: succ_word(w, "ПВ"))
