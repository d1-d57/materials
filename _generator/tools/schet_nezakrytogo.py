#!/usr/bin/env python3
"""СЧЁТ НЕЗАКРЫТОГО — одна команда, БЕЗ аргументов, печатает четыре числа.

    python3 _generator/tools/schet_nezakrytogo.py

ЗАЧЕМ ЭТОТ ФАЙЛ СУЩЕСТВУЕТ (причина дороже кода — не удалять).

Владелец: «я не готов пользоваться фабрикой, пока не закрыты все отчёты и
инциденты» — и предложил лечение сам: «может быть, сразу после этапа закрытия
сессии выставлять флаг, что вот сейчас нужно пойти и сделать небольшую чистку».

🔴 ПЕЧАТЬ, А НЕ ГЕЙТ — НАРОЧНО. Красное на ста тридцати семи унаследованных
пунктах очереди никто читать не будет (тот же урок, что уже оплачен
`priyomka.py`: гейт, красный на каждом обычном отчёте, отключают первым).
Здесь — только счёт, вызывается ДОПОЛНИТЕЛЬНО из `zakryt_sessiyu.py`.

🔴 ПОРЯДОК СТРОК — ПРИОРИТЕТ ВЛАДЕЛЬЦА, НАЗВАННЫЙ ЧИСЛАМИ, А НЕ СЛОВАМИ:
«разобрать инциденты важнее, потом закрыть долги» — неразобранный инцидент
это повторяющаяся ошибка, долг может подождать. Инциденты печатаются первой
строкой, долги — второй.

Ничего не пишет и не гейтит — ТОЛЬКО чтение и печать. Переиспользует разбор
уже существующих инструментов (не пишет второй парсер одной и той же вещи —
в этом репозитории они уже расходились молча):
  * инциденты/уроки — классификация и вердикты `check_incidenty.py`;
  * уроки фабрике   — `check_uroki.lessons_in()`;
  * очередь заходов — `dostavit_urok.punkty_zahoda()` (публичный вход, тот же,
    что зовёт Г8 `priyomka.py`);
  * долги           — прямое чтение `DOLG.md` (другой git-репозиторий, см.
    `check_uroki.DOLG_PATH` и ## ПЛАН захода `kod_zamykanie-reestrov.md`).

🔴 БЕЗ argparse/sys.argv НАРОЧНО: у инструмента нет входа, который может быть
кривым, — единственный вызов без аргументов сам себе доказательство. Это же
выводит файл из-под требования `check_tool_contract.py` про
спутник-фикстуру для разбора входа (её просто нечему проверять).

Только stdlib.
"""
# TOOL-CONTRACT: no-input — инструмент не разбирает вход вовсе (см. докстринг
# выше): у вызова без аргументов нет кривой формы, которую стоило бы ловить
# фикстурой.
import os
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
REPO_ROOT = TOOLS.parents[1]
ZHURNAL = REPO_ROOT / "_studio" / "zhurnal"

sys.path.insert(0, str(TOOLS))
import check_incidenty  # noqa: E402
import check_uroki  # noqa: E402
import dostavit_urok  # noqa: E402

DOLG_PATH = Path(os.environ.get("CHECK_UROKI_DOLG") or check_uroki.DOLG_PATH)


def incidenty_bez_verdikta():
    """int — классов без вердикта. None — VERDIKTY.md/INCIDENTY.md недоступны."""
    incidenty = REPO_ROOT / check_incidenty.INCIDENTY_REL
    verdikty = REPO_ROOT / check_incidenty.VERDIKTY_REL
    if not incidenty.is_file() or not verdikty.is_file():
        return None
    klassy = check_incidenty.klassifikaciya(incidenty.read_text(encoding="utf-8"))
    razobrano = check_incidenty.parse_verdikty(verdikty.read_text(encoding="utf-8"))
    return len([k for k in klassy if k not in razobrano])


def dolgi_zhiv():
    """int — долгов со СТАТУС: ЖИВ. None — DOLG.md недоступен (другой репозиторий)."""
    if not DOLG_PATH.is_file():
        return None
    text = DOLG_PATH.read_text(encoding="utf-8", errors="ignore")
    return len(re.findall(r"СТАТУС:\s*ЖИВ\b", text))


def uroki_bez_verdikta():
    """int — уроков без ВЕРДИКТ: по всем UROKI-FABRIKE.md реестра."""
    if not ZHURNAL.is_dir():
        return 0
    n = 0
    for f in ZHURNAL.rglob(check_uroki.UROKI_NAME):
        n += sum(1 for les in check_uroki.lessons_in(f) if not les["verdict"])
    return n


def punkty_ne_dostavleny():
    """int — пунктов очереди `ДОСТАВЛЕНО: нет` по всем kod_*.md реестра."""
    if not ZHURNAL.is_dir():
        return 0
    n = 0
    for f in ZHURNAL.rglob("kod_*.md"):
        n += sum(1 for p in dostavit_urok.punkty_zahoda(f) if not p["метка"])
    return n


def stroka(chislo, kogda_net):
    return str(chislo) if chislo is not None else kogda_net


def main():
    inc = incidenty_bez_verdikta()
    dolg = dolgi_zhiv()
    urok = uroki_bez_verdikta()
    ochered = punkty_ne_dostavleny()

    print("── СЧЁТ НЕЗАКРЫТОГО (печать, не гейт) ──")
    print("Приоритет владельца: разобрать инциденты важнее, потом закрыть долги — "
          "неразобранный инцидент это повторяющаяся ошибка, долг может подождать.")
    print(f"  1. инцидентов без вердикта            : "
          f"{stroka(inc, 'н/д — VERDIKTY.md/INCIDENTY.md не найдены')}")
    print(f"  2. долгов СТАТУС: ЖИВ                 : "
          f"{stroka(dolg, f'н/д — {DOLG_PATH} недоступен (другой git-репозиторий)')}")
    print(f"  3. уроков фабрике без ВЕРДИКТ:         : {urok}")
    print(f"  4. пунктов очереди «ДОСТАВЛЕНО: нет»  : {ochered}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
