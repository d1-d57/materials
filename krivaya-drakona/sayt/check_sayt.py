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

# 3. Ф6: обложка и ШЕСТЬ глав, у каждой заголовок, на каждой что-то живое.
#    Было восемь секций: две главы про способы рисования слиты в одну (Ф1).
scenes = re.findall(r'data-scene="([a-z]+)"', html)
titles = len(re.findall(r'class="(?:scene__title|cover__title)"', html))
alive = all(s in html for s in ('IntersectionObserver', 'requestAnimationFrame'))
hooks = len(re.findall(r'data-in=|data-seg=|d-hit|data-act=', html))
check(3, 'обложка и шесть глав: секций %d, заголовков %d, крючков интерактива %d'
      % (len(scenes), titles, hooks),
      len(scenes) == 7 and titles == 7 and alive and hooks >= 8)

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

# 8-9. снимки на двух ширинах: одиннадцать кадров (семь секций, из них у
#      главы «как нарисовать» две карточки и у доказательства четыре шага)
#      плюс кадры наведения и зума на широкой
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

# 10. Ф6: надзаголовков нет вообще — «Одна полоска бумаги» с обложки убран
eyebrows = len(re.findall(r'class="eyebrow"', html))
check(10, 'надзаголовков .eyebrow: %d (по Ф6 должно быть 0)' % eyebrows, eyebrows == 0)

# 11. заголовки глав — РОВНО те шесть, что в таблице Ф6, дословно
WANT = ['Сгибаем полоску', 'Как её нарисовать', 'Пересекает ли она себя?',
        'Почему нет самопересечений', 'Четыре дракона', 'Фрактальная размерность']
got = [re.sub(r'\s+', ' ', t).strip()
       for t in re.findall(r'<h2 class="scene__title">(.*?)</h2>', html, re.S)]
check(11, 'заголовки глав: %s' % (' · '.join(got) if got != WANT else 'все шесть по Ф6'),
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

# 13. стрелка вниз у глав 1–5 (у последней её нет — идти некуда); листалок
#     ДВЕ: две карточки способов рисования и ТРИ шага доказательства.
#     ⚠ ЧИСЛО ТОЧЕК СНИЗИЛОСЬ С ШЕСТИ ДО ПЯТИ, и это не ослабление гейта.
#     Правка владельца слила шаги «вершины двух сортов» и «строки» в один: на
#     одной картинке уголок покрашен по стороне поворота, и цвет совпадает с
#     цветом его строки. Шагов стало три, точек 2 + 3.
downs = len(re.findall(r'class="godown"', html))
dots = len(re.findall(r'class="pager__dot(?: on)?"', html))
keys = all(k in html for k in ('ArrowDown', 'ArrowUp', 'ArrowRight', 'ArrowLeft'))
check(13, 'стрелок вниз %d из 5 · точек листалок %d из 5 (2 + 3) · клавиши: %s'
      % (downs, dots, 'да' if keys else 'НЕТ'),
      downs == 5 and dots == 5 and keys)

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

# ══════════════════ ПРОГОН 4: пункты Ф2–Ф5 ══════════════════

# 15. Ф5: строк-показаний нет ни одной — ни в разметке, ни в коде, который их
#     заполнял. Отсчёты «ранг 6 · звеньев 64», «пройдено N из 4», «площадь 2048
#     клеток» удалены целиком, а не спрятаны стилем.
readouts = len(re.findall(r'class="readout"|data-out=', html))
check(15, 'строк-показаний .readout/data-out: %d (по Ф5 должно быть 0)' % readouts,
      readouts == 0)

# 16. Ф2: на сцене «Пересекает ли она себя?» текста, кроме заголовка, нет.
#     Мерим по разметке секции: абзацев и колонки текста быть не должно.
m = re.search(r'<section[^>]*id="s3".*?</section>', html, re.S)
sec3 = m.group(0) if m else ''
paras = len(re.findall(r'<p[\s>]', sec3))
cols = len(re.findall(r'class="col"', sec3))
check(16, 'сцена «Пересекает ли она себя?»: абзацев %d, колонок текста %d'
      % (paras, cols), bool(sec3) and paras == 0 and cols == 0)

# 17. Ф2: механика референса на месте — прогрессивные батчи, отмена устаревших
#     кадров и лог-интерполяция зума. Именно она снимает зависание, поэтому её
#     отсутствие обязано краснеть.
mech = {
    'батчи по rAF': 'requestAnimationFrame' in html,
    'отмена устаревших кадров (renderToken)': 'renderToken' in html or 'TK.v' in html,
    'лог-интерполяция зума': 'Math.log(fromZ)' in html,
    'обход заливки порциями (deepWalk)': 'deepWalk' in html,
    'старый несдерживаемый drawDeep убран': 'function drawDeep' not in html,
}
check(17, 'механика зума: ' + (', '.join(k for k, v in mech.items() if not v)
                              or 'вся на месте'),
      all(mech.values()))

# 18. Ф3/Ф4: слоты фиксированы и управление стоит в правом нижнем углу —
#     проверяется по наличию самой конструкции; сами координаты мерены
#     прогоном в браузере (числа — в ОТЧЁТЕ, разброс 0.00 px).
layout = {
    'слот тела фиксированной высоты': '--fig-h' in html,
    'полоса управления .tools': 'class="tools"' in html,
    'правая колонка .fig-wrap': 'class="fig-wrap"' in html,
    'управления в левой колонке нет': not re.search(
        r'class="col"[^>]*>(?:(?!</div>).)*?(?:data-in=|data-seg=)', html, re.S),
}
check(18, 'раскладка: ' + (', '.join(k for k, v in layout.items() if not v)
                           or 'слоты и полоса управления на месте'),
      all(layout.values()))

# ══════════════════ ПРОГОН 5: правки владельца по живому сайту ══════════════════

# 19. ВРЕЗКА «ОТКУДА БЕРЁТСЯ ПРАВИЛО СТРОК» РИСУЕТ УТВЕРЖДЕНИЕ, А НЕ КАРТИНКУ.
#     Врезка говорит три вещи, и каждая обязана быть ВЫЧИСЛИМОЙ, иначе схема
#     красивая, а факт выдуманный:
#       а) у уголка первое звено всегда горизонтально — значит уголок на
#          диагонали определён однозначно;
#       б) сторона поворота = знак произведения приращений диагонали, то есть
#          свойство одной диагонали, а не «так вышло на рисунке»;
#       в) соседние уголки поворачивают в РАЗНЫЕ стороны — отсюда чередование
#          по строкам, ради которого врезка и нарисована.
#     Плюс само правило строк: сторона поворота = цвет строки излома.
try:
    node_src = core + '''
const out = [];
for (const N of [5, 6, 7]) {
  const P = rank(N), C = corners(P);
  let rows = 0, sign = 0, alt = 0, horiz = 0, prev = null;
  C.forEach(([a, b, c]) => {
    const L = turnsLeft(a, b, c);
    if (L !== rowBlue(b[1])) rows++;
    if (L !== ((c[0] - a[0]) * (c[1] - a[1]) > 0)) sign++;
    if (prev !== null && prev === L) alt++;
    if (a[1] !== b[1]) horiz++;
    prev = L;
  });
  out.push(N + ':' + rows + sign + alt + horiz);
}
console.log(out.join(' '));
'''
    out19 = subprocess.run(['node', '-e', node_src], capture_output=True,
                           text=True, timeout=60).stdout.strip()
except Exception as e:                                    # noqa: BLE001
    out19 = 'ошибка: %s' % e
check(19, 'врезка правила строк: нарушений строк/знака/чередования/горизонтали '
      'по рангам 5-7 — %s' % out19,
      out19 == '5:0000 6:0000 7:0000')

# 20. ПРЕДЕЛЬНОЕ ЗАПОЛНЕНИЕ ЧЕТЫРЁХ ДРАКОНОВ: «ни повтора, ни дырки» — счётом.
#     Сцена рисует клетки-ромбы всех четырёх драконов и утверждает, что в пределе
#     дырок не остаётся. Считаем ровно это: клеток 4·2ⁿ, разных ключей столько
#     же (наложений нет), и ни одной пустой клетки, у которой заняты все четыре
#     соседа по стороне (дырок нет). Заявить это подписью было бы браком.
try:
    node_src = core + '''
const out = [];
for (const n of [4, 6, 8, 10]) {
  const C = dragCells(n), S = new Set(); let dup = 0;
  for (let r = 0; r < 4; r++) {
    let K = C.map(k => k.slice());
    for (let i = 0; i < r; i++) K = K.map(([p, q]) => [-q, p]);
    for (const k of K) { const key = k[0] + ',' + k[1];
      if (S.has(key)) dup++; else S.add(key); }
  }
  const xs = [...S].map(s => s.split(',').map(Number));
  const x0 = Math.min(...xs.map(a => a[0])), x1 = Math.max(...xs.map(a => a[0]));
  const y0 = Math.min(...xs.map(a => a[1])), y1 = Math.max(...xs.map(a => a[1]));
  let holes = 0;
  for (let p = x0; p <= x1; p++) for (let q = y0; q <= y1; q++) {
    if (((p + q) % 2 + 2) % 2 !== 1) continue;
    if (S.has(p + ',' + q)) continue;
    let nb = 0; for (const [a, b] of NB) if (S.has((p + a) + ',' + (q + b))) nb++;
    if (nb === 4) holes++;
  }
  out.push(n + ':' + (S.size === 4 * Math.pow(2, n) ? 'ok' : S.size)
           + '/' + dup + '/' + holes);
}
console.log(out.join(' '));
'''
    out20 = subprocess.run(['node', '-e', node_src], capture_output=True,
                           text=True, timeout=120).stdout.strip()
except Exception as e:                                    # noqa: BLE001
    out20 = 'ошибка: %s' % e
check(20, 'заполнение: клеток/наложений/дырок по рангам 4-10 — %s' % out20,
      out20 == '4:ok/0/0 6:ok/0/0 8:ok/0/0 10:ok/0/0')

# 21. ПРАВКИ ПРОГОНА 5 СТОЯТ В РАЗМЕТКЕ, А НЕ «СДЕЛАНЫ В КОДЕ».
#     Каждый пункт проверяется тем, что обязан покраснеть при откате:
#       П1 — слитый шаг: заголовка «Строки решают…» больше нет, шагов три;
#       П1 — стрелки хода крупные: у arrowOn появился размер, и он больше 7;
#       П2 — второй способ подписан операциями, а не рангами;
#       П3 — переключатель заполнения и класс заливки;
#       П4 — формулировка владельца про «прошли по ребру дважды»;
#       П5 — шахматная раскраска всей решётки (latticeNodes);
#       П6 — врезка (insetRule);
#       П7 — «по одному звену восстанавливается его уголок целиком».
p5 = {
    # ⚠ считаем ТОЛЬКО разметку: `data-step="` встречается ещё и в селекторах
    # вшитого кода (`[data-step="v"] svg`), и голый счёт даёт вдвое больше
    'П1 шаги слиты': ('Строки решают' not in html
                      and len(re.findall(r'data-step="[a-z]+">', html)) == 3),
    'П1 стрелки крупные': bool(re.search(r"arrowOn\([^)]*,\s*(1[0-9]|2[0-9])\)", html)),
    'П2 второй способ — операции': 'через одну</button>' in html,
    'П3 предельное заполнение': ('data-seg="fill"' in html
                                 and '.d-fill-a2' in html),
    'П4 формулировка про два прохода': 'прошли по ребру дважды' in html,
    'П5 шахматная на всей решётке': 'function latticeNodes' in html,
    'П6 врезка правила строк': 'function insetRule' in html,
    'П7 ключевой факт': 'восстанавливается его' in html,
}
check(21, 'правки прогона 5: ' + (', '.join('НЕТ ' + k for k, v in p5.items()
                                            if not v) or 'все на месте'),
      all(p5.values()))

TOTAL = 21
print('\n' + ('✅ гейт пройден: %d из %d' % (TOTAL - len(bad), TOTAL) if not bad
              else '❌ провалены пункты: %s (из %d)'
              % (', '.join(map(str, bad)), TOTAL)))
sys.exit(1 if bad else 0)
