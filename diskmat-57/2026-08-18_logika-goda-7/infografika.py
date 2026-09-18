#!/usr/bin/env python3
# TOOL-CONTRACT: called-by-hand — the owner reruns it after each lesson
"""Class infographic: who of the kids is where.

Reads the per-lesson hand-in CSVs of one day and writes one self-contained
page INFOGRAFIKA.html next to this script (inline SVG, CSS and JS; no external
files or links).

    python3 infografika.py            # latest day in DAYS
    python3 infografika.py 2026-09-15 # a given day

Adding a day = adding one entry to DAYS. The page shows three things:
  * the matrix kid x task, rows and columns sorted by their totals, with the
    ideal staircase drawn over it;
  * how each kid moves between the first two lessons of the day (slopegraph);
  * how many tasks of the day each kid took (distribution with names).
The evenness of the staircase ("breaks": a kid took a harder task and missed an
easier one, inside one lesson vs between lessons, against randomly reshuffled
tables with the same totals) is computed and printed to stdout, not drawn.
"""
import csv
import html
import itertools
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

DAYS = [
    {
        'date': '2026-09-15',
        'label': '15 сентября',
        'klass': '7И',
        'sheets': [
            {'csv': 'SDACHA-15-09_obratnyj-hod.csv', 'title': 'Обратный ход', 'color': '#2a78d6'},
            {'csv': 'SDACHA-15-09_logika.csv', 'title': 'Правда, ложь и перебор', 'color': '#eb6834'},
        ],
    },
]

VARIANTS_OK = ('A', 'B', '—')
PASSED = set('+в')
MARKS = {'+': 'плюс преподавателя', 'в': 'верный ответ без плюса', 'н': 'неверный ответ',
         '?': 'не прочитано на фото', '-': 'пусто'}
N_RANDOM = 1000     # reshuffled tables for the baseline
SWAPS_PER_STEP = 300
SEED = 15

INK = '#0b0b0b'
INK2 = '#52514e'
INK3 = '#8a8984'
EMPTY = '#ebeae5'


# ---------------------------------------------------------------- data

def short_name(raw):
    """'Карцев Фёдор (примечание)' -> 'Фёдор К.'"""
    parts = re.sub(r'\s*\(.*?\)', '', raw).split()
    return f'{parts[1]} {parts[0][0]}.' if len(parts) > 1 else parts[0]


def surname(raw):
    return re.sub(r'\s*\(.*?\)', '', raw).split()[0]


def load_sheet(path):
    with open(path, encoding='utf-8') as f:
        rows = list(csv.DictReader(f, delimiter=';'))
    tasks = [c for c in rows[0].keys() if re.fullmatch(r'з\d+', c)]
    kids = {}
    for r in rows:
        if r['вариант'] not in VARIANTS_OK:
            continue
        key = surname(r['фамилия_имя'])
        kids[key] = {'name': short_name(r['фамилия_имя']),
                     'marks': [r[t].strip() for t in tasks],
                     'variant': r['вариант']}
    return len(tasks), kids


def build_day(day):
    sheets = []
    for s in day['sheets']:
        n, kids = load_sheet(HERE / s['csv'])
        sheets.append(dict(s, n=n, kids=kids))
    common = sorted(set.intersection(*(set(s['kids']) for s in sheets)))
    cols = [(si, t) for si, s in enumerate(sheets) for t in range(s['n'])]
    kids = []
    for key in common:
        marks = [sheets[si]['kids'][key]['marks'][t] for si, t in cols]
        kids.append({'key': key, 'name': sheets[0]['kids'][key]['name'], 'marks': marks,
                     'ok': [m in PASSED for m in marks],
                     'per_sheet': [sum(sheets[si]['kids'][key]['marks'][t] in PASSED
                                       for t in range(sheets[si]['n'])) for si in range(len(sheets))]})
    for k in kids:
        k['total'] = sum(k['ok'])
    takers = [sum(k['ok'][j] for k in kids) for j in range(len(cols))]
    col_order = sorted(range(len(cols)), key=lambda j: (-takers[j], j))
    kids.sort(key=lambda k: (-k['total'], k['name']))
    for i, k in enumerate(kids):
        k['id'] = f'k{i}'   # surnames never reach the page, not even in attributes
    return sheets, cols, kids, takers, col_order


# ---------------------------------------------------------------- measures

def mismatches(ok_rows, col_order):
    """Cells that differ from the ideal staircase (S filled cells from the left)."""
    out = []
    for ok in ok_rows:
        s = sum(ok)
        out.append(sum(1 for p, j in enumerate(col_order) if ok[j] != (p < s)))
    return out


def breaks(ok_rows, cols, takers):
    """Per kid: (inside one lesson, between lessons). A break = a pair of tasks where
    the kid took the harder one (fewer takers) and not the easier one."""
    pairs = [(a, b) if takers[a] > takers[b] else (b, a)
             for a, b in itertools.combinations(range(len(cols)), 2) if takers[a] != takers[b]]
    same = [cols[e][0] == cols[h][0] for e, h in pairs]
    out = []
    for ok in ok_rows:
        ins = btw = 0
        for (e, h), sm in zip(pairs, same):
            if ok[h] and not ok[e]:
                if sm:
                    ins += 1
                else:
                    btw += 1
        out.append((ins, btw))
    return out


def random_baseline(ok_rows, cols, takers, col_order):
    """Swap randomisation: tables with the same row and column totals."""
    rnd = random.Random(SEED)
    a = [list(r) for r in ok_rows]
    nr, nc = len(a), len(a[0])
    fit, ins, btw = [], [], []
    for _ in range(N_RANDOM):
        for _ in range(SWAPS_PER_STEP):
            r1, r2 = rnd.sample(range(nr), 2)
            c1, c2 = rnd.sample(range(nc), 2)
            if a[r1][c1] and a[r2][c2] and not a[r1][c2] and not a[r2][c1]:
                a[r1][c1] = a[r2][c2] = False
                a[r1][c2] = a[r2][c1] = True
        fit.append(sum(mismatches(a, col_order)))
        b = breaks(a, cols, takers)
        ins.append(sum(x for x, _ in b))
        btw.append(sum(y for _, y in b))
    mean = lambda v: sum(v) / len(v)
    return {'mis': mean(fit), 'inside': mean(ins), 'between': mean(btw)}


# ---------------------------------------------------------------- svg helpers

def esc(s):
    return html.escape(str(s), quote=True)


def text(x, y, s, size=13, anchor='start', fill=INK, weight=None, cls=None, extra=''):
    w = f' font-weight="{weight}"' if weight else ''
    c = f' class="{cls}"' if cls else ''
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" '
            f'fill="{fill}"{w}{c}{extra}>{esc(s)}</text>')


def plural(n, one, few, many):
    n = abs(n)
    if n % 10 == 1 and n % 100 != 11:
        return one
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return few
    return many


# ---------------------------------------------------------------- blocks

def svg_matrix(sheets, cols, kids, takers, col_order):
    name_w, cw, rh, head, right_w = 128, 32, 31, 66, 52
    nc, nr = len(cols), len(kids)
    x0 = name_w
    w = x0 + nc * cw + right_w
    h = head + nr * rh + 4
    out = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Матрица: ученик × задача">']
    # headers
    out.append(text(x0 - 10, 18, f'сдали из {nr}', 12, 'end', INK2))
    out.append(text(x0 - 10, 40, 'задача', 12, 'end', INK2))
    out.append(text(x0 + nc * cw + 10, 40, 'взял', 12, 'start', INK2))
    for p, j in enumerate(col_order):
        si, t = cols[j]
        cx = x0 + p * cw + (cw - 3) / 2
        out.append(text(cx, 18, takers[j], 12, 'middle', INK2))
        out.append(text(cx, 40, t + 1, 13, 'middle', INK, 600))
        out.append(f'<rect x="{x0 + p * cw:.1f}" y="48" width="{cw - 3}" height="5" rx="1.5" '
                   f'fill="{sheets[si]["color"]}"/>')
    # rows
    for i, k in enumerate(kids):
        y = head + i * rh
        out.append(f'<g class="kid" data-k="{k["id"]}">')
        out.append(f'<rect class="rowbg" x="0" y="{y - 1.5}" width="{w}" height="{rh}" fill="transparent"/>')
        out.append(text(x0 - 10, y + rh / 2 + 3, k['name'], 14, 'end', INK))
        for p, j in enumerate(col_order):
            si, t = cols[j]
            ok = k['ok'][j]
            fill = sheets[si]['color'] if ok else EMPTY
            tip = f'{k["name"]} · {sheets[si]["title"]}, задача {t + 1} · {MARKS.get(k["marks"][j], k["marks"][j])}'
            out.append(f'<rect class="cell" x="{x0 + p * cw:.1f}" y="{y:.1f}" width="{cw - 3}" '
                       f'height="{rh - 3}" rx="3" fill="{fill}" data-t="{esc(tip)}"/>')
        out.append(text(x0 + nc * cw + 10, y + rh / 2 + 3, k['total'], 14, 'start', INK, 600))
        out.append('</g>')
    # ideal staircase line
    pts = []
    for i, k in enumerate(kids):
        x = x0 + k['total'] * cw - 1.5
        y1, y2 = head + i * rh - 1.5, head + (i + 1) * rh - 1.5
        pts += [(x, y1), (x, y2)]
    d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    out.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round" '
               f'pointer-events="none"/>')
    out.append('</svg>')
    return '\n'.join(out)


def slope_positions(kids, a, b):
    order_a = sorted(kids, key=lambda k: (-k['per_sheet'][a], -k['per_sheet'][b], k['name']))
    order_b = sorted(kids, key=lambda k: (-k['per_sheet'][b], -k['per_sheet'][a], k['name']))
    pa = {k['key']: i for i, k in enumerate(order_a)}
    pb = {k['key']: i for i, k in enumerate(order_b)}
    return order_a, order_b, pa, pb


def pair_counts(kids, a, b):
    keep = swap = tie = 0
    for k1, k2 in itertools.combinations(kids, 2):
        d = (k1['per_sheet'][a] - k2['per_sheet'][a]) * (k1['per_sheet'][b] - k2['per_sheet'][b])
        if d > 0:
            keep += 1
        elif d < 0:
            swap += 1
        else:
            tie += 1
    return keep, swap, tie


def svg_slope(sheets, kids, a=0, b=1):
    W, pitch, top = 640, 19, 50
    xl_name, xl_dot, xr_dot, xr_name = 176, 186, 454, 464
    order_a, order_b, pa, pb = slope_positions(kids, a, b)
    n = len(kids)
    h = top + n * pitch + 6
    y = lambda i: top + i * pitch + pitch / 2
    # crossings must equal swapped pairs (ties are broken by the other lesson)
    cross = sum(1 for k1, k2 in itertools.combinations(kids, 2)
                if (pa[k1['key']] - pa[k2['key']]) * (pb[k1['key']] - pb[k2['key']]) < 0)
    keep, swap, tie = pair_counts(kids, a, b)
    assert cross == swap, (cross, swap)
    out = [f'<svg viewBox="0 0 {W} {h:.0f}" role="img" aria-label="Переезд детей между двумя уроками">',
           '<defs><linearGradient id="mv" gradientUnits="userSpaceOnUse" '
           f'x1="{xl_dot}" y1="0" x2="{xr_dot}" y2="0"><stop offset="0" stop-color="{sheets[a]["color"]}"/>'
           f'<stop offset="1" stop-color="{sheets[b]["color"]}"/></linearGradient></defs>']
    out.append(f'<rect x="30" y="8" width="10" height="10" rx="2" fill="{sheets[a]["color"]}"/>')
    out.append(text(45, 17, sheets[a]['title'], 13, 'start', INK, 600))
    out.append(f'<rect x="{xr_name}" y="8" width="10" height="10" rx="2" fill="{sheets[b]["color"]}"/>')
    out.append(text(xr_name + 15, 17, sheets[b]['title'], 13, 'start', INK, 600))
    out.append(text(14, 38, f'из {sheets[a]["n"]}', 11, 'middle', INK2))
    out.append(text(W - 14, 38, f'из {sheets[b]["n"]}', 11, 'middle', INK2))
    # score brackets
    for order, xb, xn, s in ((order_a, 30, 14, a), (order_b, W - 30, W - 14, b)):
        i = 0
        while i < n:
            j = i
            while j + 1 < n and order[j + 1]['per_sheet'][s] == order[i]['per_sheet'][s]:
                j += 1
            out.append(f'<line x1="{xb}" y1="{y(i) - 7:.1f}" x2="{xb}" y2="{y(j) + 7:.1f}" '
                       f'stroke="{INK3}" stroke-width="1.5" stroke-linecap="round"/>')
            out.append(text(xn, (y(i) + y(j)) / 2 + 4.5, order[i]['per_sheet'][s], 13, 'middle', INK, 600))
            i = j + 1
    # lines, far movers on top
    lines = sorted(kids, key=lambda k: abs(pa[k['key']] - pb[k['key']]))
    for k in lines:
        ia, ib = pa[k['key']], pb[k['key']]
        far = abs(ia - ib) >= n // 3
        out.append(f'<g class="kid{" far" if far else ""}" data-k="{k["id"]}">'
                   f'<line class="mvl" x1="{xl_dot}" y1="{y(ia):.1f}" x2="{xr_dot}" y2="{y(ib):.1f}" '
                   f'stroke="url(#mv)" stroke-width="{2.6 if far else 1.6}" '
                   f'stroke-opacity="{1 if far else 0.45}" stroke-linecap="round"/>'
                   f'<line x1="{xl_dot}" y1="{y(ia):.1f}" x2="{xr_dot}" y2="{y(ib):.1f}" '
                   f'stroke="transparent" stroke-width="9"/>'
                   f'<circle cx="{xl_dot}" cy="{y(ia):.1f}" r="3.5" fill="{sheets[a]["color"]}"/>'
                   f'<circle cx="{xr_dot}" cy="{y(ib):.1f}" r="3.5" fill="{sheets[b]["color"]}"/>'
                   + text(xl_name, y(ia) + 4.5, k['name'], 13, 'end', INK if far else INK2,
                          600 if far else None)
                   + text(xr_name, y(ib) + 4.5, k['name'], 13, 'start', INK if far else INK2,
                          600 if far else None)
                   + '</g>')
    out.append('</svg>')
    return '\n'.join(out), (keep, swap, tie)


def svg_distribution(kids, ncols):
    """How many tasks of the day each kid took: one row per total (empty totals kept,
    so the shape of the distribution stays honest), each kid a dot with a name."""
    W, pitch, top, ax, chip = 640, 21, 26, 64, 128
    hi, lo = max(k['total'] for k in kids), min(k['total'] for k in kids)
    rows = list(range(hi, lo - 1, -1))
    h = top + len(rows) * pitch + 4
    out = [f'<svg viewBox="0 0 {W} {h}" role="img" aria-label="Сколько задач взял каждый ребёнок">',
           text(0, 14, f'задач из {ncols}', 12, 'start', INK2)]
    for r, total in enumerate(rows):
        y = top + r * pitch + pitch / 2
        group = [k for k in kids if k['total'] == total]
        out.append(text(ax - 14, y + 5, total, 13, 'end', INK if group else INK3, 600 if group else None))
        for i, k in enumerate(group):
            x = ax + 6 + i * chip
            out.append(f'<g class="kid" data-k="{k["id"]}">'
                       f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{INK2}"/>'
                       + text(x + 12, y + 5, k['name'], 13, 'start', INK) + '</g>')
    out.append(f'<line x1="{ax - 4}" y1="{top}" x2="{ax - 4}" y2="{h - 4}" stroke="{INK3}" stroke-width="1.5"/>')
    out.append('</svg>')
    return '\n'.join(out)


# ---------------------------------------------------------------- page

CSS = """
*{box-sizing:border-box}
html,body{margin:0;background:#fcfcfb;color:#0b0b0b}
body{font:15px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;padding:18px 24px 22px}
svg{display:block;width:100%;height:auto;font-family:inherit}
header{display:flex;align-items:baseline;gap:28px;flex-wrap:wrap;margin-bottom:12px}
h1{font-size:26px;margin:0;font-weight:700;letter-spacing:-.01em}
.legend{display:flex;gap:20px;color:#52514e;font-size:14px}
.legend i{display:inline-block;width:12px;height:12px;border-radius:2px;margin-right:6px;vertical-align:-1px}
main{display:grid;grid-template-columns:58fr 42fr;gap:34px;align-items:start}
.side{display:grid;gap:26px}
figure{margin:0}
.kid{transition:opacity .12s}
body.hover .kid{opacity:.22}
body.hover .kid.hl{opacity:1}
body.hover .kid.hl .rowbg{fill:#f1efe8}
body.hover .kid.hl .mvl{stroke-opacity:1;stroke-width:3}
#tip{position:fixed;pointer-events:none;background:#0b0b0b;color:#fff;font-size:13px;padding:5px 8px;
 border-radius:4px;display:none;white-space:nowrap;z-index:9}
@media (max-width:900px){main{grid-template-columns:1fr}}
"""

JS = """
(function(){
  var tip=document.getElementById('tip'), cur=null;
  function mark(k){
    if(k===cur)return; cur=k;
    document.querySelectorAll('.kid.hl').forEach(function(e){e.classList.remove('hl')});
    if(k){document.body.classList.add('hover');
      document.querySelectorAll('.kid').forEach(function(e){if(e.getAttribute('data-k')===k)e.classList.add('hl')});}
    else document.body.classList.remove('hover');
  }
  document.addEventListener('mouseover',function(ev){
    var g=ev.target.closest('.kid'); mark(g?g.getAttribute('data-k'):null);
    var t=ev.target.getAttribute&&ev.target.getAttribute('data-t');
    if(t){tip.textContent=t;tip.style.display='block';}else tip.style.display='none';
  });
  document.addEventListener('mousemove',function(ev){
    if(tip.style.display==='block'){tip.style.left=(ev.clientX+14)+'px';tip.style.top=(ev.clientY+14)+'px';}
  });
  document.addEventListener('mouseleave',function(){mark(null);tip.style.display='none';});
})();
"""


def render(day):
    sheets, cols, kids, takers, col_order = build_day(day)
    ok_rows = [k['ok'] for k in kids]
    # The evenness measures stay in the generator and go to stdout (decision Р137),
    # but are no longer drawn on the page (owner, ПРАВКА 2 of 18.09).
    mis = mismatches(ok_rows, col_order)
    per_kid = breaks(ok_rows, cols, takers)
    base = random_baseline(ok_rows, cols, takers, col_order)
    ncell = len(kids) * len(cols)
    agree = ncell - sum(mis)
    rand_agree = ncell - base['mis']
    matrix = svg_matrix(sheets, cols, kids, takers, col_order)
    slope, (keep, swap, tie) = svg_slope(sheets, kids) if len(sheets) >= 2 else ('', (0, 0, 0))
    dist = svg_distribution(kids, len(cols))
    n = len(kids)
    legend = ''.join(f'<span><i style="background:{s["color"]}"></i>{esc(s["title"])}, {s["n"]} '
                     f'{plural(s["n"], "задача", "задачи", "задач")}</span>' for s in sheets)
    # Explanations are off the page by the owner's rule "a good infographic needs no comments"
    # (ПРАВКА 1 of 18.09). Kept here as the key to what is drawn:
    #   matrix — row = kid, column = task (number inside its lesson), coloured cell = passed
    #            (plus or a correct answer); kids with more tasks on top, tasks taken by more
    #            kids on the left; the black step = the ideal staircase: with a strict order
    #            every coloured cell would lie left of it.
    #   slope  — line = kid: left his place in the first lesson, right in the second; numbers
    #            at the edges = tasks taken; a crossing = two kids who swapped places
    #            (swap / keep / tie pairs are printed to stdout).
    #   dist   — one row per day total, every kid a dot with a name.
    title = f'{day["klass"]} · {day["label"]} · кто из детей где'
    page = f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<style>{CSS}</style></head>
<body>
<header><h1>{esc(title)}</h1><div class="legend">{legend}</div></header>
<main>
<figure>{matrix}</figure>
<div class="side">
<figure>{slope}</figure>
<figure>{dist}</figure>
</div>
</main>
<div id="tip"></div>
<script>{JS}</script>
</body></html>
"""
    stats = {'kids': n, 'cells': ncell, 'agree': agree, 'rand_agree': rand_agree,
             'inside': sum(a for a, _ in per_kid), 'between': sum(b for _, b in per_kid),
             'rand_inside': base['inside'], 'rand_between': base['between'],
             'keep': keep, 'swap': swap, 'tie': tie}
    return page, stats


def main():
    want = sys.argv[1] if len(sys.argv) > 1 else None
    days = [d for d in DAYS if want in (None, d['date'])]
    if not days:
        sys.exit(f'no day {want!r} in DAYS')
    day = days[-1]
    page, stats = render(day)
    out = HERE / 'INFOGRAFIKA.html'
    out.write_text(page, encoding='utf-8')
    print(f'{out.name}: day {day["date"]} · ' + ' · '.join(f'{k}={v:.1f}' if isinstance(v, float) else f'{k}={v}'
                                                          for k, v in stats.items()))


if __name__ == '__main__':
    main()
