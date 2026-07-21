#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ассемблер карты областей. Читает _digest-parts/*.md, проверяет записи,
группирует по областям, печатает диагностику и пишет _tables.md
(готовые таблицы по областям — вставляются в KARTA-OBLASTEJ.md).

Числа отчёта берутся ОТСЮДА, а не из головы (KONSTITUCIYA §10).
Запуск: python3 _assemble.py
"""
import os
import re
import sys
from collections import Counter, OrderedDict, defaultdict

ZONE = os.path.dirname(os.path.abspath(__file__))
PARTS = os.path.join(ZONE, "_digest-parts")
IDS = os.path.join(ZONE, "_ids-229.txt")

FIELDS = ["id", "род", "область", "область-2", "суть", "эстет", "метка",
          "канал", "прок", "несёт", "статус+", "стар.", "связи"]
NF = len(FIELDS)

# Порядок областей в карте — от главной линии гипотезы к периферии
AREA_ORDER = [
    "комбинаторика", "теория-множеств", "линейная-алгебра", "теория-групп",
    "алгебра-общая", "теория-чисел", "логика", "информатика-и-типы",
    "топология", "геометрия", "анализ", "вероятность", "физика",
    "прикладное", "теория-категорий", "методика-курса",
]
ROD_OK = {"понятие", "мотивация", "утверждение", "пример", "сцена",
          "мостик", "затравка", "находка", "инструмент/донор"}
EST_OK = {"высокая-геометричная", "средняя", "сухая"}
MARK_OK = {"новый-взгляд", "незнакомый-объект", "нет"}
ST_OK = {"несёт-язык", "контекст", "за-потолком", "мёртвая-рамка", "под-ревизией"}


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def esc_cell(s):
    """Обезопасить `|` в ячейке таблицы, не сломав формулы."""
    def in_math(m):
        return m.group(0).replace("|", r"\vert ")
    s = re.sub(r"\$[^$]*\$", in_math, s)
    return s.replace("|", "\\|")


def load_records():
    recs, problems = [], []
    if not os.path.isdir(PARTS):
        sys.exit("нет папки _digest-parts")
    for fn in sorted(os.listdir(PARTS)):
        if not fn.endswith(".md"):
            continue
        src = fn[:-3]
        section = "records"
        for ln, line in enumerate(open(os.path.join(PARTS, fn), encoding="utf-8"), 1):
            line = line.rstrip("\n")
            if line.startswith("## РЁБРА"):
                section = "edges"
                continue
            if line.startswith("## ЗАМЕТКИ"):
                section = "notes"
                continue
            if line.startswith("## ИТОГО"):
                section = "done"
                continue
            if section != "records":
                continue
            if not line.strip() or line.startswith("#") or line.startswith(">"):
                continue
            if " | " not in line:
                continue
            # разделитель — именно ` | ` с пробелами: голый `|` встречается
            # внутри поля как LaTeX-модуль ($|A_x|$) и резать по нему нельзя
            parts = [norm(p) for p in line.split(" | ")]
            if len(parts) != NF:
                problems.append(f"{src}:{ln} полей {len(parts)}, ждали {NF}: {line[:90]}")
                continue
            r = dict(zip(FIELDS, parts))
            r["_src"] = src
            recs.append(r)
    return recs, problems


def main():
    authoritative = [l.strip() for l in open(IDS, encoding="utf-8") if l.strip()]
    auth_set = set(authoritative)
    recs, problems = load_records()

    seen, dupes = OrderedDict(), []
    for r in recs:
        if r["id"] in seen:
            dupes.append(r["id"])
        else:
            seen[r["id"]] = r

    missing = [i for i in authoritative if i not in seen]
    phantom = [i for i in seen if i not in auth_set]

    print("=" * 62)
    print(f"записей разобрано : {len(recs)}   уникальных id: {len(seen)}")
    print(f"узлов в картотеке : {len(authoritative)}")
    print(f"ПОКРЫТИЕ          : {len(auth_set & set(seen))} из {len(authoritative)}")
    print(f"пропущено         : {len(missing)}  {missing[:12]}")
    print(f"фантомных id      : {len(phantom)}  {phantom[:12]}")
    print(f"дублей            : {len(dupes)}  {dupes[:12]}")
    print(f"битых строк       : {len(problems)}")
    for p in problems[:15]:
        print("   !", p)

    def vocab_check(field, ok):
        bad = [(r["id"], r[field]) for r in seen.values()
               if r[field] not in ok and r[field] != "?"]
        if bad:
            print(f"  вне словаря {field}: {len(bad)} -> {bad[:6]}")
        return bad

    print("-" * 62)
    vocab_check("род", ROD_OK)
    vocab_check("эстет", EST_OK)
    vocab_check("метка", MARK_OK)
    vocab_check("статус+", ST_OK)

    by_area = defaultdict(list)
    for r in seen.values():
        by_area[r["область"]].append(r)

    print("-" * 62)
    print("ПО ОБЛАСТЯМ (основная):")
    for a, rs in sorted(by_area.items(), key=lambda kv: -len(kv[1])):
        flag = "" if a in AREA_ORDER else "   <-- вне базового списка"
        print(f"  {len(rs):4d}  {a}{flag}")
    print("-" * 62)
    for f in ("статус+", "канал", "несёт", "эстет", "метка", "род"):
        c = Counter(r[f] for r in seen.values())
        print(f"{f:9s}: " + " · ".join(f"{k}={v}" for k, v in c.most_common()))

    # гости: узлы, у которых область-2 указывает сюда
    guests = defaultdict(list)
    for r in seen.values():
        a2 = r["область-2"]
        if a2 and a2 not in ("—", "-", "нет", "?"):
            guests[a2].append(r)

    order = [a for a in AREA_ORDER if a in by_area]
    order += [a for a in sorted(by_area) if a not in AREA_ORDER]

    out = []
    for a in order:
        rs = sorted(by_area[a], key=lambda r: (r["статус+"] != "несёт-язык",
                                               r["эстет"] != "высокая-геометричная",
                                               r["id"]))
        out.append(f"\n<!-- AREA:{a} -->\n")
        out.append(f"**Узлов в области: {len(rs)}**"
                   + (f" · гостями из других областей: {len(guests.get(a, []))}" if guests.get(a) else "")
                   + "\n")
        out.append("| id | род | суть | эстет | метка | канал | прок | несёт | статус⁺ | стар. | связи |")
        out.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for r in rs:
            cells = [f"`{r['id']}`", r["род"], r["суть"], r["эстет"], r["метка"],
                     r["канал"], r["прок"], r["несёт"], r["статус+"], r["стар."],
                     r["связи"].replace(";", " ")]
            # `|` в ячейке рвёт колонку. Внутри $…$ экранировать через `\|` нельзя:
            # KaTeX рисует `\|` как двойную черту ‖ (норма), а нужен модуль |·| — там `\vert`.
            # Вне формул достаточно `\|`.
            out.append("| " + " | ".join(esc_cell(c) for c in cells) + " |")
        if guests.get(a):
            out.append("")
            out.append("*Гостями сюда заходят (основная область другая):* "
                       + ", ".join(f"`{g['id']}` ({g['область']})" for g in guests[a]))
        out.append("")

    with open(os.path.join(ZONE, "_tables.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("=" * 62)
    print(f"написано _tables.md — областей {len(order)}, строк {len(seen)}")


if __name__ == "__main__":
    main()
