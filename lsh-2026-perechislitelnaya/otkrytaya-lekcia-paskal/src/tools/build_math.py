#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Кэш формул дека: content/*.md → math/katex.json + overlay.css (CSS и шрифты KaTeX).

Зачем. Генератор `_generator/build_deck.py` — чистая stdlib без сети: он не умеет
набирать TeX, он подставляет ГОТОВЫЙ html формулы из кэша `math/katex.json`
(SLIDE-FORMAT.md, ключ = TeX-исходник дословно). `harvest_katex.py` наполняет такой
кэш из УЖЕ отрендеренной колоды — для нового дека брать нечего. Этот скрипт закрывает
дыру: набирает формулы настоящим KaTeX один раз и кладёт результат в кэш. Дек остаётся
самодостаточным — KaTeX в рантайме не нужен, внешних URL нет (гейт линтера №4).

Запуск (после ЛЮБОЙ правки формул в content/*.md):

    cd <дек>/src/tools && npm install katex@0.16.9    # один раз
    python3 <дек>/src/tools/build_math.py

Путь к KaTeX ищется в таком порядке: --katex → $KATEX_DIST → tools/node_modules/katex/dist.

Что пишет:
  math/katex.json — {tex: готовый html}, ключ дословно как в `$…$`;
  overlay.css     — katex.min.css со ВШИТЫМИ в base64 шрифтами формул (те семейства,
                    что реально встретились в наборе; остальные @font-face выброшены,
                    иначе они тянули бы относительные url и молча падали в 404).

Формулы НЕ выдумываются: набирается ровно то, что нашлось в `content/*.md`. Формула,
которую скрипт не увидел, всплывёт как ⟦MISSING-MATH:…⟧ и уронит линтер — это и есть
гейт, который может провалиться.
"""
import argparse, base64, json, os, re, subprocess, sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
MATH_RE = re.compile(r"\$(.+?)\$")

# семейство KaTeX → файл woff2 (вшиваем только те, что реально понадобились)
FAMILY_FILE = {
    "KaTeX_Main": ["KaTeX_Main-Regular", "KaTeX_Main-Bold", "KaTeX_Main-Italic"],
    "KaTeX_Math": ["KaTeX_Math-Italic", "KaTeX_Math-BoldItalic"],
    "KaTeX_Size1": ["KaTeX_Size1-Regular"],
    "KaTeX_Size2": ["KaTeX_Size2-Regular"],
    "KaTeX_Size3": ["KaTeX_Size3-Regular"],
    "KaTeX_Size4": ["KaTeX_Size4-Regular"],
    "KaTeX_AMS": ["KaTeX_AMS-Regular"],
    "KaTeX_Caligraphic": ["KaTeX_Caligraphic-Regular", "KaTeX_Caligraphic-Bold"],
    "KaTeX_Fraktur": ["KaTeX_Fraktur-Regular", "KaTeX_Fraktur-Bold"],
    "KaTeX_SansSerif": ["KaTeX_SansSerif-Regular", "KaTeX_SansSerif-Bold", "KaTeX_SansSerif-Italic"],
    "KaTeX_Script": ["KaTeX_Script-Regular"],
    "KaTeX_Typewriter": ["KaTeX_Typewriter-Regular"],
}


def collect_tex():
    """Все $…$ из content/*.md, в порядке появления, без повторов."""
    out = []
    for p in sorted((SRC / "content").glob("*.md")):
        for m in MATH_RE.finditer(p.read_text(encoding="utf-8")):
            tex = m.group(1)
            if tex not in out:
                out.append(tex)
    return out


def render(tex_list, katex_dist):
    """Набор формул одним запуском node — по одному процессу на формулу было бы вдвое дольше."""
    script = (
        "const katex=require(%s);"
        "const inp=JSON.parse(require('fs').readFileSync(0,'utf8'));"
        "const out={};for(const t of inp){out[t]=katex.renderToString(t,{throwOnError:true});}"
        "process.stdout.write(JSON.stringify(out));"
        % json.dumps(str(katex_dist / "katex.js"))
    )
    r = subprocess.run(["node", "-e", script], input=json.dumps(tex_list),
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("KaTeX упал:\n" + r.stderr.strip())
    return json.loads(r.stdout)


def build_overlay(rendered, katex_dist):
    """katex.min.css, где @font-face использованных семейств несут base64-woff2,
    а неиспользованных — выброшены целиком."""
    css = (katex_dist / "katex.min.css").read_text(encoding="utf-8")
    html = "".join(rendered.values())
    used = {fam for fam in FAMILY_FILE if re.search(r"\b" + fam + r"\b", css) and _in_use(fam, html)}
    used.add("KaTeX_Main")  # базовое семейство набора, встречается всегда

    def one(m):
        block = m.group(0)
        fam = re.search(r"font-family:\s*([A-Za-z_0-9]+)", block)
        woff2 = re.search(r"url\(fonts/([A-Za-z_0-9-]+)\.woff2\)", block)
        if not fam or not woff2 or fam.group(1) not in used:
            return ""
        f = katex_dist / "fonts" / (woff2.group(1) + ".woff2")
        if not f.is_file():
            return ""
        b64 = base64.b64encode(f.read_bytes()).decode()
        return re.sub(r"src:[^;}]+", 'src:url(data:font/woff2;base64,%s) format("woff2")', block, count=1) % b64

    css = re.sub(r"@font-face\{[^}]*\}", one, css)
    head = ("/* ⚠ СГЕНЕРИРОВАНО src/tools/build_math.py — РУКАМИ НЕ ПРАВИТЬ.\n"
            "   katex.min.css + вшитые base64-woff2 шрифты формул (%s).\n"
            "   Пересобрать: python3 src/tools/build_math.py */\n" % ", ".join(sorted(used)))
    tail = ("\n/* формула в теле слайда: кегль наравне с текстом, акцент красит и её */\n"
            ".slide .t-body .katex { font-size: 1em; }\n"
            ".slide .t-body .acc .katex, .slide .t-body .acc .katex * { color: var(--brick); }\n")
    return head + css + tail


def _in_use(fam, html):
    """Семейство считается использованным, если в наборе есть класс, который его включает."""
    marks = {
        "KaTeX_Main": ["mord", "mbin", "mrel"], "KaTeX_Math": ["mathnormal"],
        "KaTeX_Size1": ["size1", "delim-size1"], "KaTeX_Size2": ["size2"],
        "KaTeX_Size3": ["size3"], "KaTeX_Size4": ["size4"], "KaTeX_AMS": ["amsrm", "mathbb"],
        "KaTeX_Caligraphic": ["mathcal"], "KaTeX_Fraktur": ["mathfrak"],
        "KaTeX_SansSerif": ["mathsf", "textsf"], "KaTeX_Script": ["mathscr"],
        "KaTeX_Typewriter": ["mathtt"],
    }
    return any(m in html for m in marks.get(fam, []))


def main():
    ap = argparse.ArgumentParser(description="кэш формул дека: content/*.md → math/katex.json + overlay.css")
    ap.add_argument("--katex", help="папка dist установленного katex")
    args = ap.parse_args()

    katex_dist = Path(args.katex or os.environ.get("KATEX_DIST")
                      or (SRC / "tools" / "node_modules" / "katex" / "dist"))
    if not (katex_dist / "katex.js").is_file():
        sys.exit("KaTeX не найден: %s\nПоставь: cd %s && npm install katex@0.16.9"
                 % (katex_dist, SRC / "tools"))

    tex_list = collect_tex()
    if not tex_list:
        sys.exit("в content/*.md не нашлось ни одной $формулы$ — проверь, туда ли смотрю")
    rendered = render(tex_list, katex_dist)

    (SRC / "math").mkdir(exist_ok=True)
    (SRC / "math" / "katex.json").write_text(
        json.dumps(rendered, ensure_ascii=False, indent=1), encoding="utf-8")
    (SRC / "overlay.css").write_text(build_overlay(rendered, katex_dist), encoding="utf-8")

    print("── ФОРМУЛЫ ──")
    for t in tex_list:
        print("  ✓ $%s$" % t)
    print("  math/katex.json — %d формул(ы)" % len(rendered))
    print("  overlay.css — %d КБ" % (len((SRC / 'overlay.css').read_bytes()) // 1024))


if __name__ == "__main__":
    main()
