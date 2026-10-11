# Симуляция баланса квеста 29.09 (Р187). ВСЕ вероятности и времена — допущения аналитика, не замер:
# после урока их надо заменить данными сдачи (Ф13), иначе симуляция ничего не доказывает.
import random, json, statistics as st
from collections import deque
KRUG=[('K16',1),('K09а',1),('K09б',1.5),('K08а',1.5),('K08б',1),('K08в',1.5),('K10',3),('K04а',2),('K04б',2)]  # (клетка, мин подготовленного)
TRI=[('K07',2),('K14',3),('K13',4)]
# ромбы: (клетка, трудность 1..3)
ROMB={'R1':[1,1,2],'R2':[1,2,2],'R3':[1,2],'R4':[1,2],'R5':[2,2,3],'R6':[1,2,3],'R7':[1,2],'R8':[2,3],'R11':[2,3]}
cells={f'{r}{"абв"[i]}':d for r,ds in ROMB.items() for i,d in enumerate(ds)}
adj={c:set() for c in cells}; adj['ЛАГЕРЬ']=set(); adj['ДРАКОН']=set()
def link(a,b): adj[a].add(b); adj[b].add(a)
for r,ds in ROMB.items():
    link('ЛАГЕРЬ',f'{r}а')
    for i in range(1,len(ds)): link(f'{r}{"абв"[i-1]}',f'{r}{"абв"[i]}')
CROSS=[('R1б','R7б'),('R2б','R5б'),('R4б','R6б'),('R3б','R8а'),('R11а','R5а')]   # тропы сходятся
DRAGON=['R2в','R4б','R6в','R8б','R1в']                                          # клетки у дракона
for a,b in CROSS: link(a,b)
for c in DRAGON: link(c,'ДРАКОН')
# pb — вероятность, что ребёнок вообще может взять пункт базы. КАЛИБРОВКА по 22.09: при 11 пунктах кружков
# доля закрывших маршрут = 0,3·0,99^11 + 0,5·0,96^11 + 0,2·0,88^11 ≈ 0,64 (факт 22.09: 14 из 23 = 0,61).
# На втором занятии застрявший пункт берётся с вероятностью HELP (помощь принимающих) — допущение.
HELP=0.5
TYPES={'сильный':dict(share=.3,speed=.8,pb=.99,pr={1:.8,2:.6,3:.4},budget=110),
       'средний':dict(share=.5,speed=1.0,pb=.96,pr={1:.6,2:.4,3:.2},budget=100),
       'слабый': dict(share=.2,speed=1.6,pb=.88,pr={1:.35,2:.2,3:.08},budget=95)}
RT={1:4,2:6,3:8}
def dist(frm):
    D={frm:0}; q=deque([frm])
    while q:
        u=q.popleft()
        for v in adj[u]:
            if v not in D: D[v]=D[u]+1; q.append(v)
    return D
DD=dist('ДРАКОН')
def kid(T,rng):
    t=0; route=KRUG if rng.random()<.8 or T['speed']>1.2 else TRI
    for c,m in route:                         # база: пункт либо «могу», либо застрял; на 2-м занятии — помощь
        t+=m*T['speed']*1.6
        if rng.random()>=T['pb'] and rng.random()>=HELP: return dict(base=False,rombi=0,dragon=False)
    done={'ЛАГЕРЬ'}; tried={}
    while t<T['budget']:
        front=[c for c in cells if c not in done and adj[c]&done and tried.get(c,0)<2]
        if not front: break
        c=min(front,key=lambda c:(DD.get(c,99),cells[c],rng.random()))
        t+=RT[cells[c]]*T['speed']; tried[c]=tried.get(c,0)+1
        if t>T['budget']: break
        if rng.random()<T['pr'][cells[c]]:
            done.add(c)
            if 'ДРАКОН' in adj[c]: return dict(base=True,rombi=len(done)-1,dragon=True)
    return dict(base=True,rombi=len(done)-1,dragon=False)
def run(N=25,R=400,seed=1):
    rng=random.Random(seed); B=[];Dr=[];Rm=[]
    for _ in range(R):
        res=[]
        for name,T in TYPES.items():
            for _ in range(round(N*T['share'])): res.append(kid(T,rng))
        B.append(sum(r['base'] for r in res)/len(res)); Dr.append(sum(r['dragon'] for r in res)/len(res)); Rm.append(st.mean(r['rombi'] for r in res))
    return st.mean(B),st.mean(Dr),st.mean(Rm)
import sys
if len(sys.argv)>1: DRAGON[:]=sys.argv[1].split(',')
for c in list(adj['ДРАКОН']): adj[c].discard('ДРАКОН')
adj['ДРАКОН']=set()
for c in DRAGON: link(c,'ДРАКОН')
DD=dist('ДРАКОН')
b,d,r=run(); print(DRAGON,f'база (4): {b:.0%} · дракон (5): {d:.0%} · ромб-пунктов в среднем: {r:.1f}')
print('кратчайший путь от лагеря до дракона:',dist('ЛАГЕРЬ')['ДРАКОН']-1,'пункта')
json.dump(dict(cells=cells,adj={k:sorted(v) for k,v in adj.items()},dragon=DRAGON,cross=CROSS),open('kvest_graph.json','w'),ensure_ascii=False)
