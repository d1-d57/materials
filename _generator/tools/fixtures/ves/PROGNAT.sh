#!/bin/sh
# TOOL-CONTRACT-COVERS: check_ves.py
# Фикстуры гейта ВЕСА. Гоняй ПОСЛЕ любой правки check_ves.py.
# Строка COVERS выше — не украшение: по ней хук решает, поднимать ли фикстуру.
#
# Зачем именно эти случаи. У check_ves.py три разных кода возврата, и путать их
# дороже всего: 0 — чисто, 1 — нашли тяжёлое вне git, 2 — гейт НЕ ОТРАБОТАЛ.
# Пока разбор входа был `"--tiho" in sys.argv`, опечатка `--tixo` давала шумный
# прогон с кодом 0 или 1 — то есть выглядела как нормальная работа гейта. Это та
# же мина, что оплачена 23.07 на bootstrap_arka.py: `--help` проглотили как имя
# арки и завели папку-сироту, которую потом каждый `plan` тянул в коммит.
#
# Проверяем ТОЛЬКО разбор входа: он отрабатывает до сканирования репозитория,
# поэтому фикстура быстрая и не зависит от того, что сейчас лежит на диске.
cd "$(dirname "$0")/../../../.." || exit 1
G=_generator/tools/check_ves.py
fail=0

# кривой вход → ровно 2, и ни в коем случае не 0/1
for krivoj in "--tixo" "-t" "--help" "putь/k/faylu" "--tiho --lishnee"; do
  # shellcheck disable=SC2086
  python3 "$G" $krivoj >/dev/null 2>&1
  got=$?
  if [ "$got" = "2" ]; then
    echo "  ✅ «$krivoj»: exit 2 (отвергнут громко)"
  else
    echo "  ❌ «$krivoj»: exit $got, ожидался 2"
    fail=1
  fi
done

# кривой вход обязан НАЗВАТЬ себя, а не просто упасть
if python3 "$G" --tixo 2>&1 | grep -q -- "--tixo"; then
  echo "  ✅ сообщение называет сам аргумент"
else
  echo "  ❌ упал молча: в сообщении нет самого аргумента"
  fail=1
fi

# законные флаги разбор проходят: код возврата 0 или 1, но НЕ 2
for zakonnyj in "--tiho" "--staged" "--staged --tiho"; do
  # shellcheck disable=SC2086
  python3 "$G" $zakonnyj >/dev/null 2>&1
  got=$?
  if [ "$got" = "0" ] || [ "$got" = "1" ]; then
    echo "  ✅ «$zakonnyj»: exit $got (разбор пройден)"
  else
    echo "  ❌ «$zakonnyj»: exit $got — разбор отверг законный флаг"
    fail=1
  fi
done

# ── Ворота индекса: тяжёлое обязано быть остановлено ДО коммита ──
# Кладём файл заведомо тяжелее POROG_INDEKS (5 МБ), стейджим, ждём rc=1 и
# упоминание файла по имени.
#
# 🔴 ПОЧЕМУ ЧЕРЕЗ GIT_INDEX_FILE, А НЕ ПРОСТО `git add`. Первая редакция
# стейджила в ЖИВОЙ индекс — автономно зелёная, из хука КРАСНАЯ. Причина: хук
# запускается внутри `git commit`, который уже держит `.git/index.lock`, поэтому
# `git add` тихо не срабатывает, фикстура проверяет пустой индекс и печатает
# «ворота пропускают тяжёлое». То есть фикстура ломалась ровно там, где она
# единственно и нужна — при живом коммите.
# GIT_INDEX_FILE уводит ВЕСЬ git (и `add` фикстуры, и `diff --cached` внутри
# самого гейта) на временный индекс: настоящий не трогается, лок не нужен,
# результат тот же. Подсовывать гейту выдуманные данные при этом не приходится —
# он работает с настоящим git, просто с другим файлом индекса.
T=_generator/tools/fixtures/ves/PROBA-tyazhelogo.bin
mkfile -n 6m "$T" 2>/dev/null || dd if=/dev/zero of="$T" bs=1m count=6 2>/dev/null
VREMENNYJ="${TMPDIR:-/tmp}/ves-proba-index.$$"
rm -f "$VREMENNYJ"
vyvod=$(
  GIT_INDEX_FILE="$VREMENNYJ" export GIT_INDEX_FILE
  git --no-optional-locks read-tree HEAD >/dev/null 2>&1
  git --no-optional-locks add -f -- "$T" >/dev/null 2>&1
  python3 "$G" --staged 2>&1
)
got=$?
rm -f "$VREMENNYJ" "$T"
if [ "$got" = "1" ]; then
  echo "  ✅ индекс: тяжёлое остановлено (exit 1)"
else
  echo "  ❌ индекс: exit $got, ожидался 1 — ворота пропускают тяжёлое в историю"
  fail=1
fi
if printf '%s' "$vyvod" | grep -q "PROBA-tyazhelogo.bin"; then
  echo "  ✅ индекс: файл назван по имени"
else
  echo "  ❌ индекс: файл не назван — по такому сообщению не починишь"
  fail=1
fi

[ $fail = 0 ] && echo "ФИКСТУРЫ ЗЕЛЁНЫЕ" || echo "ФИКСТУРЫ КРАСНЫЕ — гейт сломан правкой"
exit $fail
