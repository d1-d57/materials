#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""СЧЁТЧИК БЛОКОВ И БЕСХОЗНЫХ АБЗАЦЕВ — печать, а НЕ гейт (заход `yadro-blokov`, 2026-08-13).

    python3 _generator/tools/schet_blokov.py <папка-лента> [<папка-лента> …]
    python3 _generator/tools/schet_blokov.py obzory/*/src

Вход — папка-источник документа (`obzory/<обзор>/src`), та же, что у `dvizhki doc`.

🔴 ПОЧЕМУ НЕ ГЕЙТ, И ЭТО РЕШЕНИЕ, А НЕ НЕДОДЕЛКА. Требование «каждый абзац тела
принадлежит блоку» (Я1 §6) на этом заходе В ДВИЖОК НЕ ВНЕДРЯЕТСЯ: живые тексты
написаны до правила, и красный гейт на них закрыл бы сборку всему репозиторию в
день заведения. Внедрение — после контракта Ф4 арки `2026-08-13_skill-mat-teksta`.
Поэтому находки НИКОГДА не меняют код возврата: сколько бы бесхозных абзацев ни
нашлось, выход 0. Ненулевой код тут значит ровно одно — инструмент НЕ ОТРАБОТАЛ
(кривой вход → 2), и спутать эти два случая нельзя по устройству.

ЧТО СЧИТАЕТСЯ. Текст делится на сегменты ровно так же, как их делит движок, —
пустой строкой (`render_stream`: `re.split(r"\\n\\s*\\n", …)`), и разбирается
ядром `sborka/bloki.py`, а не собственной копией разметки:
  · БЛОК — сегмент с зачином врезки (`bloki.BOLD_STMT_RE`) или зачином вывода
    (`bloki.PROOF_HEAD_RE`); род блока = жанр врезки либо слово зачина;
  · АБЗАЦ ВНЕ БЛОКА — сегмент связной прозы, не попавший ни в один блок;
  · ПРОЧЕЕ — служебные сегменты, которые прозой не являются и в бесхозные не
    записываются: заголовки, списки, таблицы, поля/цитаты, строки-формулы,
    плейсхолдеры иллюстраций, сырой HTML, курсивные пометки (`*Статус…*`).
«Прочее» печатается ПОИМЁННО и не сворачивается в одно число нарочно: молчащая
корзина «остальное» — это то место, где счётчик начинает врать незаметно.
"""
# TOOL-CONTRACT: called-by-hand
# Зовётся руками: это инвентарь фазы Ф2 арки `2026-08-13_skill-mat-teksta`, а не
# шаг сборки. Гейтом он станет только после контракта Ф4 — тогда же и получит
# точку вызова в хуке.
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

GENERATOR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GENERATOR))
sys.path.insert(0, str(GENERATOR / "sborka"))
import bloki                                          # noqa: E402  (ядро блоков)
from build_doc import read_text, split_frontmatter    # noqa: E402  (тот же отбор файлов, что у движка)

# та же граница сегмента, что у движка (`build_doc.render_stream`): пустая строка
SEGMENT_SPLIT = re.compile(r"\n\s*\n")

PROCHEE = ("заголовки", "списки", "таблицы", "поля/цитаты", "формулы",
           "иллюстрации", "сырой HTML", "курсивные пометки")


def klass_segmenta(seg):
    """Сегмент → (вид, род|None). Виды: 'blok' · 'abzac' · один из PROCHEE · 'pusto'.

    Порядок веток повторяет порядок веток `render_stream` в `build_doc.py`:
    служебные формы разбираются РАНЬШЕ прозы, иначе таблица или список уедут в
    бесхозные абзацы и число раздуется на ровном месте."""
    s = seg.strip()
    if not s:
        return "pusto", None
    if s.startswith("#"):
        return "заголовки", None
    if s.startswith(">"):
        return "поля/цитаты", None
    if s.lstrip().startswith("- "):
        return "списки", None
    if s.startswith("|"):
        return "таблицы", None
    if s.startswith("🖼"):
        return "иллюстрации", None
    if s.startswith("<"):
        return "сырой HTML", None
    if s.startswith("$$") and s.endswith("$$") and len(s) > 4 and "\n" not in s:
        return "формулы", None
    u = bloki.razobrat_zachin(s)
    if u:
        return "blok", u.zhanr
    v = bloki.razobrat_zachin_vyvoda(s)
    if v:
        return "blok", v.zachin
    if s.startswith("*"):
        return "курсивные пометки", None
    return "abzac", None


def schitat_papku(papka):
    """Папка-источник → сводка. Файлы берутся тем же `glob('*.md')`, что и у
    движка (`build_doc.load_streams`), и фронтматтер срезается его же
    `split_frontmatter` — чтобы счётчик не считал по своей выборке."""
    itog = {"fajlov": 0, "blokov": 0, "abzacev": 0,
            "rody": Counter(), "prochee": Counter()}
    for p in sorted(Path(papka).glob("*.md")):
        itog["fajlov"] += 1
        _meta, body = split_frontmatter(read_text(p))
        for seg in SEGMENT_SPLIT.split(body.strip("\n")):
            vid, rod = klass_segmenta(seg)
            if vid == "pusto":
                continue
            if vid == "blok":
                itog["blokov"] += 1
                itog["rody"][rod] += 1
            elif vid == "abzac":
                itog["abzacev"] += 1
            else:
                itog["prochee"][vid] += 1
    return itog


def pechat(papka, s):
    print("%s" % papka)
    print("  файлов .md: %d" % s["fajlov"])
    print("  блоков: %d · абзацев вне блоков: %d" % (s["blokov"], s["abzacev"]))
    rody = " · ".join("%s %d" % (r, n) for r, n in s["rody"].most_common()) or "(нет)"
    print("  по родам: %s" % rody)
    proch = " · ".join("%s %d" % (k, s["prochee"][k]) for k in PROCHEE if s["prochee"][k])
    print("  прочее (не проза и не блок): %s" % (proch or "(нет)"))


def main():
    ap = argparse.ArgumentParser(
        description="Считает блоки и абзацы вне блоков в папках-лентах. Печать, не гейт: "
                    "находки НИКОГДА не меняют код возврата (0), ненулевой код = инструмент не отработал.")
    ap.add_argument("papki", nargs="+", help="папка-источник документа, например obzory/<обзор>/src")
    args = ap.parse_args()

    # Кривой вход обязан падать ГРОМКО и НАЗЫВАТЬ себя (цена 23.07: `bootstrap_arka.py`
    # проглотил `--help` как имя арки и завёл папку-сироту). Это единственный способ
    # получить отсюда ненулевой код — с содержательными находками он не смешивается.
    for p in args.papki:
        if not Path(p).is_dir():
            print("schet_blokov: «%s» — не папка (нужна папка-источник, например obzory/<обзор>/src)" % p,
                  file=sys.stderr)
            return 2

    vsego = {"papok": 0, "blokov": 0, "abzacev": 0, "rody": Counter(), "prochee": Counter()}
    for p in args.papki:
        s = schitat_papku(p)
        pechat(p, s)
        vsego["papok"] += 1
        vsego["blokov"] += s["blokov"]
        vsego["abzacev"] += s["abzacev"]
        vsego["rody"].update(s["rody"])
        vsego["prochee"].update(s["prochee"])

    if vsego["papok"] > 1:
        print("\nИТОГО по %d папкам: блоков %d · абзацев вне блоков %d"
              % (vsego["papok"], vsego["blokov"], vsego["abzacev"]))
        print("  по родам: %s" % (" · ".join("%s %d" % (r, n) for r, n in vsego["rody"].most_common()) or "(нет)"))
        print("  прочее: %s" % (" · ".join("%s %d" % (k, vsego["prochee"][k]) for k in PROCHEE if vsego["prochee"][k]) or "(нет)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
