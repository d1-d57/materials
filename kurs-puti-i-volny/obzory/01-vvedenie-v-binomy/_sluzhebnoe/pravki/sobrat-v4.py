"""Сборка источника ленты: _sluzhebnoe/lenta-istochnik.md (ПРАВИТЬ ЕГО) → LENTA/lenta.md.
{{S:cN}} — симуляция из _sluzhebnoe/sim/cN.html (+ cN.css) + cN.js; общая библиотека (sim.css + lib.js)
вставляется один раз перед первой симуляцией. Копия схемы abel-ruffini/_sluzhebnoe/sobrat.py (СИ2).
Запуск из папки обзора: python3 _sluzhebnoe/sobrat.py"""
import re, os
D = '_sluzhebnoe/'
S = D + 'sim/'
rd = lambda p: "\n".join(l for l in open(p).read().splitlines() if l.strip())
src = open(D + 'lenta-istochnik.md').read()
src = re.sub(r'\$\$.+?\$\$|\$[^$\n]+?\$',
             lambda m: m.group(0).replace('<', r'\lt ').replace('>', r'\gt '), src, flags=re.S)
first = [True]
def sim(m):
    k = m.group(1)
    css = '<style>%s</style>' % rd(S + k + '.css') if os.path.exists(S + k + '.css') else ''
    blk = '<div class="sim" id="sim-%s">%s%s<script>%s</script></div>' % (k, css, rd(S + k + '.html'), rd(S + k + '.js'))
    if first[0]:
        first[0] = False
        lib = '<div class="sim-lib" hidden><style>%s</style><script>%s</script></div>' % (rd(S + 'sim.css'), rd(S + 'lib.js'))
        return lib + '\n\n' + blk
    return blk
src = re.sub(r'\{\{S:(c\d+)\}\}', sim, src)
assert '{{' not in src, re.findall(r'\{\{[^}]*\}\}', src)
open('LENTA/lenta.md', 'w').write(src)
proza = re.sub(r'<svg.*?</svg>|<script>.*?</script>|<style>.*?</style>|<div class="sim.*?</div>\n|<[^>]+>', ' ', src, flags=re.S)
proza = re.sub(r'^---.*?---', '', proza, flags=re.S)
print('симуляций:', len(re.findall(r'<div class="sim" id=', src)), '| слов прозы:', len(proza.split()), '| знаков прозы:', len(proza))
