#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сборка ЦЕЛОГО дека — параллельно по слайдам (Э6 захода kartochka-i-sborka).

  python3 _generator/sborka/deck.py <лекция> -o <лекция>/dist/index.html [-j 15]

Раскладка — Я2 (istochnik-istiny.md §2): `<лекция>/slajdy/<imya>/slaid.md`, один
файл на слайд, ИМЯ ПАПКИ = `sid` (не `slide_path.stem` — тот теперь всегда literally
"slaid" у всех слайдов сразу, различает их только папка). Иллюстрации — ОТДЕЛЬНЫЙ
пул `<лекция>/illustracii/` (Э5 захода, имя ПО СПЕЦИФИКАЦИИ, не англ. "illustrations"
старого пути). `status: rezerv` — слайд лежит в папке, в дек НЕ входит и в
`slide_order` может не быть вовсе (Я1 §4-бис).

Слайды независимы (параметры + текст, никаких перекрёстных ссылок между файлами
слайдов), поэтому компиляция каждого — отдельный процесс (`ProcessPoolExecutor`,
stdlib, без pip). Порядок — `brief.md:slide_order` тем же диалектом, что читает
`build_deck.py` (Я6, `parse_brief`, READ-ONLY импорт; `brief.md` — И манифест
порядка, И карточка лекции, см. `## ПЛАН` захода п.4); `oblozhka` принудительно
первой, `finalnyj` принудительно последней — по ТИПУ слайда, а не по месту в списке
автора (устойчивее зарезервированных id старого `build_deck.py`).

`build_deck.py` этим НЕ трогается — параллельный путь, отдельная папка.
"""
import argparse
import sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
import os

SBORKA = Path(__file__).resolve().parent
GENERATOR = SBORKA.parent
SKELETON = GENERATOR / "skeleton"
for p in (str(SBORKA), str(GENERATOR)):
    if p not in sys.path:
        sys.path.insert(0, p)


def _compile_one(slide_path_str):
    """Воркер отдельного процесса: путь к .md → (sid, tip, status, illustracii-стемы,
    css, html, n_scenes). `sid` — ИМЯ ПАПКИ слайда (`slajdy/<sid>/slaid.md`), не
    стем файла. `n_scenes` — Э8 захода kartochka-i-sborka: без него движок считает
    слайд односценовым и пропуск (`{@N|…}`) не раскрывается НИКОГДА (см. slaid.py).
    Импорты — ВНУТРИ функции: `ProcessPoolExecutor` на macOS стартует процессы
    методом spawn, каждый воркер импортирует этот модуль заново с нуля."""
    import sys as _sys
    from pathlib import Path as _Path
    sb = _Path(__file__).resolve().parent
    gen = sb.parent
    for p in (str(sb), str(gen)):
        if p not in _sys.path:
            _sys.path.insert(0, p)
    from formaty import parse_slide, render_body
    from tipy import compile_tip
    from build_deck import max_scenes  # noqa: E402  (READ-ONLY импорт, Я6)
    from slaid import load_math_cache  # noqa: E402  (Э5 захода solver-vmeshcheniya)

    slide_path = _Path(slide_path_str)
    sid = slide_path.parent.name
    text = slide_path.read_text(encoding="utf-8")
    params, body_md = parse_slide(text, sid=sid)
    params["illustracii"] = [_Path(s).stem for s in (params.get("illustracii") or [])]
    # slide_path = <лекция>/slajdy/<sid>/slaid.md → parents[2] = <лекция>
    math = load_math_cache(slide_path.parents[2])
    body_html = render_body(body_md, acc_tag="span", math=math)
    css, html = compile_tip(sid, params, body_html)
    n_scenes = max_scenes(html)
    return (sid, params.get("tip_verstki"), params.get("status", "v_deke"),
            params["illustracii"], css, html, n_scenes)


# Р3 захода porcia-1-zamknut-konvejer: ось `liniya` солвера имеет смысл только
# у двух типов вёрстки (полоса делится горизонтально/вертикально) — остальные
# типы подбирают только kegl/lh/blok (axis=None, vmeshchenie.podobrat_slide сам
# не варьирует liniya без оси).
AXIS_BY_TIP = {"polosa_gorizontalnaya": "horizontal", "polosa_vertikalnaya": "vertical"}


def _podobrat_tipografiku(to_compile):
    """Прогоняет солвер (`vmeshchenie.podobrat_slide`) по каждому слайду из
    `to_compile`, у которого В ШАПКЕ ЕЩЁ НЕТ явного `kegl_px`/`liniya`, и
    применяет выбор в карточку (`vmeshchenie.apply_to_card`) ДО финальной
    параллельной компиляции. Раньше `deck.py` вообще не звал `vmeshchenie.py`
    (Р3: главный инструмент арки был не подключён к сборке).

    Явный `kegl_px` ИЛИ явный `liniya` в шапке — солвер слайд НЕ ТРОГАЕТ вовсе
    (не «подбирает недостающее вокруг явного» — это уже дизайн типографики,
    не проводка, не моя задача; «явное не перетирается» read буквально)."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        raise SystemExit(
            "playwright не установлен — подбор типографики недоступен и деку "
            "БЕЗ подбора я не соберу молча (см. §2 Р3 захода "
            "porcia-1-zamknut-konvejer): либо `pip install playwright && "
            "playwright install chrome`, либо явный флаг --bez-podbora. (%s)" % e)
    import tempfile
    from formaty import parse_card
    from slaid import compile_slide_html
    import vmeshchenie

    podobrano, propushcheno = 0, 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 810}, device_scale_factor=1)
        try:
            for slide_path in to_compile:
                sid = slide_path.parent.name
                params, _ = parse_card(slide_path.read_text(encoding="utf-8"), sid=sid)
                axis = AXIS_BY_TIP.get(params.get("tip_verstki"))
                # `liniya` — ОБЯЗАТЕЛЬНОЕ поле шапки у ЛЮБОГО tip_verstki (гейт того
                # требует), но солвер её вообще трогает только у polosa_* (axis не
                # None). У остальных типов число в liniya — просто заполненное ради
                # гейта, не решение автора про ЭТУ типографику; считать его «явным»
                # заблокировало бы подбор kegl_px для каждого не-polosa слайда.
                kegl_yavnyj = bool(params.get("kegl_px"))
                liniya_yavnaya = axis is not None and params.get("liniya") not in (None, "", "заполнить")
                if kegl_yavnyj or liniya_yavnaya:
                    propushcheno += 1
                    print("подбор: %s — пропущен, явные значения в шапке (kegl_px=%s liniya=%s)"
                          % (sid, params.get("kegl_px"), params.get("liniya")), file=sys.stderr)
                    continue
                with tempfile.TemporaryDirectory() as tmp:
                    _, html = compile_slide_html(slide_path)
                    html_path = Path(tmp) / "slide.html"
                    html_path.write_text(html, encoding="utf-8")
                    res = vmeshchenie.podobrat_slide(page, html_path, axis=axis)
                if res["chosen"] is None:
                    raise SystemExit(
                        "подбор: %s — ни одна проба не влезла внутри жёстких зон "
                        "(см. `vmeshchenie.py --demo-zony`)" % sid)
                vmeshchenie.apply_to_card(slide_path, res["chosen"])
                podobrano += 1
                print("подбор: %s — kegl=%.1f liniya=%s" % (
                    sid, res["chosen"]["kegl"], res["chosen"].get("liniya")), file=sys.stderr)
        finally:
            browser.close()
    print("подбор типографики: %d слайдов подобрано, %d пропущено (явные значения в шапке)"
          % (podobrano, propushcheno))
    return podobrano, propushcheno


def _order(slide_order, tips):
    """slide_order автора + принудительно oblozhka первой, finalnyj последней —
    по ТИПУ (устойчиво к тому, где автор их фактически перечислил)."""
    cover = [s for s in slide_order if tips.get(s) == "oblozhka"]
    final = [s for s in slide_order if tips.get(s) == "finalnyj"]
    middle = [s for s in slide_order if tips.get(s) not in ("oblozhka", "finalnyj")]
    return cover + middle + final


def build(src, out, jobs=None, podbor=True):
    from slaid import load_illustrations as load_ill  # переиспользуем загрузчик Э2/Э3
    sys.path.insert(0, str(GENERATOR))
    from build_deck import parse_brief, read_text  # READ-ONLY импорт (Я6)

    src = Path(src)
    slajdy_dir = src / "slajdy"
    illustrations_dir = src / "illustracii"  # ИМЯ ПО СПЕЦИФИКАЦИИ (Я2), не "illustrations"
    slide_paths = sorted(slajdy_dir.glob("*/slaid.md"))
    if not slide_paths:
        raise SystemExit("нет слайдов в %s (ищу */slaid.md)" % slajdy_dir)

    brief = src / "brief.md"
    meta = parse_brief(read_text(brief)) if brief.is_file() else {}
    have = {p.parent.name for p in slide_paths}
    # status слайда узнаём, только распарсив карточку — до первого прохода компиляции
    # его не знаем, поэтому лёгкая предпроверка (missing/extra) читает шапки сама,
    # не дожидаясь параллельной сборки (нужно ДО того, как решать `slide_order` по
    # умолчанию, и ошибка тут дешевле, чем после N параллельных компиляций).
    from formaty import parse_card
    status_by_sid = {}
    for p in slide_paths:
        params, _ = parse_card(read_text(p), sid=p.parent.name)
        status_by_sid[p.parent.name] = params.get("status", "v_deke")

    slide_order = meta.get("slide_order") or [sid for sid in sorted(have)
                                               if status_by_sid[sid] != "rezerv"]
    missing = [s for s in slide_order if s not in have]
    if missing:
        raise SystemExit("brief.md называет слайды, которых нет в slajdy/: %s" % missing)
    # "лишний" на диске — ошибка, ТОЛЬКО если он не в резерве: резервный слайд по
    # Я1 §4-бис легально сидит в папке и в slide_order может не значиться вовсе.
    extra = sorted(s for s in have - set(slide_order) if status_by_sid[s] != "rezerv")
    if extra:
        raise SystemExit("в slajdy/ есть слайды (не в резерве), не названные в "
                          "brief.md slide_order: %s" % extra)
    # 🔴 резерв ИСКЛЮЧАЕТСЯ из компиляции безусловно — даже если автор по ошибке
    # (или намеренно, как явная документация) оставил его в slide_order: «лежит в
    # папке, в дек не входит» (Я1 §4-бис) — свойство САМОГО слайда, не манифеста.
    slide_order = [s for s in slide_order if status_by_sid[s] != "rezerv"]

    jobs = jobs or os.cpu_count() or 1
    # 🔴 `fork`, не дефолт macOS (`spawn`). Компиляция слайда — регэкспы над
    # несколькими КБ текста, микросекунды; `spawn` пересобирает интерпретатор и
    # заново импортирует модули НА КАЖДЫЙ воркер (десятки мс) — накладные расходы
    # старта перевешивают всю полезную работу разом (замерено этим же прогоном:
    # `-j 15` на 15 слайдах стабильно МЕДЛЕННЕЕ `-j 1`, реальный wall time 0.26с
    # против 0.15с). `fork` дешевле в разы (не пересобирает интерпретатор с нуля);
    # если и он не даёт выигрыша — это законный отрицательный результат про ЭТУ
    # задачу (лёгкая CPU-работа), а не брак реализации, и назван в отчёте как есть.
    # Компилируем ТОЛЬКО то, что реально войдёт в дек — резервные слайды могут быть
    # намеренно недописаны и не обязаны собираться (Я1 §4-бис: «в дек не входит»).
    to_compile = [p for p in slide_paths if p.parent.name in slide_order]

    if podbor:
        _podobrat_tipografiku(to_compile)

    ctx = mp.get_context("fork") if hasattr(os, "fork") else None
    with ProcessPoolExecutor(max_workers=jobs, mp_context=ctx) as ex:
        results = list(ex.map(_compile_one, [str(p) for p in to_compile]))

    by_id = {sid: (tip, status, ills, css, html, n_scenes)
              for sid, tip, status, ills, css, html, n_scenes in results}
    tips = {sid: tip for sid, (tip, _, _, _, _, _) in by_id.items()}
    order = _order(slide_order, tips)

    all_ills = []
    seen_ill = set()
    for sid in order:
        for stem in by_id[sid][2]:
            if stem not in seen_ill:
                seen_ill.add(stem)
                all_ills.append(stem)
    templates = load_ill(all_ills, illustrations_dir) if all_ills else ""

    all_css = "\n".join(by_id[sid][3] for sid in order)
    sections = "\n".join(
        '<section class="slide" id="%s" data-scenes="%d">\n%s\n</section>'
        % (sid, by_id[sid][5], by_id[sid][4])
        for sid in order)
    # 🔴 каскад ОДИН на весь дек (общий <style>) — обязан покрывать МАКСИМУМ сцен
    # среди всех слайдов, не только последнего скомпилированного (Э8 захода
    # kartochka-i-sborka, критерий 4; см. slaid.py — та же дыра без этого).
    n_scenes_dek = max([1] + [by_id[sid][5] for sid in order])

    from tipy import GLOBAL_CSS
    from build_deck import scene_cascade_css  # noqa: E402  (READ-ONLY импорт, Я6)
    fonts_css = read_text(SKELETON / "fonts" / "faces.css")
    katex_css = read_text(SKELETON / "katex.css")  # см. slaid.py — Э5 захода solver-vmeshcheniya
    tokens_css = read_text(SKELETON / "tokens.css")
    base_css = read_text(SKELETON / "base.css").replace("{{SCENE_CASCADE}}", scene_cascade_css(n_scenes_dek))
    engine_js = read_text(SKELETON / "engine.js")

    doc = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>%(title)s</title>
<style>
%(fonts)s
%(katex)s
%(tokens)s
%(base)s
%(global_css)s
%(css)s
</style>
</head>
<body>
<div id="stage"><div id="deck">
%(sections)s
</div></div>
<div id="hint">← → листать · F — экран · B — чёрный</div>
%(templates)s
<script>%(engine)s</script>
</body>
</html>
""" % {
        "title": meta.get("title", src.name),
        "fonts": fonts_css,
        "katex": katex_css,
        "tokens": tokens_css,
        "base": base_css,
        "global_css": GLOBAL_CSS,
        "css": all_css,
        "sections": sections,
        "templates": templates,
        "engine": engine_js,
    }

    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    n_rezerv = sum(1 for s in status_by_sid.values() if s == "rezerv")
    return len(order), n_rezerv, out


def main():
    ap = argparse.ArgumentParser(description="Параллельная сборка дека из папки лекции")
    ap.add_argument("src", help="папка <лекция> (содержит slajdy/, illustracii/, brief.md)")
    ap.add_argument("-o", "--out", required=True, help="путь выхода .html")
    ap.add_argument("-j", "--jobs", type=int, default=None, help="число процессов (по умолчанию — ядра)")
    ap.add_argument("--bez-podbora", action="store_true",
                     help="не подбирать типографику солвером — собрать как есть "
                          "(умолчание: подбор ВКЛЮЧЁН, Р3 захода porcia-1-zamknut-konvejer)")
    args = ap.parse_args()
    n, n_rezerv, out = build(args.src, args.out, jobs=args.jobs, podbor=not args.bez_podbora)
    print("собран дек: слайдов в деке %d, в резерве %d → %s" % (n, n_rezerv, out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
