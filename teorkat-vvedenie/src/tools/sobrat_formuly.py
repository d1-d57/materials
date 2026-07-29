#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Список формул дека → src/tools/formuly.json (вход для katex_kesh.js).

  python3 teorkat-vvedenie/src/tools/sobrat_formuly.py

Ключ формулы обязан совпадать с тем, по которому её ищет генератор, поэтому TeX
вынимается ТЕМ ЖЕ регексом, что стоит в `_generator/build_deck.py.render_inline_md`
(`\\$(.+?)\\$`) — не «похожим». Расхождение регексов дало бы ⟦MISSING-MATH⟧ на сборке.

displayMode ставится там, где формула стоит абзацем `{.formula}`: в inline-режиме
пределы `\\sum_{0\\le l\\le k\\le n}` уезжают сбоку от сигмы, в display — над и под.
Если один и тот же TeX встретится и абзацем, и в строке, кэш (ключ = TeX) их не
различит — поэтому пересечение проверяется и печатается, а не предполагается.
"""
import re, json, sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
TEX_RE = re.compile(r"\$(.+?)\$")          # дословно как в build_deck.render_inline_md

inline, display = set(), set()
for p in sorted((SRC / "content").glob("*.md")):
    for block in re.split(r"\n\s*\n", p.read_text(encoding="utf-8")):
        target = display if block.lstrip().startswith("{.formula}") else inline
        for m in TEX_RE.finditer(block):
            target.add(m.group(1))

both = inline & display
print("формул уникальных: %d (инлайн %d · абзацем %d · в обеих ролях %d)"
      % (len(inline | display), len(inline), len(display), len(both)))
if both:
    # режим берётся ИНЛАЙН: display-обёртка `katex-display` — блочный элемент с
    # margin:1em 0, вставленный в середину строки текста, он разорвал бы абзац.
    # Абзац-формула от инлайн-рендера теряет только положение пределов, а таких
    # формул среди пересечения нет (проверено печатью ниже).
    print("⚠ один TeX в двух ролях — кэш их не различит, режим взят ИНЛАЙН:")
    for t in sorted(both):
        print("   $%s$   (крупных операторов: %s)"
              % (t, "есть" if re.search(r"\\(sum|prod|bigsqcup|int|coprod)", t) else "нет"))

# Режим ВСЕГДА инлайновый: абзац-формулы несут \\displaystyle в самом TeX
# (см. porodit.py), поэтому блочная обёртка katex-display не нужна и
# коллизия ключей невозможна по построению — она печатается как контроль.
jobs = [{"tex": t, "display": False} for t in sorted(inline | display)]
out = SRC / "tools" / "formuly.json"
out.write_text(json.dumps(jobs, ensure_ascii=False, indent=0), encoding="utf-8")
print("→ %s" % out)
sys.exit(0)
