#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Измеритель вмещения + солвер (Э2/Э3 захода solver-vmeshcheniya).

Ядро задачи: текст должен помещаться в зону без обрезки, а генератор — сам
подбирать под это кегль/межстрочье/отступ блока, вместо ручной подгонки (88
CSS-правил на дек в `teorkat-vvedenie`, ради ухода от которой всё затевается).

Помещается или нет — знает только браузер (метрики шрифта, разрывы строк,
высота формул), питон сам не вычислит. Поднимать браузер на каждую пробу
дорого, поэтому браузер стартует ОДИН раз на слайд, а весь перебор идёт
ВНУТРИ страницы на JS — один `page.evaluate()` возвращает и решение, и трассу
всех проб (для отчёта: сколько проб понадобилось).

  python3 _generator/sborka/vmeshchenie.py <slide.html>            # разовый промер дефолтов
  python3 _generator/sborka/vmeshchenie.py <slide.html> --podobrat  # солвер, печатает решение

Ручки (Я1, дословно из тела этого захода — раздел ПЛАН ФАЗЫ 4 в
OTKRYTYE-ZADACHI.md не существует на диске, проверено грепом; работаю по
числам, названным в самом заходе): кегль слайда (пол 35px — canon
`podgonka.kegl_dlya_znakov`/`sverstat.py:FLOOR_PX`, потолок 38px — token
`--t-body`), межстрочье `--lh` (1.24–1.44), отступ блока `--blok` (14–20px).

🔴 Гранулярность — ОДИН триплет (кегль, lh, blok) НА СЛАЙД, не на блок. Я1
называет «отступ после блока» ручкой БЛОКА, но без текста Я1 нет схемы
пер-блочного CSS-scope и нет обоснования, что общего значения на слайд
недостаточно (переполнение s08 — зоны целиком, не одного блока). Сознательное
сужение объёма при недостающем Я1 — см. отчёт захода.

🔴 «Ступени» (RUNGI ниже) — МОЯ интерполяция между canon-дефолтом
(lh=1.5278, blok=26 — teorkat-vvedenie/src/tokens.css + overlay.css) и полом
диапазона, названного заходом (lh=1.24, blok=14), НЕ копия чужой таблицы:
`sverstat.py:STUPENI` в teorkat-vvedenie сцепляет lh/blok/margins/боковую
полосу — тех рычагов (margins, ширина иллюстрации) этот заход не касается, и
портировать чужую таблицу один-в-один означало бы тащить лишние переменные.
"""
import argparse
import json
import re
import sys
from pathlib import Path

GENERATOR = Path(__file__).resolve().parents[1]

KEGL_FLOOR = 35
KEGL_DEFAULT = 38
FILL_LO, FILL_HI = 75, 90

# (lh, blok, потолок_кегля) — от canon-дефолта к полу диапазона захода, роомиест
# первым. Потолок кегля сужается вместе с рангом (тот же принцип, что в
# sverstat.STUPENI: чем туже ритм, тем ниже разумный потолок шрифта).
RUNGI = [
    (1.5278, 26, KEGL_DEFAULT),  # 0 — canon-дефолт как есть
    (1.44, 22, KEGL_DEFAULT),    # 1
    (1.38, 20, 37),              # 2
    (1.32, 18, 36),              # 3
    (1.28, 16, 35),              # 4
    (1.24, 14, 35),              # 5 — пол диапазона захода
]

# `liniya` (доля слайда под текст у polosa_gorizontalnaya/polosa_vertikalnaya) —
# ручка СЛАЙДА (Я1, дословно в теле захода: «Ручки — у слайда: liniya, кегль по
# умолчанию, межстрочье по умолчанию»). Найдено живым прогоном на s08: без неё
# солвер честно отказывает даже на самом тугом ранге (кегль=пол, lh=пол, blok=пол
# всё равно даёт 113% заполнения) — а рост liniya на несколько пунктов даёт зоне
# текста больше высоты БЕСПЛАТНО, раньше, чем жертвовать кеглем. Кандидаты — от
# авторского значения вверх, самый маленький прирост испробован первым.
LINIYA_STEPS = (0, 6, 12, 18, 24)
LINIYA_MAX = 92

# JS выполняется ОДИН раз на слайд (page.evaluate), сам гоняет перебор внутри
# страницы — без единого лишнего похода питон↔браузер на пробу.
_JS_SOLVE = r"""
(cfg) => {
  const zone = document.querySelector('.zone.t-body') || document.querySelector('.t-body');
  if (!zone) return {error: 'зона .zone.t-body не найдена на слайде'};
  const slide = document.querySelector('.slide');
  // раскрыть ФИНАЛЬНУЮ сцену — худший случай по заполнению (сцены только
  // добавляют содержимое, engine.js: applyScene/scenesOf уже в странице).
  // (На практике [data-scene-from] прячется через visibility, не display, —
  // место в потоке зарезервировано и на скрытой сцене, но раскрытие — явное
  // условие Э2 захода, оставляю для честности промера.)
  if (slide && typeof applyScene === 'function' && typeof scenesOf === 'function') {
    applyScene(slide, scenesOf(slide));
  }
  const grid = document.querySelector('.grid');
  const trials = [];
  // capPct — порог, который считается «влезло» ДЛЯ ПОИСКА (не для факта
  // обрезки — тот всегда fill<=100, пишется отдельно как `clipped`). Два
  // прохода снаружи: сперва capPct=90 (целевая полоса Э3), и только если
  // НИГДЕ во всей сетке не нашлось — capPct=100 (честно влезает, но без
  // запаса; лучше так, чем отказ на пустом месте).
  function measure(kegl, lh, blok, liniya, capPct) {
    zone.style.setProperty('--t-body', kegl + 'px');
    zone.style.setProperty('--lh', String(lh));
    zone.style.setProperty('--blok', blok + 'px');
    if (grid && liniya != null) grid.style.setProperty('--liniya', liniya + '%');
    const sh = zone.scrollHeight, ch = zone.clientHeight;
    const fill = ch ? (100 * sh / ch) : null;
    const rec = {kegl: kegl, lh: lh, blok: blok, liniya: liniya,
                 scrollHeight: sh, clientHeight: ch,
                 clipped: sh > ch, fill: fill, fits: fill != null && fill <= capPct};
    trials.push(rec);
    return rec;
  }
  // бинарный поиск максимального влезающего (в смысле capPct) кегля в
  // [floor, ceil] при (lh, blok, liniya). Монотонность (Э3 захода): меньше
  // кегль — заполнение не хуже. iters проб.
  function maxKegl(floor, ceil, lh, blok, liniya, iters, capPct) {
    const top = measure(ceil, lh, blok, liniya, capPct);
    if (top.fits) return top;                 // потолок ранга уже в пределах capPct — он и максимум
    const bot = measure(floor, lh, blok, liniya, capPct);
    if (!bot.fits) return null;                // даже пол ранга не укладывается в capPct
    let lo = floor, hi = ceil, best = bot;
    for (let i = 0; i < iters; i++) {
      const mid = (lo + hi) / 2;
      const r = measure(mid, lh, blok, liniya, capPct);
      if (r.fits) { best = r; lo = mid; } else { hi = mid; }
    }
    return best;
  }
  // авторское liniya слайда — читаю с самого элемента (inline `--liniya`, tipy.py),
  // а не из cfg: у типов без грида (polnyj_ekran/tolko_tekst) переменной нет вовсе.
  let liniyaBase = null;
  if (grid) {
    const raw = getComputedStyle(grid).getPropertyValue('--liniya').trim();
    const v = parseFloat(raw);
    if (isFinite(v)) liniyaBase = v;
  }
  const liniyaCandidates = liniyaBase == null ? [null]
    : cfg.liniya_steps.map(d => Math.min(cfg.liniya_max, liniyaBase + d));
  // Целевая функция (Э3 захода, дословно): среди влезающих — самый крупный
  // кегль; при равном кегле — заполнение ближе к середине полосы; при
  // равенстве и этого — минимальный прирост liniya (меньше отъедено у
  // иллюстрации). НЕ останавливаюсь на первом влезшем варианте — перебираю
  // всю сетку (liniya × ранг), она мала, проба дёшева (Э2: доли мс).
  function luchshe(a, b) {
    if (!b) return true;
    if (a.kegl !== b.kegl) return a.kegl > b.kegl;
    const da = Math.abs(a.fill - 82.5), db = Math.abs(b.fill - 82.5);
    if (da !== db) return da < db;
    return (a.liniya || 0) < (b.liniya || 0);
  }
  function poisk(capPct) {
    let best = null;
    for (const liniya of liniyaCandidates) {
      for (const [lh, blok, ceil] of cfg.rungi) {
        const cand = maxKegl(cfg.kegl_floor, ceil, lh, blok, liniya, cfg.iters, capPct);
        if (cand && luchshe(cand, best)) best = cand;
      }
    }
    return best;
  }
  let best = poisk(cfg.fill_hi);          // проход 1: целевая полоса (≤90%)
  let otstuplenie = false;
  if (!best) { best = poisk(100); otstuplenie = true; }  // проход 2: честно влезает, без запаса
  return {trials: trials, best: best, liniya_base: liniyaBase, otstuplenie: otstuplenie};
}
"""


def podobrat(page, html_path, iters=6, rungi=None, liniya_steps=None, liniya_max=LINIYA_MAX):
    """Один слайд (уже скомпилированный `slaid.py`-HTML) → решение солвера.
    Один `page.goto` + один `page.evaluate` — весь перебор внутри браузера."""
    from urllib.parse import quote
    url = "file://" + quote(str(Path(html_path).resolve()))
    page.goto(url)
    page.wait_for_timeout(120)  # шрифты/раскладка устаканились
    cfg = {"kegl_floor": KEGL_FLOOR, "iters": iters, "fill_hi": FILL_HI,
           "rungi": rungi if rungi is not None else RUNGI,
           "liniya_steps": list(liniya_steps if liniya_steps is not None else LINIYA_STEPS),
           "liniya_max": liniya_max}
    result = page.evaluate(_JS_SOLVE, cfg)
    if result.get("error"):
        raise RuntimeError(result["error"])
    return result  # {"trials", "best": {...}|None, "liniya_base", "otstuplenie": bool}


def izmerit(page, html_path, kegl=None, lh=None, blok=None):
    """Разовый промер (без перебора) — текущий/заданный триплет → влезло или нет."""
    from urllib.parse import quote
    url = "file://" + quote(str(Path(html_path).resolve()))
    page.goto(url)
    page.wait_for_timeout(120)
    js = r"""
    (c) => {
      const zone = document.querySelector('.zone.t-body') || document.querySelector('.t-body');
      if (!zone) return {error: 'зона .zone.t-body не найдена на слайде'};
      const slide = document.querySelector('.slide');
      if (slide && typeof applyScene === 'function' && typeof scenesOf === 'function') {
        applyScene(slide, scenesOf(slide));
      }
      if (c.kegl != null) zone.style.setProperty('--t-body', c.kegl + 'px');
      if (c.lh != null) zone.style.setProperty('--lh', String(c.lh));
      if (c.blok != null) zone.style.setProperty('--blok', c.blok + 'px');
      const sh = zone.scrollHeight, ch = zone.clientHeight;
      return {scrollHeight: sh, clientHeight: ch, fits: sh <= ch,
              fill: ch ? (100 * sh / ch) : null};
    }
    """
    r = page.evaluate(js, {"kegl": kegl, "lh": lh, "blok": blok})
    if r.get("error"):
        raise RuntimeError(r["error"])
    return r


def apply_to_card(slide_md_path, best):
    """Решение солвера → карточка слайда (`slaid.md`): дописывает/заменяет поля
    `liniya`, `kegl_px`, `mezhstrochye`, `otstup_bloka` в YAML-шапке (диалект
    `formaty.parse_front_matter`: `key: value`, по строке). Правит ТОЛЬКО эти
    четыре строки, остального не касается — solver применяет решение, не
    переписывает карточку."""
    p = Path(slide_md_path)
    text = p.read_text(encoding="utf-8")
    new_fields = {
        "kegl_px": round(best["kegl"], 2),
        "mezhstrochye": round(best["lh"], 4),
        "otstup_bloka": round(best["blok"], 1),
    }
    if best.get("liniya") is not None:
        new_fields["liniya"] = round(best["liniya"], 2)
    lines = text.split("\n")
    seen = set()
    out = []
    in_head = False
    head_dashes = 0
    for line in lines:
        if line.strip() == "---":
            head_dashes += 1
            in_head = head_dashes == 1
            out.append(line)
            if head_dashes == 2:
                # закрывающая граница шапки — дописать недостающие поля перед ней
                for k, v in new_fields.items():
                    if k not in seen:
                        out.insert(len(out) - 1, "%s: %s" % (k, v))
                in_head = False
            continue
        if in_head:
            m = re.match(r"^([A-Za-z_]+):", line)
            if m and m.group(1) in new_fields:
                k = m.group(1)
                out.append("%s: %s" % (k, new_fields[k]))
                seen.add(k)
                continue
        out.append(line)
    p.write_text("\n".join(out), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Измеритель/солвер вмещения (Э2/Э3 захода solver-vmeshcheniya)")
    ap.add_argument("html", help="путь к скомпилированному HTML одного слайда (slaid.py -o ...)")
    ap.add_argument("--podobrat", action="store_true", help="прогнать солвер (иначе — промер дефолтов)")
    ap.add_argument("--iters", type=int, default=6, help="итераций бинарного поиска на ранг (default 6)")
    ap.add_argument("--primenit", metavar="SLAID_MD",
                     help="решение солвера записать в карточку по этому пути (только с --podobrat)")
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        page = b.new_page(viewport={"width": 1440, "height": 810}, device_scale_factor=1)
        if args.podobrat:
            res = podobrat(page, args.html, iters=args.iters)
            print(json.dumps(res, ensure_ascii=False, indent=2))
            if res["best"] is None:
                # лучшая (наименьшее заполнение) проба всей трассы — сколько не влезло даже там
                худшая_подгонка = min((t for t in res["trials"] if t["fill"] is not None),
                                       key=lambda t: t["fill"], default=None)
                print("ОТКАЗ: не сошлось даже на минимуме (пол кегля %dpx, самый тугой ранг %s, liniya до %s%%). "
                      "Лучшая проба всё равно даёт заполнение %.1f%% (нужно ≤100%%) — "
                      "не влезает %.1f%% высоты зоны."
                      % (KEGL_FLOOR, RUNGI[-1], LINIYA_MAX,
                         худшая_подгонка["fill"] if худшая_подгонка else float("nan"),
                         (худшая_подгонка["fill"] - 100) if худшая_подгонка else float("nan")),
                      file=sys.stderr)
                b.close()
                return 1
            if args.primenit:
                apply_to_card(args.primenit, res["best"])
                print("применено в карточку: %s" % args.primenit, file=sys.stderr)
        else:
            res = izmerit(page, args.html)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        b.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
