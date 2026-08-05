# PRIMERY — живые эталоны для шага 9 «Иллюстрации»

> Цитаты из уже собранных деков (`dandelin`, `buffon`) — точные пути, дословный код, каждый факт ниже сверен чтением реального файла (не пересказ). Открой этот файл ПЕРЕД тем, как писать первый SVG или трогать первый чаптер — канон уже здесь, не изобретай заново.

## §1. Статичный SVG — канон рисунка

### 1а. Линия + палитра + идентификаторы (полная цитата, 20 строк)
`dandelin/src/illustrations/axial-section.svg`:
```svg
<svg width="100%" height="100%" preserveAspectRatio="xMidYMid meet" style="display:block" viewBox="0 0 620 460" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Осевое сечение конуса с двумя сферами Данделена; сферы касаются секущей плоскости в фокусах, образующая через P касается сфер в A1 и A2, отрезок A1A2 равен 2a">
  <line x1="310" y1="50" x2="184.5" y2="395" stroke="#b8b4a8" stroke-width="1.3"/>
  <line x1="310" y1="50" x2="435.5" y2="395" stroke="#b8b4a8" stroke-width="1.3"/>
  <circle cx="310" cy="170" r="41" fill="#dfeaf4" fill-opacity="0.45" stroke="#8fb0cf" stroke-width="1"/>
  <circle cx="310" cy="330" r="95.8" fill="#dfeaf4" fill-opacity="0.4" stroke="#8fb0cf" stroke-width="1"/>
  <line x1="224.6" y1="270.2" x2="366.8" y2="183.2" stroke="#b5532a" stroke-width="2"/>
  <line x1="271.4" y1="156" x2="220.0" y2="297.4" stroke="#1a5276" stroke-width="3.2"/>
  <circle cx="310" cy="50" r="2.4" fill="#9a9384"/>
  <circle cx="331.3" cy="205" r="4" fill="#b5532a"/>
  <circle cx="260.5" cy="248.2" r="4" fill="#b5532a"/>
  <circle cx="271.4" cy="156" r="3.6" fill="#1a5276"/>
  <circle cx="220.0" cy="297.4" r="3.6" fill="#1a5276"/>
  <circle cx="231.4" cy="266" r="4.4" fill="#6A5ECF"/>
  <text x="337" y="202" text-anchor="start" font-size="14" fill="#b5532a">F&#8321;</text>
  <text x="254" y="252" text-anchor="end" font-size="14" fill="#b5532a">F&#8322;</text>
  <text x="277" y="151" text-anchor="start" font-size="14" fill="#1a5276">A&#8321;</text>
  <text x="213" y="303" text-anchor="end" font-size="14" fill="#1a5276">A&#8322;</text>
  <text x="222" y="261" text-anchor="end" font-size="15" fill="#6A5ECF">P</text>
  <text x="190" y="232" text-anchor="end" font-size="14" fill="#1a5276">2a</text>
</svg>
```
Канон, который стоит скопировать буквально:
- корневой `<svg>` несёт `width="100%" height="100%" preserveAspectRatio="xMidYMid meet" style="display:block"` + `viewBox` — обязательная четвёрка Р10, без неё фолбэк на intrinsic-размер и обрезание при масштабе (`svgOverflow`);
- обводка 1–3.6px, тонкая линия, ничего заплывшего;
- ТОЛЬКО идентификаторы в `<text>` — `F₁`, `F₂`, `A₁`, `A₂`, `P`, `2a` — ни одного слова-комментария;
- `role="img" aria-label="…"` — единственное место, где допустима полная проза: это для a11y/скринридера, не «текст на картинке».

**Пометка (важно для НОВЫХ файлов):** все 3 проверенных `.svg` дандэлина (`cone-title`, `axial-section`, `tangent-ray` — дистиллят называет и четвёртый, `montage`, не читан здесь) — литеральный hex (`#b8b4a8`, `#1a5276`, `#b5532a`…), НЕ `var()`. Проверено чтением файлов лично, не только со слов дистиллята. Дандэлин — образец СТИЛЯ рисунка (линия, палитра, идентификаторы), НЕ образец механики токенов. **Эталоны хардкодят hex — новые писать через `var()`.**

### 1б. Та же дисциплина, но через `var()` — образец МЕХАНИКИ для новых файлов (полная цитата, 1 строка)
`buffon/src/illustrations/prob-2p.svg` — целиком:
```svg
<svg viewBox="0 0 196 120" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="0" width="196" height="120" fill="var(--card)"/><line x1="10" y1="70" x2="186" y2="70" stroke="var(--rule)" stroke-width="2.5"/><path d="M98 18 L56 104 L140 104 Z" fill="none" stroke="var(--steel)" stroke-width="3.5" stroke-linejoin="round"/><circle cx="73" cy="70" r="6" fill="var(--brick)"/><circle cx="123" cy="70" r="6" fill="var(--brick)"/></svg>
```
Каждая заливка/обводка — `var(--card|--rule|--steel|--brick)`, ноль hex. Это буффон, не дандэлин, — уже живой, собранный в дек пример именно того правила, которое дандэлин пока не соблюдает. Копировать МЕХАНИКУ (var-заливки) — отсюда; СТИЛЬ рисунка (плотность линии, идентификаторы, «без прозы») — из §1а.

**Расхождение, которое стоит знать заранее:** ни один из трёх проверенных SVG буффона (`prob-2p.svg`, `sl-area-1.svg`, `sl-grid-circle.svg`, и ещё 8 файлов той же папки при беглой проверке через `grep`) не несёт на корневом `<svg>` явных `preserveAspectRatio`/`width`/`height`/`style` — только `viewBox`. У дандэлина (§1а) все три проверенных файла несут полный набор. Причина не установлена (внешний CSS вроде `.ill-box svg{width:100%;height:100%;display:block}` в `shablon.html` буффона — вероятная гипотеза, не проверялась — файл не входил в список для чтения). **Для новых файлов арки 9 — писать явно, как в §1а**: это гарантированно верно независимо от внешнего CSS шаблона и буквально то, что требует пайплайн Р10; несоответствие ловит `svgOverflow`.

### 1в. Прецедент конфликта id при инлайне нескольких SVG
`dandelin/src/illustrations/cone-title.svg`, начало файла:
```svg
<svg viewBox="0 0 200 272" preserveAspectRatio="xMidYMid meet" style="display:block;width:100%;height:100%">
  <defs><clipPath id="waffle"><path d="M58 126 L142 126 L100 252 Z"/></clipPath></defs>
```
`id="waffle"` — глобальный для всего итогового документа: все `<template id="ill-*">` лежат бок о бок в одном `dist/index.html` одновременно (слайды не перемонтируются при навигации). Второй независимый `id="waffle"` в другом SVG-файле тихо ломает `clipPath` этого через общий id-namespace. В проекте нет pinned SVGO с `prefixIds` (открытый вопрос и в DOK, и в дистилляте шага 9) — на практике такой id префиксуется РУКАМИ (например `cone-title-waffle`, поправить и ссылку `url(#cone-title-waffle)`) ДО того, как файл ляжет в `illustrations/`.

## §2. Плейсхолдер — формат входа
`dandelin/src/illustrations/spheres.html` — целиком:
```html
<div class="ph"><div><div class="ph-t">Шары Данделена</div><div class="ph-s">3D ЯДРО · ждём файл · 4 сцены<br>конус → верхний → нижний → F₁ F₂</div></div></div>
```
`.ph` — корень плейсхолдера · `.ph-t` — заголовок (какая иллюстрация) · `.ph-s` — `РОД · ждём файл · N сцен<br>такты через →`. Род (`SVG ЯДРО`/`3D ЯДРО`/`РАСТР`), заявленный в плейсхолдере, — заявка сценария, не приговор: арка 9 сама решает ветку по правилу оркестрации (ZAHOD §3), глядя на содержание, а не только на слово в тексте.

**Живой урок осиротевшего плейсхолдера.** Этот самый файл (`illustrations/spheres.html`) до сих пор лежит в дереве дандэлина, хотя решение по нему давно принято — ветка 3. Реальная иллюстрация живёт в `chapters/spheres.html`+`drivers/10.js` (см. §3), а слайды ссылаются на неё через `data-iframe="tpl-spheres"` — проверено `grep` по `slides/s04.html` и `slides/s05.html`, НЕ через `data-ill="spheres"`. Значит `illustrations/spheres.html` сегодня нигде не резолвится — мёртвый плейсхолдер; генератор в лучшем случае молча пропустит его («неиспользуемый файл → warn»), не упадёт. Урок для арки 9: когда плейсхолдер в `illustrations/` на деле оказывается веткой 3, старый файл-плейсхолдер надо убрать или явно пометить, а не оставлять висеть рядом с готовым `chapters/*` — иначе получится ровно такой сирота.

## §3. 3D-глава — контракт deck↔scene
`dandelin/src/chapters/spheres.html` (34 строки) — ключевые фрагменты дословно:
```html
  #hint,#playbtn,#playP,#cap{display:none}
```
```html
<div id="c"></div>
<div id="hint">тащить — вращать · ← → — шаги · E — цвет</div>
<div id="bar"><div id="cap"></div><div id="dots"></div></div>
<button id="playbtn" title="вращение">❚❚</button>
<button id="playP" title="прогон точки">▶ точка</button>
<script>window.THREE=window.parent.THREE;<\/script>
<script>{{DRIVER:10}}<\/script>
```
Разбор:
- `#hint,#playbtn,#playP,#cap{display:none}` — прячет СВОЙ UI чаптера при встраивании (хинт, play-кнопки, подпись), НО НЕ `#dots` — точки-шаги остаются видимыми/кликабельными, ровно по правилу `embedded-scene-in-slides.md`: «hide only genuine junk… never hide the step-dots row».
- `<script>window.THREE=window.parent.THREE;<\/script>` — заём готового three.js у родителя; no-op standalone (открытый отдельно файл имеет `window.parent===window`, строка ничего не делает и не мешает — один и тот же байт-код работает в обоих местах).
- `{{DRIVER:10}}` — слот, куда генератор дословно вставляет байты `drivers/10.js`. Номер слота — 10, не 01: резолвится ИЗ этого конкретного файла, не по аналогии с другим чаптером (см. ниже, это не абстрактная оговорка).
- Контракт `data-scenes`/`data-step-offset` ↔ `goStep`/`ride` живёт на стороне СЛАЙДА и ДРАЙВЕРА, не в этом HTML-скелете: подтверждено `grep` по `slides/s05.html` — `<div class="ill-box" data-iframe="tpl-spheres" data-step-offset="3" data-steps-clickable="1"></div>`. Полный код контракта (движок шлёт `{goStep:n}`/`{ride:true}` через `postMessage`; глава реализует `goStep(n)`/`resize()`; клик по точке шлёт `{navSub:n}` строго родителю, не своей навигацией) — в `embedded-scene-in-slides.md`, раздел «The deck↔scene contract».

**Расхождение с более ранним черновиком дистиллята шага 9 — важно не повторить.** Дистиллят называл парой «пример `chapters/spheres.html`+`drivers/01.js`» (актуальный `DOK.md` этого уже не повторяет — там исправлено на `drivers/10.js`). Живой репозиторий прежнюю формулировку не подтверждает: `grep -o "{{DRIVER:[0-9]*}}" chapters/*.html` в `dandelin/src/` даёт `chapters/spheres.html → {{DRIVER:10}}`, а `{{DRIVER:01}}` реально стоит в `chapters/mirror.html`. Файл `drivers/01.js` (цитата ниже) обслуживает `mirror.html`, не «Шары Данделена». Настоящий драйвер сфер — `drivers/10.js` (27 КБ, three.js-сцена, за пределами объёма этой цитаты, не входил в список для чтения). Урок: номер драйвера всегда резолвить из `{{DRIVER:NN}}` внутри самого `chapters/<NAME>.html`, никогда не предполагать по сюжетному сходству имён файлов.

`dandelin/src/drivers/01.js` — целиком (реальный драйвер `chapters/mirror.html`, показан как рабочий пример КОНТРАКТА драйвера — плоский IIFE, мутирующий конкретные `id` внутри SVG DOM; ни одного упоминания `THREE` — драйвер необязательно про three.js, может быть чистой SVG-интерактивностью):
```js
(function(){
var svg=document.getElementById('svg');
// штриховка зеркала
var h=document.getElementById('hatch'),s='';
for(var x=80;x<=600;x+=40) s+='<line x1="'+x+'" y1="250" x2="'+(x-14)+'" y2="266"/>';
h.innerHTML=s;
function arcBetween(vx,vy,ax,ay,bx,by,r){
  var a1=Math.atan2(ay-vy,ax-vx),a2=Math.atan2(by-vy,bx-vx);
  var d=a2-a1; while(d>Math.PI)d-=2*Math.PI; while(d<-Math.PI)d+=2*Math.PI;
  var x0=vx+r*Math.cos(a1),y0=vy+r*Math.sin(a1),x1=vx+r*Math.cos(a1+d),y1=vy+r*Math.sin(a1+d);
  return 'M'+x0.toFixed(2)+' '+y0.toFixed(2)+' A'+r+' '+r+' 0 0 '+(d>0?1:0)+' '+x1.toFixed(2)+' '+y1.toFixed(2);
}
var S={x:190,y:80}, R={x:470,y:110}, P={x:300,y:250}; // P сдвинут от оптимума → углы неравные
document.getElementById('ray').setAttribute('points',S.x+','+S.y+' '+P.x+','+P.y+' '+R.x+','+R.y);
document.getElementById('P').setAttribute('cx',P.x); document.getElementById('P').setAttribute('cy',P.y);
// дуги С ЗЕРКАЛОМ (горизонталью): слева между лучом к источнику и зеркалом, справа между зеркалом и лучом к приёмнику
document.getElementById('arcA').setAttribute('d',arcBetween(P.x,P.y, S.x,S.y, P.x-40,P.y, 30));
document.getElementById('arcB').setAttribute('d',arcBetween(P.x,P.y, P.x+40,P.y, R.x,R.y, 30));
})();
```
`arcBetween(vertex, rayA, rayB)` — тот самый «единый инструмент для угловых дуг», которого требует `images.md` («Angle arcs are drawn exactly between the two rays — use one shared tool»): дуга строго между двумя лучами, не «на глаз». Полезно и для веток 1/2, не только для драйверов чаптеров — угол всегда через одну такую функцию.

## §4. Растр — `<img>` base64
`buffon/src/illustrations/portrait.html` (478 005 байт, весь файл — одна строка; голова и хвост ниже, base64-тело между ними опущено):
```html
<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAfAAAAKICAIAAAAAVz+AAAAACXBIWXMAAAsSAAALEgHS3X78AAAgAElEQVR42rS9W7MkR3Ie6O4RmVXn1nd0A93obtwvM5whh5SGM9RQfNE+7+sazbRPuzJKtpefJTPZaneNqyFXK3K1kkkiKQ0GwACNWzfQALobfT+XPufUqcqMcN8Hz4zyjMgqNLm2PWNjZ86pysqKjPDw+Pz7PseP/vpPmRkRRSTGqD8455xzIhGQRaRpGudc
… (base64 продолжается) …
ijSHRismDAAAAABJRU5ErkJggg==" alt="">
```
Файл — ровно `<img src="data:image/png;base64,…" alt="">` и ничего больше: нет обёртки `<div class="zone">`, нет `object-fit` внутри самого файла. Значит позиционирование (contain/cover, зона) задаёт `.ill-box`/шаблон СНАРУЖИ, а этот файл несёт только байты картинки — согласуется с `images.md`: «An image occupies a zone like text does; the grid decides its box». `<img>`-изоляция здесь ОК ТОЛЬКО для этой ветки (4, готовый растр) — цвет есть содержимое (фото), не тема; ветки 1–3 никогда не заворачивают результат в `<img>`.

## Откуда эти файлы (точные пути)
- `dandelin/src/illustrations/cone-title.svg`, `dandelin/src/illustrations/axial-section.svg`, `dandelin/src/illustrations/tangent-ray.svg`
- `dandelin/src/illustrations/spheres.html` (плейсхолдер, сегодня осиротевший — §2)
- `dandelin/src/chapters/spheres.html`, `dandelin/src/chapters/mirror.html`, `dandelin/src/drivers/01.js` (реально mirror.html), `dandelin/src/drivers/10.js` (реально spheres.html, не читан целиком — 27 КБ)
- `dandelin/src/tokens.css`, `dandelin/src/slides/s04.html`, `dandelin/src/slides/s05.html` (только грепнуты на `data-iframe`/`data-step-offset`, не читаны целиком)
- `buffon/src/illustrations/prob-2p.svg`, `buffon/src/illustrations/sl-area-1.svg`, `buffon/src/illustrations/sl-grid-circle.svg`, `buffon/src/illustrations/portrait.html`
