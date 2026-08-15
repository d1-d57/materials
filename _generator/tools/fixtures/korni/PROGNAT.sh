#!/bin/sh
# TOOL-CONTRACT-COVERS: korni.py check_kartoteka.py register_doc.py bootstrap_arka.py bootstrap_zahod.py check_incidenty.py git_zona.py
# ↑ ОХВАТ, а не список авторства. Семь имён, потому что механизм «инструменты
# судят НЕСКОЛЬКО корней» размазан по реестру и шести его потребителям. Правка
# ЛЮБОГО из них может вернуть одноместность — и вернуть её МОЛЧА: вынесенная
# фабрика получит не отсутствующие ворота, а молчащие, а молчание читается как
# «всё чисто».
#
# Запуск:  sh _generator/tools/fixtures/korni/PROGNAT.sh
# Ожидание: ФИКСТУРЫ ЗЕЛЁНЫЕ, exit 0.
#
# ЗАЧЕМ. Путь `_studio` был вшит литералом в одиннадцать мест шести инструментов.
# Пока это так, вынос любой фабрики даёт не «фабрику без гейтов», а фабрику с
# гейтами, которые МОЛЧАТ (`KONSTITUCIYA §11а` — класс, оплаченный месяцем:
# четыре гейта и хук числились существующими и не работали). Лечение — реестр
# `korni.py`. Но реестр без того, что покраснеет при его поломке, — надежда, а
# не правило (`KONSTITUCIYA §11`). Здесь краснеет.
#
# 🔴 ГЛАВНАЯ ЛОВУШКА ПРОВЕРЯЕТ МОЛЧАНИЕ, А НЕ КРАСНОТУ. Обычная фикстура ловит
# «гейт не покраснел, где должен». Здесь опаснее обратное: гейт, который ПРОПАЛ.
# Поэтому ловушка 1 мутацией СНИМАЕТ второй корень из реестра и требует, чтобы
# гейт после этого замолчал: если он краснеет и без реестра — значит краснеет по
# другой причине, и ловушка сторожит не то, что думает.
#
# ВОСЕМЬ ЛОВУШЕК, каждая проверена МУТАЦИЕЙ (гейт, который не умеет падать, — театр):
#   1. незарегистрированный `.md` во ВТОРОМ корне → ворота 5 краснеют по нему;
#      мутация: убрать корень из реестра → ворота МОЛЧАТ (это и есть покупаемое);
#   2. `register_doc.py` пишет в индекс ЭТОГО корня, чужой не трогает ни байтом;
#   3. старый корень `_studio/` краснеет ровно как раньше — регрессии нет;
#   4. `bootstrap_arka.py --koren` заводит арку в журнале второго корня;
#   5. `bootstrap_zahod.py` заводит заход в арке второго корня;
#   6. `check_incidenty.py` находит заход по имени в ОБОИХ корнях;
#   7. третий корень — ОДНА строка в реестре, ноль правок в инструментах;
#   7-бис. индекс, где `§6` ПОСЛЕДНИЙ раздел (свежая `KARTA.md` новой фабрики):
#      дверь пишет, ворота 5 засчитывают; мутация: вернуть старую границу
#      «до следующего `## §N`» → дверь обязана отказать «вписывать некуда»;
#   8. пункт Д: `poteri` печатает ДВА числа, `merge --zone` — готовую строку.
#
# ПОЧЕМУ ИНСТРУМЕНТЫ КОПИРУЮТСЯ, А НЕ ЗОВУТСЯ НА МЕСТЕ. Корень репозитория —
# «на два уровня выше файла инструмента». Копия в `$T/_generator/tools/` делает
# `parents[2]` честным адресом /tmp; символическая ссылка не годится —
# `resolve()` развернёт её в боевой путь, и фикстура начнёт судить настоящий
# репозиторий.

set -e
TOOLS=$(cd "$(dirname "$0")/../.." && pwd)

# 🔴 ОБЯЗАТЕЛЬНО ПЕРВЫМ ХОДОМ: вычистить окружение git. Внутри хука git
# экспортирует GIT_DIR/GIT_INDEX_FILE АБСОЛЮТНЫМИ путями на БОЕВОЙ репозиторий,
# и без вычистки `git add` фикстуры уходит в боевой индекс. Цена 21.07:
# фикстура, поднятая хуком, СОЗДАЛА КОММИТ В БОЕВОМ РЕПОЗИТОРИИ.
unset $(git rev-parse --local-env-vars)

T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT

VTOROY=fabrika-lenty
TRETIY=fabrika-illustracij

mkdir -p "$T/_generator/tools" "$T/_studio/docs" "$T/_studio/zhurnal" \
         "$T/$VTOROY/docs" "$T/$VTOROY/zhurnal" \
         "$T/$TRETIY/docs" "$T/$TRETIY/zhurnal" \
         "$T/teoriya-kategoriy/kartoteka"
cp "$TOOLS/korni.py" "$TOOLS/check_kartoteka.py" "$TOOLS/register_doc.py" \
   "$TOOLS/check_zahod.py" "$TOOLS/bootstrap_zahod.py" "$TOOLS/bootstrap_arka.py" \
   "$TOOLS/check_incidenty.py" "$TOOLS/git_zona.py" "$TOOLS/check_sborki.py" \
   "$TOOLS/schet_nezakrytogo.py" "$TOOLS/check_uroki.py" "$TOOLS/dostavit_urok.py" \
   "$TOOLS/modeli.py" "$TOOLS/check_tool_contract.py" \
   "$T/_generator/tools/"
# 🔴 `check_tool_contract.py` в списке — ТОТ ЖЕ КЛАСС, что `modeli.py` строкой
# ниже, и пойман он на baseline этого захода, ДО единой правки шва: `check_zahod.py`
# импортирует его на верхнем уровне (строка 84), под временной копией без него
# падает `ModuleNotFoundError: No module named 'check_tool_contract'`, и через
# него — весь `bootstrap_zahod.py`. Красной от этого была не проверка, а сама
# фикстура: ловушки 5 и 6 давали ❌ на чистом `HEAD`, без чьих-либо правок.
# Класс повторяется каждый раз, когда инструмент из списка обзаводится новым
# импортом: список копирования — ручной, а зависимость — нет.
# 🔴 `modeli.py` в списке — не украшение: `bootstrap_zahod.py` импортирует его
# на верхнем уровне, и под временной копией без него падает
# `ModuleNotFoundError: No module named 'modeli'`. Красной от этого была не
# проверка, а сама фикстура — и красной на baseline, без чьих-либо правок.
# ЦЕНА 14.08: каждый коммит и каждое слияние захода `konflikty` прошли с
# `--no-verify` «чужой долг: фикстура korni красна» — семь обходов подряд, и
# ровно та дыра, сквозь которую перестают смотреть на остальные ворота.
# Тот же класс уже был починен в `fixtures/git_zona` (там же и комментарий).
# 🔴 ДЕКЛАРАЦИЯ КАНОНИЧЕСКОГО КОРНЯ (заход `kanon-put`, 14.08): без неё
# `bootstrap_zahod.py` ОТКАЗЫВАЕТСЯ собирать заход — он больше не пишет в файл
# путь от места запуска. Одноразовое дерево объявляет каноническим себя: оно
# существует, значит подмена путей не делается вовсе и поведение прежнее.
printf '# синтетика фикстуры\n%s\n' "$T" > "$T/_generator/tools/KANON-KOREN"
cp "$TOOLS/../../_studio/zhurnal/_TEMPLATE-zahod.md" "$T/_studio/zhurnal/"
cp -r "$TOOLS/../../_studio/zhurnal/_TEMPLATE-arka" "$T/_studio/zhurnal/_TEMPLATE-arka"

REESTR="$T/_generator/tools/korni.py"

# Вписать/убрать корень в реестре — ОДНОЙ строкой, ровно как это сделал бы
# человек. `sed -i` не годится: GNU-изм, линтер инструментов его запрещает
# (BSD sed на macOS требует аргумент у -i, и строка молча ломается).
reestr_dobavit() {
    python3 - "$REESTR" "$1" "$2" "$3" "${4:-net}" <<'PY'
import sys, pathlib
p, имя, карта, журнал = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
рама = "True" if sys.argv[5] == "rama" else "False"
t = p.read_text(encoding="utf-8")
якорь = '    Корень("obzory",'
assert t.count(якорь) == 1, f"якорь неоднозначен: {t.count(якорь)}"
строка = f'    Корень("{имя}", "{карта}", "{журнал}", True, "обязательна", {рама}),\n'
p.write_text(t.replace(якорь, строка + якорь, 1), encoding="utf-8")
PY
}
reestr_ubrat() {
    python3 - "$REESTR" "$1" <<'PY'
import sys, pathlib
p, имя = pathlib.Path(sys.argv[1]), sys.argv[2]
t = p.read_text(encoding="utf-8")
строки = [l for l in t.splitlines(keepends=True) if f'Корень("{имя}"' not in l]
p.write_text("".join(строки), encoding="utf-8")
PY
}

karta_zavesti() {
    printf '%s\n' '# КАРТА (фикстурная)' '' \
        '## §5. Раздел ДО — обязан остаться нетронутым' 'Соседний текст сверху.' '' \
        '## §6. Карта документов (все `.md`)' \
        '**`docs/`:** `KARTA.md` (этот индекс).' '' \
        '## §7. Раздел ПОСЛЕ — обязан остаться нетронутым' 'Соседний текст снизу.' \
        > "$1"
}
karta_zavesti "$T/_studio/docs/KARTA.md"
karta_zavesti "$T/$VTOROY/docs/KARTA.md"
karta_zavesti "$T/$TRETIY/docs/KARTA.md"

printf '%s\n' '# Картотека (фикстурная)' '' '## Индекс по роду' '' '## Нити' \
    > "$T/teoriya-kategoriy/kartoteka/KARTA-OBLASTI.md"

cd "$T"
git init -q .
git config user.email fixture@test
git config user.name fixture
git add -A
git commit -qm baseline

GATE="python3 $T/_generator/tools/check_kartoteka.py teoriya-kategoriy/kartoteka/KARTA-OBLASTI.md --gates"
DOOR="python3 $T/_generator/tools/register_doc.py"
FAIL=0

# ── ЛОВУШКА 1: незарегистрированный .md во ВТОРОМ корне → ворота 5 краснеют ──
# Ровно то, что покупается заходом. До реестра гейт про такой файл МОЛЧАЛ, и
# молчание читалось как «всё чисто».
reestr_dobavit "$VTOROY" "$VTOROY/docs/KARTA.md" "$VTOROY/zhurnal"
echo "лента: рабочий документ" > "$T/$VTOROY/docs/FORMA.md"
if $GATE 2>&1 | grep -q "$VTOROY/docs/FORMA.md"
then echo "  ✅ незарегистрированный .md во ВТОРОМ корне краснеет (ворота 5 его видят)"
else echo "  ❌ ВОРОТА 5 НЕ ВИДЯТ ВТОРОЙ КОРЕНЬ — расшивка не сделана"; FAIL=1
fi

# ── ЛОВУШКА 1-мутация: убрать корень из реестра → ворота обязаны ЗАМОЛЧАТЬ ──
# 🔴 Без этой половины ловушка 1 ничего не доказывает: гейт мог краснеть по
# любой другой причине. Здесь проверяется, что краснота приходит ИМЕННО от
# строки реестра, — и заодно воспроизводится ровно то состояние, которое было
# до захода.
reestr_ubrat "$VTOROY"
if $GATE 2>&1 | grep -q "$VTOROY/docs/FORMA.md"
then echo "  ❌ МУТАЦИЯ НЕ СРАБОТАЛА: корень убран из реестра, а гейт всё равно краснеет — ловушка сторожит не то"; FAIL=1
else echo "  ✅ мутация: корень убран из реестра → ворота молчат (краснота идёт от реестра)"
fi
reestr_dobavit "$VTOROY" "$VTOROY/docs/KARTA.md" "$VTOROY/zhurnal"

# ── ЛОВУШКА 2: дверь пишет в индекс СВОЕГО корня, чужой не трогает ──
# Пока индекс был одной константой, дверь вписала бы документ второй фабрики в
# индекс ПЕРВОЙ: он числился бы зарегистрированным там, где его нет.
cp "$T/_studio/docs/KARTA.md" "$T/karta-studio.snapshot"
$DOOR "$VTOROY/docs/FORMA.md" "форма ленты: фикстурная проба двери" > /dev/null 2>&1 || true
if grep -q "FORMA.md" "$T/$VTOROY/docs/KARTA.md"
then echo "  ✅ дверь вписала строку в индекс ВТОРОГО корня"
else echo "  ❌ ДВЕРЬ НЕ ВПИСАЛА в индекс своего корня"; FAIL=1
fi
if cmp -s "$T/karta-studio.snapshot" "$T/_studio/docs/KARTA.md"
then echo "  ✅ чужой индекс (_studio) не тронут ни байтом"
else echo "  ❌ ДВЕРЬ ЗАПИСАЛА В ЧУЖОЙ ИНДЕКС — отображение «корень → индекс» сломано"; FAIL=1
fi
if $GATE 2>&1 | grep -q "$VTOROY/docs/FORMA.md"
then echo "  ❌ ДВЕРЬ ВПИСАЛА, А ВОРОТА НЕ ЗАСЧИТАЛИ — предикаты разъехались"; FAIL=1
else echo "  ✅ после двери ворота 5 по второму корню зелёные (дверь и гейт согласны)"
fi

# ── ЛОВУШКА 3: старый корень краснеет ровно как раньше — регрессии нет ──
echo "старый корень: сирота" > "$T/_studio/docs/SIROTA.md"
if $GATE 2>&1 | grep -q "_studio/docs/SIROTA.md"
then echo "  ✅ старый корень _studio/ краснеет как раньше (регрессии нет)"
else echo "  ❌ РЕГРЕССИЯ: ворота 5 перестали видеть _studio/"; FAIL=1
fi
rm "$T/_studio/docs/SIROTA.md"

# ── ЛОВУШКА 4: bootstrap_arka --koren заводит арку в журнале второго корня ──
python3 "$T/_generator/tools/bootstrap_arka.py" --koren "$VTOROY" 2026-08-06_proba \
    "проба второго корня" > /dev/null 2>&1 || true
if [ -f "$T/$VTOROY/zhurnal/2026-08-06_proba/PLAN.md" ]
then echo "  ✅ bootstrap_arka --koren завёл арку в журнале второго корня"
else echo "  ❌ АРКА ВО ВТОРОМ КОРНЕ НЕ ЗАВЕДЕНА"; FAIL=1
fi
if [ -d "$T/_studio/zhurnal/2026-08-06_proba" ]
then echo "  ❌ АРКА УЕХАЛА В ПЕРВЫЙ КОРЕНЬ — --koren не действует"; FAIL=1
else echo "  ✅ в первый корень арка не уехала"
fi
# мутация: неизвестный корень обязан упасть ГРОМКО и НИЧЕГО не создать
if python3 "$T/_generator/tools/bootstrap_arka.py" --koren net-takogo 2026-08-06_mimo \
        > /dev/null 2>&1
then echo "  ❌ BOOTSTRAP ПРОГЛОТИЛ НЕИЗВЕСТНЫЙ КОРЕНЬ"; FAIL=1
else
    if [ -d "$T/_studio/zhurnal/2026-08-06_mimo" ] || [ -d "$T/$VTOROY/zhurnal/2026-08-06_mimo" ]
    then echo "  ❌ неизвестный корень отвергнут, НО папка всё же создана"; FAIL=1
    else echo "  ✅ мутация: неизвестный корень → отказ, ничего не создано"
    fi
fi

# ── ЛОВУШКА 5: bootstrap_zahod заводит заход в арке второго корня ──
python3 "$T/_generator/tools/bootstrap_zahod.py" "$VTOROY/zhurnal/2026-08-06_proba" \
    proba --branch zahod/proba --zone "_generator/" --kanal terminal \
    --finalizirovano "ф1" --finalizirovano "ф2" --intervyu da \
    --opisanie "фикстурный заход второго корня" > "$T/zahod.log" 2>&1 || true
if [ -f "$T/$VTOROY/zhurnal/2026-08-06_proba/kod_proba.md" ]
then echo "  ✅ bootstrap_zahod завёл заход в арке второго корня"
else
    echo "  ❌ ЗАХОД ВО ВТОРОМ КОРНЕ НЕ ЗАВЕДЁН"; FAIL=1
    cat "$T/zahod.log"
fi

# ── ЛОВУШКА 6: check_incidenty находит заход по имени в ОБОИХ корнях ──
# Заход, лежащий в журнале второй фабрики, до расшивки просто не находился.
mkdir -p "$T/_studio/zhurnal/2026-08-06_pervaya"
echo "заход первого корня" > "$T/_studio/zhurnal/2026-08-06_pervaya/kod_pervyj.md"
NASHEL=$(python3 - "$T" <<'PY'
import sys, importlib.util, pathlib
t = pathlib.Path(sys.argv[1])
s = importlib.util.spec_from_file_location("ci", t / "_generator/tools/check_incidenty.py")
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
оба = [m.najti_zahod("kod_pervyj.md"), m.najti_zahod("kod_proba.md")]
print("оба" if all(x is not None for x in оба) else "не-оба")
PY
)
if [ "$NASHEL" = "оба" ]
then echo "  ✅ check_incidenty находит заход по имени в ОБОИХ корнях"
else echo "  ❌ CHECK_INCIDENTY ВИДИТ НЕ ВСЕ ЖУРНАЛЫ — заход второй фабрики не находится"; FAIL=1
fi

# ── ЛОВУШКА 6-бис: ВОРОТА 4 судят корень по ЕГО СОБСТВЕННОЙ раме ──
# 🔴 Найдено ВЕРИФИКАТОРОМ захода, и дожило до конца только потому, что первая
# редакция этой фикстуры ворота 4 не трогала вовсе. Дыра была ровно того же
# класса, ради которого заведён реестр, но для `SPEKA.md` вместо `KARTA.md`:
# `КОРНИ_РАМЫ` оставался ЛИТЕРАЛОМ, и новый корень либо не получал ворот 4
# ВООБЩЕ (`if not дома: continue` — молчание), либо судился по ЧУЖОЙ раме, а
# диагноз называл чужой файл.
reestr_ubrat "$VTOROY"
reestr_dobavit "$VTOROY" "$VTOROY/docs/KARTA.md" "$VTOROY/zhurnal" rama
mkdir -p "$T/teorkat-vvedenie"
printf '%s\n' '# Рама курса' '' '## ОбщаяСекция' > "$T/teorkat-vvedenie/SPEKA.md"
printf '%s\n' '# Рама ленты' '' '## ЛентаТолькоЗдесь' > "$T/$VTOROY/SPEKA.md"
printf '%s\n' '# Док ленты' '' 'см. SPEKA §ЛентаТолькоЗдесь' \
    > "$T/$VTOROY/docs/DOK-rama.md"
$DOOR "$VTOROY/docs/DOK-rama.md" "док ленты: проба рамы" > /dev/null 2>&1 || true

# (а) ссылка на СВОЮ секцию — ворота 4 обязаны молчать, а не ругаться чужой рамой
if $GATE 2>&1 | grep -q "ЛентаТолькоЗдесь"
then echo "  ❌ ВОРОТА 4 СУДЯТ ПО ЧУЖОЙ РАМЕ: своя секция корня объявлена мёртвой"; FAIL=1
else echo "  ✅ ворота 4 видят СОБСТВЕННУЮ раму второго корня (своя секция жива)"
fi
# (б) мёртвая ссылка обязана краснеть, И диагноз обязан называть СВОЙ файл рамы —
#     иначе «молчат», «судят верно» и «судят чужой рамой» неотличимы.
printf '%s\n' '# Док ленты' '' 'см. SPEKA §НетТакойСекцииВовсе' \
    > "$T/$VTOROY/docs/DOK-rama.md"
if $GATE 2>&1 | grep "НетТакойСекцииВовсе" | grep -q "$VTOROY/SPEKA.md"
then echo "  ✅ мёртвая ссылка краснеет, и диагноз называет СВОЮ раму корня"
else echo "  ❌ ВОРОТА 4 МОЛЧАТ ЛИБО НАЗЫВАЮТ ЧУЖОЙ ФАЙЛ на мёртвой ссылке второго корня"; FAIL=1
fi
# (в) МУТАЦИЯ РЕЕСТРА — суть находки верификатора. Снимаем раму у корня и
#     возвращаем ЖИВУЮ ссылку на его собственную секцию. Без строки реестра
#     корень не игнорируется — он судится по ЧУЖОЙ раме, и живая ссылка
#     объявляется мёртвой, а диагноз называет чужой файл. Ровно это и было до
#     расшивки; ловушка обязана уметь это воспроизвести, иначе она сторожит
#     не находку, а её тень.
printf '%s\n' '# Док ленты' '' 'см. SPEKA §ЛентаТолькоЗдесь' \
    > "$T/$VTOROY/docs/DOK-rama.md"
reestr_ubrat "$VTOROY"
reestr_dobavit "$VTOROY" "$VTOROY/docs/KARTA.md" "$VTOROY/zhurnal"   # без рамы
if $GATE 2>&1 | grep "ЛентаТолькоЗдесь" | grep -q "teorkat-vvedenie/SPEKA.md"
then echo "  ✅ мутация: рама снята → живая ссылка объявлена мёртвой по ЧУЖОЙ раме (старое поведение воспроизведено)"
else echo "  ❌ мутация не воспроизвела старый дефект — ловушка сторожит не то"; FAIL=1
fi
reestr_ubrat "$VTOROY"
reestr_dobavit "$VTOROY" "$VTOROY/docs/KARTA.md" "$VTOROY/zhurnal" rama
rm -f "$T/$VTOROY/docs/DOK-rama.md"

# ── ЛОВУШКА 7: третий корень — ОДНА строка в реестре, ноль правок в инструментах ──
# 🔴 Проверка на себе, названная критерием захода: если ради нового корня надо
# тронуть хоть один инструмент — расшивка не сделана, сделано переименование.
cp "$T/_generator/tools/check_kartoteka.py" "$T/ck.snapshot"
cp "$T/_generator/tools/register_doc.py" "$T/rd.snapshot"
echo "иллюстрации: сирота" > "$T/$TRETIY/docs/SLOVAR.md"
if $GATE 2>&1 | grep -q "$TRETIY/docs/SLOVAR.md"
then echo "  ❌ третий корень судится ДО внесения в реестр — реестр ни при чём"; FAIL=1
else echo "  ✅ до строки в реестре третий корень не судится (как и должно)"
fi
reestr_dobavit "$TRETIY" "$TRETIY/docs/KARTA.md" "$TRETIY/zhurnal"
if $GATE 2>&1 | grep -q "$TRETIY/docs/SLOVAR.md"
then echo "  ✅ третий корень судится после ОДНОЙ строки в реестре"
else echo "  ❌ ОДНОЙ СТРОКИ НЕ ХВАТИЛО — реестр не является единственным домом"; FAIL=1
fi
if cmp -s "$T/ck.snapshot" "$T/_generator/tools/check_kartoteka.py" \
   && cmp -s "$T/rd.snapshot" "$T/_generator/tools/register_doc.py"
then echo "  ✅ инструменты не тронуты ни байтом (ноль правок на новый корень)"
else echo "  ❌ ИНСТРУМЕНТЫ ИЗМЕНИЛИСЬ — значит корень добавляется не только реестром"; FAIL=1
fi
reestr_ubrat "$TRETIY"           # откат: третий корень был показом, а не состоянием

# ── ЛОВУШКА 7-бис: индекс, где `§6` — ПОСЛЕДНИЙ раздел ──
# 🔴 Ровно тот индекс, который получает НОВАЯ фабрика: свежая `KARTA.md`, где
# §6 «Карта документов» стоит в конце и §7 за ним ещё не заведён. Граница
# раздела бралась как «от `## §6.` до следующего `## §N`» — без «или до конца
# файла», и на таком индексе раздел вырезался ПУСТЫМ: дверь отвечала «нет
# раздела `## §6.` — вписывать некуда», а ворота 5 в ту же секунду объявляли
# сиротой каждый документ фабрики. Два обязательных указания, невыполнимых
# разом, — тот же класс, что стоил 27 обходов `--no-verify`.
# Почему дефект дожил: у живого `_studio/docs/KARTA.md` за §6 стоит §7, и у
# `karta_zavesti` выше — тоже (§5 сверху, §7 снизу). Ни одна проба его не
# касалась. Найдено приёмкой 2026-08-06; дефект НАСЛЕДОВАННЫЙ, не регрессия.
reestr_dobavit "$TRETIY" "$TRETIY/docs/KARTA.md" "$TRETIY/zhurnal"
rm -f "$T/$TRETIY/docs/SLOVAR.md"
printf '%s\n' '# КАРТА иллюстраций (фикстурная, свежая фабрика)' '' \
    '## §1. Что это' 'Индекс новой фабрики.' '' \
    '## §6. Карта документов (все `.md`)' \
    '**`docs/`:** `KARTA.md` (этот индекс).' \
    > "$T/$TRETIY/docs/KARTA.md"
echo "иллюстрации: ядро" > "$T/$TRETIY/docs/DISCIPLINA.md"

# (а) до двери файл обязан КРАСНЕТЬ. Без этой половины «зелено после двери»
#     неотличимо от «ворота его вообще не смотрят».
if $GATE 2>&1 | grep -q "$TRETIY/docs/DISCIPLINA.md"
then echo "  ✅ на индексе с §6 последним ворота 5 видят незарегистрированный файл"
else echo "  ❌ ВОРОТА МОЛЧАТ ДО ДВЕРИ — дальнейшая зелень ничего не значит"; FAIL=1
fi
# (б) дверь обязана вписать: rc=0 и строка в индексе ЭТОЙ фабрики
if $DOOR "$TRETIY/docs/DISCIPLINA.md" "ядро фабрики: как устроен рисунок" \
        > "$T/dver-posl.log" 2>&1
then echo "  ✅ дверь регистрирует на индексе, где §6 последний (rc=0)"
else
    echo "  ❌ ДВЕРЬ ОТКАЗАЛА на индексе с §6 последним — новая фабрика не заводится"; FAIL=1
    cat "$T/dver-posl.log"
fi
if grep -q "DISCIPLINA.md" "$T/$TRETIY/docs/KARTA.md"
then echo "  ✅ строка легла в индекс самой фабрики"
else echo "  ❌ СТРОКИ В ИНДЕКСЕ НЕТ — дверь отчиталась, а вписать не смогла"; FAIL=1
fi
# (в) и ворота обязаны эту строку ЗАСЧИТАТЬ — дверь и гейт режут одну границу
if $GATE 2>&1 | grep -q "$TRETIY/docs/DISCIPLINA.md"
then echo "  ❌ ДВЕРЬ ВПИСАЛА, А ВОРОТА 5 НЕ ЗАСЧИТАЛИ на индексе с §6 последним"; FAIL=1
else echo "  ✅ ворота 5 засчитали строку (граница у двери и ворот одна)"
fi

# ── ЛОВУШКА 7-бис МУТАЦИЯ: вернуть старый регексп → обязано покраснеть ──
# 🔴 Без этой половины ловушка не доказывает ничего: она могла бы зеленеть и на
# сломанной границе. Возвращаем ровно ту границу, что стояла в `HEAD`, и
# требуем воспроизведения дефекта — иначе ловушка сторожит не его.
cp "$T/_generator/tools/check_kartoteka.py" "$T/ck-do-mutacii.snapshot"
python3 - "$T/_generator/tools/check_kartoteka.py" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text(encoding="utf-8")
старое, новое = r'(?=^## §\d|\Z)', r'(?=^## §\d)'
assert t.count(старое) == 1, f"якорь границы неоднозначен: {t.count(старое)}"
p.write_text(t.replace(старое, новое, 1), encoding="utf-8")
PY
echo "иллюстрации: покрытие" > "$T/$TRETIY/docs/POKRYTIE.md"
if $DOOR "$TRETIY/docs/POKRYTIE.md" "покрытие фабрики: инцидент → рычаг" \
        > "$T/dver-mutaciya.log" 2>&1
then
    echo "  ❌ МУТАЦИЯ НЕ СРАБОТАЛА: старый регексп вернули, а дверь всё равно пишет — ловушка сторожит не то"; FAIL=1
else
    if grep -q "нет раздела" "$T/dver-mutaciya.log"
    then echo "  ✅ мутация: старая граница → дверь отказывает «вписывать некуда» (дефект воспроизведён)"
    else
        echo "  ❌ дверь упала, но НЕ на границе §6 — мутация воспроизвела другой отказ"; FAIL=1
        cat "$T/dver-mutaciya.log"
    fi
fi
cp "$T/ck-do-mutacii.snapshot" "$T/_generator/tools/check_kartoteka.py"
rm -f "$T/$TRETIY/docs/POKRYTIE.md" "$T/$TRETIY/docs/DISCIPLINA.md"
karta_zavesti "$T/$TRETIY/docs/KARTA.md"   # откат индекса к общему виду фикстуры
reestr_ubrat "$TRETIY"                     # откат: третий корень — показ, не состояние

# ── ЛОВУШКА 8 (пункт Д): poteri — ДВА числа, merge --zone — готовая строка ──
# Ветка, где ОДИН файл писали обе стороны, а другой — только ветка: ровно тот
# случай, на котором аналитик объявил заходу зону вдвое уже настоящей.
GZ="python3 $T/_generator/tools/git_zona.py"
mkdir -p "$T/zonaA" "$T/zonaB"
echo "общий, база" > "$T/zonaA/oba.md"
git add -A > /dev/null 2>&1; git commit -qm "база для Д"
git checkout -q -b vetka-d
echo "общий, версия ВЕТКИ" > "$T/zonaA/oba.md"
echo "только ветка" > "$T/zonaB/tolko-vetka.md"
git add -A > /dev/null 2>&1; git commit -qm "ветка написала оба"
git checkout -q -
echo "общий, версия HEAD" > "$T/zonaA/oba.md"
git add -A > /dev/null 2>&1; git commit -qm "HEAD написал общий"

$GZ poteri --branch vetka-d > "$T/poteri.txt" 2>&1 || true
# Ждём ИТОГ + разбивку: 2 всего = 1 «нет здесь вовсе» + 1 «писали обе стороны».
# Итог обязан остаться первым числом — см. комментарий в `print_loss_watch`:
# заголовок `пропадёт файлов: 0` при живой потере есть молчание, а не точность.
if grep -q "изменено с обеих сторон: 1" "$T/poteri.txt" \
   && grep -q "нет здесь вовсе: 1" "$T/poteri.txt" \
   && grep -q "пропадёт файлов: 2" "$T/poteri.txt"
then echo "  ✅ poteri печатает ИТОГ 2 и разбивку: нет-здесь-вовсе=1, с-обеих-сторон=1"
else
    echo "  ❌ POTERI НЕ РАЗДЕЛЯЕТ ДВА КЛАССА — зона по его выводу занижается"; FAIL=1
    cat "$T/poteri.txt"
fi
# мутация: файл, изменённый обеими сторонами, обязан влиять на второе число.
# Уберём расхождение (вернём версию ветки) — второе число обязано стать 0.
git checkout -q vetka-d -- zonaA/oba.md
git add -A > /dev/null 2>&1; git commit -qm "снял расхождение"
$GZ poteri --branch vetka-d > "$T/poteri2.txt" 2>&1 || true
if grep -q "изменено с обеих сторон: 0" "$T/poteri2.txt"
then echo "  ✅ мутация: расхождение снято → второе число стало 0 (оно живое, а не подпись)"
else echo "  ❌ ВТОРОЕ ЧИСЛО НЕ РЕАГИРУЕТ на снятие расхождения — это подпись, а не счёт"; FAIL=1
fi

$GZ merge vetka-d --zone zonaA > "$T/merge.txt" 2>&1 || true
if grep -q -- "--zone zonaA" "$T/merge.txt" && grep -q -- "--zone zonaB" "$T/merge.txt"
then echo "  ✅ merge при отказе печатает готовую строку со ВСЕМИ зонами"
else
    echo "  ❌ MERGE НЕ ПЕЧАТАЕТ ГОТОВУЮ СТРОКУ — зону приходится собирать руками"; FAIL=1
    cat "$T/merge.txt"
fi

# ── ЛОВУШКА 9: ДОМ ШАБЛОНОВ — репозиторий ИНСТРУМЕНТОВ, а не `GIT_ZONA_REPO` ──
# 🔴 ВОСПРОИЗВОДИТ ЖИВОЙ СЛУЧАЙ 2026-08-15, а не выдуманный: инструменты лежат
# в `materials`, а `GIT_ZONA_REPO` показывает на `disciplina`, где
# `_TEMPLATE-zahod.md` нет ВОВСЕ (`bootstrap_zahod.py` падал «шаблон не
# найден»), а лежащая копия `_TEMPLATE-arka` протухла — несла греп-гейт
# `^ЦЕНА: `, из-за которого на арке `2026-07-25_lekcia-1` тринадцать уроков из
# девятнадцати получили ложный зелёный; в `materials` он починен 06.08, до
# копии починка не доехала.
# Пока `шаблон()` собирался от `REPO`, дом шаблонов переезжал вместе с
# переменной — то есть КАЖДЫЙ обслуживаемый репозиторий обязан был держать свою
# копию шаблонов, а копии расходятся МОЛЧА: разъезд виден не в момент разъезда,
# а через неделю, на собранном по протухшему шаблону заходе.
# Здесь дерево `GIT_ZONA_REPO` заведомо БЕЗ шаблонов — журнал есть, шаблонов в
# нём нет (ровно состояние `disciplina`), и проверяются ОБЕ половины: ответ
# лежит внутри дерева ИНСТРУМЕНТОВ и файл по нему СУЩЕСТВУЕТ. Одной первой
# половины мало: путь можно вернуть верный и в дерево без файла.
# 🔴 `pwd -P` обязателен: macOS кладёт `mktemp -d` в `/var/folders/…`, где
# `/var` — симлинк на `/private/var`. `Path(__file__).resolve()` внутри
# `korni.py` даёт написание через `/private`, а `$T` несёт написание через
# `/var`; сравнение без `pwd -P` не совпало бы НИКОГДА и ловушка краснела бы
# всегда — то есть сторожила бы симлинк, а не шов. Тот же класс уже оплачен в
# `kanonizirovat_tekst()` (комментарий «у одного корня бывает два написания»).
TR=$(cd "$T" && pwd -P)
NET_SHABLONOV="$T/net-shablonov"
mkdir -p "$NET_SHABLONOV/_studio/zhurnal"     # журнал есть, `_TEMPLATE-*` в нём нет
for IMYA in _TEMPLATE-zahod.md _TEMPLATE-arka; do
    OTVET=$(GIT_ZONA_REPO="$NET_SHABLONOV" python3 - "$T" "$IMYA" <<'PY'
import sys, importlib.util, pathlib
t, имя = pathlib.Path(sys.argv[1]), sys.argv[2]
s = importlib.util.spec_from_file_location("k", t / "_generator/tools/korni.py")
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
п = m.шаблон(имя)
print(f"{п}|{'da' if п.exists() else 'net'}")
PY
) || OTVET="|net"
    PUT=${OTVET%|*}
    EST=${OTVET##*|}
    case "$PUT" in
        "$TR"/*)
            if [ "$EST" = da ]
            then echo "  ✅ дом шаблонов: $IMYA взят из репозитория ИНСТРУМЕНТОВ и существует"
            else echo "  ❌ ПУТЬ ВНУТРИ ИНСТРУМЕНТОВ, НО ФАЙЛА НЕТ — $IMYA: $PUT"; FAIL=1
            fi ;;
        "$NET_SHABLONOV"/*)
            echo "  ❌ ДОМ ШАБЛОНОВ УЕХАЛ ЗА GIT_ZONA_REPO — $IMYA взят из дерева без шаблонов: $PUT"; FAIL=1 ;;
        *)
            echo "  ❌ ШАБЛОН НЕ ИЗ ИНСТРУМЕНТОВ И НЕ ИЗ GIT_ZONA_REPO — $IMYA: $PUT"; FAIL=1 ;;
    esac
done

if [ "$FAIL" = 0 ]
then echo "ФИКСТУРЫ ЗЕЛЁНЫЕ"; exit 0
else echo "ФИКСТУРЫ КРАСНЫЕ"; exit 1
fi
