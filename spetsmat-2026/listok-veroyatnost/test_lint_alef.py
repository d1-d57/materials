#!/usr/bin/env python3
"""Проверка самого линтера: каждое правило краснеет на порче и молчит на чистом листке 18ℵ v21.

    python3 test_lint_alef.py      → «lint ALL OK», rc=0; иначе список сломанных правил, rc=1.

Берёт 18alef-veroyatnost.tex и LOGIKA-18alef.md, портит их по одному правилу за раз во временной папке
и проверяет, что lint_alef.py выдаёт именно этот код. Запускать после любой правки lint_alef.py.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

TUT = Path(__file__).resolve().parent
TEX = (TUT / "18alef-veroyatnost.tex").read_text(encoding="utf-8")
LOG = (TUT / "../zhurnal/2026-09-27_listok-18-veroyatnost/LOGIKA-18alef.md").read_text(encoding="utf-8")
NACH = r"\begin{document}"


def v_telo(tekst):
    """вставить фразу в условие задачи 1 (после «\\zad{1}{…}{»)."""
    m = re.search(r"\\zad\{1\}\{[^}]*\}\{", TEX)
    return TEX[:m.end()] + tekst + " " + TEX[m.end():]


def zapusk(tex, logika=LOG):
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "l.tex").write_text(tex, encoding="utf-8")
        (Path(d) / "L.md").write_text(logika, encoding="utf-8")
        r = subprocess.run([sys.executable, str(TUT / "lint_alef.py"), str(Path(d) / "l.tex"), "--logika", str(Path(d) / "L.md")],
                           capture_output=True, text=True)
    kras = r.stdout.split("── ЖЁЛТОЕ")[0]
    zhelt = r.stdout.split("── ЖЁЛТОЕ")[1] if "── ЖЁЛТОЕ" in r.stdout else ""
    return r.returncode, kras, zhelt


def stroka_tablicy(n, novaya):
    return re.sub(r"(?m)^\| %d \|.*$" % n, novaya, LOG)


PORCHI = [  # (код, уровень, испорченный tex, испорченная LOGIKA)
    ("К5.1", "к", TEX.replace(r"\tekst{", r"\tekst{Монету бросают, все исходы равновероятны. ", 1), LOG),
    ("К5.3", "к", v_telo("Сформулируйте гипотезу."), LOG),
    ("К5.4", "к", v_telo("Теорема. Всё верно."), LOG),
    ("К5.5", "к", v_telo("Решите задачу 1 при a=5."), LOG),
    ("К5.6", "к", v_telo("Почему они равновероятны?"), LOG),
    ("К5.7", "к", TEX.replace(r"\punkt{а}{}{", r"\punkt{а}{}{(может, по индукции?) ", 1), LOG),
    ("К5.9", "к", v_telo("Сравните с задачей 2."), LOG),
    ("К5.9", "к", v_telo("Почему ответы совпали?"), LOG),
    ("К5.21", "к", v_telo("Ответ — простые дроби."), LOG),
    ("К6.9", "к", v_telo("Считаем $C_0=1$."), LOG),
    ("К6.10", "к", v_telo("У вершины два ребёнка, т. е. дети."), LOG),
    ("К6.10", "к", v_telo("Треугольник Дика."), LOG),
    ("К9.9", "к", v_telo(r"\obtek{3}{x}"), LOG),
    ("К10.3", "к", v_telo("Давайте посчитаем."), LOG),
    ("К10.4", "к", v_telo("Угадайте ответ."), LOG),
    ("К5.24", "ж", v_telo("Изменим условие задачи 1."), LOG),
    ("К3.10", "к", TEX, stroka_tablicy(18, "")),
    ("К3.10", "к", TEX, stroka_tablicy(16, "| 16 | ◦ | IV | откуда | | нет |")),
    ("К7.1", "к", TEX, stroka_tablicy(16, "| 16 | ветка | IV | откуда | куда | нет |")),
    ("К4.3", "к", TEX, stroka_tablicy(2, "| 2 | отступление | I | откуда | куда | нет |").replace("| 2 | отступление", "| 2 | отступление", 1)),
]


def main():
    plohie = []
    rc, kras, zhelt = zapusk(TEX)
    if rc != 0:
        plohie.append("чистый листок v21 красный:\n" + kras)
    for kod, ur, tex, log in PORCHI:
        rc, kras, zhelt = zapusk(tex, log)
        gde = kras if ur == "к" else zhelt
        if "  %s " % kod not in gde or (ur == "к" and rc != 1):
            plohie.append("%s (%s) не сработал" % (kod, ur))
    # К7.5 и К7.2: ◦ на задаче, ⋆ на пункте
    tex = re.sub(r"(\\nomer\{16\}\{\\circ\}.*?\\punkt\{б\}\{)\}", r"\1\\star}", TEX, count=1, flags=re.S)
    if tex == TEX:
        plohie.append("К7.5: не нашёл «\\nomer{16}{\\circ} … \\punkt{б}{}» для порчи — тест устарел")
    else:
        rc, kras, zhelt = zapusk(tex)
        if "  К7.5 " not in kras:
            plohie.append("К7.5 не сработал")
        if "  К7.2 " not in zhelt:
            plohie.append("К7.2 (ж) не сработал")
    if plohie:
        print("lint СЛОМАН:\n  " + "\n  ".join(plohie))
        return 1
    print("lint ALL OK: %d порч поймано, чистый v21 зелёный" % (len(PORCHI) + 2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
