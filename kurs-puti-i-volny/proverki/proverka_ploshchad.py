"""Честный вход в модулярность через комбинаторику: вес по площади даёт тэта-ряд.
Запуск: python3 proverka_ploshchad.py"""
from collections import defaultdict

def q_puti(N, y):
    """{площадь: число путей} по всем путям длины N из 0 в y, шаги ±1, без стенок.
    Площадь = сумма высот после каждого шага."""
    cur = {0: {0: 1}}
    for _ in range(N):
        nxt = defaultdict(lambda: defaultdict(int))
        for h, pol in cur.items():
            for h2 in (h - 1, h + 1):
                for a, c in pol.items():
                    nxt[h2][a + h2] += c
        cur = nxt
    return dict(cur.get(y, {}))

def gauss_binom(n, k):
    """коэффициенты [n k]_q как целого многочлена"""
    T = {}
    def g(a, b):
        if b < 0 or b > a: return [0]
        if (a, b) in T: return T[(a, b)]
        if b in (0, a): r = [1]
        else:
            u, v = g(a - 1, b - 1), g(a - 1, b)
            r = [0] * max(len(u), len(v) + b)
            for i, c in enumerate(u): r[i] += c
            for i, c in enumerate(v): r[i + b] += c
        T[(a, b)] = r
        return r
    return g(n, k)

m = lambda N, y: (y * y + 2 * (N + 1) * y - N * N) // 4

print("=== 1. q-счёт свободных путей ЕСТЬ ГАУССОВ БИНОМ ===")
print("    sum q^площадь по путям 0->y = q^{m(N,y)} * [N choose (N+y)/2]_{q^2},")
print("    m(N,y) = (y^2 + 2(N+1)y - N^2)/4")
bad = []
for N in range(2, 19, 2):
    for y in range(-N, N + 1, 2):
        d = q_puti(N, y)
        if not d: continue
        exp = defaultdict(int)
        for i, c in enumerate(gauss_binom(N, (N + y) // 2)):
            exp[m(N, y) + 2 * i] += c
        if dict(d) != dict(exp): bad.append((N, y))
print("    N=2..18, все y:", "сходится всюду ✓" if not bad else f"РАСХОЖДЕНИЯ {bad[:5]}")

print("\n=== 2. показатель КВАДРАТИЧЕН по числу обмоток ===")
print("    подставляем y = jn:  m(N,jn) = (n^2/4) j^2 + (n(N+1)/2) j - N^2/4")
# при нечётном n длина N и обмотка связаны чётностью: y = jn обязано быть чётным,
# поэтому там пробегают только чётные j. Иначе путей просто нет.
for n, N in ((4, 12), (6, 12), (5, 10)):
    js = [j for j in range(-4, 5) if (j * n) % 2 == N % 2][:5]
    xs = [m(N, j * n) for j in js]
    d2 = [xs[i + 2] - 2 * xs[i + 1] + xs[i] for i in range(len(xs) - 2)]
    print(f"    n={n}, N={N}: обмотки {js}, показатели {xs}")
    print(f"              вторые разности {d2} — постоянны, значит показатель квадратичен")

print("\n=== 3. сумма по обмоткам с весом = прямой счёт по циклу ===")
for n, N in ((4, 12), (6, 12), (4, 16)):
    tot = defaultdict(int)
    for j in range(-(N // n) - 2, N // n + 3):
        y = j * n
        if abs(y) <= N:
            for a, c in q_puti(N, y).items(): tot[a] += c
    cur = {0: {0: 1}}
    for _ in range(N):
        nxt = defaultdict(lambda: defaultdict(int))
        for h, pol in cur.items():
            for h2 in (h - 1, h + 1):
                for a, c in pol.items(): nxt[h2][a + h2] += c
        cur = nxt
    direct = defaultdict(int)
    for h, pol in cur.items():
        if h % n == 0:
            for a, c in pol.items(): direct[a] += c
    print(f"    n={n}, N={N}:", "совпало ✓" if dict(tot) == dict(direct) else "РАСХОЖДЕНИЕ")

print("\nИТОГ: тэта-ряд (квадратичные показатели) получен ЧИСТО КОМБИНАТОРНО —")
print("      из счёта площади под путями, без всякого анализа.")

# ─────────────────────────────────────────────────────────────────────────────
# 4. ПОЧЕМУ КОРНИ ИЗ ЕДИНИЦЫ. Подъём замкнутого пути не единствен: можно стартовать
#    с высоты 0, а можно с высоты n. Все высоты сдвигаются на n, площадь — на n*N.
#    Значит вес q^{площадь} определён на окружности ТОЛЬКО при q^n = 1.
import cmath, math
def lifts(n, N, seed=0):
    out = []
    def rec(pos, path):
        if len(path) - 1 == N:
            if (pos - seed) % n == 0: out.append(list(path))
            return
        for d in (-1, 1): rec(pos + d, path + [pos + d])
    rec(seed, [seed]); return out

print("\n=== 4. площадь на окружности определена лишь по модулю одного оборота ===")
for n, N in ((4, 6), (3, 6), (4, 8)):
    a0 = sorted(sum(p[1:]) for p in lifts(n, N, 0))
    a1 = sorted(sum(p[1:]) for p in lifts(n, N, n))
    d = set(x - y for x, y in zip(a1, a0))
    print(f"    n={n}, N={N}: сдвиг подъёма меняет площадь на {d}, ожидалось {{{n*N}}}",
          "✓" if d == {n * N} else "✗")
print("    СЛЕДСТВИЕ: q^{площадь} осмыслен <=> q^{nN}=1 при всех N <=> q^n=1.")
print("    Корни из единицы приходят из ГЕОМЕТРИИ окружности, а не из теории чисел.")

# 5. При q = w^c взвешенный шаг НЕ диагонален в волнах — он лестница: v_k -> v_{k+c}.
print("\n=== 5. взвешенный шаг в базисе волн — лестница ===")
for n, c in ((5, 1), (6, 2), (7, 3), (8, 3)):
    w = cmath.exp(2j * math.pi / n); q = w ** c; ok = True
    for k in range(n):
        v = [w ** (k * x) for x in range(n)]
        Av = [q ** x * (v[(x - 1) % n] + v[(x + 1) % n]) for x in range(n)]
        tgt = [2 * math.cos(2 * math.pi * k / n) * w ** ((k + c) * x) for x in range(n)]
        ok &= all(abs(a - b) < 1e-9 for a, b in zip(Av, tgt))
    print(f"    n={n}, q=w^{c}: A_q v_k = 2cos(2pi k/n) * v_(k+c)", "✓" if ok else "✗")
print("    Сдвиг и умножение на q^x связаны соотношением S D_q = q D_q S —")
print("    это соотношение конечной группы Гейзенберга, откуда и растут гауссовы суммы.")

# 6. Счёт по волнам с весом = сумма произведений косинусов вдоль лестницы.
print("\n=== 6. взвешенный счёт по волнам: произведение косинусов по лестнице ===")
def pryamo(n, N, c):
    w = cmath.exp(2j * math.pi / n); q = w ** c
    M = [[0j] * n for _ in range(n)]
    for x in range(n):
        M[x][(x - 1) % n] += q ** x; M[x][(x + 1) % n] += q ** x
    v = [0j] * n; v[0] = 1
    for _ in range(N):
        v = [sum(M[x][y] * v[x] for x in range(n)) for y in range(n)]
    return v[0]
def lestnica(n, N, c):
    return sum(math.prod(2 * math.cos(2 * math.pi * ((k + i * c) % n) / n) for i in range(N))
               for k in range(n)) / n
for n, N, c in ((5, 6, 1), (6, 8, 2), (7, 6, 3), (5, 10, 2), (8, 8, 3)):
    a, b = pryamo(n, N, c), lestnica(n, N, c)
    print(f"    n={n}, N={N}, q=w^{c}: прямой счёт {a.real:>10.5f}  лестница {b:>10.5f}",
          "✓" if abs(a - b) < 1e-9 else "✗")
