# Свод контрольной 29.09 по RAZMETKA (jsonl от распознавателя). Ключ — SHPARGALKA-29-09.pdf.
import json,re,glob,sys,collections
K={'А':{'1':'64','2а':'71 45','2б':'390','3а':'32','3б':'27','4а':{'267','357','367','457','467','567'},'4б':'13'},
   'Б':{'1':'69','2а':'85 46','2б':'475','3а':'40','3б':'31','4а':{'278','458','468','478','568','578','678'},'4б':'14'}}
P=['1','2а','2б','3а','3б','4а','4б']
R=[json.loads(l) for f in sorted(glob.glob(sys.argv[1]+'/out/batch*.jsonl')) for l in open(f) if l.strip()]
R=[r for r in R if 'brak' not in r]
def last(s): m=re.findall(r'\d+',str(s).split('|')[-1]); return m[-1] if m else None
def ok(p,v,k):
    if v is None: return None
    s=str(v).split('|')[-1]
    if p=='4а': got=set(re.findall(r'\d{3}',s.replace(' ','').replace(',','')) or re.findall(r'\d+',s)); return got==k
    if p=='2а': return ' '.join(re.findall(r'\d+',s)[-2:])==k
    return last(s)==k
print('детей:',len(R),collections.Counter(r.get('var') for r in R)); C=collections.Counter(); A=collections.defaultdict(collections.Counter)
rows=[]
for r in R:
    k=K.get(r.get('var'));
    if not k: print('нет варианта:',r.get('imya')); continue
    s=''; n=0
    for p in P:
        v=r.get('n',{}).get(p); z=ok(p,v,k[p]); A[(r['var'],p)][v if p!='4а' else (r.get('spisok') or {}).get('4а')]+=1
        s+='·' if z is None else ('+' if z else '−'); n+=bool(z); C[p]+=bool(z)
    rows.append((r.get('imya') or '?? '+str(r.get('imya_kak_napisano')),r['var'],s,n,','.join(r.get('neuvereno',[]))))
for x in sorted(rows,key=lambda t:-t[3]): print(f'{x[0]:28s} {x[1]} {x[2]} {x[3]}/7  ?:{x[4]}')
print('верно по пунктам:',{p:f'{C[p]}/{len(rows)}' for p in P})
for key,c in sorted(A.items()): print(key,dict(c.most_common()))
