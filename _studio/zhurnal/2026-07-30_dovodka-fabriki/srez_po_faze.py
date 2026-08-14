#!/usr/bin/env python3
"""Как забрать пачку записей одной фазы из KARTOTEKA-problem.md — часть D захода.
Читает ЖИВОЙ файл (не приватные _data_*.py), считает Σ кратности по фазе для каждого
из 5 разделов и печатает сводную таблицу. Пересчитывать этой командой, не переписывать руками.

Использование:
  python3 srez_po_faze.py                # сводная таблица по всем фазам
  python3 srez_po_faze.py 06-tekst        # список строк (все разделы), относящихся к фазе
"""
import re, sys, os, collections

PATH = os.path.expanduser("~/Documents/GitHub/disciplina/korpus/2026-07-30_dovodka-fabriki/KARTOTEKA-problem.md")
PHASES = ["01-brief","02-reserch","03-matbaza","04-gibrid-istochnik","04.5-intervyu",
          "05-raskadrovka","06-tekst","07-verstka","08-sceny","09-illustracii",
          "10-sborka-qa","вне-фаз"]

# Раздел 1/2/5: | id | `фаза` | кратность | адреса |
ROW4 = re.compile(r'^\|\s*([^|]+?)\s*\|\s*`([^`]+)`\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*$')
# Раздел 3: | id | класс | `фаза` | подкласс | симптом | цена | статус | рычаг |  (кратность=1)
ROW_R3 = re.compile(r'^\|\s*И-\d+\s*\|\s*И\s*\|\s*`([^`]+)`\s*\|')
# Раздел 4: | id | симптом | кратность | класс | `фаза` | статус | рычаг |
ROW_R4 = re.compile(r'^\|\s*ГИТ-\w+\s*\|[^|]*\|\s*(\d+)\s*\|[^|]*\|\s*`([^`]+)`\s*\|')

def parse():
    with open(PATH, encoding="utf-8") as f:
        text = f.read()
    sections = re.split(r'\n(?=## Раздел \d)', text)
    counts = collections.Counter()
    rows_by_phase = collections.defaultdict(list)
    for sec in sections:
        head = sec.split("\n", 1)[0]
        if not head.startswith("## Раздел"):
            continue
        num = re.match(r'## Раздел (\d)', head).group(1)
        for ln in sec.split("\n"):
            if num == "3":
                m = ROW_R3.match(ln)
                if m:
                    phase = m.group(1).split("/")[0]
                    counts[phase] += 1
                    rows_by_phase[phase].append(ln)
            elif num == "4":
                m = ROW_R4.match(ln)
                if m:
                    n, phase = int(m.group(1)), m.group(2).split("/")[0]
                    counts[phase] += n
                    rows_by_phase[phase].append(ln)
            else:
                m = ROW4.match(ln)
                if m and not ln.startswith("| id |") and not ln.startswith("|---"):
                    _id, phase, n, _addr = m.groups()
                    phase = phase.split("/")[0]
                    if phase in PHASES:
                        counts[phase] += int(n)
                        rows_by_phase[phase].append(ln)
    return counts, rows_by_phase

def main():
    counts, rows_by_phase = parse()
    if len(sys.argv) > 1:
        phase = sys.argv[1]
        for ln in rows_by_phase.get(phase, []):
            print(ln)
        print(f"\nИтого строк для {phase}: {len(rows_by_phase.get(phase, []))}", file=sys.stderr)
        return
    total = 0
    print(f"{'фаза':22} {'Σ кратность':>12}")
    for p in sorted(PHASES, key=lambda x: -counts[x]):
        print(f"{p:22} {counts[p]:>12}")
        total += counts[p]
    print(f"{'ИТОГО':22} {total:>12}")

if __name__ == "__main__":
    main()
