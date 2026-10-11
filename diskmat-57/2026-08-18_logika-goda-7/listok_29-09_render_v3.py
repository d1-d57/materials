import json, html
from collections import deque
exec(open('render29.py').read().split("# ---------- карта ----------")[0])
R=json.load(open('out/romby3.json')); T={t[0]:t for t in R['T']}; ORDER=R['ORDER']; STARS=set(R['STARS']); adj=R['adj']; SKULL=set(R['SKULL']); COIN=set(R['COIN'])
exec(open('render2.py').read().split("def DOMINO179")[1].split("def num")[0].join(["def DOMINO179",""]))
def num(v,t): return 9+ORDER[v].index(t)
def inline_pole(l): return f'<span class="ip"><span class="pl">{l}</span><span class="box"></span><span class="sig"></span></span>'
def romb(v,t):
    _,src_,txt,ps=T[t]; pics=''
    if t=='domino': pics=DOMINO179()
    if t=='otrezki': pics=pic(('diag',))
    mark='◇'+('⋆' if t in STARS else '')
    return f'<div class="z" style="grid-template-columns:40px 1fr"><div class="n">{mark}{num(v,t)}</div><div><div class="row"><div class="tx">{txt}</div>{("<div>"+pics+"</div>") if pics else ""}</div><div class="ips">{"".join(inline_pole(l) for l,_,_ in ps)}</div></div></div>'
def lab(v,c): t,l=c.split(':'); return f'{num(v,t)}{l}'
def kmap(v):
    W,H=420,380; dist={'L':0}; q=deque(['L'])
    while q:
        u=q.popleft()
        for w in adj[u]:
            if w not in dist: dist[w]=dist[u]+1; q.append(w)
    dD=dist['D']; pos={'L':(W/2,H-24),'D':(W/2,64)}
    layers={}
    for c,d in dist.items():
        if c in ('L','D'): continue
        if c.split(':')[0] in STARS: continue
        layers.setdefault(d,[]).append(c)
    nL=max(layers); step=(H-24-64)/(nL+1)
    for d in sorted(layers):
        cs=layers[d]; y=H-24-d*step
        for i,c in enumerate(cs): pos[c]=(20+(W-40)*(i+.5)/len(cs),y)
    for _ in range(4):
        for d in sorted(layers)+sorted(layers,reverse=True):
            cs=layers[d]; y=H-24-d*step
            nb=lambda c:[pos[w][0] for w in adj[c] if w in pos and w not in ('L','D')]
            cs.sort(key=lambda c:(sum(nb(c))/len(nb(c)) if nb(c) else W/2))
            for i,c in enumerate(cs): pos[c]=(20+(W-40)*(i+.5)/len(cs),y)
    st=[t for t in ORDER[v] if t in STARS]
    for i,t in enumerate(st): pos[f'{t}:']=(W/2+(i-1.5)*70,18)
    s=[]
    for a,bs in adj.items():
        for b in bs:
            if a<b and a in pos and b in pos: s.append(f'<line x1="{pos[a][0]:.0f}" y1="{pos[a][1]:.0f}" x2="{pos[b][0]:.0f}" y2="{pos[b][1]:.0f}" class="s-thin"/>')
    for c,(x,y) in pos.items():
        if c in ('L','D'): continue
        t=c.split(':')[0]; r=15
        s.append(f'<polygon points="{x:.0f},{y-r:.0f} {x+r:.0f},{y:.0f} {x:.0f},{y+r:.0f} {x-r:.0f},{y:.0f}" class="s-cell" style="stroke:#1d1d1b;stroke-width:1.1{";stroke-dasharray:3 2" if t in STARS else ""}"/><text x="{x:.0f}" y="{y:.0f}" class="s-txt" style="font-size:9.5px">{lab(v,c)}</text>')
        if c in SKULL: s.append(f'<text x="{x+17:.0f}" y="{y-12:.0f}" class="s-txt" style="font-size:12px">☠</text>')
        if c in COIN: s.append(f'<circle cx="{x+18:.0f}" cy="{y-12:.0f}" r="5" class="s-fillsh"/>')
    x,y=pos['L']; s.append(f'<polygon points="{x:.0f},{y-22:.0f} {x+32:.0f},{y+16:.0f} {x-32:.0f},{y+16:.0f}" class="s-fillsh"/><text x="{x:.0f}" y="{y+4:.0f}" class="s-big" style="font-size:14px">4</text>')
    x,y=pos['D']; s.append(f'<path d="M{x-38:.0f},{y+16:.0f} L{x-25:.0f},{y-16:.0f} L{x-10:.0f},{y:.0f} L{x:.0f},{y-24:.0f} L{x+10:.0f},{y:.0f} L{x+25:.0f},{y-16:.0f} L{x+38:.0f},{y+16:.0f} Z" class="s-fillsh"/><text x="{x:.0f}" y="{y+5:.0f}" class="s-big" style="font-size:14px">5</text>')
    return f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="карта квеста, вариант {v}">{"".join(s)}</svg>'
def page1(v):
    Z=D['V'][v]
    mp=f'''<div class="mapbox"><div class="mt">Карта</div>{kmap(v)}
<ol class="rl"><li>Сдал пункт — закрась клетку.</li><li>Все кружки или все треугольники — ты в лагере («4»); дальше по ромбам — только в клетку рядом с закрашенной.</li><li>Дошёл до дракона — «5». За драконом — звёздочки.</li></ol>
<div class="rl2">♥ У тебя одна жизнь. ☠ Неверный ответ на черепе сжигает жизнь; без жизни череп не сдать. ● Монета даёт ещё одну жизнь.</div></div>'''
    K=[z for z in Z if z['m']=='○']; Tr=[z for z in Z if z['m']=='△']
    zz=lambda z: zad(z).replace('class="box"','class="box" style="height:50px"') if z['n']==4 else zad(z)
    body=''.join(zz(z) for z in K[:3])+mp+''.join(zz(z) for z in K[3:])+'<div class="sec">&nbsp;</div>'+''.join(zad(z) for z in Tr)
    return f'<div class="page p1"><div class="hd"><b>Комбинаторика 2 · таблицы и группы</b><span>29 сентября · 7И · вариант {v}</span></div><div class="fio">Фамилия, имя: <span></span></div>{body}</div>'
def page2(v):
    return f'<div class="page c"><div class="hd"><b>Ромбы</b><span>вариант {v} · ◇⋆ — звёздочки, за драконом</span></div>'+''.join(romb(v,t) for t in ORDER[v])+'</div>'
X='''.p1{position:relative;font-size:11.3pt;line-height:1.27}.p1 .z{margin-bottom:5px}
.mapbox{float:right;width:74mm;margin:2px 0 4px 8px;border:1px solid #8a877d;padding:3px 5px;background:#fff}
.mt{font-weight:700;font-size:11pt}.rl{font-size:8.6pt;margin:2px 0 0;padding-left:15px;line-height:1.2}.rl li{margin:0}.rl2{font-size:8.6pt;line-height:1.2;margin-top:2px}
.ips{display:flex;flex-wrap:wrap;gap:4px 10px;margin-top:2px}.ip{display:flex;align-items:center;gap:4px;flex:1 1 30%;min-width:52mm}.ip .box{flex:1;height:17px;border:1px solid #1d1d1b}.ip .sig{width:30px;height:17px;border:1px solid #8a877d}
.c{font-size:10.4pt;line-height:1.22}.c .z{margin-bottom:5px}'''
def doc(title,body): return f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}{X}</style></head><body>{body}</body></html>'
for v,f in (('А','A'),('Б','B')): open(f'out/LISTOK-29-09-{f}.html','w').write(doc(f'Листок 29.09 {v}',page1(v)+page2(v)))
print('ok')
