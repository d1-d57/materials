"""Вставить/обновить симуляции в LENTA/lenta.md из _sluzhebnoe/sim/*. Идемпотентно.
Запуск: python3 _sluzhebnoe/vstavit_sim.py"""
import re
D = '_sluzhebnoe/sim/'
rd = lambda f: "\n".join(l for l in open(D + f).read().splitlines() if l.strip())
L = 'LENTA/lenta.md'; s = open(L).read()
LIB = '<div class="sim-lib" hidden><style>%s</style><script>%s</script></div>' % (rd('sim.css'), rd('lib.js'))
SIMS = {
 "c1": ('<svg viewBox="0 0 650 275" role="img" aria-label="Интерактив: плоскость коэффициентов квадратного трёхчлена с параболой-дискриминантом и график трёхчлена; точку можно тащить"></svg>'
        '<div class="sim-out"></div><div class="sim-cap">Точку на плоскости $(p,q)$ можно тащить. Из точки под параболой проходят две касательные; их наклоны со знаком минус — корни трёхчлена, отмеченные на графике справа тем же цветом. Над параболой касательных нет, и корней нет.</div>'),
 "c3": ('<svg viewBox="0 0 580 250" role="img" aria-label="Интерактив: параметр лямбда обходит ноль, корни трёхчлена x квадрат плюс лямбда меняются местами"></svg>'
        '<div class="sim-bar"><button type="button">обойти ноль</button></div><div class="sim-cap">Слева $\\lambda$ обходит точку дискриминанта $0$, справа корни $x^2+\\lambda$. Каждый корень проходит пол-оборота, и после обхода корни меняются местами; второй обход возвращает их обратно.</div>'),
 "c4": ('<svg viewBox="0 0 650 310" role="img" aria-label="Интерактив: плоскость параметра a с четырьмя точками дискриминанта и пять корней многочлена x в пятой минус x плюс a; петли вокруг точек переставляют корни"></svg>'
        '<div class="sim-bar"><button type="button">вокруг +a*</button><button type="button">вокруг −a*</button><button type="button">вокруг +ia*</button><button type="button">вокруг −ia*</button><button type="button">заново</button></div>'
        '<div class="sim-out"></div><div class="sim-cap">Слева плоскость параметра $a$: крестики — точки дискриминанта, точку $a$ можно тащить или пустить по петле кнопкой. Справа пять корней $x^5-x+a$; пунктирные кружки — места корней при $a=0$. Под рисунком видно, какой корень оказался на каком месте после обходов.</div>'),
}
def block(k):
    return '<div class="sim" id="sim-%s">%s<script>%s</script></div>' % (k, SIMS[k], rd(k + '.js'))
def put(k, anchor_re=None, after=None):
    global s
    pat = re.compile(r'<div class="sim" id="sim-%s">.*?</script></div>' % k, re.S)
    if pat.search(s):
        s = pat.sub(lambda m: block(k), s); return
    if anchor_re:
        m = re.search(anchor_re, s, re.S); assert m, k
        s = s[:m.start()] + block(k) + s[m.end():]
    else:
        i = s.index(after); j = s.index("\n\n", i)
        s = s[:j] + "\n\n" + block(k) + s[j:]
# библиотека
pl = re.compile(r'<div class="sim-lib" hidden>.*?</script></div>', re.S)
if pl.search(s): s = pl.sub(lambda m: LIB, s)
put("c1", r'<figure>\n<svg[^>]*aria-label="Слева плоскость коэффициентов p, q.*?</figure>')
if not pl.search(s): s = s.replace('<div class="sim" id="sim-c1">', LIB + "\n\n" + '<div class="sim" id="sim-c1">', 1)
put("c3", r'<figure>\n<svg[^>]*aria-label="Слева: параметр лямбда обходит.*?</figure>')
put("c4", after="*Доказательство — возле точки слияния")
open(L, 'w').write(s)
print("симуляций:", len(re.findall(r'<div class="sim" id=', s)), "| библиотека:", len(pl.findall(s)))
