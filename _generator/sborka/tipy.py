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
    ".zone.copy{ padding:46px 64px; } "
    ".zagolovok{ font-family:'Forum',serif; text-transform:uppercase; "
    "font-size:44px; line-height:1.15; margin-bottom:28px; color:var(--ink); }"
)


class TipVerstki(Exception):
    pass


def _esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _zagolovok_html(p):
    z = p.get("zagolovok")
    if not z:
        return ""
    return '<div class="zagolovok">%s</div>' % _esc(z)


def _kegl_style(p):
    k = p.get("kegl")
    if not k or float(k) == 1.0:
        return ""
    return ' style="--t-body:calc(38px * %s)"' % k


def _text_zone(sid, p, text_html, cls="copy"):
    return ('<div class="zone %s t-body"%s>%s%s</div>'
            % (cls, _kegl_style(p), _zagolovok_html(p), text_html))


def _ill_zone(ills, axis, cls="board"):
    """axis: 'row' — бок о бок (для горизонтальной полосы, где полоса делится по
    ВЫСОТЕ и картинка занимает её по ШИРИНЕ); 'col' — стопкой (для вертикальной
    полосы, где картинка занимает зону по ВЫСОТЕ). Я1 Э2, правило дословно.

    🔴 `align-items:stretch` (дефолт flex, НЕ `center`) + `flex:1 1 0` на панели —
    это и есть «занимают целиком»: без них панель без явных width/height схлопывается
    в 0×0 (найдено этим же прогоном на живом кадре — полоса была голубой заливкой без
    единого пикселя картинки, притом что `data-ill` был в порядке)."""
    n = len(ills)
    if n < 1 or n > MAX_ILL:
        raise TipVerstki("иллюстраций в полосе %d — допустимо 1..%d (Я1 Э2)" % (n, MAX_ILL))
    flex_dir = "row" if axis == "row" else "column"
    panels = "".join(
        '<div class="panel" data-ill="%s" style="flex:1 1 0;min-width:0;min-height:0"></div>'
        % _esc(s) for s in ills)
    # 🔴 `height:100%` — БЕЗУСЛОВНО, не только «на всякий случай». В гриде (пер-долевые
    # типы 1–2) родитель растягивает ребёнка по умолчанию (CSS Grid, align-items:stretch
    # контейнера), и без явного правила это работало «случайно». В `position:absolute`
    # контейнерах (обложка/разделитель, оба НЕ grid и НЕ flex) блочный ребёнок высоту
    # родителя не наследует вовсе — найдено на живом кадре: круг обложки распирал зону
    # по своей ширине и вылезал за нижний край холста, потому что `ill-row` держал auto-
    # высоту вместо заданных 250px. Явный `height:100%` делает оба случая одинаковыми.
    return ('<div class="zone %s ill-row" style="display:flex;flex-direction:%s;'
            'align-items:stretch;justify-content:center;gap:%dpx;padding:%dpx;'
            'height:100%%;box-sizing:border-box">%s</div>'
            % (cls, flex_dir, ILL_GAP, ILL_PAD, panels))


def _require_liniya(sid, p):
    if "liniya" not in p:
        raise TipVerstki("слайд %s: тип требует поле 'liniya' (единственное число, Э1)" % sid)
    try:
        return float(p["liniya"])
    except ValueError:
        raise TipVerstki("слайд %s: 'liniya' не число: %r" % (sid, p["liniya"]))


# ───────────────────────── 1. polosa_gorizontalnaya ─────────────────────────
def polosa_gorizontalnaya(sid, p, text_html):
    liniya = _require_liniya(sid, p)
    ills = p.get("illustracii") or []
    css = ("#%s .grid{ position:absolute; inset:0; display:grid; "
           "grid-template-rows: %g%% calc(100%% - %g%%); }" % (sid, liniya, liniya))
    text = _text_zone(sid, p, text_html)
    ill = _ill_zone(ills, axis="row") if ills else '<div class="zone board"></div>'
    body = '<div class="grid">%s%s</div>' % (text, ill)
    return css, body


# ───────────────────────── 2. polosa_vertikalnaya ─────────────────────────
def polosa_vertikalnaya(sid, p, text_html):
    liniya = _require_liniya(sid, p)
    ills = p.get("illustracii") or []
    css = ("#%s .grid{ position:absolute; inset:0; display:grid; "
           "grid-template-columns: %g%% calc(100%% - %g%%); }" % (sid, liniya, liniya))
    text = _text_zone(sid, p, text_html)
    ill = _ill_zone(ills, axis="col") if ills else '<div class="zone board"></div>'
    body = '<div class="grid">%s%s</div>' % (text, ill)
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
    css = ("#%s .grid{ position:absolute; inset:0; display:grid; padding:64px 96px; }" % sid)
    body = '<div class="grid">%s</div>' % _text_zone(sid, p, text_html)
    return css, body


# ───────────────────────── 7. oblozhka ─────────────────────────
def oblozhka(sid, p, text_html):
    z = p.get("zagolovok", "")
    ills = p.get("illustracii") or []
    css = ("#%s{ background:var(--board); } "
           "#%s .wrap{ position:absolute; inset:0; display:grid; "
           "grid-template-rows:1fr auto 1.7fr; align-items:center; padding:0 130px; } "
           "#%s .head{ grid-row:2; } "
           "#%s .head .t-display{ font-size:96px; } "
           "#%s .art{ position:absolute; left:0; right:0; bottom:46px; height:250px; }"
           % (sid, sid, sid, sid, sid))
    art = ('<div class="art">%s</div>' % _ill_zone(ills, axis="row", cls="")
           if ills else "")
    body = ('<div class="wrap"><div class="head"><div class="t-display">%s</div></div></div>%s'
            % (_esc(z), art))
    return css, body


# ───────────────────────── 8. vizitka ─────────────────────────
def vizitka(sid, p, text_html):
    z = p.get("zagolovok", "Про меня")
    ills = p.get("illustracii") or []
    photo = ills[0] if len(ills) >= 1 else None
    qr = ills[1] if len(ills) >= 2 else None
    css = ("#%s .grid{ position:absolute; inset:0; display:grid; "
           "grid-template-columns:410px 56px 1fr; grid-template-rows:107px 1fr; } "
           "#%s .board{ grid-area:1/1/3/2; background:var(--board); position:relative; } "
           "#%s .brd-title{ position:absolute; left:36px; top:34px; font-size:74px; } "
           "#%s .p-photo{ position:absolute; left:81px; top:174px; width:251px; height:260px; } "
           "#%s .p-qr{ position:absolute; left:81px; top:479px; width:250px; height:250px; } "
           "#%s .copy{ grid-area:2/3; }"
           % (sid, sid, sid, sid, sid, sid))
    photo_html = ('<div class="panel p-photo" data-ill="%s"></div>' % _esc(photo)) if photo else ""
    qr_html = ('<div class="panel p-qr" data-ill="%s"></div>' % _esc(qr)) if qr else ""
    body = ('<div class="grid">'
            '<div class="zone board"><div class="brd-title t-display">%s</div>%s%s</div>'
            '<div class="zone copy t-body">%s</div>'
            '</div>' % (_esc(z), photo_html, qr_html, text_html))
    return css, body


# ───────────────────────── 9. finalnyj (не «финальный» — имя словаря) ─────────────────────────
def finalnyj(sid, p, text_html):
    z = p.get("zagolovok", "Спасибо за внимание")
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
    z = p.get("zagolovok", "")
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


REESTR = {
    "polosa_gorizontalnaya": polosa_gorizontalnaya,
    "polosa_vertikalnaya": polosa_vertikalnaya,
    "polnyj_ekran": polnyj_ekran,
    "tolko_tekst": tolko_tekst,
    "oblozhka": oblozhka,
    "vizitka": vizitka,
    "finalnyj": finalnyj,
    "razdelitel": razdelitel,
}

ОТЛОЖЕННЫЕ = ("kartochka_centr", "kompozit", "rejka_sajdbar")


def compile_tip(sid, p, text_html):
    tip = p.get("tip")
    if tip in ОТЛОЖЕННЫЕ:
        raise TipVerstki(
            "тип '%s' отложен сознательно в этом заходе (Э2 захода) — не реализован" % tip)
    handler = REESTR.get(tip)
    if handler is None:
        raise TipVerstki(
            "тип '%s' неизвестен. Поддержаны: %s" % (tip, ", ".join(sorted(REESTR))))
    return handler(sid, p, text_html)
