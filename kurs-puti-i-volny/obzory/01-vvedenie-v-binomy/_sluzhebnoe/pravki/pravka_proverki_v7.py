"""Добавляет в _sluzhebnoe/proverki.py проверки v7 (размещения, 8!, две формулы). Якорь — ровно один."""
import sys
P = '_sluzhebnoe/proverki.py'
s = open(P, encoding='utf-8').read()
a = '\nimport re, os\n_t = open('
if s.count(a) != 1: sys.exit('якорь')
add = '''
# v7 (10.10, голосовая после занятия 4): размещения, 8!, две формулы
def Ar(n, k):  # перебором: упорядоченные наборы k различных из n
    return sum(1 for _ in permutations(range(n), k))
check("v7: задача 10: 8·7·6 = 336 = размещений из 8 по 3", 8*7*6 == 336 == prod(range(6, 9)))
check("v7: утв. 12: размещений из n по k = n(n-1)…(n-k+1), 0<=k<=n (перебор n<7)",
      all(Ar(n, k) == prod(range(n - k + 1, n + 1)) for n in range(7) for k in range(n + 1)))
check("v7: размещений при k>n нет", all(Ar(n, k) == 0 for n in range(5) for k in range(n + 1, n + 3)))
check("v7: опр. 13: n! = размещения из n по n", all(Ar(n, n) == factorial(n) for n in range(7)))
check("v7: треугольник размещений, строки 0..5",
      [[prod(range(n - k + 1, n + 1)) for k in range(n + 1)] for n in range(6)] ==
      [[1], [1, 1], [1, 2, 2], [1, 3, 6, 6], [1, 4, 12, 24, 24], [1, 5, 20, 60, 120, 120]])
check("v7: пример 4^2 = 12 = 3^2 + 2·3^1 = 6 + 6", Ar(4, 2) == 12 == Ar(3, 2) + 2 * Ar(3, 1) and Ar(3, 2) == 6 == 2 * Ar(3, 1))
check("v7: утв. 14: n^k = (n-1)^k + k·(n-1)^(k-1), 1<=k<=n (перебор n<7)",
      all(Ar(n, k) == Ar(n - 1, k) + k * Ar(n - 1, k - 1) for n in range(1, 7) for k in range(1, n + 1)))
check("v7: утв. 15: n^k = n^(k-1)·(n-k+1) = n·(n-1)^(k-1) (перебор n<7)",
      all(Ar(n, k) == Ar(n, k - 1) * (n - k + 1) == n * Ar(n - 1, k - 1) for n in range(1, 7) for k in range(1, n + 1)))
check("v7: строка 4: 1,4,12,24,24 — множители 4,3,2,1; 6! = 6·5!",
      [prod(range(4 - k + 1, 5)) for k in range(5)] == [1, 4, 12, 24, 24] and factorial(6) == 6 * factorial(5))
check("v7: т. 19 через размещения: C(n,k)·k! = n^k (перебор n<7)",
      all(C(n, k) * factorial(k) == Ar(n, k) for n in range(7) for k in range(n + 1)))
check("v7: задача 21: 8! = 40320 = C(8,3)·3!·5! = 720·56", factorial(8) == 40320 == C(8, 3) * factorial(3) * factorial(5) == 720 * 56)
check("v7: n! = C(n,k)·k!·(n-k)!", all(factorial(n) == C(n, k) * factorial(k) * factorial(n - k) for n in range(N) for k in range(n + 1)))
check("v7: мультиномиальный пример: N·2!·3!·4! = 9!, N = 1260",
      1260 * factorial(2) * factorial(3) * factorial(4) == factorial(9))
check("v7: пример 5!/(2!3!) = 10 = 5!/(3!2!), 6!/(3!3!) = 20 = 10 + 10",
      factorial(5) // (factorial(2) * factorial(3)) == 10 and factorial(6) // factorial(3) ** 2 == 20)
check("v7: утв. 22: формула подчиняется правилу Паскаля, n>=2, 1<=k<=n-1 (дроби точно)",
      all(F(factorial(n - 1), factorial(k - 1) * factorial(n - k)) + F(factorial(n - 1), factorial(k) * factorial(n - k - 1))
          == F(factorial(n), factorial(k) * factorial(n - k)) for n in range(2, 15) for k in range(1, n)))
check("v7: утв. 22, док.: числители (n-1)!·k + (n-1)!·(n-k) = n!",
      all(factorial(n - 1) * k + factorial(n - 1) * (n - k) == factorial(n) for n in range(2, 15) for k in range(1, n)))
'''
s = s.replace(a, add + a)
open(P, 'w', encoding='utf-8').write(s)
print('ok')
