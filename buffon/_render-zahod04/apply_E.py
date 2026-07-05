#!/usr/bin/env python3
import pathlib
f = pathlib.Path(__file__).resolve().parent.parent / "index.html"
s = f.read_text()

D_KATEX = ('<span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML">'
 '<semantics><mrow><mi mathvariant="bold-italic">d</mi></mrow><annotation encoding="application/x-tex">'
 '\\boldsymbol{d}</annotation></semantics></math></span><span class="katex-html" aria-hidden="true">'
 '<span class="base"><span class="strut" style="height:0.6944em;"></span><span class="mord"><span class="mord">'
 '<span class="mord boldsymbol">d</span></span></span></span></span></span>')

# ---- Part 1: de-spoiler question paragraph ----
old_q = ('<p data-scene-from="2"><b>Чему равна вероятность, если диаметр ' + D_KATEX +
         '?: <span class="fill"><span class="blur-reveal" data-reveal="3"><span class="acc">' + D_KATEX +
         '</span></span></span></b></p>')
new_q = ('<p data-scene-from="2"><b>Чему равна вероятность, если диаметр ' + D_KATEX + '?</b></p>\n'
         '      <p data-scene-from="3">Тогда вероятность равна <span class="acc">' + D_KATEX + '</span></p>')
assert s.count(old_q) == 1, f"old_q count={s.count(old_q)}"
s = s.replace(old_q, new_q)

# ---- Parts 2+3: thermometer SVG (steel full-height, grouped red bands, ¼/d label) ----
old_tpl = ('<template id="ill-sl-interval-1"><svg viewBox="0 0 88 649" xmlns="http://www.w3.org/2000/svg">'
 '<rect x="0" y="0" width="88" height="649" fill="var(--card)"/>'
 '<rect x="0" y="29.3" width="37.2" height="143.6" fill="var(--brick)" fill-opacity="0.16"/>'
 '<rect x="0" y="460.1" width="37.2" height="143.6" fill="var(--brick)" fill-opacity="0.16"/>'
 '<line x1="0" y1="29.3" x2="88" y2="29.3" stroke="var(--rule)" stroke-width="1.5"/>'
 '<line x1="0" y1="603.7" x2="88" y2="603.7" stroke="var(--rule)" stroke-width="1.5"/>'
 '<line x1="42.7" y1="172.9" x2="42.7" y2="460.1" stroke="var(--steel)" stroke-width="7"/>'
 '<line x1="42.7" y1="29.3" x2="42.7" y2="172.9" stroke="var(--brick)" stroke-width="11" stroke-linecap="round"/>'
 '<line x1="42.7" y1="460.1" x2="42.7" y2="603.7" stroke="var(--brick)" stroke-width="11" stroke-linecap="round"/>'
 '<line x1="29.7" y1="29.3" x2="55.7" y2="29.3" stroke="var(--ink)" stroke-width="2"/>'
 '<line x1="29.7" y1="172.9" x2="55.7" y2="172.9" stroke="var(--ink)" stroke-width="2"/>'
 '<line x1="29.7" y1="316.5" x2="55.7" y2="316.5" stroke="var(--ink)" stroke-width="2"/>'
 '<line x1="29.7" y1="460.1" x2="55.7" y2="460.1" stroke="var(--ink)" stroke-width="2"/>'
 '<line x1="29.7" y1="603.7" x2="55.7" y2="603.7" stroke="var(--ink)" stroke-width="2"/></svg></template>')
new_tpl = ('<template id="ill-sl-interval-1"><svg viewBox="0 0 88 649" xmlns="http://www.w3.org/2000/svg">'
 '<rect x="0" y="0" width="88" height="649" fill="var(--card)"/>'
 '<line x1="0" y1="29.3" x2="88" y2="29.3" stroke="var(--rule)" stroke-width="1.5"/>'
 '<line x1="0" y1="603.7" x2="88" y2="603.7" stroke="var(--rule)" stroke-width="1.5"/>'
 '<line x1="42.7" y1="29.3" x2="42.7" y2="603.7" stroke="var(--steel)" stroke-width="7"/>'
 '<g class="xz xtop"><rect x="0" y="29.3" width="37.2" height="143.6" fill="var(--brick)" fill-opacity="0.16"/>'
 '<line x1="42.7" y1="29.3" x2="42.7" y2="172.9" stroke="var(--brick)" stroke-width="11" stroke-linecap="round"/></g>'
 '<g class="xz xbot"><rect x="0" y="460.1" width="37.2" height="143.6" fill="var(--brick)" fill-opacity="0.16"/>'
 '<line x1="42.7" y1="460.1" x2="42.7" y2="603.7" stroke="var(--brick)" stroke-width="11" stroke-linecap="round"/></g>'
 '<line x1="29.7" y1="29.3" x2="55.7" y2="29.3" stroke="var(--ink)" stroke-width="2"/>'
 '<line x1="29.7" y1="172.9" x2="55.7" y2="172.9" stroke="var(--ink)" stroke-width="2"/>'
 '<line x1="29.7" y1="316.5" x2="55.7" y2="316.5" stroke="var(--ink)" stroke-width="2"/>'
 '<line x1="29.7" y1="460.1" x2="55.7" y2="460.1" stroke="var(--ink)" stroke-width="2"/>'
 '<line x1="29.7" y1="603.7" x2="55.7" y2="603.7" stroke="var(--ink)" stroke-width="2"/>'
 '<text class="thermo-lbl thermo-q" x="60" y="112" font-family="Georgia, serif" font-size="30" fill="var(--brick)">¼</text>'
 '<text class="thermo-lbl thermo-d" x="62" y="112" font-family="Georgia, serif" font-style="italic" font-size="30" fill="var(--brick)">d</text>'
 '</svg></template>')
assert s.count(old_tpl) == 1, f"old_tpl count={s.count(old_tpl)}"
s = s.replace(old_tpl, new_tpl)

# ---- CSS: after the p-thermo rule ----
old_css = '#sl-interval .p-thermo { position: absolute; left: 54px; top: 80px; width: 88px; height: 649px; }'
new_css = (old_css + '\n'
 '/* A1: крест-зоны градусника сужаются к d на сцене 3; подпись ¼→d */\n'
 '#sl-interval .p-thermo .xz { transform-box: fill-box; transition: transform .55s cubic-bezier(.4,0,.2,1); }\n'
 '#sl-interval .p-thermo .xtop { transform-origin: top; }\n'
 '#sl-interval .p-thermo .xbot { transform-origin: bottom; }\n'
 '#sl-interval .p-thermo .thermo-lbl { transition: opacity .4s ease; }\n'
 '#sl-interval .p-thermo .thermo-d { opacity: 0; }\n'
 '#sl-interval.scene-3 .p-thermo .xz { transform: scaleY(.66); }\n'
 '#sl-interval.scene-3 .p-thermo .thermo-q { opacity: 0; }\n'
 '#sl-interval.scene-3 .p-thermo .thermo-d { opacity: 1; }')
assert s.count(old_css) == 1, f"old_css count={s.count(old_css)}"
s = s.replace(old_css, new_css)

f.write_text(s)
print("OK all three E edits applied")
