#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""15 calls of pravilo.py, one per rule С18–С32; first sentence of each rule's text from B2.

    python3 -I pravila_dver.py              # print the first sentences only
    python3 -I pravila_dver.py --run [--vse] # call the door per rule; --vse: do not stop on refusal
"""
import json, re, subprocess, sys
from pathlib import Path

D = Path("/Users/ivanyakovlev/Documents/GitHub/disciplina")
VST = Path("/Users/ivanyakovlev/Documents/GitHub/materials/_studio/zhurnal/"
           "2026-08-24_obzor-funkciya-putey/z2/VSTAVKI-navyk-lenta.md")
OUT = Path("/private/tmp") / "pravila_rezultat.json"
UROKI = "../materials/_studio/zhurnal/2026-08-24_obzor-funkciya-putey/UROKI-FABRIKE.md"
NADEZHDA = ("no countable signal; held by reading — genre profile "
            "skills/lenta/references/ZHANR-statya.md and etalon skills/lenta/references/etalon-obzor-01/")
RYCHAG = {"С18", "С22", "С29"}

vt = VST.read_text(encoding="utf-8")
b2 = re.search(r"^## В2 · .*?(?=^---$)", vt, re.S | re.M).group(0)
pravila = []
for m in re.finditer(r"^## (С\d+) · [^\n]*\n\n(.*?)(?:\n\n|\Z)", b2, re.S | re.M):
    abz = " ".join(m.group(2).split())
    # first sentence: '.' followed by space + capital, outside «…»
    glub, konec = 0, len(abz)
    for i, c in enumerate(abz):
        if c == "«":
            glub += 1
        elif c == "»":
            glub -= 1
        elif c == "." and glub == 0 and (i + 1 == len(abz) or
                                          (abz[i + 1] == " " and i + 2 < len(abz) and abz[i + 2].isupper())):
            konec = i + 1
            break
    pravila.append((m.group(1), abz[:konec]))
assert [n for n, _ in pravila] == ["С%d" % i for i in range(18, 33)], [n for n, _ in pravila]

if "--run" not in sys.argv:
    for n, f in pravila:
        print("%s. %s" % (n, f))
    sys.exit(0)

rez = []
for n, f in pravila:
    zakr = UROKI + "#64" + ("," + UROKI + "#61" if n == "С18" else "")
    cmd = ["python3", "_generator/tools/pravilo.py", "--skill", "lenta", "--tekst", "%s. %s" % (n, f),
           "--zakryvaet", zakr]
    cmd += ["--rychag", "_generator/tools/check_lenta.py профиль статьи %s" % n] if n in RYCHAG \
        else ["--nadezhda", NADEZHDA]
    r = subprocess.run(cmd, cwd=D, capture_output=True, text=True)
    rez.append({"pravilo": n, "rc": r.returncode, "out": r.stdout.strip(), "err": r.stderr.strip()})
    print("rc=%d %s | %s" % (r.returncode, n, (r.stdout.strip() or r.stderr.strip()).splitlines()[-1:]))
    OUT.write_text(json.dumps(rez, ensure_ascii=False, indent=1), encoding="utf-8")
    if r.returncode != 0 and "--vse" not in sys.argv:
        print("door refused — stop here, nothing written by hand")
        sys.exit(1)
