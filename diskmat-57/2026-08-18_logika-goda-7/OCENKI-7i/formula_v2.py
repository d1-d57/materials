"""Оценка за КР по навыкам: пункт несёт основной навык и вспомогательные (punkty.csv),
навык засчитан, если верно ≥ порога его пунктов (○ и, по флагу, △). «0»/отсутствие строки = не писал этот пункт.
Печатает только распределения — без имён."""
import os,csv,collections,itertools
DAN=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','sistema-7i','sistema','dannye')+os.sep
P=list(csv.DictReader(open(DAN+'punkty.csv'))); N=list(csv.DictReader(open(DAN+'nablyudeniya.csv')))
def navyki(p): return [p['navyk_osn']]+[s.strip() for s in p['navyki_vspom'].split(',') if s.strip()]
def ocenki(ev, ms, thr, s_tr=True, need5=None, need4=1):
    pts=[p for p in P if p['sobytie']==ev and (p['uroven']=='○' or s_tr)]
    sk=collections.defaultdict(list)
    for p in pts:
        for s in navyki(p):
            if s in ms: sk[s].append(p['punkt'])
    res=collections.defaultdict(dict)
    for n in N:
        if n['sobytie']==ev: res[n['rebyonok']][n['punkt']]=n['verdikt']
    c=collections.Counter(); pusto=0
    for ch,m in res.items():
        if not any(v=='+' for v in m.values()): pusto+=1; continue
        own=sum(1 for s,l in sk.items() if sum(m.get(x)=='+' for x in l)/len(l)>=thr)
        k=len(sk); n5=k if need5 is None else need5
        c[5 if own>=n5 else 4 if own>=need4 else 3]+=1
    return dict(sorted(c.items())), pusto, {s:len(l) for s,l in sk.items()}
for ev in ['KR-2026-09-29','KR-2026-10-06']:
    print('==',ev)
    for ms in (['1','2','3'],['1','2','3','5б']):
        for s_tr in (False,True):
            for thr in (.5,.6,2/3):
                for need4 in (1,2):
                    d,pusto,sz=ocenki(ev,ms,thr,s_tr,need4=need4)
                    print(f" навыки {','.join(ms):9} {'○+△' if s_tr else '○  '} порог {thr:.2f} «4»≥{need4}: {d}  без единого + (не писал?): {pusto}  пунктов на навык {sz}")
