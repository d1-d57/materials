#!/usr/bin/env python3
"""Список, поиск и гейт паспортов по обзорам. Читает шапки `obzory/*/src/*.md`.

    python3 obzory/spisok.py              # все обзоры
    python3 obzory/spisok.py ординал      # только те, где слово встречается в шапке
    python3 obzory/spisok.py --polnyj     # плюс путь к источнику и к виду
    python3 obzory/spisok.py --proverit   # ГЕЙТ: обзор без паспорта → красный, exit 1

Список обзоров — производный факт (KONSTITUCIYA §10): руками он нигде не лежит,
эта команда его считает. Гейт `--proverit` — механизм к правилу «у обзора есть
паспорт» (KONSTITUCIYA §11): без него правило нарушается молча, потому что обзор
без полей просто не находится поиском и никто этого не замечает.
Чистый stdlib, без сети.
"""
import re
import sys
from pathlib import Path

FIELDS = ("tab", "tema", "oblast", "klyuchevye", "data", "status", "adresat")
OBYAZATELNYE = ("tab", "tema", "oblast", "klyuchevye", "data")
ROOT = Path(__file__).resolve().parent


def shapka(md):
    """Фронтматтер файла → словарь. Пустой, если шапки нет."""
    text = md.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        lm = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if lm:
            out[lm.group(1)] = lm.group(2).strip().strip('"')
    return out


def sluzhebnaya(name):
    """Папка на `_` — служебная (фикстуры гейта и т.п.), обзором не считается.
    Без этого ломающая фикстура неотличима от настоящего долга и красит гейт всегда."""
    return name.startswith("_")


def sobrat():
    """Все обзоры: (папка, шапка, путь-источника). Отсортированы по дате, свежие сверху."""
    found = []
    for src in sorted(ROOT.glob("*/src/*.md")):
        if sluzhebnaya(src.parent.parent.name):
            continue
        meta = shapka(src)
        if meta:
            found.append((src.parent.parent.name, meta, src))
    found.sort(key=lambda r: (r[1].get("data", ""), r[0]), reverse=True)
    return found


def proverit():
    """Гейт: у каждого обзора заполнен паспорт. Возвращает код выхода."""
    print("── ГЕЙТ ПАСПОРТОВ (obzory) ──")
    bad = []
    papki = {p.parent.parent for p in ROOT.glob("*/src/*.md")}
    for d in sorted(p for p in ROOT.iterdir() if p.is_dir()):
        if sluzhebnaya(d.name):
            continue
        if d not in papki:
            bad.append((d.name, "нет ни одного `src/*.md` с шапкой"))
    for papka, meta, src in sobrat():
        net = [f for f in OBYAZATELNYE if not meta.get(f)]
        if net:
            bad.append((papka, "нет полей: " + ", ".join(net)))
    if bad:
        print("  ✗ КРАСНЫЙ — %d" % len(bad))
        for name, why in bad:
            print("     %s: %s" % (name, why))
        return 1
    print("  ✓ ЗЕЛЁНЫЙ: у всех обзоров паспорт заполнен")
    return 0


def main():
    args = [a for a in sys.argv[1:]]
    if "--proverit" in args:
        sys.exit(proverit())
    polnyj = "--polnyj" in args
    if polnyj:
        args.remove("--polnyj")
    zapros = " ".join(args).strip().lower()

    vse = sobrat()
    if zapros:
        vse = [r for r in vse
               if zapros in " ".join(r[1].get(f, "") for f in FIELDS).lower()
               or zapros in r[0].lower()]

    if not vse:
        print("— ничего не нашлось" if zapros else "— обзоров пока нет")
        return

    for papka, meta, src in vse:
        print()
        print("  %s  ·  %s  ·  %s" % (meta.get("data", "без даты"),
                                      papka,
                                      meta.get("status", "без статуса")))
        print("    %s" % meta.get("tab", "—"))
        if meta.get("tema"):
            print("    тема:      %s" % meta["tema"])
        if meta.get("oblast"):
            print("    область:   %s" % meta["oblast"])
        if meta.get("klyuchevye"):
            print("    ключевые:  %s" % meta["klyuchevye"])
        if polnyj:
            rel = src.relative_to(ROOT.parent)
            print("    источник:  %s" % rel)
            print("    вид:       %s" % rel.parent.joinpath("view.html"))

    print()
    print("  всего: %d" % len(vse))


if __name__ == "__main__":
    main()
