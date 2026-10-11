# final_verify.py — проверка ВСЕХ чисел и списков итоговой лестницы LESTNICA-PEREBOR.md
# Запуск: python3 final_verify.py ; каждая строка печатает OK/FAIL с id (id совпадают с §10 документа).
from collections import Counter
from itertools import combinations, permutations

res = []
def ok(cid, name, cond):
    res.append((cid, bool(cond)))
    print(("OK   " if cond else "FAIL ") + cid + "  " + name)

def isprime(n): return n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))
ds = lambda n: n // 10 + n % 10
TWO = range(10, 100)

# ---------- V: ДЗ 4 и список Васи ----------
hw = [n for n in TWO if isprime(ds(n))]
ok("V1", f"ДЗ 4: двузначных с простой суммой цифр = {len(hw)}", len(hw) == 33)
grp = [(s, sum(1 for n in hw if ds(n) == s)) for s in (2, 3, 5, 7, 11, 13, 17)]
ok("V2", f"кучки по сумме {grp} -> 2+3+5+7+8+6+2", [g[1] for g in grp] == [2, 3, 5, 7, 8, 6, 2])

VASYA = """85 76 38 43 20 58 14 50 89 49 83
65 56 30 94 16 41 23 67 92 25 32
34 47 52 61 25 11 12 29 74 98 21"""
rows = [list(map(int, r.split())) for r in VASYA.splitlines()]
v = [x for r in rows for x in r]
c = Counter(v)
ok("V3", f"список Васи: {len(v)} чисел, 3 строки по 11", len(v) == 33 and all(len(r) == 11 for r in rows))
ok("V4", f"повтор ровно один: {[k for k in c if c[k] > 1]}, разных {len(set(v))}",
   [k for k in c if c[k] > 1] == [25] and c[25] == 2 and len(set(v)) == 32)
ok("V5", f"пропуск ровно один: {sorted(set(hw) - set(v))}; лишних {sorted(set(v) - set(hw))}",
   sorted(set(hw) - set(v)) == [70] and not (set(v) - set(hw)))
pos25 = [(i + 1, r.index(25) + 1) for i, r in enumerate(rows) if 25 in r]
ok("V6", f"25 не в первой строке: (строка, столбец) = {pos25}", 25 not in rows[0] and pos25 == [(2, 10), (3, 5)])
s7v = [n for n in v if ds(n) == 7]
ok("V7", f"числа с суммой 7 у Васи в порядке чтения: {s7v}", s7v == [43, 16, 25, 34, 52, 61, 25])
srt = sorted(v); i = srt.index(67)
ok("V8", f"Вася по возрастанию вокруг 70: {srt[i-1:i+3]} (после 67 сразу 74)", srt[i:i + 2] == [67, 74])
right = {d: [n for n in hw if n // 10 == d] for d in range(1, 10)}
ok("V9", f"верные строки по первой цифре: {[len(right[d]) for d in range(1,10)]}",
   [len(right[d]) for d in range(1, 10)] == [4, 5, 4, 4, 4, 3, 3, 3, 3])
vrows = {d: sorted(n for n in v if n // 10 == d) for d in range(1, 10)}
bad = [d for d in range(1, 10) if vrows[d] != right[d]]
ok("V10", f"у Васи расходятся строки {bad}: 2 -> {vrows[2]}, 7 -> {vrows[7]}",
   bad == [2, 7] and vrows[2] == [20, 21, 23, 25, 25, 29] and vrows[7] == [74, 76])
ok("V11", f"строка 2 верно {right[2]}, строка 7 верно {right[7]}",
   right[2] == [20, 21, 23, 25, 29] and right[7] == [70, 74, 76])

# ---------- S: сумма цифр 7 и запас «отличаются на 6» ----------
s7 = [n for n in TWO if ds(n) == 7]
ok("S1", f"сумма цифр 7: {s7} ({len(s7)})", s7 == [16, 25, 34, 43, 52, 61, 70])
gaps = [b - a for a, b in zip(s7, s7[1:])]
ok("S2", f"«по возрастанию»: проверок до следующего {gaps}; от 61 до 70 — {70-61} (62…70)", gaps == [9] * 6)
ok("S3", f"после 70 чтобы сказать «всё» — проверить 71…99: {len(range(71,100))} чисел, ни одно не годится",
   len(range(71, 100)) == 29 and not [n for n in range(71, 100) if ds(n) == 7])
flips = sorted({n for n in s7 if n % 10 != 0} | {int(str(n)[::-1]) for n in s7 if n % 10 != 0})
ok("S4", f"«перевёртыши» 16/61, 25/52, 34/43 дают {len(flips)} и теряют 70 (07 не двузначное)",
   flips == [16, 25, 34, 43, 52, 61] and 70 not in flips)
ok("S5", "столбик «держу первую цифру»: 1→6 … 7→0; первая 8 или 9 — нет",
   [(n // 10, n % 10) for n in s7] == [(a, 7 - a) for a in range(1, 8)] and all(7 - a < 0 for a in (8, 9)))
d6 = [n for n in TWO if abs(n // 10 - n % 10) == 6]
ok("S6", f"запас «цифры отличаются на 6»: {d6} ({len(d6)})", d6 == [17, 28, 39, 60, 71, 82, 93])
p11 = []
x = 17
while x < 100 and abs(x // 10 - x % 10) == 6:
    p11.append(x); x += 11
ok("S7", f"ход «+11 от 17» даёт {p11}, у 50 разность {abs(5-0)}; теряет {len(d6)-len(p11)} из 7",
   p11 == [17, 28, 39] and len(d6) - len(p11) == 4)
cut6 = {a: [b for b in range(10) if abs(a - b) == 6] for a in range(1, 10)}
ok("S8", f"разрез по первой цифре: {cut6}",
   cut6 == {1: [7], 2: [8], 3: [9], 4: [], 5: [], 6: [0], 7: [1], 8: [2], 9: [3]})

# ---------- P: пары дежурных ----------
L4, L5 = "АБВГ", "АБВГД"
nf = lambda s: "".join(sorted(s, key=L5.index))
p4 = ["".join(t) for t in combinations(L4, 2)]
ok("P1", f"пары из 4: {p4} ({len(p4)})", p4 == ["АБ", "АВ", "АГ", "БВ", "БГ", "ВГ"])
robot = [a + b for a in L4 for b in L4 if a != b]
seen, first = set(), None
for k, s in enumerate(robot, 1):
    if nf(s) in seen and first is None: first = (k, s)
    seen.add(nf(s))
ok("P2", f"робот «Аня со всеми, Боря со всеми…»: {robot} — {len(robot)} записей, разных {len(seen)}, первый повтор {first}",
   len(robot) == 12 and len(seen) == 6 and first == (4, "БА")
   and robot == "АБ АВ АГ БА БВ БГ ВА ВБ ВГ ГА ГБ ГВ".split())
ok("P3", "у робота каждая пара ровно дважды", all(v_ == 2 for v_ in Counter(nf(s) for s in robot).values()))
fixed = [a + b for i, a in enumerate(L4) for b in L4[i + 1:]]
ok("P4", f"починка «с теми, кто после него»: {fixed} ({len(fixed)}); столбики 3+2+1, у Гены 0", fixed == p4)
ok("P5", "«дежурный и помощник» из 4 = 12 = ровно список робота",
   {"".join(t) for t in permutations(L4, 2)} == set(robot) and len(list(permutations(L4, 2))) == 12)
krug = ["АБ", "БВ", "ВГ", "ГА"]
ok("P6", f"«по кругу» на 4: {len(krug)} пары, пропущены {sorted(set(p4)-{nf(s) for s in krug})}",
   sorted(set(p4) - {nf(s) for s in krug}) == ["АВ", "БГ"])
p5 = ["".join(t) for t in combinations(L5, 2)]
ok("P7", f"пары из 5: {p5} ({len(p5)}); столбики 4+3+2+1",
   len(p5) == 10 and [sum(1 for p in p5 if p[0] == l) for l in "АБВГ"] == [4, 3, 2, 1])
nxt = lambda lst, a: lst[lst.index(a) + 1] if lst.index(a) + 1 < len(lst) else None
ok("P8", f"мяч: после АГ→{nxt(p5,'АГ')}, после АД→{nxt(p5,'АД')}, после БГ→{nxt(p5,'БГ')}, после ВД→{nxt(p5,'ВД')}, после ГД→{nxt(p5,'ГД')}",
   (nxt(p5, "АГ"), nxt(p5, "АД"), nxt(p5, "БГ"), nxt(p5, "ВД"), nxt(p5, "ГД")) == ("АД", "БВ", "БД", "ГД", None))

# ---------- R: робот буквален во всех проходах (правки верификации 05.10) ----------
def robot_run(rule):
    """rule(x, done) -> список вторых для x; done — уже обработанные «главные». Запись: буквы в порядке, как сказано."""
    out, done = [], []
    for x in L4:
        out += [x + y for y in rule(x, done)]
        done.append(x)
    return out
def stats(lst):
    seen, first = set(), None
    for k, s in enumerate(lst, 1):
        if nf(s) in seen and first is None: first = (k, s)
        seen.add(nf(s))
    return len(lst), len(seen), first
everyone = lambda x, done: [y for y in L4 if y != x]
ra = [nf(s) for s in robot_run(everyone)]     # «каждый со всеми» + «каждую пару пишем по алфавиту»
ok("R1", f"«каждый со всеми» + «пару пишем по алфавиту»: {ra} -> {stats(ra)} (повтор АБ на 4-м)",
   stats(ra) == (12, 6, (4, "АБ")))
part = lambda x, done: [y for y in L4 if y != x and not (x == "Б" and y == "А")]
rb = robot_run(part)                           # починка только для Бори
ok("R2", f"починка только для Бори: {rb} -> {stats(rb)} (снова ВА, ВБ; первый повтор ВА на 6-м)",
   stats(rb) == (11, 6, (6, "ВА")) and "ВА" in rb and "ВБ" in rb)
after = lambda x, done: [y for y in L4 if L4.index(y) > L4.index(x)]
rc = robot_run(after)
ok("R3", f"общая починка «с теми, кто после него»: {rc} ({len(rc)})", rc == p4)
notyet = lambda x, done: [y for y in L4 if y != x and y not in done]
rd = robot_run(notyet)
ok("R4", f"общая починка «кроме тех, кто уже был»: {rd} ({len(rd)})", rd == p4)
whole = sorted({nf(a + b) for a in L4 for b in L4 if a != b}, key=lambda s: (L4.index(s[0]), L4.index(s[1])))
ok("R5", f"«по алфавиту — вся пара» (внутри и между парами): {whole} — сразу 6, ловушки нет", whole == p4)
first_only = sorted((a + b for a in L4 for b in L4 if a != b), key=lambda s: L4.index(s[0]))
ok("R6", f"«по алфавиту — первые буквы»: {first_only[:5]}… первый повтор {stats(first_only)[2]}",
   stats(first_only)[2] == (4, "БА"))

# ---------- B: число бросков в запасных ходах ----------
t5 = ["".join(t) for t in combinations(L5, 3)]
ok("B1", f"тройки: мяч с АГД до «всё» = {len(t5)-t5.index('АГД')-1} записей + «всё» = {len(t5)-t5.index('АГД')} бросков",
   len(t5) - t5.index("АГД") == 5)
ok("B2", f"повтор мяча на парах из 4 (учитель говорит АБ): {len(p4)-1} записей + «всё» = {len(p4)} бросков", len(p4) == 6)
ok("B3", f"пары из 5, мяч сразу с АД: {len(p5)-p5.index('АД')-1} записей + «всё» = {len(p5)-p5.index('АД')} бросков",
   len(p5) - p5.index("АД") == 7)

# ---------- F: флаги ----------
order = "БКС"
flags = ["".join(t) for t in permutations(order)]  # permutations выдаёт в словарном порядке Б<К<С
ok("F1", f"флаги: {flags} ({len(flags)})", flags == ["БКС", "БСК", "КБС", "КСБ", "СБК", "СКБ"])
ok("F2", f"сетка верх×середина: 9 клеток, 3 запрещены (одинаковый цвет), рабочих {sum(1 for a in order for b in order if a!=b)}",
   sum(1 for a in order for b in order if a != b) == 6)
ok("F3", f"мяч: после БСК→{nxt(flags,'БСК')}, после КСБ→{nxt(flags,'КСБ')}, после СКБ→{nxt(flags,'СКБ')}",
   (nxt(flags, "БСК"), nxt(flags, "КСБ"), nxt(flags, "СКБ")) == ("КБС", "СБК", None))
sh, cur = ["БКС"], "БКС"
while True:
    cur = cur[1:] + cur[0]
    sh.append(cur)
    if cur == "БКС": break
ok("F4", f"сдвиг «верхнюю вниз» от БКС: {sh} — повтор на {len(sh)}-м броске, флагов {len(set(sh))} из 6",
   sh == ["БКС", "КСБ", "СБК", "БКС"] and len(set(sh)) == 3)
ok("F5", "КБС и БКС — разные записи (у флага есть места)", "КБС" != "БКС" and set("КБС") == set("БКС"))

# ---------- T: тройки из 5 ----------
t5 = ["".join(t) for t in combinations(L5, 3)]
ok("T1", f"тройки из 5: {t5} ({len(t5)})",
   t5 == "АБВ АБГ АБД АВГ АВД АГД БВГ БВД БГД ВГД".split())
ok("T2", "группы по первой букве 6+3+1", [sum(1 for t in t5 if t[0] == l) for l in "АБВ"] == [6, 3, 1])
ok("T3", f"мяч: после АБД→{nxt(t5,'АБД')}, после АГД→{nxt(t5,'АГД')}, после АВД→{nxt(t5,'АВД')}, после БВД→{nxt(t5,'БВД')}, после БГД→{nxt(t5,'БГД')}, после ВГД→{nxt(t5,'ВГД')}",
   (nxt(t5, "АБД"), nxt(t5, "АГД"), nxt(t5, "АВД"), nxt(t5, "БВД"), nxt(t5, "БГД"), nxt(t5, "ВГД"))
   == ("АВГ", "БВГ", "АГД", "БГД", "ВГД", None))
for lead, n in (("А", 6), ("Б", 3), ("В", 1)):
    tr = [t[1:] for t in t5 if t[0] == lead]
    rest = [p for p in p5 if L5.index(p[0]) > L5.index(lead)]
    ok("T4" + lead, f"мост: закрыть столбики пар до {lead} включительно -> {rest}; приписать {lead} = тройки с {lead} ({n})",
       tr == rest and len(tr) == n)
odo = [a + b + cc for i, a in enumerate(L5) for j, b in enumerate(L5[i + 1:], i + 1) for cc in L5[j + 1:]]
ok("T5", "«держим двух первых — меняем третьего» даёт тот же список", odo == t5)
comp = {t: "".join(l for l in L5 if l not in t) for t in t5}
ok("T6", f"ставка: троек {len(t5)} = пар {len(p5)}; «трое дежурят — двое отдыхают» — каждой тройке своя пара",
   len(t5) == len(p5) == 10 and sorted(comp.values()) == sorted(p5))
ok("T7", "АБВ и ВБА — одна тройка (одно множество)", set("АБВ") == set("ВБА"))

# ---------- K: палочки ----------
def tri(maxlen):
    return [(maxlen, m, s) for m in range(maxlen - 1, 0, -1) for s in range(m - 1, 0, -1) if m + s > maxlen]
k6 = tri(6)
ok("K1", f"палочки 1…6, наибольшая 6: {k6} ({len(k6)})", k6 == [(6, 5, 4), (6, 5, 3), (6, 5, 2), (6, 4, 3)])
flat = [(6, m, s) for m in range(5, 0, -1) for s in range(m - 1, 0, -1) if m + s == 6]
ok("K2", f"плоские (сумма меньших ровно 6): {flat}", flat == [(6, 5, 1), (6, 4, 2)])
all6 = [(6, m, s) for m in range(5, 0, -1) for s in range(m - 1, 0, -1)]
ok("K3", f"всех троек с шестёркой {len(all6)} (клеток в сетке средняя×меньшая), из них треугольников 4",
   len(all6) == 10)
ok("K4", f"с 6 впереди, без договорённости о записи: {2*len(k6)} записей на 4 тройки", 2 * len(k6) == 8)
bymid = {m: [t for t in k6 if t[1] == m] for m in (5, 4, 3)}
ok("K5", f"лесенка по средней: 5→{len(bymid[5])}, 4→{len(bymid[4])}, 3→{len(bymid[3])}",
   [len(bymid[m]) for m in (5, 4, 3)] == [3, 1, 0])
k6up = sorted(tuple(sorted(t)) for t in k6)
ok("K6", f"запись по возрастанию: {k6up} — тот же ответ 4", k6up == [(2, 5, 6), (3, 4, 6), (3, 5, 6), (4, 5, 6)])
k5 = tri(5)
ok("K7", f"запас: палочки 1…5, наибольшая 5: {k5} ({len(k5)})", k5 == [(5, 4, 3), (5, 4, 2)])
ok("K8", "6-4-5 и 6-5-4 — одна тройка", {6, 4, 5} == {6, 5, 4})

# ---------- G: сетки учителя (число рабочих клеток = ответ) ----------
grids = {"сумма 7": len(s7), "пары из 4": len(p4), "пары из 5": len(p5), "флаги": len(flags),
         "тройки из 5": len(t5), "палочки 6": len(k6), "палочки 5": len(k5), "разность 6": len(d6)}
ok("G1", f"рабочих клеток: {grids}",
   list(grids.values()) == [7, 6, 10, 6, 10, 4, 2, 7])

# ---------- H: хронометраж ----------
plan = [("0", 1.5), ("1", 3.5), ("2", 5.5), ("3", 2), ("4", 5), ("5", 1.5), ("6", 4)]
t, marks = 0, []
for s, m in plan:
    t += m; marks.append(t)
ok("H1", f"план {sum(m for _, m in plan)} мин, контрольные точки {marks}, резерв {25-sum(m for _, m in plan)}",
   sum(m for _, m in plan) == 23 and marks == [1.5, 5.0, 10.5, 12.5, 17.5, 19.0, 23.0])

n_ok = sum(1 for _, b in res if b)
print(f"\nИТОГО: {n_ok} из {len(res)} OK")
