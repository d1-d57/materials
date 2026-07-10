# -*- coding: utf-8 -*-
# (A) стандартный обход пути -> плоское дерево (форма) vs (B) правило "по столбцам" (Теорема 5, помеченное).
import itertools, collections

def is_parking(f):
    s=sorted(f); return all(s[i]<=i+1 for i in range(len(f)))

def pf_to_tree_B(f):   # помеченное дерево по столбцам (Теорема 5)
    n=len(f); cols={c:sorted(i+1 for i in range(n) if f[i]==c) for c in range(1,n+1)}
    a=[0]
    for c in range(1,n+1): a.extend(cols[c])
    kids=collections.defaultdict(list)
    for c in range(1,n+1):
        for ch in cols[c]: kids[a[c-1]].append(ch)
    return kids

def path_seq(f):       # U/D последовательность пути Дика парковки: для c: U^{m_c} D
    n=len(f); seq=[]
    for c in range(1,n+1):
        seq += [1]*sum(1 for x in f if x==c) + [-1]
    return seq, n

def path_to_plane_tree_A(f):   # стандартный обход: U=спуск к новому ребёнку, D=подъём к родителю
    seq,n=path_seq(f)
    kids=collections.defaultdict(list); cur=0; nxt=1; stack=[]
    for s in seq:
        if s==1:
            child=nxt; nxt+=1; kids[cur].append(child); stack.append(cur); cur=child
        else:
            cur=stack.pop()
    return kids   # дерево-ФОРМА (вершины пронумерованы порядком обхода)

def canon(kids, root=0):   # AHU: канон НЕупорядоченной корневой формы
    def rec(u):
        return "("+"".join(sorted(rec(c) for c in kids.get(u,[])))+")"
    return rec(root)

# --- пример постера ---
f=(6,2,1,2,1,1,6)
B=pf_to_tree_B(f); A=path_to_plane_tree_A(f)
print("Пример постера f =",f)
print("  (B) по столбцам, дерево (родитель→дети):", dict(B))
print("      степень корня 0:", len(B[0]), "| форма:", canon(B))
print("  (A) обход пути,   дерево (родитель→дети):", dict(A))
print("      степень корня 0:", len(A[0]), "| форма:", canon(A))
print("  ФОРМЫ СОВПАДАЮТ?", canon(A)==canon(B))

# --- как часто формы (A) и (B) совпадают, по малым n ---
print("\nСовпадение форм (A)=(B) по всем парковкам:")
for n in range(1,7):
    pfs=[g for g in itertools.product(range(1,n+1),repeat=n) if is_parking(g)]
    eq=sum(1 for g in pfs if canon(path_to_plane_tree_A(g))==canon(pf_to_tree_B(g)))
    print(f"  n={n}: {eq} из {len(pfs)} парковок дают одинаковую форму дерева")
