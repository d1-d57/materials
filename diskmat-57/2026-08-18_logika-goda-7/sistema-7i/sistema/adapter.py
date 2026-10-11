# -*- coding: utf-8 -*-
"""Адаптер «старые выгрузки → нормальные таблицы учёта» (схема из SISTEMA-chernovik.md §3).
Запуск: python3 adapter.py [папка_данных]  → пишет sistema/dannye/*.csv.
Источник — импорт ../navyki/navyki.py (он сам импортирует ../klaster/klaster.py); оба только читаются, не меняются.
Дальше движок (sistema.py) читает ТОЛЬКО dannye/*.csv — так проверяется, что схемы хватает.
Будущие источники (бот, сайт, фото КР) пишут в те же таблицы, см. §3 отчёта."""
import csv, importlib.util, os, sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
OUTD = os.path.join(HERE, 'dannye')


def load_navyki(data_dir=None):
    argv = sys.argv[:]
    sys.argv = [argv[0]] + ([data_dir] if data_dir else [])
    spec = importlib.util.spec_from_file_location('navyki', os.path.join(HERE, '..', 'navyki', 'navyki.py'))
    N = importlib.util.module_from_spec(spec); spec.loader.exec_module(N)
    sys.argv = argv
    return N


# событие: (id, дата, порядок в дне, тип, режим, источник)
SOB = {
    'P22':  ('LS-2026-09-22', '2026-09-22', 1, 'LS', 'pomosch', 'csv-priema'),
    'I22':  ('LS-2026-09-22i', '2026-09-22', 2, 'LS', 'pomosch', 'csv-priema'),
    'DZ29': ('DZ-2026-09-29', '2026-09-29', 0, 'DZ', 'dom', 'foto-razmetka'),
    'LS29': ('LS-2026-09-29', '2026-09-29', 1, 'LS', 'pomosch', 'csv-priema'),
    'KR29': ('KR-2026-09-29', '2026-09-29', 2, 'KR', 'sam', 'foto-razmetka'),
    'DZ06': ('DZ-2026-10-06', '2026-10-06', 0, 'DZ', 'dom', 'foto-razmetka'),
    'KR06': ('KR-2026-10-06', '2026-10-06', 1, 'KR', 'sam', 'foto-razmetka'),
    'ML06': ('ML-2026-10-06', '2026-10-06', 2, 'ML', 'pomosch', 'foto-razmetka'),
}
TEMA = 'komb'
# уровень пунктов (○/△) и обязательность — как в klaster.py: P22 △ = 6–9, LS29 △ = 6–8, KR06 △ = 7–12, ML06 весь △;
# KR29 4б — обязательный, но «вершинный» (△-сигнал в klaster.py)
def uroven(ev, p, kr06_o):
    if ev == 'P22': return ('△', 0) if p in ('6', '7', '8', '9') else ('○', 1)
    if ev == 'LS29': return ('△', 0) if p in ('6', '7', '8') else ('○', 1)
    if ev == 'KR29': return ('△', 1) if p == '4б' else ('○', 1)
    if ev == 'KR06': return ('○', 1) if p in kr06_o else ('△', 0)
    if ev == 'ML06': return ('△', 0)
    return ('○', 1)                                   # ДЗ


def build(data_dir=None, outd=OUTD):
    N = load_navyki(data_dir); K = N.K
    os.makedirs(outd, exist_ok=True)
    rid = {c: f'r{i + 1:02d}' for i, c in enumerate(K.ROSTER)}
    def wcsv(name, head, rows):
        with open(os.path.join(outd, name), 'w', encoding='utf-8', newline='') as f:
            w = csv.writer(f); w.writerow(head); w.writerows(rows)
    wcsv('deti.csv', ['id', 'fio', 'aktiven'], [[rid[c], c, 1] for c in K.ROSTER])
    MIN = {'1', '2', '3', '5б'}                       # [M] обязательный минимум темы — решает владелец
    wcsv('navyki.csv', ['kod', 'tema', 'deystvie', 'minimum', 's_daty'],
         [[k, TEMA, v, int(k in MIN), '2026-09-22'] for k, v in N.SK.items()])
    wcsv('sobytiya.csv', ['id', 'data', 'poryadok', 'tip', 'rezhim', 'tema', 'istochnik'],
         [[s[0], s[1], s[2], s[3], s[4], TEMA, s[5]] for s in SOB.values()])
    rows = []
    for d in N.IT:
        u, ob = uroven(d['ev'], d['p'], K.KR06_P)
        rows.append([SOB[d['ev']][0], d['p'], u, ob, d['main'], d['aux'], d['obhod'], d['q']])
    wcsv('punkty.csv', ['sobytie', 'punkt', 'uroven', 'obyazat', 'navyk_osn', 'navyki_vspom', 'obhod', 'uslovie'], rows)
    # наблюдения: попытка/подсказка/кто сейчас неизвестны — пусто (это и есть дыра, которую закроет бот)
    obs = [[SOB[x['ev']][0], x['p'], rid[x['c']], '', x['v'], '', '', SOB[x['ev']][5]] for x in N.A]
    # доп. пункты листков и «Инфографика» 22.09 — без навыка ('?'): нужны только для силы по теме (как в klaster.py)
    extra = []
    def put(ev, p, lvl, c, v):
        extra.append([SOB[ev][0], p, lvl, 0 if lvl != '○' else 1, '?', '', '', 'нет условия в выгрузке'])
        if c and v: obs.append([SOB[ev][0], p, rid[c], '', v, '', '', SOB[ev][5]])
    D = N.D
    for r in K.rows_csv(f'{D}/SDACHA-22-09_podschety.csv'):
        c = K.who(r['фамилия_имя'], 'P22-dop'); cols = list(r)[list(r).index('9') + 1:]
        for p in cols:
            if p in ('плюсов', '_cells'): continue
            x = r.get(p, ''); put('P22', p, 'доп', c, '+' if x == '+' else '-' if x == 'x' else '')
    for r in K.rows_csv(f'{K.I29}/SDACHA.csv'):
        c = K.who(r['фамилия_имя'], 'LS29-dop'); cols = list(r)[list(r).index('8') + 1: list(r).index('зачтено')]
        for p in cols:
            x = r.get(p, ''); put('LS29', p, 'доп', c, '+' if x in ('+', 'в') else '-' if x == 'н' else '')
    for r in K.rows_csv(f'{D}/SDACHA-22-09_infografika.csv'):
        c = K.who(r['фамилия_имя'], 'I22')
        for i in range(1, 40):
            p = f'з{i}'; x = r.get(p, '')
            put('I22', p, '○' if i <= 11 else '△' if i <= 15 else 'доп', c, '+' if x in ('+', 'в') else '-' if x == 'н' else '')
    seen = set(); ex2 = []
    for e in extra:
        if (e[0], e[1]) not in seen: seen.add((e[0], e[1])); ex2.append(e)
    with open(os.path.join(outd, 'punkty.csv'), 'a', encoding='utf-8', newline='') as f: csv.writer(f).writerows(ex2)
    wcsv('nablyudeniya.csv', ['sobytie', 'punkt', 'rebyonok', 'popytka', 'verdikt', 'podskazka', 'kto', 'istochnik'], obs)
    wcsv('ruchnye.csv', ['data', 'rebyonok', 'chto', 'klyuch', 'znachenie', 'kto', 'prichina'], [])
    wcsv('prepody.csv', ['imya', 'rol', 'max_detej', 'k_klasteru'],
         [['Ваня', 'seminar', 14, ''], ['Алексей', 'priem', 4, 'верх'], ['Михаил', 'priem', 4, 'верх'],
          ['Ксения', 'priem', 4, 'низ'], ['Арсен', 'priem', 4, 'середина']])
    return N


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else None)
    for f in sorted(os.listdir(OUTD)):
        print(f, sum(1 for _ in open(os.path.join(OUTD, f), encoding='utf-8')) - 1, 'строк')
