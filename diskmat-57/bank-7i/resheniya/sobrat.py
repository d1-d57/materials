# -*- coding: utf-8 -*-
"""Сборка решений банка 7И: src/<rabota_id>.py → out/<rabota_id>/<номер>.html (фрагменты div.rs для бота)
и out/PREVIEW.html (все решения одной страницей — для владельца и проверки глазами).

    python3 sobrat.py              собрать
    python3 sobrat.py --proverka   ничего не писать; rc=1, если out/ устарел, числовой ответ решения
                                   не совпал с bank-7i/otvety.csv или решение лежит вне охвата

Охват (Р329, владелец 11.10 19:15): работы с 22.09; на листках — только обязательные (○ и △),
дополнительные задачи листков решений в общем доступе не получают; КР, ДЗ, доп. листок Л5 — целиком."""
import csv
import importlib.util
import pathlib
import sys

KOREN = pathlib.Path(__file__).resolve().parent
OTVETY = KOREN.parent / 'otvety.csv'
OUT = KOREN / 'out'

OHVAT = {  # работа: (код, номера задач с открытым решением)
    'LS-2026-09-22': ('Л3', [str(i) for i in range(1, 10)]),    # ○ 1–5, △ 6–9
    'DZ-2026-09-29': ('ДЗ1', [str(i) for i in range(1, 6)]),
    'LS-2026-09-29': ('Л4', [str(i) for i in range(1, 9)]),     # ○ 1–5, △ 6–8
    'KR-2026-09-29': ('КР1', [str(i) for i in range(1, 5)]),
    'DZ-2026-10-06': ('ДЗ2', [str(i) for i in range(1, 7)]),
    'KR-2026-10-06': ('КР2', [str(i) for i in range(1, 13)]),   # ○ 1–6, △ 7–12
    'ML-2026-10-06': ('Л5', [str(i) for i in range(1, 7)]),     # доп. листок — целиком
}


def zagruzit(tolko=None):
    raboty = []
    faily = [pathlib.Path(tolko).resolve()] if tolko else sorted((KOREN / 'src').glob('*.py'))
    for f in faily:
        spec = importlib.util.spec_from_file_location(f.stem.replace('-', '_'), f)
        m = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(KOREN))
        spec.loader.exec_module(m)
        raboty.append(m.R)
    return raboty


def klyuch():
    k = {}
    with open(OTVETY, encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            if r['chislo'].strip():
                k[(r['rabota_id'], r['variant'], r['punkt'])] = r['chislo'].strip()
    return k


def preview(raboty):
    css = (KOREN / 'reshenie.css').read_text(encoding='utf-8')
    body = []
    vse = sorted(((rid, z) for R in raboty for z in R.zadachi for rid in [R.id]),
                 key=lambda t: (list(OHVAT).index(t[0]) if t[0] in OHVAT else 99, int(t[1].n)))
    for rid, z in vse:
        body.append(f'<h2>{OHVAT.get(rid, (rid,))[0]} №{z.n}</h2>' + z.html())
    return ('<!doctype html><html lang="ru"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1"><title>Решения 7И</title>'
            '<style>body{margin:0 auto;max-width:760px;padding:20px 16px 80px;background:#fbfaf7;'
            'font-family:Georgia,"PT Serif",serif}h2{font:600 18px system-ui,sans-serif;margin:2em 0 .3em;'
            'border-top:1px solid #d9d6cc;padding-top:1em}@media (prefers-color-scheme: dark){body{background:#1b1c1f;color:#ecebe6}}'
            + css + '</style></head><body><h1>Решения 7И</h1>' + '\n'.join(body) + '</body></html>')


def main():
    proverka = '--proverka' in sys.argv
    tolko = sys.argv[sys.argv.index('--src') + 1] if '--src' in sys.argv else None
    if tolko:   # один файл: только сверка ответов и охвата, ничего не пишется
        R = zagruzit(tolko)[0]
        k, osh = klyuch(), []
        for z in R.zadachi:
            if z.n not in OHVAT.get(R.id, ('', []))[1]:
                osh.append(f'№{z.n}: вне охвата')
            for (v, punkt), x in z.otvety.items():
                kl = k.get((R.id, v, punkt))
                if str(x) != str(kl):
                    osh.append(f'№{z.n} {v or "—"} {punkt}: в решении {x}, в otvety.csv {kl}')
            z.html()
        print(f'{R.id}: задач {len(R.zadachi)}; ошибок {len(osh)}')
        for o in osh:
            print('ОШИБКА:', o)
        sys.exit(1 if osh else 0)
    raboty = zagruzit()
    k = klyuch()
    oshibki, faily = [], {}
    for R in raboty:
        if R.id not in OHVAT:
            oshibki.append(f'{R.id}: работа вне охвата')
            continue
        for z in R.zadachi:
            if z.n not in OHVAT[R.id][1]:
                oshibki.append(f'{R.id} №{z.n}: задача вне охвата (дополнительная?) — решение в общий доступ не идёт')
            for (v, punkt), x in z.otvety.items():
                kl = k.get((R.id, v, punkt))
                if kl is None:
                    oshibki.append(f'{R.id} {v or "—"} {punkt}: в otvety.csv нет числового ответа')
                elif str(x) != kl:
                    oshibki.append(f'{R.id} {v or "—"} {punkt}: в решении {x}, в otvety.csv {kl}')
            faily[OUT / R.id / f'{z.n}.html'] = z.html()
    faily[OUT / 'PREVIEW.html'] = preview(raboty)
    if proverka:
        for p, t in faily.items():
            if not p.exists() or p.read_text(encoding='utf-8') != t:
                oshibki.append(f'устарел или нет файла: {p.relative_to(KOREN)} — запусти sobrat.py')
    else:
        for p, t in faily.items():
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(t, encoding='utf-8')
    est = {(R.id, z.n) for R in raboty for z in R.zadachi}
    for rid, (kod, nomera) in OHVAT.items():
        net = [n for n in nomera if (rid, n) not in est]
        print(f'{kod} ({rid}): решений {len(nomera) - len(net)} из {len(nomera)}' + (f'; нет: {", ".join(net)}' if net else ''))
    for o in oshibki:
        print('ОШИБКА:', o)
    sys.exit(1 if oshibki else 0)


if __name__ == '__main__':
    main()
