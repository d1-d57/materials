#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Иллюстрация-осознанный генератор слайд-колод (html-slides-studio канон, 4 блока)
istochnik/src/ → self-contained index.html + линтер-гейт.
Чистая stdlib (re, pathlib, argparse) — запускается без pip/сети.

  python3 build_deck.py <src-dir>            # линтер-гейт + сборка → <src-dir>/dist/index.html
  python3 build_deck.py <src-dir> --lint     # только линтер
  python3 build_deck.py <src-dir> -o <path>  # выбрать выход

Контракт (см. materials/_generator/DESIGN.md): HTML — чистая функция источника.
`shablon.html` — оригинал колоды с каждым извлечённым куском, заменённым НА МЕСТЕ
уникальным плейсхолдером `{{TOKEN}}`; сборка — обратная подстановка плейсхолдеров
байтами файлов (или, для `{{MD:...}}`, рендером markdown — единственный «умный»
преобразователь, см. DESIGN §7; всё прочее — дословная конкатенация).
Плейсхолдеры МОГУТ быть вложенными на один уровень (глава несёт свой `{{DRIVER:NN}}»
внутри) — substitute() гоняет несколько проходов до неподвижной точки.
"""
import re, sys, json, argparse
from functools import lru_cache
from pathlib import Path

PLACEHOLDER_RE = re.compile(r"\{\{[A-Za-z0-9_:.\-]+\}\}")
GEN_BANNER = "<!-- ⚠ СГЕНЕРИРОВАНО ИЗ src/ ГЕНЕРАТОРОМ _generator/build_deck.py — РУКАМИ НЕ ПРАВИТЬ. Правь источник в src/. -->\n"
CYR = re.compile(r"[а-яА-ЯёЁ]")

# ───────────────────────── канон трёх служебных слайдов ─────────────────────────
# Обложка, визитка «Про меня» и финал «Спасибо за внимание» ПОРОЖДАЮТСЯ из полей
# brief.md и заготовок ниже — рукописных `slides/<id>.html` для них не существует.
# Это хук H6 (`_studio/konvejer/GEJTY.md`) в слое вёрстки: величина, обязанная
# совпадать между деками, порождается, а не выписывается руками в каждом.
SLUZHEBNYE = Path(__file__).resolve().parent / "skeleton" / "sluzhebnye"
COVER_ID, VIZITKA_ID, FINAL_ID = "sl-title", "sl-vizitka", "sl-thanks"
SERVICE_IDS = (COVER_ID, VIZITKA_ID, FINAL_ID)
# `?ПОЛЕ` в начале строки заготовки — строка живёт, только если поле объявлено;
# `!ПОЛЕ` — только если НЕ объявлено. Нет поля — нет элемента: значений по
# умолчанию у служебных слайдов нет ни одного, выводить их из `id`/`title` нельзя.
OPT_LINE_RE = re.compile(r"^([ \t]*)([?!])([A-Z]+)(.*)$")


# ───────────────────────── каскад раскрытия сцен: ПОРОЖДАЕТСЯ, не пишется руками ─────────────────────────
# Пары «сцена × шаг» были выписаны в `skeleton/base.css` РУКАМИ до `.scene-5`.
# Слайд с шестью сценами не раскрывал шаги с шестого — не по запрету, а потому что
# строчку не дописали, и цена уже оплачена в арке Паскаля («на шестой оставалась
# первая сцена»). Величина, обязанная совпадать с числом сцен дека, порождается.
#
# Включается ОДНИМ признаком — плейсхолдером `{{SCENE_CASCADE}}` в источнике.
# Его отсутствие у buffon/dandelin/fibonacci и есть гарантия, что их выход не
# меняется: ни одна строка ниже для них не исполняется (тот же приём, что у
# `{{SLIDES}}`).
# 🔴 Кавычки — НЕОБЯЗАТЕЛЬНЫЕ, и любые. Строгая форма `="(\d+)"` (как у линтера)
# здесь давала дефект, которого у рукописного списка не было: слайд с
# `data-scenes='6'` в ОДИНАРНЫХ кавычках не матчился, максимум выходил 1, каскад
# схлопывался в одно правило — и сцены 2..6 не раскрывали НИЧЕГО при rc=0 линтера.
# Рукописный список от разбора не зависел вовсе и на них работал. Порождение не
# имеет права быть хрупче того, что оно заменяет. Найдено верификатором.
SCENE_ATTR_RE = re.compile(r'data-scene(?:s|-from|-until)\s*=\s*["\']?(\d+)')

# Потолок сцен: `scene_cascade_css` растёт КВАДРАТИЧНО (n=12 → 2,9 КБ, n=100 →
# 171 КБ, n=400 → 2,8 МБ CSS в самодостаточном монолите), а опечатка вроде
# `data-scenes="44"` вместо `4` раздувала бы выход молча. Порог = фактический
# максимум живых деков (buffon 5, fibonacci 4, dandelin 4, teorkat-vvedenie 2;
# сверено 30.07 грепом по src/) с запасом вдвое — органический рост дека до
# 6-9 сцен не спотыкается, а опечатка ловится. Найдено долгом фабрики, потолка
# не было вовсе.
SCENE_CAP = 10


def max_scenes(*texts):
    """Фактический максимум сцен по источнику.

    Считается по ТРЁМ атрибутам, а не по одному `data-scenes`. «Ровно до
    max(data-scenes)» было бы регрессией против рукописного списка: слайд с
    `data-scenes="2"` и тегом `{@3}` рукописный каскад до пятой раскрывал, а
    каскад по одному `data-scenes` — уже нет. Максимум по объединению не может
    оказаться меньше того, что в разметке реально размечено.
    """
    found = [1]
    for t in texts:
        found.extend(int(m) for m in SCENE_ATTR_RE.findall(t or ""))
    return max(found)


def scene_cascade_css(n):
    """Каскад раскрытия `.scene-1..n` — CSS-текст, дословно в форме рукописного.

    🔴 J идёт С ЕДИНИЦЫ, а не с двойки, и это починка молчаливой потери, а не
    запас. Рукописный каскад начинался с J=2 («сцена 1 — это то, что видно сразу,
    тега не несёт»). Но `_attrs_from_tag` на тег `{@1}` честно пишет
    `data-scene-from="1"` (тег на первой сцене ставят не ради появления, а ради
    того, чтобы блок потом УШЁЛ по `data-scene-until`), а базовое правило
    `[data-scene-from]` прячет ВСЁ с этим атрибутом — раскрыть единицу было нечем,
    и блок не показывался НИ В ОДНОЙ сцене. Цена: 49 абзацев ленты Л1, при этом
    зелёные линтер, `check_view.py` и `audit.py --scene-diff`.

    Специфичность не меняется, `!important` не нужен: форма селектора дословно
    прежняя — `.scene-N [data-scene-from="K"]` это (0,2,0) против скрывающего
    `[data-scene-from]` (0,1,0), а `.scene-off` как и раньше выигрывает своим
    `!important`.

    🔴 НАЗВАННАЯ СВЯЗЬ С ДВИЖКОМ (иначе она молчаливая). Рукописный список всегда
    доходил до `.scene-5`, даже у дека с двумя сценами, и потому терпел сцену вне
    диапазона. Порождённый обрывается на фактическом `n` — и это КОРРЕКТНО ровно
    потому, что `applyScene` в `skeleton/engine.js` зажимает `k` числом сцен
    слайда: класса `.scene-K` при `K > n` не возникает, значит правило для него не
    нужно. Снимут зажатие — каскад станет узким для входов вроде `#s1.9`, и
    покраснеет фикстура `fixtures/dvizhok/` (она держит обе половины разом).
    Связь названа верификатором как незадокументированная.
    """
    # sc идёт С ЕДИНИЦЫ: на первой сцене шаг 1 обязан быть виден, иначе `{@1}`
    # не показан ни в одной сцене — ровно та потеря, что описана выше. Список
    # поэтому не бывает пустым даже при n=1, и пустого селектора не возникает.
    pairs = [".scene-%d [data-scene-from=\"%d\"]" % (sc, step)
             for sc in range(1, n + 1) for step in range(1, sc + 1)]
    return ("/* каскад раскрытия ПОРОЖДЁН по фактическому максимуму сцен дека\n"
            "   (было выписано руками до .scene-5 — слайд с шестью сценами не\n"
            "   раскрывался с шестого шага). Правится в build_deck.py, не здесь. */\n"
            + ",\n".join(pairs)
            + "\n  { opacity: 1; visibility: visible; }")


# ───────────────────────── чтение/запись без трансляции переводов строк ─────────────────────────
def read_text(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


# ───────────────────────── brief.md: фронтматтер (id/title/canvas/slide_order/…) ─────────────────────────
def parse_brief(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    meta, cur_list = {}, None
    for line in m.group(1).splitlines():
        lm = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if lm:
            key, val = lm.group(1), lm.group(2).strip()
            if val == "":
                cur_list = key
                meta[key] = []
            else:
                cur_list = None
                meta[key] = val.strip('"')
            continue
        lm2 = re.match(r"^\s*-\s*(.+?)\s*$", line)
        if lm2 and cur_list is not None:
            meta[cur_list].append(lm2.group(1))
    return meta


# ───────────────────────── markdown → HTML зон текста (Milestone 2, DESIGN §7) ─────────────────────────
# Единственный «умный» преобразователь во всём генераторе; всё прочее — дословная
# конкатенация. Диалект минимален и рассчитан на round-trip конкретной вёрстки канона:
# content/*.md пишем сами (не произвольный ввод), поэтому HTML в них (напр. дословный
# <b>лид-ин</b> или явный <br>) не экранируется, а проходит как есть — в духе
# render_inline() из kurs leto 2026/istochnik/_generator/build.py, но без escape-шага.
# Формат сцен (DESIGN §7): ведущий тег абзаца/списка {@N}=с N сцены, {@N-M}=с N до M,
# {@-M}=до M, {.cls}=класс. Инлайн {@N| …}=спан-раскрытие, {fill@N| бланк | ответ}=шторка.
SCENE_PREFIX = re.compile(r"^\{([^}|]*)\}[ \t]*")


def _attrs_from_tag(tag, default_cls=None):
    """Атрибуты В ПОРЯДКЕ токенов тега — чтобы точно воспроизвести исходный порядок
    class/data-scene (браузеру он безразличен, но строгая посимвольная сверка ловит):
    '@2 .note' → ' data-scene-from="2" class="note"'; '.pA @-3' → ' class="pA" data-scene-until="3"';
    '@2-4' → ' data-scene-from="2" data-scene-until="4"'. Классы (несколько .x) сливаются в один
    class="…" на месте ПЕРВОГО класс-токена. `default_cls` — класс, если тег ни одного своего не
    несёт (нужен `<ul>` без явного `{.cls}`: раньше дефолт `tlist` был отдельной переменной у
    вызывающего, теперь общий для всех вызовов — заход tihie-polomki, П1)."""
    parts, cls, cls_at = [], [], None
    for tok in tag.split():
        if tok.startswith("@"):
            body = tok[1:]
            if "-" in body:
                a, b = body.split("-", 1)
                if a:
                    parts.append('data-scene-from="%s"' % a)
                if b:
                    parts.append('data-scene-until="%s"' % b)
            else:
                parts.append('data-scene-from="%s"' % body)
        elif tok.startswith("."):
            if cls_at is None:
                cls_at = len(parts)
                parts.append(None)
            cls.append(tok[1:])
    if cls_at is not None:
        parts[cls_at] = 'class="%s"' % " ".join(cls)
    elif default_cls:
        parts.append('class="%s"' % default_cls)
    return (" " + " ".join(parts)) if parts else ""


def _join_lines(lines):
    """Склейка строк абзаца: строка, кончающаяся на '\\' → жёсткий <br>; иначе пробел
    (браузер схлопнёт перевод в пробел). Так автор сам расставляет переносы строк."""
    res = ""
    for i, ln in enumerate(lines):
        if i == 0:
            res = ln
        elif res.endswith("\\"):
            res = res[:-1].rstrip() + "<br>" + ln
        else:
            res = res + " " + ln
    return res


def render_inline_md(text, math, acc_tag="b"):
    """$tex$ → готовый KaTeX-HTML из кэша формул (math); **x** → <b class="acc">x</b> (акцент);
    *x* → <em>; {fill@N|бланк|ответ} → шторка; {@N| x} → спан-раскрытие. Сырой HTML — как есть.
    Формулы прячем в плейсхолдеры на время структурной разметки: '}' внутри TeX
    (\\boldsymbol{p}) иначе ломает разбор {@N|…} — приём stash→parse→unstash из build.py."""
    stash = []
    text = re.sub(r"\$(.+?)\$",
                  lambda m: stash.append(m.group(1)) or "\x00M%d\x00" % (len(stash) - 1), text)
    text = re.sub(r"\*\*(.+?)\*\*", r'<%s class="acc">\1</%s>' % (acc_tag, acc_tag), text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"\{fill@(\d+)\|(.*?)\|(.*?)\}",
                  lambda m: '<span class="fill"><span data-scene-until="%s">%s</span>'
                            '<span data-scene-from="%s">%s</span></span>'
                            % (m.group(1), m.group(2).strip(), m.group(1), m.group(3).strip()),
                  text)
    text = re.sub(r"\{blur@(\d+)\|(.*?)\}",
                  lambda m: '<span class="blur-reveal" data-reveal="%s">%s</span>'
                            % (m.group(1), m.group(2).strip()),
                  text)
    text = re.sub(r"\{@([-\d]+)\|(.*?)\}",
                  lambda m: "<span%s>%s</span>" % (_attrs_from_tag("@" + m.group(1)), m.group(2).strip()),
                  text)
    text = re.sub(r"\x00M(\d+)\x00",
                  lambda m: math.get(stash[int(m.group(1))], "⟦MISSING-MATH:%s⟧" % stash[int(m.group(1))]),
                  text)
    return text


def render_md(text, math, acc_tag="b"):
    """content/*.md → HTML зон текста (DESIGN §7 / SLIDE-FORMAT.md). Пустая строка = абзац <p>.
    Ведущий тег {@N}/{.cls} → сцена/класс БЛОКА (абзаца ИЛИ списка целиком — заход tihie-polomki,
    П1: раньше тег снимался только с абзаца, список под ним схлопывался в текст, потому что
    отдельная узкая проверка `{.cls}`-строки не понимала `@N`). Блок «- » → <ul>.
    Перенос внутри абзаца: '\\' на конце строки → <br>, иначе пробел. $tex$ → кэш. HTML — как есть."""
    out = []
    for block in re.split(r"\n\s*\n", text.strip("\n")):
        lines = [ln.strip() for ln in block.split("\n") if ln.strip()]
        if not lines:
            continue
        # тег в начале блока снимается ОДИН раз, до развилки список/абзац — он
        # свойство блока целиком, не абзаца отдельно от списка
        tag, body = None, lines
        m = SCENE_PREFIX.match(lines[0])
        if m:
            tag = m.group(1)
            rest = lines[0][m.end():]
            if rest.strip() == "":
                body = lines[1:] or [""]
            else:
                body = [rest] + lines[1:]
        if all(l.startswith("- ") for l in body):
            attrs = _attrs_from_tag(tag or "", default_cls="tlist")
            items = "".join("<li>%s</li>" % render_inline_md(l[2:].strip(), math, acc_tag) for l in body)
            out.append('<ul%s>%s</ul>' % (attrs, items))
            continue
        attrs = _attrs_from_tag(tag) if tag is not None else ""
        out.append("<p%s>%s</p>" % (attrs, render_inline_md(_join_lines(body), math, acc_tag)))
    return "\n".join(out)


# ───────────────────────── словарь классов {.имя} (заход tihie-polomki, П2) ─────────────────────────
# `{.tlsit}` вместо `{.tlist}` рендерился обычным классом молча — гейт зелёный, класс без стиля.
# Словарь СОБИРАЕТСЯ из файлов (не пишется списком в коде — список разошёлся бы со скелетом через
# неделю): класс-селекторы `skeleton/base.css` (канон-CSS тела карточки, читается всеми пайплайнами)
# + `GLOBAL_CSS` из `sborka/tipy.py`, импортированный (не regex по .py — там `.get()/.split()` дали
# бы мусорные «классы» вроде `get`/`split`; `tipy.py` не импортирует ничего из `build_deck.py`,
# цикла не будет — тот же приём, каким `slaid.py`/`deck.py` уже читают `GLOBAL_CSS`).
CSS_CLASS_RE = re.compile(r"\.([A-Za-z_][\w-]*)")


CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)


@lru_cache(maxsize=1)
def known_classes():
    """Комментарии CSS вырезаются ДО разбора: в них живая проза («engine.js», «sborka/deck.py»)
    даёт `.js`/`.py`-мусор в CSS_CLASS_RE — не опасно (лишний класс в словаре не даёт ложного
    красного, только теоретически пропустил бы опечатку, совпавшую с расширением файла), но
    вырезать дёшево и без него список чище."""
    generator = Path(__file__).resolve().parent
    base_css_path = generator / "skeleton" / "base.css"
    base_css = CSS_COMMENT_RE.sub("", read_text(base_css_path)) if base_css_path.is_file() else ""
    classes = set(CSS_CLASS_RE.findall(base_css))
    sborka = generator / "sborka"
    if str(sborka) not in sys.path:
        sys.path.insert(0, str(sborka))
    from tipy import GLOBAL_CSS  # noqa: E402  (read-only импорт, см. докстроку выше)
    classes |= set(CSS_CLASS_RE.findall(GLOBAL_CSS))
    return classes


# `{.имя}` — ТОЛЬКО ведущий тег блока (та же позиция, что ищет `SCENE_PREFIX` в `render_md`);
# инлайн-формы `{@N|…}`/`{fill@N|…}`/`{blur@N|…}` (`render_inline_md`) класса не несут вовсе —
# проверено по их regex'ам, там нет `.`-токена. Строка считается от НАЧАЛА переданного текста
# (`text`), а не исходного файла — вызывающий не глотает нумерацию, он и сам сырой текст карточки.
LEADING_TAG_RE = re.compile(r"^\{([^}|]*)\}", re.M)


def find_unknown_classes(text, known):
    """Сырой markdown (ДО render_md) → [(имя_класса, номер_строки), …] для классов вне `known`."""
    problems = []
    for m in LEADING_TAG_RE.finditer(text):
        for tok in m.group(1).split():
            if tok.startswith("."):
                name = tok[1:]
                if name not in known:
                    line = text[:m.start()].count("\n") + 1
                    problems.append((name, line))
    return problems


# ───────────────────────── порождение служебных слайдов ─────────────────────────
def fill_template(text, fields):
    """Заготовка из `skeleton/sluzhebnye/` + поля → HTML слайда.

    Диалект нарочно крошечный (две формы, обе построчные), чтобы заготовку можно
    было читать как обычный HTML: `?ПОЛЕ`/`!ПОЛЕ` в начале строки — условная
    строка, `{ПОЛЕ}` — подстановка. Значения идут из `brief.md` как есть (сырой
    HTML не экранируется — та же договорённость, что в render_inline_md)."""
    kept = []
    for line in text.split("\n"):
        m = OPT_LINE_RE.match(line)
        if m:
            indent, sign, name, rest = m.groups()
            if (sign == "?") != bool(fields.get(name)):
                continue
            line = indent + rest
        kept.append(line)
    out = "\n".join(kept)
    for name, val in fields.items():
        out = out.replace("{%s}" % name, val if isinstance(val, str) else "")
    return out


def generate_service_slides(meta, filemap, names, math):
    """Обложка/визитка/финал → filemap; возвращает (порождённые id, порядок слайдов).

    Порядок служебных слайдов — тоже не рукописный: обложка первая, визитка ВСЕГДА
    вторая (снимается только явным `vizitka: net`), финал последний. Если дек всё
    же несёт рукописный `slides/<служебный id>.html` — приоритет у него, а
    порождение молчит: три немигрированных дека обязаны собираться как прежде."""
    hand = set(names.get("slides", []))
    middle = [x for x in (meta.get("slide_order") or []) if x not in SERVICE_IDS]
    order = [COVER_ID]
    if str(meta.get("vizitka", "")).strip().lower() != "net":
        order.append(VIZITKA_ID)
    order += middle + [FINAL_ID]

    generated = []

    def emit(sid, shablon_name, fields):
        if sid in hand:                       # рукописный слайд имеет приоритет
            return
        tpl = read_text(SLUZHEBNYE / shablon_name)
        filemap["{{SLIDE:%s}}" % sid] = fill_template(tpl, fields).rstrip("\n")
        generated.append(sid)

    date_place = " · ".join(x for x in (meta.get("cover_date", ""), meta.get("cover_place", ""))
                            if isinstance(x, str) and x)
    emit(COVER_ID, "oblozhka.html", {
        "ID": COVER_ID,
        "TITLE": meta.get("title", ""),
        "SUB": meta.get("cover_sub", ""),
        "DATEPLACE": date_place,
        "ILL": meta.get("cover_ill", ""),
    })
    if VIZITKA_ID in order:
        emit(VIZITKA_ID, "vizitka.html", {
            "ID": VIZITKA_ID,
            # активы визитки живут в каноне и вшиваются ОТТУДА: копий в деках нет,
            # правка биографии/фото должна быть в одном месте на все деки.
            "PHOTO": read_text(SLUZHEBNYE / "vizitka-photo.html").strip(),
            "QR": read_text(SLUZHEBNYE / "vizitka-qr.html").strip(),
            "COPY": render_md(read_text(SLUZHEBNYE / "vizitka.md"), math,
                              meta.get("accent_tag", "b")),
        })
    emit(FINAL_ID, "final.html", {"ID": FINAL_ID, "ILL": meta.get("final_ill", "")})
    return generated, order


# ───────────────────────── загрузка src/ ─────────────────────────
def load_source(src):
    """shablon.html + все дословные части → (shablon, filemap{token:content}, meta, names{kind:[имена]})."""
    shablon = read_text(src / "shablon.html")
    meta = parse_brief(read_text(src / "brief.md")) if (src / "brief.md").exists() else {}

    filemap = {}
    filemap["{{TOKENS_CSS}}"] = read_text(src / "tokens.css")
    filemap["{{FONTS_CSS}}"] = read_text(src / "fonts" / "faces.css")
    filemap["{{ENGINE_JS}}"] = read_text(src / "engine.js")

    def load_if_present(token, path):
        """Дек-специфичный дословный файл, который есть не у каждой колоды
        (three.min.js — только Dandelin; overlay.css/sims/lab.core.js — только
        Buffon) — грузим, только если файл физически существует."""
        if path.is_file():
            filemap[token] = read_text(path)

    load_if_present("{{THREE_LIB}}", src / "lib" / "three.min.js")
    load_if_present("{{BASE_CSS}}", src / "base.css")        # общий канон-base скелета (опц.; эталонов без него не задевает)
    load_if_present("{{OVERLAY_CSS}}", src / "overlay.css")
    load_if_present("{{SIM:lab.core}}", src / "sims" / "lab.core.js")

    names = {}
    def load_dir(kind, folder, token_fmt):
        items = sorted(folder.glob("*")) if folder.is_dir() else []
        got = []
        for p in items:
            if not p.is_file():
                continue
            filemap[token_fmt % p.stem] = read_text(p)
            got.append(p.stem)
        names[kind] = got

    load_dir("illustrations", src / "illustrations", "{{ILL:%s}}")
    load_dir("chapters", src / "chapters", "{{CHAPTER:%s}}")
    load_dir("drivers", src / "drivers", "{{DRIVER:%s}}")
    load_dir("slides", src / "slides", "{{SLIDE:%s}}")
    load_dir("sims", src / "sims" / "ext", "{{SIM:%s}}")

    math_path = src / "math" / "katex.json"
    math = json.loads(read_text(math_path)) if math_path.is_file() else {}

    names["content"] = []
    names["content_raw"] = {}
    for p in sorted((src / "content").glob("*.md")) if (src / "content").is_dir() else []:
        raw = read_text(p)
        filemap["{{MD:%s}}" % p.stem] = render_md(raw, math, meta.get("accent_tag", "b"))
        names["content"].append(p.stem)
        # сырой текст — для П2-проверки {.имя} в lint() (заход tihie-polomki): она смотрит
        # именно на авторские теги блока, а не на весь HTML (там ещё классы KaTeX и дословный
        # HTML контента — не тег {.имя}, лезть в них было бы неверным охватом проверки).
        names["content_raw"][p.stem] = raw

    # Канон-CSS служебных слайдов — по требованию шаблона (у деков, собранных до
    # перехода на порождение, плейсхолдера нет, и подстановка их не касается).
    filemap["{{SLUZHEBNYE_CSS}}"] = read_text(SLUZHEBNYE / "style.css")

    # Порождение включается ОДНИМ признаком — плейсхолдером {{SLIDES}} в шаблоне.
    # Его отсутствие у buffon/dandelin/fibonacci и есть гарантия, что их выход не
    # меняется: ни одна ветка ниже для них не исполняется.
    names["generated"] = []
    if "{{SLIDES}}" in shablon:
        names["generated"], names["order"] = generate_service_slides(meta, filemap, names, math)
        filemap["{{SLIDES}}"] = "\n".join(
            filemap.get("{{SLIDE:%s}}" % sid, "{{SLIDE:%s}}" % sid) for sid in names["order"])

    # Каскад сцен — по фактическому максимуму ЭТОГО дека, и СТРОГО ПОСЛЕ порождения
    # служебных слайдов: они тоже попадают в filemap, и считать до них означало бы
    # мерить неполный дек. Запись безусловна, как у `{{SLUZHEBNYE_CSS}}`; источник
    # без плейсхолдера её не заметит.
    filemap["{{SCENE_CASCADE}}"] = scene_cascade_css(
        max_scenes(shablon, *filemap.values()))

    return shablon, filemap, meta, names


# ───────────────────────── сборка: подстановка плейсхолдеров до неподвижной точки ─────────────────────────
def assemble(shablon, filemap, max_passes=6):
    out = shablon
    for _ in range(max_passes):
        changed = False
        for token, content in filemap.items():
            if token in out:
                out = out.replace(token, content)
                changed = True
        if not changed:
            break
    return out


def chapter_base_name(name):
    """'mirror-2' → 'mirror' (второе вхождение дублирующегося id в оригинале)."""
    m = re.match(r"^(.*)-(\d+)$", name)
    return m.group(1) if m else name


def _slide_sections(assembled):
    """[(id, html)] — секции <section class="slide"> из assembled, в порядке файла."""
    out = []
    for m in re.finditer(r'<section\b[^>]*class="[^"]*\bslide\b[^"]*"[^>]*>', assembled):
        end = assembled.find("</section>", m.end())
        if end == -1:
            continue
        body = assembled[m.start():end + len("</section>")]
        mid = re.search(r'\bid="([^"]+)"', m.group(0))
        if mid:
            out.append((mid.group(1), body))
    return out


# ───────────────────────── линтер (структурный гейт, DESIGN.md §9) ─────────────────────────
def lint(shablon, filemap, meta, names):
    errors, warns = [], []
    assembled = assemble(shablon, filemap)

    # 1. 0 нерезрешённых {{...}}
    for tok in PLACEHOLDER_RE.findall(assembled):
        errors.append("нерезрешённый плейсхолдер %s в выходе" % tok)

    # 1b. все $tex$ из content нашли рендер в кэше формул math/katex.json
    for tex in re.findall(r"⟦MISSING-MATH:(.*?)⟧", assembled):
        errors.append("формула $%s$ не в math/katex.json (пересобери harvest_katex.py)" % tex)

    # 1c. {.имя} из content/*.md — сверка со словарём скелета (заход tihie-polomki, П2;
    # тот же приём, что var(--x) в п.3 ниже: 0 внешнего словаря в коде, только regex по файлам).
    # 🔴 Смотрим СЫРОЙ текст (`names["content_raw"]`), а не рендер: рендер несёт ЕЩЁ и классы
    # KaTeX (`.mord`/`.vlist`/…) и дословный HTML контента (докстрока render_md — content/*.md
    # пишем сами, HTML в них не экранируется), у них class="…" совсем не про тег {.имя} и не
    # обязан жить в словаре скелета — первый прогон на живых деках дал 1823/6/3/2970 ложных
    # красных именно по этой причине, пока проверка смотрела на `filemap["{{MD:%s}}"]`.
    # `render_body` (sborka/formaty.py) закрывает эту же дыру для НОВОГО пайплайна живым
    # исключением с номером строки; здесь — старый пайплайн, номера строки нет (как и у
    # соседней проверки var(--x) ниже).
    # 🔴 Деки старого пайплайна (buffon/dandelin/fibonacci — до перехода на канон-скелет)
    # несут СВОЙ CSS прямо в `<style>` шаблона (`#sl-vizitka .bullets`, `.slide .t-body p.eq`
    # и т.п.) — классы оттуда тоже законные, не только словарь скелета. Без этой строки первый
    # прогон на живых деках дал 7+3 ложных красных (buffon/fibonacci) на классах, которые есть
    # и стилизованы, просто не в skeleton/base.css. Источник — САМ `shablon` этого дека, тот же
    # приём «из файлов, не из головы».
    deck_css = "".join(re.findall(r"<style\b[^>]*>(.*?)</style>", shablon, re.S))
    known = known_classes() | set(CSS_CLASS_RE.findall(CSS_COMMENT_RE.sub("", deck_css)))
    for name, raw in names.get("content_raw", {}).items():
        for cls, _line in find_unknown_classes(raw, known):
            errors.append("content/%s.md: класс '.%s' не найден в словаре скелета "
                          "(base.css + tipy.py:GLOBAL_CSS) — опечатка в {.имя}?"
                          % (name, cls))

    # 2. data-ill / data-iframe → файл существует
    ill_names = set(names.get("illustrations", []))
    chapter_bases = {chapter_base_name(n) for n in names.get("chapters", [])}
    for m in re.finditer(r'data-ill="([^"]+)"', assembled):
        if m.group(1) not in ill_names:
            errors.append('битая ссылка: data-ill="%s" — нет illustrations/%s.*' % (m.group(1), m.group(1)))
    for m in re.finditer(r'data-iframe="tpl-([^"]+)"', assembled):
        if m.group(1) not in chapter_bases:
            errors.append('битая ссылка: data-iframe="tpl-%s" — нет chapters/%s.html' % (m.group(1), m.group(1)))

    # 3. var(--x) в иллюстрациях определена в tokens.css
    defined = set(re.findall(r'--([A-Za-z0-9_-]+)\s*:', filemap.get("{{TOKENS_CSS}}", "")))
    for name in names.get("illustrations", []):
        content = filemap.get("{{ILL:%s}}" % name, "")
        for v in re.findall(r'var\(--([A-Za-z0-9_-]+)', content):
            if v not in defined:
                errors.append("illustrations/%s: var(--%s) не определена в tokens.css (→ чёрная заливка)" % (name, v))

    # 4. 0 внешних asset-URL (src/href на http(s)://, //…); <a href> — разрешено
    ext_re = re.compile(r'<(?!a[\s>])[a-zA-Z][\w:-]*\b[^>]*?\b(?:src|href)\s*=\s*"(?:https?:)?//[^"]*"', re.S)
    for m in ext_re.finditer(assembled):
        errors.append("внешний asset-URL: %s…" % m.group(0)[:70])

    # 5. slide_order покрывает все slides/, нет сирот/дублей.
    # У дека на порождении судится ЭФФЕКТИВНЫЙ порядок (со служебными слайдами,
    # которые генератор вставил сам) — иначе линтер объявил бы их сиротами.
    order = names.get("order") or meta.get("slide_order", [])
    present = set(names.get("slides", [])) | set(names.get("generated", []))
    missing = present - set(order)
    extra = set(order) - present
    dupes = sorted({x for x in order if order.count(x) > 1})
    if missing:
        errors.append("слайды вне slide_order: %s" % sorted(missing))
    if extra:
        errors.append("slide_order ссылается на несуществующие слайды: %s" % sorted(extra))
    if dupes:
        errors.append("дубли id в slide_order: %s" % dupes)

    # 5b. в выходе есть хотя бы один слайд. Ловит опечатку в плейсхолдере потока:
    # `{{ SLIDES }}` с пробелами — не плейсхолдер (PLACEHOLDER_RE пробелов не знает),
    # он молча уезжает в выход как текст, порождение не включается, и дек собирается
    # ЧИСТЫМ, но пустым. Такое состояние не ловил никто (найдено верификатором 28.07).
    if not re.search(r'<section[^>]*class="slide"', assembled):
        errors.append("в собранном деке ноль слайдов — проверь плейсхолдер потока "
                      "{{SLIDES}} (пробелы внутри скобок его убивают) и slide_order")

    # 6. (мягко) неиспользуемые illustrations/* — сводная строка с ОХВАТОМ (иначе тонут в потоке)
    used_ill = set(re.findall(r'data-ill="([^"]+)"', assembled))
    all_ill = names.get("illustrations", [])
    orphans = sorted(n for n in all_ill if n not in used_ill)
    if orphans:
        warns.append('ассетов-сирот %d из %d в реестре (не используется ни одним слайдом): %s. '
                     'Мёртвый вес в самодостаточном монолите.'
                     % (len(orphans), len(all_ill), ", ".join(orphans)))

    # дублирующийся id главы в оригинале — второе вхождение недостижимо через getElementById
    from collections import Counter
    cnt = Counter(chapter_base_name(n) for n in names.get("chapters", []))
    for base, c in cnt.items():
        if c > 1:
            errors.append('исходный id "tpl-%s" встречается %d× в оригинале — второе вхождение '
                         'недостижимо через getElementById (сохранено дословно)' % (base, c))

    # 7. русский текст внутри рисунка (illustrations/* и chapters/*) — error
    # opt-out: data-text-ok="diagram" на корневом <svg> (коммутативные диаграммы легальны)
    TEXT_NODE_RE = re.compile(r"<(text|tspan|figcaption)\b[^>]*>(.*?)</\1>", re.S)

    def _svg_opts_out(content):
        m = re.search(r"<svg\b[^>]*>", content)
        return bool(m and 'data-text-ok="diagram"' in m.group(0))

    cyr_sources = [("illustrations/%s" % n, filemap.get("{{ILL:%s}}" % n, ""))
                   for n in names.get("illustrations", [])]
    cyr_sources += [("chapters/%s" % n, filemap.get("{{CHAPTER:%s}}" % n, ""))
                    for n in names.get("chapters", [])]
    for path, content in cyr_sources:
        if _svg_opts_out(content):
            continue
        found = []
        for m in TEXT_NODE_RE.finditer(content):
            inner = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(2))).strip()
            if inner and CYR.search(inner):
                found.append((m.group(1), inner))
        if found:
            tag, sample = found[0]
            errors.append('%s: русский текст в рисунке — <%s> «%s» (всего таких узлов %d). '
                          'Буквы выносятся в текст слайда. Коммутативная диаграмма — поставь '
                          'data-text-ok="diagram" на корневой <svg>.' % (path, tag, sample, len(found)))

    # 7b. (мягко) кириллица, рисуемая кодом sims/**/*.js — второй проход, обходит проверку выше
    # opt-out: комментарий "// text-ok: hint" на той же строке (подсказки взаимодействия легальны)
    SIM_TEXT_RE = re.compile(r"(fillText|textContent\s*=)\s*\(?\s*(['\"`])(.*?)\2")
    sim_sources = []
    if "{{SIM:lab.core}}" in filemap:
        sim_sources.append(("sims/lab.core.js", filemap["{{SIM:lab.core}}"]))
    for n in names.get("sims", []):
        sim_sources.append(("sims/ext/%s.js" % n, filemap.get("{{SIM:%s}}" % n, "")))
    for path, content in sim_sources:
        for line in content.splitlines():
            if "text-ok: hint" in line:
                continue
            m = SIM_TEXT_RE.search(line)
            if m and CYR.search(m.group(3)):
                kind = "fillText" if m.group(1) == "fillText" else "textContent"
                warns.append('%s: %s с русским текстом «%s» — подпись рисуется кодом и обходит '
                             'проверку рисунков. Подсказка взаимодействия — пометь // text-ok: hint.'
                             % (path, kind, re.sub(r"\s+", " ", m.group(3)).strip()))

    # 8. порция текста на клик — error, порог 4 (худший слайд эталона buffon/sl-polygons).
    # Только слайды с реальной сменой сцен (data-scenes>1): у односценового слайда весь
    # текст показан сразу при входе, «клика» как такового нет — метрика о нём не судит.
    for sid, shtml in _slide_sections(assembled):
        msc = re.search(r'data-scenes="(\d+)"', shtml)
        if not msc or int(msc.group(1)) <= 1:
            continue
        body = re.sub(r"<(script|style|template)\b.*?</\1>", " ", shtml, flags=re.S)
        # `<details>` раскрывает КНОПКА ЧИТАТЕЛЯ, а не кликер докладчика: в зале этот
        # текст не появляется ни на одной сцене, и метрика «порция текста на клик»
        # о нём не судит. Без этой строки комментарий-подстрочник считался бы текстом
        # первой сцены и переводил слайд через порог 4 на ровном месте.
        body = re.sub(r"<details\b.*?</details>", " ", body, flags=re.S)
        buckets = {}
        for m in re.finditer(r"<(p|li)\b([^>]*)>(.*?)</\1>", body, re.S):
            text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(3))).strip()
            if not text:
                continue
            msf = re.search(r'data-scene-from="(\d+)"', m.group(2))
            scene = int(msf.group(1)) if msf else 1
            buckets[scene] = buckets.get(scene, 0) + 1
        if buckets:
            scene, count = max(buckets.items(), key=lambda kv: kv[1])
            if count > 4:
                errors.append('slides/%s.html: на сцене %d раскрывается %d текстовых блоков разом '
                              '(порог 4 — худший слайд эталона buffon/sl-polygons). Дроби сцены: '
                              '{@N} по абзацу, SLIDE-FORMAT.md стр. 16.' % (sid, scene, count))

    # 9. потолок сцен — error, а не молчаливые мегабайты CSS (SCENE_CAP выше).
    # Судим КАЖДЫЙ слайд отдельно: `max_scenes` ловит и `data-scenes`, и
    # `data-scene-from`/`-until` — опечатка в любом из трёх раздувает каскад.
    for sid, shtml in _slide_sections(assembled):
        n = max_scenes(shtml)
        if n > SCENE_CAP:
            errors.append('slides/%s.html: data-scenes/data-scene-from/-until даёт %d — выше '
                          'потолка %d (build_deck.py:SCENE_CAP). Опечатка в числе? Каскад растёт '
                          'квадратично, молчаливые мегабайты CSS не собираем.' % (sid, n, SCENE_CAP))

    return errors, warns, assembled


# ───────────────────────── самопроверка-статистика ─────────────────────────
def stats_line(assembled, names):
    return ("слайдов:%d  шаблонов(иллюстраций):%d  глав(3D):%d  драйверов:%d  sims:%d  вес:%dКБ"
            % (len(names.get("slides", [])) + len(names.get("generated", [])),
               len(names.get("illustrations", [])),
               len(names.get("chapters", [])), len(names.get("drivers", [])),
               len(names.get("sims", [])),
               len(assembled.encode("utf-8")) // 1024))


# ───────────────────────── CLI ─────────────────────────
def main():
    ap = argparse.ArgumentParser(description="Генератор src/ → self-contained index.html + линтер")
    ap.add_argument("src", help="папка-источник (содержит shablon.html, brief.md, tokens.css, …)")
    ap.add_argument("--lint", action="store_true", help="только линтер, без сборки")
    ap.add_argument("-o", "--out", help="путь выхода (по умолчанию <src>/dist/index.html)")
    ap.add_argument("--no-banner", dest="banner", action="store_false", default=True,
                    help="НЕ добавлять HTML-коммент «СГЕНЕРИРОВАНО…» в шапку. По умолчанию "
                         "баннер ВКЛ и render-neutral (комментарий не влияет на пиксели). "
                         "Флаг нужен только для byte-exact сверки выхода с оригиналом.")
    args = ap.parse_args()

    src = Path(args.src)
    shablon, filemap, meta, names = load_source(src)

    errors, warns, assembled = lint(shablon, filemap, meta, names)
    print("── ЛИНТЕР ──")
    for w in warns:
        print("  ⚠ %s" % w)
    if errors:
        for e in errors:
            print("  ✗ %s" % e)
        print("ЛИНТЕР ПРОВАЛЕН: %d структурн. ошибк(а/и). Сборка прервана." % len(errors))
        return 1
    print("  ✓ структурные проверки пройдены (%d мягк. предупрежд.)" % len(warns))
    print("  " + stats_line(assembled, names))

    if args.lint:
        return 0

    out_path = Path(args.out) if args.out else (src / "dist" / "index.html")
    if args.banner:
        # баннер СРАЗУ ПОСЛЕ строки <!DOCTYPE html>, чтобы ничего не предшествовало
        # доктайпу (иначе риск quirks-mode); HTML-комментарий рендер не меняет.
        nl = assembled.find("\n") + 1
        out_text = assembled[:nl] + GEN_BANNER + assembled[nl:] if nl else GEN_BANNER + assembled
    else:
        out_text = assembled
    write_text(out_path, out_text)
    print("── СБОРКА ──")
    print("  ✓ %s (%d КБ)" % (out_path, len(out_text.encode("utf-8")) // 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
