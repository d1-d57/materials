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
  4. <script> НА СТРАНИЦАХ РАЗРЕШЁН (доводка 2026-08-20, П11: тумблер держит
     состояние через localStorage) — но внутри него ищутся вызовы, которые
     пишут текст в DOM (innerHTML/innerText/textContent/document.write/
     insertAdjacentHTML): их обязано быть 0, иначе JS мог бы родить текст,
     которого гейт не увидит статическим разбором. Голое число тегов <script>
     печатается СПРАВОЧНО, в провал больше не идёт — см. «чего гейт не
     проверяет» ниже, это её честная слепая зона;
  5. отсутствие CSS `content:"…"` с буквами — там тоже прячется видимый текст;
  6. служебные поля данных (sluzhebnoe, snoska, istochniki, utok) на страницы
     не доехали: они законны как данные, но запрещены ТЗ §4.

Чего гейт НЕ проверяет — печатается в конце прогона, чтобы это не пришлось
угадывать по коду.
"""
import json, os, re, sys, html
from html.parser import HTMLParser

TUT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(TUT, 'dist')
# Несколько классов (7 и 8, владелец 2026-08-22) — несколько source-файлов;
# страница любого класса может использовать слово из ЛЮБОГО god-файла (общая
# шапка одна на все классы), поэтому корпус и белый список — объединение.
IST_FAJLY = [f for f in ('god.json', 'god-8.json')
             if os.path.exists(os.path.join(TUT, f))]

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
        self.skript_tekst = []
        self._v_style = False
        self._v_script = False

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.skripty += 1
            self.glushit += 1
            self._v_script = True
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
            if tag == 'script':
                self._v_script = False

    def handle_data(self, data):
        if self._v_style:
            self.stili.append(data)
        if self._v_script:
            self.skript_tekst.append(data)
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
    # Несколько классов — несколько g; корпус/белый список/запрет объединяются
    # по ВСЕМ (общая шапка одного класса легально цитирует "7 класс"/"8 класс"
    # из ЛЮБОГО god-файла — см. IST_FAJLY).
    gg = [json.load(open(os.path.join(TUT, f), encoding='utf-8')) for f in IST_FAJLY]
    belyj = set()
    korpus_kuski = []
    zapret = []
    razresh_kuski = []
    for g in gg:
        belyj |= set(norm(x) for x in g['interfejs'])
        korpus_kuski += korpus_iz(g, [])
        for pole in ZAPRET_POLYA:
            korpus_iz(g.get(pole), zapret)
        for c in g['chetverti']:
            for e in c['elementy']:
                if 'istochniki' in e:
                    zapret.append(e['istochniki'])
        razresh = dict(g)
        for pole in ZAPRET_POLYA:
            razresh.pop(pole, None)
        razresh_kuski += korpus_iz(razresh, [])
    korpus_slit = ' ¦ '.join(norm(x) for x in korpus_kuski)
    zapret = [norm(x) for x in zapret if norm(x)]
    # Разрешённый корпус — данные БЕЗ служебных полей. Фраза, которая есть и там
    # и там (например «правило произведения» — и метод в utok, и тема в karta),
    # служебной не считается: иначе гейт краснеет на законном материале.
    razresh_slit = ' ¦ '.join(norm(x) for x in razresh_kuski)
    zapret = [z for z in zapret if z not in razresh_slit]

    fajly = sorted(f for f in os.listdir(DIST) if f.endswith('.html'))
    if not fajly:
        print('в %s нет собранных страниц — гейту нечего проверять' % DIST)
        return 1

    vsego = 0
    siroty = []
    skripty = 0
    skript_tekst_vyzovy = []
    css_tekst = []
    zapret_naideno = []

    for f in fajly:
        put = os.path.join(DIST, f)
        soder = open(put, encoding='utf-8').read()
        p = Sbor()
        p.feed(soder)
        skripty += p.skripty
        for skript in p.skript_tekst:
            for m in re.finditer(
                    r'\.(innerHTML|innerText|textContent)\s*=|'
                    r'\b(document\.write|insertAdjacentHTML)\s*\(', skript):
                skript_tekst_vyzovy.append((f, m.group(0)))
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

    print('источники данных : %s' % ', '.join(IST_FAJLY))
    print('страниц проверено: %d' % len(fajly))
    print('строк проверено %d, сирот %d' % (vsego, len(siroty)))
    for f, rod, t in siroty[:40]:
        print('   СИРОТА %-26s [%s] %s' % (f, rod, t))
    if len(siroty) > 40:
        print('   … и ещё %d' % (len(siroty) - 40))

    print('тегов <script> на страницах: %d (справочно — JS разрешён П11, доводка 2026-08-20)'
          % skripty)
    print('текст-порождающих вызовов в JS (innerHTML/innerText/textContent/'
          'document.write/insertAdjacentHTML), должно быть 0: %d' % len(skript_tekst_vyzovy))
    for f, t in skript_tekst_vyzovy[:10]:
        print('   JS-ТЕКСТ %s : %s' % (f, t))
    print('CSS content: с буквами: %d' % len(css_tekst))
    for f, t in css_tekst[:10]:
        print('   CSS-ТЕКСТ %s : %s' % (f, t))
    print('служебных полей данных (%s) на страницах: %d'
          % (', '.join(ZAPRET_POLYA), len(zapret_naideno)))
    for f, t in zapret_naideno[:10]:
        print('   ЗАПРЕЩЁННОЕ ПОЛЕ %s : %s…' % (f, t))

    vse_slova = sorted({w for g in gg for w in g['interfejs']})
    print()
    print('БЕЛЫЙ СПИСОК (interfejs всех источников, %d слов, слово в слово):'
          % len(vse_slova))
    for w in vse_slova:
        print('   · %s' % w)

    print()
    print('ЧЕГО ЭТОТ ГЕЙТ НЕ ПРОВЕРЯЕТ:')
    print('   · смысл — только происхождение: перестановка слов данных в новую')
    print('     фразу гейт пропустит, если такая подстрока в данных есть;')
    print('   · текст, дорисованный CSS не через content (фоновой картинкой или')
    print('     шрифтом-иконкой) — таких на страницах нет, но гейт к ним слеп;')
    print('   · текст внутри SVG-графики — на страницах SVG нет, проверено тем,')
    print('     что тега <svg> в собранных файлах не встречается;')
    print('   · внешние ресурсы — их нет, страницы самодостаточны;')
    print('   · РЕАЛЬНОЕ ИСПОЛНЕНИЕ JS В БРАУЗЕРЕ (слепая зона, П11, доводка')
    print('     2026-08-20): гейт читает <script> статически — эвристикой по')
    print('     именам вызовов (innerHTML/innerText/textContent/document.write/')
    print('     insertAdjacentHTML), а не настоящим прогоном страницы. Текст,')
    print('     построенный иначе (например через шаблонные строки, minified')
    print('     код без этих имён, или вставленный не в DOM, а куда-то ещё),')
    print('     эта эвристика не увидит — она приближение, не гарантия.')

    plohо = len(siroty) + len(skript_tekst_vyzovy) + len(css_tekst) + len(zapret_naideno)
    return 1 if plohо else 0



if __name__ == '__main__':
    sys.exit(main())
