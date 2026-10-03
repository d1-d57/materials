# Картинка к осенней контрольной — промпт для ChatGPT

**Как устроены картинки прошлых контрольных.** Чёрная линейная графика на белом фоне, внизу страницы, шириной примерно в половину листа:
- весной — полевые цветы тонким пером, как ботаническая гравюра;
- зимой — два снеговика карандашом.

Цвета нет, текста нет, лист печатается на ч/б принтере.

**Замысел.** Осеннее дерево, которое оказывается деревом и в смысле теории графов.
- Ветки — рёбра, развилки — отчётливые кружки-вершины.
- Ветки нигде не срастаются обратно, то есть циклов нет.
- На концах веток висят листья. Это скрытая шутка: висячие вершины — буквально листья.
- Несколько листьев падают.
- Внизу сидит ёжик с жёлудем.
- Мотив ветвей — спирали «Древа жизни» Климта, но в чёрно-белой графике.

## Промпт (вставить в ChatGPT целиком)

```
Black-and-white pen-and-ink illustration on a pure white background, in the style of a delicate botanical engraving / fine line drawing (like a vintage book illustration), no colour, no grey wash, no text, no frame. Landscape format, about 3:2.

Subject: an autumn tree that is secretly a mathematical tree (a graph without cycles). The trunk splits into branches again and again; every branching point is marked by a small clear solid black dot, and every branch is a smooth line from one dot to the next. Branches NEVER grow back together or touch each other — there are no loops anywhere in the crown. The branches curl into elegant spirals, inspired by Gustav Klimt's "Tree of Life", but drawn only with clean black lines.

At the tip of every outermost branch hangs exactly one leaf — maple and oak leaves, drawn with fine veins. A few leaves are falling, drifting down to the ground; two or three acorns lie on the ground. At the foot of the tree a small hedgehog sits, holding an acorn, drawn in the same fine-line style.

Composition: the tree centred, slightly asymmetric, lots of white space, light and airy, suitable for printing at the bottom of an A4 exam sheet on a black-and-white laser printer. Thin, even line weight; no heavy shading, no solid black areas except the small dots at the branching points.
```

## Если вышло не то — короткие поправки

- **Ветки срослись в кольца:** «Remove every loop: no two branches may touch or reconnect; it must be a tree graph.»
- **Вершины не читаются:** «Make the dots at every branching point clearly visible, the same size, slightly larger.»
- **Слишком тёмно или с тенями:** «Pure line art, no shading, no grey, no hatching, white background.»
- **Климт превратился в золото и орнамент:** «Keep only the spiral shape of the branches, no gold, no decorative patterns.»
- **Нужен вариант проще:** вместо дерева — один кленовый лист, у которого прожилки нарисованы как дерево-граф с точками в развилках, и два жёлудя рядом.

## Как вставить в TeX

Сохранить как `figs/osen.png` и вставить в конец задач первой страницы (или в пустое место второй):

```
\begin{center}\includegraphics[width=.5\textwidth]{Listki/figs/osen.png}\end{center}
```

Вторая страница сейчас заполнена на треть — картинка помещается под «Трудными задачами».
