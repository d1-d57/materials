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
