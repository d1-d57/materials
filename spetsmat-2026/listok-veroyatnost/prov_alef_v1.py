# Проверка перебором ответов черновика 18ℵ v1 (30.09). Печатает ALL OK.
# Номера задач в комментариях ниже — по черновику 1 (с нуля); в черновике 1.1 листок перенумерован с 1: задача k здесь = задача k+1 в листке.
from itertools import product, combinations
from math import comb
from fractions import Fraction as F
ok=True
def chk(name,c):
    global ok
    if not c: ok=False; print("FAIL",name)
def ps(s):
    S=[0]
    for x in s: S.append(S[-1]+x)
    return S
Cat=lambda n: comb(2*n,n)//(n+1)
def orders(a,b):
    for pos in combinations(range(a+b),b):
        p=set(pos); yield tuple(-1 if i in p else 1 for i in range(a+b))
# зад.1 и 0
def weak(a,b): o=list(orders(a,b)); return F(sum(min(ps(x))>=0 for x in o),len(o))
def strict(a,b): o=list(orders(a,b)); return F(sum(all(v>0 for v in ps(x)[1:]) for x in o),len(o))
chk("1a", weak(3,2)==F(1,2) and strict(3,2)==F(1,5))
chk("1b", weak(3,3)==F(1,4) and strict(3,3)==0)
for a in range(1,9):
    for b in range(a+1):
        chk("0weak",weak(a,b)==F(a-b+1,a+1))
        if b<a: chk("0strict",strict(a,b)==F(a-b,a+b))
# зад.2 треугольник: число неотриц. путей в (k,h)
T={(0,0):1}
for k in range(1,11):
    for h in range(0,k+1):
        T[(k,h)]=T.get((k-1,h-1),0)+T.get((k-1,h+1),0)
for k in range(11):
    for h in range(k%2,k+1,2):
        a=(k+h)//2; b=(k-h)//2
        chk("2",T[(k,h)]==comb(k,a)*(a-b+1)//(a+1))
print("треугольник, строка 10:",[T[(10,h)] for h in range(0,11,2)])
# зад.3
C=[1]
for n in range(12): C.append(sum(C[i]*C[n-i] for i in range(n+1)))
chk("3",C[:7]==[1,1,2,5,14,42,132] and all(C[n]==Cat(n) for n in range(12)))
# зад.9 тождество
chk("9",all((n+2)*Cat(n+1)==2*(2*n+1)*Cat(n) for n in range(30)))
# триангуляции: число = C_n
def tri(m):  # число триангуляций выпуклого m-угольника
    t={}
    for L in range(2,m+1): pass
    from functools import lru_cache
    @lru_cache(None)
    def f(i,j):
        if j-i<2: return 1
        return sum(f(i,k)*f(k,j) for k in range(i+1,j))
    return f(0,m-1)
chk("5tri",all(tri(n+2)==Cat(n) for n in range(1,10)))
# зад.11,12,14,17 на путях
for n in range(1,8):
    N=2*n; P=[ps(s) for s in product((1,-1),repeat=N)]
    noret=sum(all(v!=0 for v in S[1:]) for S in P)
    nonneg=sum(min(S)>=0 for S in P)
    chk("11",noret==nonneg==comb(N,n))
    # телескоп: строго положительные, конец 2h
    tel=sum(comb(N-1,n+h-1)-comb(N-1,n+h) for h in range(1,n+1))
    chk("11tel",tel==sum(all(v>0 for v in S[1:]) for S in P)==comb(N,n)//2)
    # 12а: разрез в первом минимуме, B затем A повёрнутая на 180°
    img=set()
    for S in P:
        if S[-1]!=0: continue
        m=min(S); t=S.index(m)
        steps=[S[i+1]-S[i] for i in range(N)]
        A=steps[:t]; B=steps[t:]
        new=B+[-x for x in reversed(A)]
        Q=ps(new); chk("12a-nonneg",min(Q)>=0)
        img.add(tuple(new))
    chk("12a-bij",len(img)==comb(N,n)==nonneg)
    # 14 первое возвращение
    first=sum(S[-1]==0 and all(v!=0 for v in S[1:-1]) for S in P)
    u=lambda j: F(comb(2*j,j),4**j)
    chk("14",F(first,4**n)==F(2*Cat(n-1),4**n)==u(n-1)-u(n))
    # 17а: ни одной смены лидера
    ch=[sum(1 for k in range(1,N) if S[k]==0 and S[k-1]*S[k+1]<0) for S in P]
    chk("17a",F(ch.count(0),4**n)==F(2*comb(N-1,n-1),2**(N-1)))
    for r in range(n):
        chk("17b",F(ch.count(r),4**n)==F(2*comb(N-1,n-1-r),2**(N-1)))
    # 16: последний ноль
    lz=[max(i for i in range(N+1) if S[i]==0) for S in P]
    for k in range(n+1):
        chk("16",F(lz.count(2*k),4**n)==u(k)*u(n-k))
    # 8 Чжун—Феллер
    cnt={}
    for S in P:
        if S[-1]!=0: continue
        k=sum(1 for i in range(N) if S[i]+S[i+1]>0); cnt[k]=cnt.get(k,0)+1
    chk("8",set(cnt.values())=={Cat(n)} and len(cnt)==n+1)
# зад.7 цикл-лемма (a>b: ровно a-b хороших начал)
for a in range(1,8):
    for b in range(a):
        for w in orders(a,b):
            g=sum(all(v>0 for v in ps(w[i:]+w[:i])[1:]) for i in range(a+b))
            chk("7",g==a-b)
# зад.15 коридор из 4 клеток 0..3, старт в 0
fib=[1,1]
for _ in range(30): fib.append(fib[-1]+fib[-2])
for N in range(1,15):
    stay=0; home=0
    for s in product((1,-1),repeat=N):
        S=ps(s)
        if all(0<=v<=3 for v in S):
            stay+=1; home+= S[-1]==0
    chk("15a",stay==fib[N])
    if N%2==0: chk("15b",home==fib[N-2])  # F_{N-1} при fib[k]=F_{k+1}
print("15: N=10 ->",fib[10],"/ 1024")
# 16: числа для 2n=100 и 2n=20
from fractions import Fraction
def u(j): return Fraction(comb(2*j,j),4**j)
for n in (10,50):
    p=[u(k)*u(n-k) for k in range(n+1)]
    h=n//2
    print(f"2n={2*n}: P(последнее равенство после 0-го или 2-го броска)={float(p[0]+p[1]):.4f}; P(после броска {2*h-2},{2*h} или {2*h+2})={float(p[h-1]+p[h]+p[h+1]):.4f}; P(последнее равенство в первой четверти, 2k<={n//2})={float(sum(p[k] for k in range(n+1) if 4*k<=n)):.4f}")
    chk("16sum",sum(p)==1)
print("ALL OK" if ok else "SOME FAIL")
