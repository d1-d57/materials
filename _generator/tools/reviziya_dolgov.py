#!/usr/bin/env python3
"""Чекер статусов DOLG.md скилла slajdy.

Читает ~/Documents/GitHub/disciplina/skills/slajdy/DOLG.md (путь можно
переопределить первым аргументом), находит все записи-долги и проверяет,
что у каждой дописана строка вида:

    СТАТУС: <МЁРТВ|ЖИВ|УСТАРЕЛ|НЕПРОВЕРЯЕМ|РЕШЕНИЕ ВЛАДЕЛЬЦА> · <дата> · <команда> → <вывод>

Записью считается либо строка markdown-таблицы вида `| Д<N> | ... |` /
`| Б<N> | ... |` (статус ищется на ТОЙ ЖЕ строке — так дописывает ревизия),
либо заголовок `## Долг <N>` / `## Дефект конкретной лекции...` (статус
ищется в теле раздела, до следующего `## ` или строки `---`).

Печатает: сколько долгов всего, распределение по пяти статусам, и список
записей без статуса. Только stdlib. exit 1, если хоть одна запись без
статуса (или с нераспознанным статусом).
"""
import re
import sys
from pathlib import Path

DEFAULT_PATH = Path("~/Documents/GitHub/disciplina/skills/slajdy/DOLG.md").expanduser()

STATUSY = ("МЁРТВ", "ЖИВ", "УСТАРЕЛ", "НЕПРОВЕРЯЕМ", "РЕШЕНИЕ ВЛАДЕЛЬЦА")
STATUS_RE = re.compile(
    r"СТАТУС:\s*(" + "|".join(re.escape(s) for s in STATUSY) + r")\b"
)

ROW_RE = re.compile(r"^\|\s*((?:Д|Б)\d+)\s*\|")
NARRATIVE_HEADING_RE = re.compile(r"^##\s+(Долг\s+\d+|Дефект конкретной лекции)\b")
ANY_HEADING_RE = re.compile(r"^##\s")
SEPARATOR_RE = re.compile(r"^---\s*$")


def find_records(lines):
    """Возвращает список (label, status_or_None) по всем записям файла."""
    records = []
    seen_labels = {}

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]

        m = ROW_RE.match(line)
        if m:
            base_label = m.group(1)
            occ = seen_labels.get(base_label, 0) + 1
            seen_labels[base_label] = occ
            label = base_label if occ == 1 else f"{base_label}#{occ}"
            status_m = STATUS_RE.search(line)
            records.append((label, status_m.group(1) if status_m else None))
            i += 1
            continue

        m = NARRATIVE_HEADING_RE.match(line)
        if m:
            label = m.group(1).strip()
            j = i + 1
            block = []
            while j < n and not ANY_HEADING_RE.match(lines[j]) and not SEPARATOR_RE.match(lines[j]):
                block.append(lines[j])
                j += 1
            status = None
            for bline in block:
                sm = STATUS_RE.search(bline)
                if sm:
                    status = sm.group(1)
            records.append((label, status))
            i = j
            continue

        i += 1

    return records


def main():
    path = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT_PATH
    if not path.exists():
        print(f"НЕ НАЙДЕН: {path}")
        return 1

    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    records = find_records(lines)

    total = len(records)
    counts = {s: 0 for s in STATUSY}
    missing = []
    for label, status in records:
        if status is None:
            missing.append(label)
        else:
            counts[status] += 1

    print(f"Долгов всего: {total}")
    for s in STATUSY:
        print(f"  {s}: {counts[s]}")
    summa = sum(counts.values()) + len(missing)
    print(f"Сумма (статусы + без статуса): {summa} (сходится: {summa == total})")

    if missing:
        print(f"БЕЗ СТАТУСА ({len(missing)}):")
        for label in missing:
            print(f"  - {label}")
        return 1

    print("Все записи имеют статус. rc=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
