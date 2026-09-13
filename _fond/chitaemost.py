#!/usr/bin/env python3
"""Читаемость фонда: что из PDF можно взять машиной, а что только глазами.

Зачем. В фонде смешаны книги с живым текстовым слоем, книги с битой кодировкой
и сканы. По имени файла это не видно, а цена ошибки разная: из первых задачи
извлекаются командой, вторые лечатся перекодировкой, третьи требуют человека
или OCR. Прежде чем планировать работу с источником, надо знать, какой он.

Правило репозитория (KONSTITUCIYA §10): в документ пишется не число, а команда,
которая его считает. Этот файл и есть та команда.

Использование:
    python3 _fond/chitaemost.py                      # аудит всего фонда
    python3 _fond/chitaemost.py --tekst <pdf>        # текст с починкой кодировки
    python3 _fond/chitaemost.py --znamenskaya <pdf>  # разбор сборника на задачи

Вердикты:
    OK     текстовый слой живой — задачи извлекаются командой
    FIX    символы есть, но кодировка бита; --tekst чинит перекодировкой
    SCAN   текстового слоя нет: OCR или читать глазами постранично
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys

BIBL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "biblioteka")


def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, errors="replace").stdout


def pages(pdf):
    m = re.search(r"Pages:\s+(\d+)", _run(["pdfinfo", pdf]))
    return int(m.group(1)) if m else 0


def raw_text(pdf, layout=False):
    cmd = ["pdftotext"] + (["-layout"] if layout else []) + [pdf, "-"]
    return _run(cmd)


def cyr_share(s):
    """Доля кириллицы среди букв — так отличается живой текст от битой кодировки."""
    letters = sum(1 for c in s if c.isalpha())
    if not letters:
        return 0
    return round(100 * sum(1 for c in s if "Ѐ" <= c <= "ӿ") / letters)


def fix_encoding(s):
    """Чинит текст из PDF, собранных pdfTeX с cp1251-раскладкой.

    Байты cp1251 прочитаны как latin-1, поэтому обратный ход возвращает кириллицу.
    Проверено на Богомолове (0% → 98%) и Бабичевой (0% → 97%).
    Если не помогло — возвращаем как было, а не молча портим.
    """
    try:
        fixed = s.encode("latin-1", "ignore").decode("cp1251", "ignore")
    except Exception:
        return s
    return fixed if cyr_share(fixed) > cyr_share(s) else s


def text(pdf, layout=False):
    """Текст книги, по возможности читаемый."""
    t = raw_text(pdf, layout)
    return fix_encoding(t) if cyr_share(t) < 40 else t


def verdict(pdf):
    n = pages(pdf)
    t = raw_text(pdf)
    per = round(len(t) / n) if n else 0
    cyr = cyr_share(t)
    if per < 100:
        return "SCAN", n, per, cyr
    if cyr < 40:
        return ("FIX" if cyr_share(fix_encoding(t)) >= 40 else "SCAN"), n, per, cyr
    return "OK", n, per, cyr


def audit():
    files = sorted(glob.glob(os.path.join(BIBL, "*.pdf")))
    files += sorted(glob.glob(os.path.join(BIBL, "*", "*.pdf")))
    if not files:
        sys.exit(f"в {BIBL} нет pdf — фонд вне git, файлы могут отсутствовать на этой машине")
    rows = []
    print(f"{'файл':<58}{'стр':>5}{'зн/стр':>8}{'кир%':>6}  вердикт")
    print("-" * 92)
    for f in files:
        v, n, per, cyr = verdict(f)
        rows.append((f, v, n))
        print(f"{os.path.relpath(f, BIBL):<58}{n:>5}{per:>8}{cyr:>6}  {v}")
    print("-" * 92)
    print(f"ВСЕГО {len(rows)} файлов, {sum(r[2] for r in rows)} страниц")
    for v in ("OK", "FIX", "SCAN"):
        sel = [r for r in rows if r[1] == v]
        print(f"  {v:<5} {len(sel):>3} файлов / {sum(r[2] for r in sel):>5} страниц")
    scans = [os.path.relpath(r[0], BIBL) for r in rows if r[1] == "SCAN"]
    if scans:
        print("\nТолько глазами или через OCR:")
        for s in scans:
            print("  ·", s)


def znamenskaya(pdf, total=100):
    """Разбирает сборник «100 задач» на задачи, подсказки и ответы.

    Устройство сборника: три блока подряд, в каждом нумерация 1..100.
    Наивное деление «по сбросу номера» ломается — внутри условий и решений
    тоже встречаются строки, начинающиеся с числа. Поэтому идём жадно:
    берём номер, если он продолжает счёт, а дойдя до 100 — начинаем следующий
    блок. Мусор при этом проходит мимо.

    SLACK=2 — допуск на пропуск номера. Строгий счёт (slack=0) терял третий
    блок: в 4 классе он не находился вовсе (ответы есть, но один номер свёрстан
    иначе), в 1 классе обрывался на 52. С допуском в два номера оба собираются
    целиком, а на 2, 3 и 5 классе результат не меняется — проверено прогоном.
    """
    SLACK = 2
    t = raw_text(pdf, layout=True)
    t = re.sub(r"(?m)^\s*100 задач для \d класса\s*$", "", t)
    cands = [(int(m.group(1)), m.start(), m.end())
             for m in re.finditer(r"(?m)^\s{0,6}(\d{1,3})[.)]\s", t)]
    blocks, cur, expect = [], [], 1
    for num, st, en in cands:
        if expect <= num <= expect + SLACK:
            cur.append((num, st, en))
            expect = num + 1
            if expect > total:
                blocks.append(cur)
                cur, expect = [], 1
    if cur:
        blocks.append(cur)

    starts = [b[0][1] for b in blocks]
    out = []
    for bi, b in enumerate(blocks):
        d = {}
        stop = starts[bi + 1] if bi + 1 < len(starts) else len(t)
        for i, (num, st, en) in enumerate(b):
            end = b[i + 1][1] if i + 1 < len(b) else stop
            d[num] = " ".join(t[en:end].split())
        out.append(d)

    names = ["zadacha", "podskazka", "otvet"]
    merged = {}
    for n in range(1, total + 1):
        rec = {}
        for bi, key in enumerate(names):
            if bi < len(out) and n in out[bi]:
                rec[key] = out[bi][n]
        if rec.get("zadacha"):
            merged[n] = rec
    return merged, [len(b) for b in blocks]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tekst", metavar="PDF", help="печатает текст книги с починенной кодировкой")
    ap.add_argument("--znamenskaya", metavar="PDF", help="разбирает сборник «100 задач» в JSON")
    a = ap.parse_args()
    if a.tekst:
        sys.stdout.write(text(a.tekst, layout=True))
    elif a.znamenskaya:
        merged, sizes = znamenskaya(a.znamenskaya)
        sys.stderr.write(f"блоков: {sizes} · собрано задач: {len(merged)}\n")
        full = sum(1 for r in merged.values() if len(r) == 3)
        sys.stderr.write(f"из них с подсказкой И ответом: {full}\n")
        print(json.dumps(merged, ensure_ascii=False, indent=1))
    else:
        audit()


if __name__ == "__main__":
    main()
