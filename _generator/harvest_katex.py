#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""harvest_katex.py — тонкий диспетчер: ОДНА дверь, а не вторая копия.

Тело переехало в плагин: `disciplina/_generator/harvest_katex.py`
(заход `ostatok-generatora`, 2026-08-25). Старый путь остаётся рабочим —
вызывающие документы не меняются (ручные вызовы по `_generator/harvest_katex.py`
задокументированы в SLIDE-FORMAT.md и konvejer/10-sborka-qa; программных
вызовов пути нет — проверено грепом обоих репозиториев).

Путь до двери вычисляется ОТ ЭТОГО ФАЙЛА (`__file__`), а не хардкод-
литералом: репозитории `materials` и `disciplina` лежат рядом друг с другом
у ЭТОГО владельца, но это не гарантия для всех — вычисление по имени соседа
переживёт переезд там, где захардкоженная абсолютная строка умрёт молча.
Форма — образец `render.py`. Поведение сборщика не меняется: `runpy.run_path`
исполняет ТОТ ЖЕ файл с тем же `sys.argv`; код возврата пролетает насквозь
(кривой вход — rc=2, контракт §5).
"""

import runpy
import sys
from pathlib import Path

СОСЕД = Path(__file__).resolve().parents[2]
ДВЕРЬ = СОСЕД / "disciplina" / "_generator" / "harvest_katex.py"

if not ДВЕРЬ.is_file():
    print(f"⛔ Тело сборщика не найдено по вычисленному пути: {ДВЕРЬ}", file=sys.stderr)
    print("   Ожидается репозиторий `disciplina` рядом с `materials` "
          f"(сосед {СОСЕД}). Если разложено иначе — "
          "поправь вычисление ДВЕРЬ в этом файле.", file=sys.stderr)
    if __name__ == "__main__":
        sys.exit(1)
    raise ModuleNotFoundError(f"дверь диспетчера harvest_katex.py не найдена: {ДВЕРЬ}")

globals().update(runpy.run_path(str(ДВЕРЬ), run_name=__name__))
