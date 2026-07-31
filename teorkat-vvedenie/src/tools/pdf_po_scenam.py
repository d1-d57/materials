#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Колода → PDF, СТРАНИЦА НА СЦЕНУ (а не на слайд).

  python3 teorkat-vvedenie/src/tools/pdf_po_scenam.py <выходной.pdf> [папка-кадров]

Почему страница на СЦЕНУ. Владелец 31.07: «PDF точно такой же должен быть», то есть
читатель PDF обязан увидеть ровно то же, что зал, — включая шаги, которые на слайде
открываются по клику. Слайд с четырьмя сценами, сплющенный в одну страницу, показал бы
всё разом: это другой документ, а не тот же.

🔴 ЧИСЛО СТРАНИЦ НЕ КОНСТАНТА. Оно равно живой сумме `data-scenes` по колоде и растёт
от любой правки текста. Скрипт печатает и число снятых кадров, и число страниц, и они
обязаны совпадать. *Цена, из-за которой это написано красным: аналитик спросил владельца
«PDF на 34 страницы?», владелец ответил «делаем 34» — а 34 было выдумано аналитиком,
живых сцен было 23. Согласие владельца на выдуманное число не делает число верным.*

Кадры снимает `kadry.py` — тот же код, что и для зрительной петли, и это НЕ дубль ради
удобства: PDF обязан состоять ровно из тех кадров, которые исполнитель смотрел глазами.
Своя съёмка здесь означала бы, что проверено одно, а выдано другое.

Растр, а не вектор, — осознанно. `page.pdf()` печатает в print-медиа, а колода стоит на
`#stage{position:fixed}` и на пер-слайдовых гридах в `<style>`; печатная раскладка от
экранной там расходится, и PDF перестал бы быть «точно таким же». Кадр 2× даёт 2880×1620
на страницу 1440×810 pt — то есть 2 пикселя на точку, этого хватает и на проекторе,
и в печать.
"""
import sys, subprocess, tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
KADRY = Path(__file__).resolve().parent / "kadry.py"

if len(sys.argv) < 2:
    raise SystemExit(__doc__.strip().split("\n")[2].strip())
OUT_PDF = Path(sys.argv[1]).resolve()
# 🔴 Кадры по умолчанию ВНЕ репозитория. Первая версия клала их в `src/dist/`, и 34
# кадра по 2× (≈40 МБ) поехали бы в коммит как побочный продукт сборки PDF, который
# из PDF же и восстанавливается. Своя папка нужна — но временная.
KADR_DIR = (Path(sys.argv[2]).resolve() if len(sys.argv) > 2
            else Path(tempfile.mkdtemp(prefix="kadry-pdf-")))

# ── 1. кадры: по одному на сцену, 2× ────────────────────────────────────────────
env_scale = {"KADRY_SCALE": "2"}
import os
env = dict(os.environ, **env_scale)
r = subprocess.run([sys.executable, str(KADRY), str(KADR_DIR)], env=env,
                   capture_output=True, text=True)
print(r.stdout.strip() or r.stderr.strip())
if r.returncode != 0:
    raise SystemExit("kadry.py вернул rc=%d" % r.returncode)

# ── 2. кадры → PDF в порядке показа ─────────────────────────────────────────────
from PIL import Image

def key(p):
    """Порядок страниц = порядок показа. Имя кадра — `<id>-c<K>.png`; сортировать
    их лексикографически нельзя (`s10` встал бы перед `s02`), поэтому номер сцены
    и номер слайда разбираются числами, а служебные слайды держатся своим местом
    по `slide_order`."""
    stem = p.stem
    sid, _, k = stem.rpartition("-c")
    return (ORDER.index(sid), int(k))

order_src = (SRC / "brief.md").read_text(encoding="utf-8")
ORDER = [l.strip()[2:] for l in order_src.split("\n")
         if l.startswith("  - ")]
kadry = sorted(KADR_DIR.glob("*.png"), key=key)
if not kadry:
    raise SystemExit("кадров нет: %s" % KADR_DIR)

pages = [Image.open(p).convert("RGB") for p in kadry]
pages[0].save(OUT_PDF, save_all=True, append_images=pages[1:],
              resolution=144.0)   # 2880px / 20in → страница 1440×810 pt

sceny = sum(int((__import__("re").search(r'data-scenes="(\d+)"', f.read_text(encoding="utf-8"))
                 or [0, "1"])[1]) for f in sorted((SRC / "slides").glob("*.html")))
print("кадров: %d · страниц в PDF: %d · сцен по slides/: %d"
      % (len(kadry), len(pages), sceny))
print("→ %s (%d КБ)" % (OUT_PDF, OUT_PDF.stat().st_size // 1024))
if len(pages) != len(kadry):
    raise SystemExit("страниц не столько, сколько кадров")
