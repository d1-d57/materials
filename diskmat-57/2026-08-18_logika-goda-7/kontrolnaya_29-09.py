from itertools import combinations
import json,html
def tri(L):
    r=[(a,b,c) for a,b,c in combinations(sorted(L),3) if a+b>c]; by={}
    for a,b,c in r: by.setdefault(c,[]).append((a,b,c))
    return r,by
def sq(m,n): return [(m-k+1)*(n-k+1) for k in range(1,min(m,n)+1)]
V={'А':dict(f=87,l=214,N=500,p=7,q=11,m=3,n=6,L=[1,2,3,4,5,6,7]),
   'Б':dict(f=95,l=232,N=600,p=7,q=13,m=4,n=5,L=[1,2,4,5,6,7,8])}
K={}
for v,d in V.items():
    assert d['f']%2==1 and d['l']%2==0
    s=(d['l']-d['f']+1)//2
    A,B,AB=d['N']//d['p'],d['N']//d['q'],d['N']//(d['p']*d['q']); none=d['N']-A-B+AB
    assert none==sum(1 for x in range(1,d['N']+1) if x%d['p'] and x%d['q'])
    S=sq(d['m'],d['n']); r,by=tri(d['L']); top=max(d['L'])
    h,vv=d['m']*(d['n']-1),(d['m']-1)*d['n']
    K[v]=[('1',f"({d['l']} − {d['f']} + 1) : 2 = {s}"),('2а',f"{A} и {B}"),('2б',f"{d['N']} − {A} − {B} + {AB} = {none}"),
          ('3а'," + ".join(map(str,S))+f" = {sum(S)}"+"  ("+", ".join(f"{k+1}×{k+1}: {x}" for k,x in enumerate(S))+")"),
          ('3б',f"горизонтальных {d['m']}·{d['n']-1} = {h}, вертикальных {d['m']-1}·{d['n']} = {vv}; всего {h+vv}"),
          ('4а',f"{len(by[top])}: "+", ".join("–".join(map(str,t)) for t in sorted(by[top]))),
          ('4б'," + ".join(str(len(by[c])) for c in sorted(by))+f" = {len(r)}")]
    print(v,K[v])
def pole(l): return f'<div class="pole"><span class="pl">{l}</span><span class="box"></span><span class="sig"></span></div>'
def var(v):
    d=V[v]; L=", ".join(map(str,d['L'][:-1]))+f" и {d['L'][-1]}"; top=max(d['L'])
    return f'''<section class="sheet"><header><b>Контрольная</b><span>Комбинаторика · 29 сентября · 7И · вариант {v}</span></header>
<div class="fio">Фамилия, имя: <span></span></div>
<div class="z"><div class="n">1</div><div class="t">Из книги выпала пачка листов. Первая страница пачки имеет номер {d['f']}, последняя — номер {d['l']}. Сколько листов выпало?{pole('')}</div></div>
<div class="z"><div class="n">2</div><div class="t">Сколько чисел от 1 до {d['N']}<br>(а) делятся на {d['p']}? делятся на {d['q']}? (два числа)<br>(б) не делятся ни на {d['p']}, ни на {d['q']}?{pole('а')}{pole('б')}</div></div>
<div class="z"><div class="n">3</div><div class="t">Клетчатая доска {d['m']}&thinsp;×&thinsp;{d['n']} клеток.<br>(а) Сколько на ней квадратов любого размера, составленных из целых клеток? Напишите отдельно, сколько квадратов каждого размера.<br>(б) Сколько на ней прямоугольников 1&thinsp;×&thinsp;2 из двух клеток? Напишите отдельно, сколько горизонтальных и сколько вертикальных.{pole('а')}{pole('б')}</div></div>
<div class="z"><div class="n">4</div><div class="t">Есть семь палочек длиной {L} см. Из трёх палочек можно сложить треугольник, если сумма длин любых двух из них больше длины третьей.<br>(а) Выпишите все тройки палочек, из которых складывается треугольник и в которых самая длинная палочка — {top} см.<br>(б) Сколькими способами можно выбрать из этих семи палочек три так, чтобы сложился треугольник?{pole('а')}{pole('б')}</div></div></section>'''
def kl(v): return ''.join(f'<tr><td>{a}</td><td>{html.escape(b)}</td></tr>' for a,b in K[v])
css=open('gen_html.py').read().split("css='''")[1].split("'''")[0]
dz=open('gen_html.py').read().split("dz='''")[1].split("'''")[0].replace('ДЗ-1, 4, 5 в контрольную не идут — почему, в обосновании.','ДЗ-1, 4, 5 в контрольную не идут.').replace('(1в «книга» и 2в «ни на 3, ни на 5»)','(1в «книга» — без ловушки; 2в «ни на 3, ни на 5»)')
page=f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Контрольная 29.09</title><style>{css}</style></head><body><main>
<h1>Контрольная 29.09 — черновик v3</h1><p class="sub">Спецмат 7И · проверка ДЗ «Комбинаторика 1» · 20 минут · 4 задачи · 7 пунктов · форма ответа свободная (Р179)</p>
<h2>ДЗ, которое она проверяет</h2>{dz}
<h2>Два варианта</h2><div class="pair">{var("А")}{var("Б")}</div>
<h2>Ключ</h2><div class="pair"><table><tr><th>пункт</th><th>вариант А</th></tr>{kl("А")}</table><table><tr><th>пункт</th><th>вариант Б</th></tr>{kl("Б")}</table></div>
<p class="note">Ответы посчитаны перебором (kontrolnaya_29-09.py). Арифметическая ошибка при верной структуре — «плюс с точкой» (Р163).</p></main></body></html>'''
open('KONTROLNAYA-29-09.html','w').write(page)
