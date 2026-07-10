# СПИСОК НА СКАЧИВАНИЕ — источники арки «Программа курса»

Статус 2026-07-03: **Claude не скачал ничего** (только читал 2 страницы в вебе). Ниже — всё, что нужно достать. Качай чистыми PDF и клади в эту папку (`biblioteka/istochniki/`) либо загружай в чат — разложу и обновлю индекс. Аннотации — в `../istochniki-perechislitelnaya.md`.

## A. Книги (копирайт — со стороны владельца)
- [ ] **Loehr, «Bijective Combinatorics»** (CRC, 2011) — единый биективный костяк. Проверить TOC: Дик + парковки + Кэли + цикл-лемма.
- [ ] **Stanley, «Catalan Numbers»** (Cambridge, 2015) — каталог 214 интерпретаций.
- [ ] **Aigner–Ziegler, «Proofs from THE BOOK»** — глава про формулу Кэли (4 доказательства).
      archive.org: https://archive.org/details/MartinAignerGnterM.ZieglerAuth.ProofsFromTHEBOOK · Springer-глава: https://link.springer.com/chapter/10.1007/978-3-662-04315-8_24

## B. Свободные PDF — прямые ссылки
- [ ] Stanley, Catalan Addendum — https://math.mit.edu/~rstan/ec/catadd.pdf
- [ ] Yan, «Parking functions» (Handbook, авторская копия) — https://people.tamu.edu/~huafei-yan/Files/Yan-Final-Own-Copy.pdf
- [ ] Ardila, «Algebraic and geometric methods in enumerative combinatorics» — https://fardila.com/Clase/AC/algmethods.pdf
- [ ] Dershowitz–Zaks, «The Cycle Lemma and Some Applications» — https://www.cs.tau.ac.il/~nachumd/papers/CL.pdf
- [ ] Pak, «History of Catalan Numbers» — https://www.math.ucla.edu/~pak/papers/cathist4.pdf
- [ ] Pollak-доказательство парковок (arXiv) — https://arxiv.org/abs/2511.20796

## C. Русские (педагогичные)
- [ ] Мерзон, «Диаграммы Юнга, пути на решётке и метод отражений» — https://dev.mccme.ru/~merzon/pscache/reflection_method.pdf
- [ ] Вялый, конспект ДМ (ВШЭ), числа Каталана — https://math.hse.ru/data/2017/04/03/1168595906/dm05.pdf
- [ ] Ландо, «Лекции о производящих функциях» (МЦНМО) — https://old.mccme.ru/free-books/lando/lando-genfunc.pdf

## D. Постников (записки; «тот самый» пришлёт владелец)
- [ ] «Тот самый» курс — ссылка от Вани.
- [ ] 18.315 (2006) — https://math.mit.edu/~apost/courses/18.315-2006/
- [ ] 18.217 (2023) — https://math.mit.edu/~apost/courses/18.217_2023/
- [ ] 18.212 (2025) — https://math.mit.edu/~apost/courses/18.212_2025/ · ранняя PDF: https://web.stanford.edu/~lindrew/18.212.pdf

## E. Опционально / потом
- [ ] LGV-лемма — https://en.wikipedia.org/wiki/Lindström–Gessel–Viennot_lemma · экспозиция: https://qchu.wordpress.com/2009/11/17/the-lindstrom-gessel-viennot-lemma/

## Разыскивается (не потерять)
Красивые **визуальные слайды** с отдельным визуальным доказательством, передоказывающим **теорему возвращения** (не принцип отражения). Автор не вспомнен. Всплывёт — кладём сюда.

## F. Мир 2 — нить B (парковки ↔ деревья ↔ помеченные пути Дика)
- [x] Perkinson, Yang, Yu, «G-parking functions and tree inversions» — https://arxiv.org/pdf/1309.2201
- [x] Gaydarov, Hopkins, «Parking functions and tree inversions revisited» — https://arxiv.org/pdf/1506.03470
- [x] Hopkins, слайды — https://www.samuelfhopkins.com/docs/pf_talk.pdf
- [x] Shin, «A New Bijection Between Forests and Parking Functions» — https://arxiv.org/pdf/0810.0427
- [x] Armstrong, Loehr, Warrington, «Rational Parking Functions and Catalan Numbers» (опц., каталан-сторона) — https://arxiv.org/pdf/1403.1845
- Пропущено: Stanley, «Hyperplane arrangements, parking functions and tree inversions» (1998) — платный (Birkhäuser), открытого PDF не найдено.

## Статус получения (2026-07-03)
Получено в папке Downloads/«Перечислительная комбинаторика» (mount), **все читаются**: Стэнли (Catalan Numbers), Айгнер–Циглер (RU), Yan, Ardila, Dershowitz–Zaks, Pollak (arXiv), Addendum, Пак, Мерзон, Ландо, Вялый (`dm05` — короткий листок), Спивак «Числа Каталана» + Спивак-энциклопедия.
Постников 18.212: **[x]** три набора — официальный курс с Drive (`konspekty/18.212 [official, Spring 2025]/`; нужные лекции 01, 08, 09, 10, 11) + конспекты Yu и Ko. **[x] Loehr** — читаемая текстовая версия в `knigi/`. Комплект источников собран.
(по желанию: полный курс Вялого. Старый скан Loehr 273 МБ — удалить из Downloads вместе с продублированными оригиналами.)

## G. Мир 2 — волна ресёрча (сессия 4, 2026-07-04)
Приоритет волны — извлечь **рекурсивную биекцию Кревераса** (промах↔inv, выводимую из рекурренты) и проверить её школьность: это решает судьбу «поэлементного этажа». Большинство нужного УЖЕ в библиотеке — качать только новое.

**Читать из имеющегося (НЕ качать):**
- [ ] Yan (Handbook) §1.5–1.6 — искать явную рекурсивную конструкцию Кревераса (не только факт существования).
- [ ] Gaydarov–Hopkins (1506.03470), тело — рекурсивная vs нерекурсивная биекция, перенос статистик.
- [ ] Yu 18.212 §1 (первое возвращение $C_{k-1}C_{n-k}$, «many bijections») и §6 (Кэли ×4, §6.9 парковки) — мотивированные Дик↔дерево и три лица.
- [ ] Dershowitz–Zaks §2.2 (Trees) — цикл-лемма + отражение → матожидание высоты (Каталан-аналог «счастливых машин»).

**Докачать (новое, нет в библиотеке):**
- [ ] Stanley, «A Survey of Parking Functions» (transparencies) — https://math.mit.edu/~rstan/transparencies/parking3.pdf — возможна явная конструкция Кревераса + постановка задачи «нерекурсивная биекция».
- [ ] Zara, «Parking Functions, Stack-Sortable Permutations…», EJC 9(2) 2002, #R11 — https://www.combinatorics.org/ojs/index.php/eljc/article/download/v9i2r11/pdf — парковка → перестановка = 231-избегающая (мост через перестановки Кнута).
- [ ] Avron–Dershowitz, «Cayley's Formula: A Page from the Book» — https://www.cs.tau.ac.il/~nachumd/papers/Cayley.pdf — мотивированный Питман (одна страница).
- [ ] опц. Guedes de Oliveira–Las Vergnas, SLC B65e — https://www.mat.univie.ac.at/~slc/wpapers/s65guedlas.pdf — ещё одна нерекурсивная биекция парковка↔дерево.
- [ ] опц. Lin, ранние 18.212 notes — https://web.stanford.edu/~lindrew/18.212.pdf — стек-сортируемые / 231-избегающие школьно.

## H. Записки лекций + обзоры (волна пополнения, сессия 4)
Найдено разведкой. **Жирным — топ-кандидаты на «единый понятный текст».**

**Обзоры (EN):**
- [ ] **Martínez Mori, «WHAT IS… a Parking Function?», Notices AMS, авг. 2024** — https://www.ams.org/journals/notices/202408/rnoti-p1062.pdf (arXiv 2404.15372) — компактный школьно-доступный вход: парковки, (n+1)ⁿ⁻¹, связь с деревьями/Кэли.
- [ ] **Harris et al., «Parking Functions: Choose Your Own Adventure», College Math. J. 2021** — https://arxiv.org/pdf/2001.04817 — объединяет сюжет, мотивированные биекции, игровой формат; undergrad.
- [ ] опц. Mei Yin, «Parking functions: interdisciplinary connections» (2021) — https://arxiv.org/pdf/2107.01767 — graduate, вероятностный акцент.
- [ ] опц. Lillo–Rosas–Trandafir, «On Weary Drivers, Records of Trees, and Parking Functions» (2025) — https://arxiv.org/pdf/2506.22145 — свежая record-preserving биекция дерево↔парковка (источник идей).

**Записки лекций (EN):**
- [ ] **Emma Yang, «Labeled Trees and Parking Functions», Berkeley DRP, 2024** — https://wp.math.berkeley.edu/drp/wp-content/uploads/sites/18/2025/01/2024_Fall_Yang.pdf — образцовая мотивированная биекция дерево↔парковка с разобранным примером + обратный ход.
- [ ] Forcey et al., «Recursive bijections for Catalan objects», JIS 2013 (arXiv 1212.1188) — https://cs.uwaterloo.ca/journals/JIS/VOL16/Forcey/forcey.pdf — рекурсивные биекции объектов Каталана (в тему рекуррентной оси).
- [ ] опц. Cameron, LTCC Enumerative Combinatorics, лекция 3 «Catalan numbers» — https://maths.qmul.ac.uk/~pjc/ec/l3.pdf — чистый компактный конспект.
- (веб-реф, не PDF) Ardila, курс EC 2013, пост «Parking functions and Dyck paths» — https://icountslowly.wordpress.com/2013/10/20/parking-functions-and-dyck-paths/

**Русские (Кэли / Прюфер / цикл-лемма — по нашему сюжету):**
- [ ] **Ильинский–Купавский–Райгородский–Скопенков, «Дискретный анализ…», Мат. просвещение №17 (2013), с. 162–181** — https://old.mccme.ru/free-books/matpros/articles/МП-17/mp-17-pages-13.pdf — листок: код Прюфера, формула Кэли, деревья с заданными степенями. Кружок/олимпиада.
- [ ] **Яковлев (MathUs.ru), «Перечисление графов»** — https://mathus.ru/math/graphs-count.pdf — школьно-кружковый листок: Прюфер + Кэли + задачи.
- [ ] Бычков–Нурлигареев, «Введение в комбинаторику», Лекция 4 «Теорема Кэли» — https://lipn.fr/~nurligareev/files-teaching/2013-CombAlg-Bychkov-Nurligareev-Course-4.pdf — биективное док-во через Прюфера.
- [ ] Фейгин, «Дискретная математика» (ВШЭ) — https://math.hse.ru/discrete_2015 — листки seminar7/8_catalan.pdf, лекции Прюфер/Кэли/леса; **терминология: цикл-лемма = «лемма Рени»**. (Code: снять прямые PDF-ссылки с курс-страницы.)
- [ ] опц. Пак–Постников, «Перечисление остовных деревьев некоторых графов» (УМН, рус.) — https://www.math.ucla.edu/~pak/papers/PP-trees-Russian.pdf — код Реньи, ближе к парковкам; научный, для учителя.

**Пробел (важно):** «парковочная функция» по-русски в комбинаторном смысле — НЕ описана (пусто на mccme / hse / mathnet). Русскую подачу парковок строим сами с нуля; Кэли / Прюфер / цикл-лемма («Рени») по-русски покрыты хорошо.

## I. Мир 1 — волна разведки (арка «Мир 1», 2026-07-05)
Найдено разведкой Cowork (Фаза A/B); аннотации + таргеты — в `../../zhurnal/2026-07-05_mir1/razvedka-mir1.md`. Качать чистыми PDF в `biblioteka/istochniki/` (или в чат — разложу).
**Уже в библиотеке, только ЧИТАТЬ (не качать):** MIT 18.212 Notes 01/08 · Dershowitz–Zaks (§Trees) · Lin (231/стек-сорт) · Merzon (отражение) · Pak «History of Catalan numbers» (Эйлер–Сегнер, истор. крючок Л1).

**Таргет 1 — мосты / area в языках дерева и перестановки / путь↔Кнут:**
- [x] Bijections 231-avoiding ↔ Dyck (area↔inv), arXiv 0803.3706 — https://arxiv.org/abs/0803.3706
- [x] Linusson (KTH), «Pattern avoidance and Catalan numbers» — https://www.kth.se/social/files/5493dabff2765406ac5c8e75/CatalanEng.pdf
- [x] «Counting Dyck paths by area and rank», arXiv 1206.0803 — https://arxiv.org/abs/1206.0803
- [x] «On individual leaf depths of trees», arXiv 2302.05252 — https://arxiv.org/abs/2302.05252 (area↔глубины дерева)
- [x] «Catalan из биекции перестановки↔помеченные деревья», arXiv math/0112107 — https://arxiv.org/abs/math/0112107 (орбитный/цикл-лемма вкус)
- [x] опц. (advanced) «area-depth symmetric q,t-Catalan», arXiv 2109.06300 — https://arxiv.org/abs/2109.06300

**Таргет 2 — задачи-жемчужины:**
- [x] Bricklayer problem + Strong Cycle Lemma (Snevily–West, Monthly 1998), arXiv math/9802026 — https://arxiv.org/abs/math/9802026
- [x] «Generalized Chung–Feller Theorems for Lattice Paths», arXiv 0907.3254 — https://arxiv.org/abs/0907.3254
- [x] опц. (мост в Мир 2) «Lucky cars and lucky spots», arXiv 2412.07873 — https://arxiv.org/abs/2412.07873

**Таргет 3 — карта взаимосвязей деревья↔остальное / общий каркас:**
- [x] KTH thesis «Bijections on Catalan Structures» — https://kth.diva-portal.org/smash/get/diva2:820906/FULLTEXT01.pdf
- [x] «Signature Catalan Combinatorics», arXiv 1805.03863 — https://arxiv.org/abs/1805.03863
- [x] «Parking functions and Łukasiewicz paths», arXiv 2403.17438 — https://arxiv.org/abs/2403.17438 (общий путь)

**Педагогичные (решёточные пути / плоские деревья):**
- [x] Dziemiańczuk (Warsaw), «Counting lattice paths» — https://inf.ug.edu.pl/~mdziemia/kombinatoryka/counting-lattice-paths.pdf
- [x] Bender–Williamson (UCSD), «Rooted Plane Trees» (ch. 9) — https://mathweb.ucsd.edu/~ebender/CombText/ch-9.pdf
