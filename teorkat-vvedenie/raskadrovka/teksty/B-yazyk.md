---
tab: B. Язык и зоопарк
status: chernovik
poryadok: 2
registr: читаемый
---

# Блок B. Язык и зоопарк

> поле:mn **Что это.** Тексты слайдов лекции 1 в том объёме, в котором они лягут на слайд, собранные лентой. Каждый раздел ниже = ОДИН слайд, ОДИН экран, потолок 650 знаков видимого. Сцены несёт сама лента: `{@N}` — приходит с $N$-й сцены, `{@N-M}` — приходит на $N$-й и уходит после $M$-й; сцен не более двух, и только для дозирования.

## Категория, функтор, естественное преобразование

> поле:mn **Раскладка.** Один экран: четыре пункта категории, затем функтор и естественное преобразование. Справа треугольник композиции и квадрат естественности. **Задача вёрстки (текст не трогал):** сюда приехала из блока E третья иллюстрация — одно пространство и два базиса в нём, то есть замена базиса как естественное преобразование. Раздел односценный, картинок стало три на одну полосу — раскладку решает вёрстка.

**Категория** $\mathcal C$:

- объекты: класс $\mathrm{Ob}\,\mathcal C$
- морфизмы: на упорядоченную пару $A,B$ множество $\mathcal C(A,B)$
- композиция: $\circ\colon\mathcal C(A,B)\times\mathcal C(B,C)\to\mathcal C(A,C)$, ассоциативная
- единица: $1_A\in\mathcal C(A,A)$

**Функтор** $F\colon\mathcal C\to\mathcal D$: $\mathrm{Ob}\,\mathcal C\to\mathrm{Ob}\,\mathcal D$ и $\mathcal C(A,B)\to\mathcal D(FA,FB)$; $F(g\circ f)=Fg\circ Ff$, $F1_A=1_{FA}$

**Естественное преобразование** $\alpha\colon F\Rightarrow G$: $\alpha_A\in\mathcal D(FA,GA)$ с $Gf\circ\alpha_A=\alpha_B\circ Ff$ при всяком $f\in\mathcal C(A,B)$

Пример: матрица перехода между двумя базисами — компонента естественного изоморфизма

<figure class="mn"><svg viewBox="0 0 250 200" width="250" role="img" aria-label="Треугольник композиции: стрелка из A в B, стрелка из B в C и нижняя стрелка из A в C, помеченная композицией"><text class="s-txt" x="40" y="170" text-anchor="middle" font-size="17">A</text><text class="s-txt" x="125" y="46" text-anchor="middle" font-size="17">B</text><text class="s-txt" x="210" y="170" text-anchor="middle" font-size="17">C</text><line class="s-thin" x1="50" y1="152" x2="112" y2="60"></line><path class="s-ar-m" d="M105,58 l10,-4 -2,10 z"></path><line class="s-thin" x1="138" y1="60" x2="200" y2="152"></line><path class="s-ar-m" d="M192,150 l10,4 -2,-10 z"></path><line class="s-thin" x1="58" y1="176" x2="190" y2="176"></line><path class="s-ar-m" d="M181,172 l9,4 -9,4 z"></path><text class="s-txt-m" x="70" y="106" text-anchor="end" font-size="15">f</text><text class="s-txt-m" x="182" y="106" font-size="15">g</text><text class="s-txt-m" x="125" y="196" text-anchor="middle" font-size="15">g∘f</text></svg><figcaption>Композиция — единственная операция категории: у пары стрелок с общим средним объектом есть третья стрелка, замыкающая треугольник. Ассоциативность означает, что при четырёх объектах порядок замыканий не важен.</figcaption></figure>

<figure class="mn"><svg viewBox="0 0 250 200" width="250" role="img" aria-label="Квадрат естественности: компонента преобразования, применённая до и после действия морфизма, даёт один результат"><text class="s-txt" x="52" y="34" text-anchor="middle" font-size="17">FA</text><text class="s-txt" x="198" y="34" text-anchor="middle" font-size="17">FB</text><text class="s-txt" x="52" y="178" text-anchor="middle" font-size="17">GA</text><text class="s-txt" x="198" y="178" text-anchor="middle" font-size="17">GB</text><line class="s-thin" x1="86" y1="29" x2="158" y2="29"></line><path class="s-ar-m" d="M149,25 l9,4 -9,4 z"></path><line class="s-thin" x1="86" y1="173" x2="158" y2="173"></line><path class="s-ar-m" d="M149,169 l9,4 -9,4 z"></path><line class="s-thin" x1="52" y1="48" x2="52" y2="152"></line><path class="s-ar-m" d="M48,143 l4,9 4,-9 z"></path><line class="s-thin" x1="198" y1="48" x2="198" y2="152"></line><path class="s-ar-m" d="M194,143 l4,9 4,-9 z"></path><text class="s-txt-m" x="122" y="18" text-anchor="middle" font-size="15">Ff</text><text class="s-txt-m" x="122" y="196" text-anchor="middle" font-size="15">Gf</text><text class="s-txt-m" x="44" y="105" text-anchor="end" font-size="15">α<tspan dy="3" font-size="11">A</tspan></text><text class="s-txt-m" x="206" y="105" font-size="15">α<tspan dy="3" font-size="11">B</tspan></text></svg><figcaption>Перевести и потом подействовать — то же, что подействовать и потом перевести. Этот квадрат уже стоял в требовании красоты; там оба функтора были видами, здесь они произвольны.</figcaption></figure>

<figure class="mn">
<svg viewBox="0 0 200 190" width="200" role="img" aria-label="Одна плоскость и в ней две пары осей из общего начала: сплошная пара помечена e с индексами, пунктирная акцентная пара помечена f с индексами">
<circle class="s-node" cx="60" cy="130" r="4.4"/>
<line class="s-thin" x1="66" y1="130" x2="140" y2="130"/>
<path class="s-ar-m" d="M133,126 l9,4 -9,4 z"/>
<line class="s-thin" x1="60" y1="124" x2="60" y2="52"/>
<path class="s-ar-m" d="M56,61 l4,-9 4,9 z"/>
<line class="s-dash" x1="66" y1="127" x2="132" y2="98"/>
<path class="s-ar-a" d="M124,97 l9,1 -4,-9 z"/>
<line class="s-dash" x1="63" y1="124" x2="98" y2="56"/>
<path class="s-ar-a" d="M92,60 l6,-8 3,9 z"/>
<text class="s-txt" x="150" y="135">e₁</text>
<text class="s-txt" x="48" y="46" text-anchor="end">e₂</text>
<text class="s-txt" x="142" y="94">f₁</text>
<text class="s-txt" x="106" y="50">f₂</text>
</svg>
<figcaption>Пространство одно, а базисов в нём сколько угодно; каждый выбор задаёт свой изоморфизм с координатным пространством. Переход от одного выбора к другому и есть матрица перехода, то есть компонента естественного изоморфизма.</figcaption>
</figure>

## Конструкции

> поле:mn **Раскладка.** Один экран: четыре конструкции. Справа подкатегория внутри категории и путь как один морфизм.

**Противоположная** $\mathcal C^{\mathrm{op}}$: те же объекты, $\mathcal C^{\mathrm{op}}(A,B)=\mathcal C(B,A)$, композиция $g\circ_{\mathrm{op}}f=f\circ g$

**Подкатегория** $\mathcal D\subseteq\mathcal C$: класс объектов и $\mathcal D(A,B)\subseteq\mathcal C(A,B)$, замкнутое по композиции и с тождествами. **Полна**, если $\mathcal D(A,B)=\mathcal C(A,B)$ всюду

**Произведение** $\mathcal C\times\mathcal D$: покомпонентно, $(\mathcal C\times\mathcal D)\bigl((C,D),(C',D')\bigr)=\mathcal C(C,C')\times\mathcal D(D,D')$

<figure class="mn"><svg viewBox="0 0 250 200" width="250" role="img" aria-label="Внутри категории выделена залитая область: четыре её объекта со стрелками между ними образуют подкатегорию, пятый объект остался снаружи, и стрелка к нему в подкатегорию не входит"><rect class="s-fillsh" x="26" y="32" width="132" height="128" rx="10"></rect><circle class="s-node-a" cx="58" cy="64" r="4.6"></circle><circle class="s-node-a" cx="126" cy="64" r="4.6"></circle><circle class="s-node-a" cx="58" cy="128" r="4.6"></circle><circle class="s-node-a" cx="126" cy="128" r="4.6"></circle><circle class="s-node" cx="212" cy="96" r="4.6"></circle><line class="s-line" x1="66" y1="64" x2="118" y2="64"></line><path class="s-ar-m" d="M109,60 l9,4 -9,4 z"></path><line class="s-line" x1="58" y1="72" x2="58" y2="120"></line><path class="s-ar-m" d="M54,111 l4,9 4,-9 z"></path><line class="s-line" x1="126" y1="72" x2="126" y2="120"></line><path class="s-ar-m" d="M122,111 l4,9 4,-9 z"></path><line class="s-thin" x1="134" y1="70" x2="204" y2="90"></line><path class="s-ar-m" d="M196,86 l9,4 -10,4 z"></path><text class="s-txt" x="40" y="176" text-anchor="middle" font-size="17">D</text><text class="s-txt" x="228" y="120" text-anchor="middle" font-size="17">C</text></svg><figcaption>Залитая область — подкатегория: часть объектов и часть стрелок между ними, замкнутая относительно композиции. Стрелка к внешнему объекту в неё не входит; подкатегория полна, если между своими объектами она забрала все стрелки без исключения.</figcaption></figure>

<figure class="mn"><svg viewBox="0 0 250 200" width="250" role="img" aria-label="Три вершины графа в ряд, соединённые двумя рёбрами; ниже акцентная дуга ведёт из первой вершины прямо в третью — это путь, который в свободной категории служит одним морфизмом"><circle class="s-node-a" cx="44" cy="60" r="4.6"></circle><circle class="s-node" cx="125" cy="60" r="4.6"></circle><circle class="s-node-a" cx="206" cy="60" r="4.6"></circle><line class="s-line" x1="52" y1="60" x2="117" y2="60"></line><path class="s-ar-m" d="M108,56 l9,4 -9,4 z"></path><line class="s-line" x1="133" y1="60" x2="198" y2="60"></line><path class="s-ar-m" d="M189,56 l9,4 -9,4 z"></path><path class="s-accent" d="M44,72 C60,150 190,150 206,72"></path><path class="s-ar-a" d="M202,82 l4,-10 5,9 z"></path><text class="s-txt" x="44" y="42" text-anchor="middle" font-size="17">u</text><text class="s-txt" x="206" y="42" text-anchor="middle" font-size="17">v</text></svg><figcaption>Рёбра графа сами морфизмами не считаются: морфизмом объявлен путь. Два ребра подряд дают одну стрелку из $u$ в $v$, композиция сводится к приписыванию путей, а тождество есть путь нулевой длины.</figcaption></figure>

## Категории: множество со структурой

> поле:mn **Раскладка.** Один экран: список обозначений четырьмя группами. Справа только полезные картинки: нерастягивающее отображение и отношение против диагонали. **Задача вёрстки (текст не трогал):** figure раскраски графов остался без текста — разбор раскраски выкинут; figure кобордизма и тангла ушли текстом на следующий слайд, картинки перенести туда же.

Стрелка — отображение, сохраняющее структуру. Алгебраические:

$\mathbf{Set}$ · $\mathbf{Grp}$ · $\mathbf{Vect}$ · $\mathbf{Ring}$ · $\mathbf{Mod}_R$ · $\mathbf{Lie}$

Геометрические: $\mathbf{Top}$ · $\mathbf{Man}$ · $\mathbf{Met}$ · $\mathbf{Hilb}$

Множества со структурой: $G\text{-}\mathbf{Set}$ · $\mathbf{Grph}$

Информация в стрелках: $\mathbf{Mat}$ объекты — числа, морфизмы — матрицы $m\times n$ · $\mathbf{Rel}$ объекты — множества, морфизмы — отношения

**Категория — решение, а не свойство объектов:** в $\mathbf{Met}$ морфизмом объявлен суженный класс, нерастягивающие

<figure class="mn"><svg viewBox="0 0 250 200" width="250" role="img" aria-label="Наверху три точки метрического пространства с широкими промежутками, внизу их образы с промежутками поуже; расстояние помечено сверху как d, снизу как не больше d"><circle class="s-node" cx="40" cy="56" r="4.6"></circle><circle class="s-node" cx="124" cy="56" r="4.6"></circle><circle class="s-node" cx="208" cy="56" r="4.6"></circle><line class="s-thin" x1="40" y1="34" x2="124" y2="34"></line><text class="s-txt-m" x="82" y="26" text-anchor="middle" font-size="15">d</text><circle class="s-node-r" cx="40" cy="150" r="4.6"></circle><circle class="s-node-r" cx="96" cy="150" r="4.6"></circle><circle class="s-node-r" cx="152" cy="150" r="4.6"></circle><line class="s-accent" x1="40" y1="176" x2="96" y2="176"></line><text class="s-txt-m" x="68" y="194" text-anchor="middle" font-size="15">≤ d</text><line class="s-dash" x1="40" y1="70" x2="40" y2="136"></line><path class="s-ar-a" d="M36,127 l4,9 4,-9 z"></path><line class="s-dash" x1="124" y1="70" x2="98" y2="136"></line><path class="s-ar-a" d="M94,127 l4,9 7,-6 z"></path><line class="s-dash" x1="208" y1="70" x2="154" y2="136"></line><path class="s-ar-a" d="M150,127 l4,9 9,-4 z"></path><text class="s-txt-m" x="228" y="108" font-size="15">f</text></svg><figcaption>Нерастягивающее отображение: расстояние между образами не больше расстояния между точками. Сохраняющих структуру отображений здесь больше, но морфизмами объявлен только этот суженный класс, и категория получается другая.</figcaption></figure>

<figure class="mn"><svg viewBox="0 0 250 200" width="250" role="img" aria-label="Слева граф-путь из четырёх вершин, окрашенных в три сорта; справа треугольник — полный граф на трёх вершинах; между ними стрелка, каждая вершина слева идёт в вершину своего цвета"><circle class="s-node-r" cx="30" cy="46" r="5"></circle><circle class="s-node-a" cx="86" cy="46" r="5"></circle><circle class="s-node" cx="86" cy="118" r="5"></circle><circle class="s-node-a" cx="30" cy="118" r="5"></circle><line class="s-line" x1="36" y1="46" x2="80" y2="46"></line><line class="s-line" x1="86" y1="52" x2="86" y2="112"></line><line class="s-line" x1="80" y1="118" x2="36" y2="118"></line><circle class="s-node-r" cx="196" cy="46" r="5"></circle><circle class="s-node-a" cx="228" cy="112" r="5"></circle><circle class="s-node" cx="164" cy="112" r="5"></circle><line class="s-line" x1="193" y1="52" x2="167" y2="106"></line><line class="s-line" x1="199" y1="52" x2="225" y2="106"></line><line class="s-line" x1="170" y1="112" x2="222" y2="112"></line><line class="s-thin" x1="104" y1="82" x2="142" y2="82"></line><path class="s-ar-m" d="M133,78 l9,4 -9,4 z"></path><text class="s-txt-m" x="123" y="70" text-anchor="middle" font-size="15">f</text><text class="s-txt" x="58" y="166" text-anchor="middle" font-size="17">G</text><text class="s-txt" x="196" y="166" text-anchor="middle" font-size="17">K₃</text></svg><figcaption>Правильная раскраска — гомоморфизм графов: смежные вершины обязаны пойти в разные вершины полного графа, а это в точности запрет на одинаковый цвет у концов ребра. Считать раскраски и считать морфизмы — одна задача.</figcaption></figure>

<figure class="mn"><svg viewBox="0 0 250 200" width="250" role="img" aria-label="Слева два элемента множества, справа те же два; акцентная линия соединяет первый слева со вторым справа — это всё отношение; пунктиром показаны две линии диагонали"><circle class="s-node-r" cx="62" cy="64" r="5"></circle><circle class="s-node" cx="62" cy="136" r="5"></circle><circle class="s-node" cx="188" cy="64" r="5"></circle><circle class="s-node-r" cx="188" cy="136" r="5"></circle><line class="s-dash" x1="70" y1="64" x2="180" y2="64"></line><line class="s-dash" x1="70" y1="136" x2="180" y2="136"></line><line class="s-accent" x1="70" y1="70" x2="180" y2="130"></line><path class="s-ar-a" d="M171,123 l9,7 -1,-10 z"></path><text class="s-txt" x="44" y="70" text-anchor="middle" font-size="17">1</text><text class="s-txt" x="44" y="142" text-anchor="middle" font-size="17">2</text><text class="s-txt" x="208" y="70" text-anchor="middle" font-size="17">1</text><text class="s-txt" x="208" y="142" text-anchor="middle" font-size="17">2</text><text class="s-txt-m" x="125" y="182" text-anchor="middle" font-size="15">R</text></svg><figcaption>Отношение $R$ состоит из единственной пары, и на носителях оно взаимно однозначно. Пунктиром показана диагональ, то есть тождественный морфизм: композиция обратного отношения с $R$ до неё не дотягивает, поэтому изоморфизма нет.</figcaption></figure>

<figure class="mn"><svg viewBox="0 0 250 200" width="250" role="img" aria-label="Кобордизм: две окружности слева, одна справа, между ними поверхность-штаны; композиция — склейка по общей границе"><ellipse class="s-line" cx="34" cy="58" rx="13" ry="26"></ellipse><ellipse class="s-line" cx="34" cy="140" rx="13" ry="26"></ellipse><path class="s-line" d="M34,32 C90,32 108,66 130,66 C158,66 168,52 186,52"></path><path class="s-line" d="M34,84 C74,84 86,96 104,99"></path><path class="s-line" d="M34,114 C74,114 86,102 104,99"></path><path class="s-line" d="M34,166 C90,166 108,132 130,132 C158,132 168,146 186,146"></path><ellipse class="s-line" cx="186" cy="99" rx="13" ry="47"></ellipse><text class="s-txt-m" x="34" y="16" text-anchor="middle" font-size="14">две</text><text class="s-txt-m" x="186" y="24" text-anchor="middle" font-size="14">одна</text></svg><figcaption>Источник — две окружности, цель — одна, а морфизм есть сама поверхность между ними. Композиция кобордизмов есть склейка по общей границе; эта же картинка вернётся, когда на штанах окажется написано «умножение».</figcaption></figure>

<figure class="mn"><svg viewBox="0 0 250 200" width="250" role="img" aria-label="Тангл: три точки слева, три справа, морфизм — сплетение нитей; одна нить проходит под другой, поэтому в разрыве видно, какая сверху"><circle class="s-node-r" cx="34" cy="46" r="4"></circle><circle class="s-node-r" cx="34" cy="100" r="4"></circle><circle class="s-node-r" cx="34" cy="154" r="4"></circle><circle class="s-node-r" cx="216" cy="46" r="4"></circle><circle class="s-node-r" cx="216" cy="100" r="4"></circle><circle class="s-node-r" cx="216" cy="154" r="4"></circle><path class="s-line" d="M34,46 C86,46 112,100 164,100 C186,100 200,100 216,100"></path><path class="s-line" d="M34,100 C64,100 78,86 92,74"></path><path class="s-line" d="M110,60 C140,46 170,46 216,46"></path><path class="s-line" d="M34,154 C100,154 150,154 216,154"></path><text class="s-txt-m" x="34" y="24" text-anchor="middle" font-size="14">три</text><text class="s-txt-m" x="216" y="24" text-anchor="middle" font-size="14">три</text></svg><figcaption>Тангл: объект есть набор точек, морфизм есть сплетение нитей между двумя наборами. В разрыве видно, какая нить проходит снизу, и именно это отличает один морфизм от другого; композиция есть стыковка сплетений одного за другим.</figcaption></figure>

## Стрелка как следование и как шаг

> поле:mn **Раскладка.** Один экран: предпорядок как категория, дальше список. Справа два предпорядка на одном множестве и автомат.

**Предпорядок** $(X,\le)$ — категория: объекты — элементы, $\mathcal C(x,y)$ одноэлементно при $x\le y$ и пусто иначе; композиция и тождество единственны

Порядки: $\mathbf{Pos}$ · $\mathbb N$ с делимостью и с $\le$ — две разные категории · решётки · открытые множества с включением · высказывания с выводимостью

Комбинаторика: **свободная категория графа** — объекты вершины, морфизмы пути

Геометрия: $\mathbf{Cob}$ объекты — наборы окружностей, морфизмы — поверхности · косы и танглы: объекты — точки, морфизмы — сплетения

Шаг, а не соответствие: **конечные автоматы** — морфизм слово · **алгоритмы и правила вывода** — морфизм вычисление или правило

<figure class="mn"><svg viewBox="0 0 250 200" width="250" role="img" aria-label="Три элемента с петлями: от x к y стрелка идёт, а между x и z стрелки нет вовсе"><circle class="s-node-r" cx="66" cy="150" r="5"></circle><circle class="s-node-r" cx="66" cy="62" r="5"></circle><circle class="s-node" cx="190" cy="106" r="5"></circle><line class="s-accent" x1="66" y1="142" x2="66" y2="76"></line><path class="s-ar-a" d="M62,85 l4,-9 4,9 z"></path><path class="s-thin" d="M56,144 C40,138 40,124 54,120"></path><path class="s-thin" d="M56,56 C40,50 40,36 54,32"></path><path class="s-thin" d="M200,100 C216,94 216,80 202,76"></path><text class="s-txt" x="88" y="156" font-size="17">x</text><text class="s-txt" x="88" y="68" font-size="17">y</text><text class="s-txt" x="190" y="142" text-anchor="middle" font-size="17">z</text></svg><figcaption>Стрелка из $x$ в $y$ означает $x\le y$, и она единственна. Между $x$ и $z$ отношения нет, поэтому нет и стрелки; маленькие петли есть тождества, они существуют по рефлексивности.</figcaption></figure>

<figure><svg viewBox="0 0 620 180" width="620" role="img" aria-label="Слева числа один, два, три и шесть, соединённые по делимости: из единицы в двойку и в тройку, из двойки и тройки в шестёрку. Справа те же числа выстроены в цепочку по возрастанию"><circle class="s-node" cx="130" cy="140" r="5"></circle><circle class="s-node" cx="76" cy="90" r="5"></circle><circle class="s-node" cx="184" cy="90" r="5"></circle><circle class="s-node" cx="130" cy="40" r="5"></circle><line class="s-thin" x1="124" y1="134" x2="82" y2="96"></line><path class="s-ar-m" d="M87,94 l-9,-3 3,9 z"></path><line class="s-thin" x1="136" y1="134" x2="178" y2="96"></line><path class="s-ar-m" d="M173,94 l9,-3 -3,9 z"></path><line class="s-thin" x1="82" y1="84" x2="124" y2="46"></line><path class="s-ar-m" d="M119,44 l9,-3 -3,9 z"></path><line class="s-thin" x1="178" y1="84" x2="136" y2="46"></line><path class="s-ar-m" d="M141,44 l-9,-3 3,9 z"></path><text class="s-txt" x="130" y="166" text-anchor="middle" font-size="17">1</text><text class="s-txt" x="54" y="96" text-anchor="middle" font-size="17">2</text><text class="s-txt" x="206" y="96" text-anchor="middle" font-size="17">3</text><text class="s-txt" x="130" y="28" text-anchor="middle" font-size="17">6</text><text class="s-txt-m" x="266" y="96" text-anchor="middle" font-size="17">a | b</text><circle class="s-node" cx="374" cy="90" r="5"></circle><circle class="s-node" cx="444" cy="90" r="5"></circle><circle class="s-node" cx="514" cy="90" r="5"></circle><circle class="s-node" cx="584" cy="90" r="5"></circle><line class="s-thin" x1="382" y1="90" x2="436" y2="90"></line><path class="s-ar-m" d="M427,86 l9,4 -9,4 z"></path><line class="s-thin" x1="452" y1="90" x2="506" y2="90"></line><path class="s-ar-m" d="M497,86 l9,4 -9,4 z"></path><line class="s-thin" x1="522" y1="90" x2="576" y2="90"></line><path class="s-ar-m" d="M567,86 l9,4 -9,4 z"></path><text class="s-txt" x="374" y="122" text-anchor="middle" font-size="17">1</text><text class="s-txt" x="444" y="122" text-anchor="middle" font-size="17">2</text><text class="s-txt" x="514" y="122" text-anchor="middle" font-size="17">3</text><text class="s-txt" x="584" y="122" text-anchor="middle" font-size="17">6</text><text class="s-txt-m" x="326" y="96" text-anchor="middle" font-size="17">≤</text></svg><figcaption>Одни и те же четыре числа, два разных отношения, две разные категории. По делимости двойка и тройка несравнимы, и стрелки между ними нет ни в одну сторону; по возрастанию все объекты выстраиваются в цепочку. Категория задаётся не объектами, а стрелками.</figcaption></figure>

<figure class="mn"><svg viewBox="0 0 250 200" width="250" role="img" aria-label="Три состояния автомата, соединённые стрелками; над стрелками стоят буквы входного слова, обратного хода нет"><circle class="s-node-r" cx="44" cy="60" r="5"></circle><circle class="s-node" cx="164" cy="60" r="5"></circle><circle class="s-node-a" cx="164" cy="146" r="5"></circle><line class="s-accent" x1="52" y1="60" x2="156" y2="60"></line><path class="s-ar-a" d="M147,56 l9,4 -9,4 z"></path><line class="s-accent" x1="164" y1="68" x2="164" y2="138"></line><path class="s-ar-a" d="M160,129 l4,9 4,-9 z"></path><path class="s-thin" d="M44,74 C60,140 100,166 156,152"></path><path class="s-ar-m" d="M147,148 l9,4 -8,5 z"></path><text class="s-txt-m" x="104" y="44" text-anchor="middle" font-size="15">a</text><text class="s-txt-m" x="180" y="108" font-size="15">b</text><text class="s-txt-m" x="96" y="132" text-anchor="middle" font-size="15">ab</text><text class="s-txt" x="30" y="80" text-anchor="middle" font-size="17">q</text></svg><figcaption>Состояния служат объектами, а морфизмом идёт слово, переводящее одно состояние в другое. Композиция есть приписывание слов: буква $a$, затем буква $b$, и весь путь помечен словом $ab$. Обратного слова обычно нет, и это содержание примера, а не его дефект.</figcaption></figure>

## Функторы

> поле:mn **Раскладка.** Список вскрывается двумя порциями. Справа три ступени забывания и дифференциал. **Слито из двух разделов:** «Функторы» и «Зоопарк функторов» были двумя слайдами про одно и то же; экзотика зоопарка снята по критерию понятности, уцелевшая строка приехала сюда последней, реплика-мостик — за ней.

Забывание: $\mathbf{Ab}\to\mathbf{Grp}$ свойство · $\mathbf{Grp}\to\mathbf{Set}$ структуру · $\mathbf{Set}^2\to\mathbf{Set}$ материал

**Цепное правило** — матрица Якоби: без языка категорий у самого школьного утверждения нет имени

{@2} Фундаментальная группа $\pi_1$ · называния: гомоморфизм, монотонное отображение, $G$-множество, представление

{@2} Функтор $\mathbf{Cob}_2\to\mathbf{Vect}$, согласованный с $\sqcup$, называется **топологической теорией поля**

{@2} Функтор из свободной категории графа в $\mathbf{Vect}$ называется **представлением колчана**

{@2} $\mathbf{Mat}\simeq\mathbf{Vect}^{\mathrm{fd}}$ · $\mathbf{FinBool}\simeq\mathbf{FinSet}^{\mathrm{op}}$

<figure class="mn"><svg viewBox="0 0 250 200" width="250" role="img" aria-label="Столбик из трёх категорий: абелевы группы, группы, множества, соединённые стрелками сверху вниз; сбоку стоят пары множеств, и от них стрелка тоже ведёт в множества"><text class="s-txt" x="70" y="40" text-anchor="middle" font-size="17">Ab</text><text class="s-txt" x="70" y="112" text-anchor="middle" font-size="17">Grp</text><text class="s-txt" x="70" y="184" text-anchor="middle" font-size="17">Set</text><text class="s-txt" x="200" y="112" text-anchor="middle" font-size="17">Set²</text><line class="s-thin" x1="70" y1="52" x2="70" y2="94"></line><path class="s-ar-m" d="M66,85 l4,9 4,-9 z"></path><line class="s-thin" x1="70" y1="124" x2="70" y2="166"></line><path class="s-ar-m" d="M66,157 l4,9 4,-9 z"></path><line class="s-dash" x1="192" y1="124" x2="106" y2="172"></line><path class="s-ar-a" d="M115,171 l-10,3 4,-9 z"></path></svg><figcaption>Три ступени забывания различаются тем, что именно забыто: свойство коммутативности, вся операция или сам материал, из которого объект собран. Ступень читается по свойствам функтора, а не на глаз.</figcaption></figure>

<figure class="mn"><svg viewBox="0 0 250 200" width="250" role="img" aria-label="Гладкое отображение переводит точку в точку, а его дифференциал переводит касательную плоскость в касательную плоскость"><circle class="s-line" cx="62" cy="126" r="38"></circle><circle class="s-line" cx="188" cy="126" r="38"></circle><line class="s-accent" x1="22" y1="88" x2="102" y2="88"></line><line class="s-accent" x1="148" y1="88" x2="228" y2="88"></line><circle class="s-node-r" cx="62" cy="88" r="4"></circle><circle class="s-node-r" cx="188" cy="88" r="4"></circle><line class="s-thin" x1="108" y1="126" x2="142" y2="126"></line><path class="s-ar-m" d="M133,122 l9,4 -9,4 z"></path><line class="s-dash" x1="108" y1="66" x2="142" y2="66"></line><path class="s-ar-a" d="M133,62 l9,4 -9,4 z"></path><text class="s-txt-m" x="125" y="148" text-anchor="middle" font-size="15">f</text><text class="s-txt-m" x="125" y="56" text-anchor="middle" font-size="15">Df</text><text class="s-txt" x="50" y="80" text-anchor="end" font-size="15">a</text><text class="s-txt" x="200" y="80" font-size="15">f(a)</text></svg><figcaption>Внизу гладкое отображение переводит точку в точку, наверху дифференциал переводит касательную плоскость в касательную плоскость. Два отображения подряд дают наверху произведение матриц, и это равенство есть цепное правило.</figcaption></figure>

> поле:mn **Реплика (не слайд).** Лектор произносит мостик в следующую вкладку: мы назвали десяток функторов, а вот эта конструкция функтором не оказывается, и эта тоже. А как такое вообще доказывают?
