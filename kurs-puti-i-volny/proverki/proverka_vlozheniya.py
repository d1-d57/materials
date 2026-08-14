from math import comb
from collections import defaultdict

def halfline(N,x,y):
    """пути x->y за N шагов, не касающиеся уровня -1 (одна стенка)"""
    f=defaultdict(int); f[x]=1
    for _ in range(N):
        g=defaultdict(int)
        for h,c in f.items():
            for h2 in (h-1,h+1):
                if h2>=0: g[h2]+=c
        f=g
    return f[y]
def free(N,x,y):
    d=y-x
    if (N+d)%2 or abs(d)>N: return 0
    return comb(N,(N+d)//2)

print("=== принцип отражения на луче: свободный член минус зеркальный ===")
print("   #(x->y, N шагов, не ниже 0) = C(N,(N+y-x)/2) - C(N,(N+y+x+2)/2)")
bad=[]
for N in range(1,13):
    for x in range(0,9):
        for y in range(0,9):
            lhs=halfline(N,x,y)
            rhs=free(N,x,y)-free(N,-x-2,y)
            if lhs!=rhs: bad.append((N,x,y,lhs,rhs))
print("   N=1..12, x,y=0..8:", "сходится всюду ✓" if not bad else f"РАСХОЖДЕНИЯ {bad[:3]}")

print()
print("=== ЗЕРКАЛЬНЫЙ ЧЛЕН ОБНУЛЯЕТСЯ, если старт унесён от стенки дальше длины пути ===")
for N in (6,10,14):
    for x in (0,2,N//2, N, N+2):
        mirror=free(N,-x-2,N%2 if (N-x)%2 else x)  # какой-нибудь достижимый конец
        y = x if (N%2==0) else x+1
        m2=free(N,-x-2,y)
        print(f"   N={N:2d}, старт x={x:2d}: зеркальный член C(N,(N+y+x+2)/2) = {m2}"
              f"   {'-> ноль, стенка не чувствуется' if m2==0 else ''}")

print()
print("=== СЛЕДСТВИЕ: счёт по ПРЯМОЙ есть частный случай счёта по ЛУЧУ ===")
ok=True
for N in range(1,13):
    x=N+2                      # старт дальше, чем путь может пройти
    for y in range(max(0,x-N), x+N+1):
        if halfline(N,x,y)!=free(N,x,y): ok=False
print("   при x > N: #(луч, x->y) == C(N,(N+y-x)/2) для всех достижимых y:", "✓" if ok else "НЕТ")
print("   то есть биномиальные коэффициенты — это луч со стартом, унесённым от стенки")

print()
print("=== а вот ЭКСКУРСИИ (старт и финиш в нуле) биномов НЕ дают ===")
print("   пути Дика 0->0:", [halfline(2*n,0,0) for n in range(1,8)], " (Каталан)")
print("   свободные 0->0:", [free(2*n,0,0) for n in range(1,8)], " (центральные биномы)")
print("   -> из производящей функции ЭКСКУРСИЙ прямую не достать; нужны концы")

print()
print("=== то же с весом по площади: работает ли? ===")
def halfline_area(N,x,y):
    cur={x:{0:1}}
    for _ in range(N):
        nxt=defaultdict(lambda: defaultdict(int))
        for h,pol in cur.items():
            for h2 in (h-1,h+1):
                if h2>=0:
                    for a,c in pol.items(): nxt[h2][a+h2]+=c
        cur=nxt
    return dict(cur.get(y,{}))
def free_area(N,x,y):
    cur={x:{0:1}}
    for _ in range(N):
        nxt=defaultdict(lambda: defaultdict(int))
        for h,pol in cur.items():
            for h2 in (h-1,h+1):
                for a,c in pol.items(): nxt[h2][a+h2]+=c
        cur=nxt
    return dict(cur.get(y,{}))
ok=True
for N in range(2,11):
    x=N+2
    for y in range(max(0,x-N),x+N+1):
        if halfline_area(N,x,y)!=free_area(N,x,y): ok=False
print("   при x > N совпадают и ПОЛНЫЕ распределения по площади:", "✓" if ok else "НЕТ")
print("   значит и гауссовы биномы, и разбиения достаются из луча — просто стартом подальше от стенки")
