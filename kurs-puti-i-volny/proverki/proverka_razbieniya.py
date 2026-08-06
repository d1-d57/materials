from collections import defaultdict
from functools import lru_cache
P=45
def mul(a,b):
    r=[0]*P
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if i+j<P: r[i+j]+=x*y
    return r
def one():
    r=[0]*P; r[0]=1; return r
def qpow(k):
    r=[0]*P
    if k<P: r[k]=1
    return r
def inv(a):
    r=[0]*P; r[0]=1
    for n in range(1,P): r[n]=-sum(a[k]*r[n-k] for k in range(1,n+1))
    return r
def sub(a,b): return [x-y for x,y in zip(a,b)]
@lru_cache(None)
def _qb(n,k):
    if k<0 or k>n: return ()
    if k in (0,n): return (1,)
    u=list(_qb(n-1,k-1)); v=list(_qb(n-1,k))
    r=[0]*max(len(u),len(v)+k)
    for i,c in enumerate(u): r[i]+=c
    for i,c in enumerate(v): r[i+k]+=c
    while r and r[-1]==0: r.pop()
    return tuple(r)
def qbin(n,k):
    c=list(_qb(n,k)); return (c+[0]*P)[:P]

# --- 1. СВОБОДНЫЕ пути (без стенок) с весом площади
def free_area(N,y):
    cur={0:{0:1}}
    for _ in range(N):
        nxt=defaultdict(lambda: defaultdict(int))
        for h,pol in cur.items():
            for h2 in (h-1,h+1):
                for a,c in pol.items(): nxt[h2][a+h2]+=c
        cur=nxt
    return dict(cur.get(y,{}))

print("=== 1. свободные пути (СТЕНОК НЕТ) + площадь = гауссов бином = разбиения в коробке ===")
m=lambda N,y:(y*y+2*(N+1)*y-N*N)//4
ok=True
for N in range(2,15,2):
    for y in range(-N,N+1,2):
        d=free_area(N,y)
        if not d: continue
        e=defaultdict(int)
        for i,c in enumerate(_qb(N,(N+y)//2)): e[m(N,y)+2*i]+=c
        if dict(d)!=dict(e): ok=False
print("   N=2..14, все концы:", "сходится ✓" if ok else "РАСХОЖДЕНИЕ")

print()
print("=== 2. коробка растёт: гауссов бином -> разбиения не более чем на k частей ===")
def parts_at_most(k):
    r=one()
    for i in range(1,k+1): r=mul(r, inv(sub(one(),qpow(i))))
    return r
for k in (2,3,4):
    tgt=parts_at_most(k)
    for N in (k+6, k+14, k+30):
        b=qbin(N,k)
        d=min(20, N-k+1)
        same=b[:d]==tgt[:d]
        print(f"   [N={N:2d}, k={k}]_q против 1/((1-q)...(1-q^{k})): первые {d} коэф. {'совпали ✓' if same else 'нет'}")

print()
print("=== 3. снимаем и вторую границу: получается ЧИСЛО РАЗБИЕНИЙ ===")
allp=one()
for i in range(1,P): allp=mul(allp, inv(sub(one(),qpow(i))))
@lru_cache(None)
def p(n):
    if n<0: return 0
    if n==0: return 1
    s=0;k=1
    while True:
        a=k*(3*k-1)//2; b=k*(3*k+1)//2
        if a>n and b>n: break
        s+=(-1)**(k+1)*(p(n-a)+p(n-b)); k+=1
    return s
print("   prod 1/(1-q^i) :", allp[:14])
print("   p(n)           :", [p(n) for n in range(14)])
print("   совпало:", allp[:P]==[p(n) for n in range(P)])
print("   и это предел гауссовых биномов при обеих растущих сторонах коробки")

print()
print("=== 4. а на ЛУЧЕ (одна стенка) площадь даёт НЕ разбиения ===")
def dyck_area_all(maxsteps=200):
    cur={0:{0:1}}; tot=[0]*P; tot[0]=1
    for step in range(maxsteps):
        nxt=defaultdict(lambda: defaultdict(int))
        for h,pol in cur.items():
            for h2 in (h-1,h+1):
                if h2>=0:
                    d=h2 if h2>h else 0
                    for a,c in pol.items():
                        if a+d<P: nxt[h2][a+d]+=c
        cur={h:dict(x) for h,x in nxt.items()}
        if step%2==1:
            for a,c in cur.get(0,{}).items():
                if a<P: tot[a]+=c
    return tot
dy=dyck_area_all()
print("   пути Дика по площади:", dy[:14])
print("   p(n)                :", [p(n) for n in range(14)])
print("   совпало:", dy[:20]==[p(n) for n in range(20)])
