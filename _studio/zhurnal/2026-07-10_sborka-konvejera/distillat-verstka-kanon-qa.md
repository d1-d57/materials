# Дистиллят: вёрстка / канон / QA → семя арок 7, 8, 10

Источники: `html-slides-studio` (`per-slide-algorithm.md`, `slide-engine.md`, `style-core.md`,
`typography.md`, `simulations.md`, `scripts/audit.py`, `scripts/build_single.py`,
`assets/deck-skeleton.html`, `decks/02-buffon.md`, `decks/06-conics.md`) + наш
`_generator/{build_deck.py,DESIGN.md,SLIDE-FORMAT.md,render.py}` + живой код `dandelin/src`
и `buffon/src`. Все числа/имена проверены по живым файлам (не по памяти о скилле).

## Рамка: два билда, одна суть

Скилл описывает вёрстку/сцены/сборку через СВОЙ путь: `deck-skeleton.html` → ручная правка →
`build_single.py` (delivery-копия) + `scripts/audit.py`. У нас — `_generator/build_deck.py`
собирает `src/` (`content/*.md` + `slides/*.html` + `illustrations/*` + `tokens.css` +
`engine.js` + `brief.md`) в `dist/index.html`; движок и per-slide-грид уже физически лежат
внутри `shablon.html`/`engine.js` конкретного дека — не в шаблоне-заготовке.

Ключевой факт, меняющий чтение скилла: наш `engine.js` — это НЕ чистый `deck-skeleton.html`,
а уже РАСПИЛЕННЫЙ из живого канон-дека файл, в котором pilot-validated патчи из
`slide-engine.md` уже вшиты и верифицированы: `style.zoom` для обзора (grep подтвердил в
`buffon/src/engine.js`), binary-search `.fit`/`fitAll`/`measureGroups`/`applyScene`
(подтверждено в `dandelin/src/engine.js`). Sim-reset-на-входе (`justShown`/`_simVis`/
`MutationObserver`) живёт НЕ в `engine.js`, а в `sims/lab.core.js` (подтверждено grep'ом —
`Lab.prototype.settle`, `activate(slide, justShown)`). Значит именованный patch-механизм
из `DESIGN.md` §6 («движок дословно + патчи sim_reset/overview из `buffon-canon-build.py`»)
build_deck.py на деле НЕ реализует и не должен — патчи уже осели в файлах на этапе распила.

Оба tokens.css (`dandelin`, `buffon`) палитрой и типо-токенами **идентичны**: `--paper:#e6e5e1
--board:#a7c2cb --card:#ffffff --ink:#333333 --accent:#785a18 --marker:#c0aa5a` +
`--t-lead:50px --t-body:38px --t-dense:33px --t-caption:20px` — это подтверждает Р8 (canon.tokens
primitive-слой общий) фактически, не только по решению.

---

## Арка 7 — Вёрстка

**Контракт вход→выход.** Вход: строка раскадровки (beat·archetype·описание
иллюстрации·текст) ИЛИ существующий Canva-слайд под распил + `tokens.css` дека. Выход:
`slides/<id>.html` (`<section class="slide" data-scenes="N">`, грид-зоны, слот
`{{MD:<id>}}`/`{{copy:zone}}`, пустые `data-ill` боксы) + `content/<id>.md` (или дословный
HTML — escape hatch) + per-slide грид-CSS `#<id> .grid{…}`, который остаётся ВНУТРИ
`shablon.html` — отдельный файл `grids.css` из контракта `DESIGN.md` §4 НЕ используется ни
в dandelin, ни в buffon (проверено: грид живёт в `<style>` шаблона, как в
`deck-skeleton.html`-демо). Арка 7 наследует эту практику, не аспирационный контракт.

**Гейт.** Правка существующего слайда → Р1 (render-identity/нормализованная сверка). Новый
слайд → цепочка `per-slide-algorithm.md` шагов 1→2→5→6, адаптированная: текст сначала (из
арки 6, дословно) → архетип/грид (не хэнд-тюнинг ширин зон) → fill&fit (переполнение =
SPLIT слайда, `--t-body` никогда не уменьшать) → рендер + глаз (`render.py`, `?only=N`).
Машинно (арка 10): 0 overflow `.zone`, body ≥ 35px (4.3%H@810), фон-палитра только из
`:root`-токенов, fit-группы консистентны.

**Что переносим дословно.** Two-plane core (paper/board/card, острые стыки, текст всегда
`#333`, акцент только Bold + один охряный `.acc`); блочный ритм — ОДИН `copy p+p{margin-top:
26px}`, ОДИН `--t-body` без уменьшенных `.t-small` (`.t-small{font-size:var(--t-body)}`);
порядок починки переполнения (блок-гэп → отступ формулы → перераспределение grid-rows →
ТОЛЬКО В КОНЦЕ фиттер) — уже буквально в `overlay.css`/`shablon.html` обоих деков, арка 7
это документирует как чек-лист, не изобретает.

**Что адаптируем.** Каталог архетипов (25%W сайдбар, 74%W рейка, 15/19.5%H плашка, 44%H
доска-полоса из `decks/02-buffon.md`) — статистика Canva-корпуса, НЕ буквальный CSS: ни
dandelin, ни buffon не используют общие классы `fr-sidebar`/`fr-board` — каждый `#sNN .grid`
bespoke под слайд (проверено в обоих `shablon.html`). Решение для арки 7: держать архетипы
как справочную таблицу выбора «что где сидит», код грида писать point-wise на id слайда —
не абстрагировать в общие CSS-классы преждевременно. Различение fit-роли (`.fit`+`data-max`,
display-элементы: Forum caps, цифры, рубрики) vs body-роли (фиксированный `--t-body`,
никогда не фитится) — переносим правило, «куда вешать `.fit`» решает арка 7 по типу
элемента слайд за слайдом.

**Уточнение, не явное в скилле, вскрытое сверкой с живым кодом.** «No padding on zone» —
правило для зон С `.fit`-элементами (фиттер читает `clientWidth/Height`, паддинг искажает
измерение); зоны только с фиксированным `--t-body` спокойно носят паддинг через
утилитарный класс (`.pad{padding:46px 56px 0 56px}`, слитый с `.zone` в `dandelin/src/
shablon.html`: `<div class="zone pad">`). Арка 7 обязана закрепить это разделение явно, а
не копировать общее «zero padding» буквально.

**Внешнее.** Ничего (Р3). `frontend-design`/`web-typography` в скилле — только для
свободного режима, вне scope (канон заморожен).

**Ловушки.** Процентная высота внутри auto-sized grid-row молча схлопывается в размер
контента (тянет SVG до ~2000px) → всегда `minmax(0,1fr)` или явные px/fr в
`grid-template-rows`. Два `.fit` в одной зоне проходят по отдельности, переполняют вместе
→ один `.fit` на зону. Архетипные проценты — ориентир поиска, не копипаст: слепой перенос
на новый слайд без проверки объёма текста поймает только глаз, не гейт (Р1 гейт есть лишь
для регрессии, не для нового слайда).

---

## Арка 8 — Сцены

**Контракт вход→выход.** Вход: `slides/<id>.html` с готовой финальной геометрией (все шаги
уже размещены, скрыты) + разметка в `content/<id>.md`: `{@N}`/`{@N-M}`/`{@-M}` на абзаце,
инлайн `{@N|текст}`, шторки `{fill@N|бланк|ответ}` и `{blur@N|значение}` (SLIDE-FORMAT.md,
исполняет `render_inline_md`/`_attrs_from_tag` в `build_deck.py`). Выход:
`data-scene-from`/`data-scene-until` на `<p>`/`<span>`, `data-scenes="N"` на `<section>`,
CSS-раскрытие через `opacity+visibility` (никогда `display`) — уже пишет генератор +
`engine.js`; арка 8 отвечает за ПРАВИЛЬНУЮ разметку в md, не за код движка.

**Гейт.** Аналог `--scene-diff` (`scripts/audit.py`): последовательные сцены отличаются
ТОЛЬКО добавленными пикселями (заморожена геометрия) и ни один клик не пустой. Ручной
чек: связка (`≈`, `=`) никогда не блюрится вместе со значением — только сам ответ;
структурные символы вне `.fill`/blur. Дед-клик (сцена без видимых изменений) — дефект
(прецедент Kepler 3→1 сцены).

**Что переносим дословно.** Весь синтаксис Р2 уже парсит `build_deck.py`: `{@N}` →
`data-scene-from`, `{fill@N|a|b}` → пара `<span class="fill">`, `{blur@N|x}` →
`<span class="blur-reveal" data-reveal="N">`; `engine.js` несёт `applyScene`, CSS-каскад
`.scene-K [data-scene-from="K"]{opacity:1;visibility:visible}` до 9 сцен, `scene-off` для
`data-scene-until`. Правило «связка вне блюра» (`≈ <span class="fill">…</span>`, НИКОГДА
`<span class="fill">≈ …</span>` — второй child ломает `grid-area:1/1`) — рабочий пример есть
в `buffon/src/content/sl-polygons.md` (вложенные `{fill@N|…}` + `{blur@N|…}` в одном списке,
`{fill@4|$\boldsymbol{8}$|$\boldsymbol{k}$}` внутри строки с отдельным `{blur@3|…}`).

**Что адаптируем.** `transition-delay` на `.formula`/`.panel`/`[data-scene-from]` должен
быть обнулён для синхронного раскрытия текста+картинки одной сцены (иначе картинка
отстаёт на ~120–140мс) — фикс уже в `buffon/src/overlay.css`
(`.formula[data-scene-from],[data-scene-from] .formula,.panel[data-scene-from]{transition-
delay:0s!important}`), но это PER-DECK патч, не базовый `shablon.html` — на каждом новом
деке нужно решать/подтверждать заново. Мост к арке 9: каждый sim (`canvas
data-sim="kind"`) обязан реализовать `settle()`/`reset()`/`play()`/`onScene(k)`, чтобы
попасть под контракт «открывается на нуле» — сама механика (`justShown`/`_simVis`/
`MutationObserver`) уже дословно в `sims/lab.core.js`, арка 8 её не пишет, только требует
эти 4 метода от нового sim.

**Внешнее.** Ничего для механики сцен. 3D-главы (архетип A из `decks/06-conics.md`:
`data-step-offset`, postMessage `{goStep}`/`{ride}`, resize-on-show) — мост к арке
9/`threejs`; сама синхронизация deck↔iframe (hash-поллинг, ~150мс) уже дословно в
`shablon.html` обоих деков вне блока `[4]` (подтверждено в `dandelin/src/shablon.html`,
последний `<script>`) — арка 8 знает контракт (не ставить `data-ride` рядом со степами),
авторинг сцены — арка 9.

**Ловушки.** Общее правило `[data-scene-from]{opacity:0;transition:opacity .35s}`
перебивает `.reveal`/`.blur-reveal` при равной специфичности (правило позже в каскаде
выигрывает) — блюр «дёргается» вместо анимации, если не отделить общее правило через
`:not(.reveal)`/`:not(.blur-reveal)`. **Не проверено дословно в этом дистилляте**, разносит
ли БАЗОВЫЙ `shablon.html` (вне overlay-патча) эти селекторы по умолчанию — риск, см. next.
`.fill` — inline-grid ровно с одним активным child на сцену, связка-текст ДО `.fill`, не
внутри. `prev()` в `engine.js` не покадровый откат: внутри сцены — сброс на шаг 1, с шага 1
— переход на ФИНАЛЬНУЮ сцену предыдущего слайда; авторам сцен нужно знать это заранее, не
проектировать сцены под покадровый назад.

---

## Арка 10 — Сборка + QA

**Контракт вход→выход.** Вход: заполненная `<lecture>/src/` (итог арок 6–9): `brief.md`
(`slide_order`, id, canvas), `shablon.html`, `tokens.css`, `fonts/faces.css`, `engine.js`,
`content/*.md`, `slides/*.html`, `illustrations/*`, опц. `chapters/`+`drivers/`+
`lib/three.min.js`, опц. `sims/`+`math/katex.json`. Выход: `dist/index.html`
самодостаточный (0 внешних asset-URL) + консольный PASS/FAIL-отчёт с exit-кодом.

**Гейт слоями (дёшево → дорого).**
1. Линтер `build_deck.py` (уже реализован, stdlib, без браузера): 0 нерезолвленных
   `{{...}}`; 0 `⟦MISSING-MATH⟧`; каждый `data-ill`/`data-iframe` резолвится в файл; каждый
   `var(--x)` в illustrations/overlay определён в `tokens.css`; 0 внешних src/href (кроме
   `<a href>`); `slide_order` = точное покрытие `slides/`, без сирот/дублей.
2. Render-identity (Р1, для правок существующего дека): нормализованный посимвольный
   дифф (снять HTML-комментарии, схлопнуть пробелы) — доказано byte-exact на dandelin
   (sha256 `69812415…`), почти byte-exact на buffon (`cmp` exit 0 при `--no-banner`).
   Дешевле браузерной сверки — первый рубеж.
3. Аудит (адаптация `scripts/audit.py`, нужен playwright): overflow `.zone`==0;
   shadow/radius/gradient==0; фон-плашки только из палитры (парсить `:root` из СОБРАННОГО
   `tokens.css` дека, не хардкодить allow-list — Р8 tiers разрешает пер-дек оверрайд);
   весь `.fit`/`.t-body` текст `#333333`; 0 `<figcaption>`; `.t-body` ≥ 35px;
   fit-группы консистентны. Адвайзори: проза в `<text>` SVG, канвас < 12% площади слайда.
4. `--scene-diff` (тот же аудит): см. арку 8.
5. Глаз: `render.py <deck> [outdir]` (все слайды PNG, `?only=N&scene=99`); `render.py
   --compare orig rebuilt outdir` (попиксельный дифф Pillow) — уже реализовано у нас,
   гонять на каждой правке, не только на майлстоуне.

**Что переносим дословно.** `build_deck.py` (линтер+сборка) и `render.py`
(shoot+compare) уже готовы — арке 10 нужно только СЕКВЕНИРОВАТЬ их в один прогон и
описать как арк-файл (когда какой гейт, что делать при FAIL). Метод «рендерь ОБА,
оригинал и пересборку, сравнивай side-by-side ДО done» — уже в `render.py --compare`.

**Что адаптируем.** Из `scripts/audit.py` переносим паттерн 1:1 (JS-пробинг через
`page.evaluate`, PASS/FAIL/WARN построчно, exit 1 при FAIL, WARN не валит билд;
`FLOOR_PX=35`; структурные проверки overflow/forbidden/fit-group/figcaption), но: точка
входа — наш `dist/index.html`; `ALLOWED_BG` — не хардкод-сет, а парс `:root` собранного
`tokens.css` (палитра пока идентична в dandelin/buffon, но чужой дек может завести
оверрайд). `build_single.py` (working→delivery split, режет E/A/X regex-якорями) — открытый
вопрос: grep подтвердил, что наш `engine.js` ДЕЙСТВИТЕЛЬНО несёт feedback-tools блок
(`editMode`/`noteMode`/`showReport`: 12 вхождений в dandelin, 6 в buffon) — решения, нужна
ли лектору delivery-копия без них, ещё нет.

**Внешнее.** Ничего для сборки/аудита (Р3, stdlib). Playwright/Pillow — инструменты на
машине автора, не скиллы; в песочнице генератора браузера нет (`README.md` это фиксирует
явно) — `render.py`/аудит гоняются локально у Вани.

**Ловушки.** `audit.py` скилла заточен на браузер и НЕ дублирует наш линтер (сироты
`slide_order`, битые `data-ill`, неопределённые `var`) — оставить оба слоями, не сливать в
монолит. Render-identity нормализованным текстом сильнее скриншот-сверки (тот же DOM на
входе рендереру), но не ловит рантайм-баги (JS-ошибка в `engine.js`, CSS-конфликт
специфичности из арки 8) — для этого нужен именно browser-аудит/глаз, текстовый дифф не
заменяет. Delivery vs working copy — решение не принято (см. next).

---

## Next / чего не хватает для сборки арк-файлов

1. **Арка 7:** не решено — bespoke per-slide грид (`#id .grid{}` в `shablon.html`, текущая
   практика обоих деков) канонизировать как правило, или для GREENFIELD вводить разделяемые
   архетип-классы (`fr-sidebar`/`fr-board`)? В тексте выше — рекомендация в пользу bespoke,
   не подтверждена владельцем.
2. **Арка 8:** не проверено, разносит ли БАЗОВЫЙ (не overlay-патч) слой канона селекторы
   `.reveal`/`.blur-reveal` от общего `[data-scene-from]{opacity:0}` по умолчанию — если
   нет, каждый новый blur-дек должен копировать overlay-фикс руками; решить, переезжает ли
   фикс в стандартный слой `shablon.html`/будущий `base.css` (одна правка на все деки) или
   остаётся per-deck.
3. **Арка 10:** решить нужность delivery-копии без E/A/X для лектора; если да — нужен
   аналог `build_single.py` под наш `engine.js` (свои regex-якоря, не проверялись). Сам
   адаптированный `audit.py` под наш canon физически ещё не написан (только спроектирован
   здесь) — решить путь файла (`_generator/audit.py`? `_studio/tools/`?) при сборке
   арк-файла.
4. Весь материал дистиллята верифицирован на РЕГРЕССИИ (распил Canva-монолитов dandelin/
   buffon), не на GREENFIELD-слайде с нуля — первая реальная проверка сцепки арок 7/8/10 —
   гейт готовности фабрики (собрать «многогранники» end-to-end).
