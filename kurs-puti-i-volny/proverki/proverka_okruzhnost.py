"""Проверки к заходу ZAHOD-okruzhnost.md: что на окружности Z_n считается проще.
Запуск: python3 proverka_okruzhnost.py
Ничего не берётся из памяти: каждое утверждение проверяется прямым перебором."""
from math import comb, cos, pi, sin, sqrt, exp, log
import cmath
import numpy as np

W = lambda n: cmath.exp(2j * pi / n)
OK = "  ✓"

# ---------- 0. прямой перебор: пути по циклу Z_n ----------
def cikl_perebor(n, N, x=0):
    """число путей длины N из 0 в x по циклу Z_n, шаги ±1"""
    f = [0] * n
    f[0] = 1
    for _ in range(N):
        f = [f[(i - 1) % n] + f[(i + 1) % n] for i in range(n)]
    return f[x % n]

def otrezok_perebor(m, N, x=0):
    """число путей длины N из 0 в x по отрезку {0..m} со стенками"""
    f = [0] * (m + 1)
    f[0] = 1
    for _ in range(N):
        g = [0] * (m + 1)
        for i, c in enumerate(f):
            for j in (i - 1, i + 1):
                if 0 <= j <= m:
                    g[j] += c
        f = g
    return f[x]


# ---------- 1. развёртка окружности: сумма по обмоткам (тождество Рамуса) ----------
print("=== 1. развёртка: сумма по ОБМОТКАМ, все знаки ПЛЮС ===")
def obmotki(n, N, x=0):
    """путь по Z_n = путь по прямой, пришедший в x + jn. Знаков нет."""
    s = 0
    for j in range(-(N // n) - 2, N // n + 3):
        top = N + x + j * n
        if top % 2 == 0 and 0 <= top // 2 <= N:
            s += comb(N, top // 2)
    return s

for n in (3, 4, 5, 6, 7):
    for N in range(0, 13):
        for x in range(n):
            assert cikl_perebor(n, N, x) == obmotki(n, N, x), (n, N, x)
print("  n=3..7, N<=12, все x: перебор = сумма по обмоткам" + OK)
print("  сравнение со СТЕНКАМИ (m=n/2-2): там та же сумма, но ЗНАКОПЕРЕМЕННАЯ —")
print("  теорема 25 обзора: sum_j [C(2n, n-j(m+2)) - C(2n, n+1-j(m+2))]")

# ---------- 2. ряд Фурье окружности: сумма по спектру ----------
print("\n=== 2. Фурье: сумма по характерам, спектр 2cos(2pi k/n) ===")
def spektr_cikl(n, N, x=0):
    w = W(n)
    return sum(w ** (-k * x) * (2 * cos(2 * pi * k / n)) ** N for k in range(n)) / n

for n in (3, 4, 5, 6, 7, 8):
    for N in range(0, 13):
        for x in range(n):
            assert abs(spektr_cikl(n, N, x) - cikl_perebor(n, N, x)) < 1e-6, (n, N, x)
print("  n=3..8, N<=12, все x: перебор = спектральная сумма" + OK)
print("  собственные векторы даны ГРУППОЙ (характеры omega^{kx}), решать нечего;")
print("  на отрезке их надо добывать из трёхчленной рекурренты + две стенки.")

# ---------- 3. равенство 1 = 2 есть КОНЕЧНОЕ суммирование Пуассона ----------
print("\n=== 3. равенство двух формул = мультисекция ряда (фильтр корнями из 1) ===")
print("  тождество Рамуса (Ramus 1834):  sum_j C(N, r+jn) = (1/n) sum_k w^{-kr} (1+w^k)^N")
for n in (3, 4, 5, 6, 7):
    for N in range(0, 14):
        for r in range(0, N + 1):
            lhs = sum(comb(N, r + j * n) for j in range(-(N // n) - 2, N // n + 3)
                      if 0 <= r + j * n <= N)
            w = W(n)
            rhs = sum(w ** (-k * r) * (1 + w ** k) ** N for k in range(n)) / n
            assert abs(lhs - rhs) < 1e-6, (n, N, r, lhs, rhs)
print("  n=3..7, N<=13, все r: сходится" + OK)
print("  доказательство — три строки: sum_k w^{k(a-b)} = n*[a=b mod n].")

# ---------- 4. дополнительность сложностей: сколько членов нужно каждой формуле ----------
print("\n=== 4. дополнительность: сколько членов нужно каждой формуле (n=12) ===")
n = 12
print(f"  {'N':>4} {'ответ':>14} {'обмоток':>9} {'гармоник':>9}")
for N in (2, 6, 12, 40, 120, 400):
    tochno = cikl_perebor(n, N, 0)
    # сколько обмоток даёт 10 знаков
    def obm_chastich(J):
        s = 0
        for j in range(-J, J + 1):
            top = N + j * n
            if top % 2 == 0 and 0 <= top // 2 <= N:
                s += comb(N, top // 2)
        return s
    n_obm = next(J for J in range(0, 200) if abs(obm_chastich(J) - tochno) <= 1e-10 * abs(tochno))
    def spek_chastich(K):
        w = W(n)
        # берём K старших по модулю гармоник
        idx = sorted(range(n), key=lambda k: -abs(2 * cos(2 * pi * k / n)))[:K]
        return sum((2 * cos(2 * pi * k / n)) ** N for k in idx).real / n
    n_spek = next((K for K in range(1, n + 1)
                   if abs(spek_chastich(K) - tochno) <= 1e-10 * abs(tochno)), n)
    print(f"  {N:>4} {tochno:>14} {2*n_obm+1:>9} {n_spek:>9}")
print("  та же дополнительность, что на отрезке, но БЕЗ знакопеременности:")
print("  на окружности обмотки не сокращаются катастрофически, они просто малы.")

# ---------- 5. ДВА параметра: время N и поток (твист) phi ----------
print("\n=== 5. два параметра: длина N и поток phi через окружность ===")
print("  Z(N,phi) = sum_j C(N,(N+x)/2 + jn) e^{i j phi}   [обмотки, вес за оборот]")
print("           = (1/n) sum_k e^{-i(2pi k+phi)x/n} (2cos((2pi k+phi)/n))^N   [гармоники]")
def obmotki_tvist(n, N, phi, x=0):
    s = 0
    for j in range(-(N // n) - 3, N // n + 4):
        top = N + x + j * n
        if top % 2 == 0 and 0 <= top // 2 <= N:
            s += comb(N, top // 2) * cmath.exp(1j * j * phi)
    return s

def spektr_tvist(n, N, phi, x=0):
    s = 0
    for k in range(n):
        th = (2 * pi * k + phi) / n
        s += cmath.exp(-1j * th * x) * (2 * cos(th)) ** N
    return s / n

bad = 0
for n in (3, 4, 5, 6, 7):
    for N in range(0, 12):
        for x in range(n):
            for phi in (0.0, 0.3, 1.0, 2.0, pi, 4.7):
                a = obmotki_tvist(n, N, phi, x)
                b = spektr_tvist(n, N, phi, x)
                if abs(a - b) > 1e-6:
                    bad += 1
                    if bad < 4:
                        print("  РАСХОЖДЕНИЕ", n, N, x, phi, a, b)
print(("  все случаи сошлись" + OK) if bad == 0 else f"  РАСХОЖДЕНИЙ: {bad}")
print("  ДВЕ симметрии, каждая очевидна на СВОЕЙ стороне и невидима на другой:")
print("   (а) phi -> phi + 2pi : слева умножение на e^{2pi i j}=1, тривиально;")
print("       справа это ПЕРЕНУМЕРАЦИЯ гармоник k -> k+1 — сдвиг спектра.")
print("   (б) x -> x + n : справа фаза e^{-i phi}, слева сдвиг обмотки j -> j-1.")

# ---------- 6. есть ли симметрия «пространство <-> время»? ----------
print("\n=== 6. ПРОВЕРКА заявки «у тора нет выделенного времени» ===")
def tr_A(n, N):
    return sum((2 * cos(2 * pi * k / n)) ** N for k in range(n)).real
print(f"  {'n':>3} {'N':>3} {'tr A_n^N':>14} {'tr A_N^n':>14}")
for (n_, N_) in ((4, 6), (6, 4), (5, 10), (10, 5), (6, 8), (8, 6)):
    print(f"  {n_:>3} {N_:>3} {tr_A(n_, N_):>14.4f} {tr_A(N_, n_):>14.4f}")
print("  ВЫВОД: голого равенства tr A_n^N = tr A_N^n НЕТ. Заявку «пространство и время")
print("  на торе равноправны» в этом виде предъявлять НЕЛЬЗЯ — она ложна.")

# ---------- 7. конечная модулярная группа НА ОКРУЖНОСТИ (представление Вейля) ----------
print("\n=== 7. модулярная группа на окружности из n точек: S = Фурье, T = гауссов вес ===")
for n in (5, 7, 9, 11, 13):
    w = W(n)
    S = np.array([[w ** (j * k) for k in range(n)] for j in range(n)]) / sqrt(n)
    S2 = S @ S
    perm = np.zeros((n, n), dtype=complex)
    for k in range(n):
        perm[(-k) % n, k] = 1
    f1 = np.allclose(S2, perm)                      # S^2 = отражение x -> -x
    f2 = np.allclose(S @ S @ S @ S, np.eye(n))      # S^4 = I
    # ищем гауссов вес T = diag(w^{c k^2}), при котором (ST)^3 пропорционально S^2
    nashli = None
    for c in range(1, n):
        T = np.diag([w ** (c * k * k) for k in range(n)])
        M = (S @ T) @ (S @ T) @ (S @ T)
        idx = np.argmax(np.abs(S2))
        lam = M.flat[idx] / S2.flat[idx]
        if np.allclose(M, lam * S2, atol=1e-8):
            nashli = (c, lam)
            break
    print(f"  n={n}: S^2 = отражение x->-x: {f1};  S^4=I: {f2};  "
          f"(ST)^3 = c*S^2 при T=diag(w^{{{nashli[0]}k^2}}), c={nashli[1]:.4f}"
          if nashli else f"  n={n}: (ST)^3 ~ S^2 НЕ НАЙДЕНО")
print("  🔴 СМЫСЛ: S^2 — это ровно то отражение x -> -x, которым окружность")
print("  складывается в отрезок. Складывание в стенки и элемент S модулярной")
print("  группы — один и тот же оператор.")

# ---------- 8. соотношение Ландсберга — Шаара: тэта-преобразование БЕЗ анализа ----------
print("\n=== 8. Ландсберг — Шаар: конечное тождество, дискретный носитель tau -> -1/tau ===")
print("  (1/sqrt(a)) sum_{k<a} e^{2pi i k^2 b/a} = (e^{i pi/4}/sqrt(2b)) sum_{k<2b} e^{-i pi k^2 a/(2b)}")
for a in (1, 2, 3, 4, 5, 6, 7, 8, 9):
    for b in (1, 2, 3, 4, 5):
        lhs = sum(cmath.exp(2j * pi * k * k * b / a) for k in range(a)) / sqrt(a)
        rhs = cmath.exp(1j * pi / 4) * sum(cmath.exp(-1j * pi * k * k * a / (2 * b))
                                           for k in range(2 * b)) / sqrt(2 * b)
        assert abs(lhs - rhs) < 1e-8, (a, b, lhs, rhs)
print("  a=1..9, b=1..5: сходится всюду" + OK)
print("  это буквально функциональное уравнение тэты, снятое в рациональных точках,")
print("  и доказывается конечными средствами (Moore, arXiv:1810.06172).")

# ---------- 9. вероятностная задача: за сколько шагов забывается начало ----------
print("\n=== 9. вероятностная задача: время перемешивания на Z_n ===")
def tv_rasst(n, N):
    """полная вариация между ленивым блужданием после N шагов и равномерным"""
    f = np.zeros(n); f[0] = 1
    P = np.zeros((n, n))
    for i in range(n):
        P[i, i] = 0.5; P[i, (i + 1) % n] += 0.25; P[i, (i - 1) % n] += 0.25
    v = f @ np.linalg.matrix_power(P, N)
    return 0.5 * np.sum(np.abs(v - 1 / n))

print(f"  {'n':>4} {'t_mix(1/4)':>11} {'t_mix/n^2':>10} {'щель':>10} {'2/(pi^2) est':>13}")
for n in (7, 11, 21, 41, 81):
    t = next(N for N in range(1, 40000) if tv_rasst(n, N) < 0.25)
    gap = 1 - (0.5 + 0.5 * cos(2 * pi / n))
    print(f"  {n:>4} {t:>11} {t/n**2:>10.4f} {gap:>10.6f} {gap*n**2:>13.4f}")
print("  щель = 1 - (1+cos(2pi/n))/2 ~ pi^2/n^2  =>  время релаксации ~ n^2/pi^2.")
print("  Это ОТВЕТ АНАЛИЗА НА ВЕРОЯТНОСТНЫЙ ВОПРОС: собственное число ближайшее к 1")
print("  считается тривиально (характеры даны группой) и сразу даёт порядок n^2.")

print("\n=== 9б. чётность: без лени блуждание на ЧЁТНОЙ окружности не перемешивается ===")
for n in (6, 7):
    f = np.zeros(n); f[0] = 1
    A = np.zeros((n, n))
    for i in range(n):
        A[i, (i + 1) % n] = A[i, (i - 1) % n] = 0.5
    for N in (50, 51):
        v = f @ np.linalg.matrix_power(A, N)
        print(f"  n={n}, N={N}: расст.до равномерного = {0.5*np.sum(np.abs(v-1/n)):.6f}")
print("  причина видна в спектре: при чётном n есть собственное число -1 (k=n/2).")
print("  Это тот же паритет, из-за которого на отрезке считают пути ЧЁТНОЙ длины.")

# ---------- 10. q на окружности: циклическое просеивание ----------
print("\n=== 10. q-версия на окружности: циклическое просеивание (Райнер—Стэнтон—Уайт) ===")
def q_binom_poly(n, k):
    """коэффициенты гауссова бинома [n k]_q как ЦЕЛОГО многочлена (точно)"""
    P = [[1]] + [[] for _ in range(n)]
    tabl = {(0, 0): [1]}
    def get(a, b):
        if b < 0 or b > a:
            return [0]
        if (a, b) in tabl:
            return tabl[(a, b)]
        if b == 0 or b == a:
            r = [1]
        else:
            u, v = get(a - 1, b - 1), get(a - 1, b)   # [n k] = [n-1 k-1] + q^k [n-1 k]
            r = [0] * max(len(u), len(v) + b)
            for i, c in enumerate(u):
                r[i] += c
            for i, c in enumerate(v):
                r[i + b] += c
        tabl[(a, b)] = r
        return r
    return get(n, k)

def q_binom(n, k, q):
    return sum(c * q ** i for i, c in enumerate(q_binom_poly(n, k)))

from itertools import combinations
for n, k in ((6, 2), (6, 3), (8, 4), (9, 3), (10, 5), (12, 4)):
    podmn = list(combinations(range(n), k))
    for d in range(n):
        nepodv = sum(1 for s in podmn
                     if set((x + d) % n for x in s) == set(s))
        val = q_binom(n, k, W(n) ** d)
        assert abs(val - nepodv) < 1e-6, (n, k, d, val, nepodv)
    print(f"  n={n}, k={k}: [n k]_q в корне w^d = число подмножеств, неподвижных"
          f" при повороте на d" + OK)
print("  q-биномиальный коэффициент, посчитанный В КОРНЕ ИЗ ЕДИНИЦЫ, СЧИТАЕТ.")
print("  Это ровно связка «q-версия <-> окружность», которой на отрезке нет.")

print("\nВсё сошлось.")

# ---------- 11. производящая функция окружности: прямая x поправка на обмотки ----------
print("\n=== 11. производящая функция: цепной дроби НЕ НУЖНО ===")
print("  G_n(z) = sum_N (замкнутых путей длины N на Z_n) z^N")
print("  гипотеза:  G_n(z) = 1/sqrt(1-4z^2) * (1+u^n)/(1-u^n),  u=(1-sqrt(1-4z^2))/(2z)")
for n in (3, 4, 5, 6, 7, 8):
    for z in (0.05, 0.1, 0.17, 0.2):
        ryad = sum(cikl_perebor(n, N, 0) * z ** N for N in range(0, 160))
        s = sqrt(1 - 4 * z * z)
        u = (1 - s) / (2 * z)
        zamk = (1 / s) * (1 + u ** n) / (1 - u ** n)
        spek = sum(1 / (1 - 2 * z * cos(2 * pi * k / n)) for k in range(n)) / n
        assert abs(ryad - zamk) < 1e-9, (n, z, ryad, zamk)
        assert abs(ryad - spek) < 1e-9, (n, z, ryad, spek)
    print(f"  n={n}: ряд = замкнутая формула = сумма простейших дробей  ✓")
print("  ЧИТАЕТСЯ БУКВАЛЬНО: 1/sqrt(1-4z^2) — прямая (свободный путь);")
print("  (1+u^n)/(1-u^n) = 1 + 2u^n + 2u^{2n} + ... — сумма по числу обмоток,")
print("  u^n — цена одного оборота. Разложение на простейшие дроби дано СПЕКТРОМ,")
print("  то есть характерами; решать характеристическое уравнение не нужно.")
geom = [sum(cikl_perebor(5,N,0)*0.1**N for N in range(160))]
print("  на ОТРЕЗКЕ то же место — цепная дробь глубины m и многочлены Чебышёва.")

# ---------- 12. вес по площади на окружности: откуда берётся тэта ----------
print("\n=== 12. вес q^{площадь}: на развёртке показатели КВАДРАТИЧНЫ по обмотке ===")
print("  путь по Z_n длины N с обмоткой j = путь по прямой из 0 в jn.")
print("  минимальная площадь под таким путём растёт квадратично по j:")
def min_ploshad(N, konec):
    """мин. сумма высот пути из 0 в konec за N шагов ±1 (высоты после каждого шага)"""
    import functools
    NEG = 10**9
    dp = {0: 0}
    for t in range(N):
        nd = {}
        for x, a in dp.items():
            for y in (x - 1, x + 1):
                v = a + y
                if y not in nd or v < nd[y]:
                    nd[y] = v
        dp = nd
    return dp.get(konec, None)
n = 4
print(f"  n={n}, N=24:  j -> минимальная площадь")
for j in range(0, 4):
    p = min_ploshad(24, j * n)
    print(f"    j={j}: конец {j*n:>3},  мин.площадь = {p}")
print("  разности вторые постоянны => показатель вида c*j^2 + ...")
print("  => sum_j q^{c j^2} x^j — это тэта-ряд, и на окружности он выходит")
print("  БЕЗ знаков: знакопеременность на отрезке приходит от ОТРАЖЕНИЙ,")
print("  которых на окружности нет. Тождество Якоби о ТРОЙНОМ произведении")
print("  (со знаками) — это уже сложенная версия. СТАТУС: наблюдение на малых")
print("  случаях, полного вывода тэты из путей на окружности здесь НЕ сделано.")
