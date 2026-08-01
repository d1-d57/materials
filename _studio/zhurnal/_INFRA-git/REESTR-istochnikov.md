# РЕЕСТР ИСТОЧНИКОВ — все PDF репозитория, один список

> **Собран командой, руками не править — правка умрёт при следующей пересборке:**
> ```
> python3 _studio/zhurnal/_INFRA-git/sobrat_reestr.py
> ```
> Сами PDF в git НЕ идут (`.gitignore`) — идёт только этот список. Он и есть
> ответ на «что у нас вообще есть», когда файлов не видно с другой машины.

**Зачем источники лежат на диске и почему их нельзя удалять.** Владелец: *«я их
скачиваю, потому что мы по ним делаем поиск, когда хотим узнать конкретную
информацию, которую нельзя установить из интернета… иногда нам нужно из всех
книжек взять упражнения»*. Ценность — в **локальном полнотекстовом поиске**;
удаление её убивает. Сжатие тоже: PDF уже сжаты, ghostscript даёт 10–20 % и
портит формулы, zip ломает сам поиск.

**Числа — не вписаны, а посчитаны сборщиком в момент сборки:**

| | |
|---|---|
| файлов | **166** |
| суммарный вес | **378.1 МБ** |
| с дайджестом в `VYCHITANO.md` | 115 |
| без дайджеста (механизм в проекте есть) | 39 |
| механизма дайджестов в проекте нет | 12 |

Сверить число файлов с диском, не веря этой таблице:
```
find . -name "*.pdf" -not -path "./.git/*" | wc -l
grep -c '^| `' _studio/zhurnal/_INFRA-git/REESTR-istochnikov.md
```

⚠ **Что значит «✓» и чего оно НЕ значит.** Отметка ставится грубо: имя файла
упомянуто в ближайшем вверх по дереву `VYCHITANO.md`. Это метод самого проекта
(шапка `teoriya-kategoriy/istochniki/VYCHITANO.md`), и он отвечает на вопрос
«заводили ли по файлу дайджест», а **не** «прочитан ли он целиком». Прочерк «—»
означает не «не читан», а что в проекте нет самого файла `VYCHITANO.md`.

| Путь | Размер | Проект | `VYCHITANO` |
|---|---|---|---|
| `_fond/zadachi/arhiv-lmsh57-2025/stanciya-listok.pdf` | 25.2 КБ | _fond | — |
| `catalan/biblioteka/istochniki/knigi/Aigner, Ziegler — Proofs from THE BOOK (RU).pdf` | 7.6 МБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/knigi/Haglund — The q,t-Catalan Numbers and Diagonal Harmonics.pdf` | 1.1 МБ | catalan | нет |
| `catalan/biblioteka/istochniki/knigi/Lando — Лекции о производящих функциях.pdf` | 1.1 МБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/knigi/Loehr — Bijective Combinatorics (2011).pdf` | 4.9 МБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/knigi/Sagan — Combinatorics, The Art of Counting (AMS prepub draft).pdf` | 2.0 МБ | catalan | нет |
| `catalan/biblioteka/istochniki/knigi/Spivak — Новая школьная энциклопедия (математика).pdf` | 17.1 МБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/knigi/Stanley — Catalan Numbers (2015).pdf` | 5.2 МБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/knigi/Stanley — Enumerative Combinatorics vol.1 (2nd ed, 2011 draft).pdf` | 4.4 МБ | catalan | нет |
| `catalan/biblioteka/istochniki/knigi/Stanley — Topics in Algebraic Combinatorics (2013, free).pdf` | 1.2 МБ | catalan | нет |
| `catalan/biblioteka/istochniki/konspekty/18.212 [official, Spring 2025]/Notes 01. Catalan Numbers.pdf` | 399.3 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/18.212 [official, Spring 2025]/Notes 02. Young Tableaux.pdf` | 687.1 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/18.212 [official, Spring 2025]/Notes 03. Permutations.pdf` | 920.1 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/18.212 [official, Spring 2025]/Notes 04. Partially Ordered Sets.pdf` | 625.6 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/18.212 [official, Spring 2025]/Notes 05. More Young Diagrams.pdf` | 1.8 МБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/18.212 [official, Spring 2025]/Notes 06. q-Analogs.pdf` | 490.9 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/18.212 [official, Spring 2025]/Notes 07. Partitions.pdf` | 719.9 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/18.212 [official, Spring 2025]/Notes 08. Trees.pdf` | 2.0 МБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/18.212 [official, Spring 2025]/Notes 09. Arrangements, Parking.pdf` | 1.0 МБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/18.212 [official, Spring 2025]/Notes 10. More Graphs.pdf` | 508.4 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/18.212 [official, Spring 2025]/Notes 11. Misc Topics.pdf` | 981.5 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/18.212 [official, Spring 2025]/diagrams.pdf` | 845.4 КБ | catalan | нет |
| `catalan/biblioteka/istochniki/konspekty/18.212 [official, Spring 2025]/info.pdf` | 20.3 КБ | catalan | нет |
| `catalan/biblioteka/istochniki/konspekty/Ammar — Bijections on Catalan Structures (KTH thesis 2015).pdf` | 829.1 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/Ardila — Algebraic & geometric methods in enumerative combinatorics.pdf` | 1.4 МБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/Bender, Williamson — Rooted Plane Trees, ch.9 (UCSD 2005).pdf` | 227.0 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/Bychkov, Nurligareev — Введение в комбинаторику, Лекция 4 (Теорема Кэли).pdf` | 124.0 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/Cameron — LTCC Enumerative Combinatorics, Lecture 3 Catalan Numbers.pdf` | 94.4 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/Dziemiańczuk — Counting Lattice Paths (Warsaw 2015).pdf` | 1.8 МБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/Feigin — ВШЭ ДМ, seminar7_catalan.pdf` | 236.9 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/Forcey et al. — Recursive bijections for Catalan objects (JIS 2013).pdf` | 535.6 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/Ilyinsky, Kupavsky, Raigorodsky, Skopenkov — Дискретный анализ (Мат. просвещение №17, 2013).pdf` | 600.1 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/Ko — MIT 18.212 Concise Algebraic Combinatorics.pdf` | 448.2 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/Lin — MIT 18.212 early notes.pdf` | 764.9 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/Linusson — Pattern Avoidance and Catalan Numbers (KTH 2014).pdf` | 154.6 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/Vyalyi — ВШЭ ДМ, семинар 5 (числа Каталана).pdf` | 190.7 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/Yang — Labeled Trees and Parking Functions (Berkeley DRP 2024).pdf` | 217.2 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/konspekty/Yu — MIT 18.212 Algebraic Combinatorics (2026).pdf` | 830.5 КБ | catalan | нет |
| `catalan/biblioteka/istochniki/stati-obzory/Armstrong, Loehr, Warrington — Rational Parking Functions and Catalan Numbers (arXiv 1403.1845).pdf` | 621.5 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Avron, Dershowitz — Cayley's Formula, A Page from the Book.pdf` | 138.1 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Blanco, Petersen — Counting Dyck Paths by Area and Rank (arXiv 2012).pdf` | 274.5 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Butler et al. — Lucky Cars and Lucky Spots in Parking Functions (arXiv 2024).pdf` | 189.8 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Ceballos, González D'León — Signature Catalan Combinatorics (arXiv 2018).pdf` | 683.0 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Dershowitz, Zaks — The Cycle Lemma and some applications (1990).pdf` | 265.0 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Elizalde — On Individual Leaf Depths of Trees (arXiv 2023).pdf` | 484.1 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Gaydarov, Hopkins — Parking functions and tree inversions revisited (arXiv 1506.03470).pdf` | 2.1 МБ | catalan | нет |
| `catalan/biblioteka/istochniki/stati-obzory/Guedes de Oliveira, Las Vergnas — SLC B65e.pdf` | 164.8 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Harris et al. — Parking Functions, Choose Your Own Adventure (2021).pdf` | 3.9 МБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Hopkins — Parking functions and tree inversions (slides).pdf` | 2.4 МБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Huq — Generalized Chung-Feller Theorems for Lattice Paths (arXiv 2009).pdf` | 1.0 МБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Kreweras — Une famille de polynômes ayant plusieurs propriétés énumeratives (Periodica Math. Hung. 1980).pdf` | 522.0 КБ | catalan | нет |
| `catalan/biblioteka/istochniki/stati-obzory/Lillo, Rosas, Trandafir — On Weary Drivers, Records of Trees, and Parking Functions (2025).pdf` | 481.9 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Martinez Mori — WHAT IS a Parking Function (Notices AMS 2024).pdf` | 6.4 МБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Merzon — Диаграммы Юнга, пути на решётке и метод отражений.pdf` | 1.7 МБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Pak — History of Catalan numbers.pdf` | 266.9 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Pak — Increasing trees and alternating permutations.pdf` | 1.5 МБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Pak, Postnikov — Перечисление остовных деревьев некоторых графов (УМН, рус.).pdf` | 148.5 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Pappe, Paul, Schilling — An Area-Depth Symmetric q,t-Catalan Polynomial (arXiv 2021).pdf` | 270.7 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Perkinson, Yang, Yu — G-parking functions and tree inversions (arXiv 1309.2201).pdf` | 183.4 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Pollak — weakly increasing parking functions (arXiv 2511.20796).pdf` | 1.0 МБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Selig, Zhu — Parking Functions and Łukasiewicz Paths (arXiv 2024).pdf` | 210.7 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Shin — A New Bijection Between Forests and Parking Functions (arXiv 0810.0427).pdf` | 353.3 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Slavik, Vestenicka — Lucky Cars.pdf` | 156.1 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Snevily, West — The Bricklayer Problem and the Strong Cycle Lemma (arXiv 1998).pdf` | 143.6 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Spivak — Числа Каталана (статья).pdf` | 102.8 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Stanley — A Survey of Parking Functions (transparencies).pdf` | 479.1 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Stanley — Catalan Addendum (EC2).pdf` | 590.6 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Stump — On Bijections between 231-avoiding Permutations and Dyck Paths (arXiv 2008).pdf` | 192.1 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Vance — A Derivation of the Catalan Numbers from a Bijection between Permutations and Labeled Trees (arXiv 2001).pdf` | 109.6 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Yan — Parking functions (Handbook 2015).pdf` | 358.5 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Yin — Parking functions, interdisciplinary connections (2021).pdf` | 283.7 КБ | catalan | ✓ |
| `catalan/biblioteka/istochniki/stati-obzory/Zara — Parking Functions, Stack-Sortable Permutations (EJC 2002).pdf` | 124.8 КБ | catalan | ✓ |
| `fibonacci/istochniki/pdf/Benjamin, Quinn - Proofs that Really Count.pdf` | 2.5 МБ | fibonacci | нет |
| `fibonacci/istochniki/pdf/Комбинаторные тождества.pdf` | 1.3 МБ | fibonacci | ✓ |
| `fibonacci/istochniki/pdf/Числа_Фибоначчи.pdf` | 126.2 КБ | fibonacci | ✓ |
| `graph-course/istochniki/pdf/chetnost_01-Chetnost.pdf` | 335.7 КБ | graph-course | ✓ |
| `graph-course/istochniki/pdf/graf_02-Grafy.pdf` | 1019.3 КБ | graph-course | ✓ |
| `graph-course/istochniki/pdf/kanel-belov_KanKov.pdf` | 656.0 КБ | graph-course | ✓ |
| `graph-course/istochniki/pdf/neprer_12-Neprer.pdf` | 136.1 КБ | graph-course | ✓ |
| `graph-course/istochniki/pdf/shapovalov_uzkoe.pdf` | 154.7 КБ | graph-course | ✓ |
| `graph-course/istochniki/pdf/turniry_10-Turniry.pdf` | 1.1 МБ | graph-course | ✓ |
| `informacia-i-kody/istochniki/pdf/dorichenko-yashchenko-25-etudov-o-shifrah.pdf` | 1.3 МБ | informacia-i-kody | нет |
| `informacia-i-kody/istochniki/pdf/fkn-diskretnaya-matematika-lekcii.pdf` | 2.6 МБ | informacia-i-kody | нет |
| `informacia-i-kody/istochniki/pdf/kleptsyn-kvantik-2024-07-magicheskie-kartochki.pdf` | 479.3 КБ | informacia-i-kody | нет |
| `informacia-i-kody/istochniki/pdf/kleptsyn-kvantik-2024-08-vas-ploho-slyshno.pdf` | 423.1 КБ | informacia-i-kody | нет |
| `informacia-i-kody/istochniki/pdf/knop-vzveshivaniya-shmk05.pdf` | 1.1 МБ | informacia-i-kody | ✓ |
| `informacia-i-kody/istochniki/pdf/kriptografia-komandnaya-igra.pdf` | 767.1 КБ | informacia-i-kody | нет |
| `informacia-i-kody/istochniki/pdf/kvant-1977-08-vilenkin-matematika-i-shifry.pdf` | 5.0 МБ | informacia-i-kody | нет |
| `informacia-i-kody/istochniki/pdf/matprazdnik-2023-book.pdf` | 615.8 КБ | informacia-i-kody | нет |
| `informacia-i-kody/istochniki/pdf/matprazdnik-2024-book.pdf` | 373.4 КБ | informacia-i-kody | нет |
| `informacia-i-kody/istochniki/pdf/matprazdnik-2025-book.pdf` | 2.3 МБ | informacia-i-kody | нет |
| `informacia-i-kody/istochniki/pdf/matprazdnik-2026-book.pdf` | 2.7 МБ | informacia-i-kody | нет |
| `informacia-i-kody/kartoteka/L3-print.pdf` | 21.1 КБ | informacia-i-kody | — |
| `informacia-i-kody/kartoteka/L4-print.pdf` | 20.8 КБ | informacia-i-kody | — |
| `krivaya-drakona/istochniki/pdf/kvant-2020-01-vasilev-gutenmaher-krivye-drakona.pdf` | 1.2 МБ | krivaya-drakona | нет |
| `krivaya-drakona/istochniki/pdf/kvant_1970_2_vasilev-gutenmaher_krivyie-drakona.pdf` | 5.9 МБ | krivaya-drakona | нет |
| `krivaya-drakona/kartoteka/L1-print.pdf` | 30.6 КБ | krivaya-drakona | — |
| `krivaya-drakona/kartoteka/L2-print.pdf` | 21.2 КБ | krivaya-drakona | — |
| `krivaya-drakona/kartoteka/L3-print.pdf` | 13.2 КБ | krivaya-drakona | — |
| `krivaya-drakona/kartoteka/L4-print.pdf` | 16.1 КБ | krivaya-drakona | — |
| `kurs leto 2026/6-lending/pitch-plakat.pdf` | 93.6 КБ | kurs leto 2026 | — |
| `kurs leto 2026/biblioteka/Кому нужна математика (Нелли Литвак, Андрей Райгородский).pdf` | 2.9 МБ | kurs leto 2026 | — |
| `matchings/matchings.pdf` | 499.8 КБ | matchings | — |
| `nagliadnaya-geometriya/istochniki/mccme/6kl-12-razvertki.pdf` | 544.8 КБ | nagliadnaya-geometriya | нет |
| `nagliadnaya-geometriya/istochniki/mccme/6kl-16-svyazi.pdf` | 75.6 КБ | nagliadnaya-geometriya | нет |
| `nagliadnaya-geometriya/istochniki/mccme/6kl-18-razrezanie.pdf` | 77.0 КБ | nagliadnaya-geometriya | нет |
| `nagliadnaya-geometriya/istochniki/mccme/6kl-23-obhody.pdf` | 112.1 КБ | nagliadnaya-geometriya | нет |
| `nagliadnaya-geometriya/istochniki/mccme/6kl-25-kvadraty-kletki.pdf` | 100.3 КБ | nagliadnaya-geometriya | нет |
| `nagliadnaya-geometriya/istochniki/mccme/6kl-29-billiard.pdf` | 292.4 КБ | nagliadnaya-geometriya | нет |
| `nagliadnaya-geometriya/istochniki/mccme/geom7-03_kletki.pdf` | 140.1 КБ | nagliadnaya-geometriya | нет |
| `nagliadnaya-geometriya/istochniki/mccme/geom7-04_pik.pdf` | 279.0 КБ | nagliadnaya-geometriya | нет |
| `nagliadnaya-geometriya/istochniki/mccme/geom7-05_sgibaniya.pdf` | 535.7 КБ | nagliadnaya-geometriya | нет |
| `nagliadnaya-geometriya/istochniki/pdf/sharygin-nagliadnaya-geometria-1992.pdf` | 8.2 МБ | nagliadnaya-geometriya | ✓ |
| `nagliadnaya-geometriya/istochniki/pdf/Мерзон Ященко Длин, площадь, объем.pdf` | 1.2 МБ | nagliadnaya-geometriya | ✓ |
| `nagliadnaya-geometriya/istochniki/polina/inzhenernoe-origami-deck.pdf` | 40.3 МБ | nagliadnaya-geometriya | ✓ |
| `nagliadnaya-geometriya/istochniki/polina/inzhenernoe-origami-kvantik-chernovik.pdf` | 3.6 МБ | nagliadnaya-geometriya | ✓ |
| `nagliadnaya-geometriya/istochniki/polina/optika-konicheskie-secheniya.pdf` | 16.7 МБ | nagliadnaya-geometriya | ✓ |
| `teoriya-kategoriy/istochniki/pdf/adamek-herrlich-strecker-joy-of-cats.pdf` | 4.2 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/altenkirch-lazy-fp-1-2.pdf` | 464.8 КБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/altenkirch-lazy-fp-3.pdf` | 485.0 КБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/altenkirch-lazy-fp-4.pdf` | 392.0 КБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/altenkirch-lazy-fp-5.pdf` | 297.5 КБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/aluffi-algebra-chapter-0.pdf` | 4.2 МБ | teoriya-kategoriy | нет |
| `teoriya-kategoriy/istochniki/pdf/asperti-longo-categories-types-structures.pdf` | 1.6 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/atiyah-macdonald-commutative-algebra.pdf` | 3.8 МБ | teoriya-kategoriy | нет |
| `teoriya-kategoriy/istochniki/pdf/awodey-category-theory-2ed.pdf` | 1.1 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/baez-category-theory-course.pdf` | 423.6 КБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/baez-dolan-finite-sets-to-feynman-diagrams.pdf` | 219.5 КБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/baez-euler-characteristic-vs-homotopy-cardinality.pdf` | 161.6 КБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/baez-stay-rosetta-stone.pdf` | 845.4 КБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/barr-wells-category-theory-computing-science.pdf` | 2.0 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/bradley-what-is-applied-ct.pdf` | 7.1 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/cheng-cambridge-category-notes.pdf` | 1014.3 КБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/cheng-mfa23-session1.pdf` | 3.8 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/cheng-mfa23-session2.pdf` | 2.3 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/cheng-mfa23-session3.pdf` | 2.2 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/cheng-the joy of abstraction - an exploration of math, category .pdf` | 8.2 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/ct2019-lecture5-curry-howard-lambek.pdf` | 193.0 КБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/eilenberg-maclane-1942-natural-isomorphisms-group-theory.pdf` | 624.8 КБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/eilenberg-maclane-1945-general-theory-natural-equivalences.pdf` | 5.7 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/fong-spivak-seven-sketches-in-compositionality.pdf` | 2.9 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/gelfand-manin-methods-homological-algebra-en.pdf` | 8.6 МБ | teoriya-kategoriy | нет |
| `teoriya-kategoriy/istochniki/pdf/hatcher-algebraic-topology.pdf` | 3.7 МБ | teoriya-kategoriy | нет |
| `teoriya-kategoriy/istochniki/pdf/hott-book.pdf` | 3.0 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/lawvere-schanuel-conceptual-mathematics-2ed.pdf` | 13.6 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/leinster-basic-category-theory.pdf` | 1.2 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/maclane-categories-working-mathematician-en.pdf` | 5.7 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/maclane-ru-fizmatlit2004.pdf` | 30.2 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/mazur-when-is-one-thing-equal.pdf` | 513.7 КБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/milewski-category-theory-for-programmers.pdf` | 15.7 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/milne-fields-and-galois-theory.pdf` | 1.8 МБ | teoriya-kategoriy | нет |
| `teoriya-kategoriy/istochniki/pdf/mit-programming-with-categories-notes.pdf` | 853.5 КБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/nesin-very-introductory-notes-ct.pdf` | 546.5 КБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/perrone-notes-on-category-theory.pdf` | 1.4 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/pierce-basic-category-theory-cs-1991.pdf` | 8.3 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/pierce-taste-of-category-theory-cmu-1988.pdf` | 2.3 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/riehl-category-theory-in-context.pdf` | 1.5 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/ru-lekciya-1-kategorii-funktory.pdf` | 337.5 КБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/shafarevich-basic-notions-of-algebra-en.pdf` | 5.3 МБ | teoriya-kategoriy | нет |
| `teoriya-kategoriy/istochniki/pdf/smith-introducing-category-theory-3ed.pdf` | 3.0 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/spivak-category-theory-for-scientists-2013.pdf` | 3.9 МБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/spivak-kent-ologs.pdf` | 637.7 КБ | teoriya-kategoriy | ✓ |
| `teoriya-kategoriy/istochniki/pdf/vakil-rising-sea-2015.pdf` | 3.4 МБ | teoriya-kategoriy | нет |
| `teoriya-kategoriy/istochniki/pdf/yorgey-2014-species-and-labelled-structures.pdf` | 1.6 МБ | teoriya-kategoriy | нет |
| `teorkat/lekciya-1.pdf` | 6.7 МБ | teorkat | — |
| `ucheniki/literatura/shen-igry-i-strategii.pdf` | 855.3 КБ | ucheniki | — |
