# -*- coding: utf-8 -*-
"""Решения банка 7И: рисунки (SVG кодом) и сборщик текста решения.

Источник решений — src/<rabota_id>.py: на каждую задачу `z = R.z('<номер>', idei=[...])`, затем
вызовы z.otv / z.plan / z.p / z.ol / z.pic / z.tab / z.f / z.vb / z.drugoe и z.chisla(...) — числовые
ответы для сверки с bank-7i/otvety.csv. Сборка — sobrat.py. Стиль текста — STIL.md.
Цвет в рисунках — ТОЛЬКО классами из reshenie.css (s-*, f-*), никаких fill="#…"."""
import itertools

_ID = itertools.count(1)


def svg(w, h, body, label):
    """Обёртка рисунка: viewBox, role=img, подпись для чтения с экрана."""
    return (f'<svg viewBox="0 0 {w} {h}" width="{w}" role="img" aria-label="{label}">{body}</svg>')


# ---------------------------------------------------------------- готовые рисунки
def poezd(n, a, b, who, label):
    """n вагонов; верхняя полоса — вагоны 1..a, нижняя — b..n; вагон who залит."""
    cw, g, x0 = 26, 4, 18
    W = x0 * 2 + n * (cw + g)
    X = lambda i: x0 + (i - 1) * (cw + g)
    s = f'<rect class="s-band1" x="{X(1)-3}" y="8" width="{X(a)+cw-X(1)+6}" height="10" rx="3"/>'
    s += f'<rect class="s-band2" x="{X(b)-3}" y="52" width="{X(n)+cw-X(b)+6}" height="10" rx="3"/>'
    for i in range(1, n + 1):
        s += f'<rect class="{"s-car-r" if i == who else "s-car"}" x="{X(i)}" y="24" width="{cw}" height="22" rx="3"/>'
    for i in sorted({1, who, n}):
        s += f'<text class="s-txt-m" x="{X(i)+cw/2}" y="80" text-anchor="middle">{i}</text>'
    return svg(W, 88, s, label)


def numeraciya(step, last, cut, label):
    """Верхний ряд — кратные step (первые три, …, последнее лишнее | два первых нужных, …, два последних);
    нижний — их номера (делим на step). Слева лишние (до cut включительно), справа нужные."""
    kc, kn = cut // step, last // step
    seq = [1, 2, 3, '…', kc, kc + 1, kc + 2, '…', kn - 1, kn]
    dx, x0 = 46, 26
    W = x0 * 2 + (len(seq) - 1) * dx
    ia = seq.index(kc)
    xa, xb = x0 - 20, x0 + ia * dx + 20
    s = f'<rect class="s-fill-skip" x="{xa}" y="4" width="{xb-xa}" height="104" rx="8"/>'
    s += f'<rect class="s-fill-need" x="{xb+4}" y="4" width="{x0+(len(seq)-1)*dx+20-xb-4}" height="104" rx="8"/>'
    for n_, k in enumerate(seq):
        x = x0 + n_ * dx
        if k == '…':
            s += f'<text class="s-num" x="{x}" y="30" text-anchor="middle">…</text>'
            s += f'<text class="s-num" x="{x}" y="96" text-anchor="middle">…</text>'
            continue
        cls = 's-big-a' if k > kc else 's-big'
        s += f'<text class="{cls}" x="{x}" y="30" text-anchor="middle">{k*step}</text>'
        s += f'<line class="s-thin" x1="{x}" y1="40" x2="{x}" y2="70"/>'
        s += f'<path class="s-ar-m" d="M{x-4},68 l4,8 4,-8 z"/>'
        s += f'<text class="{cls}" x="{x}" y="96" text-anchor="middle">{k}</text>'
    return svg(W, 112, s, label)


def krugi(lev, prav, oba, nik, zona, label, podpisi=('', '')):
    """Круги Эйлера в прямоугольнике: числа в областях (строки или числа);
    zona: 'union' — залиты оба круга, 'inter' — пересечение, 'lev' / 'prav' — один круг, '' — ничего.
    podpisi — подписи кругов (слева, справа) над ними."""
    W, H = 360, 200
    k = next(_ID)
    s = f'<defs><clipPath id="rs-kl-{k}"><circle cx="135" cy="105" r="70"/></clipPath></defs>'
    s += f'<rect class="s-frame" x="10" y="8" width="{W-20}" height="{H-16}" rx="10"/>'
    if zona == 'union':
        s += '<circle class="s-fill-need" cx="135" cy="105" r="70"/><circle class="s-fill-need" cx="225" cy="105" r="70"/>'
    elif zona == 'inter':
        s += f'<circle class="s-fill-need" cx="225" cy="105" r="70" clip-path="url(#rs-kl-{k})"/>'
    elif zona == 'lev':
        s += '<circle class="s-fill-need" cx="135" cy="105" r="70"/>'
    elif zona == 'prav':
        s += '<circle class="s-fill-need" cx="225" cy="105" r="70"/>'
    s += '<circle class="s-ring" cx="135" cy="105" r="70"/><circle class="s-ring" cx="225" cy="105" r="70"/>'
    for x, t in ((100, lev), (260, prav), (180, oba)):
        s += f'<text class="s-num" x="{x}" y="112" text-anchor="middle">{t}</text>'
    s += f'<text class="s-num" x="{W-38}" y="{H-22}" text-anchor="middle">{nik}</text>'
    if podpisi[0]:
        s += f'<text class="s-txt" x="90" y="28" text-anchor="middle">{podpisi[0]}</text>'
    if podpisi[1]:
        s += f'<text class="s-txt" x="270" y="28" text-anchor="middle">{podpisi[1]}</text>'
    return svg(W, H, s, label)


def spichki(r, c, label):
    """Прямоугольник r рядов по c клеток из спичек: горизонтальные — s-m1 (оранж.), вертикальные — s-m2 (син.)."""
    L, x0, y0 = 30, 16, 16
    s = ''
    for i in range(r + 1):
        for j in range(c):
            s += f'<line class="s-m1" x1="{x0+j*L+3}" y1="{y0+i*L}" x2="{x0+(j+1)*L-3}" y2="{y0+i*L}"/>'
    for j in range(c + 1):
        for i in range(r):
            s += f'<line class="s-m2" x1="{x0+j*L}" y1="{y0+i*L+3}" x2="{x0+j*L}" y2="{y0+(i+1)*L-3}"/>'
    return svg(x0 * 2 + c * L, y0 * 2 + r * L, s, label)


COL = {'Б': 'f-b', 'К': 'f-k', 'С': 'f-s'}


def flagi(rows, label):
    """Строки флагов [[флаг, …], …]; флаг — строка из букв Б/К/С (любой длины), рисуется полосами."""
    fw, fh, gx, gy, x0, y0 = 30, 36, 12, 16, 14, 12
    W = x0 * 2 + max(len(r) for r in rows) * (fw + gx)
    s = ''
    for ri, row in enumerate(rows):
        for ci, f in enumerate(row):
            x, y = x0 + ci * (fw + gx), y0 + ri * (fh + gy)
            for k, ch in enumerate(f):
                s += f'<rect class="{COL[ch]}" x="{x}" y="{y+k*fh/len(f):.1f}" width="{fw}" height="{fh/len(f):.1f}"/>'
            s += f'<rect class="s-frame" x="{x}" y="{y}" width="{fw}" height="{fh}"/>'
    return svg(W, y0 * 2 + len(rows) * (fh + gy) - gy, s, label)


def reshetka(ryadov, v_ryadu, kvadraty, label, shag=40):
    """Решётка точек ryadov × v_ryadu; kvadraty — список четвёрок точек (столбец, ряд) от 0,
    каждый рисуется ломаной: первый — s-line-a, остальные — s-line-w."""
    x0 = y0 = 18
    W, H = x0 * 2 + (v_ryadu - 1) * shag, y0 * 2 + (ryadov - 1) * shag
    P = lambda c, r: (x0 + c * shag, y0 + r * shag)
    s = ''
    for i, q in enumerate(kvadraty):
        pts = ' '.join(f'{P(c, r)[0]},{P(c, r)[1]}' for c, r in q)
        s += f'<polygon class="{"s-line-a" if i == 0 else "s-line-w"}" points="{pts}"/>'
    for r in range(ryadov):
        for c in range(v_ryadu):
            x, y = P(c, r)
            s += f'<circle class="s-dot" cx="{x}" cy="{y}" r="4"/>'
    return svg(W, H, s, label)


def ryad(chisla, vydeleny, label, shag=40):
    """Ряд клеток с числами (строки или числа); индексы из vydeleny залиты. '…' — многоточие без клетки."""
    x0, cw = 10, shag - 6
    s = ''
    for i, t in enumerate(chisla):
        x = x0 + i * shag
        if t != '…':
            s += f'<rect class="{"s-fill-need" if i in vydeleny else "s-fill-skip"}" x="{x}" y="6" width="{cw}" height="30" rx="4"/>'
        s += f'<text class="s-big" x="{x+cw/2}" y="27" text-anchor="middle">{t}</text>'
    return svg(x0 * 2 + len(chisla) * shag - 6, 42, s, label)


# ---------------------------------------------------------------- текст решения
class Zadacha:
    def __init__(self, rabota, n, idei):
        self.rabota, self.n, self.idei = rabota, n, list(idei)
        self.P, self.N, self.otvety = [], 0, {}

    def _add(self, t):
        self.P.append(t)
        return self

    def otv(self, t):
        """Ответ одной строкой — в начале решения: «(а) А: 18, Б: 20. (б) …»."""
        return self._add(f'<p class="otv"><b>Ответ.</b> {t}</p>')

    def plan(self, t):
        """Подводка «План: …» перед содержательным шагом."""
        return self._add(f'<p class="plan"><b>План.</b> {t}</p>')

    def p(self, t):
        return self._add(f'<p>{t}</p>')

    def f(self, t):
        """Формула отдельной строкой."""
        return self._add(f'<p class="f">{t}</p>')

    def ol(self, items):
        """Шаги, по одной идее в каждом; нумерация сквозная внутри задачи."""
        self._add(f'<ol start="{self.N+1}">' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>')
        self.N += len(items)
        return self

    def pic(self, s, cap):
        return self._add(f'<figure>{s}<figcaption>{cap}</figcaption></figure>')

    def tab(self, head, rows):
        return self._add('<div class="tab-wrap"><table><tr>' + ''.join(f'<th>{x}</th>' for x in head) + '</tr>' +
                         ''.join('<tr>' + ''.join(f'<td>{x}</td>' for x in r) + '</tr>' for r in rows) +
                         '</table></div>')

    def vb(self, t):
        """Что меняется в варианте Б (одна-две строки, тем же рассуждением)."""
        return self._add(f'<p class="vb"><b>Вариант Б.</b> {t}</p>')

    def drugoe(self, t):
        """Другое решение — только когда идея действительно другая (STIL.md)."""
        return self._add(f'<p class="drugoe"><b>Другое решение.</b> {t}</p>')

    def chisla(self, **po_variantam):
        """Числовые ответы для сверки с otvety.csv: z.chisla(А={'1а': 18}, Б={'1а': 20}); у ДЗ без вариантов — z.chisla(_={'1': 135})."""
        for v, d in po_variantam.items():
            for punkt, x in d.items():
                self.otvety[('' if v == '_' else v, str(punkt))] = x
        return self

    def html(self):
        return (f'<div class="rs" data-rabota="{self.rabota}" data-n="{self.n}" data-idei="{",".join(map(str, self.idei))}">'
                + '\n'.join(self.P) + '</div>')


class Rabota:
    def __init__(self, rabota_id):
        self.id, self.zadachi = rabota_id, []

    def z(self, n, idei=()):
        """Новая задача: n — номер задачи в работе без буквы пункта ('1', '12'); idei — номера идей (STIL.md)."""
        z = Zadacha(self.id, str(n), idei)
        self.zadachi.append(z)
        return z
