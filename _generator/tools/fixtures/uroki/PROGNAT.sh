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
# ── Гейт «закрытие без метки» (заход zamykanie-reestrov, ## ПЛАН) ───────────
# Требуемая пара по критерию Б1: заявлено «закрыт Д99», метка не тронута →
# красный; метка переставлена (дата данных = сегодня) → зелёный. Долговое
# плечо — БЕЗ git (DOLG.md живёт в ДРУГОМ репозитории, `~/Documents/GitHub/
# disciplina`, не `materials` — см. ## ПЛАН этого захода), сверяется чтением
# файла с диска; путь подставляется через `CHECK_UROKI_DOLG` (тот же приём,
# что `PRIYOMKA_REPO`/`GIT_ZONA_REPO` у соседних инструментов).
Z=_generator/tools/fixtures/uroki/zakrytie
mkdir -p "$Z/arka"
cat > "$Z/DOLG.md" <<'MD'
| Д99 | тестовый долг | СТАТУС: ЖИВ · 2020-01-01 · grep -c foo bar.py → 3 |
MD
cat > "$Z/arka/kod_dolg.md" <<'MD'
## ОТЧЁТ — (заполняет исполнитель)
Починили баг, закрыт Д99.
**АРТЕФАКТ:** артефакта нет: инфраструктурный заход
**КОММИТ:** `deadbeef` — тест
MD
OUT_R=$(CHECK_UROKI_DOLG="$Z/DOLG.md" python3 _generator/tools/check_uroki.py "$Z/arka/kod_dolg.md" 2>&1)
RC_R=$?
if [ "$RC_R" = 1 ] && echo "$OUT_R" | grep -q "❌ ЗАКРЫТИЕ БЕЗ МЕТКИ"; then
  echo "  ✅ долг заявлен закрытым, метка НЕ тронута сегодня — покраснело поимённо"
else
  echo "❌ ЛОВУШКА: долг без свежей метки не покраснел (или не тем). rc=$RC_R"
  echo "$OUT_R"; fail=1
fi

TODAY=$(python3 -c "import datetime; print(datetime.date.today().isoformat())")
cat > "$Z/DOLG.md" <<MD
| Д99 | тестовый долг | СТАТУС: МЁРТВ · $TODAY · grep -c foo bar.py → 0 |
MD
OUT_G=$(CHECK_UROKI_DOLG="$Z/DOLG.md" python3 _generator/tools/check_uroki.py "$Z/arka/kod_dolg.md" 2>&1)
RC_G=$?
if [ "$RC_G" = 0 ]; then
  echo "  ✅ долг заявлен закрытым, метка тронута сегодня — зелёное"
else
  echo "❌ ЛОВУШКА: долг со свежей меткой всё равно покраснел. rc=$RC_G"
  echo "$OUT_G"; fail=1
fi

# Регрессия: обычный отчёт БЕЗ заявлений о закрытии — гейт молчит про этот
# новый гейт (обратная совместимость), даже когда DOLG.md вовсе недоступен.
cat > "$Z/arka/kod_obychnyj.md" <<'MD'
## ОТЧЁТ — (заполняет исполнитель)
Сделали X, ничего не закрывали.
**АРТЕФАКТ:** артефакта нет: инфраструктурный заход
**КОММИТ:** `deadbeef` — тест
MD
OUT_N=$(CHECK_UROKI_DOLG="/nonexistent/DOLG.md" python3 _generator/tools/check_uroki.py "$Z/arka/kod_obychnyj.md" 2>&1)
RC_N=$?
if [ "$RC_N" = 0 ]; then
  echo "  ✅ обычный отчёт без заявлений о закрытии — обратная совместимость цела"
else
  echo "❌ ЛОВУШКА: обычный отчёт без заявлений покраснел — регрессия обратной совместимости. rc=$RC_N"
  echo "$OUT_N"; fail=1
fi

# Плечи инцидент/урок сверяют ДОБАВЛЕННУЮ git-diff строку — нужен настоящий
# репозиторий (VERDIKTY.md/UROKI-FABRIKE.md живут внутри `materials`, в
# отличие от DOLG.md выше). Тот же приём, что ловушки 13–15 fixtures/priyomka.
TZ=$(mktemp -d)
trap 'rm -rf "$TZ"' EXIT
git init -q "$TZ"
git -C "$TZ" config user.email t@t.test
git -C "$TZ" config user.name t
mkdir -p "$TZ/_studio/zhurnal/_INFRA-git" "$TZ/_studio/zhurnal/test-arka"
: > "$TZ/_studio/zhurnal/_INFRA-git/VERDIKTY.md"
: > "$TZ/_studio/zhurnal/test-arka/UROKI-FABRIKE.md"
git -C "$TZ" add -A >/dev/null
git -C "$TZ" commit -qm base >/dev/null
cat > "$TZ/_studio/zhurnal/test-arka/kod_test.md" <<'MD'
## ОТЧЁТ — (заполняет исполнитель)
Разобрали инцидент, закрыт. Урок реализован.
**АРТЕФАКТ:** артефакта нет: инфраструктурный заход
**КОММИТ:** `deadbeef` — тест
MD
git -C "$TZ" add -A >/dev/null
TOOLS_ABS="$(pwd)/_generator/tools"
OUT_IR=$(python3 -c "
import sys; sys.path.insert(0, '$TOOLS_ABS')
import check_uroki
from pathlib import Path
p = Path('$TZ/_studio/zhurnal/test-arka/kod_test.md')
print(check_uroki.zakrytiya_bez_metki(p, p.read_text(), repo_root=Path('$TZ'), dolg_path=Path('/nonexistent')))
")
if echo "$OUT_IR" | grep -q "'инцидент'" && echo "$OUT_IR" | grep -q "'урок'"; then
  echo "  ✅ инцидент и урок заявлены, метки НЕ тронуты этим коммитом — оба поймал поимённо"
else
  echo "❌ ЛОВУШКА: инцидент/урок заявлены, метки не тронуты — не покраснело как надо. Вывод: $OUT_IR"
  fail=1
fi

echo "- C прочий чужой долг · вердикт: закрыт гейтом \`check_uroki.py\` · дата данных: $TODAY" >> "$TZ/_studio/zhurnal/_INFRA-git/VERDIKTY.md"
printf '### урок\nВЕРДИКТ: реализовано\n' >> "$TZ/_studio/zhurnal/test-arka/UROKI-FABRIKE.md"
git -C "$TZ" add -A >/dev/null
OUT_IG=$(python3 -c "
import sys; sys.path.insert(0, '$TOOLS_ABS')
import check_uroki
from pathlib import Path
p = Path('$TZ/_studio/zhurnal/test-arka/kod_test.md')
print(check_uroki.zakrytiya_bez_metki(p, p.read_text(), repo_root=Path('$TZ'), dolg_path=Path('/nonexistent')))
")
if [ "$OUT_IG" = "[]" ]; then
  echo "  ✅ инцидент/урок — метки добавлены этим же коммитом, зелёное"
else
  echo "❌ ЛОВУШКА: метки добавлены этим коммитом, но гейт всё равно покраснел. Вывод: $OUT_IG"
  fail=1
fi
rm -rf "$TZ"
trap - EXIT

[ $fail = 0 ] && echo "ФИКСТУРЫ ЗЕЛЁНЫЕ" || echo "ФИКСТУРЫ КРАСНЫЕ — гейт сломан правкой"
exit $fail
