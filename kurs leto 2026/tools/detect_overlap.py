#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""detect_overlap — СОВЕТНИК дублей прозы между CANON-доками (НЕ гейт).

ЗАЧЕМ. Разные доки могут незаметно начать пересказывать одно и то же (анти-дрейф
из `dizajn-sistemy-pamyati.md §4`). Печатает пары абзацев-кандидатов на дубль —
решение (слить/оставить/это нормальное эхо) принимает человек на консолидации.
Всегда завершается exit 0 (не блокирует ничего) — только печатает.

МЕТОД: stdlib, БЕЗ сети/БД. Грубая эвристика: абзацы длиной ≥40 слов сравниваются
по Jaccard-похожести множества слов (без стоп-слов, нижний регистр); порог и
топ-N — см. константы ниже. Запуск: `python3 tools/detect_overlap.py`.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CANON_SPECS = [
    ('', False),
    ('1-START-HERE', False),
    ('0-koncept', True),
    ('2-idei', False),
    ('biblioteka', False),
    ('istochnik', False),
]
EXCLUDE_DIRS = ('zhurnal', 'snapshots', '_arhiv', 'tools')
EXCLUDE_DIR_NAMES_ANYWHERE = ('_out', '_arhiv')

MIN_WORDS = 40          # игнорируем короткие абзацы (заголовки, списки-однострочники)
JACCARD_THRESHOLD = 0.5  # порог похожести множества слов
TOP_N = 20               # печатаем не больше N пар-кандидатов


def canon_md_files():
    out = []
    for base, recursive in CANON_SPECS:
        d = ROOT / base if base else ROOT
        if not d.exists():
            continue
        it = d.rglob('*.md') if recursive else d.glob('*.md')
        for p in it:
            rel = p.relative_to(ROOT)
            parts = rel.parts
            if not base and (parts[0] in EXCLUDE_DIRS or parts[0].startswith('.')):
                continue
            if any(x in EXCLUDE_DIR_NAMES_ANYWHERE for x in parts):
                continue
            out.append(rel)
    return sorted(set(out))


def paragraphs(rel):
    text = (ROOT / rel).read_text(encoding='utf-8')
    for i, para in enumerate(re.split(r'\n\s*\n', text)):
        words = re.findall(r'[\wА-Яа-яЁё]+', para.lower())
        if len(words) >= MIN_WORDS:
            yield i, para.strip(), set(words)


def jaccard(a, b):
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def main():
    items = []  # (rel, para_idx, text, wordset)
    for rel in canon_md_files():
        for idx, text, ws in paragraphs(rel):
            items.append((rel, idx, text, ws))

    candidates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            rel_a, idx_a, text_a, ws_a = items[i]
            rel_b, idx_b, text_b, ws_b = items[j]
            if rel_a == rel_b:
                continue  # дубли внутри одного файла — не цель этого советника
            score = jaccard(ws_a, ws_b)
            if score >= JACCARD_THRESHOLD:
                candidates.append((score, rel_a, idx_a, text_a, rel_b, idx_b, text_b))

    candidates.sort(key=lambda c: -c[0])
    if not candidates:
        print('detect_overlap: явных кандидатов на дубль прозы не найдено.')
        return

    shown = candidates[:TOP_N]
    print(f'detect_overlap: {len(candidates)} кандидат(ов) на дубль прозы '
          f'(похожесть ≥ {JACCARD_THRESHOLD:.0%}), показаны top-{len(shown)}:\n')
    for score, rel_a, idx_a, text_a, rel_b, idx_b, text_b in shown:
        print(f'— {score:.0%} похожесть: {rel_a}#абзац{idx_a} ↔ {rel_b}#абзац{idx_b}')
        print(f'    A: {text_a[:120].replace(chr(10), " ")}…')
        print(f'    B: {text_b[:120].replace(chr(10), " ")}…')
    if len(candidates) > TOP_N:
        print(f'\n… и ещё {len(candidates) - TOP_N} кандидат(ов) не показано (см. TOP_N в скрипте).')


if __name__ == '__main__':
    main()
