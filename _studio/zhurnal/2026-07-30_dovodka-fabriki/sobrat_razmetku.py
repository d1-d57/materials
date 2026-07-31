#!/usr/bin/env python3
"""СБОРЩИК РАЗМЕТКИ — склеивает скелет с вердиктами и САМ считает покрытие.

    python3 .../sobrat_razmetku.py vladelca   # ярусы этажа продукта
    python3 .../sobrat_razmetku.py chisla     # числа с контекстом
    python3 .../sobrat_razmetku.py osi        # оси этажа процесса

ЗАЧЕМ (причина дороже кода — не удалять).

Модель дописывает ТОЛЬКО вердикт: `id<TAB>ярус<TAB>материя`. Всё остальное —
адрес, заголовок, источник, арифметика покрытия — берётся с диска. Поэтому:

1. Адрес не проходит через модель и не может быть искажён. Пункт критерия
   «проверь 10 адресов грепом» становится не нужен: копирования нет.
2. Арифметику покрытия (сколько на ярус, сколько не легло, сходится ли сумма)
   считает скрипт. Модель не умеет складывать 1379 строк и не должна.
3. Скрипт КРАСНЕЕТ (exit 1) на браке, который иначе виден только глазами:
   пропущенный id, неизвестный ярус, «не ложится» без причины, дубль id.

Только stdlib.
"""
import sys
from collections import Counter
from pathlib import Path

ARKA = Path(__file__).resolve().parent

YARUSY = {"0": "замысел", "1": "порционность", "2": "читаемость",
          "3": "ориентир", "процесс": "этаж процесса", "не ложится": "—"}
MATERII = {"время", "кадр", "рисунок", "доказательство", "—", ""}
FORMY = {"ориентир", "WARN", "гейт"}


def sohranit_hvost(path: Path, zagolovok: str) -> str:
    """Достать из существующего файла раздел, который писала МОДЕЛЬ.

    🔴 ЦЕНА, оплачено в ночь на 01.08. Скрипт перезаписывал файл целиком, и
    каждый прогон молча съедал `## РАЗБОР` — главный артефакт захода. Пачка 1
    предсказала это в плане и спасала раздел через `/tmp`; пачка 2 назвала себя
    «первым потерпевшим» и спасала уже два чужих раздела (31 КБ разбора и 9 КБ
    конфликтующих чисел). Финальный шлюз в `noch-2.sh` — то есть МОЙ шлюз —
    прогнал сборку после всех пачек и снёс разбор насовсем.

    Вывод, который дороже кода: инструмент, требующий ручного обходного манёвра
    от каждого, кто им пользуется, — это не инструмент, а ловушка. Сохранение
    обязано быть внутри, а не в инструкции.
    """
    if not path.exists():
        return ""
    t = path.read_text(encoding="utf-8")
    i = t.find(zagolovok)
    return t[i:] if i >= 0 else ""


def chitat_tsv(path: Path):
    if not path.exists():
        sys.exit(f"❌ нет файла {path.name} — заход его не создал")
    rows = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        rows.append((n, line.split("\t")))
    return rows


def sverit_id(skelet_ids, verdikt_ids, brak):
    net = [i for i in skelet_ids if i not in verdikt_ids]
    lishnie = [i for i in verdikt_ids if i not in skelet_ids]
    dubli = [i for i, c in Counter(verdikt_ids).items() if c > 1]
    if net:
        brak.append(f"без вердикта осталось {len(net)} записей: {net[:8]}…")
    if lishnie:
        brak.append(f"вердикт на несуществующий id ({len(lishnie)}): {lishnie[:8]}")
    if dubli:
        brak.append(f"дубли id в вердиктах ({len(dubli)}): {dubli[:8]}")


def rezhim_vladelca(brak):
    skelet = {r[0]: r for _, r in chitat_tsv(ARKA / "skelet-vladelca.tsv")}
    verdikt = chitat_tsv(ARKA / "verdikt-vladelca.tsv")
    vd = {}
    for n, r in verdikt:
        if len(r) < 2:
            brak.append(f"verdikt-vladelca.tsv:{n} — меньше двух полей")
            continue
        gid, yarus = r[0].strip(), r[1].strip()
        mat = r[2].strip() if len(r) > 2 else "—"
        prich = r[3].strip() if len(r) > 3 else ""
        if yarus not in YARUSY:
            brak.append(f"строка {n}: неизвестный ярус {yarus!r} (id {gid})")
        if mat not in MATERII:
            brak.append(f"строка {n}: неизвестная материя {mat!r} (id {gid})")
        if yarus == "1" and mat in ("—", ""):
            brak.append(f"строка {n}: ярус 1 без материи (id {gid})")
        if yarus == "не ложится" and len(prich) < 10:
            brak.append(f"строка {n}: «не ложится» без причины (id {gid})")
        vd[gid] = (yarus, mat, prich)
    sverit_id(list(skelet), [r[0].strip() for _, r in verdikt], brak)

    out = ["# РАЗМЕТКА КОРПУСА ВЛАДЕЛЬЦА ПО ЯРУСАМ", "",
           "> Собрано `sobrat_razmetku.py` из `skelet-vladelca.tsv` + "
           "`verdikt-vladelca.tsv`. Руками не править: правь вердикт и пересобери.",
           "", "| id | ярус | материя | заголовок | АДРЕС |", "|---|---|---|---|---|"]
    schet, spor, ne_leglo = Counter(), 0, []
    for gid, r in skelet.items():
        y, m, p = vd.get(gid, ("—", "—", ""))
        schet[y] += 1
        # Спорность помечают ДВУМЯ способами, и второй родился из дефекта этого
        # же скрипта: формат `1?`, который велел заход, скрипт отвергал как
        # неизвестный ярус, и все четыре пачки согласованно перешли на префикс
        # `СПОРНО:` в поле причины. Счётчик видел только первый способ и печатал
        # «спорных 0» — то самое число, которое заход сам называет подозрительным.
        # Реально их было 285 из 1379.
        if y.endswith("?") or "?" in m or p.startswith(("СПОРНО", "СОМНЕНИЕ")):
            spor += 1
        if y == "не ложится":
            ne_leglo.append((gid, r[2], p))
        out.append(f"| {gid} | {y} | {m} | {r[2]} | `{r[3]}` |")
    (ARKA / "RAZMETKA-VLADELCA.md").write_text("\n".join(out) + "\n", encoding="utf-8")

    vsego = len(skelet)
    pok = ["# ПОКРЫТИЕ КАРКАСА — арифметика, посчитанная скриптом", "",
           "> Числа считает `sobrat_razmetku.py`, не модель. Разбор и выводы "
           "заход дописывает НИЖЕ этой таблицы, в разделе «## РАЗБОР».", "",
           f"Записей в корпусе: **{vsego}**", "",
           "| ярус | что это | записей | доля |", "|---|---|---|---|"]
    for y, name in YARUSY.items():
        n = schet.get(y, 0)
        pok.append(f"| {y} | {name} | {n} | {100 * n / vsego:.1f} % |")
    pok += [f"| — | БЕЗ ВЕРДИКТА | {schet.get('—', 0)} | "
            f"{100 * schet.get('—', 0) / vsego:.1f} % |", "",
            f"Сумма: **{sum(schet.values())}** (обязана равняться {vsego})", "",
            f"Помечено спорными: **{spor}**", "",
            "## Гипотеза аналитика ПО ГРУППАМ против факта ПО ЗАПИСЯМ", "",
            "| | продукт | процесс | не легло |", "|---|---|---|---|",
            "| гипотеза (`AKSIOMATIKA-karkas.md §2`) | 1067 | 151 | 161 |",
            f"| факт по записям | {sum(schet.get(y, 0) for y in '0123')} | "
            f"{schet.get('процесс', 0)} | {len(ne_leglo)} |", "",
            "⚠ Доля яруса отражает то, на что владелец смотрел, а не важность "
            "яруса (`AKSIOMATIKA-karkas.md §1`). Ярус с малой долей может быть несущим.",
            "", f"## НЕ ЛОЖИТСЯ — {len(ne_leglo)} записей", ""]
    for gid, zag, p in ne_leglo:
        pok.append(f"- `{gid}` {zag} — **{p}**")
    hvost = sohranit_hvost(ARKA / "POKRYTIE-karkasa.md", "## РАЗБОР")
    pok += ["", hvost if hvost else "## РАЗБОР — заполняет заход\n"]
    (ARKA / "POKRYTIE-karkasa.md").write_text("\n".join(pok) + "\n", encoding="utf-8")
    return f"размечено {vsego - schet.get('—', 0)} из {vsego}, не легло {len(ne_leglo)}, спорных {spor}"


def rezhim_chisla(brak):
    skelet = {r[0]: r for _, r in chitat_tsv(ARKA / "skelet-chisla.tsv")}
    verdikt = chitat_tsv(ARKA / "verdikt-chisla.tsv")
    vd = {}
    for n, r in verdikt:
        if len(r) < 3:
            brak.append(f"verdikt-chisla.tsv:{n} — нужно три поля: id, масштаб, форма")
            continue
        gid, masshtab, forma = r[0].strip(), r[1].strip(), r[2].strip()
        if len(masshtab) < 10:
            brak.append(f"строка {n}: пустой или куцый МАСШТАБ (id {gid}) — "
                        "число без контекста в гейт не идёт")
        if forma not in FORMY:
            brak.append(f"строка {n}: форма {forma!r} не из {sorted(FORMY)} (id {gid})")
        vd[gid] = (masshtab, forma)
    sverit_id(list(skelet), [r[0].strip() for _, r in verdikt], brak)

    out = ["# ЧИСЛА ВЛАДЕЛЬЦА С КОНТЕКСТОМ ПРИМЕНИМОСТИ", "",
           "> Собрано скриптом. `ФОРМА: ориентир` — значение по умолчанию: "
           "число без контекста в гейт не идёт (`AKSIOMATIKA-karkas.md §3, ярус 3`).",
           "", "| id | ЧИСЛО | ПРИ КАКОМ МАСШТАБЕ | ФОРМА | ОТКУДА |",
           "|---|---|---|---|---|"]
    formy = Counter()
    for gid, r in skelet.items():
        m, f = vd.get(gid, ("—", "—"))
        formy[f] += 1
        out.append(f"| {gid} | {r[1]} | {m} | {f} | `{r[2]}` |")
    hvost = sohranit_hvost(ARKA / "CHISLA-s-kontekstom.md", "## КОНФЛИКТУЮЩИЕ")
    out += ["", hvost if hvost else "## КОНФЛИКТУЮЩИЕ — заполняет заход\n"]
    (ARKA / "CHISLA-s-kontekstom.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    return f"чисел {len(skelet)}, по формам: {dict(formy)}"


def rezhim_osi(brak):
    skelet = {r[0]: r for _, r in chitat_tsv(ARKA / "skelet-ispolnitelej.tsv")}
    verdikt = chitat_tsv(ARKA / "verdikt-osej.tsv")
    vd = {}
    for n, r in verdikt:
        if len(r) < 2:
            brak.append(f"verdikt-osej.tsv:{n} — меньше двух полей")
            continue
        gid, os_ = r[0].strip(), r[1].strip()
        prich = r[2].strip() if len(r) > 2 else ""
        if os_ == "не ложится" and len(prich) < 10:
            brak.append(f"строка {n}: «не ложится» без причины (id {gid})")
        vd[gid] = (os_, prich)
    sverit_id(list(skelet), [r[0].strip() for _, r in verdikt], brak)

    out = ["# РАЗМЕТКА КОРПУСА ИСПОЛНИТЕЛЕЙ ПО ОСЯМ", "",
           "> Собрано скриптом из `skelet-ispolnitelej.tsv` + `verdikt-osej.tsv`.",
           "", "| id | ось | файл | заголовок | АДРЕС |", "|---|---|---|---|---|"]
    schet = Counter()
    for gid, r in skelet.items():
        o, p = vd.get(gid, ("—", ""))
        schet[o] += 1
        out.append(f"| {gid} | {o} | {r[1]} | {r[2]} | `{r[3]}` |")
    out += ["", "## СЧЁТ ПО ОСЯМ", "", "| ось | записей |", "|---|---|"]
    for o, n in schet.most_common():
        out.append(f"| {o} | {n} |")
    out += ["", f"Сумма: **{sum(schet.values())}** из **{len(skelet)}**", "",
            "⚠ Порядок отражает частоту в отчётах исполнителей, а не важность оси "
            "(`AKSIOMATIKA-karkas.md §1`).", ""]
    (ARKA / "RAZMETKA-OSEJ.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    return f"размечено {len(skelet) - schet.get('—', 0)} из {len(skelet)}"


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("vladelca", "chisla", "osi"):
        sys.exit("нужен режим: vladelca | chisla | osi")
    brak = []
    itog = {"vladelca": rezhim_vladelca, "chisla": rezhim_chisla,
            "osi": rezhim_osi}[sys.argv[1]](brak)
    print(itog)
    if brak:
        print(f"\n❌ БРАК — {len(brak)} претензий:", file=sys.stderr)
        for b in brak[:25]:
            print("  ·", b, file=sys.stderr)
        sys.exit(1)
    print("✅ вердикты собраны без брака")
