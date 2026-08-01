#!/usr/bin/env python3
"""СБОРЩИК СВОДНОГО РЕЕСТРА ИСТОЧНИКОВ (PDF по всем проектам).

    python3 _studio/zhurnal/_INFRA-git/sobrat_reestr.py          # пересобрать реестр
    python3 _studio/zhurnal/_INFRA-git/sobrat_reestr.py --stdout # напечатать, не писать

Запускать из корня репо. stdlib, без сети, детерминизм (сортировка по пути).

ЗАЧЕМ. Книги и статьи (166 файлов, 378 МБ) с диска НЕ удаляются: их ценность —
локальный полнотекстовый поиск, и удаление её убивает. Но лежат они россыпью по
десятку проектов, и на вопрос «что у нас вообще есть» до сих пор отвечал только
`find`. Реестр — один список на все проекты, он в git идёт, сами PDF — нет.

ПОЧЕМУ ЭТО СКРИПТ, А НЕ ФАЙЛ, НАПИСАННЫЙ РУКАМИ. Реестр целиком состоит из
производных фактов: размер, число файлов, наличие дайджеста. `KONSTITUCIYA §10`
— такое либо считается командой, либо не пишется. Записанный руками реестр
устареет с первой же скачанной книгой и соврёт, как соврала строка «19» в
`teoriya-kategoriy/istochniki/VYCHITANO.md` (починка враньём продержалась один ход).

ОТМЕТКА `VYCHITANO` — НЕ СВОЯ ВЫДУМКА. Берётся метод, который проект прописал
сам себе в шапке `teoriya-kategoriy/istochniki/VYCHITANO.md`:

    for f in pdf/*.pdf; do grep -q "$(basename $f)" VYCHITANO.md || echo "БЕЗ ДАЙДЖЕСТА: $f"

То есть: имя файла упомянуто в ближайшем вверх по дереву `VYCHITANO.md` — есть
дайджест. Метод грубый (совпадение по имени, не по смыслу) — так и написано в
шапке реестра, чтобы никто не принял «✓» за «прочитано целиком».

ЧЕГО НЕ ДЕЛАЕТ: не открывает PDF, не проверяет текстовый слой, не судит о
качестве дайджеста и не трогает ни одного файла источников.
"""
import subprocess
import sys
from pathlib import Path

KOREN = Path(__file__).resolve().parents[3]
REESTR = KOREN / "_studio/zhurnal/_INFRA-git/REESTR-istochnikov.md"


def chelovecheski(bajt):
    """Байты → «12.3 МБ». Двоичные единицы, как у du."""
    for edinica, porog in (("ГБ", 1 << 30), ("МБ", 1 << 20), ("КБ", 1 << 10)):
        if bajt >= porog:
            return f"{bajt / porog:.1f} {edinica}"
    return f"{bajt} Б"


def vychitano_dlya(pdf):
    """Ближайший вверх по дереву VYCHITANO.md → упомянуто ли имя файла.

    Возвращает (otmetka, put_k_vychitano). Файла нет вообще → («—», None):
    это не «не вычитан», это «в проекте нет самого механизма дайджестов».
    """
    papka = pdf.parent
    while papka != KOREN and KOREN in papka.parents:
        kandidat = papka / "VYCHITANO.md"
        if kandidat.exists():
            tekst = kandidat.read_text(encoding="utf-8", errors="replace")
            est = pdf.name in tekst
            return ("✓" if est else "нет"), kandidat.relative_to(KOREN)
        papka = papka.parent
    return "—", None


def proekt(otn):
    """Путь относительно корня → имя проекта (первый компонент)."""
    return otn.parts[0]


def sobrat():
    pdfy = sorted(
        p for p in KOREN.rglob("*.pdf")
        if ".git" not in p.relative_to(KOREN).parts and p.is_file()
    )
    stroki, vsego_bajt = [], 0
    bez_mehanizma, bez_dajdzhesta, s_dajdzhestom = 0, 0, 0
    for pdf in pdfy:
        otn = pdf.relative_to(KOREN)
        razmer = pdf.stat().st_size
        vsego_bajt += razmer
        otmetka, istochnik = vychitano_dlya(pdf)
        if otmetka == "✓":
            s_dajdzhestom += 1
        elif otmetka == "нет":
            bez_dajdzhesta += 1
        else:
            bez_mehanizma += 1
        stroki.append(
            f"| `{otn}` | {chelovecheski(razmer)} | {proekt(otn)} | {otmetka} |"
        )
    return stroki, vsego_bajt, (s_dajdzhestom, bez_dajdzhesta, bez_mehanizma)


def sobrat_tekst():
    stroki, vsego, (est, net, nikak) = sobrat()
    shapka = f"""# РЕЕСТР ИСТОЧНИКОВ — все PDF репозитория, один список

> **Собран командой, руками не править — правка умрёт при следующей пересборке:**
> ```
> python3 _studio/zhurnal/_INFRA-git/sobrat_reestr.py
> ```
> Сами PDF в git НЕ идут (`.gitignore`) — идёт только этот список. Он и есть
> ответ на «что у нас вообще есть», когда файлов не видно с другой машины.

**Зачем источники лежат на диске и почему их нельзя удалять.** Владелец: *«я их
скачиваю, потому что мы по ним делаем поиск, когда хотим узнать конкретную
информацию, которую нельзя установить из интернета… иногда нам нужно из всех
книжек взять упражнения»*. Ценность — в **локальном полнотекстовом поиске**;
удаление её убивает. Сжатие тоже: PDF уже сжаты, ghostscript даёт 10–20 % и
портит формулы, zip ломает сам поиск.

**Числа — не вписаны, а посчитаны сборщиком в момент сборки:**

| | |
|---|---|
| файлов | **{len(stroki)}** |
| суммарный вес | **{chelovecheski(vsego)}** |
| с дайджестом в `VYCHITANO.md` | {est} |
| без дайджеста (механизм в проекте есть) | {net} |
| механизма дайджестов в проекте нет | {nikak} |

Сверить число файлов с диском, не веря этой таблице:
```
find . -name "*.pdf" -not -path "./.git/*" | wc -l
grep -c '^| `' _studio/zhurnal/_INFRA-git/REESTR-istochnikov.md
```

⚠ **Что значит «✓» и чего оно НЕ значит.** Отметка ставится грубо: имя файла
упомянуто в ближайшем вверх по дереву `VYCHITANO.md`. Это метод самого проекта
(шапка `teoriya-kategoriy/istochniki/VYCHITANO.md`), и он отвечает на вопрос
«заводили ли по файлу дайджест», а **не** «прочитан ли он целиком». Прочерк «—»
означает не «не читан», а что в проекте нет самого файла `VYCHITANO.md`.

| Путь | Размер | Проект | `VYCHITANO` |
|---|---|---|---|
"""
    return shapka + "\n".join(stroki) + "\n"


if __name__ == "__main__":
    tekst = sobrat_tekst()
    if "--stdout" in sys.argv:
        sys.stdout.write(tekst)
    else:
        REESTR.write_text(tekst, encoding="utf-8")
        print(f"собран: {REESTR.relative_to(KOREN)}")
        print(subprocess.run(
            ["grep", "-c", "^| `", str(REESTR)],
            capture_output=True, text=True).stdout.strip() + " строк-файлов")
