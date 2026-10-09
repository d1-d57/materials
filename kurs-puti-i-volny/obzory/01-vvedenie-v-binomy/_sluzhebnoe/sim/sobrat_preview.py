"""Сборка preview.html — шесть симуляций, вставленные так же, как это делает
abel-ruffini/_sluzhebnoe/sobrat.py: метка {{S:cN}} → <div class="sim" id="sim-cN"> + <style>cN.css</style>
+ cN.html + <script>cN.js</script>; sim.css + lib.js — один раз, перед первой симуляцией.
Стили движка — preview-dvizhok.css (копия первого <style> из abel-ruffini/LENTA/view.html).
Запуск: python3 sobrat_preview.py (из этой папки)."""
import re, os
H = os.path.dirname(os.path.abspath(__file__)) + '/'
rd = lambda p: "\n".join(l for l in open(H + p).read().splitlines() if l.strip())

SRC = r"""
<h1>Введение в биномиальные коэффициенты</h1>
<div class="podzag">черновик шести симуляций</div>
<p>Число $\binom nk$ — это число способов выбрать $k$ предметов из $n$, или, что то же самое, число слов длины $n$ из нулей и единиц, в которых ровно $k$ единиц. Слово рисуем рядом клеток: единица — закрашенная клетка, ноль — пустая.</p>
<h2>Все варианты выбора</h2>
<p>Занумеруем предметы числами от $1$ до $n$. Вариант выбора — набор номеров, например $\{1,3\}$. Его код — слово длины $n$: на местах выбранных номеров единицы, на остальных нули.</p>
{{S:c0}}
<h2>Зеркало</h2>
<p>Поменяем в слове все нули на единицы и наоборот. Слово с $k$ единицами станет словом с $n-k$ единицами.</p>
{{S:c1}}
<h2>Разъезд по первой цифре</h2>
<p>Разложим слова на две кучки по первой цифре и забудем её.</p>
{{S:c2}}
<h2>Капитан тремя способами</h2>
<p>Сколькими способами выбрать из $n$ человек команду из $k+1$ человека и в ней капитана? Посчитаем тремя способами.</p>
{{S:c3}}
<h2>Стрелки и отрезки</h2>
<p>Стрелок между $n$ точками вдвое больше, чем отрезков.</p>
{{S:c4}}
<h2>Клетки таблицы</h2>
<p>Те же пары можно разложить по клеткам таблицы: пара $\{i,j\}$ при $i&lt;j$ — клетка в строке $i$ и столбце $j$.</p>
{{S:c5}}
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
open(H + 'preview.html', 'w').write(HEAD + body + TAIL)
print('preview.html: симуляций', len(re.findall(r'<div class="sim" id=', body)))
