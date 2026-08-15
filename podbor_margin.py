#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Перебор Э0.3/Э0.5 (T_BODY_MARGIN_TOP_PX / T_BODY_MARGIN_SIDE_PX) для захода
vid-blokov-vnedrenie. НЕ часть зоны, не коммитится — рабочий инструмент.
Правит константы в smeta.py и .blk:first-of-type/.blk{margin} в base.css ПО
МЕСТУ, гоняет progon.py, пишет таблицу в podbor-margin.md, В КОНЦЕ
восстанавливает файлы к значению-победителю (не к тому, что было ДО перебора)."""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SMETA = ROOT / "_generator" / "sborka" / "smeta.py"
CSS = ROOT / "_generator" / "skeleton" / "base.css"

TOP_VALUES = [18.0, 22.0, 26.0, 30.0, 34.0]
SIDE_VALUES = [6.0, 12.0, 18.0, 24.0]


def set_values(top, side):
    s = SMETA.read_text(encoding="utf-8")
    s = re.sub(r"T_BODY_MARGIN_TOP_PX = [\d.]+",
               "T_BODY_MARGIN_TOP_PX = %.1f" % top, s)
    s = re.sub(r"T_BODY_MARGIN_SIDE_PX = [\d.]+",
               "T_BODY_MARGIN_SIDE_PX = %.1f" % side, s)
    SMETA.write_text(s, encoding="utf-8")

    c = CSS.read_text(encoding="utf-8")
    c = re.sub(r"\.blk:first-of-type\{margin-top:-[\d.]+px\}",
               ".blk:first-of-type{margin-top:-%.0fpx}" % top, c)
    c = re.sub(r"\.blk\{margin-left:-[\d.]+px;margin-right:-[\d.]+px\}",
               ".blk{margin-left:-%.0fpx;margin-right:-%.0fpx}" % (side, side), c)
    CSS.write_text(c, encoding="utf-8")


def run_point(top, side):
    set_values(top, side)
    r = subprocess.run([sys.executable, str(ROOT / "_generator" / "sborka" / "deck.py"),
                         "teorkat-vvedenie/L2", "-o", "teorkat-vvedenie/L2/dist/index.html",
                         "--zanovo"], cwd=str(ROOT), capture_output=True, text=True)
    # rc=1 у deck.py здесь означает «солвер не нашёл пробы хоть на одной
    # карточке (retrakt)», НЕ «сборка не удалась» — артефакт всё равно
    # пишется на диск (использует последние значения), мерить есть что.
    if "собран дек" not in (r.stdout + r.stderr):
        return {"top": top, "side": side, "sborka_rc": r.returncode, "stderr": r.stderr[-300:]}
    p = subprocess.run([sys.executable, str(ROOT / "progon.py"), "--tag",
                         "podbor-t%g-s%g" % (top, side)],
                        cwd=str(ROOT), capture_output=True, text=True)
    out = p.stdout
    m_n = re.search(r"(\d+) переполнено, суммарно ([\d.]+) px", out)
    m_c = re.search(r"средняя ([\d.]+)%, худшая ([\d.]+)%", out)
    return {
        "top": top, "side": side,
        "n_pereliv": int(m_n.group(1)) if m_n else None,
        "px_pereliv": float(m_n.group(2)) if m_n else None,
        "cena_sr": float(m_c.group(1)) if m_c else None,
        "cena_hud": float(m_c.group(2)) if m_c else None,
    }


def main():
    rows = []
    for top in TOP_VALUES:
        rows.append(run_point(top, 12.0))
    best_top = min([r for r in rows if r.get("n_pereliv") is not None],
                    key=lambda r: (r["n_pereliv"], r["px_pereliv"]))["top"]

    rows2 = []
    for side in SIDE_VALUES:
        rows2.append(run_point(best_top, side))
    best = min([r for r in rows2 if r.get("n_pereliv") is not None],
                key=lambda r: (r["n_pereliv"], r["px_pereliv"], r["cena_sr"]))

    lines = ["# Перебор T_BODY_MARGIN_TOP_PX / T_BODY_MARGIN_SIDE_PX (Э0.3/Э0.5)\n",
             "## Шаг 1 — верх (SIDE=12 фикс)\n",
             "| top | переполнено | суммарно px | цена ср % | цена худш % |",
             "|---|---|---|---|---|"]
    for r in rows:
        lines.append("| %g | %s | %s | %s | %s |" % (
            r["top"], r.get("n_pereliv"), r.get("px_pereliv"), r.get("cena_sr"), r.get("cena_hud")))
    lines.append("\n**Выбран top=%g** (минимум переполнений, затем минимум суммы px).\n" % best_top)
    lines.append("## Шаг 2 — бок (top=%g фикс)\n" % best_top)
    lines.append("| side | переполнено | суммарно px | цена ср % | цена худш % |")
    lines.append("|---|---|---|---|---|")
    for r in rows2:
        lines.append("| %g | %s | %s | %s | %s |" % (
            r["side"], r.get("n_pereliv"), r.get("px_pereliv"), r.get("cena_sr"), r.get("cena_hud")))
    lines.append("\n**Выбрано: top=%g, side=%g** (минимум переполнений → минимум px → минимум цены кегля)."
                 % (best["top"], best["side"]))

    (ROOT / "podbor-margin.md").write_text("\n".join(lines), encoding="utf-8")
    set_values(best["top"], best["side"])
    print("ПОБЕДИТЕЛЬ: top=%g side=%g" % (best["top"], best["side"]))
    print("таблица → podbor-margin.md, значения записаны в smeta.py/base.css")


if __name__ == "__main__":
    main()
