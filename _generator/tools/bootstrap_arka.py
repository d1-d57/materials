#!/usr/bin/env python3
"""Scaffold — заводит папку АРКИ (процесс-память) копией `zhurnal/_TEMPLATE-arka/`.

Использование:
    python3 bootstrap_arka.py <дата_тема> ["<концепция>"]
    python3 bootstrap_arka.py --koren <корень> <дата_тема> ["<концепция>"]

Корень по умолчанию — ИНФРА-корень реестра `korni.py` (сегодня `_studio`), то
есть поведение без флага не изменилось ни на йоту. `--koren` называет ЛЮБОЙ
корень реестра, у которого есть журнал: пока имя корня было вшито литералом,
вынесенная фабрика не могла завести ни арки, ни захода вовсе.

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

# Регистрацию делает ОБЩЕЕ ЯДРО, а не своя копия вставки в §6: та же причина,
# что у bootstrap_zahod.py — шаг «арка» и шаг «заход» обязаны писать в индекс
# одинаково, иначе строки разъедутся и разъезд обнаружится только через неделю.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import register_doc  # noqa: E402
import korni  # noqa: E402

REPO_ROOT = korni.REPO  # .../materials — единая формула на все инструменты
TEMPLATE_DIR = korni.шаблон("_TEMPLATE-arka")
# 🔴 ЖУРНАЛ ПО УМОЛЧАНИЮ ОСТАЁТСЯ МОДУЛЬНЫМ АТРИБУТОМ, а не вычисляется внутри
# `main()`. Это ШОВ, на котором держится ловушка 14 фикстуры `git_zona`: она
# подменяет `ZHURNAL_DIR` временным каталогом, чтобы проверять `validate_slug`,
# НИЧЕГО не записывая в боевой репозиторий. Спрячь его в локальную переменную —
# и подмена перестанет действовать МОЛЧА: проверка кривого входа начнёт заводить
# арки в живом `_studio/zhurnal/`. Поймано этой же ловушкой в этом заходе.
ZHURNAL_DIR = korni.REPO / f"{korni.ИНФРА}/zhurnal"

# Роль файла, а не выдумка: описание должно называть ЧТО это и КАКОЙ арки —
# иначе пять строк в §6 неотличимы друг от друга и от соседних арок.
ОПИСАНИЯ_АРКИ = {
    "PLAN.md": "план арки {slug}",
    "TZ.md": "контракт арки {slug}",
    "SESSIYA.md": "дневник арки {slug}",
    "NAVIGATOR.md": "навигатор арки {slug} (ориентация, читается первым): {concept}",
    "UROKI-FABRIKE.md": "уроки арки {slug} с ценой, вход закрывающей сессии",
}


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


def zhurnal_korny(имя):
    """Папка журнала названного корня. Кривое имя → ГРОМКИЙ отказ, а не «сделал не то».

    Тот же закон, что у `validate_slug`: инструмент, молча подставивший корень по
    умолчанию вместо непонятого, завёл бы арку не там, где просили, и это
    обнаружилось бы только когда её начнут искать.

    Для ИНФРА-корня отдаём модульный `ZHURNAL_DIR` — тот самый шов, на котором
    фикстура проверяет валидацию имени, не записывая в боевое дерево.
    """
    if имя == korni.ИНФРА:
        return ZHURNAL_DIR
    for к in korni.КОРНИ:
        if к.имя == имя:
            if not к.журнал:
                raise SystemExit(
                    f"❌ У корня «{имя}» нет журнала: арке негде лежать. "
                    f"Журналы есть у: {', '.join(korni.все_журналы()) or '<ни у кого>'}")
            return REPO_ROOT / к.журнал
    известные = ", ".join(к.имя for к in korni.КОРНИ)
    raise SystemExit(f"❌ Корень «{имя}» не назван в реестре _generator/tools/korni.py. "
                     f"Известные: {известные}")


def main(argv):
    argv = list(argv)
    корень = korni.ИНФРА
    if argv and argv[0] == "--koren":
        if len(argv) < 2:
            raise SystemExit("❌ `--koren` требует имя корня из реестра korni.py")
        корень = argv[1]
        argv = argv[2:]
    if not (1 <= len(argv) <= 2):
        print(__doc__.strip(), file=sys.stderr)
        return 2

    slug = argv[0]
    validate_slug(slug, "имя арки")  # флаг/кривой слаг → SystemExit ДО любой записи
    concept = argv[1] if len(argv) == 2 else "<концепция — заполнить на Ф0>"

    ZHURNAL_DIR = zhurnal_korny(корень)   # неизвестный корень → SystemExit ДО записи

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

    # 🔴 Дверь на все пять файлов ТЕМ ЖЕ ходом — иначе каждая новая арка рождает
    # пять сирот: ворота 5 про них молчат по подстрочному совпадению чужих
    # токенов §6 (в разделе уже есть `PLAN.md` и прочие от других арок), то
    # есть дефект не просто есть, а невидим.
    провал = False
    for имя, шаблон_описания in ОПИСАНИЯ_АРКИ.items():
        путь = target / имя
        if not путь.is_file():
            continue
        описание = шаблон_описания.format(slug=slug, concept=concept)
        if register_doc.registrate(путь, описание):
            print(f"❌ АРКА СОЗДАНА, НО «{имя}» НЕ ЗАРЕГИСТРИРОВАН в KARTA.md §6 "
                  f"(причина выше). Файлы НЕ удаляю — удаление лоссово; "
                  f"зарегистрируй руками дверью register_doc.py "
                  f"{путь.relative_to(REPO_ROOT)} \"<описание>\".", file=sys.stderr)
            провал = True
    if провал:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
