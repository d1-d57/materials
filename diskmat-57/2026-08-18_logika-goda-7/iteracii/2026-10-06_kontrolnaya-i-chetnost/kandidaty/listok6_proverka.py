# -*- coding: utf-8 -*-
"""Проверка кандидатов на последнюю задачу листка 6 (умный перебор, 7 класс).
Всё считается прямым перебором, без формул. Запуск: python3 listok6_proverka.py
"""
from fractions import Fraction

# ---------- 1. Белый и чёрный король ----------
def koroli(n):
    """Упорядоченные пары (белый, чёрный) на разных клетках n×n, короли не соседствуют."""
    kl = [(r, c) for r in range(n) for c in range(n)]
    cnt = 0
    for (r1, c1) in kl:
        for (r2, c2) in kl:
            if (r1, c1) == (r2, c2):
                continue
            if max(abs(r1 - r2), abs(c1 - c2)) == 1:  # бьют друг друга
                continue
            cnt += 1
    return cnt

def koroli_po_klassam(n):
    """Раскладка ответа по месту белого короля: угол / край / середина."""
    d = {}
    for r in range(n):
        for c in range(n):
            na_krayu = (r in (0, n - 1)) + (c in (0, n - 1))
            klass = {2: 'угол', 1: 'край', 0: 'середина'}[na_krayu]
            svobodno = 0
            for r2 in range(n):
                for c2 in range(n):
                    if (r2, c2) != (r, c) and max(abs(r - r2), abs(c - c2)) != 1:
                        svobodno += 1
            d.setdefault(klass, []).append(svobodno)
    return {k: (len(v), set(v)) for k, v in d.items()}

assert koroli(8) == 3612
assert koroli(7) == 2040
assert koroli(6) == 1040
assert koroli_po_klassam(8) == {'угол': (4, {60}), 'край': (24, {58}), 'середина': (36, {55})}
assert 4 * 60 + 24 * 58 + 36 * 55 == 3612
assert koroli_po_klassam(7) == {'угол': (4, {45}), 'край': (20, {43}), 'середина': (25, {40})}
assert 4 * 45 + 20 * 43 + 25 * 40 == 2040

# ---------- 2. Смены цифр на табло ----------
def tablo_24():
    """ЧЧ:ММ, 00:00 ... 23:59 -> 00:00. Сумма по всем 1440 переходам числа сменившихся цифр."""
    pok = ['%02d%02d' % (h, m) for h in range(24) for m in range(60)]
    total = 0
    po_razryadam = [0, 0, 0, 0]
    for i in range(len(pok)):
        a, b = pok[i], pok[(i + 1) % len(pok)]
        for j in range(4):
            if a[j] != b[j]:
                total += 1
                po_razryadam[j] += 1
    return total, po_razryadam

def tablo_12():
    """ЧЧ:ММ, 12-часовые: 01:00 ... 12:59 -> 01:00 (за 12 часов)."""
    hours = list(range(1, 13))
    pok = ['%02d%02d' % (h, m) for h in hours for m in range(60)]
    total = 0
    po_razryadam = [0, 0, 0, 0]
    for i in range(len(pok)):
        a, b = pok[i], pok[(i + 1) % len(pok)]
        for j in range(4):
            if a[j] != b[j]:
                total += 1
                po_razryadam[j] += 1
    return total, po_razryadam

assert tablo_24() == (1611, [3, 24, 144, 1440])
assert tablo_12() == (806, [2, 12, 72, 720])

# ---------- 3. Квадраты с вершинами в узлах решётки ----------
def kvadraty(n):
    """Число квадратов (любого наклона) с вершинами в точках n×n."""
    pts = [(x, y) for x in range(n) for y in range(n)]
    S = set(pts)
    found = set()
    for (x1, y1) in pts:
        for (x2, y2) in pts:
            if (x1, y1) == (x2, y2):
                continue
            dx, dy = x2 - x1, y2 - y1
            x3, y3 = x2 - dy, y2 + dx
            x4, y4 = x1 - dy, y1 + dx
            if (x3, y3) in S and (x4, y4) in S:
                found.add(frozenset([(x1, y1), (x2, y2), (x3, y3), (x4, y4)]))
    return len(found)

def kvadraty_po_ramke(n):
    """Раскладка по размеру описанной рамки k: сколько квадратов с рамкой k×k."""
    pts = [(x, y) for x in range(n) for y in range(n)]
    S = set(pts)
    found = set()
    for (x1, y1) in pts:
        for (x2, y2) in pts:
            if (x1, y1) == (x2, y2):
                continue
            dx, dy = x2 - x1, y2 - y1
            q = [(x1, y1), (x2, y2), (x2 - dy, y2 + dx), (x1 - dy, y1 + dx)]
            if all(p in S for p in q):
                found.add(frozenset(q))
    d = {}
    for q in found:
        k = max(p[0] for p in q) - min(p[0] for p in q)
        d[k] = d.get(k, 0) + 1
    return d

assert kvadraty(4) == 20
assert kvadraty(5) == 50
assert kvadraty_po_ramke(4) == {1: 9, 2: 8, 3: 3}
assert kvadraty_po_ramke(5) == {1: 16, 2: 18, 3: 12, 4: 4}

# ---------- 4. Палиндромы на часах ----------
def palindromy_24():
    cnt = 0
    for h in range(24):
        for m in range(60):
            s = '%02d%02d' % (h, m)
            if s == s[::-1]:
                cnt += 1
    return cnt

def palindromy_12():
    """Часы без ведущего нуля: 1:00 ... 12:59 (за 12 часов), читаем цифры подряд."""
    cnt = 0
    for h in range(1, 13):
        for m in range(60):
            s = '%d%02d' % (h, m)
            if s == s[::-1]:
                cnt += 1
    return cnt

assert palindromy_24() == 16
assert palindromy_12() == 57

# ---------- 5. Точки на костях домино ----------
def domino(n):
    """Сумма всех точек на всех костях от 0-0 до n-n."""
    total = 0
    for a in range(n + 1):
        for b in range(a, n + 1):
            total += a + b
    return total

def domino_vhozhdeniya(n):
    """Сколько раз каждое число встречается на половинках."""
    d = {}
    for a in range(n + 1):
        for b in range(a, n + 1):
            d[a] = d.get(a, 0) + 1
            d[b] = d.get(b, 0) + 1
    return d

assert domino(6) == 168
assert domino(5) == 105
assert set(domino_vhozhdeniya(6).values()) == {8}
assert set(domino_vhozhdeniya(5).values()) == {7}

# ---------- 6. Стрелки часов ----------
def strelki(ugol):
    """Сколько раз за сутки [0:00, 24:00) угол между стрелками равен ugol (0 или 180).
    Время t в минутах; положение минутной 6t, часовой t/2 градусов.
    Проверяем ВСЕ моменты вида t = k/11 минуты (только в такие моменты угол
    между стрелками может быть кратен 180, потому что 11t/2 должно быть целым*180;
    но для честности перебираем сетку 1/11 и сверяем точно дробями)."""
    cnt = 0
    for k in range(24 * 60 * 11):
        t = Fraction(k, 11)
        raz = (6 * t - t / 2) % 360
        if raz == ugol:
            cnt += 1
    return cnt

def strelki_proverka_setki():
    """Контроль: на более мелкой сетке (1/110 мин) за 12 часов находим те же моменты."""
    cnt = 0
    for k in range(12 * 60 * 110):
        t = Fraction(k, 110)
        if (6 * t - t / 2) % 360 == 0:
            cnt += 1
    return cnt

assert strelki(0) == 22
assert strelki(180) == 22
assert strelki_proverka_setki() == 11

# ---------- 7. Треугольники с целыми сторонами ----------
def treugolniki(P):
    cnt = 0
    for a in range(1, P):
        for b in range(a, P):
            c = P - a - b
            if c < b:
                continue
            if a + b > c:
                cnt += 1
    return cnt

assert treugolniki(15) == 7
assert treugolniki(17) == 8
assert treugolniki(13) == 5
assert treugolniki(16) == 5  # ловушка: при чётном периметре меньше

# ---------- запасной: пятницы 13-е ----------
def pyatnicy13(visokosny):
    dni = [31, 29 if visokosny else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    best, worst = 0, 99
    for start in range(7):  # день недели 1 января
        d = start
        cnt = 0
        for m in range(12):
            if (d + 12) % 7 == 4:  # 13-е число; 4 = пятница при 0 = понедельник
                cnt += 1
            d = (d + dni[m]) % 7
        best, worst = max(best, cnt), min(worst, cnt)
    return best, worst

assert pyatnicy13(False) == (3, 1)
assert pyatnicy13(True) == (3, 1)

# ---------- запасной: минуты с пятёркой ----------
def pyaterki():
    return sum('5' in '%02d%02d' % (h, m) for h in range(24) for m in range(60))

assert pyaterki() == 450

if __name__ == '__main__':
    print('короли 8x8:', koroli(8), ' 7x7:', koroli(7), ' 6x6:', koroli(6))
    print('табло 24ч:', tablo_24(), ' 12ч:', tablo_12())
    print('квадраты 4x4 точки:', kvadraty(4), kvadraty_po_ramke(4), ' 5x5:', kvadraty(5), kvadraty_po_ramke(5))
    print('палиндромы 24ч:', palindromy_24(), ' 12ч H:MM:', palindromy_12())
    print('домино 0-6:', domino(6), ' 0-5:', domino(5))
    print('стрелки совпадают:', strelki(0), ' противоположны:', strelki(180))
    print('треугольники P=15,17,13,16:', treugolniki(15), treugolniki(17), treugolniki(13), treugolniki(16))
    print('пятницы 13 (max, min) обычный/високосный:', pyatnicy13(False), pyatnicy13(True))
    print('минут с пятёркой:', pyaterki())
    print('ВСЕ assert ПРОШЛИ')
