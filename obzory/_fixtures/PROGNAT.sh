#!/usr/bin/env bash
# Фикстуры гейта паспортов (obzory/spisok.py --proverit).
# Зелёный гейт ничего не доказывает, пока не показано, на чём он КРАСНЕЕТ.
# Гонять после каждой правки spisok.py:  bash obzory/_fixtures/PROGNAT.sh
#
# Фикстуры собираются во временной папке, а не лежат в obzory/ рядом с живыми
# обзорами: ломающая фикстура внутри obzory/ красила бы гейт всегда и была бы
# неотличима от настоящего долга (та же ловушка, что описана в KARTA §6 про
# _generator/tools/fixtures/). Папки на `_` гейт и так пропускает.
set -u

GATE="$(cd "$(dirname "$0")/.." && pwd)/spisok.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
OK=0

pusk () {                       # pusk <имя> <ожидаемый-код>
  local name="$1" want="$2"
  python3 "$TMP/obzory/spisok.py" --proverit >/dev/null 2>&1
  local got=$?
  if [ "$got" = "$want" ]; then
    echo "  ✓ $name: код $got"
  else
    echo "  ✗ $name: код $got, ожидался $want"
    OK=1
  fi
}

echo "── ФИКСТУРЫ ГЕЙТА ПАСПОРТОВ ──"

# 1. здоровый обзор — гейт обязан молчать
mkdir -p "$TMP/obzory/zdorovyj/src"
cp "$GATE" "$TMP/obzory/spisok.py"
cat > "$TMP/obzory/zdorovyj/src/obzor.md" <<'EOF'
---
tab: Здоровый обзор
tema: тема есть
oblast: область есть
klyuchevye: ключевые есть
data: 2026-01-01
status: chistovik
---

# Здоровый
EOF
pusk "здоровый обзор ⇒ зелёный" 0

# 2. шапка без обязательных полей — гейт обязан покраснеть
mkdir -p "$TMP/obzory/bez-pasporta/src"
cat > "$TMP/obzory/bez-pasporta/src/obzor.md" <<'EOF'
---
tab: Без паспорта
status: skelet
---

# Без паспорта
EOF
pusk "обзор без полей ⇒ красный" 1
rm -rf "$TMP/obzory/bez-pasporta"

# 3. папка без источника вовсе — гейт обязан покраснеть
mkdir -p "$TMP/obzory/pustaya"
pusk "папка без src/*.md ⇒ красный" 1
rm -rf "$TMP/obzory/pustaya"

# 4. служебная папка на `_` — гейт обязан её пропустить
mkdir -p "$TMP/obzory/_sluzhebnaya"
pusk "папка на _ пропускается ⇒ зелёный" 0

echo
[ "$OK" = 0 ] && echo "ВСЁ ЗЕЛЁНОЕ" || echo "ЕСТЬ ПРОВАЛЫ"
exit "$OK"
