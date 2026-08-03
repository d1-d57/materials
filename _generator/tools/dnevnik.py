#!/usr/bin/env python3
"""ГЕЙТ ПОЛНОТЫ ДНЕВНИКА — краснеет, когда реплика владельца в дневник не попала.

    python3 _generator/tools/dnevnik.py proverit <папка-арки> [--transcript <путь.jsonl>]
    python3 _generator/tools/dnevnik.py zapis    <папка-арки> --tekst "<текст>" [--repliki S1a2b-В03,S1a2b-В04]

ЗАЧЕМ ЭТОТ ФАЙЛ СУЩЕСТВУЕТ (причина дороже кода — не удалять).

`zakryt_sessiyu.py` выгружает реплики владельца из транскрипта, но разносит их
по дневнику человек. Пока разнос держится на внимательности аналитика, он течёт:
независимая вычитка 03.08 нашла СЕМЬ потерь за одну сессию при том, что дневник
вёлся по ходу и считался полным. Выгрузка эту дыру не закрывает — она даёт
сырьё, а не сверку. Здесь закрыто последнее звено: непопадание реплики в
дневник КРАСНЕЕТ КОМАНДОЙ.

🔴 ГЛАВНОЕ ПРОЕКТНОЕ РЕШЕНИЕ УНАСЛЕДОВАНО У `zakryt_sessiyu.py`:
инструмент НЕ РЕШАЕТ, что важно. Покрытие — это НАЛИЧИЕ НОМЕРА РЕПЛИКИ в тексте
`SESSIYA.md`, где угодно, хоть в HTML-комментарии. Никакого сопоставления «по
смыслу»: гейт, который сам судит о важности, потеряет ровно то, что теряет
человек, — сказанное вскользь. Аналитик разносит и ставит номер; гейт считает
номера.

🔴 НОМЕР НЕСЁТ ИДЕНТИФИКАТОР СЕССИИ: `S<4 символа имени транскрипта>-В<NN>`.
Без него нумерация двух сессий в одном дневнике сталкивается, и вторая сессия
«покрывает» реплики первой своими номерами — тихая поломка ровно того вида,
против которого инструмент и построен (ловушка 5 фикстуры).

🔴 РАЗБОР НЕ КОПИРУЕТСЯ: `najti_transcript` и `razobrat` импортируются из
`zakryt_sessiyu.py`. Две копии разбора разъедутся на первом же изменении формата
транскрипта, и разъедутся МОЛЧА — сверка начнёт считать не те реплики, которые
выгружены.

Молчит при полном покрытии (`KONSTITUCIYA` Р31): гейт, который шумит зря,
отключат.

Только stdlib.
"""
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

# Разбор берём у выгрузки, а не повторяем. Путь — от этого файла, а не от cwd:
# гейт зовут и из корня репо, и из хука, и из фикстуры.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from zakryt_sessiyu import najti_transcript, razobrat  # noqa: E402

DNEVNIK = "SESSIYA.md"


def id_sessii(tr: Path) -> str:
    """Идентификатор сессии для номера реплики — первые 4 символа имени файла."""
    return tr.stem[:4]


def nomer(sid: str, i: int) -> str:
    # Три знака НАРОЧНО: на сотне реплик `В{:02d}` перестаёт быть фиксированной
    # шириной (В01..В99, но В100), а сессии такого размера уже рядом. Старых
    # номеров в дневниках нет (проверено, их там ноль) — миграция не нужна.
    return "S{}-В{:03d}".format(sid, i)


def pokryta(tekst_dnevnika: str, nom: str) -> bool:
    """Номер найден в дневнике.

    Граница справа обязательна: без неё `S1a2b-В10` считался бы покрытым
    строкой `S1a2b-В100`. На сессии в сотню реплик это дало бы ЛОЖНО-ЗЕЛЁНЫЙ
    гейт — худший исход для инструмента, который ловит потери.
    """
    return re.search(re.escape(nom) + r"(?!\d)", tekst_dnevnika) is not None


def put_dnevnika(arka_arg: str) -> Path:
    arka = Path(arka_arg).resolve()
    if not arka.is_dir():
        sys.exit("❌ нет папки арки: {}".format(arka))
    d = arka / DNEVNIK
    if not d.is_file():
        sys.exit("❌ в арке нет дневника {}: {}".format(DNEVNIK, d))
    return d


def repliki_vladelca(yavnyj_transcript):
    """Реплики владельца + идентификатор сессии. Пустой список — это отказ."""
    tr = najti_transcript(yavnyj_transcript)
    vladelec, _analitik, vsego, neponyatnyh = razobrat(tr)
    if not vladelec:
        sys.exit("❌ в транскрипте {} не найдено ни одной реплики владельца "
                 "({} записей, нераспознано {}). Сверять нечего — и это НЕ «всё "
                 "покрыто»: формат изменился, чинить разбор в `zakryt_sessiyu.py`."
                 .format(tr.name, vsego, neponyatnyh))
    return tr, vladelec


def cmd_proverit(args) -> int:
    d = put_dnevnika(args.arka)
    tr, vladelec = repliki_vladelca(args.transcript)
    sid = id_sessii(tr)
    tekst = d.read_text(encoding="utf-8", errors="ignore")

    nepokrytye = [(nomer(sid, i), t) for i, t in enumerate(vladelec, 1)
                  if not pokryta(tekst, nomer(sid, i))]
    vsego_replik = len(vladelec)
    pokryto = vsego_replik - len(nepokrytye)

    if not nepokrytye:
        return 0                                    # Р31: полное покрытие — молча

    # 🔴 ОХВАТ В САМОМ ВЕРДИКТЕ. «Непокрытых нет» без чисел — не вердикт:
    # «проверено 2 из 9» и «проверено 9 из 9» выглядят одинаково.
    print("❌ дневник неполон: покрыто {} из {} реплик владельца".format(pokryto, vsego_replik))
    print("   транскрипт: {}".format(tr))
    print("   дневник:    {}".format(d))
    print()
    for nom, t in nepokrytye:
        print("── {}".format(nom))
        print("   {}".format(t[:300].replace("\n", " ")))
        print()
    print("Разнести в {} и пометить номером — например строкой:".format(DNEVNIK))
    print("    python3 {} zapis {} --tekst \"<суть>\" --repliki {}"
          .format(Path(__file__).name, args.arka, ",".join(n for n, _ in nepokrytye[:2])))
    return 1


def cmd_zapis(args) -> int:
    d = put_dnevnika(args.arka)
    if not args.tekst.strip():
        sys.exit("❌ пустой --tekst: запись без содержания дневник только засоряет")

    repliki = [s.strip() for s in (args.repliki or "").split(",") if s.strip()]
    stamp = datetime.now().strftime("%Y-%m-%d, %H:%M")

    blok = ["", "## {} — запись".format(stamp), "", args.tekst.strip(), ""]
    if repliki:
        # Маркер — в HTML-комментарии: он не мешает чтению дневника, но именно
        # его считает `proverit`. Дневник ведёт человек, метку ставит инструмент.
        blok += ["<!-- РЕПЛИКИ РАЗНЕСЕНЫ: {} -->".format(" · ".join(repliki)), ""]

    # Дописываем в КОНЕЦ и ничего не переписываем: в дневнике лежит знание,
    # которое никуда больше не уехало.
    staroe = d.read_text(encoding="utf-8", errors="ignore")
    hvost = "" if staroe.endswith("\n") else "\n"
    with d.open("a", encoding="utf-8") as f:
        f.write(hvost + "\n".join(blok) + "\n")

    print("✅ запись добавлена в {}".format(d))
    if repliki:
        print("   помечены реплики: {}".format(" · ".join(repliki)))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Гейт полноты дневника арки")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("proverit", help="сверить дневник с репликами владельца из транскрипта")
    p.add_argument("arka", help="папка арки с SESSIYA.md")
    p.add_argument("--transcript", help="путь к .jsonl (иначе ищется самый свежий)")
    p.set_defaults(func=cmd_proverit)

    z = sub.add_parser("zapis", help="дописать запись в дневник, пометив разнесённые реплики")
    z.add_argument("arka", help="папка арки с SESSIYA.md")
    z.add_argument("--tekst", required=True, help="текст записи")
    z.add_argument("--repliki", help="номера разнесённых реплик через запятую")
    z.set_defaults(func=cmd_zapis)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
