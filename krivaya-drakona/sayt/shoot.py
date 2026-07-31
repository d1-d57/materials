#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Снимает каждую сцену сайта и складывает в build/_snimki/.

    python3 krivaya-drakona/sayt/shoot.py            # 1440×900, все сцены
    python3 krivaya-drakona/sayt/shoot.py 390 844    # телефон
    python3 krivaya-drakona/sayt/shoot.py --hover    # плюс кадры наведения мыши

Зачем: критерии 8 и 9 захода требуют, чтобы КАЖДАЯ сцена была снята и
просмотрена глазами, а не «код выглядит правильно». Скрипт ещё и собирает
ошибки консоли — критерий 1 требует ноль ошибок при выключенной сети,
поэтому страница открывается с file:// и запросы в сеть блокируются наглухо.
"""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(ROOT, 'build', 'index.html')
OUT = os.path.join(ROOT, 'build', '_snimki')

# (id секции, имя файла, шаг листалки или None, лишний клик или None).
# Листалок две: две карточки способов рисования (s2) и ТРИ шага доказательства
# (s4 — прежние «вершины двух сортов» и «строки» слиты в один по правке
# владельца). Снять их «доскроллом» нельзя — скрытая карточка физически
# display:none, поэтому шаг выбирается кликом по точке-индикатору, ровно так,
# как это делает читатель.
# Четвёртое поле — кнопки, которые надо нажать перед кадром (по порядку):
# предельное заполнение четырёх драконов иначе выключено, а посмотреть на него
# надо именно глазами (владелец: «не видно, что в пределе не остаётся дырок»).
# Ранг 10 снимается отдельным кадром: 4096 плиток на дракона — это и есть то
# «в пределе», и если браузер на них ляжет, увидеть это надо здесь, а не у
# владельца.
SCENES = [
    ('s0', 'oblozhka', None, None),
    ('s1', 'poloska', None, None),
    ('s2', 'narisovat-1-kopiya', 0, None),
    ('s2', 'narisovat-2-vershiny', 1, None),
    ('s3', 'peresekaet', None, None),
    ('s4', 'pochemu-net-a', 0, None),
    ('s4', 'pochemu-net-v', 1, None),
    ('s4', 'pochemu-net-g', 2, None),
    ('s5', 'chetyre-drakona', None, None),
    ('s5', 'chetyre-drakona-predel', None, ('#s5 [data-seg="fill"] button',)),
    ('s5', 'chetyre-drakona-predel-10', None,
     ('#s5 [data-seg="rank"] button[data-v="10"]',)),
    ('s6', 'razmernost', None, None),
]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    hover = '--hover' in sys.argv
    w = int(args[0]) if args else 1440
    h = int(args[1]) if len(args) > 1 else 900
    tag = '%dx%d' % (w, h)
    os.makedirs(OUT, exist_ok=True)

    from playwright.sync_api import sync_playwright
    errors, requests_out = [], []

    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': w, 'height': h},
                            device_scale_factor=2)
        # СЕТЬ ВЫКЛЮЧЕНА НАГЛУХО: любой внешний запрос — провал критерия 1
        def block(route, request):
            u = request.url
            if u.startswith('file://') or u.startswith('data:') or u.startswith('about:'):
                route.continue_()
            else:
                requests_out.append(u)
                route.abort()
        ctx.route('**/*', block)

        pg = ctx.new_page()
        pg.on('console', lambda m: errors.append(m.type + ': ' + m.text)
              if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: errors.append('pageerror: ' + str(e)))

        pg.goto('file://' + PAGE)
        pg.wait_for_function("document.documentElement.dataset.ready === '1'", timeout=15000)
        pg.wait_for_timeout(500)

        for sid, name, step, extra in SCENES:
            pg.evaluate("(id) => window.scrollTo(0, document.getElementById(id).offsetTop)", sid)
            if step is not None:
                pg.locator('#%s .pager__dot' % sid).nth(step).click()
            for sel in (extra or ()):
                pg.click(sel)
            # ⚠ ПОВТОРНЫЙ ДОСКРОЛЛ ПОСЛЕ КЛИКОВ. Playwright перед click() сам
            # прокручивает элемент в поле зрения, а листалка стоит у НИЖНЕГО края
            # сцены: на 390 px секция выше экрана, и кадр ловил листалку вместе с
            # началом следующей сцены, а сама картинка оставалась выше кадра.
            # Проверять «сцена снята» такими кадрами нельзя.
            if step is not None or extra:
                pg.evaluate("(id) => window.scrollTo(0, "
                            "document.getElementById(id).offsetTop)", sid)
            # ждём, пока сцена доиграет ДО СОСТОЯНИЯ ПОКОЯ, а не первый кадр:
            # у сцены 2 вся последовательность (лента → гармошка → две кривые)
            # идёт около 6,4 с, и на 4,2 с кадр ловил гармошку, а не результат.
            # У сцены 1 въездное складывание с передачей такта — около 6,3 с.
            wait = {'s1': 7200, 's2': 8600, 's5': 5200, 's6': 4200}
            pg.wait_for_timeout(wait.get(sid, 2600))
            path = os.path.join(OUT, '%s-%s-%s.png' % (sid, name, tag))
            pg.screenshot(path=path)
            print('  %s' % os.path.basename(path))

        if hover:
            # Кадры наведения снимаются НАСТОЯЩЕЙ мышью по координатам центра
            # зоны: .d-hit прозрачен, и hover() по селектору его не видит, а
            # dispatchEvent проверял бы обработчик в обход попадания мыши —
            # то есть не то, что делает читатель.
            # (id секции, шаг листалки или None, селектор зоны, номер, имя кадра)
            # Шагов теперь три, и номера сдвинулись: 0 — слитый шаг про вершины
            # и строки, 1 — достройка уголка, 2 — отсутствие повторов. У слитого
            # шага зона наведения — уголок (.d-hit), а не вершина: точечных зон
            # .d-hit-dot на нём больше нет.
            for sid, step, sel, idx, name in (
                    ('s4', 1, '[data-step="v"] svg .d-hit', 5,  'proof-v-hover-A'),
                    ('s4', 1, '[data-step="v"] svg .d-hit', 12, 'proof-v-hover-B'),
                    ('s4', 2, '[data-step="g"] svg .d-hit', 9,  'proof-g-hover'),
                    ('s4', 2, '[data-step="g"] svg .d-hit', 80, 'proof-g-hover-rebro'),
                    ('s4', 0, '[data-step="a"] svg .d-hit', 6, 'proof-a-hover'),
                    ('s2', 0, '[data-card="halves"] svg .d-hit', 0, 'narisovat-hover')):
                pg.evaluate("(id) => window.scrollTo(0, document.getElementById(id).offsetTop)", sid)
                if step is not None:
                    pg.locator('#%s .pager__dot' % sid).nth(step).click()
                # сцене 2 нужно дать досчитать её последовательность целиком:
                # зоны наведения на половины создаются только при угле ≥ 88°,
                # и на 1,5 с их ещё физически нет — кадр ловил гармошку
                pg.wait_for_timeout(8800 if sid == 's2' else 1500)
                # ⚠ ТОЧКА БЕРЁТСЯ НА САМОЙ ЛИНИИ, а не в центре рамки. У зоны-path
                # (половины кривой на сцене 2) центр рамки — пустое место между
                # звеньями, мышь там ни во что не попадает, и проверка «наведение
                # не работает» была ЛОЖНОЙ: обработчик исправен, промах был у пробы.
                box = pg.evaluate("""([sel, i]) => {
                    const els = document.querySelectorAll(sel);
                    if (!els.length) return null;
                    const e = els[Math.min(i, els.length - 1)];
                    if (e.getTotalLength && e.getTotalLength() > 0) {
                        const p = e.getPointAtLength(e.getTotalLength() * 0.4);
                        const q = new DOMPoint(p.x, p.y).matrixTransform(e.getScreenCTM());
                        return {x: q.x, y: q.y};
                    }
                    const r = e.getBoundingClientRect();
                    return {x: r.x + r.width / 2, y: r.y + r.height / 2};
                }""", [sel, idx])
                if not box:
                    print('  ⚠ нет элементов %s' % sel)
                    continue
                pg.mouse.move(box['x'], box['y'])
                pg.wait_for_timeout(1000)
                path = os.path.join(OUT, '%s-%s.png' % (name, tag))
                pg.screenshot(path=path)
                print('  %s' % os.path.basename(path))

            # зум сцены «Пересекает ли она себя?»: приближаемся трижды и смотрим,
            # видно ли, что линия не сплошная
            pg.evaluate("()=>window.scrollTo(0,document.getElementById('s3').offsetTop)")
            pg.wait_for_timeout(1800)
            for k in (1, 2, 3):
                pg.click('#s3 [data-seg="zoom"] button[data-v="in"]')
                pg.wait_for_timeout(2200)
                path = os.path.join(OUT, 'peresekaet-zoom%d-%s.png' % (k, tag))
                pg.screenshot(path=path)
                print('  %s' % os.path.basename(path))

            # зум финальной сцены: край на каждом увеличении выглядит так же
            pg.evaluate("()=>window.scrollTo(0,document.getElementById('s6').offsetTop)")
            pg.wait_for_timeout(1500)
            for k in (1, 2, 3):
                pg.click('#s6 [data-seg="zoom"] button[data-v="in"]')
                pg.wait_for_timeout(2200)
                path = os.path.join(OUT, 'razmernost-zoom%d-%s.png' % (k, tag))
                pg.screenshot(path=path)
                print('  %s' % os.path.basename(path))

        b.close()

    print('\nошибок/предупреждений консоли: %d' % len(errors))
    for e in errors[:25]:
        print('  ! %s' % e)
    print('внешних запросов (обязан быть 0): %d' % len(requests_out))
    for u in requests_out[:10]:
        print('  ! %s' % u)
    return 1 if (errors or requests_out) else 0


if __name__ == '__main__':
    sys.exit(main())
