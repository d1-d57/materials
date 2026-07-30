---
tab: I. Треугольник
status: chernovik
poryadok: 1
registr: читаемый
---

# Блок I. Треугольник

> поле:mn **Что это.** Тексты слайдов лекции в том объёме, в котором они лягут на слайд, — собранные лентой, без сценовых разворотов и без блюров. Каждый раздел ниже = один слайд; нумерация совпадает с номерами слайдов раскадровки. Пилот: S1–S5, до разреза по центру. Текст — тезисы под слова лектора, не самодостаточное изложение: доказательства произносятся, на слайде остаются утверждения и опоры. Иллюстрации нарисованы.

## Внутри треугольника Паскаля

Открытая лекция курса «Перечислительная комбинаторика». ЛШП NlogN, август.

## Пьяница у обрыва

> поле:mn **Раскладка.** Мало текста, крупный канвас снизу.

Пьяница стоит на самом краю обрыва. Каждую секунду он шагает влево или вправо, с равной вероятностью. Шаг влево с края — шаг в пропасть

**С какой вероятностью он продержится $2n$ шагов?**

За эту лекцию мы её решим. По дороге встретим тождество Вандермонда и числа Фибоначчи, а в конце посмотрим на треугольник Серпинского

<figure>
<svg viewBox="0 0 400 156" width="620" role="img" aria-label="Ломаная траектория частицы: время слева направо, положение вверх; частица стартует на нулевом уровне и ни разу не опускается до нижней запретной черты">
<line class="s-thin" x1="38" y1="112" x2="386" y2="112" stroke-dasharray="5 4"/>
<line class="s-line" x1="38" y1="134" x2="386" y2="134"/>
<polyline class="s-accent" points="44,112 72,90 100,112 128,90 156,68 184,46 212,24 240,46 268,68 296,46 324,68 352,90 380,112"/>
<circle class="s-node" cx="72" cy="90" r="3.4"/><circle class="s-node" cx="100" cy="112" r="3.4"/><circle class="s-node" cx="128" cy="90" r="3.4"/><circle class="s-node" cx="156" cy="68" r="3.4"/><circle class="s-node" cx="184" cy="46" r="3.4"/><circle class="s-node" cx="212" cy="24" r="3.4"/><circle class="s-node" cx="240" cy="46" r="3.4"/><circle class="s-node" cx="268" cy="68" r="3.4"/><circle class="s-node" cx="296" cy="46" r="3.4"/><circle class="s-node" cx="324" cy="68" r="3.4"/><circle class="s-node" cx="352" cy="90" r="3.4"/><circle class="s-node" cx="380" cy="112" r="3.4"/>
<circle class="s-node-r" cx="44" cy="112" r="4.4"/>
<text class="s-txt-m" x="30" y="116" text-anchor="end">0</text>
<text class="s-txt-m" x="30" y="138" text-anchor="end">−1</text>
</svg>
<figcaption>Частица стартует в нуле; сплошная черта внизу — обрыв, до которого траектория не должна дотянуться ни разу.</figcaption>
</figure>

## Столбцы

> поле:mn **Раскладка.** Текст слева, вертикальная полоса иллюстраций справа; таблица заполняется вместе с текстом.

Отложим обрыв. Частица стоит в нуле и каждую секунду шагает влево или вправо

**Где она окажется через секунду, через две, через три — и с какой вероятностью?**

Записываем столбцами: время — столбец, положение — строка

$$1 \quad\bigl|\quad \tfrac12,\ \tfrac12 \quad\bigl|\quad \tfrac14,\ \tfrac12,\ \tfrac14 \quad\bigl|\quad \tfrac18,\ \tfrac38,\ \tfrac38,\ \tfrac18$$

Клетки идут через одну: положение и время всегда одной чётности

В клетку частица приходит либо снизу, либо сверху. Формула полной вероятности даёт рекурсию: **каждое число — среднее двух соседей слева**

<figure>
<svg viewBox="0 0 410 254" width="620" role="img" aria-label="Вероятности разложены столбцами: столбец — момент времени, строка — положение; ненулевые значения образуют треугольник, положенный на бок">
<text class="s-txt" x="40" y="129" text-anchor="middle">1</text>
<text class="s-txt" x="122" y="153" text-anchor="middle">1/2</text>
<text class="s-txt" x="122" y="105" text-anchor="middle">1/2</text>
<text class="s-txt" x="204" y="177" text-anchor="middle">1/4</text>
<text class="s-txt" x="204" y="129" text-anchor="middle">1/2</text>
<text class="s-txt" x="204" y="81" text-anchor="middle">1/4</text>
<text class="s-txt" x="286" y="201" text-anchor="middle">1/8</text>
<text class="s-txt" x="286" y="153" text-anchor="middle">3/8</text>
<text class="s-txt" x="286" y="105" text-anchor="middle">3/8</text>
<text class="s-txt" x="286" y="57" text-anchor="middle">1/8</text>
<text class="s-txt" x="368" y="225" text-anchor="middle">1/16</text>
<text class="s-txt" x="368" y="177" text-anchor="middle">4/16</text>
<text class="s-txt" x="368" y="129" text-anchor="middle">6/16</text>
<text class="s-txt" x="368" y="81" text-anchor="middle">4/16</text>
<text class="s-txt" x="368" y="33" text-anchor="middle">1/16</text>
</svg>
<figcaption>Столбец — момент времени, строка — положение. Через шаг положение меняет чётность, поэтому заполненные клетки идут через одну.</figcaption>
</figure>

<figure>
<svg viewBox="0 0 410 254" width="620" role="img" aria-label="Те же вероятности, поверх них проложена одна ломаная — путь частицы по клеткам">
<polyline class="s-accent" points="40,109 122,85 204,61 286,85 368,109"/>
<text class="s-txt" x="40" y="129" text-anchor="middle">1</text>
<text class="s-txt" x="122" y="153" text-anchor="middle">1/2</text>
<text class="s-txt" x="122" y="105" text-anchor="middle">1/2</text>
<text class="s-txt" x="204" y="177" text-anchor="middle">1/4</text>
<text class="s-txt" x="204" y="129" text-anchor="middle">1/2</text>
<text class="s-txt" x="204" y="81" text-anchor="middle">1/4</text>
<text class="s-txt" x="286" y="201" text-anchor="middle">1/8</text>
<text class="s-txt" x="286" y="153" text-anchor="middle">3/8</text>
<text class="s-txt" x="286" y="105" text-anchor="middle">3/8</text>
<text class="s-txt" x="286" y="57" text-anchor="middle">1/8</text>
<text class="s-txt" x="368" y="225" text-anchor="middle">1/16</text>
<text class="s-txt" x="368" y="177" text-anchor="middle">4/16</text>
<text class="s-txt" x="368" y="129" text-anchor="middle">6/16</text>
<text class="s-txt" x="368" y="81" text-anchor="middle">4/16</text>
<text class="s-txt" x="368" y="33" text-anchor="middle">1/16</text>
<circle class="s-node-a" cx="40" cy="109" r="3.4"/>
<circle class="s-node-a" cx="122" cy="85" r="3.4"/>
<circle class="s-node-a" cx="204" cy="61" r="3.4"/>
<circle class="s-node-a" cx="286" cy="85" r="3.4"/>
<circle class="s-node-a" cx="368" cy="109" r="3.4"/>
</svg>
<figcaption>Каждая ломаная — путь через соседние клетки слева направо. Таблица и считает, сколько таких путей приходит в клетку.</figcaption>
</figure>

<figure>
<svg viewBox="0 0 120 154" width="200" role="img" aria-label="В одну выделенную клетку приходят две стрелки — сверху-слева и снизу-слева, каждая с весом одна вторая">
<line class="s-ar-m" x1="30" y1="29" x2="82" y2="72"/>
<polyline class="s-ar-m" points="72.5,69.4 82,72 77.5,63.2"/>
<line class="s-ar-m" x1="30" y1="127" x2="82" y2="84"/>
<polyline class="s-ar-m" points="77.6,92.8 82,84 72.6,86.6"/>
<circle class="s-node" cx="24" cy="24" r="4.4"/>
<circle class="s-node" cx="24" cy="132" r="4.4"/>
<circle class="s-node-r" cx="90" cy="78" r="5.2"/>
<text class="s-txt" x="52" y="38" text-anchor="middle">1/2</text>
<text class="s-txt" x="46" y="106" text-anchor="middle">1/2</text>
</svg>
<figcaption>В клетку можно попасть ровно из двух соседних, и каждая отдаёт половину своей вероятности.</figcaption>
</figure>

## Треугольник Паскаля

> поле:mn **Раскладка.** Мало текста, два треугольника рядом на всю ширину: слева дроби, справа целые числа.

Дроби мешают смотреть. Спросим иначе: **сколько траекторий ведёт в клетку?** Это то же самое, умноженное на $2^n$

Среднее превращается в сумму: каждое число — сумма двух соседей слева. Это **треугольник Паскаля**

> поле:mn ✂ **разрез №1** — по последнему шагу.

Тот же счёт читается иначе: траектории в клетке разложены на две кучи по последнему шагу

<figure>
<svg viewBox="0 0 580 248" width="620" role="img" aria-label="Слева треугольник из дробей со знаменателями — степенями двойки, справа тот же треугольник из целых чисел; между ними стрелка">
<text class="s-txt" x="150" y="48" text-anchor="middle">1</text>
<text class="s-txt" x="133" y="88" text-anchor="middle">1/2</text>
<text class="s-txt" x="167" y="88" text-anchor="middle">1/2</text>
<text class="s-txt" x="116" y="128" text-anchor="middle">1/4</text>
<text class="s-txt" x="150" y="128" text-anchor="middle">2/4</text>
<text class="s-txt" x="184" y="128" text-anchor="middle">1/4</text>
<text class="s-txt" x="99" y="168" text-anchor="middle">1/8</text>
<text class="s-txt" x="133" y="168" text-anchor="middle">3/8</text>
<text class="s-txt" x="167" y="168" text-anchor="middle">3/8</text>
<text class="s-txt" x="201" y="168" text-anchor="middle">1/8</text>
<text class="s-txt" x="82" y="208" text-anchor="middle">1/16</text>
<text class="s-txt" x="116" y="208" text-anchor="middle">4/16</text>
<text class="s-txt" x="150" y="208" text-anchor="middle">6/16</text>
<text class="s-txt" x="184" y="208" text-anchor="middle">4/16</text>
<text class="s-txt" x="218" y="208" text-anchor="middle">1/16</text>
<text class="s-txt" x="452" y="48" text-anchor="middle">1</text>
<text class="s-txt" x="435" y="88" text-anchor="middle">1</text>
<text class="s-txt" x="469" y="88" text-anchor="middle">1</text>
<text class="s-txt" x="418" y="128" text-anchor="middle">1</text>
<text class="s-txt" x="452" y="128" text-anchor="middle">2</text>
<text class="s-txt" x="486" y="128" text-anchor="middle">1</text>
<text class="s-txt" x="401" y="168" text-anchor="middle">1</text>
<text class="s-txt" x="435" y="168" text-anchor="middle">3</text>
<text class="s-txt" x="469" y="168" text-anchor="middle">3</text>
<text class="s-txt" x="503" y="168" text-anchor="middle">1</text>
<text class="s-txt" x="384" y="208" text-anchor="middle">1</text>
<text class="s-txt" x="418" y="208" text-anchor="middle">4</text>
<text class="s-txt" x="452" y="208" text-anchor="middle">6</text>
<text class="s-txt" x="486" y="208" text-anchor="middle">4</text>
<text class="s-txt" x="520" y="208" text-anchor="middle">1</text>
<line class="s-ar-m" x1="272" y1="128" x2="352" y2="128"/>
<polyline class="s-ar-m" points="343,123.5 352,128 343,132.5"/>
</svg>
<figcaption>Отбросим общий знаменатель строки — таблица вероятностей превращается в треугольник из целых чисел.</figcaption>
</figure>

## Один объект, много обликов

> поле:mn **Раскладка.** Текст слева, четыре облика столбиком в правой полосе.

Одна траектория, четыре облика:

- ломаная;
- слово из О и Р;
- маршрут в решётке;
- выбор $k$ мест из $n$, то есть $\binom nk$

Считать можно рекуррентно, комбинаторно или из многочлена $(1+x)^n$

**Облик решает, что даётся даром.** Симметрия — это замена О ↔ Р. Сумма строки равна $2^n$, потому что частица где-то да находится

**Сколькими способами выбрать команду из $k+1$ человек и капитана в ней?** Команда, потом капитан: $(k+1)\binom n{k+1}$. Или $k$ рядовых, потом капитан из оставшихся: $(n-k)\binom nk$

$$\binom n{k+1}=\frac{n-k}{k+1}\binom nk=\frac{n-k}{k+1}\cdot\frac{n-k+1}{k}\binom n{k-1}=\dots=\frac{n(n-1)\cdots(n-k)}{(k+1)!}$$

<figure>
<svg viewBox="0 0 300 344" width="300" role="img" aria-label="Одна и та же последовательность из четырёх бросков в четырёх обликах: ломаная траектория вверх-вниз-вниз-вверх; ряд из четырёх кружков, где залиты первый и четвёртый; ступенчатый маршрут по решётке из левого нижнего угла в правый верхний; ряд из четырёх клеток, где закрашены первая и четвёртая">
<line class="s-thin" x1="70" y1="62" x2="230" y2="62" stroke-dasharray="5 4"/>
<polyline class="s-line" points="82,62 116,40 150,62 184,84 218,62"/>
<circle class="s-node-a" cx="82" cy="62" r="3.4"/>
<circle class="s-node" cx="116" cy="40" r="3.4"/>
<circle class="s-node" cx="150" cy="62" r="3.4"/>
<circle class="s-node" cx="184" cy="84" r="3.4"/>
<circle class="s-node-a" cx="218" cy="62" r="3.4"/>
<circle class="s-node-r" cx="82" cy="136" r="7"/>
<circle class="s-node" cx="116" cy="136" r="7"/>
<circle class="s-node" cx="150" cy="136" r="7"/>
<circle class="s-node-r" cx="184" cy="136" r="7"/>
<line class="s-thin" x1="110" y1="180" x2="190" y2="180"/>
<line class="s-thin" x1="110" y1="220" x2="190" y2="220"/>
<line class="s-thin" x1="110" y1="260" x2="190" y2="260"/>
<line class="s-thin" x1="110" y1="180" x2="110" y2="260"/>
<line class="s-thin" x1="150" y1="180" x2="150" y2="260"/>
<line class="s-thin" x1="190" y1="180" x2="190" y2="260"/>
<polyline class="s-accent" points="110,260 150,260 150,220 150,180 190,180"/>
<circle class="s-node-a" cx="110" cy="260" r="3.4"/>
<circle class="s-node-a" cx="190" cy="180" r="3.4"/>
<rect class="s-fillsh" x="82" y="296" width="34" height="26"/>
<rect class="s-line" x="116" y="296" width="34" height="26"/>
<rect class="s-line" x="150" y="296" width="34" height="26"/>
<rect class="s-fillsh" x="184" y="296" width="34" height="26"/>
</svg>
<figcaption>Один и тот же исход четырёх бросков в четырёх обликах: траектория, слово (залитый кружок — орёл), маршрут по решётке, выбор мест под орлов.</figcaption>
</figure>

<figure>
<svg viewBox="0 0 240 112" width="440" role="img" aria-label="Строка треугольника Паскаля 1 4 6 4 1 с вертикальной осью посередине: крайние числа переходят друг в друга, вторые с краю — тоже">
<line class="s-dash" x1="120" y1="18" x2="120" y2="32"/>
<line class="s-dash" x1="120" y1="54" x2="120" y2="100"/>
<text class="s-txt" x="24" y="46" text-anchor="middle">1</text>
<text class="s-txt" x="72" y="46" text-anchor="middle">4</text>
<text class="s-txt" x="120" y="46" text-anchor="middle">6</text>
<text class="s-txt" x="168" y="46" text-anchor="middle">4</text>
<text class="s-txt" x="216" y="46" text-anchor="middle">1</text>
<path class="s-thin" d="M 82,60 Q 120,80 158,60"/>
<path class="s-ar-m" d="M 84,56 l-6,7 8,2 z"/>
<path class="s-ar-m" d="M 156,56 l6,7 -8,2 z"/>
<path class="s-thin" d="M 32,62 Q 120,102 208,62"/>
<path class="s-ar-m" d="M 34,58 l-6,7 8,2 z"/>
<path class="s-ar-m" d="M 206,58 l6,7 -8,2 z"/>
</svg>
<figcaption>Замена всех орлов на решки отражает строку относительно середины: равноудалённые от краёв числа совпадают.</figcaption>
</figure>

<figure>
<svg viewBox="0 0 240 210" width="300" role="img" aria-label="Сверху: рамка охватывает четыре кружка, один из них залит. Снизу: та же четвёрка, но рамка охватывает три кружка, а залитый стоит вне рамки, и стрелка ведёт от рамки к нему">
<rect class="s-fillsh" x="38" y="36" width="164" height="44" rx="8"/>
<circle class="s-node" cx="62" cy="58" r="9"/>
<circle class="s-node-r" cx="102" cy="58" r="9"/>
<circle class="s-node" cx="142" cy="58" r="9"/>
<circle class="s-node" cx="182" cy="58" r="9"/>
<rect class="s-fillsh" x="26" y="132" width="124" height="44" rx="8"/>
<circle class="s-node" cx="50" cy="154" r="9"/>
<circle class="s-node" cx="90" cy="154" r="9"/>
<circle class="s-node" cx="130" cy="154" r="9"/>
<line class="s-thin" x1="160" y1="154" x2="186" y2="154"/>
<path class="s-ar-m" d="M 184,150 l9,4 -9,4 z"/>
<circle class="s-node-r" cx="206" cy="154" r="9"/>
</svg>
<figcaption>Одну и ту же пару «команда с капитаном» можно собрать двумя способами: сверху — команда, потом капитан внутри неё; снизу — рядовые, а капитан из оставшихся.</figcaption>
</figure>

<figure>
<svg viewBox="0 0 400 116" width="700" role="img" aria-label="Пять чисел строки треугольника Паскаля 1, 5, 10, 10, 5 связаны стрелками слева направо; над каждой стрелкой стоит множитель: пять первых, четыре вторых, три третьих, два четвёртых; первое число обведено акцентным кольцом как исходное">
<line class="s-thin" x1="74" y1="76" x2="101" y2="76"/>
<path class="s-ar-m" d="M 99,72 l9,4 -9,4 z"/>
<line class="s-thin" x1="148" y1="76" x2="177" y2="76"/>
<path class="s-ar-m" d="M 175,72 l9,4 -9,4 z"/>
<line class="s-thin" x1="224" y1="76" x2="253" y2="76"/>
<path class="s-ar-m" d="M 251,72 l9,4 -9,4 z"/>
<line class="s-thin" x1="300" y1="76" x2="329" y2="76"/>
<path class="s-ar-m" d="M 327,72 l9,4 -9,4 z"/>
<circle class="s-accent" cx="50" cy="76" r="21"/>
<circle class="s-node" cx="50" cy="76" r="16"/>
<circle class="s-node" cx="126" cy="76" r="16"/>
<circle class="s-node" cx="202" cy="76" r="16"/>
<circle class="s-node" cx="278" cy="76" r="16"/>
<circle class="s-node" cx="354" cy="76" r="16"/>
<text class="s-txt" x="50" y="81" text-anchor="middle">1</text>
<text class="s-txt" x="126" y="81" text-anchor="middle">5</text>
<text class="s-txt" x="202" y="81" text-anchor="middle">10</text>
<text class="s-txt" x="278" y="81" text-anchor="middle">10</text>
<text class="s-txt" x="354" y="81" text-anchor="middle">5</text>
<text class="s-txt-m" x="88" y="58" text-anchor="middle">5/1</text>
<text class="s-txt-m" x="164" y="58" text-anchor="middle">4/2</text>
<text class="s-txt-m" x="240" y="58" text-anchor="middle">3/3</text>
<text class="s-txt-m" x="316" y="58" text-anchor="middle">2/4</text>
</svg>
<figcaption>Строка раскручивается из единицы слева направо: очередное число получается из предыдущего умножением на дробь над стрелкой.</figcaption>
</figure>

## Разрез по центру

> поле:mn **Раскладка.** Мало текста, крупная горизонтальная иллюстрация снизу: разрез, переворот, две ломаные рядом.

Мы всё время резали по последнему шагу. **А если резать по центру?**

Возьмём путь длины $2n$ с концом в нуле и разрежем пополам. Первая половина кончилась на какой-то высоте, вторая обязана оттуда вернуться в ноль

> поле:mn ✂ **разрез №2** — по центру.

Перевернём вторую половину — получится второй путь длины $n$, кончающийся на **той же высоте**

Путь длины $2n$ в ноль ↔ пара путей длины $n$ на одной высоте

Считаем обе стороны: слева $\binom{2n}n$, справа сумма по высоте — $\sum_k\binom nk^2$

<figure>
<svg viewBox="0 0 360 200" width="620" role="img" aria-label="Путь длины восемь разрезан посередине; вторая половина перевёрнута, получились два пути длины четыре, оба кончающиеся на одной высоте">
<line class="s-thin" x1="24" y1="80" x2="276" y2="80" stroke-dasharray="5 4"/>
<line class="s-thin" x1="24" y1="36" x2="276" y2="36" stroke-dasharray="5 4"/>
<polyline class="s-line" points="30,80 60,58 90,36 120,58 150,36"/>
<polyline class="s-accent" points="150,36 180,58 210,80 240,58 270,80"/>
<line class="s-dash" x1="150" y1="18" x2="150" y2="98"/>
<circle class="s-node-a" cx="30" cy="80" r="3.4"/>
<circle class="s-node" cx="60" cy="58" r="3.4"/>
<circle class="s-node" cx="90" cy="36" r="3.4"/>
<circle class="s-node" cx="120" cy="58" r="3.4"/>
<circle class="s-node-r" cx="150" cy="36" r="3.4"/>
<circle class="s-node" cx="180" cy="58" r="3.4"/>
<circle class="s-node" cx="210" cy="80" r="3.4"/>
<circle class="s-node" cx="240" cy="58" r="3.4"/>
<circle class="s-node-a" cx="270" cy="80" r="3.4"/>
<line class="s-thin" x1="24" y1="170" x2="336" y2="170" stroke-dasharray="5 4"/>
<line class="s-thin" x1="24" y1="126" x2="336" y2="126" stroke-dasharray="5 4"/>
<polyline class="s-line" points="30,170 60,148 90,126 120,148 150,126"/>
<polyline class="s-accent" points="210,170 240,148 270,170 300,148 330,126"/>
<circle class="s-node-a" cx="30" cy="170" r="3.4"/>
<circle class="s-node" cx="60" cy="148" r="3.4"/>
<circle class="s-node" cx="90" cy="126" r="3.4"/>
<circle class="s-node" cx="120" cy="148" r="3.4"/>
<circle class="s-node-r" cx="150" cy="126" r="3.4"/>
<circle class="s-node-a" cx="210" cy="170" r="3.4"/>
<circle class="s-node" cx="240" cy="148" r="3.4"/>
<circle class="s-node" cx="270" cy="170" r="3.4"/>
<circle class="s-node" cx="300" cy="148" r="3.4"/>
<circle class="s-node-r" cx="330" cy="126" r="3.4"/>
</svg>
<figcaption>Разрез по центру: вторая половина перевёрнута, и получились два пути вдвое короче, кончающиеся на одной высоте.</figcaption>
</figure>

## Сумма квадратов

> поле:mn **Раскладка.** Текст слева, справа строка треугольника и центральный столбец.

Что это значит на треугольнике: возводим числа строки в квадрат и складываем

$$1+4+1=6 \qquad 1+9+9+1=20 \qquad 1+16+36+16+1=70$$

**2, 6, 20, 70** — и это ровно центральный столбец. Сошлось

**Два игрока бросили по 10 монет. С какой вероятностью у них поровну орлов?** Это и есть пара путей на одной высоте: ответ $\binom{20}{10}/4^{10}$

То же самое даёт многочлен. Коэффициент при $x^n$ слева и справа:

$$(1+x)^{2n}=\bigl[(1+x)^n\bigr]^2=\Bigl[\sum_k\binom nk x^k\Bigr]^2$$

Слева при $x^n$ стоит $\binom{2n}n$, справа — $\sum_k\binom nk\binom n{n-k}=\sum_k\binom nk^2$

А если резать не пополам, выйдет **тождество Вандермонда** — в листок

<figure>
<svg viewBox="0 0 420 160" width="620" role="img" aria-label="Строка треугольника Паскаля, под ней квадраты её чисел, справа их сумма — число центрального столбца">
<text class="s-txt" x="60" y="46" text-anchor="middle">1</text>
<text class="s-txt" x="112" y="46" text-anchor="middle">4</text>
<text class="s-txt" x="164" y="46" text-anchor="middle">6</text>
<text class="s-txt" x="216" y="46" text-anchor="middle">4</text>
<text class="s-txt" x="268" y="46" text-anchor="middle">1</text>
<text class="s-txt" x="60" y="104" text-anchor="middle">1</text>
<line class="s-thin" x1="60" y1="58" x2="60" y2="86"/>
<text class="s-txt" x="112" y="104" text-anchor="middle">16</text>
<line class="s-thin" x1="112" y1="58" x2="112" y2="86"/>
<text class="s-txt" x="164" y="104" text-anchor="middle">36</text>
<line class="s-thin" x1="164" y1="58" x2="164" y2="86"/>
<text class="s-txt" x="216" y="104" text-anchor="middle">16</text>
<line class="s-thin" x1="216" y1="58" x2="216" y2="86"/>
<text class="s-txt" x="268" y="104" text-anchor="middle">1</text>
<line class="s-thin" x1="268" y1="58" x2="268" y2="86"/>
<line class="s-thin" x1="40" y1="122" x2="272" y2="122"/>
<line class="s-ar-a" x1="290" y1="104" x2="330" y2="104"/>
<polyline class="s-ar-a" points="321,99.5 330,104 321,108.5"/>
<text class="s-txt" x="366" y="110" text-anchor="middle">70</text>

</svg>
<figcaption>Возводим числа строки в квадрат и складываем — получается число из центрального столбца.</figcaption>
</figure>

