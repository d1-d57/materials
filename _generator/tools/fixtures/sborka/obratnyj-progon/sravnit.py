#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Заход obratnyj-progon, Э3: один слайд — карточка → солвер → строка
человек/солвер/разница. Печатает JSON, дальше в таблицу отчёта руками
(ОДИН слайд за раз — дисциплина Э3, не батч)."""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SBORKA = REPO / "_generator" / "sborka"
sys.path.insert(0, str(SBORKA))
import korpus  # noqa: E402
import vmeshchenie  # noqa: E402
from postroit_kartochku import build_card  # noqa: E402

TOKENS_DEFAULT = {"kegl": 38.0, "lh": 1.5278, "blok": 26.0}


def human_values(deck, sid):
    shablon_path = REPO / deck / "src" / "shablon.html"
    _, per_slide = korpus.analyze_deck(shablon_path)
    slot = per_slide.get(sid, {})
    out, src = {}, {}
    for k in ("kegl", "lh", "blok"):
        if k in slot:
            out[k], src[k] = slot[k], "per-slide"
        else:
            out[k], src[k] = TOKENS_DEFAULT[k], "canon-дефолт"
    return out, src


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("sid")
    args = ap.parse_args()

    card = build_card(args.deck, args.sid, HERE)
    axis = card["axis"]
    human, src = human_values(args.deck, args.sid)
    human["liniya"] = card["liniya_human_original"]
    src["liniya"] = card["istochnik_liniya"]

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        page = b.new_page(viewport={"width": 1440, "height": 810}, device_scale_factor=1)
        res = vmeshchenie.podobrat_slide(page, card["html"], axis=axis)
        b.close()

    chosen = res["chosen"]
    row = {"deck": args.deck, "sid": args.sid, "axis": axis, "chars": card["chars"]}
    if chosen is None:
        row["otkaz"] = True
        row["diag"] = res["diagnostics"]
    else:
        row["otkaz"] = False
        for k in ("kegl", "lh", "blok", "liniya"):
            hv = human[k]
            sv = chosen.get(k)
            row[k] = {"человек": round(hv, 3), "источник": src[k],
                       "солвер": round(sv, 3) if sv is not None else None,
                       "разница_солвер_минус_человек": round(sv - hv, 3) if sv is not None else None}
        row["fill"] = chosen["fill"]
        row["n_trials"] = res["n_trials"]
        row["n_fitting"] = res["n_fitting"]
    print(json.dumps(row, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
