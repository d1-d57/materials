# Примеры — Вёрстка (шаг 7)

> 🗄 **АРХИВ — конвейер до 27.07.2026.** Файл описывает СТАРЫЙ конвейер: 10 стадий `01-brief`…`10-sborka-qa`,
> реестр `GEJTY.md`, дерево `src/`+`slides/`. **Живой конвейер — фазы Ф1…Ф7**, его
> карта: `../KARTA-ZHIVOGO-KONVEJERA.md` (там же машиночитаемый реестр инструментов §5 и гейт
> согласованности `_generator/tools/check_karty.py`, который краснеет, когда реестр
> и диск разъезжаются). 🔴 **Отсюда НИЧЕГО не удалено:** история решений — единственное,
> чем доказывается «почему так», и стадия может оказаться живой в другом проекте.
> Помечено заходом `karta-kak-reestr` 2026-08-09; гейт согласованности архивные файлы
> не читает вовсе.


> Источник — ЖИВОЙ код `dandelin/` и `buffon/` (два дека, распиленные из Canva-монолитов).
> Все фрагменты ниже — дословные цитаты (путь указан на каждый), не реконструкция по памяти.
> Пути — от корня репозитория (там, где лежат папки `dandelin/`, `buffon/`, `_studio/`).
> Курсивные пометки «канон» / «не канон» — что отсюда переносить на новый слайд, а что нет.

---

## 1. Целый слайд: зоны + `{{MD}}`-слот + рейка иллюстраций

`buffon/src/slides/sl-plan.html` — слайд целиком:

```html
<section class="slide" id="sl-plan" data-scenes="2" data-refs="p-13.jpg,p-13.jpg">
  <div class="grid">
    <div class="zone copy t-body">
      {{MD:sl-plan}}
    </div>
    <div class="rail">
      <div class="panel p1 ill-box" data-ill="rail-needle3"></div>
      <div class="panel p2 ill-box" data-ill="rail-triangle"></div>
      <div class="panel p3 ill-box" data-ill="rail-minisim"></div>
    </div>
  </div>
</section>
```

Грид этого же слайда — `buffon/src/shablon.html`, внутри общего `<style>`, рядом со всеми
остальными `#id .grid` (bespoke-блок точно под `sl-plan`, ничего общего с другими id):

```css
#sl-plan { --t-body: 41px; }
#sl-plan .grid { position: absolute; inset: 0; display: grid;
  grid-template-columns: 20px 1080px 23px 317px; grid-template-rows: 36px 1fr; }
#sl-plan .copy { grid-area: 2 / 2; }
#sl-plan .rail { grid-area: 1 / 4 / 3 / 5; background: var(--board); position: relative; }
#sl-plan .p1 { position: absolute; left: 22px; top: 32px;  width: 274px; height: 187px; }
#sl-plan .p2 { position: absolute; left: 22px; top: 231px; width: 274px; height: 146px; }
#sl-plan .p3 { position: absolute; left: 22px; top: 389px; width: 274px; height: 401px; }
```

Разбор зон (что здесь канон):
- **`#sl-plan{--t-body:41px}`** — кегль тела ВЫБРАН для этого конкретного слайда один раз,
  до вёрстки (у `sl-buffon` рядом на той же странице — `36px`, у `sl-vizitka` — `38px`, у
  `sl-count`/`sl-circle` — `41px`: разброс 32–41px по всему деку — это диапазон осознанного
  выбора кегля, НЕ дрейф и не патч overflow; см. §2 про разницу между «выбрать» и «уменьшить».)
- **`.grid{position:absolute;inset:0;display:grid;grid-template-columns:20px 1080px 23px 317px;…}`**
  — колонки в px (20+1080+23+317=1440 ровно), **bespoke точно под `#sl-plan`**, не общий
  класс вроде `.fr-sidebar`. Это и есть решение «bespoke-грид» из `DOK.md`.
- **`.copy{grid-area:2/2}`** — текстовая зона: НЕТ `.fit`, нет паддинга (верхний отступ —
  через `36px` строку грида, а не через CSS `padding` зоны).
- **`.rail{grid-area:1/4/3/5;background:var(--board)}`** — иллюстрационная колонка шириной
  317/1440 = **22.0%W** — близко к архетипу «сайдбар 25%W» из таблицы `DOK.md` (см. §4);
  фон СТРОГО `var(--board)`, ни одного произвольного цвета.
- **`.p1/.p2/.p3`** — три панели рейки, абсолютные координаты внутри `.rail`
  (`position:relative` на родителе), числа — промер оригинального кадра Canva. На
  greenfield-слайде (без оригинала) числа берутся из объёма/пропорций самой иллюстрации,
  не из промера — механика позиционирования (abs внутри `position:relative` рейки) та же.
- **`data-refs="p-13.jpg,p-13.jpg"` и `data-scenes="2"`** — `data-scenes` канон (нужен
  всегда, даже 1). `data-refs` — **НЕ канон для greenfield**: это provenance регрессии
  (какой Canva-кадр сверять на какой сцене), пишется только когда есть оригинал для сверки.
  Не копировать по умолчанию на новый слайд без оригинала.

---

## 2. `.fit` + `data-max` (display-роль) vs фиксированный `--t-body` (body-роль)

**Display-роль — `.fit`, без паддинга.** `dandelin/src/slides/s05c.html`:

```html
<section class="slide" id="s05c" data-scenes="1">
  <div class="grid">
    <div class="zone covertitle"><div class="fit cer" data-max="64">Оптические свойства</div></div>
    <div class="coverframe"><div class="ill-box" data-ill="optics-caustic"></div></div>
  </div>
</section>
```
Грид (`dandelin/src/shablon.html`):
```css
#s05c .grid{ grid-template-columns:1fr; grid-template-rows:152px 1fr; background:var(--board); padding:0; }
#s05c .covertitle{ grid-row:1; align-self:center; justify-self:center; width:80%; }
#s05c .cer{ text-align:center; }
```
`.covertitle` — зона БЕЗ единого px паддинга; центрирование идёт через `align-self`/
`justify-self`/`width:80%`, не через `padding`. Внутри — `.fit.cer[data-max=64]`: заголовок
без явного `font-size`, кегль находит движок бинарным поиском (см. ниже).

**Body-роль — фиксированный `--t-body`, без `.fit`.** Тот же `sl-plan` из §1:
`#sl-plan{--t-body:41px}` + `<div class="zone copy t-body">{{MD:sl-plan}}</div>` — здесь
кегль — **застывшая константа**, ни разу не пересчитывается в рантайме.

**Почему их нельзя перепутать — механика фиттера.** `dandelin/src/engine.js` (блок `[4]`,
не редактируется, но полезно понимать, что он делает):
```js
function fitText(el) {
  const zone = el.closest('.zone');
  if (!zone) return;
  const maxS = parseFloat(el.dataset.max) || 200;
  const minS = parseFloat(el.dataset.min) || 12;
  let lo = minS, hi = maxS;
  const fits = () => el.scrollWidth <= zone.clientWidth &&
                     el.scrollHeight <= zone.clientHeight;
  for (let i = 0; i < 22; i++) {
    const mid = (lo + hi) / 2;
    el.style.fontSize = mid + 'px';
    if (fits()) lo = mid; else hi = mid;
  }
  el.style.fontSize = Math.floor(lo) + 'px';
}
```
`.fit` ищет ближайшую к `data-max` величину, которая не переполняет `.closest('.zone')` —
бинарным поиском по `scrollWidth/scrollHeight` против `zone.clientWidth/clientHeight`.
`--t-body` в этот код вообще не попадает: body-текст `.fit`-класс не носит, значит для него
фиттер не вызывается никогда — «никогда не фитится» в `DOK.md` буквально значит «не имеет
класса `.fit`», а не «недостаточно ужат руками». `data-max` в реальных слайдах — 64/84/100
(`s05c`/`s00`/`s11`); `data-min` в коде поддержан (дефолт 12), но в обоих деках нигде не
задан явно — на практике авторы полагаются на дефолт.

---

## 3. `.zone.pad` (dandelin) и правило «нет паддинга там, где `.fit`»

**Зона с паддингом — только фиксированный body, `.fit` внутри нет.**
`dandelin/src/slides/s01.html` / `s02.html`:
```html
<div class="zone pad"><div class="copy">{{MD:s01}}</div></div>
```
Утилита (`dandelin/src/shablon.html`, общий слой, не per-id):
```css
.pad{ padding:46px 56px 0 56px; }                 /* text inset: top-left gravity */
```
`.pad` слит с `.zone` прямо в атрибуте класса (`class="zone pad"`) — паддинг здесь безопасен,
потому что `.copy` не содержит `.fit`: ничего не читает `zone.clientWidth/clientHeight`, чтобы
посчитать себе размер, значит "лишние" 46/56px внутри `clientWidth` никого не обманывают.

**Зона с `.fit` — паддинга нет.** `#s05c .covertitle` из §2 (`grid-row:1; align-self:center;
justify-self:center; width:80%` — ни одного свойства `padding`) — тот же приём, что и в
`.grid{padding:0}` на этом слайде.

**Почему это правило, а не вкусовщина.** `fitText()` (см. §2) меряет `zone.clientWidth` —
а `clientWidth` ВКЛЮЧАЕТ паддинг зоны. Если зона несёт и паддинг, и `.fit`-ребёнка, бинарный
поиск считает доступным пространством ВЕСЬ `clientWidth` (с паддингом внутри), хотя реальное
место для текста — на паддинг меньше; результат — `.fit`-текст наезжает на паддинг-буфер,
который для того и заводился, чтобы текст туда не заходил. Отсюда правило `DOK.md`: паддинг —
только на зоны БЕЗ `.fit`, для зон с `.fit` — центрирование через `align-self`/`justify-self`/
`width:%`/`grid-template`, никогда `padding`.

**Живое исключение, НЕ образец.** `dandelin/src/shablon.html`:
```css
#s11 .card{ grid-area:2/2; background:transparent; display:grid; place-items:center;
            grid-template-rows:auto auto; row-gap:20px; padding:48px; }
```
— зона `.card` (= `.zone.card` на слайде `s11`) несёт И `padding:48px`, И `.fit.cer` внутри.
Это единственное найденное отклонение от правила выше во всём просмотренном коде; скорее
всего сходит с рук из-за короткого текста («Спасибо за внимание») и большого запаса места —
не потому что паддинг+`.fit` в принципе безопасны. **Не копировать эту комбинацию на новый
слайд** — ориентир для новой вёрстки строго `#s05c` (паддинг=0 там, где есть `.fit`).

---

## 4. Архетип из таблицы `DOK.md` на реальном слайде

Таблица (`DOK.md`, дословно): «сайдбар 25%W · рейка 74%W · плашка 15/19.5%H · доска-полоса
44%H — статистика Canva-корпуса из `decks/02-buffon.md`». Ниже — реальные числа рядом с
табличными, чтобы увидеть: таблица — ориентир поиска архетипа, не CSS для копипаста
(дословно так и написано в `DOK.md`, §«Ловушки»).

**Сайдбар/рейка — семья узкая-иллюстрация-колонка + широкий-текст.** Три слайда одного
архетипа в `buffon/src/shablon.html`, у каждого своя точная пропорция:

| слайд | текст (`.copy`), px/1440 | илл.-колонка (`.rail`), px/1440 |
|---|---|---|
| `#sl-plan` | 1080 → 75.0%W | 317 → 22.0%W |
| `#sl-polygons` | 1098 → 76.25%W | 315 → 21.9%W |
| `#sl-result` | 1056 → 73.3%W | 316 → 21.9%W |

Табличные 74%/25% — среднее по корпусу; каждый реальный слайд выше в пределах ±2–3 п.п. от
него, но ни один не равен ему ровно. Разница — это и есть «не копипаст»: ширина рейки в
каждом случае подогнана под РЕАЛЬНЫЙ размер иллюстраций этого слайда, не взята из таблицы.

**Плашка/доска-полоса — семья узкий-верх + широкий-board.** `dandelin/src/shablon.html`:

| слайд | верхняя зона, %H | нижняя (board), %H | заметка |
|---|---|---|---|
| `#s04` | 25% | 75% | комментарий в файле зовёт её «top plaque 15%H» — комментарий устарел, реальное число 25% |
| `#s05` | 23% | 77% | тот же архетип, другой слайд — 23%, не 25% |
| `#s09b` | 24% | 76% | тот же архетип — ещё одно третье число, 24% |
| `#s06` | 44% | 56% | верхняя зона (текст, не board!) — единственное точное попадание в табличные «44%H», но это текстовая зона, а табличное имя — «доска-полоса» |

Вывод для вёрстки нового слайда: искать архетип по таблице («у меня узкий верх + широкий
board — это семья `s04/s05/s09b`»), затем МЕРИТЬ реальный объём текста/иллюстрации ЭТОГО
слайда и ставить своё число (23–25%, а не обязательно табличное). Слепой перенос табличного
процента без проверки — ловушка, которую поймает только глаз (см. `ZAHOD.md` §3, гейт).

**Вложенный грид с защитой от коллапса (ближайший живой аналог `minmax(0,1fr)`).**
`dandelin/src/shablon.html`:
```css
#s05 .spics{ display:grid; grid-template-rows:1fr 1fr; gap:13px; padding:10px 18px 12px 2px; min-height:0; }
```
Буквального `minmax(0,1fr)` в обоих деках нет ни разу (проверено grep'ом) — `DOK.md` сам
помечает это правило как непроверенное на greenfield. `#s05 .spics` — ближайший реальный
пример той же идеи: `fr`-доли для рядов вложенного грида + `min-height:0`, чтобы ряд не
раздулся под контент. При вводе НОВОГО вложенного грида с рядом переменной высоты —
использовать `minmax(0,1fr)` или это же `min-height:0`-подстраховку, не голый `auto`.

---

## 5. Что НЕ повторять (антипаттерн, найден в живом коде)

`buffon/src/tokens.css` + `buffon/src/shablon.html`:
```css
/* tokens.css */
--t-body: 38px;   /* тело НИКОГДА не автофитится; на слайде может быть свой кегль (промер) */
--t-small: 30px;
/* shablon.html — база */
.t-small { font-size: var(--t-small); }
/* shablon.html — переопределение на конкретном слайде */
#sl-result .t-small { font-size: 26px; }  /* примечание про выпуклый контур: кегль 26, шаг 40 (промер) */
```
Это **не** нарушение «`--t-body` никогда не уменьшать» — `.t-small`/`--t-small` здесь
самостоятельная типографическая роль (сноска/примечание рядом с основным текстом слайда,
как `--t-caption`), а не тот же самый абзац `.copy`, ужатый ради overflow. Урок для вёрстки:
если нужна ВТОРАЯ, заведомо более мелкая роль (подпись/сноска) — заводится отдельно как своя
роль с самого начала слайда, а не как патч поверх переполнившегося `--t-body`. Если во время
вёрстки чешутся руки добавить `.t-small`/уменьшить кегль ИМЕННО у `.copy`, чтобы победить
overflow — это и есть запрещённый приём; правильный порядок починки — `ZAHOD.md` §3.

**Важная оговорка (проверено `overlay.css`):** в живом рендере буффона `#sl-result .t-small{font-size:26px}` выше сегодня фактически мёртвый код — `buffon/src/overlay.css:36` несёт `.t-small{font-size:var(--t-body,38px)!important}` (комментарий автора «не кустарно»), и этот `!important` бьёт более специфичный, но не-`!important` селектор из `shablon.html`; итоговый размер `.t-small` везде равен `--t-body`. Токен/роль `--t-small:30px` в коде остаются, просто нейтрализованы этим оверрайдом. У dandelin ни токена, ни оверрайда нет вовсе — greenfield-дек, скопировавший только базовый паттерн `tokens.css`+`shablon.html` без `overlay.css`-нейтрализации, получит РЕАЛЬНО уменьшенный `.t-small`.

---

## Якоря (если нужно свериться глубже)
- `DOK.md`, `../FORMAT-ISTOCHNIKA.md` — контракты, которые этот файл иллюстрирует.
- `../../../dandelin/src/shablon.html`, `../../../buffon/src/shablon.html` — полные гриды
  (десятки `#id .grid`, здесь процитирована только часть).
- `../../../dandelin/src/engine.js` (блок `[4]`) — `fitText`/`fitAll`/`measureGroups`
  (строки 13–50 на момент написания).
- `../../../_generator/{build_deck.py,render.py}` — точный CLI (см. `ZAHOD.md` §3).
