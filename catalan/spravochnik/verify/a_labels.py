# -*- coding: utf-8 -*-
# Конструкция владельца (A+метки): помеченный путь Дика -> ПЛАНАРНОЕ дерево стандартным обходом,
# метки подъёмов переносятся на создаваемые вершины. Забываем порядок -> помеч. дерево на {0..n}.
# Вопрос: это биекция? Совпадает ли с правилом "по столбцам" (B)?
import itertools, collections

def is_parking(f):
    s=sorted(f); return all(s[i]<=i+1 for i in range(len(f)))

def labeled_path(f):
    # метки подъёмов в порядке пути = столбцы 1..n, внутри столбца по возрастанию (стандартный помеч. путь)
    n=len(f); cols={c:sorted(i+1 for i in range(n) if f[i]==c) for c in range(1,n+1)}
    labels=[]; seq=[]
    for c in range(1,n+1):
        labels += cols[c]
        seq += [1]*len(cols[c]) + [-1]
    return labels, seq

def pf_to_tree_A(f):
    labels,seq=labeled_path(f)
    cur=0; st=[]; ui=0; edges=set()
    for s in seq:
        if s==1:
            ch=labels[ui]; ui+=1
            edges.add(frozenset((cur,ch))); st.append(cur); cur=ch
        else:
            cur=st.pop()
    return frozenset(edges)

def pf_to_tree_B(f):
    n=len(f); cols={c:sorted(i+1 for i in range(n) if f[i]==c) for c in range(1,n+1)}
    a=[0]
    for c in range(1,n+1): a.extend(cols[c])
    edges=set()
    for c in range(1,n+1):
        for ch in cols[c]: edges.add(frozenset((a[c-1],ch)))
    return frozenset(edges)

def is_tree(edges,n):
    verts=set(range(n+1))
    if len(edges)!=n: return False
    par={v:v for v in verts}
    def find(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    for e in edges:
        u,v=tuple(e); ru,rv=find(u),find(v)
        if ru==rv: return False
        par[ru]=rv
    return len({find(v) for v in verts})==1

for n in [2,3,4,5]:
    pfs=[f for f in itertools.product(range(1,n+1),repeat=n) if is_parking(f)]
    imgs=collections.Counter(); allvalid=True; sameB=0
    for f in pfs:
        eA=pf_to_tree_A(f)
        if not is_tree(eA,n): allvalid=False
        imgs[eA]+=1
        if eA==pf_to_tree_B(f): sameB+=1
    exp=(n+1)**(n-1)
    bij = (len(imgs)==len(pfs)==exp) and allvalid
    print(f"n={n}: парковок {len(pfs)}(ожид {exp}) | различных образов A+метки {len(imgs)} | все деревья {allvalid} "
          f"| A+метки — БИЕКЦИЯ? {bij} | A совпало с B: {sameB}/{len(pfs)}")
    if not bij:
        # покажем коллизию (две парковки -> одно дерево) и/или неохваченное дерево
        col=[e for e,cnt in imgs.items() if cnt>1]
        if col:
            e=col[0]; ff=[g for g in pfs if pf_to_tree_A(g)==e]
            print("   коллизия: парковки", ff[:4], "-> одно дерево", sorted(tuple(sorted(x)) for x in e))

f=(6,2,1,2,1,1,6)
print("\nпостер f=",f)
print("  A+метки:  ", sorted(tuple(sorted(e)) for e in pf_to_tree_A(f)))
print("  B столбцы:", sorted(tuple(sorted(e)) for e in pf_to_tree_B(f)))
print("  совпадают:", pf_to_tree_A(f)==pf_to_tree_B(f))
