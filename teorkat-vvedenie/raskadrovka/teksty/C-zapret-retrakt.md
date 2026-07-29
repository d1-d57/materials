---
tab: C. Запрет второй: Брауэр
status: chernovik
poryadok: 4
registr: читаемый
---

# Блок C. Запрет второй — Брауэр

> поле:mn **Что это.** Тексты слайдов лекции 1 в том объёме, в котором они лягут на слайд, собранные лентой. Каждый раздел ниже = ОДИН слайд. Сцены несёт сама лента: `{@N}` — приходит с $N$-й сцены, `{@N-M}` — приходит на $N$-й и уходит после $M$-й. Бюджет — на СЦЕНУ, не на слайд.

## Откуда взялся этот язык

> поле:mn **Раскладка.** Один экран, одна сцена: список слева, два портрета столбиком и хронология таблицей справа.

{@1} **Этот язык — побочный продукт другого вопроса: что значит «конструкция задана единообразно»**

{@1} Эйленберг и Маклейн, топологи

{@1} Порядок понятий: естественность, затем функтор, затем категория

{@1} **Отсюда два сюжета этой части: $V$ и $V^{\ast}$, затем Брауэр**

🖼 Портрет Сэмюэла Эйленберга {1} · 🖼 Портрет Сондерса Маклейна {1}

<table>
<thead><tr><th>год</th><th>что появилось</th></tr></thead>
<tbody>
<tr><td>1942</td><td>«Natural isomorphisms in group theory»: функтор и естественный изоморфизм; слова «категория» нет</td></tr>
<tr><td>1945</td><td>категория и естественное преобразование</td></tr>
</tbody>
</table>

## Как доказывают, что функтора нет

> поле:mn **Раскладка.** Текстовая область — на всю ширину, коммутативная диаграмма ложится горизонтальной полосой снизу (правка 20.2).

> поле:mn **Вёрстка.** Осиротели две иллюстрации, обе оставлены в файле нетронутыми. (1) «Носитель против палитры»: текста под неё на ленте нет (пример с инъекциями выкинут по бюджету), но сама задача про инъекции уходит в лист упражнений — картинка может уехать туда вместе с ней, решение за аналитиком. (2) На следующем слайде схема $FX\to FY$ — по-прежнему без своего текста: либо снимается, либо ей нужен текст, которого в источнике нет.

**Утверждение.** Сопоставление $G\mapsto Z(G)$ не продолжается до функтора $\mathbf{Grp}\to\mathbf{Grp}$

{@1-2} $Z(G)=\{z\in G:\ zg=gz\ \ \forall g\in G\}$

{@2} Рассмотрим группу $\mathbb Z_2$ и отображения $s\colon\mathbb Z_2\to S_3$ и $\mathrm{sgn}$, где $s(0)=e$, $s(1)=(1\,2)$

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

## Брауэр в работе

> поле:mn **Раскладка.** Мало текста, вертикальная полоса справа: окружность в диске и луч внутри диска с портретом (правка владельца 29.07 — нижнюю полоску снять, полосу сделать вертикальной).

**Теорема Брауэра.** В топологических пространствах нет ретракции из диска в $S^1$

{@1-2} Предположим, что ретракция есть. Рассмотрим функтор $\pi_1$: $\pi_1(S^1)=\mathbb Z$, $\pi_1(D^2)=e$

{@2} Тогда была бы коммутативная диаграмма $\mathbb Z\to\{e\}\to\mathbb Z$, которой быть не может

🖼 Портрет Лёйтзена Брауэра {1}

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
