#!/bin/sh
# TOOL-CONTRACT-COVERS: check_uroki.py
# Фикстуры гейта УРОКОВ. Гоняй ПОСЛЕ любой правки check_uroki.py.
# Строка COVERS выше — не украшение: по ней хук решает, поднимать ли фикстуру.
# Пока охват жил только в этом комментарии, триггер расходился с покрытием
# (см. check_tool_contract.py и GIT-disciplina §5).
# Зачем: гейт, который может ПРОЙТИ, обязан иметь фикстуру, на которой он ПАДАЕТ —
# иначе «зелёный» ничего не доказывает. Цена этого урока в арке mat-kostyak:
# PRIEMKA.sh печатал ✅ на грепе, падавшем с Invalid collation character.
# ⚠ Путь фикстуры обязан лежать внутри .../zhurnal/<арка>/kod_*.md — скрипт
#   фильтрует цели по этой структуре и файл вне её молча игнорирует (печатая 0).
cd "$(dirname "$0")/../../../.." || exit 1
F=_generator/tools/fixtures/uroki/zhurnal/test-arka
fail=0
for c in "bez-ceny 1" "zhirnaya 0" "golaya 0" "pustaya 1" "obratnaya 0" "cenalog 1" "backtick 1"; do
  set -- $c
  python3 _generator/tools/check_uroki.py "$F/kod_$1.md" >/dev/null 2>&1
  got=$?
  if [ "$got" = "$2" ]; then echo "  ✅ $1: exit $got"; else echo "  ❌ $1: exit $got, ожидался $2"; fail=1; fi
done
[ $fail = 0 ] && echo "ФИКСТУРЫ ЗЕЛЁНЫЕ" || echo "ФИКСТУРЫ КРАСНЫЕ — гейт сломан правкой"
exit $fail
