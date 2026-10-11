"""Сравнение КР 29.09 и КР 6.10 у одних и тех же детей, по приёмам. Источники: OTSENKA-KR-29-09.json, svod_kr_6-10.py (V).
Соответствие приёмов (решение аналитика, оспоримо): «на единицу» 29.09 №1 ↔ 6.10 ○1а,○1б,○2а,○2б; «включения-исключения» 29.09 №2б ↔ 6.10 ○3а,○3б;
«организованный перебор» 29.09 №4а,№4б ↔ 6.10 ○4,○6в. 29.09 №2а (делимость) и №3 (квадраты) и 6.10 ○5,○6а,○6б — без пары, в сравнение не входят.
Дети, решавшие 6.10 только △ (○ пусто), исключены: у них нет данных по ○."""
import json, os, sys, importlib.util
H=os.path.dirname(os.path.abspath(__file__))
old=json.load(open(os.path.join(H,'../../2026-09-29_kombinatorika-2/OTSENKA-KR-29-09.json'),encoding='utf-8'))
po=old['punkty']; spec=importlib.util.spec_from_file_location('s',os.path.join(H,'svod_kr_6-10.py'))
src=open(os.path.join(H,'svod_kr_6-10.py'),encoding='utf-8').read(); V={}; exec(src.split('rows=')[0],{} ,g:={}); V=g['V']
P='1а 1б 2а 2б 3а 3б 4 5а 5б 5в 6а 6б 6в'.split()
M={'на единицу':(['1'],['1а','1б','2а','2б']),'включ.-искл.':(['2б'],['3а','3б']),'перебор':(['4а','4б'],['4','6в'])}
def norm(n): return n.replace('ё','е').replace('Петр','Пётр')
O={norm(k):v for k,v in old['deti'].items()}
oba=[k for k in V if set(V[k][1])!={'.'} and norm(k) in O]
print(f'детей в обеих КР (6.10 с ○): {len(oba)}; только в 6.10: {[k for k in V if norm(k) not in O]}')
for tema,(a,b) in M.items():
    s1=sum(O[norm(k)][1][po.index(p)]=='+' for k in oba for p in a); n1=len(oba)*len(a)
    s2=sum(V[k][1][P.index(p)]=='+' for k in oba for p in b); n2=len(oba)*len(b)
    print(f'{tema:14} 29.09: {s1}/{n1} = {s1/n1:.0%}   6.10: {s2}/{n2} = {s2/n2:.0%}')
print('по детям: доля + в 29.09 (7 пунктов) → доля + в ○ 6.10 (13 пунктов)')
r=[]
for k in oba:
    a=O[norm(k)][1].count('+')/7; b=V[k][1].count('+')/13; r.append((b-a,k,a,b))
for d,k,a,b in sorted(r): print(f'  {k:24} {a:4.0%} → {b:4.0%}  ({d:+.0%})')
up=sum(d>0.1 for d,*_ in r); dn=sum(d<-0.1 for d,*_ in r); print(f'выросли >10 п.п.: {up}, упали >10 п.п.: {dn}, без изменений: {len(r)-up-dn}')
