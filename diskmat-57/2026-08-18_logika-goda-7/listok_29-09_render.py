import json, html
e=html.escape
D=json.load(open('out/listok29.json')); G=json.load(open('kvest_graph.json'))
CSS='''
@page{size:A4;margin:11mm 12mm}
:root{--ink:#1d1d1b;--mute:#6b6a64;--line:#8a877d;--sh:#d9d6cc}
body{margin:0;font:12.3pt/1.32 "PT Serif",Georgia,serif;color:var(--ink);background:#fff}
.page{page-break-after:always;break-after:page}
.hd{display:flex;justify-content:space-between;align-items:baseline;border-bottom:2px solid var(--ink);padding-bottom:3px;margin-bottom:5px}
.hd b{font-size:17pt}.hd span{font-size:10pt;color:var(--mute)}
.fio{margin:3px 0 7px;font-size:11pt}.fio span{display:inline-block;width:62%;border-bottom:1px solid var(--ink)}
.z{display:grid;grid-template-columns:30px 1fr;gap:4px;margin:0 0 7px;break-inside:avoid}
.n{font-weight:700;font-size:12.5pt;white-space:nowrap}
.row{display:flex;gap:10px;align-items:flex-start}.row .tx{flex:1}
.pole{display:flex;align-items:center;gap:5px;margin:3px 0 0}.pl{width:14px;color:var(--mute);font-size:10pt}
.box{flex:1;height:22px;border:1px solid var(--ink)}.sig{width:38px;height:22px;border:1px solid var(--line)}
.tpl{flex:1;height:22px;border:1px solid var(--ink);display:flex;align-items:center;gap:3px;padding:0 5px}
.sq{display:inline-block;width:26px;height:15px;border:1px dashed var(--ink)}
.sl{display:inline-block;width:34px;height:14px;border-bottom:1.3px solid var(--ink);margin:0 3px}.tpl{font-size:13pt}
.sec{font-size:10pt;color:var(--mute);letter-spacing:.06em;text-transform:uppercase;margin:6px 0 4px;border-top:1px solid var(--line);padding-top:3px}
svg{display:block}.s-line{fill:none;stroke:var(--ink);stroke-width:1}.s-cell{fill:#fff;stroke:var(--line);stroke-width:.8}
.s-fillsh{fill:var(--sh);stroke:var(--ink);stroke-width:.8}.s-dash{stroke:var(--ink);stroke-dasharray:4 3;stroke-width:1.2;fill:none}
.s-thin{stroke:var(--ink);stroke-width:1.3;fill:none}.s-txt{font:11px "PT Sans",Arial,sans-serif;fill:var(--ink);text-anchor:middle;dominant-baseline:central}
.s-big{font:bold 17px "PT Sans",Arial,sans-serif;fill:var(--ink);text-anchor:middle;dominant-baseline:central}
.c{font-size:10.8pt;line-height:1.25}.c .box,.c .sig,.c .tpl{height:17px}.c .z{margin-bottom:4px}.c .pole{margin-top:2px}
.rules{font-size:12pt;margin:6px 0 0}.rules li{margin:2px 0}
table{border-collapse:collapse;width:100%;font-size:9.6pt}td,th{border:1px solid var(--line);padding:2px 4px;vertical-align:top;text-align:left}th{background:#eee}
'''
def grid(m,n,shade,cell=9,hole=None,extra=''):
    W=n*cell;H=m*cell;s=[]
    for r in range(m):
        for c in range(n):
            if shade(r,c): s.append(f'<rect x="{c*cell}" y="{r*cell}" width="{cell}" height="{cell}" class="s-fillsh"/>')
    return f'<svg viewBox="-2 -2 {W+4} {H+4}" width="{W+4}" height="{H+4}" role="img" aria-label="клетчатая фигура">{"".join(s)}{extra}</svg>'
def pic(p):
    if p[0]=='frame':
        n,k=p[1],p[2]; o=(n-k)//2
        return grid(n,n,lambda r,c: not (o<=r<o+k and o<=c<o+k),cell=8)
    if p[0]=='corner':
        a,b,c,w=p[1:]
        return grid(b,a,lambda r,cc: not (r<w and cc>=a-c),cell=10)
    if p[0]=='domino':
        L=2;n=L+4;cells=set()
        for (r0,c0) in ((0,0),(0,n-2),(n-2,0),(n-2,n-2)):
            for x in range(2):
                for y in range(2): cells.add((r0+x,c0+y))
        for c in range(2,n-2): cells.add((0,c)); cells.add((n-1,c))
        for r in range(2,n-2): cells.add((r,0)); cells.add((r,n-1))
        return grid(n,n,lambda r,c:(r,c) in cells,cell=14)
    if p[0]=='diag':
        return grid(10,10,lambda r,c:c>r,cell=7,extra='<line x1="0" y1="0" x2="70" y2="70" class="s-dash"/>')
def pole(l,tpl=False):
    sl='<span class="sl"></span>'
    inner=('<span class="tpl">'+sl+'·'+sl+' + '+sl+'·'+sl+'</span>') if tpl else '<span class="box"></span>'
    return f'<div class="pole"><span class="pl">{l}</span>{inner}<span class="sig"></span></div>'
def zad(z):
    ps_=z.get('pic',[])
    pics=('<div style="display:flex;gap:10px;align-items:flex-end">'+''.join(f'<div style="text-align:center">{pic(p)}<div style="font-size:9pt">{"аб"[i]}</div></div>' for i,p in enumerate(ps_))+'</div>') if len(ps_)>1 else ''.join(pic(p) for p in ps_)
    pl=''.join(pole(l, z.get('tpl')==l) for l,_ in z['p'])
    body=f'<div class="row"><div class="tx">{z["t"]}</div>{("<div>"+pics+"</div>") if pics else ""}</div>{pl}'
    return f'<div class="z"><div class="n">{z.get("m","◇")}{z["n"]}</div><div>{body}</div></div>'
def list_page(v):
    Z=D['V'][v]
    h=f'<div class="page"><div class="hd"><b>Комбинаторика 2 · таблицы и группы</b><span>29 сентября · 7И · вариант {v}</span></div><div class="fio">Фамилия, имя: <span></span></div>'
    h+=''.join(zad(z) for z in Z if z['m']=='○')+'<div class="sec">&nbsp;</div>'+''.join(zad(z) for z in Z if z['m']=='△')+'</div>'
    h+=f'<div class="page c"><div class="hd"><b>Ромбы</b><span>вариант {v} · ромбы в обоих вариантах одинаковые</span></div>'+''.join(zad(dict(z,m='◇')) for z in D['R'])+'</div>'
    return h
# ---------- карта ----------
NUM={r['rid']:r['n'] for r in D['R']}
def lab(c):  # 'R5в' -> '15в'
    return f"{NUM[c[:-1]]}{c[-1]}"
COLS=['R1','R7','R4','R6','R2','R5','R11','R8','R3']   # порядок столбцов: соседи по «мостам» рядом
def kmap():
    W,H=760,640; pos={}; s=[]
    for i,r in enumerate(COLS):
        x=50+i*82
        for j,l in enumerate('абв'):
            c=r+l
            if c in G['cells']: pos[c]=(x,400-j*95)
    pos['ЛАГЕРЬ']=(380,500); pos['ДРАКОН']=(430,70)
    for a,bs in G['adj'].items():
        for b in bs:
            if a<b and a in pos and b in pos: s.append(f'<line x1="{pos[a][0]}" y1="{pos[a][1]}" x2="{pos[b][0]}" y2="{pos[b][1]}" class="s-thin"/>')
    for c,(x,y) in pos.items():
        if c in G['cells']:
            s.append(f'<polygon points="{x},{y-20} {x+20},{y} {x},{y+20} {x-20},{y}" class="s-cell" style="stroke:#1d1d1b;stroke-width:1.2"/><text x="{x}" y="{y}" class="s-txt">{lab(c)}</text>')
    x,y=pos['ЛАГЕРЬ']; s.append(f'<polygon points="{x},{y-30} {x+42},{y+22} {x-42},{y+22}" class="s-fillsh"/><text x="{x}" y="{y+5}" class="s-big">4</text>')
    x,y=pos['ДРАКОН']; s.append(f'<path d="M{x-46},{y+20} L{x-30},{y-24} L{x-12},{y-2} L{x},{y-34} L{x+12},{y-2} L{x+30},{y-24} L{x+46},{y+20} Z" class="s-fillsh"/><text x="{x}" y="{y+5}" class="s-big">5</text>')
    # базовые дороги
    kr=[1,2,'2','3','3','3',4,5,'5']
    klab=['1','2а','2б','3а','3б','3в','4','5а','5б']
    for i,t in enumerate(klab):
        x=40+i*44; y=610
        s.append(f'<circle cx="{x}" cy="{y}" r="17" class="s-cell" style="stroke:#1d1d1b;stroke-width:1.2"/><text x="{x}" y="{y}" class="s-txt">{t}</text>')
        if i: s.append(f'<line x1="{x-27}" y1="{y}" x2="{x-17}" y2="{y}" class="s-thin"/>')
    s.append(f'<line x1="{40+8*44+17}" y1="610" x2="{380-30}" y2="{522}" class="s-thin"/>')
    for i,t in enumerate(['6','7','8']):
        x=720-i*62; y=610
        s.append(f'<polygon points="{x},{y-20} {x+19},{y+14} {x-19},{y+14}" class="s-cell" style="stroke:#1d1d1b;stroke-width:1.2"/><text x="{x}" y="{y+3}" class="s-txt">{t}</text>')
        if i: s.append(f'<line x1="{x+19}" y1="{y}" x2="{x+43}" y2="{y}" class="s-thin"/>')
    s.append(f'<line x1="{720-2*62-19}" y1="600" x2="{380+30}" y2="{522}" class="s-thin"/>')
    return f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="карта квеста: две дороги к лагерю, от лагеря тропы ромбов к дракону">{"".join(s)}</svg>'
def map_page(v):
    return f'''<div class="page"><div class="hd"><b>Карта</b><span>вариант {v} · закрашивай клетки сданных пунктов</span></div>{kmap()}
<ol class="rules"><li>Сдал пункт — закрась его клетку.</li>
<li>Закрасил все кружки или все треугольники — ты в лагере («4»), а дальше по ромбам ходишь только в клетку рядом с закрашенной.</li><li>Дошёл до дракона — «5».</li></ol></div>'''
def doc(title,body): return f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>'
for v in ('А','Б'):
    open(f'out/LISTOK-29-09-{"A" if v=="А" else "B"}.html','w').write(doc(f'Листок 29.09 {v}',list_page(v)+map_page(v)))
# ---------- шпаргалка ----------
rows=''
ZA={z['n']:z for z in D['V']['А']}; ZB={z['n']:z for z in D['V']['Б']}
for n in sorted(ZA):
    za,zb=ZA[n],ZB[n]
    for i,(l,a) in enumerate(za['p']):
        rows+=f"<tr><td>{za['m']}{n}{l}</td><td>{e(a)}</td><td>{e(zb['p'][i][1])}</td><td>{'<br>'.join('<b>'+e(x)+'</b> → '+e(y) for x,y in za['hint']) if i==0 else ''}</td></tr>"
for z in D['R']:
    for i,(l,a) in enumerate(z['p']):
        rows+=f"<tr><td>◇{z['n']}{l}</td><td colspan=2>{e(a)}</td><td>{'<br>'.join('<b>'+e(x)+'</b> → '+e(y) for x,y in z['hint']) if i==0 else ''}</td></tr>"
shp=f'''<div class="hd"><b>Шпаргалка принимающего</b><span>Комбинаторика 2 · 29.09 и 6.10 · 7И</span></div>
<p style="font-size:10pt;margin:2px 0 6px">Ответ — строка-выражение. Структура верна, ошибка в счёте — «плюс с точкой», ошибку обвести. Голое неверное число — минус, и сразу наводящий вопрос из правого столбца. В 2б, 3в — принимать и другое верное выражение.</p>
<table><tr><th>пункт</th><th>вариант А</th><th>вариант Б</th><th>частая ошибка → наводящий вопрос</th></tr>{rows}</table>'''
open('out/SHPARGALKA-29-09.html','w').write(doc('Шпаргалка 29.09',shp))
print('ok')
