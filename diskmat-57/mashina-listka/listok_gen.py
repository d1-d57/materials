# -*- coding: utf-8 -*-
"""ГЕНЕРАТОР ЛИСТКА спецмата 7И (формат 22.09 → 29.09, Р196–Р199). Данные → HTML → PDF (Chromium).

Выход руками не правится: правится файл данных листка (например listok_29-09_dannye.py) или этот генератор.

Терминология (закреплена, см. FORMAT-listka-po-otvetu.md):
  стр. 1 — «Обязательные задачи»: кружки ○ (техника) и треугольники △ (идея). Две тропы к оценке «4»:
           все ○ ИЛИ все △.
  стр. 2 — «Дополнительные задачи»: номера без значков; ★ — звёздочки (открываются после вершины карты).
  шапка на КАЖДОЙ странице: «<тема>» слева, «<дата> · <класс> · вариант <В>» справа;
  «Фамилия, имя» — ТОЛЬКО на первой странице.
Поля ответа (формат 22.09): у задачи слева узкий блок «пункт · ответ · подпись» (подпись принимающего и
есть плюс); длинный ответ (выписать список) и шаблон-прочерки — строкой во всю ширину колонки под условием.

Спецификация задачи (dict):
  mark  '○' | '△' | '' | '★'         num   номер         text  условие (HTML, <br> разрешён)
  block ['а','б'] или [''] или None   — узкий блок слева (None — блока нет)
  rows  [{'h':20} | {'tpl':['_','+','_','=','_'],'lab':'б'}] — строки во всю ширину под условием
  pics  [svg, ...] + pics_wide True/False — картинки под условием (wide: во всю ширину, иначе в колонке текста)
Карта: map_svg(spec) — см. docstring функции.
"""
import re, html
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt

CSS = '''
@page{size:A4;margin:8mm 10mm 7mm}
:root{--ink:#1d1d1b;--mute:#6b6a64;--line:#8a877d;--sh:#d9d6cc;--grid:#cfccc2;--topo:#cdcabf}
*{box-sizing:border-box}
body{margin:0;font:10.3pt/1.25 "Liberation Serif","DejaVu Serif",serif;color:var(--ink);background:#fff}
.page{page-break-after:always;break-after:page;height:282mm;overflow:hidden;position:relative}
.page:last-child{page-break-after:auto;break-after:auto}
.hd{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1.6px solid var(--ink);padding-bottom:2px}
.hd b{font-size:15.5pt}.hd span{font-size:9.5pt;color:var(--mute)}
.fio{margin:4px 0 2px;font-size:10.5pt;display:flex;gap:6px}.fio span{flex:1;border-bottom:1px solid var(--ink)}
.sec{font-weight:700;font-size:12pt;margin:2mm 0 1.6mm}
.two{display:grid;grid-template-columns:1fr 63mm;gap:0 5mm}
/* ПОТОК, а не сетка (Р204): поле ответа — float слева, картинка — float справа; текст этой и СЛЕДУЮЩИХ задач обтекает
   картинку, как wrapfigure в TeX; пустой полосы рядом с картинкой нет. Строки-поля — отдельный контекст (grid), они
   сужаются рядом с картинкой, а не залезают под неё. */
.z{clear:left;margin:0 0 2.2mm;position:relative}
.ab{float:left;width:var(--abw,46mm);margin:0 3.5mm .8mm 0;border:1px solid var(--ink)}
.z .tx{margin-left:calc(var(--abw,46mm) + 3.5mm)}
.z.w .tx{margin-left:0}
.ab .r{display:grid;grid-template-columns:4mm 1fr 8.5mm;height:var(--rowh,7mm)}
.ab .r+.r{border-top:1px solid var(--ink)}
.ab .l{font-size:8.5pt;padding:1px 0 0 1.2mm}.ab .s{border-left:1px solid var(--ink)}
.ab.one .r{grid-template-columns:1fr 9mm;height:8.5mm}
.n{font-weight:700;white-space:nowrap}
.full{clear:left;margin-top:1.4mm;display:grid;grid-template-columns:1fr 9mm;border:1px solid var(--ink);position:relative}
.full .s{border-left:1px solid var(--ink)}
.full .tp{display:flex;align-items:flex-end;justify-content:space-around;padding:0 4mm 1.6mm 6mm;font-size:13pt}
.full .tp .sl{flex:0 1 22mm;border-bottom:1.3px solid var(--ink);height:6mm}
.full .tp .op{padding:0 1.5mm}
.full .lb{font-size:8.5pt;padding:1px 0 0 1.2mm;position:absolute;left:0;top:0}
.pics{display:flex;gap:5mm;align-items:flex-end;margin-top:1.5mm}
.pics.wide{clear:left;justify-content:space-between;padding-left:2mm}
.pics.float{float:right;clear:right;margin:0 0 1mm 3mm;display:block}
/* задача с угловой раскладкой (○2 29.09): высокая картинка слева, текст в «закутке» над низкими, полоса полей под всеми */
.ugol{display:grid;grid-template-columns:auto 1fr 1fr;column-gap:4mm;align-items:end}
.ugol .t{grid-column:2/4;align-self:start}
.ugol .p1{grid-row:1/3}
.ugol figure{margin:0;text-align:center;font-size:8.5pt}
.strip{clear:left;display:grid;gap:2.5mm;margin-top:1.4mm}
/* правая рамка у края листа срезалась наполовину (субпиксель при печати) — отступ .4 мм (Р208) */
.full,.strip{margin-right:.4mm}
.strip.kor{width:var(--abw,46mm);margin-top:1mm}
.strip .c{display:grid;grid-template-columns:4mm 1fr 8.5mm;height:8mm;border:1px solid var(--ink)}
.strip .c .l{font-size:8.5pt;padding:1px 0 0 1.2mm}.strip .c .s{border-left:1px solid var(--ink)}
.kom{margin-top:.8mm}.ctr{text-align:center;margin:.6mm 0 0;word-spacing:.15em}
.rules ul{margin:0;padding-left:3.5mm}.rules li{margin:0 0 1mm}
.foot{position:absolute;left:0;right:0;bottom:0;font-weight:700;font-size:10.5pt;border-top:1px solid var(--ink);padding-top:1.2mm}
.pics figure{margin:0;text-align:center;font-size:8.5pt}
svg{display:block}
.s-grid{stroke:var(--grid);stroke-width:.18}.s-out{fill:none;stroke:var(--ink);stroke-width:.45;stroke-linecap:round}
.rules{font-size:9.2pt;line-height:1.23;margin-top:1.5mm;border-top:1px solid var(--ink);padding-top:1.2mm}
.rules p{margin:0 0 1.1mm}.rules b{font-size:9pt}.gl{font-family:"DejaVu Sans",sans-serif;font-size:8.5pt}
.m-topo{fill:none;stroke:var(--topo);stroke-width:.22}
.m-road{fill:none;stroke:#fff;stroke-width:1.9;stroke-linecap:round}
.m-edge{fill:none;stroke:var(--ink);stroke-width:.55;stroke-linecap:round}
.m-cell{fill:#fff;stroke:var(--ink);stroke-width:.45}
.m-lab{font:bold 2.75px "Liberation Sans","DejaVu Sans",sans-serif;fill:var(--ink);text-anchor:middle;dominant-baseline:central}
.m-lab2{font:2.5px "Liberation Sans","DejaVu Sans",sans-serif;fill:var(--mute);text-anchor:middle;dominant-baseline:central}
.m-cp{fill:var(--ink)}.m-cpt{font:bold 3.2px "Liberation Sans",sans-serif;fill:#fff;text-anchor:middle;dominant-baseline:central}
.m-sym{font:4.2px "DejaVu Sans",sans-serif;fill:var(--ink);text-anchor:middle;dominant-baseline:central}
.m-coin{fill:#5c5a55;stroke:var(--ink);stroke-width:.3}
.m-tent{fill:var(--sh);stroke:var(--ink);stroke-width:.45;stroke-linejoin:round}
'''
def nbsp(t):
    """Неразрывные пробелы: формула не рвётся («x + 2y + 5z = 17»), «(а)» не отрывается от пункта,
    число — от слова («2 меридиана»), тире — от предыдущего слова."""
    t = re.sub(r'(?<=[\w\d)]) ([+=−·×]) (?=[\w\d(])', r'&nbsp;\1&nbsp;', t)
    t = re.sub(r'\((а|б|в|г)\) ', r'(\1)&nbsp;', t)
    t = t.replace(' — ', '&nbsp;— ')
    t = re.sub(r' (и|или) (\d)', r'&nbsp;\1&nbsp;\2', t)
    return re.sub(r'(?<![\d,])(\d+) (?=[а-яё])', r'\1&nbsp;', t)

# ---------------- клетчатая картинка в стиле Шеня: штриховка на клетчатом фоне ----------------
def shen(m, n, inside, cell=2.8, pid='h', margin=1):
    """m строк × n столбцов; inside(r,c) — клетка фигуры. Сетка видна сквозь штриховку, контур жирный."""
    W = (n + 2 * margin) * cell; H = (m + 2 * margin) * cell; s = []
    for i in range(n + 2 * margin + 1): s.append(f'<line x1="{i*cell:.2f}" y1="0" x2="{i*cell:.2f}" y2="{H:.2f}" class="s-grid"/>')
    for j in range(m + 2 * margin + 1): s.append(f'<line x1="0" y1="{j*cell:.2f}" x2="{W:.2f}" y2="{j*cell:.2f}" class="s-grid"/>')
    X = lambda c: (c + margin) * cell
    ins = lambda r, c: 0 <= r < m and 0 <= c < n and inside(r, c)
    for r in range(m):
        for c in range(n):
            if ins(r, c): s.append(f'<rect x="{X(c):.2f}" y="{X(r):.2f}" width="{cell+.01:.2f}" height="{cell+.01:.2f}" fill="url(#{pid})"/>')
    for r in range(-1, m + 1):
        for c in range(-1, n + 1):
            if ins(r, c) != ins(r, c + 1) and 0 <= r < m: s.append(f'<line x1="{X(c+1):.2f}" y1="{X(r):.2f}" x2="{X(c+1):.2f}" y2="{X(r+1):.2f}" class="s-out"/>')
            if ins(r, c) != ins(r + 1, c) and 0 <= c < n: s.append(f'<line x1="{X(c):.2f}" y1="{X(r+1):.2f}" x2="{X(c+1):.2f}" y2="{X(r+1):.2f}" class="s-out"/>')
    hatch = (f'<defs><pattern id="{pid}" patternUnits="userSpaceOnUse" width="1.1" height="1.1" patternTransform="rotate(45)">'
             f'<line x1="0" y1="0" x2="0" y2="1.1" stroke="#1d1d1b" stroke-width=".32"/></pattern></defs>')
    return f'<svg viewBox="0 0 {W:.2f} {H:.2f}" style="width:{W:.2f}mm;height:{H:.2f}mm" role="img" aria-label="клетчатая фигура">{hatch}{"".join(s)}</svg>'

# ---------------- поля ответа ----------------
def block(labels):
    if labels == ['']: return '<div class="ab one"><div class="r"><div></div><div class="s"></div></div></div>'
    return '<div class="ab">' + ''.join(f'<div class="r"><div class="l">{l}</div><div></div><div class="s"></div></div>' for l in labels) + '</div>'
def row(r):
    lab = f'<span class="lb">{r.get("lab","")}</span>'
    if 'tpl' in r:
        parts = ''.join('<span class="sl"></span>' if x == '_' else f'<span class="op">{x}</span>' for x in r['tpl'])
        return f'<div class="full" style="height:{r.get("h",9.5)}mm">{lab}<div class="tp">{parts}</div><div class="s"></div></div>'
    return f'<div class="full" style="height:{r["h"]}mm">{lab}<div></div><div class="s"></div></div>'
def strip(labels, kor=False, cols=None, h=None):
    """Полоса полей в одну строку. cols — свои ширины ('3fr 1fr'): длинный пункт и короткий рядом; h — высота, мм."""
    hs = f' style="height:{h}mm"' if h else ''
    return (f'<div class="strip{" kor" if kor else ""}" style="grid-template-columns:{cols or f"repeat({len(labels)},1fr)"}">' +
            ''.join(f'<div class="c"{hs}><div class="l">{l}</div><div></div><div class="s"></div></div>' for l in labels) + '</div>')
def task(z):
    """Поле ответа выбирается по ДЛИНЕ ответа, а не по разделу (Р204): короткое число/выражение — узкий блок слева
    (block); одна строка перечисления — строка во всю ширину (rows h≈8); многострочное перечисление — высокая строка.
    Картинки: pics_float — справа с обтеканием (и следующие задачи обтекают); pics_wide — ряд во всю ширину;
    ugol — высокая первая картинка слева, текст в закутке над остальными, полоса полей strip под всеми."""
    head = f'<span class="n">{z.get("mark","")}{z["num"]}.</span> '
    txt = nbsp(z['text'])
    caps = z.get('pic_caps', [''] * 9)
    if z.get('ugol'):
        P = z['pics']
        figs = f'<figure class="p1">{P[0]}{caps[0]}</figure><div class="t">{head}{txt}</div>' + ''.join(f'<figure>{p}{caps[i+1]}</figure>' for i, p in enumerate(P[1:]))
        return f'<div class="z w"><div class="ugol">{figs}</div>{strip(z["strip"])}</div>'
    pics = ''
    if z.get('pics'):
        figs = ''.join(f'<figure>{p}{caps[i]}</figure>' for i, p in enumerate(z['pics']))
        pics = f'<div class="pics{" wide" if z.get("pics_wide") else ""}{" float" if z.get("pics_float") else ""}">{figs}</div>'
    flt = pics if z.get('pics_float') else ''
    inner = pics if pics and not z.get('pics_float') and not z.get('pics_wide') else ''
    after = pics if z.get('pics_wide') else ''
    rows = ''.join(row(r) for r in z.get('rows', [])) + (strip(z['strip'], z.get('strip_kor'), z.get('strip_cols'), z.get('strip_h')) if z.get('strip') else '')
    if z.get('block') is None:
        return f'<div class="z w">{flt}<div class="tx">{head}{txt}{inner}</div>{after}{rows}</div>'
    return f'<div class="z">{flt}{block(z["block"])}<div class="tx">{head}{txt}{inner}</div>{after}{rows}</div>'

# ---------------- карта-восхождение ----------------
def _curve(a, b, bend=0.0):
    (x1, y1), (x2, y2) = a, b; mx, my = (x1 + x2) / 2, (y1 + y2) / 2; dx, dy = x2 - x1, y2 - y1
    return f'M{x1:.2f},{y1:.2f} Q{mx-dy*bend:.2f},{my+dx*bend:.2f} {x2:.2f},{y2:.2f}'
def _diamond(x, y, r): return f'<polygon points="{x:.2f},{y-r:.2f} {x+r:.2f},{y:.2f} {x:.2f},{y+r:.2f} {x-r:.2f},{y:.2f}" class="m-cell"/>'
def _topo(W, H, peak, camp, seed):
    xs = np.linspace(0, W, 160); ys = np.linspace(0, H, 480); X, Y = np.meshgrid(xs, ys)
    px, py = peak; cx, cy = camp
    F = 1.25 * np.exp(-(((X - px) / 30) ** 2 + ((Y - py) / 55) ** 2))
    rng = np.random.default_rng(seed)
    for _ in range(9):
        ax, ay = rng.uniform(0, W), rng.uniform(py, cy + 10); s = rng.uniform(6, 14); h = rng.uniform(-.18, .22)
        F += h * np.exp(-(((X - ax) / s) ** 2 + ((Y - ay) / s) ** 2))
    F += .35 * np.exp(-(((X - px) / 9) ** 2 + ((Y - py) / 12) ** 2))
    fig = plt.figure(); cs = plt.contour(X, Y, F, levels=np.linspace(.12, 1.55, 15)); plt.close(fig)
    out = []
    for segs in cs.allsegs:
        for sg in segs:
            if len(sg) < 8 or (np.ptp(sg[:, 0]) < 14 and np.ptp(sg[:, 1]) < 14): continue   # мелкие петли похожи на узлы
            out.append('<path d="M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in sg[::2]) + '" class="m-topo"/>')
    return ''.join(out)
def map_svg(M):
    """M: W,H (мм) · camp (x,y) · peak (x,y) · nodes {id: dict(x,y,kind,label,sym)} ·
    edges [(a,b,bend)] — a,b: id узла или 'CAMP'/'PEAK' · starts [(node_id, 'left'|'right')] · seed.
    kind: 'circ' (кружок-тропа), 'tri' (треугольник-тропа), 'romb', 'star'. sym: None|'skull'|'coin'|'star'.
    Все линии одного вида: у линии нет смысла, кроме «отсюда можно идти сюда, вверх»."""
    W, H = M['W'], M['H']; P = lambda k: M['camp'] if k == 'CAMP' else M['peak'] if k == 'PEAK' else (M['nodes'][k]['x'], M['nodes'][k]['y'])
    s = [_topo(W, H, M['peak'], M['camp'], M.get('seed', 7))]
    paths = [_curve(P(a), P(b), bd) for a, b, bd in M['edges']]
    s += [f'<path d="{d}" class="m-road"/>' for d in paths] + [f'<path d="{d}" class="m-edge"/>' for d in paths]
    for nid, side in M['starts']:                          # флажок старта — сбоку от первого значка, не налезает
        x, y = P(nid); sg = -1 if side == 'left' else 1; px = x + sg * 4.6
        s.append(f'<path d="M{px:.2f},{y+3.2:.2f} L{px:.2f},{y-3.4:.2f} L{px+sg*3.4:.2f},{y-2.4:.2f} L{px:.2f},{y-1.4:.2f}" class="m-tent"/>')
        s.append(f'<text x="{px+sg*1.4:.2f}" y="{y+5.0:.2f}" class="m-lab2">старт</text>')
    x, y = M['camp']                                        # лагерь и чекпоинт «4»
    s.append(f'<path d="M{x-5.2:.2f},{y+2.6:.2f} L{x:.2f},{y-4.2:.2f} L{x+5.2:.2f},{y+2.6:.2f} Z" class="m-tent"/><path d="M{x-1.2:.2f},{y+2.6:.2f} L{x:.2f},{y-.4:.2f} L{x+1.2:.2f},{y+2.6:.2f}" class="m-edge"/>')
    if M.get('checkpoints'): s.append(f'<circle cx="{x+7.2:.2f}" cy="{y+.4:.2f}" r="2.4" class="m-cp"/><text x="{x+7.2:.2f}" y="{y+.5:.2f}" class="m-cpt">4</text>')
    for nid, d in M['nodes'].items():
        x, y, k = d['x'], d['y'], d['kind']; lab = d['label']; sym = d.get('sym')
        if k == 'circ':
            s.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.5" class="m-cell"/><text x="{x:.2f}" y="{y+.1:.2f}" class="m-lab">{lab}</text>'); continue
        if k == 'tri':
            s.append(f'<polygon points="{x:.2f},{y-2.9:.2f} {x+2.9:.2f},{y+2.1:.2f} {x-2.9:.2f},{y+2.1:.2f}" class="m-cell"/><text x="{x:.2f}" y="{y+.6:.2f}" class="m-lab">{lab}</text>'); continue
        if sym:
            s.append(_diamond(x, y, 5.0) + f'<text x="{x:.2f}" y="{y-1.35:.2f}" class="m-lab">{lab}</text>')
            if sym == 'skull': s.append(f'<text x="{x:.2f}" y="{y+1.9:.2f}" class="m-sym">☠</text>')
            if sym == 'star': s.append(f'<text x="{x:.2f}" y="{y+1.9:.2f}" class="m-sym">★</text>')
            if sym == 'coin': s.append(f'<circle cx="{x:.2f}" cy="{y+1.9:.2f}" r="1.55" class="m-coin"/>')
        else:
            s.append(_diamond(x, y, 4.1) + f'<text x="{x:.2f}" y="{y:.2f}" class="m-lab">{lab}</text>')
    x, y = M['peak']                                        # вершина и чекпоинт «5»
    s.append(f'<path d="M{x-6.5:.2f},{y+3:.2f} L{x-2.6:.2f},{y-2.2:.2f} L{x-1.2:.2f},{y-.6:.2f} L{x+1.4:.2f},{y-4.6:.2f} L{x+6.5:.2f},{y+3:.2f} Z" class="m-tent"/>')
    s.append(f'<path d="M{x+1.4:.2f},{y-4.6:.2f} L{x+1.4:.2f},{y-8.6:.2f} L{x+4.4:.2f},{y-7.7:.2f} L{x+1.4:.2f},{y-6.8:.2f}" class="m-tent"/>')
    if M.get('checkpoints'): s.append(f'<circle cx="{x-8.6:.2f}" cy="{y+1.4:.2f}" r="2.4" class="m-cp"/><text x="{x-8.6:.2f}" y="{y+1.5:.2f}" class="m-cpt">5</text>')
    return f'<svg viewBox="0 0 {W} {H}" style="width:{W}mm;height:{H}mm" role="img" aria-label="карта-восхождение">{"".join(s)}</svg>'

# ---------------- страницы ----------------
def header(L, v): return f'<div class="hd"><b>{L["title"]}</b><span>{L["date"]} · {L["klass"]} · вариант {v}</span></div>'
def page(L, v, P, first, pol=False):
    fio = '<div class="fio">Фамилия, имя: <span></span></div>' if first else ''
    # na_vsyu=True у задачи — она встаёт ПОД колонками (карта кончилась) и идёт на всю ширину страницы (Р208)
    uz = [z for z in P['items'] if not (P.get('side') and z.get('na_vsyu'))]
    shir = [z for z in P['items'] if P.get('side') and z.get('na_vsyu')]
    body = f'<div class="sec">{P["heading"]}</div>' + ''.join(task(z) for z in uz)
    if P.get('side'):
        body = f'<div class="two"><div>{body}</div><div>{P["side"]}</div></div>' + ''.join(task(z) for z in shir)
    st = ';'.join(x for x in (f'--abw:{P["abw"]}' if P.get('abw') else '', f'--rowh:{P["rowh"]}' if P.get('rowh') else '') if x)
    st = f' style="{st}"' if st else ''
    foot = f'<div class="foot">{P["footer"]}</div>' if P.get('footer') else ''
    return f'<div class="page{" pol" if pol else ""}"{st}>{header(L, v)}{fio}{body}{foot}</div>'
def document(L, v, pages, extra_css=''):
    return (f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>{html.escape(L["title"])} · {v}</title>'
            f'<style>{CSS}{extra_css}</style></head><body>' + ''.join(page(L, v, P, i == 0) for i, P in enumerate(pages)) + '</body></html>')
POL_CSS = '''
.list{height:282mm;overflow:hidden;page-break-after:always;break-after:page}
.list:last-child{page-break-after:auto;break-after:auto}
.page.pol{height:136mm;page-break-after:auto;break-after:auto}
.rez{height:9.5mm;position:relative}
.rez:before{content:"";position:absolute;left:0;right:0;top:50%;border-top:1px dashed var(--line)}
.rez span{position:absolute;left:50%;top:50%;transform:translate(-50%,-55%);background:#fff;padding:0 2mm;color:var(--line);font-family:"DejaVu Sans",sans-serif}'''
def polulist(L, halves, extra_css=''):
    """ФОРМАТ «ПОЛ-ЛИСТА НА ЧЕЛОВЕКА» (Р209, железно): всё, что раздаётся по одному экземпляру на ребёнка и помещается, —
    контрольная, ДЗ — верстается на половину A4 (190 × 136 мм); на листе две половины и линия реза ровно посередине.
    halves = [(вариант, P), ...] по порядку: контрольная — [(А, P), (Б, P)] (режем и раздаём по вариантам),
    ДЗ — [('', P), ('', P)] (два одинаковых). Перелив половины проверяет fit_report (каждая половина — .page)."""
    sh = []
    for i in range(0, len(halves), 2):
        a = page(L, halves[i][0], halves[i][1], True, pol=True)
        b = page(L, halves[i + 1][0], halves[i + 1][1], True, pol=True) if i + 1 < len(halves) else ''
        sh.append(f'<div class="list">{a}<div class="rez"><span>✂</span></div>{b}</div>')
    return (f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>{html.escape(L["title"])}</title>'
            f'<style>{CSS}{POL_CSS}{extra_css}</style></head><body>' + ''.join(sh) + '</body></html>')
# ---------------- шпаргалка ----------------
SHP_CSS = '''
@page{size:A4;margin:9mm 9mm 8mm}
body{margin:0;font:19pt/1.22 "Liberation Serif","DejaVu Serif",serif;color:#1d1d1b;background:#fff}
.sh-hd{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1.6px solid #1d1d1b;padding-bottom:1mm;margin-bottom:3mm}
.sh-hd b{font-size:24pt}.sh-hd span{font-size:13pt}
h2{font-size:15pt;margin:4mm 0 1.5mm}h2.nov{break-before:page}
table{border-collapse:collapse;width:100%}
th{font-size:12pt;text-align:left;font-weight:700;border-bottom:1.2px solid #1d1d1b;padding:0 2mm 1mm}
td{padding:1mm 2mm;vertical-align:top;border-bottom:.5px solid #cfccc2}
td:first-child{font-weight:700;width:12mm;text-align:right;padding-right:4mm}
tr.cherta td{border-top:2.2px solid #1d1d1b}
'''
def shpargalka(title, date, sections):
    """ШПАРГАЛКА — ТОЛЬКО номер, вариант, ответ (А14, железно). sections = [(заголовок, шапка, строки, черты), ...]:
    строки — (номер, ответ А, ответ Б) или (номер, ответ); черты — номера, ПОСЛЕ которых проводится черта.
    Первая секция (листок) — на первой странице; остальные — со второй. Крупно: читается с телефона одним взглядом."""
    out = f'<div class="sh-hd"><b>{html.escape(title)}</b><span>{html.escape(date)}</span></div>'
    for k, (t, head, rows, br) in enumerate(sections):
        CH, NOV = ' class="cherta"', ' class="nov"'
        tr = ''.join(f'<tr{CH if i and rows[i - 1][0] in br else ""}>' + ''.join(f'<td>{html.escape(str(c))}</td>' for c in r) + '</tr>'
                     for i, r in enumerate(rows))
        out += f'<h2{NOV if k == 1 else ""}>{html.escape(t)}</h2><table><tr>{"".join(f"<th>{h}</th>" for h in head)}</tr>{tr}</table>'
    return f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>{html.escape(title)}</title><style>{SHP_CSS}</style></head><body>{out}</body></html>'
PODZHAT = """() => {
  const lines = el => { const r = document.createRange(); r.selectNodeContents(el);
    const ys = new Set([...r.getClientRects()].filter(q => q.width > 1).map(q => Math.round(q.top))); return ys.size; };
  document.querySelectorAll('.tx, .rules li, .ugol .t').forEach(el => {
    const n0 = lines(el); if (n0 < 2) return;
    for (const ls of [-0.008, -0.016, -0.025]) { el.style.letterSpacing = ls + 'em';
      if (lines(el) < n0) return; }
    el.style.letterSpacing = '';
  });
}"""
def to_pdf(html_paths):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 718, 'height': 1060})   # ширина = печатная колонка A4
        for h in html_paths:
            pg.goto('file://' + h); pg.wait_for_timeout(200); pg.emulate_media(media='print'); pg.evaluate(PODZHAT)
            pg.pdf(path=h[:-5] + '.pdf', format='A4', print_background=True, prefer_css_page_size=True)
        b.close()
def fit_report(html_path):
    """Сколько миллиметров колонка каждой страницы переливает за лист (>0 — обрезано). Печатный размер."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 718, 'height': 1060})
        pg.goto('file://' + html_path); pg.emulate_media(media='print'); pg.evaluate(PODZHAT)
        r = pg.evaluate('''()=>{const px=96/25.4;return [...document.querySelectorAll('.page')].map(p=>{
            const top=p.getBoundingClientRect().top; let mx=0;
            p.querySelectorAll('.z,.rules,.map,svg').forEach(e=>{if(!e.closest('.foot'))mx=Math.max(mx,e.getBoundingClientRect().bottom-top)});
            const f=p.querySelector('.foot'); const lim=f?(f.getBoundingClientRect().top-top-4):p.getBoundingClientRect().height;
            return Math.round((mx-lim)/px*10)/10})}''')
        b.close(); return r
