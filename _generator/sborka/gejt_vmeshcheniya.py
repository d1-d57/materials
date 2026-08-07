#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Гейт вмещения (Э4 захода solver-vmeshcheniya) — краснеет и не пропускает
дальше, если текст на скомпилированном слайде обрезан `overflow:hidden`.

То, чего не хватало: гейт бюджета слов (`gejt_kartochki.py`) считает знаки, а
не физическое вмещение — был зелёным ровно там, где на живом слайде s08
пропало четыре абзаца из семи. Этот гейт смотрит в тот же браузер, что и
солвер (`vmeshchenie.py`), и отвечает ИМЕННО на вопрос «влезло или обрезано».

  python3 _generator/sborka/gejt_vmeshcheniya.py <slide.html> [<slide.html> ...]
  exit 0 — все переданные слайды влезли (fill<=100%, clipped=false)
  exit 1 — хотя бы один обрезан
"""
import argparse
import sys
from pathlib import Path

SBORKA = Path(__file__).resolve().parent
sys.path.insert(0, str(SBORKA))
from vmeshchenie import izmerit  # noqa: E402


def check_slide(page, html_path):
    """Один скомпилированный слайд → (ok: bool, fill: float, clipped: bool)."""
    r = izmerit(page, html_path)
    return r


def main():
    ap = argparse.ArgumentParser(description="Гейт вмещения — краснеет на обрезанном тексте")
    ap.add_argument("html", nargs="+", help="скомпилированные HTML слайдов (slaid.py -o ...)")
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright
    bad = []
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        page = b.new_page(viewport={"width": 1440, "height": 810}, device_scale_factor=1)
        for html in args.html:
            r = check_slide(page, html)
            fill = r["fill"]
            clipped = fill is not None and fill > 100
            status = "❌ ОБРЕЗАНО" if clipped else "✅ влезло"
            print("%s  %-40s заполнение %.1f%%" % (status, html, fill if fill is not None else -1))
            if clipped:
                bad.append((html, fill))
        b.close()

    if bad:
        print("\nГЕЙТ КРАСНЫЙ: %d слайд(ов) обрезано:" % len(bad), file=sys.stderr)
        for html, fill in bad:
            print("  %s — заполнение %.1f%%, не влезает %.1f%% высоты зоны"
                  % (html, fill, fill - 100), file=sys.stderr)
        return 1
    print("\nГЕЙТ ЗЕЛЁНЫЙ: все %d слайд(ов) влезли." % len(args.html))
    return 0


if __name__ == "__main__":
    sys.exit(main())
