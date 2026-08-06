from math import comb, cos, pi, sqrt, exp
from fractions import Fraction

def d(m,n):
    """пути Дика длины 2n высоты <= m"""
    f=[0]*(m+3); f[1]=1
    for _ in range(2*n):
        g=[0]*(m+3)
        for x in range(1,m+2):
            if f[x]:
                if x-1>=1: g[x-1]+=f[x]
                if x+1<=m+1: g[x+1]+=f[x]
        f=g
    return f[1]

print("=== 1. подходящие дроби цепной дроби Каталана = известные последовательности ===")
for m in range(1,8):
    seq=[d(m,n) for n in range(1,10)]
    print(f"  высота <= {m}: {seq}   рост 2cos(pi/{m+2}) = {2*cos(pi/(m+2)):.5f}")
print(f"  высота <= oo : {[comb(2*n,n)//(n+1) for n in range(1,10)]}   (Каталан)")

print()
print("=== 2. знаменатели цепной дроби = многочлены Фибоначчи; при z=1 — числа Фибоначчи ===")
def P(m):
    # P_0=P_1=1, P_{m+1}=P_m - z P_{m-1}  (коэффициенты по z)
    a=[1]; b=[1]
    for k in range(1,m+1):
        c=[0]*(max(len(b),len(a)+1))
        for i,x in enumerate(b): c[i]+=x
        for i,x in enumerate(a): c[i+1]-=x
        a,b=b,c
    while b and b[-1]==0: b.pop()
    return b
for m in range(0,8):
    p=P(m); val=sum(p)  # z=1
    print(f"  P_{m}(z) = {p}   P_{m}(1) = {val}   |коэф| = {[abs(c) for c in p]}")
print("  -> |коэффициенты| P_m = диагонали треугольника Паскаля, P_m(1) периодично: это Фибоначчи-многочлены")

print()
print("=== 3. кристаллографическое ограничение: когда 2cos(2pi/n) целое? ===")
for n in range(1,13):
    v=2*cos(2*pi/n)
    print(f"   n={n:2d}: 2cos(2pi/{n}) = {v:+.6f}  {'ЦЕЛОЕ' if abs(v-round(v))<1e-9 else ''}")

print()
print("=== 4. ещё одна специализация: шаги +1,0,-1 (числа Моцкина) ===")
def motzkin(n):
    f={0:1}
    for _ in range(n):
        g={}
        for h,c in f.items():
            for h2 in (h-1,h,h+1):
                if h2>=0: g[h2]=g.get(h2,0)+c
        f=g
    return f.get(0,0)
print("  Моцкин:", [motzkin(n) for n in range(1,12)])
print("  цепная дробь 1/(1-z-z^2/(1-z-z^2/...))  — тот же приём, другой набор шагов")

print()
print("=== 5. предельный переход: две формулы для отрезка -> тождество для тэта-функции ===")
print("   фиксируем t = n/m^2, растим m; сравниваем сумму по образам и сумму по спектру")
def two_formulas(m,n):
    M=m+2
    spec=2/M*sum((2*cos(k*pi/M))**(2*n)*sin_(k*pi/M)**2 for k in range(1,M))
    return spec
from math import sin as sin_
for t in (0.05,0.1,0.2):
    print(f"   t = {t}:")
    for m in (10,20,40,80):
        n=int(t*m*m)
        if n<1: continue
        val=d(m,n)
        # нормируем: доля путей * sqrt(n)
        norm=val/ (comb(2*n,n)) * m
        print(f"      m={m:3d} n={n:5d}:  d_m(n)/C(2n,n) * m = {norm:.6f}")
