# -*- coding: utf-8 -*-
"""Проверка задач, пришедших от исполнителя из книги, а не посчитанных самому."""
from itertools import combinations, permutations

def sep(t): print("\n" + "=" * 76); print(t); print("=" * 76)


# ============================================================================
# Д55. Четыре математика. Номера различны, двузначны, один равен сумме трёх.
# Никто, зная три чужих номера, не может вычислить свой.
# ============================================================================
def kandidaty(troe):
    """какие двузначные числа x могут стоять у человека, видящего troe"""
    p, q, r = troe
    out = set()
    # вариант 1: мой номер — сумма трёх увиденных
    s = p + q + r
    if 10 <= s <= 99 and s not in troe: out.add(s)
    # вариант 2: суммой является один из увиденных
    for bolshoy in (p, q, r):
        ostalnye = [y for y in troe if y is not bolshoy] if troe.count(bolshoy) == 1 \
                   else [y for y in troe]
        ost = list(troe); ost.remove(bolshoy)
        x = bolshoy - sum(ost)
        if 10 <= x <= 99 and x not in troe: out.add(x)
    return out

def matematiki():
    res = []
    for c in combinations(range(10, 100), 4):
        # ровно один равен сумме трёх других
        summy = [d for d in c if sum(x for x in c if x != d) == d]
        if len(summy) != 1: continue
        # никто не догадывается: у каждого минимум два кандидата
        if all(len(kandidaty(tuple(y for y in c if y != x))) >= 2 for x in c):
            res.append(c)
    return res


# ============================================================================
# Д44. Мафия. 2 мафиози, 2 мирных, 1 комиссар.
# Мафиози знают друг друга и всегда лгут. Комиссар знает всех, говорит правду.
# Мирные не знают ничьих ролей, говорят правду.
# ============================================================================
IM = ['Петя', 'Дима', 'Миша', 'Саша', 'Илья']

def mafia(chtenie_znayu):
    """chtenie_znayu: как читать фразу Саши «я знаю, что Миша комиссар»
       'znanie'  — истинна, только если Саша ЗНАЕТ роль Миши и Миша комиссар
       'fakt'    — истинна, если Миша комиссар (слово «знаю» не несёт нагрузки)"""
    good = []
    for roli in set(permutations(['M', 'M', 'G', 'G', 'K'])):
        r = dict(zip(IM, roli))
        def znaet_rol(kto, pro):
            if r[kto] == 'K': return True
            if r[kto] == 'M' and r[pro] == 'M': return True
            return False
        def govorit(kto, utv):
            return (not utv) if r[kto] == 'M' else utv
        # Петя: «я не знаю, кто Дима»
        if not govorit('Петя', not znaet_rol('Петя', 'Дима')): continue
        # Дима: «я знаю, кто комиссар» — знает только сам комиссар
        if not govorit('Дима', r['Дима'] == 'K'): continue
        # Миша: «я знаю, кто Петя»
        if not govorit('Миша', znaet_rol('Миша', 'Петя')): continue
        # Саша: «я знаю, что Миша — комиссар»
        utv = (znaet_rol('Саша', 'Миша') and r['Миша'] == 'K') \
              if chtenie_znayu == 'znanie' else (r['Миша'] == 'K')
        if not govorit('Саша', utv): continue
        good.append(r)
    return good


if __name__ == "__main__":
    sep("Д55. Четыре математика в одиночных камерах")
    r = matematiki()
    print(f"  наборов, где НИКТО не догадывается: {len(r)}")
    for c in r: print(f"    {c}   сумма-номер: {[d for d in c if sum(x for x in c if x != d) == d][0]}")
    print(f"\n  ВЕРДИКТ: ответ {'ЕДИНСТВЕННЫЙ' if len(r) == 1 else 'НЕ единственный — задача негодна в таком виде'}")

    sep("Д44. Мафия — два прочтения фразы Саши")
    for cht, opis in [('znanie', '«знаю» = знает роль И она такова'),
                      ('fakt',   '«знаю» не несёт нагрузки, важен только факт')]:
        g = mafia(cht)
        print(f"\n  Прочтение: {opis}")
        print(f"  согласованных раскладов: {len(g)}")
        for x in g: print("    ", {k: v for k, v in x.items()})
        if g:
            for im in IM:
                vse = sorted({x[im] for x in g})
                print(f"     {im:5}: " + ("ОДНОЗНАЧНО " + vse[0] if len(vse) == 1
                                          else "неоднозначно " + str(vse)))
