#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ГЕЙТ ВЫХОДА doc-движка — «текст не съеден при отрисовке».

    python3 _generator/tools/check_view.py <src-dir>     # после build_doc.py

Зачем. Линтер build_doc.py проверяет СТРУКТУРУ источника, но не то, что реально
увидит глаз. Реальный инцидент 2026-07-16: в формуле стоял сырой `<`
($a<b<c<d$) — браузер прочитал `<b` как открывающий тег и съел ВЕСЬ текст до
ближайшего `>`, то есть до конца блока. В markdown и в HTML текст на месте,
пропадает только при отрисовке; глазами в источнике не ловится. Владелец
натыкался на это регулярно.

Две проверки (обе могут ПРОВАЛИТЬСЯ):
  1. ОПАСНАЯ ФОРМУЛА — сырой `<` или `>` внутри $…$ / $$…$$.
     Лечение: писать \lt и \gt (KaTeX их понимает, в HTML угловая скобка не идёт).
  2. ХВОСТ БЛОКА НЕ ВИДЕН — конец каждого блока источника ищется в тексте
     выхода со снятыми тегами. Ловит ЛЮБОЕ съедание, а не только случай `<`.

Идиома семьи (_generator/DVIZHKI.md): stdlib, детерминизм, без сети и pip.
Выход: exit 1 при красном — чтобы гейт валил цепочку, а не печатал в пустоту.
"""
import re, sys, pathlib

# '<' — блок сырого HTML (figure/svg/table): он САМ разметка, сверять его хвост
# с текстом выхода бессмысленно (в выходе тегов уже нет) — иначе ложное красное.
SKIP = ('---', '#', '>', '🖼', '<', 'tab:', 'status:', 'poryadok:', 'registr:')


def norm(s):
    """Одинаковая нормализация ОБЕИХ сторон: снять разметку, маркеры, все пробелы.
    Пробелы убираем целиком — иначе `</strong>.` даёт ложное «Венцля .»."""
    s = re.sub(r'^[-*+]\s+', '', s, flags=re.M)   # маркеры списков
    s = re.sub(r'[*_`$\\]', '', s)                # разметка markdown и TeX-слэши
    return re.sub(r'\s+', '', s)


def check(srcdir):
    srcdir = pathlib.Path(srcdir)
    view = srcdir / 'view.html'
    if not view.exists():
        return [("НЕТ ВЫХОДА", "сначала собери: python3 _generator/build_doc.py %s" % srcdir)]
    plain = norm(re.sub(r'<[^>]+>', '', view.read_text(encoding='utf-8')))
    bad = []
    for md in sorted(srcdir.glob('*.md')):
        src = md.read_text(encoding='utf-8')
        for f in re.finditer(r'\$\$.+?\$\$|\$[^$\n]+?\$', src, re.S):
            if re.search(r'[<>]', f.group(0)):
                bad.append(("ОПАСНАЯ ФОРМУЛА (%s) — сырой < или >; пиши \\lt / \\gt" % md.name,
                            f.group(0)[:60]))
        hidden = False           # секция `## Заголовок {скрыть}` в HTML не попадает — и не должна
        for blk in re.split(r'\n\s*\n', src):
            blk = blk.strip()
            if blk.startswith('## '):
                hidden = '{скрыть}' in blk.split('\n')[0]
            # мат-долги (⚑ / «Флаг закрыт») — учёт автора, в HTML не идут по решению владельца
            if '⚑' in blk or 'Флаг закрыт' in blk:
                continue
            if not blk or hidden or blk.startswith(SKIP):
                continue
            tail = norm(blk)[-35:]
            if len(tail) > 12 and tail not in plain:
                bad.append(("ХВОСТ БЛОКА НЕ ВИДЕН В HTML (%s)" % md.name, tail))
    return bad


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[2]); sys.exit(2)
    bad = check(sys.argv[1])
    print("── ГЕЙТ ВЫХОДА (check_view) ──")
    if bad:
        print("  ✗ КРАСНЫЙ — %d" % len(bad))
        for k, v in bad:
            print("     %s: %s" % (k, v))
        sys.exit(1)
    print("  ✓ ЗЕЛЁНЫЙ: текст не съеден, опасных формул нет")


if __name__ == "__main__":
    main()
