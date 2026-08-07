#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Формат слайда (Э1 захода) и markdown его тела.

  <лекция>/src2/slides/<id>.md:
    ---
    tip: polosa_gorizontalnaya
    liniya: 44
    kegl: 1.0
    zagolovok: Комбинаторные виды
    illustracii: [s06-a.svg, s06-b.svg]
    ---
    Основной текст. Markdown.

Шапка — свой мини-парсер (flat key:value + один список), НЕ `parse_brief` из
build_deck.py: тот читает диалект brief.md (`slide_order` списком через все
последующие строки), у слайда шапка другая — списком может быть только
конкретное поле `illustracii`, и после него у слайда снова идут скаляры
(здесь их нет, но парсер обязан не путать «список» и «конец шапки»).
Markdown тела — ИМПОРТ `render_md`/`render_inline_md` из build_deck.py,
READ-ONLY (см. `## ПЛАН` захода): не плодить второй диалект markdown в
фабрике.
"""
import re
import sys
from pathlib import Path

_GENERATOR = Path(__file__).resolve().parents[1]
if str(_GENERATOR) not in sys.path:
    sys.path.insert(0, str(_GENERATOR))
from build_deck import render_md, render_inline_md  # noqa: E402  (read-only импорт, см. докстроку)

FRONT_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.S)
LIST_ITEM_RE = re.compile(r"^\s*-\s*(.+?)\s*$")
KEY_RE = re.compile(r"^([A-Za-z_]+):\s*(.*)$")
INLINE_LIST_RE = re.compile(r"^\[(.*)\]$")


class FormatSlaida(Exception):
    pass


def parse_slide(text, sid="?"):
    """.md слайда → (params: dict, body_md: str)."""
    m = FRONT_RE.match(text)
    if not m:
        raise FormatSlaida("слайд %s: нет YAML-шапки (---...---)" % sid)
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
                if lm:
                    inner = lm.group(1).strip()
                    params[key] = [x.strip() for x in inner.split(",") if x.strip()] if inner else []
                else:
                    params[key] = val.strip('"')
            continue
        lim = LIST_ITEM_RE.match(line)
        if lim and cur_list is not None:
            params[cur_list].append(lim.group(1))
            continue
        raise FormatSlaida("слайд %s: непонятная строка шапки: %r" % (sid, line))
    if "tip" not in params:
        raise FormatSlaida("слайд %s: обязательное поле 'tip' отсутствует" % sid)
    params.setdefault("illustracii", [])
    if isinstance(params["illustracii"], str):
        params["illustracii"] = [params["illustracii"]]
    return params, body.strip("\n")


def render_body(body_md, acc_tag="span"):
    """markdown тела слайда → HTML (без формул-кэша: $…$ здесь рендерится КАК KaTeX
    inline-заглушкой не занимаемся — новый путь пока не несёт math/katex.json, поэтому
    `$…$` передаётся в render_md пустым кэшем; формула, которой нет в кэше, вернётся
    видимым маркером `⟦MISSING-MATH:...⟧` — это НАМЕРЕННО (лучше кричащий пробел,
    чем молча съеденная формула), сцены (`{@N}`) в этом заходе не входят (Э1 их не
    описывает), но `render_md` их пропускает безопасно — не участвуют в разметке типов."""
    if not body_md.strip():
        return ""
    return render_md(body_md, {}, acc_tag)
