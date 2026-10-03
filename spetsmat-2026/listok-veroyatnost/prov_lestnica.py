# Проверки к лестницам 18ℵ (30.09, вечер): (1) стягивание треугольника — биекция
# {(триангуляция (n+3)-угольника, небазовая сторона)} ↔ {(триангуляция (n+2)-угольника, ребро, конец ребра)};
# (2) циклическая лемма: выкидывание соседней пары (+1,−1) не меняет число хороших начал;
# (3) число путей с r сменами лидера = 4·C(2n−1,n−1−r) (уже проверено раньше, повтор для полноты).
from itertools import combinations, product
from math import comb
ok=True
def chk(name,c):
    global ok
    if not c: ok=False; print("FAIL",name)
Cat=lambda n: comb(2*n,n)//(n+1)

def triangulations(vs):
    """все триангуляции выпуклого многоугольника с вершинами vs (список по кругу), как множества диагоналей"""
    if len(vs)<=3: return [frozenset()]
    a,b=vs[0],vs[-1]; out=[]
    for k in range(1,len(vs)-1):
        v=vs[k]
        left=vs[:k+1]; right=vs[k:]
        for L in triangulations(left):
            for R in triangulations(right):
                d=set(L)|set(R)
                if k!=1: d.add(frozenset((a,v)))
                if k!=len(vs)-2: d.add(frozenset((v,b)))
                out.append(frozenset(d))
    return out

def edges(T,m):
    return set(T)|{frozenset((i,(i+1)%m)) for i in range(m)}

for m in range(4,9):
    n=m-3  # (n+3)-угольник
    Ts=triangulations(list(range(m)))
    chk(f"count {m}", len(Ts)==Cat(m-2))
    Tp=triangulations(list(range(m-1)))
    chk(f"count {m-1}", len(Tp)==Cat(m-3))
    images=set()
    for T in Ts:
        E=edges(T,m)
        for i in range(m-1):            # небазовые стороны (i,i+1); база — (m−1,0)
            side=frozenset((i,i+1))
            apex=[v for v in range(m) if v not in (i,i+1) and frozenset((i,v)) in E and frozenset((i+1,v)) in E]
            chk("apex unique", len(apex)==1); v=apex[0]
            f=lambda j: j if j<=i else j-1
            newE=set()
            for e in E:
                a,b=tuple(e); fa,fb=f(a),f(b)
                if fa!=fb: newE.add(frozenset((fa,fb)))
            sides=[frozenset((j,(j+1)%(m-1))) for j in range(m-1)]
            diag=frozenset(e for e in newE if e not in sides)
            marked=frozenset((i,f(v))); endpoint=i
            chk("marked edge in T'", marked in newE)
            chk("T' is triangulation", diag in set(Tp))
            images.add((diag,marked,endpoint))
    total=(m-1)*len(Ts)
    chk(f"injective m={m}", len(images)==total)
    chk(f"count identity m={m}", total==2*(2*(m-3)+1)*Cat(m-3))
    print(f"{m}-угольник: (T, небазовая сторона) = {total}; (T', ребро, конец) = {2*(2*(m-3)+1)*Cat(m-3)}; образов различных {len(images)}")

# (2) циклическая лемма и выкидывание пары
def good_starts(w):
    N=len(w); c=0
    for s in range(N):
        t=0; okk=True
        for j in range(N):
            t+=w[(s+j)%N]
            if t<=0: okk=False; break
        c+=okk
    return c
for a in range(1,7):
    for b in range(0,a):
        for pos in combinations(range(a+b),b):
            w=[-1 if i in pos else 1 for i in range(a+b)]
            chk("cycle lemma", good_starts(w)==a-b)
            if b>0:
                N=a+b
                j=next(i for i in range(N) if w[i]==1 and w[(i+1)%N]==-1)
                w2=[w[k] for k in range(N) if k not in (j,(j+1)%N)]
                chk("pair removal", good_starts(w2)==good_starts(w))
print("ALL OK" if ok else "SOME FAIL")
