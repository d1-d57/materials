# -*- coding: utf-8 -*-
"""Два кандидата на звёздочку-гроб ИМЕННО ПО ЛОГИКЕ, уровень 8-9 класса."""
from itertools import permutations, product

def sep(t): print("\n" + "=" * 78); print(t); print("=" * 78)


# ============================================================================
# A. СТРЕЛКИ. n жителей, каждый указал на одного другого и сказал «он лжец».
#    Каждый назван ровно один раз. Доказать, что рыцарей и лжецов поровну.
# ============================================================================
def strelki(n):
    vsego, ravno, raspr = 0, 0, set()
    for p in permutations(range(n)):
        if any(p[i] == i for i in range(n)): continue
        for w in product([1, 0], repeat=n):
            # i говорит «p(i) — лжец». Рыцарь говорит правду, лжец лжёт.
            if all((w[i] == 1) == (w[p[i]] == 0) for i in range(n)):
                vsego += 1
                k = sum(w)
                raspr.add(k)
                if k * 2 == n: ravno += 1
    return vsego, ravno, sorted(raspr)


# ============================================================================
# B. ДУМА. Дурак считает всех дураками, а себя умным.
#    Скромный умный про всех знает верно, а себя считает дураком.
#    Уверенный умный про всех знает верно и себя считает умным.
#    В зале N-1 депутат, каждый пишет, сколько в зале умных.
#    Премьер по анкетам ответа не понял. Вернулся N-й, заполнил анкету
#    про всю думу включая себя — и премьер понял. Сколько умных в думе?
# ============================================================================
def anketa_v_zale(tipy):
    """что напишет каждый из сидящих в зале. tipy: список 'D','S','U'"""
    umnyh = sum(1 for t in tipy if t in 'SU')
    out = []
    for t in tipy:
        if t == 'D': out.append(1)              # себя умным, всех дураками
        elif t == 'S': out.append(umnyh - 1)    # себя не считает
        else: out.append(umnyh)
    return tuple(sorted(out))

def duma(n_zal, max_perebor=9):
    """n_zal — сколько человек в зале. Возвращает: какие мультимножества анкет
       встречаются более чем у одного состава (премьер не понял)."""
    from collections import defaultdict
    vstrech = defaultdict(set)
    for tipy in product('DSU', repeat=n_zal):
        umnyh = sum(1 for t in tipy if t in 'SU')
        vstrech[anketa_v_zale(tipy)].add(umnyh)
    neodnozn = {a: sorted(u) for a, u in vstrech.items() if len(u) > 1}
    return neodnozn

def duma_final(n_zal):
    """после неоднозначной анкеты приходит путешественник.
       он пишет число умных ВО ВСЕЙ думе (зал + он сам) по своему типу.
       Ищем, при каких его ответах общее число умных M определяется однозначно."""
    from collections import defaultdict
    neodn = duma(n_zal)
    itog = defaultdict(set)
    for anketa, varianty_umnyh_v_zale in neodn.items():
        for uz in varianty_umnyh_v_zale:
            for t in 'DSU':
                M = uz + (1 if t in 'SU' else 0)
                if t == 'D': otvet = 1
                elif t == 'S': otvet = M - 1
                else: otvet = M
                itog[(anketa, otvet)].add(M)
    odnozn = sorted({list(v)[0] for k, v in itog.items() if len(v) == 1})
    return neodn, odnozn


if __name__ == "__main__":
    sep("A. СТРЕЛКИ — «он лжец», каждый назван ровно раз")
    print("   n | схем стрелок с решением | из них с равенством | какие числа рыцарей бывают")
    for n in range(2, 9):
        v, r, d = strelki(n)
        print(f"  {n:>2} | {v:>23} | {r:>19} | {d}")
    print("\n  ВЫВОД: при нечётном n решений НЕТ; при чётном во ВСЕХ решениях рыцарей ровно n/2.")
    print("  Значит утверждение «поровну» верно всегда, когда расстановка вообще существует.")

    sep("B. ДУМА — дураки, скромные и уверенные")
    for nz in (3, 4, 5, 6, 7):
        neodn, odnozn = duma_final(nz)
        print(f"  зал {nz:>2} чел.: неоднозначных анкет {len(neodn):>2} "
              f"-> после путешественника однозначно M = {odnozn}")
    print("\n  ПРОВЕРКА УСТОЙЧИВОСТИ: если ответ не зависит от размера зала,")
    print("  задачу можно давать с любым числом депутатов, в том числе с 200.")
