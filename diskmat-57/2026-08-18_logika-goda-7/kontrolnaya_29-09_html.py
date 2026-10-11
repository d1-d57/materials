import json,html
D=json.load(open('kontr.json')); V,K=D['V'],D['K']
def pole(lbl,templ=None):
    inner = templ if templ else ''
    return f'<div class="pole"><span class="pl">{lbl}</span><span class="box">{inner}</span><span class="sig"></span></div>'
def box(): return '<span class="sq"></span>'
def var(v):
    d=V[v]; L=", ".join(map(str,d['L'][:-1]))+f" и {d['L'][-1]}"
    top=max(d['L']); lens=sorted(set(d['L'])-{1,2})
    t=f'''<section class="sheet"><header><b>Контрольная</b><span>Комбинаторика · 29 сентября · 7И · вариант {v}</span></header>
<div class="fio">Фамилия, имя: <span></span></div>
<div class="z"><div class="n">1</div><div class="t">Из книги выпала пачка листов. На первой выпавшей странице стоит номер {d['f']}, на последней — номер {d['l']}.<br>(а) Сколько страниц в выпавшей пачке? (б) Сколько в ней листов?
{pole('а')}{pole('б')}</div></div>
<div class="z"><div class="n">2</div><div class="t">Сколько чисел от 1 до {d['N']}<br>(а) делятся на {d['p']}? делятся на {d['q']}? (два числа)<br>(б) не делятся ни на {d['p']}, ни на {d['q']}?<br>(в) С какой вероятностью наугад выбранное число от 1 до {d['N']} не делится ни на {d['p']}, ни на {d['q']}? Ответ можно записать дробью.
{pole('а')}{pole('б')}{pole('в')}</div></div>
<div class="z"><div class="n">3</div><div class="t">Клетчатая доска {d['m']}&thinsp;×&thinsp;{d['n']} клеток.<br>(а) Сколько на ней квадратов любого размера, составленных из целых клеток?
{pole('а', box()+' + '+box()+' + '+box()+' = '+box())}
<span class="dop">(б) Сколько на ней прямоугольников 1&thinsp;×&thinsp;2 — лежащих и стоящих?</span>
{pole('б')}</div></div>
<div class="z"><div class="n">4</div><div class="t">Есть семь палочек длиной {L} см. Из трёх палочек можно сложить треугольник, если сумма длин любых двух из них больше длины третьей.<br>
(а) Выпишите все тройки, из которых складывается треугольник и в которых самая длинная палочка — {top} см. В тройке длины пишите по возрастанию; тройки — по возрастанию самой короткой палочки, а при равной — средней.<br>
(б) Сколькими способами можно выбрать из этих семи палочек три так, чтобы сложился треугольник? Ответ запишите суммой: сколько таких троек с каждой возможной самой длинной палочкой.
{pole('а')}{pole('б')}</div></div></section>'''
    return t
def kl(v):
    k=K[v]
    rows=[('1а',k['k1b'].split(' : ')[0].strip('()')+' = '+str(int(eval(k['k1b'].split(' : ')[0].replace('−','-'))))),('1б',str(int(eval(k['k1b'].split(' : ')[0].replace('−','-'))))+' : 2 = '+k['k1b'].split('= ')[-1]),('2а',k['k2a']),('2б',k['k2b']),('2в',k['k2c']),('3а',k['k3a']),('3б (доп.)',k['k3b']),('4а',k['k4a']),('4б',k['k4b'])]
    return ''.join(f'<tr><td>{a}</td><td>{html.escape(b)}</td></tr>' for a,b in rows)
css='''
:root{--bg:#f6f4ee;--paper:#fff;--ink:#1d1d1b;--mute:#6b6a64;--line:#c9c5b8;--acc:#8a2f1d}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#1b1b19;--paper:#262623;--ink:#ecebe6;--mute:#a4a29a;--line:#4a4944;--acc:#e0876f}}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.45 "PT Serif",Georgia,serif}
main{max-width:1180px;margin:0 auto;padding:24px 16px 60px}
h1{font-size:26px;margin:0 0 4px}h2{font-size:20px;margin:36px 0 10px;border-bottom:1px solid var(--line);padding-bottom:4px}
.sub{color:var(--mute);margin:0 0 18px}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px}@media(max-width:860px){.pair{grid-template-columns:1fr}}
.sheet{background:var(--paper);border:1px solid var(--line);padding:18px 20px}
.sheet header{display:flex;justify-content:space-between;align-items:baseline;border-bottom:2px solid var(--ink);padding-bottom:4px;margin-bottom:8px;gap:8px;flex-wrap:wrap}
.sheet header b{font-size:22px}.sheet header span{color:var(--mute);font-size:14px}
.fio{margin:6px 0 12px}.fio span{display:inline-block;width:60%;border-bottom:1px solid var(--ink)}
.z{display:grid;grid-template-columns:26px 1fr;gap:6px;margin:12px 0 16px}.n{font-weight:700;font-size:18px}
.pole{display:flex;align-items:center;gap:6px;margin:6px 0}.pl{width:18px;color:var(--mute)}
.box{flex:1;min-height:30px;border:1px solid var(--ink);display:flex;align-items:center;gap:4px;padding:0 6px;font-size:18px}
.sig{width:46px;height:30px;border:1px solid var(--line)}
.sq{display:inline-block;width:34px;height:22px;border:1px dashed var(--ink)}
.dop{display:block;margin-top:8px}
table{border-collapse:collapse;width:100%;background:var(--paper)}td,th{border:1px solid var(--line);padding:5px 8px;text-align:left;vertical-align:top}th{background:var(--bg)}
.note{color:var(--mute);font-size:14px}
.dz ol{margin:0;padding-left:22px}.dz li{margin:0 0 8px}
'''
dz='''<div class="sheet dz"><header><b>Домашнее задание 22.09</b><span>как выдано · Комбинаторика 1</span></header><ol>
<li>В классе 30 человек. Футболом занимаются 18 из них, шахматами — 15, а пятеро не занимаются ни тем, ни другим. Сколько человек занимаются и футболом, и шахматами? <i>— 8</i></li>
<li>Сколько всего квадратов можно найти на клетчатой доске 3×3 клетки? Считаются квадраты любого размера, составленные из целых клеток. <i>— 9 + 4 + 1 = 14</i> · <b>→ К3</b></li>
<li>Есть девять палочек длин 1, 2, 3, …, 9 см. Сколькими способами можно выбрать три палочки так, чтобы из них складывался треугольник? <i>— 34</i> · <b>→ К4</b></li>
<li>Выпишите все разложения числа 8 в сумму натуральных слагаемых (порядок не важен). Сколько их? <i>— 22</i></li>
<li>Нарисуйте все пентамино. Сколько их? <i>— 12</i></li></ol>
<p class="note">К1 и К2 — из листка 22.09 (1в «книга» и 2в «ни на 3, ни на 5»), разбирались у доски. ДЗ-1, 4, 5 в контрольную не идут — почему, в обосновании.</p></div>'''
page=f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Контрольная 29.09</title><style>{css}</style></head><body><main>
<h1>Контрольная 29.09 — черновик v2</h1><p class="sub">Спецмат 7И · проверка ДЗ «Комбинаторика 1» · 20 минут · 4 задачи · 8 оцениваемых пунктов + 1 дополнительный (3б)</p>
<h2>ДЗ, которое она проверяет</h2>{dz}
<h2>Два варианта</h2><div class="pair">{var("А")}{var("Б")}</div>
<p class="note">Пунктирные квадратики в 3а — шаблон выражения (Р169, Р178): структура «по размеру квадрата» здесь однозначна. В остальных полях — строка-выражение свободно.</p>
<h2>Ключ — ответ-строка</h2><div class="pair"><table><tr><th>пункт</th><th>вариант А</th></tr>{kl("А")}</table><table><tr><th>пункт</th><th>вариант Б</th></tr>{kl("Б")}</table></div>
<p class="note">Все ответы посчитаны перебором (kontr.py). Арифметическая ошибка при верной структуре — «плюс с точкой» (Р163).</p>
</main></body></html>'''
open('KONTROLNAYA-29-09.html','w').write(page); print(len(page))
