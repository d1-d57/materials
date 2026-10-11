"""Проверка кандидатов на «гроб» КР 6.10 (7И, школа 57).
Каждая функция считает ответ ПРЯМЫМ перебором объектов, не по формуле.
Запуск: python3 kr_grob_proverka.py  (все assert должны пройти)."""
from fractions import Fraction
from itertools import combinations


# 1. Квадраты с вершинами в узлах решётки (включая наклонные)
def kvadraty_v_uzlah(stolbcov, strok):
    """Узлы (x, y): 0 <= x < stolbcov, 0 <= y < strok. Перебираем все пары
    узлов как сторону, достраиваем квадрат поворотом на 90°, собираем множества вершин."""
    uzly = {(x, y) for x in range(stolbcov) for y in range(strok)}
    najdeno = set()
    for (x1, y1) in uzly:
        for (x2, y2) in uzly:
            if (x1, y1) == (x2, y2):
                continue
            dx, dy = x2 - x1, y2 - y1
            p3 = (x2 - dy, y2 + dx)
            p4 = (x1 - dy, y1 + dx)
            if p3 in uzly and p4 in uzly:
                najdeno.add(frozenset([(x1, y1), (x2, y2), p3, p4]))
    return len(najdeno)


# 2. Сколько клеток пересекает диагональ прямоугольника
def kletki_pod_diagonalyu(shirina, vysota):
    """Клетка [i,i+1]x[j,j+1] считается, если отрезок (0,0)-(shirina,vysota)
    проходит через её ВНУТРЕННОСТЬ (касание угла не считается)."""
    k = Fraction(vysota, shirina)
    schet = 0
    for i in range(shirina):
        y_lo, y_hi = k * i, k * (i + 1)          # на x из [i, i+1] диагональ пробегает y из [y_lo, y_hi]
        for j in range(vysota):
            if max(y_lo, j) < min(y_hi, j + 1):  # пересечение открытых интервалов непусто
                schet += 1
    return schet


# 3. Треугольники на треугольной сетке
def treugolniki_v_treugolnike(n):
    """Большой треугольник со стороной n, разбитый на n*n маленьких.
    Узлы в косых координатах (a, b), a, b >= 0, a + b <= n. Три линии сетки:
    a = const, b = const, a + b = const. Перебираем все тройки узлов: треугольник
    со сторонами по линиям сетки = каждая пара узлов на общей линии, и тройка не на одной линии."""
    uzly = [(a, b) for a in range(n + 1) for b in range(n + 1 - a)]

    def napravlenie(p, q):
        if p[0] == q[0]:
            return 0
        if p[1] == q[1]:
            return 1
        if p[0] + p[1] == q[0] + q[1]:
            return 2
        return None

    schet = 0
    for p, q, r in combinations(uzly, 3):
        d = {napravlenie(p, q), napravlenie(q, r), napravlenie(p, r)}
        if None not in d and len(d) == 3:
            schet += 1
    return schet


# 4. Сумма по клеткам: «в скольких квадратах лежит клетка»
def summa_po_kletkam(stolbcov, strok):
    """В каждую клетку пишем, сколько квадратов (по линиям сетки, любого размера)
    её содержат; считаем честно по клеткам и складываем."""
    kvadraty = []
    for s in range(1, min(stolbcov, strok) + 1):
        for x in range(stolbcov - s + 1):
            for y in range(strok - s + 1):
                kvadraty.append((x, y, s))
    itogo = 0
    for cx in range(stolbcov):
        for cy in range(strok):
            chislo = sum(1 for (x, y, s) in kvadraty if x <= cx < x + s and y <= cy < y + s)
            itogo += chislo
    return itogo


def chislo_v_kletke(stolbcov, strok, cx, cy):
    schet = 0
    for s in range(1, min(stolbcov, strok) + 1):
        for x in range(stolbcov - s + 1):
            for y in range(strok - s + 1):
                if x <= cx < x + s and y <= cy < y + s:
                    schet += 1
    return schet


# 5. Электронные часы: палиндромы
def palindromy_na_chasah(chasov_v_sutkah, minut_v_chase=60):
    """Показания ЧЧ:ММ от 00:00 до последней минуты суток; палиндром = 4 цифры читаются одинаково."""
    schet = 0
    for h in range(chasov_v_sutkah):
        for m in range(minut_v_chase):
            s = f"{h:02d}{m:02d}"
            if s == s[::-1]:
                schet += 1
    return schet


# 6. Домино: сколько всего точек
def tochki_domino(maks):
    """Набор домино с числами от 0 до maks: все кости {a, b}, a <= b (каждая ровно один раз)."""
    return sum(a + b for a in range(maks + 1) for b in range(a, maks + 1))


def kosti_s_chislom(maks, k):
    """Сколько ПОЛОВИНОК в наборе несут число k (дубль даёт две)."""
    return sum((a == k) + (b == k) for a in range(maks + 1) for b in range(a, maks + 1))


# 7 (отложено). Совпадения стрелок
def sovpadeniya_strelok(nachalo_min, konec_min, ugol=0):
    """Считаем моменты t (минуты, в [nachalo, konec)), когда угол от часовой стрелки до минутной
    (по часовой стрелке) равен ugol. Минутная — 6 град/мин, часовая — 1/2 град/мин.
    Все такие моменты кратны 1/11 минуты, поэтому перебираем сетку с шагом 1/11 мин."""
    schet = 0
    for s in range(nachalo_min * 11, konec_min * 11):
        t = Fraction(s, 11)
        raznost = (6 * t - Fraction(1, 2) * t) % 360
        if raznost == ugol % 360:
            schet += 1
    return schet


if __name__ == "__main__":
    # 1. Квадраты в узлах
    assert kvadraty_v_uzlah(4, 4) == 20          # А
    assert kvadraty_v_uzlah(5, 4) == 30          # Б (5 точек в ряд, 4 ряда)
    assert kvadraty_v_uzlah(5, 5) == 50          # запас
    assert kvadraty_v_uzlah(3, 3) == 6           # разбор на уроке/проверка «по шагам»

    # 2. Диагональ
    assert kletki_pod_diagonalyu(60, 36) == 84   # А (12 кусков 5x3 по 7 клеток)
    assert kletki_pod_diagonalyu(48, 30) == 72   # Б (6 кусков 8x5 по 12 клеток)
    assert kletki_pod_diagonalyu(5, 3) == 7 and kletki_pod_diagonalyu(8, 5) == 12
    assert kletki_pod_diagonalyu(4, 2) == 4      # пример в условии (видно правило «уголок не считается»)
    assert kletki_pod_diagonalyu(20, 12) == 28   # запас
    assert kletki_pod_diagonalyu(10, 6) == 14    # маленький пример для разбора
    assert kletki_pod_diagonalyu(5, 3) == 7

    # 3. Треугольники
    assert treugolniki_v_treugolnike(3) == 13
    assert treugolniki_v_treugolnike(4) == 27    # А
    assert treugolniki_v_treugolnike(5) == 48    # Б

    # 4. Сумма чисел по клеткам
    assert summa_po_kletkam(3, 3) == 34
    assert summa_po_kletkam(4, 4) == 104         # А
    assert summa_po_kletkam(5, 3) == 74          # Б
    assert summa_po_kletkam(5, 5) == 259
    assert [chislo_v_kletke(4, 4, x, y) for (x, y) in [(0, 0), (1, 0), (1, 1)]] == [4, 6, 10]

    # 5. Палиндромы на часах
    assert palindromy_na_chasah(24) == 16        # А (Земля)
    assert palindromy_na_chasah(30) == 18        # Б (планета: 30 часов по 60 минут)
    assert palindromy_na_chasah(37) == 24        # запас

    # 6. Домино
    assert tochki_domino(6) == 168               # А
    assert tochki_domino(5) == 105               # Б
    assert tochki_domino(9) == 495               # запас: двойная девятка
    assert all(kosti_s_chislom(6, k) == 8 for k in range(7))
    assert all(kosti_s_chislom(5, k) == 7 for k in range(6))

    # 7. Стрелки
    assert sovpadeniya_strelok(0, 24 * 60) == 22               # совпадения за сутки [00:00, 24:00)
    assert sovpadeniya_strelok(0, 24 * 60, ugol=180) == 22     # противоположны
    assert sovpadeniya_strelok(0, 24 * 60, ugol=90) + sovpadeniya_strelok(0, 24 * 60, ugol=270) == 44
    assert sovpadeniya_strelok(6 * 60, 18 * 60 + 1) == 11       # с 6:00 до 18:00 включительно

    print("Все проверки пройдены.")
