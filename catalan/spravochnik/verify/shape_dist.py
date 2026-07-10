# -*- coding: utf-8 -*-
# Вопрос: можно ли биекцию парковки<->помеч.деревья реализовать как "биекция путь<->дерево (форма) + метки"?
# Это возможно ТОГДА И ТОЛЬКО ТОГДА, когда для КАЖДОЙ формы:
#   (число парковок с данной формой пути) == (число помеч. деревьев с соответствующей формой дерева).
# Проверяем сильнее: равны ли МУЛЬТИМНОЖЕСТВА этих чисел (тогда пары форм с равными числами существуют),
# и реализует ли это стандартный обход A (или его сопряжённый A').
import itertools, collections, heapq, math

def is_parking(f):
    s=sorted(f); return all(s[i]<=i+1 for i in range(len(f)))

def dyck_shape(f):                 # (k_1,...,k_n): сколько машин любят место c
    n=len(f); return tuple(sum(1 for x in f if x==c) for c in range(1,n+1))

def canon_children(kids, root):    # AHU: канон неупорядоченной корневой формы
    def rec(u): return "("+"".join(sorted(rec(c) for c in kids.get(u,[])))+")"
    return rec(root)

def seq_from_shape(k):             # U^{k_1} D U^{k_2} D ...
    seq=[]
    for kc in k: seq += [1]*kc + [-1]
    return seq

def plane_tree(seq, mirror=False): # обход: U=спуск к новому ребёнку, D=подъём
    s = [(-x) for x in reversed(seq)] if mirror else seq
    kids=collections.defaultdict(list); cur=0; nxt=1; st=[]
    for x in s:
        if x==1: c=nxt; nxt+=1; kids[cur].append(c); st.append(cur); cur=c
        else: cur=st.pop()
    return canon_children(kids,0)

def prufer_trees(n):               # все помеч. деревья на {0..n}, канон формы (корень 0)
    verts=list(range(n+1))
    for seq in itertools.product(verts, repeat=n-1) if n>=2 else [()]:
        deg={v:1 for v in verts}
        for x in seq: deg[x]+=1
        h=[v for v in verts if deg[v]==1]; heapq.heapify(h)
        edges=[]
        for x in seq:
            u=heapq.heappop(h); edges.append((u,x)); deg[u]-=1; deg[x]-=1
            if deg[x]==1: heapq.heappush(h,x)
        a=heapq.heappop(h); b=heapq.heappop(h); edges.append((a,b))
        adj=collections.defaultdict(list)
        for u,v in edges: adj[u].append(v); adj[v].append(u)
        kids=collections.defaultdict(list); seen={0}; dq=collections.deque([0])
        while dq:
            u=dq.popleft()
            for w in adj[u]:
                if w not in seen: seen.add(w); kids[u].append(w); dq.append(w)
        yield canon_children(kids,0)

for n in range(2,6):
    pfs=[f for f in itertools.product(range(1,n+1),repeat=n) if is_parking(f)]
    # число парковок на форму пути:
    by_shape=collections.Counter(dyck_shape(f) for f in pfs)          # shape -> #parking
    park_counts=sorted(by_shape.values())
    # число помеч. деревьев на форму дерева:
    tree_shape_count=collections.Counter(prufer_trees(n))             # treeShape -> #labeled
    tree_counts=sorted(tree_shape_count.values())
    # реализует ли обход A / A' shape-сохранение p(D)=t(shape)?:
    okA=all(by_shape[D]==tree_shape_count.get(plane_tree(seq_from_shape(D)),0) for D in by_shape)
    okAm=all(by_shape[D]==tree_shape_count.get(plane_tree(seq_from_shape(D),mirror=True),0) for D in by_shape)
    print(f"n={n}: парковок {len(pfs)} = деревьев {sum(tree_shape_count.values())} = (n+1)^(n-1)={ (n+1)**(n-1)}")
    print(f"   мультимн. чисел-по-форме: парковки {park_counts}")
    print(f"                              деревья  {tree_counts}")
    print(f"   МУЛЬТИМНОЖЕСТВА равны? {park_counts==tree_counts}  |  обход A даёт shape-сохранение? {okA}  |  сопряжённый A'? {okAm}")
