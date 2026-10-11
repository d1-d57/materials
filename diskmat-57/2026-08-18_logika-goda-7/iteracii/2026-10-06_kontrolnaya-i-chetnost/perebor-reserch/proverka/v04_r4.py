from verify_bank import *

L5 = "АБВГД"
def to_idx(w): return tuple(L5.index(ch) + 1 for ch in w)
def from_idx(t): return "".join(L5[i - 1] for i in t)

# T9 (R4): пары дежурных из пятерых
hand = S("АБ АВ АГ АД БВ БГ БД ВГ ВД ГД")
brute = ["".join(c) for c in combinations(L5, 2)]
check("T9", 10, hand, brute, key=lambda w: w,
      succ=lambda w: (lambda r: None if r is None else from_idx(r))(succ_comb(to_idx(w), 5)))
print("  T9 наивно «каждый с каждым» с порядком:", len(list(permutations(L5, 2))))

# T10 (R4): выбрать 3 разных числа из 1..5 (набор, порядок не важен)
hand = S("123 124 125 134 135 145 234 235 245 345")
brute = ["".join(map(str, c)) for c in combinations(range(1, 6), 3)]
check("T10", 10, hand, brute, key=int,
      succ=lambda w: (lambda r: None if r is None else "".join(map(str, r)))(succ_comb(tuple(map(int, w)), 5)))
print("  T10 наивно «упорядоченные тройки разных»:", len(list(permutations(range(1, 6), 3))), "= 10*6")

# T11 (R4): наряды — кофта 1..3, юбка 1..2, обувь 1..2; код «кофта-юбка-обувь»
alph = [("1", "2", "3"), ("1", "2"), ("1", "2")]
hand = S("111 112 121 122 211 212 221 222 311 312 321 322")
brute = ["".join(t) for t in product(*alph)]
check("T11", 12, hand, brute, key=int,
      succ=lambda w: (lambda r: None if r is None else "".join(r))(succ_odometer(tuple(w), alph)))

# T12 (R4): разложения 6 (порядок слагаемых не важен)
hand = [(6,), (5,1), (4,2), (4,1,1), (3,3), (3,2,1), (3,1,1,1), (2,2,2), (2,2,1,1), (2,1,1,1,1), (1,)*6]
check("T12", 11, hand, list(partitions(6)), key=lambda p: tuple(-x for x in p), succ=succ_partition_desc)
# запас: разложения 7
hand7 = [(7,), (6,1), (5,2), (5,1,1), (4,3), (4,2,1), (4,1,1,1), (3,3,1), (3,2,2), (3,2,1,1), (3,1,1,1,1),
         (2,2,2,1), (2,2,1,1,1), (2,1,1,1,1,1), (1,)*7]
check("T12b", 15, hand7, list(partitions(7)), key=lambda p: tuple(-x for x in p), succ=succ_partition_desc)
# наивный главный признак «по числу слагаемых»: размеры групп
from collections import Counter
print("  T12 по числу слагаемых:", dict(sorted(Counter(len(p) for p in partitions(6)).items())))

# T13 (R4): маршруты в прямоугольнике 2 (вверх) x 3 (вправо): слова из ППП ВВ
brute = list({"".join(p) for p in permutations("ПППВВ")})
hand = S("ПППВВ ППВПВ ППВВП ПВППВ ПВПВП ПВВПП ВПППВ ВППВП ВПВПП ВВППП")
check("T13", 10, hand, brute, key=lambda w: w.replace("П", "0").replace("В", "1"), succ=lambda w: succ_word(w, "ПВ"))
# эквивалент: маршрут = выбор двух номеров шагов (из 5), на которых идём вверх
pos = ["".join(str(i + 1) for i, ch in enumerate(w) if ch == "В") for w in hand]
print("  T13 номера шагов «вверх»:", pos)
