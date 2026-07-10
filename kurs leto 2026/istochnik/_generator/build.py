#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор istochnik/ → self-contained HTML (дизайн v4) + линтер + бэклинк-индекс.
Чистая stdlib (re, html, base64, pathlib, argparse) — запускается без pip/сети.

  python3 istochnik/_generator/build.py              # линтер(структурный гейт) + сборка L4 (kriptografiya, по умолчанию)
  python3 istochnik/_generator/build.py --build optimizaciya  # собрать конкретную лекцию по id
  python3 istochnik/_generator/build.py --lint       # только линтер
  python3 istochnik/_generator/build.py --backlinks turing   # все места →[turing]

Контракт: HTML — чистая функция источника. Каждый блок несёт data-source="<файл> §N"
и HTML-коммент перед собой (паттерн md-redline: правку из HTML вернуть в MD).
"""
import re, html as html_mod, base64, argparse, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # istochnik/
KARTA = ROOT / "karta"
DIZAJN = ROOT / "_dizajn"
OUT = ROOT / "_out"
LECTURE_GLOB = "L*-*.md"

TYPES_MAT = {"МАТЕМАТИКА", "ТЕХБЛОК", "ЧЁРНЫЙ-ЯЩИК"}
TYPES_ALL = {"КРЮЧОК", "МАТЕМАТИКА", "РАССКАЗ", "ТЕХБЛОК", "ЧЁРНЫЙ-ЯЩИК", "ДОМАШКА"}
MAT_FIELDS = ["утверждение", "логика", "подробность", "чёрный-ящик"]
TYPE_TAG = {"КРЮЧОК": ("t-hook", "Крючок"), "РАССКАЗ": ("t-story", "Рассказ"),
            "МАТЕМАТИКА": ("t-math", "Математика · руками"), "ТЕХБЛОК": ("t-tech", "Техблок"),
            "ЧЁРНЫЙ-ЯЩИК": ("t-box", "Чёрный ящик"), "ДОМАШКА": ("t-hw", "Домашка")}

# ───────────────────────── формулы: LaTeX-подмножество → unicode/HTML ─────────────────────────
# Порядок важен: сперва экранируем <>&, потом команды, потом sup/sub (вставляют теги).
_CMD = [
    (r"\\pmod\{([^}]*)\}", r"(mod \1)"), (r"\\pmod\s*([A-Za-z0-9]+)", r"(mod \1)"),
    (r"\\bmod", "mod"), (r"\\varphi", "φ"), (r"\\phi", "φ"),
    (r"\\not\\equiv", "≢"), (r"\\equiv", "≡"),
    (r"\\geq", "≥"), (r"\\ge", "≥"), (r"\\leq", "≤"), (r"\\le", "≤"),
    (r"\\neq", "≠"), (r"\\approx", "≈"), (r"\s*\\cdot\s*", "·"), (r"\s*\\times\s*", "×"),
    (r"\\Rightarrow", "⇒"), (r"\\rightarrow", "→"), (r"\\to", "→"), (r"\\iff", "⇔"),
    (r"\\int", "∫"), (r"\\infty", "∞"),                         # ДО \in: иначе \int→«∈t» (тихая подмена)
    (r"\\in", "∈"), (r"\\cap", "∩"), (r"\\cup", "∪"),
    (r"\\cdots", "⋯"), (r"\\ldots", "…"), (r"\\dots", "…"),
    (r"\\sum", "∑"), (r"\\prod", "∏"), (r"\\nabla", "∇"),
    (r"\\min", "min"), (r"\\max", "max"), (r"\\sup", "sup"), (r"\\log", "log"),
    (r"\\mu", "μ"), (r"\\nu", "ν"), (r"\\lambda", "λ"), (r"\\theta", "θ"),
    (r"\\alpha", "α"), (r"\\beta", "β"), (r"\\gamma", "γ"), (r"\\delta", "δ"),
    (r"\\pi", "π"), (r"\\sigma", "σ"), (r"\\omega", "ω"),       # проактивно, тот же класс
    (r"\\textstyle", ""), (r"\\displaystyle", ""),             # директивы стиля, без вывода
    (r"\\text\{([^}]*)\}", r"\1"), (r"\\mathsf\{([^}]*)\}", r"\1"), (r"\\mathrm\{([^}]*)\}", r"\1"),
    (r"\\mathsf\s+", ""),                                       # §16: c^{\mathsf T} — форма БЕЗ скобок
    (r"\\tfrac\{([^}]*)\}\{([^}]*)\}", r"\1/\2"), (r"\\frac\{([^}]*)\}\{([^}]*)\}", r"\1/\2"),
    (r"\\tfrac(\d)(\d)", r"\1/\2"),                             # §28: \tfrac13 — короткая форма без скобок
    (r"\\[Bb]igg?\(", "("), (r"\\[Bb]igg?\)", ")"),
    (r"\\[Bb]igg?\[", "["), (r"\\[Bb]igg?\]", "]"),
    (r"\\left\(", "("), (r"\\right\)", ")"),
    (r"\\left\[", "["), (r"\\right\]", "]"),
    (r"\\\{", "{"), (r"\\\}", "}"),                             # §25: экранир. \{ \} → {} (снимутся шагом 4)
    (r"\\\*", "*"),                                             # §11: экранир. звёздочка \* (X^\*) → *
    (r"\\qquad", "    "),                                       # вдвое шире \quad
    (r"\\quad", "  "), (r"\\,", " "), (r"\\;", " "),
    (r"\\:", " "), (r"\\!", ""), (r"\\ ", " "),
    (r"\\([×·])", r"\1"),                                       # §175: осиротевший \ перед ×/· (после \ \times)
]
_SUP = {"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶",
        "7": "⁷", "8": "⁸", "9": "⁹", "-": "⁻", "+": "⁺", "n": "ⁿ"}
_SUB = {"0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄", "5": "₅", "6": "₆",
        "7": "₇", "8": "₈", "9": "₉"}

def _script(inner, table):
    """Если все символы маппятся в unicode-надстрочные/подстрочные — отдать unicode, иначе тег."""
    if inner and all(ch in table for ch in inner):
        return "".join(table[ch] for ch in inner)
    return None

def _matrix_to_text(m):
    r"""\begin{…matrix}…\end{…matrix} → плоский «(a  b  c; d  e  f)».
    Вызывается ПОСЛЕ html.escape, поэтому разделитель столбцов — экранированный «&amp;», не «&».
    Строки разделены «\\» (двумя бэкслешами), их escape не трогает."""
    rows = [r for r in m.group(1).split(r"\\") if r.strip()]
    return "(" + "; ".join("  ".join(c.strip() for c in row.split("&amp;")) for row in rows) + ")"

def latex_to_html(s):
    s = html_mod.escape(s)                       # 1. экранируем литералы < > &
    s = re.sub(r"\\begin\{[a-zA-Z]*matrix\}(.*?)\\end\{[a-zA-Z]*matrix\}",  # 1b. матрицы → плоский текст
               _matrix_to_text, s, flags=re.S)
    for pat, rep in _CMD:                          # 2. команды
        s = re.sub(pat, rep, s)
    # 3. надстрочные/подстрочные
    def sup_group(m):
        inner = m.group(1)
        u = _script(inner, _SUP)
        return u if u is not None else "<sup>%s</sup>" % inner
    def sub_group(m):
        inner = m.group(1)
        u = _script(inner, _SUB)
        return u if u is not None else "<sub>%s</sub>" % inner
    s = re.sub(r"\^\{([^}]*)\}", sup_group, s)
    s = re.sub(r"_\{([^}]*)\}", sub_group, s)
    s = re.sub(r"\^(.)", lambda m: _SUP.get(m.group(1), "<sup>%s</sup>" % m.group(1)), s)
    s = re.sub(r"_(.)", lambda m: _SUB.get(m.group(1), "<sub>%s</sub>" % m.group(1)), s)
    s = s.replace("{", "").replace("}", "")        # 4. убрать остаточные группирующие скобки
    return s

# ───────────────────────── модель источника ─────────────────────────
class Lecture:
    def __init__(self, path):
        self.path = path
        self.name = path.name
        raw = path.read_text(encoding="utf-8")
        self.header, self.body = self._split(raw)
        self.id = self.header.get("id", "")
        self.title = self.header.get("title", self.id)
        self.status = self.header.get("status", "skelet")
        self.sections = self._parse_sections(self.body)

    @staticmethod
    def _split(raw):
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        if not m:
            return {}, raw
        head, body = {}, m.group(1)
        for line in body.splitlines():
            mm = re.match(r"^([\w-]+):\s*(.*)$", line)
            if mm:
                head[mm.group(1)] = mm.group(2).strip()
        return head, m.group(2)

    @staticmethod
    def _parse_sections(body):
        secs, cur = [], None
        for line in body.splitlines():
            if line.startswith("## "):
                parts = [p.strip() for p in line[3:].split(" · ")]
                par = parts[0].lstrip("§").strip()
                typ = parts[1] if len(parts) > 1 else ""
                rest = parts[2] if len(parts) > 2 else ""
                flags = re.findall(r"\{([^}]*)\}", rest)
                title = re.sub(r"\s*\{[^}]*\}", "", rest).strip()
                cur = {"par": par, "type": typ, "title": title, "flags": flags, "lines": []}
                secs.append(cur)
            elif cur is not None:
                cur["lines"].append(line)
        return secs

def budget(header):
    m = re.search(r"math_blokov:\s*(\d+).*?vsego_blokov:\s*(\d+)", header.get("budget", ""))
    return (int(m.group(1)), int(m.group(2))) if m else (0, 0)

# ───────────────────────── реестр id (декларации) ─────────────────────────
def load_registry():
    reg = {"lecture": {}, "person": {}, "theory": {}, "thread": {}, "artifact": {}}
    dups = []
    lectures = {}
    for p in sorted(ROOT.glob(LECTURE_GLOB)):
        lec = Lecture(p)
        if lec.id in reg["lecture"]:
            dups.append(("lecture", lec.id))
        reg["lecture"][lec.id] = {"title": lec.title, "lec": lec}
        lectures[lec.id] = lec

    def card_lines(fn):
        f = KARTA / fn
        return f.read_text(encoding="utf-8").splitlines() if f.exists() else []

    for line in card_lines("lica.md"):
        m = re.match(r"^-\s*\{([\w-]+)\}\s*(.*)$", line)
        if not m:
            continue
        pid, rest = m.group(1), m.group(2)
        if pid in reg["person"]:
            dups.append(("person", pid))
        name = rest.split("|")[0].strip()
        fm = re.search(r"фото:([^\s|]+)", rest)
        bio = re.search(r"био:([^|]+)", rest)
        role = re.search(r"роль:([^|]+)", rest)
        reg["person"][pid] = {"name": name, "foto": fm.group(1) if fm else "",
                              "bio": bio.group(1).strip() if bio else "",
                              "role": role.group(1).strip() if role else ""}
    for fn, key in [("teorii.md", "theory"), ("svyazujushchee.md", "artifact")]:
        for line in card_lines(fn):
            m = re.match(r"^-\s*\{([\w-]+)\}\s*(.*)$", line)
            if m:
                tid = m.group(1)
                if tid in reg[key]:
                    dups.append((key, tid))
                reg[key][tid] = {"label": m.group(2).split("|")[0].strip()}
    # нити из graf.md (секция НИТИ)
    in_threads = False
    for line in card_lines("graf.md"):
        if line.startswith("## "):
            in_threads = "НИТИ" in line
            continue
        if in_threads:
            m = re.match(r"^-\s*\{([\w-]+)\}\s*(.*)$", line)
            if m:
                nid = m.group(1)
                if nid in reg["thread"]:
                    dups.append(("thread", nid))
                reg["thread"][nid] = {"label": m.group(2).split("|")[0].strip()}
    return reg, dups, lectures

REF_RE = re.compile(r"→\[([^\]]+)\]")

def split_ref(token):
    """→[T:x]/→[N:x]/→[L:x]/→[x] → (kind|None, core_id)."""
    token = token.strip()
    if ":" in token:
        pre, core = token.split(":", 1)
        return pre.strip(), core.strip()
    return None, token

def resolve_kind(core, reg):
    for k in ("lecture", "person", "theory", "thread", "artifact"):
        if core in reg[k]:
            return k
    return None

# ───────────────────────── рендер инлайна ─────────────────────────
def render_inline(text, reg, ctx):
    """markdown-подмножество (**bold**, *em*), формулы $…$/$$…$$, ссылки →[id]."""
    # 1. защитим формулы плейсхолдерами (до экранирования прозы)
    formulas = []
    def stash(m, disp):
        formulas.append((disp, m))
        return "\x00F%d\x00" % (len(formulas) - 1)
    text = re.sub(r"\$\$(.+?)\$\$", lambda m: stash(m.group(1), True), text, flags=re.S)
    text = re.sub(r"\$(.+?)\$", lambda m: stash(m.group(1), False), text)
    # 2. ссылки →[id] → плейсхолдеры
    refs = []
    def stash_ref(m):
        refs.append(m.group(1))
        return "\x00R%d\x00" % (len(refs) - 1)
    text = REF_RE.sub(stash_ref, text)
    # 3. экранируем прозу, затем markdown-инлайн
    text = html_mod.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    # 4. вернём формулы
    def unstash_f(m):
        disp, fm = formulas[int(m.group(1))]
        inner = latex_to_html(fm)
        return ('<div class="eq">%s</div>' % inner) if disp else ('<span class="m">%s</span>' % inner)
    text = re.sub(r"\x00F(\d+)\x00", unstash_f, text)
    # 5. вернём ссылки как чипы/портреты
    def unstash_r(m):
        return render_ref(refs[int(m.group(1))], reg, ctx)
    text = re.sub(r"\x00R(\d+)\x00", unstash_r, text)
    return text

def render_ref(token, reg, ctx):
    pre, core = split_ref(token)
    kind = resolve_kind(core, reg)
    if kind == "lecture":
        return '<span class="lref">→ %s</span>' % html_mod.escape(reg["lecture"][core]["title"])
    if kind == "person":
        p = reg["person"][core]
        if core not in ctx["seen_persons"]:
            ctx["seen_persons"].add(core)
            ctx["pending_portraits"].append(core)
        # лицо в прозе — спокойное имя, не кнопка (портрет даёт первое упоминание)
        return '<span class="pers">%s</span>' % html_mod.escape(p["name"])
    if kind == "thread":
        return '<span class="spine sp-meta">%s</span>' % html_mod.escape(reg["thread"][core]["label"])
    if kind == "theory":
        return '<span class="ln">→ %s</span>' % html_mod.escape(reg["theory"][core]["label"])
    return '<span class="ln">→ %s</span>' % html_mod.escape(core)   # не должно случаться: линтер ловит

def portrait_html(pid, reg):
    p = reg["person"][pid]
    foto_path = DIZAJN / "foto" / p["foto"] if p["foto"] else None
    # короткая подпись: даты (1-й сегмент био до «;») + роль-фраза; полный био — в lica.md
    dates = p["bio"].split(";")[0].strip() if p["bio"] else ""
    short = " · ".join(x for x in (dates, p.get("role", "")) if x)
    cap = '<figcaption><span class="pn">%s</span>%s</figcaption>' % (
        html_mod.escape(p["name"]), html_mod.escape(short))
    if foto_path and foto_path.exists():
        return ('<figure class="port"><div class="pi" style="background-image:var(--p-%s)"></div>%s</figure>'
                % (pid, cap))
    initial = (p["name"] or "·")[0]
    return ('<figure class="port mono"><div class="pi"><span>%s</span></div>%s</figure>'
            % (html_mod.escape(initial), cap))

# ───────────────────────── рендер блоков ─────────────────────────
def fields_of(section):
    """[поле] → текст, для матблоков."""
    text = "\n".join(section["lines"])
    out = {}
    for i, fld in enumerate(MAT_FIELDS):
        m = re.search(r"\*\*\[%s\]\*\*\s*(.*?)(?=\n\*\*\[|\n>\s*поле:|\Z)" % re.escape(fld), text, re.S)
        out[fld] = m.group(1).strip() if m else None
    return out

def footnotes_of(section):
    res = []
    for line in section["lines"]:
        m = re.match(r"^>\s*поле:(\S+)\s*(.*)$", line)
        if m:
            res.append((m.group(1), m.group(2).strip()))
    return res

def prose_of(section):
    """непустые строки, не поля-сноски, не теги матблока."""
    keep = []
    for line in section["lines"]:
        if line.startswith(">") or re.match(r"^\*\*\[", line):
            continue
        keep.append(line)
    return "\n".join(keep).strip()

FOOTNOTE_MAP = {
    "нить": ("aside", "note thread", "нить"), "честно": ("aside", "note honest", "честно"),
    "в-кармане": ("aside", "note", "в кармане"), "отложимо": ("aside", "note", "отложимо"),
    "боковой": ("aside", "note", "на полях"),
    "cue-визуал": ("cue", None, "Визуал"), "cue-интерактив": ("cue", None, "Интерактив"),
}

def render_footnote(kind, body, reg, ctx, src):
    rendered = render_inline(body, reg, ctx)
    el, cls, label = FOOTNOTE_MAP.get(kind, ("aside", "note", kind))
    if el == "cue":
        return '<div class="cue" data-source="%s"><b>%s:</b> %s</div>' % (src, html_mod.escape(label), rendered)
    return '<aside class="%s" data-source="%s"><span class="nt">%s</span>%s</aside>' % (
        cls, src, html_mod.escape(label), rendered)

def comment(src):
    return "<!-- src: %s -->" % src

def render_section(sec, lec, reg, ctx):
    src_base = "%s §%s" % (lec.name, sec["par"])
    typ = sec["type"]
    tag_cls, tag_label = TYPE_TAG.get(typ, ("t-story", typ))
    head_label = "§%s · %s" % (sec["par"], tag_label)
    flag_suffix = (" · " + " · ".join(sec["flags"])) if sec["flags"] else ""
    out = []
    # h3
    out.append('%s\n<h3><span class="h3tag %s">%s</span> %s%s</h3>' % (
        comment(src_base), tag_cls, html_mod.escape(head_label),
        html_mod.escape(sec["title"]), html_mod.escape(flag_suffix)))

    ctx["pending_portraits"] = []

    if typ == "ДОМАШКА":
        out.append(render_homework(sec, lec, reg, ctx, src_base))
        return "\n".join(out), False

    if typ in TYPES_MAT:
        flds = fields_of(sec)
        is_theorem = "теорема-заголовок" in sec["flags"]
        # утверждение → claimbox
        if flds["утверждение"]:
            s = src_base + " [утверждение]"
            label = "Теорема-заголовок" if is_theorem else "Утверждение"
            out.append('%s\n<div class="claimbox" data-source="%s"><span class="nt">%s</span> %s</div>' % (
                comment(s), s, label, render_inline(flds["утверждение"], reg, ctx)))
        if flds["логика"]:
            s = src_base + " [логика]"
            out.append('%s\n<p data-source="%s"><b>Логика.</b> %s</p>' % (
                comment(s), s, render_inline(flds["логика"], reg, ctx)))
        if flds["подробность"]:
            s = src_base + " [подробность]"
            out.append('%s\n<div class="claimbox" data-source="%s"><span class="nt">Подробность</span> %s</div>' % (
                comment(s), s, render_inline(flds["подробность"], reg, ctx)))
        if flds["чёрный-ящик"]:
            s = src_base + " [чёрный-ящик]"
            out.append('%s\n<p data-source="%s"><b>Чёрный ящик.</b> %s</p>' % (
                comment(s), s, render_inline(flds["чёрный-ящик"], reg, ctx)))
    else:  # КРЮЧОК / РАССКАЗ — проза
        prose = prose_of(sec)
        if prose:
            for para in re.split(r"\n\s*\n", prose):
                out.append('%s\n<p data-source="%s">%s</p>' % (
                    comment(src_base), src_base, render_inline(para.strip(), reg, ctx)))

    # портреты лиц, впервые упомянутых в этой секции — сразу после h3
    if ctx["pending_portraits"]:
        figs = "\n".join(portrait_html(pid, reg) for pid in ctx["pending_portraits"])
        out.insert(1, figs)

    # поля-сноски
    for kind, body in footnotes_of(sec):
        out.append(render_footnote(kind, body, reg, ctx, src_base))

    return "\n".join(out), (typ == "ТЕХБЛОК")

def render_homework(sec, lec, reg, ctx, src_base):
    items = []
    for line in sec["lines"]:
        m = re.match(r"^\d+\.\s*(.*)$", line)
        if not m:
            continue
        body = m.group(1)
        star = ""
        if body.startswith("*"):
            star = '<span class="star">*</span> '
            body = body[1:].strip()
        body = re.sub(r"\(([^)]*)\)\s*$", lambda mm: '<span class="hint">(%s)</span>' % mm.group(1), body)
        items.append("<li>%s%s</li>" % (star, render_inline(body, reg, ctx)))
    return '<ol class="hw" data-source="%s">\n%s\n</ol>' % (src_base, "\n".join(items))

# ───────────────────────── сборка одной лекции ─────────────────────────
def build_lecture(lec, reg):
    ctx = {"seen_persons": set(), "pending_portraits": []}
    body_parts, inside_tech = [], False
    for sec in lec.sections:
        html_sec, is_tech = render_section(sec, lec, reg, ctx)
        if is_tech and not inside_tech:
            body_parts.append('<div class="actdiv"><span class="ad-k">АКТ II</span>'
                              '<span class="ad-t">Технический блок — отделяемый</span></div>')
            body_parts.append('<div class="techblock"><div class="plaque">'
                              '⏸ Можно уйти — досмотришь в записи. Дальше зал всерьёз работает формулы руками.</div>')
            inside_tech = True
        elif inside_tech and not is_tech:
            body_parts.append("</div>")
            inside_tech = False
        body_parts.append(html_sec)
    if inside_tech:
        body_parts.append("</div>")

    # шапка-витрина
    mb, vb = budget(lec.header)
    theory = lec.header.get("theory", "")
    cel = lec.header.get("cel", "")
    teorema = lec.header.get("teorema-zagolovok", "")
    role = lec.header.get("role", "")
    masthead_body = []
    masthead_body.append('<p class="kicker"><span class="lec-num">Лекция %s</span> · %s</p>' % (
        html_mod.escape(lec.header.get("poryadok", "")), html_mod.escape(role)))
    masthead_body.append("<h2>%s</h2>" % html_mod.escape(lec.title))
    masthead_body.append('<p class="role">Цель: %s · теория: %s · теорема-заголовок: %s</p>' % (
        html_mod.escape(cel), html_mod.escape(theory.strip("[]")), html_mod.escape(teorema)))
    masthead_body.append('<span class="budget">бюджет: %d матблоков / %d блоков · статус: %s</span>' % (
        mb, vb, html_mod.escape(lec.status)))

    full_body = "\n".join(masthead_body) + "\n\n" + "\n\n".join(body_parts)

    # стиль фото: base64 присутствующих портретов
    photo_vars = []
    for pid, p in reg["person"].items():
        fp = DIZAJN / "foto" / p["foto"] if p["foto"] else None
        if fp and fp.exists():
            b64 = base64.b64encode(fp.read_bytes()).decode("ascii")
            photo_vars.append('--p-%s:url("data:image/jpeg;base64,%s")' % (pid, b64))
    photos_style = '<style id="photos">:root{%s}</style>' % ";".join(photo_vars) if photo_vars else ""

    css = (DIZAJN / "stil.css").read_text(encoding="utf-8")
    tpl = (DIZAJN / "shablon.html").read_text(encoding="utf-8")
    repl = {
        "TITLE": "Лекция %s «%s»" % (lec.header.get("poryadok", ""), lec.title),
        "PHOTOS": photos_style, "STYLE": css,
        "TOP_LEFT": "Летний онлайн-курс · научпоп-математика",
        "TOP_RIGHT": "Лекция %s · формат v4 · генератор istochnik/" % lec.header.get("poryadok", ""),
        "H1": html_mod.escape(lec.title),
        "SUB": "Лекция %s · %s · сгенерировано из источника" % (
            html_mod.escape(lec.header.get("poryadok", "")), html_mod.escape(role)),
        "LEDE": ("Самодостаточная страница лекции в формате v4. HTML — чистая функция источника "
                 "<code>%s</code>; портрет вшит base64 (открывается офлайн). Каждый блок несёт "
                 "<code>data-source</code> — правку из HTML видно, куда вернуть в MD." % html_mod.escape(lec.name)),
        "SECTION_ID": lec.id,
        "BODY": full_body,
        "FOOTER": ("Сгенерировано из <code>istochnik/%s</code> генератором "
                   "<code>_generator/build.py</code>. Правь источник, не HTML." % html_mod.escape(lec.name)),
    }
    for k, v in repl.items():
        tpl = tpl.replace("{{%s}}" % k, v)
    return tpl

# ───────────────────────── линтер ─────────────────────────
def collect_refs(lectures):
    """[(file, §, token, line)] по всем лекциям."""
    refs = []
    for lec in lectures.values():
        cur = "?"
        for line in lec.body.splitlines():
            if line.startswith("## "):
                cur = line[3:].split(" · ")[0].strip().lstrip("§")
            for m in REF_RE.finditer(line):
                refs.append((lec.name, cur, m.group(1), line.strip()))
    return refs

def lint(reg, dups, lectures):
    errors, warns = [], []
    # — структурные (жёсткий гейт) —
    for ns, idv in dups:
        errors.append("дубль id [%s]: {%s}" % (ns, idv))
    # все объявленные id уникальны и между пространствами
    seen = {}
    for ns in reg:
        for idv in reg[ns]:
            if idv in seen:
                errors.append("id {%s} объявлен в двух пространствах: %s и %s" % (idv, seen[idv], ns))
            seen[idv] = ns
    # →[id] резолвится
    for fn, par, token, line in collect_refs(lectures):
        pre, core = split_ref(token)
        if resolve_kind(core, reg) is None:
            errors.append("%s §%s: ссылка →[%s] не резолвится (нет объявленного id «%s»)" % (fn, par, token, core))
    # заголовки валидны + матблок несёт 4 поля
    for lec in lectures.values():
        for sec in lec.sections:
            if sec["type"] not in TYPES_ALL:
                errors.append("%s §%s: неизвестный ТИП раздела «%s»" % (lec.name, sec["par"], sec["type"]))
            if not re.match(r"^[\w.]+$", sec["par"]):
                errors.append("%s: битый номер раздела «§%s»" % (lec.name, sec["par"]))
            if sec["type"] in TYPES_MAT:
                flds = fields_of(sec)
                missing = [f for f in MAT_FIELDS if not flds[f]]
                if missing:
                    errors.append("%s §%s: матблок без полей %s" % (lec.name, sec["par"], missing))
    # битая трансклюзия {{вкл:id}}
    for lec in lectures.values():
        for m in re.finditer(r"\{\{вкл:([\w-]+)\}\}", lec.body):
            if resolve_kind(m.group(1), reg) is None:
                errors.append("%s: битая трансклюзия {{вкл:%s}}" % (lec.name, m.group(1)))

    # — редакционные (мягко; жёстко только при status: polno) —
    edit = []
    for lec in lectures.values():
        if lec.status == "skelet":
            continue
        mb, vb = budget(lec.header)
        nmat = sum(1 for s in lec.sections if s["type"] in TYPES_MAT and all(fields_of(s).values()))
        if mb and nmat < mb:
            edit.append(("%s: %d/%d матблоков" % (lec.id, nmat, mb), lec.status))
        nhw = sum(1 for s in lec.sections if s["type"] == "ДОМАШКА"
                  for ln in s["lines"] if re.match(r"^\d+\.", ln))
        if not (5 <= nhw <= 10):
            edit.append(("%s: домашка %d задач (норма 5–10)" % (lec.id, nhw), lec.status))
    # квоты графа
    threads = read_threads()
    cross5 = sum(1 for t in threads if len(t["lec"]) >= 5)
    cross4 = sum(1 for t in threads if len(t["lec"]) >= 4)
    edges = read_edges()
    if cross5 < 3:
        edit.append(("граф: сквозных через ≥5 лекций %d (норма ≥3)" % cross5, "—"))
    if cross4 < 6:
        edit.append(("граф: сквозных через ≥4 лекций %d (норма ≥6)" % cross4, "—"))
    if len(edges) < 10:
        edit.append(("граф: парных рёбер %d (норма ≥10)" % len(edges), "—"))
    types = set(t["type"] for t in threads if t["type"])
    if len(types) < 4:
        edit.append(("граф: типов нитей %d (норма ≥4)" % len(types), "—"))
    # лицо в 2–5 лекциях
    for pid, p in read_lica_appearances().items():
        if not (2 <= p <= 5):
            edit.append(("лицо {%s}: появлений в %d лекциях (норма 2–5)" % (pid, p), "—"))

    # эскалация редакционных при polno
    for msg, st in edit:
        if st == "polno":
            errors.append("[polno] " + msg)
        else:
            warns.append(msg)
    return errors, warns

def read_threads():
    f = KARTA / "graf.md"
    res, in_t = [], False
    if not f.exists():
        return res
    for line in f.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_t = "НИТИ" in line
            continue
        if in_t:
            m = re.match(r"^-\s*\{[\w-]+\}", line)
            if m:
                lecs = re.search(r"лекции:\[([^\]]*)\]", line)
                typ = re.search(r"тип:([^\s|]+)", line)
                res.append({"lec": [x.strip() for x in lecs.group(1).split(",")] if lecs else [],
                            "type": typ.group(1) if typ else ""})
    return res

def read_edges():
    f = KARTA / "graf.md"
    res, in_e = [], False
    if not f.exists():
        return res
    for line in f.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_e = "РЁБРА" in line
            continue
        if in_e and re.match(r"^-\s+\w+\s*[~-]", line):
            res.append(line)
    return res

def read_lica_appearances():
    f = KARTA / "lica.md"
    res = {}
    if not f.exists():
        return res
    for line in f.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^-\s*\{([\w-]+)\}", line)
        if m:
            app = re.search(r"появления:\[([^\]]*)\]", line)
            lecs = set()
            if app:
                for piece in app.group(1).split(","):
                    lid = piece.strip().split("§")[0].strip()
                    if lid:
                        lecs.add(lid)
            res[m.group(1)] = len(lecs)
    return res

# ───────────────────────── бэклинки ─────────────────────────
def backlinks(query, lectures):
    hits = []
    for fn, par, token, line in collect_refs(lectures):
        pre, core = split_ref(token)
        if core == query:
            hits.append((fn, par, line))
    return hits

# ───────────────────────── CLI ─────────────────────────
def main():
    ap = argparse.ArgumentParser(description="Генератор istochnik/ → HTML + линтер + бэклинки")
    ap.add_argument("--lint", action="store_true", help="только линтер, без сборки")
    ap.add_argument("--backlinks", metavar="ID", help="показать все места →[ID]")
    ap.add_argument("--build", metavar="ID", help="собрать конкретную лекцию по id (по умолчанию — kriptografiya, для обратной совместимости)")
    args = ap.parse_args()

    reg, dups, lectures = load_registry()

    if args.backlinks:
        hits = backlinks(args.backlinks, lectures)
        if not hits:
            print("→[%s]: упоминаний не найдено" % args.backlinks)
        else:
            print("→[%s] — задето в %d месте(ах):" % (args.backlinks, len(hits)))
            for fn, par, line in hits:
                print("  %s §%s | %s" % (fn, par, line))
        return 0

    errors, warns = lint(reg, dups, lectures)
    print("── ЛИНТЕР ──")
    for w in warns:
        print("  ⚠ редакц.: %s" % w)
    if errors:
        for e in errors:
            print("  ✗ структ.: %s" % e)
        print("ЛИНТЕР ПРОВАЛЕН: %d структурн. ошибк(а/и). Сборка прервана." % len(errors))
        return 1
    print("  ✓ структурные проверки пройдены (%d редакц. замечани(й))" % len(warns))

    if args.lint:
        return 0

    OUT.mkdir(exist_ok=True)
    build_id = args.build or "kriptografiya"
    target = reg["lecture"].get(build_id)
    if not target:
        print("нет лекции %s — нечего собирать" % build_id)
        return 1
    lec = target["lec"]
    if lec.status == "skelet":
        print("лекция %s — status: skelet, собирать нечего" % build_id)
        return 1
    html_out = build_lecture(lec, reg)
    out_path = OUT / ("L%s-%s.html" % (lec.header.get("poryadok", ""), build_id))
    out_path.write_text(html_out, encoding="utf-8")
    print("── СБОРКА ──")
    print("  ✓ %s (%d КБ)" % (out_path.relative_to(ROOT.parent), len(html_out) // 1024))
    return 0

if __name__ == "__main__":
    sys.exit(main())
