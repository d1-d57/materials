#!/usr/bin/env python3
"""Scaffold — заводит папку АРКИ (процесс-память) копией _studio/zhurnal/_TEMPLATE-arka/.

Использование:
    python3 bootstrap_arka.py <дата_тема> ["<концепция>"]

Операционализация правила «перекопировать начальное состояние с новыми задачами»
(ARKA.md §10 C, RESHENIYA Р22). НЕ то же, что bootstrap_lekcia.py: тот генерит дерево
ЛЕКЦИИ из строк; этот КОПИРУЕТ шаблон АРКИ и подставляет {{ИМЯ}}/{{ДАТА}}/{{КОНЦЕПЦИЯ}}.
Ручные плейсхолдеры (<...>) остаются — их дозаполняет Cowork с владельцем на Ф0.

Идемпотентен: существующую папку НЕ перезатирает — предупреждает и выходит с кодом 1.
Только stdlib.
"""
import datetime
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]  # .../materials
TEMPLATE_DIR = REPO_ROOT / "_studio" / "zhurnal" / "_TEMPLATE-arka"
ZHURNAL_DIR = REPO_ROOT / "_studio" / "zhurnal"


def validate_slug(name, chto):
    """Кривой вход обязан ГРОМКО падать, а не тихо фабриковать папку.

    Инцидент 23.07: `bootstrap_arka.py --help` проглотил флаг как имя арки и
    молча создал папку-сироту `_studio/zhurnal/--help/` со скелетом — untracked,
    и каждый `git_zona.py plan` тянул её в черновик коммита. Корень: на кривом
    входе инструмент обязан упасть, а не сделать не то (флаг проглочен как данные).

    Дублируется в трёх bootstrap_* СОЗНАТЕЛЬНО: общий модуль лёг бы вне зоны
    захода (зона — поимённо три скрипта, не вся tools/); ~8 строк дешевле
    нарушения контракта. Парная защита в git_zona.py: `plan` карантинит такой
    мусор, `purge` его снимает.
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


def substitute(text, name, today, concept):
    return (
        text.replace("{{ИМЯ}}", name)
        .replace("{{ДАТА}}", today)
        .replace("{{КОНЦЕПЦИЯ}}", concept)
    )


def main(argv):
    if not (1 <= len(argv) <= 2):
        print(__doc__.strip(), file=sys.stderr)
        return 2

    slug = argv[0]
    validate_slug(slug, "имя арки")  # флаг/кривой слаг → SystemExit ДО любой записи
    concept = argv[1] if len(argv) == 2 else "<концепция — заполнить на Ф0>"

    if not TEMPLATE_DIR.is_dir():
        print(f"ОШИБКА: шаблон не найден — {TEMPLATE_DIR}", file=sys.stderr)
        return 1

    target = ZHURNAL_DIR / slug
    if target.exists():
        print(f"ОШИБКА: папка арки уже существует — {target} (не затираю)", file=sys.stderr)
        return 1

    today = datetime.date.today().isoformat()

    target.mkdir(parents=True)
    for src in sorted(TEMPLATE_DIR.rglob("*")):
        rel = src.relative_to(TEMPLATE_DIR)
        dst = target / rel
        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
            continue
        text = src.read_text(encoding="utf-8")
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(substitute(text, slug, today, concept), encoding="utf-8")

    print(f"Готово: {target}")
    print("Дальше (ARKA §10 C): Cowork дозаполняет NAVIGATOR/TZ/PLAN (границы, задачи) и пишет хэндофф в эту арку.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
