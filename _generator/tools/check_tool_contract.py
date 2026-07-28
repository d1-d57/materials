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
MARKER_COVERS = "TOOL-CONTRACT-COVERS:"


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

    Охват объявляет САМА фикстура строкой `# TOOL-CONTRACT-COVERS: a.py b.py`.
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


CHECKS = [
    ("переносимость", check_gnuisms),
    ("--no-optional-locks", check_optional_locks),
    ("shell владельцу", check_shell_to_owner),
    ("запрет записи из песочницы", check_sandbox_guard),
    ("кривой вход", check_input_fixture),
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
    """Собрать `(путь, текст, только_эти_строки)`. В режиме хука — ИЗ ИНДЕКСА."""
    out, bad = [], 0
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
                print(f"❌ {path}: не читается ({e.__class__.__name__})")
                bad += 1
    return out, bad


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
        return 0

    if a.staged:
        paths = staged_paths()
    elif a.all:
        paths = sorted(str(p) for p in (REPO / TOOLS_REL).rglob("*.py"))
    else:
        paths = a.paths
    if not paths:
        return 0

    targets, bad = read_targets(paths, a.staged)
    bad += judge(targets, verbose=a.verbose or not a.staged)
    if bad:
        print(f"\n❌ Контракт инструмента нарушен ({bad}). "
              f"Правила и цены — {CANON} §5.")
        print("   Правило кажется кривым — чинить надо ПРОВЕРКУ, а не обходить гейт.")
        return 1
    if not a.staged:
        print(f"✅ Контракт держится: проверено {len(targets)} из {len(targets)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
