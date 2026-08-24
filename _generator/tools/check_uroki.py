#!/usr/bin/env python3
"""check_uroki.py — тонкий диспетчер: ОДНА дверь, а не вторая копия.

ОТКЛЮЧЕНО 2026-08-24, заход `odin-istochnik-kopij`: копия разошлась с живым
экземпляром МОЛЧА (сторож `sverka_kopij.py` в `disciplina`, девять пар).
Проверено перед отключением диффом по существу: уникальной работы в редакции
`materials` не было — вся она уже лежит в живом экземпляре. Ведущая сторона —
`disciplina`. Живой экземпляр — `disciplina/_generator/tools/check_uroki.py`.
Путь остаётся рабочим: вызывающие документы не меняются.

Форма — образцы `priyomka.py` и `dolg_repozitoriev.py` (заходы
`otkljuchit-dubli`, `vynos-instrumentov`): файл остаётся и CLI, и библиотекой —
`runpy.run_path(ДВЕРЬ, run_name=__name__)` без `__main__`-гварда. При запуске
дверь получает `__name__ == "__main__"` и её `sys.exit(main())` срабатывает
как обычно, с тем же кодом возврата; при импорте все имена двери переезжают
в этот модуль (`import check_uroki`; `check_uroki.<имя>` продолжает работать). Дверь не
найдена — внятный отказ, а не голый ModuleNotFoundError.

🔴 Перед exec двери ставится умолчание `GIT_ZONA_REPO` = корень ЭТОГО дерева:
тело судит дерево вызова, а не свой дом. `setdefault`, а не присвоение —
явный env зовущего (например, фикстурный одноразовый репозиторий) сильнее
умолчания диспетчера.
"""

# TOOL-CONTRACT: called-by-hand — живая точка вызова названа: хук `.githooks/pre-commit` этого репозитория зовёт `check_uroki.py` на каждом коммите;
# плюс руки владельца и вызовы из соседних инструментов.

import os
import runpy
import sys
from pathlib import Path

КОРЕНЬ_MATERIALS = Path(__file__).resolve().parents[2]
ДВЕРЬ = КОРЕНЬ_MATERIALS.parent / "disciplina" / "_generator" / "tools" / "check_uroki.py"

os.environ.setdefault("GIT_ZONA_REPO", str(КОРЕНЬ_MATERIALS))

if not ДВЕРЬ.is_file():
    print(f"⛔ Полная дверь не найдена по вычисленному пути: {ДВЕРЬ}", file=sys.stderr)
    print("   Ожидается репозиторий `disciplina` рядом с `materials` "
          f"(сосед {КОРЕНЬ_MATERIALS.parent}). Если разложено иначе — "
          "поправь вычисление ДВЕРЬ в этом файле.", file=sys.stderr)
    if __name__ == "__main__":
        sys.exit(1)
    raise ModuleNotFoundError(f"дверь диспетчера check_uroki.py не найдена: {ДВЕРЬ}")

globals().update(runpy.run_path(str(ДВЕРЬ), run_name=__name__))
