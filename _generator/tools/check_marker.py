#!/usr/bin/env python3
"""Гейт маркера: файл-заход или хэндофф обязан быть рождён генератором.

ЗАЧЕМ ЭТОТ ФАЙЛ СУЩЕСТВУЕТ (не удалять причину — она дороже кода).

За одну сессию трижды нарушилась одна дисциплина: документ-заход или хэндофф
создавался РУКАМИ мимо генератора (`bootstrap_zahod.py` / `sdelat_handoff.py`).
Оба генератора теперь ставят в собранный файл маркер-комментарий, но на его
ОТСУТСТВИЕ до сих пор не краснело ничто — маркер был меткой без потребителя.
Этот скрипт — потребитель: он не даёт закоммитить новый файл-заход/хэндофф
без маркера. Обойти можно только явным `git commit --no-verify` — то есть
громко, не молча (KONSTITUCIYA §11).

КОГО СУДИТ. Только НОВЫЕ файлы коммита (`--diff-filter=A`), и только те,
которые ОБЪЯВЛЯЮТ себя заходом или хэндоффом — признак ЛЮБОЙ из двух:
  * по имени: корень `kod` · `handoff` · `peredacha` · `zahod` (РЕГИСТРО-
    НЕЗАВИСИМО), за которым следует необязательный ОДИН разделитель —
    дефис ИЛИ подчёркивание ИЛИ вовсе ничего — и любой хвост до `.md`.
    Ловит и старые формы (`kod_*.md`, `HANDOFF-*.md`), и новые
    (`handoff-poisk-syuzheta.md`, `peredacha-START.md`,
    `zahod_perenos-biblioteki.md`, голый `HANDOFF.md` без суффикса).
    Заведомый компромисс (решение владельца 2026-08-11): файл вида
    `zahody-ocheredi.md` (список заходов, а не заход) тоже попадёт под
    суд — ложное срабатывание тут дешевле пропуска.
  * по содержимому первых ~30 строк: заголовок «# Канал исполнителя —» ·
    строка, НАЧИНАЮЩАЯСЯ с «## КОНТРАКТ ЗОНЫ» · заголовок «# ХЭНДОФФ»
Оба признака нужны: имя обходится переименованием (ровно так и вышел один из
трёх сегодняшних промахов), содержимое — тем, что рукописный файл может не
скопировать шапку. Вместе они закрывают обе дыры; ложное срабатывание тут
дешевле пропуска — на чужой `.md` чекер просто не посмотрит.

ЧТО ТРЕБУЕТ. Один из двух маркеров-комментариев в первых ШЕСТИ строках файла:
    <!-- собран bootstrap_zahod.py -->
    <!-- собран sdelat_handoff.py -->
Нет ни одного → ❌, exit 1. Текст красного называет путь и чем чинить.

🔴 ШЕСТЬ СТРОК, А НЕ ПЯТЬ — вопреки первоначальной формулировке задания.
ДО-верификатор (независимый субагент, задача — сессия `zapret-rukopisnyh`,
2026-08-11) и собственная проверка по живому дереву нашли: `sdelat_handoff.py`
кладёт маркер СТРОКОЙ 6, после пяти строк YAML-фронтматтера (`---` / `tab:` /
`status:` / `poryadok: 0` / `---`) — подтверждено на всех живых `HANDOFF-*.md`
с маркером, включая калибровочный `2026-08-10_dizajn-i-metriki/
HANDOFF-2026-08-11.md`. Порог «пять» ловил бы СОБСТВЕННЫЙ обязан-промолчать
калибровочный файл в ❌ уже на первом прогоне. `bootstrap_zahod.py` кладёт
маркер строкой 3 — внутри окна что с пятью, что с шестью; окно расширено
только под вторую форму, без домысливания дальнейшего запаса.

Режим и молчание. Явные пути — приоритет; без путей и с `--staged` —
автовыбор `git diff --cached --diff-filter=A --name-only`. Чисто → молчит
ПОЛНОСТЬЮ (rc=0) — идиома `check_uroki.py`, и она не зависит от `--staged`:
здоровый файл, переданный явным путём без флага, тоже обязан дать пустой
вывод, иначе шум на каждый коммит его отключат (RESHENIYA Р31).

ДОКСТРИНГ ОБЯЗАН ЧЕСТНО НАЗВАТЬ СЛЕПЫЕ ЗОНЫ (клауза 4, образец —
`check_kartoteka.py`). Их четыре:
  1. судятся только НОВЫЕ файлы — существующие `kod_*.md` без маркера
     проходят молча ВСЕГДА (осознанная граница, не недоделка: см. область
     задания в `kod_zapret.md`);
  2. маркер подделывается печатью одной строки — чекер ловит забывчивость,
     а не злой умысел, и не должен читаться как защита от второго;
  3. чекер не судит СОДЕРЖАНИЕ: заход с маркером и пустой задачей для него
     зелёный (содержание судят `check_zahod.py` и `check_sborki.py`);
  4. признак «заход/хэндофф» по имени охватывает регистр и разделитель
     (заход `kod_ohvat.md`, решение владельца 2026-08-11), но НЕ шапку-
     заголовок: это расширение сознательно не делалось. Рукописный файл
     с заголовком, набранным обычным дефисом вместо «—» (U+2014), или с
     совсем неузнаваемым именем (мимо всех четырёх корней) под признак не
     подпадёт и пройдёт молча, даже будучи заходом/хэндоффом по сути.
     Четыре корня — `kod` · `handoff` · `peredacha` · `zahod` — те же, что
     назвал заход `kod_zapret.md`; новых корней `kod_ohvat.md` не добавлял
     (не его решение).

Запуск:
    python3 _generator/tools/check_marker.py --staged        # staged, автовыбор
    python3 _generator/tools/check_marker.py <путь.md> ...   # явные файлы
Код возврата: 0 — чисто (или судить нечего), 1 — есть нарушения (годится в
ворота). Обойти: `git commit --no-verify` (не дыра — придётся напечатать
руками, а значит уже не молча).
"""
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]  # .../materials

# Корень (регистронезависимо) + необязательный ОДИН разделитель (`-`/`_`/
# ничего) + любой хвост до `.md`. Ловит `kod_*.md`, `HANDOFF-*.md`, а также
# `handoff-poisk-syuzheta.md`, `peredacha-START.md`,
# `zahod_perenos-biblioteki.md`, голый `HANDOFF.md`. Корней ровно четыре —
# расширять список не в этом заходе (см. докстринг, слепая зона 4).
NAME_RE = re.compile(r"^(?:kod|handoff|peredacha|zahod)[_-]?.*\.md$", re.IGNORECASE)
# Префиксный, не точный матч — «## КОНТРАКТ ЗОНЫ» в живых файлах несёт хвост
# («(обязателен — не удалять; вписан Cowork)»), точное равенство строки не
# совпало бы НИ НА ОДНОМ реальном файле (находка ДО-верификатора).
CONTENT_PREFIXES = ("# Канал исполнителя —", "## КОНТРАКТ ЗОНЫ", "# ХЭНДОФФ")
CONTENT_WINDOW = 30
MARKER_WINDOW = 6
MARKERS = ("<!-- собран bootstrap_zahod.py -->", "<!-- собран sdelat_handoff.py -->")


def declares_itself(path):
    """Признак «заход/хэндофф»: по имени ИЛИ по содержимому первых 30 строк."""
    if NAME_RE.match(path.name):
        return True
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()[:CONTENT_WINDOW]
    except OSError:
        return False
    return any(line.startswith(p) for line in lines for p in CONTENT_PREFIXES)


def has_marker(path):
    """Один из двух маркеров-комментариев в первых MARKER_WINDOW строках."""
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()[:MARKER_WINDOW]
    except OSError:
        return False
    return any(m in line for line in lines for m in MARKERS)


def staged_added_md():
    """Пути `.md`, ДОБАВЛЕННЫЕ этим коммитом (`--diff-filter=A`). Пусто — не в
    git-контексте или ничего не добавлено; это не ошибка.

    `-z` — как у `check_kartoteka.staged_md()`: без него не-ASCII путь уезжает
    в C-экранировке и выпадает из фильтра `.endswith(".md")`.

    🔴 Фикстуры самого гейта (`_generator/tools/fixtures/marker/`) отсюда
    ИСКЛЮЧЕНЫ — тот же приём, что у `check_uroki.staged_files()`, и по той же
    причине: среди них НАРОЧНО лежат `ZAHOD-*.md`/`HANDOFF-*.md`-подобные
    рукописные ловушки без маркера — иначе коммит САМИХ фикстур в свою же
    зону валил бы этот же хук. Явно переданный путь (`PROGNAT.sh`) проверяется
    по-прежнему: фильтр только для автоподбора из индекса.
    """
    try:
        out = subprocess.run(
            ["git", "--no-optional-locks", "diff", "--cached", "--name-only",
             "-z", "--diff-filter=A"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    return [REPO_ROOT / p for p in out.split("\0")
            if p.endswith(".md") and "/fixtures/" not in "/" + p]


def rel(p):
    try:
        return p.relative_to(REPO_ROOT)
    except ValueError:
        return p  # файл вне репо (ручной прогон на калибровке) — печатаем как есть


def main(argv):
    # `--help`/`-h` — тот же контракт, что у соседей: rc=0 И непустой вывод.
    if argv and argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    staged = "--staged" in argv
    explicit = [Path(a).resolve() for a in argv if a != "--staged"]
    paths = explicit if explicit else (staged_added_md() if staged else [])

    targets = [p for p in paths if p.is_file() and declares_itself(p)]
    broken = [p for p in targets if not has_marker(p)]

    if not broken:
        return 0

    print("❌ ЗАХОД/ХЭНДОФФ БЕЗ МАРКЕРА ГЕНЕРАТОРА — создан в обход "
          "bootstrap_zahod.py / sdelat_handoff.py:\n", file=sys.stderr)
    for p in broken:
        print(f"  {rel(p)}\n      ↳ нет ни одного из двух маркеров в первых "
              f"{MARKER_WINDOW} строках", file=sys.stderr)
    print(f"\nСудимо файлов: {len(targets)}, без маркера: {len(broken)}, "
          f"с маркером: {len(targets) - len(broken)}.", file=sys.stderr)
    print("\nЧини одним из двух — оба законных:", file=sys.stderr)
    print("  • содержание уже написано руками мимо генератора — пересобери "
          "каркас `bootstrap_zahod.py` (заход) или `sdelat_handoff.py` "
          "(хэндофф) и перенеси текст в оставленные `<...>`: содержание "
          "после генерации дописывается руками, это норма;", file=sys.stderr)
    print("  • файл не заход и не хэндофф, а совпал по имени/шапке случайно — "
          "переименуй или убери спутавшие признаки.", file=sys.stderr)
    print("\nПроскочить: git commit --no-verify (можно; но уже не молча).",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
