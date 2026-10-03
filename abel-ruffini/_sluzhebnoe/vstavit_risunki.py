"""Обновить рисунки в LENTA/lenta.md из _sluzhebnoe/ris/*.svg (сопоставление по aria-label).
Запуск: python3 _sluzhebnoe/risunki.py && python3 _sluzhebnoe/vstavit_risunki.py"""
import re, glob, os
L = 'LENTA/lenta.md'; s = open(L).read(); n = 0
for fn in glob.glob('_sluzhebnoe/ris/*.svg'):
    new = open(fn).read().strip()
    lab = re.search(r'aria-label="([^"]+)"', new).group(1)
    pat = re.compile(r'<svg[^>]*aria-label="%s"[^>]*>.*?</svg>' % re.escape(lab), re.S)
    s, k = pat.subn(lambda m: new, s); n += k
open(L, 'w').write(s); print('заменено рисунков:', n)
