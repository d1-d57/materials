import os
DAN=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','sistema-7i','sistema','dannye')+os.sep
import csv,collections
P=[r for r in csv.DictReader(open(DAN+'punkty.csv'))]
N=[r for r in csv.DictReader(open(DAN+'nablyudeniya.csv'))]
D={r['id'] for r in csv.DictReader(open(DAN+'deti.csv')) if r['aktiven']=='1'}
def run(ev, minskills, thr_skill=2/3):
    pts=[p for p in P if p['sobytie']==ev and p['uroven']=='○']
    sk={}
    for p in pts: sk.setdefault(p['navyk_osn'],[]).append(p['punkt'])
    res=collections.defaultdict(dict)
    for n in N:
        if n['sobytie']==ev: res[n['rebyonok']][n['punkt']]=n['verdikt']
    out={}
    for ch,m in res.items():
        tot=sum(1 for p in pts if m.get(p['punkt'])=='+')
        share=tot/len(pts)
        v1=5 if share>=.85 else 4 if share>=.6 else 3
        own=[s for s in minskills if s in sk and sum(m.get(x)=='+' for x in sk[s])/len(sk[s])>=thr_skill]
        k=len([s for s in minskills if s in sk])
        v2=5 if len(own)==k else 4 if len(own)>=k/2 else 3
        out[ch]=(v1,v2,share)
    return out,sk,len(pts)
for ev in ['KR-2026-09-29','KR-2026-10-06']:
    for label,ms in [('навыки 1,2,3 (без 5б)',['1','2','3']),('навыки 1,2,3,5б',['1','2','3','5б'])]:
        o,sk,np=run(ev,ms)
        c1=collections.Counter(v[0] for v in o.values()); c2=collections.Counter(v[1] for v in o.values())
        print(ev,'| писали',len(o),'| ○-пунктов',np,'| пункты по навыкам',{k:len(v) for k,v in sk.items()})
        print('  V1 доля ○ (5≥85%,4≥60%):',dict(sorted(c1.items())))
        print('  V2',label,'(навык=≥2/3 его пунктов; 5=все, 4=≥половины):',dict(sorted(c2.items())))
print('--- доп. варианты ---')
for ev in ['KR-2026-09-29','KR-2026-10-06']:
    for thr in [1/2, 2/3]:
        for rule in ['5=все,4=≥1','5=все,4=≥половины']:
            o,sk,np=run(ev,['1','2','3'],thr)
            # recompute v2 with rule
            res=collections.defaultdict(dict)
            for n in N:
                if n['sobytie']==ev: res[n['rebyonok']][n['punkt']]=n['verdikt']
            ms=[s for s in ['1','2','3'] if s in sk]
            c=collections.Counter()
            for ch,m in res.items():
                own=[s for s in ms if sum(m.get(x)=='+' for x in sk[s])/len(sk[s])>=thr]
                if len(own)==len(ms): g=5
                elif (rule.endswith('≥1') and len(own)>=1) or (len(own)>=len(ms)/2): g=4
                else: g=3
                c[g]+=1
            print(ev,f'навык≥{thr:.2f}',rule,dict(sorted(c.items())))
# доли ○ по детям — гистограмма
for ev in ['KR-2026-09-29','KR-2026-10-06']:
    o,_,np=run(ev,['1'])
    h=collections.Counter(round(v[2]*np) for v in o.values())
    print(ev,'число верных ○-пунктов из',np,':',dict(sorted(h.items())))
# ДЗ: одна оценка за месяц
dz=collections.defaultdict(lambda:[0,0])
for n in N:
    if n['sobytie'].startswith('DZ'):
        dz[n['rebyonok']][1]+=1; dz[n['rebyonok']][0]+= n['verdikt']=='+'
sh=[a/b for a,b in dz.values()]
print('ДЗ: сдавали',len(dz),'из',len(D),'; доля + по детям: ≥.8:',sum(s>=.8 for s in sh),' .6–.8:',sum(.6<=s<.8 for s in sh),' <.6:',sum(s<.6 for s in sh))
