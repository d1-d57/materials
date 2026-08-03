#!/bin/sh
# TOOL-CONTRACT-COVERS: git_zona.py bootstrap_arka.py bootstrap_zahod.py bootstrap_lekcia.py
# ↑ ОХВАТ, а не список авторства: ловушка 14 внизу сторожит validate_slug во ВСЕХ
# трёх bootstrap_*, поэтому правка любого из них обязана поднимать эту фикстуру.
# Пока охват жил в голове автора, хук поднимал её только на правку git_zona.py —
# то есть у гейта триггер был уже его собственного покрытия (ZHURNAL §4.4,
# «остаточный зазор»). Теперь охват объявлен строкой, и её читает хук.
#
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

# 🔴 ЛОВУШКА 16 (СТОРОЖ СОСЕДНИХ ВЕТОК по коммитам, инцидент 2026-07-28) —
# СНЯТА частью B захода `kod_dobivka-vetok.md` ВМЕСТЕ с самим счётным сторожем
# (`print_branch_watch`): на живом репозитории 03.08 сравнение поимённо
# показало, что сторож по СОДЕРЖИМОМУ (ловушка 18 ниже) называет ВСЕ те же
# ветки явно — как потерю или как безопасную с причиной — а счётный давал 43 %
# шума. Правка существующего пути исполнения, названа отдельной строкой в
# отчёте захода. Читать про доказательство инцидента 28.07 — в истории git
# этого файла (коммит, снявший ловушку) и в `_INFRA-git/INCIDENT-2026-07-28…`.

# Слайс блока doctor — сторожа по содержимому (ловушка 18). Нужен потому, что
# doctor печатает внизу строку «Ветки: …» со ВСЕМИ именами — грепом по целому
# выводу проверка «про влитую ветку промолчал» ложно краснела бы на этой строке.
slice_poteri() {
    python3 - "$1" <<'PY'
import sys
out, on = [], False
for line in open(sys.argv[1], encoding="utf-8").read().splitlines():
    if "ЧТО ПРОПАДЁТ" in line:
        on = True
    elif "Последние коммиты" in line:
        on = False
    if on:
        out.append(line)
print("\n".join(out))
PY
}

# ── ЛОВУШКА 17: 🔴 сгенерированный заход НЕСЁТ формат очереди ДОМ/ДОСТАВЛЕНО ──
# Ф1/тираж (kod_tirazh-ocheredi.md часть A): формат вшивается ГЕНЕРАТОРОМ поверх
# РЕАЛЬНОГО `_TEMPLATE-zahod.md` (файл шаблона вне зоны, не трогается) — без
# этой ловушки следующая правка `bootstrap_zahod.py` может тихо вымыть анкор, и
# формат снова перестанет тиражироваться незамеченным. Копируем РЕАЛЬНЫЙ
# генератор и РЕАЛЬНЫЙ шаблон (тот же приём, что fixtures/register_doc/), не
# синтетику — иначе ловушка проверяла бы не то, что реально штампуется.
T17=$(mktemp -d)
trap 'rm -rf "$T" "$T17"' EXIT
mkdir -p "$T17/_generator/tools" "$T17/_studio/zhurnal" "$T17/arka"
cp "$TOOLS/bootstrap_zahod.py" "$TOOLS/register_doc.py" "$TOOLS/check_kartoteka.py" "$T17/_generator/tools/"
cp "$TOOLS/../../_studio/zhurnal/_TEMPLATE-zahod.md" "$T17/_studio/zhurnal/"
cd "$T17"
git init -q .
git config user.email fixture@test
git config user.name fixture
git add -A >/dev/null
git commit -qm baseline >/dev/null
cd - >/dev/null
python3 "$T17/_generator/tools/bootstrap_zahod.py" arka proba17 \
    --branch fixture-branch --zone "moya-zona/" \
    --opisanie "фикстура: заход несёт формат очереди" > /dev/null 2>&1 || true
if [ -f "$T17/arka/kod_proba17.md" ]; then
    V=$(grep -c 'ДОМ:.*ДОСТАВЛЕНО:\|ДОСТАВЛЕНО: нет' "$T17/arka/kod_proba17.md" || true)
    V2=$(grep -c 'ДОСТАВЛЕНО: нет' "$T17/arka/kod_proba17.md" || true)
    [ "$V2" != "0" ] && echo "  ✅ сгенерированный заход несёт формат очереди (ДОМ:/ДОСТАВЛЕНО: на месте)" \
                     || { echo "  ❌ ФОРМАТ ОЧЕРЕДИ ВЫМЫЛСЯ ИЗ ГЕНЕРАЦИИ — тираж снова одноразовый"; FAIL=1; }
else
    echo "  ❌ bootstrap_zahod.py не создал заход — проверить формат очереди нечем"; FAIL=1
fi
rm -rf "$T17"

# ── ЛОВУШКА 18: сторож по СОДЕРЖИМОМУ — «что пропадёт, если удалить ветку» ──
# Сторож по коммитам (ловушка 16) отвечает «сколько не влито». На живом
# репозитории 03.08 это дало 43 % шума: 7 находок из 16 веток, из них ТРИ не
# теряют при удалении ничего (`main` и `arka/vneshnie-istorii` целиком на
# origin, `zahod/tirazh-ocheredi` довезла содержимое через `adopt`).
# ЦЕНА, ради которой ловушка стоит: гейт, кричащий волком на безопасных,
# отключают целиком (`RESHENIYA Р31`) — и тогда пропадает защита и от настоящей
# потери. Здесь держатся ОБЕ половины, и вторая не менее первой:
#   · уникальное содержимое названо опасным, ФАЙЛАМИ (а не числом коммитов);
#   · доехавшее копией названо БЕЗОПАСНЫМ и в опасных не значится.
# Плюс охват на обоих исходах и регрессия на урок 25 (тег-омоним).
T3=$(mktemp -d)
# Выводы кладём ВНЕ рабочего дерева репо: `git add -A` ниже иначе
# закоммитит их в проверяемую ветку, и `adopt` честно назовёт их
# несобранным — ловушка покраснеет на собственном мусоре (поймано сразу).
O3=$(mktemp -d)
trap 'rm -rf "$T" "$T3" "$O3"' EXIT

git init -q "$T3"
git -C "$T3" config user.email fixture@test
git -C "$T3" config user.name fixture
mkdir -p "$T3/zona-a" "$T3/zona-b"
echo "документация v1" > "$T3/zona-a/DOC.md"
echo "код v1" > "$T3/zona-b/CODE.py"
git -C "$T3" add -A >/dev/null 2>&1
git -C "$T3" commit -qm "база"
git -C "$T3" branch -M osnova          # имя ветки по умолчанию разное у версий git

# ветка 1 — УНИКАЛЬНОЕ содержимое: файл, которого нет больше нигде
git -C "$T3" checkout -q -b vetka-uniq
echo "работа, которой нет нигде ещё" > "$T3/zona-a/UNIQ.md"
git -C "$T3" add -A >/dev/null 2>&1
git -C "$T3" commit -qm "уникальная работа"

# ветка 2 — содержимое ДОЕХАЛО копией: имитируем `adopt` дословно —
# `checkout <ветка> -- <зона>` переносит ФАЙЛЫ, историю НЕ сливая. Ветка
# остаётся невлитой НАВСЕГДА, а терять при её удалении нечего.
git -C "$T3" checkout -q osnova
git -C "$T3" checkout -q -b vetka-doehala
echo "эта работа уже перенесена" > "$T3/zona-b/DOEHALO.md"
git -C "$T3" add -A >/dev/null 2>&1
git -C "$T3" commit -qm "работа, которую потом заадоптируют"
git -C "$T3" checkout -q osnova
git -C "$T3" checkout -q vetka-doehala -- zona-b/DOEHALO.md
git -C "$T3" commit -qm "adopt: содержимое ветки без её истории" >/dev/null 2>&1

# ветка 3 — отставшая целиком: стоит на базе, писать ей нечего
git -C "$T3" branch vetka-otstala osnova
# 🔴 тег-омоним ветки — регрессия на урок 25: короткое имя разрешается в ТЕГ
# (refs/tags идут раньше refs/heads), и сторож посчитал бы не ту историю.
git -C "$T3" tag vetka-uniq osnova

GIT_ZONA_REPO="$T3" python3 "$TOOLS/git_zona.py" doctor > "$O3/doctor.txt" 2>&1 || true
slice_poteri "$O3/doctor.txt" > "$O3/poteri.txt"

# Судим РЕЗУЛЬТАТ, а не присутствие имени: `vetka-uniq` встречается и в списке
# безопасных, и в команде лечения, поэтому грубый grep по имени был бы зелёным
# на сломанном сторóже (дважды оплаченное правило, урок 25).
V=$(grep -c '· vetka-uniq — пропадёт файлов: 1' "$O3/poteri.txt" || true)
[ "$V" = "1" ] && echo "  ✅ содержимое: уникальная ветка названа ОПАСНОЙ (и тег-омоним её не заглушил)" \
               || { echo "  ❌ УНИКАЛЬНАЯ РАБОТА НЕ НАЙДЕНА — сторож по содержимому мёртв (либо короткое имя ветки вместо refs/heads/)"; FAIL=1; }

V=$(grep -c 'zona-a/UNIQ.md' "$O3/poteri.txt" || true)
[ "$V" -ge 1 ] && echo "  ✅ содержимое: назван ФАЙЛ, который пропадёт (а не число коммитов)" \
               || { echo "  ❌ файл не назван — «что-то не влито» лечением не является"; FAIL=1; }

# 🔴 ГЛАВНАЯ ПОЛОВИНА: доехавшая копией ветка обязана быть названа безопасной
# ЯВНО и отсутствовать в опасных. Иначе список опасных тонет в шуме.
V=$(grep -c 'содержимое ДОЕХАЛО, хотя история не влита: .*vetka-doehala' "$O3/poteri.txt" || true)
[ "$V" = "1" ] && echo "  ✅ содержимое: доехавшая копией ветка названа БЕЗОПАСНОЙ явно" \
               || { echo "  ❌ ШУМ НА ЗДОРОВОМ: работа доехала через adopt, а ветка не названа безопасной — такой гейт отключат"; FAIL=1; }
V=$(grep -c '· vetka-doehala — пропадёт файлов\|· vetka-doehala — файлов' "$O3/poteri.txt" || true)
[ "$V" = "0" ] && echo "  ✅ содержимое: доехавшей ветки НЕТ в списках опасных и расходящихся" \
               || { echo "  ❌ доехавшая ветка попала в опасные — наивная метрика вернулась"; FAIL=1; }

# ОХВАТ = числу существующих веток минус текущая. Веток 4 (osnova, vetka-uniq,
# vetka-doehala, vetka-otstala), текущая osnova ⇒ 3 из 3.
V=$(grep -c 'Охват: проверено 3 из 3' "$O3/poteri.txt" || true)
[ "$V" = "1" ] && echo "  ✅ содержимое: охват объявлен и равен числу существующих веток (3 из 3)" \
               || { echo "  ❌ ОХВАТ НЕ ОБЪЯВЛЕН ИЛИ НЕВЕРЕН — «нашёл на одной» и «смотрел одну» неразличимы"; FAIL=1; }

# READ-ONLY: диагност не смеет брать лок и двигать индекс.
[ ! -f "$T3/.git/index.lock" ] && echo "  ✅ содержимое: сторож не оставил index.lock" \
               || { echo "  ❌ СТОРОЖ ПО СОДЕРЖИМОМУ ВЗЯЛ index.lock — уронит чужой коммит"; FAIL=1; }

git -C "$T3" tag -d vetka-uniq > /dev/null 2>&1 || true

# ── ЛОВУШКА 19: `adopt` называет, чего он НЕ забрал ──
# Урок 20 арки 2026-07-30: перенос по путям привёз документацию БЕЗ кода —
# четыре гейта и хук месяц числились существующими. Ничто не краснело: гейт
# «работа доехала в git» судит рабочее дерево, а файлы там на месте, просто
# версия старее. adopt обязан назвать зоны, оставшиеся на ветке. Убрал печать —
# ловушка красная.
git -C "$T3" checkout -q osnova
git -C "$T3" checkout -q -b vetka-dvuzonnaya
echo "описание гейта" > "$T3/zona-a/GEJTY.md"
mkdir -p "$T3/zona-b"
echo "реализация гейта" > "$T3/zona-b/gejt.py"
git -C "$T3" add -A >/dev/null 2>&1
git -C "$T3" commit -qm "описание в zona-a, реализация в zona-b"
git -C "$T3" checkout -q osnova
GIT_ZONA_REPO="$T3" python3 "$TOOLS/git_zona.py" adopt --branch vetka-dvuzonnaya \
    --zone zona-a > "$O3/adopt.txt" 2>&1 || true
V=$(grep -c 'ВНЕ зоны `zona-a` ветка `vetka-dvuzonnaya` расходится ещё в 1 путях' "$O3/adopt.txt" || true)
[ "$V" = "1" ] && echo "  ✅ adopt называет, что осталось на ветке ВНЕ зоны" \
               || { echo "  ❌ ADOPT МОЛЧИТ ПРО НЕСОБРАННОЕ — документация приедет без кода (урок 20)"; FAIL=1; }
V=$(grep -c 'zona-b' "$O3/adopt.txt" || true)
[ "$V" -ge 1 ] && echo "  ✅ adopt называет ЗОНУ несобранного поимённо" \
               || { echo "  ❌ зона несобранного не названа — «что-то осталось» не лечится"; FAIL=1; }
# И не сломал предпросмотр: без --yes adopt НИЧЕГО не переносит.
[ ! -f "$T3/zona-a/GEJTY.md" ] && echo "  ✅ adopt без --yes остался предпросмотром (ничего не перенёс)" \
               || { echo "  ❌ ADOPT ПЕРЕНЁС БЕЗ --yes — предпросмотр перестал быть предпросмотром"; FAIL=1; }

# ── ЛОВУШКА 20: две дыры, найденные ВЕРИФИКАТОРОМ захода 03.08 ──
# Обе про одно: метрика мерила отношение «ветка ↔ текущее окно» вместо
# «ветка ↔ весь репозиторий», и обе — регулярные, а не искусственные.
#   20а. МОЛЧАНИЕ ПРИ ЖИВОЙ ПОТЕРЕ. `adopt` сам кладёт файлы ветки в НАШ коммит,
#        после чего путь навсегда числится «нашим» — и любая ПОСЛЕДУЮЩАЯ работа
#        ветки над этим файлом уходила в не-красное «расхождение без потери».
#        То есть сторож глох ровно на тех ветках, с которыми работали активнее
#        всего: adopt зоны — обычный шаг, а не редкость.
#   20б. ТРЕВОГА НА ПУСТОМ МЕСТЕ. Работу могли заадоптить на СОСЕДНЮЮ ветку, а
#        вопрос задаётся из третьего worktree — сравнение только с HEAD красило
#        безопасную ветку. Красный, который врёт, отключают вместе с настоящим.
T4=$(mktemp -d); O4=$(mktemp -d)
trap 'rm -rf "$T" "$T3" "$O3" "$T4" "$O4"' EXIT
git init -q "$T4"
git -C "$T4" config user.email fixture@test
git -C "$T4" config user.name fixture
mkdir -p "$T4/zona"
echo "база" > "$T4/zona/a.txt"
git -C "$T4" add -A >/dev/null 2>&1; git -C "$T4" commit -qm "база"
git -C "$T4" branch -M osnova

# 20а: ветка написала v1 → мы её заадоптили → ветка поехала дальше в v2
git -C "$T4" checkout -q -b vetka-posle-adopt
echo "черновик v1" > "$T4/zona/a.txt"
git -C "$T4" commit -qam "ветка: v1" >/dev/null
git -C "$T4" checkout -q osnova
git -C "$T4" checkout -q vetka-posle-adopt -- zona/a.txt
git -C "$T4" commit -qm "adopt зоны с ветки" >/dev/null
git -C "$T4" checkout -q vetka-posle-adopt
echo "переписанный раздел, есть только здесь" > "$T4/zona/a.txt"
git -C "$T4" commit -qam "ветка: v2 после адопта" >/dev/null

# 20б: работа ветки заадоптлена на СОСЕДНЮЮ ветку, стоим на третьей
git -C "$T4" checkout -q osnova
git -C "$T4" checkout -q -b vetka-slides
mkdir -p "$T4/zona-c"; echo "готовый дек" > "$T4/zona-c/deck.html"
git -C "$T4" add -A >/dev/null 2>&1; git -C "$T4" commit -qm "slides: дек"
git -C "$T4" checkout -q -b vetka-sosed osnova
git -C "$T4" checkout -q vetka-slides -- zona-c/deck.html
git -C "$T4" commit -qm "сосед: adopt дека" >/dev/null

git -C "$T4" checkout -q osnova
GIT_ZONA_REPO="$T4" python3 "$TOOLS/git_zona.py" doctor > "$O4/doctor.txt" 2>&1 || true
slice_poteri "$O4/doctor.txt" > "$O4/poteri.txt"

V=$(grep -c '· vetka-posle-adopt — пропадёт файлов: 1' "$O4/poteri.txt" || true)
[ "$V" = "1" ] && echo "  ✅ 20а: работа ветки ПОСЛЕ адопта названа потерей (путь «наш», текст — нет)" \
               || { echo "  ❌ МОЛЧАНИЕ ПРИ ЖИВОЙ ПОТЕРЕ: после adopt любая работа ветки уходит в не-красное"; FAIL=1; }
V=$(grep -c 'писали обе стороны — версия ветки здесь отсутствует' "$O4/poteri.txt" || true)
[ "$V" -ge 1 ] && echo "  ✅ 20а: сказано, ЧТО именно пропадёт — версия ветки, и что сливать глазами" \
               || { echo "  ❌ «расхождение» снова объявлено не-потерей"; FAIL=1; }

V=$(grep -c 'содержимое ДОЕХАЛО, хотя история не влита: .*vetka-slides' "$O4/poteri.txt" || true)
[ "$V" = "1" ] && echo "  ✅ 20б: работа, заадоптленная на СОСЕДНЮЮ ветку, признана доехавшей" \
               || { echo "  ❌ ТРЕВОГА НА ПУСТОМ МЕСТЕ: содержимое лежит на соседней ветке, а сторож красит"; FAIL=1; }
V=$(grep -c '· vetka-slides — пропадёт файлов' "$O4/poteri.txt" || true)
[ "$V" = "0" ] && echo "  ✅ 20б: и в опасных её нет" \
               || { echo "  ❌ vetka-slides в опасных — сравнение всё ещё только с HEAD"; FAIL=1; }

# Гарантия «держит origin/*» слабее локальной — названа отдельной строкой.
V=$(grep -c 'сверялись ВЕРШИНЫ веток' "$O4/poteri.txt" || true)
[ "$V" -ge 1 ] && echo "  ✅ слепая зона «сверяются вершины» ОБЪЯВЛЕНА, а не умолчана" \
               || { echo "  ❌ зелёное молчит про свою границу — читается шире, чем оно есть"; FAIL=1; }

# 20в: уровень 2 (сверка с НАШИМ деревом) пришпилен отдельно — в detached HEAD.
# Пока HEAD стоит на ветке, его дерево видно и через ссылку, и проверка «блоб
# лежит на соседней ветке» (20б) закрывает тот же случай, то есть уровень 2
# становится ненаблюдаемым — а гейт, который не умеет падать, это театр.
# В detached HEAD ссылки на текущее дерево НЕТ ⇒ работу, доехавшую сюда,
# признаёт доехавшей ТОЛЬКО уровень 2. Убери его — эта строка красная.
git -C "$T4" checkout -q --detach osnova
git -C "$T4" checkout -q vetka-posle-adopt -- zona/a.txt
git -C "$T4" commit -qm "detached: работа ветки доехала в текущее дерево" >/dev/null 2>&1
GIT_ZONA_REPO="$T4" python3 "$TOOLS/git_zona.py" doctor > "$O4/doctor-det.txt" 2>&1 || true
slice_poteri "$O4/doctor-det.txt" > "$O4/poteri-det.txt"
V=$(grep -c 'содержимое ДОЕХАЛО, хотя история не влита: .*vetka-posle-adopt' "$O4/poteri-det.txt" || true)
[ "$V" = "1" ] && echo "  ✅ 20в: в detached HEAD доехавшее в ДЕРЕВО признано доехавшим (уровень 2 жив)" \
               || { echo "  ❌ УРОВЕНЬ 2 МЁРТВ: работа доехала в текущее дерево, а сторож красит"; FAIL=1; }

# ── ЛОВУШКА 21: лок в ЛИЧНОМ каталоге worktree — `doctor` из этой папки ВИДИТ ──
# Часть A захода `kod_dobivka-vetok.md`. `.git` рабочей папки worktree — ФАЙЛ-
# указатель на `<основной>/.git/worktrees/<имя>`, и старый код читал `REPO/".git"`
# как каталог — там локи не находились НИКОГДА. ЦЕНА: настоящий лок, положенный
# туда живым прогоном 03.08, дал «Локи в .git: ✅ свободно» — защита от гонки
# отсутствовала ровно там, где заведён параллелизм (`GIT-disciplina §4`).
T5=$(mktemp -d); O5=$(mktemp -d)
trap 'rm -rf "$T" "$T3" "$O3" "$T4" "$O4" "$T5" "$O5"' EXIT
git init -q "$T5"
git -C "$T5" config user.email fixture@test
git -C "$T5" config user.name fixture
echo "база" > "$T5/f.txt"
git -C "$T5" add -A >/dev/null 2>&1; git -C "$T5" commit -qm "база"
git -C "$T5" branch -M osnova
WT5="$T5-wt"
git -C "$T5" worktree add -q -b feature-x "$WT5" >/dev/null 2>&1
GD5=$(git -C "$WT5" rev-parse --git-dir)
touch "$GD5/proba.lock"
GIT_ZONA_REPO="$WT5" python3 "$TOOLS/git_zona.py" doctor > "$O5/doctor.txt" 2>&1 || true
V=$(grep -c 'ЛОКИ в .git' "$O5/doctor.txt" || true)
[ "$V" = "1" ] && echo "  ✅ часть A: doctor ИЗ РАБОЧЕЙ ПАПКИ worktree видит лок в её личном каталоге" \
               || { echo "  ❌ ЧАСТЬ A СЛОМАНА: лок в .git/worktrees/<имя>/ не найден — гонка снова невидима"; FAIL=1; }
V=$(grep -c 'proba.lock' "$O5/doctor.txt" || true)
[ "$V" -ge 1 ] && echo "  ✅ часть A: лок назван ПОЛНЫМ путём (personal git-dir вне рабочей папки)" \
               || { echo "  ❌ путь лока не назван — печать сломана на personal git-dir"; FAIL=1; }
rm -f "$GD5/proba.lock"
git -C "$T5" worktree remove --force "$WT5" >/dev/null 2>&1 || true

# ── ЛОВУШКА 22: `bootstrap_zahod.py --worktree` кладёт файл-заход В ОСНОВНУЮ
# папку, В ОДНОМ ЭКЗЕМПЛЯРЕ, а worktree заводит ТОЛЬКО для кода ──
# Часть D захода `kod_dobivka-vetok.md`, регрессия на урок 23. ЦЕНА (до починки):
# файл рождался ТОЛЬКО в рабочей папке — исполнитель, отправленный контрактом в
# основную (там ПЛАН/ВОПРОСЫ/ОТЧЁТ), не находил там ничего.
T22=$(mktemp -d)
trap 'rm -rf "$T" "$T3" "$O3" "$T4" "$O4" "$T5" "$O5" "$T22"' EXIT
mkdir -p "$T22/_generator/tools" "$T22/_studio/zhurnal/proba22"
cp "$TOOLS/bootstrap_zahod.py" "$TOOLS/git_zona.py" "$TOOLS/register_doc.py" "$TOOLS/check_kartoteka.py" "$T22/_generator/tools/"
cp "$TOOLS/../../_studio/zhurnal/_TEMPLATE-zahod.md" "$T22/_studio/zhurnal/"
cd "$T22"
git init -q .
git config user.email fixture@test
git config user.name fixture
git add -A >/dev/null; git commit -qm baseline >/dev/null
cd - >/dev/null
python3 "$T22/_generator/tools/bootstrap_zahod.py" _studio/zhurnal/proba22 proba22t \
    --branch fixture-branch22 --zone "_studio/zhurnal/proba22/" --worktree proba22wt \
    --opisanie "фикстура: файл в основной, worktree для кода" > /dev/null 2>&1 || true
[ -f "$T22/_studio/zhurnal/proba22/kod_proba22t.md" ] \
    && echo "  ✅ часть D: файл-заход создан В ОСНОВНОЙ папке (--worktree задан)" \
    || { echo "  ❌ ЧАСТЬ D СЛОМАНА: файла-захода в основной папке нет — урок 23 вернулся"; FAIL=1; }
[ ! -f "$T22-wt/proba22wt/_studio/zhurnal/proba22/kod_proba22t.md" ] \
    && echo "  ✅ часть D: файла НЕТ в рабочей папке (одна копия, не тень)" \
    || { echo "  ❌ ДВОЙНАЯ КОПИЯ: файл рождается ещё и в worktree — та самая тень из урока 2026-07-23"; FAIL=1; }
[ -d "$T22-wt/proba22wt" ] \
    && echo "  ✅ часть D: рабочая папка для КОДА всё равно заведена" \
    || { echo "  ❌ worktree не заведён — --worktree перестал заводить папку для кода"; FAIL=1; }

# ── ЛОВУШКА 23: `poteri` — read-only подкоманда, печатает ОХВАТ ──
# Часть C захода `kod_dobivka-vetok.md`. Держится тем же прогоном, что T3 выше
# (ловушка 18: uniq/doehala/otstala), только через отдельную подкоманду, а не
# через `doctor` — это и есть разница между «блок в doctor» и «команда poteri».
RC_POTERI=0
GIT_ZONA_REPO="$T3" python3 "$TOOLS/git_zona.py" poteri > "$O3/poteri-cmd.txt" 2>&1 || RC_POTERI=$?
V=$(grep -c 'Охват: проверено 4 из 4' "$O3/poteri-cmd.txt" || true)
[ "$V" = "1" ] && echo "  ✅ часть C: poteri (без --branch) печатает охват (4 из 4, после ловушки 19)" \
               || { echo "  ❌ ОХВАТ НЕ ОБЪЯВЛЕН — poteri не несёт гарантию «смотрел всё»"; FAIL=1; }
V=$(grep -c '· vetka-uniq — пропадёт файлов: 1' "$O3/poteri-cmd.txt" || true)
[ "$V" = "1" ] && echo "  ✅ часть C: poteri находит ту же уникальную работу, что и блок в doctor" \
               || { echo "  ❌ poteri разъехался с doctor — два входа судят по-разному"; FAIL=1; }
[ "$RC_POTERI" = "1" ] && echo "  ✅ часть C: poteri вернул rc=1 — реальная потеря есть" \
               || { echo "  ❌ КОД ВОЗВРАТА poteri НЕ СИГНАЛИТ О ПОТЕРЕ (rc=$RC_POTERI, ожидался 1)"; FAIL=1; }
# read-only и по одной ветке — доехавшая ветка, вызов с --branch
RC_BRANCH=0
GIT_ZONA_REPO="$T3" python3 "$TOOLS/git_zona.py" poteri --branch vetka-doehala > "$O3/poteri-branch.txt" 2>&1 || RC_BRANCH=$?
V=$(grep -c 'проверено 1 из 1' "$O3/poteri-branch.txt" || true)
[ "$V" -ge 1 ] && echo "  ✅ часть C: poteri --branch судит РОВНО одну ветку (охват 1 из 1)" \
               || { echo "  ❌ poteri --branch не сузил проверку до одной ветки"; FAIL=1; }
[ "$RC_BRANCH" = "0" ] && echo "  ✅ часть C: poteri --branch на безопасной ветке — rc=0" \
               || { echo "  ❌ poteri --branch на безопасной ветке дал rc=$RC_BRANCH, ожидался 0"; FAIL=1; }
GIT_ZONA_REPO="$T3" python3 "$TOOLS/git_zona.py" poteri --branch net-takoj-vetki > "$O3/poteri-bad.txt" 2>&1 && G=bad || G=ok
{ [ "$G" = "ok" ]; } && grep -q 'нет среди' "$O3/poteri-bad.txt" \
    && echo "  ✅ часть C: poteri --branch на несуществующей ветке отказывает громко" \
    || { echo "  ❌ poteri --branch молча проглотил несуществующую ветку"; FAIL=1; }

# ── ЛОВУШКА 24: унаследованный GIT_DIR НЕ уводит `doctor` на чужой worktree ──
# Найдено ВЕРИФИКАТОРОМ части A (заход 2026-08-03): `git rev-parse --git-dir`
# следует переменной `GIT_DIR` из окружения БЕЗУСЛОВНО, `cwd` игнорируется
# целиком. Если процесс, которым запущен `git_zona.py`, унаследовал `GIT_DIR`
# (утечка из git-хука, обёртки, забытый `export`) — `git_dir()` без чистки
# окружения тихо указал бы на ЧУЖУЮ рабочую копию, и `find_locks()` отчитался
# бы «свободно», проверив не тот каталог. Ровно тот класс, что уже назван в
# докстроке `git_zona.py` и в ловушке-первом-ходе этой самой фикстуры выше
# («ОБЯЗАТЕЛЬНО ПЕРВЫМ ХОДОМ: вычистить окружение git») — но там чистится
# окружение ФИКСТУРЫ, а не каждого вызова `git()` внутри инструмента.
T6=$(mktemp -d)
trap 'rm -rf "$T" "$T3" "$O3" "$T4" "$O4" "$T5" "$O5" "$T22" "$T6"' EXIT
git init -q "$T6"
git -C "$T6" config user.email fixture@test
git -C "$T6" config user.name fixture
echo "база" > "$T6/f.txt"
git -C "$T6" add -A >/dev/null 2>&1; git -C "$T6" commit -qm "база"
git -C "$T6" branch -M osnova
git -C "$T6" worktree add -q -b wtA "$T6-wtA" >/dev/null 2>&1
git -C "$T6" worktree add -q -b wtB "$T6-wtB" >/dev/null 2>&1
GDA=$(git -C "$T6-wtA" rev-parse --git-dir)
GDB=$(git -C "$T6-wtB" rev-parse --git-dir)
touch "$GDA/svoj.lock"
# GIT_DIR подделан на СОСЕДНИЙ worktree — doctor должен ИГНОРИРОВАТЬ подделку
# и всё равно проверить СВОЙ (wtA) каталог, потому что запущен GIT_ZONA_REPO=wtA.
GIT_DIR="$GDB" GIT_ZONA_REPO="$T6-wtA" python3 "$TOOLS/git_zona.py" doctor \
    > "$T6/doctor-git-dir.txt" 2>&1 || true
V=$(grep -c 'svoj.lock' "$T6/doctor-git-dir.txt" || true)
[ "$V" -ge 1 ] && echo "  ✅ часть A: унаследованный GIT_DIR НЕ уводит doctor от своего лока" \
               || { echo "  ❌ ПОДДЕЛКА GIT_DIR СРАБОТАЛА — doctor проверил чужой worktree, свой лок не видит"; FAIL=1; }
V=$(grep -c "$GDB" "$T6/doctor-git-dir.txt" || true)
[ "$V" = "0" ] && echo "  ✅ часть A: doctor не смотрит на подделанный (чужой) git-dir вовсе" \
               || { echo "  ❌ doctor смотрит на путь из подделанного GIT_DIR, а не на свой"; FAIL=1; }

[ "$FAIL" = "0" ] && { echo "ФИКСТУРЫ ЗЕЛЁНЫЕ"; exit 0; } || { echo "ФИКСТУРЫ КРАСНЫЕ"; exit 1; }
