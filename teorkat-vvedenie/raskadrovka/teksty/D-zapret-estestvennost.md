---
tab: D. Запрет первый: естественность
status: chernovik
poryadok: 3
registr: читаемый
---

# Блок D. Запрет первый — естественность

> поле:mn **Что это.** Тексты слайдов лекции 1 в том объёме, в котором они лягут на слайд, собранные лентой. Каждый раздел ниже = ОДИН слайд. Сцены несёт сама лента: `{@N}` — приходит с $N$-й сцены, `{@N-M}` — приходит на $N$-й и уходит после $M$-й. Бюджет — на СЦЕНУ, не на слайд.

## Ответ снова «ни одного»

> поле:mn **Раскладка.** Много текста, вертикальная полоса справа: квадрат с подставленным скаляром, на всех сценах. Квадрат тот же, что задавал требование красоты, и здесь он впервые работает орудием. *Правка владельца 29.07: первая и вторая картинки сверху сняты (корни $\pm i$ — лента сама звала её осиротевшей; изоморфизмы $V\to V^{\ast}$ пунктиром), осталась только нижняя.*

{@1-2} **Есть ли естественный изоморфизм $\mathrm{Id}\Rightarrow(-)^{\ast}$ на $\mathcal V$?**

**Теорема.** Если в поле есть обратимый $\lambda$ с $\lambda^2\ne1$, то на группоиде $\mathcal V$ конечномерных пространств естественного изоморфизма $\mathrm{Id}\Rightarrow(-)^{\ast}$ не существует

{@2} $f=\lambda\,\mathrm{id}_V$ умножает $V$ на $\lambda$, а $V^{\ast}$ — на $\lambda^{-1}$

{@2} Компонента $\alpha_V\colon V\to V^{\ast}$, квадрат на $v$: $\lambda\,\alpha_V(v)=\lambda^{-1}\alpha_V(v)$ · $(\lambda^2-1)\,\alpha_V(v)=0$ ⇒ $\alpha_V=0$, при $V\ne0$ не изоморфизм

{@2} $V^{\ast\ast}$: та же подстановка $\lambda\,\eta_V=\lambda\,\eta_V$ — препятствия нет; $\eta_V(v)=(\psi\mapsto\psi(v))$ формулой

<figure class="mn"><svg viewBox="0 0 250 200" width="250" role="img" aria-label="Квадрат естественности с подставленным обратимым скаляром: сверху умножение на лямбда, снизу на обратную лямбда, поэтому квадрат не сходится"><text class="s-txt" x="52" y="34" text-anchor="middle" font-size="17">V</text><text class="s-txt" x="198" y="34" text-anchor="middle" font-size="17">V</text><text class="s-txt" x="52" y="178" text-anchor="middle" font-size="17">V*</text><text class="s-txt" x="198" y="178" text-anchor="middle" font-size="17">V*</text><line class="s-thin" x1="70" y1="29" x2="180" y2="29"></line><path class="s-ar-m" d="M171,25 l9,4 -9,4 z"></path><line class="s-thin" x1="74" y1="173" x2="176" y2="173"></line><path class="s-ar-m" d="M167,169 l9,4 -9,4 z"></path><line class="s-thin" x1="52" y1="48" x2="52" y2="152"></line><path class="s-ar-m" d="M48,143 l4,9 4,-9 z"></path><line class="s-thin" x1="198" y1="48" x2="198" y2="152"></line><path class="s-ar-m" d="M194,143 l4,9 4,-9 z"></path><text class="s-txt-m" x="125" y="18" text-anchor="middle" font-size="15">·λ</text><text class="s-txt-m" x="125" y="196" text-anchor="middle" font-size="15">·λ⁻¹</text><text class="s-txt-m" x="44" y="105" text-anchor="end" font-size="15">η</text><text class="s-txt-m" x="206" y="105" font-size="15">η</text><text class="s-txt-m" x="125" y="108" text-anchor="middle" font-size="14">λ ≠ λ⁻¹</text></svg><figcaption>Тот же квадрат, что задавал определение, впервые служит орудием: в него подставлена обратимая стрелка объекта в себя. Наверху растяжение умножает на $\lambda$, внизу, на двойственном, — на $\lambda^{-1}$; центральная метка называет требование, которое из этого выходит: $\lambda\ne\lambda^{-1}$, то есть в поле нужен обратимый $\lambda$ с $\lambda^2\ne1$.</figcaption></figure>

## Ответ не нуль: центр и степени

> поле:mn **Раскладка.** Много текста, квадрат на правой полосе: у группы с одним объектом все четыре угла совпали.

**Утверждение.** Для группы $G$, взятой как категория $BG$ с одним объектом, естественные преобразования $\mathrm{Id}\Rightarrow\mathrm{Id}$ находятся в биекции с центром $Z(G)$

{@2} **Утверждение.** Для забывающего функтора $U\colon\mathbf{Grp}\to\mathbf{Set}$ естественные преобразования $U\Rightarrow U$ находятся в биекции с $\mathbb Z$: это в точности $x\mapsto x^n$

<figure class="mn"><svg viewBox="0 0 250 200" width="250" role="img" aria-label="Тот же квадрат, у которого все четыре угла — один и тот же объект: сверху и снизу элемент группы, слева и справа компонента преобразования, в центре условие перестановочности"><text class="s-txt" x="52" y="34" text-anchor="middle" font-size="17">∗</text><text class="s-txt" x="198" y="34" text-anchor="middle" font-size="17">∗</text><text class="s-txt" x="52" y="178" text-anchor="middle" font-size="17">∗</text><text class="s-txt" x="198" y="178" text-anchor="middle" font-size="17">∗</text><line class="s-thin" x1="66" y1="29" x2="184" y2="29"></line><path class="s-ar-m" d="M175,25 l9,4 -9,4 z"></path><line class="s-thin" x1="66" y1="173" x2="184" y2="173"></line><path class="s-ar-m" d="M175,169 l9,4 -9,4 z"></path><line class="s-thin" x1="52" y1="48" x2="52" y2="152"></line><path class="s-ar-m" d="M48,143 l4,9 4,-9 z"></path><line class="s-thin" x1="198" y1="48" x2="198" y2="152"></line><path class="s-ar-m" d="M194,143 l4,9 4,-9 z"></path><text class="s-txt-m" x="125" y="18" text-anchor="middle" font-size="15">g</text><text class="s-txt-m" x="125" y="196" text-anchor="middle" font-size="15">g</text><text class="s-txt-m" x="44" y="105" text-anchor="end" font-size="15">x</text><text class="s-txt-m" x="206" y="105" font-size="15">x</text><text class="s-txt-m" x="125" y="108" text-anchor="middle" font-size="14">xg = gx</text></svg><figcaption>У группы, взятой категорией, объект один, поэтому все четыре угла квадрата совпадают: остаются два элемента и требование, чтобы они перестановочны были. Ответ на категорный вопрос оказывается школьной алгебраической мелочью.</figcaption></figure>

## Остальные ответы и граф как функтор

> поле:mn **Раскладка.** Полоса справа пустая — иллюстраций у слайда нет, список зал пробегает сам. *Правка владельца 29.07: иллюстрация с хроматическим многочленом (треугольник и палитра) снята, полоса убрана.*

{@1-2} **Классификационные результаты, списком**

{@1-2} Функторы в предупорядоченное множество: преобразований не более одного · $A\times B\Rightarrow A$: в точности проекции · $G\times G\Rightarrow G$: биекция со свободной группой $F_2$

{@2} Категория $\mathcal J$: объекты $E$, $V$ и морфизмы $s,t\colon E\to V$. Функтор $\mathcal J\to\mathbf{Set}$ — в точности ориентированный граф

{@2} **Теорема.** Естественные преобразования графа $G$ в полный граф $K_k$ — в точности правильные раскраски $G$ в $k$ цветов, а их число — хроматический многочлен $P(G,k)$

{@2} **Сколько правильных раскрасок у треугольника в $k$ цветов?**

