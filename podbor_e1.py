#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Перебор Э1: верхнее поле .zone.copy (сейчас 46px) и margin-bottom .zagolovok
(сейчас 28px). НЕ часть зоны, не коммитится — рабочий инструмент §2 файла-захода.

Правит tipy.py ЯКОРНОЙ заменой (abort при ≠1 совпадении), гоняет deck.py
--zanovo и progon.py КАЖДЫЙ КАК ОТДЕЛЬНЫЙ ПРОЦЕСС (не in-process импорт: tipy
кэшируется в slaid.py на момент импорта, правка на диске между итерациями
внутри одного процесса молча не подхватилась бы). Пишет таблицу в podbor-e1.md.

  python3 podbor_e1.py
"""
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TIPY = ROOT / "_generator" / "sborka" / "tipy.py"
ORIG_TIPY = TIPY.read_text(encoding="utf-8")
PROGON_LOG = ROOT / "_studio" / "zhurnal" / "2026-08-10_dizajn-i-metriki" / "polya-i-uzor" / "progon.log"
LOG_MD = ROOT / "_studio" / "zhurnal" / "2026-08-10_dizajn-i-metriki" / "polya-i-uzor" / "podbor-e1.md"

ANCHOR_PAD = "padding:46px 52px 46px 52px"
ANCHOR_MB = "margin-bottom:28px"

# (pad_top, zag_mb) — сторона/низ пока НЕ трогаются (Э2, отдельный перебор).
# Второй раунд: первый (10/8..20/14, лог в podbor-e1.md) показал монотонный
# тренд — меньше значение, меньше переполнения И дешевле кегль; проверяем,
# держится ли тренд ниже 10/8.
GRID = [(4, 4), (6, 6), (8, 6), (10, 8)]  # 10/8 — повтор контроля из первого раунда


def set_values(pad_top, zag_mb):
    src = ORIG_TIPY
    n1 = src.count(ANCHOR_PAD)
    if n1 != 1:
        raise SystemExit("якорь ANCHOR_PAD совпадений: %d (ожидался 1)" % n1)
    n2 = src.count(ANCHOR_MB)
    if n2 != 1:
        raise SystemExit("якорь ANCHOR_MB совпадений: %d (ожидался 1)" % n2)
    # 4-значный padding: top=pad_top(перебор), right=52(честная замена -12px
    # обхода, нейтраль), bottom=46(не тронут — своя правка Э2), left=52.
    src = src.replace(ANCHOR_PAD, "padding:%dpx 52px 46px 52px" % pad_top)  # top меняется, 52/46/52 держим
    src = src.replace(ANCHOR_MB, "margin-bottom:%dpx" % zag_mb)
    TIPY.write_text(src, encoding="utf-8")


def run(cmd, tolerate_unfit=False):
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    if r.returncode != 0:
        # deck.py возвращает rc=1, если хоть одна карточка не влезла НИ В ОДНУ
        # пробу солвера ("ни одна проба не влезла") — это информативный, а не
        # аварийный исход для перебора: карточка остаётся с прежними
        # kegl_px/liniya (солвер их не тронул), измерение всё равно валидно.
        if tolerate_unfit and "ни одна проба не влезла" in r.stdout:
            print("  ⚠ deck.py rc=1 (карточка(и) не влезли ни в одну пробу) — измеряем как есть")
            return r.stdout
        print(r.stdout[-3000:])
        print(r.stderr[-3000:])
        raise SystemExit("команда упала rc=%d: %s" % (r.returncode, " ".join(cmd)))
    return r.stdout


def main():
    results = []
    for pad_top, zag_mb in GRID:
        set_values(pad_top, zag_mb)
        tag = "e1-pt%d-mb%d" % (pad_top, zag_mb)
        print("=== кандидат pad_top=%d zag_mb=%d (tag=%s) ===" % (pad_top, zag_mb, tag), flush=True)
        run([sys.executable, "_generator/sborka/deck.py", "teorkat-vvedenie/L2",
             "-o", "teorkat-vvedenie/L2/dist/index.html", "--zanovo"], tolerate_unfit=True)
        out = run([sys.executable, "progon.py", "--tag", tag])
        print(out, flush=True)

        rows = []
        with PROGON_LOG.open(encoding="utf-8") as f:
            for line in f:
                d = json.loads(line)
                if d.get("tag") == tag and "pereliv_h_px" in d:
                    rows.append(d)
        pereliv = [r for r in rows if r["pereliv_h_px"] > 0.5]
        svobodnye = [r for r in pereliv if not r["verstka_reshena"]]
        zapertye = [r for r in pereliv if r["verstka_reshena"]]
        kegli = [r["cena_kegl_pct"] for r in rows]
        row = {
            "pad_top": pad_top, "zag_mb": zag_mb, "tag": tag,
            "n_pereliv": len(pereliv), "n_svob": len(svobodnye), "n_zapert": len(zapertye),
            "px_total": round(sum(r["pereliv_h_px"] for r in pereliv), 1),
            "px_svob": round(sum(r["pereliv_h_px"] for r in svobodnye), 1),
            "kegl_avg_pct": round(sum(kegli) / len(kegli), 2) if kegli else None,
            "kegl_worst_pct": round(max(kegli), 2) if kegli else None,
            "svob_slaidy": [r["sid"] for r in svobodnye],
            "zapert_slaidy": [(r["sid"], r["pereliv_h_px"]) for r in zapertye],
            "t": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        results.append(row)
        print("  -> переполнено %d (своб %d / заперт %d), px_svob=%.1f, кегль ср %.2f%% худш %.2f%%"
              % (row["n_pereliv"], row["n_svob"], row["n_zapert"], row["px_svob"],
                 row["kegl_avg_pct"] or 0, row["kegl_worst_pct"] or 0), flush=True)

    # Таблица собирается по ВСЕМ tag="e1-*" из progon.log (не только текущего
    # запуска) — второй раунд не должен стереть данные первого.
    all_rows = {}
    with PROGON_LOG.open(encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            tag = d.get("tag", "")
            if tag.startswith("e1-pt") and "pereliv_h_px" in d:
                all_rows.setdefault(tag, []).append(d)
    all_results = []
    for tag, rows in all_rows.items():
        pt, mb = tag[5:].split("-mb")
        pereliv = [r for r in rows if r["pereliv_h_px"] > 0.5]
        svobodnye = [r for r in pereliv if not r["verstka_reshena"]]
        zapertye = [r for r in pereliv if r["verstka_reshena"]]
        kegli = [r["cena_kegl_pct"] for r in rows]
        all_results.append({
            "pad_top": int(pt), "zag_mb": int(mb), "tag": tag,
            "n_pereliv": len(pereliv), "n_svob": len(svobodnye), "n_zapert": len(zapertye),
            "px_svob": round(sum(r["pereliv_h_px"] for r in svobodnye), 1),
            "kegl_avg_pct": round(sum(kegli) / len(kegli), 2) if kegli else None,
            "kegl_worst_pct": round(max(kegli), 2) if kegli else None,
            "svob_slaidy": [r["sid"] for r in svobodnye],
        })
    all_results.sort(key=lambda r: (r["pad_top"], r["zag_mb"]))

    lines = ["# Перебор Э1 — верхнее поле .zone.copy / margin-bottom .zagolovok",
             "", "Метод: `deck.py --zanovo` (полный переподбор солвера) + `progon.py`"
             " (тот же браузерный замер, что и baseline) на каждую комбинацию.",
             "", "| pad_top | zag_mb | переполнено (своб/заперт) | px_svob | кегль ср% | кегль худш% | свободные слайды |",
             "|---|---|---|---|---|---|---|"]
    for r in all_results:
        lines.append("| %d | %d | %d (%d/%d) | %.1f | %.2f | %.2f | %s |" % (
            r["pad_top"], r["zag_mb"], r["n_pereliv"], r["n_svob"], r["n_zapert"],
            r["px_svob"], r["kegl_avg_pct"] or 0, r["kegl_worst_pct"] or 0,
            ", ".join(r["svob_slaidy"]) or "—"))
    best = min(all_results, key=lambda r: (r["n_svob"], r["px_svob"], r["kegl_avg_pct"] or 999))
    lines += ["", "**ЛУЧШИЙ (цель: 1) меньше переполненных свободных, 2) меньше px, 3) меньше цена кегля):** "
              "pad_top=%d zag_mb=%d" % (best["pad_top"], best["zag_mb"])]
    LOG_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("таблица → %s" % LOG_MD)
    print("ЛУЧШИЙ: pad_top=%d zag_mb=%d -> %r" % (best["pad_top"], best["zag_mb"], best))
    set_values(best["pad_top"], best["zag_mb"])
    print("tipy.py оставлен на лучшей комбинации")


if __name__ == "__main__":
    main()
