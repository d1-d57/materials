# PRIMERY — живые эталоны для шага 8 «Сцены»

> 🗄 **АРХИВ — конвейер до 27.07.2026.** Файл описывает СТАРЫЙ конвейер: 10 стадий `01-brief`…`10-sborka-qa`,
> реестр `GEJTY.md`, дерево `src/`+`slides/`. **Живой конвейер — фазы Ф1…Ф7**, его
> карта: `../KARTA-ZHIVOGO-KONVEJERA.md` (там же машиночитаемый реестр инструментов §5 и гейт
> согласованности `_generator/tools/check_karty.py`, который краснеет, когда реестр
> и диск разъезжаются). 🔴 **Отсюда НИЧЕГО не удалено:** история решений — единственное,
> чем доказывается «почему так», и стадия может оказаться живой в другом проекте.
> Помечено заходом `karta-kak-reestr` 2026-08-09; гейт согласованности архивные файлы
> не читает вовсе.


> Цитаты из уже собранных деков (`dandelin`, `buffon`) — точные пути, дословный код, каждый факт ниже сверен чтением реального файла (не пересказ). Открой этот файл ПЕРЕД тем, как ставить первый `{blur@}`/`{fill@}` — канон уже здесь, не изобретай заново.

## §1. `{fill@}` + `{blur@}` в одном списке — и правило «связка вне блюра»

### 1а. Полная цитата — `buffon/src/content/sl-polygons.md`, строка 5 (степенчатый абзац)
```md
{.steps @2}Погнём иглу длины $\boldsymbol{1}$ на {fill@4| $\boldsymbol{8}$ | $\boldsymbol{k}$ } равных частей и сложим из<br>них правильный многоугольник. Бросим его $\boldsymbol{N}$ раз:<br><span class="li">• каждая сторона пересечёт линию ≈<span class="fill"><span class="blur-reveal" data-reveal="3" data-scene-until="4">$\boldsymbol{\tfrac{p}{8}\cdot N}$</span><span data-scene-from="4">$\boldsymbol{\tfrac{p}{k}\cdot N}$</span></span> раз,</span><br><span class="li">• всего произойдёт ≈{blur@3| $\boldsymbol{p\cdot N}$ } пересечений,</span><br><span class="li">• многоугольник пересекает линию {blur@3| $\boldsymbol{0}$ или $\boldsymbol{2}$ } раза,</span><br><span class="li">• ≈{blur@3| $\boldsymbol{\tfrac{p}{2}\cdot N}$ } многоугольников пересекает линии.</span>
```
Разбор:
- `{fill@4| $\boldsymbol{8}$ | $\boldsymbol{k}$ }` — верхнеуровневый инлайн-fill шорткатом Р2: конкретное число сторон «8» меняется на общее «k» на сцене 4; генератор сам собирает пару `<span class="fill">`.
- Внутри второго буллета — РУЧНОЙ `<span class="fill">` (escape hatch, не шорткат), потому что нужен ЕЩЁ и блюр внутри одного из двух состояний: `<span class="fill"><span class="blur-reveal" data-reveal="3" data-scene-until="4">…p/8·N…</span><span data-scene-from="4">…p/k·N…</span></span>`. Это по-прежнему РОВНО два child верхнего уровня (блюр-до-сцены-4 / смена-на-сцене-4) — третий child не добавлен, блюр «вложен» в первый.
- Три отдельных `{blur@3|...}` (для `p·N`, `0 или 2`, `p/2·N`) — три независимые блюр-шторки на одну и ту же сцену 3; каждая станет своим `<span class="blur-reveal" data-reveal="3">`.
- **Правило «связка вне блюра» в действии.** Символ `≈` перед КАЖДЫМ из трёх мест (в буллетах 1, 2, 4) стоит СНАРУЖИ шторки — литеральный текст абзаца, не аргумент `{blur@}`/`{fill@}`. DOK формулирует антипаттерн так: НИКОГДА `<span class="fill">≈ …</span>` — если бы `≈` оказался ВНУТРИ шторки вместе со значением, он вошёл бы в содержимое ОДНОГО конкретного child'а (например, того, что виден ДО раскрытия), а второй child (виден ПОСЛЕ) этого `≈` не содержит по построению — при равном `grid-area:1/1` у обоих child'ов результат «прыгает» вместо чистой замены значения. Ставь связку строкой ДО шторки — как везде в этом примере.

### 1б. Тот же механизм без блюра — «разболдивание» вопроса, строки 1–2 того же файла
```md
{.q} <span class="fill fill-q"><span data-scene-until="2">А если вместо треугольника бросать **квадрат**</span><span data-scene-from="2">А если вместо треугольника бросать квадрат</span></span>\
<span class="fill fill-q"><span data-scene-until="2">**периметра $\boldsymbol{1}$**? **пятиугольник**? **восьмиугольник**?</span><span data-scene-from="2">периметра $\boldsymbol{1}$? пятиугольник? восьмиугольник?</span></span>\
```
`.fill` здесь меняет НЕ значение, а НАЧЕРТАНИЕ (жирный вопрос → обычный текст на сцене 2) — тот же принцип «ровно два взаимоисключающих child» (`data-scene-until="2"` / `data-scene-from="2"`), без единого символа блюра. `buffon/src/shablon.html`, строки 255–256, подтверждает это осознанным авторским решением комментарием прямо у грид-правила:
```css
/* вопрос раз-болживается на шаге 2 — свап через .fill, выключка влево (паттерн sl-count) */
#sl-polygons .fill-q { text-align: left; }
```

## §2. `{@N}` на весь абзац — `buffon/src/content/sl-plan.md` (файл целиком, 12 строк)
```md
Разрежем иглу на три равные части. Сложим из\
них треугольник и будем бросать на плоскость\
<b>Сколько</b> (примерно) <b>будет точек пересечения\
треугольников и линий?</b>

{@2} Покрасим стороны треугольников в зелёный,\
жёлтый и оранжевый

{@2} Сначала мы найдём количество пересечений\
линий со сторонами <b>жёлтого</b> цвета\
Пересечений с зелёными и оранжевыми будет\
столько же, а всех вместе в три раза больше
```
`_generator/SLIDE-FORMAT.md` документирует разворачивание ЭТОГО ЖЕ файла дословно: «→ разворачивается в три `<p>`, второй и третий с `data-scene-from="2"`, все переносы `<br>` на местах. Пересобранный слайд рендер-идентичен оригиналу (проверено)». Заметь: оба нижних абзаца несут ОДИН И ТОТ ЖЕ `{@2}` — раскадровка этого слайда даёт им появиться ОДНИМ кликом вместе, а не по одному (если бы требовался отдельный клик на каждый, второй абзац нёс бы `{@3}`, и слайд стал бы трёхсценовым).

## §3. Как `{@N}` разворачивается на экране — каскад в `shablon.html`
`{@2}` из §2 генератор превращает в `data-scene-from="2"` на `<p>`; ПОКАЗЫВАЕТ это CSS-каскад, дословно живущий в `<style>` шаблона дека (не в `content/*.md`, не в отдельном `base.css` — см. `FORMAT-ISTOCHNIKA.md` о расхождении с `DESIGN.md §4`), структурно идентичный в обоих деках:

`buffon/src/shablon.html`, строки 51–60:
```css
/* сцены: скрытые шаги сохраняют место (visibility, НИКОГДА display) */
[data-scene-from] { opacity: 0; visibility: hidden; transition: opacity .24s ease; }
.formula[data-scene-from], [data-scene-from] .formula { transition-delay: .14s; }
.panel[data-scene-from] { transition-delay: .12s; }
.scene-2 [data-scene-from="2"],
.scene-3 [data-scene-from="2"], .scene-3 [data-scene-from="3"],
.scene-4 [data-scene-from="2"], .scene-4 [data-scene-from="3"], .scene-4 [data-scene-from="4"],
.scene-5 [data-scene-from="2"], .scene-5 [data-scene-from="3"], .scene-5 [data-scene-from="4"], .scene-5 [data-scene-from="5"]
  { opacity: 1; visibility: visible; }
@media (prefers-reduced-motion: reduce) { [data-scene-from] { transition: none; } }
```
`dandelin/src/shablon.html`, строки 58–66 — структурно тот же каскад, числа сцен идентичны (сама длительность transition отличается — `.35s` против `.24s` в buffon, это уже вкус конкретного дека, не часть контракта):
```css
[data-scene-from] { opacity: 0; visibility: hidden; transition: opacity .35s; }
.scene-2 [data-scene-from="2"],
.scene-3 [data-scene-from="2"], .scene-3 [data-scene-from="3"],
.scene-4 [data-scene-from="2"], .scene-4 [data-scene-from="3"], .scene-4 [data-scene-from="4"],
.scene-5 [data-scene-from="2"], .scene-5 [data-scene-from="3"], .scene-5 [data-scene-from="4"], .scene-5 [data-scene-from="5"]
  { opacity: 1; visibility: visible; }
@media (prefers-reduced-motion: reduce) { [data-scene-from] { transition: none; } }
```
`engine.js` ставит класс `scene-K` на `<section>` при навигации (сам движок здесь не цитируется — чужой слой, арка 8 его не трогает); класс `.scene-K` НА СЕКЦИИ + атрибут `[data-scene-from="K"]` НА ПОТОМКЕ нужны одновременно, иначе элемент остаётся `opacity:0`. Каскад жёстко перечислен только ДО сцены 5 (последняя строка — `.scene-5 […]`) — слайду с числом сцен БОЛЬШЕ 5 нужно либо продолжение каскада в `shablon.html` (чужой слой — вопрос в `## ВОПРОСЫ`, не тихая правка), либо раскадровка в ≤5 сцен.

**Деталь, которую легко упустить:** stagger-задержка (`.14s`/`.12s`) на `.formula`/`.panel` (buffon, строки 53–54 выше) и на `.pull`/`.panel` (dandelin, строки 87–88, тот же приём — `[data-scene-from] .pull, [data-scene-from].pull { transition-delay: .14s; }` / `[data-scene-from] .panel, [data-scene-from].panel { transition-delay: .12s; }`) — часть БАЗОВОГО `shablon.html` у ОБОИХ деков, то есть общий канон, а не per-deck вкус. Само число (~120–140мс) — и есть то отставание картинки от текста, о котором предупреждает DOK.

## §4. `overlay.css` — blur-reveal + отмена стагера (per-deck, кандидат в канон-базу)
`buffon/src/overlay.css`, строки 12–25 (механизм блюра, полная цитата):
```css
/* ===== KaTeX + accent + blur-reveal (multi-scene threshold) ===== */
:root{--accent:#785a18}   /* охра: переменная не была определена в деке — лечит тёмные акценты B1 */
.katex{font-size:1.02em}
.acc,.acc .katex,.acc .katex *{color:var(--accent)!important}
/* G5: переход 8→k на sl-polygons — изменившийся символ подсвечен золотом */
#sl-polygons [data-scene-from="4"],#sl-polygons [data-scene-from="4"] .katex *{color:var(--accent)}
.blur-reveal{filter:blur(5.5px) saturate(.55);opacity:.9;color:var(--steel);
  transition:filter .5s ease,opacity .5s ease,color .5s ease;will-change:filter}
.scene-2 .blur-reveal[data-reveal="2"],
.scene-3 .blur-reveal[data-reveal="2"],
.scene-3 .blur-reveal[data-reveal="3"],
.scene-4 .blur-reveal[data-reveal="2"],
.scene-4 .blur-reveal[data-reveal="3"],
.scene-4 .blur-reveal[data-reveal="4"]{filter:none;opacity:1;color:var(--accent)}
```
…(строки 26–32 опущены — кегль формул/акцента-героя, не про сцены)…, затем строки 33–34:
```css
/* ===== синхронное раскрытие сцены: текст + картинка появляются ВМЕСТЕ ===== */
.formula[data-scene-from],[data-scene-from] .formula,.panel[data-scene-from]{transition-delay:0s!important}
```
Разбор: `.blur-reveal{filter:blur(...)…}` + сценовый каскад `.scene-K .blur-reveal[data-reveal="K"]{filter:none...}` — это ВЕСЬ визуальный механизм блюра; без него `data-reveal` — не более чем инертный атрибут (клик формально засчитан генератором, но глазами ничего не размыто и не проявляется — визуальный дед-клик поверх честной разметки). Строка 34 — ОТМЕНА базового стагера `.formula`/`.panel` из §3 (`.14s`/`.12s`) через `!important 0s`, когда текст и картинка одной сцены должны проявиться синхронно. **Обе части живут ТОЛЬКО в `overlay.css`, который есть у buffon и физически ОТСУТСТВУЕТ у dandelin** (`FORMAT-ISTOCHNIKA.md`: «overlay.css — опц. … Есть у buffon, НЕТ у dandelin») — на dandelin `.pull`/`.panel` ВСЕГДА проявляются с отставанием ~140/120мс от текста (см. §3), синхронного режима там нет нигде, и `{blur@}` там тоже не используется ни разу.

**Почему это важно для нового дека** (аннотация уровня конвейера, ещё НЕ решено — см. DOK «Открытые вопросы»): оба правила — механизм, а не стиль конкретного дека, поэтому DOK рекомендует со временем вынести их в канон-базу (`base.css`/`shablon.html`), одна правка на все деки. Пока не вынесено — арка 8 обязана на КАЖДОМ новом деке с `{blur@}` или синхронным «текст+картинка» проверить, есть ли этот блок в `overlay.css` дека, и если нет — поднять вопрос переноса (не тихо копировать мимо отчёта, см. `ZAHOD.md` `## 2`).

## Откуда эти файлы (точные пути)
- `buffon/src/content/sl-polygons.md` (строки 1–2, 5, 7), `buffon/src/content/sl-plan.md` (целиком, 12 строк)
- `buffon/src/shablon.html` (строки 51–60, 255–256), `dandelin/src/shablon.html` (строки 58–66, 87–88)
- `buffon/src/overlay.css` (строки 12–25, 33–34)
- `_generator/SLIDE-FORMAT.md` (документированное разворачивание `sl-plan.md`)
- `_studio/konvejer/FORMAT-ISTOCHNIKA.md` (какой опциональный модуль есть у какого дека)
- `_studio/konvejer/08-sceny/DOK.md` (формулировка правила «связка вне блюра», контракт `data-scenes`, гейт `--scene-diff`)
