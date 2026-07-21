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
        st["html"], st["toc"] = render_stream(st["body"], "s%d" % i)
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
