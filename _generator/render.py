#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render.py — тонкий диспетчер: ОДНА дверь, а не вторая копия.

Тело движка переехало в плагин: `disciplina/_generator/dvizhki/render.py`
(заход `vynos-dvizhkov`, 2026-08-23). Старый путь остаётся рабочим —
вызывающие документы не меняются (по `_generator/render` зовут 28 файлов .md).

Путь до двери вычисляется ОТ ЭТОГО ФАЙЛА (`__file__`), а не хардкод-
литералом: репозитории `materials` и `disciplina` лежат рядом друг с другом
у ЭТОГО владельца, но это не гарантия для всех — вычисление по имени соседа
переживёт переезд там, где захардкоженная абсолютная строка умрёт молча.
Форма — образец `_generator/tools/priyomka.py`. Поведение движка не меняется:
`runpy.run_path(..., run_name=__name__)` исполняет ТОТ ЖЕ файл с тем же
`sys.argv` и тем же кодом возврата (`sys.exit(main())` пролетает насквозь).
"""

import runpy
import sys
from pathlib import Path

СОСЕД = Path(__file__).resolve().parents[2]
ДВЕРЬ = СОСЕД / "disciplina" / "_generator" / "dvizhki" / "render.py"

if not ДВЕРЬ.is_file():
    print(f"⛔ Тело движка не найдено по вычисленному пути: {ДВЕРЬ}", file=sys.stderr)
    print("   Ожидается репозиторий `disciplina` рядом с `materials` "
          f"(сосед {СОСЕД}). Если разложено иначе — "
          "поправь вычисление ДВЕРЬ в этом файле.", file=sys.stderr)
    if __name__ == "__main__":
        sys.exit(1)
    raise ModuleNotFoundError(f"дверь диспетчера render.py не найдена: {ДВЕРЬ}")

globals().update(runpy.run_path(str(ДВЕРЬ), run_name=__name__))
