#!/usr/bin/env python3
# Свод 4 часов 7И: 15.09 (обратный ход, логика) + 22.09 (комбинаторика 1). Единица — пункт.
# Зачтено = плюс преподавателя ИЛИ верный записанный ответ (правило инфографики 15.09).
# Исправленная версия: пустые кружки засчитываются ЧЕТВЕРЫМ, начавшим с треугольников (решение владельца 22.09):
KRUZHKI_ZA_TREUG = {'Бердичевский', 'Литвиненко', 'Юнгельсон', 'Вишницкий'}
import csv, json, re, statistics as st, difflib
from pathlib import Path
H = Path(__file__).resolve().parent
num = lambda k: int(re.match(r'\d+', k).group())
NORM = lambda n: re.sub(r'\s*\(.*', '', n).replace('ё', 'е').strip()
def load15(fn):
    return {NORM(r['фамилия_имя']): (int(r['зачтено']), sum(1 for k in r if re.fullmatch(r'з\d+', k)))
            for r in csv.DictReader(open(H/fn, encoding='utf-8'), delimiter=';') if r['зачтено'].isdigit()}
OH, LG = load15('SDACHA-15-09_obratnyj-hod.csv'), load15('SDACHA-15-09_logika.csv')
names = sorted(set(OH) | set(LG))
# эталон 22.09 из шпаргалки: строки «№ & A & Б»
E = {'А': {}, 'Б': {}}
for line in open(H/'shpargalka_22-09_podschety.tex', encoding='utf-8'):
    m = re.match(r'\s*(\d+)\s*&(.*?)&(.*?)\\\\', line)
    if not m or 'multicolumn' in line: continue
    for v, cell in (('А', m.group(2)), ('Б', m.group(3))):
        parts = [p for p in re.split(r'\\quad|\\ ', re.sub(r'\\textbf\{([^}]*)\}', r'\1', cell)) if p.strip()]
        E[v][int(m.group(1))] = [re.sub(r'[\s$\\,%]', '', p) for p in parts]
BUK = 'абвг'
def correct(v, k, ans):
    n = num(k); sub = k[len(str(n)):]
    et = E[v].get(n)
    if not et or ans is None: return False
    i = BUK.index(sub) if sub else 0
    return i < len(et) and re.sub(r'[\s,%]', '', str(ans)) == et[i]
rows22 = {}
ITEMS22, ITEMS22_D, RAW22 = {}, {}, {}  # вектор пунктов 22.09 по ребёнку (исправленная версия), 39 мест
PROF = {}  # номер задачи -> [взято пунктов, всего пунктов] по классу, исправленная версия
for l in open(H/'RAZMETKA-22-09.jsonl', encoding='utf-8'):
    r = json.loads(l); v = 'А' if r['var'] in ('A', 'А') else 'Б'
    m = difflib.get_close_matches(r['imya'].split()[0], [n.split()[0] for n in names], 1, 0.6)
    fix = {'Вильчинский': 'Вишницкий', 'Любименко': 'Литвиненко', 'Титус': 'Юстус'}
    fam = fix.get(r['imya'].split()[0], m[0] if m else r['imya'].split()[0])
    nm = next((n for n in names if n.split()[0] == fam), r['imya'])
    o = r['o']; z = {k: (c == '+' or (c in 'xz' and correct(v, k, r['n'].get(k)))) for k, c in o.items() if c}
    raw = dict(z)
    tri_plus = nm.split()[0] in KRUZHKI_ZA_TREUG
    ispr = {k: (z[k] or (tri_plus and num(k) <= 5 and o[k] == '.')) for k in z}
    bez_plyusa = sum(1 for k in z if z[k] and o[k] != '+')
    ITEMS22_D[nm] = ispr; RAW22[nm] = o
    for k in ispr:
        a = PROF.setdefault(num(k), [0, 0]); a[0] += ispr[k]; a[1] += 1
    rows22[nm] = dict(var=v, maks=39,  # 39 пунктов в обоих вариантах, 15 из них обязательные (по шпаргалке);
                      # разметчик мог пропустить пустой пункт, поэтому максимум не берётся из разметки
                      syroj=sum(raw.values()), ispr=sum(ispr.values()),
                      zony={zn: sum(ispr[k] for k in ispr if lo <= num(k) <= hi)
                            for zn, lo, hi in (('o', 1, 5), ('t', 6, 9), ('d', 10, 19), ('g', 20, 22))},
                      dobavleno=sum(ispr.values()) - sum(raw.values()), bez_plyusa=bez_plyusa,
                      obyaz=sum(ispr[k] for k in ispr if num(k) <= 9), obyaz_max=15)
# канонические 39 пунктов варианта: число подпунктов каждой задачи — по листку и шпаргалке (в доп А и Б разные задачи)
CHASTI = {'А': dict(zip(range(1, 23), [3, 4, 1, 2, 1, 1, 1, 1, 1, 2, 2, 3, 3, 2, 2, 1, 2, 2, 2, 1, 1, 1])),
          'Б': dict(zip(range(1, 23), [3, 4, 1, 2, 1, 1, 1, 1, 1, 2, 2, 3, 2, 2, 2, 3, 2, 2, 1, 1, 1, 1]))}
def CANON(v):
    return [f'{n}{BUK[i]}' if c > 1 else str(n) for n, c in CHASTI[v].items() for i in range(c)]
for n, d in ITEMS22_D.items():
    keys = CANON(rows22[n]['var'])
    def val(k):
        if k in d: return int(bool(d[k]))
        alt = [kk for kk in d if num(kk) == num(k)]          # разметчик назвал пункт иначе («16» вместо «16а»)
        return int(len(alt) == 1 and bool(d[alt[0]]) and sum(1 for kk in keys if num(kk) == num(k)) == 1)
    ITEMS22[n] = [val(k) for k in keys]; ITEMS22_D[n] = dict(zip(keys, ITEMS22[n]))
# та же сдача в формате таблиц 15.09 — для infografika.py: + плюс · в засчитано без плюса · н не принято · - пусто
with open(H/'SDACHA-22-09_infografika.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['фамилия_имя', 'вариант'] + [f'з{i}' for i in range(1, 40)] + ['зачтено'])
    for n in sorted(ITEMS22_D):
        o, keys = RAW22[n], CANON(rows22[n]['var'])
        def raw(k):
            alt = [kk for kk in o if num(kk) == num(k)]
            return o.get(k, o[alt[0]] if len(alt) == 1 and sum(num(kk) == num(k) for kk in keys) == 1 else '.')
        m = ['+' if ITEMS22_D[n][k] and raw(k) == '+' else 'в' if ITEMS22_D[n][k] else 'н' if raw(k) in ('x', 'z') else '-'
             for k in keys]
        w.writerow([n, {'А': 'A', 'Б': 'B'}[rows22[n]['var']]] + m + [sum(ITEMS22_D[n].values())])
out = []
for n in sorted(set(names) | set(rows22)):
    oh, lg, k22 = OH.get(n), LG.get(n), rows22.get(n)
    out.append(dict(imya=n, oh=oh and oh[0], oh_max=oh and oh[1], lg=lg and lg[0], lg_max=lg and lg[1],
                    k22=k22 and k22['ispr'], k22_syroj=k22 and k22['syroj'], k22_max=k22 and k22['maks'],
                    k22_zony=k22 and k22['zony'], k22_dobavleno=k22 and k22['dobavleno'],
                    k22o=k22 and k22['obyaz'], k22o_max=k22 and k22['obyaz_max'], bez_plyusa=k22 and k22['bez_plyusa']))
json.dump(out, open(H/'SVOD-4-chasa.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump({n: PROF[n] for n in sorted(PROF)}, open(H/'SVOD-4-chasa-profil.json', 'w'))
# отчёт
def pct(a, b): return None if a is None else round(100 * a / b)
L = [('ОХ 15.09', 'oh', 'oh_max'), ('логика 15.09', 'lg', 'lg_max'), ('комб. 22.09 испр', 'k22', 'k22_max'),
     ('комб. 22.09 сырой', 'k22_syroj', 'k22_max'), ('комб. обязат. 1-9', 'k22o', 'k22o_max')]
for t, a, b in L:
    P = [pct(r[a], r[b]) for r in out if r[a] is not None]
    print(f'{t:18} n={len(P):2} медиана {st.median(P):3.0f}%  разброс {min(P)}..{max(P)}  ширина {max(P)-min(P)}  σ {st.pstdev(P):4.1f}')
both = [r for r in out if None not in (r['oh'], r['lg'], r['k22'])]
P = lambda r, a, b: 100 * r[a] / r[b]
def cor(a, b): return st.correlation([P(r, *a) for r in both], [P(r, *b) for r in both])
oh, lg, kb = ('oh', 'oh_max'), ('lg', 'lg_max'), ('k22', 'k22_max')
print('все три листка у', len(both), '| корреляции: ОХ-лог %.2f  ОХ-комб %.2f  лог-комб %.2f' % (cor(oh, lg), cor(oh, kb), cor(lg, kb)))
print('добавлено исправлением:', {r['imya'].split()[0]: r['k22_dobavleno'] for r in out if r['k22_dobavleno']})
print('засчитано по верному ответу без плюса:', sum(r['bez_plyusa'] or 0 for r in out))
# место в классе: перцентиль внутри листка, среднее по доступным листкам
def perc(key, mx):
    vals = [(P(r, key, mx), r['imya']) for r in out if r[key] is not None]
    return {n: 100 * sum(v2 < v for v2, _ in vals) / (len(vals) - 1) for v, n in vals}
PC = [perc(*x) for x in (oh, lg, kb)]
for r in out:
    r['perc'] = [round(pc[r['imya']]) if r['imya'] in pc else None for pc in PC]
    have = [x for x in r['perc'] if x is not None]; r['perc_sr'] = round(st.mean(have)) if have else None
json.dump(out, open(H/'SVOD-4-chasa.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\nперцентили ОХ / лог / комб → среднее')
for r in sorted(out, key=lambda r: -(r['perc_sr'] or -1)):
    print(f"{r['imya'][:18]:18} {str(r['perc']):20} {r['perc_sr']}")
