from itertools import combinations, product, permutations
from math import comb, factorial, prod

def C(n,k):  # по определению 1: число k-подмножеств [n]
    return sum(1 for _ in combinations(range(1,n+1),k))

print("C(3,2) =", C(3,2), [set(s) for s in combinations([1,2,3],2)])
# утв.2: слова
for n in range(0,8):
    for k in range(n+1):
        assert C(n,k)==sum(1 for w in product('01',repeat=n) if w.count('1')==k)
print("утв.2 (слова) ok для n<=7")
# слова из примера
enc=lambda S,n:''.join('1' if i in S else '0' for i in range(1,n+1))
print("{1,2,3}⊂[5] ->",enc({1,2,3},5)," {2,3,4} ->",enc({2,3,4},5))
# утв.3,4,5
for n in range(0,15):
    assert C(n,0)==C(n,n)==1
    if n>=1: assert C(n,1)==C(n,n-1)==n
    if n>=2: assert C(n,2)==n*(n-1)//2==sum(range(1,n))
    for k in range(n+1): assert C(n,k)==C(n,n-k)
print("утв.3–5 ok для n<=14 (утв.3 вторая часть — только n>=1; утв.4 — n>=2)")
# лесенка: строки и столбцы
for n in range(2,12):
    cells={(i,j) for i in range(1,n+1) for j in range(1,n+1) if i<j}
    rows=[sum(1 for (i,j) in cells if i==r) for r in range(1,n+1)]
    cols=[sum(1 for (i,j) in cells if j==c) for c in range(1,n+1)]
    assert rows==list(range(n-1,-1,-1)) and cols==list(range(0,n)) and len(cells)==C(n,2)
    # шоколадка: нижняя лесенка сдвигается на клетку вверх
    lower={(j,i) for (i,j) in cells}
    shifted={(i-1,j) for (i,j) in lower}
    assert not (cells & shifted)
    U=cells|shifted
    assert U=={(i,j) for i in range(1,n) for j in range(1,n+1)}, n   # строки 1..n-1, столбцы 1..n
print("лесенка и шоколадка (n-1 рядов по n) ok для n=2..11")
# многоугольник
for n in range(3,15):
    assert C(n,2)-n==n*(n-3)//2
print("диагонали n(n-3)/2 ok, n>=3")
# Гаусс
print("1+..+100 =", sum(range(1,101)), "=", 100*101//2)
# треугольник 0–6 и «одна клетка»
for n in range(7): print(n, [C(n,k) for k in range(n+1)])
fill=[(n,k) for n in range(7) for k in range(n+1) if min(k,n-k)<=2]
bad=[(n,k) for n in range(7) for k in range(n+1) if min(k,n-k)>=3]
print("клеток с k>=3 и n-k>=3 в строках 0–6:", bad)
# правило Паскаля в видимом треугольнике (кроме ?)
print("6=3+3:",C(4,2)==C(3,1)+C(3,2)," 10=4+6:",C(5,2)==C(4,1)+C(4,2))
for n in range(2,20):
    for k in range(1,n):
        assert C(n,k)==C(n-1,k-1)+C(n-1,k)
print("утв.7 ok n<=19")
print("C(7,2),C(7,3),C(8,3):",C(7,2),C(7,3),C(8,3), C(7,2)+C(7,3)==C(8,3)==56)
print("C(7,3) через C(6,3): ",C(6,2)+C(6,3))
print("C(6,3)=C(5,2)+C(5,3):",C(5,2),C(5,3),C(5,2)+C(5,3),C(6,3))
print("сумма k=1..6:",sum(C(6,k) for k in range(1,7)), "=2^6-1", 2**6-1)
print("разбивка Чараки (по 1..6):",[C(6,k) for k in range(1,7)])
# утв.8: прямой подсчёт команд с капитаном
for n in range(1,9):
    for k in range(0,n):
        teams=sum(1 for T in combinations(range(n),k+1) for cap in T)
        assert teams==n*C(n-1,k)==(n-k)*C(n,k)==(k+1)*C(n,k+1)
print("утв.8 ok n<=8 (перебор команд с капитаном)")
print("футбол:",25*comb(24,10),15*comb(25,10),11*comb(25,11))
# следствие 9 и т.11
from fractions import Fraction as F
for n in range(0,25):
    for k in range(0,n):
        assert F(comb(n,k+1))==F(n-k,k+1)*comb(n,k)
    for k in range(0,n+1):
        p=prod(range(n-k+1,n+1))  # пустое произведение =1 при k=0
        assert comb(n,k)==p//factorial(k)==factorial(n)//(factorial(k)*factorial(n-k))
        if k>=1: assert F(comb(n,k))==F(n,k)*comb(n-1,k-1)
print("сл.9, т.11, диагональный шаг ok n<=24")
print("10! =",factorial(10), " 0! =",factorial(0))
for n in range(0,7): assert factorial(n)==sum(1 for _ in permutations(range(n)))
print("n! = число расстановок, n<=6")
print("16·15·14·13/(1·2·3·4) =",16*15*14*13,"/",24,"=",16*15*14*13//24, C(16,4))
print("6·5·4/(1·2·3) =",6*5*4//6)
# упорядоченные наборы
for n in range(0,8):
    for k in range(n+1):
        assert sum(1 for _ in permutations(range(n),k))==prod(range(n-k+1,n+1))==C(n,k)*factorial(k)
print("упорядочить-поделить ok")
# Паскаль: задача и следствие 12
print("3·4·5·6/(1·2·3·4) =",3*4*5*6,"/",24,"=",3*4*5*6//24, " = C(6,2)=C(6,4)=",comb(6,2))
# сл.12 Паскаля: основание из m клеток = строка m-1; верхняя клетка — j-я сверху
for m in range(2,20):
    N=m-1
    for j in range(1,m):  # верхняя = j-я сверху, нижняя = (j+1)-я
        up,low=comb(N,j-1),comb(N,j)
        assert F(up,low)==F(j, m-j)   # клеток от верхней до верха вкл. = j; от нижней до низа вкл. = m-j
print("сл.12 Паскаля (отношение j:(m-j)) ok; основание m у Паскаля = строка m-1")
