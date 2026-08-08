#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Формат карточки слайда (Э1 захода kartochka-i-sborka) и markdown её тела.

  <лекция>/slajdy/<imya>/slaid.md:
    ---
    imya: izomorfizm-vidov
    nazvanie: Изоморфизм комбинаторных видов
    zagolovok_na_ekrane: ""
    tip_idei: definition
    zachem: зритель должен увидеть, что изоморфизм видов — это не совпадение чисел
    akcent: согласованность, а не равенство количеств
    centralnyj_blok: изоморфизм видов
    kommentarij_lektoru: здесь я останавливаюсь и спрашиваю зал
    minuty: 6
    vazhnost: opornyj
    byudzhet_slov: 55
    tip_verstki: polosa_gorizontalnaya
    liniya: 44
    matematika_iz: [Спаривание, Двойственный базис]
    illustracii: [kvadrat-estestvennosti]
    vvodit: [изоморфизм видов]
    opiraetsya_na:
      - {termin: биекция, vvedeno: s03}
    bez_opredeleniya_namerenno:
      - {termin: функтор, poyasnyaetsya: на конкретном примере, formalno: s11}
    status: v_deke
    ---
    ## Математика — развёрнуто
    ### [narrativ] зачем вообще сравнивать виды
    …
    ## Текст слайда — сжато
    ### [narrativ] зачем сравнивать виды
    …
    ## Правки
    - …

Полная спецификация полей и разметки — Я1 канала: `kartochka-slajda.md`. Это
РАСШИРЕНИЕ прежнего формата (был плоский `tip`/`zagolovok`/`liniya`/`illustracii`
без карточных полей) — переименованы `tip`→`tip_verstki`, `zagolovok`→
`zagolovok_na_ekrane` дословно по спецификации, второго словаря имён не заводим.

Шапка — свой мини-парсер (flat key:value, список строк `- x`, список словарей
`- {k: v, …}`, инлайн-список `[a, b]`, инлайн-словарь `{k: v}` одной строкой)
— НЕ `parse_brief` из build_deck.py (тот диалект brief.md проще, READ-ONLY, не
трогаем). Markdown тела блоков — ИМПОРТ `render_md`/`render_inline_md` из
build_deck.py, READ-ONLY: не плодить второй диалект markdown в фабрике.

Компилятор (этот модуль) — ЛЕНИВЫЙ: жёстко требует только то, без чего в принципе
нельзя собрать HTML (`tip_verstki`). Полнота карточки (обязательные поля Я1 §6,
состав блоков, бюджет слов, резолв иллюстраций/терминов) — забота ГЕЙТА
(`gejt_kartochki.py`, Э4), не компилятора: слайд с недописанной карточкой обязан
собираться (иначе не на чем гонять гейт), но не обязан проходить гейт.
"""
import re
import sys
from pathlib import Path

_GENERATOR = Path(__file__).resolve().parents[1]
if str(_GENERATOR) not in sys.path:
    sys.path.insert(0, str(_GENERATOR))
from build_deck import (render_md, render_inline_md,  # noqa: E402  (read-only импорт, см. докстроку)
                         known_classes, find_unknown_classes)

import bloki  # noqa: E402

FRONT_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.S)

# Р1б захода porcia-1-zamknut-konvejer (П0: «дисциплина, которую невозможно
# игнорировать физически»): `bootstrap_lekcii.py` вшивает в каждую порождённую
# карточку слайда, СТРОГО до шапки, HTML-комментарий «что дальше с этим файлом»
# — какая фаза что заполняет и какой командой это проверяется, поимённо. Формат
# строки внутри комментария фиксирован и машиночитаем: `gejt_kartochki.py`
# гейтует на нём (см. Я1 §6-бис). Строка вида:
#   ФАЗА 2 (раскадровка): решить поля шапки :: python3 _generator/sborka/gejt_kartochki.py <лекция>
LIFECYCLE_RE = re.compile(r"^<!--(.*?)-->\s*", re.S)
FAZA_STROKA_RE = re.compile(r"^ФАЗА\s+(\d+)[^:\n]*:\s*(.+?)\s*::\s*(\S.*)$", re.M)


def strip_lifecycle_block(text):
    """Карточка слайда → (блок «что дальше»: str|None, остальной текст: str).
    Парсеру шапки блок не нужен — отрезаем ЗДЕСЬ, один раз, прозрачно для всех
    вызывающих `parse_card`/`parse_front_matter`. Блока нет (старая карточка,
    чужой формат) → (None, text) без изменений."""
    m = LIFECYCLE_RE.match(text)
    return (m.group(1), text[m.end():]) if m else (None, text)
LIST_ITEM_RE = re.compile(r"^\s*-\s*(.+?)\s*$")
DICT_ITEM_RE = re.compile(r"^\s*-\s*\{(.*)\}\s*$")
KEY_RE = re.compile(r"^([A-Za-z_]+):\s*(.*)$")
INLINE_LIST_RE = re.compile(r"^\[(.*)\]$")
INLINE_DICT_RE = re.compile(r"^\{(.*)\}$")

# Гейт (Я1 §6) требует эти поля заполненными — компилятор их не требует (см.
# докстрику), но список нужен и гейту, и bootstrap'у (Э3) для пометки «заполнить» —
# один источник правды на оба.
OBYAZATELNYE_POLYA = ("imya", "nazvanie", "zachem", "tip_idei", "akcent", "minuty",
                       "vazhnost", "tip_verstki", "liniya", "byudzhet_slov")
ZAPOLNIT = "заполнить"

# Р захода format-kartochki-faza-1: типология ИДЕИ СЛАЙДА — закрытый список из
# `fazy-1-2-plan.md §2`, выведенный замером 201 слайда по шести декам корпуса.
# Живёт ЗДЕСЬ, а не в гейте: список нужен и гейту (проверить значение), и
# `bootstrap_lekcii.py` (напечатать допустимые рядом с пометкой «заполнить») —
# один источник на оба, как и `OBYAZATELNYE_POLYA` выше.
#
# ⚠ Список ЗАКРЫТЫЙ, но НЕ ОКОНЧАТЕЛЬНЫЙ (`fazy-1-2-plan.md §2` дословно): он
# покрывает шесть деков, а не всю математику. Слайд, не ложащийся ни в один тип, —
# повод обсудить НОВЫЙ тип, а не тихо подобрать ближайший; сообщение гейта обязано
# говорить именно это, иначе исполнитель молча подгонит слайд под чужую полку.
TIPY_IDEI = ("definition", "proof_step", "narrative", "problem",
              "divider", "cover", "vizitka", "closing")

# Заход uroki-faz-1-2-v-disciplinu, У12: подмножество TIPY_IDEI, у которого по
# определению (fazy-1-2-plan.md §2 — «служебные: титул, визитка, финал») нет
# содержания — им нечего вводить и не на что опираться. Гейт выхода фазы 1
# использует этот список, чтобы не требовать vvodit/opiraetsya_na там, где
# требовать нечего.
TIPY_IDEI_BEZ_SODERZHANIYA = ("divider", "cover", "vizitka", "closing")

# Заход svedenie-i-smeta, Э1.4: список ОСВОБОЖДЁННЫХ ОТ СВЯЗЕЙ шире списка
# служебных выше, и путать их нельзя — у них разный смысл. Служебному типу нечего
# вводить, потому что у него нет СОДЕРЖАНИЯ вовсе. Слайду типа `narrative`
# содержание положено, но связей может законно не быть: вступление пересказывает
# прошлую лекцию, итог собирает уже сказанное — ни то, ни другое не вводит нового
# понятия и не опирается на конкретное.
#
# 🔴 Освобождение ПЕРМИССИВНО, а не запретительно: narrative-слайд, который реально
# на что-то опирается, поля заполняет (в живой L2 так и сделано — `teorema-brauera`,
# tip_idei: narrative, opiraetsya_na непуст). Освобождение снимает ТРЕБОВАНИЕ, а не
# возможность.
#
# ЦЕНА, из-за которой список заведён: У12 включил проверку по
# TIPY_IDEI_BEZ_SODERZHANIYA, и `--faza 1` покраснел на `napominanie` и `itog` —
# двух законно-пустых narrative-карточках из пятнадцати. Два ложных красных из трёх
# на живой лекции — ровно та доля, после которой гейт отключают целиком. При этом
# сам код уже противоречил своему комментарию: комментарий в `gejt_kartochki.py`
# говорил «слайд типа narrativ/divider может законно ничего не вводить», а
# освобождение narrativ не покрывало.
TIPY_IDEI_BEZ_TREBOVANIYA_SVYAZEJ = TIPY_IDEI_BEZ_SODERZHANIYA + ("narrative",)

# Спецзначение `centralnyj_blok` — те самые 6 слайдов из 201, где центра нет по
# существу (списки однородных пунктов: набор задач, меню будущих тем). Гейт выхода
# фазы 1 требует «ровно один блок помечен центральным (исключение — слайд-
# перечисление, помечается ЯВНО)» — вот это и есть «явно».
CENTRALNYJ_PERECHISLENIE = "perechislenie"


class FormatSlaida(Exception):
    pass


def _split_top_level(s, sep=","):
    """Разбить по `sep`, ИГНОРИРУЯ вхождения внутри "…" — значению флоу-словаря
    (Я1 `gde:`/`kachestvo:` часто несут живую прозу) законно нужна запятая
    внутри себя; naивный `str.split(sep)` её рвёт. Найдено на живом тексте
    Э8 захода kartochka-i-sborka: `gde: "… копия трёх слайдов, не всей лекции"`."""
    parts, buf, in_quotes = [], [], False
    for ch in s:
        if ch == '"':
            in_quotes = not in_quotes
            buf.append(ch)
        elif ch == sep and not in_quotes:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    parts.append("".join(buf))
    return parts


def _parse_flow_dict(inner):
    """'termin: биекция, vvedeno: s03' → {'termin': 'биекция', 'vvedeno': 's03'}.
    Плоский диалект: без вложенных скобок — ровно то, что несут карточные поля
    (Я1 §1/§2), не универсальный YAML. Запятая внутри значения — легальна,
    если значение взято в кавычки (`gde: "…, …"`)."""
    d = {}
    if not inner.strip():
        return d
    for piece in _split_top_level(inner, ","):
        if ":" not in piece:
            raise FormatSlaida("не могу разобрать пару 'ключ: значение' в %r" % piece)
        k, v = piece.split(":", 1)
        d[k.strip()] = v.strip().strip('"')
    return d


def parse_front_matter(text, sid="?"):
    """YAML-лайт шапка (между `---`) → (params: dict, body: str). Общий парсер
    для карточки слайда (`slaid.md`) И карточки лекции (`brief.md`) — оба несут
    один и тот же диалект шапки (Я1 §1/§2), различается только набор полей."""
    m = FRONT_RE.match(text)
    if not m:
        raise FormatSlaida("%s: нет YAML-шапки (---...---)" % sid)
    head, body = m.group(1), m.group(2)
    params, cur_list = {}, None
    for line in head.splitlines():
        if not line.strip():
            cur_list = None
            continue
        km = KEY_RE.match(line)
        if km:
            key, val = km.group(1), km.group(2).strip()
            cur_list = None
            if val == "":
                cur_list = key
                params[key] = []
            else:
                lm = INLINE_LIST_RE.match(val)
                dm = INLINE_DICT_RE.match(val)
                if lm:
                    inner = lm.group(1).strip()
                    params[key] = [x.strip() for x in inner.split(",") if x.strip()] if inner else []
                elif dm:
                    params[key] = _parse_flow_dict(dm.group(1))
                else:
                    params[key] = val.strip('"')
            continue
        dim = DICT_ITEM_RE.match(line)
        if dim and cur_list is not None:
            params[cur_list].append(_parse_flow_dict(dim.group(1)))
            continue
        lim = LIST_ITEM_RE.match(line)
        if lim and cur_list is not None:
            params[cur_list].append(lim.group(1))
            continue
        raise FormatSlaida("%s: непонятная строка шапки: %r" % (sid, line))
    return params, body.strip("\n")


def parse_card(text, sid="?"):
    """.md карточки слайда → (params: dict, raw_body: str) — шапка нормализована
    (illustracii/vvodit/opiraetsya_na/bez_opredeleniya_namerenno всегда списки,
    status по умолчанию 'v_deke'), raw_body — тело КАК ЕСТЬ, разделы ещё не разобраны."""
    _, text = strip_lifecycle_block(text)
    params, body = parse_front_matter(text, sid)
    if "tip_verstki" not in params:
        raise FormatSlaida("слайд %s: обязательное поле 'tip_verstki' отсутствует" % sid)
    for lst_key in ("illustracii", "vvodit", "opiraetsya_na",
                     "bez_opredeleniya_namerenno", "matematika_iz"):
        params.setdefault(lst_key, [])
        if isinstance(params[lst_key], str):
            params[lst_key] = [params[lst_key]]
    params.setdefault("status", "v_deke")
    return params, body


def parse_slide(text, sid="?"):
    """.md слайда → (params: dict, body_md: str) — body_md ПЛОСКИЙ markdown,
    готовый к `render_body`: это раздел «Текст слайда — сжато», заголовки блоков
    (`### [tip] мысль`) убраны (Я1: «ничего из шапки/заголовков блоков на экран
    не выводится»). Тело пустое (K3, слайд без текста — законный случай) →
    body_md = "". Компилятору (`slaid.py`/`deck.py`) НЕ нужна структура блоков —
    только готовый к рендеру текст; кто хочет структуру (гейт) — зовёт `parse_card`
    + `bloki.parse_sections` сам."""
    params, raw_body = parse_card(text, sid)
    if not raw_body.strip():
        return params, ""
    sections = bloki.parse_sections(raw_body, sid=sid)
    body_md = bloki.render_section_markdown(sections["tekst"])
    return params, body_md


def render_body(body_md, acc_tag="span", math=None, sid=None):
    """markdown тела (уже плоский, после `parse_slide`/`bloki.render_section_markdown`)
    → HTML. `math` — кэш формул KaTeX (Э5 захода solver-vmeshcheniya: подключён к
    новому пути, приём тот же, что `build_deck.py` уже применяет для каскада сцен —
    просто читает `<лекция>/math/katex.json`, если он есть). Без кэша (`math=None`
    или формулы в нём нет) — видимый маркер `⟦MISSING-MATH:...⟧` (НАМЕРЕННО, лучше
    кричащий пробел, чем молча съеденная формула).

    🔴 Опечатка в `{.имя}` (заход tihie-polomki, П2): раньше `_attrs_from_tag` брала
    ЛЮБУЮ строку после точки, не проверяя её ни против чего — `{.tlsit}` рендерился
    обычным классом без стиля, все гейты зелёные. Проверка ЗДЕСЬ, до `render_md`, а
    не в `build_deck.py:lint()` — `lint()` гейтует только СТАРЫЙ пайплайн
    (`load_source`/`assemble`), а `render_body` — единственная точка, через которую
    и `slaid.py`, и `deck.py` пропускают тело КАЖДОЙ карточки нового пайплайна; здесь
    же есть сырой markdown с реальными номерами строк, которых уже нет у отрендеренного
    HTML в `lint()`."""
    if not body_md.strip():
        return ""
    unknown = find_unknown_classes(body_md, known_classes())
    if unknown:
        name, line = unknown[0]
        raise FormatSlaida(
            "%sкласс '.%s' не найден в словаре скелета (строка %d тела карточки) — "
            "опечатка в {.имя}? Список классов: base.css + tipy.py:GLOBAL_CSS."
            % ("слайд %s: " % sid if sid else "", name, line))
    return render_md(body_md, math or {}, acc_tag)


MISSING_MATH_RE = re.compile(r"⟦MISSING-MATH:(.*?)⟧")


def check_no_missing_math(html, sid, lekcija_dir):
    """`html` несёт `⟦MISSING-MATH:…⟧` → `FormatSlaida` с точной командой чинки
    (заплатка sborka-l2-fazy-4-7, П3). До этой правки `slaid.py`/`deck.py` собирали
    HTML с видимым браком МОЛЧА, rc=0 — та же дыра, от которой уже защищён
    `deck.py` для playwright («деку БЕЗ подбора я не соберу молча»); эта проверка —
    тот же приём для кэша формул."""
    missing = sorted(set(MISSING_MATH_RE.findall(html)))
    if missing:
        raise FormatSlaida(
            "слайд %s: %d формул(ы) нет в кэше math/katex.json — соберите кэш: "
            "`node _generator/sborka/kesh_formul.js %s`. Не отрендерено: %s"
            % (sid, len(missing), lekcija_dir,
               "; ".join("$%s$" % t for t in missing[:5]) + (" …" if len(missing) > 5 else "")))
