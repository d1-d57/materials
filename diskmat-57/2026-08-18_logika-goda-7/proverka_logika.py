# -*- coding: utf-8 -*-
"""
Перебор для кандидатов логического листка 23.09.
Каждый блок печатает ОТВЕТ и признак ЕДИНСТВЕННОСТИ.
Р = рыцарь (1), Л = лжец (0).
"""
from itertools import product, permutations, combinations
from functools import lru_cache

def sep(t):
    print("\n" + "=" * 72); print(t); print("=" * 72)


# ====================================================================
# K1. КРУГЛЫЙ СТОЛ: каждый — «среди моих двух соседей РОВНО ОДИН рыцарь»
#     ДП по кольцу с фиксацией первых двух элементов.
# ====================================================================
def krug_rovno_odin(n):
    """возвращает {число рыцарей: сколько расстановок}"""
    from collections import defaultdict
    itog = defaultdict(int)
    for a0, a1 in product([0, 1], repeat=2):
        # dp[(prev, cur)][k] = число способов продолжить
        dp = {(a0, a1): {a0 + a1: 1}}
        for i in range(2, n):
            nd = {}
            for (p, c), ks in dp.items():
                for nx in (0, 1):
                    # условие на человека c: соседи p и nx
                    sos = p + nx
                    if c == 1 and sos != 1: continue
                    if c == 0 and sos == 1: continue
                    key = (c, nx)
                    tgt = nd.setdefault(key, {})
                    for k, v in ks.items():
                        tgt[k + nx] = tgt.get(k + nx, 0) + v
            dp = nd
        # замыкание кольца: проверяем последних двух и первого
        for (p, c), ks in dp.items():
            # человек c (индекс n-1): соседи p (n-2) и a0
            sos = p + a0
            if c == 1 and sos != 1: continue
            if c == 0 and sos == 1: continue
            # человек a0 (индекс 0): соседи c (n-1) и a1
            sos0 = c + a1
            if a0 == 1 and sos0 != 1: continue
            if a0 == 0 and sos0 == 1: continue
            for k, v in ks.items():
                itog[k] += v
    return dict(itog)


# ====================================================================
# K2. РЯД из n. Каждый НЕ крайний: «мои соседи — разных типов».
#     Максимум рыцарей + пример.
# ====================================================================
def ryad_raznye(n):
    best, primer = -1, None
    # dp[(prev,cur)] = (максимум рыцарей среди первых i, пример)
    dp = {(a, b): (a + b, [a, b]) for a, b in product([0, 1], repeat=2)}
    for i in range(2, n):
        nd = {}
        for (p, c), (k, seq) in dp.items():
            for nx in (0, 1):
                raznye = 1 if p != nx else 0
                if c != raznye: continue      # c утверждает «соседи разные»
                key = (c, nx)
                cand = (k + nx, seq + [nx])
                if key not in nd or nd[key][0] < cand[0]: nd[key] = cand
        dp = nd
    for (p, c), (k, seq) in dp.items():
        if k > best: best, primer = k, seq
    return best, primer


# ====================================================================
# K3. Все n островитян: «число рыцарей среди нас ЧЁТНО»
# ====================================================================
def vse_chetno(n):
    good = []
    for k in range(n + 1):
        istinno = (k % 2 == 0)
        if k > 0 and not istinno: continue          # рыцарь не может лгать
        if (n - k) > 0 and istinno: continue        # лжец не может говорить правду
        good.append(k)
    return good


# ====================================================================
# K4. Каждый указал на одного другого: «он лжец». Каждый назван ровно раз.
# ====================================================================
def strelki(n):
    ok_perm, all_perm = 0, 0
    for p in permutations(range(n)):
        if any(p[i] == i for i in range(n)): continue
        all_perm += 1
        for w in product([0, 1], repeat=n):
            if all(w[i] != w[p[i]] for i in range(n)):
                ok_perm += 1; break
    return ok_perm, all_perm


# ====================================================================
# K5. n фраз: k-я гласит «на этом листке ровно k ложных фраз»
# ====================================================================
def frazy(n):
    res = []
    for w in product([0, 1], repeat=n):
        lozh = n - sum(w)
        if all(w[k - 1] == (1 if lozh == k else 0) for k in range(1, n + 1)):
            res.append([k for k in range(1, n + 1) if w[k - 1]])
    return res


# ====================================================================
# K6. Рыцарь / лжец / нормальный
# ====================================================================
def tri_tipa():
    res = []
    for roli in permutations(['R', 'L', 'N']):
        A, B, C = roli
        def mozhet(rol, istina):
            if rol == 'R': return istina
            if rol == 'L': return not istina
            return True
        if not mozhet(A, A == 'N'): continue
        if not mozhet(B, A == 'N'): continue
        if not mozhet(C, C != 'N'): continue
        res.append(roli)
    return res


# ====================================================================
# K7. Забег: три предсказания, в каждом ровно одна половина верна
# ====================================================================
def zabeg():
    res = []
    for m in permutations([1, 2, 3, 4]):
        A, B, C, D = m
        if ((A == 1) + (B == 3) == 1 and
            (B == 1) + (D == 4) == 1 and
            (C == 2) + (D == 3) == 1):
            res.append(dict(A=A, B=B, C=C, D=D))
    return res


# ====================================================================
# K8. Дополнения: n человек, несколько напитков
# ====================================================================
def napitki(n=100, lyubyat=(70, 75, 80, 85)):
    ne = [n - x for x in lyubyat]
    return n - sum(ne), ne


# ====================================================================
# K9. Дружба. Рыцарь: «я дружу ровно с одним лжецом».
#     Лжец: «я не дружу ни с одним рыцарем» (ложь -> дружит хотя бы с одним).
#     Проверяем утверждение «рыцарей строго больше» перебором графов, n<=6.
# ====================================================================
def druzhba(n):
    rebra = list(combinations(range(n), 2))
    kontr = []
    for w in product([0, 1], repeat=n):
        R, L = sum(w), n - sum(w)
        if R > L: continue                      # нас интересуют только контрпримеры
        for maska in product([0, 1], repeat=len(rebra)):
            g = [set() for _ in range(n)]
            for (e, m) in zip(rebra, maska):
                if m: g[e[0]].add(e[1]); g[e[1]].add(e[0])
            ok = True
            for i in range(n):
                lzh = sum(1 for j in g[i] if not w[j])
                ryc = sum(1 for j in g[i] if w[j])
                if w[i] and lzh != 1: ok = False; break
                if (not w[i]) and ryc == 0: ok = False; break
            if ok:
                kontr.append((w, maska)); break
        if kontr: break
    return kontr


if __name__ == "__main__":
    sep("K1  круглый стол: «среди моих соседей РОВНО ОДИН рыцарь»")
    for n in list(range(3, 16)) + [30]:
        d = krug_rovno_odin(n)
        if d:
            print(f"  n={n:>2}: рыцарей может быть {sorted(d)}   всего расстановок {sum(d.values())}")
        else:
            print(f"  n={n:>2}: РЕШЕНИЙ НЕТ")

    sep("K2  ряд: «мои соседи разных типов». Максимум рыцарей")
    for n in (10, 13, 16, 19, 25, 30, 99, 100):
        b, seq = ryad_raznye(n)
        s = ''.join('Р' if x else 'Л' for x in seq)
        print(f"  n={n:>3}: максимум рыцарей {b:>3}   пример {s[:40]}{'...' if len(s) > 40 else ''}")

    sep("K3  «число рыцарей среди нас чётно» — сказали ВСЕ n жителей")
    for n in (7, 10, 24, 25, 26):
        print(f"  n={n:>2}: допустимые числа рыцарей -> {vse_chetno(n)}")

    sep("K4  стрелки «он лжец», каждый назван ровно раз")
    for n in range(2, 9):
        ok, tot = strelki(n)
        print(f"  n={n}: перестановок без неподвижных точек {tot:>5}, из них согласуемых {ok:>5}")

    sep("K5  n фраз «на этом листке ровно k ложных»")
    for n in (5, 10, 12, 100):
        if n <= 12:
            print(f"  n={n:>3}: истинные фразы -> {frazy(n)}")
        else:
            # для больших n — прямой разбор: не более одной истинной
            r = [k for k in range(1, n + 1) if (n - 1) == k]
            print(f"  n={n:>3}: истинна ровно фраза номер {r} (ложных {n-1})")

    sep("K6  рыцарь / лжец / нормальный")
    print(f"  допустимые (A,B,C) = {tri_tipa()}")

    sep("K7  забег: в каждом предсказании ровно одна верная половина")
    print(f"  {zabeg()}")

    sep("K8  дополнения: 100 человек, 4 напитка 70/75/80/85")
    v, ne = napitki()
    print(f"  не любят: {ne}, сумма {sum(ne)}  ->  любят ВСЕ четыре хотя бы {v}")

    sep("K9  дружба: Р «ровно один друг-лжец», Л «нет друзей-рыцарей»")
    for n in (3, 5):
        k = druzhba(n)
        print(f"  n={n}: контрпример (лжецов >= рыцарей) — {'НАЙДЕН ' + str(k[0][0]) if k else 'НЕ НАЙДЕН'}")
