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

# ── ЛОВУШКА 15: --no-verify обходит хук, но НЕ МОЛЧА ──
# Урок 9: чужой красный гейт останавливал работу целиком — голого
# `git commit --no-verify` в этом репо нет, весь git идёт через инструмент.
# Флаг заведён вместе с тем, что краснеет при злоупотреблении: обход САМ
# пишется в INCIDENTY. Обе половины обязательны и проверены порознь —
# «коммит прошёл» без следа означал бы тихий обход гейтов, то есть их конец.
mkdir -p "$T/krasnyj-hook"
cat > "$T/krasnyj-hook/pre-commit" <<'HOOK'
#!/bin/sh
echo "❌ фикстурный красный гейт"; exit 1
HOOK
chmod +x "$T/krasnyj-hook/pre-commit"
git -C "$T" config core.hooksPath "$T/krasnyj-hook"
mkdir -p "$T/moya-zona"
echo "под красным хуком" > "$T/moya-zona/pod-krasnym.md"

GIT_ZONA_REPO="$T" python3 "$TOOLS/git_zona.py" commit --zone moya-zona \
    -m "зона: коммит под чужим красным гейтом" > /dev/null 2>&1 || true
V=$(git -C "$T" show --stat --format= HEAD | grep -c 'pod-krasnym' || true)
[ "$V" = "0" ] && echo "  ✅ без флага красный хук коммит ОСТАНАВЛИВАЕТ (гейт жив)" \
               || { echo "  ❌ красный pre-commit не остановил коммит — гейт мёртв"; FAIL=1; }

# Голый флаг БЕЗ причины обязан отказать: обход, у которого не названо, что
# обходят, ничем не отличается от тихого (урок 9 требует причину строкой).
GIT_ZONA_REPO="$T" python3 "$TOOLS/git_zona.py" commit --zone moya-zona --no-verify \
    -m "зона: коммит под чужим красным гейтом" > /dev/null 2>&1 || true
V=$(git -C "$T" show --stat --format= HEAD | grep -c 'pod-krasnym' || true)
[ "$V" = "0" ] && echo "  ✅ --no-verify БЕЗ причины отказал (обход без причины = тихий)" \
               || { echo "  ❌ --no-verify без причины провёз коммит — обход снова тихий"; FAIL=1; }

GIT_ZONA_REPO="$T" python3 "$TOOLS/git_zona.py" commit --zone moya-zona \
    --no-verify "чужой долг: фикстурный красный гейт" \
    -m "зона: коммит под чужим красным гейтом" > /dev/null 2>&1 || true
V=$(git -C "$T" show --stat --format= HEAD | grep -c 'pod-krasnym' || true)
[ "$V" = "1" ] && echo "  ✅ --no-verify с причиной провёз зону мимо ЧУЖОГО красного гейта" \
               || { echo "  ❌ --no-verify не сработал — урок 9 не закрыт, работа встаёт"; FAIL=1; }

V=$(grep -c "чужой долг: фикстурный красный гейт" \
        "$T/_studio/zhurnal/_INFRA-git/INCIDENTY.md" 2>/dev/null || true)
[ "$V" = "1" ] && echo "  ✅ обход САМ записал в INCIDENTY.md ПРИЧИНУ, а не факт обхода" \
               || { echo "  ❌ ТИХИЙ ОБХОД ГЕЙТА: причина --no-verify не попала в INCIDENTY"; FAIL=1; }

git -C "$T" config --unset core.hooksPath

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

# ── ЛОВУШКА 12: plan КАРАНТИНИТ untracked-мусор с ведущим `-` ──
# Инцидент 23.07: `bootstrap_arka.py --help` создал `_studio/zhurnal/--help/`,
# и каждый plan тянул её в черновик — кто-то вручную выцеплял мусор из плана.
# plan обязан НЕ класть такой путь в .commit-plan и вынести его отдельным блоком.
# Убрал карантин (is_suspect всегда ложь) — мусор снова в плане, ловушка красная.
mkdir -p "$T/karantin-zona"
echo "настоящая работа" > "$T/karantin-zona/real.md"
mkdir -- "$T/--help"; echo "мусор" > "$T/--help/NAVIGATOR.md"
rm -f "$T/_studio/.commit-plan"
GIT_ZONA_REPO="$T" python3 "$TOOLS/git_zona.py" plan > /dev/null 2>&1 || true
V=$(grep -c -- '--help' "$T/_studio/.commit-plan" 2>/dev/null || true)
[ "$V" = "0" ] && echo "  ✅ карантин: мусор с ведущим '-' НЕ попал в черновик плана" \
               || { echo "  ❌ МУСОР ПРОСОЧИЛСЯ В ПЛАН — карантин мёртв"; FAIL=1; }
V=$(grep -c 'karantin-zona/real.md' "$T/_studio/.commit-plan" 2>/dev/null || true)
[ "$V" = "1" ] && echo "  ✅ карантин: настоящая работа осталась в плане" \
               || { echo "  ❌ карантин съел настоящую работу"; FAIL=1; }

# ── ЛОВУШКА 13: purge снимает ТОЛЬКО untracked-мусор ──
# Удаление лоссово: purge обязан снять названный untracked-мусор и НЕ тронуть
# ни отслеживаемое (работа), ни НЕ-названную живую untracked-работу; из
# песочницы — отказать (rc=3), как commit. Каждая половина проверена мутацией.
echo "работа" > "$T/keep-tracked.md"
git -C "$T" add keep-tracked.md && git -C "$T" commit -qm tracked >/dev/null 2>&1 || true
echo "живое" > "$T/live-untracked.md"     # НЕ-названная (без дефиса) — карантин её не берёт
GIT_ZONA_REPO="$T" python3 "$TOOLS/git_zona.py" purge --yes > /dev/null 2>&1 || true
[ ! -e "$T/--help" ] && echo "  ✅ purge снял названный untracked-мусор (--help/)" \
                     || { echo "  ❌ purge НЕ снял мусор"; FAIL=1; }
[ -f "$T/keep-tracked.md" ] && echo "  ✅ purge НЕ тронул ОТСЛЕЖИВАЕМЫЙ файл" \
                     || { echo "  ❌ PURGE УДАЛИЛ ОТСЛЕЖИВАЕМОЕ — работа потеряна"; FAIL=1; }
[ -f "$T/live-untracked.md" ] && echo "  ✅ purge НЕ тронул НЕ-названную untracked-работу" \
                     || { echo "  ❌ PURGE СНЁС НЕ-НАЗВАННУЮ ЖИВУЮ РАБОТУ"; FAIL=1; }
# явный путь к отслеживаемому — purge обязан ОТКАЗАТЬ (rc≠0) и файл сохранить
GIT_ZONA_REPO="$T" python3 "$TOOLS/git_zona.py" purge --yes keep-tracked.md >/dev/null 2>&1 && G=bad || G=ok
{ [ "$G" = "ok" ] && [ -f "$T/keep-tracked.md" ]; } \
    && echo "  ✅ purge отказал снять отслеживаемое по явному пути (файл цел)" \
    || { echo "  ❌ PURGE СНЁС ОТСЛЕЖИВАЕМОЕ ПО ЯВНОМУ ПУТИ"; FAIL=1; }
# из песочницы — отказ rc=3 (нужна живая цель, иначе выход раньше на «нечего снимать»)
mkdir -- "$T/--sbx"; echo m > "$T/--sbx/f.md"
if GIT_ZONA_REPO="$T" python3 - "$TOOLS/git_zona.py" >/dev/null 2>&1 <<'PY'
import sys, importlib.util, argparse
spec = importlib.util.spec_from_file_location("gz", sys.argv[1])
gz = importlib.util.module_from_spec(spec); spec.loader.exec_module(gz)
gz.in_sandbox = lambda: True
sys.exit(0 if gz.cmd_purge(argparse.Namespace(paths=["--sbx"], yes=True)) == 3 else 1)
PY
then echo "  ✅ purge из песочницы отказывает (rc=3)"
else echo "  ❌ PURGE ПИШЕТ ИЗ ПЕСОЧНИЦЫ — sandbox-отказ обойдён"; FAIL=1
fi
[ -e "$T/--sbx" ] && echo "  ✅ purge из песочницы ничего не удалил" \
                  || { echo "  ❌ purge из песочницы всё же удалил цель"; FAIL=1; }

# ── ЛОВУШКА 14: bootstrap_* отвергают имя-флаг/кривой слаг, НИЧЕГО не создав ──
# Инцидент 23.07: `bootstrap_arka.py --help` проглотил флаг как имя арки и создал
# папку-сироту. validate_slug обязан упасть SystemExit'ом ДО любой записи на диск.
# Модули держатся на ВРЕМЕННЫХ каталогах — гейт не смеет писать в боевой репо
# (урок 1.7): даже при снятой валидации артефакт уйдёт в /tmp, не в materials/.
# Убрал validate_slug — кривое имя рождает папку/файл, ловушка красная.
if python3 - "$TOOLS" <<'PY'
import sys, importlib.util, tempfile, pathlib, shutil
tools = pathlib.Path(sys.argv[1])
def load(n):
    s = importlib.util.spec_from_file_location(n, tools / f"{n}.py")
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
fails = []
def born(call, art):
    """call() кривого имени НЕ должен родить art. Способ падения не важен
    (SystemExit/иное) — важно, что артефакт не создан."""
    try: call()
    except BaseException: pass
    return art.exists()

# arka: сырой argv[0] — худший корень. Валидный шаблон, чтобы единственным
# стопом была валидация имени (иначе «шаблон не найден» дал бы ложь-зелёный).
arka = load("bootstrap_arka")
t = pathlib.Path(tempfile.mkdtemp())
(t / "_TPL").mkdir(); (t / "_TPL" / "X.md").write_text("{{ИМЯ}}", encoding="utf-8")
arka.TEMPLATE_DIR = t / "_TPL"; arka.ZHURNAL_DIR = t
for bad in ["--help", "-x", "bad/slug"]:
    if born(lambda b=bad: arka.main([b]), t / bad):
        fails.append(f"arka пропустил кривое имя «{bad}»")
if not born(lambda: arka.main(["2026-07-23_proba"]), t / "2026-07-23_proba"):
    fails.append("arka отверг ВАЛИДНОЕ имя — валидация переужесточена")
shutil.rmtree(t, ignore_errors=True)

# zahod: tema → kod_<tema>.md. argparse отбивает '-x' сам, поэтому мутационно-
# чувствительны пустое/со слэшем/с ведущей точкой — их ловит только validate_slug.
zahod = load("bootstrap_zahod")
t = pathlib.Path(tempfile.mkdtemp())
tpl = t / "_TPL.md"
tpl.write_text("{{ТЕМА}}{{МОДЕЛЬ}}{{ВЕТКА}}{{ЗОНА}}{{КОНТРАКТ_МЕСТО}}{{ПЕРВЫЙ_ХОД}}", encoding="utf-8")
zahod.TEMPLATE = tpl
ad = t / "arka"; ad.mkdir()
for bad in ["", "a/b", ".hidden"]:
    if born(lambda b=bad: zahod.main([str(ad), b, "--branch", "b", "--zone", "z/"]),
            ad / f"kod_{bad}.md"):
        fails.append(f"zahod пропустил кривую тему «{bad}»")
shutil.rmtree(t, ignore_errors=True)

# lekcia: main() читает sys.argv; имя = target.name. Путь с ведущим '-'/точкой
# в последнем компоненте argparse пропускает (это не флаг), ловит validate_slug.
lek = load("bootstrap_lekcia")
t = pathlib.Path(tempfile.mkdtemp())
for nm in ["-bad", ".hidden"]:
    art = t / nm
    sys.argv = ["prog", str(art)]
    if born(lambda: lek.main(), art):
        fails.append(f"lekcia пропустила кривое имя «{nm}»")
good = t / "moya-lekcia"; sys.argv = ["prog", str(good)]
try: lek.main()
except BaseException: pass
if not good.exists():
    fails.append("lekcia отвергла ВАЛИДНОЕ имя — валидация переужесточена")
shutil.rmtree(t, ignore_errors=True)

for f in fails: print("   -", f)
sys.exit(1 if fails else 0)
PY
then echo "  ✅ bootstrap_* отвергают имя-флаг/кривой слаг, ничего не создав (arka/zahod/lekcia)"
else echo "  ❌ BOOTSTRAP ПРОГЛОТИЛ КРИВОЕ ИМЯ (см. выше) — validate_slug мёртв"; FAIL=1
fi

[ "$FAIL" = "0" ] && { echo "ФИКСТУРЫ ЗЕЛЁНЫЕ"; exit 0; } || { echo "ФИКСТУРЫ КРАСНЫЕ"; exit 1; }
