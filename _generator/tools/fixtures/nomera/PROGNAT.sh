#!/usr/bin/env bash
# Фикстуры опт-ина `nomera: da` (build_doc.py, 2026-07-30).
# Гонять после каждой правки build_doc.py:  bash _generator/tools/fixtures/nomera/PROGNAT.sh
#
# Флаг может ПРОЙТИ (номер показан) — значит обязана быть фикстура, на которой видно,
# что без флага он НЕ показан, и что умолчание не поехало. Оба случая проверяются здесь.
set -u

BUILD="$(cd "$(dirname "$0")/../../.." && pwd)/build_doc.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
OK=0

telo () {                       # telo <шапка-доп>
  cat <<EOF
---
tab: Фикстура
status: chernovik
poryadok: 1
$1
---

# Фикстура

**Утверждение 7 (проба).** Тело утверждения.

Ссылка: по утверждению 7 видно, что всё сошлось.
EOF
}

proba () {                      # proba <имя> <доп-шапка> <ожидание: est|net>
  local name="$1" shapka="$2" want="$3" d="$TMP/$1" got=""
  mkdir -p "$d"
  telo "$shapka" > "$d/proba.md"
  python3 "$BUILD" "$d" >/dev/null 2>&1
  if grep -q '<span class="lbl">Утверждение 7 (проба)' "$d/view.html" 2>/dev/null; then got=est; else got=net; fi
  if [ "$got" = "$want" ]; then
    echo "  ✓ $name: номер в метке — $got"
  else
    echo "  ✗ $name: номер в метке — $got, ожидался $want"
    OK=1
  fi
}

echo "── ФИКСТУРЫ ОПТ-ИНА nomera ──"
proba "bez-flaga"      ""             net      # умолчание: номера НЕТ (решение владельца 28.07)
proba "s-flagom-da"    "nomera: da"   est      # опт-ин: номер ЕСТЬ
proba "s-flagom-net"   "nomera: net"  net      # явное «нет» ведёт себя как умолчание
proba "musor-v-flage"  "nomera: ???"  net      # непонятное значение НЕ включает флаг

# ссылка обязана резолвиться в обоих режимах
for d in "$TMP/bez-flaga" "$TMP/s-flagom-da"; do
  if grep -q 'class="xref"' "$d/view.html"; then
    echo "  ✓ $(basename "$d"): автоссылка на месте"
  else
    echo "  ✗ $(basename "$d"): автоссылка пропала"; OK=1
  fi
done

echo
[ "$OK" = 0 ] && echo "ВСЁ ЗЕЛЁНОЕ" || echo "ЕСТЬ ПРОВАЛЫ"
exit "$OK"
