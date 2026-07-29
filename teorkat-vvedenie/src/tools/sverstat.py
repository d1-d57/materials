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
from porodit import (load_all, archetype, visible_chars, slug,   # один источник разбора ленты
                     scen_count, chars_by_scene)                 # и семантики сцен

SRC = Path(__file__).resolve().parents[1]
W, H = 1440, 810

# ── ручная доводка по PNG (шаг 6). Ключ — id, значения перекрывают расчёт. ──
# Каждая строка — результат просмотра снятого кадра, а не догадка.
PRAVKI = {
    # ПЕРЕНЕСЕНО ПО КАРТЕ (`karta.py`): запись стояла на старом `s52` «Стоун:
    # конечный случай полностью», а он вошёл в новый `s30` («Стоун: конечный случай
    # и общий», s52+s53). Оставить ключ «s52» значило бы навести оплаченную глазами
    # правку на «Стоун в общем виде» — другой слайд.
    # Почему правка вообще есть: единственный слайд старого дека, которому не хватило
    # всей лестницы — промер давал +15px, треть строки, при семи блоках и двух опорных
    # точках. Взят ПЕРВЫЙ рычаг канон-порядка починки (`07-verstka/DOK.md` §4:
    # «блок-гэп → …»): промежуток между блоками 26→22px, шесть промежутков дают 24px.
    # Кегль и межстрочье не тронуты, SPLIT не понадобился.
    # 🔴 СНЯТО 29.07 (заход kod_podgonka.md): слайда `s30` в деке НЕТ — после реза и
    # двух перекомпоновок их 29. Запись висела на несуществующем id и молча не
    # применялась ни к чему.
    # "s30": {"css": [".copy{--blok:22px}"]},
    # s17 «Как доказывают, что функтора нет» — самый плотный слайд дека:
    # 25 абзацев, 7 опорных точек, 5 сцен. На последней ступени промер даёт
    # +3px — десятая доля строки. Тот же ПЕРВЫЙ рычаг канон-порядка, что
    # спас старый s52: промежуток блоков 26→22px. Кегль (35px), межстрочье
    # и число сцен не тронуты; SPLIT не понадобился (и запрещён — у захода
    # обратная задача).
    # 🔴 СНЯТО 29.07 (заход kod_podgonka.md): id уцелел, а СЛАЙД под ним другой.
    # Комментарий выше описывает «25 абзацев, 7 опорных точек, 5 сцен»; сегодняшний
    # `s17` — «Ответ снова „ни одного“», 884 знака, 2 сцены. Ручная правка,
    # оплаченная глазами на старом слайде, была наведена на чужой — а гейт этого не
    # видит: ключ существует, css применяется, дек зелёный.
    # "s17": {"css": [".copy{--blok:22px}"]},

    # s04 «Примеры видов» — единственный слайд, где переполнение видно ГЛАЗАМИ, а не
    # только промером: на кадре `s04-c2` строка «деревья и корневые деревья;» разрезана
    # доской пополам, а два пункта за ней («графы», «инъекции») не видны вовсе.
    # Причина не в кегле и не в ступени (она уже 6, максимум): это ОДИН блок `<ul>` из
    # 11 пунктов — перетекание по сценам его не делит по построению, а зона под ним
    # 498px против нужных 788px.
    # Взят канон-шаг 3 (`07-verstka/DOK.md` §4, перераспределение) в форме, уже живущей
    # в этом же файле: архетип «лестница-во-всю-ширину» ставит длинному списку
    # `column-count:2` (строка ~392, «иначе семь формул уезжают в подвал»). Здесь та же
    # болезнь и то же лекарство. Кегль (35px), межстрочье и доска с двумя картинками не
    # тронуты; SPLIT не понадобился.
    # Две колонки сняли 141px из 290 — не хватило. Доска у слайда широкая и низкая по
    # природе (галерея видов — фигура с h/w < 0.6), поэтому 260→190px её не ломает, а
    # тексту отдаёт 70px; остаток снимает первый рычаг канон-порядка (блок-гэп 26→22px).
    "s04": {"board": 116, "css": [".copy ul{column-count:2;column-gap:56px}",
                                  ".copy{--blok:22px}"]},

    # «Брауэр в работе»: доска на 3 панели держит 260px, тексту не хватает 111px.
    # Та же доска, тот же ход — панели там квадратные, 190px их поджимает, но читаются
    # (проверено кадром s15-c1: панели занимают ~180px из 260 по высоте).
    # 🔴 ПЕРЕКЛЮЧЕНО s15→s14 29.07 (заход kod_chistka.md): слияние «Функторы» +
    # «Зоопарк функторов» убрало один раздел блока B, и ВСЕ id после B съехали на −1.
    # Ключ «s15» стал наводить оплаченную глазами правку на «Откуда взялся этот язык»,
    # а «Брауэр» остался без неё и переполнился на +351px. Слайд опознан по названию
    # (`porodit.py`: s14 = C «Брауэр в работе»), а не по позиции ключа.
    "s14": {"board": 164, "css": [".copy{--blok:22px}"]},

    # s05: не хватает 11px — треть строки. Только блок-гэп, ничего больше.
    "s05": {"css": [".copy{--blok:22px}"]},
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
RITM = SRC / "tools" / "ritm.json"
POTOK = SRC / "tools" / "reflow.json"


def potok(sid):
    """Нужно ли слайду перетекание по сценам (отступление от «никогда display»).

    Список ведёт `podognat.py --potok`: слайд попадает в него ТОЛЬКО если при
    замороженной геометрии его зона переполнена, то есть весь текст слайда
    физически не влезает разом. Остальные слайды держат канон дословно.
    """
    try:
        import json
        return sid in set(json.loads(POTOK.read_text(encoding="utf-8")))
    except FileNotFoundError:
        return False


def ritm(sid):
    """Промежуток между абзацами, пер-слайдово. База дека — 26px, и это НЕ
    эстетический выбор, а лечение переполнения: канонный ритм = полная пустая строка
    (58px при кегле 38). Сжатие текста освободило место, и `podognat.py
    --minimizirovat` возвращает ритм обратно к 58px там, где он влезает, — это
    первый рычаг в заходном порядке отдачи места, раньше ступени и раньше кегля."""
    try:
        import json
        return json.loads(RITM.read_text(encoding="utf-8")).get(sid, 26)
    except FileNotFoundError:
        return 26

# ── КАРТИНКА ПО СЦЕНАМ: сменный ярус (заход, шаг 3¾, «образец 2») ──────────────
# Склейка приносит на слайд по картинке от каждого вошедшего старого слайда — до пяти
# (s13). Стопка из пяти панелей в рейке 344px даёт каждой ~140px: нечитаемо, и при
# этом четыре из пяти в любой момент не к месту. Лента просит другого и просит прямо,
# указывая сцену КАЖДОЙ картинке: «по картинке на сцену: нерастягивающее отображение
# (1), раскраска как гомоморфизм (2), отношение против диагонали (3), кобордизм и
# тангл (4)». Это и есть сменный ярус: одно место, содержимое меняется.
#
# Поэтому сцена картинки НЕ выдумывается вёрсткой, а читается из пометки ленты
# (`07-verstka/DOK.md`: «арка 7 реализует принятую раскладку, а не выбирает её»).
# Разбор прозы, однако, доверия не заслуживает молча: у s13 четыре аннотации на пять
# фигур («кобордизм и тангл» — одна аннотация на две картинки), у s16 порядок
# аннотаций обратен порядку файлов (сначала портрет, потом фигура), у s18 первая
# картинка объявлена словами «на сцене 1», а не «(1)». Поэтому правило такое:
#   · аннотаций РОВНО столько же, сколько картинок → берём их;
#   · иначе → берём запись из KARTINKI ниже, каждая с цитатой из ленты;
#   · нет ни того, ни другого → стопка с первой сцены, то есть поведение старого
#     дека (класс A так и остаётся байт-в-байт: у него картинок 0, 1 или 2).
# Разрешённое назначение печатается по каждому слайду вместе с ИСТОЧНИКОМ — ни одна
# картинка не встаёт на сцену молча.
ANN_RE = re.compile(r"\((\d+)(?:[–—-](\d+))?\)")

KARTINKI = {
    # «по картинке на сцену: нерастягивающее (1), раскраска как гомоморфизм (2),
    #  отношение против диагонали (3), кобордизм и тангл (4)» — аннотаций 4 на 5
    #  фигур: последняя покрывает ДВЕ картинки, они стоят на сцене 4 вместе.
    "s13": [(1, 1), (2, 2), (3, 3), (4, None), (4, None)],
    # «портрет Фробениуса (1), два функтора навстречу друг другу (2–3)» — порядок
    #  аннотаций обратен порядку файлов: фигура у нас первая, портрет второй.
    "s16": [(2, 3), (1, 1)],
    # «на сцене 1 согласованность с отображениями целиком, дальше окружность в диске
    #  (2) и луч внутри диска с портретом (3)» — первая картинка объявлена словами,
    #  а портрет Брауэра идёт вместе с лучом, то есть тоже на сцене 3.
    "s18": [(1, 1), (2, 2), (3, None), (3, None)],
}


def kartinki_po_scenam(sid, n_ill, n_sc, layout):
    """[(от, до|None)] на каждую картинку + источник решения."""
    if sid in KARTINKI and len(KARTINKI[sid]) == n_ill:
        return KARTINKI[sid], "таблица"
    ann = ANN_RE.findall(layout or "")
    if ann and len(ann) == n_ill:
        # Одиночное «(N)» при ДВУХ И БОЛЕЕ аннотациях читается как «на сцене N», а не
        # «с N и до конца»: лента вводит эти пометки словами «ПО КАРТИНКЕ НА СЦЕНУ»
        # (s13, s17) и перечисляет разные картинки для разных сцен. Прочитанное как
        # «с N и далее», это накопило бы все картинки одновременно — то есть вернуло
        # стопку из пяти панелей по 140px, ровно то, от чего лента уходит.
        # При ЕДИНСТВЕННОЙ аннотации так читать нельзя (одна картинка слайда никуда
        # не уходит), поэтому там оставляем открытый конец.
        zakryt = len(ann) >= 2
        return ([(int(a), int(b) if b else (int(a) if zakryt else None))
                 for a, b in ann]), "пометка ленты"
    return [(1, None)] * n_ill, "стопка с 1-й сцены"


def slots(intervals, n_sc):
    """Раскладка интервалов по слотам: интервалы, не пересекающиеся по сценам, живут
    в ОДНОМ месте (сменный ярус); пересекающиеся получают разные слоты. Число слотов
    = максимальное число картинок, видимых ОДНОВРЕМЕННО, — а не число картинок."""
    def vidno(iv, k):
        f, u = iv
        return f <= k and (u is None or k <= u)
    zanyato = []            # список слотов, каждый — список индексов картинок
    for i, iv in enumerate(intervals):
        for sl in zanyato:
            if not any(vidno(intervals[j], k) and vidno(iv, k)
                       for j in sl for k in range(1, n_sc + 1)):
                sl.append(i)
                break
        else:
            zanyato.append([i])
    return zanyato


def scene_attrs(iv):
    f, u = iv
    a = (' data-scene-from="%d"' % f) if f > 1 or u is not None else ""
    b = (' data-scene-until="%d"' % u) if u is not None else ""
    return a + b


def stupen(sid):
    try:
        import json
        return json.loads(PLOTNOST.read_text(encoding="utf-8")).get(sid, 0)
    except FileNotFoundError:
        return 0


# ── кегль тела: ВЫБОР под объём слайда, не патч переполнения (PRIMERY.md §2). ──
# Пол — 35px (audit.py FLOOR_PX), ниже не опускается нигде и никогда.
#
# 🔴 `chars` здесь — знаки САМОГО ТЯЖЁЛОГО КАДРА, а не всего текста слайда, и это
# не уточнение, а разница между читаемым деком и нечитаемым. По новой ленте
# `porodit.py --inventar` печатает: медиана слайда 980 знаков, медиана тяжёлого
# кадра 526. По слайду все 32 получили бы 35px — пол, — под текст, которого зал
# никогда не видит одновременно: часть его приходит и уходит по кликам. По кадру
# медианный слайд встаёт на штатные 38px. Заход назвал это провалом захода прямо:
# «если сдашь дек, где кегль опущен под невидимый текст, — заход провален».
def kegl(chars):
    if chars <= 430:
        return 40
    if chars <= 560:
        return 38
    return 35


# ── data-scenes: ВЫЧИСЛЯЕТСЯ из content, а не выписывается руками ──
# Хук H6 прямо про это: «величина, обязанная совпадать с другой, должна
# порождаться, а не сверяться»; гейты G14/G15 ловят именно разъехавшуюся пару.
#
# 🔴 Прежний счётчик читал регексом `\{(?:@|blur@|fill@)(\d+)` — то есть только
# ГРАНИЦУ ПРИХОДА. На деке без замены это было верно; на ленте со заменой — нет:
# слайд с одним `{@1-3}` объявлял бы ОДНУ сцену вместо трёх, а `{@-2}` регекс не
# видит вовсе (после `@` стоит минус, а не цифра). Число сцен считается теперь по
# интервалам видимости — `porodit.scen_count`, единственный дом этой семантики,
# тот же, по которому мерится тяжесть кадра.
SCENE_RE = re.compile(r"\{(?:blur@|fill@)(\d+)")


def scenes_of(sid):
    p = SRC / "content" / (sid + ".md")
    if not p.is_file():
        return 1
    txt = p.read_text(encoding="utf-8")
    nums = [int(n) for n in SCENE_RE.findall(txt)]
    return max([scen_count(txt)] + nums)


def kadry_of(sid):
    """Знаки по сценам слайда: [видно на сцене 1, на сцене 2, …]."""
    p = SRC / "content" / (sid + ".md")
    if not p.is_file():
        return [0]
    return chars_by_scene(p.read_text(encoding="utf-8"))


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
    html_files, css_parts, stats, levels, kart = {}, [], [], {}, {}

    for sid, s in zip(ids, slides):
        arch = archetype(s)
        chars = s["tyazh"]                  # знаки ТЯЖЁЛОГО КАДРА, не всего слайда
        vsego = visible_chars(s["text"])    # весь текст — только для отчёта
        st = PRAVKI.get(sid, {}).get("stupen", stupen(sid))
        lh, r_top, r_bot, r_rail, r_left, r_cap, r_board = STUPENI[min(st, len(STUPENI) - 1)]
        tb = PRAVKI.get(sid, {}).get("t-body", kegl(chars))
        if r_cap:
            tb = min(tb, r_cap)
        ills = ill_names(sid, s)
        nsc = scenes_of(sid)
        intervals, istochnik = kartinki_po_scenam(sid, len(ills), nsc, s["layout"])
        css = ["#%s{--t-body:%dpx%s}"
               % (sid, tb, (";--lh:%s" % lh) if lh else "")]
        rt = ritm(sid)
        if rt != 26:
            css.append("#%s .copy{--blok:%dpx}" % (sid, rt))
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
            zan = slots(intervals, nsc)
            n = max(1, len(zan))
            slot_h = (H - 2 * 26 - (n - 1) * 22) / n
            for si, sl in enumerate(zan):
                y = 26.0 + si * (slot_h + 22)
                for k in sl:
                    fig = (s["figures"][k] if k < len(s["figures"])
                           else {"w": 250, "h": 310})
                    pw, ph = panel_box(fig, rail, slot_h, 22)
                    cy = y + (slot_h - ph) / 2
                    css.append("#%s .p%d{position:absolute;left:%dpx;top:%dpx;"
                               "width:%dpx;height:%dpx}"
                               % (sid, k + 1, round((rail - pw) / 2), round(cy), pw, ph))
                    panels.append('      <div class="panel p%d ill-box" '
                                  'data-ill="%s"%s></div>'
                                  % (k + 1, ills[k], scene_attrs(intervals[k])))
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
                       "position:relative}" % sid)
            # 🔴 Доска кладёт ВСЕ свои картинки, а не только первую. Прежняя версия
            # брала `ills[0]` — на деке из 55 слайдов у такого слайда картинка и была
            # одна, а после склейки их четыре (s18: три фигуры + портрет Брауэра), и
            # три уезжали в сироты: файл на диске есть, `data-ill` на него нет.
            # Линтер это ловит мягким предупреждением, которое легко проехать.
            zan = slots(intervals, nsc)
            cols = max(1, len(zan))
            panels = []
            for si, sl in enumerate(zan):
                bw = (text_w - 24 * (cols - 1)) / cols
                for k in sl:
                    f = s["figures"][k] if k < len(s["figures"]) else {"w": 620, "h": 160}
                    pw, ph = panel_box(f, bw, board_h, 24)
                    css.append("#%s .p%d{position:absolute;left:%dpx;top:%dpx;"
                               "width:%dpx;height:%dpx}"
                               % (sid, k + 1,
                                  round(si * (bw + 24) + (bw - pw) / 2),
                                  round((board_h - ph) / 2), pw, ph))
                    panels.append('      <div class="panel p%d ill-box" '
                                  'data-ill="%s"%s></div>'
                                  % (k + 1, ills[k], scene_attrs(intervals[k])))
            zones = ['    <div class="zone copy t-body">{{MD:%s}}</div>' % sid,
                     '    <div class="board">', *panels, '    </div>']
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

        flow_attr = ' data-flow="reflow"' if potok(sid) else ""
        html_files[sid] = ('<section class="slide" id="%s" data-scenes="%d"%s>\n'
                           '  <div class="grid">\n%s\n  </div>\n</section>\n'
                           % (sid, nsc, flow_attr, "\n".join(zones)))
        css_parts.append("\n".join(css))
        if arch != "илл-полосой-снизу":
            stats.append((sid, arch, chars, tb, None))
        levels[sid] = st
        kart[sid] = (istochnik, intervals, len(slots(intervals, nsc)), vsego)

    return ids, html_files, css_parts, stats, levels, kart


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


# ── СЛУЖЕБНЫЕ СЛАЙДЫ И РАЗДЕЛИТЕЛИ (заход, шаг 6) ─────────────────────────────
# ⚠ Это ОСОЗНАННОЕ отступление от гейта G12, разрешённое владельцем 29.07: генератор
# служебные слайды НЕ порождает (`{{SLIDES}}`, `{{SLUZHEBNYE_CSS}}`,
# `_generator/skeleton/sluzhebnye/` в живом коде не существуют — проверено заходом
# вёрстки и перепроверено мной: `ls _generator/skeleton/` даёт 10 записей, папки
# `sluzhebnye/` среди них нет). Поэтому они свёрстаны здесь, а не руками в `slides/`:
# выход `slides/` перезаписывается каждым прогоном, и рукописный файл потерялся бы.
# Долг генератора остаётся долгом генератора; `_generator/` не тронут.
#
# Разметка — по живому образцу буффона (`buffon/src/slides/{sl-title,sl-thanks,
# sl-divider1}.html` и его гриды в `shablon.html`), а не изобретена.
#
# АКТЫ приняты владельцем 28.07 — принято ЧЕТЫРЕ акта и три разделителя, и это не
# переоткрывается. РАЗМЕРЫ актов не решение, а следствие ленты: раньше здесь стояло
# `[9, 7, 8, 8] = 32`, вписанное руками, и 29.07 рез состава (PRAVKI §СОСТАВ снял три
# раздела) сделал сборку неисполнимой — `SystemExit: акты покрывают 32 слайдов, а их 29`.
# Поэтому размеры СЧИТАЮТСЯ из блоков ленты (KONSTITUCIYA §10: не число, а то, что его
# считает). Акт ↔ блоки: 1=A, 2=B, 3=C+D (две половины «Чего не бывает»), 4=E.
# ⛔ Картинок на разделителях нет: владелец хочет туда изображения, но это арка 9 и
# отдельный заход (прямая граница шага 6).
AKT_BLOKI = [("A",), ("B",), ("C", "D"), ("E",)]


def akty(slides):
    """Размеры актов — счётом по блокам ленты, а не константой."""
    sizes = [sum(1 for s in slides if s["block"] in blks) for blks in AKT_BLOKI]
    lost = [s["block"] for s in slides if not any(s["block"] in b for b in AKT_BLOKI)]
    if lost:
        raise SystemExit("блоки ленты вне карты актов: %s — назовите их в AKT_BLOKI"
                         % sorted(set(lost)))
    return sizes
RAZDELITELI = ["Зоопарк", "Чего не бывает", "Словарь между мирами"]

# Обложка — РОВНО три строки, как задал заход, без подзаголовков и без места
# (`07-verstka/DOK.md`: «обложка — без несогласованных подписей»; `cover_place` в
# брифе не заполнено). Расхождения с полями `brief.md` названы в отчёте, не молча.
COVER = ["Зачем нужны категории", "Formal Labs", "29.07.26"]


def sluzhebnye():
    """{id: (html, css)} — обложка, три разделителя, финал."""
    out = {}
    out["sl-title"] = (
        '<section class="slide" id="sl-title" data-scenes="1">\n'
        '  <div class="grid">\n'
        '    <div class="zone head t-display">%s</div>\n'
        '    <div class="zone sub">%s</div>\n'
        '    <div class="zone date">%s</div>\n'
        '  </div>\n</section>\n' % tuple(COVER),
        "#sl-title .grid{position:absolute;inset:0;display:grid;"
        "grid-template-columns:96px 1fr 96px;"
        "grid-template-rows:1fr auto 28px auto 12px auto 1fr}\n"
        # text-align:left — потому что `.t-display` в базе центрирует, и на снятом
        # кадре заголовок стоял по центру, а «Formal Labs» и дата — по левому краю:
        # три строки обложки разъезжались по двум разным осям. Поймано глазом.
        "#sl-title .head{grid-area:2/2;font-size:76px;line-height:1.12;text-align:left}\n"
        "#sl-title .sub{grid-area:4/2;font-family:'Forum',serif;"
        "text-transform:uppercase;letter-spacing:.12em;font-size:30px;color:var(--steel)}\n"
        "#sl-title .date{grid-area:6/2;font-size:26px;color:var(--steel)}")
    for i, txt in enumerate(RAZDELITELI, start=1):
        sid = "sl-divider%d" % i
        out[sid] = (
            '<section class="slide" id="%s" data-scenes="1">\n'
            '  <div class="grid">\n'
            '    <div class="zone head t-display">%s</div>\n'
            '  </div>\n</section>\n' % (sid, txt),
            "#%s{background:var(--board)}\n"
            "#%s .grid{position:absolute;inset:0;display:grid;"
            "grid-template-columns:96px 1fr 96px;grid-template-rows:1fr auto 1fr}\n"
            "#%s .head{grid-area:2/2;font-size:72px;line-height:1.14}" % (sid, sid, sid))
    out["sl-thanks"] = (
        '<section class="slide" id="sl-thanks" data-scenes="1">\n'
        '  <div class="grid">\n'
        '    <div class="zone head t-display">Спасибо за внимание</div>\n'
        '  </div>\n</section>\n',
        "#sl-thanks{background:var(--board)}\n"
        "#sl-thanks .grid{position:absolute;inset:0;display:grid;place-items:center}\n"
        "#sl-thanks .head{font-size:72px}")
    return out


def poryadok(ids, slides):
    """Поток слайдов: обложка · акт 1 · разделитель · акт 2 · … · финал."""
    AKTY = akty(slides)
    flow, i = ["sl-title"], 0
    for a, n in enumerate(AKTY):
        if a:
            flow.append("sl-divider%d" % a)
        flow.extend(ids[i:i + n])
        i += n
    if i != len(ids):
        raise SystemExit("акты %s покрывают %d слайдов, а их %d" % (AKTY, i, len(ids)))
    flow.append("sl-thanks")
    return flow


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
    ids, html_files, css_parts, stats, levels, kart = build(slides)

    (SRC / "slides").mkdir(exist_ok=True)
    for old in (SRC / "slides").glob("*"):
        old.unlink()
    for sid in ids:
        (SRC / "slides" / (sid + ".html")).write_text(html_files[sid], encoding="utf-8")

    # служебные слайды и разделители: тот же порождаемый слой, не рукописные файлы
    sluzh = sluzhebnye()
    for sid, (html, _css) in sluzh.items():
        (SRC / "slides" / (sid + ".html")).write_text(html, encoding="utf-8")
    css_parts.extend(css for _h, css in sluzh.values())
    poryadok_ids = poryadok(ids, slides)

    ill_files = sorted(p.stem for p in (SRC / "illustrations").glob("*"))
    templates = "\n".join('<template id="ill-%s">{{ILL:%s}}</template>' % (n, n)
                          for n in ill_files)
    flow = "\n".join("{{SLIDE:%s}}" % s for s in poryadok_ids)

    sh = (SRC / "shablon.html").read_text(encoding="utf-8")
    sh = splice(sh, MARK_CSS_A, MARK_CSS_B, "\n".join(css_parts))
    sh = splice(sh, MARK_SL_A, MARK_SL_B, flow)
    sh = splice(sh, MARK_AS_A, MARK_AS_B, templates)
    (SRC / "shablon.html").write_text(sh, encoding="utf-8")

    brief = (SRC / "brief.md").read_text(encoding="utf-8")
    order = "slide_order:\n" + "\n".join("  - %s" % s for s in poryadok_ids)
    brief = re.sub(r"^slide_order:(?:\n  - .*)*", order, brief, count=1, flags=re.M)
    (SRC / "brief.md").write_text(brief, encoding="utf-8")

    from collections import Counter
    print("содержательных слайдов: %d · служебных и разделителей: %d · "
          "ВСЕГО секций: %d · шаблонов илл.: %d"
          % (len(ids), len(sluzh), len(poryadok_ids), len(ill_files)))
    print("порядок: %s" % " ".join(poryadok_ids))
    print("архетипы:", dict(Counter(s[1] for s in stats)))
    print("кегли:", dict(sorted(Counter(s[3] for s in stats).items(), reverse=True)))
    print("минимум кегля по деку: %dpx (пол audit.py — 35px)" % min(s[3] for s in stats))
    from collections import Counter as _C
    print("ступени плотности:", dict(sorted(_C(levels.values()).items())))
    sc = {s: scenes_of(s) for s in ids if scenes_of(s) > 1}
    print("data-scenes>1 (вычислено из content): %s" % sc)
    print("ручных правок по глазам (PRAVKI): %d" % len(PRAVKI))
    from collections import Counter as _C3
    print("перетекание по сценам (отступление от канона): %d слайдов из %d — %s"
          % (sum(1 for s in ids if potok(s)), len(ids),
             " ".join(s for s in ids if potok(s)) or "нет"))
    print("блочный ритм по деку: %s (база дека 26px, канон 58px)"
          % dict(sorted(_C3(ritm(s) for s in ids).items())))

    # ни одна картинка не встаёт на сцену молча: печатается и назначение, и источник
    from collections import Counter as _C2
    print("картинок по сценам — источник решения: %s"
          % dict(_C2(v[0] for v in kart.values() if v[1])))
    smen = {k: v for k, v in kart.items() if v[1] and v[2] < len(v[1])}
    print("сменный ярус (картинок больше, чем слотов): %s"
          % {k: "%d карт. в %d слот." % (len(v[1]), v[2]) for k, v in smen.items()})
    for sid in sorted(kart):
        ist, iv, ns, _ = kart[sid]
        if iv and ist != "стопка с 1-й сцены":
            print("   %s [%s] слотов %d · %s" % (sid, ist, ns, iv))
    print("знаков: тяжёлый кадр медиана %d · весь слайд медиана %d (кегль считается по КАДРУ)"
          % (sorted(s[2] for s in stats)[len(stats) // 2],
             sorted(v[3] for v in kart.values())[len(kart) // 2]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
