#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TOOL-CONTRACT: called-by-hand — закрытие ФАЗЫ 3 (заход svedenie-i-smeta, Э2.5).
# Автоматическим хуком быть НЕ МОЖЕТ по существу: требует скомпилированных
# слайдов и живого браузера, на pre-commit это минуты и падение без Chrome.
# Точка вызова названа в конвейере — `bootstrap_lekcii.LIFECYCLE_TMPL`, строка
# «ФАЗА 3.9», до ФАЗЫ 4. До 08.08 гейт был написан и не звался НИ НА ОДНОМ шаге.
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
import re
import sys
from pathlib import Path

SBORKA = Path(__file__).resolve().parent
sys.path.insert(0, str(SBORKA))
from vmeshchenie import izmerit  # noqa: E402

# 🔴 Найдено живым прогоном (заплатка sborka-l2-fazy-4-7): не у каждого слайда
# есть текстовая зона — `tip_verstki: polnyj_ekran` с непустым `illustracii`
# рендерит ТОЛЬКО картинки (`tipy.py: polnyj_ekran`), без `.zone.t-body`. Мерить
# там нечего — раньше гейт падал `RuntimeError` и ронял ВЕСЬ прогон ради одного
# бестекстового слайда, даже если он последний в списке. Тот же приём, что уже
# стоит в `deck.py:_podobrat_tipografiku` — пропуск ДО вызова измерителя.
T_BODY_RE = re.compile(r'class="[^"]*\bt-body\b[^"]*"')


def check_slide(page, html_path):
    """Один скомпилированный слайд → (ok: bool, fill: float, clipped: bool)."""
    r = izmerit(page, html_path)
    return r


def main():
    ap = argparse.ArgumentParser(description="Гейт вмещения — краснеет на обрезанном тексте")
    ap.add_argument("html", nargs="+", help="скомпилированные HTML слайдов (slaid.py -o ...)")
    args = ap.parse_args()

    # 🔴 Кривой вход отвергается ДО запуска браузера: несуществующий путь раньше
    # давал `FileNotFoundError` из середины прогона, уже подняв Chrome, и вердикт
    # по остальным слайдам терялся вместе с трейсбеком.
    net = [h for h in args.html if not Path(h).is_file()]
    if net:
        print("ОШИБКА: не существует или не файл — %s" % ", ".join(net), file=sys.stderr)
        return 2

    from playwright.sync_api import sync_playwright
    bad = []
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        page = b.new_page(viewport={"width": 1440, "height": 810}, device_scale_factor=1)
        skipped = 0
        for html in args.html:
            if not T_BODY_RE.search(Path(html).read_text(encoding="utf-8")):
                print("⚪ БЕЗ ТЕКСТА  %-40s текстовой зоны на слайде нет — не мерю" % html)
                skipped += 1
                continue
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
    print("\nГЕЙТ ЗЕЛЁНЫЙ: все %d слайд(ов) с текстом влезли (%d без текстовой зоны — не мерены)."
          % (len(args.html) - skipped, skipped))
    return 0


if __name__ == "__main__":
    sys.exit(main())
