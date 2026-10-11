# Листок 29.09 v4 (Р196–Р197): формат 22.09 (узкая зона ответа слева), карта-восхождение справа на стр. 1,
# ромбы на стр. 2. Картинки — по Шеню: фигура штрихуется на клетчатом фоне.
import json, html, math
import numpy as np
from matplotlib import contour as _c
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
e=html.escape
L=json.load(open('out/listok4.json')); R=json.load(open('out/romby4.json'))
T={t[0]:t for t in R['T']}; ORDER=R['ORDER']; STARS=set(R['STARS']); SKULL=set(R['SKULL']); COIN=set(R['COIN'])
KINGS=R['KINGS']
CSS='''
@page{size:A4;margin:9mm 10mm 8mm}
:root{--ink:#1d1d1b;--mute:#6b6a64;--line:#8a877d;--sh:#d9d6cc;--grid:#cfccc2;--topo:#c9c6bb}
*{box-sizing:border-box}
body{margin:0;font:10.1pt/1.23 "Liberation Serif","DejaVu Serif",serif;color:var(--ink);background:#fff}
.page{page-break-after:always;break-after:page;height:279mm;overflow:hidden}
.hd{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1.6px solid var(--ink);padding-bottom:2px}
.hd b{font-size:15.5pt}.hd span{font-size:9.5pt;color:var(--mute)}
.fio{margin:4px 0 6px;font-size:10.5pt;display:flex;gap:6px}.fio span{flex:1;border-bottom:1px solid var(--ink)}
.p1{display:grid;grid-template-columns:1fr 63mm;gap:0 5mm}
.z{display:grid;grid-template-columns:44mm 1fr;gap:0 3.5mm;margin:0 0 2.2mm;break-inside:avoid}
.z.w{grid-template-columns:1fr}
.ab{border:1px solid var(--ink);align-self:start}
.ab .r{display:grid;grid-template-columns:4.2mm 1fr 8.5mm;height:6.6mm}
.ab .r+.r{border-top:1px solid var(--ink)}
.ab .l{font-size:8.5pt;padding:1px 0 0 1.2mm;color:var(--ink)}.ab .a{}.ab .s{border-left:1px solid var(--ink)}
.ab.one .r{grid-template-columns:1fr 8.5mm;height:8mm}
.tx .n{font-weight:700;white-space:nowrap}
.full{grid-column:1/-1;margin-top:1.6mm;display:grid;grid-template-columns:1fr 8.5mm;border:1px solid var(--ink)}
.full .s{border-left:1px solid var(--ink)}
.full .tp{display:flex;align-items:flex-end;justify-content:space-around;padding:0 4mm 1.6mm;font-size:13pt}
.full .tp .sl{flex:0 1 20mm;border-bottom:1.3px solid var(--ink);height:6mm}
.full .tp .op{padding:0 1.5mm}
.full .lb{font-size:8.5pt;padding:1px 0 0 1.2mm;position:absolute}
.pics{display:flex;gap:4mm;align-items:flex-end;margin-top:1.5mm}
.pics figure{margin:0;text-align:center;font-size:8.5pt}
svg{display:block}
.s-grid{stroke:var(--grid);stroke-width:.18}.s-fig{fill:url(#h)}.s-out{fill:none;stroke:var(--ink);stroke-width:.45;stroke-linecap:round}
.mapcol{display:flex;flex-direction:column}
.map svg{width:63mm}
.rules{font-size:9.4pt;line-height:1.24;margin-top:1.5mm;border-top:1px solid var(--ink);padding-top:1.2mm}
.rules p{margin:0 0 1.1mm}.rules b{font-size:9pt}
.m-topo{fill:none;stroke:var(--topo);stroke-width:.22}
.m-road{fill:none;stroke:#fff;stroke-width:1.9;stroke-linecap:round}
.m-edge{fill:none;stroke:var(--ink);stroke-width:.55;stroke-linecap:round}
.m-base{fill:none;stroke:var(--ink);stroke-width:.55;stroke-dasharray:1.2 .9;stroke-linecap:round}
.m-cell{fill:#fff;stroke:var(--ink);stroke-width:.45}
.m-star{fill:#fff;stroke:var(--ink);stroke-width:.4;stroke-dasharray:.9 .6}
.m-lab{font:bold 2.75px "Liberation Sans","DejaVu Sans",sans-serif;fill:var(--ink);text-anchor:middle;dominant-baseline:central}
.m-lab2{font:2.5px "Liberation Sans","DejaVu Sans",sans-serif;fill:var(--mute);text-anchor:middle;dominant-baseline:central}
.m-cp{fill:var(--ink)}.m-cpt{font:bold 2.9px "Liberation Sans",sans-serif;fill:#fff;text-anchor:middle;dominant-baseline:central}
.m-sk{font:3.6px "DejaVu Sans",sans-serif;fill:var(--ink);text-anchor:middle;dominant-baseline:central}
.m-coin{fill:#8a877d;stroke:var(--ink);stroke-width:.3}
.m-tent{fill:var(--sh);stroke:var(--ink);stroke-width:.45;stroke-linejoin:round}
.m-peak{fill:var(--sh);stroke:var(--ink);stroke-width:.45;stroke-linejoin:round}
.p2 .z{margin-bottom:3mm}
'''
HATCH='<defs><pattern id="h" patternUnits="userSpaceOnUse" width="1.1" height="1.1" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="1.1" stroke="#1d1d1b" stroke-width=".32"/></pattern></defs>'
# ---------- клетчатые картинки в стиле Шеня ----------
def shen(m,n,inside,cell=2.8,pid='h',margin=1):
    W=(n+2*margin)*cell; H=(m+2*margin)*cell; s=[]
    for i in range(n+2*margin+1): s.append(f'<line x1="{i*cell:.2f}" y1="0" x2="{i*cell:.2f}" y2="{H:.2f}" class="s-grid"/>')
    for j in range(m+2*margin+1): s.append(f'<line x1="0" y1="{j*cell:.2f}" x2="{W:.2f}" y2="{j*cell:.2f}" class="s-grid"/>')
    X=lambda c:(c+margin)*cell
    for r in range(m):
        for c in range(n):
            if inside(r,c): s.append(f'<rect x="{X(c):.2f}" y="{X(r):.2f}" width="{cell+.01:.2f}" height="{cell+.01:.2f}" fill="url(#{pid})"/>')
    for r in range(-1,m+1):
        for c in range(-1,n+1):
            a=0<=r<m and 0<=c<n and inside(r,c)
            b=0<=r<m and 0<=c+1<n and inside(r,c+1)
            if a!=b and 0<=r<m: s.append(f'<line x1="{X(c+1):.2f}" y1="{X(r):.2f}" x2="{X(c+1):.2f}" y2="{X(r+1):.2f}" class="s-out"/>')
            b=0<=r+1<m and 0<=c<n and inside(r+1,c)
            if a!=b and 0<=c<n: s.append(f'<line x1="{X(c):.2f}" y1="{X(r+1):.2f}" x2="{X(c+1):.2f}" y2="{X(r+1):.2f}" class="s-out"/>')
    defs=HATCH.replace('id="h"',f'id="{pid}"')
    return f'<svg viewBox="0 0 {W:.2f} {H:.2f}" style="width:{W:.2f}mm;height:{H:.2f}mm" role="img" aria-label="клетчатая фигура">{defs}{"".join(s)}</svg>'
def pic2(v):
    z=[z for z in L['V'][v] if z['n']==2][0]; (_,n,k),(_,a,b,c,w)=z['pic']
    cell=min(2.65,112/((n+2)+(a+2)+2))
    o_r,o_c=1,n-k-1                                  # дырка сдвинута к правому верхнему углу (Р197)
    f1=shen(n,n,lambda r,cc: not (o_r<=r<o_r+k and o_c<=cc<o_c+k),cell=cell,pid=f'h2a{v}')
    f2=shen(b,a,lambda r,cc: not (r<w and cc>=a-c),cell=cell,pid=f'h2b{v}')
    return f'<div class="pics"><figure>{f1}а</figure><figure>{f2}б</figure></div>'
def DOMINO179(v):
    S=set(); ring=lambda r0,c0:{(r0+a,c0+b) for a in range(3) for b in range(3)}-{(r0+1,c0+1)}
    for r0,c0 in ((0,0),(0,5),(5,0),(5,5)): S|=ring(r0,c0)
    for c in (3,4): S.add((1,c)); S.add((6,c))
    for r in (3,4): S.add((r,1)); S.add((r,6))
    return shen(8,8,lambda r,c:(r,c) in S,cell=3.2,pid=f'hd{v}')
# ---------- поля ответа ----------
def ab(labels):
    if labels==['']: return '<div class="ab one"><div class="r"><div class="a"></div><div class="s"></div></div></div>'
    return '<div class="ab">'+''.join(f'<div class="r"><div class="l">{l}</div><div class="a"></div><div class="s"></div></div>' for l in labels)+'</div>'
def full(h_mm=None,tpl=None,lab=''):
    if tpl:
        parts=''.join('<span class="sl"></span>' if x=='_' else f'<span class="op">{x}</span>' for x in tpl)
        return f'<div class="full" style="height:{h_mm or 9.5}mm;position:relative"><span class="lb">{lab}</span><div class="tp">{parts}</div><div class="s"></div></div>'
    return f'<div class="full" style="height:{h_mm}mm;position:relative"><span class="lb">{lab}</span><div></div><div class="s"></div></div>'
def task(mark,n,txt,labels,extra='',wide=None,after=''):
    import re
    txt=re.sub(r'\((а|б|в)\) ',r'(\1)&nbsp;',txt).replace(' = ','&nbsp;=&nbsp;').replace(' + ','&nbsp;+ ').replace('в левой','в&nbsp;левой').replace('в правой','в&nbsp;правой').replace(' и 2 меридиана',' и&nbsp;2&nbsp;меридиана')
    head=f'<span class="n">{mark}{n}.</span> '
    if wide is not None:                             # ответ во всю ширину под условием
        return f'<div class="z w"><div class="tx">{head}{txt}{extra}</div>{wide}{after}</div>'
    return f'<div class="z">{ab(labels)}<div class="tx">{head}{txt}{extra}</div>{after}</div>'
def krug(v):
    Z={z['n']:z for z in L['V'][v]}; out=[]
    z=Z[1]; out.append(task('○',1,z['t'],[''],wide=full(8.5)))
    z=Z[2]; out.append(task('○',2,z['t'],['а','б'],after='<div style="grid-column:1/-1">'+pic2(v)+'</div>'))
    z=Z[3]; out.append(task('○',3,z['t'],['а','б','в']))
    z=Z[4]; out.append(task('○',4,z['t'],['а'],after=full(tpl=['_','·','_','+','_','·','_','=','_'],lab='б')))
    z=Z[5]; out.append(task('○',5,z['t'],[''],wide=full(20)))
    return ''.join(out)
def treug(v):
    Z={z['n']:z for z in L['V'][v]}; out=[]
    out.append(task('△',6,Z[6]['t'],[''],wide=full(8.5)))
    out.append(task('△',7,Z[7]['t'],[''],wide=full(tpl=['_','+','_','+','_','=','_'])))
    out.append(task('△',8,Z[8]['t'],[''],wide=full(8.5)))
    return ''.join(out)
# ---------- карта: восхождение ----------
MW,MH=63.0,178.0
COLX=lambda i: 5.5+i*8.67
ROWY=lambda r: 7+(8.95-r)*13.6
def P(c,r): return (COLX(c),ROWY(r))
ROMB_POS={'globus':[(0,1.05),(0,2.05),(0.35,3.05)],'klassy':[(1.55,1.25)],'kings':[(3,1.2),(3,2.2)],
          'domino':[(4.45,1.25),(4.55,2.25)],'kayuty':[(6,1.05),(6,2.05)],
          'robin':[(1.65,3.45),(2.15,4.45)],'del235':[(4.55,3.45),(4.45,4.55)],'uravn':[(3,5.45),(3,6.45)]}
CAMP=(3,0); PEAK=(3,7.55)
STAR_POS=[(0.55,8.35),(2.2,8.75),(3.8,8.75),(5.45,8.35)]
KR=[(0.35,-2.85),(1.25,-2.55),(1.05,-1.75),(1.75,-1.2),(2.35,-0.55)]
TR=[(5.65,-2.8),(5.0,-1.95),(4.15,-1.05)]
def cells_of(t): return [l for l,_,_ in T[t][3]]
def num(v,t): return 9+ORDER[v].index(t)
def topo(seed):
    xs=np.linspace(0,MW,160); ys=np.linspace(0,MH,480); X,Y=np.meshgrid(xs,ys)
    px,py=P(*PEAK); cx,cy=P(*CAMP)
    F=1.25*np.exp(-(((X-px)/30)**2+((Y-py)/55)**2))
    rng=np.random.default_rng(seed)
    for _ in range(9):
        ax,ay=rng.uniform(0,MW),rng.uniform(py,cy+10); s=rng.uniform(6,14); h=rng.uniform(-.18,.22)
        F+=h*np.exp(-(((X-ax)/s)**2+((Y-ay)/s)**2))
    F+=.35*np.exp(-(((X-px)/9)**2+((Y-py)/12)**2))
    fig=plt.figure(); cs=plt.contour(X,Y,F,levels=np.linspace(.12,1.55,15)); plt.close(fig)
    out=[]
    for segs in cs.allsegs:
        for sg in segs:
            if len(sg)<8 or (np.ptp(sg[:,0])<14 and np.ptp(sg[:,1])<14): continue
            d='M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in sg[::2])
            out.append(f'<path d="{d}" class="m-topo"/>')
    return ''.join(out)
def curve(a,b,bend=0.0):
    (x1,y1),(x2,y2)=a,b; mx,my=(x1+x2)/2,(y1+y2)/2; dx,dy=x2-x1,y2-y1
    cx,cy=mx-dy*bend,my+dx*bend
    return f'M{x1:.2f},{y1:.2f} Q{cx:.2f},{cy:.2f} {x2:.2f},{y2:.2f}'
def diamond(x,y,r,cls): return f'<polygon points="{x:.2f},{y-r:.2f} {x+r:.2f},{y:.2f} {x:.2f},{y+r:.2f} {x-r:.2f},{y:.2f}" class="{cls}"/>'
def kmap(v):
    pos={}
    for t,ps in ROMB_POS.items():
        for l,p in zip(cells_of(t),ps): pos[f'{t}:{l}']=P(*p)
    E=[]  # (a,b,bend,style)
    first=lambda t: f'{t}:{cells_of(t)[0]}'; last=lambda t: f'{t}:{cells_of(t)[-1]}'
    for t in ROMB_POS:
        cs=cells_of(t)
        for i in range(1,len(cs)): E.append((pos[f'{t}:{cs[i-1]}'],pos[f'{t}:{cs[i]}'],0,'e'))
    camp=P(*CAMP); peak=P(*PEAK)
    for t,b in (('globus',.12),('klassy',.05),('kings',0),('domino',-.05),('kayuty',-.12)): E.append((camp,pos[first(t)],b,'e'))
    for a,b,bd in (('klassy','robin',0),('globus','robin',.1),('kings','robin',.08),('kayuty','del235',-.1),('domino','del235',-.03),('robin','uravn',.08),('del235','uravn',-.08)):
        E.append((pos[last(a)],pos[first(b)],bd,'e'))
    E.append((pos[last('uravn')],peak,0,'e')); E.append((pos[last('del235')],peak,.42,'e'))
    stars=[t for t in ORDER[v] if t in STARS]
    for t,sp in zip(stars,STAR_POS): pos[f'{t}:']=P(*sp); E.append((peak,pos[f'{t}:'],0,'e'))
    kr=[P(*p) for p in KR]; tr=[P(*p) for p in TR]
    base=[]
    for seq in (kr+[camp],tr+[camp]):
        for a,b in zip(seq,seq[1:]): base.append(curve(a,b,.1))
    s=[topo(7)]
    for a,b,bd,_ in E: s.append(f'<path d="{curve(a,b,bd)}" class="m-road"/>')
    for d in base: s.append(f'<path d="{d}" class="m-road"/>')
    for a,b,bd,_ in E: s.append(f'<path d="{curve(a,b,bd)}" class="m-edge"/>')
    for d in base: s.append(f'<path d="{d}" class="m-base"/>')
    # старты
    for (x,y),sym in ((kr[0],'○'),(tr[0],'△')):
        s.append(f'<path d="M{x-1.2:.2f},{y+7.4:.2f} L{x-1.2:.2f},{y+2.6:.2f} L{x+2.6:.2f},{y+3.6:.2f} L{x-1.2:.2f},{y+4.6:.2f}" class="m-tent"/>')
        s.append(f'<text x="{x+.6:.2f}" y="{y+9.3:.2f}" class="m-lab2">старт</text>')
    for i,(x,y) in enumerate(kr):
        s.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.5" class="m-cell"/><text x="{x:.2f}" y="{y+.1:.2f}" class="m-lab">{i+1}</text>')
    for i,(x,y) in enumerate(tr):
        s.append(f'<polygon points="{x:.2f},{y-2.9:.2f} {x+2.9:.2f},{y+2.1:.2f} {x-2.9:.2f},{y+2.1:.2f}" class="m-cell"/><text x="{x:.2f}" y="{y+.6:.2f}" class="m-lab">{i+6}</text>')
    # лагерь «4»
    x,y=camp
    s.append(f'<path d="M{x-5.2:.2f},{y+2.6:.2f} L{x:.2f},{y-4.2:.2f} L{x+5.2:.2f},{y+2.6:.2f} Z" class="m-tent"/><path d="M{x-1.2:.2f},{y+2.6:.2f} L{x:.2f},{y-.4:.2f} L{x+1.2:.2f},{y+2.6:.2f}" class="m-edge"/>')
    s.append(f'<circle cx="{x+6.4:.2f}" cy="{y-1.8:.2f}" r="2.1" class="m-cp"/><text x="{x+6.4:.2f}" y="{y-1.7:.2f}" class="m-cpt">4</text>')
    # ромбы
    for c,(x,y) in pos.items():
        t,l=c.split(':')
        if t in STARS:
            s.append(diamond(x,y,4.1,'m-star')+f'<text x="{x:.2f}" y="{y:.2f}" class="m-lab">{num(v,t)}</text>'); continue
        if c in SKULL or c in COIN:
            s.append(diamond(x,y,5.0,'m-cell')+f'<text x="{x:.2f}" y="{y-1.35:.2f}" class="m-lab">{num(v,t)}{l}</text>')
            if c in SKULL: s.append(f'<text x="{x:.2f}" y="{y+1.9:.2f}" class="m-sk">☠</text>')
            if c in COIN: s.append(f'<circle cx="{x:.2f}" cy="{y+1.9:.2f}" r="1.25" class="m-coin"/>')
        else:
            s.append(diamond(x,y,4.1,'m-cell')+f'<text x="{x:.2f}" y="{y:.2f}" class="m-lab">{num(v,t)}{l}</text>')
    # вершина «5»
    x,y=peak
    s.append(f'<path d="M{x-6.5:.2f},{y+3:.2f} L{x-2.6:.2f},{y-2.2:.2f} L{x-1.2:.2f},{y-.6:.2f} L{x+1.4:.2f},{y-4.6:.2f} L{x+6.5:.2f},{y+3:.2f} Z" class="m-peak"/>')
    s.append(f'<path d="M{x+1.4:.2f},{y-4.6:.2f} L{x+1.4:.2f},{y-9:.2f} L{x+4.6:.2f},{y-8.1:.2f} L{x+1.4:.2f},{y-7.2:.2f}" class="m-tent"/>')
    s.append(f'<circle cx="{x-8.6:.2f}" cy="{y+1.6:.2f}" r="2.1" class="m-cp"/><text x="{x-8.6:.2f}" y="{y+1.7:.2f}" class="m-cpt">5</text>')
    return f'<svg viewBox="0 0 {MW} {MH}" style="width:{MW}mm;height:{MH}mm" role="img" aria-label="карта-восхождение, вариант {v}">{"".join(s)}</svg>'
RULES='''<div class="rules">
<p><b>1.</b> Начни с любой тропы: ○ или △. Сдал задачу (все её пункты) — закрась её значок на карте.</p>
<p><b>2.</b> Закрасил одну тропу целиком — ты в лагере: оценка «4». Лагерь считается закрашенным. Дальше закрашивай ромбы: брать можно любой ромб, соединённый линией с закрашенным. Ромб «12в» — это пункт (в) задачи ◇12.</p>
<p><b>3.</b> Закрасил ромб, соединённый с вершиной, — оценка «5». За вершиной — звёздочки (пунктир).</p>
<p>Жизнь у тебя одна. Ромб с <span style="font-family:DejaVu Sans">☠</span> сдаётся с одной попытки: ошибся — жизнь сгорела; без жизни <span style="font-family:DejaVu Sans">☠</span> не сдать. Ромб с <span style="font-family:DejaVu Sans;color:#8a877d">●</span> — монета: сдал его — ещё одна жизнь. Остальные ромбы можно пересдавать.</p></div>'''
def page1(v):
    return (f'<div class="page"><div class="hd"><b>Комбинаторика 2 · таблицы и группы</b><span>29 сентября · 7И · вариант {v}</span></div>'
            f'<div class="fio">Фамилия, имя: <span></span></div><div class="p1"><div>{krug(v)}{treug(v)}</div>'
            f'<div class="mapcol"><div class="map">{kmap(v)}</div>{RULES}</div></div></div>')
def romb(v,t):
    _,_,txt,ps=T[t]; extra=''
    if t=='kings':
        a,b=KINGS[v][0][0],KINGS[v][1][0]
        txt=f"Сколькими способами можно поставить белого и чёрного королей так, чтобы они не били друг друга, на доску (а) {a}×{a}; (б) {b}×{b}?"
    if t=='domino': extra=f'<div class="pics">{DOMINO179(v)}</div>'
    mark='◇'+('⋆' if t in STARS else '')
    labels=[l for l,_,_ in ps]
    if t=='samoopis': return task(mark,num(v,t),txt,[''],wide=full(8.5))
    if t=='orehi': return task(mark,num(v,t),txt,[''],wide=full(8.5))
    return task(mark,num(v,t),txt,labels,extra=extra)
def page2(v):
    return (f'<div class="page p2"><div class="hd"><b>Ромбы</b><span>вариант {v} · ◇⋆ — звёздочки, за вершиной</span></div><div class="fio">Фамилия, имя: <span></span></div>'
            +''.join(romb(v,t) for t in ORDER[v])+'</div>')
def doc(title,body): return f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>'
if __name__=='__main__':
    for v,f in (('А','A'),('Б','B')): open(f'out/LISTOK-29-09-{f}-v4.html','w').write(doc(f'Листок 29.09 {v}',page1(v)+page2(v)))
    print('ok')
