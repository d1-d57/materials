# -*- coding: utf-8 -*-
"""ШПАРГАЛКА 29.09 — ТОЛЬКО НОМЕР, ВАРИАНТ, ОТВЕТ (А14; владелец 22.09 и 29.09: «иначе невозможно быстро это понять»).
Ничего больше: ни выражений, ни частых ошибок, ни правил карты, ни пояснений. Читается с телефона одним взглядом,
крупно. Ответы берутся из тех же данных, что и листки (out/kanon.json, kontr3.py, dz_29-09_dannye.py) — не переписываются."""
import os, sys, re, json, html, importlib.util
import pathlib as _pl
_H = _pl.Path(__file__).resolve().parent
sys.path.insert(0, str(next(p / 'mashina-listka' for p in _H.parents if (p / 'mashina-listka').is_dir())))
from listok_gen import shpargalka, to_pdf
HERE = str(_H)
e = html.escape
SEP = '\u2003\u2003'                      # между пунктами — два em-пробела (обычные пробелы браузер схлопывает)
def chislo(s):
    """Итог выражения: то, что после последнего «=», без пояснений в скобках."""
    s = re.sub(r'\s*\((или|сумма)[^)]*\)', '', s).strip()
    s = s.split('=')[-1].strip()
    return s
def listok():
    K = json.load(open(f'{HERE}/out/kanon.json', encoding='utf-8'))['punkty']
    R = {}
    for v in ('А', 'Б'):
        for p in K[v]:
            n = re.match(r'\d+', p['punkt']).group()
            o = p['otvet']
            if n in ('1', '5') and len(n) == len(p['punkt']): a = o.split('—')[-1].strip() if n == '1' else o.split(':')[0].strip()
            elif '—' in o and 'единственное' in o: a = o.split('—')[0].replace(',', '').strip()
            else: a = chislo(o)
            R.setdefault(int(n), {}).setdefault(v, []).append(a)
    return [(n, SEP.join(R[n]['А']), SEP.join(R[n]['Б'])) for n in sorted(R)]
def kontrolnaya():
    ns = {}; exec(open(f'{HERE}/kontr3.py', encoding='utf-8').read().split('def pole')[0], ns); K = ns['K']
    def kr(s, p):
        if p == '3а': return s.split('(')[0].strip()
        if p == '3б': return re.sub(r'горизонтальных \S+ = (\d+), вертикальных \S+ = (\d+); всего (\d+)', r'\1 + \2 = \3', s)
        if p == '4а': return '\u2002'.join(t.replace('–', '') for t in s.split(':')[1].strip().split(', '))
        if p == '2а': return s.replace(' и ', SEP)
        return chislo(s)
    return [(p, kr(a, p), kr(b, p)) for (p, a), (_, b) in zip(K['А'], K['Б'])]     # по пунктам: у контрольной поля (а)(б) раздельные
def dz():
    spec = importlib.util.spec_from_file_location('dz', f'{HERE}/dz_29-09_dannye.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    kor = {1: '2 мин 15 с', 2: '12 кг'}
    return [(z['num'], kor.get(z['num'], chislo(z['key'].split('(')[0]).split(':')[0].strip())) for z in m.Z]
if __name__ == '__main__':
    L = listok(); KR = kontrolnaya(); D = dz()
    for r in L + KR + D: print(r)
    razryvy = [8, 16]                       # черта после 8 (обязательные) и 16 (перед ★)
    h = shpargalka('Комбинаторика 2 · ответы', '29 сентября · 7И',
                   [('Листок', ['№', 'вариант А', 'вариант Б'], L, razryvy),
                    ('Контрольная', ['№', 'вариант А', 'вариант Б'], KR, []),
                    ('ДЗ к 6 октября', ['№', 'ответ'], D, [])])
    p = f'{HERE}/out/SHPARGALKA-29-09.html'; open(p, 'w', encoding='utf-8').write(h); to_pdf([p]); print('ok')
