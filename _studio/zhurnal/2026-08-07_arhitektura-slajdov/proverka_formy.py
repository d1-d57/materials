#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Чекер критерия готовности захода `fazy-3-7-novoe-derevo` — печатает ЧИСЛА, а не мнение.

    python3 _studio/zhurnal/2026-08-07_arhitektura-slajdov/proverka_formy.py

Проверяет четыре из шести клауз критерия (те, что счётные):
  К1  адресов старого дерева в SKILL.md — 0 (грепом, как записано в критерии, И сильной
      версией, которая видит адреса без префикса `src/`);
  К2  таблица 7×6: у каждой из семи фаз шесть блоков формы, ни одной пустой клетки;
  К3  список типов блока — в одной редакции из семи имён, во всех файлах, которые его
      перечисляют; эталон берётся ИЗ КОДА (`_generator/sborka/bloki.py`), не из текста;
  К6  `references/status-bloka.md` несёт все семь типов.

🔴 ЧЕГО ЧЕКЕР НЕ ВИДИТ (объявляю слепые зоны сам, иначе зелёный врёт):
  · К4 (сквозной проход по стыкам фаз) — суждение о смысле артефакта, не счётное;
  · К5 (живой прогон верификаторов) — прогон субагентов, не грепа;
  · «клетка не пуста» проверяется ОБЪЁМОМ (≥3 непустых строк), а не тем, что в ней написано
    по делу: раздел из трёх строк воды пройдёт;
  · К3 считает файл «перечисляющим список», если в нём ≥4 из семи имён. Файл, называющий
    ровно три типа неверно, чекер не заметит;
  · у ПОСЛЕДНЕЙ фазы последняя клетка вбирает весь хвост документа (после неё нет следующего
    `## Фаза`), поэтому «МЕТРИКА фазы 7 — 75 строк» это артефакт счёта, а не объём клетки:
    реально там 13 строк, дальше идут «Сводная карта гейтов» и «Якоря». На вердикт «не пусто»
    это не влияет, на чтение числа — влияет.
"""
import re
import subprocess
import sys
from pathlib import Path

SKILL = Path.home() / "Documents/GitHub/disciplina/skills/slajdy"
BLOKI = Path.home() / "Documents/GitHub/materials/_generator/sborka/bloki.py"

BLOKI_FORMY = ("ВХОД", "РЕШЕНИЯ ФАЗЫ", "ПРОЦЕДУРА", "ВЫХОД", "ГЕЙТ ВЫХОДА", "МЕТРИКА")
FAZA_RE = re.compile(r"^## Фаза (\d) · (.+?)\s*$", re.M)
PODRAZDEL_RE = re.compile(r"^### ([А-ЯЁ ]+?)(?: —.*)?\s*$", re.M)
STAROE_DEREVO = ("src/content", "src/slides", "src/illustrations")


def tipy_iz_koda():
    """Эталон списка типов — из кода, а не из текста дисциплины (Р-В)."""
    src = BLOKI.read_text(encoding="utf-8")
    m = re.search(r"TIPY_BLOKOV\s*=\s*\((.*?)\)", src, re.S)
    if not m:
        sys.exit("ABORT: не нашёл TIPY_BLOKOV в %s" % BLOKI)
    return tuple(re.findall(r'"([a-z_]+)"', m.group(1)))


def k1(text):
    popal = [(i + 1, ln) for i, ln in enumerate(text.splitlines())
             if any(s in ln for s in STAROE_DEREVO)]
    silnyj = [(i + 1, ln) for i, ln in enumerate(text.splitlines())
              if re.search(r"<лекция>/src/|(?<![\w/])(content|slides|illustrations)/<", ln)]
    print("К1  адреса старого дерева в SKILL.md")
    print("    как записано в критерии (src/content|src/slides|src/illustrations): %d" % len(popal))
    for n, ln in popal:
        print("      %d: %s" % (n, ln.strip()[:100]))
    print("    ⚠ сильная версия (<лекция>/src/ и голые content/<…>, slides/<…>, illustrations/<…>)")
    print("      остаток: %d строк — КАЖДАЯ обязана быть объяснена в отчёте захода как законная"
          % len(silnyj))
    print("      (речь о СТАРОМ дереве старых деков или историческая пометка), иначе это дефект:")
    for n, ln in silnyj:
        print("      %d: %s" % (n, ln.strip()[:100]))
    # гейтит только критерий КАК ЗАПИСАН: сильная версия — число для отчёта, не приговор,
    # потому что законный остаток («старое дерево принадлежит старым декам») неотличим
    # грепом от дефекта, а классифицировать его хардкодом значит зашить сегодняшний список
    # строк в чекер и получить зелёный на завтрашнем.
    return not popal


def k2(text):
    fazy = list(FAZA_RE.finditer(text))
    print("\nК2  таблица 7×6 — шесть блоков формы у каждой фазы")
    print("    найдено фаз: %d" % len(fazy))
    ok = len(fazy) == 7
    print("    %-3s %-22s %s" % ("№", "фаза", "  ".join(BLOKI_FORMY)))
    for i, m in enumerate(fazy):
        start = m.end()
        end = fazy[i + 1].start() if i + 1 < len(fazy) else len(text)
        telo = text[start:end]
        kletki = []
        for j, p in enumerate(PODRAZDEL_RE.finditer(telo)):
            s = p.end()
            e = list(PODRAZDEL_RE.finditer(telo))[j + 1].start() \
                if j + 1 < len(list(PODRAZDEL_RE.finditer(telo))) else len(telo)
            kletki.append((p.group(1).strip(), len([l for l in telo[s:e].splitlines() if l.strip()])))
        imena = {k: n for k, n in kletki}
        stroka = []
        for b in BLOKI_FORMY:
            n = imena.get(b)
            if n is None:
                stroka.append("НЕТ")
                ok = False
            elif n < 3:
                stroka.append("ПУСТО(%d)" % n)
                ok = False
            else:
                stroka.append("%d стр" % n)
        print("    %-3s %-22s %s" % (m.group(1), m.group(2)[:22], "  ".join("%-9s" % s for s in stroka)))
    return ok


def k3(tipy):
    print("\nК3  список типов блока — одна редакция из семи имён (эталон: bloki.py)")
    print("    эталон из кода: %s" % " · ".join(tipy))
    ok = True
    for p in sorted(SKILL.rglob("*.md")):
        t = p.read_text(encoding="utf-8")
        est = [x for x in tipy if re.search(r"\b%s\b" % x, t)]
        if len(est) < 4:
            continue
        net = [x for x in tipy if x not in est]
        status = "✅" if not net else "❌ не хватает: %s" % ", ".join(net)
        if net:
            ok = False
        print("    %-46s %d/7  %s" % (str(p.relative_to(SKILL)), len(est), status))
    # чужие редакции
    for chuzhoj in ("vopros_zalu", "svyazka"):
        hits = subprocess.run(["grep", "-rn", chuzhoj, str(SKILL), "--include=*.md"],
                              capture_output=True, text=True).stdout.strip().splitlines()
        print("    упоминаний `%s`: %d (законны только как «отменён/было»)" % (chuzhoj, len(hits)))
        for h in hits:
            print("      %s" % h.split(str(SKILL) + "/")[-1][:130])
    return ok


def k6(tipy):
    p = SKILL / "references/status-bloka.md"
    t = p.read_text(encoding="utf-8")
    net = [x for x in tipy if not re.search(r"\b%s\b" % x, t)]
    print("\nК6  status-bloka.md приведён к семи типам: %s"
          % ("✅ все семь на месте" if not net else "❌ нет: %s" % ", ".join(net)))
    return not net


def main():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    tipy = tipy_iz_koda()
    r = [k1(text), k2(text), k3(tipy), k6(tipy)]
    print("\n" + "=" * 72)
    print("ИТОГ счётных клауз: зелёных %d из %d" % (sum(r), len(r)))
    print("НЕ ПОКРЫТО ЭТИМ ЧЕКЕРОМ: К4 (сквозной проход) и К5 (живой прогон верификаторов) —")
    print("оба суждение/прогон, не греп; их вердикт лежит в отчёте захода, а не здесь.")
    return 0 if all(r) else 1


if __name__ == "__main__":
    sys.exit(main())
