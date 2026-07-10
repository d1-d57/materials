# MANIFEST — источники проекта (что где лежит)

Физическая раскладка `biblioteka/istochniki/`. Аннотации, оценка, карта покрытия — в `../istochniki-perechislitelnaya.md`. Чеклист загрузки — `SPISOK-skachat.md`. Дайджесты «что есть / чего нет» после каждого чтения — `istochniki/VYCHITANO.md`.
Обновлено 2026-07-04. Все файлы **читаются** (текстовый слой), кроме отмеченного скана Loehr.

## knigi/ — книги
- `Loehr — Bijective Combinatorics (2011).pdf` — 600 стр. Единый биективный учебник (Дик · деревья · парковки · цикл-лемма). Текстовая версия, читается.
- `Stanley — Catalan Numbers (2015).pdf` — 224 стр. Каталог 214 интерпретаций (энциклопедия, не нарратив).
- `Aigner, Ziegler — Proofs from THE BOOK (RU).pdf` — глава про формулу Кэли = 4 красивых доказательства (Прюфер · Жойяль · Риордан–Реньи · Питман) + цикл-лемма.
- `Lando — Лекции о производящих функциях.pdf` — ПФ; неожиданно широк (цикл-лемма, Кэли, Прюфер).
- `Spivak — Новая школьная энциклопедия (математика).pdf` — 256 стр., картиночная школьная подача (Дик×91).

## konspekty/ — конспекты курсов (нужная «форма»)
- **`18.212 [official, Spring 2025]/`** — полный курс Постникова по лекциям (картиночный, с Drive — «тот самый»). **Нужны:** `Notes 01. Catalan Numbers`, `08. Trees`, `09. Arrangements, Parking`, `10. More Graphs`, `11. Misc Topics`. Мимо (контекст курса): 02 Young · 03 Permutations · 04 Posets · 05 More Young · 06 q-Analogs · 07 Partitions (+ `info.pdf`, `diagrams.pdf`).
- `Yu — MIT 18.212 Algebraic Combinatorics (2026).pdf` — 60 стр. ОБА МИРА в одном: §1 Каталан (Дик / цикл-сдвиги=цикл-лемма / отражение / первое возвращение Cₖ₋₁Cₙ₋ₖ / «Many bijections»); §6 остовные деревья (Кэли ×4, §6.9 парковки); §7 BEST.
- `Ko — MIT 18.212 Concise Algebraic Combinatorics.pdf` — 39 стр. §11 Parking Functions, §11.1 **Labeled Dyck Paths** (ключ владельца).
- `Ardila — Algebraic & geometric methods in enumerative combinatorics.pdf` — 143 стр. Биективные методы, деревья→Дик.
- `Vyalyi — ВШЭ ДМ, семинар 5 (числа Каталана).pdf` — короткий листок (образец жанра «листочек»).
- `Bychkov, Nurligareev — Введение в комбинаторику, Лекция 4 (Теорема Кэли).pdf` — 1 стр. Биективное док-во формулы Кэли через код Прюфера, кружковый жанр.
- `Cameron — LTCC Enumerative Combinatorics, Lecture 3 Catalan Numbers.pdf` — 6 стр. Компактный конспект лекции про числа Каталана.
- `Feigin — ВШЭ ДМ, seminar7_catalan.pdf` — 10 стр. Листок семинара 7 (осенний поток курса «Дискретная математика», ВШЭ) про числа Каталана; см. `## Требует внимания` — остальные ссылки страницы неоднозначны, не скачаны.
- `Forcey et al. — Recursive bijections for Catalan objects (JIS 2013).pdf` — 18 стр. Рекурсивные биекции между объектами Каталана (arXiv 1212.1188).
- `Ilyinsky, Kupavsky, Raigorodsky, Skopenkov — Дискретный анализ (Мат. просвещение №17, 2013).pdf` — 19 стр. Листок: код Прюфера, формула Кэли, деревья с заданными степенями (кружок/олимпиада).
- `Lin — MIT 18.212 early notes.pdf` — ранние студенческие конспекты 18.212 (стек-сортируемые перестановки, 231-избегающие).
- `Yang — Labeled Trees and Parking Functions (Berkeley DRP 2024).pdf` — образцовая мотивированная биекция дерево↔парковка с разобранным примером и обратным ходом.
- `Linusson — Pattern Avoidance and Catalan Numbers (KTH 2014).pdf` — 6 стр. Конспект лекции SF2741 (KTH); Таргет 1, педагогичный вход в area↔inv через избегание паттернов.
- `Dziemiańczuk — Counting Lattice Paths (Warsaw 2015).pdf` — 85 стр. (диссертация PhD, Univ. of Gdańsk/Warsaw). Педагогичный фон Таргетов 1/3: решёточные пути, разные биекции.
- `Bender, Williamson — Rooted Plane Trees, ch.9 (UCSD 2005).pdf` — 20 стр. (глава учебника «Lists, Decisions and Graphs»). Педагогичный фон Таргета 3: плоские корневые деревья, рекурсии.
- `Ammar — Bijections on Catalan Structures (KTH thesis 2015).pdf` — 72 стр. (магистерская, рук. Linusson). Таргет 3: систематическая карта биекций между объектами Каталана.

## stati-obzory/ — статьи и обзоры
- `Kreweras — Une famille de polynômes ayant plusieurs propriétés énumeratives (Periodica Math. Hung. 1980).pdf` — ОРИГИНАЛ тождества Кревераса (фр., 1980; получен от владельца, сессия 4). Ещё НЕ разобран — статус в `VYCHITANO.md`.
- `Yan — Parking functions (Handbook 2015).pdf` — ГЛАВНЫЙ обзор мира Кэли; единственный с «labeled Dyck», парковки↔деревья.
- `Dershowitz, Zaks — The Cycle Lemma and some applications (1990).pdf` — цикл-лемма как мост (Каталан ↔ Кэли).
- `Pollak — weakly increasing parking functions (arXiv 2511.20796).pdf` — циклический аргумент для (n+1)ⁿ⁻¹.
- `Pak — History of Catalan numbers.pdf` — история.
- `Stanley — Catalan Addendum (EC2).pdf` — 96 стр., доп. интерпретации.
- `Merzon — Диаграммы Юнга, пути на решётке и метод отражений.pdf` — отражение + пути↔определитель (RU, педагогично).
- `Spivak — Числа Каталана (статья).pdf` — три десятка определений на рисунках (жанр кристаллизации).
- `Perkinson, Yang, Yu — G-parking functions and tree inversions (arXiv 1309.2201).pdf` — ядро нити B: биективно доказывает тождество Кревераса area = инверсии деревьев через burning-алгоритм Дхара.
- `Gaydarov, Hopkins — Parking functions and tree inversions revisited (arXiv 1506.03470).pdf` — чистое современное экспозе нити B.
- `Hopkins — Parking functions and tree inversions (slides).pdf` — школьно-пригодная подача той же нити (слайды).
- `Shin — A New Bijection Between Forests and Parking Functions (arXiv 0810.0427).pdf` — нерекурсивная биекция лес ↔ парковка; несёт inv↔jump (=area↔displacement) ПОЭЛЕМЕНТНО (Lemma 2), sandpile-free. Вписана в `kurs/mir2-skelet.md` Сегмент 4 (Теорема 4.7).
- `Armstrong, Loehr, Warrington — Rational Parking Functions and Catalan Numbers (arXiv 1403.1845).pdf` — опц., каталан-сторона: рациональные парковочные функции и числа Каталана.
- `Pak — Increasing trees and alternating permutations.pdf` — (Kuznetsov, Pak, Postnikov, 1994) индуктивная биекция 0-1-2 возрастающих деревьев ↔ знакочередующихся перестановок (числа Эйлера), §2. Вписана в `kurs/mir2-skelet.md` Сегмент 6.2.
- `Slavik, Vestenicka — Lucky Cars.pdf` — элементарный (круговой приём Поллака) вывод E[lucky] для парковочных функций и обобщений; формула сверена с `kurs/mir2-skelet.md` Сегмент 6.1 — совпадает.
- `Avron, Dershowitz — Cayley's Formula, A Page from the Book.pdf` — мотивированное однострочное (Питмана) доказательство формулы Кэли, «одна страница».
- `Guedes de Oliveira, Las Vergnas — SLC B65e.pdf` — 10 стр. Ещё одна нерекурсивная биекция парковка↔дерево.
- `Harris et al. — Parking Functions, Choose Your Own Adventure (2021).pdf` — обзор-игра (College Math. J.): сюжет + мотивированные биекции парковок, undergrad-жанр.
- `Lillo, Rosas, Trandafir — On Weary Drivers, Records of Trees, and Parking Functions (2025).pdf` — свежая record-preserving биекция дерево↔парковка (источник идей).
- `Martinez Mori — WHAT IS a Parking Function (Notices AMS 2024).pdf` — компактный школьно-доступный обзор-вход: парковки, (n+1)ⁿ⁻¹, связь с деревьями/Кэли.
- `Pak, Postnikov — Перечисление остовных деревьев некоторых графов (УМН, рус.).pdf` — код Реньи (цикл-лемма = «лемма Рени»), ближе к парковкам; научный жанр, для учителя.
- `Stanley — A Survey of Parking Functions (transparencies).pdf` — 69 стр. слайды-обзор парковок.
- `Yin — Parking functions, interdisciplinary connections (2021).pdf` — graduate-обзор, вероятностный акцент.
- `Zara — Parking Functions, Stack-Sortable Permutations (EJC 2002).pdf` — биекция парковка → 231-избегающая перестановка (мост через перестановки Кнута).
- `Stump — On Bijections between 231-avoiding Permutations and Dyck Paths (arXiv 2008).pdf` — 13 стр. Таргет 1: биекция 231-избег.↔Дик через major index; связь с q,t-Каталан.
- `Blanco, Petersen — Counting Dyck Paths by Area and Rank (arXiv 2012).pdf` — 24 стр. Таргет 1: совместное распределение area и rank (решётка noncrossing partitions).
- `Elizalde — On Individual Leaf Depths of Trees (arXiv 2023).pdf` — 42 стр. Таргет 1: поэлементные глубины листьев/вершин в разных видах деревьев и путях Дика.
- `Vance — A Derivation of the Catalan Numbers from a Bijection between Permutations and Labeled Trees (arXiv 2001).pdf` — 10 стр. Таргет 1: биекция перестановки↔помеченные деревья, вывод Cₙ.
- `Pappe, Paul, Schilling — An Area-Depth Symmetric q,t-Catalan Polynomial (arXiv 2021).pdf` — 17 стр. Таргет 1 (опц., продвинуто): area-depth симметрия через инволюцию на плоских деревьях.
- `Snevily, West — The Bricklayer Problem and the Strong Cycle Lemma (arXiv 1998).pdf` — 14 стр. Таргет 2: задача-жемчужина, Strong Cycle Lemma (Monthly 1998).
- `Huq — Generalized Chung-Feller Theorems for Lattice Paths (arXiv 2009).pdf` — 86 стр. (диссертация, Brandeis, науч. рук. Gessel). Таргет 2: обобщения теоремы Chung–Feller.
- `Ceballos, González D'León — Signature Catalan Combinatorics (arXiv 2018).pdf` — 42 стр. Таргет 3: s-Catalan обобщение (Fuss-Каталан, рациональный Каталан как частные случаи), биекции дерево/путь/312-избег.
- `Selig, Zhu — Parking Functions and Łukasiewicz Paths (arXiv 2024).pdf` — 9 стр. Таргет 3: биекция невозрастающие парковки ↔ пути Лукасевича.
- `Butler et al. — Lucky Cars and Lucky Spots in Parking Functions (arXiv 2024).pdf` — 16 стр. Таргет 2 (опц., мост в Мир 2): lucky cars/spots в парковочных функциях.

## Требует внимания
- **Loehr** — читаемая текстовая версия получена (`knigi/Loehr … (2011).pdf`, 600 стр.). Старый скан 273 МБ остался в Downloads → к удалению.
- **Курс 18.212 [official] с Drive** — получен целиком в `konspekty/18.212 [official, Spring 2025]/`; нужные лекции 01, 08, 09, 10, 11.
- **Фейгин (math.hse.ru/discrete_2015)** — страница смешивает 2 потока (осень 2015/2016 + весна 2016) без прямых PDF на сами лекции (только текстовые аннотации с литературой на Ландо). Однозначно распознан и скачан только `seminar7_catalan.pdf` → `konspekty/Feigin — ВШЭ ДМ, seminar7_catalan.pdf`. `seminar8_catalan.pdf` из SPISOK на странице НЕ существует (реальный файл — `seminar8.pdf`, без суффикса, тема по номеру лекции похожа на разбиения/производящие функции, не Прюфер/Кэли); лекции 1–4 весеннего потока (Прюфер, Кэли, леса) описаны текстом без отдельного PDF. Полный список найденных ссылок — в отчёте захода `kod_biblioteka-dobor.md`.
- **Яковлев, «Перечисление графов» (mathus.ru/math/graphs-count.pdf)** — НЕ скачан: таймаут соединения (2 попытки, до 90 сек). Сайт mathus.ru не отвечал в момент захода — не paywall/404, а сетевая недоступность. Файла нет.

## Ключевой синтез-таргет
Слой «помеченные пути Дика ↔ парковки ↔ деревья»: `konspekty/Ko …` §11.1 + `stati-obzory/Yan …`. С него стартует граф утверждений.
