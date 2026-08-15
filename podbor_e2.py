#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Перебор Э2: боковые и нижнее поля .zone.copy (сейчас 52px/46px, "честная
нейтраль" после снятия обхода Э1). pad_top/zag_mb уже заперты Э1 (4px/4px).
НЕ часть зоны, не коммитится — рабочий инструмент §2 файла-захода.

  python3 podbor_e2.py
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
LOG_MD = ROOT / "_studio" / "zhurnal" / "2026-08-10_dizajn-i-metriki" / "polya-i-uzor" / "podbor-e2.md"

ANCHOR_PAD = "padding:4px 52px 46px 52px"

# (pad_side, pad_bottom) — pad_top=4/zag_mb=4 заперты Э1, не трогаются здесь.
GRID = [(52, 46), (40, 32), (32, 24), (24, 16), (18, 12)]  # первый — контроль (=после Э1)


def set_values(pad_side, pad_bottom):
    src = ORIG_TIPY
    n1 = src.count(ANCHOR_PAD)
    if n1 != 1:
        raise SystemExit("якорь ANCHOR_PAD совпадений: %d (ожидался 1)" % n1)
    src = src.replace(ANCHOR_PAD, "padding:4px %dpx %dpx %dpx" % (pad_side, pad_bottom, pad_side))
    TIPY.write_text(src, encoding="utf-8")


def run(cmd, tolerate_unfit=False):
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    if r.returncode != 0:
        if tolerate_unfit and "ни одна проба не влезла" in r.stdout:
            print("  ⚠ deck.py rc=1 (карточка(и) не влезли ни в одну пробу) — измеряем как есть")
            return r.stdout
        print(r.stdout[-3000:])
        print(r.stderr[-3000:])
        raise SystemExit("команда упала rc=%d: %s" % (r.returncode, " ".join(cmd)))
    return r.stdout


def main():
    for pad_side, pad_bottom in GRID:
        set_values(pad_side, pad_bottom)
        tag = "e2-ps%d-pb%d" % (pad_side, pad_bottom)
        print("=== кандидат pad_side=%d pad_bottom=%d (tag=%s) ===" % (pad_side, pad_bottom, tag), flush=True)
        run([sys.executable, "_generator/sborka/deck.py", "teorkat-vvedenie/L2",
             "-o", "teorkat-vvedenie/L2/dist/index.html", "--zanovo"], tolerate_unfit=True)
        out = run([sys.executable, "progon.py", "--tag", tag])
        print(out, flush=True)

    all_rows = {}
    with PROGON_LOG.open(encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            tag = d.get("tag", "")
            if tag.startswith("e2-ps") and "pereliv_h_px" in d:
                all_rows.setdefault(tag, []).append(d)
    all_results = []
    for tag, rows in all_rows.items():
        ps, pb = tag[5:].split("-pb")
        pereliv = [r for r in rows if r["pereliv_h_px"] > 0.5]
        svobodnye = [r for r in pereliv if not r["verstka_reshena"]]
        zapertye = [r for r in pereliv if r["verstka_reshena"]]
        kegli = [r["cena_kegl_pct"] for r in rows]
        all_results.append({
            "pad_side": int(ps), "pad_bottom": int(pb), "tag": tag,
            "n_svob": len(svobodnye), "n_zapert": len(zapertye),
            "px_svob": round(sum(r["pereliv_h_px"] for r in svobodnye), 1),
            "kegl_avg_pct": round(sum(kegli) / len(kegli), 2) if kegli else None,
            "kegl_worst_pct": round(max(kegli), 2) if kegli else None,
            "svob_slaidy": [r["sid"] for r in svobodnye],
        })
    all_results.sort(key=lambda r: (-r["pad_side"], -r["pad_bottom"]))

    lines = ["# Перебор Э2 — боковые и нижнее поля .zone.copy (pad_top=4/zag_mb=4 заперты Э1)",
             "", "Метод: `deck.py --zanovo` + `progon.py`, тот же браузерный замер.",
             "", "| pad_side | pad_bottom | переполнено (своб/заперт) | px_svob | кегль ср% | кегль худш% | свободные слайды |",
             "|---|---|---|---|---|---|---|"]
    for r in all_results:
        lines.append("| %d | %d | (%d/%d) | %.1f | %.2f | %.2f | %s |" % (
            r["pad_side"], r["pad_bottom"], r["n_svob"], r["n_zapert"],
            r["px_svob"], r["kegl_avg_pct"] or 0, r["kegl_worst_pct"] or 0,
            ", ".join(r["svob_slaidy"]) or "—"))
    best = min(all_results, key=lambda r: (r["n_svob"], r["px_svob"], r["kegl_avg_pct"] or 999))
    lines += ["", "**ЛУЧШИЙ:** pad_side=%d pad_bottom=%d" % (best["pad_side"], best["pad_bottom"])]
    LOG_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("таблица → %s" % LOG_MD)
    print("ЛУЧШИЙ: pad_side=%d pad_bottom=%d -> %r" % (best["pad_side"], best["pad_bottom"], best))
    set_values(best["pad_side"], best["pad_bottom"])
    print("tipy.py оставлен на лучшей комбинации")


if __name__ == "__main__":
    main()
