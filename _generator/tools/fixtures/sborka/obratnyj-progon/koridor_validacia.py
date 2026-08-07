#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Заход dovodka-solvera, критерий Б.2: коридор `koridor_obyoma.py` прогнан
на 10 живых слайдах трёх деков — вход (axis/liniya/состав блоков) взят из
`content/<sid>.md` СТРУКТУРОЙ (число абзацев/списков, деление по пустой
строке — тот же разбор, что `render_md` в `build_deck.py`, Я-соседний файл,
не переписан, только ПОВТОРЁН минимально для подсчёта — читать текст самих
абзацев не нужно, только считать их и отличать список от абзаца), фактическая
длина текста сверяется ОТДЕЛЬНО, уже ПОСЛЕ того как коридор посчитан —
критерий 3 захода («коридор без знания текста слайда») не нарушен: на вход
солверу текст не попадает НИКОГДА.

  python3 koridor_validacia.py
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SBORKA = REPO / "_generator" / "sborka"
sys.path.insert(0, str(SBORKA))
import korpus  # noqa: E402
import vmeshchenie  # noqa: E402
from koridor_obyoma import find_max, find_min, izmerit_dyhanie_normy, norma_tipografiki  # noqa: E402
from postroit_kartochku import find_grid_axis_liniya  # noqa: E402

# 10 слайдов из БАЗЫ 16 (А1/А2), где ось+liniya уже известны фактом (`korpus.
# analyze_deck`) — не подобраны заново под критерий, тот же исторический список.
SLIDES_10 = [
    ("teorkat-vvedenie", "s01"), ("teorkat-vvedenie", "s05"), ("teorkat-vvedenie", "s06"),
    ("teorkat-vvedenie", "s10"),
    ("dandelin", "s01"), ("dandelin", "s05"), ("dandelin", "s08"),
    ("buffon", "sl-coin"), ("buffon", "sl-condition"), ("buffon", "sl-plan"),
]


def sostav_iz_soderzhimogo(deck, sid):
    """Состав блоков БЕЗ чтения смысла текста — та же разбивка по пустой
    строке, что `render_md` (Я-сосед, `build_deck.py`), но здесь считаются
    ТОЛЬКО количество и тип (`p`/`ulK`), содержимое строк не используется
    нигде дальше по цепочке (критерий 3)."""
    path = REPO / deck / "src" / "content" / ("%s.md" % sid)
    text = path.read_text(encoding="utf-8")
    units = []
    for block in re.split(r"\n\s*\n", text.strip("\n")):
        lines = [ln.strip() for ln in block.split("\n") if ln.strip()]
        if not lines:
            continue
        body = lines
        m = re.match(r"^\{\.([\w-]+)\}$", lines[0])
        if m and len(lines) > 1 and all(l.startswith("- ") for l in lines[1:]):
            body = lines[1:]
        if all(l.startswith("- ") for l in body):
            units.append(("ul", len(body)))
        else:
            units.append(("p", 1))
    return units, len(text.strip())


def units_to_sostav_str(units):
    return ",".join(("p" if k == "p" else "ul%d" % n) for k, n in units)


def main():
    corpus = korpus.corpus_stats()
    norma = norma_tipografiki(corpus)
    rows = []

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        page = b.new_page(viewport={"width": 1440, "height": 810}, device_scale_factor=1)
        out_root = HERE
        for deck, sid in SLIDES_10:
            units, chars_real = sostav_iz_soderzhimogo(deck, sid)
            try:
                axis, liniya, istochnik_liniya = find_grid_axis_liniya(deck, sid)
            except SystemExit as e:
                rows.append({"deck": deck, "sid": sid, "пропущен": str(e)})
                continue
            dyhanie_norm = izmerit_dyhanie_normy(page, units, axis, liniya, norma, out_root)
            if dyhanie_norm is not None and dyhanie_norm < vmeshchenie.DYHANIE_P25:
                rows.append({"deck": deck, "sid": sid, "chars_real": chars_real, "axis": axis,
                             "liniya": round(liniya, 2), "sostav": units_to_sostav_str(units),
                             "коридор": None, "причина": "дыхание нормы ниже p25 (%.3f)" % dyhanie_norm})
                continue
            n_max = find_max(page, units, axis, liniya, norma, out_root)
            if n_max is None:
                rows.append({"deck": deck, "sid": sid, "chars_real": chars_real, "axis": axis,
                             "liniya": round(liniya, 2), "sostav": units_to_sostav_str(units),
                             "коридор": None, "причина": "даже минимум (20 знаков) переполняет"})
                continue
            n_min = find_min(page, units, axis, liniya, norma, out_root,
                              fill_lo=vmeshchenie.FILL_LO, n_max=n_max)
            popal = n_min <= chars_real <= n_max
            rows.append({"deck": deck, "sid": sid, "axis": axis, "liniya": round(liniya, 2),
                         "sostav": units_to_sostav_str(units), "chars_real": chars_real,
                         "min_znakov": n_min, "max_znakov": n_max, "попал": popal})
        b.close()

    hits = sum(1 for r in rows if r.get("попал") is True)
    considered = sum(1 for r in rows if "попал" in r)
    print(json.dumps({"строки": rows, "попало": hits, "из": considered}, ensure_ascii=False, indent=2))
    print("\n--- сводка (критерий Б.2) ---", file=sys.stderr)
    print("попало %d из %d (порог криterия — не меньше 7 из 10)" % (hits, considered), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
