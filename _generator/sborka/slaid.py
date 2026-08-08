#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Компилятор ОДНОГО слайда — параметры → самодостаточный HTML (Э2/Э3 захода
kompilyator-slajda, раскладка обновлена Э6 захода kartochka-i-sborka).

  python3 _generator/sborka/slaid.py <лекция>/slajdy/s06/slaid.md -o /tmp/s06.html [--kadr]

Раскладка — Я2: `<лекция>/slajdy/<imya>/slaid.md`, пул иллюстраций — ОТДЕЛЬНО,
`<лекция>/illustracii/` (не внутри папки слайда, имя по спецификации, не
англ. "illustrations"). `sid` для HTML/`data-ill` — ИМЯ ПАПКИ слайда, не стем
файла (файл всегда называется `slaid.md`).

Выход — тот же канон, что несёт `_generator/skeleton/`: токены, base.css, шрифты,
движок `engine.js` дословно (Я3: «отсюда берутся цвета, шрифты и оформление
служебных слайдов — не изобретай свои»). Отличие от полного дека — только один
`<section class="slide">`, без {{SLIDES}}-конвейера build_deck.py (тот НЕ трогается,
это параллельный путь).

`--kadr` требует ту же разметку, что ищет `_generator/render.py`: `.slide` без
`[data-skip]`, `#stage`, дословный `engine.js` — иначе `render.py` тихо отрендерит
пустой кадр (см. Э3 захода, предупреждение). Кадр кладётся РЯДОМ с HTML,
`<out>.png` вместо `<out>.html`.
"""
import argparse
import json
import sys
from pathlib import Path

SBORKA = Path(__file__).resolve().parent
GENERATOR = SBORKA.parent
SKELETON = GENERATOR / "skeleton"
sys.path.insert(0, str(SBORKA))
sys.path.insert(0, str(GENERATOR))
from formaty import parse_slide, render_body, FormatSlaida  # noqa: E402
from tipy import compile_tip, TipVerstki, GLOBAL_CSS  # noqa: E402
from build_deck import max_scenes, scene_cascade_css  # noqa: E402  (READ-ONLY импорт, Я6)


def load_math_cache(lekcija_dir):
    """<лекция>/math/katex.json → dict, тот же приём, что build_deck.py:376-377
    (READ-ONLY чтение оттуда — Э5 захода solver-vmeshcheniya). Файла нет → {}, и
    формулы уходят видимым маркером `⟦MISSING-MATH:...⟧`, не молча."""
    math_path = Path(lekcija_dir) / "math" / "katex.json"
    if not math_path.is_file():
        return {}
    return json.loads(_read(math_path))


def _read(p):
    return p.read_text(encoding="utf-8")


def load_illustrations(stems, illustrations_dir):
    """<stem> → <template id="ill-<stem>">…</template>. Пул иллюстраций (Э5 захода
    kartochka-i-sborka, раскладка Я2): `<лекция>/illustracii/<stem>/risunok.svg`
    (или `risunok.html`) — ПАПКА на иллюстрацию, не плоский файл; рядом с рисунком
    в той же папке лежит `zakaz.md` (человеку/гейту, компилятор его не читает)."""
    out = []
    for stem in stems:
        base = Path(stem).stem  # illustracii может нести "s06-a.svg" — имя ФАЙЛА (Э1)
        folder = illustrations_dir / base
        svg = folder / "risunok.svg"
        html = folder / "risunok.html"
        if svg.is_file():
            content = _read(svg)
        elif html.is_file():
            content = _read(html)
        else:
            raise FormatSlaida(
                "иллюстрация '%s' не найдена в %s (ни risunok.svg, ни risunok.html)"
                % (base, folder))
        out.append('<template id="ill-%s">%s</template>' % (base, content))
    return "\n".join(out)


def compile_slide_html(slide_path, illustrations_dir=None, title=None):
    """.md слайда → (sid, полный самодостаточный HTML документа). `sid` — имя
    ПАПКИ слайда (`slajdy/<sid>/slaid.md`), не стем файла.

    `slide_path` принимает И файл (`slajdy/<sid>/slaid.md`), И саму папку слайда
    (`slajdy/<sid>`) — раньше папка давала `IsADirectoryError` (Р4 захода
    porcia-1-zamknut-konvejer: интерфейсы путей `deck.py`/`slaid.py` разъехались,
    деку нужна папка лекции, а `slaid.py` требовал файл слайда буквально)."""
    slide_path = Path(slide_path)
    if slide_path.is_dir():
        slide_path = slide_path / "slaid.md"
    sid = slide_path.parent.name
    text = _read(slide_path)
    params, body_md = parse_slide(text, sid=sid)
    # `illustracii` в шапке — ИМЕНА ФАЙЛОВ (Э1: "ИМЕНА файлов из illustrations/"), а
    # `data-ill`/id шаблона везде дальше — stem без расширения (движок ищет
    # `#ill-<stem>`). Нормализация ЗДЕСЬ, один раз, а не по месту в каждом типе —
    # иначе typy.py и load_illustrations разъезжаются в написании имени (нашёл сам
    # этим же прогоном: .svg долетал до data-ill, шаблон не находился, панель пустая).
    params["illustracii"] = [Path(s).stem for s in (params.get("illustracii") or [])]
    acc_tag = "span"
    # lekcija_dir = <лекция>/slajdy/<sid>/slaid.md → parents[2] = <лекция> (тот же
    # расчёт, что ниже для illustrations_dir по умолчанию)
    math = load_math_cache(slide_path.parents[2])
    body_html = render_body(body_md, acc_tag=acc_tag, math=math, sid=sid)
    css, slide_html = compile_tip(sid, params, body_html)
    # 🔴 БЕЗ `data-scenes` движок (`scenesOf`, engine.js) считает слайд односценовым
    # безусловно, и БЕЗ порождённого каскада (`{{SCENE_CASCADE}}`) правило
    # `[data-scene-from]{opacity:0}` (base.css) ничем не переопределяется — пропуск
    # ({@N|…} внутри блока, Э2 захода kartochka-i-sborka) компилировался бы
    # НАВСЕГДА невидимым, не «до своей сцены», а вообще. Найдено этим же прогоном
    # (Э8, живой кадр `s03`, критерий 4) — компилятор двух прошлых заходов не нёс
    # ни того, ни другого.
    n_scenes = max_scenes(slide_html)

    if illustrations_dir is None:
        # slide_path = <лекция>/slajdy/<sid>/slaid.md → parents[2] = <лекция>
        illustrations_dir = slide_path.parents[2] / "illustracii"
    stems = params["illustracii"]
    templates = load_illustrations(stems, illustrations_dir) if stems else ""

    fonts_css = _read(SKELETON / "fonts" / "faces.css")
    # 🔴 БЕЗ ЭТОГО (Э5 захода solver-vmeshcheniya, найдено живым прогоном): формула
    # рендерится ДВАЖДЫ — видимая KaTeX-разметка и следом голый текст MathML-аннотации,
    # потому что скелет не нёс ядро katex.min.css (правило, прячущее `.katex-mathml`).
    # Раньше это было незаметно: кэш формул был пуст, всё уходило в MISSING-MATH.
    # `katex.css` — дословный порт секции [1] teorkat-vvedenie/src/overlay.css
    # (READ-ONLY источник, машинно порождён `sobrat_overlay.py`, шрифты+ядро KaTeX).
    katex_css = _read(SKELETON / "katex.css")
    tokens_css = _read(SKELETON / "tokens.css")
    base_css = _read(SKELETON / "base.css").replace("{{SCENE_CASCADE}}", scene_cascade_css(n_scenes))
    engine_js = _read(SKELETON / "engine.js")

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
<section class="slide" id="%(sid)s" data-scenes="%(n_scenes)d">
%(slide)s
</section>
</div></div>
<div id="hint">← → листать · F — экран · B — чёрный</div>
%(templates)s
<script>%(engine)s</script>
</body>
</html>
""" % {
        "title": title or sid,
        "n_scenes": n_scenes,
        "fonts": fonts_css,
        "katex": katex_css,
        "tokens": tokens_css,
        "base": base_css,
        "global_css": GLOBAL_CSS,
        "css": css,
        "sid": sid,
        "slide": slide_html,
        "templates": templates,
        "engine": engine_js,
    }
    return sid, doc


def render_kadr(html_path, png_path):
    """PNG рядом с HTML — через существующий render.py (Я6, Э3), без правки render.py."""
    render_mod_dir = str(GENERATOR)
    if render_mod_dir not in sys.path:
        sys.path.insert(0, render_mod_dir)
    import render as render_mod  # noqa: E402  (импорт read-only модуля render.py)
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        render_mod.shoot(str(html_path), tmp)
        src_png = Path(tmp) / "00.png"
        if not src_png.is_file():
            raise RuntimeError("render.py не создал 00.png — see stdout above")
        png_path.write_bytes(src_png.read_bytes())


def main():
    ap = argparse.ArgumentParser(description="Компилятор одного слайда → самодостаточный HTML")
    ap.add_argument("slide", help="путь к <лекция>/slajdy/<id>/slaid.md")
    ap.add_argument("-o", "--out", required=True, help="путь выхода .html")
    ap.add_argument("--kadr", action="store_true", help="снять PNG-кадр рядом с HTML")
    args = ap.parse_args()

    try:
        sid, doc = compile_slide_html(args.slide)
    except (FormatSlaida, TipVerstki) as e:
        print("ОШИБКА: %s" % e, file=sys.stderr)
        return 1

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    print("собрано: %s → %s" % (sid, out))

    if args.kadr:
        png = out.with_suffix(".png")
        render_kadr(out, png)
        ok = png.is_file() and png.stat().st_size > 0
        print("кадр: %s (%d байт)%s" % (png, png.stat().st_size if png.is_file() else 0,
                                        "" if ok else "  ПУСТО/НЕТ — см. Э3 захода"))
        if not ok:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
