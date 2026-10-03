from itertools import product, combinations
from math import comb
from fractions import Fraction as F
def paths(n):
    for s in product((1,-1), repeat=n): yield s
def ps(s):
    S=[0]
    for x in s: S.append(S[-1]+x)
    return S
C=lambda n: comb(2*n,n)//(n+1)
ok=True
def chk(name, cond):
    global ok
    if not cond: ok=False; print("FAIL", name)
# 1 ballot
for a in range(1,9):
    for b in range(0,a):
        seqs=[tuple(-1 if i in pos else 1 for i in range(a+b)) for pos in map(set,combinations(range(a+b),b))]
        strict=sum(all(v>0 for v in ps(c)[1:]) for c in seqs)
        weak=sum(all(v>=0 for v in ps(c)[1:]) for c in seqs)
        chk(f"ballot strict {a},{b}", F(strict,len(seqs))==F(a-b,a+b))
        chk(f"ballot weak {a},{b}", F(weak,len(seqs))==F(a-b+1,a+1))
for n in range(1,8):
    N=2*n; allp=list(paths(N)); P=[ps(s) for s in allp]
    noret=sum(all(v!=0 for v in S[1:]) for S in P)
    at0=sum(S[-1]==0 for S in P)
    nonneg=sum(all(v>=0 for v in S) for S in P)
    chk("noret",noret==comb(N,n)==at0==nonneg)
    first=sum(S[-1]==0 and all(v!=0 for v in S[1:-1]) for S in P)
    chk("firstret", first==2*C(n-1))
    # Chung-Feller: bridges, steps above axis (segment above if max endpoint >0)
    cnt={}
    for S in P:
        if S[-1]!=0: continue
        k=sum(1 for i in range(N) if max(S[i],S[i+1])>0)
        cnt[k]=cnt.get(k,0)+1
    chk("CF", sorted(cnt)==list(range(0,N+1,2)) and set(cnt.values())=={C(n)})
    # arcsine: time above (free end) and last zero
    tab={}; lz={}
    for S in P:
        k=sum(1 for i in range(N) if max(S[i],S[i+1])>0); tab[k]=tab.get(k,0)+1
        z=max(i for i in range(N+1) if S[i]==0); lz[z]=lz.get(z,0)+1
    for k in range(0,n+1):
        chk("arcsine-time", tab.get(2*k,0)==comb(2*k,k)*comb(N-2*k,n-k))
        chk("arcsine-lastzero", lz.get(2*k,0)==comb(2*k,k)*comb(N-2*k,n-k))
    # reflection in record line T=2M-S : bridges starting up -> strictly positive
    img=set()
    for S in P:
        if S[-1]!=0 or S[1]!=1: continue
        M=0;T=[]
        for v in S: M=max(M,v); T.append(2*M-v)
        chk("rec-pos", all(t>0 for t in T[1:]))
        img.add(tuple(T))
    chk("rec-bij", len(img)==comb(N,n)//2==sum(all(v>0 for v in S[1:]) for S in P))
    # two walkers meet
    chk("meet", sum(comb(n,k)**2 for k in range(n+1))==comb(N,n))
# first hit -1 at step 2n+1 = C_n ; cycle lemma
for n in range(0,6):
    N=2*n+1
    h=sum(1 for s in paths(N) if ps(s)[-1]==-1 and all(v>=0 for v in ps(s)[:-1]))
    chk("hit-1",h==C(n))
    import itertools
    for pos in map(set,combinations(range(N),n)):
        c=tuple(-1 if i in pos else 1 for i in range(N))
        good=sum(all(v>0 for v in ps(c[i:]+c[:i])[1:]) for i in range(N))
        chk("cycle",good==1)
# gambler capital x, 6 steps never below 0
g=[sum(all(x+v>=0 for v in ps(s)) for s in paths(6)) for x in range(8)]
chk("gambler", g==[20,35,50,56,62,63,64,64])
# corridor 4 cells start edge, stay N steps : Fibonacci
fib=[1,1]
for _ in range(20): fib.append(fib[-1]+fib[-2])
for N in range(1,14):
    c=sum(all(0<=v<=3 for v in ps(s)) for s in paths(N))
    chk("corridor4", c==fib[N])
# max distribution: P(max>=h)=P(S>=h)+P(S>h)
for N in range(1,13):
    P=[ps(s) for s in paths(N)]
    for h in range(1,N+1):
        chk("max", sum(max(S)>=h for S in P)==sum(S[-1]>=h for S in P)+sum(S[-1]>h for S in P))
# lead changes: define sign changes: S_{k-1}, S_{k+1} opposite sign with S_k=0
for n in range(1,8):
    N=2*n; P=[ps(s) for s in paths(N)]
    d={}
    for S in P:
        r=sum(1 for k in range(1,N) if S[k]==0 and S[k-1]*S[k+1]<0)
        d[r]=d.get(r,0)+1
    lec={r: 4*comb(N-1,n-1-r) for r in range(n)}  # число путей = вероятность 2C(2n-1,n-1-r)/2^(2n-1) * 2^(2n)
    res= all(d.get(r,0)==lec.get(r,0) for r in range(n+1))
    print("lead changes 2n=",N, dict(sorted(d.items())), "lecture formula", lec, "MATCH" if res else "DIFF")
print("ALL OK" if ok else "SOME FAIL")
