#!/usr/bin/env python3
"""ГЕЙТ ВЕСА: тяжёлый файл вне git не заводится молча.

    python3 _generator/tools/check_ves.py            # отчёт + код возврата
    python3 _generator/tools/check_ves.py --tiho     # только код возврата
    python3 _generator/tools/check_ves.py --staged   # ворота: что заезжает в git

Код возврата: 0 — чисто, 1 — нашли тяжёлое, 2 — гейт не отработал. В воротах.
Запускать из корня репо. stdlib, без сети, детерминизм (сортировка по весу).

ДВА РЕЖИМА СТЕРЕГУТ РАЗНОЕ, И ПУТАТЬ ИХ НЕЛЬЗЯ.
  · без флага — **место на диске**: что лежит в папке мимо git;
  · `--staged` — **историю**: что заезжает в коммит. Это лечится только
    запретом на входе. Файл, попавший в git, остаётся в нём навсегда: удалишь
    следующим ходом — вес не вернётся, история уже написана.
Первый режим нужен, потому что 5,2 ГБ папки оказались мусором вне git. Второй —
потому что 1,0 ГБ `.git` оказались тем, что в git когда-то ВПУСТИЛИ.

ЗАЧЕМ. К 01.08 папка `materials/` весила 5,2 ГБ при 226 МБ реальной работы.
Разница — не история и не книги, а три кучи, которые никто не заводил решением:
модель Whisper на 2,9 ГБ, скачанная под разовую расшифровку («я предполагал,
что она почистится»), 224 МБ исходных wav при готовых расшифровках рядом и
337 МБ tar-снапшотов, от которых отказались ещё 21.07, но с диска не убрали.
Все три — вне git, то есть невидимы для всех обычных проверок репозитория:
`status` про них молчит, `ls-files` их не знает, диффа они не дают.

Общее у них одно: **каждая куча появилась как «сейчас положу, потом уберу»**.
Разовая уборка это не лечит — через месяц будет новая модель и новые снапшоты.
Лечит то, что краснеет: файл тяжелее порога, лежащий вне git и не названный
в списке известных, обязан быть либо удалён, либо осознанно вписан в список.

ПОЧЕМУ ПОРОГ ИМЕННО 10 МБ. Он обязан быть тих на здоровой папке ПОСЛЕ уборки —
красный на здоровом дереве это ложный гейт, его обойдут, и защита пропадёт
(`_studio/docs/kak-delat/RUKOVODSTVO-zahodami.md`). Проверено прогоном: после
уборки 01.08 выше 10 МБ вне git остаются только книги (легальны, см. ниже) и
четыре файла, вписанные в список известных. Ниже 10 МБ шум начинается сразу.

ПОЧЕМУ КНИГИ НЕ КРАСНЕЮТ НИКОГДА. PDF в `istochniki/` и `biblioteka/` — 166
файлов, 378 МБ — накапливаются ЗАКОННО: владелец держит их ради локального
полнотекстового поиска. Краснеть на каждой новой скачанной книге значит учить
обходить гейт. Поэтому источники считаются отдельным итогом и учитываются не
здесь, а реестром `_studio/zhurnal/_INFRA-git/REESTR-istochnikov.md`.
"""
import subprocess
import sys
from pathlib import Path

KOREN = Path(__file__).resolve().parents[2]
IZVESTNOE = Path(__file__).resolve().parent / "ves_izvestnoe.txt"
POROG = 10 * (1 << 20)          # 10 МБ на диске — обоснование в шапке
POROG_INDEKS = 5 * (1 << 20)    # 5 МБ в индекс — обоснование в proverit_indeks
ISTOCHNIKI = ("istochniki", "biblioteka")   # законно растущие места


def chelovecheski(bajt):
    for edinica, porog in (("ГБ", 1 << 30), ("МБ", 1 << 20), ("КБ", 1 << 10)):
        if bajt >= porog:
            return f"{bajt / porog:.1f} {edinica}"
    return f"{bajt} Б"


def ves_dereva(korzina):
    """Суммарный вес путей (Path) на диске. Пропавшие молча пропускаются."""
    itog = 0
    for p in korzina:
        try:
            itog += p.stat().st_size
        except OSError:
            pass
    return itog


def ves_papki(papka):
    itog = 0
    for p in papka.rglob("*"):
        if p.is_file() and not p.is_symlink():
            try:
                itog += p.stat().st_size
            except OSError:
                pass
    return itog


def trekaemye():
    """Пути в индексе. `--no-optional-locks` ОБЯЗАТЕЛЕН: обычный git берёт
    .git/index.lock и роняет параллельный ручной коммит владельца."""
    vyvod = subprocess.run(
        ["git", "--no-optional-locks", "ls-files", "-z"],
        cwd=KOREN, capture_output=True, text=True)
    if vyvod.returncode != 0:
        print(f"❌ git ls-files упал (rc={vyvod.returncode}) — гейт не отработал")
        sys.exit(2)
    return {s for s in vyvod.stdout.split("\0") if s}


def izvestnye():
    """Список известных тяжёлых файлов вне git. Строка = путь от корня репо;
    после `#` — причина, почему он лежит и почему пока остаётся."""
    if not IZVESTNOE.exists():
        return {}
    spisok = {}
    for stroka in IZVESTNOE.read_text(encoding="utf-8").splitlines():
        golaya = stroka.split("#", 1)[0].strip()
        if golaya:
            prichina = stroka.split("#", 1)[1].strip() if "#" in stroka else ""
            spisok[golaya] = prichina
    return spisok


def istochnik(otn):
    return any(chast in ISTOCHNIKI for chast in Path(otn).parts)


FLAGI = {"--tiho", "--staged"}


def razobrat_vhod(argv):
    """Кривой вход обязан падать ГРОМКО, а не тихо делать не то.

    `"--tiho" in sys.argv` — ровно та мина, что оплачена 23.07: `--help`
    проглотили как имя арки. Здесь опечатка `--tixo` молча дала бы ШУМНЫЙ
    прогон вместо тихого, а в воротах это читается как «гейт отработал».
    Поэтому неизвестный аргумент — rc=2, и он отличается и от 0 (чисто),
    и от 1 (нашли тяжёлое): «гейт не отработал» ≠ «гейт сказал нет».
    """
    lishnee = [a for a in argv[1:] if a not in FLAGI]
    if lishnee:
        print(f"❌ не понимаю аргумент: {' '.join(lishnee)}")
        print(f"   допустимо: {' '.join(sorted(FLAGI))} — и больше ничего")
        print("   python3 _generator/tools/check_ves.py [--tiho] [--staged]")
        sys.exit(2)
    return "--tiho" in argv[1:], "--staged" in argv[1:]


def proverit_indeks(tiho):
    """Режим ворот: тяжёлое НЕ ВПУСКАЕТСЯ в git. Возврат — код для хука.

    ЗАЧЕМ ОТДЕЛЬНО ОТ ОСНОВНОГО РЕЖИМА. Основной смотрит на диск и стережёт
    место. Этот стережёт ИСТОРИЮ — а она не лечится уборкой: файл, попавший в
    коммит, остаётся в `.git` навсегда, даже если удалить его следующим ходом.
    Замер 01.08: из 1026 МБ `.git` — 286 МБ PDF и 258 МБ tar-снапшотов, то есть
    больше половины репозитория составляет то, что когда-то впустили сюда.

    ПОЧЕМУ ПО ВЕСУ, А НЕ ПО РАСШИРЕНИЮ. `.gitignore` уже ловит `*.pdf` в
    `istochniki/`, `*/snapshots/` и `/*.zip` — и всё равно в индексе лежат
    `genkin-itenberg-fomin_len-kruzhki.djvu` (7,5 МБ: книга, но расширение
    другое), `_studio/zhurnal/…/_backup_infra_20260710-043240.zip` (7,4 МБ: zip,
    но не в корне, а правило было `/*.zip`) и `noch-logi/H1-razmetka-osej.jsonl`
    (4,1 МБ: лог прогона). Список расширений всегда отстаёт от жизни на один
    формат — вес не отстаёт никогда.

    ПОЧЕМУ ИСТОЧНИКАМ ЗДЕСЬ ПОБЛАЖКИ НЕТ, в отличие от основного режима. На
    диске книги накапливаются законно; в ИСТОРИИ им делать нечего — это ровно
    те 286 МБ. Книга лежит на диске и живёт в реестре, а не в коммите.
    """
    vyvod = subprocess.run(
        ["git", "--no-optional-locks", "diff", "--cached", "--name-only",
         "-z", "--diff-filter=ACM"],
        cwd=KOREN, capture_output=True, text=True)
    if vyvod.returncode != 0:
        print(f"❌ git diff --cached упал (rc={vyvod.returncode}) — гейт не отработал")
        return 2
    znakomye = izvestnye()
    tyazhelye = []
    for otn in (s for s in vyvod.stdout.split("\0") if s):
        if otn in znakomye:
            continue
        try:
            razmer = (KOREN / otn).stat().st_size
        except OSError:
            continue                      # файл удаляется этим же коммитом
        if razmer >= POROG_INDEKS:
            tyazhelye.append((razmer, otn))
    tyazhelye.sort(reverse=True)

    if not tyazhelye:
        if not tiho:
            print(f"✅ вес: в индекс не лезет ничего тяжелее "
                  f"{chelovecheski(POROG_INDEKS)}")
        return 0
    print(f"🔴 ВЕС: в git заезжает тяжёлое — {len(tyazhelye)} файлов "
          f"(порог {chelovecheski(POROG_INDEKS)}):")
    for razmer, otn in tyazhelye:
        print(f"    {chelovecheski(razmer):>10}  {otn}")
    print()
    print("  Файл, попавший в коммит, остаётся в .git НАВСЕГДА — удаление")
    print("  следующим ходом вес уже не вернёт. Поэтому гейт стоит ЗДЕСЬ.")
    print("  Что делать:")
    print(f"    · книга или статья → ей место на диске и в реестре, а не в git:")
    print(f"      `git restore --staged <путь>` + строка в .gitignore;")
    print(f"    · снапшот/архив/бэкап → его работу уже делает сам git;")
    print(f"    · лог прогона → в git идёт вывод, а не сырой поток;")
    print(f"    · файл правда нужен в истории → впиши строкой С ПРИЧИНОЙ")
    print(f"      в {IZVESTNOE}.")
    return 1


def main():
    tiho, staged = razobrat_vhod(sys.argv)
    if staged:
        return proverit_indeks(tiho)
    treki = trekaemye()
    znakomye = izvestnye()

    novye, znakomye_najdeny, knigi, knigi_ves = [], set(), 0, 0
    for p in KOREN.rglob("*"):
        if not p.is_file() or p.is_symlink():
            continue
        otn = str(p.relative_to(KOREN))
        if otn.startswith(".git/"):
            continue
        try:
            razmer = p.stat().st_size
        except OSError:
            continue
        if razmer < POROG or otn in treki:
            continue
        if istochnik(otn):
            knigi += 1
            knigi_ves += razmer
        elif otn in znakomye:
            znakomye_najdeny.add(otn)
        else:
            novye.append((razmer, otn))
    novye.sort(reverse=True)

    if not tiho:
        vsya = ves_papki(KOREN)
        git = ves_papki(KOREN / ".git")
        rabota = ves_dereva(KOREN / t for t in treki)
        print("ВЕС — три числа")
        print(f"  папка целиком      {chelovecheski(vsya)}")
        print(f"  .git               {chelovecheski(git)}")
        print(f"  трекаемое дерево   {chelovecheski(rabota)}   ← реальная работа")
        print()
        print(f"Порог тяжёлого: {chelovecheski(POROG)}. Вне git и тяжелее порога:")
        print(f"  источники (книги/статьи, растут законно): "
              f"{knigi} файлов, {chelovecheski(knigi_ves)} — учёт в "
              f"_studio/zhurnal/_INFRA-git/REESTR-istochnikov.md")
        print(f"  известные (вписаны в {IZVESTNOE.name}): "
              f"{len(znakomye_najdeny)} из {len(znakomye)}")
        propali = set(znakomye) - znakomye_najdeny
        for otn in sorted(propali):
            print(f"    · в списке есть, на диске НЕТ: {otn} "
                  f"— строку можно убрать, список гниёт")
        print()
        if novye:
            print(f"🔴 НОВОЕ ТЯЖЁЛОЕ ВНЕ GIT — {len(novye)}:")
            for razmer, otn in novye:
                print(f"    {chelovecheski(razmer):>10}  {otn}")
            print()
            print("  Что делать: либо удалить (сперва ДВЕ проверки — "
                  "`git ls-files <путь>` и `git log --all -- <путь>`),")
            print(f"  либо вписать строкой в {IZVESTNOE} С ПРИЧИНОЙ.")
        else:
            print("✅ Нового тяжёлого вне git нет.")
        print()
        print("ЧЕГО ЭТОТ ГЕЙТ НЕ ПРОВЕРЯЕТ — честно:")
        print(f"  · файлы легче {chelovecheski(POROG)}: тысяча мелких файлов "
              "пройдёт мимо целиком;")
        print("  · вес .git — он только печатается. Раздутую историю чинит "
              "git-filter-repo,")
        print("    отдельной операцией с бэкапом, и гейт её не инициирует;")
        print("  · содержимое источников: дубликаты книг, битые PDF и "
              "отсутствие текстового слоя;")
        print("  · оправданность строк в списке известных — их читает человек, "
              "не гейт;")
        print("  · внешние по отношению к репо места (Загрузки, кэши) — "
              "это не его зона.")

    return 1 if novye else 0


if __name__ == "__main__":
    sys.exit(main())
