"""Сборка preview-c7.html — одна симуляция c7 (по образцу sobrat_preview.py), вставленная так же, как это делает
abel-ruffini/_sluzhebnoe/sobrat.py: метка {{S:cN}} → <div class="sim" id="sim-cN"> + <style>cN.css</style>
+ cN.html + <script>cN.js</script>; sim.css + lib.js — один раз, перед первой симуляцией.
Стили движка — preview-dvizhok.css (копия первого <style> из abel-ruffini/LENTA/view.html).
Запуск: python3 sobrat_c7.py (из этой папки)."""
import re, os
H = os.path.dirname(os.path.abspath(__file__)) + '/'
rd = lambda p: "\n".join(l for l in open(H + p).read().splitlines() if l.strip())

SRC = r"""
<h1>Треугольник Паскаля: шаги с множителями</h1>
<div class="podzag">черновик симуляции c7</div>
<p>Мы доказали, что $\binom n{k+1}=\frac{n-k}{k+1}\binom nk$ и $\binom nk=\frac nk\binom{n-1}{k-1}$. Значит, из единицы на краю треугольника можно дойти до любой клетки, умножая на простые дроби.</p>
{{S:c7}}
<p>Конец черновика.</p>
"""

first = [True]
def sim(m):
    k = m.group(1)
    css = '<style>%s</style>' % rd(k + '.css') if os.path.exists(H + k + '.css') else ''
    blk = '<div class="sim" id="sim-%s">%s%s<script>%s</script></div>' % (k, css, rd(k + '.html'), rd(k + '.js'))
    if first[0]:
        first[0] = False
        lib = '<div class="sim-lib" hidden><style>%s</style><script>%s</script></div>' % (rd('sim.css'), rd('lib.js'))
        return lib + '\n\n' + blk
    return blk
body = re.sub(r'\{\{S:(c\d+)\}\}', sim, SRC)
assert '{{' not in body

HEAD = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Биномиальные коэффициенты — симуляции</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css" crossorigin="anonymous">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" crossorigin="anonymous"></script>
<script>
  window.addEventListener("DOMContentLoaded", function () {
    if (window.renderMathInElement) renderMathInElement(document.body, {
      delimiters: [{left: "$$", right: "$$", display: true}, {left: "$", right: "$", display: false}],
      throwOnError: false
    });
  });
</script>
<style>
%s
</style>
<script>
(function(){
  var K="doc-theme";
  try{ var v=localStorage.getItem(K); if(v) document.documentElement.setAttribute("data-theme",v); }catch(e){}
  window.addEventListener("DOMContentLoaded",function(){
    var b=document.querySelector(".theme-tgl"); if(!b) return;
    b.addEventListener("click",function(){
      var cur=document.documentElement.getAttribute("data-theme");
      if(!cur) cur = matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
      var next = cur==="dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme",next);
      try{ localStorage.setItem(K,next); }catch(e){}
    });
  });
})();
</script>
</head>
<body data-zhanr="statya">
<div class="doc-btns"><button class="theme-tgl" type="button">тема</button></div>
<div class="wrap">
<main><article class="stream">
""" % open(H + 'preview-dvizhok.css').read()
TAIL = "\n</article></main>\n</div>\n</body>\n</html>\n"
# как и в ленте: блоки разделены пустыми строками, внутри блока пустых строк нет
open(H + 'preview-c7.html', 'w').write(HEAD + body + TAIL)
print('preview-c7.html: симуляций', len(re.findall(r'<div class="sim" id=', body)))
