# Ромбы v3 (Р193): путь к дракону — 6 задач, ответвление — 2 (монета), звёздочки — за драконом; черепа — на счётных пунктах
import json, random, statistics as st
from collections import deque
exec(open('romby2.py').read().split("STAR=")[0])       # T (все задачи v2 с ответами), P179
TD={t[0]:t for t in T}
PATH=['klassy','kayuty','globus','robin','del235','uravn']; BRANCH=['otrezki','domino']; STARS=['orehi','samoopis','xo','poloska']
USE=PATH+BRANCH+STARS
ORDER={'А':['klassy','kayuty','otrezki','globus','domino','del235','robin','uravn','orehi','samoopis','xo','poloska'],
       'Б':['kayuty','klassy','globus','otrezki','del235','domino','uravn','robin','samoopis','orehi','poloska','xo']}
cid=lambda t,l: f'{t}:{l}'
first=lambda t: cid(t,TD[t][3][0][0]); last=lambda t: cid(t,TD[t][3][-1][0])
cells={cid(t,l):d for t in USE for l,_,d in TD[t][3]}
adj={c:set() for c in cells}; adj['L']=set(); adj['D']=set()
def link(a,b): adj[a].add(b); adj[b].add(a)
for t in USE:
    ps=TD[t][3]
    for i in range(1,len(ps)): link(cid(t,ps[i-1][0]),cid(t,ps[i][0]))
for t in ['klassy','kayuty','globus','otrezki','domino']: link('L',first(t))
for a,b in [('klassy','robin'),('kayuty','del235'),('robin','uravn'),('del235','uravn'),('globus','robin'),('domino','del235')]: link(last(a),first(b))
for t in ['uravn','del235']: link(last(t),'D')
for t in STARS: link('D',first(t))                     # сокровищница за драконом
SKULL=[cid('kayuty','б'),cid('uravn','б')]; COIN=[cid('otrezki','а')]
def dist(frm):
    D={frm:0}; q=deque([frm])
    while q:
        u=q.popleft()
        for v in adj[u]:
            if v not in D: D[v]=D[u]+1; q.append(v)
    return D
if __name__=='__main__':
    DD=dist('D')
    TYPES={'сильный':dict(share=.3,speed=.8,pb=.99,pr={1:.8,2:.6,3:.25},budget=110),
           'средний':dict(share=.5,speed=1.0,pb=.96,pr={1:.6,2:.4,3:.1},budget=100),
           'слабый': dict(share=.2,speed=1.6,pb=.88,pr={1:.35,2:.2,3:.03},budget=95)}
    RT={1:4,2:6,3:9}; HELP=.5; BASE=[1,1,1.5,1.5,1,1.5,3,2,2]
    def kid(Tp,rng,mult):
        t=0
        for m in BASE:
            t+=m*Tp['speed']*1.6
            if rng.random()>=Tp['pb'] and rng.random()>=HELP: return (False,False)
        done={'L'}; lives=1; dead=set(); tried={}
        while t<Tp['budget']:
            front=[c for c in cells if c not in done and c not in dead and adj[c]&done and DD.get(c,99)<99 and 'D' not in done and tried.get(c,0)<3]
            if not front: break
            c=min(front,key=lambda c:(DD[c],cells[c],rng.random()))
            t+=RT[cells[c]]*Tp['speed']
            if t>Tp['budget']: break
            tried[c]=tried.get(c,0)+1
            if rng.random()<Tp['pr'][cells[c]]*mult:
                done.add(c)
                if c in COIN: lives+=1
                if 'D' in adj[c]: return (True,True)
            elif c in SKULL:
                if lives: lives-=1
                else: dead.add(c)
        return (True,False)
    for mult in (0.7,1.0,1.3):
        rng=random.Random(3); B=[];Dr=[]
        for _ in range(300):
            res=[kid(Tp,rng,mult) for Tp in TYPES.values() for _ in range(round(25*Tp['share']))]
            B.append(sum(r[0] for r in res)/len(res)); Dr.append(sum(r[1] for r in res)/len(res))
        print(f'ромбы ×{mult}: база {st.mean(B):.0%} · дракон {st.mean(Dr):.0%}')
    print('путь лагерь→дракон:',dist('L')['D']-1,'пункта; клеток',len(cells),'; задач',len(USE))
    json.dump(dict(T=[TD[t] for t in USE],ORDER=ORDER,STARS=STARS,adj={k:sorted(v) for k,v in adj.items()},SKULL=SKULL,COIN=COIN),open('out/romby3.json','w'),ensure_ascii=False,indent=1)
