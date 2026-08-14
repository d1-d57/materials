#!/usr/bin/env python3
"""СЧЁТ НЕЗАКРЫТОГО — одна команда, печатает четыре числа, область — опция.

    python3 _generator/tools/schet_nezakrytogo.py                 # весь реестр
    python3 _generator/tools/schet_nezakrytogo.py <область>        # подмножество

ЗАЧЕМ ЭТОТ ФАЙЛ СУЩЕСТВУЕТ (причина дороже кода — не удалять).

Владелец: «я не готов пользоваться фабрикой, пока не закрыты все отчёты и
инциденты» — и предложил лечение сам: «может быть, сразу после этапа закрытия
сессии выставлять флаг, что вот сейчас нужно пойти и сделать небольшую чистку».

🔴 ПЕЧАТЬ, А НЕ ГЕЙТ — НАРОЧНО. Красное на ста тридцати семи унаследованных
пунктах очереди никто читать не будет (тот же урок, что уже оплачен
`priyomka.py`: гейт, красный на каждом обычном отчёте, отключают первым).
Здесь — только счёт, вызывается ДОПОЛНИТЕЛЬНО из `zakryt_sessiyu.py` и (Ш4
захода `instrument-podklyuchen`, 2026-08-08) из `bootstrap_zahod.py` — вывод
попадает в шапку СВЕЖЕГО захода, а не только печатается в консоль.

🔴 ОБЛАСТЬ (Ш4, 2026-08-08). До этой правки инструмент был сам седьмым
неподключённым — real=0, только фикстур. Причина ровно та же, что у остальных
шести: печатал ОБЩИЙ счёт, который никому не адресован лично («в реестре 137
пунктов» не говорит исполнителю заХода, что из них КАСАЕТСЯ его области).
Область — подстрока пути ИЛИ имени фазы, единая семантика: сверяется с
POSIX-путём файла относительно `_studio/zhurnal/` — путь арки сам является
подстрокой путей своих файлов, поэтому «путь» и «имя фазы» не разные режимы,
а один и тот же фильтр.
⚠ **Сужаются 3 из 4 метрик, и это честно, не поровну.** `uroki_bez_verdikta`/
`punkty_ne_dostavleny` рекурсивно ищут файлы под `ZHURNAL` — фильтр по пути
почти бесплатный. `incidenty_bez_verdikta` фильтруется по тексту КЛЮЧА-класса
(`klassifikaciya()` уже даёт `{класс: [...]}`, класс — текст строки инцидента).
`dolgi_zhiv` (DOLG.md, ВТОРОЙ репозиторий) остаётся ГЛОБАЛЬНЫМ и печатает это
прямо: файл не размечен по записям без дублирования парсера `reviziya_dolgov.py`
— а докстринг ТОГО инструмента прямым текстом запрещает второй парсер одной и
той же вещи («расходятся молча»). Соврать числом дороже, чем не сузить его.

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

Только stdlib.
"""
import argparse
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


def incidenty_bez_verdikta(oblast=None):
    """int — классов без вердикта (сужено `oblast`, если задана — подстрока
    текста класса). None — VERDIKTY.md/INCIDENTY.md недоступны."""
    incidenty = REPO_ROOT / check_incidenty.INCIDENTY_REL
    verdikty = REPO_ROOT / check_incidenty.VERDIKTY_REL
    if not incidenty.is_file() or not verdikty.is_file():
        return None
    klassy = check_incidenty.klassifikaciya(incidenty.read_text(encoding="utf-8"))
    razobrano = check_incidenty.parse_verdikty(verdikty.read_text(encoding="utf-8"))
    nezakryto = [k for k in klassy if k not in razobrano]
    if oblast:
        nezakryto = [k for k in nezakryto if oblast in k]
    return len(nezakryto)


def dolgi_zhiv():
    """int — долгов со СТАТУС: ЖИВ, ВСЕГДА по всему DOLG.md (см. докстринг
    модуля — область здесь не сужает НАМЕРЕННО, не по недосмотру).
    None — DOLG.md недоступен (другой репозиторий)."""
    if not DOLG_PATH.is_file():
        return None
    text = DOLG_PATH.read_text(encoding="utf-8", errors="ignore")
    return len(re.findall(r"СТАТУС:\s*ЖИВ\b", text))


def _pod_oblastyu(f, oblast):
    if not oblast:
        return True
    try:
        rel = f.relative_to(ZHURNAL).as_posix()
    except ValueError:
        rel = str(f)
    return oblast in rel


def uroki_bez_verdikta(oblast=None):
    """int — уроков без ВЕРДИКТ по всем UROKI-FABRIKE.md реестра (сужено
    `oblast`, если задана — подстрока пути файла относительно ZHURNAL)."""
    if not ZHURNAL.is_dir():
        return 0
    n = 0
    for f in ZHURNAL.rglob(check_uroki.UROKI_NAME):
        if not _pod_oblastyu(f, oblast):
            continue
        n += sum(1 for les in check_uroki.lessons_in(f) if not les["verdict"])
    return n


def punkty_ne_dostavleny(oblast=None):
    """int — пунктов очереди `ДОСТАВЛЕНО: нет` по всем kod_*.md реестра
    (сужено `oblast`, та же семантика подстроки пути)."""
    if not ZHURNAL.is_dir():
        return 0
    n = 0
    for f in ZHURNAL.rglob("kod_*.md"):
        if not _pod_oblastyu(f, oblast):
            continue
        n += sum(1 for p in dostavit_urok.punkty_zahoda(f) if not p["метка"])
    return n


def stroka(chislo, kogda_net):
    return str(chislo) if chislo is not None else kogda_net


def otchet(oblast=None, snimok=None):
    """→ готовый текстовый блок (без завершающего перевода строки). Общая
    точка входа для CLI (`main`) и для встраивания в шапку захода
    (`bootstrap_zahod.py`, Ш4) — один текст, не два разных представления.

    🔴 `snimok` — строка-метка «когда снято и чем пересчитать», и она
    ПАРАМЕТР, а не безусловная добавка. Зовущих двое, и правда у них разная:
    в шапке захода (`bootstrap_zahod.py`) четыре числа лежат на диске неделями
    и к моменту прогона стареют — там метка обязательна; в консоли
    (`zakryt_sessiyu.py`, `main`) число свежее по построению, и назвать его
    «снимком при сборке» значило бы соврать в другую сторону. Метку формирует
    ВЫЗЫВАЮЩИЙ (`bootstrap_zahod.snimok_metka`) — здесь второй формы не
    заводится, иначе две копии разъедутся при первой правке формулировки.
    ЦЕНА пропуска замерена 14.08 на живом заходе: вписанный при сборке ноль
    невлитых веток к прогону означал три, и файл противоречил сам себе."""
    inc = incidenty_bez_verdikta(oblast)
    dolg = dolgi_zhiv()
    urok = uroki_bez_verdikta(oblast)
    ochered = punkty_ne_dostavleny(oblast)

    stroki = ["── СЧЁТ НЕЗАКРЫТОГО (печать, не гейт) ──"]
    if snimok:
        stroki.append(snimok)
    if oblast:
        stroki.append(f"Область: «{oblast}» — сужены пункты 1, 3, 4; долги (2) "
                       f"глобальны намеренно (DOLG.md не размечен по записям).")
    stroki.append("Приоритет владельца: разобрать инциденты важнее, потом закрыть "
                   "долги — неразобранный инцидент это повторяющаяся ошибка, долг "
                   "может подождать.")
    stroki.append(f"  1. инцидентов без вердикта             : "
                   f"{stroka(inc, 'н/д — VERDIKTY.md/INCIDENTY.md не найдены')}")
    stroki.append(f"  2. долгов СТАТУС: ЖИВ                  : "
                   f"{stroka(dolg, f'н/д — {DOLG_PATH} недоступен (другой git-репозиторий)')}")
    stroki.append(f"  3. уроков фабрике без ВЕРДИКТ          : {urok}")
    stroki.append(f"  4. пунктов очереди «ДОСТАВЛЕНО: нет»   : {ochered}")
    return "\n".join(stroki)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Счёт незакрытого по реестру заходов — печать, не гейт.")
    ap.add_argument("oblast", nargs="?", default=None,
                     help="подстрока пути ИЛИ имени фазы — сужает пункты 1/3/4; "
                          "не задана — весь реестр")
    a = ap.parse_args(argv)
    print(otchet(a.oblast))
    return 0


if __name__ == "__main__":
    sys.exit(main())
