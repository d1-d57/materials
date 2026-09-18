---
opisanie: единый дом списка пунктов курса «Пути и волны» — атом живёт здесь один раз, планы всех уровней порождаются из этого файла tools/plany.py
sloj: 3
status: zhivoy
---

# Пункты курса «Пути и волны» — единый дом

> **Что такое пункт.** Одно занятие года — один пункт, `p-NN`. У него есть координата на карте курса
> (`doska`/`ves` — где на лестнице «прямая → луч → отрезок → предел» он стоит и включён ли вес $q$),
> место в календаре (`chetvert`/`polovina`/`chast`), связи с соседями (`opiraetsya` — на что опирается,
> `obobshchaetsya-v` — во что перерастает) и адрес материала (`adres`, `iz-karkasa`). Четыре поля
> отмечены ⭐ в комментариях ниже — это красивое содержание занятия (`imya`, `vopros`, `teorema`,
> `zadacha`); их пишет отдельная позиция (наполнитель), не эта.
>
> **Почему один раз.** Раньше один и тот же список тем жил в нескольких файлах руками и разошёлся трижды
> (`SBORKA/KARTA-rashozhdeniy.md`, строки Р5, Р10, Р13). Теперь пункт существует ровно тут; год, полугодие,
> часть «до анализа», четверть и лекция — это VIEWS, которые печатает `tools/plany.py`, и трогать их руками
> нельзя: гейт `--proverit` ловит расхождение с тем, что генератор написал бы сейчас.
>
> **Как читать поле.** Каждое поле — строка `ключ: значение`; ключ фиксированный (латиница), см. список
> в `tools/plany.py`. Пусто — значит ещё не заполнено (не то же самое, что «не нужно»). Значение может
> занимать несколько строк подряд — тогда следующая строка, не начинающаяся с известного ключа, читается
> как продолжение предыдущего поля (нужно для будущей `raskadrovka`, поминутной раскадровки; в этом файле
> она везде пуста, а свою внутреннюю форму — `beat: <минута> — <текст>`, по одной на строку — вводит
> следующая позиция, когда придёт время её заполнять).
>
> **Координата.** `doska` — сколько стенок видел путь: `pryamaya` (0), `luch` (1), `otrezok` (2), `predel`
> (переход к непрерывному пределу, второе полугодие). `ves` — включён ли параметр $q$: `q-vykl` / `q-vkl`.
> Правило владельца (19.09): доска только продвигается, а включённый вес назад не выключается — во всём
> курсе ровно один пункт с `ves: q-vykl` (первая лекция), дальше `q-vkl` до конца года.
>
> **Отбор.** У пункта без `obobshchaetsya-v` в курсе делать нечего (гейт `plany.py --proverit` красный на
> этом). Последний пункт года указывает на служебный якорь `finish`, а не на другой пункт — это законно.

## Для наполнителя (S4б)

Следующая позиция заполняет содержание четверти I (6 пунктов `p-01`…`p-06`) — и только её: четверти
II–IV несут пока лишь координату и ссылку на каркас, наполнять их сейчас, по решению владельца, было бы
преждевременно (форма ещё не проверена на практике).

**Что писать.** Для каждого из `p-01`…`p-06` — все четыре поля со звёздочкой:
- `imya` — название, под которым хочется открыть это занятие как главу книги;
- `vopros` — красивый вопрос, с которого занятие начинается;
- `teorema` — красивая теорема, вот-в-чём-соль;
- `zadacha` — красивая задача.

Материал для перевода уже лежит в поле `iz-karkasa` каждого пункта (номер темы и дословная цитата
«Объект»/«Ого» из `karkas.md`) — это не инструкция, что писать, а сырьё, из которого можно писать.
`raskadrovka` пункта `p-01` тоже за наполнителем: минутная раскадровка первой лекции — единственная,
которую разворачивает `tools/plany.py` в `plan/src/lekciya-1.md`; форма поля (`beat: <минута> — <текст>`,
по одной на строку) — задача этой позиции, а не следующей.

**Каким гейтом проверить, что готово.** `python3 kurs-puti-i-volny/tools/plany.py --proverit` (по
умолчанию `--napolnennye 1`) обязан вернуть `0` — это и значит, что все ⭐-поля четверти I заполнены и
форма не нарушена. Сейчас, с пустыми ⭐-полями, тот же гейт красный ровно на этих шести пунктах — это
проверено этим заходом (см. `## ОТЧЁТ` файла-захода, критерий 1) и есть designed поведение, не брак.

## Уровни

> Один блок на уровень обобщения. `obobshchenie` — одна фраза, чем этот уровень обобщает более мелкий
> (мандат требует, чтобы каждый план открывался именно с неё). `svod` — короткий абзац, который связывает
> пункты уровня в одну историю. Оба поля пусты в этой сдаче — их пишет наполнитель, по мере того как
> заполняются пункты соответствующего уровня.

### Уровень: god
obobshchenie:
svod:

### Уровень: polugodie-1
obobshchenie:
svod:

### Уровень: polugodie-2
obobshchenie:
svod:

### Уровень: chast-do-analiza
obobshchenie:
svod:

### Уровень: chetvert-1
obobshchenie:
svod:

### Уровень: chetvert-2
obobshchenie:
svod:

### Уровень: chetvert-3
obobshchenie:
svod:

### Уровень: chetvert-4
obobshchenie:
svod:

## Пункты

<!--id: p-01-->
### p-01
id: p-01
imya:
vopros:
teorema:
zadacha:
doska: pryamaya
ves: q-vykl
chetvert: 1
polovina: 1
chast: do-analiza
opiraetsya: 
obobshchaetsya-v: p-02
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 1 «Пути и биномиальные коэффициенты» (Блок 1. Разминка)
iz-karkasa: тема 1 «Пути и биномиальные коэффициенты». Объект: $\binom nk$ как число путей. Паскаль, Вандермонд, сумма квадратов — всё двойным счётом. Возврат в ноль, вероятность $\sim1/\sqrt{\pi n}$, среднее через производную бинома.
raskadrovka:

<!--id: p-02-->
### p-02
id: p-02
imya:
vopros:
teorema:
zadacha:
doska: pryamaya
ves: q-vkl
chetvert: 1
polovina: 1
chast: do-analiza
opiraetsya: p-01
obobshchaetsya-v: p-03
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 2 «Диаграммы Юнга» (Блок 2. Прямая с весом: разбиения)
iz-karkasa: тема 2 «Диаграммы Юнга». Объект: разбиение числа. Сопряжение; разбиений на различные части ровно столько же, сколько на нечётные (биекция «удваивай и дели»). Площадь под путём — это диаграмма. Ого: два условия, не имеющих ничего общего, дают одинаковый ответ, и биекция это объясняет за пять минут.
raskadrovka:

<!--id: p-03-->
### p-03
id: p-03
imya:
vopros:
teorema:
zadacha:
doska: pryamaya
ves: q-vkl
chetvert: 1
polovina: 1
chast: do-analiza
opiraetsya: p-02
obobshchaetsya-v: p-04
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 3 «Гауссовы биномиальные коэффициенты» (Блок 2. Прямая с весом: разбиения)
iz-karkasa: тема 3 «Гауссовы биномиальные коэффициенты». Объект: $\binom nk_q$. Разбиения в коробке; два правила Паскаля, оба разрезанием диаграммы; палиндромность через дополнение; унимодальность названа и отдана чёрным ящиком. Ого: при $q=2$ выходит 35, и ровно столько двумерных подпространств в $\mathbb F_2^4$. Один многочлен считает разбиения, пути и подпространства, а при $q=1$ — просто подмножества.
raskadrovka:

<!--id: p-04-->
### p-04
id: p-04
imya:
vopros:
teorema:
zadacha:
doska: pryamaya
ves: q-vkl
chetvert: 1
polovina: 1
chast: do-analiza
opiraetsya: p-03
obobshchaetsya-v: p-05
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 4 «Производящая функция разбиений» (Блок 2. Прямая с весом: разбиения)
iz-karkasa: тема 4 «Производящая функция разбиений». Объект: $\prod 1/(1-q^i)$. Почему произведение, что такое формальный ряд, разбиения с ограничениями на части. Ого: впервые за курс объект, у которого нет ни замкнутой формулы, ни биекции. Приём кончился — нужен язык.
raskadrovka:

<!--id: p-05-->
### p-05
id: p-05
imya:
vopros:
teorema:
zadacha:
doska: luch
ves: q-vkl
chetvert: 1
polovina: 1
chast: do-analiza
opiraetsya: p-04
obobshchaetsya-v: p-06
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 7 «Триангуляции многоугольника» (Блок 3. Одна стенка: числа Каталана)
iz-karkasa: тема 7 «Триангуляции многоугольника». Объект: разрезания выпуклого многоугольника. Рекуррента-свёртка прямо из картинки.
raskadrovka:

<!--id: p-06-->
### p-06
id: p-06
imya:
vopros:
teorema:
zadacha:
doska: luch
ves: q-vkl
chetvert: 1
polovina: 1
chast: do-analiza
opiraetsya: p-05
obobshchaetsya-v: p-07
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 8 «Плоские деревья» (Блок 3. Одна стенка: числа Каталана)
iz-karkasa: тема 8 «Плоские деревья». Объект: дерево. Бинарные и произвольные; явная биекция с триангуляциями. Ого: два несвязанных объекта дают одно число, и это доказывается без единого вычисления.
raskadrovka:

<!--id: p-07-->
### p-07
id: p-07
imya:
vopros:
teorema:
zadacha:
doska: luch
ves: q-vkl
chetvert: 2
polovina: 1
chast: do-analiza
opiraetsya: p-06
obobshchaetsya-v: p-08
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 9 «Стек-сортируемые перестановки» (Блок 3. Одна стенка: числа Каталана)
iz-karkasa: тема 9 «Стек-сортируемые перестановки». Объект: запретный образец 231. Стек как алгоритм, порождающий биекцию. Ого: задача из программирования оказывается той же задачей про многоугольники.
raskadrovka:

<!--id: p-08-->
### p-08
id: p-08
imya:
vopros:
teorema:
zadacha:
doska: luch
ves: q-vkl
chetvert: 2
polovina: 1
chast: do-analiza
opiraetsya: p-07
obobshchaetsya-v: p-09
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 10 «Принцип отражения» (Блок 3. Одна стенка: числа Каталана)
iz-karkasa: тема 10 «Принцип отражения». Объект: отражение Андре. Баллотные числа; замкнутая формула наконец. Отражение одно, потому ответ конечен — это запомнить до лекции 17.
raskadrovka:

<!--id: p-09-->
### p-09
id: p-09
imya:
vopros:
teorema:
zadacha:
doska: luch
ves: q-vkl
chetvert: 2
polovina: 1
chast: do-analiza
opiraetsya: p-08
obobshchaetsya-v: p-10
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 11 «Циклическая лемма» (Блок 3. Одна стенка: числа Каталана)
iz-karkasa: тема 11 «Циклическая лемма». Объект: действие группы циклических сдвигов. Среди $2n+1$ сдвигов хорош ровно один; $k$-арные деревья бесплатно. Ого: формула Каталана в одну строку, без всякого отражения.
raskadrovka:

<!--id: p-10-->
### p-10
id: p-10
imya:
vopros:
teorema:
zadacha:
doska: luch
ves: q-vkl
chetvert: 2
polovina: 1
chast: do-analiza
opiraetsya: p-09
obobshchaetsya-v: p-11
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 12 «Первое возвращение» (Блок 3. Одна стенка: числа Каталана)
iz-karkasa: тема 12 «Первое возвращение». Объект: момент первого возврата домой. Разложение по первому возвращению. Ого: быть дома на шаге $2n$ и ни разу дома не побывать — одна и та же вероятность. Сначала телескоп, потом биекция «разрезать и переклеить», которая объясняет совпадение.
raskadrovka:

<!--id: p-11-->
### p-11
id: p-11
imya:
vopros:
teorema:
zadacha:
doska: luch
ves: q-vkl
chetvert: 2
polovina: 1
chast: do-analiza
opiraetsya: p-10
obobshchaetsya-v: p-12
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 13 «$q$-числа Каталана» (Блок 4. Вес на луче и сборка героя)
iz-karkasa: тема 13 «$q$-числа Каталана». Объект: статистика на пути. Площадь по Карлицу — Риордану против major index. Ого: $q$-Каталанов два, и они разные; при $q=1$ оба дают 42, а замкнутая формула есть только у одного.
raskadrovka:

<!--id: p-12-->
### p-12
id: p-12
imya:
vopros:
teorema:
zadacha:
doska: luch
ves: q-vkl
chetvert: 2
polovina: 1
chast: do-analiza
opiraetsya: p-11
obobshchaetsya-v: p-13
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 14 «Инверсии и major index» (Блок 4. Вес на луче и сборка героя)
iz-karkasa: тема 14 «Инверсии и major index». Объект: статистика на перестановке. Обе дают $[n]_q!$. Ого: две статистики, устроенные совершенно по-разному, распределены одинаково; биекция Фуа это объясняет.
raskadrovka:

<!--id: p-13-->
### p-13
id: p-13
imya:
vopros:
teorema:
zadacha:
doska: luch
ves: q-vkl
chetvert: 2
polovina: 1
chast: do-analiza
opiraetsya: p-12
obobshchaetsya-v: p-14
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 15 «Числа Нараяны» (Блок 4. Вес на луче и сборка героя)
iz-karkasa: тема 15 «Числа Нараяны». Объект: треугольник Нараяны. Пути по числу пиков; симметрия треугольника; связь с гауссовыми биномами.
raskadrovka:

<!--id: p-14-->
### p-14
id: p-14
imya:
vopros:
teorema:
zadacha:
doska: luch
ves: q-vkl
chetvert: 2
polovina: 1
chast: do-analiza
opiraetsya: p-13
obobshchaetsya-v: p-15
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 16 «Функция с концами» (Блок 4. Вес на луче и сборка героя)
iz-karkasa: тема 16 «Функция с концами». Объект: $F(x\to y;\,z,q)$ — откуда, куда, за сколько шагов, с какой площадью. Концы обязательны: без них прямая из луча не достаётся. Ого и точка каникул: стенка перестаёт чувствоваться, если до неё не дойти. Отодвигаем старт — зеркальный член в формуле отражения обнуляется, и луч превращается в прямую; вместе с ним Каталан превращается в биномы, а $q$-Каталан в гауссовы биномы и разбиения. Всё полугодие оказывается одной функцией при разных положениях старта и включённом или выключенном весе.
raskadrovka:

<!--id: p-15-->
### p-15
id: p-15
imya:
vopros:
teorema:
zadacha:
doska: otrezok
ves: q-vkl
chetvert: 3
polovina: 2
chast: do-analiza
opiraetsya: p-14
obobshchaetsya-v: p-16
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 17 «Метод изображений» (Блок 5. Потолок)
iz-karkasa: тема 17 «Метод изображений». Объект: группа, порождённая двумя отражениями. Отражений бесконечно много, ответ — знакопеременная сумма. Ого, и это провал: формула точна при любых числах и бесполезна. Коридор из 5 клеток, длина 80: ответ $8{,}1\cdot10^{18}$, сумма модулей слагаемых $4{,}0\cdot10^{23}$.
raskadrovka:

<!--id: p-16-->
### p-16
id: p-16
imya:
vopros:
teorema:
zadacha:
doska: otrezok
ves: q-vkl
chetvert: 3
polovina: 2
chast: do-analiza
opiraetsya: p-15
obobshchaetsya-v: p-17
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 18 «Пути ограниченной высоты» (Блок 5. Потолок)
iz-karkasa: тема 18 «Пути ограниченной высоты». Объект: лестница последовательностей. Высота $\le2$ — степени двойки; $\le3$ — Фибоначчи через одно; $\le4$ — $\frac{3^{n-1}+1}{2}$; выше — Каталан. Ого: строка высоты $m$ совпадает с Каталаном ровно на первых $m$ членах и расходится ровно на единицу. Рост идёт $1,\sqrt2,\varphi,\sqrt3,\dots\to2$, и золотое сечение сидит между корнями из двух и трёх.
raskadrovka:

<!--id: p-17-->
### p-17
id: p-17
imya:
vopros:
teorema:
zadacha:
doska: otrezok
ves: q-vkl
chetvert: 3
polovina: 2
chast: do-analiza
opiraetsya: p-16
obobshchaetsya-v: p-18
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 19 «Цепные дроби» (Блок 5. Потолок)
iz-karkasa: тема 19 «Цепные дроби». Объект: цепная дробь как самостоятельная вещь. Подходящие дроби, их числители и знаменатели; лестница лекции 18 оказывается подходящими дробями одной дроби.
raskadrovka:

<!--id: p-18-->
### p-18
id: p-18
imya:
vopros:
teorema:
zadacha:
doska: otrezok
ves: q-vkl
chetvert: 3
polovina: 2
chast: do-analiza
opiraetsya: p-17
obobshchaetsya-v: p-19
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 20 «Многочлены Чебышёва» (Блок 5. Потолок)
iz-karkasa: тема 20 «Многочлены Чебышёва». Объект: $U_k$. Вход снаружи сюжета: при каких $n$ число $2\cos\frac{2\pi}{n}$ целое? Только при $n=1,2,3,4,6$ — кристаллографическое ограничение. Ого: те же многочлены, что стоят в знаменателях лестницы, отвечают на вопрос о том, какими поворотами можно замостить плоскость.
raskadrovka:

<!--id: p-19-->
### p-19
id: p-19
imya:
vopros:
teorema:
zadacha:
doska: otrezok
ves: q-vkl
chetvert: 3
polovina: 2
chast: do-analiza
opiraetsya: p-18
obobshchaetsya-v: p-20
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 21 «Разностные уравнения и формула Бине» (Блок 6. Спектр)
iz-karkasa: тема 21 «Разностные уравнения и формула Бине». Объект: пространство решений трёхчленной рекурренты. Ого: в школе учат «подставь $t^n$» и не объясняют почему. Причина: пространство решений двумерно, сдвиг на нём линеен, а геометрические прогрессии — в точности его собственные векторы.
raskadrovka:

<!--id: p-20-->
### p-20
id: p-20
imya:
vopros:
teorema:
zadacha:
doska: otrezok
ves: q-vkl
chetvert: 3
polovina: 2
chast: do-analiza
opiraetsya: p-19
obobshchaetsya-v: p-21
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 22 «Дискретный оператор Лапласа» (Блок 6. Спектр)
iz-karkasa: тема 22 «Дискретный оператор Лапласа». Объект: лапласиан на графе — не только на отрезке. Отклонение от среднего по соседям; краевые условия.
raskadrovka:

<!--id: p-21-->
### p-21
id: p-21
imya:
vopros:
teorema:
zadacha:
doska: otrezok
ves: q-vkl
chetvert: 3
polovina: 2
chast: do-analiza
opiraetsya: p-20
obobshchaetsya-v: p-22
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 23 «Спектр отрезка» (Блок 6. Спектр)
iz-karkasa: тема 23 «Спектр отрезка». Объект: собственные таблицы. Оказываются синусами, собственные числа — $2\cos\frac{k\pi}{m+2}$. Ого: загадка лекции 18 закрыта, и косинус пришёл из краевых условий, а не ниоткуда.
raskadrovka:

<!--id: p-22-->
### p-22
id: p-22
imya:
vopros:
teorema:
zadacha:
doska: otrezok
ves: q-vkl
chetvert: 3
polovina: 2
chast: do-analiza
opiraetsya: p-21
obobshchaetsya-v: p-23
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 24 «Три формулы одного числа» (Блок 6. Спектр)
iz-karkasa: тема 24 «Три формулы одного числа». Объект: сравнение методов. Изображения, спектр, точный счёт. Ого: при высоте $\le3$ спектральная формула буквально превращается в формулу Бине, $d_3(n)=F_{2n-1}$. «Страшная сумма по спектру» — это Бине с большим числом корней.
raskadrovka:

<!--id: p-23-->
### p-23
id: p-23
imya:
vopros:
teorema:
zadacha:
doska: otrezok
ves: q-vkl
chetvert: 3
polovina: 2
chast: do-analiza
opiraetsya: p-22
obobshchaetsya-v: p-24
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 25 «Числа Каталана как интеграл» (Блок 6. Спектр)
iz-karkasa: тема 25 «Числа Каталана как интеграл». Объект: $\frac2\pi\int_0^\pi(2\cos\theta)^{2n}\sin^2\theta\,d\theta$. Ого: целое число, которое полгода считали биекциями, равно интегралу от тригонометрии. А вес $\sin^2\theta$ при раскрытии оказывается принципом отражения из лекции 10 — то же вычитание, записанное на другом языке.
raskadrovka:

<!--id: p-24-->
### p-24
id: p-24
imya:
vopros:
teorema:
zadacha:
doska: otrezok
ves: q-vkl
chetvert: 4
polovina: 2
chast: do-analiza
opiraetsya: p-23
obobshchaetsya-v: p-25
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 26 «Время перемешивания» (Блок 6. Спектр)
iz-karkasa: тема 26 «Время перемешивания». Объект: спектральная щель. Через сколько шагов фишка забывает старт; почему это $m^2$ и почему на той же длине переключаются формулы лекции 24. «Услышать форму» одним сюжетом.
raskadrovka:

<!--id: p-25-->
### p-25
id: p-25
imya:
vopros:
teorema:
zadacha:
doska: otrezok
ves: q-vkl
chetvert: 4
polovina: 2
chast: do-analiza
opiraetsya: p-24
obobshchaetsya-v: p-26
adres: владелец — тема вне каркаса, см. iz-karkasa
iz-karkasa: вне каркаса — резерв трёх занятий четверти IV под пустую клетку «отрезок × вес включён» (Р3 из KARTA-rashozhdeniy.md); кандидаты по KALENDAR-i-sostav.md §«Что делать с тремя свободными слотами»: $q$-цепная дробь, многочлены Шура, дробь из письма — выбор и порядок не сделаны здесь (архитектура, не заполнение)
raskadrovka:

<!--id: p-26-->
### p-26
id: p-26
imya:
vopros:
teorema:
zadacha:
doska: otrezok
ves: q-vkl
chetvert: 4
polovina: 2
chast: do-analiza
opiraetsya: p-25
obobshchaetsya-v: p-27
adres: владелец — тема вне каркаса, см. iz-karkasa
iz-karkasa: вне каркаса — резерв трёх занятий четверти IV под пустую клетку «отрезок × вес включён» (Р3 из KARTA-rashozhdeniy.md); кандидаты по KALENDAR-i-sostav.md §«Что делать с тремя свободными слотами»: $q$-цепная дробь, многочлены Шура, дробь из письма — выбор и порядок не сделаны здесь (архитектура, не заполнение)
raskadrovka:

<!--id: p-27-->
### p-27
id: p-27
imya:
vopros:
teorema:
zadacha:
doska: otrezok
ves: q-vkl
chetvert: 4
polovina: 2
chast: do-analiza
opiraetsya: p-26
obobshchaetsya-v: p-28
adres: владелец — тема вне каркаса, см. iz-karkasa
iz-karkasa: вне каркаса — резерв трёх занятий четверти IV под пустую клетку «отрезок × вес включён» (Р3 из KARTA-rashozhdeniy.md); кандидаты по KALENDAR-i-sostav.md §«Что делать с тремя свободными слотами»: $q$-цепная дробь, многочлены Шура, дробь из письма — выбор и порядок не сделаны здесь (архитектура, не заполнение)
raskadrovka:

<!--id: p-28-->
### p-28
id: p-28
imya:
vopros:
teorema:
zadacha:
doska: predel
ves: q-vkl
chetvert: 4
polovina: 2
chast: analiz
opiraetsya: p-27
obobshchaetsya-v: p-29
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 27 «Формула Стирлинга» (Блок 7. Пределы)
iz-karkasa: тема 27 «Формула Стирлинга». Объект: асимптотика факториала. Колокол из биномиальных коэффициентов; локальная предельная теорема в самой ручной форме.
raskadrovka:

<!--id: p-29-->
### p-29
id: p-29
imya:
vopros:
teorema:
zadacha:
doska: predel
ves: q-vkl
chetvert: 4
polovina: 2
chast: analiz
opiraetsya: p-28
obobshchaetsya-v: p-30
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 28 «Особенности производящих функций» (Блок 7. Пределы)
iz-karkasa: тема 28 «Особенности производящих функций». Объект: особенность ряда. Корень у функции Каталана даёт $n^{-3/2}$ для первого возвращения; полюс коридора даёт скорость роста. Ого: показатель $-3/2$ из точной формулы Каталана не читается вообще, а из вида особенности — сразу.
raskadrovka:

<!--id: p-30-->
### p-30
id: p-30
imya:
vopros:
teorema:
zadacha:
doska: predel
ves: q-vkl
chetvert: 4
polovina: 2
chast: analiz
opiraetsya: p-29
obobshchaetsya-v: p-31
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 29 «Закон арксинуса» (Блок 7. Пределы)
iz-karkasa: тема 29 «Закон арксинуса». Объект: доля времени выше оси. Ого: все доли равновероятны — ответ, противоречащий любой интуиции.
raskadrovka:

<!--id: p-31-->
### p-31
id: p-31
imya:
vopros:
teorema:
zadacha:
doska: predel
ves: q-vkl
chetvert: 4
polovina: 2
chast: analiz
opiraetsya: p-30
obobshchaetsya-v: p-32
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 30 «Броуновское движение» (Блок 7. Пределы)
iz-karkasa: тема 30 «Броуновское движение». Объект: предельная картинка. Лекция-симуляция: масштабирование, самоподобие, ничего не доказываем.
raskadrovka:

<!--id: p-32-->
### p-32
id: p-32
imya:
vopros:
teorema:
zadacha:
doska: predel
ves: q-vkl
chetvert: 4
polovina: 2
chast: analiz
opiraetsya: p-31
obobshchaetsya-v: p-33
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 31 «Уравнение теплопроводности» (Блок 7. Пределы)
iz-karkasa: тема 31 «Уравнение теплопроводности». Объект: непрерывный лапласиан. Синусы как моды закреплённой струны; дискретное переходит в непрерывное.
raskadrovka:

<!--id: p-33-->
### p-33
id: p-33
imya:
vopros:
teorema:
zadacha:
doska: predel
ves: q-vkl
chetvert: 4
polovina: 2
chast: analiz
opiraetsya: p-32
obobshchaetsya-v: finish
adres: kurs-puti-i-volny/plan/src/karkas.md — тема 32 «Тэта-функция» (Блок 7. Пределы)
iz-karkasa: тема 32 «Тэта-функция». Объект: $\theta(s)=\sum e^{-\pi j^2 s}$ и её симметрия $\theta(1/s)=\sqrt s\,\theta(s)$. Ого: это предел равенства «сумма по образам = сумма по спектру». Развёртка против ряда Фурье. Отсюда виден вход к теореме о четырёх квадратах.
raskadrovka:

<!--id: finish-->
### finish — служебный якорь конца года

Не пункт занятия — точка, во что «перерастает» последний пункт года (`p-33`), чтобы гейт
`obobshchaetsya-v` не требовал от последнего занятия несуществующего продолжения. Финал (модулярность
и что дальше) сознательно не назван: он не готов и на план года не влияет (та же оговорка, что у
`plan.md`, `## Долги каркаса` в `karkas.md`).

