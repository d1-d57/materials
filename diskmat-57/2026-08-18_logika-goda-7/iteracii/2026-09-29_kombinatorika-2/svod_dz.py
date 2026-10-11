# Правило владельца 05.10 (Р231): задачи «выпиши/нарисуй все» судятся ПО СПИСКУ: список полный — плюс и без числа;
# список неполный или с повторами — минус, даже если число верное (подозрение на списывание). Список не посчитан (null) — по числу.
# Старая формулировка: в пользу ребёнка — задачи 4/5 засчитаны и без числа, если выписано/нарисовано всё (spisok == ключ).
import json,re,glob,collections
K={'1':8,'2':14,'3':34,'4':22,'5':12}
R=[json.loads(l) for f in sorted(glob.glob(__import__('sys').argv[1]+'/out/batch*.jsonl')) for l in open(f) if l.strip()]
def num(s):
    m=re.findall(r'\d+',str(s).split('|')[-1]); return int(m[-1]) if m else None
fotos=sorted(x for r in R for x in r['foto']); print('фото в строках:',len(fotos),'уникальных:',len(set(fotos)),'детей(строк):',len(R))
cnt=collections.Counter(); ans=collections.defaultdict(collections.Counter); rows=[]
for r in R:
    z={};
    for p in '12345':
        v=num(r.get('n',{}).get(p)) if p in r.get('n',{}) else None
        ans[p][v]+=1; sp_=(r.get('spisok') or {}).get(p); z[p]=(sp_==K[p]) if (p in '45' and sp_ is not None and sp_>0) else (v==K[p]); cnt[p]+=z[p]
    sp=r.get('spisok',{})
    rows.append((r.get('imya') or '?? '+r.get('imya_kak_napisano',''),''.join('+' if z[p] else ('·' if p not in r.get('n',{}) else '−') for p in '12345'),sum(z.values()),sp.get('4'),sp.get('5'),','.join(r.get('neuvereno',[]))))
for x in sorted(rows,key=lambda t:-t[2]): print(f'{x[0]:28s} {x[1]}  {x[2]}/5  разл:{x[3]} пент:{x[4]}  ?:{x[5]}')
print('верно по задачам:',{p:f'{cnt[p]}/{len(R)}' for p in '12345'})
for p in '12345': print('задача',p,'ответы:',dict(ans[p].most_common()))
