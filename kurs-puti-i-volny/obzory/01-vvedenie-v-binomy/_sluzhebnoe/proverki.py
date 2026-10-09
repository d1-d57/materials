#!/usr/bin/env python3
"""Проверки чисел и тождеств SKELET.md (обзор 1, «Введение в биномиальные коэффициенты»).

Запуск: python3 _sluzhebnoe/proverki.py   → печатает пункты, rc=0 если всё сошлось.
Каждый пункт помечен номером блока SKELET, который он проверяет.
"""
from itertools import combinations, permutations, product
from math import comb, factorial, prod
import sys

ok = True
def check(name, cond, info=""):
    global ok
    print(("✓ " if cond else "✗ ") + name + (f"  [{info}]" if info else ""))
    ok = ok and cond

def C(n, k):  # перебором: число k-подмножеств [n]
    return sum(1 for _ in combinations(range(1, n + 1), k))

N = 9
# опр. 1 / утв. 2: подмножества ↔ слова
for n in range(N):
    for k in range(n + 1):
        words = [w for w in product((0, 1), repeat=n) if sum(w) == k]
        assert len(words) == C(n, k)
check("утв. 2: слов с k единицами столько же, сколько k-подмножеств (n<9)", True)

# утв. 3: края
check("утв. 3: C(n,0)=C(n,n)=1, C(n,1)=C(n,n-1)=n",
      all(C(n, 0) == C(n, n) == 1 and (n == 0 or C(n, 1) == C(n, n - 1) == n) for n in range(N)))

# утв. 4: C(n,2) семью способами
for n in range(2, 15):
    pairs = C(n, 2)
    s_min = sum(n - i for i in range(1, n))                           # а: по наименьшему
    stair = sum(1 for i in range(1, n + 1) for j in range(1, n + 1) if i < j)  # б: лесенка
    gauss = (n - 1) * n // 2                                          # в: Гаусс
    ordered = sum(1 for _ in permutations(range(n), 2))               # г: шоколадка = упорядоченные пары
    deg = n * (n - 1)                                                 # д: из каждой вершины n-1
    diag = sum(1 for i, j in combinations(range(n), 2) if (j - i) % n not in (1, n - 1))  # ж: только диагонали
    assert pairs == s_min == stair == gauss == ordered // 2 == deg // 2 == n * (n - 1) // 2, n
    if n >= 3:
        assert diag == n * (n - 3) // 2, n
check("утв. 4 (а–ж): все семь подсчётов C(n,2) сходятся, диагонали n(n-3)/2 (n=2..14)", True)

# утв. 5: симметрия
check("утв. 5: C(n,k)=C(n,n-k)", all(C(n, k) == C(n, n - k) for n in range(N) for k in range(n + 1)))

# пример 6: что остаётся незаполненным в строках 0..6
known = lambda n, k: min(k, n - k) <= 2
holes = [(n, k) for n in range(7) for k in range(n + 1) if not known(n, k)]
check("пример 6: единственная клетка строк 0–6, не следующая из утв. 3–5, — (6,3)", holes == [(6, 3)], str(holes))
check("пример 6: строки 0–6", True, " / ".join(" ".join(str(C(n, k)) for k in range(n + 1)) for n in range(7)))

# утв. 7: правило Паскаля
check("утв. 7: C(n,k)=C(n-1,k-1)+C(n-1,k), 1<=k<=n-1",
      all(C(n, k) == C(n - 1, k - 1) + C(n - 1, k) for n in range(2, N) for k in range(1, n)))
check("пример 7а: C(6,3)=C(5,2)+C(5,3)=20", C(6, 3) == C(5, 2) + C(5, 3) == 20)
check("пример 7б: C(5,2)=C(4,1)+C(4,2): 10=4+6", C(5, 2) == 10 and C(4, 1) == 4 and C(4, 2) == 6)
check("пример 7в: C(8,3)=C(7,2)+C(7,3): 56=21+35", C(8, 3) == 56 == C(7, 2) + C(7, 3) and C(7, 2) == 21)

# утв. 8: капитан — перебором множества T пар (A, c)
for n in range(1, 8):
    for k in range(0, n):
        T = [(A, c) for A in combinations(range(n), k + 1) for c in A]
        assert len(T) == n * C(n - 1, k) == (n - k) * C(n, k) == (k + 1) * C(n, k + 1), (n, k)
check("утв. 8: |T| = n·C(n-1,k) = (n-k)·C(n,k) = (k+1)·C(n,k+1) перебором (n<8)", True)
v = (25 * comb(24, 10), 11 * comb(25, 11), 15 * comb(25, 10))
check("пример 8: 25·C(24,10)=11·C(25,11)=15·C(25,10)", len(set(v)) == 1, str(v[0]))

# следствия 9, 9′
from fractions import Fraction as F
check("след. 9: C(n,k+1) = (n-k)/(k+1)·C(n,k)",
      all(F(C(n, k + 1)) == F(n - k, k + 1) * C(n, k) for n in range(1, N) for k in range(n)))
check("след. 9′: C(n,k) = n/k·C(n-1,k-1), 1<=k<=n",
      all(F(C(n, k)) == F(n, k) * C(n - 1, k - 1) for n in range(1, N) for k in range(1, n + 1)))
check("след. 9″: C(n,k) = n/(n-k)·C(n-1,k), 0<=k<=n-1",
      all(F(C(n, k)) == F(n, n - k) * C(n - 1, k) for n in range(1, N) for k in range(n)))

# опр. 10, т. 11
check("опр. 10: 10! = 3628800", factorial(10) == 3628800)
check("т. 11: C(n,k) = n(n-1)…(n-k+1)/k! = n!/(k!(n-k)!)",
      all(C(n, k) == prod(range(n - k + 1, n + 1)) // factorial(k) == factorial(n) // (factorial(k) * factorial(n - k))
          for n in range(N) for k in range(n + 1)))
check("т. 11, док. 1: ходьба вдоль строки от C(n,0)=1",
      all(prod((F(n - j, j + 1) for j in range(k)), start=F(1)) == C(n, k) for n in range(N) for k in range(n + 1)))
check("т. 11, док. 3: последовательностей из k различных = n(n-1)…(n-k+1), каждое множество — k! раз",
      all(sum(1 for _ in permutations(range(n), k)) == prod(range(n - k + 1, n + 1)) == factorial(k) * C(n, k)
          for n in range(7) for k in range(n + 1)))

# числа для вступления и истории
check("вступление: тройки из 6 вкусов = 20; все непустые наборы 6+15+20+15+6+1 = 63",
      C(6, 3) == 20 and sum(C(6, k) for k in range(1, 7)) == 63)
check("история: Варахамихира, 4 из 16 = 1820", comb(16, 4) == 1820)
check("история: задача Паскаля 3·4·5·6/(1·2·3·4) = 15 = C(6,4)", F(3 * 4 * 5 * 6, 1 * 2 * 3 * 4) == 15 == C(6, 4))
check("история: Луллий, пары из 9 = 36", C(9, 2) == 36)
check("Гаусс: 1+2+…+100 = 5050 = C(101,2)", sum(range(1, 101)) == 5050 == comb(101, 2))

# текст v2 (04.10): ходьба по шестой строке и седьмая строка из шестой
check("текст: 6/1·1=6, 5/2·6=15, 4/3·15=20", F(6,1)*1==6 and F(5,2)*6==15 and F(4,3)*15==20)
check("текст: C(7,2)=6+15=21, C(7,3)=15+20=35, C(8,3)=21+35=56", C(7,2)==6+15==21 and C(7,3)==15+20==35 and C(8,3)==56)
check("текст: смесь {1,3,5} в [6] -> 101010, {2,3,4} -> 011100",
      "".join("1" if i in {1,3,5} else "0" for i in range(1,7))=="101010" and "".join("1" if i in {2,3,4} else "0" for i in range(1,7))=="011100")

# v3: определение для всех k>=0 (ноль при k>n), правило Паскаля до k=n, пары при n=0,1
check("v3: C(n,k)=0 при k>n", all(C(n,k)==0 for n in range(6) for k in range(n+1,n+4)))
check("v3: правило Паскаля при 1<=k<=n, n>=1", all(C(n,k)==C(n-1,k-1)+C(n-1,k) for n in range(1,N) for k in range(1,n+1)))
check("v3: C(n,2)=n(n-1)/2 при n=0,1; C(n,1)=n при n=0", C(0,2)==0==C(1,2) and C(0,1)==0)
check("v3: пример C(5,2)=4+6, 4·3=12 упорядоченных пар из 4, C(4,2)=12/2", C(5,2)==C(4,1)+C(4,2)==10 and len(list(permutations(range(4),2)))==12)
check("v3: капитан n=6, команда 3: 6·10=15·4=20·3=60", 6*C(5,2)==15*4==C(6,3)*3==60)
check("v3: диагоналей пятиугольника 5", 5*(5-3)//2==5)

# v5 (04.10, второй круг): двоичная запись, сумма строки, задача 25/11, тройки из восьми, рычаг «не делим»
check("v5: 011100 = 16+8+4 = 28; 101010 = 42", int("011100",2)==28==16+8+4 and int("101010",2)==42)
check("v5: слова длины 3 по возрастанию — двоичные записи номеров 0..7",
      ["".join(map(str,w)) for w in product((0,1),repeat=3)]==[format(i,"03b") for i in range(8)])
check("v5: тройки по убыванию 111000,110100,110010,110001,101100 — первые пять",
      sorted([format(i,"06b") for i in range(64) if bin(i).count("1")==3],reverse=True)[:5]==["111000","110100","110010","110001","101100"])
check("v5: утв. 11 сумма строки = 2^n (n<9)", all(sum(C(n,k) for k in range(n+1))==2**n for n in range(N)))
check("v5: 6+15+20+15+6+1=63, 63=111111_2=32+16+8+4+2+1, 1+4+6+4+1=16", 6+15+20+15+6+1==63==int("111111",2)==32+16+8+4+2+1 and 1+4+6+4+1==16)
check("v5: рисунок slova4 — столбцы 1,4,6,4,1", [sum(1 for w in product((0,1),repeat=4) if sum(w)==k) for k in range(5)]==[1,4,6,4,1])
w52=["".join(map(str,w)) for w in product((1,0),repeat=5) if sum(w)==2]
check("v5: слова длины 5 с двумя единицами: с 1 — 11000,10100,10010,10001; с 0 — шесть",
      [w for w in w52 if w[0]=="1"]==["11000","10100","10010","10001"] and sorted([w for w in w52 if w[0]=="0"],reverse=True)==["01100","01010","01001","00110","00101","00011"])
check("v5: край C(4,4)=C(3,3)+C(3,4)=1+0", C(4,4)==C(3,3)+C(3,4)==1 and C(3,4)==0)
check("v5: задача 12: 25·C(24,10)=15·C(25,10)=11·C(25,11)=11·4457400=49031400",
      25*comb(24,10)==15*comb(25,10)==11*comb(25,11)==11*4457400==49031400)
check("v5: утв. 13 при k>=n — все три числа 0", all(n*C(n-1,k)==(n-k)*C(n,k)==(k+1)*C(n,k+1)==0 for n in range(1,7) for k in range(n,n+3)))
check("v5: задача 17: X·3·2=8·7·6=336, X=56=C(8,3); n(n-1)=2·C(n,2)", 56*3*2==8*7*6==336 and C(8,3)==56 and all(n*(n-1)==2*C(n,2) for n in range(N)))
check("v5: утв. 13 диагональ: k·C(n,k)=n·C(n-1,k-1), 1<=k<=n", all(k*C(n,k)==n*C(n-1,k-1) for n in range(1,N) for k in range(1,n+1)))
import re, os
_t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lenta-istochnik.md")).read()
_t = _t[:_t.index("## Ответ")]   # история Паскаля («делит на») — цитата, не наше рассуждение
_bad = re.findall(r"подел\w+|\bделим\b|делить на|делённ\w*|вдвое меньше", _t)
check("v5 РЫЧАГ (ZAMYSEL dvojnoj-podschet-bez-deleniya): в рассуждениях статьи нет деления словами", not _bad, str(_bad))

print("\nИТОГ:", "всё сошлось" if ok else "ЕСТЬ РАСХОЖДЕНИЯ")
sys.exit(0 if ok else 1)
