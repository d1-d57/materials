#!/usr/bin/env bash
# TOOL-CONTRACT-COVERS: reviziya_dolgov.py
# Фикстуры чекера статусов DOLG.md (reviziya_dolgov.py, 2026-08-08).
# Гонять после каждой правки:  bash _generator/tools/fixtures/reviziya_dolgov/PROGNAT.sh
#
# Кривой вход обязан падать ГРОМКО (rc=1, понятное сообщение), а не молчать
# и не трейсбеком. Плюс: запись без статуса обязана красить rc, здоровая — нет.
set -u

TOOL="$(cd "$(dirname "$0")/../.." && pwd)/reviziya_dolgov.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
OK=0

pusk () {                       # pusk <файл> <ожидаемый-код>
  out=$(python3 "$TOOL" "$1" 2>&1)
  got=$?
  if [ "$got" = "$2" ]; then
    echo "  v $(basename "$1"): код $got"
  else
    echo "  x $(basename "$1"): код $got, ожидался $2"
    echo "$out"
    OK=1
  fi
}

echo "-- ФИКСТУРЫ ЧЕКЕРА СТАТУСОВ DOLG.md --"

# 1. КРИВОЙ ВХОД: путь не существует — обязан упасть громко, rc=1, без трейсбека.
pusk "$TMP/net-takogo-fajla.md" 1

# 2. ЗДОРОВЫЙ ВХОД: у обеих записей (табличной и нарративной) есть статус — rc=0.
cat > "$TMP/zdorovyj.md" <<'EOF'
| Д1 | долг раз | откуда <br>СТАТУС: ЖИВ · 2026-08-08 · `команда` → вывод |

## Долг 2 — долг два

текст долга.

СТАТУС: МЁРТВ · 2026-08-08 · `команда` → вывод

---
EOF
pusk "$TMP/zdorovyj.md" 0

# 3. КРИВОЙ ВХОД: у табличной записи статуса нет — гейт обязан покраснеть.
cat > "$TMP/bez-statusa.md" <<'EOF'
| Д1 | долг раз | откуда |

## Долг 2 — долг два

текст долга.

СТАТУС: МЁРТВ · 2026-08-08 · `команда` → вывод

---
EOF
pusk "$TMP/bez-statusa.md" 1

echo
[ "$OK" = 0 ] && echo "ВСЁ ЗЕЛЁНОЕ" || echo "ЕСТЬ ПРОВАЛЫ"
exit "$OK"
