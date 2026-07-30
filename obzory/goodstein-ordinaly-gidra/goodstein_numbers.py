"""
Числа для текста про последовательности Гудстейна.

Конвенция (Kirby-Paris 1982, с.285; Rathjen Def.2.4; OEIS A056193):
    сначала наследственную запись по основанию b перечитываем по основанию b+1,
    ПОТОМ вычитаем единицу.

Считаем:
  1) первые члены последовательности от 4 (и от 3) прямым перебором;
  2) наследственные записи в виде строки;
  3) сопоставленный ординал (замена основания на omega) в виде строки;
  4) точную длину последовательности от 4 через фазовый анализ,
     и сверку с опубликованным 3*2^402653211 - 2.
"""

from functools import lru_cache

# ---------- 1. Наследственная запись ----------

def hered(n, b):
    """Наследственная запись n по основанию b как дерево:
    список пар (exponent_tree, coefficient), показатели по убыванию."""
    out = []
    e = 0
    m = n
    digits = []
    while m:
        digits.append(m % b)
        m //= b
    for i in range(len(digits) - 1, -1, -1):
        if digits[i]:
            out.append((hered(i, b), digits[i]))
    return out


def eval_tree(tree, b):
    """Значение дерева при основании b."""
    return sum(b ** eval_tree(e, b) * c for e, c in tree)


def goodstein_step(n, b):
    """Один шаг: перечитать по основанию b+1, потом минус 1."""
    if n == 0:
        return 0
    return eval_tree(hered(n, b), b + 1) - 1


def sequence(start, k):
    """Первые k членов: a_1 = start при основании 2, a_2 при основании 3, ..."""
    res = []
    n, b = start, 2
    for _ in range(k):
        res.append((b, n))
        if n == 0:
            break
        n = goodstein_step(n, b)
        b += 1
    return res


# ---------- 2. Печать записей ----------

def show_hered(n, b):
    if n == 0:
        return "0"
    parts = []
    for e, c in hered(n, b):
        ev = eval_tree(e, b)
        if ev == 0:
            s = str(c)
        else:
            es = "1" if ev == 1 else show_hered(ev, b)
            s = f"{b}^({es})" if ev > 1 else f"{b}"
            if c > 1:
                s += f"*{c}"
        parts.append(s)
    return " + ".join(parts)


def show_ordinal(n, b):
    if n == 0:
        return "0"
    parts = []
    for e, c in hered(n, b):
        ev = eval_tree(e, b)
        if ev == 0:
            s = str(c)
        elif ev == 1:
            s = "w" + (f"*{c}" if c > 1 else "")
        else:
            s = f"w^({show_ordinal(ev, b)})" + (f"*{c}" if c > 1 else "")
        parts.append(s)
    return " + ".join(parts)


# ---------- 3. Точная длина последовательности от 4 ----------
#
# После первого шага (4 при основании 2  ->  26 при основании 3) запись
# становится обычным полиномом степени 2: 26 = 2*3^2 + 2*3 + 2, цифры (2,2,2).
# Дальше показатели уже меньше основания, наследственность не нужна,
# и состояние = (основание b; цифры a2,a1,a0), a_i < b.
#
# Один шаг при a0>0:      (b; a2,a1,a0) -> (b+1; a2,a1,a0-1)
# при a0=0, a1>0:         (b; a2,a1,0)  -> (b+1; a2,a1-1,b)     <- заём даёт b, не b-1
# при a0=a1=0, a2>0:      (b; a2,0,0)   -> (b+1; a2-1,b,b)
#
# Отсюда закрытые формулы (вывод в комментариях к тесту ниже):
#   очистка a1 = m при основании b:  (b+1)*(2^m - 1) шагов, конечное основание 2^m*(b+1) - 1
#   один декремент a2 при основании b: (b+1)*(2^(b+1) - 1) шагов,
#                                      конечное основание (b+1)*2^(b+1) - 1

def clear_a1(b, m):
    """Шагов на очистку среднего разряда m при основании b; и новое основание."""
    B = b + 1
    return B * (2 ** m - 1), 2 ** m * B - 1


def dec_a2(b):
    """Шагов на один декремент старшего разряда при основании b; и новое основание.
    (Показатель может быть астрономическим — возвращаем symbolic-safe пару.)"""
    B = b + 1
    return B, B  # steps = B*(2^B - 1), new base = B*2^B - 1  (в exp-форме)


def brute_phase_check():
    """Проверяем закрытые формулы прямым перебором на малых случаях."""
    ok = True
    for b in range(3, 9):
        for m in range(1, b):
            # прямой перебор: состояние (b; 0, m, 0) -> (?, 0,0,0)
            n = m * b
            bb, steps = b, 0
            while n:
                n = goodstein_step(n, bb)
                bb += 1
                steps += 1
                if steps > 10 ** 6:
                    raise RuntimeError("too long")
            pred_steps, pred_base = clear_a1(b, m)
            if (steps, bb) != (pred_steps, pred_base):
                ok = False
                print(f"  MISMATCH clear_a1 b={b} m={m}: "
                      f"brute=({steps},{bb}) formula=({pred_steps},{pred_base})")
    return ok


def brute_dec_a2_check():
    ok = True
    for b in range(3, 7):
        n = b * b  # (b; 1,0,0)
        bb, steps = b, 0
        while n:
            n = goodstein_step(n, bb)
            bb += 1
            steps += 1
            if steps > 5 * 10 ** 6:
                raise RuntimeError("too long")
        B = b + 1
        pred_steps = B * (2 ** B - 1)
        pred_base = B * 2 ** B - 1
        if (steps, bb) != (pred_steps, pred_base):
            ok = False
            print(f"  MISMATCH dec_a2 b={b}: brute=({steps},{bb}) "
                  f"formula=({pred_steps},{pred_base})")
    return ok


def length_from_4():
    """Точная длина: возвращает (описание, показатель двойки, множитель)."""
    steps = 1                      # 4 при основании 2 -> 26 при основании 3
    b = 3                          # цифры (2,2,2)
    steps += 2; b += 2             # обнулили a0=2 -> основание 5, цифры (2,2,0)
    s, b = clear_a1(b, 2)          # обнулили a1=2
    steps += s                     # -> основание 23, цифры (2,0,0)
    assert b == 23, b
    # первый декремент a2: 2 -> 1
    B1 = b + 1                     # 24
    steps += B1 * (2 ** B1 - 1)
    b = B1 * 2 ** B1 - 1           # 24*2^24 - 1 = 3*2^27 - 1
    # второй декремент a2: 1 -> 0. Дальше числа астрономические, работаем в exp-форме.
    B2 = b + 1                     # 3*2^27
    assert B2 == 3 * 2 ** 27, B2
    # steps += B2*(2^B2 - 1) = B2*2^B2 - B2
    # финальное основание = B2*2^B2 - 1 = 3*2^(27 + 3*2^27) - 1
    exp = 27 + 3 * 2 ** 27
    final_base = ("3*2^%d - 1" % exp)
    # общее число шагов = final_base - 2 (основание растёт на 1 за шаг, старт 2)
    total = ("3*2^%d - 3" % exp)
    # проверим согласованность: steps до второго декремента + B2*2^B2 - B2
    partial = steps
    # symbolic: total_steps = partial + B2*2^B2 - B2
    #        и одновременно  = 3*2^exp - 3
    lhs_const = partial - B2       # то, что не содержит 2^B2
    # 3*2^exp = B2*2^B2, т.к. B2 = 3*2^27 и exp = 27 + 3*2^27
    consistent = (lhs_const == -3)
    return {
        "steps_before_last_decrement": partial,
        "B2": B2,
        "exp": exp,
        "final_base": final_base,
        "total_steps": total,
        "index_of_zero_1based": "3*2^%d - 2" % exp,
        "consistency_check": consistent,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("1. ПЕРВЫЕ ЧЛЕНЫ ОТ 4 (основание, значение, наследственная запись, ординал)")
    print("=" * 70)
    for b, n in sequence(4, 12):
        print(f"  b={b:<3} a={n:<6} {show_hered(n, b):<34} {show_ordinal(n, b)}")

    print()
    print("=" * 70)
    print("2. ПОСЛЕДОВАТЕЛЬНОСТЬ ОТ 3 (до нуля)")
    print("=" * 70)
    for b, n in sequence(3, 10):
        print(f"  b={b:<3} a={n:<4} {show_hered(n, b):<14} {show_ordinal(n, b)}")

    print()
    print("=" * 70)
    print("3. СВЕРКА С OEIS A056193 (первые 47 членов от 4)")
    print("=" * 70)
    oeis = [4, 26, 41, 60, 83, 109, 139, 173, 211, 253, 299, 348, 401, 458, 519,
            584, 653, 726, 803, 884, 969, 1058, 1151, 1222, 1295, 1370, 1447,
            1526, 1607, 1690, 1775, 1862, 1951, 2042, 2135, 2230, 2327, 2426,
            2527, 2630, 2735, 2842, 2951, 3062, 3175, 3290, 3407]
    mine = [n for _, n in sequence(4, 47)]
    print(f"  совпадает: {mine == oeis}")
    if mine != oeis:
        print("  мои:  ", mine[:12])
        print("  OEIS: ", oeis[:12])

    print()
    print("=" * 70)
    print("4. ПРОВЕРКА ЗАКРЫТЫХ ФОРМУЛ ФАЗ ПРЯМЫМ ПЕРЕБОРОМ")
    print("=" * 70)
    print(f"  clear_a1 совпадает с перебором: {brute_phase_check()}")
    print(f"  dec_a2  совпадает с перебором: {brute_dec_a2_check()}")

    print()
    print("=" * 70)
    print("5. ТОЧНАЯ ДЛИНА ПОСЛЕДОВАТЕЛЬНОСТИ ОТ 4")
    print("=" * 70)
    r = length_from_4()
    for k, v in r.items():
        print(f"  {k}: {v}")
    print()
    print(f"  опубликовано (Caicedo 2007, Wikipedia): 3*2^402653211 - 2")
    print(f"  мой показатель: {r['exp']}  ==  402653211 ? {r['exp'] == 402653211}")
    print(f"  Kirby-Paris 1982 печатают число шагов:  3*2^402653211 - 3")
    print(f"  мой total_steps: {r['total_steps']}")

    print()
    print("=" * 70)
    print("6. ПОРЯДОК ВЕЛИЧИНЫ")
    print("=" * 70)
    from decimal import Decimal, getcontext
    getcontext().prec = 30
    log10 = Decimal(r["exp"]) * Decimal(2).log10() + Decimal(3).log10()
    print(f"  log10(3*2^{r['exp']}) = {log10}")
    print(f"  то есть примерно 10^{int(log10)}  (мантисса 10^{log10 - int(log10)})")
