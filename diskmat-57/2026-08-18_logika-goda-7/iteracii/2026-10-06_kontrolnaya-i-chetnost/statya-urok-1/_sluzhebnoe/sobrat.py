# -*- coding: utf-8 -*-
"""Сборка источника: _sluzhebnoe/lenta-istochnik.md (ПРАВИТЬ ЕГО) → LENTA/lenta.md.
{{R:имя|подпись|почему статично}} — рисунок из ris.py в <figure> с подписью; причина статичности —
комментарием <!-- static: … --> внутри <figure> (ZHANR-statya С11). Схема — как у ленты про биномы.
Запуск из папки статьи: python3 _sluzhebnoe/sobrat.py"""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from ris import RIS

D = '_sluzhebnoe/'
src = open(D + 'lenta-istochnik.md', encoding='utf-8').read()
src = re.sub(r'\$\$.+?\$\$|\$[^$\n]+?\$', lambda m: m.group(0).replace('<', r'\lt ').replace('>', r'\gt '), src, flags=re.S)

def fig(m):
    name, cap, why = m.group(1), m.group(2), m.group(3)
    return '<figure>\n<!-- static: %s -->\n%s\n<figcaption>%s</figcaption>\n</figure>' % (why, RIS[name](), cap)

src = re.sub(r'\{\{R:([^|}]+)\|([^|}]+)\|([^}]+)\}\}', fig, src)
# {{S:cN}} — симуляция из _sluzhebnoe/sim/cN.html (+ cN.css) + cN.js; общая библиотека (sim.css + lib.js) — один раз
# перед первой (схема ленты про биномы, kurs-puti-i-volny/obzory/01-vvedenie-v-binomy/_sluzhebnoe/sobrat.py)
S = D + 'sim/'
rd = lambda p: "\n".join(l for l in open(p, encoding='utf-8').read().splitlines() if l.strip())
first = [True]
def sim(m):
    k = m.group(1)
    css = '<style>%s</style>' % rd(S + k + '.css') if os.path.exists(S + k + '.css') else ''
    blk = '<div class="sim" id="sim-%s">%s%s<script>%s</script></div>' % (k, css, rd(S + k + '.html'), rd(S + k + '.js'))
    if first[0]:
        first[0] = False
        return '<div class="sim-lib" hidden><style>%s</style><script>%s</script></div>' % (rd(S + 'sim.css'), rd(S + 'lib.js')) + '\n\n' + blk
    return blk
src = re.sub(r'\{\{S:(c\d+)\}\}', sim, src)
assert '{{' not in src, re.findall(r'\{\{[^}]*\}\}', src)
os.makedirs('LENTA', exist_ok=True)
open('LENTA/lenta.md', 'w', encoding='utf-8').write(src)
proza = re.sub(r'<svg.*?</svg>|<script>.*?</script>|<style>.*?</style>|<[^>]+>', ' ', src, flags=re.S)
proza = re.sub(r'^---.*?---', '', proza, flags=re.S)
print('рисунков:', src.count('<figure>'), '| симуляций:', len(re.findall(r'<div class="sim" id=', src)), '| слов прозы:', len(proza.split()), '| знаков прозы:', len(proza))
