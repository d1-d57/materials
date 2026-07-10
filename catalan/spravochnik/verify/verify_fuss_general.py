from math import comb, factorial
from fractions import Fraction as Fr
from itertools import product
from collections import Counter

def catalan(m): return comb(2*m,m)//(m+1)

# ---- 1) general plane-tree count by degree profile = (1/n) * multinomial(n; n_0,n_1,...) ----
def valid_tree_seqs(n):
    # sequences (c_1..c_n), c_i>=0, partial sums of (c_i-1) >=0 for k<n, = -1 at n
    out=[]
    for seq in product(range(n), repeat=n):
        s=0; ok=True
        for k,c in enumerate(seq):
            s+=c-1
            if k<n-1 and s<0: ok=False; break
        if ok and s==-1: out.append(seq)
    return out

print("=== 1) general profile formula: #trees(profile) == (1/n)*multinomial ===")
for n in range(1,8):
    seqs=valid_tree_seqs(n)
    by_profile=Counter(tuple(sorted(s)) for s in seqs)
    allok=True
    for prof,cnt in by_profile.items():
        # profile -> n_j counts
        cc=Counter(prof)
        multi=factorial(n)
        for j,nj in cc.items(): multi//=factorial(nj)
        pred=Fr(multi,n)
        if pred!=cnt: allok=False; print("   MISMATCH",n,prof,cnt,pred)
    total=len(seqs)
    print(f"  n={n}: #plane trees={total} (=C_(n-1)={catalan(n-1)} : {total==catalan(n-1)}); profile formula exact: {allok}")

# ---- 2) d-ary Otter-Dwass closed form vs recursion ----
def total_progeny_dist(off, N):
    F=[Fr(0)]*(N+1)
    for _ in range(N+2):
        maxk=max(off); powF=[[Fr(0)]*(N+1) for _ in range(maxk+1)]; powF[0][0]=Fr(1)
        for k in range(1,maxk+1):
            for i in range(N+1):
                powF[k][i]=sum(powF[k-1][j]*F[i-j] for j in range(i+1))
        fF=[Fr(0)]*(N+1)
        for k,p in off.items():
            for i in range(N+1): fF[i]+=Fr(p)*powF[k][i]
        Fnew=[Fr(0)]*(N+1)
        for i in range(1,N+1): Fnew[i]=fF[i-1]
        if Fnew==F: break
        F=Fnew
    return F

print()
print("=== 2) d-ary: P(T=dm+1) = 1/(dm+1) C(dm+1,m) p^m (1-p)^((d-1)m+1) ===")
for d,p in [(2,Fr(1,2)),(3,Fr(1,3)),(3,Fr(1,4)),(4,Fr(1,5))]:
    off={0:1-p, d:p}
    N=4*d+1
    F=total_progeny_dist(off,N)
    ok=True
    for m in range(0, (N-1)//d +1):
        n=d*m+1
        fuss=Fr(comb(d*m+1,m),d*m+1)
        pred=fuss*(p**m)*((1-p)**((d-1)*m+1))
        if F[n]!=pred: ok=False; print("   MISMATCH",d,m,F[n],pred)
    print(f"  d={d}, p={p}: closed form == recursion for all m: {ok}")

# ---- 3) Fuss-Catalan values, two forms agree, Lando ternary ----
print()
print("=== 3) Fuss-Catalan C_m^(d) = 1/(dm+1)C(dm+1,m) = 1/((d-1)m+1)C(dm,m) ===")
for d in [2,3,4]:
    vals=[]; formok=True
    for m in range(0,6):
        a=comb(d*m+1,m)//(d*m+1)
        b=comb(d*m,m)//((d-1)*m+1)
        if a!=b: formok=False
        vals.append(a)
    print(f"  d={d}: {vals}  two-forms-agree={formok}")
# Lando ternary t_n = 1/(2n+1) C(3n,n)
lando=[comb(3*n,n)//(2*n+1) for n in range(6)]
print("  Lando §8.3 ternary (1/(2n+1))C(3n,n):", lando, " == FussCatalan d=3:", lando==[comb(3*m+1,m)//(3*m+1) for m in range(6)])
