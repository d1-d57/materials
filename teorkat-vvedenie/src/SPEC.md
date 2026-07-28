# СКЕЛЕТ greenfield-`src/` + `base.css` — контракт и обоснование

> Стартовая папка нового дека Фазы II (шаг 0 «скопируй скелет» / выход раскадровки арки 5).
> Собран заходом `zhurnal/2026-07-10_sborka-konvejera/kod_infra.md` (стык C). Байт-безопасно.
> Канон-base переключён dandelin→buffon заходом `zhurnal/2026-07-10_sborka-konvejera/kod_base-buffon.md` (#13, Р16).

## Состав
```
_generator/skeleton/
  brief.md          манифест-шаблон: пустой slide_order, accent_tag=span, provenance=greenfield
  shablon.html      каркас канона 4 блока + {{BASE_CSS}}; пер-слайдовый грид ПУСТ; SLIDES/ASSETS пусты
  base.css          ОБЩИЙ канон-CSS (структура #stage/.slide/.zone/.fit, сцены, #hint, роли текста
                    t-body/t-display/t-math, .panel/.lab-row/.sim-controls)
  tokens.css        канон-палитра + типо-токены (дословно из buffon, Р16)
  fonts/faces.css   5 @font-face (Forum · Glacial Indifference ×2 · Noto Sans ×2), дословно
  engine.js         движок, ДОСЛОВНО
  content/          пусто (арка 6 → content/<id>.md)          [.gitkeep — генератор глобит *.md, безопасно]
  slides/           отсутствует на диске как пустая → арка 7 создаёт slides/<id>.html
  illustrations/    отсутствует → арка 9 создаёт illustrations/<name>.svg|.html
```
`build_deck.py <skeleton>` на пустом деке проходит линтер (0 слайдов — валидно) и собирает
самодостаточный `dist/index.html`. `slides/` и `illustrations/` НЕ несут keep-файл: генератор
глобит в них `*` и любой файл был бы принят за слайд/иллюстрацию (линтер бы упал). Их создаёт
арка при первом слайде; отсутствие пустой папки генератор терпит (`if folder.is_dir()`).

## `base.css` — что вынесено и откуда граница
Вынесен ОБЩИЙ канон-CSS из `<style>` эталона: сброс `*{box-sizing}`, `#stage`, `.slide/.zone/.fit`,
роли текста (`.t-body/.t-display/.t-math`, `.fill`), каскад сцен `[data-scene-from]`, `deck-in`,
`#hint`, `.panel/.lab-row/.sim-controls`. Граница = комментарий-маркер `/* ---------- сетки
слайдов ---------- */` в `<style>` эталона (в обоих текущих эталонах он идёт непосредственно
перед ПЕРВЫМ пер-слайдовым правилом — не обязательно `.grid{…}`: в buffon перед ним ещё
`#sl-reading a{…}`/`#sl-thanks{…}`/`#sl-title{background:…}`, все они уже bespoke, не base):
всё до маркера — общий base (в `base.css`), всё от него — bespoke грид (остаётся в `<style>`
`shablon.html`, слой арки 7). Механизм: генератор грузит `base.css` опционально (как `overlay.css`)
в плейсхолдер `{{BASE_CSS}}` — добавлена ОДНА строка в `build_deck.py.load_source`.
Лента прогресса (`#lect-zone`/`#lect-progress`) в buffon стилизована ИНЛАЙНОМ на самих `<div>`
(не CSS-правилом в base) — скелет несёт тот же приём дословно (см. `shablon.html`, блок [2]/chrome).

## ⚠ Важное: единого byte-shared `base.css` на ВСЕ деки НЕ существует
ALGORITM §2 предполагал «общий base определяется ОДИН раз, наследуется всеми деками». По живым
`shablon.html` базовые CSS двух эталонов **расходятся по существу канона** (не пробелами):
`.slide{background:#e6e5e1;color:#333}` (dandelin) ↔ `background:var(--paper);color:var(--ink)`
(buffon); `transition:opacity .35s` ↔ `.24s`; разный словарь классов (`.copy/.cer/.tlist/.ph/
.ill-box` ↔ `.t-display/.t-math/.panel/.lab-row/.sim-controls`); фон стейджа `#111` ↔ `#2b3038`.
Один общий byte-shared base воспроизвёл бы оба эталона байт-в-байт только ценой переверстки
одного из них = **рестайл замороженного канона (KONSTITUCIYA §1) — запрещён**.

**Следствие.** Байт-безопасен только ПЕР-ДЕКОВЫЙ `base.css` (каждый дек выносит СВОЙ base в свой
файл — доказано byte-exact на обоих эталонах, `verifikacia-infra.md`). Обещанная выгода «одна
правка base на все деки» пер-дековым выносом НЕ достигается.

**Решено (Р16, заход `kod_base-buffon` #13).** Канон-база скелета — **buffon**: он фактический
стандарт (совпадает с Canva-шаблоном и большинством референсов), а dandelin — первый пробный
эталон, собранный быстро и «разъехавшийся» с остальными. Этот скелет несёт `base.css`/`tokens.css`
= канон-base **buffon** (дословный экстракт из `buffon/src/shablon.html` + `tokens.css`, метод —
см. выше). Дек в стиле dandelin при нужде стартует с иным per-дековым base (тот же принцип: свой
`base.css` в своём `src/`) — это уже не развилка скелета; дефолт закрыт, альтернатива не блокирует.

## Гейт greenfield (1-я сборка — provenance_sha256 нет)
render-identity неприменим на первом деке → замена: **линтер + `audit.py` (браузер) + глаз
(`render.py`)**. render-identity включается со ВТОРОЙ сборки (правка уже собранного дека).
