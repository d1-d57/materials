#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Промер собранного дека: на сколько ИМЕННО не влезает каждая зона, по КАЖДОЙ сцене.

  python3 teorkat-vvedenie/src/tools/promer.py [--csv]

`audit.py` печатает факт «overflow» именем класса, но не величиной, а чинить грид
по факту без величины — это угадывание: не видно, нужен ли слайду один лишний ряд
или он не влезает вдвое. Здесь на каждую зону печатается величина в px и в строках
текущего кегля, плюс НОМЕР СЦЕНЫ, на которой она достигнута.

🔴 Два решения, каждое оплачено дефектом этого захода:

[1] МЕРИМ МАКСИМУМ ПО СЦЕНАМ, а не финальный кадр. Прежняя версия ставила слайду
    класс `scene-` + `data-scenes` и мерила один кадр — финальный. На деке БЕЗ замены
    это было верно: при накоплении финальная сцена и есть самая полная. На ленте СО
    ЗАМЕНОЙ — нет: `{@1-1}` уходит, `{@2-2}` приходит и уходит, и самой тяжёлой
    может оказаться любая сцена, а финальная — из самых пустых.

[2] ПОДГОТОВКА СТРАНИЦЫ — ОДНА И ТА ЖЕ, ЧТО У СЪЁМКИ (`kadry.SETUP`/`SHOW`).
    Пока подготовки были разные, промер и кадр расходились: на `s13` сцене 4 промер
    показывал Δh=0, а на снятом PNG нижний абзац был обрезан посередине строки.
    Расхождение опаснее любого из двух чисел по отдельности — одно заведомо врёт, а
    какое, не видно. Теперь состояние страницы у обоих ровно одно.

[3] ПЕРЕПОЛНЕНИЕ СЧИТАЕТСЯ ДВУМЯ ЛИНЕЙКАМИ, берётся максимум:
      · `scrollHeight − clientHeight` зоны;
      · насколько последний ВИДИМЫЙ блок вышел за нижнюю границу зоны («хвост»).
    Первая линейка промахивается, когда нижний margin последнего ребёнка схлопывается
    и в scrollHeight не входит, — ровно случай `s13`. Вторая это ловит.
"""
import sys, json
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kadry import SETUP, SHOW

DECK = (Path(__file__).resolve().parents[1] / "dist" / "index.html")

ZONA = r"""
([sid, k, scenes]) => {
  const s = document.getElementById(sid);
  const out = [];
  s.querySelectorAll('.zone').forEach(z => {
    const cs = getComputedStyle(z);
    const tb = parseFloat(cs.fontSize);
    const lh = parseFloat(cs.lineHeight) || tb * 1.5278;
    const zr = z.getBoundingClientRect();
    let hvost = 0;
    z.querySelectorAll('p,ul').forEach(e => {
      const es = getComputedStyle(e);
      if (es.display === 'none' || es.visibility === 'hidden') return;
      const r = e.getBoundingClientRect();
      hvost = Math.max(hvost, Math.round(r.bottom - zr.bottom));
    });
    out.push({
      id: sid, cls: z.className, scenes: scenes, scene: k,
      ch: z.clientHeight, sh: z.scrollHeight,
      dh: Math.max(z.scrollHeight - z.clientHeight, hvost),
      dw: z.scrollWidth - z.clientWidth,
      hvost: hvost, tb: tb, lh: lh,
      p: z.querySelectorAll('p').length,
      ul: z.querySelectorAll('ul').length,
      li: z.querySelectorAll('li').length,
      f: z.querySelectorAll('p.formula').length,
      op: z.querySelectorAll('p.op-def,p.op-utv,p.op-task').length,
      chars: (z.textContent || '').replace(/\s+/g, ' ').trim().length,
    });
  });
  return out;
}
"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 810}, device_scale_factor=1)
    pg.goto("file://" + str(DECK))
    pg.wait_for_load_state("networkidle")
    pg.evaluate("document.fonts && document.fonts.ready")
    pg.wait_for_timeout(500)
    plan = pg.evaluate(SETUP)
    pg.add_style_tag(content="*,*::before,*::after{transition:none!important;"
                             "animation:none!important}")
    vse = []
    for sid, scenes in plan:
        for k in range(1, scenes + 1):
            pg.evaluate(SHOW, [sid, k])
            pg.wait_for_timeout(30)
            vse.extend(pg.evaluate(ZONA, [sid, k, scenes]))
    b.close()

kadrov = sum(s for _, s in plan)

# максимум по сценам на каждую зону
acc = {}
for d in vse:
    key = (d["id"], d["cls"])
    if key not in acc or d["dh"] > acc[key]["dh"]:
        acc[key] = d
data = list(acc.values())

if "--csv" in sys.argv:
    print(json.dumps(data, ensure_ascii=False))
    sys.exit(0)

bad = [d for d in data if d["dh"] > 1 or d["dw"] > 1]
print("зон всего: %d · переполнено: %d · кадров промерено: %d"
      % (len(data), len(bad), kadrov))
print("%-5s %-14s %4s %5s %5s %7s %6s %6s %4s %3s %3s %5s"
      % ("id", "зона", "сц", "clH", "scrH", "Δh", "хвост", "строк", "кегль",
         "p", "оп", "знак"))
for d in sorted(bad, key=lambda x: -x["dh"]):
    print("%-5s %-14s %d/%d %5d %5d %+7d %+6d %6.1f %4.0f %3d %3d %5d"
          % (d["id"], d["cls"].replace("zone ", ""), d["scene"], d["scenes"],
             d["ch"], d["sh"], d["dh"], d["hvost"],
             d["dh"] / d["lh"], d["tb"], d["p"], d["op"], d["chars"]))
if bad:
    ds = sorted(d["dh"] for d in bad)
    print("Δh: медиана %+d · макс %+d · мин %+d" % (ds[len(ds) // 2], ds[-1], ds[0]))
    print("Δw>1: %d" % sum(1 for d in bad if d["dw"] > 1))
sys.exit(0)
