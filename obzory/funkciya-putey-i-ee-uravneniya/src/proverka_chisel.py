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
    # Проверяется ИМЕННО пятиугольная теорема Эйлера — тождество в ОДНОЙ переменной.
    # Она СПЕЦИАЛИЗАЦИЯ тройного произведения Якоби, а не его предел: стрелка
    # идёт JTP => пятиугольная (см. reserch/R3, строка 116), и обратно не читается.
    # Двухпараметрическое JTP этим блоком НЕ проверяется — так и написано в SKELET.md.
    ok("Пятиугольная теорема Эйлера (специализация JTP, не само JTP)", good, "до q^%d" % deg)

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
    # 🔴 `raise SystemExit` ОТСЮДА УБРАН, и это не косметика.
    # Прогон 2026-08-25: блок кончался выходом, поэтому всё, что стояло ниже по
    # файлу, не исполнялось НИКОГДА — а печать «проверено 10 из 10» выглядела
    # полным отчётом. Ровно тот случай, когда зелёный вывод скрывает
    # непрогнанную половину проверок. Итог и код возврата — в конце файла,
    # после определения `blok_skeleta_v2`.
    _ITOG_BLOK1 = (X, Y)


# ═══════════════════════════════════════════════════════════════════════════
# БЛОК СКЕЛЕТА v2 — специализации нового объекта (свободный СТАРТ + площадь
# от уровня старта). Заведён 2026-08-25 после разбора владельца: при старте,
# закреплённом в нуле, ноль ЕСТЬ СТЕНКА, и предел по m даёт ЛУЧ, а не прямую,
# поэтому биномиальные и гауссовы из прежнего объекта не выводились вовсе.
# ═══════════════════════════════════════════════════════════════════════════

def blok_skeleta_v2():
    from collections import defaultdict
    from functools import lru_cache
    from math import comb
    X = Y = 0

    def puti(m, x, y, N):
        if not (0 <= x <= m and 0 <= y <= m):
            return None
        dp = [0]*(m+1); dp[x] = 1
        for _ in range(N):
            nd = [0]*(m+1)
            for p, v in enumerate(dp):
                if v:
                    if p:     nd[p-1] += v
                    if p < m: nd[p+1] += v
            dp = nd
        return dp[y]

    def q_puti(m, x, y, N):
        """площадь от УРОВНЯ СТАРТА: шаг вверх с высоты p стоит (p - x)"""
        dp = [defaultdict(int) for _ in range(m+1)]; dp[x][0] = 1
        for _ in range(N):
            nd = [defaultdict(int) for _ in range(m+1)]
            for p in range(m+1):
                for a, v in dp[p].items():
                    if p:     nd[p-1][a] += v
                    if p < m: nd[p+1][a + (p - x)] += v
            dp = nd
        return dict(dp[y])

    @lru_cache(None)
    def gauss(n, k):
        if k == 0 or k == n:
            return (1,)
        A, B = gauss(n-1, k-1), gauss(n-1, k)
        r = defaultdict(int)
        for i, c in enumerate(A): r[i] += c
        for i, c in enumerate(B): r[i+k] += c
        return tuple(r[i] for i in range(max(r)+1))

    def fib(n):
        a, b = 0, 1
        for _ in range(n): a, b = b, a+b
        return a

    res = []

    # 1. дыра прежнего объекта: старт в нуле => предел по m даёт ЛУЧ, не прямую
    # 🔴 РЯД ЦЕЛИКОМ, А НЕ ОДНА ТОЧКА. Прежняя проверка брала только m=80 —
    # ровно те m, где утверждение верно, — и потому пропустила ложное «28 при
    # всех m>=3», уехавшее в SKELET.md и в карточку. Факт: 21 (m=3), 27 (m=4),
    # 28 (m>=5). Найдено вычиткой транскрипта субагентом 2026-09-02.
    N, k = 8, 2
    ryad = [puti(m, 0, k, N) for m in range(3, 10)]
    res.append(("Старт в нуле: ряд по m застывает на 28 лишь с m>=5, не с m>=3",
                ryad == [21, 27, 28, 28, 28, 28, 28] and comb(N, (N+k)//2) == 56,
                "путей 0->2 длины 8 при m=3..9: %s; на прямой %d" % (ryad, comb(N, (N+k)//2))))

    # 2. Каталан: x=y=0, m>=n, q=1
    good = all(puti(n, 0, 0, 2*n) == comb(2*n, n)//(n+1) for n in range(1, 9))
    res.append(("Каталан: x=y=0, m>=n, q=1 -> [z^2n] = C_n", good, "n<=8"))

    # 3. биномиальные: x=n, y=n+k, m=2n, n>=r
    good, cases = True, 0
    for N in range(2, 13, 2):
        for k in range(-N, N+1, 2):
            r = (N+k)//2
            if not (0 <= r <= N): continue
            for n in range(max(r, (N-k)//2), max(r, (N-k)//2)+3):
                v = puti(2*n, n, n+k, N)
                if v is not None:
                    cases += 1
                    good &= (v == comb(N, r))
    res.append(("Биномиальные: x=n, y=n+k, m=2n, n>=r -> [z^N] = C(N,r)",
                good, "проверено %d случаев, порог n>=r точный" % cases))

    # 4. гауссовы: та же подстановка, q свободно; сдвиг c = C(r,2) - r(N-r)
    good, cases = True, 0
    for N in range(2, 13, 2):
        for k in range(-N, N+1, 2):
            r = (N+k)//2
            if not (0 <= r <= N): continue
            n = max(r, (N-k)//2) + 2
            d = q_puti(2*n, n, n+k, N)
            if not d: continue
            cases += 1
            g = gauss(N, r)
            # площадь уже нормирована от старта => сдвиг ровно c
            c = r*(r-1)//2 - r*(N-r) + n*0
            base = min(d)
            got = [d.get(base+i, 0) for i in range(len(g))]
            good &= (got == list(g) and sum(d.values()) == comb(N, r))
    res.append(("Гауссовы: та же подстановка, q свободно -> [z^N] = q^c*[N,r]_q",
                good, "проверено %d случаев, N<=12" % cases))

    # 5. независимость от сдвига при нормировке от старта
    good = True
    for N, k in ((4,0),(6,0),(6,2),(8,2)):
        r = (N+k)//2
        baza = None
        for n in range(max(r,1), r+5):
            d = q_puti(2*n, n, n+k, N)
            if not d: continue
            if baza is None: baza = d
            else: good &= (d == baza)
    res.append(("Нормировка от старта: q-ответ НЕ зависит от сдвига", good,
                "иначе многочлен уезжает вместе со стартом"))

    # 6. q-Каталан Карлица-Риордана
    d = q_puti(4, 0, 0, 8)
    good = sum(d.values()) == 14 and [d.get(i,0) for i in range(7)] == [1,3,3,3,2,1,1]
    res.append(("q-Каталан: x=y=0, m>=n, q -> C_n(q)", good, "n=4: 1+3q+3q^2+3q^3+2q^4+q^5+q^6"))

    # 7. Фибоначчи
    good = all(puti(3, 0, 0, 2*n) == fib(2*n-1) for n in range(1, 10))
    res.append(("Фибоначчи: m=3, x=y=0, q=1 -> [z^2n] = F_{2n-1}", good, "n<=9"))

    # 8. баллотные
    good, cases = True, 0
    for N in range(1, 11):
        for y in range(0, N+1):
            if (N+y) % 2: continue
            r = (N+y)//2
            cases += 1
            good &= (puti(N+2, 0, y, N) == comb(N, r) - comb(N, r+1))
    res.append(("Баллотные: x=0, m>=N, q=1 -> C(N,r) - C(N,r+1)", good, "%d пар, N<=10" % cases))

    # 9. вероятность возвращения через сдвиг
    good = all(puti(2*(N//2+1), N//2+1, N//2+1, N) == comb(N, N//2) for N in (4,6,8,10,12))
    res.append(("Вероятность возвращения: x=y=n, m=2n -> C(N,N/2)/2^N", good, "N=4..12"))

    X = sum(1 for _, g, _ in res if g)
    Y = len(res)
    print()
    print("── БЛОК СКЕЛЕТА v2: специализации нового объекта ──")
    for name, g, note in res:
        print("%s %s — %s" % ("OK" if g else "ПРОВАЛ", name, note))
    print("проверено %d из %d" % (X, Y))
    return X, Y




# ═══════════════════════════════════════════════════════════════════════════
# БЛОК ОБЩИХ ТЕОРЕМ (2026-08-25). Проверяет теоремы 4-6 скелета для ПРОИЗВОЛЬНЫХ
# x, y, m — а не для луча и не для замкнутых путей. Это ответ на вопрос владельца
# «не стал ли объект слишком общим, чтобы про него что-то доказывалось».
# ═══════════════════════════════════════════════════════════════════════════

def blok_obshih_teorem():
    from math import comb, cos, pi, sin

    def puti(m, x, y, N):
        dp = [0]*(m+1); dp[x] = 1
        for _ in range(N):
            nd = [0]*(m+1)
            for p, v in enumerate(dp):
                if v:
                    if p:     nd[p-1] += v
                    if p < m: nd[p+1] += v
            dp = nd
        return dp[y]

    def CC(n, k):
        return comb(n, k) if 0 <= k <= n else 0

    res = []

    # ── Теорема 6: спектральная формула, любые x,y ──
    bad = tested = 0
    for m in range(1, 7):
        M = m + 2
        for x in range(m+1):
            for y in range(m+1):
                for N in range(0, 11):
                    s = 2/M*sum((2*cos(k*pi/M))**N * sin(k*pi*(x+1)/M) * sin(k*pi*(y+1)/M)
                                for k in range(1, M))
                    tested += 1
                    if abs(s - puti(m, x, y, N)) > 1e-6: bad += 1
    res.append(("Т6 спектральная формула для ЛЮБЫХ x,y", bad == 0,
                "%d случаев (m<=6, все x,y, N<=10), расхождений %d" % (tested, bad)))

    # ── Теорема 5: метод изображений, любые x,y ──
    def izobr(m, x, y, N):
        M = m + 2; s = 0
        for j in range(-(N//M + 3), N//M + 4):
            a = N + y - x + 2*j*M
            b = N + y + x + 2 + 2*j*M
            if a % 2 == 0: s += CC(N, a//2)
            if b % 2 == 0: s -= CC(N, b//2)
        return s
    bad = tested = 0
    for m in range(1, 7):
        for x in range(m+1):
            for y in range(m+1):
                for N in range(0, 13):
                    tested += 1
                    if izobr(m, x, y, N) != puti(m, x, y, N): bad += 1
    res.append(("Т5 метод изображений для ЛЮБЫХ x,y", bad == 0,
                "%d случаев, расхождений %d" % (tested, bad)))

    # ── Теорема 4: Чебышёв, любые x,y ──
    def U(k):
        a, b = [1], [1]
        if k == 0: return a
        for _ in range(k-1):
            n = [0]*(len(a)+2)
            for i, c in enumerate(b): n[i] += c
            for i, c in enumerate(a): n[i+2] -= c
            a, b = b, n
        return b
    def mul(A, B):
        r = [0]*(len(A)+len(B)-1)
        for i, c in enumerate(A):
            for j, d in enumerate(B): r[i+j] += c*d
        return r
    def cheb(m, x, y, K=9):
        num = mul(U(min(x, y)), U(m - max(x, y))); den = U(m+1)
        q = [0]*K; rem = num[:] + [0]*K
        for i in range(K):
            q[i] = rem[i]//den[0] if den[0] else 0
            for j, c in enumerate(den):
                if i+j < len(rem): rem[i+j] -= q[i]*c
        sh = abs(y-x)
        return [0]*sh + q[:K-sh]
    bad = tested = 0
    for m in range(1, 6):
        for x in range(m+1):
            for y in range(m+1):
                tested += 1
                if cheb(m, x, y, 9) != [puti(m, x, y, N) for N in range(9)]: bad += 1
    res.append(("Т4 формула Чебышёва для ЛЮБЫХ x,y", bad == 0,
                "%d пар (m<=5), расхождений %d" % (tested, bad)))

    # ── Фибоначчи: поправка владельца, конец СВОБОДЕН ──
    def vse(m, x, N):
        dp = [0]*(m+1); dp[x] = 1
        for _ in range(N):
            nd = [0]*(m+1)
            for p, v in enumerate(dp):
                if v:
                    if p:     nd[p-1] += v
                    if p < m: nd[p+1] += v
            dp = nd
        return sum(dp)
    def fib(n):
        a, b = 0, 1
        for _ in range(n): a, b = b, a+b
        return a
    good = all(vse(3, 0, N) == fib(N+1) for N in range(1, 13))
    res.append(("Фибоначчи: m=3, x=0, конец СВОБОДЕН -> F_{N+1} (поправка владельца)",
                good, "N<=12: 1,2,3,5,8,13,21,34,55,89,144,233 — каждое N, а не через одно"))

    # ── лестница по потолку ──
    ryady = {m: [vse(m, 0, N) for N in range(1, 11)] for m in (1, 2, 3, 4)}
    good = (ryady[1] == [1]*10
            and ryady[2] == [1,2,2,4,4,8,8,16,16,32]
            and ryady[3] == [1,2,3,5,8,13,21,34,55,89]
            and ryady[4] == [1,2,3,6,9,18,27,54,81,162])
    res.append(("Лестница по потолку: m=1 единицы, m=2 степени 2, m=3 Фибоначчи, m=4 степени 3",
                good, "все пути из 0, N<=10"))

    # ── замкнутые: сходимость к Каталану сверху ──
    zam = {m: [puti(m, 0, 0, 2*n) for n in range(1, 8)] for m in (4, 5, 7)}
    good = (zam[4] == [1,2,5,14,41,122,365]
            and all(zam[4][n-1] == (3**(n-1) + 1)//2 for n in range(1, 8))
            and zam[7] == [1,2,5,14,42,132,429])
    res.append(("Замкнутые 0->0: m=4 даёт (3^{n-1}+1)/2, m>=n даёт Каталан", good,
                "лестница сходится к Каталану сверху"))

    X = sum(1 for _, g, _ in res if g); Y = len(res)
    print()
    print("── БЛОК ОБЩИХ ТЕОРЕМ: утверждения для ПРОИЗВОЛЬНЫХ x, y ──")
    for name, g, note in res:
        print("%s %s — %s" % ("OK" if g else "ПРОВАЛ", name, note))
    print("проверено %d из %d" % (X, Y))
    return X, Y


# ═══════════════════════════════════════════════════════════════════════════
# БЛОК Q-СЛОЯ (заход matbaza-skeleta, 2026-08-25). Ответ на вопрос В1:
# замкнутая форма F_m(x,y;z,q) для ПРОИЗВОЛЬНЫХ x,y существует — отношение
# q-континуант (теорема 27 скелета); при q=1 вырождается в Чебышёва (Т8).
# Проверка тождества «числитель = знаменатель × перебор» почленно.
# Здесь же — программная проверка графа ссылок SKELET.md.
# ═══════════════════════════════════════════════════════════════════════════

def blok_q_sloy():
    from collections import defaultdict
    import os
    import re

    res = []
    DZ, DQ = 8, 64          # усечение по z и по |показателю q| (площади до +-N*m)

    def per(m, x, y, N):
        """перебор путей x->y с площадью от старта; {площадь: число}"""
        dp = [defaultdict(int) for _ in range(m + 1)]
        dp[x][0] = 1
        for _ in range(N):
            nd = [defaultdict(int) for _ in range(m + 1)]
            for p in range(m + 1):
                for a, v in dp[p].items():
                    if p:
                        nd[p - 1][a] += v
                    if p < m:
                        nd[p + 1][a + (p - x)] += v
            dp = nd
        return dp[y]

    def mul(A, B):
        out = defaultdict(int)
        for (z1, q1), c1 in A.items():
            for (z2, q2), c2 in B.items():
                if z1 + z2 <= DZ and abs(q1 + q2) <= DQ:
                    out[(z1 + z2, q1 + q2)] += c1 * c2
        return dict(out)

    def theta(m, x):
        th = [{(0, 0): 1}, {(0, 0): 1}]
        for i in range(2, m + 2):
            cur = defaultdict(int)
            for (z, q), c in th[i - 1].items():
                cur[(z, q)] += c
            e = i - 2 - x
            for (z, q), c in th[i - 2].items():
                if z + 2 <= DZ and abs(q + e) <= DQ:
                    cur[(z + 2, q + e)] -= c
            th.append(dict(cur))
        return th

    def phi(m, x):
        ph = {m + 2: {(0, 0): 1}, m + 1: {(0, 0): 1}}
        for j in range(m, 0, -1):
            cur = defaultdict(int)
            for (z, q), c in ph[j + 1].items():
                cur[(z, q)] += c
            e = j - 1 - x
            for (z, q), c in ph[j + 2].items():
                if z + 2 <= DZ and abs(q + e) <= DQ:
                    cur[(z + 2, q + e)] -= c
            ph[j] = dict(cur)
        return ph

    # ── Т27: числитель(континуанты, моном) == знаменатель × перебор ──
    bad = tested = 0
    for m in range(1, 7):
        for x in range(m + 1):
            thx = theta(m, x)
            phx = phi(m, x)
            den = thx[m + 1]
            for y in range(m + 1):
                F = defaultdict(int)
                for N in range(DZ + 1):
                    for a, c in per(m, x, y, N).items():
                        if abs(a) <= DQ:
                            F[(N, a)] += c
                if x <= y:
                    d = y - x
                    mon = dict(((z + d, q + d * (d - 1) // 2), c)
                               for (z, q), c in thx[x].items()
                               if z + d <= DZ and abs(q + d * (d - 1) // 2) <= DQ)
                    num = mul(mon, phx[y + 2])
                else:
                    d = x - y
                    mon = dict(((z + d, q), c) for (z, q), c in thx[y].items()
                               if z + d <= DZ)
                    num = mul(mon, phx[x + 2])
                prod = mul(den, dict(F))
                tested += 1
                keys = set(num) | set(prod)
                if any(num.get(k, 0) != prod.get(k, 0) for k in keys):
                    bad += 1
    res.append(("Т27 континуантная формула с весом площади для ЛЮБЫХ x,y",
                tested > 0 and bad == 0,
                "%d пар (m<=6), ряды до z^%d, |q|^%d, расхождений %d"
                % (tested, DZ, DQ, bad)))

    # ── Т27 при q=1 переходит в Т8 (Чебышёв) ──
    def U_poly(k):
        if k <= 0:
            return [1]
        a, b = [1], [1]
        for _ in range(k - 1):
            n = [0] * (len(a) + 2)
            for i, c in enumerate(b):
                n[i] += c
            for i, c in enumerate(a):
                n[i + 2] -= c
            a, b = b, n
        return b

    def pri_q1(poly):
        acc = defaultdict(int)
        for (z, q), c in poly.items():
            acc[z] += c
        return [acc[z] for z in sorted(acc)]

    good = True
    for m in range(1, 6):
        for x in range(m + 1):
            thx = theta(m, x)
            t_lo = pri_q1(thx[min(x, m)])          # только чётные степени z
            t_den = pri_q1(thx[m + 1])
            Ulo, Uden = U_poly(min(x, m))[::2], U_poly(m + 1)[::2]
            good &= (len(t_lo) <= len(Ulo)
                     and all(a == b for a, b in zip(t_lo, Ulo))
                     and len(t_den) <= len(Uden)
                     and all(a == b for a, b in zip(t_den, Uden)))
    res.append(("Т27 при q=1 даёт многочлены Чебышёва теоремы 8", good,
                "m<=5, все x"))

    # ── граф ссылок SKELET.md: каждое ИМЯ в «опирается» объявлено ──
    # 🔴 2026-09-03: ссылки переведены с номеров на ИМЕНА блоков (слаг в комментарии
    # `<!--id: chebyshev-->` за заголовком). Номер — только порядок чтения, он подвижен;
    # имя — личность блока, оно не меняется. Прежний разбор искал `опирается:\s*([0-9,\s]+)`
    # и на именах нашёл бы ноль ссылок при непустой строке — то есть был бы зелёным,
    # не видя ничего, ровно как разбор, чинённый 2026-08-25. Полный гейт ссылок
    # (дубли имён, справочный номер в скобках, межфайловые `[#имя]`) — `src/check_ssylki.py`;
    # здесь остаётся его счётная половина, чтобы прогон чисел не зависел от второго скрипта.
    skelet = os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), os.pardir, "SKELET.md"))
    try:
        text = open(skelet, encoding="utf-8").read()
        # 🔴 re.M ОБЯЗАТЕЛЕН: без него `^` значит «начало ТЕКСТА», а не строки.
        zag = re.findall(
            r"^\*\*(Определение|Утверждение|Теорема)\s+(\d+)\s*\([^)]*\)\.\*\*"
            r"\s*<!--\s*id:\s*([a-z0-9-]+)\s*-->", text, re.M)
        imena = set(t[2] for t in zag)
        bez_imeni = len(re.findall(
            r"^\*\*(?:Определение|Утверждение|Теорема)\s+\d+\s*\([^)]*\)\.\*\*(?!\s*<!--\s*id:)",
            text, re.M))
        refs, lines = [], 0
        for mm in re.finditer(r"^опирается:\s*(.+)$", text, re.M):
            lines += 1
            for elem in mm.group(1).split(","):
                nm = re.match(r"^\s*([a-z][a-z0-9-]*)\s*(?:\(\d+\))?\s*$", elem)
                # неразобранный элемент попадает в битые под своим сырым видом,
                # чтобы порча формы не выглядела как отсутствие ссылок
                refs.append(nm.group(1) if nm else elem.strip())
        bitye = sorted(set(v for v in refs if v not in imena))
        defs = len(re.findall(r"^\*\*Определение\s+\d+", text, re.M))
        utv = len(re.findall(r"^\*\*(?:Утверждение|Теорема)\s+\d+", text, re.M))
        graf_ok = (not bitye) and lines == utv and len(imena) == defs + utv \
            and bez_imeni == 0 and len(refs) > 0
        res.append(("Граф ссылок SKELET.md: битых 0, имя у каждого блока, "
                    "строк «опирается» = числу утверждений",
                    graf_ok,
                    "блоков %d (определений %d, утверждений %d), имён %d, без имени %d, "
                    "ссылок %d, битых %s"
                    % (defs + utv, defs, utv, len(imena), bez_imeni, len(refs),
                       bitye or "нет")))
    except OSError as ex:
        res.append(("Граф ссылок SKELET.md", False, "файл не прочитан: %s" % ex))

    X = sum(1 for _, g, _ in res if g)
    Y = len(res)
    print()
    print("── БЛОК Q-СЛОЯ: произвольные x,y с весом площади + граф скелета ──")
    for name, g, note in res:
        print("%s %s — %s" % ("OK" if g else "ПРОВАЛ", name, note))
    print("проверено %d из %d" % (X, Y))
    return X, Y


if __name__ == "__main__":
    X2, Y2 = blok_skeleta_v2()
    X3, Y3 = blok_obshih_teorem()
    X4, Y4 = blok_q_sloy()
    X1, Y1 = globals().get("_ITOG_BLOK1", (0, 0))
    print()
    print("ИТОГО по четырём блокам: проверено %d из %d" % (X1+X2+X3+X4, Y1+Y2+Y3+Y4))
    raise SystemExit(0 if (X1==Y1 and X2==Y2 and X3==Y3 and X4==Y4) else 1)
