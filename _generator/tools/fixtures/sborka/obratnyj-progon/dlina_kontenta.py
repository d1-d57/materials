#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Заход dovodka-solvera, А3: распределение длины текста по ВСЕМ контентным
слайдам трёх эталонных деков — нужно ответить, `teorkat-vvedenie/s02` (954
знака, честный отказ солвера в обеих логиках) типичная длина или выброс.

Контентные id — те же 49, что даёт `korpus.slide_ids()` + `is_content_slide()`
(идентично тому, как их считает `korpus.analyze_deck()`/`corpus_stats()`, не
дублирую логику фильтра руками). Из них 9 — проверено фактом по `shablon.html`
(`grep` на `.imgL`/`.imgR`/`canvas`/`grid-area` без текстового `.copy`) — чисто
иллюстративные/интерактивные слайды (dandelin: s00/s03/s05c/s06/s10/s11/s11b;
buffon: sl-phase/sl-sim), у них НЕТ `content/<id>.md` вовсе: солверу там
нечего вмещать, длина текста не определена, а не равна нулю. База для
перцентиля — оставшиеся 40, с явной пометкой, кто выпал и почему.

  python3 _generator/tools/fixtures/sborka/obratnyj-progon/dlina_kontenta.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SBORKA = REPO / "_generator" / "sborka"
sys.path.insert(0, str(SBORKA))
import korpus  # noqa: E402

TARGET = ("teorkat-vvedenie", "s02")


def collect():
    rows = []
    for path in korpus.DECKS:
        deck = path.parent.parent.name
        html = path.read_text(encoding="utf-8")
        ids = sorted(i for i in korpus.slide_ids(html) if korpus.is_content_slide(i))
        for sid in ids:
            content_path = REPO / deck / "src" / "content" / ("%s.md" % sid)
            if content_path.is_file():
                text = content_path.read_text(encoding="utf-8").strip()
                rows.append({"deck": deck, "sid": sid, "chars": len(text), "есть_текст": True})
            else:
                rows.append({"deck": deck, "sid": sid, "chars": None, "есть_текст": False})
    return rows


def percentile_rank(values, x):
    """Доля значений <= x, в процентах (не интерполяция pct(), а обратная
    задача — нужен перцентиль ЗНАЧЕНИЯ, а не значение перцентиля)."""
    if not values:
        return None
    n_le = sum(1 for v in values if v <= x)
    return round(100.0 * n_le / len(values), 1)


def main():
    rows = collect()
    with_text = [r for r in rows if r["есть_текст"]]
    without_text = [r for r in rows if not r["есть_текст"]]
    chars = [r["chars"] for r in with_text]

    stat = korpus.summarize(chars)
    target_row = next((r for r in with_text if (r["deck"], r["sid"]) == TARGET), None)
    rank = percentile_rank(chars, target_row["chars"]) if target_row else None

    out = {
        "всего_контентных_id": len(rows),
        "без_текста": [{"deck": r["deck"], "sid": r["sid"]} for r in without_text],
        "n_с_текстом": len(with_text),
        "длина_знаков": stat,
        "цель": {"deck": TARGET[0], "sid": TARGET[1],
                 "chars": target_row["chars"] if target_row else None,
                 "перцентиль": rank},
        "строки": sorted(rows, key=lambda r: (r["chars"] is None, r["chars"] or 0)),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    print("\n--- сводка (А3 захода dovodka-solvera) ---", file=sys.stderr)
    print("контентных id всего: %d, без текста: %d, база для перцентиля n=%d"
          % (len(rows), len(without_text), len(with_text)), file=sys.stderr)
    if stat:
        print("длина_знаков  p5=%s  медиана=%s  p95=%s" % (stat["p5"], stat["median"], stat["p95"]),
              file=sys.stderr)
    if target_row:
        print("%s/%s: %d знаков, перцентиль %s%% (%s p95)"
              % (TARGET[0], TARGET[1], target_row["chars"], rank,
                 "ВЫШЕ" if stat and target_row["chars"] > stat["p95"] else "НЕ выше"),
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
