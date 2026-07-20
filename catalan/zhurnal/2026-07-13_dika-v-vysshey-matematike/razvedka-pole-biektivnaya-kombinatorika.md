# Живо ли поле: биективная комбинаторика путей Дика и их обобщений

*Разведка ландшафта, июль 2026. Не совет по карьере — фактура для решения. Каждое нетривиальное утверждение снабжено ссылкой; приоритет — последние ~8 лет; «живое и доступное» отделено от «живого, но тяжёлого».*

---

## Вердикт

**Живо ли поле — да, однозначно, и сейчас на подъёме.** Три регулярные конференции с уже назначенными будущими выпусками; профильная конференция по решётчатым путям проходит буквально на следующей неделе (Вена, 20–24 июля 2026) и целиком состоит из работ по путям Дика, Моцкина, ν-Тамари, рациональному и q,t-Каталану [1]. Плотный поток arXiv math.CO (порядка 5–6 тысяч препринтов в год) [7], живые журналы (включая новый бесплатный Combinatorial Theory) [5], свежие статьи именно про пути Дика от первого ряда авторов [6]. За последние два года в соседней «тяжёлой» части закрыты крупные гипотезы (shuffle-теорема в 2018 году, классификация блужданий в четверти плоскости в 2024) — это признак не угасания, а зрелости.

**Находима ли доступная связанная задача — да, но с резкой оговоркой.** Доступные биективные задачи, тесно связанные с темами проекта, реально существуют, и их много. Но сосредоточены они в конкретных карманах: **статистики и биекции парковочных функций, биекции интервалов Тамари / ν-Тамари с планарными картами, комбинаторное доказательство q,t-симметрии на путях, стек-сортировка, пробелы в доказательствах циклического просеивания.** Именно там низкий машинный барьер и открытые вопросы «на бумаге». А вот громкие заголовки поля тяжелы: shuffle-теорема и диагональные гармоники, аналитическая классификация блужданий, пределы случайных перестановок, рост Av(1324) стоят на тяжёлом аппарате: симметрических функциях Макдональда, дифференциальной Галуа-теории, SLE/LQG-вероятности. Вход есть, но целиться надо в доступные углы, трезво понимая, что самое знаменитое здесь — и самое тяжёлое.

---

## Шорт-лист направлений-кандидатов

Ранжировано по доступности входа. Барьер: **низкий** = карандаш и бумага, элементарные объекты; **средний** = нужна техника (функциональные уравнения, дискретная геометрия) или computer algebra; **высокий** = тяжёлый аппарат.

**1. Статистики и биекции парковочных функций.** *Что открыто:* десятки конкретных вопросов перечисления и статистик — lucky cars, defective/Kreweras-парковка, primeness, избегание паттернов, Naples/Fubini-варианты; открытые пункты Лакнера–Панхольцера про парковку на деревьях. · **барьер: низкий** · *связь с проектом:* парковочные функции — прямой объект проекта (area/inversions, Креверас, Кэли–Прюфер, аргумент Поллака); взрывной поток статей 2023–2026, во многом из студенческих REU-программ. · вход: [39], [40], [38].

**2. Биекции «интервалы Тамари / ν-Тамари ↔ планарные карты».** *Что открыто:* найти естественное семейство планарных карт под формулу m-Тамари-интервалов Bousquet-Mélou–Fusy–Préville-Ratelle; биекция (m+1)-констелляций с greedy m-Тамари для общего m (случай m=1 закрыт биективно только в июле 2026). · **барьер: низкий–средний** · *связь:* треугольники ↔ деревья ↔ пути Дика ↔ скобки — позвоночник проекта; решётка Тамари сидит ровно на нём. · вход: [42], [33], [36].

**3. Комбинаторное доказательство q,t-симметрии q,t-Каталана.** *Что открыто (OPAC-029/030):* построить биекцию на путях Дика / word-parking-функциях, меняющую местами `dinv` и `area` (эквивалентно `area`↔`bounce` через zeta-отображение). Частично сделано (Lee–Li–Loehr, члены высоких степеней). · **барьер: низкий–средний** · *связь:* q-Каталан и статистики на путях — q-сторона проекта. · вход: [27], [26], [29].

**4. q,t-симметрия высших и рациональных Каталанов на k⃗-путях Дика.** *Что открыто:* refined q,t-симметрия для k-Дика / Фусс–Каталана и рациональных (a,b)-путей; активная свежая линия (препринты 2024–2025). · **барьер: низкий–средний** · *связь:* Фусс–Каталан, рациональная комбинаторика Каталана — прямо заявленная область проекта; смыкается с zeta/sweep-отображением. · вход: [23], [24], [25].

**5. Стек-сортировка и сортирующие машины.** *Что открыто (список Ваттера 2026):* кратчайшая перестановка, не сортируемая тремя последовательными стеками; природа производящей функции 3-stack-sortable; C-машины и обобщённые стеки; сепарабельные derangement-ы. · **барьер: низкий–средний** · *связь:* 231-избегающие = стек-сортируемые, стек как механизм — явный фасет проекта. · вход: [44], [45].

**6. Пробелы в доказательствах циклического просеивания (cyclic sieving, CSP).** *Что открыто:* единообразная биекция «непересекающиеся ↔ невложенные» (доказательство Armstrong–Stump–Thomas разбирает исключительные типы компьютером — прозрачной биекции нет); ряд CSP на каталановских объектах (promotion, circular Dyck paths) без биективного/представленческого объяснения. · **барьер: низкий–средний** · *связь:* CSP на триангуляциях, непересекающихся разбиениях, путях Дика — жанр биективных доказательств, который проект и любит. · вход: [48], [49].

**7. (Горизонт, средний барьер) Элементарные биекции в решётчатых блужданиях.** *Что открыто:* полностью биективное объяснение простых формул для чисел Кревераса/Гесселя; метод отражений в невыпуклых конусах (три-квадрант). · **барьер: средний** · *связь:* цикл-лемма, принцип отражения, баллотировка — ядро проекта; но за элементарной постановкой быстро встаёт тяжёлый аппарат. · вход: [15], [9].

---

## 1. Живо ли поле — свидетельства

**Конференции — регулярные, с назначенным будущим.**

- **Международная конференция по комбинаторике решётчатых путей (LPC)** — профильная. 10-я: TU Wien, 20–24 июля 2026, 8 пленарных докладов + 21 короткий + постеры, вся программа про пути Дика/Моцкина, ν-Тамари, рациональный и q,t-Каталан, метод ядра; 11-я уже анонсирована на 2029 (Индия). Серия идёт с 1984 [1].
- **FPSAC** (Formal Power Series and Algebraic Combinatorics) — ежегодный флагман: 2024 Бохум, 2025 Саппоро, 2026 Сиэтл, 2027 Голуэй уже назначен; архив с 1988 [2].
- **Permutation Patterns** — ежегодно (2024 Айдахо, 2025 Сент-Эндрюс, 2026 Cal State LA), с традиционными сессиями открытых задач [3].
- **Séminaire Lotharingien de Combinatoire** — и журнал (open access), и серия встреч [4].

**Журналы активны и релевантны.** Electronic Journal of Combinatorics (пример 2025: Baril–Bousquet-Mélou–Kirgizov–Naima, «The Ascent Lattice on Dyck Paths») [6]; новый бесплатный diamond-OA Combinatorial Theory, отколовшийся от Elsevier JCTA в 2020 [5]; плюс JCTA, Advances in Applied Mathematics, Annals of Combinatorics, Algebraic Combinatorics.

**arXiv math.CO** — порядка 470 препринтов в месяц; в любой месячной выборке видны работы по решётчатым путям, интервалам Тамари, парковочным функциям [7].

**Свежие прорывы (2018–2026) — признак зрелости, не застоя.** Shuffle-гипотеза доказана (Carlsson–Mellit 2018) [18]; рациональная (m,n)-shuffle доказана (Mellit 2021) [19]; rise-версия Delta-гипотезы (D'Adderio–Mellit 2022), extended Delta (Blasiak–Haiman–Morse–Pun–Seelinger 2023) [21][22]; классификация блужданий в четверти плоскости — «конечная группа ⟺ D-конечность полной производящей функции» — доказана через эллиптические функции (Dreyfus–Elvey Price–Raschel 2024), новое чисто алгебраическое доказательство 2025 [10][11]. Каждое закрытие сразу открывает следующий слой вопросов (см. §2).

---

## 2. Открытые задачи по кластерам

### 2.1. Блуждания в четверти плоскости и решётчатые пути

Ядро — тяжёлое, но есть карманы попроще.

- **Классификация малых шагов почти закрыта — открыт «одномерный» остаток.** Для полной трёхпеременной производящей функции критерий «D-конечна ⟺ группа блуждания конечна» доказан [10][11]. Осталась одномерная (univariate) версия: не-D-конечность доказана не для всех бесконечно-групповых моделей; часть моделей известна как дифференциально-алгебраические, но их D-конечность не решена. · **высокий** (асимптотика, сингулярный анализ), но новый алгебраический маршрут [11] — самый доступный вход в этот конкретный вопрос.
- **Большие шаги — полной классификации нет.** У орбиты недавно появилась Галуа-структура, дав первые доказательства алгебраичности отдельных моделей, но аналога классификации малых шагов пока нет [13]. · **высокий** в общем виде; **средний** для отдельных явных моделей (орбитные суммы, метод ядра вручную).
- **Высшие размерности (3D-октант, 4D, конусы Вейля) — во многом открыты.** Картина сложнее, чем в 2D; встречаются конечно-групповые модели, выглядящие не-D-конечными [16]. · **средний** для экспериментально-вычислительной части (перечисление, угадывание ОДУ в Sage/Maple — реально для сильного неспециалиста с навыком computer algebra), **высокий** для строгих доказательств.
- **Три-квадрант / невыпуклые конусы** — «первый уровень сложности за пределами квадранта», многие модели не решены; самый элементарный вход — метод отражений [14][15]. · **средний–высокий**.
- **Элементарный карман:** полностью биективное объяснение простых произведений для чисел Кревераса и Гесселя — классическая, всё ещё не до конца закрытая карандашная цель [9]. · **средний**.

### 2.2. Рациональный Каталан, sweep-отображение, shuffle, q,t-Каталан

Здесь — самая плотная жила доступных биективных задач, оставшихся после алгебраических доказательств.

- **Комбинаторное доказательство q,t-симметрии `C_n(q,t)=C_n(t,q)`** (OPAC-029). Левая часть симметрична по причинам теории представлений, но общей биекции `dinv`↔`area` нет. Частично: Lee–Li–Loehr закрыли члены степени `(n choose 2)−k` для малых k [26]. · **низкий–средний** — флагманская доступная задача кластера.
- **Комбинаторное доказательство сопряжённой q,t-симметрии модифицированных многочленов Макдональда** (OPAC-030): биекция на заполнениях, меняющая `inv`↔`maj`; сделаны крюковые формы и q=0 [27]. · **средний**.
- **Биективное доказательство самой shuffle-теоремы.** Доказательство Carlsson–Mellit алгебраическое (операторные тождества в алгебре путей Дика), не биективное; прямого комбинаторного объяснения тождества по парковочным функциям нет [18][27]. · **средний** поставить, **высокий** внутри имеющейся машинерии.
- **Valley-версия Delta-гипотезы** — открыта (в отличие от доказанной rise-версии) [20][21]. · **высокий** (Theta-операторы, elliptic Hall algebra).
- **q,t-симметрия высших/рациональных Каталанов** (k⃗-Дик, Фусс, рациональные (a,b)) — активная элементарная линия статистик на путях (dinv/area/bounce). · **низкий–средний**.

> **Поправка к заходу.** Sweep-отображение (и zeta-отображение) — **биективность уже доказана** (Thomas–Williams, «Sweeping up zeta», Selecta 2018), явные алгоритмы обращения есть (Garsia–Xin для рациональных, и обобщения) [24][25]. Открытым остаётся лишь «мягкое»: прозрачное человеко-читаемое описание обратного — отсюда даже свежая попытка через машинное обучение. То есть «биективность sweep-map» из захода — уже не открытый вопрос, а закрытый; это хорошая **точка входа для чтения**, не для исследования.

### 2.3. Решётка Тамари, ν-Тамари, ассоциэдр, интервалы; парковочные функции

- **Планарное семейство для (немеченых) m-Тамари-интервалов** — найти карты, перечисляемые формулой Bousquet-Mélou–Fusy–Préville-Ratelle. Чисто биективная задача, аналог известных биекций [42]. · **низкий–средний**.
- **(m+1)-констелляции ↔ greedy m-Тамари-интервалы для общего m** — случай m=1 закрыт биективно в июле 2026, общий m открыт [42]. · **низкий–средний**.
- **Равномощность m-Cambrian и m-Тамари-интервалов** (Préville-Ratelle) — счётные данные совпадают, канонической биекции нет [42]. · **средний**.
- **ν-Тамари в типе B** — дать определение хотя бы для некоторых ν (Ceballos–Padrol–Sarmiento) [34]. · **средний**.
- **Тривариантные диагональные гармоники ↔ decorated m-Тамари** (3-параметрическая гипотеза Бержерона) — комбинаторная часть (размерность, характер) доказана, связь с самим модулем гармоник открыта [37]. · **высокий**.
- **Парковочные функции** — самый плотный слой карандашных вопросов: lucky cars, defective/Kreweras, primeness, избегание паттернов, vacillating/metered/Naples/Fubini; открытые пункты Лакнера–Панхольцера про парковку на деревьях (характеризация чисел, распределения смещений, defective-парковка) — часть закрыта Contat и др., но далеко не исчерпывающе [38][39][40]. · **низкий** (probabilistic scaling limits на случайных деревьях — отдельная **высокая** линия).

> **Поправка к заходу.** Формула числа интервалов Тамари — не `3·2^{n-1}/((n+1)(n+2))·C(2n,n)`, а формула Шапото `I_n = 2(4n+1)! / ((n+1)!(3n+2)!)` = 1, 3, 13, 68, 399, … (OEIS A000260) [31]. Первая формула считает другой объект (greedy-Тамари при m=1 = двудольные планарные карты).

### 2.4. Permutation patterns (один фасет) и жанр биективных доказательств

- **Точный рост Av(1324)** — единственный паттерн длины 4 с неизвестным даже показателем роста; границы 10.27–13.5, численно ≈11.60; возможно, производящая функция не D-конечна [43]. · **высокий** (тяжёлая аналитика/численность) — знаменитая, но не элементарная.
- **Стек-сортировка (список Ваттера 2026):** кратчайшая перестановка, не сортируемая тремя стеками (известно: длина ≥14, гипотезы 15 и 22); природа производящей функции 3-stack-sortable; C-машины; сепарабельные derangement-ы и доля 9/16 [44][45]. · **низкий–средний** — плотный слой доступных задач.
- **Пермутоны** (permuton — пределы случайных избегающих перестановок): skew Brownian permuton как класс универсальности, связи с LQG/SLE [46][47]. · **высокий** (вероятность/SLE).
- **CSP без прозрачного доказательства:** единообразная биекция «непересекающиеся ↔ невложенные» [49]; CSP для promotion, circular Dyck paths — доказаны тяжёлыми средствами, биекции нет [48]. · **низкий–средний** — хорошая входная ниша.

---

## 3. Доступность входа — честное разделение

**Живое и доступное (низкий машинный барьер, «карандаш и бумага»).**
Парковочные функции целиком (статистики, биекции, избегание паттернов, primeness) — самый доступный и самый активный угол. Биекции интервалов Тамари / ν-Тамари с планарными картами. Комбинаторное доказательство q,t-симметрии и статистики на k⃗-путях Дика. Стек-сортировка и сортирующие машины. Пробелы в доказательствах CSP. Общее у них: элементарные объекты (пути, деревья, перестановки, разбиения), результат проверяется руками, частичные результаты уже есть — есть куда встроиться. Многие такие статьи выходят из студенческих REU-программ, что прямо указывает на низкий порог входа.

**Живое, но тяжёлое (высокий барьер — горизонт, не вход).**
Shuffle-теорема, Delta-гипотеза (valley), диагональные гармоники — симметрические функции Макдональда, Theta-операторы, elliptic Hall algebra, схемы Гильберта. Аналитическая классификация блужданий — комплексный анализ, эллиптические/тета-функции, дифференциальная Галуа-теория, аналитическая комбинаторика многих переменных. Пределы-пермутоны — SLE/LQG-вероятность. Рост Av(1324) — тяжёлая асимптотика производящих функций. Это стоит читать, чтобы видеть горизонт и мотивацию доступных задач, но не с этого начинать.

**Средний барьер (мост).** Метод ядра и орбитные суммы для отдельных моделей блужданий; экспериментальная комбинаторика в высших размерностях (Sage/Maple, угадать-и-доказать); дискретная геометрия ν/s-ассоциэдров; перечисление через функциональные уравнения. Требует техники, но не годов подготовки.

---

## 4. Кто и где

**Решётчатые блуждания / аналитическая комбинаторика.** Mireille Bousquet-Mélou (CNRS, LaBRI, Бордо) — центральная фигура; Kilian Raschel (CNRS, Анже/Тур); Andrew Elvey Price (CNRS, Тур); Alin Bostan (Inria, руководитель проекта ANR «De rerum natura»); Charlotte Hardouin, Thomas Dreyfus (Галуа-теория); Stephen Melczer (Waterloo, ACSV, учебник); Marni Mishna (SFU); Manuel Kauers (Linz); Michael Wallner (TU Wien).

**Симметрические функции / q,t-Каталан / shuffle.** Jim Haglund (UPenn); Anton Mellit (Вена, ERC); Erik Carlsson; Michele D'Adderio; Nick Loehr, Greg Warrington (sweep/статистики — доступная сторона); Drew Armstrong (рациональный Каталан); Maria Monks Gillespie (q,t-симметрия комбинаторно, ведёт блог открытых задач).

**Тамари / ассоциэдры / парковка.** Frédéric Chapoton; Louis-François Préville-Ratelle; Xavier Viennot; Cesar Ceballos, Viviane Pons (ν/s-геометрия); Wenjie Fang, Éric Fusy (биекции интервалы↔карты); François Bergeron (тривариантные гармоники); на парковочной стороне — Pamela E. Harris (двигатель REU-потока), Catherine Yan, Alice Contat, Nicolas Curien (вероятностная линия).

**Паттерны / биективный жанр.** Colin Defant (стек-сортировка); Vincent Vatter, Michael Albert (классы, списки задач); David Bevan, Jay Pantone (Av(1324)); Mathilde Bouvel, Valentin Féray, Jacopo Borga (пермутоны); Victor Reiner, Bruce Sagan, Brendon Rhoades (CSP).

**Семинары и школы.** Онлайн: Fields Institute Algebraic Combinatorics Seminar, UC Berkeley Combinatorics Seminar (расписания на researchseminars.org); семинары LaBRI (Бордо) и Institut Denis Poisson (Тур). Летом-2026 перед LPC в TU Wien — Sage Days 132 (13–17 июля) [1]. Видео-курс Вьенно «The Art of Bijective Combinatorics» (IMSc) — постоянная точка входа именно в биективную сторону [8].

**Списки открытых задач.** Ваттер, «An Assortment of Problems in Permutation Patterns», 2026 — самый свежий прицельный список (проверено) [44]; блог «Open Problems in Algebraic Combinatorics» (realopacblog) — точные формулировки OPAC-029/030/031 [27][28]; сборник «Open Problems in Algebraic Combinatorics», AMS PSPUM 110, 2024 [51]; Pak, «Complexity problems in enumerative combinatorics» [50]; слайды Fang с открытыми задачами по Тамари [42].

**Русскоязычные точки входа — тонко.** Специализированного русского курса или монографии именно по биекциям путей Дика нет; Каталан и решётчатые пути идут фрагментами внутри общих курсов. Фундамент: С. К. Ландо, «Лекции о производящих функциях» (МЦНМО, свободный PDF) — язык всей области [55]; Е. Ю. Смирнов (ВШЭ), «Диаграммы Юнга, плоские разбиения и знакочередующиеся матрицы» (МЦНМО, 2014) и курс комбинаторики в НМУ [56]; А. М. Райгородский — общие курсы комбинаторики [57]. Институциональные адреса, где ниша могла бы жить: лаборатория им. Чебышёва (СПбГУ, перечисление карт и меандров), ПОМИ РАН, НМУ, ВШЭ ФКН [58]. Тонкость русской ниши согласуется с проектным мандатом «писать всё самим».

---

## 5. Точки входа — книги и обзоры

- **R. Stanley, «Catalan Numbers» (Cambridge, 2015)** и «Enumerative Combinatorics» т. 1–2 — 214 интерпретаций чисел Каталана, отправная точка [52].
- **P. Flajolet, R. Sedgewick, «Analytic Combinatorics» (2009)** — свободный PDF; аналитическая сторона, метод ядра [53].
- **S. Melczer, «An Invitation to Analytic Combinatorics: From One to Several Variables» (Springer, 2021)** — учебник с Sage/Maple-воркшитами; лучший вход в высшие размерности и ACSV [17].
- **J. Haglund, «The q,t-Catalan Numbers and the Space of Diagonal Harmonics» (AMS, 2008)** — свободный PDF; каноническая книга по q,t-стороне [29].
- **Bousquet-Mélou, Mishna, «Walks with small steps in the quarter plane» (2008)** — каноническая отправная точка по блужданиям (группа, орбитная сумма, метод ядра) [9].
- **Préville-Ratelle, Viennot, «The enumeration of generalized Tamari intervals»** — определение ν-Тамари + биекция [33]; слайды Fang с картой биекций и открытыми задачами [42].
- **C. Yan, «Parking Functions»** (Handbook of Enumerative Combinatorics, 2015) — канонический обзор [38]; популярный вход — Martínez Mori, «What is… a Parking Function?», Notices AMS, 2024 [39].
- **B. Sagan, «The cyclic sieving phenomenon: a survey» (2010)** — вход в CSP и «где нет биективных доказательств» [48].
- **S. Kitaev, «Patterns in Permutations and Words» (2011)** — паттерны как соседний фасет [54].
- **X. Viennot, видео-курс «The Art of Bijective Combinatorics»** — именно биективная сторона [8].

---

## Источники

**Живость поля, площадки, общие точки входа**

[1] LPC 2026 — 10-я Международная конференция по комбинаторике решётчатых путей, TU Wien, 20–24.07.2026 — https://lpc2026.conf.tuwien.ac.at/
[2] FPSAC — серия и архив (2024 Бохум, 2025 Саппоро, 2026 Сиэтл, 2027 Голуэй) — https://fpsac.org/confs/
[3] Permutation Patterns — серия конференций — https://permutationpatterns.com/
[4] Séminaire Lotharingien de Combinatoire (журнал + встречи) — https://www.emis.de/journals/SLC/
[5] Combinatorial Theory (diamond OA, с 2020) — https://escholarship.org/uc/combinatorial_theory
[6] Baril, Bousquet-Mélou, Kirgizov, Naima, «The Ascent Lattice on Dyck Paths», EJC 32(2), 2025 — https://www.combinatorics.org/ojs/index.php/eljc/article/view/v32i2p36
[7] arXiv math.CO (листинги) — https://arxiv.org/list/math.CO/recent
[8] X. Viennot, «The Art of Bijective Combinatorics» (IMSc) — https://viennot.org/abjc.html

**Блуждания в четверти плоскости / решётчатые пути**

[9] Bousquet-Mélou, Mishna, «Walks with small steps in the quarter plane», 2008/2010 — https://arxiv.org/abs/0810.4387
[10] Dreyfus, Elvey Price, Raschel, «Enumeration of weighted quadrant walks: criteria for algebraicity and D-finiteness», 2024 — https://arxiv.org/abs/2409.12806
[11] «On the D-finiteness of generating functions counting small steps walks in the quadrant», 2025 — https://arxiv.org/abs/2509.22464
[12] Dreyfus, Hardouin, Roques, Singer, «On the nature of the generating series of walks in the quarter plane», Invent. Math., 2018 — https://arxiv.org/abs/1702.04696
[13] Bostan, Bousquet-Mélou, Melczer, «Counting walks with large steps in an orthant», 2018 — https://arxiv.org/abs/1806.00968
[14] Bousquet-Mélou, «Enumeration of three-quadrant walks via invariants…», 2021/2023 — https://arxiv.org/abs/2112.05776
[15] Bousquet-Mélou, «Walks avoiding a quadrant and the reflection principle», 2021 — https://arxiv.org/abs/2110.07633
[16] Bostan, Bousquet-Mélou, Kauers, Melczer, «On 3-dimensional lattice walks confined to the positive octant», 2016 — https://arxiv.org/abs/1409.3669
[17] Melczer, «An Invitation to Analytic Combinatorics: From One to Several Variables», Springer, 2021 — https://melczer.ca/textbook/

**Рациональный Каталан / sweep / shuffle / q,t-Каталан**

[18] Carlsson, Mellit, «A proof of the shuffle conjecture», JAMS 31, 2018 — https://arxiv.org/abs/1508.06239
[19] Mellit, «Toric braids and (m,n)-parking functions», Duke Math. J. 170, 2021 — https://arxiv.org/abs/1604.07456
[20] Haglund, Remmel, Wilson, «The Delta Conjecture», Trans. AMS 370, 2018 — https://arxiv.org/abs/1509.07058
[21] D'Adderio, Mellit, «A proof of the compositional Delta conjecture», Adv. Math. 402, 2022 — https://www.sciencedirect.com/science/article/abs/pii/S000187082200158X
[22] Blasiak, Haiman, Morse, Pun, Seelinger, «A proof of the Extended Delta Conjecture», Forum Math. Pi, 2023 — https://arxiv.org/abs/2102.08815
[23] Armstrong, Loehr, Warrington, «Sweep maps: A continuous family of sorting algorithms», Adv. Math. 284, 2015 — https://arxiv.org/abs/1406.1196
[24] Thomas, Williams, «Sweeping up zeta», Selecta Math. 24, 2018 — https://arxiv.org/abs/1512.01483
[25] Garsia, Xin, «Inverting the Rational Sweep Map», 2016 — https://arxiv.org/abs/1602.02346
[26] Lee, Li, Loehr, «A Combinatorial Approach to the Symmetry of q,t-Catalan Numbers», SIAM J. Discrete Math. 32, 2018 — https://arxiv.org/abs/1602.01126
[27] Gillespie, OPAC-029/030 «Two q,t-symmetry problems…» — https://realopacblog.wordpress.com/2020/01/12/two-qt-symmetry-problems-in-symmetric-function-theory/
[28] Zabrocki, OPAC-031 «Coinvariants and harmonics» — https://realopacblog.wordpress.com/2020/01/26/coinvariants-and-harmonics/
[29] Haglund, «The q,t-Catalan Numbers and the Space of Diagonal Harmonics», AMS ULS 41, 2008 — https://www.math.upenn.edu/~jhaglund/books/qtcat.pdf
[30] Hicks, «Combinatorics of the Diagonal Harmonics», 2019 — https://link.springer.com/chapter/10.1007/978-3-030-05141-9_5

**Тамари / ν-Тамари / ассоциэдр / парковочные функции**

[31] Chapoton, «Sur le nombre d'intervalles dans les treillis de Tamari», 2006 (OEIS A000260) — https://arxiv.org/abs/math/0602368
[32] Bousquet-Mélou, Fusy, Préville-Ratelle, «The number of intervals in the m-Tamari lattices», 2011 — https://arxiv.org/abs/1106.1498
[33] Préville-Ratelle, Viennot, «The enumeration of generalized Tamari intervals», 2015 — https://arxiv.org/abs/1511.05937
[34] Ceballos, Padrol, Sarmiento, «Geometry of ν-Tamari lattices in types A and B», 2019 — https://arxiv.org/abs/1611.09794
[35] Fang, Fusy, Nadeau, «Tamari intervals and blossoming trees», Combinatorial Theory 5(1), 2025 — https://arxiv.org/abs/2312.13159
[36] Bousquet-Mélou, Chapoton, «Intervals in the greedy Tamari posets», Combinatorial Theory 4(1), 2024 — https://arxiv.org/abs/2303.18077
[37] Bergeron, «Trivariate Diagonal Harmonics» — https://bergeron.math.uqam.ca/trivariate-diagonal-harmonics/
[38] Yan, «Parking Functions», Handbook of Enumerative Combinatorics (CRC), 2015 — https://www.taylorfrancis.com/chapters/edit/10.1201/b18255-19/parking-functions-catherine-yan
[39] Martínez Mori, «What is… a Parking Function?», Notices AMS 71(7), 2024 — https://www.ams.org/journals/notices/202408/rnoti-p1062.pdf
[40] Harris et al., «Parking functions with a fixed set of lucky cars», 2024 — https://arxiv.org/abs/2410.08057
[41] Contat, Curien, «Parking on Cayley trees and frozen Erdős–Rényi», Ann. Probab., 2023 — https://arxiv.org/abs/2107.02116
[42] Fang, слайды «…enumerative aspects of Tamari lattices» (открытые задачи), PAGCAP 2023 — https://pagcap.lisn.upsaclay.fr/docs/weissensee_fang.pdf

**Паттерны / биективный жанр / CSP**

[43] Bevan, Brignall, Elvey Price, Pantone, «A structural characterisation of Av(1324) and new bounds on its growth rate», 2020 — https://arxiv.org/abs/1711.10325
[44] Vatter, «An Assortment of Problems in Permutation Patterns», 2026 — https://arxiv.org/abs/2602.16355
[45] Defant, «Counting 3-Stack-Sortable Permutations», JCTA, 2020 — https://arxiv.org/abs/1903.09138
[46] Bassino, Bouvel, Féray, Gerin, Pierrot, «The Brownian limit of separable permutations», Ann. Probab., 2018 — https://arxiv.org/abs/1602.04960
[47] Borga, «The skew Brownian permuton…», Proc. LMS, 2023 — https://arxiv.org/abs/2112.00156
[48] Sagan, «The cyclic sieving phenomenon: a survey», 2010 — https://arxiv.org/abs/1008.0790
[49] Armstrong, Stump, Thomas, «A uniform bijection between nonnesting and noncrossing partitions», Trans. AMS, 2013 — https://arxiv.org/abs/1101.1277

**Списки задач / обзоры / русскоязычное**

[50] Pak, «Complexity problems in enumerative combinatorics», 2018 — https://arxiv.org/abs/1803.06636
[51] «Open Problems in Algebraic Combinatorics», AMS PSPUM 110, 2024 — https://www.ams.org/books/pspum/110/
[52] Stanley, «Catalan Numbers» (2015) / «Enumerative Combinatorics» — https://math.mit.edu/~rstan/
[53] Flajolet, Sedgewick, «Analytic Combinatorics», 2009 — https://algo.inria.fr/flajolet/Publications/book.pdf
[54] Kitaev, «Patterns in Permutations and Words», Springer, 2011 — https://link.springer.com/book/10.1007/978-3-642-17333-2
[55] С. К. Ландо, «Лекции о производящих функциях», МЦНМО — https://old.mccme.ru/free-books/lando/lando-genfunc.pdf
[56] Е. Ю. Смирнов, курс комбинаторики (НМУ) / «Диаграммы Юнга, плоские разбиения и знакочередующиеся матрицы» (МЦНМО, 2014) — https://old.mccme.ru/ium/s20/s20-Smirnov.html
[57] А. М. Райгородский, «Основы комбинаторики» (openedu) — https://openedu.ru/course/mipt/COMB/
[58] Лаборатория им. П. Л. Чебышёва (СПбГУ) — https://chebyshev.spbu.ru/ ; ПОМИ РАН — https://www.pdmi.ras.ru/
