# Занятие Миши 04.10.2026. Основа — ДЗ 27.09 (не решено дома) + три сюжета: рыцари (разминка) → раскраски (середина) → игра с камнями (выдох).
# Геймификация v1: разделы с 'lock' открываются за звёзды из копилки (misha:stars − misha:spent), покупки общие для всех занятий.
import sys, pathlib, runpy
H = pathlib.Path(__file__).parent
sys.path.insert(0, str(H))
from build import euler

DZ = {s['title']: s for s in runpy.run_path(str(H / 'dz-2026-09-27.py'))['LESSON']['sections']}

def board(cut=None, n=5, c=64):
    """Доска n×n, углы чёрные; cut=(r,k) — вырезанная клетка."""
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 -6 {n*c+12} {n*c+12}" width="{n*c+12}" role="img" class="bd">']
    for r in range(n):
        for k in range(n):
            x, y = k * c, r * c
            if cut == (r, k):
                o.append(f'<rect x="{x+3}" y="{y+3}" width="{c-6}" height="{c-6}" fill="none" stroke="#c03636" stroke-width="3" stroke-dasharray="7 6"/>')
            else:
                o.append(f'<rect x="{x}" y="{y}" width="{c}" height="{c}" fill="{"#3b4252" if (r+k) % 2 == 0 else "#ffffff"}" stroke="#18202e" stroke-width="1.5"/>')
    o.append('</svg>')
    return ''.join(o)


def pryam(a, b, c, cell=44, nums=True):
    """Прямоугольник (a+b)×c из клеток: левая часть a×c, правая b×c."""
    W, H = (a + b) * cell, c * cell
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-60 -50 {W+80} {H+70}" width="{W+80}" role="img" class="bd">']
    o.append(f'<rect x="0" y="0" width="{a*cell}" height="{H}" fill="#ffd8a8"/><rect x="{a*cell}" y="0" width="{b*cell}" height="{H}" fill="#a5d8ff"/>')
    if nums:
        for i in range(a + b + 1): o.append(f'<line x1="{i*cell}" y1="0" x2="{i*cell}" y2="{H}" stroke="#18202e" stroke-width="1" opacity=".35"/>')
        for j in range(c + 1): o.append(f'<line x1="0" y1="{j*cell}" x2="{W}" y2="{j*cell}" stroke="#18202e" stroke-width="1" opacity=".35"/>')
    o.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="#18202e" stroke-width="3"/><line x1="{a*cell}" y1="-8" x2="{a*cell}" y2="{H+8}" stroke="#c03636" stroke-width="4"/>')
    o.append(f'<text x="{a*cell/2}" y="-14" font-size="30" text-anchor="middle" font-family="Golos Text,sans-serif" fill="#18202e">{a}</text>')
    o.append(f'<text x="{a*cell+b*cell/2}" y="-14" font-size="30" text-anchor="middle" font-family="Golos Text,sans-serif" fill="#18202e">{b}</text>')
    o.append(f'<text x="-18" y="{H/2+10}" font-size="30" text-anchor="end" font-family="Golos Text,sans-serif" fill="#18202e">{c}</text>')
    return ''.join(o) + '</svg>'

STOL4 = 'За круглым столом сидят 4 человека. Каждый сказал: «Оба моих соседа — лжецы».'
STOL6 = 'А если за столом 6 человек и каждый сказал то же самое?'
SH4 = 'В шеренге 4 человека. Каждый, кроме самого правого, сказал: «Мой сосед справа — лжец».'
KAM = 'Из кучки по очереди берут 1 или 4 камня. Кто взял последний — выиграл.'
ON = '{?чёрной/белой=%s}'

LESSON = {
 'id': 'zanyatie-2026-10-04', 'title': 'Занятие 4 октября', 'badge': '', 'code': 'ТЫКВА',
 'sections': [
  {'title': 'Занятие 4 октября', 'items': [{'type': 'cover', 'title': 'Привет, Миша!', 'text': '4 октября', 'button': 'Начать', 'bg': 'pryatki/bg-les.jpg'}]},
  {'title': 'Остров рыцарей', 'items': [{'type': 'cover', 'title': 'Остров рыцарей', 'text': 'рыцари всегда говорят правду, лжецы всегда лгут', 'button': 'Вперёд', 'bg': 'pryatki/bg-kot.jpg'}]},
  {'title': 'Рыцари и лжецы', 'items': [
     {'type': 'slots', 'q': STOL4, 'lines': ['Рыцарей: {2}']},
     {'type': 'slots', 'q': STOL6, 'lines': ['Может ли рыцарей быть 3? {?да/нет=да}', 'А 2? {?да/нет=да}', 'А 1? {?да/нет=нет}', 'А 4? {?да/нет=нет}']},
     {'type': 'slots', 'q': SH4, 'lines': ['Рыцарей: {2}']},
     {'type': 'slots', 'q': 'А если в шеренге 5 человек?', 'lines': ['Может ли рыцарей быть 2? {?да/нет=да}', 'А 3? {?да/нет=да}', 'А 4? {?да/нет=нет}']},
     {'type': 'slots', 'q': 'А: «Среди нас ровно один лжец». Б: «Среди нас ровно два лжеца». В: «Среди нас ровно три лжеца».',
      'lines': ['А — {?рыцарь/лжец=лжец}', 'Б — {?рыцарь/лжец=рыцарь}', 'В — {?рыцарь/лжец=лжец}']},
  ]},
  {'title': 'Минутка', 'items': [{'type': 'cover', 'title': 'Подпрыгни 10 раз', 'text': 'столько, сколько людей сидело за двумя столами вместе', 'button': 'Готово', 'bg': 'pryatki/bg-sportzal.jpg'}]},
  {'title': 'Считаем', 'items': [{'type': 'cover', 'title': 'Считаем', 'text': '', 'button': 'Вперёд', 'bg': 'pryatki/bg-ploshchadka.jpg'}]},
  DZ['Разбей удобно'],
  DZ['Найди ошибку'],
  DZ['Порядок действий'],
  DZ['Множества'],
  {'title': 'Доски и кони', 'items': [{'type': 'cover', 'title': 'Доски и кони', 'button': 'Вперёд', 'bg': 'pryatki/bg-labirint.jpg'}]},
  {'title': 'Раскраски', 'items': [
     {'type': 'euler', 'q': 'Доска 5 × 5, углы чёрные', 'svg': board(), 'lines': ['Чёрных клеток: {13}', 'Белых: {12}']},
     {'type': 'euler', 'q': 'Вырезали одну клетку. Остальное хотим закрыть доминошками.', 'svg': board((0, 0)),
      'lines': ['Клеток осталось: {24}', 'Доминошек нужно: {12}', 'Каждая закрывает чёрных: {1}', 'Значит, вырезать надо {?чёрную/белую=чёрную}']},
     {'type': 'choice', 'q': 'Какие доски можно закрыть доминошками?', 'multi': True, 'ok': [0, 2],
      'options': [board((0, 0), c=52), board((0, 1), c=52), board((2, 2), c=52)]},
     {'type': 'slots', 'q': 'Конь стоит на чёрной клетке.', 'lines': ['После 1 хода он на ' + ON % 'белой', 'после 2 ходов — на ' + ON % 'чёрной', 'после 7 ходов — на ' + ON % 'белой']},
     {'type': 'slots', 'q': 'Может ли конь вернуться на свою клетку', 'lines': ['за 7 ходов? {?да/нет=нет}', 'за 6 ходов? {?да/нет=да}', 'за 11 ходов? {?да/нет=нет}']},
  ]},
  {'title': 'Минутка', 'items': [{'type': 'cover', 'title': 'Присядь 13 раз', 'text': 'столько, сколько чёрных клеток на доске 5 × 5', 'button': 'Готово', 'bg': 'pryatki/bg-sportzal.jpg'}]},
  {'title': 'Лавка', 'items': [{'type': 'cover', 'title': 'Лавка открыта', 'shop': True, 'button': 'Дальше', 'bg': 'pryatki/bg-bassejn.jpg'}]},
  {'title': 'Перерыв', 'items': [{'type': 'cover', 'title': 'Перерыв', 'bg': 'pryatki/bg-kafe.jpg',
     'text': '<a class="ext" href="kletki-i-strelki.html" target="_blank">Клетки и стрелки ↗</a>', 'button': 'Дальше'}]},
  DZ['Судоку'],
  DZ['Задача'],
  {'title': 'Игра', 'items': [{'type': 'cover', 'title': 'Игра', 'text': 'кто возьмёт последний?', 'button': 'Вперёд', 'bg': 'pryatki/bg-zima.jpg'}]},
  {'title': 'Камни', 'items': [
     {'type': 'slots', 'q': KAM, 'lines': ['Камней 2 — выиграет {?первый/второй=второй}', 'Камней 3 — {?первый/второй=первый}', 'Камней 5 — {?первый/второй=второй}']},
     {'type': 'slots', 'q': KAM, 'lines': ['Проигрышные для того, кто ходит, до 12:', '{#2;5;7;10;12}']},
     {'type': 'slots', 'q': KAM, 'lines': ['Камней 20 — выиграет {?первый/второй=второй}', 'Камней 23 — {?первый/второй=первый}', 'Из 23 первым ходом взять {1}']},
  ]},
  DZ['Футошики'],
  {'title': 'Прямоугольники', 'items': [
     {'type': 'euler', 'q': 'Сколько клеток?', 'svg': pryam(5, 2, 3), 'lines': ['Оранжевых: 5 · 3 = {15}', 'Синих: 2 · 3 = {6}', 'Всего: 7 · 3 = {21}']},
     {'type': 'euler', 'q': '', 'svg': pryam(5, 2, 3), 'lines': ['(5 + 2) · 3 = 5 · 3 + {2} · {3}', '21 = 15 + {6}']},
     {'type': 'euler', 'q': '', 'svg': pryam(10, 4, 6, cell=26, nums=False), 'lines': ['(10 + 4) · 6', '= {60} + {24}', '= {84}']},
     {'type': 'slots', 'q': 'Без картинки', 'lines': ['(20 + 3) · 4 = {80} + {12} = {92}', '(30 + 6) · 5 = {150} + {30} = {180}']},
     {'type': 'slots', 'q': 'Наоборот: склей два прямоугольника', 'lines': ['7 · 8 + 3 · 8 = {10} · 8 = {80}', '26 · 5 + 4 · 5 = {30} · 5 = {150}']},
     {'type': 'euler', 'q': 'Три куска', 'svg': pryam(3, 4, 5), 'lines': ['(3 + 4) · 5 = {15} + {20} = {35}']},
     {'type': 'choice', 'q': 'Какая запись верная?', 'ok': [1], 'options': ['(a + b) · c = a + b · c', '(a + b) · c = a · c + b · c', '(a + b) · c = a · c + b']},
     {'type': 'slots', 'q': 'Проверь на числах: a = 2, b = 3, c = 4', 'lines': ['(2 + 3) · 4 = {20}', '2 + 3 · 4 = {14}', '2 · 4 + 3 · 4 = {20}']},
     {'type': 'slots', 'q': '', 'lines': ['34 · 2 = (30 + 4) · 2 = {60} + {8} = {68}', '27 · 6 = (20 + 7) · 6 = {120} + {42} = {162}']},
  ]},
  {'title': 'Множества — ещё', 'items': [
     {'type': 'slots', 'q': 'M = {2; 4; 6; 8}', 'lines': ['4 {?∈/∉=∈} M', '5 {?∈/∉=∉} M', '8 {?∈/∉=∈} M', 'Элементов в M: {4}']},
     {'type': 'slots', 'q': 'M = {2; 4; 6; 8}', 'lines': ['｛2; 4｝ {?⊂/⊄=⊂} M', '｛4; 5｝ {?⊂/⊄=⊄} M', '｛8｝ {?⊂/⊄=⊂} M']},
     {'type': 'slots', 'q': 'Какой знак?', 'lines': ['6 {?∈/⊂=∈} M', '｛6｝ {?∈/⊂=⊂} M', '｛2; 6｝ {?∈/⊂=⊂} M']},
     {'type': 'slots', 'q': 'Запиши множество', 'lines': ['двузначных чисел меньше 15:', '{#10;11;12;13;14}']},
     {'type': 'slots', 'q': 'A = {1; 2; 3; 4},  B = {3; 4; 5}', 'lines': ['A ∩ B = {#3;4}', 'A ∪ B = {#1;2;3;4;5}']},
     {'type': 'slots', 'q': 'A = {1; 2; 3; 4},  B = {3; 4; 5}', 'lines': ['B ∩ A = {#3;4}', 'A ∩ B и B ∩ A {?равны/не равны=равны}', 'A ∪ B и B ∪ A {?равны/не равны=равны}']},
     {'type': 'choice', 'q': 'A — умеют плавать, B — умеют играть на скрипке. Кто в A ∩ B?', 'ok': [0], 'options': ['и плавают, и играют', 'плавают или играют', 'только плавают']},
     {'type': 'choice', 'q': 'A — умеют плавать, B — умеют играть на скрипке. Кто в A ∪ B?', 'ok': [1], 'options': ['и плавают, и играют', 'хотя бы что-то одно', 'никто']},
     {'type': 'slots', 'q': 'A — числа меньше 10, B — чётные числа меньше 10', 'lines': ['B {?⊂/⊄=⊂} A', 'A {?⊂/⊄=⊄} B', 'B = {#0;2;4;6;8|2;4;6;8}']},
  ]},
  {'title': 'Секретная задача', 'shop': {'emo': '🔐'}, 'lock': {'id': 'sekret-1', 'price': 4}, 'items': [
     {'type': 'slots', 'q': 'За круглым столом 10 человек. Каждый сказал: «Оба моих соседа — лжецы».',
      'lines': ['Может ли рыцарей быть 5? {?да/нет=да}', 'А 4? {?да/нет=да}', 'А 3? {?да/нет=нет}', 'А 6? {?да/нет=нет}']},
  ]},
  {'title': 'Ваня приседает 10 раз', 'shop': {'emo': '🏋️'}, 'lock': {'id': 'vanya-sit-1', 'price': 3}, 'items': [
     {'type': 'cover', 'title': 'Ваня, приседай!', 'text': 'считай вслух', 'button': 'Дальше'}]},
  {'title': 'Задача для Вани', 'shop': {'emo': '🧠'}, 'lock': {'id': 'vanya-task-1', 'price': 5}, 'items': [
     {'type': 'cover', 'title': 'Придумай задачу Ване', 'text': 'он решает при тебе', 'button': 'Дальше'}]},
  {'title': 'Ваня отжимается 10 раз', 'shop': {'emo': '💪'}, 'lock': {'id': 'vanya-otzhim-1', 'price': 2}, 'items': [
     {'type': 'cover', 'title': 'Ваня, отжимайся!', 'text': 'считай вслух', 'button': 'Дальше'}]},
  {'title': 'Ваня рисует', 'shop': {'emo': '✏️'}, 'lock': {'id': 'vanya-risuet-1', 'price': 4}, 'items': [
     {'type': 'cover', 'title': 'Скажи, что нарисовать', 'text': 'у Вани минута', 'button': 'Дальше'}]},
  {'title': 'Математический фокус', 'shop': {'emo': '🎩'}, 'lock': {'id': 'fokus-1', 'price': 6}, 'items': [
     {'type': 'cover', 'title': 'Фокус!', 'text': 'Ваня показывает, ты разгадываешь', 'button': 'Дальше'}]},
  {'title': 'Игра на выбор', 'shop': {'emo': '🎲'}, 'lock': {'id': 'igra-1', 'price': 8}, 'items': [
     {'type': 'cover', 'title': 'Выбирай игру!', 'button': 'Дальше'},
  ]},
  # картины с прятками внутри движка — из PRYATKI ниже (когда будут файлы картин)
  {'title': 'Готово', 'items': [{'type': 'cover', 'final': True, 'title': 'Готово!', 'bg': 'pryatki/bg-semya.jpg'}]},
 ]}

# Картины и лабиринты: pryatki.py рядом задаёт PRYATKI = [{'id','title','img' (путь от zanyatiya/),'mode': 'find'|'maze','n','price','stars'}]
pr = H / 'pryatki.py'
if pr.exists():
    for p in runpy.run_path(str(pr))['PRYATKI']:
        it = {'type': 'pic', 'q': '', 'img': p['img'], 'mode': p.get('mode', 'find')}
        for k in ('n', 'stars'):
            if k in p: it[k] = p[k]
        LESSON['sections'].insert(-1, {'title': p['title'], 'shop': {'name': p.get('name', p['title'])}, 'lock': {'id': p['id'], 'price': p.get('price', 10)}, 'items': [it]})

# Буквы чит-кода «ТЫКВА»: открываются верным ответом
def _letter(title, i, ch):
    s = next(s for s in LESSON['sections'] if s['title'] == title); s['items'][i] = dict(s['items'][i], letter=ch)
for t, i, ch in [('Рыцари и лжецы', 4, 'Т'), ('Найди ошибку', 0, 'Ы'), ('Множества', 3, 'К'), ('Раскраски', 2, 'В'), ('Камни', 2, 'А')]:
    _letter(t, i, ch)
