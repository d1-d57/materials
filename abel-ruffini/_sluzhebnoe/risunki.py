"""Статичные рисунки статьи. Запуск: python3 _sluzhebnoe/risunki.py → _sluzhebnoe/ris/*.svg.
Классы — только из build_doc.py (.s-*); внутри рисунка — только метки осей и координаты."""
import numpy as np, os, math
OUT = os.path.join(os.path.dirname(__file__), "ris")

class Panel:
    def __init__(s, x0, y0, w, h, xr, yr):
        s.x0, s.y0, s.w, s.h, s.xr, s.yr = x0, y0, w, h, xr, yr
    def X(s, x): return s.x0 + (x - s.xr[0]) / (s.xr[1] - s.xr[0]) * s.w
    def Y(s, y): return s.y0 + s.h - (y - s.yr[0]) / (s.yr[1] - s.yr[0]) * s.h
    def inside(s, x, y, pad=0): return s.xr[0]-pad <= x <= s.xr[1]+pad and s.yr[0]-pad <= y <= s.yr[1]+pad
    def path(s, xs, ys, cls, close=False):
        segs, cur = [], []
        for x, y in zip(xs, ys):
            if s.inside(x, y):
                cur.append("%.1f,%.1f" % (s.X(x), s.Y(y)))
            else:
                if len(cur) > 1: segs.append(cur)
                cur = []
        if len(cur) > 1: segs.append(cur)
        return "".join('<path class="%s" d="M%s%s"/>' % (cls, " L".join(c), " Z" if close else "") for c in segs)
    def poly(s, xs, ys, cls):
        pts = " ".join("%.1f,%.1f" % (s.X(min(max(x, s.xr[0]), s.xr[1])), s.Y(min(max(y, s.yr[0]), s.yr[1]))) for x, y in zip(xs, ys))
        return '<polygon class="%s" points="%s"/>' % (cls, pts)
    def axes(s, lx, ly, ox=0, oy=0):
        out = '<line class="s-thin" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (s.X(s.xr[0]), s.Y(oy), s.X(s.xr[1]), s.Y(oy))
        out += '<line class="s-thin" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (s.X(ox), s.Y(s.yr[0]), s.X(ox), s.Y(s.yr[1]))
        out += '<path class="s-ar-m" d="M%.1f,%.1f l-8,-3.5 0,7 z"/>' % (s.X(s.xr[1]), s.Y(oy))
        out += '<path class="s-ar-m" d="M%.1f,%.1f l-3.5,8 7,0 z"/>' % (s.X(ox), s.Y(s.yr[1]))
        if lx: out += '<text class="s-txt-m" x="%.1f" y="%.1f">%s</text>' % (s.X(s.xr[1]) - 10, s.Y(oy) + 16, lx)
        if ly: out += '<text class="s-txt-m" x="%.1f" y="%.1f">%s</text>' % (s.X(ox) + 7, s.Y(s.yr[1]) + 10, ly)
        return out
    def node(s, x, y, cls="s-node", r=3.6):
        return '<circle class="%s" cx="%.1f" cy="%.1f" r="%.1f"/>' % (cls, s.X(x), s.Y(y), r)
    def cross(s, x, y, d=4.5):
        X, Y = s.X(x), s.Y(y)
        return '<path class="s-accent" d="M%.1f,%.1f L%.1f,%.1f M%.1f,%.1f L%.1f,%.1f"/>' % (X-d, Y-d, X+d, Y+d, X-d, Y+d, X+d, Y-d)
    def txt(s, x, y, t, cls="s-txt-m", dx=0, dy=0):
        return '<text class="%s" x="%.1f" y="%.1f">%s</text>' % (cls, s.X(x) + dx, s.Y(y) + dy, t)

def arrow(P, x, y, dx, dy, cls="s-ar-a", L=10, W=4.5):
    """Наконечник в точке (x,y) мат. координат; (dx,dy) — направление движения в мат. координатах."""
    X, Y = P.X(x), P.Y(y)
    ux, uy = dx * P.w / (P.xr[1]-P.xr[0]), -dy * P.h / (P.yr[1]-P.yr[0])
    n = math.hypot(ux, uy); ux, uy = ux / n, uy / n
    bx, by = X - L * ux, Y - L * uy
    return '<path class="%s" d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f z"/>' % (cls, X, Y, bx - W * uy, by + W * ux, bx + W * uy, by - W * ux)

def svg(name, w, h, label, body):
    with open(os.path.join(OUT, name + ".svg"), "w") as f:
        f.write('<svg viewBox="0 0 %d %d" role="img" aria-label="%s">%s</svg>' % (w, h, label, body))

T = np.linspace

# Р1: плоскость (p,q): области «два корня» / «нет корней», парабола «один корень»
def r1():
    A = Panel(20, 15, 420, 250, (-3, 3), (-1.6, 2.6))
    b = ""
    ps = T(-3, 3, 200); qs = ps**2 / 4
    b += A.poly(list(ps) + [3, -3], list(qs) + [2.6, 2.6], "s-fillsh")
    b += A.axes("p", "q")
    b += A.path(ps, qs, "s-line")
    b += A.node(-0.6, 1.6, "s-node", 4)
    b += A.node(1.6, 0.64, "s-node s-node-r", 4)
    b += A.node(0.9, -0.9, "s-node-a", 4)
    svg("r1-ploskost", 460, 280, "Плоскость коэффициентов p, q: парабола-дискриминант делит её на область без корней (закрашена, над параболой) и область с двумя корнями (под параболой); на самой параболе — один корень", b)

# Р3: полукубическая парабола
def r3():
    A = Panel(20, 15, 360, 230, (-3.2, 1.2), (-2.6, 2.6))
    b = ""
    ts = T(-1.15, 1.15, 300)
    P, Q = -3 * ts**2, 2 * ts**3
    b += A.poly(list(P), list(Q), "s-fillsh")
    b += A.axes("p", "q")
    b += A.path(P, Q, "s-line")
    t = 0.75; ps = T(-3.2, 1.2, 200)
    b += A.path(ps, -t * ps - t**3, "s-accent")
    b += A.node(-3 * t * t, 2 * t**3, "s-node-a", 3.2)
    svg("r3-ostrie", 400, 260, "Полукубическая парабола — дискриминантная кривая кубических многочленов; внутри клюва закрашена область трёх вещественных корней; одна касательная прямая", b)

# Р4: ласточкин хвост — три сечения
def r4():
    b = ""
    for k, a in enumerate([1.0, 0.0, -2.0]):
        A = Panel(15 + k * 215, 15, 190, 200, (-2.6, 2.6), (-1.4, 2.6))
        ts = T(-1.6, 1.6, 600)
        B, C = -4 * ts**3 - 2 * a * ts, 3 * ts**4 + a * ts**2
        if a < 0:
            tt = T(-1, 1, 300)
            b += A.poly(list(-4 * tt**3 - 2 * a * tt), list(3 * tt**4 + a * tt**2), "s-fillsh")
        b += A.axes("b" if k == 0 else "", "c" if k == 0 else "")
        b += A.path(B, C, "s-line")
    svg("r4-lastochkin-hvost", 660, 230, "Три сечения ласточкина хвоста плоскостями a равно const: гладкая кривая, кривая с особой точкой, кривая с двумя остриями и самопересечением; закрашен криволинейный треугольник четырёх корней", b)

# Р5: корень не пропадает
def r5():
    A = Panel(20, 15, 400, 220, (-1.2, 1.5), (-1.3, 2.0))
    b = A.axes("x", "")
    f = lambda x: x**3 - 2 * x + 0.3
    xs = T(-1.2, 1.5, 300)
    x0 = float([r.real for r in np.roots([1, 0, -2, 0.3]) if abs(r.imag) < 1e-9 and 0 < r.real < 0.5][0])
    eps = 0.35
    b += '<rect class="s-fillsh" x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>' % (A.X(x0 - eps), A.Y(2.0), A.X(x0 + eps) - A.X(x0 - eps), A.Y(-1.3) - A.Y(2.0))
    b += A.path(xs, f(xs), "s-line")
    b += A.path(xs, f(xs) + 0.28, "s-accent")
    d = 3 * x0**2 - 2
    b += A.path(xs, d * (xs - x0), "s-dash")
    b += A.node(x0, 0, "s-node s-node-r")
    g = lambda x: f(x) + 0.28
    x1 = float([r.real for r in np.roots([1, 0, -2, 0.58]) if abs(r.imag) < 1e-9 and 0 < r.real < 0.6][0])
    b += A.node(x1, 0, "s-node-a", 3.6)
    svg("r5-koren-vyzhivaet", 440, 250, "График многочлена возле простого корня, касательная пунктиром и сдвинутый график; на полосе вокруг корня у сдвинутого графика ровно одно пересечение с осью", b)

# Р6: обход в плоскости s
def r6():
    A = Panel(20, 15, 440, 170, (-0.4, 1.4), (-0.45, 0.45))
    b = A.axes("", "")
    bad = [(0.55, 0.0), (0.2, 0.3), (0.95, -0.28), (1.2, 0.22)]
    for x, y in bad: b += A.cross(x, y)
    r = 0.09
    xs1 = T(0, 0.55 - r, 50); xs2 = T(0.55 + r, 1, 50)
    arc = T(math.pi, 0, 60)
    xs = list(xs1) + list(0.55 + r * np.cos(arc)) + list(xs2)
    ys = [0] * 50 + list(r * 1.0 * np.sin(arc) * (A.w / (A.xr[1]-A.xr[0])) / (A.h / (A.yr[1]-A.yr[0]))) + [0] * 50
    b += A.path(xs, ys, "s-accent")
    b += A.node(0, 0, "s-node s-node-r"); b += A.node(1, 0, "s-node s-node-r")
    b += A.txt(0, 0, "0", dx=5, dy=20); b += A.txt(1, 0, "1", dx=-4, dy=20)
    svg("r6-obhod", 480, 200, "Комплексная плоскость параметра s: точки 0 и 1, несколько запретных точек крестиками, путь от 0 до 1 огибает запретную точку по полуокружности", b)

# Р8: x^2 + lambda
def r8():
    b = ""
    A = Panel(20, 15, 200, 200, (-1.5, 1.5), (-1.5, 1.5))
    b += A.axes("", "")
    th = T(0, 2 * math.pi * 0.96, 200)
    b += A.path(np.cos(th), np.sin(th), "s-accent")
    e = 2 * math.pi * 0.96
    b += arrow(A, math.cos(e), math.sin(e), -math.sin(e), math.cos(e))
    b += A.cross(0, 0); b += A.node(1, 0, "s-node s-node-r")
    B = Panel(290, 15, 200, 200, (-1.5, 1.5), (-1.5, 1.5))
    b += B.axes("", "")
    th = T(math.pi / 2, math.pi / 2 + math.pi * 0.93, 120)
    b += B.path(np.cos(th), np.sin(th), "s-thin-a")
    th2 = T(-math.pi / 2, -math.pi / 2 + math.pi * 0.93, 120)
    b += B.path(np.cos(th2), np.sin(th2), "s-thin-a")
    for e in [math.pi / 2 + math.pi * 0.93, -math.pi / 2 + math.pi * 0.93]:
        b += arrow(B, math.cos(e), math.sin(e), -math.sin(e), math.cos(e))
    b += B.node(0, 1, "s-node s-node-r"); b += B.node(0, -1, "s-node-a")
    b += B.txt(0, 1, "i", dx=8, dy=-4); b += B.txt(0, -1, "−i", dx=8, dy=14)
    svg("r8-x2-lambda", 510, 230, "Слева: параметр лямбда обходит окружность вокруг нуля. Справа: корни трёхчлена x квадрат плюс лямбда поворачиваются на пол-оборота и меняются местами", b)

# Р9: x^5 + lambda
def r9():
    A = Panel(160, 15, 210, 210, (-1.5, 1.5), (-1.5, 1.5))
    b = A.axes("", "")
    for k in range(5):
        a0 = math.pi / 5 + 2 * math.pi * k / 5
        th = T(a0 + 0.12, a0 + 2 * math.pi / 5 - 0.18, 40)
        b += A.path(np.cos(th), np.sin(th), "s-thin-a")
        e = a0 + 2 * math.pi / 5 - 0.18
        b += arrow(A, math.cos(e), math.sin(e), -math.sin(e), math.cos(e))
        b += A.node(math.cos(a0), math.sin(a0), "s-node s-node-r" if k == 0 else "s-node")
    svg("r9-x5-lambda", 530, 240, "Пять корней многочлена x в пятой плюс лямбда в вершинах правильного пятиугольника; при обходе лямбда каждый корень поворачивается на одну пятую оборота", b)

# Р10: график a = x - x^5
def r10():
    A = Panel(30, 15, 440, 230, (-1.35, 1.35), (-0.95, 0.95))
    b = A.axes("x", "a")
    xs = T(-1.3, 1.3, 400)
    b += A.path(xs, xs - xs**5, "s-line")
    xs_ = 5 ** -0.25; ast = xs_ - xs_**5
    for s_ in (1, -1):
        b += A.path([-1.35, 1.35], [s_ * ast] * 2, "s-dash")
        b += A.node(s_ * xs_, s_ * ast, "s-node-a", 3.6)
    for r in (-1, 0, 1):
        b += A.node(r, 0, "s-node s-node-r")
    b += A.txt(1, 0, "1", dx=-3, dy=18); b += A.txt(-1, 0, "−1", dx=-22, dy=18); b += A.txt(0, 0, "0", dx=6, dy=16)
    svg("r10-grafik-x-x5", 500, 260, "График функции a равно x минус x в пятой: при a равном нулю корни минус один, ноль, один; на уровнях плюс-минус a со звёздочкой два корня сливаются", b)

# Р11: петли в плоскости a и звезда обменов
def r11():
    b = ""
    A = Panel(20, 15, 220, 220, (-0.8, 0.8), (-0.8, 0.8))
    ast = (256 / 3125) ** 0.25
    for k in range(4):
        u = complex(math.cos(k * math.pi / 2), math.sin(k * math.pi / 2)); c = ast * u
        r = 0.07
        near = c - r * u
        b += A.path([0, near.real], [0, near.imag], "s-thin-a")
        th = T(0, 2 * math.pi, 80)
        circ = [c - r * u * complex(math.cos(t), math.sin(t)) for t in th]
        b += A.path([z.real for z in circ], [z.imag for z in circ], "s-thin-a")
        b += A.cross(c.real, c.imag, 4)
    b += A.node(0, 0, "s-node s-node-r")
    B = Panel(300, 15, 220, 220, (-1.5, 1.5), (-1.5, 1.5))
    for (x, y) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        b += '<line class="s-accent" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (B.X(0), B.Y(0), B.X(x), B.Y(y))
    for (x, y) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        b += B.node(x, y, "s-node")
    b += B.node(0, 0, "s-node s-node-r")
    b += B.txt(1, 0, "1", dx=-2, dy=18); b += B.txt(-1, 0, "−1", dx=-8, dy=18); b += B.txt(0, 1, "i", dx=8, dy=0); b += B.txt(0, -1, "−i", dx=8, dy=4); b += B.txt(0, 0, "0", dx=6, dy=16)
    svg("r11-zvezda", 540, 250, "Слева: плоскость параметра a, четыре точки дискриминанта и четыре петли из нуля. Справа: корни 0, 1, минус 1, i, минус i; каждая петля меняет местами корень 0 с одним из четырёх — звезда обменов", b)

for f in (r1, r3, r4, r5, r6, r8, r9, r10, r11): f()
print("\n".join(sorted(os.listdir(OUT))))
