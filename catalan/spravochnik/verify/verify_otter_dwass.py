from fractions import Fraction as Fr
from math import comb

# ---- offspring pgf given as dict {k: prob} ; probs sum to 1 ----
def total_progeny_dist(off, N):
    """P(T=n) for n=1..N via F(x)=x*f(F(x)), coefficients by iteration."""
    # f(z) = sum off[k] z^k. Compute F coeffs f_1..f_N with F=x f(F).
    # iterate power series to order N
    F=[Fr(0)]*(N+1)  # F[n]=[x^n]F
    for _ in range(N+2):
        # compute f(F) as power series in x up to order N, then F_new = x*f(F)
        # f(F)=sum_k off[k]*F^k
        fF=[Fr(0)]*(N+1); fF[0]=Fr(0)
        # need powers of F up to max degree in off
        maxk=max(off)
        # F^0=1
        powF=[[Fr(0)]*(N+1) for _ in range(maxk+1)]
        powF[0][0]=Fr(1)
        for k in range(1,maxk+1):
            # powF[k]=powF[k-1]*F
            for i in range(N+1):
                s=Fr(0)
                for j in range(i+1):
                    s+=powF[k-1][j]*F[i-j]
                powF[k][i]=s
        for k,p in off.items():
            pk=Fr(p)
            for i in range(N+1):
                fF[i]+=pk*powF[k][i]
        Fnew=[Fr(0)]*(N+1)
        for i in range(1,N+1):
            Fnew[i]=fF[i-1]   # x*f(F)
        if Fnew==F: break
        F=Fnew
    return F  # F[n]=P(T=n)

def otter_dwass(off, N):
    """(1/n)*P(S_n=-1) = (1/n)[z^{n-1}] f(z)^n, f(z)=sum off[k] z^k."""
    maxk=max(off)
    res=[Fr(0)]*(N+1)
    for n in range(1,N+1):
        # coefficient of z^{n-1} in f(z)^n
        # f(z)^n as poly up to degree n-1
        target=n-1
        poly=[Fr(0)]*(target+1); poly[0]=Fr(1)
        for _ in range(n):
            new=[Fr(0)]*(target+1)
            for i in range(target+1):
                if poly[i]==0: continue
                for k,p in off.items():
                    if i+k<=target:
                        new[i+k]+=poly[i]*Fr(p)
            poly=new
        res[n]=poly[target]/n
    return res

def catalan(m): return comb(2*m,m)//(m+1)

N=9
print("=== Test 1: Otter-Dwass = total-progeny law, several offspring ===")
cases={
 "geometric(1/2) P(k)=1/2^{k+1}": {k:Fr(1,2**(k+1)) for k in range(0,40)},
 "binary {0,2} each 1/2":        {0:Fr(1,2),2:Fr(1,2)},
 "Binomial(2,1/2) {0,1,2}":      {0:Fr(1,4),1:Fr(1,2),2:Fr(1,4)},
 "Poisson-ish {0:.4,1:.2,3:.4}": {0:Fr(2,5),1:Fr(1,5),3:Fr(2,5)},
}
for name,off in cases.items():
    s=sum(off.values())
    assert s==1 or (1-s)<Fr(1,10**9), (name,s)
    F=total_progeny_dist(off,N)
    OD=otter_dwass(off,N)
    ok=all(F[n]==OD[n] for n in range(1,N+1))
    print(f"  {name:32s}: Otter-Dwass==recursion? {ok}")

print()
print("=== Test 2: geometric(1/2) -> uniform plane tree, Catalan count ===")
off={k:Fr(1,2**(k+1)) for k in range(0,40)}
F=total_progeny_dist(off,N)
for n in range(1,N+1):
    # plane trees with n vertices = C_{n-1}; each has prob (1/2)^{2n-1}
    predicted=Fr(catalan(n-1), 2**(2*n-1))
    print(f"  n={n}: P(T=n)={F[n]}  C_(n-1)/2^(2n-1)={predicted}  match={F[n]==predicted}  (C_{n-1}={catalan(n-1)})")

print()
print("=== Test 3: binary {0,2} -> full binary trees, Catalan, Dyck (T odd=2m+1) ===")
off={0:Fr(1,2),2:Fr(1,2)}
F=total_progeny_dist(off,N)
for n in range(1,N+1):
    if n%2==1:
        m=(n-1)//2
        predicted=Fr(catalan(m),2**(2*m+1))  # full binary trees w/ m internal = C_m, prob (1/2)^{2m+1}
        print(f"  n={n} (m={m}): P(T=n)={F[n]}  C_m/2^(2m+1)={predicted}  match={F[n]==predicted}  C_{m}={catalan(m)}")
    else:
        print(f"  n={n}: P(T=n)={F[n]}  (even -> 0 expected: {F[n]==0})")

print()
print("=== Test 4: Lagrange-inversion identity underlying Otter-Dwass ===")
print("  [x^n]F where F=x f(F)  ==  (1/n)[z^{n-1}] f(z)^n  is exactly Lagrange-Burmann.")
print("  Already confirmed by Test 1 across all offspring above.")
