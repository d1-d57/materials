#!/usr/bin/env python3
"""Счётчик git-долга СРАЗУ ПО ВСЕМ репозиториям рядом — с порогом и красным.

ЗАЧЕМ ЭТОТ ФАЙЛ СУЩЕСТВУЕТ (причина дороже кода — не удалять).

Требование владельца 2026-08-16 дословно: «как только накопилось больше четырёх
заявок на влитие — сразу должно краснеть. И тогда мы просто остановимся и вольём
руками… В нормальной ситуации может работать параллельно много заходов, до
трёх-четырёх, и они могут оставлять после себя четыре невлитых ветки. Но пять
невлитых веток — значит долг образовался, и это очень плохо. Надо, чтобы был
инструмент, который считает это, и сразу по всем репозиториям».

ЧЕМ ОТЛИЧАЕТСЯ ОТ Г10 `priyomka.py`. Тот судит репозитории ЗОНЫ конкретного
захода и живёт внутри приёмки. Этот — про машину целиком: он находит соседние
репозитории сам и зовётся откуда угодно, в том числе владельцем без всякого
захода. Общего кода у них нет нарочно: Г10 читает зону из контракта, здесь зоны
нет вовсе.

🔴 ПОРОГ ПО НЕВЛИТЫМ НАЗВАН ВЛАДЕЛЬЦЕМ ЧИСЛОМ — ПЯТЬ. Он не выведен из замера и
не подлежит подгонке: четыре параллельных захода — норма работы, пятая невлитая
ветка означает, что влитие перестало происходить вовсе.

🔴 ПОРОГИ ПО «ВНЕ GIT» И «НЕ ВЫВЕЗЕНО» ВЫВЕДЕНЫ ИЗ ЗАМЕРА, И ЗАМЕР НАЗВАН.
Снимок 2026-08-16 (`python3 _generator/tools/dolg_repozitoriev.py`, пересними
сам — числу в комментарии верить нельзя): `materials` — 8 путей вне git,
`disciplina` — 11 и 3 невывезенных, `matema-fest` — 25 вне git,
`matemdigest-map` — 66 вне git и 17 невывезенных, `digest` — нули.
  · ВНЕ GIT → 15. Восемь-одиннадцать путей — это ХВОСТ ОДНОЙ СЕССИИ живого
    репозитория (индекс Cowork, автологи), и краснеть на нём значит краснеть
    всегда, то есть быть отключённым в первый же вечер (`Р31`). Пятнадцать —
    выше однодневного хвоста и ниже его удвоения: две сессии подряд без
    коммита уже долг, и это ровно то, что должно быть видно.
  · НЕ ВЫВЕЗЕНО → 10. Сессия оставляет единицы коммитов (замер: 0, 0, 3).
    Десять — это несколько дней работы, которой нет на origin, то есть ровно
    тот случай «работа сделана, а владелец её не видит», оплаченный дважды.
  Оба порога — предложение исполнителя, а не слово владельца, и помечены так же
  в отчёте захода `kod_faza-priyomki.md`: если они шумят, двигать их надо
  ЗАМЕРОМ, а не на глаз.

🔴 СТАРЫЕ ЧУЖИЕ ДОЛГИ — ОТДЕЛЬНАЯ СТРОКА, А НЕ ШУМ. Владелец про `matema-fest`
и «спецмат» сказал прямо: «там много чего не закоммичено, их надо как-то, может
быть, вынести сейчас». Счётчик, который всегда красный из-за чужого архива,
перестают читать — и он не спасёт в тот день, когда покраснеет по делу. Поэтому
есть список выноса: `_studio/docs/kak-delat/DOLG-ISKLYUCHENIA.md`, где у каждого
исключения ОБЯЗАТЕЛЬНЫ причина и дата. Вынесенное печатается ОТДЕЛЬНО и всегда —
скрытый долг перестал бы существовать, а он не перестал.

🔴 ЧУЖИЕ РЕПОЗИТОРИИ ТОЛЬКО ЧИТАЮТСЯ. Инструмент не коммитит, не вливает и не
вывозит нигде и никогда: все команды ниже — read-only, и `--no-optional-locks`
стоит на каждой, потому что обычный `git status` переписывает индекс и роняет
чужой параллельный коммит (`GIT-disciplina §0`).

Запуск:
    python3 _generator/tools/dolg_repozitoriev.py              # печать + вердикт
    python3 _generator/tools/dolg_repozitoriev.py --porog-vetok 1   # проверить, что умеет краснеть
    python3 _generator/tools/dolg_repozitoriev.py --vse       # и вынесенные тоже судить
Код возврата: 0 — порогов никто не перешёл · 1 — долг образовался · 2 — неверный вызов.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]          # .../materials ИЛИ .../materials-wt/<заход>
ISKLYUCHENIA = REPO_ROOT / "_studio/docs/kak-delat/DOLG-ISKLYUCHENIA.md"


def glavnaya_rabochaya():
    """Главная рабочая копия, а НЕ рабочая папка захода.

    🔴 ПОЙМАНО ЖИВЫМ ПРОГОНОМ ПРИ ПЕРВОМ ЖЕ ЗАПУСКЕ, и цена была бы обидной.
    Инструмент лежит в `_generator/tools/`, и `parents[2]` даёт корень ТОГО
    дерева, из которого его позвали. Заход работает в worktree по построению,
    значит `parents[2]` — это `materials-wt/<заход>`, а сосед у него —
    `materials-wt/<другой заход>`: счётчик обошёл четырнадцать РАБОЧИХ ПАПОК
    одного репозитория, посчитал один и тот же долг четырнадцать раз и выдал
    «11 репозиториев за порогом» там, где репозиториев рядом пять. Число,
    которому нельзя верить, хуже отсутствующего: оно выглядит как замер.
    `--git-common-dir` — тот же приём, каким `git_zona.py` решает ровно эту
    задачу для очереди заявок: у worktree он указывает в общий `.git`.
    """
    r = subprocess.run(["git", "--no-optional-locks", "rev-parse", "--git-common-dir"],
                       cwd=REPO_ROOT, capture_output=True, text=True)
    if r.returncode == 0 and r.stdout.strip():
        obshchij = Path(r.stdout.strip())
        if not obshchij.is_absolute():
            obshchij = (REPO_ROOT / obshchij).resolve()
        return obshchij.parent
    return REPO_ROOT


SOSEDI_HOME = glavnaya_rabochaya().parent                 # .../GitHub

POROG_VETOK = 5        # слово владельца, не замер
POROG_VNE_GIT = 15     # выведено из замера, см. докстринг
POROG_NE_VYVEZENO = 10  # выведено из замера, см. докстринг

RC_DOLG = 1
RC_MISUSE = 2


def git(koren: Path, *args):
    """read-only git в названном дереве. `--no-optional-locks` — не украшение.

    Обычный git переписывает индекс, берёт `.git/index.lock` и роняет
    параллельный ручной коммит владельца; счётчик, который ради печати числа
    ломает чужую работу, вреднее отсутствующего.
    """
    return subprocess.run(["git", "--no-optional-locks", *args],
                          cwd=koren, capture_output=True, text=True)


def repozitorii():
    """Соседние репозитории — папки с `.git`, кроме рабочих папок заходов.

    `*-wt` отсекается по построению: worktree захода — не отдельный
    репозиторий, а вид на тот же самый, и посчитанный дважды долг был бы
    удвоен на ровном месте.
    """
    najdeno = []
    for p in sorted(SOSEDI_HOME.iterdir()):
        if not p.is_dir() or p.name.endswith("-wt") or p.name.startswith("."):
            continue
        if (p / ".git").exists():
            najdeno.append(p)
    return najdeno


def osnovnaya(koren: Path):
    """Имя основной ветки — СНЯТО КОМАНДОЙ, не вписано.

    `arka/mat-kostyak` в `materials` и `main` в остальных: захардкоженное имя
    сделало бы инструмент однорепозиторным ровно там, где он и нужен.
    """
    r = git(koren, "rev-parse", "--abbrev-ref", "HEAD")
    name = r.stdout.strip()
    return name if r.returncode == 0 and name and name != "HEAD" else None


def dolg(koren: Path):
    """(невлитые, вне git, не вывезено, примечания) — три числа и оговорки."""
    prim = []
    baza = osnovnaya(koren)
    nevlitye = []
    if baza:
        # 🔴 `--format`, А НЕ ОБРЕЗКА УКРАШЕНИЙ. `git branch` метит ветку,
        # вычекаученную в рабочей папке, знаком `+`, и снятие декораций через
        # `lstrip("* ")` его не убирало — ровно этот дефект три недели держал
        # сторож невлитых веток слепым (`bootstrap_zahod.nevlityje_vetki`,
        # починено 16.08). Здесь он был бы ещё дороже: заходы ЖИВУТ в worktree,
        # то есть счётчик долга не видел бы как раз должников.
        r = git(koren, "branch", "--no-merged", baza, "--format=%(refname:short)")
        if r.returncode == 0:
            nevlitye = [l.strip() for l in r.stdout.splitlines() if l.strip()]
        else:
            prim.append("невлитые не сняты: " + (r.stderr.strip().splitlines() or ["git молчит"])[0])
    else:
        prim.append("основная ветка не определена (отцепленный HEAD?)")

    r = git(koren, "status", "--porcelain")
    vne_git = len([l for l in r.stdout.splitlines() if l.strip()]) if r.returncode == 0 else 0
    if r.returncode != 0:
        prim.append("вне git не снято")

    ne_vyvezeno = 0
    up = git(koren, "rev-parse", "--abbrev-ref", "@{upstream}")
    if up.returncode == 0:
        r = git(koren, "rev-list", "--count", "@{upstream}..HEAD")
        ne_vyvezeno = int(r.stdout.strip() or 0) if r.returncode == 0 else 0
    else:
        prim.append("ветка не отслеживает origin — вывоз не проверить")
    return nevlitye, vne_git, ne_vyvezeno, prim


def chitat_isklyuchenia():
    """{имя репозитория: (причина, дата)} из списка выноса.

    Формат строки (жёсткий, по нему же и гейт формата ниже):
        - `<репозиторий>` · причина: <почему> · дата: <YYYY-MM-DD>
    Причина и дата обязательны ОБЕ: вынос без причины через месяц неотличим от
    забытого, а без даты — от вечного (`CLAUDE.md` правило 6: отметка «закрыто»
    без даты данных доверия не заслуживает).
    """
    if not ISKLYUCHENIA.is_file():
        return {}, []
    vynos, bitye = {}, []
    # 🔴 КОД-БЛОКИ ПРОПУСКАЮТСЯ. В самом файле стоит ОБРАЗЕЦ формата внутри
    # ```-блока, и без этого пропуска инструмент читал его как настоящую запись
    # и жаловался на собственную документацию (поймано первым живым прогоном).
    # Файл, который нельзя объяснить читателю не нарушив свой же формат, — это
    # формат, который перестанут соблюдать.
    v_bloke = False
    for nomer, stroka in enumerate(ISKLYUCHENIA.read_text(encoding="utf-8").splitlines(), 1):
        s = stroka.strip()
        if s.startswith("```"):
            v_bloke = not v_bloke
            continue
        if v_bloke or not s.startswith("- `"):
            continue
        m = re.match(r"- `([^`]+)`\s*·\s*причина:\s*(.+?)\s*·\s*дата:\s*(\d{4}-\d{2}-\d{2})\s*$", s)
        if not m:
            bitye.append((nomer, s[:70]))
            continue
        vynos[m.group(1)] = (m.group(2), m.group(3))
    return vynos, bitye


def main() -> int:
    ap = argparse.ArgumentParser(
        description="git-долг по всем репозиториям рядом: невлитые ветки, вне git, не вывезено")
    ap.add_argument("--porog-vetok", type=int, default=POROG_VETOK,
                    help=f"порог невлитых веток (по умолчанию {POROG_VETOK} — слово владельца)")
    ap.add_argument("--porog-vne-git", type=int, default=POROG_VNE_GIT,
                    help=f"порог путей вне git (по умолчанию {POROG_VNE_GIT})")
    ap.add_argument("--porog-ne-vyvezeno", type=int, default=POROG_NE_VYVEZENO,
                    help=f"порог невывезенных коммитов (по умолчанию {POROG_NE_VYVEZENO})")
    ap.add_argument("--vse", action="store_true",
                    help="судить и вынесенные репозитории тоже (по умолчанию они "
                         "печатаются, но не краснеют)")
    args = ap.parse_args()
    if min(args.porog_vetok, args.porog_vne_git, args.porog_ne_vyvezeno) < 1:
        print("❌ Порог меньше единицы бессмыслен: он краснел бы на пустом "
              "репозитории. Это НЕВЕРНЫЙ ВЫЗОВ (rc=2), а не найденный долг.")
        return RC_MISUSE

    vynos, bitye = chitat_isklyuchenia()
    repos = repozitorii()
    if not repos:
        print(f"❌ Рядом с {REPO_ROOT} не найдено ни одного репозитория — "
              "считать нечего. Проверь, туда ли смотрит инструмент.")
        return RC_MISUSE

    print(f"═══ git-долг по репозиториям рядом с {SOSEDI_HOME} ═══")
    print(f"Пороги: невлитых ≥{args.porog_vetok} · вне git ≥{args.porog_vne_git} · "
          f"не вывезено ≥{args.porog_ne_vyvezeno}")
    print(f"{'репозиторий':<22}{'невлитых':>10}{'вне git':>10}{'не вывезено':>14}")

    krasnye, vynesennye = [], []
    for koren in repos:
        nevlitye, vne_git, ne_vyvezeno, prim = dolg(koren)
        sudim = args.vse or koren.name not in vynos
        metka = "" if sudim else "  ← вынесен"
        print(f"{koren.name:<22}{len(nevlitye):>10}{vne_git:>10}{ne_vyvezeno:>14}{metka}")
        for p in prim:
            print(f"{'':<22}⚠ {p}")
        if not sudim:
            prichina, data = vynos[koren.name]
            vynesennye.append((koren.name, len(nevlitye), vne_git, ne_vyvezeno, prichina, data))
            continue
        prevysheno = []
        if len(nevlitye) >= args.porog_vetok:
            prevysheno.append(f"невлитых {len(nevlitye)} (≥{args.porog_vetok}): "
                              + ", ".join(nevlitye[:8]))
        if vne_git >= args.porog_vne_git:
            prevysheno.append(f"вне git {vne_git} путей (≥{args.porog_vne_git})")
        if ne_vyvezeno >= args.porog_ne_vyvezeno:
            prevysheno.append(f"не вывезено {ne_vyvezeno} коммитов (≥{args.porog_ne_vyvezeno})")
        if prevysheno:
            krasnye.append((koren.name, prevysheno))

    # 🔴 ВЫНЕСЕННОЕ ПЕЧАТАЕТСЯ ВСЕГДА, ДАЖЕ КОГДА ВСЁ ЗЕЛЁНОЕ. Вынос — это
    # «отложено с причиной и датой», а не «больше не существует»; список,
    # который не видно, через месяц становится враньём в свою пользу.
    if vynesennye:
        print("\n── вынесено из счёта (старые долги чужих проектов) ──")
        for imya, nv, vg, nvyv, prichina, data in vynesennye:
            print(f"   {imya}: невлитых {nv}, вне git {vg}, не вывезено {nvyv}")
            print(f"      причина: {prichina} · дата: {data}")
        print(f"   Список: {ISKLYUCHENIA}")
    if bitye:
        print(f"\n⚠ В списке выноса {len(bitye)} строк(и) не по формату — они НЕ "
              "вынесены и судятся наравне со всеми:")
        for nomer, s in bitye:
            print(f"   строка {nomer}: {s}")
        print("   Формат: - `<репозиторий>` · причина: <почему> · дата: <YYYY-MM-DD>")

    if krasnye:
        print(f"\n🔴 ДОЛГ ОБРАЗОВАЛСЯ — репозиториев за порогом: {len(krasnye)} из "
              f"{len(repos)} (вынесено {len(vynesennye)})")
        for imya, prichiny in krasnye:
            for p in prichiny:
                print(f"   {imya}: {p}")
        print("\n   Владелец про этот случай: «тогда мы просто остановимся и вольём "
              "руками».\n   Влитие — `git_zona.py vlit-v-osnovnuyu <ветка>`, "
              "вывоз — `git_zona.py vyvezti --yes`.")
        return RC_DOLG
    print(f"\n✅ Порогов никто не перешёл — проверено {len(repos) - len(vynesennye)} "
          f"репозиториев из {len(repos)} найденных (вынесено {len(vynesennye)}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
