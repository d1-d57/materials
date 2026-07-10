---
id: buffon
title: "Игла Бюффона"
canvas: 1440x810
provenance: materials/buffon/index.html
provenance_sha256: c0c9b846fd040eb1755d66de10fd5609e51cc050cd2ddc59848b99f767d13d19
milestone: 1 (дословный распил; текст слайдов пока HTML, markdown — M2)
accent_tag: span
slide_order:
  - sl-title
  - sl-vizitka
  - sl-buffon
  - sl-sim
  - sl-convergence
  - sl-coin
  - sl-interval
  - sl-divider1
  - sl-plan
  - sl-yellow
  - sl-count
  - sl-prob
  - sl-polygons
  - sl-circle
  - sl-result
  - sl-divider2
  - sl-grid
  - sl-coords
  - sl-condition
  - sl-phase
  - sl-area
  - sl-reading
  - sl-thanks
---

# buffon — источник (Milestone 1)

Раскроено дословно из `materials/buffon/index.html` (см. `provenance_sha256`);
пересборка `build_deck.py`-ом **байт-в-байт** совпадает с оригиналом
(`cmp` exit 0, sha256 совпадает) при `--no-banner`.

**Текст (Milestone 1).** Все 23 секции — дословный HTML в `slides/sl-*.html`
(никакого markdown ещё; это Milestone 2). Слот `{{SLIDE:sl-NAME}}` в `shablon.html`
резолвится в целую `<section class="slide" id="sl-NAME">…</section>`, включая
собственные атрибуты (`data-scenes`, `data-refs`).

## Слайды
23 секции, порядок — см. `slide_order` выше. Без 3D, без `data-skip`
(в отличие от Dandelin) — все 23 показываются в деке.

## Иллюстрации (`illustrations/`) — 18 шаблонов `<template id="ill-*">`
- **`.svg`** (13): `rail-needle3`, `rail-triangle`, `rail-minisim`, `prob-2p`,
  `sl-interval-1`, `sl-divider1-1`, `sl-grid-coins`, `sl-grid-frame`,
  `sl-grid-circle`, `sl-coords-1`, `sl-area-1`, `sl-area-2` — инлайн-векторная
  графика (часть многострочная, с отступами — не однострочный минифайл).
- **`.html`** (5, растр `<img src="data:…base64">`): `title-art`, `portrait`,
  `needles`, `vizitka-photo`, `vizitka-qr`, `sl-divider2-1`.

**Известный инвариант оригинала (не баг разбора):** 16 из 18 шаблонов
используются (`data-ill="NAME"` в слайдах); `sl-area-1` и `sl-area-2` — мёртвые
неиспользуемые заготовки в реестре ассетов самого оригинала (мягкое
предупреждение линтера). Один инлайн-SVG (`.thx-art`) живёт прямо в
`slides/sl-thanks.html`, а не в `illustrations/` — как и в Dandelin.

## Симуляции (`sims/`) — фреймворк `lab.js` (SIM-DESIGN.md в оригинале)
- `sims/lab.core.js` — ядро (`window.LabKinds`, `window.LabCore`): определяет
  базовые kind'ы `needles`, `yellow`, `coords-needles`, `coords-phase` и
  инфраструктуру канваса/панели.
- `sims/ext/*.js` (9 модулей) — каждый нёс в оригинале собственный
  самодокументирующий комментарий `/* === lab-ext/NAME.js (вшито сборкой) === */`,
  поэтому имена не гадаются, а взяты из исходника: `convergence`, `coin`, `prob`,
  `polygons`, `circle`, `result`, `phase-mass`, `title-breath`, `cos-area`.
  (`title-breath` не привязан ни к одному `canvas[data-sim]` — анимирует титульный
  арт напрямую через DOM, это не баг подсчёта.)
- Итого 13 `<canvas data-sim="KIND">` в слайдах, из них `phase-mass` встречается
  дважды (`sl-condition` и `sl-phase`) — один и тот же kind, два канваса.

## KaTeX — предвычислен, БЕЗ рантайма
Математика во всех слайдах — уже статический `<span class="katex">…</span>`
(проверено: 0 `<script>` с katex.js/CDN). Стили и шрифты для него — НЕ в
`fonts/faces.css` (там только 5 дек-шрифтов: Forum, Glacial Indifference ×2,
Noto Sans ×2), а в отдельном **`overlay.css`**:

## `overlay.css` — второй `<style id="canon-overlay">` (не часть блока [1])
Важное открытие разбора: в оригинале это ОТДЕЛЬНЫЙ `<style>`-элемент (со своим
id), физически идущий ПОСЛЕ `</style>` блока [1] DECK STYLES, а не его хвост —
между дек-шрифтами (строки ~18–22 ориг.) и KaTeX-шрифтами (строки ~371–377
ориг.) лежат ~350 строк обычного per-slide CSS. Так как `{{FONTS_CSS}}` и
`{{TOKENS_CSS}}` — каждый один непрерывный кусок в контракте `build_deck.py`, а
KaTeX-блок физически не смежен с дек-шрифтами, склеивать их в один файл/токен
значило бы либо двигать байты (ломает byte-exact), либо городить сплит одного
файла на два токена (сложнее генератора). Вместо этого `overlay.css` вшит как
ОДИН дословный блок — это готовая точка расширения из `_generator/DESIGN.md`
§4/§5 (`overlay.css` — «canon-overlay, опц., дословно»), которую Dandelin просто
не использовал. Содержимое одним куском: 7 `@font-face` KaTeX (Main/Math/Size1/
Size2/AMS), базовые `.katex{…}` классы, и мелкие деко-патчи (`--accent`,
`.blur-reveal`, точечные `#sl-*` override'ы) — не расщеплялось дальше
(«сомнительное — дословно»).

## Движок / шрифты / токены
- `engine.js` — блок `[4] ENGINE`, дословно, включая маркеры
  `/* ===== [4] ENGINE — канонический из deck-skeleton.html ===== */` …
  `/* ===== /ENGINE ===== */` (комментарий в оригинале про «патч prev()» —
  решение автора движка, не тронуто при распиле).
- `fonts/faces.css` — 5 правил `@font-face` (дек), base64 woff2, дословно.
- `tokens.css` — единственный основной блок `:root{…}` (палитра + типографика).
  Второй, маленький `:root{--accent:#785a18}` патч (комментарий в оригинале:
  «переменная не была определена в деке») остаётся ВНУТРИ `overlay.css` как
  часть его единого дословного блока — не вынесен в `tokens.css`.
- Нет `lib/three.min.js` — Buffon не использует 3D/three.js.

## Что НЕ вынесено (осталось буквальным текстом в `shablon.html`)
Базовый/грид CSS внутри `<style>` (структура канона + ~340 строк per-slide
грид-раскладок), doctype/head/body-обвязка, `#stage`/`#deck` chrome,
пост-engine скрипт (лента прогресса лекции по hash) — не входят в контракт
Milestone 1 и не мешают byte-exact пересборке.

## Milestone 2 — ВЫПОЛНЕН (вся проза в md)

Все 17 прозаических слайдов вынесены в `content/*.md` целиком (`inline<p>=0` в каждом
каркасе); обе колоды render-идентичны оригиналам по нормализованной сверке. 6 структурных
слайдов (`sl-title`, `sl-divider1`, `sl-divider2`, `sl-sim`, `sl-phase`, `sl-thanks`) прозы
для выноса не имеют — короткие подписи инлайн, как у Dandelin.

`render_md`/`render_inline_md` сейчас умеет: абзацный тег `{@N}`/`{@N-M}`/`{.cls}` (атрибуты
на `<p>` в порядке токенов), инлайн `{@N| …}`, шторки `{fill@N|…|…}` и `{blur@N|…}`,
`**acc**`→`<span class="acc">` (тег из `accent_tag`), `$tex$` из кэша `math/katex.json`,
класс списка через `{.cls}` над блоком `- `. Сырой HTML проходит как есть — escape-hatch
для нестандартного (напр. `fill-q` и вложенный fill-с-blur в `sl-polygons`). Справочник —
`_generator/SLIDE-FORMAT.md`.
