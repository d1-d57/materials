#!/usr/bin/env python3
"""check_docs.py — страж целостности документации каршеринга.

Проверяет четыре класса дрейфа (stdlib, детерминизм, без исполнения чужого кода):
  1. СИРОТЫ      — каждый содержательный файл назван в индексе README.md.
  2. ССЫЛКИ      — каждая относительная markdown-ссылка [..](path) резолвится в существующий файл.
  3. ИМЕНА       — ни одно имя файла/папки не содержит «й/ё» и совпадает с NFC (ловушка macOS NFD).
  4. УСТАРЕВШЕЕ  — нигде не осталось старых плоских имён (`carsharing_R*`, `carsharing_data_sources`,
                  `carsharing_build_log`, `carsharing_audit`, `carsharing_pricing_analysis`,
                  `carsharing_TOOL_BRIEF`, `00_README`) — иначе миграция регрессировала.

Запуск:  python tools/check_docs.py     (из корня carsharing_archive/)
Выход:   0 — чисто («OK»); 1 — есть нарушения (печатает список).
"""
from __future__ import annotations
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Папки, которые НЕ участвуют в проверке (служебные / транзитные / бэкапы).
SKIP_DIRS = {".git", "__pycache__", "cowork/reports"}
SKIP_PREFIXES = ("carsharing_archive_backup",)

# Файлы под проверку «сироты»: содержательные доки и артефакты.
ORPHAN_DIRS = ("", "spine", "research", "model", "provenance")
ORPHAN_EXT = {".md", ".py", ".xlsx"}
# Индекс сам себя не регистрирует; служебные доки связки — вне орфан-проверки.
ORPHAN_EXEMPT = {"README.md"}

STALE_TOKENS = [
    r"carsharing_R\d",
    r"carsharing_data_sources",
    r"carsharing_build_log",
    r"carsharing_audit",
    r"carsharing_pricing_analysis",
    r"carsharing_TOOL_BRIEF",
    r"00_README",
]

LINK_RE = re.compile(r"\]\(([^)]+)\)")


def skip(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if any(rel == d or rel.startswith(d + "/") for d in SKIP_DIRS):
        return True
    return any(part.startswith(SKIP_PREFIXES) for part in rel.split("/"))


def all_files() -> list[Path]:
    return [p for p in ROOT.rglob("*") if p.is_file() and not skip(p)]


def check_orphans(readme: str) -> list[str]:
    errs = []
    for p in all_files():
        if p.suffix not in ORPHAN_EXT:
            continue
        rel = p.relative_to(ROOT)
        top = rel.parts[0] if len(rel.parts) > 1 else ""
        if top not in ORPHAN_DIRS:
            continue
        if p.name in ORPHAN_EXEMPT:
            continue
        if p.name not in readme:
            errs.append(f"СИРОТА: {rel.as_posix()} — не назван в README.md §2")
    return errs


def check_links() -> list[str]:
    errs = []
    for p in all_files():
        if p.suffix != ".md":
            continue
        text = p.read_text(encoding="utf-8")
        for m in LINK_RE.finditer(text):
            target = m.group(1).strip().split()[0]  # отбросить title в кавычках
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#")[0]
            if not target:
                continue
            if not (target.endswith((".md", ".py", ".xlsx")) or "/" in target):
                continue
            if not (p.parent / target).resolve().exists():
                errs.append(f"БИТАЯ ССЫЛКА: {p.relative_to(ROOT).as_posix()} → {target}")
    return errs


def check_names() -> list[str]:
    errs = []
    for p in ROOT.rglob("*"):
        if skip(p):
            continue
        name = p.name
        if any(ch in name for ch in "йёЙЁ") or unicodedata.normalize("NFC", name) != name:
            errs.append(f"ИМЯ с й/ё или NFD: {p.relative_to(ROOT).as_posix()}")
    return errs


def check_stale() -> list[str]:
    errs = []
    pat = re.compile("|".join(STALE_TOKENS))
    for p in all_files():
        if p.suffix != ".md":
            continue
        # сам этот скрипт и заход о миграции легитимно содержат старые имена в карте переноса
        rel = p.relative_to(ROOT).as_posix()
        if rel.endswith("0001_migrate_structure.md"):
            continue
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if pat.search(line):
                errs.append(f"УСТАРЕВШЕЕ ИМЯ: {rel}:{i}: {line.strip()[:80]}")
    return errs


def main() -> int:
    readme_path = ROOT / "README.md"
    if not readme_path.exists():
        print("ОШИБКА: нет README.md — индекс не найден")
        return 1
    readme = readme_path.read_text(encoding="utf-8")

    errs = check_orphans(readme) + check_links() + check_names() + check_stale()
    if errs:
        print(f"check_docs: {len(errs)} нарушений\n")
        for e in errs:
            print("  " + e)
        return 1
    print("check_docs: OK (0 сирот, 0 битых ссылок, имена чисты, устаревших имён нет)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
