#!/bin/sh
# TOOL-CONTRACT-COVERS: check_sborki.py postroit_kartochku.py sravnit.py progon_baza.py
# ↑ ОХВАТ: гейт сборки как механизм — семь ИСПОЛНЯЮЩИХ проверок (С1-С7) над
# утверждениями файла-захода о мире, плюс граница безопасности §2.1 (белый
# список, отказ от shell, потолок, таймаут). Ловушка 25 (заход obratnyj-progon)
# — кривой вход `postroit_kartochku.py`/`sravnit.py` (Э3: временная карточка
# из старого слайда → компиляция → солвер) обязан падать ГРОМКО, не молчать.
#
# Запуск:  sh _generator/tools/fixtures/sborka/PROGNAT.sh
# Ожидание: ФИКСТУРЫ ЗЕЛЁНЫЕ, exit 0.
#
# ЛОВУШЕК ДВАДЦАТЬ ЧЕТЫРЕ. Ловушки 18-24 — регрессионные, все семь предъявлены
# верификатором §3 на живом инструменте; 18 и 19 закрывают НАСТОЯЩИЕ ДЫРЫ
# безопасности, остальные — молчаливые пропуски ложных утверждений.
#   1. 🔴 ПОЛОЖИТЕЛЬНЫЙ КОНТРОЛЬ НА ЖИВОМ МАТЕРИАЛЕ — синтетический заход, КАЖДОЕ
#      утверждение которого истинно про ЭТОТ репозиторий (живая ветка, живые
#      пути, живая команда с числом, снятым прогоном): rc=0 и ни одного ❌.
#      Главная ловушка фикстуры: она сторожит не поломку, а излишнюю строгость,
#      от которой гейт отключат. Числа в неё не вписаны — они ЗАМЕРЯЮТСЯ здесь же.
#   2. 🔴 ПОЛОЖИТЕЛЬНЫЙ КОНТРОЛЬ НА ЖИВОМ ЗАХОДЕ — настоящий `kod_*.md` корпуса:
#      гейт обязан отработать без трейсбека и напечатать блок слепых зон. Красное
#      на живом корпусе ожидаемо (заходы ссылаются на снесённые ветки), поэтому
#      сторожится ПАДЕНИЕ и МОЛЧАНИЕ ПРО ОХВАТ, а не вердикт.
#   3. С1 (урок 41): ветка объявлена стоящей, её нет — красный поимённо.
#   4. С1 положительная: ветки нет, но заход её САМ заводит `worktree add
#      --branch` — обязана молчать (иначе гейт краснеет на каждом здоровом
#      worktree-заходе).
#   5. С2 (урок 30): зона в чужом репозитории, `GIT_ZONA_REPO` не назвала.
#   6. С3a (урок 45): путь-якорь не существует — красный поимённо.
#   7. С3b (уроки 45 и 27): якорь ЕСТЬ на диске, но его НЕТ на ветке, куда послан
#      исполнитель, — в его worktree файла не будет. Ветка-мишень ЗАМЕРЯЕТСЯ.
#   8. С4 (урок 42): команда критерия даёт не то число, что стоит рядом.
#   9. С4 положительная: то же число совпало — обязана молчать.
#  10. С4 (урок 45): команда критерия падает трейсбеком.
#  11. С5 (урок 47): подкоманда зовётся позиционно, живой CLI позиционных не берёт.
#  12. С5: подкоманды не существует вовсе.
#  13. С6 (урок 33): «не существует» без команды рядом.
#  14. С6 положительная: то же утверждение С КОМАНДОЙ рядом — обязана молчать.
#  15. С7: ветка к влитию трогает пути вне названной зоны слияния.
#  16. 🔴 ГЛАВНАЯ, ВАЖНЕЕ ПОЛНОТЫ: `rm -rf`, `git push`, `git checkout`, редирект в
#      файл — напечатаны как непроверенные и НЕ ВЫПОЛНЕНЫ. Доказывается ФАКТОМ НА
#      ДИСКЕ: два файла-мишени целы и с прежним содержимым, ветка репозитория не
#      сменилась. Мишень внутри репозитория нужна отдельно от мишени снаружи:
#      наружная отклоняется ещё и правилом «путь вне репозитория», и без
#      внутренней нельзя сказать, сработало ли правило БЕЛОГО СПИСКА ПРОГРАММ.
#  17. Белый список: число входов, обещанное докстрингом, сходится с таблицей
#      (`assert` при импорте) — обещание в докстринге не расходится с кодом молча.
#  18. 🔴 ДЫРА ВЕРИФИКАТОРА: приклеенное значение опции (`grep -cf/путь`, `git -O/путь`)
#      обходило проверку «путь внутри репозитория» и читало файлы снаружи.
#  19. 🔴 ДЫРА ВЕРИФИКАТОРА: катастрофический бэктрекинг — 3 КБ прозы вешали разбор
#      навсегда, мимо таймаута (висел regex, не подпроцесс). Сторожится ВРЕМЕНЕМ.
#  20. Пропуск: ветка названа прозой без префикса `zahod/` — С1 не запускался вовсе.
#  21. Пропуск: число критерия обещано без стрелки («обязана вернуть N») — С4 молчал.
#  22. Пропуск: значение позиционного выбора вне `{add,drop,list}` — С5 сверял арность,
#      а не значение, держа usage со списком в руках.
#  23. Пропуск: `GIT_ZONA_REPO`, упомянутая ОТРИЦАНИЕМ, снимала С2 целиком.
#  24. Пропуск: якоря, оформленные ```-блоком, были невидимы для С3.
set -e
TOOLS=$(cd "$(dirname "$0")/../.." && pwd)
REPO_ROOT=$(cd "$TOOLS/../.." && pwd)
unset $(git rev-parse --local-env-vars) 2>/dev/null || true

P="$TOOLS/check_sborki.py"
ARKA="$REPO_ROOT/_studio/zhurnal/2026-08-05_faza-lenty"

T=$(mktemp -d)
# Мишень ВНУТРИ репозитория — в собственной папке фикстуры, чтобы худший исход
# сломанного гейта стоил одного временного файла, а не чужой работы.
MISHEN_VNUTRI="$TOOLS/fixtures/sborka/MISHEN-vremennaya.txt"
trap 'rm -rf "$T"; rm -f "$MISHEN_VNUTRI"' EXIT

krasnet() {  # <описание> <ожидаемый_код> <файл>
  OPIS="$1"; KOD="$2"; FILE="$3"
  OUT=$(python3 "$P" "$FILE" 2>&1) && {
    echo "❌ ЛОВУШКА НЕ СРАБОТАЛА: $OPIS — гейт принял ложное утверждение о мире"
    echo "$OUT"; exit 1
  }
  echo "$OUT" | grep -q "❌ $KOD" || {
    echo "❌ ЛОВУШКА: красное есть, но НЕ от $KOD поимённо. Вывод:"
    echo "$OUT"; exit 1
  }
  echo "  ✅ $OPIS — $KOD покраснел поимённо"
}

molchit() {  # <описание> <код, который НЕ должен прозвучать> <файл>
  OPIS="$1"; KOD="$2"; FILE="$3"
  if OUT=$(python3 "$P" "$FILE" 2>&1); then :; else :; fi
  echo "$OUT" | grep -q "❌ $KOD" && {
    echo "❌ ЛОВУШКА: $OPIS — $KOD дал ЛОЖНОЕ КРАСНОЕ, ровно то, из-за которого гейт обходят:"
    echo "$OUT"; exit 1
  }
  echo "  ✅ $OPIS — $KOD молчит"
}

# ── ЗАМЕРЫ ЖИВОГО МИРА: ни одно число и ни одно имя не вписано в фикстуру рукой ─
VETKA=$(cd "$REPO_ROOT" && git --no-optional-locks rev-parse --abbrev-ref HEAD)
DEFOV=$(cd "$REPO_ROOT" && grep -c "def " _generator/tools/check_zahod.py)
# Ветка, на которой заведомо НЕТ этого самого гейта, — для ловушки 7 (С3b).
VETKA_BEZ=""
for B in $(cd "$REPO_ROOT" && git --no-optional-locks branch --format='%(refname:short)'); do
  if ! (cd "$REPO_ROOT" && git --no-optional-locks cat-file -e "$B:_generator/tools/check_sborki.py" 2>/dev/null); then
    VETKA_BEZ="$B"; break
  fi
done
# Ветка, которую можно назвать «к влитию» в ловушке 15.
# 🔴 `--format` ДО `--no-merged`, и это не косметика: у `--no-merged` аргумент
# необязательный, и `git branch --no-merged --format=…` съедает `--format=…` как
# имя коммита («fatal: malformed object name»). Поймано первым прогоном фикстуры:
# ловушка 15 молча пропускалась при семи невлитых ветках в репозитории.
VETKA_VLIT=$(cd "$REPO_ROOT" && git --no-optional-locks branch --format='%(refname:short)' --no-merged | head -1)
echo "── замеры живого мира: ветка=$VETKA · def-ов в check_zahod.py=$DEFOV · без гейта=${VETKA_BEZ:-нет} · к влитию=${VETKA_VLIT:-нет}"

# ── эталон здорового захода: КАЖДОЕ утверждение истинно про живой репозиторий ──
sobrat_zdorovyj() {  # <путь>
  cat > "$1" <<MD
# Канал исполнителя — proba (эталон фикстуры)

## КОНТРАКТ ЗОНЫ (обязателен)
- **МЕСТО РАБОТЫ:** worktree захода; \`git rev-parse --abbrev-ref HEAD\` обязано быть \`$VETKA\`.
- **ЗОНА (можно менять):** \`_generator/tools/proba-zony.py\`. Всё вне — READ-ONLY.
- Отчёт пишется в файл ОСНОВНОЙ папки репозитория, по абсолютному пути.

## 0. ПЕРВЫЙ ХОД
- **Прочитать ТОЛЬКО это:**
  1. \`_generator/tools/check_zahod.py\` — лексический сосед.
  2. \`_generator/tools/priyomka.py\` — приёмка отчёта.

## 2. ЗАДАЧА
Сделать X, ровно по шагам. Файла \`_generator/tools/net-takogo-fajla.py\` не существует, проверено: \`test -e _generator/tools/net-takogo-fajla.py\`.

**КРИТЕРИЙ ГОТОВНОСТИ (может ПРОВАЛИТЬСЯ):**
1. Живой прогон на реальном файле: \`grep -c "def " _generator/tools/check_zahod.py\` → $DEFOV.
2. \`python3 _generator/tools/git_zona.py check --zone _generator/\` → ✅.

## 3. ВЕРИФИКАТОР
Свежий субагент проверяет результат.

## ПЛАН — (заполняет исполнитель)

## ВОПРОСЫ — (заполняет исполнитель)

## ОТЧЁТ — (заполняет исполнитель)

## УРОКИ ФАБРИКЕ — (заполняет исполнитель; пусто — нормальный исход)
MD
}

echo "── ловушка 1: 🔴 ПОЛОЖИТЕЛЬНЫЙ КОНТРОЛЬ НА ЖИВОМ МАТЕРИАЛЕ — rc=0, ни одного ❌"
sobrat_zdorovyj "$T/kod_zdorovyj.md"
OUT1=$(python3 "$P" "$T/kod_zdorovyj.md" 2>&1) || {
  echo "❌ ЛОВУШКА 1: заход, все утверждения которого ИСТИННЫ про живой репозиторий, дал красное."
  echo "   Это и есть излишняя строгость, от которой гейт отключают. Вывод:"
  echo "$OUT1"; exit 1; }
echo "$OUT1" | grep -q "❌" && {
  echo "❌ ЛОВУШКА 1: rc=0, но в выводе есть ❌ — вердикт и код возврата разошлись:"
  echo "$OUT1"; exit 1; }
echo "  ✅ ловушка 1: истинный заход — rc=0, красных нет"

echo "── ловушка 2: 🔴 ПОЛОЖИТЕЛЬНЫЙ КОНТРОЛЬ НА ЖИВОМ ЗАХОДЕ — работает, не падает, объявляет охват"
# 🔴 Живой заход ВЫБИРАЕТСЯ ЗАМЕРОМ, а не вписан именем: фикстура гоняется и из
# worktree, где файл-заход текущей работы лежит в ОСНОВНОЙ папке и потому не
# виден вовсе (контракт зоны: сам `.md` не коммитится). Имя, вписанное рукой,
# уронило бы фикстуру на ровном месте — поймано первым её прогоном.
LIVE=$(ls "$REPO_ROOT"/_studio/zhurnal/*/kod_*.md 2>/dev/null | head -1)
[ -n "$LIVE" ] && [ -f "$LIVE" ] || {
  echo "❌ ЛОВУШКА 2: ни одного живого kod_*.md не найдено под $REPO_ROOT/_studio/zhurnal/"; exit 1; }
echo "  (живой заход для контроля: ${LIVE#$REPO_ROOT/})"
if OUT2=$(python3 "$P" "$LIVE" 2>&1); then RC2=0; else RC2=$?; fi
[ "$RC2" -le 1 ] || {
  echo "❌ ЛОВУШКА 2: гейт УПАЛ на живом заходе (rc=$RC2), а не вынес вердикт:"
  echo "$OUT2"; exit 1; }
echo "$OUT2" | grep -q "Traceback" && {
  echo "❌ ЛОВУШКА 2: трейсбек на живом заходе:"; echo "$OUT2"; exit 1; }
echo "$OUT2" | grep -q "СЛЕПЫЕ ЗОНЫ И ОХВАТ" || {
  echo "❌ ЛОВУШКА 2: блок слепых зон НЕ напечатан — зелёному без объявленных границ верят:"
  echo "$OUT2"; exit 1; }
echo "$OUT2" | grep -q "ВЫПОЛНЕНО:" || {
  echo "❌ ЛОВУШКА 2: охват прогона не назван числом:"; echo "$OUT2"; exit 1; }
echo "  ✅ ловушка 2: живой заход отработан (rc=$RC2), слепые зоны и охват напечатаны"

echo "── ловушка 3: С1 (урок 41) — ветка объявлена стоящей, её нет"
sobrat_zdorovyj "$T/kod_s1.md"
python3 - "$T/kod_s1.md" "$VETKA" <<'PY'
import sys
p, vetka = sys.argv[1], sys.argv[2]
t = open(p, encoding='utf-8').read()
staro = '`git rev-parse --abbrev-ref HEAD` обязано быть `%s`' % vetka
assert t.count(staro) == 1, 'якорь ветки разъехался с фикстурой'
t = t.replace(staro, 'ветка `zahod/net-takoj-vetki-nikogda-ne-bylo` уже стоит, '
                     'проверить: `git rev-parse --abbrev-ref HEAD`')
open(p, 'w', encoding='utf-8').write(t)
PY
krasnet "ветка объявлена стоящей, а её нет" "С1" "$T/kod_s1.md"

echo "── ловушка 4: С1 положительная — ветки нет, но заход её САМ заводит"
sobrat_zdorovyj "$T/kod_s1b.md"
python3 - "$T/kod_s1b.md" "$VETKA" <<'PY'
import sys
p, vetka = sys.argv[1], sys.argv[2]
t = open(p, encoding='utf-8').read()
staro = '`git rev-parse --abbrev-ref HEAD` обязано быть `%s`' % vetka
t = t.replace(staro, 'заводишь сам: `python3 _generator/tools/git_zona.py worktree '
                     'add proba --branch zahod/net-takoj-vetki-nikogda-ne-bylo`')
open(p, 'w', encoding='utf-8').write(t)
PY
molchit "ветку заводит сам заход" "С1" "$T/kod_s1b.md"

echo "── ловушка 5: С2 (урок 30) — зона в чужом репозитории, репозиторий не назван"
sobrat_zdorovyj "$T/kod_s2.md"
python3 - "$T/kod_s2.md" <<'PY'
import sys
p = sys.argv[1]
t = open(p, encoding='utf-8').read()
staro = '- **ЗОНА (можно менять):** `_generator/tools/proba-zony.py`. Всё вне — READ-ONLY.'
assert t.count(staro) == 1, 'якорь зоны разъехался с фикстурой'
t = t.replace(staro, '- **ЗОНА (можно менять):** `disciplina/arhiv-skillov/proba.md`. '
                     'Всё вне — READ-ONLY.')
open(p, 'w', encoding='utf-8').write(t)
PY
krasnet "зона указывает в чужой репозиторий" "С2" "$T/kod_s2.md"

echo "── ловушка 6: С3a (урок 45) — путь-якорь не существует"
sobrat_zdorovyj "$T/kod_s3a.md"
python3 - "$T/kod_s3a.md" <<'PY'
import sys
p = sys.argv[1]
t = open(p, encoding='utf-8').read()
staro = '  2. `_generator/tools/priyomka.py` — приёмка отчёта.'
assert t.count(staro) == 1, 'якорь §0 разъехался с фикстурой'
t = t.replace(staro, '  2. `_generator/tools/net-takogo-yakorya.py` — счётчик покрытия.')
open(p, 'w', encoding='utf-8').write(t)
PY
krasnet "якорь §0 не существует на диске" "С3" "$T/kod_s3a.md"

echo "── ловушка 7: С3b (уроки 45, 27) — якорь есть на диске, но НЕ на ветке исполнителя"
if [ -z "$VETKA_BEZ" ]; then
  echo "  ⚠ ловушка 7 ПРОПУЩЕНА: не нашлось ветки без \`check_sborki.py\` — проверить нечем."
  echo "     Это объявленная слепая зона прогона, а не зелёное."
else
  sobrat_zdorovyj "$T/kod_s3b.md"
  python3 - "$T/kod_s3b.md" "$VETKA" "$VETKA_BEZ" <<'PY'
import sys
p, vetka, bez = sys.argv[1], sys.argv[2], sys.argv[3]
t = open(p, encoding='utf-8').read()
staro = '- **МЕСТО РАБОТЫ:** worktree захода; `git rev-parse --abbrev-ref HEAD` обязано быть `%s`.' % vetka
assert t.count(staro) == 1, 'якорь места работы разъехался с фикстурой'
t = t.replace(staro, '- **МЕСТО РАБОТЫ:** `python3 _generator/tools/git_zona.py worktree '
                     'add proba --branch %s`.' % bez)
staro2 = '  2. `_generator/tools/priyomka.py` — приёмка отчёта.'
t = t.replace(staro2, '  2. `_generator/tools/check_sborki.py` — гейт сборки.')
open(p, 'w', encoding='utf-8').write(t)
PY
  krasnet "якорь не виден с ветки, куда послан исполнитель" "С3" "$T/kod_s3b.md"
fi

echo "── ловушка 8: С4 (урок 42) — команда критерия даёт не то число"
sobrat_zdorovyj "$T/kod_s4.md"
python3 - "$T/kod_s4.md" "$DEFOV" <<'PY'
import sys
p, defov = sys.argv[1], int(sys.argv[2])
t = open(p, encoding='utf-8').read()
staro = '→ %d.' % defov
assert t.count(staro) == 1, 'якорь числа разъехался с фикстурой'
t = t.replace(staro, '→ %d.' % (defov * 4))   # ровно форма урока 42: вчетверо больше
open(p, 'w', encoding='utf-8').write(t)
PY
OUT8=$(python3 "$P" "$T/kod_s4.md" 2>&1) && {
  echo "❌ ЛОВУШКА 8: гейт принял критерий, чья команда даёт другое число:"; echo "$OUT8"; exit 1; }
echo "$OUT8" | grep -q "❌ С4" || {
  echo "❌ ЛОВУШКА 8: красное есть, но не от С4:"; echo "$OUT8"; exit 1; }
echo "$OUT8" | grep -q "даёт $DEFOV" || {
  echo "❌ ЛОВУШКА 8: С4 покраснел, но НЕ НАЗВАЛ живое число $DEFOV — а без обоих чисел"
  echo "   сообщение бесполезно, составитель не поймёт, что чинить:"; echo "$OUT8"; exit 1; }
echo "  ✅ ловушка 8: С4 покраснел и назвал оба числа"

echo "── ловушка 9: С4 положительная — число совпало, обязана молчать"
molchit "число критерия совпало с прогоном" "С4" "$T/kod_zdorovyj.md"

echo "── ловушка 10: С4 (урок 45) — команда критерия падает"
sobrat_zdorovyj "$T/kod_s4b.md"
cat > "$T/padayushchij.py" <<'PY'
raise AttributeError("module has no attribute classify_06tekst")
PY
cp "$T/padayushchij.py" "$TOOLS/proba-padayushchij-vremennyj.py"
python3 - "$T/kod_s4b.md" <<'PY'
import sys
p = sys.argv[1]
t = open(p, encoding='utf-8').read()
staro = '2. `python3 _generator/tools/git_zona.py check --zone _generator/` → ✅.'
assert t.count(staro) == 1, 'якорь второго условия разъехался с фикстурой'
t = t.replace(staro, '2. `python3 _generator/tools/proba-padayushchij-vremennyj.py --help` → справка.')
open(p, 'w', encoding='utf-8').write(t)
PY
OUT10=$(python3 "$P" "$T/kod_s4b.md" 2>&1) && RC10=0 || RC10=$?
rm -f "$TOOLS/proba-padayushchij-vremennyj.py"
[ "$RC10" -ne 0 ] || {
  echo "❌ ЛОВУШКА 10: гейт принял критерий, чья команда падает:"; echo "$OUT10"; exit 1; }
echo "$OUT10" | grep -q "❌ С4" || {
  echo "❌ ЛОВУШКА 10: красное есть, но не от С4:"; echo "$OUT10"; exit 1; }
echo "  ✅ ловушка 10: С4 покраснел на падающей команде критерия"

echo "── ловушка 11: С5 (урок 47) — подкоманда зовётся позиционно, живой CLI её так не берёт"
sobrat_zdorovyj "$T/kod_s5.md"
python3 - "$T/kod_s5.md" <<'PY'
import sys
p = sys.argv[1]
t = open(p, encoding='utf-8').read()
staro = '2. `python3 _generator/tools/git_zona.py check --zone _generator/` → ✅.'
assert t.count(staro) == 1, 'якорь второго условия разъехался с фикстурой'
t = t.replace(staro, '2. `python3 _generator/tools/git_zona.py zakryt-vetku zahod/proba` — ветка закрыта.')
open(p, 'w', encoding='utf-8').write(t)
PY
krasnet "заход зовёт подкоманду по устаревшему синтаксису" "С5" "$T/kod_s5.md"

echo "── ловушка 12: С5 — подкоманды не существует вовсе"
sobrat_zdorovyj "$T/kod_s5b.md"
python3 - "$T/kod_s5b.md" <<'PY'
import sys
p = sys.argv[1]
t = open(p, encoding='utf-8').read()
staro = '2. `python3 _generator/tools/git_zona.py check --zone _generator/` → ✅.'
t = t.replace(staro, '2. `python3 _generator/tools/git_zona.py razmagnitit --zone _generator/` → ✅.')
open(p, 'w', encoding='utf-8').write(t)
PY
krasnet "подкоманды у инструмента нет" "С5" "$T/kod_s5b.md"

echo "── ловушка 13: С6 (урок 33) — «не существует» без команды рядом"
sobrat_zdorovyj "$T/kod_s6.md"
python3 - "$T/kod_s6.md" <<'PY'
import sys
p = sys.argv[1]
t = open(p, encoding='utf-8').read()
staro = ('Файла `_generator/tools/net-takogo-fajla.py` не существует, проверено: '
         '`test -e _generator/tools/net-takogo-fajla.py`.')
assert t.count(staro) == 1, 'якорь утверждения разъехался с фикстурой'
t = t.replace(staro, 'Такого инструмента не существует, знание о нём не живёт нигде.')
open(p, 'w', encoding='utf-8').write(t)
PY
krasnet "утверждение «этого нет» написано по памяти" "С6" "$T/kod_s6.md"

echo "── ловушка 14: С6 положительная — то же утверждение С КОМАНДОЙ рядом, обязана молчать"
molchit "утверждение «этого нет» подтверждено командой" "С6" "$T/kod_zdorovyj.md"

echo "── ловушка 15: С7 — ветка к влитию трогает пути вне названной зоны слияния"
if [ -z "$VETKA_VLIT" ]; then
  echo "  ⚠ ловушка 15 ПРОПУЩЕНА: невлитых веток нет — сверять нечего."
  echo "     Это объявленная слепая зона прогона, а не зелёное."
else
  sobrat_zdorovyj "$T/kod_s7.md"
  python3 - "$T/kod_s7.md" "$VETKA_VLIT" <<'PY'
import sys
p, vetka = sys.argv[1], sys.argv[2]
t = open(p, encoding='utf-8').read()
staro = '## 2. ЗАДАЧА'
assert t.count(staro) == 1, 'якорь задачи разъехался с фикстурой'
t = t.replace(staro, '## 0.1 ВЛИТИЕ\nВлей ветку `%s` зоной '
                     '`--zone _generator/tools/net-takoj-zony/`.\n\n## 2. ЗАДАЧА' % vetka)
open(p, 'w', encoding='utf-8').write(t)
PY
  krasnet "ветка к влитию шире названной зоны слияния" "С7" "$T/kod_s7.md"
fi

echo "── ловушка 16: 🔴 ГЛАВНАЯ — необратимое из чужого текста НЕ ВЫПОЛНЕНО, доказано диском"
MISHEN_SNARUZHI="$T/mishen-snaruzhi.txt"
echo "цела" > "$MISHEN_SNARUZHI"
echo "цела" > "$MISHEN_VNUTRI"
VETKA_DO=$(cd "$REPO_ROOT" && git --no-optional-locks rev-parse --abbrev-ref HEAD)
sobrat_zdorovyj "$T/kod_opasnyj.md"
MV="$MISHEN_VNUTRI" MS="$MISHEN_SNARUZHI" python3 - "$T/kod_opasnyj.md" <<'PY'
import os, sys
p = sys.argv[1]
vnutri = os.path.relpath(os.environ['MV'], os.environ.get('REPO_ROOT', '.'))
t = open(p, encoding='utf-8').read()
staro = '2. `python3 _generator/tools/git_zona.py check --zone _generator/` → ✅.'
assert t.count(staro) == 1, 'якорь второго условия разъехался с фикстурой'
opasnoe = '\n'.join([
    '2. `rm -rf _generator/tools/fixtures/sborka/MISHEN-vremennaya.txt` — убрать мишень.',
    '3. `rm -f %s` — и наружную тоже.' % os.environ['MS'],
    '4. `git push --force origin HEAD` — выложить.',
    '5. `git checkout main` — вернуться на главную ветку.',
    '6. `echo сломано > _generator/tools/fixtures/sborka/MISHEN-vremennaya.txt` — переписать.',
])
t = t.replace(staro, opasnoe)
open(p, 'w', encoding='utf-8').write(t)
PY
OUT16=$(python3 "$P" "$T/kod_opasnyj.md" 2>&1) || true
# (a) гейт обязан НАЗВАТЬ каждую опасную команду непроверенной, а не проглотить
for OPASNAYA in "rm -rf" "rm -f" "git push" "git checkout" "echo"; do
  echo "$OUT16" | grep -q -- "$OPASNAYA" || {
    echo "❌ ЛОВУШКА 16: команда \`$OPASNAYA\` не названа в выводе — гейт молчит про то,"
    echo "   чего не проверил. Молчаливый пропуск и есть цена урока 42. Вывод:"
    echo "$OUT16"; exit 1; }
done
echo "$OUT16" | grep -q "НЕ ВЫПОЛНЕНО" || {
  echo "❌ ЛОВУШКА 16: блок «НЕ ВЫПОЛНЕНО» отсутствует:"; echo "$OUT16"; exit 1; }
# (b) 🔴 ДОКАЗАТЕЛЬСТВО ФАКТОМ НА ДИСКЕ, а не утверждением гейта о себе
[ -f "$MISHEN_VNUTRI" ] || {
  echo "❌ ЛОВУШКА 16: мишень ВНУТРИ репозитория УДАЛЕНА — гейт выполнил \`rm\` из чужого текста."
  echo "   Это тот случай, ради которого гейт снимают целиком."; exit 1; }
[ "$(cat "$MISHEN_VNUTRI")" = "цела" ] || {
  echo "❌ ЛОВУШКА 16: мишень внутри репозитория ПЕРЕЗАПИСАНА — гейт исполнил перенаправление."; exit 1; }
[ -f "$MISHEN_SNARUZHI" ] || {
  echo "❌ ЛОВУШКА 16: мишень СНАРУЖИ репозитория удалена — гейт вышел за его границы."; exit 1; }
VETKA_POSLE=$(cd "$REPO_ROOT" && git --no-optional-locks rev-parse --abbrev-ref HEAD)
[ "$VETKA_DO" = "$VETKA_POSLE" ] || {
  echo "❌ ЛОВУШКА 16: ВЕТКА СМЕНИЛАСЬ ($VETKA_DO → $VETKA_POSLE) — гейт выполнил \`git checkout\`"
  echo "   и подменил файлы под ногами у соседних заходов."; exit 1; }
echo "  ✅ ловушка 16: пять опасных команд названы непроверенными; обе мишени целы, ветка = $VETKA_POSLE"

echo "── ловушка 17: белый список — обещание докстринга сходится с таблицей"
python3 - "$TOOLS" <<'PY'
import sys, importlib.util, re, pathlib
tools = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("cs", tools / "check_sborki.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)          # `assert` внутри модуля упадёт при расхождении
obeshchano = re.search(r'БЕЛЫЙ СПИСОК ИЗ (\d+) ВХОД', m.__doc__)
assert obeshchano, 'докстринг не называет число входов белого списка'
n = int(obeshchano.group(1))
assert n == len(m.BELYJ_SPISOK), f'докстринг обещает {n}, в таблице {len(m.BELYJ_SPISOK)}'
print(f"  ✅ ловушка 17: белый список — {n} вход(ов), докстринг и таблица сходятся")
PY

echo "── ловушка 18: 🔴 РЕГРЕССИЯ (верификатор §3, дыра 1) — приклеенное значение опции"
# Короткая опция с ПРИКЛЕЕННЫМ путём (`-cf/путь`) начинается с `-` и `=` не
# содержит: раньше путь не проверялся вовсе, и гейт читал файл ВНЕ репозитория.
echo "образец" > "$T/vneshnij.txt"
sobrat_zdorovyj "$T/kod_prikleen.md"
VN="$T/vneshnij.txt" python3 - "$T/kod_prikleen.md" <<'PY'
import os, sys
p = sys.argv[1]
t = open(p, encoding='utf-8').read()
staro = '2. `python3 _generator/tools/git_zona.py check --zone _generator/` → ✅.'
assert t.count(staro) == 1, 'якорь второго условия разъехался с фикстурой'
t = t.replace(staro, '2. `grep -cf%s CLAUDE.md` → 1.\n'
                     '3. `git log -O%s --oneline -1` → готово.'
                     % (os.environ['VN'], os.environ['VN']))
open(p, 'w', encoding='utf-8').write(t)
PY
OUT18=$(python3 "$P" "$T/kod_prikleen.md" 2>&1) || true
echo "$OUT18" | grep -q "выводит за пределы репозитория" || {
  echo "❌ ЛОВУШКА 18: приклеенный путь наружу НЕ отклонён — гейт читает чужие файлы:"
  echo "$OUT18"; exit 1; }
echo "$OUT18" | grep -q -- "-O.*запрещён" || {
  echo "❌ ЛОВУШКА 18: git-ордерфайл \`-O\` НЕ отклонён:"; echo "$OUT18"; exit 1; }
echo "  ✅ ловушка 18: приклеенный путь наружу и \`git -O\` отклонены"

echo "── ловушка 19: 🔴 РЕГРЕССИЯ (верификатор §3, дыра 2) — катастрофический бэктрекинг"
# 3 КБ обычной прозы вешали разбор НАСМЕРТЬ, и таймаут команды тут не помогал:
# висел не подпроцесс, а regex. Сторожим ВРЕМЕНЕМ, а не выводом.
python3 - "$T/kod_backtrack.md" <<'PY'
import sys
open(sys.argv[1], 'w', encoding='utf-8').write(
    '# Проба\n\n## 2. ЗАДАЧА\nx.py ' + 'a' * 20000 +
    '\n\nПроза: ' + 'b' * 3000 + '\n\n## ПЛАН\n')
PY
python3 - "$P" "$T/kod_backtrack.md" <<'PY'
import subprocess, sys, time
t = time.monotonic()
try:
    subprocess.run(["python3", sys.argv[1], sys.argv[2]],
                   capture_output=True, text=True, timeout=60)
except subprocess.TimeoutExpired:
    print("❌ ЛОВУШКА 19: разбор не завершился за 60 с — бэктрекинг вернулся"); sys.exit(1)
d = time.monotonic() - t
if d > 15:
    print(f"❌ ЛОВУШКА 19: разбор занял {d:.1f} с на 23 КБ прозы — это уже висящий гейт")
    sys.exit(1)
print(f"  ✅ ловушка 19: 23 КБ прозы разобраны за {d:.2f} с")
PY

echo "── ловушка 20: 🔴 РЕГРЕССИЯ (верификатор §3) — ветка без префикса \`zahod/\`"
sobrat_zdorovyj "$T/kod_vetka-bez-prefiksa.md"
python3 - "$T/kod_vetka-bez-prefiksa.md" "$VETKA" <<'PY'
import sys
p, vetka = sys.argv[1], sys.argv[2]
t = open(p, encoding='utf-8').read()
staro = '`git rev-parse --abbrev-ref HEAD` обязано быть `%s`' % vetka
t = t.replace(staro, 'ветка `net-takoj-vetki-bez-prefiksa` уже стоит и уже принята')
open(p, 'w', encoding='utf-8').write(t)
PY
krasnet "ветка названа прозой без префикса zahod/" "С1" "$T/kod_vetka-bez-prefiksa.md"

echo "── ловушка 21: 🔴 РЕГРЕССИЯ (верификатор §3) — число критерия без стрелки"
sobrat_zdorovyj "$T/kod_chislo-bez-strelki.md"
python3 - "$T/kod_chislo-bez-strelki.md" "$DEFOV" <<'PY'
import sys
p, defov = sys.argv[1], int(sys.argv[2])
t = open(p, encoding='utf-8').read()
staro = '→ %d.' % defov
assert t.count(staro) == 1, 'якорь числа разъехался с фикстурой'
t = t.replace(staro, 'обязана вернуть %d.' % (defov * 3))
open(p, 'w', encoding='utf-8').write(t)
PY
krasnet "число критерия обещано без стрелки" "С4" "$T/kod_chislo-bez-strelki.md"

echo "── ловушка 22: 🔴 РЕГРЕССИЯ (верификатор §3) — значение позиционного выбора"
sobrat_zdorovyj "$T/kod_vybor.md"
python3 - "$T/kod_vybor.md" <<'PY'
import sys
p = sys.argv[1]
t = open(p, encoding='utf-8').read()
staro = '2. `python3 _generator/tools/git_zona.py check --zone _generator/` → ✅.'
t = t.replace(staro, '2. `python3 _generator/tools/git_zona.py worktree create proba` — папка развёрнута.')
open(p, 'w', encoding='utf-8').write(t)
PY
krasnet "значение позиционного выбора вне {add,drop,list}" "С5" "$T/kod_vybor.md"

echo "── ловушка 23: 🔴 РЕГРЕССИЯ (верификатор §3) — GIT_ZONA_REPO упомянута ОТРИЦАНИЕМ"
sobrat_zdorovyj "$T/kod_zona-repo.md"
python3 - "$T/kod_zona-repo.md" <<'PY'
import sys
p = sys.argv[1]
t = open(p, encoding='utf-8').read()
staro = '- **ЗОНА (можно менять):** `_generator/tools/proba-zony.py`. Всё вне — READ-ONLY.'
t = t.replace(staro, '- **ЗОНА (можно менять):** `disciplina/doma/proba.md`. Переменную '
                     'GIT_ZONA_REPO выставлять не надо. Всё вне — READ-ONLY.')
open(p, 'w', encoding='utf-8').write(t)
PY
krasnet "GIT_ZONA_REPO названа отрицанием, а не присвоением" "С2" "$T/kod_zona-repo.md"

echo "── ловушка 24: 🔴 РЕГРЕССИЯ (верификатор §3) — якоря оформлены код-блоком"
sobrat_zdorovyj "$T/kod_yakor-v-fense.md"
python3 - "$T/kod_yakor-v-fense.md" <<'PY'
import sys
p = sys.argv[1]
t = open(p, encoding='utf-8').read()
staro = ('  1. `_generator/tools/check_zahod.py` — лексический сосед.\n'
         '  2. `_generator/tools/priyomka.py` — приёмка отчёта.')
assert t.count(staro) == 1, 'якорный список разъехался с фикстурой'
t = t.replace(staro, '```\n_generator/tools/check_zahod.py — лексический сосед\n'
                     '_studio/docs/kak-delat/NET-TAKOGO-KANONA.md — канон, читай первым\n```')
open(p, 'w', encoding='utf-8').write(t)
PY
krasnet "якорь в код-блоке не существует" "С3" "$T/kod_yakor-v-fense.md"

echo "── ловушка 25: 🔴 TOOL-CONTRACT — postroit_kartochku.py/sravnit.py на кривом входе падают ГРОМКО"
OBP="$TOOLS/fixtures/sborka/obratnyj-progon"
OUT25A=$(python3 "$OBP/postroit_kartochku.py" net-takoj-deki net-takoj-slaid 2>&1) && {
  echo "❌ ЛОВУШКА 25: postroit_kartochku.py на несуществующем деке/слайде вернул rc=0 — молча"
  echo "   сделал не то, вместо громкого отказа:"; echo "$OUT25A"; exit 1; }
echo "$OUT25A" | grep -qi "нет\|no such file\|traceback" || {
  echo "❌ ЛОВУШКА 25: postroit_kartochku.py упал, но без понятного сообщения о причине:"
  echo "$OUT25A"; exit 1; }
echo "  ✅ ловушка 25а: postroit_kartochku.py — кривой вход упал громко (rc≠0, сообщение по делу)"
OUT25B=$(python3 "$OBP/sravnit.py" net-takoj-deki net-takoj-slaid 2>&1) && {
  echo "❌ ЛОВУШКА 25: sravnit.py на несуществующем деке/слайде вернул rc=0:"; echo "$OUT25B"; exit 1; }
echo "$OUT25B" | grep -qi "нет\|no such file\|traceback" || {
  echo "❌ ЛОВУШКА 25: sravnit.py упал, но без понятного сообщения о причине:"; echo "$OUT25B"; exit 1; }
echo "  ✅ ловушка 25б: sravnit.py — кривой вход упал громко (rc≠0, сообщение по делу)"

echo "── ловушка 26: 🔴 TOOL-CONTRACT (заход dovodka-solvera) — progon_baza.py на кривом входе падает ГРОМКО"
OUT26A=$(python3 "$OBP/progon_baza.py" 2>&1) && {
  echo "❌ ЛОВУШКА 26: progon_baza.py без обязательного --baza вернул rc=0 — молча:"
  echo "$OUT26A"; exit 1; }
echo "$OUT26A" | grep -q "required: --baza" || {
  echo "❌ ЛОВУШКА 26: progon_baza.py упал, но без понятного сообщения о причине:"
  echo "$OUT26A"; exit 1; }
echo "  ✅ ловушка 26а: progon_baza.py — без --baza падает громко (rc≠0, сообщение по делу)"
OUT26B=$(python3 "$OBP/progon_baza.py" --baza 99 2>&1) && {
  echo "❌ ЛОВУШКА 26: progon_baza.py с --baza 99 (не из choices) вернул rc=0:"
  echo "$OUT26B"; exit 1; }
echo "$OUT26B" | grep -q "invalid choice" || {
  echo "❌ ЛОВУШКА 26: progon_baza.py упал, но без понятного сообщения о причине:"
  echo "$OUT26B"; exit 1; }
echo "  ✅ ловушка 26б: progon_baza.py — мусор в --baza падает громко (rc≠0, сообщение по делу)"

echo "ФИКСТУРЫ ЗЕЛЁНЫЕ"
