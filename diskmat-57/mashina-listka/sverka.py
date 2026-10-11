# -*- coding: utf-8 -*-
"""SVERKA "prediction -> fact" and the SOLVABILITY SCALE from history; the one shared counter of the fact.

  python3 sverka.py --shkala                  -> bank-7i/reshaemost.csv for every work since 22.09 (idempotent)
  python3 sverka.py <iteration folder>        -> <folder>/SVERKA.csv, SVERKA.md; the fact also goes to reshaemost.csv
  --vygruzka <db>      default: bot-7i/data/vygruzka.db next to materials
  --reshaemost <csv>   default: diskmat-57/bank-7i/reshaemost.csv

The fact of a cell (item x avatar) = reshili / pisali, counted by the ONE function fakt() for the scale and for the sverka:
  pisali  - children of the avatar who wrote the work: a test / homework - status "sdal"; a sheet - at least one "+" on it.
            A work of two alternative parts (КР ○/△): an item is counted for those who handed in AND marked anything
            in its part (otherwise the ○ items are diluted by children who chose only △).
  reshili - of them, "+" on the item. An empty cell of a sheet = "not solved" (strict mode).
  The avatar comes from the table `avatary` of the export (СН, Ни, Ц, В); "Н" (too little data) and the test child do not count.
  Fewer than two writers in an avatar = "нет данных" (an empty share), neither 0 nor 100 %.
No child appears in the output files, only aggregates per avatar.
"""
import argparse, csv, sqlite3, sys
from pathlib import Path

M = Path(__file__).resolve().parent
MATERIALS = M.parents[1]
VYGRUZKA = MATERIALS.parent / 'bot-7i' / 'data' / 'vygruzka.db'
RESHAEMOST = MATERIALS / 'diskmat-57' / 'bank-7i' / 'reshaemost.csv'
AVATARY = ('СН', 'Ни', 'Ц', 'В')
S_DATY = '2026-09-22'            # the scale starts at the first work after the 15.09 sheets (owner, 11.10)
MIN_PISALI = 2
POLE = ['rabota_id', 'punkt', 'uroven_punkta', 'avatar', 'reshili', 'pisali', 'dolya', 'popytki_sred', 'na_datu', 'istochnik']
ZONA = (0.5, 0.8)
PROMAH_PP = 20


def otkryt(path):
    p = Path(path)
    if not p.exists():
        sys.exit(f'❗ нет выгрузки бота: {p}')
    return sqlite3.connect(f'file:{p}?mode=ro', uri=True)


def avatary(db):
    """{child: avatar} for СН, Ни, Ц, В only, without the test child."""
    test = {r for r, in db.execute("select id from deti where sopostavlenie = 'test'")}
    return {c: u for c, u in db.execute("select rebyonok, uroven from avatary") if u in AVATARY and c not in test}


def raboty(db, s_daty=None):
    """Works of the export in lesson order, as dicts; only those with items (and, with s_daty, from that date on)."""
    q = ("select m.id, m.data, m.poryadok, m.vid, m.nomer, m.est_sdacha, m.alternativy "
         "from meropriyatiya m where exists (select 1 from punkty p where p.meropriyatie = m.id) ")
    if s_daty:
        q += "and m.data >= ? "
    q += "order by m.data, m.poryadok"
    kl = ('id', 'data', 'poryadok', 'vid', 'nomer', 'est_sdacha', 'alternativy')
    return [dict(zip(kl, r)) for r in db.execute(q, (s_daty,) if s_daty else ())]


def rabota(db, rid):
    for w in raboty(db):
        if w['id'] == rid:
            return w
    return None


def punkty_raboty(db, rid):
    """[(item, level)] in sheet order."""
    return list(db.execute("select nomer, uroven from punkty where meropriyatie = ? order by poryadok", (rid,)))


def otmetki_est(db, rid):
    return db.execute("select count(*) from otmetki where meropriyatie = ?", (rid,)).fetchone()[0]


def fakt(db, rid):
    """The only counter of the fact. Returns (items, cells, mode): items - [(item, level)];
    cells - {(item, avatar): (reshili, pisali, na_datu)}; mode - 'strogo' | 'chast' (alternative parts)."""
    w = rabota(db, rid)
    if w is None:
        sys.exit(f'❗ работы {rid} нет в выгрузке бота')
    av = avatary(db)
    na = {}
    for c, d in db.execute("select rebyonok, na_datu from avatary"):
        if c in av and d:
            na[av[c]] = max(na.get(av[c], ''), d)
    pun = punkty_raboty(db, rid)
    plus, vse = {}, {}
    for n, c, o in db.execute("select nomer, rebyonok, otmetka from otmetki where meropriyatie = ?", (rid,)):
        if c not in av:
            continue
        vse.setdefault(c, set()).add(n)
        if o == '+':
            plus.setdefault(n, set()).add(c)
    if w['est_sdacha']:
        pisal = {c for c, in db.execute("select rebyonok from sdacha where meropriyatie = ? and status = 'sdal'", (rid,))} & set(av)
    else:
        pisal = {c for s in plus.values() for c in s}
    alt = {x for x in (w['alternativy'] or '').split(',') if x}
    chast = {}                                    # level of a part -> items of that part
    if alt:
        for n, u in pun:
            if u in alt:
                chast.setdefault(u, set()).add(n)
    yach = {}
    for n, u in pun:
        for a in AVATARY:
            kid = {c for c in pisal if av[c] == a}
            if u in chast:
                kid = {c for c in kid if vse.get(c, set()) & chast[u]}
            yach[(n, a)] = (len(kid & plus.get(n, set())), len(kid), na.get(a, ''))
    return pun, yach, ('chast' if chast else 'strogo')


def dolya(reshili, pisali):
    return reshili / pisali if pisali >= MIN_PISALI else None


def stroki_fakta(db, rid):
    pun, yach, rezhim = fakt(db, rid)
    out = []
    for n, u in pun:
        for a in AVATARY:
            r, p, d = yach[(n, a)]
            x = dolya(r, p)
            out.append(dict(rabota_id=rid, punkt=n, uroven_punkta=u, avatar=a, reshili=r, pisali=p,
                            dolya='' if x is None else f'{x:.4f}', popytki_sred='', na_datu=d, istochnik=f'vygruzka:{rezhim}'))
    return out


def chislo_dolya(r):
    """The share of a reshaemost row as a float, None for "нет данных"."""
    try:
        return float(r['dolya'])
    except (ValueError, KeyError, TypeError):
        return None


def chitat_reshaemost(path):
    path = Path(path)
    if not path.exists():
        return []
    with open(path, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def zapisat_reshaemost(path, novye, db):
    """Merges `novye` by key (rabota_id, punkt, avatar); order: lessons of the export, then the old order. Returns (was, now)."""
    stare = chitat_reshaemost(path)
    sl = {(r['rabota_id'], r['punkt'], r['avatar']): r for r in stare}
    for r in novye:
        sl[(r['rabota_id'], r['punkt'], r['avatar'])] = {k: r.get(k, '') for k in POLE}
    por = {}
    for i, w in enumerate(raboty(db)):
        for j, (n, _) in enumerate(punkty_raboty(db, w['id'])):
            por[(w['id'], n)] = (i, j)
    chisl = {k: i for i, k in enumerate(sl)}
    ks = sorted(sl, key=lambda k: (por.get((k[0], k[1]), (10 ** 6, 0)), AVATARY.index(k[2]) if k[2] in AVATARY else 9, chisl[k]))
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=POLE, lineterminator='\n'); w.writeheader()
        for k in ks:
            w.writerow({c: sl[k].get(c, '') for c in POLE})
    return len(stare), len(ks)


def shkala(db, reshaemost):
    ws = raboty(db, S_DATY)
    novye = []
    for w in ws:
        novye += stroki_fakta(db, w['id'])
    bylo, stalo = zapisat_reshaemost(reshaemost, novye, db)
    print(f'шкала: работ {len(ws)} ({", ".join(w["id"] for w in ws)})')
    print(f'строк в {reshaemost}: было {bylo}, записано {len(novye)}, стало {stalo}')
    return novye


def pct(x):
    return '—' if x is None else f'{round(x * 100)} %'


def sverka(papka, db, reshaemost):
    import predskazanie as P
    papka = Path(papka)
    rows = P.chitat(papka)
    if not rows:
        sys.exit(f'❗ нет {papka / P.IMYA} — сверять не с чем (предсказание делается ДО урока)')
    fz, fakt_pun = {}, {}
    rids = []
    for r in rows:
        if r['rabota_id'] not in rids:
            rids.append(r['rabota_id'])
    for rid in rids:
        if rabota(db, rid) is None or not otmetki_est(db, rid):
            sys.exit(f'❗ в выгрузке нет отметок работы {rid} — сверять нечем (сначала загрузить отметки в бот и обновить выгрузку)')
        pun, yach, rezhim = fakt(db, rid)
        fakt_pun[rid] = rezhim
        for (n, a), v in yach.items():
            fz[(rid, n, a)] = v
    cells, bez = [], []
    for r in rows:
        for a in AVATARY:
            pr = P.chislo(r[a])
            v = fz.get((r['rabota_id'], r['punkt'], a))
            if v is None:
                bez.append((r['rabota_id'], r['punkt']))
            rs, ps = (v[0], v[1]) if v else (0, 0)
            fk = dolya(rs, ps) if v else None
            err = None if (fk is None or pr is None) else (pr - fk) * 100
            cells.append(dict(rabota_id=r['rabota_id'], punkt=r['punkt'], uroven=r['uroven'], avatar=a, prognoz=pr,
                              fakt=fk, pisali=ps, reshili=rs, oshibka_pp=err))
    with open(papka / 'SVERKA.csv', 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['rabota_id', 'punkt', 'uroven', 'avatar', 'prognoz', 'fakt', 'pisali', 'reshili', 'oshibka_pp'])
        for c in cells:
            w.writerow([c['rabota_id'], c['punkt'], c['uroven'], c['avatar'],
                        '' if c['prognoz'] is None else f"{c['prognoz']:.4f}",
                        'нет данных' if c['fakt'] is None else f"{c['fakt']:.4f}", c['pisali'], c['reshili'],
                        '' if c['oshibka_pp'] is None else f"{c['oshibka_pp']:+.1f}"])
    md = [f'# Сверка «предсказание → факт» · {papka.name}', '',
          f'Работы: {", ".join(rids)}. Факт — доля «+» среди писавших аватара (пустая клетка = не решил); '
          f'меньше {MIN_PISALI} писавших — «нет данных». Ошибка = прогноз − факт, п. п.: плюс — прогноз выше факта.']
    dok = P.dokazatelstvo_git(papka)
    md += ['', ('✓ ' if dok[0] else '⚠ ') + 'Предсказание ДО урока: ' + dok[1]]
    if bez:
        md += ['', '⚠ Пунктов предсказания нет в выгрузке: ' + ', '.join(f'{a}:{b}' for a, b in sorted(set(bez)))]
    md += ['', '## По аватарам', '', '| аватар | клеток с данными | средняя ошибка | сдвиг | в 50–80 % по факту | промахов > 20 п. п. |', '|---|---|---|---|---|---|']
    for a in AVATARY:
        cs = [c for c in cells if c['avatar'] == a and c['oshibka_pp'] is not None]
        if not cs:
            md.append(f'| {a} | 0 | — | — | — | — |'); continue
        ae = sum(abs(c['oshibka_pp']) for c in cs) / len(cs); sd = sum(c['oshibka_pp'] for c in cs) / len(cs)
        zona = sum(ZONA[0] <= c['fakt'] <= ZONA[1] for c in cs); pm = sum(abs(c['oshibka_pp']) > PROMAH_PP for c in cs)
        napr = 'выше факта' if sd > 0 else 'ниже факта' if sd < 0 else 'ровно'
        md.append(f'| {a} | {len(cs)} из {sum(1 for c in cells if c["avatar"] == a)} | {ae:.1f} п. п. | {sd:+.1f} п. п. ({napr}) | {zona} из {len(cs)} ({round(100 * zona / len(cs))} %) | {pm} |')
    md += ['', '## Трек против факта (средняя решаемость по пунктам с данными)', '', '| аватар | ○ прогноз | ○ факт | △ прогноз | △ факт |', '|---|---|---|---|---|']
    for a in AVATARY:
        line = [a]
        for trek in ('○', '△'):
            cs = [c for c in cells if c['avatar'] == a and P.trek(c['uroven']) == trek and c['fakt'] is not None and c['prognoz'] is not None]
            line += [pct(sum(c['prognoz'] for c in cs) / len(cs)) if cs else '—', pct(sum(c['fakt'] for c in cs) / len(cs)) if cs else '—']
        md.append('| ' + ' | '.join(line) + ' |')
    pm = sorted((c for c in cells if c['oshibka_pp'] is not None and abs(c['oshibka_pp']) > PROMAH_PP), key=lambda c: -abs(c['oshibka_pp']))
    md += ['', f'## Промахи больше {PROMAH_PP} п. п. ({len(pm)})', '']
    if pm:
        md += ['| работа | пункт | аватар | прогноз | факт | писали | ошибка |', '|---|---|---|---|---|---|---|']
        md += [f"| {c['rabota_id']} | {c['punkt']} | {c['avatar']} | {pct(c['prognoz'])} | {pct(c['fakt'])} | {c['pisali']} | {c['oshibka_pp']:+.0f} п. п. |" for c in pm]
    else:
        md.append('Нет.')
    nd = [c for c in cells if c['fakt'] is None]
    md += ['', f'«Нет данных» (писавших < {MIN_PISALI}): клеток {len(nd)} из {len(cells)}.']
    (papka / 'SVERKA.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
    novye = []
    for rid in rids:
        novye += stroki_fakta(db, rid)
    bylo, stalo = zapisat_reshaemost(reshaemost, novye, db)
    print(f'сверка: {len(rows)} пунктов × {len(AVATARY)} аватара, клеток с данными {len(cells) - len(nd)}; '
          f'{papka / "SVERKA.md"}; reshaemost.csv: было {bylo}, стало {stalo}')
    return cells


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('papka', nargs='?'); ap.add_argument('--shkala', action='store_true')
    ap.add_argument('--vygruzka', default=str(VYGRUZKA)); ap.add_argument('--reshaemost', default=str(RESHAEMOST))
    a = ap.parse_args(argv)
    if bool(a.papka) == a.shkala:
        ap.error('нужно одно из двух: --shkala или <папка итерации>')
    db = otkryt(a.vygruzka)
    if a.shkala:
        shkala(db, a.reshaemost)
    else:
        sverka(a.papka, db, a.reshaemost)


if __name__ == '__main__':
    main()
