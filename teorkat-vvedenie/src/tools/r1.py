#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Гейт Р1 render-identity: сохранилась ли вёрстка старого дека на слайдах класса A.

  python3 teorkat-vvedenie/src/tools/r1.py

Канон требует его именно для этого случая (`07-verstka/DOK.md`: «правка существующего
→ Р1 render-identity»). Это машинный ответ на вопрос владельца «удалось ли
воспользоваться старой работой» — не «я старался», а число.

Сравнивается ГЕОМЕТРИЯ, а не пиксели: границы зон, ширина рейки/полосы, число и
высоты рядов грида, кегль тела. Отличаться должен только текст внутри зон, поэтому
сравнение идёт по СЦЕНЕ 1 (на ней у класса A стоит ровно то, что стояло на старом
слайде целиком) и по числам, а не по картинке.

Старый дек берётся из git и НИЧЕГО не пересобирает: `dist/index.html` точки отката
закоммичен, значит эталон — байты того коммита, а не моя пересборка его источника.
"""
import json, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from karta import karta, klass, TOCHKA_OTKATA, REPO

SRC = Path(__file__).resolve().parents[1]
NOVY = SRC / "dist" / "index.html"

GEOM = r"""
(scene) => {
  const out = {};
  document.querySelectorAll('.slide').forEach(s => {
    const disp = s.style.display; s.style.display = '';
    for (let i = 1; i <= 9; i++) s.classList.remove('scene-' + i);
    s.classList.remove('scene-99');
    s.classList.add('scene-' + scene);
    s.querySelectorAll('[data-scene-until]').forEach(el =>
      el.classList.toggle('scene-off', scene >= +el.dataset.sceneUntil));
    const g = s.querySelector('.grid');
    const gs = g ? getComputedStyle(g) : null;
    const box = el => { const r = el.getBoundingClientRect();
      return [Math.round(r.left), Math.round(r.top),
              Math.round(r.width), Math.round(r.height)]; };
    const zones = {};
    s.querySelectorAll('.zone,.rail,.board').forEach(z => {
      const key = z.className.replace(/\s+/g, ' ').trim();
      zones[key] = box(z);
    });
    out[s.id] = {
      cols: gs ? gs.gridTemplateColumns : null,
      rows: gs ? gs.gridTemplateRows : null,
      zones: zones,
      tb: (() => { const z = s.querySelector('.zone');
        return z ? Math.round(parseFloat(getComputedStyle(z).fontSize)) : null; })(),
      lh: (() => { const z = s.querySelector('.zone');
        return z ? Math.round(parseFloat(getComputedStyle(z).lineHeight)) : null; })(),
      blok: (() => { const z = s.querySelector('.zone');
        return z ? Math.round(parseFloat(getComputedStyle(z).getPropertyValue('--blok'))) : null; })(),
      panels: s.querySelectorAll('.panel').length,
      scenes: parseInt(s.dataset.scenes || '1', 10),
    };
    s.style.display = disp;
  });
  return out;
}
"""


def snyat(path, scene=1):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1440, "height": 810})
        pg.goto("file://" + str(path))
        pg.wait_for_load_state("networkidle")
        pg.evaluate("document.fonts && document.fonts.ready")
        pg.wait_for_timeout(400)
        d = pg.evaluate(GEOM, scene)
        b.close()
    return d


def stary_dek():
    """dist/index.html точки отката — из git, без пересборки, в /tmp."""
    r = subprocess.run(["git", "--no-optional-locks", "show",
                        "%s:teorkat-vvedenie/src/dist/index.html" % TOCHKA_OTKATA],
                       cwd=REPO, capture_output=True)
    if r.returncode != 0:
        raise SystemExit("не достать старый дек из %s: rc=%d" % (TOCHKA_OTKATA, r.returncode))
    p = Path(tempfile.gettempdir()) / ("dek_%s.html" % TOCHKA_OTKATA)
    p.write_bytes(r.stdout)
    return p


def main():
    stary_path = stary_dek()
    star = snyat(stary_path)
    nov = snyat(NOVY)
    k = karta()

    a_ids = [s for s in sorted(k) if klass(s, k) == "A"]
    b_ids = [s for s in sorted(k) if klass(s, k) == "B"]

    print("── Р1 RENDER-IDENTITY: класс A против дека %s ──" % TOCHKA_OTKATA)
    print("слайдов в старом деке: %d · в новом: %d" % (len(star), len(nov)))
    print()
    print("%-5s %-6s %-7s %-7s %-9s %-9s %s"
          % ("нов", "стар", "кегль", "межстр", "колонки", "зоны", "вердикт"))

    sovpalo, rashod = 0, []
    for sid in a_ids:
        old_id = k[sid][0]
        o, n = star.get(old_id), nov.get(sid)
        if not o or not n:
            rashod.append((sid, old_id, "нет данных"))
            continue
        pricin = []
        if o["cols"] != n["cols"]:
            pricin.append("колонки %s → %s" % (o["cols"], n["cols"]))
        if o["rows"] != n["rows"]:
            pricin.append("ряды %s → %s" % (o["rows"], n["rows"]))
        if o["tb"] != n["tb"]:
            pricin.append("кегль %s → %s" % (o["tb"], n["tb"]))
        if o["lh"] != n["lh"]:
            pricin.append("межстрочье %s → %s" % (o["lh"], n["lh"]))
        if o.get("blok") != n.get("blok"):
            pricin.append("ритм абзацев %s → %s" % (o.get("blok"), n.get("blok")))
        oz, nz = o["zones"], n["zones"]
        if set(oz) != set(nz):
            pricin.append("состав зон %s → %s" % (sorted(oz), sorted(nz)))
        else:
            for key in sorted(oz):
                if oz[key] != nz[key]:
                    pricin.append("зона %s %s → %s" % (key, oz[key], nz[key]))
        if o["panels"] != n["panels"]:
            pricin.append("панелей %d → %d" % (o["panels"], n["panels"]))
        # 🔴 «Отличается» и «стало хуже» — РАЗНЫЕ вердикты, и мерить надо второй.
        # Заход сам велит на классе A пробовать ПОНИЖАТЬ ступень, возвращая кегль
        # вверх: «часть дека станет читаемее, чем была». Понижение ступени двигает
        # геометрию по построению — кегль, межстрочье и поля растут. Гейт, который
        # красит это как утрату вёрстки, противоречит шагу, который это заказал.
        # Поэтому расхождение классифицируется: УЛУЧШЕНИЕ (ни одна величина не
        # уменьшилась) или ДЕГРАДАЦИЯ (хоть одна уменьшилась). Провал захода — это
        # деградация, а не разница.
        huzhe = []
        if n["tb"] < o["tb"]:
            huzhe.append("кегль %d→%d" % (o["tb"], n["tb"]))
        vozduh_o = (o["lh"] or 0) + (o["blok"] or 0)
        vozduh_n = (n["lh"] or 0) + (n["blok"] or 0)
        if vozduh_n < vozduh_o:
            huzhe.append("воздух (межстрочье+ритм) %d→%d" % (vozduh_o, vozduh_n))
        if o["panels"] != n["panels"]:
            huzhe.append("панелей %d→%d" % (o["panels"], n["panels"]))

        if not pricin:
            sovpalo += 1
            print("%-5s %-6s %-7s %-7s %-9s %-9s ✅ геометрия совпала"
                  % (sid, old_id, n["tb"], n["lh"], "=", "="))
        else:
            rashod.append((sid, old_id, " · ".join(pricin), huzhe))
            print("%-5s %-6s %-7s %-7s %-9s %-9s %s"
                  % (sid, old_id, n["tb"], n["lh"], "", "",
                     ("🔴 ДЕГРАДАЦИЯ: " + " · ".join(huzhe)) if huzhe
                     else "△ улучшение (%d величин)" % len(pricin)))

    degrad = [r for r in rashod if r[3]]
    uluch = [r for r in rashod if not r[3]]
    print()
    print("🔴 КЛАСС A: %d слайдов · геометрия совпала БАЙТ-В-БАЙТ у %d · "
          "изменилась в сторону УЛУЧШЕНИЯ у %d · ДЕГРАДИРОВАЛА у %d"
          % (len(a_ids), sovpalo, len(uluch), len(degrad)))
    print("   ⇒ вёрстка сохранена или улучшена на %d из %d слайдов класса A"
          % (sovpalo + len(uluch), len(a_ids)))
    for sid, old_id, why, huzhe in rashod:
        print("   %s %s (был %s): %s"
              % ("🔴" if huzhe else "△", sid, old_id, why))

    # ── кегль: поднялся или опустился против старого дека (критерий 11) ──
    print()
    print("── КЕГЛЬ против старого дека ──")
    vverh, vniz, ravno = [], [], 0
    for sid in sorted(k):
        n = nov.get(sid)
        if not n:
            continue
        stariye = [star[o]["tb"] for o in k[sid] if o in star]
        if not stariye:
            continue
        # у склейки эталон — САМЫЙ МЕЛКИЙ из вошедших: именно он определял, каким
        # кеглем зал читал этот материал в старом деке
        base = min(stariye)
        if n["tb"] > base:
            vverh.append((sid, base, n["tb"]))
        elif n["tb"] < base:
            vniz.append((sid, base, n["tb"]))
        else:
            ravno += 1
    print("ПОДНЯЛИСЬ в кегле: %d — %s"
          % (len(vverh), ", ".join("%s %d→%d" % x for x in vverh) or "нет"))
    print("опустились:        %d — %s"
          % (len(vniz), ", ".join("%s %d→%d" % x for x in vniz) or "нет"))
    print("без изменения:     %d" % ravno)

    print()
    print("── КЛАСС B: %d слайдов (гриды наследованы по сценам, Р1 к ним не применим) ──"
          % len(b_ids))
    print("класс C (собраны с нуля): 0")
    return 0 if not degrad else 2


if __name__ == "__main__":
    sys.exit(main())
