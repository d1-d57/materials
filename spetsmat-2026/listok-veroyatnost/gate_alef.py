#!/usr/bin/env python3
"""ГЕЙТ К11.1 одной командой: листок ℵ перед показом владельцу — ЗЕЛЁНЫЙ или КРАСНЫЙ с причинами.

    python3 gate_alef.py ЛИСТОК.tex --logika LOGIKA.md --prov prov_….py [--stranic 4] [--sosed СОСЕД.tex ...]

Запускать из папки листка (рядом lint_alef.py, visyachie.py, polya.py, alef-istochnik/, ../format-179/).
Ничего в папке листка не меняет: всё собирается во временной папке.

Шаги (номера — пункты К11.1):
  7  исходник воспроизводит tex: kartinki.py + sobrat.py в копии alef-istochnik → cmp с ЛИСТОК.tex;
  1  lint_alef.py --logika → красного 0;
  2  prov → rc 0 и «ALL OK»;
  4  наша вёрстка (LuaLaTeX): ошибок 0, страниц --stranic, Overfull 0;
  7  перевод коллегам = файл ЛИСТОК-179.tex; переводы соседей (--sosed) не изменились;
  4  вёрстка коллег (pdflatex + format-179/maket-179.tex + tikz): страниц --stranic, Overfull 0 (К13.4, решение владельца 01.10);
  3  visyachie.py по обоим PDF;
  —  polya.py по обоим PDF (К9.7);
  5  разделитель «∗ ∗ ∗» не последний на странице (наша вёрстка);
  6  «Фамилия, имя» на стр. 3 обеих вёрсток и номер страницы внизу нашей (при 4 страницах).
Не проверяет (держится глазами, К11.1 п. 8–11): md5 доставки, рецензию, стилистику, осмотр страниц.
"""
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

KRASNOE = []


def zapusk(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, errors="replace")
    return r.returncode, r.stdout + r.stderr


def shag(nazv, ok, podrobno=""):
    print(("  ✅ " if ok else "  ❌ ") + nazv + ("" if ok or not podrobno else "\n       " + podrobno.strip().replace("\n", "\n       ")))
    if not ok:
        KRASNOE.append(nazv)


def stranic(pdf):
    rc, out = zapusk(["pdfinfo", str(pdf)])
    m = re.search(r"Pages:\s+(\d+)", out)
    return int(m.group(1)) if m else -1


def stranica(pdf, n):
    return zapusk(["pdftotext", "-layout", "-f", str(n), "-l", str(n), str(pdf), "-"])[1]


def main():
    ap = argparse.ArgumentParser(description="гейт К11.1 листка ℵ")
    ap.add_argument("tex")
    ap.add_argument("--logika", required=True)
    ap.add_argument("--prov", required=True)
    ap.add_argument("--stranic", type=int, default=4)
    ap.add_argument("--sosed", nargs="*", default=[], help="наши tex соседних листков: их перевод не должен измениться")
    a = ap.parse_args()
    tut = Path.cwd()
    tex = Path(a.tex).resolve()
    imya = tex.stem
    t179 = tex.with_name(imya + "-179.tex")
    perevod = tut / "../format-179/perevod.py"
    maket = tut / "../format-179/maket-179.tex"
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        print("ГЕЙТ К11.1:", tex.name)
        # 7: исходник воспроизводит tex
        ist = d / "ist"
        shutil.copytree(tut / "alef-istochnik", ist)
        rc1, o1 = zapusk([sys.executable, "kartinki.py"], cwd=ist)
        rc2, o2 = zapusk([sys.executable, "sobrat.py", str(tex), str(d / "sobrano.tex")], cwd=ist)
        same = rc1 == 0 and rc2 == 0 and (d / "sobrano.tex").read_bytes() == tex.read_bytes()
        shag("исходник alef-istochnik воспроизводит " + tex.name, same, o1 + o2 if not same else "")
        # 1: lint
        rc, out = zapusk([sys.executable, str(tut / "lint_alef.py"), str(tex), "--logika", a.logika])
        shag("lint_alef.py: красного 0", rc == 0, out.split("── ЖЁЛТОЕ")[0])
        zh = re.search(r"── ЖЁЛТОЕ: (\d+)", out)
        if zh and zh.group(1) != "0":
            print("     (жёлтого %s — посмотреть глазами: python3 lint_alef.py %s --logika …)" % (zh.group(1), tex.name))
        # 2: перебор
        rc, out = zapusk([sys.executable, a.prov])
        shag("перебор %s: ALL OK" % Path(a.prov).name, rc == 0 and "ALL OK" in out, out[-600:])
        # 4: наша вёрстка
        rc, out = zapusk(["lualatex", "-interaction=nonstopmode", "-halt-on-error",
                          "-output-directory=" + str(d), str(tex)], cwd=tut)
        nash = d / (imya + ".pdf")
        log = (d / (imya + ".log")).read_text(errors="replace") if (d / (imya + ".log")).exists() else ""
        shag("наша вёрстка собирается", rc == 0 and nash.exists(), "\n".join(l for l in log.splitlines() if l.startswith("!"))[:600])
        if nash.exists():
            n = stranic(nash)
            shag("наша вёрстка: страниц %d" % a.stranic, n == a.stranic, "страниц %d" % n)
            ov = re.findall(r"Overfull \\hbox \(([\d.]+)pt too wide\)[^\n]*lines? (\d+)", log)
            shag("наша вёрстка: Overfull 0", not ov, "; ".join("%s pt, строка %s" % p for p in ov))
        # 7: перевод коллегам и соседи
        rc, out = zapusk([sys.executable, str(perevod), str(tex), str(d / "t179.tex")])
        shag("перевод = %s" % t179.name, rc == 0 and t179.exists() and (d / "t179.tex").read_bytes() == t179.read_bytes(),
             out if rc else "файл отличается от свежего перевода — перевести заново perevod.py")
        for s in a.sosed:
            s = Path(s).resolve()
            rc, out = zapusk([sys.executable, str(perevod), str(s), str(d / ("s-" + s.name))])
            st = s.with_name(s.stem + "-179.tex")
            shag("перевод соседа %s не изменился" % s.name,
                 rc == 0 and st.exists() and (d / ("s-" + s.name)).read_bytes() == st.read_bytes(), out if rc else "отличается от " + st.name)
        # 4: вёрстка коллег
        mk = maket.read_text(encoding="utf-8")
        if "tikz" not in mk:
            mk = mk.replace(r"\usepackage{amsmath,amssymb}", r"\usepackage{amsmath,amssymb}\usepackage{tikz}", 1)
        (d / "maket.tex").write_text(mk, encoding="utf-8")
        rc, out = zapusk(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-jobname=ih",
                          r"\def\telo{%s}\input{maket.tex}" % t179], cwd=d)
        ih = d / "ih.pdf"
        logi = (d / "ih.log").read_text(errors="replace") if (d / "ih.log").exists() else ""
        oshibki = "\n".join(l for l in logi.splitlines() if l.startswith("!"))[:600]
        if "t2aenc.def" in oshibki:  # Cowork-машина владельца: pdfTeX без кириллицы (01.10)
            oshibki = "на этой машине у pdfTeX нет кириллицы (t2aenc.def) — вёрстку коллег здесь не проверить; гейт целиком — в облачной сессии"
        shag("вёрстка коллег собирается", rc == 0 and ih.exists(), oshibki)
        pdfy = [nash] if nash.exists() else []
        if ih.exists():
            pdfy.append(ih)
            n = stranic(ih)
            shag("вёрстка коллег: страниц %d" % a.stranic, n == a.stranic, "страниц %d" % n)
            ov = [float(x) for x in re.findall(r"Overfull \\hbox \(([\d.]+)pt too wide\)", logi)]
            shag("вёрстка коллег: Overfull 0 (К13.4, решение владельца 01.10)", not ov, "; ".join("%.1f pt" % x for x in ov))
        # 3 и поля
        if pdfy:
            rc, out = zapusk([sys.executable, str(tut / "visyachie.py")] + [str(p) for p in pdfy])
            shag("висячих строк нет (обе вёрстки)", rc == 0, out.replace(str(d) + "/", ""))
            rc, out = zapusk([sys.executable, str(tut / "polya.py")] + [str(p) for p in pdfy])
            shag("картинки в полях (обе вёрстки)", rc == 0, out.replace(str(d) + "/", ""))
        # 5, 6: наша вёрстка
        if nash.exists():
            plohie, bez_nomera = [], []
            for s in range(1, stranic(nash) + 1):
                stroki = [l.strip() for l in stranica(nash, s).splitlines() if l.strip()]
                if stroki and stroki[-1] == str(s):
                    stroki = stroki[:-1]
                else:
                    bez_nomera.append(s)
                if stroki and re.fullmatch(r"[∗*\s]+", stroki[-1]):
                    plohie.append(s)
            shag("разделитель не последний на странице", not plohie, "страницы: %s" % plohie)
            if a.stranic == 4:
                shag("номер страницы внизу (наша вёрстка)", not bez_nomera, "нет на страницах: %s" % bez_nomera)
        if a.stranic == 4:
            for p in pdfy:
                shag("«Фамилия, имя» на стр. 3 (%s)" % ("наша" if p == nash else "коллеги"), "Фамилия, имя" in stranica(p, 3))
    print("ГЕЙТ:", "ЗЕЛЁНЫЙ" if not KRASNOE else "КРАСНЫЙ — %d: %s" % (len(KRASNOE), "; ".join(KRASNOE)))
    print("Глазами (не автоматизировано): md5 доставки, рецензия, стилистика, осмотр страниц (К11.1 п. 8–11).")
    return 1 if KRASNOE else 0


if __name__ == "__main__":
    sys.exit(main())
