# Соответствие «стянуть сторону» между триангуляциями (n+3)- и (n+2)-угольника: степени без кратностей.
from math import comb
import sys
sys.setrecursionlimit(10000)
def triangulations(vs):
    if len(vs)<=3: return [frozenset()]
    a,b=vs[0],vs[-1]; out=[]
    for k in range(1,len(vs)-1):
        v=vs[k]
        for L in triangulations(vs[:k+1]):
            for R in triangulations(vs[k:]):
                d=set(L)|set(R)
                if k!=1: d.add(frozenset((a,v)))
                if k!=len(vs)-2: d.add(frozenset((v,b)))
                out.append(frozenset(d))
    return out
def edges(T,m): return set(T)|{frozenset((i,(i+1)%m)) for i in range(m)}
def contract(T,m,i):
    """стянуть сторону (i,i+1), i=0..m-2 (сторона (m-1,0) — основание не трогаем) → триангуляция (m-1)-угольника"""
    E=edges(T,m); f=lambda j: j if j<=i else j-1
    newE={frozenset((f(a),f(b))) for a,b in map(tuple,E) if f(a)!=f(b)}
    sides={frozenset((j,(j+1)%(m-1))) for j in range(m-1)}
    return frozenset(e for e in newE if e not in sides)
def contract_any(T,m,i):
    """то же, но разрешено стягивать любую сторону (i,i+1 mod m), включая основание; метки после стягивания — циклически с нуля"""
    E=edges(T,m); j=(i+1)%m
    # переименование: вершины по кругу начиная с j, слить i и j
    order=[(j+t)%m for t in range(m)]  # j, j+1, ..., i
    lab={v:t for t,v in enumerate(order)}; lab[i]=0
    newE={frozenset((lab[a],lab[b])) for a,b in map(tuple,E) if lab[a]!=lab[b]}
    sides={frozenset((t,(t+1)%(m-1))) for t in range(m-1)}
    return frozenset(e for e in newE if e not in sides)
for m in range(5,10):
    n=m-3
    A=triangulations(list(range(m))); B=triangulations(list(range(m-1)))
    rel={}
    for T in A:
        imgs={contract(T,m,i) for i in range(m-1)}
        rel[T]=imgs
    dA={len(v) for v in rel.values()}
    back={}
    for T,imgs in rel.items():
        for S in imgs: back.setdefault(S,set()).add(T)
    dB={len(v) for v in back.values()}
    print(f"{m}-угольник→{m-1}: степени слева {sorted(dA)}, справа {sorted(dB)}; (n+2)={n+2}, (4n+2)={4*n+2}")
