#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Заход solver-v3-dyhanie, Э3: корпусная цель для «меры дыхания» — доля
`zone.clientHeight`, занятая промежутками между соседними блоками (те же
элементы, что получают `margin-top:var(--blok)`), измеренная на 16 слайдах
обратного прогона ПРЯМО НА ЖИВЫХ СОБРАННЫХ ДЕКАХ (`<deck>/src/dist/index.html`,
Я4, read-only) — не на временных карточках `postroit_kartochku.build_card`.

Почему не через `postroit_kartochku` (Я3): та карточка — МИНИМАЛЬНАЯ (только
`imya`/`tip_verstki`/`liniya`/`illustracii`), и на живых слайдах трёх деков
компилятор (`slaid.py`) через неё даёт ПУСТУЮ `.zone.t-body` (проверено
фактом: `blocks:0` на всех 16 — воспроизводимо, не разовый глюк). Ловушка
именно такого рода прямо названа в докстринге `postroit_kartochku.py`
(«кривой вход обязан падать ГРОМКО, не молчать») — здесь она, к сожалению,
молчит, а не падает; это НЕ моя зона (`postroit_kartochku.py` — Я3, не
переписываю), поэтому обхожу измерением на уже собранном `dist/index.html`,
где кегль/lh/blok/liniya УЖЕ прописаны как per-slide CSS (то, что реально
видел человек), рендер честнее реконструкции.

Список 16 пар (deck, sid) — из `REZULTATY.md`, командой (KONSTITUCIYA §10),
не переписан руками — тот же набор, на котором Э5 делает перепрогон.

Дорогая операция (16 рендеров) — поэтому ОТДЕЛЬНЫЙ разовый скрипт, не часть
`korpus.py`/`vmeshchenie.py` (те остаются быстрыми и браузер-независимыми на
каждом solve). Результат — именованная константа в `vmeshchenie.py`,
процитированная на эту команду (тот же приём, каким уже процитированы
`FILL_LO/HI`, `LINE_LEN_*`).

  python3 _generator/tools/fixtures/sborka/obratnyj-progon/izmerit_dyhanie.py
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SBORKA = REPO / "_generator" / "sborka"
sys.path.insert(0, str(SBORKA))
import korpus  # noqa: E402

REZULTATY = HERE / "REZULTATY.md"

# Ровно тот же снимок промежутков, что `tipografika()` в `vmeshchenie.py` (Э3
# захода solver-v3-dyhanie): блоки `p`/`ul.tlist` внутри текстового контейнера
# зоны — ровно то, что получает межабзацный отступ. `teorkat-vvedenie`/`buffon`
# несут КАНОН-разметку `.zone.t-body` (плоско, без обёртки), `dandelin` —
# СТАРЫЙ формат `.zone.pad > .copy` (найдено этим скриптом: korpus.py
# докстринг уже предупреждал «три дека построены ПО-РАЗНОМУ», здесь та же
# разница всплывает на уровне DOM, не только CSS-парсинга). Проверено фактом
# по живому `overlay.css`: и `dandelin` (`.copy p+p{margin-top:26px}`), и
# `buffon` (`.copy p+p{margin-top:26px!important}`) РЕАЛЬНО рендерят те же
# 26px, что и канон-умолчание `--blok` — не совпадение в номинале, вычисленный
# `calc(1em*var(--lh))` у buffon `!important`-переопределён той же цифрой.
_JS_DYHANIE = r"""
(sid) => {
  const idx = slides.findIndex(s => s.id === sid);
  if (idx < 0) return {error: 'слайд #' + sid + ' не найден в slides'};
  showSingle(idx, scenesOf(slides[idx]));  // финальная сцена — то же, что применяет солвер
  const zone = document.querySelector('#' + sid + ' .zone.t-body') ||
               document.querySelector('#' + sid + ' .zone.pad') ||
               document.querySelector('#' + sid + ' .zone.plaque') ||
               document.querySelector('#' + sid + ' .t-body');
  if (!zone) return {error: 'зона (.zone.t-body/.zone.pad/.zone.plaque) не найдена на #' + sid};
  const container = zone.querySelector(':scope > .copy') || zone;
  const blocks = Array.from(container.querySelectorAll(':scope > p, :scope > ul.tlist'));
  if (blocks.length < 2) return {dyhanie: null, blocks: blocks.length,
                                  clientHeight: zone.clientHeight};
  let gapSum = 0;
  for (let i = 1; i < blocks.length; i++) {
    const gap = blocks[i].getBoundingClientRect().top - blocks[i - 1].getBoundingClientRect().bottom;
    if (gap > 0) gapSum += gap;
  }
  const ch = zone.clientHeight;
  return {dyhanie: ch ? (100 * gapSum / ch) : null, blocks: blocks.length,
          clientHeight: ch, scrollHeight: zone.scrollHeight};
}
"""


def slides_from_rezultaty():
    """(deck, sid) из таблицы `REZULTATY.md` — те же 16, что и Э5 перепрогон.
    Строка вида `| 1 | teorkat-vvedenie/s01 | ... |`."""
    text = REZULTATY.read_text(encoding="utf-8")
    out = []
    for line in text.splitlines():
        m = re.match(r"^\|\s*\d+\s*\|\s*([\w-]+)/([\w-]+)\s*\|", line)
        if m:
            out.append((m.group(1), m.group(2)))
    return out


def main():
    pairs = slides_from_rezultaty()
    if not pairs:
        print("REZULTATY.md не дал ни одной пары (deck, sid) — нечего мерить", file=sys.stderr)
        return 1

    by_deck = {}
    for deck, sid in pairs:
        by_deck.setdefault(deck, []).append(sid)

    from playwright.sync_api import sync_playwright
    rows = []
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        page = b.new_page(viewport={"width": 1440, "height": 810}, device_scale_factor=1)
        for deck, sids in by_deck.items():
            dist = REPO / deck / "src" / "dist" / "index.html"
            if not dist.is_file():
                print("НЕТ %s — пропускаю дек целиком (%d слайдов)" % (dist, len(sids)), file=sys.stderr)
                continue
            page.goto("file://" + quote(str(dist)))
            page.wait_for_timeout(200)
            for sid in sids:
                res = page.evaluate(_JS_DYHANIE, sid)
                rows.append({"deck": deck, "sid": sid, **res})
        b.close()

    values = [r["dyhanie"] for r in rows if r.get("dyhanie") is not None]
    stat = korpus.summarize(values)
    print(json.dumps({"строки": rows, "дыхание_pct": stat}, ensure_ascii=False, indent=2))
    print("\n--- сводка (Э3 захода solver-v3-dyhanie) ---", file=sys.stderr)
    if stat:
        print("дыхание_pct  n=%d  p5=%s  медиана=%s  p95=%s  stdev=%s"
              % (stat["n"], stat["p5"], stat["median"], stat["p95"], stat["stdev"]), file=sys.stderr)
    else:
        print("нет данных (ни один слайд не дал >=2 блоков)", file=sys.stderr)
    errors = [r for r in rows if r.get("error")]
    if errors:
        print("ОШИБКИ (%d): %s" % (len(errors), errors), file=sys.stderr)
    skipped = len(rows) - len(values) - len(errors)
    if skipped:
        print("пропущено (< 2 блоков): %d из %d" % (skipped, len(rows)), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
