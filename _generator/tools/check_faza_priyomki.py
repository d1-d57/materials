#!/usr/bin/env python3
"""Гейт фазы приёмки в `pre-commit`: файл-заход с пустой `## ФАЗА ПРИЁМКИ` не коммитится.

ЗАЧЕМ ЭТОТ ФАЙЛ СУЩЕСТВУЕТ (причина дороже кода — не удалять).

Заход `kod_faza-priyomki.md` поставил гейты Г13-Г15 в `priyomka.py`, но не
подключил их никуда: `priyomka.py <файл>` запускают РУКАМИ на приёмке, и до
неё пустой раздел «## ФАЗА ПРИЁМКИ» коммитится молча сколько угодно раз.
Владелец решил дословно: «я бы сделал по максимуму, всё бы закрепил, чтобы
оно всегда краснело и просто у нас всегда всё вывозилось в начале работы. Это
нормально — в начале работы останавливаться и начинать заниматься вывозами».
Этот файл — живая точка вызова, а не только описание в markdown.

🔴 СУДИТ ТОЛЬКО СТЕЙДЖЕННЫЙ файл-заход ЭТОГО коммита, никогда чужой долг:
ночной заход сам назвал ограничитель — хук, краснеющий на ЧУЖОМ долге,
обходят `--no-verify`, и тогда пропадает вся защита разом
(`GIT-disciplina.md §4б-бис`, «ХВОСТ COWORK»). Молчит ПОЛНОСТЬЮ, если в
коммите нет ни одного `kod_*.md` — это идиома `check_uroki.py`/`check_marker.py`.

Переиспользует ТЕ ЖЕ функции, что приёмка (`gate_g13`/`gate_g14`/`gate_g15`
из `priyomka.py`), а не пишет их заново — вторая реализация разъехалась бы
с первой молча.

Судит СТЕЙДЖЕННУЮ версию файла (`git show :<путь>`), а не рабочее дерево:
частично застейдженная правка коммитится ровно тем содержимым, что уехало в
индекс, и гейт обязан видеть то же самое. Явный путь, отсутствующий в
индексе (ручной прогон/фикстура), читается с диска — тем же приёмом, что у
`check_marker.declares_itself()`.

Репозиторий, который судят гейты Г13/Г14 (влитие ветки, живые заявки), —
`priyomka.REPO`: тот же `PRIYOMKA_REPO`-override, что у самой приёмки
(`_resolve_repo()`), второго резолва не заводим — разъедутся молча.

Запуск:
    python3 _generator/tools/check_faza_priyomki.py --staged        # staged, автовыбор
    python3 _generator/tools/check_faza_priyomki.py <путь.md> ...   # явные файлы
Код возврата: 0 — чисто (или судить нечего), 1 — Г13/Г14/Г15 красные хоть на
одном файле. Обойти: `git commit --no-verify` — придётся напечатать руками,
значит уже не молча (`KONSTITUCIYA §11`).
"""
import re
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import priyomka  # noqa: E402 — переиспользуем gate_g13/14/15 и REPO, не дублируем

NAME_RE = re.compile(r"^kod[_-].*\.md$", re.IGNORECASE)

# Три исхода rc (Рычаг 3, `GIT-disciplina.md §5`): 0 — чисто/судить нечего,
# 1 — Г13/Г14/Г15 красные хоть на одном файле, 2 — позвали неверно (явный
# путь не читается ни из индекса, ни с диска). Без кода 2 «дал гейту опечатку
# в пути» и «гейт нашёл дефект» снаружи неотличимы.
RC_OK, RC_DEFECT, RC_MISUSE = 0, 1, 2


def staged_zahody():
    """Пути `kod_*.md`, ЗАТРОНУТЫЕ этим коммитом (add/copy/modify).

    `-z` — без него не-ASCII путь уезжает в C-экранировке и выпадает из
    фильтра по имени (тот же приём, что у `check_marker.staged_added_md()`).
    """
    try:
        out = subprocess.run(
            ["git", "--no-optional-locks", "diff", "--cached", "--name-only",
             "-z", "--diff-filter=ACM"],
            cwd=priyomka.REPO, capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    return [p for p in out.split("\0") if p and NAME_RE.match(Path(p).name)]


def content_for(put_str: str):
    """Стейдженное содержимое пути (`git show :<путь>`), с откатом на диск.

    Откат нужен для явно переданных путей вне индекса (фикстуры, ручной
    прогон на файле, который ещё не `git add`) — то же поведение, что у
    `check_marker.declares_itself()`, читающего с диска напрямую.
    """
    r = subprocess.run(["git", "--no-optional-locks", "show", f":{put_str}"],
                        cwd=priyomka.REPO, capture_output=True, text=True)
    if r.returncode == 0:
        return r.stdout
    p = Path(put_str)
    if not p.is_absolute():
        p = priyomka.REPO / put_str
    if p.is_file():
        return p.read_text(encoding="utf-8", errors="ignore")
    return None


def gates_for(tekst: str):
    return [
        ("Г13 фаза приёмки заполнена, заявки сверены с очередью", *priyomka.gate_g13(tekst)),
        ("Г14 ветка работы названа и её влитие проверено фактом", *priyomka.gate_g14(tekst)),
        ("Г15 отказ git-операции разобран", *priyomka.gate_g15()),
    ]


def main(argv):
    if argv and argv[0] in ("-h", "--help"):
        print(__doc__)
        return RC_OK
    staged = "--staged" in argv
    explicit = [a for a in argv if a != "--staged"]
    if explicit:
        # 🔴 ПОЗВАЛИ НЕВЕРНО, А НЕ «СУДИТЬ НЕЧЕГО» — явный путь, не читающийся
        # ни из индекса, ни с диска, почти всегда опечатка вызывающего (Рычаг 3):
        # молчаливый rc=0 читался бы как «чисто», хотя гейт вообще не смотрел
        # на файл.
        neizvestnye = [a for a in explicit if content_for(a) is None]
        if neizvestnye:
            print(f"❌ ПОЗВАЛИ НЕВЕРНО: путь(и) не читаются ни из индекса, ни с диска: "
                  f"{', '.join(neizvestnye)}", file=sys.stderr)
            return RC_MISUSE
    puti = explicit if explicit else (staged_zahody() if staged else [])
    if not puti:
        return RC_OK

    krasnyh_faylov = 0
    for put in puti:
        tekst = content_for(put)
        plohie = [(nazvanie, msg) for nazvanie, ok, msg in gates_for(tekst) if not ok]
        if plohie:
            krasnyh_faylov += 1
            print(f"❌ {put} — раздел `## ФАЗА ПРИЁМКИ` не проходит гейты:")
            for nazvanie, msg in plohie:
                for i, stroka in enumerate(str(msg).splitlines() or [""]):
                    print(f"   {nazvanie}: {stroka}" if i == 0 else f"      {stroka}")

    if krasnyh_faylov:
        print(f"\nКоммит остановлен: {krasnyh_faylov} файл(ов)-захода с красной фазой приёмки.")
        print("Заполни `## ФАЗА ПРИЁМКИ` (ВЕРДИКТ, ВЕТКА РАБОТЫ, заявки-дубли) — или, если")
        print("красное на ЧУЖОМ долге (не на твоём заходе), обойди с причиной:")
        print("  git_zona.py commit --zone <зона> --no-verify \"<причина>\" -m \"<что и зачем>\"")
        return RC_DEFECT
    return RC_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
