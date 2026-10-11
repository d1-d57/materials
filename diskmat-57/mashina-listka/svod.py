# -*- coding: utf-8 -*-
"""СВОД СДАЧИ листка — общий, для любой итерации (обобщение svod_4chasa.py 22.09).

Запуск:  python3 svod.py <папка итерации> [RAZMETKA.jsonl]
Вход:    <итерация>/out/kanon.json — канонические пункты по вариантам (пишет файл данных листка);
         RAZMETKA-*.jsonl — по строке на ребёнка: {"imya": "...", "var": "А"|"Б", "o": {пункт: код}, "n": {пункт: записанный ответ}}
         коды: '+' плюс · 'x' крест/минус · 'z' написано без отметки · '.' пусто (см. razmetka.py);
         <итерация>/POPRAVKI.json (необязательно) — поправки владельца СПИСКОМ ИМЁН: {"засчитать": {"имя": ["пункт", ...]}}.
Выход:   <итерация>/out/SVOD.json, <итерация>/SVOD.md, <итерация>/SDACHA.csv.
Правила (FORMAT-listka-po-otvetu.md): зачтено = плюс ИЛИ верный записанный ответ; пусто ≠ крест;
счёт в пунктах; разрешение — число разных баллов и доля ничьих, а не ширина; карта — лагерь/вершина по графу.
"""
import json, sys, re, csv, itertools, statistics as st
from pathlib import Path

def chislo(s):
    """Последнее число строки ответа: «10·10 − 6·6 = 64» → '64', «26/100» → '26/100'."""
    m = re.findall(r'\d+(?:[.,/]\d+)?', str(s).replace(' ', ' ').split('(')[0])
    return m[-1].replace(',', '.') if m else None

def zachteno(kod, napisano, klyuch):
    if kod == '+': return True
    if kod in ('x', 'z') and napisano is not None and chislo(napisano) and chislo(napisano) == chislo(klyuch): return True
    return False

def kr20(M):
    """Надёжность листка (Кьюдер–Ричардсон 20) по матрице дети × пункты из 0/1."""
    k = len(M[0]); tot = [sum(r) for r in M]
    if k < 2 or st.pvariance(tot) == 0: return None
    pq = sum((p := sum(r[j] for r in M) / len(M)) * (1 - p) for j in range(k))
    return k / (k - 1) * (1 - pq / st.pvariance(tot))

def karta(K, zach):
    """Что закрашено на карте: тропа ○/△ — если сданы ВСЕ пункты всех её задач; ромб — если сдан пункт и к нему
    ведёт линия от закрашенного (лагерь закрашен, когда закрыта хотя бы одна тропа). Черепа по отметке не видны."""
    kr = K['karta']; zad = {}
    for p in K['_punkty']: zad.setdefault(p['kletka'], []).append(zach.get(p['punkt'], False))
    tropa = {r: all(all(zad.get(c, [False])) for c in cs) for r, cs in kr['baza'].items()}
    lager = any(tropa.values()); done = {'CAMP'} if lager else set()
    IN = {}
    for a, b in kr['OUT'].items(): IN.setdefault(b, []).append(a)
    for e in kr['ENTRY']: IN.setdefault(e, []).append('CAMP')
    ch = True
    while ch:
        ch = False
        for c in kr['OUT']:
            if c not in done and all(zad.get(c, [False])) and any(p in done for p in IN.get(c, [])):
                done.add(c); ch = True
    vershina = any(kr['OUT'][c] == 'PEAK' for c in done if c != 'CAMP')
    return dict(tropa_o=tropa.get('○', False), tropa_t=tropa.get('△', False), lager=lager, vershina=vershina,
                rombov=len(done - {'CAMP'}))

IMENA = dict(detej='детей в разметке', ball_mediana='медиана баллов (пункты)', raznyh_ballov='разных баллов (разрешение)',
             dolya_nichej='доля ничьих (пар с равным баллом)', kr20='надёжность KR-20', lager='дошли до лагеря («4»)',
             vershina='дошли до вершины («5»)', tropa_o='закрыли тропу ○', tropa_t='закрыли тропу △')
def main(it, razm=None):
    it = Path(it); K = json.load(open(it / 'out' / 'kanon.json', encoding='utf-8'))
    razm = Path(razm) if razm else sorted(it.glob('RAZMETKA*.jsonl'))[-1]
    pop = json.load(open(it / 'POPRAVKI.json', encoding='utf-8')).get('засчитать', {}) if (it / 'POPRAVKI.json').exists() else {}
    deti = []
    for line in open(razm, encoding='utf-8'):
        if not line.strip(): continue
        r = json.loads(line); v = 'А' if r['var'] in ('A', 'А') else 'Б'
        P = K['punkty'][v]; K['_punkty'] = P
        z = {p['punkt']: zachteno(r['o'].get(p['punkt'], '.'), r.get('n', {}).get(p['punkt']), p['otvet']) for p in P}
        for p in pop.get(r['imya'], []): z[p] = True                                   # поправки — только списком имён
        kod = {p['punkt']: r['o'].get(p['punkt'], '.') for p in P}
        deti.append(dict(imya=r['imya'], var=v, z=z, kod=kod, ball=sum(z.values()),
                         obyaz=sum(z[p['punkt']] for p in P if p['razdel'] in '○△'),
                         dop=sum(z[p['punkt']] for p in P if p['razdel'] not in '○△'), **karta(K, z)))
    n = len(deti); balls = [d['ball'] for d in deti]
    pary = list(itertools.combinations(balls, 2))
    M = [[int(d['z'][p['punkt']]) for p in K['punkty'][d['var']]] for d in deti]
    by_punkt = {}
    for d in deti:
        for i, p in enumerate(K['punkty'][d['var']]):
            a = by_punkt.setdefault((d['var'], p['punkt']), dict(razdel=p['razdel'], sdano=0, krest=0, pusto=0, vsego=0))
            a['vsego'] += 1; a['sdano'] += d['z'][p['punkt']]
            a['krest'] += (not d['z'][p['punkt']]) and d['kod'][p['punkt']] in 'xz'; a['pusto'] += d['kod'][p['punkt']] == '.'
    S = dict(detej=n, ball_mediana=st.median(balls), raznyh_ballov=len(set(balls)),
             dolya_nichej=round(sum(a == b for a, b in pary) / len(pary), 3) if pary else None,
             kr20=round(kr20(M), 2) if n > 2 and len({len(r) for r in M}) == 1 and kr20(M) else None,
             lager=sum(d['lager'] for d in deti), vershina=sum(d['vershina'] for d in deti),
             tropa_o=sum(d['tropa_o'] for d in deti), tropa_t=sum(d['tropa_t'] for d in deti))
    json.dump(dict(svod=S, deti=deti, punkty={f'{v}:{p}': a for (v, p), a in by_punkt.items()}), open(it / 'out' / 'SVOD.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    with open(it / 'SDACHA.csv', 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter=';')
        for v in ('А', 'Б'):
            ps = [p['punkt'] for p in K['punkty'][v]]
            w.writerow(['фамилия_имя', 'вариант'] + ps + ['зачтено', 'лагерь', 'вершина'])
            for d in sorted((d for d in deti if d['var'] == v), key=lambda d: d['imya']):
                w.writerow([d['imya'], v] + [('+' if d['kod'][p] == '+' else 'в' if d['z'][p] else 'н' if d['kod'][p] in 'xz' else '-') for p in ps]
                           + [d['ball'], int(d['lager']), int(d['vershina'])])
    md = [f'# Свод сдачи — {it.name}', '', f'Данные: `{razm.name}`, пунктов в варианте {len(K["punkty"]["А"])}. Коды в SDACHA.csv: + плюс · в засчитано без плюса (верный ответ) · н не принято · - пусто.', '',
          '| показатель | значение |', '|---|---|'] + [f'| {IMENA.get(k, k)} | {v} |' for k, v in S.items()]
    md += ['', '## По пунктам (сдано / крест / пусто из всех)', '', '| вар | пункт | раздел | сдано | крест | пусто |', '|---|---|---|---|---|---|']
    md += [f'| {v} | {p} | {a["razdel"]} | {a["sdano"]}/{a["vsego"]} | {a["krest"]} | {a["pusto"]} |' for (v, p), a in sorted(by_punkt.items())]
    (it / 'SVOD.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
    print(json.dumps(S, ensure_ascii=False))

if __name__ == '__main__':
    main(*sys.argv[1:])
