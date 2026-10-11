import json,html,re
D=json.load(open('otbor.json')); C={c['id']:c for c in D['C']}; F=D['F']; K=D['krug']; TR=D['tri']
exec(open('otbor.py').read().split("for c in C: c['idea']=MAP")[0].split("IDEI=")[1].join(["IDEI=",""]) if False else "")
IDEI={'T1':'прямоугольник клеток = умножение','T2':'таблица из цифр (разряды — оси)','T3':'±1 при построении (линии против клеток)','T4':'сумма нескольких таблиц разного размера','T5':'линия в таблице (одна сумма цифр)','V1':'дополнение: всё минус лишнее','V2':'включение-исключение: пересечение вычесть','S1':'разбиение на непересекающиеся группы','P1':'перебор в заданном порядке, один уровень','P2':'перебор в заданном порядке, два уровня'}
css=open('gen_html.py').read().split("css='''")[1].split("'''")[0]+'.ok{color:#2e7d32}.no{color:var(--acc);font-weight:700}.small{font-size:13px}td.c{text-align:center}'
e=html.escape
fk=list(next(iter(F.values())).keys())
rows=''
for i,c in C.items():
    role='○' if i in K else ('△' if i in TR else '—')
    rows+=f"<tr><td><b>{i}</b><br><span class=small>{role}</span></td><td class=small>{e(c['src'])}</td><td>{e(c['txt'])}</td><td class=small>{e(c['ans'])}</td><td class=small>{', '.join(c['idea'])}</td><td class=c>{c['pts']}</td><td class=c>{c['t'][0]}/{c['t'][1]}</td>"+''.join(f"<td class='c {'ok' if F[i][k] else 'no'}'>{'✓' if F[i][k] else '✗'}</td>" for k in fk)+f"<td class=small>{e(c['repeat'] or '')} {e(c['forb'] or '')}</td></tr>"
def sost(ids,mark):
    out=''
    for n,i in enumerate(sorted(ids,key=lambda i:C[i]['t'][0]),1):
        c=C[i]; out+=f"<div class=z><div class=n>{mark}{n}</div><div class=t>{e(c['txt'])}<br><span class=small><b>А:</b> {e(c['ans'])} · <b>Б:</b> {e(c['b'])} · идеи {', '.join(c['idea'])} · {c['pts']} п. · {c['t'][0]}/{c['t'][1]} мин · <i>{e(c['src'])}</i></span></div></div>"
    return out
idei=''.join(f"<tr><td>{k}</td><td>{v}</td><td class=small>{', '.join(i for i in K if k in C[i]['idea'])}</td><td class=small>{', '.join(i for i in TR if k in C[i]['idea'])}</td></tr>" for k,v in IDEI.items())
page=f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Отбор задач 29.09</title><style>{css}</style></head><body><main>
<h1>Отбор задач листка 29.09 — прогон метода</h1><p class="sub">«Комбинаторика 2. Таблицы и группы» · обязательная часть (кружки и треугольники) · метод — METOD-otbora-zadach.md · все ответы перебором (otbor.py)</p>
<h2>Состав, который дал метод</h2>
<div class="pair"><section class="sheet"><header><b>Кружки ○</b><span>{sum(C[i]['pts'] for i in K)} пунктов · {sum(C[i]['t'][0] for i in K)}/{sum(C[i]['t'][1] for i in K)} мин (подгот./медл., оценка)</span></header>{sost(K,'○')}</section>
<section class="sheet"><header><b>Треугольники △</b><span>{sum(C[i]['pts'] for i in TR)} пункта · {sum(C[i]['t'][0] for i in TR)}/{sum(C[i]['t'][1] for i in TR)} мин</span></header>{sost(TR,'△')}</section></div>
<h2>Покрытие идей</h2><table><tr><th>идея</th><th>что это</th><th>в кружках</th><th>в треугольниках</th></tr>{idei}</table>
<p class="note">Вершины ядра (Р180, Р182): T — таблица (новое), P — перебор в порядке (новое), S — сумма, V — дополнение и вкл.-искл. (старое). Цель кружков — идеи T1–T4, P1, P2, S1, V1; V2 — в треугольниках и в контрольной (К2б).</p>
<h2>Пул: все карточки и фильтры</h2><div style="overflow-x:auto"><table class=small><tr><th>id</th><th>источник</th><th>условие (А)</th><th>ответ-строка</th><th>идеи</th><th>п.</th><th>мин</th>{''.join(f'<th>{e(k)}</th>' for k in fk)}<th>флаги</th></tr>{rows}</table></div>
</main></body></html>'''
open('OTBOR-29-09.html','w').write(page); print('ok')
