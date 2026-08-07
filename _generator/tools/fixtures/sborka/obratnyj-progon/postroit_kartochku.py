#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Заход obratnyj-progon, Э3: минимальная временная карточка из старого слайда.

Три эталонных дека (dandelin/buffon/teorkat-vvedenie) — СТАРЫЙ формат
(`slides/<id>.html` + `content/<id>.md`, PER-SLIDE CSS в `shablon.html`), не
карточки `slaid.md`. Компилятор солвера (`slaid.py`) — карточный. Этот скрипт
строит МИНИМАЛЬНУЮ карточку из имеющегося содержимого (заход §Э3: «дать
солверу то, от чего он зависит: текст слайда, тип вёрстки, размер зоны» —
не перекладывать слайд целиком) и компилирует её через `slaid.py`, не
переписывая ни его, ни `tipy.py`/`formaty.py`.

Ось/liniya — ДВА пути, по факту живых данных (не угаданы):
1. ПЕРВЫЙ ПРИОРИТЕТ — `korpus.py.analyze_deck()`: тот же кросс-ссылочный разбор
   `.grid`↔`.board`/`.rail`, что уже даёт корпусные диапазоны солверу (Я2 захода).
   Работает для teorkat-vvedenie/buffon (их `.board` несёт `grid-area` явно).
2. ПАДЕНИЕ НА ПРОСТОЙ РЕГЭКСП по `#<sid> .grid{...}` — только когда (1) не дал
   liniya. Нужен для dandelin: там `.board`-эквиваленты называются по-разному
   (`.board-top`/`.litho`/`.sboard`/…) без `grid-area`, и кросс-ссылка korpus.py
   их не ловит, а сам `grid-template-rows/columns` — простой 2-значный %-сплит
   (проверено вручную по пяти слайдам выборки). Текст = ПЕРВЫЙ трек — подтверждено
   DOM-порядком `.copy`/`.board` в `slides/*.html` (текстовый div идёт раньше).

  python3 postroit_kartochku.py <deck> <sid> [--out-root DIR]
  печатает JSON: {html: путь к скомпилированному файлу, axis: ..., liniya: ..., istochnik: ...}
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]  # .../fixtures/sborka/obratnyj-progon -> repo root
SBORKA = REPO / "_generator" / "sborka"
sys.path.insert(0, str(SBORKA))
sys.path.insert(0, str(REPO / "_generator"))
import slaid  # noqa: E402
import korpus  # noqa: E402


def _via_korpus(deck, sid):
    shablon_path = REPO / deck / "src" / "shablon.html"
    _, per_slide = korpus.analyze_deck(shablon_path)
    slot = per_slide.get(sid, {})
    if "liniya" in slot and "axis" in slot:
        return slot["axis"], slot["liniya"]
    return None


def _via_raw_grid(deck, sid):
    shablon = (REPO / deck / "src" / "shablon.html").read_text(encoding="utf-8")
    m = re.search(r"#%s \.grid\{([^}]*)\}" % re.escape(sid), shablon)
    if not m:
        return None
    decl = m.group(1)
    rows = re.search(r"grid-template-rows\s*:\s*([\d.]+)%", decl)
    cols = re.search(r"grid-template-columns\s*:\s*([\d.]+)%", decl)
    if rows and not cols:
        return "horizontal", float(rows.group(1))
    if cols and not rows:
        return "vertical", float(cols.group(1))
    return None


def find_grid_axis_liniya(deck, sid):
    res = _via_korpus(deck, sid)
    istochnik = "korpus.py (кросс-ссылка .grid/.board)"
    if res is None:
        res = _via_raw_grid(deck, sid)
        istochnik = "сырой regex по #<sid> .grid{...} (простой 2-значный сплит)"
    if res is None:
        raise SystemExit("слайд %s/%s: ни korpus.py, ни простой regex не дали "
                          "ось+liniya — не годится для минимальной карточки" % (deck, sid))
    axis, liniya = res
    return axis, liniya, istochnik


def build_card(deck, sid, out_root):
    content_path = REPO / deck / "src" / "content" / ("%s.md" % sid)
    if not content_path.is_file():
        raise SystemExit("нет content/%s.md в %s — нечем наполнить карточку" % (sid, deck))
    text = content_path.read_text(encoding="utf-8").strip()
    axis, liniya, istochnik = find_grid_axis_liniya(deck, sid)
    tip = "polosa_gorizontalnaya" if axis == "horizontal" else "polosa_vertikalnaya"

    lekcija_dir = out_root / ("%s-%s" % (deck, sid))
    slajd_dir = lekcija_dir / "slajdy" / sid
    slajd_dir.mkdir(parents=True, exist_ok=True)

    src_math = REPO / deck / "src" / "math" / "katex.json"
    if src_math.is_file():
        dst_math = lekcija_dir / "math"
        dst_math.mkdir(parents=True, exist_ok=True)
        shutil.copy(src_math, dst_math / "katex.json")

    card = (
        "---\n"
        "imya: %s\n"
        "tip_verstki: %s\n"
        "liniya: %g\n"
        "illustracii: []\n"
        "---\n"
        "## Математика — развёрнуто\n"
        "%s\n\n"
        "## Текст слайда — сжато\n"
        "%s\n\n"
        "## Правки\n"
    ) % (sid, tip, liniya, text, text)
    (slajd_dir / "slaid.md").write_text(card, encoding="utf-8")

    out_html = lekcija_dir / "dist" / ("%s.html" % sid)
    out_html.parent.mkdir(parents=True, exist_ok=True)
    compiled_sid, doc = slaid.compile_slide_html(slajd_dir / "slaid.md", title=sid)
    out_html.write_text(doc, encoding="utf-8")
    return {"html": str(out_html), "axis": axis, "liniya_human_original": liniya,
            "chars": len(text), "istochnik_liniya": istochnik}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("sid")
    ap.add_argument("--out-root", default=str(HERE))
    args = ap.parse_args()
    res = build_card(args.deck, args.sid, Path(args.out_root))
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
