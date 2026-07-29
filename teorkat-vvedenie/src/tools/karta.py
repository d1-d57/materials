#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Карта перехода 55 → 32: единственный дом соответствия «новый слайд → старые слайды».

  python3 teorkat-vvedenie/src/tools/karta.py            # напечатать карту и сверку
  python3 teorkat-vvedenie/src/tools/karta.py --plotnost # перенести ступени по карте

Зачем отдельным файлом: карта нужна ТРЁМ инструментам сразу — `sverstat.py` (перенос
ступеней и `PRAVKI`), гейту Р1 render-identity (какие слайды обязаны совпасть
геометрией со старым деком) и верификатору (у каждого старого слайда должен быть
новый дом). Три копии одной таблицы разъехались бы молча.

ОТКУДА ВЗЯТА, а не угадана. Соответствие «старый раздел ленты → новый раздел»
выписано владельцем ленты явной таблицей в шапке `raskadrovka/teksty/A-krasivaya.md`
(`> поле:mn **Куда уехали старые разделы (для захода вёрстки).**`, пять строк по
блокам). Мостик «раздел ленты → слайд дека» проверен КОДОМ, а не догадкой:
`porodit.main` строит `ids = ["s%02d" % (i+1)]` по `slides[1:]`, то есть обложка
(раздел 1) слайдом не становится и старый слайд `sNN` = старый раздел `NN+1`.
Отсюда: новый слайд `k` собран из старых слайдов `{раздел−1}` своей группы.
"""
import json, re, subprocess, sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SRC = TOOLS.parent
REPO = TOOLS.parents[2]
TOCHKA_OTKATA = "82a5cfc"        # старый дек из 55 слайдов, вёрстка Фазы II

# новый раздел ленты → [старые разделы ленты]; 1 = обложка в обеих нумерациях
GRUPPY = {
    1: [1], 2: [2], 3: [3], 4: [4], 5: [5], 6: [6], 7: [7], 8: [8],
    9: [9, 10], 10: [11],
    11: [12], 12: [13, 14], 13: [15, 16, 17], 14: [18, 19, 20, 21],
    15: [22, 23, 24], 16: [25, 26], 17: [27, 28],
    18: [29, 30, 31, 32], 19: [33, 34, 35],
    20: [36, 37], 21: [38, 39], 22: [40], 23: [41, 42], 24: [43], 25: [44, 45],
    26: [46], 27: [47, 48], 28: [49], 29: [50, 51], 30: [52], 31: [53, 54],
    32: [55], 33: [56],
}


def karta():
    """новый id слайда → [старые id слайдов]. Обложка (группа 1) слайдом не была."""
    out = {}
    for novy, starye in sorted(GRUPPY.items()):
        if novy == 1:
            continue
        out["s%02d" % (novy - 1)] = ["s%02d" % (r - 1) for r in starye]
    return out


def klass(novy_id, k=None):
    k = k if k is not None else karta()
    return "A" if len(k[novy_id]) == 1 else "B"


def sverka():
    """Карта обязана быть биекцией на разделы 1..56 и на слайды s01..s55."""
    vse = [r for g in GRUPPY.values() for r in g]
    beda = []
    if sorted(vse) != list(range(1, 57)):
        beda.append("разделы ленты покрыты не ровно один раз: %d значений, "
                    "дубли %s" % (len(vse), [x for x in set(vse) if vse.count(x) > 1]))
    if sorted(GRUPPY) != list(range(1, 34)):
        beda.append("новых групп не 1..33")
    k = karta()
    stary = [s for v in k.values() for s in v]
    if len(set(stary)) != 55 or len(stary) != 55:
        beda.append("старых слайдов не ровно 55 без дублей: %d" % len(stary))
    return beda


def old_file(path):
    """Файл из точки отката. Старый дек не распаковываю в /tmp — читаю из git."""
    r = subprocess.run(["git", "--no-optional-locks", "show",
                        "%s:teorkat-vvedenie/src/%s" % (TOCHKA_OTKATA, path)],
                       cwd=REPO, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def perenesti_plotnost():
    """Ступень нового слайда = МАКСИМУМ по ступеням вошедших старых (заход §2¾).

    🔴 Ключи `plotnost.json` — по `sNN`, и при сквозной перенумерации они наводятся
    на ЧУЖИЕ слайды: `plotnost["s13"]=5` — это старая «Стрелка как отображение», а
    новый `s13` — «Зоопарк». Оставить файл как есть было бы хуже, чем удалить: числа
    выглядят перенесённой ночной работой, а показывают на другие слайды.
    """
    staraya = json.loads(old_file("tools/plotnost.json"))
    k = karta()
    novaya = {}
    for novy, starye in sorted(k.items()):
        st = max(staraya.get(s, 0) for s in starye)
        if st:
            novaya[novy] = st
    return staraya, novaya


def main():
    beda = sverka()
    k = karta()
    if "--plotnost" in sys.argv:
        staraya, novaya = perenesti_plotnost()
        (TOOLS / "plotnost.json").write_text(
            json.dumps(novaya, ensure_ascii=False, indent=0, sort_keys=True),
            encoding="utf-8")
        from collections import Counter
        print("ступени ПЕРЕНЕСЕНЫ по карте (максимум по вошедшим):")
        print("  старый дек 55: %s" % dict(sorted(
            Counter([staraya.get("s%02d" % i, 0) for i in range(1, 56)]).items())))
        print("  новый дек 32: %s" % dict(sorted(
            Counter([novaya.get("s%02d" % i, 0) for i in range(1, 33)]).items())))
        print("  записано: %s" % (TOOLS / "plotnost.json"))
        return 1 if beda else 0

    print("── КАРТА ПЕРЕХОДА 55 → 32 ──")
    print("%-5s %-6s %s" % ("нов", "класс", "старые"))
    for novy, starye in sorted(k.items()):
        print("%-5s %-6s %s" % (novy, klass(novy, k), " + ".join(starye)))
    from collections import Counter
    print()
    print("классы: %s" % dict(sorted(Counter(klass(n, k) for n in k).items())))
    print("размеры групп (старых слайдов в новом): %s"
          % dict(sorted(Counter(len(v) for v in k.values()).items())))
    print("сверка карты: %s" % ("✅ биекция на 56 разделов и 55 слайдов"
                                if not beda else "❌ " + " · ".join(beda)))
    return 1 if beda else 0


if __name__ == "__main__":
    sys.exit(main())
