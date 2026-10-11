# Ромбы v5 (Р199): граф карты — ОРИЕНТИРОВАННЫЙ, всё вверх, у каждой клетки ровно один выход.
# Пять троп выходят из лагеря, сливаются как притоки: левая (Робин → уравнение), средняя (короли → уравнение),
# правая (домино/каюты → делимость). Коротких путей в обход нет: закончил цепочку — есть ровно одно «куда дальше».
import json, random, statistics as st
exec(open('romby4.py').read().split("PATH=")[0])          # T, TD, KINGS, kexpr (задачи v4 с ответами)
ORDER={'А':['klassy','kayuty','kings','globus','domino','del235','robin','uravn','orehi','samoopis','xo','poloska'],
       'Б':['kayuty','klassy','globus','kings','del235','domino','uravn','robin','samoopis','orehi','poloska','xo']}
STARS=['orehi','samoopis','xo','poloska']; ROUTE=['klassy','kayuty','kings','globus','domino','del235','robin','uravn']
cid=lambda t,l: f'{t}:{l}'
lets=lambda t:[p[0] for p in TD[t][3]]
first=lambda t: cid(t,lets(t)[0]); last=lambda t: cid(t,lets(t)[-1])
cells={cid(t,l):d for t in ROUTE for l,_,d in TD[t][3]}
OUT={}                                                    # ребро «откуда → куда», у каждой клетки ровно одно
def chain(t):
    ls=lets(t)
    for a,b in zip(ls,ls[1:]): OUT[cid(t,a)]=cid(t,b)
for t in ROUTE: chain(t)
ENTRY=['globus','klassy','kings','domino','kayuty']       # из лагеря
MERGE={'globus':'robin','klassy':'robin','robin':'uravn','kings':'uravn','domino':'del235','kayuty':'del235'}
for a,b in MERGE.items(): OUT[last(a)]=first(b)
OUT[last('uravn')]='PEAK'; OUT[last('del235')]='PEAK'
assert all(c in OUT for c in cells), [c for c in cells if c not in OUT]
IN={}
for a,b in OUT.items(): IN.setdefault(b,[]).append(a)
for t in ENTRY: IN.setdefault(first(t),[]).append('CAMP')
# Р201: ☠ на каждой дороге к вершине
SKULL=[cid('kayuty','б'),cid('uravn','б'),cid('kings','б'),cid('del235','а')]; COIN=[cid('kings','а'),cid('domino','а'),cid('kayuty','а'),cid('klassy','')]  # Р204: монет столько же, сколько ☠ (владелец 29.09)
def open_(c,done): return any(p in done for p in IN.get(c,[]))
if __name__=='__main__':
    import sys, pathlib
    _H=pathlib.Path(__file__).resolve().parent
    sys.path.insert(0,str(next(p/'mashina-listka' for p in _H.parents if (p/'mashina-listka').is_dir())))
    import kvest
    kvest.report(OUT, [first(t) for t in ENTRY], cells, SKULL, COIN)
    json.dump(dict(KINGS={v:[[n,kexpr(n)] for n in ns] for v,ns in KINGS.items()},T=[TD[t] for t in ROUTE+STARS],ORDER=ORDER,STARS=STARS,
                   OUT=OUT,ENTRY=ENTRY,SKULL=SKULL,COIN=COIN),open('out/romby5.json','w'),ensure_ascii=False,indent=1)
