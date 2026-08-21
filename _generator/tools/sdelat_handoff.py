#!/usr/bin/env python3
# TOOL-CONTRACT: called-by-hand — хэндофф собирает аналитик в конце сессии
# осознанно, не автоматический гейт (заход `instrument-podklyuchen`, Ш1).
"""sdelat_handoff.py — тонкий диспетчер: ОДНА дверь, а не вторая копия.

ОТКЛЮЧЕНО 2026-08-21, заход `otkljuchit-dubli`. Сверка копий (`disciplina`
`_generator/tools/sverka_kopij.py`) назвала этот файл разошедшимся с живым
оригиналом в `disciplina/_generator/tools/sdelat_handoff.py` молча: в
`disciplina` он переписан (добавлены `proverit_pokrytie`, `sobrat_vhod`,
`spisok_skillov`, `status_dnevnika_tekst`), а в `materials` осталась прежняя
редакция. Проверено перед отключением: строк, уникальных для редакции
`materials` (по множеству `def`/`class`), — 0; всё, что здесь было, есть и
там, только в переписанном виде. Ведущая сторона — `disciplina`. Настоящий
инструмент теперь живёт по адресу, вычисленному ниже (сосед `materials` по
имени `disciplina`), путь остаётся рабочим — вызывающие 485 документов не
меняются.

Путь до полной двери вычисляется ОТ ЭТОГО ФАЙЛА (`__file__`), а не хардкод-
литералом: репозитории `materials` и `disciplina` лежат рядом друг с другом
у ЭТОГО владельца, но это не гарантия для всех — вычисление по имени соседа
переживёт переезд там, где захардкоженная абсолютная строка умрёт молча.

🔴 ЭТОТ ФАЙЛ — И CLI, И БИБЛИОТЕКА, ОДНИМ ПРИЁМОМ СО ВСЕМИ ЧЕТЫРЬМЯ
СОСЕДЯМИ ПО ЭТОМУ ЗАХОДУ. Прямого импортёра `sdelat_handoff` в `materials`
на момент отключения не найдено — но `priyomka.py`, `bootstrap_zahod.py`,
`check_zahod.py`, `dnevnik.py` из той же пятёрки оказались одновременно и
CLI, и библиотекой (прод-хук `.githooks/pre-commit` через
`check_faza_priyomki.py` делает `import priyomka`; фикстуры делают `import
bootstrap_zahod`/`check_zahod`/`dnevnik`), и наивный диспетчер только под
`if __name__ == "__main__":` (образец `tools/git_zona.py`) на них ломался
`AttributeError`-ом при обычном импорте. Тот же приём здесь — не потому что
поломка уже видна, а чтобы пять диспетчеров этой задачи не расходились по
контракту втихую: пятый, оставшийся на старом образце, стал бы следующей
находкой следующего захода.

Приём: `runpy.run_path(ДВЕРЬ, run_name=__name__)` БЕЗ `if __name__ ==
"__main__":`-гварда вокруг вызова. `__name__` этого файла Python выставляет
сам — `"__main__"`, когда файл ЗАПУЩЕН (`python3 sdelat_handoff.py …`), и
`"sdelat_handoff"`, когда он ИМПОРТИРОВАН (`import sdelat_handoff`).
Передавая его дальше дверью, получаем: при запуске дверь получает `__name__
== "__main__"` и её собственный `if __name__ == "__main__": sys.exit(main())`
срабатывает как обычно — то же поведение, что дал бы `python3 <дверь>`
напрямую, с тем же кодом возврата. При импорте дверь получает `__name__ ==
"sdelat_handoff"`, её `__main__`-блок НЕ срабатывает (не запускает `main()`,
не делает `sys.exit`), а все её имена достаются в `_ns` и переносятся в этот
модуль.

Дверь не найдена — ВНЯТНЫЙ отказ, а не `ModuleNotFoundError` без объяснений:
при запуске — печать и `sys.exit(1)`; при импорте — то же сообщение в stderr
и `ModuleNotFoundError` с вычисленным путём, чтобы читающий трейсбек видел
ПРИЧИНУ, а не голое имя модуля.
"""

import runpy
import sys
from pathlib import Path

КОРЕНЬ_MATERIALS = Path(__file__).resolve().parents[2]
ДВЕРЬ = КОРЕНЬ_MATERIALS.parent / "disciplina" / "_generator" / "tools" / "sdelat_handoff.py"

if not ДВЕРЬ.is_file():
    print(f"⛔ Полная дверь не найдена по вычисленному пути: {ДВЕРЬ}", file=sys.stderr)
    print("   Ожидается репозиторий `disciplina` рядом с `materials` "
          f"(сосед {КОРЕНЬ_MATERIALS.parent}). Если разложено иначе — "
          "поправь вычисление ДВЕРЬ в этом файле.", file=sys.stderr)
    if __name__ == "__main__":
        sys.exit(1)
    raise ModuleNotFoundError(f"дверь диспетчера sdelat_handoff.py не найдена: {ДВЕРЬ}")

globals().update(runpy.run_path(str(ДВЕРЬ), run_name=__name__))
