#!/bin/sh
# TOOL-CONTRACT-COVERS: check_tool_contract.py
#
# Мета-фикстура КОНТРАКТА ИНСТРУМЕНТА.
#
# Запуск:  sh _generator/tools/fixtures/tool_contract/PROGNAT.sh
# Ожидание: ФИКСТУРЫ ЗЕЛЁНЫЕ, exit 0.
#
# ЗАЧЕМ ИМЕННО ОБЕ СТОРОНЫ. Гейт над гейтами опаснее всего, что он проверяет:
# ложное красное блокирует здоровые коммиты ВСЕМ ТРЁМ писателям сразу, и первым
# же ходом его отключат (Р31) — то есть цена ошибки тут не «проехало лишнее», а
# «затея кончилась». Поэтому на КАЖДУЮ проверку здесь стоит ПАРА: временный
# нарушитель обязан покраснеть, временный здоровый — пройти. Проверка, умеющая
# только краснеть, — не гейт, а помеха; умеющая только зеленеть — театр.
#
# ПОЧЕМУ ЭТО БЕЗОПАСНО ГОНЯТЬ. Пробные инструменты и пробный дом фикстур живут
# в одноразовом каталоге (`TOOL_CONTRACT_HOME`), боевое дерево не трогается ни
# на чтение-с-записью, ни на исполнение: линтер СТАТИЧЕСКИЙ и проверяемый файл
# никогда не запускает. Урок 1.7 (гейт записал коммит в боевой репозиторий)
# закрыт здесь конструктивно, а не обещанием.

set -e
TOOLS=$(cd "$(dirname "$0")/../.." && pwd)

# Та же каноническая вычистка, что в фикстуре git_zona: внутри хука git отдаёт
# дочерним процессам GIT_DIR/GIT_INDEX_FILE АБСОЛЮТНЫМИ путями на боевой репо.
unset $(git rev-parse --local-env-vars)

T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
mkdir -p "$T/fixtures/tool_contract"
: > "$T/fixtures/tool_contract/BASELINE"

LINT="python3 $TOOLS/check_tool_contract.py"
FAIL=0

# Пробный дом фикстур пуст ⇒ ни baseline, ни охват пробных имён не покрывают.
# Каждая проверка мутируется в обе стороны на ОДНОЙ паре файлов.
krasnoe() {   # $1 — файл-нарушитель, $2 — что проверяем
    if TOOL_CONTRACT_HOME="$T" $LINT "$1" > /dev/null 2>&1
    then echo "  ❌ НЕ ПОКРАСНЕЛО: $2 — проверка мертва, нарушитель доедет до репо"; FAIL=1
    else echo "  ✅ нарушитель пойман: $2"
    fi
}
zelenoe() {   # $1 — здоровый файл, $2 — что проверяем
    if TOOL_CONTRACT_HOME="$T" $LINT "$1" > /dev/null 2>&1
    then echo "  ✅ здоровый пропущен: $2"
    else echo "  ❌ ЛОЖНОЕ КРАСНОЕ на здоровом: $2 — гейт бьёт по своим"; FAIL=1
    fi
}

# ── ПРОВЕРКА 1: переносимость (GNU-измы) ──
# ЦЕНА 23.07: `touch -d` в фикстуре остановил здоровый коммит владельца на macOS,
# оставаясь зелёным у автора в Linux-песочнице.
# 🔴 Образцы-нарушители СОБИРАЮТСЯ ИЗ ПОЛОВИНОК, а не пишутся здесь буквально.
# Ловушка 7 фикстуры git_zona грепает все fixtures/*/PROGNAT.sh на GNU-измы и
# комментарии пропускает, а heredoc — нет. ЦЕНА (поймано живым прогоном хука
# 28.07): дословный `touch -d` в тестовых данных этого файла покрасил ЧУЖУЮ
# фикстуру и заблокировал бы каждый коммит, трогающий git_zona.py, — гейт
# ударил бы по своим ровно так, как заход запрещает.
# 🔴 Каждый файл, идущий в zelenoe(), несёт ОБА маркера — `no-input` (свой
# исходный смысл) и `called-by-hand` (проверка 13, живая точка вызова/маркер):
# иначе он ложно краснеет от НЕСВЯЗАННОЙ проверки, а изолировать одну переменную
# за раз — весь смысл этой мета-фикстуры (см. шапку файла). Файлы, идущие только
# в krasnoe(), маркер `called-by-hand` не несут — лишний нарушитель им не мешает.
python3 - "$T" <<'PY'
import sys, pathlib
T = pathlib.Path(sys.argv[1])
gnu = "tou" + "ch -d"          # склейка: буквального GNU-изма в файле нет
(T / "gnu_bad.py").write_text(
    "# TOOL-CONTRACT: no-input\n"
    "def podskazka():\n"
    f'    print("состарить файл: {gnu} 10-minutes-ago cel")\n', encoding="utf-8")
(T / "gnu_ok.py").write_text(
    "# TOOL-CONTRACT: no-input\n"
    "# TOOL-CONTRACT: called-by-hand\n"
    "def podskazka():\n"
    '    print("состарить файл: python3 -c os.utime(...)")\n', encoding="utf-8")
# Комментарий и докстринг — документация, а не код: перечень запрещённого в них
# краснеть НЕ должен, иначе гейт валится на собственном описании (поймано первой
# же калибровкой — линтер покраснел сам на себе).
(T / "gnu_doc.py").write_text(
    "# TOOL-CONTRACT: no-input\n"
    "# TOOL-CONTRACT: called-by-hand\n"
    f"# нельзя писать {gnu} — это GNU-изм\n"
    "def podskazka():\n"
    f'    """Запрещено: {gnu}."""\n'
    '    print("всё хорошо")\n', encoding="utf-8")
PY
krasnoe "$T/gnu_bad.py" "GNU-изм в печатаемой строке"
zelenoe "$T/gnu_ok.py"  "тот же смысл через python3 -c"
zelenoe "$T/gnu_doc.py" "GNU-изм только в комментарии и докстринге"

# ── ПРОВЕРКА 2: --no-optional-locks ──
# ЦЕНА 21.07: голое чтение git берёт .git/index.lock и роняет чужой коммит —
# так гейт, следивший за потерями, сам сорвал три коммита за сессию.
cat > "$T/lock_bad.py" <<'PY'
# TOOL-CONTRACT: no-input
import subprocess
def chitat():
    return subprocess.run(["git", "diff", "--cached"], capture_output=True)
PY
cat > "$T/lock_ok.py" <<'PY'
# TOOL-CONTRACT: no-input
# TOOL-CONTRACT: called-by-hand
import subprocess
def chitat():
    return subprocess.run(["git", "--no-optional-locks", "diff", "--cached"],
                          capture_output=True)
PY
krasnoe "$T/lock_bad.py" "вызов git без --no-optional-locks"
zelenoe "$T/lock_ok.py"  "тот же вызов с флагом"

# ── ПРОВЕРКА 3: сырой shell владельцу ──
# ЦЕНА 22.07: в zsh несовпавший glob роняет ВСЮ строку (`no matches found`),
# уборка не выполнилась, а владелец считал, что выполнилась.
cat > "$T/shell_bad.py" <<'PY'
# TOOL-CONTRACT: no-input
def podskazka():
    print("уборка: cd koren && rm -f .git/*.lock")
PY
cat > "$T/shell_ok.py" <<'PY'
# TOOL-CONTRACT: no-input
# TOOL-CONTRACT: called-by-hand
def podskazka():
    print("уборка: python3 _generator/tools/git_zona.py clean")
PY
krasnoe "$T/shell_bad.py" "владельцу печатается цепочка с rm и glob"
zelenoe "$T/shell_ok.py"  "вместо неё печатается подкоманда git_zona.py"

# Прозаическое упоминание команды в отчёте об ОШИБКЕ — не выдача shell.
# Набор специально узкий: ложное красное здесь дороже пропуска.
cat > "$T/shell_proza.py" <<'PY'
# TOOL-CONTRACT: no-input
# TOOL-CONTRACT: called-by-hand
def dolozhit(rc):
    print(f"git rm упал (rc={rc})")
PY
zelenoe "$T/shell_proza.py" "упоминание команды в сообщении об ошибке"

# ── ПРОВЕРКА 4: запрет записи из песочницы ──
# ЦЕНА 22.07: запрет жил только словами в каноне, Cowork его нарушил —
# репозиторий дважды вставал на полчаса для ВСЕХ писателей.
cat > "$T/sbx_bad.py" <<'PY'
# TOOL-CONTRACT: no-input
import subprocess
def sohranit():
    subprocess.run(["git", "--no-optional-locks", "commit", "-m", "x"])
PY
cat > "$T/sbx_ok.py" <<'PY'
# TOOL-CONTRACT: no-input
# TOOL-CONTRACT: called-by-hand
import subprocess
from gz import in_sandbox, refuse_write
def sohranit():
    if in_sandbox():
        return refuse_write("Коммит")
    subprocess.run(["git", "--no-optional-locks", "commit", "-m", "x"])
PY
krasnoe "$T/sbx_bad.py" "пишущая git-операция без ссылки на in_sandbox/refuse_write"
zelenoe "$T/sbx_ok.py"  "та же операция под защитой"

# Читающий инструмент защиты НЕ требует — требовать значило бы краснеть на
# здоровых check_*.py, которые только смотрят в индекс.
cat > "$T/sbx_read.py" <<'PY'
# TOOL-CONTRACT: no-input
# TOOL-CONTRACT: called-by-hand
import subprocess
def posmotret():
    subprocess.run(["git", "--no-optional-locks", "ls-files"])
PY
zelenoe "$T/sbx_read.py" "читающий инструмент без защиты песочницы"

# ── ПРОВЕРКА 5: кривой вход доказан, а не обещан ──
# ЦЕНА 23.07: `bootstrap_arka.py --help` проглотил флаг как имя арки и создал
# папку-сироту, которую потом каждый `plan` тянул в черновик коммита.
# 🔴 called-by-hand стоит здесь СРАЗУ: этот файл дальше проверяется ТОЛЬКО на
# «кривой вход» (BASELINE/охват фикстуры) — без маркера каждая зелёная мутация
# ниже ложно краснела бы ещё и от «живой точки вызова», путая переменные.
cat > "$T/vhod_bad.py" <<'PY'
# TOOL-CONTRACT: called-by-hand
import argparse
def main():
    argparse.ArgumentParser().parse_args()
PY
krasnoe "$T/vhod_bad.py" "разбор входа без фикстуры, пометки и baseline"

cat > "$T/vhod_marker.py" <<'PY'
# TOOL-CONTRACT: no-input
# TOOL-CONTRACT: called-by-hand
import argparse
def main():
    argparse.ArgumentParser().parse_args()
PY
zelenoe "$T/vhod_marker.py" "тот же вход с явной пометкой no-input"

# Baseline освобождает ТОЛЬКО от требования фикстуры. Мутация: очистили
# baseline — файл снова краснеет (проверено парой ниже).
echo "vhod_bad.py" > "$T/fixtures/tool_contract/BASELINE"
zelenoe "$T/vhod_bad.py" "инструмент из BASELINE (долг назван явно)"
: > "$T/fixtures/tool_contract/BASELINE"
krasnoe "$T/vhod_bad.py" "он же после очистки BASELINE — послабление снято"

# ── ПРОВЕРКА 6: 🔴 ТРИГГЕР = ОХВАТ ──
# Корень всей затеи. Пока охват жил в голове автора, хук поднимал фикстуру
# git_zona только на правку git_zona.py, хотя ловушка 14 внутри неё сторожит и
# три bootstrap_*. Теперь охват объявлен строкой, и её читают и линтер, и хук.
mkdir -p "$T/fixtures/proba"
cat > "$T/fixtures/proba/PROGNAT.sh" <<'FIX'
#!/bin/sh
# TOOL-CONTRACT-COVERS: vhod_bad.py
echo "проба"
FIX
zelenoe "$T/vhod_bad.py" "он же под объявленным охватом чужой фикстуры"

V=$(TOOL_CONTRACT_HOME="$T" $LINT --fixtures-for "$T/vhod_bad.py" | grep -c 'proba/PROGNAT.sh' || true)
[ "$V" = "1" ] && echo "  ✅ --fixtures-for нашёл фикстуру по ОБЪЯВЛЕННОМУ охвату" \
               || { echo "  ❌ ОХВАТ НЕ ЧИТАЕТСЯ — хук не поднимет покрывающую фикстуру"; FAIL=1; }

# Снятие строки охвата обязано убить и подъём фикстуры, и послабление.
printf '#!/bin/sh\necho "проба"\n' > "$T/fixtures/proba/PROGNAT.sh"
V=$(TOOL_CONTRACT_HOME="$T" $LINT --fixtures-for "$T/vhod_bad.py" | grep -c 'proba/PROGNAT.sh' || true)
[ "$V" = "0" ] && echo "  ✅ снял строку охвата — фикстура больше не поднимается (мутация ловится)" \
               || { echo "  ❌ охват держится не строкой, а догадкой — механизм мнимый"; FAIL=1; }

# ── ПРОВЕРКА 7: охват НА ЖИВОМ ДЕРЕВЕ (критерий «триггер = охват») ──
# Именно тот зазор, ради которого заход затевался: правка bootstrap_* обязана
# поднимать фикстуру git_zona, потому что ловушка 14 внутри неё их сторожит.
# Только чтение боевого дерева, ничего не исполняется и не пишется.
V=$($LINT --fixtures-for _generator/tools/bootstrap_zahod.py 2>/dev/null \
    | grep -c 'fixtures/git_zona/PROGNAT.sh' || true)
[ "$V" = "1" ] && echo "  ✅ живое дерево: правка bootstrap_zahod.py поднимает фикстуру git_zona" \
               || { echo "  ❌ ЗАЗОР ЖИВ: правка bootstrap_* не поднимает сторожащую их фикстуру"; FAIL=1; }

# ── ПРОВЕРКА 8: молчит, когда чисто (Р31) ──
# Гейт, который шумит зря, отключат — и это будет конец затеи.
# 🔴 Найдено живым прогоном (заход `instrument-podklyuchen`, 2026-08-08): `--staged` без
# `GIT_ZONA_REPO` смотрит на РЕАЛЬНЫЙ репозиторий исполнителя — если в момент прогона фикстуры
# у него ЗАСТЕЙДЖЕНЫ свои правки (обычное дело посреди коммита зоны), «молчит на чистом» ложно
# краснеет на ЕГО живой работе, а не на пустоте. `TOOL_CONTRACT_HOME` изолирует BASELINE/охват
# фикстур, но не сам git — нужна ОБА изолировать. Пустой одноразовый репозиторий с нуля даёт
# настоящую пустоту вместо «пустоты по совпадению».
T8=$(mktemp -d)
(cd "$T8" && git init -q . && git config user.email t@t && git config user.name t \
    && git commit -q --allow-empty -m base)
V=$(TOOL_CONTRACT_HOME="$T" GIT_ZONA_REPO="$T8" $LINT --staged 2>&1 | wc -c | tr -d ' ')
rm -rf "$T8"
[ "$V" = "0" ] && echo "  ✅ на пустом staged линтер молчит" \
               || { echo "  ❌ ЛИНТЕР ШУМИТ НА ЧИСТОМ — его отключат (Р31)"; FAIL=1; }

# ── ПРОВЕРКА 9: битый файл не притворяется здоровым ──
# «Не разобрался» и «нарушений нет» обязаны выглядеть по-РАЗНОМУ: иначе синтак-
# сическая ошибка молча отключает контракт целиком.
printf 'def main(\n' > "$T/bityj.py"
krasnoe "$T/bityj.py" "файл не разбирается — контракт не считается пройденным"

# ── ПРОВЕРКА 10: формы, которые провёз верификатор 28.07 ──
# Все три он назвал не трюком, а естественным стилем: GNU-изм разнесён по
# элементам списка (сплошной строкой в питоне так не пишут), команда отдана
# шеллу строкой (мимо разбора списка вообще), снос через os.remove.
python3 - "$T" <<'PY'
import sys, pathlib
T = pathlib.Path(sys.argv[1])
gnu, flag = "s" + "ed", "-" + "i"      # склейка: буквального GNU-изма в файле нет
(T / "argv_gnu.py").write_text(
    "# TOOL-CONTRACT: no-input\n"
    "import subprocess\n"
    "def pravit():\n"
    f'    subprocess.run(["{gnu}", "{flag}", "s/a/b/", "f.txt"])\n', encoding="utf-8")
(T / "shell_sys.py").write_text(
    "# TOOL-CONTRACT: no-input\n"
    "import os\n"
    "def sohranit():\n"
    '    os.system("git commit -m proba")\n', encoding="utf-8")
(T / "shell_ok.py").write_text(
    "# TOOL-CONTRACT: no-input\n"
    "# TOOL-CONTRACT: called-by-hand\n"
    "import os\n"
    "def posmotret():\n"
    '    os.system("git --no-optional-locks status")\n', encoding="utf-8")
(T / "snos.py").write_text(
    "# TOOL-CONTRACT: no-input\n"
    "import os\n"
    "def ubrat(p):\n"
    "    os.remove(p)\n", encoding="utf-8")
# Ложное, на котором линтер краснел: .remove() у обычного СПИСКА — не снос.
(T / "spisok.py").write_text(
    "# TOOL-CONTRACT: no-input\n"
    "# TOOL-CONTRACT: called-by-hand\n"
    "def ubrat(imena, x):\n"
    "    imena.remove(x)\n"
    "    return imena\n", encoding="utf-8")
# Ложное: сборка команды по кускам — огрызок ["git"] судить нельзя.
(T / "sborka.py").write_text(
    "# TOOL-CONTRACT: no-input\n"
    "# TOOL-CONTRACT: called-by-hand\n"
    "import subprocess\n"
    "FLAGS = [\"--no-optional-locks\"]\n"
    "def chitat():\n"
    '    subprocess.run(["git"] + FLAGS + ["diff"])\n', encoding="utf-8")
# Ложное: прозаическое предупреждение про rm БЕЗ glob — не выдача shell.
(T / "proza_rm.py").write_text(
    "# TOOL-CONTRACT: no-input\n"
    "# TOOL-CONTRACT: called-by-hand\n"
    "def predupredit():\n"
    '    print("⚠ Никогда не набирай rm -rf вручную")\n', encoding="utf-8")
PY
krasnoe "$T/argv_gnu.py"  "GNU-изм, разнесённый по элементам списка аргументов"
krasnoe "$T/shell_sys.py" "git-мутация строкой через os.system"
zelenoe "$T/shell_ok.py"  "та же форма на чтение и с флагом"
krasnoe "$T/snos.py"      "os.remove без ссылки на in_sandbox/refuse_write"
zelenoe "$T/spisok.py"    "remove() у обычного списка — не снос на диске"
zelenoe "$T/sborka.py"    "команда, собранная из кусков списка"
zelenoe "$T/proza_rm.py"  "предупреждение про rm без glob"

# ── ПРОВЕРКА 11: переносимость судит и .sh ──
# Урок 23.07 оплачен GNU-измом именно в ФИКСТУРЕ, а не в .py: гейт, который
# судит только питон, слеп ровно к тому артефакту, которым и был оплачен.
python3 - "$T" <<'PY'
import sys, pathlib
T = pathlib.Path(sys.argv[1])
gnu = "tou" + "ch -d"
(T / "probnaya.sh").write_text(f'#!/bin/sh\n{gnu} "10 minutes ago" f\n', encoding="utf-8")
(T / "chistaya.sh").write_text('#!/bin/sh\npython3 -c "import os"\n', encoding="utf-8")
PY
krasnoe "$T/probnaya.sh" "GNU-изм в .sh (фикстуры и хуки исполняются у владельца)"
zelenoe "$T/chistaya.sh" "здоровый .sh"

# ── ПРОВЕРКА 12: 🔴 ЖИВАЯ ТОЧКА ВЫЗОВА — не подключён и не помечен = не гейт ──
# Заход `instrument-podklyuchen` (2026-08-08): шесть инструментов были зелёными
# только потому, что их никто не звал. Написанный, но нигде не упомянутый
# инструмент обязан покраснеть; тот же инструмент с маркером «зовут руками» или
# с реальным упоминанием ВНЕ себя — пройти.
cat > "$T/sirota.py" <<'PY'
# TOOL-CONTRACT: no-input
def rabota():
    return 1
PY
krasnoe "$T/sirota.py" "инструмент нигде не упомянут и не помечен called-by-hand"

cat > "$T/pomechen.py" <<'PY'
# TOOL-CONTRACT: no-input
# TOOL-CONTRACT: called-by-hand
def rabota():
    return 1
PY
zelenoe "$T/pomechen.py" "тот же инструмент с явным маркером called-by-hand"

# Живая ссылка ИЗВНЕ (не маркер) — тоже законное доказательство подключения.
cat > "$T/podklyuchen.py" <<'PY'
# TOOL-CONTRACT: no-input
def rabota():
    return 1
PY
cat > "$T/vyzyvayushij.py" <<'PY'
# TOOL-CONTRACT: no-input
# TOOL-CONTRACT: called-by-hand
import subprocess
def zvat():
    subprocess.run(["python3", "podklyuchen.py"])
PY
zelenoe "$T/podklyuchen.py" "упомянут в другом файле того же дома — живая точка вызова есть"

# ── ПРОВЕРКА 13: 🔴 СУДИТ ИНДЕКС И ТОЛЬКО ДОБАВЛЕННЫЕ СТРОКИ ──
# Две половины, каждая из которых по отдельности убивает затею:
#  · читать рабочую копию вместо индекса — гейт зелёный на коммите с нарушителем
#    («поправил после add» — рутина, а не трюк);
#  · судить файл целиком — пре-существующее нарушение делает самый правимый
#    инструмент репозитория незакоммитабельным с первого дня, и гейт отключат.
R="$T/repo"
mkdir -p "$R/_generator/tools"
cd "$R"
git init -q .
git config user.email fixture@test
git config user.name fixture
cp "$TOOLS/check_tool_contract.py" _generator/tools/
mkdir -p _generator/tools/fixtures/tool_contract
cp "$TOOLS/fixtures/tool_contract/BASELINE" _generator/tools/fixtures/tool_contract/
printf '# TOOL-CONTRACT: no-input\n# TOOL-CONTRACT: called-by-hand\nimport subprocess\ndef a():\n    subprocess.run(["git", "diff"])\n' \
    > _generator/tools/dolg.py
git add -A && git commit -qm baseline

# Пре-существующее нарушение + безобидная правка ниже: коммит обязан ПРОЙТИ.
printf '# и ещё комментарий\n' >> _generator/tools/dolg.py
git add _generator/tools/dolg.py
if python3 _generator/tools/check_tool_contract.py --staged > /dev/null 2>&1
then echo "  ✅ пре-существующее нарушение НЕ валит безобидную правку (судятся строки)"
else echo "  ❌ ЧУЖОЙ ДОЛГ ВАЛИТ ЗДОРОВЫЙ КОММИТ — гейт бьёт по своим, его отключат"; FAIL=1
fi

# Нарушитель в НОВОЙ строке — обязан покраснеть.
printf 'def b():\n    subprocess.run(["git", "log"])\n' >> _generator/tools/dolg.py
git add _generator/tools/dolg.py
if python3 _generator/tools/check_tool_contract.py --staged > /dev/null 2>&1
then echo "  ❌ НАРУШЕНИЕ В ДОБАВЛЕННОЙ СТРОКЕ ПРОЕХАЛО"; FAIL=1
else echo "  ✅ нарушение в добавленной строке краснеет"
fi

# Застейджен нарушитель, потом файл починен НА ДИСКЕ — судить обязан индекс.
git checkout -q -- _generator/tools/dolg.py 2>/dev/null || true
printf 'def c():\n    subprocess.run(["git", "show"])\n' >> _generator/tools/dolg.py
git add _generator/tools/dolg.py
python3 - <<'PY'
import pathlib
p = pathlib.Path("_generator/tools/dolg.py")
t = p.read_text(encoding="utf-8").replace('["git", "show"]',
                                          '["git", "--no-optional-locks", "show"]')
p.write_text(t, encoding="utf-8")
PY
if python3 _generator/tools/check_tool_contract.py --staged > /dev/null 2>&1
then echo "  ❌ ЛИНТЕР ЧИТАЕТ ДИСК, А НЕ ИНДЕКС — в коммит уедет нарушитель, гейт зелёный"; FAIL=1
else echo "  ✅ судится ИНДЕКС: починка на диске после add гейт не обманывает"
fi
cd "$T"

[ "$FAIL" = "0" ] && { echo "ФИКСТУРЫ ЗЕЛЁНЫЕ"; exit 0; } || { echo "ФИКСТУРЫ КРАСНЫЕ"; exit 1; }
