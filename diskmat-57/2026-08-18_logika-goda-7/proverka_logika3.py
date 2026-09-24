# -*- coding: utf-8 -*-
"""Третья проверка: добиваем оставшихся кандидатов."""
from itertools import permutations, product, combinations

def sep(t):
    print("\n" + "=" * 72); print(t); print("=" * 72)

IM = ['Аня', 'Боря', 'Вера', 'Гриша']


# ---- W1. Забег: каждый болельщик назвал ДВУХ РАЗНЫХ людей, угадал ровно одного.
#      Требуем: все 6 утверждений различны, упомянуты все четверо, решение единственно.
def zabeg_poisk():
    utv = [(i, m) for i in range(4) for m in range(1, 5)]
    pary = [p for p in combinations(utv, 2) if p[0][0] != p[1][0]]
    rass = list(permutations(range(1, 5)))
    good = []
    for nabor in combinations(pary, 3):
        vse = [u for p in nabor for u in p]
        if len(set(vse)) != 6: continue                  # все утверждения разные
        if len({u[0] for u in vse}) != 4: continue       # упомянуты все четверо
        resh = [r for r in rass
                if all(sum(r[u[0]] == u[1] for u in p) == 1 for p in nabor)]
        if len(resh) == 1:
            good.append((nabor, resh[0]))
    return good


# ---- W2. Цепочка делимостей: ровно k из утверждений верны.
def cepochka(delimosti=(2, 4, 12, 24), skolko_verno=2, do=2000):
    podhod = []
    for N in range(1, do + 1):
        v = [N % d == 0 for d in delimosti]
        if sum(v) == skolko_verno:
            podhod.append((N, tuple(i + 1 for i, x in enumerate(v) if x)))
    nabory = {p[1] for p in podhod}
    return nabory, podhod[:8]


# ---- W3. Шкатулки: ровно одна надпись верна.
def shkatulki():
    """З, С, Св. Надписи: A='портрет в З', B='портрет НЕ в С', C='портрет НЕ в З'."""
    res = []
    for mesto in ['З', 'С', 'Св']:
        A = (mesto == 'З')
        B = (mesto != 'С')
        C = (mesto != 'З')
        if A + B + C == 1: res.append((mesto, (A, B, C)))
    return res


# ---- W4. Шкатулки, вариант «ровно одна надпись ЛОЖНА».
def shkatulki2():
    res = []
    for mesto in ['З', 'С', 'Св']:
        A = (mesto == 'З'); B = (mesto != 'С'); C = (mesto != 'З')
        if (not A) + (not B) + (not C) == 1: res.append((mesto, (A, B, C)))
    return res


# ---- W5. Круглый стол: каждый «мой сосед справа — лжец». Какие n возможны?
def krug_sosed_sprava(n):
    cnt = 0
    for w in product([0, 1], repeat=n):
        if all((w[i] == 1) == (w[(i + 1) % n] == 0) for i in range(n)): cnt += 1
    return cnt


# ---- W6. Задуманное двузначное; четыре фразы, ровно три верны.
def dvuznachnoe(usl, skolko, lo=10, hi=99):
    res = []
    for N in range(lo, hi + 1):
        v = [f(N) for f in usl]
        if sum(v) == skolko: res.append((N, tuple(i + 1 for i, x in enumerate(v) if x)))
    return res


# ---- W7. «Наименьшее число вопросов да/нет, чтобы угадать одно из m»
def voprosy(m):
    k = 0
    while 2 ** k < m: k += 1
    return k


# ---- W8. Ряд n, каждый НЕ крайний: «мои соседи разных типов». МИНИМУМ рыцарей.
def ryad_min(n):
    best, primer = 10 ** 9, None
    dp = {(a, b): (a + b, [a, b]) for a, b in product([0, 1], repeat=2)}
    for i in range(2, n):
        nd = {}
        for (p, c), (k, seq) in dp.items():
            for nx in (0, 1):
                raznye = 1 if p != nx else 0
                if c != raznye: continue
                key = (c, nx); cand = (k + nx, seq + [nx])
                if key not in nd or nd[key][0] > cand[0]: nd[key] = cand
        dp = nd
    for (p, c), (k, seq) in dp.items():
        if k < best: best, primer = k, seq
    return best, primer


if __name__ == "__main__":
    sep("W1  забег: корректные наборы предсказаний")
    g = zabeg_poisk()
    print(f"  найдено корректных наборов: {len(g)}")
    for nabor, r in g[:3]:
        print("  --- вариант ---")
        for p in nabor:
            print("     · " + " / ".join(f"{IM[u[0]]} будет {u[1]}-м" for u in p))
        print("     ответ: " + ", ".join(f"{IM[i]}={r[i]}" for i in range(4)))

    sep("W2  цепочка делимостей 2 | 4 | 12 | 24, ровно ДВА утверждения верны")
    nab, prim = cepochka()
    print(f"  какие наборы верных утверждений вообще возможны: {sorted(nab)}")
    print(f"  примеры чисел: {prim}")
    nab3, prim3 = cepochka(skolko_verno=3)
    print(f"  при ТРЁХ верных: наборы {sorted(nab3)}, примеры {prim3[:5]}")

    sep("W3/W4  шкатулки")
    print(f"  ровно одна надпись ВЕРНА  -> {shkatulki()}")
    print(f"  ровно одна надпись ЛОЖНА  -> {shkatulki2()}")

    sep("W5  круглый стол «сосед справа — лжец»")
    for n in range(3, 13):
        print(f"  n={n:>2}: расстановок {krug_sosed_sprava(n)}")

    sep("W6  двузначное, четыре фразы, ровно три верны")
    usl = [lambda N: N % 3 == 0, lambda N: N % 4 == 0,
           lambda N: N % 5 == 0, lambda N: N % 9 == 0]
    r = dvuznachnoe(usl, 3)
    print(f"  «делится на 3 / 4 / 5 / 9», ровно три верны -> {r}")
    usl2 = [lambda N: N % 2 == 0, lambda N: N % 3 == 0,
            lambda N: N % 5 == 0, lambda N: N % 7 == 0]
    print(f"  «делится на 2 / 3 / 5 / 7», ровно три верны -> {dvuznachnoe(usl2, 3)[:12]}")

    sep("W7  вопросы да/нет")
    for m in (36, 52, 100, 1000):
        print(f"  чтобы отгадать один объект из {m:>4}: нужно {voprosy(m)} вопросов")

    sep("W8  ряд «соседи разных типов»: МИНИМУМ рыцарей")
    for n in (10, 30, 100):
        b, seq = ryad_min(n)
        s = ''.join('Р' if x else 'Л' for x in seq)
        print(f"  n={n:>3}: минимум рыцарей {b}  пример {s[:40]}{'...' if len(s) > 40 else ''}")
