---
tab: C. Запрет второй: Брауэр
status: chernovik
poryadok: 4
registr: читаемый
---

# Блок C. Запрет второй — Брауэр

> поле:mn **Что это.** Тексты слайдов лекции 1 в том объёме, в котором они лягут на слайд, собранные лентой. Каждый раздел ниже = ОДИН слайд. Сцены несёт сама лента: `{@N}` — приходит с $N$-й сцены, `{@N-M}` — приходит на $N$-й и уходит после $M$-й. Бюджет — на СЦЕНУ, не на слайд.

## Как доказывают, что функтора нет

> поле:mn **Раскладка.** Текстовая область — на всю ширину, коммутативная диаграмма ложится горизонтальной полосой снизу (правка 20.2).

> поле:mn **Вёрстка.** Осиротели две иллюстрации, обе оставлены в файле нетронутыми. (1) «Носитель против палитры»: текста под неё на ленте нет (пример с инъекциями выкинут по бюджету), но сама задача про инъекции уходит в лист упражнений — картинка может уехать туда вместе с ней, решение за аналитиком. (2) На следующем слайде схема $FX\to FY$ — по-прежнему без своего текста: либо снимается, либо ей нужен текст, которого в источнике нет.

**Утверждение.** Сопоставление $G\mapsto Z(G)$ не продолжается до функтора $\mathbf{Grp}\to\mathbf{Grp}$

{@1-1} **Центр** $Z(G)$ — элементы, коммутирующие со всеми: $zg=gz$ при любом $g\in G$

$\mathbb Z_2=\{0,1\}$ · $s\colon\mathbb Z_2\to S_3$: $0\mapsto e$, $1\mapsto(1\,2)$ · $\mathrm{sgn}\colon S_3\to\mathbb Z_2$: нечётные $\mapsto1$, чётные $\mapsto0$

$\mathrm{sgn}\circ s\colon 0\mapsto e\mapsto 0$, $1\mapsto(1\,2)\mapsto 1$ — то есть $\mathrm{sgn}\circ s=\mathrm{id}_{\mathbb Z_2}$

{@2} $Z(\mathbb Z_2)=\mathbb Z_2$ · $Z(S_3)=\{e\}$: центральный $z$ сохраняет $\{a,b\}$ у каждой транспозиции $(a\,b)$, откуда $z(1)=1$ и далее $z=e$

{@2} Функтор дал бы $\mathrm{id}_{\mathbb Z_2}\colon\mathbb Z_2\to\{e\}\to\mathbb Z_2$, но $1\mapsto e\mapsto 0$ — постоянное, не тождество

<figure class="mn">
<svg viewBox="0 0 300 200" width="300" role="img" aria-label="Наверху группа ℤ₂, стрелка в S3 и стрелка знака обратно в ℤ₂, композиция тождественна. Внизу их центры: ℤ₂, единичная группа, ℤ₂, и обратного пути внизу нет">
<text class="s-txt" x="30" y="34" text-anchor="middle" font-size="17">ℤ₂</text><text class="s-txt" x="150" y="34" text-anchor="middle" font-size="17">S₃</text><text class="s-txt" x="270" y="34" text-anchor="middle" font-size="17">ℤ₂</text>
<text class="s-txt" x="30" y="180" text-anchor="middle" font-size="17">ℤ₂</text><text class="s-txt" x="150" y="180" text-anchor="middle" font-size="17">{e}</text><text class="s-txt" x="270" y="180" text-anchor="middle" font-size="17">ℤ₂</text>
<line class="s-thin" x1="46" y1="29" x2="132" y2="29"></line><path class="s-ar-m" d="M123,25 l9,4 -9,4 z"></path>
<line class="s-thin" x1="168" y1="29" x2="252" y2="29"></line><path class="s-ar-m" d="M243,25 l9,4 -9,4 z"></path>
<line class="s-thin" x1="54" y1="175" x2="126" y2="175"></line><path class="s-ar-m" d="M117,171 l9,4 -9,4 z"></path>
<line class="s-thin" x1="174" y1="175" x2="246" y2="175"></line><path class="s-ar-m" d="M237,171 l9,4 -9,4 z"></path>
<line class="s-dash" x1="30" y1="46" x2="30" y2="158"></line><path class="s-ar-a" d="M26,149 l4,9 4,-9 z"></path>
<line class="s-dash" x1="150" y1="46" x2="150" y2="158"></line><path class="s-ar-a" d="M146,149 l4,9 4,-9 z"></path>
<line class="s-dash" x1="270" y1="46" x2="270" y2="158"></line><path class="s-ar-a" d="M266,149 l4,9 4,-9 z"></path>
<text class="s-txt-m" x="89" y="18" text-anchor="middle" font-size="15">s</text><text class="s-txt-m" x="210" y="18" text-anchor="middle" font-size="15">sgn</text>
<text class="s-txt-m" x="90" y="198" text-anchor="middle" font-size="15">Zs</text><text class="s-txt-m" x="210" y="198" text-anchor="middle" font-size="15">Zr</text>
<text class="s-txt-m" x="38" y="106" font-size="15">Z</text><text class="s-txt-m" x="158" y="106" font-size="15">Z</text><text class="s-txt-m" x="278" y="106" font-size="15">Z</text>
<text class="s-txt-m" x="150" y="62" text-anchor="middle" font-size="14">sgn ∘ s = id</text>
<text class="s-txt-m" x="150" y="146" text-anchor="middle" font-size="14">= id ?</text>
</svg>
<figcaption>Наверху пара стрелок с тождественной композицией: транспозиция вкладывается в $S_3$, знак возвращает её обратно. Внизу тот же чертёж после взятия центров, и здесь средний этаж стал единичной группой: пройти $\mathbb Z_2\to\{e\}\to\mathbb Z_2$ тождественно нельзя.</figcaption>
</figure>

<figure class="mn">
<svg viewBox="0 0 200 196" width="200" role="img" aria-label="Слева столбик из пяти точек, справа четыре клетки палитры. Первые три точки уходят каждая в свою клетку, а последние две попадают в одну и ту же нижнюю клетку">
<circle class="s-node" cx="52" cy="34" r="4.4"/><circle class="s-node" cx="52" cy="60" r="4.4"/><circle class="s-node" cx="52" cy="86" r="4.4"/><circle class="s-node" cx="52" cy="112" r="4.4"/><circle class="s-node-r" cx="52" cy="138" r="4.4"/>
<rect class="s-line" x="132" y="25" width="18" height="18"/>
<rect class="s-line" x="132" y="51" width="18" height="18"/>
<rect class="s-line" x="132" y="77" width="18" height="18"/>
<rect class="s-fillsh" x="132" y="103" width="18" height="18"/><rect class="s-line" x="132" y="103" width="18" height="18"/>
<line class="s-thin" x1="60" y1="34" x2="122" y2="34"/><path class="s-ar-m" d="M120,30 l9,4 -9,4 z"/>
<line class="s-thin" x1="60" y1="60" x2="122" y2="60"/><path class="s-ar-m" d="M120,56 l9,4 -9,4 z"/>
<line class="s-thin" x1="60" y1="86" x2="122" y2="86"/><path class="s-ar-m" d="M120,82 l9,4 -9,4 z"/>
<line class="s-accent" x1="60" y1="112" x2="120" y2="112"/><path class="s-ar-a" d="M119,108 l9,4 -9,4 z"/>
<line class="s-accent" x1="60" y1="136" x2="118" y2="118"/><path class="s-ar-a" d="M117,114 l10,3 -7,7 z"/>
<text class="s-txt" x="52" y="168" text-anchor="middle">k+1</text>
<text class="s-txt" x="141" y="168" text-anchor="middle">k</text>
</svg>
<figcaption>Носитель на один элемент больше палитры, и одна клетка обязана принять две точки: инъекции из $B$ в $k$ цветов не существует ни одной, тогда как из $A$ их ровно $k!$.</figcaption>
</figure>

## Брауэр в работе

> поле:mn **Раскладка.** Мало текста, крупная горизонтальная иллюстрация снизу: окружность в диске и луч внутри диска с портретом.

**Утверждение.** В $\mathbf{Top}$ нет $r\colon D^2\to S^1$ с $r\circ i=\mathrm{id}_{S^1}$

$D^2=\{x\in\mathbb R^2:\lVert x\rVert\le1\}$ · $S^1=\{\lVert x\rVert=1\}$ · $i\colon S^1\to D^2$, $i(x)=x$

{@1-1} Известным берём: $\pi_1$ — функтор пространств с отмеченной точкой, $\pi_1(S^1)\cong\mathbb Z$, $\pi_1(D^2)=\{e\}$

{@1-1} Пара $(r,i)$ дала бы $\mathbb Z\to\{e\}\to\mathbb Z$: гомоморфизм из $\{e\}$ шлёт каждый элемент в нейтральный, композиция постоянна — тождественной не бывает

{@2} **Теорема (Брауэр).** Всякое непрерывное $f\colon D^2\to D^2$ имеет неподвижную точку

{@2} Пусть $f(x)\ne x$ всюду · $u=\dfrac{x-f(x)}{\lVert x-f(x)\rVert}$, $a=\langle x,u\rangle$, $t=-a+\sqrt{a^2+1-\lVert x\rVert^2}$ · $r(x)=x+tu\in S^1$, непрерывно

{@2} На границе $\lVert x\rVert=1$: $\langle x,x-f(x)\rangle=1-\langle x,f(x)\rangle\ge0$ при $\lVert f(x)\rVert\le1$, значит $a\ge0$, $t=0$, $r(x)=x$

{@2} Но такое $r$ запрещено утверждением выше ⇒ $f(x)\ne x$ ложно

🖼 Портрет Лёйтзена Брауэра {1}

<figure>
<svg viewBox="0 0 560 220" width="560" role="img" aria-label="Внизу два множества по четыре точки и отображение между ними, наверху их образы по три точки и отображение между образами, вертикальные стрелки поднимают каждое множество в его образ">
<rect class="s-line" x="76" y="46" width="80" height="36" rx="8"/>
<circle class="s-node" cx="96" cy="64" r="4.4"/><circle class="s-node" cx="116" cy="64" r="4.4"/><circle class="s-node" cx="136" cy="64" r="4.4"/>
<rect class="s-line" x="404" y="46" width="80" height="36" rx="8"/>
<circle class="s-node" cx="424" cy="64" r="4.4"/><circle class="s-node" cx="444" cy="64" r="4.4"/><circle class="s-node" cx="464" cy="64" r="4.4"/>
<rect class="s-line" x="64" y="150" width="104" height="36" rx="8"/>
<circle class="s-node" cx="84" cy="168" r="4.4"/><circle class="s-node" cx="108" cy="168" r="4.4"/><circle class="s-node" cx="132" cy="168" r="4.4"/><circle class="s-node" cx="156" cy="168" r="4.4"/>
<rect class="s-line" x="392" y="150" width="104" height="36" rx="8"/>
<circle class="s-node" cx="412" cy="168" r="4.4"/><circle class="s-node" cx="436" cy="168" r="4.4"/><circle class="s-node" cx="460" cy="168" r="4.4"/><circle class="s-node" cx="484" cy="168" r="4.4"/>
<line class="s-thin" x1="164" y1="64" x2="396" y2="64"/><path class="s-ar-m" d="M394,60 l9,4 -9,4 z"/>
<line class="s-thin" x1="176" y1="168" x2="384" y2="168"/><path class="s-ar-m" d="M382,164 l9,4 -9,4 z"/>
<line class="s-dash" x1="116" y1="146" x2="116" y2="90"/><path class="s-ar-a" d="M112,99 l4,-9 4,9 z"/>
<line class="s-dash" x1="444" y1="146" x2="444" y2="90"/><path class="s-ar-a" d="M440,99 l4,-9 4,9 z"/>
<text class="s-txt" x="116" y="36" text-anchor="middle" font-size="17">FX</text>
<text class="s-txt" x="444" y="36" text-anchor="middle" font-size="17">FY</text>
<text class="s-txt" x="116" y="198" text-anchor="middle" font-size="17">X</text>
<text class="s-txt" x="444" y="198" text-anchor="middle" font-size="17">Y</text>
<text class="s-txt-m" x="280" y="56" text-anchor="middle" font-size="15">Ff</text>
<text class="s-txt-m" x="280" y="160" text-anchor="middle" font-size="15">f</text>
<text class="s-txt-m" x="124" y="120" font-size="15">F</text>
<text class="s-txt-m" x="452" y="120" font-size="15">F</text>
</svg>
<figcaption>Что требуется от конструкции: каждому множеству отвечает множество строго меньшего размера, каждому отображению $f$ отвечает отображение образов $Ff$, и композиции переходят в композиции.</figcaption>
</figure>

<figure class="mn">
<svg viewBox="0 0 220 250" width="220" role="img" aria-label="Наверху окружность и диск, стрелка вложения вперёд и пунктирная стрелка обратно. Внизу их фундаментальные группы: целые числа и единичная группа, и обратный путь через единичную группу помечен вопросом">
<circle class="s-line" cx="54" cy="52" r="24"/>
<circle class="s-fillsh" cx="166" cy="52" r="24"/><circle class="s-line" cx="166" cy="52" r="24"/>
<text class="s-txt" x="54" y="92" text-anchor="middle" font-size="17">S¹</text>
<text class="s-txt" x="166" y="92" text-anchor="middle" font-size="17">D²</text>
<line class="s-thin" x1="84" y1="44" x2="132" y2="44"/><path class="s-ar-m" d="M130,40 l9,4 -9,4 z"/>
<line class="s-dash" x1="136" y1="62" x2="92" y2="62"/><path class="s-ar-a" d="M91,58 l-9,4 9,4 z"/>
<text class="s-txt-m" x="108" y="34" text-anchor="middle" font-size="15">i</text>
<text class="s-txt-m" x="108" y="78" text-anchor="middle" font-size="15">r</text>
<line class="s-dash" x1="54" y1="104" x2="54" y2="148"/><path class="s-ar-a" d="M50,139 l4,9 4,-9 z"/>
<line class="s-dash" x1="166" y1="104" x2="166" y2="148"/><path class="s-ar-a" d="M162,139 l4,9 4,-9 z"/>
<text class="s-txt-m" x="62" y="128" font-size="15">π₁</text>
<text class="s-txt-m" x="174" y="128" font-size="15">π₁</text>
<text class="s-txt" x="54" y="176" text-anchor="middle" font-size="17">ℤ</text>
<text class="s-txt" x="166" y="176" text-anchor="middle" font-size="17">{e}</text>
<line class="s-thin" x1="70" y1="194" x2="146" y2="194"/><path class="s-ar-m" d="M144,190 l9,4 -9,4 z"/>
<line class="s-dash" x1="150" y1="210" x2="73" y2="210"/><path class="s-ar-a" d="M73,206 l-9,4 9,4 z"/>
<text class="s-txt-m" x="110" y="228" text-anchor="middle" font-size="14">= id ?</text>
</svg>
<figcaption>Окружность вкладывается в диск; вопрос в том, есть ли непрерывный путь обратно, тождественный на окружности. Фундаментальная группа переводит эту пару в пару между $\mathbb Z$ и единичной группой, а там тождество через единичную группу не проходит.</figcaption>
</figure>

<figure class="mn">
<svg viewBox="0 0 220 214" width="220" role="img" aria-label="Диск с выделенной границей: внутри точка f от x, точка x и пунктирный луч из f от x через x до границы, где он упирается в точку r от x">
<circle class="s-fillsh" cx="110" cy="100" r="72"/>
<circle class="s-accent" cx="110" cy="100" r="72"/>
<line class="s-dash" x1="86" y1="128" x2="176" y2="81"/><path class="s-ar-a" d="M174,87 L170,80 L180,79 z"/>
<circle class="s-node" cx="86" cy="128" r="4.4"/>
<circle class="s-node-r" cx="120" cy="110" r="4.4"/>
<circle class="s-node-a" cx="179" cy="79" r="4.4"/>
<text class="s-txt" x="74" y="146" text-anchor="middle">f(x)</text>
<text class="s-txt" x="126" y="102" text-anchor="middle">x</text>
<text class="s-txt" x="172" y="64" text-anchor="middle">r(x)</text>
<text class="s-txt" x="150" y="142" text-anchor="middle">D²</text>
<text class="s-txt-m" x="110" y="196" text-anchor="middle">S¹</text>
</svg>
<figcaption>Если ни одна точка не остаётся на месте, то через $x$ и $f(x)$ проходит луч, и он высекает на границе точку $r(x)$. На самой границе луч упирается в исходную точку, поэтому построенное отображение оставляет окружность на месте.</figcaption>
</figure>
