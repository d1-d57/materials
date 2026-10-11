# -*- coding: utf-8 -*-
"""СОХРАНЕНЫ ЛИ НАГОВОРЫ ВЛАДЕЛЬЦА. Запуск в облачной сессии (там лежат вложения):
    python3 vlozheniya.py <папка вложений сессии> <папка арки на диске или её копия>
Краснеет (код 1), если текст хоть одного вложения (*.txt) не найден дословно ни в одном файле арки.
Ищется кусок из середины первого абзаца (80 символов) — по нему видно, лежит ли наговор на диске.
Зачем: 04.10 выяснилось, что 9 из 12 наговоров сессии 28–29.09 жили только в облачной папке (UROKI-FABRIKE 04.10).
Гонять перед каждым хэндоффом и после каждого длинного наговора."""
import sys, glob, os
def kusok(t):
    t = ' '.join(t.split())
    return t[40:120] if len(t) > 140 else t[:80]
def main(vl, arka):
    teksty = []
    for f in glob.glob(os.path.join(arka, '**', '*'), recursive=True):
        if os.path.isfile(f) and f.endswith(('.md', '.txt')):
            try: teksty.append(' '.join(open(f, encoding='utf-8', errors='ignore').read().split()))
            except Exception: pass
    red = 0
    for f in sorted(glob.glob(os.path.join(vl, '*.txt'))):
        k = kusok(open(f, encoding='utf-8', errors='ignore').read())
        ok = any(k in t for t in teksty)
        print(('✓ ' if ok else '❗ НЕТ НА ДИСКЕ ') + os.path.basename(f) + ' — «' + k[:50] + '…»')
        red += not ok
    print('вложения: ' + ('все на диске' if not red else f'не сохранено {red}')); sys.exit(1 if red else 0)
if __name__ == '__main__':
    main(*sys.argv[1:3])
