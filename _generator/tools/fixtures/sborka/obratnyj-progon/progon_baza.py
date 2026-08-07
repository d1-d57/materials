#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Заход dovodka-solvera, А1/А2/А4: batch-перепрогон солвера на выбранной базе
слайдов — та же карточка (`postroit_kartochku.build_card`), тот же солвер
(`vmeshchenie.podobrat_slide`), что и `sravnit.py` (Я4, read-only, логику
`human_values` не дублирую — импортирую), только по МНОГО слайдов за раз с
печатью Δ-таблицы и сводки, вместо одного слайда по дисциплине Э3 захода
obratnyj-progon (там дисциплина была про АРТЕФАКТ карточки на слайд, здесь —
про число на выборке, дисциплина другая).

`--baza 16` — 16 слайдов из таблицы `## ОТЧЁТ` захода `solver-v3-dyhanie`
(число дословно процитировано оттуда, не подобрано заново) — сравнимая
историческая база для А1 (до/после) и А2 (сетка веса).
`--baza 40` — ВСЕ контентные id трёх деков (`korpus.slide_ids`+
`is_content_slide`, 49 штук), у КОГО есть `content/<id>.md` (40 из 49 — см.
`dlina_kontenta.py`/`## ПЛАН`: 9 id чисто иллюстративные, текста не имеют
вовсе) — расширенная база А4.

`--dyhanie-w W` — временный monkeypatch `vmeshchenie.WEIGHTS["dyhanie"]` НА
ВРЕМЯ ЭТОГО ЗАПУСКА (не пишет в файл) — нужен только для сетки А2, `vmeshchenie.py`
не меняется этим флагом.

  python3 _generator/tools/fixtures/sborka/obratnyj-progon/progon_baza.py --baza 16
  python3 _generator/tools/fixtures/sborka/obratnyj-progon/progon_baza.py --baza 16 --dyhanie-w 1.2
  python3 _generator/tools/fixtures/sborka/obratnyj-progon/progon_baza.py --baza 40
"""
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
from sravnit import human_values  # noqa: E402

# 16 слайдов таблицы `## ОТЧЁТ` захода solver-v3-dyhanie (Я1) — процитировано
# по составу и порядку, не пересобрано заново (KONSTITUCIYA §10: набор — да
# командой, но САМ список — исторический артефакт другого захода, его номера
# строк цитируются, а не пересчитываются).
BAZA_16 = [
    ("teorkat-vvedenie", "s01"), ("teorkat-vvedenie", "s02"), ("teorkat-vvedenie", "s05"),
    ("teorkat-vvedenie", "s06"), ("teorkat-vvedenie", "s10"),
    ("dandelin", "s01"), ("dandelin", "s05"), ("dandelin", "s08"), ("dandelin", "s09"),
    ("dandelin", "s09p"),
    ("buffon", "sl-coin"), ("buffon", "sl-condition"), ("buffon", "sl-circle"),
    ("buffon", "sl-grid"), ("buffon", "sl-plan"), ("buffon", "sl-prob"),
]


def baza_40():
    out = []
    for path in korpus.DECKS:
        deck = path.parent.parent.name
        html = path.read_text(encoding="utf-8")
        ids = sorted(i for i in korpus.slide_ids(html) if korpus.is_content_slide(i))
        for sid in ids:
            if (REPO / deck / "src" / "content" / ("%s.md" % sid)).is_file():
                out.append((deck, sid))
    return out


def run(pairs, dyhanie_w=None):
    if dyhanie_w is not None:
        vmeshchenie.WEIGHTS["dyhanie"] = dyhanie_w

    corpus = korpus.corpus_stats()
    rows = []
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        page = b.new_page(viewport={"width": 1440, "height": 810}, device_scale_factor=1)
        for deck, sid in pairs:
            try:
                card = build_card(deck, sid, HERE)
            except SystemExit as e:
                # А4 захода dovodka-solvera: часть контентных слайдов — не
                # иллюстрация+текст (banner+список и т.п.), `find_grid_axis_liniya`
                # (Я3, read-only) честно не находит ось/liniya по своим двум
                # эвристикам — это граница ОХВАТА измерителя, не баг, чинить
                # не в этой зоне (postroit_kartochku.py правится ОТДЕЛЬНЫМ
                # ходом по дисциплине §3, здесь просто пропуск с меткой).
                rows.append({"deck": deck, "sid": sid, "нет_карточки": str(e)})
                continue
            axis = card["axis"]
            human, src = human_values(deck, sid)
            human["liniya"] = card["liniya_human_original"]
            res = vmeshchenie.podobrat_slide(page, card["html"], axis=axis, corpus=corpus)
            chosen = res["chosen"]
            row = {"deck": deck, "sid": sid, "chars": card["chars"], "axis": axis}
            if chosen is None:
                row["otkaz"] = True
            else:
                row["otkaz"] = False
                for k in ("kegl", "lh", "blok"):
                    hv, sv = human[k], chosen.get(k)
                    row[k] = round(sv - hv, 3) if sv is not None else None
                row["fill"] = chosen["fill"]
                row["blok_koef_solver"] = round(chosen["blok"] / chosen["kegl"], 4) if chosen.get("kegl") else None
            rows.append(row)
        b.close()
    return rows


def summarize(rows):
    # А4: "нет_карточки" — измеритель не построил карточку вовсе (не ось
    # солвера, вне вмещения) — исключается из базы решаемости отдельной
    # строкой, не путается с "отказ" (солвер карточку получил и не смог вместить).
    bez_kartochki = [r for r in rows if "нет_карточки" in r]
    solved_universe = [r for r in rows if "нет_карточки" not in r]
    ok = [r for r in solved_universe if not r["otkaz"]]
    n_otkaz = len(solved_universe) - len(ok)
    out = {"n_карточек_построено": len(solved_universe), "n_нет_карточки": len(bez_kartochki),
           "нет_карточки_список": [{"deck": r["deck"], "sid": r["sid"]} for r in bez_kartochki],
           "отказов": n_otkaz}
    for k in ("kegl", "lh", "blok"):
        vals = [r[k] for r in ok if r.get(k) is not None]
        if vals:
            out["среднее_Δ%s" % k] = round(sum(vals) / len(vals), 3)
            out["среднее_|Δ%s|" % k] = round(sum(abs(v) for v in vals) / len(vals), 3)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baza", choices=("16", "40"), required=True)
    ap.add_argument("--dyhanie-w", type=float, default=None)
    args = ap.parse_args()

    pairs = BAZA_16 if args.baza == "16" else baza_40()
    rows = run(pairs, dyhanie_w=args.dyhanie_w)
    summary = summarize(rows)

    print(json.dumps({"строки": rows, "сводка": summary}, ensure_ascii=False, indent=2))
    print("\n--- сводка (progon_baza --baza %s%s) ---"
          % (args.baza, "" if args.dyhanie_w is None else " --dyhanie-w %s" % args.dyhanie_w),
          file=sys.stderr)
    print(json.dumps(summary, ensure_ascii=False), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
