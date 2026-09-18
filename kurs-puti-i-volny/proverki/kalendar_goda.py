#!/usr/bin/env python3
"""Сколько занятий реально помещается в учебный год — и куда ложатся 32 темы.

Число занятий нельзя писать руками: оно зависит от каникул, а каникулы школа
меняет по ходу года. Поэтому здесь команда, а не число.

ИСТОЧНИК КАНИКУЛ — не догадка. Даты названы владельцем 11.09.2026 со страницы
школы schc179.mskobr.ru/uchashimsya/raspisanie-kanikuly и лежат одной константой
в spetsmat-bot/config.py (KANIKULY). Здесь они ПРОДУБЛИРОВАНЫ, и это осознанное
нарушение правила одного дома: два репозитория, общей константы нет. Если даты
разъедутся — прав spetsmat-bot, он ближе к источнику.

Запуск:  python3 proverki/kalendar_goda.py
"""

from datetime import date, timedelta

# --- ФАКТЫ КАЛЕНДАРЯ -------------------------------------------------------

KANIKULY = [
    ("2026-10-25", "2026-11-01"),   # осенние
    ("2026-12-31", "2027-01-10"),   # зимние
    ("2027-03-14", "2027-03-21"),   # весенние
]

PERVOE_ZANYATIE = date(2026, 9, 19)   # суббота
KONEC_GODA = date(2027, 5, 31)

# Состав года по plan/src/karkas.md, третья редакция. Дом состава — там,
# здесь копия для счёта; если разъедется, прав karkas.md.
BLOKI = [
    ("1. Разминка",                 1, "первое"),
    ("2. Прямая с весом: разбиения", 5, "первое"),
    ("3. Одна стенка: Каталан",      6, "первое"),
    ("4. Вес на луче, сборка героя",  4, "первое"),
    ("5. Потолок",                    4, "второе"),
    ("6. Спектр",                     6, "второе"),
    ("7. Пределы",                    6, "второе"),
]

DNI = "пн вт ср чт пт сб вс".split()


def v_kanikuly(d: date) -> bool:
    s = d.isoformat()
    return any(a <= s <= b for a, b in KANIKULY)


def chetverti():
    """Границы четвертей выводятся ИЗ каникул, а не задаются отдельно."""
    granicy = [date.fromisoformat(a) for a, _ in KANIKULY]
    konec = [date.fromisoformat(b) for _, b in KANIKULY]
    return [
        ("I",   date(2026, 9, 1),               granicy[0] - timedelta(days=1)),
        ("II",  konec[0] + timedelta(days=1),   granicy[1] - timedelta(days=1)),
        ("III", konec[1] + timedelta(days=1),   granicy[2] - timedelta(days=1)),
        ("IV",  konec[2] + timedelta(days=1),   KONEC_GODA),
    ]


def schitat(wd: int):
    out = []
    for name, a, b in chetverti():
        a = max(a, PERVOE_ZANYATIE)
        n, d = 0, a
        while d <= b:
            if d.weekday() == wd and not v_kanikuly(d):
                n += 1
            d += timedelta(days=1)
        out.append((name, n))
    return out


def main():
    wd = PERVOE_ZANYATIE.weekday()
    print(f"Первое занятие: {PERVOE_ZANYATIE.isoformat()}, это {DNI[wd]}.")
    print("Предположение: занятия еженедельные, по одной паре в этот день недели.\n")

    print("СКОЛЬКО ЗАНЯТИЙ ВМЕЩАЕТ ГОД, по дням недели")
    for w in range(7):
        row = schitat(w)
        met = "  ←" if w == wd else ""
        print(f"  {DNI[w]:3} " + " ".join(f"{n}:{k:2}" for n, k in row)
              + f"   всего {sum(k for _, k in row):2}{met}")

    sloty = schitat(wd)
    d_sloty = dict(sloty)
    print()

    print("СЛОТЫ ПРОТИВ СОСТАВА")
    p1_slot = d_sloty["I"] + d_sloty["II"]
    p2_slot = d_sloty["III"] + d_sloty["IV"]
    p1_tem = sum(n for _, n, p in BLOKI if p == "первое")
    p2_tem = sum(n for _, n, p in BLOKI if p == "второе")
    print(f"  первое полугодие: слотов {p1_slot:2} (I={d_sloty['I']}, II={d_sloty['II']}), "
          f"тем {p1_tem:2}   →  {p1_slot - p1_tem:+d}")
    print(f"  второе полугодие: слотов {p2_slot:2} (III={d_sloty['III']}, IV={d_sloty['IV']}), "
          f"тем {p2_tem:2}   →  {p2_slot - p2_tem:+d}")
    print(f"  ВСЕГО:            слотов {p1_slot + p2_slot:2}, "
          f"тем {p1_tem + p2_tem:2}   →  {p1_slot + p2_slot - p1_tem - p2_tem:+d}")
    print()

    print("КАК БЛОКИ ЛОЖАТСЯ НА ЧЕТВЕРТИ, если идти подряд без пропусков")
    ostatok = {n: k for n, k in sloty}
    poryadok = ["I", "II", "III", "IV"]
    i = 0
    for name, tem, _ in BLOKI:
        kuda = []
        while tem > 0 and i < len(poryadok):
            ch = poryadok[i]
            beru = min(tem, ostatok[ch])
            if beru:
                kuda.append(f"{ch}×{beru}")
                ostatok[ch] -= beru
                tem -= beru
            if ostatok[ch] == 0:
                i += 1
        flag = "  ⚠ РАЗРЕЗАН КАНИКУЛАМИ" if len(kuda) > 1 else ""
        print(f"  {name:32} {' + '.join(kuda)}{flag}")
    print()

    print("ПЕРВАЯ ЧЕТВЕРТЬ ПОИМЁННО")
    d = PERVOE_ZANYATIE
    konec_I = [b for n, a, b in chetverti() if n == "I"][0]
    k = 0
    while d <= konec_I:
        if d.weekday() == wd and not v_kanikuly(d):
            k += 1
            print(f"  {k}. {d.isoformat()}")
        d += timedelta(days=1)


if __name__ == "__main__":
    main()
