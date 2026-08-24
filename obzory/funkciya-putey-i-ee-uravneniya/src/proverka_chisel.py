#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка чисел обзора «Функция путей и её уравнения».
Запуск: python3 proverka_chisel.py
Блоки: 1) d_m(n): перебор против спектральной формулы;
2) формула утверждения 9 против перебора с площадью «клетки под путём»;
3) изображения против перебора и динамики; 4) число m=3, n=60 и его слагаемые."""
from collections import defaultdict
from math import comb, cos, pi, sin


def C(a, b):
    return comb(a, b) if 0 <= b <= a else 0


def peresbor(m, n):
    """d_m(n): пути из 0 в 0 по отрезку {0..m}, длина 2n."""
    dp = [0] * (m + 1)
    dp[0] = 1
    for _ in range(2 * n):
        nd = [0] * (m + 1)
        for x, v in enumerate(dp):
            if v:
                if x - 1 >= 0:
                    nd[x - 1] += v
                if x + 1 <= m:
                    nd[x + 1] += v
        dp = nd
    return dp[0]


def spektr(m, n):
    """Спектральная формула (теорема 16)."""
    return 2 / (m + 2) * sum(
        (2 * cos(k * pi / (m + 2))) ** (2 * n) * sin(k * pi / (m + 2)) ** 2
        for k in range(1, m + 2))


def brute_area(m, n):
    """Перебор путей из 0 в 0 высоты <= m длины 2n; площадь — сумма высот
    перед каждым шагом вверх. Возвращает {площадь: число путей}."""
    cnt = defaultdict(int)

    def rec(h, taken, area):
        if taken == 2 * n:
            if h == 0:
                cnt[area] += 1
            return
        for step in (1, -1):
            h_new = h + step
            if 0 <= h_new <= m:
                rec(h_new, taken + 1, area + (h if step == 1 else 0))

    rec(0, 0, 0)
    return dict(cnt)


NMAX = 6


def pmul(A, B):
    out = {}
    for i, a in A.items():
        for j, b in B.items():
            if i + j > NMAX:
                continue
            t = out.setdefault(i + j, {})
            for k, v in a.items():
                for l, w in b.items():
                    t[k + l] = t.get(k + l, 0) + v * w
    return out


def shift_xq(A):
    return dict((n, dict((k + n, v) for k, v in d.items())) for n, d in A.items())


def Am(k):
    """F_k(z,q) = 1/(1 - x*F_{k-1}(xq,q)); F_0 = 1."""
    if k == 0:
        return {0: {0: 1}}
    B = shift_xq(Am(k - 1))
    G = {0: {0: 1}}
    P = {0: {0: 1}}
    for r in range(1, NMAX + 1):
        P = pmul(P, B)
        for i, d in P.items():
            if i + r > NMAX:
                continue
            t = G.setdefault(i + r, {})
            for kk, v in d.items():
                t[kk] = t.get(kk, 0) + v
    return G


def obmotki_formula(M, N, x):
    """W_M(N,x) = сумма C(N,(N+x+jM)/2) по целым j с целым нижним индексом."""
    tot = 0
    for j in range(-(N // M + 3), N // M + 4):
        idx = (N + x + j * M)
        if idx % 2 == 0:
            tot += C(N, idx // 2)
    return tot


def obmotki_spektr(M, N, x):
    """Независимая проверка: (1/M) * сумма собственных чисел цикла в степени N."""
    return sum((2 * cos(2 * pi * k / M)) ** N * cos(2 * pi * k * x / M)
               for k in range(M)) / M


def izobrazheniya(m, n):
    """Знакопеременная сумма изображений со сдвигом m+2."""
    M = m + 2
    rng = range(-(n // M + 3), n // M + 3)
    slagaemye = dict((j, C(2 * n, n - j * M) - C(2 * n, n + 1 - j * M)) for j in rng)
    return sum(slagaemye.values()), slagaemye


if __name__ == "__main__":
    print("== d_m(n): перебор против спектральной формулы ==")
    for m in range(1, 6):
        ryad = []
        for n in range(1, 7):
            p, s = peresbor(m, n), round(spektr(m, n))
            assert p == s, (m, n, p, s)
            ryad.append(p)
        print("m=%d: %s" % (m, ryad))

    print("== формула утверждения 9 против перебора ==")
    F4 = Am(4)
    F3 = Am(3)
    F2 = Am(2)
    F1 = Am(1)
    FS = [None, F1, F2, F3, F4]
    for m in range(1, 5):
        for n in range(1, 6):
            got = FS[m].get(n, {})
            want = brute_area(m, n)
            assert got == want, (m, n, got, want)
    print("совпадает всюду при m<=4, n<=5")

    print("== обмотки: формула против спектра цикла ==")
    for M in range(2, 9):
        for N in range(0, 13):
            for x in range(M):
                f_ = obmotki_formula(M, N, x)
                s_ = round(obmotki_spektr(M, N, x))
                assert f_ == s_, (M, N, x, f_, s_)
    print("совпадает всюду при M<=8, N<=12")

    print("== изображения против перебора и динамики ==")
    for m in range(1, 7):
        for n in range(1, 9):
            s_, _ = izobrazheniya(m, n)
            assert s_ == peresbor(m, n), (m, n, s_)
    print("совпадает всюду при m<=6, n<=8")

    print("== m=3, n=60 ==")
    otvet = peresbor(3, 60)
    summ, slag = izobrazheniya(3, 60)
    assert summ == otvet
    mx_diff = max(abs(v) for v in slag.values())
    mx_binom = C(120, 60)
    print("ответ d_3(60) = %d" % otvet)
    print("наибольшее слагаемое-разность = %d, отношение к ответу = %.3g"
          % (mx_diff, mx_diff / otvet))
    print("наибольший биномиальный коэффициент C(120,60) = %d, "
          "отношение к ответу = %.3g" % (mx_binom, mx_binom / otvet))


# ===== БЛОК СКЕЛЕТА (заход svod-i-skelet, 2026-08-24): десять специализаций скелета SKELET.md, каждая проверена счётом на малых значениях =====
# -*- coding: utf-8 -*-
"""Прототип блока проверок скелета: 10 специализаций, каждая счётом."""
from math import comb, cos, pi, sin, sqrt
from collections import defaultdict

def qp_add(a, b):
    r = dict(a)
    for k, v in b.items():
        r[k] = r.get(k, 0) + v
    return r

def qp_mul(a, b):
    r = defaultdict(int)
    for k1, v1 in a.items():
        for k2, v2 in b.items():
            r[k1 + k2] += v1 * v2
    return dict(r)

def qp_shift(a, s):
    return {k + s: v for k, v in a.items()}

def qp_scale(a, c):
    return {k: c * v for k, v in a.items()}

def gauss_binom(N, K):
    """[N choose K]_q как словарь коэффициентов, рекуррентой [nk]=[n-1 k]+q^(n-k)[n-1 k-1]."""
    if K < 0 or K > N:
        return {}
    pol = {0: {0: 1}}
    for n in range(1, N + 1):
        top = min(n, K)
        new = {0: {0: 1}}
        for k in range(1, top + 1):
            a = pol.get(k, {})
            b = qp_shift(pol.get(k - 1, {}), n - k)
            new[k] = qp_add(a, b)
        pol = new
    return pol.get(K, {})

def dp_line_free(n, y):
    """Пути из 0 в y по целой прямой, n шагов ±1."""
    if (n + y) % 2:
        return 0
    dp = {0: 1}
    for _ in range(n):
        nd = defaultdict(int)
        for x, v in dp.items():
            nd[x - 1] += v
            nd[x + 1] += v
        dp = dict(nd)
    return dp.get(y, 0)

def dp_ray_area(n, y):
    """Пути из 0 в y по лучу (никогда ниже 0), n шагов; {площадь(высота перед подъёмом): число}."""
    cnt = defaultdict(int)
    def rec(h, taken, area):
        if taken == n:
            if h == y:
                cnt[area] += 1
            return
        if h + 1 >= 0:
            rec(h + 1, taken + 1, area + h)
        if h - 1 >= 0:
            rec(h - 1, taken + 1, area)
    rec(0, 0, 0)
    return dict(cnt)

def dp_seg_closed_area(m, n):
    """Замкнутые пути 0->0 в полосе {0..m}, длина 2n; {площадь(после подъёма): число}."""
    cnt = defaultdict(int)
    def rec(h, taken, area):
        if taken == 2 * n:
            if h == 0:
                cnt[area] += 1
            return
        for st in (1, -1):
            h2 = h + st
            if 0 <= h2 <= m:
                rec(h2, taken + 1, area + h2 if st == 1 else area)
    rec(0, 0, 0)
    return dict(cnt)

def drob(m, nz, nq):
    """Коэффициенты F_m(z,q)=1/(1-z*q*F_{m-1}(z*q,q)), F_0=1.
    Возвращает словарь {степень z: полином по q (dict)}; усечение до (nz,nq)."""
    Fs = [{0: {0: 1}}]
    for _k in range(1, m + 1):
        Fprev = Fs[-1]
        G = [{j + i: c for j, c in Fprev[i].items()} if i < len(Fprev) else {}
             for i in range(nz + 1)]
        Fk = {0: {0: 1}}
        for _it in range(nz + 2):
            prod = defaultdict(int)
            for i1, f1 in enumerate(G):
                if not f1:
                    continue
                for i2, f2 in Fk.items():
                    if i1 + i2 > nz:
                        continue
                    for j1, c1 in f1.items():
                        for j2, c2 in f2.items():
                            if j1 + j2 + 1 <= nq:
                                prod[(i1 + i2 + 1, j1 + j2 + 1)] += c1 * c2
            Fk = {0: {0: 1}}
            for (i, j), c in prod.items():
                Fk.setdefault(i, {})
                Fk[i][j] = Fk[i].get(j, 0) + c
        Fs.append(Fk)
    return Fs[m]

def fib(k):
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a

def proverki():
    rez = []

    def ok(imya, uslovie, detail=""):
        rez.append((imya, bool(uslovie), detail))

    # 1. Числа Каталана: луч, замкнутые пути без веса
    good = True
    for n in range(1, 8):
        dp = [0] * 40
        dp[0] = 1
        for _ in range(2 * n):
            nd = [0] * 40
            for x, v in enumerate(dp):
                if v:
                    if x: nd[x - 1] += v
                    nd[x + 1] += v
            dp = nd
        good &= dp[0] == comb(2 * n, n) // (n + 1)
    ok("Каталан", good, "луч 0->0, n<=7")

    # 2. Биномиальные коэффициенты: прямая со свободным концом
    good = True
    for n in range(1, 9):
        for y in range(-n, n + 1):
            good &= dp_line_free(n, y) == (comb(n, (n + y) // 2) if (n + y) % 2 == 0 else 0)
    ok("Биномиальные коэффициенты", good, "прямая 0->y, n<=8")

    # 3. q-биномиальные: прямая (обе стенки сняты), свободный конец, вес площади
    good = True
    for N in range(1, 10):
        for y in range(-N, N + 1, 2):
            cnt = {}
            def rec(h, taken, a):
                if taken == N:
                    if h == y:
                        cnt[a] = cnt.get(a, 0) + 1
                    return
                rec(h + 1, taken + 1, a + h + 1)
                rec(h - 1, taken + 1, a)
            rec(0, 0, 0)
            r = (N + y) // 2
            prav = qp_shift(gauss_binom(N, r), r * (3 * r - 2 * N + 1) // 2)
            prav = {k: v for k, v in prav.items() if v}
            if dict(cnt) != prav:
                good = False
    ok("Гауссовы биномиальные (свободный конец с площадью)", good,
       "прямая: q^{r(3r-2N+1)/2}[N r]_q (площадь после подъёма), N<=9")

    # 4. q-Каталана: замкнутые пути по площади против цепной дроби
    good = True
    for n in range(1, 5):
        m = 2 * n
        brut = dp_seg_closed_area(m, n)
        Fr = drob(m + 1, n, 40)
        koef = {k: v for k, v in Fr.get(n, {}).items() if v}
        if dict(brut) != koef:
            good = False
    ok("q-Каталана (Карлиц—Риордан)", good, "дробь против перебора, n<=4")

    # 5. Фибоначчи: спектральная формула при m=3
    def spektr(m, n):
        return round(2 / (m + 2) * sum(
            (2 * cos(k * pi / (m + 2))) ** (2 * n) * sin(k * pi / (m + 2)) ** 2
            for k in range(1, m + 2)))
    good = True
    for n in range(1, 10):
        good &= spektr(3, n) == fib(2 * n - 1)
    ok("Числа Фибоначчи (m=3, Бине)", good, "спектр == Fib(2n-1), n<=9")

    # 6. Пятиугольная теорема / тройное произведение Якоби
    deg = 30
    prod = {0: 1}
    for k in range(1, deg + 1):
        prod = qp_mul(prod, {0: 1, k: -1})
    suma = defaultdict(int)
    j = 0
    while j * (3 * j - 1) // 2 <= deg:
        for jj in ((j,) if j == 0 else (j, -j)):
            e = jj * (3 * jj - 1) // 2
            if e <= deg:
                suma[e] += (-1) ** jj
        j += 1
    good = all(prod.get(e, 0) == suma.get(e, 0) for e in range(deg + 1))
    ok("Тройное произведение Якоби (предел пятиугольной)", good, "до q^%d" % deg)

    # 7. Принцип отражения (одна стенка): разность двух биномов
    good = True
    for n in range(1, 9):
        for y in range(0, n + 1):
            if (n + y) % 2:
                continue
            r = (n + y) // 2
            good &= sum(dp_ray_area(n, y).values()) == comb(n, r) - comb(n, r + 1)
    ok("Принцип отражения (одна стенка)", good, "разность биномов, n<=8")

    # 8. Вероятность возвращения
    good = True
    for n in range(1, 7):
        # прямая: число путей 0->0 за 2n шагов
        good &= dp_line_free(2 * n, 0) == comb(2 * n, n)
        # отрезок m=4: динамика против нормированной спектральной суммы
        m = 4
        dp = [0] * (m + 1); dp[0] = 1
        for _ in range(2 * n):
            nd = [0] * (m + 1)
            for x, v in enumerate(dp):
                if v:
                    if x: nd[x - 1] += v
                    if x < m: nd[x + 1] += v
            dp = nd
        spec = 2 / (m + 2) * sum(
            (2 * cos(k * pi / (m + 2))) ** (2 * n) * sin(k * pi / (m + 2)) ** 2
            for k in range(1, m + 2))
        good &= abs(dp[0] - spec) < 1e-9
    ok("Вероятность возвращения", good, "прямая comb(2n,n)/4^n; отрезок спектром")

    # 9. Оператор Лапласа: матрица синусов диагонализует отрезок
    good = True
    for M in (4, 5, 6, 7):
        S = [[sqrt(2 / M) * sin(pi * j * k / M) for k in range(1, M)] for j in range(1, M)]
        SS = [[sum(S[i][l] * S[l][j] for l in range(M - 1)) for j in range(M - 1)]
              for i in range(M - 1)]
        for i in range(M - 1):
            for j in range(M - 1):
                target = 1.0 if i == j else 0.0
                if abs(SS[i][j] - target) > 1e-9:
                    good = False
        A = [[1 if abs(i - j) == 1 else 0 for j in range(1, M)] for i in range(1, M)]
        lam = [2 * cos(pi * k / M) for k in range(1, M)]
        for col in range(M - 1):
            for i in range(M - 1):
                lhs = sum(A[i][j] * S[j][col] for j in range(M - 1))
                if abs(lhs - lam[col] * S[i][col]) > 1e-9:
                    good = False
    ok("Оператор Лапласа (дискретный)", good, "S^2=I и Av=lambda v, M=4..7")

    # 10. Модулярность: эта-тест Роджерса—Рамануджана
    D = 32
    def obratnoe(i):
        """Ряд 1/(1-q^i), усечённый до степени D."""
        return {k: 1 for k in range(0, D + 1, i)}
    G = {}
    H = {}
    j = 0
    while j * j <= D:
        den = {0: 1}
        for i in range(1, j + 1):
            den = qp_mul(den, obratnoe(i))
        den = {k: v for k, v in den.items() if k <= D}
        G = qp_add(G, qp_shift(den, j * j))
        H = qp_add(H, qp_shift(den, j * j + j))
        j += 1
    # Q = H/G до степени D через решение G*Q = H (старший коэф G равен 1)
    Q = defaultdict(int)
    for mm in range(0, D + 1):
        s = H.get(mm, 0)
        for d in range(0, mm):
            s -= G.get(mm - d, 0) * Q.get(d, 0)
        Q[mm] = s
    # логарифмическая производная: S = q*Q'/Q, решаем Q*S = q*Q' почленно
    # (q*Q'/Q)[mm] = -sum_{n|mm} n c_n q^mm; при mm>=0: sum_{d=0..mm} Q[d] S[mm-d] = mm*Q[mm]
    S = defaultdict(int)
    for mm in range(0, D + 1):
        rhs = (mm * Q.get(mm, 0)) if mm >= 1 else 0
        acc = rhs - sum(Q.get(mm - d, 0) * S[d] for d in range(0, mm))
        S[mm] = acc  # Q[0]=1
    a = {mm: -S.get(mm, 0) for mm in range(1, D + 1)}

    def mobius(n):
        mu = 1
        x = n
        f = 2
        while f * f <= x:
            if x % f == 0:
                x //= f
                mu *= -1
                if x % f == 0:
                    return 0
            f += 1
        if x > 1:
            mu *= -1
        return mu

    cs = {}
    for mm in range(1, D + 1):
        val = sum(mobius(d) * a.get(mm // d, 0)
                  for d in range(1, mm + 1) if mm % d == 0)
        cs[mm] = val // mm
    pattern = [cs.get(mm) for mm in range(1, 16)]
    expected = [1, -1, -1, 1, 0] * 3
    ok("Модулярность (эта-тест RR, уровень 5)", pattern == expected,
       "показатели c_1..c_15 = %s" % (pattern,))
    return rez


if __name__ == "__main__":
    rs = proverki()
    X = sum(1 for _, u, _ in rs if u)
    Y = len(rs)
    for imya, u, det in rs:
        print(("OK " if u else "FAIL ") + imya + (" — " + det if det else ""))
    print("проверено %d из %d" % (X, Y))
    raise SystemExit(0 if X == Y else 1)
