#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Рендер собранных страниц в PNG — глазная проверка (шаг 6 захода)."""
import os, sys
from playwright.sync_api import sync_playwright
TUT = os.path.dirname(os.path.abspath(__file__))
CH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = os.path.join(TUT, '_render')
ZADANIE = [
    ('god-1440.png',     'index.html',                 1440, 900,  None),
    ('god-kruzhok.png',  'index.html',                 1440, 900,  'label[for=t-kruzhok]'),
    ('god-390.png',      'index.html',                  390, 844,  None),
    ('blok-1440.png',    'blok-dvojnoj-schet.html',    1440, 1180, None),
    ('blok-390.png',     'blok-dvojnoj-schet.html',     390, 844,  None),
    ('nedelya-1440.png', 'nedelya-13.html',            1440, 620,  None),
]
def main():
    if not os.path.isdir(OUT): os.makedirs(OUT)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CH)
        for imya, fajl, w, h, klik in ZADANIE:
            pg = b.new_page(viewport={'width': w, 'height': h})
            pg.goto('file://' + os.path.join(TUT, 'dist', fajl))
            if klik: pg.click(klik)
            per = pg.evaluate('document.documentElement.scrollWidth > document.documentElement.clientWidth')
            vys = pg.evaluate('document.documentElement.scrollHeight')
            pg.screenshot(path=os.path.join(OUT, imya))
            print('%-17s %4dx%-4d высота документа %4d  переполнение по ширине: %s'
                  % (imya, w, h, vys, 'ДА' if per else 'нет'))
            pg.close()
        b.close()
    return 0
if __name__ == '__main__':
    sys.exit(main())
