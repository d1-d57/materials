#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Реестр типов СЛАЙДА (не путать с `tipy.py` — реестром типов ВЁРСТКИ) — шесть
типов фазы 2. Т1-Т5 раскладка исходно дословно из `TIPOLOGIA-SLAJDOV.md` части 3.1
(заход porozhdenie-kartochki), Т1-Т3 РАЗДВИНУТЫ заходом tipologia-odna-os
(2026-08-13, решения владельца на интервью — не переоткрывать):

    | тип | раскладка | центральный | необязательны | L2 (Э0 замер) |
    | Т1 Введение понятия | Н?* · О · П? · У? · Н?*       | О | Н,П,У | 6 |
    | Т2 Построение        | Н?* · О? · П? · У · П? · Д? · Н?* | У | Н,О,П,Д | 2 |
    | Т3 Запрет            | У · П? · Д · Н?*              | У (первый) | П,Н | 1 |
    | Т4 Разделитель        | Н                              | Н | — | 7 |
    | Т5 Итог               | Н                              | Н | — | 0 |
    | Т6 Служебный          | (см. ниже — состав не проверяется этим реестром) | — | — | 0 |

в структуру данных, которую `porodit_slaid.py` раскладывает по слотам. Раскладка
Т4/Т5 побитово одинакова (см. типологию часть 4 п.1) — различаются только
`nazvanie` (назначение вперёд/назад читатель различает сам, генератору это не
нужно, блоков это не меняет).

🔴 Т1-Т3 несут ДВА необязательных слота `narrativ` — головной (было изначально) и
ХВОСТОВОЙ (заход tipologia-odna-os, п.1 интервью: «завершающий нарратив — законная
фигура, необязательный хвостовой слот в конце раскладки каждого СОДЕРЖАТЕЛЬНОГО
типа»). У Т2 ДВА необязательных слота `primer` — ДО `utverzhdenie` и ПОСЛЕ (п.2
интервью, проверено на живых карточках: `fundamentalnaya-gruppa` несёт пример ДО,
`inyekcii` — ПОСЛЕ; обе позиции нужны по факту, не для симметрии). Т1 сознательно
НЕ несёт слота `dokazatelstvo` (п.3 интервью): добавь его — и Т1 накроет Т2
целиком, а тип, вложенный в другой, — синоним, не тип.

Буквы — обозначения типологии: **Н** narrativ · **О** opredelenie · **П** primer ·
**У** utverzhdenie · **Д** dokazatelstvo. Порядок слота в списке — порядок блока
на слайде («у Т3 `У` первый» — не украшение, а то, что проверяет гейт Ф2.3/А9).

Раскладки ПЕРЕСЕКАЮТСЯ НАРОЧНО (Т4/Т5 совпадают побитово, О·У подходит и Т1, и Т2,
У·Д — и Т2, и Т3) — это НОРМА, не дефект: тип назначается АВТОРОМ на фазе 1/2, а не
выводится из состава блоков машиной (см. `gejt_kartochki.py`, докстрока раздела
про `tip_slaida`); обратная задача «угадать тип по блокам» существует только как
разовая помощь при миграции (`porodit_slaid.py --sverit`), не как правило гейта.
"""
from collections import namedtuple

Slot = namedtuple("Slot", "bukva tip required multi central")

# bukva → tip_bloka (bloki.TIPY_BLOKOV) — обратное используется для сообщений
BUKVA_PO_TIPU = {"narrativ": "Н", "opredelenie": "О", "primer": "П",
                  "utverzhdenie": "У", "dokazatelstvo": "Д"}


def _slot(tip, required, multi=False, central=False):
    return Slot(bukva=BUKVA_PO_TIPU[tip], tip=tip, required=required,
                multi=multi, central=central)


TIPY = {
    "Т1": {
        "nazvanie": "Введение понятия",
        "slots": [
            _slot("narrativ", required=False, multi=True),
            _slot("opredelenie", required=True, central=True),
            _slot("primer", required=False),
            _slot("utverzhdenie", required=False),
            _slot("narrativ", required=False, multi=True),
        ],
    },
    "Т2": {
        "nazvanie": "Построение",
        "slots": [
            _slot("narrativ", required=False, multi=True),
            _slot("opredelenie", required=False),
            _slot("primer", required=False),
            _slot("utverzhdenie", required=True, central=True),
            _slot("primer", required=False),
            _slot("dokazatelstvo", required=False),
            _slot("narrativ", required=False, multi=True),
        ],
    },
    "Т3": {
        "nazvanie": "Запрет",
        "slots": [
            _slot("utverzhdenie", required=True, central=True),
            _slot("primer", required=False),
            _slot("dokazatelstvo", required=True),
            _slot("narrativ", required=False, multi=True),
        ],
    },
    "Т4": {
        "nazvanie": "Разделитель",
        "slots": [_slot("narrativ", required=True, multi=True, central=True)],
    },
    "Т5": {
        "nazvanie": "Итог",
        "slots": [_slot("narrativ", required=True, multi=True, central=True)],
    },
}

# Т6 «Служебный» (Э2 захода tipologia-odna-os) — обложка/визитка/финал/разделитель:
# состав ЗАДАЁТСЯ ГЕОМЕТРИЕЙ (`tipy.py`), не раскладкой блоков, поэтому у него
# сознательно НЕТ ключа в `TIPY` выше (central_slot/raskladka_stroka на нём упали
# бы AssertionError — вызывающая сторона обязана проверить это явно, см.
# `gejt_kartochki.py` — состав блоков Т6 не сверяется с раскладкой вовсе).
TIP_SLUZHEBNYJ = "Т6"

# NE_KLASSIFICIROVAN (клауза 5 критерия готовности захода tipologia-odna-os) —
# ЯВНОЕ временное значение для карточки, которой на миграции Э4 не подошёл ни один
# тип по составу блоков (заранее известен ровно один случай — `kategoriya-vect-iso`,
# О·П·Д без утверждения). Гейт даёт на нём ЖЁЛТОЕ «тип не назначен, ждёт решения
# владельца», не красное и не молчание — и обязан печатать, сколько карточек его
# несут (растёт сверх одной — типология разъезжается, это красный флаг приёмке).
NE_KLASSIFICIROVAN = "NE_KLASSIFICIROVAN"

# Несущие — Ф2.3 закон Г-8 («двух НЕСУЩИХ блоков одного типа не бывает; нарративов
# сколько угодно»): множество типов, для которых слот в раскладке всегда `multi=False`.
NESUSHCHIE = ("opredelenie", "primer", "utverzhdenie")

# Порождается на месте необязательного слота, который решили не заполнять
# (ЧТО ФИНАЛИЗИРОВАНО, п.3): пустой блок с пометкой лучше молча отсутствующего.
NE_ZAPOLNYAEM = "⟦решили не заполнять⟧"


def central_slot(tip_slaida):
    """Тип слайда → его единственный central-слот (Slot). KeyError на неизвестном
    типе — вызывающая сторона обязана проверить `tip_slaida in TIPY` раньше."""
    for s in TIPY[tip_slaida]["slots"]:
        if s.central:
            return s
    raise AssertionError("тип %s не несёт central-слота — дефект реестра" % tip_slaida)


def raskladka_stroka(tip_slaida):
    """Строка вида «Н? · О · П? · У?» — та же нотация, что в TIPOLOGIA-SLAJDOV.md,
    для сообщений об отказе (составитель должен узнать раскладку с первого взгляда)."""
    chasti = []
    for s in TIPY[tip_slaida]["slots"]:
        znak = "" if s.required else "?"
        chasti.append(s.bukva + znak)
    return " · ".join(chasti)


def opisanie(tip_slaida):
    d = TIPY[tip_slaida]
    c = central_slot(tip_slaida)
    return "%s (%s): %s — центральный %s" % (
        tip_slaida, d["nazvanie"], raskladka_stroka(tip_slaida), c.bukva)


def proverit_sostav(tip_slaida, actual_types):
    """Строгий порядковый матч состава карточки (список типов блоков раздела
    «Математика», в порядке появления) против раскладки `tip_slaida` — ядро
    жёсткого гейта Э3 захода tipologia-odna-os. НЕ путать с
    `porodit_slaid._sverit_raskladku`: та разведочная функция намеренно
    ИСКЛЮЧАЕТ narrativ из сверки (нужна была для грубой кандидатуры типа по
    central-блоку до этого захода); здесь narrativ участвует наравне со всеми —
    порядок и позиция хвостового/головного нарратива ЕСТЬ часть раскладки.

    Возвращает (verdict, detail):
      verdict == "OK"      — состав совпал, detail = None
      verdict == "MISSING" — не хватает обязательного блока, detail = его tip
      verdict == "EXTRA"   — блок(и) типа, которому в раскладке НЕТ слота вообще,
                              detail = отсортированный список чужих типов
      verdict == "ORDER"   — все типы блоков раскладке известны, но состав/порядок
                              разошёлся (переставлены, повторены сверх слотов,
                              обязательный есть, но не на своём месте), detail —
                              человекочитаемое пояснение

    Т6 (служебный) сюда не передавать — у него нет ключа в `TIPY`, состав ему
    задаёт геометрия (`tipy.py`), не эта раскладка (см. докстрока `TIP_SLUZHEBNYJ`)."""
    slots = TIPY[tip_slaida]["slots"]
    vse_tipy = {s.tip for s in slots}
    ai = 0
    for slot in slots:
        if slot.multi:
            consumed = 0
            while ai < len(actual_types) and actual_types[ai] == slot.tip:
                ai += 1
                consumed += 1
            if slot.required and consumed == 0:
                if slot.tip in actual_types:
                    return "ORDER", "%s не на своём месте" % slot.tip
                return "MISSING", slot.tip
        else:
            if ai < len(actual_types) and actual_types[ai] == slot.tip:
                ai += 1
            elif slot.required:
                if slot.tip in actual_types:
                    return "ORDER", "%s не на своём месте" % slot.tip
                return "MISSING", slot.tip
    if ai != len(actual_types):
        ostatok = actual_types[ai:]
        chuzhie = sorted({t for t in ostatok if t not in vse_tipy})
        if chuzhie:
            return "EXTRA", ", ".join(chuzhie)
        return "ORDER", "лишние/переставленные блоки: %s" % ", ".join(ostatok)
    return "OK", None
