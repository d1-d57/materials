#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Диапазоны из корпуса живых деков (Э2 захода solver-v2).

По трём `shablon.html` (Я4 захода: `teorkat-vvedenie`, `dandelin`, `buffon` —
343 живых слайдовых CSS-правила по прикидке автора захода) снимает per-slide
числовые параметры и печатает p5/медиана/p95 — мягкий приор для солвера
(штраф по z-score, не отсечка).

Три деки построены ПО-РАЗНОМУ (найдено этим заходом, не было известно заранее):
`teorkat-vvedenie`/`dandelin` несут финальные пер-слайдовые CSS-гриды прямо в
`<style>` (`#sNN{...}`), `buffon` — новее, шаблонизирован (`{{SLIDE:id}}`), но
по факту тоже кладёт пер-слайдовые правила в `<style>` с той же идеей (`#sl-id`).
Общий парсер: слайд-id снимаются с токенов `{{SLIDE:<id>}}`, дальше любое
CSS-правило, чей селектор ссылается на `#<id>`, — «пер-слайдовое правило».

liniya (доля текстовой полосы) — переменная НОВОЙ системы (`tipy.py`,
`--liniya` + `calc(100% - var(--liniya))`); в корпусе её нет буквально — эти
три дека собраны ручным 2D CSS-гридом (`sverstat.py`, дека `teorkat-vvedenie`).
Эквивалент восстанавливается: на «делящей» оси (рядность и колоночность
слайда) ищется трек с `1fr`/`minmax(0,1fr)` (текст) и наибольший фикс-px трек
>150px (иллюстрация/`rail`/`board`) — доля иллюстрации = fix_px / canvas_dim,
liniya_equiv = 100 − доля. Это ПРИБЛИЖЕНИЕ (см. докстринг ниже секции
`_liniya_equiv_from_axis`), не точная реконструкция чужой вёрстки.

  python3 _generator/sborka/korpus.py            # печатает сводку и JSON в konsolʹ
"""
import json
import re
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

DECKS = [
    REPO / "teorkat-vvedenie" / "src" / "shablon.html",
    REPO / "dandelin" / "src" / "shablon.html",
    REPO / "buffon" / "src" / "shablon.html",
]

SKELETON_TOKENS = REPO / "_generator" / "skeleton" / "tokens.css"

CANVAS_W, CANVAS_H = 1440, 810


def extract_style(html):
    m = re.search(r"<style>(.*?)</style>", html, re.S)
    return m.group(1) if m else ""


def top_level_rules(css):
    """Плоский разбор CSS с учётом вложенности `@media{...}` (внутри тоже
    правила) — обычный построчный регэксп на `{[^{}]*}` рассыпается на
    `@keyframes`/`@media`, где есть вложенные фигурные скобки."""
    rules = []
    i, n = 0, len(css)
    while i < n:
        if css[i:i + 2] == "/*":
            j = css.find("*/", i + 2)
            i = (j + 2) if j != -1 else n
            continue
        if css[i].isspace():
            i += 1
            continue
        j = css.find("{", i)
        if j == -1:
            break
        selector = css[i:j].strip()
        depth = 1
        k = j + 1
        while k < n and depth > 0:
            if css[k] == "{":
                depth += 1
            elif css[k] == "}":
                depth -= 1
            k += 1
        body = css[j + 1:k - 1]
        if selector.startswith("@media"):
            rules.extend(top_level_rules(body))
        elif selector.startswith("@"):
            pass  # @font-face/@keyframes — не типографика слайда
        else:
            rules.append((selector, body))
        i = k
    return rules


def slide_ids(html):
    return set(re.findall(r"\{\{SLIDE:([\w-]+)\}\}", html))


def id_in_selector(sel, sid):
    return re.search(r"#%s(?![\w-])" % re.escape(sid), sel) is not None


_TYPOGRAPHY_SELECTOR = re.compile(
    r"^\s*#[\w-]+(\s*\.(copy|t-body))*\s*$")


def is_body_typography_selector(sel, sid):
    """Кегль/lh/blok тела текста — только с селектора вида `#sid` или
    `#sid .copy`/`.t-body`, БЕЗ дальнейшей цепочки (`.copy p.lestnica`,
    `.zagolovok`, `.t-display`, `.board` и т.п. — другая типографика/декор,
    не тело зоны). Найдено этим прогоном: без фильтра в кегль подмешивались
    72–96px из `.t-display`/`.brd-title` (заголовки обложки/визитки)."""
    return bool(_TYPOGRAPHY_SELECTOR.match(sel))


_NON_CONTENT_ID = re.compile(r"title|vizitka|thanks|divider|oblozhka|cover", re.I)


def is_content_slide(sid):
    """Обложка/визитка/разделитель/финал — не `polosa_*`: фиксированный
    канонический грид, повторяющийся тождественно между деками (не сигнал о
    диапазоне ручек солвера, а один и тот же шаблон, посчитанный трижды)."""
    return not _NON_CONTENT_ID.search(sid)


def parse_decl(body):
    out = {}
    for part in body.split(";"):
        part = part.strip()
        if not part or ":" not in part:
            continue
        k, v = part.split(":", 1)
        out[k.strip()] = v.strip()
    return out


_PX = re.compile(r"^(-?[\d.]+)px$")
_NUM = re.compile(r"^(-?[\d.]+)$")


def as_px(v):
    m = _PX.match(v)
    return float(m.group(1)) if m else None


def as_num(v):
    m = _NUM.match(v)
    return float(m.group(1)) if m else None


def _root_vars(css_path):
    """`:root{...}` объявления файла токенов → {переменная: сырое значение}.
    Пустой словарь, если файла нет или блока `:root` в нём нет — вызывающий
    код сам решает, есть ли откуда падать дальше по каскаду."""
    if not css_path.exists():
        return {}
    css = css_path.read_text(encoding="utf-8")
    m = re.search(r":root\s*\{([^{}]*)\}", css, re.S)
    if not m:
        return {}
    without_comments = re.sub(r"/\*.*?\*/", "", m.group(1), flags=re.S)
    return parse_decl(without_comments)


def canon_defaults(deck_src_dir):
    """Умолчание кегль/lh/blok для дека, каскад skeleton → дек-`tokens.css`
    (Э4 захода solver-v3-dyhanie): большинство слайдов НЕ переопределяют эти
    переменные per-slide — не значит, что автор не выбирал их, значит выбрал
    молчаливо унаследованное значение. `korpus.py` раньше считал только явные
    per-slide переопределения (`is_body_typography_selector`) — 8 слайдов из
    49 контентных для `blok`, ноль для `dandelin`/`buffon` (там `--blok`
    вообще не переопределён ни разу, весь дек живёт на умолчании 26px из
    `_generator/skeleton/tokens.css`). Дек-`tokens.css` может переопределить
    любую из трёх переменных на уровне всего дека (ни один из трёх живых не
    переопределяет `--blok`, `dandelin` не переопределяет и `--lh`) — каскад
    воспроизводит это, а не жёстко берёт только skeleton."""
    merged = dict(_root_vars(SKELETON_TOKENS))
    merged.update(_root_vars(Path(deck_src_dir) / "tokens.css"))
    return {
        "kegl": as_px(merged.get("--t-body", "")),
        "lh": as_num(merged.get("--lh", "")),
        "blok": as_px(merged.get("--blok", "")),
    }


def _parse_grid_area(v):
    parts = [p.strip() for p in v.split("/")]
    if len(parts) != 4:
        return None
    try:
        return tuple(int(p) for p in parts)  # row1, col1, row2, col2 — 1-indexed линии
    except ValueError:
        return None


def _track_span_px(tracks, start, end):
    """Сумма px треков между 1-индексными линиями `start`..`end` (не включая
    `end`). `None`, если в диапазоне встретился нечисловой трек (`1fr` и т.п.)."""
    sizes = [as_px(t) for t in tracks]
    span = sizes[start - 1:end - 1]
    if not span or any(s is None for s in span):
        return None
    return sum(span)


def liniya_equiv_for_slide(rules_for_slide):
    """Иллюстрация в этом корпусе — не переменная `--liniya` (её тут нет,
    корпус собран РУЧНЫМ 2D CSS-гридом, sverstat.py), а класс `.board`/`.rail`
    с явным `grid-area`. Кросс-ссылка: найти `grid-template-rows/columns` на
    `.grid` этого слайда, найти `grid-area` на `.board`/`.rail`, посчитать,
    сколько px этой оси занимает иллюстрация, и по тому, покрывает ли её
    grid-area почти всю ДРУГУЮ ось — определить, ГОРИЗОНТАЛЬНАЯ это полоса
    (иллюстрация занимает строки на всю ширину) или ВЕРТИКАЛЬНАЯ (иллюстрация
    занимает колонки на всю высоту). Первая версия скрипта (одиночный
    наибольший фикс-px трек без этой сверки) путала обычный левый/правый
    отступ страницы (`40px 1360px 40px`) с полосой — тот же 1360px «контент»
    трек читался как «иллюстрация», деля liniya≈5% вместо ≈65%; поймано
    живым прогоном (значения выходили за пределы прикидки владельца)."""
    grid_rules = [(sel, decl) for sel, decl in rules_for_slide
                  if re.search(r"\.grid\s*$", sel) and
                  ("grid-template-rows" in decl or "grid-template-columns" in decl)]
    board_rules = [(sel, decl) for sel, decl in rules_for_slide
                   if re.search(r"\.(board|rail)\b", sel) and "grid-area" in decl]
    if not grid_rules or not board_rules:
        return None
    _, gdecl = grid_rules[0]
    rows = gdecl.get("grid-template-rows", "").split()
    cols = gdecl.get("grid-template-columns", "").split()
    if not rows or not cols:
        return None
    _, bdecl = board_rules[0]
    area = _parse_grid_area(bdecl["grid-area"])
    if area is None:
        return None
    r1, c1, r2, c2 = area
    col_span, row_span = c2 - c1, r2 - r1
    full_cols_covered = col_span >= max(1, len(cols) - 1)
    full_rows_covered = row_span >= max(1, len(rows) - 1)
    if full_cols_covered and not full_rows_covered:
        ill_px = _track_span_px(rows, r1, r2)
        if ill_px is None:
            return None
        return 100.0 * (CANVAS_H - ill_px) / CANVAS_H, "horizontal"
    if full_rows_covered and not full_cols_covered:
        ill_px = _track_span_px(cols, c1, c2)
        if ill_px is None:
            return None
        return 100.0 * (CANVAS_W - ill_px) / CANVAS_W, "vertical"
    return None  # не простой 2-зонный сплит (обе оси частичны или обе полны) — не берём


def analyze_deck(path):
    html = path.read_text(encoding="utf-8")
    style = extract_style(html)
    ids = slide_ids(html)
    rules = top_level_rules(style)
    per_slide = {}
    rules_by_slide = {}
    n_rules = 0
    for sel, body in rules:
        matched = [sid for sid in ids if id_in_selector(sel, sid)]
        if not matched:
            continue
        n_rules += 1
        decl = parse_decl(body)
        for sid in matched:
            if not is_content_slide(sid):
                continue
            rules_by_slide.setdefault(sid, []).append((sel, decl))
            slot = per_slide.setdefault(sid, {})
            if is_body_typography_selector(sel, sid):
                for prop in ("--t-body", "font-size"):
                    if prop in decl:
                        px = as_px(decl[prop])
                        if px:
                            slot["kegl"] = px
                for prop in ("--lh", "line-height"):
                    if prop in decl:
                        v = as_num(decl[prop])
                        if v:
                            slot["lh"] = v
                if "--blok" in decl:
                    px = as_px(decl["--blok"])
                    if px:
                        slot["blok"] = px
            if "margin-top" in decl and ("p + p" in sel or "p+p" in sel):
                px = as_px(decl["margin-top"])
                if px:
                    slot.setdefault("blok", px)
    # Э4 захода solver-v3-dyhanie: молчаливое умолчание — тоже решение автора,
    # не «нет данных». Каждый контентный id получает слот (даже если у него
    # НИ ОДНОГО per-slide правила не было вовсе — `dandelin`/`buffon` для
    # `blok` именно такие), а kegl/lh/blok, не заданные явно, — из каскада
    # skeleton→дек `tokens.css` (`canon_defaults`). ДО этой правки `blok_px`
    # видел 8 явных переопределений из 49 контентных слайдов (все — в
    # `teorkat-vvedenie`) и строил потолок зоны 21.4px; факт измерения — см.
    # `## ПЛАН`/`## ОТЧЁТ` захода, числа сняты живым прогоном, не вписаны.
    defaults = canon_defaults(path.parent)
    for sid in ids:
        if not is_content_slide(sid):
            continue
        slot = per_slide.setdefault(sid, {})
        for k in ("kegl", "lh", "blok"):
            if k not in slot and defaults.get(k) is not None:
                slot[k] = defaults[k]
                slot.setdefault("унаследовано", set()).add(k)
    # liniya — вторым проходом, требует ВСЕ правила слайда разом (кросс-ссылка
    # `.grid` ↔ `.board`/`.rail`, см. докстринг `liniya_equiv_for_slide`).
    for sid, slot in per_slide.items():
        res = liniya_equiv_for_slide(rules_by_slide.get(sid, []))
        if res is not None:
            slot["liniya"], slot["axis"] = res
    return n_rules, per_slide


def pct(values, p):
    if not values:
        return None
    values = sorted(values)
    k = (len(values) - 1) * p / 100.0
    f, c = int(k), min(int(k) + 1, len(values) - 1)
    if f == c:
        return values[f]
    return values[f] + (values[c] - values[f]) * (k - f)


def summarize(values):
    values = [v for v in values if v is not None]
    if not values:
        return None
    out = {"n": len(values), "p5": round(pct(values, 5), 4),
           "median": round(statistics.median(values), 4),
           "p95": round(pct(values, 95), 4)}
    out["stdev"] = round(statistics.pstdev(values), 4) if len(values) > 1 else 0.0
    return out


def corpus_stats():
    """Программный вход (солвер импортирует это, не парсит свой stdout) —
    KONSTITUCIYA §10: число считается командой каждый раз, не вписывается
    руками и не кэшируется в отдельном файле-константе, который протухнет
    при следующей правке деков."""
    total_rules = 0
    all_slides = {}
    per_deck_rules = {}
    for path in DECKS:
        if not path.exists():
            continue
        n_rules, per_slide = analyze_deck(path)
        per_deck_rules[path.parent.parent.name] = n_rules
        total_rules += n_rules
        for sid, slot in per_slide.items():
            all_slides["%s/%s" % (path.parent.parent.name, sid)] = slot

    kegl = [s["kegl"] for s in all_slides.values() if "kegl" in s]
    lh = [s["lh"] for s in all_slides.values() if "lh" in s]  # lh уже отношение к кеглю (unitless line-height)
    blok = [s["blok"] for s in all_slides.values() if "blok" in s]
    # Э1 захода solver-v3-dyhanie: отступ — ДОЛЯ кегля, не свободная px-ручка
    # (тот же приём, что уже даёт `lh`). Ratio считается только там, где есть
    # ОБА числа на одном слайде — после починки Э4 это все 49 контентных
    # слайдов (было бы 8, если бы `blok` остался только явным).
    blok_koef = [s["blok"] / s["kegl"] for s in all_slides.values()
                 if "blok" in s and s.get("kegl")]
    liniya_h = [s["liniya"] for s in all_slides.values() if s.get("axis") == "horizontal"]
    liniya_v = [s["liniya"] for s in all_slides.values() if s.get("axis") == "vertical"]

    return {
        "правил_обработано_по_декам": per_deck_rules,
        "правил_обработано_всего": total_rules,
        "слайдов_с_данными": len(all_slides),
        "кегль_px": summarize(kegl),
        "lh_отношение_к_кеглю": summarize(lh),
        "blok_px": summarize(blok),
        "blok_koef_k_keglyu": summarize(blok_koef),
        "liniya_equiv_horizontal_pct": summarize(liniya_h),
        "liniya_equiv_vertical_pct": summarize(liniya_v),
    }


def main():
    report = corpus_stats()
    total_rules = report["правил_обработано_всего"]
    per_deck_rules = report["правил_обработано_по_декам"]
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("\n--- сводка ---", file=sys.stderr)
    print("правил обработано: %d (по декам: %s)" % (total_rules, per_deck_rules), file=sys.stderr)
    for name, s in (("кегль", report["кегль_px"]), ("lh", report["lh_отношение_к_кеглю"]),
                     ("blok", report["blok_px"]), ("blok/kegl", report["blok_koef_k_keglyu"]),
                     ("liniya гориз", report["liniya_equiv_horizontal_pct"]),
                     ("liniya верт", report["liniya_equiv_vertical_pct"])):
        if s:
            print("  %-14s n=%-4d p5=%-8s медиана=%-8s p95=%s" % (name, s["n"], s["p5"], s["median"], s["p95"]),
                  file=sys.stderr)
        else:
            print("  %-14s нет данных" % name, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
