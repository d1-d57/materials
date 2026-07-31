#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сборка src/overlay.css — второго <style> дека (опц. модуль формата, FORMAT-ISTOCHNIKA).

  python3 teorkat-vvedenie/src/tools/sobrat_overlay.py

Три слоя, каждый заведён по названной причине, а не «на всякий случай»:

 [1] KaTeX-CSS + ЕГО ШРИФТЫ base64. Иначе рендер формул из math/katex.json — набор
     несостыкованных <span>, а требование «0 внешних asset-URL» (линтер, пункт 4)
     запрещает ссылаться на woff2 файлом. Приём дословно буффоновский
     (`buffon/src/overlay.css` несёт KaTeX_Main тем же способом), но шрифты берутся
     не из буффона, а из самого KaTeX, которым отрендерен кэш — иначе подмножество
     глифов может не совпасть с формулами ЭТОГО дека.
     @font-face КаTeX'а переписываются: остаётся один src — data:font/woff2.

 [2] СЛОВАРЬ ПРИМИТИВОВ `s-*` — 43 иллюстрации ленты стилизованы классами, которые
     определены в `_generator/build_doc.py` (документ-вид) и в деке не существуют.
     `<circle>` без fill падает в чёрный ТИХО, а гейт G10 этого не видит: он ищет
     `var(--x)`, а здесь классы. Цвета — ТОЛЬКО токены дека (`tokens.css`).

 [3] Роли, которых нет в канон-базе: `.tlist` (её эмитит render_md), `.acc`
     (accent_tag: span), `.formula`, опорные точки Р23, плейсхолдер портрета,
     blur-reveal, и каскад сцен до 9 — база обрывает его на `.scene-5` (это ровно
     урок 8 / гейт G15), поэтому каскад ГЕНЕРИРУЕТСЯ, а не выписывается.
"""
import re, base64, sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
KATEX = REPO / "lsh-2026-perechislitelnaya/otkrytaya-lekcia-paskal/src/tools/node_modules/katex/dist"
MAX_SCENES = 9      # предел каскада движка (08-sceny/DOK.md)

# ── [1] KaTeX ──
css = (KATEX / "katex.min.css").read_text(encoding="utf-8")
faces = re.findall(r"@font-face\{.*?\}", css, re.S)
css_body = re.sub(r"@font-face\{.*?\}", "", css, flags=re.S).strip()

out_faces, embedded, missing = [], 0, []
for face in faces:
    fam = re.search(r"font-family:([^;}]+)", face).group(1)
    style = re.search(r"font-style:([^;}]+)", face)
    weight = re.search(r"font-weight:([^;}]+)", face)
    woff2 = re.search(r"url\(([^)]*?\.woff2)\)", face)
    if not woff2:
        missing.append(fam)
        continue
    fp = (KATEX / woff2.group(1).strip('"\'')).resolve()
    if not fp.is_file():
        missing.append(str(fp))
        continue
    b64 = base64.b64encode(fp.read_bytes()).decode("ascii")
    embedded += 1
    out_faces.append(
        "@font-face{font-family:%s;font-style:%s;font-weight:%s;font-display:block;"
        "src:url(data:font/woff2;base64,%s) format('woff2')}"
        % (fam, style.group(1) if style else "normal",
           weight.group(1) if weight else "normal", b64))

# ── [3] каскад сцен, порождённый ──
# 🔴 В набор сцен добавлена 99. Это не запас «на всякий случай», а долг инструмента:
# `_generator/render.py:29` снимает кадр как `?only=N&scene=99` с комментарием
# «scene=99 → показать слайд в финальной сцене», а движок (`engine.js applyScene`)
# раскрывает сцены КЛАССОМ `.scene-K`, и канон-каскад идёт до `.scene-5`. Класса
# `.scene-99` не существует ни в одном деке ⇒ на снятом PNG слайд со сценами
# показан в ПЕРВОЙ сцене, а не в финальной. Поймано глазом: на кадрах s04/s07/s11
# стояли пустые маркеры списка вместо пунктов. Лечится либо в render.py, либо в
# движке; здесь — пер-дековая заплата, чтобы зрительная петля вообще работала.
SCENES = list(range(1, MAX_SCENES + 1)) + [99]

# 🔴 Каскад `from` порождается с J=1, а НЕ с J=2, и это не запас — это починка
# молчаливой потери 49 абзацев ленты. `base.css:32` прячет ВСЁ, что несёт
# `data-scene-from`, а раскрывает только этот каскад. Канон-каскад начинался с
# J=2, потому что «сцена 1 — это то, что видно сразу, тега не несёт». Но лента
# Л1 несёт `{@1-1}`/`{@1-2}`/`{@1-3}` (49 вхождений): там тег на сцене 1 стоит
# не ради появления, а ради того, чтобы блок потом УШЁЛ. `_attrs_from_tag`
# (`build_deck.py:83-88`) единицу не исключает и честно пишет
# `data-scene-from="1"` — а раскрыть её было нечем, и абзац не показывался НИ В
# ОДНОЙ сцене. Гейты молчат все: html валиден, overflow не растёт, линтер и
# --scene-diff зелёные.
def _cascade(sel):
    return ",\n".join(sel % (n, k) for n in SCENES
                      for k in range(1, (MAX_SCENES if n == 99 else n) + 1))


cascade_layout = _cascade(".scene-%d [data-scene-from=\"%d\"]")
cascade_blur = _cascade(".scene-%d .blur-reveal[data-reveal=\"%d\"]")

# 🔴 Семантика УХОДА: элемент виден НА своей последней сцене и гаснет ПОСЛЕ неё.
# `engine.js:57` ставит `scene-off` по условию `k >= until`, то есть гасит НА
# сцене `until`. Лента же называет свою семантику вслух (шапка `A-krasivaya.md`:
# «`{@N-M}` — приходит на N-й и УХОДИТ ПОСЛЕ M-й»; пометка раскладки s17:
# «вопрос стоит на сценах 1–2» при теге `{@1-2}`, «определение ретракта доживает
# до сцены 5» при теге `{@4-5}`). Разница в одну сцену безобидна не была: при
# `{@K-K}` сцена включения и сцена выключения совпадают, и 30 блоков гасли ровно
# там, где должны были появиться, — то есть не показывались никогда.
# Правится ТОЛЬКО здесь: `_generator/` и `engine.js` не мои. `!important`
# обязателен — бьёмся с `.scene-off{opacity:0!important}` (`base.css:22`) при
# равной специфичности. `.scene-99` в семью НЕ входит осознанно: «сцена 99» —
# это состояние «ушло всё сменное», и оно не равно финальной сцене слайда,
# поэтому кадры снимаются по сценам 1..data-scenes, а не через ?scene=99.
cascade_until = ",\n".join(
    ".scene-%d [data-scene-until=\"%d\"]" % (n, n)
    for n in range(1, MAX_SCENES + 1))

# ── 🔴 ПЕРЕТЕКАНИЕ ПО СЦЕНАМ ДЛЯ ТЕКСТА В ПОТОКЕ ──────────────────────────────
# Это самое крупное отступление захода от канона, и оно вынужденное. Канон
# (`08-sceny/DOK.md`) требует раскрывать сцены «через opacity+visibility, НИКОГДА
# display». Под этим правилом вне-сценовый абзац СОХРАНЯЕТ свой блок в потоке:
# `visibility:hidden` прячет краску, но место занимает. Значит зона обязана вместить
# ВЕСЬ текст слайда одновременно, сколько бы сцен он ни имел, — а `.zone` несёт
# `overflow:hidden` (`base.css:7`), то есть лишнее просто обрезается МОЛЧА.
#
# На деке из 55 слайдов это не мешало: сцены были у 4 слайдов и работали накоплением.
# На ленте из 32 слайдов мешает фатально. Промер по собранному деку: переполнено 19
# зон из 32, максимум +1817px при зоне 766px — слайду `s13` нужно 3,4 своей зоны.
# Ни ступень (их 7), ни кегль (пол 35px по `audit.py`) не дают трёхкратного запаса:
# лекция из 32 слайдов под правилом «никогда display» НЕ СОБИРАЕТСЯ вообще, и это
# не вопрос подгонки.
#
# Поэтому вне-сценовый текст ПЕРЕСТАЁТ занимать место — но только текст В ПОТОКЕ
# (`p`, `ul` внутри зоны). Панели иллюстраций позиционированы абсолютно, на поток не
# влияют и остаются на opacity/visibility: у них сохраняется плавное появление и
# синхронность с текстом (гейт сцен 4), которую канон требует отдельно.
# Что при этом теряется честно: у абзаца больше нет перехода `opacity .24s` — он
# появляется мгновенно. Что приобретается: слайд вообще возможен.
FLOW = "p,ul"


# 🔴 Перетекание включается ПОСЛАЙДОВО, а не по всему деку. Канон («никогда
# display») нарушается только там, где иначе слайд физически не собирается, — и
# число таких слайдов называется. Остальные держат канон дословно: вне-сценовый
# абзац сохраняет своё место, и при клике не двигается НИЧЕГО (гейт сцен 6,
# «геометрия заморожена»). Цена перетекания измерена и она реальна: на слайде с
# заменой блок, видимый в обеих сценах, съезжает вверх на освободившееся место —
# до 574px. Поэтому платим эту цену ровно там, где выбора нет.
# Кто помечен — решает `podognat.py --potok`: слайд, у которого при замороженной
# геометрии зона переполнена. Метку пишет `sverstat.py` в `slides/<id>.html`.
POTOK = '.slide[data-flow="reflow"]'


def _flow(sel_tail):
    return ",\n".join("%s %s" % (POTOK, s) for s in sel_tail)


cascade_flow_show = ",\n".join(
    '.slide.scene-%d[data-flow="reflow"] .zone %s[data-scene-from="%d"]' % (n, tag, k)
    for n in SCENES
    for k in range(1, (MAX_SCENES if n == 99 else n) + 1)
    for tag in FLOW.split(","))
cascade_flow_hide = _flow([".zone %s[data-scene-from]" % t for t in FLOW.split(",")])
# ушедший блок тоже покидает поток — иначе замена не освобождает ни пикселя
cascade_flow_off = _flow([".zone %s.scene-off" % t for t in FLOW.split(",")])
# …но НА своей последней сцене он ещё стоит (та же поправка «уходит ПОСЛЕ M»)
cascade_flow_until = ",\n".join(
    '.slide.scene-%d[data-flow="reflow"] .zone %s[data-scene-until="%d"]' % (n, tag, n)
    for n in range(1, MAX_SCENES + 1)
    for tag in FLOW.split(","))
# маркер пункта прячется ВМЕСТЕ со своим пунктом. Без этого на слайде до клика
# висят пустые квадратики-засечки: `{@N|…}` скрывает СОДЕРЖИМОЕ <li>, а `::before`
# принадлежит самому <li> и остаётся видимым (тоже поймано глазом на s04).
cascade_marker = _cascade(
    ".scene-%d .tlist li:has(> [data-scene-from=\"%d\"])::before")

DECK_LAYER = """
/* ============================================================================
   [2] СЛОВАРЬ ПРИМИТИВОВ ИЛЛЮСТРАЦИЙ (s-*) — перенос из _generator/build_doc.py
   в палитру дека. Соответствие вар документа → токен дека:
     --text → --ink · --muted → --steel · --accent → --brick
     --shade → --board · --warm → --mustard · --sans → 'Noto Sans'
   Ни одного произвольного цвета: всё через var() из tokens.css (гейт G8/G10).
   ============================================================================ */
.s-line{fill:none;stroke:var(--ink);stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.s-thin{fill:none;stroke:var(--steel-d);stroke-width:1.2}
.s-dash{fill:none;stroke:var(--brick);stroke-width:1.3;stroke-dasharray:4 4}
.s-accent{fill:none;stroke:var(--brick);stroke-width:2.4;stroke-linejoin:round;stroke-linecap:round}
.s-fillw{fill:var(--mustard)}
.s-fillsh{fill:var(--board)}
/* полый узел — НЕ чистый белый: рисунок лежит на доске, и `--card` там читался
   наклейкой (словарь примитивов, §ФОН РИСУНКА, две правки палитры) */
.s-node{fill:var(--hollow);stroke:var(--ink);stroke-width:1.8}
.s-node-r{fill:var(--ink)}
.s-node-a{fill:var(--brick);stroke:var(--brick)}
/* ЦВЕТНОЙ УЗЕЛ — три цвета, которыми различаются ЭЛЕМЕНТЫ (не состояние узла).
   Заведён 31.07 под заказ владельца на «Примерах»: «просто три цвета, слева три
   элемента и справа такие же, и показывать, как мы переставляем объекты». Цвет
   несёт тождество элемента, поэтому это НЕ `.s-node-r/-a` (те про роль: «о нём
   речь» / «акцент»).
   🔴 В ФИГУРЕ ПИСАТЬ ПАРОЙ: `class="s-node s-node-c1"`. Причина ровно та ловушка
   словаря, что уже стоила девяти ненарисованных стрелок: doc-вид красится
   `_generator/build_doc.py`, где этих классов нет и завести их нельзя (файл вне
   зоны лекции). Базовый `.s-node` даёт fill/stroke в ОБОИХ носителях, а `.s-node-cN`
   в деке перебивает заливку позже по каскаду при равной специфичности — значит
   худшее, что бывает при отсутствии класса, это полый узел, а не тихая чернота. */
.s-node-c1{fill:var(--p1);stroke:var(--p1)}
.s-node-c2{fill:var(--p2);stroke:var(--p2)}
.s-node-c3{fill:var(--p3);stroke:var(--p3)}
.s-txt{font-family:'Noto Sans',sans-serif;font-size:13px;fill:var(--ink)}
.s-txt-w{font-family:'Noto Sans',sans-serif;font-size:13px;fill:var(--card);font-weight:600}
.s-txt-m{font-family:'Noto Sans',sans-serif;font-size:12px;fill:var(--steel)}
.s-ar-a{fill:var(--brick)}
/* наконечник служебной стрелки темнеет вместе с `.s-thin` — та же правка палитры */
.s-ar-m{fill:var(--steel-d)}
/* SVG обязан вписаться в бокс, иначе audit.py: «inline SVG fits its box» = FAIL.
   Атрибут width="250" у фигур ленты бьётся правилом .ill-box>svg из base.css;
   здесь добавлено только preserveAspectRatio-поведение через object-fit-аналог. */
.ill-box{position:relative;overflow:hidden}
.ill-box > svg{width:100%;height:100%;display:block}

/* ============================================================================
   [3] РОЛИ, КОТОРЫХ НЕТ В КАНОН-БАЗЕ
   ============================================================================ */
/* акцент: accent_tag=span, то есть **x** → <span class="acc">x</span>.
   Канон — «Bold + один охряный .acc»; охра берётся токеном --mustard,
   нового цвета не заводится. */
.acc{font-weight:700;color:var(--mustard)}
.acc .katex,.acc .katex *{color:var(--mustard)}

/* ── БЛОЧНЫЙ РИТМ: ОДИН промежуток между блоками, ноль внутри ──
   База даёт `p + p{margin-top:calc(1em*var(--lh))}`, то есть промежуток = ПОЛНАЯ
   пустая строка (58px при кегле 38). У слайда с девятью блоками одни промежутки
   съедают 428px из 740 — половину зоны. Канон-лечение уже оплачено буффоном
   (`overlay.css:45`: «единое значение вместо пер-слайдовых костылей → текст
   ложится регулярно, и плотнее, поэтому тело 38px помещается без уменьшения
   шрифта»). Здесь то же одним рычагом --blok; --t-body при этом НЕ тронут. */
.t-body{--blok:26px}
.t-body p + p{margin-top:var(--blok)}
.t-body ul.tlist{margin-top:var(--blok)}
.t-body ul.tlist + p{margin-top:var(--blok)}

/* список: render_md эмитит <ul class="tlist">; маркер — квадратная засечка
   (канон-паттерн dandelin, .tlist li::before), цвет — стальной токен. */
.tlist{list-style:none}
.tlist li{position:relative;padding-left:1.15em}
.tlist li + li{margin-top:10px}
.tlist li::before{content:'';position:absolute;left:0;top:.58em;
  width:.3em;height:.3em;background:var(--steel)}

/* формула абзацем: КРУПНЕЕ тела — это результат, а не строка потока.
   Уменьшением тела это не является: --t-body не тронут (гейт G8). */
.formula{text-align:center}
.t-body p.formula{margin-top:var(--blok)}
.t-body p.formula + p{margin-top:var(--blok)}
.formula .katex{font-size:1.1em}
/* Канон: «Формулу НЕ разрывать переносом строки — переносится соседнее слово,
   не формула». KaTeX сам ставит `white-space:nowrap` только на .base, а между
   двумя .base перенос разрешён, и на кадре s12 формула $g\circ f\colon A\to C$
   разъехалась: «морфизм g ∘» в конце строки, «f: A → C» в начале следующей.
   nowrap на всей .katex делает формулу одним словом. Если после этого формула
   шире колонки, это станет overflow зоны и покраснеет в audit.py — то есть
   правило не прячет проблему, а переводит её в видимую. */
.katex{font-size:1.0em;white-space:nowrap}

/* опорные точки (Р23): цветное СЛОВО-надзаголовок у левого поля, Forum caps;
   формулировка идёт ниже отдельным абзацем на всю ширину, без точки в конце.
   Определение — зелёным, утверждение/теорема — стальным, задача — кирпичным.
   Надзаголовок прижат к своей формулировке (4px), а отбивается от ПРЕДЫДУЩЕГО
   блока — иначе ярлык висит между двумя формулировками и не понятно, чей он. */
.op-def,.op-utv,.op-task{font-family:'Forum',serif;text-transform:uppercase;
  letter-spacing:.055em;line-height:1.12;font-size:.62em}
.t-body p.op-def,.t-body p.op-utv,.t-body p.op-task{margin-top:var(--blok)}
.t-body p.op-def + p,.t-body p.op-utv + p,.t-body p.op-task + p{margin-top:4px}
.op-def{color:var(--cgreen)}
.op-utv{color:var(--steel)}
.op-task{color:var(--brick)}
/* первая опорная точка слайда не отбивается сверху — она и есть начало */
.t-body > p.op-def:first-child,.t-body > p.op-utv:first-child,
.t-body > p.op-task:first-child{margin-top:.18em}

/* плейсхолдер портрета: плоская карточка, ноль тени/скругления/градиента
   (audit-clean, как .ph у dandelin). Настоящие портреты — долг арки 9. */
.ph-portret{width:100%;height:100%;display:grid;place-items:center;
  background:var(--card);color:var(--steel);padding:18px;text-align:center;
  font-family:'Forum',serif;text-transform:uppercase;letter-spacing:.05em;
  font-size:26px;line-height:1.2}

/* blur-reveal: механизм ортогонален data-scene-from (08-sceny/DOK.md) */
.blur-reveal{filter:blur(5.5px) saturate(.55);opacity:.9;color:var(--steel);
  transition:filter .5s ease,opacity .5s ease,color .5s ease;will-change:filter}
__CASCADE_BLUR__{filter:none;opacity:1;color:var(--brick)}

/* каскад раскладки — ПОРОЖДЁН до .scene-9 (база обрывалась на .scene-5: урок 8, G15)
   и с J=1, а не с J=2: тег {@1-M} ставится ради УХОДА, а раскрыть его было нечем */
__CASCADE_LAYOUT__{opacity:1;visibility:visible}

/* уход ПОСЛЕ последней своей сцены, а не НА ней (см. комментарий в скрипте):
   без этого {@K-K} гасит сам себя и блок не виден ни в одной сцене */
__CASCADE_UNTIL__{opacity:1!important;visibility:visible!important}

/* ПЕРЕТЕКАНИЕ ПО СЦЕНАМ: вне-сценовый текст в потоке не занимает места.
   Вынужденное отступление от «никогда display» — без него зона обязана вместить
   весь текст слайда разом, и 19 зон из 32 переполнены до +1817px. Разбор и цена —
   в комментарии скрипта. Панели иллюстраций сюда НЕ входят: они позиционированы
   абсолютно, поток не двигают и сохраняют плавное появление. */
__CASCADE_FLOW_HIDE__{display:none}
__CASCADE_FLOW_SHOW__{display:block}
/* `!important` у обеих строк ниже — не украшение. Показывающее правило несёт
   `.scene-K` плюс атрибут (0,3,2), а гасящее — класс `.scene-off` (0,2,1), и без
   `!important` показ ПЕРЕБИВАЛ уход: на сцене 4 стояли разом блоки сцен 1–4, то есть
   замена не освобождала ни пикселя, и промер честно показывал те же +1817px. База
   ровно поэтому и держит `.scene-off` на `!important` (`base.css:22`). */
__CASCADE_FLOW_OFF__{display:none!important}
__CASCADE_FLOW_UNTIL__{display:block!important}

/* маркер пункта живёт и гаснет вместе со своим пунктом (см. комментарий в скрипте) */
.tlist li:has(> [data-scene-from])::before{opacity:0;visibility:hidden;
  transition:opacity .24s ease}
__CASCADE_MARKER__{opacity:1;visibility:visible}

/* синхронное раскрытие «текст + картинка одной сцены» (08-sceny/DOK.md, адаптация) */
.formula[data-scene-from],[data-scene-from] .formula,
.panel[data-scene-from],.ill-box[data-scene-from]{transition-delay:0s}
"""

deck = (DECK_LAYER.replace("__CASCADE_LAYOUT__", cascade_layout)
                  .replace("__CASCADE_UNTIL__", cascade_until)
                  .replace("__CASCADE_FLOW_HIDE__", cascade_flow_hide)
                  .replace("__CASCADE_FLOW_SHOW__", cascade_flow_show)
                  .replace("__CASCADE_FLOW_OFF__", cascade_flow_off)
                  .replace("__CASCADE_FLOW_UNTIL__", cascade_flow_until)
                  .replace("__CASCADE_MARKER__", cascade_marker)
                  .replace("__CASCADE_BLUR__", cascade_blur))

text = ("/* ПОРОЖДЕНО src/tools/sobrat_overlay.py — руками не править, правь скрипт. */\n"
        "/* ===== [1] KaTeX %s: шрифты base64 + ядро CSS ===== */\n%s\n%s\n%s\n"
        % ("(dist из node_modules Паскаля, read-only)",
           "\n".join(out_faces), css_body, deck))

(SRC / "overlay.css").write_text(text, encoding="utf-8")
print("шрифтов вшито: %d из %d @font-face" % (embedded, len(faces)))
if missing:
    print("⚠ без woff2: %s" % missing)
print("каскад сцен порождён: .scene-%d..%d плюс .scene-99 (заплата render.py) · "
      "from J=%d..%d · семья until: %d правил"
      % (SCENES[0], MAX_SCENES, 1, MAX_SCENES, cascade_until.count(",") + 1))
print("→ %s (%d КБ)" % (SRC / "overlay.css", len(text.encode()) // 1024))
sys.exit(0)
