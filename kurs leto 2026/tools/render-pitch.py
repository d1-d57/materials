#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render-pitch — генерирует короткий питч-черновик из `0-koncept/KONCEPT.md`.

ЗАЧЕМ. Демонстрация блок-синхрона: КОНЦЕПТ — единственный источник (манифест +
7 карточек лекций по якорям `{L:id}`), питч — генерируемый вид, не рукописная
копия. Правишь `KONCEPT.md` → перезапускаешь этот скрипт → питч обновился.
`6-lending/pitch-kurs.md` (рукописная заготовка) этим скриптом НЕ трогается —
результат идёт в `_out/`.

МЕТОД: только stdlib, без сети/БД, детерминированно.
Запуск: `python3 tools/render-pitch.py` (из любого каталога).
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KONCEPT = ROOT / '0-koncept' / 'KONCEPT.md'
OUT_DIR = ROOT / '6-lending' / '_out'
OUT_FILE = OUT_DIR / 'pitch-generated.md'

_MANIFEST_RE = re.compile(r'\*\*В одну фразу:\*\*\s*(.+)')
_CARD_RE = re.compile(
    r'^\*\*(Л\d\.\s*[^*]+)\*\*\s*(\{L:[\w-]+\})?[^\n]*\n(.+)$', re.MULTILINE)


def _teaser(body):
    """Короткая затравка из тела карточки — до первого ' · '."""
    cut = body.find(' · ')
    teaser = body if cut < 0 else body[:cut]
    return teaser.strip()


def render():
    text = KONCEPT.read_text(encoding='utf-8')

    m_manifest = _MANIFEST_RE.search(text)
    manifest = m_manifest.group(1).strip() if m_manifest else '(манифест не найден)'

    cards = []
    for m in _CARD_RE.finditer(text):
        title, anchor, body = m.group(1).strip(), m.group(2), m.group(3)
        cards.append((title, _teaser(body)))

    lines = []
    lines.append('# Пределы вычислимого — питч (сгенерировано)')
    lines.append('')
    lines.append('> Сгенерировано из `0-koncept/KONCEPT.md`; правь ИСТОЧНИК, не этот файл.')
    lines.append('')
    lines.append('## Манифест')
    lines.append('')
    lines.append(manifest)
    lines.append('')
    lines.append('## Семь лекций')
    lines.append('')
    for title, teaser in cards:
        lines.append(f'- **{title}** — {teaser}')
    lines.append('')

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text('\n'.join(lines), encoding='utf-8')
    return len(cards)


def main():
    n = render()
    print(f'✓ {OUT_FILE.relative_to(ROOT)} — манифест + {n} карточек лекций')
    if n != 7:
        raise SystemExit(f'ожидалось 7 карточек, получено {n}')


if __name__ == '__main__':
    main()
