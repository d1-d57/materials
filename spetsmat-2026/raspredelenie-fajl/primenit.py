#!/usr/bin/env python3
"""Кладёт распределение из СКАЧАННОГО файла обратно в базу.

Замыкает круг: владелец (или Даня) правит файл у себя → присылает → эта команда
переносит его решения в базу → статика сайта пересобирается из базы.

Идемпотентна: второй прогон того же файла ничего не меняет и печатает «изменений 0».
Сначала всегда сухой прогон — он ничего не пишет:

    python3 spetsmat-2026/raspredelenie-fajl/primenit.py <файл.html>
    python3 spetsmat-2026/raspredelenie-fajl/primenit.py <файл.html> --primenit
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from datetime import date
from pathlib import Path

KORNI_BAZY = [
    Path.home() / "Documents/GitHub/spetsmat-bot/data/spetsmat.db",
    Path("/sessions/fervent-beautiful-mccarthy/mnt/GitHub/spetsmat-bot/data/spetsmat.db"),
]
# 🔴 ОБА ДНЯ ОДИНАКОВЫ — решение владельца 04.09. Занятия идут в четверг и субботу,
# и пока преподаватели ходят в оба дня, раскладка одна. Файл несёт ОДНО распределение,
# и оно кладётся в оба слота: иначе суббота молча живёт своей жизнью, а владелец
# правит четверг и думает, что поправил всё.
SLOTY = (1, 2)
OTKRYT = "9999-12-31"


def najti_bazu() -> Path:
    for p in KORNI_BAZY:
        if p.is_file():
            return p
    sys.exit("Не нашёл spetsmat.db")


def prochitat(fajl: Path) -> dict:
    text = fajl.read_text(encoding="utf-8")
    m = re.search(
        r'<script id="dannye" type="application/json">(.*?)</script>', text, re.S
    )
    if not m:
        sys.exit(f"{fajl}: это не файл распределения — блока данных внутри нет")
    return json.loads(m.group(1))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("fajl", type=Path)
    ap.add_argument("--primenit", action="store_true",
                    help="без него — сухой прогон, база не меняется")
    a = ap.parse_args()

    d = prochitat(a.fajl)
    segodnya = date.today().isoformat()
    c = sqlite3.connect(najti_bazu())
    c.row_factory = sqlite3.Row

    kabinet_gruppy = {g["kod"]: g["kabinet"] for g in d["gruppy"]}
    plan: list[tuple[str, str]] = []          # (что делаем, человеческое описание)

    # ── 1. Группы преподавателей
    for p in d["prepodavateli"]:
        est = c.execute("select gruppa from teachers where id = ?", (p["id"],)).fetchone()
        if est and est["gruppa"] != p["gruppa"]:
            plan.append(("teacher", f"{p['imya']}: группа {est['gruppa']} → {p['gruppa']}"))
            if a.primenit:
                c.execute("update teachers set gruppa = ? where id = ?",
                          (p["gruppa"], p["id"]))

    # ── 2. Кабинеты групп на дату занятия
    for kod, kab in kabinet_gruppy.items():
        est = c.execute(
            "select kabinet from kabinet_na_den where data = ? and gruppa = ?",
            (d["data"], kod)).fetchone()
        if (est["kabinet"] if est else None) != kab:
            plan.append(("kabinet", f"группа {kod} на {d['data']}: "
                                    f"{est['kabinet'] if est else '—'} → {kab}"))
            if a.primenit and kab:
                c.execute("insert or replace into kabinet_na_den (data, gruppa, kabinet) "
                          "values (?,?,?)", (d["data"], kod, kab))

    # ── 3. Закрепление школьников
    po = {p["id"]: p for p in d["prepodavateli"]}
    for s in d["shkolniki"]:
        hochu = s["prepodavatel"]
        for SLOT in SLOTY:
            _polozhit(c, s, hochu, SLOT, segodnya, po, kabinet_gruppy, plan, a.primenit)
    if a.primenit:
        c.commit()
    _pechat(plan, a.primenit)
    return 0


def _polozhit(c, s, hochu, SLOT, segodnya, po, kabinet_gruppy, plan, pisat):
        OTKRYT = "9999-12-31"
        stroka = c.execute(
            "select * from enrollment where student_id = ? and slot = ? and valid_to = ?",
            (s["id"], SLOT, OTKRYT)).fetchone()
        est = stroka["teacher_id"] if stroka else None
        if est == hochu:
            return

        imya = f"{s['familiya']} {s['imya']}"
        kto = lambda t: po.get(t, {}).get("imya", "—") if t else "не назначен"
        den = {1: "чт", 2: "сб"}.get(SLOT, str(SLOT))
        plan.append(("enrollment", f"{den}  {imya}: {kto(est)} → {kto(hochu)}"))
        if not pisat:
            return

        # 🔴 ОСВОБОДИТЬ БУДУЩЕЕ, А НЕ ТОЛЬКО ЗАКРЫТЬ ОТКРЫТУЮ СТРОКУ.
        # У ушедших преподавателей строки закрыты БУДУЩЕЙ датой (valid_to
        # 2026-09-05 при сегодняшнем 09-04). Открытой строки нет, а интервал ещё
        # тянется — и вставка новой падала о триггер перекрытия. Поэтому режем
        # ВСЁ, что заходит за сегодня: сегодняшнее и позже — удаляем, начатое
        # раньше — подрезаем сегодняшним днём.
        if stroka is not None and stroka["valid_from"] == segodnya and hochu is not None:
            c.execute("update enrollment set teacher_id = ?, room = ? where id = ?",
                      (hochu, kabinet_gruppy.get(po[hochu]["gruppa"]) or stroka["room"],
                       stroka["id"]))
            return
        for r in c.execute(
            "select id, valid_from from enrollment "
            "where student_id = ? and slot = ? and valid_to > ?",
            (s["id"], SLOT, segodnya)).fetchall():
            if r["valid_from"] >= segodnya:
                c.execute("delete from enrollment where id = ?", (r["id"],))
            else:
                c.execute("update enrollment set valid_to = ? where id = ?",
                          (segodnya, r["id"]))
        if hochu is not None:
            c.execute(
                "insert into enrollment (student_id, teacher_id, room, slot, valid_from, valid_to)"
                " values (?,?,?,?,?,?)",
                (s["id"], hochu, kabinet_gruppy.get(po[hochu]["gruppa"]) or "000",
                 SLOT, segodnya, OTKRYT))

def _pechat(plan, primenit):
    vidy = {}
    for v, _ in plan:
        vidy[v] = vidy.get(v, 0) + 1
    print(("ПРИМЕНЕНО" if primenit else "СУХОЙ ПРОГОН, база не тронута")
          + f" · изменений {len(plan)} " + (str(vidy) if plan else ""))
    for _, opisanie in plan:
        print("   " + opisanie)


if __name__ == "__main__":
    raise SystemExit(main())
