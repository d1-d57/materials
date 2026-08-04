#!/usr/bin/env bash
# TOOL-CONTRACT-COVERS: check_incidenty.py
# Фикстуры гейта разбора инцидентов (check_incidenty.py, 2026-08-04).
# Гонять после каждой правки: bash _generator/tools/fixtures/incidenty/PROGNAT.sh
#
# Гейт может ПРОЙТИ — значит обязана быть фикстура, на которой он ПАДАЕТ.
# Четыре случая — ровно КРИТЕРИЙ ГОТОВНОСТИ захода kod_gejt-razbora.md:
# нормальный ритм молчит, застоявшийся класс краснеет с именем и возрастом,
# обещанный-но-не-собранный заход краснеет с именем файла, «шум» — законный
# и молчаливый выход.
set -u

GATE="$(cd "$(dirname "$0")/../.." && pwd)/check_incidenty.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
OK=0

# Даты относительно СЕГОДНЯ — портируемо (без GNU `date -d`), через python3.
DATA_3D=$(python3 -c "from datetime import date, timedelta; print((date.today()-timedelta(days=3)).isoformat())")
DATA_9D=$(python3 -c "from datetime import date, timedelta; print((date.today()-timedelta(days=9)).isoformat())")

pusk () {                       # pusk <имя> <ожидаемый-код> <incidenty> <verdikty>
  python3 "$GATE" --incidenty "$3" --verdikty "$4" > "$TMP/$1.out" 2>&1
  got=$?
  if [ "$got" = "$2" ]; then
    echo "  ✓ $1: код $got"
  else
    echo "  ✗ $1: код $got, ожидался $2"
    cat "$TMP/$1.out"
    OK=1
  fi
}

echo "── ФИКСТУРЫ ГЕЙТА РАЗБОРА ИНЦИДЕНТОВ ──"

# 1. Класс без вердикта, старейшая строка 3 дня назад — нормальный ритм, exit 0.
cat > "$TMP/1-incidenty.md" <<EOF
- $DATA_3D 10:00 · arka/mat-kostyak · план не готов или битый (см. вывод команды) · → поправить план · статус: открыт
EOF
: > "$TMP/1-verdikty.md"
pusk "1-svezhij-bez-verdikta" 0 "$TMP/1-incidenty.md" "$TMP/1-verdikty.md"

# 2. Класс без вердикта, старейшая строка 9 дней назад — красное, в выводе класс и «9 дней».
cat > "$TMP/2-incidenty.md" <<EOF
- $DATA_9D 10:00 · arka/mat-kostyak · план не готов или битый (см. вывод команды) · → поправить план · статус: открыт
EOF
: > "$TMP/2-verdikty.md"
python3 "$GATE" --incidenty "$TMP/2-incidenty.md" --verdikty "$TMP/2-verdikty.md" > "$TMP/2.out" 2>&1
got=$?
if [ "$got" = "1" ] && grep -q "I план битый" "$TMP/2.out" && grep -q "9 дней" "$TMP/2.out"; then
  echo "  ✓ 2-stalyj-bez-verdikta: код $got, класс и «9 дней» в выводе"
else
  echo "  ✗ 2-stalyj-bez-verdikta: код $got, или в выводе нет класса/«9 дней»"
  cat "$TMP/2.out"
  OK=1
fi

# 3. Вердикт «дефект → заход kod_nesuschestvuyuschiy.md» — файла нет на диске, красное с именем.
cat > "$TMP/3-incidenty.md" <<EOF
- $DATA_9D 10:00 · arka/mat-kostyak · план не готов или битый (см. вывод команды) · → поправить план · статус: открыт
EOF
cat > "$TMP/3-verdikty.md" <<EOF
- I план битый · вердикт: дефект → заход kod_nesuschestvuyuschiy.md · дата данных: $DATA_9D
EOF
python3 "$GATE" --incidenty "$TMP/3-incidenty.md" --verdikty "$TMP/3-verdikty.md" > "$TMP/3.out" 2>&1
got=$?
if [ "$got" = "1" ] && grep -q "kod_nesuschestvuyuschiy.md" "$TMP/3.out"; then
  echo "  ✓ 3-otsutstvuyushij-zahod: код $got, имя отсутствующего файла в выводе"
else
  echo "  ✗ 3-otsutstvuyushij-zahod: код $got, или имени файла нет в выводе"
  cat "$TMP/3.out"
  OK=1
fi

# 4. Вердикт «шум: конфликты — обычная жизнь ветвления» — законный выход, exit 0.
cat > "$TMP/4-incidenty.md" <<EOF
- $DATA_9D 10:00 · arka/mat-kostyak · merge arka/x: конфликт в 1 путях · → разрешить конфликты · статус: открыт
EOF
cat > "$TMP/4-verdikty.md" <<EOF
- E конфликт путей · вердикт: шум: конфликты — обычная жизнь ветвления · дата данных: $DATA_9D
EOF
pusk "4-shum" 0 "$TMP/4-incidenty.md" "$TMP/4-verdikty.md"

echo
[ "$OK" = 0 ] && echo "ВСЁ ЗЕЛЁНОЕ" || echo "ЕСТЬ ПРОВАЛЫ"
exit "$OK"
