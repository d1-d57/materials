#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Локальный рендер/сверка колод (запускать НА СВОЁЙ МАШИНЕ — нужен Chrome + playwright,
в песочнице генератора их нет). Рецепт совпадает с buffon/_render-zahod04/shot.py:
Chrome-канал, 1440×810, deviceScaleFactor 2, кадр через ?only=N.

  # снять все слайды колоды в PNG:
  python3 render.py <deck.html> [outdir]

  # СВЕРКА оригинал↔пересборка (послайдно, с попиксельной разницей, если есть Pillow):
  python3 render.py --compare <orig.html> <rebuilt.html> [outdir]

Установка на своей машине:  pip install playwright && playwright install chrome
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

W, H, DSR = 1440, 810, 2


def _count_slides(page, url):
    """Считать ТЕМ ЖЕ селектором, что движок, иначе индексы разъезжаются.

    🔴 Здесь стоял `.slide`, а движок собирает `slides` как
    `.slide:not([data-skip])`. У dandelin ровно один слайд помечен `data-skip`:
    в документе 19 секций, в массиве движка 18. Итог — двойной промах, оба тихие:
    последний кадр снимался с `?only=18`, где `slides[18]` не существует (пустой
    кадр), а каждый индекс ПОСЛЕ пропущенного слайда указывал на соседа, то есть
    файл `NN.png` показывал не тот слайд, что назван в имени. Тот же класс, что и
    `scene=99`: харнесс смотрел не туда. Найдено верификатором.
    """
    page.goto(url)
    page.wait_for_timeout(400)
    return page.evaluate(
        "() => document.querySelectorAll('.slide:not([data-skip])').length")


def _shot(page, deck_url, idx, out, wait=1200):
    # 🔴 `scene` НЕ передаём — и это не упущение, а единственный способ получить
    # финальную сцену. Движок сам ставит её при отсутствии параметра:
    # `exportFrame` берёт `scenesOf(slides[n])`, то есть фактическое `data-scenes`
    # слайда (`skeleton/engine.js`, ветка «Q.get('scene') !== null ? … : …»).
    # Раньше здесь стояло `&scene=99` с комментарием «показать в финальной сцене».
    # Оно НЕ работало: сцены раскрываются КЛАССОМ `.scene-K`, каскад в базе идёт
    # до `.scene-5`, правила `.scene-99` не существует ⇒ на кадре всё пошаговое
    # содержимое оставалось невидимым (`opacity:0;visibility:hidden`), и зрительная
    # петля месяц смотрела на нераскрытые слайды. Диагноз был поставлен в чужом
    # проекте и залатан там же (`teorkat-vvedenie/src/tools/sobrat_overlay.py`
    # порождал `.scene-99`) — фабрика не всосала ни диагноза, ни заплаты.
    # Просьба финальной сцены — ОДИН механизм и работает на УЖЕ СОБРАННЫХ деках:
    # каждый несёт свою копию движка, а этот default есть во всех.
    page.goto(f"{deck_url}?only={idx}")
    page.wait_for_timeout(wait)
    page.screenshot(path=str(out))


def shoot(deck, outdir):
    deck = pathlib.Path(deck).resolve()
    outdir = pathlib.Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    url = f"file://{deck}"
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=DSR)
        n = _count_slides(pg, url)
        print(f"{deck.name}: {n} слайдов")
        for i in range(n):
            _shot(pg, url, i, outdir / f"{i:02d}.png")
        b.close()
    print(f"→ {n} PNG в {outdir}")


def compare(orig, rebuilt, outdir):
    orig, rebuilt = pathlib.Path(orig).resolve(), pathlib.Path(rebuilt).resolve()
    outdir = pathlib.Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image, ImageChops
        have_pil = True
    except ImportError:
        have_pil = False
        print("Pillow не найден — сохраню кадры для глазной сверки без попиксельного диффа "
              "(pip install pillow, чтобы включить).")
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=DSR)
        n = _count_slides(pg, f"file://{orig}")
        worst = []
        for i in range(n):
            oa, rb = outdir / f"{i:02d}_orig.png", outdir / f"{i:02d}_rebuilt.png"
            _shot(pg, f"file://{orig}", i, oa)
            _shot(pg, f"file://{rebuilt}", i, rb)
            if have_pil:
                a, c = Image.open(oa).convert("RGB"), Image.open(rb).convert("RGB")
                diff = ImageChops.difference(a, c)
                bbox = diff.getbbox()
                changed = 0 if bbox is None else sum(1 for px in diff.crop(bbox).getdata() if any(px))
                worst.append((changed, i))
                print(f"  слайд {i:02d}: изменённых пикселей = {changed}"
                      + ("  ✓ идентичен" if changed == 0 else "  ⟵ смотри кадр"))
        b.close()
    if have_pil:
        worst.sort(reverse=True)
        bad = [i for c, i in worst if c]
        print("\nИТОГ:", "все слайды попиксельно идентичны ✓" if not bad
              else f"различаются слайды {bad} — открой {outdir}/NN_orig.png vs NN_rebuilt.png")


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); return 1
    if a[0] == "--compare":
        compare(a[1], a[2], a[3] if len(a) > 3 else "_render")
    else:
        shoot(a[0], a[1] if len(a) > 1 else "_render")
    return 0


if __name__ == "__main__":
    sys.exit(main())
