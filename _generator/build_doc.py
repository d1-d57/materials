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


# ───────────────────────── поток текста: блоки → HTML (модель данных doc-движка) ─────────────────────────
def render_stream(body):
    """Пустая строка = граница блока. Порядок распознавания важен (флаги до заголовка,
    чтобы `## ⚑ …` тоже стал бейджем-долгом)."""
    out = []
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

        # 5. заголовок (# … #### …); хвост блока — как абзац
        hm = re.match(r"^(#{1,4})\s+(.*)$", first)
        if hm:
            lvl = len(hm.group(1))
            out.append("<h%d>%s</h%d>" % (lvl, render_inline(hm.group(2)), lvl))
            if len(lines) > 1:
                out.append("<p>%s</p>" % render_inline(_join(lines[1:])))
            continue

        # 6. список
        if all(l.lstrip().startswith("- ") for l in lines):
            items = "".join("<li>%s</li>" % render_inline(l.lstrip()[2:].strip()) for l in lines)
            out.append("<ul>%s</ul>" % items)
            continue

        # 7. абзац
        out.append("<p>%s</p>" % render_inline(joined))
    return "\n".join(out)


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
            "html": render_stream(body),
            "debt_open": max(0, opened - closed),
            "debt_raw": (opened, closed),
        })
    streams.sort(key=lambda s: (int(s["meta"].get("poryadok", "999") or "999"), s["name"]))
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
  --bg:#f7f4ee; --panel:#fffdf8; --text:#201d18; --muted:#6c655a;
  --rule:#ddd5c7; --accent:#7a1f1f; --insight-bg:#f2ecdd; --thread:#284862;
  --defn:#3a6b4f; --flag-open:#a11414; --flag-open-bg:#fbe9e9; --flag-closed:#2c7a2c;
  --flag-closed-bg:#e9f5e9; --link:#7a1f1f;
  --serif:Georgia,"Times New Roman",serif;
  --sans:"Segoe UI",system-ui,-apple-system,"Helvetica Neue",Arial,sans-serif;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--serif);
  line-height:1.62;font-size:18px;-webkit-text-size-adjust:100%}
a{color:var(--link)}
.wrap{max-width:960px;margin:0 auto;padding:2rem 1.5rem 5rem}
.doc-head{font-family:var(--sans)}
.doc-head h1{font-family:var(--serif);font-size:1.7rem;margin:.2em 0 .1em}
.gen-note{font-family:var(--sans);font-size:.8rem;color:var(--muted);margin:0 0 1.4rem}
.runtime-note{font-family:var(--sans);font-size:.82rem;line-height:1.5;background:#fff8e6;
  border:1px solid #e6d7a2;border-radius:6px;padding:.7rem .9rem;margin:0 0 1.6rem;color:#6a5a1e}
.runtime-note code{background:#f0e6c8;padding:0 .25em;border-radius:3px}

/* ── вкладки: CSS-only, скрытые radio + label (без сети/JS) ── */
.tabs>input.tab-radio{position:absolute;width:1px;height:1px;opacity:0;pointer-events:none}
.tabbar{display:flex;flex-wrap:wrap;gap:.25rem;border-bottom:2px solid var(--rule);margin:0 0 1.6rem}
.tabbar label{cursor:pointer;user-select:none;font-family:var(--sans);font-weight:600;
  font-size:.95rem;color:var(--muted);padding:.5rem 1.1rem;border:2px solid transparent;
  border-bottom:none;border-radius:9px 9px 0 0;margin-bottom:-2px;transition:color .12s}
.tabbar label:hover{color:var(--text)}
.panel{display:none}
{{TABCSS}}

/* ── поток текста ── */
.stream{max-width:840px;padding-right:200px;counter-reset:sec}
@media(max-width:900px){.stream{padding-right:0}}
.stream h2{font-family:var(--serif);font-size:1.28rem;margin:2rem 0 .6rem;counter-increment:sec}
.stream h2::before{content:counter(sec)". ";color:var(--muted)}
.stream h3{font-family:var(--serif);font-size:1.1rem;margin:1.5rem 0 .5rem}
.stream p{margin:.7em 0}
.stream ul{margin:.7em 0;padding-left:1.3em}
.stream li{margin:.25em 0}
blockquote{margin:1em 0;padding:.3em 0 .3em 1em;border-left:3px solid var(--rule);color:var(--muted)}
code{font-family:"SF Mono",Consolas,monospace;font-size:.9em;background:#efe9dd;padding:0 .25em;border-radius:3px}

/* ── поле .mn: float в правый жёлоб (CSS дословно из distillat-tehnika §2) ── */
.mn{float:right;clear:right;width:172px;margin:.35em -195px 1.1em 22px;
  font-family:var(--sans);font-size:.8rem;line-height:1.5;color:var(--muted);
  border-left:2px solid var(--rule);padding-left:.75em}
.mn b,.mn strong{color:var(--text)}
@media(max-width:900px){.mn{float:none;width:auto;margin:1.2em 0;
  border-left:3px solid var(--rule);padding:.4em 0 .4em .9em}}

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
    return ('<section class="panel" id="panel-%d">%s<div class="stream">%s</div></section>'
            % (i, meta_line, st["html"]))


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
