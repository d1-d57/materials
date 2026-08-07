#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Блоки, сцены и разделы тела карточки слайда (Э2 захода kartochka-i-sborka).

Тело карточки (после YAML-шапки, см. `formaty.parse_front_matter`) — три раздела,
каждый начинается строкой `## <заголовок>` ровно в этом порядке:

    ## Математика — развёрнуто
    ### [narrativ] зачем сравнивать виды
    Текст блока. Может быть несколько абзацев.

    ### [opredelenie] изоморфизм видов
    …

    ## Текст слайда — сжато
    ### [narrativ] зачем сравнивать виды
    Совпадение чисел — ещё не совпадение структур.
    …

    ## Правки
    - 2026-08-08 · после первого прогона: убрать второй пример

**Всё тело разбито на блоки без остатка** (Я1 §4) — абзац, не принадлежащий ни
одному блоку (текст до первого `###` внутри раздела «Математика»/«Текст слайда»),
это ошибка, а не «свободный текст». Раздел «Правки» блоков не несёт — свободный
список правок, никогда не компилируется в слайд.

Закрытый список типов — ДОСЛОВНО Я1 §4, семь штук. `vopros_zalu` НЕ существует —
отменён владельцем 2026-08-08 (см. К1 в kartochka-slajda.md): пауза для разговора
с залом — момент МЕЖДУ раскрытием двух блоков, а не отдельный тип.

Сцена/пропуск (`{@N}`, `{@N|…}`) — этот модуль их не разбирает и не трогает: они
живут ВНУТРИ текста блока (`telo`) как обычные символы markdown и уходят в
`render_inline_md`/`render_md` (`build_deck.py`, READ-ONLY импорт) без изменений
на этапе сборки HTML. Здесь блок — единица правки и типизации, а не разметки сцен.
"""
import re
from collections import namedtuple

TIPY_BLOKOV = ("narrativ", "opredelenie", "primer", "utverzhdenie",
               "dokazatelstvo", "itog", "uprazhnenie")

ZAGOLOVKI = ("Математика — развёрнуто", "Текст слайда — сжато", "Правки")
KEY_MATEMATIKA, KEY_TEKST, KEY_PRAVKI = ZAGOLOVKI

SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)
BLOCK_RE = re.compile(r"^###\s+\[([a-z_]+)\]\s+(.+?)\s*$", re.M)

Block = namedtuple("Block", "tip mysl telo")


class FormatBlokov(Exception):
    pass


def _split_sections(raw_body, sid):
    """raw_body → {загоовок: текст_раздела}, в порядке появления. Не хватает
    хотя бы одного из трёх канонических заголовков (когда тело вообще не пусто) —
    ошибка: тело либо ПУСТО целиком (K3, слайд без текста), либо размечено
    полностью."""
    matches = list(SECTION_RE.finditer(raw_body))
    if not matches:
        raise FormatBlokov(
            "слайд %s: тело не пусто, но нет ни одного раздела '## …' "
            "(нужны все три: %s)" % (sid, ", ".join(ZAGOLOVKI)))
    out = {}
    for i, m in enumerate(matches):
        title = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(raw_body)
        out[title] = raw_body[start:end]
    missing = [z for z in ZAGOLOVKI if z not in out]
    if missing:
        raise FormatBlokov(
            "слайд %s: не хватает раздела(ов) тела: %s (нужны все три: %s)"
            % (sid, ", ".join(missing), ", ".join(ZAGOLOVKI)))
    return out


def _parse_blocks(section_text, sid, zagolovok_razdela):
    """текст раздела → (orphan: str|None, [Block]). `orphan` — текст ДО первого
    '### [tip] мысль' в разделе, если он не пуст (Я1 §6: «каждый абзац тела
    принадлежит блоку»); гейт решает, ошибка это или нет, здесь — только факт."""
    matches = list(BLOCK_RE.finditer(section_text))
    orphan = section_text[:matches[0].start()].strip() if matches else section_text.strip()
    orphan = orphan or None
    blocks = []
    for i, m in enumerate(matches):
        tip, mysl = m.group(1), m.group(2)
        if tip not in TIPY_BLOKOV:
            raise FormatBlokov(
                "слайд %s, раздел «%s»: тип блока '%s' неизвестен. Допустимы: %s"
                % (sid, zagolovok_razdela, tip, ", ".join(TIPY_BLOKOV)))
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(section_text)
        telo = section_text[start:end].strip("\n")
        blocks.append(Block(tip=tip, mysl=mysl.strip(), telo=telo))
    return orphan, blocks


def parse_sections(raw_body, sid="?"):
    """raw_body (после шапки) → dict:
        matematika: [Block]   tekst: [Block]   pravki: str (сырой текст раздела)
        orphan_matematika / orphan_tekst: str|None — абзац вне блока, если есть
    Тело целиком пустое (K3) — вызывающая сторона (formaty.parse_slide) сюда не
    попадает вовсе, это НЕ забота этого модуля."""
    secs = _split_sections(raw_body, sid)
    orph_m, bloki_m = _parse_blocks(secs[KEY_MATEMATIKA], sid, KEY_MATEMATIKA)
    orph_t, bloki_t = _parse_blocks(secs[KEY_TEKST], sid, KEY_TEKST)
    return {
        "matematika": bloki_m,
        "tekst": bloki_t,
        "pravki": secs[KEY_PRAVKI].strip("\n"),
        "orphan_matematika": orph_m,
        "orphan_tekst": orph_t,
    }


def check_composition(sections):
    """Состав блоков «Текст слайда» обязан СОВПАДАТЬ с «Математикой» по
    (tip, mysl) в том же порядке — Я1 §6: «структура блоков во втором разделе
    совпадает с первым по составу», Я1 §3: «меняется форма, не состав».
    Возвращает список расхождений (пустой — состав совпал)."""
    a = [(b.tip, b.mysl) for b in sections["matematika"]]
    b = [(b.tip, b.mysl) for b in sections["tekst"]]
    if a == b:
        return []
    issues = []
    if len(a) != len(b):
        issues.append("разное число блоков: «Математика» %d, «Текст слайда» %d" % (len(a), len(b)))
    for i in range(min(len(a), len(b))):
        if a[i] != b[i]:
            issues.append("блок %d: «Математика» [%s] %s ≠ «Текст слайда» [%s] %s"
                           % (i + 1, a[i][0], a[i][1], b[i][0], b[i][1]))
    if len(a) != len(b):
        extra = a[len(b):] if len(a) > len(b) else b[len(a):]
        chej = "«Математике»" if len(a) > len(b) else "«Тексту слайда»"
        for tip, mysl in extra:
            issues.append("блок [%s] %s есть только в %s" % (tip, mysl, chej))
    return issues


def render_section_markdown(blocks):
    """[Block] → плоский markdown (тела блоков через пустую строку) — то, что
    компилятор (`formaty.render_body`) скармливает `render_md`. Заголовки блоков
    (`### [tip] мысль`) на экран НИКОГДА не выводятся (Я1 §2, §4) — только текст."""
    return "\n\n".join(b.telo for b in blocks if b.telo.strip())
