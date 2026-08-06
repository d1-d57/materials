#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сшивка разбора: текст (правится руками) + иллюстрации (считаются генератором) → doc-вид.

    python3 assemble.py            # gen_ill → инлайн SVG в tekst/*.md → build/ → build_doc → view.html

Своего md→HTML парсера тут НЕТ (правило №1 корня): HTML печёт `_generator/build_doc.py`.
Здесь только подстановка `{{ILL:имя|подпись}}` → <figure><svg…/><figcaption>…</figcaption></figure>,
чтобы текст оставался редактируемым, а геометрия — считаемой.
"""
import re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent
# `ROOT = HERE.parents[1]` снят: он существовал ТОЛЬКО чтобы собрать путь к
# `_generator`, а движки теперь зовутся по имени (`python3 -m dvizhki`, ставится
# один раз — `_generator/README.md`). Считать корень репозитория этому скрипту незачем.
TEKST, ILL, BUILD = HERE / "tekst", HERE / "ill", HERE / "build"

def main():
    subprocess.run([sys.executable, str(HERE / "gen_ill.py")], check=True)
    BUILD.mkdir(exist_ok=True)
    # чистим устаревшие потоки; в песочнице прав на unlink может не быть — не валимся
    live = {p.name for p in TEKST.glob("*.md")}
    for old in BUILD.glob("*.md"):
        if old.name not in live:
            try:
                old.unlink()
            except OSError as e:
                print("  ⚠ не смог убрать устаревший поток %s (%s) — убери руками" % (old.name, e))

    missing = []
    for src in sorted(TEKST.glob("*.md")):
        text = src.read_text(encoding="utf-8")

        def sub(m):
            name, cap = m.group(1), (m.group(2) or "").strip()
            f = ILL / (name + ".svg")
            if not f.exists():
                missing.append(name)
                return m.group(0)
            svg = f.read_text(encoding="utf-8")
            cap_html = "<figcaption>%s</figcaption>" % cap if cap else ""
            return "<figure>\n%s\n%s\n</figure>" % (svg, cap_html)

        text = re.sub(r"\{\{ILL:([\w-]+)(?:\|([^}]*))?\}\}", sub, text)
        (BUILD / src.name).write_text(text, encoding="utf-8")
        print("  сшито: %s" % src.name)

    if missing:
        print("ГЕЙТ ПРОВАЛЕН: нет иллюстраций %s" % sorted(set(missing)))
        return 1

    # `sys.executable`, а не голое `python3`: интерпретатор обязан остаться ТЕМ ЖЕ,
    # которым запущен этот скрипт, — пакет `dvizhki` стоит именно в нём.
    r = subprocess.run([sys.executable, "-m", "dvizhki", "doc", str(BUILD)])
    if r.returncode:
        return r.returncode
    print("\nГейт вида (правило №2 корня):")
    return subprocess.run([sys.executable, "-m", "dvizhki", "vid", str(BUILD)]).returncode

if __name__ == "__main__":
    sys.exit(main())
