---
tab: Математика
status: chernovik
poryadok: 1
registr: читаемый
---

# Внутри треугольника Паскаля

## Вопрос

> поле:mn **Что это.** Связное изложение всего материала. Одна линия: **треугольник Паскаля — это перепись траекторий случайного блуждания**, и потому один вопрос «сколько траекторий?» отвечает и на арифметические, и на вероятностные вопросы. Финал — ответ на вопрос, поставленный в первой части. Доказательства свёрнуты под кат; в правом жёлобе — что тривиально, что нет, и куда смотреть дальше.

### Частица, монета и три облика траектории

Частица стоит в нуле числовой прямой. Каждую секунду бросаем монету: орёл — шаг вправо, решка — шаг влево. Всё изложение про этот единственный объект.

Последовательность бросков задаёт **траекторию** $S_0 = 0,\ S_1,\ \dots,\ S_n$, где $S_k$ — положение после $k$-го шага. Её удобно рисовать ломаной: по горизонтали время, по вертикали положение.

<figure>
<svg viewBox="0 0 366 192" width="430" role="img" aria-label="Траектория частицы за восемь шагов: ломаная поднимается на орле и опускается на решке">
<line class="s-thin" x1="28" y1="118" x2="348" y2="118" stroke-dasharray="5 4"/>
<polyline class="s-accent" points="44,118 80,92 116,66 152,92 188,66 224,92 260,118 296,144 332,118"/>
<circle class="s-node-a" cx="44" cy="118" r="3.4"/>
<circle class="s-node" cx="80" cy="92" r="3.4"/>
<circle class="s-node" cx="116" cy="66" r="3.4"/>
<circle class="s-node" cx="152" cy="92" r="3.4"/>
<circle class="s-node" cx="188" cy="66" r="3.4"/>
<circle class="s-node" cx="224" cy="92" r="3.4"/>
<circle class="s-node" cx="260" cy="118" r="3.4"/>
<circle class="s-node" cx="296" cy="144" r="3.4"/>
<circle class="s-node-a" cx="332" cy="118" r="3.4"/>
<text class="s-txt-m" x="62" y="81" text-anchor="middle">О</text>
<text class="s-txt-m" x="98" y="55" text-anchor="middle">О</text>
<text class="s-txt-m" x="134" y="55" text-anchor="middle">Р</text>
<text class="s-txt-m" x="170" y="55" text-anchor="middle">О</text>
<text class="s-txt-m" x="206" y="55" text-anchor="middle">Р</text>
<text class="s-txt-m" x="242" y="81" text-anchor="middle">Р</text>
<text class="s-txt-m" x="278" y="107" text-anchor="middle">Р</text>
<text class="s-txt-m" x="314" y="107" text-anchor="middle">О</text>
<text class="s-txt-m" x="44" y="182" text-anchor="middle">0</text>
<text class="s-txt-m" x="116" y="182" text-anchor="middle">2</text>
<text class="s-txt-m" x="188" y="182" text-anchor="middle">4</text>
<text class="s-txt-m" x="260" y="182" text-anchor="middle">6</text>
<text class="s-txt-m" x="332" y="182" text-anchor="middle">8</text>
<text class="s-txt-m" x="16" y="123" text-anchor="middle">0</text>
</svg>
<figcaption>Траектория за восемь бросков ОООРОРРРО.</figcaption>
</figure>

> поле:mn **Три слова, которые дальше не смешиваем.** **Траектория** — сама ломаная. **Положение** $S_n$ — одно число, её конец. **Маршрут** — та же траектория, нарисованная по клеткам. Ломаная показывает то, что таблица прячет: касания нуля, рекорды высоты, симметрию оси. Весь финал — про её геометрию, поэтому заводим сразу.

Траекторий длины $n$ ровно $2^n$, и все они равновероятны. Это единственное вероятностное предположение во всём тексте: дальше «вероятность события» всегда значит «доля траекторий, на которых оно произошло». Поэтому любой вероятностный вопрос — это вопрос **сколько траекторий**.

У одной траектории три облика, и мы будем свободно переходить между ними.

- **Ломаная** — график движения, как на рисунке.
- **Подмножество** — траектория задана тем, на каких местах стояли орлы; значит траектории длины $n$ это ровно подмножества множества $\{1, \dots, n\}$.
- **Маршрут по клеткам** — пусть орёл будет шагом вправо, а решка вверх; тогда траектория превращается в кратчайший маршрут из левого нижнего угла в правый верхний.

<figure class="mn">
<svg viewBox="0 0 194 172" width="250" role="img" aria-label="Та же траектория как кратчайший маршрут по клеткам: вправо на орле, вверх на решке">
<line class="s-thin" x1="44" y1="26" x2="164" y2="26"/>
<line class="s-thin" x1="44" y1="56" x2="164" y2="56"/>
<line class="s-thin" x1="44" y1="86" x2="164" y2="86"/>
<line class="s-thin" x1="44" y1="116" x2="164" y2="116"/>
<line class="s-thin" x1="44" y1="146" x2="164" y2="146"/>
<line class="s-thin" x1="44" y1="26" x2="44" y2="146"/>
<line class="s-thin" x1="74" y1="26" x2="74" y2="146"/>
<line class="s-thin" x1="104" y1="26" x2="104" y2="146"/>
<line class="s-thin" x1="134" y1="26" x2="134" y2="146"/>
<line class="s-thin" x1="164" y1="26" x2="164" y2="146"/>
<polyline class="s-accent" points="44,146 74,146 104,146 104,116 134,116 134,86 134,56 134,26 164,26"/>
<circle class="s-node-a" cx="44" cy="146" r="3.4"/>
<circle class="s-node-a" cx="164" cy="26" r="3.4"/>
<text class="s-txt-m" x="28" y="151" text-anchor="middle">0</text>
</svg>
<figcaption>Та же последовательность ОООРОРРРО как маршрут: орёл — вправо, решка — вверх.</figcaption>
</figure>

### Два вопроса, с которых всё начинается

Теперь два вопроса. Первый — лёгкий:

> **Где окажется частица через $n$ шагов?**

Второй — та гора, к которой мы идём весь текст:

> **Сколько траекторий длины $2n$ ни разу не возвращаются в ноль?**

Первый вопрос закроется в следующей части. Второй так, в лоб, не считается: правила «сколько траекторий не задели ноль» через соседей не выпишешь. Чтобы к нему подойти, придётся научиться **перекладывать траектории** — и вся середина текста об этом.

### Перепись: треугольник Паскаля

Обозначим через $N_n(x)$ число траекторий длины $n$, заканчивающихся в точке $x$.

**Утверждение 1.**
$$N_n(x) = N_{n-1}(x-1) + N_{n-1}(x+1).$$

*Доказательство.* Смотрим на последний шаг. В точку $x$ приходят либо из $x-1$ шагом вправо, либо из $x+1$ шагом влево. Два этих набора траекторий не пересекаются и вместе дают все. ∎

Выпишем числа $N_n(x)$ строка за строкой: в нулевой строке одна единица, каждое следующее число — сумма двух соседей сверху.

<figure class="mn">
<svg viewBox="0 0 362 272" width="420" role="img" aria-label="Строки треугольника Паскаля как числа маршрутов; две стрелки показывают правило сложения">
<text class="s-txt" x="181" y="35" text-anchor="middle">1</text>
<text class="s-txt" x="158" y="77" text-anchor="middle">1</text>
<text class="s-txt" x="204" y="77" text-anchor="middle">1</text>
<text class="s-txt" x="135" y="119" text-anchor="middle">1</text>
<text class="s-txt" x="181" y="119" text-anchor="middle">2</text>
<text class="s-txt" x="227" y="119" text-anchor="middle">1</text>
<text class="s-txt" x="112" y="161" text-anchor="middle">1</text>
<text class="s-txt" x="158" y="161" text-anchor="middle">3</text>
<text class="s-txt" x="204" y="161" text-anchor="middle">3</text>
<text class="s-txt" x="250" y="161" text-anchor="middle">1</text>
<text class="s-txt" x="89" y="203" text-anchor="middle">1</text>
<text class="s-txt" x="135" y="203" text-anchor="middle">4</text>
<text class="s-txt" x="181" y="203" text-anchor="middle">6</text>
<text class="s-txt" x="227" y="203" text-anchor="middle">4</text>
<text class="s-txt" x="273" y="203" text-anchor="middle">1</text>
<text class="s-txt" x="66" y="245" text-anchor="middle">1</text>
<text class="s-txt" x="112" y="245" text-anchor="middle">5</text>
<text class="s-txt" x="158" y="245" text-anchor="middle">10</text>
<text class="s-txt" x="204" y="245" text-anchor="middle">10</text>
<text class="s-txt" x="250" y="245" text-anchor="middle">5</text>
<text class="s-txt" x="296" y="245" text-anchor="middle">1</text>
<line class="s-dash" x1="165" y1="165" x2="168.528" y2="177.346"/><path class="s-ar-a" d="M 171,186 L 172.374,176.247 L 164.681,178.445 Z"/>
<line class="s-dash" x1="197" y1="165" x2="193.472" y2="177.346"/><path class="s-ar-a" d="M 191,186 L 197.319,178.445 L 189.626,176.247 Z"/>
<text class="s-txt-m" x="6" y="35" text-anchor="start">n = 0</text>
<text class="s-txt-m" x="6" y="77" text-anchor="start">n = 1</text>
<text class="s-txt-m" x="6" y="119" text-anchor="start">n = 2</text>
<text class="s-txt-m" x="6" y="161" text-anchor="start">n = 3</text>
<text class="s-txt-m" x="6" y="203" text-anchor="start">n = 4</text>
<text class="s-txt-m" x="6" y="245" text-anchor="start">n = 5</text>
</svg>
<figcaption>Первые шесть строк. Стрелки показывают, откуда взялась шестёрка.</figcaption>
</figure>

Треугольник Паскаля мы не вспомнили, а построили: это таблица числа траекторий.

**Утверждение 2.**
Если за $n$ шагов выпало $k$ орлов, частица оказалась в точке $2k-n$, и таких траекторий ровно $\binom{n}{k}$.

*Доказательство.* Траектория задана множеством позиций орлов; чтобы попасть в $2k-n$, орлов нужно ровно $k$. Число $k$-элементных подмножеств $n$-элементного множества и есть $\binom{n}{k}$. ∎

Первый вопрос закрыт: по утверждению 2 вероятность оказаться в точке $2k-n$ равна $\binom{n}{k}/2^n$.

### Что видно в одной строке

> поле:mn **Куда это ведёт.** Симметрия понадобится в части про склейку (там она превращает Вандермонда в сумму квадратов), а трюк «перевернуть монету» — прямой предок отражения в линии рекордов из финала.

Три факта, и все три доказываются одинаково — **предъявлением биекции**, а не подсчётом суммы. Этот приём будет работать до самого конца.

**Утверждение 3.**
Строка симметрична, сумма её равна $2^n$, а чётное число орлов выпадает ровно с вероятностью $\tfrac12$:
$$\binom{n}{k} = \binom{n}{n-k},\qquad \sum_k \binom{n}{k} = 2^n,\qquad \sum_k (-1)^k\binom{n}{k} = 0.$$

*Доказательство — три переворота монеты.* **Симметрия.** Перевернём все монеты: орлы станут решками. Это биекция между траекториями с $k$ орлами и траекториями с $n-k$ орлами.
**Сумма строки.** Слева пересчитаны все траектории длины $n$, разбитые по числу орлов; справа те же траектории пересчитаны напрямую. Одно множество, два счёта.
**Чётность.** Перевернём *первую* монету. Число орлов меняется ровно на единицу, значит это биекция между траекториями с чётным и с нечётным числом орлов. ∎

<figure>
<svg viewBox="0 0 384 108" width="380" role="img" aria-label="Шестая строка треугольника симметрична относительно вертикальной оси">
<rect class="s-line" x="24" y="26" width="40" height="40"/>
<text class="s-txt" x="44" y="52" text-anchor="middle">1</text>
<rect class="s-line" x="74" y="26" width="40" height="40"/>
<text class="s-txt" x="94" y="52" text-anchor="middle">6</text>
<rect class="s-line" x="124" y="26" width="40" height="40"/>
<text class="s-txt" x="144" y="52" text-anchor="middle">15</text>
<rect class="s-line" x="174" y="26" width="40" height="40"/>
<text class="s-txt" x="194" y="52" text-anchor="middle">20</text>
<rect class="s-line" x="224" y="26" width="40" height="40"/>
<text class="s-txt" x="244" y="52" text-anchor="middle">15</text>
<rect class="s-line" x="274" y="26" width="40" height="40"/>
<text class="s-txt" x="294" y="52" text-anchor="middle">6</text>
<rect class="s-line" x="324" y="26" width="40" height="40"/>
<text class="s-txt" x="344" y="52" text-anchor="middle">1</text>
<line class="s-thin" x1="194" y1="10" x2="194" y2="96" stroke-dasharray="5 4"/>
</svg>
<figcaption>Шестая строка: замена орлов на решки отражает её относительно вертикальной оси.</figcaption>
</figure>

Теперь инструмент, который дальше понадобится дважды — и его тоже не надо доказывать формулой.

**Утверждение 4.**
$$(k+1)\binom{n}{k+1} = (n-k)\binom{n}{k},\qquad\text{то есть}\qquad \frac{\binom{n}{k+1}}{\binom{n}{k}} = \frac{n-k}{k+1}.$$

*Доказательство — счёт двумя способами.* Считаем пары «$(k+1)$-элементное подмножество и отмеченный элемент внутри него».
**Слева:** сначала выбираем подмножество ($\binom{n}{k+1}$ способов), потом отмечаем в нём один элемент ($k+1$ способ).
**Справа:** сначала выбираем $k$ элементов, которые останутся неотмеченными ($\binom{n}{k}$ способов), потом добавляем отмеченный — любой из оставшихся $n-k$.
Одно и то же множество пар, посчитанное двумя способами. ∎

> поле:mn Формула через факториалы дала бы то же самое, но она **выводится** из этого тождества, а не наоборот. Двойной счёт здесь первичен.

Отсюда сразу: числа строки растут, пока $n-k \gt k+1$, и убывают после. Максимум стоит в середине. Этот максимум — **центральный биномиальный коэффициент** $\binom{2n}{n}$ — окажется ответом на все главные вопросы текста.

### Первая работа для нового инструмента

**Задача 1.**
Найдите в треугольнике три подряд идущих числа одной строки, которые относятся как $1 : 2 : 3$.

Задача честно решается за две минуты, и ответ во всём бесконечном треугольнике **один**: строка $14$, числа $1001,\ 2002,\ 3003$.

*Решение.* Пусть это $\binom{n}{k}, \binom{n}{k+1}, \binom{n}{k+2}$. По утверждению 4 условия дают $\dfrac{n-k}{k+1} = 2$ и $\dfrac{n-k-1}{k+2} = \dfrac{3}{2}$.
Из первого $n = 3k+2$; подставляя во второе, получаем $\dfrac{2k+1}{k+2} = \dfrac32$, то есть $4k+2 = 3k+6$, откуда $k = 4$ и $n = 14$. Система линейная, решение единственно. ∎

**Замечание 1.**
Тот же инструмент отвечает и на более общий вопрос: три подряд идущих числа строки $n$ образуют арифметическую прогрессию тогда и только тогда, когда $n+2$ — точный квадрат. Условие $\binom{n}{k} + \binom{n}{k+2} = 2\binom{n}{k+1}$ превращается в квадратное уравнение на $k$ с дискриминантом $n+2$.

> поле:mn Проверено перебором до $n = 700$: подходят ровно $n = 7, 14, 23, 34, 47, \dots$, то есть все $n = m^2-2$; прогрессий из **четырёх** подряд идущих чисел не бывает никогда.

## Запреты: Фибоначчи и время ожидания

Пока мы считали траектории по их концу. Спросим иначе: запретим **образец** и посчитаем, сколько траекторий уцелело.

### Запрет образца: числа Фибоначчи

> **Сколько последовательностей длины $n$ не содержат двух орлов подряд?**

**Утверждение 5.**
Их ровно $F_{n+2}$, где $F_1 = F_2 = 1$ — числа Фибоначчи.

*Доказательство — разбор первого шага.* Пусть таких последовательностей $a_n$. Если первый бросок решка, дальше идёт любая хорошая последовательность длины $n-1$. Если орёл — второй бросок обязан быть решкой, а дальше любая хорошая длины $n-2$. Значит $a_n = a_{n-1} + a_{n-2}$, причём $a_1 = 2$, $a_2 = 3$. ∎

> поле:mn **Что здесь нетривиально.** Не сама рекуррента — она такая же лёгкая, как у Паскаля. Нетривиально то, что запрет образца даёт ДРУГОЕ правило сложения, а значит другую таблицу: одно и то же множество траекторий режется по-новому.

Приём тот же, что в утверждении 1, — разбор по одному шагу, — но правило сложения получилось **другое**, и потому таблица другая. Где же тут треугольник Паскаля? Разобьём хорошие последовательности по числу орлов.

**Утверждение 6.**
Числа Фибоначчи — это суммы по восходящим диагоналям треугольника Паскаля:
$$F_{n+2} = \sum_{k} \binom{n-k+1}{k}.$$

*Доказательство — биекция «вставить решки».* Возьмём хорошую последовательность с $k$ орлами. Выкинем по одной решке сразу после каждого орла, кроме случая, когда орёл стоит последним. Останется слово длины $n-k$ из $k$ орлов и $n-2k$ решок — без всяких ограничений.
Обратно: по любому такому слову решки вставляются однозначно. Значит хороших последовательностей с $k$ орлами ровно $\binom{n-k+1}{k}$ — столько, сколько способов расставить $k$ орлов среди $n-k+1$ мест. Суммируя по $k$, получаем то же множество, посчитанное вторым способом. ∎

<figure class="mn">
<svg viewBox="0 0 380 360" width="370" role="img" aria-label="Суммы по восходящим диагоналям треугольника Паскаля дают числа Фибоначчи">
<text class="s-txt-m" x="30" y="31" text-anchor="middle">1</text>
<text class="s-txt-m" x="30" y="69" text-anchor="middle">1</text>
<text class="s-txt-m" x="80" y="69" text-anchor="middle">1</text>
<text class="s-txt-m" x="30" y="107" text-anchor="middle">1</text>
<text class="s-txt-m" x="80" y="107" text-anchor="middle">2</text>
<text class="s-txt-m" x="130" y="107" text-anchor="middle">1</text>
<text class="s-txt-m" x="30" y="145" text-anchor="middle">1</text>
<text class="s-txt-m" x="80" y="145" text-anchor="middle">3</text>
<text class="s-txt-m" x="130" y="145" text-anchor="middle">3</text>
<text class="s-txt-m" x="180" y="145" text-anchor="middle">1</text>
<text class="s-txt-m" x="30" y="183" text-anchor="middle">1</text>
<text class="s-txt-m" x="80" y="183" text-anchor="middle">4</text>
<text class="s-txt-m" x="130" y="183" text-anchor="middle">6</text>
<text class="s-txt-m" x="180" y="183" text-anchor="middle">4</text>
<text class="s-txt-m" x="230" y="183" text-anchor="middle">1</text>
<text class="s-txt-m" x="30" y="221" text-anchor="middle">1</text>
<text class="s-txt-m" x="80" y="221" text-anchor="middle">5</text>
<text class="s-txt-m" x="130" y="221" text-anchor="middle">10</text>
<text class="s-txt-m" x="180" y="221" text-anchor="middle">10</text>
<text class="s-txt-m" x="230" y="221" text-anchor="middle">5</text>
<text class="s-txt-m" x="280" y="221" text-anchor="middle">1</text>
<text class="s-txt-m" x="30" y="259" text-anchor="middle">1</text>
<text class="s-txt-m" x="80" y="259" text-anchor="middle">6</text>
<text class="s-txt-m" x="130" y="259" text-anchor="middle">15</text>
<text class="s-txt-m" x="180" y="259" text-anchor="middle">20</text>
<text class="s-txt-m" x="230" y="259" text-anchor="middle">15</text>
<text class="s-txt-m" x="280" y="259" text-anchor="middle">6</text>
<text class="s-txt-m" x="322" y="259" text-anchor="start">…</text>
<text class="s-txt-m" x="30" y="297" text-anchor="middle">1</text>
<text class="s-txt-m" x="80" y="297" text-anchor="middle">7</text>
<text class="s-txt-m" x="130" y="297" text-anchor="middle">21</text>
<text class="s-txt-m" x="180" y="297" text-anchor="middle">35</text>
<text class="s-txt-m" x="230" y="297" text-anchor="middle">35</text>
<text class="s-txt-m" x="280" y="297" text-anchor="middle">21</text>
<text class="s-txt-m" x="322" y="297" text-anchor="start">…</text>
<text class="s-txt-m" x="30" y="335" text-anchor="middle">1</text>
<text class="s-txt-m" x="80" y="335" text-anchor="middle">8</text>
<text class="s-txt-m" x="130" y="335" text-anchor="middle">28</text>
<text class="s-txt-m" x="180" y="335" text-anchor="middle">56</text>
<text class="s-txt-m" x="230" y="335" text-anchor="middle">70</text>
<text class="s-txt-m" x="280" y="335" text-anchor="middle">56</text>
<text class="s-txt-m" x="322" y="335" text-anchor="start">…</text>
<polyline class="s-dash" points="53,93 103,55"/>
<polyline class="s-dash" points="53,131 103,93"/>
<polyline class="s-dash" points="53,169 103,131 153,93"/>
<polyline class="s-dash" points="53,207 103,169 153,131"/>
<polyline class="s-dash" points="53,245 103,207 153,169 203,131"/>
<polyline class="s-dash" points="53,283 103,245 153,207 203,169"/>
<polyline class="s-dash" points="53,321 103,283 153,245 203,207 253,169"/>
</svg>
<figcaption>Суммы по восходящим диагоналям: 1, 2, 3, 5, 8, 13, 21.</figcaption>
</figure>

### Как долго ждать

Из этого счёта немедленно вырастает вопрос, ответ на который ломает интуицию, — и попутно даёт технику, без которой не обойдётся финал.

> **Ждём «два орла подряд». Потом ждём «орёл, а сразу за ним решка». Обе комбинации имеют вероятность $\tfrac14$ на каждом месте. Одинаково ли долго ждать?**

**Утверждение 7.**
Комбинации «ОО» ждать в среднем $6$ бросков, комбинации «ОР» — $4$.

*Доказательство — сумма по хвостам.* Для целой неотрицательной величины $T$ верно $\mathbb{E}[T] = \sum_{n \geq 0} \mathbb{P}(T \gt n)$: считаем не исходы, а шаги — каждый шаг вносит единицу во все исходы, которые до него дожили.
Событие «$T \gt n$» значит, что в первых $n$ бросках комбинация не встретилась. Для «ОО» таких последовательностей $F_{n+2}$ по утверждению 5, и при $x = \tfrac12$ сумма $\sum_m F_m x^m = \dfrac{x}{1-x-x^2}$ равна $2$, откуда
$$\mathbb{E}[T_{\text{ОО}}] = \sum_{n\geq 0} \frac{F_{n+2}}{2^n} = 4\left(2 - \tfrac12\right) = 6 .$$
Последовательностей без «ОР» ровно $n+1$: такая обязана иметь вид «сначала решки, потом орлы», её задаёт положение границы. Значит $\mathbb{E}[T_{\text{ОР}}] = \sum_{n \geq 0} (n+1)/2^n = 4$. ∎

Причина — **самоперекрытие**. Ждёте «ОО», после орла выпала решка — вы отброшены в начало. Ждёте «ОР», после орла выпал орёл — вы всё ещё на середине пути. Равновероятные на фиксированном месте, комбинации не равноправны как цели.

> поле:mn Проверено точной арифметикой по автомату Кнута — Морриса — Пратта: «ООО» ждать $14$, «ОРО» — $10$, «ООР», «ОРР», «РОО» — по $8$.

> поле:insight Приём, который вернётся в финале | Сумма по хвостам $\mathbb{E}[T] = \sum \mathbb{P}(T \gt n)$ переводит вопрос «сколько ждать» в вопрос «сколько траекторий дожили». Ровно этим же ходом в последней части выясняется, сколько ждать возвращения домой — и там сумма разойдётся.

## Многочлен как машина: чётность и Серпинский

### Строка целиком: многочлен $(1+x)^n$

До сих пор строка треугольника была списком чисел. Сложим её в один объект:

$$(1+x)^n = \sum_k \binom{n}{k}\, x^k .$$

Это не формула, а **упаковка**: многочлен несёт всю строку сразу, а умножение на $(1+x)$ — это ещё один шаг блуждания. Посмотрим, что машина умеет, если её включить по модулю два.

По модулю $2$ верно $(1+x)^2 \equiv 1 + x^2$: средний член $2x$ исчезает. Возводя в квадрат дальше, получаем $(1+x)^{2^j} \equiv 1 + x^{2^j}$ — многочлен из двух членов, как бы велика ни была степень.

> поле:mn **Почему именно многочлены.** Правило сложения работает по одному шагу, а тут нужен ответ сразу про всю строку и про все степени двойки. Многочлен — единственная упаковка в этом тексте, которая позволяет возвести строку в квадрат одним движением.

**Утверждение 8 (Люка при $p=2$).**
$\binom{n}{k}$ нечётно тогда и только тогда, когда каждая двоичная единица числа $k$ стоит на месте единицы числа $n$.

*Доказательство.* Разложим $n$ по двоичным разрядам: $n = \sum_j n_j 2^j$. Тогда по модулю $2$
$$(1+x)^n \equiv \prod_{j:\, n_j = 1} \left(1 + x^{2^j}\right).$$
Раскрывая скобки, видим: каждый одночлен собирается выбором подмножества сомножителей, и разные подмножества дают разные степени. Значит коэффициент при $x^k$ нечётен ровно тогда, когда $k$ собирается из тех же степеней двойки, то есть когда единицы $k$ сидят внутри единиц $n$. ∎

### Та же задача про монеты

Условие «единицы $k$ внутри единиц $n$» звучит сухо. Переведём его на язык, где оно станет задачей про монеты. Положим $a = k$, $b = n-k$; тогда условие равносильно тому, что при сложении $a$ и $b$ столбиком в двоичной записи **нигде не возникает переноса**.

> **Мы играем $m$ раундов, в каждом каждый бросает свою монету. Если в каком-то раунде у обоих орёл — проиграли. Какова вероятность выиграть?**

Ответ получается в строку: раунды независимы, в каждом три исхода из четырёх нас устраивают, значит $(3/4)^m$. Но интересно не число, а **какие партии выжили**. Нарисуем пару $(a, b)$ точкой квадрата $2^m \times 2^m$ и будем решать задачу **сверху, со старшего разряда**.

Четыре равновероятных случая старшего разряда — это четыре четверти квадрата. Случай «у обоих орёл» — мгновенный проигрыш, значит одна четверть пуста. В каждой из трёх оставшихся стоит дословно та же задача на $m-1$ разряде — та же картинка вдвое меньше.

<figure>
<svg viewBox="0 0 636 306" width="520" role="img" aria-label="Пары чисел, складывающихся без переноса: одна четверть квадрата пуста, три остальные повторяют картинку вдвое меньше">
<rect class="s-fillsh" x="26" y="146" width="60" height="60"/>
<rect class="s-fillsh" x="26" y="206" width="60" height="60"/>
<rect class="s-fillsh" x="86" y="146" width="60" height="60"/>
<rect class="s-thin" x="26" y="146" width="120" height="120"/>
<line class="s-dash" x1="86" y1="146" x2="86" y2="266"/>
<line class="s-dash" x1="26" y1="206" x2="146" y2="206"/>
<text class="s-txt-m" x="86" y="290" text-anchor="middle">m = 1</text>
<rect class="s-fillsh" x="198" y="146" width="30" height="30"/>
<rect class="s-fillsh" x="198" y="176" width="30" height="30"/>
<rect class="s-fillsh" x="198" y="206" width="30" height="30"/>
<rect class="s-fillsh" x="198" y="236" width="30" height="30"/>
<rect class="s-fillsh" x="228" y="146" width="30" height="30"/>
<rect class="s-fillsh" x="228" y="206" width="30" height="30"/>
<rect class="s-fillsh" x="258" y="146" width="30" height="30"/>
<rect class="s-fillsh" x="258" y="176" width="30" height="30"/>
<rect class="s-fillsh" x="288" y="146" width="30" height="30"/>
<rect class="s-thin" x="198" y="146" width="120" height="120"/>
<line class="s-dash" x1="258" y1="146" x2="258" y2="266"/>
<line class="s-dash" x1="198" y1="206" x2="318" y2="206"/>
<text class="s-txt-m" x="258" y="290" text-anchor="middle">m = 2</text>
<rect class="s-fillsh" x="370" y="26" width="15" height="15"/>
<rect class="s-fillsh" x="370" y="41" width="15" height="15"/>
<rect class="s-fillsh" x="370" y="56" width="15" height="15"/>
<rect class="s-fillsh" x="370" y="71" width="15" height="15"/>
<rect class="s-fillsh" x="370" y="86" width="15" height="15"/>
<rect class="s-fillsh" x="370" y="101" width="15" height="15"/>
<rect class="s-fillsh" x="370" y="116" width="15" height="15"/>
<rect class="s-fillsh" x="370" y="131" width="15" height="15"/>
<rect class="s-fillsh" x="370" y="146" width="15" height="15"/>
<rect class="s-fillsh" x="370" y="161" width="15" height="15"/>
<rect class="s-fillsh" x="370" y="176" width="15" height="15"/>
<rect class="s-fillsh" x="370" y="191" width="15" height="15"/>
<rect class="s-fillsh" x="370" y="206" width="15" height="15"/>
<rect class="s-fillsh" x="370" y="221" width="15" height="15"/>
<rect class="s-fillsh" x="370" y="236" width="15" height="15"/>
<rect class="s-fillsh" x="370" y="251" width="15" height="15"/>
<rect class="s-fillsh" x="385" y="26" width="15" height="15"/>
<rect class="s-fillsh" x="385" y="56" width="15" height="15"/>
<rect class="s-fillsh" x="385" y="86" width="15" height="15"/>
<rect class="s-fillsh" x="385" y="116" width="15" height="15"/>
<rect class="s-fillsh" x="385" y="146" width="15" height="15"/>
<rect class="s-fillsh" x="385" y="176" width="15" height="15"/>
<rect class="s-fillsh" x="385" y="206" width="15" height="15"/>
<rect class="s-fillsh" x="385" y="236" width="15" height="15"/>
<rect class="s-fillsh" x="400" y="26" width="15" height="15"/>
<rect class="s-fillsh" x="400" y="41" width="15" height="15"/>
<rect class="s-fillsh" x="400" y="86" width="15" height="15"/>
<rect class="s-fillsh" x="400" y="101" width="15" height="15"/>
<rect class="s-fillsh" x="400" y="146" width="15" height="15"/>
<rect class="s-fillsh" x="400" y="161" width="15" height="15"/>
<rect class="s-fillsh" x="400" y="206" width="15" height="15"/>
<rect class="s-fillsh" x="400" y="221" width="15" height="15"/>
<rect class="s-fillsh" x="415" y="26" width="15" height="15"/>
<rect class="s-fillsh" x="415" y="86" width="15" height="15"/>
<rect class="s-fillsh" x="415" y="146" width="15" height="15"/>
<rect class="s-fillsh" x="415" y="206" width="15" height="15"/>
<rect class="s-fillsh" x="430" y="26" width="15" height="15"/>
<rect class="s-fillsh" x="430" y="41" width="15" height="15"/>
<rect class="s-fillsh" x="430" y="56" width="15" height="15"/>
<rect class="s-fillsh" x="430" y="71" width="15" height="15"/>
<rect class="s-fillsh" x="430" y="146" width="15" height="15"/>
<rect class="s-fillsh" x="430" y="161" width="15" height="15"/>
<rect class="s-fillsh" x="430" y="176" width="15" height="15"/>
<rect class="s-fillsh" x="430" y="191" width="15" height="15"/>
<rect class="s-fillsh" x="445" y="26" width="15" height="15"/>
<rect class="s-fillsh" x="445" y="56" width="15" height="15"/>
<rect class="s-fillsh" x="445" y="146" width="15" height="15"/>
<rect class="s-fillsh" x="445" y="176" width="15" height="15"/>
<rect class="s-fillsh" x="460" y="26" width="15" height="15"/>
<rect class="s-fillsh" x="460" y="41" width="15" height="15"/>
<rect class="s-fillsh" x="460" y="146" width="15" height="15"/>
<rect class="s-fillsh" x="460" y="161" width="15" height="15"/>
<rect class="s-fillsh" x="475" y="26" width="15" height="15"/>
<rect class="s-fillsh" x="475" y="146" width="15" height="15"/>
<rect class="s-fillsh" x="490" y="26" width="15" height="15"/>
<rect class="s-fillsh" x="490" y="41" width="15" height="15"/>
<rect class="s-fillsh" x="490" y="56" width="15" height="15"/>
<rect class="s-fillsh" x="490" y="71" width="15" height="15"/>
<rect class="s-fillsh" x="490" y="86" width="15" height="15"/>
<rect class="s-fillsh" x="490" y="101" width="15" height="15"/>
<rect class="s-fillsh" x="490" y="116" width="15" height="15"/>
<rect class="s-fillsh" x="490" y="131" width="15" height="15"/>
<rect class="s-fillsh" x="505" y="26" width="15" height="15"/>
<rect class="s-fillsh" x="505" y="56" width="15" height="15"/>
<rect class="s-fillsh" x="505" y="86" width="15" height="15"/>
<rect class="s-fillsh" x="505" y="116" width="15" height="15"/>
<rect class="s-fillsh" x="520" y="26" width="15" height="15"/>
<rect class="s-fillsh" x="520" y="41" width="15" height="15"/>
<rect class="s-fillsh" x="520" y="86" width="15" height="15"/>
<rect class="s-fillsh" x="520" y="101" width="15" height="15"/>
<rect class="s-fillsh" x="535" y="26" width="15" height="15"/>
<rect class="s-fillsh" x="535" y="86" width="15" height="15"/>
<rect class="s-fillsh" x="550" y="26" width="15" height="15"/>
<rect class="s-fillsh" x="550" y="41" width="15" height="15"/>
<rect class="s-fillsh" x="550" y="56" width="15" height="15"/>
<rect class="s-fillsh" x="550" y="71" width="15" height="15"/>
<rect class="s-fillsh" x="565" y="26" width="15" height="15"/>
<rect class="s-fillsh" x="565" y="56" width="15" height="15"/>
<rect class="s-fillsh" x="580" y="26" width="15" height="15"/>
<rect class="s-fillsh" x="580" y="41" width="15" height="15"/>
<rect class="s-fillsh" x="595" y="26" width="15" height="15"/>
<rect class="s-thin" x="370" y="26" width="240" height="240"/>
<line class="s-dash" x1="490" y1="26" x2="490" y2="266"/>
<line class="s-dash" x1="370" y1="146" x2="610" y2="146"/>
<text class="s-txt-m" x="490" y="290" text-anchor="middle">m = 4</text>
</svg>
<figcaption>Пары, складывающиеся без переноса, при m = 1, 2, 4. Одна четверть пуста, три остальные — уменьшенные копии всей картинки.</figcaption>
</figure>

### Откуда берётся самоподобие

«Выбросить четверть и повторить в трёх оставшихся» — это построение треугольника Серпинского. Мы его не рисовали заранее: он получился как ответ на вопрос про монеты.

> поле:insight Откуда взялось самоподобие | Не из ответа, а из **способа решения**. Первый вопрос решения — «что в старшем разряде?» — и есть деление квадрата на четверти. Фрактал не подгоняется под картинку, он выпадает из рекурсии.

А $\binom{a+b}{a}$ у нас уже есть: по утверждению 2 это **число маршрутов в клетку $(a,b)$**. Значит нарисованное множество — карта клеток с нечётным числом маршрутов, а по диагоналям $a+b=n$ читаются строки треугольника по модулю два.

<figure class="mn">
<svg viewBox="0 0 392 382" width="400" role="img" aria-label="Нечётные числа первых тридцати двух строк треугольника Паскаля образуют треугольник Серпинского">
<rect class="s-fillsh" x="190.5" y="16" width="11" height="11"/>
<rect class="s-fillsh" x="185" y="27" width="11" height="11"/>
<rect class="s-fillsh" x="196" y="27" width="11" height="11"/>
<rect class="s-fillsh" x="179.5" y="38" width="11" height="11"/>
<rect class="s-fillsh" x="201.5" y="38" width="11" height="11"/>
<rect class="s-fillsh" x="174" y="49" width="11" height="11"/>
<rect class="s-fillsh" x="185" y="49" width="11" height="11"/>
<rect class="s-fillsh" x="196" y="49" width="11" height="11"/>
<rect class="s-fillsh" x="207" y="49" width="11" height="11"/>
<rect class="s-fillsh" x="168.5" y="60" width="11" height="11"/>
<rect class="s-fillsh" x="212.5" y="60" width="11" height="11"/>
<rect class="s-fillsh" x="163" y="71" width="11" height="11"/>
<rect class="s-fillsh" x="174" y="71" width="11" height="11"/>
<rect class="s-fillsh" x="207" y="71" width="11" height="11"/>
<rect class="s-fillsh" x="218" y="71" width="11" height="11"/>
<rect class="s-fillsh" x="157.5" y="82" width="11" height="11"/>
<rect class="s-fillsh" x="179.5" y="82" width="11" height="11"/>
<rect class="s-fillsh" x="201.5" y="82" width="11" height="11"/>
<rect class="s-fillsh" x="223.5" y="82" width="11" height="11"/>
<rect class="s-fillsh" x="152" y="93" width="11" height="11"/>
<rect class="s-fillsh" x="163" y="93" width="11" height="11"/>
<rect class="s-fillsh" x="174" y="93" width="11" height="11"/>
<rect class="s-fillsh" x="185" y="93" width="11" height="11"/>
<rect class="s-fillsh" x="196" y="93" width="11" height="11"/>
<rect class="s-fillsh" x="207" y="93" width="11" height="11"/>
<rect class="s-fillsh" x="218" y="93" width="11" height="11"/>
<rect class="s-fillsh" x="229" y="93" width="11" height="11"/>
<rect class="s-fillsh" x="146.5" y="104" width="11" height="11"/>
<rect class="s-fillsh" x="234.5" y="104" width="11" height="11"/>
<rect class="s-fillsh" x="141" y="115" width="11" height="11"/>
<rect class="s-fillsh" x="152" y="115" width="11" height="11"/>
<rect class="s-fillsh" x="229" y="115" width="11" height="11"/>
<rect class="s-fillsh" x="240" y="115" width="11" height="11"/>
<rect class="s-fillsh" x="135.5" y="126" width="11" height="11"/>
<rect class="s-fillsh" x="157.5" y="126" width="11" height="11"/>
<rect class="s-fillsh" x="223.5" y="126" width="11" height="11"/>
<rect class="s-fillsh" x="245.5" y="126" width="11" height="11"/>
<rect class="s-fillsh" x="130" y="137" width="11" height="11"/>
<rect class="s-fillsh" x="141" y="137" width="11" height="11"/>
<rect class="s-fillsh" x="152" y="137" width="11" height="11"/>
<rect class="s-fillsh" x="163" y="137" width="11" height="11"/>
<rect class="s-fillsh" x="218" y="137" width="11" height="11"/>
<rect class="s-fillsh" x="229" y="137" width="11" height="11"/>
<rect class="s-fillsh" x="240" y="137" width="11" height="11"/>
<rect class="s-fillsh" x="251" y="137" width="11" height="11"/>
<rect class="s-fillsh" x="124.5" y="148" width="11" height="11"/>
<rect class="s-fillsh" x="168.5" y="148" width="11" height="11"/>
<rect class="s-fillsh" x="212.5" y="148" width="11" height="11"/>
<rect class="s-fillsh" x="256.5" y="148" width="11" height="11"/>
<rect class="s-fillsh" x="119" y="159" width="11" height="11"/>
<rect class="s-fillsh" x="130" y="159" width="11" height="11"/>
<rect class="s-fillsh" x="163" y="159" width="11" height="11"/>
<rect class="s-fillsh" x="174" y="159" width="11" height="11"/>
<rect class="s-fillsh" x="207" y="159" width="11" height="11"/>
<rect class="s-fillsh" x="218" y="159" width="11" height="11"/>
<rect class="s-fillsh" x="251" y="159" width="11" height="11"/>
<rect class="s-fillsh" x="262" y="159" width="11" height="11"/>
<rect class="s-fillsh" x="113.5" y="170" width="11" height="11"/>
<rect class="s-fillsh" x="135.5" y="170" width="11" height="11"/>
<rect class="s-fillsh" x="157.5" y="170" width="11" height="11"/>
<rect class="s-fillsh" x="179.5" y="170" width="11" height="11"/>
<rect class="s-fillsh" x="201.5" y="170" width="11" height="11"/>
<rect class="s-fillsh" x="223.5" y="170" width="11" height="11"/>
<rect class="s-fillsh" x="245.5" y="170" width="11" height="11"/>
<rect class="s-fillsh" x="267.5" y="170" width="11" height="11"/>
<rect class="s-fillsh" x="108" y="181" width="11" height="11"/>
<rect class="s-fillsh" x="119" y="181" width="11" height="11"/>
<rect class="s-fillsh" x="130" y="181" width="11" height="11"/>
<rect class="s-fillsh" x="141" y="181" width="11" height="11"/>
<rect class="s-fillsh" x="152" y="181" width="11" height="11"/>
<rect class="s-fillsh" x="163" y="181" width="11" height="11"/>
<rect class="s-fillsh" x="174" y="181" width="11" height="11"/>
<rect class="s-fillsh" x="185" y="181" width="11" height="11"/>
<rect class="s-fillsh" x="196" y="181" width="11" height="11"/>
<rect class="s-fillsh" x="207" y="181" width="11" height="11"/>
<rect class="s-fillsh" x="218" y="181" width="11" height="11"/>
<rect class="s-fillsh" x="229" y="181" width="11" height="11"/>
<rect class="s-fillsh" x="240" y="181" width="11" height="11"/>
<rect class="s-fillsh" x="251" y="181" width="11" height="11"/>
<rect class="s-fillsh" x="262" y="181" width="11" height="11"/>
<rect class="s-fillsh" x="273" y="181" width="11" height="11"/>
<rect class="s-fillsh" x="102.5" y="192" width="11" height="11"/>
<rect class="s-fillsh" x="278.5" y="192" width="11" height="11"/>
<rect class="s-fillsh" x="97" y="203" width="11" height="11"/>
<rect class="s-fillsh" x="108" y="203" width="11" height="11"/>
<rect class="s-fillsh" x="273" y="203" width="11" height="11"/>
<rect class="s-fillsh" x="284" y="203" width="11" height="11"/>
<rect class="s-fillsh" x="91.5" y="214" width="11" height="11"/>
<rect class="s-fillsh" x="113.5" y="214" width="11" height="11"/>
<rect class="s-fillsh" x="267.5" y="214" width="11" height="11"/>
<rect class="s-fillsh" x="289.5" y="214" width="11" height="11"/>
<rect class="s-fillsh" x="86" y="225" width="11" height="11"/>
<rect class="s-fillsh" x="97" y="225" width="11" height="11"/>
<rect class="s-fillsh" x="108" y="225" width="11" height="11"/>
<rect class="s-fillsh" x="119" y="225" width="11" height="11"/>
<rect class="s-fillsh" x="262" y="225" width="11" height="11"/>
<rect class="s-fillsh" x="273" y="225" width="11" height="11"/>
<rect class="s-fillsh" x="284" y="225" width="11" height="11"/>
<rect class="s-fillsh" x="295" y="225" width="11" height="11"/>
<rect class="s-fillsh" x="80.5" y="236" width="11" height="11"/>
<rect class="s-fillsh" x="124.5" y="236" width="11" height="11"/>
<rect class="s-fillsh" x="256.5" y="236" width="11" height="11"/>
<rect class="s-fillsh" x="300.5" y="236" width="11" height="11"/>
<rect class="s-fillsh" x="75" y="247" width="11" height="11"/>
<rect class="s-fillsh" x="86" y="247" width="11" height="11"/>
<rect class="s-fillsh" x="119" y="247" width="11" height="11"/>
<rect class="s-fillsh" x="130" y="247" width="11" height="11"/>
<rect class="s-fillsh" x="251" y="247" width="11" height="11"/>
<rect class="s-fillsh" x="262" y="247" width="11" height="11"/>
<rect class="s-fillsh" x="295" y="247" width="11" height="11"/>
<rect class="s-fillsh" x="306" y="247" width="11" height="11"/>
<rect class="s-fillsh" x="69.5" y="258" width="11" height="11"/>
<rect class="s-fillsh" x="91.5" y="258" width="11" height="11"/>
<rect class="s-fillsh" x="113.5" y="258" width="11" height="11"/>
<rect class="s-fillsh" x="135.5" y="258" width="11" height="11"/>
<rect class="s-fillsh" x="245.5" y="258" width="11" height="11"/>
<rect class="s-fillsh" x="267.5" y="258" width="11" height="11"/>
<rect class="s-fillsh" x="289.5" y="258" width="11" height="11"/>
<rect class="s-fillsh" x="311.5" y="258" width="11" height="11"/>
<rect class="s-fillsh" x="64" y="269" width="11" height="11"/>
<rect class="s-fillsh" x="75" y="269" width="11" height="11"/>
<rect class="s-fillsh" x="86" y="269" width="11" height="11"/>
<rect class="s-fillsh" x="97" y="269" width="11" height="11"/>
<rect class="s-fillsh" x="108" y="269" width="11" height="11"/>
<rect class="s-fillsh" x="119" y="269" width="11" height="11"/>
<rect class="s-fillsh" x="130" y="269" width="11" height="11"/>
<rect class="s-fillsh" x="141" y="269" width="11" height="11"/>
<rect class="s-fillsh" x="240" y="269" width="11" height="11"/>
<rect class="s-fillsh" x="251" y="269" width="11" height="11"/>
<rect class="s-fillsh" x="262" y="269" width="11" height="11"/>
<rect class="s-fillsh" x="273" y="269" width="11" height="11"/>
<rect class="s-fillsh" x="284" y="269" width="11" height="11"/>
<rect class="s-fillsh" x="295" y="269" width="11" height="11"/>
<rect class="s-fillsh" x="306" y="269" width="11" height="11"/>
<rect class="s-fillsh" x="317" y="269" width="11" height="11"/>
<rect class="s-fillsh" x="58.5" y="280" width="11" height="11"/>
<rect class="s-fillsh" x="146.5" y="280" width="11" height="11"/>
<rect class="s-fillsh" x="234.5" y="280" width="11" height="11"/>
<rect class="s-fillsh" x="322.5" y="280" width="11" height="11"/>
<rect class="s-fillsh" x="53" y="291" width="11" height="11"/>
<rect class="s-fillsh" x="64" y="291" width="11" height="11"/>
<rect class="s-fillsh" x="141" y="291" width="11" height="11"/>
<rect class="s-fillsh" x="152" y="291" width="11" height="11"/>
<rect class="s-fillsh" x="229" y="291" width="11" height="11"/>
<rect class="s-fillsh" x="240" y="291" width="11" height="11"/>
<rect class="s-fillsh" x="317" y="291" width="11" height="11"/>
<rect class="s-fillsh" x="328" y="291" width="11" height="11"/>
<rect class="s-fillsh" x="47.5" y="302" width="11" height="11"/>
<rect class="s-fillsh" x="69.5" y="302" width="11" height="11"/>
<rect class="s-fillsh" x="135.5" y="302" width="11" height="11"/>
<rect class="s-fillsh" x="157.5" y="302" width="11" height="11"/>
<rect class="s-fillsh" x="223.5" y="302" width="11" height="11"/>
<rect class="s-fillsh" x="245.5" y="302" width="11" height="11"/>
<rect class="s-fillsh" x="311.5" y="302" width="11" height="11"/>
<rect class="s-fillsh" x="333.5" y="302" width="11" height="11"/>
<rect class="s-fillsh" x="42" y="313" width="11" height="11"/>
<rect class="s-fillsh" x="53" y="313" width="11" height="11"/>
<rect class="s-fillsh" x="64" y="313" width="11" height="11"/>
<rect class="s-fillsh" x="75" y="313" width="11" height="11"/>
<rect class="s-fillsh" x="130" y="313" width="11" height="11"/>
<rect class="s-fillsh" x="141" y="313" width="11" height="11"/>
<rect class="s-fillsh" x="152" y="313" width="11" height="11"/>
<rect class="s-fillsh" x="163" y="313" width="11" height="11"/>
<rect class="s-fillsh" x="218" y="313" width="11" height="11"/>
<rect class="s-fillsh" x="229" y="313" width="11" height="11"/>
<rect class="s-fillsh" x="240" y="313" width="11" height="11"/>
<rect class="s-fillsh" x="251" y="313" width="11" height="11"/>
<rect class="s-fillsh" x="306" y="313" width="11" height="11"/>
<rect class="s-fillsh" x="317" y="313" width="11" height="11"/>
<rect class="s-fillsh" x="328" y="313" width="11" height="11"/>
<rect class="s-fillsh" x="339" y="313" width="11" height="11"/>
<rect class="s-fillsh" x="36.5" y="324" width="11" height="11"/>
<rect class="s-fillsh" x="80.5" y="324" width="11" height="11"/>
<rect class="s-fillsh" x="124.5" y="324" width="11" height="11"/>
<rect class="s-fillsh" x="168.5" y="324" width="11" height="11"/>
<rect class="s-fillsh" x="212.5" y="324" width="11" height="11"/>
<rect class="s-fillsh" x="256.5" y="324" width="11" height="11"/>
<rect class="s-fillsh" x="300.5" y="324" width="11" height="11"/>
<rect class="s-fillsh" x="344.5" y="324" width="11" height="11"/>
<rect class="s-fillsh" x="31" y="335" width="11" height="11"/>
<rect class="s-fillsh" x="42" y="335" width="11" height="11"/>
<rect class="s-fillsh" x="75" y="335" width="11" height="11"/>
<rect class="s-fillsh" x="86" y="335" width="11" height="11"/>
<rect class="s-fillsh" x="119" y="335" width="11" height="11"/>
<rect class="s-fillsh" x="130" y="335" width="11" height="11"/>
<rect class="s-fillsh" x="163" y="335" width="11" height="11"/>
<rect class="s-fillsh" x="174" y="335" width="11" height="11"/>
<rect class="s-fillsh" x="207" y="335" width="11" height="11"/>
<rect class="s-fillsh" x="218" y="335" width="11" height="11"/>
<rect class="s-fillsh" x="251" y="335" width="11" height="11"/>
<rect class="s-fillsh" x="262" y="335" width="11" height="11"/>
<rect class="s-fillsh" x="295" y="335" width="11" height="11"/>
<rect class="s-fillsh" x="306" y="335" width="11" height="11"/>
<rect class="s-fillsh" x="339" y="335" width="11" height="11"/>
<rect class="s-fillsh" x="350" y="335" width="11" height="11"/>
<rect class="s-fillsh" x="25.5" y="346" width="11" height="11"/>
<rect class="s-fillsh" x="47.5" y="346" width="11" height="11"/>
<rect class="s-fillsh" x="69.5" y="346" width="11" height="11"/>
<rect class="s-fillsh" x="91.5" y="346" width="11" height="11"/>
<rect class="s-fillsh" x="113.5" y="346" width="11" height="11"/>
<rect class="s-fillsh" x="135.5" y="346" width="11" height="11"/>
<rect class="s-fillsh" x="157.5" y="346" width="11" height="11"/>
<rect class="s-fillsh" x="179.5" y="346" width="11" height="11"/>
<rect class="s-fillsh" x="201.5" y="346" width="11" height="11"/>
<rect class="s-fillsh" x="223.5" y="346" width="11" height="11"/>
<rect class="s-fillsh" x="245.5" y="346" width="11" height="11"/>
<rect class="s-fillsh" x="267.5" y="346" width="11" height="11"/>
<rect class="s-fillsh" x="289.5" y="346" width="11" height="11"/>
<rect class="s-fillsh" x="311.5" y="346" width="11" height="11"/>
<rect class="s-fillsh" x="333.5" y="346" width="11" height="11"/>
<rect class="s-fillsh" x="355.5" y="346" width="11" height="11"/>
<rect class="s-fillsh" x="20" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="31" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="42" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="53" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="64" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="75" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="86" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="97" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="108" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="119" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="130" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="141" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="152" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="163" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="174" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="185" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="196" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="207" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="218" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="229" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="240" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="251" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="262" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="273" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="284" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="295" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="306" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="317" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="328" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="339" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="350" y="357" width="11" height="11"/>
<rect class="s-fillsh" x="361" y="357" width="11" height="11"/>
</svg>
<figcaption>Нечётные числа первых тридцати двух строк треугольника Паскаля.</figcaption>
</figure>

> поле:mn Что надо сказать честно. Число $(3/4)^m$ берётся по независимости в одну строку — содержание не в числе, а во множестве, поэтому такт «а какие пары выжили?» с рисованием обязателен. Условие раскладывается по разрядам именно потому, что «переносов нет вообще» поразрядно; у вопроса «ровно один перенос» такой структуры нет.

### Картинка превращается в числа

Тот же счёт переносов даёт и арифметику.

**Утверждение 9 (Куммер).**
Наибольшая степень двойки, на которую делится $\binom{2n}{n}$, равна числу единиц в двоичной записи $n$.

*Доказательство.* Показатель двойки в $n!$ равен $n - s(n)$, где $s(n)$ — число двоичных единиц: сумма $\lfloor n/2\rfloor + \lfloor n/4\rfloor + \dots$ телескопируется. Тогда
$$v_2\!\left(\binom{2n}{n}\right) = \bigl(2n - s(2n)\bigr) - 2\bigl(n - s(n)\bigr) = 2s(n) - s(2n),$$
а $s(2n) = s(n)$, потому что сдвиг влево не меняет числа единиц. ∎

**Пример 2.**
$\binom{200}{100}$ — число из 59 цифр. Сто в двоичной записи это $1100100$, три единицы; значит оно делится на $8$ и не делится на $16$.

Отсюда же — сколько в строке нечётных чисел: ровно $2^{s(n)}$. В строке никогда не бывает ровно трёх нечётных, только степень двойки; в тысячной строке их $64$; строка нечётна целиком тогда и только тогда, когда $n = 2^j-1$.

**Замечание 2.**
Среди первых $2^m$ строк нечётных ровно $3^m$, а клеток около $4^m/2$. Значит **почти все числа треугольника чётны**: при восьми тысячах строк доля нечётных уже $4{,}75\,\%$. Показатель роста $\log_2 3 \approx 1{,}585$ — это в точности фрактальная размерность треугольника Серпинского. Арифметика и геометрия дали одно число.

> поле:mn Если запускать выбор разрядов по одному бесконечно, получится случайный процесс, рисующий ту же картинку прыжками к трём углам, — игра в хаос Барнсли. Как визуальный финал блока годится; самостоятельной задачи на счёт из неё не выходит.

## Склейка: Вандермонд и встреча двух прогулок

### Разрез пополам: тождество Вандермонда

Многочлен несёт строку; умножение двух многочленов должно нести что-то про две строки сразу. Что именно?

$$(1+x)^m (1+x)^n = (1+x)^{m+n}.$$

Слева траектория разрезана после $m$-го шага и склеена из двух независимых кусков. Справа — она же целиком. Сравним коэффициенты.

<figure>
<svg viewBox="0 0 398 182" width="420" role="img" aria-label="Блуждание разрезано после m шагов: положение в конце — сумма двух независимых кусков">
<line class="s-thin" x1="30" y1="110" x2="378" y2="110" stroke-dasharray="5 4"/>
<polyline class="s-accent" points="44,110 76,88 108,66 140,88 172,66"/>
<polyline class="s-line" points="172,66 204,88 236,66 268,44 300,66 332,88 364,66"/>
<line class="s-dash" x1="172" y1="14" x2="172" y2="150"/>
<circle class="s-node" cx="44" cy="110" r="3.4"/>
<circle class="s-node" cx="76" cy="88" r="3.4"/>
<circle class="s-node" cx="108" cy="66" r="3.4"/>
<circle class="s-node" cx="140" cy="88" r="3.4"/>
<circle class="s-node-r" cx="172" cy="66" r="3.4"/>
<circle class="s-node" cx="204" cy="88" r="3.4"/>
<circle class="s-node" cx="236" cy="66" r="3.4"/>
<circle class="s-node" cx="268" cy="44" r="3.4"/>
<circle class="s-node" cx="300" cy="66" r="3.4"/>
<circle class="s-node" cx="332" cy="88" r="3.4"/>
<circle class="s-node" cx="364" cy="66" r="3.4"/>
<text class="s-txt" x="172" y="168" text-anchor="middle">m</text>
<text class="s-txt-m" x="44" y="168" text-anchor="middle">0</text>
<text class="s-txt-m" x="364" y="168" text-anchor="middle">m+n</text>
</svg>
<figcaption>Траектория разрезана после m шагов: её конец — сумма двух независимых кусков.</figcaption>
</figure>

**Утверждение 10 (Вандермонд).**
$$\binom{m+n}{r} = \sum_{i} \binom{m}{i}\binom{n}{r-i}$$

*Доказательство — счёт двумя способами.* Слева: число способов выбрать $r$ орлов среди $m+n$ бросков. Справа: разобьём броски на первые $m$ и последние $n$; если в первой части орлов ровно $i$, то во второй их $r-i$. Суммируя по $i$, пересчитываем то же множество вторым способом. ∎

> поле:mn Умножение многочленов — это склейка двух блужданий подряд. Дальше вся работа идёт с одним частным случаем, но он окажется главным.

> поле:mn **Тривиально и нетривиально.** Сам Вандермонд тривиален — это разбиение по числу орлов в первой половине. Нетривиально следствие: сумма КВАДРАТОВ строки оказывается одним числом из середины следующей чётной строки, и это то самое число, которым закончится текст.

### Сумма квадратов: встреча двух прогулок

Возьмём $m = n$ и $r = n$. Вместе с симметрией из утверждения 3 это даёт

$$\sum_k \binom{n}{k}^{2} = \binom{2n}{n}.$$

Слева стоит сумма квадратов строки. У неё есть прямой смысл.

> **Двое выходят из одной точки и независимо гуляют по $n$ шагов. С какой вероятностью они встретятся?**

<figure>
<svg viewBox="0 0 314 158" width="330" role="img" aria-label="Две независимые прогулки по шесть шагов, вышедшие из нуля и пришедшие в одну точку">
<line class="s-thin" x1="32" y1="96" x2="290" y2="96" stroke-dasharray="5 4"/>
<polyline class="s-accent" points="46,96 84,70 122,44 160,70 198,44 236,70 274,44"/>
<polyline class="s-line" points="46,96 84,122 122,96 160,70 198,44 236,70 274,44"/>
<circle class="s-node" cx="46" cy="96" r="3.4"/>
<circle class="s-node" cx="84" cy="70" r="3.4"/>
<circle class="s-node" cx="122" cy="44" r="3.4"/>
<circle class="s-node" cx="160" cy="70" r="3.4"/>
<circle class="s-node" cx="198" cy="44" r="3.4"/>
<circle class="s-node" cx="236" cy="70" r="3.4"/>
<circle class="s-node" cx="274" cy="44" r="3.4"/>
<circle class="s-node" cx="46" cy="96" r="3.4"/>
<circle class="s-node" cx="84" cy="122" r="3.4"/>
<circle class="s-node" cx="122" cy="96" r="3.4"/>
<circle class="s-node" cx="160" cy="70" r="3.4"/>
<circle class="s-node" cx="198" cy="44" r="3.4"/>
<circle class="s-node" cx="236" cy="70" r="3.4"/>
<circle class="s-node" cx="274" cy="44" r="3.4"/>
<circle class="s-node-r" cx="274" cy="44" r="4.6"/>
<circle class="s-node-r" cx="46" cy="96" r="4.6"/>
</svg>
<figcaption>Две независимые прогулки по шесть шагов, пришедшие в одну точку.</figcaption>
</figure>

**Утверждение 11.**
Пар траекторий длины $n$ с общим концом ровно $\binom{2n}{n}$. Столько же есть траекторий длины $2n$, заканчивающихся в нуле.

*Доказательство.* **Пары.** Пара с общим концом — это выбор точки $x$ и двух траекторий в неё, то есть $\sum_x N_n(x)^2 = \sum_k \binom{n}{k}^2$, а это $\binom{2n}{n}$ по следствию из утверждения 10.
**Возврат в ноль.** По утверждению 2 чтобы за $2n$ шагов оказаться в нуле, нужно ровно $n$ орлов из $2n$. ∎

Два разных вопроса дали одно число — значит между их объектами есть биекция. Она устроена так, что её стоит увидеть отдельно: она понадобится через страницу.

> поле:insight Смотри на разрыв | Пусть двое ходят **по очереди**: сначала первый, потом второй, потом снова первый. Следим за разрывом «насколько первый впереди второго». Каждый полуход меняет разрыв ровно на $\pm 1$ — двинулся-то только один. А «встретились» значит «разрыв вернулся в ноль». Одна и та же последовательность бросков, посмотренная под другим углом: пара прогулок стала одной траекторией, вернувшейся домой.

<figure>
<svg viewBox="0 0 396 160" width="400" role="img" aria-label="Разрыв между двумя гуляющими, ходящими по очереди: он возвращается в ноль ровно тогда, когда они встретились">
<line class="s-thin" x1="30" y1="92" x2="372" y2="92" stroke-dasharray="5 4"/>
<polyline class="s-accent" points="44,92 70,70 96,48 122,26 148,48 174,70 200,92 226,70 252,92 278,114 304,92 330,70 356,92"/>
<circle class="s-node-r" cx="44" cy="92" r="3.4"/>
<circle class="s-node" cx="70" cy="70" r="3.4"/>
<circle class="s-node" cx="96" cy="48" r="3.4"/>
<circle class="s-node" cx="122" cy="26" r="3.4"/>
<circle class="s-node" cx="148" cy="48" r="3.4"/>
<circle class="s-node" cx="174" cy="70" r="3.4"/>
<circle class="s-node" cx="200" cy="92" r="3.4"/>
<circle class="s-node" cx="226" cy="70" r="3.4"/>
<circle class="s-node" cx="252" cy="92" r="3.4"/>
<circle class="s-node" cx="278" cy="114" r="3.4"/>
<circle class="s-node" cx="304" cy="92" r="3.4"/>
<circle class="s-node" cx="330" cy="70" r="3.4"/>
<circle class="s-node-r" cx="356" cy="92" r="3.4"/>
<text class="s-txt-m" x="57" y="144" text-anchor="middle">1</text>
<text class="s-txt-m" x="83" y="144" text-anchor="middle">2</text>
<text class="s-txt-m" x="109" y="144" text-anchor="middle">1</text>
<text class="s-txt-m" x="135" y="144" text-anchor="middle">2</text>
<text class="s-txt-m" x="161" y="144" text-anchor="middle">1</text>
<text class="s-txt-m" x="187" y="144" text-anchor="middle">2</text>
<text class="s-txt-m" x="213" y="144" text-anchor="middle">1</text>
<text class="s-txt-m" x="239" y="144" text-anchor="middle">2</text>
<text class="s-txt-m" x="265" y="144" text-anchor="middle">1</text>
<text class="s-txt-m" x="291" y="144" text-anchor="middle">2</text>
<text class="s-txt-m" x="317" y="144" text-anchor="middle">1</text>
<text class="s-txt-m" x="343" y="144" text-anchor="middle">2</text>
</svg>
<figcaption>Разрыв между двумя гуляющими, ходящими по очереди; цифры под шагами — чей это полуход.</figcaption>
</figure>

**Утверждение 12.**
Чередование $(p_1, -q_1, p_2, -q_2, \dots, p_n, -q_n)$ — биекция между парами траекторий длины $n$ с общим концом и траекториями длины $2n$, заканчивающимися в нуле.

*Доказательство.* Сумма всех шагов равна $\sum p_i - \sum q_i$ и обращается в ноль ровно тогда, когда концы совпали. Обратное отображение очевидно: нечётные шаги дают первую траекторию, чётные с обратным знаком — вторую. ∎

> поле:mn Есть и традиционный способ склеить: приписать к первой траектории вторую, развёрнутую во времени и с обратным знаком. Он тоже биекция, но требует держать в голове разворот времени. Разрыв дешевле.

## Ответ: сколько траекторий не возвращаются

### Что показывает перебор

Возвращаемся к вопросу из первой части. Считать «в лоб» нечего — посчитаем перебором на малых длинах и посмотрим.

<table>
<thead><tr><th>$2n$</th><th>ни разу не в нуле</th><th>заканчиваются в нуле</th><th>$\binom{2n}{n}$</th></tr></thead>
<tbody>
<tr><td>2</td><td>2</td><td>2</td><td>2</td></tr>
<tr><td>4</td><td>6</td><td>6</td><td>6</td></tr>
<tr><td>6</td><td>20</td><td>20</td><td>20</td></tr>
<tr><td>8</td><td>70</td><td>70</td><td>70</td></tr>
<tr><td>10</td><td>252</td><td>252</td><td>252</td></tr>
<tr><td>12</td><td>924</td><td>924</td><td>924</td></tr>
</tbody>
</table>

Числа те самые, которые мы рисовали весь текст: центр строки. Два совершенно разных вопроса — «сколько ни разу не задели ноль» и «сколько кончили в нуле» — дали один ответ.

**Утверждение 13 (Феллер).**
Траекторий длины $2n$, ни разу не попадающих в ноль, ровно $\binom{2n}{n}$.

Шаги равны $\pm 1$, поэтому траектория не может перепрыгнуть ноль. «Ни разу не вернуться» значит **ни разу не сменить знак** — остаться целиком по одну сторону. Знак задаёт первый шаг, так что достаточно разобраться с траекториями, идущими выше нуля (см. утверждение 14).

### Отражение в линии рекордов

Половину работы мы уже сделали: по утверждению 12 пара встретившихся прогулок — это траектория, вернувшаяся в ноль. Остался один ход.

Пусть траектория $S$ кончается в нуле и первый шаг у неё вверх. Нарисуем её **линию рекордов** $M_\ell = \max(S_0, \dots, S_\ell)$ — ступенчатую линию «самая большая высота, где траектория уже побывала». И отразим траекторию в этой линии: точка, висевшая на $d$ ниже рекорда, поднимается на $d$ выше него:

$$T_\ell = 2M_\ell - S_\ell .$$

<figure>
<svg viewBox="0 0 450 184" width="440" role="img" aria-label="Мост, ступенчатая линия его рекордов и отражённый в ней путь, который больше не касается нуля">
<line class="s-thin" x1="46" y1="150" x2="434" y2="150" stroke-dasharray="5 4"/>
<line class="s-thin" x1="152" y1="150" x2="152" y2="94" stroke-dasharray="2 3"/>
<line class="s-thin" x1="284" y1="122" x2="284" y2="66" stroke-dasharray="2 3"/>
<line class="s-thin" x1="328" y1="150" x2="328" y2="38" stroke-dasharray="2 3"/>
<line class="s-thin" x1="372" y1="122" x2="372" y2="66" stroke-dasharray="2 3"/>
<line class="s-thin" x1="416" y1="150" x2="416" y2="38" stroke-dasharray="2 3"/>
<polyline class="s-dash" points="64,150 108,150 108,122 152,122 152,122 196,122 196,122 240,122 240,94 284,94 284,94 328,94 328,94 372,94 372,94 416,94 416,94"/>
<polyline class="s-line" points="64,150 108,122 152,150 196,122 240,94 284,122 328,150 372,122 416,150"/>
<polyline class="s-accent" points="64,150 108,122 152,94 196,122 240,94 284,66 328,38 372,66 416,38"/>
<circle class="s-node" cx="64" cy="150" r="3.4"/>
<circle class="s-node" cx="108" cy="122" r="3.4"/>
<circle class="s-node" cx="152" cy="150" r="3.4"/>
<circle class="s-node" cx="196" cy="122" r="3.4"/>
<circle class="s-node" cx="240" cy="94" r="3.4"/>
<circle class="s-node" cx="284" cy="122" r="3.4"/>
<circle class="s-node" cx="328" cy="150" r="3.4"/>
<circle class="s-node" cx="372" cy="122" r="3.4"/>
<circle class="s-node" cx="416" cy="150" r="3.4"/>
<circle class="s-node-a" cx="64" cy="150" r="3.4"/>
<circle class="s-node-a" cx="108" cy="122" r="3.4"/>
<circle class="s-node-a" cx="152" cy="94" r="3.4"/>
<circle class="s-node-a" cx="196" cy="122" r="3.4"/>
<circle class="s-node-a" cx="240" cy="94" r="3.4"/>
<circle class="s-node-a" cx="284" cy="66" r="3.4"/>
<circle class="s-node-a" cx="328" cy="38" r="3.4"/>
<circle class="s-node-a" cx="372" cy="66" r="3.4"/>
<circle class="s-node-a" cx="416" cy="38" r="3.4"/>
<text class="s-txt-m" x="34" y="155" text-anchor="middle">0</text>
</svg>
<figcaption>Тёмная ломаная — траектория, вернувшаяся в ноль; пунктирная ступенчатая — её рекорды; цветная — результат отражения. Она больше не касается нуля.</figcaption>
</figure>

**Утверждение 14.**
Отражение в линии рекордов — биекция между траекториями длины $2n$, кончающимися в нуле и начинающимися вверх, и траекториями, целиком лежащими выше нуля.

*Доказательство.* **Это снова траектория.** Если шаг ставил рекорд, $M$ выросло на единицу и $T$ изменилось на $2\cdot 1 - 1 = +1$. Если шаг был вверх, но не рекордный, $M$ не изменилось и $T$ изменилось на $-1$. Если шаг был вниз — на $+1$. Всегда $\pm 1$.
**Она не касается нуля.** $T_\ell = 2M_\ell - S_\ell \geq M_\ell \geq 1$ при $\ell \geq 1$: ведь $S_\ell \leq M_\ell$ по определению рекорда, а первый шаг был вверх.
**Обратимость.** Линия рекордов восстанавливается по результату как обрезанный будущий минимум: если $T$ кончается на высоте $2h$, то $J_\ell = \min\bigl(h,\ \min_{j \geq \ell} T_j\bigr)$ и $S_\ell = 2J_\ell - T_\ell$. ∎

> поле:mn **Проверка руками.** На длине 4 обе стороны состоят из шести объектов; отражение переводит их друг в друга без совпадений. Это тот размер, на котором биекцию можно предъявить классу целиком, не веря на слово.

Правило на доске произносится без единой формулы: **пройди по траектории слева направо; шаг, которым она впервые попадает на новую рекордную высоту, оставь, любой другой переверни.**

> поле:mn Проверено перебором до $2n = 14$: отображение инъективно, попадает в цель и накрывает её целиком. Та же конструкция — биекция $\Phi_1$ из препринта arXiv:1903.00158; замкнутая форма $T = 2M - S$ — наша запись.

> поле:insight Почему нельзя проще | Естественная мысль — разрезать траекторию в нижней точке и переставить куски. Этот путь обречён: перестановка кусков сохраняет набор шагов, а значит и конец траектории, поэтому из траектории с концом в нуле так получится опять траектория с концом в нуле. Перебор всех $128$ вариантов «разрез, развороты кусков, порядок склейки» даёт ровно четыре биекции, и все четыре — на **неотрицательные** пути, которые ноль касаться могут. Отражение в линии рекордов попадает в цель сразу.

Вопрос, поставленный в первой части, закрыт: невозвратных траекторий столько же, сколько возвращающихся ровно к концу, и это $\binom{2n}{n}$.

### Колокол, корень и возвращение

Комбинаторный ответ получен. Переведём его обратно в вероятность и посмотрим, что будет при больших $n$. Обозначим

$$u_{2n} = \mathbb{P}(S_{2n} = 0) = \frac{\binom{2n}{n}}{4^n},$$

тогда по утверждению 13 ровно та же величина — вероятность **ни разу** не побывать дома за $2n$ шагов.

<figure class="mn">
<svg viewBox="0 0 312 278" width="300" role="img" aria-label="Распределение положения частицы после двадцати шагов: колокол с пиком в нуле">
<rect class="s-fillsh" x="59.7" y="248.667" width="10.6" height="1.33278"/>
<rect class="s-fillsh" x="72.7" y="244.336" width="10.6" height="5.66434"/>
<rect class="s-fillsh" x="85.7" y="231.874" width="10.6" height="18.1259"/>
<rect class="s-fillsh" x="98.7" y="204.685" width="10.6" height="45.3147"/>
<rect class="s-fillsh" x="111.7" y="159.371" width="10.6" height="90.6294"/>
<rect class="s-fillsh" x="124.7" y="102.727" width="10.6" height="147.273"/>
<rect class="s-fillsh" x="137.7" y="53.6364" width="10.6" height="196.364"/>
<rect class="s-fillw" x="150.7" y="34" width="10.6" height="216"/>
<rect class="s-fillsh" x="163.7" y="53.6364" width="10.6" height="196.364"/>
<rect class="s-fillsh" x="176.7" y="102.727" width="10.6" height="147.273"/>
<rect class="s-fillsh" x="189.7" y="159.371" width="10.6" height="90.6294"/>
<rect class="s-fillsh" x="202.7" y="204.685" width="10.6" height="45.3147"/>
<rect class="s-fillsh" x="215.7" y="231.874" width="10.6" height="18.1259"/>
<rect class="s-fillsh" x="228.7" y="244.336" width="10.6" height="5.66434"/>
<rect class="s-fillsh" x="241.7" y="248.667" width="10.6" height="1.33278"/>
<line class="s-thin" x1="20" y1="250" x2="292" y2="250"/>
<line class="s-dash" x1="156" y1="255" x2="156" y2="20"/>
<text class="s-txt-m" x="156" y="270" text-anchor="middle">0</text>
</svg>
<figcaption>Распределение положения после двадцати шагов; пик в нуле выделен.</figcaption>
</figure>

**Утверждение 15.**
Отношение соседних значений равно $1 - \tfrac{1}{2n}$, откуда $u_{2n}$ убывает как $c/\sqrt{n}$:
$$\frac{u_{2n}}{u_{2n-2}} = 1 - \frac{1}{2n}.$$

*Доказательство.* По утверждению 4 отношение соседних центральных коэффициентов равно $\dfrac{2n-1}{2n}$ после деления на четвёрку. Перемножая такие множители, получаем $u_{2n} = \dfrac{(2n-1)!!}{(2n)!!}$; логарифм суммы даёт порядок $n^{-1/2}$. ∎

*Статус.* Константу этим способом не получить: $u_{2n} \approx 1/\sqrt{\pi n}$, и число $\sqrt{\pi}$ — не лень, а теорема. Его даёт интеграл Валлиса или формула Стирлинга; производящая функция $(1-4x)^{-1/2} = \sum \binom{2n}{n}x^n$ даёт саму последовательность, но константу без анализа особенности из неё не извлечь. В школьной версии её называют «площадью колокола» и выносят за кадр.

> поле:mn **Мост назад.** Ровно этот корень мы видели в начале части про колокол как ширину разброса. Одна величина отвечает и за то, как далеко уходит частица, и за то, как редко она бывает дома.

Наглядно это выглядит так: разброс частицы за $2n$ шагов имеет порядок $\sqrt{2n}$, вероятность размазана по колоколу такой ширины, значит на каждую отдельную точку приходится порядка $1/\sqrt{n}$.

> поле:mn Тот же корень виден и в среднем удалении от дома: $\mathbb{E}|S_{2n}| = 2n\,u_{2n} \approx \sqrt{4n/\pi}$. За десять тысяч шагов пьяница в среднем в восьмидесяти шагах от дома, а не в пяти тысячах.

**Утверждение 16 (Пойа).**
Частица возвращается в ноль с вероятностью $1$.

*Доказательство.* Ожидаемое число визитов в ноль за всё время равно $\sum_{n\geq1} u_{2n}$, то есть $\sum 1/\sqrt{\pi n}$ — ряд расходится. Если бы вероятность возврата равнялась $q \lt 1$, число визитов было бы геометрическим с конечным средним $q/(1-q)$. Значит $q = 1$. ∎

А теперь тот же ряд, прочитанный второй раз — тем самым приёмом суммирования хвостов, которым доказано утверждение 7.

**Утверждение 17.**
Среднее время до первого возвращения **бесконечно**.

*Доказательство.* Вероятность «за $2n$ шагов ни разу не дома» равна $u_{2n}$ по утверждению 13. Значит $\mathbb{E}[T] = \sum_n \mathbb{P}(T \gt n) = 2\sum_{n \geq 1} u_{2n} = \infty$ — тот же расходящийся ряд. ∎

> поле:insight Один ряд, два вывода | Расходимость $\sum u_{2n}$ **одновременно** гарантирует возвращение и убивает среднее время ожидания. Домой придёшь наверняка — а сколько ждать, в среднем бесконечно. Медленность $1/\sqrt{n}$ здесь окупается дважды: достаточно медленная, чтобы ряд разошёлся, и достаточно быстрая, чтобы вероятность невозврата стремилась к нулю.

Вопрос, с которого мы начали, звучал как вопрос про счёт: сколько траекторий не возвращаются. Ответ оказался вопросом про время: не «вернётся ли», а «сколько ждать».

## Что дальше? {свёрнуто}

Всё ниже проверено, но в сквозную линию не встроено. Материал для листка задач, звёздочек и крючков.

### Сюжеты для листка и звёздочек

#### Звезда Давида

Вокруг любого внутреннего числа стоят шесть соседей; раскрасим их через одного. Произведения троек равны, и равны их наибольшие общие делители.

<figure class="mn">
<svg viewBox="0 0 300 198" width="380" role="img" aria-label="Шесть соседей клетки треугольника, раскрашенные через одного в два цвета">
<rect class="s-fillsh" x="23" y="25" width="50" height="34"/>
<rect class="s-line" x="23" y="25" width="50" height="34"/>
<text class="s-txt" x="48" y="48" text-anchor="middle">21</text>
<rect class="s-fillw" x="91" y="25" width="50" height="34"/>
<rect class="s-line" x="91" y="25" width="50" height="34"/>
<text class="s-txt" x="116" y="48" text-anchor="middle">35</text>
<rect class="s-fillw" x="-11" y="85" width="50" height="34"/>
<rect class="s-line" x="-11" y="85" width="50" height="34"/>
<text class="s-txt" x="14" y="108" text-anchor="middle">28</text>
<rect class="s-line" x="57" y="85" width="50" height="34"/>
<text class="s-txt" x="82" y="108" text-anchor="middle">56</text>
<rect class="s-fillsh" x="125" y="85" width="50" height="34"/>
<rect class="s-line" x="125" y="85" width="50" height="34"/>
<text class="s-txt" x="150" y="108" text-anchor="middle">70</text>
<rect class="s-fillsh" x="23" y="145" width="50" height="34"/>
<rect class="s-line" x="23" y="145" width="50" height="34"/>
<text class="s-txt" x="48" y="168" text-anchor="middle">84</text>
<rect class="s-fillw" x="91" y="145" width="50" height="34"/>
<rect class="s-line" x="91" y="145" width="50" height="34"/>
<text class="s-txt" x="116" y="168" text-anchor="middle">126</text>
</svg>
<figcaption>Шесть соседей числа 56: 21·70·126 = 28·35·84, и оба наибольших общих делителя равны 7.</figcaption>
</figure>

*Доказательство равенства произведений.* Распишем обе тройки через факториалы. В числителе слева и справа стоит одно и то же: $(n-1)!\,n!\,(n+1)!$. В знаменателях — одни и те же шесть факториалов, только переставленные местами. ∎

*Статус.* Равенство наибольших общих делителей — теорема Гулда (1972), доказана Хиллманом и Хоггаттом; школьного доказательства у нас нет. Проверено перебором для всех $2 \leq n \lt 40$ без единого нарушения. Хорошее место для честного «приходите на курс».

#### Задача Банаха о спичках

Курильщик носит два коробка по $n$ спичек и каждый раз лезет в случайный; обнаружив коробок пустым, сколько спичек найдёт в другом? Среднее равно $(2n+1)u_{2n} - 1$. Ровно то же число отвечает и на совсем другой вопрос: сколько в среднем раз частица побывала в нуле за $2n$ шагов.

#### Сколько раз меняется лидер

Вероятность ровно $r$ смен лидера в $2n$ бросках равна $2\binom{2n-1}{n-1-r}/2^{2n-1}$ — просто элемент строки Паскаля. Распределение убывает по $r$, значит **самое вероятное число смен лидера — ноль**. Аудитория обычно уверена в противоположном.

#### Разорение игрока

У вас $a$ рублей, у соперника $b$, играете по рублю. Вероятность выиграть $a/(a+b)$ — предсказуемо; а среднее число партий равно $a\cdot b$: при пятидесяти против пятидесяти это две с половиной тысячи партий. Доказательство школьное — проверить, что $D_x = x(N-x)$ удовлетворяет $D_x = 1 + (D_{x-1}+D_{x+1})/2$.

#### Малая теорема Ферма ожерельями

Строка простого номера $p$ делится на $p$ целиком, кроме краёв. Отсюда: $a^p - a$ непостоянных слов длины $p$ разбиваются поворотом на орбиты ровно по $p$ штук, значит $p \mid a^p - a$.

#### Гипотеза Сингмастера

Число $3003$ встречается в треугольнике восемь раз. Больше восьми не знает никто, и никто не умеет доказать, что число повторений вообще ограничено — задача открыта с 1971 года. Формулировку понимает девятиклассник.

#### Ним и Серпинский в трёх измерениях

Проигрышные позиции нима на трёх кучках — те, где двоичный XOR размеров равен нулю. Разбив куб на восемь октантов по старшим битам, получаем ровно четыре допустимых, и это вершины правильного тетраэдра: множество проигрышных позиций — тетраэдр Серпинского.

> поле:mn Ханойские башни дают ещё один сюжет: граф их состояний — треугольник Серпинского, а при случайных ходах время сборки растёт впятеро при удвоении размера — это показатель диффузии на фрактале $\log 5/\log 2$. Для полутора часов не тянет и с треугольником Паскаля не связано.

### Что проверено и что опровергнуто

Все числа в тексте получены перебором или точной арифметикой. Ключевые проверки: невозвратные, возвращающиеся и пары встретившихся совпадают до $2n = 14$; обе биекции инъективны и накрывают цель; пар без переноса ровно $3^m$ до $m = 7$; равенство «нет переноса ⟺ коэффициент нечётен» — без расхождений при $a, b \lt 48$; показатель двойки и число нечётных в строке — без расхождений при $n \lt 150$; тройка $1:2:3$ единственна до $n = 700$; звезда Давида — без нарушений при $n \lt 40$.

#### Опровергнуто

В раннем черновике стояло, что максимум блуждания распределён так же, как $|S_n|$. Для дискретного блуждания это неверно: при $n = 4$ распределение максимума по значениям $0,\dots,4$ равно $(6,4,4,1,1)$, а модуля по значениям $0,2,4$ — $(6,8,2)$. Совпадение — факт про броуновское движение, а не про монеты.

#### Отброшено после проверки

Правило 90 при случайной начальной строке смывает узор. Игра в хаос не даёт задачи на счёт. «Два случайных подмножества» дают ту же тройку, но самоподобие из постановки не видно. Делимость $\binom{2n}{n}$ на $n+1$ — числа Каталана в профиль, за границей темы. Постулат Бертрана через центральный коэффициент — доказательство на страницу.

> поле:mn **Чего мы не проверяли сами.** Доказательство про смены лидера взято у Феллера и своими руками не восстановлено. Если сюжет пойдёт в лекцию — восстановить.

> поле:mn **Что сверить перед сценой.** Формулировку теоремы Гулда — с оригиналом 1972 года: мы её только проверили перебором, но не доказывали.

## Источники {скрыть}

1. Феллер В. Введение в теорию вероятностей и её приложения, т. 1 — гл. III (невозврат, смены лидера), VI.8 (задача Банаха), XIII.4 (времена ожидания), XIV (разорение игрока).
2. Song S., Yao Q. The Construction of Two Kinds of Bijections in Simple Random Walk Paths. arXiv:1903.00158 — явная биекция между возвращающимися и строго положительными траекториями.
3. Kummer E. J. reine angew. Math. 44 (1852) — показатель простого равен числу переносов.
4. Granville A. Zaphod Beeblebrox's Brain and the Fifty-ninth Row of Pascal's Triangle. Amer. Math. Monthly 99 (1992) — самоподобие треугольника по модулю $p$.
5. Graham R., Knuth D., Patashnik O. Конкретная математика — §5.3 (Куммер), §8.4 (времена ожидания).
6. Hoggatt V. E., Hansell W. Fibonacci Quarterly 9 (1971); Gould H. W. (1972); Hillman A. P., Hoggatt V. E. (1972) — звезда Давида.
7. Singmaster D. Fibonacci Quarterly 13 (1975); Matomäki K. и др. Q. J. Math 73 (2022) — гипотеза Сингмастера.
8. Golomb S. Amer. Math. Monthly 63 (1956) — малая теорема Ферма ожерельями.
9. Gibbons K. The Geometry of Nim. arXiv:1109.6712; Alekseyev M., Berger T. arXiv:1304.3780 — ним и ханойские башни.
10. OEIS A001316, A000984.

> поле:foot Черновик, статус `chernovik`. Математика проверена перебором, терминология сверена; полный стилевой прогон не делался. Два долга помечены флагами. Порядок изложения — логический: каждая часть отвечает на вопрос, оставленный предыдущей.
