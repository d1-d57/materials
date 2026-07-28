#!/usr/bin/env python3
"""Гейт предвёрсточной ленты (арка 6, G7). Печатает то, что заход требует напечатать,
и НЕ принимает на веру ни одного числа, вписанного руками.

    python3 teorkat-vvedenie/raskadrovka/gejt_lenty.py                       # наша лента
    python3 teorkat-vvedenie/raskadrovka/gejt_lenty.py --etalon              # эталон Паскаля из git

Линейка объявлена здесь, а не в отчёте, потому что в каноне её нет: замер «медиана 50 слов /
324 знака» снят неизвестным счётчиком, и сравнивать с ним можно только прогнав ТОТ ЖЕ счётчик
по эталону. Поэтому у скрипта два режима, и оба печатают одну и ту же линейку.

ЛИНЕЙКА (видимый текст слайда):
  - выбрасывается: фронтматтер, `# `-заголовок файла, все боковые поля `> поле:…`,
    блоки `<figure>…</figure>` и `<table>…</table>` целиком (в деке подписей не будет,
    а таблица — это иллюстрация слайда, не его проза);
  - `$$…$$` отдельной строкой считается за 3 слова и 120 знаков (две строки экрана с воздухом:
    длина исходника формулы к её месту на экране отношения не имеет);
  - `$…$` внутри строки считается за 1 слово, знаки — по длине без знаков доллара;
  - маркеры разметки (`**`, ведущий `- `, `·`) в знаки не идут.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEKSTY = ROOT / "teorkat-vvedenie" / "raskadrovka" / "teksty"
ETALON_COMMIT = "4833841"
ETALON_PATHS = [
    "lsh-2026-perechislitelnaya/otkrytaya-lekcia-paskal/raskadrovka/teksty/blok-1.md",
    "lsh-2026-perechislitelnaya/otkrytaya-lekcia-paskal/raskadrovka/teksty/blok-2.md",
]

DISPLAY_WORDS, DISPLAY_CHARS = 3, 120


def strip_blocks(lines):
    """Выбрасывает <figure>…</figure> и <table>…</table> целиком, вместе с содержимым."""
    out, depth = [], 0
    for ln in lines:
        low = ln.strip().lower()
        if depth == 0 and (low.startswith("<figure") or low.startswith("<table")):
            depth = 1
            if "</figure>" in low or "</table>" in low:
                depth = 0
            continue
        if depth:
            if "</figure>" in low or "</table>" in low:
                depth = 0
            continue
        out.append(ln)
    return out


def measure(lines):
    """→ (слов, знаков, число предложений, число блоков **acc**, число тире)."""
    words = chars = 0
    text_for_sent = []
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        if s.startswith(">") or s.startswith("<") or s.startswith("#"):
            continue
        if s.startswith("$$") and s.endswith("$$") and len(s) > 4:
            words += DISPLAY_WORDS
            chars += DISPLAY_CHARS
            continue
        inline = re.findall(r"\$[^$]+\$", s)
        bare = re.sub(r"\$[^$]+\$", " ", s)
        bare = bare.replace("**", "").replace("·", " ")
        bare = re.sub(r"^-\s+", "", bare)
        words += len([w for w in bare.split() if w]) + len(inline)
        chars += len(bare.strip()) + sum(len(f) - 2 for f in inline)
        text_for_sent.append(bare)
    joined = " ".join(text_for_sent)
    sentences = len([x for x in re.split(r"[.!?]+\s+|[.!?]+$", joined) if x.strip()])
    accents = sum(len(re.findall(r"\*\*[^*]+\*\*", ln)) for ln in lines if not ln.strip().startswith(">"))
    dashes = joined.count("—")
    return words, chars, sentences, accents, dashes


def parse(md_text, fname):
    """→ (tab, poryadok, [ {name, lines, layout, figures} ])."""
    body = md_text
    tab, order = fname, 999
    if body.startswith("---"):
        fm, _, body = body[3:].partition("\n---")
        for ln in fm.splitlines():
            if ln.startswith("tab:"):
                tab = ln.split(":", 1)[1].strip()
            if ln.startswith("poryadok:"):
                order = int(ln.split(":", 1)[1].strip())
    secs, cur = [], None
    for ln in body.splitlines():
        if ln.startswith("## "):
            cur = {"name": ln[3:].strip(), "raw": [], "file": fname, "tab": tab}
            secs.append(cur)
        elif cur is not None:
            cur["raw"].append(ln)
    for s in secs:
        s["layout"] = any(re.search(r"поле:mn\s+\*\*Раскладка\.\*\*", l) for l in s["raw"])
        s["figures"] = sum(1 for l in s["raw"] if "<svg" in l or "🖼" in l)
        s["lines"] = strip_blocks(s["raw"])
        s["w"], s["c"], s["sent"], s["acc"], s["dash"] = measure(s["lines"])
    return tab, order, secs


def load_ours():
    files = sorted(TEKSTY.glob("*.md"))
    got = [parse(p.read_text(encoding="utf-8"), p.name) for p in files]
    got.sort(key=lambda x: x[1])
    return got


def load_etalon():
    got = []
    for p in ETALON_PATHS:
        txt = subprocess.run(
            ["git", "--no-optional-locks", "show", "%s:%s" % (ETALON_COMMIT, p)],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout
        got.append(parse(txt, Path(p).name))
    got.sort(key=lambda x: x[1])
    return got


def median(xs):
    xs = sorted(xs)
    if not xs:
        return 0
    m = len(xs) // 2
    return xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2


def main():
    etalon = "--etalon" in sys.argv
    got = load_etalon() if etalon else load_ours()
    secs = [s for _, _, ss in got for s in ss]

    print("=" * 78)
    print("ЛЕНТА:", "ЭТАЛОН ПАСКАЛЯ (%s)" % ETALON_COMMIT if etalon else TEKSTY)
    print("=" * 78)
    print("%-4s %-34s %5s %6s %5s %4s %4s %4s" %
          ("#", "раздел", "слов", "знаков", "предл", "acc", "тире", "илл"))
    for i, s in enumerate(secs, 1):
        print("%-4d %-34s %5d %6d %5d %4d %4d %4d" %
              (i, s["name"][:34], s["w"], s["c"], s["sent"], s["acc"], s["dash"], s["figures"]))

    ws = [s["w"] for s in secs]
    cs = [s["c"] for s in secs]
    print("-" * 78)
    print("РАЗДЕЛОВ: %d   МЕДИАНА: %g слов / %g знаков   макс %d/%d   мин %d/%d"
          % (len(secs), median(ws), median(cs), max(ws), max(cs), min(ws), min(cs)))

    print("\nГИСТОГРАММА СЛОВ (шаг 15):")
    for lo in range(0, (max(ws) // 15 + 1) * 15, 15):
        n = len([w for w in ws if lo <= w < lo + 15])
        print("  %3d–%3d | %s %d" % (lo, lo + 14, "#" * n, n))

    print("\nВНЕ КОРИДОРА 45–57 СЛОВ (читаемый регистр):")
    out = [s for s in secs if not (45 <= s["w"] <= 57)]
    for s in out:
        print("   %-36s %4d слов  (%s)" % (s["name"][:36], s["w"], s["file"]))
    print("   ИТОГО вне коридора: %d из %d" % (len(out), len(secs)))

    print("\nАРХЕТИПНЫЕ ПОТОЛКИ (односторонние — обязаны быть 0):")
    print("   обложка (первый раздел) > 25 слов:",
          "❌ %d" % secs[0]["w"] if secs[0]["w"] > 25 else "✅ 0  (обложка: %d слов)" % secs[0]["w"])
    heavy = [s for s in secs[1:] if s["figures"] == 0 and s["c"] > 650]
    print("   text-only (без илл.) > 650 знаков:",
          "❌ %d — %s" % (len(heavy), ", ".join(s["name"][:24] for s in heavy)) if heavy else "✅ 0")

    print("\nРАСКЛАДКА:")
    nolay = [s for s in secs[1:] if not s["layout"]]
    print("   разделов без «поле:mn **Раскладка.**» (кроме обложки): %d %s"
          % (len(nolay), "— " + ", ".join(s["name"][:28] for s in nolay) if nolay else "✅"))

    print("\nИЛЛЮСТРАЦИИ:")
    noill = [s for s in secs[1:] if s["figures"] == 0]
    print("   слайдов без единой картинки: %d из %d" % (len(noill), len(secs) - 1))
    for s in noill:
        print("     · %s" % s["name"])

    print("\nСЦЕНОВЫЕ ШОРТКАТЫ (в ленте обязан быть НОЛЬ — это арка 8):")
    joined = "\n".join(l for s in secs for l in s["raw"])
    for pat in (r"\{@\d", r"\{blur@", r"\{fill@"):
        print("   %-10s %d" % (pat, len(re.findall(pat, joined))))

    print("\nПО ФАЙЛАМ:")
    for tab, order, ss in got:
        print("   %-2s %-34s разделов %2d · медиана %g слов"
              % (order, tab, len(ss), median([s["w"] for s in ss])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
