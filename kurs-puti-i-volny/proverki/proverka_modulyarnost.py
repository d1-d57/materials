from math import comb, exp, pi, sqrt, log
from itertools import product

# --- 1. r_4(n) = 8 * (сумма делителей n, не кратных 4)   [Якоби; Загир, Prop.11] ---
def r_k(n, k, B=None):
    B = B or int(sqrt(n)) + 1
    cnt = 0
    def rec(k, rest):
        if k == 0: return 1 if rest == 0 else 0
        s = 0
        j = 0
        while j*j <= rest:
            s += (1 if j == 0 else 2) * rec(k-1, rest - j*j)
            j += 1
        return s
    return rec(k, n)

def sig_star4(n): return sum(d for d in range(1, n+1) if n % d == 0 and d % 4)
def sig(n, p=1): return sum(d**p for d in range(1, n+1) if n % d == 0)

print("=== r_4(n) = 8 * (сумма делителей n, не кратных 4) ===")
ok = all(r_k(n,4) == 8*sig_star4(n) for n in range(1, 31))
print("  n=1..30:", "сходится ✓" if ok else "РАСХОЖДЕНИЕ")
print("  примеры:", [(n, r_k(n,4), 8*sig_star4(n)) for n in (1,2,3,4,7,12)])

print("\n=== r_2(n) = 4 * сумма (-1)^((d-1)/2) по нечётным делителям ===")
def r2f(n): return 4*sum((-1)**((d-1)//2) for d in range(1, n+1, 2) if n % d == 0)
ok = all(r_k(n,2) == r2f(n) for n in range(1, 41))
print("  n=1..40:", "сходится ✓" if ok else "РАСХОЖДЕНИЕ")

# --- 2. решётка E8: число векторов нормы 2n равно 240*sigma_3(n) ---
print("\n=== E8: число векторов длины^2 = 2n равно 240*sigma_3(n) ===")
def e8_counts(maxnorm=8):
    # E8 = {целые или все полуцелые, сумма чётна}
    from itertools import product
    cnt = {}
    R = 3
    # целые координаты
    for v in product(range(-R, R+1), repeat=8):
        if sum(v) % 2: continue
        nn = sum(x*x for x in v)
        if 0 < nn <= maxnorm: cnt[nn] = cnt.get(nn,0)+1
    # полуцелые: x_i = a_i + 1/2, работаем в удвоенных координатах
    for v in product(range(-2*R-1, 2*R+2, 2), repeat=8):
        if sum(v) % 4: continue           # сумма координат чётна  <=> sum(v)/2 чётна
        nn4 = sum(x*x for x in v)
        if nn4 % 4: continue
        nn = nn4 // 4
        if 0 < nn <= maxnorm: cnt[nn] = cnt.get(nn,0)+1
    return cnt
c = e8_counts(6)
for n in (1,2,3):
    print(f"  норма {2*n}: векторов {c.get(2*n,0):>6}   240*sigma_3({n}) = {240*sig(n,3):>6}")

# --- 3. КОНЕЧНОМЕРНОСТЬ в действии: E4^2 = E8 как ряды ---
print("\n=== конечномерность: dim M_8 = 1  =>  E4^2 = E8 (проверка по коэффициентам) ===")
N = 15
def E(k, N):
    # E_k = 1 - (2k/B_k) sum sigma_{k-1}(n) q^n ; для k=4: 1+240 sum sigma_3 ; k=8: 1+480 sum sigma_7
    c = {4: 240, 6: -504, 8: 480, 10: -264, 12: 65520/691}
    return [1] + [c[k]*sig(n, k-1) for n in range(1, N)]
def mul(a, b, N):
    r = [0]*N
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if i+j < N: r[i+j] += x*y
    return r
lhs, rhs = mul(E(4,N), E(4,N), N), E(8,N)
print("  E4^2:", lhs[:6]); print("  E8  :", rhs[:6])
print("  совпали до q^%d:" % (N-1), all(abs(a-b) < 1e-6 for a, b in zip(lhs, rhs)))
print("  СМЫСЛ: проверив ОДИН коэффициент, доказали тождество для всех n.")
print("  В числах это: sum_{m=1}^{n-1} sigma_3(m) sigma_3(n-m) = (sigma_7(n) - sigma_3(n))/120")
ok = all(abs(sum(sig(m,3)*sig(n-m,3) for m in range(1,n)) - (sig(n,7)-sig(n,3))/120) < 1e-6
         for n in range(1, 25))
print("  n=1..24:", "сходится ✓" if ok else "РАСХОЖДЕНИЕ")

# --- 4. тэта-ряд решётки = след теплового ядра на торе R^k/Λ ---
print("\n=== тэта-ряд решётки Z^k = след теплового ядра на торе (вероятность возврата) ===")
def theta(t, J=60): return sum(exp(-pi*j*j*t) for j in range(-J, J+1))
def heat_trace_torus(k, t, J=40):
    # sum по решётке exp(-pi t |lambda|^2) = theta(t)^k
    return theta(t)**k
def walk_return_torus(k, t):
    # то же через спектр: сумма по двойственной решётке -- тождество Якоби покоординатно
    return theta(1/t)**k / t**(k/2)
for k in (1,2,4,8):
    for t in (0.3, 1.7):
        a,b = heat_trace_torus(k,t), walk_return_torus(k,t)
        print(f"  k={k}, t={t}: по решётке {a:.10f}   по спектру {b:.10f}   расх={abs(a-b):.1e}")

# --- 5. разбиения: откуда берётся pi^2/6 ---
print("\n=== разбиения: log prod 1/(1-q^k) ~ zeta(2)/(1-q) при q->1 ===")
for q in (0.9, 0.99, 0.999, 0.9999):
    L = -sum(log(1-q**k) for k in range(1, 200000))
    print(f"  q={q:<7} log(произв.)={L:>12.5f}   zeta(2)/(1-q)={pi*pi/6/(1-q):>12.5f}   отн.={L/(pi*pi/6/(1-q)):.5f}")
print("  ИМЕННО отсюда pi*sqrt(2n/3) в асимптотике p(n): sqrt(4*zeta(2)*...)")
def p(n):
    dp=[1]+[0]*n
    for k in range(1,n+1):
        for i in range(k,n+1): dp[i]+=dp[i-k]
    return dp[n]
print("\n=== p(n) ~ exp(pi sqrt(2n/3)) / (4n sqrt3) ===")
for n in (50,100,200,500):
    a=p(n); b=exp(pi*sqrt(2*n/3))/(4*n*sqrt(3))
    print(f"  n={n:>4}: p(n)={a:<24} асимптотика={b:<22.4g} отношение={b/a:.4f}")
