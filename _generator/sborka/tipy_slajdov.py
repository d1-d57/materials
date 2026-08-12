#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Реестр типов СЛАЙДА (не путать с `tipy.py` — реестром типов ВЁРСТКИ) — пять
типов фазы 2, раскладка каждого дословно из `TIPOLOGIA-SLAJDOV.md` части 3.1
(заход porozhdenie-kartochki). Числа и состав НЕ сочиняются здесь: это перенос
таблицы

    | тип | раскладка | центральный | необязательны | L2 |
    | Т1 Введение понятия | Н? · О · П? · У? | О | Н,П,У | 5 |
    | Т2 Построение        | Н? · О? · У · Д? | У | Н,О,Д* | 3 |
    | Т3 Запрет            | У · П? · Д        | У (первый) | П | 4 |
    | Т4 Разделитель        | Н                  | Н | — | 2 |
    | Т5 Итог               | Н                  | Н | — | 2 |

в структуру данных, которую `porodit_slaid.py` раскладывает по слотам. Раскладка
Т4/Т5 побитово одинакова (см. типологию часть 4 п.1) — различаются только
`nazvanie` (назначение вперёд/назад читатель различает сам, генератору это не
нужно, блоков это не меняет).

Буквы — обозначения типологии: **Н** narrativ · **О** opredelenie · **П** primer ·
**У** utverzhdenie · **Д** dokazatelstvo. Порядок слота в списке — порядок блока
на слайде («у Т3 `У` первый» — не украшение, а то, что проверяет гейт Ф2.3/А9).
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
        ],
    },
    "Т2": {
        "nazvanie": "Построение",
        "slots": [
            _slot("narrativ", required=False, multi=True),
            _slot("opredelenie", required=False),
            _slot("utverzhdenie", required=True, central=True),
            _slot("dokazatelstvo", required=False),
        ],
    },
    "Т3": {
        "nazvanie": "Запрет",
        "slots": [
            _slot("utverzhdenie", required=True, central=True),
            _slot("primer", required=False),
            _slot("dokazatelstvo", required=True),
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
