# -*- coding: utf-8 -*-
"""ДЗ к 6.10 (после «Комбинаторики 2», 29.09). 6 задач (Р202: «самые важные, ключевые; чем меньше, тем лучше»; островки ушли в листок ○2в, треугольник со стороной 8 — в банк к теме «сумма 1 + … + n»): обе недели — «Комбинаторика 1» (отрезок чисел,
дополнение, включения-исключения, суммы цифр) и «Комбинаторика 2» (таблица, группы). Источники у каждой задачи.
Ни одна не повторяет листки 22.09 и 29.09, ДЗ 22.09 и контрольную 29.09. Ответы — перебором ниже.
Сборка: python3 dz_29-09_dannye.py → out/DZ-29-09.html/.pdf, out/DZ-29-09-otvety.txt"""
import os, sys, math
import pathlib as _pl
_H = _pl.Path(__file__).resolve().parent
sys.path.insert(0, str(next(p / 'mashina-listka' for p in _H.parents if (p / 'mashina-listka').is_dir())))
from listok_gen import shen, document, polulist, to_pdf, fit_report
HERE = os.path.dirname(os.path.abspath(__file__))

def ostrova():                                       # Шень, Листок 1, №10: прямоугольник 7×4, раздвинутый пустыми рядами
    cs = {0: 0, 2: 1, 3: 1, 4: 1, 5: 1, 7: 2, 8: 2}; rs = {0: 0, 2: 1, 3: 1, 5: 2}
    return shen(6, 9, lambda r, c: r in rs and c in cs, cell=5.6, pid='dzo')
def treugolnik(n=8, a=7.4):                          # РШ 1.7: треугольник со стороной 8, разбитый на единичные
    h = a * math.sqrt(3) / 2; W = n * a; H = n * h; s = []
    for i in range(n + 1):                               # линии трёх направлений
        y = i * h; x0 = (n - i) * a / 2; s.append(f'<line x1="{x0:.2f}" y1="{y:.2f}" x2="{x0 + i*a:.2f}" y2="{y:.2f}" class="s-out" style="stroke-width:.3"/>')
        s.append(f'<line x1="{i*a:.2f}" y1="{H:.2f}" x2="{i*a + (n-i)*a/2:.2f}" y2="{H-(n-i)*h:.2f}" class="s-out" style="stroke-width:.3"/>')
        s.append(f'<line x1="{i*a:.2f}" y1="{H:.2f}" x2="{i*a/2:.2f}" y2="{H - i*h:.2f}" class="s-out" style="stroke-width:.3"/>')
    s.append(f'<polygon points="{W/2:.2f},0 {W:.2f},{H:.2f} 0,{H:.2f}" class="s-out" style="stroke-width:.6"/>')
    return f'<svg viewBox="-1 -1 {W+2:.2f} {H+2:.2f}" style="width:{W+2:.2f}mm;height:{H+2:.2f}mm" role="img" aria-label="треугольник со стороной 8, разбитый на маленькие треугольники">{"".join(s)}</svg>'

# --- проверка ответов ---
from collections import Counter
PR = {2, 3, 5, 7, 11, 13, 17}; C = Counter(x // 10 + x % 10 for x in range(10, 100))
A_prost = sum(C[s] for s in PR)
A_110 = sum(1 for x in range(100, 1000) if (x // 100) % 2 != (x // 10 % 10) % 2 and sum(map(int, str(x))) % 10 == 0)
A_915 = sum(1 for x in range(100, 1000) if x % 9 == 0 or x % 15 == 0)
assert (A_prost, A_110, A_915) == (33, 45, 140)
assert (1 + 4 + 2) * (1 + 2 + 1) == 28 and sum(2 * k - 1 for k in range(1, 9)) == 64 and 101 - 22 - 29 == 50 and (16 * 14 + 16) * 50 == 12000

Z = [
 dict(num=1, src='Шень, Листок 1, №6', text='Человек поднимается с первого этажа на пятый за минуту. Сколько ему понадобится времени, чтобы с той же скоростью подняться с первого на десятый этаж?',
      block=[''], key='9 пролётов · 15 с = 2 мин 15 с (частая ошибка: 2 мин)'),
 dict(num=2, src='Раскина–Шаповалов, вып. 20, 1.8', text='В деревне Простоквашино 16 мальчиков и 14 девочек. На 1 сентября каждый мальчик подарил по цветку каждой девочке и ещё один цветок Марье Ивановне, а потом девочки тоже подарили все полученные цветы Марье Ивановне. Сколько килограммов цветов принесла своей козе Марья Ивановна, если каждый цветок весил 50 г?',
      block=[''], key='(16·14 + 16)·50 г = 12 000 г = 12 кг'),
 dict(num=3, src='Раскина–Шаповалов, вып. 20, Д36', text='Из 101 далматинца у 29 пятно только на левом ухе, у 17 — только на правом ухе, а у 22 далматинцев нет пятен на ушах. Сколько далматинцев имеют пятно на правом ухе?',
      block=[''], key='101 − 22 − 29 = 50'),
 dict(num=4, src='Раскина–Шаповалов, вып. 20, Д2', text='У скольких двузначных чисел сумма цифр — простое число?',
      block=[''], key='2 + 3 + 5 + 7 + 8 + 6 + 2 = 33 (суммы 2, 3, 5, 7, 11, 13, 17)'),
 dict(num=5, src='179 школа, 8 кл., листок 2 «Правила суммы и произведения», №4', text='Сколько существует трёхзначных чисел, делящихся хотя бы на одно из чисел 9 и 15?',
      block=[''], key='100 + 60 − 20 = 140 (на 9 и на 15 сразу — это кратные 45; частая ошибка — вычесть кратные 135)'),
 dict(num=6, src='Раскина–Шаповалов, вып. 20, 1.10', text='Сколько всего трёхзначных чисел, у которых первая и вторая цифры разной чётности, а сумма цифр делится на 10?',
      block=[''], key='9·5 = 45: первые две цифры — таблица 9 × 5, третья по ним определяется однозначно'),
]
META = dict(title='Домашнее задание', date='Комбинаторика 2 · к 6 октября', klass='7И')
X = '''.hd span{font-size:10pt}.page{--abw:50mm}body{font-size:11.4pt;line-height:1.3}.z{margin-bottom:3.4mm}.ab.one .r{height:12mm}.ab{margin-bottom:2.4mm}
.foot{font-weight:400;font-size:9.4pt;color:#6b6a64;border-top:1px solid #8a877d}'''
NOTE = 'В начале следующего занятия — короткая контрольная на эти же приёмы. Ответ записывайте выражением — так, как вы считали.'
def build():
    """Пол-листа на человека (Р209): два одинаковых экземпляра на A4, режется пополам."""
    items = [{k: v for k, v in z.items() if k not in ('src', 'key')} for z in Z]
    P = dict(heading='', items=items, footer=NOTE)
    h = polulist(META, [('', P), ('', P)], X)
    return h.replace(' · вариант </span>', '</span>').replace('<div class="sec"></div>', '<div style="height:2mm"></div>')
if __name__ == '__main__':
    p = f'{HERE}/out/DZ-29-09.html'; open(p, 'w').write(build()); to_pdf([p]); print('перелив, мм:', fit_report(p))
    key = '\n'.join(f'{z["num"]}. {z["key"]}   [{z["src"]}]' for z in Z)
    open(f'{HERE}/out/DZ-29-09-otvety.txt', 'w').write('ДЗ к 6.10 — ответы (перебор в dz_29-09_dannye.py)\n' + key + '\n'); print(key)
