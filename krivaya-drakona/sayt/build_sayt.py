#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сборщик сайта-лонгрида про кривую дракона.

    python3 krivaya-drakona/sayt/build_sayt.py

Источник → генератор → самодостаточный HTML, как везде в проекте.

ПОЧЕМУ СБОРЩИК СВОЙ, А НЕ `_generator/`. Правило №1 корня запрещает писать HTML
мимо генератора, но `_generator` умеет два жанра — документ (`build_doc.py`) и
слайды (`build_deck.py`), — а третьего, «лендинг», у него нет. Владелец ослабил
правило для этого захода сознательно; доработка самого генератора в заход не
входила. `_generator/` не тронут. Урок фабрике записан в файле захода.

Что делает сборщик:
  · подставляет src/site.css в <style>, src/dragon.js + src/scenes.js в <script>;
  · вшивает шрифт base64-ом, ПОДРЕЗАВ его под реально используемые символы;
  · вшивает фотографии base64-ом;
  · проверяет самодостаточность программно и падает, если из сети что-то грузится.

Самодостаточность — не пожелание, а гейт: сайт открывается при выключенной сети.
"""
import base64
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'src')
BUILD = os.path.join(ROOT, 'build')
FOTO = os.path.join(ROOT, 'foto')

# Кириллица есть только у IBM Plex Mono из локального набора: IBM Plex Sans
# локально не нашёлся, а Instrument Sans / Work Sans / Outfit кириллицу не
# покрывают (проверено чтением cmap). Поэтому mono вшивается, sans идёт
# системным стеком — из сети не грузится ничего.
FONT_DIRS = [
    os.path.expanduser('~/Library/Application Support/Claude/local-agent-mode-sessions'),
    os.path.expanduser('~/Library/Fonts'),
    '/Library/Fonts',
]
FONT_WANT = 'IBMPlexMono-Regular.ttf'


def find_font():
    for base in FONT_DIRS:
        if not os.path.isdir(base):
            continue
        for dirpath, _dirs, files in os.walk(base):
            if FONT_WANT in files:
                return os.path.join(dirpath, FONT_WANT)
    return None


def visible_text(html):
    """Видимый текст страницы: тот же замер, что применён к референсу."""
    s = re.sub(r'(?is)<script.*?</script>', '', html)
    s = re.sub(r'(?is)<style.*?</style>', '', s)
    s = re.sub(r'(?is)<head.*?</head>', '', s)
    s = re.sub(r'(?is)<!--.*?-->', '', s)
    t = re.sub(r'(?s)<[^>]+>', ' ', s)
    t = (t.replace('&nbsp;', ' ').replace('&mdash;', '—')
          .replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>'))
    return re.sub(r'\s+', ' ', t).strip()


def subset_font(path, chars):
    """Подрезать шрифт под нужные символы. Без fontTools — вшить целиком."""
    try:
        from fontTools import subset
    except ImportError:
        return open(path, 'rb').read(), False
    import io
    opts = subset.Options()
    opts.layout_features = ['*']
    opts.notdef_outline = True
    opts.recalc_bounds = True
    opts.drop_tables += ['DSIG']
    font = subset.load_font(path, opts)
    subsetter = subset.Subsetter(options=opts)
    subsetter.populate(text=''.join(sorted(chars)))
    subsetter.subset(font)
    buf = io.BytesIO()
    opts.flavor = 'woff2'
    try:
        subset.save_font(font, buf, opts)
    except Exception:
        opts.flavor = None
        buf = io.BytesIO()
        subset.save_font(font, buf, opts)
    return buf.getvalue(), opts.flavor == 'woff2'


def photo_tag(name):
    """Фото → data-URI. Нет файла — честная заглушка, а не битая ссылка."""
    for ext, mime in (('.jpg', 'image/jpeg'), ('.jpeg', 'image/jpeg'),
                      ('.png', 'image/png'), ('.webp', 'image/webp')):
        p = os.path.join(FOTO, name + ext)
        if os.path.exists(p):
            b = base64.b64encode(open(p, 'rb').read()).decode('ascii')
            return 'data:%s;base64,%s' % (mime, b), os.path.getsize(p)
    return None, 0


def main():
    html = open(os.path.join(SRC, 'index.html'), encoding='utf-8').read()
    css = open(os.path.join(SRC, 'site.css'), encoding='utf-8').read()
    js_core = open(os.path.join(SRC, 'dragon.js'), encoding='utf-8').read()
    js_scenes = open(os.path.join(SRC, 'scenes.js'), encoding='utf-8').read()

    problems = []

    # ── фотографии ──
    # Плейсхолдеров в разметке сейчас нет: свободнолицензированных снимков
    # Галливан (2002) и «Разрушителей легенд» (2007) найти не удалось, и на их
    # месте стоит типографская пара (см. комментарий в src/index.html).
    # Поддержка вшивания оставлена рабочей: положить файл в foto/ под именем
    # gallivan.jpg или mythbusters.jpg, вернуть в разметку <img src="__FOTO_…__">
    # с классами .photo/.photo__wrap — и снимок уедет в сборку base64-ом.
    for key, name in (('__FOTO_GALLIVAN__', 'gallivan'),
                      ('__FOTO_MYTHBUSTERS__', 'mythbusters')):
        if key not in html:
            continue
        uri, size = photo_tag(name)
        if uri is None:
            problems.append('в разметке есть %s, но файла foto/%s.* нет' % (key, name))
            uri = ('data:image/svg+xml;base64,' + base64.b64encode(
                ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4 3">'
                 '<rect width="4" height="3" fill="#1a1a1e"/></svg>'
                 ).encode('utf-8')).decode('ascii'))
        else:
            print('  фото %-12s %6.1f КБ' % (name, size / 1024.0))
        html = html.replace(key, uri)

    # ── шрифт: подрезать под то, что реально на странице ──
    used = set(visible_text(html))
    used |= set('0123456789 ·×→↓°…«»—–%+-/()[]:;,.!?✓')
    used |= set('абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
    used |= set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    fp = find_font()
    if fp:
        data, is_woff2 = subset_font(fp, used)
        fmt = 'woff2' if is_woff2 else 'truetype'
        b64 = base64.b64encode(data).decode('ascii')
        fonts = ("@font-face{font-family:'PlexMonoLocal';font-style:normal;"
                 "font-weight:400;font-display:block;"
                 "src:url(data:font/%s;base64,%s) format('%s');}"
                 % ('woff2' if is_woff2 else 'ttf', b64, fmt))
        print('  шрифт %-12s %6.1f КБ (%s, %d символов)'
              % ('Plex Mono', len(data) / 1024.0, fmt, len(used)))
    else:
        fonts = '/* локальный IBM Plex Mono не найден — mono идёт системным стеком */'
        problems.append('шрифт IBMPlexMono-Regular.ttf не найден — mono системный')
    css = css.replace('/*__FONTS__*/', fonts)

    # ── сборка ──
    out = html.replace('/*__CSS__*/', css)
    out = out.replace('/*__JS__*/', js_core + '\n\n' + js_scenes)

    # ── ГЕЙТ САМОДОСТАТОЧНОСТИ: ни одной внешней ссылки ──
    ext = re.findall(r'(?:src|href)="(?:https?:)?//[^"]*"', out)
    if ext:
        print('❌ внешние ссылки в сборке: %s' % ext[:5])
        return 1
    for bad in ('cdn.', 'fonts.googleapis', 'fonts.gstatic', 'jsdelivr', 'unpkg'):
        if bad in out:
            print('❌ в сборке осталось «%s»' % bad)
            return 1

    os.makedirs(BUILD, exist_ok=True)
    dst = os.path.join(BUILD, 'index.html')
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(out)

    vis = visible_text(out)

    # ── ГЕЙТ ДОЧИСТКИ: чего на странице быть НЕ должно ──
    # Мерим по ВИДИМОМУ тексту, а не по всему файлу: сборка вшивает src целиком,
    # вместе с комментариями кода, и голый grep по index.html считает слово в
    # комментарии за надзаголовок на экране. Здесь запрещено ровно то, что
    # видит читатель.
    banned = [r'сцена\s*\d', r'наведите', r'коснитесь', r'в руках ранг',
              r'углы скруглены', r'дальше они значения не меняют']
    hits = []
    for pat in banned:
        for m in re.finditer(pat, vis, re.I):
            hits.append('%s → «%s»' % (pat, vis[max(0, m.start() - 20):m.end() + 20]))
    if hits:
        print('❌ на странице осталось вырезанное:')
        for h in hits[:10]:
            print('   %s' % h)
        return 1
    print('  вырезанного на странице: 0 (проверено %d запретов)' % len(banned))

    print('  собрано: %s' % os.path.relpath(dst, os.path.dirname(ROOT)))
    print('  размер: %.1f КБ' % (len(out.encode('utf-8')) / 1024.0))
    print('  видимого текста: %d знаков (потолок — референс, 15233)' % len(vis))
    if len(vis) > 15233:
        print('❌ текста больше, чем у референса')
        return 1
    for p in problems:
        print('  ⚠ %s' % p)
    print('✅ самодостаточно: внешних ссылок 0')
    return 0


if __name__ == '__main__':
    sys.exit(main())
