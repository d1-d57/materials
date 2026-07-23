#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doc-движок (#11, движок 2 семейства _generator) — растущие markdown-документы
Фазы I (интервью → концепт → котёл → раскадровка) → ОДИН самодостаточный
HTML-вид для авторской вычитки. Модель данных: ПОТОК текста (не слайд-канвас).

    python3 build_doc.py <src-dir>           # линтер-гейт + сборка → <src>/view.html
    python3 build_doc.py <src-dir> --lint     # только линтер (без записи)
    python3 build_doc.py <src-dir> -o <path>  # выбрать выход

Семейство (см. _generator/DVIZHKI.md): markdown — источник истины, HTML — только
вид; пересборка md→HTML — чистый Python БЕЗ токенов/сети/pip (stdlib: re, sys,
argparse, pathlib, html); линтер-гейт до сборки (структурная ошибка → exit 1).
Брат — `build_deck.py` (движок 1, слайд-канвас); намеренно НЕ сливаем в общую
библиотеку (разные модели данных; дистиллят-техника §4). Прародитель — `build.py`
(`kurs leto 2026/istochnik/_generator/`, в этом репо недоступен) — диалект полей
`> поле:<вид>` и `status`-гейт портированы из его дистиллята.

ПОТОКИ И ВКЛАДКИ (D1 — вид «котла»): каждый `*.md` в папке-источнике = один поток
= одна вкладка. Движок сшивает их в ОДИН HTML с CSS-only переключением вкладок
(скрытые radio + label, без сети/JS). Демо: matematika.md ‖ naupop.md.

⚠ МАТЕМАТИКА — АВТОРСКИЙ РАНТАЙМ-ВИД (Р7). Формулы набираются KaTeX через CDN —
единственная внешняя зависимость выхода, допустимая ТОЛЬКО здесь: это вид для
вычитки автором, не финальный дек. В финальном деке — статический кэш формул
(harvest_katex.py), не рантайм. Офлайн вид деградирует в сырой `$…$`, не падая.
"""
import re, sys, argparse
from pathlib import Path
from html import escape as esc

GEN_BANNER = ("<!-- ⚠ СГЕНЕРИРОВАНО ИЗ *.md ГЕНЕРАТОРОМ _generator/build_doc.py — "
             "РУКАМИ НЕ ПРАВИТЬ. Правь markdown-источник, пересобирай (0 токенов). -->\n")

# известная лестница зрелости (дистиллят-техника §3); неизвестное — не валим, warn
KNOWN_STATUS = {"skelet", "chernovik", "chistovik", "polirovka", "polno"}


# ───────────────────────── чтение/запись без трансляции переводов строк ─────────────────────────
def read_text(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


# ───────────────────────── фронтматтер (YAML-lite, порт parse_brief из build_deck) ─────────────────────────
def split_frontmatter(text):
    """'---\\n k: v \\n---' в начале файла → (meta{k:v}, тело-после). Нет шапки → ({}, text)."""
    m = re.match(r"^﻿?---\n(.*?)\n---\n?", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        lm = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if lm:
            meta[lm.group(1)] = lm.group(2).strip().strip('"')
    return meta, text[m.end():]


def first_heading(body):
    m = re.search(r"^#{1,3}\s+(.+?)\s*$", body, re.M)
    return m.group(1).strip() if m else ""


# ───────────────────────── инлайн-разметка (stash→parse→unstash математики, приём build.py) ─────────────────────────
def render_inline(text):
    """$tex$/$$tex$$ прячем в плейсхолдеры до структурной разметки (иначе '*'/'_'/'{}'
    внутри TeX ломают markdown-регексы), потом **b**→<strong>, *i*→<em>, `c`→<code>,
    [t](u)→<a>; TeX восстанавливаем ДОСЛОВНО — KaTeX-рантайм получает сырьё. HTML
    автора проходит как есть (доверенный источник, традиция семьи build_deck)."""
    stash = []

    def keep(m):
        stash.append(m.group(0))
        return "\x00M%d\x00" % (len(stash) - 1)

    text = re.sub(r"\$\$.+?\$\$", keep, text, flags=re.S)   # display-математика
    text = re.sub(r"\$[^$\n]+?\$", keep, text)              # inline-математика
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)([^*\n]+?)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\x00M(\d+)\x00", lambda m: stash[int(m.group(1))], text)
    return text


def _join(lines):
    """Склейка строк абзаца: строка на '\\' → жёсткий <br>; иначе пробел (порт build_deck)."""
    res = ""
    for i, ln in enumerate(lines):
        if i == 0:
            res = ln
        elif res.endswith("\\"):
            res = res[:-1].rstrip() + "<br>" + ln
        else:
            res = res + " " + ln
    return res


# ───────────────────────── семья полей (порт FOOTNOTE_MAP из build.py) ─────────────────────────
# markdown-примитив `> поле:<вид> …` → HTML-примитив. Grounded в distillat-format-teksta:
# .mn (float-жёлоб), .insight (крупное прозрение/разворот), .foot (статус черновика),
# generic aside (буква ТЗ). «честно»→.mn (§3: честные пометки идут в .mn). Уровень (§5).
FIELD_MAP = {
    "":        ("aside", "note"),         # > поле: … → generic <aside> (буква ТЗ)
    "mn":      ("p",     "mn"),           # мелкая оговорка в правом жёлобе (float)
    "честно":  ("p",     "mn"),           # честная пометка → .mn (дистиллят §3)
    "insight": ("div",   "insight"),      # крупное прозрение/разворот (экономно)
    "foot":    ("p",     "foot"),         # закрывающий статус черновика
    "нить":    ("aside", "note thread"),  # сквозная нить (вокабуляр build.py)
    "cue":     ("div",   "cue"),          # cue-визуал (вокабуляр build.py)
    "уровень": ("p",     "level-line"),   # уровень мат-блока (школьно·приручение·вне-школы)
}


def render_field(kind, body):
    kind = kind.strip()
    body = body.strip()
    if kind == "insight":
        # `Тег | текст`; без '|' — тег по умолчанию «Прозрение»
        if "|" in body:
            tag, txt = body.split("|", 1)
        else:
            tag, txt = "Прозрение", body
        return ('<div class="insight"><span class="tag">%s</span> %s</div>'
                % (render_inline(tag.strip()), render_inline(txt.strip())))
    if kind == "уровень":
        return '<p class="level-line">Уровень: <span class="level">%s</span></p>' % render_inline(body)
    tag, cls = FIELD_MAP.get(kind, ("aside", "note"))
    return '<%s class="%s">%s</%s>' % (tag, cls, render_inline(body), tag)


def render_ill(text):
    """🖼 описание {N} → заметный dashed-плейсхолдер (стык с аркой 9 иллюстраций)."""
    text = text.lstrip("🖼").strip()
    scenes = ""
    sm = re.search(r"\{(\d+)\}", text)
    if sm:
        scenes = sm.group(1)
        text = re.sub(r"\s*\{\d+\}", "", text).strip()
    badge = "🖼 ИЛЛЮСТРАЦИЯ" + (" · %s сцен" % scenes if scenes else "")
    return ('<figure class="ill-ph"><div class="ill-badge">%s</div>'
            '<figcaption>%s</figcaption></figure>' % (badge, render_inline(text)))


# ───────────────────────── типы блоков-утверждений (§3 STANDART-oformlenia: зачин блока → класс) ─────────────────────────
# Автор пишет по STANDART-teksta (номер+имя+статус), движок красит сам. Имя в скобках сохраняем,
# номер метки → id-якорь (defn=d-N, thm=t-N). Курсивные зачины — логика/статус/техфакт/рассказ.
_KW_THM = ("Теорема", "Лемма", "Предложение", "Утверждение")
_BOLD_STMT = re.compile(
    r"^\*\*(Определение|Теорема|Лемма|Предложение|Утверждение|Пример|Замечание)"
    r"\s+(\d+)(.*?)\.\*\*\s*(.*)$", re.S)


def _typed_block(joined, sid):
    """Зачин блока → HTML-врезка нужного типа, либо None (пусть решают прочие ветки)."""
    m = _BOLD_STMT.match(joined)
    if m:
        kw, num, name, body = m.group(1), m.group(2), m.group(3), m.group(4)
        label = "%s %s%s." % (kw, num, name)              # имя в скобках сохранено
        if kw == "Определение":
            cls, anchor = "stmt defn", ' id="%s-d-%s"' % (sid, num)
        elif kw in _KW_THM:
            cls, anchor = "stmt thm", ' id="%s-t-%s"' % (sid, num)
        elif kw == "Пример":
            cls, anchor = "example", ""
        else:                                             # Замечание
            cls, anchor = "note", ""
        return ('<div class="%s"%s><span class="lbl">%s</span> %s</div>'
                % (cls, anchor, render_inline(label), render_inline(body)))
    # курсивный зачин: *Логика…* / *Доказательство…* / *Статус…* / *Техфакт…* / *Рассказ…*
    m = re.match(r"^\*([^*].*?)\*\s*(.*)$", joined, re.S)
    if m:
        label, body = m.group(1), m.group(2)
        head = label.lstrip()
        if head.startswith(("Логика", "Доказательство")):
            cls = "proof"
        elif head.startswith("Статус"):
            cls = "blackbox"
        elif head.startswith("Техфакт"):
            cls = "tech"
        elif head.startswith("Рассказ"):
            cls = "rasskaz"
        else:
            return None                                   # прочий курсив (*Замечание о знаке.*) — не тип-блок
        return ('<div class="%s"><span class="lbl">%s</span> %s</div>'
                % (cls, render_inline(label), render_inline(body)))
    return None


def _toc_title(md):
    """Текст пункта оглавления из markdown-заголовка: снять inline-разметку, математику ($…$) оставить."""
    md = re.sub(r"\*\*(.+?)\*\*", r"\1", md)
    md = re.sub(r"(?<!\*)\*(?!\*)([^*\n]+?)\*(?!\*)", r"\1", md)
    md = re.sub(r"`([^`]+)`", r"\1", md)
    md = re.sub(r"\[([^\]]+)\]\([^)\s]+\)", r"\1", md)
    return md.strip()


# ───────────────────────── поток текста: блоки → HTML (модель данных doc-движка) ─────────────────────────
def render_stream(body, sid="s0"):
    """Пустая строка = граница блока. Возвращает (html, toc): toc — список (id, заголовок) по h2
    для бокового оглавления (§4). Порядок распознавания важен (флаги до заголовка,
    чтобы `## ⚑ …` тоже стал бейджем-долгом; типы-блоки — до абзаца)."""
    out, toc, h2n = [], [], 0
    for block in re.split(r"\n\s*\n", body.strip("\n")):
        lines = [ln.rstrip() for ln in block.split("\n") if ln.strip() != ""]
        if not lines:
            continue
        joined = _join(lines)
        first = lines[0].lstrip()

        # 1. цитата / поле  (все строки блока начинаются с '>')
        if all(l.lstrip().startswith(">") for l in lines):
            inner = _join([re.sub(r"^\s*>\s?", "", l) for l in lines])
            fm = re.match(r"^поле:(\S*)\s*(.*)$", inner, re.S)
            if fm:
                out.append(render_field(fm.group(1), fm.group(2)))
            else:
                out.append("<blockquote>%s</blockquote>" % render_inline(inner))
            continue

        # 2. иллюстрация-плейсхолдер
        if first.startswith("🖼"):
            out.append(render_ill(joined))
            continue

        # 2b. сырой HTML-блок автора верхнего уровня (доверенный источник) — без обёртки <p>
        if first.startswith(("<figure", "<svg", "<div", "<table", "<details")):
            out.append(joined)
            continue

        # 3. закрытый мат-долг (до открытого и до заголовка — распознаётся по фразе)
        if "Флаг закрыт" in joined:
            txt = re.sub(r"^#{1,4}\s*", "", joined)
            out.append('<p class="flag closed"><b>✔ закрыт.</b> %s</p>' % render_inline(txt))
            continue

        # 4. открытый мат-долг
        if "⚑" in joined:
            txt = re.sub(r"^#{1,4}\s*", "", joined)
            out.append('<p class="flag open">%s</p>' % render_inline(txt))
            continue

        # 5. заголовок (# … #### …); h2 → якорь + пункт бокового оглавления (§4); хвост блока — как абзац
        hm = re.match(r"^(#{1,4})\s+(.*)$", first)
        if hm:
            lvl = len(hm.group(1))
            if lvl == 2:
                h2n += 1
                hid = "%s-h-%d" % (sid, h2n)
                out.append('<h2 id="%s">%s</h2>' % (hid, render_inline(hm.group(2))))
                toc.append((hid, _toc_title(hm.group(2))))
            else:
                out.append("<h%d>%s</h%d>" % (lvl, render_inline(hm.group(2)), lvl))
            if len(lines) > 1:
                out.append("<p>%s</p>" % render_inline(_join(lines[1:])))
            continue

        # 6. список
        if all(l.lstrip().startswith("- ") for l in lines):
            items = "".join("<li>%s</li>" % render_inline(l.lstrip()[2:].strip()) for l in lines)
            out.append("<ul>%s</ul>" % items)
            continue

        # 6b. типизированный блок-утверждение (§3): распознаётся по зачину, между списком и абзацем
        tb = _typed_block(joined, sid)
        if tb:
            out.append(tb)
            continue

        # 7. абзац
        out.append("<p>%s</p>" % render_inline(joined))
    return "\n".join(out), toc


# ───────────────────────── drill-down-формат (ОПТ-ИН: frontmatter `format: drill-down`) ─────────────────────────
# Ступень-2 БРИФ-фазы mat-kostyak (заход kod_dvizhok-format): раздел `##` → <details open>,
# утверждение `###` с полем `род` → свёрнутый <details> с «тихим слоем» тегов (род — тонкая
# цветная метка слева на <summary>, вердикт нетривиально — амбер-точка; полный набор осей —
# приглушённой строкой внутри), доказательство/идея — отдельный вложенный свёрнутый кат.
# Документы БЕЗ флага идут старым render_stream и не меняются НИ БАЙТОМ: drill-стиль и
# скрипт фильтра едут внутри html самого drill-потока, шаблон PAGE не тронут.
# Сегменты без «рода» (понятия словаря) рендерятся старым конвейером без изменений.

_DRILL_AXES = ("род", "вердикт", "уровень", "вход")            # голые значения → строка осей
_DRILL_LINES = ("узел", "следует-из", "источник", "решение")   # тела с готовыми лейблами → своя строка
_DRILL_PROOF_RE = re.compile(r"^\*(Доказательство|Логика|Идея)")

# стиль тихого слоя: тонкие метки, не пилюли; цвета приглушены, замечаются только при поиске глазом
DRILL_CSS = """<style>
details.d-sec{margin:2.1em 0 .6em}
details.d-sec>summary{list-style:none;cursor:pointer}
details.d-sec>summary::-webkit-details-marker{display:none}
details.d-sec>summary::before{content:"▸";font-family:var(--sans);font-size:1rem;color:var(--muted);
  display:inline-block;width:1em;margin-left:-1em;vertical-align:.25em}
details.d-sec[open]>summary::before{content:"▾"}
details.d-sec>summary h2{display:inline;margin:0}
details.d-st{margin:.06em 0 .06em .2em}
details.d-st>summary{list-style:none;cursor:pointer;font-family:var(--sans);font-size:1.02rem;
  line-height:1.16;padding:.03em .55em .03em .8em;border-left:3px solid transparent;border-radius:0 3px 3px 0}
details.d-st>summary::-webkit-details-marker{display:none}
details.d-st>summary:hover{background:var(--accent-soft)}
details.d-st[open]{margin:.4em 0 .55em .2em}
details.d-st[data-rod="внутреннее"]>summary{border-left-color:#4d8a66}
details.d-st[data-rod="внешнее-пример"]>summary{border-left-color:#d4796b}
details.d-st[data-rod="упражнение"]>summary{border-left-color:#8a6fb3}
details.d-st[data-zona="называем-мостиком"]>summary{border-left:3px dashed #9a938a}
details.d-st[data-zona="условно"]>summary{border-left-color:#c9962e}
.d-num{color:var(--muted);font-weight:600;font-variant-numeric:tabular-nums}
.d-dot{display:inline-block;width:.42em;height:.42em;border-radius:50%;background:#c9962e;
  margin-left:.45em;vertical-align:.08em;opacity:.8}
.d-body{padding:.1em 0 .5em 1.5em}
.stream .d-quiet{font-family:var(--sans);font-size:.8rem;line-height:1.55;color:var(--muted);margin:.6em 0}
.stream .d-quiet p{margin:.12em 0}
details.d-proof{margin:.7em 0}
details.d-proof>summary{list-style:none;cursor:pointer;font-family:var(--sans);font-size:.85rem;
  font-style:italic;color:#8a8375}
details.d-proof>summary::-webkit-details-marker{display:none}
details.d-proof>summary::before{content:"▸ "}
details.d-proof[open]>summary::before{content:"▾ "}
details.d-proof>summary+.proof>.lbl,details.d-proof>summary+p>em:first-child{display:none}
.d-filter{display:flex;flex-wrap:wrap;gap:.4em;margin:1.5em 0 .2em;align-items:center;
  position:sticky;top:0;z-index:30;background:var(--bg);padding:.5em 0 .45em;
  box-shadow:0 5px 7px -7px rgba(33,31,27,.4)}
.d-filter button{font-family:var(--sans);font-size:.8rem;color:var(--muted);background:var(--panel);
  border:1px solid var(--rule);border-radius:12px;padding:.18em .8em;cursor:pointer}
.d-filter button:hover{color:var(--accent);border-color:var(--accent)}
.d-filter button.on{color:#fff;background:var(--accent);border-color:var(--accent)}
.d-count{font-family:var(--sans);font-size:.78rem;color:var(--muted);margin-left:auto;
  font-variant-numeric:tabular-nums}
.d-off{display:none}
.d-grp h3{margin:1.1em 0 .12em}
details.d-why{margin:.05em 0 .3em}
details.d-sec details.d-st,details.d-sec .d-grp h3,details.d-sec .stmt,
details.d-sec>summary h2{scroll-margin-top:64px}
.toc .d-toc2{list-style:none;margin:.05em 0 .2em;padding:0}
.toc .d-toc2 li{counter-increment:none;margin:.02em 0}
.toc .d-toc2 a{padding:.08em .3em .08em 1.9em;font-size:.78rem}
.toc .d-toc2 a::before{content:none}
.toc .d-toc2 a.d-cur{color:var(--accent);background:var(--accent-soft);font-weight:600}
</style>"""

# фильтр: чипы гасят непопадающие details.d-st по data-атрибутам (не парсингом текста).
# Р2/Р3 (заход kod_navigacija): счётчик «показано N из M», свернуть/развернуть всё,
# фильтр прячет опустевшие группы (.d-grp) и разделы (.d-sec) — «все» возвращает всё.
# Р4: второй уровень TOC (группы) строится через setTimeout(0) из DOMContentLoaded —
# ПОСЛЕ того как scrollspy шаблона PAGE соберёт свои ссылки: движковый TOC разделов
# моих ссылок не видит и не меняет поведения; подсветка групп — свой observer, класс d-cur.
# Р6: клик по внутреннему якорю раскрывает цепочку details над целью (иначе не доскроллит).
# Намеренно НИ ОДНОГО символа '<'/'>' (и стрелок '=>') — см. заход про check_view.
DRILL_JS = """<script>
(function () {
  "use strict";
  function all(root, sel) { return Array.prototype.slice.call(root.querySelectorAll(sel)); }
  all(document, ".d-filter").forEach(function (bar) {
    if (bar.getAttribute("data-init")) { return; }
    bar.setAttribute("data-init", "1");
    var root = bar.closest("section") || document;
    var items = all(root, "details.d-st");
    var chips = all(bar, "button[data-f]");
    var count = bar.querySelector(".d-count");
    function apply(f) {
      var everything = f === "все";
      items.forEach(function (it) {
        var show;
        if (everything) { show = true; }
        else if (f === "нетривиально") { show = it.getAttribute("data-verdikt") === "нетривиально"; }
        else { show = it.getAttribute("data-rod") === f; }
        it.classList.toggle("d-off", !show);
      });
      all(root, ".d-grp").forEach(function (g) {
        g.classList.toggle("d-off", !everything && !g.querySelector("details.d-st:not(.d-off)"));
      });
      all(root, "details.d-sec").forEach(function (s) {
        s.classList.toggle("d-off", !everything && !s.querySelector("details.d-st:not(.d-off)"));
      });
      if (count) {
        var n = 0;
        items.forEach(function (it) { if (!it.classList.contains("d-off")) { n += 1; } });
        count.textContent = "показано " + n + " из " + items.length;
      }
    }
    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        chips.forEach(function (c) { c.classList.remove("on"); });
        chip.classList.add("on");
        apply(chip.getAttribute("data-f"));
      });
    });
    all(bar, "button[data-a]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var op = btn.getAttribute("data-a") === "open";
        all(root, "details.d-st,details.d-sec").forEach(function (d) { d.open = op; });
      });
    });
    apply("все");
  });
  if (document.documentElement.getAttribute("data-d-nav")) { return; }
  document.documentElement.setAttribute("data-d-nav", "1");
  function reveal(id) {
    var el = id ? document.getElementById(id) : null;
    if (!el) { return null; }
    var p = el;
    while (p) {
      if (p.tagName === "DETAILS") { p.open = true; }
      p = p.parentElement;
    }
    return el;
  }
  document.addEventListener("click", function (ev) {
    var a = ev.target;
    while (a && !(a.tagName === "A" && a.getAttribute("href"))) { a = a.parentElement; }
    if (!a) { return; }
    var h = a.getAttribute("href");
    if (h.charAt(0) === "#") { reveal(h.slice(1)); }
  });
  window.addEventListener("DOMContentLoaded", function () {
    if (location.hash) {
      var el = reveal(location.hash.slice(1));
      if (el) { el.scrollIntoView(); }
    }
    window.setTimeout(function () {
      var spy = [], byId = {};
      all(document, ".toc a").forEach(function (a) {
        var h = a.getAttribute("href") || "";
        if (h.charAt(0) !== "#") { return; }
        var target = document.getElementById(h.slice(1));
        if (!target || target.tagName !== "H2") { return; }
        var sec = target.closest("details.d-sec");
        if (!sec) { return; }
        var heads = all(sec, ".d-grp h3[id]");
        if (!heads.length) { return; }
        var ol = document.createElement("ol");
        ol.className = "d-toc2";
        heads.forEach(function (h3) {
          var li = document.createElement("li");
          var link = document.createElement("a");
          link.setAttribute("href", "#" + h3.id);
          link.textContent = h3.getAttribute("data-toc") || h3.textContent;
          li.appendChild(link);
          ol.appendChild(li);
          spy.push({ id: h3.id, el: h3 });
          byId[h3.id] = link;
        });
        a.parentElement.appendChild(ol);
      });
      if (!spy.length || !window.IntersectionObserver) { return; }
      var visible = {}, cur = null;
      var obs = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { visible[e.target.id] = 1; } else { delete visible[e.target.id]; }
        });
        var cand = [];
        Object.keys(visible).forEach(function (id) {
          var el = document.getElementById(id);
          if (el) { cand.push({ id: id, top: el.getBoundingClientRect().top }); }
        });
        cand.sort(function (a, b) { return a.top - b.top; });
        var best = cand.length ? byId[cand[0].id] : null;
        if (best && best !== cur) {
          if (cur) { cur.classList.remove("d-cur"); }
          best.classList.add("d-cur");
          cur = best;
        }
      }, { rootMargin: "-4% 0px -70% 0px", threshold: 0 });
      spy.forEach(function (s) { obs.observe(s.el); });
    }, 0);
  });
})();
</script>"""

DRILL_FILTER = ('<div class="d-filter">'
                '<button data-f="все" class="on">все</button>'
                '<button data-f="внутреннее">внутреннее</button>'
                '<button data-f="внешнее-пример">внешнее</button>'
                '<button data-f="упражнение">упражнение</button>'
                '<button data-f="нетривиально">нетривиальные</button>'
                '<span class="d-count"></span>'
                '<button data-a="close">Свернуть всё</button>'
                '<button data-a="open">Развернуть всё</button>'
                '</div>')


def _drill_field(block):
    """Блок-цитата `> поле:<вид> …` → (вид, тело) либо None (не блок-поле)."""
    lines = [ln.rstrip() for ln in block.split("\n") if ln.strip() != ""]
    if not lines or not all(l.lstrip().startswith(">") for l in lines):
        return None
    inner = _join([re.sub(r"^\s*>\s?", "", l) for l in lines])
    fm = re.match(r"^поле:(\S*)\s*(.*)$", inner, re.S)
    if not fm:
        return None
    return fm.group(1).strip(), fm.group(2).strip()


def _drill_cut_stop(block):
    """Стоп-маркер границы ката (заход kod_dokat-pod-kat) — блок, который кат уже НЕ глотает:
    курсивный зачин-вставка `*` + заглавная (`*Зачем названо отдельно.*`, `*Следствие (Кантор).*`),
    флаг `⚑ …` / `Флаг закрыт: …`, блок-поле `> поле:…`. Заглавная — через isupper(), не
    кириллическим классом в regex; заголовки/конец потока сюда блоками не приходят."""
    s = block.lstrip()
    if s.startswith("*") and len(s) > 1 and s[1].isupper():
        return True
    if s.startswith("⚑") or s.startswith("Флаг закрыт:"):
        return True
    return _drill_field(block) is not None


def _drill_stmt(head_text, blocks, sid):
    """Группа `###` с полем `род` → свёрнутое утверждение drill-формата.
    Внутри раскрытого: формулировка → тихий блок осей/ссылок → кат доказательства → остальное.
    Отсутствующее поле (напр. `вердикт` у упражнения) — не ошибка: тег просто не печатается."""
    m = re.match(r"^(.*?)\.\s+(.*)$", head_text.strip(), re.S)
    num, name = (m.group(1), m.group(2)) if m else ("", head_text.strip())
    fields, proof_blocks, content_blocks = {}, [], []
    in_proof = False                          # кат открыт: глотать тело вывода до стоп-маркера
    for b in blocks:
        f = _drill_field(b)
        if f and (f[0] in _DRILL_AXES or f[0] in _DRILL_LINES):
            fields[f[0]] = f[1]
            in_proof = False                  # поле — стоп-маркер: кат закрыт, маркер в кат не входит
        elif _DRILL_PROOF_RE.match(b.lstrip()):
            proof_blocks.append(b)
            in_proof = True                   # зачин открывает кат
        elif in_proof and not _drill_cut_stop(b):
            proof_blocks.append(b)            # тело вывода: абзацы и $$-выкладки до стоп-маркера
        else:
            in_proof = False
            content_blocks.append(b)          # формулировка, следствие, чужие поля — стандартный рендер
    # summary: номер · имя + метки тихого слоя (род — цветной бордюр по data-rod, нетривиально — точка)
    dot = ('<span class="d-dot" title="нетривиально"></span>'
           if fields.get("вердикт") == "нетривиально" else "")
    label = ('<span class="d-num">%s</span> · %s' % (render_inline(num), render_inline(name))
             if num else render_inline(name))
    data = ""
    if num.startswith("Ex"):                  # Р6: у Ex-блока нет врезки с якорем — якорь на самом details
        data += ' id="%s-ex-%s"' % (sid, esc(num[2:].strip()))
    if "род" in fields:
        data += ' data-rod="%s"' % esc(fields["род"])
    if "вердикт" in fields:
        data += ' data-verdikt="%s"' % esc(fields["вердикт"])
    # тело: формулировка (первый контент-блок) стандартным конвейером
    first_html = render_stream(content_blocks[0], sid)[0] if content_blocks else ""
    rest_html = render_stream("\n\n".join(content_blocks[1:]), sid)[0] if len(content_blocks) > 1 else ""
    # тихий блок: полная строка осей + узел/следует-из/источник/решение своими строками
    quiet_ps = []
    axes = [(k, fields[k]) for k in _DRILL_AXES if k in fields]
    if axes:
        quiet_ps.append('<p class="d-axes">%s</p>'
                        % " · ".join("%s: %s" % (k, render_inline(v)) for k, v in axes))
    for k in _DRILL_LINES:
        if k in fields:
            quiet_ps.append("<p>%s</p>" % render_inline(fields[k]))
    quiet = '<div class="d-quiet">%s</div>' % "".join(quiet_ps) if quiet_ps else ""
    # кат доказательства: у упражнения (зачин *Идея…*) — «Идея»
    cut = ""
    if proof_blocks:
        pm = _DRILL_PROOF_RE.match(proof_blocks[0].lstrip())
        cut_label = "Идея" if pm.group(1) == "Идея" else "Доказательство"
        cut = ('<details class="d-proof"><summary>%s</summary>%s</details>'
               % (cut_label, render_stream("\n\n".join(proof_blocks), sid)[0]))
    return ('<details class="d-st"%s><summary>%s%s</summary>'
            '<div class="d-body">%s%s%s%s</div></details>'
            % (data, label, dot, first_html, quiet, cut, rest_html))


_DRILL_PON_QUIET = ("зона", "зависимости", "узел")               # тихая строка П-блока (Р1)
_DRILL_PON_CUTS = (("оправдание", "Оправдание"), ("не-говорим", "Не говорим"))
_DRILL_LBL_RE = re.compile(r"^\*\*[^*]*\*\*\s*")                 # жирный лейбл в начале тела поля


def _drill_pon(head_text, blocks, sid):
    """Группа `###` с полем `зона` (понятие словаря) → свёрнутый d-st (Р1 kod_navigacija).
    Внутри раскрытого: врезка-определение существующим конвейером (несёт якорь s-d-N) →
    тихая строка зона · зависимости · узел → «Оправдание» и «Не говорим» свёрнутыми
    мини-катами (лейбл из тела снят — его дублирует summary ката) → прочие блоки хвостом.
    Тихая метка summary — по data-zona: определяем — ничего, называем-мостиком — серый
    пунктир, условно — амбер (CSS)."""
    m = re.match(r"^(.*?)\.\s+(.*)$", head_text.strip(), re.S)
    num, name = (m.group(1), m.group(2)) if m else ("", head_text.strip())
    known = set(_DRILL_PON_QUIET) | set(k for k, _ in _DRILL_PON_CUTS)
    fields, content_blocks = {}, []
    for b in blocks:
        f = _drill_field(b)
        if f and f[0] in known:
            fields[f[0]] = f[1]
        else:
            content_blocks.append(b)
    zona = _DRILL_LBL_RE.sub("", fields.get("зона", "")).strip()
    label = ('<span class="d-num">%s</span> · %s' % (render_inline(num), render_inline(name))
             if num else render_inline(name))
    data = ' data-zona="%s"' % esc(zona) if zona else ""
    first_html = render_stream(content_blocks[0], sid)[0] if content_blocks else ""
    rest_html = render_stream("\n\n".join(content_blocks[1:]), sid)[0] if len(content_blocks) > 1 else ""
    quiet_ps = [render_inline(fields[k]) for k in _DRILL_PON_QUIET if k in fields]
    quiet = ('<div class="d-quiet"><p class="d-axes">%s</p></div>' % " · ".join(quiet_ps)
             if quiet_ps else "")
    cuts = ""
    for key, cap in _DRILL_PON_CUTS:
        if key in fields:
            body = _DRILL_LBL_RE.sub("", fields[key]).strip()
            cuts += ('<details class="d-proof"><summary>%s</summary><p>%s</p></details>'
                     % (cap, render_inline(body)))
    return ('<details class="d-st"%s><summary>%s</summary>'
            '<div class="d-body">%s%s%s%s</div></details>'
            % (data, label, first_html, quiet, cuts, rest_html))


def _drill_grp(head_text, blocks, sid, gid):
    """Заголовок группы (`###` без род/зона) → ОТКРЫВАЮЩАЯ обёртка `<div class="d-grp">`
    (Р3/Р4/Р5): h3 с якорем и data-toc (чистый текст — второй уровень TOC строит JS,
    не завися от KaTeX), преамбула «Зачем эта группа…» и прочие абзацы — свёрнутым
    мини-катом «зачем группа». Div закрывает вызывающий цикл: внутрь попадают d-st
    группы — фильтр прячет опустевшую группу целиком одним классом."""
    why = ""
    if blocks:
        why = ('<details class="d-proof d-why"><summary>зачем группа</summary>%s</details>'
               % render_stream("\n\n".join(blocks), sid)[0])
    return ('<div class="d-grp"><h3 id="%s" data-toc="%s">%s</h3>%s'
            % (gid, esc(_toc_title(head_text)), render_inline(head_text), why))


def _drill_anchor_scan(body, sid):
    """Множество живых якорей потока для Р6 — по сырому источнику, ДО рендера тел
    (упоминание может стоять раньше цели). Зеркалит якоря _typed_block (d-N/t-N)
    и Ex-якоря _drill_stmt; несуществующий номер в множество не попадает — не линкуется."""
    anchors = {"d": {}, "t": {}, "ex": {}}
    for n in re.findall(r"(?m)^\*\*Определение\s+(\d+)", body):
        anchors["d"][n] = "%s-d-%s" % (sid, n)
    for n in re.findall(r"(?m)^\*\*(?:Теорема|Лемма|Предложение|Утверждение)\s+(\d+)", body):
        anchors["t"][n] = "%s-t-%s" % (sid, n)
    for n in re.findall(r"(?m)^###\s+Ex\s+(\S+?)\.\s", body):
        anchors["ex"][n] = "%s-ex-%s" % (sid, n)
    return anchors


# Р6: что защищаем от линковки — summary (в т.ч. h2 секций), код-спаны, лейблы врезок
# (лейбл — место определения, не упоминание: самоссылку не рисуем), формулы $…$/$$…$$.
_DRILL_LINK_STASH = re.compile(
    r"<summary\b.*?</summary>|<code\b.*?</code>|<span class=\"lbl\">.*?</span>"
    r"|\$\$.+?\$\$|\$[^$\n]+?\$", re.S)
# упоминания: падежные формы по букве захода (только литеральные альтернации, без
# кириллических классов-диапазонов); последовательность чисел — «8 и 9», «14, 15», «36–40»
_DRILL_NUMSEQ = r"\d+(?:\s*[–—-]\s*\d+)?(?:(?:,\s*|\s+и\s+)\d+(?:\s*[–—-]\s*\d+)?)*"
_DRILL_LINK_WORD = re.compile(
    "(?:У|у)тверждени(?:ям|ем|е|ю|я|и)\\s+" + _DRILL_NUMSEQ
    + "|(?:О|о)пределени(?:ям|ем|е|ю|я|и)\\s+" + _DRILL_NUMSEQ
    + r"|Ex\s+\d+(?:\.\d+)*\.[ivxlcdm]+")


def _drill_linkify(html, anchors):
    """Р6: текстовые упоминания «утверждение 47» / «определения 36–40» / «Ex 1.4.ii»
    → якорные ссылки на живые блоки. Каждое число последовательности линкуется отдельно
    (у диапазона это первое и последнее — середина текстом); номер без якоря остаётся
    текстом. Ссылка — только вокруг числа: тег снимается check_view без потери текста."""
    if not (anchors["d"] or anchors["t"] or anchors["ex"]):
        return html
    stash = []

    def keep(m):
        stash.append(m.group(0))
        return "\x00L%d\x00" % (len(stash) - 1)

    html = _DRILL_LINK_STASH.sub(keep, html)

    def link_mention(m):
        s = m.group(0)
        if s.startswith("Ex"):
            key = re.sub(r"^Ex\s+", "", s)
            aid = anchors["ex"].get(key)
            return '<a href="#%s">%s</a>' % (aid, s) if aid else s
        kind = "t" if s.startswith(("У", "у")) else "d"

        def one(nm):
            aid = anchors[kind].get(nm.group(0))
            return '<a href="#%s">%s</a>' % (aid, nm.group(0)) if aid else nm.group(0)

        return re.sub(r"\d+", one, s)

    html = _DRILL_LINK_WORD.sub(link_mention, html)
    return re.sub(r"\x00L(\d+)\x00", lambda m: stash[int(m.group(1))], html)


def render_stream_drill(body, sid="s0"):
    """Поток в drill-down-формате. Контракт как у render_stream: (html, toc).
    `##` → <details> уровня-1 (summary = стандартный h2: якорь, toc, счётчик; open —
    по Р7: до последней секции с drill-блоками включительно, служебный хвост closed);
    группы `###` с полем `род` → _drill_stmt, с полем `зона` → _drill_pon (Р1),
    прочие `###` — заголовки групп в обёртке .d-grp (Р3–Р5); сегменты без `###`
    (преамбулы секций) — нетронутый render_stream. Тела — сквозь _drill_linkify (Р6),
    кроме секции «Приложение…» (там команды — исключение названо заходом)."""
    prefix, sections, cur_sec, cur_grp = [], [], None, None
    for block in re.split(r"\n\s*\n", body.strip("\n")):
        if not block.strip():
            continue
        first = block.split("\n", 1)[0].lstrip()
        hm = re.match(r"^(#{2,3})\s+(.*)$", first)
        if hm and len(hm.group(1)) == 2:
            cur_sec = {"head": hm.group(2).strip(), "pre": [], "groups": []}
            cur_grp = None
            sections.append(cur_sec)
            tail = block.split("\n", 1)[1] if "\n" in block else ""
            if tail.strip():
                cur_sec["pre"].append(tail)
            continue
        if hm and len(hm.group(1)) == 3:
            cur_grp = {"head": hm.group(2).strip(), "blocks": []}
            if cur_sec is None:
                cur_sec = {"head": None, "pre": [], "groups": []}
                sections.append(cur_sec)
            cur_sec["groups"].append(cur_grp)
            tail = block.split("\n", 1)[1] if "\n" in block else ""
            if tail.strip():
                cur_grp["blocks"].append(tail)
            continue
        if cur_grp is not None:
            cur_grp["blocks"].append(block)
        elif cur_sec is not None:
            cur_sec["pre"].append(block)
        else:
            prefix.append(block)
    def grp_kind(g):
        for b in g["blocks"]:
            f = _drill_field(b)
            if f and f[0] == "род":
                return "stmt"
            if f and f[0] == "зона":
                return "pon"
        return "hdr"

    kinds = [[grp_kind(g) for g in s["groups"]] for s in sections]
    has_stmt = any(k == "stmt" for ks in kinds for k in ks)
    # Р7 (без хардкода имён): открыты секции до ПОСЛЕДНЕЙ несущей drill-блоки (род/зона)
    # включительно; служебный хвост (C, D, E, История, Приложение) — closed. Нет ни одной
    # содержательной — все открыты (прежнее поведение).
    content_idx = [i for i, s in enumerate(sections)
                   if s["head"] is not None and any(k != "hdr" for k in kinds[i])]
    last_content = max(content_idx) if content_idx else len(sections) - 1
    anchors = _drill_anchor_scan(body, sid)
    toc, h2n, gn, out = [], 0, 0, [DRILL_CSS]
    if prefix:
        out.append(_drill_linkify(render_stream("\n\n".join(prefix), sid)[0], anchors))
    if has_stmt:
        out.append(DRILL_FILTER)
    for si, s in enumerate(sections):
        parts, grp_open = [], False
        if s["pre"]:
            parts.append(render_stream("\n\n".join(s["pre"]), sid)[0])
        for g, kind in zip(s["groups"], kinds[si]):
            if kind == "stmt":
                parts.append(_drill_stmt(g["head"], g["blocks"], sid))
            elif kind == "pon":                # понятие словаря — свёрнутый d-st (Р1)
                parts.append(_drill_pon(g["head"], g["blocks"], sid))
            else:                              # заголовок группы — обёртка до следующей группы
                if grp_open:
                    parts.append("</div>")
                gn += 1
                parts.append(_drill_grp(g["head"], g["blocks"], sid, "%s-g-%d" % (sid, gn)))
                grp_open = True
        if grp_open:
            parts.append("</div>")
        chunk = "\n".join(parts)
        if s["head"] is None:
            out.append(_drill_linkify(chunk, anchors))
            continue
        h2n += 1
        hid = "%s-h-%d" % (sid, h2n)
        toc.append((hid, _toc_title(s["head"])))
        sec_html = ('<details class="d-sec"%s><summary><h2 id="%s">%s</h2></summary>\n%s</details>'
                    % (" open" if si <= last_content else "", hid, render_inline(s["head"]), chunk))
        if not s["head"].lstrip().startswith("Приложение"):
            sec_html = _drill_linkify(sec_html, anchors)
        out.append(sec_html)
    out.append(DRILL_JS)
    return "\n".join(out), toc


# ───────────────────────── загрузка потоков (каждый *.md = вкладка) ─────────────────────────
def load_streams(src):
    streams = []
    for p in sorted(src.glob("*.md")):
        meta, body = split_frontmatter(read_text(p))
        opened = body.count("⚑")
        closed = len(re.findall(r"Флаг закрыт", body))
        streams.append({
            "name": p.name,
            "meta": meta,
            "body": body,
            "label": meta.get("tab") or first_heading(body) or p.stem,
            "debt_open": max(0, opened - closed),
            "debt_raw": (opened, closed),
        })
    streams.sort(key=lambda s: (int(s["meta"].get("poryadok", "999") or "999"), s["name"]))
    # рендер ПОСЛЕ сортировки: индекс потока → префикс якорей (уникальность id между вкладками)
    for i, st in enumerate(streams):
        render = (render_stream_drill if st["meta"].get("format") == "drill-down"
                  else render_stream)                      # ОПТ-ИН drill-down; без флага — как раньше
        st["html"], st["toc"] = render(st["body"], "s%d" % i)
    return streams


# ───────────────────────── линтер-гейт (структурный, стиль build_deck §9) ─────────────────────────
# внешний asset-URL в ТЕЛЕ автора (src/href на http(s):// или //…); <a href> — разрешён.
# KaTeX-CDN в <head> инжектим мы сами и НЕ сканируем (доверенный авторский рантайм-вид).
_EXT_RE = re.compile(r'<(?!a[\s>])[a-zA-Z][\w:-]*\b[^>]*?\b(?:src|href)\s*=\s*"(?:https?:)?//[^"]*"', re.S)


def lint(streams):
    errors, warns = [], []
    if not streams:
        errors.append("нет ни одного *.md источника в папке")
        return errors, warns
    for st in streams:
        status = st["meta"].get("status", "")
        net = st["debt_open"]
        # мат-долг: открытый ⚑ при финальном статусе — жёсткая ошибка; иначе — warn
        if net > 0:
            if status == "polno":
                errors.append('%s: %d открытый мат-долг ⚑ при status: polno — '
                              'закрой строкой «Флаг закрыт …» или понизь статус'
                              % (st["name"], net))
            else:
                warns.append('%s: %d открытый мат-долг ⚑ (status: %s — допустимо на этой стадии)'
                             % (st["name"], net, status or "—"))
        # ярлык вкладки обязателен
        if not st["label"].strip():
            errors.append('%s: пустой ярлык вкладки (задай frontmatter tab: или заголовок #)' % st["name"])
        # статус — из известной лестницы (иначе, вероятно, опечатка)
        if status and status not in KNOWN_STATUS:
            warns.append('%s: неизвестный status: %s (лестница: %s)'
                         % (st["name"], status, " → ".join(["skelet", "chernovik", "…", "polno"])))
        # внешний asset-URL в теле автора
        for m in _EXT_RE.finditer(st["html"]):
            errors.append('%s: внешний asset-URL в теле: %s…' % (st["name"], m.group(0)[:60]))
    return errors, warns


# ───────────────────────── шаблон вида (template + подстановка, стиль семьи) ─────────────────────────
PAGE = r"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}}</title>
<!-- ⚠ KaTeX через CDN — АВТОРСКИЙ РАНТАЙМ-ВИД (Р7), единственная внешняя зависимость.
     Только для вычитки; финальный дек несёт статический кэш формул, не рантайм. -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css" crossorigin="anonymous">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" crossorigin="anonymous"></script>
<script>
  // оба katex-скрипта — defer, поэтому выполнены ДО DOMContentLoaded; guard — на офлайн.
  window.addEventListener("DOMContentLoaded", function () {
    if (window.renderMathInElement) renderMathInElement(document.body, {
      delimiters: [{left: "$$", right: "$$", display: true},
                   {left: "$", right: "$", display: false}],
      throwOnError: false
    });
  });
</script>
<style>
:root{
  /* §5 STANDART-oformlenia: каталанская база (решение владельца 2026-07-16), дословно */
  --bg:#fbfaf6; --panel:#fffdf8; --text:#211f1b; --muted:#726c60;
  --rule:#e7e2d6; --accent:#2f6e8e; --accent-soft:#e8f0f4; --warm:#c9743a; --warm-soft:#f6ece2;
  --shade:#dfeaf0; --insight-bg:#e8f0f4; --thread:#284862;
  --defn:#3a6b4f; --flag-open:#a11414; --flag-open-bg:#fbe9e9; --flag-closed:#2c7a2c;
  --flag-closed-bg:#e9f5e9; --link:#2f6e8e;
  /* §5 шрифты: Source Serif 4 / Source Sans 3 БЕЗ подключения из сети (самодостаточность,
     DVIZHKI §1) — только font-family с фолбэками; нет шрифта в системе → Georgia/system-ui */
  --serif:"Source Serif 4",Georgia,"Times New Roman",serif;
  --sans:"Source Sans 3",system-ui,-apple-system,"Helvetica Neue",Arial,sans-serif;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--serif);
  line-height:1.7;font-size:21px;font-optical-sizing:auto}
a{color:var(--link)}
.wrap{max-width:1335px;margin:0 auto;padding:1.6rem 30px 130px}
.doc-head,.runtime-note{max-width:1015px}
.doc-head{font-family:var(--sans)}
.doc-head h1{font-family:var(--serif);font-size:1.7rem;margin:.2em 0 .1em}
.gen-note{font-family:var(--sans);font-size:.8rem;color:var(--muted);margin:0 0 1.4rem}
.runtime-note{font-family:var(--sans);font-size:.82rem;line-height:1.5;background:#fff8e6;
  border:1px solid #e6d7a2;border-radius:6px;padding:.7rem .9rem;margin:0 0 1.6rem;color:#6a5a1e}
.runtime-note code{background:#f0e6c8;padding:0 .25em;border-radius:3px}

/* ── §4 макет трёх зон: [оглавление 210px][текст ≤820][жёлоб .mn ~195] (порт catalan/kurs) ── */
.layout{display:grid;grid-template-columns:210px minmax(0,1015px);gap:46px}
.layout.solo{grid-template-columns:minmax(0,1015px)}
main{min-width:0}

/* ── §4 боковое оглавление (sticky, авто-нумерация, подсветка активного пункта при скролле) ── */
.toc{position:sticky;top:16px;align-self:start;max-height:calc(100vh - 40px);overflow:auto;
  font-family:var(--sans);font-size:.83rem;line-height:1.4;border-right:1px solid var(--rule);padding-right:14px}
.toc>summary{list-style:none;cursor:default;font-weight:600;font-size:.74rem;letter-spacing:.09em;
  text-transform:uppercase;color:var(--muted);margin:0 0 .8em;padding-bottom:.5em;border-bottom:1px solid var(--rule)}
.toc>summary::-webkit-details-marker{display:none}
.toc ol{list-style:none;margin:0;padding:0;counter-reset:toc}
.toc li{counter-increment:toc;margin:.16em 0}
.toc a{display:block;color:var(--muted);text-decoration:none;border:0;padding:.18em .3em .18em 1.7em;
  border-radius:3px;position:relative}
.toc a::before{content:counter(toc);position:absolute;left:.2em;color:#b7ae9c;font-variant-numeric:tabular-nums}
.toc a:hover{color:var(--accent);background:var(--accent-soft)}
.toc a.active{color:var(--accent);background:var(--accent-soft);font-weight:600}
.toc a.active::before{color:var(--accent)}

/* ── вкладки: CSS-only, скрытые radio + label (без сети/JS) ── */
.tabs>input.tab-radio{position:absolute;width:1px;height:1px;opacity:0;pointer-events:none}
.tabbar{display:flex;flex-wrap:wrap;gap:.25rem;border-bottom:2px solid var(--rule);margin:0 0 1.6rem}
.tabbar label{cursor:pointer;user-select:none;font-family:var(--sans);font-weight:600;
  font-size:.95rem;color:var(--muted);padding:.5rem 1.1rem;border:2px solid transparent;
  border-bottom:none;border-radius:9px 9px 0 0;margin-bottom:-2px;transition:color .12s}
.tabbar label:hover{color:var(--text)}
.panel{display:none}
{{TABCSS}}

/* ── §4 поток текста: article ≤820, номера разделов авто-counter акцентом (§5, руками не писать) ── */
.stream{max-width:820px;counter-reset:sec}
.stream h1{font-size:1.9rem;line-height:1.15;font-weight:600;letter-spacing:-.01em;margin:.1em 0 .45em}
.stream h2{font-family:var(--sans);font-size:1.6rem;font-weight:600;letter-spacing:-.01em;line-height:1.2;
  margin:2.3em 0 .55em;counter-increment:sec;scroll-margin-top:16px}
.stream h2::before{content:counter(sec)". ";color:var(--accent);font-weight:600}
.stream h3{font-family:var(--sans);font-size:1.18rem;font-weight:600;margin:1.6em 0 .5rem}
.stream p{margin:0 0 1.05em}
.stream ul{margin:.7em 0;padding-left:1.3em}
.stream li{margin:.3em 0}
.stream a{border-bottom:1px solid #bcd2dd}
.stream a:hover{border-bottom-color:var(--accent)}

/* ── §3 блоки-утверждения: цвет кодирует СТАТУС (синий=опред., тёплый=утвержд., приглуш.=док-во) ── */
.stmt{margin:1.5em 0;padding:.55em 0 .55em 1.15em;border-left:3px solid var(--rule);scroll-margin-top:16px}
.stmt .lbl{font-family:var(--sans);font-weight:600;font-size:.98rem;letter-spacing:.01em}
.defn{border-left-color:var(--accent);background:linear-gradient(90deg,var(--accent-soft),transparent 78%)}
.defn .lbl{color:var(--accent)}
.thm{border-left-color:var(--warm);background:linear-gradient(90deg,var(--warm-soft),transparent 78%)}
.thm .lbl{color:var(--warm)}
.proof{color:var(--muted);font-size:.99rem;border-left:2px dotted #cfc7b6;padding-left:1.05em;margin:1em 0}
.proof .lbl{font-style:italic;font-weight:600;color:#8a8375}
.example{background:#f4f1ea;border-radius:5px;padding:.8em 1.1em;margin:1.5em 0;font-size:1rem}
.example .lbl{font-family:var(--sans);font-weight:600;font-size:.9rem;letter-spacing:.02em;color:var(--muted);
  display:block;margin-bottom:.25em;text-transform:uppercase}
/* Замечание — div.note, чтобы НЕ конфликтовать с движковым aside.note (дженерик > поле:) */
div.note{background:#f4f1ea;border-left:3px solid var(--rule);border-radius:0 5px 5px 0;
  padding:.7em 1.05em;margin:1.5em 0;font-size:1rem}
div.note .lbl{font-family:var(--sans);font-weight:600;font-size:.82rem;letter-spacing:.03em;color:var(--muted);
  display:block;margin-bottom:.25em;text-transform:uppercase}
/* чёрный ящик — рамка-пунктир («за это не платили»); техфакт — нейтральная плашка; рассказ — не математика */
.blackbox{border:1.5px dashed var(--muted);border-radius:5px;padding:.7em 1.05em;margin:1.5em 0;
  font-size:.97rem;color:var(--muted);background:#faf8f3}
.blackbox .lbl{font-family:var(--sans);font-weight:600;font-size:.8rem;letter-spacing:.04em;text-transform:uppercase;
  color:var(--text);display:block;margin-bottom:.3em}
.tech{background:#f4f1ea;border-left:3px solid var(--muted);border-radius:0 4px 4px 0;
  padding:.65em 1.05em;margin:1.4em 0;font-size:.97rem}
.tech .lbl{font-family:var(--sans);font-weight:600;font-size:.78rem;letter-spacing:.05em;text-transform:uppercase;
  color:var(--muted);display:block;margin-bottom:.25em}
.rasskaz{font-style:italic;color:var(--muted);margin:1.5em 0;padding-left:1em;border-left:2px solid var(--warm-soft)}
.rasskaz .lbl{font-family:var(--sans);font-style:normal;font-weight:600;font-size:.82rem;letter-spacing:.02em;
  color:var(--warm);display:block;margin-bottom:.2em}

/* KaTeX (порт catalan/kurs) */
.katex-display{margin:1.15em 0;overflow-x:auto;overflow-y:hidden;padding:.2em 0}
.katex{font-size:1.05em}
blockquote{margin:1em 0;padding:.3em 0 .3em 1em;border-left:3px solid var(--rule);color:var(--muted)}
code{font-family:"SF Mono",Consolas,monospace;font-size:.9em;background:#efe9dd;padding:0 .25em;border-radius:3px}

/* ── таблица (напр. трёхколоночное соответствие): бордюр по --rule, шапка --shade ── */
table{border-collapse:collapse;margin:1.6em 0;width:100%;max-width:820px;font-size:.98rem}
table th,table td{border:1px solid var(--rule);padding:.45em .8em;text-align:left;vertical-align:top}
table thead th{font-family:var(--sans);background:var(--shade);font-weight:600;color:var(--text)}
table tbody tr:nth-child(even){background:var(--panel)}
table tbody td:first-child{color:var(--muted)}

/* ── поле .mn: float в правый жёлоб (CSS дословно из distillat-tehnika §2) ── */
.mn{float:right;clear:right;width:172px;margin:.35em -195px 1.1em 22px;
  font-family:var(--sans);font-size:.8rem;line-height:1.5;color:var(--muted);
  border-left:2px solid var(--rule);padding-left:.75em}
.mn b,.mn strong{color:var(--text)}
/* ── §10 адаптив (порт catalan/kurs): ≤900 одна колонка, оглавление наверх; ≤520 кегль 19 ── */
@media(max-width:900px){
  .layout{grid-template-columns:1fr;gap:0}
  .stream{max-width:none}
  .toc{position:static;max-height:none;border-right:0;border-bottom:1px solid var(--rule);
    padding:0 0 1em;margin-bottom:1.5em}
  .toc>summary{cursor:pointer}
  .toc ol{columns:2;column-gap:22px}
  .mn{float:none;width:auto;margin:1.2em 0;border-left:3px solid var(--rule);padding:.4em 0 .4em .9em}
}
@media(max-width:520px){
  body{font-size:19px}
  .toc ol{columns:1}
  .katex{font-size:1em}
}

/* ── поле-aside (generic > поле:) ── */
aside.note{font-family:var(--sans);font-size:.9rem;background:var(--panel);
  border:1px solid var(--rule);border-left:3px solid var(--muted);
  padding:.6rem .9rem;margin:1rem 0;border-radius:0 4px 4px 0;color:var(--muted)}
aside.note.thread{border-left-color:var(--thread)}

/* ── .insight: крупное прозрение/разворот ── */
.insight{background:var(--insight-bg);border-left:4px solid var(--accent);
  padding:1rem 1.25rem;margin:1.5rem 0;border-radius:0 6px 6px 0}
.insight .tag{display:inline-block;font-family:var(--sans);font-size:.7rem;font-weight:700;
  letter-spacing:.07em;text-transform:uppercase;color:var(--accent);margin-right:.5em}

/* ── .foot: статус черновика ── */
.foot{margin-top:2.5rem;padding-top:1rem;border-top:1px solid var(--rule);
  font-family:var(--sans);font-size:.85rem;color:var(--muted)}

/* ── cue-визуал ── */
.cue{font-family:var(--sans);font-size:.85rem;background:#eef3f0;
  border:1px dashed var(--defn);padding:.5rem .85rem;margin:1rem 0;color:var(--defn)}

/* ── уровень-пилюля ── */
.level-line{font-family:var(--sans);font-size:.85rem;color:var(--muted);margin:.4rem 0}
.level{display:inline-block;font-weight:600;font-size:.72rem;padding:.12rem .55rem;
  border-radius:11px;background:#e7e0d2;color:var(--text)}

/* ── мат-долг: бейджи ── */
.flag{font-family:var(--sans);font-size:.85rem;font-weight:600;padding:.55rem .85rem;
  margin:1rem 0;border-radius:4px}
.flag.open{background:var(--flag-open-bg);border-left:4px solid var(--flag-open);color:var(--flag-open)}
.flag.open::before{content:"⚑ мат-долг открыт — ";font-weight:700}
.flag.closed{background:var(--flag-closed-bg);border-left:4px solid var(--flag-closed);color:var(--flag-closed)}

/* ── иллюстрация-плейсхолдер ── */
.ill-ph{border:2px dashed var(--rule);background:repeating-linear-gradient(45deg,
  transparent,transparent 9px,rgba(0,0,0,.02) 9px,rgba(0,0,0,.02) 18px);
  padding:1.3rem;margin:1.5rem 0;text-align:center;border-radius:8px}
.ill-ph .ill-badge{font-family:var(--sans);font-weight:700;letter-spacing:.04em;color:var(--muted)}
.ill-ph figcaption{font-family:var(--sans);font-size:.88rem;color:var(--muted);margin-top:.5rem}

/* ── иллюстрация (готовый SVG автора) ── */
figure{margin:2.1em 0;text-align:center}
figure svg{max-width:100%;height:auto;display:block;margin:0 auto}
figure figcaption{font-family:var(--sans);font-size:.88rem;color:var(--muted);margin-top:.5rem}

/* ── SVG-палитра (портировано дословно из catalan/kurs/kurs-lekcii.html) ── */
.s-line{fill:none;stroke:var(--text);stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.s-thin{fill:none;stroke:var(--muted);stroke-width:1.2}
.s-dash{fill:none;stroke:var(--accent);stroke-width:1.3;stroke-dasharray:4 4}
.s-accent{fill:none;stroke:var(--accent);stroke-width:2.4;stroke-linejoin:round;stroke-linecap:round}
.s-fillw{fill:var(--warm)}
.s-fillsh{fill:var(--shade)}
.s-node{fill:#fff;stroke:var(--text);stroke-width:1.8}
.s-node-r{fill:var(--text)}
/* .s-node-a — акцентный узел. Словарь примитивов (09-illustracii, строка «узел») обещал его
   с самого начала, а движок не реализовывал: <circle> без fill падает в чёрный ТИХО, без
   ошибки — та же ловушка, что undefined var(--x). Заведён 2026-07-16 (арка krivaya-drakona:
   нужна была пара «акцентная засечка на полоске ↔ акцентная вершина ломаной»). */
.s-node-a{fill:var(--accent);stroke:var(--accent)}
.s-txt{font-family:var(--sans);font-size:13px;fill:var(--text)}
.s-txt-w{font-family:var(--sans);font-size:13px;fill:#fff;font-weight:600}
.s-txt-m{font-family:var(--sans);font-size:12px;fill:var(--muted)}
.s-ar-a{fill:var(--accent)} .s-ar-m{fill:var(--muted)}

/* ── мета-строка потока ── */
.stream-meta{font-family:var(--sans);font-size:.8rem;color:var(--muted);
  margin:0 0 1.2rem;display:flex;flex-wrap:wrap;gap:.5rem 1rem}
.stream-meta .status{font-weight:700;color:var(--text)}
.stream-meta .debt{color:var(--flag-open);font-weight:700}
</style>
</head>
<body>
<div class="wrap">
<div class="doc-head">
  <h1>{{TITLE}}</h1>
  <p class="gen-note">Вид doc-движка · вкладки = потоки-«котёл» (стадия склада сюжетов). Источник истины — markdown; правь его и пересобирай (0 токенов).</p>
</div>
<div class="runtime-note">Математика набрана <b>KaTeX через CDN</b> — это <b>авторский рантайм-вид для вычитки</b> (Р7), единственная внешняя зависимость. Офлайн формулы деградируют в сырой <code>$…$</code>, страница не падает. Финальный дек несёт статический кэш формул, не рантайм.</div>
<div class="tabs">
{{RADIOS}}
<nav class="tabbar">
{{LABELS}}
</nav>
{{PANELS}}
</div>
</div>
<script>
/* §4б: подсветка активного пункта оглавления при скролле. Один IntersectionObserver на все h2[id]
   с toc-ссылкой; скрытые вкладки (display:none) не пересекаются → скоуп сам сходится к активной. */
window.addEventListener("DOMContentLoaded", function () {
  if (!("IntersectionObserver" in window)) return;
  var links = {};
  Array.prototype.forEach.call(document.querySelectorAll('.toc a[href^="#"]'), function (a) {
    links[a.getAttribute("href").slice(1)] = a;
  });
  var current = null, visible = {};
  function setActive(a) {
    if (current) current.classList.remove("active");
    if (a) { a.classList.add("active"); current = a; }
  }
  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) visible[e.target.id] = 1; else delete visible[e.target.id];
    });
    var best = null, bestTop = Infinity;
    Object.keys(visible).forEach(function (id) {
      var el = document.getElementById(id); if (!el) return;
      var top = el.getBoundingClientRect().top;
      if (top < bestTop) { bestTop = top; best = id; }
    });
    if (best && links[best]) setActive(links[best]);
  }, { rootMargin: "-15% 0px -75% 0px", threshold: 0 });
  Object.keys(links).forEach(function (id) {
    var el = document.getElementById(id); if (el) obs.observe(el);
  });
});
</script>
</body>
</html>
"""


def build_html(streams, title):
    radios, labels, panels, tabcss = [], [], [], []
    for i, st in enumerate(streams):
        checked = " checked" if i == 0 else ""
        radios.append('<input class="tab-radio" type="radio" name="doc-tab" id="tab-%d"%s>' % (i, checked))
        labels.append('<label class="tab-label" for="tab-%d">%s</label>' % (i, esc(st["label"])))
        tabcss.append('#tab-%d:checked ~ #panel-%d{display:block}' % (i, i))
        tabcss.append('#tab-%d:checked ~ .tabbar label[for="tab-%d"]{color:var(--accent);'
                      'background:var(--panel);border-color:var(--rule) var(--rule) var(--panel)}' % (i, i))
        panels.append(_panel_html(i, st))
    page = PAGE
    page = page.replace("{{TITLE}}", esc(title))
    page = page.replace("{{TABCSS}}", "\n".join(tabcss))
    page = page.replace("{{RADIOS}}", "\n".join(radios))
    page = page.replace("{{LABELS}}", "\n".join(labels))
    page = page.replace("{{PANELS}}", "\n".join(panels))
    # баннер «сгенерировано» сразу после доктайпа (комментарий рендер не меняет)
    nl = page.find("\n") + 1
    return page[:nl] + GEN_BANNER + page[nl:]


def _toc_html(toc):
    """Боковое оглавление из h2 (§4): sticky-список с якорями; пусто → нет оглавления."""
    if not toc:
        return ""
    items = "".join('<li><a href="#%s">%s</a></li>' % (tid, title) for tid, title in toc)
    return ('<details class="toc" open><summary>Содержание</summary>'
            '<ol>%s</ol></details>' % items)


def _panel_html(i, st):
    meta = st["meta"]
    bits = []
    if meta.get("status"):
        bits.append('<span class="status">status: %s</span>' % esc(meta["status"]))
    if meta.get("registr"):
        bits.append('регистр: %s' % esc(meta["registr"]))
    if st["debt_open"] > 0:
        bits.append('<span class="debt">⚑ открытых долгов: %d</span>' % st["debt_open"])
    bits.append('источник: %s' % esc(st["name"]))
    meta_line = '<div class="stream-meta">%s</div>' % " ".join('<span>%s</span>' % b for b in bits)
    # §4 макет трёх зон: [оглавление 210px][текст ≤820][жёлоб .mn]; нет h2 → одна колонка (.solo)
    toc = _toc_html(st["toc"])
    return ('<section class="panel" id="panel-%d">%s'
            '<div class="layout%s">%s<main><article class="stream">%s</article></main></div>'
            '</section>' % (i, meta_line, "" if toc else " solo", toc, st["html"]))


# ───────────────────────── CLI ─────────────────────────
def main():
    ap = argparse.ArgumentParser(description="doc-движок: папка *.md → self-contained view.html + линтер-гейт")
    ap.add_argument("src", help="папка-источник (один/несколько *.md со `status:`-шапкой)")
    ap.add_argument("--lint", action="store_true", help="только линтер, без записи")
    ap.add_argument("-o", "--out", help="путь выхода (по умолчанию <src>/view.html)")
    ap.add_argument("--title", help="заголовок вида (по умолчанию имя папки)")
    args = ap.parse_args()

    src = Path(args.src)
    if not src.is_dir():
        print("✗ не папка: %s" % src)
        return 2

    streams = load_streams(src)
    errors, warns = lint(streams)

    print("── ЛИНТЕР (doc-движок) ──")
    for w in warns:
        print("  ⚠ %s" % w)
    if errors:
        for e in errors:
            print("  ✗ %s" % e)
        print("ЛИНТЕР ПРОВАЛЕН: %d структурн. ошибк(а/и). Сборка прервана." % len(errors))
        return 1
    print("  ✓ структура и мат-долги в норме (%d мягк. предупрежд.)" % len(warns))
    total_open = sum(s["debt_open"] for s in streams)
    print("  потоков(вкладок): %d · открытых ⚑ всего: %d · %s"
          % (len(streams), total_open, " · ".join("%s→«%s»" % (s["name"], s["label"]) for s in streams)))

    if args.lint:
        return 0

    title = args.title or src.name
    out_text = build_html(streams, title)
    out_path = Path(args.out) if args.out else (src / "view.html")
    write_text(out_path, out_text)
    print("── СБОРКА ──")
    print("  ✓ %s (%d КБ, вкладок: %d)" % (out_path, len(out_text.encode("utf-8")) // 1024, len(streams)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
