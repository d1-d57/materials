# Проверочные скрипты ресёрча по перебору (перенесено из облака 2026-10-05, Ф2 спасения)

Каждый скрипт пересчитывает утверждения одного документа ресёрча (`../*.md`) перебором. Запускать из этой папки:
`python3 <скрипт>.py` — пути внутри относительные (`verify_bank`, `fig/`).

| скрипт | что проверяет |
|---|---|
| `verify_bank.py` | библиотека: перебор, счётчики; импортируется `v0*.py` |
| `v01_r1.py` … `v06_r6.py`, `v07_grids.py` | банк задач `B_bank.md`: ответы задач, ловушки «наивного» счёта |
| `c1_verify.py`, `c2_verify.py` | лестницы `C1_ladder.md`, `C2_ladder.md` |
| `d1_verify.py`, `d2_verify.py` | красные команды `D1_redteam.md`, `D2_redteam.md` |
| `ev/chk.py` | `E_verify.md` |
| `../final_verify.py` | итоговая `LESTNICA-PEREBOR.md` (60 проверок) |
| `g_haos.py`, `g_rules.py`, `g_greedy.py` (+ `.out` — их вывод на 05.10) | `G_haos.md`, `BRAINSTORM-perebor.md`: хаос на разбиениях 6, каталог правил, флаги |
| `H/h_verify.py` | `H_oshibka.md` — ложные правила R1–R14 |
| `chk.py`, `kids.py`, `tris.py`, `fig.py` → `fig/variants.png` | отвергнутые K5/K6 (отрезки, треугольники) и детские варианты |

`../_istoriya/LESTNICA-PEREBOR.v1.md` — первая версия лестницы до красной команды.
