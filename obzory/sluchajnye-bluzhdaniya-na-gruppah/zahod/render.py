#!/usr/bin/env python3
"""Рендер иллюстраций вкладки в PNG для глазной сверки (cairosvg, без браузера)."""
import re, pathlib, cairosvg
D = pathlib.Path(__file__).resolve().parent
gen = (D.parent.parent / "_generator/build_doc.py").read_text(encoding="utf-8")
css = gen[gen.index(".s-line{"):gen.index(".s-ar-a{")]
css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)   # в комментариях движка есть <circle> — ломает XML
css += ".s-ar-a{fill:#2f6e8e} .s-ar-m{fill:#726c60}"
for k, v in {"--text": "#211f1b", "--muted": "#726c60", "--accent": "#2f6e8e",
             "--warm": "#c9743a", "--shade": "#dfeaf0",
             "--sans": "Helvetica,Arial,sans-serif"}.items():
    css = css.replace("var(%s)" % k, v)
(D / "render").mkdir(exist_ok=True)
md = (D.parent / "01-poyya-kesten.md").read_text(encoding="utf-8")
for m in re.finditer(r'(<svg viewBox="0 0 (\d+) (\d+)".*?</svg>)', md, re.S):
    svg, w, h = m.group(1), int(m.group(2)), int(m.group(3))
    name = re.search(r'aria-label="([^"]+)"', svg).group(1)
    cairosvg.svg2png(bytestring=svg.replace(">", "><style>%s</style>" % css, 1).encode(),
                     write_to=str(D / "render" / (name + ".png")),
                     output_width=w * 2, output_height=h * 2, background_color="#fbfaf6")
    print("ok", name, w, h)
