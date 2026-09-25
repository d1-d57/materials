# -*- coding: utf-8 -*-
"""Генератор HTML-каталога пула задач. Источник — /tmp/pul.json (собирает katalog.py).
ВЫХОД KATALOG-pula-22-09.html руками не правится: правь этот файл и пересобирай."""
import json, re, html, io

P = json.load(open('/tmp/pul.json', encoding='utf-8'))

SRC = {
 'shen':('Шень','«Комбинаторика», 8 листков, маткласс онлайн'),
 'raskina-1':('Раскина–Шаповалов 20','«Комбинаторика», ШМК вып. 20, МЦНМО 2024'),
 'raskina-2':('Раскина–Шаповалов 24','«Комбинаторика: заседание продолжается», вып. 24'),
 'trudnye':('Шаповалов / Канель-Белов','«Конструкции» + «Как решают нестандартные задачи»'),
 'matshkola':('Матшкола 5–6','выездная школа, М. Корсаков'),
 'nlogn-manzhina':('NLOGN / Манжина','зимний интенсив 6–7 кл. + летняя школа 6 кл.'),
 'bank-babicheva':('Банк / Бабичева','банк задач проекта + «Олимпиадная математика» А1'),
 'ksenia-1':('Ксения · МЦНМО 15','листки от Ксении: МЦНМО 6 зан. 15, МММФ-4'),
 'ksenia-2':('Ксения · МЦНМО 16/23','листки от Ксении: перестановки и сочетания'),
 '8klass':('Наш 8 класс','листки 02 «Правило суммы и произведения», 04 «Ещё раз»'),
}

# --- что аналитик предлагает в листок: (источник, кусок id) ---
PREDLOZHENIE = {
 'КРУЖОК':[('shen','Листок 1, задача 1'),('shen','Листок 1, задача 3'),('shen','Листок 1, задача 16'),
           ('raskina-1','1.1'),('bank-babicheva','7.6.14'),('raskina-1','Д89')],
 'ТРЕУГОЛЬНИК':[('nlogn-manzhina','короли'),('nlogn-manzhina','гирлянда'),('shen','Листок 5, задача 22'),
           ('nlogn-manzhina','kombinatorika.docx, задача 11'),('matshkola','5_chetnost-i-raskraski_listok.tex, задача 3')],
 'РОМБ':[('nlogn-manzhina','красные плитки'),('nlogn-manzhina','уголки'),('bank-babicheva','5.9.5'),
           ('shen','Листок 3, задача 12'),('bank-babicheva','avtobiograficheskoe-chislo'),
           ('matshkola','4.2_ocenka-i-primer_listok.tex, задача 6'),('shen','Листок 4, задача 13')],
 'ГРОБ':[('trudnye','A4'),('trudnye','A11'),('matshkola','4.2_ocenka-i-primer_listok.tex, задача 7')],
}
def predlagaem(c):
    # (?![0-9]) — иначе «Листок 1, задача 1» ловит и «задачу 10», а «1.1» ловит «1.10».
    # Ловушка поймана сверкой числа совпадений: было 28 попаданий вместо 21.
    for tip, lst in PREDLOZHENIE.items():
        for s, frag in lst:
            if c['src'] != s: continue
            if re.search(re.escape(frag) + r'(?![0-9])', c['id'], re.I): return tip
    return ''

def g(c,*p):
    for k,v in c.items():
        if any(k.startswith(x) for x in p): return v
    return ''
def cl(s): return re.sub(r'\s+',' ', s or '').strip()
def e(s): return html.escape(cl(s))

TIPY = [('predlozhenie','Предложение',0),('КРУЖОК','Кружки',5),('ТРЕУГОЛЬНИК','Треугольники',5),
        ('РОМБ','Ромбы',7),('ГРОБ','Гробы',3),('rezerv','Резерв',0),('vybrosheno','Выброшено',0)]

for c in P:
    c['pred'] = predlagaem(c)
    if not c.get('keep'): c['bucket'] = 'vybrosheno'
    else: c['bucket'] = c['tip'] if c['tip'] in ('КРУЖОК','ТРЕУГОЛЬНИК','РОМБ','ГРОБ') else 'rezerv'

cards_json = [{
  'id':c['id'],'src':c['src'],'srcName':SRC.get(c['src'],(c['src'],''))[0],
  'bucket':c['bucket'],'pred':c['pred'],'metod':c['metod'],'dolya':c['dolya'],
  'hod':c['hod'],'neko':c['neko'],'punkty':bool(c['punkty']),
  'keep':bool(c.get('keep')),'rol':c.get('rol','нет вердикта'),'why':c.get('why',''),
  'uslovie':cl(g(c,'УСЛОВИЕ')),'otvet':cl(g(c,'ОТВЕТ')),
  'pk':cl(g(c,'ПУНКТЫ')),'prim':cl(g(c,'ПРИМЕЧАНИЕ')),
} for c in P]

CSS = """
:root{
  --paper:#f7f4ed; --ink:#14100c; --ink-soft:#5d554a; --line:#ddd5c6;
  --card:#fffdf8; --accent:#b8341f; --accent-soft:#f0d9d3;
  --kruzhok:#2f6b4f; --treug:#1f5b8f; --romb:#8a5a12; --grob:#7a2352;
  --shadow:0 1px 0 var(--line), 0 6px 18px -14px rgba(20,16,12,.5);
}
:root:not([data-theme="light"]){ @media (prefers-color-scheme:dark){
  --paper:#12100e; --ink:#f2ece1; --ink-soft:#a79c8b; --line:#312b24;
  --card:#1a1714; --accent:#ff6a4d; --accent-soft:#3a1d16;
  --kruzhok:#6fd3a0; --treug:#79bdf0; --romb:#e0b062; --grob:#e58bbd;
  --shadow:0 1px 0 var(--line), 0 6px 18px -14px #000;
}}
:root[data-theme="dark"]{
  --paper:#12100e; --ink:#f2ece1; --ink-soft:#a79c8b; --line:#312b24;
  --card:#1a1714; --accent:#ff6a4d; --accent-soft:#3a1d16;
  --kruzhok:#6fd3a0; --treug:#79bdf0; --romb:#e0b062; --grob:#e58bbd;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:"IBM Plex Serif",Georgia,serif;font-size:16px;line-height:1.55;
  -webkit-text-size-adjust:100%}
.wrap{max-width:1080px;margin:0 auto;padding:0 16px 96px}
header{border-bottom:3px solid var(--ink);padding:28px 0 16px;margin-bottom:0}
h1{font-family:"Unbounded",sans-serif;font-weight:900;letter-spacing:-.03em;
  font-size:clamp(28px,6.2vw,58px);line-height:.98;margin:0 0 10px;text-transform:uppercase}
.sub{font-family:"IBM Plex Mono",monospace;font-size:12.5px;color:var(--ink-soft);
  text-transform:uppercase;letter-spacing:.09em}
.totals{display:flex;flex-wrap:wrap;gap:6px 22px;margin-top:14px;
  font-family:"IBM Plex Mono",monospace;font-size:12.5px;color:var(--ink-soft)}
.totals b{color:var(--ink);font-weight:600}
nav{position:sticky;top:0;z-index:20;background:var(--paper);border-bottom:1px solid var(--line);
  margin:0 -16px;padding:0 16px;overflow-x:auto;-webkit-overflow-scrolling:touch}
.tabs{display:flex;gap:2px;min-width:max-content}
.tab{appearance:none;border:0;background:none;cursor:pointer;color:var(--ink-soft);
  font-family:"Unbounded",sans-serif;font-weight:600;font-size:12px;letter-spacing:.02em;
  text-transform:uppercase;padding:14px 12px;border-bottom:3px solid transparent;white-space:nowrap}
.tab:hover{color:var(--ink)} .tab[aria-selected="true"]{color:var(--accent);border-bottom-color:var(--accent)}
.tab .n{font-family:"IBM Plex Mono",monospace;font-weight:400;opacity:.65;margin-left:5px}
.controls{display:flex;flex-wrap:wrap;gap:8px;padding:14px 0;border-bottom:1px solid var(--line)}
input[type=search],select{font-family:"IBM Plex Mono",monospace;font-size:13px;color:var(--ink);
  background:var(--card);border:1px solid var(--line);border-radius:2px;padding:8px 10px}
input[type=search]{flex:1 1 220px;min-width:0}
.card{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--line);
  border-radius:2px;margin:12px 0;box-shadow:var(--shadow)}
.card[data-b="КРУЖОК"]{border-left-color:var(--kruzhok)}
.card[data-b="ТРЕУГОЛЬНИК"]{border-left-color:var(--treug)}
.card[data-b="РОМБ"]{border-left-color:var(--romb)}
.card[data-b="ГРОБ"]{border-left-color:var(--grob)}
.card.pred{outline:2px solid var(--accent);outline-offset:-1px}
summary{cursor:pointer;list-style:none;padding:14px 16px;display:block}
summary::-webkit-details-marker{display:none}
.top{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin-bottom:6px}
.cid{font-family:"IBM Plex Mono",monospace;font-size:11.5px;color:var(--ink-soft);
  overflow-wrap:anywhere}
.badge{font-family:"IBM Plex Mono",monospace;font-size:10px;text-transform:uppercase;
  letter-spacing:.08em;padding:2px 7px;border:1px solid var(--line);border-radius:999px;color:var(--ink-soft)}
.badge.b{border-color:currentColor;font-weight:600}
.badge.kruzhok{color:var(--kruzhok)} .badge.treug{color:var(--treug)}
.badge.romb{color:var(--romb)} .badge.grob{color:var(--grob)}
.badge.rol{border-style:dashed}
.card[data-b="vybrosheno"]{opacity:.62;border-left-color:var(--line)}
.badge.hot{background:var(--accent);border-color:var(--accent);color:var(--paper);font-weight:700}
.peek{font-size:15.5px;color:var(--ink)}
details[open] .peek{display:none}
.body{padding:0 16px 18px;border-top:1px dashed var(--line);margin-top:2px}
.body h4{font-family:"Unbounded",sans-serif;font-size:10.5px;text-transform:uppercase;
  letter-spacing:.12em;color:var(--ink-soft);margin:16px 0 5px;font-weight:700}
.body p{margin:0;font-size:16px}
.usl{font-size:17px;line-height:1.6;margin-top:10px}
.meta{display:flex;flex-wrap:wrap;gap:5px;margin-top:14px}
.pick{display:flex;align-items:center;gap:8px;margin-top:16px;
  font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--ink-soft)}
.pick input{width:17px;height:17px;accent-color:var(--accent)}
#basket{position:fixed;left:0;right:0;bottom:0;z-index:40;background:var(--ink);color:var(--paper);
  font-family:"IBM Plex Mono",monospace;font-size:12.5px;padding:10px 16px;
  display:flex;gap:8px 18px;align-items:center;flex-wrap:wrap;
  box-shadow:0 -8px 24px -18px #000}
#basket .sl{display:flex;gap:14px;flex-wrap:wrap}
#basket b{font-weight:700}
#basket .ok{color:#8fe3b4} #basket .over{color:#ffb38a}
#basket button{margin-left:auto;font-family:inherit;font-size:12px;cursor:pointer;
  background:var(--paper);color:var(--ink);border:0;border-radius:2px;padding:7px 13px;font-weight:600}
.empty{padding:48px 0;text-align:center;color:var(--ink-soft);font-family:"IBM Plex Mono",monospace;font-size:13px}
.note{font-size:14px;color:var(--ink-soft);border-left:2px solid var(--line);padding-left:12px;margin-top:12px}
.warn{background:var(--accent-soft);border:1px solid var(--accent);border-radius:2px;
  padding:14px 16px;margin:18px 0;font-size:15px}
.warn b{font-family:"Unbounded",sans-serif;font-size:11px;text-transform:uppercase;letter-spacing:.1em;
  display:block;margin-bottom:6px;color:var(--accent)}
@media (max-width:640px){ .usl{font-size:16px} h1{letter-spacing:-.02em} }
"""

JS = """
const CARDS = __DATA__;
const NEED = {"КРУЖОК":5,"ТРЕУГОЛЬНИК":5,"РОМБ":7,"ГРОБ":3};
const RU = {"КРУЖОК":"кружки","ТРЕУГОЛЬНИК":"треуг.","РОМБ":"ромбы","ГРОБ":"гробы"};
const picked = new Set();
let tab = 'predlozhenie';
const $ = s => document.querySelector(s);

function visible(c){
  if (tab==='predlozhenie') { if(!c.pred) return false; }
  else if (c.bucket !== tab) return false;
  const s = $('#q').value.trim().toLowerCase();
  if (s && !(c.uslovie+' '+c.id+' '+c.srcName).toLowerCase().includes(s)) return false;
  const src = $('#fsrc').value; if (src && c.src !== src) return false;
  const m = $('#fmet').value;  if (m && c.metod !== m) return false;
  const p = $('#fpk').value;
  if (p==='1' && !c.punkty) return false;
  if (p==='0' && c.punkty) return false;
  return true;
}
function badge(c){
  const cls={"КРУЖОК":"kruzhok","ТРЕУГОЛЬНИК":"treug","РОМБ":"romb","ГРОБ":"grob"}[c.bucket]||'';
  const nm={"КРУЖОК":"кружок","ТРЕУГОЛЬНИК":"треугольник","РОМБ":"ромб","ГРОБ":"гроб"}[c.bucket]||'резерв';
  return `<span class="badge b ${cls}">${nm}</span>`;
}
function esc(s){ const d=document.createElement('div'); d.textContent=s||''; return d.innerHTML; }
function render(){
  const list = CARDS.filter(visible);
  $('#list').innerHTML = list.length ? list.map((c,i)=>{
    const k = c.src+'||'+c.id;
    return `<details class="card${c.pred?' pred':''}" data-b="${c.bucket}">
      <summary>
        <div class="top">${badge(c)}${c.pred?'<span class="badge hot">предлагаю</span>':''}
          <span class="badge rol">${esc(c.rol)}</span>
          ${c.punkty?'<span class="badge">есть пункты</span>':''}
          <span class="badge">${esc(c.dolya)}</span>
          <span class="cid">${esc(c.srcName)} · ${esc(c.id)}</span></div>
        <div class="peek">${esc(c.uslovie.slice(0,150))}${c.uslovie.length>150?'…':''}</div>
      </summary>
      <div class="body">
        <h4>Условие</h4><p class="usl">${esc(c.uslovie)}</p>
        ${c.otvet?`<h4>Ответ и идея</h4><p>${esc(c.otvet)}</p>`:''}
        ${c.punkty&&c.pk?`<h4>Пункты</h4><p>${esc(c.pk)}</p>`:''}
        ${c.prim?`<p class="note">Примечание выемщика: ${esc(c.prim)}</p>`:''}
        ${c.why?`<h4>${c.keep?'Что именно считается':'Почему выброшена'}</h4><p>${esc(c.why)}</p>`:''}
        <div class="meta"><span class="badge">метод: ${esc(c.metod)}</span>
          <span class="badge">ход виден: ${esc(c.hod)}</span>
          <span class="badge">некомбинаторная на вид: ${esc(c.neko)}</span></div>
        ${c.keep?`<label class="pick"><input type="checkbox" data-k="${esc(k)}"${picked.has(k)?' checked':''}>
          взять в листок</label>`:''}
      </div></details>`;
  }).join('') : '<div class="empty">ничего не нашлось — ослабьте фильтры</div>';
  $('#shown').textContent = list.length;
}
function basket(){
  const by = {"КРУЖОК":0,"ТРЕУГОЛЬНИК":0,"РОМБ":0,"ГРОБ":0};
  picked.forEach(k=>{ const c=CARDS.find(x=>x.src+'||'+x.id===k); if(c&&by[c.bucket]!==undefined) by[c.bucket]++; });
  $('#slots').innerHTML = Object.keys(NEED).map(t=>{
    const n=by[t], need=NEED[t];
    const cls = n===need?'ok':(n>need?'over':'');
    return `<span class="${cls}">${RU[t]} <b>${n}</b>/${need}</span>`;
  }).join('') + `<span>всего <b>${picked.size}</b></span>`;
}
document.addEventListener('change', ev=>{
  const cb = ev.target.closest('input[type=checkbox][data-k]');
  if(cb){ cb.checked ? picked.add(cb.dataset.k) : picked.delete(cb.dataset.k); basket(); return; }
  if(ev.target.closest('.controls')) render();
});
document.addEventListener('input', ev=>{ if(ev.target.id==='q') render(); });
document.addEventListener('click', ev=>{
  const t = ev.target.closest('.tab');
  if(t){ tab=t.dataset.t; document.querySelectorAll('.tab').forEach(x=>x.setAttribute('aria-selected', x===t));
         render(); window.scrollTo({top:0}); }
  if(ev.target.id==='copy'){
    const out = [...picked].map(k=>{const c=CARDS.find(x=>x.src+'||'+x.id===k);
      return `[${c.bucket}] ${c.srcName} · ${c.id}\\n${c.uslovie}`;}).join('\\n\\n');
    navigator.clipboard.writeText(out||'(ничего не выбрано)').then(()=>{
      ev.target.textContent='скопировано'; setTimeout(()=>ev.target.textContent='скопировать выбранное',1600); });
  }
});
render(); basket();
"""

# --- счётчики для вкладок ---
def count(key):
    if key=='predlozhenie': return sum(1 for c in P if c['pred'])
    return sum(1 for c in P if c['bucket']==key)

srcs = sorted({c['src'] for c in P}, key=lambda s: -sum(1 for c in P if c['src']==s))
mets = sorted({c['metod'] for c in P})

o = io.StringIO(); w = o.write
w('<!doctype html><html lang="ru"><head><meta charset="utf-8">')
w('<meta name="viewport" content="width=device-width,initial-scale=1">')
w('<title>Каталог пула — комбинаторика 22.09</title>')
w('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
w('<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@600;900&family=IBM+Plex+Serif:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;600;700&display=swap" rel="stylesheet">')
w(f'<style>{CSS}</style></head><body><div class="wrap">')
w('<header><h1>Пул задач<br>комбинаторика</h1>')
w('<div class="sub">блок «Перебор и правило суммы» · пара 22.09 · дата данных 2026-09-21</div>')
kept = sum(1 for c in P if c.get('keep'))
w(f'<div class="totals"><span>счётных <b>{kept}</b> из {len(P)}</span>')
w(f'<span>источников <b>{len(srcs)}</b></span>')
w(f'<span>с пунктами <b>{sum(1 for c in P if c["punkty"] and c.get("keep"))}</b></span>')
w(f'<span>показано <b id="shown">0</b></span></div></header>')
w('<nav><div class="tabs" role="tablist">')
for k,name,_ in TIPY:
    sel = 'true' if k=='predlozhenie' else 'false'
    w(f'<button class="tab" role="tab" aria-selected="{sel}" data-t="{k}">{name}<span class="n">{count(k)}</span></button>')
w('</div></nav>')
w('<div class="controls"><input type="search" id="q" placeholder="поиск по условию, источнику, номеру…">')
w('<select id="fsrc"><option value="">все источники</option>')
for s in srcs: w(f'<option value="{s}">{html.escape(SRC.get(s,(s,""))[0])}</option>')
w('</select><select id="fmet"><option value="">любой метод</option>')
for m in mets: w(f'<option value="{html.escape(m)}">{html.escape(m)}</option>')
w('</select><select id="fpk"><option value="">пункты: неважно</option><option value="1">только с пунктами</option><option value="0">только монолиты</option></select></div>')
w('<div class="warn"><b>Два просева, и чему здесь нельзя верить</b>')
w('<b style="margin-top:0">Просев 1 — отрицательный.</b> Выемка отбрасывала правило произведения, дроби и проценты, геометрию, двойной подсчёт, Евклида и Дирихле. ')
w('Умножение равных групп как подсчёт клеток прямоугольной таблицы оставлено: граница по объекту — таблица можно, дерево нельзя.<br><br>')
w('<b style="margin-top:0">Просев 2 — положительный.</b> Из 244 карточек оставлено 169: те, в РЕШЕНИИ которых есть шаг «сколько элементов в таком-то множестве». ')
w('Ушли логика и рыцари, обратный ход, игры на чётность позиции, инварианты-не-количества, делимость. Они лежат на вкладке «Выброшено» с причиной у каждой. ')
w('У оставшихся проставлена роль подсчёта: прямая мощность · оценка счётом · сравнение мощностей · дополнение · вспомогательный подсчёт. ')
w('Последняя роль — самая ценная: вопрос звучит не про количество, но без подсчёта мощности решения нет.<br><br>')
w('<b style="margin-top:0">Чему нельзя верить.</b> Поле «доля класса» — оценка выемщика, а не данные, и именно на нём держится расчёт разброса. ')
w('Прогноз в процентах по каждой задаче пишете вы до занятия (Р148), замер сверяет его с фактом.</div>')
w('<div id="list"></div></div>')
w('<div id="basket"><span class="sl" id="slots"></span><button id="copy">скопировать выбранное</button></div>')
w('<script>' + JS.replace('__DATA__', json.dumps(cards_json, ensure_ascii=False)) + '</script>')
w('</body></html>')

open('KATALOG-pula-22-09.html','w',encoding='utf-8').write(o.getvalue())
print('KATALOG-pula-22-09.html собран:', round(len(o.getvalue())/1024), 'КБ, карточек', len(P),
      ', в предложении', sum(1 for c in P if c['pred']))
