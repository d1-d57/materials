#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Вёрстка: src/slides/<id>.html + пер-слайдовый грид в <style> шаблона (арка 7).

  python3 teorkat-vvedenie/src/tools/sverstat.py

Почему генератором, а не руками: 55 слайдов, и у каждого грид обязан быть согласован
с числом знаков текста и с пропорцией СВОЕЙ иллюстрации. Хук H6 (`GEJTY.md`) прямо
называет руками выписанную вычислимую величину дефектом: «если значение обязано
совпадать с другим значением — оно должно порождаться, а не сверяться». Решение
«какая раскладка этому слайду» при этом НЕ отдано скрипту: архетип каждого слайда
назначила лента (`> поле:mn **Раскладка.**`), скрипт его исполняет — ровно как
требует `07-verstka/DOK.md` («арка 7 реализует принятую раскладку»).

Ручная доводка по глазам (шаг 6 захода) живёт в PRAVKI ниже — пер-слайдовым
словарём, а не правкой выхода: выход перезаписывается каждым прогоном.

Четыре архетипа:
  рейка-справа          текст ~72%W + полоса-доска ~24%W с белой панелью илл.
  доска-пустая          текст ~86%W + узкая полоса-доска без илл. (илл. у слайда нет)
  илл-полосой-снизу     текст сверху во всю ширину + широкая илл. полосой снизу
  лестница-во-всю-ширину  только текст во всю ширину, двумя колонками (список тождеств)
"""
import re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from porodit import load_all, archetype, visible_chars, slug  # один источник разбора ленты

SRC = Path(__file__).resolve().parents[1]
W, H = 1440, 810

# ── ручная доводка по PNG (шаг 6). Ключ — id, значения перекрывают расчёт. ──
# Каждая строка — результат просмотра снятого кадра, а не догадка.
PRAVKI = {
    # s52 «Стоун: конечный случай полностью» — единственный слайд, которому не
    # хватило всей лестницы: промер даёт +15px, то есть треть строки, при семи
    # блоках и двух опорных точках. Взят ПЕРВЫЙ рычаг канон-порядка починки
    # (`07-verstka/DOK.md` §4 — «блок-гэп → …»): промежуток между блоками 26→22px,
    # шесть промежутков дают 24px, чего хватает. Кегль 35px и межстрочье не
    # тронуты, SPLIT не понадобился.
    "s52": {"css": [".copy{--blok:22px}"]},
}

# ── СТУПЕНИ ПЛОТНОСТИ ──────────────────────────────────────────────────────────
# Порядок починки переполнения задан каноном (`07-verstka/DOK.md` §4): блок-гэп →
# отступ формулы → перераспределение grid-rows → и ТОЛЬКО в конце фиттер; «не влезло
# после этого → SPLIT». Фиттера у тела нет по построению (`--t-body` не фитится
# никогда), поэтому последним рычагом до SPLIT стоит МЕЖСТРОЧЬЕ — и это не костыль:
# у dandelin пер-слайдовое `line-height` от 1.26 до 1.40 стоит в живом коде
# (`shablon.html`, #s08/#s09/#s09p), то есть практика канона, а не изобретение.
# --t-body ни на одной ступени НЕ уменьшается: пол 35px держится кеглем ниже.
#
# ступень: (line-height, верх, низ, полоса, левое поле, потолок кегля, потолок полосы-илл.)
# Потолок кегля — это ВЫБОР кегля под объём (PRIMERY.md §2: «разброс 32–41px по деку —
# диапазон осознанного выбора, НЕ дрейф и не патч overflow»), и он жёстко стоит на 35:
# ниже пола audit.py ни одна ступень не спускается, сколько бы их ни добавить.
STUPENI = [
    (None, 38, 32, 344, 56, None, 430),   # 0 — токенное межстрочье 1.5278, поля щедрые
    (1.44, 32, 26, 344, 56, None, 400),   # 1
    (1.38, 28, 22, 328, 52, 38, 360),     # 2
    (1.32, 24, 20, 312, 48, 37, 330),     # 3
    (1.26, 20, 16, 300, 44, 35, 300),     # 4
    (1.24, 16, 12, 288, 40, 35, 276),     # 5
    (1.24, 16, 12, 244, 40, 35, 260),     # 6 — полоса сужается до 17%W;
                                          #     кегль и межстрочье НЕ двигаются.
                                          #     дальше только SPLIT
]
PLOTNOST = SRC / "tools" / "plotnost.json"


def stupen(sid):
    try:
        import json
        return json.loads(PLOTNOST.read_text(encoding="utf-8")).get(sid, 0)
    except FileNotFoundError:
        return 0


# ── кегль тела: ВЫБОР под объём слайда, не патч переполнения (PRIMERY.md §2). ──
# Пол — 35px (audit.py FLOOR_PX), ниже не опускается нигде и никогда.
def kegl(chars):
    if chars <= 430:
        return 40
    if chars <= 560:
        return 38
    return 35


# ── data-scenes: ВЫЧИСЛЯЕТСЯ из content, а не выписывается руками ──
# Хук H6 прямо про это: «величина, обязанная совпадать с другой, должна
# порождаться, а не сверяться»; гейты G14/G15 ловят именно разъехавшуюся пару.
# Считаем максимум по всем статическим источникам сцены, как это делает признак
# G14: `{@k}` / `{@k|…}` / `{blur@k}` / `{fill@k}`.
SCENE_RE = re.compile(r"\{(?:@|blur@|fill@)(\d+)")


def scenes_of(sid):
    p = SRC / "content" / (sid + ".md")
    if not p.is_file():
        return 1
    nums = [int(n) for n in SCENE_RE.findall(p.read_text(encoding="utf-8"))]
    return max(nums) if nums else 1


def panel_box(fig, box_w, box_h, pad):
    """Белая панель под фигуру: вписать её пропорцию в полосу, не растягивая."""
    w, h = fig["w"] or 250, fig["h"] or 200
    aw = box_w - 2 * pad
    ah = aw * h / w
    if ah > box_h - 2 * pad:
        ah = box_h - 2 * pad
        aw = ah * w / h
    return round(aw), round(ah)


def build(slides):
    ids = ["s%02d" % (i + 1) for i in range(len(slides))]
    html_files, css_parts, stats, levels = {}, [], [], {}

    for sid, s in zip(ids, slides):
        arch = archetype(s)
        chars = visible_chars(s["text"])
        st = PRAVKI.get(sid, {}).get("stupen", stupen(sid))
        lh, r_top, r_bot, r_rail, r_left, r_cap, r_board = STUPENI[min(st, len(STUPENI) - 1)]
        tb = PRAVKI.get(sid, {}).get("t-body", kegl(chars))
        if r_cap:
            tb = min(tb, r_cap)
        ills = ill_names(sid, s)
        css = ["#%s{--t-body:%dpx%s}"
               % (sid, tb, (";--lh:%s" % lh) if lh else "")]
        zones = []

        if arch == "рейка-справа":
            rail = PRAVKI.get(sid, {}).get("rail", r_rail)
            left, gap, top, bot = r_left, 24, r_top, r_bot
            text_w = W - left - gap - rail
            css.append("#%s .grid{position:absolute;inset:0;display:grid;"
                       "grid-template-columns:%dpx %dpx %dpx %dpx;"
                       "grid-template-rows:%dpx minmax(0,1fr) %dpx}"
                       % (sid, left, text_w, gap, rail, top, bot))
            css.append("#%s .copy{grid-area:2/2}" % sid)
            css.append("#%s .rail{grid-area:1/4/4/5;background:var(--board);"
                       "position:relative}" % sid)
            panels = []
            n = max(1, len(ills))
            slot_h = (H - 2 * 26 - (n - 1) * 22) / n
            y = 26.0
            for k, nm in enumerate(ills):
                fig = s["figures"][k] if k < len(s["figures"]) else {"w": 250, "h": 310}
                pw, ph = panel_box(fig, rail, slot_h, 22)
                cy = y + (slot_h - ph) / 2
                css.append("#%s .p%d{position:absolute;left:%dpx;top:%dpx;"
                           "width:%dpx;height:%dpx}"
                           % (sid, k + 1, round((rail - pw) / 2), round(cy), pw, ph))
                panels.append('      <div class="panel p%d ill-box" data-ill="%s"></div>'
                              % (k + 1, nm))
                y += slot_h + 22
            zones = ['    <div class="zone copy t-body">{{MD:%s}}</div>' % sid,
                     '    <div class="rail">', *panels, '    </div>']

        elif arch == "доска-пустая":
            stripe = PRAVKI.get(sid, {}).get("stripe", 116)
            left, gap, top, bot = r_left, 28, r_top, r_bot
            text_w = W - left - gap - stripe
            css.append("#%s .grid{position:absolute;inset:0;display:grid;"
                       "grid-template-columns:%dpx %dpx %dpx %dpx;"
                       "grid-template-rows:%dpx minmax(0,1fr) %dpx}"
                       % (sid, left, text_w, gap, stripe, top, bot))
            css.append("#%s .copy{grid-area:2/2}" % sid)
            css.append("#%s .rail{grid-area:1/4/4/5;background:var(--board)}" % sid)
            zones = ['    <div class="zone copy t-body">{{MD:%s}}</div>' % sid,
                     '    <div class="rail"></div>']

        elif arch == "илл-полосой-снизу":
            left, top, bot, gap = r_left, r_top, r_bot + 2, 22
            text_w = W - 2 * left
            fig = s["figures"][0] if s["figures"] else {"w": 620, "h": 160}
            board_h = PRAVKI.get(sid, {}).get("board", None)
            if board_h is None:
                board_h = min(r_board, max(200, round(0.78 * text_w * (fig["h"] or 160) / (fig["w"] or 620)) + 48))
            text_h = H - top - bot - gap - board_h
            css.append("#%s .grid{position:absolute;inset:0;display:grid;"
                       "grid-template-columns:%dpx %dpx %dpx;"
                       "grid-template-rows:%dpx minmax(0,1fr) %dpx %dpx %dpx}"
                       % (sid, left, text_w, left, top, gap, board_h, bot))
            css.append("#%s .copy{grid-area:2/2}" % sid)
            css.append("#%s .board{grid-area:4/2;background:var(--board);"
                       "position:relative;display:grid;place-items:center}" % sid)
            pw, ph = panel_box(fig, text_w, board_h, 24)
            css.append("#%s .p1{width:%dpx;height:%dpx}" % (sid, pw, ph))
            zones = ['    <div class="zone copy t-body">{{MD:%s}}</div>' % sid,
                     '    <div class="board">',
                     '      <div class="panel p1 ill-box" data-ill="%s"></div>' % ills[0],
                     '    </div>']
            stats.append((sid, arch, chars, tb, text_h))

        else:  # лестница-во-всю-ширину
            # Пометка ленты у этого слайда двойная: «лестница тождеств крупно НА
            # ВСЮ ШИРИНУ; правая полоса ПУСТАЯ». Первый прогон исполнил только
            # первую половину — доски не было вовсе, и слайд выпадал из ритма семи
            # своих соседей по «пустой полосе» (нашёл свежий верификатор). Полоса
            # возвращена той же шириной 116px, лестница по-прежнему в две колонки.
            stripe = PRAVKI.get(sid, {}).get("stripe", 116)
            left, gap, top, bot = r_left, 28, r_top, r_bot + 2
            text_w = W - left - gap - stripe
            css.append("#%s .grid{position:absolute;inset:0;display:grid;"
                       "grid-template-columns:%dpx %dpx %dpx %dpx;"
                       "grid-template-rows:%dpx minmax(0,1fr) %dpx}"
                       % (sid, left, text_w, gap, stripe, top, bot))
            css.append("#%s .copy{grid-area:2/2}" % sid)
            css.append("#%s .rail{grid-area:1/4/4/5;background:var(--board)}" % sid)
            # лестница тождеств: список в две колонки, иначе семь формул уезжают в подвал
            css.append("#%s .copy ul.tlist{column-count:2;column-gap:56px}" % sid)
            zones = ['    <div class="zone copy t-body">{{MD:%s}}</div>' % sid,
                     '    <div class="rail"></div>']

        for extra in PRAVKI.get(sid, {}).get("css", []):
            css.append("#%s %s" % (sid, extra))

        html_files[sid] = ('<section class="slide" id="%s" data-scenes="%d">\n'
                           '  <div class="grid">\n%s\n  </div>\n</section>\n'
                           % (sid, scenes_of(sid), "\n".join(zones)))
        css_parts.append("\n".join(css))
        if arch != "илл-полосой-снизу":
            stats.append((sid, arch, chars, tb, None))
        levels[sid] = st

    return ids, html_files, css_parts, stats, levels


def ill_names(sid, s):
    """Имена иллюстраций слайда — ровно те, что порождает porodit.py."""
    names = []
    for k in range(len(s["figures"])):
        nm = "%s-%s" % (sid, slug(s["title"]))
        if len(s["figures"]) > 1:
            nm += "-%d" % (k + 1)
        names.append(nm)
    for p in s["portraits"]:
        for pm in re.finditer(r"Портрет ([^{·]+)\{(\d+)\}", p):
            names.append("portret-%s-%s" % (pm.group(2), slug(pm.group(1).strip(), 24)))
    return names


MARK_CSS_A = "/* ---------- ПОРОЖДЁННЫЕ пер-слайдовые гриды (sverstat.py) ---------- */"
MARK_CSS_B = "/* ---------- конец порождённых гридов ---------- */"
MARK_SL_A = "<!-- ===== ПОРОЖДЁННЫЙ поток слайдов (sverstat.py) ===== -->"
MARK_SL_B = "<!-- ===== конец потока слайдов ===== -->"
MARK_AS_A = "<!-- ===== ПОРОЖДЁННЫЙ реестр иллюстраций (sverstat.py) ===== -->"
MARK_AS_B = "<!-- ===== конец реестра иллюстраций ===== -->"


def splice(text, a, b, payload):
    """Заменить участок между маркерами; маркеров нет — вставить их по месту."""
    if a in text and b in text:
        i, j = text.index(a) + len(a), text.index(b)
        return text[:i] + "\n" + payload + "\n" + text[j:]
    raise SystemExit("нет маркеров %r / %r в shablon.html" % (a, b))


def main():
    slides = load_all()[1:]                     # [0] — обложка, служебный слой
    ids, html_files, css_parts, stats, levels = build(slides)

    (SRC / "slides").mkdir(exist_ok=True)
    for old in (SRC / "slides").glob("*"):
        old.unlink()
    for sid in ids:
        (SRC / "slides" / (sid + ".html")).write_text(html_files[sid], encoding="utf-8")

    ill_files = sorted(p.stem for p in (SRC / "illustrations").glob("*"))
    templates = "\n".join('<template id="ill-%s">{{ILL:%s}}</template>' % (n, n)
                          for n in ill_files)
    flow = "\n".join("{{SLIDE:%s}}" % s for s in ids)

    sh = (SRC / "shablon.html").read_text(encoding="utf-8")
    sh = splice(sh, MARK_CSS_A, MARK_CSS_B, "\n".join(css_parts))
    sh = splice(sh, MARK_SL_A, MARK_SL_B, flow)
    sh = splice(sh, MARK_AS_A, MARK_AS_B, templates)
    (SRC / "shablon.html").write_text(sh, encoding="utf-8")

    brief = (SRC / "brief.md").read_text(encoding="utf-8")
    order = "slide_order:\n" + "\n".join("  - %s" % s for s in ids)
    brief = re.sub(r"^slide_order:(?:\n  - .*)*", order, brief, count=1, flags=re.M)
    (SRC / "brief.md").write_text(brief, encoding="utf-8")

    from collections import Counter
    print("слайдов: %d · шаблонов илл.: %d · slide_order: %d"
          % (len(ids), len(ill_files), len(ids)))
    print("архетипы:", dict(Counter(s[1] for s in stats)))
    print("кегли:", dict(sorted(Counter(s[3] for s in stats).items(), reverse=True)))
    print("минимум кегля по деку: %dpx (пол audit.py — 35px)" % min(s[3] for s in stats))
    from collections import Counter as _C
    print("ступени плотности:", dict(sorted(_C(levels.values()).items())))
    sc = {s: scenes_of(s) for s in ids if scenes_of(s) > 1}
    print("data-scenes>1 (вычислено из content): %s" % sc)
    print("ручных правок по глазам (PRAVKI): %d" % len(PRAVKI))
    return 0


if __name__ == "__main__":
    sys.exit(main())
