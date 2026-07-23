#!/usr/bin/env python3
"""Scaffold — создаёт стаб-дерево папки лекции по docs/spravka/PAPKA-LEKCII.md.

Использование:
    python3 bootstrap_lekcia.py <путь/имя-лекции> [--slides yes|no]

Идемпотентен: существующую папку НЕ перезатирает — предупреждает и выходит с кодом 1.
"""
import argparse
import datetime
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]  # .../materials
SKELETON_DIR = REPO_ROOT / "_generator" / "skeleton"
CATALAN_STANDART_UZLA = REPO_ROOT / "catalan" / "spravochnik" / "STANDART-uzla.md"


def validate_slug(name, chto):
    """Кривой вход обязан ГРОМКО падать, а не тихо создать папку не с тем именем.

    Тот же класс, что закрыт в bootstrap_arka.py (инцидент 23.07 с `--help`).
    Здесь `path` — путь целиком (слэши легитимны как разделители), поэтому
    валидируется ИМЯ последнего компонента (`target.name`): ведущий `-`, пустое,
    пробелы, ведущая точка — не слаг. Дублируется сознательно (общий модуль лёг бы
    вне зоны захода — см. kod_bootstrap-guard).
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


def navigator_md(name):
    return f"""# НАВИГАТОР лекции «{name}»

## Концепция — что строим, какую функцию (1 абзац)

## Границы — что НЕ входит (anti-scope)

## Указатели в долгую — места проекта, которые трогаем (выжимка; файл→раздел→когда)

## Внешние источники — ссылки

## Скиллы — какие поднимать

## Процедуры
вход → ARKA §3 · план → §4 · хэндофф → §6 · закрытие → §7
"""


def plan_md(name):
    return f"""# ПЛАН лекции «{name}»

## ⭐ СЕЙЧАС
бриф (01-brief) — заполнить 9 полей `brief.md`.

## Шаги
- [ ] 01 бриф
- [ ] 02 ресёрч (карточный граф)
- [ ] 03 матбаза (строгий слой skelet)
- [ ] 04 гибрид-источник (rasskaz + skelet)
- [ ] 05 раскадровка
- [ ] 06 текст
- [ ] 07 вёрстка
- [ ] 08 сцены
- [ ] 09 иллюстрации
- [ ] 10 сборка + QA
"""


def sessiya_md(name, today):
    return f"""# СЕССИЯ — дневник лекции «{name}»

## {today} — старт
Папка заведена скаффолдом `bootstrap_lekcia.py`. Дальше — по `PLAN.md`.
"""


def brief_md(slides_flag):
    return f"""# БРИФ

1. тема: <...>
2. аудитория: <...>
3. длительность: <...> → бюджет слайдов: <...>
4. throughline-кандидат: <...>
5. что резать: <...>
6. материал/референс: <...>
7. уровень строгости: интуитивный | выкладки-свёрнуты | полностью-строгий — <выбрать>
8. формат события: устный | читаемый — <выбрать>; лекция|курс: <выбрать>
9. слайды: {"да" if slides_flag == "yes" else "нет"}
"""


def karta_oblasti_md(name):
    return f"""# КАРТА ОБЛАСТИ — «{name}»

Индекс всех узлов: по роду и по нитям. Адресация по `id`. Пуст на старте — пополняется в 02-reserch.

## Узлы по роду

## Нити
"""


def obiekty_md(name):
    return f"""# ОБЪЕКТЫ-РУЧКИ — «{name}»

Общие узлы, на которые ссылаются несколько нитей. Формат строки: `id · род · суть · счёт · источник` (см. `STANDART-uzla.md`).

(пусто)
"""


def manifest_md(name):
    return f"""# MANIFEST — источники лекции «{name}»

Физическая раскладка `istochniki/pdf/`. Дайджесты чтения — `VYCHITANO.md`. Чеклист докачки — `SPISOK-skachat.md`.

(пусто — заполняется в 02-reserch)
"""


def vychitano_md(name):
    return f"""# ВЫЧИТАНО — что реально ЕСТЬ (и чего НЕТ) в источниках лекции «{name}»

> Дисциплина: после каждого прочтения источника — дайджест сюда ТЕМ ЖЕ ходом. Источник без дайджеста = как будто не читан.
>
> Шаблон записи:
> ```
> ### <файл или ссылка>
> Читал: <кто/заход; стр./разделы>
> Искали: <вопрос>
> ЕСТЬ: <что найдено, со стр.>
> НЕТ (проверено): <чего точно нет>
> Уровень: школьно | требует-приручения | вне-школы
> Итог: <как используем>
> ```

(пусто)
"""


def spisok_skachat_md(name):
    return f"""# СПИСОК НА СКАЧИВАНИЕ — источники лекции «{name}»

(пусто — заполняется в 02-reserch)
"""


def terminy_md(name):
    return f"""# ТЕРМИНЫ (русские) — «{name}»

> Правило: гейт сверки терминов смотрит СЮДА первым; веб-поиск — только для термина, которого здесь нет; нашёл — сразу дописал строку.

## Имена

| Оригинал | Русский | Статус | Примечание |
|---|---|---|---|
"""


def kotel_matematika_md(name):
    return f"""---
tab: Математика
status: stub
poryadok: 1
registr: TBD
---

# {name} — математический скелет

> поле: стаб, наполняется в 02–03 (карточный граф котла математика → строгий слой skelet).
"""


def kotel_naupop_md(name):
    return f"""---
tab: Научпоп
status: stub
poryadok: 2
registr: TBD
---

# {name} — научпоп

> поле: стаб, наполняется в 02 (карточный граф котла научпоп).
"""


def rasskaz_md(name):
    return f"""# {name} — рассказ (нить)

> Стаб. Наполняется аркой 4a: нить, вытянутая из карточного графа в сюжет.
"""


def skelet_md(name):
    return f"""# {name} — skelet (гибрид-источник)

> Стаб. Наполняется аркой 4b: сшивка `rasskaz.md` со строгим слоем котла математика цитатой-сноской.
"""


def write(path, text):
    path.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Scaffold папки лекции (стаб-дерево).")
    parser.add_argument("path", help="путь/имя новой папки лекции")
    parser.add_argument("--slides", choices=["yes", "no"], default="no", help="заводить ли src/ (копия _generator/skeleton/)")
    args = parser.parse_args()

    target = Path(args.path).resolve()
    validate_slug(target.name, "имя лекции")  # флаг/кривой слаг → SystemExit ДО mkdir
    if target.exists():
        print(f"ОШИБКА: папка уже существует — {target} (не затираю)", file=sys.stderr)
        return 1

    name = target.name
    today = datetime.date.today().isoformat()

    target.mkdir(parents=True)

    write(target / "NAVIGATOR.md", navigator_md(name))
    write(target / "PLAN.md", plan_md(name))
    write(target / "SESSIYA.md", sessiya_md(name, today))
    write(target / "brief.md", brief_md(args.slides))

    kartoteka = target / "kartoteka"
    kartoteka.mkdir()
    write(kartoteka / "KARTA-OBLASTI.md", karta_oblasti_md(name))
    if CATALAN_STANDART_UZLA.exists():
        shutil.copyfile(CATALAN_STANDART_UZLA, kartoteka / "STANDART-uzla.md")
    else:
        print(f"ПРЕДУПРЕЖДЕНИЕ: {CATALAN_STANDART_UZLA} не найден — STANDART-uzla.md не скопирован", file=sys.stderr)
    write(kartoteka / "obiekty.md", obiekty_md(name))

    istochniki = target / "istochniki"
    istochniki.mkdir()
    write(istochniki / "MANIFEST.md", manifest_md(name))
    write(istochniki / "VYCHITANO.md", vychitano_md(name))
    write(istochniki / "SPISOK-skachat.md", spisok_skachat_md(name))
    write(istochniki / "TERMINY.md", terminy_md(name))
    pdf_dir = istochniki / "pdf"
    pdf_dir.mkdir()
    write(pdf_dir / ".gitkeep", "")

    kotly = target / "kotly"
    kotly.mkdir()
    write(kotly / "matematika.md", kotel_matematika_md(name))
    write(kotly / "naupop.md", kotel_naupop_md(name))

    chernovik = target / "chernovik"
    chernovik.mkdir()
    write(chernovik / "rasskaz.md", rasskaz_md(name))
    write(chernovik / "skelet.md", skelet_md(name))

    raskadrovka = target / "raskadrovka"
    raskadrovka.mkdir()
    write(raskadrovka / ".gitkeep", "")

    if args.slides == "yes":
        if not SKELETON_DIR.exists():
            print(f"ОШИБКА: {SKELETON_DIR} не найден — src/ не создан", file=sys.stderr)
            return 1
        shutil.copytree(SKELETON_DIR, target / "src")

    print(f"Готово: {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
