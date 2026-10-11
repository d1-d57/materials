"""G. Каталоги детских правил: что получится при ЧЕСТНОМ исполнении каждого правила.
Для каждого правила: последовательность записей, как её выписал бы ребёнок, исполняющий правило буквально;
вердикт: РАБОТАЕТ (все, без повторов, следующее единственно) / ПОВТОР / ПРОПУСК / НЕДОПУСТИМЫЙ / НИЧЬЯ (следующее не определено)."""
from itertools import combinations, product, permutations
from collections import Counter, deque

NRULES = 0
def verdict(tag, rule, seq, canon, universe, ties=None, show=True, note=""):
    """seq — записи в порядке выписывания; canon(x) -> канонический объект или None (недопустимый)."""
    global NRULES; NRULES += 1
    cs = [canon(x) for x in seq]
    bad = [x for x, c in zip(seq, cs) if c is None or c not in universe]
    good = [c for c in cs if c is not None and c in universe]
    cnt = Counter(good)
    reps = sum(m - 1 for m in cnt.values())
    miss = [u for u in universe if u not in cnt]
    v = []
    if bad: v.append(f"НЕДОПУСТИМЫЕ {len(bad)}")
    if reps: v.append(f"ПОВТОРЫ {reps}")
    if miss: v.append(f"ПРОПУСК {len(miss)}")
    if ties: v.append(f"НИЧЬЯ (следующее не определено): {ties}")
    if not v: v = ["РАБОТАЕТ"]
    print(f"  [{tag}] {rule}\n      записей {len(seq)}, различных {len(cnt)} из {len(universe)} → {'; '.join(v)} {note}")
    if show: print("      " + ", ".join(map(str, seq)))
    if miss: print("      пропущены: " + ", ".join(map(str, miss)))
    if bad: print("      недопустимые: " + ", ".join(map(str, bad)))

def groups_ties(objs, key):
    c = Counter(key(o) for o in objs)
    return {k: m for k, m in sorted(c.items()) if m > 1}

# ============ K1: разложения 6 ============
def parts(n, mx=None):
    mx = n if mx is None else mx
    if n == 0: yield (); return
    for a in range(min(n, mx), 0, -1):
        for r in parts(n - a, a): yield (a,) + r
def comps(n):
    if n == 0: yield (); return
    for a in range(1, n + 1):
        for r in comps(n - a): yield (a,) + r
P6 = list(parts(6)); S = lambda t: '+'.join(map(str, t)); nf = lambda t: tuple(sorted(t, reverse=True))
cP = lambda s: nf(tuple(int(x) for x in s.split('+')))
print("=== K1 · разложения 6 (11) ===")
verdict("K1-1", "«по возрастанию первого слагаемого», записи как придут в голову (без НФ) — честно: все суммы с 1, потом с 2…",
        [S(c) for c in sorted(comps(6))], cP, P6, show=False,
        note="(записей-с-порядком 32 — это все «композиции» 6)")
nums = sorted(P6, key=lambda t: int(''.join(map(str, t))))
verdict("K1-2", "НФ «от больших к меньшим», потом «по возрастанию» — запись читаем как число (6, 33, 42, 51, 222…)",
        [S(t) for t in nums], cP, P6)
asc = sorted(tuple(sorted(t)) for t in P6)
verdict("K1-3", "НФ «от меньших к большим» (1+1+4) и «по возрастанию» как в словаре",
        [S(t) for t in asc], cP, P6)
by_len_any = sorted(P6, key=len)
verdict("K1-4", "«по количеству слагаемых» (сначала из одного, из двух…), внутри группы — как придёт",
        [S(t) for t in by_len_any], cP, P6, ties=groups_ties(P6, len))
verdict("K1-5", "«сначала самое большое слагаемое» (6, потом с пятёркой, с четвёркой…), при равном — как придёт",
        [S(t) for t in P6], cP, P6, ties=groups_ties(P6, lambda t: t[0]),
        note="(с добавкой «при равном — по второму» → РАБОТАЕТ, это и есть НФ-порядок банка)")
# отщипываем единичку от последнего неединичного
seq = [(6,)]
while True:
    t = list(seq[-1]); i = max((j for j, x in enumerate(t) if x > 1), default=None)
    if i is None: break
    t[i] -= 1; t.append(1); seq.append(nf(tuple(t)))
verdict("K1-6", "«меняем по чуть-чуть»: от 6 каждый раз отщипываем единичку", [S(t) for t in seq], cP, P6)
# переливание: для k слагаемых стартуем с (n-k+1,1,...,1), перекладываем по 1 из первого во второе, пока первое > 1
seq = []
for k in range(1, 7):
    t = [6 - k + 1] + [1] * (k - 1); seq.append(tuple(t))
    while k >= 2 and t[0] > 1:
        t[0] -= 1; t[1] += 1; seq.append(tuple(t))
verdict("K1-7", "«перекладываем по одному»: для двух слагаемых 5+1→4+2→3+3→2+4…, для трёх 4+1+1→3+2+1→2+3+1…",
        [S(t) for t in seq], cP, P6)
# дерево «разбиваем одно слагаемое на два» — честно пишем каждый результат
seq = []; q = deque([(6,)]); seen = set()
while q:
    t = q.popleft()
    if t in seen: continue
    seen.add(t)
    for i, x in enumerate(t):
        if i and t[i] == t[i - 1]: continue
        for b in range(1, x // 2 + 1):
            u = nf(t[:i] + (x - b, b) + t[i + 1:]); seq.append(u); q.append(u)
verdict("K1-8", "«разбиваем»: из каждого записанного разбиваем одно слагаемое на два всеми способами и записываем",
        [S((6,))] + [S(t) for t in seq], cP, P6, show=False)
print("  [K1-9] «как придёт, но каждое новое сверяем со всеми» — повторов нет, если сверять сортировкой в уме;\n"
      "      пропуск НЕ ловится (нечем); «следующее» не определено → мяч невозможен. (не моделируется: недетерминировано)")
NRULES += 1

# ============ K3: 9 рублей монетами 1, 2, 5 ============
C9 = [t for t in parts(9) if set(t) <= {1, 2, 5}]
print("\n=== K3 · 9 рублей монетами 1, 2, 5 (8) ===")
cC = lambda s: nf(tuple(int(x) for x in s.split('+')))
verdict("K3-1", "«по убыванию пятёрок, при равном — по убыванию двушек» (как в ДЗ к 29.09)",
        [S(t) for t in sorted(C9, key=lambda t: (-t.count(5), -t.count(2)))], cC, C9)
verdict("K3-2", "«по числу монет, от меньшего»", [S(t) for t in sorted(C9, key=len)], cC, C9, ties=groups_ties(C9, len))
k1 = sorted(C9, key=lambda t: t.count(1))
verdict("K3-3", "«по числу рублёвых монет, от меньшего»", [S(t) for t in k1], cC, C9,
        ties=groups_ties(C9, lambda t: t.count(1)), note=f"(число рублёвых: {[t.count(1) for t in k1]} — 6 и 8 нет!)")
verdict("K3-4", "«по возрастанию» — НФ от больших к меньшим, запись читаем как число (522, 5211, …)",
        [S(t) for t in sorted(C9, key=lambda t: int(''.join(map(str, t))))], cC, C9)
verdict("K3-5", "«сначала самая крупная монета» (все с пятёркой, потом с двушкой), внутри — как придёт",
        [S(t) for t in C9], cC, C9, ties=groups_ties(C9, lambda t: t[0]))
seq = [(1,) * 9]
while True:
    t = list(seq[-1])
    if t.count(1) < 2: break
    t.remove(1); t.remove(1); t.append(2); seq.append(nf(tuple(t)))
verdict("K3-6", "«начинаю с рублей и меняю две рублёвые на двушку», пока можно", [S(t) for t in seq], cC, C9)
seq = []; q = deque([(5, 2, 2)]); seen = set(); seq.append((5, 2, 2))
SPL = {5: [(2, 2, 1), (2, 1, 1, 1), (1,) * 5], 2: [(1, 1)]}
while q:
    t = q.popleft()
    if t in seen: continue
    seen.add(t)
    for x in set(t):
        if x == 1: continue
        for sp in SPL[x]:
            u = list(t); u.remove(x); u = nf(tuple(u) + sp); seq.append(u); q.append(u)
verdict("K3-7", "«размениваю»: из каждого записанного меняю одну монету на мелкие всеми способами и записываю",
        [S(t) for t in seq], cC, C9, show=False)

# ============ K4: трое дежурных из пятерых ============
L = "АБВГД"; T = [''.join(c) for c in combinations(L, 3)]; cT = lambda s: ''.join(sorted(s))
print("\n=== K4 · трое дежурных из пятерых (10) ===")
verdict("K4-1", "«по алфавиту»: в команде буквы по алфавиту, команды — как в словаре", T, cT, T)
seq = [''.join(c) for p in L for c in combinations(L, 3) if p in c]
verdict("K4-2", "«сначала все с Аней, потом все с Борей, …» — буквально, без «кроме уже бывших»", seq, cT, T, show=False)
seq = []; used = set()
for p in L:
    for c in combinations(L, 3):
        if p in c and not (set(c) & used): seq.append(''.join(c))
    used.add(p)
verdict("K4-3", "то же, но «с Борей — без Ани, она уже была»", seq, cT, T)
out = [''.join(c) for c in combinations(L, 2)]
verdict("K4-4", "«кого НЕ берём»: пары оставшихся по алфавиту (без БВ = АГД, …)",
        [''.join(sorted(set(L) - set(o))) for o in out], cT, T, note="(сами пары: " + ' '.join(out) + ")")
rot = lambda s: ''.join(L[(L.index(ch) + 1) % 5] for ch in s)
seq = ["АБВ"]
for _ in range(4): seq.append(rot(seq[-1]))
verdict("K4-5", "«сдвиг по кругу»: каждого заменяем на следующего (Д → А)", seq, cT, T)
seq2 = seq + ["АБГ"]
for _ in range(4): seq2.append(rot(seq2[-1]))
verdict("K4-5b", "то же, но после остановки — второй круг от АБГ", seq2, cT, T,
        note="(два круга покрывают всё; но «с чего начать второй круг» — правило не говорит)")
# меняем одного: заменяем самого «позднего» по алфавиту участника на самого раннего свободного, дающего новую команду
seq = ["АБВ"]; seen = {"АБВ"}
while True:
    cur = seq[-1]; nxt = None
    for out_p in sorted(cur, reverse=True):
        for in_p in L:
            if in_p in cur: continue
            cand = cT(cur.replace(out_p, in_p))
            if cand not in seen: nxt = cand; break
        if nxt: break
    if not nxt: break
    seq.append(nxt); seen.add(nxt)
verdict("K4-6", "«меняем по одному человеку»: заменяем одного на свободного, чтобы получилась новая команда (жадно, без возвратов)",
        seq, cT, T)
verdict("K4-7", "«по самому старшему по алфавиту» (сначала команды, где последний — В, потом Г, потом Д), внутри — как придёт",
        sorted(T, key=lambda s: s[-1]), cT, T, ties=groups_ties(T, lambda s: s[-1]))

# ============ Ч.3: флаги, 3 полосы, Б К С, соседние разные ============
F = [''.join(w) for w in product('БКС', repeat=3) if w[0] != w[1] and w[1] != w[2]]
cF = lambda s: s if s in F else None
print("\n=== Ч3 · флаги: три полосы из Б, К, С, соседние полосы разного цвета (12) ===")
verdict("F-1", "«как в словаре»: договорились Б < К < С, сравниваем по верхней, при равной — по средней…", F, cF, F)
verdict("F-2", "«по верхней полосе» (сначала все с белым верхом…), внутри — как придёт", F, cF, F,
        ties=groups_ties(F, lambda s: s[0]))
seq = ["БКС"]; r = lambda s: s[-1] + s[:-1]
for _ in range(2): seq.append(r(seq[-1]))
s2 = ["БКБ"]
for _ in range(2): s2.append(r(s2[-1]))
verdict("F-3", "«сдвиг по кругу» (нижняя полоса уходит наверх): от БКС и от БКБ", seq + s2, lambda s: s if s in F else ('?' if len(set(s)) else None), F)
rev = []
for f in F:
    if f[::-1] not in rev and f not in rev: rev += [f, f[::-1]] if f != f[::-1] else [f]
verdict("F-4", "«переворачиваем флаг»: пишем флаг и сразу его перевёрнутый", rev, cF, F,
        note="(пары «флаг–перевёртыш»; симметричные БКБ… без пары; порядок пар не задан → НИЧЬЯ между парами)")
sym = [f for f in F if f[0] == f[2]]; asym = [f for f in F if f[0] != f[2]]
verdict("F-5", "«сначала с одинаковыми краями, потом все три разные»", sym + asym, cF, F,
        ties={"края равны": len(sym), "все разные": len(asym)})
seq = ["БКБ"]; seen = {"БКБ"}
while True:
    cur = seq[-1]; nxt = None
    for pos in (2, 1, 0):
        for col in "БКС":
            cand = cur[:pos] + col + cur[pos + 1:]
            if cand != cur and cand in F and cand not in seen: nxt = cand; break
        if nxt: break
    if not nxt: break
    seq.append(nxt); seen.add(nxt)
verdict("F-6", "«меняем одну полосу» (сначала нижнюю, если нельзя — среднюю, потом верхнюю; жадно, без возвратов)",
        seq, cF, F)
verdict("F-7", "«по средней полосе» (сначала все с белой серединой…), при равной — по верхней",
        sorted(F, key=lambda s: (s[1], s[0], s[2])), cF, F,
        note="(без «при равной — …» — НИЧЬЯ по 4 в группе)")
print("  после-X для F-1 (словарный): ", {x: F[i + 1] for i, x in enumerate(F[:-1]) if x[1:] in ("СК", "КС", "СБ", "БС", "СС") or x[2] == 'С'})

# ============ запас к ч.3: полоска 1x6 из квадратиков (1) и доминошек (2) ============
D = [c for c in comps(6) if set(c) <= {1, 2}]
cD = lambda s: tuple(int(x) for x in s.split('+'))
Ds = [S(c) for c in D]
print("\n=== Ч3-запас · полоска 1×6 из клеток 1 и доминошек 2 (13) ===")
verdict("D-1", "«как в словаре» (1 раньше 2): 1+1+1+1+1+1, 1+1+1+1+2, …", [S(c) for c in sorted(D)], cD, D)
verdict("D-2", "«по числу доминошек», внутри — как придёт", [S(c) for c in sorted(D, key=lambda c: c.count(2))], cD, D,
        ties=groups_ties(D, lambda c: c.count(2)))
verdict("D-3", "«по числу доминошек, внутри — где стоит первая доминошка (слева направо)»",
        [S(c) for c in sorted(D, key=lambda c: (c.count(2), [i for i, x in enumerate(c) if x == 2][:1]))], cD, D,
        ties={k: v for k, v in groups_ties(D, lambda c: (c.count(2), tuple(
            sum(c[:i]) for i, x in enumerate(c) if x == 2)[:1])).items()})
print(f"\nВСЕГО правил в каталогах: {NRULES}")
