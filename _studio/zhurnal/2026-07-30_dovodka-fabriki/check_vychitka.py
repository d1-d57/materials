#!/usr/bin/env python3
"""Проверка REESTR-vychitki.md: хэш блоба в реестре обязан совпадать с живым git hash-object.
Запуск из корня репозитория: python3 _studio/zhurnal/2026-07-30_dovodka-fabriki/check_vychitka.py
rc=0 — все хэши сходятся. rc=1 — есть расхождение (строка устарела, файл дописан после пометки).
"""
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
REESTR = Path(__file__).resolve().parent / "REESTR-vychitki.md"


def git_hash_object(path: Path) -> str:
    result = subprocess.run(
        ["git", "hash-object", str(path)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def parse_rows(text: str):
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 6:
            continue
        if cells[0] in ("путь", "---") or set(cells[0]) <= {"-", ":"}:
            continue
        rows.append(cells)
    return rows


def main() -> int:
    if not REESTR.exists():
        print(f"нет файла реестра: {REESTR}")
        return 1
    rows = parse_rows(REESTR.read_text(encoding="utf-8"))
    total = len(rows)
    mismatches = []
    for cells in rows:
        path, section, _lines, stored_hash, _cands, _date = cells[:6]
        full_path = REPO_ROOT / path
        if not full_path.exists():
            mismatches.append((path, section, stored_hash, "ФАЙЛ НЕ НАЙДЕН"))
            continue
        live_hash = git_hash_object(full_path)
        if not stored_hash or live_hash != stored_hash:
            mismatches.append((path, section, stored_hash, live_hash))

    ok = total - len(mismatches)
    print(f"прочитано {ok} из {total}")
    if mismatches:
        print("РАСХОЖДЕНИЯ:")
        for path, section, stored_hash, live_hash in mismatches:
            print(f"  {path}#{section}: реестр={stored_hash!r} живой={live_hash!r}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
