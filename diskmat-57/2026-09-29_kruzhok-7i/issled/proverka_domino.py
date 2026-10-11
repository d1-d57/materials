"""Проверки задач про доминошки и Т-тетрамино (лестница «Раскраски», черновик)."""
from tiling import *

print("== Задача 6: доминошки")
print("5x5 целиком:", count_tilings(rect(5, 5), [DOMINO]))
n, ex = count_tilings(rect(5, 5) - {(2, 2)}, [DOMINO], want_example=True)
print("5x5 без центра: способов", n)
print(draw(5, 5, ex, holes={(2, 2)}))
for k in [3, 5, 7, 4, 6]:
    print(f"{k}x{k} без угловой:", count_tilings(rect(k, k) - {(0, 0)}, [DOMINO]))

print("\n== Задача 7: 8x8 без двух угловых")
print("соседние углы (0,0),(0,7):", count_tilings(rect(8, 8) - {(0, 0), (0, 7)}, [DOMINO]))
print("противоположные (0,0),(7,7):", count_tilings(rect(8, 8) - {(0, 0), (7, 7)}, [DOMINO]))

print("\n== Задача 10: какую клетку вырезать из 5x5")
good = []
for r in range(5):
    row = []
    for c in range(5):
        k = count_tilings(rect(5, 5) - {(r, c)}, [DOMINO])
        row.append(k)
        if k:
            good.append((r, c))
    print(" ".join(f"{x:3d}" for x in row))
print("подходят:", len(good), "клеток; все ли цвета угла (r+c чётно):",
      all((r + c) % 2 == 0 for r, c in good), "; все ли клетки цвета угла подходят:",
      len(good) == sum(1 for r in range(5) for c in range(5) if (r + c) % 2 == 0))

print("\n== Задача 11: квадрат n x n на Т-тетрамино")
for k in [4, 6, 8]:
    n, ex = count_tilings(rect(k, k), [T4], want_example=True)
    print(f"{k}x{k}: способов {n}")
    if k == 4 and ex:
        print(draw(4, 4, ex))
# 10x10: только существование не нужно -- проверяем доводом; но проверим 4x8 и 8x4 для конструкции
print("4x8 на Т:", count_tilings(rect(4, 8), [T4]))
