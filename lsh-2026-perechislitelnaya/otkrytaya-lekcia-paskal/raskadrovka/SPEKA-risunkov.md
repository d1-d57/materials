# СПЕКА рисунков лекции «Внутри треугольника Паскаля» (doc-вид)

Читать целиком. Отступать от неё нельзя — иначе 19 рисунков разъедутся в 19 стилей.

## Носитель
Инлайн-`<svg>` внутри `<figure>` в markdown-файле. Собирается `../disciplina/_generator/build_doc.py`.

## Жёсткие правила
1. **Цвет — ТОЛЬКО классом.** Никаких `stroke="black"`, никаких hex, никаких `style=`.
   Доступные классы (они определены в движке, других нет):
   `.s-line` (основная линия 2px) · `.s-thin` (вспомогательная 1.2px) ·
   `.s-dash` (пунктир акцентом — разрез/построение) · `.s-accent` (акцентная линия 2.4px) ·
   `.s-node` (узел белый с обводкой) · `.s-node-r` (узел залитый — «тот, о ком речь») ·
   `.s-node-a` (узел акцентный) · `.s-fillw` / `.s-fillsh` (заливки) ·
   `.s-txt` (метка 13px) · `.s-txt-m` (метка мелкая приглушённая 12px) ·
   `.s-ar-a` / `.s-ar-m` (стрелки).
2. **Внутри рисунка — только МЕТКА: число, координата, одна буква.** Ни одного слова, ни одного
   пояснения, ни подписей осей. Слова идут в `<figcaption>` под рисунком. Это главное правило
   фабрики и самое нарушаемое. Смысл несёт графика: залитый узел = «вот этот»,
   `.s-accent` = «вот что изменилось», пунктир = построение.
3. **Меток по минимуму.** Если смысл виден без числа — числа не ставить.
4. `viewBox` обязателен, `width` в атрибуте, `role="img"`, `aria-label` человеческим языком.
5. **Пропорция решает место:** высота/ширина **< 0,6** → рисунок в поток (делай горизонтальным);
   **≥ 0,6** → уедет на правое поле (делай узким, вытянутым вверх). Реши ДО рисования.
6. **Сетка:** шаг по x 30–36px, по y 22–26px, узел `r="3.4"`. Поля от края viewBox ≥ 18px.
   Строки «до → после» — вторым рядом ниже, шаг между рядами 90px.
7. **Центрируй предмет рисунка**, а не служебные подписи.
8. Никаких `id`, `marker`, `defs`, `clipPath` — несколько SVG в одном документе делят
   пространство имён и тихо ломают друг друга.

## ЭТАЛОН СТИЛЯ — скопируй манеру отсюда

Разрез пути по центру: путь длины 8 с пунктирной вертикалью посередине, вторая половина
акцентом; ниже — два пути длины 4, оба кончаются на одной высоте (тонкая пунктирная
горизонталь показывает это без единого слова).

```svg
<svg viewBox="0 0 360 200" width="620" role="img" aria-label="Путь длины восемь разрезан посередине; вторая половина перевёрнута, получились два пути длины четыре, оба кончающиеся на одной высоте">
<line class="s-thin" x1="54" y1="80" x2="306" y2="80" stroke-dasharray="5 4"/>
<line class="s-thin" x1="54" y1="36" x2="306" y2="36" stroke-dasharray="5 4"/>
<polyline class="s-line" points="60,80 90,58 120,36 150,58 180,36"/>
<polyline class="s-accent" points="180,36 210,58 240,80 270,58 300,80"/>
<line class="s-dash" x1="180" y1="18" x2="180" y2="98"/>
<circle class="s-node-a" cx="60" cy="80" r="3.4"/>
<circle class="s-node" cx="90" cy="58" r="3.4"/>
<circle class="s-node" cx="120" cy="36" r="3.4"/>
<circle class="s-node" cx="150" cy="58" r="3.4"/>
<circle class="s-node-r" cx="180" cy="36" r="3.4"/>
<circle class="s-node" cx="210" cy="58" r="3.4"/>
<circle class="s-node" cx="240" cy="80" r="3.4"/>
<circle class="s-node" cx="270" cy="58" r="3.4"/>
<circle class="s-node-a" cx="300" cy="80" r="3.4"/>
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
```

Обрати внимание: ноль слов внутри, ни одной цифры. Уровни показаны тонким пунктиром,
разрез — пунктиром акцентом, «что изменилось» — акцентной линией, «та самая точка» — заливкой узла.

## ОБЯЗАТЕЛЬНАЯ ПРОВЕРКА ГЛАЗАМИ (без неё работу не сдавать)

`cairosvg` не понимает CSS-классы и зальёт всё чёрным, соврав. Разверни классы в атрибуты и
посмотри PNG собственными глазами:

```python
import re, cairosvg, pathlib
M = {
 's-line':'fill="none" stroke="#211f1b" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"',
 's-thin':'fill="none" stroke="#726c60" stroke-width="1.2"',
 's-dash':'fill="none" stroke="#2f6e8e" stroke-width="1.3" stroke-dasharray="4 4"',
 's-accent':'fill="none" stroke="#2f6e8e" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"',
 's-node':'fill="#fbfaf6" stroke="#211f1b" stroke-width="1.5"',
 's-node-r':'fill="#211f1b" stroke="#211f1b" stroke-width="1.5"',
 's-node-a':'fill="#2f6e8e" stroke="#2f6e8e" stroke-width="1.5"',
 's-fillsh':'fill="#dfeaf0" stroke="#211f1b" stroke-width="1.5"',
 's-fillw':'fill="#f6ece2" stroke="#211f1b" stroke-width="1.5"',
 's-txt':'font-family="sans-serif" font-size="13" fill="#211f1b"',
 's-txt-m':'font-family="sans-serif" font-size="12" fill="#726c60"',
 's-txt-w':'font-family="sans-serif" font-size="13" fill="#fbfaf6"',
 # стрелки: наконечник — ЗАЛИТЫЙ треугольник (path с l9,4 -9,4 z), не обводка
 's-ar-m':'fill="#726c60" stroke="#726c60" stroke-width="1.2"',
 's-ar-a':'fill="#2f6e8e" stroke="#2f6e8e" stroke-width="1.2"',
}
s = pathlib.Path('X.svg').read_text()
# ВАЖНО: снять атрибут width — cairosvg масштабирует по нему и врёт про пропорцию
s = re.sub(r'\swidth="\d+"', '', s, count=1)
s = re.sub(r'class="([a-z0-9 -]+)"', lambda m: " ".join(M[c] for c in m.group(1).split()), s)
cairosvg.svg2png(bytestring=s.encode(), write_to='X.png', scale=2.2, background_color='#fbfaf6')
```

Потом **прочитай PNG инструментом Read и посмотри на него**. Проверь: ничего не наехало,
композиция не съехала вбок, пустоты по краям нет, всё читается без слов.
Плохо — переделай и посмотри снова. Сдавай только то, что сам увидел.

## Что сдать
Для каждого рисунка — готовый блок `<figure>…</figure>`: сам `<svg>` плюс `<figcaption>`
одной фразой (вот сюда идут все слова, которых нельзя внутри рисунка).
Верни блоки текстом в ответе, по порядку, с пометкой, к какому пункту задания какой относится.
