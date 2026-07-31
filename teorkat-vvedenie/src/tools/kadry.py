#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Снять КАЖДУЮ СЦЕНУ каждого слайда в PNG — вход в зрительную петлю (заход, шаг 5).

  python3 teorkat-vvedenie/src/tools/kadry.py [outdir]

Почему свой, а не `_generator/render.py`: тот снимает кадр как `?only=N&scene=99`,
то есть один кадр на слайд и в состоянии «сцена 99». Для этого дека оба решения
негодны:

  · один кадр на слайд слеп по построению — заход прямо: «смотреть надо каждый слайд
    в КАЖДОЙ сцене, именно между сценами живут моргание, отставание картинки и
    совпадение последней с первой»;
  · «сцена 99» НЕ РАВНА финальной сцене слайда, когда на слайде есть ЗАМЕНА: при
    `k=99` гаснет всё, у чего есть `data-scene-until`, включая блок, который на своей
    последней сцене (`{@4-5}` при пяти сценах) обязан стоять. То есть кадр «99» —
    это состояние, которого зал не увидит НИКОГДА.

Поэтому сцены ставятся классом напрямую, ровно как их ставит движок (`engine.js`
`applyScene`), включая толкование `scene-off` по условию `k >= until`. Имя файла —
`sNN-cK.png`, чтобы порядок просмотра совпадал с порядком показа.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

SRC = Path(__file__).resolve().parents[1]
DECK = SRC / "dist" / "index.html"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/kadry-l1")

SETUP = r"""
() => {
  // движок сам прячет неактивные слайды и масштабирует активный; для съёмки нам
  // нужен слайд в натуральную величину и без чужих поверх
  document.querySelectorAll('.slide').forEach(s => {
    s.style.display = 'none';
    s.style.transform = 'none';
    // 🔴 `position` НЕ трогать. `.grid` внутри слайда — `position:absolute;inset:0`,
    // и его якорь — сам слайд (`.slide{position:relative}`, base.css:5). Первая
    // версия ставила слайду `position:static`, грид отрывался от слайда и уезжал по
    // ближайшему позиционированному предку: на кадре s13-c4 нижний абзац оказался
    // обрезан ПОСЕРЕДИНЕ СТРОКИ, при промере 0 переполнений. То есть дефект был в
    // съёмке, а выглядел как дефект вёрстки — ровно тот случай, когда «посмотрел
    // глазами» врёт в обратную сторону.
  });
  // 🔴 `#stage` НЕ переконфигурировать. Он `display:grid;place-items:center`
  // (base.css:4), и слайды лежат в ОДНОЙ ячейке грида друг на друге. Первая версия
  // переводила его в `display:block`, и это меняло перенос строк: та же зона той же
  // ширины давала контент на 11px выше, чем в конфигурации движка. На кадре s13-c4
  // из-за этого нижний абзац выходил за слайд, а `promer.py` — который мерит В
  // КОНФИГУРАЦИИ ДВИЖКА — честно показывал 0. Расхождение съёмки с промером опаснее
  // обоих по отдельности: одно из двух чисел заведомо врёт, а какое — не видно.
  // Теперь съёмка и промер стоят в одной конфигурации по построению.
  return [...document.querySelectorAll('.slide')].map(s =>
    [s.id, parseInt(s.dataset.scenes || '1', 10) || 1]);
}
"""

SHOW = r"""
([sid, k]) => {
  document.querySelectorAll('.slide').forEach(s => { s.style.display = 'none'; });
  const s = document.getElementById(sid);
  s.style.display = 'block';
  for (let i = 1; i <= 9; i++) s.classList.remove('scene-' + i);
  s.classList.remove('scene-99');
  s.classList.add('scene-' + k);
  // ДОСЛОВНО как engine.js:57
  s.querySelectorAll('[data-scene-until]').forEach(el =>
    el.classList.toggle('scene-off', k >= +el.dataset.sceneUntil));
}
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.png"):
        old.unlink()
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1440, "height": 810},
                        device_scale_factor=1)
        pg.goto("file://" + str(DECK))
        pg.wait_for_load_state("networkidle")
        pg.evaluate("document.fonts && document.fonts.ready")
        pg.wait_for_timeout(600)
        plan = pg.evaluate(SETUP)
        # переходы выключены: кадр обязан показывать доехавшее состояние, а не
        # середину анимации (на этом же попался гейт сцен)
        pg.add_style_tag(content="*,*::before,*::after{transition:none!important;"
                                 "animation:none!important}")
        # 🔴 ХРОМ ДВИЖКА С КАДРА СНИМАЕТСЯ. `#hint` («← → листать · P — экран · …»)
        # показывается на загрузке классом `.is-shown` и лежит `position:fixed` над
        # слайдом, поэтому попадал на ВСЕ 23 кадра — поверх нижней полосы, ровно там,
        # где у половины слайдов стоит иллюстрация. `_generator/render.py` его гасит
        # (`exportFrame`), а эта петля — нет, и глазная проверка месяц смотрела на
        # надпись, которой в показе на этом месте не бывает. Гейты такого не видят:
        # хром не часть слайда, промер и `sceny_gejt` его не мерят.
        pg.add_style_tag(content="#hint{display:none!important}")
        n = 0
        for sid, scenes in plan:
            for k in range(1, scenes + 1):
                pg.evaluate(SHOW, [sid, k])
                pg.wait_for_timeout(60)
                el = pg.query_selector("#" + sid)
                el.screenshot(path=str(OUT / ("%s-c%d.png" % (sid, k))))
                n += 1
        b.close()
    print("кадров снято: %d (слайдов %d, сумма сцен %d)"
          % (n, len(plan), sum(s for _, s in plan)))
    print("→ %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
