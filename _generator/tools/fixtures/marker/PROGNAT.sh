#!/bin/sh
# TOOL-CONTRACT-COVERS: check_marker.py
# Фикстуры гейта маркера. Гоняй ПОСЛЕ любой правки check_marker.py.
# Строка COVERS выше — не украшение: по ней хук решает, поднимать ли фикстуру
# (см. check_tool_contract.py и GIT-disciplina §5).
cd "$(dirname "$0")/../../../.." || exit 1
D=_generator/tools/fixtures/marker
CHK="python3 _generator/tools/check_marker.py"
fail=0

# ── Табличные ловушки: явный путь → ожидаемый rc ──────────────────────────
for c in \
    "zhurnal/test-arka/kod_bootstrap-ok.md 0" \
    "zhurnal/test-arka/kod_ruchnoj.md 1" \
    "HANDOFF-test-ok.md 0" \
    "HANDOFF-test-ruchnoj.md 1" \
    "ZAHOD-test-ruchnoj.md 1" \
    "PEREDACHA-test-ruchnoj.md 1" \
    "ne-zahod.md 0" \
    "HANDOFF.md 1" \
    "peredacha-test.md 1" \
    "zahod_test.md 1" \
    "Kod_Test.md 1" \
; do
  set -- $c
  $CHK "$D/$1" >/dev/null 2>&1
  got=$?
  if [ "$got" = "$2" ]; then echo "  ✅ $1: exit $got"; else echo "  ❌ $1: exit $got, ожидался $2"; fail=1; fi
done

# ── «Окно шесть строк, не пять» — HANDOFF-test-ok.md обязан ПРОЙТИ ────────
# Это тот самый случай, из-за которого задание правили ДО кода (см. ## ПЛАН
# kod_zapret.md): маркер sdelat_handoff.py стоит строкой 6. Табличный тест
# выше уже это проверяет (rc=0), эта проверка — что причина именно та, а не
# случайное совпадение: маркер физически на 6-й строке фикстуры.
LINE=$(grep -n '^<!-- собран sdelat_handoff.py -->$' "$D/HANDOFF-test-ok.md" | cut -d: -f1)
if [ "$LINE" = "6" ]; then
  echo "  ✅ HANDOFF-test-ok.md: маркер физически на строке 6, окно его ловит"
else
  echo "❌ ЛОВУШКА: маркер HANDOFF-test-ok.md на строке '$LINE', ожидалась 6 — фикстура сама сломана"
  fail=1
fi

# ── Чисто → вывод ПУСТОЙ (обе зелёные фикстуры разом, явные пути) ─────────
OUT_CLEAN=$($CHK "$D/zhurnal/test-arka/kod_bootstrap-ok.md" "$D/HANDOFF-test-ok.md" 2>&1)
RC_CLEAN=$?
if [ "$RC_CLEAN" = 0 ] && [ -z "$OUT_CLEAN" ]; then
  echo "  ✅ обе зелёные разом: rc=0, вывод пуст"
else
  echo "❌ ЛОВУШКА: здоровые файлы дали шум или ненулевой rc. rc=$RC_CLEAN"
  echo "$OUT_CLEAN"; fail=1
fi

# ── Красные — поимённо, все разом (критерий 1 задания) ────────────────────
RED="$D/zhurnal/test-arka/kod_ruchnoj.md $D/HANDOFF-test-ruchnoj.md $D/ZAHOD-test-ruchnoj.md $D/PEREDACHA-test-ruchnoj.md"
OUT_RED=$($CHK $RED 2>&1)
RC_RED=$?
poimenno=0
for p in $RED; do
  echo "$OUT_RED" | grep -qF "$p" || poimenno=1
done
if [ "$RC_RED" = 1 ] && [ "$poimenno" = 0 ]; then
  echo "  ✅ четыре красных разом: rc=1, все названы поимённо"
else
  echo "❌ ЛОВУШКА: красные не покраснели разом или не все названы. rc=$RC_RED"
  echo "$OUT_RED"; fail=1
fi

# ── Чужой .md вообще не судится (не заход, не хэндофф) ────────────────────
OUT_NE=$($CHK "$D/ne-zahod.md" 2>&1)
RC_NE=$?
if [ "$RC_NE" = 0 ] && [ -z "$OUT_NE" ]; then
  echo "  ✅ чужой .md: молчание, rc=0"
else
  echo "❌ ЛОВУШКА: чужой .md не должен был попасть под суд. rc=$RC_NE"
  echo "$OUT_NE"; fail=1
fi

# ── Автоподбор --staged исключает СВОИ ЖЕ фикстуры ─────────────────────────
# Иначе коммит этих самых файлов (ZAHOD-test-ruchnoj.md и т.п., красные по
# имени) валил бы pre-commit хук в СВОЕЙ ЖЕ зоне — тот же приём и та же
# причина, что у check_uroki.staged_files() (см. докстринг staged_added_md).
OUT_FX=$(python3 -c "
import sys; sys.path.insert(0, '_generator/tools')
import check_marker
print([str(p) for p in check_marker.staged_added_md() if '/fixtures/marker/' in str(p)])
")
if [ "$OUT_FX" = "[]" ]; then
  echo "  ✅ автоподбор --staged: фикстуры marker/ исключены из своего же списка"
else
  echo "❌ ЛОВУШКА: автоподбор --staged видит собственные фикстуры — самокоммит себя завалит. $OUT_FX"
  fail=1
fi

# ── Положительный контроль Ш1 — HANDOFF.md без дефиса ТЕПЕРЬ ловится ──────
# До этого захода (`kod_ohvat.md`, 2026-08-11) файл демонстрировал слепую
# зону «имя без дефиса не ловится»; после расширения регэкспа она закрыта —
# табличный тест выше уже сверяет rc=1, здесь — что причина именно «имени
# теперь достаточно», а не «файл внезапно обзавёлся маркером».
if grep -q 'собран' "$D/HANDOFF.md"; then
  echo "❌ ЛОВУШКА: HANDOFF.md неожиданно несёт маркер — красный получен бы не тем путём"
  fail=1
else
  echo "  ✅ HANDOFF.md: красный получен именно расширением имени (маркера и так нет)"
fi

[ $fail = 0 ] && echo "ФИКСТУРЫ ЗЕЛЁНЫЕ" || echo "ФИКСТУРЫ КРАСНЫЕ — гейт сломан правкой"
exit $fail
