#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сборка ЦЕЛОГО дека — параллельно по слайдам (Э6 захода kartochka-i-sborka).

  python3 _generator/sborka/deck.py <лекция> -o <лекция>/dist/index.html [-j 15]

Раскладка — Я2 (istochnik-istiny.md §2): `<лекция>/slajdy/<imya>/slaid.md`, один
файл на слайд, ИМЯ ПАПКИ = `sid` (не `slide_path.stem` — тот теперь всегда literally
"slaid" у всех слайдов сразу, различает их только папка). Иллюстрации — ОТДЕЛЬНЫЙ
пул `<лекция>/illustracii/` (Э5 захода, имя ПО СПЕЦИФИКАЦИИ, не англ. "illustrations"
старого пути). `status: rezerv` — слайд лежит в папке, в дек НЕ входит и в
`slide_order` может не быть вовсе (Я1 §4-бис).

Слайды независимы (параметры + текст, никаких перекрёстных ссылок между файлами
слайдов), поэтому компиляция каждого — отдельный процесс (`ProcessPoolExecutor`,
stdlib, без pip). Порядок — `brief.md:slide_order` тем же диалектом, что читает
`build_deck.py` (Я6, `parse_brief`, READ-ONLY импорт; `brief.md` — И манифест
порядка, И карточка лекции, см. `## ПЛАН` захода п.4); `oblozhka` принудительно
первой, `finalnyj` принудительно последней — по ТИПУ слайда, а не по месту в списке
автора (устойчивее зарезервированных id старого `build_deck.py`).

`build_deck.py` этим НЕ трогается — параллельный путь, отдельная папка.
"""
import argparse
import re
import sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
import os

SBORKA = Path(__file__).resolve().parent
GENERATOR = SBORKA.parent
SKELETON = GENERATOR / "skeleton"
for p in (str(SBORKA), str(GENERATOR)):
    if p not in sys.path:
        sys.path.insert(0, p)

import vmeshchenie  # noqa: E402 — П1: дом метки `podbor_avto` и её разбора ОДИН, и он там
POLE_METKI = vmeshchenie.POLE_METKI
POLE_NAMERENIYA = vmeshchenie.POLE_NAMERENIYA


def _compile_one(slide_path_str):
    """Воркер отдельного процесса: путь к .md → (sid, tip, status, illustracii-стемы,
    css, html, n_scenes). `sid` — ИМЯ ПАПКИ слайда (`slajdy/<sid>/slaid.md`), не
    стем файла. `n_scenes` — Э8 захода kartochka-i-sborka: без него движок считает
    слайд односценовым и пропуск (`{@N|…}`) не раскрывается НИКОГДА (см. slaid.py).
    Импорты — ВНУТРИ функции: `ProcessPoolExecutor` на macOS стартует процессы
    методом spawn, каждый воркер импортирует этот модуль заново с нуля."""
    import sys as _sys
    from pathlib import Path as _Path
    sb = _Path(__file__).resolve().parent
    gen = sb.parent
    for p in (str(sb), str(gen)):
        if p not in _sys.path:
            _sys.path.insert(0, p)
    from formaty import parse_slide, render_body, check_no_missing_math
    from tipy import compile_tip
    from build_deck import max_scenes  # noqa: E402  (READ-ONLY импорт, Я6)
    from slaid import load_math_cache  # noqa: E402  (Э5 захода solver-vmeshcheniya)

    slide_path = _Path(slide_path_str)
    sid = slide_path.parent.name
    text = slide_path.read_text(encoding="utf-8")
    params, body_md = parse_slide(text, sid=sid)
    params["illustracii"] = [_Path(s).stem for s in (params.get("illustracii") or [])]
    # slide_path = <лекция>/slajdy/<sid>/slaid.md → parents[2] = <лекция>
    lekcija_dir = slide_path.parents[2]
    math = load_math_cache(lekcija_dir)
    body_html = render_body(body_md, acc_tag="span", math=math, sid=sid)
    # формулы бывают и в `zagolovok_na_ekrane` (tipy._zagolovok_html) — тот же кэш
    params["_math"] = math
    css, html = compile_tip(sid, params, body_html)
    # 🔴 проверка ПОСЛЕ compile_tip, а не только по `body_html`: заголовок слайда
    # тоже рендерит формулы, и по телу его брак не виден.
    check_no_missing_math(html, sid, lekcija_dir)
    n_scenes = max_scenes(html)
    return (sid, params.get("tip_verstki"), params.get("status", "v_deke"),
            params["illustracii"], css, html, n_scenes)


# Р3 захода porcia-1-zamknut-konvejer: ось `liniya` солвера имеет смысл только
# у двух типов вёрстки (полоса делится горизонтально/вертикально) — остальные
# типы подбирают только kegl/lh/blok (axis=None, vmeshchenie.podobrat_slide сам
# не варьирует liniya без оси).
AXIS_BY_TIP = {"polosa_gorizontalnaya": "horizontal", "polosa_vertikalnaya": "vertical"}

# П1 захода tri-provodki: значения полей-намерений, читаемые как «да».
DA = ("da", "да", "true", "yes", "1")


def _da(value):
    return isinstance(value, str) and value.strip().lower() in DA


def reshenie_o_podbore(params, otpechatok_tela, zanovo=False):
    """Шапка карточки + отпечаток её тела → (подбирать: bool, причина: str).

    🔴 КЛАСС ОШИБКИ, ОТ КОТОРОЙ ЭТА ФУНКЦИЯ ЛЕЧИТ (П1 захода tri-provodki):
    ПРИЗНАК НАЛИЧИЯ ПРИНЯТ ЗА ПРИЗНАК РЕШЕНИЯ. Прежняя развилка читала непустую
    `liniya` как «автор сам выбрал ширину полосы — не лезь». Но `liniya` —
    ОБЯЗАТЕЛЬНОЕ поле шапки (`formaty.OBYAZATELNYE_POLYA`; без числа
    `tipy._require_liniya` роняет компиляцию, `gejt_kartochki.py` требует поле
    заполненным) ⇒ у ЛЮБОЙ полосы, прошедшей гейт, условие было истинно ВСЕГДА, и
    солвер выключался ровно на тех слайдах, ради которых он и писался (ось
    `liniya` существует только у `polosa_*`). Замер до правки на живой Л2:
    подобрано 0 из 18, пропущено 18.

    Поэтому признаков теперь два, и оба НЕобязательны — то есть их наличие
    действительно есть решение, а не следствие гейта:

    - `verstka_reshena: da` — НАМЕРЕНИЕ АВТОРА: типографику слайда он решил сам,
      солвер не трогает ничего. Одно поле на все четыре ручки солвера
      (`liniya`/`kegl_px`/`mezhstrochye`/`otstup_bloka`), а не на одну ось: автор
      решает вёрстку слайда целиком.
    - `podbor_avto` — МЕТКА САМОГО СОЛВЕРА (`vmeshchenie.apply_to_card`): отпечаток
      тела, по которому подбирали, и значения, которые он записал. Лечит второй
      дефект того же класса: без метки записанный солвером `kegl_px` на следующей
      сборке читался как «явный», подбор был ОДНОРАЗОВЫМ, и любая правка текста
      молча ехала на старом кегле.

    Шесть исходов — таблицей, потому что каждый оплачен отдельной причиной:

      | шапка                                   | решение     | `--zanovo` |
      | `verstka_reshena: da`                   | не трогать  | не трогать |
      | метки нет, есть `kegl_px` (легаси)      | не трогать  | подбирать  |
      | метки нет, `kegl_px` нет                | ПОДБИРАТЬ   | подбирать  |
      | метка есть, значения свои, тело то же   | пропустить (вход не менялся) | подбирать |
      | метка есть, тело изменилось             | ПЕРЕПОДОБРАТЬ | подбирать |
      | метка есть, значения в шапке чужие      | не трогать (правил человек) | подбирать |

    🔴 ЛЕГАСИ ПО УМОЛЧАНИЮ НЕ ТРОГАЕМ, и это решение стоило одного прогона, а не
    вкуса. Карточки, размеченные ДО этого захода, несут `kegl_px`/`liniya` без
    метки — рука автора и рука солвера в них неразличимы. Первый вариант правила
    («легаси = запись солвера, переподбирать») прогнан на живой Л2: солвер тронул
    15 слайдов из 15 и разошёлся с ручными решениями круга 2 КРУПНО и в сторону
    хуже — `dvazhdy-dvojstvennoe` liniya 54 → 79,17 (полосу под квадрат сузили
    втрое, а её РАСШИРЯЛИ осознанно, чтобы квадрат не висел в пустоте),
    `inyekcii` 58 → 82, `fundamentalnaya-gruppa` 70 → 53,5. Причина расхождения
    названа, а не подогнана порогом: солвер оптимизирует вмещение ТЕКСТА и
    похожесть на корпус и ничего не знает про пропорцию картинки, под которую
    человек и крутил `liniya`. ⇒ по умолчанию молчим, а размораживается лекция
    ЯВНОЙ командой `--zanovo` — то есть решением человека, а не побочным эффектом
    ближайшей сборки. Иначе получаем ровно тот исход, который хуже нынешнего:
    солвер не молчит, а молча портит.
    """
    if _da(params.get(POLE_NAMERENIYA)):
        return False, "намерение автора: %s: %s" % (POLE_NAMERENIYA, params[POLE_NAMERENIYA])

    otp_metki, znacheniya_metki = vmeshchenie.razobrat_metku(params.get(POLE_METKI))
    kegl = params.get("kegl_px")
    if zanovo:
        return True, "переподбор по --zanovo"
    if otp_metki is None:
        if kegl:
            return False, ("легаси: значения без метки `%s` (kegl_px=%s) — солвер их не "
                           "трогает; переподобрать всю лекцию: --zanovo; заморозить "
                           "навсегда: `%s: da`" % (POLE_METKI, kegl, POLE_NAMERENIYA))
        return True, "подбор впервые"

    for k, v in znacheniya_metki.items():
        v_shapki = params.get(k)
        try:
            if v_shapki is None or abs(float(v_shapki) - v) > 1e-9:
                return False, "после солвера правили руками: %s=%s, солвер писал %s" % (
                    k, v_shapki, v)
        except (TypeError, ValueError):
            return False, "после солвера правили руками: %s=%r нечисловое" % (k, v_shapki)

    if otp_metki != otpechatok_tela:
        return True, "текст изменился (было %s, стало %s)" % (otp_metki, otpechatok_tela)
    return False, "вход не менялся с прошлого подбора (%s)" % otp_metki


def _podobrat_tipografiku(to_compile, zanovo=False):
    """Прогоняет солвер (`vmeshchenie.podobrat_slide`) по каждому слайду из
    `to_compile`, который этого требует по `reshenie_o_podbore`, и применяет выбор
    в карточку (`vmeshchenie.apply_to_card`) ДО финальной параллельной компиляции.
    Раньше `deck.py` вообще не звал `vmeshchenie.py` (Р3: главный инструмент арки
    был не подключён к сборке).

    🔴 КОГО пропускать — решает `reshenie_o_podbore` (см. её докстринг: там весь
    разбор «решение автора» против «поле обязано быть заполнено»). Здесь только
    прогон и печать: почему пропущен КАЖДЫЙ слайд — строкой, поимённо."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        raise SystemExit(
            "playwright не установлен — подбор типографики недоступен и деку "
            "БЕЗ подбора я не соберу молча (см. §2 Р3 захода "
            "porcia-1-zamknut-konvejer): либо `pip install playwright && "
            "playwright install chrome`, либо явный флаг --bez-podbora. (%s)" % e)
    import tempfile
    from formaty import parse_card
    from slaid import compile_slide_html

    podobrano, propushcheno, legasi = 0, 0, []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 810}, device_scale_factor=1)
        try:
            for slide_path in to_compile:
                sid = slide_path.parent.name
                params, telo = parse_card(slide_path.read_text(encoding="utf-8"), sid=sid)
                axis = AXIS_BY_TIP.get(params.get("tip_verstki"))
                nado, prichina = reshenie_o_podbore(params, vmeshchenie.otpechatok(telo),
                                                    zanovo=zanovo)
                if not nado:
                    propushcheno += 1
                    if prichina.startswith("легаси"):
                        legasi.append(sid)
                    print("подбор: %s — пропущен, %s" % (sid, prichina), file=sys.stderr)
                    continue
                bylo = (params.get("kegl_px"), params.get("liniya")) if params.get("kegl_px") else None
                print("подбор: %s — %s" % (sid, prichina), file=sys.stderr)
                with tempfile.TemporaryDirectory() as tmp:
                    _, html = compile_slide_html(slide_path)
                    # 🔴 Найдено живым прогоном (заплатка sborka-l2-fazy-4-7): не у
                    # каждого tip_verstki есть текстовая зона вовсе — `polnyj_ekran`
                    # с непустым `illustracii` рендерит ТОЛЬКО картинки (`tipy.py:
                    # polnyj_ekran`), без `.zone.t-body`. Раньше солвер лез туда
                    # безусловно и падал `RuntimeError("зона .zone.t-body не найдена
                    # на слайде")`, роняя ВЕСЬ дек ради одного слайда без текста.
                    # Подгонять там нечего — тот же класс, что и «явные значения»,
                    # только причина другая. 🔴 Проверять НЕ голой подстрокой "t-body":
                    # `--t-body` (CSS-токен кегля) сидит в <style> КАЖДОГО слайда
                    # безусловно, даже без единой `.t-body`-зоны в теле — голая
                    # подстрока всегда находила совпадение и не пропускала ничего
                    # (найдено этим же прогоном, вторая попытка). Ищем реальный
                    # class="… t-body …" в HTML-теле.
                    if not re.search(r'class="[^"]*\bt-body\b[^"]*"', html):
                        propushcheno += 1
                        print("подбор: %s — пропущен, текстовой зоны на слайде нет "
                              "(tip_verstki=%s без текста)" % (sid, params.get("tip_verstki")),
                              file=sys.stderr)
                        continue
                    html_path = Path(tmp) / "slide.html"
                    html_path.write_text(html, encoding="utf-8")
                    res = vmeshchenie.podobrat_slide(page, html_path, axis=axis)
                if res["chosen"] is None:
                    raise SystemExit(
                        "подбор: %s — ни одна проба не влезла внутри жёстких зон "
                        "(см. `vmeshchenie.py --demo-zony`)" % sid)
                vmeshchenie.apply_to_card(slide_path, res["chosen"])
                podobrano += 1
                print("подбор: %s — kegl=%.1f liniya=%s" % (
                    sid, res["chosen"]["kegl"], res["chosen"].get("liniya")), file=sys.stderr)
                if bylo is not None:
                    # Значения в карточке уже были — печатаем расхождение поимённо.
                    # Молча заменить прежнее число новым это ровно то, чего боится
                    # §3 захода: солвер, который не молчит, а молча портит.
                    print("  ⚠ поверх прежних значений: kegl %s → %.1f · liniya %s → %s"
                          % (bylo[0], res["chosen"]["kegl"], bylo[1],
                             res["chosen"].get("liniya") if res["chosen"].get("liniya") is not None
                             else "не трогалась"), file=sys.stderr)
        finally:
            browser.close()
    print("подбор типографики: %d слайдов подобрано, %d пропущено" % (podobrano, propushcheno))
    if legasi:
        print("  ⚠ ЗАМОРОЖЕННЫХ ЛЕГАСИ-карточек (значения без метки `%s`): %d — %s.\n"
              "     Разморозить лекцию целиком: `deck.py <лекция> -o <выход> --zanovo`;\n"
              "     закрепить решение автора навсегда: `%s: da` в шапке карточки."
              % (POLE_METKI, len(legasi), ", ".join(legasi), POLE_NAMERENIYA))
    return podobrano, propushcheno


# ─────────────── П2 захода tri-provodki: служебные слайды ───────────────
# Обложка, визитка и финальный слайд УЖЕ УМЕЮТ рисоваться (`tipy.oblozhka`,
# `tipy.vizitka`, `tipy.finalnyj` — все три принимают `zagolovok_na_ekrane` и
# `illustracii`), и `_order` уже ставит обложку первой, финальный последним. Не
# хватало ровно одного: шага, который их ПОРОДИТ. Сегодня они появлялись, только
# если автор заводил папку слайда руками, — а он не обязан и не должен.
#
# 🔴 ВХОД — `brief.md`, и НИКАКОГО нового документа: требование владельца «чем
# меньше документов, тем лучше». `brief.md` уже и манифест порядка, и карточка
# лекции; служебный слайд — производная лекции в целом, а не отдельный источник.
# Все поля НЕОБЯЗАТЕЛЬНЫ: лекция, ничего про них не сказавшая, собирается как
# раньше плюс обложка с заголовком из `title`.
SLUZHEBNYE = (
    # тип         поле-выключатель   поле заголовка         поле иллюстраций
    ("oblozhka",  None,              "oblozhka_zagolovok",  "oblozhka_illustracii"),
    # В1 захода vizitka-i-oblozhka: содержание визитки — канон sluzhebnye/,
    # поля brief.md для неё больше не читаются (см. plan_sluzhebnyh ниже).
    ("vizitka",   "bez_vizitki",     None,                   None),
    ("finalnyj",  "bez_finalnogo",   "finalnyj_zagolovok",  "finalnyj_illustracii"),
)


def _spisok(v):
    """Значение поля `brief.md` → список имён. `parse_brief` отдаёт либо список
    (многострочная запись `- имя`), либо одну строку; строку с запятыми режем."""
    if not v:
        return []
    if isinstance(v, str):
        return [x.strip() for x in v.split(",") if x.strip()]
    return [str(x).strip() for x in v if str(x).strip()]


def plan_sluzhebnyh(meta, tipy_na_diske, zanyatye_sid=()):
    """`brief.md` + типы слайдов, УЖЕ лежащих на диске → что генератор порождает сам.

    → список `(sid, params, tekst_md)`, готовый к `tipy.compile_tip`.

    Правила (П2 захода tri-provodki):
    - **обложка безусловна**, выключателя у неё нет: дек без обложки — это не
      решение автора, это забытый слайд;
    - **визитка и финальный есть по умолчанию**, снимаются явным флагом в
      `brief.md` (`bez_vizitki: da` / `bez_finalnogo: da`);
    - 🔴 **автор завёл служебный слайд руками — генератор молчит.** Проверка по
      ТИПУ карточки, а не по её имени: слайд-обложка может называться как угодно
      (`_order` тоже сортирует по типу, по той же причине).
    Заголовок обложки НЕ обязан совпадать с внутренним `title` лекции: `title` —
    рабочее имя («Функторы»), а на экран выносится `oblozhka_zagolovok`, если он
    назван. Обложка также умеет две необязательные строки — `oblozhka_sub`
    (обычно «Лекция N») и `oblozhka_dateplace` (дата эфира), в `sluzhebnye/
    oblozhka.html` это слоты `?SUB`/`?DATEPLACE` (В2 захода vizitka-i-oblozhka).
    Разделители здесь не порождаются вовсе — их автор ставит осознанно.

    🔴 Визитка — не как остальные два: В1 захода vizitka-i-oblozhka закрыл
    дефект «механизм построен и не подключён» — `brief.md` для неё ничего не
    решает, содержание (текст, фото, QR) читается прямо из
    `_generator/skeleton/sluzhebnye/` при КАЖДОЙ сборке. Владелец правит текст
    ТАМ, не здесь — лекция про визитку не думает вовсе.
    """
    from build_deck import read_text  # READ-ONLY импорт, Я6 — тот же приём, что build()

    est_tipy = set(tipy_na_diske.values())
    zanyatye = set(zanyatye_sid) | set(tipy_na_diske)
    plan = []
    for tip, vykl, pole_z, pole_ill in SLUZHEBNYE:
        if tip in est_tipy:
            continue                      # автор завёл сам — дубля не будет
        if vykl and _da(meta.get(vykl)):
            continue                      # снят явным флагом в brief.md
        sid = tip if tip not in zanyatye else tip + "-avto"
        zanyatye.add(sid)
        if tip == "vizitka":
            sluzh = SKELETON / "sluzhebnye"
            params = {
                "tip_verstki": "vizitka",
                # опциональный per-лекция override: `vizitka_illustracii` в brief.md —
                # если назван, vizitka() рисует ТОЛЬКО эту иллюстрацию во весь слайд
                # (см. tipy.py:vizitka), канон sluzhebnye/ не читается вовсе. Пусто по
                # умолчанию — поведение для всех лекций без этого поля не меняется.
                "illustracii": _spisok(meta.get("vizitka_illustracii")),
                "photo_html": read_text(sluzh / "vizitka-photo.html").strip(),
                "qr_html": read_text(sluzh / "vizitka-qr.html").strip(),
            }
            plan.append((sid, params, read_text(sluzh / "vizitka.md")))
            continue
        zagolovok = meta.get(pole_z)
        if tip == "oblozhka" and not zagolovok:
            zagolovok = meta.get("title", "")
        params = {"tip_verstki": tip, "illustracii": _spisok(meta.get(pole_ill))}
        if zagolovok:
            params["zagolovok_na_ekrane"] = zagolovok
        if tip == "oblozhka":
            sub = meta.get("oblozhka_sub")
            if sub:
                params["sub"] = sub
            dateplace = meta.get("oblozhka_dateplace")
            if dateplace:
                params["dateplace"] = dateplace
        plan.append((sid, params, ""))
    return plan


def _order(slide_order, tips):
    """slide_order автора + принудительно oblozhka первой, finalnyj последней —
    по ТИПУ (устойчиво к тому, где автор их фактически перечислил)."""
    cover = [s for s in slide_order if tips.get(s) == "oblozhka"]
    final = [s for s in slide_order if tips.get(s) == "finalnyj"]
    middle = [s for s in slide_order if tips.get(s) not in ("oblozhka", "finalnyj")]
    return cover + middle + final


def build(src, out, jobs=None, podbor=True, zanovo=False):
    from slaid import load_illustrations as load_ill  # переиспользуем загрузчик Э2/Э3
    sys.path.insert(0, str(GENERATOR))
    from build_deck import parse_brief, read_text  # READ-ONLY импорт (Я6)

    src = Path(src)
    slajdy_dir = src / "slajdy"
    illustrations_dir = src / "illustracii"  # ИМЯ ПО СПЕЦИФИКАЦИИ (Я2), не "illustrations"
    slide_paths = sorted(slajdy_dir.glob("*/slaid.md"))
    if not slide_paths:
        raise SystemExit("нет слайдов в %s (ищу */slaid.md)" % slajdy_dir)

    brief = src / "brief.md"
    meta = parse_brief(read_text(brief)) if brief.is_file() else {}
    have = {p.parent.name for p in slide_paths}
    # status слайда узнаём, только распарсив карточку — до первого прохода компиляции
    # его не знаем, поэтому лёгкая предпроверка (missing/extra) читает шапки сама,
    # не дожидаясь параллельной сборки (нужно ДО того, как решать `slide_order` по
    # умолчанию, и ошибка тут дешевле, чем после N параллельных компиляций).
    from formaty import parse_card
    status_by_sid, tip_by_sid = {}, {}
    for p in slide_paths:
        params, _ = parse_card(read_text(p), sid=p.parent.name)
        status_by_sid[p.parent.name] = params.get("status", "v_deke")
        # тип нужен П2 (служебные слайды) ДО компиляции — второй раз файлы не читаем
        tip_by_sid[p.parent.name] = params.get("tip_verstki")

    slide_order = meta.get("slide_order") or [sid for sid in sorted(have)
                                               if status_by_sid[sid] != "rezerv"]
    missing = [s for s in slide_order if s not in have]
    if missing:
        raise SystemExit("brief.md называет слайды, которых нет в slajdy/: %s" % missing)
    # "лишний" на диске — ошибка, ТОЛЬКО если он не в резерве: резервный слайд по
    # Я1 §4-бис легально сидит в папке и в slide_order может не значиться вовсе.
    extra = sorted(s for s in have - set(slide_order) if status_by_sid[s] != "rezerv")
    if extra:
        raise SystemExit("в slajdy/ есть слайды (не в резерве), не названные в "
                          "brief.md slide_order: %s" % extra)
    # 🔴 резерв ИСКЛЮЧАЕТСЯ из компиляции безусловно — даже если автор по ошибке
    # (или намеренно, как явная документация) оставил его в slide_order: «лежит в
    # папке, в дек не входит» (Я1 §4-бис) — свойство САМОГО слайда, не манифеста.
    slide_order = [s for s in slide_order if status_by_sid[s] != "rezerv"]

    jobs = jobs or os.cpu_count() or 1
    # 🔴 `fork`, не дефолт macOS (`spawn`). Компиляция слайда — регэкспы над
    # несколькими КБ текста, микросекунды; `spawn` пересобирает интерпретатор и
    # заново импортирует модули НА КАЖДЫЙ воркер (десятки мс) — накладные расходы
    # старта перевешивают всю полезную работу разом (замерено этим же прогоном:
    # `-j 15` на 15 слайдах стабильно МЕДЛЕННЕЕ `-j 1`, реальный wall time 0.26с
    # против 0.15с). `fork` дешевле в разы (не пересобирает интерпретатор с нуля);
    # если и он не даёт выигрыша — это законный отрицательный результат про ЭТУ
    # задачу (лёгкая CPU-работа), а не брак реализации, и назван в отчёте как есть.
    # Компилируем ТОЛЬКО то, что реально войдёт в дек — резервные слайды могут быть
    # намеренно недописаны и не обязаны собираться (Я1 §4-бис: «в дек не входит»).
    to_compile = [p for p in slide_paths if p.parent.name in slide_order]

    if podbor:
        _podobrat_tipografiku(to_compile, zanovo=zanovo)

    ctx = mp.get_context("fork") if hasattr(os, "fork") else None
    with ProcessPoolExecutor(max_workers=jobs, mp_context=ctx) as ex:
        results = list(ex.map(_compile_one, [str(p) for p in to_compile]))

    by_id = {sid: (tip, status, ills, css, html, n_scenes)
              for sid, tip, status, ills, css, html, n_scenes in results}

    # П2: служебные слайды порождаются ЗДЕСЬ, а не читаются с диска — файла у них
    # нет и не будет. Компилируются в этом же процессе, не в пуле: их максимум три,
    # а `_compile_one` умеет только путь к .md.
    from formaty import render_body
    from tipy import compile_tip
    from build_deck import max_scenes  # noqa: E402  (READ-ONLY импорт, Я6)
    from slaid import load_math_cache
    math = load_math_cache(src)
    sluzhebnye = plan_sluzhebnyh(meta, {s: tip_by_sid[s] for s in slide_order}, zanyatye_sid=have)
    for sid, params, tekst_md in sluzhebnye:
        body_html = render_body(tekst_md, acc_tag="span", math=math, sid=sid) if tekst_md else ""
        params["_math"] = math
        css, html = compile_tip(sid, params, body_html)
        by_id[sid] = (params["tip_verstki"], "v_deke", params["illustracii"],
                       css, html, max_scenes(html))
        print("служебный слайд порождён генератором: %s (%s)" % (sid, params["tip_verstki"]))
    # обложка/финальный встанут по типу в `_order`; визитка — сразу за обложкой,
    # то есть в НАЧАЛО авторского порядка.
    slide_order = [s for s, p, _ in sluzhebnye if p["tip_verstki"] != "finalnyj"] + slide_order \
        + [s for s, p, _ in sluzhebnye if p["tip_verstki"] == "finalnyj"]

    tips = {sid: tip for sid, (tip, _, _, _, _, _) in by_id.items()}
    order = _order(slide_order, tips)

    all_ills = []
    seen_ill = set()
    for sid in order:
        for stem in by_id[sid][2]:
            if stem not in seen_ill:
                seen_ill.add(stem)
                all_ills.append(stem)
    templates = load_ill(all_ills, illustrations_dir) if all_ills else ""

    all_css = "\n".join(by_id[sid][3] for sid in order)
    sections = "\n".join(
        '<section class="slide" id="%s" data-scenes="%d">\n%s\n</section>'
        % (sid, by_id[sid][5], by_id[sid][4])
        for sid in order)
    # 🔴 каскад ОДИН на весь дек (общий <style>) — обязан покрывать МАКСИМУМ сцен
    # среди всех слайдов, не только последнего скомпилированного (Э8 захода
    # kartochka-i-sborka, критерий 4; см. slaid.py — та же дыра без этого).
    n_scenes_dek = max([1] + [by_id[sid][5] for sid in order])

    from tipy import GLOBAL_CSS
    from build_deck import scene_cascade_css  # noqa: E402  (READ-ONLY импорт, Я6)
    fonts_css = read_text(SKELETON / "fonts" / "faces.css")
    katex_css = read_text(SKELETON / "katex.css")  # см. slaid.py — Э5 захода solver-vmeshcheniya
    tokens_css = read_text(SKELETON / "tokens.css")
    base_css = read_text(SKELETON / "base.css").replace("{{SCENE_CASCADE}}", scene_cascade_css(n_scenes_dek))
    # узор углов темы — ОТДЕЛЬНЫМ файлом, а не в base.css: тот читают оба движка,
    # и деки чужих лекций получили бы узор «Теорката» (заход primenenie-vizuala,
    # Ш5; причина расписана в шапке uzor.css)
    uzor_css = read_text(SKELETON / "uzor.css")
    engine_js = read_text(SKELETON / "engine.js")

    doc = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>%(title)s</title>
<style>
%(fonts)s
%(katex)s
%(tokens)s
%(base)s
%(uzor)s
%(global_css)s
%(css)s
</style>
</head>
<body>
<div id="stage"><div id="deck">
%(sections)s
</div></div>
<div id="hint">← → листать · F — экран · B — чёрный</div>
%(templates)s
<script>%(engine)s</script>
</body>
</html>
""" % {
        "title": meta.get("title", src.name),
        "fonts": fonts_css,
        "katex": katex_css,
        "tokens": tokens_css,
        "base": base_css,
        "uzor": uzor_css,
        "global_css": GLOBAL_CSS,
        "css": all_css,
        "sections": sections,
        "templates": templates,
        "engine": engine_js,
    }

    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    n_rezerv = sum(1 for s in status_by_sid.values() if s == "rezerv")
    return len(order), n_rezerv, out


def main():
    ap = argparse.ArgumentParser(description="Параллельная сборка дека из папки лекции")
    ap.add_argument("src", help="папка <лекция> (содержит slajdy/, illustracii/, brief.md)")
    ap.add_argument("-o", "--out", required=True, help="путь выхода .html")
    ap.add_argument("-j", "--jobs", type=int, default=None, help="число процессов (по умолчанию — ядра)")
    ap.add_argument("--bez-podbora", action="store_true",
                     help="не подбирать типографику солвером — собрать как есть "
                          "(умолчание: подбор ВКЛЮЧЁН, Р3 захода porcia-1-zamknut-konvejer)")
    ap.add_argument("--zanovo", action="store_true",
                     help="переподобрать типографику ВСЕЙ лекции, не считаясь ни с меткой "
                          "`podbor_avto`, ни с легаси-значениями в шапках; `verstka_reshena: da` "
                          "по-прежнему неприкосновенно (П1 захода tri-provodki)")
    args = ap.parse_args()
    from formaty import FormatSlaida  # noqa: E402  (тот же приём, что slaid.py main())
    try:
        n, n_rezerv, out = build(args.src, args.out, jobs=args.jobs,
                                 podbor=not args.bez_podbora, zanovo=args.zanovo)
    except FormatSlaida as e:
        print("ОШИБКА: %s" % e, file=sys.stderr)
        return 1
    print("собран дек: слайдов в деке %d, в резерве %d → %s" % (n, n_rezerv, out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
