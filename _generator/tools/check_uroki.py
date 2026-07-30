#!/usr/bin/env python3
"""Гейт уроков фабрике: у каждого урока обязана быть ЦЕНА.

ЗАЧЕМ ЭТОТ ФАЙЛ СУЩЕСТВУЕТ (не удалять причину — она дороже кода).

За трое суток (16–17.07.2026) написано 17 секций «→ фабрика». До канона дошла ОДНА.
Проверено: `git log _studio/docs/` — канон правился один раз, и не про уроки. У фабрики
было ТРИ хука «→ фабрика» (после отчёта · хэндофф · закрытие арки), и втроём они
доставили ~1 урок из ~12.

Разбор (RESHENIYA Р31): хуки были ПРОЗОЙ в .md — правилом, которое можно нарушить
молча. А по закону KONSTITUCIYA §11 такое правило будет нарушено, включая автором.
Ещё одно «теперь точно заносим» стало бы тем же пожеланием в четвёртый раз, поэтому
вместо уговоров — этот скрипт в pre-commit.

ЧТО ОН ЛОВИТ. Ровно одно: урок без строки `ЦЕНА:`. Порог канона дословно — «урок без
цены это наблюдение, ему в канон нельзя» — потому что цена задним числом НЕ
восстанавливается: через день помнишь мораль, но не помнишь, что сломалось.

Урок с `ВЕРДИКТ:` НЕ проверяется: его уже отсудила закрывающая сессия, и она же решала,
настоящая ли цена. Гейт защищает ВХОД в эту сессию, а не её выход. (Оно же лечит и
исторические файлы, где цена написана прозой до появления формата.)

⚠️ ЧЕКЕР СОВРАЛ НА ПЕРВОМ ЗАПУСКЕ — как и `check_kartoteka.py`, трижды. Он объявил браком
все 11 уроков арки teorkat: цена у них есть, но прозой («**Цена — четыре рецидива:**»),
а не строкой `ЦЕНА:`. Соблазн был ослабить регексп до «есть слово цена» — это убило бы
гейт (он перестал бы уметь краснеть). Вместо этого — правило про вердикт выше.

ЧЕГО ОН НЕ ЛОВИТ (сказано честно — клауза 3 гейта, RUKOVODSTVO §Заход):
  * что цена НАСТОЯЩАЯ, а не приписана для галочки;
  * что урок вообще записан — молчание не отличить от «уроков не было»;
  * что урок доехал до канона (это закрытие арки, ARKA §7 п.3).
Скрипт считает строки, а не правду. Правду ловит владелец и свежая сессия.

Проверяет ТОЛЬКО арки, файлы которых есть в этом коммите: чинить старые арки он не
требует и потому не шумит. Молчит, когда всё чисто, — иначе его отключат, и это будет
конец затеи.

Запуск (обычно через pre-commit, но можно руками):
    python3 _generator/tools/check_uroki.py                 # staged-файлы коммита
    python3 _generator/tools/check_uroki.py <путь.md> ...   # явные файлы
Код возврата: 0 — чисто, 1 — есть уроки без цены (годится в ворота).
Обойти можно: `git commit --no-verify`. Это НЕ дыра — закон говорит «нельзя нарушить
МОЛЧА», а не «нельзя нарушить». Обошёл — значит напечатал это руками и знаешь, что делаешь.
"""
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]  # .../materials
UROKI_NAME = "UROKI-FABRIKE.md"
ZAHOD_SECTION = "## УРОКИ ФАБРИКЕ"

HEADING = re.compile(r"^### (.+)$")
# Цена засчитывается и с жирным выделением: `**ЦЕНА: …**` — это то же самое,
# что `ЦЕНА: …`, автор просто подчеркнул её. Гейт судит СУТЬ, а не оформление.
# Цена ошибки прежней строгой формы (21.07): в закрытой арке лежали 7 полноценных
# уроков с настоящей ценой, написанной жирным, — гейт объявил их «уроками без цены»
# и блокировал коммиты ЧУЖИХ заходов. Из-за этого один заход ушёл через --no-verify,
# а аналитик записал в канон ложный урок «гейт штрафует за чужой долг».
# Разделитель после токена — ЛЮБОЙ, не только «: »: гейт судил пунктуацию, а не
# наличие цены, и урок «ЦЕНА обратная, и она названа конкретно: …» был объявлен
# уроком без цены (нашла верификация 30.07). `(?!\w)` — токен «ЦЕНА» ЦЕЛЫМ словом:
# без него «ЦЕНАЛОГ: 5» проходил бы как цена, хотя слово другое.
PRICE = re.compile(r"^\*{0,2}ЦЕНА(?!\w)[^\w]*(.*?)\*{0,2}$")
VERDICT = re.compile(r"^\*{0,2}ВЕРДИКТ: *(.*?)\*{0,2}$")
# Заголовок-плейсхолдер из шаблона (`### <что произошло>`) — не урок, а рыба.
PLACEHOLDER = re.compile(r"^<.*>$")


def staged_files():
    """Файлы в индексе коммита. Пусто — не в git-контексте, это не ошибка.

    🔴 Фикстуры самого гейта (`_generator/tools/fixtures/`) отсюда ИСКЛЮЧЕНЫ.
    Они по своему назначению содержат уроки без цены — иначе не на чем проверить,
    что гейт умеет падать, — и лежат в структуре `zhurnal/<арка>/kod_*.md`, потому
    что скрипт выбирает цели по ней. Для хука это неотличимо от настоящей арки.
    Цена (21.07): в первый же коммит после их появления хук завалил ВСЕ ДЕСЯТЬ
    коммитов плана — репозиторий не мог принять ничего, включая сами фикстуры.
    Явно переданный аргументом путь проверяется по-прежнему: так `PROGNAT.sh`
    гоняет фикстуры и видит их падение. Фильтр только для автоподбора из индекса.
    """
    try:
        out = subprocess.run(
            ["git", "--no-optional-locks", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    return [REPO_ROOT / line for line in out.splitlines()
            if line and "/fixtures/" not in "/" + line]


def targets_from(paths):
    """Какие файлы уроков проверять: UROKI-FABRIKE.md тронутых АРОК + тронутые kod_*.md.

    Арка тронута = в коммите есть ЛЮБОЙ её файл. Тогда её уроки обязаны быть в форме,
    даже если сам файл уроков в этот коммит не попал: иначе гейт молчит ровно тогда,
    когда урок забыли записать.
    """
    found = set()
    for p in paths:
        if p.name.startswith("kod_") and p.suffix == ".md" and p.is_file():
            found.add(p)
        for parent in p.parents:
            if parent.parent.name == "zhurnal" and parent.name != "_TEMPLATE-arka":
                uroki = parent / UROKI_NAME
                if uroki.is_file():
                    found.add(uroki)
                break
    return sorted(found)


def lessons_in(path):
    """[(строка, заголовок)] — уроки БЕЗ цены и БЕЗ вердикта; плюс сколько всего проверено.

    В UROKI-FABRIKE.md уроки лежат в корне файла; в kod_<тема>.md — только внутри
    секции `## УРОКИ ФАБРИКЕ` (иначе `### ` из ПЛАНА/ОТЧЁТА посчитались бы уроками).
    """
    text = path.read_text(encoding="utf-8").splitlines()
    scoped = path.name != UROKI_NAME
    inside = not scoped
    lessons = []
    cur = None

    def flush():
        if cur:
            lessons.append(cur)

    for n, line in enumerate(text, 1):
        if scoped and line.startswith("## "):
            flush()
            cur = None
            inside = line.strip().startswith(ZAHOD_SECTION)
            continue
        if not inside:
            continue
        m = HEADING.match(line)
        if m:
            flush()
            title = m.group(1).strip()
            cur = None if PLACEHOLDER.match(title) else {"line": n, "title": title,
                                                         "price": False, "verdict": False}
            continue
        if not cur:
            continue
        if (mp := PRICE.match(line)) and mp.group(1).strip():
            cur["price"] = True
        elif (mv := VERDICT.match(line)) and mv.group(1).strip():
            cur["verdict"] = True
    flush()
    return lessons


def main(argv):
    paths = [Path(a).resolve() for a in argv] if argv else staged_files()
    broken = []
    checked = 0
    for f in targets_from(paths):
        for les in lessons_in(f):
            if les["verdict"]:
                continue  # уже отсуждён закрывающей сессией — не пересматриваем
            checked += 1
            if not les["price"]:
                broken.append((f, les["line"], les["title"]))

    if not broken:
        return 0

    def rel(p):
        try:
            return p.relative_to(REPO_ROOT)
        except ValueError:
            return p  # файл вне репо (ручной прогон) — печатаем как есть

    print("❌ УРОК БЕЗ ЦЕНЫ — в канон он не пойдёт (RESHENIYA Р31, KONSTITUCIYA §11):\n",
          file=sys.stderr)
    for f, line_no, title in broken:
        print(f"  {rel(f)}:{line_no}\n      ### {title}\n      ↳ нет строки «ЦЕНА: ...»",
              file=sys.stderr)
    print(f"\nПроверено уроков: {checked}, без цены: {len(broken)}.", file=sys.stderr)
    print("Цена = что сломалось и сколько стоило (ходов/заходов/лекций, кто поймал).",
          file=sys.stderr)
    print("Задним числом она не восстанавливается — через день помнишь мораль, а не поломку.",
          file=sys.stderr)
    print("\nЧини одним из двух — оба законных:", file=sys.stderr)
    print("  • дописать «ЦЕНА: ...» под заголовком;", file=sys.stderr)
    print("  • удалить урок — цены нет, значит это наблюдение, а не закон.", file=sys.stderr)
    print("\nПроскочить: git commit --no-verify (можно; но уже не молча).", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
