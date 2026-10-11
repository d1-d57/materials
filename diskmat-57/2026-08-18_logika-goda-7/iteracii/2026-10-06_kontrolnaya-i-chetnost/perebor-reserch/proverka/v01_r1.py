from verify_bank import *

# T1 (R1): двузначные числа с суммой цифр 4
hand = S("13 22 31 40")
brute = [str(n) for n in range(10, 100) if sum(map(int, str(n))) == 4]
check("T1", 4, hand, brute, key=int, succ=lambda s: (str(int(s)+9) if int(s)+9 <= 99 and sum(map(int,str(int(s)+9)))==4 else None))

# T2 (R1): из Ани, Бори, Вики, Гены выбрать двух дежурных
hand = S("АБ АВ АГ БВ БГ ВГ")
brute = ["".join(c) for c in combinations("АБВГ", 2)]
check("T2", 6, hand, brute, key=lambda w: w,
      succ=lambda w: (lambda r: None if r is None else "".join("АБВГ"[i-1] for i in r))(succ_comb(tuple("АБВГ".index(ch)+1 for ch in w), 4)))
# наивный перебор «каждый с каждым» без нормальной формы даёт 12 записей = каждая пара дважды
naive = ["".join(p) for p in permutations("АБВГ", 2)]
print("  T2 наивно (каждый с каждым, порядок важен):", len(naive), "записей, различных пар:", len({frozenset(x) for x in naive}))
