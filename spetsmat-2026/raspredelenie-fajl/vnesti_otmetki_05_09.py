#!/usr/bin/env python3
"""Отметки за 5 сентября 2026 + починка состава листка 16α.

🔴 ПИШЕТ В ЖИВУЮ БАЗУ НА СЕРВЕРЕ: /opt/spetsmat-bot/data/spetsmat.db.
Ноутбучная копия — не она: `deploy/vykatka.sh` исключает `data/` намеренно, и
вписанное на ноутбуке на сайте не появится. Поэтому по умолчанию скрипт
отказывается работать с базой вне /opt — см. `--razreshit-lokalno`.

ЧТО ДЕЛАЕТ, ПО ШАГАМ

  1. Убеждается, что база наша: ≥50 активных школьников, листки 16A/16α/16ℵ.
     Если листков нет — заводит их и все задачи (состав снят из PDF, которые
     раздаются с сайта: /listki/16A-derevya.pdf и соседние).

  2. Приводит состав 16α к тому листку, что выложен на сайте: задачи 1–15,
     пункты а/б/в у задачи 14, у задачи 10 пунктов НЕТ.
     🔴 Ячейки 10а/10б/10в удаляются, только если на них нет ни одной отметки.
     Если хоть одна есть — скрипт их не трогает и пишет об этом в отчёт.

  3. Кладёт 113 отметок за 05.09: event='assert', source='фото',
     teacher_id пустой (решение владельца 07.09 — как и 03.09).

  4. Перечитывает записанное ИЗ БАЗЫ и печатает «внесено N из 113».

ИДЕМПОТЕНТЕН. Ключ '<student_id>-<problem_id>-2026-09-05' уникален в схеме
(`marks_idempotency`), повторный прогон печатает «новых 0».

    python3 vnesti_otmetki_05_09.py             # сухой прогон, база не тронута
    python3 vnesti_otmetki_05_09.py --primenit
    python3 vnesti_otmetki_05_09.py --proverka  # только перечитать и посчитать

Расшифровка семи фотографий и все оговорки: materials/spetsmat-2026/konduit-5-sentyabrya.md
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

BAZA_PO_UMOLCHANIYU = Path("/opt/spetsmat-bot/data/spetsmat.db")
DATA_ZANYATIYA = "2026-09-05"
ISTOCHNIK = "фото"          # схема: кнопка · фото · голос · импорт
ZAMETKA = ("бумажка 05.09, расшифрована аналитиком; "
           "см. materials/spetsmat-2026/konduit-5-sentyabrya.md")

# ── СОСТАВ ЛИСТКОВ ────────────────────────────────────────────────────────────
# Снят из PDF, которые отдаёт сам сайт. Знак после номера в листке:
# ◦ обязательная · † письменная сдача · ? звезда · без знака обычная.
# 🔴 Решение 05.09, оставлено как было: † — способ сдачи, а не сложность,
# такие задачи кладём как «обязательная».
LISTKI = {
    "16A": ("16A. Деревья", [
        ("1а", "обязательная"), ("1б", "обязательная"),
        ("2", "обязательная"), ("3", "обязательная"), ("4", "обязательная"),
        ("5", "обязательная"),
        ("6а", "обязательная"), ("6б", "обязательная"),
        ("7а", "обязательная"), ("7б", "обязательная"), ("7в", "обязательная"),
        ("8", "обязательная"), ("9", "обязательная"),
        ("10а", "обязательная"), ("10б", "обязательная"),
        ("11а", "обязательная"), ("11б", "обязательная"), ("11в", "обязательная"),
        ("12", "звезда"), ("13а", "звезда"), ("13б", "звезда"),
    ]),
    # 🔴 ПЯТНАДЦАТЬ задач на ОДНОЙ странице. Пункты а/б/в стоят у 14, а не у 10.
    # Проверка: `pdftotext -layout 16α-derevya.pdf` и та же выдача с сайта.
    "16α": ("16α. Деревья", [
        ("1", "обязательная"), ("2", "обязательная"), ("3", "обязательная"),
        ("4", "обязательная"), ("5", "обязательная"), ("6", "обязательная"),
        ("7", "обязательная"), ("8", "обязательная"),
        ("9", "обычная"), ("10", "обязательная"), ("11", "обычная"),
        ("12", "обычная"), ("13", "обычная"),
        ("14а", "обязательная"), ("14б", "обязательная"), ("14в", "звезда"),
        ("15", "звезда"),
    ]),
    "16ℵ": ("16ℵ. Деревья", [
        ("-1а", "обязательная"), ("-1б", "обязательная"), ("-1в", "обязательная"),
        ("0", "звезда"),
        ("1", "обычная"), ("2", "обычная"),
        ("3а", "обычная"), ("3б", "обычная"),
        ("4", "обычная"), ("5", "обычная"), ("6", "обычная"),
        ("7", "обязательная"), ("8", "обычная"),
    ]),
}

# Ячейки, которых в листке 16α нет: пункты приписаны не той задаче.
LISHNIE_V_ALFA = ["10а", "10б", "10в"]

# ── ОТМЕТКИ ЗА 5 СЕНТЯБРЯ ─────────────────────────────────────────────────────
# (фамилия, листок, [задачи]). id школьников берутся ИЗ БАЗЫ по фамилии, не вписаны.
# Диапазон и одиночный номер уже развёрнуты в задачу целиком (правило владельца:
# «1–6» — все шесть со всеми пунктами; «7» — вся седьмая).
SDANO = [
    ("Пономарев",     "16α", ["1", "3", "5", "6"]),
    # Вторая восьмёрка в строке — задача 4 (владелец, 07.09).
    ("Глебова",       "16A", ["6а", "6б", "8", "10б", "4"]),
    ("Фефелов",       "16ℵ", ["1", "2"]),
    # Замазанная позиция — 2 (владелец, 07.09).
    ("Ишкаев",        "16α", ["1", "2", "3", "4", "5", "6"]),
    # Знак после 12 — 8 (владелец, 07.09).
    ("Быков",         "16α", ["2", "3", "4", "8", "12"]),
    ("Кудишин",       "16α", ["1", "2", "3", "4", "5", "6"]),
    ("Верхошинский",  "16α", ["1", "2", "3", "4", "5", "6", "7", "8", "9",
                              "10", "12", "13", "14а", "14б"]),
    ("Пирогов",       "16A", ["1а", "1б", "2", "3", "4", "5", "6а", "6б"]),
    ("Пирогов",       "16α", ["1", "2", "3", "4", "5", "6", "7", "8"]),
    ("Юсуфов",        "16A", ["1а", "1б", "2", "3", "4", "5", "6а", "6б",
                              "7а", "7б", "7в"]),
    ("Кудряшов",      "16ℵ", ["-1а", "-1в"]),
    ("Симонова",      "16α", ["5", "6", "7"]),
    ("Храмченко",     "16α", ["4", "8", "10"]),
    ("Ордян",         "16A", ["3"]),
    ("Ордян",         "16α", ["3"]),
    # Перечёркнутая крест-накрест «3» не ставится.
    ("Болотин",       "16A", ["4", "5", "7а"]),
    ("Белеванцева",   "16A", ["1а", "1б", "2", "3", "4", "5", "6а", "6б"]),
    ("Аникина",       "16α", ["2", "3", "4", "5", "6"]),
    ("Жуков",         "16α", ["4", "6", "8"]),
    ("Устинина",      "16α", ["2", "3", "4", "6", "8"]),
    ("Егоров",        "16α", ["3", "4"]),
    ("Леонович",      "16A", ["1б"]),
    ("Леонович",      "16α", ["4", "6"]),
    ("Лим",           "16α", ["1", "4"]),
    ("Лупулешин",     "16α", ["1", "4", "6"]),
]
# Ничего не сдали, отметок нет: Фёдоров (прочерк на листе), Романчук (закорючки).

VSEGO_OZHIDAEM = sum(len(z) for _, _, z in SDANO)


def otkryt(put: Path, tolko_chtenie: bool) -> sqlite3.Connection:
    if not put.is_file():
        sys.exit(f"🔴 Базы нет: {put}")
    c = sqlite3.connect(f"file:{put}?mode={'ro' if tolko_chtenie else 'rw'}", uri=True)
    c.row_factory = sqlite3.Row
    c.execute("pragma busy_timeout = 10000")
    c.execute("pragma foreign_keys = on")
    return c


def eto_nasha_baza(c: sqlite3.Connection) -> list[str]:
    bedy = []
    n = c.execute("select count(*) from students where status = 'active'").fetchone()[0]
    if n < 50:
        bedy.append(f"активных школьников {n}, ожидали не меньше 50 — это не та база")
    return bedy


def resolve(c: sqlite3.Connection) -> tuple[dict, dict, list[str]]:
    """Фамилия → id и (листок, метка) → id задачи. Вторым — список бед."""
    bedy: list[str] = []
    shkolniki: dict[str, int] = {}
    for familiya in {f for f, _, _ in SDANO}:
        rows = c.execute(
            "select id from students where surname = ? and status = 'active'",
            (familiya,)).fetchall()
        if len(rows) == 1:
            shkolniki[familiya] = rows[0]["id"]
        elif not rows:
            bedy.append(f"🔴 {familiya}: нет в базе среди активных")
        else:
            bedy.append(f"🔴 {familiya}: в базе {len(rows)} однофамильцев, id не выбрать")
    zadachi: dict[tuple[str, str], int] = {}
    for nomer in LISTKI:
        sh = c.execute("select id from sheets where number = ?", (nomer,)).fetchone()
        if not sh:
            continue
        for pid, label in c.execute("select id, label from problems where sheet_id = ?",
                                    (sh["id"],)):
            zadachi[(nomer, label)] = pid
    return shkolniki, zadachi, bedy


def shag_listki(c: sqlite3.Connection, primenyat: bool,
                otchet: list[str]) -> set[tuple[str, str]]:
    """Заводит листки и задачи. Возвращает то, что ЗАВЕЛОСЬ БЫ при сухом прогоне —
    иначе сухой прогон врёт, будто отметки на новые задачи некуда положить."""
    zaplanirovano: set[tuple[str, str]] = set()
    maks = c.execute("select coalesce(max(ord), 0) from sheets").fetchone()[0]
    for i, (nomer, (nazvanie, sostav)) in enumerate(LISTKI.items(), start=1):
        sh = c.execute("select id from sheets where number = ?", (nomer,)).fetchone()
        if not sh:
            otchet.append(f"листок {nomer} — ЗАВЕСТИ ({len(sostav)} задач)")
            if primenyat:
                c.execute("insert into sheets (number, title, issued_at, ord)"
                          " values (?,?,?,?)", (nomer, nazvanie, "2026-09-03", maks + i))
                sh = c.execute("select id from sheets where number = ?", (nomer,)).fetchone()
            else:
                zaplanirovano.update((nomer, label) for label, _ in sostav)
                continue
        sid = sh["id"]

        # лишние ячейки — только у 16α и только если на них нет отметок
        if nomer == "16α":
            for label in LISHNIE_V_ALFA:
                pr = c.execute("select id from problems where sheet_id = ? and label = ?",
                               (sid, label)).fetchone()
                if not pr:
                    continue
                zanyato = c.execute("select count(*) from marks where problem_id = ?",
                                    (pr["id"],)).fetchone()[0]
                if zanyato:
                    otchet.append(f"⚠ {nomer}.{label}: на ячейке {zanyato} отметок — "
                                  f"НЕ трогаю, разбирать руками")
                    continue
                otchet.append(f"{nomer}.{label} — УДАЛИТЬ (такой задачи в листке нет, "
                              f"отметок на ней нет)")
                if primenyat:
                    c.execute("delete from problems where id = ?", (pr["id"],))

        for j, (label, kind) in enumerate(sostav, start=1):
            est = c.execute("select id, kind, ord from problems where sheet_id = ? and label = ?",
                            (sid, label)).fetchone()
            if not est:
                otchet.append(f"{nomer}.{label} — ЗАВЕСТИ ({kind})")
                zaplanirovano.add((nomer, label))
                if primenyat:
                    c.execute("insert into problems (sheet_id, label, kind, ord)"
                              " values (?,?,?,?)", (sid, label, kind, j))
            elif est["ord"] != j and primenyat:
                c.execute("update problems set ord = ? where id = ?", (j, est["id"]))
    return zaplanirovano


def shag_otmetki(c: sqlite3.Connection, primenyat: bool, otchet: list[str],
                 zaplanirovano: set[tuple[str, str]] | None = None) -> int:
    zaplanirovano = zaplanirovano or set()
    shkolniki, zadachi, bedy = resolve(c)
    otchet.extend(bedy)
    teper = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    novyh = 0
    for familiya, listok, metki in SDANO:
        sid = shkolniki.get(familiya)
        if sid is None:
            continue
        for label in metki:
            pid = zadachi.get((listok, label))
            if pid is None:
                if (listok, label) in zaplanirovano:
                    novyh += 1          # задача заведётся тем же прогоном
                    continue
                otchet.append(f"🔴 {listok}.{label}: такой задачи в базе нет — "
                              f"отметка {familiya} НЕ поставлена")
                continue
            klyuch = f"{sid}-{pid}-{DATA_ZANYATIYA}"
            if c.execute("select 1 from marks where idempotency_key = ?", (klyuch,)).fetchone():
                continue
            novyh += 1
            if primenyat:
                c.execute(
                    "insert into marks (student_id, problem_id, event, teacher_id,"
                    " valid_at, recorded_at, source, note, idempotency_key)"
                    " values (?,?,?,?,?,?,?,?,?)",
                    (sid, pid, "assert", None, f"{DATA_ZANYATIYA}T12:00:00Z", teper,
                     ISTOCHNIK, ZAMETKA, klyuch))
    return novyh


def shag_proverka(c: sqlite3.Connection) -> int:
    """Перечитать ИЗ БАЗЫ то, что должно было лечь, и назвать числом."""
    shkolniki, zadachi, bedy = resolve(c)
    for b in bedy:
        print("  ", b)
    est = 0
    net: list[str] = []
    for familiya, listok, metki in SDANO:
        sid = shkolniki.get(familiya)
        for label in metki:
            pid = zadachi.get((listok, label))
            if sid is None or pid is None:
                net.append(f"{familiya} {listok}.{label} (нет "
                           f"{'школьника' if sid is None else 'задачи'} в базе)")
                continue
            row = c.execute(
                "select id from marks where student_id = ? and problem_id = ?"
                " and idempotency_key = ?", (sid, pid, f"{sid}-{pid}-{DATA_ZANYATIYA}")
            ).fetchone()
            if row:
                est += 1
            else:
                net.append(f"{familiya} {listok}.{label}")
    print(f"\nВНЕСЕНО {est} ОТМЕТОК ИЗ {VSEGO_OZHIDAEM} НА БУМАЖКАХ")
    if net:
        print(f"не легло {len(net)}:")
        for x in net:
            print("   ·", x)
    vsego_v_bazu = c.execute(
        "select count(*) from marks where source = ? and valid_at like ?",
        (ISTOCHNIK, f"{DATA_ZANYATIYA}%")).fetchone()[0]
    print(f"всего строк за {DATA_ZANYATIYA} с source='{ISTOCHNIK}' в базе: {vsego_v_bazu}")
    return 0 if est == VSEGO_OZHIDAEM else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--primenit", action="store_true", help="писать в базу")
    ap.add_argument("--proverka", action="store_true", help="только перечитать и посчитать")
    ap.add_argument("--baza", default=str(BAZA_PO_UMOLCHANIYU))
    ap.add_argument("--razreshit-lokalno", action="store_true",
                    help="снять запрет на базу вне /opt (для прогона на копии)")
    a = ap.parse_args()

    put = Path(a.baza)
    if not str(put).startswith("/opt/") and not a.razreshit_lokalno:
        sys.exit(f"🔴 {put} — это не серверная база. Ноутбучная копия не выкатывается "
                 f"(data/ исключена из vykatka.sh), запись в неё пропадёт. "
                 f"Если это осознанный прогон на копии — добавь --razreshit-lokalno.")

    print(f"база: {put}")
    if a.proverka:
        return shag_proverka(otkryt(put, tolko_chtenie=True))

    c = otkryt(put, tolko_chtenie=not a.primenit)
    bedy = eto_nasha_baza(c)
    if bedy:
        for b in bedy:
            print("🔴", b)
        return 2

    otchet: list[str] = []
    zaplanirovano = shag_listki(c, a.primenit, otchet)
    novyh = shag_otmetki(c, a.primenit, otchet, zaplanirovano)
    if a.primenit:
        c.commit()

    print("\n".join(otchet) if otchet else "состав листков уже верный")
    print(("ПРИМЕНЕНО" if a.primenit else "СУХОЙ ПРОГОН, база не тронута")
          + f" · новых отметок {novyh} из {VSEGO_OZHIDAEM}")
    if a.primenit:
        print("\n── перечитываю из базы ──")
        return shag_proverka(otkryt(put, tolko_chtenie=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
