#!/bin/sh
# TOOL-CONTRACT-COVERS: check_sborki.py postroit_kartochku.py sravnit.py progon_baza.py koridor_obyoma.py bootstrap_lekcii.py gejt_kartochki.py deck.py smeta.py zamer_smety.py gejt_vmeshcheniya.py
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
#  42. 🔴 (заход `nositel`, 13.08.2026) секция-носитель («## СТАРТОВОЕ
#      СООБЩЕНИЕ ВЛАДЕЛЬЦУ») НЕ ловится С5 ни в однострочной (проблемной), ни
#      в переформатированной вёрстке — обе обязаны молчать одинаково.
#      🔴 Число ловушек в этой шапке (пункты 25-41) отстало от тела файла ДО
#      этой правки (найдено верификатором живого прогона, не мной заведено) —
#      не чиню чужой долг вне своей зоны, называю пунктом очереди в `## ВОПРОСЫ`.
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
# 🔴 Раздел «## 4.1 ГИГИЕНА» добавлен в эталон 2026-08-09 вместе с гейтом С8, и это
# не подгонка эталона под гейт. Положительный контроль обязан моделировать
# ЗДОРОВЫЙ заход в СЕГОДНЯШНЕМ смысле слова: раздел вшит в `bootstrap_zahod.py` и
# рождается сам, значит заход без него — это заход, написанный руками, а руками
# их писать запрещено (`CLAUDE.md`: «заход НИКОГДА не пишется с нуля»). Эталон,
# застывший на вчерашнем определении здоровья, превратил бы ловушку 1 из защиты
# от излишней строгости в запрет заводить новые структурные проверки вообще.
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

## 4.1 🔴 ГИГИЕНА — ПРОВЕРКИ ПЕРЕД СДАЧЕЙ
**ЗОНА ГИГИЕНЫ:** \`_generator/tools/proba-zony.py\`

- **Г1.** \`python3 _generator/tools/git_zona.py check --zone _generator/tools/proba-zony.py\` → ✅
- **Г6.** \`git --no-optional-locks show --stat\` — только свои пути

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

echo "── ловушка 27: 🔴 TOOL-CONTRACT (заход dovodka-solvera, Часть Б) — koridor_obyoma.py на кривом входе падает ГРОМКО"
OUT27A=$(python3 "$OBP/koridor_obyoma.py" 2>&1) && {
  echo "❌ ЛОВУШКА 27: koridor_obyoma.py без обязательных флагов вернул rc=0 — молча:"
  echo "$OUT27A"; exit 1; }
echo "$OUT27A" | grep -q "required: --axis, --liniya, --sostav" || {
  echo "❌ ЛОВУШКА 27: koridor_obyoma.py упал, но без понятного сообщения о причине:"
  echo "$OUT27A"; exit 1; }
echo "  ✅ ловушка 27а: koridor_obyoma.py — без флагов падает громко (rc≠0, сообщение по делу)"
OUT27B=$(python3 "$OBP/koridor_obyoma.py" --axis diagonal --liniya 50 --sostav p 2>&1) && {
  echo "❌ ЛОВУШКА 27: koridor_obyoma.py с --axis diagonal (не из choices) вернул rc=0:"
  echo "$OUT27B"; exit 1; }
echo "$OUT27B" | grep -q "invalid choice" || {
  echo "❌ ЛОВУШКА 27: koridor_obyoma.py упал, но без понятного сообщения о причине:"
  echo "$OUT27B"; exit 1; }
echo "  ✅ ловушка 27б: koridor_obyoma.py — мусор в --axis падает громко (rc≠0, сообщение по делу)"
OUT27C=$(python3 "$OBP/koridor_obyoma.py" --axis horizontal --liniya 50 --sostav xyz 2>&1) && {
  echo "❌ ЛОВУШКА 27: koridor_obyoma.py с нераспознанным токеном --sostav вернул rc=0:"
  echo "$OUT27C"; exit 1; }
echo "$OUT27C" | grep -qi "токен состава не распознан\|traceback" || {
  echo "❌ ЛОВУШКА 27: koridor_obyoma.py упал, но без понятного сообщения о причине:"
  echo "$OUT27C"; exit 1; }
echo "  ✅ ловушка 27в: koridor_obyoma.py — мусор в --sostav падает громко (rc≠0, сообщение по делу)"

echo "── ловушка 28: 🔴 Р1 (заход porcia-1-zamknut-konvejer) — своя карточка зелёная для своего гейта"
SBORKA="$REPO_ROOT/_generator/sborka"
ZAP_VALS_PY='
import sys
from pathlib import Path
lek = Path(sys.argv[1])
sids = sys.argv[2:]
vals = {
    "nazvanie: заполнить": "nazvanie: X", "zagolovok_na_ekrane: заполнить": "zagolovok_na_ekrane: X",
    "zachem: заполнить": "zachem: X", "akcent: заполнить": "akcent: X",
    "kommentarij_lektoru: заполнить": "kommentarij_lektoru: X", "minuty: заполнить": "minuty: 1",
    "vazhnost: заполнить": "vazhnost: opornyj", "byudzhet_slov: заполнить": "byudzhet_slov: 10",
    "tip_verstki: заполнить": "tip_verstki: tolko_tekst", "liniya: заполнить": "liniya: 50",
    # решения ФАЗЫ 1 (заход format-kartochki-faza-1, поле переименовано заходом
    # tipologia-odna-os): тип слайда из закрытого списка (Т4 — единственный блок
    # [narrativ] «завязка» ниже структурно ложится в его раскладку без правок)
    # и центральный блок, чья мысль обязана резолвиться в блок «Математики».
    # Мысль «завязка» ставят те же ловушки ниже, когда пишут настоящее тело.
    "tip_slaida: заполнить": "tip_slaida: Т4",
    "centralnyj_blok: заполнить": "centralnyj_blok: завязка",
}
for sid in sids:
    p = lek / "slajdy" / sid / "slaid.md"
    t = p.read_text(encoding="utf-8")
    for old, new in vals.items():
        t = t.replace(old, new)
    p.write_text(t, encoding="utf-8")
'
L28="$T/lek28"
python3 "$SBORKA/bootstrap_lekcii.py" "$L28" >/dev/null
python3 - "$L28" <<'PY'
import sys
p = sys.argv[1] + "/brief.md"
t = open(p, encoding="utf-8").read()
t = t.replace("slide_order:\n", "slide_order:\n  - s01\n  - s02\n")
open(p, "w", encoding="utf-8").write(t)
PY
python3 "$SBORKA/bootstrap_lekcii.py" "$L28" >/dev/null
python3 -c "$ZAP_VALS_PY" "$L28" s01 s02
# 🔴 дочистка приёмки (тот же заход): шапки мало — тело-заглушка полный гейт теперь
# красит (ловушка 32), поэтому «зелёная своя карточка» проверяется на ПОЛНОСТЬЮ
# заполненной (шапка + настоящее тело), не только на шапке.
python3 - "$L28" <<'PY'
import sys
from pathlib import Path
lek = Path(sys.argv[1])
for sid in ("s01", "s02"):
    p = lek / "slajdy" / sid / "slaid.md"
    t = p.read_text(encoding="utf-8")
    t = t.replace(
        "## Математика — развёрнуто\n### [narrativ] заполнить\nзаполнить",
        "## Математика — развёрнуто\n### [narrativ] завязка\nНастоящий развёрнутый текст %s." % sid)
    t = t.replace(
        "## Текст слайда — сжато\n### [narrativ] заполнить\nзаполнить",
        "## Текст слайда — сжато\n### [narrativ] завязка\nНастоящий сжатый текст %s." % sid)
    p.write_text(t, encoding="utf-8")
PY
OUT28=$(python3 "$SBORKA/gejt_kartochki.py" "$L28" 2>&1) || {
  echo "❌ ЛОВУШКА 28: bootstrap_lekcii.py + заполненная шапка и тело не дают зелёный гейт (Р1 регрессия):"
  echo "$OUT28"; exit 1; }
echo "$OUT28" | grep -q "ЗЕЛЁНЫЙ" || {
  echo "❌ ЛОВУШКА 28: rc=0, но текст не «ЗЕЛЁНЫЙ»:"; echo "$OUT28"; exit 1; }
echo "  ✅ ловушка 28: порождённая карточка (шапка и тело заполнены по-настоящему) — гейт зелёный"

echo "── ловушка 29: 🔴 Р (заход format-kartochki-faza-1) — --faza 1 КРАСНЕЕТ на свежепорождённой карточке"
# 🔴 ЛОВУШКА ПЕРЕВЁРНУТА, и это главное содержание захода format-kartochki-faza-1.
# Прежняя редакция сторожила ОБРАТНОЕ — «--faza 1 зелёный на нетронутой карточке» —
# и тем самым закрепляла дефект фикстурой: гейт выхода фазы 1 в спецификации
# (`fazy-1-2-plan.md §3`) требует тип идеи, размеченные блоки и ровно один
# центральный блок, а код на всём этом молчал и отвечал зелёным. Гейт, который не
# может провалиться, — не гейт; ловушка сторожит именно способность провалиться.
L29="$T/lek29"
python3 "$SBORKA/bootstrap_lekcii.py" "$L29" >/dev/null
python3 - "$L29" <<'PY'
import sys
p = sys.argv[1] + "/brief.md"
t = open(p, encoding="utf-8").read()
t = t.replace("slide_order:\n", "slide_order:\n  - s01\n")
open(p, "w", encoding="utf-8").write(t)
PY
python3 "$SBORKA/bootstrap_lekcii.py" "$L29" >/dev/null
OUT29F=$(python3 "$SBORKA/gejt_kartochki.py" --faza 1 "$L29" 2>&1) && {
  echo "❌ ЛОВУШКА 29: --faza 1 на свежепорождённой (нетронутой) карточке ЗЕЛЁНЫЙ — решений фазы 1 нет, а гейт их не требует:"
  echo "$OUT29F"; exit 1; }
for TREB in "tip_slaida" "centralnyj_blok" "незаполненной мыслью"; do
  echo "$OUT29F" | grep -q "$TREB" || {
    echo "❌ ЛОВУШКА 29: --faza 1 покраснел, но не поимённо на «$TREB»:"; echo "$OUT29F"; exit 1; }
done
echo "$OUT29F" | grep -q "проверено 1 из 1" || {
  echo "❌ ЛОВУШКА 29: вердикт без строки охвата «проверено X из Y»:"; echo "$OUT29F"; exit 1; }
echo "$OUT29F" | grep -q "НЕ проверяю:" || {
  echo "❌ ЛОВУШКА 29: вердикт без объявленных слепых зон («НЕ проверяю:»):"; echo "$OUT29F"; exit 1; }
# принимаем решения РОВНО ФАЗЫ 1 и ничего сверх: тип идеи, название, идея одной
# фразой, минуты, центральный блок, разметка блоков БЕЗ тел. Поля вёрстки
# (akcent/vazhnost/tip_verstki/liniya/byudzhet_slov) НЕ трогаем намеренно — иначе
# ловушка проверяла бы не то: --faza 1 обязан зеленеть на этом, а полный гейт —
# краснеть, потому что Ф2 и Ф3 ещё не проходили.
python3 - "$L29" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1]) / "slajdy" / "s01" / "slaid.md"
t = p.read_text(encoding="utf-8")
for old, new in (("nazvanie: заполнить", "nazvanie: Завязка"),
                 ("tip_slaida: заполнить", "tip_slaida: Т1"),
                 ("zachem: заполнить", "zachem: зритель должен увидеть, зачем всё это"),
                 ("minuty: заполнить", "minuty: 6"),
                 ("centralnyj_blok: заполнить", "centralnyj_blok: само понятие"),
                 # Т1 — содержательный тип (не служебный/Т4/Т5), связей не освобождён:
                 # реалистичное решение фазы 1 — назвать хоть что-то вводимое.
                 ("vvodit: []", "vvodit: [само понятие]")):
    t = t.replace(old, new)
for razdel in ("## Математика — развёрнуто", "## Текст слайда — сжато"):
    t = t.replace("%s\n### [narrativ] заполнить\nзаполнить" % razdel,
                  "%s\n### [narrativ] завязка\n\n### [opredelenie] само понятие" % razdel)
p.write_text(t, encoding="utf-8")
PY
OUT29G=$(python3 "$SBORKA/gejt_kartochki.py" --faza 1 "$L29" 2>&1) || {
  echo "❌ ЛОВУШКА 29: план фазы 1 принят целиком (тип слайда, блоки с мыслью, центральный), а --faza 1 всё равно красный:"
  echo "$OUT29G"; exit 1; }
OUT29P=$(python3 "$SBORKA/gejt_kartochki.py" "$L29" 2>&1) && {
  echo "❌ ЛОВУШКА 29: полный гейт на карточке с одним лишь планом фазы 1 дал rc=0 — поля Ф2/Ф3 не проверяются:"
  echo "$OUT29P"; exit 1; }
echo "  ✅ ловушка 29: свежая карточка — --faza 1 красный поимённо (tip_slaida, центральный блок, мысль блока), с охватом и слепыми зонами; принятый план фазы 1 — зелёный, полный гейт всё ещё красный"

echo "── ловушка 30: 🔴 Р3 — солвер встроен в deck.py: явный kegl/liniya переживает сборку"
L30="$T/lek30"
python3 "$SBORKA/bootstrap_lekcii.py" "$L30" >/dev/null
python3 - "$L30" <<'PY'
import sys
p = sys.argv[1] + "/brief.md"
t = open(p, encoding="utf-8").read()
t = t.replace("slide_order:\n", "slide_order:\n  - s01\n")
open(p, "w", encoding="utf-8").write(t)
PY
python3 "$SBORKA/bootstrap_lekcii.py" "$L30" >/dev/null
python3 -c "$ZAP_VALS_PY" "$L30" s01
python3 - "$L30" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1]) / "slajdy" / "s01" / "slaid.md"
lines = p.read_text(encoding="utf-8").split("\n")
out = []
for line in lines:
    out.append(line)
    if line.startswith("liniya:"):
        out.append("kegl_px: 77")  # явное значение — солвер обязан его не тронуть
p.write_text("\n".join(out), encoding="utf-8")
PY
KEGL_DO=$(grep "^kegl_px:" "$L30/slajdy/s01/slaid.md")
if python3 -c "import playwright" >/dev/null 2>&1; then
  OUT30=$(python3 "$SBORKA/deck.py" "$L30" -o "$L30/dist/index.html" 2>&1) || {
    echo "❌ ЛОВУШКА 30: deck.py с playwright в наличии упал:"; echo "$OUT30"; exit 1; }
  [ -f "$L30/dist/index.html" ] || {
    echo "❌ ЛОВУШКА 30: дек не создан на диске:"; echo "$OUT30"; exit 1; }
  KEGL_POSLE=$(grep "^kegl_px:" "$L30/slajdy/s01/slaid.md")
  [ "$KEGL_DO" = "$KEGL_POSLE" ] || {
    echo "❌ ЛОВУШКА 30: явный kegl_px ПЕРЕЗАПИСАН солвером ($KEGL_DO → $KEGL_POSLE):"; exit 1; }
  echo "$OUT30" | grep -q "s01 — пропущен" || {
    echo "❌ ЛОВУШКА 30: deck.py не назвал слайд пропущенным поимённо:"
    echo "$OUT30"; exit 1; }
  echo "$OUT30" | grep -q "verstka_reshena" || {
    echo "❌ ЛОВУШКА 30: пропуск назван, но не сказано, чем закрепить решение автора — а именно"
    echo "   этого не хватало исполнителю, который потом полез искать причину в код:"
    echo "$OUT30"; exit 1; }
  echo "  ✅ ловушка 30: playwright в наличии — явный kegl_px пережил сборку ($KEGL_DO), дек собран"
  # 30б (заход tri-provodki): ТА ЖЕ карточка с флагом --zanovo обязана быть
  # ПЕРЕПОДОБРАНА — иначе размораживать замороженную лекцию нечем вовсе, и
  # «подбор одноразовый» остаётся ровно там, где был.
  OUT30C=$(python3 "$SBORKA/deck.py" "$L30" -o "$L30/dist/index.html" --zanovo 2>&1) || {
    echo "❌ ЛОВУШКА 30б: сборка с --zanovo упала:"; echo "$OUT30C"; exit 1; }
  KEGL_ZANOVO=$(grep "^kegl_px:" "$L30/slajdy/s01/slaid.md")
  [ "$KEGL_DO" != "$KEGL_ZANOVO" ] || {
    echo "❌ ЛОВУШКА 30б: --zanovo НЕ переподобрал ($KEGL_DO остался) — размораживать лекцию нечем:"
    echo "$OUT30C"; exit 1; }
  grep -q "^podbor_avto:" "$L30/slajdy/s01/slaid.md" || {
    echo "❌ ЛОВУШКА 30б: солвер записал значения и НЕ пометил их своей рукой (podbor_avto) —"
    echo "   на следующей сборке они снова станут неотличимы от решения автора"; exit 1; }
  echo "  ✅ ловушка 30б: --zanovo переподобрал ($KEGL_DO → $KEGL_ZANOVO) и пометил запись podbor_avto"
  # 30в: намерение автора сильнее --zanovo — иначе поле-намерение ничего не значит.
  python3 - "$L30" <<'PY30'
import sys
from pathlib import Path
p = Path(sys.argv[1]) / "slajdy" / "s01" / "slaid.md"
t = p.read_text(encoding="utf-8").replace("\nliniya:", "\nverstka_reshena: da\nliniya:", 1)
p.write_text(t, encoding="utf-8")
PY30
  KEGL_DO_V=$(grep "^kegl_px:" "$L30/slajdy/s01/slaid.md")
  OUT30D=$(python3 "$SBORKA/deck.py" "$L30" -o "$L30/dist/index.html" --zanovo 2>&1) || {
    echo "❌ ЛОВУШКА 30в: сборка с --zanovo и намерением автора упала:"; echo "$OUT30D"; exit 1; }
  [ "$KEGL_DO_V" = "$(grep '^kegl_px:' "$L30/slajdy/s01/slaid.md")" ] || {
    echo "❌ ЛОВУШКА 30в: verstka_reshena: da НЕ удержало --zanovo — намерение автора ничего не значит:"
    echo "$OUT30D"; exit 1; }
  echo "  ✅ ловушка 30в: verstka_reshena: da сильнее --zanovo — решение автора неприкосновенно"
else
  OUT30=$(python3 "$SBORKA/deck.py" "$L30" -o "$L30/dist/index.html" 2>&1) && {
    echo "❌ ЛОВУШКА 30: playwright ОТСУТСТВУЕТ, а deck.py (подбор по умолчанию) вернул rc=0 — молча собрал без подбора:"
    echo "$OUT30"; exit 1; }
  echo "$OUT30" | grep -qi "playwright" || {
    echo "❌ ЛОВУШКА 30: отказ без playwright не назвал причину внятно:"; echo "$OUT30"; exit 1; }
  OUT30B=$(python3 "$SBORKA/deck.py" "$L30" -o "$L30/dist/index.html" --bez-podbora 2>&1) || {
    echo "❌ ЛОВУШКА 30: --bez-podbora без playwright всё равно упал:"; echo "$OUT30B"; exit 1; }
  echo "  ✅ ловушка 30: playwright ОТСУТСТВУЕТ — deck.py громко отказал по умолчанию, --bez-podbora собрал"
fi

echo "── ловушка 31: 🔴 Р1б — гейт краснеет, если блок «что дальше» убрать (не украшение)"
L31="$T/lek31"
python3 "$SBORKA/bootstrap_lekcii.py" "$L31" >/dev/null
python3 - "$L31" <<'PY'
import sys
p = sys.argv[1] + "/brief.md"
t = open(p, encoding="utf-8").read()
t = t.replace("slide_order:\n", "slide_order:\n  - s01\n")
open(p, "w", encoding="utf-8").write(t)
PY
python3 "$SBORKA/bootstrap_lekcii.py" "$L31" >/dev/null
python3 -c "$ZAP_VALS_PY" "$L31" s01
python3 - "$L31" <<'PY'
import re, sys
from pathlib import Path
p = Path(sys.argv[1]) / "slajdy" / "s01" / "slaid.md"
t = p.read_text(encoding="utf-8")
t2 = re.sub(r"^<!--.*?-->\s*", "", t, flags=re.S)
assert t2 != t, "блок «что дальше» не найден — ловушке нечего убирать"
p.write_text(t2, encoding="utf-8")
PY
OUT31=$(python3 "$SBORKA/gejt_kartochki.py" "$L31" 2>&1) && {
  echo "❌ ЛОВУШКА 31: карточка без блока «что дальше» прошла гейт зелёным — блок украшение, не дисциплина:"
  echo "$OUT31"; exit 1; }
echo "$OUT31" | grep -q "блок «что дальше».*отсутствует" || {
  echo "❌ ЛОВУШКА 31: гейт покраснел, но не поимённо на отсутствии блока «что дальше»:"
  echo "$OUT31"; exit 1; }
echo "  ✅ ловушка 31: карточка без блока «что дальше» — гейт красный, поимённо"

echo "── ловушка 32: 🔴 МЫСЛЬ блока — выход Ф1, ТЕЛО блока — выход Ф2/Ф3, и оба умеют краснеть"
L32="$T/lek32"
python3 "$SBORKA/bootstrap_lekcii.py" "$L32" >/dev/null
python3 - "$L32" <<'PY'
import sys
p = sys.argv[1] + "/brief.md"
t = open(p, encoding="utf-8").read()
t = t.replace("slide_order:\n", "slide_order:\n  - s01\n")
open(p, "w", encoding="utf-8").write(t)
PY
python3 "$SBORKA/bootstrap_lekcii.py" "$L32" >/dev/null
python3 -c "$ZAP_VALS_PY" "$L32" s01
# 🔴 Заход format-kartochki-faza-1 развёл заглушку на ДВА события разных фаз:
# МЫСЛЬ блока — выход Ф1 (разметка), ТЕЛО блока — выход Ф2/Ф3 (содержание).
# Прежняя редакция ловушки требовала «--faza 1 зелёный на нетронутом теле» и тем
# самым утверждала, что разметка блоков фазы 1 не касается. Касается — это и есть
# её единственный выход.
# шапка настоящая, тело — НЕТРОНУТАЯ заглушка бутстрапа: мысль тоже «заполнить»
OUT32P=$(python3 "$SBORKA/gejt_kartochki.py" "$L32" 2>&1) && {
  echo "❌ ЛОВУШКА 32: полный гейт дал rc=0 на теле-заглушке — ZAPOLNIT в теле не ловится:"
  echo "$OUT32P"; exit 1; }
echo "$OUT32P" | grep -q "незаполненной мыслью" || {
  echo "❌ ЛОВУШКА 32: полный гейт красный, но не поимённо на заглушке мысли блока:"
  echo "$OUT32P"; exit 1; }
OUT32F=$(python3 "$SBORKA/gejt_kartochki.py" --faza 1 "$L32" 2>&1) && {
  echo "❌ ЛОВУШКА 32: --faza 1 на нетронутой заглушке тела ЗЕЛЁНЫЙ — разметка блоков не проверяется:"
  echo "$OUT32F"; exit 1; }
echo "$OUT32F" | grep -q "незаполненной мыслью" || {
  echo "❌ ЛОВУШКА 32: --faza 1 красный, но не поимённо на заглушке мысли блока:"
  echo "$OUT32F"; exit 1; }
# размечаем блоки (мысль есть, тела ещё нет) — Ф1 зеленеет, полный гейт красный
python3 - "$L32" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1]) / "slajdy" / "s01" / "slaid.md"
t = p.read_text(encoding="utf-8")
for razdel in ("## Математика — развёрнуто", "## Текст слайда — сжато"):
    t = t.replace("%s\n### [narrativ] заполнить\nзаполнить" % razdel,
                  "%s\n### [narrativ] завязка\nзаполнить" % razdel)
p.write_text(t, encoding="utf-8")
PY
OUT32F1=$(python3 "$SBORKA/gejt_kartochki.py" --faza 1 "$L32" 2>&1) || {
  echo "❌ ЛОВУШКА 32: блоки размечены (мысль есть), а --faza 1 всё равно красный — Ф1 требует тел, которых на ней не пишут:"
  echo "$OUT32F1"; exit 1; }
OUT32P1=$(python3 "$SBORKA/gejt_kartochki.py" "$L32" 2>&1) && {
  echo "❌ ЛОВУШКА 32: полный гейт дал rc=0 на размеченных, но НЕ НАПИСАННЫХ блоках:"
  echo "$OUT32P1"; exit 1; }
echo "$OUT32P1" | grep -q "ненаписанное тело блока" || {
  echo "❌ ЛОВУШКА 32: полный гейт красный, но не поимённо на незаполненном теле блока:"
  echo "$OUT32P1"; exit 1; }
# заполняем тела настоящим текстом — оба режима обязаны позеленеть
python3 - "$L32" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1]) / "slajdy" / "s01" / "slaid.md"
t = p.read_text(encoding="utf-8")
t = t.replace(
    "## Математика — развёрнуто\n### [narrativ] завязка\nзаполнить",
    "## Математика — развёрнуто\n### [narrativ] завязка\nНастоящий развёрнутый текст.")
t = t.replace(
    "## Текст слайда — сжато\n### [narrativ] завязка\nзаполнить",
    "## Текст слайда — сжато\n### [narrativ] завязка\nНастоящий сжатый текст.")
p.write_text(t, encoding="utf-8")
PY
OUT32P2=$(python3 "$SBORKA/gejt_kartochki.py" "$L32" 2>&1) || {
  echo "❌ ЛОВУШКА 32: настоящее тело — полный гейт всё равно красный:"; echo "$OUT32P2"; exit 1; }
OUT32F2=$(python3 "$SBORKA/gejt_kartochki.py" --faza 1 "$L32" 2>&1) || {
  echo "❌ ЛОВУШКА 32: настоящее тело — --faza 1 покраснел:"; echo "$OUT32F2"; exit 1; }
echo "  ✅ ловушка 32: заглушка — оба красные на МЫСЛИ; размечено без тел — faza1 зелёный, полный красный на ТЕЛЕ; написано — оба зелёные"

echo "── ловушка 33: 🔴 Д17 (заход tihie-polomki, П1) — тег сцены над списком не рушит его в абзац"
OUT33=$(python3 - <<'PY'
import sys
sys.path.insert(0, "_generator")
from build_deck import render_md
html = render_md('{@3}\n- раз\n- два', {}, None)
print(html)
sys.exit(0 if ('<ul' in html and html.count('<li>') == 2 and 'data-scene-from="3"' in html) else 1)
PY
)
RC33=$?
[ "$RC33" -eq 0 ] || {
  echo "❌ ЛОВУШКА 33: список под тегом сцены схлопнулся в абзац (Д17 регрессия):"
  echo "$OUT33"; exit 1; }
echo "  ✅ ловушка 33: {@3}+список → <ul> с data-scene-from=\"3\" и двумя <li>: $OUT33"

echo "── ловушка 34: 🔴 (заход tihie-polomki, П2) — опечатка в {.имя} даёт красное поимённо, rc≠0"
L34="$T/lek34"
python3 "$SBORKA/bootstrap_lekcii.py" "$L34" >/dev/null
python3 - "$L34" <<'PY'
import sys
p = sys.argv[1] + "/brief.md"
t = open(p, encoding="utf-8").read()
t = t.replace("slide_order:\n", "slide_order:\n  - s01\n")
open(p, "w", encoding="utf-8").write(t)
PY
python3 "$SBORKA/bootstrap_lekcii.py" "$L34" >/dev/null
python3 -c "$ZAP_VALS_PY" "$L34" s01
python3 - "$L34" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1]) / "slajdy" / "s01" / "slaid.md"
t = p.read_text(encoding="utf-8")
t = t.replace(
    "## Текст слайда — сжато\n### [narrativ] заполнить\nзаполнить",
    "## Текст слайда — сжато\n### [narrativ] завязка\n{.tlsit}\n- раз\n- два")
p.write_text(t, encoding="utf-8")
PY
OUT34A=$(python3 "$SBORKA/slaid.py" "$L34/slajdy/s01" -o "$T/s01-bad.html" 2>&1) && {
  echo "❌ ЛОВУШКА 34: {.tlsit} (опечатка) прошла молча, rc=0:"; echo "$OUT34A"; exit 1; }
echo "$OUT34A" | grep -q "tlsit" || {
  echo "❌ ЛОВУШКА 34: гейт покраснел, но не поимённо на классе tlsit:"; echo "$OUT34A"; exit 1; }
echo "$OUT34A" | grep -q "строка" || {
  echo "❌ ЛОВУШКА 34: гейт покраснел, но без номера строки (П2-критерий требует именно его):"
  echo "$OUT34A"; exit 1; }
echo "  ✅ ловушка 34а: {.tlsit} — красное поимённо, с номером строки, rc≠0"
python3 - "$L34" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1]) / "slajdy" / "s01" / "slaid.md"
p.write_text(p.read_text(encoding="utf-8").replace("{.tlsit}", "{.tlist}"), encoding="utf-8")
PY
OUT34B=$(python3 "$SBORKA/slaid.py" "$L34/slajdy/s01" -o "$T/s01-good.html" 2>&1) || {
  echo "❌ ЛОВУШКА 34: {.tlist} (правильный класс) НЕ прошла:"; echo "$OUT34B"; exit 1; }
echo "  ✅ ловушка 34б: {.tlist} — зелёное, rc=0"

echo "── ловушка 35: 🔴 Д-6 (заход format-kartochki-faza-1) — миграция дописывает поля, не трогая заполненного, и идемпотентна"
# Зачем сторожить фикстурой: формат карточки меняется, пока интервью по живой
# лекции уже идёт. Цель владельца дословно — «не переделывать слайды», и
# единственное, что её обеспечивает, — КОМАНДА миграции, а не инструкция
# «допишите поле». Ловушка сторожит три её свойства разом: поля появились,
# заполненное не тронуто, второй прогон даёт нулевой диф.
L35="$T/lek35"
python3 "$SBORKA/bootstrap_lekcii.py" "$L35" >/dev/null
python3 - "$L35" <<'PY'
import sys
p = sys.argv[1] + "/brief.md"
t = open(p, encoding="utf-8").read()
t = t.replace("slide_order:\n", "slide_order:\n  - s01\n")
open(p, "w", encoding="utf-8").write(t)
PY
python3 "$SBORKA/bootstrap_lekcii.py" "$L35" >/dev/null
# имитируем карточку СТАРОГО формата: вырезаем поля фазы 1 и блок «что дальше»,
# одно поле заполняем по-настоящему — миграция обязана его не тронуть
python3 - "$L35" <<'PY'
import re, sys
from pathlib import Path
p = Path(sys.argv[1]) / "slajdy" / "s01" / "slaid.md"
t = re.sub(r"^<!--.*?-->\s*", "", p.read_text(encoding="utf-8"), flags=re.S)
for pole in ("tip_slaida", "centralnyj_blok", "matematika_iz"):
    t = re.sub(r"^%s:.*\n" % pole, "", t, flags=re.M)
t = t.replace("nazvanie: заполнить", "nazvanie: Живое название")
p.write_text(t, encoding="utf-8")
PY
cp -R "$L35" "$T/lek35-do"
OUT35=$(python3 "$SBORKA/bootstrap_lekcii.py" "$L35" --migraciya 2>&1) || {
  echo "❌ ЛОВУШКА 35: миграция упала:"; echo "$OUT35"; exit 1; }
for POLE in "tip_slaida" "centralnyj_blok" "matematika_iz"; do
  grep -q "^$POLE:" "$L35/slajdy/s01/slaid.md" || {
    echo "❌ ЛОВУШКА 35: после миграции в шапке нет поля $POLE:"; echo "$OUT35"; exit 1; }
done
grep -q "^ФАЗА 1" "$L35/slajdy/s01/slaid.md" || {
  echo "❌ ЛОВУШКА 35: блок «что дальше» не перешит — ФАЗА 1 в нём не названа:"; exit 1; }
grep -q "^nazvanie: Живое название$" "$L35/slajdy/s01/slaid.md" || {
  echo "❌ ЛОВУШКА 35: миграция затёрла ЗАПОЛНЕННОЕ поле nazvanie — ровно то, чего Д-6 запрещает:"
  exit 1; }
cp -R "$L35" "$T/lek35-posle1"
OUT35B=$(python3 "$SBORKA/bootstrap_lekcii.py" "$L35" --migraciya 2>&1) || {
  echo "❌ ЛОВУШКА 35: повторная миграция упала:"; echo "$OUT35B"; exit 1; }
diff -r "$T/lek35-posle1" "$L35" >/dev/null || {
  echo "❌ ЛОВУШКА 35: второй прогон миграции изменил дерево — не идемпотентна:"; exit 1; }
echo "  ✅ ловушка 35: поля дописаны, блок «что дальше» перешит с ФАЗЫ 1, заполненное цело, второй прогон — нулевой диф"

# ── ловушки 36-38: смета вмещения (заход svedenie-i-smeta, Э2) ─────────────────
echo "── ловушка 36: смета — КРИВОЙ ВХОД отвергается внятно, а не трейсбеком"
for PROBA in "--byudzhet net_takogo_tipa 50" "--byudzhet polosa_vertikalnaya abc" "$T/net-takoj-papki"; do
  OUT36=$(python3 "$SBORKA/smeta.py" $PROBA 2>&1) && {
    echo "❌ ЛОВУШКА 36: кривой вход «$PROBA» принят (rc=0):"; echo "$OUT36"; exit 1; }
  echo "$OUT36" | grep -q "ОШИБКА" || {
    echo "❌ ЛОВУШКА 36: кривой вход «$PROBA» отвергнут, но БЕЗ внятного «ОШИБКА»:"
    echo "$OUT36"; exit 1; }
  echo "$OUT36" | grep -q "Traceback" && {
    echo "❌ ЛОВУШКА 36: кривой вход «$PROBA» дал ТРЕЙСБЕК вместо сообщения:"
    echo "$OUT36"; exit 1; }
done
OUT36G=$(python3 "$SBORKA/gejt_vmeshcheniya.py" "$T/net-takogo-slajda.html" 2>&1) && {
  echo "❌ ЛОВУШКА 36: гейт вмещения принял несуществующий файл:"; echo "$OUT36G"; exit 1; }
echo "$OUT36G" | grep -q "ОШИБКА" || {
  echo "❌ ЛОВУШКА 36: гейт вмещения отверг несуществующий файл без «ОШИБКА»:"
  echo "$OUT36G"; exit 1; }
OUT36Z=$(python3 "$SBORKA/zamer_smety.py" --konstanty "$T/net-takoj-lekcii" 2>&1) && {
  echo "❌ ЛОВУШКА 36: замер принял несуществующую лекцию:"; echo "$OUT36Z"; exit 1; }
echo "  ✅ ловушка 36: пять кривых входов отвергнуты внятно, без трейсбеков"

echo "── ловушка 37: 🔴 смета ВОСПРОИЗВОДИТ ЗАМЕР геометрии — иначе она живёт своей жизнью"
# Сердце Э2: `smeta.py` — вторая модель вёрстки рядом с браузером. Разойтись она
# может только молча, поэтому сверка с замером обязана быть исполнимой командой.
OUT37=$(python3 "$SBORKA/smeta.py" --proverit-geometriyu 2>&1) || {
  echo "❌ ЛОВУШКА 37: геометрия сметы разошлась с замером браузера:"; echo "$OUT37"; exit 1; }
echo "$OUT37" | grep -q "проверено 20 точек из 20" || {
  echo "❌ ЛОВУШКА 37: сверка геометрии без строки охвата «проверено X точек из Y»:"
  echo "$OUT37"; exit 1; }
echo "  ✅ ловушка 37: геометрия сметы воспроизводит замер, охват объявлен"

echo "── ловушка 38: 🔴 ГЕЙТ РАСХОЖДЕНИЯ УМЕЕТ ПРОВАЛИТЬСЯ (иначе он украшение)"
# Тот же принцип, что у ловушки 29: гейт, который не может покраснеть, — не гейт.
OUT38K=$(python3 "$SBORKA/smeta.py" --sverit "$REPO_ROOT/teorkat-vvedenie/L2" --isportit 1.3 2>&1) && {
  echo "❌ ЛОВУШКА 38: ПОДДЕЛАННАЯ смета (×1.3) не покрасила гейт расхождения:"
  echo "$OUT38K"; exit 1; }
echo "$OUT38K" | grep -q "ГЕЙТ РАСХОЖДЕНИЯ КРАСНЫЙ" || {
  echo "❌ ЛОВУШКА 38: гейт вернул rc≠0, но без вердикта «ГЕЙТ РАСХОЖДЕНИЯ КРАСНЫЙ»:"
  echo "$OUT38K"; exit 1; }
OUT38Z=$(python3 "$SBORKA/smeta.py" --sverit "$REPO_ROOT/teorkat-vvedenie/L2" 2>&1) || {
  echo "❌ ЛОВУШКА 38: КАЛИБРОВАННАЯ смета покрасила гейт — ложное срабатывание:"
  echo "$OUT38Z"; exit 1; }
echo "$OUT38Z" | grep -q "мереных карточках" || {
  echo "❌ ЛОВУШКА 38: зелёный вердикт без охвата «N мереных карточках»:"
  echo "$OUT38Z"; exit 1; }
echo "  ✅ ловушка 38: подделанная смета — красный с вердиктом; калиброванная — зелёный с охватом"

echo "── ловушка 39: 🔴 ПУСТОЙ ТЕГ не съедает блоки сметы (`<br>`, `<br/>`, `<img>`)"
# Найдено верификатором §3 на НЕ-калибровочном материале: `HTMLParser` зовёт
# `handle_starttag` и на `<br>`, парного закрытия не будет, стек глубины уезжал
# НАВСЕГДА — и все следующие абзацы верхнего уровня переставали опознаваться.
# Молча: ни ошибки, ни предупреждения, просто смета занижала на 6.9 строки
# (`buffon/sl-grid` — один блок вместо трёх). На L2 `<br>` не встречается ни разу.
OUT39=$(python3 - <<'PYEOF' 2>&1
import sys
sys.path.insert(0, "_generator/sborka")
from smeta import _ZonaParser
Z = '<div class="zone copy t-body">%s<p>BBBB</p><p>CCCC</p></div>'
for imya, pervyj, segm in (("без пустых", "<p>AAAA</p>", 1),
                            ("br", "<p>AA<br>AA</p>", 2),
                            ("br со слэшем", "<p>AA<br/>AA</p>", 2),
                            ("img", "<p>AA<img src=x>AA</p>", 1)):
    p = _ZonaParser(); p.feed(Z % pervyj)
    if len(p.bloki) != 3:
        print("ПРОВАЛ: %s — блоков %d, ожидалось 3" % (imya, len(p.bloki))); sys.exit(1)
    if len(p.bloki[0]["segmenty"]) != segm:
        print("ПРОВАЛ: %s — сегментов %d, ожидалось %d"
              % (imya, len(p.bloki[0]["segmenty"]), segm)); sys.exit(1)
print("ok")
PYEOF
) || { echo "❌ ЛОВУШКА 39: $OUT39"; exit 1; }
echo "  ✅ ловушка 39: три формы пустого тега — блоки целы, `<br>` рвёт строку, `<img>` нет"

echo "── ловушка 40: 🔴 смета ОТКАЗЫВАЕТСЯ на узкой колонке, а не занижает молча"
# Занижение — опасная сторона ошибки: даёт ПРОПУСК переполнения, а не ложную
# тревогу. Проверено верификатором §3: при 22 знаках в строке смета занижала на
# 2.95 строки. Ниже проверенной границы обязан быть ОТКАЗ.
OUT40=$(python3 "$SBORKA/smeta.py" --byudzhet polosa_vertikalnaya 20 2>&1) && {
  echo "❌ ЛОВУШКА 40: смета выдала бюджет на колонке уже проверенной границы:"
  echo "$OUT40"; exit 1; }
echo "$OUT40" | grep -q "знаков в строке" || {
  echo "❌ ЛОВУШКА 40: отказ без названного числа знаков в строке:"; echo "$OUT40"; exit 1; }
OUT40G=$(python3 "$SBORKA/smeta.py" --byudzhet polosa_vertikalnaya 66 2>&1) || {
  echo "❌ ЛОВУШКА 40: рабочая колонка (66%) тоже отвергнута — граница задрана:"
  echo "$OUT40G"; exit 1; }
echo "  ✅ ловушка 40: узкая колонка — отказ с числом; рабочая — бюджет"

echo "── ловушка 41: 🔴 заход zakony-v-gejt — двенадцать законов фазы 2, каждый ловит СВОЙ кривой вход"
# Фикстура `zakony-l2/` — 14 карточек, каждая нарушает РОВНО один из двенадцати
# законов (две служебные соседки zk-bound1/zk-bound2 несут ноль нарушений вовсе —
# они держат границы для Г-15, а не проверяют закон сами). Порог включения — ЖЁЛТОЕ,
# не красное (заход дословно: «закон, у которого появился нарушитель, выдаёт
# жёлтое»), поэтому здесь сторожим НАЗВАННОСТЬ закона поимённо в выводе, а не rc:
# `rc=0` на этой фикстуре — ожидаемый и правильный исход, не провал ловушки.
L41="$SBORKA/../tools/fixtures/sborka/zakony-l2"
OUT41=$(python3 "$SBORKA/gejt_kartochki.py" "$L41" 2>&1) || {
  echo "❌ ЛОВУШКА 41: фикстура законов дала rc≠0 — жёлтое покрасило гейт, порог включения нарушен:"
  echo "$OUT41"; exit 1; }
echo "$OUT41" | grep -q "ЗЕЛЁНЫЙ" || {
  echo "❌ ЛОВУШКА 41: rc=0, но текст не «ЗЕЛЁНЫЙ» — двенадцать законов обязаны быть жёлтыми, не красными:"
  echo "$OUT41"; exit 1; }
for ZAK in "zk-a6" "zk-a8" "zk-a9" "zk-a10" "zk-g1" "zk-g2" "zk-g3" "zk-g6" "zk-g7" "zk-g8" "zk-g12" "zk-g15"; do
  echo "$OUT41" | grep -q "$ZAK:" || {
    echo "❌ ЛОВУШКА 41: закон, чья фикстура — $ZAK, не назван в выводе поимённо:"
    echo "$OUT41"; exit 1; }
done
for ZAK in "А6" "А8" "А9" "А10" "Г-1" "Г-2" "Г-3" "Г-6" "Г-7" "Г-8" "Г-12" "Г-15"; do
  echo "$OUT41" | grep -q "⚠ $ZAK " || {
    echo "❌ ЛОВУШКА 41: закон $ZAK не отмечен жёлтым (⚠) в сводке двенадцати:"
    echo "$OUT41"; exit 1; }
done
echo "$OUT41" | grep -q "12 из 12" || {
  echo "❌ ЛОВУШКА 41: сводка не называет охват «12 из 12» законов:"; echo "$OUT41"; exit 1; }
echo "  ✅ ловушка 41: двенадцать законов фазы 2 — каждый ловит свой кривой вход поимённо, rc=0 (жёлтое не красит гейт)"

echo "── ловушка 42: 🔴 заход tipologia-odna-os, Э3 — жёсткий гейт состава УМЕЕТ КРАСНЕТЬ"
# Клауза 3 критерия готовности захода: зелёный гейт, который ни на чём не
# краснеет, — не гейт, а декорация. Фикстура tipologia-e3-negativ несёт три
# карточки, КАЖДАЯ нарушает РОВНО одну из трёх красных клауз Э3 (недостающий
# обязательный блок / лишний блок вне раскладки / нарушенный порядок) и
# ничего больше — изоляция та же, что у ловушки 41 для законов фазы 2.
L42="$SBORKA/../tools/fixtures/sborka/tipologia-e3-negativ"
OUT42=$(python3 "$SBORKA/gejt_kartochki.py" "$L42" 2>&1) && {
  echo "❌ ЛОВУШКА 42: фикстура Э3 (три заведомо неправильные карточки) дала rc=0 — гейт состава не краснеет вовсе:"
  echo "$OUT42"; exit 1; }
echo "$OUT42" | grep -q "проверено 3 из 3" || {
  echo "❌ ЛОВУШКА 42: вердикт без охвата «проверено 3 из 3»:"; echo "$OUT42"; exit 1; }
echo "$OUT42" | grep -q "nedostayushchij: тип Т3 — не хватает обязательного блока \[dokazatelstvo\]" || {
  echo "❌ ЛОВУШКА 42: клауза «недостающий обязательный блок» не сработала на nedostayushchij:"
  echo "$OUT42"; exit 1; }
echo "$OUT42" | grep -q "lishnij: тип Т1 — блок(и) вне раскладки: dokazatelstvo" || {
  echo "❌ ЛОВУШКА 42: клауза «лишний блок вне раскладки» не сработала на lishnij:"
  echo "$OUT42"; exit 1; }
echo "$OUT42" | grep -q "poryadok: тип Т3 — нарушен порядок блоков" || {
  echo "❌ ЛОВУШКА 42: клауза «нарушенный порядок» не сработала на poryadok:"
  echo "$OUT42"; exit 1; }
echo "$OUT42" | grep -q "замечаний 3" || {
  echo "❌ ЛОВУШКА 42: ожидалось РОВНО три замечания (по одному на карточку), сводка другая:"
  echo "$OUT42"; exit 1; }
echo "  ✅ ловушка 42: три негативные фикстуры Э3 — каждая красит СВОЮ клаузу поимённо, rc≠0, замечаний ровно 3"
echo "── ловушка 43: 🔴 (заход nositel) секция-носитель НЕ ловится С5 — на ОБЕИХ вёрстках"
# 🔴 ЗАМЕРЕНО, А НЕ ПРЕДПОЛОЖЕНО (заход `nositel`, ## ЗАДАЧА шаг 1, ловушка
# «помельче»): первая редакция секции-носителя дала «❌ С5: заход зовёт
# `git_zona.py worktree` с позиционным аргументом» — С5 разбирал `vyzovy()` из
# блока ВМЕСТЕ с прозой, стоявшей на той же строке за командой («…, затем
# чтение захода»). Починка (`check_sborki._bez_startovogo`, тем же приёмом,
# что `check_zahod._bez_startovogo`) вырезает секцию ДО разбора — проверяем
# ОБЕ вёрстки: однострочную (проблемную форму) и переформатированную
# (нынешнюю форму генератора), чтобы молчание не оказалось случайностью вёрстки.
sobrat_zdorovyj "$T/kod_nositel-odna-stroka.md"
python3 - "$T/kod_nositel-odna-stroka.md" <<'PY'
import sys
p = sys.argv[1]
t = open(p, encoding='utf-8').read()
yakor = "# Канал исполнителя — proba (эталон фикстуры)\n"
assert t.count(yakor) == 1, 'якорь шапки разъехался с фикстурой'
sekciya = (
    "\n## СТАРТОВОЕ СООБЩЕНИЕ ВЛАДЕЛЬЦУ\n\n"
    "> Это блок для владельца — то, чем тебя запустили. Исполнителю здесь делать нечего, твоё задание ниже.\n\n"
    "```\n"
    "Первым ходом: python3 _generator/tools/git_zona.py worktree add nositel "
    "--branch zahod/nositel, затем чтение захода, затем секция\n"
    "## ПЛАН внутри него — до всяких действий.\n"
    "```\n"
)
t = t.replace(yakor, yakor + sekciya, 1)
open(p, 'w', encoding='utf-8').write(t)
PY
molchit "секция-носитель, однострочная вёрстка (проблемная форма)" "С5" "$T/kod_nositel-odna-stroka.md"

sobrat_zdorovyj "$T/kod_nositel-pereformat.md"
python3 - "$T/kod_nositel-pereformat.md" <<'PY'
import sys
p = sys.argv[1]
t = open(p, encoding='utf-8').read()
yakor = "# Канал исполнителя — proba (эталон фикстуры)\n"
assert t.count(yakor) == 1, 'якорь шапки разъехался с фикстурой'
# 🔴 Та же фраза, что в форме 1, но перенос строки стоит СРАЗУ после запятой —
# ровно то, чем в живом заходе `kod_nositel.md` обошли ловушку ДО этой правки
# (см. ## ЗАДАЧА, шаг 1: «в этом файле я обошёл ловушку иначе — снял `##` в
# одной строке блока»). Это случайность вёрстки, а не починка, и обе формы
# обязаны молчать ОДИНАКОВО — не только та, что сейчас случайно не ловится.
sekciya = (
    "\n## СТАРТОВОЕ СООБЩЕНИЕ ВЛАДЕЛЬЦУ\n\n"
    "> Это блок для владельца — то, чем тебя запустили. Исполнителю здесь делать нечего, твоё задание ниже.\n\n"
    "```\n"
    "Первым ходом: python3 _generator/tools/git_zona.py worktree add nositel --branch zahod/nositel,\n"
    "затем чтение захода, затем секция ПЛАН внутри него — до всяких действий.\n"
    "```\n"
)
t = t.replace(yakor, yakor + sekciya, 1)
open(p, 'w', encoding='utf-8').write(t)
PY
molchit "секция-носитель, переформатированная вёрстка (текущая случайная форма)" "С5" "$T/kod_nositel-pereformat.md"
echo "  ✅ ловушка 43: секция-носитель не ловится С5 ни в однострочной, ни в переформатированной вёрстке"

echo "ФИКСТУРЫ ЗЕЛЁНЫЕ"
