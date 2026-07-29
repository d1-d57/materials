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

for rnd in range(1, MAX_ST + 3):
    run(["python3", str(TOOLS / "sverstat.py")])
    run(["python3", str(REPO / "_generator" / "build_deck.py"), str(SRC)])
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
    [levels.get("s%02d" % i, 0) for i in range(1, 56)]).items())))
