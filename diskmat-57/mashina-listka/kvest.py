# -*- coding: utf-8 -*-
"""КВЕСТ-КАРТА листка: проверка графа и симуляция баланса (Р187, Р193, Р199).

Граф карты задаётся так (всё — строки-идентификаторы клеток «задача:буква»):
  OUT   {клетка: следующая}  — у КАЖДОЙ клетки ровно один выход вверх; последняя клетка пути ведёт в 'PEAK';
  ENTRY [клетка, ...]      — клетки, в которые ведёт линия от лагеря ('CAMP');
  DIFF  {клетка: 1|2|3}     — трудность пункта (1 — техника, 2 — идея, 3 — звёздочка уровня);
  SKULL [клетки] — одна попытка, ошибка сжигает жизнь; COIN [клетки] — сдал: +1 жизнь.
Правило хода: клетка открыта, если закрашена клетка, из которой в неё ведёт линия (или лагерь для ENTRY).

⚠ Все вероятности и времена в модели — ДОПУЩЕНИЯ аналитика, откалиброванные по одному уроку (22.09: 14 из 23
закрыли обязательную дорогу; модель даёт 64%). После каждого урока с картой — перекалибровать по SDACHA
(svod.py печатает факт «лагерь/вершина»), иначе симуляция ничего не доказывает.
"""
import random, statistics as st

# Время — ЧЕСТНОЕ (29.09, Р207): пара 90 мин − контрольная с разбором 20 − раздача 5 = ~65 мин работы у среднего;
# тропа ○ ≈ 10 пунктов по ~4 мин. Прежняя модель (бюджет 95–110 мин, база ×1,6) завышала вершину вдвое (55% вместо 30%).
TYPES = {'сильный': dict(share=.3, speed=.8, pb=.99, pr={1: .8, 2: .6, 3: .25}, budget=70),
         'средний': dict(share=.5, speed=1.0, pb=.96, pr={1: .6, 2: .4, 3: .1}, budget=65),
         'слабый':  dict(share=.2, speed=1.6, pb=.88, pr={1: .35, 2: .2, 3: .03}, budget=60)}
RT = {1: 4, 2: 6, 3: 9}      # минут на пункт подготовленному ребёнку
HELP = .5                    # вероятность, что застрявший пункт базы берётся с помощью принимающего (второй урок пары)

def validate(OUT, ENTRY, DIFF):
    """Краснеет (AssertionError), если нарушено: один выход у клетки; нет циклов; всё достижимо из лагеря;
    каждая тропа доходит до вершины. Возвращает {вход: длина пути до вершины в пунктах}."""
    cells = set(DIFF)
    assert set(OUT) == cells, f'у клеток нет выхода или лишние выходы: {cells ^ set(OUT)}'
    for c, n in OUT.items(): assert n == 'PEAK' or n in cells, f'{c} ведёт в несуществующую клетку {n}'
    lens = {}
    for e in ENTRY:
        c, seen = e, set()
        while c != 'PEAK':
            assert c not in seen, f'цикл через {c}'; seen.add(c); c = OUT[c]
        lens[e] = len(seen)
    reach = set()
    for e in ENTRY:
        c = e
        while c != 'PEAK': reach.add(c); c = OUT[c]
    # клетка достижима, если из неё и из какого-то входа приходим в неё: проверяем через обратный обход
    IN = {}
    for a, b in OUT.items(): IN.setdefault(b, []).append(a)
    ok = set(ENTRY); stack = list(ENTRY)
    while stack:
        c = stack.pop(); n = OUT[c]
        if n != 'PEAK' and n not in ok: ok.add(n); stack.append(n)
    assert ok == cells, f'недостижимы из лагеря: {cells - ok}'
    return lens

def simulate(OUT, ENTRY, DIFF, SKULL=(), COIN=(), BASE=(4,) * 10, klass=25, runs=300,
             mults=(0.7, 1.0, 1.3), seed=3, types=TYPES, base_factor=1.0, help=None, po_tipam=False):
    """Доля класса, дошедшего до лагеря («4») и до вершины («5») при множителе трудности ромбов mult.
    BASE — минуты на пункты обязательной тропы у среднего (умножаются на скорость типа); HELP — доля застрявших
    пунктов, которые берутся с помощью принимающего (5 принимающих 29.09 → разумно 0,7).
    po_tipam=True → {mult: {тип: (лагерь, вершина)}} вместо {mult: (лагерь, вершина)}."""
    H = HELP if help is None else help
    IN = {}
    for a, b in OUT.items(): IN.setdefault(b, []).append(a)
    for e in ENTRY: IN.setdefault(e, []).append('CAMP')
    def dpk(c):
        n = 0
        while c != 'PEAK': c = OUT[c]; n += 1
        return n
    def kid(Tp, rng, mult):
        t = 0
        for m in BASE:
            t += m * Tp['speed'] * base_factor
            if rng.random() >= Tp['pb'] and rng.random() >= H: return (False, False)
        done = {'CAMP'}; lives = 1; dead = set(); tried = {}
        while t < Tp['budget']:
            front = [c for c in DIFF if c not in done and c not in dead and any(p in done for p in IN.get(c, [])) and tried.get(c, 0) < 3]
            if not front: break
            c = min(front, key=lambda c: (dpk(c), DIFF[c], rng.random()))
            t += RT[DIFF[c]] * Tp['speed']
            if t > Tp['budget']: break
            tried[c] = tried.get(c, 0) + 1
            if rng.random() < Tp['pr'][DIFF[c]] * mult:
                done.add(c)
                if c in COIN: lives += 1
                if OUT[c] == 'PEAK': return (True, True)
            elif c in SKULL:
                if lives: lives -= 1
                else: dead.add(c)
        return (True, False)
    res = {}
    for mult in mults:
        rng = random.Random(seed); B = []; D = []; T = {k: [] for k in types}
        for _ in range(runs):
            r = []
            for k, Tp in types.items():
                rk = [kid(Tp, rng, mult) for _ in range(round(klass * Tp['share']))]; r += rk; T[k] += rk
            B.append(sum(x[0] for x in r) / len(r)); D.append(sum(x[1] for x in r) / len(r))
        res[mult] = ({k: (st.mean(x[0] for x in v), st.mean(x[1] for x in v)) for k, v in T.items()} if po_tipam
                     else (st.mean(B), st.mean(D)))
    return res

def report(OUT, ENTRY, DIFF, SKULL=(), COIN=(), klass=25, **kw):
    lens = validate(OUT, ENTRY, DIFF)
    print('граф карты: всё вверх, у каждой клетки один выход, всё достижимо — ок')
    print('длина пути лагерь → вершина по входам:', lens)
    for m, (b, d) in simulate(OUT, ENTRY, DIFF, SKULL, COIN, klass=klass, **kw).items():
        print(f'трудность ромбов ×{m}: «5» {d:.0%} · «4» {b - d:.0%} · ниже «4» {1 - b:.0%} (≈{(1 - b) * klass:.0f} чел. из {klass})')
    print('по типам детей при ×1.0 (лагерь / вершина):')
    for k, (b, d) in simulate(OUT, ENTRY, DIFF, SKULL, COIN, klass=klass, mults=(1.0,), po_tipam=True, **kw)[1.0].items():
        print(f'  {k}: {b:.0%} / {d:.0%}')
    print('рычаг «помощь принимающего на застрявшем пункте ○» (при ×1.0):')
    for h in (.5, .7, .85):
        (b, d), = simulate(OUT, ENTRY, DIFF, SKULL, COIN, klass=klass, mults=(1.0,), help=h, **kw).values()
        print(f'  помощь {h:.0%}: «5» {d:.0%} · ниже «4» {1 - b:.0%} (≈{(1 - b) * klass:.0f} чел.)')
