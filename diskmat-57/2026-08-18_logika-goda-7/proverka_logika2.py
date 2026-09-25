# -*- coding: utf-8 -*-
"""
Вторая проверка: ищем КОРРЕКТНЫЕ условия там, где придуманное не сработало,
и добиваем оставшихся кандидатов.
"""
from itertools import permutations, product, combinations
import random

def sep(t):
    print("\n" + "=" * 72); print(t); print("=" * 72)

IMENA = ['Аня', 'Боря', 'Вера', 'Гриша']


# ====================================================================
# Z1. «Каждый болельщик назвал два места, ровно одно угадал».
#     Ищем набор из трёх (или четырёх) предсказаний с ЕДИНСТВЕННЫМ решением.
# ====================================================================
def poisk_zabega(n=4, chislo_predskazanij=3):
    """утверждение = (кто, какое место). предсказание = пара утверждений."""
    utv = [(i, m) for i in range(n) for m in range(1, n + 1)]
    pary = [p for p in combinations(utv, 2)]
    rasstanovki = list(permutations(range(1, n + 1)))   # mesto[i]

    def verno(u, r): return r[u[0]] == u[1]

    najdeno = []
    for nabor in combinations(pary, chislo_predskazanij):
        resh = []
        for r in rasstanovki:
            if all(sum(verno(u, r) for u in p) == 1 for p in nabor):
                resh.append(r)
                if len(resh) > 1: break
        if len(resh) == 1:
            # отбрасываем вырожденные наборы: у каждого предсказания
            # две части должны быть про РАЗНЫХ людей — так интереснее
            if all(p[0][0] != p[1][0] for p in nabor):
                najdeno.append((nabor, resh[0]))
        if len(najdeno) >= 6: break
    return najdeno


# ====================================================================
# Z2. «Если я рыцарь, то P» — проверка табличкой истинности.
#     Говорящий x (Р/Л) произносит импликацию «x рыцарь -> P».
# ====================================================================
def implikaciya():
    print("  x=тип говорящего, P=есть ли золото. Импликация И = (x -> P).")
    print("  Условие согласованности: (x рыцарь и И истинна) ИЛИ (x лжец и И ложна)\n")
    for x in (1, 0):
        for P in (1, 0):
            I = (0 if (x == 1 and P == 0) else 1)      # x -> P
            soglas = (x == 1 and I == 1) or (x == 0 and I == 0)
            print(f"   говорящий={'рыцарь' if x else 'лжец ':6}  золото={'есть' if P else 'нет ':4}"
                  f"  высказывание={'истинно' if I else 'ложно ':7}  -> {'СОГЛАСОВАНО' if soglas else 'противоречие'}")


# ====================================================================
# Z3. Круглый стол, «хотя бы один из моих соседей — лжец». Сколько рыцарей max?
# ====================================================================
def krug_hotya_by_odin(n):
    best, primer = -1, None
    for a0, a1 in product([0, 1], repeat=2):
        dp = {(a0, a1): (a0 + a1, [a0, a1])}
        for i in range(2, n):
            nd = {}
            for (p, c), (k, seq) in dp.items():
                for nx in (0, 1):
                    est_lzhec = 1 if (p == 0 or nx == 0) else 0
                    if c != est_lzhec: continue
                    key = (c, nx); cand = (k + nx, seq + [nx])
                    if key not in nd or nd[key][0] < cand[0]: nd[key] = cand
            dp = nd
        for (p, c), (k, seq) in dp.items():
            el1 = 1 if (p == 0 or a0 == 0) else 0
            if c != el1: continue
            el0 = 1 if (c == 0 or a1 == 0) else 0
            if a0 != el0: continue
            if k > best: best, primer = k, seq
    return best, primer


# ====================================================================
# Z4. n жителей, каждый: «среди нас ровно k рыцарей» — все назвали РАЗНЫЕ k.
# ====================================================================
def raznye_chisla(n):
    """i-й сказал «рыцарей ровно i» (i = 1..n). Сколько рыцарей?"""
    res = []
    for k in range(n + 1):
        ok = True
        for i in range(1, n + 1):
            istinno = (k == i)
            # i-й рыцарь <=> его фраза истинна... но кто рыцарь, надо задать
            pass
        # рыцарями обязаны быть ровно те, чья фраза истинна
        rycari = [i for i in range(1, n + 1) if k == i]
        if len(rycari) == k: res.append((k, rycari))
    return res


# ====================================================================
# Z5. Шеренга: каждый «слева от меня рыцарей больше, чем справа».
# ====================================================================
def sherenga_bolshe(n):
    res = []
    for w in product([0, 1], repeat=n):
        ok = True
        for i in range(n):
            sl, sp = sum(w[:i]), sum(w[i + 1:])
            if w[i] != (1 if sl > sp else 0): ok = False; break
        if ok: res.append(w)
    return res


# ====================================================================
# Z6. Проверка задачи «дополнения» с другими числами
# ====================================================================
def dopolneniya(n, spisok):
    ne = [n - x for x in spisok]
    return n - sum(ne), ne, sum(ne)


if __name__ == "__main__":
    sep("Z1  забег: подбираем предсказания с ЕДИНСТВЕННЫМ решением")
    nd = poisk_zabega(4, 3)
    for nabor, r in nd[:4]:
        opis = []
        for p in nabor:
            opis.append(" / ".join(f"{IMENA[u[0]]} — {u[1]}-е" for u in p))
        print("  предсказания:")
        for o in opis: print(f"     · {o}")
        print(f"  единственное решение: " +
              ", ".join(f"{IMENA[i]}={r[i]}" for i in range(4)) + "\n")

    sep("Z2  «Если я рыцарь, то на острове есть золото»")
    implikaciya()

    sep("Z3  круглый стол: «хотя бы один мой сосед — лжец». Максимум рыцарей")
    for n in (9, 10, 12, 15, 20, 30):
        b, seq = krug_hotya_by_odin(n)
        s = ''.join('Р' if x else 'Л' for x in seq)
        print(f"  n={n:>2}: максимум рыцарей {b:>2}  пример {s}")

    sep("Z4  i-й сказал «рыцарей ровно i»")
    for n in (5, 10, 12):
        print(f"  n={n:>2}: согласованные (k, кто рыцарь) -> {raznye_chisla(n)}")

    sep("Z5  шеренга: «слева от меня рыцарей больше, чем справа»")
    for n in (3, 4, 5, 6, 7, 8):
        r = sherenga_bolshe(n)
        print(f"  n={n}: решений {len(r)}" +
              (f"  -> {[''.join('Р' if x else 'Л' for x in w) for w in r]}" if len(r) <= 4 else ""))

    sep("Z6  дополнения — варианты чисел для листка")
    for n, sp in [(100, (70, 75, 80, 85)), (100, (85, 80, 75, 70, 95)),
                  (50, (35, 40, 42, 45)), (30, (22, 24, 26, 27))]:
        v, ne, s = dopolneniya(n, sp)
        print(f"  n={n}, любят {sp}: не любят {ne} (сумма {s}) -> все сразу хотя бы {v}")
