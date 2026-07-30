#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
promer_dekov.py — пер-слайдовый ПРОМЕР собранных деков (`index.html`) в числах.

Зачем: у фабрики есть машинные гейты (переполнение, знаки, сцены) и ни одного
критерия «понятно и красиво ли это человеку». Этот скрипт — попытка выразить
«красиво» замерами, чтобы можно было сравнить эталонный дек (buffon) с теми,
которые владельцу не нравятся, и увидеть РАСХОЖДЕНИЕ РАСПРЕДЕЛЕНИЙ, а не мнение.

Запуск (из корня репо, повторяемо, stdlib-only):
    python3 _studio/zhurnal/2026-07-30_dovodka-fabriki/promer_dekov.py
    python3 .../promer_dekov.py --deck buffon/index.html --deck fibonacci/src/dist/index.html
    python3 .../promer_dekov.py --tsv        # пер-слайдовая таблица машинно-читаемо

ТРИ ЛОВУШКИ, которые здесь закрыты (иначе таблица красивая и ложная):

1. Иллюстрации на слайде физически ОТСУТСТВУЮТ. В `<section>` стоит пустой бокс
   `<div class="ill-box" data-ill="NAME">`, а картинка лежит в `<template id="ill-NAME">`
   в блоке [3] и инъектируется движком в рантайме. Наивный подсчёт «<svg> внутри
   <section>» даёт НОЛЬ иллюстраций у всех четырёх деков. Поэтому resolve_ills():
   data-ill → <template id="ill-NAME">, data-iframe="tpl-X" → <script type="text/html" id="tpl-X">.

2. KaTeX удваивает и текст, и inline-стили. Формула = <span class="katex-mathml">
   (MathML + <annotation> с TeX-исходником) + <span class="katex-html" aria-hidden="true">
   (видимый рендер, нашпигованный style="height:…"). Поэтому:
   - katex-mathml вырезается целиком (иначе каждая формула считается дважды, плюс в
     «знаки видимого текста» попадает TeX-исходник);
   - style= внутри .katex НЕ считается «индивидуальностью слайда» (иначе у teorkat
     inline-стилей вчетверо больше, чем у buffon, — артефакт числа формул).

3. CSS-селекторы нельзя грепать по всему файлу: у dandelin `#include`/`#endif`/`#define`
   — это GLSL-шейдеры внутри 3D-глав, 1100+ ложных «id-селекторов». Scoped-CSS
   считается ТОЛЬКО внутри <style>-блоков.

Нумерация слайдов — С ЕДИНИЦЫ и всегда рядом с `id` секции: предыдущий промер этой
фабрики нумеровал с нуля, и три захода спорили о разных слайдах под одним номером.
"""
import re, sys, json, argparse, statistics
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]

DECKS = [
    ("buffon",   "buffon/index.html"),                     # эталон: «приятно взаимодействовать»
    ("teorkat",  "teorkat-vvedenie/src/dist/index.html"),  # «первые 15 слайдов сделаны плохо»
    ("fibonacci","fibonacci/src/dist/index.html"),         # «неприятно открывать»
    ("dandelin", "dandelin/index.html"),                   # эталон стиля РИСУНКА
]

CYR = re.compile(r"[а-яА-ЯёЁ]")


# ─────────────────────────── общие резалки разметки ───────────────────────────
def cut_tags(s, *tagnames):
    """Вырезать элементы вместе с содержимым (по именам тегов), с учётом вложенности
    одноимённых. Регексп-парсинг допустим: деки машинно-порождены и однородны."""
    for tag in tagnames:
        pat = re.compile(r"<%s\b" % tag, re.I)
        close = re.compile(r"</%s\s*>" % tag, re.I)
        out, pos = [], 0
        while True:
            m = pat.search(s, pos)
            if not m:
                out.append(s[pos:])
                break
            out.append(s[pos:m.start()])
            depth, i = 1, m.end()
            while depth:
                nxt_o, nxt_c = pat.search(s, i), close.search(s, i)
                if not nxt_c:
                    i = len(s)
                    break
                if nxt_o and nxt_o.start() < nxt_c.start():
                    depth += 1
                    i = nxt_o.end()
                else:
                    depth -= 1
                    i = nxt_c.end()
            pos = i
        s = "".join(out)
    return s


def cut_class_spans(s, cls):
    """Вырезать <span class="…cls…">…</span> вместе с содержимым (вложенность span учтена).
    Нужно для katex-mathml: он несёт MathML-дубль формулы и TeX-исходник в <annotation>."""
    open_re = re.compile(r'<span\b[^>]*class="[^"]*\b%s\b[^"]*"[^>]*>' % re.escape(cls))
    span_o = re.compile(r"<span\b", re.I)
    span_c = re.compile(r"</span\s*>", re.I)
    out, pos = [], 0
    while True:
        m = open_re.search(s, pos)
        if not m:
            out.append(s[pos:])
            break
        out.append(s[pos:m.start()])
        depth, i = 1, m.end()
        while depth:
            nxt_o, nxt_c = span_o.search(s, i), span_c.search(s, i)
            if not nxt_c:
                i = len(s)
                break
            if nxt_o and nxt_o.start() < nxt_c.start():
                depth += 1
                i = nxt_o.end()
            else:
                depth -= 1
                i = nxt_c.end()
        pos = i
    s = "".join(out)
    return s


def visible_text(html):
    """Видимый текст: без script/style/template, без MathML-дубля KaTeX, без разметки.
    Сущности разворачиваются, пробелы схлопываются."""
    s = cut_tags(html, "script", "style", "template")
    s = cut_class_spans(s, "katex-mathml")
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = (s.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<")
          .replace("&gt;", ">").replace("&quot;", '"').replace("&#8203;", "")
          .replace("​", ""))
    return re.sub(r"\s+", " ", s).strip()


# ─────────────────────────── разбор дека ───────────────────────────
def split_slides(doc):
    """[(idx1, id, html)] — секции слайдов В ПОРЯДКЕ ФАЙЛА, нумерация С 1.
    Возвращает также список НЕ РАЗОБРАННЫХ (секция без id) — молча в ноль не уходит."""
    slides, unparsed = [], []
    for n, m in enumerate(re.finditer(r'<section\b[^>]*class="[^"]*\bslide\b[^"]*"[^>]*>', doc), 1):
        head = m.group(0)
        end = doc.find("</section>", m.end())
        if end == -1:
            unparsed.append((n, "?", "нет закрывающего </section>"))
            continue
        body = doc[m.start():end + len("</section>")]
        mid = re.search(r'\bid="([^"]+)"', head)
        if not mid:
            unparsed.append((n, "?", "у секции нет id"))
            continue
        slides.append((n, mid.group(1), body))
    return slides, unparsed


def asset_registry(doc):
    """{name: html} — реестры ассетов: <template id="ill-NAME"> и 3D-главы
    <script type="text/html" id="tpl-NAME">. Плюс список продублированных id.

    🔴 ПЕРВОЕ вхождение выигрывает, а не последнее. Движок достаёт ассет через
    getElementById, который возвращает ПЕРВЫЙ элемент с этим id; все следующие
    недостижимы. У dandelin реально 10 тегов `<script id="tpl-…">` на 8 уникальных
    имён: `tpl-mirror` и `tpl-tangent` объявлены ДВАЖДЫ, причём содержимое дублей
    РАЗНОЕ. Первая версия этой функции складывала в dict и оставляла последнее —
    и слайды s07/s07b получали пустые дубли вместо живых картинок: 8 текстовых
    узлов, 3 из них кириллицей, пропадали из замера. (build_deck.py lint() знает
    про эти дубли, но только мягким warn — см. его строку 298.)
    """
    reg, dupes = {}, []
    for m in re.finditer(r'<template\b[^>]*\bid="ill-([^"]+)"[^>]*>(.*?)</template>', doc, re.S):
        key = "ill:" + m.group(1)
        if key in reg:
            dupes.append(key)
            continue
        reg[key] = m.group(2)
    # содержимое <script> кончается на ПЕРВОМ настоящем `</script>`: вложенные
    # закрытия внутри 3D-главы экранированы как `<\/script`, поэтому нежадный
    # захват совпадает с тем, что видит парсер браузера (проверено по dandelin).
    for m in re.finditer(r'<script\b[^>]*type="text/html"[^>]*\bid="tpl-([^"]+)"[^>]*>(.*?)</script>',
                         doc, re.S):
        key = "tpl:" + m.group(1)
        if key in reg:
            dupes.append(key)
            continue
        reg[key] = m.group(2)
    return reg, dupes


def scene_window(tag_html):
    """(from, until) из data-scene-from/until на теге; None = без ограничения.
    Проверено: у всех четырёх деков сцена-гейт стоит на САМОМ теге с data-ill
    (контейнеров-предков со сценой, содержащих data-ill, — 0), поэтому окно
    видимости иллюстрации читается из её собственного тега."""
    mf = re.search(r'data-scene-from="(\d+)"', tag_html)
    mu = re.search(r'data-scene-until="(\d+)"', tag_html)
    return (int(mf.group(1)) if mf else None, int(mu.group(1)) if mu else None)


def resolve_ills(slide_html, reg):
    """Иллюстрации слайда как список dict(kind, name, html, from, until). Источники:
    (1) data-ill= → template из реестра; (2) data-iframe="tpl-X" → 3D-глава;
    (3) inline <svg>/<img>/<canvas>/<figure>, лежащие прямо в секции.
    Отсутствие имени в реестре — отдельная запись MISSING (не молчание)."""
    ills, missing = [], []
    for m in re.finditer(r'<[a-zA-Z]+[^>]*data-ill="([^"]+)"[^>]*>', slide_html):
        name, tag = m.group(1), m.group(0)
        key = "ill:" + name
        if key not in reg:
            missing.append(name)
            continue
        f, u = scene_window(tag)
        ills.append({"kind": "template", "name": name, "html": reg[key], "from": f, "until": u})
    for m in re.finditer(r'<[a-zA-Z]+[^>]*data-iframe="tpl-([^"]+)"[^>]*>', slide_html):
        name, tag = m.group(1), m.group(0)
        key = "tpl:" + name
        if key not in reg:
            missing.append("tpl-" + name)
            continue
        f, u = scene_window(tag)
        ills.append({"kind": "iframe3d", "name": name, "html": reg[key], "from": f, "until": u})
    # inline-графика прямо в секции (не через реестр)
    for tag in ("svg", "figure"):
        for m in re.finditer(r"<%s\b" % tag, slide_html):
            frag = extract_element(slide_html, m.start(), tag)
            f, u = scene_window(frag[:frag.find(">") + 1])
            ills.append({"kind": "inline-" + tag, "name": tag, "html": frag, "from": f, "until": u})
    for m in re.finditer(r"<(img|canvas)\b[^>]*>", slide_html):
        f, u = scene_window(m.group(0))
        ills.append({"kind": "inline-" + m.group(1), "name": m.group(1),
                     "html": m.group(0), "from": f, "until": u})
    return ills, missing


def visible_at(ill, scene):
    f, u = ill["from"], ill["until"]
    return (f is None or scene >= f) and (u is None or scene <= u)


def extract_element(s, start, tag):
    """Подстрока элемента <tag …>…</tag>, начиная с позиции start, с учётом вложенности."""
    open_re = re.compile(r"<%s\b" % tag, re.I)
    close_re = re.compile(r"</%s\s*>" % tag, re.I)
    depth, i = 1, start + 1
    while depth:
        nxt_o, nxt_c = open_re.search(s, i), close_re.search(s, i)
        if not nxt_c:
            return s[start:]
        if nxt_o and nxt_o.start() < nxt_c.start():
            depth += 1
            i = nxt_o.end()
        else:
            depth -= 1
            i = nxt_c.end()
    return s[start:i]


def ill_area(html, kind=None):
    """Объявленная площадь иллюстрации в px² — ТОЛЬКО по КОРНЕВОМУ элементу.

    🔴 Читать корневой тег, а не искать width/height по всему фрагменту, обязательно:
    первая версия этой функции хватала `width="180" height="90"` у первого <rect>
    ВНУТРИ svg и печатала для титульной иллюстрации fibonacci 270 px² вместо
    216 000 (viewBox 1200×180) — то есть ровно то фальшивое «миллион мелких картинок»,
    которое заход просил проверить, а не подтвердить.

    Порядок: width/height атрибуты корня → viewBox корня → width/height в style корня.
    None — размер не объявлен (слайд не даёт числа; это видно в таблице, а не 0).

    ⚠ ЧТО ЭТО ЧИСЛО ЗНАЧИТ: у SVG канона стоит style="width:100%;height:100%" +
    preserveAspectRatio, т.е. РЕНДЕР-размер задаёт грид-CSS панели, а не сам SVG.
    Поэтому viewBox-площадь — это координатное пространство и ПРОПОРЦИЯ рисунка,
    а не пиксели на экране. Для «мелких картинок на экране» смысл несёт
    `одновременно видимых илл. на сцене` (ниже), а не эта колонка.
    """
    root = html[:html.find(">") + 1] if ">" in html else html
    mw = re.search(r'\bwidth="(\d+(?:\.\d+)?)(?:px)?"', root)
    mh = re.search(r'\bheight="(\d+(?:\.\d+)?)(?:px)?"', root)
    if mw and mh:
        return float(mw.group(1)) * float(mh.group(1))
    mv = re.search(r'viewBox="\s*[-\d.]+[ ,]+[-\d.]+[ ,]+([\d.]+)[ ,]+([\d.]+)', root)
    if mv:
        return float(mv.group(1)) * float(mv.group(2))
    ms_w = re.search(r'style="[^"]*\bwidth:\s*(\d+(?:\.\d+)?)px', root)
    ms_h = re.search(r'style="[^"]*\bheight:\s*(\d+(?:\.\d+)?)px', root)
    if ms_w and ms_h:
        return float(ms_w.group(1)) * float(ms_h.group(1))
    return None


def ill_text_nodes(html):
    """(всего текстовых узлов внутри рисунка, из них с кириллицей).
    Считаются <text> и <tspan> внутри SVG + <figcaption> внутри <figure>.
    Пустые/пробельные узлы не считаются: они ничего не показывают человеку.
    tspan внутри text не удваивает — узел засчитывается по внешнему <text>."""
    total, cyr = 0, 0
    for m in re.finditer(r"<text\b[^>]*>(.*?)</text>", html, re.S):
        t = re.sub(r"<[^>]+>", "", m.group(1))
        t = re.sub(r"\s+", " ", t).strip()
        if not t:
            continue
        total += 1
        if CYR.search(t):
            cyr += 1
    body_wo_text = re.sub(r"<text\b[^>]*>.*?</text>", " ", html, flags=re.S)
    for m in re.finditer(r"<(tspan|figcaption)\b[^>]*>(.*?)</\1>", body_wo_text, re.S):
        t = re.sub(r"<[^>]+>", "", m.group(2))
        t = re.sub(r"\s+", " ", t).strip()
        if not t:
            continue
        total += 1
        if CYR.search(t):
            cyr += 1
    return total, cyr


def text_blocks(slide_html):
    """Текстовых блоков: <p> + <li> + заголовки (h1-h4 и канон-зоны .head/.title/.nomer).
    Внутри template/script/style не считаем; пустые блоки не считаем."""
    s = cut_tags(slide_html, "script", "style", "template")
    s = cut_class_spans(s, "katex-mathml")
    n = 0
    for m in re.finditer(r"<(p|li|h1|h2|h3|h4)\b[^>]*>(.*?)</\1>", s, re.S):
        t = re.sub(r"<[^>]+>", "", m.group(2))
        if re.sub(r"[\s​]+", "", t):
            n += 1
    return n


def has_heading(slide_html):
    """Видимый заголовок слайда: h1-h4 с текстом ИЛИ канон-зона класса head/title/zag."""
    s = cut_tags(slide_html, "script", "style", "template")
    for m in re.finditer(r"<(h1|h2|h3|h4)\b[^>]*>(.*?)</\1>", s, re.S):
        if re.sub(r"<[^>]+>|\s", "", m.group(2)):
            return True
    for m in re.finditer(r'<(\w+)\b[^>]*class="[^"]*\b(head|title|zag|zagolovok)\b[^"]*"[^>]*>',
                         s):
        frag = extract_element(s, m.start(), m.group(1))
        if re.sub(r"<[^>]+>|\s", "", frag):
            return True
    return False


def scenes(slide_html):
    """Сцен на слайде. Механика движка (SLIDE-FORMAT.md): число сцен задаётся
    data-scenes="N" на <section>. Атрибута нет → слайд односценовый (1)."""
    m = re.search(r'\bdata-scenes="(\d+)"', slide_html)
    return int(m.group(1)) if m else 1


KATEX_FONT = re.compile(r"^katex_", re.I)


def font_families(*chunks):
    """Уникальные font-family из переданных кусков. KaTeX-гарнитуры (KaTeX_Main,
    KaTeX_Math, …) исключаются: их печёт формульный движок, к дизайну слайда они
    отношения не имеют, а иначе у любого дека с формулами «13 гарнитур»."""
    fams = set()
    for chunk in chunks:
        for m in re.finditer(r"font-family\s*:\s*([^;\"'}]+)", chunk or ""):
            v = re.sub(r"\s+", " ", m.group(1)).strip().strip(",").lower()
            if not v or KATEX_FONT.match(v):
                continue
            fams.add(v)
    return fams


def scoped_css_text(css, slide_id):
    """Текст всех CSS-правил, привязанных к id этого слайда — тут живут его шрифт,
    цвет и геометрия (в inline-стилях слайдов канона их почти нет)."""
    css = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)
    out = []
    for m in re.finditer(r"([^{}@]+)\{([^{}]*)\}", css):
        if re.search(r"#%s(?![\w-])" % re.escape(slide_id), m.group(1)):
            out.append(m.group(2))
    return "\n".join(out)


def inline_styles_no_katex(slide_html):
    """Все style="…" слайда, КРОМЕ находящихся внутри .katex (там KaTeX печёт
    height/vertical-align тысячами — это не дизайн слайда)."""
    s = cut_class_spans(slide_html, "katex")
    return re.findall(r'style="([^"]*)"', s)


def deck_style_blocks(doc):
    """Содержимое всех <style>…</style> — единственное законное место поиска CSS-правил
    (в остальном файле '#'-токены дают GLSL-шейдеры 3D-глав)."""
    return "\n".join(re.findall(r"<style\b[^>]*>(.*?)</style>", doc, re.S))


def scoped_rules(css, slide_ids):
    """{slide_id: число CSS-правил, привязанных к этому слайду по id}.
    Правило = один блок «селектор { … }». Селектор с несколькими id-слайдами
    (#sl-a, #sl-b { … }) засчитывается КАЖДОМУ — правило и правда индивидуализирует оба."""
    css = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)
    css = re.sub(r"@(?:media|supports)[^{]*\{", " ", css)  # раскрываем обёртки, правила внутри учтутся
    per = {sid: 0 for sid in slide_ids}
    for m in re.finditer(r"([^{}@]+)\{([^{}]*)\}", css):
        sel = m.group(1)
        if not m.group(2).strip():
            continue
        for sid in slide_ids:
            if re.search(r"#%s(?![\w-])" % re.escape(sid), sel):
                per[sid] += 1
    return per


HEXCOL = re.compile(r"#[0-9a-fA-F]{3,8}\b")
FUNCCOL = re.compile(r"\b(?:rgba?|hsla?)\([^)]*\)")

# Подписи, которые РИСУЮТСЯ КОДОМ, а не лежат текстовым узлом: canvas.fillText(),
# element.textContent=. Их не видит ни одна структурная метрика выше, а на экране
# они есть. Нашёл верификатор захода: колонка ill_text_cyr давала «у buffon и
# fibonacci кириллицы в рисунках ноль», и это верно СТРУКТУРНО, но у buffon в
# симуляции есть «потяни точку или иглу», а у fibonacci четыре таких подписи.
JS_TEXT = re.compile(r"""(fillText|textContent\s*=|innerHTML\s*=)\s*\(?\s*(['"`])(.*?)\2""", re.S)


def js_drawn_cyrillic(doc):
    """[(вид, текст)] — подписи с кириллицей, которые печатает JS. Считается по ВСЕМУ
    документу: приписать их конкретному слайду нельзя, симуляция переиспользуется."""
    out = []
    for m in JS_TEXT.finditer(doc):
        if CYR.search(m.group(3)):
            out.append((m.group(1).rstrip(" ="), re.sub(r"\s+", " ", m.group(3)).strip()))
    return out


def deck_totals(doc, slides, reg):
    """Три сводных числа на дек (задание §1, «отдельно, одним числом на дек»)."""
    css = deck_style_blocks(doc)
    fams = font_families(css, *[h for _, _, h in slides], *reg.values())

    # цвета в inline-стилях слайдов (как просит задание) — у канона их почти нет:
    # палитра живёт в CSS-переменных, поэтому рядом даём цвета из scoped-CSS.
    colors = set()
    for _, _, html in slides:
        for st in inline_styles_no_katex(html):
            colors |= {c.lower() for c in HEXCOL.findall(st)}
            colors |= {re.sub(r"\s+", "", c).lower() for c in FUNCCOL.findall(st)}
    scoped_colors = set()
    for _, sid, _ in slides:
        st = scoped_css_text(css, sid)
        scoped_colors |= {c.lower() for c in HEXCOL.findall(st)}
        scoped_colors |= {re.sub(r"\s+", "", c).lower() for c in FUNCCOL.findall(st)}
    ill_colors = set()
    for v in reg.values():
        ill_colors |= {c.lower() for c in HEXCOL.findall(v)}

    ids = [sid for _, sid, _ in slides]
    per = scoped_rules(css, ids)
    return {
        "font_families_deck": sorted(fams),
        "inline_colors_slides": sorted(colors),
        "scoped_colors_slides": sorted(scoped_colors),
        "ill_hex_colors": sorted(ill_colors),
        "scoped_rules_total": sum(per.values()),
        "per_slide_scoped": per,
    }


def measure_deck(name, relpath):
    path = REPO / relpath
    doc = path.read_text(encoding="utf-8", errors="replace")
    slides, unparsed = split_slides(doc)
    reg, dup_ids = asset_registry(doc)
    css = deck_style_blocks(doc)
    per_scoped = scoped_rules(css, [sid for _, sid, _ in slides])

    rows, missing_all = [], []
    for n, sid, html in slides:
        ills, missing = resolve_ills(html, reg)
        missing_all += [(sid, x) for x in missing]
        nsc = scenes(html)
        areas = [a for a in (ill_area(i["html"]) for i in ills) if a is not None]
        tn = cn = 0
        for i in ills:
            a, b = ill_text_nodes(i["html"])
            tn += a
            cn += b
        # одновременно видимых иллюстраций — максимум по сценам (гипотеза 1: «полоса,
        # забитая мелкими картинками» — это про ОДНОВРЕМЕННО видимое, а не про сумму
        # по всем сценам: у fibonacci три картинки слайда 2 сменяют друг друга)
        best_n, best_min = 0, None
        for s in range(1, nsc + 1):
            vis_ills = [i for i in ills if visible_at(i, s)]
            if len(vis_ills) > best_n:
                ar = [a for a in (ill_area(i["html"]) for i in vis_ills) if a is not None]
                best_n, best_min = len(vis_ills), (min(ar) if ar else None)
        scss = scoped_css_text(css, sid)
        rows.append({
            "n": n, "id": sid,
            "chars": len(visible_text(html)),
            "blocks": text_blocks(html),
            "ills": len(ills),
            "ills_visible_max": best_n,
            "min_area_visible": best_min,
            "min_area": min(areas) if areas else None,
            "areas_declared": len(areas),
            "ill_text_nodes": tn,
            "ill_text_cyr": cn,
            "fonts": len(font_families(html, scss, *[i["html"] for i in ills])),
            "scenes": nsc,
            "heading": has_heading(html),
            "scoped": per_scoped.get(sid, 0),
        })
    declared = len(re.findall(r'<section\b[^>]*class="[^"]*\bslide\b[^"]*"', doc))
    # ассеты-сироты: лежат в реестре, ни один слайд не ссылается (мёртвый вес в
    # самодостаточном монолите). build_deck.py их warn'ит на сборке, но в СОБРАННОМ
    # файле уже никто не проверяет.
    used = set()
    for _, _, html in slides:
        used |= {"ill:" + x for x in re.findall(r'data-ill="([^"]+)"', html)}
        used |= {"tpl:" + x for x in re.findall(r'data-iframe="tpl-([^"]+)"', html)}
    return {
        "deck": name, "path": relpath,
        "slides_declared": declared, "slides_parsed": len(rows),
        "unparsed": unparsed, "missing_assets": missing_all,
        "dup_asset_ids": dup_ids, "orphan_assets": sorted(set(reg) - used),
        "js_cyrillic": js_drawn_cyrillic(doc),
        "rows": rows, "totals": deck_totals(doc, slides, reg),
    }


# ─────────────────────────── вывод ───────────────────────────
def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def fmt(v):
    if v is None:
        return "—"
    if isinstance(v, float):
        return "%.0f" % v
    return str(v)


def print_deck(d):
    print("\n" + "=" * 108)
    print("ДЕК %s  —  %s" % (d["deck"].upper(), d["path"]))
    print("ОХВАТ: обработано %d из %d слайдов" % (d["slides_parsed"], d["slides_declared"]))
    if d["unparsed"]:
        print("НЕ РАЗОБРАНО (%d):" % len(d["unparsed"]))
        for n, sid, why in d["unparsed"]:
            print("   слайд %d (%s): %s" % (n, sid, why))
    else:
        print("НЕ РАЗОБРАНО: 0")
    if d["missing_assets"]:
        print("ССЫЛКИ БЕЗ АССЕТА (%d): %s" % (len(d["missing_assets"]), d["missing_assets"]))
    print("ДУБЛИРОВАННЫЕ id ассетов (2-е вхождение недостижимо через getElementById): %d %s"
          % (len(d["dup_asset_ids"]), d["dup_asset_ids"] or ""))
    print("АССЕТЫ-СИРОТЫ (в реестре, ни один слайд не ссылается): %d %s"
          % (len(d["orphan_assets"]), d["orphan_assets"] or ""))
    print("-" * 108)
    print("%-3s %-18s %6s %5s %4s %4s %10s %6s %6s %5s %5s %4s %6s" %
          ("№", "id", "знаков", "блок", "илл", "одн", "минS,px²", "узлТ", "КИРИЛ",
           "шрфт", "сцен", "заг", "scoped"))
    print("-" * 108)
    for r in d["rows"]:
        print("%-3d %-18s %6d %5d %4d %4d %10s %6d %6s %5d %5d %4s %6d" %
              (r["n"], r["id"][:18], r["chars"], r["blocks"], r["ills"],
               r["ills_visible_max"], fmt(r["min_area"]), r["ill_text_nodes"],
               ("**%d**" % r["ill_text_cyr"]) if r["ill_text_cyr"] else "0",
               r["fonts"], r["scenes"], "да" if r["heading"] else "НЕТ", r["scoped"]))
    t = d["totals"]
    rows = d["rows"]
    print("-" * 108)
    print("МЕДИАНЫ: знаков=%s блоков=%s илл=%s минS=%s узлТ=%s кирил=%s сцен=%s scoped=%s" % (
        fmt(med([r["chars"] for r in rows])), fmt(med([r["blocks"] for r in rows])),
        fmt(med([r["ills"] for r in rows])), fmt(med([r["min_area"] for r in rows])),
        fmt(med([r["ill_text_nodes"] for r in rows])), fmt(med([r["ill_text_cyr"] for r in rows])),
        fmt(med([r["scenes"] for r in rows])), fmt(med([r["scoped"] for r in rows]))))
    print("МАКСИМУМЫ: знаков=%d блоков=%d илл=%d узлТ=%d кирил=%d сцен=%d scoped=%d" % (
        max(r["chars"] for r in rows), max(r["blocks"] for r in rows),
        max(r["ills"] for r in rows), max(r["ill_text_nodes"] for r in rows),
        max(r["ill_text_cyr"] for r in rows), max(r["scenes"] for r in rows),
        max(r["scoped"] for r in rows)))
    print("СВОДНО ПО ДЕКУ: font-family уник (без KaTeX-гарнитур)=%d %s"
          % (len(t["font_families_deck"]), t["font_families_deck"]))
    print("                уник цветов в inline-стилях слайдов (без KaTeX)=%d %s"
          % (len(t["inline_colors_slides"]), t["inline_colors_slides"]))
    print("                уник цветов в scoped-CSS слайдов=%d %s"
          % (len(t["scoped_colors_slides"]), t["scoped_colors_slides"]))
    print("                уник hex-цветов в иллюстрациях=%d" % len(t["ill_hex_colors"]))
    print("                CSS-правил, привязанных к id слайда (scoped)=%d, на слайд=%.1f"
          % (t["scoped_rules_total"], t["scoped_rules_total"] / max(1, len(rows))))
    print("                текстовых узлов в рисунках ВСЕГО по деку=%d; из них кириллицей=%d"
          % (sum(r["ill_text_nodes"] for r in rows), sum(r["ill_text_cyr"] for r in rows)))
    print("                слайдов с КИРИЛЛИЦЕЙ в рисунке=%d из %d; узлов кириллицы всего=%d"
          % (sum(1 for r in rows if r["ill_text_cyr"]), len(rows),
             sum(r["ill_text_cyr"] for r in rows)))
    print("                🔴 КИРИЛЛИЦА, РИСУЕМАЯ КОДОМ (fillText/textContent — структурных")
    print("                   метрик НЕ касается, но на экране есть): %d %s"
          % (len(d["js_cyrillic"]), [t for _, t in d["js_cyrillic"]][:4] or ""))
    print("                блоков текста на сцену: медиана=%.2f макс=%.2f"
          % (med([r["blocks"] / r["scenes"] for r in rows]),
             max(r["blocks"] / r["scenes"] for r in rows)))
    print("                слайдов БЕЗ заголовка=%d из %d"
          % (sum(1 for r in rows if not r["heading"]), len(rows)))


def print_compare(ds):
    """Расхождение распределений: «у скольких слайдов метрика ХУЖЕ, чем худший слайд Бюффона»."""
    b = next(d for d in ds if d["deck"] == "buffon")
    print("\n" + "=" * 108)
    print("РАСХОЖДЕНИЕ РАСПРЕДЕЛЕНИЙ — база сравнения: ХУДШИЙ слайд Бюффона по каждой метрике")
    print("=" * 108)
    # (метрика, извлечь, «хуже» = больше?)
    METRICS = [
        ("знаков видимого текста", lambda r: r["chars"], True),
        ("текстовых блоков", lambda r: r["blocks"], True),
        # ПРОИЗВОДНЫЕ: сколько текста прилетает за ОДИН клик. Это и есть машинное
        # выражение G6 «мелкое дробление на сцены»: слайд с 6 абзацами и 2 сценами
        # выкладывает по 3 абзаца за клик, слайд с 6 абзацами и 6 сценами — по одному.
        ("блоков на сцену", lambda r: round(r["blocks"] / r["scenes"], 2), True),
        ("знаков на сцену", lambda r: round(r["chars"] / r["scenes"]), True),
        ("иллюстраций на слайде", lambda r: r["ills"], True),
        ("одновременно видимых илл.", lambda r: r["ills_visible_max"], True),
        ("мин.площадь одновр.видимых", lambda r: r["min_area_visible"], False),
        ("узлов текста в рисунке", lambda r: r["ill_text_nodes"], True),
        ("КИРИЛЛИЦЫ в рисунке", lambda r: r["ill_text_cyr"], True),
        ("семейств шрифтов", lambda r: r["fonts"], True),
        ("минимальная площадь илл.", lambda r: r["min_area"], False),
        ("scoped CSS-правил", lambda r: r["scoped"], False),
        ("сцен", lambda r: r["scenes"], False),
    ]
    for label, get, worse_is_more in METRICS:
        bv = [get(r) for r in b["rows"] if get(r) is not None]
        if not bv:
            continue
        thresh = max(bv) if worse_is_more else min(bv)
        print("\n%-26s порог buffon = %s  (медиана buffon %s)"
              % (label, fmt(thresh), fmt(med(bv))))
        for d in ds:
            vals = [(r["n"], r["id"], get(r)) for r in d["rows"] if get(r) is not None]
            bad = [(n, i, v) for n, i, v in vals
                   if (v > thresh if worse_is_more else v < thresh)]
            print("   %-10s медиана=%-7s макс=%-7s мин=%-7s хуже порога: %d из %d %s"
                  % (d["deck"], fmt(med([v for _, _, v in vals])),
                     fmt(max(v for _, _, v in vals)), fmt(min(v for _, _, v in vals)),
                     len(bad), len(vals),
                     ("← " + ", ".join("%d/%s=%s" % (n, i, fmt(v)) for n, i, v in bad[:6])
                      + (" …" if len(bad) > 6 else "")) if bad else ""))


def main():
    ap = argparse.ArgumentParser(description="Пер-слайдовый промер собранных деков")
    ap.add_argument("--deck", action="append", default=None,
                    help="путь к index.html (можно повторять); по умолчанию все четыре")
    ap.add_argument("--tsv", action="store_true", help="пер-слайдовая таблица в TSV")
    ap.add_argument("--json", action="store_true", help="сырые замеры в JSON")
    args = ap.parse_args()

    decks = DECKS if not args.deck else [(Path(p).parts[0], p) for p in args.deck]
    missing = [p for _, p in decks if not (REPO / p).is_file()]
    if missing:
        print("НЕТ ФАЙЛА: %s" % missing, file=sys.stderr)
        return 2

    ds = [measure_deck(n, p) for n, p in decks]

    if args.json:
        print(json.dumps(ds, ensure_ascii=False, indent=1))
        return 0
    if args.tsv:
        print("\t".join(["deck", "n", "id", "chars", "blocks", "ills", "ills_visible_max",
                         "min_area", "min_area_visible", "ill_text_nodes", "ill_text_cyr",
                         "fonts", "scenes", "heading", "scoped"]))
        for d in ds:
            for r in d["rows"]:
                print("\t".join(str(x) for x in [
                    d["deck"], r["n"], r["id"], r["chars"], r["blocks"], r["ills"],
                    r["ills_visible_max"], fmt(r["min_area"]), fmt(r["min_area_visible"]),
                    r["ill_text_nodes"], r["ill_text_cyr"],
                    r["fonts"], r["scenes"], int(r["heading"]), r["scoped"]]))
        return 0

    for d in ds:
        print_deck(d)
    if any(d["deck"] == "buffon" for d in ds):
        print_compare(ds)
    print("\nВСЕГО: %s" % ", ".join("%s %d/%d" % (d["deck"], d["slides_parsed"], d["slides_declared"])
                                    for d in ds))
    return 0


if __name__ == "__main__":
    sys.exit(main())
