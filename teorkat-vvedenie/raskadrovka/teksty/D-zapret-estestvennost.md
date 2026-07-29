---
tab: D. Запрет первый: естественность
status: chernovik
poryadok: 3
registr: читаемый
---

# Блок D. Запрет первый — естественность

> поле:mn **Что это.** Тексты слайдов лекции 1 в том объёме, в котором они лягут на слайд, собранные лентой. Каждый раздел ниже = ОДИН слайд. Сцены несёт сама лента: `{@N}` — приходит с $N$-й сцены, `{@N-M}` — приходит на $N$-й и уходит после $M$-й. Бюджет — на СЦЕНУ, не на слайд.

## Ответ снова «ни одного»

> поле:mn **Раскладка.** Много текста, квадрат на правой полосе, на всех сценах. Квадрат тот же, что задавал требование красоты, и здесь он впервые работает орудием.

> поле:mn **Вёрстка.** Осиротела иллюстрация с корнями $\pm i$: разбор выкинут по бюджету.

{@1-2} **Есть ли естественный изоморфизм $\mathrm{Id}\Rightarrow(-)^{\ast}$ на $\mathcal V$?**

**Теорема.** Если в поле есть обратимый $\lambda$ с $\lambda^2\ne1$, то на группоиде $\mathcal V$ конечномерных пространств естественного изоморфизма $\mathrm{Id}\Rightarrow(-)^{\ast}$ не существует

{@2} $f=\lambda\,\mathrm{id}_V$ умножает $V$ на $\lambda$, а $V^{\ast}$ — на $\lambda^{-1}$

{@2} Компонента $\alpha_V\colon V\to V^{\ast}$, квадрат на $v$: $\lambda\,\alpha_V(v)=\lambda^{-1}\alpha_V(v)$ · $(\lambda^2-1)\,\alpha_V(v)=0$ ⇒ $\alpha_V=0$, при $V\ne0$ не изоморфизм

{@2} $V^{\ast\ast}$: та же подстановка $\lambda\,\eta_V=\lambda\,\eta_V$ — препятствия нет; $\eta_V(v)=(\psi\mapsto\psi(v))$ формулой

<figure class="mn">
<svg viewBox="0 0 200 200" width="200" role="img" aria-label="Две одинаковые белые точки на вертикальной оси, симметричные относительно горизонтальной оси; верхняя помечена i, нижняя помечена минус i">
<line class="s-dash" x1="24" y1="100" x2="176" y2="100"/>
<line class="s-thin" x1="100" y1="24" x2="100" y2="176"/>
<circle class="s-node" cx="100" cy="48" r="5.4"/>
<circle class="s-node" cx="100" cy="152" r="5.4"/>
<text class="s-txt" x="114" y="45">i</text>
<text class="s-txt" x="114" y="158">−i</text>
<text class="s-txt-m" x="90" y="114" text-anchor="end">0</text>
</svg>
<figcaption>Оба корня лежат на мнимой оси симметрично вещественной, и по своим свойствам они неотличимы: узлы нарисованы одинаковыми намеренно. Отметить один из них можно только произволом.</figcaption>
</figure>

<figure class="mn">
<svg viewBox="0 0 200 190" width="200" role="img" aria-label="Сверху пространство, снизу его двойственное, между ними три одинаковые пунктирные стрелки; у правой стоит метка скалярного произведения">
<text class="s-txt" x="100" y="42" text-anchor="middle" font-size="17">V</text>
<text class="s-txt" x="100" y="168" text-anchor="middle" font-size="17">V*</text>
<line class="s-dash" x1="70" y1="58" x2="70" y2="140"/>
<path class="s-ar-a" d="M66,131 l4,9 4,-9 z"/>
<line class="s-dash" x1="100" y1="58" x2="100" y2="140"/>
<path class="s-ar-a" d="M96,131 l4,9 4,-9 z"/>
<line class="s-dash" x1="130" y1="58" x2="130" y2="140"/>
<path class="s-ar-a" d="M126,131 l4,9 4,-9 z"/>
<text class="s-txt-m" x="140" y="103" font-size="12">⟨v,−⟩</text>
</svg>
<figcaption>Изоморфизмов $V\to V^{\ast}$ много: каждое скалярное произведение даёт свой, и ни один из них не выделен. Пунктир стоит там, где стрелка не построена, а выбрана.</figcaption>
</figure>

<figure class="mn"><svg viewBox="0 0 250 200" width="250" role="img" aria-label="Квадрат естественности с подставленным обратимым скаляром: сверху умножение на лямбда, снизу на обратную лямбда, поэтому квадрат не сходится"><text class="s-txt" x="52" y="34" text-anchor="middle" font-size="17">V</text><text class="s-txt" x="198" y="34" text-anchor="middle" font-size="17">V</text><text class="s-txt" x="52" y="178" text-anchor="middle" font-size="17">V*</text><text class="s-txt" x="198" y="178" text-anchor="middle" font-size="17">V*</text><line class="s-thin" x1="70" y1="29" x2="180" y2="29"></line><path class="s-ar-m" d="M171,25 l9,4 -9,4 z"></path><line class="s-thin" x1="74" y1="173" x2="176" y2="173"></line><path class="s-ar-m" d="M167,169 l9,4 -9,4 z"></path><line class="s-thin" x1="52" y1="48" x2="52" y2="152"></line><path class="s-ar-m" d="M48,143 l4,9 4,-9 z"></path><line class="s-thin" x1="198" y1="48" x2="198" y2="152"></line><path class="s-ar-m" d="M194,143 l4,9 4,-9 z"></path><text class="s-txt-m" x="125" y="18" text-anchor="middle" font-size="15">·λ</text><text class="s-txt-m" x="125" y="196" text-anchor="middle" font-size="15">·λ⁻¹</text><text class="s-txt-m" x="44" y="105" text-anchor="end" font-size="15">η</text><text class="s-txt-m" x="206" y="105" font-size="15">η</text><text class="s-txt-m" x="125" y="108" text-anchor="middle" font-size="14">λ ≠ λ⁻¹</text></svg><figcaption>Тот же квадрат, что задавал определение, впервые служит орудием: в него подставлена обратимая стрелка объекта в себя. Наверху растяжение умножает на $\lambda$, внизу, на двойственном, — на $\lambda^{-1}$; центральная метка называет требование, которое из этого выходит: $\lambda\ne\lambda^{-1}$, то есть в поле нужен обратимый $\lambda$ с $\lambda^2\ne1$.</figcaption></figure>

## Ответ не нуль: центр и степени

> поле:mn **Раскладка.** Много текста, квадрат на правой полосе: у группы с одним объектом все четыре угла совпали.

**Утверждение.** Для группы $G$, взятой как категория $BG$ с одним объектом, естественные преобразования $\mathrm{Id}\Rightarrow\mathrm{Id}$ находятся в биекции с центром $Z(G)$

{@2} **Утверждение.** Для забывающего функтора $U\colon\mathbf{Grp}\to\mathbf{Set}$ естественные преобразования $U\Rightarrow U$ находятся в биекции с $\mathbb Z$: это в точности $x\mapsto x^n$

<figure class="mn"><svg viewBox="0 0 250 200" width="250" role="img" aria-label="Тот же квадрат, у которого все четыре угла — один и тот же объект: сверху и снизу элемент группы, слева и справа компонента преобразования, в центре условие перестановочности"><text class="s-txt" x="52" y="34" text-anchor="middle" font-size="17">∗</text><text class="s-txt" x="198" y="34" text-anchor="middle" font-size="17">∗</text><text class="s-txt" x="52" y="178" text-anchor="middle" font-size="17">∗</text><text class="s-txt" x="198" y="178" text-anchor="middle" font-size="17">∗</text><line class="s-thin" x1="66" y1="29" x2="184" y2="29"></line><path class="s-ar-m" d="M175,25 l9,4 -9,4 z"></path><line class="s-thin" x1="66" y1="173" x2="184" y2="173"></line><path class="s-ar-m" d="M175,169 l9,4 -9,4 z"></path><line class="s-thin" x1="52" y1="48" x2="52" y2="152"></line><path class="s-ar-m" d="M48,143 l4,9 4,-9 z"></path><line class="s-thin" x1="198" y1="48" x2="198" y2="152"></line><path class="s-ar-m" d="M194,143 l4,9 4,-9 z"></path><text class="s-txt-m" x="125" y="18" text-anchor="middle" font-size="15">g</text><text class="s-txt-m" x="125" y="196" text-anchor="middle" font-size="15">g</text><text class="s-txt-m" x="44" y="105" text-anchor="end" font-size="15">x</text><text class="s-txt-m" x="206" y="105" font-size="15">x</text><text class="s-txt-m" x="125" y="108" text-anchor="middle" font-size="14">xg = gx</text></svg><figcaption>У группы, взятой категорией, объект один, поэтому все четыре угла квадрата совпадают: остаются два элемента и требование, чтобы они перестановочны были. Ответ на категорный вопрос оказывается школьной алгебраической мелочью.</figcaption></figure>

## Остальные ответы и граф как функтор

> поле:mn **Раскладка.** Вертикальная полоса справа: треугольник и палитра, со сцены 2. Первая сцена идёт без картинки — список зал пробегает сам.

{@1-2} **Классификационные результаты, списком**

{@1-2} Функторы в предупорядоченное множество: преобразований не более одного · $A\times B\Rightarrow A$: в точности проекции · $G\times G\Rightarrow G$: биекция со свободной группой $F_2$

{@2} Категория $\mathcal J$: объекты $E$, $V$ и морфизмы $s,t\colon E\to V$. Функтор $\mathcal J\to\mathbf{Set}$ — в точности ориентированный граф

{@2} **Теорема.** Естественные преобразования графа $G$ в полный граф $K_k$ — в точности правильные раскраски $G$ в $k$ цветов, а их число — хроматический многочлен $P(G,k)$

{@2} **Сколько правильных раскрасок у треугольника в $k$ цветов?**

<figure class="mn">
<svg viewBox="0 0 200 220" width="200" role="img" aria-label="Треугольник из трёх вершин и трёх рёбер; все три вершины закрашены по-разному. Ниже палитра из трёх клеток">
<line class="s-line" x1="100" y1="42" x2="42" y2="146"/>
<line class="s-line" x1="100" y1="42" x2="158" y2="146"/>
<line class="s-line" x1="42" y1="146" x2="158" y2="146"/>
<circle class="s-node-r" cx="100" cy="42" r="6"/>
<circle class="s-node-a" cx="42" cy="146" r="6"/>
<circle class="s-node" cx="158" cy="146" r="6"/>
<rect class="s-fillsh" x="52" y="168" width="20" height="20"/>
<rect class="s-fillw" x="90" y="168" width="20" height="20"/>
<rect class="s-line" x="128" y="168" width="20" height="20"/>
<text class="s-txt-m" x="100" y="202" text-anchor="middle">K₃</text>
</svg>
<figcaption>Три вершины треугольника попарно смежны, поэтому каждая обязана получить свой цвет, и раскраска в три цвета есть в точности нумерация вершин палитрой. Клетки внизу — сама палитра, то есть вершины полного графа.</figcaption>
</figure>
