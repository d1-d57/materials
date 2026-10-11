# -*- coding: utf-8 -*-
"""Движок учёта 7И: читает только dannye/*.csv (схема §3 отчёта) и считает
статусы навыков (три модели), силу по теме, кластеры (4 уровня, с гистерезисом), группы на пару.
Импортируется из sistema.py; сам ничего не пишет. Метки в комментариях: [M] допущение, [H] гипотеза."""
import csv, os
from collections import defaultdict, OrderedDict
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
G = ['—', '0', 'П', 'С', 'У']                 # нет данных · не умеет · с помощью · сам · уверенно
GN = {'—': 'нет данных', '0': 'не умеет', 'П': 'с помощью', 'С': 'сам', 'У': 'уверенно'}
PTS = {'0': 0, 'П': 1, 'С': 2, 'У': 3}
LV = ['СН', 'Ни', 'Ц', 'В']                     # самый низ · низ · середина · верх; 'Н' — мало данных
LVN = {'СН': 'самый низ', 'Ни': 'низ', 'Ц': 'середина', 'В': 'верх', 'Н': 'мало данных'}


def d_(s): y, m, d = map(int, s.split('-')); return date(y, m, d)


class Baza:
    def __init__(self, dd=os.path.join(HERE, 'dannye')):
        rd = lambda f: list(csv.DictReader(open(os.path.join(dd, f), encoding='utf-8')))
        self.deti = OrderedDict((r['id'], r['fio']) for r in rd('deti.csv') if r['aktiven'] == '1')
        self.navyki = OrderedDict((r['kod'], r) for r in rd('navyki.csv'))
        self.MIN = [k for k, r in self.navyki.items() if r['minimum'] == '1']
        self.sob = OrderedDict((r['id'], dict(r, d=d_(r['data']), seq=(d_(r['data']), int(r['poryadok'])))) for r in rd('sobytiya.csv'))
        self.punkt = {(r['sobytie'], r['punkt']): r for r in rd('punkty.csv')}
        self.ruchnye = rd('ruchnye.csv')
        self.prepody = rd('prepody.csv')
        self.obs = []
        for r in rd('nablyudeniya.csv'):
            p = self.punkt[(r['sobytie'], r['punkt'])]; s = self.sob[r['sobytie']]
            self.obs.append(dict(c=r['rebyonok'], ev=r['sobytie'], p=r['punkt'], v=r['verdikt'], skill=p['navyk_osn'],
                                 lvl=p['uroven'], ob=p['obyazat'] == '1', mode=s['rezhim'], tip=s['tip'], d=s['d'], seq=s['seq']))
        self.obs.sort(key=lambda x: x['seq'])
        self.by = defaultdict(list)
        for x in self.obs: self.by[(x['c'], x['skill'])].append(x)

    def upto(self, xs, cut):
        return [x for x in xs if cut is None or x['seq'] <= cut]


# ---------------- наблюдения навыка, сгруппированные по событиям ----------------
def used(x, blank_fail=True):
    """Пункт идёт в навык: обязательный — всегда (пусто на КР = провал [M]); необязательный (△ по выбору) — только верный [M]."""
    if x['v'] == '0' and not blank_fail: return False
    return x['ob'] or x['v'] == '+'


def events(xs, porog=2 / 3, blank_fail=True):
    """[(seq, дата, режим, сдал?)] — сдал = ≥ порога обязательных пунктов верно; без обязательных — верный необязательный [M]."""
    out = OrderedDict()
    for x in xs:
        if not used(x, blank_fail): continue
        e = out.setdefault(x['ev'], dict(seq=x['seq'], d=x['d'], mode=x['mode'], k=0, n=0, kt=0))
        if x['ob']: e['n'] += 1; e['k'] += x['v'] == '+'
        else: e['kt'] += 1
    res = []
    for e in out.values():
        ok = (e['k'] / e['n'] >= porog - 1e-9) if e['n'] else (True if e['kt'] else None)
        if ok is not None: res.append((e['seq'], e['d'], e['mode'], ok))
    return res


# ---------------- модель 1: лестница ----------------
def lestnica(xs, porog=2 / 3, blank_fail=True):
    """У — две последние самостоятельные (КР) сданы, в разные дни; С — последняя самостоятельная сдана;
    П — последняя самостоятельная не сдана или её нет, но с помощью (листок/приём) сдавал; 0 — не сдавал нигде; — — данных нет.
    ДЗ в статус не входит (меряет помощь, а не ребёнка)."""
    ev = events(xs, porog, blank_fail)
    sam = [e for e in ev if e[2] == 'sam']; pom = [e for e in ev if e[2] == 'pomosch']
    if not sam and not pom: return '—'
    if sam and sam[-1][3]:
        return 'У' if len(sam) >= 2 and sam[-2][3] and sam[-2][1] != sam[-1][1] else 'С'
    return 'П' if any(e[3] for e in pom) else '0'


# ---------------- модель 2: взвешенный счёт с затуханием ----------------
M2P = dict(W={'sam': 1.0, 'pomosch': 0.35, 'dom': 0.1}, HL=21, A0=2.0, P0=0.5)


def vzves(xs, today, par=M2P, blank_fail=True):
    """p = (Σ w·верно + A0·P0) / (Σ w + A0), w = вес режима · 0,5^(возраст/HL). Возвращает (оценка, p, w_сам, дней_сам)."""
    sw = swy = ws = 0.0; dsam = set()
    for x in xs:
        if not used(x, blank_fail): continue
        w = par['W'][x['mode']] * 0.5 ** ((today - x['d']).days / par['HL'])
        sw += w; swy += w * (x['v'] == '+')
        if x['mode'] == 'sam': ws += w; dsam.add(x['d'])
    p = (swy + par['A0'] * par['P0']) / (sw + par['A0'])
    if sw < 0.3: g = '—'
    elif p < 0.5: g = '0'
    elif ws < 0.67: g = 'П'
    elif p >= 0.8 and len(dsam) >= 2: g = 'У'
    elif p >= 0.67: g = 'С'
    else: g = 'П'
    return g, p, ws, len(dsam)


# ---------------- модель 3: BKT ----------------
BKTP = dict(L0=0.3, T=0.15, g={'sam': 0.15, 'pomosch': 0.6, 'dom': 0.75}, s={'sam': 0.1, 'pomosch': 0.05, 'dom': 0.05})


def bkt(xs, par=BKTP, blank_fail=True):
    """Bayesian Knowledge Tracing: P(знает) обновляется по каждому пункту (угадывание g и ошибка s зависят от режима),
    после каждого события — переход «выучил» с вероятностью T. Возвращает (оценка, L, P(верно на КР), было ли самостоятельное)."""
    L = par['L0']; cur = None; n = 0; had_sam = False
    for x in xs:
        if not used(x, blank_fail): continue
        if cur is not None and x['ev'] != cur: L = L + (1 - L) * par['T']
        cur = x['ev']; n += 1; had_sam |= x['mode'] == 'sam'
        g, s = par['g'][x['mode']], par['s'][x['mode']]
        if x['v'] == '+': L = L * (1 - s) / (L * (1 - s) + (1 - L) * g)
        else: L = L * s / (L * s + (1 - L) * (1 - g))
    if cur is not None: L = L + (1 - L) * par['T']
    pc = L * (1 - par['s']['sam']) + (1 - L) * par['g']['sam']
    if n == 0: return '—', L, pc, False
    g = '0' if L < 0.4 else 'П' if L < 0.7 else 'С' if L < 0.95 else 'У'
    return g, L, pc, had_sam


# ---------------- сила по теме (насколько хорошо решает) ----------------
TRI_POROG = {'LS': 2, 'KR': 2, 'ML': 4}
VES_TRI = {'LS': 1, 'KR': 2, 'ML': 1}        # [M] как klaster.py: в листках ○+△+доп поровну, на КР ○ + 2·△


def sila(B, cut, rezhim='ew', hl=14):
    """Сила по теме = «насколько хорошо решает». Перцентиль-ранг ребёнка в каждом классном событии (листок, КР;
    балл = ○ верно + вес·△ верно + доп верно, все пункты, включая неразмеченные по навыкам), среднее по событиям до cut:
    'cum' — поровну, 'last' — только последнее, 'ew' — с затуханием (полураспад hl дней).
    Р155 владельца: решил ≥ 3 △ и нет ни одной ошибки в ○ — все ○ события засчитаны.
    △-сигнал события: △ верно ≥ min(порог, число △ в событии). Возвращает {ребёнок: (s, △-сигналов, событий)}."""
    evs = [e for e, s in B.sob.items() if s['tip'] in ('LS', 'KR', 'ML') and (cut is None or s['seq'] <= cut)]
    no = defaultdict(int); ntri = defaultdict(int)
    for (e, p), r in B.punkt.items():
        if e in evs: no[e] += r['uroven'] == '○'; ntri[e] += r['uroven'] == '△'
    agg = defaultdict(lambda: dict(o=0, ow=0, t=0, d=0))
    for x in B.obs:
        if x['ev'] not in evs: continue
        a = agg[(x['ev'], x['c'])]
        if x['lvl'] == '○': a['o'] += x['v'] == '+'; a['ow'] += x['v'] != '+'
        elif x['lvl'] == '△': a['t'] += x['v'] == '+'
        else: a['d'] += x['v'] == '+'
    sc = defaultdict(dict); tri = defaultdict(dict)
    for (e, c), a in agg.items():
        tip = B.sob[e]['tip']
        o = no[e] if (a['t'] >= min(3, ntri[e]) and a['t'] > 0 and a['ow'] == 0) else a['o']
        sc[e][c] = o + VES_TRI[tip] * a['t'] + a['d']; tri[e][c] = a['t']
    today = max(B.sob[e]['d'] for e in evs)
    cls = [e for e in evs if B.sob[e]['tip'] in ('LS', 'KR')]
    R = {}
    for e in cls:
        xs = sc[e]; vals = sorted(xs.values()); n = len(vals)
        R[e] = {k: ((vals.index(v) + n - 1 - vals[::-1].index(v)) / 2) / max(1, n - 1) for k, v in xs.items()}
    # «единица» = (день, тип): два листка 22.09 усредняются в одну, листок и КР одного дня — разные (как «дни» в klaster.py)
    out = {}
    for c in B.deti:
        pres = [e for e in cls if c in R[e]]
        if not pres: out[c] = (None, 0, 0); continue
        byd = defaultdict(list)
        for e in pres: byd[(B.sob[e]['d'], B.sob[e]['tip'])].append(R[e][c])
        dd = sorted(byd)
        if rezhim == 'last': ws = {dd[-1]: 1.0}
        elif rezhim == 'cum': ws = {u: 1.0 for u in dd}
        else: ws = {u: 0.5 ** ((today - u[0]).days / hl) for u in dd}
        s = sum(sum(byd[u]) / len(byd[u]) * w for u, w in ws.items()) / sum(ws.values())
        nt = sum(1 for e in evs if tri[e].get(c, 0) >= min(TRI_POROG[B.sob[e]['tip']], ntri[e]) and tri[e].get(c, 0) > 0)
        out[c] = (s, nt, len(dd))
    return out


# ---------------- кластер ----------------
CUT = dict(V=0.55, NI=0.40, SN=0.25)          # [M] пороги силы; верх ещё требует ≥2 △-сигналов (как klaster.py)


def klaster_syroj(s, nt, ndn, ndn_vsego, n_sam, prev=None, delta=0.0):
    """Уровень по теме. s — сила, nt — △-сигналов, ndn — дней с работой из ndn_vsego, n_sam — навыков минимума на «сам»/«уверенно».
    Мало данных — меньше min(3, дней всего) дней. Верх [M] — s ≥ 0,55 и ≥ 2 △-сигналов (как klaster.py).
    Самый низ [M] — s < 0,25 И самостоятельно («сам»/«уверенно») не больше одного навыка минимума. Низ — s < 0,40. Иначе середина.
    prev+delta — гистерезис: пороги над текущим уровнем сдвинуты вверх на delta, под ним — вниз; удержаться в верхе — 1 △-сигнал."""
    if s is None or ndn < min(3, ndn_vsego): return 'Н'
    def c(name, lvl_above):
        base = CUT[name]
        if prev is None or prev == 'Н': return base
        return base + delta if LV.index(prev) < LV.index(lvl_above) else base - delta
    tri_need = 2 if prev != 'В' else 1
    if s >= c('V', 'В') and nt >= min(tri_need, ndn_vsego): return 'В'
    if s < c('SN', 'Ни') and n_sam <= 1: return 'СН'
    if s < c('NI', 'Ц'): return 'Ни'
    return 'Ц'


def shag(prev, new):
    """Не больше одного уровня за пересчёт [M]."""
    if prev in (None, 'Н') or new == 'Н': return new
    i, j = LV.index(prev), LV.index(new)
    return LV[i + (1 if j > i else -1)] if abs(j - i) > 1 else new
