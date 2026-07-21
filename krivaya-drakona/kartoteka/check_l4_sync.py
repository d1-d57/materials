#!/usr/bin/env python3
"""ГЕЙТ СИНХРОНА УСЛОВИЙ Л4 — запускать после каждой правки любого из трёх файлов:

    python3 kartoteka/check_l4_sync.py

Зачем он есть. Одни и те же условия задач 23–26 лежат в ТРЁХ местах:
    kartoteka/L4-print-tmpl.html — ИСТОЧНИК того, что печатается (L4-print.html порождается);
    kartoteka/L4-listok.md    — то же плюс ответы, для преподавателя;
    L4/L4-usloviya.html       — то же на проектор.
Разъехаться им нельзя: у ребёнка на руках окажется одно условие, на экране другое, а в ключе
ответ к третьему. Держать три копии синхронными «внимательно» невозможно — поэтому машина.

⚠ Первая версия сравнения врала: теги срезались ДО подстановки пробела вместо <br>, и слова
склеивались («дракона.Сделай») — гейт кричал о расхождении там, где тексты совпадали буква
в букву. Гейт, ругающийся по неверной причине, хуже отсутствующего: ему перестают верить.
"""
import re, html, sys, pathlib

BASE = pathlib.Path(__file__).resolve().parent.parent
NUMS = range(23, 27)

def norm(t: str) -> str:
    """Текст условия без разметки. <br> — это АБЗАЦ, значит пробел, и снимать его надо ПЕРВЫМ."""
    t = re.sub(r'<br\s*/?>', ' ', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = html.unescape(t).replace(' ', ' ')
    return re.sub(r'\s+', ' ', t).strip()

def from_print():
    src = (BASE / 'kartoteka/L4-print-tmpl.html').read_text()
    return [norm(x) for x in re.findall(r'<li>(.*?)</li>', src, re.S)]

def from_key():
    src = (BASE / 'kartoteka/L4-listok.md').read_text().split('## Ответы подробно')[0]
    out = []
    for n in NUMS:
        m = re.search(r'(?m)^\*\*%d\.\*\* (.*?)$' % n, src)
        out.append(norm(m.group(1)) if m else None)
    return out

def from_screen():
    """На экране первым слайдом идёт ОПРЕДЕЛЕНИЕ кривой (помечено def:true) — оно не задача
    и в сверку не входит. Печатный листок несёт его же, но в шапке, а не в списке задач."""
    src = (BASE / 'L4/L4-usloviya.html').read_text()
    out = []
    for entry in re.findall(r"\{ n:.*?\},\n", src, re.S):
        if 'def:true' in entry:
            continue
        m = re.search(r"t:'(.*?)' \}", entry, re.S)
        if m:
            out.append(norm(m.group(1)))
    return out

def main():
    got = {'печать': from_print(), 'ключ': from_key(), 'экран': from_screen()}
    bad = []
    for name, lst in got.items():
        if len(lst) != len(NUMS):
            bad.append(f'{name}: условий {len(lst)}, а должно быть {len(NUMS)}')
    if bad:
        print('ГЕЙТ СИНХРОНА ПРОВАЛЕН:\n  ' + '\n  '.join(bad)); sys.exit(1)
    for i, n in enumerate(NUMS):
        vals = {k: v[i] for k, v in got.items()}
        if len(set(vals.values())) == 1:
            print(f'  ✓ задача {n}: три места совпадают ({len(vals["печать"])} знаков)')
        else:
            bad.append(f'задача {n} разъехалась:')
            for k, v in vals.items():
                bad.append(f'    {k:8s}: {v[:150]}')
    print('\nГЕЙТ СИНХРОНА ПРОЙДЕН — печать, ключ и экран несут одно и то же'
          if not bad else 'ГЕЙТ СИНХРОНА ПРОВАЛЕН:\n  ' + '\n  '.join(bad))
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
