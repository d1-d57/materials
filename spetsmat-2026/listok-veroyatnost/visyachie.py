"""Рычаг «нет висячих строк» (владелец, 01.10 13:02: «не нравятся некрасивые переносы»).
Краснеет, если в PDF строка из одного короткого слова/формулы стоит после полной строки.
Запуск: python3 visyachie.py листок.pdf [листок-179-pechat.pdf ...]   → rc=1 при находке.
Эвристика по pdftotext: строка ≤ 14 символов после строки > 60 символов; номера страниц,
разделители «∗ ∗ ∗», номера задач и дроби из выключных формул отсеиваются."""
import re, subprocess, sys
rc = 0
for f in sys.argv[1:]:
    L = [l.rstrip() for l in subprocess.run(["pdftotext", f, "-"], capture_output=True, text=True).stdout.splitlines()]
    for i in range(1, len(L)):
        t, prev = L[i].strip(), L[i-1].strip()
        if not (0 < len(t) <= 14 and len(prev) > 60):
            continue
        if t.isdigit() or "∗" in t or re.fullmatch(r"\d+[†◦]?", t) or not re.search(r"[а-яА-Яa-zA-Z]{3}", t):
            continue  # номер, разделитель, обрывок формулы
        if len(t.split()) >= 2 and len(t) > 9:
            continue  # две-три слова — допустимо
        print(f"{f}: висит «{t}» после «…{prev[-40:]}»"); rc = 1
sys.exit(rc)
