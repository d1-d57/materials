"""G. «Хаос с ассистентом»: проверка кандидатов (часть 1).
Для каждого кандидата: brute() — все объекты в каноническом виде; script — что ассистент называет (в той форме,
как учитель пишет на доске); canon(item) -> канонический объект или None (недопустимый).
Проверяем: (1) каждый названный — допустимый объект; (2) названо ровно N = ответ записей;
(3) различных N-1; (4) ровно одна пара совпадает, и это заявленный повтор; (5) отсутствует ровно один — заявленный пропуск;
(6) разметка доски: все клетки разные, повтор-пара в разных четвертях доски (манхэттен >= 3).
Оценка времени (модельное допущение, не измерено): 2 с на фразу ассистента + 0.7 с на символ, который пишет учитель."""
from itertools import combinations, product
from collections import Counter

def parts(n, k=None, mx=None):
    mx = n if mx is None else mx
    if n == 0:
        if k in (None, 0): yield ()
        return
    if k == 0: return
    for a in range(min(n, mx), 0, -1):
        for rest in parts(n - a, None if k is None else k - 1, a):
            yield (a,) + rest

def canon_sum(s, total, k=None, allowed=None):
    xs = tuple(sorted((int(t) for t in s.replace(' ', '').split('+')), reverse=True))
    if sum(xs) != total: return None
    if k is not None and len(xs) != k: return None
    if allowed is not None and any(x not in allowed for x in xs): return None
    return xs

ALL = {}

def run(name, answer, brute, script, canon, repeat, skip, board, fmt=str):
    objs = set(brute)
    assert len(objs) == answer, (name, len(objs))
    cs = [canon(x) for x in script]
    bad = [x for x, c in zip(script, cs) if c is None or c not in objs]
    cnt = Counter(cs)
    dup = [c for c, m in cnt.items() if m > 1]
    missing = objs - set(cs)
    ok = True; msg = []
    if bad: ok = False; msg.append(f"недопустимые {bad}")
    if len(script) != answer: ok = False; msg.append(f"названо {len(script)} != {answer}")
    if len(set(cs)) != answer - 1: ok = False; msg.append(f"различных {len(set(cs))}")
    if dup != [canon(repeat[0])] or canon(repeat[0]) != canon(repeat[1]) or repeat[0] == repeat[1]:
        ok = False; msg.append(f"повтор {dup}")
    if missing != {skip}: ok = False; msg.append(f"пропуск {missing}")
    # доска
    cells = [board[x] for x in script]
    if len(set(cells)) != len(cells): ok = False; msg.append("клетки доски совпадают")
    (c1, r1), (c2, r2) = board[repeat[0]], board[repeat[1]]
    dist = abs(c1 - c2) + abs(r1 - r2)
    if dist < 3: ok = False; msg.append(f"повтор слишком близко на доске ({dist})")
    L0 = len(repeat[0].replace('-', '+').split('+')) if '+' in repeat[0] or '-' in repeat[0] else len(repeat[0])
    same = [x for x in script if x not in repeat and (len(x.replace('-', '+').split('+')) if ('+' in x or '-' in x) else len(x)) == L0]
    msg.append(f"рядом той же длины (приманки): {len(same)} {same}")
    secs = sum(2 + 0.7 * len(x.replace(' ', '')) for x in script)
    ALL[name] = ok
    print(f"[{name}] {'OK' if ok else 'FAIL'}  ответ={answer}, названо={len(script)}, различных={len(set(cs))}, "
          f"повтор: «{repeat[0]}» = «{repeat[1]}» = {fmt(canon(repeat[0]))}, пропуск: {fmt(skip)}, "
          f"расстояние на доске={dist}, время≈{secs:.0f} с {'; '.join(msg)}")
    # картинка доски 4 столбца x 3 строки
    grid = {board[x]: (i + 1, x) for i, x in enumerate(script)}
    W = max(len(x) for x in script) + 5
    for r in range(3):
        row = ''
        for c in range(4):
            if (c, r) in grid:
                i, x = grid[(c, r)]
                mark = '*' if x in repeat else ' '
                row += f"{i:>2}{mark}{x}".ljust(W)
            else:
                row += '·'.ljust(W)
        print('    ' + row)
    return ok

P = lambda t: '+'.join(map(str, t))

# ---------- K1. Разложения 6 (11) ----------
K1 = ["2+4", "1+1+1+1+1+1", "1+2+1+2", "3+3", "1+5", "1+1+2+1+1", "2+3+1", "6", "1+1+3+1", "2+1+1+2", "2+2+2"]
B1 = {"2+4": (0, 0), "1+1+1+1+1+1": (2, 1), "1+2+1+2": (0, 2), "3+3": (3, 0), "1+5": (1, 1), "1+1+2+1+1": (1, 2),
      "2+3+1": (2, 0), "6": (3, 2), "1+1+3+1": (0, 1), "2+1+1+2": (3, 1), "2+2+2": (2, 2)}
run("K1 разложения 6", 11, list(parts(6)), K1, lambda s: canon_sum(s, 6),
    ("1+2+1+2", "2+1+1+2"), (4, 1, 1), B1, P)

# ---------- K2. 10 = сумма четырёх натуральных (9) ----------
K2 = ["2+3+4+1", "1+5+1+3", "2+2+1+5", "1+1+1+7", "4+1+1+4", "2+2+4+2", "1+3+5+1", "3+1+3+3", "2+1+6+1"]
B2 = {"2+3+4+1": (1, 0), "1+5+1+3": (0, 0), "2+2+1+5": (0, 1), "1+1+1+7": (2, 1), "4+1+1+4": (3, 0),
      "2+2+4+2": (1, 2), "1+3+5+1": (3, 2), "3+1+3+3": (2, 0), "2+1+6+1": (2, 2)}
run("K2 10 на четыре слагаемых", 9, list(parts(10, 4)), K2, lambda s: canon_sum(s, 10, 4),
    ("1+5+1+3", "1+3+5+1"), (3, 3, 2, 2), B2, P)

# ---------- K3. 9 рублей монетами 1, 2, 5 (8) ----------
# учитель пишет так, как сказано; «5+1·4» — ассистент говорит «пятёрка и четыре рубля», учитель пишет 5+1+1+1+1
K3 = ["2+5+2", "1+2+1+1+2+1+1", "1+1+5+1+1", "2+2+1+2+2", "1+1+1+1+1+1+1+1+1", "1+2+1+5", "2+1+1+1+1+1+1+1", "2+1+1+1+1+1+2"]
B3 = {"2+5+2": (1, 0), "1+2+1+1+2+1+1": (0, 0), "1+1+5+1+1": (2, 1), "2+2+1+2+2": (3, 0),
      "1+1+1+1+1+1+1+1+1": (1, 2), "1+2+1+5": (0, 1), "2+1+1+1+1+1+1+1": (2, 2), "2+1+1+1+1+1+2": (3, 2)}
run("K3 9 рублей", 8, [p for p in parts(9) if set(p) <= {1, 2, 5}], K3,
    lambda s: canon_sum(s, 9, allowed={1, 2, 5}), ("1+2+1+1+2+1+1", "2+1+1+1+1+1+2"), (2, 2, 2, 1, 1, 1), B3, P)

# ---------- K4. Тройка дежурных из пятерых (10), повтор — в форме «все, кроме ...» ----------
L = "АБВГД"
def canon_team(s):
    if s.startswith("без "):
        out = set(s[4:]); assert len(out) == 2 and out <= set(L)
        return tuple(sorted(set(L) - out))
    assert len(s) == 3 and len(set(s)) == 3 and set(s) <= set(L)
    return tuple(sorted(s))
K4 = ["ВГА", "ДБА", "БГВ", "АДВ", "ГДБ", "без БД", "ВДГ", "БАГ", "АДГ", "ВБА"]
B4 = {"ВГА": (0, 0), "ДБА": (2, 0), "БГВ": (1, 1), "АДВ": (3, 0), "ГДБ": (0, 2), "без БД": (3, 2),
      "ВДГ": (2, 1), "БАГ": (1, 0), "АДГ": (2, 2), "ВБА": (0, 1)}
run("K4 трое дежурных из пятерых", 10, [tuple(c) for c in combinations(L, 3)], K4, canon_team,
    ("ВГА", "без БД"), tuple("БВД"), B4, ''.join)

# ---------- K5. Наряды 3 кофты x 2 юбки x 2 обуви (12) ----------
# кофты: Б(елая), Ж(ёлтая), З(елёная); юбки: Д(линная), К(ороткая); обувь: С(андалии), Т(уфли).
# Учитель пишет три буквы В ТОМ ПОРЯДКЕ, в каком ассистент назвал.
KOF, YUB, OB = "БЖЗ", "ДК", "СТ"
def canon_outfit(s):
    k = [x for x in s if x in KOF]; y = [x for x in s if x in YUB]; o = [x for x in s if x in OB]
    if not (len(k) == len(y) == len(o) == 1 and len(s) == 3): return None
    return k[0] + y[0] + o[0]
K5 = ["КБС", "ЗТД", "ЖКТ", "СДБ", "ТЗК", "БКТ", "ДЖС", "СЗК", "ТБД", "КТЖ", "ЖДТ", "ЗДС"]
B5 = {"КБС": (1, 0), "ЗТД": (3, 1), "ЖКТ": (0, 0), "СДБ": (2, 2), "ТЗК": (2, 0), "БКТ": (1, 1), "ДЖС": (0, 2),
      "СЗК": (3, 0), "ТБД": (2, 1), "КТЖ": (3, 2), "ЖДТ": (1, 2), "ЗДС": (0, 1)}
run("K5 наряды", 12, [a + b + c for a in KOF for b in YUB for c in OB], K5, canon_outfit, ("ЖКТ", "КТЖ"), "ЖКС", B5)

# ---------- K6. Маршруты 2x3 (10), повтор — в форме «вверх на шагах i и j» ----------
def canon_route(s):
    if s.startswith("В:"):
        i, j = map(int, s[2:].split(','))
        w = ['П'] * 5; w[i - 1] = 'В'; w[j - 1] = 'В'; return ''.join(w)
    assert len(s) == 5 and s.count('В') == 2 and s.count('П') == 3; return s
routes = [''.join(w) for w in product('ПВ', repeat=5) if w.count('В') == 2]
K6 = ["ПВППВ", "ВВППП", "ППВПВ", "ВППВП", "ПППВВ", "ПВПВП", "В:1,4", "ВПППВ", "ПВВПП", "ППВВП"]
B6 = {"ПВППВ": (3, 0), "ВВППП": (2, 0), "ППВПВ": (1, 1), "ВППВП": (0, 0), "ПППВВ": (0, 2), "ПВПВП": (2, 1),
      "В:1,4": (3, 2), "ВПППВ": (1, 0), "ПВВПП": (2, 2), "ППВВП": (0, 1)}
run("K6 маршруты 2x3", 10, routes, K6, canon_route, ("ВППВП", "В:1,4"), "ВПВПП", B6)

# ---------- K7. Флаги 3 полосы Б/К/С, соседние разные (12); повтор — названный «снизу вверх» ----------
flags = [''.join(w) for w in product('БКС', repeat=3) if w[0] != w[1] and w[1] != w[2]]
def canon_flag(s):
    if s.startswith('↑'): s = s[1:][::-1]   # «снизу вверх»
    return s if s in flags else None
K7 = ["КСК", "БКС", "СБС", "КБК", "↑СКБ", "СКБ", "БСБ", "КСБ", "СБК", "КБС", "СКС", "БКБ"]
B7 = {"КСК": (1, 0), "БКС": (0, 0), "СБС": (2, 0), "КБК": (3, 0), "↑СКБ": (3, 2), "СКБ": (2, 1), "БСБ": (0, 1),
      "КСБ": (1, 1), "СБК": (3, 1), "КБС": (0, 2), "СКС": (1, 2), "БКБ": (2, 2)}
run("K7 флаги (соседние разные)", 12, flags, K7, canon_flag, ("БКС", "↑СКБ"), "БСК", B7)

# ---------- K8. Треугольники из палочек 1..6 (7) ----------
def canon_tri(s):
    xs = tuple(sorted(map(int, s.split('-')), reverse=True))
    if len(set(xs)) != 3 or not all(1 <= x <= 6 for x in xs): return None
    return xs if xs[1] + xs[2] > xs[0] else None
tris = [c[::-1] for c in combinations(range(1, 7), 3) if c[0] + c[1] > c[2]]
K8 = ["3-5-4", "6-4-3", "2-4-3", "4-6-5", "4-2-5", "5-6-3", "3-6-5"]
B8 = {"3-5-4": (0, 0), "6-4-3": (2, 0), "2-4-3": (3, 1), "4-6-5": (1, 1), "4-2-5": (0, 2), "5-6-3": (3, 0), "3-6-5": (1, 2)}
run("K8 треугольники из палочек 1..6", 7, tris, K8, canon_tri, ("5-6-3", "3-6-5"), (6, 5, 2), B8,
    lambda t: '-'.join(map(str, t)))

print("ИТОГО:", sum(ALL.values()), "из", len(ALL), "кандидатов OK")
