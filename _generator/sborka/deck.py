#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сборка ЦЕЛОГО дека — параллельно по слайдам (Э4 захода).

  python3 _generator/sborka/deck.py <лекция>/src2 -o <лекция>/src2/dist/index.html [-j 15]

Слайды независимы (Э1: параметры + текст, никаких перекрёстных ссылок между файлами
слайдов), поэтому компиляция каждого — отдельный процесс (`ProcessPoolExecutor`,
stdlib, без pip). Порядок — `brief.md:slide_order` тем же диалектом, что читает
`build_deck.py` (Я6, `parse_brief`, READ-ONLY импорт); `oblozhka` принудительно
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
    """Воркер отдельного процесса: путь к .md → (sid, tip, illustracii-стемы, css, html).
    Импорты — ВНУТРИ функции: `ProcessPoolExecutor` на macOS стартует процессы
    методом spawn, каждый воркер импортирует этот модуль заново с нуля."""
    import sys as _sys
    from pathlib import Path as _Path
    sb = _Path(__file__).resolve().parent
    if str(sb) not in _sys.path:
        _sys.path.insert(0, str(sb))
    from formaty import parse_slide, render_body
    from tipy import compile_tip

    slide_path = _Path(slide_path_str)
    sid = slide_path.stem
    text = slide_path.read_text(encoding="utf-8")
    params, body_md = parse_slide(text, sid=sid)
    params["illustracii"] = [_Path(s).stem for s in (params.get("illustracii") or [])]
    body_html = render_body(body_md, acc_tag="span")
    css, html = compile_tip(sid, params, body_html)
    return sid, params.get("tip"), params["illustracii"], css, html


def _order(slide_order, tips):
    """slide_order автора + принудительно oblozhka первой, finalnyj последней —
    по ТИПУ (устойчиво к тому, где автор их фактически перечислил)."""
    cover = [s for s in slide_order if tips.get(s) == "oblozhka"]
    final = [s for s in slide_order if tips.get(s) == "finalnyj"]
    middle = [s for s in slide_order if tips.get(s) not in ("oblozhka", "finalnyj")]
    return cover + middle + final


def build(src, out, jobs=None):
    from slaid import load_illustrations as load_ill  # переиспользуем загрузчик Э2/Э3
    sys.path.insert(0, str(GENERATOR))
    from build_deck import parse_brief, read_text  # READ-ONLY импорт (Я6)

    src = Path(src)
    slides_dir = src / "slides"
    illustrations_dir = src / "illustrations"
    slide_paths = sorted(slides_dir.glob("*.md"))
    if not slide_paths:
        raise SystemExit("нет слайдов в %s" % slides_dir)

    brief = src / "brief.md"
    meta = parse_brief(read_text(brief)) if brief.is_file() else {}
    slide_order = meta.get("slide_order") or [p.stem for p in slide_paths]
    have = {p.stem for p in slide_paths}
    missing = [s for s in slide_order if s not in have]
    if missing:
        raise SystemExit("brief.md называет слайды, которых нет в slides/: %s" % missing)
    extra = have - set(slide_order)
    if extra:
        raise SystemExit("в slides/ есть слайды, не названные в brief.md slide_order: %s"
                          % sorted(extra))

    jobs = jobs or os.cpu_count() or 1
    # 🔴 `fork`, не дефолт macOS (`spawn`). Компиляция слайда — регэкспы над
    # несколькими КБ текста, микросекунды; `spawn` пересобирает интерпретатор и
    # заново импортирует модули НА КАЖДЫЙ воркер (десятки мс) — накладные расходы
    # старта перевешивают всю полезную работу разом (замерено этим же прогоном:
    # `-j 15` на 15 слайдах стабильно МЕДЛЕННЕЕ `-j 1`, реальный wall time 0.26с
    # против 0.15с). `fork` дешевле в разы (не пересобирает интерпретатор с нуля);
    # если и он не даёт выигрыша — это законный отрицательный результат про ЭТУ
    # задачу (лёгкая CPU-работа), а не брак реализации, и назван в отчёте как есть.
    ctx = mp.get_context("fork") if hasattr(os, "fork") else None
    with ProcessPoolExecutor(max_workers=jobs, mp_context=ctx) as ex:
        results = list(ex.map(_compile_one, [str(p) for p in slide_paths]))

    by_id = {sid: (tip, ills, css, html) for sid, tip, ills, css, html in results}
    tips = {sid: tip for sid, (tip, _, _, _) in by_id.items()}
    order = _order(slide_order, tips)

    all_ills = []
    seen_ill = set()
    for sid in order:
        for stem in by_id[sid][1]:
            if stem not in seen_ill:
                seen_ill.add(stem)
                all_ills.append(stem)
    templates = load_ill(all_ills, illustrations_dir) if all_ills else ""

    all_css = "\n".join(by_id[sid][2] for sid in order)
    sections = "\n".join('<section class="slide" id="%s">\n%s\n</section>' % (sid, by_id[sid][3])
                          for sid in order)

    from tipy import GLOBAL_CSS
    fonts_css = read_text(SKELETON / "fonts" / "faces.css")
    tokens_css = read_text(SKELETON / "tokens.css")
    base_css = read_text(SKELETON / "base.css").replace("{{SCENE_CASCADE}}", "")
    engine_js = read_text(SKELETON / "engine.js")

    doc = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>%(title)s</title>
<style>
%(fonts)s
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
    return len(order), out


def main():
    ap = argparse.ArgumentParser(description="Параллельная сборка дека из src2/")
    ap.add_argument("src", help="папка <лекция>/src2 (содержит slides/, illustrations/, brief.md)")
    ap.add_argument("-o", "--out", required=True, help="путь выхода .html")
    ap.add_argument("-j", "--jobs", type=int, default=None, help="число процессов (по умолчанию — ядра)")
    args = ap.parse_args()
    n, out = build(args.src, args.out, jobs=args.jobs)
    print("собран дек: %d слайдов → %s" % (n, out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
