#!/usr/bin/env python3
"""Собирает САМОДОСТАТОЧНЫЙ HTML-файл распределения — один файл, без сервера.

Зачем. Правит распределение один человек (Даня). Городить под это сервер, туннель
и роли — дороже задачи; туннель к тому же умирал сегодня дважды. Файл лежит у него
на диске, работает офлайн, ничего не деплоится.

Круг: владелец правит своих → «Скачать файл» → шлёт Дане → Даня правит всё →
«Скачать файл» → присылает обратно → владелец выкладывает на сайт.
На каждом шаге ездит ОДИН файл: выгрузка отдаёт новый самодостаточный HTML.

Запуск из корня materials/:
    python3 spetsmat-2026/raspredelenie-fajl/sobrat.py
"""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import date
from pathlib import Path

KORNI_BAZY = [
    Path.home() / "Documents/GitHub/spetsmat-bot/data/spetsmat.db",
    Path("/sessions/fervent-beautiful-mccarthy/mnt/GitHub/spetsmat-bot/data/spetsmat.db"),
]
TUT = Path(__file__).resolve().parent
SHABLON = TUT / "shablon.html"
VYHOD = TUT / "raspredelenie.html"

DATA_ZANYATIYA = "2026-09-05"

# 🔴 Группа у ТРЁХ УШЕДШИХ записана инициалами старшего, а не кодом группы.
# Это не догадка: ДМ = Даня Макаров, НС = Наталья Стрелкова, ИЯ = Иван Яковлев —
# ровно старшие трёх групп. Чиним на чтении, базу не трогаем.
POCHINKA_GRUPPY = {"ДМ": "Д", "НС": "Н", "ИЯ": "В"}

# Записи-нелюди в таблице преподавателей: служебная заглушка и дубль Стрелковой.
NE_LYUDI = {"отсутствует", "НС"}

# Предположение ВЛАДЕЛЬЦА, произнесённое 04.09, а не решение сборки.
# Помечается в файле отдельно, чтобы Даня видел разницу.
PREDPOLOZHENIYA: dict = {}   # отменено владельцем 04.09: догадок в файле нет


def najti_bazu() -> Path:
    for p in KORNI_BAZY:
        if p.is_file():
            return p
    sys.exit("Не нашёл spetsmat.db. Проверь пути в KORNI_BAZY.")


def sobrat_dannye() -> dict:
    baza = najti_bazu()
    c = sqlite3.connect(f"file:{baza}?mode=ro", uri=True)
    c.row_factory = sqlite3.Row

    gruppy = {r["kod"]: r["starshij"] for r in c.execute("select kod, starshij from gruppy")}
    kabinety = {
        r["gruppa"]: r["kabinet"]
        for r in c.execute(
            "select gruppa, kabinet from kabinet_na_den where data = ?", (DATA_ZANYATIYA,)
        )
    }

    prepodavateli = []
    for r in c.execute("select id, name, gruppa, aktiven from teachers order by name"):
        if r["name"] in NE_LYUDI:
            continue
        gruppa = POCHINKA_GRUPPY.get(r["gruppa"], r["gruppa"])
        prepodavateli.append(
            {
                "id": r["id"],
                "imya": r["name"],
                "gruppa": gruppa,
                "aktiven": bool(r["aktiven"]),
            }
        )

    # Действующее закрепление: открытая строка первого слота.
    zakreplenie = {
        r["student_id"]: r["teacher_id"]
        for r in c.execute(
            "select student_id, teacher_id from enrollment "
            "where slot = 1 and valid_to = '9999-12-31'"
        )
    }
    # 🔴 А вот ЗАКРЫТЫЕ строки выбрасывать нельзя, и на этом я один раз уже ошибся.
    # Когда преподаватель ушёл, его строки закрыли датой — вместе с единственным
    # следом того, В КАКОЙ ГРУППЕ ребёнок был. Без него восемь детей выглядят
    # «ничьими вообще», хотя группа у них известна и менять её незачем.
    byloe = {}
    for r in c.execute(
        "select student_id, teacher_id from enrollment "
        "where slot = 1 and valid_to <> '9999-12-31' order by valid_to, id"
    ):
        byloe[r["student_id"]] = r["teacher_id"]

    aktivnye_id = {p["id"] for p in prepodavateli if p["aktiven"]}
    po_id = {p["id"]: p for p in prepodavateli}

    shkolniki = []
    for r in c.execute(
        "select id, surname, name, class from students "
        "where status = 'active' order by surname, name"
    ):
        tid = zakreplenie.get(r["id"])
        # Закрепление на УШЕДШЕГО — это отсутствие принимающего, а не принимающий.
        # Ровно так дети и потерялись: строка есть, человека за ней нет.
        if tid is not None and tid not in aktivnye_id:
            tid = None
        if tid is None:
            byvshij = po_id.get(byloe.get(r["id"]), {})
            shkolniki.append(
                {
                    "id": r["id"],
                    "familiya": r["surname"],
                    "imya": r["name"],
                    "klass": r["class"],
                    "prepodavatel": None,
                    "gruppa": byvshij.get("gruppa"),
                    "otkuda": byvshij.get("imya"),
                }
            )
            continue
        shkolniki.append(
            {
                "id": r["id"],
                "familiya": r["surname"],
                "imya": r["name"],
                "klass": r["class"],
                "prepodavatel": tid,
                "gruppa": po_id.get(tid, {}).get("gruppa"),
                "otkuda": None,
            }
        )

    return {
        "data": DATA_ZANYATIYA,
        "sobrano": date.today().isoformat(),
        "gruppy": [
            {"kod": k, "starshij": gruppy[k], "kabinet": kabinety.get(k)}
            for k in ("В", "Д", "Н")
        ],
        "prepodavateli": prepodavateli,
        "shkolniki": shkolniki,
        "predpolozheniya": PREDPOLOZHENIYA,
    }


def bez_predzapolneniya(d: dict) -> dict:
    """Ничего не расставляем за человека.

    🔴 Прежняя версия раскидывала сирот по группам сама и помечала «авто». Владелец
    отменил: «автопредположение — это пример бессмысленной траты времени», «не должно
    быть лишнего». Ребёнок без принимающего показывается как «не назначен» — и всё.
    """
    for s in d["shkolniki"]:
        s.pop("avto", None)
    return d


def main() -> int:
    d = bez_predzapolneniya(sobrat_dannye())
    shablon = SHABLON.read_text(encoding="utf-8")
    blob = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
    if "/*ДАННЫЕ*/" not in shablon:
        sys.exit("В шаблоне нет метки /*ДАННЫЕ*/ — вставлять некуда.")
    VYHOD.write_text(shablon.replace("/*ДАННЫЕ*/", blob), encoding="utf-8")

    net = [s for s in d["shkolniki"] if s["prepodavatel"] is None]
    print(f"собран {VYHOD}  ({VYHOD.stat().st_size // 1024} КБ)")
    print(f"школьников {len(d['shkolniki'])} · преподавателей активных "
          f"{sum(1 for p in d['prepodavateli'] if p['aktiven'])}")
    print(f"не назначены: {len(net)} — " + ", ".join(s["familiya"] for s in net))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
