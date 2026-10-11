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
assert '{{' not in src, re.findall(r'\{\{[^}]*\}\}', src)
os.makedirs('LENTA', exist_ok=True)
open('LENTA/lenta.md', 'w', encoding='utf-8').write(src)
proza = re.sub(r'<svg.*?</svg>|<style>.*?</style>|<[^>]+>', ' ', src, flags=re.S)
proza = re.sub(r'^---.*?---', '', proza, flags=re.S)
print('рисунков:', src.count('<figure>'), '| слов прозы:', len(proza.split()), '| знаков прозы:', len(proza))
