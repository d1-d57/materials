#!/usr/bin/env python3
"""The answers of the 7И works 22.09–06.10 -> ``otvety.csv`` (owner's rule Р328: the right answer is a
NUMBER, not an expression).

One row per work × variant × item: ``rabota_id,variant,punkt,otvet,chislo,istochnik``.

* ``rabota_id`` -- the work's id in ``bot-7i/katalog.yaml``; ``punkt`` -- the item label of the export;
* ``otvet`` -- the answer as a child is shown it;
* ``chislo`` -- the final number (integer or irreducible ``a/b``; a quantity in the key's unit:
  seconds, kilograms), empty for a non-numeric item (a list, a formula, yes/no, a proof, a table,
  letters, several numbers, an inequality);
* ``istochnik`` -- the key file and the place in it.

Nothing is typed by hand where a key is computed by code: every key below is read from its own
file (READ-ONLY -- a script that writes on import is run with its writes kept in memory).  Where
two sources give one number (a text key and the code), they must agree; a disagreement drops the
row and is printed.  The run prints numbers only.

    python3 diskmat-57/bank-7i/sobrat_otvety.py
"""

from __future__ import annotations

import ast
import builtins
import csv
import html
import importlib.util
import io
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
LG = HERE.parent / "2026-08-18_logika-goda-7"
I29 = LG / "iteracii" / "2026-09-29_kombinatorika-2"
I06 = LG / "iteracii" / "2026-10-06_kontrolnaya-i-chetnost"
MASHINA = HERE.parent / "mashina-listka"
OUT = HERE / "otvety.csv"

rows: list = []          # the table
razoshlos: list = []     # (work, variant, item, text, code) -- rows not written
dvazhdy = 0              # numbers confirmed by two sources
ustarelo: list = []      # code entries that are not the printed problem (older draft)


def rel(p: Path) -> str:
    return str(p.relative_to(HERE.parent.parent))


# ------------------------------------------------------------------ numbers of a key text
def chislo_kluch(s: str):
    """The number of a key's answer text: after the last «=», notes in brackets dropped; a
    fraction stays exact; «53 %» -> 53/100.  ``None`` when it is not one number."""
    s = re.sub(r"\((или|сумма)[^)]*\)", "", s)
    s = s.split("=")[-1].strip().replace("\u2009", "").replace(" ", "")
    s = s.replace("\\,", "").replace("\\%", "%")
    m = re.fullmatch(r"(-?\d+)(?:/(\d+))?(%?)", s)
    if not m:
        return None
    x = Fraction(int(m.group(1)), int(m.group(2) or 1))
    return x / 100 if m.group(3) else x


def itog(s: str) -> str:
    """What a child is shown for a numeric key: the result, not the expression (owner, Р328) --
    the text after the last «=», without the key's «(или …)» notes."""
    return re.sub(r"\s*\((или|сумма)[^)]*\)", "", s).split("=")[-1].strip()


def fmt(x) -> str:
    return "" if x is None else (str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator))


def vychislit(expr: str):
    """Exact value of an arithmetic expression of the key (· × − : / ^ and brackets)."""
    e = expr.replace("·", "*").replace("×", "*").replace("−", "-").replace("–", "-").replace(":", "/")
    e = e.replace("^", "**").replace(" ", "")
    if not re.fullmatch(r"[\d+\-*/()]+", e):
        return None
    e = re.sub(r"(\d+)", r"F(\1)", e)
    return eval(e, {"__builtins__": {}, "F": Fraction})


def dobavit(rid, var, punkt, otvet, chislo, istochnik, vtoroe=None, vtoroe_ist=""):
    """One row; ``vtoroe`` -- the second source's number (must equal ``chislo``)."""
    global dvazhdy
    if vtoroe is not None:
        if chislo != vtoroe:
            razoshlos.append((rid, var, punkt, fmt(chislo), fmt(vtoroe), vtoroe_ist))
            return
        dvazhdy += 1
        istochnik += " = " + vtoroe_ist
    rows.append({"rabota_id": rid, "variant": var, "punkt": punkt, "otvet": otvet,
                 "chislo": fmt(chislo), "istochnik": istochnik})


def bez_zapisi(path: Path, ns: dict) -> dict:
    """Run a key script whose module code writes a file: writes go to memory, reads to disk."""
    def open_(f, mode="r", *a, **k):
        if any(c in mode for c in "wax+"):
            return io.StringIO() if "b" not in mode else io.BytesIO()
        return builtins.open(f, mode, *a, **k)
    ns.update({"__file__": str(path), "__name__": "kluch", "open": open_})
    out = io.StringIO()
    old, sys.stdout = sys.stdout, out
    try:
        exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), ns)
    finally:
        sys.stdout = old
    return ns


def modul(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem.replace("-", "_"), path)
    m = importlib.util.module_from_spec(spec)
    old, sys.stdout = sys.stdout, io.StringIO()
    try:
        spec.loader.exec_module(m)
    finally:
        sys.stdout = old
    return m


def literal(path: Path, name: str):
    """A dict literal ``name = {...}`` of a script, read without running it."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise KeyError("%s: no %s" % (path.name, name))


# ============================================================ Л3, 22.09 (LS-2026-09-22)
def l3():
    tex = LG / "shpargalka_22-09_podschety.tex"
    ist = rel(tex)
    # the sub-items of each problem, per variant, in sheet order (the printed sheet = the export)
    METKI = {
        "А": "1а 1б 1в 2а 2б 2в 2г 3 4а 4б 5 6 7 8 9 10а 10б 11а 11б 12а 12б 12в 13а 13б 13в 14а 14б"
             " 15а 15б 16 17а 17б 18а 18б 19а 19б 20 21 22",
        "Б": "1а 1б 1в 2а 2б 2в 2г 3 4а 4б 5 6 7 8 9 10а 10б 11а 11б 12а 12б 12в 13а 13б 14а 14б 15а"
             " 15б 16а 16б 16в 17а 17б 18а 18б 19 20 21 22"}
    po_nomeru = {v: {} for v in METKI}
    for v, s in METKI.items():
        for lab in s.split():
            po_nomeru[v].setdefault(re.match(r"\d+", lab).group(), []).append(lab)
    # non-numeric items (decided in ## ПЛАН): lists, formula, yes/no, inequality, several numbers
    NE = {"А": {"1в", "5", "6", "9", "11а", "15а", "15б", "16", "20", "21", "22"},
          "Б": {"1в", "5", "6", "9", "17а", "18а", "18б", "19", "20", "21", "22"}}
    # the code key otvety.py: (variant, label) -> (R key, index of the variant), only where its
    # parameters are the printed problem's (it is an older draft; the rest is named in ustarelo)
    ns = bez_zapisi(LG / "otvety.py", {})
    R = ns["R"]
    KOD = {("А", "1а"): ("1а", 0), ("А", "1б"): ("1б", 0), ("А", "2б"): ("2", 0), ("А", "3"): ("3", 0),
           ("А", "4а"): ("4а", 0), ("А", "4б"): ("4б", 0), ("А", "7"): ("7", 0), ("А", "8"): ("8", 0),
           ("А", "10а"): ("10а", 0), ("А", "10б"): ("10б", 0), ("А", "11б"): ("11б", 0),
           ("А", "13а"): ("13", 0, 0), ("А", "13б"): ("13", 0, 1), ("А", "13в"): ("13", 0, 2),
           ("А", "14б"): ("14", 0), ("А", "17а"): ("17", 0), ("А", "18а"): ("18а", 0),
           ("А", "18б"): ("18б", 0), ("А", "19а"): ("19а", 0), ("А", "19б"): ("19б", 0),
           ("Б", "1а"): ("1а", 1), ("Б", "1б"): ("1б", 1), ("Б", "2б"): ("2", 1), ("Б", "3"): ("3", 1),
           ("Б", "4а"): ("4а", 1), ("Б", "4б"): ("4б", 1), ("Б", "7"): ("7", 1), ("Б", "8"): ("8", 1),
           ("Б", "10б"): ("14", 1), ("Б", "11а"): ("17", 1),
           ("Б", "12а"): ("13", 1, 0), ("Б", "12б"): ("13", 1, 1), ("Б", "12в"): ("13", 1, 2),
           ("Б", "13а"): ("19а", 1), ("Б", "13б"): ("19б", 1), ("Б", "14а"): ("10а", 1),
           ("Б", "14б"): ("10б", 1), ("Б", "15а"): ("18а", 1), ("Б", "15б"): ("18б", 1)}
    # otvety.py entries whose problem the sheet prints with other numbers (not a second source)
    ustarelo.extend(["Л3 otvety.py 12а-12в (7s up to 100/1000; sheet А: up to 200/2000, Б: digit 4"
                     " up to 300/3000)", "Л3 otvety.py 11а/11б variant Б (28-25…; sheet Б17: 24, 21, 18)"])
    SPISKI = {("А", "5"): R["5спис"][0], ("Б", "5"): R["5спис"][1],
              ("А", "9"): R["9спис"][0], ("Б", "9"): R["9спис"][1]}

    def chist(c: str) -> str:
        c = re.sub(r"\\textbf\{([^}]*)\}", r"\1", c).replace("$", "").replace("\\,", "\u2009")
        c = c.replace("\\%", "%").replace("---", "—").replace("--", "–")
        return " ".join(c.split())

    tab = tex.read_text(encoding="utf-8").split("\\hline", 1)[1].split("\\end{tabular}")[0]
    for line in tab.splitlines():
        line = line.strip()
        m = re.match(r"(\d+)\s*&(.*)\\\\(\[\d+pt\])?$", line)
        if not m:
            continue
        num, rest = m.group(1), m.group(2)
        mc = re.match(r"\\multicolumn\{2\}\{(?:[^{}]|\{\})*\}\{(.*)\}\s*$", rest.strip())
        cells = {"А": mc.group(1), "Б": mc.group(1)} if mc else dict(zip(("А", "Б"), rest.split("&")))
        for v, cell in cells.items():
            labs = po_nomeru[v][num]
            parts = [p for p in cell.split("\\quad")]
            if len(labs) == 1:
                parts = [" ".join(parts)]
            if len(parts) != len(labs):
                raise SystemExit("Л3 %s %s: %d answers for %d items" % (v, num, len(parts), len(labs)))
            for lab, p in zip(labs, parts):
                otv = chist(re.sub(r"\s*\\ \s*", ", ", p))
                if (v, lab) in SPISKI:
                    # the list itself, from the code; the sheet's key prints the triples (5) or
                    # only their count (9) -- both must agree with the list
                    sp = SPISKI[(v, lab)]
                    assert (len(sp) == len(otv.split(", ")) and otv.split(", ") == ["".join(map(str, t)) for t in sp]
                            if lab == "5" else str(len(sp)) == otv), (v, lab, otv)
                    otv = "; ".join(" ".join(map(str, t)) for t in sp)
                if lab in NE[v]:
                    dobavit("LS-2026-09-22", v, lab, otv, None, "%s №%s, вариант %s" % (ist, num, v))
                    continue
                x = chislo_kluch(otv)
                if x is None:
                    raise SystemExit("Л3 %s %s: no number in %r" % (v, lab, otv))
                kod = KOD.get((v, lab))
                vt = None
                if kod:
                    val = R[kod[0]][kod[1]]
                    if len(kod) == 3:
                        val = val[kod[2]]
                    vt = Fraction(val)
                dobavit("LS-2026-09-22", v, lab, otv, x, "%s №%s, вариант %s" % (ist, num, v),
                        vt, "%s R[%r]" % (rel(LG / "otvety.py"), kod[0]) if kod else "")


# ============================================================ ДЗ1, к 29.09 (DZ-2026-09-29)
def dz1():
    tex = LG / "dz_22-09_podschety.tex"
    sostav = tex.read_text(encoding="utf-8").split("СОСТАВ v5", 1)[1].split("% Числа", 1)[0]
    tekst = {m.group(1): m.group(2) for m in re.finditer(r"^%\s+(\d)\s.*?\s(\d+)\s*$", sostav, re.M)}
    K = literal(I29 / "svod_dz.py", "K")
    NE = {"4", "5"}   # «выпишите все разложения», «нарисуйте все пентамино»: judged by the list (Р231)
    for p in sorted(tekst):
        ist = "%s, «СОСТАВ v5» №%s" % (rel(tex), p)
        if p in NE:
            dobavit("DZ-2026-09-29", "", p, tekst[p], None, ist)
        else:
            dobavit("DZ-2026-09-29", "", p, tekst[p], Fraction(tekst[p]), ist,
                    Fraction(K[p]), "%s K[%r]" % (rel(I29 / "svod_dz.py"), p))


# ============================================================ Л4, 29.09 (LS-2026-09-29)
def l4():
    kanon = I29 / "out" / "kanon.json"
    K = json.loads(kanon.read_text(encoding="utf-8"))["punkty"]
    NE = {"1", "5", "17", "18"}           # «выпишите все …» (1: list + count), «можно ли … приведите»
    for v in ("А", "Б"):
        for p in K[v]:
            lab, o = p["punkt"], p["otvet"]
            ist = "%s, %s %s" % (rel(kanon), v, lab)
            if lab in NE:
                dobavit("LS-2026-09-29", v, lab, o, None, ist)
                continue
            base = re.sub(r"\s*\((или|сумма)[^)]*\)", "", o).strip()
            x = chislo_kluch(base)
            if x is None and re.fullmatch(r"\d+/\d+", base):
                x = Fraction(base)
            if x is None:
                raise SystemExit("Л4 %s %s: no number in %r" % (v, lab, o))
            # the expression before «=» is evaluated: it must give the stated result
            vt = None
            if "=" in base:
                vt = vychislit(base.split("=")[-2])
            dobavit("LS-2026-09-29", v, lab, itog(base), x, ist, vt,
                    "the expression before «=» evaluated" if vt is not None else "")


# ============================================================ КР1, 29.09 (KR-2026-09-29)
def kr1():
    ns = {}
    src = (I29 / "kontr3.py").read_text(encoding="utf-8").split("def pole")[0]
    old, sys.stdout = sys.stdout, io.StringIO()
    try:
        exec(src, ns)
    finally:
        sys.stdout = old
    K = ns["K"]
    T = literal(I29 / "svod_kr.py", "K")
    NE = {"2а", "3а", "3б", "4а"}  # two numbers; breakdown by size / direction required; a list
    for v in ("А", "Б"):
        for lab, o in K[v]:
            ist = "%s K[%r] %s" % (rel(I29 / "kontr3.py"), v, lab)
            if lab in NE:
                if lab == "3а":       # the total and the breakdown, without the sum
                    o = itog(o.split("(")[0]) + " (" + o.split("(", 1)[1]
                if lab == "3б":
                    o = re.sub(r"(горизонтальных) \S+ = (\d+), (вертикальных) \S+ = (\d+)", r"\1 \2, \3 \4", o)
                dobavit("KR-2026-09-29", v, lab, o, None, ist)
                continue
            x = chislo_kluch(o)
            dobavit("KR-2026-09-29", v, lab, itog(o), x, ist, Fraction(T[v][lab]),
                    "%s K[%r][%r]" % (rel(I29 / "svod_kr.py"), v, lab))


# ============================================================ ДЗ2, к 6.10 (DZ-2026-10-06)
def dz2():
    txt = LG / "DZ-29-09-otvety.txt"
    m = modul(I29 / "dz_29-09_dannye.py")
    kod = {"2": Fraction(12000, 1000), "3": Fraction(101 - 22 - 29), "4": Fraction(m.A_prost),
           "5": Fraction(m.A_915), "6": Fraction(m.A_110)}
    src = (I29 / "dz_29-09_dannye.py").read_text(encoding="utf-8")
    assert "(16 * 14 + 16) * 50 == 12000" in src and "101 - 22 - 29 == 50" in src
    EDINICY = {"1": ("с", {"мин": 60, "с": 1}), "2": ("кг", {"кг": 1, "г": Fraction(1, 1000)})}
    for line in txt.read_text(encoding="utf-8").splitlines()[1:]:
        mm = re.match(r"(\d)\.\s*(.*?)\s*\[", line)
        if not mm:
            continue
        p, key = mm.group(1), mm.group(2)
        itog = key.split("=")[-1].split("(")[0].split(":")[0].strip()
        ist = "%s №%s" % (rel(txt), p)
        if p in EDINICY:
            base, ed = EDINICY[p]
            x = Fraction(0)
            for n, u in re.findall(r"(\d+(?: \d{3})*)\s*(мин|кг|с|г)(?![а-я])", itog):
                x += Fraction(n.replace(" ", "")) * ed[u]
            otv = itog
        else:
            x, otv = Fraction(itog), itog
        dobavit("DZ-2026-10-06", "", p, otv, x, ist, kod.get(p),
                "%s (asserts)" % rel(I29 / "dz_29-09_dannye.py") if p in kod else "")


# ============================================================ КР2, 6.10 (KR-2026-10-06)
def kr2():
    sys.path.insert(0, str(MASHINA))
    ns = bez_zapisi(I06 / "kr_kluch.py", {})
    ROWS, K = ns["ROWS"], ns["K"]
    sh = I06 / "out" / "SHPARGALKA-KR-06-10.html"
    h = sh.read_text(encoding="utf-8")
    tekst = {}
    for r in re.findall(r"<tr[^>]*>(.*?)</tr>", h, re.S):
        c = [html.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S)]
        if c and c[0] != "№":
            tekst[c[0].lstrip("△")] = (c[1], c[2])
    NE = {"4", "5а", "5б", "5в", "6б"}   # table, flags in letters, «выпишите все флаги», an explanation
    for (lab, a, b) in ROWS:
        lab = lab.lstrip("△")
        for v, val, t in (("А", a, tekst[lab][0]), ("Б", b, tekst[lab][1])):
            ist = "%s ROWS %s" % (rel(I06 / "kr_kluch.py"), lab)
            if lab == "11":             # (а), (б), (в) of one row: three numbers in order
                for l2, x, tx in zip("абв", str(val).split(", "), t.split(", ")):
                    dobavit("KR-2026-10-06", v, "11" + l2, x, Fraction(x), ist + l2,
                            Fraction(tx), "%s %s" % (rel(sh), "△11" + l2))
                continue
            if lab in NE:
                otv = str(val)
                if lab == "5в":
                    otv = "%s: %s" % (K[v]["5в"][0], K[v]["5в"][1])
                dobavit("KR-2026-10-06", v, lab, otv, None, ist)
                continue
            x = Fraction(val) if isinstance(val, int) else chislo_kluch(str(val))
            dobavit("KR-2026-10-06", v, lab, itog(str(val)), x, ist, chislo_kluch(t),
                    "%s %s" % (rel(sh), lab))


# ============================================================ Л5, 6.10 (ML-2026-10-06)
def l5():
    sys.path.insert(0, str(MASHINA))
    m = modul(I06 / "minilistok_06-10_dannye.py")
    T = literal(I06 / "raspoznavanie" / "svod_minilistok_6-10.py", "K")
    for v in ("А", "Б"):
        for i, x in enumerate(m.kluch(v), 1):
            dobavit("ML-2026-10-06", v, str(i), str(x), Fraction(x),
                    "%s kluch(%r)[%d]" % (rel(I06 / "minilistok_06-10_dannye.py"), v, i - 1),
                    Fraction(T[v][i - 1]), "%s K[%r][%d]" % (rel(I06 / "raspoznavanie" / "svod_minilistok_6-10.py"), v, i - 1))


def main() -> int:
    for f in (l3, dz1, l4, kr1, dz2, kr2, l5):
        f()
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["rabota_id", "variant", "punkt", "otvet", "chislo", "istochnik"])
        w.writeheader()
        w.writerows(rows)
    po = {}
    for r in rows:
        po.setdefault(r["rabota_id"], [0, 0])
        po[r["rabota_id"]][0] += 1
        po[r["rabota_id"]][1] += bool(r["chislo"])
    print("otvety.csv: %d rows (%s)" % (len(rows), ", ".join("%s %d, numeric %d" % (k, a, b) for k, (a, b) in po.items())))
    print("numbers confirmed by a second source: %d" % dvazhdy)
    print("code entries not the printed problem (not a second source): %d" % len(ustarelo))
    for u in ustarelo:
        print("   " + u)
    print("disagreements (rows NOT written): %d" % len(razoshlos))
    for r in razoshlos:
        print("   %s %s %s: key %s, second source %s (%s)" % r)
    return 1 if razoshlos else 0


if __name__ == "__main__":
    sys.exit(main())
