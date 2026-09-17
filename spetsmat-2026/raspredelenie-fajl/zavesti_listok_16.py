#!/usr/bin/env python3
"""Заводит три листка 16 (A · α · ℵ), их задачи и отметки за 3 сентября 2026.

Состав задач снят из `materials/spetsmat-2026/listki/16*-derevya.pdf` и `16-derevya.tex`,
а не придуман. Отметки — с семи фотографий владельца, расшифровка и все оговорки в
`materials/spetsmat-2026/konduit-3-sentyabrya.md`.

🔴 ТРИ ЛИСТКА, А НЕ ТРИ ВЕРСИИ ОДНОГО. Слова владельца 05.09: «классу одновременно
выдаётся три разных листка, три разных подборки, у них разные задачи». Совпадение
номеров ничего не значит: `16A.3` и `16α.3` — разные задачи.

Идемпотентен: второй прогон печатает «изменений 0».
    python3 spetsmat-2026/raspredelenie-fajl/zavesti_listok_16.py            # сухой
    python3 spetsmat-2026/raspredelenie-fajl/zavesti_listok_16.py --primenit
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

KORNI_BAZY = [
    Path.home() / "Documents/GitHub/spetsmat-bot/data/spetsmat.db",
    Path("/sessions/fervent-beautiful-mccarthy/mnt/GitHub/spetsmat-bot/data/spetsmat.db"),
]
DATA_ZANYATIYA = "2026-09-03"
# 🔴 `source` в схеме — ПЕРЕЧЕНЬ: кнопка · фото · голос · импорт. Это каналы приёма,
# и «фото» заведён ровно под наш случай: преподаватель снял бумажку, её расшифровали.
# Подробность уходит в `note`, а не в `source`.
ISTOCHNIK = "фото"

# ── СОСТАВ ЛИСТКОВ ────────────────────────────────────────────────────────────
# Знак после номера: ◦ обязательная · ★ звезда · † письменная сдача · без знака обычная.
# 🔴 РЕШЕНИЕ СБОРКИ, НАЗВАННОЕ ВСЛУХ: `†` — это способ сдачи, а не сложность, и в схеме
# отдельного вида под него нет. Кладём такие задачи как «обязательная». Если владелец
# захочет различать — это отдельная колонка, а не подмена вида.
LISTKI = {
    "16A": ("16A. Деревья", [
        ("1а", "обязательная"), ("1б", "обязательная"),
        ("2", "обязательная"), ("3", "обязательная"), ("4", "обязательная"),
        ("5", "обязательная"),
        ("6а", "обязательная"), ("6б", "обязательная"),
        ("7а", "обязательная"), ("7б", "обязательная"), ("7в", "обязательная"),
        ("8", "обязательная"),
        ("9", "обязательная"),
        ("10а", "обязательная"), ("10б", "обязательная"),
        ("11а", "обязательная"), ("11б", "обязательная"), ("11в", "обязательная"),
        ("12", "звезда"),
        ("13а", "звезда"), ("13б", "звезда"),
    ]),
    "16α": ("16α. Деревья", [
        ("1", "обязательная"), ("2", "обязательная"), ("3", "обязательная"),
        ("4", "обязательная"), ("5", "обязательная"), ("6", "обязательная"),
        ("7", "обязательная"), ("8", "обязательная"),
        ("10а", "обязательная"), ("10б", "обязательная"), ("10в", "обязательная"),
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

# ── ОТМЕТКИ ЗА 3 СЕНТЯБРЯ ─────────────────────────────────────────────────────
# (фамилия, листок, [задачи])  — id школьников берутся из базы по фамилии, не вписаны.
SDANO = [
    ("Агаркова",   "16A", ["1а", "1б", "2", "3", "4", "5", "6а", "6б"]),
    ("Чапышев",    "16A", ["1а", "1б", "2", "3", "4", "5"]),
    ("Ордян",      "16A", ["1а", "1б", "11а"]),
    ("Будылин",    "16A", ["1а", "1б", "2"]),
    ("Болотин",    "16A", ["1а", "1б", "2"]),
    ("Долгирева",  "16A", ["1а", "1б"]),
    ("Бочарова",   "16A", ["1а"]),
    ("Цикунов",    "16α", ["3", "4", "6"]),
    ("Пономарев",  "16α", ["2"]),
    ("Симонова",   "16α", ["2", "3", "4"]),
    ("Кудряшов",   "16α", ["3", "2"]),
    # 🔴 Алеф — прочитан владельцем 05.09: «Ваня Фефелов сдавал алеф, у Даниловой Веры тоже».
    # Знак на бумаге, похожий на «N», — это ℵ. Задача −1 с пунктами а, б, в есть только
    # в алефе; на этом обе записи и сошлись.
    ("Фефелов",    "16ℵ", ["-1а", "-1б", "-1в"]),
    ("Данилова",   "16ℵ", ["-1а", "-1б"]),
]

# 🔴 ПРАВИЛО ВЛАДЕЛЬЦА 05.09: «если стоит 1–5, значит полностью всё сдано; 7 — тоже
# значит, что сдано всё». Диапазон и одиночный номер берут задачу ЦЕЛИКОМ, со всеми
# пунктами. Пункты выписывают только когда сдана ЧАСТЬ — как «11 аб» у той же Глебовой.
SPORNOE = [
    ("Глебова", "16A", ["1а", "1б", "2", "3", "4", "5", "7а", "7б", "7в", "11а", "11б"]),
    # Вторая строка той же бумажки. Фамилия восстановлена сравнением со списком класса:
    # на Н в классе ровно ОДНА фамилия — Николаева. Хвост «-ва», частокол палочек от
    # «-икол-», первая буква как латинская N. Сравнивать было больше не с чем.
    ("Николаева", "16A", ["12", "1а"]),
]


def najti_bazu() -> Path:
    for p in KORNI_BAZY:
        if p.is_file():
            return p
    sys.exit("Не нашёл spetsmat.db")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--primenit", action="store_true")
    ap.add_argument("--s-glebovoj", action="store_true",
                    help="внести Глебову и Николаеву — записи, разобранные с владельцем 05.09")
    a = ap.parse_args()

    c = sqlite3.connect(najti_bazu())
    c.row_factory = sqlite3.Row
    plan: list[str] = []
    teper = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # ── листки
    maks = c.execute("select coalesce(max(ord), 0) from sheets").fetchone()[0]
    for i, (nomer, (nazvanie, zadachi)) in enumerate(LISTKI.items(), start=1):
        est = c.execute("select id from sheets where number = ?", (nomer,)).fetchone()
        if not est:
            plan.append(f"листок {nomer} — завести ({len(zadachi)} задач)")
            if a.primenit:
                c.execute("insert into sheets (number, title, issued_at, ord) values (?,?,?,?)",
                          (nomer, nazvanie, DATA_ZANYATIYA, maks + i))
        sid = (est or c.execute("select id from sheets where number = ?", (nomer,)).fetchone())
        if sid is None:
            continue
        for j, (label, kind) in enumerate(zadachi, start=1):
            if not c.execute("select 1 from problems where sheet_id = ? and label = ?",
                             (sid["id"], label)).fetchone():
                plan.append(f"  задача {nomer}.{label} ({kind})")
                if a.primenit:
                    c.execute("insert into problems (sheet_id, label, kind, ord) values (?,?,?,?)",
                              (sid["id"], label, kind, j))

    # ── отметки
    zapisi = SDANO + (SPORNOE if a.s_glebovoj else [])
    for familiya, listok, zadachi in zapisi:
        st = c.execute("select id from students where surname = ? and status = 'active'",
                       (familiya,)).fetchone()
        if not st:
            plan.append(f"🔴 {familiya} — НЕТ В БАЗЕ, отметки пропущены")
            continue
        sh = c.execute("select id from sheets where number = ?", (listok,)).fetchone()
        if not sh:
            plan.append(f"🔴 листок {listok} ещё не заведён — отметки {familiya} пропущены")
            continue
        for label in zadachi:
            pr = c.execute("select id from problems where sheet_id = ? and label = ?",
                           (sh["id"], label)).fetchone()
            if not pr:
                plan.append(f"🔴 {listok}.{label} — такой задачи нет, {familiya} пропущен")
                continue
            klyuch = f"{st['id']}-{pr['id']}-{DATA_ZANYATIYA}"
            if c.execute("select 1 from marks where idempotency_key = ?", (klyuch,)).fetchone():
                continue
            plan.append(f"отметка: {familiya} — {listok}.{label}")
            if a.primenit:
                c.execute(
                    "insert into marks (student_id, problem_id, event, valid_at, recorded_at,"
                    " source, note, idempotency_key) values (?,?,?,?,?,?,?,?)",
                    (st["id"], pr["id"], "assert", f"{DATA_ZANYATIYA}T12:00:00Z", teper,
                     ISTOCHNIK, "бумажка 03.09, расшифрована аналитиком; см. spetsmat-2026/konduit-3-sentyabrya.md", klyuch))

    if a.primenit:
        c.commit()

    print(("ПРИМЕНЕНО" if a.primenit else "СУХОЙ ПРОГОН, база не тронута")
          + f" · изменений {len(plan)}")
    for s in plan:
        print("   " + s)
    if not a.s_glebovoj:
        print("\n⚠ Глебова и Николаева не внесены — нужен флаг --s-glebovoj.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
