#!/bin/sh
# TOOL-CONTRACT-COVERS: porodit_slaid.py
# ↑ ОХВАТ: несущий принцип фазы 2 (заход porozhdenie-kartochki) — порождение по
# раскладке типа вместо ручной карточки. Здоровый вход + пять кривых, по одному
# на каждый запрет п.3 задачи; плюс идемпотентность и --sverit на синтетической
# лекции.
#
# Запуск:  sh _generator/tools/fixtures/porozhdenie/PROGNAT.sh
# Ожидание: ФИКСТУРЫ ЗЕЛЁНЫЕ, exit 0.
set -e
TOOLS=$(cd "$(dirname "$0")/../.." && pwd)
GENERATOR=$(cd "$TOOLS/.." && pwd)
REPO_ROOT=$(cd "$GENERATOR/.." && pwd)
P="$GENERATOR/sborka/porodit_slaid.py"

T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT

krasnet() {  # <описание> <регэксп ожидаемый в выводе> shift... <аргументы porodit_slaid.py>
  OPIS="$1"; PATTERN="$2"; shift 2
  OUT=$(python3 "$P" "$@" 2>&1) && {
    echo "❌ ЛОВУШКА НЕ СРАБОТАЛА: $OPIS — инструмент породил запрещённое (rc=0)"
    echo "$OUT"; exit 1
  }
  echo "$OUT" | grep -q "$PATTERN" || {
    echo "❌ ЛОВУШКА: красное есть, но не по делу («$PATTERN» не найдено). Вывод:"
    echo "$OUT"; exit 1
  }
  echo "  ✅ $OPIS"
}

echo "── здоровый вход: Т1 с центральным/вспомогательным/нарративом — rc=0, карточка на диске"
L="$T/lek-zdorovaya"
OUT=$(python3 "$P" "$L" --imya s01 --tip Т1 \
  --centralnyj "opredelenie:изоморфизм видов" \
  --vspomogatelnyj "primer:числовые примеры" \
  --narrativ "зачем сравнивать виды" 2>&1) || {
  echo "❌ ЗДОРОВЫЙ ВХОД УПАЛ:"; echo "$OUT"; exit 1; }
[ -f "$L/slajdy/s01/slaid.md" ] || {
  echo "❌ ЗДОРОВЫЙ ВХОД: карточка не создана на диске"; exit 1; }
grep -q "centralnyj_blok: изоморфизм видов" "$L/slajdy/s01/slaid.md" || {
  echo "❌ ЗДОРОВЫЙ ВХОД: centralnyj_blok не заполнен мыслью центрального блока"; exit 1; }
grep -q "^### \[primer\] числовые примеры$" "$L/slajdy/s01/slaid.md" || {
  echo "❌ ЗДОРОВЫЙ ВХОД: вспомогательный блок не породился"; exit 1; }
grep -c "^### \[opredelenie\] изоморфизм видов$" "$L/slajdy/s01/slaid.md" | grep -q "^2$" || {
  echo "❌ ЗДОРОВЫЙ ВХОД: центральный блок обязан стоять В ОБОИХ разделах (bloki.check_composition)"
  exit 1; }
grep -q "⟦решили не заполнять⟧" "$L/slajdy/s01/slaid.md" || {
  echo "❌ ЗДОРОВЫЙ ВХОД: необязательный блок 'utverzhdenie' раскладки Т1 не порождён с пометкой"
  exit 1; }
echo "  ✅ здоровый вход: карточка на диске, центральный/вспомогательный/опциональный блоки на месте"

echo "── идемпотентность: повторный вызов ТЕМ ЖЕ запросом не трогает файл"
HASH_DO=$(shasum "$L/slajdy/s01/slaid.md" | awk '{print $1}')
OUT=$(python3 "$P" "$L" --imya s01 --tip Т1 \
  --centralnyj "opredelenie:изоморфизм видов" \
  --vspomogatelnyj "primer:числовые примеры" \
  --narrativ "зачем сравнивать виды" 2>&1) || { echo "❌ повторный вызов упал:"; echo "$OUT"; exit 1; }
HASH_POSLE=$(shasum "$L/slajdy/s01/slaid.md" | awk '{print $1}')
[ "$HASH_DO" = "$HASH_POSLE" ] || { echo "❌ ИДЕМПОТЕНТНОСТЬ: файл изменился на повторном вызове"; exit 1; }
echo "$OUT" | grep -q "диф пуст" || { echo "❌ ИДЕМПОТЕНТНОСТЬ: не напечатано «диф пуст»"; exit 1; }
echo "  ✅ идемпотентность: тот же запрос — файл не тронут, диф пуст"

echo "── идемпотентность: РАЗНЫЙ запрос на существующее имя — печатает diff, НЕ перезаписывает"
OUT=$(python3 "$P" "$L" --imya s01 --tip Т1 --centralnyj "opredelenie:ДРУГОЕ" 2>&1) || {
  echo "❌ диф-режим упал:"; echo "$OUT"; exit 1; }
HASH_POSLE2=$(shasum "$L/slajdy/s01/slaid.md" | awk '{print $1}')
[ "$HASH_DO" = "$HASH_POSLE2" ] || { echo "❌ ИДЕМПОТЕНТНОСТЬ: разный запрос ПЕРЕЗАПИСАЛ файл"; exit 1; }
echo "$OUT" | grep -q "НЕ перезаписываю" || { echo "❌ диф-режим: не назван отказ от перезаписи"; exit 1; }
echo "  ✅ идемпотентность: разный запрос — диф напечатан, файл цел"

echo "── запрет 1: у Т1 центральным просят не [opredelenie]"
krasnet "Т1 с центральным utverzhdenie — отказ" "не \[opredelenie\]" \
  "$T/lek-zapret1" --imya s01 --tip Т1 --centralnyj "utverzhdenie:что-то"

echo "── запрет 2: у Т2/Т3 центральным просят не [utverzhdenie]"
krasnet "Т2 с центральным opredelenie — отказ" "не \[utverzhdenie\]" \
  "$T/lek-zapret2a" --imya s01 --tip Т2 --centralnyj "opredelenie:что-то"
krasnet "Т3 с центральным opredelenie — отказ" "не \[utverzhdenie\]" \
  "$T/lek-zapret2b" --imya s01 --tip Т3 --centralnyj "opredelenie:что-то"

echo "── запрет 3: два НЕСУЩИХ блока одного типа"
krasnet "два вспомогательных primer на Т1 — отказ" "два НЕСУЩИХ блока" \
  "$T/lek-zapret3" --imya s01 --tip Т1 --centralnyj "opredelenie:A" \
  --vspomogatelnyj "primer:B" --vspomogatelnyj "primer:C"

echo "── запрет 4: у Т4 просят блок кроме [narrativ]"
krasnet "Т4 с вспомогательным primer — отказ" "не предусматривает блок" \
  "$T/lek-zapret4a" --imya s01 --tip Т4 --centralnyj "narrativ:переход" \
  --vspomogatelnyj "primer:X"
krasnet "Т4 с доказательством — отказ" "не предусматривает блок" \
  "$T/lek-zapret4b" --imya s01 --tip Т4 --centralnyj "narrativ:итог" \
  --dokazatelstvo "Y"

echo "── запрет 5: у Т3 не задано доказательство"
krasnet "Т3 без --dokazatelstvo — отказ" "не задан обязательный блок \[Д\]" \
  "$T/lek-zapret5" --imya s01 --tip Т3 --centralnyj "utverzhdenie:запрет"

echo "── --sverit: пустая лекция (карточек нет) — отказ, а не трейсбек"
mkdir -p "$T/lek-pustaya/slajdy"
OUT=$(python3 "$P" "$T/lek-pustaya" --sverit 2>&1) && {
  echo "❌ --sverit на пустой лекции вернул rc=0"; echo "$OUT"; exit 1; }
echo "$OUT" | grep -q "карточек не найдено" || {
  echo "❌ --sverit на пустой лекции упал без внятной причины:"; echo "$OUT"; exit 1; }
echo "$OUT" | grep -q "Traceback" && {
  echo "❌ --sverit дал трейсбек вместо сообщения:"; echo "$OUT"; exit 1; }
echo "  ✅ --sverit на пустой лекции: внятный отказ, без трейсбека"

echo "── --sverit: свежепорождённая карточка Т1 сверяется как ЛЁГ"
OUT=$(python3 "$P" "$L" --sverit 2>&1) || { echo "❌ --sverit упал:"; echo "$OUT"; exit 1; }
echo "$OUT" | grep -q "сверено 1 карточек из 1" || {
  echo "❌ --sverit: строка охвата не напечатана верно:"; echo "$OUT"; exit 1; }
echo "$OUT" | grep -q "s01.*Т1.*Т1: ЛЁГ" || {
  echo "❌ --sverit: свежая карточка Т1 не сверилась как ЛЁГ:"; echo "$OUT"; exit 1; }
echo "$OUT" | grep -q "НЕ проверяю:" || {
  echo "❌ --sverit: блок слепых зон не напечатан:"; echo "$OUT"; exit 1; }
echo "  ✅ --sverit: свежая карточка сверена как ЛЁГ, охват и слепые зоны напечатаны"

echo "── живая дека L2: --sverit не падает, печатает охват по ВСЕМ карточкам"
# 🔴 ЧИСЛО СЧИТАЕТСЯ, А НЕ ВПИСЫВАЕТСЯ (KONSTITUCIYA §10). Здесь стояло «18 из 18»
# литералом, и ловушка молча покраснела, когда лекция доросла до 23 карточек: сама
# сверка была в полном порядке, врал ориентир. Это ровно тот случай, против которого
# правило и заведено, — и найден он тем, что ловушка встала на пути новой (Д8
# дочистки-2 pravila-kadra), которая из-за неё не исполнялась вовсе.
N_L2=$(ls -d "$REPO_ROOT"/teorkat-vvedenie/L2/slajdy/*/ | wc -l | tr -d ' ')
# 🔴 READ-ONLY СВЕРЯЕТСЯ СЛЕПКОМ ДО/ПОСЛЕ, А НЕ ЧИСТОТОЙ РАБОЧЕГО ДЕРЕВА.
# Здесь стоял `git status --porcelain -- teorkat-vvedenie/L2 | grep -q .`, и он
# краснел на ЛЮБОЙ грязи в лекции — в том числе на той, что оставил солвер при
# обычной сборке дека минутой раньше (`deck.py` дописывает kegl_px/liniya в
# карточки, это его работа). Ловушка обвиняла `--sverit` в чужой правке. Плюс
# `git status` не read-only сам: он переписывает индекс и берёт `.git/index.lock`
# (CLAUDE.md п.5), то есть фикстура могла уронить параллельный коммит. Слепок
# хэшей отвечает ровно на заданный вопрос — тронул ли файлы ЭТОТ прогон.
DO_L2=$(find "$REPO_ROOT/teorkat-vvedenie/L2/slajdy" -name slaid.md -exec shasum {} \; | sort)
OUT=$(python3 "$P" "$REPO_ROOT/teorkat-vvedenie/L2" --sverit 2>&1) || {
  echo "❌ --sverit на живой L2 упал:"; echo "$OUT"; exit 1; }
echo "$OUT" | grep -q "сверено $N_L2 карточек из $N_L2" || {
  echo "❌ --sverit на живой L2: охват не $N_L2 из $N_L2 (столько карточек лежит на диске):"
  echo "$OUT"; exit 1; }
POSLE_L2=$(find "$REPO_ROOT/teorkat-vvedenie/L2/slajdy" -name slaid.md -exec shasum {} \; | sort)
[ "$DO_L2" = "$POSLE_L2" ] || {
  echo "❌ ЖИВАЯ ДЕКА ИЗМЕНЕНА прогоном --sverit — READ-ONLY нарушен. Разошлись:"
  printf '%s\n' "$DO_L2" > "$T/do.txt"; printf '%s\n' "$POSLE_L2" > "$T/posle.txt"
  diff "$T/do.txt" "$T/posle.txt"; exit 1; }
echo "  ✅ живая L2: --sverit отработал, охват $N_L2 из $N_L2 (число снято с диска), карточки побайтово те же (READ-ONLY, слепок до/после)"

echo "── Д8 дочистки-2 (pravila-kadra): ОБА слота [primer] у Т2 доступны обычным флагом"
# Долг назван двумя заходами подряд: `--vspomogatelnyj-posle` завели, а обычный
# флаг по-прежнему бил ТОЛЬКО в первый слот — «после» через него не запросить, и
# второй такой же запрос падал на «слей в один блок» там, где слот был свободен.
LD8="$T/lek-d8"
OUT=$(python3 "$P" "$LD8" --imya dva-primera --tip Т2 \
  --centralnyj "utverzhdenie:главное" \
  --vspomogatelnyj "primer:пример ДО" \
  --vspomogatelnyj "primer:пример ПОСЛЕ" 2>&1) || {
  echo "❌ Д8: два --vspomogatelnyj primer у Т2 не породились — обычный флаг всё ещё бьёт в один слот:"
  echo "$OUT"; exit 1; }
# порядок в файле обязан быть раскладочный: П(до) · У(центральный) · П(после)
POR=$(grep -n "^### \[\(primer\|utverzhdenie\)\]" "$LD8/slajdy/dva-primera/slaid.md" | head -3 | sed 's/.*### //' | tr '\n' '|')
[ "$POR" = "[primer] пример ДО|[utverzhdenie] главное|[primer] пример ПОСЛЕ|" ] || {
  echo "❌ Д8: примеры легли не в те слоты — порядок в карточке: $POR"; exit 1; }
echo "$OUT" | grep -q "лёг в слот 1 из 2" || {
  echo "❌ Д8: молчаливая подстановка слота вернулась — нет заметки про слот 1 из 2:"
  echo "$OUT"; exit 1; }
echo "$OUT" | grep -q "vspomogatelnyj-posle" || {
  echo "❌ Д8: заметка не называет флаг, которым просить соседний слот:"; echo "$OUT"; exit 1; }
echo "  ✅ Д8: два обычных --vspomogatelnyj занимают ОБА слота Т2, порядок раскладочный, слот назван вслух"

echo "── Д8: ОДИН обычный флаг у многослотового типа — тоже не молчит"
OUT=$(python3 "$P" "$T/lek-d8b" --imya odin --tip Т2 \
  --centralnyj "utverzhdenie:главное" --vspomogatelnyj "primer:единственный" 2>&1) || {
  echo "❌ Д8: одиночный запрос упал:"; echo "$OUT"; exit 1; }
echo "$OUT" | grep -q "лёг в слот 1 из 2.*vspomogatelnyj-posle" || {
  echo "❌ Д8: одиночный --vspomogatelnyj у Т2 подставил слот МОЛЧА (это и был дефект):"
  echo "$OUT"; exit 1; }
echo "  ✅ Д8: одиночный запрос печатает, в какой слот лёг и каким флагом просить второй"

echo "── Д8: совет «слей в один блок» выдаётся ТОЛЬКО когда свободного слота нет"
krasnet "три primer на Т2 (слотов два) — отказ с ВЕРНЫМ советом" "все \
заняты" \
  "$T/lek-d8c" --imya tri --tip Т2 --centralnyj "utverzhdenie:У" \
  --vspomogatelnyj "primer:A" --vspomogatelnyj "primer:B" --vspomogatelnyj "primer:C"

echo "── Д8: --vspomogatelnyj-posle не сломан — по-прежнему метит в ПОСЛЕДНИЙ слот"
OUT=$(python3 "$P" "$T/lek-d8d" --imya posle --tip Т2 \
  --centralnyj "utverzhdenie:У" --vspomogatelnyj-posle "primer:только после" 2>&1) || {
  echo "❌ Д8: --vspomogatelnyj-posle упал:"; echo "$OUT"; exit 1; }
echo "$OUT" | grep -q "лёг в слот 2 из 2" || {
  echo "❌ Д8: --vspomogatelnyj-posle перестал метить в последний слот:"; echo "$OUT"; exit 1; }
echo "  ✅ Д8: --vspomogatelnyj-posle цел (заход tipologia-dochistka, Э2, не сломан)"

echo "ФИКСТУРЫ ЗЕЛЁНЫЕ"
