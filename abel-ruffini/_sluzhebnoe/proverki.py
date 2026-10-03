"""Проверки предпосылок записки-видения. Запуск: python3 _sluzhebnoe/proverki.py (из папки abel-ruffini)."""
import sympy as sp, numpy as np
x, p, q, a, t = sp.symbols('x p q a t')

print("1. Дискриминанты")
print("   x^2+px+q :", sp.discriminant(x**2+p*x+q, x))
print("   x^3+px+q :", sp.discriminant(x**3+p*x+q, x))
D5 = sp.discriminant(x**5+x+a, x)
print("   x^5+x+a  :", sp.factor(D5), "| корни по a:", sp.Poly(D5, a).degree(), "шт.")

print("2. Прямая «многочлены с корнем t» касается параболы p^2=4q")
qline = -t*p - t**2                       # t^2 + p t + q = 0
print("   p^2-4q на прямой:", sp.factor(p**2 - 4*qline))

print("3. Монодромия x^5+x+a: обход вокруг каждой точки дискриминанта")
def roots(av): return np.roots([1,0,0,0,1,av])
def track(path):
    r = roots(path[0]); start = r.copy()
    for av in path[1:]:
        new = roots(av); r = np.array([new[np.argmin(abs(new-z))] for z in r])
    return start, r
def perm(start, end): return [int(np.argmin(abs(start-z))) for z in end]
branch = [complex(z) for z in sp.Poly(D5, a).nroots()]
base = 0.3+0.0j  # базовая точка вне дискриминанта
for b in branch:
    # путь: база -> почти b по прямой, круг радиуса eps, обратно
    eps = 0.05; d = (b-base)/abs(b-base); near = b - eps*d
    seg = list(np.linspace(base, near, 4000))
    circ = [b - eps*d*np.exp(2j*np.pi*s) for s in np.linspace(0, 1, 4000)]
    path = seg + circ + seg[::-1]
    s, e = track(path); pr = perm(s, e)
    cyc = [i for i in range(5) if pr[i] != i]
    print(f"   a≈{b:.3f}: двигаются корни {cyc}  (транспозиция: {len(cyc)==2})")

print("4. Семейство Фукса — Табачникова x^5-x+a (И1, Л5) для сравнения")
D5m = sp.discriminant(x**5-x+a, x)
print("   D =", sp.factor(D5m), "| корни по a:", [complex(z) for z in sp.Poly(D5m,a).nroots()])
def roots_m(av): return np.roots([1,0,0,0,-1,av])
def track_m(path):
    r = roots_m(path[0]); start=r.copy()
    for av in path[1:]:
        new = roots_m(av); r = np.array([new[np.argmin(abs(new-z))] for z in r])
    return start, r
basem = 0.0+0.3j
for b in [complex(z) for z in sp.Poly(D5m,a).nroots()]:
    eps=0.03; d=(b-basem)/abs(b-basem); near=b-eps*d
    seg=list(np.linspace(basem,near,4000)); circ=[b-eps*d*np.exp(2j*np.pi*s) for s in np.linspace(0,1,4000)]
    s,e=track_m(seg+circ+seg[::-1]); pr=perm(s,e)
    print(f"   a≈{b:.3f}: двигаются корни {[i for i in range(5) if pr[i]!=i]}")

print("5. Ласточкин хвост x^4+ax^2+bx+c: число вещественных корней в точках при a=-2")
for (bb,cc) in [(0,0.5),(0,-1),(0,3),(1.5,0.2)]:
    r=np.roots([1,0,-2,bb,cc]); n=sum(abs(z.imag)<1e-9 for z in r)
    print(f"   a=-2, b={bb}, c={cc}: вещественных корней {n}")
D4=sp.discriminant(x**4+a*x**2+p*x+q, x)
print("   D(x^4+ax^2+bx+c) =", sp.expand(D4.subs({p:sp.Symbol('b'),q:sp.Symbol('c')})))
print("6. Пример из записки x^5+x+1 раскладывается:", sp.factor(x**5+x+1))

print("7. x^5-x+a, база a=0 (корни 0, ±1, ±i), петли: отрезок к точке ветвления, малый круг, обратно")
base0 = 0j
r0 = roots_m(0)
names = {}
for z in r0:
    w = complex(round(z.real,6), round(z.imag,6))
    names[len(names)] = {0j:'0',1+0j:'1',-1+0j:'-1',1j:'i',-1j:'-i'}.get(w, str(w))
for b in [complex(z) for z in sp.Poly(D5m,a).nroots()]:
    eps=0.02; d=b/abs(b); near=b-eps*d
    seg=list(np.linspace(base0,near,6000)); circ=[b-eps*d*np.exp(2j*np.pi*s) for s in np.linspace(0,1,6000)]
    s,e=track_m(seg+circ+seg[::-1]); pr=perm(s,e)
    moved=[names[i] for i in range(5) if pr[i]!=i]
    print(f"   точка a≈{b:.3f}: меняются местами корни {moved}")

print("8. Пример результанта двух приведённых квадратных трёхчленов")
p1,q1,p2,q2=sp.symbols('p1 q1 p2 q2')
R=sp.resultant(x**2+p1*x+q1, x**2+p2*x+q2, x)
print("   разность с формулой:", sp.expand(R-((q1-q2)**2+(p1-p2)*(p1*q2-p2*q1))))
print("   R(x^2+px+q, 2x+p) =", sp.factor(sp.resultant(x**2+p*x+q, 2*x+p, x)))
print("9. a_* = (256/3125)^(1/4) =", float((sp.Rational(256,3125))**sp.Rational(1,4)), " 4/5*5^(-1/4) =", float(sp.Rational(4,5)*5**sp.Rational(-1,4)))

print("10. Коммутатор циклов (1 2 4) и (1 3 5) в S5 (довод Арнольда в разделе «Почему нет формулы»)")
from sympy.combinatorics import Permutation
A_ = Permutation([[0,1,3]], size=5); B_ = Permutation([[0,2,4]], size=5)
for name, c in (("a b a⁻¹ b⁻¹", A_*B_*A_**-1*B_**-1), ("a⁻¹ b⁻¹ a b", A_**-1*B_**-1*A_*B_)):
    print("   ", name, "=", c.cyclic_form, "| длина цикла:", [len(x) for x in c.cyclic_form])
