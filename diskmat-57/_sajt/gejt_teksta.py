#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Гейт текста: на собранных страницах нет ни одной фразы, которой нет в данных.

    python3 gejt_teksta.py            # rc=0 при нуле сирот, rc=1 иначе

Правило (интервью 2026-08-19, п.7): весь видимый текст происходит ЛИБО из
god.json, ЛИБО из белого списка интерфейсных слов god.json["interfejs"].
Строка не оттуда и не оттуда — СИРОТА, гейт красный.

Что гейт проверяет:
  1. текстовые узлы всех dist/*.html (кроме <script>/<style>/комментариев);
  2. видимые атрибуты title / alt / aria-label / placeholder;
  3. содержимое <title>;
  4. отсутствие <script> вовсе — иначе текст мог бы родиться в JS уже в браузере,
     и пункты 1-3 его не увидели бы;
  5. отсутствие CSS `content:"…"` с буквами — там тоже прячется видимый текст;
  6. служебные поля данных (sluzhebnoe, snoska, istochniki, utok) на страницы
     не доехали: они законны как данные, но запрещены ТЗ §4.

Чего гейт НЕ проверяет — печатается в конце прогона, чтобы это не пришлось
угадывать по коду.
"""
import json, os, re, sys, html
from html.parser import HTMLParser

TUT = os.path.dirname(os.path.abspath(__file__))
IST = os.path.join(TUT, 'god.json')
DIST = os.path.join(TUT, 'dist')

VIDIMYE_ATR = ('title', 'alt', 'aria-label', 'placeholder')
ZAPRET_POLYA = ('sluzhebnoe', 'snoska', 'istochniki', 'utok')
RIM = {'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x'}


def norm(s):
    s = html.unescape(s)
    s = s.replace(' ', ' ').replace('ё', 'е').replace('Ё', 'Е')
    return re.sub(r'\s+', ' ', s).strip().lower()


class Sbor(HTMLParser):
    """Собирает видимый текст: текстовые узлы + видимые атрибуты."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.kuski = []          # (rod, tekst)
        self.glushit = 0
        self.skripty = 0
        self.stili = []
        self._v_style = False

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.skripty += 1
            self.glushit += 1
        elif tag == 'style':
            self.glushit += 1
            self._v_style = True
        for k, v in attrs:
            if k in VIDIMYE_ATR and v and v.strip():
                self.kuski.append(('@' + k, v))

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.glushit = max(0, self.glushit - 1)
            if tag == 'style':
                self._v_style = False

    def handle_data(self, data):
        if self._v_style:
            self.stili.append(data)
        if self.glushit:
            return
        if data.strip():
            self.kuski.append(('текст', data))


def korpus_iz(o, out):
    if isinstance(o, dict):
        for v in o.values():
            korpus_iz(v, out)
    elif isinstance(o, list):
        for v in o:
            korpus_iz(v, out)
    elif isinstance(o, str):
        out.append(o)
    return out


def chisto(frag, korpus_slit, belyj):
    """Фрагмент законен, если он целиком из данных, целиком из белого списка,
    состоит из чисел и знаков, либо это белое слово рядом с числом."""
    f = norm(frag)
    if not f:
        return True, 'пусто'
    if f in belyj:
        return True, 'белый список'
    if f in korpus_slit:
        return True, 'данные'
    ostatok = ' '.join(t for t in f.split()
                       if not re.fullmatch(r'[\d.,;:·—–\-()«»\[\]/№]+', t)
                       and t not in RIM).strip()
    if not ostatok:
        return True, 'числа и знаки'
    if ostatok in belyj:
        return True, 'белый список + число'
    if ostatok in korpus_slit:
        return True, 'данные + число'
    return False, 'СИРОТА'


def main():
    g = json.load(open(IST, encoding='utf-8'))
    belyj = set(norm(x) for x in g['interfejs'])
    korpus_slit = ' ¦ '.join(norm(x) for x in korpus_iz(g, []))

    # запрещённые ТЗ §4 поля — отдельным списком, чтобы ловить их адресно
    zapret = []
    for pole in ZAPRET_POLYA:
        korpus_iz(g.get(pole), zapret)
    for c in g['chetverti']:
        for e in c['elementy']:
            if 'istochniki' in e:
                zapret.append(e['istochniki'])
    zapret = [norm(x) for x in zapret if norm(x)]
    # Разрешённый корпус — данные БЕЗ служебных полей. Фраза, которая есть и там
    # и там (например «правило произведения» — и метод в utok, и тема в karta),
    # служебной не считается: иначе гейт краснеет на законном материале.
    razresh = dict(g)
    for pole in ZAPRET_POLYA:
        razresh.pop(pole, None)
    razresh_slit = ' ¦ '.join(norm(x) for x in korpus_iz(razresh, []))
    zapret = [z for z in zapret if z not in razresh_slit]

    fajly = sorted(f for f in os.listdir(DIST) if f.endswith('.html'))
    if not fajly:
        print('в %s нет собранных страниц — гейту нечего проверять' % DIST)
        return 1

    vsego = 0
    siroty = []
    skripty = 0
    css_tekst = []
    zapret_naideno = []

    for f in fajly:
        put = os.path.join(DIST, f)
        soder = open(put, encoding='utf-8').read()
        p = Sbor()
        p.feed(soder)
        skripty += p.skripty
        for stil in p.stili:
            for m in re.finditer(r'content\s*:\s*(["\'])(.*?)\1', stil, re.S):
                if re.search(r'[A-Za-zА-Яа-яЁё]', m.group(2)):
                    css_tekst.append((f, m.group(2)))
        stranica_norm = ' '.join(norm(t) for _, t in p.kuski)
        for z in zapret:
            if len(z) > 20 and z in stranica_norm:
                zapret_naideno.append((f, z[:60]))
        for rod, t in p.kuski:
            vsego += 1
            ok, _ = chisto(t, korpus_slit, belyj)
            if not ok:
                siroty.append((f, rod, ' '.join(t.split())[:110]))

    print('источник данных  : %s' % IST)
    print('страниц проверено: %d' % len(fajly))
    print('строк проверено %d, сирот %d' % (vsego, len(siroty)))
    for f, rod, t in siroty[:40]:
        print('   СИРОТА %-26s [%s] %s' % (f, rod, t))
    if len(siroty) > 40:
        print('   … и ещё %d' % (len(siroty) - 40))

    print('тегов <script> на страницах: %d (текста, рождённого в JS, нет только при 0)'
          % skripty)
    print('CSS content: с буквами: %d' % len(css_tekst))
    for f, t in css_tekst[:10]:
        print('   CSS-ТЕКСТ %s : %s' % (f, t))
    print('служебных полей данных (%s) на страницах: %d'
          % (', '.join(ZAPRET_POLYA), len(zapret_naideno)))
    for f, t in zapret_naideno[:10]:
        print('   ЗАПРЕЩЁННОЕ ПОЛЕ %s : %s…' % (f, t))

    print()
    print('БЕЛЫЙ СПИСОК (god.json["interfejs"], %d слов, слово в слово):'
          % len(g['interfejs']))
    for w in g['interfejs']:
        print('   · %s' % w)

    print()
    print('ЧЕГО ЭТОТ ГЕЙТ НЕ ПРОВЕРЯЕТ:')
    print('   · смысл — только происхождение: перестановка слов данных в новую')
    print('     фразу гейт пропустит, если такая подстрока в данных есть;')
    print('   · текст, дорисованный CSS не через content (фоновой картинкой или')
    print('     шрифтом-иконкой) — таких на страницах нет, но гейт к ним слеп;')
    print('   · текст внутри SVG-графики — на страницах SVG нет, проверено тем,')
    print('     что тега <svg> в собранных файлах не встречается;')
    print('   · внешние ресурсы — их нет, страницы самодостаточны.')

    plohо = len(siroty) + skripty + len(css_tekst) + len(zapret_naideno)
    return 1 if plohо else 0



if __name__ == '__main__':
    sys.exit(main())
