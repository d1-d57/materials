#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Прогонщик захода polya-i-uzor. НЕ часть зоны, не коммитится — рабочий
инструмент §2 файла-захода («ночной режим», правило 2: числа перебором,
не на глаз). Меряет переполнение и цену кегля по всем карточкам
teorkat-vvedenie/L2 с ТЕКСТОВОЙ зоной (использует уже осевшие в шапках
kegl_px/mezhstrochye/otstup_bloka — солвер деки не перезапускается).

  python3 progon.py --tag <метка>

Метод — тот же, что у vmeshchenie.izmerit/smeta.smeta_slajda, применённый
к каждой карточке в отдельности (slaid.compile_slide_html), а не к деку
целиком: так меряла сборка, давшая baseline 6/21, 171.2px (коммит 17e093e).
"""
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "_generator" / "sborka"))
import smeta  # noqa: E402
import vmeshchenie  # noqa: E402
from slaid import compile_slide_html  # noqa: E402
from formaty import parse_slide  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

LEK = ROOT / "teorkat-vvedenie" / "L2"
LOG = ROOT / "_studio" / "zhurnal" / "2026-08-10_dizajn-i-metriki" / "polya-i-uzor" / "progon.log"


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
            params, _ = parse_slide(md.read_text(encoding="utf-8"), sid=sid)
            reshena = str(params.get("verstka_reshena", "")).strip().lower() == "da"
            rows.append({
                "sid": sid, "tag": tag, "kegl": kegl, "cena_kegl_pct": cena_kegl,
                "pereliv_h_px": round(pereliv_h, 1), "pereliv_x_px": r["pereliv_x"],
                "smeta_vlezaet": s["vlezaet"], "brauzer_fits": r["fits"],
                "verstka_reshena": reshena,
            })
        b.close()
        tmp.unlink(missing_ok=True)

    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        for row in rows:
            row["t"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    pereliv = [r for r in rows if r.get("pereliv_h_px", 0) > 0.5]
    mereno = [r for r in rows if "pereliv_h_px" in r]
    svobodnye = [r for r in pereliv if not r["verstka_reshena"]]
    zapertye = [r for r in pereliv if r["verstka_reshena"]]
    kegli = [r["cena_kegl_pct"] for r in mereno]
    print("=== прогон %r: %d слайдов измерено, %d переполнено (своб. %d / заперт. %d), суммарно %.1f px ==="
          % (tag, len(mereno), len(pereliv), len(svobodnye), len(zapertye),
             sum(r["pereliv_h_px"] for r in pereliv)))
    for r in pereliv:
        print("  ❌ %-28s +%-7.1f px  %s" % (r["sid"], r["pereliv_h_px"],
              "(verstka_reshena: da)" if r["verstka_reshena"] else ""))
    if kegli:
        print("цена кегля: средняя %.2f%%, худшая %.2f%% (%s)"
              % (sum(kegli) / len(kegli), max(kegli),
                 max(mereno, key=lambda r: r["cena_kegl_pct"])["sid"]))
    print("лог дописан → %s" % LOG)


if __name__ == "__main__":
    main()
