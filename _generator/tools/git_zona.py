#!/usr/bin/env python3
"""git_zona.py — вся работа с git в `materials/` идёт через этот файл.

ДЛЯ ВЛАДЕЛЬЦА — четыре команды, больше знать ничего не надо:

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
LOCK = REPO / ".git" / "index.lock"
LOCK_WAIT_SEC = 90


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


def git(*args, check=True):
    """Единственная дверь к git. --no-optional-locks не даёт чтению взять лок."""
    r = subprocess.run(
        ["git", "--no-optional-locks", *args],
        cwd=REPO, capture_output=True, text=True,
    )
    if check and r.returncode != 0:
        sys.exit(f"❌ git {' '.join(args)} упал:\n{r.stderr.strip()}")
    return r


def wait_for_lock(limit=LOCK_WAIT_SEC):
    """Ждём чужой коммит вместо того, чтобы падать.

    Почему ждём, а не сносим: правило канона «pgrep пуст ⇒ лок стейл ⇒ удалить»
    в песочнице ЛОЖНО — она видит только свои процессы и хостовый git ей не
    виден. Условие, на котором стоит разрешение удалить лок, тут непроверяемо.
    """
    if not LOCK.exists():
        return True
    print(f"⏳ .git/index.lock занят — рядом кто-то коммитит. Жду до {limit} с…")
    waited, step = 0, 2
    while waited < limit:
        time.sleep(step)
        waited += step
        if not LOCK.exists():
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

    # незаконченные операции — частая причина «ничего не коммитится»
    g = REPO / ".git"
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
    g = REPO / ".git"
    locks = sorted(g.glob("*.lock")) + sorted(g.glob("objects/*.lock"))
    junk = sorted(g.glob("objects/*/tmp_obj_*"))
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
            print(f"   {p.relative_to(REPO)}   ({age_of(p)})")
        print("   Свежий (секунды–минуты) — рядом РЕАЛЬНО идёт коммит: ЖДАТЬ, не трогать.\n"
              "   Старый — мёртвая мина от упавшего процесса.")
    else:
        print("\nЛоки в .git: ✅ свободно")

    # tmp_obj — НЕ блокер, просто мусор от прерванной записи. Тревогу не поднимаем.
    if junk:
        print(f"\nМусорные объекты (`tmp_obj_*`): {len(junk)} шт., "
              f"старейшему {age_of(junk[0])} — на работу не влияют, но копятся.")

    if locks or junk:
        print("   Уборка — в терминале ВЛАДЕЛЬЦА и только когда живого git нет:")
        print("     cd <корень репо> && rm -f .git/*.lock .git/objects/*.lock "
              "&& find .git/objects -name 'tmp_obj_*' -delete")

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
    print(f"\nВне git: {len(rows)} путей.")
    if rows:
        by_top = {}
        for code, p in rows:
            by_top.setdefault(p.split("/")[0], []).append(code)
        for top in sorted(by_top):
            cs = by_top[top]
            print(f"   {len(cs):>4}  {top}"
                  f"   (новых {sum(1 for c in cs if c == '??')}, "
                  f"правленых {sum(1 for c in cs if c != '??')})")
        print("\n→ `git_zona.py plan` соберёт черновик коммитов, дальше `commit`.")
    else:
        print("   ✅ всё доехало.")

    print("\nПоследние коммиты:")
    for l in git("log", "-5", "--oneline").stdout.splitlines():
        print(f"   {l}")
    print("\nВетки:", ", ".join(
        b.strip().lstrip("* ") for b in git("branch").stdout.splitlines()))
    print("\n═══ конец. Непонятно — покажи этот вывод Claude целиком. ═══")
    return 0


# ─────────────────────────────── check ───────────────────────────────

def find_locks():
    """(локи, мусорные объекты) — то, что мешает записи или копится в .git."""
    g = REPO / ".git"
    return (sorted(g.glob("*.lock")) + sorted(g.glob("objects/*.lock")),
            sorted(g.glob("objects/*/tmp_obj_*")))


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
            print(f"   {p.relative_to(REPO)}")

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
    new = [p for c, p in rows if c == "??"]
    mod = [p for c, p in rows if c != "??"]
    print(f"❌ {where}: вне git {len(rows)} путей "
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
    groups = {}
    for _, path in rows:
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
          f"  групп: {len(groups)}, путей: {len(rows)}\n"
          "→ Переписать сообщения `==`, затем `git_zona.py commit`.")
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


def cmd_commit(args):
    # 🔴 ПЕРВЫМ ходом, до любой работы: писать из песочницы нельзя (см. refuse_write).
    # Раньше запрет жил только словами в каноне — и был нарушён: три отказа за
    # сессию 22.07, репозиторий дважды вставал на полчаса для всех писателей.
    # Правило, которое можно нарушить молча, будет нарушено (KONSTITUCIYA §11).
    if in_sandbox():
        return refuse_write("Коммит")
    commits = parse_plan()

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
            return 1

    missing = [p for c in commits for p in c["paths"] if not (REPO / p).exists()]
    if missing:
        print("❌ План называет пути, которых нет на диске — ничего не коммичу:")
        for p in missing:
            print(f"   {p}")
        print("→ Дерево изменилось после сборки плана. Пересобрать: `git_zona.py plan`.")
        return 1

    # Мёртвый лок снимаем САМИ — это самая частая причина «не коммитится»,
    # и раньше она требовала отдельной команды владельцу, которая падала в zsh.
    sweep_dead_locks()
    if not wait_for_lock():
        return 2

    print(f"План: {len(commits)} коммит(ов).\n")
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
        r = git("commit", "-m", c["msg"], "--", *c["paths"], check=False)
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
        return 1
    # 🔴 Успех печатается ДО уборки, и уборка не смеет убить процесс.
    # Цена (22.07): `PLAN.unlink()` без защиты бросил PermissionError уже ПОСЛЕ
    # успешного коммита `a512964` — человек увидел traceback под словом «✅» и
    # дважды сверял `git log`, чтобы понять, прошло или нет. Это ровно урок
    # «код возврата первым»: успех и сбой уборки выглядели одинаково.
    print(f"✅ Все пути плана в git. Коммитов сделано: {len(done)}.")
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
    if not args.push:
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
        return 1
    print("✅ push прошёл — работа больше не только на этой машине.")
    return 0


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


def main():
    ap = argparse.ArgumentParser(description="Вся работа с git в materials/ — через этот файл.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("doctor", help="что с репо прямо сейчас (начинай отсюда)")
    d.set_defaults(func=cmd_doctor)

    c = sub.add_parser("check", help="что вне git (read-only, краснеет)")
    c.add_argument("--zone", help="проверять только этот префикс пути")
    c.set_defaults(func=cmd_check)

    p = sub.add_parser("plan", help="черновик плана из текущего дерева")
    p.add_argument("--zone", help="планировать только этот префикс пути")
    p.add_argument("--force", action="store_true",
                   help="перезаписать черновик, даже если сообщения уже вписаны")
    p.set_defaults(func=cmd_plan)

    k = sub.add_parser("commit", help="исполнить _studio/.commit-plan")
    k.add_argument("--zone", help="отказаться, если план выходит за этот префикс")
    k.add_argument("--push", action="store_true", help="сразу вывезти на origin")
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

    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
