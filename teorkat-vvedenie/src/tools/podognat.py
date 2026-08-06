#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Петля подгонки: собрать → промерить → поднять ступень плотности переполненным → снова.

  python3 teorkat-vvedenie/src/tools/podognat.py

Каждый круг печатает, сколько зон переполнено и на сколько; кончается либо нулём
переполнений, либо списком слайдов, которым не хватило ступени 4 — эти и есть
кандидаты на SPLIT, и они называются поимённо, а не тонут в «почти влезло».
Ступени и почему они такие — `sverstat.py`, блок STUPENI.
"""
import json, subprocess, sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SRC = TOOLS.parents[0]
# REPO остаётся, но теперь ТОЛЬКО как рабочая папка прогонов (`cwd=REPO` в `run`).
# Путь к движку из него больше не собирается: движок зовётся по имени —
# `python3 -m dvizhki dek <src>` (ставится один раз, см. `_generator/README.md`).
# Голое «python3», а не `sys.executable`, — так было до правки, и это не меняется:
# заход переписывает адресацию, а не выбор интерпретатора.
REPO = TOOLS.parents[2]
PLOTNOST = TOOLS / "plotnost.json"
MAX_ST = 6


def run(cmd, quiet=True):
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    if r.returncode != 0:
        print("rc=%d  %s" % (r.returncode, " ".join(cmd)))
        print(r.stdout[-3000:], r.stderr[-2000:])
        sys.exit(r.returncode)
    return r.stdout


def measure():
    out = run(["python3", str(TOOLS / "promer.py"), "--csv"])
    return json.loads(out.strip().splitlines()[-1])


levels = json.loads(PLOTNOST.read_text(encoding="utf-8")) if PLOTNOST.exists() else {}
RITM = TOOLS / "ritm.json"


def zapisat(d, path):
    path.write_text(json.dumps(d, ensure_ascii=False, indent=0, sort_keys=True),
                    encoding="utf-8")


def peremerit():
    run(["python3", str(TOOLS / "sverstat.py")])
    run(["python3", "-m", "dvizhki", "dek", str(SRC)])
    data = measure()
    return {d["id"] for d in data if d["dh"] > 1 or d["dw"] > 1}, data


# ── ОБРАТНЫЙ ХОД: отдать слайдам место, которое освободило сжатие текста ────────
# Сжатие убрало треть знаков, а ступени приехали с дека, который верстался под
# НЕсжатый текст. Значит часть слайдов сидит поджатыми без причины: межстрочье 1.24
# и кегль 35px там, где влезли бы 1.5278 и 38–40px. Порядок отдачи задан заходом и
# он НЕ начинается с кегля: сначала ритм между абзацами, потом ступень (она поднимает
# и межстрочье, и поля), и только затем кегль — который тут и не разгоняется вручную,
# а следует из ступени и объёма (`kegl(chars)`, потолок 40px).
#
# Ход батчевый, а не по одному слайду: понизить ступень ВСЕМ разом, померить, и
# вернуть на место ровно тех, кто от этого переполнился. Так круг стоит одну сборку
# вместо тридцати двух.
# ── КТО ИМЕННО ЗАСЛУЖИЛ ОТСТУПЛЕНИЕ ОТ КАНОНА ──────────────────────────────────
# Канон запрещает `display` в сценах, и запрет содержательный: с ним геометрия
# заморожена, при клике не двигается ничего. Но под ним зона обязана вместить ВЕСЬ
# текст слайда разом, а лента из 32 слайдов этого не позволяет. Значит отступать
# надо — но послайдово и по замеру, а не оптом «так проще».
# Ход: снять метки со ВСЕХ слайдов (весь дек по канону), померить, и вернуть метку
# ровно тем, у кого зона переполнена. Круг повторяется, пока список не устоится.
# На выходе — число для отчёта: столько слайдов держат канон, столько нарушают, и
# у каждого нарушителя названа причина числом.
POTOK = TOOLS / "reflow.json"

if "--potok" in sys.argv:
    zapisat = lambda d, p: p.write_text(json.dumps(sorted(d), ensure_ascii=False,
                                                   indent=0), encoding="utf-8")
    nado = set()
    for rnd in range(1, 8):
        zapisat(nado, POTOK)
        run(["python3", str(TOOLS / "sverstat.py")])
        run(["python3", "-m", "dvizhki", "dek", str(SRC)])
        bad = {d["id"] for d in measure() if d["dh"] > 1 or d["dw"] > 1}
        novye = bad - nado
        print("круг %d: канон держат %d из 32 · переполнено %d · добавляем в перетекание %d"
              % (rnd, 32 - len(nado), len(bad), len(novye)))
        if not novye:
            break
        nado |= novye
    zapisat(nado, POTOK)
    run(["python3", str(TOOLS / "sverstat.py")])
    run(["python3", "-m", "dvizhki", "dek", str(SRC)])
    ost = [d for d in measure() if d["dh"] > 1 or d["dw"] > 1]
    print("\nитог: перетекание у %d слайдов из 32 · канон держат %d · переполнено %d"
          % (len(nado), 32 - len(nado), len(ost)))
    print("перетекание: %s" % " ".join(sorted(nado)))
    for d in sorted(ost, key=lambda x: -x["dh"]):
        print("   ОСТАЛОСЬ переполнение %s сцена %d/%d: %+dpx"
              % (d["id"], d["scene"], d["scenes"], d["dh"]))
    sys.exit(1 if ost else 0)

if "--minimizirovat" in sys.argv:
    ritm = json.loads(RITM.read_text(encoding="utf-8")) if RITM.exists() else {}
    plohie, _ = peremerit()
    if plohie:
        print("старт не зелёный (%s) — сначала подгонка вверх" % sorted(plohie))
        sys.exit(1)
    print("старт: 0 переполнений ✓")

    # [1] БЛОЧНЫЙ РИТМ 26 → 58px, шагами по 8
    for val in (34, 42, 50, 58):
        kand = [s for s in ["s%02d" % i for i in range(1, 33)]
                if ritm.get(s, 26) == val - 8]
        for s in kand:
            ritm[s] = val
        zapisat(ritm, RITM)
        plohie, _ = peremerit()
        for s in sorted(plohie):
            ritm[s] = val - 8            # этому слайду место нужно на текст
        zapisat(ritm, RITM)
        print("ритм → %dpx: удержали %d из %d" % (val, len(kand) - len(plohie & set(kand)),
                                                  len(kand)))

    # [2] СТУПЕНЬ ВНИЗ, пока зелено
    for rnd in range(1, MAX_ST + 2):
        kand = [s for s, v in levels.items() if v > 0]
        if not kand:
            break
        for s in kand:
            levels[s] -= 1
        zapisat(levels, PLOTNOST)
        plohie, _ = peremerit()
        vernuli = sorted(plohie)
        for s in vernuli:
            levels[s] += 1
        zapisat(levels, PLOTNOST)
        print("круг вниз %d: понизили %d, вернули %d (%s)"
              % (rnd, len(kand), len(vernuli), " ".join(vernuli) or "—"))
        if len(vernuli) == len(kand):
            break

    plohie, data = peremerit()
    print("\nитог: переполнено %d из %d" % (len(plohie), len(data)))
    from collections import Counter
    print("ступени: %s" % dict(sorted(Counter(
        [levels.get("s%02d" % i, 0) for i in range(1, 33)]).items())))
    print("ритм: %s" % dict(sorted(Counter(
        [ritm.get("s%02d" % i, 26) for i in range(1, 33)]).items())))
    sys.exit(1 if plohie else 0)

for rnd in range(1, MAX_ST + 3):
    run(["python3", str(TOOLS / "sverstat.py")])
    run(["python3", "-m", "dvizhki", "dek", str(SRC)])
    data = measure()
    bad = [d for d in data if d["dh"] > 1 or d["dw"] > 1]
    print("круг %d: переполнено %d из %d" % (rnd, len(bad), len(data)), end="")
    if bad:
        print(" · Δh макс %+d" % max(d["dh"] for d in bad))
    else:
        print(" ✓")
        break
    stuck = []
    for d in bad:
        cur = levels.get(d["id"], 0)
        if cur >= MAX_ST:
            stuck.append((d["id"], d["dh"]))
        else:
            levels[d["id"]] = cur + 1
    PLOTNOST.write_text(json.dumps(levels, ensure_ascii=False, indent=0, sort_keys=True),
                        encoding="utf-8")
    if stuck and len(stuck) == len(bad):
        print("\nступени кончились — КАНДИДАТЫ НА SPLIT (id, сколько не влезло px):")
        for sid, dh in sorted(stuck, key=lambda x: -x[1]):
            print("   %s  %+d" % (sid, dh))
        break

print("\nступени по деку:", dict(sorted(
    (k, v) for k, v in levels.items())) if levels else "все на 0")
from collections import Counter
print("распределение ступеней:", dict(sorted(Counter(
    [levels.get("s%02d" % i, 0) for i in range(1, 33)]).items())))
