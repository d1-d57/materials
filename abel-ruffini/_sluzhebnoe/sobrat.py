"""Сборка источника ленты: _sluzhebnoe/lenta-istochnik.md (ПРАВИТЬ ЕГО) → LENTA/lenta.md.
Плейсхолдеры: {{R:имя|подпись}} — рисунок _sluzhebnoe/ris/имя.svg в <figure> с подписью;
{{S:cN}} — симуляция из _sluzhebnoe/sim/cN.html (+ cN.css, если есть) + cN.js; общая библиотека
(sim.css + lib.js) вставляется один раз перед первой симуляцией.
Запуск из папки abel-ruffini: python3 _sluzhebnoe/risunki.py && python3 _sluzhebnoe/sobrat.py"""
import re, os
D = '_sluzhebnoe/'
S = D + 'sim/'
rd = lambda p: "\n".join(l for l in open(p).read().splitlines() if l.strip())
src = open(D + 'lenta-istochnik.md').read()

# 1. в тексте вне сырого HTML формулы с сырыми < > -> \lt \gt
def fixmath(t):
    return re.sub(r'\$\$.+?\$\$|\$[^$\n]+?\$',
                  lambda m: m.group(0).replace('<', r'\lt ').replace('>', r'\gt '), t, flags=re.S)
src = fixmath(src)

# 2. рисунки
def fig(m):
    name, cap = m.group(1), m.group(2)
    svg = open(D + 'ris/%s.svg' % name).read().strip()
    return '<figure>\n%s\n<figcaption>%s</figcaption>\n</figure>' % (svg, cap)
src = re.sub(r'\{\{R:([^|}]+)\|([^}]+)\}\}', fig, src)

# 3. симуляции
first = [True]
def sim(m):
    k = m.group(1)
    css = '<style>%s</style>' % rd(S + k + '.css') if os.path.exists(S + k + '.css') else ''
    blk = '<div class="sim" id="sim-%s">%s%s<script>%s</script></div>' % (k, css, rd(S + k + '.html'), rd(S + k + '.js'))
    if first[0]:
        first[0] = False
        lib = '<div class="sim-lib" hidden><style>%s</style><script>%s</script></div>' % (rd(S + 'sim.css'), rd(S + 'lib.js'))
        # первая симуляция должна стоять отдельным блоком (не внутри <details>)
        return lib + '\n\n' + blk
    return blk
src = re.sub(r'\{\{S:(c\d+)\}\}', sim, src)
assert '{{' not in src, re.findall(r'\{\{[^}]*\}\}', src)
open('LENTA/lenta.md', 'w').write(src)
print('рисунков:', src.count('<figure>'), '| симуляций:', len(re.findall(r'<div class="sim" id=', src)),
      '| слов (без svg/js):', len(re.sub(r'<svg.*?</svg>|<script>.*?</script>|<style>.*?</style>|<[^>]+>', ' ', src, flags=re.S).split()))
