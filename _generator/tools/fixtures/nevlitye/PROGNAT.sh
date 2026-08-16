#!/bin/sh
# TOOL-CONTRACT-COVERS: bootstrap_zahod.py
# ↑ ОХВАТ: СТОРОЖ НЕВЛИТЫХ ВЕТОК — функция `nevlityje_vetki()` и то, что она
# печатает в §0.1 собранного захода. Отдельная фикстура, а не пункт в
# `fixtures/zahod/`, по одной причине: та судит ЛИНТЕР входа (`check_zahod.py`)
# над текстом захода, а здесь предмет иной — ЧТЕНИЕ ВЫВОДА GIT. Ловушки 17-19
# соседней фикстуры проверяли сторож на репозитории БЕЗ рабочих папок, и именно
# поэтому дефект дожил незамеченным: в таком репозитории префикса `+` не бывает
# вовсе, а заходы фабрики работают в worktree ПО ПОСТРОЕНИЮ.
#
# Запуск:  sh _generator/tools/fixtures/nevlitye/PROGNAT.sh
# Ожидание: ФИКСТУРЫ ЗЕЛЁНЫЕ, exit 0.
#
# ЧТО СТОРОЖИТ КАЖДАЯ ЛОВУШКА (сколько их — печатает сам прогон, `KONSTITUCIYA §10`):
#   1. ЖИВОЙ GIT + ЖИВАЯ РАБОЧАЯ ПАПКА: ветка, вычекаученная в worktree, попадает
#      в список невлитых. Это тот самый случай, на котором сторож слеп с 08.08.
#   2. 🔴 ОТРИЦАТЕЛЬНЫЙ КОНТРОЛЬ САМОЙ ЛОВУШКИ: тот же вывод git, прочитанный
#      СТАРОЙ формулой (`lstrip("* ")`), обязан дать ДРУГОЙ, беднее, ответ.
#      Совпали — ловушка бессильна и говорит об этом вслух: зелёная в обоих
#      случаях фикстура не ловушка, а украшение.
#   3. ВСЕ ТРИ ПРЕФИКСА РАЗОМ (`*` текущая, `+` worktree, голое имя) — на
#      подставном `git`, который ведёт себя как настоящий: с `--format` отдаёт
#      голые имена, без него — украшенные. Живой git не даёт собрать все три
#      префикса в одном выводе (текущая ветка в `--no-merged <она же>` не
#      появляется по построению), а требование захода буквально про три.
#   4. ФИЛЬТР НЕ ОСЛАБ: ветка не из `zahod/*` в список НЕ попадает. Без этой
#      половины «починка» вида «вернуть всё подряд» была бы зелёной.
#   5. СКВОЗНОЙ ПРОГОН ГЕНЕРАТОРА: собранный заход НАЗЫВАЕТ невлитую
#      worktree-ветку ПОИМЁННО в §0.1, а не пишет «вливать нечего». Функция может
#      быть верна, а печать — потеряна; проверяется то, что читает исполнитель.
#   6. ГЕНЕРАТОР НЕ ОТКАЗЫВАЕТ на невлитом (§2.3: невлитая ветка — законное
#      состояние): rc=0 и файл на диске. Регрессия на превращение сторожа в гейт.
set -e
TOOLS=$(cd "$(dirname "$0")/../.." && pwd)
REPO_ROOT=$(cd "$TOOLS/../.." && pwd)
# Наследованное окружение git ломает синтетический репозиторий: `GIT_DIR` и
# соседи от родительского процесса увели бы все команды ниже в `materials`.
unset $(git rev-parse --local-env-vars) 2>/dev/null || true

LOVUSHEK=$(grep -c '^echo "── ловушка' "$0" || true)
echo "ловушек в этом прогоне: $LOVUSHEK  ← grep -c '^echo \"── ловушка' $0"

T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT

G() { git -c user.email=proba@proba -c user.name=proba "$@"; }

# ── синтетический репозиторий: main + три ветки, одна под рабочей папкой ───────
R="$T/repo"
mkdir -p "$R"
( cd "$R"
  G -c init.defaultBranch=main init -q
  echo start > f.txt; G add f.txt; G commit -q -m init
  for B in zahod/v-worktree zahod/prostaya chuzhaya/ne-zahod; do
    G checkout -q -b "$B"
    echo "$B" > "$(echo "$B" | tr '/' '-').txt"
    G add -A; G commit -q -m "$B"
    G checkout -q main
  done
  # 🔴 РАБОЧАЯ ПАПКА — СЕРДЦЕ ФИКСТУРЫ. Именно она заставляет git пометить ветку
  # знаком `+`; без неё вывод состоит из голых имён и дефект невоспроизводим.
  G worktree add -q "$T/wt-v-worktree" zahod/v-worktree )

echo "── ловушка 1: живой git + живая рабочая папка — worktree-ветка видна сторожу"
SYROJ=$( cd "$R" && git --no-optional-locks branch --no-merged main )
echo "$SYROJ" | sed -n 'l' | sed 's/^/    сырой git: /'
# Предохранитель от ложно-зелёной фикстуры: если этот git НЕ метит worktree-ветку
# плюсом, то ловушка 1 зеленела бы не потому, что код верен, а потому, что
# проверять нечего. Такую фикстуру нельзя оставлять молча зелёной.
echo "$SYROJ" | grep -q '^+ zahod/v-worktree$' || {
  echo "❌ ФИКСТУРА НЕДЕЙСТВИТЕЛЬНА: этот git не метит worktree-ветку знаком '+',"
  echo "   значит ловушка проверяет не тот мир. Вывод:"; echo "$SYROJ"; exit 1; }
NAJDENO=$(cd "$R" && GIT_ZONA_REPO="$R" python3 -c "
import sys
sys.path.insert(0, '$TOOLS')
import bootstrap_zahod as bz
vetki, err = bz.nevlityje_vetki()
assert err is None, 'сторож отказал: %s' % err
print(' '.join(sorted(vetki)))
")
echo "    сторож вернул: [$NAJDENO]"
echo "$NAJDENO" | grep -q 'zahod/v-worktree' || {
  echo "❌ ЛОВУШКА 1: сторож НЕ увидел ветку, вычекаученную в рабочей папке —"
  echo "   ровно тот дефект, из-за которого в каждый заход печаталось «вливать нечего»."
  echo "   Вернул: [$NAJDENO]"; exit 1; }
echo "$NAJDENO" | grep -q 'zahod/prostaya' || {
  echo "❌ ЛОВУШКА 1: сторож потерял ОБЫЧНУЮ невлитую ветку (без рабочей папки)."
  echo "   Вернул: [$NAJDENO]"; exit 1; }
echo "  ✅ ловушка 1: обе невлитые ветки названы — и worktree-ветка, и обычная"

echo "── ловушка 2: 🔴 отрицательный контроль — СТАРАЯ формула на том же выводе беднее"
# Ловушка обязана уметь провалиться. Здесь буквально воспроизводится прежнее
# чтение (`l.strip().lstrip("* ").strip()`) и требуется, чтобы оно дало ДРУГОЙ
# ответ: пока формулы различимы, ловушка 1 имеет силу. Станут неразличимы —
# фикстура скажет об этом сама, а не будет зелёной по инерции.
STARAYA=$(SYROJ="$SYROJ" python3 -c "
import os
vyvod = os.environ['SYROJ']
imena = [l.strip().lstrip('* ').strip() for l in vyvod.splitlines() if l.strip()]
print(' '.join(sorted(b for b in imena if b.startswith('zahod/'))))
")
echo "    старая формула вернула: [$STARAYA]"
[ "$STARAYA" != "$NAJDENO" ] || {
  echo "❌ ЛОВУШКА 2: старая и новая формулы дали ОДИН ответ — ловушка 1 ничего не"
  echo "   различает и была бы зелёной на сломанном коде тоже. Чинить фикстуру."
  exit 1; }
echo "$STARAYA" | grep -q 'zahod/v-worktree' && {
  echo "❌ ЛОВУШКА 2: старая формула НЕ теряет worktree-ветку — значит воспроизведён"
  echo "   не тот дефект, и вся фикстура сторожит фантом."; exit 1; }
echo "  ✅ ловушка 2: старая формула теряет worktree-ветку, новая — нет; ловушка различает"

echo "── ловушка 3: все три префикса разом (* текущая, + worktree, голое имя)"
# Живой git не выдаёт три префикса в одном выводе `--no-merged <текущая>`:
# текущая ветка влита в саму себя и в список не попадает. Требование захода —
# буквально про три, поэтому здесь подставной `git`, который ведёт себя как
# настоящий: с `--format` отдаёт голые имена, без него — украшенные. Всё, чего
# он не знает, уходит НАСТОЯЩЕМУ git — иначе импорт `korni` умер бы на первой
# же незнакомой команде, и ловушка молчала бы по постороннней причине.
mkdir -p "$T/bin"
REALGIT=$(command -v git)
cat > "$T/bin/git" <<SH
#!/bin/sh
case "\$*" in
  *"branch --no-merged"*)
    case "\$*" in
      *--format=*) printf 'zahod/tekushchaya\nzahod/v-worktree\nzahod/prostaya\nchuzhaya/ne-zahod\n' ;;
      *)           printf '* zahod/tekushchaya\n+ zahod/v-worktree\n  zahod/prostaya\n  chuzhaya/ne-zahod\n' ;;
    esac
    exit 0 ;;
  *"rev-parse --abbrev-ref HEAD"*) echo main; exit 0 ;;
esac
exec "$REALGIT" "\$@"
SH
chmod +x "$T/bin/git"
TRI=$(cd "$R" && PATH="$T/bin:$PATH" GIT_ZONA_REPO="$R" python3 -c "
import sys
sys.path.insert(0, '$TOOLS')
import bootstrap_zahod as bz
vetki, err = bz.nevlityje_vetki()
assert err is None, 'сторож отказал: %s' % err
print(' '.join(sorted(vetki)))
")
echo "    сторож вернул: [$TRI]"
for V in zahod/tekushchaya zahod/v-worktree zahod/prostaya; do
  echo "$TRI" | grep -q "$V" || {
    echo "❌ ЛОВУШКА 3: потеряна ветка $V — сторож читает не все префиксы. Вернул: [$TRI]"
    exit 1; }
done
echo "  ✅ ловушка 3: все три префикса прочитаны"

echo "── ловушка 4: фильтр не ослаб — ветка не из zahod/* в список НЕ попадает"
echo "$TRI" | grep -q 'chuzhaya/ne-zahod' && {
  echo "❌ ЛОВУШКА 4: в список попала ветка вне `zahod/*` — «починка» вида «вернуть"
  echo "   всё подряд» тоже сделала бы ловушки 1 и 3 зелёными. Вернул: [$TRI]"; exit 1; }
echo "$NAJDENO" | grep -q 'chuzhaya/ne-zahod' && {
  echo "❌ ЛОВУШКА 4: на живом git в список попала ветка вне `zahod/*`. Вернул: [$NAJDENO]"
  exit 1; }
echo "  ✅ ловушка 4: чужая ветка отфильтрована на обоих прогонах"

# ── сквозной прогон: то, что реально читает исполнитель ────────────────────────
# Функция может быть верна, а печать в §0.1 — потеряна: между ними два ветвления
# (`_sostoyanie_nevlityh`) и слот `--vlit`. Проверяется ФАЙЛ, а не возврат.
mkdir -p "$R/_studio/zhurnal/proba" "$R/_studio/docs" "$R/_generator/tools/dummy-zone"
cp "$REPO_ROOT/_studio/zhurnal/_TEMPLATE-zahod.md" "$R/_studio/zhurnal/_TEMPLATE-zahod.md"
: > "$R/_generator/tools/dummy-zone/fake.py"
printf '# синтетика фикстуры\n%s\n' "$R" > "$R/_generator/tools/KANON-KOREN"
cat > "$R/_studio/docs/KARTA.md" <<'MD'
# KARTA (синтетика фикстуры, не настоящий индекс)

## §6. Заходы и документы
MD
( cd "$R" && G add -A && G commit -q -m "скелет для сборки захода" )

echo "── ловушка 5: сквозной прогон — §0.1 называет worktree-ветку ПОИМЁННО"
OUT5=$(cd "$R" && GIT_ZONA_REPO="$R" python3 "$TOOLS/bootstrap_zahod.py" --intervyu da \
    _studio/zhurnal/proba proba-nevlitye --branch proba-nevlitye-branch \
    --zone '_generator/tools/dummy-zone/fake.py' --kanal terminal \
    --finalizirovano "ф1" --finalizirovano "ф2" 2>&1)
RC5=$?
[ "$RC5" -eq 0 ] || { echo "❌ ЛОВУШКА 5: генератор упал (rc=$RC5). Вывод:"; echo "$OUT5"; exit 1; }
F5="$R/_studio/zhurnal/proba/kod_proba-nevlitye.md"
[ -f "$F5" ] || { echo "❌ ЛОВУШКА 5: заход не создан — $F5"; exit 1; }
grep -q 'zahod/v-worktree' "$F5" || {
  echo "❌ ЛОВУШКА 5: в собранном заходе НЕТ имени невлитой worktree-ветки —"
  echo "   исполнитель прочтёт «вливать нечего» при живой невлитой ветке."
  echo "   Строка §0.1 из файла:"; grep -n 'вливать нечего\|НЕ ЗАПОЛНЕНО' "$F5" | head -3
  exit 1; }
grep -q 'вливать нечего' "$F5" && {
  echo "❌ ЛОВУШКА 5: файл говорит «вливать нечего» при живой невлитой ветке."
  exit 1; }
echo "    §0.1 собранного захода:"
grep -n 'zahod/v-worktree' "$F5" | head -2 | sed 's/^/      /'
echo "  ✅ ловушка 5: невлитая worktree-ветка названа в §0.1 поимённо"

echo "── ловушка 6: сторож ПРЕДУПРЕЖДАЕТ, а не отказывает (§2.3) — rc=0 и файл на диске"
echo "$OUT5" | grep -q 'zahod/v-worktree' || {
  echo "❌ ЛОВУШКА 6: предупреждение в консоли не назвало ветку поимённо. Вывод:"
  echo "$OUT5"; exit 1; }
echo "  ✅ ловушка 6: rc=0, файл собран, предупреждение поимённое"

echo
echo "✅ ВСЕ ЛОВУШКИ ЗЕЛЁНЫЕ ($LOVUSHEK шт.)"
