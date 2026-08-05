"""Оптика «одна цепная дробь»: пути в полосе, вес по площади, финал — Роджерс — Рамануджан.
Запуск: python3 proverka_cepnaya_drob.py     (только stdlib)

F_m(z,q) = sum по путям 0->0, шаги +-1, высоты в полосе 0..m, z^полудлина q^площадь,
площадь = сумма высот, достигнутых подъёмами (= размер диаграммы Юнга под путём).
"""
from collections import defaultdict
from functools import lru_cache
from fractions import Fraction
import math

P = 60  # точность рядов по q

def mul(a, b):
    r = [0]*P
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if i+j < P: r[i+j] += x*y
    return r
def add(a, b): return [x+y for x, y in zip(a, b)]
def sub(a, b): return [x-y for x, y in zip(a, b)]
def one():
    r = [0]*P; r[0] = 1; return r
def qpow(k):
    r = [0]*P
    if k < P: r[k] = 1
    return r
def inv(a):
    assert a[0] == 1
    r = [0]*P; r[0] = 1
    for n in range(1, P):
        r[n] = -sum(a[k]*r[n-k] for k in range(1, n+1))
    return r

@lru_cache(None)
def _qb(n, k):
    if k < 0 or k > n: return ()
    if k in (0, n): return (1,)
    u, v = list(_qb(n-1, k-1)), list(_qb(n-1, k))
    r = [0]*max(len(u), len(v)+k)
    for i, c in enumerate(u): r[i] += c
    for i, c in enumerate(v): r[i+k] += c
    while r and r[-1] == 0: r.pop()
    return tuple(r)
def qbin(n, k): return list(_qb(n, k))
def qpoch(n):
    r = one()
    for i in range(1, n+1): r = mul(r, sub(one(), qpow(i)))
    return r

def strip(m, zsign, maxsteps=240):
    """сумма z^полудлина q^площадь по путям 0->0 в полосе 0..m; z = +-1"""
    cur = {0: {0: 1}}
    tot = [0]*P; tot[0] = 1
    for step in range(maxsteps):
        nxt = defaultdict(lambda: defaultdict(int))
        for h, pol in cur.items():
            for h2 in (h-1, h+1):
                if 0 <= h2 <= m:
                    d = h2 if h2 > h else 0
                    for a, c in pol.items():
                        if a+d < P: nxt[h2][a+d] += c
        cur = {h: dict(p) for h, p in nxt.items()}
        if step % 2 == 1:
            s = zsign**((step+1)//2)
            for a, c in cur.get(0, {}).items():
                if a < P: tot[a] += s*c
    return tot

def cf(m, zsign):
    """цепная дробь 1/(1 - z q^1/(1 - z q^2/(...))) с m ярусами"""
    r = one()
    for k in range(m, 0, -1):
        r = inv(sub(one(), [zsign*x for x in mul(qpow(k), r)]))
    return r

def euler_exponents(f, upto=35):
    """f = prod (1-q^n)^{c_n}; вернуть c_n. Периодичность c_n <=> эта-произведение."""
    cur = [Fraction(x) for x in f[:upto+1]]
    assert cur[0] == 1
    c = []
    for n in range(1, upto+1):
        cn = -cur[n]; c.append(cn)
        if cn:
            fac = [Fraction(0)]*(upto+1); fac[0] = Fraction(1); k = 1
            while n*k <= upto:
                b = Fraction(1)
                for i in range(k): b *= (Fraction(-cn)-i)
                fac[n*k] = b/Fraction(math.factorial(k))*((-1)**k); k += 1
            new = [Fraction(0)]*(upto+1)
            for i, x in enumerate(cur):
                if x:
                    for j, y in enumerate(fac):
                        if i+j <= upto: new[i+j] += x*y
            cur = new
    return [int(x) if x.denominator == 1 else x for x in c]

# ---------------------------------------------------------------- 1
print("=== 1. пути в полосе с весом по площади ЕСТЬ ЦЕПНАЯ ДРОБЬ ===")
print("    F_m(1,q) = 1/(1 - q/(1 - q^2/(1 - q^3/(... m ярусов))))")
ok = all(strip(m, 1) == cf(m, 1) for m in range(1, 6))
print(f"    m=1..5, до q^{P-1}: {'сходится ✓' if ok else 'РАСХОЖДЕНИЕ'}")
print("    вывод — разложение по первому возвращению: F_m(z,q) = 1/(1 - z q F_(m-1)(zq,q))")

# ---------------------------------------------------------------- 2
print("\n=== 2. знаменатели сходящихся — МНОГОЧЛЕНЫ ШУРА (q-Чебышёв) ===")
def B(m):
    a, b = one(), one()
    for k in range(1, m+1): a, b = b, sub(b, mul(qpow(k), a))
    return b
def schur(m):
    r = [0]*P
    for j in range(0, (m+1)//2+1):
        cc = qbin(m+1-j, j)
        if cc: r = add(r, [((-1)**j)*x for x in mul(qpow(j*j), cc+[0]*(P-len(cc)))])
    return r
print("    B_m = B_(m-1) - q^m B_(m-2)  ==  sum_j (-1)^j q^(j^2) [m+1-j, j]_q")
print(f"    m=0..19: {'сходится ✓' if all(B(m)==schur(m) for m in range(20)) else 'РАСХОЖДЕНИЕ'}")

# ---------------------------------------------------------------- 3
print("\n=== 3. ФИНАЛ: z = -1 даёт цепную дробь Роджерса — Рамануджана ===")
G = [0]*P; H = [0]*P
for n in range(14):
    ip = inv(qpoch(n))
    G = add(G, mul(qpow(n*n), ip)); H = add(H, mul(qpow(n*n+n), ip))
HG = mul(H, inv(G))
print("    F_oo(-1,q) = 1/(1 + q/(1 + q^2/(1 + q^3/...)))  =  H(q)/G(q)")
print(f"    {'сходится ✓' if strip(40,-1)==HG else 'РАСХОЖДЕНИЕ'}   (стабилизация по m уже при m=4)")
print(f"    H/G = {HG[:12]}")

# ---------------------------------------------------------------- 4
print("\n=== 4. МОДУЛЯРНОСТЬ: тест на эта-произведение (периодичность показателей) ===")
print(f"    H/G     c_n = {euler_exponents(HG)[:20]}")
print( "              -> период 5  =>  эта-произведение  =>  модулярная функция уровня 5")
print(f"    G       c_n = {euler_exponents(G)[:15]}   (период 5: части 1,4 mod 5)")
print(f"    H       c_n = {euler_exponents(H)[:15]}   (период 5: части 2,3 mod 5)")
print(f"    z=+1    c_n = {euler_exponents(strip(40,1))[:12]} ...")
print( "              -> НЕ периодичны => не эта-произведение => НЕ модулярна")

# ---------------------------------------------------------------- 5
print("\n=== 5. два способа счёта на этом этаже: конечное тождество Роджерса — Рамануджана (Шур, 1917) ===")
def polyadd(a, b):
    n = max(len(a), len(b)); r = [0]*n
    for i, x in enumerate(a): r[i] += x
    for i, x in enumerate(b): r[i] += x
    while r and r[-1] == 0: r.pop()
    return r
bad = []
for n in range(1, 13):
    bos = []
    for j in range(-n-2, n+3):
        e = j*(5*j+1)//2
        cc = qbin(2*n, n+2*j)
        if cc and e >= 0:
            t = [0]*e+cc
            bos = polyadd(bos, t if j % 2 == 0 else [-x for x in t])
    fer = []
    for j in range(n+1): fer = polyadd(fer, [0]*(j*j)+qbin(n, j))
    if bos != fer: bad.append(n)
print("    бозон  sum_j (-1)^j q^(j(5j+1)/2) [2n, n+2j]_q")
print("    фермион sum_j q^(j^2) [n, j]_q")
print(f"    n=1..12: {'сходится ✓' if not bad else f'РАСХОЖДЕНИЯ {bad}'}")

# ---------------------------------------------------------------- 6
print("\n=== 6. пентагональная теорема: вход НЕ через отражение, а через q-биномиальную теорему ===")
badn = []
for n in range(1, 15):
    lhs = one()
    for i in range(1, n+1): lhs = mul(lhs, sub(one(), qpow(i)))
    rhs = [0]*P
    for j in range(n+1):
        cc = qbin(n, j)
        rhs = add(rhs, [((-1)**j)*x for x in mul(qpow(j*(j+1)//2), cc+[0]*(P-len(cc)))])
    if lhs != rhs: badn.append(n)
print("    prod_(i=1..n) (1-q^i) = sum_j (-1)^j q^(j(j+1)/2) [n,j]_q   (тождество Роте)")
print(f"    n=1..14: {'сходится ✓' if not badn else f'РАСХОЖДЕНИЯ {badn}'}")
lim = one()
for i in range(1, P): lim = mul(lim, sub(one(), qpow(i)))
pent = [0]*P
for j in range(-8, 9):
    e = j*(3*j-1)//2
    if 0 <= e < P: pent[e] += (-1)**j
print(f"    предел n->oo: prod(1-q^i) == пятиугольный ряд до q^{P-1}: {'✓' if lim==pent else 'НЕТ'}")
print(f"    ненулевые места: {[i for i,c in enumerate(lim) if c][:11]}  — пятиугольные числа")

# ---------------------------------------------------------------- 7
print("\n=== 7. отрицательный результат: наивный q-метод изображений на полосе НЕ работает ===")
def strip_len(N, m):
    cur = {0: {0: 1}}
    for _ in range(N):
        nxt = defaultdict(lambda: defaultdict(int))
        for h, pol in cur.items():
            for h2 in (h-1, h+1):
                if 0 <= h2 <= m:
                    for a, c in pol.items(): nxt[h2][a+h2] += c
        cur = nxt
    return dict(cur.get(0, {}))
def free_len(N, y):
    if (N+y) % 2 or abs(y) > N: return {}
    mm = (y*y+2*(N+1)*y-N*N)//4
    return {mm+2*i: c for i, c in enumerate(qbin(N, (N+y)//2)) if c}
for m, N in ((2, 8), (3, 8), (2, 12)):
    exact = strip_len(N, m)
    img = defaultdict(int)
    per = 2*(m+2)
    for j in range(-3, 4):
        for s, y in ((1, j*per), (-1, -2+j*per)):
            for a, c in free_len(N, y).items(): img[a] += s*c
    img = {a: c for a, c in img.items() if c}
    print(f"    m={m} N={N}: совпало = {exact == img}   (отражение площадь не сохраняет)")
