#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Гейты сцен 1–6 (заход, шаг 4) плюс главный смысловой гейт 1а — все машинно.

  python3 teorkat-vvedenie/src/tools/sceny_gejt.py

Мерится ВИДИМОСТЬ В БРАУЗЕРЕ, а не разметка в md. Это принципиально: между тегом
`{@N-M}` и тем, что зал видит, стоят три слоя (генератор → каскад overlay → движок),
и заход этого захода начался именно с того, что 79 из 83 тегов замены не показывали
ничего — при валидном html и зелёных гейтах. Разметку проверять бессмысленно;
проверять надо пиксели.

Что считается:
  1. пустых сцен нет           — каждый клик меняет множество видимого
  2. последняя ≠ первой        — и отдельно 1а: последняя ВКЛЮЧАЕТ первую
  3. интервалы видимости связны — элемент не исчезает и не появляется снова (моргание)
  4. синхронность текст+картинка — transition-delay у панелей и формул равен 0
  5. связка вне блюра           — `.fill` со вторым ребёнком (в этом деке `.fill` нет)
  6. геометрия между сценами    — на сколько сдвигается текст, видимый в обеих сценах
"""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

SRC = Path(__file__).resolve().parents[1]
DECK = SRC / "dist" / "index.html"

JS = r"""
() => {
  const out = {};
  document.querySelectorAll('.slide').forEach(s => {
    const n = parseInt(s.dataset.scenes || '1', 10) || 1;
    const disp = s.style.display; s.style.display = '';
    // все смысловые элементы слайда: абзацы/списки текста и панели иллюстраций
    const els = [...s.querySelectorAll('.zone p, .zone ul, .panel')];
    els.forEach((e, i) => e.dataset.gi = i);
    const kadry = [];
    for (let k = 1; k <= n; k++) {
      for (let i = 1; i <= 9; i++) s.classList.remove('scene-' + i);
      s.classList.remove('scene-99');
      s.classList.add('scene-' + k);
      // ДОСЛОВНО как движок (engine.js:57)
      s.querySelectorAll('[data-scene-until]').forEach(el =>
        el.classList.toggle('scene-off', k >= +el.dataset.sceneUntil));
      const vid = [];
      els.forEach((e, i) => {
        const cs = getComputedStyle(e);
        const r = e.getBoundingClientRect();
        const visible = cs.display !== 'none' && cs.visibility !== 'hidden'
                        && parseFloat(cs.opacity) > 0.01 && r.width > 0 && r.height > 0;
        if (visible) vid.push({i: i, box: [Math.round(r.left), Math.round(r.top),
                                           Math.round(r.width), Math.round(r.height)],
                               panel: e.classList.contains('panel')});
      });
      kadry.push(vid);
    }
    for (let i = 1; i <= 9; i++) s.classList.remove('scene-' + i);
    s.classList.add('scene-1');
    s.querySelectorAll('[data-scene-until]').forEach(el =>
      el.classList.toggle('scene-off', 1 >= +el.dataset.sceneUntil));
    s.style.display = disp;
    out[s.id] = {
      n: n, kadry: kadry, vsego: els.length,
      // синхронность: задержка перехода у панелей и формул обязана быть нулевой
      delay: [...s.querySelectorAll('.panel[data-scene-from],.formula[data-scene-from]')]
             .map(e => getComputedStyle(e).transitionDelay),
      // связка вне блюра: .fill обязан иметь ровно одного ребёнка-обёртку
      fill: [...s.querySelectorAll('.fill')].map(e => e.children.length),
    };
  });
  return out;
}
"""


def main():
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1440, "height": 810})
        pg.goto("file://" + str(DECK))
        pg.wait_for_load_state("networkidle")
        pg.evaluate("document.fonts && document.fonts.ready")
        pg.wait_for_timeout(500)
        # 🔴 Переходы ОБЯЗАНЫ быть выключены до замера. Канон-раскрытие идёт через
        # `opacity` с `transition:.24s` (`base.css:32`), и `getComputedStyle`,
        # прочитанный сразу после смены класса сцены, возвращает ЕЩЁ НЕ доехавшее
        # значение — opacity 0 при visibility:visible. Первый прогон этого гейта на
        # том и попался: 16 «пустых сцен» и 8 «откатов на первую» нашлись ровно на
        # тех 10 слайдах, что держат канон (у слайдов с перетеканием меняется
        # `display`, он мгновенный, и артефакт их не касался). То есть гейт
        # диагностировал собственную спешку как брак дека.
        pg.add_style_tag(content="*,*::before,*::after{transition:none!important;"
                                 "animation:none!important}")
        pg.wait_for_timeout(150)
        data = pg.evaluate(JS)
        b.close()

    so_scenami = {k: v for k, v in data.items() if v["n"] > 1}
    kadrov = sum(v["n"] for v in data.values())

    pustye, otkat, nevkl, razryv, sdvig, delay_bad, fill_bad = [], [], [], [], [], [], []

    for sid, v in sorted(data.items()):
        n, kadry = v["n"], v["kadry"]
        mn = [set(x["i"] for x in kadr) for kadr in kadry]
        panels = {x["i"] for kadr in kadry for x in kadr if x["panel"]}

        # [1] пустых сцен нет
        for k in range(1, n):
            if mn[k] == mn[k - 1]:
                pustye.append("%s сцена %d→%d" % (sid, k, k + 1))

        # [2] последняя ≠ первой
        if n > 1 and mn[-1] == mn[0]:
            otkat.append(sid)

        # [1а] последняя ВКЛЮЧАЕТ первую, за вычетом сменного яруса (панели)
        if n > 1:
            propalo = (mn[0] - mn[-1]) - panels
            if propalo:
                znakov = sum(x["box"][2] * x["box"][3] for x in kadry[0]
                             if x["i"] in propalo)
                nevkl.append((sid, len(propalo), znakov))

        # [3] интервалы видимости связны
        for i in range(v["vsego"]):
            sc = [k + 1 for k in range(n) if i in mn[k]]
            if sc and sc != list(range(sc[0], sc[-1] + 1)):
                razryv.append("%s элемент %d виден в сценах %s" % (sid, i, sc))

        # [6] геометрия: сдвиг элементов, видимых в обеих соседних сценах
        for k in range(1, n):
            a = {x["i"]: x["box"] for x in kadry[k - 1] if not x["panel"]}
            bb = {x["i"]: x["box"] for x in kadry[k] if not x["panel"]}
            dv = [abs(a[i][1] - bb[i][1]) for i in set(a) & set(bb)
                  if abs(a[i][1] - bb[i][1]) > 1]
            if dv:
                sdvig.append((sid, k, k + 1, len(dv), max(dv)))

        # [4] синхронность
        for d in v["delay"]:
            if d not in ("0s", "0"):
                delay_bad.append("%s delay=%s" % (sid, d))
        # [5] связка вне блюра
        for c in v["fill"]:
            if c != 1:
                fill_bad.append("%s .fill детей=%d" % (sid, c))

    print("── ГЕЙТЫ СЦЕН ──")
    print("слайдов: %d · со сценами (>1): %d · кадров всего: %d"
          % (len(data), len(so_scenami), kadrov))
    print("максимум data-scenes по деку: %d" % max(v["n"] for v in data.values()))
    print()
    print("1. пустых сцен (клик ничего не меняет):        %d %s"
          % (len(pustye), pustye or ""))
    print("2. «последняя = первой» (откат):                %d %s"
          % (len(otkat), otkat or ""))
    print("3. разрывных интервалов видимости (моргание):   %d %s"
          % (len(razryv), razryv[:6] or ""))
    print("4. панелей/формул с ненулевой задержкой:        %d %s"
          % (len(delay_bad), delay_bad[:3] or ""))
    print("5. `.fill` со вторым ребёнком:                  %d %s"
          % (len(fill_bad), fill_bad or "(в деке .fill нет)"))
    print()
    print("1а. 🔴 ГЛАВНЫЙ СМЫСЛОВОЙ ГЕЙТ — финальная сцена ПОЛНЕЕ первой")
    print("    слайдов, где текст первой сцены НЕ доехал до финальной: %d из %d"
          % (len(nevkl), len(so_scenami)))
    for sid, cnt, pl in sorted(nevkl, key=lambda x: -x[1]):
        print("    %s: ушло блоков %d (площадь %d px²)" % (sid, cnt, pl))
    print()
    print("6. ГЕОМЕТРИЯ между сценами (сдвиг текста, видимого в обеих):")
    print("    переходов со сдвигом: %d из %d" % (len(sdvig), kadrov - len(data)))
    for sid, a, bq, cnt, mx in sorted(sdvig, key=lambda x: -x[4])[:12]:
        print("    %s %d→%d: сдвинулось %d блоков, максимум %dpx" % (sid, a, bq, cnt, mx))

    plohо = len(pustye) + len(otkat) + len(razryv) + len(delay_bad) + len(fill_bad)
    print()
    print("гейты 1–5: %s" % ("✅ все зелёные" if not plohо else "❌ %d нарушений" % plohо))
    return 0 if not plohо else 2


if __name__ == "__main__":
    sys.exit(main())
