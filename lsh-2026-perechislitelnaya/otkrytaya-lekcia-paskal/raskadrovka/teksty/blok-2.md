---
tab: II. Запреты
status: chernovik
poryadok: 2
registr: читаемый
---

# Блок II. Запреты

> поле:mn **Что это.** Вторая вкладка, слайды S8–S15 раскадровки. Нумерация разделов идёт от единицы внутри вкладки — это S8, S9 и так далее. Раскладка помечена у каждого слайда.

## Запретим что-нибудь

> поле:mn **Раскладка.** Мало текста, крупно вопрос. Поворот объявляется вслух.

**С какой вероятностью за $n$ бросков не выпадет двух орлов подряд?**

Выпишем все хорошие слова: длины 1, потом 2, потом 3

$$2 \qquad 3 \qquad 5$$

Это **числа Фибоначчи**

> поле:mn ✂ **разрез №3** — снова по последнему шагу.

Последняя Р — перед ней любое хорошее слово длины $n-1$. Последняя О — перед ней обязана стоять Р, дальше любое длины $n-2$

$$a_n=a_{n-1}+a_{n-2}$$

<figure>
<svg viewBox="0 0 320 184" width="620" role="img" aria-label="Дерево слов из букв О и Р без двух О подряд: из корня две ветви, на втором шаге три, на третьем пять концов">
<line class="s-line" x1="44" y1="82.5" x2="122" y2="53"/>
<line class="s-line" x1="44" y1="82.5" x2="122" y2="112"/>
<line class="s-line" x1="122" y1="53" x2="200" y2="53"/>
<line class="s-line" x1="122" y1="112" x2="200" y2="92"/>
<line class="s-line" x1="122" y1="112" x2="200" y2="131"/>
<line class="s-line" x1="200" y1="53" x2="278" y2="40"/>
<line class="s-line" x1="200" y1="53" x2="278" y2="66"/>
<line class="s-line" x1="200" y1="92" x2="278" y2="92"/>
<line class="s-line" x1="200" y1="131" x2="278" y2="118"/>
<line class="s-line" x1="200" y1="131" x2="278" y2="144"/>
<text class="s-txt" x="83" y="62" text-anchor="middle">О</text>
<text class="s-txt" x="83" y="111" text-anchor="middle">Р</text>
<text class="s-txt" x="161" y="45" text-anchor="middle">Р</text>
<text class="s-txt" x="149" y="99" text-anchor="middle">О</text>
<text class="s-txt" x="173" y="137" text-anchor="middle">Р</text>
<text class="s-txt" x="227" y="43" text-anchor="middle">О</text>
<text class="s-txt" x="259" y="77" text-anchor="middle">Р</text>
<text class="s-txt" x="231" y="85" text-anchor="middle">Р</text>
<text class="s-txt" x="227" y="121" text-anchor="middle">О</text>
<text class="s-txt" x="251" y="153" text-anchor="middle">Р</text>
<circle class="s-node-r" cx="44" cy="82.5" r="3.4"/>
<circle class="s-node" cx="122" cy="53" r="3.4"/>
<circle class="s-node" cx="122" cy="112" r="3.4"/>
<circle class="s-node" cx="200" cy="53" r="3.4"/>
<circle class="s-node" cx="200" cy="92" r="3.4"/>
<circle class="s-node" cx="200" cy="131" r="3.4"/>
<circle class="s-node" cx="278" cy="40" r="3.4"/>
<circle class="s-node" cx="278" cy="66" r="3.4"/>
<circle class="s-node" cx="278" cy="92" r="3.4"/>
<circle class="s-node" cx="278" cy="118" r="3.4"/>
<circle class="s-node" cx="278" cy="144" r="3.4"/>
</svg>
<figcaption>После орла разрешена только решка, поэтому ветки с двумя О подряд не вырастают вовсе — концов становится 2, 3, 5.</figcaption>
</figure>

## Домики

> поле:mn **Раскладка.** Текст сверху, широкая иллюстрация со сжатием снизу.

Подъёмы встречаются только домиками ∧

**Уберём спуск после каждого подъёма.** Ломаная станет короче, и обратно восстанавливается однозначно

> поле:mn Здесь мы не режем, а сжимаем — единственное такое место в лекции.

Хороших слов с $k$ орлами ровно $\binom{n+1-k}k$, а всего

$$a_n=\sum_k\binom{n+1-k}k$$

Это **восходящие диагонали** треугольника Паскаля: 1, 2, 3, 5, 8, 13

<figure>
<svg viewBox="0 0 524 310" width="700" role="img" aria-label="Сверху ломаная, в которой каждый подъём сразу сменяется спуском: подъёмы собраны в домики, они выделены; снизу та же ломаная после сжатия — каждый домик заменён одним шагом вниз, и ломаная стала короче">
<polyline class="s-line" points="46,52 82,30 118,52 154,30 190,52 226,74 262,52 298,74 334,52 370,74 406,96 442,74 478,96"/>
<polyline class="s-accent" points="46,52 82,30 118,52"/>
<polyline class="s-accent" points="118,52 154,30 190,52"/>
<polyline class="s-accent" points="226,74 262,52 298,74"/>
<polyline class="s-accent" points="298,74 334,52 370,74"/>
<polyline class="s-accent" points="406,96 442,74 478,96"/>
<circle class="s-node-a" cx="46" cy="52" r="3.4"/>
<circle class="s-node" cx="82" cy="30" r="3.4"/>
<circle class="s-node" cx="118" cy="52" r="3.4"/>
<circle class="s-node" cx="154" cy="30" r="3.4"/>
<circle class="s-node" cx="190" cy="52" r="3.4"/>
<circle class="s-node" cx="226" cy="74" r="3.4"/>
<circle class="s-node" cx="262" cy="52" r="3.4"/>
<circle class="s-node" cx="298" cy="74" r="3.4"/>
<circle class="s-node" cx="334" cy="52" r="3.4"/>
<circle class="s-node" cx="370" cy="74" r="3.4"/>
<circle class="s-node" cx="406" cy="96" r="3.4"/>
<circle class="s-node" cx="442" cy="74" r="3.4"/>
<circle class="s-node-a" cx="478" cy="96" r="3.4"/>
<path class="s-ar-m" d="M262,104 L262,124"/>
<path class="s-ar-m" d="M257.5,123 l4.5,9 l4.5,-9 z"/>
<polyline class="s-line" points="136,136 172,158 208,180 244,202 280,224 316,246 352,268 388,290"/>
<polyline class="s-accent" points="136,136 172,158 208,180"/>
<polyline class="s-accent" points="244,202 280,224 316,246"/>
<polyline class="s-accent" points="352,268 388,290"/>
<circle class="s-node-a" cx="136" cy="136" r="3.4"/>
<circle class="s-node" cx="172" cy="158" r="3.4"/>
<circle class="s-node" cx="208" cy="180" r="3.4"/>
<circle class="s-node" cx="244" cy="202" r="3.4"/>
<circle class="s-node" cx="280" cy="224" r="3.4"/>
<circle class="s-node" cx="316" cy="246" r="3.4"/>
<circle class="s-node" cx="352" cy="268" r="3.4"/>
<circle class="s-node-a" cx="388" cy="290" r="3.4"/>
</svg>
<figcaption>Все подъёмы собраны в домики. Схлопнем каждый домик в один шаг вниз — ломаная станет короче ровно на число домиков.</figcaption>
</figure>

<figure>
<svg viewBox="0 0 278 208" width="430" role="img" aria-label="Треугольник Паскаля из семи строк; пять восходящих диагоналей отмечены пунктиром, у начала каждой стоит сумма её чисел: один, два, три, пять, восемь">
<line class="s-dash" x1="110" y1="77" x2="160" y2="51"/>
<text class="s-txt-m" x="98" y="85" text-anchor="end">1</text>
<line class="s-dash" x1="92" y1="103" x2="194" y2="51"/>
<text class="s-txt-m" x="80" y="111" text-anchor="end">2</text>
<line class="s-dash" x1="76" y1="129" x2="178" y2="77"/>
<text class="s-txt-m" x="64" y="137" text-anchor="end">3</text>
<line class="s-dash" x1="58" y1="155" x2="212" y2="77"/>
<text class="s-txt-m" x="46" y="163" text-anchor="end">5</text>
<line class="s-dash" x1="42" y1="181" x2="194" y2="103"/>
<text class="s-txt-m" x="30" y="189" text-anchor="end">8</text>
<text class="s-txt" x="148" y="34" text-anchor="middle">1</text>
<text class="s-txt" x="131" y="60" text-anchor="middle">1</text>
<text class="s-txt" x="165" y="60" text-anchor="middle">1</text>
<text class="s-txt" x="114" y="86" text-anchor="middle">1</text>
<text class="s-txt" x="148" y="86" text-anchor="middle">2</text>
<text class="s-txt" x="182" y="86" text-anchor="middle">1</text>
<text class="s-txt" x="97" y="112" text-anchor="middle">1</text>
<text class="s-txt" x="131" y="112" text-anchor="middle">3</text>
<text class="s-txt" x="165" y="112" text-anchor="middle">3</text>
<text class="s-txt" x="199" y="112" text-anchor="middle">1</text>
<text class="s-txt" x="80" y="138" text-anchor="middle">1</text>
<text class="s-txt" x="114" y="138" text-anchor="middle">4</text>
<text class="s-txt" x="148" y="138" text-anchor="middle">6</text>
<text class="s-txt" x="182" y="138" text-anchor="middle">4</text>
<text class="s-txt" x="216" y="138" text-anchor="middle">1</text>
<text class="s-txt" x="63" y="164" text-anchor="middle">1</text>
<text class="s-txt" x="97" y="164" text-anchor="middle">5</text>
<text class="s-txt" x="131" y="164" text-anchor="middle">10</text>
<text class="s-txt" x="165" y="164" text-anchor="middle">10</text>
<text class="s-txt" x="199" y="164" text-anchor="middle">5</text>
<text class="s-txt" x="233" y="164" text-anchor="middle">1</text>
<text class="s-txt" x="46" y="190" text-anchor="middle">1</text>
<text class="s-txt" x="80" y="190" text-anchor="middle">6</text>
<text class="s-txt" x="114" y="190" text-anchor="middle">15</text>
<text class="s-txt" x="148" y="190" text-anchor="middle">20</text>
<text class="s-txt" x="182" y="190" text-anchor="middle">15</text>
<text class="s-txt" x="216" y="190" text-anchor="middle">6</text>
<text class="s-txt" x="250" y="190" text-anchor="middle">1</text>
</svg>
<figcaption>Треугольник, разрезанный не по строкам, а наискосок: суммы вдоль пунктира дают 1, 2, 3, 5, 8.</figcaption>
</figure>

## Пьяница возвращается

> поле:mn **Раскладка.** Текст слева, таблица перебора справа. Ключевой слайд: здесь приём отказывает.

**Сколько траекторий длины $2n$ не уходят ниже нуля?**

Выпишем все для $2n=4$. Их шесть

Тот же приём: режем по последнему шагу. Рекуррента есть, таблица строится — а формулы из неё **не видно**

Перебор даёт **2, 6, 20, 70** — те самые числа. Гипотеза: ответ $\binom{2n}n$

Доказательства нет. Нужен другой разрез

<figure>
<svg viewBox="0 0 500 252" width="700" role="img" aria-label="Шесть панелей: все шесть траекторий из четырёх шагов вверх или вниз, которые стартуют на нулевом уровне и ни разу не опускаются ниже него">
<line class="s-thin" x1="18" y1="118" x2="162" y2="118" stroke-dasharray="5 4"/>
<polyline class="s-line" points="30,118 60,96 90,74 120,52 150,30"/>
<circle class="s-node-r" cx="30" cy="118" r="3.4"/>
<circle class="s-node" cx="60" cy="96" r="3.4"/>
<circle class="s-node" cx="90" cy="74" r="3.4"/>
<circle class="s-node" cx="120" cy="52" r="3.4"/>
<circle class="s-node" cx="150" cy="30" r="3.4"/>
<line class="s-thin" x1="178" y1="118" x2="322" y2="118" stroke-dasharray="5 4"/>
<polyline class="s-line" points="190,118 220,96 250,74 280,52 310,74"/>
<circle class="s-node-r" cx="190" cy="118" r="3.4"/>
<circle class="s-node" cx="220" cy="96" r="3.4"/>
<circle class="s-node" cx="250" cy="74" r="3.4"/>
<circle class="s-node" cx="280" cy="52" r="3.4"/>
<circle class="s-node" cx="310" cy="74" r="3.4"/>
<line class="s-thin" x1="338" y1="118" x2="482" y2="118" stroke-dasharray="5 4"/>
<polyline class="s-line" points="350,118 380,96 410,74 440,96 470,74"/>
<circle class="s-node-r" cx="350" cy="118" r="3.4"/>
<circle class="s-node" cx="380" cy="96" r="3.4"/>
<circle class="s-node" cx="410" cy="74" r="3.4"/>
<circle class="s-node" cx="440" cy="96" r="3.4"/>
<circle class="s-node" cx="470" cy="74" r="3.4"/>
<line class="s-thin" x1="18" y1="226" x2="162" y2="226" stroke-dasharray="5 4"/>
<polyline class="s-line" points="30,226 60,204 90,182 120,204 150,226"/>
<circle class="s-node-r" cx="30" cy="226" r="3.4"/>
<circle class="s-node" cx="60" cy="204" r="3.4"/>
<circle class="s-node" cx="90" cy="182" r="3.4"/>
<circle class="s-node" cx="120" cy="204" r="3.4"/>
<circle class="s-node" cx="150" cy="226" r="3.4"/>
<line class="s-thin" x1="178" y1="226" x2="322" y2="226" stroke-dasharray="5 4"/>
<polyline class="s-line" points="190,226 220,204 250,226 280,204 310,182"/>
<circle class="s-node-r" cx="190" cy="226" r="3.4"/>
<circle class="s-node" cx="220" cy="204" r="3.4"/>
<circle class="s-node" cx="250" cy="226" r="3.4"/>
<circle class="s-node" cx="280" cy="204" r="3.4"/>
<circle class="s-node" cx="310" cy="182" r="3.4"/>
<line class="s-thin" x1="338" y1="226" x2="482" y2="226" stroke-dasharray="5 4"/>
<polyline class="s-line" points="350,226 380,204 410,226 440,204 470,226"/>
<circle class="s-node-r" cx="350" cy="226" r="3.4"/>
<circle class="s-node" cx="380" cy="204" r="3.4"/>
<circle class="s-node" cx="410" cy="226" r="3.4"/>
<circle class="s-node" cx="440" cy="204" r="3.4"/>
<circle class="s-node" cx="470" cy="226" r="3.4"/>
</svg>
<figcaption>Все траектории из четырёх шагов, ни разу не уходящие ниже нуля. Их ровно шесть.</figcaption>
</figure>

<figure>
<svg viewBox="0 0 202 152" width="300" role="img" aria-label="Значок разреза ломаной, заключённый в рамку-метку, целиком перечёркнут крест-накрест двумя жирными линиями">
<rect class="s-line" x="27" y="41" width="148" height="70"/>
<polyline class="s-line" points="41,87 71,65 101,87 131,65 161,87"/>
<line class="s-dash" x1="71" y1="51" x2="71" y2="101"/>
<circle class="s-node" cx="41" cy="87" r="3.4"/>
<circle class="s-node-r" cx="71" cy="65" r="3.4"/>
<circle class="s-node" cx="101" cy="87" r="3.4"/>
<circle class="s-node" cx="131" cy="65" r="3.4"/>
<circle class="s-node" cx="161" cy="87" r="3.4"/>
<line class="s-accent" x1="19" y1="33" x2="183" y2="119"/>
<line class="s-accent" x1="19" y1="119" x2="183" y2="33"/>
</svg>
<figcaption>Приём, который только что работал, здесь отказывает: рекуррента есть, а формулы из неё не видно.</figcaption>
</figure>

## Считаем сорвавшихся

> поле:mn **Раскладка.** Мало текста, крупная горизонтальная иллюстрация: путь, вертикаль в первом касании, левый кусок выделен.

Зайдём с изнанки: посчитаем **сорвавшихся** и вычтем. Всего путей с концом на высоте $h$ мы считать умеем

> поле:mn ✂ **разрез №4** — в первый момент попадания в $-1$.

Разрежем путь в первый момент, когда он попал в $-1$

Левый кусок идёт из $0$ в $-1$ и раньше $-1$ не касался

**Что с ним вообще можно сделать?**

<figure>
<svg viewBox="0 0 372 122" width="640" role="img" aria-label="Ломаная из шагов плюс-минус один стартует в нуле и в середине впервые опускается на уровень минус один; в этой точке путь разрезан пунктирной вертикалью, левый кусок выделен, правый доходит до высоты два">
<line class="s-thin" x1="36" y1="70" x2="352" y2="70" stroke-dasharray="5 4"/>
<line class="s-thin" x1="36" y1="94" x2="352" y2="94"/>
<polyline class="s-accent" points="46,70 76,46 106,70 136,46 166,70 196,94"/>
<polyline class="s-line" points="196,94 226,70 256,46 286,70 316,46 346,22"/>
<line class="s-dash" x1="196" y1="18" x2="196" y2="112"/>
<circle class="s-node" cx="46" cy="70" r="3.4"/>
<circle class="s-node" cx="76" cy="46" r="3.4"/>
<circle class="s-node" cx="106" cy="70" r="3.4"/>
<circle class="s-node" cx="136" cy="46" r="3.4"/>
<circle class="s-node" cx="166" cy="70" r="3.4"/>
<circle class="s-node" cx="226" cy="70" r="3.4"/>
<circle class="s-node" cx="256" cy="46" r="3.4"/>
<circle class="s-node" cx="286" cy="70" r="3.4"/>
<circle class="s-node" cx="316" cy="46" r="3.4"/>
<circle class="s-node" cx="346" cy="22" r="3.4"/>
<circle class="s-node-a" cx="46" cy="70" r="3.4"/>
<circle class="s-node-r" cx="196" cy="94" r="4.2"/>
<text class="s-txt-m" x="30" y="74" text-anchor="end">0</text>
<text class="s-txt-m" x="30" y="98" text-anchor="end">−1</text>
</svg>
<figcaption>У сорвавшегося пути есть единственный момент первого касания уровня −1 — он и разрезает путь надвое.</figcaption>
</figure>

## Отражение

> поле:mn **Раскладка.** Текст слева, три кадра отражения столбиком справа.

**Отразим левый кусок относительно уровня $-1$** — больше с ним делать нечего. Отражённый идёт из $-2$ в $-1$

Склеиваем обратно: получился путь из $-2$ в $h$. Соответствие обратимо — первое касание $-1$ никуда не делось

Значит сорвавшихся с концом в $h$ ровно столько, сколько путей из $-2$ в $h$:

$$\binom{L}{\tfrac{L+h}2+1}$$

Всего путей в $h$ было $\binom L{\tfrac{L+h}2}$, значит уцелевших

$$A_h=\binom L{\tfrac{L+h}2}-\binom L{\tfrac{L+h}2+1}$$

При $L=4$ сходится с перебором

<figure>
<svg viewBox="0 0 372 462" width="330" role="img" aria-label="Три кадра сверху вниз: путь с разрезом в точке первого касания уровня минус один; затем левый кусок отражён относительно уровня минус один и идёт из уровня минус два, исходный показан бледно; затем склеенный путь целиком из уровня минус два в ту же конечную высоту">
<line class="s-thin" x1="36" y1="78" x2="352" y2="78" stroke-dasharray="5 4"/>
<line class="s-thin" x1="36" y1="102" x2="352" y2="102" stroke-dasharray="5 4"/>
<polyline class="s-accent" points="46,78 76,54 106,78 136,54 166,78 196,102"/>
<polyline class="s-line" points="196,102 226,78 256,54 286,78 316,54 346,30"/>
<line class="s-dash" x1="196" y1="6" x2="196" y2="126"/>
<circle class="s-node" cx="46" cy="78" r="3.4"/>
<circle class="s-node" cx="76" cy="54" r="3.4"/>
<circle class="s-node" cx="106" cy="78" r="3.4"/>
<circle class="s-node" cx="136" cy="54" r="3.4"/>
<circle class="s-node" cx="166" cy="78" r="3.4"/>
<circle class="s-node" cx="226" cy="78" r="3.4"/>
<circle class="s-node" cx="256" cy="54" r="3.4"/>
<circle class="s-node" cx="286" cy="78" r="3.4"/>
<circle class="s-node" cx="316" cy="54" r="3.4"/>
<circle class="s-node" cx="346" cy="30" r="3.4"/>
<circle class="s-node-a" cx="46" cy="78" r="4.2"/>
<circle class="s-node-r" cx="196" cy="102" r="4.2"/>
<text class="s-txt-m" x="30" y="82" text-anchor="end">0</text>
<text class="s-txt-m" x="30" y="106" text-anchor="end">−1</text>
<line class="s-thin" x1="36" y1="216" x2="352" y2="216" stroke-dasharray="5 4"/>
<line class="s-thin" x1="36" y1="264" x2="352" y2="264" stroke-dasharray="5 4"/>
<line class="s-thin" x1="36" y1="288" x2="352" y2="288" stroke-dasharray="5 4"/>
<line class="s-dash" x1="36" y1="240" x2="352" y2="240"/>
<polyline class="s-thin" points="46,216 76,192 106,216 136,192 166,216 196,240"/>
<polyline class="s-accent" points="46,264 76,288 106,264 136,288 166,264 196,240"/>
<polyline class="s-thin" points="196,240 226,216 256,192 286,216 316,192 346,168"/>
<circle class="s-node" cx="46" cy="264" r="3.4"/>
<circle class="s-node" cx="76" cy="288" r="3.4"/>
<circle class="s-node" cx="106" cy="264" r="3.4"/>
<circle class="s-node" cx="136" cy="288" r="3.4"/>
<circle class="s-node" cx="166" cy="264" r="3.4"/>
<circle class="s-node-a" cx="46" cy="264" r="4.2"/>
<circle class="s-node-r" cx="196" cy="240" r="4.2"/>
<text class="s-txt-m" x="30" y="220" text-anchor="end">0</text>
<text class="s-txt-m" x="30" y="244" text-anchor="end">−1</text>
<text class="s-txt-m" x="30" y="268" text-anchor="end">−2</text>
<line class="s-thin" x1="36" y1="366" x2="352" y2="366" stroke-dasharray="5 4"/>
<line class="s-thin" x1="36" y1="390" x2="352" y2="390" stroke-dasharray="5 4"/>
<line class="s-thin" x1="36" y1="414" x2="352" y2="414" stroke-dasharray="5 4"/>
<line class="s-thin" x1="36" y1="438" x2="352" y2="438" stroke-dasharray="5 4"/>
<polyline class="s-accent" points="46,414 76,438 106,414 136,438 166,414 196,390"/>
<polyline class="s-line" points="196,390 226,366 256,342 286,366 316,342 346,318"/>
<circle class="s-node" cx="46" cy="414" r="3.4"/>
<circle class="s-node" cx="76" cy="438" r="3.4"/>
<circle class="s-node" cx="106" cy="414" r="3.4"/>
<circle class="s-node" cx="136" cy="438" r="3.4"/>
<circle class="s-node" cx="166" cy="414" r="3.4"/>
<circle class="s-node" cx="226" cy="366" r="3.4"/>
<circle class="s-node" cx="256" cy="342" r="3.4"/>
<circle class="s-node" cx="286" cy="366" r="3.4"/>
<circle class="s-node" cx="316" cy="342" r="3.4"/>
<circle class="s-node" cx="346" cy="318" r="3.4"/>
<circle class="s-node-a" cx="46" cy="414" r="4.2"/>
<circle class="s-node-r" cx="196" cy="390" r="4.2"/>
<text class="s-txt-m" x="30" y="370" text-anchor="end">0</text>
<text class="s-txt-m" x="30" y="394" text-anchor="end">−1</text>
<text class="s-txt-m" x="30" y="418" text-anchor="end">−2</text>
</svg>
<figcaption>Левый кусок переворачивают относительно уровня −1, правый оставляют как есть. Обратная операция ровно та же, поэтому соответствие взаимно однозначно.</figcaption>
</figure>

## Телескоп и ответ

> поле:mn **Раскладка.** Мало текста, выкладка крупно; анимация сокращения снизу.

Уцелевшие раскладываем по тому, где они кончились, и суммируем

$$\sum_h A_h=\sum_j\Bigl[\binom Lj-\binom L{j+1}\Bigr]$$

Соседние члены гасят друг друга. **Остаётся один**

$$\binom L{\lceil L/2\rceil}\ \xrightarrow{\ L=2n\ }\ \binom{2n}n$$

$$\mathbb{P}=\binom{2n}n\Big/4^n$$

То самое число в середине строки, оно же сумма квадратов. **Вопрос с первой минуты закрыт**

<figure>
<svg viewBox="0 0 380 118" width="620" role="img" aria-label="Цепочка разностей: соседние члены попарно связаны дугами и перечёркнуты, остаётся только крайний левый член, отмеченный залитым узлом">
<line class="s-line" x1="46" y1="70" x2="78" y2="70"/>
<line class="s-line" x1="130" y1="70" x2="162" y2="70"/>
<line class="s-line" x1="214" y1="70" x2="246" y2="70"/>
<line class="s-line" x1="298" y1="70" x2="330" y2="70"/>
<path class="s-thin" d="M78,62 C 86,38 122,38 130,62"/>
<path class="s-thin" d="M162,62 C 170,38 206,38 214,62"/>
<path class="s-thin" d="M246,62 C 254,38 290,38 298,62"/>
<circle class="s-node-r" cx="46" cy="70" r="4.2"/>
<text class="s-txt-m" x="46" y="92" text-anchor="middle">1</text>
<circle class="s-node" cx="78" cy="70" r="3.4"/>
<text class="s-txt-m" x="78" y="92" text-anchor="middle">2</text>
<circle class="s-node" cx="130" cy="70" r="3.4"/>
<text class="s-txt-m" x="130" y="92" text-anchor="middle">2</text>
<circle class="s-node" cx="162" cy="70" r="3.4"/>
<text class="s-txt-m" x="162" y="92" text-anchor="middle">3</text>
<circle class="s-node" cx="214" cy="70" r="3.4"/>
<text class="s-txt-m" x="214" y="92" text-anchor="middle">3</text>
<circle class="s-node" cx="246" cy="70" r="3.4"/>
<text class="s-txt-m" x="246" y="92" text-anchor="middle">4</text>
<circle class="s-node" cx="298" cy="70" r="3.4"/>
<text class="s-txt-m" x="298" y="92" text-anchor="middle">4</text>
<circle class="s-node" cx="330" cy="70" r="3.4"/>
<text class="s-txt-m" x="330" y="92" text-anchor="middle">5</text>
<line class="s-accent" x1="70.5" y1="77.5" x2="85.5" y2="62.5"/>
<line class="s-accent" x1="122.5" y1="77.5" x2="137.5" y2="62.5"/>
<line class="s-accent" x1="154.5" y1="77.5" x2="169.5" y2="62.5"/>
<line class="s-accent" x1="206.5" y1="77.5" x2="221.5" y2="62.5"/>
<line class="s-accent" x1="238.5" y1="77.5" x2="253.5" y2="62.5"/>
<line class="s-accent" x1="290.5" y1="77.5" x2="305.5" y2="62.5"/>
<line class="s-accent" x1="322.5" y1="77.5" x2="337.5" y2="62.5"/>
</svg>
<figcaption>Каждый член гасит соседа — от всей длинной суммы остаётся один первый.</figcaption>
</figure>

<figure>
<svg viewBox="0 0 356 146" width="560" role="img" aria-label="Траектория, которая ни разу не опускается до горизонтали обрыва: ломаная идёт над сплошной чертой, старт отмечен залитым узлом">
<line class="s-line" x1="20" y1="122" x2="336" y2="122"/>
<polyline class="s-line" points="34,98 66,74 98,98 130,74 162,50 194,74 226,50 258,74 290,50 322,26"/>
<circle class="s-node" cx="66" cy="74" r="3.4"/>
<circle class="s-node" cx="98" cy="98" r="3.4"/>
<circle class="s-node" cx="130" cy="74" r="3.4"/>
<circle class="s-node" cx="162" cy="50" r="3.4"/>
<circle class="s-node" cx="194" cy="74" r="3.4"/>
<circle class="s-node" cx="226" cy="50" r="3.4"/>
<circle class="s-node" cx="258" cy="74" r="3.4"/>
<circle class="s-node" cx="290" cy="50" r="3.4"/>
<circle class="s-node" cx="322" cy="26" r="3.4"/>
<circle class="s-node-a" cx="34" cy="98" r="4.6"/>
</svg>
<figcaption>Тот самый кадр, с которого всё началось: путь, ни разу не задевший черту обрыва.</figcaption>
</figure>

## Что осталось

> поле:mn **Раскладка.** Картинка крупно, текста почти нет. Три хвоста уходят в листок: Серпинский, время ожидания «два орла подряд», общий Вандермонд.

<figure>
<svg viewBox="0 0 346 312" width="330" role="img" aria-label="Треугольник Паскаля на тридцать две строки: закрашены только клетки с нечётными числами, узор повторяет треугольник Серпинского">
<circle class="s-node-r" cx="173" cy="22" r="3.2"/> <circle class="s-node-r" cx="168" cy="30.7" r="3.2"/> <circle class="s-node-r" cx="178" cy="30.7" r="3.2"/> <circle class="s-node-r" cx="163" cy="39.3" r="3.2"/> <circle class="s-node-r" cx="183" cy="39.3" r="3.2"/> <circle class="s-node-r" cx="158" cy="48" r="3.2"/>
<circle class="s-node-r" cx="168" cy="48" r="3.2"/> <circle class="s-node-r" cx="178" cy="48" r="3.2"/> <circle class="s-node-r" cx="188" cy="48" r="3.2"/> <circle class="s-node-r" cx="153" cy="56.6" r="3.2"/> <circle class="s-node-r" cx="193" cy="56.6" r="3.2"/> <circle class="s-node-r" cx="148" cy="65.3" r="3.2"/>
<circle class="s-node-r" cx="158" cy="65.3" r="3.2"/> <circle class="s-node-r" cx="188" cy="65.3" r="3.2"/> <circle class="s-node-r" cx="198" cy="65.3" r="3.2"/> <circle class="s-node-r" cx="143" cy="74" r="3.2"/> <circle class="s-node-r" cx="163" cy="74" r="3.2"/> <circle class="s-node-r" cx="183" cy="74" r="3.2"/>
<circle class="s-node-r" cx="203" cy="74" r="3.2"/> <circle class="s-node-r" cx="138" cy="82.6" r="3.2"/> <circle class="s-node-r" cx="148" cy="82.6" r="3.2"/> <circle class="s-node-r" cx="158" cy="82.6" r="3.2"/> <circle class="s-node-r" cx="168" cy="82.6" r="3.2"/> <circle class="s-node-r" cx="178" cy="82.6" r="3.2"/>
<circle class="s-node-r" cx="188" cy="82.6" r="3.2"/> <circle class="s-node-r" cx="198" cy="82.6" r="3.2"/> <circle class="s-node-r" cx="208" cy="82.6" r="3.2"/> <circle class="s-node-r" cx="133" cy="91.3" r="3.2"/> <circle class="s-node-r" cx="213" cy="91.3" r="3.2"/> <circle class="s-node-r" cx="128" cy="99.9" r="3.2"/>
<circle class="s-node-r" cx="138" cy="99.9" r="3.2"/> <circle class="s-node-r" cx="208" cy="99.9" r="3.2"/> <circle class="s-node-r" cx="218" cy="99.9" r="3.2"/> <circle class="s-node-r" cx="123" cy="108.6" r="3.2"/> <circle class="s-node-r" cx="143" cy="108.6" r="3.2"/> <circle class="s-node-r" cx="203" cy="108.6" r="3.2"/>
<circle class="s-node-r" cx="223" cy="108.6" r="3.2"/> <circle class="s-node-r" cx="118" cy="117.3" r="3.2"/> <circle class="s-node-r" cx="128" cy="117.3" r="3.2"/> <circle class="s-node-r" cx="138" cy="117.3" r="3.2"/> <circle class="s-node-r" cx="148" cy="117.3" r="3.2"/> <circle class="s-node-r" cx="198" cy="117.3" r="3.2"/>
<circle class="s-node-r" cx="208" cy="117.3" r="3.2"/> <circle class="s-node-r" cx="218" cy="117.3" r="3.2"/> <circle class="s-node-r" cx="228" cy="117.3" r="3.2"/> <circle class="s-node-r" cx="113" cy="125.9" r="3.2"/> <circle class="s-node-r" cx="153" cy="125.9" r="3.2"/> <circle class="s-node-r" cx="193" cy="125.9" r="3.2"/>
<circle class="s-node-r" cx="233" cy="125.9" r="3.2"/> <circle class="s-node-r" cx="108" cy="134.6" r="3.2"/> <circle class="s-node-r" cx="118" cy="134.6" r="3.2"/> <circle class="s-node-r" cx="148" cy="134.6" r="3.2"/> <circle class="s-node-r" cx="158" cy="134.6" r="3.2"/> <circle class="s-node-r" cx="188" cy="134.6" r="3.2"/>
<circle class="s-node-r" cx="198" cy="134.6" r="3.2"/> <circle class="s-node-r" cx="228" cy="134.6" r="3.2"/> <circle class="s-node-r" cx="238" cy="134.6" r="3.2"/> <circle class="s-node-r" cx="103" cy="143.2" r="3.2"/> <circle class="s-node-r" cx="123" cy="143.2" r="3.2"/> <circle class="s-node-r" cx="143" cy="143.2" r="3.2"/>
<circle class="s-node-r" cx="163" cy="143.2" r="3.2"/> <circle class="s-node-r" cx="183" cy="143.2" r="3.2"/> <circle class="s-node-r" cx="203" cy="143.2" r="3.2"/> <circle class="s-node-r" cx="223" cy="143.2" r="3.2"/> <circle class="s-node-r" cx="243" cy="143.2" r="3.2"/> <circle class="s-node-r" cx="98" cy="151.9" r="3.2"/>
<circle class="s-node-r" cx="108" cy="151.9" r="3.2"/> <circle class="s-node-r" cx="118" cy="151.9" r="3.2"/> <circle class="s-node-r" cx="128" cy="151.9" r="3.2"/> <circle class="s-node-r" cx="138" cy="151.9" r="3.2"/> <circle class="s-node-r" cx="148" cy="151.9" r="3.2"/> <circle class="s-node-r" cx="158" cy="151.9" r="3.2"/>
<circle class="s-node-r" cx="168" cy="151.9" r="3.2"/> <circle class="s-node-r" cx="178" cy="151.9" r="3.2"/> <circle class="s-node-r" cx="188" cy="151.9" r="3.2"/> <circle class="s-node-r" cx="198" cy="151.9" r="3.2"/> <circle class="s-node-r" cx="208" cy="151.9" r="3.2"/> <circle class="s-node-r" cx="218" cy="151.9" r="3.2"/>
<circle class="s-node-r" cx="228" cy="151.9" r="3.2"/> <circle class="s-node-r" cx="238" cy="151.9" r="3.2"/> <circle class="s-node-r" cx="248" cy="151.9" r="3.2"/> <circle class="s-node-r" cx="93" cy="160.6" r="3.2"/> <circle class="s-node-r" cx="253" cy="160.6" r="3.2"/> <circle class="s-node-r" cx="88" cy="169.2" r="3.2"/>
<circle class="s-node-r" cx="98" cy="169.2" r="3.2"/> <circle class="s-node-r" cx="248" cy="169.2" r="3.2"/> <circle class="s-node-r" cx="258" cy="169.2" r="3.2"/> <circle class="s-node-r" cx="83" cy="177.9" r="3.2"/> <circle class="s-node-r" cx="103" cy="177.9" r="3.2"/> <circle class="s-node-r" cx="243" cy="177.9" r="3.2"/>
<circle class="s-node-r" cx="263" cy="177.9" r="3.2"/> <circle class="s-node-r" cx="78" cy="186.5" r="3.2"/> <circle class="s-node-r" cx="88" cy="186.5" r="3.2"/> <circle class="s-node-r" cx="98" cy="186.5" r="3.2"/> <circle class="s-node-r" cx="108" cy="186.5" r="3.2"/> <circle class="s-node-r" cx="238" cy="186.5" r="3.2"/>
<circle class="s-node-r" cx="248" cy="186.5" r="3.2"/> <circle class="s-node-r" cx="258" cy="186.5" r="3.2"/> <circle class="s-node-r" cx="268" cy="186.5" r="3.2"/> <circle class="s-node-r" cx="73" cy="195.2" r="3.2"/> <circle class="s-node-r" cx="113" cy="195.2" r="3.2"/> <circle class="s-node-r" cx="233" cy="195.2" r="3.2"/>
<circle class="s-node-r" cx="273" cy="195.2" r="3.2"/> <circle class="s-node-r" cx="68" cy="203.9" r="3.2"/> <circle class="s-node-r" cx="78" cy="203.9" r="3.2"/> <circle class="s-node-r" cx="108" cy="203.9" r="3.2"/> <circle class="s-node-r" cx="118" cy="203.9" r="3.2"/> <circle class="s-node-r" cx="228" cy="203.9" r="3.2"/>
<circle class="s-node-r" cx="238" cy="203.9" r="3.2"/> <circle class="s-node-r" cx="268" cy="203.9" r="3.2"/> <circle class="s-node-r" cx="278" cy="203.9" r="3.2"/> <circle class="s-node-r" cx="63" cy="212.5" r="3.2"/> <circle class="s-node-r" cx="83" cy="212.5" r="3.2"/> <circle class="s-node-r" cx="103" cy="212.5" r="3.2"/>
<circle class="s-node-r" cx="123" cy="212.5" r="3.2"/> <circle class="s-node-r" cx="223" cy="212.5" r="3.2"/> <circle class="s-node-r" cx="243" cy="212.5" r="3.2"/> <circle class="s-node-r" cx="263" cy="212.5" r="3.2"/> <circle class="s-node-r" cx="283" cy="212.5" r="3.2"/> <circle class="s-node-r" cx="58" cy="221.2" r="3.2"/>
<circle class="s-node-r" cx="68" cy="221.2" r="3.2"/> <circle class="s-node-r" cx="78" cy="221.2" r="3.2"/> <circle class="s-node-r" cx="88" cy="221.2" r="3.2"/> <circle class="s-node-r" cx="98" cy="221.2" r="3.2"/> <circle class="s-node-r" cx="108" cy="221.2" r="3.2"/> <circle class="s-node-r" cx="118" cy="221.2" r="3.2"/>
<circle class="s-node-r" cx="128" cy="221.2" r="3.2"/> <circle class="s-node-r" cx="218" cy="221.2" r="3.2"/> <circle class="s-node-r" cx="228" cy="221.2" r="3.2"/> <circle class="s-node-r" cx="238" cy="221.2" r="3.2"/> <circle class="s-node-r" cx="248" cy="221.2" r="3.2"/> <circle class="s-node-r" cx="258" cy="221.2" r="3.2"/>
<circle class="s-node-r" cx="268" cy="221.2" r="3.2"/> <circle class="s-node-r" cx="278" cy="221.2" r="3.2"/> <circle class="s-node-r" cx="288" cy="221.2" r="3.2"/> <circle class="s-node-r" cx="53" cy="229.8" r="3.2"/> <circle class="s-node-r" cx="133" cy="229.8" r="3.2"/> <circle class="s-node-r" cx="213" cy="229.8" r="3.2"/>
<circle class="s-node-r" cx="293" cy="229.8" r="3.2"/> <circle class="s-node-r" cx="48" cy="238.5" r="3.2"/> <circle class="s-node-r" cx="58" cy="238.5" r="3.2"/> <circle class="s-node-r" cx="128" cy="238.5" r="3.2"/> <circle class="s-node-r" cx="138" cy="238.5" r="3.2"/> <circle class="s-node-r" cx="208" cy="238.5" r="3.2"/>
<circle class="s-node-r" cx="218" cy="238.5" r="3.2"/> <circle class="s-node-r" cx="288" cy="238.5" r="3.2"/> <circle class="s-node-r" cx="298" cy="238.5" r="3.2"/> <circle class="s-node-r" cx="43" cy="247.2" r="3.2"/> <circle class="s-node-r" cx="63" cy="247.2" r="3.2"/> <circle class="s-node-r" cx="123" cy="247.2" r="3.2"/>
<circle class="s-node-r" cx="143" cy="247.2" r="3.2"/> <circle class="s-node-r" cx="203" cy="247.2" r="3.2"/> <circle class="s-node-r" cx="223" cy="247.2" r="3.2"/> <circle class="s-node-r" cx="283" cy="247.2" r="3.2"/> <circle class="s-node-r" cx="303" cy="247.2" r="3.2"/> <circle class="s-node-r" cx="38" cy="255.8" r="3.2"/>
<circle class="s-node-r" cx="48" cy="255.8" r="3.2"/> <circle class="s-node-r" cx="58" cy="255.8" r="3.2"/> <circle class="s-node-r" cx="68" cy="255.8" r="3.2"/> <circle class="s-node-r" cx="118" cy="255.8" r="3.2"/> <circle class="s-node-r" cx="128" cy="255.8" r="3.2"/> <circle class="s-node-r" cx="138" cy="255.8" r="3.2"/>
<circle class="s-node-r" cx="148" cy="255.8" r="3.2"/> <circle class="s-node-r" cx="198" cy="255.8" r="3.2"/> <circle class="s-node-r" cx="208" cy="255.8" r="3.2"/> <circle class="s-node-r" cx="218" cy="255.8" r="3.2"/> <circle class="s-node-r" cx="228" cy="255.8" r="3.2"/> <circle class="s-node-r" cx="278" cy="255.8" r="3.2"/>
<circle class="s-node-r" cx="288" cy="255.8" r="3.2"/> <circle class="s-node-r" cx="298" cy="255.8" r="3.2"/> <circle class="s-node-r" cx="308" cy="255.8" r="3.2"/> <circle class="s-node-r" cx="33" cy="264.5" r="3.2"/> <circle class="s-node-r" cx="73" cy="264.5" r="3.2"/> <circle class="s-node-r" cx="113" cy="264.5" r="3.2"/>
<circle class="s-node-r" cx="153" cy="264.5" r="3.2"/> <circle class="s-node-r" cx="193" cy="264.5" r="3.2"/> <circle class="s-node-r" cx="233" cy="264.5" r="3.2"/> <circle class="s-node-r" cx="273" cy="264.5" r="3.2"/> <circle class="s-node-r" cx="313" cy="264.5" r="3.2"/> <circle class="s-node-r" cx="28" cy="273.1" r="3.2"/>
<circle class="s-node-r" cx="38" cy="273.1" r="3.2"/> <circle class="s-node-r" cx="68" cy="273.1" r="3.2"/> <circle class="s-node-r" cx="78" cy="273.1" r="3.2"/> <circle class="s-node-r" cx="108" cy="273.1" r="3.2"/> <circle class="s-node-r" cx="118" cy="273.1" r="3.2"/> <circle class="s-node-r" cx="148" cy="273.1" r="3.2"/>
<circle class="s-node-r" cx="158" cy="273.1" r="3.2"/> <circle class="s-node-r" cx="188" cy="273.1" r="3.2"/> <circle class="s-node-r" cx="198" cy="273.1" r="3.2"/> <circle class="s-node-r" cx="228" cy="273.1" r="3.2"/> <circle class="s-node-r" cx="238" cy="273.1" r="3.2"/> <circle class="s-node-r" cx="268" cy="273.1" r="3.2"/>
<circle class="s-node-r" cx="278" cy="273.1" r="3.2"/> <circle class="s-node-r" cx="308" cy="273.1" r="3.2"/> <circle class="s-node-r" cx="318" cy="273.1" r="3.2"/> <circle class="s-node-r" cx="23" cy="281.8" r="3.2"/> <circle class="s-node-r" cx="43" cy="281.8" r="3.2"/> <circle class="s-node-r" cx="63" cy="281.8" r="3.2"/>
<circle class="s-node-r" cx="83" cy="281.8" r="3.2"/> <circle class="s-node-r" cx="103" cy="281.8" r="3.2"/> <circle class="s-node-r" cx="123" cy="281.8" r="3.2"/> <circle class="s-node-r" cx="143" cy="281.8" r="3.2"/> <circle class="s-node-r" cx="163" cy="281.8" r="3.2"/> <circle class="s-node-r" cx="183" cy="281.8" r="3.2"/>
<circle class="s-node-r" cx="203" cy="281.8" r="3.2"/> <circle class="s-node-r" cx="223" cy="281.8" r="3.2"/> <circle class="s-node-r" cx="243" cy="281.8" r="3.2"/> <circle class="s-node-r" cx="263" cy="281.8" r="3.2"/> <circle class="s-node-r" cx="283" cy="281.8" r="3.2"/> <circle class="s-node-r" cx="303" cy="281.8" r="3.2"/>
<circle class="s-node-r" cx="323" cy="281.8" r="3.2"/> <circle class="s-node-r" cx="18" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="28" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="38" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="48" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="58" cy="290.5" r="3.2"/>
<circle class="s-node-r" cx="68" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="78" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="88" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="98" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="108" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="118" cy="290.5" r="3.2"/>
<circle class="s-node-r" cx="128" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="138" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="148" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="158" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="168" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="178" cy="290.5" r="3.2"/>
<circle class="s-node-r" cx="188" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="198" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="208" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="218" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="228" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="238" cy="290.5" r="3.2"/>
<circle class="s-node-r" cx="248" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="258" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="268" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="278" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="288" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="298" cy="290.5" r="3.2"/>
<circle class="s-node-r" cx="308" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="318" cy="290.5" r="3.2"/> <circle class="s-node-r" cx="328" cy="290.5" r="3.2"/>
</svg>
<figcaption>Закрасим нечётные числа треугольника Паскаля — проступает треугольник Серпинского.</figcaption>
</figure>

Курс «Перечислительная комбинаторика» — ЛШП NlogN, август
