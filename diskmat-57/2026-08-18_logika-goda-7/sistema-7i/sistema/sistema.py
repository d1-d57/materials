# -*- coding: utf-8 -*-
"""🗄 ЗАМЕНЕНО 11.10: аватар считается в боте, `bot-7i/bot7i/avatary.py`, по выгрузке бота; этот расчёт — только для истории и регрессии.

Система учёта 7И: статусы навыков (3 модели), кластеры по теме (4 уровня), группы и ДЗ на следующую пару.
Запуск:  python3 sistema.py [папка_данных]
  1) adapter.py собирает dannye/*.csv из выгрузок (через импорт ../navyki/navyki.py и ../klaster/klaster.py, их не меняя);
  2) движок dvizhok.py читает ТОЛЬКО dannye/*.csv;
  3) печать списков на пару + SISTEMA-chernovik.md рядом. Все числа отчёта считает этот файл.
Метки: [F] посчитано · [M] допущение · [H] гипотеза."""
import os, sys, statistics as st
from collections import Counter, defaultdict, OrderedDict
from datetime import date, timedelta

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import adapter, dvizhok as D

DATA = sys.argv[1] if len(sys.argv) > 1 else None
N = adapter.build(DATA)                    # пишет dannye/*.csv; N — модуль navyki (с K = klaster) для сверки
K = N.K
B = D.Baza()
SK = list(B.navyki); MIN = B.MIN; EXT = [k for k in SK if k not in MIN]
FIO = B.deti; IDS = list(FIO)
fam = lambda c: FIO[c].split()[0]
CP = OrderedDict([('22.09', (date(2026, 9, 22), 9)), ('29.09', (date(2026, 9, 29), 9)), ('6.10', (date(2026, 10, 6), 9))])
C3 = CP['6.10']; C2 = CP['29.09']
NEXT = date(2026, 10, 13)
xs_ = lambda c, sk, cut=None: B.upto(B.by[(c, sk)], cut)
pc = lambda a, b: f'{a}/{b}' if b else '—'
pp = lambda a, b: f'{round(100 * a / b)}%' if b else '—'
f2 = lambda x: '—' if x is None else f'{x:.2f}'.replace('.', ',')


# ---------------- статусы трёх моделей ----------------
def statusy(cut, model='L', **kw):
    out = {}
    for c in IDS:
        for sk in SK:
            xs = xs_(c, sk, cut)
            if model == 'L': out[(c, sk)] = D.lestnica(xs, **kw)
            elif model == 'W': out[(c, sk)] = D.vzves(xs, cut[0], **kw)[0]
            else: out[(c, sk)] = D.bkt(xs, **kw)[0]
    for r in B.ruchnye:                                 # ручная правка Вани главнее модели
        if r['chto'] == 'status' and (r['rebyonok'], r['klyuch']) in out: out[(r['rebyonok'], r['klyuch'])] = r['znachenie']
    return out


ST = {(m, cp): statusy(cut, m) for m in 'LWB' for cp, cut in CP.items()}
MN = {'L': 'лестница', 'W': 'взвешенный счёт', 'B': 'BKT'}

# ---------------- 1. сравнение моделей ----------------
dist = {m: Counter(ST[(m, '6.10')][(c, sk)] for c in IDS for sk in SK) for m in 'LWB'}
distmin = {m: Counter(ST[(m, '6.10')][(c, sk)] for c in IDS for sk in MIN) for m in 'LWB'}
ge = lambda g: g in ('С', 'У')
def agree(a, b, cp='6.10', fn=lambda g: g):
    X, Y = ST[(a, cp)], ST[(b, cp)]
    return sum(fn(X[k]) == fn(Y[k]) for k in X), len(X)
stab = {m: sum(ST[(m, '29.09')][k] != ST[(m, '6.10')][k] for k in ST[(m, '6.10')]) for m in 'LWB'}
# BKT: «сам»/«уверенно» без единого самостоятельного наблюдения
bkt_nosam = sum(1 for c in IDS for sk in SK if ge(D.bkt(xs_(c, sk, C3))[0]) and not D.bkt(xs_(c, sk, C3))[3])
w_nosam = sum(1 for c in IDS for sk in SK if ge(D.vzves(xs_(c, sk, C3), C3[0])[0]) and not any(x['mode'] == 'sam' for x in xs_(c, sk, C3)))


# чувствительность к параметрам: доля ячеек (28×6), меняющих оценку
def sens(model, variants):
    base = ST[(model, '6.10')]; res = []
    for name, kw in variants:
        alt = statusy(C3, model, **kw); res.append((name, sum(alt[k] != base[k] for k in base)))
    return res
SENS_L = sens('L', [('порог 1/2', dict(porog=1 / 2)), ('порог 1 (всё верно)', dict(porog=1.0)), ('пусто на КР = нет данных', dict(blank_fail=False))])
def m2(**ch):
    p = dict(D.M2P); p['W'] = dict(D.M2P['W']);
    for k, v in ch.items():
        if k in ('sam', 'pomosch', 'dom'): p['W'][k] = v
        else: p[k] = v
    return dict(par=p)
SENS_W = sens('W', [('вес приёма 0,2', m2(pomosch=0.2)), ('вес приёма 0,5', m2(pomosch=0.5)), ('вес ДЗ 0', m2(dom=0.0)), ('вес ДЗ 0,3', m2(dom=0.3)),
                    ('полураспад 14 дн', m2(HL=14)), ('полураспад 42 дн', m2(HL=42)), ('априор A0 = 1', m2(A0=1.0)), ('априор A0 = 4', m2(A0=4.0))])
grid = []
for gs in (0.1, 0.25):
    for ss in (0.05, 0.2):
        for T in (0.05, 0.3):
            for L0 in (0.2, 0.5):
                for gp in (0.4, 0.75):
                    p = dict(L0=L0, T=T, g={'sam': gs, 'pomosch': gp, 'dom': 0.75}, s={'sam': ss, 'pomosch': 0.05, 'dom': 0.05})
                    grid.append((f'g={gs} s={ss} T={T} L0={L0} gп={gp}', dict(par=p)))
SENS_B = sens('B', grid)
sb = sorted(n for _, n in SENS_B)


# сколько наблюдений нужно: синтетические ряды, событие раз в неделю
def synth(seq):
    """seq: список событий [(режим, 'ВВН…')]; возвращает оценки трёх моделей после каждого события."""
    xs, out = [], []
    d0 = date(2026, 9, 1)
    for i, (mode, vs) in enumerate(seq):
        d = d0 + timedelta(days=7 * i)
        for j, v in enumerate(vs):
            xs.append(dict(c='x', ev=f'e{i}', p=str(j), v='+' if v == 'В' else '-', skill='s', lvl='○', ob=True, mode=mode, tip='KR', d=d, seq=(d, 0)))
        out.append((D.lestnica(xs), D.vzves(xs, d)[0], D.bkt(xs)[0]))
    return out
SYN = OrderedDict([
    ('КР раз в неделю, 2 пункта, всё верно', synth([('sam', 'ВВ')] * 3)),
    ('КР раз в неделю, 1 пункт, всё верно', synth([('sam', 'В')] * 3)),
    ('только приём (с помощью), 2 пункта, всё верно', synth([('pomosch', 'ВВ')] * 4)),
    ('две КР верно, третья — 0 из 2', synth([('sam', 'ВВ'), ('sam', 'ВВ'), ('sam', 'НН')])),
    ('КР провал, потом приём верно, потом КР верно', synth([('sam', 'НН'), ('pomosch', 'ВВ'), ('sam', 'ВВ')])),
])

# предсказание: состояние на 29.09 (до пары 6.10) → сдал ли навык на ○ КР 6.10
KR06 = 'KR-2026-10-06'
def y06(c, sk):
    ev = D.events([x for x in B.by[(c, sk)] if x['ev'] == KR06 and x['ob']])
    return ev[0][3] if ev else None
def auc(pairs):
    pos = [s for s, y in pairs if y]; neg = [s for s, y in pairs if not y]
    if not pos or not neg: return None
    return sum((p > n) + 0.5 * (p == n) for p in pos for n in neg) / (len(pos) * len(neg))
S2 = D.sila(B, C2); S3 = D.sila(B, C3)
PR = []
for c in IDS:
    for sk in SK:
        y = y06(c, sk)
        if y is None: continue
        xs = xs_(c, sk, C2); L = ST[('L', '29.09')][(c, sk)]
        PR.append(dict(c=c, sk=sk, y=y, L=None if L == '—' else D.G.index(L), W=D.vzves(xs, C2[0])[1] if L != '—' else None,
                       B=D.bkt(xs)[2] if L != '—' else None, S=S2[c][0], sam=any(x['mode'] == 'sam' for x in xs)))
def auc_of(rows, key): return auc([(r[key], r['y']) for r in rows if r[key] is not None and r['S'] is not None])
PRc = [r for r in PR if r['L'] is not None and r['S'] is not None]
PRs = [r for r in PRc if r['sam']]; PRh = [r for r in PRc if not r['sam']]; PRn2 = [r for r in PRc if r['sk'] != '2']
base_rate = sum(r['y'] for r in PRc) / len(PRc)
# лестница как правило: «С/У» на 29.09 → доля сдавших 6.10
lad_tab = {g: (sum(r['y'] for r in PRc if D.G[r['L']] == g), sum(1 for r in PRc if D.G[r['L']] == g)) for g in D.G[1:]}
lad_sk = {sk: {g: (sum(r['y'] for r in PRc if r['sk'] == sk and D.G[r['L']] == g), sum(1 for r in PRc if r['sk'] == sk and D.G[r['L']] == g)) for g in D.G[1:]} for sk in SK}
import random
def boot_delta(rows, a, b, n=2000, seed=7):
    rnd = random.Random(seed); ds = []
    for _ in range(n):
        smp = [rnd.choice(rows) for _ in rows]
        x, y = auc_of(smp, a), auc_of(smp, b)
        if x is not None and y is not None: ds.append(x - y)
    ds.sort(); return ds[int(.025 * len(ds))], ds[int(.975 * len(ds))]
CI_WL = boot_delta(PRn2, 'W', 'L'); CI_BL = boot_delta(PRn2, 'B', 'L')
def brier(rows, key): return sum((r[key] - r['y']) ** 2 for r in rows) / len(rows)

# ---------------- 2. кластеры ----------------
def n_sam(stt, c): return sum(ge(stt[(c, sk)]) for sk in MIN)
def pts_min(stt, c):
    v = [D.PTS[stt[(c, sk)]] for sk in MIN if stt[(c, sk)] != '—']; return sum(v) / len(v) if v else None
def ndays_total(cut): return len({(s['d'], s['tip']) for e, s in B.sob.items() if s['tip'] in ('LS', 'KR') and s['seq'] <= cut})

def kl_run(rezhim, hyst, delta=0.05):
    hist = OrderedDict(); prev = {c: None for c in IDS}
    for cp, cut in CP.items():
        S = D.sila(B, cut, rezhim); stt = ST[('L', cp)]; nd = ndays_total(cut); cur = {}
        for c in IDS:
            s, nt, ndn = S[c]
            raw = D.klaster_syroj(s, nt, ndn, nd, n_sam(stt, c), prev[c] if hyst else None, delta if hyst else 0)
            cur[c] = D.shag(prev[c], raw) if hyst else raw
        for r in B.ruchnye:
            if r['chto'] == 'klaster' and r['rebyonok'] in cur: cur[r['rebyonok']] = r['znachenie']
        hist[cp] = cur; prev = cur
    return hist
VAR = OrderedDict([('A', ('накопленное среднее, без гистерезиса', 'cum', False)), ('Б', ('только последний день', 'last', False)),
                   ('В', ('затухание 14 дн + гистерезис ±0,05 + шаг ≤ 1', 'ew', True))])
KLH = {v: kl_run(r, h) for v, (_, r, h) in VAR.items()}
def jumps(h):
    cps = list(h); ch = 0; kids = set(); big = 0
    for a, b in zip(cps, cps[1:]):
        for c in IDS:
            x, y = h[a][c], h[b][c]
            if x != y and 'Н' not in (x, y):
                ch += 1; kids.add(c); big += abs(D.LV.index(x) - D.LV.index(y)) > 1
    return ch, len(kids), big
KL = KLH['В']['6.10']
cntKL = Counter(KL.values())
# сверка с klaster.py (3 уровня): самый низ сливаем с низом
mapk = {'СН': 'Ни'}
rid = {v: k for k, v in FIO.items()}
agree_k = sum(mapk.get(KL[c], KL[c]) == K.P[FIO[c]]['rule'] for c in IDS)
def spearman(a, b):
    ks = [k for k in a if a[k] is not None and b.get(k) is not None]
    def rk(d):
        vals = sorted(d[k] for k in ks); return {k: (vals.index(d[k]) + len(vals) - 1 - vals[::-1].index(d[k])) / 2 for k in ks}
    ra, rb = rk(a), rk(b); ma, mb = st.mean(ra.values()), st.mean(rb.values())
    num = sum((ra[k] - ma) * (rb[k] - mb) for k in ks)
    den = (sum((ra[k] - ma) ** 2 for k in ks) * sum((rb[k] - mb) ** 2 for k in ks)) ** .5
    return num / den, len(ks)
rho_k = spearman({c: S3[c][0] for c in IDS}, {c: K.P[FIO[c]]['rank'] for c in IDS})
# двухуровневость: статусы минимума против кластера
ST3 = ST[('L', '6.10')]
PM = {c: pts_min(ST3, c) for c in IDS}; NS = {c: n_sam(ST3, c) for c in IDS}
rho_sp = spearman({c: S3[c][0] for c in IDS}, PM)
xt = defaultdict(Counter)
for c in IDS: xt[KL[c]][NS[c]] += 1
vis = [c for c in IDS if KL[c] != 'Н']
sizes = Counter(KL[c] for c in vis)
by_pm = sorted(vis, key=lambda c: (PM[c] if PM[c] is not None else -1))
f_lv = {}; i = 0
for lv in D.LV:
    for c in by_pm[i:i + sizes[lv]]: f_lv[c] = lv
    i += sizes[lv]
mism = [c for c in vis if f_lv[c] != KL[c]]
mism2 = [c for c in mism if abs(D.LV.index(f_lv[c]) - D.LV.index(KL[c])) >= 2]
HOLE = lambda c, sk: ST3[(c, sk)] in ('0', 'П')
top_hole = [c for c in IDS if KL[c] == 'В' and any(HOLE(c, sk) for sk in MIN)]
top_hole_sk = Counter(sk for c in top_hole for sk in MIN if HOLE(c, sk))
# «сам/уверенно» на одном пункте: последняя КР по навыку содержала один обязательный пункт
def last_sam_n(c, sk):
    xs = [x for x in xs_(c, sk, C3) if x['mode'] == 'sam' and x['ob']]
    if not xs: return None
    last = xs[-1]['ev']; return sum(1 for x in xs if x['ev'] == last)
one_item = [(c, sk) for c in IDS for sk in SK if ge(ST3[(c, sk)]) and last_sam_n(c, sk) == 1]
one_item_sk = Counter(sk for _, sk in one_item)
mean_pm = {lv: st.mean(PM[c] for c in IDS if KL[c] == lv and PM[c] is not None) for lv in D.LV if any(KL[c] == lv for c in IDS)}
mean_s = {lv: st.mean(S3[c][0] for c in IDS if KL[c] == lv) for lv in D.LV if any(KL[c] == lv for c in IDS)}
# альтернативный минимум (1,2,3,4) — сколько детей меняют кластер
alt_min = ['1', '2', '3', '4']
def kl_alt():
    S = D.sila(B, C3, 'ew'); prev = KLH['В']['29.09']; nd = ndays_total(C3); out = {}
    for c in IDS:
        ns = sum(ge(ST3[(c, sk)]) for sk in alt_min)
        out[c] = D.shag(prev[c], D.klaster_syroj(*S[c], nd, ns, prev[c], 0.05))
    return out
KL_ALT = kl_alt(); alt_ch = [c for c in IDS if KL_ALT[c] != KL[c]]

# ---------------- 3. списки на следующую пару ----------------
PRIO = {'0': 0, 'П': 1}
need = {sk: [c for c in IDS if ST3[(c, sk)] in PRIO and KL[c] != 'В'] for sk in MIN}
need_all = {sk: [c for c in IDS if ST3[(c, sk)] in PRIO] for sk in MIN}
nodata = {sk: [c for c in IDS if ST3[(c, sk)] == '—'] for sk in SK}
sem_sk = max(MIN, key=lambda sk: len(need[sk]))
CAP = int(next(p['max_detej'] for p in B.prepody if p['rol'] == 'seminar'))
PW = lambda c, sk: D.vzves(xs_(c, sk, C3), C3[0])[1]     # p взвешенного счёта — порядок внутри статуса
order_need = sorted(need[sem_sk], key=lambda c: (PRIO[ST3[(c, sem_sk)]], D.LV.index(KL[c]) if KL[c] != 'Н' else 1, PW(c, sem_sk)))
seminar = order_need[:CAP]; overflow = order_need[CAP:]
sem2_sk = max([sk for sk in MIN if sk != sem_sk], key=lambda sk: len(need[sk]))
prep = [p for p in B.prepody if p['rol'] == 'priem']
slots = OrderedDict((p['imya'], []) for p in prep)
rest = [c for c in IDS if c not in seminar]
lvl_ord = lambda c: {'В': 0, 'Ц': 1, 'Н': 2, 'Ни': 3, 'СН': 4}[KL[c]]
for c in sorted(rest, key=lambda c: (lvl_ord(c), -(S3[c][0] or 0))):
    want = D.LVN[KL[c]]
    cands = [p for p in prep if p['k_klasteru'] == want and len(slots[p['imya']]) < int(p['max_detej'])]
    if not cands: cands = [p for p in prep if len(slots[p['imya']]) < int(p['max_detej'])]
    if cands:
        p = min(cands, key=lambda p: len(slots[p['imya']])); slots[p['imya']].append(c)
sam_list = [c for c in rest if not any(c in v for v in slots.values())]
def dz(c):
    holes = [sk for sk in MIN if ST3[(c, sk)] in PRIO]
    if holes:
        sk = sem_sk if sem_sk in holes else min(holes, key=lambda s: (PRIO[ST3[(c, s)]], MIN.index(s)))
        lvl = '△-задачи на' if KL[c] == 'В' else '○-задачи на'
        return f'{lvl} навык {sk} (сейчас «{D.GN[ST3[(c, sk)]]}»)'
    nd = [sk for sk in MIN if ST3[(c, sk)] == '—']
    if nd: return f'обычное; навык {nd[0]} не измерен — пункт на КР'
    conf = [sk for sk in MIN if ST3[(c, sk)] == 'С']
    if conf: return f'закрепление навыка {conf[0]} («сам» → «уверенно»: второй раз на КР)'
    return 'расширенный: навыки ' + ', '.join(EXT) + ' и △'
KR_NEED = OrderedDict([(sk, (len(nodata[sk]), sum(ST3[(c, sk)] == 'С' for c in IDS))) for sk in SK])

# ---------------- печать ----------------
L = []; w = L.append
cnt_cells = len(IDS) * len(SK)
w('# 7И: система учёта — статус навыка, кластер по теме, группы на пару\n')
w('> 🗄 ЗАМЕНЕНО 11.10: аватар считается в боте, `bot-7i/bot7i/avatary.py`, по выгрузке бота; этот расчёт — только для истории и регрессии.\n')
w('*Черновик 08.10. Всё пересчитывается `python3 sistema.py` (папка данных — аргумент): адаптер собирает `dannye/*.csv`, движок `dvizhok.py` читает только их. '
  'Разметка «пункт → навык» и вердикты — из `../navyki/navyki.py` и `../klaster/klaster.py` (импортом, без изменений). '
  'Метки: **[F]** посчитано · **[M]** допущение · **[H]** гипотеза. Ребёнок в таблицах — фамилия (поимённо — только в арке).*\n')
w(f'**Тема в прототипе — комбинаторика 22.09–6.10.** Навыки: ' + '; '.join(f"**{k}** — {B.navyki[k]['deystvie'].split(':')[0]}" for k in SK) + '. '
  f'**Обязательный минимум [M, решает владелец]: {", ".join(MIN)}** (±1, сумма, разность, перебор со своим порядком); 4 (ВИ) и 5а — расширенные. '
  f'Почему так: ±1/сумма/разность/свой перебор — четыре действия «на уровне кружочков», без которых тему не решить; 5а — чтение чужого порядка, 4 — пока ни разу не измерен сам (§1.4). '
  f'Альтернатива {{1, 2, 3, 4}} проверена в §2.5.\n')

w('## 0. Короткий ответ\n')
w(f'1. **Статус навыка — лестница** (модель 1): пять градаций, правила переходов читаются вслух, ассистент может их проверить глазами; p взвешенного счёта — только порядок внутри статуса (кого звать первым). '
  f'Предсказание КР 6.10 по состоянию на 29.09 у всех трёх слабое: AUC {f2(auc_of(PRc, "L"))} / {f2(auc_of(PRc, "W"))} / {f2(auc_of(PRc, "B"))} (лестница / счёт / BKT, n = {len(PRc)}); '
  f'без спорного навыка 2 — {f2(auc_of(PRn2, "L"))} / {f2(auc_of(PRn2, "W"))} / {f2(auc_of(PRn2, "B"))}, перевес счёта над лестницей, 95%-интервал [{f2(CI_WL[0])}; {f2(CI_WL[1])}] — на границе шума: слабый довод за счёт, поэтому его p и оставлен внутри лестницы [F]. '
  f'BKT при этом ставит «уверенно» с первой КР и меняет до {pp(sb[-1], cnt_cells)} оценок от выбора параметров, которые на 28 детях не откалибровать [F].')
w(f'2. **Кластер — да, второй уровень нужен, но вычисляемый, а не ручной.** Он выводится из силы по теме (как хорошо решает, включая △) + △-сигналов + одного условия из статусов (для «самого низа»). '
  f'Функцией статусов минимума он не является: ρ(сила, средний статус минимума) = {f2(rho_sp[0])}; если резать класс по статусам на те же размеры групп, {len(mism)} из {len(vis)} детей меняют уровень [F]; '
  f'в верхе {len(top_hole)} из {cntKL["В"]} имеют навык минимума на «0/П» (' + ', '.join(f'{sk} — {n}' for sk, n in top_hole_sk.most_common()) + ') [F].')
w(f'3. **Хранение — плоские CSV в git**, одна таблица на сущность, наблюдения — только дописываются; SQLite — как кэш, если бот начнёт писать сотни строк в день (§3).')
w(f'4. **На пару {NEXT.strftime("%d.%m")}:** семинар Вани — навык **{sem_sk}** ({len(seminar)} детей, ещё {len(overflow)} в очереди к преподавателям); остальные — к 4 преподавателям по ≤ 4; '
  f'на КР обязательно: ≥ 2 ○-пункта на каждый навык минимума (сейчас {len(one_item)} оценок «сам/уверенно» стоят на одном пункте) и нормальный пункт на ВИ (§4).\n')

# ---- §1
w('## 1. Статус навыка: три модели\n')
w('### 1.1. Градации и правила (рекомендуемая — лестница) [M]\n')
w('| знак | статус | правило (по событиям, где навык — основной в пункте) |\n|---|---|---|')
for g, t in [('—', 'ни одного наблюдения на листке/приёме/КР (ДЗ не считается)'),
             ('0', 'наблюдения есть, но навык не сдан нигде — ни сам, ни с помощью'),
             ('П', 'сдавал с помощью (листок, приём), но последняя КР по навыку не сдана или КР ещё не было'),
             ('С', 'последняя КР, где был навык, сдана'),
             ('У', 'две последние КР с навыком сданы, и они в разные дни')]:
    w(f'| **{g}** | {D.GN[g]} | {t} |')
w('\n«Сдал навык на событии» — верно ≥ 2/3 обязательных пунктов с этим навыком (1 из 1, 2 из 2, 2 из 3). Пусто на КР — не сдал. '
  'Необязательные △ (по выбору) идут только в плюс: верный △ — сдал, неверный — не улика. ДЗ (дом) в статус не входит — стоит рядом справочно (меряет помощь, `01-klass.md`). '
  'Ручная правка Вани (`ruchnye.csv`) главнее модели.\n')
w('**Переходы:** КР сдана → С (если и предыдущая КР сдана в другой день → У). КР не сдана → П (если когда-то сдавал с помощью), иначе 0 — то есть «уверенно» падает до П одним провалом КР (это и есть проверка «устойчиво»). '
  'Листок/приём поднимает только 0 → П, на С/У не влияет. Незакрытый навык минимума (не У к концу темы) переносится в следующую тему как «долг»: статус сохраняется, навык ставится в КР новой темы.\n')
w('**Что даст бот (поэтапно) [M]:** «плюсик» = событие режима «помощь» (0 → П). Когда появятся «попытка» и «подсказка»: приём с 1-й попытки без подсказки — тоже самостоятельное событие (может дать С, но не У: У — только две КР). '
  'Сайт ДЗ с автоприёмом — режим «дом», в статус не входит, но даёт флаг «дома решает / не решает» и выбор навыка для ДЗ.\n')
w('### 1.2. Две другие модели\n')
w(f'- **Взвешенный счёт с затуханием:** p = (Σ w·верно + {D.M2P["A0"]:g}·0,5)/(Σ w + {D.M2P["A0"]:g}), w = вес режима (КР {D.M2P["W"]["sam"]:g}, приём {D.M2P["W"]["pomosch"]:g}, ДЗ {D.M2P["W"]["dom"]:g}) · 0,5^(возраст/{D.M2P["HL"]} дн). '
  'Оценка: — если Σ w < 0,3; 0 если p < 0,5; П если вес КР < 0,67; У если p ≥ 0,8 и КР в ≥ 2 дня; С если p ≥ 0,67; иначе П.'.replace('0.', '0,'))
bp = D.BKTP
w((f'- **BKT (Bayesian Knowledge Tracing):** P(знает) старт {bp["L0"]}, после события «выучил» с вероятностью {bp["T"]}; угадать/ошибиться: КР {bp["g"]["sam"]}/{bp["s"]["sam"]}, приём {bp["g"]["pomosch"]}/{bp["s"]["pomosch"]}, ДЗ {bp["g"]["dom"]}/{bp["s"]["dom"]}. '
  'Оценка: 0 если P < 0,4; П < 0,7; С < 0,95; У ≥ 0,95 (0,95 — стандартный порог «освоено» в адаптивных системах). Elo-подобная модель (рейтинг ребёнка против трудности пункта) — та же логика с той же нуждой в калибровке, отдельно не считалась.\n').replace('0.', '0,'))
w('### 1.3. Как ведут себя на наших данных [F]\n')
w(f'Ячеек ребёнок × навык: {cnt_cells}. Распределение оценок на 6.10 (все навыки / только минимум):\n')
w('| модель | ' + ' | '.join(f'{g} {D.GN[g]}' for g in D.G) + ' | изменилось 29.09 → 6.10 |\n|---|' + '---|' * 6)
for m in 'LWB':
    w(f'| {MN[m]} | ' + ' | '.join(f'{dist[m][g]} / {distmin[m][g]}' for g in D.G) + f' | {stab[m]} |')
w('')
for a, b in (('L', 'W'), ('L', 'B'), ('W', 'B')):
    s1, n1 = agree(a, b); s2, _ = agree(a, b, fn=ge)
    w(f'- {MN[a]} ↔ {MN[b]}: совпадает оценка {pc(s1, n1)} = {pp(s1, n1)}; совпадает «сам или выше / ниже» {pp(s2, n1)}.')
w(f'- BKT ставит «сам/уверенно» без единого самостоятельного пункта {bkt_nosam} раз (из них навык 4 — ВИ, который сам не мерился ни у кого); взвешенный счёт — {w_nosam} раз. '
  'Причина: при малом числе пунктов вероятность «знает» разгоняется листками с помощью — чтобы этого не было, угадывание на приёме приходится ставить ~0,75, и тогда листки почти ничего не значат.\n')
w(f'**Предсказание.** Состояние на 29.09 (до пары 6.10) → сдал ли ребёнок навык на ○ КР 6.10. Пар ребёнок × навык: {len(PRc)} (без «нет данных»), сдали {pp(sum(r["y"] for r in PRc), len(PRc))}. AUC (0,5 — монетка, 1 — идеально):\n')
w('| предиктор | все пары | навык уже был на КР 29.09 | навык был только на листках | без навыка 2 | Брайер |\n|---|---|---|---|---|---|')
for key, nm in (('L', 'лестница (порядок 0 < П < С < У)'), ('W', 'взвешенный счёт, p'), ('B', 'BKT, P(верно на КР)'), ('S', 'сила по теме (без навыков)')):
    br = f2(brier(PRc, key)) if key in ('W', 'B') else '—'
    w(f'| {nm} | {f2(auc_of(PRc, key))} | {f2(auc_of(PRs, key))} (n={len(PRs)}) | {f2(auc_of(PRh, key))} (n={len(PRh)}) | {f2(auc_of(PRn2, key))} (n={len(PRn2)}) | {br} |')
w('\nПо навыкам (оценка на 29.09 → сдал на КР 6.10): ' + '; '.join(f'**{sk}** ' + ', '.join(f'{g} {pc(*lad_sk[sk][g])}' for g in D.G[1:] if lad_sk[sk][g][1]) for sk in SK if any(lad_sk[sk][g][1] for g in D.G[1:])) + '. '
  'Провал «сам» на 6.10 сидит в навыке 2: 29.09 его мерили домино и квадратами (разрез виден на картинке), 6.10 — разрезом «по числу пятёрок» с поиском чужой ошибки (○6); это другой сюжет, а возможно и другое действие (`NAVYKI` §3.3 п. 4) [F + H].\n')
w('\nЛестница как правило (29.09 → доля сдавших навык на КР 6.10): ' + '; '.join(f'«{D.GN[g]}» {pc(*lad_tab[g])} = {pp(*lad_tab[g])}' for g in D.G[1:] if lad_tab[g][1]) + '.\n')
w(f'*Читать осторожно [M]:* n мал, КР 29.09 и 6.10 разные по пунктам (навык 2 на 6.10 — другой сюжет, `NAVYKI` §6), между ними был разбор. '
  f'Без навыка 2 счёт и BKT ранжируют лучше лестницы; 95%-интервал разности (бутстрэп по парам) — счёт − лестница [{f2(CI_WL[0])}; {f2(CI_WL[1])}], BKT − лестница [{f2(CI_BL[0])}; {f2(CI_BL[1])}]'
  + (': вероятностные модели ранжируют лучше, но исключение навыка 2 сделано задним числом — довод слабый, и поэтому их p оставлен как порядок внутри статуса. ' if CI_BL[0] > 0 else ': различие не доказано. ') +
  'Вывод не «какая модель точнее», а «сложная модель не окупается как ярлык»: все три слабо предсказывают следующую КР, и **сила по теме предсказывает навык не хуже статуса навыка** — '
  'на двух КР навыковая модель ещё не отделилась от общего уровня. Это ожидаемо: у ребёнка 1–3 пункта на навык за КР. Пересмотреть выбор модели, когда КР по навыку будет ≥ 4 и пунктов ≥ 2 на навык [M].\n')
w('### 1.4. Сколько наблюдений нужно [F, синтетика]\n')
w('Событие раз в неделю; в строке — оценки (лестница / счёт / BKT) после 1-го, 2-го, … события.\n')
w('| сценарий | ' + ' | '.join(f'после {i + 1}' for i in range(4)) + ' |\n|---|---|---|---|---|')
for nm, r in SYN.items():
    w(f'| {nm} | ' + ' | '.join(' / '.join(t) for t in r) + ' |' * (1 + 4 - len(r)) if len(r) < 4 else f'| {nm} | ' + ' | '.join(' / '.join(t) for t in r) + ' |')
w('\nЛестница: «сам» — одна сданная КР, «уверенно» — две КР в разные дни, это минимум и он же — определение. BKT доходит до «уверенно» на первой же КР с двумя верными пунктами — '
  '«устойчиво» он не проверяет. Счёт осторожнее, но его пороги (0,67/0,8, вес 0,35) никто не сможет объяснить ассистенту.\n')
w('### 1.5. Чувствительность к параметрам [F]\n')
w(f'Сколько из {cnt_cells} ячеек меняют оценку на 6.10, если сдвинуть параметр:\n')
w('- лестница: ' + '; '.join(f'{n} — {k}' for k, n in SENS_L))
w('- взвешенный счёт: ' + '; '.join(f'{n} — {k}' for k, n in SENS_W))
w(f'- BKT, сетка 32 вариантов (угадывание КР 0,1/0,25, ошибка 0,05/0,2, обучение 0,05/0,3, старт 0,2/0,5, угадывание на приёме 0,4/0,75): '
  f'медиана {sb[len(sb) // 2]} ({pp(sb[len(sb) // 2], cnt_cells)}), максимум {sb[-1]} ({pp(sb[-1], cnt_cells)}). Калибровать нечем: нужно сотни пар «пункт — исход» на навык.\n')
w('### 1.6. Понятность [M]\n')
w('| модель | ассистент поймёт за минуту? | ребёнку объяснить «что сделать, чтобы стало „уверенно“» | спорную оценку проверить руками |\n|---|---|---|---|')
w('| лестница | да: «последняя КР сдана? а предыдущая?» | «напиши навык на двух КР подряд» | да, по двум строкам журнала |')
w('| взвешенный счёт | частично: «КР весит больше» | нет, порог в процентах с затуханием | только скриптом |')
w('| BKT | нет | нет | нет |')
w('')

# ---- §1.7 таблица статусов
w('### 1.7. Таблица ребёнок × навык (лестница, 6.10) [F по правилу M]\n')
w('Порядок — по кластеру и силе. Жирным — навыки минимума. В скобках — оценка на 29.09, если другая.\n')
w('| ребёнок | кластер | сила | △ | ' + ' | '.join(f'**{k}**' if k in MIN else k for k in SK) + ' | сам из минимума |\n|---|---|---|---|' + '---|' * (len(SK) + 1))
ORD = sorted(IDS, key=lambda c: (-D.LV.index(KL[c]) if KL[c] != 'Н' else 1, -(S3[c][0] or 0)))
for c in ORD:
    cells = []
    for sk in SK:
        a, b = ST[('L', '29.09')][(c, sk)], ST3[(c, sk)]
        cells.append(b + ('¹' if (c, sk) in one_item else '') + (f' ({a})' if a != b and a != '—' else ''))
    w(f'| {fam(c)} | {D.LVN[KL[c]]} | {f2(S3[c][0])} | {S3[c][1]} | ' + ' | '.join(cells) + f' | {NS[c]}/{len(MIN)} |')
w(f'\n¹ — «сам/уверенно», где последняя КР по навыку содержала один обязательный пункт: {len(one_item)} из {sum(ge(v) for v in ST3.values())} таких оценок (' + ', '.join(f'{sk} — {n}' for sk, n in sorted(one_item_sk.items())) + '). Это слабое «сам» [F].\n')
w('\nСвод по навыкам (лестница, 6.10): ' + '; '.join(f'**{sk}**: ' + ', '.join(f'{g} {sum(ST3[(c, sk)] == g for c in IDS)}' for g in D.G if sum(ST3[(c, sk)] == g for c in IDS)) for sk in SK) + '.\n')

# ---- §2
w('## 2. Кластер по теме\n')
w('### 2.1. Правило [M]\n')
w('**Сила по теме** s — «насколько хорошо решает» (определение владельца): в каждом классном событии темы (листок, КР) перцентиль-ранг ребёнка по баллу ○ + △ + доп (на КР △ ×2; Р155: решил ≥ 3 △ без ошибок в ○ — ○ засчитаны); '
  'два листка одного дня усредняются; дни усредняются с затуханием (полураспад 14 дней), так что последняя пара весит больше. ДЗ в силу не входит. '
  '**△-сигнал** — событие, где ребёнок решил ≥ 2 △ (мини-листок ≥ 4 из 6).\n')
w(f'| уровень | правило | сейчас |\n|---|---|---|')
for lv, t in [('В', f's ≥ {D.CUT["V"]} и ≥ 2 △-сигналов («знает базу, нужно продвинутое»)'),
              ('Ц', f'остальные'),
              ('Ни', f's < {D.CUT["NI"]}'),
              ('СН', f's < {D.CUT["SN"]} и самостоятельно («сам»/«уверенно») не больше одного навыка минимума'),
              ('Н', 'работы меньше чем в 3 днях темы')]:
    w(f'| {D.LVN[lv]} | {t} | {cntKL[lv]} |'.replace('0.', '0,'))
w(f'\n**Гистерезис [M]:** пороги над текущим уровнем ребёнка сдвинуты вверх на 0,05, под ним — вниз на 0,05 (чтобы выехать вверх, надо перескочить с запасом; чтобы провалиться — упасть с запасом); '
  'удержаться в верхе — достаточно 1 △-сигнала; за пересчёт — не больше одного уровня. Пересчёт — после каждой пары, когда внесены КР/приём. '
  'Ручная правка Вани (`ruchnye.csv`, «klaster») главнее. Новая тема стартует с уровнем прошлой темы до своей первой КР [M].\n')
w('*[H] «Ворота» в верх* — кандидат владельца «написать идеально»: вход в верх только через КР, где все ○ минимума верны. В прототип не встроено: на 6.10 ○ «всё верно» — у единиц, ворота пока закрыли бы верх почти целиком; решить после следующей КР.\n')
w('### 2.2. Стабильность: варианты пересчёта на трёх точках (22.09 → 29.09 → 6.10) [F]\n')
w('| вариант | смен уровня | детей сменило | прыжков через уровень | на 6.10: верх / середина / низ / самый низ / мало данных |\n|---|---|---|---|---|')
for v, (nm, _, _) in VAR.items():
    ch, kids, big = jumps(KLH[v]); cc = Counter(KLH[v]['6.10'].values())
    w(f'| {v}: {nm} | {ch} | {kids} | {big} | {cc["В"]} / {cc["Ц"]} / {cc["Ни"]} / {cc["СН"]} / {cc["Н"]} |')
w('\nТочек всего три, 22.09 — один день листков с помощью, так что это проверка механики, не доказательство [M]. Рекомендуется вариант В.\n')
w('Траектории (вариант В): ' + '; '.join(f'{fam(c)} ' + '→'.join(D.LVN[KLH["В"][cp][c]] for cp in CP) for c in ORD if len({KLH["В"][cp][c] for cp in CP}) > 1) + '.\n')
w('### 2.3. Сверка с klaster.py [F]\n')
w(f'Сила здесь пересчитана из `dannye/` (без листков логики 15.09); ρ(сила, ранг klaster.py) = {f2(rho_k[0])} (n={rho_k[1]}). '
  f'Уровень совпадает с правилом klaster.py (самый низ слит с низом) у {agree_k} из {len(IDS)}. Расхождения: '
  + '; '.join(f'{fam(c)} — здесь {D.LVN[KL[c]]}, там {K.LV[K.P[FIO[c]]["rule"]]}' for c in IDS if mapk.get(KL[c], KL[c]) != K.P[FIO[c]]['rule']) + '.\n')
w('### 2.4. Нужна ли двухуровневая система [F + M]\n')
w(f'**Да, но второй уровень вычисляется, а не ведётся руками.** Довод — на данных:\n')
w(f'1. ρ(сила по теме, средний статус минимума) = {f2(rho_sp[0])} (n={rho_sp[1]}): связаны, но не одно и то же.')
w('2. Кластер × число навыков минимума на «сам/уверенно» (лестница, 6.10):\n')
w('| кластер | ' + ' | '.join(str(i) for i in range(len(MIN) + 1)) + ' | средний статус минимума | средняя сила |\n|---|' + '---|' * (len(MIN) + 3))
for lv in ['В', 'Ц', 'Ни', 'СН', 'Н']:
    if not any(KL[c] == lv for c in IDS): continue
    w(f'| {D.LVN[lv]} | ' + ' | '.join(str(xt[lv][i]) for i in range(len(MIN) + 1)) + f' | {f2(mean_pm.get(lv))} | {f2(mean_s.get(lv))} |')
w(f'\n3. Если кластер сделать функцией статусов (резать по среднему статусу минимума на те же размеры групп), уровень меняют {len(mism)} из {len(vis)} видимых детей, '
  f'из них {len(mism2)} — через уровень [F]. В верхе {len(top_hole)} из {cntKL["В"]} с дырой в минимуме: ' + ', '.join(f'{fam(c)} ({", ".join(sk for sk in MIN if not ge(ST3[(c, sk)]))})' for c in top_hole) + '.')
w('4. Значит, «верх по решению» и «верх по владению минимумом» — разные множества. Владелец назвал оба определения («по тому, насколько хорошо решают» и «уверены, что знают все базовые приёмы»); '
  f'на 6.10 они расходятся на навыках ' + ', '.join(sk for sk, _ in top_hole_sk.most_common()) + ' — дыры минимума есть и у сильных, поэтому верх не освобождается от семинарных навыков, а получает их через своего преподавателя на △.\n')
w('**Как разделить работу [M]:** кластер — для **рассадки и уровня листка** (кто с кем, кому △ с начала), меняется медленно (гистерезис); статус навыка — для **семинара и ДЗ** (кого позвать на разбор навыка X), меняется после каждой КР. '
  'Связь одна: «самый низ» требует и слабой силы, и почти пустого минимума. Вручную ведётся только правка (`ruchnye.csv`), обе таблицы — производные.\n')
w(f'### 2.5. Если минимум — {{{", ".join(alt_min)}}} [F]\n')
w(f'Кластер меняют {len(alt_ch)} из {len(IDS)}: ' + ('; '.join(f'{fam(c)} {D.LVN[KL[c]]} → {D.LVN[KL_ALT[c]]}' for c in alt_ch) or 'никто') + '. Выбор минимума влияет только на «самый низ» и на семинары, не на верх.\n')

# ---- §3
w('## 3. Хранение\n')
w('**Рекомендация: плоские CSV в git (UTF-8, запятая), одна таблица — одна сущность; наблюдения — только дописываются.** Всё производное (статусы, кластеры, группы) не хранится, а пересчитывается. '
  'Эта папка — рабочий пример: `dannye/*.csv` собраны адаптером, движок читает только их.\n')
w('| таблица | ключ | поля | кто пишет |\n|---|---|---|---|')
for a, b, c, d in [
    ('deti.csv', 'id (r01…)', 'fio, aktiven', 'Ваня, раз в год'),
    ('navyki.csv', 'kod', 'tema, deystvie, minimum (0/1), s_daty', 'Ваня, в начале темы'),
    ('sobytiya.csv', 'id (KR-2026-10-06)', 'data, poryadok (в дне), tip KR/LS/ML/DZ/SAIT, rezhim sam/pomosch/dom, tema, istochnik', 'при подготовке пары'),
    ('punkty.csv', '(sobytie, punkt)', 'uroven ○/△/доп, obyazat 0/1, navyk_osn, navyki_vspom, obhod, uslovie [+ kluch, variant]', 'при подготовке листка/КР — разметка навыков ДО урока'),
    ('nablyudeniya.csv', '(sobytie, punkt, rebyonok, popytka)', 'verdikt + − 0 ?, podskazka (пусто/0/nav/ar), kto, istochnik, ts', 'бот, сайт, разметка фото КР — только дописывают'),
    ('ruchnye.csv', 'строка', 'data, rebyonok, chto status/klaster, klyuch, znachenie, kto, prichina', 'только Ваня'),
    ('prepody.csv', 'imya', 'rol seminar/priem, max_detej, k_klasteru', 'Ваня, перед парой'),
]:
    w(f'| `{a}` | {b} | {c} | {d} |')
w('\n**Как вносится каждый источник:**\n')
for t in [
    '**Фото КР** → разметка (как сейчас, JSONL) → нормализатор пишет строки `nablyudeniya` с rezhim=sam (из события), popytka=1, verdikt по ключу из `punkty`. Пусто на ○ → «0».',
    '**Листок, устный приём (сейчас — CSV-таблица)** → строка на (ребёнок, пункт); «в» → «+». Попытки и подсказки пока пусто.',
    '**Telegram-бот ассистентов, этап 1 «плюсик»** → строка (sobytie, punkt, rebyonok, verdikt=+, kto=ассистент, ts). Этап 2 «попытки» → та же строка с popytka=n и verdikt − для неудачных. Этап 3 «обратная связь» → поле podskazka (0 / nav / ar) и, отдельно, `zametki.csv` (свободный текст, в статусы не идёт).',
    '**Сайт ДЗ с автоприёмом** → строки rezhim=dom (событие типа SAIT), popytka = номер отправки, verdikt по ключу. Бот-собеседник — то же + podskazka.',
    '**Ручная правка** — только `ruchnye.csv`; модель её не перезаписывает.',
]:
    w('- ' + t)
w('\n**CSV в git против SQLite [M]:**\n')
w('| | CSV в git | SQLite |\n|---|---|---|')
for a, b, c in [('правка руками / глазами', 'да, в любом редакторе и в таблице', 'нужен клиент'),
                ('история и откат', 'git: кто, когда, что', 'нет без отдельного журнала'),
                ('одновременная запись бота и сайта', 'конфликт при параллельной записи — нужен один писатель или файл на источник', 'транзакции из коробки'),
                ('объём (28 детей × ~30 пунктов × 30 недель ≈ 25 тыс. строк в год)', 'хватает с запасом', 'избыточно'),
                ('дисциплина репозитория (`git_zona.py`, гейты)', 'встраивается', 'бинарник в git — плохо')]:
    w(f'| {a} | {b} | {c} |')
w('\nРешение: CSV — источник правды. Бот и сайт пишут каждый в свой файл (`nablyudeniya-bot.csv`, `nablyudeniya-sait.csv`) — нет параллельной записи в один файл; движок читает все `nablyudeniya*.csv`. '
  'SQLite — только если бот станет сервером с онлайн-запросами («что у Пети сейчас»), и то как кэш, пересобираемый из CSV.\n')

# ---- §4
w(f'## 4. Списки на пару {NEXT.strftime("%d.%m")} (по состоянию на 6.10) [F по правилам M]\n')
w('Кандидатов на семинар (не-верх, «0/П») по навыкам минимума: ' + ', '.join(f'{sk} — {len(need[sk])}' for sk in MIN) + '; навык семинара — где их больше всего.\n')
w(f'**Семинар Вани — навык {sem_sk}** ({B.navyki[sem_sk]["deystvie"]}). Кандидаты — не-верх со статусом «не умеет»/«с помощью»: {len(need[sem_sk])}; '
  f'вместимость {CAP}; порядок: сначала «не умеет», затем ниже кластер, затем ниже p взвешенного счёта по навыку.\n')
w('Семинар: ' + ', '.join(f'{fam(c)} ({ST3[(c, sem_sk)]}, {D.LVN[KL[c]]})' for c in seminar) + '.')
if overflow: w('\nНе влезли (навык {} — задача преподавателю): '.format(sem_sk) + ', '.join(fam(c) for c in overflow) + '.')
w(f'\nНуждаются в навыке {sem_sk} и в верхе (разбирают с преподавателем на △): ' + (', '.join(fam(c) for c in need_all[sem_sk] if KL[c] == 'В') or 'нет') + '.')
w(f'\nВторой по нужде навык минимума — **{sem2_sk}** ({len(need[sem2_sk])} не-верх детей «0/П»): кандидат на вторую половину пары или на следующую неделю.\n')
w('**Преподаватели (≤ 4 детей, фиксированный список на пару):**\n')
for p, cs in slots.items():
    role = next(x['k_klasteru'] for x in prep if x['imya'] == p)
    w(f'- **{p}** (профиль: {role}): ' + (', '.join(f'{fam(c)} ({D.LVN[KL[c]]}; дыры: {", ".join(sk for sk in MIN if ST3[(c, sk)] in PRIO) or "нет"})' for c in cs) or '—'))
if sam_list: w('- **сами с листком (мест у преподавателей нет):** ' + ', '.join(fam(c) for c in sam_list))
w('\n**Что обязательно на КР этой пары (измерить):** ' + '; '.join(f'навык {sk}: нет данных у {a}, «сам» → ждут второй КР {b}' for sk, (a, b) in KR_NEED.items() if a or b) + '. '
  'Особо — **навык 4 (ВИ)**: за тему один самостоятельный пункт (КР 29.09 2б, решался и обходом), на ○ КР 6.10 — ни одного; нужен ○-пункт, где пересечение не дано и без него не решить.\n')
w('**Индивидуальные ДЗ:**\n')
w('| ребёнок | кластер | ДЗ |\n|---|---|---|')
for c in ORD: w(f'| {fam(c)} | {D.LVN[KL[c]]} | {dz(c)} |')
w('\n**Листок по кластерам [M]:** верх — △ с начала (Р155), ○ засчитываются по △; середина — ○ + △, приём у своего преподавателя; низ — ○ с упором на навык семинара, после семинара сразу к задаче; '
  'самый низ — внутри семинара, свой короткий ○-листок на тот же навык.\n')

# ---- §5
w('## 5. Риски\n')
for t in [
    f'**Мало самостоятельных пунктов на навык [F]:** на КР 1–3 пункта на навык, «сдал» решается одним пунктом. Лечится не моделью, а КР: каждую неделю 6–8 ○-пунктов, на каждый навык минимума ≥ 2.',
    '**Разметка «пункт → навык» — суждение [M]:** пункты смешивают навыки (КР 6.10 ○6 — сумма + ±1 + «найди ошибку»). Ошибка разметки — ошибка статуса. Разметку делать до урока, спорные пункты не считать.',
    '**Листки с помощью завышают, а ДЗ не меряет [F]:** поэтому листки дают только П, ДЗ — ничего. Цена: «сам» видно только раз в неделю.',
    '**Принимающие ставят «+» неверным [F, мини-листок 6.10]:** бот без ключа размножит ошибку. Ключ — в `punkty.csv`, бот показывает его принимающему.',
    '**Дети, писавшие только △ [F]:** ○ не измерены — статус «нет данных/с помощью» при высокой силе. Правило: один ○-пункт минимума обязателен для всех.',
    '**Ассистенты не будут заполнять [M, владелец]:** система работает и на одном «плюсике» (этап 1); всё сверх — бонус.',
    '**Пороги кластера и выбор минимума — договорённость [M]:** резких разрывов в силе нет (`KLASTERY` §3); «самый низ» = 3 человека по условию, которое владелец должен подтвердить.',
    '**Ярлык [H]:** кластер виден детям через рассадку; гистерезис уменьшает дёрганье, но «самый низ» как название — только для команды.',
]:
    w('- ' + t)
w('\n## 6. Стратификация\n')
w('| утверждение | статус |\n|---|---|')
for a, b in [('распределения оценок, совпадения моделей, AUC, чувствительность, сверка с klaster.py, состав групп', 'F (по правилам M)'),
             ('разметка пунктов по навыкам, вердикты КР', 'M/F — из navyki.py/klaster.py'),
             ('обязательный минимум {1, 2, 3, 5б}', 'M — решает владелец'),
             ('порог «сдал» 2/3, «уверенно» = 2 КР в разные дни', 'M'),
             ('пороги кластера 0,55 / 0,40 / 0,25, гистерезис 0,05, шаг ≤ 1', 'M'),
             ('сила по теме предсказывает навык не хуже статуса — потому что пунктов мало', 'H'),
             ('приём с 1-й попытки без подсказки можно считать самостоятельным', 'H — проверить, когда бот начнёт писать попытки'),
             ('«ворота» в верх через идеальную КР', 'H — кандидат владельца')]:
    w(f'| {a} | {b} |')
TXT = '\n'.join(L)
open(os.path.join(HERE, 'SISTEMA-chernovik.md'), 'w', encoding='utf-8').write(TXT + '\n')

# ---- консоль: списки на пару
print(f'== Пара {NEXT.strftime("%d.%m")} ==')
print(f'Семинар (Ваня), навык {sem_sk}: ' + ', '.join(FIO[c] for c in seminar))
if overflow: print('  не влезли: ' + ', '.join(FIO[c] for c in overflow))
for p, cs in slots.items(): print(f'{p}: ' + ', '.join(FIO[c] for c in cs))
if sam_list: print('сами: ' + ', '.join(FIO[c] for c in sam_list))
print(f'Кластеры: ' + ', '.join(f'{D.LVN[k]} {v}' for k, v in cntKL.items()))
print(f'AUC L/W/B/S: {f2(auc_of(PRc, "L"))} {f2(auc_of(PRc, "W"))} {f2(auc_of(PRc, "B"))} {f2(auc_of(PRc, "S"))} (n={len(PRc)})')
print('-> SISTEMA-chernovik.md')
