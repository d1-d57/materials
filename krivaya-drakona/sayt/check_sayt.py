#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ГЕЙТ КРИТЕРИЕВ ГОТОВНОСТИ сайта. Запускать из корня репо:

    python3 krivaya-drakona/sayt/check_sayt.py

Проверяет девять пунктов §2.5 файла захода — те, что проверяются машиной.
Каждый может ПРОВАЛИТЬСЯ, и тогда exit 1 с указанием, что именно.

Пункты 8 и 9 (сцена снята и просмотрена ГЛАЗАМИ) машиной не проверяются по
существу: гейт проверяет только НАЛИЧИЕ снимков на двух ширинах — про то, что
их кто-то посмотрел, честно отчитывается исполнитель в отчёте, файл захода.
Гейт, который печатает «просмотрено», ничего не проверив, хуже отсутствующего.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(ROOT, 'build', 'index.html')
SNIMKI = os.path.join(ROOT, 'build', '_snimki')
SRC = os.path.join(ROOT, 'src')
REF = os.path.join(ROOT, '_referens', 'matema-fest.html')

bad = []


def check(n, name, ok, detail=''):
    print(('  %s %d. %s' % ('✅' if ok else '❌', n, name))
          + ('' if ok or not detail else ' — ' + detail))
    if not ok:
        bad.append(n)


def visible_text(html):
    s = re.sub(r'(?is)<script.*?</script>', '', html)
    s = re.sub(r'(?is)<style.*?</style>', '', s)
    s = re.sub(r'(?is)<head.*?</head>', '', s)
    s = re.sub(r'(?is)<!--.*?-->', '', s)
    t = re.sub(r'(?s)<[^>]+>', ' ', s)
    t = (t.replace('&nbsp;', ' ').replace('&mdash;', '—')
          .replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>'))
    return re.sub(r'\s+', ' ', t).strip()


print('ГЕЙТ КРИТЕРИЕВ ГОТОВНОСТИ — krivaya-drakona/sayt/')

# 1. файл существует; консоль и сеть проверяются shoot.py, здесь — наличие
ok1 = os.path.exists(BUILD)
check(1, 'build/index.html существует', ok1,
      'нет файла — сначала build_sayt.py')
if not ok1:
    sys.exit(1)
html = open(BUILD, encoding='utf-8').read()

# 2. САМОДОСТАТОЧНОСТЬ: ни одной ссылки в сеть
ext = re.findall(r'(?:src|href)="(?:https?:)?//[^"]*"', html)
check(2, 'внешних ссылок ноль (grep src|href="//…")', not ext,
      'найдено %d: %s' % (len(ext), ext[:3]))

# 3. восемь сцен, у каждой заголовок, на каждой что-то живое
scenes = re.findall(r'data-scene="([a-z]+)"', html)
titles = len(re.findall(r'class="(?:scene__title|cover__title)"', html))
alive = all(s in html for s in ('IntersectionObserver', 'requestAnimationFrame'))
hooks = len(re.findall(r'data-in=|data-seg=|d-hit|data-act=', html))
check(3, 'восемь сцен (%d), заголовков %d, крючков интерактива %d'
      % (len(scenes), titles, hooks),
      len(scenes) == 8 and titles == 8 and alive and hooks >= 8)

# 4. сцена 5в: все четыре случая ДОСТИЖИМЫ — считаем по самой геометрии
core = open(os.path.join(SRC, 'dragon.js'), encoding='utf-8').read()
try:
    node_src = core + '''
const P = rank(6), seen = new Set();
for (let i = 0; i + 1 < P.length; i++) {
  const r = corner(P[i], P[i+1]);
  seen.add((r.horiz ? 'h' : 'v') + (r.blue ? '1' : '0'));
}
console.log([...seen].sort().join(','));
'''
    out = subprocess.run(['node', '-e', node_src], capture_output=True,
                         text=True, timeout=60).stdout.strip()
except Exception as e:                                    # noqa: BLE001
    out = 'ошибка: %s' % e
check(4, 'сцена 5в: четыре случая на ранге 6 (%s)' % out,
      out == 'h0,h1,v0,v1')

# 5. геометрия дракона определена РОВНО ОДИН РАЗ
#    ⚠ Критерий захода написан как `grep -c "function poly"` = 1, но эта
#    подстрока ловит и `function polyAngles`, то есть на верной работе даёт 2.
#    Меряем то, что критерий имел в виду: определений самой ломаной.
defs_src = sum(len(re.findall(r'^function poly\(', open(os.path.join(SRC, f),
               encoding='utf-8').read(), re.M))
               for f in os.listdir(SRC) if f.endswith('.js'))
defs_build = len(re.findall(r'^function poly\(', html, re.M))
check(5, 'определение ломаной одно: src %d, build %d' % (defs_src, defs_build),
      defs_src == 1 and defs_build == 1)

# 6. видимого текста не больше, чем у референса
vis = len(visible_text(html))
ref = len(visible_text(open(REF, encoding='utf-8').read())) if os.path.exists(REF) else 0
check(6, 'текста %d знаков против %d у референса' % (vis, ref),
      ref > 0 and vis <= ref)

# 7. Пункт составной: ДВЕ фотографии вшиты И «Парка Юрского периода» нет.
#    Гейт обязан краснеть, пока выполнена только половина: зелёная галочка на
#    половине пункта — то самое молчаливое усечение, от которого гейт и нужен.
photos = len(re.findall(r'class="photo__wrap"', html))
no_jp = not re.search(r'юрск', html, re.I)
check(7, 'фотографий на сцене 1: %d из 2 · «Парка Юрского периода» нет: %s'
      % (photos, 'да' if no_jp else 'НЕТ'),
      photos == 2 and no_jp,
      'свободнолицензированных снимков Галливан и «Разрушителей легенд» '
      'не найдено; на их месте типографская пара .records — см. ОТЧЁТ')

# 8-9. снимки на двух ширинах
if os.path.isdir(SNIMKI):
    shots = os.listdir(SNIMKI)
else:
    shots = []
wide = [s for s in shots if '1440x900' in s]
narrow = [s for s in shots if '390x844' in s]
check(8, 'снимки 1440×900: %d файлов' % len(wide), len(wide) >= 12)
check(9, 'снимки 390×844: %d файлов' % len(narrow), len(narrow) >= 12)

print('\n' + ('✅ гейт пройден: %d из %d' % (9 - len(bad), 9) if not bad
              else '❌ провалены пункты: %s' % ', '.join(map(str, bad))))
sys.exit(1 if bad else 0)
