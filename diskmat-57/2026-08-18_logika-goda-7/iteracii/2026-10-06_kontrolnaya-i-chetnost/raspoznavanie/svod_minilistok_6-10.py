"""Свод мини-листка «Умный перебор △» 6.10. Ключ — out/SHPARGALKA-MINILISTOK-06-10.pdf (№3 перепроверен перебором ниже).
Вердикты — аналитик вручную по n и Р231/Р232/Р287; скрипт считает, сверяет плюсы принимающих (o) с вердиктом и печатает охват."""
import json, collections
from itertools import product
assert sum(1 for f in product('WRB',repeat=4) if all(a!=b for a,b in zip(f,f[1:])) and f.count('W')==1)==12  # №3, 4 полосы
assert sum(1 for f in product('WRB',repeat=3) if all(a!=b for a,b in zip(f,f[1:])) and f.count('W')==1)==8   # тот же вопрос для 3 полос
K={'А':['8','136','12','133','168','1611'],'Б':['10','126','12','200','105','806']}
V={'ls01':'++-++.','ls02':'++-+++','ls03':'++-+++',
   'ls04':'++-++-',   # 1 «4+3+1» = 8; 2 прочитано «186» — карандаш, 3/8 спутаны, по Р287 → 136
   'ls05':'++-++.','ls06':'++.-..','ls07':'++-+++'}
rows=[json.loads(l) for l in open('RAZMETKA-MINILISTOK-6-10.jsonl',encoding='utf-8') if l.strip()]
print(f'строк: {len(rows)}; с вердиктом: {sum(r["foto"][0][:4] in V for r in rows)} из {len(rows)}')
spor=0
for r in rows:
    v=V[r['foto'][0][:4]]
    s=[str(i+1) for i in range(6) if r['o'].get(str(i+1))=='+' and v[i]!='+']
    spor+=len(s)
    print(f"{(r['imya'] or 'без подписи'):22} {r['var']}  {v}  плюсов {v.count('+')} из 6" + (f'  ⚠ плюс принимающего при неверном: №{",".join(s)}' if s else ''))
print('по задачам:')
for i in range(6):
    c=collections.Counter(V[r['foto'][0][:4]][i] for r in rows)
    print(f'  {i+1}: +{c["+"]} −{c["-"]} .{c["."]}')
print(f'плюсов принимающих при неверном ответе: {spor}')
