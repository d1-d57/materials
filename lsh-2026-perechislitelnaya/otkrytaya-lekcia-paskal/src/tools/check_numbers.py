#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ГЕЙТ ЧИСЕЛ: каждое число, попавшее на слайд, пересчитано ПЕРЕБОРОМ, а не формулой.

  python3 src/tools/check_numbers.py            # прогнать все проверки
  python3 src/tools/check_numbers.py -v         # + печатать сами перебранные объекты

Правило захода (§1а.5): написал число на слайд — проверь его itertools.
Перебор идёт по настоящим последовательностям из О и Р, а не по формуле, которую
мы же и доказываем: иначе проверка проверяет саму себя. Формула — вторая сторона
равенства, и расхождение красит гейт.

Соглашение лекции (РАЗБОР §17.3): орёл = шаг ВВЕРХ (+1), решка = шаг ВНИЗ (−1).
Оно не декоративное: запрет «двух орлов подряд» превращается в «после подъёма сразу
спуск» только при таком соглашении.

Красное — exit 1.
"""
import sys
from itertools import product
from math import comb

VERBOSE = "-v" in sys.argv
FAILS = []
LINES = []


def check(name, got, want, note=""):
    ok = got == want
    LINES.append(("PASS" if ok else "FAIL") + "  " + name +
                 ("" if ok else "  — перебор даёт %r, на слайде %r" % (got, want)) +
                 (("   · " + note) if note and ok else ""))
    if not ok:
        FAILS.append(name)


def walks(L):
    """Все 2^L последовательностей длины L из '+' (орёл, вверх) и '-' (решка, вниз)."""
    return product("+-", repeat=L)


def heights(w):
    """Список высот после каждого шага, начиная с 0 (нулевая позиция не входит)."""
    h, out = 0, []
    for c in w:
        h += 1 if c == "+" else -1
        out.append(h)
    return out


def end(w):
    """Конечная высота пути; у пустого пути она нулевая (нужно для L = 0)."""
    hs = heights(w)
    return hs[-1] if hs else 0


def safe(w):
    """Путь ни разу не опускается ниже нуля (обрыв на уровне −1)."""
    return all(h >= 0 for h in heights(w))


# ─────────── 1. Основной ряд: путей длины L, не уходящих ниже нуля ───────────
SAFE_ROW = [len([w for w in walks(L) if safe(w)]) for L in range(0, 13)]
check("ряд безопасных путей, L = 0…10  (слайд «пьяница возвращается», РАЗБОР §17.2)",
      SAFE_ROW[:11], [1, 1, 2, 3, 6, 10, 20, 35, 70, 126, 252])

# чётная длина 2n → C(2n, n); нечётная 2n+1 → C(2n+1, n)
check("чётная длина: безопасных = C(2n,n) для n ≤ 6",
      [SAFE_ROW[2 * n] for n in range(7)], [comb(2 * n, n) for n in range(7)])
check("нечётная длина: безопасных = C(2n+1,n) для n ≤ 5  (РАЗБОР §17.2)",
      [SAFE_ROW[2 * n + 1] for n in range(6)], [comb(2 * n + 1, n) for n in range(6)])
check("нечётная длина: 2·C(2n,n) — НЕВЕРНО, гейт обязан это видеть",
      SAFE_ROW[5] != 2 * comb(4, 2), True,
      "L=5: перебор 10, ошибочная формула 12")

# ─────────── 2. Телескоп: безопасные пути длины 10 по числу орлов ───────────
BY_K = {}
for w in walks(10):
    if safe(w):
        BY_K[w.count("+")] = BY_K.get(w.count("+"), 0) + 1
check("телескоп: хороших путей длины 10 при k орлах, k = 5…10  (РАЗБОР §17.3)",
      [BY_K.get(k, 0) for k in range(5, 11)], [42, 90, 75, 35, 9, 1])
check("телескоп: те же числа как разности C(10,k) − C(10,k+1)",
      [comb(10, k) - comb(10, k + 1) for k in range(5, 11)], [42, 90, 75, 35, 9, 1])
check("телескоп: диапазон k — ровно от 5 до 10 (ниже пяти безопасных нет)",
      sorted(BY_K), [5, 6, 7, 8, 9, 10])
check("телескоп: контрольная сумма 42+90+75+35+9+1",
      sum(BY_K.values()), 252)
check("телескоп: сумма = C(10,5)", 252, comb(10, 5))

# ─────────── 3. Фибоначчи: слова без двух О подряд ───────────
def good(w):
    return "++" not in "".join(w)


GOOD_ROW = [len([w for w in walks(L) if good(w)]) for L in range(1, 11)]
check("хороших слов длины 1…10  (слайды S8/S8B, РАЗБОР §17.4)",
      GOOD_ROW, [2, 3, 5, 8, 13, 21, 34, 55, 89, 144])
check("хороших слов длины 10 ровно 144", GOOD_ROW[-1], 144)
check("рекуррента F(n+1)=F(n)+F(n−1) держится на всём ряду",
      all(GOOD_ROW[i] == GOOD_ROW[i - 1] + GOOD_ROW[i - 2] for i in range(2, 10)), True)
check("хорошие слова длины 3 — их пять  (вопрос 8 бота)",
      sorted("".join(w) for w in walks(3) if good(w)),
      sorted(["---", "--+", "-+-", "+--", "+-+"]))
check("хороших слов длины 10 ровно с тремя О  (вопрос 9 бота: C(8,3))",
      len([w for w in walks(10) if good(w) and w.count("+") == 3]), comb(8, 3))
check("C(8,3) = 56", comb(8, 3), 56)
check("разбор F4 = F3 + F2, то есть 8 = 5 + 3  (слайд S8B)",
      (GOOD_ROW[3], GOOD_ROW[2], GOOD_ROW[1]), (8, 5, 3))
# биекция §8B поштучно: слово длины 4 кончается на Р → любое хорошее длины 3;
# кончается на О → перед ней обязана быть Р → любое хорошее длины 2
g4 = ["".join(w) for w in walks(4) if good(w)]
check("биекция S8B: из восьми слов длины 4 ровно 5 кончаются решкой и 3 орлом",
      (len([s for s in g4 if s.endswith("-")]), len([s for s in g4 if s.endswith("+")])),
      (5, 3))
check("биекция S8B: у каждого слова на О перед ней стоит Р",
      all(s[-2] == "-" for s in g4 if s.endswith("+")), True)

# ─────────── 4. Домики: слова длины n без двух О подряд, ровно k орлов ───────────
def by_k_good(n):
    d = {}
    for w in walks(n):
        if good(w):
            d[w.count("+")] = d.get(w.count("+"), 0) + 1
    return d


for n in (6, 10):
    d = by_k_good(n)
    check("домики: слов длины %d с k орлами = C(%d−k, k) для всех k" % (n, n + 1),
          [d.get(k, 0) for k in range(0, n // 2 + 2)],
          [comb(n + 1 - k, k) for k in range(0, n // 2 + 2)])

# ─────────── 5. Столбцы и треугольник Паскаля ───────────
def reach(L):
    return sorted({h for w in walks(L) for h in [end(w)]})


check("вопрос 1: за 10 шагов частица попадает во все чётные от −10 до 10, их 11",
      (reach(10), len(reach(10))), (list(range(-10, 11, 2)), 11))
check("вопрос 1б: за 11 шагов — во все нечётные от −11 до 11, их 12",
      (reach(11), len(reach(11))), (list(range(-11, 12, 2)), 12))
p3 = {}
for w in walks(3):
    p3[end(w)] = p3.get(end(w), 0) + 1
check("вопрос 2: после трёх шагов вероятности в −3,−1,1,3 равны 1/8, 3/8, 3/8, 1/8",
      [p3[h] for h in (-3, -1, 1, 3)], [1, 3, 3, 1])
check("вопрос 3: каждое число — полусумма двух соседей слева (проверено до 8 шага)",
      all(len([w for w in walks(L) if end(w) == h]) ==
          len([w for w in walks(L - 1) if end(w) == h - 1]) +
          len([w for w in walks(L - 1) if end(w) == h + 1])
          for L in range(1, 9) for h in range(-L, L + 1)), True)
check("вопрос 5: траекторий длины 10 в точку 4 ровно C(10,7) = 120",
      len([w for w in walks(10) if end(w) == 4]), 120)
check("C(10,7) = 120", comb(10, 7), 120)
# ⚠ ПОЙМАНО ГЕЙТОМ. РАЗБОР §4 предлагает спросить «сколькими способами попасть
# в точку 3 за 8 шагов». Перебор даёт НОЛЬ: за 8 шагов достижимы только чётные точки,
# и это ровно тот факт, который лекция доказывает слайдом раньше (вопрос 1 бота).
# Вопрос переставлен на точку 2 — число шагов владельца сохранено. См. ## ВОПРОСЫ.
check("S4: за 8 шагов в точку 3 попасть НЕЛЬЗЯ — чётность (формулировка §4 не годится)",
      len([w for w in walks(8) if end(w) == 3]), 0)
check("S4: «сколькими способами попасть в точку 2 за 8 шагов» — ответ 56",
      len([w for w in walks(8) if end(w) == 2]), 56)
check("S4: то же число = вероятность × 2^8, то есть C(8,5)", comb(8, 5), 56)
check("сумма строки треугольника = 2^n для n ≤ 10",
      [sum(comb(n, k) for k in range(n + 1)) for n in range(11)],
      [2 ** n for n in range(11)])
check("суммы строк на слайде S5B: 1, 2, 4, 8, 16",
      [2 ** n for n in range(5)], [1, 2, 4, 8, 16])
check("симметрия строки: C(n,k) = C(n,n−k) для n ≤ 12",
      all(comb(n, k) == comb(n, n - k) for n in range(13) for k in range(n + 1)), True)

# ─────────── 6. Сумма квадратов ───────────
check("вопрос 6: сумма квадратов шестой строки 1,6,15,20,15,6,1",
      sum(comb(6, k) ** 2 for k in range(7)), 924)
check("вопрос 6: она же C(12,6)", comb(12, 6), 924)
check("сумма квадратов строки n = C(2n,n) для n ≤ 10  (канвас S7)",
      [sum(comb(n, k) ** 2 for k in range(n + 1)) for n in range(11)],
      [comb(2 * n, n) for n in range(11)])
check("центральный столбец 1, 2, 6, 20, 70 (слайд S10, узнавание)",
      [comb(2 * n, n) for n in range(5)], [1, 2, 6, 20, 70])
check("вопрос 7: двое по 10 бросков поровну орлов — C(20,10)/2^20",
      sum(comb(10, k) * comb(10, k) for k in range(11)), comb(20, 10))
check("C(20,10) = 184756", comb(20, 10), 184756)

# ─────────── 7. Задача о дежурных (S5C) ───────────
check("дежурные: C(25,3)·22 = C(25,4)·4 = 25·C(24,3)",
      (comb(25, 3) * 22, comb(25, 4) * 4, 25 * comb(24, 3)),
      (comb(25, 3) * 22, comb(25, 3) * 22, comb(25, 3) * 22))
check("дежурные: обе связи вида (k+1)C(n,k+1) = (n−k)C(n,k), n ≤ 20",
      all((k + 1) * comb(n, k + 1) == (n - k) * comb(n, k)
          for n in range(1, 21) for k in range(n)), True)
check("раскрутка строки из единицы: 1 → 5 → 10 → 10 → 5 множителями 5/1, 4/2, 3/3, 2/4",
      [comb(5, k) for k in range(5)], [1, 5, 10, 10, 5])

# ─────────── 8. Отражение (S11–S12) ───────────
def touches(w, level=-1):
    return any(h <= level for h in heights(w))


L, END = 11, 5
bad = [w for w in walks(L) if end(w) == END and touches(w)]
def reflect(w):
    """Отразить начальный кусок до первого касания −1 относительно уровня −1."""
    h, i = 0, None
    for j, c in enumerate(w):
        h += 1 if c == "+" else -1
        if h == -1:
            i = j
            break
    flip = {"+": "-", "-": "+"}
    return "".join(flip[c] for c in w[:i + 1]) + "".join(w[i + 1:])


img = sorted(reflect(w) for w in bad)
from_m2 = sorted("".join(w) for w in walks(L) if end(w) == END + 2)
check("вопрос 11: отражение даёт РОВНО все пути из −2 в 5, каждый по одному разу",
      img, from_m2)
check("вопрос 11б: их C(11,9) = 55", len(from_m2), comb(11, 9))
check("C(11,9) = 55", comb(11, 9), 55)
check("при отражении число орлов растёт ровно на единицу  (РАЗБОР §16.9 — «по факту»)",
      sorted({reflect(w).count("+") - w.count("+") for w in bad}), [1])
check("вопрос 10: траекторий длины 4, ни разу не попавших в −1, ровно шесть",
      sorted("".join(w) for w in walks(4) if safe(w)),
      sorted(["++++", "+++-", "++-+", "++--", "+-++", "+-+-"]))
check("S12: хороших путей длины 10 с 5 орлами = C(10,5) − C(10,6)  (РАЗБОР §12)",
      BY_K[5], comb(10, 5) - comb(10, 6))
check("C(10,5) − C(10,6) = 252 − 210 = 42", (comb(10, 5), comb(10, 6)), (252, 210))

# ─────────── 9. Финал ───────────
check("вероятность продержаться 10 шагов = 252/1024",
      (SAFE_ROW[10], 2 ** 10), (252, 1024))
check("хороших слов длины 10: вероятность 144/1024 = 0,140625  (РАЗБОР §17.4)",
      round(144 / 1024, 6), 0.140625)
check("ответ для 100 шагов — C(100,50), безопасных путей ровно столько (формула, "
      "перебор до L=12 её подтверждает)",
      [SAFE_ROW[L] for L in range(0, 13, 2)],
      [comb(L, L // 2) for L in range(0, 13, 2)])

if VERBOSE:
    LINES.append("")
    LINES.append("хорошие слова длины 4 (S8B): " + ", ".join(
        s.replace("+", "О").replace("-", "Р") for s in g4))
    LINES.append("безопасные длины 4 (вопрос 10): " + ", ".join(
        "".join(w).replace("+", "О").replace("-", "Р") for w in walks(4) if safe(w)))

print("\n".join(LINES))
print("\n" + ("ВСЕ ЧИСЛА СОШЛИСЬ — проверок %d" % len(LINES)
              if not FAILS else "%d РАСХОЖДЕНИЙ: %s" % (len(FAILS), FAILS)))
sys.exit(1 if FAILS else 0)
