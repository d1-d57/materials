# Аватарка канала «Пути и волны» — концепции и промпты

Канал: t.me/puti_i_volny · «Методы перечислительной комбинаторики» · кружок 8–11 кл., школа 179.
Задача картинки: вау с первого взгляда, круглый кроп, читается в 40–50 px, красива в 640 px.

---

## 0. Текст на аватарке — не нужен

- Telegram и так пишет имя канала рядом с кружком; надпись дублирует его и съедает площадь у образа.
- В 40–50 px любая надпись превращается в серую полоску: ни «Пути и волны», ни «179» не читаются, а образ из-за них становится мельче.
- Генератор картинок до сих пор нестабильно пишет кириллицу (лишние/кривые буквы), а значит, надпись — это лишний цикл правок ради элемента, который всё равно не виден.
- Если позже понадобится «марка», это должен быть знак (точка в центре, одна ломаная), а не слова, и подставлять его лучше руками в редакторе, а не через генерацию.

---

## 1. Референсы (всё ниже открыто, кроме явно помеченного)

**Пути / перечисление**
1. Доска Гальтона — https://en.wikipedia.org/wiki/Galton_board — брать: штырьки в шахматном порядке, шарик отскакивает влево/вправо, а наложенный на штырьки треугольник Паскаля считает пути к каждой корзине; «веер ветвлений», который сам собирается в колокол.
2. Треугольник Паскаля по модулю 2 = Серпинский — https://jwilson.coe.uga.edu/EMAT6680/Parsons/MVP6690/Essay1/sierpinski.html — брать: самоподобие «треугольники в треугольниках» как скрытая структура обычных биномиальных коэффициентов (вариант заполнения внутри веера).
3. Пути Дика — https://scipython.com/blog/dyck-paths-and-catalan-numbers — брать: путь из ступенек `/` и `\`, который не опускается ниже стартовой высоты, буквально рисуется как горный профиль.
4. Генеративное ветвление (inconvergent, «fractures») — https://inconvergent.net/generative/fractures/ — брать: ветвящиеся сети, плотнее у источника и реже к краю; плотность ветвей как композиционный приём (без копирования вида).

**Волны / спектр**
5. Фигуры Хладни (APS) — https://www.aps.org/apsnews/2017/07/first-experiments-chladni-figures — брать: песок на вибрирующей пластине собирается на узловых линиях и показывает моду колебания.
6. Фигуры Хладни (Toronto, нелинейная физика) — https://www.physics.utoronto.ca/~nonlin/chladni.html — брать: на круглой пластине — радиальные «спицы» (10 и 14 спиц), на квадратной — четырёхкратная симметрия; песок сбрасывается с движущихся участков и копится в узлах.
7. Интерференция двух источников в волновой ванне (IOP) — https://spark.iop.org/interference-two-sources-using-vibrators — брать: изогнутые узловые линии, расходящиеся от оси симметрии; чем выше частота, тем линий больше и они теснее.
8. Фурье-ряд «рисование кругами» (3Blue1Brown, DE4) — https://yt.chop.dev/en/v/r6sGWTCMz2k — брать: эпициклы, сумма вращающихся окружностей рисует кривую — «путь = сумма волн» как зрелище. *Открыта зеркальная страница с описанием видео, сам YouTube не открывал.*
9. Тэта-функция в раскраске фазы (Fredrik Johansson) — https://fredrikj.net/blog/2016/03/phaseful-plots/ — брать: график Якоби θ₁ в палитре «белое/чёрное/золото/синее», где линии уровня видны чётко — визуальный финал курса (модулярность) и хорошая подсказка палитры.

**Оп-арт / муар**
10. Вазарели, «Vega» (1957) — https://www.artchive.com/artwork/vega-victor-vasarely-1957/ — брать: чёрно-белая шахматная решётка, вспученная в центре в сферу — решётка как мембрана.
11. Бриджит Райли (Britannica) — https://www.britannica.com/print/article/503767 — брать: волнистые линии, дающие иллюзию колебания и рельефа на плоскости; чёрно-белое, потом чередование цветов.
12. Бриджит Райли, «Fall» (Tate) — https://www.tate.org.uk/art/artworks/riley-fall-t00616 — *страница открылась, но текстового описания работы в ней нет; визуально не проверено.*
13. Муар концентрических колец (Michael Bach) — https://michaelbach.de/ot/lum-moire1/ — брать: два набора колец, сдвинутых друг относительно друга, дают тёмные изогнутые полосы-разностные частоты — «интерференция» без физики.

**Генеративная графика / кинетика**
14. Ryoji Ikeda, «test pattern» (ISEA 2013) — https://www.isea-archives.org/symposia/isea2013/2013-artworks-video-ikeda — брать: данные → штрихкод/бинарные паттерны, предельный контраст; дисциплина «одна идея, никакого декора».
15. Zach Lieberman, «Circles, Blobs, Ripples» (Unit London) — https://unitlondon.com/exhibitions/zach-lieberman-circles-blobs-ripples — брать: идеальные круги + рябь из сходящихся линий с градиентами; «немного случайности внутри строгого кода».
16. Tyler Hobbs, Fidenza (Toledo Museum) — https://infiniteimages.toledomuseum.org/artwork/fidenza-370 — брать: поле потока ведёт линии; разнообразие при сохранённом единстве — урок про плотность линий, а не про стиль.
17. Reuben Margolin, кинетические волны — https://en.wikipedia.org/wiki/Reuben_Heyday_Margolin и https://www.reubenmargolin.com/about/ — брать: подвесные механизмы (кулачки, рычаги, шкивы), где движение волны выводится из геометрии механизма — «аналитическое решение», ставшее физическим.

**Орнамент / настроение**
18. Исламские розетки (Kaplan) — https://www.mi.sanu.ac.rs/vismath/kaplan/node2.html — брать: центральная звезда, окружённая кольцом шестиугольников, n-кратная симметрия — строгая радиальная композиция, идеальная под круг.
19. Хокусай, «Большая волна» (Met) — https://www.metmuseum.org/articles/great-wave — брать только настроение: оттенки синего (берлинская лазурь + индиго), волна-передний план против крошечной вершины вдали; не копировать композицию.

Радужку/линзу/калейдоскоп отдельным референсом не искал — используется как метафора в концепции 1.

---

## 2. Математика под картинками (что точно, что образ)

- **Точно.** Блуждание по циклу ℤ/N (шаг ±1). Число путей длины n из 0 в k:
  `#paths = (1/N) · Σ_{j=0}^{N−1} (2cos(2πj/N))^n · e^{2πi jk/N}`.
  Если нарисовать «время = радиус, положение = угол», получится полярный треугольник Паскаля, а его плотность — сумма косинусов. Это ровно концепция 1.
- **Точно.** Метод отражения: путей длины 2n из 0 в 0, заходящих ниже нуля, столько же, сколько путей в −2, т.е. `C(2n, n+1)`; Каталан = `C(2n,n) − C(2n,n+1)`. Линия воды в концепции 2 = ось отражения.
- **Точно (физика из референса 6).** Песок сбрасывается с колеблющихся участков и копится в узлах.
- **Образ, не теорема.** «Песчинки блуждают, пока не найдут узел» (концепция 3) — красивая модель, но реальная динамика песка — подпрыгивания со сносом, а не честное решёточное блуждание.
- **Образ.** Что нарисует генератор, — впечатление, а не точная плотность путей. Точную версию любой концепции можно потом построить кодом (полярный Паскаль считается за минуту) и использовать как подложку/референс-изображение.

---

## 3. Четыре концепции

### К1. «Радужка блуждания»
- **Идея.** Зритель видит светящийся глаз-радужку; на деле это пространство-время блуждания по кругу: зрачок — стартовая точка, волокна радужки — пути (на каждом кольце шаг на деление по или против часовой), а к краю плотность путей складывается в концентрические кольца стоячей волны. Пути переходят в волны внутри одного кадра.
- **Композиция.** Центр: крошечная белая точка-зрачок + тёмное кольцо-зазор. Середина: веер из зигзагов, 12–16 ярких «спиц» плотности. Край: 5–7 чётких колец ряби, тонкое тёмное лимбальное кольцо на ~85% кадра. Углы — почти чёрный фон, их не жалко.
- **Палитра.** `#0B1026` чернильно-синий фон · `#F2B33D` золото путей · `#FFF4D6` горячий кремово-белый в плотных местах · `#3FD0C9` бирюза колец · `#5B3FA8` фиолетовый ореол лимба.
- **Фактура/стиль.** Генеративная линия со световым свечением, как длинная выдержка следов света от механизма; бритвенно тонкие линии, без «космоса».
- **В 40 px.** Яркая точка в центре, лучи, кольцевой обод: силуэт «глаза/мишени» на тёмном — хорошо выделяется в списке чатов, особенно в тёмной теме.
- **Риски.** (а) «Нейросетевая космическая мандала»: запретить звёзды, туманности, блики, фрактальные завихрения, требовать прямые ломаные на полярной сетке. (б) Шум в мелком размере: держать крупную структуру (немного спиц, немного колец, тёмный зазор вокруг зрачка). (в) Слишком похоже на настоящий глаз (жилки, веки): прямо запретить анатомию.

### К2. «Хребты Каталана»
- **Идея.** Горный хребет на рассвете, каждый гребень — путь Дика (ступени по 45°, не ниже линии воды), а в воде его отражение у берега ещё точное, ниже рассыпается в синусоидальную рябь. Линия воды — это и «не ниже нуля», и ось метода отражения, а рябь — волны.
- **Композиция.** Горизонт-ватерлиния горизонтально, чуть ниже центра. Над ней — 4–5 слоёв гребней с воздушной перспективой, за ними большой бледный диск солнца по центру (даёт «глаз» и держит круг). Под линией — отражение, переходящее в полосы ряби. Края круга — небо и вода, срезаются безболезненно.
- **Палитра.** `#1D2B53` индиго · `#1F4E79` берлинская лазурь · `#F4A261` абрикосовое небо · `#FBEFD5` кремовый диск/бумага · `#E4572E` киноварь (одна тонкая линия/точки в вершинах).
- **Фактура/стиль.** Настроение японской ксилографии: плоские слои цвета, бумажное зерно, градиент неба «бокаси», чёткие резаные края; но геометрично и современно.
- **В 40 px.** Тёмный зубчатый треугольник над светлой полосой + бледный диск — читается как «пейзаж/закат», спокойно, но менее броско, чем К1/К4.
- **Риски.** (а) Стоковый «закат в горах»: требовать прямые 45° отрезки, светящиеся точки в узлах решётки, едва видную точечную сетку. (б) Похожесть на Хокусая/Фудзи: прямо запретить Фудзи, лодки, когти пены, ссылку на конкретную гравюру. (в) Горизонтальная композиция в круге слабее радиальной — компенсирует диск солнца в центре.

### К3. «Песок Хладни»
- **Идея.** Макрофото чёрной круглой пластины: золотой песок собрался в фигуру Хладни (кольца + радиальные спицы), а несколько песчинок застыли в прыжке с короткими ступенчатыми следами-зигзагами. Блуждающие частицы находят узлы волны.
- **Композиция.** Край пластины = окружность на ~85%. Центр: узел-перекрестье. Звезда из 8 спиц + 3–4 кольца. Пара «прыгающих» песчинок со следами — ближе к центру, крупно. Углы — чёрная пустота.
- **Палитра.** `#0E0E10` чёрный анодированный металл · `#E8C98A` песок · `#FFE7B0` тёплый блик · `#6FA8DC` холодный контровой свет.
- **Фактура/стиль.** Фотореализм, лабораторная макросъёмка, низкий скользящий тёплый свет с одной стороны, холодный контур с другой; тактильность, каждая песчинка искрит.
- **В 40 px.** Золотая звезда-мандала на чёрном: очень хорошо.
- **Риски.** (а) «Путей» не видно, остаются только волны: следы-зигзаги песчинок должны быть заметны в большом размере; в маленьком их потеря допустима. (б) Следы превращаются в шум/мусор: 3–6 песчинок, не больше. (в) Глянцевый «AI-фотореал»: просить настоящий фото-вид, лёгкую несовершенность, пыль, без идеальной симметрии песка.

### К4. «Решётка, по которой идёт волна» (оп-арт)
- **Идея.** Чёрно-белая клетчатая решётка, по которой ходит точка, вспучена двумя интерферирующими круговыми волнами, а по линиям этой искажённой решётки идёт один ярко-красный ступенчатый путь. Решётка путей, волна, которая её колышет, и сам путь — в одной плоской графике.
- **Композиция.** Решётка ~11 клеток в поперечнике круга, маска-круг с тонким чёрным ободом; два центра волн симметрично относительно центра; красный путь стартует в центре и уходит к краю, пересекая гребни. Углы вне круга — однотонный светлый фон.
- **Палитра.** `#F4F1EA` тёплый белый · `#111111` чернила · `#FF3B1F` киноварь (путь) · опционально `#1E40FF` кобальт для одной тонкой второй линии.
- **Фактура/стиль.** Строгий плоский вектор, никаких градиентов и текстур, идеальные края, дисциплина постера середины XX века.
- **В 40 px.** Самый контрастный и «значковый» вариант: вспученная шахматка + красный штрих. Отлично видно и в светлой, и в тёмной теме.
- **Риски.** (а) Банальность «под Вазарели»: отличие держится на красном пути и двух источниках волн, их нельзя терять. (б) Муар/алиасинг при уменьшении: крупные клетки (≤12), без тонких полос. (в) Сухость: может выглядеть как учебная иллюстрация, а не вау — нужна смелая амплитуда вспучивания.

---

## 4. Промпты для ChatGPT (GPT image)

### К1. «Радужка блуждания»

```
Square 1:1 image, 1024×1024. All important content sits inside a centered circle occupying about 85% of the canvas; the corners are expendable and fall off into near-black.

Subject: a luminous abstract iris made of lattice paths, seen perfectly head-on and centered — a diagram of light that you look through, not a biological eye.

Structure (render it faithfully, it is mathematically meaningful):
– Exact center: a tiny, brilliant white-gold point (the pupil) — the starting point of a random walk — surrounded by a narrow ring of darkness.
– From the point, thousands of hair-thin glowing threads travel outward ring by ring on a faint polar grid (concentric rings × radial lines). At every ring each thread steps exactly one notch clockwise or one notch counterclockwise, so every thread is a crisp piecewise-straight angular zigzag, never a smooth curve. Together they form a branching fan — a Pascal-triangle / bean-machine fan wrapped around a circle.
– Where many threads overlap they glow brighter, so near the center the path density forms 12–16 soft radial spokes of light.
– Further out, fans coming around the circle from both sides meet and overlap, and their brightness organizes into 5–7 crisp concentric ripple rings, like standing waves on a drumhead: the density of paths visibly turns into interference fringes toward the rim.
– At about 85% of the canvas: a thin, sharp, dark limbal ring with a faint violet halo, then darkness.

Style: precise generative line art with a physical glow, like a long-exposure photograph of light traces drawn by a mechanism. Razor-thin lines, fine detail without noise, high contrast, calm and scientific, deep dark background with nothing in it.

Palette, strictly: background ink-navy #0B1026; threads warm gold #F2B33D brightening to hot cream-white #FFF4D6 where they are dense; outer ripple rings cool teal #3FD0C9; limbal halo violet #5B3FA8.

Small-size readability: shrunk to 48 px it must still read as a bright eye-like disc — bright center point, radiating spokes, ringed rim. Keep the large-scale structure bold and simple.

Do not include: any text, letters, digits, formulas or symbols; watermark, signature, logo, frame or UI; eye anatomy (eyelids, lashes, skin, veins, catchlight reflections); stars, galaxies, nebulae, space dust; lens flare, bokeh, sparkles, smoke; fractal-flame swirls; glossy 3D chrome.
```

Если вышло не то:
- Похоже на космическую мандалу/фрактал → «Make every thread strictly piecewise-straight steps along a visible faint polar grid; halve the glow; remove all swirls and soft clouds; more diagram, less nebula.»
- Шумно/каша в мелком размере → «Simplify: fewer threads, 8 bold spokes, 4 rings, a wider dark gap around the pupil, thicker limbal ring.»
- Слишком похоже на живой глаз → «Remove all organic texture; it is an instrument made of light lines, not an organ.» (Светлая версия: «invert to cream background #FBF6EA with ink-navy and gold lines, no glow».)

### К2. «Хребты Каталана»

```
Square 1:1 image, 1024×1024. All important content inside a centered circle occupying about 85% of the canvas; the corners are expendable.

Subject: a mountain range at dawn made of mathematical lattice paths, mirrored in still water that dissolves into waves.

Composition:
– A perfectly horizontal waterline slightly below the center.
– Above it, 4–5 layered ridgelines receding into haze. Each ridge is a piecewise-straight zigzag of equal-length up and down segments at exactly 45 degrees, starting and ending on the waterline and never dipping below it; peaks of different heights. Nearest ridge darkest and sharpest, farther ridges progressively paler (atmospheric perspective). At every corner of the nearest ridge, a tiny point of light, as if marking a lattice vertex; a barely visible dot grid in the sky.
– A large pale disc (low sun) centered behind the ridges.
– Below the waterline: the mirror reflection of the ridges, exact right at the line, then breaking downward into horizontal sinusoidal ripple bands that get smoother and wider — the reflection turning into a sum of waves.

Style: the mood of a Japanese woodblock print — flat layered color planes, subtle washi paper grain, crisp carved edges, soft graded sky — but contemporary, strictly geometric and minimal. No figures, no boats, no buildings, no trees, no recognizable real mountain, no foaming wave crests, no imitation of any specific historical print.

Palette, strictly: indigo #1D2B53, Prussian blue #1F4E79, apricot dawn sky #F4A261, cream disc and paper #FBEFD5, one thin vermilion accent #E4572E on the nearest ridge.

Small-size readability: at 48 px it must read as a dark zigzag silhouette over a light band with a pale disc behind.

Do not include: any text, letters, digits, symbols, seals or stamps, watermark, signature, logo, frame; photographic realism; lens flare; birds; clouds with detail.
```

Если вышло не то:
- Стоковый пейзаж → «Make every ridge strictly straight 45-degree segments, like a graph on squared paper; remove all natural rock texture.»
- Слишком похоже на известную гравюру → «Remove any wave crests and any single dominant cone-shaped peak; keep only layered zigzag ridges and calm ripples.»
- Скучно в маленьком → «Increase contrast: nearest ridge near-black indigo, sky brighter apricot, disc larger and closer to the exact center.»

### К3. «Песок Хладни»

```
Square 1:1 image, 1024×1024. All important content inside a centered circle occupying about 85% of the canvas; the corners are expendable and pure black.

Subject: top-down macro photograph of a circular matte-black metal plate vibrating, fine golden sand gathered into a sharp Chladni nodal figure: 8 radial nodal lines crossing 3–4 concentric rings, forming a symmetric star-and-ring pattern. The plate's edge is the circle at about 85% of the frame; the plate's center is a clean crossing point of the lines.

Hero detail: 3–6 individual sand grains near the center caught mid-bounce, slightly lifted with a soft shadow below, each leaving a faint short motion trail made of tiny straight right-angle steps (left/right/up/down), like a staircase — grains wandering at random until they settle onto the still nodal lines. The trails are subtle, only visible on close inspection.

Lighting and camera: low warm raking light from one side so every grain glints; a cool blue rim light from the opposite side along the plate edge; crisp focus in the center, gentle falloff toward the edge; real laboratory-photograph feel with tiny natural imperfections and a little dust — not an illustration, not a 3D render.

Palette: black anodized metal #0E0E10, sand #E8C98A, warm glints #FFE7B0, cool rim light #6FA8DC.

Small-size readability: at 48 px it must read as a golden star-mandala on black.

Do not include: any text, letters, digits, symbols, watermark, signature, logo; hands, tools, speakers, cables, violin bow; table or background objects; perfectly CG-smooth sand; glitter, sparkle stars, bokeh orbs.
```

Если вышло не то:
- Не видно «путей» → «Make the staircase trails of the 4 lifted grains clearly visible: thin, slightly glowing, right-angled, each 6–10 steps long.»
- Выглядит как рендер → «Shoot it like a real 100mm macro photo: slight uneven sand density, a few stray grains, natural light falloff, no perfect symmetry.»
- Вяло в мелком размере → «Fewer, thicker nodal lines (6 spokes, 2 rings) and denser brighter sand on them.»

### К4. «Решётка, по которой идёт волна»

```
Square 1:1 image, 1024×1024, flat vector graphic. All important content inside a centered circle occupying about 85% of the canvas, outlined by a thin black ring; outside the circle the corners are plain warm white and expendable.

Subject: a black-and-white checkerboard lattice, about 11 cells across the circle, deformed as if it were an elastic membrane pushed by two overlapping circular waves emanating from two points placed symmetrically left and right of the center. Where the waves add, cells swell into rounded bulging lozenges; where they cancel, cells pinch thin — a strong optical illusion of a rippling surface with curved nodal valleys between the two sources.

On top: one single bold vermilion line — a lattice path that follows the deformed grid lines, a staircase of right-angle steps (only left/right/up/down moves along cell edges), starting with a small vermilion dot at the exact center and wandering outward to the rim, crossing several wave crests, so its steps visibly stretch and squeeze with the membrane.

Style: strict flat colors, no gradients, no shading, no texture, no glow, perfectly crisp geometric edges, the discipline of a mid-century optical-art poster; large cells so the pattern stays clean when tiny.

Palette, strictly: warm white #F4F1EA, ink black #111111, vermilion #FF3B1F (the path and dot only).

Small-size readability: at 48 px it must read as a bulging checkerboard disc crossed by one red stroke.

Do not include: any text, letters, digits, symbols, watermark, signature, logo; thin stripe patterns that alias when small; 3D rendering, shadows, paper texture; extra colors.
```

Если вышло не то:
- Скучная плоская шахматка → «Push the deformation much harder: cells near wave crests up to 2× larger, near nodal lines almost vanishing; the illusion must feel like a sphere breathing.»
- Путь не идёт по решётке → «The red line must run exactly along cell edges of the deformed grid, turning only at grid vertices.»
- Мерцание/муар в маленьком → «Use 9 cells across instead of 11, thicker black ring, no line thinner than 1/100 of the canvas.»

---

## 5. Рекомендация была К1 «Радужка блуждания» — выбрана К2 (владелец 04.10 02:19)

Финал — v2 после добивки (сияющий снег, контраст гор с фоном, без второго круга): `kanal/avatarka-final.png`, 1254×1254, стоит на канале с 04.10. Промпт — `PROMPT-K2.md`.


Только она одновременно отвечает на «как глаз» буквально, ложится в круг без потерь (радиальная композиция, края и так тёмные) и в 40 px даёт самый сильный силуэт — яркая точка, лучи, обод. При этом она честная: полярный треугольник Паскаля на цикле ℤ/N — ровно та картинка, где число путей равно сумме степеней косинусов, то есть «путь = суперпозиция волн» нарисован, а не обещан. Вау она даёт за счёт света и масштаба (тысячи путей из одной точки), а за «нейросетевость» отвечают явные запреты в промпте; запасной вариант — К4, если хочется максимально графичный значок, и К2, если хочется поэзии и метода отражения.

## 6. Как проверять результат
- Уменьшить до 48 px и посмотреть в круглой маске (на Mac: `sips -Z 48 avatar.png --out avatar48.png`).
- Посмотреть в светлой и тёмной теме Telegram: у К1 тёмный фон, в светлой теме кружок будет «дырой» — это нормально и даже заметно; если не нравится, есть светлая версия (строка итерации).
- Загружать 640×640 и больше; ChatGPT отдаёт 1024×1024, этого хватает.
