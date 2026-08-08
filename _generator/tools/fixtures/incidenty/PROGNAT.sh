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
#    Вердикт того же дня, что строка, но ПОЗЖЕ неё по часам — явное время,
#    не угадывание формата (старый костыль same-day-если-сегодня отсюда убран).
cat > "$TMP/4-incidenty.md" <<EOF
- $DATA_9D 10:00 · arka/mat-kostyak · merge arka/x: конфликт в 1 путях · → разрешить конфликты · статус: открыт
EOF
cat > "$TMP/4-verdikty.md" <<EOF
- E конфликт путей · вердикт: шум: конфликты — обычная жизнь ветвления · дата данных: $DATA_9D 12:00
EOF
pusk "4-shum" 0 "$TMP/4-incidenty.md" "$TMP/4-verdikty.md"

# 5. Класс-корзина «шум» получил строку ПОЗЖЕ даты вердикта — красное с именем класса.
cat > "$TMP/5-incidenty.md" <<EOF
- $DATA_9D 10:00 · arka/mat-kostyak · коммит с --no-verify: старый чужой долг · → чинить · статус: открыт
- $DATA_3D 10:00 · arka/mat-kostyak · коммит с --no-verify: новый чужой долг · → чинить · статус: открыт
EOF
cat > "$TMP/5-verdikty.md" <<EOF
- C прочий чужой долг · вердикт: шум: разнородное, отдельного класса не образует · дата данных: $DATA_9D
EOF
python3 "$GATE" --incidenty "$TMP/5-incidenty.md" --verdikty "$TMP/5-verdikty.md" > "$TMP/5.out" 2>&1
got=$?
if [ "$got" = "1" ] && grep -q "C прочий чужой долг" "$TMP/5.out"; then
  echo "  ✓ 5-korzina-vyroslo: код $got, класс в выводе"
else
  echo "  ✗ 5-korzina-vyroslo: код $got, или класса нет в выводе"
  cat "$TMP/5.out"
  OK=1
fi

# 6. Вердикт «шум» со ВРЕМЕНЕМ, строка ТОГО ЖЕ дня РАНЬШЕ по часам — зелёный.
#    Ровно живой случай класса C 04.08: вердикт написан ПОСЛЕ строки в тот же
#    день; старый костыль («сегодняшний вердикт — всегда подозрительно»)
#    красил бы это независимо от часов, правка 2 отличает по факту.
SEGODNYA=$(python3 -c "from datetime import date; print(date.today().isoformat())")
cat > "$TMP/6-incidenty.md" <<EOF
- $SEGODNYA 08:00 · arka/mat-kostyak · коммит с --no-verify: чужой долг: тест раньше вердикта · → чинить · статус: открыт
EOF
cat > "$TMP/6-verdikty.md" <<EOF
- C прочий чужой долг · вердикт: шум: тестовый вердикт с временем · дата данных: $SEGODNYA 09:00
EOF
pusk "6-shum-so-vremenem-ranshe" 0 "$TMP/6-incidenty.md" "$TMP/6-verdikty.md"

# 7. Та же пара часов, но строка ПОЗЖЕ вердикта — по-прежнему красный:
#    «шум» не бывает вечным даже внутри одного дня, когда порядок известен.
cat > "$TMP/7-incidenty.md" <<EOF
- $SEGODNYA 10:00 · arka/mat-kostyak · коммит с --no-verify: чужой долг: тест позже вердикта · → чинить · статус: открыт
EOF
cat > "$TMP/7-verdikty.md" <<EOF
- C прочий чужой долг · вердикт: шум: тестовый вердикт с временем · дата данных: $SEGODNYA 09:00
EOF
python3 "$GATE" --incidenty "$TMP/7-incidenty.md" --verdikty "$TMP/7-verdikty.md" > "$TMP/7.out" 2>&1
got=$?
if [ "$got" = "1" ] && grep -q "C прочий чужой долг" "$TMP/7.out"; then
  echo "  ✓ 7-shum-so-vremenem-pozhe: код $got, класс в выводе"
else
  echo "  ✗ 7-shum-so-vremenem-pozhe: код $got, или класса нет в выводе"
  cat "$TMP/7.out"
  OK=1
fi

# 8. Вердикт «закрыт гейтом `<имя>`» (заход zamykanie-reestrov, ## ПЛАН) —
#    новая форма словаря, признаётся типом «закрыт» и класс молчит, exit 0.
#    Владелец дословно: «должны писать, что закрыт гейтом КОНКРЕТНО» — до этой
#    формы «закрыт» умел только голую дату, имя гейта уходило мимо машины.
cat > "$TMP/8-incidenty.md" <<EOF
- $DATA_9D 10:00 · arka/mat-kostyak · план не готов или битый (см. вывод команды) · → поправить план · статус: открыт
EOF
cat > "$TMP/8-verdikty.md" <<EOF
- I план битый · вердикт: закрыт гейтом \`check_plan_svezhest.py\` · дата данных: $DATA_9D
EOF
pusk "8-zakryt-gejtom" 0 "$TMP/8-incidenty.md" "$TMP/8-verdikty.md"

# 9. Regression guard: «закрыт гейтом» БЕЗ backtick-имени — сломанная форма,
#    razobrat_verdikt() обязан вернуть None (класс остаётся БЕЗ вердикта, а не
#    молча приниматься), иначе вписать пустое имя гейта стало бы легальным.
cat > "$TMP/9-incidenty.md" <<EOF
- $DATA_9D 10:00 · arka/mat-kostyak · план не готов или битый (см. вывод команды) · → поправить план · статус: открыт
EOF
cat > "$TMP/9-verdikty.md" <<EOF
- I план битый · вердикт: закрыт гейтом плохая форма · дата данных: $DATA_9D
EOF
python3 "$GATE" --incidenty "$TMP/9-incidenty.md" --verdikty "$TMP/9-verdikty.md" > "$TMP/9.out" 2>&1
got=$?
if [ "$got" = "1" ] && grep -q "I план битый" "$TMP/9.out"; then
  echo "  ✓ 9-zakryt-gejtom-bez-imeni: код $got, класс без вердикта поймал сломанную форму"
else
  echo "  ✗ 9-zakryt-gejtom-bez-imeni: код $got, или класса нет в выводе — сломанная форма молча принята"
  cat "$TMP/9.out"
  OK=1
fi

echo
[ "$OK" = 0 ] && echo "ВСЁ ЗЕЛЁНОЕ" || echo "ЕСТЬ ПРОВАЛЫ"
exit "$OK"
