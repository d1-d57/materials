#!/usr/bin/env python3
# TOOL-CONTRACT: called-by-hand — ревизия DOLG.md, зовёт аналитик/владелец
# осознанно, не автоматический гейт (заход `instrument-podklyuchen`, Ш1).
"""Чекер статусов DOLG.md скилла slajdy.

Читает ~/Documents/GitHub/disciplina/skills/slajdy/DOLG.md (путь можно
переопределить первым аргументом), находит все записи-долги и проверяет три
вещи разом:

1. **Статус есть.** У каждой записи дописана строка
   `СТАТУС: <МЁРТВ|ЖИВ|УСТАРЕЛ|НЕПРОВЕРЯЕМ|РЕШЕНИЕ ВЛАДЕЛЬЦА> · <дата> ·
   <команда> → <вывод>`.
2. **Фаза есть.** В той же строке — `ФАЗА: <Ф0..Ф7[,Ф..]|НЕПРОВЕРЯЕМ>`.
3. **Записанная команда переиспол­нена и сверена с записанным выводом** —
   но только если команда попадает в закрытый БЕЛЫЙ список заведомо читающих
   инструментов (`grep`, `ls`, `test`, `wc`, `git log/show/grep/ls-files`,
   `python3 <скрипт> --help`, `awk`, `sed -n` без `-i`). Всё остальное —
   «не перепроверяемо автоматически», это законный исход, а не ошибка.
   Команда с явным опасным паттерном (`rm`, `>`, `mv`, `git
   checkout/reset/commit`, `pip`, `curl`) НЕ запускается никогда и
   печатается отдельным списком — значит метку писали неаккуратно.

Записью считается либо строка markdown-таблицы вида `| Д<N> | ... |` /
`| Б<N> | ... |` (статус/фаза ищутся на ТОЙ ЖЕ строке — так дописывает
ревизия), либо заголовок `## Долг <N>` / `## Дефект конкретной лекции...`
(статус/фаза ищутся в теле раздела, до следующего `## ` или строки `---`).

Печатает: сколько долгов всего, распределение по пяти статусам, таблицу
«фаза × статус», разбивку репрогона (совпало/разошлось/не перепроверяемо —
сумма сходится с общим числом долгов), списки без статуса / без фазы /
разошедшихся / опасных команд в метках. Только stdlib.

exit 1, если хоть одна запись без статуса, ИЛИ без фазы, ИЛИ хоть один долг
классифицирован репрогоном как РАЗОШЁЛСЯ.
"""
import re
import shlex
import subprocess
import sys
from pathlib import Path

DEFAULT_PATH = Path("~/Documents/GitHub/disciplina/skills/slajdy/DOLG.md").expanduser()

STATUSY = ("МЁРТВ", "ЖИВ", "УСТАРЕЛ", "НЕПРОВЕРЯЕМ", "РЕШЕНИЕ ВЛАДЕЛЬЦА")
STATUS_RE = re.compile(
    r"СТАТУС:\s*(" + "|".join(re.escape(s) for s in STATUSY) + r")\b"
)
STATUS_TAIL_RE = re.compile(
    r"СТАТУС:\s*(?:" + "|".join(re.escape(s) for s in STATUSY) + r")"
    r"\s*·\s*[^·]+·\s*(.*)",
    re.S,
)
FAZA_RE = re.compile(r"ФАЗА:\s*(Ф[0-7](?:\s*,\s*Ф[0-7])*|НЕПРОВЕРЯЕМ)\b")

ROW_RE = re.compile(r"^\|\s*((?:Д|Б)\d+)\s*\|")
NARRATIVE_HEADING_RE = re.compile(r"^##\s+(Долг\s+\d+|Дефект конкретной лекции)\b")
ANY_HEADING_RE = re.compile(r"^##\s")
SEPARATOR_RE = re.compile(r"^---\s*$")

CMD_OUT_RE = re.compile(
    r"`([^`]+)`\s*→\s*(.*?)(?=(?:\s*`[^`]+`\s*→)|(?:\s*·\s*ФАЗА:)|\Z)",
    re.S,
)
BANNED_RE = re.compile(
    r"(?:\brm\b|>>?(?!=)|\bmv\b|\bpip\b|\bcurl\b|git\s+(?:checkout|reset|commit))"
)
RC_RE = re.compile(r"\brc\s*=\s*(\d+)")
NUM_RE = re.compile(r"(?<!\w)\d+(?!\w)")
NO_FILE_RE = re.compile(r"No such file or directory")
PLACEHOLDER_RE = re.compile(r"<[^<>]*>")  # <лекция>, <имя> — не редирект, а плейсхолдер
CHAIN_OP_RE = re.compile(r"&&|\|\||\$\(|`")
# «требует/обязателен --флаг» в записи vs argparse-usage, где флаг теперь в
# квадратных скобках (опционален) — специфичный, но частый в этом корпусе класс.
REQUIRE_FLAG_RE = re.compile(r"(?<!не )(?:требует|обязател(?:ен|ьно|ьный)|required)\s+(--[\w-]+)")

# Три живых конвенции cwd, встреченные в записанных метках — пробуем по
# очереди, берём первую, где команда не спотыкается о "No such file".
_TOOLS_DIR = Path(__file__).resolve().parent
MATERIALS_ROOT = _TOOLS_DIR.parents[1]
DISCIPLINA_ROOT = Path("~/Documents/GitHub/disciplina").expanduser()
CANDIDATE_CWDS = [
    p for p in (
        MATERIALS_ROOT,
        MATERIALS_ROOT / "_generator",
        DISCIPLINA_ROOT / "skills" / "slajdy",
        DISCIPLINA_ROOT,
    ) if p.exists()
]
TIMEOUT = 10


def find_records(lines):
    """Возвращает список записей: label, status, faza, tail (текст на переисполнение)."""
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
            faza_m = FAZA_RE.search(line)
            records.append({
                "label": label,
                "status": status_m.group(1) if status_m else None,
                "faza": faza_m.group(1) if faza_m else None,
                "tail": line,
            })
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
            block_text = "\n".join(block)
            status_m = STATUS_RE.search(block_text)
            faza_m = FAZA_RE.search(block_text)
            records.append({
                "label": label,
                "status": status_m.group(1) if status_m else None,
                "faza": faza_m.group(1) if faza_m else None,
                "tail": block_text,
            })
            i = j
            continue

        i += 1

    return records


def extract_cmd_output_pairs(tail):
    """Из полного текста записи достаёт пары (команда, записанный вывод) —
    только те, что стоят ПОСЛЕ 'СТАТУС: <вердикт> · <дата> ·'."""
    m = STATUS_TAIL_RE.search(tail)
    if not m:
        return []
    status_tail = m.group(1)
    pairs = []
    for cm in CMD_OUT_RE.finditer(status_tail):
        cmd = cm.group(1).strip()
        out = cm.group(2).strip().rstrip("| \t")
        pairs.append((cmd, out))
    return pairs


def split_segments(cmd):
    """Бьёт команду на сегменты конвейера/цепочки (| и ;), уважая кавычки.
    None — не удалось безопасно токенизировать (несбалансированные кавычки),
    либо команда несёт `&&`/`||`/`$(...)`/бэктик — эти составные формы не
    разбираются посегментно нигде дальше в коде, значит их части остаются
    непроверенными; безопаснее отказаться целиком, чем ошибочно пропустить."""
    if CHAIN_OP_RE.search(cmd):
        return None
    try:
        lex = shlex.shlex(cmd, posix=True, punctuation_chars="|;")
        lex.whitespace_split = True
        tokens = list(lex)
    except ValueError:
        return None
    segments = []
    current = []
    for t in tokens:
        if t in ("|", ";"):
            if current:
                segments.append(current)
            current = []
        else:
            current.append(t)
    if current:
        segments.append(current)
    return segments


def segment_whitelisted(seg):
    if not seg:
        return False
    argv0 = seg[0]
    if argv0 in ("grep", "ls", "test", "wc", "awk"):
        return True
    if argv0 == "sed":
        return "-n" in seg and not any(a.startswith("-i") for a in seg)
    if argv0 == "git":
        return len(seg) >= 2 and seg[1] in ("log", "show", "grep", "ls-files")
    if argv0 == "python3":
        return len(seg) == 3 and seg[2] == "--help"
    return False


def reads_stdin_without_file(cmd, segments):
    """grep/wc/awk без файлового аргумента, ВНЕ конвейера, читает stdin —
    отдельно от соседних шагов (которые её туда пишут) не воспроизводится."""
    if len(segments) != 1:
        return False  # внутри своего конвейера — stdin даёт предыдущий сегмент
    seg = segments[0]
    argv0 = seg[0]
    if argv0 not in ("grep", "wc", "awk"):
        return False
    non_flag = [a for a in seg[1:] if not a.startswith("-")]
    if argv0 == "grep":
        return len(non_flag) < 2  # паттерн есть, файла нет
    if argv0 == "wc":
        return len(non_flag) < 1
    if argv0 == "awk":
        return len(non_flag) < 2  # программа есть, файла нет
    return False


def run_command(cmd):
    """Возвращает (rc, вывод, cwd) либо (None, None, None), если не выполнилось
    ни в одном из кандидатов cwd (таймаут или файлов нет нигде)."""
    last = (None, None, None)
    for cwd in CANDIDATE_CWDS:
        try:
            proc = subprocess.run(
                ["/bin/bash", "-c", cmd],
                cwd=str(cwd),
                capture_output=True,
                text=True,
                timeout=TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            last = (None, "ТАЙМАУТ", cwd)
            continue
        combined = (proc.stdout or "") + (proc.stderr or "")
        if "No such file or directory" in combined and cwd != CANDIDATE_CWDS[-1]:
            last = (proc.returncode, combined, cwd)
            continue
        return proc.returncode, combined, cwd
    return last


def _normalize(s):
    return re.sub(r"\s+", " ", s).strip()


def classify_pair(recorded_out, actual_rc, actual_out):
    """'match' | 'mismatch' | 'unknown' для одной пары команда/вывод."""
    rc_m = RC_RE.search(recorded_out)
    if rc_m and int(rc_m.group(1)) != actual_rc:
        return "mismatch"

    req_m = REQUIRE_FLAG_RE.search(recorded_out)
    if req_m:
        flag = req_m.group(1)
        if re.search(r"\[\s*" + re.escape(flag) + r"\b", actual_out):
            return "mismatch"  # записано «требует», а сейчас в usage опционален

    rec_norm = _normalize(recorded_out)
    act_norm = _normalize(actual_out)
    if rec_norm and act_norm and (rec_norm in act_norm or act_norm in rec_norm):
        return "match"

    stripped = re.sub(r"rc\s*=\s*\d+", "", recorded_out)
    stripped = re.sub(r"«[^»]*»|\"[^\"]*\"", "", stripped)
    residual_alpha = re.sub(r"[\d\s,;:/\-—→.()%]", "", stripped)
    if len(residual_alpha) <= 2:
        rec_nums = [int(x) for x in NUM_RE.findall(recorded_out)]
        act_nums = [int(x) for x in NUM_RE.findall(actual_out)]
        if rec_nums:
            # число-доминированная запись ("1, 0, 0", "12", "6/4/6/4") — точное
            # совпадение ПО ПОРЯДКУ, не просто пересечение множеств: реальный
            # прогон Д44 (0 → 13 при неизменных соседних 1 и 0) показал, что
            # подмножественная проверка маскирует именно такой сдвиг.
            return "match" if rec_nums == act_nums else "mismatch"

    if rc_m:
        return "match"

    return "unknown"


def classify_debt(tail):
    """Возвращает (bucket, detail, danger) для одной записи целиком."""
    pairs = extract_cmd_output_pairs(tail)
    detail = []
    danger = []
    matched = mismatched = unknown = 0

    for cmd, out in pairs:
        if BANNED_RE.search(PLACEHOLDER_RE.sub("", cmd)):
            danger.append(cmd)
            detail.append((cmd, out, "ОПАСНАЯ команда — не выполнена"))
            continue
        segments = split_segments(cmd)
        if not segments or not all(segment_whitelisted(s) for s in segments):
            detail.append((cmd, out, "не в белом списке — не выполнена"))
            continue
        if reads_stdin_without_file(cmd, segments):
            detail.append((cmd, out, "не выполнена — читает stdin без файла, "
                                      "отдельно от соседних шагов не воспроизводится"))
            continue
        rc, actual_out, cwd_used = run_command(cmd)
        if rc is None:
            detail.append((cmd, out, "не выполнена (таймаут / нет подходящего cwd)"))
            continue
        if NO_FILE_RE.search(actual_out or ""):
            detail.append((cmd, out, f"не выполнена — файл(ы) не найдены ни в одном "
                                      f"из cwd (последний: {cwd_used})"))
            continue
        verdict = classify_pair(out, rc, actual_out or "")
        detail.append((
            cmd, out,
            f"{verdict} · rc={rc} · cwd={cwd_used} · реальный вывод={actual_out!r}",
        ))
        if verdict == "match":
            matched += 1
        elif verdict == "mismatch":
            mismatched += 1
        else:
            unknown += 1

    if mismatched:
        bucket = "РАЗОШЛОСЬ"
    elif matched and not unknown:
        bucket = "совпало"
    else:
        bucket = "не перепроверяемо"
    return bucket, detail, danger


def main():
    path = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT_PATH
    if not path.exists():
        print(f"НЕ НАЙДЕН: {path}")
        return 1

    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    records = find_records(lines)
    total = len(records)

    status_counts = {s: 0 for s in STATUSY}
    missing_status = []
    missing_faza = []
    faza_table = {}
    repogon_counts = {"совпало": 0, "РАЗОШЛОСЬ": 0, "не перепроверяемо": 0}
    diverged = []
    danger_all = []

    for rec in records:
        label, status, faza, tail = rec["label"], rec["status"], rec["faza"], rec["tail"]

        if status is None:
            missing_status.append(label)
        else:
            status_counts[status] += 1

        if faza is None:
            missing_faza.append(label)
        for p in (faza.split(",") if faza else ["—"]):
            p = p.strip()
            faza_table.setdefault(p, {s: 0 for s in STATUSY})
            if status:
                faza_table[p][status] += 1

        bucket, detail, danger = classify_debt(tail)
        repogon_counts[bucket] += 1
        if bucket == "РАЗОШЛОСЬ":
            diverged.append((label, detail))
        if danger:
            danger_all.append((label, danger))

    print(f"Долгов всего: {total}")
    for s in STATUSY:
        print(f"  {s}: {status_counts[s]}")
    summa = sum(status_counts.values()) + len(missing_status)
    print(f"Сумма (статусы + без статуса): {summa} (сходится: {summa == total})")

    print("\nФАЗА × СТАТУС (долг с двумя фазами считается в обеих строках):")
    for faza_key in sorted(faza_table):
        row = faza_table[faza_key]
        row_str = " · ".join(f"{s}:{row[s]}" for s in STATUSY if row[s])
        print(f"  {faza_key}: {row_str or '—'}")

    print("\nРЕПРОГОН (по каждому долгу — самый строгий исход среди его команд):")
    for bucket in ("совпало", "РАЗОШЛОСЬ", "не перепроверяемо"):
        print(f"  {bucket}: {repogon_counts[bucket]}")
    summa2 = sum(repogon_counts.values())
    print(f"Сумма (репрогон): {summa2} (сходится: {summa2 == total})")

    rc = 0

    if missing_status:
        print(f"\nБЕЗ СТАТУСА ({len(missing_status)}):")
        for label in missing_status:
            print(f"  - {label}")
        rc = 1

    if missing_faza:
        print(f"\nБЕЗ ФАЗЫ ({len(missing_faza)}):")
        for label in missing_faza:
            print(f"  - {label}")
        rc = 1

    if diverged:
        print(f"\nРАЗОШЛИСЬ ({len(diverged)}):")
        for label, detail in diverged:
            print(f"  - {label}")
            for cmd, out, verdict in detail:
                print(f"      команда:  {cmd}")
                print(f"      записано: {out}")
                print(f"      {verdict}")
        rc = 1

    if danger_all:
        print(f"\nОПАСНЫЕ КОМАНДЫ В МЕТКАХ, не выполнены ({len(danger_all)}):")
        for label, danger in danger_all:
            for d in danger:
                print(f"  - {label}: {d}")

    if rc == 0:
        print("\nВсе записи имеют статус и фазу, разошедшихся не осталось. rc=0")
    return rc


if __name__ == "__main__":
    sys.exit(main())
