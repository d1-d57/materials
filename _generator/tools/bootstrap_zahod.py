#!/usr/bin/env python3
"""Scaffold — генерит файл-заход `kod_<тема>.md` из `_studio/zhurnal/_TEMPLATE-zahod.md`
с ОБЯЗАТЕЛЬНЫМ контрактом зоны (ветка · зона · коммит · запрет).

Использование:
    python3 bootstrap_zahod.py <папка-арки> <тема> --branch <ветка> --zone "<пути>" \\
        [--opisanie "<что за заход>"] [--worktree <имя>] [--model Sonnet]

Пример (одиночный заход):
    python3 bootstrap_zahod.py _studio/zhurnal/2026-07-11_reserch-zadach zapusk \\
        --branch fibonacci-l1 --zone "graph-course/" --model Sonnet

Пример (ПАРАЛЛЕЛЬНЫЙ — так надо, когда рядом идёт другой заход):
    python3 bootstrap_zahod.py _studio/zhurnal/2026-07-21_mat-kostyak vychitano \\
        --branch zahod/vychitano --zone "teorkat-vvedenie/" --worktree vychitano

🔴 --worktree заводит заходу СВОЮ рабочую папку и вписывает `cd` вместо `git checkout`.
Без него все заходы делят ОДНУ рабочую папку, и checkout одного подменяет файлы под
ногами другого (у репозитория одна рабочая папка на все ветки — `git worktree list`).
Прежний совет «параллельным заходам — разные ветки» этой гонки не лечил, а назначал.
Забыл флаг в опасной обстановке — скрипт скажет об этом в конце, а не промолчит.

Зачем: заход НИКОГДА не пишется с нуля — Cowork вызывает этот скрипт, и контракт зоны
вшивается автоматически (RUKOVODSTVO §Зона изменений и git). --branch и --zone ОБЯЗАТЕЛЬНЫ:
без ветки и зоны заход не создаётся в принципе. Cowork дозаполняет `<...>` (контекст, задача,
критерий, что читать). Владелец руками ничего не вставляет.

🔴 ЗАХОД РОЖДАЕТСЯ УЖЕ ЗАРЕГИСТРИРОВАННЫМ в `_studio/docs/KARTA.md §6`.
Тем же ходом, без отдельной команды и без напоминания. Почему это делает
ИМЕННО генератор: его запускает аналитик, у которого `docs/` открыт, — значит
на этом ходу конфликта «зарегистрируй / не смей править docs» не существует
by construction. У исполнителя он существовал, и цена известна: из 56 срывов
коммита 28 — обходы `--no-verify`, 27 из них по этой одной причине (автолог
`_studio/zhurnal/_INFRA-git/INCIDENTY.md`). Файлам, рождающимся ВО ВРЕМЯ
захода, служит та же дверь напрямую — `register_doc.py`.

Идемпотентен: существующий kod-файл НЕ перезатирает. Только stdlib.
"""
import argparse
import subprocess
import sys
from pathlib import Path

# Регистрацию делает ОБЩЕЕ ЯДРО, а не своя копия вставки в §6: шаг «заход» и
# шаг «артефакт» обязаны писать в индекс одинаково, иначе строки разъедутся, и
# разъезд обнаружится только через неделю чужим красным хуком.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import register_doc  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]  # .../materials
TEMPLATE = REPO_ROOT / "_studio" / "zhurnal" / "_TEMPLATE-zahod.md"
GIT_ZONA = REPO_ROOT / "_generator" / "tools" / "git_zona.py"


def validate_slug(name, chto):
    """Кривой вход обязан ГРОМКО падать, а не тихо создать файл не с тем именем.

    Тот же класс, что закрыт в bootstrap_arka.py (инцидент 23.07 с `--help`):
    имя, которое станет путём на диске, не валидируется. Здесь `tema` → имя файла
    `kod_<tema>.md`; ведущий `-`, слэш, пустое, ведущая точка — не слаг. argparse
    отбивает опции-позиции сам, но НЕ пустое/со слэшем — их ловит эта проверка.
    Дублируется сознательно (общий модуль лёг бы вне зоны — см. kod_bootstrap-guard).
    """
    if name.startswith("-"):
        raise SystemExit(
            f"❌ «{name}» похоже на флаг, а не {chto}. Имя — слаг вида "
            "`2026-07-23_tema`, без ведущего дефиса.")
    if (not name) or any(c.isspace() for c in name) or "/" in name \
            or "\\" in name or name.startswith("."):
        raise SystemExit(
            f"❌ «{name}» не годится как {chto}: нужен слаг вида "
            "`2026-07-23_tema` — без пробелов, слэшей и ведущей точки.")


def _git(*args):
    return subprocess.run(["git", "--no-optional-locks", *args],
                          cwd=REPO_ROOT, capture_output=True, text=True)


def ensure_worktree(name, branch):
    """Заводит рабочую папку захода (идемпотентно). Возвращает (путь, код-возврата).

    Почему через git_zona.py, а не своим `git worktree add`: там уже лежит
    вся дисциплина — куда класть папки, как называть ветку, отказ снимать
    папку с незакоммиченной работой. Второй реализации быть не должно.
    """
    wt_home = REPO_ROOT.parent / f"{REPO_ROOT.name}-wt"
    path = wt_home / name
    if path.is_dir():
        print(f"Рабочая папка уже есть, беру её: {path}")
        return path, 0
    r = subprocess.run([sys.executable, str(GIT_ZONA), "worktree", "add", name,
                        "--branch", branch], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())
    if r.returncode != 0:
        print("ОШИБКА: рабочая папка не завелась — заход НЕ создаю.", file=sys.stderr)
        print("  Заход с несуществующей папкой хуже отсутствующего: исполнитель "
              "пойдёт работать в основную и подменит файлы соседям.", file=sys.stderr)
        return path, 1
    return path, 0


def main(argv):
    p = argparse.ArgumentParser(
        description="Генерит kod_<тема>.md с вшитым контрактом зоны.",
        epilog="--branch и --zone обязательны: контракт зоны — не опция.",
    )
    p.add_argument("arka_dir", help="папка арки (относительно корня репо или абсолютная)")
    p.add_argument("tema", help="короткий слаг темы → имя файла kod_<тема>.md")
    p.add_argument("--branch", required=True, help="ветка, на которой работает заход")
    p.add_argument("--zone", required=True, help="пути зоны (что МОЖНО менять), одной строкой")
    p.add_argument("--model", default="Sonnet", help="модель (по умолчанию Sonnet)")
    # ФЛАГ, а не третий позиционный: позиционных уже два, и третий сделал бы
    # «описание не задано» неотличимым от «аргументы поехали» — опечатка в
    # порядке молча родила бы `kod_<описание>.md`. Флаг необязателен по природе
    # и виден в --help.
    p.add_argument("--opisanie", metavar="ТЕКСТ",
                   help="описание захода одной фразой — уходит в KARTA.md §6 "
                        "тем же ходом; не задан → в индекс уйдёт явная пометка")
    p.add_argument("--kanal", choices=["terminal", "app"], default="terminal",
                   help="канал запуска: terminal (по умолчанию, печатает командную "
                        "строку для системного Терминала) или app (Claude Code в "
                        "десктопе) — см. RUKOVODSTVO §Два канала запуска")
    p.add_argument("--worktree", metavar="ИМЯ",
                   help="ПАРАЛЛЕЛЬНЫЙ заход: своя рабочая папка. Заводит её "
                        "`git_zona.py worktree add ИМЯ` и вписывает `cd` вместо checkout")
    a = p.parse_args(argv)
    validate_slug(a.tema, "тема захода (→ имя файла kod_<тема>.md)")  # ДО любой записи

    if not TEMPLATE.is_file():
        print(f"ОШИБКА: шаблон не найден — {TEMPLATE}", file=sys.stderr)
        return 1

    arka = Path(a.arka_dir)
    if not arka.is_absolute():
        arka = REPO_ROOT / arka
    if not arka.is_dir():
        print(f"ОШИБКА: папка арки не найдена — {arka}", file=sys.stderr)
        return 1

    dst = arka / f"kod_{a.tema}.md"
    if dst.exists():
        print(f"ОШИБКА: заход уже существует — {dst} (не затираю)", file=sys.stderr)
        return 1

    # 🔴 Развилку «worktree или checkout» решает ГЕНЕРАТОР, а не исполнитель.
    # Заход обязан быть самоценным: исполнитель работает с пустым контекстом, и
    # инструкция вида «дали папку — cd, не дали — checkout» заставляет его гадать
    # о том, чего он знать не может. Поэтому в файл уходит РОВНО ОДИН вариант.
    if a.worktree:
        wt_path, rc = ensure_worktree(a.worktree, a.branch)
        if rc:
            return rc
        mesto = (f"**рабочая папка `{wt_path}`** (worktree захода, ветка `{a.branch}` "
                 f"в ней уже стоит). 🔴 `git checkout` ЗАПРЕЩЁН: рядом идут другие "
                 f"заходы, переключение подменит файлы у них под ногами.")
        pervyj = (f"- `cd {wt_path}` — это твоя рабочая папка. Ветку НЕ переключай: "
                  f"`{a.branch}` в ней уже стоит.\n"
                  f"- Проверить, что ты на месте: `git rev-parse --abbrev-ref HEAD` "
                  f"→ должно быть `{a.branch}`.")
        start_line = f"cd {wt_path}"
    else:
        mesto = (f"ветка `{a.branch}` в основной папке. 🔴 Она должна УЖЕ стоять. "
                 f"НЕ на ней — СТОП, НЕ делай `git checkout`: в общей папке он МОЛЧА "
                 f"откатывает дерево к состоянию ветки (цена 27→28.07: файл сильно "
                 f"откатился ночью, поймал владелец вручную; след в git НЕ остаётся). "
                 f"Тогда заход пересобрать с `--worktree`. Ветку не переключай, в другие НЕ коммить.")
        pervyj = (f"- Проверь ветку: `git branch --show-current` — обязано быть `{a.branch}`. "
                  f"Не она — СТОП, `git checkout` НЕ делай (§4 GIT-disciplina), нужен `--worktree`.")
        start_line = "git branch --show-current"

    text = (
        TEMPLATE.read_text(encoding="utf-8")
        .replace("{{ТЕМА}}", a.tema)
        .replace("{{МОДЕЛЬ}}", a.model)
        .replace("{{ВЕТКА}}", a.branch)
        .replace("{{ЗОНА}}", a.zone)
        .replace("{{КОНТРАКТ_МЕСТО}}", mesto)
        .replace("{{ПЕРВЫЙ_ХОД}}", pervyj)
    )
    if "{{" in text:
        leftover = sorted({"{{" + t.split("}}")[0] + "}}" for t in text.split("{{")[1:]})
        print(f"ОШИБКА: в заходе остались незаполненные плейсхолдеры: {', '.join(leftover)}",
              file=sys.stderr)
        print("  Шаблон и генератор разъехались — чинить генератор, не заход.", file=sys.stderr)
        return 1
    dst.write_text(text, encoding="utf-8")

    print(f"Готово: {dst}")
    print("Контракт зоны вшит (ветка/зона/коммит/запрет). Дальше Cowork дозаполняет <...>:")
    print("  контекст · цель · что читать (якоря) · задача + критерий-что-провалится.")

    # 🔴 Регистрация — ТЕМ ЖЕ ХОДОМ, не отдельной командой и не напоминанием.
    # Напоминание здесь уже стояло в каноне и не работало: 27 обходов подряд.
    описание = a.opisanie or register_doc.ОПИСАНИЕ_НЕ_ЗАДАНО
    rc_reg = register_doc.registrate(dst, описание)
    if not a.opisanie:
        # Тихая заглушка ХУЖЕ отсутствия строки: она выглядит как выполненная
        # регистрация. Поэтому пометка видна и в индексе, и здесь.
        print(f"⚠ --opisanie не задан: в KARTA.md §6 ушла пометка "
              f"«{register_doc.ОПИСАНИЕ_НЕ_ЗАДАНО}». Опиши заход одной фразой и "
              f"поправь строку — описание единственное, ради чего индекс есть.",
              file=sys.stderr)
    if rc_reg:
        print("❌ Заход СОЗДАН, но НЕ зарегистрирован в KARTA.md §6 (причина выше). "
              "Файл не удаляю — удаление лоссово; зарегистрируй его руками "
              "дверью register_doc.py, иначе первый же коммит встанет.",
              file=sys.stderr)
        return 1

    rel = dst.relative_to(REPO_ROOT)
    print()
    if a.kanal == "terminal":
        kod_abs = str(REPO_ROOT / rel)
        model_l = a.model.lower()
        tema_raw = a.tema
        quote_hit = '"' in kod_abs or '"' in tema_raw
        kod_abs_safe = kod_abs.replace('"', "'")
        tema_log_safe = tema_raw.replace('"', "'")
        prompt_text = (
            f"Твой заход — файл {kod_abs_safe}. Прочитай ТОЛЬКО его и то, что он "
            "называет; остальной проект не изучай. План/вопросы/отчёт пиши в этот "
            "же файл внизу (## ПЛАН / ## ВОПРОСЫ / ## ОТЧЁТ). Ничего сверх задачи "
            "не трогай."
        )
        terminal_line = (
            f'cd {REPO_ROOT} && claude -p --verbose --model {model_l} '
            f'--dangerously-skip-permissions "{prompt_text}" 2>&1 | '
            f'tee /tmp/zahod-{tema_log_safe}.log'
        )
        print("═══ СТАРТОВАЯ КОМАНДА — вставить в системный Терминал ДОСЛОВНО ═══")
        print("(RUKOVODSTVO §Два канала запуска, форма A: -p — разовый запуск без")
        print(" диалога, --verbose — виден ход работы (иначе живой, зависший и")
        print(" оборванный прогоны выглядят одинаково), модель — флагом,")
        print(" tee — единственный след, если прогон упадёт.)")
        print()
        print("```")
        print(terminal_line)
        print("```")
        if quote_hit:
            print("⚠ В пути/теме была двойная кавычка — заменена на одинарную, чтобы "
                  "не сломать строку молча.", file=sys.stderr)
    else:
        print("═══ СТАРТОВОЕ СООБЩЕНИЕ — отдать владельцу ДОСЛОВНО, вместе с готовым заходом ═══")
        print("(RUKOVODSTVO §Стандартный текст запуска: МОДЕЛЬ — первой строкой. Печатается")
        print(" здесь, а не пишется по памяти: правило жило в каноне и всё равно забывалось.)")
        print()
        print("```")
        print(f"Модель: {a.model} — <одна фраза почему; см. шапку захода>.")
        print()
        print(f"Ты исполнитель в репозитории {REPO_ROOT}.")
        print()
        print("Твой единственный вход — файл-заход:")
        print(f"{REPO_ROOT / rel}")
        print()
        print("Прочитай его ЦЕЛИКОМ и работай строго по нему. Он самоценный: в нём назван")
        print("контракт зоны, ветка, что читать, задача, критерий готовности и форма отчёта.")
        print("Проект самостоятельно НЕ изучай и никаких других файлов по своей инициативе")
        print("не открывай — заход сам скажет, что читать.")
        print()
        print(f"Первым ходом: {start_line}, затем чтение захода, затем секция")
        print("## ПЛАН внутри него — до всяких действий.")
        print("```")
    if not a.worktree:
        # 🔴 Гейт против самой дорогой ошибки: checkout-заход, запущенный рядом
        # с живым соседом, подменит ему файлы. Молча этого не допускаем.
        others = [l for l in _git("worktree", "list").stdout.splitlines() if l.strip()]
        cur = _git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
        risky = len(others) > 1 or (cur and cur != a.branch)
        if risky:
            print()
            print("⚠⚠ ВНИМАНИЕ: заход СЕЙЧАС checkout-типа, а обстановка на гонку.")
            if cur and cur != a.branch:
                print(f"   Основная папка стоит на `{cur}`, а заходу нужна `{a.branch}`:")
                print("   его checkout перепишет рабочее дерево под всеми, кто там работает.")
            if len(others) > 1:
                print(f"   Живых рабочих папок: {len(others)} — значит заходы уже идут параллельно.")
            print(f"   Правильно: пересоздать с `--worktree {a.tema}` "
                  "(GIT-disciplina.md §4).")
    print()
    print("⚠ Путь выше — от того места, откуда запущен ЭТОТ скрипт. Гоняешь из песочницы —")
    print("  подставь путь машины владельца, иначе исполнитель не найдёт файл.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
