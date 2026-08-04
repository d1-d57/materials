#!/usr/bin/env python3
"""git_zona.py — вся работа с git в `materials/` идёт через этот файл.

ДЛЯ ВЛАДЕЛЬЦА. Самый частый случай — «сохранить зону с сообщением» — ОДНА команда:

    python3 <корень репо>/_generator/tools/git_zona.py commit --zone <зона> -m "<что и зачем>" --push

Путь к файлу в ней — АБСОЛЮТНЫЙ, поэтому команда работает из ЛЮБОГО каталога:
инструмент находит репозиторий от самого себя (`__file__`), не от cwd. «Запустил
из ~ и питон не нашёл файла» (два срыва 23.07) закрывается только этой формой —
при относительном пути инструмент даже не загружается и подсказать не может.

Вокруг неё — четыре команды на остальные случаи:

    python3 _generator/tools/git_zona.py doctor    # что с репо прямо сейчас
    python3 _generator/tools/git_zona.py plan      # собрать черновик плана коммитов
    python3 _generator/tools/git_zona.py commit    # закоммитить по плану
    python3 _generator/tools/git_zona.py check     # что осталось вне git

Сломалось что-то непонятное → `doctor`, и покажи вывод Claude. Он самодостаточен:
печатает ветку, состояние индекса, лок, недоделанные merge/rebase, расхождение с
origin и всё, что вне git. По нему диагноз ставится без доступа к твоей машине.

ЗАЧЕМ ЭТОТ ФАЙЛ (не удалять, не «упрощать» вслепую).

За одну сессию арки 2026-07-21 работа ТРИЖДЫ не доехала в git. Разбор показал,
что виноват не забывчивый исполнитель, а устройство пути коммита:

  1. Гейт САМ ронял коммиты. `ARKA §6` велел Cowork гонять `git status --short`,
     а обычный `git status` НЕ read-only: он переписывает индекс и берёт
     `.git/index.lock`. Механизм, следивший, чтобы работа не терялась, отбирал
     лок у владельца ровно в момент ручного коммита.
  2. Коммит ехал ХЕНД-ОФФОМ — самым дырявым каналом фабрики по её же
     статистике (RUKOVODSTVO §Приёмка: 8 накопилось, 0 дошло). Владелец
     собирал и вставлял цепочку `&&`, обрыв которой посередине НЕВИДИМ
     (цена 17.07: коммита не было час при живой параллельной работе).
  3. Параллельные писатели (Cowork + Claude Code + владелец) не были разведены
     МЕХАНИЗМОМ. «Каждый коммитит свою зону» было правилом, которое можно
     нарушить молча, — и его нарушали (инцидент 2026-07-11: авто-коммит
     Фибоначчи утащил файлы чужого захода в свой коммит под своим именем).

ТРИ ОТВЕТА, ВШИТЫЕ В КОД:

  · `--no-optional-locks` во ВСЕХ вызовах — чтение индекс не трогает.
  · Лок занят → ЖДЁМ с отступом (по умолчанию до 90 с), а не падаем. Лок НИКОГДА
    не удаляем: из песочницы проверка «живой ли git» слепа, а снести лок у
    работающего git — испортить индекс.
  · `commit --zone <путь>` — коммитит ТОЛЬКО внутри зоны и ОТКАЗЫВАЕТСЯ трогать
    что-либо вне её. Разведение параллельных писателей становится механизмом:
    чужую работу физически нельзя забрать в свой коммит.
"""

import argparse
import os
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

# GIT_ZONA_REPO — ТОЛЬКО для фикстур: направляет инструмент на одноразовый репо
# в /tmp. Без этого поведение коммита проверить нечем: в боевом `materials/`
# песочница не может `unlink` в `.git/objects`, тестовый коммит падает с rc=128 —
# и это выглядит как содержательный отрицательный результат (цена: четыре ложных
# прогона за сессию 21.07, из-за них верную форму коммита искали вслепую).
# В одноразовом репо git работает полностью — проверено.
REPO = Path(os.environ.get("GIT_ZONA_REPO") or Path(__file__).resolve().parents[2])
PLAN = REPO / "_studio" / ".commit-plan"
LOCK_WAIT_SEC = 90
INCIDENTY = REPO / "_studio" / "zhurnal" / "_INFRA-git" / "INCIDENTY.md"


def in_sandbox():
    """Мы в песочнице Cowork? Тогда ПИСАТЬ в .git нельзя (см. отказ ниже).

    Детект по типу монтирования: репозиторий владельца лежит на обычной ФС,
    а в песочницу он проброшен через FUSE. Признак дешёвый и, главное, НЕ
    оставляет следов — проба «создать файл и удалить» в песочнице необратима
    (удалить его нечем, мусор остаётся в дереве навсегда).
    На macOS у владельца и у host-side Claude Code `/proc/mounts` нет вовсе ⇒
    False ⇒ им писать разрешено, как и должно быть.
    """
    try:
        with open("/proc/mounts", encoding="utf-8") as f:
            mounts = [ln.split() for ln in f if len(ln.split()) > 2]
    except OSError:
        return False
    best, fstype = "", ""
    repo = str(REPO)
    for parts in mounts:
        mp, typ = parts[1], parts[2]
        if (repo == mp or repo.startswith(mp.rstrip("/") + "/")) and len(mp) > len(best):
            best, fstype = mp, typ
    return fstype.startswith("fuse")


def refuse_write(action, suggest="commit"):
    """Единый отказ на любую ПИШУЩУЮ операцию из песочницы.

    🔴 ПОЧЕМУ ЗАПРЕТ, А НЕ «ДРУГАЯ ФОРМА КОММИТА» (решено 2026-07-22, экспериментом).
    В песочнице запрещён `unlink` во ВСЁМ монтировании. Git при любой записи
    создаёт временные файлы и потом их удаляет — удалить не может, и они
    остаются минами, которые блокируют репозиторий для ВСЕХ троих писателей.
    Проверено на одноразовом репозитории внутри того же монтирования:
      · `commit -- <pathspec>` → остаются `next-index-<PID>.lock`, `index.lock`,
        `HEAD.lock`; следующий git падает «File exists» (PID переиспользуются);
      · ОБЫЧНЫЙ `commit` без pathspec → мин меньше, но `HEAD.lock` и
        `objects/**/tmp_obj_*` остаются ВСЁ РАВНО ⇒ «другая форма» не лечит;
      · `GIT_INDEX_FILE` в /tmp НЕ помогает: git всё равно кладёт
        `next-index-*.lock` внутрь `.git`.
    Коммит при этом технически СОЗДАЁТСЯ — поэтому соблазн «ну прошло же»
    силён, а цена приходит следующему, кто упрётся в чужой лок.
    ⇒ Cowork в песочнице НЕ коммитер. Он готовит план и отдаёт одну команду.
    """
    print(f"⛔ {action} из песочницы Cowork — НЕЛЬЗЯ, и это не перестраховка.\n"
          "   Здесь запрещено удаление файлов, а git при записи оставляет\n"
          "   временные локи и мусорные объекты, снять которые отсюда нечем.\n"
          "   Репозиторий встанет для всех: владельца, Cowork и Claude Code.\n"
          "   (Полное «почему» и опыт — GIT-disciplina.md §2.)\n\n"
          "   → Работу делает ВЛАДЕЛЕЦ в своём терминале:\n\n"
          f"   cd <корень {REPO.name} на машине владельца>\n"
          f"   python3 _generator/tools/git_zona.py {suggest}\n\n"
          "   ⚠ COWORK: подставь в чат РЕАЛЬНЫЙ путь владельца, не этот плейсхолдер\n"
          f"     и НИКОГДА не путь песочницы ({REPO}) — такой папки у него нет,\n"
          "     будет `fatal: not a git repository` (инцидент 2026-07-11).")
    return 3


_LOCAL_ENV_VARS = None


def _git_env():
    """Окружение процесса БЕЗ унаследованных GIT_* (`GIT_DIR`, `GIT_INDEX_FILE`
    и т.п.) — иначе `git()` подчиняется чужому репозиторию МОЛЧА.

    🔴 НАЙДЕНО ВЕРИФИКАТОРОМ части A (заход 2026-08-03): `git rev-parse
    --git-dir` следует `GIT_DIR` из окружения БЕЗУСЛОВНО — `cwd=REPO`
    игнорируется целиком. Если процесс, которым запущен `git_zona.py`,
    унаследовал `GIT_DIR` (типичная утечка из git-хука, обёртки-скрипта,
    который сам когда-то был хуком, или забытого `export` в сессии терминала),
    `git_dir()` тихо укажет на ЧУЖУЮ рабочую копию — и `find_locks()` честно
    отчитается «свободно», проверив не тот каталог. Ровно тот класс риска, что
    уже назван в докстроке модуля («Внутри хука git экспортирует GIT_DIR…») и
    в `fixtures/git_zona/PROGNAT.sh` («ОБЯЗАТЕЛЬНО ПЕРВЫМ ХОДОМ: вычистить
    окружение git») — но там чистится окружение ФИКСТУРЫ, а не каждого
    вызова `git()` внутри самого инструмента.

    Список — `git rev-parse --local-env-vars`: то же самое, чем чистится
    фикстура. Кэш модульный: список имён переменных не зависит от репозитория
    и не меняется между вызовами — спрашивать его у git на каждый вызов было
    бы лишним процессом ради константы. `GIT_ZONA_REPO` — НЕ git-нативная
    переменная (это собственный переключатель инструмента, читается в Python
    ДО спуска в subprocess), в список `--local-env-vars` не попадает и не
    трогается.
    """
    global _LOCAL_ENV_VARS
    if _LOCAL_ENV_VARS is None:
        r = subprocess.run(["git", "--no-optional-locks", "rev-parse", "--local-env-vars"],
                           capture_output=True, text=True)
        _LOCAL_ENV_VARS = [v for v in r.stdout.split() if v]
    env = os.environ.copy()
    for v in _LOCAL_ENV_VARS:
        env.pop(v, None)
    return env


def git(*args, check=True):
    """Единственная дверь к git. --no-optional-locks не даёт чтению взять лок.

    Окружение — `_git_env()`, без унаследованных `GIT_*`: см. её докстроку.
    """
    r = subprocess.run(
        ["git", "--no-optional-locks", *args],
        cwd=REPO, capture_output=True, text=True, env=_git_env(),
    )
    if check and r.returncode != 0:
        sys.exit(f"❌ git {' '.join(args)} упал:\n{r.stderr.strip()}")
    return r


# ───── КАТАЛОГИ .git — ЛИЧНЫЙ vs ОБЩИЙ (часть A захода 2026-08-03) ─────
#
# ЗАЧЕМ. В рабочей папке worktree `.git` — не каталог, а ФАЙЛ-указатель
# (`gitdir: …/materials/.git/worktrees/<имя>`). Код, читавший `REPO / ".git"`
# как каталог, там слеп: `glob("*.lock")` по файлу возвращает пусто. Проверено
# прогоном: настоящий лок положен в `…/.git/worktrees/dobivka-vetok/`, `doctor`
# из этой папки напечатал «Локи в .git: ✅ свободно» — защита от гонки
# отсутствовала ровно там, где заведён параллелизм, и ровно в команде, которую
# канон велит запускать первой.
#
# `git rev-parse --git-dir` и `--git-common-dir` дают РАЗНОЕ внутри worktree:
#   · `--git-dir`        → …/worktrees/<имя> — ЛИЧНЫЙ: `index.lock`, `HEAD.lock`,
#     `index` — у каждой рабочей папки свои, общий коммит одной НЕ трогает другую;
#   · `--git-common-dir`  → …/materials/.git — ОБЩИЙ: `objects/`, упаковка — один
#     на все worktree, и лок/мусор там бьёт по каждому писателю разом.
# В основной папке (не-worktree) оба совпадают — код не различает случаи, просто
# спрашивает git, а не гадает по структуре `.git`.
def _resolve_git_path(rel_or_abs):
    p = Path(rel_or_abs)
    return p if p.is_absolute() else REPO / p


def git_dir():
    """Личный служебный каталог ЭТОЙ рабочей копии (локи, HEAD, index)."""
    return _resolve_git_path(git("rev-parse", "--git-dir", check=False).stdout.strip() or ".git")


def git_common_dir():
    """Общий каталог хранилища (objects, refs) — один на все worktree."""
    return _resolve_git_path(git("rev-parse", "--git-common-dir",
                                 check=False).stdout.strip() or ".git")


def wait_for_lock(limit=LOCK_WAIT_SEC):
    """Ждём чужой коммит вместо того, чтобы падать.

    Почему ждём, а не сносим: правило канона «pgrep пуст ⇒ лок стейл ⇒ удалить»
    в песочнице ЛОЖНО — она видит только свои процессы и хостовый git ей не
    виден. Условие, на котором стоит разрешение удалить лок, тут непроверяемо.

    🔴 `index.lock` — ЛИЧНЫЙ (`git_dir()`), не общий: коммит в СОСЕДНЕЙ рабочей
    папке НЕ держит лок здесь, и ждать его — значит стоять без причины.
    """
    lock = git_dir() / "index.lock"
    if not lock.exists():
        return True
    print(f"⏳ {lock} занят — рядом кто-то коммитит. Жду до {limit} с…")
    waited, step = 0, 2
    while waited < limit:
        time.sleep(step)
        waited += step
        if not lock.exists():
            print(f"   лок отпущен через {waited} с — продолжаю.")
            return True
    print(f"⛔ Лок держат дольше {limit} с. Ничего не делаю — файлы на диске целы.\n"
          "   Это НЕ поломка: рядом идёт длинный коммит. Подожди и повтори ту же\n"
          "   команду. Лок руками НЕ удалять, пока git реально работает.")
    return False


def dirty(zone=None):
    """[(код, путь)] — вне git. Пустой список = чисто."""
    out = git("status", "--porcelain", "--untracked-files=all").stdout
    rows = []
    for line in out.splitlines():
        if not line.strip():
            continue
        code, path = line[:2], line[3:].strip()
        if path.startswith('"') and path.endswith('"'):
            path = path[1:-1].encode().decode("unicode_escape").encode("latin-1").decode("utf-8")
        if zone and not in_zone(path, zone):
            continue
        rows.append((code, path))
    return rows


def in_zone(path, zone):
    z = zone.rstrip("/")
    return path == z or path.startswith(z + "/")


# ─────────────── карантин подозрительного untracked-мусора ───────────────
# Инцидент 23.07: `bootstrap_arka.py --help` принял флаг за имя арки и создал
# папку-сироту `_studio/zhurnal/--help/`. Она untracked, и каждый `plan` тянул
# её в черновик коммита вперемешку с настоящим — кто-то вручную выцеплял мусор
# из плана каждую коммит-сессию. Здесь мусор детектится и выносится отдельно.

def is_suspect(code, path):
    """Untracked-путь, у которого КАКОЙ-ЛИБО компонент имени начинается с `-`.

    Почти наверняка мусор от проглоченного флага. Легитимной арки/файла с таким
    именем не бывает ⇒ строгая эвристика «ведущий дефис в компоненте» даёт НОЛЬ
    ложных срабатываний. Проверяем каждый компонент, а не только первый: под
    `--untracked-files=all` папка `--help/` разворачивается в
    `…/--help/NAVIGATOR.md` — дефис оказывается в середине пути. Только для
    untracked (`??`): отслеживаемое и правленое — это работа, не мусор; парная
    защита в bootstrap_* (validate_slug) не даёт такому родиться заново.
    """
    return code == "??" and any(
        seg.startswith("-") for seg in path.split("/") if seg)


def suspect_root(path):
    """Обрезать путь по ПЕРВОМУ компоненту с ведущим `-` — это корень мусора.

    Папку сносим целиком (и показываем одной строкой), а не пофайлово:
    `_studio/zhurnal/--help/NAVIGATOR.md` → `_studio/zhurnal/--help`.
    """
    segs = path.split("/")
    for i, seg in enumerate(segs):
        if seg.startswith("-"):
            return "/".join(segs[:i + 1])
    return path


def suspect_roots(rows):
    """Отсортированные корни подозрительного мусора из dirty-строк (без дублей)."""
    return sorted({suspect_root(p) for c, p in rows if is_suspect(c, p)})


def print_suspect_block(suspect):
    """Единый вид карантина — мусор называется ОТДЕЛЬНО от честного «вне git»."""
    if not suspect:
        return
    print(f"\n⚠ Подозрительный мусор ({len(suspect)}; имя с ведущим `-`, "
          "вероятно проглоченный флаг) — НЕ работа, не коммитить:")
    for r in suspect:
        print(f"   ⚠ {r}")
    print("   Снять без shell:  python3 _generator/tools/git_zona.py purge")


def log_incident(symptom, hint):
    """Класс 4 (kod_commit-ux §2b): НЕУСПЕШНЫЙ commit сам оставляет след.

    Инструмент — единственная дверь к коммитам всех троих писателей, поэтому
    «единый дневник инцидентов даже без просьбы» держится его поведением, а не
    дисциплиной агентов: правило «пиши отчёт о поломках» в чужом чате забывают,
    и ничто не краснеет (KONSTITUCIYA §11). Разбор и уроки с ценой — ZHURNAL.md;
    сюда падает сырьё: симптом + подсказка инструмента + статус.

    Дедуп: тот же симптом на той же ветке в тот же день второй раз не пишется —
    иначе корзина зашумит повторами одного и того же и читать её бросят.
    Лог не смеет ни ронять инструмент, ни менять его код возврата: любая ошибка
    записи молча глотается (это журнал, не гейт).
    """
    try:
        branch = git("rev-parse", "--abbrev-ref", "HEAD", check=False).stdout.strip() or "?"
        stamp = time.strftime("%Y-%m-%d %H:%M")
        if INCIDENTY.exists():
            rows = [l for l in INCIDENTY.read_text(encoding="utf-8").splitlines()
                    if l.startswith("- ")]
            if rows and f" · {branch} · {symptom} · " in rows[-1] \
                    and rows[-1][2:12] == stamp[:10]:
                return
        else:
            INCIDENTY.parent.mkdir(parents=True, exist_ok=True)
            INCIDENTY.write_text(
                "# INCIDENTY — сырые симптомы неуспешных коммитов (пишет сам git_zona.py)\n\n"
                "> Входящая корзина, НЕ журнал уроков: при каждом неуспешном `commit`\n"
                "> инструмент САМ дописывает сюда строку — в любом чате, без просьбы.\n"
                "> Руками строки не заводятся. Разобранное переносится в `ZHURNAL.md`\n"
                "> уроком с ЦЕНОЙ; здесь у строки статус меняется на `→ ZHURNAL`.\n"
                "> Формат: `- дата время · ветка · симптом · → подсказка · статус`.\n\n",
                encoding="utf-8")
        with open(INCIDENTY, "a", encoding="utf-8") as f:
            f.write(f"- {stamp} · {branch} · {symptom} · → {hint} · статус: открыт\n")
    except OSError:
        pass


# ───────────────── зона и worktree-карта соседних веток ─────────────────
#
# Инцидент 2026-07-28: дерево переключили с `zahod/dek-paskal-v2` на
# `arka/mat-kostyak`, и 19 коммитов двух арок остались на покинутой ветке.
# `doctor` показывал текущую ветку и молчал про соседние. Отсюда родился
# СЧЁТНЫЙ сторож `print_branch_watch` («ветка впереди на N коммитов»).
#
# 🔴 СЧЁТНЫЙ СТОРОЖ СНЯТ (часть B захода 2026-08-03) — заменён `print_loss_watch`
# ниже, а не дополнен им. На живом репозитории 03.08 счётный дал 8 находок из
# 17 веток; сравнение поимённо (см. отчёт захода) показало, что по содержимому
# сторож называет ВСЕ ТЕ ЖЕ 8 веток явно — 4 как реальную потерю, 4 как
# безопасные с названной причиной (`main`/`arka/vneshnie-istorii` — только на
# `origin`; `zahod/storozh-vetok`/`zahod/tirazh-ocheredi` — содержимое доехало).
# Пропажи находок нет; два сторожа рядом на одном выводе только путали (43 %
# находок счётного были шумом — `RESHENIYA Р31`, гейт с таким процентом шума
# отключают). `zone_of`/`worktree_branches` остаются: их использует
# `print_loss_watch` для тех же целей (свёртка простыни путей, пометка «в
# другой рабочей папке»).


def zone_of(path):
    """Путь → ЗОНА, в терминах которой сторож говорит и предлагает лечение.

    Зона арки — `_studio/zhurnal/<арка>/`: именно так её называет `adopt --zone`,
    и именно на этом уровне случился инцидент. Всё прочее сворачивается до
    верхнего каталога — иначе на 222 путях сторож превратится в простыню, а
    простыню не читают (тот же класс, что «сотни ❌ старых нарушений»).
    """
    segs = [s for s in path.split("/") if s]
    if len(segs) >= 3 and segs[0] == "_studio" and segs[1] == "zhurnal":
        return "/".join(segs[:3])
    return segs[0] if segs else path


def worktree_branches():
    """{ветка: путь} для веток, вычекаученных в ДРУГИХ рабочих папках.

    Их невлитое — тоже находка (работа существует в одной версии не здесь), но
    лечение другое: там может идти живой заход, и `merge` притащит недоделанное.
    Поэтому такие ветки называются с пометкой, а не молчат: промолчать про
    worktree — ровно та дыра, из-за которой инцидент и произошёл.
    """
    res, path = {}, None
    for line in git("worktree", "list", "--porcelain", check=False).stdout.splitlines():
        if line.startswith("worktree "):
            path = line[len("worktree "):].strip()
        elif line.startswith("branch ") and path:
            if Path(path).resolve() != REPO.resolve():
                res[line[len("branch "):].strip().replace("refs/heads/", "", 1)] = path
            path = None
    return res

# ───── ЧТО ПРОПАДЁТ ПРИ УДАЛЕНИИ ВЕТКИ — по СОДЕРЖИМОМУ (заход 2026-08-03) ─────
#
# ЗАЧЕМ — ЕДИНСТВЕННЫЙ сторож веток (счётный `print_branch_watch` снят частью B
# захода `kod_dobivka-vetok.md`, см. комментарий над `zone_of` выше). Считать
# КОММИТЫ («ветка впереди») на живом репозитории 03.08 соврало В ОБЕ СТОРОНЫ:
# 7 находок из 16 веток, из них ТРИ не теряют при удалении ничего —
#   · `main` и `arka/vneshnie-istorii` целиком лежат на `origin/*`;
#   · `zahod/tirazh-ocheredi` довезла содержимое через `adopt`, который копирует
#     файлы, НЕ сливая историю: формально невлита навсегда, а терять нечего.
# 43 % находок — шум, а шумящий гейт отключают (`RESHENIYA Р31`), и тогда
# пропадает вся защита. Владелец спрашивает не «сколько коммитов не влито», а
# «ЧТО ПРОПАДЁТ, если эту ветку удалить».
#
# 🔴 КОРЕНЬ, ОБЩИЙ С УРОКАМИ 23 И 25: там доверились ИМЕНИ вместо объекта — пути
# вместо файла, короткому `%(refname:short)` вместо самой ссылки. Число коммитов —
# тоже имя содержимого, а не оно само. Поэтому здесь судятся БЛОБЫ.
#
# ТРИ УРОВНЯ, каждый следующий дороже и считается, только если предыдущий не дал
# зелёного (на 17 ветках уровень 1 закрывает 12 одним дешёвым вызовом):
#   1. ИСТОРИЯ — коммиты ветки, недостижимые НИ ИЗ ОДНОЙ другой ссылки (включая
#      теги и `origin/*`). Ноль ⇒ удаление не удаляет ни одного объекта. Это
#      точный ответ, а не эвристика.
#   2. СОДЕРЖИМОЕ — файлы, которые ветка САМА написала после развилки; их блобы
#      совпали с нашими ⇒ содержимое доехало.
#   3. ЧТО ИМЕННО — оставшиеся файлы делятся по ТРЕТЬЕЙ точке, базе развилки.
#      🔴 Именно третья точка отличает «у них новее» от «у нас новее». Сравнение
#      одних вершин (`diff HEAD <ветка>`) этого не умеет и 03.08 объявило бы у
#      `zahod/tirazh-ocheredi` 2 расходящихся файла, которых она НЕ писала вовсе:
#      разница ехала от нас, а не от неё.


def all_refs(exclude=None):
    """Все ссылки репозитория ПОЛНЫМИ именами (ветки, теги, remotes), кроме одной.

    Полные имена, а не короткие, — по уроку 25: короткое имя разрешается
    неоднозначно при теге-омониме, и сравнение пошло бы не с тем объектом.
    """
    out = git("for-each-ref", "--format=%(refname)",
              "refs/heads/", "refs/tags/", "refs/remotes/", check=False).stdout
    return [l.strip() for l in out.splitlines()
            if l.strip() and l.strip() != exclude]


def diff_status(a, b):
    """{путь: статус} между двумя деревьями (`A`/`M`/`D`).

    `-z`, поэтому кириллица и пробелы в путях приезжают как есть — без
    экранирования `core.quotepath` (в этом репо есть и то и другое, напр.
    `kurs leto 2026/**`, и на расщеплении такого пути уже падал shell-вариант).
    `--no-renames` — чтобы путь оставался буквальным: переименование, посчитанное
    за один файл, спрятало бы от списка и старое имя, и новое.
    """
    out = git("diff", "--name-status", "--no-renames", "-z", a, b, check=False).stdout
    parts = [p for p in out.split("\0") if p]
    return {parts[i + 1]: parts[i] for i in range(0, len(parts) - 1, 2)}


def batch_oids(queries):
    """[oid | None] по списку `<ссылка>:<путь>` — ОДНИМ процессом git.

    Поштучный `rev-parse` на каждую пару «ссылка × путь» дал бы сотни запусков
    внутри `doctor`; `cat-file --batch-check` отвечает на все одним. Порядок
    строк ответа совпадает с порядком запросов — по нему и сопоставляем
    (у отсутствующего пути строка вида `<запрос> missing`, оид там не встанет).
    """
    if not queries:
        return []
    r = subprocess.run(
        ["git", "--no-optional-locks", "cat-file", "--batch-check"],
        cwd=REPO, input="".join(q + "\n" for q in queries),
        capture_output=True, text=True)
    out = r.stdout.splitlines() if r.returncode == 0 else []
    res = []
    for i in range(len(queries)):
        line = out[i] if i < len(out) else ""
        first = line.split(" ")[0] if line else ""
        res.append(first if (" blob " in line and len(first) in (40, 64)) else None)
    return res


def blobs_v_istorii(pairs, refs):
    """Пути из `pairs` [(путь, оид)], чей блоб лежит в ИСТОРИИ `refs`, а не
    только на их вершинах.

    🔴 ЗАЧЕМ (заход `zhizn-vetki`, Ф0 — возражение к части A). Проверка по
    вершинам объявляет потерей работу, которая ДОЕХАЛА приёмкой и была развита
    дальше: на вершине лежит уже следующая версия файла, а версия ветки ушла
    в историю. Замер 03.08 на живом репозитории: из 16 «пропадающих» путей
    10 лежали в истории, три ветки были ложно-красными ЦЕЛИКОМ
    (`zahod/ochered-domov`, `zahod/priyomka-mehanizm`, `zahod/storozh-vetok`).
    Цена этой ошибки — не косметика: правило «уникальное есть ⇒ отказ»
    (`zakryt-vetku`) не закрыло бы 3 ветки из 5, то есть ровно те, ради
    которых механизм уборки и заведён.

    Вопрос метрики — «ЧТО ПРОПАДЁТ при удалении ветки», и достижимость из
    другой ссылки отвечает на него буквально: объект, достижимый из чужой
    истории, удаление этой ветки не удалит. Дороже вершинной проверки (по
    `rev-list` на путь), поэтому зовётся ВТОРЫМ шагом — только для тех путей,
    которые вершинная проверка не закрыла.
    """
    if not pairs or not refs:
        return set()
    found = set()
    for p, oid in pairs:
        r = git("rev-list", *refs, "--", p, check=False)
        if r.returncode != 0:
            continue
        commits = [l.strip() for l in r.stdout.splitlines() if l.strip()]
        if not commits:
            continue
        if oid in batch_oids([f"{c}:{p}" for c in commits]):
            found.add(p)
    return found


def blobs_elsewhere(pairs, refs):
    """Пути из `pairs` [(путь, оид)], чей ТОТ ЖЕ блоб лежит по ТОМУ ЖЕ пути
    хотя бы в одной из `refs`.

    🔴 ЗАЧЕМ. Работу переносит `adopt`, и перенести её могли НЕ на текущую
    ветку, а на соседнюю. Сравнение только с `HEAD` объявило бы такую ветку
    красной — ложная тревога ровно того сорта, из-за которого гейты отключают.
    Найдено верификатором захода 03.08 (случай «adopt был в main, а спрашиваем
    из третьего worktree») и признано регулярным: у владельца рабочих папок
    шесть, и ревизия запускается из того окна, которое открыто.
    """
    if not pairs or not refs:
        return set()
    got = batch_oids([f"{r}:{p}" for r in refs for p, _ in pairs])
    found, i = set(), 0
    for _ in refs:
        for p, oid in pairs:
            if i < len(got) and got[i] == oid:
                found.add(p)
            i += 1
    return found


def branch_loss(name, head="HEAD"):
    """Что пропадёт при удалении ветки `name`. Только чтение.

    Возвращает словарь с вердиктом (`safe` / `loss` / `skip`),
    причиной зелёного и тремя списками путей. Ничего не печатает: печать — дело
    вызывающего, а решение о вердикте обязано быть проверяемо отдельно от вида.
    """
    full = "refs/heads/" + name
    others = all_refs(exclude=full)
    # УРОВЕНЬ 1 — история.
    r = (git("rev-list", "--count", full, "--not", *others, check=False) if others
         else git("rev-list", "--count", full, check=False))
    if r.returncode != 0:
        return {"name": name, "verdict": "skip"}
    only = int(r.stdout.strip() or "0")
    res = {"name": name, "only": only, "propadet": [], "rashozhdenie": [],
           "udalila": [], "pushed": False}
    if only == 0:
        # 🔴 ЧЕМ ИМЕННО держится — часть вердикта, а не деталь. «Держит соседняя
        # ветка на этом же диске» и «держит только `origin/*`» — гарантии разного
        # качества: remote-tracking ссылка переживает удаление самого удалённого
        # репозитория и продолжает утверждать, что копия есть (случай верификатора
        # 03.08: бэкап снесли при чистке диска, ссылка осталась).
        loc = [x for x in others if not x.startswith("refs/remotes/")]
        rl = git("rev-list", "--count", full, "--not", *loc, check=False) if loc else None
        res["verdict"] = "safe"
        res["why"] = ("история целиком есть в других ЛОКАЛЬНЫХ ссылках"
                      if rl is not None and rl.returncode == 0 and rl.stdout.strip() == "0"
                      else "история есть ТОЛЬКО в `origin/*` — держится удалённой копией")
        return res

    # УРОВЕНЬ 2/3 — содержимое. База развилки и есть третья точка.
    mb = git("merge-base", head, full, check=False)
    base = mb.stdout.strip() if mb.returncode == 0 else ""
    if base:
        wrote = diff_status(base, full)
        ours = set(diff_status(base, head))
    else:
        # Общей истории нет вовсе — тогда «ветка написала» ВСЁ, что в ней лежит,
        # и нашего вклада с развилки не существует. Молчать здесь нельзя: это
        # самый тяжёлый случай, а не пограничный.
        wrote = {p: "A" for p in git("ls-tree", "-r", "--name-only", full,
                                     check=False).stdout.splitlines() if p}
        ours = set()
    differ = set(diff_status(head, full))

    for p in sorted(wrote):
        if wrote[p] == "D":
            # Ветка УДАЛИЛА файл. При её удалении пропадает намерение, а не
            # содержимое — в опасные не идёт, иначе чистка старья читалась бы
            # как потеря работы.
            res["udalila"].append(p)
        elif p not in differ:
            continue                      # блоб совпал с нашим ⇒ содержимое доехало
        elif p in ours:
            res["rashozhdenie"].append(p)  # писали обе стороны — сливать глазами
        else:
            res["propadet"].append(p)      # мы не трогали ⇒ этого текста здесь нет

    # 🔴 ПРОВЕРКА ПО ВСЕМ ССЫЛКАМ, А НЕ ТОЛЬКО ПО HEAD — иначе ложная тревога на
    # работе, которую `adopt` перенёс на СОСЕДНЮЮ ветку (случай верификатора 2.1).
    kand = res["propadet"] + res["rashozhdenie"]
    if kand:
        oids = batch_oids([f"{full}:{p}" for p in kand])
        pairs = [(p, o) for p, o in zip(kand, oids) if o]
        gde = [x for x in others
               if x.startswith("refs/heads/") or x.startswith("refs/remotes/")]
        doehalo = blobs_elsewhere(pairs, gde)
        # 🔴 ВТОРОЙ ШАГ — ИСТОРИЯ, а не только вершины (см. `blobs_v_istorii`).
        # Дороже, поэтому спрашивается только про то, что не закрыл первый.
        ostalos = [(p, o) for p, o in pairs if p not in doehalo]
        v_istorii = blobs_v_istorii(ostalos, gde)
        doehalo = doehalo | v_istorii
        if v_istorii:
            res["doehalo_istoriya"] = sorted(v_istorii)
        if doehalo:
            res["doehalo_sosed"] = sorted(doehalo)
            res["propadet"] = [p for p in res["propadet"] if p not in doehalo]
            res["rashozhdenie"] = [p for p in res["rashozhdenie"] if p not in doehalo]

    # 🔴 РАСХОЖДЕНИЕ — ТОЖЕ ПОТЕРЯ, и это правка по верификатору (случай 1.1).
    # Прежде «писали обе стороны» считалось «ничего не пропадёт». Но `adopt` сам
    # кладёт файлы ветки в наш коммит, после чего путь навсегда числится «нашим»,
    # и ЛЮБАЯ последующая работа ветки над этим файлом уходила в не-красное — то
    # есть глохла ровно на тех ветках, с которыми работали активнее всего.
    # Версия ветки здесь отсутствует ⇒ при удалении пропадёт именно она. Разница
    # с `propadet` только в ЛЕЧЕНИИ (сливать глазами, а не забирать целиком), и
    # она осталась — отдельным списком, а не отдельным вердиктом.
    if res["propadet"] or res["rashozhdenie"]:
        res["verdict"] = "loss"
    else:
        res["verdict"] = "safe"
        res["why"] = "содержимое доехало (история не влита, а файлы совпадают)"
        # 🔴 ОБЪЯВЛЕННАЯ СЛЕПАЯ ЗОНА, а не молчание: сверяются ВЕРШИНЫ. Работа,
        # написанная в промежуточном коммите ветки и затёртая в её же вершине
        # (штатный ход «подтянуть свежее из main в свою зону»), этой проверкой
        # не видна. Печатается строкой, чтобы зелёное не читалось шире, чем оно есть.
        res["vershiny"] = True
        return res

    # «Только на этой машине» — отдельная ось тяжести, а не то же самое.
    rem = [x for x in all_refs() if x.startswith("refs/remotes/")]
    if rem:
        rr = git("rev-list", "--count", full, "--not", *rem, check=False)
        res["pushed"] = rr.returncode == 0 and rr.stdout.strip() == "0"
    return res


def print_paths(paths, mark, limit=12):
    """Список путей с ограничением: простыню не читают, а обрезанную молча —
    принимают за полную. Поэтому остаток называется числом, а не съедается.
    """
    for p in paths[:limit]:
        print(f"        {mark} {p}")
    if len(paths) > limit:
        print(f"        … ещё {len(paths) - limit}")


def print_loss_watch(only=None, title=True):
    """🔴 `doctor`/`poteri`: что ПРОПАДЁТ при удалении ветки — списком ФАЙЛОВ,
    не числом.

    READ-ONLY: только `for-each-ref` / `rev-list` / `merge-base` / `diff` /
    `ls-tree` через общий git() с `--no-optional-locks`. Ничего не сливает, не
    удаляет и не переключает — лечение печатается строкой, которую владелец
    исполняет сам (`GIT-disciplina §0`).

    `only` — судить РОВНО эту ветку, а не все соседние (подкоманда `poteri
    --branch`); печать и вердикт — та же функция, чтобы `doctor` и `poteri` не
    могли разъехаться в двух реализациях одного и того же вопроса. Возвращает
    код: 0 — прогон состоялся (вне зависимости от того, есть потери), 1 — `only`
    не нашлась среди веток (опечатка в имени, не молчим об этом).
    """
    head = git("rev-parse", "--abbrev-ref", "HEAD", check=False).stdout.strip()
    names = [l.strip()[len("refs/heads/"):]
             for l in git("for-each-ref", "--format=%(refname)",
                          "refs/heads/", check=False).stdout.splitlines()
             if l.strip().startswith("refs/heads/")]
    # Текущую ветку не рассматриваем: её нельзя удалить, пока она вычекаучена.
    # В detached HEAD текущей ветки НЕТ ⇒ исключать нечего, смотрим все.
    others = [n for n in names if head == "HEAD" or n != head]
    if only is not None:
        if only == head:
            print(f"❌ `{only}` — это и есть текущая ветка, её нельзя удалить, "
                  "пока ты на ней.")
            return 1
        if only not in others:
            print(f"❌ Ветки `{only}` нет среди {len(others)} проверяемых.")
            return 1
        others = [only]
    where = "" if head == "HEAD" else f" (кроме текущей `{head}`)"
    if title:
        print("\n─── ЧТО ПРОПАДЁТ, ЕСЛИ УДАЛИТЬ ВЕТКУ (по содержимому) ───")
    if not others:
        print(f"✅ Веток, которые можно удалить, нет — проверено 0 из 0{where}.")
        return 0

    wt = worktree_branches()
    rows = [branch_loss(n, head) for n in others]
    skipped = [r["name"] for r in rows if r["verdict"] == "skip"]
    checked = len(others) - len(skipped)
    ohvat = f"проверено {checked} из {len(others)}{where}"
    loss = [r for r in rows if r["verdict"] == "loss"]
    safe = [r for r in rows if r["verdict"] == "safe"]

    def lechenie(r):
        zones = sorted({zone_of(p) for p in r["propadet"] + r["rashozhdenie"]})
        if r["name"] in wt:
            print(f"      ⚠ ветка вычекаучена в рабочей папке: {wt[r['name']]}\n"
                  "        там может идти живой заход — merge притащит недоделанное;\n"
                  "        сперва спроси того, кто в ней работает.")
        elif len(zones) == 1:
            print(f"      → python3 _generator/tools/git_zona.py adopt "
                  f"--branch {r['name']} --zone {zones[0]}\n"
                  f"        либо целиком: … git_zona.py merge {r['name']}")
        else:
            print(f"      → python3 _generator/tools/git_zona.py merge {r['name']}")

    if loss:
        print(f"\n🔴 ПРОПАДЁТ РАБОТА — на {len(loss)} ветк(е/ах) из {checked} лежит "
              "текст, которого здесь нет:")
        for r in loss:
            gde = "" if r["pushed"] else "; есть ТОЛЬКО на этой машине"
            n = len(r["propadet"]) + len(r["rashozhdenie"])
            print(f"\n   · {r['name']} — пропадёт файлов: {n}{gde}")
            if r["propadet"]:
                print("      мы этот файл с развилки не трогали — заберётся целиком:")
                print_paths(r["propadet"], "🔴")
            if r["rashozhdenie"]:
                print("      писали обе стороны — версия ветки здесь отсутствует, "
                      "сливать глазами:")
                print_paths(r["rashozhdenie"], "⚠")
            if r.get("doehalo_sosed"):
                print(f"      ✅ и ещё {len(r['doehalo_sosed'])} файл(ов) ветки уже "
                      "лежат в других ссылках — не потеря:")
                print_paths(r["doehalo_sosed"], "✅", limit=6)
            if r.get("doehalo_istoriya"):
                print(f"         из них {len(r['doehalo_istoriya'])} — в ИСТОРИИ "
                      "(доехали и были развиты дальше), а не на вершине.")
            lechenie(r)
    if not loss:
        # 🔴 ОТРИЦАТЕЛЬНЫЙ ВЕРДИКТ НЕСЁТ ОХВАТ В СЕБЕ: не «потерь нет», а
        # «потерь нет, проверено X из Y» — иначе «в порядке то, что я смотрел»
        # читается как «в порядке всё» (тот же урок, что у сторожа выше).
        print(f"✅ Потерь нет: удаление любой ветки не унесёт содержимого — {ohvat}.")

    if safe:
        # 🔴 БЕЗОПАСНЫЕ НАЗЫВАЮТСЯ ЯВНО, и отдельно — те, чьё содержимое доехало
        # копией: без этого `zahod/tirazh-ocheredi` неотличима от опасной, и
        # список опасных тонет в шуме — ровно то, из-за чего гейты отключают.
        dovezli = [r["name"] for r in safe
                   if r.get("why", "").startswith("содержимое доехало")]
        lokal = [r["name"] for r in safe if "ЛОКАЛЬНЫХ" in r.get("why", "")]
        tolko_origin = [r["name"] for r in safe
                        if r["name"] not in dovezli and r["name"] not in lokal]
        print(f"\n✅ Безопасны ({len(safe)} из {checked}):")
        if dovezli:
            print("   · содержимое ДОЕХАЛО, хотя история не влита: "
                  + ", ".join(dovezli))
            print("     ⚠ сверялись ВЕРШИНЫ веток: работа, затёртая внутри самой "
                  "ветки, этой проверкой не видна.")
        if lokal:
            print("   · история целиком есть в других ЛОКАЛЬНЫХ ссылках: "
                  + ", ".join(lokal))
        if tolko_origin:
            # Гарантия слабее локальной: remote-tracking ссылка переживает
            # удаление самого удалённого репозитория и продолжает утверждать,
            # что копия есть. Поэтому названо отдельной строкой, а не в общей куче.
            print("   · история есть ТОЛЬКО в `origin/*` — держится удалённой копией "
                  "(на диске её больше нет): " + ", ".join(tolko_origin))
    print(f"\n   Охват: {ohvat}. Ветки НЕ удалять — это решение владельца; "
          "здесь только названо, чем оно обойдётся.")
    if skipped:
        print(f"   ⚠ Не удалось прочитать {len(skipped)} ветк(у/и) — охват НЕПОЛОН: "
              + ", ".join(skipped))
    # 🔴 Код возврата ОТЛИЧАЕТСЯ от `doctor`, и это НЕ противоречие: `doctor` —
    # диагност, не гейт, ему нельзя печатать ❌ на здоровом исходе (урок арки
    # `2026-07-28_konspekt-l1`, «плана нет» при чистом дереве обязано быть rc=0).
    # `poteri` — целевая проверка вроде `check`: её зовут СПРОСИТЬ, и молчаливый
    # rc=0 при реальной потере обесценил бы её как гейт в скрипте/хуке.
    return 1 if loss else 0


def cmd_poteri(args):
    """🔴 Часть C захода `kod_dobivka-vetok.md`: то же, что блок в `doctor`, но
    ОТДЕЛЬНОЙ командой (владелец приходит СПРОСИТЬ, не как побочный эффект
    диагностики всего репо) и, по желанию, по ОДНОЙ ветке — `--branch <имя>`.

    Переиспользует `print_loss_watch`, а не дублирует: вопрос один и тот же
    («что пропадёт, если удалить ветку X»), и у двух путей входа обязана быть
    ОДНА реализация — иначе они разъедутся, как разъехались канон и код в
    уроке 23 (`bootstrap_zahod.py --worktree`).
    """
    return print_loss_watch(only=args.branch)


# ──── ЖИЗНЬ ВЕТКИ: надгробие, закрытие, воскрешение (заход `zhizn-vetki`) ────
#
# Все числа ниже — живые замеры этого захода, дата данных 2026-08-04.
#
# ЗАЧЕМ. Защита от потери ловит редкое событие, но не убирает то, что его
# порождает: ветки заводятся заходом и не закрываются НИКОГДА. Замер:
# 18 веток при пяти живых, 13 из них при удалении не теряют ничего. Через месяц
# их полсотни, и любой сторож на такой куче становится шумом ПО ПОСТРОЕНИЮ —
# сторожить дюжину мёртвых объектов бессмысленно (`RESHENIYA Р31`).
#
# 🔴 ГЛАВНЫЙ ПРИЁМ — НЕ СПОРИТЬ, КАКАЯ ПРОВЕРКА НАДЁЖНЕЕ, А СДЕЛАТЬ ЦЕНУ ОШИБКИ
# НУЛЕВОЙ. Перед удалением на вершину ветки ставится тег `mogila/<имя>`. Тег —
# ссылка: она держит коммиты вечно и весит ничего (замер: уникальные объекты
# ВСЕХ 19 веток вместе — 0.79 МБ при `.git` = 1.0 ГБ, у 11 веток из 19 их ноль).
# После этого удаление перестаёт быть необратимым В ПРИНЦИПЕ, а не «пока reflog
# не протух», и воскрешение — одна команда.
#
# 🔴 ЧЕГО НАДГРОБИЕ НЕ ДЕРЖИТ (Ф0 захода, каждый случай закрыт кодом ниже):
#   1. НЕЗАКОММИЧЕННОЕ в рабочей папке — тег держит КОММИТЫ, а файл, который
#      никогда не коммитили, не держит ничто. Это единственный по-настоящему
#      необратимый канал во всей конструкции, и он открыт ровно тем шагом, что
#      сносит рабочую папку вместе с веткой. Замер 03.08: грязных рабочих папок
#      3 из 7. ⇒ грязная папка = ОТКАЗ, и его НЕЛЬЗЯ перебить `--vsyo-ravno`.
#   2. ОСКОЛКИ `reset`/`amend`: коммиты в стороне от вершины тегом не
#      достижимы, а `branch -D` сносит и reflog ветки — они умирают НЕМЕДЛЕННО,
#      не «когда протухнет». Замер: такие осколки есть сейчас на 2 ветках из 19
#      (`arka/mat-kostyak` — 5, `teorkat-istochniki` — 1 «rollback point»).
#      ⇒ печатается предупреждением перед закрытием, найденное — поимённо.
#   3. КОЛЛИЗИЯ ИМЕНИ — тот самый корень «доверились ИМЕНИ, а не объекту».
#      Слаг захода повторяем; `tag -f` затёр бы ПЕРВОЕ надгробие, и работа
#      первой ветки стала бы недостижимой ровно тем механизмом, который её
#      страховал. ⇒ существующее надгробие = ОТКАЗ, `-f` не используется НИГДЕ.
#   4. ПАДЕНИЕ ПОСЕРЕДИНЕ: тег стоит, удаление не прошло (штатный случай —
#      ветка занята рабочей папкой, `branch -D` → rc=1). Ветка жива с
#      надгробием, и УРОВЕНЬ 1 метрики видит её историю в теге ⇒ объявляет
#      вечно-безопасной. Сторож слепнет ровно на той ветке, которую не закрыли.
#      ⇒ тег СНИМАЕТСЯ обратно при любой неудаче удаления.
#   5. Надгробие живёт на ОДНОМ ДИСКЕ: теги не уезжают обычным `push`.
#      «Вечно» = «пока цел диск» — печатается строкой, а не умалчивается.

MOGILA = "mogila/"
# `main` — ветка публикации сайта, у неё другая роль. Запрет в КОДЕ, а не в
# просьбе: правило, которое можно нарушить молча, будет нарушено (§11).
NELZYA_ZAKRYVAT = ("main",)


def mogila_ref(name):
    return "refs/tags/" + MOGILA + name


def worktree_gryaz(path):
    """(незакоммиченные пути, ИГНОРИРУЕМЫЕ пути) в рабочей папке.

    Спрашиваем git ИЗ ЭТОЙ папки, а не по общему индексу: у каждой рабочей
    папки свой индекс, и «чисто у меня» ничего не говорит про соседнюю.

    🔴 ИГНОРИРУЕМОЕ СЧИТАЕТСЯ ОТДЕЛЬНО — НАЙДЕНО ВЕРИФИКАТОРОМ ЗАХОДА.
    `status --porcelain --untracked-files=all` пути под `.gitignore` НЕ
    показывает, а `git worktree remove` БЕЗ `--force` сносит их молча (оба
    факта проверены прогоном). То есть проверка, чей смысл — «незакоммиченное
    надгробие не держит», пропускала ровно тот класс файлов, который в этом
    репозитории лежит вне git НАМЕРЕННО: `.gitignore` держит на диске
    `*/_snapshots/` (тарболлы рабочего дерева), pdf в `istochniki/`,
    `biblioteka/`, `literatura/` («нужны НА ДИСКЕ для поиска») и `carshering/`
    целиком. Заход, скачавший источники в свою рабочую папку, терял бы их при
    закрытии ветки — с печатью `✅` и без единого предупреждения.

    Разница в лечении, поэтому и в возврате два числа: незакоммиченное — это
    РАБОТА (отказ неперебиваемый), игнорируемое — чаще мусор (`__pycache__`,
    `.DS_Store`), но иногда ценность, и решение про него принимает человек
    (отказ перебивается `--vsyo-ravno`, список печатается).
    """
    p = Path(path)
    if not p.is_dir():
        return [], []
    r = subprocess.run(["git", "--no-optional-locks", "-C", str(p), "status",
                        "--porcelain", "--untracked-files=all", "--ignored"],
                       capture_output=True, text=True, env=_git_env())
    if r.returncode != 0:
        return [], []
    rabota, ignor = [], []
    for line in r.stdout.splitlines():
        if not line.strip():
            continue
        (ignor if line.startswith("!!") else rabota).append(line[3:].strip())
    return rabota, ignor


def glavnaya_rabochaya():
    """Путь ГЛАВНОЙ рабочей копии репозитория (не worktree-ответвления).

    🔴 ЗАЧЕМ ОТДЕЛЬНО ОТ `REPO`. Инструмент, запущенный ИЗ рабочей папки
    захода, считает своим корнем именно её — и тогда главная папка для него
    просто «соседняя», то есть попадает в `worktree_branches()` наравне с
    остальными и становится кандидатом на снос. Живой случай 04.08:
    `--vse-zelenye`, запущенный из рабочей папки, дошёл до `arka/mat-kostyak`
    (она зелёная по метрике и стоит в главной папке) и остановился только
    потому, что там СЛУЧАЙНО было 57 путей вне git. Была бы главная папка
    чиста — инструмент попытался бы снести рабочую копию всего репозитория.
    Общий каталог `.git` лежит внутри главной копии всегда — от него и
    считаем, а не от `REPO`.
    """
    gcd = git_common_dir()
    return gcd.parent if gcd.name == ".git" else REPO


def vetka_vychekauchena(name):
    """Стоит ли ветка в КАКОЙ-ЛИБО рабочей папке, включая основную.

    `worktree_branches()` про основную папку молчит нарочно (её лечение —
    другое), а здесь важен именно факт занятости: занятую ветку git удалить
    не даст, и узнать это надо ДО постановки надгробия.
    """
    for line in git("worktree", "list", "--porcelain", check=False).stdout.splitlines():
        if line.startswith("branch ") and \
                line[len("branch "):].strip() == "refs/heads/" + name:
            return True
    return False


def oskolki_vetki(name):
    """Коммиты из reflog ветки, недостижимые НИ ИЗ ОДНОЙ ссылки (случай 2).

    Именно они умрут вместе с reflog при удалении ветки — надгробие на вершине
    их не держит. Возвращает [(короткий хэш, строка reflog)].
    """
    r = git("reflog", "show", "--format=%H %gs", name, check=False)
    if r.returncode != 0:
        return []
    refs = all_refs()
    lost, vidano = [], set()
    for line in r.stdout.splitlines():
        parts = line.split(" ", 1)
        if not parts or not parts[0].strip():
            continue
        h = parts[0].strip()
        if h in vidano:
            continue
        vidano.add(h)
        if any(git("merge-base", "--is-ancestor", h, x, check=False).returncode == 0
               for x in refs):
            continue
        lost.append((h[:8], (parts[1] if len(parts) > 1 else "")[:60]))
    return lost


def stroka_voskresheniya(name):
    return f"python3 _generator/tools/git_zona.py voskresit --branch {name}"


def zakryt_odnu(name, head, wt, vsyo_ravno=None):
    """Закрыть ОДНУ ветку: метрика → надгробие → снос папки → снос ветки.

    Возвращает 0 при успехе, 1 при отказе. Печатает всё сама — вызывающему
    остаётся считать. Порядок шагов НЕ переставлять: каждый закрывает свой
    случай из шапки раздела.
    """
    full = "refs/heads/" + name
    if name in NELZYA_ZAKRYVAT:
        print(f"⛔ `{name}` не закрывается никогда — это ветка публикации сайта.")
        return 1
    if name == head:
        print(f"⛔ `{name}` — текущая ветка, её нельзя удалить, пока ты на ней.")
        return 1
    if git("rev-parse", "--verify", "--quiet", full, check=False).returncode != 0:
        print(f"⛔ Ветки нет: {name}")
        return 1

    # ── 1. МЕТРИКА: что пропадёт (та же `branch_loss`, что у `poteri`) ──
    res = branch_loss(name, head)
    if res.get("verdict") == "skip":
        print(f"⛔ `{name}` не читается — не трогаю, охват неполон.")
        return 1
    if res["verdict"] == "loss":
        n = len(res["propadet"]) + len(res["rashozhdenie"])
        print(f"🔴 `{name}` — НЕ закрываю: пропадёт файлов {n}, этого текста здесь нет.")
        if res["propadet"]:
            print("   мы этот файл с развилки не трогали — заберётся целиком:")
            print_paths(res["propadet"], "🔴")
        if res["rashozhdenie"]:
            print("   писали обе стороны — версия ветки здесь отсутствует:")
            print_paths(res["rashozhdenie"], "⚠")
        if not vsyo_ravno:
            print(f"   → сперва перенести: python3 _generator/tools/git_zona.py "
                  f"merge {name}\n"
                  f"   → либо, если это осознанный отказ от работы ветки, повтори с\n"
                  f"     `--vsyo-ravno \"<причина>\"` — надгробие всё равно ставится,\n"
                  f"     и воскрешение остаётся одной командой.")
            return 1
        print(f"   ⚠ --vsyo-ravno: закрываю несмотря на потерю. Причина: {vsyo_ravno}")
        log_incident(f"zakryt-vetku --vsyo-ravno: {name} — {vsyo_ravno}",
                     "работа ветки не перенесена; вернуть — voskresit --branch " + name)

    # ── 2. РАБОЧАЯ ПАПКА: незакоммиченное надгробие НЕ держит (случай 1) ──
    # Отказ неперебиваемый: это единственная реально необратимая потеря.
    put_wt = wt.get(name)
    # 🔴 ОСНОВНАЯ рабочая папка в `wt` НЕ значится нарочно (`worktree_branches`
    # отдаёт только соседние), и без этой проверки ветка основной папки пошла
    # бы прямо на `branch -D` — то есть надгробие ставилось бы, git отказывал
    # «used by worktree», и тег откатывался. Работает, но диагноз человеку
    # приходит от git, а не от инструмента. Живой случай: `arka/mat-kostyak`
    # стоит в основной папке и при этом зелёная по метрике, то есть попадает
    # в `--vse-zelenye` каждый раз.
    glavnaya = glavnaya_rabochaya()
    v_glavnoj = (put_wt is not None
                 and Path(put_wt).resolve() == Path(glavnaya).resolve())
    if v_glavnoj or (put_wt is None and vetka_vychekauchena(name)):
        print(f"⛔ `{name}` стоит в ГЛАВНОЙ рабочей папке — не закрываю.\n"
              f"   {glavnaya}\n"
              "   Её снести нельзя: это рабочая копия всего репозитория, а не\n"
              "   папка захода. Ветку, занятую рабочей папкой, git удалить не даст.\n"
              "   Сперва переведи главную папку на другую ветку.")
        return 1
    if put_wt:
        gryazno, ignoriruemoe = worktree_gryaz(put_wt)
        if gryazno:
            print(f"⛔ `{name}` — НЕ закрываю: в рабочей папке {len(gryazno)} "
                  f"путей вне git.\n   {put_wt}\n"
                  "   Надгробие держит КОММИТЫ; файл, который никогда не коммитили,\n"
                  "   не держит ничто — это единственная необратимая потеря здесь,\n"
                  "   и `--vsyo-ravno` её НЕ перебивает.\n"
                  "   Посмотреть:  python3 _generator/tools/git_zona.py check   "
                  f"(запусти из {put_wt})")
            print_paths(gryazno, "??", limit=8)
            return 1
        # 🔴 ИГНОРИРУЕМОЕ (найдено верификатором): `worktree remove` сносит его
        # молча, а `status` без `--ignored` о нём не говорит. В этом репозитории
        # под `.gitignore` намеренно лежат снапшоты и pdf-источники, поэтому
        # молчать нельзя. Но и запрещать намертво нельзя: тот же шаблон ловит
        # `__pycache__` и `.DS_Store`, а уборка, встающая на каждом `.DS_Store`,
        # не состоится вовсе. ⇒ отказ, перебиваемый названной причиной.
        if ignoriruemoe and not vsyo_ravno:
            print(f"⛔ `{name}` — НЕ закрываю: в рабочей папке {len(ignoriruemoe)} "
                  f"ИГНОРИРУЕМЫХ путей.\n   {put_wt}\n"
                  "   Они вне git по `.gitignore` — значит надгробие их не держит,\n"
                  "   а снос рабочей папки унесёт их молча. В этом репозитории так\n"
                  "   лежат снапшоты и pdf-источники, а не только кэш:")
            print_paths(ignoriruemoe, "!!", limit=8)
            print("   Мусор (`__pycache__`, `.DS_Store`) — повтори с "
                  "`--vsyo-ravno \"<причина>\"`.")
            return 1
        if ignoriruemoe:
            print(f"   ⚠ Игнорируемых путей в папке: {len(ignoriruemoe)} — "
                  "уйдут вместе с ней, надгробие их не держит.")

    # ── 3. НАДГРОБИЕ: имя занято ⇒ отказ, `-f` не используем НИКОГДА (случай 3) ──
    # 🔴 СРАВНЕНИЕ БЕЗ УЧЁТА РЕГИСТРА — НАЙДЕНО ВЕРИФИКАТОРОМ. Диск владельца
    # (APFS) и `/tmp` регистронезависимы, а git — нет: `rev-parse` по точному
    # имени НЕ найдёт упакованный `mogila/Zametki`, тег `mogila/zametki`
    # создастся loose-файлом, и дальше ОБА имени разрешаются в ОДИН файл. Тогда
    # `voskresit` вернёт ветку на ЧУЖУЮ вершину (сверка по хэшу бесполезна:
    # обе её стороны читают одну ссылку), а один `tag -d` снесёт оба надгробия
    # разом — работа старой ветки не держится больше ничем. Экзотика (в этом
    # репозитории все имена в нижнем регистре), но цена — тихая необратимая
    # потеря, поэтому сравниваем casefold по всему списку могил, а не точным
    # именем через `rev-parse`.
    zanyato = [l.strip() for l in git("for-each-ref", "--format=%(refname:short)",
                                      "refs/tags/" + MOGILA, check=False).stdout.splitlines()
               if l.strip().casefold() == (MOGILA + name).casefold()]
    if zanyato:
        stoit = git("rev-parse", "--short", "refs/tags/" + zanyato[0],
                    check=False).stdout.strip()
        print(f"⛔ `{name}` — надгробие `{zanyato[0]}` УЖЕ есть (на {stoit}).\n"
              "   Не перезаписываю: под этим именем уже похоронена другая ветка,\n"
              "   и `-f` сделал бы ЕЁ работу недостижимой. Сперва разбери старое:\n"
              f"   {stroka_voskresheniya(zanyato[0][len(MOGILA):])}")
        if zanyato[0] != MOGILA + name:
            print(f"   ⚠ Имена различаются только РЕГИСТРОМ (`{zanyato[0]}` vs "
                  f"`{MOGILA}{name}`).\n     На этом диске git разрешил бы оба "
                  "в одну ссылку — и потерял бы одно из двух.")
        return 1

    vershina = git("rev-parse", full, check=False).stdout.strip()
    # 🔴 ОСКОЛКИ ХОРОНИМ ТОЖЕ — ПРАВКА ПО ВЕРИФИКАТОРУ. Прежде они лишь
    # печатались строкой ПОСЛЕ удаления, то есть соболезнованием: их держал
    # reflog ветки, `branch -D` сносит `logs/refs/heads/<имя>`, а
    # `worktree remove` — личный `logs/HEAD` рабочей папки; оба держателя
    # исчезают одним ходом, и объект умирает при ближайшем `gc` (верификатор
    # воспроизвёл: `gc --prune=now` → `could not get object info`). Хэши в
    # выводе терминала после этого бесполезны. Тег стоит ничего и держит
    # вечно — значит хоронить надо и их. Имя `mogila-oskolok/<ветка>/<хэш>`, а
    # не `mogila/<ветка>/…`: `mogila/<ветка>` уже ТЕГ, и вложенное имя под ним
    # git создать не даст (D/F-конфликт).
    oskolki = oskolki_vetki(name)
    pohoronennye_oskolki = []
    for h, _ in oskolki:
        polnyj = git("rev-parse", h, check=False).stdout.strip() or h
        imya = f"mogila-oskolok/{name}/{h}"
        if git("tag", imya, polnyj, check=False).returncode == 0:
            pohoronennye_oskolki.append(imya)
    r = git("tag", MOGILA + name, full, check=False)
    if r.returncode != 0:
        print(f"❌ `{name}` — надгробие не поставилось (rc={r.returncode}): "
              f"{r.stderr.strip().splitlines()[0] if r.stderr.strip() else ''}\n"
              "   Ветку НЕ трогаю: без надгробия удаление необратимо.")
        return 1

    def snyat_nadgrobie(pochemu):
        git("tag", "-d", MOGILA + name, check=False)
        for t in pohoronennye_oskolki:
            git("tag", "-d", t, check=False)
        print(f"❌ `{name}` — {pochemu}. Надгробие СНЯТО обратно: ветка жива, и\n"
              "   оставленный тег объявил бы её вечно-безопасной для сторожа.")

    # ── 4. РАБОЧАЯ ПАПКА СНОСИТСЯ ДО ВЕТКИ: занятую ветку git удалить не даст ──
    if put_wt:
        if Path(put_wt).is_dir():
            r = git("worktree", "remove", put_wt, check=False)
            if r.returncode != 0:
                snyat_nadgrobie(f"рабочая папка не снялась: "
                                f"{r.stderr.strip().splitlines()[0] if r.stderr.strip() else ''}")
                return 1
        else:
            # Папки нет, а запись есть — та самая осиротевшая служебная запись.
            git("worktree", "prune", check=False)

    # 🔴 СВЕРКА ВЕРШИНЫ ПЕРЕД УДАЛЕНИЕМ — НАЙДЕНО ВЕРИФИКАТОРОМ (гонка).
    # Между `git tag` и `git branch -D` лежит целый `worktree remove`, а до них —
    # весь `branch_loss` с десятками git-вызовов. Всё, что второй писатель
    # закоммитит в это окно, надгробие НЕ держит: тег зафиксировал прежнюю
    # вершину, а `-D` удаляет ветку не глядя. Верификатор воспроизвёл прогоном:
    # коммит, врезанный сразу после `tag`, стал unreachable, и `voskresit`
    # бодро отчитался «вершина совпала с надгробием» — с ней и совпала, только
    # ветка успела уехать дальше. В этом монорепо параллельные рабочие папки —
    # штатный режим, поэтому окно закрываем перечитыванием ссылки.
    seychas = git("rev-parse", full, check=False).stdout.strip()
    if seychas != vershina:
        snyat_nadgrobie(f"ветка уехала во время закрытия ({vershina[:8]} → "
                        f"{seychas[:8]}): рядом писал кто-то ещё, и надгробие "
                        f"держало бы уже не ту вершину")
        print("   Повтори команду — метрика пересчитается на новой вершине.")
        return 1

    # ── 5. ВЕТКА: `-D`, НИКОГДА `-d` ──
    # `-d` судит по ИСТОРИИ и откажет там, где терять нечего: работа доезжает
    # копированием содержимого (`adopt`), а не слиянием, и формально невлитой
    # ветка остаётся навсегда. Безопасность здесь держит метрика выше и
    # надгробие, а не мнение git о графе коммитов.
    r = git("branch", "-D", name, check=False)
    if r.returncode != 0:
        snyat_nadgrobie(f"ветка не удалилась (rc={r.returncode}): "
                        f"{r.stderr.strip().splitlines()[0] if r.stderr.strip() else ''}")
        return 1

    print(f"✅ `{name}` закрыта. Надгробие: {MOGILA}{name} → {vershina[:8]}")
    if put_wt:
        print(f"   Рабочая папка снята: {put_wt}")
    if oskolki:
        print(f"   Осколков вне всех ссылок было {len(oskolki)} (reset/amend) — "
              f"их держал reflog ветки,\n   и он удалён вместе с ней; "
              f"похоронено отдельными надгробиями: {len(pohoronennye_oskolki)}")
        for (h, s), t in zip(oskolki, pohoronennye_oskolki):
            print(f"        {h}  {s}\n          вернуть: python3 "
                  f"_generator/tools/git_zona.py voskresit --tag {t} "
                  f"--branch <имя новой ветки>")
        if len(pohoronennye_oskolki) < len(oskolki):
            print(f"   ⚠ {len(oskolki) - len(pohoronennye_oskolki)} осколк(ов) "
                  "похоронить НЕ удалось — они держались только reflog'ом "
                  "и умрут при ближайшем `gc`.")
    print(f"   Воскресить одной командой:\n     {stroka_voskresheniya(name)}")
    return 0


def cmd_zakryt_vetku(args):
    """Закрыть ветку(и) безопасно: надгробие + удаление + строка воскрешения."""
    if in_sandbox():
        rest = ("zakryt-vetku --vse-zelenye" if args.vse_zelenye
                else f"zakryt-vetku --branch {args.branch or '<ветка>'}")
        return refuse_write("Закрытие ветки", suggest=rest)
    if not args.branch and not args.vse_zelenye:
        print("⛔ Нужна ветка: `zakryt-vetku --branch <имя>` — либо "
              "`--vse-zelenye`\n   (подмести все, у кого метрика зелёная).")
        return 1
    if args.branch and args.vse_zelenye:
        print("⛔ `--branch` и `--vse-zelenye` вместе не имеют смысла: либо одна "
              "названная,\n   либо все зелёные.")
        return 1

    head = git("rev-parse", "--abbrev-ref", "HEAD", check=False).stdout.strip()
    wt = worktree_branches()
    names = [l.strip()[len("refs/heads/"):]
             for l in git("for-each-ref", "--format=%(refname)",
                          "refs/heads/", check=False).stdout.splitlines()
             if l.strip().startswith("refs/heads/")]
    bylo = len(names)

    if args.branch:
        celi = [args.branch]
    else:
        # 🔴 Отбор ТОЙ ЖЕ функцией, что печатает `poteri`: два входа в один
        # вопрос обязаны иметь одну реализацию, иначе разъедутся (урок 23).
        celi = [n for n in names
                if n != head and n not in NELZYA_ZAKRYVAT
                and branch_loss(n, head).get("verdict") == "safe"]
        if not celi:
            print(f"✅ Подметать нечего: зелёных веток нет — проверено "
                  f"{len([n for n in names if n != head])} из {bylo - 1}.")
            return 0
        print(f"═══ подметание: {len(celi)} зелёных ветк(и/ок) из {bylo} ═══\n")

    zakryto, otkazano = [], []
    for n in celi:
        rc = zakryt_odnu(n, head, wt, vsyo_ravno=args.vsyo_ravno)
        (zakryto if rc == 0 else otkazano).append(n)
        print()

    stalo = len([l for l in git("for-each-ref", "--format=%(refname)",
                                "refs/heads/", check=False).stdout.splitlines() if l.strip()])
    print(f"── итог: закрыто {len(zakryto)}, отказано {len(otkazano)}. "
          f"Веток было {bylo}, стало {stalo}.")
    if otkazano:
        print("   не закрыты: " + ", ".join(otkazano))
    if zakryto:
        print("   ⚠ Надгробия живут на ЭТОМ диске: обычный `push` теги не вывозит.\n"
              "     «Держит вечно» здесь значит «пока цел диск».")
    return 1 if otkazano else 0


def cmd_voskresit(args):
    """Вернуть ветку из надгробия и снять надгробие — обратная сторона закрытия.

    Она же печатается как «команда воскрешения»: голый `git branch X mogila/X`
    в чат владельцу выдавать нельзя (`GIT-disciplina §0` — весь git через этот
    инструмент), а обратимость, ради которой вся конструкция, обязана быть
    ОДНОЙ командой, а не инструкцией из трёх шагов.
    """
    if in_sandbox():
        return refuse_write("Воскрешение ветки",
                            suggest=f"voskresit --branch {args.branch}")
    name = args.branch
    # `--tag` — воскрешение ОСКОЛКА (коммита, отвязанного `reset`/`amend`):
    # у него нет своего имени ветки, поэтому имя задаёт человек. Тот же путь,
    # та же сверка по хэшу, то же снятие тега после успеха.
    ref = ("refs/tags/" + args.tag.lstrip("/")) if args.tag else mogila_ref(name)
    snimaemyj_teg = args.tag if args.tag else (MOGILA + name)
    if git("rev-parse", "--verify", "--quiet", ref, check=False).returncode != 0:
        print(f"⛔ Надгробия `{snimaemyj_teg}` нет — воскрешать нечего.\n"
              "   Что похоронено: python3 _generator/tools/git_zona.py mogily")
        return 1
    if git("rev-parse", "--verify", "--quiet", "refs/heads/" + name,
           check=False).returncode == 0:
        print(f"⛔ Ветка `{name}` уже существует — не перезаписываю её могилой.\n"
              "   Сравнить руками: работа под тем же именем идёт прямо сейчас.")
        return 1
    vershina = git("rev-parse", ref + "^{commit}", check=False).stdout.strip()
    r = git("branch", name, ref, check=False)
    if r.returncode != 0:
        print(f"❌ Ветка не создалась (rc={r.returncode}): {r.stderr.strip()}")
        return 1
    # 🔴 СВЕРКА ПО ХЭШУ, А НЕ ПО «команда прошла»: вершина обязана совпасть
    # с той, что держало надгробие, — иначе воскрешение вернуло не то.
    stalo = git("rev-parse", "refs/heads/" + name, check=False).stdout.strip()
    if stalo != vershina:
        print(f"❌ Вершина не совпала: надгробие держало {vershina[:8]}, "
              f"ветка встала на {stalo[:8]}. Надгробие НЕ снимаю.")
        return 1
    git("tag", "-d", snimaemyj_teg, check=False)
    print(f"✅ `{name}` воскрешена: вершина {stalo[:8]} (совпала с надгробием).\n"
          f"   Надгробие `{snimaemyj_teg}` снято — ветка снова живая и снова "
          "видна сторожу.\n"
          f"   Рабочая папка НЕ восстанавливается: `git_zona.py worktree add "
          f"<имя> --branch {name}`")
    return 0


def cmd_mogily(args):
    """Что похоронено — read-only список надгробий."""
    # 🔴 ПРЕФИКС, А НЕ `mogila/*`. Поймано на живом прогоне 04.08: со звёздочкой
    # `for-each-ref` матчит РОВНО ОДИН сегмент имени, и надгробия веток вида
    # `zahod/<слаг>` (то есть почти всех) выпадали молча — команда печатала
    # «Надгробий: 3» при двенадцати живых. Тихая потеря охвата в самой команде,
    # которая существует, чтобы показывать, что похоронено: воскрешать пришли
    # бы то, чего в списке нет. Тот же корень, что у всего механизма — доверие
    # ИМЕНИ (здесь — шаблону имени) вместо самого набора объектов.
    rows = [l.strip() for l in git("for-each-ref",
            "--format=%(refname:short) %(objectname:short) %(creatordate:short)",
            "refs/tags/" + MOGILA, check=False).stdout.splitlines() if l.strip()]
    oskolki = [l.strip() for l in git("for-each-ref",
               "--format=%(refname:short) %(objectname:short) %(creatordate:short)",
               "refs/tags/mogila-oskolok/", check=False).stdout.splitlines() if l.strip()]
    if not rows and not oskolki:
        print("✅ Надгробий нет — закрытых веток в репозитории не числится.")
        return 0
    print(f"Надгробий: {len(rows)}")
    for r in rows:
        parts = r.split()
        imya = parts[0][len(MOGILA):]
        print(f"   · {parts[0]:<40} {' '.join(parts[1:])}")
        print(f"     вернуть: {stroka_voskresheniya(imya)}")
    if oskolki:
        # Осколки — коммиты, отвязанные `reset`/`amend`: своего имени ветки у
        # них нет, поэтому и возврат другой формой.
        print(f"\nНадгробий-осколков: {len(oskolki)} (коммиты вне вершин, "
              "reset/amend)")
        for r in oskolki:
            parts = r.split()
            print(f"   · {parts[0]:<40} {' '.join(parts[1:])}")
            print(f"     вернуть: python3 _generator/tools/git_zona.py voskresit "
                  f"--tag {parts[0]} --branch <имя новой ветки>")
    return 0


# ─────────────────────────────── doctor ───────────────────────────────

def cmd_doctor(args):
    """Один вызов, отвечающий «что не так с репо». Вывод самодостаточен."""
    print("═══ git doctor ═══\n")

    head = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if head == "HEAD":
        print("🔴 DETACHED HEAD — ты не на ветке. Коммит здесь потеряется при "
              "переключении.\n   Лечение: `git checkout <ветка>` (см. список ниже).")
    else:
        print(f"Ветка: {head}")
    print(f"HEAD:  {git('log', '-1', '--oneline').stdout.strip()}")

    # незаконченные операции — частая причина «ничего не коммитится».
    # 🔴 ЛИЧНЫЙ каталог (`git_dir()`), не `REPO / ".git"`: в worktree это файл-
    # указатель, а MERGE_HEAD/rebase-merge и т.п. — состояние ЭТОЙ рабочей копии,
    # оно лежит в персональном `…/worktrees/<имя>/`, не в общем `.git`.
    g = git_dir()
    stuck = [n for n, p in [
        ("MERGE — незаконченное слияние", g / "MERGE_HEAD"),
        ("REBASE — незаконченный ребейз", g / "rebase-merge"),
        ("REBASE (apply)", g / "rebase-apply"),
        ("CHERRY-PICK", g / "CHERRY_PICK_HEAD"),
        ("BISECT", g / "BISECT_LOG"),
    ] if p.exists()]
    if stuck:
        print("\n🔴 Репозиторий в НЕЗАКОНЧЕННОЙ операции — пока она висит, обычный "
              "коммит не пройдёт:")
        for s in stuck:
            print(f"   · {s}")
        print("   Это и есть «что-то не коммитится». Покажи этот вывод Claude — "
              "выход зависит от того, что начинали.")

    # 🔴 ВСЕ локи и мусор, а не только index.lock.
    # Цена (22.07): висели `next-index-15.lock`, `next-index-22.lock` и
    # `HEAD.lock`, а doctor смотрел ровно один файл и молчал — два цикла
    # диагностики прошли вслепую. Диагност, не видящий самого частого
    # состояния-блокера, отправляет читателя искать причину не там.
    locks, junk = find_locks()
    def age_of(p):
        try:
            m = int((time.time() - p.stat().st_mtime) / 60)
            return f"{m} мин назад" if m < 120 else f"{m // 60} ч назад"
        except OSError:
            return "?"

    # ЛОКИ — блокеры: пока висят, запись не пройдёт ни у кого.
    if locks:
        print("\n🔴 ЛОКИ в .git — репозиторий НЕ примет запись, ни от кого:")
        for p in locks:
            # 🔴 Путь ПОЛНЫЙ, не `relative_to(REPO)`: личный `git_dir()` внутри
            # worktree лежит ВНЕ рабочей папки (`…/materials/.git/worktrees/<имя>`),
            # и `relative_to` там упал бы ValueError.
            print(f"   {p}   ({age_of(p)})")
        print("   Свежий (секунды–минуты) — рядом РЕАЛЬНО идёт коммит: ЖДАТЬ, не трогать.\n"
              "   Старый — мёртвая мина от упавшего процесса.")
    else:
        print("\nЛоки в .git: ✅ свободно")

    # tmp_obj — НЕ блокер, просто мусор от прерванной записи. Тревогу не поднимаем.
    if junk:
        print(f"\nМусорные объекты (`tmp_obj_*`): {len(junk)} шт., "
              f"старейшему {age_of(junk[0])} — на работу не влияют, но копятся.")

    if locks or junk:
        print("   Уборка — одной командой (владелец; сама щадит свежий лок живого git):")
        print("     python3 _generator/tools/git_zona.py clean")

    if in_sandbox():
        print("\n⚠ Ты в песочнице Cowork (репозиторий смонтирован через FUSE).\n"
              "  Читать можно всё; ПИСАТЬ нельзя — `commit` и `worktree` откажутся.\n"
              "  Это защита: здесь запрещено удаление, и любая запись оставляет мины.")

    # расхождение с origin: работа в git, но только на этой машине
    up = git("rev-parse", "--abbrev-ref", "@{upstream}", check=False)
    if up.returncode == 0:
        ahead = git("rev-list", "--count", "@{upstream}..HEAD").stdout.strip()
        behind = git("rev-list", "--count", "HEAD..@{upstream}").stdout.strip()
        print(f"Отслеживает: {up.stdout.strip()} — впереди на {ahead}, позади на {behind}")
        if ahead != "0":
            print(f"   ⚠ {ahead} коммит(ов) есть только на этой машине. "
                  "Смерть диска = потеря. `git push` их вывезет.")
    else:
        print(f"Отслеживаемой ветки нет: `{head}` живёт только локально.")
        print("   ⚠ Всё, что в ней, есть ТОЛЬКО на этой машине.")

    rows = dirty()
    suspect = suspect_roots(rows)
    clean = [(c, p) for c, p in rows if not is_suspect(c, p)]
    print(f"\nВне git: {len(clean)} путей.")
    if clean:
        by_top = {}
        for code, p in clean:
            by_top.setdefault(p.split("/")[0], []).append(code)
        for top in sorted(by_top):
            cs = by_top[top]
            print(f"   {len(cs):>4}  {top}"
                  f"   (новых {sum(1 for c in cs if c == '??')}, "
                  f"правленых {sum(1 for c in cs if c != '??')})")
        print("\n→ `git_zona.py plan` соберёт черновик коммитов, дальше `commit`.")
    else:
        print("   ✅ всё доехало.")
    print_suspect_block(suspect)

    # 🔴 Сторож соседних веток — САМ, без отдельной команды (требование 3
    # спецификации инцидента 2026-07-28). Стоит здесь, а не в конце: находка про
    # потерянную ветку важнее списка последних коммитов. Раньше здесь стояли ДВА
    # блока (счётный + по содержимому) — счётный снят частью B захода
    # `kod_dobivka-vetok.md`: сравнение поимённо на живом репозитории показало,
    # что он не находит ничего, чего не находит блок по содержимому, а 43 % его
    # находок были шумом (см. отчёт захода).
    print_loss_watch()

    # Разбор инцидентов — ПЕЧАТЬ, не гейт (гейт стоит на закрытии сессии,
    # `zakryt_sessiyu.py`). Видимость каждый день `doctor` не даёт забыть про
    # разбор до самого закрытия (`kod_gejt-razbora.md`). Отложенный импорт —
    # та же причина, что у `dnevnik` в `zakryt_sessiyu.py`: не тянуть лишний
    # модуль в каждый вызов git_zona.py, только когда реально дошли до doctor.
    try:
        import check_incidenty
        inc_text = (REPO / check_incidenty.INCIDENTY_REL).read_text(encoding="utf-8")
        verd_text = (REPO / check_incidenty.VERDIKTY_REL).read_text(encoding="utf-8")
        print(f"\n{check_incidenty.status_line(inc_text, verd_text)}")
    except (ImportError, OSError):
        pass  # doctor не обязан валиться из-за печати; гейт при закрытии сессии всё равно проверит

    print("\nПоследние коммиты:")
    for l in git("log", "-5", "--oneline").stdout.splitlines():
        print(f"   {l}")
    print("\nВетки:", ", ".join(
        b.strip().lstrip("* ") for b in git("branch").stdout.splitlines()))
    print("\n═══ конец. Непонятно — покажи этот вывод Claude целиком. ═══")
    return 0


# ─────────────────────────────── check ───────────────────────────────

def find_locks():
    """(локи, мусорные объекты) — то, что мешает записи или копится в .git.

    🔴 ДВА каталога, не один (часть A захода 2026-08-03): верхнеуровневые локи
    (`index.lock`, `HEAD.lock`) — ЛИЧНЫЕ (`git_dir()`), у каждой рабочей папки
    свои; `objects/**` — ОБЩИЙ склад (`git_common_dir()`), один на все worktree.
    В основной (не-worktree) папке они совпадают, разница не видна.
    """
    gd, gcd = git_dir(), git_common_dir()
    return (sorted(gd.glob("*.lock")) + sorted(gcd.glob("objects/*.lock")),
            sorted(gcd.glob("objects/*/tmp_obj_*")))


DEAD_LOCK_SEC = 300


def sweep_dead_locks(quiet=False):
    """Снять МЁРТВЫЕ локи (старше 5 мин). Свежие не трогать — там живой коммит.

    Почему это делает инструмент, а не человек командой из чата: команда
    `rm -f .git/*.lock` в zsh ПАДАЕТ целиком, если ни один файл не совпал
    (`no matches found`), и владелец остаётся и без уборки, и без диагноза.
    Цена 22.07: мёртвый `maintenance.lock` и 103 мусорных объекта пережили
    две выданные команды уборки — обе не выполнились.
    """
    locks, _ = find_locks()
    now, killed, alive = time.time(), [], []
    for p in locks:
        try:
            if now - p.stat().st_mtime < DEAD_LOCK_SEC:
                alive.append(p)
                continue
            p.unlink()
            killed.append(p)
        except OSError:
            alive.append(p)
    if killed and not quiet:
        print(f"🧹 Снято мёртвых локов: {len(killed)} "
              f"({', '.join(p.name for p in killed)}).")
    return killed, alive


def cmd_clean(args):
    if in_sandbox():
        return refuse_write("Уборка .git", suggest="clean")
    locks, junk = find_locks()
    if not locks and not junk:
        print("✅ В .git чисто: ни локов, ни мусорных объектов.")
        return 0

    killed, alive = sweep_dead_locks()
    if alive:
        print(f"⏳ Оставил {len(alive)} свежих лок(ов) — младше 5 мин, рядом может\n"
              "   идти живой коммит. Снимать их опасно: испортишь индекс.\n"
              "   Подожди и повтори `clean`.")
        for p in alive:
            # Полный путь, не `relative_to(REPO)` — см. find_locks().
            print(f"   {p}")

    removed = 0
    for p in junk:
        try:
            p.unlink()
            removed += 1
        except OSError:
            pass
    if removed:
        print(f"🧹 Убрано мусорных объектов (`tmp_obj_*`): {removed}.")

    locks2, junk2 = find_locks()
    if not locks2 and not junk2:
        print("✅ Готово: .git чист.")
        return 0
    if alive and not junk2:
        return 0
    print(f"⚠ Осталось: локов {len(locks2)}, мусора {len(junk2)}.")
    return 1


def cmd_check(args):
    rows = dirty(args.zone)
    where = f"зона {args.zone}" if args.zone else "всё дерево"
    if not rows:
        print(f"✅ {where}: работа доехала в git, вне git ничего нет.")
        return 0
    suspect = suspect_roots(rows)
    clean = [(c, p) for c, p in rows if not is_suspect(c, p)]
    new = [p for c, p in clean if c == "??"]
    mod = [p for c, p in clean if c != "??"]
    if clean:
        print(f"❌ {where}: вне git {len(clean)} путей "
              f"(рождено и никогда не ставилось — {len(new)}, "
              f"правлено и не закоммичено — {len(mod)}).\n")
        if new:
            print("Рождено и НИКОГДА не ставилось в git (умрёт от git clean и от смерти диска):")
            for p in new:
                print(f"  ?? {p}")
        if mod:
            print("\nПравлено и не закоммичено:")
            for p in mod:
                print(f"   M {p}")
        print("\n→ Это НЕ «сделано». `git_zona.py plan`, затем `git_zona.py commit`.")
    else:
        print(f"⚠ {where}: настоящей работы вне git нет — только подозрительный мусор (ниже).")
    print_suspect_block(suspect)
    return 1


# ─────────────────────────────── plan ───────────────────────────────

def cmd_plan(args):
    """Черновик плана ИЗ ТЕКУЩЕГО состояния дерева.

    Зачем командой, а не руками: дерево движется под руками. В сессии 21.07 план,
    набранный по снимку двадцатиминутной давности, устарел на 78 путей — рядом
    успели сделать `reset` и пересобрать коммит уже. План, набранный руками,
    врёт молча; сгенерированный — врать не успевает.
    """
    # 🔴 Не затирать работу человека молча. Если в черновике уже НЕТ
    # плейсхолдеров — значит сообщения переписаны руками, и пересборка их
    # уничтожит. Цена (22.07): владельцу велели `rm .commit-plan` перед `plan`,
    # черновик вернулся с плейсхолдером, гейт справедливо покраснел — и этот
    # шум был прочитан как «опять инструмент сломался», маскируя настоящий дефект.
    if PLAN.exists() and not args.force:
        txt = PLAN.read_text(encoding="utf-8")
        if "<что и зачем" not in txt and txt.strip():
            print(f"⛔ В {PLAN.relative_to(REPO)} уже вписаны сообщения — не затираю.\n"
                  "   Исполнить его:      python3 _generator/tools/git_zona.py commit\n"
                  "   Пересобрать заново: тот же plan с --force (сообщения пропадут)")
            return 1

    rows = dirty(args.zone)
    if not rows:
        print("✅ Дерево чисто — планировать нечего.")
        return 0
    # 🔴 Карантин: подозрительный untracked-мусор (имя с ведущим `-`) в черновик
    # НЕ входит — иначе его каждую коммит-сессию выцепляют из плана вручную
    # (23.07 папка-сирота `--help` чуть не уехала в гейт-коммит `_studio`).
    suspect = suspect_roots(rows)
    clean = [(c, p) for c, p in rows if not is_suspect(c, p)]
    if not clean:
        print("✅ Настоящей работы вне git нет — планировать нечего.")
        print_suspect_block(suspect)
        return 0
    groups = {}
    for _, path in clean:
        groups.setdefault(path.split("/")[0], []).append(path)

    lines = ["# ЧЕРНОВИК плана — собран `git_zona.py plan`.",
             "# Сообщения `==` переписать по-человечески: что и зачем.",
             "# Проверить, не попало ли сюда то, чему в git не место (мусор,",
             "# черновики, порождаемое) — такое идёт в .gitignore, а не в коммит.",
             ""]
    for top in sorted(groups):
        lines.append(f"== {top}: <что и зачем — переписать>")
        lines += sorted(groups[top])
        lines.append("")
    PLAN.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Черновик записан: {PLAN.relative_to(REPO)}\n"
          f"  групп: {len(groups)}, путей: {len(clean)}\n"
          "→ Переписать сообщения `==`, затем `git_zona.py commit`.")
    print_suspect_block(suspect)
    return 0


def parse_plan():
    """Формат нарочно тупой — строка есть строка, экранировать нечего.

        == teorkat-vvedenie: маткостяк — правки после приёмки
        teorkat-vvedenie/MAT-KOSTYAK.md

    Пути читаются построчно ⇒ пробелы и кириллица безопасны (в репо есть
    `kurs leto 2026/**` — на нём падал shell-вариант с `$(...)`).
    """
    if not PLAN.exists():
        sys.exit(f"❌ Плана нет: {PLAN.relative_to(REPO)}\n"
                 "   Собрать: `python3 _generator/tools/git_zona.py plan`")
    commits, cur = [], None
    for raw in PLAN.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("=="):
            cur = {"msg": line[2:].strip(), "paths": []}
            commits.append(cur)
        elif cur is None:
            sys.exit(f"❌ План начинается с пути, а не с `== сообщение`: {line}")
        else:
            cur["paths"].append(line)
    if not commits:
        sys.exit("❌ План пуст.")
    bad = [c["msg"] for c in commits if not c["paths"]]
    if bad:
        sys.exit("❌ В плане есть коммит без путей: " + "; ".join(bad))
    raw_msg = [c["msg"] for c in commits if "<что и зачем" in c["msg"]]
    if raw_msg:
        sys.exit("❌ В плане остались неотредактированные сообщения — "
                 f"их {len(raw_msg)}. Перепиши их, прежде чем коммитить.")
    return commits


# ─────────────────────────────── commit ───────────────────────────────

def cmd_untrack(args):
    """Снять с индекса то, что стало игнорируемым. Файлы на диске НЕ трогает.

    Заменяет shell-конструкцию `git ls-files -z … | xargs -0 git rm --cached`,
    которую владельцу приходилось вставлять руками. Та форма ломалась о zsh,
    о пути с пробелами и о разницу BSD/GNU xargs — здесь этого нет.
    """
    if in_sandbox():
        return refuse_write("untrack", suggest="untrack")
    out = git("ls-files", "-z", "-i", "-c", "--exclude-standard").stdout
    paths = [p for p in out.split("\0") if p]
    if not paths:
        print("✅ В индексе нет ничего, что попадало бы под .gitignore.")
        return 0

    by_top = {}
    for p in paths:
        by_top.setdefault(p.split("/")[0], []).append(p)
    print(f"Под .gitignore, но всё ещё в индексе: {len(paths)} путей.")
    for top in sorted(by_top):
        print(f"   {len(by_top[top]):>4}  {top}")
    print("\nФайлы останутся на диске — из git уходит только ссылка на них.")
    if not args.yes:
        print("→ Выполнить: тот же untrack с --yes")
        return 0

    if not wait_for_lock():
        return 2
    for i in range(0, len(paths), 200):          # пачками: длина командной строки
        r = git("rm", "--cached", "--quiet", "--", *paths[i:i + 200], check=False)
        if r.returncode != 0:
            print(f"❌ git rm упал (rc={r.returncode}):\n   "
                  + (r.stderr.strip().splitlines() or ["(пусто)"])[0])
            return 1
    left = [p for p in git("ls-files", "-z", "-i", "-c",
                           "--exclude-standard").stdout.split("\0") if p]
    print(f"✅ Снято с индекса: {len(paths) - len(left)}. "
          f"Осталось под правилом: {len(left)}.")
    print("→ Теперь закоммитить: plan → commit (удаления попадут в коммит).")
    return 0


def execute_commits(commits, push=False, delete_plan=False, no_verify=False):
    """Общее ядро ОБОИХ путей коммита — планового (`commit`) и однокомандного
    (`commit --zone -m`).

    Ядро одно НАРОЧНО: инварианты (форма `add` + pathspec, ожидание чужого
    лока, сверка результата по живым файлам) живут в одном месте, и «сгладить
    обёртку», молча ослабив ядро, невозможно — ядро у троп общее.
    """
    # Мёртвый лок снимаем САМИ — это самая частая причина «не коммитится»,
    # и раньше она требовала отдельной команды владельцу, которая падала в zsh.
    sweep_dead_locks()
    if not wait_for_lock():
        log_incident("чужой лок держится дольше 90 с",
                     "подождать и повторить ту же команду; лок руками не удалять")
        return 2

    # 🔴 --no-verify: обойти хук МОЖНО, но НЕ МОЛЧА (ISTOCHNIK-PRAVDY §3).
    # ЦЕНА (урок 9): гейт судит только пути коммита, но фикстуры и общие гейты
    # краснеют на ЧУЖОМ долге — и тогда собственная чистая зона не коммитится
    # вовсе. Голого `git commit --no-verify` в этом репо нет (весь git идёт
    # через этот инструмент), значит без флага здесь работа встаёт совсем.
    # Правило «красное на чужой зоне — в отчёт долгом, а не правкой»
    # (ISTOCHNIK-PRAVDY §4.5) держится тем, что обход САМ пишется в INCIDENTY:
    # запись, которую забудут сделать руками, инструмент делает за них.
    if no_verify:
        print(f"⚠ --no-verify: pre-commit ОБОЙДЁН. Причина: {no_verify}\n"
              "   Это законно только когда красное — ЧУЖОЕ (фикстура/гейт чужой зоны).\n"
              "   Своя красная зона чинится, а не обходится. Обход записан в\n"
              "   INCIDENTY.md — назвать его долгом в отчёте захода.")
        log_incident(f"коммит с --no-verify: {no_verify}",
                     "назвать причину долгом в отчёте захода; своё красное — чинить")

    done, failed = [], []
    for c in commits:
        if not wait_for_lock():
            print(f"⛔ Остановился перед: {c['msg']}")
            failed.append(c["msg"])
            break
        if not git("status", "--porcelain", "--", *c["paths"]).stdout.strip():
            print(f"⏭  нечего коммитить: {c['msg']}")
            continue
        # 🔴 ДВА ХОДА, и оба обязательны — по одному на каждую беду 21.07.
        # Не «упрощать»: убрав любой из них, воспроизведёшь оплаченную поломку.
        #
        #  · `add -- <пути>` — потому что pathspec в commit знает ТОЛЬКО
        #    ОТСЛЕЖИВАЕМЫЕ пути. Для нового файла `git commit -- <путь>` падает с
        #    «did not match any file(s) known to git». Цена: убрали `add`, считая
        #    pathspec самодостаточным, — завалились все 10 коммитов плана, новых
        #    путей в нём было около трёх четвертей.
        #
        #  · `-- <пути>` в самом commit — потому что `git commit -m` без путей
        #    забирает индекс ЦЕЛИКОМ, вместе с чужим. Цена: коммит из 89 файлов
        #    вместо трёх; план из 10 осмысленных коммитов схлопнулся в один свальный.
        #    ⚠ Грязнит индекс НЕ авто-коммит (его в репо нет — единственный хук
        #    .githooks/pre-commit ничего не стейджит), а живые писатели рядом:
        #    владелец, Cowork, Claude Code. Окно гонки тут ни при чём — чужое
        #    просто лежит в общем индексе, и pathspec его отсекает.
        #
        # ОБЕ половины держит фикстура (мутационно проверена, не на слово):
        #   sh _generator/tools/fixtures/git_zona/PROGNAT.sh
        # В pre-commit она поднимается при любой правке этого файла.
        r = git("add", "--", *c["paths"], check=False)
        if r.returncode != 0:
            print(f"❌ add упал (rc={r.returncode}): {c['msg']}\n   "
                  + (r.stderr.strip().splitlines() or ["(stderr пуст)"])[0])
            failed.append(c["msg"])
            continue
        # Флаг встраивается ЗДЕСЬ, в общем ядре, а не в обёртках: тропы `commit`
        # и `commit --zone -m` обязаны вести себя одинаково (см. докстроку).
        nv = ["--no-verify"] if no_verify else []
        r = git("commit", *nv, "-m", c["msg"], "--", *c["paths"], check=False)
        if r.returncode != 0:
            # Показываем ПРИЧИНУ, а не первую попавшуюся строку.
            # Цена: 21.07 коммит уронил pre-commit-хук, а печаталась первая
            # строка его stdout — бодрое «→ гоню фикстуру». Настоящая ошибка
            # (красная фикстура) осталась невидимой, и владелец получил rc=1
            # без причины. Поэтому: сперва строки, похожие на ошибку, и только
            # если таких нет — хвост вывода целиком.
            out = (r.stderr.strip() + "\n" + r.stdout.strip()).strip().splitlines()
            marks = ("❌", "error", "fatal", "КРАСН", "rror:")
            hits = [l for l in out if any(m in l for m in marks)]
            shown = hits[:5] if hits else out[-5:] or ["(вывод пуст)"]
            print(f"❌ commit упал (rc={r.returncode}): {c['msg']}")
            for l in shown:
                print(f"   {l}")
            if not hits and len(out) > 5:
                print(f"   (показан хвост; всего строк вывода: {len(out)})")
            failed.append(c["msg"])
            continue
        print(f"✅ {git('log', '-1', '--format=%h').stdout.strip()}  {c['msg']}")
        done.append(c["msg"])

    # Хвост-верификатор: «команда прошла» ≠ «файлы в git». Сверяем по факту.
    # Без него обрыв посередине невидим — цена 17.07: коммита не было час.
    print("\n— проверка по живым файлам —")
    live = dirty()
    still = [p for c in commits for p in c["paths"]
             if any(path == p or path.startswith(p.rstrip("/") + "/") for _, path in live)]
    if still or failed:
        print(f"❌ НЕ доехало: {len(still)} путей, упавших коммитов: {len(failed)}.")
        for p in still[:30]:
            print(f"   {p}")
        if len(still) > 30:
            print(f"   … ещё {len(still) - 30}")
        print("\n→ Причину покажет `git_zona.py doctor`.")
        log_incident("коммит прошёл не целиком: пути не доехали или коммиты упали",
                     "смотреть вывод команды и `doctor`")
        return 1
    # 🔴 Успех печатается ДО уборки, и уборка не смеет убить процесс.
    # Цена (22.07): `PLAN.unlink()` без защиты бросил PermissionError уже ПОСЛЕ
    # успешного коммита `a512964` — человек увидел traceback под словом «✅» и
    # дважды сверял `git log`, чтобы понять, прошло или нет. Это ровно урок
    # «код возврата первым»: успех и сбой уборки выглядели одинаково.
    print(f"✅ Все пути в git. Коммитов сделано: {len(done)}.")
    if delete_plan:
        try:
            PLAN.unlink(missing_ok=True)
            print("   План исполнен и удалён.")
        except OSError as e:
            print(f"   ⚠ План исполнен, но файл плана не удалился ({e.strerror}).\n"
                  f"     Это НЕ влияет на коммит. Удалить вручную: rm {PLAN}")
    up = git("rev-parse", "--abbrev-ref", "@{upstream}", check=False)
    if up.returncode != 0:
        print("\n⚠ Ветка не отслеживает origin — всё это есть только на этой машине.")
        return 0
    ahead = git("rev-list", "--count", "@{upstream}..HEAD").stdout.strip()
    if ahead == "0":
        return 0
    if not push:
        print(f"\n⚠ {ahead} коммит(ов) есть только на этой машине. "
              "Вывезти: тот же commit с --push (или `git push`).")
        return 0
    # push отдельным шагом забывался, и работа оставалась на одном диске.
    print(f"\n→ push: вывожу {ahead} коммит(ов) на origin…")
    r = git("push", check=False)
    if r.returncode != 0:
        first = ((r.stderr.strip() + "\n" + r.stdout.strip()).strip().splitlines()
                 or ["(вывод пуст)"])[0]
        print(f"❌ push упал (rc={r.returncode}):\n   {first}")
        log_incident("push упал", "коммиты целы; повторить `commit --push` или `git push`")
        return 1
    print("✅ push прошёл — работа больше не только на этой машине.")
    return 0


def commit_zone_oneshot(args):
    """Однокомандная тропа: «сохрани вот эту зону с вот этим сообщением».

    Родилась из пяти живых срывов 2026-07-23 (kod_commit-ux.md §2): путь
    `plan` → правка сообщения в `.commit-plan` → `commit` рвался на каждом
    стыке, а 90% случаев — один связный кусок работы с одним сообщением.
    Здесь упрощена ОБЁРТКА, не ядро: те же `add` + pathspec, лок, сверка —
    через общий execute_commits().

    `.commit-plan` тропа НЕ читает и НЕ трогает: молча исполнить залежавшийся
    план — значит закоммитить устаревшее чужими словами; про оставшийся план
    она предупреждает после успеха.
    """
    msg = (args.message or "").strip()
    if not args.zone:
        print("⛔ `-m` коммитит ЗОНУ одной командой — рядом с ним нужен `--zone <путь>`.\n"
              "   Всё дерево одной командой не коммитится: в репозитории трое писателей,\n"
              "   и без зоны чужая работа уехала бы в твой коммит (инцидент 2026-07-11).\n"
              "   Пакет РАЗНЫХ коммитов — через план: `plan`, затем `commit`.")
        log_incident("commit -m без --zone", "добавить --zone <путь зоны>")
        return 1
    if (not msg) or (msg.startswith("<") and msg.endswith(">")) \
            or "<что и зачем" in msg or "<сообщение" in msg:
        print("⛔ Сообщение коммита пустое или осталось плейсхолдером — впиши,\n"
              "   ЧТО сделано и ЗАЧЕМ, в кавычках после -m. Образец:\n"
              f"   commit --zone {args.zone} -m \"моя-зона: починен X, чтобы Y\" --push")
        log_incident("commit -m: сообщение пустое или плейсхолдер",
                     "вписать в -m живое «что и зачем»")
        return 1
    rows = dirty(args.zone)
    if not rows:
        last = git("log", "-1", "--format=%h %s").stdout.strip()
        print(f"✅ Зона `{args.zone}` чиста — коммитить нечего.\n"
              f"   Последний коммит: {last}")
        return 0
    print(f"Зона `{args.zone}`: вне git {len(rows)} путей — коммичу одним коммитом.")
    # 🔴 ЧТО ОСТАЁТСЯ ЗА БОРТОМ — НАЗВАТЬ ВСЛУХ, но не запрещать.
    # Ровно это стоило проекту разъехавшихся веток: команды коммита называли зону
    # арки, а работа писалась ещё и в картотеку — и месяц жила в одной ветке,
    # пока другая писала своё. Зона отсекала молча, и «закоммичено» читалось как
    # «сохранено всё». Узкий коммит бывает законным (рядом чужой заход), поэтому
    # здесь ПРЕДУПРЕЖДЕНИЕ, а не отказ: решение остаётся за человеком, но
    # принимается со списком перед глазами, а не вслепую.
    снаружи = sorted({p for _, p in dirty() if not in_zone(p, args.zone)})
    if снаружи:
        print(f"\n⚠ ВНЕ зоны `{args.zone}` изменено ещё {len(снаружи)} путей — "
              "они в ЭТОТ коммит НЕ уедут:")
        for p in снаружи[:20]:
            print(f"   {p}")
        if len(снаружи) > 20:
            print(f"   … ещё {len(снаружи) - 20}")
        print("   Это норма, если рядом работает кто-то ещё. Если это ТВОЯ работа —\n"
              "   назови её вторым коммитом со своей зоной, иначе она останется вне git.\n")
    rc = execute_commits([{"msg": msg, "paths": [p for _, p in rows]}], push=args.push,
                         no_verify=getattr(args, "no_verify", None))
    if rc == 0 and PLAN.exists():
        print("\n⚠ Лежит черновик _studio/.commit-plan — эта команда его НЕ исполняла.\n"
              "   Устарел → пересобрать `plan --force`; актуален → исполнить `commit` без -m.")
    # 🔴 ФИНАЛЬНАЯ СТРОКА-ВЕРДИКТ — всегда ПОСЛЕДНЯЯ, чтобы владелец читал только её.
    # Всё выше (⚠, списки «вне зоны») — контекст; решение «дальше или к Claude» — здесь.
    # Родилось из вопроса владельца 28.07: жёлтый ⚠ на успехе читался как «что-то не так».
    if rc == 0:
        print("\n✅ ГОТОВО — сохранено и вывезено. Дальше без Claude; вернись, только если увидишь 🔴.")
    else:
        print("\n🔴 ВЕРНИСЬ К CLAUDE — что-то не доехало; пришли ему вывод выше.")
    return rc


def cmd_commit(args):
    # 🔴 --no-verify без ПРИЧИНЫ не бывает (урок 9 арки 2026-07-25_lekcia-1).
    # Флаг заведён ровно затем, чтобы обход чужого красного был ВИДИМЫМ; обход
    # без названной причины видимым не является — в INCIDENTY попала бы строка,
    # по которой через неделю не восстановить, чей долг обходили и закрыт ли он.
    # Отказ человеческим языком, а не питоновый usage (§0в канона).
    if getattr(args, "no_verify", None) == "":
        print("⛔ `--no-verify` требует ПРИЧИНУ строкой сразу за флагом — обход,\n"
              "   у которого не названо, что именно обходят, ничем не отличается\n"
              "   от тихого. Образец:\n"
              "     commit --zone <зона> --no-verify \"чужой долг: 51 мёртвая секция рамы\" \\\n"
              "            -m \"<что и зачем>\" --push")
        log_incident("--no-verify без причины", "назвать причину строкой сразу за флагом")
        return 1

    # 🔴 ПЕРВЫМ ходом, до любой работы: писать из песочницы нельзя (см. refuse_write).
    # Раньше запрет жил только словами в каноне — и был нарушён: три отказа за
    # сессию 22.07, репозиторий дважды вставал на полчаса для всех писателей.
    # Правило, которое можно нарушить молча, будет нарушено (KONSTITUCIYA §11).
    # Пустой или плейсхолдерный -m ЗДЕСЬ законен: Cowork из песочницы готовит
    # команду (получая отказ с готовой строкой для владельца), а жмёт владелец.
    if in_sandbox():
        # Флаг обхода обязан попасть в ПРЕДЛОЖЕННУЮ владельцу строку: он её
        # копирует целиком, и потерянный здесь флаг вернёт ему тот же красный
        # хук, из-за которого команда и собиралась.
        nv = (f" --no-verify {shlex.quote(args.no_verify)}"
              if getattr(args, "no_verify", None) else "")
        if args.message is not None:
            m = args.message.strip() or "<что и зачем>"
            sug = f"commit --zone {args.zone or '<зона>'} -m {shlex.quote(m)} --push{nv}"
        else:
            sug = f"commit --push{nv}"
        log_incident("песочница: запись в .git запрещена",
                     "команду исполняет владелец в своём терминале")
        return refuse_write("Коммит", suggest=sug)

    # Однокомандная тропа: сообщение прямо в команде, план не нужен.
    if args.message is not None:
        return commit_zone_oneshot(args)

    # 🔴 «Плана нет» — НЕ всегда беда. `commit` сам удаляет план после успеха,
    # поэтому повторный запуск попадал на пугающее ❌ и читался как «коммит не
    # сработал» — при том что он прошёл минуту назад.
    # ЦЕНА (23.07): владелец решил, что коммит арки провалился; на деле он был
    # сделан (`0b17189`). Сообщение обязано различать «плана не написали» и
    # «план уже исполнен».
    if not PLAN.exists():
        last = git("log", "-1", "--format=%h %s").stdout.strip()
        rows = dirty()
        if not rows:
            print("✅ Плана нет — и коммитить нечего: всё доехало в git.\n"
                  f"   Последний коммит: {last}")
            return 0
        # 🔴 ПОРЯДОК СТРОК — НЕ КОСМЕТИКА. Урок 8 чинил этот же испуг, но только
        # для ЧИСТОГО дерева; при грязном сообщение начиналось с «Плана нет»
        # и снова читалось как «коммит провалился» — при том что он прошёл
        # секунду назад. ЦЕНА (28.07): владелец второй раз решил, что коммита
        # нет, и написал об этом. Поэтому первой строкой — что УЖЕ сделано,
        # и только потом что осталось.
        print(f"✅ Последний коммит на месте: {last}\n"
              f"   Плана нет — исполнять нечего. Это НЕ ошибка: `commit` сам удаляет\n"
              f"   план после успеха, так что повторный запуск и должен так отвечать.\n\n"
              f"⚠ Отдельно: в дереве ещё {len(rows)} путей вне git.\n"
              "   Твоя работа — одной командой:\n"
              "     `commit --zone <зона> -m \"что и зачем\" --push`, либо `plan` → `commit`.\n"
              "   Чужая зона (Claude Code, другая сессия) — так и надо, не трогай.")
        log_incident("commit без плана при грязном дереве",
                     "одной командой commit --zone -m, либо plan → commit")
        return 1

    try:
        commits = parse_plan()
    except SystemExit:
        # parse_plan сам печатает причину (нет путей / заглушки `==` / битый формат)
        log_incident("план не готов или битый (см. вывод команды)",
                     "поправить _studio/.commit-plan или пересобрать plan --force")
        raise

    # Зона — МЕХАНИЗМ, а не просьба: чужое физически не уедет в твой коммит.
    if args.zone:
        outside = [p for c in commits for p in c["paths"] if not in_zone(p, args.zone)]
        if outside:
            print(f"⛔ План выходит за зону `{args.zone}` — не коммичу НИЧЕГО.\n"
                  "   Это защита от инцидента 2026-07-11, когда авто-коммит одного\n"
                  "   захода утащил файлы другого в свой коммит под своим именем.\n"
                  "   Лишние пути:")
            for p in outside[:20]:
                print(f"     {p}")
            if len(outside) > 20:
                print(f"     … ещё {len(outside) - 20}")
            log_incident(f"план выходит за зону {args.zone}",
                         "пересобрать план по зоне: plan --zone, или чужое не трогать")
            return 1

    missing = [p for c in commits for p in c["paths"] if not (REPO / p).exists()]
    if missing:
        print("❌ План называет пути, которых нет на диске — ничего не коммичу:")
        for p in missing:
            print(f"   {p}")
        print("→ Дерево изменилось после сборки плана. Пересобрать: `git_zona.py plan`.")
        log_incident("план называет пути, которых нет на диске",
                     "пересобрать план из живого дерева: plan --force")
        return 1

    print(f"План: {len(commits)} коммит(ов).\n")
    return execute_commits(commits, push=args.push, delete_plan=True,
                           no_verify=getattr(args, "no_verify", None))


# ─────────────────────────────── worktree ───────────────────────────────
#
# ЗАЧЕМ. У репозитория ОДНА рабочая папка на все ветки. Поэтому канонное
# «параллельным заходам — РАЗНЫЕ ветки» в ней НЕ спасение, а самая опасная из
# возможностей: пока заход A работает на своей ветке, `git checkout` захода B
# подменяет файлы под ногами A — правки либо блокируют переключение, либо
# уезжают в чужую ветку. Проверено 21.07: `worktree list` даёт один вход,
# в reflog переключения между ветками заходов есть.
#
# Worktree даёт каждому заходу СВОЮ рабочую папку, СВОЙ индекс и СВОЙ HEAD при
# общем хранилище объектов. Отсюда: чужое в твой коммит не попадает физически
# (индексы разные), checkout соседа тебя не задевает (папки разные).
# ⚠ Что worktree НЕ чинит: ссылки и упаковка объектов остаются общими, поэтому
# короткие блокировки при одновременном коммите сохраняются — их держит ретрай
# с отступом (`wait_for_lock`). Два механизма дополняют друг друга.

WT_HOME = REPO.parent / f"{REPO.name}-wt"


def cmd_worktree(args):
    if args.action == "list":
        print(git("worktree", "list").stdout.rstrip())
        return 0
    # add/drop пишут в .git (заводят/убирают служебные файлы) — тот же запрет.
    if in_sandbox():
        rest = f"worktree {args.action} {args.name or '<имя>'}"
        rest += f" --branch {args.branch}" if args.branch else ""
        return refuse_write(f"worktree {args.action}", suggest=rest)

    if args.action == "add":
        if not args.name:
            sys.exit("❌ Нужно имя: `git_zona.py worktree add <имя> [--branch <ветка>]`")
        path = WT_HOME / args.name
        if path.exists():
            print(f"⚠ Уже есть: {path}\n   Работай в ней или сними: "
                  f"`git_zona.py worktree drop {args.name}`")
            return 1
        branch = args.branch or f"zahod/{args.name}"
        exists = git("rev-parse", "--verify", "--quiet", f"refs/heads/{branch}",
                     check=False).returncode == 0
        WT_HOME.mkdir(parents=True, exist_ok=True)
        cmd = (["worktree", "add", str(path), branch] if exists
               else ["worktree", "add", "-b", branch, str(path)])
        r = git(*cmd, check=False)
        if r.returncode != 0:
            print(f"❌ Не завелась (rc={r.returncode}):\n{r.stderr.strip()}")
            return 1
        print(f"✅ Рабочая папка захода готова.\n"
              f"   Папка:  {path}\n"
              f"   Ветка:  {branch} ({'существующая' if exists else 'новая'})\n\n"
              f"В заход впиши ПЕРВЫМ ходом (вместо `git checkout`):\n"
              f"   cd {path}\n"
              f"Ветку НЕ переключать: она у этой папки своя и уже стоит.\n"
              f"Закончив — коммит своей зоны там же, потом:\n"
              f"   python3 {REPO}/_generator/tools/git_zona.py worktree drop {args.name}")
        return 0

    if args.action == "drop":
        if not args.name:
            sys.exit("❌ Нужно имя: `git_zona.py worktree drop <имя>`")
        path = WT_HOME / args.name
        if not path.exists():
            print(f"⚠ Нет такой папки: {path}")
            return 1
        # 🔴 Незакоммиченное — НЕ удаляем. Автоочистка worktree с незакоммиченной
        # работой — известный способ потерять её безвозвратно (тот же дефект
        # заведён у claude-code как issue #55724). Лучше оставить папку висеть.
        st = subprocess.run(["git", "--no-optional-locks", "-C", str(path),
                             "status", "--porcelain", "--untracked-files=all"],
                            capture_output=True, text=True).stdout.strip()
        if st and not args.force:
            n = len(st.splitlines())
            print(f"⛔ В папке {n} путей вне git — НЕ удаляю, работа дороже порядка.\n"
                  f"   Посмотреть: python3 {Path(__file__)} check   (запусти из {path})\n"
                  f"   Точно мусор — повтори с --force.")
            return 1
        r = git("worktree", "remove", *(["--force"] if args.force else []),
                str(path), check=False)
        if r.returncode != 0:
            print(f"❌ Не снялась:\n{r.stderr.strip()}")
            return 1
        print(f"✅ Снята: {path}\n   Ветка осталась — её работа никуда не делась.")
        return 0


def cmd_adopt(args):
    """Перенести зону с ДРУГОЙ ветки на ТЕКУЩУЮ рабочую ветку (`git checkout <ветка> -- <зона>`).

    Случай: заход отработал в worktree на своей ветке, зона там закоммичена, а в
    основной папке осталась УСТАРЕВШАЯ untracked-копия (тень). adopt заменяет тень
    содержимым ветки и ставит его в индекс — дальше `commit --zone`. Ничего не теряет:
    хорошая версия на ветке цела, тень и так вне git. Родился из урока 2026-07-23
    (worktree-заход оставил двойную копию зоны — `RUKOVODSTVO §Заход`).
    """
    branch, zone = args.branch, args.zone
    if git("rev-parse", "--verify", "--quiet", f"refs/heads/{branch}", check=False).returncode != 0:
        sys.exit(f"❌ Ветки нет: {branch}")
    diff = git("diff", "--stat", f"HEAD..{branch}", "--", zone, check=False)
    print(f"═══ adopt: зону `{zone}` берём с ветки `{branch}` на текущую ═══\n")
    print(diff.stdout.rstrip() or "(различий по зоне между ветками нет — брать нечего)")

    # 🔴 ЧТО ОСТАЁТСЯ НА ВЕТКЕ — НАЗВАТЬ ВСЛУХ. adopt берёт РОВНО названную зону,
    # и это его правильное поведение; беда в том, что «зону перенёс» читается как
    # «работу перенёс». ЦЕНА (урок 20 арки 2026-07-30): перенос по путям привёз
    # документацию без кода — четыре гейта и хук месяц числились существующими,
    # потому что их описание доехало, а реализация осталась на ветке, и НИЧТО не
    # покраснело: гейт «работа доехала в git» смотрит рабочее дерево, а файлы там
    # на месте — просто версия чужая и старее.
    # Печать, а не отказ: узкий adopt законен (соседний заход ещё пишет своё).
    ostalos = sorted(p for p in diff_status("HEAD", f"refs/heads/{branch}")
                     if not in_zone(p, zone))
    if ostalos:
        zony = {}
        for p in ostalos:
            zony[zone_of(p)] = zony.get(zone_of(p), 0) + 1
        print(f"\n⚠ ВНЕ зоны `{zone}` ветка `{branch}` расходится ещё в "
              f"{len(ostalos)} путях — они НЕ приедут:")
        for z, c in sorted(zony.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"   {c:>4}  {z}")
        print("   Это норма, если чужое. Если это ТА ЖЕ работа (напр. описание "
              "здесь,\n   а реализация там) — вторым ходом adopt по той зоне, "
              "либо merge целиком.")
    if not args.yes:
        print("\n→ Это ПРЕДПРОСМОТР. Выполнить: повтори с `--yes`\n"
              "  (рабочая копия зоны заменится версией ветки и встанет в индекс; дальше `commit --zone`).")
        return 0
    if in_sandbox():
        return refuse_write(f"adopt {branch} -- {zone}",
                            suggest=f"adopt --branch {branch} --zone {zone} --yes")
    r = git("checkout", branch, "--", zone, check=False)
    if r.returncode != 0:
        print(f"❌ Не вышло (rc={r.returncode}):\n{r.stderr.strip()}")
        return 1
    print(f"✅ Зона `{zone}` взята с `{branch}` и поставлена в индекс.\n"
          f"   Дальше: python3 _generator/tools/git_zona.py commit --zone {zone}")
    return 0


def cmd_merge(args):
    """Влить ветку в ТЕКУЩУЮ — единственная законная дверь к слиянию.

    ЗАЧЕМ ПОДКОМАНДА. Канон (`GIT-disciplina §0`) запрещает выдавать владельцу
    голый shell, а слияния в инструменте не было — и ровно поэтому ветка
    `arka/konsolidacia-l1` месяц не была влита («у `git_zona.py` нет команды
    слияния — долг инструмента», корневой `CLAUDE.md`). Цена долга измерена:
    две ветки писали картотеку независимо и разошлись на 25 карточек, пять пар
    описывали одно и то же разными словами.

    🔴 ЧИСТОТА ДЕРЕВА — УСЛОВИЕ ТОЧНОЕ, А НЕ ГРУБОЕ. «Требуем чистое дерево»
    звучит строже, но в этом репозитории оно недостижимо: рядом всегда пишет
    кто-то третий (владелец, Cowork, соседний заход), и грубое условие сделало бы
    команду неисполнимой — то есть вернуло бы всех к голому `git merge`, от
    которого мы и уходим. Опасно НЕ «что-то грязное в дереве», а ровно одно:
    грязный путь, который слияние собирается переписать. Его и проверяем; про
    остальную грязь ГРОМКО предупреждаем и называем поимённо — она в слияние не
    участвует и в merge-коммит не поедет (индекс не трогаем).

    `--zone` (можно повторять) — тот же механизм, что у `commit --zone`: если
    ветка тащит пути ВНЕ названных зон, не сливаем ничего. Заход работает в своей
    зоне и не должен молча привезти чужую.

    Конфликт НЕ разрешаем сами: печатаем конфликтные пути и останавливаемся —
    разрешение смысловое, его делает человек или исполнитель захода. Дальше
    `merge --continue` (завершить) или `merge --abort` (откатить целиком).
    """
    # --abort / --continue: хвосты незаконченного слияния. Обе пишут в .git.
    if args.abort or args.cont:
        if in_sandbox():
            return refuse_write("merge --abort/--continue",
                                suggest=f"merge {args.branch or ''} "
                                        f"{'--abort' if args.abort else '--continue'}".strip())
        if not (git_dir() / "MERGE_HEAD").exists():
            print("⚠ Незаконченного слияния нет — отменять/продолжать нечего.\n"
                  "   Что с репо сейчас: `git_zona.py doctor`")
            return 1
        if args.abort:
            r = git("merge", "--abort", check=False)
            if r.returncode != 0:
                print(f"❌ merge --abort упал (rc={r.returncode}):\n   {r.stderr.strip()}")
                return 1
            print("✅ Слияние отменено, дерево вернулось к состоянию до него.")
            return 0
        unmerged = [l for l in git("diff", "--name-only", "--diff-filter=U").stdout.splitlines() if l]
        if unmerged:
            print(f"⛔ Ещё {len(unmerged)} путей с неразрешённым конфликтом — не завершаю:")
            for p in unmerged:
                print(f"   {p}")
            print("   Разреши их и повтори `merge --continue`.")
            return 1
        if not wait_for_lock():
            return 2
        r = git("commit", "--no-edit", check=False)
        if r.returncode != 0:
            out = (r.stderr.strip() + "\n" + r.stdout.strip()).strip().splitlines()
            print(f"❌ merge-коммит упал (rc={r.returncode}):")
            for l in (out[-5:] or ["(вывод пуст)"]):
                print(f"   {l}")
            log_incident("merge --continue: коммит слияния не прошёл",
                         "смотреть вывод хука и `doctor`")
            return 1
        print(f"✅ Слияние завершено: {git('log', '-1', '--oneline').stdout.strip()}")
        return 0

    if not args.branch:
        sys.exit("❌ Нужна ветка: `git_zona.py merge <ветка> [--zone <путь>]`")
    branch = args.branch
    if git("rev-parse", "--verify", "--quiet", f"refs/heads/{branch}",
           check=False).returncode != 0:
        sys.exit(f"❌ Ветки нет: {branch}")

    head = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if head == branch:
        sys.exit(f"❌ `{branch}` — это и есть текущая ветка. Сливать нечего.")
    if (git_dir() / "MERGE_HEAD").exists():
        print("⛔ В репозитории уже идёт незаконченное слияние — второе не начинаю.\n"
              "   Завершить: `git_zona.py merge --continue` · отменить: `merge --abort`")
        return 1

    base = git("merge-base", "HEAD", branch).stdout.strip()
    commits = [l for l in git("log", "--oneline", f"HEAD..{branch}").stdout.splitlines() if l]
    touched = [l for l in git("diff", "--name-only", f"HEAD...{branch}").stdout.splitlines() if l]

    print(f"═══ merge: `{branch}` → `{head}` ═══\n")
    if not commits:
        print(f"✅ Всё, что есть в `{branch}`, уже в `{head}` — сливать нечего.")
        return 0
    print(f"База слияния: {base[:7]}  ({git('log', '-1', '--format=%s', base).stdout.strip()})")
    print(f"\nПриедет коммитов: {len(commits)}")
    for l in commits:
        print(f"   {l}")
    print(f"\nЗатронет путей: {len(touched)}")
    for p in touched:
        print(f"   {p}")

    # Зона — механизм, а не просьба (та же защита, что в cmd_commit).
    if args.zone:
        outside = [p for p in touched if not any(in_zone(p, z) for z in args.zone)]
        if outside:
            print(f"\n⛔ Слияние выходит за зон{'ы' if len(args.zone) > 1 else 'у'} "
                  f"({', '.join(args.zone)}) — не сливаю НИЧЕГО.")
            for p in outside[:20]:
                print(f"     {p}")
            if len(outside) > 20:
                print(f"     … ещё {len(outside) - 20}")
            log_incident(f"merge {branch} выходит за зону",
                         "назвать все зоны через повторный --zone либо сливать без --zone осознанно")
            return 1

    # 🔴 Пересечение грязного с тем, что слияние перепишет, — единственный
    # настоящий блокер: git такие правки затрёт или встанет на середине.
    dirty_rows = dirty()
    collision = sorted({p for _, p in dirty_rows if p in touched})
    other = sorted({p for _, p in dirty_rows if p not in touched})
    if collision:
        print(f"\n⛔ {len(collision)} путей ОДНОВРЕМЕННО грязные и участвуют в слиянии — "
              "не сливаю:")
        for p in collision:
            print(f"   {p}")
        print("   Сперва закоммить их (`commit --zone <зона> -m …`) или откати — "
              "иначе слияние их затрёт.")
        log_incident(f"merge {branch}: грязные пути пересекаются со сливаемыми",
                     "закоммитить или откатить эти пути и повторить merge")
        return 1
    if other:
        print(f"\n⚠ Вне слияния грязных путей: {len(other)}. Они в merge-коммит НЕ поедут "
              "(индекс не трогаю), но и не защищены:")
        for p in other[:20]:
            print(f"   {p}")
        if len(other) > 20:
            print(f"   … ещё {len(other) - 20}")

    sweep_dead_locks()
    if not wait_for_lock():
        log_incident("merge: чужой лок держится дольше 90 с",
                     "подождать и повторить ту же команду")
        return 2

    r = git("merge", "--no-edit", branch, check=False)
    if r.returncode == 0:
        print(f"\n✅ Влито без конфликтов: {git('log', '-1', '--oneline').stdout.strip()}")
        return 0

    conflicts = [l for l in git("diff", "--name-only", "--diff-filter=U").stdout.splitlines() if l]
    if not conflicts:
        # не конфликт, а отказ самого git — показываем причину, а не первую строку
        out = (r.stderr.strip() + "\n" + r.stdout.strip()).strip().splitlines()
        print(f"\n❌ merge не прошёл (rc={r.returncode}):")
        for l in (out[:5] or ["(вывод пуст)"]):
            print(f"   {l}")
        log_incident(f"merge {branch} не прошёл", "смотреть вывод команды и `doctor`")
        return 1
    print(f"\n🔴 КОНФЛИКТ в {len(conflicts)} путях — слияние ОСТАНОВЛЕНО, "
          "сама не разрешаю (это смысловое решение):")
    for p in conflicts:
        print(f"   {p}")
    print("\n   Разрешает человек или исполнитель захода. Дальше:\n"
          "     завершить — `git_zona.py merge --continue`\n"
          "     откатить целиком — `git_zona.py merge --abort`")
    log_incident(f"merge {branch}: конфликт в {len(conflicts)} путях",
                 "разрешить конфликты, затем merge --continue (или merge --abort)")
    return 1


def cmd_purge(args):
    """Снять ПОДОЗРИТЕЛЬНЫЙ untracked-мусор (имя с ведущим `-`) без shell.

    Почему подкомандой, а не `rm`: имя `--help` начинается с `-`, любой `rm`
    примет его за флаг (нужен `rm -- --help`), а выдавать такое владельцу — ровно
    ловушка §0 канона (shell-в-чат ломается о zsh). Форма — как `untrack`/`adopt`:
    без `--yes` предпросмотр, с `--yes` снос; из песочницы отказ с готовой строкой
    владельцу; неуспех сам пишется в INCIDENTY (§0б). Удаление — Python
    (`shutil`/`pathlib`), не shell.

    🔴 ИНВАРИАНТ БЕЗОПАСНОСТИ: трогает ТОЛЬКО untracked. Отслеживаемое (в индексе
    или в HEAD) — это работа; удаление лоссово, ошибка здесь безвозвратна.
    Поэтому каждый путь проверяется git'ом (под ним нет отслеживаемого?) и на
    «внутри репо», а тронутое совпадает с названным РОВНО, ни файлом больше.

    Цели: явные пути-аргументы ИЛИ карантин-список `plan` (мусор с ведущим `-`).
    """
    if args.paths:
        targets = list(dict.fromkeys(args.paths))    # сохранить порядок, снять дубли
    else:
        targets = suspect_roots(dirty())
    if not targets:
        print("✅ Подозрительного мусора не найдено — снимать нечего.")
        return 0

    repo_root = REPO.resolve()
    safe, refused_tracked, refused_outside, missing = [], [], [], []
    for t in targets:
        full = REPO / t
        try:                                          # 1) внутри репо? (защита от `../…`)
            full.resolve().relative_to(repo_root)
        except ValueError:
            refused_outside.append(t)
            continue
        if not full.exists() and not full.is_symlink():   # 2) существует?
            missing.append(t)
            continue
        # 3) под путём есть хоть один ОТСЛЕЖИВАЕМЫЙ файл? тогда это работа — не трогаем
        if git("ls-files", "--", t, check=False).stdout.strip():
            refused_tracked.append(t)
            continue
        safe.append(t)

    for t in refused_outside:
        print(f"⛔ Вне репозитория — не трогаю: {t}")
    if refused_tracked:
        print("⛔ Пропущены — под ними есть ОТСЛЕЖИВАЕМЫЕ файлы (это работа, не мусор):")
        for t in refused_tracked:
            print(f"   {t}")
        print("   purge снимает только untracked. Отслеживаемое убирают осознанно (git rm).")
    if missing:
        print("⚠ Нет на диске (уже снято?):")
        for t in missing:
            print(f"   {t}")

    if not safe:
        print("✅ Снимать нечего: untracked-мусора среди целей нет.")
        return 1 if (refused_tracked or refused_outside) else 0

    print(f"\nЦели (untracked-мусор, {len(safe)}):")
    for t in safe:
        print(f"   {t}")
    if not args.yes:
        print("\n→ Это ПРЕДПРОСМОТР, ничего не удалено. Снести: повтори с `--yes`.")
        return 0

    # ── запись: сначала sandbox-отказ (как commit/untrack/adopt) ──
    if in_sandbox():
        if args.paths:
            # `--yes` ПЕРЕД `--`, пути ПОСЛЕ: после `--` всё считается путём,
            # иначе `--yes`/дефисное имя перепутаются с флагом (см. help подкоманды).
            sug = "purge --yes -- " + " ".join(shlex.quote(t) for t in args.paths)
        else:
            sug = "purge --yes"
        log_incident("песочница: снос untracked-мусора запрещён",
                     "purge исполняет владелец в своём терминале")
        return refuse_write("purge", suggest=sug)

    removed, failed = [], []
    for t in safe:
        full = REPO / t
        try:
            if full.is_dir() and not full.is_symlink():
                shutil.rmtree(full)
            else:
                full.unlink()
            removed.append(t)
        except OSError as e:
            failed.append((t, e))

    print(f"\n🧹 Снято: {len(removed)}.")
    for t in removed:
        print(f"   {t}")
    if failed:
        print(f"❌ Не удалось снять: {len(failed)}")
        for t, e in failed:
            print(f"   {t}: {e.strerror}")
        log_incident("purge не смог удалить часть мусора",
                     "проверить права на файлы и повторить purge, либо снять вручную")
        return 1
    return 0


def main():
    ap = argparse.ArgumentParser(description="Вся работа с git в materials/ — через этот файл.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("doctor", help="что с репо прямо сейчас (начинай отсюда)")
    d.set_defaults(func=cmd_doctor)

    po = sub.add_parser("poteri", help="что пропадёт при удалении ветки — файлами, read-only")
    po.add_argument("--branch", help="судить только эту ветку (без флага — все соседние)")
    po.set_defaults(func=cmd_poteri)

    zv = sub.add_parser("zakryt-vetku",
                        help="закрыть ветку безопасно: надгробие `mogila/<имя>`, "
                             "снос рабочей папки и ветки, строка воскрешения")
    zv.add_argument("--branch", help="имя ветки")
    zv.add_argument("--vse-zelenye", dest="vse_zelenye", action="store_true",
                    help="подмести ВСЕ ветки с зелёной метрикой одной командой")
    zv.add_argument("--vsyo-ravno", dest="vsyo_ravno", metavar="ПРИЧИНА",
                    help="закрыть, даже если метрика нашла потерю; ПРИЧИНА "
                         "обязательна и пишется в INCIDENTY. Грязную рабочую "
                         "папку НЕ перебивает — там потеря необратима")
    zv.set_defaults(func=cmd_zakryt_vetku)

    vs = sub.add_parser("voskresit", help="вернуть ветку из надгробия и снять надгробие")
    vs.add_argument("--branch", required=True,
                    help="имя ветки: закрытой (из её надгробия) либо новой — "
                         "когда поднимаешь осколок через --tag")
    vs.add_argument("--tag", help="полное имя надгробия-осколка "
                                  "(`mogila-oskolok/<ветка>/<хэш>`) — для коммитов, "
                                  "отвязанных reset/amend: своего имени ветки у них нет")
    vs.set_defaults(func=cmd_voskresit)

    mg2 = sub.add_parser("mogily", help="что похоронено: список надгробий (read-only)")
    mg2.set_defaults(func=cmd_mogily)

    c = sub.add_parser("check", help="что вне git (read-only, краснеет)")
    c.add_argument("--zone", help="проверять только этот префикс пути")
    c.set_defaults(func=cmd_check)

    p = sub.add_parser("plan", help="черновик плана из текущего дерева")
    p.add_argument("--zone", help="планировать только этот префикс пути")
    p.add_argument("--force", action="store_true",
                   help="перезаписать черновик, даже если сообщения уже вписаны")
    p.set_defaults(func=cmd_plan)

    k = sub.add_parser("commit",
                       help="закоммитить: с --zone и -m — одной командой; без -m — по плану")
    k.add_argument("--zone", help="коммитить только этот префикс пути (с -m); "
                                  "без -m — отказаться, если план выходит за него")
    k.add_argument("-m", "--message",
                   help="однокомандная тропа: закоммитить зону с этим сообщением, без плана")
    k.add_argument("--push", action="store_true", help="сразу вывезти на origin")
    # Значение ОБЯЗАТЕЛЬНО по букве урока 9: `--no-verify "чужой долг: …"`.
    # nargs="?", а не required-значение, — чтобы голый флаг ловился не питоновым
    # usage, а человеческим отказом с диагнозом (§0в канона).
    k.add_argument("--no-verify", nargs="?", const="", metavar="ПРИЧИНА",
                   help="обойти pre-commit, когда красное — ЧУЖОЕ; ПРИЧИНА обязательна "
                        "и пишется в INCIDENTY")
    k.set_defaults(func=cmd_commit)

    cl = sub.add_parser("clean", help="снять мёртвые локи и мусор из .git")
    cl.set_defaults(func=cmd_clean)

    u = sub.add_parser("untrack", help="снять с индекса то, что стало игнорируемым")
    u.add_argument("--yes", action="store_true", help="выполнить (без него — только показать)")
    u.set_defaults(func=cmd_untrack)

    w = sub.add_parser("worktree", help="отдельная рабочая папка на заход (параллельные заходы)")
    w.add_argument("action", choices=["add", "drop", "list"])
    w.add_argument("name", nargs="?", help="имя захода")
    w.add_argument("--branch", help="ветка (по умолчанию zahod/<имя>)")
    w.add_argument("--force", action="store_true", help="снять даже с незакоммиченным")
    w.set_defaults(func=cmd_worktree)

    a = sub.add_parser("adopt", help="перенести зону с другой ветки на текущую (заменить устаревшую тень)")
    a.add_argument("--branch", required=True, help="ветка-источник (где зона закоммичена)")
    a.add_argument("--zone", required=True, help="префикс зоны")
    a.add_argument("--yes", action="store_true", help="выполнить (без него — только предпросмотр)")
    a.set_defaults(func=cmd_adopt)

    mg = sub.add_parser("merge", help="влить ветку в текущую (конфликт — останавливается и показывает пути)")
    mg.add_argument("branch", nargs="?", help="ветка-источник")
    # --zone повторяемый: заход законно держит НЕСКОЛЬКО каталогов записи
    # (картотека + папка арки + инструменты), одним префиксом они не накрываются.
    mg.add_argument("--zone", action="append",
                    help="разрешённый префикс пути; можно повторять — слияние вне зон откажется")
    mg.add_argument("--abort", action="store_true", help="откатить незаконченное слияние целиком")
    mg.add_argument("--continue", dest="cont", action="store_true",
                    help="завершить слияние после разрешения конфликтов")
    mg.set_defaults(func=cmd_merge)

    pu = sub.add_parser("purge",
                        help="снять подозрительный untracked-мусор (имя с ведущим `-`); без --yes — предпросмотр")
    pu.add_argument("paths", nargs="*",
                    help="явные пути (только untracked); без них — карантин-список из plan. "
                         "Путь с ведущим дефисом — после `--`, а флаг `--yes` ПЕРЕД ним: "
                         "`purge --yes -- --help` (после `--` всё считается путём)")
    pu.add_argument("--yes", action="store_true", help="выполнить снос (без него — только показать)")
    pu.set_defaults(func=cmd_purge)

    # parse_known_args вместо parse_args: лишние аргументы — НЕ питоновый usage,
    # а человеческий диагноз. Цена (23.07): владелец скопировал команду с хвостом
    # `# предпросмотр`; его zsh без interactivecomments отдал `#` и слово дальше
    # в argv, argparse упал с «unrecognized arguments» — обе adopt-команды подряд.
    # «unrecognized arguments: #» не говорит человеку НИ что случилось, НИ что делать.
    args, extra = ap.parse_known_args()
    if extra:
        got = " ".join(extra)
        print(f"⛔ Не понял часть команды: {got}\n"
              "   Частая причина — хвост-«комментарий» в строке: zsh владельца передаёт\n"
              "   `# …` программе как аргументы. Убери из команды всё после последней\n"
              "   кавычки (или закавычь сообщение целиком) и повтори.\n"
              "   Ничего не сделано.")
        log_incident("запуск с мусорными аргументами",
                     f"лишнее в команде: {got[:60]} — убрать хвост и повторить")
        sys.exit(2)
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
