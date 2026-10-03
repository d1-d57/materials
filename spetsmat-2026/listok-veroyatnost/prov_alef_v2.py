# Проверка перебором ответов листка 18ℵ версии 2 (30.09, 23:59). Номера — по листку v2. Печатает ALL OK.
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
chk("3б",all(strict(a,b)==F(a-b,a+b) for a in range(1,9) for b in range(a) if a+b<=8))
chk("4а",[Cat(n) for n in range(8)]==[1,1,2,5,14,42,132,429])
chk("4в",all(strict(n+1,n)==F(1,2*n+1) for n in range(1,6)))
chk("6а",all(comb(2*n,n)-Cat(n)==comb(2*n,n+1) for n in range(1,15)))
chk("9а",all((n+2)*Cat(n+1)==(4*n+2)*Cat(n) for n in range(1,5)))
chk("10",all(weak(a,b)==F(a-b+1,a+1) for a in range(1,9) for b in range(a+1)))
for n in range(1,8):
    N=2*n; P=[ps(s) for s in product((1,-1),repeat=N)]
    chk("11",sum(all(v!=0 for v in S[1:]) for S in P)==comb(N,n)==sum(min(S)>=0 for S in P))
    # 8в: верхние звенья у мостов равномерны
    up={}
    for S in P:
        if S[-1]==0:
            k=sum(1 for i in range(N) if max(S[i],S[i+1])>0); up[k]=up.get(k,0)+1
    chk("8",set(up.values())=={Cat(n)})
    # 17а: время над осью при свободном конце = последний ноль
    t={};l={}
    for S in P:
        k=sum(1 for i in range(N) if max(S[i],S[i+1])>0); t[k]=t.get(k,0)+1
        z=max(i for i in range(N+1) if S[i]==0); l[z]=l.get(z,0)+1
    chk("16б,17а",all(t.get(2*k,0)==l.get(2*k,0)==comb(2*k,k)*comb(N-2*k,n-k) for k in range(n+1)))
    ch=[sum(1 for k in range(1,N) if S[k]==0 and S[k-1]*S[k+1]<0) for S in P]
    chk("18б",all(F(ch.count(r),4**n)==F(2*comb(N-1,n-1-r),2**(N-1)) for r in range(n)))
    chk("18в",F(ch.count(0),4**n)==2*F(comb(N,n),4**n))
# 12а: 2n=6 — кучки 5,9,5,1
P=[ps(s) for s in product((1,-1),repeat=6)]
nonneg=[S[-1] for S in P if min(S)>=0]; depth=[-min(S) for S in P if S[-1]==0]
chk("12а",[nonneg.count(h) for h in (0,2,4,6)]==[depth.count(d) for d in (0,1,2,3)]==[5,9,5,1])
# 15
fib=[1,1]
for _ in range(30): fib.append(fib[-1]+fib[-2])
cnt=sum(all(0<=v<=3 for v in ps(s)) for s in product((1,-1),repeat=10))
chk("15а",F(cnt,1024)==F(89,1024))
# 16в
u=lambda j: F(comb(2*j,j),4**j); p=[u(k)*u(50-k) for k in range(51)]
a=float(sum(p[:6])); b=float(sum(p[45:])); c=float(sum(p[23:28]))
chk("16в",abs(a-0.2192)<1e-3 and abs(b-a)<1e-12 and abs(c-0.0631)<1e-3)
print("16в: первые 10 — %.3f, последние 10 — %.3f, 46–55 — %.3f"%(a,b,c))
print("ALL OK" if ok else "SOME FAIL")
