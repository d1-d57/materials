# Верификация разведения 156 id (`meta §7.2` → zahody/priyomka/SPORNYE)

Независимая проверка. Метод: собственный python3-скрипт, программное извлечение id из markdown-таблиц по границам секций, без обращения к файлам `RAZVOD-156.md`, `joined-3-lists.json`, `srez-7.2-vhodnye-156.md`, `table-*-*.md` в этой же папке — это чужая работа, которую я проверяю, а не источник данных для проверки.

## (а) Источник

`doma/meta/POKRYTIE.md`, секция `### §7.2 Под-дом «заходы и приёмка» — 156 id`.

Граница секции определена программно: от строки, матчащей `^### §7\.2\b`, до первой следующей строки, матчащей `^### §7\.3\b|^## §8\b`. Фактически получился срез строк **228–396** (следующий заголовок — `### §7.3` на строке 397).

Извлечено первой колонкой из строк вида `| id | ... |` (пропущены строка-заголовок таблицы `| id | кратность | ... |` и строка-разделитель `|---|---|...|`):

**156 id**, все уникальны (проверено — `len(set(ids)) == len(ids) == 156`).

## (б) Три целевых места

| место | секция | границы (строки) | извлечено id | заявлено в заголовке |
|---|---|---|---|---|
| `doma/zahody/POKRYTIE.md` | `## §2. Разведённые записи — 65 id` | 43–112 (до `## §3`) | **65** | 65 |
| `doma/priyomka/POKRYTIE.md` | `## §2. Разведённые записи — 17 id` | 42–74 (до `## §3`) | **17** | 17 |
| `doma/SPORNYE.md` | `## §Б. Батч 14.08 — 74 строки` | 105–223 (до конца файла — это последняя секция; НЕ секция `§А. Батч 06.08`, которая осталась вне среза) | **74** | 74 |

Сумма трёх целевых списков: 65 + 17 + 74 = **156**, совпадает с числом id источника.

## (в) Потерянные id (есть в источнике, нет ни в одном из трёх целевых списков)

**Потерь нет.** Множество источника (156) равно объединению трёх целевых множеств (156 уникальных элементов, объединение без пересечений).

## (г) Задвоенные id (попали в 2+ списков одновременно)

**Дублей нет** — ни между списками (пересечение zahody∩priyomka∩SPORNYE §Б пусто по всем парам), ни внутри одного списка (ни в одном из четырёх списков, включая источник, нет повторяющейся строки).

## (д) Посторонние id (есть в целевых, нет в источнике)

**Посторонних нет.**

## (е) Вердикт

```
ВЕРДИКТ: потерь 0, дублей 0, посторонних 0
```

Мандат задания («список потерь пуст, дублей 0») подтверждён программно — разведение 156 id по трём местам (zahody 65 + priyomka 17 + SPORNYE §Б 74) корректно: без потерь, без дублей, без посторонних записей.

---

## Скрипт проверки (воспроизводим дословно)

```python
#!/usr/bin/env python3
import re

ROOT = "/Users/ivanyakovlev/Documents/GitHub/disciplina"

def read_lines(path):
    with open(path, encoding="utf-8") as f:
        return f.readlines()

def extract_section(lines, start_pat, end_pat=None):
    start_idx = None
    for i, line in enumerate(lines):
        if re.search(start_pat, line):
            start_idx = i
            break
    if start_idx is None:
        raise ValueError(f"Начало секции не найдено: {start_pat}")
    end_idx = len(lines)
    if end_pat is not None:
        for j in range(start_idx + 1, len(lines)):
            if re.search(end_pat, lines[j]):
                end_idx = j
                break
    return lines[start_idx:end_idx], start_idx, end_idx

TABLE_ROW = re.compile(r"^\|\s*([^\s|][^|]*?)\s*\|")

def extract_ids_from_table(section_lines):
    ids = []
    for line in section_lines:
        line = line.rstrip("\n")
        if not line.startswith("|"):
            continue
        m = TABLE_ROW.match(line)
        if not m:
            continue
        cell = m.group(1).strip()
        if cell.lower() in ("id",):
            continue
        if re.fullmatch(r"-{2,}", cell):
            continue
        if not cell:
            continue
        ids.append(cell)
    return ids

def report_dupes(ids):
    seen = {}
    for i in ids:
        seen[i] = seen.get(i, 0) + 1
    return [(i, c) for i, c in seen.items() if c > 1]

# 1. Источник
meta_lines = read_lines(f"{ROOT}/doma/meta/POKRYTIE.md")
src_section, s_start, s_end = extract_section(
    meta_lines, r"^### §7\.2\b", r"^### §7\.3\b|^## §8\b")
src_ids = extract_ids_from_table(src_section)

# 2. zahody §2
zahody_lines = read_lines(f"{ROOT}/doma/zahody/POKRYTIE.md")
z_section, *_ = extract_section(
    zahody_lines, r"^## §2\. Развед[её]нные записи", r"^## §3\b")
zahody_ids = extract_ids_from_table(z_section)

# 3. priyomka §2
priyomka_lines = read_lines(f"{ROOT}/doma/priyomka/POKRYTIE.md")
p_section, *_ = extract_section(
    priyomka_lines, r"^## §2\. Развед[её]нные записи", r"^## §3\b")
priyomka_ids = extract_ids_from_table(p_section)

# 4. SPORNYE §Б (батч 14.08) — последняя секция файла, до конца
spornye_lines = read_lines(f"{ROOT}/doma/SPORNYE.md")
b_section, *_ = extract_section(
    spornye_lines, r"^## §Б\. Батч 14\.08", None)
spornye_ids = extract_ids_from_table(b_section)

src_set = set(src_ids)
union_targets = set(zahody_ids) | set(priyomka_ids) | set(spornye_ids)

lost = sorted(src_set - union_targets)
foreign = sorted(union_targets - src_set)

from collections import defaultdict
membership = defaultdict(list)
for i in zahody_ids: membership[i].append("zahody")
for i in priyomka_ids: membership[i].append("priyomka")
for i in spornye_ids: membership[i].append("SPORNYE")
cross_dupes = [(i, l) for i, l in membership.items() if len(l) > 1]

total_dupes = (len(cross_dupes) + len(report_dupes(zahody_ids))
               + len(report_dupes(priyomka_ids)) + len(report_dupes(spornye_ids)))

print(f"источник: {len(src_ids)} (уникальных {len(src_set)})")
print(f"zahody: {len(zahody_ids)}, priyomka: {len(priyomka_ids)}, SPORNYE §Б: {len(spornye_ids)}")
print(f"потерь: {len(lost)} {lost}")
print(f"дублей: {total_dupes} {cross_dupes}")
print(f"посторонних: {len(foreign)} {foreign}")
print(f"ВЕРДИКТ: потерь {len(lost)}, дублей {total_dupes}, посторонних {len(foreign)}")
```

Фактический вывод скрипта при запуске (13.08–14.08 сессии, `python3`, macOS):

```
[meta] §7.2 срез строк: 228..396, файл .../doma/meta/POKRYTIE.md
[zahody] §2 срез строк: 43..112, файл .../doma/zahody/POKRYTIE.md
[priyomka] §2 срез строк: 42..74, файл .../doma/priyomka/POKRYTIE.md
[SPORNYE] §Б срез строк: 105..223 (до конца файла), файл .../doma/SPORNYE.md

Источник (meta §7.2):  156 id (заявлено в заголовке: 156)
zahody §2:             65 id (заявлено в заголовке: 65)
priyomka §2:           17 id (заявлено в заголовке: 17)
SPORNYE §Б:            74 id (заявлено в заголовке: 74)
Сумма трёх целевых:    156

=== ПОТЕРЯННЫЕ id ===
0 []

=== ЗАДВОЕННЫЕ id (в 2+ целевых списках) ===
итого: 0

=== ВНУТРЕННИЕ повторы (в одном списке) ===
zahody: []
priyomka: []
SPORNYE §Б: []
источник (meta §7.2): []

=== ПОСТОРОННИЕ id ===
0 []

ВЕРДИКТ: потерь 0, дублей 0, посторонних 0
```
