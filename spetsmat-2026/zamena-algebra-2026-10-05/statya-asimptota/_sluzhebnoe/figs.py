"""Генератор статичных SVG для ленты «График без таблицы». Классы — словарь s-* движка."""
import math, json

class P:
    def __init__(s, x0, y0, w, h, xr, yr):
        s.x0, s.y0, s.w, s.h, s.xr, s.yr = x0, y0, w, h, xr, yr
    def X(s, x): return s.x0 + (x - s.xr[0]) / (s.xr[1] - s.xr[0]) * s.w
    def Y(s, y): return s.y0 + s.h - (y - s.yr[0]) / (s.yr[1] - s.yr[0]) * s.h
    def axes(s, lx='x', ly='y'):
        o = []
        if s.yr[0] < 0 < s.yr[1]:
            o.append(f'<line class="s-thin" x1="{s.x0:.1f}" y1="{s.Y(0):.1f}" x2="{s.x0+s.w:.1f}" y2="{s.Y(0):.1f}"/>')
            o.append(f'<text class="s-txt-m" x="{s.x0+s.w-10:.1f}" y="{s.Y(0)+15:.1f}">{lx}</text>')
        if s.xr[0] < 0 < s.xr[1]:
            o.append(f'<line class="s-thin" x1="{s.X(0):.1f}" y1="{s.y0:.1f}" x2="{s.X(0):.1f}" y2="{s.y0+s.h:.1f}"/>')
            o.append(f'<text class="s-txt-m" x="{s.X(0)+6:.1f}" y="{s.y0+12:.1f}">{ly}</text>')
        return o
    def curve(s, f, a, b, cls='s-line', n=500):
        """Ломаная по графику на [a,b]; рвётся, где значение уходит за рамку."""
        out, cur = [], []
        lo, hi = s.yr[0] - (s.yr[1]-s.yr[0]) * .02, s.yr[1] + (s.yr[1]-s.yr[0]) * .02
        for i in range(n + 1):
            x = a + (b - a) * i / n
            try: y = f(x)
            except ZeroDivisionError: y = None
            if y is None or not (lo <= y <= hi):
                if len(cur) > 1: out.append(cur)
                cur = []
                continue
            cur.append((s.X(x), s.Y(y)))
        if len(cur) > 1: out.append(cur)
        return [f'<polyline class="{cls}" points="' + ' '.join(f'{px:.1f},{py:.1f}' for px, py in c) + '"/>' for c in out]
    def hline(s, y, cls='s-dash'):
        return f'<line class="{cls}" x1="{s.x0:.1f}" y1="{s.Y(y):.1f}" x2="{s.x0+s.w:.1f}" y2="{s.Y(y):.1f}"/>'
    def vline(s, x, cls='s-dash'):
        return f'<line class="{cls}" x1="{s.X(x):.1f}" y1="{s.y0:.1f}" x2="{s.X(x):.1f}" y2="{s.y0+s.h:.1f}"/>'
    def txt(s, x, y, t, cls='s-txt', dx=0, dy=0, anchor='start'):
        return f'<text class="{cls}" x="{s.X(x)+dx:.1f}" y="{s.Y(y)+dy:.1f}" text-anchor="{anchor}">{t}</text>'
    def dot(s, x, y, cls='s-node'):
        return f'<circle class="{cls}" cx="{s.X(x):.1f}" cy="{s.Y(y):.1f}" r="3.5"/>'

def svg(w, h, label, body):
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}">' + ''.join(body) + '</svg>'

def safe(g):
    def f(x):
        try: return g(x)
        except (ZeroDivisionError, ValueError): return None
    return f

figs = {}

# Ф1. Полоса: ограниченная и неограниченная
L = P(20, 30, 290, 200, (-6, 6), (-7, 7)); R = P(350, 30, 290, 200, (-6, 6), (-7, 7))
b = []
for p in (L, R):
    b.append(f'<rect class="s-fillsh" x="{p.x0}" y="{p.Y(2):.1f}" width="{p.w}" height="{p.Y(-2)-p.Y(2):.1f}"/>')
    b += p.axes()
    b.append(p.hline(2, 's-thin-a')); b.append(p.hline(-2, 's-thin-a'))
b += L.curve(safe(lambda x: 4*x/(1+x*x)), -6, 6, 's-accent')
b.append(L.txt(-6, 2, 'y = 2', 's-txt-a', dx=4, dy=-5)); b.append(L.txt(-6, -2, 'y = −2', 's-txt-a', dx=4, dy=15))
b += R.curve(safe(lambda x: x + 4/x), -6, 6, 's-accent')
b.append(R.txt(-6, 2, 'y = 2', 's-txt-a', dx=4, dy=-5))
b.append(L.txt(0, 7, 'y = 4x/(1+x²): внутри полосы', 's-txt', anchor='middle', dy=-14)); b.append(R.txt(0, 7, 'y = x + 4/x: вылезает', 's-txt', anchor='middle', dy=-14))
figs['polosa'] = svg(660, 245, 'Слева график 4x делённое на 1 плюс x квадрат целиком лежит в полосе между y равно минус 2 и 2; справа график x плюс 4 делённое на x выходит из полосы', b)

# Ф2. Асимптоту можно пересекать бесконечно много раз
p = P(20, 15, 620, 170, (-26, 26), (-0.35, 1.1))
b = p.axes()
b.append(p.hline(0, 's-dash'))
b += p.curve(safe(lambda x: math.sin(x)/x if x != 0 else 1.0), -26, 26, 's-accent', n=1200)
b.append(f'<circle class="s-node" cx="{p.X(0):.1f}" cy="{p.Y(1):.1f}" r="3.5"/>')
b.append(p.txt(26, 0, 'асимптота y = 0', 's-txt-a', dx=-4, dy=-8, anchor='end'))
b.append(p.txt(0, 1, 'y = sin x / x', 's-txt', dx=30, dy=12))
figs['volna'] = svg(660, 195, 'Затухающая волна sin x делённое на x пересекает прямую y равно 0 бесконечно много раз и всё ближе к ней прижимается', b)

# Ф3. Дробно-линейная: сдвинутая гипербола
p = P(30, 15, 600, 300, (-8, 12), (-8, 12))
b = p.axes()
b.append(p.vline(2)); b.append(p.hline(2))
b += p.curve(safe(lambda x: 2 + 7/(x-2)), -8, 12, 's-accent', n=900)
b.append(p.dot(2, 2)); b.append(p.txt(2, 2, '(2; 2)', 's-txt', dx=7, dy=16))
b.append(p.dot(-1.5, 0)); b.append(p.txt(-1.5, 0, '−1,5', 's-txt', dx=-6, dy=16, anchor='end'))
b.append(p.txt(2, 12, 'x = 2', 's-txt-a', dx=6, dy=14)); b.append(p.txt(-8, 2, 'y = 2', 's-txt-a', dx=4, dy=-6))
b.append(p.txt(6, 2 + 7/4, 'y = (2x+3)/(x−2)', 's-txt', dx=10, dy=-14))
figs['giperbola'] = svg(660, 330, 'График 2x плюс 3 делённое на x минус 2: гипербола с асимптотами x равно 2 и y равно 2, центр симметрии в точке 2;2, пересекает ось x в точке минус 1,5', b)

# Ф4. Два модуля
L = P(20, 25, 290, 210, (-7, 7), (-3, 5)); R = P(350, 25, 290, 210, (-5, 3), (-3, 5))
b = L.axes() + R.axes()
b += L.curve(safe(lambda x: 4/(x+2)), -7, 7, 's-dash', n=700)
b += L.curve(safe(lambda x: 4/(abs(x)+2)), -7, 7, 's-accent')
b.append(L.txt(0, 5, 'модуль на x: зеркало — ось y', 's-txt', anchor='middle', dy=-12))
b.append(L.txt(3.5, 4/5.5, 'y = 4/(|x|+2)', 's-txt-a', dy=-10))
b.append(L.txt(-7, -3, 'пунктир: y = 4/(x+2)', 's-txt-m', dx=4, dy=-6))
b += R.curve(safe(lambda x: 2 + 1/(x+2)), -5, 3, 's-dash', n=900)
b += R.curve(safe(lambda x: abs(2 + 1/(x+2))), -5, 3, 's-accent', n=900)
b.append(R.dot(-2.5, 0)); b.append(R.txt(-2.5, 0, '−2,5', 's-txt', dx=-6, dy=16, anchor='end'))
b.append(R.vline(-2, 's-thin'))
b.append(R.txt(0, 5, 'модуль на y: зеркало — ось x', 's-txt', anchor='middle', dy=-12))
b.append(R.txt(-5, -3, 'пунктир: y = 2 + 1/(x+2)', 's-txt-m', dx=4, dy=-6))
figs['moduli'] = svg(660, 245, 'Слева график 4 делённое на модуль x плюс 2: правая половина графика 4 делённое на x плюс 2 отражена относительно оси y. Справа модуль от 2 плюс 1 делённое на x плюс 2: часть под осью x отражена вверх', b)

json.dump(figs, open('figs.json', 'w'), ensure_ascii=False)
print({k: len(v) for k, v in figs.items()})

# === статья «Асимптота» ===
# Ф5. Ложная вертикаль: ломаная по точкам с шагом 1 через особую точку
p = P(30, 15, 600, 300, (-6, 10), (-14, 18))
b = p.axes()
b += p.curve(safe(lambda x: 2 + 7/(x-2)), -6, 10, 's-thin', n=1200)
xs = [-5.5 + i for i in range(16)]
pts = [(x, 2 + 7/(x-2)) for x in xs]
b.append('<polyline class="s-accent" points="' + ' '.join(f'{p.X(x):.1f},{p.Y(y):.1f}' for x, y in pts) + '"/>')
for x, y in pts: b.append(p.dot(x, y))
b.append(p.txt(2, 0, 'ложный отрезок', 's-txt-a', dx=14, dy=-30))
b.append(p.txt(10, 2, 'шаг 1', 's-txt-m', dx=-4, dy=-28, anchor='end'))
figs['lozh'] = svg(660, 330, 'Точки графика 2x плюс 3 делённое на x минус 2, взятые с шагом 1 и соединённые отрезками: между x равно 1,5 и x равно 2,5 появляется почти вертикальный отрезок, которого у графика нет', b)

# Ф6. Подслеповатый наблюдатель: обе полосы гиперболы y=1/x и зеркало y=x
p = P(30, 15, 400, 400, (-0.5, 6), (-0.5, 6))
h = 0.4; N = 1/h
b = p.axes()
b.append(f'<rect class="s-fillsh" x="{p.X(N):.1f}" y="{p.Y(h):.1f}" width="{p.X(6)-p.X(N):.1f}" height="{p.Y(-h)-p.Y(h):.1f}"/>')
b.append(f'<rect class="s-fillsh" x="{p.X(-h):.1f}" y="{p.Y(6):.1f}" width="{p.X(h)-p.X(-h):.1f}" height="{p.Y(N)-p.Y(6):.1f}"/>')
b.append(f'<line class="s-dash" x1="{p.X(-0.5):.1f}" y1="{p.Y(-0.5):.1f}" x2="{p.X(6):.1f}" y2="{p.Y(6):.1f}"/>')
b += p.curve(safe(lambda x: 1/x), 0.05, 6, 's-accent', n=900)
b.append(f'<line class="s-thin" x1="{p.X(N):.1f}" y1="{p.Y(0)-5:.1f}" x2="{p.X(N):.1f}" y2="{p.Y(0)+5:.1f}"/>'); b.append(f'<line class="s-thin" x1="{p.X(0)-5:.1f}" y1="{p.Y(N):.1f}" x2="{p.X(0)+5:.1f}" y2="{p.Y(N):.1f}"/>')
b.append(p.txt(N, 0, 'N = 1/h', 's-txt', dx=-4, dy=18, anchor='middle'))
b.append(p.txt(0, N, 'N', 's-txt', dx=-10, dy=4, anchor='end'))
b.append(p.txt(6, h, 'полоса |y| &lt; h', 's-txt-a', dx=-4, dy=-8, anchor='end'))
b.append(p.txt(h, 6, 'полоса |x| &lt; h', 's-txt-a', dx=6, dy=14))
b.append(p.txt(5.2, 5.2, 'y = x', 's-txt-m', dx=6, dy=14))
figs['polosy'] = svg(460, 430, 'Правая ветвь гиперболы y равно 1 делённое на x: при x больше N она лежит в горизонтальной полосе толщины h вокруг оси x, при y больше N в вертикальной полосе вокруг оси y; полосы симметричны относительно прямой y равно x', b)

json.dump(figs, open('figs.json', 'w'), ensure_ascii=False)
print('ok', list(figs))

# === статья v2 ===
# Ф7. Средний балл: точки (n; 5-2/(n+1)) и полоса точности
p = P(40, 15, 600, 260, (-1, 41), (2.8, 5.25))
b = []
b.append(f'<line class="s-thin" x1="{p.X(0):.1f}" y1="{p.Y(3):.1f}" x2="{p.X(41):.1f}" y2="{p.Y(3):.1f}"/>')
b.append(f'<line class="s-thin" x1="{p.X(0):.1f}" y1="{p.Y(2.8):.1f}" x2="{p.X(0):.1f}" y2="{p.Y(5.25):.1f}"/>')
h = 0.1
b.append(f'<rect class="s-fillsh" x="{p.X(0):.1f}" y="{p.Y(5+h):.1f}" width="{p.X(41)-p.X(0):.1f}" height="{p.Y(5-h)-p.Y(5+h):.1f}"/>')
b.append(p.hline(5))
for n in range(0, 41):
    b.append(p.dot(n, 5 - 2/(n+1)))
for yv in (3, 4, 5):
    b.append(p.txt(0, yv, str(yv), 's-txt-m', dx=-8, dy=4, anchor='end'))
b.append(p.txt(41, 5, 'y = 5', 's-txt-a', dx=-4, dy=-10, anchor='end'))
b.append(p.vline(19, 's-thin'))
b.append(p.txt(19, 2.8, 'n = 19', 's-txt', dx=4, dy=-6))
b.append(p.txt(41, 3, 'число пятёрок n', 's-txt-m', dx=-4, dy=-6, anchor='end'))
b.append(p.txt(25, 4.9, 'полоса 4,9 … 5,1', 's-txt-a', dy=-14))
figs['ball'] = svg(660, 290, 'Средний балл после одной тройки и n пятёрок: точки поднимаются к прямой y равно 5, начиная с n равно 19 они лежат в полосе от 4,9 до 5,1', b)

# Ф8. Средняя скорость: 60v/(30+v) ограничена числом 60
p = P(40, 15, 600, 240, (0, 400), (0, 70))
b = []
b.append(f'<line class="s-thin" x1="{p.X(0):.1f}" y1="{p.Y(0):.1f}" x2="{p.X(400):.1f}" y2="{p.Y(0):.1f}"/>')
b.append(f'<line class="s-thin" x1="{p.X(0):.1f}" y1="{p.Y(0):.1f}" x2="{p.X(0):.1f}" y2="{p.Y(70):.1f}"/>')
b.append(p.hline(60))
b += p.curve(safe(lambda v: 60*v/(30+v)), 0.5, 400, 's-accent')
for yv in (30, 60):
    b.append(p.txt(0, yv, str(yv), 's-txt-m', dx=-8, dy=4, anchor='end'))
b.append(p.dot(30, 30)); b.append(p.txt(30, 30, 'v = 30: средняя 30', 's-txt', dx=8, dy=14))
b.append(p.dot(150, 50)); b.append(p.txt(150, 50, 'v = 150: средняя 50', 's-txt', dx=8, dy=16))
b.append(p.txt(400, 60, 'y = 60', 's-txt-a', dx=-4, dy=-8, anchor='end'))
b.append(p.txt(400, 0, 'скорость обратно v, км/ч', 's-txt-m', dx=-4, dy=-6, anchor='end'))
figs['skorost'] = svg(660, 270, 'Средняя скорость поездки туда со скоростью 30 и обратно со скоростью v: кривая растёт, приближаясь к прямой y равно 60, и никогда её не достигает', b)

json.dump(figs, open('figs.json', 'w'), ensure_ascii=False)
print('ok', list(figs))

# === v3: панели для доски ===
def panel(x0, y0, w, h, xr, yr, fns, asym=(), title='', marks=(), holes=(), n=700):
    p = P(x0, y0 + 18, w, h - 18, xr, yr)
    b = p.axes('', '')
    for kind, val in asym:
        if kind == 'h': b.append(p.hline(val))
        elif kind == 'v': b.append(p.vline(val))
        elif kind == 'o':
            k, c, a1, a2 = val
            pts = []
            for i in range(201):
                x = a1 + (a2 - a1) * i / 200; y = k * x + c
                if yr[0] <= y <= yr[1]: pts.append((p.X(x), p.Y(y)))
            if len(pts) > 1:
                b.append(f'<line class="s-dash" x1="{pts[0][0]:.1f}" y1="{pts[0][1]:.1f}" x2="{pts[-1][0]:.1f}" y2="{pts[-1][1]:.1f}"/>')
        elif kind == 'hb': b.append(p.hline(val, 's-thin-a'))
    for f, a, bb in fns:
        b += p.curve(safe(f), a, bb, 's-accent', n=n)
    for x, y in holes:
        b.append(f'<circle class="s-node" cx="{p.X(x):.1f}" cy="{p.Y(y):.1f}" r="3.5"/>')
    for x, y, t in marks:
        b.append(p.txt(x, y, t, 's-txt-m', dx=4, dy=-4))
    b.append(f'<text class="s-txt" x="{x0 + w/2:.1f}" y="{y0 + 12:.1f}" text-anchor="middle">{title}</text>')
    return b

def grid(cells, cols, cw, ch, label):
    b = []
    for i, c in enumerate(cells):
        r, k = divmod(i, cols)
        b += panel(10 + k * (cw + 10), 5 + r * (ch + 10), cw, ch, *c)
    rows = (len(cells) + cols - 1) // cols
    return svg(10 + cols * (cw + 10), 10 + rows * (ch + 10), label, b)

import math as _m
# Ф9. Цепочка 1/x → 7/x → 7/(x−2) → 2+7/(x−2)
cells = [
 ((-8, 10), (-8, 10), [(lambda x: 1/x, -8, 10)], [('h', 0), ('v', 0)], 'y = 1/x'),
 ((-8, 10), (-8, 10), [(lambda x: 7/x, -8, 10)], [('h', 0), ('v', 0)], 'растянуть: y = 7/x'),
 ((-8, 10), (-8, 10), [(lambda x: 7/(x-2), -8, 10)], [('h', 0), ('v', 2)], 'вправо на 2: y = 7/(x−2)'),
 ((-8, 10), (-8, 10), [(lambda x: 2+7/(x-2), -8, 10)], [('h', 2), ('v', 2)], 'вверх на 2: y = 2 + 7/(x−2)'),
]
figs['cepochka'] = grid(cells, 2, 315, 230, 'Четыре шага построения: гипербола 1 делённое на x, растяжение в 7 раз, сдвиг вправо на 2, сдвиг вверх на 2; асимптоты сдвигаются вместе с графиком')

# Ф10. Шесть функций из задачи о множестве значений
cells = [
 ((-7, 7), (-3, 3), [(lambda x: 4*x/(1+x*x), -7, 7)], [('h', 0), ('hb', 2), ('hb', -2)], 'А) 4x/(1+x²)'),
 ((-9, 9), (-14, 14), [(lambda x: x+4/x, -9, 9)], [('v', 0), ('o', (1, 0, -9, 9)), ('hb', 4), ('hb', -4)], 'Б) x + 4/x'),
 ((-4.5, 4.5), (-1, 4), [(lambda x: _m.sqrt(9-x*x), -3, 3)], [('hb', 3)], 'В) √(9 − x²)'),
 ((-1, 16), (-4, 2), [(lambda x: 1-_m.sqrt(x), 0, 16)], [('hb', 1)], 'Г) 1 − √x'),
 ((-4, 6), (-1, 10), [(lambda x: abs(x)+abs(x-2), -4, 6)], [('hb', 2)], 'Д) |x| + |x − 2|'),
 ((-16, 16), (-28, 36), [(lambda x: (x+3)**2/x, -16, 16)], [('v', 0), ('o', (1, 6, -16, 16)), ('hb', 12)], 'Е) (x + 3)²/x'),
]
figs['zn6'] = grid(cells, 3, 205, 175, 'Шесть графиков: 4x делённое на 1 плюс x квадрат в полосе от минус 2 до 2; x плюс 4 делённое на x с асимптотами x равно 0 и y равно x; полуокружность; 1 минус корень из x; сумма модулей; квадрат x плюс 3 делённый на x с асимптотами x равно 0 и y равно x плюс 6')

# Ф11. Шесть функций с модулями
cells = [
 ((-7, 5), (-1, 6), [(lambda x: 4/abs(x+2), -7, 5)], [('h', 0), ('v', -2)], '1) 4/|x + 2|'),
 ((-7, 7), (-1, 3), [(lambda x: 4/(abs(x)+2), -7, 7)], [('h', 0)], '2) 4/(|x| + 2)'),
 ((-7, 7), (-0.5, 3.5), [(lambda x: 2+1/(abs(x)+2), -7, 7)], [('h', 2)], '3) (2|x| + 5)/(|x| + 2)'),
 ((-7, 4), (-1, 6), [(lambda x: abs(2+1/(x+2)), -7, 4)], [('h', 2), ('v', -2)], '4) |(2x + 5)/(x + 2)|'),
 ((-8, 10), (-8, 10), [(lambda x: (abs(x)+4)/(x-2), -8, 10)], [('v', 2), ('h', 1), ('h', -1)], '5) (|x| + 4)/(x − 2)'),
 ((-6, 6), (-1, 8), [(lambda x: abs(2+3/(abs(x)-1)), -6, 6)], [('h', 2), ('v', 1), ('v', -1)], '6) |(2|x| + 1)/(|x| − 1)|'),
]
figs['mod6'] = grid(cells, 3, 205, 175, 'Шесть графиков с модулями и их асимптоты; ограничены только второй и третий')

# Ф12. Наклонные асимптоты
cells = [
 ((-5, 5), (-5, 5), [(lambda x: x**3/(x*x+1), -5, 5)], [('o', (1, 0, -5, 5))], 'x³/(x² + 1) → асимптота y = x'),
 ((-12, 10), (-25, 15), [(lambda x: (x*x-2*x+3)/(x+2), -12, 10)], [('v', -2), ('o', (1, -4, -12, 10))], '(x² − 2x + 3)/(x + 2) → y = x − 4'),
]
figs['naklon'] = grid(cells, 2, 315, 240, 'Наклонные асимптоты: x в кубе делённое на x квадрат плюс 1 прижимается к прямой y равно x; второй график имеет асимптоты x равно минус 2 и y равно x минус 4')

json.dump(figs, open('figs.json', 'w'), ensure_ascii=False)
print('ok', list(figs))

# Ф13. Линза: ход лучей и график b(a)
p = P(10, 10, 420, 220, (-22, 36), (-10, 6))
b = [f'<line class="s-thin" x1="{p.X(-22):.1f}" y1="{p.Y(0):.1f}" x2="{p.X(36):.1f}" y2="{p.Y(0):.1f}"/>']
b.append(f'<line class="s-line" x1="{p.X(0):.1f}" y1="{p.Y(5.5):.1f}" x2="{p.X(0):.1f}" y2="{p.Y(-9.5):.1f}"/>')
for fx in (-10, 10):
    b.append(p.dot(fx, 0)); b.append(p.txt(fx, 0, 'F', 's-txt', dy=16, anchor='middle'))
b.append(f'<line class="s-line" x1="{p.X(-15):.1f}" y1="{p.Y(0):.1f}" x2="{p.X(-15):.1f}" y2="{p.Y(4):.1f}"/>')
b.append(f'<path class="s-ar-m" d="M{p.X(-15)-5:.1f},{p.Y(4)+8:.1f} L{p.X(-15):.1f},{p.Y(4):.1f} L{p.X(-15)+5:.1f},{p.Y(4)+8:.1f} z"/>')
b.append(f'<line class="s-accent" x1="{p.X(30):.1f}" y1="{p.Y(0):.1f}" x2="{p.X(30):.1f}" y2="{p.Y(-8):.1f}"/>')
b.append(f'<polyline class="s-thin-a" points="{p.X(-15):.1f},{p.Y(4):.1f} {p.X(0):.1f},{p.Y(4):.1f} {p.X(30):.1f},{p.Y(-8):.1f}"/>')
b.append(f'<polyline class="s-thin-a" points="{p.X(-15):.1f},{p.Y(4):.1f} {p.X(30):.1f},{p.Y(-8):.1f}"/>')
b.append(p.txt(-15, 4, 'предмет', 's-txt', dy=-8, anchor='middle'))
b.append(p.txt(30, -8, 'изображение', 's-txt-a', dy=16, anchor='middle'))
b.append(p.txt(-7.5, 0, 'a', 's-txt-m', dy=-6, anchor='middle'))
b.append(p.txt(15, 0, 'b', 's-txt-m', dy=-6, anchor='middle'))
q = P(470, 10, 300, 220, (0, 60), (0, 70))
b.append(f'<line class="s-thin" x1="{q.X(0):.1f}" y1="{q.Y(0):.1f}" x2="{q.X(60):.1f}" y2="{q.Y(0):.1f}"/>')
b.append(f'<line class="s-thin" x1="{q.X(0):.1f}" y1="{q.Y(0):.1f}" x2="{q.X(0):.1f}" y2="{q.Y(70):.1f}"/>')
b.append(q.vline(10)); b.append(q.hline(10))
b += q.curve(safe(lambda a: a*10/(a-10) if a > 10 else None), 10.05, 60, 's-accent', n=800)
b.append(q.dot(15, 30)); b.append(q.txt(15, 30, '(15; 30)', 's-txt', dx=6, dy=-4))
b.append(q.txt(10, 70, 'a = f', 's-txt-a', dx=4, dy=14))
b.append(q.txt(60, 10, 'b = f', 's-txt-a', dx=-4, dy=-6, anchor='end'))
b.append(q.txt(60, 0, 'a', 's-txt-m', dx=-4, dy=-6, anchor='end'))
b.append(q.txt(0, 70, 'b', 's-txt-m', dx=6, dy=12))
figs['linza'] = svg(790, 245, 'Слева ход двух лучей через собирающую линзу с фокусами F: предмет на расстоянии 15, изображение на расстоянии 30, перевёрнутое и вдвое больше. Справа график расстояния до изображения b от расстояния до предмета a при f равно 10: гипербола с асимптотами a равно f и b равно f', b)
json.dump(figs, open('figs.json', 'w'), ensure_ascii=False)
print('ok')
