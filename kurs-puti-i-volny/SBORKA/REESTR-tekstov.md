---
opisanie: что написано, в каком состоянии, чей вердикт; 26 долгов с адресами
sloj: 0
status: zhivoy
---

# Реестр написанного: что есть, в каком состоянии, чей вердикт

*Снято 18.09.2026 сплошным чтением 44 файлов. Объёмы — `wc -c` (байты; кириллица в UTF-8 — два байта на букву, знаков примерно вдвое меньше). Пути от `materials/`.*

> 🔴 **Поле `status:` во фронтматтере бесполезно как статус.** У принятого обзора, у забракованного обзора и у забракованного плана стоит одинаково — `chernovik`. Реальный статус живёт только в словесных пометках внутри текста и в `REESTR-reserchey.md`. Это дефект разметки, а не трудность чтения: **гейта, который судил бы статус, нет.**

---

## A. Готовое и принятое

Ровно один текст. Больше ничьей приёмки в корпусе не зафиксировано.

**`obzory/puti-ogranichennoy-vysoty/src/obzor.md`** — 47 803. Обзор второй-третьей четверти: пути Дика высоты ≤ $m$, цепная дробь, Бине, Чебышёв, спектральная формула, метод изображений, интеграл Каталана.
«Состояние: рабочий текст, **владельцем принят**» (`kurs-puti-i-volny/README.md:75`). Подтверждено независимо дважды: `plan/src/voprosy.md` — «наш собственный принятый текст»; `REESTR-reserchey.md` №20.
⚠ Внутри принятого текста собственный список несделанного (см. Д12).

**Отдельно: принятыми числятся решения, а не тексты.** `ZAMYSEL.md:60` центральный объект — «принято 2026-09-02 владельцем на интервью»; `:80` жанр — «принято 02.09, подтверждено 03.09»; `PERESTROYKA.md:99` — «владелец принял (В) с условием»; `LEKCIYA-v2/00-arhitektura.md:46` — восемь глав, решение 03.09.

---

## B. Написано, вердикта нет — около 350 000 знаков

**Прогулка, `obzory/funkciya-putey-i-ee-uravneniya/LEKCIYA-v2/` — 119 581 без архитектуры.** Все восемь глав дописаны, у каждой подвал «Черновик 2026-09-03» с честным перечнем проверенного и взятого чёрным ящиком.

| глава | знаков | о чём |
|---|---|---|
| `01-dve-drobi` | 15 221 | 1913, письмо Харди; две дроби рядом |
| `02-koridor` | 13 636 | объект и параметры; почему имена обрываются на четвёртой высоте |
| `03-zverinec` | 16 043 | 🆕 концы отпущены: биномы, Каталан, Фибоначчи; биекции |
| `04-tri-sposoba` | 16 499 | отражение, определитель, спектр — три формулы одного числа |
| `05-ploshchad` | 15 957 | включаем площадь; что ломается, что выживает |
| `06-bolshie-chisla` | 15 835 | 🆕 асимптотика, $n^{-3/2}$, перемешивание, тэта |
| `07-vozvrashchenie` | 12 759 | дробь коридора = дробь из письма; Роджерс, Шур |
| `08-za-dveryu` | 13 631 | граница объекта; что не выводится |

Плюс `00-arhitektura.md` — 18 134, служебная вкладка, читателю не показывается; композиционные решения в ней владельцем утверждены.

**Остальное без вердикта:**

- `SKELET.md` — 40 850. Строгий каркас: объект с пятью ручками, четыре теоремы, ~36 утверждений. `REESTR-reserchey.md` №29: «жив, **ждёт „да" владельца**».
- `SVEDENIE-kursa.md` — 11 774. 38 утверждений плана сведены к общим теоремам. Содержит незакрытую ошибку (Д1, Р4).
- `RAZVEDKA-2026-09-03.md` — 23 894. Три разведзахода: что оспорено литературой, что противоречит внутри арки, какая теорема центральная. Повод назван честно: «владелец не поверил, что этого достаточно. Он был прав: из семи утверждений, перепроверенных счётом, **три оказались ошибочны**».
- `reserch/R1–R4` — 109 487. R1: объекта у людей нет, ближайший сосед Owczarek — Prellberg. R2: образцы жанра. R3: 16 теорем-кандидатов на центральную. R4: честного перехода отрезок → окружность нет.
- `otchety/` — 152 856, восемь файлов (кроме забракованного, см. C5). Самый поздний и сжатый ответ на «про что курс» — `OPTIKA-odna-funkciya.md`.
- `OBRAZEC-summy-kvadratov.md` — 15 922, и его дубль `obrazec/src/obrazec.md` — 16 995. Три страницы от вопроса до формулы Якоби; образец арки для финала.
- `anons.md` — 4 576. Готовый внешний текст для постера; по `REESTR-reserchey.md` — «самая чистая **формулировка замысла** лежит тут».
- `RAZVEDKA-metody-i-obrazcy.md` — 39 965. ~17 источников фигуры «счёт → производящая функция → уравнение → асимптотика». «В первый текст не вошла никак».
- `CHITAT.md` — 11 089. Проверенный список чтения.
- Живые заходы `ZAHOD-okruzhnost.md`, `ZAHOD-formy-yakobi.md`, `ZAHOD-sverka-koncepcii.md` — 29 736. ⚠ Два последних помечены ядовитыми: стоят на отменённой рамке.

---

## C. Забраковано — около 230 000 знаков, с причиной дословно

**C1. `obzory/funkciya-putey-i-ee-uravneniya/src/obzor.md`** — 55 853.
Забракован владельцем целиком как изложение — «**я не понял, о чём он**», но объект в нём есть. Статус: «устарел как текст; склад формулировок» (`REESTR-reserchey.md` №22).

**C2. `obzory/kombinatorika-okruzhnosti/src/obzor.md`** — 45 816.
«⚠️ **Забракован по содержанию 05.08.** Первая половина держится, **вторая — набор результатов без вопроса**» (`README.md:76`). Механизм брака назван отдельно и стоит запоминания: «**У каждого раздела свой вопрос.** Механические гейты этого не судят. *(Цена: обзор на 33 врезки, прошедший оба гейта и забракованный целиком.)*»

**C3. `plan/src/plan.md`** — 35 658. Во фронтматтере прямо: `tab: План (забракован)`.
«⚠️ ЗАБРАКОВАН владельцем 06.08. Причина: у частей II и III нет своих содержательных вопросов, вместо вопроса стоит „сейчас введём язык"; занятия 12–13 — одно уравнение, переписанное переносом члена; разбиений нет в первой половине; полугодие кончается на 16, а не на 24».
⚠ Токсичный след: формулы с отменённым $m+1$ могли утечь из него в другие тексты.

**C4. `obzory/funkciya-putey-i-ee-uravneniya/LEKCIYA/`** — все пять файлов, 72 801.
«🔴🔴 **ЭТО МИШЕНЬ, А НЕ ТЕКСТ. ЧИТАТЬ КАК ГОТОВОЕ НЕЛЬЗЯ.** Черновик собран 03.09 за один ход, глядя ТОЛЬКО в `SKELET.md`… **Мишень оставлена намеренно:** по ней видно, какая композиция получается без материала». Частные приговоры внутри: «вкладка пробита в основании», «опровергнуто разведкой 03.09, весь блок читать нельзя». Брак по самооценке автора, не вердикт владельца.

**C5. `otchety/RASSKAZ-dva-sposoba.md`** — 18 411. «Устарел: написан по спине, от которой отказались; держать как заготовку, **не как план**».

**C6. `zahody/ZAHOD-okruzhnost-i-nepreryvnyj-predel.md`** — 959. Отменён: владелец в тот же день переопределил фокус.

**C7. Отменённые куски внутри живых файлов** (`ZAMYSEL.md` §5): окружность как несущая — отменено 02.09 на интервью; прежний throughline «потолок есть параметр финитизации» — забракован, «требовал знать теорему, которую ещё не рассказали»; вычитка 36 утверждений счётом — «названа лишней задачей»; ADE как финал — забракован.

---

## D. Долги — двадцать шесть, каждый с адресом

### Главный

**Д0.** Шаг 6(е) костяка: свести взвешенное равенство «обмотки = волны» в одну формулу. «Обе стороны построены и **численно совпадают, выкладки нет**. Без неё мост объявлен, но не построен» (`README.md:88`). Повторён в `KOSTYAK.md:211,233,298`, `ZAHOD-sverka-koncepcii.md:55`, `SVEDENIE-kursa.md:69`. Плюс `KOSTYAK.md:310`: «⚠️ Честно: точные константы я не свёл. Аккуратный пересчёт констант — часть долга 6(е)».

**Д0б.** Переписать обзор про окружность по костяку (`README.md:90`).

### Про завтрашнюю работу

**Д10.** `karkas.md:219` — «⚑ **задачи для листков не выписаны ни к одной лекции.** Часть материала по Каталану сознательно вытеснена в листки — **эти листки тоже не написаны**». В `plan.md:306` то же резче: «это следующая работа, и она главная — **план без задач не проверяется**».

**Д11.** `HREBET-kursa.md:308` — «**Тексты не написаны.** Есть только материал второй-третьей четверти, и он сам требует разборки. **Четвёртая четверть не написана. $q$-четверть не написана.**»

### Про сведение и скелет

**Д1.** `SVEDENIE-kursa.md` числит пятиугольную теорему сведённой полностью; её место — «частично», внешний механизм есть инволюция Франклина (`LEKCIYA-v2/00-arhitektura.md:93`).
**Д2.** `proverka_chisel.py` живёт в своей нормировке площади, не совпадающей с определением 2 скелета. «Ровно тот класс, который гейты не ловят: два документа согласованы каждый с собой и расходятся друг с другом» (`SKELET.md:306`). Чинить переводом на канон, **не подгонкой чисел**.
**Д3.** Форма показателей в `q-izobrazheniya` выписана схематически, без явных $\alpha_j,\beta_j$, «взята по памяти и с источником не сверялась» (`SKELET.md:289`).
**Д4.** Переход между двумя записями формулы Чебышёва нигде не выписан (`RAZVEDKA:74`).
**Д5.** arXiv:1004.1698 и arXiv:0907.3101 — «не читались, только аннотации»; Краттенталер §10.19 — «раздел не прочитан» (`RAZVEDKA:139,143`).
**Д6.** Либо доказательства невыводимости Эйлера пишутся, либо обещание снимается — снято 03.09, но `SVEDENIE` не поправлен (`PERESTROYKA:165`).

### Про покрытие

**Д7.** Покрытие курса прогулкой: диагноз 03.09 — «блок 3 покрыт одной темой, блок 7 не покрыт ни одной». Главы 3 и 6 написаны, **проверки покрытия после них в файлах нет**.
**Д8.** Клетка «отрезок × вес включён» пуста; вес выключается дважды (`PERESTROYKA:185,187`).
**Д9.** Разметка координат 32 тем «не сверялась с владельцем» (`PERESTROYKA:197`).

### Содержательные — не доказано, не выведено

**Д12.** В **принятом** обзоре собственный список: не выведена формула $P_m(z)=z^{m/2}U_m\!\left(\frac1{2\sqrt z}\right)$; связь веса $\sin^2\theta$ с усреднением по матрицам сформулирована, не доказана; двойственность проверена счётом, не выведена; про гипергеометрические функции нет ничего сверх названия; **иллюстраций нет**.
**Д13.** Функциональное уравнение: «выкладка приведена; аналитическое продолжение объявлено, не доказано».
**Д14.** `KOSTYAK.md:57` — «**Я не могу назвать конкретный вероятностный вопрос про $F_n$, ответ на который даёт теория модулярных форм и не дают первые три четверти.** Кандидаты есть, но ни один не проверен». Там же: квадратичный закон взаимности — «вход есть, вывод не сделан».
**Д15.** `OTCHET-okruzhnost.md:195` — «наблюдение на малых случаях, полного вывода нет. Это самое соблазнительное место отчёта и потому самое опасное; **в обзор без вывода не пойдёт**».
**Д16.** «Отрезок = свёрнутая окружность» проверено счётом, **не доказано**; суммирование Пуассона и тождество Якоби только названы.
**Д17.** Не проверено совпадение $F_m$ с моделями Эндрюса — Гордона; связь с бозонной стороной не выписана.
**Д18.** Асимптотика $N^*\asymp n^2$ — «не доказана, только наблюдение на семи значениях».
**Д19.** «Полюс в $s=1$ означает бесконечность простых» — названо, не доказано.
**Д20.** Объект с свободным правым концом и area-весом «не выписан никем из найденных» — то есть определять приходится самим.
**Д21.** Открытые места `ZAMYSEL.md`: где доказывается полностью, а где ссылкой; доказательство равенства подходящей дроби отношению многочленов Шура; **как пара «пути ↔ волны» подаётся школьникам, для которых спектр — новое слово**; второе полугодие описано только намерением.

### Инфраструктурные

**Д22.** `SKELET.md` — слой 2, основание курса — физически лежит внутри обзора. «Переезд ломает ссылки и делается отдельным заходом».
**Д23.** Слово «полоса» осталось ведущим в `SKELET.md` (8 вхождений); `ZAMYSEL.md` сам пишет и «полоса», и «коридор», и «отрезок». Ждёт решения владельца.
**Д24.** Картотека материалов ресёрча у этого курса **не заведена**.
**Д25.** Два захода в `zahody/` — задания исполнителям на отменённой рамке. «Запусти его как есть — исполнитель месяц проработает по мёртвой концепции».
**Д26.** Скрипты `proverki/` после 06.08 не трогались — счётное обеспечение отстаёт от текстов на полтора месяца.

---
*Открыто 44 файла, `wc -c` по 54. Статусы взяты из самих файлов и из `REESTR-reserchey.md`; ни один не выведен по догадке.*


---

## E. Catalogue: every course file with its status and a confirming address

*Added 2026-09-19 (task katalog-kursa) to finish this registry, not to start a second one. The number of files is a command, not a figure:*

```bash
python3 -c "import pathlib; print(len(list(pathlib.Path('kurs-puti-i-volny').rglob('*.md'))))"
```

*Coverage of the table below — prints «покрыто X из N»; X below N is red (a row counts only with a closed-list status and an address of the form `file:line`):*

```bash
python3 -c 'import pathlib,re;n={str(p) for p in pathlib.Path("kurs-puti-i-volny").rglob("*.md")};t=pathlib.Path("kurs-puti-i-volny/SBORKA/REESTR-tekstov.md").read_text(encoding="utf-8");r=set(re.findall(r"^\| \x60(kurs-puti-i-volny/[^\x60]+\.md)\x60 \| .+ \| (?:живой|устарел|отменён|порождаемый|архив) \| .*\S:\d+.*\|$",t,re.M));print("покрыто",len(r&n),"из",len(n))'
```

**Closed list of statuses:** `живой` · `устарел` · `отменён` · `порождаемый` (built by a tool, never edited by hand) · `архив`. No sixth category. **A status without an address is forbidden:** the address is `file:line` plus a quote of at most 12 words that shows the status. Where the address is the row's own file, the status is self-attested and there is no independent confirmation.

**Cancelled files say so about themselves.** A file that is cancelled as a whole carries the banner `🗄 АРХИВ — ГЕЙТ НЕ СУДИТ` in its first 10 lines plus one line naming what cancelled it; a live file with one cancelled section carries a line starting `🚫 ОТМЕНЕНО ЗАПИСЬЮ <entry id>` next to that section. Both must name the entry of `ZAMYSEL.md` §5 that cancelled it. The check — with its coverage and its blind zones printed — is `python3 ../disciplina/_generator/tools/check_arhiv.py kurs-puti-i-volny/ZAMYSEL.md` (run from `materials/`).

| path | what it is | status | confirming address |
|---|---|---|---|
| `kurs-puti-i-volny/ARHITEKTURA.md` | map of homes: where each kind of information lives and what feeds what | живой | `kurs-puti-i-volny/ZAMYSEL.md:14` «Сразу вторым — ARHITEKTURA.md: где какая информация лежит» |
| `kurs-puti-i-volny/CHITAT.md` | checked reading list and links for the course | живой | `kurs-puti-i-volny/ARHITEKTURA.md:89` «что почитать | CHITAT.md» |
| `kurs-puti-i-volny/HREBET-kursa.md` | 2026-08 research digest: the year by quarters, materials per board, ending in the duality of two formulas; the quarter framing is cancelled, the rest stands | живой | `kurs-puti-i-volny/ARHITEKTURA.md:98` «Богатые и местами единственные носители материала» |
| `kurs-puti-i-volny/INDEKS.md` | generated index of the corpus built from the file headers | порождаемый | `kurs-puti-i-volny/INDEKS.md:1` «СОБРАН ГЕНЕРАТОРОМ tools/indeks.py. РУКАМИ НЕ ПРАВИТЬ» |
| `kurs-puti-i-volny/KOSTYAK.md` | mathematical skeleton «one problem counted twice» of the pre-rebuild course | устарел | `kurs-puti-i-volny/KOSTYAK.md:2` «математический скелет с излагаемыми теоремами (УСТАРЕЛ)» |
| `kurs-puti-i-volny/OBEKT.md` | the whole course on two pages: the object, its degenerations, four views, two directions of the story | живой | `kurs-puti-i-volny/ARHITEKTURA.md:78` «что такое объект и во что он вырождается | OBEKT.md» |
| `kurs-puti-i-volny/OBOZNACHENIYA.md` | single home of notation: one letter, one meaning | живой | `kurs-puti-i-volny/ARHITEKTURA.md:82` «буква | OBOZNACHENIYA.md» |
| `kurs-puti-i-volny/OBRAZEC-summy-kvadratov.md` | pointer stub to the sum-of-four-squares sample kept in obrazec/src/obrazec.md | живой | `kurs-puti-i-volny/OBRAZEC-summy-kvadratov.md:7` «Указатель — см. obrazec/src/obrazec.md» |
| `kurs-puti-i-volny/PAZL.md` | grid «specialization × view»: what is known, where the holes are, in which order to dig | живой | `kurs-puti-i-volny/ARHITEKTURA.md:79` «PAZL.md, сетка «специализация × взгляд»» |
| `kurs-puti-i-volny/PERESTROYKA.md` | record of the restructuring: goal, fork, plan (2026-09-03) | живой | `kurs-puti-i-volny/ZAMYSEL.md:207` «Разбор и предложение из семи глав — PERESTROYKA.md §5б–5в» |
| `kurs-puti-i-volny/PLAN-goda-krupno.md` | year at a glance: one object, two generalization axes, seven blocks (draft of 2026-09-19) | живой | `kurs-puti-i-volny/PLAN-goda-krupno.md:14` «Собран 2026-09-19 по решениям владельца» |
| `kurs-puti-i-volny/RASSKAZ-god.md` | year story in eight chapters about one path function, in a single readable file | живой | `kurs-puti-i-volny/RASSKAZ-god.md:2` «годовая история курса «Пути и волны» одним читаемым файлом» |
| `kurs-puti-i-volny/RAZVEDKA-metody-i-obrazcy.md` | map of about 17 sources of the figure «count → generating function → equation → asymptotics» | живой | `kurs-puti-i-volny/SBORKA/REESTR-tekstov.md:53` «В первый текст не вошла никак» |
| `kurs-puti-i-volny/README.md` | course entry page as of 2026-08-05: goal, state, debts | устарел | `kurs-puti-i-volny/ARHITEKTURA.md:100` «заморожен на 05.08, описывает курс до перестройки» |
| `kurs-puti-i-volny/REESTR-reserchey.md` | numbered register of research moves with verdicts | живой | `kurs-puti-i-volny/ARHITEKTURA.md:88` «что уже делалось и зачем | REESTR-reserchey.md» |
| `kurs-puti-i-volny/SBORKA/KALENDAR-i-sostav.md` | real class calendar against the 32-topic composition, counted by command | живой | `kurs-puti-i-volny/ARHITEKTURA.md:101` «счётные своды от 18.09 (расхождения, реестр текстов, календарь)» |
| `kurs-puti-i-volny/SBORKA/KARTA-rashozhdeniy.md` | map of the places where course documents contradict each other | живой | `kurs-puti-i-volny/ARHITEKTURA.md:235` «Расхождения — SBORKA/KARTA-rashozhdeniy.md» |
| `kurs-puti-i-volny/SBORKA/REESTR-tekstov.md` | this registry: what is written, in what state, whose verdict; debts; the catalogue of all files | живой | `kurs-puti-i-volny/ARHITEKTURA.md:101` «счётные своды от 18.09 (расхождения, реестр текстов, календарь)» |
| `kurs-puti-i-volny/SBORKA/RESHENIE-instrumenty.md` | decision not to install IWE and what is built instead (2026-09-18) | живой | `kurs-puti-i-volny/ARHITEKTURA.md:101` «счётные своды от 18.09 (расхождения, реестр текстов, календарь)» |
| `kurs-puti-i-volny/SBORKA/SLEDUYUSHCHIY-ZAHOD.md` | program and calendar for the next executor's work on the corpus | живой | `kurs-puti-i-volny/SBORKA/SLEDUYUSHCHIY-ZAHOD.md:23` «Course Shape (Owner Decision 2026-09-19)» |
| `kurs-puti-i-volny/SBORKA/ZAMER-grafa.md` | measurement of the corpus link graph, written by tools/graf.py | порождаемый | `kurs-puti-i-volny/tools/graf.py:7` «Writes ZAMER-grafa.md and graf-rebra.tsv to the SBORKA folder» |
| `kurs-puti-i-volny/SLOVAR.md` | single home of words: which word names which concept | живой | `kurs-puti-i-volny/ZAMYSEL.md:48` «OBOZNACHENIYA.md · SLOVAR.md» |
| `kurs-puti-i-volny/ZAMYSEL.md` | decision home: what the course tells and why; cancelled decisions with their traces | живой | `kurs-puti-i-volny/ZAMYSEL.md:8` «Единственный дом решений о том, ЧТО мы рассказываем и ЗАЧЕМ» |
| `kurs-puti-i-volny/anons.md` | ready announcement text for a poster or an external audience | живой | `kurs-puti-i-volny/ARHITEKTURA.md:90` «формулировка замысла для внешнего читателя | anons.md» |
| `kurs-puti-i-volny/obrazec/src/obrazec.md` | source of the sum-of-four-squares sample text, embedded into the output HTML | живой | `kurs-puti-i-volny/SBORKA/REESTR-tekstov.md:51` «образец арки для финала» |
| `kurs-puti-i-volny/otchety/GRANICA-chto-vidno-na-okruzhnosti.md` | report: what modular-form theory shows on the one-dimensional circle | живой | `kurs-puti-i-volny/SBORKA/REESTR-tekstov.md:50` «восемь файлов (кроме забракованного» |
| `kurs-puti-i-volny/otchety/KARTA-mosta.md` | report: what modular forms really give the walk problem, and where it is a stretch | живой | `kurs-puti-i-volny/SBORKA/REESTR-tekstov.md:50` «восемь файлов (кроме забракованного» |
| `kurs-puti-i-volny/otchety/OPTIKA-odna-funkciya.md` | report: the whole course as a study of one continued fraction (2026-08-06) | живой | `kurs-puti-i-volny/SBORKA/REESTR-tekstov.md:50` «Самый поздний и сжатый ответ на «про что курс»» |
| `kurs-puti-i-volny/otchety/OTCHET-okruzhnost.md` | report answering the brief «is it simpler on the circle», with checked / from memory / unchecked marks | живой | `kurs-puti-i-volny/SBORKA/REESTR-tekstov.md:50` «восемь файлов (кроме забракованного» |
| `kurs-puti-i-volny/otchety/RASSKAZ-dva-sposoba.md` | story «two ways to count the same thing» ending at the zeta functional equation | устарел | `kurs-puti-i-volny/otchety/RASSKAZ-dva-sposoba.md:2` «рассказ двумя способами (УСТАРЕЛ)» |
| `kurs-puti-i-volny/otchety/RAZBOR-i-perestroyka.md` | analysis of the rejected circle survey and where the entrance to modularity was found | живой | `kurs-puti-i-volny/SBORKA/REESTR-tekstov.md:50` «восемь файлов (кроме забракованного» |
| `kurs-puti-i-volny/otchety/ZAMETKI.md` | provenance notes, open places and plans for the accepted survey | живой | `kurs-puti-i-volny/SBORKA/REESTR-tekstov.md:50` «восемь файлов (кроме забракованного» |
| `kurs-puti-i-volny/otchety/ZAPISKA-iz-simmetrii.md` | note on counting on the circle from symmetry, with a verdict on sources | живой | `kurs-puti-i-volny/SBORKA/REESTR-tekstov.md:50` «восемь файлов (кроме забракованного» |
| `kurs-puti-i-volny/plan/src/chast-1-do-analiza.md` | generated view: the «before analysis» part of the year | порождаемый | `kurs-puti-i-volny/plan/src/chast-1-do-analiza.md:5` «СОБРАН ГЕНЕРАТОРОМ tools/plany.py ИЗ punkty.md. РУКАМИ НЕ ПРАВИТЬ» |
| `kurs-puti-i-volny/plan/src/chetvert-1.md` | generated view: quarter 1 | порождаемый | `kurs-puti-i-volny/plan/src/chetvert-1.md:5` «СОБРАН ГЕНЕРАТОРОМ tools/plany.py ИЗ punkty.md. РУКАМИ НЕ ПРАВИТЬ» |
| `kurs-puti-i-volny/plan/src/chetvert-2.md` | generated view: quarter 2 (still «not yet written») | порождаемый | `kurs-puti-i-volny/plan/src/chetvert-2.md:5` «СОБРАН ГЕНЕРАТОРОМ tools/plany.py ИЗ punkty.md. РУКАМИ НЕ ПРАВИТЬ» |
| `kurs-puti-i-volny/plan/src/chetvert-3.md` | generated view: quarter 3 (still «not yet written») | порождаемый | `kurs-puti-i-volny/plan/src/chetvert-3.md:5` «СОБРАН ГЕНЕРАТОРОМ tools/plany.py ИЗ punkty.md. РУКАМИ НЕ ПРАВИТЬ» |
| `kurs-puti-i-volny/plan/src/chetvert-4.md` | generated view: quarter 4 (still «not yet written») | порождаемый | `kurs-puti-i-volny/plan/src/chetvert-4.md:5` «СОБРАН ГЕНЕРАТОРОМ tools/plany.py ИЗ punkty.md. РУКАМИ НЕ ПРАВИТЬ» |
| `kurs-puti-i-volny/plan/src/god.md` | generated view: the year, one line per point | порождаемый | `kurs-puti-i-volny/plan/src/god.md:5` «СОБРАН ГЕНЕРАТОРОМ tools/plany.py ИЗ punkty.md. РУКАМИ НЕ ПРАВИТЬ» |
| `kurs-puti-i-volny/plan/src/karkas.md` | 32-topic skeleton, third edition; now the raw source that punkty.md cites | живой | `kurs-puti-i-volny/plan/src/karkas.md:14` «Этот файл остаётся источником ПЕРЕВОДА» |
| `kurs-puti-i-volny/plan/src/lekciya-1.md` | generated view: lecture 1 expanded from its storyboard | порождаемый | `kurs-puti-i-volny/plan/src/lekciya-1.md:5` «СОБРАН ГЕНЕРАТОРОМ tools/plany.py ИЗ punkty.md. РУКАМИ НЕ ПРАВИТЬ» |
| `kurs-puti-i-volny/plan/src/plan.md` | rejected schedule of 32 sessions, kept as a historical draft | отменён | `kurs-puti-i-volny/plan/src/plan.md:19` «ЗАБРАКОВАН владельцем 06.08» |
| `kurs-puti-i-volny/plan/src/punkty.md` | single home of the list of course points; source of the generated plan views | живой | `kurs-puti-i-volny/plan/src/punkty.md:7` «Пункты курса «Пути и волны» — единый дом» |
| `kurs-puti-i-volny/plan/src/voprosy.md` | list of the questions the year is assembled from, in groups | живой | `kurs-puti-i-volny/ARHITEKTURA.md:85` «открытый вопрос года | plan/src/voprosy.md» |
| `kurs-puti-i-volny/zahody/ZAHOD-formy-yakobi.md` | executor brief: is F(z,q) a Jacobi form; stands on the cancelled circle frame | отменён | `kurs-puti-i-volny/ZAMYSEL.md:302` «задания исполнителям, стоящие на отменённой рамке» |
| `kurs-puti-i-volny/zahody/ZAHOD-okruzhnost-i-nepreryvnyj-predel.md` | first version of the circle brief, cancelled the same day | отменён | `kurs-puti-i-volny/zahody/ZAHOD-okruzhnost-i-nepreryvnyj-predel.md:8` «ОТМЕНЁН — см. ZAHOD-okruzhnost.md» |
| `kurs-puti-i-volny/zahody/ZAHOD-okruzhnost.md` | brief that started the circle line: is it simpler on the circle | живой | `kurs-puti-i-volny/SBORKA/REESTR-tekstov.md:55` «Живые заходы ZAHOD-okruzhnost.md» |
| `kurs-puti-i-volny/zahody/ZAHOD-sverka-koncepcii.md` | executor brief: reconcile the concept, then modularity; stands on the cancelled circle frame | отменён | `kurs-puti-i-volny/ZAMYSEL.md:302` «задания исполнителям, стоящие на отменённой рамке» |
