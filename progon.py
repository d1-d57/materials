#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Прогонщик захода vid-blokov-vnedrenie. НЕ часть зоны, не коммитится —
рабочий инструмент, требуемый §2 файла-захода («ночной режим», правило 2).

  python3 progon.py [--tag <метка>]

Компилирует КАЖДУЮ карточку teorkat-vvedenie/L2 отдельно (после сборки декой,
т.е. со значениями kegl_px/mezhstrochye/otstup_bloka, уже осевшими в шапках),
меряет переполнение в px (vmeshchenie.izmerit) и цену кегля (относительно
KEGL_DEFAULT смет), дописывает строку в лог `progon.log` (JSONL, по одной
записи на слайд на прогон)."""
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "_generator" / "sborka"))
import smeta  # noqa: E402
import vmeshchenie  # noqa: E402
from slaid import compile_slide_html  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

LEK = ROOT / "teorkat-vvedenie" / "L2"
LOG = ROOT / "progon.log"


def main():
    tag = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--tag" else "run"
    slides = sorted((LEK / "slajdy").glob("*/slaid.md"))
    rows = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="chrome", headless=True)
        page = b.new_page(viewport={"width": 1440, "height": 810}, device_scale_factor=1)
        tmp = ROOT / "_progon_tmp.html"
        for md in slides:
            sid = md.parent.name
            try:
                s = smeta.smeta_slajda(md)
            except (ValueError, smeta.NeBerus) as e:
                rows.append({"sid": sid, "tag": tag, "propushcheno": str(e)})
                continue
            _, html = compile_slide_html(md)
            tmp.write_text(html, encoding="utf-8")
            r = vmeshchenie.izmerit(page, tmp)
            pereliv_h = max(0.0, r["content_extent"] - r["content_h"])
            kegl = s["kegl"]
            cena_kegl = round(100.0 * (smeta.KEGL_DEFAULT - kegl) / smeta.KEGL_DEFAULT, 2)
            rows.append({
                "sid": sid, "tag": tag, "kegl": kegl, "cena_kegl_pct": cena_kegl,
                "pereliv_h_px": round(pereliv_h, 1), "pereliv_x_px": r["pereliv_x"],
                "smeta_vlezaet": s["vlezaet"], "brauzer_fits": r["fits"],
            })
        b.close()
        tmp.unlink(missing_ok=True)

    with LOG.open("a", encoding="utf-8") as f:
        for row in rows:
            row["t"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    pereliv = [r for r in rows if r.get("pereliv_h_px", 0) > 0.5]
    mereno = [r for r in rows if "pereliv_h_px" in r]
    kegli = [r["cena_kegl_pct"] for r in mereno]
    print("=== прогон %r: %d слайдов измерено, %d переполнено, суммарно %.1f px ==="
          % (tag, len(mereno), len(pereliv), sum(r["pereliv_h_px"] for r in pereliv)))
    for r in pereliv:
        print("  ❌ %-28s +%.1f px" % (r["sid"], r["pereliv_h_px"]))
    if kegli:
        print("цена кегля: средняя %.2f%%, худшая %.2f%% (%s)"
              % (sum(kegli) / len(kegli), max(kegli),
                 max(mereno, key=lambda r: r["cena_kegl_pct"])["sid"]))
    print("лог дописан → %s" % LOG)


if __name__ == "__main__":
    main()
