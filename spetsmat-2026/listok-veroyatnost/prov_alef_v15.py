# Проверка перебором ответов листка 18ℵ версии 15 (01.10.2026). Номера — по листку v15 (полоска удалена). Печатает ALL OK.
from itertools import product, combinations
from math import comb
from fractions import Fraction as F
ok=True
def chk(n,c):
    global ok
    if not c: ok=False; print("FAIL",n)
def ps(s):
    S=[0]
    for x in s: S.append(S[-1]+x)
    return S
def orders(a,b):
    for pos in combinations(range(a+b),b):
        p=set(pos); yield tuple(-1 if i in pos else 1 for i in range(a+b))
def strict(a,b): o=list(orders(a,b)); return F(sum(all(v>0 for v in ps(x)[1:]) for x in o),len(o))
def weak(a,b): o=list(orders(a,b)); return F(sum(min(ps(x))>=0 for x in o),len(o))
Cat=lambda n: comb(2*n,n)//(n+1)
chk("2б",strict(3,2)==F(1,5) and strict(4,2)==F(1,3))
def strict_dp(a,b):  # число строгих путей подсчёта через треугольник (динамика), a+b до 12
    d={(0,0):1}
    for i in range(a+b):
        nd={}
        for (x,y),v in d.items():
            for (nx,ny) in ((x+1,y),(x,y+1)):
                if nx<=a and ny<=b and nx>ny: nd[(nx,ny)]=nd.get((nx,ny),0)+v
        d=nd
    return F(d.get((a,b),0),comb(a+b,a))
chk("3в",all(strict_dp(a,b)==F(a-b,a+b) for a in range(1,13) for b in range(a) if a+b<=12))
chk("3в=перебор",all(strict_dp(a,b)==strict(a,b) for a in range(1,7) for b in range(a) if a+b<=8))
chk("4а",[Cat(n) for n in range(8)]==[1,1,2,5,14,42,132,429])
# 4а: кучки по первому возвращению — (6,0): 2,1,2; (8,0): 5,2,2,5 = C_k·C_{n-1-k}
for n,ozh in ((3,[2,1,2]),(4,[5,2,2,5])):
    d={}
    for s_ in product((1,-1),repeat=2*n):
        S=ps(s_)
        if S[-1]==0 and min(S)>=0:
            f=next(k for k in range(1,2*n+1) if S[k]==0); d[f]=d.get(f,0)+1
    chk("4а",[d[2*k] for k in range(1,n+1)]==ozh==[Cat(k-1)*Cat(n-k) for k in range(1,n+1)])
chk("4б",all(Cat(n+1)==sum(Cat(i)*Cat(n-i) for i in range(n+1)) for n in range(12)))
# 5: вагоны через тупик — |S_n| = C_n; S_3 без 312
def tupik(n):
    res=set()
    def go(i,st,out):
        if len(out)==n: res.add(tuple(out)); return
        if i<=n: go(i+1,st+[i],out)
        if st: go(i,st[:-1],out+[st[-1]])
    go(1,[],[]); return res
chk("5 S_n",[len(tupik(n)) for n in range(1,9)]==[Cat(n) for n in range(1,9)])
chk("5 S_3",(3,1,2) not in tupik(3) and len(tupik(3))==5)
chk("пример 2314",(2,3,1,4) in tupik(4))
# 5а: деревья и триангуляции
def der(n): return 1 if n==0 else sum(der(i)*der(n-1-i) for i in range(n))
chk("5 D_n",[der(n) for n in range(9)]==[Cat(n) for n in range(9)])
chk("4в",all(strict(n+1,n)==F(1,2*n+1) for n in range(1,6)))
chk("6б",all(comb(2*n,n)-Cat(n)==comb(2*n,n+1) for n in range(1,15)))
chk("10",all((n+2)*Cat(n+1)==(4*n+2)*Cat(n) for n in range(1,5)))
chk("7",all(weak(a,b)==F(a-b+1,a+1) for a in range(1,9) for b in range(a+1)))
for n in range(1,8):
    N=2*n; P=[ps(s) for s in product((1,-1),repeat=N)]
    chk("11в",sum(all(v!=0 for v in S[1:]) for S in P)==comb(N,n)==sum(min(S)>=0 for S in P))
    chk("первое возвращение (убрано из листка)",sum(all(v!=0 for v in S[1:-1]) and S[-1]==0 for S in P)==2*Cat(n-1))
    # 13: мосты, начинающиеся вверх, T=2M-S — биекция на пути, ни разу не возвращающиеся на ось
    img=set(); m_=0
    for S in P:
        if S[-1]==0 and S[1]==1:
            m_+=1; M=0; T=[]
            for v in S: M=max(M,v); T.append(2*M-v)
            img.add(tuple(T))
    chk("линия рекордов (убрано из листка)",len(img)==m_ and img=={tuple(S) for S in P if all(v>0 for v in S[1:])})
    # 14: Петя и Вася — поровну орлов
    chk("Петя и Вася (убрано из листка)",sum(comb(n,k)**2 for k in range(n+1))==comb(N,n))
    # 8в: верхние звенья у мостов равномерны
    up={}
    for S in P:
        if S[-1]==0:
            k=sum(1 for i in range(N) if max(S[i],S[i+1])>0); up[k]=up.get(k,0)+1
    chk("9",set(up.values())=={Cat(n)})
    # 17а: время над осью при свободном конце = последний ноль
    t={};l={}
    for S in P:
        k=sum(1 for i in range(N) if max(S[i],S[i+1])>0); t[k]=t.get(k,0)+1
        z=max(i for i in range(N+1) if S[i]==0); l[z]=l.get(z,0)+1
    chk("14б,15а",all(t.get(2*k,0)==l.get(2*k,0)==comb(2*k,k)*comb(N-2*k,n-k) for k in range(n+1)))
    ch=[sum(1 for k in range(1,N) if S[k]==0 and S[k-1]*S[k+1]<0) for S in P]
    chk("16б",all(F(ch.count(r),4**n)==F(2*comb(N-1,n-1-r),2**(N-1)) for r in range(n)))
    chk("16в",F(ch.count(0),4**n)==2*F(comb(N,n),4**n))
# 12а: 2n=6 — кучки 5,9,5,1
P=[ps(s) for s in product((1,-1),repeat=6)]
nonneg=[S[-1] for S in P if min(S)>=0]; depth=[-min(S) for S in P if S[-1]==0]
chk("12а",[nonneg.count(h) for h in (0,2,4,6)]==[depth.count(d) for d in (0,1,2,3)]==[5,9,5,1])
# 16в
u=lambda j: F(comb(2*j,j),4**j); p=[u(k)*u(50-k) for k in range(51)]
a=float(sum(p[:6])); b=float(sum(p[45:])); c=float(sum(p[23:28]))
chk("14в",abs(a-0.2192)<1e-3 and abs(b-a)<1e-12 and abs(c-0.0631)<1e-3)
# 3а: концы путей Дика — точки (m,h), 0<=h<=m, m-h чётно
from itertools import product as _pr
kon=set()
for L in range(0,9):
    for st in _pr((1,-1),repeat=L):
        S=ps(st)
        if min(S)>=0: kon.add((L,S[-1]))
chk("3а",kon=={(m,h) for m in range(9) for h in range(m+1) if (m-h)%2==0})
chk("6а",[comb(2*n,n)-Cat(n) for n in (2,3)]==[4,15]==[comb(4,1),comb(6,2)])
print("15в (моменты 0–10, 90–100, 45–55): первые 10 — %.3f, последние 10 — %.3f, 46–55 — %.3f"%(a,b,c))
# 8а: циклическая лемма — ровно a−b начальных мест, для которых все суммы положительны
for a_ in range(1,7):
    for b_ in range(a_):
        L=a_+b_
        for pl in combinations(range(L),a_):
            x=[1 if i in pl else -1 for i in range(L)]
            good=sum(all(sum(x[(st+j)%L] for j in range(t+1))>0 for t in range(L)) for st in range(L))
            chk("8а",good==a_-b_)
# 8б: из леммы — путей Дика C_n = C(2n+1,n)/(2n+1)
chk("8б",all(Cat(n)==comb(2*n+1,n)//(2*n+1) for n in range(12)))
# --- часть III по статье STATYA-chast-III.md (12а, 12б, 13б) ---
def ps(s):
    S=[0]
    for x in s: S.append(S[-1]+x)
    return S
B=lambda m:[s for s in product((1,-1),repeat=m) if min(ps(s))>=0]          # пути Дика (конец любой)
P=lambda m:[s for s in product((1,-1),repeat=m) if all(v>0 for v in ps(s)[1:])]  # после начала выше оси
Z=lambda m:[s for s in product((1,-1),repeat=m) if all(v!=0 for v in ps(s)[1:])] # после начала не на оси
A=lambda m:[s for s in product((1,-1),repeat=m) if ps(s)[-1]==0]             # кончаются на оси
for m in range(1,13):
    # Л1 «ножки»: P_m ↔ B_{m-1}, отрезать первое звено ↗ и опустить на 1
    img={s[1:] for s in P(m)}; chk("Л1 m=%d"%m, img==set(B(m-1)) and len(img)==len(P(m)))
for n in range(1,7):
    m=2*n
    chk("Л2 n=%d"%n, len(B(m))==2*len(B(m-1)))                  # удвоение на чётной длине
    chk("Z=2P=B n=%d"%n, len(Z(m))==2*len(P(m))==len(B(m)))
    chk("|B|=C(2n,n) n=%d"%n, len(B(m))==comb(m,n)==len(A(m)))
    # телескоп через 6в: путей Дика в (2n,2j) = C(2n,n-j)-C(2n,n-j-1)
    chk("телескоп n=%d"%n, all(sum(1 for s in B(m) if ps(s)[-1]==2*j)==comb(m,n-j)-(comb(m,n-j-1) if n-j-1>=0 else 0) for j in range(n+1)))
    # биекция «самая низкая точка»: мост глубины d ↔ путь Дика с концом 2d
    def f(s):
        S=ps(s); d=-min(S); t=S.index(-d)
        return s[t:]+tuple(-x for x in reversed(s[:t])), d
    im=[f(s) for s in A(m)]
    chk("биекция n=%d"%n, {x for x,_ in im}==set(B(m)) and len({x for x,_ in im})==len(im)
        and all(ps(x)[-1]==2*d for x,d in im))
# 13а: при 2n=6 группы 5,9,5,1 у обеих сторон
S6=[ps(s) for s in A(6)]; D6=[ps(s) for s in B(6)]
chk("12а", [sum(-min(S)==d for S in S6) for d in range(4)]==[sum(D[-1]==2*d for D in D6) for d in range(4)]==[5,9,5,1])
# --- v15: 11б (вдвое больше путей Дика длины 2n−1), 11в телескоп по нечётной строке, 13 оценка ---
for n in range(1,7):
    chk("11б n=%d"%n, len(Z(2*n))==2*len(B(2*n-1)))
    chk("11в телескоп n=%d"%n, len(B(2*n-1))==comb(2*n-1,n))
from fractions import Fraction as Fr
u=lambda n: Fr(comb(2*n,n),4**n)
chk("13а", all(u(n)**2<=Fr(1,2*n+1) for n in range(300)))
chk("13б", u(5000)<Fr(1,100))
print("ALL OK" if ok else "SOME FAIL")
