# -*- coding: utf-8 -*-
"""Черновая кластеризация 7И (спецмат, школа 57) по сдаче задач 15.09–6.10.
Запуск: python3 klaster.py [папка_данных]  → печать сводки + KLASTERY-7I-chernovik.md рядом со скриптом.
Данные только читаются. Чужой код не исполняется: вердикты КР 6.10 берутся из svod_kr_6-10.py через ast.literal_eval
(словарь V), КР 29.09 — восстановлены здесь по ключу (OTSENKA-KR-29-09.json в выгрузке нет) и сверены с итогами ITOGI-2026-10-05/01-klass.md.
Метки: F — посчитано из данных; M — модельное допущение (правило, выбранное здесь); H — гипотеза."""
import ast, csv, json, os, re, sys, statistics as st
from collections import Counter, OrderedDict

D = sys.argv[1] if len(sys.argv) > 1 else '/mnt/user-data/uploads/GitHub/materials/diskmat-57/2026-08-18_logika-goda-7'
I29 = f'{D}/iteracii/2026-09-29_kombinatorika-2'
I06 = f'{D}/iteracii/2026-10-06_kontrolnaya-i-chetnost'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'KLASTERY-7I-chernovik.md')

# ---------------- ростер и сведение имён ----------------
ROSTER = ['Александров Авдей', 'Андронова Аглая', 'Атутов Кирилл', 'Бердичевский Петр', 'Блидман Наталия', 'Брызгалова Дарья',
          'Букия Алексей', 'Вигель Владимир', 'Вишницкий Даниил', 'Голухов Уильям', 'Гороховатская Екатерина', 'Дроздов Александр',
          'Дубков Егор', 'Егорова Алиса', 'Иванова Александра', 'Идрисова Ясмин', 'Исаева Вера', 'Карцев Фёдор', 'Кондаурова София',
          'Левандовский Илья', 'Литвиненко Ярослав', 'Мосина Анна', 'Неверов Андрей', 'Николаев Ярослав', 'Сычев Никита',
          'Трибунский Глеб', 'Юнгельсон Марк', 'Юстус Мария']
SUR = {r.split()[0]: r for r in ROSTER}
ALIAS = {'Лебедовский': 'Левандовский', 'Титус': 'Юстус', 'Гороховская': 'Гороховатская', 'Лявиченко': 'Литвиненко',
         'Митвиненко': 'Литвиненко', 'Любименко': 'Литвиненко', 'Випель': 'Вигель', 'Вильчинский': 'Вишницкий',
         'Ятутов': 'Атутов', 'Идрилова': 'Идрисова', 'Сычёв': 'Сычев', 'Идрисов': 'Идрисова'}
NAMEFLAGS = []          # (событие, как записано, кому отнесено, почему сомнительно)

def who(raw, ev, extra_flag=None):
    if not raw:
        NAMEFLAGS.append((ev, '(пусто)', '—', extra_flag or 'подписи нет, не отнесено')); return None
    s = raw.replace('ё', 'е').replace('Ё', 'Е')
    toks = re.findall(r'[А-ЯA-Z][а-яa-z]+', s)
    for t in toks:
        t2 = ALIAS.get(t, t)
        for k, v in SUR.items():
            if k.replace('ё', 'е') == t2.replace('ё', 'е'):
                if t != t2 or extra_flag or '(' in raw:
                    NAMEFLAGS.append((ev, raw, v, extra_flag or (f'написано «{t}»' if t != t2 else 'пометка в источнике')))
                return v
    NAMEFLAGS.append((ev, raw, '—', 'не сопоставлено')); return None

def rows_csv(p):
    out, head = [], None
    for r in csv.reader(open(p, encoding='utf-8'), delimiter=';'):
        if r and r[0] == 'фамилия_имя': head = r; continue
        out.append(dict(zip(head, r)) | {'_cells': r})
    return out
def jl(p): return [json.loads(l) for l in open(p, encoding='utf-8') if l.strip()]

E = OrderedDict()       # событие -> {ребёнок: dict}
EV_INFO = OrderedDict()

# ---- 15.09 логика (12 задач) и обратный ход (10): без ○/△ (F), «в»/«+» засчитаны как в CSV
for key, fn, n in (('L15', 'SDACHA-15-09_logika.csv', 12), ('OH15', 'SDACHA-15-09_obratnyj-hod.csv', 10)):
    E[key] = {}
    for r in rows_csv(f'{D}/{fn}'):
        c = who(r['фамилия_имя'], key, 'опознан(а) без подписи' if '(' in r['фамилия_имя'] else None)
        if r.get('вариант', '').startswith(('ЛИСТКА', 'НЕ БЫЛА')): continue
        zach = int(r['зачтено']); E[key][c] = dict(score=zach, share=zach / n, o=None, tri=None)
EV_INFO['L15'] = 'листок «Логика» 15.09, 12 задач, класс'
EV_INFO['OH15'] = 'листок «Обратный ход» 15.09, 10 задач, класс'

# ---- 22.09 подсчёты: ○ = 1а…5 (11 пунктов), △ = 6–9, доп = 10+ (M: границы блоков выведены из того, кто их пропускал)
E['P22'] = {}
for r in rows_csv(f'{D}/SDACHA-22-09_podschety.csv'):
    c = who(r['фамилия_имя'], 'P22'); cells = r['_cells']
    o = cells[3:14]; t = cells[14:18]; dop = cells[18:-1]
    no, nt, nd = o.count('+'), t.count('+'), dop.count('+')
    via_tri = no == 0 and nt >= 3                     # M: перенос Р155 («решил △ — ○ засчитаны»)
    oc = 11 if via_tri else no
    E['P22'][c] = dict(score=oc + nt + nd, share=None, o=oc / 11, tri=nt, tri_n=4, dop=nd, via_tri=via_tri)
EV_INFO['P22'] = 'листок «Подсчёты» 22.09: ○ 11 пунктов, △ 4, доп'
# ---- 22.09 инфографика: ○ = з1–11, △ = з12–15, доп = з16+; «в» засчитано (так в CSV)
E['I22'] = {}
for r in rows_csv(f'{D}/SDACHA-22-09_infografika.csv'):
    c = who(r['фамилия_имя'], 'I22'); cells = r['_cells']
    ok = lambda x: x in ('+', 'в')
    o = cells[2:13]; t = cells[13:17]; dop = cells[17:-1]
    no, nt, nd = sum(map(ok, o)), sum(map(ok, t)), sum(map(ok, dop))
    via_tri = all(x == 'в' for x in o)
    E['I22'][c] = dict(score=int(r['зачтено']), share=None, o=no / 11, tri=nt, tri_n=4, dop=nd, via_tri=via_tri)
EV_INFO['I22'] = 'листок «Инфографика» 22.09: ○ 11, △ 4, доп'
# ---- 23.09 логика: 3 анонимных листа → в матрицу не входит (F)
anon23 = sum(1 for _ in open(f'{D}/SDACHA-23-09_logika.csv', encoding='utf-8')) - 1

# ---- 29.09 листок: ○ 10 пунктов (1–5), △ 6–8, доп 9+; лагерь/вершина из CSV
E['LS29'] = {}
for r in rows_csv(f'{I29}/SDACHA.csv'):
    c = who(r['фамилия_имя'], 'LS29'); cells = r['_cells']
    ok = lambda x: x in ('+', 'в')
    o, t, dop = cells[2:12], cells[12:15], cells[15:33]
    no, nt, nd = sum(map(ok, o)), sum(map(ok, t)), sum(map(ok, dop))
    camp, peak = int(r['лагерь']), int(r['вершина'])
    via_tri = nt == 3 and camp == 1                   # Р155: решил △ — ○ засчитаны (F: правило владельца)
    oc = 10 if via_tri else no
    E['LS29'][c] = dict(score=oc + nt + nd, share=None, o=oc / 10, tri=nt, tri_n=3, dop=nd, via_tri=via_tri, camp=camp, peak=peak)
EV_INFO['LS29'] = 'листок «Комбинаторика 2» 29.09: ○ 10, △ 3, доп 18; Р155 применено'

# ---- 29.09 КР: вердикты восстановлены по ключу (А: 64; 71,45; 390; 32; 27; 6 троек; 13 — Б: 69; 85,46; 475; 40; 31; 7 троек; 14)
KR29_P = ['1', '2а', '2б', '3а', '3б', '4а', '4б']
KR29 = {  # '+' верно, '-' неверно, '.' пусто. Сверка с 01-klass.md ниже (assert).
 'Дроздов Александр': '++++++-', 'Голухов Уильям': '-+--++-', 'Трибунский Глеб': '++-++--', 'Брызгалова Дарья': '++.-+--',
 'Карцев Фёдор': '+++++++', 'Вигель Владимир': '+---++-', 'Вишницкий Даниил': '++-----', 'Блидман Наталия': '-+.-+-.',
 'Юстус Мария': '-++-++-', 'Сычев Никита': '+--++++', 'Андронова Аглая': '-+-++--', 'Дубков Егор': '-+-++--',
 'Мосина Анна': '++-++--', 'Иванова Александра': '---+---', 'Гороховатская Екатерина': '++-+++-', 'Исаева Вера': '--.-+..',
 'Юнгельсон Марк': '--+-+--', 'Неверов Андрей': '-+-+++-', 'Литвиненко Ярослав': '+++++-.', 'Идрисова Ясмин': '---++--',
 'Кондаурова София': '---.+..', 'Николаев Ярослав': '++-++--', 'Бердичевский Петр': '++-+++-', 'Александров Авдей': '+..++-.',
 'Атутов Кирилл': '-+-++..', 'Егорова Алиса': '-+.-+..', 'Левандовский Илья': '----+-.'}
KR29_NOTE = {'Мосина Анна': '2б: перечтение читает 380 (не 390) → «−»; в 01-klass.md засчитано (там 6 верных, здесь 5)',
             'Голухов Уильям': '2а: «95/85» — неуверенное чтение, засчитано как в 01-klass.md',
             'Вигель Владимир': '3б: «Г-116, В-31» засчитано как в 01-klass.md; фамилия по силуэту (перечтение: низкая уверенность)',
             'Александров Авдей': '1: засчитано по правилу 6½ (верный ход, обсчёт)'}
ITOGI29 = {'1': 13, '2а': 18, '2б': 6, '3а': 16, '3б': 25, '4а': 9, '4б': 2}
razm29 = {who(d['imya'], 'KR29', 'фамилия в списке «неуверенно»' if 'imya' in d['neuvereno'] else None): d for d in jl(f'{I29}/RAZMETKA-KR-29-09.jsonl')}
assert set(razm29) == set(KR29), set(razm29) ^ set(KR29)
kr29_tot = {p: sum(KR29[k][i] == '+' for k in KR29) for i, p in enumerate(KR29_P)}
kr29_diff = {p: (kr29_tot[p], ITOGI29[p]) for p in KR29_P if kr29_tot[p] != ITOGI29[p]}
assert kr29_diff == {'2б': (5, 6)}, kr29_diff      # единственное расхождение — Мосина 2б по перечтению
E['KR29'] = {k: dict(score=v.count('+'), share=v.count('+') / 7, verd=v, var=razm29[k]['var']) for k, v in KR29.items()}
EV_INFO['KR29'] = 'контрольная 29.09, 7 пунктов, сам, ~20 мин'

# ---- 6.10 КР: вердикты аналитика из svod_kr_6-10.py (literal_eval, не exec)
src = open(f'{I06}/raspoznavanie/svod_kr_6-10.py', encoding='utf-8').read()
vtxt = src[src.index('V={') + 2: src.index('\nrows=')]
vtxt = vtxt.replace("'+-+--++-----—'.replace('—','-')", "'+-+--++------'").replace("'++.++++......'[:12]+'-'", "'++.++++.....-'")
KR06 = ast.literal_eval(re.sub(r'#[^\n]*', '', vtxt))
assert len(KR06) == 26 and all(len(v[1]) == 13 for v in KR06.values())
KR06_P = '1а 1б 2а 2б 3а 3б 4 5а 5б 5в 6а 6б 6в'.split()
razm06 = {}
for d in jl(f'{I06}/raspoznavanie/RAZMETKA-KR-06-10.jsonl'):
    fl = 'фамилия «неуверенно»' if any('imya' in str(x) for x in d.get('neuvereno', [])) else None
    if not d['imya_kak_napisano']: fl = 'подписи нет; имя восстановлено (ДЗ + почерк)'
    razm06[who(d['imya'] if fl is None or d['imya_kak_napisano'] else d['imya'], 'KR06', fl)] = d
E['KR06'] = {}
for k, (var, s, tri, note) in KR06.items():
    k2 = who(k, 'KR06_svod'); NAMEFLAGS.pop() if NAMEFLAGS and NAMEFLAGS[-1][0] == 'KR06_svod' else None
    only_tri = set(s) == {'.'}
    o = s.count('+')
    via_tri = tri >= 3 and '-' not in s                # M: перенос Р155 на КР (△ ≥ 3 из 8 и ни одной ошибки в ○)
    oc = 13 if via_tri else o
    E['KR06'][k2] = dict(score=oc + 2 * tri, o=None if only_tri else o / 13, oraw=o, tri=tri, tri_n=8, verd=s, var=var,
                         only_tri=only_tri, via_tri=via_tri, note=note)
EV_INFO['KR06'] = 'контрольная 6.10: ○ 13 пунктов, △ 8 пунктов; балл для ранга = ○ + 2·△ (M)'

# ---- 6.10 мини-листок (уровень △, «для уверенных»): отметки проверяющего; у Атутова отметок нет — сверка с принятыми ответами варианта
ML = jl(f'{I06}/raspoznavanie/RAZMETKA-MINILISTOK-6-10.jsonl')
acc = {}
for d in ML:
    for z, m in d['o'].items():
        if m == '+': acc.setdefault((d['var'], z), set()).add(d['n'][z].strip())
E['ML06'] = {}; ml_anon = []
for d in ML:
    c = who(d['imya'] or '', 'ML06', ('подписи нет; рядом в стопке Карцев и Литвиненко' if not d['imya'] else 'фамилия «неуверенно»') if 'imya' in d['neuvereno'] else None)
    if all(m == 'z' for m in d['o'].values()):
        def val(a):                                   # «4+3+1» → «8»: ответ выражением
            a = a.split('=')[-1].strip()
            return str(sum(map(int, a.split('+')))) if re.fullmatch(r'\d+(\+\d+)+', a) else a
        ok = sum(val(a) in acc.get((d['var'], z), set()) for z, a in d['n'].items())
        checked = False
    else:
        ok = sum(m == '+' for m in d['o'].values()); checked = True
    if c is None: ml_anon.append((d['var'], ok)); continue
    E['ML06'][c] = dict(score=ok, share=ok / 6, checked=checked)
EV_INFO['ML06'] = 'мини-листок «Умный перебор» 6.10 (весь уровня △), 6 задач, по выбору'

# ---- ДЗ: только факт сдачи (по ДЗ знание не судим — 01-klass.md); совпадение с ключом — справочно
DZ29_KEY = {'1': '8', '2': '14', '3': '34', '4': '22', '5': '12'}
DZ06_KEY = {'1': ('2,25', '2 мин 15', '135'), '2': ('12',), '3': ('50',), '4': ('33',), '5': ('140',), '6': ('45',)}
def last_num(a):
    a = a.replace('2 1/4', '2,25'); nums = re.findall(r'\d+(?:[.,]\d+)?', a); return nums
def dz_ok(n, key):
    s = 0
    for z, a in n.items():
        if z not in key: continue
        ks = key[z] if isinstance(key[z], tuple) else (key[z],)
        tail = a.split('|')[0].split('=')[-1]
        if any(k in a for k in ('2 мин 15', '135')) and z == '1' and '2,25' in ks: s += 1; continue
        nums = last_num(tail)
        if nums and nums[0].replace('.', ',') in ks: s += 1
    return s
for d in jl(f'{D}/RAZMETKA-22-09.jsonl'):        # исходная разметка 22.09: только сверка имён (баллы — из CSV)
    who(d['imya'], 'разметка 22.09')
for d in jl(f'{I29}/RAZMETKA-LISTOK-29-09.jsonl'):  # исходная разметка листка 29.09: только сверка имён
    who(d['imya_kak_napisano'], 'разметка Л29', '«(?)» в разметке' if '(?)' in d['imya_kak_napisano'] else None)
E['DZ29'] = {}; E['DZ06'] = {}
for d in jl(f'{I29}/RAZMETKA-DZ-k-29-09.jsonl'):
    fl = 'подпись «Идрисов Дан…» — отнесено к Идрисовой разметчиком' if d['imya_kak_napisano'].startswith('Идрисов ') else None
    c = who(d['imya'], 'DZ29', fl)
    E['DZ29'][c] = dict(score=dz_ok(d['n'], DZ29_KEY), late=False)
per = {}
for p in jl(f'{I06}/raspoznavanie/RAZMETKA-DZ-k-6-10_perechtenie.jsonl'): per[(p['foto'], p['zadacha'])] = p['n']
for d in jl(f'{I06}/raspoznavanie/RAZMETKA-DZ-k-6-10.jsonl'):
    fl = 'фамилия «неуверенно»' if 'imya' in d.get('neuvereno', []) else None
    c = who(d['imya'], 'DZ06', fl)
    n = {z: per.get((d['foto'][0], z), a) for z, a in d['n'].items()}   # перечтение главнее
    if len(d['o']) == 5:            # запоздавшее ДЗ к 29.09 в стопке 6.10
        E['DZ29'][c] = dict(score=dz_ok(n, DZ29_KEY), late=True)
    else:
        prev = E['DZ06'].get(c, {}).get('score', -1)
        E['DZ06'][c] = dict(score=max(prev, dz_ok(n, DZ06_KEY)))
EV_INFO['DZ29'] = 'ДЗ к 29.09 (5 задач), дома'
EV_INFO['DZ06'] = 'ДЗ к 6.10 (6 задач), дома'

CLASS_EV = ['L15', 'OH15', 'P22', 'I22', 'LS29', 'KR29', 'KR06']   # классные события (ранги); ML06 по выбору, ДЗ — нет
COMB_EV = ['P22', 'I22', 'LS29', 'KR29', 'KR06']

# ---------------- признаки по ребёнку ----------------
def pct_rank(ev):
    """Перцентиль-ранг 0..1 по score внутри события (средний ранг при равенстве)."""
    xs = {k: v['score'] for k, v in E[ev].items() if k}
    vals = sorted(xs.values()); n = len(vals)
    r = {}
    for k, x in xs.items():
        lo = vals.index(x); hi = n - 1 - vals[::-1].index(x)
        r[k] = ((lo + hi) / 2) / (n - 1)
    return r
R = {ev: pct_rank(ev) for ev in CLASS_EV}

def spearman(a, b):
    ks = [k for k in E[a] if k in E[b] and k]
    if len(ks) < 5: return None, len(ks)
    ra = {k: v for k, v in R_sub(a, ks).items()}; rb = R_sub(b, ks)
    ma, mb = st.mean(ra.values()), st.mean(rb.values())
    num = sum((ra[k] - ma) * (rb[k] - mb) for k in ks)
    den = (sum((ra[k] - ma) ** 2 for k in ks) * sum((rb[k] - mb) ** 2 for k in ks)) ** .5
    return num / den, len(ks)
def R_sub(ev, ks):
    xs = {k: E[ev][k]['score'] for k in ks}; vals = sorted(xs.values()); n = len(vals)
    return {k: (vals.index(x) + n - 1 - vals[::-1].index(x)) / 2 for k, x in xs.items()}

P = {}
for k in ROSTER:
    p = dict(name=k)
    p['pres'] = [ev for ev in CLASS_EV if k in E[ev]]
    p['n_pres'] = len(p['pres'])
    p['comb_pres'] = [ev for ev in COMB_EV if k in E[ev]]
    # основной ранг — только комбинаторика (22.09 = среднее двух листков одного дня), как в 01-klass.md; логика 15.09 — отдельно
    rk = []
    if any(k in E[ev] for ev in ('P22', 'I22')): rk.append(st.mean(R[ev][k] for ev in ('P22', 'I22') if k in E[ev]))
    rk += [R[ev][k] for ev in ('LS29', 'KR29', 'KR06') if k in E[ev]]
    p['rank'] = st.mean(rk) if rk else None
    p['rank_log'] = st.mean(R[ev][k] for ev in ('L15', 'OH15') if k in E[ev]) if any(k in E[ev] for ev in ('L15', 'OH15')) else None
    p['days'] = [d for d, evs in (('22.09', ('P22', 'I22')), ('Л29', ('LS29',)), ('КР29', ('KR29',)), ('КР06', ('KR06',))) if any(k in E[ev] for ev in evs)]
    p['n_kr'] = (k in E['KR29']) + (k in E['KR06'] and not E['KR06'][k]['only_tri'])
    os_ = [E[ev][k]['o'] for ev in ('P22', 'I22', 'LS29') if k in E[ev]]
    if k in E['KR06'] and E['KR06'][k]['o'] is not None: os_.append(E['KR06'][k]['o'])
    p['o_mean'] = st.mean(os_) if os_ else None
    p['o_n'] = len(os_)
    # △-сигналы (F: факты, порог — M): событие засчитывается как «шёл вверх», если
    sig = []
    if any(k in E[ev] and E[ev][k]['tri'] >= 3 for ev in ('P22', 'I22')): sig.append('22.09')
    if k in E['LS29'] and (E['LS29'][k]['tri'] >= 2 or E['LS29'][k]['peak']): sig.append('LS29')
    if k in E['KR29'] and E['KR29'][k]['verd'][6] == '+': sig.append('KR29-4б')
    if k in E['KR06'] and E['KR06'][k]['tri'] >= 2: sig.append('KR06')
    if k in E['ML06'] and E['ML06'][k]['score'] >= 4: sig.append('ML06')
    p['tri_sig'] = sig
    p['kr29'] = E['KR29'][k]['score'] if k in E['KR29'] else None
    p['kr06o'] = E['KR06'][k]['oraw'] if k in E['KR06'] and not E['KR06'][k]['only_tri'] else None
    p['kr06t'] = E['KR06'][k]['tri'] if k in E['KR06'] else None
    p['via06'] = k in E['KR06'] and E['KR06'][k]['via_tri']
    p['d_kr'] = (p['kr06o'] / 13 - p['kr29'] / 7) if p['kr29'] is not None and p['kr06o'] is not None and not p['via06'] else None
    # приёмы (соответствие — из sravnenie_kr_29-09_6-10.py)
    MAP = {'±1': (['1'], ['1а', '1б', '2а', '2б']), 'ВИ': (['2б'], ['3а', '3б']), 'перебор': (['4а', '4б'], ['4', '6в'])}
    p['priem'] = {}
    for t, (a, b) in MAP.items():
        x = f"{sum(E['KR29'][k]['verd'][KR29_P.index(q)] == '+' for q in a)}/{len(a)}" if k in E['KR29'] else '—'
        y = (f"{sum(E['KR06'][k]['verd'][KR06_P.index(q)] == '+' for q in b)}/{len(b)}"
             if k in E['KR06'] and not E['KR06'][k]['only_tri'] and not E['KR06'][k]['via_tri'] else '—')
        p['priem'][t] = (x, y)
    p['dz'] = ('29' if k in E['DZ29'] else '') + ('*' if k in E['DZ29'] and E['DZ29'][k]['late'] else '') + (' 6' if k in E['DZ06'] else '')
    p['ml'] = E['ML06'][k]['score'] if k in E['ML06'] else None
    P[k] = p

# ---------------- кластеры ----------------
# (1) правило (M, по-человечески): мало данных — < 3 из 4 комбинаторных «дней» (22.09, листок 29.09, КР 29.09, КР 6.10);
#     верх — ≥ 2 событий с △-сигналом И средний ранг ≥ 0,55; низ — средний ранг < 0,40 и △-сигналов ≤ 1; иначе центр.
def rule(p):
    if len(p['days']) < 3: return 'Н'
    if len(p['tri_sig']) >= 2 and p['rank'] >= 0.55: return 'В'
    if p['rank'] < 0.40 and len(p['tri_sig']) <= 1: return 'Ни'
    return 'Ц'
for p in P.values(): p['rule'] = rule(p)

# (2) разрывы в среднем ранге (как klastery.py в 01-klass.md): два самых больших разрыва среди видимых
vis = sorted([p for p in P.values() if p['rule'] != 'Н'], key=lambda p: -p['rank'])
gaps = sorted(((vis[i]['rank'] - vis[i + 1]['rank'], i) for i in range(len(vis) - 1)), reverse=True)
# разрывы ищем только так, чтобы в каждом куске было ≥ 3 человек
cuts = []
for g, i in gaps:
    if all(abs(i - c) >= 3 for c in cuts) and 2 <= i <= len(vis) - 4:
        cuts.append(i)
    if len(cuts) == 2: break
cuts.sort()
for j, p in enumerate(vis):
    p['gap'] = 'В' if j <= cuts[0] else ('Ц' if j <= cuts[1] else 'Ни')
for p in P.values(): p.setdefault('gap', 'Н')

# (3) k-means k=3 на двух осях: X = средний ранг (все классные), Y = доля событий с △-сигналом из присутствий; детерминированный старт
pts = {p['name']: (p['rank'], len(p['tri_sig']) / (len(p['days']) + (1 if p['ml'] is not None else 0))) for p in vis}
ys = [v[1] for v in pts.values()]; xs = [v[0] for v in pts.values()]
sx, sy = st.pstdev(xs) or 1, st.pstdev(ys) or 1
Z = {k: ((x - st.mean(xs)) / sx, (y - st.mean(ys)) / sy) for k, (x, y) in pts.items()}
srt = sorted(Z, key=lambda k: Z[k][0] + Z[k][1])
C = [Z[srt[0]], Z[srt[len(srt) // 2]], Z[srt[-1]]]
for _ in range(100):
    lab = {k: min(range(3), key=lambda c: (z[0] - C[c][0]) ** 2 + (z[1] - C[c][1]) ** 2) for k, z in Z.items()}
    C2 = [tuple(st.mean(Z[k][d] for k in lab if lab[k] == c) for d in (0, 1)) for c in range(3)]
    if C2 == C: break
    C = C2
order = sorted(range(3), key=lambda c: C[c][0] + C[c][1])
KL = {order[0]: 'Ни', order[1]: 'Ц', order[2]: 'В'}
for k, c in lab.items(): P[k]['km'] = KL[c]
for p in P.values(): p.setdefault('km', 'Н')

def agree(p): return len({p['rule'], p['gap'], p['km']})
LV = {'В': 'верх', 'Ц': 'центр', 'Ни': 'низ', 'Н': 'мало данных'}

# ---------------- корреляции событий (Спирмен по общим детям) ----------------
CORR_EV = CLASS_EV + ['DZ29', 'DZ06']
corr = {(a, b): spearman(a, b) for i, a in enumerate(CORR_EV) for b in CORR_EV[i + 1:]}

# ---------------- печать / md ----------------
f2 = lambda x: '—' if x is None else f'{x:.2f}'.replace('.', ',')
pc = lambda x: '—' if x is None else f'{round(100 * x)}%'
L = []
w = L.append
w('# 7И: черновая кластеризация по сдаче 15.09–6.10\n')
w('*Черновик. Всё ниже пересчитывается `python3 klaster.py` (папка данных — аргумент). '
  'Метки: **[F]** посчитано из данных · **[M]** модельное допущение (правило выбрано здесь) · **[H]** гипотеза.*\n')
w('## 0. Источники и что из них взято\n')
w('| код | событие | детей | как считается |\n|---|---|---|---|')
for ev in ['L15', 'OH15', 'P22', 'I22', 'LS29', 'KR29', 'DZ29', 'DZ06', 'KR06', 'ML06']:
    n = len([k for k in E[ev] if k])
    how = {'L15': 'зачтено/12 («+» и «в»)', 'OH15': 'зачтено/10', 'P22': '○ 1а–5 (11), △ 6–9, доп 10+; ○ засчитаны при △≥3 и пустом ○ [M]',
           'I22': '○ з1–11, △ з12–15, доп з16+; «в» засчитано (как в CSV)', 'LS29': '○ 10, △ 3, доп 18; Р155: лагерь по △ → ○ засчитаны',
           'KR29': 'вердикты восстановлены по ключу (OTSENKA-KR-29-09.json нет в выгрузке), сверены с 01-klass.md',
           'DZ29': 'только факт сдачи (+3 поздних из стопки 6.10)', 'DZ06': 'только факт сдачи', 'KR06': 'вердикты svod_kr_6-10.py; ○/13, △/8',
           'ML06': 'отметки проверяющего; у Атутова отметок нет — сверено с принятыми ответами'}[ev]
    w(f'| {ev} | {EV_INFO[ev]} | {n} | {how} |')
w(f'\nЛогика 23.09 (`SDACHA-23-09_logika.csv`) — {anon23} листа, все без привязки к ребёнку; в матрицу не входит. '
  f'Мини-листок 6.10: {len(ml_anon)} лист без подписи (вар. {", ".join(v for v, _ in ml_anon)}, верно {", ".join(str(o) for _, o in ml_anon)}) — не отнесён.\n')
w(f'**Сверка КР 29.09 с 01-klass.md [F]:** по пунктам совпадает всё, кроме 2б: здесь {kr29_diff["2б"][0]}, там {kr29_diff["2б"][1]} '
  '(Мосина: перечтение читает 380, а не 390; перечтение главнее).\n')

w('## 1. Матрица ребёнок × событие [F]\n')
w('Ячейка: балл события (для листков — засчитано ○+△+доп с Р155; для КР 29.09 — из 7; для КР 6.10 — ○/13 и △/8). «·» — нет работы. '
  '△ — сколько задач △ решено. ДЗ: «29» сдано к 29.09 (* — поздно), «6» — к 6.10.\n')
w('| ребёнок | Л15 /12 | ОХ15 /10 | Подсч 22 (○%·△) | Инфогр 22 (○%·△) | Листок 29 (○%·△·лагерь) | КР29 /7 | КР06 ○/13·△/8 | мини 6.10 /6 | ДЗ |')
w('|---|---|---|---|---|---|---|---|---|---|')
def cell(ev, k):
    if k not in E[ev]: return '·'
    v = E[ev][k]
    if ev in ('L15', 'OH15'): return str(v['score'])
    if ev in ('P22', 'I22'): return f"{pc(v['o'])}·△{v['tri']}" + ('ᵛ' if v['via_tri'] else '')
    if ev == 'LS29': return f"{pc(v['o'])}·△{v['tri']}·{'Л' if v['camp'] else '–'}{'▲' if v['peak'] else ''}" + ('ᵛ' if v['via_tri'] else '')
    if ev == 'KR29': return str(v['score'])
    if ev == 'KR06': return ('только △' if v['only_tri'] else str(v['oraw'])) + f"·△{v['tri']}"
    if ev == 'ML06': return str(v['score']) + ('' if v['checked'] else '?')
for k in ROSTER:
    w(f"| {k} | {cell('L15', k)} | {cell('OH15', k)} | {cell('P22', k)} | {cell('I22', k)} | {cell('LS29', k)} | {cell('KR29', k)} | "
      f"{cell('KR06', k)} | {cell('ML06', k) if k in E['ML06'] else '·'} | {P[k]['dz'].strip() or '—'} |")
w('\nᵛ — ○ засчитаны «по △» (Р155 / перенос Р155). ▲ — вершина. «?» — проверяющий не отметил, сверено с принятыми ответами.\n')

w('## 2. Профиль ребёнка [F, кроме кластера]\n')
w('Явка — из 7 классных событий (Л15, ОХ15, Подсч, Инфогр, Листок 29, КР29, КР06). Дни — сколько из 4 комбинаторных «дней» есть (22.09, листок 29.09, КР 29.09, КР 6.10); '
  'КР — сколько самостоятельных КР с измеренными ○ (КР29; КР06, если писал ○). ○ — средняя доля ○ по листкам 22.09, 29.09 и ○ КР 6.10 (листки — с принимающими). '
  '△-сигналы — события, где ребёнок шёл вверх: 22.09 (△≥3 из 4 хотя бы в одном листке), Л29 (△≥2 из 3 или вершина), КР29-4б (верно), КР06 (△≥2 из 8), мини (≥4 из 6) [пороги M]. '
  'Ранг — средний перцентиль-ранг (0 худший, 1 лучший) по комбинаторике: 22.09 (два листка одного дня усреднены), листок 29.09, КР 29.09, КР 6.10 — как в 01-klass.md. '
  'Ранг лог. — то же по логике 15.09 (в кластеризацию не входит: см. §4, с комбинаторикой почти не согласуется). Δ КР — доля ○ 6.10 минус доля 29.09. '
  'Приёмы — КР29 → КР06 (соответствие из sravnenie_kr_29-09_6-10.py: ±1 = №1 → 1а,1б,2а,2б; ВИ = 2б → 3а,3б; перебор = 4а,4б → 4,6в).\n')
w('| ребёнок | явка | дни | КР | ○ ср. | △-сигналы | КР29 | КР06 ○ | КР06 △ | Δ КР | ±1 | ВИ | перебор | ранг | ранг лог. | правило | разрыв | k-means |')
w('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for k in sorted(ROSTER, key=lambda k: -(P[k]['rank'] or 0)):
    p = P[k]
    pr = lambda t: f"{p['priem'][t][0]}→{p['priem'][t][1]}"
    w(f"| {k} | {p['n_pres']}/7 | {len(p['days'])}/4 | {p['n_kr']} | {pc(p['o_mean'])} | {len(p['tri_sig'])} ({', '.join(p['tri_sig']) or '—'}) | {p['kr29'] if p['kr29'] is not None else '·'} | "
      f"{(str(p['kr06o']) + ('ᵛ' if p['via06'] else '')) if p['kr06o'] is not None else ('△' if k in E['KR06'] else '·')} | {p['kr06t'] if p['kr06t'] is not None else '·'} | "
      f"{'—' if p['d_kr'] is None else f'{round(100*p['d_kr']):+d} пп'} | {pr('±1')} | {pr('ВИ')} | {pr('перебор')} | {f2(p['rank'])} | {f2(p['rank_log'])} | "
      f"{LV[p['rule']]} | {LV[p['gap']]} | {LV[p['km']]} |")

w('\n## 3. Кластеры\n')
w('Три метода, все прозрачные:\n')
w('1. **Правило [M]** (основное): «мало данных» — меньше 3 из 4 комбинаторных дней; '
  '**верх** — ≥2 событий с △-сигналом и средний ранг ≥ 0,55; **низ** — средний ранг < 0,40 и не больше одного △-сигнала; остальные — **центр**.')
w(f'2. **Разрывы [M]** — как klastery.py из 01-klass.md: видимые дети по среднему рангу, режем по двум самым большим разрывам '
  f'(в куске ≥ 3 человек). Разрезы после позиций {cuts[0] + 1} и {cuts[1] + 1}: разрывы '
  f'{f2(vis[cuts[0]]["rank"] - vis[cuts[0] + 1]["rank"])} и {f2(vis[cuts[1]]["rank"] - vis[cuts[1] + 1]["rank"])}.')
w('3. **k-means, k = 3 [M]** на двух осях (стандартизованы): средний ранг и доля событий с △-сигналом. '
  'Не независим от правила: оси те же, что в правиле, поэтому совпадение с правилом — проверка порогов, а не подтверждение.\n')
top_gap = max(g for g, _ in gaps)
w(f'Самый большой разрыв в ранге между соседями — {f2(top_gap)} (в 01-klass.md был разрыв 0,12 между верхом и Николаевым). '
  'Резких границ нет: класс — непрерывная лестница, уровни режутся по договорённости [F о разрывах, M о порогах].\n')
cnt = {m: Counter(p[m] for p in P.values()) for m in ('rule', 'gap', 'km')}
w('| уровень | правило | разрывы | k-means |\n|---|---|---|---|')
for lv in ('В', 'Ц', 'Ни', 'Н'):
    w(f"| {LV[lv]} | {cnt['rule'][lv]} | {cnt['gap'][lv]} | {cnt['km'][lv]} |")
full = sum(agree(p) == 1 for p in P.values() if p['rule'] != 'Н'); nvis = sum(p['rule'] != 'Н' for p in P.values())
w(f'\nВсе три метода согласны у {full} из {nvis} видимых детей [F].\n')
for lv in ('В', 'Ц', 'Ни', 'Н'):
    grp = [P[k] for k in sorted(ROSTER, key=lambda k: -(P[k]['rank'] or 0)) if P[k]['rule'] == lv]
    if not grp: continue
    def mean_of(key):
        xs = [g[key] for g in grp if g[key] is not None]; return st.mean(xs) if xs else None
    kr29m = mean_of('kr29'); kr06m = mean_of('kr06o')
    w(f"### {LV[lv].capitalize()} — {len(grp)} чел.\n")
    w(f"Средний ранг {f2(mean_of('rank'))}; ○ ср. {pc(mean_of('o_mean'))}; △-сигналов в среднем {f2(st.mean(len(g['tri_sig']) for g in grp))}; "
      f"КР29 ср. {f2(kr29m)}/7; КР06 ○ ср. {f2(kr06m)}/13 (у писавших ○); явка ср. {f2(st.mean(g['n_pres'] for g in grp))}/7.\n")
    names = []
    for g in grp:
        mark = '' if agree(g) == 1 or lv == 'Н' else f" (разрывы: {LV[g['gap']]}, k-means: {LV[g['km']]})"
        names.append(g['name'] + mark)
    w('Состав: ' + '; '.join(names) + '.\n')

# пограничные
w('### Пограничные и особые случаи [F + H]\n')
border = [p for p in P.values() if p['rule'] != 'Н' and agree(p) > 1]
for p in sorted(border, key=lambda p: -p['rank']):
    w(f"- **{p['name']}**: правило — {LV[p['rule']]}, разрывы — {LV[p['gap']]}, k-means — {LV[p['km']]}; ранг {f2(p['rank'])}, △-сигналы: {', '.join(p['tri_sig']) or 'нет'}.")
spec = []
for k, v in E['KR06'].items():
    if v['only_tri'] and P[k]['rule'] != 'В':
        spec.append(f"- **{k}** на КР 6.10 писал(а) только △ ({v['tri']}/8), хотя по остальным событиям — {LV[P[k]['rule']]}. "
                    f"Его ○ на КР 6.10 не измерены.")
w('\n'.join(spec) + '\n')

w('## 4. Согласие событий между собой (Спирмен, по общим детям) [F]\n')
w('| пара | ρ | n |\n|---|---|---|')
for (a, b), (r, n) in corr.items():
    if r is None: continue
    if a in ('DZ29', 'DZ06') or b in ('DZ29', 'DZ06') or (a, b) in (('LS29', 'KR29'), ('KR29', 'KR06'), ('I22', 'LS29'), ('LS29', 'KR06'), ('P22', 'I22'), ('L15', 'OH15'), ('OH15', 'KR29'), ('L15', 'KR06')):
        w(f'| {a} ↔ {b} | {f2(r)} | {n} |')
dzr = [r for (a, b), (r, n) in corr.items() if r is not None and ('DZ' in a or 'DZ' in b) and not ('DZ' in a and 'DZ' in b)]
w(f'\nДЗ ↔ классные события: ρ от {f2(min(dzr))} до {f2(max(dzr))}. Ранг ДЗ здесь — число ответов, совпавших с ключом (грубо, справочно).\n')

# динамика
both = [p for p in P.values() if p['d_kr'] is not None]
up = [p['name'] for p in both if p['d_kr'] > .1]; dn = [p['name'] for p in both if p['d_kr'] < -.1]
w('## 5. Динамика КР 29.09 → КР 6.10 [F]\n')
w(f'Писали обе КР (6.10 — с ○): {len(both)}. Выросли > 10 пп: {len(up)}; упали > 10 пп: {len(dn)}; без изменений: {len(both) - len(up) - len(dn)}. '
  f'*Оговорка [M]: КР разные (7 и 13 пунктов, разные темы и трудность), Δ — разность долей, не «рост ребёнка».*\n')
MAP = {'±1': (['1'], ['1а', '1б', '2а', '2б']), 'ВИ': (['2б'], ['3а', '3б']), 'перебор': (['4а', '4б'], ['4', '6в'])}
w('| приём | КР 29.09 | КР 6.10 |\n|---|---|---|')
oba = [p['name'] for p in both]
for t, (a, b) in MAP.items():
    s1 = sum(E['KR29'][k]['verd'][KR29_P.index(q)] == '+' for k in oba for q in a); n1 = len(oba) * len(a)
    s2 = sum(E['KR06'][k]['verd'][KR06_P.index(q)] == '+' for k in oba for q in b); n2 = len(oba) * len(b)
    w(f'| {t} | {s1}/{n1} = {pc(s1 / n1)} | {s2}/{n2} = {pc(s2 / n2)} |')
w('\nПо уровням (правило), доля верных пунктов приёма на КР 6.10 у писавших ○ (без тех, кому ○ засчитаны по △):\n')
w('| приём | ' + ' | '.join(LV[l] for l in ('В', 'Ц', 'Ни')) + ' |\n|---|---|---|---|')
for t, (_, b) in MAP.items():
    row = []
    for lv in ('В', 'Ц', 'Ни'):
        ks = [k for k in E['KR06'] if not E['KR06'][k]['only_tri'] and not E['KR06'][k]['via_tri'] and P[k]['rule'] == lv]
        s = sum(E['KR06'][k]['verd'][KR06_P.index(q)] == '+' for k in ks for q in b); n = len(ks) * len(b)
        row.append(f'{s}/{n} = {pc(s / n)}' if n else '—')
    w(f'| {t} | ' + ' | '.join(row) + ' |')
w('')

w('## 6. Неоднозначные сопоставления имён [F]\n')
w('| событие | как записано | отнесено | почему сомнительно |\n|---|---|---|---|')
seen = set()
for ev, raw, to, why in NAMEFLAGS:
    if ev == 'KR06_svod' or (ev, raw) in seen: continue
    seen.add((ev, raw)); w(f'| {ev} | {raw} | {to} | {why} |')
w('')

# ---------------- 7. наблюдения, 8. стратификация, 9. дыры, 10. уровни листков ----------------
grp = {lv: [k for k in sorted(ROSTER, key=lambda k: -(P[k]['rank'] or 0)) if P[k]['rule'] == lv] for lv in ('В', 'Ц', 'Ни', 'Н')}
ri = lambda a, b: corr[(a, b)][0]
def dmean(lv):
    xs = [P[k]['d_kr'] for k in grp[lv] if P[k]['d_kr'] is not None]
    return f'{round(100 * st.mean(xs)):+d} пп (n={len(xs)})' if xs else '—'
gap_i = max(gaps)[1]
gap_top = [p['name'] for p in vis[:gap_i + 1]]
low_hi06 = [k for k in grp['Ни'] if P[k]['kr06o'] is not None and P[k]['kr06o'] >= 10]
big_d = sorted([p for p in both if abs(p['d_kr']) >= .4], key=lambda p: -p['d_kr'])
tri_only = [k for k, v in E['KR06'].items() if v['only_tri']]
ml_names = list(E['ML06'])
absent = {ev: [k for k in ROSTER if k not in E[ev]] for ev in ('L15', 'OH15', 'P22', 'LS29', 'KR29', 'KR06')}
nkr1 = [k for k in ROSTER if P[k]['n_kr'] <= 1 and P[k]['rule'] != 'Н']
def ks(xs): return ', '.join(x.split()[0] for x in xs)
pr_lv = {}
for t, (_, b) in MAP.items():
    for lv in ('В', 'Ц', 'Ни'):
        kk = [k for k in E['KR06'] if not E['KR06'][k]['only_tri'] and not E['KR06'][k]['via_tri'] and P[k]['rule'] == lv]
        pr_lv[(t, lv)] = sum(E['KR06'][k]['verd'][KR06_P.index(q)] == '+' for k in kk for q in b) / (len(kk) * len(b))

w('## 7. Главные наблюдения\n')
w(f"1. **Верх виден уверенно [F + M].** {len(grp['В'])} человек ({ks(grp['В'])}) — у каждого ≥ 2 независимых событий, где он шёл по △, и высокий ранг. "
  f"Самый большой разрыв ранга в классе ({f2(max(gaps)[0])}) отделяет верхние {len(gap_top)} ({ks(gap_top)}): это верх плюс {ks([x for x in gap_top if P[x]['rule'] != 'В'])} — "
  "сильные «по ○», но вверх почти не ходят. Мини-листок 6.10 взяли " + ', '.join(f"{x.split()[0]} ({LV[P[x]['rule']]})" for x in ml_names) + ".")
w(f"2. **Центр/низ — без границы [F].** Ниже верха ранги идут лестницей без разрывов; правило режет по 0,40 условно. "
  f"Низ по правилу — {len(grp['Ни'])} человек, это слишком много для одной группы: из них КР 6.10 ○ ≥ 10/13 написали {ks(low_hi06)} "
  "— по последней КР они на уровне центра.")
assert pr_lv[('перебор','Ни')] + .2 <= min(pr_lv[('перебор','В')], pr_lv[('перебор','Ц')]) and min(pr_lv[(t, l)] for t in ('±1', 'ВИ') for l in ('В', 'Ц', 'Ни')) >= .75
w(f"3. **КР 6.10 по ○ почти не различает класс [F].** ±1: {pc(pr_lv[('±1','В')])} / {pc(pr_lv[('±1','Ц')])} / {pc(pr_lv[('±1','Ни')])} (верх/центр/низ); "
  f"«ВИ»: {pc(pr_lv[('ВИ','В')])} / {pc(pr_lv[('ВИ','Ц')])} / {pc(pr_lv[('ВИ','Ни')])}. Различает только перебор — и отделяет низ, а не верх от центра: "
  f"{pc(pr_lv[('перебор','В')])} / {pc(pr_lv[('перебор','Ц')])} / {pc(pr_lv[('перебор','Ни')])}. Верх от центра отличают △, а не ○. "
  "*Оговорка [M]:* ○3 КР 6.10 («только шахматы / только футбол / никуда») решается вычитанием и не требует учитывать пересечение — "
  "это правило разности, а не включения-исключения; рост «ВИ» с 14% до 95% — рост разности, о ВИ он не говорит.")
w(f"4. **Две КР плохо согласованы между собой [F]:** ρ(КР29, КР06) = {f2(ri('KR29','KR06'))}, а листок 29.09 ↔ КР 6.10 = {f2(ri('LS29','KR06'))}, листок ↔ КР29 = {f2(ri('LS29','KR29'))}. "
  "КР 29.09 — 7 пунктов, один пункт сдвигает ребёнка на 14 пп; ранги по ней шумные. Резкие сдвиги (|Δ| ≥ 40 пп): "
  + '; '.join(f"{p['name'].split()[0]} {p['kr29']}/7 → {p['kr06o']}/13" for p in big_d)
  + f". Средняя Δ: верх {dmean('В')}, центр {dmean('Ц')}, низ {dmean('Ни')}. *[H]* низ вырос сильнее, потому что ○ КР 6.10 после разбора — правило разности, а верх упёрся в потолок.")
w(f"5. **Самооценка «я — △» не совпадает с данными у части детей [F + H].** На КР 6.10 только △ писали {ks(tri_only)}; "
  f"Трибунский по всем прочим событиям — низ (ранг {f2(P['Трибунский Глеб']['rank'])}) и решил △ {E['KR06']['Трибунский Глеб']['tri']}/8. "
  "У этих детей ○ на КР 6.10 не измерены вовсе. *[H]* выбор △ — сигнал мотивации или ухода от ○, а не уровня; проверять устно.")
w(f"6. **Логика 15.09 с комбинаторикой не согласуется [F]:** ρ(Л15, КР06) = {f2(ri('L15','KR06'))}, ρ(ОХ15, КР29) = {f2(ri('OH15','KR29'))}; "
  f"ДЗ ↔ классные события — от {f2(min(dzr))} до {f2(max(dzr))}. Подтверждается вывод 01-klass.md: ДЗ знание не меряет. Обе вещи в кластеризацию не входят.\n")

w('## 8. Стратификация: что факт, что допущение, что гипотеза\n')
w('| утверждение | статус | на чём держится |\n|---|---|---|')
for a, b, c in [
    ('баллы по пунктам листков, КР 6.10, мини-листка; явка по событиям', 'F', 'CSV/разметка/svod_kr_6-10.py, пересчёт этим скриптом'),
    ('вердикты КР 29.09', 'F*', 'восстановлены по ключу здесь; совпадают с 01-klass.md по всем пунктам, кроме 2б (Мосина, перечтение)'),
    ('корреляции событий, разрывы рангов, динамика долей', 'F', '§4–5'),
    ('границы ○/△/доп в листках 22.09 (○ 11, △ 4)', 'M', 'выведены из того, какие пункты пропускали шедшие вверх; ключей листков 22.09 в выгрузке нет'),
    ('Р155 «решил △ — ○ засчитаны» на 22.09 и КР 6.10 (порог △ ≥ 3, ○ без ошибок)', 'M', 'перенос правила листка 29.09; без него △-дети проваливаются в ранге'),
    ('балл КР 6.10 для ранга = ○ + 2·△', 'M', 'вес △ взят из v2 КР (2–4 балла за △); в v4 баллов у △ нет'),
    ('ранг = среднее перцентилей по 4 комбинаторным дням', 'M', 'как klastery.py в 01-klass.md; разная трудность событий не учтена'),
    ('пороги: верх ≥ 2 △-сигналов и ранг ≥ 0,55; низ < 0,40; «мало данных» < 3 дней', 'M', 'подобраны «по-человечески», не оптимизированы'),
    ('соответствие приёмов КР29 ↔ КР06', 'M', 'из sravnenie_kr_29-09_6-10.py («решение аналитика, оспоримо»)'),
    ('«ВИ» на КР 6.10 = правило разности, а не ВИ', 'M', 'чтение условия ○3 v4'),
    ('листки с принимающими меряют ребёнка + помощь', 'H', 'доля ○ у всех 70–100%; различают в основном △ и доп'),
    ('выбор «только △» на КР — мотивация, не уровень', 'H', 'Трибунский; проверяется устно'),
    ('низ вырос к 6.10 из-за разбора правила разности', 'H', 'рост сосредоточен в ±1 и «ВИ», перебор не вырос'),
]:
    w(f'| {a} | {b} | {c} |')
w('')

w('## 9. Дыры в данных и что бы их закрыло\n')
w('| дыра | кого касается | что закрыло бы |\n|---|---|---|')
for a, b, c in [
    ('нет OTSENKA-KR-29-09.json и ANALIZ/KLASTERY 29.09 в выгрузке', 'все', 'положить в папку — сверить вердикты КР 29.09'),
    ('22.09 нет работ', ks(absent['P22']), '—'),
    ('листок 29.09 нет', ks(absent['LS29']), '—'),
    ('КР 29.09 нет', ks(absent['KR29']), '—'),
    ('КР 6.10 нет', ks(absent['KR06']), 'дописать КР 6.10 или устный мини-зачёт по ○'),
    ('КР 6.10: ○ не измерены (писали только △)', ks(tri_only), 'на следующей КР один ○-пункт обязателен для всех; или 3 минуты устно'),
    ('одна самостоятельная КР с ○ или меньше', ks(nkr1), 'то же'),
    ('логика 23.09 — 3 анонимных листа; мини-листок 6.10 — 1 анонимный', '?', 'подпись — обязательная клетка в шапке; спросить в классе'),
    ('листки: нет числа попыток, времени до лагеря, подсказок принимающих', 'все', 'журнал приёма: ребёнок × задача × попытка × «с подсказкой?» (1 строка на сдачу)'),
    ('устные ответы у доски, работа на разборе', 'все', 'короткие пометки ассистентов после пары («кто вышел / кто объяснил»)'),
    ('кружок 7И: посещаемость и сдача', 'все', 'выгрузка сдачи кружка в том же формате CSV'),
    ('ДЗ: неизвестно, сколько помощи', 'все', 'не мерить ДЗ; если нужно — одна задача ДЗ повторяется на КР'),
    ('семантика «в» в CSV 15.09 и 22.09 не задокументирована', 'все', 'одна строка-легенда в CSV'),
]:
    w(f'| {a} | {b} | {c} |')
w('')

w('## 10. Можно ли уже делить на 3 уровня листков [H]\n')
gap3 = [p['name'] for p in vis if p['gap'] == 'В']
assert set(grp['В']) == {k for k in ROSTER if P[k]['km'] == 'В'} and set(grp['В']) <= set(gap_top)
w(f"- **Верх ({len(grp['В'])}): да.** {ks(grp['В'])}. Правило и k-means дают один и тот же состав; метод разрывов кладёт всех восьмерых в свои верхние {len(gap_top)} "
  f"(внутри них малый разрыв выделяет {ks(gap3)}). "
  "Им — △-листок с самого начала (как мини-листок 6.10), ○ по Р155.")
w(f"- **Центр ({len(grp['Ц'])}) и низ ({len(grp['Ни'])}): пока нет.** Граница — 0,40 ранга без разрыва; "
  f"{ks(low_hi06)} из «низа» на КР 6.10 написали ○ ≥ 10/13. Разумнее два уровня ниже верха делать по одному признаку — "
  f"**перебор, порядок которого выбирает сам ребёнок** (○4/○6в КР 6.10: центр {pc(pr_lv[('перебор','Ц')])}, низ {pc(pr_lv[('перебор','Ни')])}), "
  "и перед делением перемерить его отдельно, коротко, в одном формате.")
w(f"- **Мало данных ({len(grp['Н'])}): {ks(grp['Н'])}.** До решения — устная проверка ○ на уровне КР 6.10.")
w(f"- Отдельно смотреть: {ks(tri_only)} (только △ на КР 6.10) и {ks([p['name'] for p in big_d])} (|Δ КР| ≥ 40 пп).\n")
TXT = '\n'.join(L)

if __name__ == '__main__':
    open(OUT, 'w', encoding='utf-8').write(TXT + '\n')
    print(TXT)
