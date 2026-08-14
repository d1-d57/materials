#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Реестр типов вёрстки — словарь Я1 (primitivy-verstki.md), восемь обязательных
типов этого захода. Имена БУКВАЛЬНО из словаря, где он их называет; где словаря нет
(«только текст») — заведён новый.

Каждый обработчик:
    handler(sid, p, text_html) -> (css: str, html: str)
  sid       — id слайда
  p         — параметры YAML-шапки (formaty.parse_slide)
  text_html — тело слайда, уже HTML (formaty.render_body)

`html` — содержимое `<section class="slide" id="<sid>">…</section>` (без обёртки
section — её ставит `slaid.py`/`deck.py`). `css` — грид и зоны, `#<sid> …{…}`.

🔴 Правило, ради которого всё делается (заход, Э1): вторая доля НЕ ЗАДАЁТСЯ отдельным
числом. `_split_css` пишет `calc(100% - <liniya>%)`, а не вычисленный в питоне второй
литерал — так `grep -nE "grid-template-(rows|columns): *[0-9.]+% +[0-9.]+%"` не
находит пары ДВУХ литералов (после первого `%` в CSS идёт `calc(`, не цифра), и
дефект «поправили один, забыли второй» становится структурно невыразимым, а не
просто отсутствующим сегодня.
"""

MAX_ILL = 3  # Я1 Э2: «не больше трёх, обычный максимум два»
ILL_GAP = 24
ILL_PAD = 28

# Общие архетипические правила — то же место, что `.board{background:var(--board);}`
# и `.pad{padding:…}` в dandelin/buffon (Я4): один раз на все типы, не дублируется
# в каждом handler'е. Подключается `slaid.py`/`deck.py` РЯДОМ с пер-слайдовым `css`.
GLOBAL_CSS = (
    ".zone.board{ background:var(--board); } "
    # ФОН ИЛЛЮСТРАЦИИ — ПРОЗРАЧНЫЙ (владелец, интервью 2026-08-14, заход
    # polya-i-uzor Э3, дословно): «фон иллюстрации должен быть прозрачен, сейчас
    # это зелёный прямоугольник и он перекрывает, разрезает паттерн». `.ill-row` —
    # класс, который `_ill_zone` ставит ТОЛЬКО контейнеру с реальной картинкой
    # (пустая полоса без иллюстраций — `<div class="zone board"></div>`, без
    # `ill-row` — этого правила не видит и остаётся закрашенной, как и раньше:
    # это не про иллюстрацию, её там нет). Три класса специфичностью (0,3,0)
    # осознанно перебивают `.zone.board` (0,2,0) выше — не порядок в файле.
    ".zone.board.ill-row{ background:none; } "
    # ВОЗДУХ — В ПРОМЕЖУТКИ МЕЖДУ БЛОКАМИ, А НЕ В ПОЛЯ (доводка Л2, Ф1б).
    # Владелец дословно: «дыхание должно быть не за счёт полей сверху и снизу, а
    # дыхание между блоками. Это сущностная вещь». Замерено на собранной Л2
    # (12 текстовых слайдов): солвер сажает текст в зону с запасом 100-150 px —
    # три лишние строки, и они висели ОДНИМ куском внизу зоны.
    # `space-between` отдаёт этот запас промежуткам сам, без числа: сколько солвер
    # оставил, столько и разойдётся по стыкам блоков. Числом это сделать нельзя —
    # запас у каждой карточки свой, а `--blok` считает солвер, и трогать его
    # запрещено заданием.
    # `flex:0 0 auto` детям — не украшение: в колоночном flex у детей
    # `flex-shrink:1` по умолчанию, и при тесной карточке абзацы СЖАЛИСЬ бы по
    # высоте, порвав текст внутри себя вместо честного переполнения, которое видит
    # солвер. Ноль сжатия = поведение зоны для солвера прежнее: не влезло — не
    # влезло.
    # Переполнение эта правка не создаёт: когда запаса нет, space-between не
    # добавляет ничего (лишнего места нет по определению).
    ".zone.copy{ padding:4px 18px 12px 18px; display:flex; flex-direction:column; "
    "justify-content:space-between; } "
    ".zone.copy > *{ flex:0 0 auto; } "
    # Заголовок слайда — РОЛЬ темы `frametitle`, а не своё число и свой цвет
    # (заход primenenie-vizuala, Ш1-Ш2). Цвет: `.sty:172` `\setbeamercolor{frametitle}
    # {fg=CTPlum,...}` и то же дословно в теле `\CTContentNode` (`.sty:372`) и в
    # fallback-шаблоне (`.sty:595`) — CTPlum, то есть `--accent`; чёрным заголовок
    # в теме не бывает нигде. Кегль/интерлиньяж: `.sty:183` 24/32pt → перенесённая
    # пара `--t-frametitle`/`--lh-frametitle` (76px/1.333) вместо прежних 44px/1.15.
    # УЗКИЙ вариант той же роли (20/28pt, `.sty:428,454`) тема включает НЕ по
    # переполнению, а по типу слайда — там, где сбоку или снизу иллюстрация;
    # у нас это `_zag_uzkij` на трёх типах ниже.
    ".zagolovok{ font-family:var(--font-display); text-transform:uppercase; "
    "font-size:var(--t-frametitle); line-height:var(--lh-frametitle); "
    "margin-bottom:4px; color:var(--accent); } "
    # ---- визитка: текст канона (sluzhebnye/vizitka.md) несёт {.bullets} и
    # <a class="tg-link">; правила дословно с sluzhebnye/style.css (заход
    # vizitka-i-oblozhka, В1) — без них render_body роняет карточку гейтом
    # «класс не найден в словаре скелета» (base.css + этот файл — весь словарь).
    ".bullets{ list-style:none; padding-left:32px; } "
    ".bullets li{ position:relative; } "
    ".bullets li::before{ content:''; position:absolute; left:-30px; top:.55em; "
    "width:9px; height:9px; border-radius:50%; background:var(--ink); } "
    ".tg-link{ color:inherit; text-decoration:none; cursor:pointer; }"
)


class TipVerstki(Exception):
    pass


def _esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _zagolovok_html(p):
    """🔴 Формулы в заголовке РЕНДЕРЯТСЯ, а не эскейпятся. Найдено глазами на
    собранной Л2: `zagolovok_na_ekrane: Изоморфизм $V$ и $V^*$` выводился на экран
    как «ИЗОМОРФИЗМ $V$ И $V^*$» — доллары и каретка буквально, при зелёных гейтах
    (никакой из них в заголовок не смотрит). Заголовок такого слайда продиктован
    владельцем именно с математикой, так что запретить формулу нельзя — надо её
    рендерить. Кэш формул кладёт сюда компилятор (`slaid.py`/`deck.py`) в
    `p['_math']`: второго рендерера не заводится, зовётся тот же
    `render_inline_md`, что и для тела. Кэша нет (служебные слайды, обложка) —
    старое поведение, эскейп."""
    z = p.get("zagolovok_na_ekrane")
    if not z:
        return ""
    math = p.get("_math")
    if math and "$" in z:
        from formaty import render_inline_md   # он же настраивает sys.path до _generator
        return '<div class="zagolovok">%s</div>' % render_inline_md(z, math, acc_tag="span")
    return '<div class="zagolovok">%s</div>' % _esc(z)


def _kegl_style(p):
    """Инлайновые CSS-переменные текстовой зоны — авторская ручка `kegl`
    (множитель token'а `--t-body`, как было) плюс три числа солвера (заход
    solver-vmeshcheniya, Э3): `kegl_px` (абсолютный кегль, замещает `kegl`),
    `mezhstrochye` (`--lh`), `otstup_bloka` (`--blok`). Солвер пишет ИМЕННО эти
    поля в карточку — они и есть найденное решение, применённое к вёрстке."""
    parts = []
    kegl_px = p.get("kegl_px")
    if kegl_px:
        parts.append("--t-body:%spx" % kegl_px)
    else:
        k = p.get("kegl")
        if k and float(k) != 1.0:
            parts.append("--t-body:calc(38px * %s)" % k)
    lh = p.get("mezhstrochye")
    if lh:
        parts.append("--lh:%s" % lh)
    blok = p.get("otstup_bloka")
    if blok:
        parts.append("--blok:%spx" % blok)
    if not parts:
        return ""
    return ' style="%s"' % ";".join(parts)


def _text_zone(sid, p, text_html, cls="copy"):
    return ('<div class="zone %s t-body"%s>%s%s</div>'
            % (cls, _kegl_style(p), _zagolovok_html(p), text_html))


def _ill_zone(ills, axis, cls="board", pad=None, pad_bottom=None):
    """axis: 'row' — бок о бок (для горизонтальной полосы, где полоса делится по
    ВЫСОТЕ и картинка занимает её по ШИРИНЕ); 'col' — стопкой (для вертикальной
    полосы, где картинка занимает зону по ВЫСОТЕ). Я1 Э2, правило дословно.

    🔴 `align-items:stretch` (дефолт flex, НЕ `center`) + `flex:1 1 0` на панели —
    это и есть «занимают целиком»: без них панель без явных width/height схлопывается
    в 0×0 (найдено этим же прогоном на живом кадре — полоса была голубой заливкой без
    единого пикселя картинки, притом что `data-ill` был в порядке).

    `pad` — отступ полосы внутрь (верх/право/лево); по умолчанию общий `ILL_PAD`.
    Обложка передаёт 0: там полоса сама и есть свободное поле кадра, а 28px с двух
    сторон срезали у квадратного рисунка 56px из 250 доступных — почти четверть
    (заход `zakrytie-l2`, Ш3; замер на живом кадре: панель 1384×194 в полосе
    высотой 250).

    `pad_bottom` — отдельный низ (по умолчанию = `pad`). Владелец, интервью
    2026-08-14: «иллюстрация в нижней полосе должна прижиматься к нижнему краю» —
    заход polya-i-uzor, Э2-низ; ручка нужна только `polosa_gorizontalnaya`, у
    остальных типов низ равен верху/бокам, как и было."""
    n = len(ills)
    if n < 1 or n > MAX_ILL:
        raise TipVerstki("иллюстраций в полосе %d — допустимо 1..%d (Я1 Э2)" % (n, MAX_ILL))
    flex_dir = "row" if axis == "row" else "column"
    panels = "".join(
        '<div class="panel" data-ill="%s" style="flex:1 1 0;min-width:0;min-height:0"></div>'
        % _esc(s) for s in ills)
    p = ILL_PAD if pad is None else pad
    pb = p if pad_bottom is None else pad_bottom
    # 🔴 `height:100%` — БЕЗУСЛОВНО, не только «на всякий случай». В гриде (пер-долевые
    # типы 1–2) родитель растягивает ребёнка по умолчанию (CSS Grid, align-items:stretch
    # контейнера), и без явного правила это работало «случайно». В `position:absolute`
    # контейнерах (обложка/разделитель, оба НЕ grid и НЕ flex) блочный ребёнок высоту
    # родителя не наследует вовсе — найдено на живом кадре: круг обложки распирал зону
    # по своей ширине и вылезал за нижний край холста, потому что `ill-row` держал auto-
    # высоту вместо заданных 250px. Явный `height:100%` делает оба случая одинаковыми.
    return ('<div class="zone %s ill-row" style="display:flex;flex-direction:%s;'
            'align-items:stretch;justify-content:center;gap:%dpx;padding:%dpx %dpx %dpx %dpx;'
            'height:100%%;box-sizing:border-box">%s</div>'
            % (cls, flex_dir, ILL_GAP, p, p, pb, p, panels))


def _zag_uzkij(sid):
    """Узкая роль заголовка (`--t-frametitle-n`, 20/28pt `.sty:428,454`) для типов,
    где рядом с текстом стоит иллюстрация. Признак взят у темы, а не подобран по
    факту переполнения: `ctrightframe` (`.sty:427-428`) и `ctbottomframe`
    (`.sty:453-454`) переопределяют `frametitle` на 20pt ВСЕГДА, просто потому что
    это тип слайда с картинкой; полнотекстовый `cttextframe` оставляет 24pt."""
    return (" #%s .zagolovok{ font-size:var(--t-frametitle-n); "
            "line-height:var(--lh-frametitle-n); }" % sid)


def _linija_ill(sid, storona):
    """ПРАВИЛО (заход primenenie-vizuala, Ш4): есть блок иллюстрации, соседствующий
    с текстовой зоной → на общей грани разделительная линия. Нет иллюстрации (пустая
    доска, полноэкранная картинка без текста, служебный слайд) → линии нет.
    Условие живёт в типе вёрстки, а не в списке слайдов: новая лекция получает
    линию сама, ровно там, где у неё появится иллюстрация.

    Где это записано у дизайнера. В тексте `.sty` линия одна — `:562`, и она про
    ДРУГОЕ (шапка визитки). Граница блока иллюстрации записана не текстом, а
    ассетом: зелёная панель `assets/green-bg.png`, которую `\\CTRightBackground`
    (`.sty:312`) и `\\CTBottomBackground` (`.sty:333`) растягивают на полосу
    иллюстрации, обведена по всем четырём сторонам каймой #757E70 (замер по
    пикселям: 3px из 2500×1406, все четыре стороны; наружу от кадра три стороны
    уходят в вылет `\\CTPanelBleed`, видна одна — обращённая к тексту). То есть
    правило владельца в теме есть, просто оно в картинке, а не в коде.
    Носитель у нас — перенесённые токены `--rule`/`--rule-w`/`--rule-op` (новых
    констант заход заводить запрещает); расхождение цвета названо в отчёте:
    кайма #757E70 против CTSageDark #708174 — соседние тона, не один.

    storona: 'top' — иллюстрация под текстом, 'left' — иллюстрация справа от него.
    Линия рисуется псевдоэлементом, а не border: `--rule-op` (opacity=.55 темы)
    к border-color не применить, не изобретая четвёртой константы с альфой."""
    geom = ("left:0; right:0; top:0; height:var(--rule-w);" if storona == "top"
            else "top:0; bottom:0; left:0; width:var(--rule-w);")
    return (" #%s .zone.board::before{ content:''; position:absolute; %s "
            "background:var(--rule); opacity:var(--rule-op); z-index:1; }"
            % (sid, geom))


def _require_liniya(sid, p):
    if "liniya" not in p:
        raise TipVerstki("слайд %s: тип требует поле 'liniya' (единственное число, Э1)" % sid)
    try:
        return float(p["liniya"])
    except ValueError:
        raise TipVerstki("слайд %s: 'liniya' не число: %r" % (sid, p["liniya"]))


def _require_num(sid, p, key):
    if key not in p:
        raise TipVerstki("слайд %s: тип 'kompozit' требует поле '%s'" % (sid, key))
    try:
        return float(p[key])
    except ValueError:
        raise TipVerstki("слайд %s: '%s' не число: %r" % (sid, key, p[key]))


# ───────────────────────── 1. polosa_gorizontalnaya ─────────────────────────
def polosa_gorizontalnaya(sid, p, text_html):
    liniya = _require_liniya(sid, p)
    ills = p.get("illustracii") or []
    # `--liniya` — CSS-переменная, не литерал в CSS (заход solver-vmeshcheniya,
    # Э3): `liniya` — ручка СЛАЙДА солвера, JS меняет её тем же путём, что
    # `--t-body`/`--lh`/`--blok`, без пересборки. Инвариант «второй литерал не
    # задаётся отдельным числом» (см. докстринг модуля) не просто сохранён, а
    # усилен: теперь в самой CSS-строке нет числовых литералов вовсе, ОБА
    # значения — производные одной переменной.
    css = ("#%s .grid{ position:absolute; inset:0; display:grid; "
           "grid-template-rows: var(--liniya) calc(100%% - var(--liniya)); }" % sid
           + _zag_uzkij(sid))   # ctbottomframe: иллюстрация снизу → 20pt
    if ills:
        css += _linija_ill(sid, "top")
    text = _text_zone(sid, p, text_html)
    # Ф1б доводки Л2: «низ области рисунков опустить ниже — там большой зазор».
    # Полоса у этого типа лежит НА кромке слайда, и 28 px её внутреннего отступа
    # читались как зазор под картинкой. 14 px отдают картинке 28 px высоты полосы —
    # центровка и размер догоняют это сами (flex + object-fit:contain), своего числа
    # у картинки нет. Остальным типам ILL_PAD оставлен: у вертикальной полосы тот же
    # отступ работает по ширине, а претензия была только к горизонтальной.
    # Э2-низ (владелец, интервью 2026-08-14): полоса лежит на нижней кромке слайда,
    # низ прижат к краю (pad_bottom=0) — верх/бока остаются 14px (Ф1б доводки Л2).
    ill = _ill_zone(ills, axis="row", pad=14, pad_bottom=0) if ills else '<div class="zone board"></div>'
    body = '<div class="grid" style="--liniya:%g%%">%s%s</div>' % (liniya, text, ill)
    return css, body


# ───────────────────────── 2. polosa_vertikalnaya ─────────────────────────
def polosa_vertikalnaya(sid, p, text_html):
    liniya = _require_liniya(sid, p)
    ills = p.get("illustracii") or []
    css = ("#%s .grid{ position:absolute; inset:0; display:grid; "
           "grid-template-columns: var(--liniya) calc(100%% - var(--liniya)); }" % sid
           + _zag_uzkij(sid))   # ctrightframe: иллюстрация сбоку → 20pt
    if ills:
        css += _linija_ill(sid, "left")
    text = _text_zone(sid, p, text_html)
    ill = _ill_zone(ills, axis="col") if ills else '<div class="zone board"></div>'
    body = '<div class="grid" style="--liniya:%g%%">%s%s</div>' % (liniya, text, ill)
    return css, body


# ───────────────────────── 3. polnyj_ekran ─────────────────────────
def polnyj_ekran(sid, p, text_html):
    ills = p.get("illustracii") or []
    # 🔴 БЫЛО: второе присваивание `css = …` затирало первое (`position:absolute;
    # inset:0` для `.full` пропадало) — найдено на живом кадре, слайд рендерился
    # почти пустым (только узкая полоса `.board` без размера). Обе строки нужны разом.
    css = "#%s .full{ position:absolute; inset:0; }" % sid
    if ills:
        body = '<div class="full">%s</div>' % _ill_zone(ills, axis="row", cls="board full")
    else:
        body = '<div class="full">%s</div>' % _text_zone(sid, p, text_html, cls="copy full")
    return css, body


# ───────────────────────── 4. tolko_tekst (нет в словаре — заведён) ─────────────────────────
def tolko_tekst(sid, p, text_html):
    # Ф1б доводки Л2: вертикальный отступ 64 px лежал ПОВЕРХ 46 px самой зоны —
    # 110 px сверху и снизу, это две с половиной строки пустоты у чисто текстового
    # слайда (владелец: «огромное лишнее место сверху и снизу никому не нужно»).
    # 24 + 46 = 70 px ≈ полторы строки, ровно та мера, что он назвал. Горизонтальный
    # отступ не тронут: по ширине претензии не было, а строка длиннее ухудшает чтение.
    css = ("#%s .grid{ position:absolute; inset:0; display:grid; padding:24px 96px; }" % sid)
    body = '<div class="grid">%s</div>' % _text_zone(sid, p, text_html)
    return css, body


# ───────────────────────── 7. oblozhka ─────────────────────────
def oblozhka(sid, p, text_html):
    """`sub`/`dateplace` — необязательные вторая/третья строка обложки
    (`sluzhebnye/oblozhka.html`: `?SUB{SUB}`/`?DATEPLACE{DATEPLACE}`, заход
    vizitka-i-oblozhka, В2); числа CSS дословно из `sluzhebnye/style.css`.

    🔴 `.art` — ЕДИНСТВЕННОЕ место, где число НЕ из `sluzhebnye/style.css`, и вот
    почему (заход `zakrytie-l2`, Ш3). Канон там задаёт `bottom:46px; height:250px`,
    и эти же значения стояли здесь — то есть расхождения с каноном не было вовсе.
    Дефект в другом: канон снят с обложки Л1, где мотив ШИРОКИЙ и в полосу 250px
    ложится сам. Квадратный рисунок в такой полосе упирается в высоту и рисуется
    маркой — замер на живом кадре Л2: панель 1384×194 при ширине зоны 1440.
    Поэтому высота здесь — доля кадра, а не абсолют, и доля выбрана НЕ на глаз:
    три канонные строки занимают 169–522 из 810 (тот же замер), ниже них свободны
    288px, и это жёсткий потолок — двигать строки запрещено. `height:30%` (243px)
    при `bottom:3%` (24px) ставит верх полосы на 543 — ровно те же ~20px просвета
    под третьей строкой, что и раньше, а рисунок растёт со 194 до 243 (+25%).
    Больше на этой обложке не даёт геометрия текста, а не выбор числа.
    Вместе с `pad=0` (см. `_ill_zone`) полоса отдаётся рисунку целиком."""
    z = p.get("zagolovok_na_ekrane", "")
    sub = p.get("sub")
    dateplace = p.get("dateplace")
    ills = p.get("illustracii") or []
    css = ("#%s{ background:var(--board); } "
           "#%s .wrap{ position:absolute; inset:0; display:grid; "
           "grid-template-rows:1fr auto 1.7fr; align-items:center; padding:0 130px; } "
           "#%s .head{ grid-row:2; } "
           "#%s .head .t-display{ font-size:96px; } "
           "#%s .sub{ font-family:var(--font-body); "
           "text-align:center; color:var(--ink); font-size:32px; letter-spacing:.04em; margin-top:36px; } "
           "#%s .sub2{ font-size:22px; margin-top:14px; color:var(--ink); opacity:.78; line-height:1.5; } "
           "#%s .art{ position:absolute; left:0; right:0; bottom:3%%; height:30%%; }"
           % (sid, sid, sid, sid, sid, sid, sid))
    art = ('<div class="art">%s</div>' % _ill_zone(ills, axis="row", cls="", pad=0)
           if ills else "")
    sub_html = '<div class="sub">%s</div>' % _esc(sub) if sub else ""
    dateplace_html = '<div class="sub sub2">%s</div>' % _esc(dateplace) if dateplace else ""
    body = ('<div class="wrap"><div class="head"><div class="t-display">%s</div>%s%s</div></div>%s'
            % (_esc(z), sub_html, dateplace_html, art))
    return css, body


# ───────────────────────── 8. vizitka ─────────────────────────
def vizitka(sid, p, text_html):
    """Фото и QR — не иллюстрации лекции (не через `data-ill`/пул `illustracii/`),
    а готовый HTML канона (`sluzhebnye/vizitka-photo.html`/`vizitka-qr.html`,
    `<img src="data:...">`): deck.py читает их с диска и кладёт в `photo_html`/
    `qr_html` (заход vizitka-i-oblozhka, В1). Раскладка (251×260, 250×250) не
    менялась — она уже совпадала с каноном."""
    ills = p.get("illustracii") or []
    if ills:
        # override: вся визитка — одна иллюстрация во весь слайд (см. deck.py:
        # plan_sluzhebnyh, поле `vizitka_illustracii`), канон sluzhebnye/ не рисуется.
        css = "#%s{ background:var(--board); } #%s .full{ position:absolute; inset:0; }" % (sid, sid)
        body = '<div class="full">%s</div>' % _ill_zone(ills, axis="row", cls="", pad=0)
        return css, body
    z = p.get("zagolovok_na_ekrane", "Про меня")
    css = ("#%s .grid{ position:absolute; inset:0; display:grid; "
           "grid-template-columns:410px 56px 1fr; grid-template-rows:107px 1fr; } "
           "#%s .board{ grid-area:1/1/3/2; background:var(--board); position:relative; } "
           # 74px было подобрано под Forum; Cormorant Garamond шире — «Про меня» переставало
           # влезать в доску 410px, вторая строка ложилась на фото (замер: 374px при 74px,
           # 329px при 64px, доступно 374px). Кегль взят из перенесённой шкалы —
           # --t-frametitle-n, заголовок узкой колонки (.sty:428,454 → 20pt).
           "#%s .brd-title{ position:absolute; left:36px; top:34px; font-size:var(--t-frametitle-n); } "
           "#%s .p-photo{ position:absolute; left:81px; top:174px; width:251px; height:260px; } "
           "#%s .p-photo img{ width:100%%; height:100%%; object-fit:cover; } "
           "#%s .p-qr{ position:absolute; left:81px; top:479px; width:250px; height:250px; } "
           "#%s .p-qr img{ width:100%%; height:100%%; } "
           "#%s .copy{ grid-area:2/3; }"
           % (sid, sid, sid, sid, sid, sid, sid, sid))
    photo_raw = p.get("photo_html", "")
    qr_raw = p.get("qr_html", "")
    photo_html = ('<div class="panel p-photo">%s</div>' % photo_raw) if photo_raw else ""
    qr_html = ('<div class="panel p-qr">%s</div>' % qr_raw) if qr_raw else ""
    body = ('<div class="grid">'
            '<div class="zone board"><div class="brd-title t-display">%s</div>%s%s</div>'
            '<div class="zone copy t-body">%s</div>'
            '</div>' % (_esc(z), photo_html, qr_html, text_html))
    return css, body


# ───────────────────────── 9. finalnyj (не «финальный» — имя словаря) ─────────────────────────
def finalnyj(sid, p, text_html):
    z = p.get("zagolovok_na_ekrane", "Спасибо за внимание")
    ills = p.get("illustracii") or []
    css = ("#%s{ background:var(--board); } "
           "#%s .thx-wrap{ position:absolute; inset:0; display:grid; "
           "grid-template-rows:%s; padding:0 120px 52px; } "
           "#%s .thx-head{ align-self:center; justify-self:center; font-size:60px; } "
           "#%s .thx-art{ min-height:0; }"
           % (sid, sid, "186px 1fr" if ills else "1fr", sid, sid))
    art = ('<div class="thx-art">%s</div>' % _ill_zone(ills, axis="row", cls="")
           if ills else "")
    body = ('<div class="thx-wrap"><div class="thx-head t-display">%s</div>%s</div>'
            % (_esc(z), art))
    return css, body


# ───────────────────────── 10. razdelitel (утверждён владельцем 2026-08-08) ─────────────────────────
def razdelitel(sid, p, text_html):
    z = p.get("zagolovok_na_ekrane", "")
    ills = p.get("illustracii") or []
    css = ("#%s{ background:var(--board); } "
           "#%s .head{ position:absolute; left:0; top:61px; width:100%%; "
           "font-size:56px; line-height:1.18; }"
           % (sid, sid))
    if ills:
        css += (" #%s .art{ position:absolute; left:28px; top:206px; right:28px; height:403px; }"
                % sid)
        art = '<div class="art">%s</div>' % _ill_zone(ills, axis="row", cls="")
    else:
        css += " #%s .head{ top:0; bottom:0; display:flex; align-items:center; justify-content:center; }" % sid
        art = ""
    body = '<div class="head t-display">%s</div>%s' % (_esc(z), art)
    return css, body


# ───────────────────────── 11. kompozit (Д18 захода gruppa-D-kompilyator) ─────────────────────────
def kompozit(sid, p, text_html):
    """Текст + доска, а доска сама разбита на ДВЕ неравные иллюстрации — геометрия
    снята с живых деков (Я2 захода): dandelin `s05a`/`s09` (`.grid{grid-template-
    columns:56% 44%}` снаружи + `.board{grid-template-rows:54% 46%}` внутри) и
    buffon `sl-coords` (доска с двумя иллюстрациями разной ширины). Не сводится к
    восьми готовым: `_ill_zone` даёт только РАВНЫЙ flex для списка иллюстраций, а
    здесь сплит процентный и неравный — вторая независимая доля, поэтому и второй
    параметр `liniya_ill` (не хардкод пары чисел: `calc()`, тот же инвариант
    модуля, что уже несёт `liniya`, применён дважды — см. докстринг модуля)."""
    liniya = _require_liniya(sid, p)
    liniya_ill = _require_num(sid, p, "liniya_ill")
    ills = p.get("illustracii") or []
    if len(ills) != 2:
        raise TipVerstki(
            "слайд %s: 'kompozit' требует ровно 2 иллюстрации в 'illustracii', получено %d"
            % (sid, len(ills)))
    css = ("#%s .grid{ position:absolute; inset:0; display:grid; "
           "grid-template-columns: var(--liniya) calc(100%% - var(--liniya)); } "
           "#%s .board{ display:grid; grid-template-rows: var(--liniya-ill) "
           "calc(100%% - var(--liniya-ill)); gap:%dpx; padding:%dpx; box-sizing:border-box; }"
           % (sid, sid, ILL_GAP, ILL_PAD)
           + _zag_uzkij(sid)    # текст рядом с доской — та же узкая колонка, что ctrightframe
           + _linija_ill(sid, "left"))  # доска здесь всегда с двумя иллюстрациями (проверка выше)
    text = _text_zone(sid, p, text_html)
    panels = "".join(
        '<div class="panel" data-ill="%s" style="min-width:0;min-height:0"></div>' % _esc(s)
        for s in ills)
    board = '<div class="zone board" style="--liniya-ill:%g%%">%s</div>' % (liniya_ill, panels)
    body = '<div class="grid" style="--liniya:%g%%">%s%s</div>' % (liniya, text, board)
    return css, body


REESTR = {
    "polosa_gorizontalnaya": polosa_gorizontalnaya,
    "polosa_vertikalnaya": polosa_vertikalnaya,
    "polnyj_ekran": polnyj_ekran,
    "tolko_tekst": tolko_tekst,
    "oblozhka": oblozhka,
    "vizitka": vizitka,
    "finalnyj": finalnyj,
    "razdelitel": razdelitel,
    "kompozit": kompozit,
}

ОТЛОЖЕННЫЕ = ("kartochka_centr", "rejka_sajdbar")


def compile_tip(sid, p, text_html):
    tip = p.get("tip_verstki")
    if tip in ОТЛОЖЕННЫЕ:
        raise TipVerstki(
            "тип '%s' отложен сознательно в этом заходе (Э2 захода) — не реализован" % tip)
    handler = REESTR.get(tip)
    if handler is None:
        raise TipVerstki(
            "тип '%s' неизвестен. Поддержаны: %s" % (tip, ", ".join(sorted(REESTR))))
    return handler(sid, p, text_html)
