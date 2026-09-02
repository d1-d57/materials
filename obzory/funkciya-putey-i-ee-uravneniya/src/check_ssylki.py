#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ГЕЙТ НЕПРОТУХАЮЩИХ ССЫЛОК: имя блока — истина, номер — только вид.

    python3 check_ssylki.py <скелет.md> [ссылающийся.md ...]   # rc=0 зелёный, rc=1 красный

🔴 ЗАЧЕМ. `SVEDENIE-kursa.md` ссылался на «Т9, Т12, У14–У25» прежней редакции
скелета. Скелет перенумеровали — документ стал указывать в пустоту, и НИ ОДИН
гейт этого не увидел: номер это просто число, у него нет адресата, промах
номером неотличим от попадания. Владелец 2026-09-02: «нумерация должна быть
устроена как ссылка… чтобы она не могла протухнуть».

УСТРОЙСТВО. У каждого блока два атрибута, и они разного рода:
  ИМЯ   — слаг в комментарии сразу за заголовком: `**Теорема 20 (…).** <!--id: chebyshev-->`
          Имя не меняется никогда; оно и есть личность блока.
  НОМЕР — порядок чтения. Подвижен по устройству: вставили блок — номера поехали.
Ссылка пишется ИМЕНЕМ, номер идёт справочно в скобках: `chebyshev (20)`.
Тогда протухнуть может только скобка — и её ловит проверка С3, которая сверяет
её с живым номером носителя имени.

Что судит:
  С1  каждое имя объявлено ровно один раз (во всех поданных файлах сразу).
  С2  каждая ссылка разрешается в объявленное имя — внутри файла и между файлами.
  С3  справочный номер в скобках равен живому номеру блока с этим именем.
  С4  у каждого утверждения и теоремы есть строка «опирается», и она не пуста;
      определения строки «опирается» не несут.
  С5  ссылок найдено больше нуля. Гейт, который ничего не нашёл, зелёным
      не бывает: ровно так граф ссылок был зелёным 2026-08-25, не видя ничего.

⚠ ОБЪЯВЛЕННАЯ СЛЕПАЯ ЗОНА. Гейт НЕ судит, УМЕСТНА ли ссылка по смыслу и не
пропущена ли нужная. Он судит только разрешимость: указывает ли ссылка во
что-то живое. Прозаические упоминания «по теореме 22» внутри тела проверяются
как номера (С3-prose) — они разрешаются в блок с таким номером, но личности
не несут и при перенумерации молча уедут; поэтому в новых текстах их место
занимают имена.
"""
import re
import sys
from pathlib import Path

ZHANRY = r"(?:Определение|Утверждение|Теорема|Лемма|Предложение|Следствие)"
# заголовок блока с именем: **Теорема 20 (…).** <!--id: chebyshev-->
ZAGOLOVOK = re.compile(
    r"^\*\*(%s)\s+(\d+)\s*\(([^)]*)\)\.\*\*\s*<!--\s*id:\s*([a-z0-9-]+)\s*-->" % ZHANRY,
    re.M)
# заголовок блока БЕЗ имени — отдельная жалоба, иначе блок молча выпадет из графа
ZAGOLOVOK_BEZ = re.compile(r"^\*\*(%s)\s+(\d+)\s*\(([^)]*)\)\.\*\*(?!\s*<!--\s*id:)" % ZHANRY, re.M)
OPIRAETSYA = re.compile(r"^опирается:\s*(.+)$", re.M)
# 🔴 Ссылки НЕ ищутся вольным грепом по всему тексту. Первая редакция гейта искала
# `имя (номер)` регекспом, требующим дефис в имени, — и не видела однословных имён
# (`chebyshev`, `spektr`, `obekt`): 38 ссылок вместо 72, то есть половина графа
# оставалась непроверенной при зелёном гейте. Область поиска сужена до двух мест,
# где ссылка ЗАЯВЛЕНА как ссылка:
#   * строка `опирается:` — граф скелета, имена через запятую;
#   * форма `[#имя]` — ссылка из любого другого файла в любом месте текста.
# Расширять область вольным регекспом нельзя: латинское слово перед числом в скобках
# встречается в математическом тексте и станет ложной битой ссылкой.
SSYLKA_ELEM = re.compile(r"^([a-z][a-z0-9-]*)\s*(?:\((\d+)\))?$")
# ссылка из чужого файла: [#имя] или [#имя] (20)
SSYLKA_KV = re.compile(r"\[#([a-z0-9-]+)\](?:\s*\((\d+)\))?")


def sobrat_imena(fajly):
    """имя → (номер, жанр, файл). Дубли собираются отдельно: одно имя, два носителя
    хуже отсутствующего имени — ссылка разрешается, но не туда."""
    imena, dubli, bez_imeni = {}, [], []
    for p in fajly:
        text = p.read_text(encoding="utf-8")
        for m in ZAGOLOVOK.finditer(text):
            zhanr, nomer, _, imya = m.groups()
            if imya in imena:
                dubli.append((imya, imena[imya][2].name, p.name))
            else:
                imena[imya] = (int(nomer), zhanr, p)
        for m in ZAGOLOVOK_BEZ.finditer(text):
            bez_imeni.append("%s: %s %s" % (p.name, m.group(1), m.group(2)))
    return imena, dubli, bez_imeni


def sobrat_ssylki(fajly):
    """Все ссылки во всех поданных файлах: (имя, справочный номер или None, откуда)."""
    out, mus = [], []
    for p in fajly:
        for i, stroka in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            gde = "%s:%d" % (p.name, i)
            mo = OPIRAETSYA.match(stroka)
            if mo:
                for elem in mo.group(1).split(","):
                    elem = elem.strip()
                    if not elem:
                        continue
                    me = SSYLKA_ELEM.match(elem)
                    if me:
                        out.append((me.group(1),
                                    int(me.group(2)) if me.group(2) else None, gde))
                    else:
                        # неразобранный элемент — не «ссылок нет», а порча формы:
                        # молчать о нём значит повторить провал первой редакции
                        mus.append((elem, gde))
            for m in SSYLKA_KV.finditer(stroka):
                out.append((m.group(1), int(m.group(2)) if m.group(2) else None, gde))
    return out, mus


def opiraetsya_est(skelet):
    """С4: строк «опирается» ровно столько, сколько утверждений и теорем."""
    text = skelet.read_text(encoding="utf-8")
    utv = len(re.findall(r"^\*\*(?:Утверждение|Теорема)\s+\d+", text, re.M))
    stroki = [m.group(1).strip() for m in OPIRAETSYA.finditer(text)]
    pustye = [s for s in stroki if not s]
    return utv, len(stroki), pustye


def main(argv):
    if not argv:
        print(__doc__)
        return 0
    fajly = [Path(a) for a in argv]
    net = [p for p in fajly if not p.is_file()]
    if net:
        print("НЕ НАЙДЕНЫ: %s" % ", ".join(str(p) for p in net))
        return 2

    imena, dubli, bez_imeni = sobrat_imena(fajly)
    ssylki, mus = sobrat_ssylki(fajly)
    utv, strok, pustye = opiraetsya_est(fajly[0])

    bitye = [(im, gde) for im, _, gde in ssylki if im not in imena]
    protuhli = [(im, n, imena[im][0], gde)
                for im, n, gde in ssylki
                if im in imena and n is not None and n != imena[im][0]]

    print("── ГЕЙТ ССЫЛОК (check_ssylki) ──")
    print("  файлов: %d · имён объявлено: %d · ссылок найдено: %d"
          % (len(fajly), len(imena), len(ssylki)))
    krasnye = 0

    print("  С1 имя объявлено один раз:     дублей %d                %s"
          % (len(dubli), "✅" if not dubli else "❌"))
    if dubli:
        krasnye += 1
        for imya, a, b in dubli:
            print("     дубль «%s»: %s и %s" % (imya, a, b))
    if bez_imeni:
        krasnye += 1
        print("  С1 блоки БЕЗ имени:            %d                       ❌" % len(bez_imeni))
        for s in bez_imeni[:10]:
            print("     %s" % s)

    print("  С2 ссылка разрешается в имя:   битых %d                 %s"
          % (len(bitye), "✅" if not bitye else "❌"))
    if bitye:
        krasnye += 1
        for im, gde in bitye[:14]:
            print("     %s ← %s" % (im, gde))
    if mus:
        krasnye += 1
        print("  С2 неразобранных элементов «опирается»: %d            ❌" % len(mus))
        for elem, gde in mus[:14]:
            print("     «%s» ← %s" % (elem, gde))

    print("  С3 справочный номер совпал:    протухших %d             %s"
          % (len(protuhli), "✅" if not protuhli else "❌"))
    if protuhli:
        krasnye += 1
        for im, bylo, stalo, gde in protuhli[:14]:
            print("     %s: в ссылке (%d), живой номер %d ← %s" % (im, bylo, stalo, gde))

    c4 = (strok == utv) and not pustye
    print("  С4 «опирается» у каждого утв.: строк %d, утверждений %d  %s"
          % (strok, utv, "✅" if c4 else "❌"))
    if not c4:
        krasnye += 1
        if pustye:
            print("     пустых строк «опирается»: %d" % len(pustye))

    c5 = len(ssylki) > 0
    print("  С5 ссылок найдено больше нуля: %d                       %s"
          % (len(ssylki), "✅" if c5 else "❌"))
    if not c5:
        krasnye += 1

    print("  ⚠ НЕ судит: уместность ссылки по смыслу и полноту графа.")
    print("%s ССЫЛКИ: красных %d" % ("✅" if not krasnye else "❌", krasnye))
    return 0 if not krasnye else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
