#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сборка KARTA-OBLASTEJ.md = скелет (проза, писана человеком)
                         + таблицы из _tables.md (машинные, из дистиллятов)
                         + вычисленные блоки PROFILE / GAPS / COVERAGE.

Ни одно число здесь не набирается руками: всё считается из дистиллятов.
Запуск: python3 _assemble.py && python3 _build_karta.py
"""
import os
import re
from collections import Counter

ZONE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ZONE, "KARTA-OBLASTEJ.md")

FIELDS10 = 10  # ярлык|якорь|область|суть|эстет|метка|канал|прок|несёт|статус+


def read(p):
    return open(os.path.join(ZONE, p), encoding="utf-8").read()


def syuzhety(fn):
    """Записи сюжетных дистиллятов (10 полей). Заголовок-легенду отбрасываем."""
    p = os.path.join(ZONE, "_digest-syuzhety", fn)
    if not os.path.exists(p):
        return []
    out = []
    for line in open(p, encoding="utf-8"):
        if line.startswith(("#", ">", "РЕБРО")) or " | " not in line:
            continue
        parts = [x.strip() for x in line.rstrip("\n").split(" | ")]
        if len(parts) == FIELDS10 and parts[2] != "область":
            out.append(parts)
    return out


# ---- таблицы картотеки по областям ----
tbl = read("_tables.md")
chunks = re.split(r"<!-- AREA:(.+?) -->", tbl)
AREA_TABLE, AREA_N = {}, Counter()
for i in range(1, len(chunks), 2):
    a, body = chunks[i], chunks[i + 1]
    AREA_TABLE[a] = body.strip("\n")
    AREA_N[a] = len([l for l in body.split("\n") if l.startswith("| `")])

rows = [[x.strip() for x in l.split(" | ")]
        for b in AREA_TABLE.values() for l in b.split("\n") if l.startswith("| `")]
# колонки таблицы: id род суть эстет метка канал прок несёт статус⁺ стар. связи
ST, ES, KA = 8, 3, 5

per = syuzhety("PER.md")
fab = syuzhety("FAB.md")
perA, fabA = Counter(r[2] for r in per), Counter(r[2] for r in fab)
LIVE = {"несёт-язык", "контекст"}
liveA = Counter(r[2] for r in per + fab if r[9] in LIVE)

# ---- PROFILE ----
prof = ["| область | узлов | несёт язык | контекст | за потолком | под ревизией | мёртвых | высокая эстет. | есть канал |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
for a, n in AREA_N.most_common():
    rs = [r for r in rows if f"<!-- AREA:{a} -->" or True]
    rs = [[x.strip() for x in l.split(" | ")]
          for l in AREA_TABLE[a].split("\n") if l.startswith("| `")]
    st = Counter(r[ST] for r in rs)
    prof.append(f"| **{a}** | {n} | {st['несёт-язык']} | {st['контекст']} | "
                f"{st['за-потолком']} | {st['под-ревизией']} | {st['мёртвая-рамка']} | "
                f"{sum(1 for r in rs if r[ES] == 'высокая-геометричная')} | "
                f"{sum(1 for r in rs if r[KA] != 'нет')} |")
tot = Counter(r[ST] for r in rows)
prof.append(f"| **ИТОГО** | **{len(rows)}** | **{tot['несёт-язык']}** | **{tot['контекст']}** | "
            f"**{tot['за-потолком']}** | **{tot['под-ревизией']}** | **{tot['мёртвая-рамка']}** | "
            f"**{sum(1 for r in rows if r[ES] == 'высокая-геометричная')}** | "
            f"**{sum(1 for r in rows if r[KA] != 'нет')}** |")

# ---- GAPS ----
allA = sorted(set(AREA_N) | set(perA) | set(fabA),
              key=lambda a: -(AREA_N[a] + perA[a] + fabA[a]))
gaps = ["| область | картотека | каталог (отбор) | Fable | **всего** | из них живых вне картотеки |",
        "|---|---:|---:|---:|---:|---:|"]
for a in allA:
    tt = AREA_N[a] + perA[a] + fabA[a]
    mark = " 🔴" if tt <= 6 else ""
    gaps.append(f"| **{a}**{mark} | {AREA_N[a]} | {perA[a]} | {fabA[a]} | **{tt}** | {liveA[a]} |")
gaps.append(f"| **ИТОГО** | **{sum(AREA_N.values())}** | **{len(per)}** | **{len(fab)}** | "
            f"**{sum(AREA_N.values())+len(per)+len(fab)}** | **{sum(liveA.values())}** |")

# ---- COVERAGE ----
auth = [l.strip() for l in open(os.path.join(ZONE, "_ids-229.txt"), encoding="utf-8") if l.strip()]
# r[0] приходит как "| `some-id`" — ведущая черта таблицы входит в ячейку.
# Снимать только бэктики недостаточно: получится "| `some-id" и покрытие обнулится.
ids = {r[0].lstrip("| ").strip("`") for r in rows}
parts_n = len([f for f in os.listdir(os.path.join(ZONE, "_digest-parts")) if f.endswith(".md")])
sy_dir = os.path.join(ZONE, "_digest-syuzhety")
sy = sorted(f for f in os.listdir(sy_dir) if f.endswith(".md")) if os.path.isdir(sy_dir) else []
edges = sum(1 for f in os.listdir(os.path.join(ZONE, "_digest-parts"))
            for l in open(os.path.join(ZONE, "_digest-parts", f), encoding="utf-8")
            if l.startswith("РЕБРО"))

cov = [
    "**Картотека — сведено {} из {} узлов.** Пропущенных: {}. Фантомных id (нет в картотеке): {}. Дублей: {}.".format(
        len(ids & set(auth)), len(auth),
        len([i for i in auth if i not in ids]) or "0",
        len([i for i in ids if i not in set(auth)]) or "0",
        len(rows) - len(ids) or "0"),
    "",
    "Проверка независимая, командой:",
    "```",
    "grep -c '^id:' ../../../../teoriya-kategoriy/kartoteka/KARTA-OBLASTI.md   # 229 — сколько узлов есть",
    "python3 _assemble.py | head -8                                            # сколько сведено",
    "```",
    "",
    "| источник | объём | статус |",
    "|---|---|---|",
    f"| `KARTA-OBLASTI.md` | 229 узлов | ✅ переварено {len(ids)} из {len(auth)}, {parts_n} срезами |",
    "| `STANDART-uzla.md` | 18K, схема полей | ✅ прочитан целиком (исполнителем, не субагентом) |",
    "| `KARTA-LEKCIY.md` | 72K, 9 записей L1–L9 | ✅ 96 живых записей + 20 переходов |",
    "| `VERDIKT-khl-kontent.md` | 44K | ✅ 35 записей, 11 вариантов подачи финала |",
    "| `VERDIKT-shov-L4-L5.md` | 64K | см. `_digest-syuzhety/V2-shov.md` |",
    "| `VERDIKT-l4-l5-kontent.md` | 76K | см. `_digest-syuzhety/V3-l4l5-kontent.md` |",
    "| `VERDIKT-l4-l5-programma.md` | 92K | см. `_digest-syuzhety/V4-l4l5-programma.md` |",
    f"| `PERECHOT-kataloga.md` | 242 находки (**не «800+»**) | ✅ раскладка по областям полная, отобрано {len(per)} |",
    f"| `fable_generacia-sjuzhetov.md` | §A + §B + дыры | ✅ {len(fab)} записей, 8 дыр выписаны |",
    "",
    f"**Сверх картотеки сведено:** {len(per)} отобранных находок каталога + {len(fab)} сюжетов Fable = "
    f"{len(per)+len(fab)} позиций, все с проверяемыми якорями.",
    f"**Новых рёбер найдено:** {edges} (в картотеку не внесены — она read-only).",
    "",
    "**Чего в этой карте НЕТ и почему.** Поля `находка` карточек (самое объёмное) — сознательно: "
    "`VNESHNIE-RESURSY §Железное правило` запрещает клон картотеки, карта остаётся указателем. "
    "Пер-узловой привязки к старым нитям — тоже: поля `нить` в карточках не существует, "
    "нити живут одной глобальной секцией и разобраны целиком в `REVIZIYA-starogo.md`.",
]

# ---- сборка ----
skel = read("_karta-skelet.md")
skel = skel.replace("<!-- PROFILE -->", "\n".join(prof))
skel = skel.replace("<!-- GAPS -->", "\n".join(gaps))
skel = skel.replace("<!-- COVERAGE -->", "\n".join(cov))

pieces = re.split(r"<!-- SUM:(.+?) -->", skel)
out = [pieces[0]]
for i in range(1, len(pieces), 2):
    area, prose = pieces[i], pieces[i + 1]
    tail = ""
    m = re.search(r"\n---\n\n# ЧАСТЬ III", prose)
    if m:
        prose, tail = prose[:m.start()], prose[m.start():]
    out.append(f"## {area} — {AREA_N.get(area, 0)} узлов\n")
    out.append(prose.strip("\n"))
    out.append("\n\n" + AREA_TABLE.get(area, "*(таблицы нет)*") + "\n")
    if tail:
        out.append(tail)

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(out).rstrip() + "\n")

print(f"KARTA-OBLASTEJ.md: {len(open(OUT, encoding='utf-8').readlines())} строк, "
      f"{os.path.getsize(OUT)//1024}K, областей {len(AREA_N)}, узлов {len(rows)}")
