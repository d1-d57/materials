#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверки иллюстраций из POMARKI-2026-08-09.md §3 (заход pomarki-slajd) —
нагружают верификатор, который включается при СОЗДАНИИ иллюстрации (см.
`fazy/ZAHOD.md §4`), а не гейт собранного слайда: дефекты рождаются в картинке,
и ловить их надо там же, до того как их одиннадцать штук уедут на слайды.

  П9.  Вопросительные знаки на иллюстрации — ЗАПРЕЩЕНЫ. Дословно владельца:
       «лишних подписей вот этих вопросительных знаков вообще не нужно,
       это запрещено просто».
  П12. Фон иллюстрации — прозрачный, не белый и не залитый.
  П10/П11. Равенство композиции не пишется подписью поверх стрелки — рисуется
       ДУГОЙ. Признак нарушения: <text> несёт одновременно '∘' и '=' — то есть
       уравнение записано текстом, а не изображено дугой с подписью-меткой.

  python3 _illustracii/proverka_pomarok.py <file.svg|file.html> [ещё файлы...]
  exit 0 — зелёный (нарушений нет), 1 — красный (нарушение хотя бы в одном файле)
"""
import re
import sys
from pathlib import Path

TEXT_RE = re.compile(r"<text\b[^>]*>(.*?)</text>", re.S)
INNER_TAG_RE = re.compile(r"<[^>]+>")
BG_FILL_RE = re.compile(r'fill\s*=\s*["\']?\s*(#fff(?:fff)?|white|var\(--card\))\s*["\']?', re.I)


def _text_contents(svg):
    return [INNER_TAG_RE.sub("", t) for t in TEXT_RE.findall(svg)]


def check_p9_voprositelnye(svg):
    return ["П9: <text> несёт «?» — вопросительные знаки на иллюстрации запрещены: %r" % t
            for t in _text_contents(svg) if "?" in t]


def check_p12_fon(svg):
    m = BG_FILL_RE.search(svg)
    if m:
        return ["П12: заливка фона (%s) — фон обязан быть прозрачным, не белым и не залитым"
                % m.group(1)]
    return []


def check_p10_p11_podpis_nad_strelkoj(svg):
    return ["П10/П11: <text> несёт равенство композиции текстом (%r) — рисуется ДУГОЙ, не "
            "подписью поверх стрелки" % t
            for t in _text_contents(svg) if "∘" in t and "=" in t]


CHECKS = (check_p9_voprositelnye, check_p12_fon, check_p10_p11_podpis_nad_strelkoj)


def check_file(path):
    svg = Path(path).read_text(encoding="utf-8")
    issues = []
    for c in CHECKS:
        issues.extend(c(svg))
    return issues


def main():
    if len(sys.argv) < 2:
        print("использование: proverka_pomarok.py <file.svg|file.html> [ещё файлы...]")
        return 2
    all_issues = []
    for f in sys.argv[1:]:
        issues = check_file(f)
        if issues:
            print("КРАСНЫЙ — %s:" % f)
            for i in issues:
                print("  ✗ %s" % i)
        else:
            print("ЗЕЛЁНЫЙ — %s" % f)
        all_issues.extend(issues)
    return 1 if all_issues else 0


if __name__ == "__main__":
    sys.exit(main())
