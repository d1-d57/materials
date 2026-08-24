# Р1 — веб-ресёрч: есть ли объект у людей?

## Шапка

- **Тема**: одна производящая функция путей на отрезке {0..m} с потолком высоты m, СВОБОДНЫМИ КОНЦАМИ (из a в произвольную точку) и весом «длина × площадь», из которой специализациями выпадают Каталан, q-Каталан, гауссовы биномиальные, Роджерс–Рамануджан, Фибоначчи. Функциональное уравнение: F_m(x,q) = 1/(1 − x·F_{m−1}(qx,q)).
- **Дата данных**: 2026-08-24
- **Кто искал**: ox-alpha (веб-ресёрчер Р1)
- **Метод**: websearch + webfetch, проверка работ поимённо.

## Находки

1. **Philippe Flajolet, "Combinatorial aspects of continued fractions", Discrete Mathematics 32 (1980) 125–161.**
   - Проверено (несколько независимых источников, DOI 10.1016/0012-365X(80)90050-3).
   - Что доказано (одной фразой): формальная эквивалентность между J/S-продолженными дробями и характеристическими рядами взвешенных путей Мотцкина/Дика (падение с уровня i несёт вес β_i/α_i, горизонтальный шаг — γ_i), т.е. произвольные веса, зависящие от высоты, кодируются продолженной дробью.
   - Роль для кандидата: это каркас «пути в полосе ↔ дробь», но area-веса тут НЕ выделены — веса произвольны и статичны, а не «q растёт с высотой по ходу пути». Нужна доп. проверка, кто первым записал дробь с q-зависимыми коэффициентами как счёт площади.

2. **L. Carlitz, J. Riordan, «Two element lattice enumeration problems» / Carlitz–Riordan q-Catalan** (1964; Duquense? — уточнить журнал).
   - Проверено косвенно (многие вторичные источники: Sulzmast thesis, Alexandersson–Linusson arXiv:1206.0803, ELJC v18i1p158): C_n(q) = Σ_{Dyck(n)} q^area, рекурсия C_n(q) = Σ_k q^{k−1} C_{k−1}(q) C_{n−k}(q); «The distribution of area for Dyck paths has been studied by many, starting with Carlitz and Riordan [11]».
   - Роль: это q-Каталан как специализация кандидата (фиксированные концы 0→0 без потолка). У Карлица–Риордана НЕТ потолка высоты m и свободных концов — это одномерная рекурсия, а не функция F_m(x,q) полосы.
   - Точное название оригинала ещё проверить (возможно: L. Carlitz, J. Riordan, "Two element lattice enumeration problems", Abh. Math. Sem. Univ. Hamburg? — НЕ подтверждено).

3. **A. L. Owczarek, T. Prellberg, «Enumeration of area-weighted Dyck paths with restricted height», Advances in Applied Combinatorics (AJC?) / arXiv:1004.1699 (2010).**
   - Проверено: webspace.maths.qmul.ac.uk/t.prellberg/papers/pub079.pdf; ajc.maths.uq.edu.au/pdf/54/ajc_v54_p013.pdf (J. Austral. Math. Soc.? том 54, с.13); MaRDI подтверждает авторов.
   - Что доказано: явные выражения через q-биномиальные коэффициенты (суммы по m с (−t)^m q^{m(m−1)/2} [...]-биномиальные) для Dh(a,b; q,t) — производящей функции Дика-путей высоты ≤ h с весом «длина t × площадь q» и параметрами числа касаний нижней/верхней стенок.
   - Роль: БЛИЖАЙШИЙ сосед кандидата — полоса высоты h + area + длина есть. Отличия: у них пути Дика (фиксированные оба конца на 0), а не СВОБОДНЫЙ конец; ответ — ряд по m, а не простая цепная функция F_m; функциональное уравнение у них W(z)=A(z)+B(z)W(qz) для вспомогательной величины.
   
4. **Функциональное уравнение area-weighted Dyck paths без потолка: G(t,q) = 1 + t·G(t,q)·G(qt,q)** — встречается в нескольких работах школы Преллберга:
   - N. Haug, T. Prellberg, «Uniform asymptotics of area-weighted Dyck paths», J. Math. Phys. 56 (2015) 043301, arXiv:1412.5108: «By a standard factorization argument one obtains the functional equation G(t,q)=1+t G(t,q) G(qt,q)», решается анзацем G=H(qt)/H(t), H(t)=Σ q^{n²−n}(−t)^n/(q;q)_n.
   - Работа про везикулы (arXiv:1311.2174, давление везикулы): та же модель, и выписана непрерывная дробь G(z,q)=1/(1 − z/(1 − qz/(1 − q²z/(1 − …)))) и модифицированная G(z,q;κ)=1/(1−zκ·G(qz,q)) для веса контактов.
   - Роль: это кандидат БЕЗ потолка (m→∞, свободный конец = возврат на землю). Конечного потолка m тут нет; уравнение кандидата F_m(x,q)=1/(1−xF_{m−1}(qx,q)) — это в точности конечное усечение этой дроби, но у людей оно фигурирует лишь как промежуточный шаг факторизации, не как именованный объект.

5. **Nils Haug, Thomas Prellberg, Grzegorz Siudem, «Area-width scaling in generalised Motzkin paths», (2017, pub106, J. Phys. A / Elsevier open access).**
   - Проверено (webspace.maths.qmul.ac.uk/t.prellberg/papers/pub106.pdf).
   - Что сделано: ℓ-Мотцкин пути (горизонтальные шаги длины ℓ) с area-width генерирующей функцией; общее ФУ G(s,u,p,q)=1+sG+qu²G(ps,qu,p,q)G(s,u,p,q); для Дика совпадает с (14) G∞=1+aqt²G∞(qt,q)G∞.
   - Роль: показывает, что школа Преллберга систематически работает с area-взвешенными путями разных типов, но опять без потолка высоты как параметра семейства F_m.

6. **Cyril Banderier, Philippe Flajolet, «Basic analytic combinatorics of directed lattice paths», Theoret. Comput. Sci. 281 (2002) 37–80.**
   - Проверено (ScienceDirect, MathSciNet MR1909568, PDF авторов).
   - Что доказано: метод ядра даёт единую перечислительную и асимптотическую теорию направленных путей в полуплоскости/четверти (мосты, экскурсии, meanders); BGF меандров с u, отмечающим конечную высоту, алгебрична.
   - Роль: метод для кандидата, но area-весов у них нет вообще — только веса шагов; полоса {0..m} у них заменена полуплоскостью.

## Блок II: обзор Кратенталера — центральный источник

**Christian Krattenthaler, «Lattice Path Enumeration», глава 10 в Handbook of Enumerative Combinatorics (CRC Press, 2015), arXiv:1503.05930.**
Проверено полностью по arXiv HTML (v3, 2017). Ключевые куски:

7. **§10.9, Theorem 10.9.1 (Flajolet [42])**: GF взвешенных Мотцкин-путей из 0 в 0 ниже y=k — конечная J-дробь 1/(1−b₀−λ₁/(1−b₁−⋯−λ_k/(1−b_k)…)). Специализация λ_i=q^{i−1}z, b_i=0 даёт дробь Карлица–Риордана для q-Каталан: Σ C_n(q)z^n = 1/(1−z/(1−qz/(1−q²z/(1−…)))) (усечения = потолок высоты k).
8. **§10.11, Theorem 10.11.1**: GF Моткzkin-путей от высоты r к ПРОИЗВОЛЬНОЙ высоте s в полосе {0..k} с весами b_i (уровень на i), λ_i (спуск с i+1) выражается через ортогональные полиномы p_n(x) и их сдвинутые версии Sp_n: x^{s−r}p*_r·S^{s+1}p*_{k−s}/p*_{k+1}. Это в точности структура «свободный правый конец + потолок», доказано transfer-matrix через трёхдиагональную матрицу (путь Чебышёва). При b_i=0, λ_i=1 это классические полиномы Чебышёва (пример 10.11.2: подсчёт путей между диагоналями через cos/sin).
   - ВАЖНО ДЛЯ ВЕРДИКТА: у людей «свободный конец + потолок» есть как ОБЩАЯ теорема о произвольных высотных весах (Флажоле–Вьенно), а area-вес — как ЧАСТНЫЙ случай λ_i=q^{i−1}z того же каркаса. Но связка «именно F_m(x,q)=1/(1−xF_{m−1}(qx,q)) как именованный объект со свободным концом и area» в этом обзоре не выписана.
9. **§10.19**: q-Catalan Карлица–Риордана → дробь (10.163); подстановка z=−q превращает её в обратную к **дроби Рамануджана** (10.164): 1+q/(1+q²/(1+q³/…)) = Σq^{n²}/(q;q)_n ÷ Σq^{n(n+1)}/(q;q)_n; числитель/знаменатель — левые части **тождеств Роджерса–Рамануджана** (10.165)–(10.166): Σq^{n²}/(q;q)_n = 1/(q;q⁵)_∞(q⁴;q⁵)_∞ и т.д.
   - «The fact that we came across the left-hand sides by starting with lattice path counting problems may indicate that RR identities themselves may be linked with lattice path enumeration. **Bressoud was the first to actually set up such a link**».
10. **D. M. Bressoud, «Lattice paths and the Rogers–Ramanujan identities», в: Number Theory (Madras 1987), Lecture Notes in Math. 1395, Springer, Berlin, 1989, pp. 140–172.**
    - Проверено по библиографии Кратенталера [24] + вторично через arXiv:2312.15445 («In 1989, Bressoud provided a series of results on lattice paths, which included lattice path forms of the results related to Gordon, Andrews, and Bressoud»).
    - Что сделано: первый перевод RR-типа тождеств (Гордон/Андрюс/Брессуд) на язык решёточных путей с весами.
11. **L. Carlitz, J. Riordan, «Two element lattice path permutation numbers and their q-generalization», Duke Math. J.? (точный журнал проверить) — библиография Кратенталера [25].**
    - Точное название получено из библиографии Кратенталера; журнал не выписан в извлечённом фрагменте (пометка: НЕ проверен первичный выход).
12. **J. Bonin, L. Shapiro, R. Simion, «Some q-analogues of the Schröder numbers arising from combinatorial statistics on lattice paths»** — библиография Кратенталера [11]; журнал/год в извлечённом фрагменте не видны (пометка: НЕ проверено первично). Подсказка аналитика про «Bonin, Shapiro про полиномы Фибоначчи/Каталана с параметрами» соответствует этой линии (статистики на путях → q-аналоги Шрёдера).
13. **J. Cigler, «Fibonacci-Zahlen, Gitterpunktwege und die Identitäten von Rogers–Ramanujan»** — библиография Кратенталера [29]; Abh. Math. Sem. Univ. Hamburg? (НЕ проверено первично).

## Блок III: Циглер (Cigler) — q-Fibonacci как пути в полосе

14. **Johann Cigler, «q-Fibonacci polynomials and the Rogers-Ramanujan identities»** (preprint, homepage.univie.ac.at/johann.cigler/preprints/fibon.pdf).
    - Проверено по PDF автора.
    - Что сделано: Карлицевы q-Fibonacci полиномы F_n(t)=F_{n−1}(t)+q^{n−3}tF_{n−2}(t) представлены как веса решёточных путей в R², содержащихся в ПОЛОСЕ вдоль оси x (напр., пути в полосе −2≤y≤1); веса пиков q^m·t; выводятся конечные версии RR (Шур 1926), предельный переход даёт сами RR; комбинаторное доказательство включениями-исключениями.
    - Роль: у людей ЕСТЬ «пути в полосе фиксированной высоты с q-весами, зависящими от координаты» → конечные RR. Но вес — произведение весов ПИКОВ (экстремумов), а не площадь; рекурсия по длине n, а не по потолку m; концы фиксированы ((0,0)→(n,0) либо пары концов), свободного конца нет.
15. **Johann Cigler, «Some elementary aspects of q-Fibonacci and q-Lucas polynomials», arXiv:2209.08878 (2022)** и его же статьи EJC 10(1)R19 (2003) «A new class of q-Fibonacci polynomials», Fibonacci Quarterly 41 (2003) 35–45 (fq.math.ca/Scanned/41-1/cigler.pdf).
    - Проверено по PDF/arXiv.
    - Что сделано: q-Fibonacci полиномы F_n(x,s,q)=xF_{n−1}(x,qs,q)+qsF_{n−2}(x,q²s,q); производящая функция удовлетворяет F(x,s,z)=1+(xz+qsz²)F(x,qs,z) — ФУ с растяжкой аргумента qx; связь с Морзе-кодами, ортогональностью, pentagonal theorem; в FQ перечислены предшественники: Al-Salam–Ismail, Andrews–Knopfmacher–Paule, Carlitz, Ismail–Prodinger–Stanton, Schur.
    - Роль: семейство функций с ФУ вида «F(z)=A(z)F(qz)+B(z)» систематически изучается как q-Fibonacci; но это одномерная рекурсия по длине, не двухпараметрический потолок m полосы.

## Блок IV: уточнения по Bonin–Shapiro–Simion и деталям Преллберга

16. **J. E. Bonin, L. W. Shapiro, R. Simion, «Some q-analogues of the Schröder numbers arising from combinatorial statistics on lattice paths», J. Statist. Plann. Inference 34 (1993), no. 1, 35–55**, DOI 10.1016/0378-3758(93)90032-2.
    - Проверено (MathSciNet через страницу публикаций Симон на Rutgers, MaRDI, цитирования).
    - Что сделано: q-аналоги чисел Шрёдера из комбинаторных статистик (major index и др.) на решёточных путях.
    - Роль: линия «статистики на путях → q-аналоги», но без потолка высоты и без единой производящей функции полосы.

17. **Детали Owczarek–Prellberg (pub079), важные для кандидата**:
    - Их Dh(a,b;q,t) удовлетворяет функциональной рекурсии **Dh(a,b;q,t)=1+at·D_{h−1}(1,b;q,qt)·Dh(a,b;q,t)** и выписывается как УСЕЧЁННАЯ S-дробь: Dh=1/(1−at/(1−qt/(1−q²t/(⋯(1−bq^{h−1}t)…)))) — т.е. потолок h реализован как обрыв дроби с весом верхней стенки b.
    - Знаменатели Qh(a,b;q,t) подчинены трёхчленной рекурсии Qh=Q_{h−1}−bq^{h−1}tQ_{h−2} — это q-Fibonacci/q-Chebyshev тип.
    - Роль: это ближайшая к кандидату структура у людей (полоса + длина + площадь + параметр верхней стенки), НО: путь всегда возвращается на землю (конец фиксирован 0), старт фиксирован 0; нет суммы по произвольному правому концу; ФУ записано для Дика-объекта, а не для F_m(x,q) со свободным концом.

## Блок V: смежные линии (для карты окрестности)

18. **Alan J. Sokal, диссипативная линия branched continued fractions**: A. Sokal (с соавторами), «Lattice paths and branched continued fractions» (arXiv:1807.03271, с O. Dimitrov? — авторов проверить первично).
    - Проверено по PDF UCL discovery.
    - Что сделано: m-Stieltjes–Rogers и m-Thron–Rogers полиномы как GF m-Dyck/m-Schröder путей с height-dependent weights; partial m-Dyck paths «allowed to end anywhere» — свободный конец появляется здесь естественно; доказана коэфициентная ганкелева тотальная положительность.
    - Роль: свободный конец + произвольные высотные веса есть, area-специализации (λ_i=q^{i−1}) упоминаются как приложения, но объекта «F_m(x,q) с потолком и area» тут тоже нет.
19. **Стековые полимино / Ferrers диаграммы с area+периметром**: функциональные уравнения вида G_s(x,y,q)=y/(1−qx)^s·G_s(qx,y,q)+… решаются итерацией: G_s=Σ q^n xy^n/((1−q^nx)(qx;q)_{n−1}^s); стеки считаются площадью: S(q)=Σ q^n/((q)_n(q)_n) (Auluck 1951; Bousquet-Mélou et al. 1999 самодвойственность; Guttmann–Conway–Prellberg обзор arXiv:0811.4415; Richard et al. cond-mat/0107329).
    - Роль: та же механика растяжки аргумента q·x при подсчёте площади, но объекты — полимино, а не пути со свободным концом.
20. **Stieltjes–Wigert / q-ортогональные полиномы**: классические S/J-дроби с q-коэффициентами (Stieltjes §56: c_{2n}=(q;q)_{n−1}q^n, c_{2n+1}=q^{2n+1}(q;q)_n; Wigert w_k(x)=e^{−k²log²x}; обзор Van Assche «The impact of Stieltjes' work...»).
    - Роль: аналитическая сторона того же каркаса (дробь с q-зависимыми звеньями ↔ ортогональные полиномы); у Преллберга прямо сказано, что их полиномы — q-ортогональные. Отдельной работы «Stieltjes-Wigert = paths with free endpoint and area» не найдено.

21. **R. Brak, A. L. Owczarek, «Anisotropic step, surface contact, and area weighted directed walks on the triangular lattice», J. Phys. A (2003)** (CiteseerX doi 10.1.1.492.6903).
    - Проверено по аннотации CiteseerX.
    - Что сделано: GF полностью направленных путей на треугольной решётке с весом за каждый тип шага, за площадь между путём и стенкой полуплоскости и за контакты со стенкой; явные формулы суммарных area-производящих функций и моментов высоты; методы ECO/marked area; ответы в виде отношений бесконечных q-рядов и цепных дробей.
    - Роль: area-взвешенные направленные пути ЕСТЬ у людей, но геометрия — полуплоскость (стенка снизу), не полоса {0..m}; свободный конец не выделен как параметр.

22. **R. Brak, J. Osborn, «Chebyshev type lattice path weight polynomials by a constant term method», J. Phys. A: Math. Theor. 42 (2009) 445201.**
    - Проверено по PDF авторов (ANU).
    - Что сделано: CT-теорема для весовых полиномов Ballot/Motzkin путей в ПОЛОСЕ высоты L с фиксированным числом «декорированных» весов и фоновым весом; через ортогональные полиномы (в т.ч. неклассические чебышёвского типа); новое доказательство теоремы Вьенно диагонализацией transfer-matrix; применение к модели ДиМарцио–Рубина (полимер в щели с весами стенок κ, ω).
    - Роль: полоса высоты L + произвольные высотные веса + ортогональные полиномы — всё есть; area-веса не выделены.

23. **Cyril Banderier, Philippe Nicodème, «Bounded discrete walks», DMTCS Proceedings (AofA 2010).**
    - Проверено по PDF (lipn.univ-paris13.fr).
    - Что сделано: метод ядра даёт GF мостов/отражённых мостов заданной высоты для произвольного набора шагов; отмечено: «the height has already been investigated mainly for Dyck paths which have a nice relationship with continued fractions and Chebyshev polynomials»; про area под путями сказано, что она исследовалась в другой статье тех же авторов.
    - Роль: современный kernel-method каркас для полосы; area тут не центральный параметр.

## ВЕРДИКТ

**Есть ли объект у людей и как называется: единого объекта НЕ найдено.**
Ни одна проверенная работа не вводит и не изучает F_m(x,q) — производящую функцию путей из фиксированной точки в ПРОИЗВОЛЬНУЮ точку полосы {0..m} с весом «длина × площадь» — как самостоятельный именованный объект. Имени у кандидата в литературе нет. При этом ВСЕ компоненты кандидата существуют по отдельности, и кандидат лежит на пересечении четырёх известных линий:

1. **Каркас Флажоле–Вьенно** (Flajolet 1980; Krattenthaler гл.10 §10.9–10.11; Brak–Osborn 2009): пути в полосе высоты k с ЛЮБЫМИ высотными весами ↔ конечная J-дробь; свободный конец r→s выражается через ортогональные полиномы (Theorem 10.11.1). Area-вес — частный случай λ_i=q^{i−1}z, но именно этот случай у них не выделен.
2. **q-Каталан Карлица–Риордана → усечённая дробь → Рамануджан → Роджерс–Рамануджан** (Carlitz–Riordan; Krattenthaler §10.19; Bressoud 1989; Schur 1926 / Cigler): ΣC_n(q)z^n = 1/(1−z/(1−qz/(1−…))) — это кандидат при m→∞ и конце 0→0; конечные усечения = потолок высоты, но рассматриваются лишь как сходящиеся дроби, не как функция полосы со свободным концом.
3. **Area-weighted Dyck paths with restricted height** (Owczarek–Prellberg 2010): БЛИЖАЙШИЙ сосед — полоса высоты h, вес длина×площадь, ответ усечённой S-дробью и через q-ортогональные полиномы; их рекурсия Dh=1+at·D_{h−1}(1,b;q,qt)·Dh структурно совпадает с уравнением кандидата, НО концы фиксированы (0→0), свободный конец отсутствует.
4. **Школа Преллберга без потолка**: G(t,q)=1+tG(t,q)G(qt,q), решение H(qt)/H(t) (Haug–Prellberg 2015); непрерывная дробь 1/(1−z/(1−qz/(…))) (vesicle-работа arXiv:1311.2174).

**Чего не хватает (что искать не удалось ни одной из ≥12 формулировок запросов):**
- связки «свободный правый конец» × «area-вес»: сумма по всем конечным высотам как главный объект не выписана никем из найденных;
- записи именно рекуррентности F_m(x,q)=1/(1−xF_{m−1}(qx,q)) как определения объекта (у людей либо факторизация без потолка, либо усечённая дробь для Дика-путей);
- имени/термина: ближайшие существующие названия — «area-weighted Dyck paths with restricted height», «усечённая S-дробь Карлица–Риордана», «convergents дроби Рамануджана», «Motzkin paths in a strip (Flajolet–Viennot)».

Следствие для захода: кандидат не опровергнут («у людей такого нет» относится к объекту как целому, а не к его частям), но он собирается из стандартных деталей — претензия владельца может быть только в УПАКОВКЕ (одна функция вместо четырёх линий литературы + свободный конец + явное ФУ), а не в новых ингредиентах.

## Список использованных формулировок поиска (обоснование отрицательного вывода)

1. Flajolet combinatorics continued fractions Motzkin paths (1980)
2. Carlitz Riordan q-Catalan numbers Dyck paths area enumeration
3. Prellberg area-weighted Dyck paths enumeration functional equation
4. Banderier Flajolet directed lattice paths kernel method 2002
5. Rogers-Ramanujan identities lattice paths area quadratic exponent
6. Cigler q-Fibonacci polynomials continued fraction
7. Bonin Shapiro Simion q-analogues Schröder numbers statistics journal
8. Stieltjes-Wigert orthogonal polynomials continued fraction Motzkin q-area
9. stack polyominoes functional equation area perimeter Tutte
10. Dyck prefixes / partial Dyck paths q-analogue area bounded height
11. Brak Owczarek Prellberg directed walks walls area weight polymer strip
12. q-Chebyshev polynomials lattice paths bounded height strip

## Непроверенное / хвосты

- Точный журнал статьи Carlitz–Riordan (библиографическая запись [25] у Кратенталера: название «Two element lattice path permutation numbers and their q-generalization»; журнал в извлечённом фрагменте не виден).
- Первичная запись Cigler «Fibonacci-Zahlen, Gitterpunktwege und die Identitäten von Rogers–Ramanujan» (Abh. Math. Sem. Univ. Hamburg — НЕ проверено).
- Авторы статьи arXiv:1807.03271 «Lattice paths and branched continued fractions» — Sokal с соавторами (по PDF UCL виден только Sokal; полный список авторов не выписан).
- Статья Banderier–Nicodème, где «area under the walks» исследована отдельно ([6] в их списке) — не открыта.
