# R1. Явная модель исследовательского процесса в математике

Ресёрч под задачу: 15 стартующих / 12 доехавших школьных матпроектов в школе 179, руководители — практикующие математики, исполнители — десятиклассники.

---

## 1. Сводка

Главный вывод: **единой канонической модели «как вести исследование» не существует, но существует четыре независимо возникших описания, которые сходятся в деталях** — и их пересечение можно предъявить школьнику как рабочий алгоритм.

Что есть:

- **Пойа** — единственный, кто дал формальный список шагов и эвристик. Но его схема заточена под задачу с известным ответом. Вторая книга («Mathematics and Plausible Reasoning») уже про исследование: индукция по малым случаям, аналогия, проверка догадки, специализация/обобщение. Это ближе всего к тому, что нужно.
- **Практики (Атья, Боллобаш, Сарнак, Макдафф, Тао, Терстон)** — дают не алгоритм, а *набор режимов работы и правил переключения между ними*. Ключевое у всех: (а) начинать с простейших случаев и примеров, (б) держать несколько задач разной сложности одновременно, (в) «застрять» — норма, а не сбой.
- **Программы (Duluth REU Галлиана, PRIMES, RSI, PROMYS/Ross)** — единственные, кто описал ЯВНО *критерии подбора задачи* и *ритм работы*, потому что им приходится это масштабировать на десятки новичков в год. Галлиан — самый ценный источник по вашему вопросу.
- **Дидактика (Moore method, IBL, guided reinvention Фройденталя)** — про то, как устроен обратный дизайн: ведущий знает пункт назначения, ученик проходит путь сам.

Что важнее всего для 179:
1. Критерии Галлиана к задаче (четыре штуки, дословно) — прямое попадание в вашу проблему.
2. Правило Галлиана «начинаю лето с вдвое большим числом задач, чем студентов» и его признание, что **половина задач оказывается негодной** — и это нормальная эксплуатационная норма, а не провал.
3. Еженедельный доклад о прогрессе перед группой — единственный найденный механизм ранней диагностики «проект умирает».
4. Развилка «ментор умеет решить / ментор сам бьётся» решается не выбором одного полюса, а конструкцией «свежая статья + открытый вопрос из неё»: ментор владеет контекстом и техникой, но не знает ответа.

---

## 2. Пять конкурирующих явных моделей процесса

### Модель A. Пойа: четыре фазы + эвристический вопросник

**Источник:** G. Pólya, *How to Solve It* (1945); *Mathematics and Plausible Reasoning*, т. I–II (1954).

Четыре фазы:
1. **Понять задачу.** Что дано? Что ищем? Каково условие? Нарисовать. Ввести обозначения. Переформулировать своими словами.
2. **Составить план.** Здесь работает вопросник:
   - Видел ли я такую задачу раньше? Похожую?
   - Знаю ли родственную задачу? Теорему, которая могла бы пригодиться?
   - Можно ли переформулировать? Иначе?
   - Если не выходит — **решите более частную задачу**. Более общую. Аналогичную. Отбросьте часть условия.
   - Можно ли получить *что-нибудь* из данных? Что нужно, чтобы прийти к искомому (работа с конца)?
   - Все ли данные использованы?
3. **Выполнить план.** Проверять каждый шаг: очевиден ли он, можете ли доказать.
4. **Оглянуться назад (looking back).** Проверить результат. Проверить рассуждение. Можно ли получить иначе? Можно ли использовать результат или метод в другой задаче?

Фаза 4 — **точка, где решение задачи превращается в исследование**. Именно из «оглянуться назад» рождается следующий вопрос. Для школьного проекта это ключевая операция: цикл «решил малый случай → looking back → новый вопрос» и есть двигатель года.

Вторая книга (том I «Induction and Analogy in Mathematics», том II «Patterns of Plausible Inference») — рабочая схема исследования:
- посчитать частные случаи → заметить закономерность → сформулировать гипотезу → **испытать гипотезу на новых, специально неудобных случаях** → искать доказательство → при неудаче ослабить гипотезу.
- Явно вводится «правдоподобное рассуждение» как легитимный этап: догадка со статусом «пока не доказано» — это результат, а не позор.

Ограничение модели: у Пойа задача всегда поставлена. Постановка вопроса вне схемы.

---

### Модель B. Атья: вопрос → контекст → примеры → метод → доказательство

**Источник:** M. Atiyah, «Advice to a Young Mathematician», в *The Princeton Companion to Mathematics*, VIII.6.
https://assets.press.princeton.edu/releases/gowers/gowers_VIII_6.pdf

Порядок явно назван:

> «In mathematics, ideas and concepts come first, then come questions and problems. At this stage the search for solutions begins, one looks for a method or strategy. Once you have convinced yourself that the problem has been well-posed, and that you have the right tools for the job, you then begin to think hard about the technicalities of the proof.»

И следующим шагом — переформулировка задачи, а не отказ от неё:

> «Before long you may realize, perhaps by finding counterexamples, that the problem was incorrectly formulated. … You then have to go back and refine your formalization of the problem.»

Стратегия входа в задачу:

> «It is a good idea to start thinking hard about a problem as soon as you have fully absorbed it. To get to grips with it, there is no substitute for a hands-on approach. **You should investigate special cases and try to identify where the essential difficulty lies.**»

Про роль примеров (это прямо про вычислительный эксперимент):

> «It is essential to be able to test general results by applying them to simple examples. … These are examples where one can do concrete calculations, sometimes with elaborate formulas, that help to make the general theory understandable. **They keep your feet on the ground.**»
> «But most of all a good example is a thing of beauty. It shines and convinces. … It provides the bedrock of belief.»

Про происхождение задачи — важно для руководителя:

> «A good problem always has antecedents: it arises from some background, it has roots. You have to understand these roots in order to make progress. That is why it is always better to find your own problem, asking your own questions, rather than getting it on a plate from your supervisor. **If you know where a problem comes from, why the question has been asked, then you are halfway toward its solution.**»

И честная оценка искусства постановки:

> «The art in good mathematics … is to identify and tackle problems that are both interesting and solvable.»

Отдельно — режим «любопытства как двигателя»: при чтении статьи или на семинаре постоянно спрашивать «когда это верно? это лучшее доказательство? в какой общности результат живёт?». Атья честно пишет: девять раз из десяти это тупик («nine times out of ten it turns out to be a blind alley»), но десятый окупает.

---

### Модель C. Боллобаш–Сарнак: портфель задач + режим застревания

**Источник:** тот же файл, разделы II (Bollobás) и V (Sarnak).

Боллобаш даёт **явную конструкцию портфеля**, которую можно буквально скопировать в школу:

> (i) «A “dream”: a big problem that you would love to solve, but you cannot reasonably expect to solve.»
> (ii) «Some very worthwhile problems that you feel you should have a good chance of solving, given enough time, effort, and luck.»
> плюс (iii) задачи «below your dignity», которые решаются быстро, и (iv) красивые нерабочие задачки для удовольствия.

Его правило про малые случаи:

> «Avoid pedestrian approaches, but always be happy to put in work. In particular, **doing the simplest cases of a problem is unlikely to be a waste of time** and may well turn out to be very useful.»

Про фиксацию промежуточного (прямой ответ на «упёрся и забыл, что уже сделал»):

> «When you spend a significant amount of time on a problem, it is easy to underestimate the progress you have made, and it is equally easy to overestimate your ability to remember it all. **It is best to write down even your very partial results.**»

Про страх пустого листа:

> «What you should be terrified of is a blank sheet in front of you after having thought about a problem for a little while. **If after a session your wastepaper basket is full of notes of failed attempts, you may still be doing very well.**»

Про чтение литературы — контринтуитивно и важно для школьника:

> «It is often useful not to read up everything about an open problem you are about to attack: once you have thought deeply about it and apparently got nowhere, you can (and should) read the failed attempts of others.»

Сарнак (научрук со стажем) даёт критерий, который прямо решает вопрос заказчика о «задаче, которую ментор умеет решить»:

> «Most of the time one is stuck, and **if this is not the case for you, then either you are exceptionally talented or you are tackling problems that you knew how to solve before you started.** There is room for some work of the latter kind, and it can be of a high quality, but most of the big breakthroughs are earned the hard way.»

И его формулировка роли руководителя:

> «The role of a senior mentor is more like that of a **coach**: one provides encouragement and makes sure that the person being mentored is working on interesting problems and is aware of the basic tools that are available.»

---

### Модель D. Галлиан (Duluth REU): производственный цикл на 10 недель

**Источники:**
- J. Gallian, «The Duluth Undergraduate Research Program 1977–2006», Proceedings of the Conference on Promoting Undergraduate Research in Mathematics, AMS, 2007. https://www.d.umn.edu/~jgallian/PURMweb/duluthreu.pdf
- https://www.d.umn.edu/~jgallian/progdesc.html

Это единственный источник, где описан весь конвейер. Шаги:

1. **Поиск задач.** Просмотр свежих журналов, arXiv, конференции, письма коллегам. Область — теория графов, комбинаторика, теория чисел (мало предварительных знаний, много места для изобретательности).
2. **Запас.** «As a rule of thumb, I begin the summer with **twice the number of problems as I have students**.»
3. **Выдача.** «Each student is given his or her own problem together with **an article or two as resource material**.» Обычно в статье есть гипотезы и открытые вопросы.
4. **Еженедельный доклад перед всей группой.** «Each week the participants give talks on their progress during the previous week to the group. This gives me, the research advisers and visitors an opportunity to assess progress, raise questions, make suggestions and **identify difficulties**. Preparing their talks helps the students organize their work.»
5. **Пересборка при провале задачи.** «It sometimes happens — **about half the time in fact** — that a problem is inappropriate. Sometimes a problem is too easy or too hard; sometimes we discover it is already solved by someone else. In these cases I simply assign a new one.»
6. **К седьмой неделе (из десяти) — начало письменной работы.** «Ideally, by the seventh week of the program the students are writing up their work. Papers are written in a style suitable for submission to a research journal.»
7. **Многоступенчатое чтение черновика.** «All manuscripts are read by me, the two research advisers, and one or more visitors.»
8. **Follow through** — самая тяжёлая часть, по признанию Галлиана: доведение текста до публикации после окончания программы.

Отдельно — среда: студенты живут в смежных квартирах, обедают вместе три раза в неделю, среда — выездной день. Галлиан подчёркивает: **это не украшение, это часть конструкции** («The living arrangements naturally foster interaction and collaboration»). Плюс постоянное присутствие «старших» — двух бывших участников в роли research advisers и полутора десятков выпускников программы, приезжающих на неделю-три.

---

### Модель E. Терстон: понимание вместо доказательства

**Источник:** W. Thurston, «On proof and progress in mathematics», Bull. AMS 30 (1994) 161–177. https://arxiv.org/abs/math/9404236

Тезис: прогресс в математике — это рост человеческого *понимания*, а не накопление доказанных утверждений. Правильный вопрос про деятельность математика — не «какие теоремы он доказал», а «насколько он продвинул понимание людей».

Практические следствия для проекта:
- Терстон перечисляет разные *способы думать* об одном объекте (для производной: символьный, инфинитезимальный, наклон касательной, скорость, аппроксимация, микроскоп…). Смена способа мышления — легитимный ход при застревании.
- Ценным результатом считается не только теорема, но: новое определение, удачное обозначение, контрпример, вычислительный эксперимент, ясная экспозиция чужого результата. **Для школы это критично: расширяет множество «доехавших» проектов.**
- Знание передаётся в основном не через тексты, а через людей и разговор. Отсюда: без регулярного живого общения проект не идёт.

Дополнение — знаменитый ответ Терстона на MathOverflow «Thinking and Explaining» (вопрос 38639): математики думают внутренними, невербализуемыми образами, и «перевод» из этого режима в текст — отдельная тяжёлая работа, которой надо учить отдельно.

---

### Модель F (дидактическая рамка). Guided reinvention / Moore method / IBL

- **Фройденталь, «guided reinvention»**: ученик переоткрывает содержание сам, но по спроектированной траектории; учитель заранее строит «гипотетическую траекторию обучения» и вмешивается минимально.
- **Moore method**: преподаватель выдаёт определения и утверждения, запрещает литературу, ученики доказывают всё сами и защищают у доски. Из него выросло современное **Inquiry-Based Learning** (см. Academy of Inquiry Based Learning, Journal of Inquiry-Based Learning in Mathematics).
- Общий каркас: руководитель знает пункт назначения и рельеф, ученик идёт сам; вмешательство — только когда ученик остановился, и в форме вопроса, а не ответа.

Это не модель исследования, а **модель поведения руководителя**. Её надо ставить поверх моделей A–E.

---

## 3. Критерии подбора задачи для новичка

### 3.1 Галлиан — четыре критерия, дословно

> «Obviously, the selection of appropriate problems is of fundamental importance to a successful research program. I search for problems that meet the following criteria: **not much background reading is required; partial results are probable; recently posed; new results will likely be publishable.**»

Разбор под школу 179:

| Критерий Галлиана | Перевод на школьный язык |
|---|---|
| not much background reading | вход в задачу — не больше 2–3 недель чтения; иначе год уйдёт на подготовку |
| **partial results are probable** | самое важное: задача должна быть устроена так, что частичный результат почти неизбежен. Это и есть гарантия «доехавшего» проекта |
| recently posed | задача не обсосана; в интернете нет готового ответа |
| new results likely publishable | есть внешняя инстанция, признающая результат (для школы — конференция, «Турнир городов»/ВКР-защита, препринт) |

Плюс метакритерий про подбор пары:

> «Matching students with problems is a critical task. **The skill with which this is done is a major factor in the success of a program.**»

И — критично для планирования на 15 проектов:

> «As a rule of thumb, I begin the summer with twice the number of problems as I have students.»
> «It sometimes happens — about half the time in fact — that a problem is inappropriate.»

**То есть: чтобы 12 проектов доехали, надо стартовать не с 15, а иметь в запасе ~30 задач и быть готовым к замене примерно половины.** Галлиан считает замену задачи штатной операцией, а не катастрофой.

Выбор области:

> «Graph theory, combinatorics and number theory provide the source of most of the problems» — потому что они «accessible to people without much background», а решения «rely more on creativity, insight and raw talent and less on using existing results and mastering known techniques».

### 3.2 Как ищутся задачи

Галлиан: «I find problems by perusing recently published journals, math arXiv, attending conferences, and writing people.» То есть источник задачи — **свежая статья с разделом open problems / conjectures**, а не собственная фантазия руководителя.

### 3.3 «Ментор умеет решить» vs «ментор сам бьётся»

Прямых текстов на эту тему мало, но три источника дают ответ вместе:

1. **Сарнак**: если ты не застреваешь, значит, ты решаешь то, что уже умел решать. Задача, которую руководитель умеет решать, — не исследование по определению.
2. **Галлиан** решает дилемму конструктивно: он **не знает решения**, но **знает область, знает свежую статью, знает, что частичный результат вероятен**. Асимметрия не в знании ответа, а во владении контекстом и в умении оценить, что вообще считается продвижением.
3. **Атья**: «If you know where a problem comes from, why the question has been asked, then you are halfway toward its solution.» — Руководитель обязан владеть *происхождением* задачи. Это то, что он даёт вместо ответа.

Практический критерий для 179: руководитель должен уметь ответить на вопросы «откуда эта задача взялась», «что уже про неё известно», «какой первый нетривиальный случай», «как выглядел бы минимальный публикуемый результат» — и **не должен** уметь ответить «а какой ответ».

Опасность обратного полюса — задача, об которую бьётся сам ментор: у неё, как правило, нет свойства «partial results are probable», и она не проходит критерий 2 Галлиана. Именно этот критерий и отделяет одно от другого.

Историческая контрастная практика — Литтлвуд (по Атье):

> «J. E. Littlewood is reported to have set each of his research students to work on a **disguised version of the Riemann hypothesis**, letting them know what he had done only after six months. … The policy may not have led to a proof of the Riemann hypothesis, but it certainly led to resilient and battle-hardened students.»

Приводится как курьёз, а не как рекомендация. Для школы неприменимо: цена — год жизни ребёнка.

---

## 4. Что делать, когда упёрся

Сводный протокол по всем источникам, от дешёвого к дорогому.

**Уровень 0. Нормализация.**
Сарнак: «Doing research in mathematics is frustrating and if being frustrated is something you cannot get used to, then mathematics may not be an ideal occupation for you. **Most of the time one is stuck.**» — Это первое, что должен услышать десятиклассник. Застревание — рабочий режим, а не сигнал провала.

**Уровень 1. Спуститься вниз по сложности (Пойа + Боллобаш + Атья).**
- Решить более частный случай. n = 1, 2, 3. Самый маленький нетривиальный пример.
- Отбросить часть условия и решить ослабленную задачу.
- Наоборот: решить более общую («парадокс изобретателя» Пойа — общая задача бывает легче).
- Атья: «investigate special cases and **try to identify where the essential difficulty lies**» — цель спуска не в ответе, а в локализации трудности.

**Уровень 2. Вычислительный эксперимент.**
- Посчитать много случаев, искать закономерность. Проверить последовательность в OEIS. Написать перебор.
- Пойа (Plausible Reasoning): после появления гипотезы — **специально искать неудобные случаи** для её проверки, а не подтверждающие.
- Атья про роль примеров: «They keep your feet on the ground.»

**Уровень 3. Сменить представление.**
- Терстон: переключиться на другой способ думать об объекте (алгебраический ↔ геометрический ↔ комбинаторный ↔ вероятностный).
- Пойа: переформулировать задачу; работать с конца (что нужно, чтобы получить искомое).
- Атья: «My own approach has been to try to avoid the direct onslaught and look for indirect approaches.»

**Уровень 4. Записать и разложить.**
- Боллобаш: записывать даже совсем частичные результаты — иначе прогресс недооценивается, а память переоценивается.
- Галлиан: подготовка еженедельного доклада сама по себе — инструмент («Preparing their talks helps the students organize their work»).

**Уровень 5. Вынести наружу.**
- Доклад перед группой (Галлиан) — главный штатный механизм. Именно на нём руководитель «identify difficulties».
- Разговор с другими участниками. Галлиан прямо культивирует горизонтальный обмен: «Cooperation rather than competition is stressed.»
- Ваиль: разговаривать с другими много, ходить на семинары, даже когда понимаешь 5%.

**Уровень 6. Читать чужие неудачи.**
Боллобаш: сначала подумать самому и упереться, **потом** читать, что пробовали другие. В обратном порядке — теряется собственная интуиция.

**Уровень 7. Переключить задачу, не бросая.**
- Боллобаш: держать портфель из «мечты» и «реалистичных» задач; переключаться.
- Сарнак: «attack these on and off over time, looking at them from different points of view».
- Конн: считать в уме на долгой прогулке без бумаги; работать лёжа в темноте. (Буквально: «go for a long walk (no paper or pencil) and do the computation in one's head».)

**Уровень 8. Признать задачу негодной и заменить.**
Галлиан: примерно половина задач негодна; замена — штатное действие, выполняемое руководителем без драмы. **Это должно быть заранее объявленным правилом, а не поражением.**

**Роль руководителя в момент застревания** (Галлиан, дословно):

> «Undergraduate students, even the most talented ones, have a tendency to become frustrated and want to give up too soon. Here I serve as a **counselor and cheerleader**, offering **an idea, a reference or a pep talk**.»

Три вида интервенции — идея / ссылка / моральная поддержка. Ничего больше.

---

## 5. Роль вычислительного эксперимента и малых случаев — сводка

Все источники сходятся, что это первый ход и главный источник гипотез:

- **Пойа**: индукция по малым случаям — основной путь к догадке; догадка со статусом «правдоподобно» — легитимный промежуточный результат.
- **Атья**: коллекция конкретных примеров, на которых можно реально считать, — личный капитал математика, накапливаемый годами.
- **Боллобаш**: «doing the simplest cases of a problem is unlikely to be a waste of time».
- **Макдафф**: «often one sees further by **starting with the simplest questions and examples**, because that makes it easier to understand the basic problem and then perhaps to find a new approach to it». Она прямо называет своей ошибкой в аспирантуре противоположную привычку — «I often used to start in the middle, using some complicated theory already developed by others».
- **Ваиль**: «When you learn the theory, you should try to calculate some toy cases, and think of some explicit basic examples»; и — про происхождение задач — «I'll suggest problems to think about, **starting from small toy problems (which have a habit of growing into interesting serious research)**».
- **Терстон**: вычислительный эксперимент — полноправная форма продвижения понимания, даже без теоремы.

Для школы: **обязательный первый месяц любого проекта — счёт малых случаев и накопление таблицы данных**. Это дешёвая проверка, что задача вообще жива, и одновременно гарантия, что у проекта будет хоть какой-то предъявимый материал.

---

## 6. Программы для школьников и студентов — что взять из устройства

- **MIT PRIMES** (https://math.mit.edu/research/highschool/primes/program/) — годовой формат, ближайший аналог школы 179. Ритм: ≥10 ч/нед, **полуторачасовая еженедельная встреча с ментором**; в начале — чтение по теме и **пятистраничный reading report, одобряемый ментором, к началу марта**; затем финализация проекта; доклад на осенней конференции; финальная статья, публикуемая на сайте программы. Задачи предлагает преподаватель MIT, ведёт аспирант/постдок, есть фигура head mentor как арбитра.
  → Взять: reading report как формальные ворота между «вхождением в тему» и «исследованием»; фигуру старшего ментора над руководителями.
- **RSI** (Research Science Institute, MIT) — 6 недель, обязательный письменный отчёт + устный доклад, жёсткие дедлайны на abstract / draft / final.
- **Ross / PROMYS** — не исследование, а «think deeply of simple things»: длинные серии задач без лекций, ученик переоткрывает теорию чисел. Готовит именно ту привычку (счёт примеров → гипотеза → доказательство), на которой потом стоит исследование. Галлиан прямо пишет, что выпускники Ross/PROMYS/Hampshire приходят к нему хорошо подготовленными.
- **Duluth REU** — см. модель D.
- **Budapest Semesters in Mathematics** — комбинаторный уклон, Галлиан считает участие маркером годности к его программе.

---

## 7. Источники

**Классика**
- G. Pólya. *How to Solve It*. Princeton UP, 1945 (рус.: «Как решать задачу»).
- G. Pólya. *Mathematics and Plausible Reasoning*, vol. I «Induction and Analogy in Mathematics», vol. II «Patterns of Plausible Inference». Princeton UP, 1954 (рус.: «Математика и правдоподобные рассуждения»).
- G. Pólya. *Mathematical Discovery*, 1962–65.

**Практики**
- M. Atiyah, B. Bollobás, A. Connes, D. McDuff, P. Sarnak. «Advice to a Young Mathematician», in *The Princeton Companion to Mathematics*, VIII.6, Princeton UP, 2008. PDF в открытом доступе: https://assets.press.princeton.edu/releases/gowers/gowers_VIII_6.pdf
- W. P. Thurston. «On proof and progress in mathematics». Bull. AMS 30 (1994) 161–177. https://arxiv.org/abs/math/9404236
- W. P. Thurston. Ответ на вопрос «Thinking and Explaining», MathOverflow, вопрос 38639.
- T. Tao. Career advice. https://terrytao.wordpress.com/career-advice/
  — в частности: «Solving mathematical problems» https://terrytao.wordpress.com/career-advice/solving-mathematical-problems/ ; «Ask yourself dumb questions — and answer them!» https://terrytao.wordpress.com/career-advice/ask-yourself-dumb-questions-and-answer-them/ ; «There's more to mathematics than rigour and proofs» https://terrytao.wordpress.com/career-advice/theres-more-to-mathematics-than-rigour-and-proofs/
- T. Tao. «What is good mathematics?» arXiv:math/0702396.
- T. Gowers. Blog, категория «Demystifying proofs»: https://gowers.wordpress.com/category/demystifying-proofs/
- T. Gowers. «Mini-monomath» — запись собственного хода мысли при решении задачи IMO в реальном времени, со всеми тупиками: https://gowers.wordpress.com/2014/07/19/mini-monomath/
- T. Gowers. «How to work out proofs in Analysis I»: https://gowers.wordpress.com/2014/02/03/how-to-work-out-proofs-in-analysis-i/
- T. Gowers. «Brief review of polymath1»: https://gowers.wordpress.com/2009/02/23/brief-review-of-polymath1/ ; «Can Polymath be scaled up?»: https://gowers.wordpress.com/2009/03/24/can-polymath-be-scaled-up/
- T. Gowers. «How do IMO problems compare with research problems?» https://link.springer.com/chapter/10.1007/978-3-642-19533-4_5
- R. Vakil. «For potential Ph.D. students»: https://math.stanford.edu/~vakil/potentialstudents.html ; упражнение «three things»: https://math.stanford.edu/~vakil/threethings.html

**Программы**
- J. Gallian. «The Duluth Undergraduate Research Program 1977–2006». https://www.d.umn.edu/~jgallian/PURMweb/duluthreu.pdf
- J. Gallian. Описание программы: https://www.d.umn.edu/~jgallian/progdesc.html
- Duluth REU (актуальный сайт): https://sites.google.com/view/gallian-reu
- MIT PRIMES, Program Details: https://math.mit.edu/research/highschool/primes/program/
- MIT PRIMES, How to Apply: https://math.mit.edu/research/highschool/primes/usa/index.html
- Proceedings of the Conference on Summer Undergraduate Mathematics Research Programs (AMS) — сборник описаний REU-программ.

**Дидактика**
- H. Freudenthal. *Revisiting Mathematics Education: China Lectures*, 1991 — guided reinvention.
- Journal of Inquiry-Based Learning in Mathematics: http://www.jiblm.org
- Academy of Inquiry Based Learning: https://www.inquirybasedlearning.org
- Литература Moore method: F. B. Jones, «The Moore method», Amer. Math. Monthly 84 (1977).
- Borwein, Bailey, Girgensohn. *Experimentation in Mathematics: Computational Paths to Discovery*, 2004 — про экспериментальную математику как метод.
