#!/bin/sh
# Фикстура git_zona.py — ловит ОБЕ поломки 21.07, каждая из которых завалила
# все 10 коммитов плана и оставила 125 путей вне git.
#
# Запуск:  sh _generator/tools/fixtures/git_zona/PROGNAT.sh
# Ожидание: ФИКСТУРЫ ЗЕЛЁНЫЕ, exit 0.
#
# ЗАЧЕМ. Гейт уроков после инцидента фикстуры получил, а git_zona.py — нет: чинили
# кодом и проверяли глазами. По KONSTITUCIYA §11 это пожелание, а не правило —
# ничто не покраснеет, если правку откатят. Здесь краснеет.
#
# ПОЧЕМУ ЭТО ВООБЩЕ ЗАПУСКАЕТСЯ В ПЕСОЧНИЦЕ. Работает на ОДНОРАЗОВОМ репо в /tmp
# через GIT_ZONA_REPO. Утверждение «в песочнице Cowork git-поведение проверять
# нельзя» верно только для боевого `materials/` (нет прав на unlink в
# .git/objects) и НЕ верно для свежего репо — проверено 21.07.
#
# ДВЕ ЛОВУШКИ, обе оплаченные:
#   1. ГРЯЗНЫЙ ИНДЕКС. `git commit -m` без pathspec забирает индекс ЦЕЛИКОМ,
#      включая чужое, застейдженное кем-то ещё. Цена: коммит из 89 файлов вместо
#      трёх; план из 10 осмысленных коммитов схлопнулся в один свальный.
#   2. НОВЫЕ ФАЙЛЫ. Первая починка убрала `add` и оставила голый
#      `commit -- <пути>` — а pathspec знает ТОЛЬКО отслеживаемые пути. Новый
#      файл даёт `did not match any file(s) known to git`. В плане новых было
#      около трёх четвертей ⇒ всё завалилось повторно.
#   Верная форма — ОБА хода: `add -- <пути>` вводит новые в индекс,
#   pathspec в `commit -- <пути>` отсекает чужое. Фикстура держит обе половины:
#   уберёшь `add` — покраснеет ловушка 2; уберёшь pathspec — покраснеет ловушка 1.

set -e
TOOLS=$(cd "$(dirname "$0")/../.." && pwd)

# 🔴 ОБЯЗАТЕЛЬНО ПЕРВЫМ ХОДОМ: вычистить окружение git.
# Внутри хука git экспортирует GIT_DIR, GIT_INDEX_FILE и другие GIT_* —
# АБСОЛЮТНЫМИ путями на БОЕВОЙ репозиторий. Без этой строки все git-команды
# фикстуры адресуют не одноразовый репо в /tmp, а настоящий: `git init` создаёт
# папку в /tmp, а `add`/`commit` идут в боевой индекс.
# ЦЕНА (21.07, поймано на владельце): фикстура, запущенная хуком, СОЗДАЛА
# КОММИТ В БОЕВОМ РЕПОЗИТОРИИ — автор `fixture fixture@test`, сообщение
# `baseline`, внутрь попал служебный baseline.txt; заодно уронила коммит
# владельца ложным красным и оставила три залипших .lock. Гейт, который пишет
# в проверяемый репозиторий, опаснее отсутствия гейта.
# Проверка, что строка жива: запусти фикстуру с
#   GIT_DIR=$PWD/.git GIT_INDEX_FILE=$PWD/.git/index sh …/PROGNAT.sh
# — она обязана остаться ЗЕЛЁНОЙ и не тронуть текущий репозиторий.
# Форма — КАНОНИЧЕСКАЯ, из документации git (githooks: «if your hook needs to
# invoke Git commands in a foreign repository … it should clear these environment
# variables»). Список даёт сам git, поэтому он не разъедется с версией — самодельный
# перебор по маске `GIT_*` пропустил бы переменные без этого префикса.
unset $(git rev-parse --local-env-vars)

T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT

mkdir -p "$T/_studio"
cd "$T"
git init -q .
# Личность нужна В КОНФИГЕ одноразового репо, а не инлайном через -c: коммит
# делает git_zona.py отдельным процессом, и -c до него не долетает (пробовал —
# фикстура краснеет на «Please tell me who you are»).
# Единственное, что не даёт этим строкам переписать БОЕВОЙ конфиг, — вычистка
# окружения выше. Цена, когда её не было: коммит владельца уехал с автором
# `fixture <fixture@test>`, и заметили это не сразу.
git config user.email fixture@test
git config user.name fixture
# hooksPath не наследуется — одноразовый репо не должен тащить боевые гейты
echo "baseline" > baseline.txt
git add baseline.txt
git commit -qm "baseline"

# ── ЛОВУШКА 1: чужой файл, застейдженный ДО нашего коммита ──
echo "чужая работа" > CHUZHOJ.txt
git add CHUZHOJ.txt

# ── ЛОВУШКА 2: наши пути — НОВЫЕ, git о них ещё не знает ──
mkdir -p moya-zona
echo "новый 1" > moya-zona/novyj-1.md
echo "новый 2" > moya-zona/novyj-2.md
# и один уже отслеживаемый, правленый — чтобы форма работала и на таких
echo "правка" >> baseline.txt

cat > _studio/.commit-plan <<'PLAN'
== фикстура: только своя зона
moya-zona/novyj-1.md
moya-zona/novyj-2.md
baseline.txt
PLAN

GIT_ZONA_REPO="$T" python3 "$TOOLS/git_zona.py" commit > /dev/null 2>&1 || true

FAIL=0
V=$(git show --stat --format= HEAD | grep -c 'novyj-1.md' || true)
[ "$V" = "1" ] && echo "  ✅ новые файлы доехали (add на месте)" \
               || { echo "  ❌ НОВЫЕ ФАЙЛЫ НЕ ДОЕХАЛИ — убран 'git add', вернулась поломка 2"; FAIL=1; }

V=$(git show --stat --format= HEAD | grep -c 'CHUZHOJ' || true)
[ "$V" = "0" ] && echo "  ✅ чужой застейдженный файл НЕ утащен (pathspec на месте)" \
               || { echo "  ❌ ЧУЖОЕ УЕХАЛО В КОММИТ — убран pathspec, вернулась поломка 1"; FAIL=1; }

V=$(git diff --cached --name-only | grep -c 'CHUZHOJ' || true)
[ "$V" = "1" ] && echo "  ✅ чужое осталось в индексе нетронутым" \
               || { echo "  ❌ чужое из индекса пропало — коммит трогает не своё"; FAIL=1; }

V=$(git show --stat --format= HEAD | grep -c 'baseline.txt' || true)
[ "$V" = "1" ] && echo "  ✅ правленый отслеживаемый файл доехал" \
               || { echo "  ❌ правка отслеживаемого файла не доехала"; FAIL=1; }

# ── ЛОВУШКА 3: запрет записи из песочницы ──
# Проверяем ОБЕ стороны детекта, иначе он бесполезен:
#  · на обычной ФС (наш /tmp-репо) commit обязан РАБОТАТЬ — иначе запрет
#    сломает владельца и Claude Code, которым писать можно;
#  · при подделанном /proc/mounts (fuse) commit обязан ОТКАЗАТЬ с rc=3.
# Цена, ради которой это здесь (22.07): запрет жил только словами в каноне,
# Cowork его нарушил, репозиторий дважды вставал на полчаса для всех писателей.
V=$(git show --stat --format= HEAD | grep -c 'novyj-1.md' || true)
[ "$V" = "1" ] && echo "  ✅ на обычной ФС commit работает (запрет не задел своих)" \
               || { echo "  ❌ commit не сработал на обычной ФС — детект песочницы ложно-положительный"; FAIL=1; }

# `if`, а НЕ `cmd; [ $? -eq 0 ]`: при `set -e` ненулевой код убил бы скрипт
# до проверки, и мутация прошла бы незамеченной (поймано мутационным тестом).
if python3 - "$TOOLS/git_zona.py" <<'PY'
import sys, importlib.util, pathlib, types
spec = importlib.util.spec_from_file_location("gz", sys.argv[1])
gz = importlib.util.module_from_spec(spec); spec.loader.exec_module(gz)
# подделываем окружение: репозиторий якобы на fuse-монтировании
fake = "/fake-mount\n"
real_open = open
def fake_open(p, *a, **k):
    if str(p) == "/proc/mounts":
        import io; return io.StringIO(f"dev {gz.REPO} fuse rw 0 0\n")
    return real_open(p, *a, **k)
gz.open = fake_open
import builtins; builtins.open = fake_open
ok = gz.in_sandbox()
builtins.open = real_open
sys.exit(0 if ok else 1)
PY
then echo "  ✅ детект песочницы срабатывает на fuse-монтировании"
else echo "  ❌ ДЕТЕКТ ПЕСОЧНИЦЫ НЕ РАБОТАЕТ — запрет записи мёртв"; FAIL=1
fi

# ── ЛОВУШКА 4: clean не должен трогать СВЕЖИЙ лок ──
# Свежий лок = рядом идёт живой коммит; снести его — испортить чужой индекс.
# Мёртвый (старше 5 мин) — наоборот, обязан уйти, иначе репозиторий стоит.
# ⚠ Возраст файла ставим PYTHON'ом, а не `touch -d '10 minutes ago'`.
# `-d` с человеческим временем — GNU-изм: на macOS BSD-touch его не понимает,
# fallback создавал файл с ТЕКУЩИМ временем, лок считался свежим, и фикстура
# краснела у владельца, оставаясь зелёной в Linux-песочнице.
# ЦЕНА: коммит владельца остановлен хуком на здоровом коде (23.07).
# Правило шире одного места: фикстуры и хуки исполняются НА macOS ВЛАДЕЛЬЦА —
# никаких GNU-измов (`touch -d`, `date -d`, `sed -i`, `xargs -r`, `stat -c`).
python3 -c "import os,sys,time; p=sys.argv[1]; open(p,'w').close(); os.utime(p,(time.time()-600,)*2)" "$T/.git/dead.lock"
touch "$T/.git/fresh.lock"
mkdir -p "$T/.git/objects/ab" && touch "$T/.git/objects/ab/tmp_obj_FIX"
GIT_ZONA_REPO="$T" python3 "$TOOLS/git_zona.py" clean > /dev/null 2>&1 || true
[ ! -f "$T/.git/dead.lock" ] && echo "  ✅ clean снял МЁРТВЫЙ лок" \
                            || { echo "  ❌ мёртвый лок остался — репозиторий будет стоять"; FAIL=1; }
[ -f "$T/.git/fresh.lock" ] && echo "  ✅ clean НЕ тронул свежий лок (там живой коммит)" \
                           || { echo "  ❌ СНЯТ СВЕЖИЙ ЛОК — можно испортить чужой индекс"; FAIL=1; }
[ ! -f "$T/.git/objects/ab/tmp_obj_FIX" ] && echo "  ✅ clean убрал мусорный объект" \
                           || { echo "  ❌ мусор не убран"; FAIL=1; }
rm -f "$T/.git/fresh.lock"

# ── ЛОВУШКА 5: untrack снимает с индекса, но НЕ трогает диск ──
mkdir -p "$T/lib/istochniki"
echo "книга" > "$T/lib/istochniki/kniga.pdf"
git add "lib/istochniki/kniga.pdf" && git commit -qm "книга в индексе"
printf '**/istochniki/**/*.pdf\n' > "$T/.gitignore"
GIT_ZONA_REPO="$T" python3 "$TOOLS/git_zona.py" untrack --yes > /dev/null 2>&1 || true
V=$(git ls-files | grep -c 'kniga.pdf' || true)
[ "$V" = "0" ] && echo "  ✅ untrack снял игнорируемое с индекса" \
              || { echo "  ❌ untrack не сработал — файл остался в индексе"; FAIL=1; }
[ -f "$T/lib/istochniki/kniga.pdf" ] && echo "  ✅ untrack НЕ удалил файл с диска" \
              || { echo "  ❌ ФАЙЛ УДАЛЁН С ДИСКА — untrack обязан только разотслеживать"; FAIL=1; }

# ── ЛОВУШКА 9: однокомандная тропа `commit --zone -m` ──
# Родилась из пяти живых срывов 23.07 (kod_commit-ux.md §2): «сохранить зону»
# было многошаговым и рвалось на каждом стыке. Тропа обязана держать ТЕ ЖЕ
# инварианты, что план-путь: add (новые доезжают), pathspec (чужое staged не
# утаскивается), граница зоны (вне зоны не тронуто). Тропа, обходящая любую
# половину, хуже её отсутствия — она делает обход инвариантов удобным.
echo "чужая работа 2" > CHUZHOJ2.txt
git add CHUZHOJ2.txt
echo "вне зоны" > vne-zony.md
mkdir -p moya-zona
echo "новый тропный" > moya-zona/tropnyj.md
GIT_ZONA_REPO="$T" python3 "$TOOLS/git_zona.py" commit --zone moya-zona -m "тропа: фикстурный прогон" > /dev/null 2>&1 || true

V=$(git show --stat --format= HEAD | grep -c 'tropnyj.md' || true)
[ "$V" = "1" ] && echo "  ✅ тропа -m: новый файл зоны доехал одной командой" \
               || { echo "  ❌ ТРОПА НЕ ДОВЕЗЛА новый файл зоны — add в тропе сломан"; FAIL=1; }

V=$(git show --stat --format= HEAD | grep -c 'CHUZHOJ2' || true)
[ "$V" = "0" ] && echo "  ✅ тропа -m: чужой застейдженный файл НЕ утащен" \
               || { echo "  ❌ ТРОПА УТАЩИЛА ЧУЖОЕ — pathspec в тропе сломан"; FAIL=1; }

V=$(git diff --cached --name-only | grep -c 'CHUZHOJ2' || true)
[ "$V" = "1" ] && echo "  ✅ тропа -m: чужое осталось в индексе нетронутым" \
               || { echo "  ❌ тропа тронула чужой индекс"; FAIL=1; }

V=$(git show --stat --format= HEAD | grep -c 'vne-zony' || true)
[ "$V" = "0" ] && echo "  ✅ тропа -m: файл вне зоны не закоммичен (граница держит)" \
               || { echo "  ❌ ТРОПА ВЫШЛА ЗА ЗОНУ — граница --zone сломана"; FAIL=1; }

[ -z "$(git status --porcelain --untracked-files=all -- moya-zona)" ] \
               && echo "  ✅ тропа -m: зона чиста после одной команды" \
               || { echo "  ❌ зона не чиста после тропы — «одна команда» не довела до конца"; FAIL=1; }

# ── ЛОВУШКА 10: тропа -m не обходит sandbox-отказ ──
# -m — та же пишущая операция; из песочницы обязана отказать (rc=3), как
# план-путь. Обход = Cowork снова коммитер = мины в .git для всех (§2 канона).
# GIT_ZONA_REPO обязателен и здесь: cmd_commit из песочницы логирует инцидент,
# и без него след ушёл бы в БОЕВОЙ INCIDENTY.md.
if GIT_ZONA_REPO="$T" python3 - "$TOOLS/git_zona.py" >/dev/null 2>&1 <<'PY'
import sys, importlib.util, argparse
spec = importlib.util.spec_from_file_location("gz", sys.argv[1])
gz = importlib.util.module_from_spec(spec); spec.loader.exec_module(gz)
gz.in_sandbox = lambda: True                      # песочница «включена»
ns = argparse.Namespace(zone="moya-zona", message="проба", push=False)
sys.exit(0 if gz.cmd_commit(ns) == 3 else 1)
PY
then echo "  ✅ тропа -m из песочницы отказывает (rc=3)"
else echo "  ❌ ТРОПА -m ПИШЕТ ИЗ ПЕСОЧНИЦЫ — sandbox-отказ обойдён"; FAIL=1
fi

# ── ЛОВУШКА 11: неуспешный commit САМ пишется в INCIDENTY ──
# Класс 4 (kod_commit-ux §2b): память об инциденте — поведение инструмента,
# а не дисциплина агента (та живёт ровно один чат и забывается молча).
# Убрал автозапись — эта ловушка красная.
rm -f "$T/_studio/zhurnal/_INFRA-git/INCIDENTY.md"
echo "грязь для инцидента" > moya-zona/grjaz.md
GIT_ZONA_REPO="$T" python3 "$TOOLS/git_zona.py" commit > /dev/null 2>&1 || true   # плана нет, дерево грязное
V=$(grep -c "commit без плана" "$T/_studio/zhurnal/_INFRA-git/INCIDENTY.md" 2>/dev/null || true)
[ "$V" = "1" ] && echo "  ✅ неуспешный commit оставил след в INCIDENTY.md" \
               || { echo "  ❌ СЛЕДА В INCIDENTY НЕТ — класс 4 мёртв, поломки снова забываются"; FAIL=1; }
GIT_ZONA_REPO="$T" python3 "$TOOLS/git_zona.py" commit > /dev/null 2>&1 || true   # тот же симптом повторно
V=$(grep -c "commit без плана" "$T/_studio/zhurnal/_INFRA-git/INCIDENTY.md" 2>/dev/null || true)
[ "$V" = "1" ] && echo "  ✅ повтор того же симптома не задвоился (дедуп за день)" \
               || { echo "  ❌ дедуп INCIDENTY не работает — корзина зашумит, читать бросят"; FAIL=1; }
GIT_ZONA_REPO="$T" python3 "$TOOLS/git_zona.py" commit --zone moya-zona -m "" > /dev/null 2>&1 || true
V=$(grep -c "пустое или плейсхолдер" "$T/_studio/zhurnal/_INFRA-git/INCIDENTY.md" 2>/dev/null || true)
[ "$V" = "1" ] && echo "  ✅ другой класс симптома — отдельная строка (пустое -m)" \
               || { echo "  ❌ пустое -m не залогировано в INCIDENTY"; FAIL=1; }

# ── ЛОВУШКА 8: ❌ на НОРМАЛЬНОМ исходе ──
# `commit` сам удаляет план после успеха; повторный запуск не должен пугать.
# ЦЕНА (23.07): владелец прочитал «❌ Плана нет» как «коммит не сработал» —
# при том что коммит прошёл минутой раньше. Инструмент, печатающий ❌ на
# здоровом исходе, обучает не доверять собственным гейтам.
rm -f "$T/_studio/.commit-plan"
git -C "$T" add -A >/dev/null 2>&1 || true
git -C "$T" commit -qm "чисто перед проверкой" >/dev/null 2>&1 || true
if GIT_ZONA_REPO="$T" python3 "$TOOLS/git_zona.py" commit > /dev/null 2>&1
then echo "  ✅ «плана нет» при чистом дереве — не ошибка (rc=0)"
else echo "  ❌ ❌ НА НОРМАЛЬНОМ ИСХОДЕ: плана нет, дерево чисто, а инструмент краснеет"; FAIL=1
fi

# ── ЛОВУШКА 7: GNU-измы в коде, который исполняется у ВЛАДЕЛЬЦА ──
# Фикстуры и хуки гоняются на macOS (BSD), а пишутся в Linux-песочнице (GNU).
# ЦЕНА (23.07): `touch -d` в этой самой фикстуре остановил здоровый коммит
# владельца — у Cowork было зелено. Гейт, зелёный у автора и красный у
# владельца, хуже отсутствующего.
# Проверка python'ом, а не grep: надо пропускать КОММЕНТАРИИ, иначе гейт
# краснеет на собственном списке запрещённых конструкций (поймано сразу).
if python3 - "$TOOLS" <<'PY'
import re, sys, pathlib
tools = pathlib.Path(sys.argv[1])
# склеиваем из частей, иначе паттерн ловит собственную же строку
bad_re = re.compile("|".join(a + b for a, b in [
    ("touch", " -d"), ("date", " -d"), ("sed", " -i "),
    ("xargs", " -r"), ("stat", " -c"), ("grep", " -P")]))
files = list(tools.glob("fixtures/*/PROGNAT.sh")) + list((tools / ".." / "..").glob(".githooks/*"))
hits = []
for f in files:
    try:
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("#"):
                continue          # комментарий — это документация, не код
            if bad_re.search(line):
                hits.append(f"{f.name}:{n}")
    except OSError:
        pass
print(" ".join(hits))
sys.exit(1 if hits else 0)
PY
then echo "  ✅ GNU-измов в фикстурах и хуках нет (портируемо на macOS)"
else echo "  ❌ GNU-ИЗМ (см. выше) — сломается на macOS владельца"; FAIL=1
fi

# ── ЛОВУШКА 6: канон не отстал от инструмента ──
# Добавили подкоманду и не вписали в дом дисциплины — владелец о ней не узнает,
# а Cowork выдаст вместо неё shell-строчку, которая сломается (§0 канона).
DOC="$TOOLS/../../_studio/docs/kak-delat/GIT-disciplina.md"
if [ -f "$DOC" ]; then
    MISS=""
    for c in $(python3 "$TOOLS/git_zona.py" --help 2>/dev/null \
               | sed -n 's/^ *{\(.*\)}$/\1/p' | tr ',' ' '); do
        grep -q "git_zona.py $c" "$DOC" || MISS="$MISS $c"
    done
    [ -z "$MISS" ] && echo "  ✅ все подкоманды описаны в GIT-disciplina.md" \
                   || { echo "  ❌ В КАНОНЕ НЕТ ПОДКОМАНД:$MISS — владелец о них не узнает"; FAIL=1; }
else
    echo "  ⚠ GIT-disciplina.md не найден рядом — проверку канона пропускаю"
fi

[ "$FAIL" = "0" ] && { echo "ФИКСТУРЫ ЗЕЛЁНЫЕ"; exit 0; } || { echo "ФИКСТУРЫ КРАСНЫЕ"; exit 1; }
