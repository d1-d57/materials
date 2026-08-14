#!/usr/bin/env python3
"""КОНТРАКТ ИНСТРУМЕНТА — гейт над инструментами фабрики (`_generator/tools/*.py`).

    python3 _generator/tools/check_tool_contract.py --staged        # режим хука
    python3 _generator/tools/check_tool_contract.py <пути…>         # калибровка/фикстура
    python3 _generator/tools/check_tool_contract.py --fixtures-for <пути…>

ЗАЧЕМ. За четыре сессии ~15 поломок инфраструктуры свелись к одному классу,
который возвращался в НОВЫХ аренах, потому что лекарство каждый раз было ПРОЗОЙ —
заметка, строка канона, урок в дневнике. Проза не переносится на следующий
инструмент: она лежит там, куда исполнитель с пустым контекстом не заглядывает.
Живое доказательство (ZHURNAL 4.4): фикстура `git_zona` поднималась хуком только
при правке `git_zona.py`, хотя ловушка 14 внутри неё сторожит `bootstrap_*` —
у гейта триггер был уже его собственного охвата.

Здесь то же лекарство выдано МЕХАНИЗМОМ: набор дешёвых статических проверок,
который хук гонит на КАЖДЫЙ staged-инструмент, так что нарушитель не доезжает
до репозитория. Правила — не новые: каждая проверка кодифицирует уже оплаченный
урок из `_studio/docs/kak-delat/GIT-disciplina.md`.

🔴 ДВА ЗАКОНА, БЕЗ КОТОРЫХ ГЕЙТ ОПАСНЕЕ ЕГО ОТСУТСТВИЯ:

1. **Судим staged-диф, а не дерево.** Пре-существующее нарушение НЕ валит чужой
   коммит, пока файл не правят (та же клауза, что у `check_kartoteka --staged`).
   Молчим, когда чисто (Р31): гейт, который шумит зря, отключат.
2. **Проверяемый инструмент НИКОГДА не исполняется.** Только чтение текста, AST
   и греп. Гейт, запускающий боевой инструмент с мусорным входом, — это цена
   21.07: фикстура, поднятая хуком, создала коммит в БОЕВОМ репозитории.

🔴 ОДНО УЗКОЕ ИСКЛЮЧЕНИЕ ИЗ ЗАКОНА 2 (заход `kod_gejty-kotorye-vrut.md`, 06.08):
`--help` — проверка `check_help()` РЕАЛЬНО запускает инструмент, но РОВНО с
флагом `--help` и НИКОГДА в режиме `--staged` (хук): по конвенции CLI это
безопасный, свободный от побочных эффектов вызов — не «мусорный вход», от
которого защищает закон 2, а единственный вход, для которого исполнение и
есть проверка. Живой дефект: канон в каждом заходе требует «сверь `--help`,
не угадывай», а `check_kurs.py --help` падает трейсбеком (аргумент принят за
путь). Работает только в аудите (`--all`, явные пути) — там, где мутация
боевого репозитория и так не грозит.
"""
import argparse
import ast
import io
import os
import re
import subprocess
import sys
import tokenize
from pathlib import Path

# GIT_ZONA_REPO — та же дверь, что у git_zona.py: фикстура гоняет линтер на
# одноразовом каталоге, боевой репозиторий при этом не адресуется вовсе.
REPO = Path(os.environ.get("GIT_ZONA_REPO") or Path(__file__).resolve().parents[2])
TOOLS_REL = "_generator/tools"
# TOOL_CONTRACT_HOME — дом фикстур и baseline. Подменяется ТОЛЬКО мета-фикстурой:
# без него она не смогла бы промутировать сам механизм охвата, не записав
# пробную фикстуру в боевое дерево (урок 1.7: гейт не смеет писать в проверяемый
# репозиторий). В бою переменной нет, и дом берётся рядом с инструментом.
HOME_DIR = Path(os.environ.get("TOOL_CONTRACT_HOME") or Path(__file__).resolve().parent)
FIXTURES = HOME_DIR / "fixtures"
BASELINE = FIXTURES / "tool_contract" / "BASELINE"
CANON = "_studio/docs/kak-delat/GIT-disciplina.md"

# ── Паттерны GNU-измов ────────────────────────────────────────────────────────
# Склеиваем из половинок — иначе линтер краснеет на собственном списке
# запрещённых конструкций (эта ошибка уже ловилась в ловушке 7 фикстуры
# git_zona; повторять её здесь нет смысла).
GNU_PAIRS = [("touch", " -d"), ("date", " -d"), ("sed", " -i"),
             ("xargs", " -r"), ("stat", " -c"), ("grep", " -P")]
GNU_RE = re.compile("|".join(re.escape(a + b) for a, b in GNU_PAIRS))
# Тот же GNU-изм, разнесённый по элементам списка: `["sed", "-i", …]`. Ищется
# отдельно, потому что сплошной строкой он в питоне как раз НЕ пишется — а
# регексп выше видит только сплошную. {команда: флаги}
GNU_ARGV = {a: {b.strip()} for a, b in GNU_PAIRS}

# Сырой shell, который нельзя печатать владельцу (канон §0). Набор УЗКИЙ
# НАМЕРЕННО: сюда взяты ровно те конструкции, которые в таблице цен §0 уже
# ломались на переходе bash/Linux → zsh/macOS, — цепочка (обрыв невидим),
# подстановка (расщепление аргумента с пробелами), xargs (BSD≠GNU).
# Прозаическое упоминание команды («git rm упал») под них не подпадает — и не
# должно: ложное красное дороже пропуска (Шаг 1 захода прямо это разрешает).
# Обратный апостроф пробовали и УБРАЛИ: в этом репо он — markdown-цитирование
# русской прозы (`git_zona.py`), а не подстановка; давал 60+ ложных на корпусе.
SHELL_PAIRS = [("&", "&"), ("$", "("), ("xa", "rgs ")]
SHELL_RE = re.compile("|".join(re.escape(a + b) for a, b in SHELL_PAIRS))
# `rm` с флагом — отдельно и ТОЛЬКО вместе с glob: цена §0 не в самом `rm`, а в
# том, что несовпавший `*` в zsh роняет ВСЮ строку. Без этой связки краснело
# прозаическое предупреждение «никогда не набирай rm -rf вручную».
RM_GLOB_RE = re.compile(re.escape("rm" + " -") + r"\S*\s[^\n]*\*")

# Подкоманды git, которые ПИШУТ. Чтение (`diff`, `ls-files`, `show`) защиты
# песочницы не требует — требовать её значило бы краснеть на здоровых читающих
# инструментах (проверено: так краснели check_kartoteka и check_uroki).
GIT_MUTATING = {"commit", "add", "push", "worktree", "rm", "reset", "clean",
                "checkout", "merge", "init", "gc", "prune", "update-index"}

# Снос на диске. `remove` БЕЗ явного `os.` сюда не входит намеренно: голый
# `.remove(` — это ещё и метод списка (`names.remove(x)`), и на нём линтер
# требовал sandbox-защиту от совершенно безобидного кода.
FS_DESTRUCTIVE = {"rmtree", "unlink"}
FS_DESTRUCTIVE_QUALIFIED = {("os", "remove"), ("os", "rmdir"), ("os", "unlink"),
                            ("os", "removedirs"), ("shutil", "rmtree")}

MARKER_NO_INPUT = "TOOL-CONTRACT: no-input"
MARKER_CALLED_BY_HAND = "TOOL-CONTRACT: called-by-hand"
MARKER_COVERS = "TOOL-CONTRACT-COVERS:"
HELP_TIMEOUT = 10  # секунд: `--help` обязан быть мгновенным, зависший процесс — тоже дефект контракта

# ── КОНТРАКТ ГЕЙТА (рычаг 3) ──────────────────────────────────────────────────
# Три исхода вызова. Снаружи гейт виден ТОЛЬКО кодом возврата: «чисто»,
# «нашёл дефект» и «позвали неверно» обязаны различаться, иначе вызывающий
# (хук, шаг сборки, исполнитель) читает упавший гейт как зелёный.
RC_OK, RC_DEFECT, RC_MISUSE = 0, 1, 2
# Тот же признак «инструмент разбирает вход», что и у check_input_fixture, —
# вынесен, чтобы два пункта контракта судили ОДНО И ТО ЖЕ множество файлов.
INPUT_RE = re.compile(r"\bargparse\b|\bsys\.argv\b|\bargv\b")

# Длина иголки, ниже которой самоцитирование не судим: `"#"`, `"\n"`, `"git "`
# встречаются в прозе любого файла, и «совпало» там ничего не значит.
MIN_NEEDLE = 8
# Что считается СЛУЖЕБНЫМ МАРКЕРОМ: заголовок, флаг, html-комментарий, фенса,
# версальный токен с двоеточием. Обычное слово маркером НЕ считается, и это
# сужение оплачено сплошным прогоном: без него краснели `worktree `, `инцидент`,
# `живая точка вызова` — то есть словарь, а не разметка; совпадение такого слова
# с прозой не значит ничего, а ложное красное на трёх инструментах из четырёх
# гейт хоронит (KONSTITUCIYA §11а). ЦЕНА СУЖЕНИЯ, названная прямо: маркер
# кириллической фразой (`Флаг закрыт:` в sostoyanie.py) проверка ПРОПУСКАЕТ.
MARKER_SHAPE_RE = re.compile(r"^\s*(#{1,6}\s|--\w|<!--|```|\*\*)"
                             r"|[A-ZА-ЯЁ][A-ZА-ЯЁ0-9_-]{3,}\s*[:\-]")
# Имена, за которыми стоит СЫРОЙ ТЕКСТ проверяемого файла. Сужение НАМЕРЕННОЕ и
# оплачено ложным красным на самом этом файле: `"--no-optional-locks" not in vals`
# ищет флаг в СПИСКЕ АРГУМЕНТОВ, а докстринг git_lines этот флаг называет — то
# есть по «иголка встречается в собственной прозе» линтер краснел бы на здоровом
# коде, где никакого самоцитирования нет. Иголку в тексте и иголку в структуре
# надо различать, и различаются они хвостом — тем, ГДЕ ищут.
# Односимвольные и служебные имена (`s`, `out`, `raw`) сюда НЕ входят — тоже по
# живому ложному красному: в `check_optional_locks` через `s` ходят строки
# ШЕЛЛ-КОМАНД, вынутых из проверяемого файла, докстринг же `git_lines` этот флаг
# просто называет — совпасть они не могут никогда, а линтер краснел.
TEXT_HAYSTACKS = {"text", "tekst", "src", "content", "soderzhimoe", "ln", "line",
                  "stroka", "body", "docstring", "proza"}
# Методы, которыми ищут: первый аргумент — иголка.
NEEDLE_METHODS = {"find", "index", "count", "startswith", "endswith", "search",
                  "match", "fullmatch", "findall", "finditer", "split", "partition"}
# Честная приписка «я это не читал». Она — ПОВОД проверить, а не освобождение от
# проверки: гейт, который на неё замолкает, выключается ровно тем, кто должен был
# бы попасться. Собрано из половинок по той же причине, что и GNU_PAIRS выше.
MUTE_PAIRS = [("не", "чита"), ("не", "провер"), ("не", "смотре"), ("не", "сверя"),
              ("без", "проверк"), ("not", "read"), ("not", "checked")]
MUTE_RE = re.compile("|".join([a + r"\s+" + b for a, b in MUTE_PAIRS]
                              + ["unverified", "unchecked"]), re.IGNORECASE)


def check_help(path):
    """`<инструмент> --help` обязан дать rc=0 и непустой вывод.

    Единственное место файла, где инструмент ИСПОЛНЯЕТСЯ — см. исключение из
    закона 2 в докстринге модуля. Не участвует в CHECKS/judge(): те работают
    по staged-тексту и AST, а здесь нужен реальный процесс. Вызывается из
    main() только когда НЕ `--staged`.
    """
    try:
        out = subprocess.run([sys.executable, str(path), "--help"],
                             capture_output=True, text=True,
                             timeout=HELP_TIMEOUT, cwd=str(REPO))
    except subprocess.TimeoutExpired:
        return f"--help не вернулся за {HELP_TIMEOUT}с"
    except OSError as e:
        return f"--help не запустился: {e.__class__.__name__}"
    if out.returncode != 0:
        return f"--help вернул rc={out.returncode} (нужен 0)"
    if not out.stdout.strip():
        return "--help вернул rc=0, но пустой вывод"
    return None


def git_lines(*args):
    """Единственная дверь к git. `--no-optional-locks`: чтение не берёт лок и не
    переписывает индекс — голый `git` тут ронял чужой коммит (канон §0)."""
    out = subprocess.run(["git", "--no-optional-locks", *args],
                         capture_output=True, text=True, cwd=str(REPO))
    if out.returncode != 0:
        return []
    return [ln for ln in out.stdout.splitlines() if ln.strip()]


def staged_paths():
    """Пути под контрактом среди staged: инструменты и то, что исполняется рядом.

    Подпапки тоже: `_generator/tools/lib/x.py` — такой же инструмент, а прежний
    `[^/]*.py` оставлял бы его вне гейта навсегда.
    """
    out = []
    for p in git_lines("diff", "--cached", "--name-only", "--diff-filter=ACMR"):
        if p.startswith(TOOLS_REL + "/") and p.endswith(".py"):
            out.append(p)
        elif p.startswith(".githooks/") or (p.startswith(TOOLS_REL + "/fixtures/")
                                            and p.endswith(".sh")):
            out.append(p)
    return out


def staged_text(rel):
    """Текст ИЗ ИНДЕКСА, а не с диска.

    🔴 Это не педантизм. Коммит несёт то, что застейджено: поправил файл ПОСЛЕ
    `add` — на диске чисто, а в коммит уезжает нарушитель. Линтер, читающий
    рабочую копию, в этом случае зелёный, и гейт врёт ровно в ту сторону, ради
    которой заводился (поймано верификатором на живом сценарии «поправил после
    add» — рутина, а не трюк).
    """
    out = subprocess.run(["git", "--no-optional-locks", "show", f":{rel}"],
                         capture_output=True, text=True, cwd=str(REPO))
    return out.stdout if out.returncode == 0 else None


def added_lines(rel):
    """Номера строк, ДОБАВЛЕННЫХ этим коммитом.

    Судим их, а не файл целиком: пре-существующее нарушение не должно валить
    чужой коммит. Иначе `git_zona.py` — самый правимый инструмент репозитория —
    становится незакоммитабельным с первого дня жизни гейта из-за строки,
    которой правящий не касался. Это ровно «гейт бьёт по своим», после чего его
    отключают (Р31), и никакого контракта больше нет.
    """
    lines = set()
    for ln in git_lines("diff", "--cached", "-U0", "--", rel):
        if not ln.startswith("@@"):
            continue
        m = re.search(r"\+(\d+)(?:,(\d+))?", ln)
        if m:
            start, count = int(m.group(1)), int(m.group(2) or 1)
            lines.update(range(start, start + count))
    return lines


def baseline_names():
    """Инструменты, жившие ДО контракта. Освобождены ТОЛЬКО от требования
    фикстуры — переносимость, локи, shell и sandbox-guard судят их в полную силу.

    Зачем список вообще: без него первая же правка любого из восьми инструментов
    без фикстуры остановила бы здоровый коммит, а завести фикстуру в тот момент
    правящему негде. Долг тут виден строкой и тает по мере обрастания фикстурами.
    """
    if not BASELINE.exists():
        return set()
    names = set()
    for ln in BASELINE.read_text(encoding="utf-8").splitlines():
        ln = ln.split("#")[0].strip()
        if ln:
            names.add(ln)
    return names


def fixture_coverage():
    """{фикстура: {покрытые имена файлов}}.

    Охват объявляет САМА фикстура строкой-шапкой: решётка, маркер MARKER_COVERS,
    имена файлов через пробел. Маркер здесь НЕ выписан буквально — он собирается
    из константы, иначе эта самая строка документации попадала бы под собственный
    поиск (проверка «самоцитирование маркера» ловит ровно такую пару).
    Это и есть лечение зазора «триггер уже охвата»: пока охват жил в голове
    автора, хук поднимал фикстуру git_zona только на правку git_zona.py, хотя
    ловушка 14 внутри неё сторожит три bootstrap_*.
    Фикстура без объявления покрывает `<имя папки>.py` — старое поведение.
    """
    cover = {}
    if not FIXTURES.exists():
        return cover
    for script in sorted(FIXTURES.glob("*/PROGNAT.sh")):
        names = set()
        # ТОЛЬКО шапка: иначе объявление подделывается строкой внутри heredoc с
        # тестовыми данными — и посторонняя фикстура «покрывает» инструмент, ничего
        # о нём не зная. Тот же зазор был и у самой мета-фикстуры контракта.
        for ln in script.read_text(encoding="utf-8", errors="replace").splitlines()[:15]:
            if ln.lstrip().startswith("#") and MARKER_COVERS in ln:
                names.update(ln.split(MARKER_COVERS, 1)[1].split())
        cover[script] = names or {script.parent.name + ".py"}
    return cover


def docstring_lines(tree):
    """Номера строк, занятых докстрингами.

    Докстринг — такая же документация, как комментарий: он объясняет, ЧЕГО
    делать нельзя, и владельцу не печатается. Не выведи его — линтер краснеет
    на собственном описании запрещённых конструкций (поймано первой калибровкой).
    """
    lines = set()
    if tree is None:                 # не питон (фикстура, хук) — докстрингов нет
        return lines
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                                 ast.ClassDef)):
            continue
        body = getattr(node, "body", None)
        if not body:
            continue
        first = body[0]
        if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) \
                and isinstance(first.value.value, str):
            lines.update(range(first.lineno, (first.end_lineno or first.lineno) + 1))
    return lines


def code_lines(path, text, tree):
    """Строки файла БЕЗ комментариев и докстрингов: `(номер, текст)`.

    Обычные строковые литералы, наоборот, ОСТАЮТСЯ: GNU-изм, напечатанный
    владельцу, ломается на его macOS ровно так же, как исполненный.
    """
    skip = docstring_lines(tree)
    if tree is None:
        # В shell комментарий — только строка, начинающаяся с `#`; питоновский
        # tokenize к ней неприменим.
        return [(n, "" if ln.lstrip().startswith("#") else ln)
                for n, ln in enumerate(text.splitlines(), 1)]
    try:
        # Токенизируем ПЕРЕДАННЫЙ текст, а не файл с диска: в режиме хука текст
        # приходит из индекса, и рабочая копия может от него отличаться.
        # Колонка, а не split("#"): решётка бывает внутри строки, и резать по
        # первой значило бы терять код слева от неё.
        comments = {t.start[0]: t.start[1]
                    for t in tokenize.generate_tokens(io.StringIO(text).readline)
                    if t.type == tokenize.COMMENT}
    except (tokenize.TokenError, SyntaxError, IndentationError, ValueError):
        comments = {}
    out = []
    for n, ln in enumerate(text.splitlines(), 1):
        if n in skip:
            continue
        if n in comments:
            ln = ln[:comments[n]]
        out.append((n, ln))
    return out


def printed_strings(tree):
    """Строки, которые инструмент ПЕЧАТАЕТ владельцу."""
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "print"):
            continue
        for arg in node.args:
            for sub in ast.walk(arg):
                if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                    yield sub.value, getattr(sub, "lineno", node.lineno)


def arglists(tree):
    """Списки строковых литералов: `(узел, значения)`.

    Список из ОДНОГО элемента пропускаем: `["git"] + FLAGS + ["diff"]` — это
    сборка команды по кускам, и судить огрызок значило бы краснеть на здоровом.
    """
    for node in ast.walk(tree):
        if not isinstance(node, ast.List) or len(node.elts) < 2:
            continue
        vals = [e.value for e in node.elts
                if isinstance(e, ast.Constant) and isinstance(e.value, str)]
        if vals:
            yield node, vals


def git_arglists(tree):
    """Списки вида `["git", …]` — так инструмент зовёт git."""
    for node, vals in arglists(tree):
        if vals and vals[0] == "git":
            yield node, vals


def shell_commands(tree):
    """Команды, отданные ШЕЛЛУ строкой: `os.system("…")`, `run("…", shell=True)`.

    Мимо разбора списка аргументов проходит всё: и `--no-optional-locks`, и
    запрет записи. Верификатор назвал эту форму естественным стилем, а не
    обходом, — значит её и надо ловить.
    """
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = node.func.attr if isinstance(node.func, ast.Attribute) else \
            node.func.id if isinstance(node.func, ast.Name) else ""
        shell = any(k.arg == "shell" and getattr(k.value, "value", False) is True
                    for k in node.keywords)
        if name not in ("system", "popen") and not shell:
            continue
        for arg in node.args:
            for sub in ast.walk(arg):
                if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                    yield sub.value, getattr(sub, "lineno", node.lineno)


def call_name(func):
    """`sys.exit` / `os.remove` / `print` — имя вызываемого одной строкой."""
    if isinstance(func, ast.Attribute):
        owner = func.value.id if isinstance(func.value, ast.Name) else ""
        return f"{owner}.{func.attr}" if owner else func.attr
    return func.id if isinstance(func, ast.Name) else ""


def base_name(node):
    """Имя, в котором лежит haystack: у `ln.lstrip().startswith(x)` это `ln`."""
    while isinstance(node, (ast.Call, ast.Attribute, ast.Subscript)):
        node = node.func if isinstance(node, ast.Call) else node.value
    return node.id if isinstance(node, ast.Name) else ""


def module_constants(tree):
    """`{ИМЯ: значение}` для присваиваний ВЕРХНЕГО УРОВНЯ (строки и целые).

    Нужна, потому что и маркер, и код возврата приличный инструмент держит
    константой (`MARKER_NO_INPUT`, `RC_MISUSE`), а не литералом по месту. Гейт,
    умеющий только литералы, объявил бы такой инструмент нарушителем — это ровно
    «гейт бьёт по своим», после чего его отключают (Р31).
    """
    out = {}
    if tree is None:
        return out
    def zapomnit(target, value):
        if not (isinstance(target, ast.Name) and isinstance(value, ast.Constant)):
            return
        val = value.value
        if isinstance(val, (str, int)) and not isinstance(val, bool):
            out[target.id] = val

    for node in getattr(tree, "body", []):
        if not isinstance(node, ast.Assign):
            continue
        for t in node.targets:
            # `RC_OK, RC_DEFECT, RC_MISUSE = 0, 1, 2` — ровно та форма, которой
            # объявляют набор кодов возврата; не разобрав её, проверка «три
            # исхода» краснела на инструменте, где все три кода на месте
            # (поймано первым же прогоном на самом этом файле).
            if isinstance(t, ast.Tuple) and isinstance(node.value, ast.Tuple):
                for tt, vv in zip(t.elts, node.value.elts):
                    zapomnit(tt, vv)
            else:
                zapomnit(t, node.value)
    return out


def str_value(node, consts):
    """Строковое значение узла: литерал или имя модульной константы."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name):
        v = consts.get(node.id)
        return v if isinstance(v, str) else None
    return None


def int_value(node, consts):
    """Целое значение узла: литерал или имя модульной константы."""
    if isinstance(node, ast.Constant) and isinstance(node.value, int) \
            and not isinstance(node.value, bool):
        return node.value
    if isinstance(node, ast.Name):
        v = consts.get(node.id)
        return v if isinstance(v, int) and not isinstance(v, bool) else None
    return None


def needles(node, consts):
    """Строки, которые инструмент ИЩЕТ, и место поиска: `(иголка, строка, стог)`.

    Формы: `X in text`, `text.find(X)`, `re.search(X, text)`, `ln.split(X)`.
    Ходит по ЛЮБОМУ поддереву — так один механизм кормит и самоцитирование
    маркера, и глушилку «не читан».
    """
    for sub in ast.walk(node):
        if isinstance(sub, ast.Compare) and \
                any(isinstance(o, (ast.In, ast.NotIn)) for o in sub.ops):
            v = str_value(sub.left, consts)
            if v is not None:
                yield v, sub.lineno, base_name(sub.comparators[0])
        elif isinstance(sub, ast.Call) and sub.args:
            name = sub.func.attr if isinstance(sub.func, ast.Attribute) else \
                sub.func.id if isinstance(sub.func, ast.Name) else ""
            if name not in NEEDLE_METHODS:
                continue
            v = str_value(sub.args[0], consts)
            if v is None:
                continue
            # `re.search(X, text)` — стог вторым аргументом; `text.find(X)` — слева
            hay = sub.args[1] if len(sub.args) > 1 else \
                sub.func.value if isinstance(sub.func, ast.Attribute) else None
            yield v, sub.lineno, base_name(hay) if hay is not None else ""


def prose_lines(text, tree):
    """`(номер, текст)` для строк ДОКУМЕНТАЦИИ — комментариев и докстрингов.

    Ровно дополнение `code_lines()`: там документация выбрасывается как «не
    исполняется», здесь она и есть предмет — самоцитирование живёт именно в ней.
    """
    doc = docstring_lines(tree)
    comments = {}
    if tree is not None:
        try:
            comments = {t.start[0]: t.start[1]
                        for t in tokenize.generate_tokens(io.StringIO(text).readline)
                        if t.type == tokenize.COMMENT}
        except (tokenize.TokenError, SyntaxError, IndentationError, ValueError):
            comments = {}
    out = []
    for n, ln in enumerate(text.splitlines(), 1):
        if n in doc:
            out.append((n, ln))
        elif n in comments:
            out.append((n, ln[comments[n]:]))
    return out


def rc_functions(tree, consts=None):
    """Функции, чей `return N` — КОД ВОЗВРАТА, а не число.

    `main` по имени, всё, что само зовёт `sys.exit(...)`, и всё, что возвращает
    литеральные 1 или 2. Сужение НАМЕРЕННОЕ: без него «пустой вход даёт зелёное»
    краснело бы на честном `if not items: return 0` внутри счётчика — а там ноль
    это сумма, а не исход вызова.
    """
    consts = consts or {}
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.name == "main":
            out.append(node)
            continue
        codes, exits = set(), False
        for sub in ast.walk(node):
            if isinstance(sub, ast.Call) and call_name(sub.func) in ("sys.exit", "exit"):
                exits = True
            elif isinstance(sub, ast.Return) and sub.value is not None:
                v = int_value(sub.value, consts)
                if v is not None:
                    codes.add(v)
        if exits or {RC_DEFECT, RC_MISUSE} & codes:
            out.append(node)
    return out


def exit_codes(tree, consts):
    """Коды, которыми инструмент РЕАЛЬНО умеет завершиться."""
    codes = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and call_name(node.func) in ("sys.exit", "exit"):
            codes.add(int_value(node.args[0], consts) if node.args else RC_OK)
    for fn in rc_functions(tree, consts):
        for node in ast.walk(fn):
            if isinstance(node, ast.Return) and node.value is not None:
                codes.add(int_value(node.value, consts))
    return {c for c in codes if c is not None}


def has_entry(text, tree):
    """У файла есть точка входа: он кому-то ОТДАЁТ код возврата."""
    if re.search(r"__name__\s*==", text):
        return True
    return any(isinstance(n, ast.Call) and call_name(n.func) in ("sys.exit", "exit")
               for n in ast.walk(tree))


def green_body(stmts):
    """Ветка означает «всё хорошо, дальше не смотрим»: пустой возврат, ноль,
    `True`, `continue`, `pass` — и НИ ОДНОГО слова владельцу."""
    if not stmts:
        return False
    for node in stmts:
        for sub in ast.walk(node):
            if isinstance(sub, ast.Call) and call_name(sub.func) in ("print", "warn"):
                return False
    last = stmts[-1]
    if isinstance(last, (ast.Continue, ast.Pass)):
        return True
    if not isinstance(last, ast.Return):
        return False
    if last.value is None:
        return True
    v = last.value
    if isinstance(v, (ast.List, ast.Tuple, ast.Set)) and not v.elts:
        return True
    if isinstance(v, ast.Dict) and not v.keys:
        return True
    return isinstance(v, ast.Constant) and v.value in (0, True, "", None)


READ_METHODS = {"read_text", "read", "read_bytes", "readlines"}


def input_names(fn):
    """Имена, в которых лежит ВХОД, ДАННЫЙ ВЫЗЫВАЮЩИМ: список путей из разбора
    аргументов (`paths = a.paths`, `sys.argv`) и содержимое файла (`.read_text()`).

    🔴 Сужение до этих двух источников — не лень, а РАЗДЕЛЕНИЕ ДВУХ ПУСТОТ,
    которые иначе стравливают Р5-3 и Р31 лбами. «Пустой вход» (нечего было
    проверять) и «пустой результат» (проверил и не нашёл) выглядят в коде
    ОДИНАКОВО — `if not X: return 0`, — а означают противоположное: первое обязано
    сказать, второе обязано молчать. Отличить их можно только по происхождению X.
    ЦЕНА, найденная сплошным прогоном ДО этого сужения: краснели
    `check_marker.py` (`if not broken`) и `dnevnik.py` (`if not nepokrytye`) —
    то есть образцовое исполнение Р31 объявлялось нарушением Р5-3.
    ЦЕНА СУЖЕНИЯ, названная прямо: вход, пропущенный через фильтр (`targets = [p
    for p in paths if …]`), проверка уже не считает входом и пропускает.
    """
    ns, out = set(), set()
    for node in ast.walk(fn):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call) \
                and call_name(node.value.func).endswith("parse_args"):
            ns.update(t.id for t in node.targets if isinstance(t, ast.Name))
    for node in ast.walk(fn):
        if not isinstance(node, ast.Assign):
            continue
        tgt = {t.id for t in node.targets if isinstance(t, ast.Name)}
        if not tgt:
            continue
        for sub in ast.walk(node.value):
            if isinstance(sub, ast.Attribute) and (
                    sub.attr == "argv"
                    or (isinstance(sub.value, ast.Name) and sub.value.id in ns)):
                out |= tgt
            elif isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute) \
                    and sub.func.attr in READ_METHODS:
                out |= tgt
    return out


def emptiness_test(node):
    """Имя, о пустоте которого спрашивают: `not X`, `len(X) == 0`, `X == []`,
    `X == ""`. Не тест на пустоту — `None`.

    Флаги режима (`if a.staged`) сюда НЕ попадают намеренно: «нечего судить,
    потому что режим такой» и «дали пустоту» — разные вещи, и молчаливое зелёное
    законно только в первом случае (Р31 против Р5-3).
    """
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        inner = node.operand
        if isinstance(inner, ast.Call) and call_name(inner.func) == "len" \
                and inner.args:
            return base_name(inner.args[0])
        if isinstance(inner, (ast.Name, ast.Attribute, ast.Subscript)):
            return base_name(inner)
        return None
    if isinstance(node, ast.Compare) and len(node.ops) == 1 \
            and isinstance(node.ops[0], ast.Eq):
        left, right = node.left, node.comparators[0]
        if isinstance(left, ast.Call) and call_name(left.func) == "len" \
                and left.args and int_value(right, {}) == 0:
            return base_name(left.args[0])
        if isinstance(right, (ast.List, ast.Tuple, ast.Set)) and not right.elts:
            return base_name(left)
        if isinstance(right, ast.Constant) and right.value == "":
            return base_name(left)
    return None


# ── ПРОВЕРКИ ──────────────────────────────────────────────────────────────────
# Каждая — кодификация УЖЕ ОПЛАЧЕННОГО урока, а не новое пожелание.

def check_gnuisms(path, text, tree, ctx):
    """Кластер B. Инструменты исполняются на macOS владельца (BSD), а пишутся в
    Linux-песочнице (GNU). ЦЕНА 23.07: `touch -d` в фикстуре остановил здоровый
    коммит владельца, оставаясь зелёным у автора."""
    bad = []
    for n, ln in code_lines(path, text, tree):
        m = GNU_RE.search(ln)
        if m:
            bad.append((n, m.group(0)))
    if tree is not None:
        # тот же GNU-изм, разнесённый по элементам списка аргументов
        for node, vals in arglists(tree):
            flags = GNU_ARGV.get(vals[0])
            if flags and flags & set(vals[1:]):
                hit = sorted(flags & set(vals[1:]))[0]
                bad.append((node.lineno, f"{vals[0]} {hit}"))
    return [f"строка {n}: GNU-изм «{s}» — на macOS владельца ведёт себя иначе; "
            f"нетривиальный системный вызов делают через python3 -c" for n, s in bad]


def check_optional_locks(path, text, tree, ctx):
    """Кластер B. Голый git переписывает индекс и берёт `.git/index.lock` —
    так гейт, следивший за потерями, сам сорвал три коммита за сессию 21.07."""
    bad = []
    for node, vals in git_arglists(tree):
        if "--no-optional-locks" not in vals:
            bad.append(node.lineno)
    for s, n in shell_commands(tree):
        if re.search(r"\bgit\s", s) and "--no-optional-locks" not in s:
            bad.append(n)
    return [f"строка {n}: вызов git без `--no-optional-locks` — чтение возьмёт лок "
            f"и уронит параллельный коммит" for n in sorted(set(bad))]


def check_shell_to_owner(path, text, tree, ctx):
    """Канон §0. Cowork пишет в bash/Linux, владелец исполняет в zsh/macOS —
    выданный shell ломается систематически (несовпавший glob роняет всю строку,
    обрыв `&&` невидим). Владельцу печатают `git_zona.py <команда>`, не shell."""
    bad = []
    for s, n in printed_strings(tree):
        m = SHELL_RE.search(s) or RM_GLOB_RE.search(s)
        if m:
            bad.append((n, m.group(0).strip()[:40]))
    return [f"строка {n}: владельцу печатается сырой shell («{s}») — вместо него "
            f"должна печататься подкоманда git_zona.py (канон §0)" for n, s in bad]


def check_sandbox_guard(path, text, tree, ctx):
    """Кластеры E/B. Пишущая операция из песочницы Cowork оставляет мины в `.git`:
    репозиторий дважды вставал на полчаса для ВСЕХ писателей (22.07). Проверяем
    ПРИСУТСТВИЕ защиты, а не её работу — работу держит фикстура git_zona."""
    writes = []
    # (а) git-мутация списком аргументов: ["git", …, "commit", …]
    for node, vals in git_arglists(tree):
        hit = [v for v in vals[1:] if v in GIT_MUTATING]
        if hit:
            writes.append((node.lineno, f"git {hit[0]}"))
    # (б) команда шеллу строкой: os.system("git commit …")
    for s, n in shell_commands(tree):
        hit = [w for w in GIT_MUTATING if re.search(rf"\bgit\s+(-\S+\s+)*{w}\b", s)]
        if hit:
            writes.append((n, f"git {hit[0]}"))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = node.func.id if isinstance(node.func, ast.Name) else \
            node.func.attr if isinstance(node.func, ast.Attribute) else ""
        owner = node.func.value.id if isinstance(node.func, ast.Attribute) \
            and isinstance(node.func.value, ast.Name) else ""
        # (в) вызов обёртки: git("commit", …) — так пишет сам git_zona.py
        if name == "git" and node.args and isinstance(node.args[0], ast.Constant) \
                and node.args[0].value in GIT_MUTATING:
            writes.append((node.lineno, f"git {node.args[0].value}"))
        # (г) снос на диске: shutil.rmtree / os.remove / Path.unlink
        elif name in FS_DESTRUCTIVE or (owner, name) in FS_DESTRUCTIVE_QUALIFIED:
            writes.append((node.lineno, f"{owner}.{name}" if owner else name))
    if not writes:
        return []
    if "in_sandbox" in text or "refuse_write" in text:
        return []
    where, what = sorted(writes)[0]
    return [f"строка {where}: инструмент ПИШЕТ ({what}), но не ссылается на "
            f"in_sandbox/refuse_write — из песочницы такая запись кладёт мины в "
            f".git, и репозиторий встаёт для всех троих писателей ({CANON} §2)"]


def check_input_fixture(path, text, tree, ctx):
    """Кластер A. Кривой вход обязан падать ГРОМКО, а не тихо делать не то:
    `bootstrap_arka.py --help` проглотил флаг как имя арки и создал папку-сироту,
    которую потом каждый `plan` тянул в черновик коммита (23.07).

    Линтер проверяет НАЛИЧИЕ доказательства (фикстура или явная пометка) и
    мусорный вход сам НЕ подаёт — подать значило бы исполнить боевой инструмент.
    """
    if MARKER_NO_INPUT in text:
        return []
    if not re.search(r"\bargparse\b|\bsys\.argv\b|\bargv\b", text):
        return []
    if path.name in ctx["baseline"]:
        return []
    covered = any(path.name in names for names in ctx["cover"].values())
    if covered:
        return []
    return [f"инструмент разбирает вход, но ничто не доказывает, что кривой вход "
            f"он отвергает: нет спутник-фикстуры (объявить охват строкой "
            f"`# {MARKER_COVERS} {path.name}` в fixtures/*/PROGNAT.sh) и нет "
            f"пометки `# {MARKER_NO_INPUT}`"]


def live_trigger_scope():
    """Файлы, где может жить реальный вызов инструмента: сам дом инструментов
    (`HOME_DIR` — та же дверь, что у FIXTURES/BASELINE, работает и в фикстуре),
    плюс сиблинги в бою (`_generator/*.py`, `_generator/sborka/*.py`,
    `.githooks/*`) через REPO.

    🔴 `_generator/sborka/` добавлена 09.08 (заход `gigiena-i-svedenie`) — и это
    починка ЛОЖНОГО КРАСНОГО, а не расширение «на всякий случай». `REPO/_generator`
    обходился `iterdir()` с `p.is_file()`, то есть подпапка отсеивалась, — а
    боевой конвейер сборки живёт именно там. Замер до починки: `bloki.py`,
    `korpus.py`, `podgonka.py` числились «нигде не вызываются», хотя импортируются
    соседями (`bloki` — из `formaty/bootstrap_lekcii/lenta/gejt_kartochki/smeta`,
    `korpus` и `podgonka` — из `vmeshchenie`, `podgonka` ещё из `zamer_smety`).
    Три ложных красных из шести на сплошном прогоне — половина; гейт с такой
    долей ложных срабатываний обходят, а не чинят по нему (`KONSTITUCIYA §11а`).
    Тот же пробел заставлял ГЕЙТЫ этой папки зеленеть только маркером
    `called-by-hand`: у `gejt_vmeshcheniya.py` строка «ФАЗА 3.9» в
    `bootstrap_lekcii.LIFECYCLE_TMPL` есть, а увидеть её проверке было нечем."""
    paths = list(HOME_DIR.glob("*.py"))
    for extra in (REPO / "_generator", REPO / "_generator" / "sborka",
                  REPO / ".githooks"):
        if extra.is_dir():
            paths += [p for p in extra.iterdir() if p.is_file()]
    return paths


def has_live_trigger(name):
    """Инструмент `name` (basename) реально упомянут ВНЕ собственного файла —
    та же текстовая эвристика, что и замер Ш1 захода `instrument-podklyuchen`
    (грепом среди `_generator/tools/*.py _generator/*.py .githooks/*`)."""
    for p in live_trigger_scope():
        if p.name == name:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if name in text:
            return True
    return False


def check_live_trigger(path, text, tree, ctx):
    """Кластер F (заход `instrument-podklyuchen`, 2026-08-08). Написанный, но
    нигде не вызываемый гейт не гейт: он зелёный только потому, что его никто
    не звал — шесть живых случаев на дату замера (`proverka_pomarok.py`,
    `gejt_illyustracij.py`, `graf_zavisimostej.py`, `check_lenta.py`,
    `reviziya_dolgov.py`, `sdelat_handoff.py`), половина из них — гейты,
    обязанные срабатывать сами, половина — законно вызываемые руками.
    Инструмент обязан ЛИБО реально упоминаться вне собственного файла (хук,
    другой инструмент, шаг сборки), ЛИБО нести явный маркер «зовут руками» —
    третьего не дано, и «я потом подключу» не считается.

    🔴 Исключение: файлы ВНУТРИ `fixtures/` (не сам `PROGNAT.sh`, а `.py`-нагрузка
    рядом с ним, например `fixtures/sborka/obratnyj-progon/*.py`) — это данные
    ОДНОЙ фикстуры, не инструмент фабрики; у них нет и не может быть своей точки
    вызова, требовать её значило бы красить исторические файлы захода задним
    числом (найдено живым прогоном `--all`, 2026-08-08)."""
    if "fixtures" in path.parts:
        return []
    if MARKER_CALLED_BY_HAND in text:
        return []
    if has_live_trigger(path.name):
        return []
    return [f"инструмент нигде не упоминается как вызываемый (хук/другой "
            f"инструмент/шаг сборки) и не несёт маркера `# {MARKER_CALLED_BY_HAND}` — "
            f"либо подключи живую точку вызова, либо объяви инструмент по вызову"]


def check_rc_outcomes(path, text, tree, ctx):
    """🔴 РЫЧАГ 3, пункт 1. Снаружи гейт виден ТОЛЬКО кодом возврата, и трёх
    исходов там обязано быть три: чисто (0), нашёл дефект (1), позвали неверно
    (2 — нет аргумента, нет файла, неизвестный флаг). Пока кода 2 нет, «гейт
    упал, потому что я дал ему несуществующий путь» и «гейт нашёл дефект»
    снаружи ОДНО И ТО ЖЕ число, а «гейт вообще не отработал» читается как
    зелёное — то есть проверка выключается опечаткой в вызове, и никто этого
    не видит.

    🔴 ЧЕГО ЭТА ПРОВЕРКА НЕ ДОКАЗЫВАЕТ, и это НЕ придирка к формулировке:
    она видит ПРИСУТСТВИЕ различения в тексте, а не то, что коды расставлены
    по верным веткам. Проверить последнее можно было бы только ЗАПУСТИВ
    инструмент с кривым входом — ровно то, что запрещает закон 2 модуля, и
    запрещает не из перестраховки: `bootstrap_arka.py --help` проглотил флаг
    как имя арки и создал папку-сироту. Присутствие защиты вместо её работы —
    та же сделка, что у check_sandbox_guard; работу держит фикстура.

    argparse отдаёт rc=2 сам, но ТОЛЬКО на неизвестный флаг: «нет аргумента» и
    «файла не существует» — на инструменте, и именно они молча превращаются в 1.
    Требуем кода 2, а не кода 1: гейтом инструмент быть не обязан (bootstrap_*
    законно живёт на 0/2), а вот отличить «позвали неверно» обязан любой.
    """
    if "fixtures" in path.parts:
        return []
    if not INPUT_RE.search(text) or not has_entry(text, tree):
        return []
    codes = exit_codes(tree, module_constants(tree))
    if RC_MISUSE in codes:
        return []
    est = ", ".join(str(c) for c in sorted(codes)) or "ни одного"
    return [f"инструмент разбирает вход и отдаёт код возврата, но кода "
            f"{RC_MISUSE} («позвали неверно»: нет аргумента, нет файла, "
            f"неизвестный флаг) среди его исходов нет — есть {est}; снаружи "
            f"неверный вызов неотличим от «чисто» ({RC_OK}) или «нашёл "
            f"дефект» ({RC_DEFECT})"]


def check_marker_echo(path, text, tree, ctx):
    """🔴 РЫЧАГ 3, пункт 2. Служебный маркер, который инструмент ИЩЕТ в чужом
    тексте, стоит буквально в его собственной документации — и гейт находит сам
    себя: документация о маркере либо краснит свой же файл, либо (хуже) даёт
    ему поблажку, которую маркер и раздаёт. Лечение известно и уже применено в
    этом файле: GNU_PAIRS и SHELL_PAIRS склеены из половинок, потому что иначе
    линтер краснел на собственном списке запрещённого (поймано первой же
    калибровкой). Здесь тот же приём выдан МЕХАНИЗМОМ, а не памятью автора.

    Судим только иголки длиной от MIN_NEEDLE и только те, что ищут в СЫРОМ
    ТЕКСТЕ (TEXT_HAYSTACKS): иголка в списке аргументов — не самоцитирование,
    см. ложное красное на `--no-optional-locks` в комментарии к TEXT_HAYSTACKS.
    """
    consts = module_constants(tree)
    prose = prose_lines(text, tree)
    seen, bad = set(), []
    for value, _, hay in needles(tree, consts):
        if len(value.strip()) < MIN_NEEDLE or value in seen:
            continue
        if hay not in TEXT_HAYSTACKS or not MARKER_SHAPE_RE.search(value):
            continue
        for n, s in prose:
            if value in s:
                seen.add(value)
                bad.append((n, value))
                break
    return [f"строка {n}: служебный маркер «{v}», который инструмент ИЩЕТ в "
            f"проверяемом тексте, стоит буквально в его собственной прозе — "
            f"гейт находит сам себя; собирай маркер из половинок, как GNU_PAIRS"
            for n, v in sorted(bad)]


def check_mute_phrase(path, text, tree, ctx):
    """🔴 РЫЧАГ 3, пункт 3. Честная приписка «этот файл я не читал» / «не
    проверял» в проверяемом тексте ВЫКЛЮЧАЕТ проверку. Так гейт отключается
    ровно тем, кто должен был на нём попасться, и отключается тихо: снаружи это
    неотличимо от «проверено, чисто». Непрочитанность — ПОВОД проверить, а не
    освобождение от проверки.

    Красим только ГЛУШИЛКУ: фраза в условии, чья ветка молчит и возвращает
    «всё хорошо» (green_body). Гейт, который ту же фразу ЛОВИТ и о ней
    докладывает, — здоровый и обязан пройти; без этого различения проверка
    краснела бы на честных гейтах, сторожащих эту самую приписку.
    """
    consts = module_constants(tree)
    bad = []
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            test, body = node.test, node.body
        elif isinstance(node, ast.IfExp):
            test, body = node.test, [ast.Return(value=node.body)]
        else:
            continue
        hits = [v for v, _, _ in needles(test, consts) if MUTE_RE.search(v)]
        if hits and green_body(body):
            bad.append((node.lineno, hits[0][:40]))
    return [f"строка {n}: приписка «{v}» ГЛУШИТ проверку — ветка молча "
            f"возвращает «чисто»; непрочитанность это повод проверить, а не "
            f"освобождение от проверки" for n, v in sorted(set(bad))]


def check_empty_green(path, text, tree, ctx):
    """🔴 РЫЧАГ 3, пункт 4 (Р5-3 дословно). Гейт, которому дали пустой файл или
    пустой список, обязан НЕ МОЛЧАТЬ ЗЕЛЁНЫМ: молчаливый ноль на пустоте — это
    «проверено, всё хорошо» на языке вызывающего, хотя проверено ровно ничто.
    Так пустой охват, опечатка в маске и не собравшийся список выглядят как
    здоровый прогон.

    Судим ТОЛЬКО функции, чей возврат — код (rc_functions), только пустоту
    ВХОДА, ДАННОГО ВЫЗЫВАЮЩИМ (input_names — там же цена сужения и два живых
    ложных красных), и только МОЛЧАЛИВУЮ ветку: сказать «нечего проверять:
    0 файлов» и вернуть 0 — законно, это уже не молчание. Тест на РЕЖИМ
    (`if a.staged: return 0`) под проверку не подпадает — пустой staged обязан
    молчать (Р31), и путать эти два случая значило бы стравить два правила лбами.
    """
    consts = module_constants(tree)
    bad = []
    for fn in rc_functions(tree, consts):
        inputs = input_names(fn)
        for node in ast.walk(fn):
            if not isinstance(node, ast.If):
                continue
            name = emptiness_test(node.test)
            if not name or name not in inputs:
                continue
            if not green_body(node.body):
                continue
            last = node.body[-1]
            green = isinstance(last, ast.Return) and last.value is not None \
                and int_value(last.value, consts) == RC_OK
            if not green:
                green = any(isinstance(s, ast.Call)
                            and call_name(s.func) in ("sys.exit", "exit")
                            and s.args and int_value(s.args[0], consts) == RC_OK
                            for s in ast.walk(node))
            if green:
                bad.append(node.lineno)
    return [f"строка {n}: пустой вход даёт МОЛЧАЛИВОЕ зелёное (rc={RC_OK} без "
            f"единого слова) — «проверено ничто» уезжает к вызывающему как "
            f"«проверено, чисто» (Р5-3); скажи, что проверять было нечего, или "
            f"верни {RC_MISUSE}" for n in sorted(set(bad))]


CHECKS = [
    ("переносимость", check_gnuisms),
    ("--no-optional-locks", check_optional_locks),
    ("shell владельцу", check_shell_to_owner),
    ("запрет записи из песочницы", check_sandbox_guard),
    ("кривой вход", check_input_fixture),
    ("живая точка вызова", check_live_trigger),
    ("три исхода rc", check_rc_outcomes),
    ("самоцитирование маркера", check_marker_echo),
    ("глушилка «не читан»", check_mute_phrase),
    ("пустой вход = зелёное", check_empty_green),
]


LINE_RE = re.compile(r"строка (\d+)")


def judge(targets, verbose=False):
    """`targets` — список `(путь, текст, только_эти_строки|None)`.

    `только_эти_строки` — добавленные коммитом; остальное не судим, чтобы чужой
    долг не валил чужой коммит. `None` = судить всё (калибровка, явные пути).
    """
    ctx = {"baseline": baseline_names(), "cover": fixture_coverage()}
    total = 0
    for path, text, only in targets:
        shown = path.relative_to(REPO) if REPO in path.parents else path
        if path.suffix == ".py":
            try:
                tree = ast.parse(text, filename=str(path))
            except (SyntaxError, ValueError) as e:
                print(f"❌ {shown}: не разбирается ({e.__class__.__name__}) — "
                      f"контракт проверить нельзя")
                total += 1
                continue
            checks = CHECKS
        else:
            # Фикстуры и хуки исполняются у ВЛАДЕЛЬЦА и потому тоже под контрактом
            # — но по-питоновьи не разбираются: им достаётся только переносимость.
            # Без этого GNU-изм в .sh оставался вне гейта, а именно им и оплачен
            # урок 23.07 (`touch -d` в фикстуре остановил здоровый коммит).
            tree, checks = None, [c for c in CHECKS if c[0] == "переносимость"]
        hits = []
        for name, fn in checks:
            for msg in fn(path, text, tree, ctx):
                m = LINE_RE.search(msg)
                if only is not None and m and int(m.group(1)) not in only:
                    continue
                hits.append(f"   [{name}] {msg}")
        if hits:
            total += len(hits)
            print(f"❌ {shown}")
            for h in hits:
                print(h)
        elif verbose:
            print(f"   ✅ {path.name}")
    return total


def read_targets(paths, staged):
    """Собрать `(путь, текст, только_эти_строки)`. В режиме хука — ИЗ ИНДЕКСА.

    Возвращает `(цели, сколько_раз_позвали_неверно)`. Несуществующий или
    нечитаемый путь — это НЕ дефект инструмента, а неверный вызов, и уезжает он
    кодом RC_MISUSE: раньше он считался наравне с находками и превращался в
    rc=1, то есть «я опечатался в пути» и «гейт нашёл нарушение» выглядели
    снаружи одинаково (пункт 1 контракта, рычаг 3).
    """
    out, misuse = [], 0
    for p in paths:
        if staged:
            text = staged_text(p)
            if text is None:
                continue
            out.append((REPO / p, text, added_lines(p)))
        else:
            path = Path(p).resolve()
            try:
                out.append((path, path.read_text(encoding="utf-8"), None))
            except (OSError, UnicodeDecodeError) as e:
                print(f"❌ {path}: не читается ({e.__class__.__name__}) — "
                      f"позвали неверно")
                misuse += 1
    return out, misuse


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Контракт инструмента фабрики: статический гейт над "
                    "_generator/tools/*.py")
    ap.add_argument("paths", nargs="*", help="файлы для проверки")
    ap.add_argument("--staged", action="store_true",
                    help="судить staged-инструменты (режим pre-commit)")
    ap.add_argument("--all", action="store_true",
                    help="судить все _generator/tools/*.py (калибровка)")
    ap.add_argument("--fixtures-for", nargs="*", metavar="ПУТЬ",
                    help="напечатать фикстуры, покрывающие эти инструменты")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args(argv)

    if a.fixtures_for is not None:
        names = {Path(p).name for p in a.fixtures_for}
        for script, covered in sorted(fixture_coverage().items()):
            if names & covered:
                print(script.relative_to(REPO) if REPO and REPO in script.parents
                      else script)
        return RC_OK

    if a.staged:
        paths = staged_paths()
    elif a.all:
        paths = sorted(str(p) for p in (REPO / TOOLS_REL).rglob("*.py"))
    else:
        paths = a.paths
    if not paths:
        # Пустой staged — законная пустота хука: судить нечего, и молчать тут
        # ОБЯЗАНО (Р31). Пустота во всех остальных режимах — Р5-3: гейт, которому
        # не дали ни одного файла, не смеет ответить молчаливым зелёным, иначе
        # опечатка в вызове читается как «проверено, чисто».
        if a.staged:
            return RC_OK
        print("❌ не дано ни одного файла — проверять нечего. Это НЕ «чисто»: "
              "пустой вход и пройденная проверка обязаны выглядеть по-разному "
              "(Р5-3). Укажи пути или позови с --all/--staged.")
        return RC_MISUSE

    targets, misuse = read_targets(paths, a.staged)
    bad = judge(targets, verbose=a.verbose or not a.staged)

    if a.all:
        # Реальный запуск `--help` — ТОЛЬКО в полном аудите (`--all`), не в
        # хуке (`--staged`, закон 2) и не на явных путях калибровки: мета-
        # фикстура (`fixtures/tool_contract/PROGNAT.sh`) зовёт линтер на
        # синтетических файлах-обрывках (GNU-изм в одной строке и т.п.) —
        # это не рабочие CLI и `--help` на них закономерно падает, а не
        # проверка живого инструмента. Живой прогон это и поймал: до сужения
        # условия здоровые фикстуры-обрывки стали ложно-красными.
        # paths, а не targets: интересует файл на диске, не staged-текст.
        help_bad = []
        for p in paths:
            path = Path(p).resolve()
            if path.suffix != ".py":
                continue
            reason = check_help(path)
            if reason:
                help_bad.append((path, reason))
        if help_bad:
            shown_root = REPO
            print(f"\n❌ `--help` сломан у {len(help_bad)} инструмент(ов):")
            for path, reason in help_bad:
                shown = path.relative_to(shown_root) if shown_root in path.parents else path
                print(f"   {shown}: {reason}")
            bad += len(help_bad)

    if misuse:
        # Неверный вызов ПЕРЕБИВАЕТ находки: пока не ясно, что именно проверяли,
        # число дефектов ничего не значит — и уж точно не значит «чисто».
        print(f"\n❌ Позвали неверно ({misuse}): указанного файла нет или он не "
              f"читается. Это rc={RC_MISUSE}, а не находка гейта.")
        return RC_MISUSE
    if bad:
        print(f"\n❌ Контракт инструмента нарушен ({bad}). "
              f"Правила и цены — {CANON} §5.")
        print("   Правило кажется кривым — чинить надо ПРОВЕРКУ, а не обходить гейт.")
        return RC_DEFECT
    if not a.staged:
        print(f"✅ Контракт держится: проверено {len(targets)} из {len(targets)}.")
    return RC_OK


if __name__ == "__main__":
    sys.exit(main())
