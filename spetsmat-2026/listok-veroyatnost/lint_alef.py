#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Рычаг к канону листка ℵ: краснеет там, где текст листка нарушает механически проверяемые правила.

    python3 lint_alef.py ЛИСТОК.tex [--logika LOGIKA-<листок>.md]

Коды — номера правил канона (скилл listok-alef, KANON-alef). Красное без --logika:
  К5.1  \\tekst объясняет модель («исход»/«равновероятн» рядом с «бросают»/«пут»);
  К5.3  «наблюдени…», «гипотез…» — спросите ответ прямо;
  К5.4  «Теорема.» или «Докажите теорему» в условии;
  К5.5  «Решите задачу N», «ответ задачи N» — надо «Найдите ответ в задаче N»;
  К5.6  «почему … равновероятн…» — вопрос с ответом внутри;
  К5.7  подсказка-вопрос в скобках «(…?)» внутри пункта;
  К5.9  «сравните», «где вы (уже) видели», «что вы замечаете», «почему совпал…»;
  К5.21 «простые дроби» — бессмысленное требование;
  К5.22 регистр пунктов: условие кончается «:» → пункты со строчной, «;», последний «.»; иначе с заглавной;
  К5.25 придуманный заголовок у \\nomer (короткая фраза с точкой без вопроса);
  К6.9  очевидное соглашение «C_0 = 1»;
  К6.10 неканонические термины: «дети» (надо «потомки»), «треугольник Дика», «циклический сдвиг», «Чжун»;
  К7.5  ◦ на номере задачи и ⋆ на пункте — значки тогда ставятся на пункты;
  К8.1  картинок меньше половины числа задач;
  К8.4  названа функция («графиком функции»), а графика с осями x, y в том же блоке нет;
  К9.9  \\obtek или wrapfigure в теле листка;
  К10.3 пустые слова: «утомительно», «давайте», «посмотрите на пример», «бросается в глаза»;
  К10.4 «угадайте» (надо «предположите»).
Красное с --logika (таблица задач LOGIKA; колонки ищутся по заголовку):
  К3.10 задача есть в листке, но нет в таблице (или наоборот); пустое «куда ведёт» у не-отступления;
  К7.1  ◦/† в листке не совпадают с колонкой «значок» (◦ на пункте делает задачу ◦);
  К4.3  отступление стоит не в конце листка.
  Старая таблица без колонки «значок» (18ℵ: «| № | роль | …») читается так: роль ◦/† — значок, остальное — функция.
Жёлтое (показать, где посмотреть):
  К5.3  в задаче нет ни «?», ни повеления (Докажите, Постройте, Выведите, Выпишите, Нарисуйте, Найдите);
  К5.24 «изменим условие задачи» — законно, только если вопрос тот же;
  К7.2  ⋆ в листке есть — их «практически может не быть»;
  К9.9  \\obtek или wrapfig остались в преамбуле.
Печатает нарушения с номером задачи и сводку; код возврата 1, если есть красное.
Это счётчик, не судья: держит только механику. Остальные правила канона — глазами (К11.7).
"""
import re
import sys
from pathlib import Path

KRASNOE = []
ZHELTOE = []
BLOK = r"\\(?:zad|nomer|zadp)\{(\d+)\}\{([^}]*)\}(.*?)(?=\\(?:zad|nomer|zadp)\{\d+\}|\Z)"
POVELENIYA = ("докажите", "постройте", "выведите", "выпишите", "нарисуйте", "найдите")


def zadachi(telo):
    """(номер, текст) для \\zad и блоков \\nomer…\\punkt."""
    out = []
    for m in re.finditer(r"\\zad\{(\d+)\}\{[^}]*\}\{", telo):
        out.append((m.group(1), skobki(telo, m.end() - 1)))
    for m in re.finditer(r"\\(?:nomer|zadp)\{(\d+)\}\{[^}]*\}(.*?)\\end\{samepage\}", telo, re.S):
        out.append((m.group(1), m.group(2)))
    return sorted(out, key=lambda p: int(p[0]))


def skobki(s, i):
    glub = 0
    for j in range(i, len(s)):
        if s[j] == "{" and s[j - 1] != "\\":
            glub += 1
        elif s[j] == "}" and s[j - 1] != "\\":
            glub -= 1
            if glub == 0:
                return s[i + 1:j]
    return s[i:]


def tablica(path):
    """{номер: (функция, значок, куда)} из таблицы задач LOGIKA; колонки — по строке заголовка."""
    out, kol = {}, None
    for stroka in Path(path).read_text(encoding="utf-8").splitlines():
        yach = [c.strip() for c in stroka.strip().strip("|").split("|")]
        if stroka.lstrip().startswith("|") and yach and yach[0] == "№":
            kol = {c: i for i, c in enumerate(yach)}
            continue
        if kol is None or not yach or not yach[0].isdigit():
            continue
        kuda = yach[kol["куда ведёт"]] if "куда ведёт" in kol else "?"
        if "значок" in kol:
            out[int(yach[0])] = (yach[kol["функция"]], yach[kol["значок"]], kuda)
        else:  # старая таблица 18ℵ: одна колонка «роль» несёт и значок, и функцию
            rol = yach[1]
            out[int(yach[0])] = (rol, rol if rol in ("◦", "†") else "", kuda)
    return out


LOGIKA = None


def main(path):
    tex = Path(path).read_text(encoding="utf-8")
    pre, telo = tex.split(r"\begin{document}", 1)
    # К5.1: теория объясняет модель
    for m in re.finditer(r"\\tekst\{", telo):
        t = skobki(telo, m.end() - 1)
        if any(w in t for w in ("исход", "равновероятн")) and ("бросают" in t or "пут" in t):
            KRASNOE.append(("К5.1", "теория", "объясняет исходы/равновероятность вместо эксперимента: " + t[:90] + "…"))
    z = zadachi(telo)
    for nomer, t in z:
        if re.search(r"\(\\textit\{Теорема", t) or "Теорема." in t or "Докажите теорему" in t:
            KRASNOE.append(("К5.4", nomer, "«Теорема» объявлена в условии"))
        if "простые дроби" in t or "простая дробь" in t:
            KRASNOE.append(("К5.21", nomer, "«простые дроби» — бессмысленное требование"))
        if "?" not in t and not any(w in t.lower() for w in POVELENIYA):
            ZHELTOE.append(("К5.3", nomer, "ни вопроса, ни повеления — есть ли конкретный вопрос?"))
    nizh = telo.lower()
    for kod, slova in (("К5.9", ("сравните", "что вы замечаете", "где вы уже видели", "где вы видели")),
                       ("К10.3", ("утомительно", "давайте", "посмотрите на пример", "бросается в глаза")),
                       ("К10.4", ("угадайте",))):
        for w in slova:
            if w in nizh:
                KRASNOE.append((kod, "текст", "«%s»" % w))
    if re.search(r"почему[^?]{0,40}совпал", nizh):
        KRASNOE.append(("К5.9", "текст", "«почему совпало» — связь ребёнок видит сам"))
    for w in ("наблюдени", "гипотез"):
        if w in nizh:
            KRASNOE.append(("К5.3", "текст", "«%s…» — спросите ответ прямо" % w))
    if re.search(r"почему[^?]{0,60}равновероятн", nizh):
        KRASNOE.append(("К5.6", "текст", "вопрос «почему … равновероятны» содержит ответ"))
    if re.search(r"решите\s+задач|ответ\s+задачи", nizh):
        KRASNOE.append(("К5.5", "текст", "надо «Найдите ответ в задаче N»"))
    if re.search(r"измен\w*\s+услови\w*\s+задач", nizh):
        ZHELTOE.append(("К5.24", "текст", "«изменим условие задачи» — законно, только если вопрос тот же"))
    for rx, chto in ((r"\bдет(и|ей|ям|ьми|ях)\b", "«дети» — надо «потомки»"),
                     (r"треугольник\w*\s+дика", "«треугольник Дика» — надо «треугольник Каталана»"),
                     (r"циклическ\w*\s+сдвиг", "«циклический сдвиг» — надо «циклическая лемма»"),
                     (r"чжун", "имя «Чжун» в листке излишне")):
        if re.search(rx, nizh):
            KRASNOE.append(("К6.10", "текст", chto))
    if re.search(r"C_0\s*=\s*1|C_\{0\}\s*=\s*1", telo):
        KRASNOE.append(("К6.9", "текст", "очевидное соглашение C_0=1"))
    if r"\obtek" in telo or r"\begin{wrapfigure}" in telo:
        KRASNOE.append(("К9.9", "текст", "обтекание \\obtek/wrapfigure — только \\sboku"))
    if r"\obtek" in pre or "wrapfig" in pre:
        ZHELTOE.append(("К9.9", "преамбула", "\\obtek/wrapfig остались в преамбуле — удалить при заведении листка"))
    zvezd = 0
    for blk in re.finditer(BLOK, telo, re.S):
        pm = re.findall(r"\\punkt\{[^}]*\}\{([^}]*)\}", blk.group(3))
        zvezd += (r"\star" in blk.group(2)) + sum(r"\star" in p for p in pm)
        if r"\circ" in blk.group(2) and any(r"\star" in p for p in pm):
            KRASNOE.append(("К7.5", blk.group(1), "◦ на задаче и ⋆ на пункте — значки ставятся на пункты"))
    if zvezd:
        ZHELTOE.append(("К7.2", "весь листок", "звёздочек: %d — их «практически может не быть»" % zvezd))
    # К5.22: регистр пунктов
    for blk in re.finditer(BLOK, telo, re.S):
        tekst = blk.group(3)
        if r"\punkt" not in tekst:
            continue
        usl = tekst.split(r"\punkt", 1)[0].rstrip().rstrip("}").rstrip()
        dvoet = usl.endswith(":")
        pts = [skobki(tekst, m.end() - 1) for m in re.finditer(r"\\punkt\{[^}]*\}\{[^}]*\}\{", tekst)]
        for i, pt in enumerate(pts):
            bukva = re.search(r"[A-Za-zА-Яа-яЁё]", re.sub(r"\$[^$]*\$|\\[A-Za-z]+", "", pt))
            if not bukva or pt.lstrip().startswith("$"):
                continue
            if dvoet != bukva.group(0).islower():
                KRASNOE.append(("К5.22", blk.group(1), "пункт %d: %s буква, а условие %s двоеточием" % (i + 1, "строчная" if bukva.group(0).islower() else "заглавная", "кончается" if dvoet else "не кончается")))
            if dvoet:
                konec = pt.rstrip()[-1:]
                nado = "." if i == len(pts) - 1 else ";"
                if konec != nado and not (konec == "?" and i == len(pts) - 1):
                    KRASNOE.append(("К5.22", blk.group(1), "пункт %d кончается «%s», нужно «%s»" % (i + 1, konec, nado)))
    for m in re.finditer(r"\\nomer\{(\d+)\}\{[^}]*\}\\hspace\{\\zazor\}([^{}]*?)\}", telo):
        g = m.group(2).strip()
        if g and len(g) < 45 and g.endswith(".") and "?" not in g and not g.startswith("("):
            KRASNOE.append(("К5.25", m.group(1), "придуманный заголовок «%s»" % g))
    for m in re.finditer(r"\\punkt\{([^}]*)\}\{[^}]*\}\{", telo):
        pt = skobki(telo, m.end() - 1)
        if re.search(r"\([^()]*\?\s*\)", pt):
            KRASNOE.append(("К5.7", "пункт " + m.group(1), "подсказка-вопрос в скобках"))
    # К8.4: названная функция — график в том же блоке (\celoe / \sboku)
    for m in re.finditer(r"графиком? функции", telo):
        nach = max(telo.rfind(r"\celoe{", 0, m.start()), telo.rfind(r"\sboku{", 0, m.start()))
        blok = ""
        if nach >= 0:  # все аргументы макроса: у \sboku их три, у \celoe один
            j = telo.index("{", nach)
            for _ in range(3 if telo.startswith(r"\sboku", nach) else 1):
                arg = skobki(telo, j); blok += arg; j = j + len(arg) + 2
                while j < len(telo) and telo[j] in " \n": j += 1
        # график = картинка с подписанными осями x и y (так рисует kartinki.py), а не любой рисунок рядом
        if nach < 0 or "{$y$}" not in blok:
            KRASNOE.append(("К8.4", "текст", "названа функция, а графика (оси x, y) рядом нет"))
    if LOGIKA:
        tab = tablica(LOGIKA)
        markery = {}
        for mm in re.finditer(r"\\(?:zad|nomer|zadp)\{(\d+)\}\{([^}]*)\}", telo):
            markery[int(mm.group(1))] = mm.group(2)
        for n in sorted(set(markery) ^ set(tab)):
            KRASNOE.append(("К3.10", n, "задача есть %s, но нет %s" % (("в листке", "в таблице логики") if n in markery else ("в таблице логики", "в листке"))))
        for blk in re.finditer(BLOK, telo, re.S):  # значок на пункте делает задачу носителем значка
            n = int(blk.group(1))
            for p in re.findall(r"\\punkt\{[^}]*\}\{([^}]*)\}", blk.group(3)):
                markery[n] += p
        for n in sorted(set(markery) & set(tab)):
            funk, znak, kuda = tab[n]
            if (r"\circ" in markery[n]) != ("◦" in znak) or (r"\dagger" in markery[n]) != ("†" in znak):
                KRASNOE.append(("К7.1", n, "значок в листке (%s) не совпадает с колонкой «значок» (%s)" % (markery[n] or "нет", znak or "пусто")))
            if not kuda.strip() and funk != "отступление":
                KRASNOE.append(("К3.10", n, "пустое «куда ведёт» — отступление или лишняя задача"))
        otst = [n for n, r in tab.items() if r[0] == "отступление"]
        ne_otst = [n for n, r in tab.items() if r[0] != "отступление"]
        if otst and ne_otst and min(otst) < max(ne_otst):
            KRASNOE.append(("К4.3", min(otst), "отступление стоит не в конце листка"))
    kartinok = telo.count(r"\begin{tikzpicture}")
    if kartinok * 2 < len(z):
        KRASNOE.append(("К8.1", "весь листок", "картинок %d при %d задачах — меньше половины" % (kartinok, len(z))))
    for uroven, spisok in (("КРАСНОЕ", KRASNOE), ("ЖЁЛТОЕ", ZHELTOE)):
        print("── %s: %d" % (uroven, len(spisok)))
        for p, n, s in spisok:
            print("  %s  задача %s: %s" % (p, n, s))
    print("задач: %d, картинок: %d" % (len(z), kartinok))
    return 1 if KRASNOE else 0


if __name__ == "__main__":
    if "--logika" in sys.argv:
        LOGIKA = sys.argv[sys.argv.index("--logika") + 1]
    sys.exit(main(sys.argv[1]))
