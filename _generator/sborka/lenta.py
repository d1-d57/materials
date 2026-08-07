#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Лента лекции — ОДИН HTML, три вкладки, собран из карточек (Э7 захода
kartochka-i-sborka; конструкция — Я2 §4.3): «владелец смотрит лекцию только
целиком; без этого источник истины ему невидим».

  python3 _generator/sborka/lenta.py <лекция> -o <лекция>/dist/lenta.html

Три вкладки — представления ОДНОГО и того же материала, не источники (Я2 §4.3):
  1. «Вся математика» — раздел «Математика — развёрнуто» всех карточек ПОДРЯД,
     без разбивки по слайдам (свободный текст, как раньше нёс MATEMATIKA.md).
  2. «По слайдам» — тот же раздел, но с заголовком-разделителем на каждый слайд.
  3. «Сжато (финал)» — раздел «Текст слайда — сжато» по слайдам — то, что
     реально попадёт на экран.

Только слайды `status: v_deke` (резерв — не часть лекции, симметрично `deck.py`).
Переключение вкладок — CSS radio-инпуты, 0 внешних URL (канон генератора).
"""
import argparse
import html as _html
import sys
from pathlib import Path

SBORKA = Path(__file__).resolve().parent
GENERATOR = SBORKA.parent
sys.path.insert(0, str(SBORKA))
sys.path.insert(0, str(GENERATOR))
from formaty import parse_card, parse_front_matter, render_body  # noqa: E402
import bloki  # noqa: E402
from build_deck import parse_brief, read_text  # noqa: E402  (READ-ONLY импорт, Я6)


def _load_slides(lekcija_dir):
    """Папка лекции → [(sid, params, sections|None)], порядок brief.md
    slide_order, ТОЛЬКО status v_deke. sections=None — тело пусто (K3)."""
    brief = lekcija_dir / "brief.md"
    meta = parse_brief(read_text(brief)) if brief.is_file() else {}
    lekcija_params, _ = parse_front_matter(read_text(brief), sid="brief.md") if brief.is_file() else ({}, "")

    slajdy_dir = lekcija_dir / "slajdy"
    have = {p.parent.name: p for p in slajdy_dir.glob("*/slaid.md")}
    order = meta.get("slide_order") or sorted(have)

    out = []
    for sid in order:
        p = have.get(sid)
        if p is None:
            continue
        text = read_text(p)
        params, raw_body = parse_card(text, sid=sid)
        if params.get("status", "v_deke") == "rezerv":
            continue
        sections = bloki.parse_sections(raw_body, sid=sid) if raw_body.strip() else None
        out.append((sid, params, sections))
    return lekcija_params, out


def _blocks_html(blocks):
    if not blocks:
        return '<p class="pusto">(текста нет)</p>'
    return "\n".join(render_body(b.telo, acc_tag="span") for b in blocks if b.telo.strip())


def _vkladka_potokom(slides):
    """Вкладка 1 — вся математика подряд, без разбивки по слайдам."""
    parts = []
    for sid, params, sections in slides:
        if sections is None:
            continue
        parts.append(_blocks_html(sections["matematika"]))
    return "\n".join(parts) or '<p class="pusto">(математики нет)</p>'


def _vkladka_po_slajdam(slides, razdel):
    """Вкладка 2/3 — тот же/сжатый материал, с заголовком на каждый слайд.
    `razdel`: 'matematika' или 'tekst'."""
    parts = []
    for sid, params, sections in slides:
        title = params.get("nazvanie") or sid
        parts.append('<section class="slajd-lenty" id="ls-%s">' % _html.escape(sid))
        parts.append('<h2>%s</h2>' % _html.escape(title))
        if sections is None:
            parts.append('<p class="pusto">(текста нет — иллюстрация/пусто, K3)</p>')
        else:
            parts.append(_blocks_html(sections[razdel]))
        parts.append('</section>')
    return "\n".join(parts)


CSS = """
body{font-family:'Glacial Indifference',Arial,sans-serif;max-width:900px;margin:0 auto;padding:32px;
     background:#faf7f2;color:#242019;line-height:1.5}
h1{font-family:'Forum',serif;font-size:32px;margin-bottom:4px}
.podzagolovok{color:#7a7267;margin-bottom:24px}
.taby input{display:none}
.taby label{display:inline-block;padding:10px 20px;margin-right:6px;background:#e9e2d8;
            border-radius:8px 8px 0 0;cursor:pointer;font-weight:600}
.panel{display:none;border-top:3px solid #bf5b4f;padding-top:20px}
#t1:checked ~ .taby label[for=t1],
#t2:checked ~ .taby label[for=t2],
#t3:checked ~ .taby label[for=t3]{background:#bf5b4f;color:#fff}
#t1:checked ~ #p1,#t2:checked ~ #p2,#t3:checked ~ #p3{display:block}
h2{font-family:'Forum',serif;font-size:22px;margin:28px 0 8px;color:#bf5b4f}
.slajd-lenty:first-child h2{margin-top:0}
.pusto{color:#a39a8c;font-style:italic}
"""


def build(lekcija_dir, out):
    lekcija_dir = Path(lekcija_dir)
    lekcija_params, slides = _load_slides(lekcija_dir)
    if not slides:
        raise SystemExit("нет слайдов status:v_deke в %s" % lekcija_dir)

    title = lekcija_params.get("title") or lekcija_dir.name
    tab1 = _vkladka_potokom(slides)
    tab2 = _vkladka_po_slajdam(slides, "matematika")
    tab3 = _vkladka_po_slajdam(slides, "tekst")

    doc = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>%(title)s — лента</title>
<style>%(css)s</style>
</head>
<body>
<h1>%(title)s</h1>
<div class="podzagolovok">лента · %(n)d слайдов (status: v_deke)</div>
<input type="radio" name="tab" id="t1" checked>
<input type="radio" name="tab" id="t2">
<input type="radio" name="tab" id="t3">
<div class="taby">
<label for="t1">Вся математика</label>
<label for="t2">По слайдам</label>
<label for="t3">Сжато (финал)</label>
</div>
<div class="panel" id="p1">%(tab1)s</div>
<div class="panel" id="p2">%(tab2)s</div>
<div class="panel" id="p3">%(tab3)s</div>
</body>
</html>
""" % {
        "title": _html.escape(title),
        "css": CSS,
        "n": len(slides),
        "tab1": tab1,
        "tab2": tab2,
        "tab3": tab3,
    }

    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    return len(slides), out


def main():
    ap = argparse.ArgumentParser(description="Собирает ленту лекции (3 вкладки) из карточек слайдов")
    ap.add_argument("lekcija", help="папка <лекция> (несёт brief.md + slajdy/)")
    ap.add_argument("-o", "--out", required=True, help="путь выхода .html")
    args = ap.parse_args()
    n, out = build(args.lekcija, args.out)
    print("собрана лента: %d слайдов → %s" % (n, out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
