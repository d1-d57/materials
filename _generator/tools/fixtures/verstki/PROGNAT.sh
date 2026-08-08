#!/bin/sh
# TOOL-CONTRACT-COVERS: gejt_verstki.py
# Фикстуры ГЕЙТА ВЁРСТКИ. Гоняй ПОСЛЕ любой правки gejt_verstki.py.
# Строка COVERS выше — не украшение: по ней хук решает, поднимать ли фикстуру
# (тот же приём, что у соседа `fixtures/illyustracii/PROGNAT.sh:2`).
#
# Запуск:  sh _generator/tools/fixtures/verstki/PROGNAT.sh
# Ожидание: ФИКСТУРЫ ЗЕЛЁНЫЕ, exit 0.
#
# ЗАЧЕМ. Разбор Лекции 2 владельцем (заход `verstka-v-faze-1`) — 5 ловушек ниже это ровно
# критерий готовности того захода: Д2 (полоса без иллюстрации) и Д6 (вёрстка без обоснования)
# по паре красный/зелёный каждая, плюс регрессионная защита от разночтения В3/В4 этого же захода
# (`## ПЛАН` п.5) — Д4 (обложка) НЕ гейтится нигде в этом инструменте, ловушка 5 это доказывает.
cd "$(dirname "$0")/../../../.." || exit 1
TOOL=_generator/tools/gejt_verstki.py
FIX=_generator/tools/fixtures/verstki
fail=0

ok() { echo "  ✅ $1"; }
no() { echo "  ❌ $1"; fail=1; }
je() { [ "$2" = "$3" ] && ok "$1 (rc=$2)" || no "$1: rc=$2, ожидался $3"; }

# 1 — Д2: полоса, illustracii: [] → красный
python3 $TOOL "$FIX/polosa-bez-illustracii" --tiho
je "1. полоса без иллюстрации" "$?" "1"
python3 $TOOL "$FIX/polosa-bez-illustracii" 2>&1 | grep -q "Д2" \
  && ok "1. класс Д2 назван в выводе" \
  || no "1. класс Д2 не найден в выводе"

# 2 — Д2 здоровый: полоса + иллюстрация → зелёный
python3 $TOOL "$FIX/polosa-s-illustraciej" --tiho
je "2. полоса с иллюстрацией" "$?" "0"

# 3 — Д6: tip_verstki без obosnovanie_verstki → красный
python3 $TOOL "$FIX/bez-obosnovaniya" --tiho
je "3. вёрстка без обоснования" "$?" "1"
python3 $TOOL "$FIX/bez-obosnovaniya" 2>&1 | grep -q "Д6" \
  && ok "3. класс Д6 назван в выводе" \
  || no "3. класс Д6 не найден в выводе"

# 4 — Д6 здоровый: обоснование есть → зелёный
python3 $TOOL "$FIX/s-obosnovaniem" --tiho
je "4. вёрстка с обоснованием" "$?" "0"

# 5 — Д4 регрессия: лекция без слайда типа oblozhka/vizitka/finalnyj — ЗЕЛЁНЫЙ (Д4 не гейтится;
# см. `## ПЛАН` п.5 захода — В4 в исходном тексте ждал здесь «красный», это исправлено сознательно)
python3 $TOOL "$FIX/bez-oblozhki" --tiho
je "5. лекция без обложки (Д4 сознательно не гейтится)" "$?" "0"

# кривой вход — без аргументов
python3 $TOOL >/dev/null 2>&1
je "6. без аргументов" "$?" "2"

# кривой вход — путь не существует
python3 $TOOL "$FIX/net-takoj-papki" >/dev/null 2>&1
je "7. несуществующий путь лекции" "$?" "2"

[ $fail = 0 ] && echo "ФИКСТУРЫ ЗЕЛЁНЫЕ" || echo "ФИКСТУРЫ КРАСНЫЕ — гейт вёрстки сломан правкой"
exit $fail
