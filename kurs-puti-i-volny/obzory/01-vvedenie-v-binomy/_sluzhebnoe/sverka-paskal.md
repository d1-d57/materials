# сверка: паскаль, «traité du triangle arithmétique»

источник: перевод Richard J. Pulskamp, https://gtfp.cs.rhul.ac.uk/pulskamp/Pascal/Sources/arith_triangle.pdf (страницы — по этому pdf, номера сообщены инструментом извлечения, могут быть ±1).

**как читалось.** прямое скачивание pdf (curl) заблокировано прокси (403), кембриджский pdf — тоже. текст получен через WebFetch: он отдаёт дословные фрагменты длиной < 125 символов, последовательными кусками. все цитаты ниже — такие дословные фрагменты, а не пересказ. отдельная перекрёстная проверка: числовой пример из доказательства 12-го следствия я пересчитал по биномиальным коэффициентам — сходится, это подтверждает, что ориентация и «верхняя/нижняя» прочитаны правильно. французский оригинал (gallica / wikisource) не открывал.

---

## 1. даты: 1654 написан и отпечатан, 1665 вышел посмертно

**вердикт: подтверждено.**

стр. 1, вводная заметка Пулскампа:
- "The treatises related to arithmetic triangle appear to be dated near the end of 1654"
- "These were discovered after his death and published at Paris by Guillaume Desprez" / "in 1665 under the title: Traite du Triangle arithmétique"
- "Date: Printed 1654, published 1665."

нюанс: у Пулскампа датировка 1654 дана осторожно («appear to be dated»). в самом pdf год смерти Паскаля (1662) не указан, но «discovered after his death» для «посмертно» достаточно.

## 2. «основания» — диагонали; основание m — наша строка m−1

**вердикт: подтверждено.**

стр. 2–3, определения:
- "I join thus the two points of the second division by another line, which forms a second" / "triangle of which is the base."
- "And those that one same base traverse diagonally are so-called cells of one same base," / "as those which follow, D, B, θ, λ, and these A, ψ, π."
- "each base contains one cell more than the preceding," / "and each as many as its exponent of units; thus the second φσ has two cells, the third" / "Aψπ has three of them, etc."

первое основание — одна клетка: стр. 5, доказательство 8-го следствия: "Because the first base is unity." второе основание φσ — две клетки, обе равны 1: стр. 6, "φ is to σ as 1 to 1". значит, основание m состоит из m клеток C(m−1, k), то есть это наша строка m−1. индексация в статье верная.

## 3. двенадцатое следствие: формулировка, «включительно», верх/низ

**вердикт: подтверждено** (и «включительно», и то, какая клетка верхняя, а какая нижняя).

стр. 6, формулировка у Пулскампа целиком:
> "In every arithmetic Triangle, two contiguous cells being in one same base, the superior is to the inferior as the number of cells from the superior to the top of the base to the number of cells from the inferior to the bottom inclusively."

- **верх/низ.** в числителе стоит верхняя клетка (superior) и число клеток от неё до верха основания, в знаменателе — нижняя (inferior) и число клеток от неё до низа. в статье так же.
- **«включительно»** («inclusively», во французском «inclusivement») относится к обоим счётам: сама клетка тоже считается. это видно по числам Паскаля. стр. 7: "D is to B as 1 to 3, by hypothesis" (4-е основание 1,3,3,1: D — самая верхняя клетка, счёт до верха = 1, считая саму D) и "E is to C as 2 to 3" (5-е основание 1,4,6,4,1: 4/6 = 2/3).
- **проверка по формуле.** верхняя клетка стоит в параллельном ряду p основания m, тогда до верха p клеток, а от нижней клетки до низа m−p клеток. отношение C(m−1, p−1)/C(m−1, p) = p/(m−p) — это и есть утверждение Паскаля.

## 4. доказательство индукцией: база — второе основание, шаг — к следующему основанию

**вердикт: подтверждено.**

стр. 6:
- "Although this proposition has an infinite number of cases, I will give a quite short demonstration," / " in supposing 2 lemmas."
- "The first, that it is evident by itself, that this proportion is encountered in the second base; " / "for it is quite clear that φ is to σ as 1 to 1."
- "The second, that if this proportion is found in any base, it will be found necessarily in the base following."

стр. 7: шаг показан на переходе от 4-го основания к 5-му — "I say that the same proportion will be found in the following base, Hµ, and that, for example, E is to C as 2 to 3." Дальше идёт вывод через "disturbed proportion". База индукции — второе основание, то есть наша строка «1 1»; в статье верно.

## 5. задача сразу после следствий: 3·4·5·6 / 1·2·3·4 = 15, это C(6,4)

**вердикт: подтверждено по существу; «сразу» — с маленькой оговоркой.**

- **порядок.** у Паскаля 18 нумерованных следствий и "LAST CONSEQUENCE" (19-е, стр. 9). за ним идёт короткая "NOTE", и только потом заголовок "PROBLEM". текст заметки, стр. 9: "We are able to draw from there many other proportions that I suppress, because each" … "I end therefore with the following problem, which makes the fulfillment of the treatise." сама заметка — мостик к задаче, так что «сразу после следствий» допустимо.
- **условие**, стр. 9: "Being given the exponents of the perpendicular and parallel ranks of a cell, to find the number of the cell," / "without using the arithmetic Triangle."
- **пример**, стр. 9:
  - "Let, for example, it be proposed to find the number of the cell ξ of the fifth perpendicular" / "rank and the third parallel rank."
  - "Having taken all the numbers which precede the exponent of the perpendicular 5, namely 1, 2, 3, 4,"
  - "let there be taken as many natural numbers, starting with the exponent of the parallel 3, namely 3, 4, 5, 6."
  - "Let the first ones be multiplied by one another, and let the product be 24."
  - "Let the others be multiplied by one another, and let the product be 360, which, divided by the other" / "product 24, gives for quotient 15. This quotient is the number sought."
  - обоснование: "Therefore ξ is to V as 3 by 4 by 5 by 6, to 4 by 3 by 2 by 1." / "But V is unity; …"
- **почему это C(6,4).** клетка в перпендикулярном ряду q = 5 и параллельном ряду p = 3 лежит в основании p+q−1 = 7, то есть в нашей строке 6. её значение C(p+q−2, q−1) = C(6,4) = C(6,2) = 15. произведение Паскаля 3·4·5·6 / 4! дословно совпадает с C(6,4) = 6·5·4·3 / 4!: четыре множителя, потому что q−1 = 4. так что запись C(6,4) в статье естественная. C(6,2) — то же число, но эту запись дал бы счёт с другого края основания.
- **мелочь.** пример у Паскаля рассчитан на треугольник с образующей 1. после решения сказано: "If the generator is not unity, it would be necessary to multiply the quotient by the generator."

## 6. (новое) следствия 7 и 8: сумма основания удваивается, сумма основания m равна 2^(m−1)

**вердикт: подтверждено.**

стр. 5:
- 7-е следствие: "In every arithmetic triangle, the sum of the cells of each base is double the cells of the base preceding."
- 8-е следствие: "In every arithmetic triangle, the sum of the cells of each base is a number of the double" / "progression which begins with the unit of which the exponent is the same as that of the base."
- доказательство 8-го: "Because the first base is unity." / "The second is double of the first, therefore it is 2." / "The third is double of the second, therefore it is 4." / "And thus to infinity."

8-е следствие говорит, что сумма основания m — это m-й член ряда 1, 2, 4, …, то есть 2^(m−1). формулы 2^(m−1) у Паскаля нет, это наша запись его слов. 7-е следствие верно при любой образующей. 8-е опирается на то, что образующая равна 1 (стр. 3: "where I consider the triangles of which the generator is unity").

предлагаемая формулировка для статьи: «седьмое следствие Паскаля: сумма клеток каждого основания вдвое больше суммы предыдущего; восьмое: сумма основания — член двойной прогрессии 1, 2, 4, … с тем же номером, что и основание, то есть сумма основания m равна 2^(m−1).»

---

выдано 6 позиций из 6 найденных
