# -*- coding: utf-8 -*-
"""КР 6.10: HTML → PDF (A4, одна страница на вариант) + ключ. python3 sobrat_kr.py"""
import asyncio, subprocess, json
def pl(n,a,b,c):
    return a if n%10==1 and n%100!=11 else (b if 2<=n%10<=4 and not 12<=n%100<=14 else c)
from playwright.async_api import async_playwright
P = {'А': dict(g=7, t=12, x3=3, a=17, b=52, tot=28, ch=9, fo=6, no=5, T=7, after='БКСК', before='КБКБ', top='белой', topL='Б',
               S=12, carp=71, inc=75, d1=6, d2=10, st='четырёх', S5=20),
     'Б': dict(g=6, t=15, x3=4, a=23, b=64, tot=30, ch=11, fo=7, no=4, T=8, after='БСБС', before='СБКБ', top='красной', topL='К',
               S=13, carp=74, inc=84, d1=4, d2=6, st='пяти', S5=21)}
MON = '''<svg viewBox="0 0 60 64" class="mon" role="img" aria-label="лохматое чудище с одним глазом"><path d="M8 58 Q4 30 14 18 L10 4 L20 14 Q30 8 40 14 L50 4 L46 18 Q56 30 52 58 L46 52 L40 60 L34 52 L28 60 L22 52 L16 60 L12 52 Z" fill="#fff" stroke="#111" stroke-width="2"/><circle cx="30" cy="30" r="9" fill="#fff" stroke="#111" stroke-width="2"/><circle cx="32" cy="31" r="3.6" fill="#111"/><path d="M20 45 Q30 51 40 45" fill="none" stroke="#111" stroke-width="2"/><path d="M24 45 l2 4 l2 -4 M33 46 l2 4 l2 -4" fill="#fff" stroke="#111" stroke-width="1.4"/></svg>'''
CSS = '''@page{size:A4;margin:7mm 10mm 6mm}*{box-sizing:border-box}body{font-family:"PT Serif","Liberation Serif",Georgia,serif;font-size:9.4pt;line-height:1.25;color:#111;margin:0}
.hd{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1.4px solid #111;padding-bottom:2px;margin-bottom:3px}
.hd b{font-size:12pt}.nm{font-size:9.6pt}.intro{font-size:8.8pt;margin:2px 0 4px;color:#222}
.z{margin:3px 0 0;break-inside:avoid}.z>.t{margin:0}.z b.n{font-family:"PT Sans",Arial,sans-serif}
.p{display:flex;gap:6px;align-items:flex-end;margin:2px 0 0 14px}.p .q{flex:1}
.ln{display:inline-block;border-bottom:1px solid #444;min-width:34mm;height:1.1em;vertical-align:bottom}
.ln.w{min-width:0;flex:1;display:block}.ln.s{min-width:16mm}
.row{display:flex;gap:10px;margin-left:14px}.row>div{flex:1}
table{border-collapse:collapse;margin:2px 0 0 14px;font-size:8.8pt}td,th{border:1px solid #555;padding:1px 4px;height:4.8mm;text-align:left;font-weight:400}th{background:#eee}
.sec{font-family:"PT Sans",Arial,sans-serif;font-weight:700;font-size:10.4pt;margin:5px 0 1px;border-top:1px solid #111;padding-top:2px}
.stop{display:flex;gap:8px;align-items:center;border:1.6px dashed #111;border-radius:4px;padding:3px 7px;margin:5px 0 2px}.mon{width:15mm;height:16mm;flex:none}
.stop ol{margin:0;padding-left:16px;font-size:8.8pt}.hint{font-style:italic;font-size:8.8pt;color:#333}'''
def page(V, p):
    L = lambda c='': f'<span class="ln {c}"></span>'
    h = f'''<div class="hd"><b>Спецмат 7И · Контрольная 6 октября · Вариант {V}</b><span class="nm">Имя, фамилия: <span class="ln" style="min-width:52mm"></span></span></div>
<div class="intro">Базовая часть — для всех. Часть «Вверх» — по желанию: можно сразу начать с неё, можно решить базовую часть и добавить задачи оттуда. Ответ пишите <b>выражением</b> — так, как считали; за арифметику не снижаем. Черновик — на обороте.</div>
<div class="z"><p class="t"><b class="n">1. Поезд.</b> Петя едет в {p['g']}-м вагоне, если считать от головы поезда, и в {p['t']}-м, если считать от хвоста. <span class="hint">Нарисуйте поезд схематично: голова, Петин вагон, хвост — и подпишите, сколько вагонов в каждом куске.</span></p>
<div class="row"><div>(а) Сколько вагонов в поезде? {L()}</div><div>(б) Вася едет в {p['x3']}-м вагоне от хвоста. Какой это вагон от головы? {L('s')}</div></div></div>
<div class="z"><p class="t"><b class="n">2. Числа от {p['a']} до {p['b']}</b> (оба включаются). <span class="hint">Запишите каждый ответ разностью: (сколько таких чисел от 1 до {p['b']}) − (сколько таких чисел от 1 до …).</span></p>
<div class="row"><div>(а) Сколько среди них чётных? {L('s')} − {L('s')} = {L('s')}</div><div>(б) Сколько из них делятся на 3? {L('s')} − {L('s')} = {L('s')}</div></div></div>
<div class="z"><p class="t"><b class="n">3. Кружки.</b> В классе {p['tot']} человек. {p['ch']} ходят только в шахматный кружок, {p['fo']} — только в футбольную секцию, {p['no']} никуда не ходят, остальные ходят и туда и туда. <span class="hint">Нарисуйте полосу из {p['tot']} человек и разрежьте её на куски, как далматинцев на уроке.</span></p>
<div class="row"><div>(а) Сколько человек ходят в футбольную секцию? {L()}</div><div>(б) Сколько ходят и туда, и туда? {L('s')}</div></div></div>
<div class="z"><p class="t"><b class="n">4. Разложения.</b> Число {p['T']} раскладываем в сумму слагаемых, каждое из которых 1, 2 или 3; порядок не важен (3+2+2 и 2+3+2 — одно разложение). <span class="hint">Пишите слагаемые по убыванию, по одной записи на разложение.</span></p>
<p class="t" style="margin-left:14px">(а) Заполните таблицу: в каждой строке — все разложения с данным числом троек.</p>
<table style="width:calc(100% - 14px)"><tr><th style="width:22mm">троек</th><th>разложения</th><th style="width:20mm">сколько</th></tr>{''.join(f'<tr><td>{r}</td><td></td><td></td></tr>' for r in ('2', '1', '0'))}</table>
<div class="p"><span class="q">(б) Сколько всего разложений? Ответ — суммой по строкам: {L()}</span></div></div>
<div class="z"><p class="t"><b class="n">5. Флаги по порядку.</b> Флаг состоит из четырёх горизонтальных полос, каждая белая (Б), красная (К) или синяя (С); соседние полосы разного цвета. Флаг записываем буквами сверху вниз. Все флаги выписаны в <b>словарном порядке</b>: сначала по верхней полосе (Б, потом К, потом С), при одинаковой верхней — по второй, и так далее. Начало списка: БКБК, БКБС, БКСБ, …</p>
<div class="row"><div>(а) Какой флаг идёт сразу после {p['after']}? {L('s')}</div><div>(б) Какой флаг стоит прямо перед {p['before']}? {L('s')}</div></div>
<div class="p"><span class="q">(в) Сколько флагов с {p['top']} верхней полосой? Объясните счётом или выпишите все: {L('w')}</span></div></div>
<div class="z"><p class="t"><b class="n">6. Ошибка Васи.</b> Набираем {p['S']} рублей монетами по 1, 2 и 5 рублей. Вася рассуждает: «Перебираю по числу пятёрок. Если на двушки и рубли осталось m рублей и в них помещается q двушек, то двушек можно взять от 0 до q — это q способов. Остаётся сложить».</p>
<div class="row"><div>(а) Сколько способов насчитает Вася? {L('s')}</div><div></div></div>
<div class="p"><span class="q">(б) В чём ошибка Васи? Объясните словами:</span></div><div class="p"><span class="ln w"></span></div><div class="p"><span class="ln w"></span></div>
<p class="t" style="margin-left:14px">(в) Сколько способов на самом деле? Заполните таблицу и сложите.</p>
<table><tr><th>пятёрок</th><th>осталось рублей</th><th>двушек: от 0 до …</th><th>способов</th></tr>{''.join(f'<tr><td>{f}</td><td></td><td></td><td></td></tr>' for f in range(p['S']//5+1))}<tr><td colspan="3" style="text-align:right">всего</td><td></td></tr></table></div>
<div class="stop">{MON}<div><b>СТОП! Самопроверка перед сдачей</b> (баллов не даёт, но спасает их):<ol><li>Ответ вида «от … до …» проверьте на маленьком случае: от 5 до 5 — одно число, а что даёт ваше выражение?</li><li>Перебор: по какому правилу вы выписывали? Нет ли одного предмета, записанного дважды? Не кончился ли ряд раньше времени?</li><li>Куски: не попал ли кто-то в два куска сразу?</li></ol></div></div>
<div class="sec">Вверх — по желанию</div>
<div class="z"><p class="t"><b class="n">В1.</b> Саша учится с понедельника по пятницу. Он приходит к началу первого урока и после последнего сразу идёт домой. На каждом уроке он съедает 1 карамельку, на каждой перемене между уроками — 2. За неделю в школе он съел {p['carp']} {'карамельку' if p['carp']%10==1 and p['carp']%100!=11 else 'карамельки'}. Сколько у Саши уроков в неделю? {L()}</p></div>
<div class="z"><p class="t"><b class="n">В2.</b> Стоит очередь. В каждый промежуток между соседями влез ещё один человек. Потом снова в каждый промежуток между соседями влезло по человеку. Всего очередь выросла на {p['inc']} {pl(p['inc'],'человека','человека','человек')}. Сколько людей было в очереди сначала? {L()}</p></div>
<div class="z"><p class="t"><b class="n">В3.</b> Сколько чисел от 1 до 1000 не делятся ни на {p['d1']}, ни на {p['d2']}? Ответ — выражением. {L()}</p></div>
<div class="z"><p class="t"><b class="n">В4.</b> Флаги из {p['st']} полос, цвета Б, К, С, соседние полосы разного цвета (как в задаче 5), и вдобавок верхняя и нижняя полосы тоже разного цвета. Сколько таких флагов? {L()}</p></div>
<div class="z"><p class="t"><b class="n">В5.</b> Сколькими способами можно набрать {p['S5']} {pl(p['S5'],'рубль','рубля','рублей')} монетами по 1, 2, 5 и 10 рублей? Сделайте таблицу: строки — сколько десяток и сколько пятёрок. {L()}</p></div>'''
    return f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>КР 6.10 вариант {V}</title><style>{CSS}</style></head><body>{h}</body></html>'
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for V, p in P.items():
            fn = f'KR-6-10-{"A" if V=="А" else "B"}'
            open(fn + '.html', 'w', encoding='utf-8').write(page(V, p))
            pg = await b.new_page(); await pg.goto('file:///mnt/user-data/outputs/kr610/' + fn + '.html')
            await pg.pdf(path=fn + '.pdf', format='A4', print_background=True, prefer_css_page_size=True)
            h = await pg.evaluate('document.body.scrollHeight'); print(V, 'высота px', h)
        await b.close()
asyncio.run(main())
for f in ('KR-6-10-A.pdf', 'KR-6-10-B.pdf'):
    out = subprocess.run(['python3', '-c', f'import pypdf;print(len(pypdf.PdfReader("{f}").pages))'], capture_output=True, text=True)
    print(f, 'страниц:', out.stdout.strip() or out.stderr[-200:])
