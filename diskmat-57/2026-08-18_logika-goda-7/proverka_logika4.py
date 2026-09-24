# -*- coding: utf-8 -*-
"""
Четвёртая проверка — закрывает дыры, которые нашёл верификатор:
блоки, на которые ссылался пул, но которых в скриптах не было,
и главный дефект — тождество Л15 и Л16.
"""
from itertools import product, permutations
from collections import deque

def sep(t):
    print("\n" + "=" * 72); print(t); print("=" * 72)


# ====================================================================
# T1. ГЛАВНОЕ. Тождественны ли условия Л15 и Л16?
#     Л15: «мои соседи — люди РАЗНЫХ ТИПОВ»
#     Л16: «среди двух моих соседей РОВНО ОДИН рыцарь»
# ====================================================================
def tozhdestvo():
    print("  сосед1 сосед2 | «разных типов» | «ровно один рыцарь»")
    sovpalo = True
    for a, b in product([1, 0], repeat=2):
        raznye = (a != b)
        rovno1 = (a + b == 1)
        if raznye != rovno1: sovpalo = False
        print(f"    {'Р' if a else 'Л'}     {'Р' if b else 'Л'}    |      {str(raznye):5}     |       {str(rovno1):5}")
    print(f"\n  ВЫВОД: условия {'ТОЖДЕСТВЕННЫ' if sovpalo else 'различны'}")
    return sovpalo


# ====================================================================
# T2. Л16, полное строение решений на кольце. Блоки Р длины 2, блоки Л длины 1.
# ====================================================================
def kolco_stroenie(n):
    res = []
    for w in product([1, 0], repeat=n):
        ok = True
        for i in range(n):
            s = w[(i - 1) % n] + w[(i + 1) % n]
            if w[i] == 1 and s != 1: ok = False; break
            if w[i] == 0 and s == 1: ok = False; break
        if ok: res.append(''.join('Р' if x else 'Л' for x in w))
    return res


# ====================================================================
# T3. Л14 хамелеоны — BFS по достижимым состояниям
# ====================================================================
def hameleony(start=(13, 15, 17)):
    n = sum(start)
    seen = {start}; q = deque([start])
    odnocvetnye = []
    while q:
        s = q.popleft()
        if sorted(s) == [0, 0, n]: odnocvetnye.append(s)
        for i in range(3):
            for j in range(3):
                if i == j: continue
                k = 3 - i - j
                if s[i] > 0 and s[j] > 0:
                    t = list(s); t[i] -= 1; t[j] -= 1; t[k] += 2; t = tuple(t)
                    if t not in seen: seen.add(t); q.append(t)
    return len(seen), odnocvetnye, [x % 3 for x in start]


# ====================================================================
# T4. Л11 самоописывающая строка из десяти цифр
# ====================================================================
def samoopisanie():
    out = []
    def rec(pos, cur, ost):
        if pos == 10:
            if ost == 0 and all(cur[k] == cur.count(k) for k in range(10)):
                out.append(''.join(map(str, cur)))
            return
        for d in range(min(ost, 9) + 1):
            rec(pos + 1, cur + [d], ost - d)
    rec(0, [], 10)
    return out


# ====================================================================
# T5. Л13 развилка — таблица из четырёх строк
# ====================================================================
def razvilka():
    """вопрос: «правда ли, что на вопрос "эта дорога ведёт в город?"
       ты ответишь да?»  Лжец лжёт и про факт, и про свой будущий ответ."""
    rows = []
    for rycar in (True, False):
        for v_gorod in (True, False):
            pryamoy = v_gorod if rycar else (not v_gorod)      # как ответил бы на прямой вопрос
            istina_o_otvete = (pryamoy is True)                 # правда ли, что он ответит «да»
            otvet = istina_o_otvete if rycar else (not istina_o_otvete)
            rows.append((rycar, v_gorod, otvet, otvet == v_gorod))
    return rows


# ====================================================================
# T6. Л15 — посимвольная проверка примера на 100 человек
# ====================================================================
def primer_100(n=100):
    # узор РЛРРЛРР…: позиция 0 — Р, далее период ЛРР
    w = [1] + [(0 if (i - 1) % 3 == 0 else 1) for i in range(1, n)]
    bad = []
    for i in range(1, n - 1):
        raznye = 1 if w[i - 1] != w[i + 1] else 0
        if w[i] != raznye: bad.append(i)
    return sum(w), bad, ''.join('Р' if x else 'Л' for x in w)


# ====================================================================
# T7. Л7 — зависит ли вывод от симметричности дружбы?
# ====================================================================
def druzhba_napravlennaya(n):
    """если «дружу» НЕ взаимно: перебираем произвольные орграфы, n<=3"""
    par = [(i, j) for i in range(n) for j in range(n) if i != j]
    plohie = []
    for w in product([1, 0], repeat=n):
        R, L = sum(w), n - sum(w)
        if R > L: continue
        for m in product([0, 1], repeat=len(par)):
            out = [set() for _ in range(n)]
            for (e, b) in zip(par, m):
                if b: out[e[0]].add(e[1])
            ok = True
            for i in range(n):
                lzh = sum(1 for j in out[i] if not w[j])
                ryc = sum(1 for j in out[i] if w[j])
                if w[i] and lzh != 1: ok = False; break
                if (not w[i]) and ryc == 0: ok = False; break
            if ok: plohie.append((w, m)); break
        if plohie: break
    return plohie


if __name__ == "__main__":
    sep("T1  ТОЖДЕСТВО Л15 и Л16 — главный дефект, найденный верификатором")
    tozhdestvo()
    print("\n  сверка множеств решений на кольце (одно и то же условие, два вида записи):")
    for n in range(3, 13):
        a = set(kolco_stroenie(n))
        print(f"    n={n:>2}: решений {len(a):>2}  ->  {sorted(a)[:4]}{' …' if len(a) > 4 else ''}")

    sep("T2  Л16: строение решений — блоки РР через одиночные Л")
    for n in (9, 12, 15):
        r = kolco_stroenie(n)
        print(f"  n={n:>2}: расстановок {len(r)}  ->  {r}")

    sep("T3  Л14 хамелеоны 13/15/17 — BFS")
    k, odn, ost = hameleony()
    print(f"  достижимых состояний: {k}")
    print(f"  среди них одноцветных: {len(odn)}  {odn}")
    print(f"  остатки по модулю 3 в начале: {ost} — попарно различны, поэтому нулей два быть не может")

    sep("T4  Л11 самоописывающая строка")
    print(f"  решения: {samoopisanie()}")

    sep("T5  Л13 развилка — таблица четырёх случаев")
    print("   тип       дорога в город   ответ    совпало")
    for rycar, vg, otv, ok in razvilka():
        print(f"   {'рыцарь' if rycar else 'лжец  '}    {str(vg):5}            {str(otv):5}    {'ДА' if ok else 'НЕТ'}")

    sep("T6  Л15 — проверка примера на 100 человек посимвольно")
    k, bad, s = primer_100()
    print(f"  рыцарей в примере: {k}")
    print(f"  нарушений правила: {len(bad)}  {bad[:10]}")
    print(f"  начало строки: {s[:33]}…")
    print(f"  оценка сверху: 100 = 3*33 + 1  ->  33*2 + 1 = {33*2+1}")

    sep("T7  Л7 — что будет, если дружбу читать НЕ взаимной")
    for n in (3, 4):
        p = druzhba_napravlennaya(n)
        print(f"  n={n}: контрпример {'НАЙДЕН ' + str(p[0][0]) if p else 'не найден'}")
    print("  вывод: при направленном прочтении подсчёт ломается ->")
    print("  в условии или решении нужна явная взаимность дружбы")
