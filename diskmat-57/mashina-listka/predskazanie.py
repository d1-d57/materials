# -*- coding: utf-8 -*-
"""PREDICTION before the lesson: the sheet PREDSKAZANIE.csv in the iteration folder.

  python3 predskazanie.py zagotovka <iteration folder> <rabota_id> [<rabota_id> ...]
  python3 predskazanie.py proverit  <iteration folder> [--git]

zagotovka: one row per item of each work (rabota_id, punkt, uroven, СН, Ни, Ц, В, istochnik_ocenki, kommentarij),
  the four share columns empty. Items come from the bot export (table punkty) or, for a work that is not there yet,
  from PUNKTY.csv in the folder (rabota_id,punkt,uroven[,yakor]; yakor = "<rabota_id>:<punkt>" of a past item).
  If reshaemost.csv knows the item (the same work and item, or the yakor) its fact goes into kommentarij as a hint.
  A file that exists is MERGED: filled shares are never overwritten, only missing rows are appended.
proverit: every item has all four shares as numbers in [0, 1]; nachalo is set in ITERACIYA.json; prints the expected
  solvability of the ○ and △ track per avatar and warns outside 50-80 %; writes PREDSKAZANIE.md next to the csv.
  --git additionally demands the proof "committed earlier than nachalo" (the table gate uses it).
The prediction is proved by git: the last commit of PREDSKAZANIE.csv must be earlier than `nachalo` of the pair
(ITERACIYA.json, "2026-10-13T15:30", Moscow time) and the file must be clean against HEAD.
"""
import csv, json, subprocess, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import sverka as S

IMYA = 'PREDSKAZANIE.csv'
POLE = ['rabota_id', 'punkt', 'uroven', 'СН', 'Ни', 'Ц', 'В', 'istochnik_ocenki', 'kommentarij']
AV = S.AVATARY
MSK = timezone(timedelta(hours=3))


def trek(uroven):
    """The track an item belongs to: '' counts as the base ○; доп and * are outside both tracks."""
    return '○' if uroven in ('○', '') else '△' if uroven == '△' else None


def chislo(s):
    """A share as a float, or None if empty or not a number. A decimal comma is accepted."""
    try:
        return float(str(s).strip().replace(',', '.'))
    except ValueError:
        return None


def chitat(papka):
    f = Path(papka) / IMYA
    if not f.exists():
        return []
    with open(f, encoding='utf-8', newline='') as fh:
        return list(csv.DictReader(fh))


def nachalo(papka):
    """Start of the pair as an aware datetime (naive value in ITERACIYA.json = Moscow time), or None."""
    j = Path(papka) / 'ITERACIYA.json'
    if not j.exists():
        return None
    v = json.load(open(j, encoding='utf-8')).get('nachalo')
    if not v:
        return None
    try:
        d = datetime.fromisoformat(str(v))
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=MSK)


def _git(papka, *args):
    return subprocess.run(['git', '--no-optional-locks', '-C', str(papka)] + list(args), capture_output=True, text=True)


def dokazatelstvo_git(papka, seychas=None):
    """(proved, text): PREDSKAZANIE.csv is committed earlier than nachalo and clean against HEAD."""
    papka = Path(papka); f = papka / IMYA
    n = nachalo(papka)
    if n is None:
        return False, 'в ITERACIYA.json нет `nachalo` (ГГГГ-ММ-ДДTЧЧ:ММ) — не с чем сравнить коммит'
    if not f.exists():
        return False, f'нет {IMYA}'
    if _git(papka, 'rev-parse', '--show-toplevel').returncode != 0:
        return False, 'папка вне git — доказать «до урока» нечем'
    if _git(papka, 'ls-files', '--error-unmatch', IMYA).returncode != 0:
        return False, f'{IMYA} не в git — закоммитить ДО начала пары ({n:%Y-%m-%d %H:%M})'
    if _git(papka, 'status', '--porcelain', '--', IMYA).stdout.strip():
        return False, f'{IMYA} изменён после последнего коммита — закоммитить ДО начала пары ({n:%Y-%m-%d %H:%M})'
    t = _git(papka, 'log', '-1', '--format=%cI', '--', IMYA).stdout.strip()
    ct = datetime.fromisoformat(t)
    if ct >= n:
        return False, f'последний коммит {ct:%Y-%m-%d %H:%M} НЕ раньше начала пары {n:%Y-%m-%d %H:%M} — предсказание «задним числом»'
    return True, f'последний коммит {ct:%Y-%m-%d %H:%M} раньше начала пары {n:%Y-%m-%d %H:%M}'


def _punkty_papki(papka):
    f = Path(papka) / 'PUNKTY.csv'
    if not f.exists():
        return {}
    out = {}
    with open(f, encoding='utf-8', newline='') as fh:
        for r in csv.DictReader(fh):
            out.setdefault(r['rabota_id'], []).append(r)
    return out


def _podskazka(rez, rid, punkt, yakor=''):
    """Hint from reshaemost.csv: the fact of the same item or of the anchor item."""
    k = (rid, punkt)
    src = ''
    if yakor and ':' in yakor:
        k = tuple(yakor.split(':', 1)); src = f'якорь {yakor}'
    else:
        src = f'тот же пункт {rid}:{punkt}'
    cells = {a: r for (w, p, a), r in rez.items() if (w, p) == k}
    if not cells:
        return ''
    chast = []
    for a in AV:
        r = cells.get(a)
        x = S.chislo_dolya(r) if r else None
        chast.append(f'{a} {"нет данных" if x is None else str(round(x * 100)) + " %"}')
    return f'{src}: факт ' + ' · '.join(chast)


def zagotovka(papka, rids, db, reshaemost):
    papka = Path(papka); papka.mkdir(parents=True, exist_ok=True)
    rez = {(r['rabota_id'], r['punkt'], r['avatar']): r for r in S.chitat_reshaemost(reshaemost)}
    iz_papki = _punkty_papki(papka)
    stare = chitat(papka)
    ostalis = {(r['rabota_id'], r['punkt']): r for r in stare}
    novye = 0
    itog = list(stare)
    for rid in rids:
        if S.rabota(db, rid) is not None and S.punkty_raboty(db, rid):
            spisok = [dict(punkt=n, uroven=u, yakor='') for n, u in S.punkty_raboty(db, rid)]
        elif rid in iz_papki:
            spisok = [dict(punkt=r['punkt'], uroven=r.get('uroven', ''), yakor=(r.get('yakor') or '').strip()) for r in iz_papki[rid]]
        else:
            sys.exit(f'❗ у работы {rid} нет пунктов: её нет в выгрузке бота и нет строк в {papka / "PUNKTY.csv"} '
                     f'(колонки rabota_id,punkt,uroven[,yakor])')
        for p in spisok:
            k = (rid, p['punkt'])
            if k in ostalis:
                r = ostalis[k]
                if not (r.get('kommentarij') or '').strip():
                    r['kommentarij'] = _podskazka(rez, rid, p['punkt'], p['yakor'])
                continue
            r = {c: '' for c in POLE}
            r.update(rabota_id=rid, punkt=p['punkt'], uroven=p['uroven'], kommentarij=_podskazka(rez, rid, p['punkt'], p['yakor']))
            itog.append(r); ostalis[k] = r; novye += 1
    with open(papka / IMYA, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=POLE, lineterminator='\n'); w.writeheader()
        for r in itog:
            w.writerow({c: r.get(c, '') for c in POLE})
    print(f'заготовка: {papka / IMYA} — строк {len(itog)} (новых {novye}), доли аватаров пустые: заполнить и прогнать `proverit`')


def proverit(papka, db=None, git=False):
    """Returns (ok, errors, warnings, info). Writes PREDSKAZANIE.md when the sheet is readable."""
    papka = Path(papka); err, warn, info = [], [], []
    rows = chitat(papka)
    if not (papka / IMYA).exists():
        return False, [f'нет {IMYA} — `predskazanie.py zagotovka {papka} <rabota_id>`'], warn, info
    if not rows:
        return False, [f'{IMYA} пуст'], warn, info
    pustye = [c for c in POLE if c not in rows[0]]
    if pustye:
        return False, ['в шапке нет колонок: ' + ', '.join(pustye)], warn, info
    seen = set(); chisla = []; bez_istochnika = []
    for r in rows:
        k = (r['rabota_id'].strip(), r['punkt'].strip())
        if not all(k):
            err.append(f'строка без rabota_id или punkt: {dict(r)}'); continue
        if k in seen:
            err.append(f'пункт {k[0]}:{k[1]} записан дважды')
        seen.add(k)
        vs = {a: chislo(r[a]) for a in AV}
        for a, v in vs.items():
            if v is None:
                err.append(f'{k[0]}:{k[1]} · {a}: доля не заполнена числом')
            elif not 0 <= v <= 1:
                err.append(f'{k[0]}:{k[1]} · {a}: доля {v} вне 0–1')
        chisla.append((k, r['uroven'], vs))
        if not (r.get('istochnik_ocenki') or '').strip():
            bez_istochnika.append(f'{k[0]}:{k[1]}')
    if bez_istochnika:
        warn.append(f'пуст istochnik_ocenki у {len(bez_istochnika)} из {len(rows)} пунктов (откуда оценка: якорь, аналитик…)')
    if db is not None:
        by = {}
        for (rid, p) in seen:
            by.setdefault(rid, set()).add(p)
        iz_papki = _punkty_papki(papka)
        for rid, ps in by.items():
            if S.rabota(db, rid) is not None and S.punkty_raboty(db, rid):
                ozhid = {n for n, _ in S.punkty_raboty(db, rid)}
            elif rid in iz_papki:
                ozhid = {r['punkt'] for r in iz_papki[rid]}
            else:
                warn.append(f'{rid}: список пунктов сверить не с чем (нет в выгрузке и нет PUNKTY.csv)'); continue
            if ozhid - ps:
                err.append(f'{rid}: нет предсказания для пунктов ' + ', '.join(sorted(ozhid - ps)))
            if ps - ozhid:
                err.append(f'{rid}: лишние пункты ' + ', '.join(sorted(ps - ozhid)))
    if nachalo(papka) is None:
        err.append('в ITERACIYA.json нет поля `nachalo` (ГГГГ-ММ-ДДTЧЧ:ММ, начало пары) — завести: без него «до урока» не доказать')
    treki = {}
    for a in AV:
        for t in ('○', '△'):
            vs = [v[a] for _, u, v in chisla if trek(u) == t and v[a] is not None]
            if vs:
                treki[(a, t)] = sum(vs) / len(vs)
    for (a, t), x in treki.items():
        if not S.ZONA[0] <= x <= S.ZONA[1]:
            warn.append(f'трек {t} у аватара {a}: ожидаемая решаемость {round(x * 100)} % вне 50–80 %')
    info += [f'ожидаемая решаемость трека — {a}: ' + ' · '.join(f'{t} {"—" if (a, t) not in treki else str(round(treki[(a, t)] * 100)) + " %"}' for t in ('○', '△')) for a in AV]
    dok = dokazatelstvo_git(papka)
    info.append(('git ✓ ' if dok[0] else 'git ✗ ') + dok[1])
    if git and not dok[0]:
        err.append('предсказание не доказано гитом: ' + dok[1])
    md = [f'# Предсказание · {papka.name}', '', 'Ожидаемая решаемость по аватарам (доля «+» среди писавших).', '',
          '| работа | пункт | уровень | СН | Ни | Ц | В | откуда оценка | комментарий |', '|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        f = lambda a: '—' if chislo(r[a]) is None else f'{round(chislo(r[a]) * 100)} %'
        md.append(f"| {r['rabota_id']} | {r['punkt']} | {r['uroven']} | {f('СН')} | {f('Ни')} | {f('Ц')} | {f('В')} | {r.get('istochnik_ocenki', '')} | {r.get('kommentarij', '')} |")
    md += ['', '## Ожидаемая решаемость трека', '', '| аватар | ○ | △ |', '|---|---|---|']
    for a in AV:
        md.append(f'| {a} | ' + ' | '.join('—' if (a, t) not in treki else f'{round(treki[(a, t)] * 100)} %' for t in ('○', '△')) + ' |')
    (papka / 'PREDSKAZANIE.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
    return not err, err, warn, info


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('komanda', choices=['zagotovka', 'proverit']); ap.add_argument('papka'); ap.add_argument('rabota', nargs='*')
    ap.add_argument('--git', action='store_true'); ap.add_argument('--vygruzka', default=str(S.VYGRUZKA))
    ap.add_argument('--reshaemost', default=str(S.RESHAEMOST))
    a = ap.parse_args(argv)
    db = S.otkryt(a.vygruzka) if Path(a.vygruzka).exists() else None
    if a.komanda == 'zagotovka':
        if not a.rabota:
            ap.error('zagotovka: нужен хотя бы один rabota_id')
        if db is None:
            sys.exit(f'❗ нет выгрузки бота: {a.vygruzka}')
        zagotovka(a.papka, a.rabota, db, a.reshaemost)
        return 0
    ok, err, warn, info = proverit(a.papka, db, git=a.git)
    for s in info:
        print('  ' + s)
    for s in warn:
        print('⚠ ' + s)
    for s in err:
        print('❗ ' + s)
    print('✓ предсказание в порядке' if ok else f'❗ предсказание НЕ принято: ошибок {len(err)}')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
