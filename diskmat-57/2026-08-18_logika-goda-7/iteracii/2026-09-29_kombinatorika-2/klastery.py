# Устойчивость уровней по всем сдачам 15.09–29.09. Запуск из папки арки: python3 klastery.py
# Балл события → процентильный ранг ребёнка среди сдавших (0..1); итог — средний ранг и разброс.
import csv,json,re,statistics as st,collections,os
I='iteracii/2026-09-29_kombinatorika-2'
def nm(s): s=re.sub(r'\s*\(.*\)','',s).strip().replace('Федор','Фёдор'); return ' '.join(s.split()[:2])
def read_last(f,col=None):
    R={}
    for row in csv.reader(open(f,encoding='utf-8'),delimiter=';'):
        if not row: continue
        if 'фамилия' in row[0]: H=row; continue
        if re.match(r'^[ЛL]\d',row[0]): continue
        v=row[H.index(col)] if col else row[-1]
        try: R[nm(row[0])]=float(str(v).replace(',','.'))
        except: pass
    return R
E={}
E['15.09 логика']=read_last('SDACHA-15-09_logika.csv','зачтено')
E['15.09 обр.ход']=read_last('SDACHA-15-09_obratnyj-hod.csv','зачтено')
E['22.09 подсчёты']=read_last('SDACHA-22-09_podschety.csv')
E['22.09 инфогр.']=read_last('SDACHA-22-09_infografika.csv')
# 29.09 листок: ядро ○/△ по Р155 (закрыл △ — ○ засчитаны) + доп
L={}; H=None
for row in csv.reader(open(f'{I}/SDACHA.csv',encoding='utf-8'),delimiter=';'):
    if 'зачтено' in row: H=row; continue
    r=dict(zip(H,row)); ok=lambda k:r.get(k) in ('+','в')
    o=sum(ok(k) for k in ['1','2а','2б','2в','3а','3б','3в','4а','4б','5']); t=sum(ok(k) for k in '678')
    core=(10 if t==3 else o)+t; L[nm(r['фамилия_имя'])]=core+0.5*(int(r['зачтено'])-o-t)
E['29.09 листок']=L
K={'1':8,'2':14,'3':34,'4':22,'5':12}
def num(s):
    m=re.findall(r'\d+',str(s).split('|')[-1]); return int(m[-1]) if m else None
D={}
for l in open(f'{I}/RAZMETKA-DZ-k-29-09.jsonl'):
    r=json.loads(l); z=0
    for p in '12345':
        sp=(r.get('spisok') or {}).get(p); v=num(r['n'][p]) if p in r.get('n',{}) else None
        z+=(sp==K[p]) if (p in '45' and sp) else (v==K[p])
    D[r['imya']]=z
E['ДЗ к 29.09']=D
E['КР 29.09']={k:v[1].count('+') for k,v in json.load(open(f'{I}/OTSENKA-KR-29-09.json'))['deti'].items()}
spisok=[nm(l) for l in open('SPISOK-7I.txt') if l.strip() and not l.startswith('#')]
def ranks(d):
    xs=sorted(d.values()); n=len(xs)
    return {k:(sum(x<v for x in xs)+0.5*(sum(x==v for x in xs)-1))/(n-1) for k,v in d.items()}
RK={e:ranks(d) for e,d in E.items()}
print('событий',len(E),'| сдавших:',{e:len(d) for e,d in E.items()})
rows=[]
for x in spisok:
    rs=[RK[e][x] for e in E if x in RK[e]]
    if not rs: continue
    samo=[RK[e][x] for e in ('КР 29.09',) if x in RK[e]]
    rows.append((x,st.mean(rs),st.pstdev(rs) if len(rs)>1 else 0,len(rs),rs,samo))
rows.sort(key=lambda r:-r[1])
print('\nребёнок                     ср.ранг  разброс  n  | '+' '.join(f'{e[:11]:>11s}' for e in E))
for x,m,s,n,rs,_ in rows:
    cells=' '.join(f'{RK[e][x]:11.2f}' if x in RK[e] else f'{"—":>11s}' for e in E)
    print(f'{x:26s} {m:7.2f}  {s:7.2f}  {n}  | {cells}')
# согласие событий: корреляция рангов пар событий (Спирмен по общим детям)
def sp(a,b):
    c=[k for k in a if k in b]
    if len(c)<5: return None
    ra=ranks({k:a[k] for k in c}); rb=ranks({k:b[k] for k in c})
    ma,mb=st.mean(ra.values()),st.mean(rb.values())
    num_=sum((ra[k]-ma)*(rb[k]-mb) for k in c); den=(sum((ra[k]-ma)**2 for k in c)*sum((rb[k]-mb)**2 for k in c))**.5
    return round(num_/den,2) if den else None
print('\nСогласие событий (ранговая корреляция по общим детям):')
ev=list(E)
for i,a in enumerate(ev):
    print(f'{a[:14]:14s} '+' '.join(f'{(sp(E[a],E[b]) if b!=a else 1):>6}' for b in ev))

# Уровни по блоку «Комбинаторика» (22.09–29.09) без ДЗ: ДЗ не согласуется ни с одним событием (см. таблицу выше)
B=['22.09 подсчёты','22.09 инфогр.','29.09 листок','КР 29.09']
print('\nБлок комбинаторики без ДЗ (средний ранг по', ', '.join(B)+'):')
bl=[]
for x in spisok:
    rs=[RK[e][x] for e in B if x in RK[e]]
    if len(rs)>=2: bl.append((st.mean(rs),len(rs),x))
bl.sort(reverse=True)
prev=None
for m,n,x in bl:
    gap=f'   ← разрыв {prev-m:.2f}' if prev is not None and prev-m>=0.08 else ''
    print(f'  {m:5.2f} (n={n})  {x}{gap}'); prev=m
