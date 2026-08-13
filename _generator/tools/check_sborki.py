#!/usr/bin/env python3
"""ГЕЙТ СБОРКИ — прогоняет то, что заход УТВЕРЖДАЕТ О МИРЕ, и краснеет на расхождении.

    python3 _generator/tools/check_sborki.py <путь к kod_*.md> [...]

ЗАЧЕМ. У фабрики два гейта на петлю «заход → исполнитель → отчёт», и оба работают
с ТЕКСТОМ: `check_zahod.py` (З1-З8) судит лексику задания, `priyomka.py` (Г0-Г7)
судит отчёт. Между ними дыра: ни один не проверяет, ПРАВДА ЛИ то, что заход
говорит о мире — существует ли названная ветка, лежит ли файл там, где сказано,
даёт ли команда критерия обещанное число, есть ли у инструмента такая подкоманда.
Всё это проверяется только ЗАПУСКОМ, а лексический разбор к нему не способен.

Семь оплаченных случаев одной арки (`UROKI-FABRIKE.md` 25, 30, 33, 41, 42, 45,
47) — это и есть список требований: проверка, не ловящая ни одного из них, здесь
не нужна. Общее у всех семи: у составителя была под рукой команда, дающая точный
ответ за секунду, и он её ни разу не выполнил.

`exit 1` на любом красном. Блок слепых зон печатается ВСЕГДА, включая полный
зелёный прогон: зелёный гейт с необъявленной слепой зоной опаснее красного —
ему верят.

════════════════════════════════════════════════════════════════════════════════
🔴 ГРАНИЦА БЕЗОПАСНОСТИ — главное решение этого инструмента, важнее полноты
════════════════════════════════════════════════════════════════════════════════
Гейт ВЫПОЛНЯЕТ команды из чужого текста. Заход — документ, где команды написаны
для человека; гейт, который начнёт запускать их без разбора, однажды выполнит
`rm`, `git checkout` или `push`. Такой гейт снимут целиком, вместе со всей
пользой. Поэтому граница проведена так:

1. **SHELL НЕ УЧАСТВУЕТ ВООБЩЕ.** `subprocess.run(argv, shell=False)`. `&&`, `;`,
   `|`, `>`, `` ` ``, `$(…)`, glob не «фильтруются регуляркой» — они не имеют
   исполнителя по построению. Строка сперва проверяется на метасимволы
   (`METASIMVOLY`), и при первом же — НЕ ТОКЕНИЗИРУЕТСЯ вовсе: уходит в ⚠.
2. **БЕЛЫЙ СПИСОК ИЗ 15 ВХОДОВ, по паре (программа, подкоманда)** — `BELYJ_SPISOK`
   ниже; чёрный список не годится, он неполон по построению. `git` целиком НЕ
   разрешён: разрешены девять его подкоманд поимённо, и токен сразу после `git`
   обязан быть одной из них — этим закрыта инъекция через глобальные опции
   (`git -c alias.x='!sh' …`). Число 15 сторожится `assert` ниже: разошлось —
   инструмент падает при импорте, а не врёт докстрингом.
3. **ФЛАГИ — тоже списком там, где у команды есть разрушительная форма.**
   `git branch` — только перечисляющие флаги (никаких `-d/-D/-m/-M/-c/-C/--force/
   --set-upstream-to`). `git diff/show/log` — без `--output=` (пишет файл!), без
   `--ext-diff` и `--textconv` (запускают внешние драйверы из конфига, то есть
   произвольный код под видом read-only команды).
4. **КАЖДЫЙ ПУТЬ-АРГУМЕНТ ОБЯЗАН ЛЕЖАТЬ ВНУТРИ РЕПОЗИТОРИЯ.** Без этого
   `grep -c x /Users/…/.ssh/id_rsa` — совершенно законная read-only команда,
   которой гейт читает чужой файл. Абсолютный путь и любой `..`, выводящий
   наружу, отклоняются (`_vnutri_repo`, сверка после `resolve()`, так что
   симлинк тоже не выводит).
5. **ТАЙМАУТ 20 с на команду, ПОТОЛОК 120 команд на файл-заход.** Гейт, который
   висит, — это гейт, который отключат. Исчерпание потолка не проглатывается:
   оно печатается числом в слепых зонах.
6. **ОКРУЖЕНИЕ ПОДЧИЩЕНО.** Все `GIT_*` из среды вырезаны (иначе гейт, позванный
   из хука, унаследует чужой `GIT_INDEX_FILE`), `GIT_CONFIG_NOSYSTEM=1` и
   `GIT_CONFIG_GLOBAL=/dev/null` отрезают алиасы из чужих конфигов,
   `GIT_TERMINAL_PROMPT=0` — сеть не спросит пароль, `GIT_OPTIONAL_LOCKS=0` плюс
   вклеиваемый `--no-optional-locks`: канон этого репозитория (`CLAUDE.md` п.5)
   говорит прямо — обычный git берёт `.git/index.lock` и роняет параллельный
   коммит владельца. По той же причине `git status` в белый список НЕ ВХОДИТ:
   в этом репозитории он не read-only.

🔴 ЕДИНСТВЕННЫЙ ПРИВИЛЕГИРОВАННЫЙ ВХОД — `python3 <инструмент> [подкоманда] --help`.
Он выполняет код чужого файла на импорте, и это осознанная плата: без него урок
47 (заход зовёт живой CLI по устаревшему синтаксису) не ловится ничем. Сужен до
предела: только `.py`, только внутри `_generator/tools/` ТОГО репозитория, где
лежит сам гейт (не того, на который его натравили), `--help` обязан быть
последним аргументом, промежуточные токены — только `[a-z0-9-]+` (подкоманда),
никаких флагов. Все инструменты этой папки — argparse: `--help` печатается на
разборе аргументов, до тела подкоманды.

════════════════════════════════════════════════════════════════════════════════
🔴 ЧЕГО ЭТОТ ГЕЙТ НЕ ПРОВЕРЯЕТ (объявленные слепые зоны)
════════════════════════════════════════════════════════════════════════════════
- **Правдивость «этого нет» (С6) не проверяется сама по себе.** «Не существует
  нигде» неопровержимо без указания, ГДЕ искать. С6 требует, чтобы рядом стояли
  ОБЪЕКТ в backtick и команда про него, и выполняет её, если она в белом списке;
  само отсутствие предмета остаётся на совести составителя. Это половина урока
  33, и она честная. Словарь отрицаний (`NET_RE`) — двенадцать словоформ, и он
  по построению неполон: тринадцатая форма пройдёт молча.
- **Форма «ЛОЖНО, но верно по смыслу» гейту недоступна вся целиком.** Он сверяет
  адреса, числа и синтаксис вызовов — то, у чего есть машинный ответ. «Задача
  нужна», «этот подход правильный», «времени хватит» не проверяются ничем.
- **С6 не судит строки markdown-таблиц и текст в «ёлочках».** Заход, который
  РАССКАЗЫВАЕТ про чужую ошибку («ветки не существует — холостой прогон»), не
  утверждает этого о мире; без отсечки гейт краснел бы на каждом заходе, который
  цитирует уроки, — а ложное красное обходят вместе со всеми остальными гейтами.
- **Утверждение, написанное прозой без команды и без адреса, гейту невидимо.**
  Проверяются адреса (пути, ветки, подкоманды) и числа рядом с командами; «мне
  кажется, тут всё просто» не проверяется ничем и никогда.
- **Число сверяется только со СЧИТАЮЩЕЙ командой** — той, чей вывод есть одно
  целое число (`grep -c`, `wc -l`, `--count`). `git show --stat` рядом с «ровно
  два новых пути» не сверяется: сопоставить произвольный вывод с числом в прозе
  нечем, и попытка дала бы ложное красное на здоровом критерии.
- **Команда вне белого списка не выполняется и потому не проверена.** Она
  печатается поимённо: молчание про неё — ровно то, что стоило урока 42.
- **С3 резолвит путь от двух баз — корня репозитория и папки самого захода.**
  Путь, осмысленный от какой-то третьей базы, будет назван несуществующим.
- **Пути ЗОНЫ из красного С3 исключены:** зона сплошь и рядом перечисляет файлы,
  которые исполнитель только создаст. Их отсутствие печатается, но не краснеет.
- **С3b (виден ли якорь с ветки исполнителя) судит только якоря §0.** Остальной
  корпус путей проверяется на диске основной папки.
- **Таймаут убивает прямого потомка.** Привилегированный вход (`python3 … --help`)
  теоретически может оставить внука; в этой папке таких инструментов нет.

Только stdlib.
"""
import argparse
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
REPO = TOOLS.parent.parent

TAJMAUT = 20          # секунд на одну команду
POTOLOK = 120         # команд на один файл-заход
# 🔴 ДВА РАЗНЫХ ПРЕДЕЛА, и путать их дорого. Первый живой прогон поймал: единый
# предел в 20 000 символов ОБРЕЗАЛ вывод `git ls-files` (2411 путей) на четверти,
# и С3 объявляла несуществующими файлы, которые в индексе есть. Обрезка нужна
# ПЕЧАТИ, а не разбору: проверка обязана видеть весь вывод.
PREDEL_VYVODA = 4_000_000  # символов на разбор — защита памяти, не косметика
PREDEL_PECHATI = 200       # символов команды в строке отчёта
RADIUS = 300          # символов окна «команда рядом с утверждением»

# ── §1 границы: строка с любым из этих символов НЕ токенизируется вовсе ────────
# `&|;<>$`\` — управление шеллом и подстановка; `*?[]{}()` — глобы и группировка;
# `~` — раскрытие в чужой домашний каталог. Оболочка не вызывается никогда, но
# строка с метасимволом означает, что автор ПИСАЛ для шелла, и разбирать её по
# токенам — угадывать его намерение.
# 🔴 КАВЫЧКИ В СПИСОК НЕ ВХОДЯТ, И ЭТО НЕ НЕДОСМОТР. При `shell=False` кавычка не
# управляет ничем: её снимает `shlex.split`, а незакрытая роняет его в ValueError,
# который здесь же и ловится. Зато без кавычек не разбирается ровно та команда,
# ради которой проверка С4 существует, — `grep -c "НЕ покрыто" <файл>` из урока 42.
METASIMVOLY = set('&|;<>$`\\\n*?[]{}()~')


# ══════════════════════════════ БЕЛЫЙ СПИСОК ══════════════════════════════════
# Ключ — (программа, подкоманда|None). `flagi_belyj` задан там, где у команды
# есть разрушительная форма: тогда разрешены ТОЛЬКО перечисленные флаги.
# `flagi_zapret` — точечные запреты у команд, чей набор флагов слишком широк,
# чтобы перечислять его целиком, но чьи опасные формы известны поимённо.
BELYJ_SPISOK = {
    ("git", "rev-parse"):  {"opis": "разрешение ссылки/ветки, ничего не меняет"},
    # `-O` — orderfile: читает произвольный файл (находка верификатора §3, та же
    # школа, что приклеенное значение опции).
    ("git", "show"):       {"opis": "показ объекта",
                            "flagi_zapret": ("--output", "--ext-diff", "--textconv", "-O")},
    ("git", "log"):        {"opis": "история",
                            "flagi_zapret": ("--output", "--ext-diff", "--textconv", "-O")},
    ("git", "diff"):       {"opis": "различие деревьев",
                            "flagi_zapret": ("--output", "--ext-diff", "--textconv", "-O")},
    ("git", "branch"):     {"opis": "перечисление веток",
                            "flagi_belyj": ("--list", "-l", "-a", "--all", "-r", "--remotes",
                                            "--merged", "--no-merged", "--show-current",
                                            "--contains", "--no-contains", "--format",
                                            "-v", "-vv", "--verbose", "--sort", "--color",
                                            "--no-color", "-q", "--quiet")},
    ("git", "ls-tree"):    {"opis": "содержимое дерева коммита"},
    ("git", "ls-files"):   {"opis": "перечень отслеживаемых файлов"},
    ("git", "cat-file"):   {"opis": "существование/содержимое объекта"},
    ("git", "merge-base"): {"opis": "точка расхождения веток"},
    ("ls", None):          {"opis": "перечень файлов"},
    ("test", None):        {"opis": "проверка существования пути"},
    ("wc", None):          {"opis": "счёт строк/слов"},
    ("grep", None):        {"opis": "поиск по файлам",
                            "flagi_zapret": ("-f", "--file")},  # читает шаблоны из файла
    ("head", None):        {"opis": "начало файла"},
    ("python3", "--help"): {"opis": "🔴 привилегированный вход: справка инструмента "
                                    "из _generator/tools/ этого репозитория"},
}
# 🔴 Число из докстринга сторожится здесь, а не остаётся обещанием: правило
# заводится вместе с тем, что покраснеет при нарушении (`KONSTITUCIYA §11`).
assert len(BELYJ_SPISOK) == 15, (
    f"докстринг обещает 15 входов белого списка, в таблице {len(BELYJ_SPISOK)} — "
    f"поправь ОБА места")

GIT_PODKOMANDY = {p for (prog, p) in BELYJ_SPISOK if prog == "git"}

# Программы, по которым строка в backtick опознаётся КАК КОМАНДА. Список нарочно
# шире белого: опасные программы нужно УВИДЕТЬ и назвать отказом, а не пропустить
# мимо глаз как обычный текст.
PROGRAMMY = {
    "git", "python3", "python", "sh", "bash", "zsh", "ls", "test", "wc", "grep",
    "head", "tail", "cat", "rm", "mv", "cp", "mkdir", "rmdir", "touch", "chmod",
    "chown", "sudo", "pip", "pip3", "curl", "wget", "find", "xargs", "echo",
    "sed", "awk", "make", "npm", "npx", "node", "open", "zip", "unzip", "tar",
    "cd", "export", "kill", "pkill", "ln", "diff", "sort", "uniq", "jq",
}

SREDA = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
SREDA.update({
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_TERMINAL_PROMPT": "0",
    "GIT_OPTIONAL_LOCKS": "0",
    "GIT_PAGER": "cat",
})


def _vnutri_repo(token: str) -> bool:
    """Резолвится ли путь-аргумент внутри репозитория (после `resolve()`).

    Относительный путь без `..` внутри по построению — быстрый выход без обращения
    к диску. Всё остальное (абсолютный путь, `..`, симлинк) сверяется настоящим
    `resolve()`: `_generator/../../.ssh` обязан отклоняться так же, как `/etc`.
    """
    if token.startswith("~"):
        return False
    p = Path(token)
    if not p.is_absolute() and ".." not in p.parts:
        return True
    try:
        (REPO / p).resolve().relative_to(REPO.resolve())
        return True
    except (ValueError, OSError):
        return False


def _puti_argumenta(token: str):
    """Части токена, которые могут оказаться путями.

    🔴 ДЫРА, НАЙДЕННАЯ ВЕРИФИКАТОРОМ §3, И ЕЁ ЦЕНА. Раньше у токена-флага путь
    искался ТОЛЬКО после `=`. Короткая опция с ПРИКЛЕЕННЫМ значением начинается
    с `-` и `=` не содержит — путь не проверялся вовсе, и
    `grep -cf/Users/…/.ssh/id_rsa <файл>` проходил белый список целиком: `grep`
    разбирает это как `-c -f /Users/…/.ssh/id_rsa` и читает файл ВНЕ
    репозитория. Верификатор предъявил рабочий эксплойт: та же команда в
    раздельной форме отклонялась, в приклеенной — выполнялась, и вывод менялся
    вместе с содержимым внешнего файла (оракул по чужим строкам).
    Лечение — не список опасных букв (он неполон по построению), а правило о
    ФОРМЕ: путь в токене распознаётся по первому `/` или `~`, флаг это или нет.
    """
    if not token.startswith("-"):
        return [token]
    chasti = []
    if "=" in token:
        chasti.append(token.split("=", 1)[1])
    # 🔴 Только у ФЛАГА хвост от первого `/` или `~` — это приклеенное значение.
    # У обычного токена так делать нельзя: `zahod/moya-vetka` дал бы «путь
    # `/moya-vetka`», абсолютный и вне репозитория, и гейт отказывался бы
    # проверять собственные ветки. Поймано прогоном фикстуры сразу после
    # закрытия дыры — лечение чуть не сломало С1 целиком.
    for otmetka in ("/", "~"):
        i = token.find(otmetka)
        if i >= 0:
            chasti.append(token[i:])
    return [c for c in chasti if c]


def bezopasna(argv):
    """`(да, причина_отказа)` — пускать ли этот argv в исполнение.

    Проверяет ровно четыре вещи в порядке убывания цены ошибки: пара
    (программа, подкоманда) из белого списка · флаги · привилегированный вход ·
    путь-аргумент не выводит наружу репозитория.
    """
    if not argv:
        return False, "пустая команда"
    prog = argv[0]

    if prog == "git":
        # 🔴 РОВНО ОДНА глобальная опция допускается перед подкомандой —
        # `--no-optional-locks`, и это не послабление: канон репозитория ТРЕБУЕТ
        # писать её в каждом вызове, и заходы её пишут. Прогон по корпусу дал
        # ⚠ «`git --no-optional-locks` вне белого списка» на командах, исполненных
        # по канону дословно, — гейт наказывал за соблюдение правила. Список из
        # одного элемента, а не «пропускать любые опции до подкоманды»: `-c`,
        # `--exec-path` и прочие остаются закрытыми.
        if len(argv) > 1 and argv[1] == "--no-optional-locks":
            argv = [argv[0]] + argv[2:]
        if len(argv) < 2 or argv[1] not in GIT_PODKOMANDY:
            sub = argv[1] if len(argv) > 1 else "(нет)"
            return False, f"`git {sub}` вне белого списка (разрешены только: " \
                          f"{', '.join(sorted(GIT_PODKOMANDY))})"
        pravilo = BELYJ_SPISOK[("git", argv[1])]
        ostatok = argv[2:]
    elif prog in ("python3", "python"):
        # 🔴 Привилегированный вход: `python3 <tools/x.py> [подкоманда] --help`.
        if len(argv) < 3 or argv[-1] != "--help":
            return False, "`python3` разрешён ТОЛЬКО в форме " \
                          "`python3 <инструмент из _generator/tools/> [подкоманда] --help`"
        instrument = Path(argv[1])
        if not instrument.is_absolute():
            instrument = REPO / instrument
        try:
            instrument = instrument.resolve()
            instrument.relative_to(TOOLS)
        except (ValueError, OSError):
            return False, f"инструмент `{argv[1]}` вне `_generator/tools/` того " \
                          f"репозитория, где лежит гейт — отказ"
        if instrument.suffix != ".py" or not instrument.is_file():
            return False, f"`{argv[1]}` — не существующий .py-файл инструмента"
        for tok in argv[2:-1]:
            if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', tok):
                return False, f"между инструментом и `--help` разрешена только " \
                              f"подкоманда вида `[a-z0-9-]+`, встречено `{tok}`"
        return True, ""
    elif (prog, None) in BELYJ_SPISOK:
        pravilo = BELYJ_SPISOK[(prog, None)]
        ostatok = argv[1:]
    else:
        return False, f"`{prog}` вне белого списка"

    belyj = pravilo.get("flagi_belyj")
    zapret = pravilo.get("flagi_zapret", ())
    for tok in ostatok:
        if tok.startswith("-"):
            imya = tok.split("=", 1)[0]
            if belyj is not None and imya not in belyj:
                return False, f"флаг `{imya}` не входит в белый список флагов этой команды"
            if any(imya == z or imya.startswith(z) for z in zapret):
                return False, f"флаг `{imya}` запрещён: у этой команды он пишет файл " \
                              f"или запускает внешний драйвер"
        for chast in _puti_argumenta(tok):
            if chast and not _vnutri_repo(chast):
                return False, f"аргумент `{chast}` выводит за пределы репозитория"
    return True, ""


class Prognon:
    """Исполнитель с потолком, таймаутом и протоколом отказов.

    Считает всё, что нашёл, а не только то, что смог: числа охвата в блоке
    слепых зон берутся отсюда, и «нашёл 34, выполнил 12» — это и есть честный
    ответ на вопрос «что гейт НЕ проверил».
    """

    def __init__(self):
        self.najdeno = 0
        self.vypolneno = 0
        self.otkazy = []      # (команда, причина)
        self.potolok_ischerpan = 0

    def vypolnit(self, stroka: str):
        """`(состояние, rc, вывод, причина)`; состояние — `ok` либо `otkaz`."""
        self.najdeno += 1
        stroka = stroka.strip()
        plohie = sorted(set(stroka) & METASIMVOLY)
        if plohie:
            return self._otkaz(stroka, f"метасимвол(ы) {' '.join(plohie)} — строка писана "
                                        f"для шелла, к токенам не приводится")
        try:
            argv = shlex.split(stroka)
        except ValueError as e:
            return self._otkaz(stroka, f"не разбирается на токены ({e})")
        da, prichina = bezopasna(argv)
        if not da:
            return self._otkaz(stroka, prichina)
        if self.vypolneno >= POTOLOK:
            self.potolok_ischerpan += 1
            return self._otkaz(stroka, f"исчерпан потолок {POTOLOK} команд на файл")
        if argv[0] == "git" and "--no-optional-locks" not in argv:
            argv = [argv[0], "--no-optional-locks"] + argv[1:]
        try:
            r = subprocess.run(argv, cwd=str(REPO), capture_output=True, text=True,
                               timeout=TAJMAUT, env=SREDA, shell=False)
        except subprocess.TimeoutExpired:
            return self._otkaz(stroka, f"таймаут {TAJMAUT} с")
        except OSError as e:
            return self._otkaz(stroka, f"не запустилась ({e.__class__.__name__})")
        self.vypolneno += 1
        vyvod = (r.stdout or "")[:PREDEL_VYVODA]
        oshibka = (r.stderr or "")[:PREDEL_VYVODA]
        return "ok", r.returncode, vyvod, oshibka

    def _otkaz(self, stroka, prichina):
        self.otkazy.append((stroka, prichina))
        return "otkaz", None, "", prichina


# ═══════════════════════════ РАЗБОР ТЕКСТА ЗАХОДА ═════════════════════════════

ZADANIE_KONEC_RE = re.compile(r'^##\s+ПЛАН\b', re.M)
# 🔴 Тем же приёмом, что `check_zahod._bez_startovogo` (заход `nositel`,
# 13.08.2026, ## ЗАДАЧА шаг 1) — без общего импорта, эти два инструмента и так
# дублируют проверки между собой (`KRITERIJ_RE`/`ZONA_RE` ниже — та же копия).
# Блок канала `app` секции-носителя несёт `git_zona.py worktree add …
# --branch …` дословно; блок канала `terminal` несёт саму стартовую команду.
# Оба — ЦИТАТЫ, не задание: разобранные как команды из текста захода, они
# ловились С5 ложно (заход `nositel`, ## ЗАДАЧА шаг 1, «главная ловушка,
# найденная живым прогоном при сборке этого захода» — `git_zona.py worktree`
# с позиционным аргументом, живой CLI такого не принимает; причина —
# трейлинг-проза на той же строке за командой, `…, затем чтение захода`).
STARTOVOE_ZAGOLOVOK_RE = re.compile(r'^##\s+СТАРТОВОЕ\s+СООБЩЕНИЕ\s+ВЛАДЕЛЬЦУ.*$', re.M)
KRITERIJ_RE = r'\*\*КРИТЕРИЙ\s+ГОТОВНОСТИ[^\n]*\*\*'
KONTRAKT_RE = r'^##\s+КОНТРАКТ\s+ЗОНЫ.*$'
ZONA_RE = re.compile(r'\*\*ЗОНА[^*\n]*\(можно менять\)[^*\n]*\*\*:?\s*([^\n]*)', re.I)
FENCE_RE = re.compile(r'^```[^\n]*\n(.*?)^```', re.M | re.S)
INLINE_RE = re.compile(r'`([^`\n]+)`')
YAKORYA_RE = re.compile(r'Прочитать\s+ТОЛЬКО\s+это', re.I)


def _bez_startovogo(text: str) -> str:
    """Текст без секции «## СТАРТОВОЕ СООБЩЕНИЕ ВЛАДЕЛЬЦУ» — она цитата, не задание.

    🔴 Граница учитывает ```-ограждение И останавливается также на `^──`
    (тот же приём и обе находки живым прогоном, что в
    `check_zahod._bez_startovogo` — см. её докстринг). Вторая находка:
    секция-носитель встаёт ПЕРЕД блоком «── СЧЁТ НЕЗАКРЫТОГО ──», который не
    `##`-заголовок — граница только по `##` проезжала мимо него и вырезала
    ЧУЖОЙ легитимный текст вместе с секцией (живой прогон чужой, но
    применимой фикстуры `fixtures/gigiena/PROGNAT.sh`, поймавшей это как
    исчезновение «## 4.1 ГИГИЕНА» из поля зрения С8 дальше по файлу).
    """
    m = STARTOVOE_ZAGOLOVOK_RE.search(text)
    if not m:
        return text
    hvost = text[m.end():]
    v_fense, konec = False, len(hvost)
    for lm in re.finditer(r'^([^\n]*)$', hvost, re.M):
        line = lm.group(1)
        if line.strip().startswith('```'):
            v_fense = not v_fense
            continue
        if not v_fense and re.match(r'^(##\s|──)', line):
            konec = lm.start()
            break
    return text[:m.start()] + hvost[konec:]


def zadanie(text: str) -> str:
    """Текст без секции-носителя, ДО `## ПЛАН` — то, что составитель утверждал
    в момент выдачи.

    Ниже начинается писанина исполнителя; судить её этим гейтом значит менять
    вердикт о заходе задним числом (тот же закон, что у З8 в `check_zahod.py`).

    🔴 ПОРЯДОК ОБЯЗАТЕЛЕН: секция-носитель вырезается ПЕРВОЙ, срез по
    `## ПЛАН` — ВТОРЫМ. Живая находка: канал `app` несёт строку `## ПЛАН
    внутри него…` ВНУТРИ ```-блока секции — обратный порядок резал `text` по
    ЭТОМУ фальшивому заголовку раньше, чем секция вырезалась, и всё, что
    реально стоит МЕЖДУ секцией и настоящим `## ПЛАН» (включая «## 4.1
    ГИГИЕНА»), исчезало из «задания» целиком — С8 переставала видеть раздел
    ГИГИЕНА на КАЖДОМ свежем заходе. Тот же приём, что в
    `check_zahod.judge()` — см. докстринг `STARTOVOE_ZAGOLOVOK_RE` выше.
    """
    bez = _bez_startovogo(text)
    m = ZADANIE_KONEC_RE.search(bez)
    return bez[:m.start()] if m else bez


def span_sekcii(text, heading_re):
    """`(начало, конец)` тела секции после заголовка — или None."""
    m = re.search(heading_re, text, re.M)
    if not m:
        return None
    tail = text[m.end():]
    nxt = re.search(r'^##\s', tail, re.M)
    return (m.end(), m.end() + (nxt.start() if nxt else len(tail)))


def sekciya(text, heading_re):
    sp = span_sekcii(text, heading_re)
    return text[sp[0]:sp[1]] if sp else None


def adresnye_zony(z):
    """Спаны мест, где путь — АДРЕС РАБОТЫ, а не иллюстрация в прозе.

    🔴 Различение оплачено первым же живым прогоном: заход объясняет цену ошибок
    и по дороге называет `.git/index.lock`, `_INFRA-git/INCIDENTY.md`, `/cost` —
    десятки путей, которых на диске нет и быть не должно. Красное на них — ровно
    тот шум, из-за которого гейт отключают. Адресными считаются три места:
    якоря «Прочитать ТОЛЬКО это» (туда исполнителя посылают читать), КОНТРАКТ
    ЗОНЫ (там его рабочие пути) и КРИТЕРИЙ ГОТОВНОСТИ (там пути, по которым он
    отчитывается). Ровно в них лежали пути уроков 45 и 27.
    """
    spany = []
    m = YAKORYA_RE.search(z)
    if m:
        hvost = z[m.end():]
        nxt = re.search(r'^##\s', hvost, re.M)
        spany.append((m.end(), m.end() + (nxt.start() if nxt else len(hvost))))
    for pat in (KONTRAKT_RE, KRITERIJ_RE):
        sp = span_sekcii(z, pat)
        if sp:
            spany.append(sp)
    return spany


def _v_kavychkah(text: str, i: int) -> bool:
    """Стоит ли позиция внутри «ёлочек» — то есть является цитатой, а не речью."""
    return text.count('«', 0, i) > text.count('»', 0, i)


def _v_tablice(text: str, i: int) -> bool:
    """Стоит ли позиция в строке markdown-таблицы (`| … | … |`)."""
    nachalo = text.rfind('\n', 0, i) + 1
    return text[nachalo:].lstrip().startswith('|')


def _v_skobkah(text: str, i: int) -> bool:
    """Стоит ли позиция внутри круглых скобок в пределах своей строки.

    🔴 Оплачено первым живым прогоном: «красное — утверждение опровергнуто
    прогоном (ветки нет, путь не существует, подкоманды нет)» — это ПЕРЕЧИСЛЕНИЕ
    исходов проверки, а не утверждение о мире. Скобочная врезка поясняет, а не
    заявляет; краснеть на ней — краснеть на любом заходе, который объясняет,
    что делает.
    """
    nachalo = text.rfind('\n', 0, i) + 1
    konec = text.find('\n', i)
    stroka, otn = text[nachalo:konec if konec > 0 else len(text)], i - nachalo
    return stroka.count('(', 0, otn) > stroka.count(')', 0, otn)


def komandy(text: str):
    """`[(строка команды, позиция)]` — из код-блоков и из инлайн-backtick.

    Командой считается то, чей ПЕРВЫЙ токен — имя программы (`PROGRAMMY`, список
    нарочно шире белого). Иначе backtick-строка — это путь, флаг или имя, и её
    разбирают другие проверки.
    """
    out, zanyato = [], []
    for m in FENCE_RE.finditer(text):
        zanyato.append((m.start(), m.end()))
        # 🔴 ПОЗИЦИЯ СВОЕЙ СТРОКИ, А НЕ НАЧАЛА БЛОКА (находка верификатора §3):
        # С4 ищет обещанное число в строке команды, и с общей позицией блока
        # искал его в ПЕРВОЙ строке блока — то есть у чужой команды.
        smeshchenie = m.start(1)
        for stroka in m.group(1).splitlines():
            golaya = stroka.strip()
            if golaya and not golaya.startswith('#'):
                out.append((golaya, smeshchenie + stroka.find(golaya[0])))
            smeshchenie += len(stroka) + 1
    for m in INLINE_RE.finditer(text):
        if any(a <= m.start() < b for a, b in zanyato):
            continue
        golaya = m.group(1).strip()
        if golaya.split() and golaya.split()[0] in PROGRAMMY:
            out.append((golaya, m.start()))
    return [(s, i) for s, i in out if s.split() and s.split()[0] in PROGRAMMY]


# `=` — присвоение переменной (`GIT_ZONA_REPO=/tmp/…`), `§` и кириллица — проза в
# бэктиках («`стр.N`», «`высота/ширина`», «`ЖАНР/ЦЕНА`»). Пути этого репозитория
# латинские все до одного; прогон по корпусу дал этой формой четыре ложных красных.
PUT_MUSOR_RE = re.compile(r'[<>{}*?=§]|[А-Яа-яЁё]')


def puti(text: str, propustit_komandy=True):
    """`[(путь, позиция)]` — backtick-токены, похожие на адрес файла или папки."""
    out, zanyato, kandidaty = [], [], []
    # 🔴 КОД-БЛОК ТОЖЕ ЧИТАЕТСЯ — НО ТОЛЬКО ЕГО НЕ-КОМАНДНЫЕ СТРОКИ. Находка
    # верификатора §3: список якорей, оформленный ```-блоком вместо
    # маркированного списка (обычная форма для перечня файлов), делал ВЕСЬ корпус
    # путей захода невидимым для С3 — пути брались лишь из инлайн-backtick.
    for m in FENCE_RE.finditer(text):
        zanyato.append((m.start(), m.end()))
        smeshchenie = m.start(1)
        for stroka in m.group(1).splitlines():
            golaya = stroka.strip()
            if golaya and not golaya.startswith('#') and \
                    not (golaya.split() and golaya.split()[0] in PROGRAMMY):
                kandidaty.append((golaya.split()[0] if golaya.split() else "", smeshchenie))
            smeshchenie += len(stroka) + 1
    for m in INLINE_RE.finditer(text):
        if any(a <= m.start() < b for a, b in zanyato):
            continue
        kandidaty.append((m.group(1).strip(), m.start()))
    for soderzhimoe, poz in kandidaty:
        if propustit_komandy and soderzhimoe.split() and soderzhimoe.split()[0] in PROGRAMMY:
            continue
        # «`RUKOVODSTVO-zahodami.md §Приёмка`» — адрес это первое слово.
        tok = soderzhimoe.split()[0] if soderzhimoe.split() else ""
        if not tok or tok.startswith('-') or PUT_MUSOR_RE.search(tok):
            continue
        if tok.startswith('http') or tok.startswith('~'):
            continue
        if re.fullmatch(r'\.\w+', tok):
            continue          # «`.md`» — расширение, а не адрес
        if re.fullmatch(r'/[\w.-]+/?', tok):
            continue          # «`/usage`», «`/zhurnal/`» — слэш-команда или кусок
                              # grep-шаблона, а не адрес от корня репозитория
        if '/' not in tok and not re.search(r'\.\w{1,4}$', tok):
            continue
        out.append((tok, poz))
    return out


def vetki(text: str):
    """`{имя ветки: [все позиции упоминания]}`.

    🔴 ПЯТЬ ИСТОЧНИКОВ И ВСЕ ПОЗИЦИИ, а не префикс `zahod/` и первое совпадение.
    Оба сужения предъявил верификатор §3: заход, написавший «ветка `mat-kostyak`
    уже стоит и уже принята» (ветки нет; есть `arka/mat-kostyak`), проходил С1
    молча — имя без префикса в словарь не попадало вовсе, и `rev-parse` не
    запускался ни разу. А хранение ОДНОЙ позиции глушило С7: имя ветки стоит в
    шапке, приказ «влей» — абзацем ниже, дальше окна в 300 символов.
    """
    najdeno = {}
    for pat in (r'--branch\s+([^\s`]+)',
                r'обязано быть\s+`([^`]+)`',
                r'`(zahod/[^`\s]+)`',
                r'(?<![\w/`])(zahod/[A-Za-z0-9._-]+)',
                r'ветк\w*\s+`([^`\s]{2,80})`'):
        for m in re.finditer(pat, text):
            imya = m.group(1).strip().strip('`').rstrip('.,;:')
            if not imya or PUT_MUSOR_RE.search(imya) or imya.endswith('/'):
                continue
            najdeno.setdefault(imya, []).append(m.start())
    return najdeno


# ═════════════════════════════ ПРОВЕРКИ С1-С7 ═════════════════════════════════

SOZDAET_RE = r'worktree\s+add[^\n]*--branch\s+{}'
UTVERZHDAET_RE = re.compile(
    r'уже\s+сто|УЖЕ\s+сто|уже\s+созда|уже\s+есть|уже\s+принят|обязано\s+быть|'
    r'должно\s+быть|стоит\s+ветка|ветка\s+стоит', re.I)
DOPUSKAET_RE = re.compile(
    r'ветки\s+нет|если\s+она|если\s+уже|не\s+вливай|может\s+не\s+существ|'
    r'нет\s+или\s+на\s+ней', re.I)


def check_s1_vetki(z, pr):
    """С1 (урок 41) — ветка, названная заходом, существует.

    Три исхода, а не два, и это принципиально: заход, который САМ заводит ветку
    первым ходом (`worktree add --branch X`), обязан молчать — иначе гейт краснел
    бы на каждом здоровом worktree-заходе.
    """
    msgs = []
    for imya, pozicii in vetki(z).items():
        sostoyanie, rc, _, _ = pr.vypolnit(f"git rev-parse --verify {imya}")
        if sostoyanie == "otkaz":
            msgs.append(("⚠", "С1", f"ветку `{imya}` проверить не удалось"))
            continue
        if rc == 0:
            continue
        if re.search(SOZDAET_RE.format(re.escape(imya)), z):
            continue  # заход её сам и заводит — это не утверждение о мире
        okna = [z[max(0, p - RADIUS):p + RADIUS] for p in pozicii]
        if any(DOPUSKAET_RE.search(o) for o in okna):
            continue  # заход прямо допускает, что ветки нет
        if any(UTVERZHDAET_RE.search(o) for o in okna):
            msgs.append(("❌", "С1", f"ветки `{imya}` НЕ СУЩЕСТВУЕТ "
                                     f"(`git rev-parse --verify` → rc={rc}), а заход "
                                     f"утверждает, что она уже стоит — урок 41, "
                                     f"холостой прогон на первом ходе"))
        else:
            msgs.append(("⚠", "С1", f"ветки `{imya}` нет, и заход не говорит, кто её "
                                     f"заводит — исполнитель встанет на первом ходе"))
    return msgs


def check_s2_chuzhoj_repo(z, pr, zahod_path):
    """С2 (урок 30) — зона указывает в чужой репозиторий, а репозиторий не назван.

    🔴 Сосед ищется рядом с репозиторием ЗАХОДА, а не рядом с папкой, откуда
    позвали гейт. Живой прогон из worktree поймал разницу: `../disciplina` от
    `materials-wt/wt-sborki` — это `materials-wt/disciplina`, которого нет, и
    проверка молчала бы ровно там, где урок 30 её и требует.
    """
    # 🔴 ПРИСВОЕНИЕ, А НЕ УПОМИНАНИЕ (находка верификатора §3): проверка по
    # подстроке снималась даже ОТРИЦАЮЩЕЙ фразой «GIT_ZONA_REPO выставлять не
    # надо» — то есть ровно тем текстом, который делает заход опаснее.
    m = ZONA_RE.search(z)
    if not m or re.search(r'GIT_ZONA_REPO\s*=', z):
        return []
    bazy = _bazy(zahod_path)
    msgs = []
    for tok in re.findall(r'`([^`]+)`', m.group(1)):
        pervyj = tok.strip().strip('/').split('/')[0]
        if not pervyj or any((b / pervyj).exists() for b in bazy):
            continue
        sosedi = [b.parent / pervyj / ".git" for b in bazy]
        sosed = next((s for s in sosedi if s.exists()), None)
        if sosed:
            msgs.append(("❌", "С2", f"зона названа путями `{tok}`, а `{pervyj}/` — "
                                     f"ОТДЕЛЬНЫЙ репозиторий рядом ({sosed.parent}); "
                                     f"`GIT_ZONA_REPO` в тексте захода не упомянута — "
                                     f"урок 30: 0 файлов во всех ветках, холостой прогон"))
    return msgs


_GLAVNYJ_REPO = None


def glavnyj_repo():
    """ОСНОВНАЯ папка репозитория — не worktree, из которого позвали гейт.

    🔴 Единственная команда, которую гейт запускает не из текста захода, а от
    себя: она зашита здесь целиком, read-only и без аргументов извне. Нужна,
    потому что из worktree `REPO` — это `materials-wt/<имя>`, и «репозиторий
    рядом» (`../disciplina`, урок 30) от неё не находится вовсе. Поймано
    прогоном фикстуры: ловушка С2 молчала при живом соседнем репозитории.
    """
    global _GLAVNYJ_REPO
    if _GLAVNYJ_REPO is None:
        try:
            r = subprocess.run(["git", "--no-optional-locks", "rev-parse", "--git-common-dir"],
                               cwd=str(REPO), capture_output=True, text=True,
                               timeout=TAJMAUT, env=SREDA, shell=False)
            gitdir = Path(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else None
            if gitdir is not None and not gitdir.is_absolute():
                gitdir = REPO / gitdir
            _GLAVNYJ_REPO = gitdir.resolve().parent if gitdir else REPO
        except (OSError, subprocess.TimeoutExpired):
            _GLAVNYJ_REPO = REPO
    return _GLAVNYJ_REPO


def _bazy(zahod_path: Path):
    """Базы, от которых путь захода имеет право резолвиться.

    🔴 ЧЕТЫРЕ, И КАЖДАЯ ОПЛАЧЕНА ЖИВЫМ ПРОГОНОМ. `REPO` — репозиторий, где лежит
    сам гейт (из worktree это папка worktree). ОСНОВНАЯ папка — то дерево, о
    котором заход на самом деле говорит и рядом с которым живут соседние
    репозитории. Корень репозитория самого файла-захода. Папка арки — база для
    путей вида `../../docs/…`, которыми заход ссылается на канон.
    """
    bazy = [REPO, glavnyj_repo(), zahod_path.parent]
    p = zahod_path.parent
    while p != p.parent:
        if (p / ".git").exists():
            bazy.append(p)
            break
        p = p.parent
    vidano, itog = set(), []
    for b in bazy:
        if b not in vidano:
            vidano.add(b)
            itog.append(b)
    return itog


def _indeks(pr):
    """`(множество путей, множество базовых имён)` из `git ls-files` — или `(None, None)`.

    Нужен для двух форм ссылки, которыми заход пользуется постоянно и которые
    `test -e` от корня разрешить не может: голое имя инструмента (`priyomka.py`)
    и СОКРАЩЁННЫЙ путь (`_INFRA-git/INCIDENTY.md` вместо
    `_studio/zhurnal/_INFRA-git/INCIDENTY.md`). Untracked-файла в индексе нет — и
    это верно по существу: именно невидимый из worktree untracked-файл стоил
    урока 45.
    """
    sost, rc, vyvod, _ = pr.vypolnit("git ls-files")
    if sost != "ok" or rc != 0:
        return None, None
    puti_indeksa = {ln.strip() for ln in vyvod.splitlines() if ln.strip()}
    return puti_indeksa, {p.rsplit('/', 1)[-1] for p in puti_indeksa}


def _vse_vetki(pr):
    """Имена всех веток репозитория — чтобы С3 не судила их как пути.

    Прогон по корпусу: `arka/mat-kostyak` дал 11 красных «путь не существует».
    Имя ветки СОДЕРЖИТ слэш и от пути лексически неотличимо; отличается оно тем,
    что живёт в git, — это и спрашиваем, одной командой на файл.
    """
    # 🔴 `--list`, А НЕ `--format=%(refname:short)`: в `%(…)` есть `(` и `)`, а это
    # метасимволы, и гейт ОТКЛОНЯЛ СОБСТВЕННУЮ команду — молча, ничего не сломав
    # на вид. Поймано прогоном по корпусу: число отказов подскочило ровно на
    # число файлов (176), а фильтр веток не работал вовсе.
    sost, rc, vyvod, _ = pr.vypolnit("git branch --list --no-color")
    if sost != "ok" or rc != 0:
        return set()
    return {ln.lstrip('*+ ').strip() for ln in vyvod.splitlines() if ln.strip()}


def check_s3_puti(z, pr, zahod_path):
    """С3 (уроки 45, 27) — путь существует, и существует ТАМ, куда послан исполнитель.

    Часть (b) — та, ради которой проверка стоит своей цены: файл может лежать в
    основной папке untracked и быть НЕВИДИМ из worktree, куда послан исполнитель.
    Ровно это стоило урока 45 (`pokrytie_rychagami.py` в основной папке) и урока
    27 (заход велел читать файл, которого в worktree нет по построению).
    """
    msgs = []
    imena_vetok = set(vetki(z)) | _vse_vetki(pr)
    zona_puti = set()
    m = ZONA_RE.search(z)
    if m:
        zona_puti = {t.split()[0] for t in re.findall(r'`([^`]+)`', m.group(1)) if t.split()}
    bazy = _bazy(zahod_path)
    korni_imena = {b.name for b in bazy}
    indeks_puti, indeks_imena = _indeks(pr)
    adresnye = adresnye_zony(z)

    # 🔴 ПУТЬ, НАЧАТЫЙ ИМЕНЕМ РЕПОЗИТОРИЯ, РЕЗОЛВИТСЯ ОТ ИХ ОБЩЕГО РОДИТЕЛЯ.
    # Прогон по корпусу поймал ложное красное там, где заход поступил ПРАВИЛЬНО:
    # работая в двух репозиториях, он писал `materials/_illustracii/POKRYTIE.md`
    # и `disciplina/skills/` — то самое явное называние репозитория, которого
    # требует вердикт урока 30. Краснеть на этом значит наказывать за исполнение
    # канона.
    roditel = glavnyj_repo().parent
    soseda = {d.name for d in roditel.iterdir() if (d / ".git").exists()} \
        if roditel.is_dir() else set()

    def sushchestvuet(tok):
        if any((b / tok).exists() for b in bazy) or (TOOLS / tok).exists():
            return True
        if tok.split('/')[0] in soseda and (roditel / tok).exists():
            return True
        if '/' not in tok.rstrip('/'):
            if indeks_imena is not None and tok in indeks_imena:
                return True
        if indeks_puti is None:
            return False
        golyj = tok.rstrip('/')
        # Сокращённая ссылка на ФАЙЛ: путь-хвост от настоящего пути в индексе.
        if any(p.endswith('/' + golyj) for p in indeks_puti):
            return True
        # 🔴 ПАПКА, названная относительно ПРОЕКТА, а не корня репозитория
        # (`src/`, `slides/`, `content/`). Прогон по корпусу дал этой формой 30
        # ложных красных: заход работает внутри папки проекта и пишет пути от
        # неё — нормальная и правильная форма, которой корень не знает.
        return any(p.startswith(golyj + '/') or ('/' + golyj + '/') in p
                   for p in indeks_puti)

    def put_zony(tok):
        """Путь зоны — в том числе названный сокращённо (`fixtures/sborka/PROGNAT.sh`)."""
        golyj = tok.rstrip('/')
        return any(golyj == zp.rstrip('/') or zp.rstrip('/').endswith('/' + golyj)
                   or golyj.endswith('/' + zp.rstrip('/')) for zp in zona_puti)

    # 🔴 Г2 (заход `gejty-vrut`). Путь вида `../<репо>-wt/<имя>` в КОНТРАКТЕ ЗОНЫ —
    # не адрес на диске, а ОБЕЩАНИЕ: `git_zona.py worktree add <имя>` заводит эту
    # папку ПЕРВЫМ ХОДОМ исполнителя (см. `WT_HOME / args.name` в `git_zona.py`),
    # и в момент проверки её по построению ещё нет. Урок 45 (путь, названный
    # адресом работы, обязан существовать) здесь неприменим: заход сам объявляет,
    # что заведёт эту папку. Оговорка узкая — НЕ гасит С3 на битых путях: без
    # парного `worktree add <то же имя>` в тексте токен остаётся обычным
    # непроверенным путём и краснеет по-старому.
    # `<репо>` — не литерал «materials»: `glavnyj_repo().name`, тот же приём, что
    # уже живёт в С2/С3 для путей соседних репозиториев.
    WORKTREE_OBESHCHANIE_RE = re.compile(r'^\.\./([\w.-]+)-wt/([\w.-]+)/?$')

    def worktree_obeshchanie(tok):
        m = WORKTREE_OBESHCHANIE_RE.match(tok)
        if not m or m.group(1) != glavnyj_repo().name:
            return False
        imya = m.group(2)
        return bool(re.search(rf'worktree\s+add\s+{re.escape(imya)}\b', z))

    proverennye, v_proze = {}, []
    for tok, poz in puti(z):
        if tok in imena_vetok or tok.rstrip('/') in imena_vetok:
            continue
        if tok.rstrip('/') in korni_imena:
            continue          # имя корня репозитория целиком — не адрес внутри него
        if tok.startswith('.git/'):
            continue          # внутренности git (`.git/index.lock`) адресами не бывают
        if _v_kavychkah(z, poz):
            continue          # это цитата-пример, а не адрес
        est = sushchestvuet(tok)
        proverennye[tok] = est
        if est:
            continue
        if put_zony(tok):
            msgs.append(("⚠", "С3", f"путь зоны `{tok}` не существует — законно, если "
                                     f"его создаёт сам заход"))
            continue
        if worktree_obeshchanie(tok):
            msgs.append(("⚠", "С3", f"путь `{tok}` — обещание worktree (заход сам зовёт "
                                     f"`worktree add` под этим именем первым ходом), не "
                                     f"адрес на диске; легитимно не существовать сейчас "
                                     f"(Г2)"))
            continue
        if not any(a <= poz < b for a, b in adresnye):
            v_proze.append(tok)
            continue
        msgs.append(("❌", "С3", f"путь `{tok}` НЕ СУЩЕСТВУЕТ ни от одной из "
                                 f"{len(bazy)} баз (`test -e` → ложь), а назван "
                                 f"АДРЕСОМ работы — урок 45"))
    if v_proze:
        msgs.append(("⚠", "С3", f"пути, названные в прозе и не найденные "
                                 f"({len(sorted(set(v_proze)))}): "
                                 f"{', '.join('`' + t + '`' for t in sorted(set(v_proze)))} "
                                 f"— адресами работы они не являются, красным не считаю"))

    # ── (b) видны ли якоря §0 с той ветки, куда послан исполнитель ────────────
    vetka_raboty = None
    m_vetka = re.search(r'--branch\s+([^\s`]+)', z)
    if m_vetka:
        vetka_raboty = m_vetka.group(1).strip().strip('`')
    yakorya_blok = None
    m_ya = YAKORYA_RE.search(z)
    if m_ya:
        hvost = z[m_ya.end():]
        nxt = re.search(r'^##\s', hvost, re.M)
        yakorya_blok = hvost[:nxt.start()] if nxt else hvost
    if not vetka_raboty or yakorya_blok is None:
        return msgs
    sostoyanie, rc, _, _ = pr.vypolnit(f"git rev-parse --verify {vetka_raboty}")
    if sostoyanie != "ok" or rc != 0:
        return msgs  # ветки нет — это уже сказал С1, второй раз не кричим
    for tok, _poz in puti(yakorya_blok):
        if tok in imena_vetok:
            continue
        # 🔴 ГОЛОЕ ИМЯ ЯКОРЯ ДОВОДИТСЯ ДО ПОЛНОГО ПУТИ, а не отбрасывается.
        # Находка верификатора §3: заход, назвавший якорь просто
        # «`check_sborki.py` — он уже лежит в дереве» (файл untracked, в worktree
        # исполнителя его не будет), проходил С3b молча — токен без слэша до
        # `git cat-file` не доезжал. Это буквально урок 45, пропущенный из-за
        # ФОРМЫ записи адреса.
        polnyj = tok
        if '/' not in tok:
            if (TOOLS / tok).is_file():
                polnyj = str((TOOLS / tok).relative_to(REPO)) \
                    if str(TOOLS).startswith(str(REPO)) else tok
            else:
                continue
        if not (REPO / polnyj).exists():
            continue
        tok = polnyj
        sost, rc2, _, _ = pr.vypolnit(f"git cat-file -e {vetka_raboty}:{tok}")
        if sost != "ok":
            continue
        if rc2 != 0:
            msgs.append(("❌", "С3", f"якорь `{tok}` есть в основной папке, но его НЕТ "
                                     f"на ветке `{vetka_raboty}`, куда послан исполнитель "
                                     f"(`git cat-file -e` → rc={rc2}) — в его worktree "
                                     f"файла не будет (уроки 45 и 27)"))
    return msgs


# 🔴 НЕ ТОЛЬКО СТРЕЛКА (находка верификатора §3, самая дорогая из его пропусков).
# Критерий «команда обязана вернуть 12» — то же самое обещание, что «→ 12», но
# прежний шаблон знал лишь стрелку и `=`, и такое число молча не сверялось:
# исполнитель сдавал бы «12 из 12» зелёным при живых 36 — буквально урок 42.
CHISLO_RYADOM_RE = re.compile(
    r'(?:→|->|=|верн\w*|даёт|дает|выда\w*|ровно|равн\w*|стать|показ\w*)\s*\**\s*(\d+)|'
    r'(\d+)\s*(?:позици|строк|файл|шт|вхожден|запис|урок)')


def _chislo_ryadom(stroka: str):
    m = CHISLO_RYADOM_RE.search(stroka)
    if not m:
        return None
    return int(m.group(1) or m.group(2))


def _schitayushchaya(vyvod: str):
    """Вывод как ОДНО целое число — иначе сверять его с числом в прозе нечем."""
    golyj = vyvod.strip()
    return int(golyj) if re.fullmatch(r'\d+', golyj) else None


def check_s4_kriterij(z, pr):
    """С4 (уроки 42, 45) — команда критерия прогоняется, её вывод сверяется с числом.

    Самая ценная и самая опасная проверка захода: команда из критерия может
    оказаться какой угодно. Прогоняется только прошедшая белый список; остальные
    печатаются как непроверенные — молчать про них нельзя, непроверенная команда
    и есть урок 42.
    """
    krit = sekciya(z, KRITERIJ_RE)
    if krit is None:
        return [("⚠", "С4", "секция «КРИТЕРИЙ ГОТОВНОСТИ» не найдена — сверять нечего")]
    msgs = []
    for stroka, poz in komandy(krit):
        sostoyanie, rc, vyvod, oshibka = pr.vypolnit(stroka)
        if sostoyanie == "otkaz":
            msgs.append(("⚠", "С4", f"команда критерия `{stroka}` НЕ ПРОВЕРЕНА "
                                     f"({oshibka}) — выполните вручную"))
            continue
        golaya = stroka.split()
        grep_bez_sovpadenij = golaya[0] == "grep" and rc == 1
        if "Traceback" in (oshibka or ""):
            pervaya = [l for l in oshibka.strip().splitlines() if l.strip()][-1]
            msgs.append(("❌", "С4", f"команда критерия `{stroka}` ПАДАЕТ трейсбеком: "
                                     f"{pervaya.strip()} — урок 45"))
            continue
        if rc != 0 and not grep_bez_sovpadenij:
            hvost = (oshibka or vyvod).strip().splitlines()
            pervaya = hvost[0].strip() if hvost else "(вывод пуст)"
            # 🔴 ОШИБКА УПОТРЕБЛЕНИЯ — НЕ ПАДЕНИЕ КОМАНДЫ. Прогон по корпусу
            # поймал: заход упоминает инструмент фрагментом («снять `grep -c`»),
            # гейт запускает фрагмент, тот отвечает `usage:` — и красное встаёт на
            # УПОМИНАНИИ, а не на команде. Отличаются они ровно этим ответом.
            if re.match(r'usage:|Usage:|illegal option|unrecognized arguments', pervaya):
                msgs.append(("⚠", "С4", f"`{stroka}` — не команда, а фрагмент: "
                                         f"инструмент ответил «{pervaya[:80]}». "
                                         f"Проверить нечего"))
                continue
            msgs.append(("❌", "С4", f"команда критерия `{stroka}` даёт rc={rc}: "
                                     f"{pervaya} — критерий на ней провалиться не может"))
            continue
        # строка исходного текста, в которой стоит команда — там же стоит и число
        nachalo = krit.rfind('\n', 0, poz) + 1
        konec = krit.find('\n', poz)
        stroka_teksta = krit[nachalo:konec if konec > 0 else len(krit)]
        obeshchano = _chislo_ryadom(stroka_teksta)
        fakt = _schitayushchaya(vyvod)
        if obeshchano is None or fakt is None:
            continue
        if obeshchano != fakt:
            msgs.append(("❌", "С4", f"команда критерия `{stroka}` даёт {fakt}, а рядом "
                                     f"стоит число {obeshchano} — исполнитель сдаст "
                                     f"«{fakt} из {fakt}» зелёным, пропустив "
                                     f"{abs(obeshchano - fakt)} (урок 42)"))
    return msgs


# 🔴 `[^\S\n]` ВМЕСТО `\s` В ХВОСТЕ — оплачено первым живым прогоном. С `\s`
# хвост вызова перепрыгивал перенос строки и утаскивал продолжение команды после
# `\` целиком: `git_zona.py commit --zone <зона> \ --no-verify "чужой долг: …"`
# читался как вызов с восемью позиционными аргументами, и С5 краснел ложно на
# совершенно здоровом шаблоне коммита. Вызов живёт в пределах одной строки.
#
# 🔴 ХВОСТ БЕРЁТСЯ ЦЕЛИКОМ ДО BACKTICK ИЛИ КОНЦА СТРОКИ, а не по токенам. Прогон
# по корпусу из 175 заходов поймал: 80 красных из 99 — одна и та же ложная
# тревога на `--zone "teorkat-vvedenie _studio/zhurnal/2026-07-21_mat-kostyak"`.
# Зона в кавычках содержит ПРОБЕЛ, разбор по пробелам рвал её пополам, и вторая
# половина читалась как позиционный аргумент, которого CLI не принимает. Кавычки
# снимает `shlex`, а не регулярка.
#
# 🔴 ВТОРАЯ ДЫРА ВЕРИФИКАТОРА §3 — И ОНА БЫЛА ХУЖЕ ПЕРВОЙ. Прежняя форма
# `([\w./-]*?([\w-]+\.py))` содержит вложенный квантификатор по пересекающимся
# классам символов и на длинном прогоне обычных букв даёт катастрофический
# бэктрекинг: 3 КБ прозы без единой команды вешали гейт НАСМЕРТЬ. Заявленные
# «таймаут 20 с и потолок 120 команд» его не ограничивали вовсе — висел не
# подпроцесс, а разбор текста, до всякого `subprocess`. Замер верификатора:
# 500 символов — 0.42 с, 1000 — 2.57 с, 2000 — свыше 10 с.
# Лечение двойное: вложенности больше нет, длина головы ограничена, и поиск
# идёт ПОСТРОЧНО только по строкам, где вообще есть `.py`.
VYZOV_RE = re.compile(
    r'(?<![\w./-])((?:[\w.-]{1,60}/){0,6}[\w-]{1,60}\.py)[^\S\n]+([a-z][a-z0-9-]*)([^\n`]*)')


def vyzovy(z: str):
    """`(путь, имя, подкоманда, хвост)` для каждого вызова инструмента в тексте.

    Построчно и только по строкам с `.py` — см. комментарий к `VYZOV_RE`: это
    вторая половина лечения зависания, найденного верификатором.
    """
    for stroka in z.splitlines():
        if ".py" not in stroka:
            continue
        for m in VYZOV_RE.finditer(stroka):
            put = m.group(1)
            yield put, put.rsplit("/", 1)[-1], m.group(2), m.group(3) or ""


def _usage_vybor(usage: str, sub: str):
    """Допустимые значения первого позиционного выбора `{add,drop,list}` — или None.

    🔴 Находка верификатора §3: гейт ДЕРЖАЛ В РУКАХ usage со списком
    `{add,drop,list}` и молча пропускал `worktree create` — сверялась только
    арность, а не значение. Урок 47 был именно про форму аргумента.
    """
    i = usage.find(sub)
    hvost = usage[i + len(sub):] if i >= 0 else usage
    m = re.search(r'\{([^}]+)\}', hvost.split("\n\n")[0])
    return {c.strip() for c in m.group(1).split(',') if c.strip()} if m else None


def _usage_forma(usage: str, sub: str):
    """`(обязательные флаги, ёмкость позиционных)` из usage-строки argparse.

    🔴 ЁМКОСТЬ, А НЕ ЧИСЛО ОБЯЗАТЕЛЬНЫХ. Первый живой прогон поймал ошибку:
    `worktree [-h] [--branch BRANCH] [--force] {add,drop,list} [name]` принимает
    ДВА позиционных — группу выбора `{add,drop,list}` и необязательный `[name]`, —
    а подсчёт «только небракетированные, кроме `{…}`» давал ноль, и здоровый
    вызов `worktree add wt-sborki` краснел. Считаются все позиционные слоты
    любой обязательности; `…` означает неограниченную ёмкость.
    Обязательные флаги — наоборот, только небракетированные: бракетированный
    флаг по определению необязателен.
    """
    i = usage.find(sub)
    hvost = usage[i + len(sub):] if i >= 0 else usage
    hvost = hvost.split("\n\n")[0]
    obyaz, pozic, glubina, predydushchij_flag = [], 0, 0, False
    for tok in hvost.split():
        vedushchie = len(tok) - len(tok.lstrip('['))
        glubina_do = glubina
        glubina += vedushchie
        chistyj = tok.strip('[]')
        glubina -= tok.count(']')
        if '...' in chistyj or '…' in chistyj:
            return obyaz, 10 ** 6
        if not chistyj:
            continue
        if chistyj.startswith('-'):
            if glubina_do == 0 and not vedushchie:
                obyaz.append(chistyj.split('=')[0])
            predydushchij_flag = True
            continue
        if predydushchij_flag and (chistyj.isupper() or chistyj.startswith('<')):
            predydushchij_flag = False
            continue
        predydushchij_flag = False
        pozic += 1
    return obyaz, pozic


FLAG_SO_ZNACHENIEM_RE = re.compile(r'(--?[\w-]+)\s+(?:\[)?([A-ZА-ЯЁ][A-ZА-ЯЁ_0-9]*|<[^>]+>)')


def _flagi_so_znacheniem(usage: str):
    """Флаги, забирающие следующий токен, — по метапеременной в usage.

    Без этого «съедать токен после любого флага» ошибается на флагах-выключателях
    (`--push`, `--force`): следующий за ними позиционный аргумент терялся бы, и
    урок 47 проходил бы молча ровно там, где его и надо ловить.
    """
    return {m.group(1) for m in FLAG_SO_ZNACHENIEM_RE.finditer(usage)}


def _razobrat_vyzov(hvost: str, s_znacheniem=frozenset()):
    """`(позиционные, флаги)` из хвоста вызова; кавычки снимает `shlex`."""
    hvost = hvost.split('#')[0]
    try:
        tokeny = shlex.split(hvost)
    except ValueError:
        tokeny = hvost.split()
    tokeny = [t for t in tokeny if t and t != '\\']
    pozic, flagi, zhdem_znachenie = [], set(), False
    for tok in tokeny:
        if tok.startswith('-'):
            imya = tok.split('=')[0]
            flagi.add(imya)
            zhdem_znachenie = '=' not in tok and imya in s_znacheniem
            continue
        if zhdem_znachenie:
            zhdem_znachenie = False
            continue
        pozic.append(tok)
    return pozic, flagi


def check_s5_podkomandy(z, pr):
    """С5 (урок 47) — подкоманда существует, И ЗАХОД ЗОВЁТ ЕЁ ПО ЖИВОМУ CLI.

    🔴 Верхнего `--help` мало. Урок 47 был не про отсутствие подкоманды, а про
    ФОРМУ аргумента: заход писал `zakryt-vetku <ветка>` позиционным, живой CLI
    требует `--branch`. Поэтому два уровня: справка ПОДКОМАНДЫ и сверка usage —
    и откат на верхний `--help`, если справка подкоманды падает (урок 26: у части
    инструментов `--help` отдаёт трейсбек, и там сверять нечем).
    """
    msgs, vidano = [], set()
    for put, imya, sub, hvost in vyzovy(z):
        if (imya, sub) in vidano:
            continue
        vidano.add((imya, sub))
        fajl = TOOLS / imya
        if not fajl.is_file():
            continue  # чужой/несуществующий инструмент — это забота С3
        otn = f"_generator/tools/{imya}"
        sost, rc, vyvod, oshibka = pr.vypolnit(f"python3 {otn} {sub} --help")
        if sost != "ok" or rc != 0 or not vyvod.strip():
            sost2, rc2, vyvod2, osh2 = pr.vypolnit(f"python3 {otn} --help")
            if sost2 != "ok":
                msgs.append(("⚠", "С5", f"`{imya} {sub}`: справку получить не удалось "
                                         f"({osh2}) — форма вызова не проверена"))
                continue
            if rc2 != 0 or "Traceback" in (osh2 or ""):
                msgs.append(("⚠", "С5", f"`{imya} --help` падает (rc={rc2}) — сверять "
                                         f"подкоманду `{sub}` нечем (урок 26)"))
                continue
            if not re.search(rf'(?<![\w-]){re.escape(sub)}(?![\w-])', vyvod2):
                msgs.append(("❌", "С5", f"подкоманды `{sub}` у `{imya}` НЕТ — её нет в "
                                         f"выводе `--help` (урок 47)"))
            else:
                msgs.append(("⚠", "С5", f"`{imya} {sub}` существует, но её собственная "
                                         f"справка не отвечает — форма аргументов не "
                                         f"проверена"))
            continue
        usage = vyvod[:vyvod.find("\n\n")] if "\n\n" in vyvod else vyvod
        obyaz, pozic = _usage_forma(usage, sub)
        dano_poz, dano_flagov = _razobrat_vyzov(hvost, _flagi_so_znacheniem(usage))
        dano_pozic = len(dano_poz)
        odna_stroka = ' '.join(usage.split())
        vybor = _usage_vybor(usage, sub)
        if vybor and dano_poz and dano_poz[0] not in vybor:
            msgs.append(("❌", "С5", f"заход зовёт `{imya} {sub} {dano_poz[0]}`, а живой "
                                     f"CLI принимает здесь только "
                                     f"{'{' + ', '.join(sorted(vybor)) + '}'} — "
                                     f"{odna_stroka} (урок 47)"))
            continue
        if dano_pozic > pozic:
            msgs.append(("❌", "С5", f"заход зовёт `{imya} {sub}` с позиционным аргументом, "
                                     f"а живой CLI позиционных здесь не принимает — "
                                     f"{odna_stroka} (урок 47)"))
            continue
        propushcheno = [f for f in obyaz if f not in dano_flagov and f != "-h"]
        if propushcheno and (dano_poz or dano_flagov):
            msgs.append(("❌", "С5", f"заход зовёт `{imya} {sub}` без обязательного "
                                     f"{' '.join(propushcheno)} — {odna_stroka} (урок 47)"))
    return msgs


# 🔴 СЛОВАРЬ РАСШИРЕН ПО НАХОДКЕ ВЕРИФИКАТОРА §3. Прежние восемь буквальных
# строк пропускали самые естественные русские формы того же утверждения: «нет ни
# одной», «не заведена», «не найдено», «отсутствует» (без «вовсе»). Заход,
# сказавший «проверки зоны слияния нет ни одной», проходил молча — а функция
# была на месте, и цена пропуска — сессия на переписывание существующего кода.
NET_RE = re.compile(r'не существует|не существуют|нет нигде|нет ни одн\w*|'
                    r'не живёт нигде|не живет нигде|нигде не живёт|нигде не живет|'
                    r'не заведен\w*|не заведён\w*|не найден\w*|'
                    # 🔴 ТОЛЬКО ГЛАГОЛ, НЕ ПРИЧАСТИЕ. Прогон по корпусу: `отсутству\w*`
                    # дал 131 красное из 230 на форме «отсутствующего <чего-то>» —
                    # это ОПРЕДЕЛЕНИЕ («недостающий пункт»), а не утверждение о том,
                    # что предмета нет в мире. Причастие судить нечем: у него нет
                    # ни субъекта, ни проверяемого адреса.
                    r'отсутствует|отсутствуют|отсутствовал\w*', re.I)


def check_s6_utverzhdenie_net(z, pr):
    """С6 (урок 33) — «этого нет» подтверждено командой, а не памятью составителя.

    Утверждение «этого нет» — самое дорогое в заходе: оно снимает с исполнителя
    обязанность искать, поверив, он не посмотрит. Половина проверки лексическая
    и объявлена такой: «нет нигде» неопровержимо без указания, ГДЕ искать.
    Поэтому требуется команда рядом — и, если она в белом списке, выполняется.
    """
    msgs = []
    for m in NET_RE.finditer(z):
        if _v_kavychkah(z, m.start()) or _v_tablice(z, m.start()) or _v_skobkah(z, m.start()):
            continue
        nachalo = max(0, m.start() - RADIUS)
        okno = z[nachalo:m.end() + RADIUS]
        # 🔴 КОМАНДА ОБЯЗАНА БЫТЬ ПРО ТОТ ЖЕ ОБЪЕКТ. Первый прогон фикстуры поймал:
        # окно ±300 достаёт до соседнего пункта критерия, и `grep -c "def " …`,
        # стоящий рядом совсем по другому поводу, «опровергал» утверждение о
        # третьем файле. Объект утверждения — backtick-токен его собственной
        # строки; команда без этого токена к утверждению отношения не имеет.
        stroka_utv = z[z.rfind('\n', 0, m.start()) + 1:
                       (z.find('\n', m.end()) if z.find('\n', m.end()) > 0 else len(z))]
        obekty = [t.split()[0] for t in re.findall(r'`([^`]+)`', stroka_utv)
                  if t.split() and t.split()[0] not in PROGRAMMY]
        # 🔴 ПОДТВЕРЖДАЕТ ТОЛЬКО КОМАНДА, ПРИВЯЗАННАЯ К ОБЪЕКТУ УТВЕРЖДЕНИЯ.
        # Утверждение без объекта в backtick подтвердить нечем: находка
        # верификатора §3 — пустой список объектов отключал привязку, и ЛЮБАЯ
        # безобидная команда с пустым выводом в той же строке глушила С6
        # целиком, а молчание читается как подтверждение. Нет объекта — нет и
        # подтверждения, это тот же красный, что «команды рядом нет».
        ryadom = [(s, p) for s, p in komandy(okno) if any(o in s for o in obekty)] \
            if obekty else []
        if not ryadom:
            fraza = ' '.join(z[max(0, m.start() - 60):m.end() + 60].split())
            pochemu = (f"без команды рядом (±{RADIUS} символов)" if obekty else
                       "без названного объекта в backtick, к которому можно "
                       "привязать команду")
            msgs.append(("❌", "С6", f"утверждение «{m.group(0)}» {pochemu}: «…{fraza}…» "
                                     f"— урок 33: обе предпосылки такого вида оказались "
                                     f"ложны, обе проверялись одной командой"))
            continue
        for stroka, _p in ryadom:
            sost, rc, vyvod, _osh = pr.vypolnit(stroka)
            if sost != "ok" or rc != 0:
                continue
            strok = len([l for l in vyvod.splitlines() if l.strip()])
            if strok:
                msgs.append(("❌", "С6", f"утверждение «{m.group(0)}» опровергнуто "
                                         f"командой рядом: `{stroka}` даёт {strok} "
                                         f"строк(и) вывода — урок 33"))
                break
    return msgs


VLITIE_RE = re.compile(r'вле[йи]|влить|влитие|уже принята', re.I)


def check_s7_zona_sliyaniya(z, pr):
    """С7 (уроки 30, 6) — зона слияния не уже того, что ветка реально трогает.

    Считается НЕ по `git show` (он видит только вершину — ровно жалоба урока 6),
    а по `git diff --name-only <merge-base> <ветка>`: это вся ветка, а не её
    последний коммит.

    🔴 ЗОНА СЛИЯНИЯ — НЕ ЗОНА ЗАХОДА, и первый живой прогон показал цену путаницы:
    заход, чья собственная ЗОНА — два новых файла, получил красное на десяти путях
    чужой ветки, к его зоне отношения не имеющих. Сравнивать надо с зоной, которую
    заход назвал ДЛЯ ВЛИТИЯ (`--zone` рядом с «влей»); не назвал — сверять нечем,
    и это ⚠, а не красное.
    """
    # 🔴 КОНТЕКСТ ВЛИТИЯ — ОКНО ЛЮБОГО УПОМИНАНИЯ ПЛЮС ВСЯ СЕКЦИЯ «ВЛИТИЕ».
    # Верификатор §3 показал бесплатное отключение С7: имя ветки в шапке, приказ
    # «влей» с `--zone` — абзацем ниже, и окна в 300 символов вокруг ПЕРВОГО
    # упоминания не хватало. Естественная композиция захода выключала проверку.
    sp_vlitie = span_sekcii(z, r'^#+[^\n]*ВЛИТИЕ[^\n]*$')
    msgs = []
    for imya, pozicii in vetki(z).items():
        okna = [z[max(0, p - RADIUS):p + RADIUS] for p in pozicii]
        if sp_vlitie and any(sp_vlitie[0] <= p < sp_vlitie[1] for p in pozicii):
            okna.append(z[sp_vlitie[0]:sp_vlitie[1]])
        okna = [o for o in okna if VLITIE_RE.search(o)]
        if not okna:
            continue
        prefiksy = [t.strip('`') for o in okna
                    for t in re.findall(r'--zone\s+([^\s`]+)', o)]
        if not prefiksy:
            msgs.append(("⚠", "С7", f"ветка `{imya}` названа к влитию, но зона слияния "
                                     f"рядом не задана (`--zone` не найден) — что именно "
                                     f"вливать, гейту неизвестно"))
            continue
        sost, rc, _, _ = pr.vypolnit(f"git rev-parse --verify {imya}")
        if sost != "ok" or rc != 0:
            continue
        sost, rc, baza, _ = pr.vypolnit(f"git merge-base HEAD {imya}")
        if sost != "ok" or rc != 0 or not baza.strip():
            msgs.append(("⚠", "С7", f"точку расхождения с `{imya}` снять не удалось — "
                                     f"зона слияния не проверена"))
            continue
        sost, rc, vyvod, _ = pr.vypolnit(f"git diff --name-only {baza.strip()} {imya}")
        if sost != "ok" or rc != 0:
            continue
        tronuto = [l.strip() for l in vyvod.splitlines() if l.strip()]
        vne = [p for p in tronuto
               if not any(p == pref or p.startswith(pref.rstrip('/') + '/') for pref in prefiksy)]
        if vne:
            msgs.append(("❌", "С7", f"ветка `{imya}` названа к влитию, но трогает "
                                     f"{len(vne)} путь(ей) ВНЕ зоны слияния: "
                                     f"{', '.join(vne[:6])}"
                                     f"{'…' if len(vne) > 6 else ''} "
                                     f"(зона: {', '.join(prefiksy)}) — урок 30"))
    return msgs


# ── С8: раздел «ГИГИЕНА» на месте и слот зоны в нём заполнен ─────────────────
# Требование владельца 2026-08-09: раздел ГИГИЕНА рождается в КАЖДОМ заходе
# автоматически (`bootstrap_zahod.gigiena_blok`), аналитику остаются конкретные
# зоны. Без гейта это правило прожило бы неделю: место, которое можно оставить
# пустым и ничего за это не получить, оставляют пустым (`KONSTITUCIYA §11` —
# нечему краснеть, значит это не правило, а надежда).
#
# 🔴 ЧТО ИМЕННО СУДИТСЯ — и почему не больше. Только НАЛИЧИЕ раздела и НЕПУСТОТА
# слота зоны: это ровно то, за что отвечает генератор, и ровно то, что ломается
# при сборке захода руками. Судить содержимое пунктов Г1–Г6 гейт не может и не
# пытается — они выполняются ПОСЛЕ прогона, а этот гейт живёт ДО него; проверка,
# которая краснела бы на невыполненной ещё работе, краснела бы всегда, а такую
# отключают первым же вечером (Р31).
#
# 🔴 НЕ ДУБЛИРУЕТ С1/С3/С7. Те судят правильность файла-захода (существует ли
# ветка, существуют ли пути зоны, не уже ли зона слияния). С8 не проверяет ни
# существования путей, ни веток — только что место под гигиену есть и не пусто.
# Пересечение с З10 (`check_zahod.py`) тоже отсутствует: З10 сторожит блок §0.1
# ГИТ-КОНТУР — НАМЕРЕНИЕ до работы, С8 — раздел про СОСТОЯНИЕ после неё.
#
# 🔴 СУДИТСЯ ТОЛЬКО ЗАДАНИЕ (`zadanie()` режет по `## ПЛАН`) — как у С6/С7 и по
# той же причине: заход, ОБСУЖДАЮЩИЙ маркер пустоты в своём плане или отчёте,
# краснеть из-за цитаты не должен.
GIGIENA_ZAG_RE = re.compile(r'^##\s+4\.1\s.*ГИГИЕНА', re.M)
# 🔴 `[ \t]*`, а НЕ `\s*` — поймано первым же живым прогоном пустого слота.
# `\s` включает `\n`: на пустом слоте регексп перепрыгивал пустую строку и
# захватывал СЛЕДУЮЩУЮ (пункт «Г1…») как содержимое слота, то есть гейт на
# пустоту не краснел НИКОГДА — ровно та болезнь, ради которой он писался.
GIGIENA_ZONA_RE = re.compile(r'^\*\*ЗОНА[ \t]+ГИГИЕНЫ:\*\*[ \t]*([^\n]*)', re.M)
GIGIENA_MARKER_PUSTOTY = "НЕ ЗАПОЛНЕНО"


def check_s8_gigiena(z, pr):
    if not GIGIENA_ZAG_RE.search(z):
        return [("❌", "С8", "нет раздела «## 4.1 ГИГИЕНА» — заход не говорит, чем "
                            "исполнитель проверит СОСТОЯНИЕ репозитория перед сдачей "
                            "(зона доехала в git, второй репозиторий, невлитые ветки, "
                            "точка вызова нового инструмента, регистрация нового `.md`, "
                            "чужие пути в коммите). Раздел вшит в `bootstrap_zahod.py` "
                            "и появляется сам — его отсутствие означает заход, собранный "
                            "или правленный руками")]
    m = GIGIENA_ZONA_RE.search(z)
    if not m:
        return [("❌", "С8", f"в разделе «ГИГИЕНА» нет строки «{ '**ЗОНА ГИГИЕНЫ:**' }» — "
                            f"раздел и генератор разъехались, чинить генератор, а не "
                            f"заход")]
    telo = m.group(1).strip()
    if not telo:
        return [("❌", "С8", "слот «ЗОНА ГИГИЕНЫ» ПУСТ — Г1 без путей неисполним "
                            "(`git_zona.py check --zone` нечего дать), и приёмка не "
                            "сможет повторить проверку")]
    if GIGIENA_MARKER_PUSTOTY in telo:
        return [("❌", "С8", "слот «ЗОНА ГИГИЕНЫ» не заполнен — стоит маркер генератора "
                            "«НЕ ЗАПОЛНЕНО». Пересобери заход с непустым `--zone`")]
    return []


PROVERKI = [check_s1_vetki, check_s4_kriterij, check_s5_podkomandy,
            check_s6_utverzhdenie_net, check_s7_zona_sliyaniya, check_s8_gigiena]
PROVERKI_S_PUTYAMI = [check_s2_chuzhoj_repo, check_s3_puti]


def sudit(text: str, zahod_path: Path):
    """`(сообщения, прогон)`; сообщение — `(знак, код, текст)`, знак `❌` либо `⚠`.

    Три исхода различаются везде и это обязательно: красное — утверждение
    опровергнуто прогоном; ⚠ — проверить не удалось (это НЕ зелёное и НЕ красное,
    это «смотри руками»); молчание — подтверждено.
    """
    z = zadanie(text)
    pr = Prognon()
    msgs = []
    for fn in PROVERKI:
        msgs.extend(fn(z, pr))
    for fn in PROVERKI_S_PUTYAMI:
        msgs.extend(fn(z, pr, zahod_path))
    return msgs, pr


SLEPYE_ZONY = [
    "правдивость «этого нет» (С6) не проверяется — только наличие ОБЪЕКТА и "
    "команды про него рядом; «нет нигде» неопровержимо без указания, где искать. "
    "Словарь отрицаний из 12 словоформ неполон по построению",
    "имя ветки распознаётся по пяти формам записи (`--branch X`, «обязано быть "
    "`X`», `zahod/…`, «ветка `X`»); шестая форма пройдёт мимо С1 и С7",
    "С6 не судит строки markdown-таблиц, текст в «ёлочках» и врезки в круглых "
    "скобках — заход, который ЦИТИРУЕТ или ПОЯСНЯЕТ, ничего не утверждает о мире",
    "утверждение прозой, без адреса и без команды, невидимо этому гейту целиком",
    "число сверяется только со СЧИТАЮЩЕЙ командой (вывод — одно целое); "
    "`git show --stat` рядом с «ровно два пути» не сверяется",
    "С3 краснеет ТОЛЬКО на путях в адресных местах (якоря §0, КОНТРАКТ ЗОНЫ, "
    "КРИТЕРИЙ); путь, названный в прозе, печатается ⚠ одной строкой и красным "
    "не считается",
    "С3 резолвит путь от трёх баз (корень репо гейта, корень репо захода, папка "
    "арки) плюс индекс `git ls-files` — по голому имени и по хвосту пути; "
    "четвёртая база даст ложное «не существует»",
    "С3 не судит `.git/…`, слэш-команды (`/usage`) и голые расширения (`.md`)",
    "пути ЗОНЫ в С3 не краснеют: зона перечисляет и те файлы, которые исполнитель "
    "только создаст",
    "С3b (виден ли якорь с ветки исполнителя) судит только якоря секции "
    "«Прочитать ТОЛЬКО это»",
    "команда вне белого списка НЕ ВЫПОЛНЯЕТСЯ и потому не проверена — список "
    "отказов выше поимённо, молчать про них нельзя (урок 42)",
    "С8 судит только НАЛИЧИЕ раздела «ГИГИЕНА» и НЕПУСТОТУ слота зоны в нём. "
    "Выполнил ли исполнитель Г1–Г6 и что они ответили, гейт не знает и знать не "
    "может: он живёт ДО прогона, а они — после. Это проверяет приёмка по отчёту",
    "С8 краснеет на любом заходе, написанном ДО 2026-08-09 (раздела в них нет) — "
    "красное истинное, но живого шума не даёт: `check_sborki` зовётся только на "
    "свежесобранном файле из `bootstrap_zahod.py`, старые заходы не перелинтуются",
]


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Гейт сборки: прогоняет утверждения захода о мире и краснеет на "
                    "расхождении. Выполняет ТОЛЬКО команды из белого списка "
                    "(см. докстринг), без shell.")
    ap.add_argument("paths", nargs="+", help="файлы kod_*.md")
    a = ap.parse_args(argv)

    krasnyh = vsego_najdeno = vsego_vypolneno = 0
    otkazy_vse, potolok_vse, sudimo, fajlov_s_krasnym = [], 0, 0, 0
    for p in a.paths:
        path = Path(p).resolve()
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"❌ {p}: не читается ({e.__class__.__name__})")
            krasnyh += 1
            continue
        sudimo += 1
        msgs, pr = sudit(text, path)
        vsego_najdeno += pr.najdeno
        vsego_vypolneno += pr.vypolneno
        potolok_vse += pr.potolok_ischerpan
        otkazy_vse.extend(pr.otkazy)
        if msgs:
            print(f"── {p}")
            for znak, kod, soobshch in msgs:
                print(f"{znak} {kod}: {soobshch}")
            v_fajle = sum(1 for znak, _, _ in msgs if znak == "❌")
            krasnyh += v_fajle
            fajlov_s_krasnym += 1 if v_fajle else 0

    # 🔴 ПЕЧАТАЕТСЯ ВСЕГДА, включая полный зелёный: зелёный гейт с необъявленной
    # слепой зоной опаснее красного — ему верят (тот же приём, что у priyomka.py).
    print("\n═══ СЛЕПЫЕ ЗОНЫ И ОХВАТ — печать всегда, не гейт ═══")
    print(f"   судимо файлов: {sudimo} из {len(a.paths)}")
    print(f"   белый список: {len(BELYJ_SPISOK)} вход(ов) · таймаут {TAJMAUT} с · "
          f"потолок {POTOLOK} команд на файл")
    print(f"   команд найдено в текстах: {vsego_najdeno} · ВЫПОЛНЕНО: {vsego_vypolneno} · "
          f"отказано: {len(otkazy_vse)}")
    if potolok_vse:
        print(f"   ⚠ потолок исчерпан {potolok_vse} раз(а) — столько команд НЕ проверено")
    svodka = {}
    for stroka, prichina in otkazy_vse:
        svodka.setdefault(prichina.split('—')[0].strip(), []).append(stroka)
    if svodka:
        print("   НЕ ВЫПОЛНЕНО (проверьте вручную), по причинам:")
        for prichina, stroki in sorted(svodka.items(), key=lambda kv: -len(kv[1])):
            obraz = sorted(set(stroki))[:3]
            print(f"     · {prichina} — {len(stroki)} шт.: " +
                  "; ".join(f"`{s[:70]}`" for s in obraz))
    print("   структурно не проверяется:")
    for s in SLEPYE_ZONY:
        print(f"     · {s}")

    if krasnyh:
        print(f"\n❌ ГЕЙТ СБОРКИ: красных {krasnyh} в {fajlov_s_krasnym} файл(ах) "
              f"из {sudimo}.")
        return 1
    print(f"\n✅ ГЕЙТ СБОРКИ: красных нет — 0 из {sudimo} файл(ов) "
          f"(слепые зоны выше — они не зелёные).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
