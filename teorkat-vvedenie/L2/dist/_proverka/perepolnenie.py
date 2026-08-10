#!/usr/bin/env python3
"""Переполнение по ВСЕМ слайдам дека: для каждого элемента с overflow:hidden
сравнить scrollHeight/scrollWidth с client*. perepolnenie.py <index.html>"""
import sys, pathlib
from playwright.sync_api import sync_playwright
src = pathlib.Path(sys.argv[1]).resolve()
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": 1440, "height": 810})
    pg.goto(src.as_uri()); pg.wait_for_timeout(1800)
    r = pg.evaluate("""() => {
      const out = [];
      const slides = [...document.querySelectorAll('#deck > .slide:not([data-skip])')];
      slides.forEach((s, i) => {
        const prev = s.style.display; s.style.display = '';
        [s, ...s.querySelectorAll('*')].forEach(el => {
          if ((el.className||'').toString().includes('katex-mathml')) return;  // скрытая MathML-аннотация KaTeX клипается намеренно
          const cs = getComputedStyle(el);
          if (cs.overflow === 'hidden' || cs.overflowY === 'hidden' || cs.overflowX === 'hidden') {
            const dh = el.scrollHeight - el.clientHeight, dw = el.scrollWidth - el.clientWidth;
            if (dh > 2 || dw > 2) out.push({slide: i + 1, id: s.id,
              el: el.className || el.tagName, dh, dw});
          }
        });
        // 🔴 МЕРИТЬ ДО ВОЗВРАТА display. Было наоборот: `s.style.display = prev`
        // стояло ПЕРЕД этой проверкой, слайд снова становился display:none, обе
        // getBoundingClientRect давали нули, и условие 0 > 0 не срабатывало НИКОГДА.
        // Ветка «наезд без клипа» была мертва с рождения; найдено контрольным
        // выстрелом захода primenenie-vizuala: возвращённая поломка визитки
        // (74px) даёт реальный наезд +35px, а сторож молчал.
        const bt = s.querySelector('.brd-title'), ph = s.querySelector('.p-photo');
        if (bt && ph) { const a = bt.getBoundingClientRect(), b2 = ph.getBoundingClientRect();
          if (a.bottom > b2.top) out.push({slide: i+1, id: s.id, el: 'brd-title НАЕХАЛ на .p-photo',
            dh: Math.round(a.bottom - b2.top), dw: 0}); }
        s.style.display = prev;
      });
      return {n: slides.length, bad: out};
    }""")
    b.close()
print("слайдов проверено:", r["n"])
print("переполнений:", len(r["bad"]))
for x in r["bad"]:
    print("  s%02d %-12s %-28s +%dpx по высоте, +%dpx по ширине" % (x["slide"], x["id"], str(x["el"])[:28], x["dh"], x["dw"]))
