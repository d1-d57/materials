#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Формат карточки слайда (Э1 захода kartochka-i-sborka) и markdown её тела.

  <лекция>/slajdy/<imya>/slaid.md:
    ---
    imya: izomorfizm-vidov
    nazvanie: Изоморфизм комбинаторных видов
    zagolovok_na_ekrane: ""
    zachem: зритель должен увидеть, что изоморфизм видов — это не совпадение чисел
    akcent: согласованность, а не равенство количеств
    kommentarij_lektoru: здесь я останавливаюсь и спрашиваю зал
    minuty: 6
    vazhnost: opornyj
    byudzhet_slov: 55
    tip_verstki: polosa_gorizontalnaya
    liniya: 44
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
from build_deck import render_md, render_inline_md  # noqa: E402  (read-only импорт, см. докстроку)

import bloki  # noqa: E402

FRONT_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.S)
LIST_ITEM_RE = re.compile(r"^\s*-\s*(.+?)\s*$")
DICT_ITEM_RE = re.compile(r"^\s*-\s*\{(.*)\}\s*$")
KEY_RE = re.compile(r"^([A-Za-z_]+):\s*(.*)$")
INLINE_LIST_RE = re.compile(r"^\[(.*)\]$")
INLINE_DICT_RE = re.compile(r"^\{(.*)\}$")

# Гейт (Я1 §6) требует эти поля заполненными — компилятор их не требует (см.
# докстрику), но список нужен и гейту, и bootstrap'у (Э3) для пометки «заполнить» —
# один источник правды на оба.
OBYAZATELNYE_POLYA = ("imya", "nazvanie", "zachem", "akcent", "minuty",
                       "vazhnost", "tip_verstki", "liniya", "byudzhet_slov")
ZAPOLNIT = "заполнить"


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
    params, body = parse_front_matter(text, sid)
    if "tip_verstki" not in params:
        raise FormatSlaida("слайд %s: обязательное поле 'tip_verstki' отсутствует" % sid)
    for lst_key in ("illustracii", "vvodit", "opiraetsya_na", "bez_opredeleniya_namerenno"):
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


def render_body(body_md, acc_tag="span", math=None):
    """markdown тела (уже плоский, после `parse_slide`/`bloki.render_section_markdown`)
    → HTML. `math` — кэш формул KaTeX (Э5 захода solver-vmeshcheniya: подключён к
    новому пути, приём тот же, что `build_deck.py` уже применяет для каскада сцен —
    просто читает `<лекция>/math/katex.json`, если он есть). Без кэша (`math=None`
    или формулы в нём нет) — видимый маркер `⟦MISSING-MATH:...⟧` (НАМЕРЕННО, лучше
    кричащий пробел, чем молча съеденная формула)."""
    if not body_md.strip():
        return ""
    return render_md(body_md, math or {}, acc_tag)
