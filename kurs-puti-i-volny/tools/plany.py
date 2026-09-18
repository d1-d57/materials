#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator of the plan VIEWS for course «Пути и волны» — reads `plan/src/punkty.md`
(the ONE home of the item list) and writes seven derived files. Standard library only.

WHY THIS EXISTS. The item list used to live by hand in several files and had already
diverged three times (`../SBORKA/KARTA-rashozhdeniy.md`, rows Р5, Р10, Р13). Now the
item is an atom that lives ONCE, in `punkty.md`; every other plan — year, part «до
анализа», quarter, lecture — is a VIEW this script derives from it, exactly like
`tools/indeks.py` derives `INDEKS.md` from the corpus. A view is never hand-edited;
`--proverit` catches a hand edit by re-generating in memory and diffing against disk.

PUNKTY.MD FORMAT (what this parser assumes — keep in sync if you change the source).
  * One item = one block starting with an anchor line `<!--id: p-NN-->` followed by a
    `### p-NN` heading, followed by plain `ключ: значение` lines. Known keys are listed
    in `ITEM_FIELDS` below. A line that is not a recognised `ключ:` and is not blank is
    treated as a CONTINUATION of the previous field (this is how a future multi-line
    `raskadrovka` — one `beat: <minute> — <text>` per line — is meant to be read; today
    every multi-line field is empty, so this path is untested by real data but is exercised
    by the verifier's mutation tests).
  * A block starts with `<!--id: p-`; the block `<!--id: finish-->` is a terminal marker,
    not an item, and is only ever a valid TARGET of `obobshchaetsya-v` — it is not parsed
    as an item and carries none of `ITEM_FIELDS`.
  * A "## Уровни" section holds one `### Уровень: <name>` block per LEVEL (`god`,
    `polugodie-1`, `polugodie-2`, `chast-do-analiza`, `chetvert-1`..`chetvert-4`), each with
    `obobshchenie:` and `svod:` lines. These feed the opening sentence the owner's mandate
    requires every generated plan to carry ("how this level generalises the finer one").

⭐ FIELDS (owner's mandate Д2: architecture and filling are separate positions — this
script never invents their content, only carries whatever is in `punkty.md`):
  imya, vopros, teorema, zadacha.

VIEWS WRITTEN (all under `plan/src/`, all begin with a "generated, do not hand-edit"
line and a YAML header carrying `opisanie:` — `indeks.py` requires that field on every
new .md, generated or not):
  god.md                  — year: every item one line, `imya` + `vopros`.
  chast-1-do-analiza.md   — part «до анализа» (`chast: do-analiza` items): `teorema`.
  chetvert-1..4.md        — quarter: all four ⭐ fields in full, plus the karkas source
                             quote (`iz-karkasa`) as context for whoever fills them in.
  lekciya-1.md            — lecture: item `p-01` unfolded from its `raskadrovka`.

LINKAGE `indeks.py`/`graf.py [c]` READ (see docstring note further down on the ONE known
gap between this design and the CURRENT `graf.py [c]`, which this script does not edit —
it is outside this position's zone):
  god sections      <!--id: god-pNN-->      link [[p-NN]]
  chast sections    <!--id: chast-pNN-->    link [[god-pNN]]              (chast: do-analiza items only)
  chetvert sections <!--id: chetvert-pNN--> link [[chast-pNN]] or [[god-pNN]]
                                             (do-analiza items link up to chast-pNN;
                                              analiz items — block 7, «Пределы» — have no
                                              chast-pNN of their own and link straight to
                                              god-pNN, per the owner's spec in the kod_
                                              brief §2 "Linkage that the existing gates
                                              can read")
  lekciya sections  <!--id: lekciya-pNN-->  link [[chetvert-pNN]]

  🔴 KNOWN GAP, NOT FIXED HERE (graf.py is read-only to this position — see the executor's
  `## ВОПРОСЫ` in the kod_ brief for the exact patch needed): `graf.py`'s `gate_c` hard-codes
  the parent of a `chetvert-*` anchor to be a `chast-*` id ONLY; it has no exception for an
  item whose `chast` is `analiz`. So the six `chetvert-pNN` sections of the analysis part
  (quarter 4, items p-28..p-33) link `[[god-pNN]]` as this docstring and the brief require,
  and `graf.py`'s CURRENT `gate_c` will still count them as orphans — not because the link
  is wrong, but because `gate_c`'s `parent_map = {'chetvert': 'chast', ...}` has no second
  accepted parent prefix. The fix `graf.py` needs (when someone is allowed to touch it):
  accept target prefix `god-` as an ALTERNATIVE parent for a `chetvert-*` anchor whenever
  no `chast-*` link is present, or equivalently look at the item's own `chast` field. Until
  then, `graf.py | grep -A3 '^[c]'` will read `orphans: 6` for a fully-built punkty.md, and
  that is a documented, expected mismatch — not a bug in this file.

RUN
    python3 tools/plany.py                      # (re)build all seven views, print their paths
    python3 tools/plany.py --proverit            # validate only, write nothing; rc=1 on any
                                                  # failure (see gates below); rc=0 if clean
    python3 tools/plany.py --proverit --napolnennye N   # also require the four ⭐ fields to
                                                  # be non-empty for every item of quarter N
                                                  # (default: 1). `--napolnennye none` skips
                                                  # this one check entirely.

GATES (`--proverit`, rc=1 on ANY of):
  1. an item without `opiraetsya` (except the very first item in the file);
  2. a dangling id in `opiraetsya` / `obobshchaetsya-v` (not an existing item id, and not
     the terminal marker `finish`);
  3. an item without `obobshchaetsya-v` (the course's own selection gate: "an item with
     no generalisation does not enter the course");
  4. items per quarter != sessions per quarter, read from `../proverki/kalendar_goda.py`
     (imported, never retyped — the 6/8/9/10 split lives in exactly one place);
  5. a ⭐ field empty in the quarter named by `--napolnennye` (default 1; `none` skips it);
  6. a generated view that differs from what this script would write right now — i.e. a
     hand edit. A MISSING view file is not a hand edit (nothing to diff against yet) and
     is silently skipped by this check; the plain run below always writes it.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
KPV_DIR = TOOLS_DIR.parent
SRC_DIR = KPV_DIR / "plan" / "src"
PUNKTY = SRC_DIR / "punkty.md"

sys.path.insert(0, str(KPV_DIR / "proverki"))
import kalendar_goda  # noqa: E402  (path set up above on purpose)

ITEM_FIELDS = [
    "id", "imya", "vopros", "teorema", "zadacha", "doska", "ves",
    "chetvert", "polovina", "chast", "opiraetsya", "obobshchaetsya-v",
    "adres", "iz-karkasa", "raskadrovka",
]
STAR_FIELDS = ["imya", "vopros", "teorema", "zadacha"]
LEVELS = ["god", "polugodie-1", "polugodie-2", "chast-do-analiza",
          "chetvert-1", "chetvert-2", "chetvert-3", "chetvert-4"]

RE_ITEM_START = re.compile(r"^<!--id:\s*(p-\d+)\s*-->\s*$", re.M)
RE_ANY_ANCHOR = re.compile(r"^<!--id:\s*[a-zA-Z0-9_\-]+\s*-->\s*$", re.M)
RE_FIELD_LINE = re.compile(r"^([a-z][a-z0-9\-]*):\s?(.*)$")
RE_LEVEL_HEAD = re.compile(r"^### Уровень:\s*([a-zA-Z0-9\-]+)\s*$", re.M)

GENERATED_BANNER = (
    "<!-- 🤖 СОБРАН ГЕНЕРАТОРОМ `tools/plany.py` ИЗ `punkty.md`. РУКАМИ НЕ ПРАВИТЬ: "
    "правка будет стёрта следующим прогоном. Хочешь другое содержание — правь "
    "`plan/src/punkty.md` и пересобери. -->"
)


class PunktyError(Exception):
    pass


def _parse_fields(block_text):
    """Turn the field lines of one block into an ordered dict, honouring the
    "unrecognised line continues the previous field" convention documented above."""
    fields = {}
    order = []
    current = None
    for line in block_text.split("\n"):
        if not line.strip():
            continue
        if line.startswith("###") or RE_ANY_ANCHOR.match(line):
            continue
        m = RE_FIELD_LINE.match(line)
        if m and m.group(1) in ITEM_FIELDS:
            key, val = m.group(1), m.group(2).strip()
            fields[key] = val
            order.append(key)
            current = key
        elif current is not None:
            fields[current] = (fields[current] + "\n" + line.strip()).strip()
        # else: stray line before any known field — ignored (defensive, not expected)
    for k in ITEM_FIELDS:
        fields.setdefault(k, "")
    return fields


def parse_punkty(text=None):
    """Return (items: dict[id -> fields], order: list[id], levels: dict[name -> {obobshchenie,svod}])."""
    if text is None:
        text = PUNKTY.read_text(encoding="utf-8")

    # --- level blocks, between "## Уровни" and "## Пункты" ---
    levels = {name: {"obobshchenie": "", "svod": ""} for name in LEVELS}
    m_lvl_section = re.search(r"^## Уровни\s*$(.*?)^## Пункты\s*$", text, re.M | re.S)
    if m_lvl_section:
        lvl_text = m_lvl_section.group(1)
        heads = list(RE_LEVEL_HEAD.finditer(lvl_text))
        for i, hm in enumerate(heads):
            name = hm.group(1)
            start = hm.end()
            end = heads[i + 1].start() if i + 1 < len(heads) else len(lvl_text)
            body = lvl_text[start:end]
            f = _parse_fields(body)
            if name in levels:
                levels[name] = {"obobshchenie": f.get("obobshchenie", ""), "svod": f.get("svod", "")}

    # --- items, after "## Пункты" ---
    m_items_section = re.search(r"^## Пункты\s*$(.*)\Z", text, re.M | re.S)
    items_text = m_items_section.group(1) if m_items_section else text

    starts = list(RE_ITEM_START.finditer(items_text))
    items = {}
    order = []
    for i, sm in enumerate(starts):
        item_id = sm.group(1)
        block_start = sm.end()
        # block ends at the next ANY anchor (item or `finish`) or EOF
        next_anchor = RE_ANY_ANCHOR.search(items_text, block_start)
        block_end = next_anchor.start() if next_anchor else len(items_text)
        block = items_text[block_start:block_end]
        fields = _parse_fields(block)
        if fields.get("id") != item_id:
            raise PunktyError(f"{item_id}: поле id ({fields.get('id')!r}) не совпадает с якорем")
        items[item_id] = fields
        order.append(item_id)

    if not order:
        raise PunktyError("в punkty.md не найдено ни одного пункта `<!--id: p-NN-->`")

    return items, order, levels


# --------------------------------------------------------------------------- gates

def kalendar_slots():
    """{'1': 6, '2': 8, '3': 9, '4': 10} — read from kalendar_goda.py, never retyped."""
    wd = kalendar_goda.PERVOE_ZANYATIE.weekday()
    rimskoe = {"I": "1", "II": "2", "III": "3", "IV": "4"}
    return {rimskoe[name]: n for name, n in kalendar_goda.schitat(wd)}


def proverit(items, order, napolnennye):
    """Return list of failure strings (empty list = clean)."""
    fail = []
    ids_ok_target = set(order) | {"finish"}

    # 1: opiraetsya missing, except first item
    for i, iid in enumerate(order):
        if i == 0:
            continue
        if not items[iid]["opiraetsya"].strip():
            fail.append(f"без opiraetsya (не первый пункт): {iid}")

    # 2: dangling ids in opiraetsya / obobshchaetsya-v
    for iid in order:
        for field in ("opiraetsya", "obobshchaetsya-v"):
            val = items[iid][field].strip()
            if not val:
                continue
            for ref in re.split(r"[,\s]+", val):
                ref = ref.strip()
                if ref and ref not in ids_ok_target:
                    fail.append(f"висячий id в {field} пункта {iid}: {ref!r}")

    # 3: obobshchaetsya-v missing
    for iid in order:
        if not items[iid]["obobshchaetsya-v"].strip():
            fail.append(f"без obobshchaetsya-v (пункт без обобщения не входит в курс): {iid}")

    # 4: items per quarter vs kalendar_goda.py
    slots = kalendar_slots()
    counts = {}
    for iid in order:
        q = items[iid]["chetvert"].strip()
        counts[q] = counts.get(q, 0) + 1
    for q, expected in slots.items():
        got = counts.get(q, 0)
        if got != expected:
            fail.append(f"четверть {q}: пунктов {got}, занятий по календарю {expected}")
    for q in counts:
        if q not in slots:
            fail.append(f"четверть {q!r} не существует в календаре")

    # 5: ⭐ fields empty in a FILLED quarter
    if napolnennye != "none":
        wanted = {q.strip() for q in napolnennye.split(",") if q.strip()}
        for iid in order:
            if items[iid]["chetvert"].strip() not in wanted:
                continue
            for f in STAR_FIELDS:
                if not items[iid][f].strip():
                    fail.append(f"⭐ пусто: {iid}.{f}")

    # 6: hand edit — generated view differs from what we'd write now (skip if missing)
    views = build_views(items, order)
    for relpath, content in views:
        path = SRC_DIR / relpath
        if path.exists():
            on_disk = path.read_text(encoding="utf-8")
            if on_disk != content:
                fail.append(f"вид разошёлся с генератором (правка руками?): {relpath}")

    return fail


# --------------------------------------------------------------------------- views

def _star_or_blank(items, iid, field):
    return items[iid][field].strip()


def _yaml_header(opisanie):
    return f"---\nopisanie: {opisanie}\n---\n"


def _level_open(levels, name, fallback_title):
    lvl = levels.get(name, {"obobshchenie": "", "svod": ""})
    lines = [f"# {fallback_title}", ""]
    lines.append(f"**Обобщение:** {lvl['obobshchenie'] or '_(ещё не написано)_'}")
    lines.append("")
    if lvl["svod"]:
        lines.append(lvl["svod"])
        lines.append("")
    return lines


def view_god(items, order, levels):
    lines = [GENERATED_BANNER, ""]
    lines += _level_open(levels, "god", "Год — «Пути и волны»")
    for iid in order:
        n = iid.split("-")[1]
        imya = _star_or_blank(items, iid, "imya") or "_(без названия)_"
        vopros = _star_or_blank(items, iid, "vopros")
        lines.append(f"<!--id: god-{iid}-->")
        line = f"**{iid}.** {imya}"
        if vopros:
            line += f" — {vopros}"
        line += f" [[{iid}]]"
        lines.append(line)
        lines.append("")
    text = _yaml_header(
        "год курса «Пути и волны» — вид, порождённый tools/plany.py из punkty.md: "
        "каждый пункт одной строкой (imya + vopros)"
    ) + "\n" + "\n".join(lines)
    return text


def view_chast_do_analiza(items, order, levels):
    lines = [GENERATED_BANNER, ""]
    lines += _level_open(levels, "chast-do-analiza", "Часть «до анализа»")
    for iid in order:
        if items[iid]["chast"].strip() != "do-analiza":
            continue
        teorema = _star_or_blank(items, iid, "teorema")
        lines.append(f"<!--id: chast-{iid}-->")
        lines.append(f"### {iid}")
        lines.append(f"teorema: {teorema}" if teorema else "teorema: _(ещё не написано)_")
        lines.append(f"[[god-{iid}]]")
        lines.append("")
    text = _yaml_header(
        "часть «до анализа» курса «Пути и волны» — вид, порождённый tools/plany.py из "
        "punkty.md: пункты с chast=do-analiza, поле teorema"
    ) + "\n" + "\n".join(lines)
    return text


def view_chetvert(items, order, levels, n):
    lines = [GENERATED_BANNER, ""]
    lines += _level_open(levels, f"chetvert-{n}", f"Четверть {n}")
    for iid in order:
        if items[iid]["chetvert"].strip() != str(n):
            continue
        lines.append(f"<!--id: chetvert-{iid}-->")
        lines.append(f"### {iid}")
        for f in STAR_FIELDS:
            v = _star_or_blank(items, iid, f)
            lines.append(f"{f}: {v}" if v else f"{f}:")
        iz = items[iid]["iz-karkasa"].strip()
        if iz:
            lines.append(f"_источник каркаса:_ {iz}")
        chast = items[iid]["chast"].strip()
        if chast == "analiz":
            lines.append(f"[[god-{iid}]]")
        else:
            lines.append(f"[[chast-{iid}]]")
        lines.append("")
    text = _yaml_header(
        f"четверть {n} курса «Пути и волны» — вид, порождённый tools/plany.py из "
        "punkty.md: все четыре ⭐-поля целиком"
    ) + "\n" + "\n".join(lines)
    return text


def view_lekciya_1(items, order, levels):
    iid = "p-01"
    lines = [GENERATED_BANNER, "", f"# Лекция 1 — {iid}", ""]
    raskadrovka = items[iid]["raskadrovka"].strip()
    lines.append(f"<!--id: lekciya-{iid}-->")
    lines.append(f"### {iid}")
    if raskadrovka:
        for beat in raskadrovka.split("\n"):
            lines.append(f"- {beat}")
    else:
        lines.append("_(раскадровка ещё не написана — см. `punkty.md`, поле `raskadrovka` пункта p-01)_")
    lines.append(f"[[chetvert-{iid}]]")
    lines.append("")
    text = _yaml_header(
        "лекция 1 курса «Пути и волны» — вид, порождённый tools/plany.py из punkty.md: "
        "пункт p-01 развёрнутый из его raskadrovka"
    ) + "\n" + "\n".join(lines)
    return text


def build_views(items, order):
    """Return [(relative_path, content), ...] — 7 entries, deterministic given punkty.md."""
    _, _, levels = parse_punkty()  # re-read levels fresh (cheap; keeps this fn pure in `items`/`order`)
    out = [
        ("god.md", view_god(items, order, levels)),
        ("chast-1-do-analiza.md", view_chast_do_analiza(items, order, levels)),
    ]
    for n in (1, 2, 3, 4):
        out.append((f"chetvert-{n}.md", view_chetvert(items, order, levels, n)))
    out.append(("lekciya-1.md", view_lekciya_1(items, order, levels)))
    return out


# --------------------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--proverit", action="store_true")
    ap.add_argument("--napolnennye", default="1")
    args = ap.parse_args(argv)

    try:
        items, order, levels = parse_punkty()
    except PunktyError as e:
        print(f"ошибка разбора punkty.md: {e}")
        return 1

    if args.proverit:
        fail = proverit(items, order, args.napolnennye)
        if fail:
            print(f"❌ {len(fail)} нарушени{'е' if len(fail) == 1 else 'й' if len(fail) >= 5 else 'я'}:")
            for line in fail:
                print(f"  - {line}")
            return 1
        print("✅ punkty.md чист")
        return 0

    SRC_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for relpath, content in build_views(items, order):
        path = SRC_DIR / relpath
        path.write_text(content, encoding="utf-8")
        written.append(path)
    for p in written:
        print(f"wrote {p.relative_to(KPV_DIR.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
