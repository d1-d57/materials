# -*- coding: utf-8 -*-
"""Статичные рисунки статьи «Умный перебор»: SVG строкой, цвет только токенами движка (var(--…)) с запасным цветом.
Рисунки статичны: каждый показывает раскладку одного подсчёта, двигать в них нечего."""

ST = ('<style>.up-t{font-family:var(--sans,system-ui,sans-serif);fill:var(--text,#222)}'
      '.up-m{font-family:var(--sans,system-ui,sans-serif);fill:var(--muted,#666)}'
      '.up-c{fill:var(--panel,#fff);stroke:var(--rule,#c9c9c9);stroke-width:1}'
      '.up-a{fill:var(--accent,#2f6f8f);fill-opacity:.2;stroke:var(--accent,#2f6f8f);stroke-width:1}'
      '.up-w{fill:var(--warm,#b5651d);fill-opacity:.2;stroke:var(--warm,#b5651d);stroke-width:1}'
      '.up-s{fill:var(--muted,#888);fill-opacity:.16;stroke:var(--rule,#c9c9c9);stroke-width:1}'
      '.up-x{fill:none;stroke:var(--text,#222);stroke-width:2.2}'
      '.up-l{fill:none;stroke:var(--muted,#666);stroke-width:1.2}'
      '.up-al{fill:none;stroke:var(--accent,#2f6f8f);stroke-width:1.4}</style>')


def _t(x, y, s, cls='up-t', size=14, anchor='middle', weight=400):
    return f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>'


def grid():
    """Двузначные числа таблицей 9×10: строка 70–79 и столбец «…7» пересекаются в 77."""
    w, h, x0, y0 = 42, 28, 58, 30
    out = [ST]
    out.append(_t(x0 + 5 * w, 16, 'последняя цифра →', 'up-m', 12))
    for u in range(10):
        out.append(_t(x0 + u * w + w / 2, y0 - 4, str(u), 'up-m', 12))
    for r, d in enumerate(range(1, 10)):
        out.append(_t(x0 - 30, y0 + r * h + h / 2 + 5, str(d), 'up-m', 12))
        for u in range(10):
            n = 10 * d + u
            cls = 'up-c'
            if d == 7 and u == 7:
                cls = 'up-a'
            elif d == 7:
                cls = 'up-a'
            elif u == 7:
                cls = 'up-w'
            x, y = x0 + u * w, y0 + r * h
            out.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}"/>')
            if u == 7 and d != 7:
                pass
            out.append(_t(x + w / 2, y + h / 2 + 5, str(n), 'up-t', 13, weight=600 if (d == 7 or u == 7) else 400))
    # столбец «…7» поверх строки: тёплая заливка на 77 тоже, и рамка
    x77, y77 = x0 + 7 * w, y0 + 6 * h
    out.append(f'<rect class="up-w" x="{x77}" y="{y77}" width="{w}" height="{h}"/>')
    out.append(_t(x77 + w / 2, y77 + h / 2 + 5, '77', 'up-t', 13, weight=700))
    out.append(f'<rect class="up-x" x="{x77}" y="{y77}" width="{w}" height="{h}"/>')
    out.append(_t(x0 - 30, y0 - 4, 'первая ↓', 'up-m', 11))
    W, H = x0 + 10 * w + 8, y0 + 9 * h + 8
    return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Таблица двузначных чисел: строка семидесятых и столбец чисел, '
            f'оканчивающихся на семь, выделены и пересекаются в числе 77">' + ''.join(out) + '</svg>')


def dalm():
    """Полоса из 101 далматинца: 22 без пятен, 29 только левое, 17 только правое, 33 оба уха."""
    x0, X, y, hh = 20, 600, 46, 34
    k = X / 101
    seg = [(22, 'без пятен на ушах', '22', 'up-s'), (29, 'только левое', '29', 'up-s'),
           (17, 'только правое', '17', 'up-a'), (33, 'оба уха', '?', 'up-a')]
    out, x = [ST], x0
    for n, lab, num, cls in seg:
        w = n * k
        out.append(f'<rect class="{cls}" x="{x:.1f}" y="{y}" width="{w:.1f}" height="{hh}"/>')
        out.append(_t(x + w / 2, y - 22, lab, 'up-m', 12))
        out.append(_t(x + w / 2, y - 7, num, 'up-t', 13, weight=600))
        x += w
    # скобка под «пятном на правом ухе»
    a, b, yb = x0 + 51 * k, x0 + 101 * k, y + hh + 10
    out.append(f'<path class="up-al" d="M{a:.1f},{yb} v8 H{b:.1f} v-8"/>')
    out.append(_t((a + b) / 2, yb + 26, 'пятно на правом ухе: 101 − 22 − 29 = 50', 'up-t', 13, weight=600))
    a2, b2 = x0, x0 + 51 * k
    out.append(f'<path class="up-l" d="M{a2:.1f},{yb} v8 H{b2:.1f} v-8"/>')
    out.append(_t((a2 + b2) / 2, yb + 26, 'ненужные: 22 + 29', 'up-m', 12))
    W, H = x0 + X + 20, yb + 36
    return (f'<svg viewBox="0 0 {W:.0f} {H:.0f}" role="img" aria-label="Полоса из 101 далматинца разрезана на четыре куска: '
            f'без пятен 22, только левое ухо 29, только правое 17, оба уха неизвестно; пятно на правом ухе у 101 минус 22 минус 29">'
            + ''.join(out) + '</svg>')


def strip():
    """Ряд 1…23: кусок 1…16 и наш кусок 17…23."""
    x0, w, y, hh = 14, 24, 40, 30
    out = [ST]
    for i in range(1, 24):
        cls = 'up-s' if i <= 16 else 'up-a'
        x = x0 + (i - 1) * w
        out.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{hh}"/>')
        out.append(_t(x + w / 2, y + hh / 2 + 4.5, str(i), 'up-t', 11, weight=600 if i > 16 else 400))
    a, b = x0, x0 + 16 * w
    out.append(f'<path class="up-l" d="M{a},{y - 6} v-8 H{b} v8"/>')
    out.append(_t((a + b) / 2, y - 20, 'от 1 до 16: 16 чисел', 'up-m', 12))
    c, d = x0 + 16 * w, x0 + 23 * w
    out.append(f'<path class="up-al" d="M{c},{y - 6} v-8 H{d} v8"/>')
    out.append(_t((c + d) / 2, y - 20, 'наши: 23 − 16 = 7', 'up-t', 12, weight=600))
    e = y + hh + 8
    out.append(f'<path class="up-l" d="M{a},{e} v8 H{d} v-8"/>')
    out.append(_t((a + d) / 2, e + 24, 'от 1 до 23: 23 числа', 'up-m', 12))
    W, H = x0 + 23 * w + 14, e + 32
    return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Ряд чисел от 1 до 23: первые шестнадцать серые, '
            f'числа с 17 по 23 выделены; выделенных 23 минус 16">' + ''.join(out) + '</svg>')


RIS = {'grid': grid, 'dalm': dalm, 'strip': strip}


COL = {'Б': '#ffffff', 'К': '#c8322c', 'С': '#2a55b5'}
def _flag(x, y, f, w=46, h=30):
    s = []
    for i, c in enumerate(f):
        s.append(f'<rect x="{x}" y="{y + i*h/len(f):.1f}" width="{w}" height="{h/len(f):.2f}" fill="{COL[c]}"/>')
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="var(--text,#222)" stroke-width="1.2"/>')
    s.append(_t(x + w/2, y + h + 14, f, 'up-t', 12, weight=600))
    return ''.join(s)
def flags3():
    """12 флагов из трёх полос: три строки по верхней полосе, внутри — словарный порядок."""
    from itertools import product
    fl = [''.join(f) for f in product('БКС', repeat=3) if f[0] != f[1] and f[1] != f[2]]
    out = [ST]; x0, y0, dx, dy = 96, 10, 62, 58
    names = {'Б': 'верх белый', 'К': 'верх красный', 'С': 'верх синий'}
    for r, top in enumerate('БКС'):
        row = [f for f in fl if f[0] == top]
        out.append(_t(8, y0 + r*dy + 19, names[top], 'up-m', 12, 'start'))
        for j, f in enumerate(row):
            out.append(_flag(x0 + j*dx, y0 + r*dy, f))
        out.append(_t(x0 + 4*dx + 6, y0 + r*dy + 19, '4', 'up-t', 15, 'start', 700))
    W, H = x0 + 4*dx + 26, y0 + 3*dy
    return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Двенадцать флагов из трёх полос в трёх строках по цвету верхней полосы, по четыре в строке, в словарном порядке">'
            + ''.join(out) + '</svg>')
def flagtree():
    """Почему в строке четыре флага: верх белый → средняя К или С → нижняя любая, кроме средней."""
    out = [ST]; LY = [6, 60, 114, 168]; leaves = ['БКБ', 'БКС', 'БСБ', 'БСК']
    out.append(_flag(10, 88, 'Б', 40, 26))
    for m, my, ls in (('БК', 33, (0, 1)), ('БС', 141, (2, 3))):
        out.append(f'<path class="up-l" d="M50,101 L120,{my+15}"/>')
        out.append(_flag(120, my, m, 40, 30))
        for i in ls:
            out.append(f'<path class="up-l" d="M160,{my+15} L230,{LY[i]+15}"/>')
            out.append(_flag(230, LY[i], leaves[i], 40, 30))
    out.append(_t(140, 236, 'средняя: 2 цвета', 'up-m', 12))
    out.append(_t(250, 236, 'нижняя: 2 цвета', 'up-m', 12))
    return ('<svg viewBox="0 0 310 244" role="img" aria-label="Дерево выбора для флагов с белым верхом: два цвета средней полосы, для каждого два цвета нижней, всего четыре флага">'
            + ''.join(out) + '</svg>')
RIS.update({'flags3': flags3, 'flagtree': flagtree})
