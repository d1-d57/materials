#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ЗАМЕР ВАРИАНТА НА ЖИВОМ КАДРЕ — геометрия из браузера, а не из головы.

Собирает вариант (оверлей `shema.overlay`) поверх обёрнутой копии деки, открывает
её в том же headless Chrome, которым генератор подбирает типографику
(`sborka/deck.py:200`), и снимает с КАДРА:

  · высоту текстовой колонки каждого слайда и факт переполнения зоны;
  · кегль тела и кегль доказательства — из `getComputedStyle`, то есть то,
    что реально нарисовано, а не то, что я задумал;
  · ширину, цвет и прозрачность линейки — из `::before` центрального блока;
  · цвет тихого заголовка ПОСЛЕ применения прозрачности, сведённый на холст,
    и его контраст к холсту по формуле WCAG 2.1;
  · все вертикальные зазоры между блоками в долях шага строк.

🔴 Две накладки на время замера, обе названы вслух, обе нужны и обе безвредны:
  1. `[data-scene-from]` раскрываются принудительно — иначе половина текста
     скрыта `visibility:hidden` и высота колонки меряется по недособранному
     кадру. Слайд смотрят в ПОСЛЕДНЕЙ сцене, её и меряем.
  2. Все слайды делаются видимыми одновременно — движок показа тут не нужен,
     нужен только вёрстка-слой.
Обе живут в `NAKLADKA` ниже и в итоговый CSS-фрагмент НЕ входят.
"""
import argparse
import json
import os
import re
import sys

ZDES = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ZDES)
import shema  # noqa: E402

NAKLADKA = """
/* только для замера/съёмки — в схему не входит (см. докстроку zamer.py) */
[data-scene-from] { opacity: 1 !important; visibility: visible !important; }
.slide { display: block !important; animation: none !important; }
#stage { position: static !important; display: block !important; overflow: visible !important; }
#bleed, #hint, #lect-zone, #lect-progress { display: none !important; }
"""

JS = r"""
() => {
  const out = [];
  document.querySelectorAll('section.slide').forEach(s => {
    const zone = s.querySelector('.zone.copy.t-body');
    if (!zone) return;
    const zr = zone.getBoundingClientRect();
    const zs = getComputedStyle(zone);
    const blks = [...zone.querySelectorAll(':scope > .blk')];
    if (!blks.length) return;
    const bl = [];
    for (const b of blks) {
      const cs = getComputedStyle(b), r = b.getBoundingClientRect();
      const pb = getComputedStyle(b, '::before');
      const h  = b.querySelector('.blk-h');
      const hs = h ? getComputedStyle(h) : null;
      const hr = h ? h.getBoundingClientRect() : null;
      bl.push({
        tip: b.dataset.tip, central: b.dataset.central === '1',
        top: r.top, bottom: r.bottom, left: r.left, width: r.width,
        fs: parseFloat(cs.fontSize), lh: parseFloat(cs.lineHeight),
        padLeft: parseFloat(cs.paddingLeft), marginTop: parseFloat(cs.marginTop),
        rule: pb.content !== 'none' ? {
          w: parseFloat(pb.width), h: parseFloat(pb.height),
          bg: pb.backgroundColor, op: parseFloat(pb.opacity), left: pb.left
        } : null,
        zag: hs ? { fs: parseFloat(hs.fontSize), color: hs.color,
                    op: parseFloat(hs.opacity), h: hr.height,
                    mb: parseFloat(hs.marginBottom), mt: parseFloat(hs.marginTop),
                    text: h.innerText.trim() } : null
      });
    }
    const last = blks[blks.length - 1].getBoundingClientRect();
    out.push({
      id: s.id, zoneTop: zr.top, zoneH: zr.height, zoneW: zr.width,
      fsZone: parseFloat(zs.fontSize), lhZone: parseFloat(zs.lineHeight),
      blok: parseFloat(getComputedStyle(zone).getPropertyValue('--blok')) || null,
      kolonka: last.bottom - zr.top,
      perepolnenie: (last.bottom - zr.bottom),
      bloki: bl
    });
  });
  return out;
}
"""


def _rgb(s):
    m = re.findall(r"[\d.]+", s or "")
    if len(m) < 3:
        return None
    r, g, b = (float(x) for x in m[:3])
    a = float(m[3]) if len(m) > 3 else 1.0
    return (r, g, b, a)


def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def yarkost(rgb):
    r, g, b = rgb[:3]
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def svesti(perednij, fon, alpha):
    """цвет с прозрачностью, сведённый на холст — то, что глаз видит на кадре."""
    return tuple(perednij[i] * alpha + fon[i] * (1 - alpha) for i in range(3))


def kontrast(a, b):
    la, lb = yarkost(a), yarkost(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def sobrat(baza_html, css, out):
    h = open(baza_html, encoding="utf-8").read()
    stil = "\n<style id='overlay'>%s\n%s</style>\n" % (css, NAKLADKA)
    i = h.rfind("</head>")
    h = h[:i] + stil + h[i:] if i > 0 else h + stil
    open(out, "w", encoding="utf-8").write(h)
    return out


class Sessiya(object):
    """Один браузер на весь перебор.

    Прежняя схема поднимала Chrome под КАЖДЫЙ вариант и перезагружала страницу
    на 3,5 МБ — двадцать три варианта не уложились в две минуты и прогон
    оборвался по таймауту. Здесь страница грузится один раз, а вариант меняет
    ТОЛЬКО содержимое `<style id="overlay">`; замер тот же, данные те же.
    """

    def __init__(self, put_html):
        from playwright.sync_api import sync_playwright
        self._pw = sync_playwright().start()
        self._br = self._pw.chromium.launch(channel="chrome", headless=True)
        self.pg = self._br.new_page(viewport={"width": 1440, "height": 810},
                                    device_scale_factor=1)
        self.pg.goto("file://" + os.path.abspath(put_html))
        self.pg.wait_for_timeout(700)

    def variant(self, css, snimki=None, papka=None):
        self.pg.evaluate("t => { document.getElementById('overlay').textContent = t; }",
                         css + "\n" + NAKLADKA)
        self.pg.wait_for_timeout(120)
        dannye = self.pg.evaluate(JS)
        if snimki and papka:
            os.makedirs(papka, exist_ok=True)
            for sid in snimki:
                el = self.pg.query_selector("section.slide#%s" % sid)
                if el:
                    el.screenshot(path=os.path.join(papka, "%s.png" % sid))
        return dannye

    def cena_v_kegle(self):
        """ЦЕНА СХЕМЫ В КЕГЛЕ ТЕЛА — то, чем расплачивается зритель.

        «Прибавка в строках» отвечает не на тот вопрос. Кегль на живом деке
        подбирает солвер, и он уже выбрал максимум, влезающий в зону: любая
        прибавка высоты не «вылезет за кадр», а заставит солвер УМЕНЬШИТЬ кегль
        на следующем прогоне. Значит честная валюта сравнения одна — на сколько
        процентов придётся опустить кегль тела, чтобы колонка снова влезла.

        Меряется в лоб: кегль зоны множится на s и ищется наибольшее s, при
        котором переполнения нет. Межблочный отступ при этом НЕ трогается —
        оценка получается консервативной (солвер ужал бы и его).
        """
        return self.pg.evaluate(r"""
        () => {
          const out = [];
          document.querySelectorAll('section.slide').forEach(s => {
            const zone = s.querySelector('.zone.copy.t-body');
            if (!zone) return;
            const blks = zone.querySelectorAll(':scope > .blk');
            if (!blks.length) return;
            const bazovyj = parseFloat(getComputedStyle(zone).fontSize);
            const vlez = (sc) => {
              zone.style.fontSize = (bazovyj * sc) + 'px';
              const zr = zone.getBoundingClientRect();
              const last = blks[blks.length - 1].getBoundingClientRect();
              return last.bottom - zr.bottom;
            };
            let lo = 0.70, hi = 1.0, s_ok = null;
            if (vlez(1.0) <= 0.5) { s_ok = 1.0; }
            else {
              for (let i = 0; i < 14; i++) {
                const m = (lo + hi) / 2;
                if (vlez(m) <= 0.5) { s_ok = m; lo = m; } else { hi = m; }
              }
            }
            zone.style.fontSize = '';
            out.push({ id: s.id, bazovyj: bazovyj, s: s_ok });
          });
          return out;
        }
        """)

    def close(self):
        self._br.close()
        self._pw.stop()


def snyat(put_html, snimki=None, papka_snimkov=None):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch(channel="chrome", headless=True)
        pg = br.new_page(viewport={"width": 1440, "height": 810},
                         device_scale_factor=1)
        pg.goto("file://" + os.path.abspath(put_html))
        pg.wait_for_timeout(700)
        dannye = pg.evaluate(JS)
        if snimki and papka_snimkov:
            os.makedirs(papka_snimkov, exist_ok=True)
            for sid in snimki:
                el = pg.query_selector("section.slide#%s" % sid)
                if el:
                    el.screenshot(path=os.path.join(papka_snimkov, "%s.png" % sid))
        br.close()
    return dannye


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--baza", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--variant", required=True, help="l,d,z,s,o через запятую")
    p.add_argument("--snimki", default="", help="id слайдов через запятую")
    a = p.parse_args()
    l, d, z, s, o = a.variant.split(",")
    v = dict(l=l, d=d, z=z, s=s, o=o)
    css = shema.overlay(v)
    os.makedirs(a.out_dir, exist_ok=True)
    html = sobrat(a.baza, css, os.path.join(a.out_dir, "%s.html" % shema.imya(v)))
    dannye = snyat(html, [x for x in a.snimki.split(",") if x],
                   os.path.join(a.out_dir, "snimki", shema.imya(v)))
    print(json.dumps(dannye, ensure_ascii=False)[:400])
    print("слайдов измерено:", len(dannye))


if __name__ == "__main__":
    main()
