import json, html
from collections import deque
src=open('render29.py').read()
exec(src.split("# ---------- карта ----------")[0])          # CSS, grid, pic, pole, zad, e, D (базовая часть)
R=json.load(open('out/romby2.json')); T={t[0]:t for t in R['T']}; ORDER=R['ORDER']; STAR=set(R['STAR']); adj=R['adj']; SKULL=set(R['SKULL'])
def DOMINO179():
    S=set()
    ring=lambda r0,c0:{(r0+a,c0+b) for a in range(3) for b in range(3)}-{(r0+1,c0+1)}
    for r0,c0 in ((0,0),(0,5),(5,0),(5,5)): S|=ring(r0,c0)
    for c in (3,4): S.add((1,c)); S.add((6,c))
    for r in (3,4): S.add((r,1)); S.add((r,6))
    return grid(8,8,lambda r,c:(r,c) in S,cell=13)
def num(v,t): return 9+ORDER[v].index(t)
def romb_zad(v,t):
    _,src_,txt,ps=T[t]; pics=''
    if t=='domino': pics=DOMINO179()
    if t=='otrezki': pics=pic(('diag',))
    pl=''.join(pole(l) for l,_,_ in ps)
    mark='◇'+('⋆' if t in STAR else '')
    return f'<div class="z" style="grid-template-columns:44px 1fr"><div class="n">{mark}{num(v,t)}</div><div><div class="row"><div class="tx">{txt}</div>{("<div>"+pics+"</div>") if pics else ""}</div>{pl}</div></div>'
def lab(v,c):
    t,l=c.split(':'); return f'{num(v,t)}{l}'
def kmap(v):
    W,H=760,560; dist={'L':0}; q=deque(['L'])
    while q:
        u=q.popleft()
        for w in adj[u]:
            if w not in dist and w!='D': dist[w]=dist[u]+1; q.append(w)
    layers={}
    for c,d in dist.items():
        if c!='L': layers.setdefault(d,[]).append(c)
    pos={'L':(380,500),'D':(380,40)}
    for d in sorted(layers):
        cs=layers[d]
        def bary(c):
            xs=[pos[w][0] for w in adj[c] if w in pos and w not in ('L','D')]
            return (sum(xs)/len(xs) if xs else 380, num(v,c.split(':')[0]))
        cs.sort(key=bary)
        n=len(cs); y=500-d*105
        for i,c in enumerate(cs): pos[c]=(60+(W-120)*(i+.5)/n,y)
    for _ in range(3):                      # пара проходов сверху вниз и снизу вверх
        for d in sorted(layers,reverse=True)+sorted(layers):
            cs=layers[d]
            cs.sort(key=lambda c: sum(pos[w][0] for w in adj[c] if w in pos and w not in ('L','D'))/max(1,len([w for w in adj[c] if w in pos and w not in ('L','D')])))
            n=len(cs); y=500-d*105
            for i,c in enumerate(cs): pos[c]=(60+(W-120)*(i+.5)/n,y)
    s=[]
    for a,bs in adj.items():
        for b in bs:
            if a<b and a in pos and b in pos: s.append(f'<line x1="{pos[a][0]:.0f}" y1="{pos[a][1]}" x2="{pos[b][0]:.0f}" y2="{pos[b][1]}" class="s-thin"/>')
    for c,(x,y) in pos.items():
        if c in ('L','D'): continue
        s.append(f'<polygon points="{x:.0f},{y-21} {x+21:.0f},{y} {x:.0f},{y+21} {x-21:.0f},{y}" class="s-cell" style="stroke:#1d1d1b;stroke-width:1.2"/><text x="{x:.0f}" y="{y}" class="s-txt">{lab(v,c)}</text>')
        if c in SKULL: s.append(f'<text x="{x+25:.0f}" y="{y-16}" class="s-txt" style="font-size:15px">☠</text>')
    x,y=pos['L']; s.append(f'<polygon points="{x},{y-30} {x+44},{y+24} {x-44},{y+24}" class="s-fillsh"/><text x="{x}" y="{y+6}" class="s-big">4</text>')
    x,y=pos['D']; s.append(f'<path d="M{x-50},{y+22} L{x-32},{y-22} L{x-13},{y} L{x},{y-32} L{x+13},{y} L{x+32},{y-22} L{x+50},{y+22} Z" class="s-fillsh"/><text x="{x}" y="{y+7}" class="s-big">5</text>')
    return f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="карта квеста, вариант {v}">{"".join(s)}</svg>'
def base_road():
    s=[]
    for i,t in enumerate(['1','2а','2б','3а','3б','3в','4','5а','5б']):
        x=30+i*44; s.append(f'<circle cx="{x}" cy="22" r="17" class="s-cell" style="stroke:#1d1d1b;stroke-width:1.2"/><text x="{x}" y="22" class="s-txt">{t}</text>')
    for i,t in enumerate(['6','7','8']):
        x=520+i*56; s.append(f'<polygon points="{x},2 {x+19},36 {x-19},36" class="s-cell" style="stroke:#1d1d1b;stroke-width:1.2"/><text x="{x}" y="25" class="s-txt">{t}</text>')
    return f'<svg viewBox="0 0 760 44" width="100%" role="img" aria-label="две дороги к лагерю: кружки и треугольники">{"".join(s)}</svg>'
def pages(v):
    Z=D['V'][v]
    h=f'<div class="page"><div class="hd"><b>Комбинаторика 2 · таблицы и группы</b><span>29 сентября · 7И · вариант {v}</span></div><div class="fio">Фамилия, имя: <span></span></div>'
    h+=''.join(zad(z) for z in Z if z['m']=='○')+'<div class="sec">&nbsp;</div>'+''.join(zad(z) for z in Z if z['m']=='△')+'</div>'
    o=ORDER[v]; half=7
    for part,ts in ((1,o[:half]),(2,o[half:])):
        h+=f'<div class="page c"><div class="hd"><b>Ромбы{"" if part==1 else " (продолжение)"}</b><span>вариант {v}</span></div>'+''.join(romb_zad(v,t) for t in ts)+'</div>'
    h+=f'''<div class="page"><div class="hd"><b>Карта</b><span>вариант {v}</span></div>
<div style="font-size:10pt;color:#6b6a64;margin:2px 0">Дорога кружков и дорога треугольников ведут в лагерь (закрашивай и их):</div>{base_road()}{kmap(v)}
<ol class="rules"><li>Сдал пункт — закрась его клетку.</li><li>Закрасил все кружки или все треугольники — ты в лагере («4»), а дальше по ромбам ходишь только в клетку рядом с закрашенной.</li><li>Дошёл до дракона — «5».</li></ol>
<p class="rules" style="margin-top:4px">☠ Клетку с черепом можно сдать только с первой попытки. &nbsp; <span style="display:inline-block;width:16px;height:16px;border:3px solid #1d1d1b;border-radius:50%;vertical-align:-3px"></span> Спасательный круг — один на листок: он отменяет один промах, зачеркни его, когда используешь.</p></div>'''
    return h
def doc(title,body): return f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>'
for v,f in (('А','A'),('Б','B')): open(f'out/LISTOK-29-09-{f}.html','w').write(doc(f'Листок 29.09 {v}',pages(v)))
# шпаргалка: база как было + ромбы с номерами А/Б
shp=open('out/SHPARGALKA-29-09.html').read()
import re
rows=''
for t in ORDER['А']:
    _,src_,txt,ps=T[t]
    for l,a,d in ps:
        rows+=f"<tr><td>◇{num('А',t)}{l}</td><td>◇{num('Б',t)}{l}</td><td>{e(a)}{' ☠' if f'{t}:{l}' in SKULL else ''}</td><td class=small>{e(src_)}</td></tr>"
rtab=f'<h3 style="margin:10px 0 4px">Ромбы — одинаковые задачи, в вариантах разный порядок (у доски не разбираются)</h3><table><tr><th>№ в А</th><th>№ в Б</th><th>ответ-строка (☠ — только с первой попытки)</th><th>источник</th></tr>{rows}</table>'
shp=re.sub(r'<tr><td>◇.*?</tr>','',shp,flags=re.S).replace('</table>','</table>'+rtab,1)
open('out/SHPARGALKA-29-09.html','w').write(shp); print('ok')
