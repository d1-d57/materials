#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Листок в СТАРОМ формате Overleaf: в файле только задачи.

    python3 overleaf_export.py

Зачем. Наш .tex самодостаточен: он несёт свою преамбулу, свои окна, номера
в рамке и знаки уровня. Проект в Overleaf устроен иначе — там подключён
`my.sty`, задачи пишутся одной командой `\\problem`, а нумерацию, отступы
и шапку делает стиль. Файл одного формата в проекте другого не собирается
ни в ту, ни в другую сторону, поэтому здесь листок выпускается ВТОРОЙ раз —
в виде, который кладут в тот проект (владелец 04.09: «в файле с листком
должны быть только задачи, в старом формате»).

Чего этот вид НЕ несёт и почему: окна для плюса, кружки, кинжалы и звёздочки
живут в нашей преамбуле, а не в `my.sty`. Как они называются в стиле — из
PDF не видно, `my.sty` в репозитории нет. Пункты идут прозой «а) … б) …»,
как в прошлогодних файлах курса.
"""
import importlib.util
import re
from pathlib import Path

ZDES = Path(__file__).parent
# Базовый уровень живёт уже в markdown инструмента, второй — пока в питоне.
MD = ZDES.parents[2] / "disciplina/skills/sborka-listka/derevya.md"
INSTRUMENT = MD.parent / "tools/listok.py"


def dannye_iz_generatora(imya_fajla):
    spec = importlib.util.spec_from_file_location("gen", ZDES / imya_fajla)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def v_tex(t):
    """Разметка данных → TeX. Термин курсивом: жирного в старом формате нет."""
    t = re.sub(r"<t>(.+?)</t>", r"\\textit{\1}", t)
    # Термин в markdown-формате инструмента размечен двойными скобками.
    t = re.sub(r"\[\[(.+?)\]\]", r"\\textit{\1}", t)
    t = re.sub(r"<i>(.+?)</i>", r"\\textit{\1}", t)
    return t.replace("×", "$\\times$").replace("≥", "$\\geqslant$")


BUKVY = "абвгдеж"


def telo(zadachi, bullety):
    kuski = []
    for imya, _pismenno, uslovie, punkty, hvost in zadachi:
        stroki = []
        if uslovie:
            stroki.append(v_tex(uslovie))
        if punkty and imya in bullety:
            stroki[-1] += " " + " ".join("$\\bullet$ " + v_tex(p) for p in punkty)
        else:
            for i, p in enumerate(punkty):
                stroki.append("%s) %s" % (BUKVY[i], v_tex(p)))
        if hvost:
            stroki.append(v_tex(hvost))
        kuski.append("\\problem " + "\\\\\n".join(stroki))
    return "\n\n".join(kuski)


def iz_markdown(put):
    """Базовый уровень читаем ТЕМ ЖЕ парсером, что и сборка, а не своим:
    два читателя одного формата разъезжаются молча."""
    spec = importlib.util.spec_from_file_location("listok", INSTRUMENT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sheet = mod.parse_sheet(put)
    zadachi, bullety = [], set()
    for z in sheet.problems:
        zadachi.append((z.name, z.written, z.statement, list(z.parts), z.tail))
        if z.bulleted:
            bullety.add(z.name)
    return zadachi, bullety


if __name__ == "__main__":
    gen = dannye_iz_generatora("build_listok2.py")
    out = ZDES / "overleaf-16alpha.tex"
    out.write_text(telo(gen.ZADACHI, gen.BULLETY) + "\n", encoding="utf-8")
    print("  задач: %d → %s" % (len(gen.ZADACHI), out.name))

    zadachi, bullety = iz_markdown(MD)
    out = ZDES / "overleaf-16A.tex"
    out.write_text(telo(zadachi, bullety) + "\n", encoding="utf-8")
    print("  задач: %d → %s" % (len(zadachi), out.name))
