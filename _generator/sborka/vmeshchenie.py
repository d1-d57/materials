#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Измеритель вмещения + солвер (заход solver-v2, перестройка Э1–Э6 поверх
`vmeshchenie.py` захода `solver-vmeshcheniya`).

ПРИЧИНА ПЕРЕСТРОЙКИ (заход solver-v2, дословно): первый солвер давал формально
верный, но некрасивый результат — на `s08` он раздул `liniya` с 74% до 92%,
ужав иллюстрацию до ~8% высоты, потому что минимальный размер иллюстрации был
свободной переменной, а не жёстким ограничением. Здесь — жёстко.

Архитектура не изменилась (один браузер, один `page.evaluate`, весь перебор
внутри страницы — Э5 обоих заходов): меняется, ЧТО именно перебирается и КАК
выбирается победитель.

  python3 _generator/sborka/vmeshchenie.py <slide.html>             # промер дефолтов
  python3 _generator/sborka/vmeshchenie.py <slide.html> --podobrat   # солвер v2
  python3 _generator/sborka/vmeshchenie.py --demo-zony               # Э1: отказ ДО поиска (п.1 критерия)
"""
import argparse
import json
import re
import sys
from pathlib import Path

SBORKA = Path(__file__).resolve().parent
sys.path.insert(0, str(SBORKA))
import korpus  # noqa: E402 — Э2: диапазоны корпуса, вызывается командой, не переписываются руками (KONSTITUCIYA §10)

GENERATOR = SBORKA.parent

KEGL_FLOOR = 35            # canon — podgonka.kegl_dlya_znakov / sverstat.py:FLOOR_PX. Пол обязателен ВСЕГДА (Э1).
KEGL_DEFAULT = 38
BLOK_FLOOR_PX = 4          # px — абсолютная страховка снизу для отступа (Э1 захода solver-v3-dyhanie):
                            # отступ теперь ДОЛЯ кегля (blok_koef), но на самом тугом ряду это не даёт
                            # ему уйти в 0/отрицательное; пол оставлен «как страховку», не как рабочую ручку.
FILL_LO, FILL_HI = 75, 90  # целевая полоса заполнения (Э3, уровень 4)
LINE_LEN_LO, LINE_LEN_HI, LINE_LEN_OPT = 45, 75, 66  # символов в строке (Э3, уровень 3); >80 — никогда
LINE_LEN_HARD_MAX = 80

# ─────────────────────────── Э1: ЖЁСТКИЕ ЗОНЫ ───────────────────────────
# «penalty = +∞, а не большое слагаемое» (Кнут–Пласс, дословно из захода):
# нарушение любой из этих границ отвергает пробу ДО измерения в браузере —
# такие точки solver даже не генерирует (см. `_rungi_from_corpus`/`_liniya_candidates`).
#
# Числа — не переписаны руками «на глаз»: p5/медиана/p95 из корпуса (Э2,
# `korpus.corpus_stats()`, живой перерасчёт по трём shablon.html при каждом
# запуске) раздвинуты запасом 15% от размаха p5–p95 и подрезаны абсолютными
# рельсами (canon-пол, здравый типографский смысл, известный баг). Абсолютные
# рельсы побеждают, если корпус когда-нибудь даст экстремум за пределами
# разумного, — заведомо плохой корпусный выброс не должен расширить жёсткую
# зону солвера.
_MARGIN = 0.15


def _bounds_from_corpus(stat, abs_floor, abs_ceil, min_owner=None, max_owner=None, margin=None):
    """p5/p95 корпуса ± запас (по умолчанию 15%, `margin` переопределяет —
    Э2 захода solver-v3-dyhanie: потолок кегля приглушён margin=0, без
    запаса сверху), объединённый с прикидкой владельца (если дана),
    подрезанный абсолютными рельсами. `stat=None` (нет данных) — работают
    только рельсы/прикидка."""
    margin = _MARGIN if margin is None else margin
    los, his = [abs_floor], [abs_ceil]
    if stat:
        span = max(stat["p95"] - stat["p5"], 0.0)
        los.append(stat["p5"] - margin * span)
        his.append(stat["p95"] + margin * span)
    if min_owner is not None:
        los.append(min_owner)
    if max_owner is not None:
        his.append(max_owner)
    lo = max(abs_floor, min(los[1:]) if len(los) > 1 else abs_floor)
    hi = min(abs_ceil, max(his[1:]) if len(his) > 1 else abs_ceil)
    return round(lo, 2), round(max(hi, lo), 2)


def build_zones(corpus=None):
    """Явный список зон слайда — Э1, п.1 критерия готовности. `corpus=None`
    вызывает `korpus.corpus_stats()` сам (лениво — не на импорте модуля)."""
    c = corpus if corpus is not None else korpus.corpus_stats()
    # Э2 захода solver-v3-dyhanie: потолок кегля приглушён — margin=0 убирает
    # запас 15% СВЕРХУ p95 (было 41.9 при p95=41), запас снизу не трогаем
    # (там и так доминирует abs_floor=KEGL_FLOOR). Контрпримеры sl-circle/
    # sl-plan (человек взял 41 — потолок корпуса) обязаны остаться внутри
    # зоны: p95=41 <= hi, проверено фактом (см. `## ОТЧЁТ`).
    kegl = _bounds_from_corpus(c["кегль_px"], abs_floor=KEGL_FLOOR, abs_ceil=44, margin=0.0)
    lh = _bounds_from_corpus(c["lh_отношение_к_кеглю"], abs_floor=1.05, abs_ceil=1.8,
                              min_owner=1.20, max_owner=1.50)  # Э1: «ожидаемо 1.2–1.5»
    # Э1 захода solver-v3-dyhanie: отступ — ДОЛЯ кегля (`blok_koef`), не
    # независимая px-ручка (тот же приём, что уже даёт `lh`). Потолок ratio —
    # канон-грань 26px (canon-дефолт --blok) / KEGL_FLOOR (пол кегля): при
    # самом мелком допустимом кегле отступ не вправе превысить канон-максимум
    # в px. Абсолютный px-пол (`BLOK_FLOOR_PX`) — отдельная страховка снизу,
    # применяется в JS на фактическом кегле пробы, не здесь.
    # А1 захода dovodka-solvera: margin=0.0 убирает запас 15% СНИЗУ p5 (было
    # 0.15, стало 0.23 по факту корпуса) — тот же приём, каким Э2 предыдущего
    # захода убрал запас СВЕРХУ p95 у kegl. Причина: на пяти слайдах, где
    # раньше не влезало вовсе (`dandelin/s09`, `s09p`, `buffon/sl-circle`,
    # `teorkat-vvedenie/s05`, `s06`), солвер выбирал blok_koef НИЖЕ p25 корпуса
    # (0.634) у всех пяти, а на `s05` — буквально дно зоны (0.15 = сам предел,
    # не что-то между) — проверено фактом (`progon_baza.py --baza 16`), не
    # предположено. Причина механическая: `build_rungi` кладёт на самый тугой
    # ряд ровно `zones["blok_koef"][0]` (см. докстринг `build_rungi`), т.е.
    # запас в зоне — это запас, который солвер реально использует на плотных
    # слайдах, а не подстраховка на случай выброса корпуса.
    blok_koef = _bounds_from_corpus(c["blok_koef_k_keglyu"], abs_floor=0.05,
                                     abs_ceil=round(26 / KEGL_FLOOR, 3), margin=0.0)
    # liniya — ДОЛЯ ТЕКСТА. Горизонтальная: владелец «15–80% широко» + корпус
    # (медиана ≈49%, p95≈69%) согласны в ту же сторону; 82 как потолок —
    # чуть выше корпусного p95, но строго ниже 92 (баг s08, здесь дисквалифицирован).
    liniya_h = _bounds_from_corpus(c["liniya_equiv_horizontal_pct"], abs_floor=15, abs_ceil=85,
                                    min_owner=15, max_owner=82)
    # Вертикальная — здесь ЖИВОЕ РАСХОЖДЕНИЕ с прикидкой владельца (см. ВОПРОСЫ
    # в заходе): владелец предположил liniya УЗКО 15–23% (текст — тонкая
    # полоса), корпус (n=17, p5≈75/медиана≈78/p95≈92) показывает ОБРАТНОЕ —
    # во всех измеренных вертикальных сплитах текст ШИРОКИЙ, иллюстрация/rail
    # — узкая полоса. Жёсткая зона объединяет ОБЕ гипотезы (не выбирает
    # молча одну), мягкий приоритет (Э2/Э3) тянет к корпусной медиане —
    # «похоже на то, что владелец уже признал хорошим» в буквальном смысле.
    liniya_v = _bounds_from_corpus(c["liniya_equiv_vertical_pct"], abs_floor=15, abs_ceil=92,
                                    min_owner=15, max_owner=23)
    return {"kegl": kegl, "lh": lh, "blok_koef": blok_koef,
            "liniya_horizontal": liniya_h, "liniya_vertical": liniya_v}


class ZonaNarushena(Exception):
    pass


def check_zone(zones, name, value):
    lo, hi = zones[name]
    if value is None or not (lo <= value <= hi):
        raise ZonaNarushena(
            "зона '%s': значение %s вне [%s, %s] — отвергнуто ДО поиска (Э1 захода solver-v2)"
            % (name, value, lo, hi))
    return value


def check_liniya_zone(zones, axis, value):
    return check_zone(zones, "liniya_%s" % axis, value)


# ─────────────────────────── Э4: РЕШЁТКА (rungi) ───────────────────────────
def build_rungi(zones, steps=6):
    """(lh, blok_koef, потолок_кегля) от роскошного к тугому — Э4: небольшая
    фиксированная решётка вместо континуума (визуальная стабильность между
    похожими слайдами), построена ИЗ zones (Э1), не захардкожена отдельно.
    `blok_koef` вместо `blok` (Э1 захода solver-v3-dyhanie) — отступ едет
    вместе с кеглем, отдельной px-оси для перебора больше нет."""
    lh_lo, lh_hi = zones["lh"]
    koef_lo, koef_hi = zones["blok_koef"]
    kegl_lo, kegl_hi = zones["kegl"]
    rungi = []
    for i in range(steps):
        t = i / (steps - 1)  # 0 — роскошный (max lh/koef), 1 — тугой (min)
        lh = round(lh_hi - t * (lh_hi - lh_lo), 4)
        koef = round(koef_hi - t * (koef_hi - koef_lo), 4)
        # потолок кегля сужается вместе с рангом — тот же принцип, что в
        # sverstat.STUPENI (чем туже ритм, тем ниже разумный потолок шрифта).
        ceil = round(kegl_hi - t * (kegl_hi - kegl_lo) * 0.4, 1)
        rungi.append((lh, koef, max(ceil, kegl_lo)))
    return rungi


def build_kegl_grid(zones, steps=7):
    """Фиксированная решётка кегля (Э4, «как `fontScale` PowerPoint») —
    визуальная стабильность: два похожих слайда снапятся на ОДНУ и ТУ ЖЕ
    точку, а не разъедутся на 22 против 21 по капризу бинарного поиска
    (критерий готовности 5)."""
    lo, hi = zones["kegl"]
    return [round(lo + (hi - lo) * k / (steps - 1), 2) for k in range(steps)]


# ─────────────────────── Э3: веса мягких (кубических) штрафов ───────────────────────
WEIGHTS = {"liniya": 0.8, "kegl": 0.6, "lh": 0.6, "blok": 0.4, "edge": 0.5, "dyhanie": 0.6}
EPS_KEGL = 1.0        # px — полоса ε на тай-брейке «кегль между похожими» (Э2 захода solver-v3-dyhanie)
EPS_PENALTY = 0.15    # доля от минимального штрафа — полоса ε на уровне «похожесть на корпус»

# Э3 захода solver-v3-dyhanie, «мера дыхания»: доля zone.clientHeight, занятая
# промежутками между соседними блоками (p/ul.tlist верхнего уровня зоны — те
# же элементы, что получают margin-top:var(--blok)). Корпусная цель снята
# ЖИВЫМ РЕНДЕРОМ 16 эталонных слайдов обратного прогона на их человеческих
# значениях (не статическим CSS-парсом — дыхание зависит от переноса строк,
# который CSS не знает без браузера); дорого гонять на каждом solve, поэтому
# — разовая команда, число процитировано (тот же приём, что уже у FILL_LO/HI,
# LINE_LEN_*): `python3 _generator/tools/fixtures/sborka/obratnyj-progon/
# izmerit_dyhanie.py` → n=13 (3 слайда с одним абзацем пропущены — с чем
# сравнивать промежуток, если блок один), p5=3.28, медиана=6.70, p95=10.07,
# stdev=2.17. Дата данных 2026-08-07.
DYHANIE_STAT = {"median": 6.6982, "stdev": 2.1728}
# p25 — Часть Б захода dovodka-solvera («коридор объёма»): «дыхание ≥ p25»
# — один из двух полов корпусной нормы для коридора (второй — kegl≥median).
# `DYHANIE_STAT` выше не содержит p25 (снят другим заходом под другую задачу —
# z-score штрафу нужны только median/stdev), поэтому досчитан ОТДЕЛЬНО тем же
# инструментом и тем же измерением, не новым: `python3 -c` над сырыми строками
# `izmerit_dyhanie.py` → `korpus.pct(значения, 25)` = 5.5543 (n=13, те же 13
# значений, что дали DYHANIE_STAT). Дата данных 2026-08-08.
DYHANIE_P25 = 5.5543


# JS выполняется ОДИН раз на слайд (page.evaluate), весь перебор — внутри
# страницы (Э5: батчинг записи CSS-переменных, один scrollHeight на пробу,
# мемоизация одинаковых троек).
_JS_SOLVE = r"""
(cfg) => {
  const zone = document.querySelector('.zone.t-body') || document.querySelector('.t-body');
  if (!zone) return {error: 'зона .zone.t-body не найдена на слайде'};
  const slide = document.querySelector('.slide');
  if (slide && typeof applyScene === 'function' && typeof scenesOf === 'function') {
    applyScene(slide, scenesOf(slide));
  }
  const grid = document.querySelector('.grid');

  // ── Э6: одна getClientRects() на текстовый узел — строки почти бесплатно ──
  function tipografika() {
    const paras = zone.querySelectorAll('p, li');
    let orphanCount = 0, edges = [];
    for (const p of paras) {
      for (const node of p.childNodes) {
        if (node.nodeType !== 3 || !node.textContent.trim()) continue;
        const range = document.createRange();
        range.selectNodeContents(node);
        const rects = Array.from(range.getClientRects());
        if (!rects.length) continue;
        for (const r of rects) edges.push(r.right);
        const lastLineText = (() => {
          // последняя строка — прямоугольник с максимальным top
          const lastTop = Math.max(...rects.map(r => r.top));
          return null; // точный текст строки не нужен — считаем слова по ширине последнего rect ниже
        })();
        const last = rects[rects.length - 1];
        // одинокое слово: последняя строка короче ~15% от типичной ширины строк
        if (rects.length > 1) {
          const widths = rects.map(r => r.width);
          const typical = widths.slice(0, -1).reduce((a, b) => a + b, 0) / (widths.length - 1);
          if (typical > 0 && last.width < 0.22 * typical) orphanCount++;
        }
      }
    }
    let edgeStd = 0;
    if (edges.length > 1) {
      const mean = edges.reduce((a, b) => a + b, 0) / edges.length;
      edgeStd = Math.sqrt(edges.reduce((a, b) => a + (b - mean) ** 2, 0) / edges.length);
    }
    // Э3 захода solver-v3-dyhanie, «мера дыхания»: доля zone.clientHeight,
    // занятая суммой ПОЛОЖИТЕЛЬНЫХ промежутков между соседними блоками
    // p/ul.tlist верхнего уровня зоны — ровно те элементы, что получают
    // margin-top:var(--blok) (Э1). Тот же проход браузера, что orphan/edge
    // (getBoundingClientRect на блоках вместо getClientRects на тексте) —
    // ни одной лишней пробы, как велит заход.
    const blocks = Array.from(zone.querySelectorAll(':scope > p, :scope > ul.tlist'));
    let dyhanie = null;
    if (blocks.length > 1) {
      let gapSum = 0;
      for (let i = 1; i < blocks.length; i++) {
        const gap = blocks[i].getBoundingClientRect().top - blocks[i - 1].getBoundingClientRect().bottom;
        if (gap > 0) gapSum += gap;
      }
      const ch = zone.clientHeight;
      dyhanie = ch ? (100 * gapSum / ch) : null;
    }
    return {orphanCount, edgeStd, lineCount: edges.length, dyhanie};
  }

  const textLen = zone.textContent.replace(/\s+/g, ' ').trim().length;
  const memo = new Map();
  const trials = [];
  // Э1 захода solver-v3-dyhanie: `blokKoef` — ДОЛЯ кегля, не независимая
  // px-ручка; фактический отступ вычисляется здесь же, на кегле ЭТОЙ пробы
  // (кегль меняется внутри бинарного поиска), с абсолютным полом-страховкой
  // `cfg.blok_floor_px` (перебор по отдельной px-оси исчез физически — такого
  // параметра в cfg больше нет).
  function measure(kegl, lh, blokKoef, liniya) {
    const key = kegl + '|' + lh + '|' + blokKoef + '|' + liniya;
    if (memo.has(key)) return memo.get(key);
    const blokPx = Math.max(cfg.blok_floor_px, kegl * blokKoef);
    // Э5: батч — все записи разом, потом ОДИН scrollHeight (никакого чередования читать/писать)
    zone.style.setProperty('--t-body', kegl + 'px');
    zone.style.setProperty('--lh', String(lh));
    zone.style.setProperty('--blok', blokPx + 'px');
    if (grid && liniya != null) grid.style.setProperty('--liniya', liniya + '%');
    const sh = zone.scrollHeight, ch = zone.clientHeight;
    const fill = ch ? (100 * sh / ch) : null;
    const fits = fill != null && fill <= 100;
    const typ = fits ? tipografika() : null;
    const rec = {kegl, lh, blokKoef, blok: blokPx, liniya, scrollHeight: sh, clientHeight: ch,
                 clipped: sh > ch, fill, fits, typ, dyhanie: typ ? typ.dyhanie : null};
    trials.push(rec);
    memo.set(key, rec);
    return rec;
  }

  // Бинарный поиск максимального влезающего кегля при (lh, blokKoef, liniya) —
  // вмещение монотонно (Э5 захода solver-vmeshcheniya): меньше кегль
  // помещается не хуже. `iters` проб на решётку.
  function maxKegl(floor, ceil, lh, blokKoef, liniya, iters) {
    const top = measure(ceil, lh, blokKoef, liniya);
    if (top.fits) return top;
    const bot = measure(floor, lh, blokKoef, liniya);
    if (!bot.fits) return null;
    let lo = floor, hi = ceil, best = bot;
    for (let i = 0; i < iters; i++) {
      const mid = Math.round((lo + hi) / 2 * 4) / 4;  // точность 0.25px
      if (mid === lo || mid === hi) break;
      const r = measure(mid, lh, blokKoef, liniya);
      if (r.fits) { best = r; lo = mid; } else { hi = mid; }
    }
    return best;
  }

  let liniyaBase = null;
  if (grid) {
    const raw = getComputedStyle(grid).getPropertyValue('--liniya').trim();
    const v = parseFloat(raw);
    if (isFinite(v)) liniyaBase = v;
  }
  const liniyaCandidates = liniyaBase == null ? [null] : cfg.liniya_steps;

  // Все влезающие пробы решётки × liniya — сетка мала (Э2 захода
  // solver-vmeshcheniya: доли мс на пробу), полный перебор дешевле, чем
  // хитрая эвристика остановки на первом найденном.
  let fitting = [];
  for (const liniya of liniyaCandidates) {
    for (const [lh, blokKoef, ceil] of cfg.rungi) {
      const best = maxKegl(cfg.kegl_floor, ceil, lh, blokKoef, liniya, cfg.iters);
      if (best && best.fits) {
        // Э4, снап на решётку: не «пол ниже непрерывного результата» (дал бы
        // 22 против 21 на почти одинаковом слайде — дрожание), а наибольшая
        // точка ФИКСИРОВАННОЙ решётки cfg.kegl_grid, не превышающая найденный
        // максимум. Снап ВНИЗ безопасен — вмещение монотонно (Э5), меньший
        // кегль влезает не хуже. Последний шаг решётки — целый px (округление
        // вниз, дробный px после растеризации переполняет незаметно).
        let snapped = cfg.kegl_grid.filter(g => g <= best.kegl + 1e-9).pop();
        if (snapped == null) snapped = cfg.kegl_floor;
        snapped = Math.floor(snapped);
        const rounded = snapped === best.kegl ? best : measure(snapped, lh, blokKoef, liniya);
        if (rounded.fits) fitting.push(rounded);
      }
    }
  }

  return {trials, fitting, liniya_base: liniyaBase, text_len: textLen};
}
"""


def _line_chars_estimate(kegl, zone_width_px, line_count, text_len_chars):
    """Символов в строке — оценка без парсинга шрифта (Э3, уровень 3):
    средняя длина строки по общему числу символов текста и числу строк из
    Э6 (getClientRects уже посчитал реальные строки, экономнее не парсить
    ширину каждого символа отдельно)."""
    if not line_count:
        return None
    return text_len_chars / line_count


def _zscore(value, stat):
    if not stat or value is None or stat.get("stdev", 0) == 0:
        return 0.0
    return (value - stat["median"]) / stat["stdev"]


def _cube_penalty(z, w):
    return w * (abs(z) ** 3)


def _fill_band_penalty(fill):
    if fill is None:
        return 10.0
    if FILL_LO <= fill <= FILL_HI:
        return 0.0
    d = (FILL_LO - fill) if fill < FILL_LO else (fill - FILL_HI)
    return d / 10.0  # нормировка — единицы штрафа сравнимы с z-score-штрафами


def _select_lexicograficheski(fitting, corpus, axis, text_len_chars):
    """Э2 захода solver-v3-dyhanie: порядок уровней ПЕРЕСТАВЛЕН — похожесть на
    корпус выше максимизации кегля (было наоборот: старый уровень 2 сразу
    брал самый крупный кегль, похожесть служила лишь для выбора СРЕДИ них —
    поэтому солвер систематически бил в потолок кегля и платил за это отступом,
    Э1 диагноз захода). Уровень 1 (вмещение) уже гарантирован (`fitting` —
    только влезшие). Дальше:
      2. читаемость — символы в строке 45–75 (никогда >80), фильтр, не ранг;
      3. похожесть на корпус — выпуклый (кубический) штраф по z-score корпуса
         (кегль, lh, blok_koef, liniya, дыхание Э3) + ровность правого края,
         полоса ε=EPS_PENALTY;
      4. кегль как тай-брейк МЕЖДУ ОДИНАКОВО ПОХОЖИМИ (не среди всех влезших) —
         максимизировать, полоса ε=EPS_KEGL;
      5. заполнение — минимальный штраф отклонения от полосы 75–90%;
      6. финальный тай-брейк (не назван заходом отдельным уровнем, нужен для
         детерминизма при полной ничьей) — минимальный liniya (меньше
         отъедено у иллюстрации).
    Возвращает (выбранный trial, диагностику: что отсеяно и почему)."""
    if not fitting:
        return None, {}

    def line_chars(t):
        lc = t.get("typ", {}).get("lineCount") if t.get("typ") else None
        return _line_chars_estimate(t["kegl"], None, lc, text_len_chars)

    diag = {}
    readable = [t for t in fitting
                if (lambda ch: ch is None or ch <= LINE_LEN_HARD_MAX)(line_chars(t))]
    pool = readable if readable else fitting
    diag["читаемых_по_длине_строки"] = len(readable)
    diag["всего_влезших"] = len(fitting)
    diag["лучший_кегль_среди_всех_влезших"] = max(t["kegl"] for t in pool)  # для критерия 2: что отвергли

    def penalty(t):
        p = _cube_penalty(_zscore(t["kegl"], corpus["кегль_px"]), WEIGHTS["kegl"])
        p += _cube_penalty(_zscore(t["lh"], corpus["lh_отношение_к_кеглю"]), WEIGHTS["lh"])
        blok_koef = t["blok"] / t["kegl"] if t.get("kegl") else None
        p += _cube_penalty(_zscore(blok_koef, corpus["blok_koef_k_keglyu"]), WEIGHTS["blok"])
        if t.get("liniya") is not None:
            stat = corpus["liniya_equiv_horizontal_pct" if axis == "horizontal"
                          else "liniya_equiv_vertical_pct"]
            p += _cube_penalty(_zscore(t["liniya"], stat), WEIGHTS["liniya"])
        p += _cube_penalty(_zscore(t.get("dyhanie"), DYHANIE_STAT), WEIGHTS["dyhanie"])
        edge = t.get("typ", {}).get("edgeStd", 0) or 0
        p += WEIGHTS["edge"] * ((edge / max(t["kegl"], 1)) ** 3)
        return p

    scored = [(penalty(t), t) for t in pool]
    min_p = min(p for p, _ in scored)
    level_similar = [t for p, t in scored if p <= min_p * (1 + EPS_PENALTY) + 1e-9]
    diag["мин_штраф"] = round(min_p, 4)
    diag["уровень_похожести_после_epsilon"] = len(level_similar)

    best_kegl_similar = max(t["kegl"] for t in level_similar)
    level_kegl = [t for t in level_similar if t["kegl"] >= best_kegl_similar - EPS_KEGL]
    diag["лучший_кегль_в_группе_похожести"] = best_kegl_similar
    diag["уровень_кегля_после_epsilon"] = len(level_kegl)

    min_fill_p = min(_fill_band_penalty(t["fill"]) for t in level_kegl)
    level_fill = [t for t in level_kegl if _fill_band_penalty(t["fill"]) <= min_fill_p + 1e-9]
    diag["уровень_заполнения"] = len(level_fill)

    chosen = min(level_fill, key=lambda t: (t.get("liniya") if t.get("liniya") is not None else -1))
    return chosen, diag


def podobrat_slide(page, html_path, axis, iters=8, steps=6, text_len_chars=None, corpus=None):
    """Полный солвер с известной осью liniya. `axis` — 'horizontal'/'vertical'/None."""
    from urllib.parse import quote
    url = "file://" + quote(str(Path(html_path).resolve()))
    page.goto(url)
    page.wait_for_timeout(120)

    corpus = corpus if corpus is not None else korpus.corpus_stats()
    zones = build_zones(corpus)
    rungi = build_rungi(zones, steps=steps)

    cfg = {"kegl_floor": zones["kegl"][0], "iters": iters, "rungi": rungi, "liniya_steps": [None],
           "kegl_grid": build_kegl_grid(zones), "blok_floor_px": BLOK_FLOOR_PX}
    if axis:
        # базовый liniya читается в JS с самого элемента; шаги строим уже
        # после первого прохода, когда знаем liniyaBase — делаем это в два
        # вызова evaluate НЕЛЬЗЯ (Э5: один evaluate), поэтому JS сам читает
        # base и Python заранее не знает точный список — передаём широкий
        # диапазон кандидатов, вычисленный от зоны целиком (не от base),
        # т.к. base сам может быть вне зоны (баг s08: 92 > потолка 82).
        lo, hi = zones["liniya_%s" % axis]
        cfg["liniya_steps"] = [round(lo + (hi - lo) * k / 6, 2) for k in range(7)]

    result = page.evaluate(_JS_SOLVE, cfg)
    if result.get("error"):
        raise RuntimeError(result["error"])

    fitting = result["fitting"]
    if axis:
        for t in fitting:
            if t.get("liniya") is not None:
                check_liniya_zone(zones, axis, t["liniya"])  # защитный повтор — не должно случиться

    # длина текста — измеренная в браузере (`zone.textContent`), не угаданная
    # снаружи; `text_len_chars` как параметр остаётся ТОЛЬКО на случай, если
    # вызывающий код заранее знает более точное число (не используется CLI).
    measured_len = result.get("text_len") or text_len_chars or 1200
    chosen, diag = _select_lexicograficheski(fitting, corpus, axis, measured_len)
    otstuplenie = False
    if chosen is None:
        # Э3 захода solver-vmeshcheniya, «отступление»: ни одна проба внутри
        # ЖЁСТКИХ зон не влезла — честный отказ, не расширяем зоны молча.
        otstuplenie = True
    return {"chosen": chosen, "diagnostics": diag, "n_trials": len(result["trials"]),
            "n_fitting": len(fitting), "liniya_base": result["liniya_base"],
            "otstuplenie": otstuplenie, "zones": zones}


def izmerit(page, html_path, kegl=None, lh=None, blok=None):
    """Разовый промер (без перебора) — текущий/заданный триплет → влезло или нет.

    Часть Б захода dovodka-solvera («коридор объёма») добавила `content_fill`
    и `dyhanie` — найдено ЭТИМ прогоном (не было известно заранее): `.zone`
    растянута CSS-гридом до высоты своего ряда (`align-items` по умолчанию —
    `stretch`), поэтому `scrollHeight` при НЕ переполненном содержимом ВСЕГДА
    равен `clientHeight` (растянутый бокс, не контент) — `fill` отсюда даёт
    100% при 10 знаках так же, как при 300 (проверено фактом: `koridor_obyoma.py`
    на синтетической пробе, `content_extent` при этом честно росло 33.5%→97.8%).
    `fill`/`fits` — старое поведение, не тронуты (уже используются в других
    местах через `scrollHeight<=clientHeight`, это условие переполнения не
    зависит от stretch). `content_fill` — доля `clientHeight`, которую РЕАЛЬНО
    занял текст (нижний край последнего ребёнка минус верх зоны) — то, что
    нужно для «мельчит и пусто внизу» (fill от stretch-бокса для этого
    непригоден). `dyhanie` — тот же промежуточный расчёт, что в `_JS_SOLVE.
    tipografika()` (Э3 захода solver-v3-dyhanie), для одноразового промера
    без полного перебора решётки."""
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
      const blocks = Array.from(zone.querySelectorAll(':scope > p, :scope > ul.tlist'));
      const zoneTop = zone.getBoundingClientRect().top;
      const contentExtent = blocks.length ? blocks[blocks.length - 1].getBoundingClientRect().bottom - zoneTop : 0;
      let dyhanie = null;
      if (blocks.length > 1) {
        let gapSum = 0;
        for (let i = 1; i < blocks.length; i++) {
          const gap = blocks[i].getBoundingClientRect().top - blocks[i - 1].getBoundingClientRect().bottom;
          if (gap > 0) gapSum += gap;
        }
        dyhanie = ch ? (100 * gapSum / ch) : null;
      }
      return {scrollHeight: sh, clientHeight: ch, fits: sh <= ch,
              fill: ch ? (100 * sh / ch) : null,
              content_fill: ch ? (100 * contentExtent / ch) : null,
              n_blocks: blocks.length, dyhanie: dyhanie};
    }
    """
    r = page.evaluate(js, {"kegl": kegl, "lh": lh, "blok": blok})
    if r.get("error"):
        raise RuntimeError(r["error"])
    return r


def apply_to_card(slide_md_path, best):
    """Решение солвера → карточка слайда (`slaid.md`): дописывает/заменяет поля
    `liniya`, `kegl_px`, `mezhstrochye`, `otstup_bloka` в YAML-шапке. Правит
    ТОЛЬКО эти четыре строки."""
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


def _demo_zony():
    """Э1, п.1 критерия готовности: показать выводом команды, что нарушение
    зоны отвергается ДО поиска, на заведомо плохом входе — буквально баг s08
    (liniya=92 на горизонтальной полосе)."""
    zones = build_zones()
    print("Жёсткие зоны (Э1, из корпуса + рельсы):")
    for name, (lo, hi) in zones.items():
        print("  %-20s [%s, %s]" % (name, lo, hi))
    print("\nЗаведомо плохой вход — заход solver-vmeshcheniya реально выбрал liniya=92 на s08 "
          "(горизонтальная полоса), ужав иллюстрацию до ~8%:")
    try:
        check_liniya_zone(zones, "horizontal", 92)
        print("❌ НЕ ОТВЕРГНУТО — дефект солвера")
        return 1
    except ZonaNarushena as e:
        print("✅ ОТВЕРГНУТО ДО ПОИСКА: %s" % e)
        return 0


def main():
    ap = argparse.ArgumentParser(description="Измеритель/солвер вмещения v2 (заход solver-v2)")
    ap.add_argument("html", nargs="?", help="путь к скомпилированному HTML одного слайда")
    ap.add_argument("--podobrat", action="store_true", help="прогнать солвер (иначе — промер дефолтов)")
    ap.add_argument("--axis", choices=("horizontal", "vertical"), default=None,
                     help="ось liniya (для polosa_gorizontalnaya/polosa_vertikalnaya)")
    ap.add_argument("--iters", type=int, default=8)
    ap.add_argument("--text-len", type=int, default=1200, help="длина текста в знаках (оценка строки)")
    ap.add_argument("--primenit", metavar="SLAID_MD")
    ap.add_argument("--demo-zony", action="store_true", help="Э1 п.1: показать отказ ДО поиска на плохом входе")
    args = ap.parse_args()

    if args.demo_zony:
        return _demo_zony()

    if not args.html:
        ap.error("нужен путь к HTML (или --demo-zony)")

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        page = b.new_page(viewport={"width": 1440, "height": 810}, device_scale_factor=1)
        if args.podobrat:
            res = podobrat_slide(page, args.html, axis=args.axis, iters=args.iters,
                                  text_len_chars=args.text_len)
            print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
            if res["chosen"] is None:
                print("ОТКАЗ: ни одна проба не влезла внутри жёстких зон Э1.", file=sys.stderr)
                b.close()
                return 1
            if args.primenit:
                apply_to_card(args.primenit, res["chosen"])
                print("применено в карточку: %s" % args.primenit, file=sys.stderr)
        else:
            res = izmerit(page, args.html)
            print(json.dumps(res, ensure_ascii=False, indent=2))
        b.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
