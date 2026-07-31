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

# 7. Фотографии. Д6 захода переписал этот пункт: «Не нашёл за десять минут —
#    не вставляй вообще, блок 12/11 всё равно удалён». Поэтому законных
#    состояний два — ноль фотографий И удалённый блок записей, либо обе. Одна
#    из двух — брак: полупункт с зелёной галочкой и есть то молчаливое усечение,
#    от которого гейт нужен. «Парка Юрского периода» не должно быть никогда.
photos = len(re.findall(r'class="photo__wrap"', html))
no_jp = not re.search(r'юрск', html, re.I)
no_records = 'class="records"' not in html
check(7, 'фотографий: %d (законно 0 или 2) · блок 12/11 удалён: %s · '
      '«Парка Юрского периода» нет: %s'
      % (photos, 'да' if no_records else 'НЕТ', 'да' if no_jp else 'НЕТ'),
      no_jp and ((photos == 0 and no_records) or photos == 2),
      'свободнолицензированных снимков Галливан и «Разрушителей легенд» нет '
      'ни на Wikimedia Commons, ни в Openverse — см. ОТЧЁТ')

# 8-9. снимки на двух ширинах: одиннадцать кадров (восемь сцен, из них у
#      сцены 5 четыре шага листалки) плюс кадры наведения на широкой
if os.path.isdir(SNIMKI):
    shots = os.listdir(SNIMKI)
else:
    shots = []
wide = [s for s in shots if '1440x900' in s]
narrow = [s for s in shots if '390x844' in s]
check(8, 'снимки 1440×900: %d файлов' % len(wide), len(wide) >= 11)
check(9, 'снимки 390×844: %d файлов' % len(narrow), len(narrow) >= 11)

# ══════════════════ ДОЧИСТКА: пункты Д1–Д5 файла захода ══════════════════

vis = visible_text(html)

# 10. надзаголовки сцен вырезаны — у обложки остаётся ровно один
eyebrows = len(re.findall(r'class="eyebrow"', html))
check(10, 'надзаголовков .eyebrow: %d (только обложка)' % eyebrows, eyebrows == 1)

# 11. заголовки сцен — РОВНО те семь, что в таблице Д3, дословно
WANT = ['Сгибаем полоску', 'Как её нарисовать', 'Второй способ нарисовать',
        'Пересекает ли она себя?', 'Доказательство',
        'Четыре дракона покрывают решётку', 'У линии есть площадь']
got = [re.sub(r'\s+', ' ', t).strip()
       for t in re.findall(r'<h2 class="scene__title">(.*?)</h2>', html, re.S)]
check(11, 'заголовки сцен: %s' % (' · '.join(got) if got != WANT else 'все семь по Д3'),
      got == WANT)

# 12. вырезанное вырезано: подписи в холстах, блок записей, подвал, снап-скролл
left = {
    'подпись <text> в SVG': bool(re.search(r"mk\('text'", html)),
    'блок .records': 'class="records"' in html,
    'подвал .foot': 'class="foot"' in html,
    'снап-скролл': 'setupSnapScroll' in html or 'animateScrollTo' in html,
    '.scene--tall': 'scene--tall' in html,
}
check(12, 'вырезано: ' + (', '.join(k for k, v in left.items() if v) or 'всё'),
      not any(left.values()))

# 13. Д2: стрелка вниз у сцен 1–6 (у последней её нет — идти некуда),
#     листалка из четырёх точек на сцене 5, клавиши ↓/↑ и ←/→ подключены
downs = len(re.findall(r'class="godown"', html))
dots = len(re.findall(r'class="pager__dot(?: on)?"', html))
keys = all(k in html for k in ('ArrowDown', 'ArrowUp', 'ArrowRight', 'ArrowLeft'))
check(13, 'стрелок вниз %d из 6 · точек листалки %d из 4 · клавиши: %s'
      % (downs, dots, 'да' if keys else 'НЕТ'),
      downs == 6 and dots == 4 and keys)

# 14. Д1: слов-инструкций и метаразговора в ВИДИМОМ тексте нет.
#     Мерим по видимому тексту, а не по всему файлу: сборка вшивает src вместе
#     с комментариями кода, и голый grep считает слово в комментарии за
#     надзаголовок на экране.
BANNED = [r'сцена\s*\d', r'наведите', r'коснитесь', r'в руках ранг',
          r'углы скруглены', r'дальше они значения не меняют',
          r'как мы увидим ниже', r'руки кончаются']
found = [p for p in BANNED if re.search(p, vis, re.I)]
check(14, 'вырезанного в видимом тексте: %d из %d запретов'
      % (len(found), len(BANNED)), not found, ', '.join(found))

TOTAL = 14
print('\n' + ('✅ гейт пройден: %d из %d' % (TOTAL - len(bad), TOTAL) if not bad
              else '❌ провалены пункты: %s (из %d)'
              % (', '.join(map(str, bad)), TOTAL)))
sys.exit(1 if bad else 0)
