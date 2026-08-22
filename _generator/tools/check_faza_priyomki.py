#!/usr/bin/env python3
"""check_faza_priyomki.py — тонкий диспетчер: ОДНА дверь, а не вторая копия.

ОТКЛЮЧЕНО 2026-08-22, заход `vynos-instrumentov`: тело переехало туда целиком, байт в байт, вместе со спутник-фикстурой
`fixtures/faza-priyomki/PROGNAT.sh`; инструмент судит только переданные ему пути.
Живой экземпляр — `disciplina/_generator/tools/check_faza_priyomki.py`. Путь остаётся
рабочим: вызывающие документы не меняются.

Форма — образец `priyomka.py` (заход `otkljuchit-dubli`): файл остаётся и CLI,
и библиотекой — `runpy.run_path(ДВЕРЬ, run_name=__name__)` без
`__main__`-гварда. При запуске дверь получает `__name__ == "__main__"` и её
`sys.exit(main())` срабатывает как обычно, с тем же кодом возврата; при
импорте все имена двери переезжают в этот модуль (`import check_faza_priyomki`;
`check_faza_priyomki.<имя>` продолжает работать). Дверь не найдена — внятный отказ,
а не голый ModuleNotFoundError.

🔴 Перед exec двери ставится умолчание `GIT_ZONA_REPO` = корень ЭТОГО дерева.
Судимый корень инструменты берут как «env или parents[2] от своего файла»
(`korni.py:43`), и без этой строки тело из соседнего репозитория молча судило
бы свой дом вместо дерева вызова. `setdefault`, а не присвоение: явный env
зовущего сильнее умолчания диспетчера.
"""

import os
import runpy
import sys
from pathlib import Path

КОРЕНЬ_MATERIALS = Path(__file__).resolve().parents[2]
ДВЕРЬ = КОРЕНЬ_MATERIALS.parent / "disciplina" / "_generator" / "tools" / "check_faza_priyomki.py"

os.environ.setdefault("GIT_ZONA_REPO", str(КОРЕНЬ_MATERIALS))

if not ДВЕРЬ.is_file():
    print(f"⛔ Полная дверь не найдена по вычисленному пути: {ДВЕРЬ}", file=sys.stderr)
    print("   Ожидается репозиторий `disciplina` рядом с `materials` "
          f"(сосед {КОРЕНЬ_MATERIALS.parent}). Если разложено иначе — "
          "поправь вычисление ДВЕРЬ в этом файле.", file=sys.stderr)
    if __name__ == "__main__":
        sys.exit(1)
    raise ModuleNotFoundError(f"дверь диспетчера check_faza_priyomki.py не найдена: {ДВЕРЬ}")

globals().update(runpy.run_path(str(ДВЕРЬ), run_name=__name__))
