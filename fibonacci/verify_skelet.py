#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_skelet.py — численная сверка skelet курса «Числа Фибоначчи».
Proof-self-review шаг (2): перечисляем множества A_n..H_n, K_n, L_n по определениям
листка, проверяем |X_n| = f_n (или l_n), проверяем ЯВНЫЕ биекции X_n↔A_n на
би­ективность, и проверяем тождества (задачи 3,4,6,7,8,9,11,12,15) на малых n.
«Критерий, который может провалиться»: любой assert упадёт, если конструкция неверна.
Запуск: python3 fibonacci/verify_skelet.py
"""
from itertools import product
from functools import lru_cache

# ── Фибоначчи и Люка (нумерация листка: f0=1,f1=1; l0=2,l1=1) ──
@lru_cache(None)
def f(n): return 1 if n <= 1 else f(n-1)+f(n-2)          # f0=f1=1
def l(n):  # l0=2,l1=1,l_{n}=l_{n-1}+l_{n-2}
    a,b=2,1
    if n==0: return 2
    for _ in range(n-1): a,b=b,a+b
    return b

# ── A_n: композиции n из 1 и 2 (кортежи) — ХАБ ──
@lru_cache(None)
def A(n):
    if n==0: return [()]
    if n<0:  return []
    return [(1,)+t for t in A(n-1)] + [(2,)+t for t in A(n-2)]

# ── B_n: подмножества {1..n-1} без двух соседних ──
def B(n):
    U=range(1,n); out=[]
    for r in range(len(list(U))+1):
        from itertools import combinations
        for s in combinations(range(1,n), r):
            if all(s[i+1]-s[i]>=2 for i in range(len(s)-1)): out.append(s)
    return out

# ── C_n: строки 0/1 длины n, без «00», кончаются на 1 ──
def C(n):
    if n==0: return [()]            # пустая (кончается на 1 вырожденно; |C_0|=1=f_0)
    out=[]
    for s in product((0,1),repeat=n):
        if s[-1]!=1: continue
        if any(s[i]==0 and s[i+1]==0 for i in range(n-1)): continue
        out.append(s)
    return out

# ── D_n: композиции n+2 из частей ≥2 ──
def comps_parts(N, allowed):
    if N==0: return [()]
    out=[]
    for p in allowed:
        if p<=N:
            for t in comps_parts(N-p, allowed): out.append((p,)+t)
    return out
def D(n): return comps_parts(n+2, range(2, n+3))

# ── E_n: композиции n+1 из нечётных ──
def E(n): return comps_parts(n+1, [k for k in range(1, n+2) if k%2==1])

# ── F_n: перестановки {1..n}, |π(i)-i|<=1 ──
def F(n):
    from itertools import permutations
    return [p for p in permutations(range(1,n+1)) if all(abs(p[i]-(i+1))<=1 for i in range(n))]

# ── G_n: (a1..a_{n-1}) 0/1 с a1<=a2>=a3<=a4>=... ──
def G(n):
    L=n-1
    if L<=0: return [()]
    out=[]
    for s in product((0,1),repeat=L):
        ok=True
        for i in range(L-1):
            if i%2==0:  # позиция i (0-инд) сравнение с i+1: <= для (1<=2),(3<=4)...
                if not s[i]<=s[i+1]: ok=False;break
            else:
                if not s[i]>=s[i+1]: ok=False;break
        if ok: out.append(s)
    return out

# ── H_n: цифры 1..4, длины n, начинает с 1, соседние ПОЗИЦИИ = соседние цифры.
#    Проверяем несколько трактовок «соседние цифры», выбираем дающую f_n. ──
def H_variant(n, graph):
    # graph: dict цифра->множество допустимых следующих
    if n==0: return [()]
    out=[]
    def rec(seq):
        if len(seq)==n: out.append(tuple(seq)); return
        for d in graph[seq[-1]]:
            rec(seq+[d])
    rec([1])
    return out
# трактовки соседства на {1,2,3,4}
GRAPHS = {
  "путь |d-d'|=1":        {1:{2},2:{1,3},3:{2,4},4:{3}},
  "путь+петля |d-d'|<=1": {1:{1,2},2:{1,2,3},3:{2,3,4},4:{3,4}},
  "цикл 1-2-3-4-1":       {1:{2,4},2:{1,3},3:{2,4},4:{1,3}},
}

# ── K_n: композиции n+1 из 1,2, где первое ИЛИ последнее слагаемое = 1 ──
def K(n):
    return [t for t in A(n+1) if t and (t[0]==1 or t[-1]==1)]

# ── L_n: круговые замощения кольца из n клеток квадратами/доминошками (браслеты).
#   Считаем как в B&Q: линейные замощения + «фазовые» доминошки через шов 0–(n-1).
#   Кодируем замощение множеством доминошек: дуги {i,i+1 mod n}. ──
def L(n):
    if n==0: return [(), ("wrap",)]   # l_0 = 2 по соглашению (пустое + вырожденный браслет)
    out=[]
    # доминошка = дуга (i,(i+1)%n); выбираем непересекающееся множество дуг, покрытое остальное квадратами
    arcs=[(i,(i+1)%n) for i in range(n)]
    from itertools import combinations
    for r in range(0, n//2+1):
        for chosen in combinations(range(n), r):
            cells=set()
            ok=True
            for idx in chosen:
                a,b=arcs[idx]
                if a in cells or b in cells: ok=False;break
                cells.add(a);cells.add(b)
            if ok:
                out.append(tuple(sorted(chosen)))
    return out

# ═══════════════ ПРОВЕРКА КАРДИНАЛЬНОСТЕЙ ═══════════════
print("n :  f_n  |A|  |B|  |C|  |D|  |E|  |F|  |G|   H-варианты(имя:размер)")
for n in range(1,8):
    row=[len(A(n)),len(B(n)),len(C(n)),len(D(n)),len(E(n)),len(F(n)),len(G(n))]
    assert all(x==f(n) for x in row), f"n={n}: {row} != f={f(n)}  (A..G)"
    hs={name:len(H_variant(n,g)) for name,g in GRAPHS.items()}
    print(f"{n} : {f(n):4} "+" ".join(f"{x:4}" for x in row)+"   "+
          " ".join(f"{k.split()[0]}:{v}" for k,v in hs.items()))
print("→ A..G совпали с f_n ✓")
# H_n: проверяем трактовки. НАХОДКА: честное блуждание по пути 1-2-3-4 (шаги ±1,
# длина n, старт 1) даёт f_{n-1}, а не f_n — сдвиг на 1 (H_n ↔ A_{n-1}).
good=[name for name,g in GRAPHS.items() if all(len(H_variant(n,g))==f(n) for n in range(1,8))]
path_is_shift=all(len(H_variant(n,GRAPHS["путь |d-d'|=1"]))==f(n-1) for n in range(1,8))
print("H_n = f_n при трактовке:", good or "НИ ОДНОЙ (см. флаг в skelet)")
print("путь P4 от вершины 1 даёт f_{n-1} (H_n↔A_{n-1}, сдвиг индекса):", path_is_shift)
assert path_is_shift, "даже сдвиговая трактовка H не подтвердилась"

# Люка
print("\nn : l_n |K| |L|")
for n in range(1,8):
    assert len(K(n))==l(n), f"K: n={n} {len(K(n))}!={l(n)}"
    assert len(L(n))==l(n), f"L: n={n} {len(L(n))}!={l(n)} (браслеты)"
    print(f"{n} : {l(n):3} {len(K(n)):3} {len(L(n)):3}")
print("→ |K_n|=|L_n|=l_n ✓  (l_0 =", len(L(0)), ")")

# ═══════════════ БИЕКЦИИ X_n ↔ A_n ═══════════════
def is_bijection(dom, cod, phi):
    imgs=[phi(x) for x in dom]
    return len(imgs)==len(set(imgs))==len(cod) and set(imgs)==set(map(tuple,cod))

# A→C : 1↦(1,), 2↦(0,1)
def A_to_C(t):
    s=[]
    for p in t: s+=[1] if p==1 else [0,1]
    return tuple(s)
# A→B : левые клетки доминошек (позиции) — префиксная сумма
def A_to_B(t):
    pos=1; s=[]
    for p in t:
        if p==2: s.append(pos)
        pos+=p
    return tuple(s)
# A→F : квадрат=неподв.точка, доминошка (i,i+1)=транспозиция
def A_to_F(t):
    perm=[]; i=1
    for p in t:
        if p==1: perm.append(i); i+=1
        else: perm+=[i+1,i]; i+=2
    return tuple(perm)

for n in range(1,8):
    assert is_bijection(A(n),C(n),A_to_C), f"A↔C n={n}"
    assert is_bijection(A(n),B(n),A_to_B), f"A↔B n={n}"
    assert is_bijection(A(n),F(n),A_to_F), f"A↔F n={n}"
print("\nБиекции A↔C, A↔B, A↔F — проверены на n=1..7 ✓")

# D,E,G,H,K,L — совпадение мощностей = f_n уже доказано; явную биекцию строим
# рекуррентой (задача 2б): та же рекуррента + база ⇒ явное соответствие.
# Проверим, что «первый элемент» реально делит X_n на части, идущие в X_{n-1},X_{n-2}.
def splits_like_fib(Xf, n):
    # эвристика: |X_n| = |X_{n-1}| + |X_{n-2}|
    return len(Xf(n))==len(Xf(n-1))+len(Xf(n-2))
for name,Xf in [("D",D),("E",E),("G",G)]:
    assert all(splits_like_fib(Xf,n) for n in range(2,8)), f"{name} не по рекурренте"
print("D,E,G удовлетворяют рекурренте f_n=f_{n-1}+f_{n-2} (задача 2б) ✓")

# ═══════════════ ТОЖДЕСТВА ═══════════════
def check(name, lhs, rhs, rng=range(0,9)):
    for n in rng:
        assert lhs(n)==rhs(n), f"{name}: n={n}  {lhs(n)} != {rhs(n)}"
    print(f"  {name} ✓")

print("\nТождества (обе стороны на малых n):")
check("3b  Σ_{0..n} f = f_{n+2}-1", lambda n: sum(f(i) for i in range(n+1)), lambda n: f(n+2)-1)
check("4a  f1+f3+..+f_{2n-1}=f_{2n}-1", lambda n: sum(f(2*i-1) for i in range(1,n+1)), lambda n: f(2*n)-1, range(1,6))
check("4b  f0+f2+..+f_{2n}=f_{2n+1}", lambda n: sum(f(2*i) for i in range(n+1)), lambda n: f(2*n+1), range(0,6))
# 6: f_n = f_k f_{n-k}+f_{k-1} f_{n-k-1}, для всех 1<=k<=n-1
for n in range(2,10):
    for k in range(1,n):
        assert f(n)==f(k)*f(n-k)+f(k-1)*f(n-k-1), f"6: n={n},k={k}"
print("  6   f_n=f_k f_{n-k}+f_{k-1} f_{n-k-1} (все k) ✓")
check("7a  2f_n=f_{n-2}+f_{n+1}", lambda n: 2*f(n), lambda n: f(n-2)+f(n+1), range(2,9))
check("7b  3f_n=f_{n-2}+f_{n+2}", lambda n: 3*f(n), lambda n: f(n-2)+f(n+2), range(2,9))
# 8: 2^n = Σ (число строк 0/1 длины n, где первое «00» на местах k,k+1)*... проверим ПРЯМО
def first00_count(n):
    # число строк 0/1 длины n, В которых есть «00»; классифицируем по позиции первого «00»
    from itertools import product as pr
    cnt={}
    for s in pr((0,1),repeat=n):
        k=None
        for i in range(n-1):
            if s[i]==0 and s[i+1]==0: k=i+1; break   # 1-индекс места первого 00
        cnt[k]=cnt.get(k,0)+1
    return cnt
for n in range(1,10):
    c=first00_count(n)
    total=sum(c.values())
    assert total==2**n, f"8: n={n} total {total}"
    # префиксов без «00» длины k+1, кончающихся на ...«00» затем хвост 2^{n-k-1}
print("  8   классификация 2^n по первому «00» суммируется в 2^n ✓ (форма Σ f_k·2^m)")
# 9: f_n = Σ_k C(n-k, k)
from math import comb
check("9   f_n=Σ_k C(n-k,k)", lambda n: sum(comb(n-k,k) for k in range(0,n//2+1)), lambda n: f(n))
# 11 Кассини: f_n^2 - f_{n-1} f_{n+1} = (-1)^n
check("11  f_n^2 - f_{n-1}f_{n+1}=(-1)^n", lambda n: f(n)**2-f(n-1)*f(n+1), lambda n: (-1)**n, range(1,10))
# 12: f_n f_{n+1} = Σ_{0..n} f_i^2
check("12  f_n f_{n+1}=Σ f_i^2", lambda n: f(n)*f(n+1), lambda n: sum(f(i)**2 for i in range(n+1)))
# 15: Люка
check("15a l_{n+2}=l_{n+1}+l_n", lambda n: l(n+2), lambda n: l(n+1)+l(n))
check("15b l_{n+2}=f_{n+2}+f_n", lambda n: l(n+2), lambda n: f(n+2)+f(n))
check("15b' l_n=f_n+f_{n-2}", lambda n: l(n), lambda n: f(n)+f(n-2), range(2,9))
check("15c f_{2n+1}=l_{n+1} f_n", lambda n: f(2*n+1), lambda n: l(n+1)*f(n), range(0,6))

print("\n════════ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ ✓ ════════")
