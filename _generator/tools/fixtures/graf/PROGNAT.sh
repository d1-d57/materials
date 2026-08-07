#!/usr/bin/env bash
# TOOL-CONTRACT-COVERS: graf_zavisimostej.py
# Фикстуры графа зависимостей лекции (graf_zavisimostej.py, заход kod_graf-zavisimostej.md).
# Гонять после каждой правки graf_zavisimostej.py:  bash _generator/tools/fixtures/graf/PROGNAT.sh
#
# Шесть случаев: заведомый цикл (обязан упасть) · законное раннее упоминание (обязан
# смолчать) · лекция без единой карточки нового формата (норма фазы 1, не трейсбек) ·
# три КРИВЫХ входа — несуществующая папка, файл вместо папки, битая карточка рядом со
# здоровой (кривой вход обязан дать читаемую ошибку, не Traceback).
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
TOOL="$HERE/../../graf_zavisimostej.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
OK=0

pusk () {                       # pusk <имя> <путь> <ожидаемый-код>
  out="$(python3 "$TOOL" "$2" 2>&1)"
  got=$?
  if echo "$out" | grep -q "Traceback"; then
    echo "  ✗ $1: УПАЛ ТРЕЙСБЕКОМ (код $got) — кривой вход обязан давать читаемую ошибку"
    OK=1
    return
  fi
  if [ "$got" = "$3" ]; then
    echo "  ✓ $1: код $got"
  else
    echo "  ✗ $1: код $got, ожидался $3"
    OK=1
  fi
}

echo "── ФИКСТУРЫ ГРАФА ЗАВИСИМОСТЕЙ ──"

# 1. Заведомый цикл в терминах (готовая фикстура рядом).
pusk "cikl" "$HERE/cikl" 1

# 2. Законное раннее упоминание — не краснеет (готовая фикстура рядом).
pusk "rannee-upominanie" "$HERE/rannee-upominanie" 0

# 3. Лекция без единой карточки нового формата — норма фазы 1, не трейсбек.
mkdir -p "$TMP/pustaya-lekcia"
pusk "pustaya-lekcia" "$TMP/pustaya-lekcia" 0

# 4. КРИВОЙ ВХОД: несуществующая папка.
pusk "net-papki" "$TMP/net-takoj-papki-voobsche" 2

# 5. КРИВОЙ ВХОД: путь — файл, а не папка.
echo "я не папка" > "$TMP/ya-fajl.txt"
pusk "ne-papka" "$TMP/ya-fajl.txt" 2

# 6. КРИВОЙ ВХОД: битая карточка (нет tip_verstki) рядом со здоровой — не падает,
#    печатает предупреждение и работает с тем, что смог разобрать.
mkdir -p "$TMP/bitaya-kartochka/slajdy/bitaya" "$TMP/bitaya-kartochka/slajdy/zdorovaya"
cat > "$TMP/bitaya-kartochka/slajdy/bitaya/slaid.md" <<'EOF'
---
imya: bitaya
nazvanie: Без обязательного поля
---
EOF
cat > "$TMP/bitaya-kartochka/slajdy/zdorovaya/slaid.md" <<'EOF'
---
imya: zdorovaya
tip_verstki: polosa_gorizontalnaya
vvodit: [termin-zdorovyj]
---
EOF
pusk "bitaya-kartochka" "$TMP/bitaya-kartochka" 0

echo
[ "$OK" = 0 ] && echo "ВСЁ ЗЕЛЁНОЕ" || echo "ЕСТЬ ПРОВАЛЫ"
exit "$OK"
