#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ЧЕТЫРЕ ПРОГРАММНЫХ ГЕЙТА ДЕКА (заход §1а.4). Красное — exit 1.

  python3 src/tools/gates.py           # все четыре
  python3 src/tools/gates.py --table   # + таблица «12 вопросов бота → слайд и сцена»

Каждый куплен ценой, и цена записана у самого гейта. Все четыре ловятся десятком
строк и НЕ ловятся глазами — именно поэтому два из них дожили до живой лекции.

  1. data-scenes на слайде ≥ максимума номеров сцен, которые он использует
  2. каскады раскрытия покрывают ВСЕ сцены, какие есть в деке
  3. в собранном dist нет буквальных {@N}, {blur@N}, {fill@N}
  4. каждый из 12 вопросов бота имеет слайд, сцену вопроса и сцену ответа
"""
import re, sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
FAILS, REPORT = [], []


def say(ok, name, detail=""):
    REPORT.append(("PASS" if ok else "FAIL") + "  " + name +
                  (("\n        " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


# ─────────────────────────────── разбор источника ───────────────────────────────
def slide_ids():
    """Порядок слайдов из brief.md — единственный источник истины порядка."""
    txt = (SRC / "brief.md").read_text(encoding="utf-8")
    m = re.search(r"^slide_order:\s*$(.*?)^---", txt, re.S | re.M)
    return re.findall(r"^\s*-\s*(\S+)\s*$", m.group(1), re.M) if m else []


def scenes_declared():
    """id → data-scenes из slides/<id>.html."""
    out = {}
    for p in sorted((SRC / "slides").glob("*.html")):
        m = re.search(r'data-scenes="(\d+)"', p.read_text(encoding="utf-8"))
        out[p.stem] = int(m.group(1)) if m else 1
    return out


def scenes_used(sid):
    """Максимальный номер сцены, который слайд РЕАЛЬНО использует, и откуда он взят."""
    used = []
    md = SRC / "content" / (sid + ".md")
    if md.is_file():
        t = md.read_text(encoding="utf-8")
        for m in re.finditer(r"\{@(\d+)(?:-(\d+))?[|}]", t):
            used += [int(g) for g in m.groups() if g]
        for m in re.finditer(r"\{(?:blur|fill)@(\d+)\|", t):
            used.append(int(m.group(1)))
    html = SRC / "slides" / (sid + ".html")
    if html.is_file():
        t = html.read_text(encoding="utf-8")
        used += [int(x) for x in re.findall(r'data-scene-(?:from|until)="(\d+)"', t)]
    return (max(used) if used else 1), sorted(set(used))


# ─────────────────────────── гейт 1: data-scenes не мал ───────────────────────────
# ЦЕНА: на живой лекции 27.07 data-scenes был МЕНЬШЕ реального числа сцен, и кликер
# уходил на следующий слайд вместо того, чтобы снять блюр с ответа. Глазами не ловится:
# слайд выглядит нормально, ломается только поведение кликера.
def gate_scenes():
    decl = scenes_declared()
    bad = []
    for sid in slide_ids():
        need, seen = scenes_used(sid)
        have = decl.get(sid)
        if have is None:
            bad.append("%s: нет slides/%s.html" % (sid, sid))
        elif have < need:
            bad.append("%s: data-scenes=%d, а используются сцены %s (нужно ≥ %d)"
                       % (sid, have, seen, need))
    say(not bad, "гейт 1 · data-scenes ≥ максимума используемых сцен", "\n        ".join(bad))
    return max([scenes_declared().get(s, 1) for s in slide_ids()] or [1])


# ─────────────────────── гейт 2: каскады покрывают все сцены ───────────────────────
# ЦЕНА: на живой лекции каскад CSS обрывался на .scene-5 — начиная с шестой сцены
# всё, что должно было проступить, скрывалось, и на экране оставался первый абзац.
# Тоже не ловится глазами, если смотреть слайд только в первой сцене.
def gate_cascade(max_scenes):
    base = (SRC / "base.css").read_text(encoding="utf-8")
    shab = (SRC / "shablon.html").read_text(encoding="utf-8")
    miss = []
    for k in range(2, max_scenes + 1):
        for j in range(2, k + 1):
            if not re.search(r"\.scene-%d\s+\[data-scene-from=\"%d\"\]" % (k, j), base):
                miss.append("base.css: нет .scene-%d [data-scene-from=\"%d\"]" % (k, j))
            if not re.search(r"\.scene-%d\s+\.blur-reveal\[data-reveal=\"%d\"\]" % (k, j), shab):
                miss.append("shablon.html: нет .scene-%d .blur-reveal[data-reveal=\"%d\"]" % (k, j))
    # потолок движка: applyScene снимает классы циклом i = 1..9
    if max_scenes > 9:
        miss.append("движок снимает классы сцен только до .scene-9 (engine.js, applyScene) — "
                    "слайд с %d сценами он не сможет перевести назад" % max_scenes)
    say(not miss, "гейт 2 · каскады покрывают все %d сцен(ы) дека" % max_scenes,
        "\n        ".join(miss[:12] + (["… ещё %d" % (len(miss) - 12)] if len(miss) > 12 else [])))


# ──────────────── гейт 3: разметка распозналась (в dist нет сырых шорткатов) ────────────────
# ЦЕНА: {blur@4|…} с опечаткой (лишний пробел, кириллическая «а» в слове blur) не падает
# ни линтером, ни аудитом — он просто печатается на слайд как текст, и зал видит ответ
# вместе с вопросом. То есть механика вопроса в зал тихо выключается.
def gate_raw():
    dist = SRC / "dist" / "index.html"
    if not dist.is_file():
        say(False, "гейт 3 · в dist нет сырых шорткатов", "нет dist/index.html — сначала build_deck.py")
        return
    t = dist.read_text(encoding="utf-8")
    hits = re.findall(r"\{@\d|\{blur@|\{fill@|\{\.[\w-]+\}", t)
    say(not hits, "гейт 3 · в собранном dist нет буквальных {@N} / {blur@} / {fill@}",
        "найдено: %s" % sorted(set(hits)))


# ──────────────── гейт 4: все 12 вопросов бота отражены на слайдах ────────────────
# ЦЕНА: список вопросов появился ПОСЛЕ того, как заход ушёл в работу (PRAVKI §шапка),
# и сквозное требование «каждый вопрос отражён» держалось только на честном слове.
# Вопрос без места на слайде = лектор задаёт его в воздух, а ответ показать негде.
#
# Карта живёт здесь ДАННЫМИ, а не отдельным .md: документ пришлось бы регистрировать
# в KARTA §6, а зона этого не позволяет. Гейт сверяет карту с ЖИВЫМИ content/*.md.
VOPROSY = [
    # № , о чём вопрос (кратко)                          , слайд           , задан, ответ
    (1,  "в какие точки попадёт за 10 шагов",             "sl-columns",      2, 3),
    (2,  "вероятности после трёх шагов",                  "sl-cells",        2, 3),
    (3,  "как число связано с соседями слева",            "sl-cells",        4, 5),
    (4,  "поменяли О на Р — что с ломаной",               "sl-tri",          1, 2),
    (5,  "траекторий длины 10 в точку 4",                 "sl-team",         4, 5),
    (6,  "сумма квадратов шестой строки",                 "sl-squares",      1, 3),
    (7,  "двое по 10 бросков — поровну орлов",            "sl-pairs",        3, 4),
    (8,  "все хорошие слова длины 3",                     "sl-ban",          2, 3),
    (9,  "хороших длины 10 ровно с тремя О",              "sl-diagonals",    3, 4),
    (10, "траектории длины 4 мимо −1",                    "sl-cliff-return", 2, 3),
    (11, "что даёт отражение начального куска",           "sl-reflect",      3, 4),
    (12, "сколько безопасных всего",                      "sl-telescope",    5, 6),
]


def gate_voprosy():
    decl, order = scenes_declared(), slide_ids()
    bad = []
    for n, about, sid, ask, ans in VOPROSY:
        if sid not in order:
            bad.append("вопрос %d (%s): слайда %s нет в slide_order" % (n, about, sid))
            continue
        have = decl.get(sid, 1)
        if have < max(ask, ans):
            bad.append("вопрос %d (%s): на %s всего %d сцен, а нужны %d и %d"
                       % (n, about, sid, have, ask, ans))
        md = SRC / "content" / (sid + ".md")
        t = md.read_text(encoding="utf-8") if md.is_file() else ""
        # сцена ОТВЕТА обязана быть реально реализована: блюр, шторка или появление абзаца
        realized = (re.search(r"\{(?:blur|fill)@%d\|" % ans, t) or
                    re.search(r"\{@%d[|} ]" % ans, t) or
                    re.search(r"\{@%d[- ]" % ans, t) or
                    re.search(r'data-scene-from="%d"' % ans,
                              (SRC / "slides" / (sid + ".html")).read_text(encoding="utf-8")
                              if (SRC / "slides" / (sid + ".html")).is_file() else ""))
        if not realized and re.search(r'data-sim="', (SRC / "slides" / (sid + ".html")).read_text(encoding="utf-8")):
            # слайд-канвас: текста на нём нет вовсе (§7 разбора — «убрать со слайда
            # текст»), и ответ раскрывает сам канвас через onScene. Требуем только,
            # чтобы сцена ответа существовала — она проверена выше по data-scenes.
            realized = True
        if not realized:
            bad.append("вопрос %d (%s): на %s сцена ответа %d ничего не раскрывает — "
                       "ни блюра, ни появляющегося абзаца" % (n, about, sid, ans))
    say(not bad, "гейт 4 · все 12 вопросов бота имеют слайд, сцену вопроса и сцену ответа",
        "\n        ".join(bad))


def table():
    decl = scenes_declared()
    out = ["", "| № | вопрос | слайд | вопрос звучит | ответ проступает | сцен на слайде |",
           "|---|---|---|---|---|---|"]
    for n, about, sid, ask, ans in VOPROSY:
        out.append("| %d | %s | `%s` | сцена %d | сцена %d | %d |"
                   % (n, about, sid, ask, ans, decl.get(sid, 0)))
    return "\n".join(out)


def main():
    mx = gate_scenes()
    gate_cascade(mx)
    gate_raw()
    gate_voprosy()
    print("\n".join(REPORT))
    if "--table" in sys.argv:
        print(table())
    print("\n" + ("ЧЕТЫРЕ ГЕЙТА ЗЕЛЁНЫЕ" if not FAILS else "КРАСНЫХ ГЕЙТОВ: %d" % len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
