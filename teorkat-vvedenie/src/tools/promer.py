#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Промер собранного дека: на сколько ИМЕННО не влезает каждая зона.

  python3 teorkat-vvedenie/src/tools/promer.py [--csv]

`audit.py` печатает факт «overflow» именем класса, но не величиной, а чинить грид
по факту без величины — это угадывание: не видно, нужен ли слайду один лишний ряд
или он не влезает вдвое и требует SPLIT. Здесь на каждую зону печатается
scrollHeight − clientHeight в px и в строках текущего кегля, плюс что внутри
(абзацев, списков, формул) — чтобы решение «шире колонка / другой архетип / SPLIT»
принималось по числу.
"""
import sys, os, json
from pathlib import Path
from playwright.sync_api import sync_playwright

DECK = (Path(__file__).resolve().parents[1] / "dist" / "index.html")

# 🔴 МЕРИМ МАКСИМУМ ПО СЦЕНАМ, а не финальный кадр. Прежняя версия ставила слайду
# класс `scene-` + `data-scenes` и мерила один кадр — финальный. На деке БЕЗ замены
# это было корректно: при накоплении финальная сцена и есть самая полная. На ленте
# СО ЗАМЕНОЙ — нет: `{@1-1}` уходит, `{@2-2}` приходит и уходит, и самой тяжёлой
# может оказаться любая сцена, а финальная — из самых пустых. Мерить финальный кадр
# значило бы подгонять грид под неверный кадр и объявлять зелёным слайд, который
# переполнен на втором клике. Поэтому: перебрать сцены 1..N, померить КАЖДУЮ, взять
# максимум Δh/Δw по зоне и запомнить, НА КАКОЙ сцене он достигнут (без этого нечего
# смотреть глазами: «слайд переполнен» без номера сцены — снова угадывание).
JS = r"""
() => {
  const out = [];
  document.querySelectorAll('.slide').forEach(s => {
    const n = parseInt(s.dataset.scenes || '1', 10) || 1;
    // движок держит нетекущие слайды в display:none — у скрытой зоны clientHeight
    // и scrollHeight оба 0, и переполнение измеряется как «нет». Тот же приём,
    // что в audit.py: раскрыть, померить, вернуть как было.
    const disp = s.style.display; s.style.display = '';
    const acc = new Map();
    for (let k = 1; k <= n; k++) {
      for (let i = 1; i <= 9; i++) s.classList.remove('scene-' + i);
      s.classList.remove('scene-99');
      s.classList.add('scene-' + k);
      s.querySelectorAll('[data-scene-until]').forEach(el =>
        el.classList.toggle('scene-off', k >= +el.dataset.sceneUntil));
      s.querySelectorAll('.zone').forEach(z => {
        const cs = getComputedStyle(z);
        const tb = parseFloat(cs.fontSize);
        const lh = parseFloat(cs.lineHeight) || tb * 1.5278;
        const rec = {
          id: s.id, cls: z.className, scenes: n, scene: k,
          ch: z.clientHeight, sh: z.scrollHeight,
          cw: z.clientWidth, sw: z.scrollWidth,
          dh: z.scrollHeight - z.clientHeight,
          dw: z.scrollWidth - z.clientWidth,
          tb: tb, lh: lh,
          p: z.querySelectorAll('p').length,
          ul: z.querySelectorAll('ul').length,
          li: z.querySelectorAll('li').length,
          f: z.querySelectorAll('p.formula').length,
          op: z.querySelectorAll('p.op-def,p.op-utv,p.op-task').length,
          chars: (z.textContent || '').replace(/\s+/g, ' ').trim().length,
        };
        const key = s.id + '|' + z.className;
        const prev = acc.get(key);
        if (!prev || rec.dh > prev.dh || (rec.dh === prev.dh && rec.dw > prev.dw))
          acc.set(key, rec);
      });
    }
    // вернуть слайд в первую сцену и снять служебные метки
    for (let i = 1; i <= 9; i++) s.classList.remove('scene-' + i);
    s.classList.add('scene-1');
    s.querySelectorAll('[data-scene-until]').forEach(el =>
      el.classList.toggle('scene-off', 1 >= +el.dataset.sceneUntil));
    s.style.display = disp;
    acc.forEach(v => out.push(v));
  });
  return out;
}
"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 810})
    pg.goto("file://" + str(DECK))
    pg.wait_for_load_state("networkidle")
    pg.evaluate("document.fonts && document.fonts.ready")
    pg.wait_for_timeout(400)
    data = pg.evaluate(JS)
    b.close()

if "--csv" in sys.argv:
    print(json.dumps(data, ensure_ascii=False))
    sys.exit(0)

bad = [d for d in data if d["dh"] > 1 or d["dw"] > 1]
print("зон всего: %d · переполнено: %d · кадров промерено: %d"
      % (len(data), len(bad), sum(d["scenes"] for d in data)))
print("%-5s %-14s %4s %5s %5s %7s %6s %4s %3s %3s %3s %5s"
      % ("id", "зона", "сц", "clH", "scrH", "Δh", "строк", "кегль", "p", "li", "оп", "знак"))
for d in sorted(bad, key=lambda x: -x["dh"]):
    print("%-5s %-14s %d/%d %5d %5d %+7d %6.1f %4.0f %3d %3d %3d %5d"
          % (d["id"], d["cls"].replace("zone ", ""), d["scene"], d["scenes"],
             d["ch"], d["sh"], d["dh"],
             d["dh"] / d["lh"], d["tb"], d["p"], d["li"], d["op"], d["chars"]))
if bad:
    ds = sorted(d["dh"] for d in bad)
    print("Δh: медиана %+d · макс %+d · мин %+d" % (ds[len(ds) // 2], ds[-1], ds[0]))
    print("Δw>1: %d" % sum(1 for d in bad if d["dw"] > 1))
sys.exit(0)
