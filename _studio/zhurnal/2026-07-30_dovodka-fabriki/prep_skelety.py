#!/usr/bin/env python3
"""ПРЕДПОДГОТОВКА СКЕЛЕТОВ — переносит механику разметки с модели на скрипт.

    python3 _studio/zhurnal/2026-07-30_dovodka-fabriki/prep_skelety.py

ЗАЧЕМ ЭТОТ ФАЙЛ СУЩЕСТВУЕТ (причина дороже кода — не удалять).

Первая редакция заходов Н1/Н2 требовала от исполнителя ВЫПИСАТЬ таблицу:
на каждую запись корпуса строку вида `| ось | файл | заголовок | АДРЕС |`.
На 1379 записях корпуса владельца и 461 корпуса исполнителей это ~55 000
токенов ВЫХОДА, потраченных на копирование того, что уже лежит на диске.

Вторая беда была дороже денег: адрес, переписанный моделью, — это адрес,
который модель могла исказить. В критерии приёмки Н1 отдельным пунктом стоит
«возьми 10 адресов и проверь грепом, что они существуют» — то есть заход
защищался от собственного копирования.

Лечение: скрипт нарезает корпус на СКЕЛЕТ (id · источник · заголовок · адрес ·
группа), модель дописывает только ВЕРДИКТ (`id<TAB>ярус<TAB>материя`), а
финальную таблицу собирает `sobrat_razmetku.py` join'ом по id. Адреса при этом
не проходят через модель ВООБЩЕ и исказиться не могут.

Только stdlib. Идемпотентен: перезаписывает скелеты, вердикты не трогает.
"""
import re
import sys
from pathlib import Path

ARKA = Path(__file__).resolve().parent


def rez(s: str, n: int) -> str:
    """Обрезать и вычистить табы — TSV не терпит их внутри поля."""
    s = re.sub(r"\s+", " ", s).replace("\t", " ").strip()
    return s[:n]


def zapisi(text: str):
    """Разбить корпус на записи `### ...` с полями `ПОЛЕ: значение`.

    Возвращает список словарей; ключ `_zagolovok` — текст после `### `,
    `_istochnik` — последний виденный `## Источник: ...` (в корпусе владельца).
    """
    out, cur, istochnik = [], None, ""
    for line in text.splitlines():
        if line.startswith("## Источник: "):
            istochnik = line[len("## Источник: "):].strip()
            istochnik = re.sub(r"`?\s*\(\d+\s*строк.*$", "", istochnik).strip("` ")
            continue
        if line.startswith("### "):
            if cur:
                out.append(cur)
            cur = {"_zagolovok": line[4:].strip(), "_istochnik": istochnik}
            continue
        if cur is None:
            continue
        m = re.match(r"^([А-ЯЁA-Z][А-ЯЁA-Z ]{2,20}):\s*(.*)$", line)
        if m:
            cur.setdefault(m.group(1).strip(), m.group(2).strip())
    if cur:
        out.append(cur)
    return out


def pisat(path: Path, header: str, rows: list) -> int:
    path.write_text(header + "\n" + "\n".join(rows) + "\n", encoding="utf-8")
    return len(rows)


def skelet_vladelca():
    src = ARKA / "KORPUS-VLADELCA.md"
    zs = zapisi(src.read_text(encoding="utf-8"))
    rows, chisla = [], []
    for i, z in enumerate(zs, 1):
        gid = f"V{i:04d}"
        rows.append("\t".join([
            gid,
            rez(z.get("_istochnik", ""), 70),
            rez(z["_zagolovok"], 90),
            rez(z.get("АДРЕС", ""), 160),
            rez(z.get("КАСАЕТСЯ", ""), 30),
            rez(z.get("КЛАСС", ""), 20),
            # Цитата нужна для СУЖДЕНИЯ: с ней разметчик в большинстве случаев
            # не открывает корпус вообще. 200 знаков хватает — реплики владельца
            # короткие, а длинные всё равно судятся по началу.
            rez(z.get("ЦИТАТА", ""), 200),
        ]))
        # Осторожно: у одной записи поле выглядит как «НЕТ (названы величины,
        # но не значения)» — это ОТСУТСТВИЕ числа, а не число. Сравнение на
        # равенство её пропускает, поэтому проверяем префикс.
        ch = z.get("ЧИСЛО", "НЕТ")
        if ch and not ch.upper().startswith("НЕТ"):
            chisla.append("\t".join([
                gid,
                rez(ch, 90),
                rez(z.get("АДРЕС", ""), 160),
                rez(z.get("ЦИТАТА", ""), 220),
            ]))
    n1 = pisat(ARKA / "skelet-vladelca.tsv",
               "# id\tисточник\tзаголовок\tАДРЕС\tКАСАЕТСЯ\tКЛАСС\tЦИТАТА", rows)
    n2 = pisat(ARKA / "skelet-chisla.tsv",
               "# id\tЧИСЛО\tАДРЕС\tЦИТАТА", chisla)
    return n1, n2


def skelet_ispolnitelej():
    rows = []
    files = sorted(p for p in ARKA.glob("KORPUS-*.md") if "VLADELCA" not in p.name)
    i = 0
    for p in files:
        for z in zapisi(p.read_text(encoding="utf-8")):
            i += 1
            rows.append("\t".join([
                f"I{i:04d}",
                p.name,
                rez(z["_zagolovok"], 90),
                rez(z.get("АДРЕС", ""), 160),
                rez(z.get("ЦЕНА", ""), 90),
            ]))
    n = pisat(ARKA / "skelet-ispolnitelej.tsv",
              "# id\tфайл\tзаголовок\tАДРЕС\tЦЕНА", rows)
    return n, len(files)


if __name__ == "__main__":
    v, ch = skelet_vladelca()
    isp, nf = skelet_ispolnitelej()
    print(f"skelet-vladelca.tsv:      {v} записей")
    print(f"skelet-chisla.tsv:        {ch} записей с названным числом")
    print(f"skelet-ispolnitelej.tsv:  {isp} записей из {nf} файлов")
    if v != 1379 or ch != 269 or isp != 461:
        print("⚠ РАСХОЖДЕНИЕ с базой 1379 / 269 / 461 — разобраться ДО запуска ночи",
              file=sys.stderr)
        sys.exit(1)
    print("✅ сошлось с базой 1379 / 269 / 461")
