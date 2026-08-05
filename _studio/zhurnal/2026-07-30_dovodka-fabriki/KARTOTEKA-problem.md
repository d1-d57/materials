---
tab: Картотека проблем фабрики
status: sobrana
poryadok: 1
---

# КАРТОТЕКА-problem.md — единая картотека проблем фабрики

> **Как пересчитать числа этой шапки (KONSTITUCIYA §10 — числа командой, не руками):**
> ```
> cd _studio/zhurnal/2026-07-30_dovodka-fabriki && python3 srez_po_faze.py   # Σ по строкам, ИТОГО = 2264 (см. оговорку ниже)
> grep -c '^| КРТ-\|^| КРВ-\|^| И-\|^| ГИТ-' KARTOTEKA-problem.md            # 596 групп с id-префиксом (Разделы 1-4)
> ```
> 🔴 **Обновлено этим заходом (2026-08-05, `kod_razbros-po-fazam.md`).** Прежняя редакция шапки считала
> только 295 ГРУПП (153+56+74+12) без колонки фазы и без Раздела 5. Теперь у каждой группы всех 5
> разделов (191 Раздел 1 + 319 Раздел 2 + 74 Раздел 3 + 12 Раздел 4 + 193 Раздел 5 = 789 строк-групп;
> Раздел 5 без id-префикса `КРТ-`/`КРВ-`, поэтому не в 596 выше — считается вместе с остальными только
> скриптом) заполнена колонка `фаза`. 🔴 **`srez_po_faze.py` даёт ИТОГО = 2264, а не 2263** (найдено
> независимым верификатором) — Раздел 3 считает 74 СТРОКИ-цитаты класса И, а не 73 уникальные секции
> урока, которые эти 74 цитаты физически покрывают (одна секция несёт два подкласса И). **Верное число
> покрытых ИСХОДНЫХ ЗАПИСЕЙ 4 живых корпусов — 2263**, подробный разбор обоих чисел — в
> `## Гейт-против-охвата`.

## Зачем этот файл и откуда данные

В репозитории накоплено **2263 живые записи** о проблемах фабрики (дата данных 2026-08-05, все 4
числа подтверждены независимым верификатором прямым пересчётом сырых файлов: 316 уроков арок · 461
кандидат исполнителей · 1379 реплик владельца · 107 строк автолога git — сумма ровно 2263, совпадает
с `DOK.md`). Разбросаны по пяти форматам, посчитать «сколько живо» и «какой фазе конвейера
принадлежит» было нельзя. Этот файл — один дом для всех четырёх корпусов на уровне групп кратности
(Раздел 1–2, унаследовано от прошлого захода) плюс два дополнительных корпуса (класс И уроков арок —
Раздел 3, автолог git — Раздел 4, унаследовано) плюс **новый Раздел 5** (этот заход): 243 урока арок,
которые не входили никуда — ни в кратность (тот корпус не про уроки арок), ни в класс И (закреплён
за 74 намеренно). **Главное новое в этом заходе — колонка `фаза` конвейера у каждой группы всех 5
разделов** (часть A0/B/C захода `kod_razbros-po-fazam.md`), плюс полный охват (было 74 из 316 уроков
арок, стало 316 из 316).

### Метод (прочти, прежде чем читать таблицы)

1. **Единица записи — ГРУППА, а не отдельное вхождение.** `KRATNOST.md`/`KRATNOST-vladelca.md` уже
   свернули 461+1379=1840 сырых записей в 153+56=209 групп по механизму/предмету; картотека наследует
   эту свёртку, а не разворачивает её обратно — иначе строк было бы тысячи, и работать с ними опять
   стало бы нельзя (та же болезнь, ради лечения которой заведена фаза).
2. **Id устойчив, не позиционен.** `КРТ-NNN` = номер группы в живом `KRATNOST.md` (файл её присвоил,
   не эта картотека); `КРВ-NN` = номер строки сводной таблицы `KRATNOST-vladelca.md`; `И-NN` = сквозной
   номер по девяти подклассам `POKRYTIE.md` в порядке самого файла; `ГИТ-<буква>` = буква класса
   `RAZBOR-povtorov.md §2` (буквы файла-источника, максимально стабильный id из всех четырёх).
3. **🔴 Класс И закреплён ИСКЛЮЧИТЕЛЬНО за 74 записями Раздела 3.** Это решение метода, а не
   недосмотр: `KRATNOST-vladelca.md` (Раздел 2) содержит МНОГО групп, топически совпадающих с
   подклассами И (тайминг, компоновка, вопрос-в-зал и т.д.) — но это ДРУГОЙ корпус (сырые реплики
   владельца, не синтезированные уроки арок), посчитанный ДРУГИМ методом. Слить их значило бы задвоить
   счёт одного и того же явления под двумя разными механизмами свёртки. Критерий готовности №2 требует
   `grep -c` класса И в картотеке == строкам класса И в `POKRYTIE.md` — при таком решении метода
   это тождество проверяется буквально, а не подгоняется постфактум. Раздел 2 несёт отдельную колонку
   «пересечение» — честную перекрёстную ссылку без переноса содержания.
4. **Класс назначается по МЕХАНИЗМУ ПОЧИНКИ, не по теме** (`POKRYTIE.md`, метод которому велено
   следовать): И — лечится интервью с владельцем (только Раздел 3) · Т — технический баг инструмента ·
   П — процесс и git · Д — дисциплина документа.
5. **Статус/рычаг — честный дефолт «жив, не оценён», если не найдено доказательство обратного.**
   Раздел 1 несёт явные статусы/рычаги там, где они прослежены до `RAZBOR-povtorov.md` или до строки
   уже существующего шаблона захода (§0/§1/§4 самого этого файла-захода); Раздел 2 (владелец) и
   бо́льшая часть длинного хвоста Раздела 1 (группы 47–152, кратность 1 каждая) статуса не имеют —
   называть его без проверки значило бы придумывать (запрещено законом `GEJTY.md`).


## ЧАСТЬ A0 (этот заход) · Критерии принадлежности фазе конвейера

> Выписано ДО разноса по `_studio/konvejer/00-KONVEJER.md` + 11×`DOK.md`, как требует заход
> `kod_razbros-po-fazam.md`. Разнос (колонка `фаза` ниже) идёт по этим критериям, не по интуиции.
> Буквы `Часть Б`/`Часть C` ниже по файлу — секции ПРЕДЫДУЩЕГО захода (`kartoteka-intervyu`), про
> перевод рычагов класса И; не путать с `ЧАСТЬ B`/`ЧАСТЬ C` ЭТОГО захода (колонка ФАЗА и пересуд
> класса И по всем группам) — они помечены явно «(этот заход)».

| фаза | что происходит (1 фраза) | вход → выход | признак «инцидент — сюда» | признак «похоже, но НЕ сюда» (граница с соседом) |
|---|---|---|---|---|
| `01-brief` | Снять 8 полей брифа (тема·аудитория·бюджет слайдов·throughline-кандидат·что резать·референс·строгость·формат события) до всякого ресёрча | запрос владельца → бриф 8 полей | throughline-кандидат не назван одной фразой / бюджет слайдов не посчитан арифметически из длительности / строгость или регистр-сигнал не зафиксированы явно / формат микро-интервью нарушен (открытый диалог вместо дефолт+подтверждение) | throughline НЕ ПОДТВЕРДИЛСЯ фактурой — это `02-reserch` (арка 1 даёт только кандидата); число слайдов ПОСЛЕ раскадровки — это `05-raskadrovka` |
| `02-reserch` | Собрать карточный граф (котлы математика‖научпоп) широко, без навязанной линии | бриф → карточки+KARTA-OBLASTI+нити, `TERMINY.md` | находка без карточки / источник не назван / <5 источников / котлы схлопнуты в один / ранний нарратив/throughline-скелет протащен в ресёрч (запрещено редизайном) / нет разворота «но» | строгость/полнота ДОКАЗАТЕЛЬСТВА — это `03-matbaza`; вытягивание НИТИ в сюжет — это `04-gibrid-istochnik` (4a) |
| `03-matbaza` | Вырастить карточки котла математика в строгий слой `skelet` (Определение/Утверждение/Доказательство) | карточки котла математика → `skelet`, 0 открытых `⚑ Флаг` | доказательство неверно / пропущен логический шаг / нотация не единообразна по потоку / термин не сверен с `TERMINY.md` / факт заявлен сильнее, чем доказан / `⚑ Флаг` не закрыт до гейта 3→4 | подача/объяснение уже ВЕРНОЙ математики для читателя — `04-gibrid-istochnik`/`06-tekst`; иллюстрация к доказательству — `09-illustracii` (здесь только пометка `🖼`) |
| `04-gibrid-istochnik` | Вытащить нить (4a) и сшить `rasskaz`‖`skelet` цитатой-сноской (4b) в закрытый источник | граф+`skelet` → источник (`rasskaz`‖`skelet`, `🖼`-описания) | throughline не держит/рвётся на фактуре / нарратив начат ДО закрытия гейта математики («платоновы тела») / ядро вывода урезано ради нарратива / `🖼`-описание отсутствует или не по тактам / спутаны два разреза (котлы арки 2 vs `rasskaz`/`skelet`) | сам РАЗГОВОР с владельцем о жанре/форме артефакта — `04.5-intervyu`; разрез источника на слайды — `05-raskadrovka` |
| `04.5-intervyu` | Интервью с владельцем → утверждённый контракт артефакта (рамка, законы формы, единицы выхода, открытые пункты) | закрытый источник+бриф+эталон → `KONTRAKT-*.md` | инцидент про МЕХАНИКУ САМОГО РАЗГОВОРА: вопрос не да/нет · цена варианта не названа · >4 вопросов разом · названия единиц выхода не показаны в чате · число выдумано и получило согласие · ресёрч принят за готовность · рамка сужена аналитиком · гипотеза владельца не проверена · шапка документа врёт телу · решение пересказано, а не процитировано · рамка/габарит/жанр/зал не установлены ДО начала фазы | если то же топически (габарит/плотность/раскладка), но лечится ФАКТОМ на диске, проверяемым гейтом ДРУГОГО шага (а не суждением интервьюера в моменте разговора) — рычаг там, не здесь (см. `Часть C` предыдущего захода: 62 из 74 «не переводятся» ровно по этой причине) |
| `05-raskadrovka` | Разрезать закрытый источник на слайды: archetype+дистилляция смысла+сцены+описание илл. на каждый | источник+бриф(+контракт) → HTML-демо + `src/` (`slides/*.html` каркасы, `brief.md` `slide_order`+регистр+бюджет) | архетип не выбран/неверен · дистилляция смысла подменена финальным текстом (роль арки 6) · единица вместимости спутана (сцена вместо экрана) · доминирующий архетип не распознан рано · регистр+бюджет не переданы в `brief.md` как поле · список слайдов не предъявлен владельцу и не принят им · throughline не режется на слайды чисто | финальные СЛОВА текста — `06-tekst`; раскладка ВЁРСТКИ (CSS/грид) реализующая архетип — `07-verstka` (арка 5 выбирает архетип, не меняет его 7-я) |
| `06-tekst` | Написать плакатный текст слайда в финальном объёме и стиле + выбрать раскладку (боковая пометка) | archetype+дистилляция+сцены+илл.описание+регистр/бюджет(унаследовано) → `teksty/*.md`+`view.html` | плотность/бюджет слов текста · маркированный список vs абзацы (главный регистр) · заголовок слайда отсутствует/неверной формы · слайд повторяет предыдущий · формулировка обрывочна там, где обязана быть полной (статус куска) · голос/стиль вне корпуса · опорная точка («Задача»/«Определение») не размечена · раскладка (текст+илл-справа vs илл-снизу) не проставлена | сама CSS-реализация выбранной раскладки (grid, overflow, паддинг) — `07-verstka`; решение АРХЕТИПА — `05-raskadrovka` |
| `07-verstka` | Разложить текст+иллюстрацию в грид канона (archetype→CSS) | текст арки 6 дословно+описание илл.+`tokens.css` → `slides/<id>.html`+per-slide CSS | overflow `.zone` / `--t-body` уменьшен / палитра не из `:root` / служебные слайды (обложка/визитка/финал) свёрстаны руками (запрещено) / номер слайда нечитаем / состояние доводки адресовано позицией `sNN`, а не устойчивым именем / раскладка внутри архетипа не варьируется (Р24 — арка 7 варьирует раскладку, не архетип) | смена АРХЕТИПА — вне мандата арки 7 (это `05-raskadrovka`); текст слов — `06-tekst`; что и когда раскрывается кликом — `08-sceny` |
| `08-sceny` | Разметить поклик-раскрытие поверх ЗАМОРОЖЕННОЙ геометрии (`{@N}`/`{fill}`/`{blur}`) | свёрстанный слайд+шорткаты в `content/*.md` → `data-scene-from/until` | сцена по ошибке считается экономией МЕСТА (запрещено — зона обязана вмещать весь текст разом) / накопление vs замена перепутаны (дефолт — накопление) / ссылка на текст, ушедший на прошлой сцене / ответ виден сразу, не заблюрен / тег сцены над списком `- ` не работает (известный блокер) / дед-клик | геометрия/CSS-раскладка сама — `07-verstka`; какой ТЕКСТ показывать — `06-tekst` |
| `09-illustracii` | Материализовать иллюстрацию (SVG/canvas/3D/растр) по плейсхолдеру+ТЗ | плейсхолдер+число сцен(8)+проза `🖼`(4/5) → живой SVG/HTML/3D-глава | ТЗ иллюстрации неполно (5 полей: изображено·подписи·действие·чего НЕ рисовать·размер) / картинка нечитаема за 3 секунды / пример не общего положения (лишняя симметрия) / коммутативный квадрат написан текстом, а не нарисован / персоналия — эпитет вместо портрета / иллюстрация не используется (сирота) / `var(--x)` не определён → чёрная заливка / SVGO id-конфликт | нужна ли иллюстрация ВООБЩЕ по смыслу текста — решение `05-raskadrovka`/`06-tekst`; КОГДА картинка раскрывается по сцене — `08-sceny` |
| `10-sborka-qa` | Секвенировать готовые инструменты (`build_deck.py`/`render.py`/`audit.py`) в один PASS/FAIL прогон | заполненный `src/` целиком → `dist/index.html`+отчёт | гейт слоями даёт неверный сигнал ИМЕННО НА СБОРКЕ / render-identity не ловит смену группировки смысла / сцены надо проверять попиксельно, не по тегам в md / сообщение гейта называет нерабочую в этом состоянии команду / новый гейт не прогнан сперва на живом эталоне | авторство контента (математика/текст/иллюстрация) — предыдущие арки; сама механика раскладки/сцен — авторится в `07`/`08`, здесь только проверяется |
| `вне-фаз` | — | — | git/коммиты/регистрация/индекс · харнесс субагентов/токены-cost недоступны · общие regex/парсер-баги инструмента, не специфичные для шага дека · дисциплина документа общего назначения (не текста слайда) | если баг воспроизводится ИМЕННО на артефакте дека определённого шага — фаза этого шага, не `вне-фаз` |

**Как читать таблицу при спорной записи:** сначала проверить «признак — сюда» для кандидата-фазы;
если он тоже подходит под «похоже, но НЕ сюда» соседней фазы — граница обычно в том, что именно
МЕНЯЕТ инцидент (суждение в разговоре vs факт на диске; выбор структуры vs её CSS-реализация; текст
vs картинка). Не решается за 30 секунд — в `## ВОПРОСЫ`, не гадать.

## Раздел 1 · корпус «кандидаты исполнителей» — группы механизмов (`KRATNOST.md`)

> Источник: `KRATNOST.md`, группировка по МЕХАНИЗМУ поломки, корпус 461 записей (`I0001`…`I0461`, `skelet-ispolnitelej.tsv`). **Разнесено субагентами по фазе A0 этого захода (2026-08-05); группы, разнородные по фазам, разрезаны на подгруппы `a/b/c…` — часть B, обновление владельца.** `КРТ-РАЗН` — 131 несведённая находка `KRATNOST.md#Разное`, здесь разложена по фазам десятью подгруппами (не 131 отдельной строкой — механизм каждой уникален, но фаза внутри подгруппы общая). Адреса сокращены: базовая папка `_studio/zhurnal/<арка>/`, если явно не указан другой корень (`catalan/`, `buffon/`, `kurs leto 2026/`).

| id | фаза | кратность | адреса (файл:строки, сокращены — базовая папка `_studio/zhurnal/<арка>/`, если не указано иное) |
|---|---|---|---|
| КРТ-001a | `вне-фаз` | 6 | kod_katalog.md#ОТЧЁТ:99-101; kod_spina.md#ВОПРОСЫ:96; kod_poisk-primerov.md#УРОКИ ФАБРИКЕ:83-85; UROKI-FABRIKE.md(teorkat-l1)#77-82; kod_konsolidacia-l1.md#УРОКИ ФАБРИКЕ:204-206; kod_commit-ux.md#ЗАДАНИЕ:71-73 |
| КРТ-001b | `02-reserch` | 5 | kod_vneshnyaya-merka.md#ОТЧЁТ:257; UROKI-FABRIKE.md(teorkat-l1)#57-60; kod_svedenie-i-gejty.md#УРОКИ ФАБРИКЕ:175-177; kod_biblioteka-dobor.md#ОТЧЁТ:114-115; kod_generator.md#ВОПРОСЫ:109 |
| КРТ-001c | `03-matbaza` | 3 | kod_chitaemost.md#ВОПРОСЫ:251-260; kod_mat-kostyak.md#ЗАДАНИЕ:93-99; UROKI-FABRIKE.md(mat-kostyak)#101-104 |
| КРТ-001d | `05-raskadrovka` | 2 | kod_treker.md#ВОПРОСЫ:109; UROKI-FABRIKE.md(paskal-lekcia-sborka)#72-76 |
| КРТ-001e | `01-brief` | 1 | kod_treker.md#ПЛАН:79 |
| КРТ-001f | `04-gibrid-istochnik` | 1 | kod_sborka-L2.md#ВОПРОСЫ:105 |
| КРТ-001g | `06-tekst` | 1 | kod_lekcia1-modeli.md#ОТЧЁТ:211 |
| КРТ-001h | `07-verstka` | 1 | kod_infra.md#ПЛАН:62-73 |
| КРТ-001i | `08-sceny` | 1 | kod_lekcia1-modeli.md#ОТЧЁТ:217 |
| КРТ-001j | `09-illustracii` | 1 | kod_lekcia1-modeli.md#ОТЧЁТ:213 |
| КРТ-002 | `вне-фаз` | 17 | kod_biblioteka-dobor.md#123-124; kod_dobor-skelet.md#82; kod_krever-extract.md#168-169; kod_skelet-mir2.md#105; kod_statya-mir2.md#149; kod_vychitano-backfill.md#67-68; kod_biblioteka-mir1.md#100-101; kod_html-obshchiy.md#164; kod_skelet-mir1.md#95; kod_port-oformlenia-v-build-doc.md#193-194; kod_svap-tz-v2.md#137; kod_dobor-L2.md#114; kod_html-L2.md#189; kod_ideal-L2.md#121; kod_sborka-L2.md#159; kod_generator-visual.md#90; kod_generator.md#154 |
| КРТ-003a | `вне-фаз` | 8 | kod_chitaemost.md#ЗАДАНИЕ:119; kod_chitaemost.md#ОТЧЁТ:497-513; kod_dvizhok-format.md#ЗАДАНИЕ:33; kod_dvizhok-format.md#ЗАДАНИЕ:34; kod_kostyak-rez.md#ЗАДАНИЕ:70; kod_mat-kostyak.md#УРОКИ ФАБРИКЕ:150-154; UROKI-FABRIKE.md(mat-kostyak)#133-136; UROKI-FABRIKE.md(mat-kostyak)#159-163 |
| КРТ-003b | `04-gibrid-istochnik` | 2 | kod_gejty-kursa.md#ЗАДАНИЕ:6-10,85; kod_shov-l4-l5.md#УРОКИ ФАБРИКЕ:189-191 |
| КРТ-003c | `03-matbaza` | 2 | kod_gejty-kursa.md#ЗАДАНИЕ:83; kod_shov-l4-l5.md#ЗАДАНИЕ:77 |
| КРТ-003d | `10-sborka-qa` | 2 | kod_sluzhebnye-slajdy.md#ОТЧЁТ:268; kod_sluzhebnye-slajdy.md#ОТЧЁТ:270 |
| КРТ-003e | `02-reserch` | 1 | kod_gejty-kursa.md#ЗАДАНИЕ:84 |
| КРТ-004a | `вне-фаз` | 13 | kod_lekcia1-pereverstka.md#ВОПРОСЫ:127; kod_reserch-geometria.md#ВОПРОСЫ:83; kod_biblioteka-vneshnyaya.md#ЗАДАНИЕ:3-5; kod_gejty-kursa.md#УРОКИ ФАБРИКЕ:156-158; kod_khl-kontent.md#УРОКИ ФАБРИКЕ:129-131; kod_resheniya.md#ЗАДАНИЕ:17; kod_dek-paskal-v2.md#ЗАДАНИЕ:232; kod_dek-paskal.md#ЗАДАНИЕ:201; kod_gejty-shaga-6.md#ЗАДАНИЕ:92; kod_sluzhebnye-slajdy.md#ЗАДАНИЕ:101; kod_skelet-konspekt-l1.md#ЗАДАНИЕ:57; kod_commit-ux.md#ЗАДАНИЕ:41; kod_tool-contract.md#ЗАДАНИЕ:81 |
| КРТ-004b | `03-matbaza` | 1 | kod_vneshnyaya-merka.md#ВОПРОСЫ:162-166 |
| КРТ-005 | `вне-фаз` | 12 | kod_biblioteka-vhodyashchee.md#ЗАДАНИЕ:7; kod_zamykanie.md#УРОКИ ФАБРИКЕ:160-164; kod_razbor-kartoteki.md#ЗАДАНИЕ:94-96; kod_resheniya.md#ЗАДАНИЕ:155-157; kod_dek-paskal-v2.md#ЗАДАНИЕ:224; kod_dek-paskal.md#ЗАДАНИЕ:26; kod_gejty-shaga-6.md#ЗАДАНИЕ:21; kod_sluzhebnye-slajdy.md#ЗАДАНИЕ:25; kod_skelet-konspekt-l1.md#ЗАДАНИЕ:13; kod_bootstrap-guard.md#ЗАДАНИЕ:66; kod_commit-ux.md#ЗАДАНИЕ:98; kod_tool-contract.md#ЗАДАНИЕ:73 |
| КРТ-006 | `вне-фаз` | 10 | kod_chitaemost.md#29; kod_razbor-kartoteki.md#29; kod_dek-paskal-v2.md#118; kod_dek-paskal.md#57; kod_gejty-shaga-6.md#38; kod_sluzhebnye-slajdy.md#42; kod_skelet-konspekt-l1.md#22; kod_bootstrap-guard.md#27; kod_commit-ux.md#28; kod_tool-contract.md#29 |
| КРТ-007 | `вне-фаз` | 10 | kod_klassifikacia-kartoteki.md#119; kod_brillianty-l1.md#334-337; kod_priruchenie-vneshnego.md#181-184; kod_dek-paskal-v2.md#41; kod_dek-paskal.md#25; kod_gejty-shaga-6.md#20; kod_sluzhebnye-slajdy.md#24; kod_skelet-konspekt-l1.md#12; kod_terminal-kanal.md#92-94,117-121; kod_tool-contract.md#12 |
| КРТ-008 | `вне-фаз` | 9 | kod_bootstrap.md#119-123; kod_gid.md#18-25; kod_polnyj-prohod-vneshnie.md#81-83; UROKI-FABRIKE.md(vneshnie-istorii)#37-41; kod_brillianty-l1.md#321-323; kod_svedenie-i-gejty.md#199-203; kod_dek-paskal-v2.md#291-302; kod_commit-ux.md#80; kod_terminal-kanal.md#96 |
| КРТ-009 | `вне-фаз` | 7 | kod_bootstrap.md#85; kod_obogatit-vvedenie.md#65-66; UROKI-FABRIKE.md(teorkat-l1)#43-46; kod_fib-kategorno.md#112-113; kod_razobrat-git.md#10,14; kod_chitaemost.md#17; kod_razbor-kartoteki.md#21 |
| КРТ-010 | `вне-фаз` | 7 | kod_vychitano.md#99-101,140; kod_chitaemost.md#143; UROKI-FABRIKE.md(mat-kostyak)#97-100,105-108,145-148; UROKI-FABRIKE.md(paskal-lekcia-sborka)#132-136 |
| КРТ-011a | `02-reserch` | 5 | kod_zapusk-korpusa.md#76; kod_biblioteka-vhodyashchee.md#116,165; kod_motivacii-l1-l8-l9.md#148; kod_poisk-listochki.md#225-228; kod_biblioteka-dobor.md#108-109 |
| КРТ-011b | `03-matbaza` | 1 | kod_riehl-b.md#64-66 |
| КРТ-012a | `02-reserch` | 4 | kod_riehl-lccc.md#30; kod_vychitka-istochnikov.md#192; kod_l4-motivaciya.md#47-48; kod_motivacii-l1-l8-l9.md#299 |
| КРТ-012b | `вне-фаз` | 1 | UROKI-FABRIKE.md(teorkat-programma-dizajn)#365-378 |
| КРТ-013a | `09-illustracii` | 3 | kod_kurs-avtonom.md#144; buffon/WORKLIST.md#108(§3); buffon/WORKLIST.md#214(§7 A3) |
| КРТ-013b | `10-sborka-qa` | 2 | kod_gejty-shaga-6.md#227; buffon/WORKLIST.md#113(§3) |
| КРТ-014 | `вне-фаз` | 5 | kod_motivacii-l1-l8-l9.md#336; kod_dobrat-vshir.md#74-76; kod_obogatit-vvedenie.md#71-72; UROKI-FABRIKE.md(teorkat-l1)#51-56; UROKI-FABRIKE.md(teorkat-l1)#83-86 |
| КРТ-015a | `08-sceny` | 2 | buffon/WORKLIST.md#109(§3); buffon/WORKLIST.md#112(§3) |
| КРТ-015b | `09-illustracii` | 2 | buffon/WORKLIST.md#110(§3); buffon/WORKLIST.md#111(§3) |
| КРТ-015c | `10-sborka-qa` | 1 | buffon/WORKLIST.md#114(§3) |
| КРТ-016a | `02-reserch` | 3 | kod_chego-net.md#63; kod_dajdzhesty-i-mit.md#67; kod_khl-kontent.md#40 |
| КРТ-016b | `03-matbaza` | 1 | kod_nno-i-shkolnye-opory.md#181-182 |
| КРТ-017a | `10-sborka-qa` | 3 | kod_lekcia1-pereverstka.md#149; buffon/WORKLIST.md#115; buffon/ZAHOD-01.md#189 |
| КРТ-017b | `вне-фаз` | 1 | kod_html-obshchiy.md#152-155 |
| КРТ-018a | `02-reserch` | 3 | kod_chego-net.md#135; kod_l4-l5-programma.md#77-79; kod_progon-subagentami.md#78 |
| КРТ-018b | `03-matbaza` | 1 | kod_absorb-vstrechi.md#108 |
| КРТ-019 | `вне-фаз` | 3 | kod_perechot-kataloga.md#118-122; kod_brillianty-l1.md#240; kod_port-oformlenia-v-build-doc.md#109 |
| КРТ-020a | `вне-фаз` | 1 | kod_faza1.md#124-126 |
| КРТ-020b | `02-reserch` | 1 | kod_gejty-kursa.md#225 |
| КРТ-020c | `03-matbaza` | 1 | kod_chitaemost.md#371-376 |
| КРТ-021 | `вне-фаз` | 3 | kod_shov-l4-l5.md#193-195; kod_vychitano.md#142; kod_zamykanie.md#148-152 |
| КРТ-022 | `вне-фаз` | 3 | kod_absorb-prizemlenie.md#64-67; kod_absorb-prizemlenie.md#60; kod_faza1-redesign.md#112-113 |
| КРТ-023a | `09-illustracii` | 2 | buffon/ZAHOD-02.md#93; buffon/ZAHOD-02.md#108 |
| КРТ-023b | `вне-фаз` | 1 | kod_navigacija.md#63-65 |
| КРТ-024 | `вне-фаз` | 3 | kod_maclane-smith.md#58-60; kod_pereverstka.md#90-91; kod_riehl-a.md#227 |
| КРТ-025 | `02-reserch` | 3 | UROKI-FABRIKE.md(teorkat-programma-dizajn)#323-332; UROKI-FABRIKE.md(teorkat-programma-dizajn)#349-364; kod_nochnaya-karta-oblastej.md#210-212 |
| КРТ-026 | `вне-фаз` | 2 | kod_karta-lekciy-8.md#ВОПРОСЫ:175; kod_terminal-kanal.md#ЗАДАНИЕ:32-33 |
| КРТ-027 | `вне-фаз` | 2 | kod_fix-latex.md#ПЛАН:118-121; kod_pravki-L6.md#ВОПРОСЫ:137 |
| КРТ-028a | `вне-фаз` | 1 | kod_spina.md#ПЛАН:76 |
| КРТ-028b | `06-tekst` | 1 | kod_lekcia1-modeli.md#ОТЧЁТ:212 |
| КРТ-029a | `05-raskadrovka` | 1 | kod_lekcia1-modeli.md#ОТЧЁТ:210 |
| КРТ-029b | `02-reserch` | 1 | kod_l4-motivaciya.md#ЗАДАНИЕ:49-50 |
| КРТ-030 | `вне-фаз` | 2 | kod_L4-html-v4.md#ОТЧЁТ:153; kod_generator.md#ВОПРОСЫ:107 |
| КРТ-031 | `02-reserch` | 2 | kod_zapusk-korpusa.md#ОТЧЁТ:72; kod_chego-net.md#ВОПРОСЫ:117 |
| КРТ-032 | `03-matbaza` | 2 | kod_chitaemost.md#ОТЧЁТ:231-232; kod_kostyak-rez.md#ОТЧЁТ:231-232 |
| КРТ-033 | `вне-фаз` | 2 | kod_razbor-kartoteki.md#УРОКИ ФАБРИКЕ:105-106; UROKI-FABRIKE.md(mat-kostyak)#164-168 |
| КРТ-034 | `03-matbaza` | 2 | UROKI-FABRIKE.md(mat-kostyak)#117-120; UROKI-FABRIKE.md(mat-kostyak)#179-182 |
| КРТ-035a | `вне-фаз` | 1 | kod_dvizhok-format.md#ЗАДАНИЕ:57 |
| КРТ-035b | `10-sborka-qa` | 1 | kod_gejty-shaga-6.md#ПЛАН:118-119 |
| КРТ-036 | `03-matbaza` | 2 | kod_riehl-b.md#УРОКИ ФАБРИКЕ:60-62; kod_riehl-a.md#УРОКИ ФАБРИКЕ:90-92 |
| КРТ-037 | `03-matbaza` | 2 | kod_mat-kostyak.md#УРОКИ ФАБРИКЕ:162-166; UROKI-FABRIKE.md(mat-kostyak)#65-68 |
| КРТ-038a | `вне-фаз` | 1 | kod_treker.md#ВОПРОСЫ:110 |
| КРТ-038b | `02-reserch` | 1 | kod_nochnaya-karta-oblastej.md#УРОКИ ФАБРИКЕ:103-105 |
| КРТ-039 | `вне-фаз` | 2 | kod_dobrat-vshir.md#УРОКИ ФАБРИКЕ:78-80; UROKI-FABRIKE.md(teorkat-l1)#87-90 |
| КРТ-040 | `вне-фаз` | 2 | kod_dobrat-vshir.md#УРОКИ ФАБРИКЕ:82-84; UROKI-FABRIKE.md(teorkat-l1)#91-94 |
| КРТ-041 | `вне-фаз` | 2 | kod_dobrat-vshir.md#УРОКИ ФАБРИКЕ:86-88; UROKI-FABRIKE.md(teorkat-l1)#95-100 |
| КРТ-042 | `02-reserch` | 2 | kod_obogatit-vvedenie.md#УРОКИ ФАБРИКЕ:68-69; UROKI-FABRIKE.md(teorkat-l1)#47-50 |
| КРТ-043 | `02-reserch` | 2 | kod_poisk-primerov.md#УРОКИ ФАБРИКЕ:67-69; UROKI-FABRIKE.md(teorkat-l1)#61-64 |
| КРТ-044 | `02-reserch` | 2 | kod_poisk-primerov.md#УРОКИ ФАБРИКЕ:75-77; UROKI-FABRIKE.md(teorkat-l1)#69-72 |
| КРТ-045 | `02-reserch` | 2 | kod_motivacii-l1-l8-l9.md#ЗАДАНИЕ:45-58; kod_shov-l4-l5.md#ЗАДАНИЕ:57 |
| КРТ-046 | `10-sborka-qa` | 2 | kod_dek-paskal-v2.md#ЗАДАНИЕ:9-10; kod_dek-paskal-v2.md#ЗАДАНИЕ:99-102 |
| КРТ-047 | `вне-фаз` | 1 | kod_razvedka-sborka.md#ВОПРОСЫ:60 |
| КРТ-048 | `вне-фаз` | 1 | kod_lekcia1-modeli.md#ОТЧЁТ:215 |
| КРТ-049 | `02-reserch` | 1 | kod_kurs-avtonom.md#ОТЧЁТ:142 |
| КРТ-050 | `02-reserch` | 1 | kod_nochnaya-karta-oblastej.md#УРОКИ ФАБРИКЕ:95-97 |
| КРТ-051 | `02-reserch` | 1 | kod_dajdzhesty-i-mit.md#ЗАДАНИЕ:8-14 |
| КРТ-052 | `03-matbaza` | 1 | kod_zamykanie.md#УРОКИ ФАБРИКЕ:166-170 |
| КРТ-053 | `вне-фаз` | 1 | UROKI-FABRIKE.md(mat-kostyak)#85-88 |
| КРТ-054 | `03-matbaza` | 1 | kod_zamykanie.md#УРОКИ ФАБРИКЕ:154-158 |
| КРТ-055 | `03-matbaza` | 1 | kod_riehl-a.md#УРОКИ ФАБРИКЕ:94-96 |
| КРТ-056 | `02-reserch` | 1 | kod_nochnaya-karta-oblastej.md#УРОКИ ФАБРИКЕ:107-109 |
| КРТ-057 | `02-reserch` | 1 | kod_poisk-listochki.md#УРОКИ ФАБРИКЕ:210-214 |
| КРТ-058 | `02-reserch` | 1 | kod_priruchenie-vneshnego.md#ПЛАН:205-207 |
| КРТ-059 | `02-reserch` | 1 | kod_svedenie-i-gejty.md#ОТЧЁТ:322-323 |
| КРТ-060 | `вне-фаз` | 1 | UROKI-FABRIKE.md(teorkat-programma-dizajn)#280-295 |
| КРТ-061 | `вне-фаз` | 1 | UROKI-FABRIKE.md(teorkat-programma-dizajn)#296-307 |
| КРТ-062 | `вне-фаз` | 1 | UROKI-FABRIKE.md(teorkat-programma-dizajn)#308-322 |
| КРТ-063 | `вне-фаз` | 1 | UROKI-FABRIKE.md(teorkat-programma-dizajn)#333-348 |
| КРТ-064 | `вне-фаз` | 1 | kod_obogatit-vvedenie.md#УРОКИ ФАБРИКЕ:62-63 |
| КРТ-065 | `02-reserch` | 1 | kod_poisk-primerov.md#УРОКИ ФАБРИКЕ:63-65 |
| КРТ-066 | `02-reserch` | 1 | kod_poisk-primerov.md#УРОКИ ФАБРИКЕ:71-73 |
| КРТ-067 | `02-reserch` | 1 | kod_poisk-primerov.md#УРОКИ ФАБРИКЕ:79-81 |
| КРТ-068 | `вне-фаз` | 1 | UROKI-FABRIKE.md(teorkat-programma-dizajn)#213-279 |
| КРТ-069 | `вне-фаз` | 1 | kod_katalog.md#ОТЧЁТ:93 |
| КРТ-070 | `вне-фаз` | 1 | kod_katalog.md#ОТЧЁТ:100 |
| КРТ-071 | `вне-фаз` | 1 | kod_spina.md#ВОПРОСЫ:95 |
| КРТ-072 | `вне-фаз` | 1 | kod_treker.md#ЗАДАНИЕ:18-19 |
| КРТ-073 | `вне-фаз` | 1 | kod_treker.md#ВОПРОСЫ:104 |
| КРТ-074 | `вне-фаз` | 1 | kod_base-buffon.md#ОТЧЁТ:172-178 |
| КРТ-075 | `вне-фаз` | 1 | kod_base-buffon.md#ОТЧЁТ:209-215 |
| КРТ-076 | `вне-фаз` | 1 | kod_infra.md#ПЛАН:55-61 |
| КРТ-077 | `02-reserch` | 1 | kod_kurs-avtonom.md#ОТЧЁТ:143 |
| КРТ-078 | `02-reserch` | 1 | kod_kurs-avtonom.md#ОТЧЁТ:145 |
| КРТ-079 | `03-matbaza` | 1 | kod_kurs-avtonom.md#ОТЧЁТ:146 |
| КРТ-080 | `05-raskadrovka` | 1 | kod_lekcia1-modeli.md#ОТЧЁТ:218 |
| КРТ-081 | `06-tekst` | 1 | kod_lekcia1-modeli.md#ОТЧЁТ:225 |
| КРТ-082 | `02-reserch` | 1 | kod_zapusk-korpusa.md#ОТЧЁТ:88 |
| КРТ-083 | `02-reserch` | 1 | kod_riehl-lccc.md#ВОПРОСЫ:115 |
| КРТ-084 | `02-reserch` | 1 | kod_vychitka-istochnikov.md#ВОПРОСЫ:173 |
| КРТ-085 | `02-reserch` | 1 | kod_vychitka-istochnikov.md#ОТЧЁТ:256-266 |
| КРТ-086 | `02-reserch` | 1 | kod_vychitka-istochnikov.md#ВОПРОСЫ:176 |
| КРТ-087 | `вне-фаз` | 1 | kod_dajdzhesty-i-mit.md#ЗАДАНИЕ:94 |
| КРТ-088 | `02-reserch` | 1 | kod_karta-lekciy-8.md#ВОПРОСЫ:173 |
| КРТ-089 | `02-reserch` | 1 | kod_karta-lekciy-8.md#ОТЧЁТ:215 |
| КРТ-090 | `02-reserch` | 1 | kod_karta-lekciy-8.md#ОТЧЁТ:208 |
| КРТ-091 | `02-reserch` | 1 | kod_l4-l5-vlivanie.md#УРОКИ ФАБРИКЕ:62-64 |
| КРТ-092 | `02-reserch` | 1 | kod_molchalivye-opory.md#ЗАДАНИЕ:7-9 |
| КРТ-093 | `02-reserch` | 1 | kod_molchalivye-opory.md#ВОПРОСЫ:178 |
| КРТ-094 | `02-reserch` | 1 | kod_motivacii-l1-l8-l9.md#ОТЧЁТ:295 |
| КРТ-095 | `02-reserch` | 1 | kod_nno-i-shkolnye-opory.md#ЗАДАНИЕ:27 |
| КРТ-096 | `02-reserch` | 1 | kod_nno-i-shkolnye-opory.md#ОТЧЁТ:192 |
| КРТ-097 | `02-reserch` | 1 | kod_shov-l4-l5.md#ЗАДАНИЕ:12-16 |
| КРТ-098 | `02-reserch` | 1 | kod_shov-l4-l5.md#ЗАДАНИЕ:64 |
| КРТ-099 | `вне-фаз` | 1 | kod_razobrat-git.md#ВОПРОСЫ:238 |
| КРТ-100 | `03-matbaza` | 1 | kod_vidy-obzor.md#УРОКИ ФАБРИКЕ:97-98 |
| КРТ-101 | `03-matbaza` | 1 | kod_vidy-obzor.md#УРОКИ ФАБРИКЕ:100-101 |
| КРТ-102 | `вне-фаз` | 1 | kod_vidy-obzor.md#ПЛАН:111-119 |
| КРТ-103 | `02-reserch` | 1 | kod_nochnaya-karta-oblastej.md#УРОКИ ФАБРИКЕ:99-101 |
| КРТ-104 | `02-reserch` | 1 | kod_nochnaya-karta-oblastej.md#УРОКИ ФАБРИКЕ:111-113 |
| КРТ-105 | `02-reserch` | 1 | kod_nochnaya-karta-oblastej.md#УРОКИ ФАБРИКЕ:115-117 |
| КРТ-106 | `02-reserch` | 1 | kod_nochnaya-karta-oblastej.md#УРОКИ ФАБРИКЕ:119-121 |
| КРТ-107 | `03-matbaza` | 1 | kod_riehl-b.md#ВОПРОСЫ:131 |
| КРТ-108 | `03-matbaza` | 1 | kod_zamykanie.md#УРОКИ ФАБРИКЕ:142-146 |
| КРТ-109 | `03-matbaza` | 1 | kod_zamykanie.md#ОТЧЁТ:419-420 |
| КРТ-110 | `03-matbaza` | 1 | kod_absorb-vstrechi.md#ПЛАН:105-106 |
| КРТ-111 | `03-matbaza` | 1 | kod_absorb-vstrechi.md#ПЛАН:107 |
| КРТ-112 | `03-matbaza` | 1 | kod_dokat-pod-kat.md#ЗАДАНИЕ:6 |
| КРТ-113 | `03-matbaza` | 1 | kod_dokat-pod-kat.md#ПЛАН:73 |
| КРТ-114 | `03-matbaza` | 1 | kod_kostyak-rez.md#ВОПРОСЫ:136 |
| КРТ-115 | `03-matbaza` | 1 | kod_kostyak-rez.md#УРОКИ ФАБРИКЕ:98-102 |
| КРТ-116 | `03-matbaza` | 1 | kod_kostyak-rez.md#УРОКИ ФАБРИКЕ:104-108 |
| КРТ-117 | `03-matbaza` | 1 | kod_mat-kostyak.md#УРОКИ ФАБРИКЕ:138-142 |
| КРТ-118 | `03-matbaza` | 1 | kod_mat-kostyak.md#УРОКИ ФАБРИКЕ:144-148 |
| КРТ-119 | `03-matbaza` | 1 | kod_mat-kostyak.md#УРОКИ ФАБРИКЕ:156-160 |
| КРТ-120 | `03-matbaza` | 1 | kod_mat-kostyak.md#ВОПРОСЫ:223 |
| КРТ-121 | `03-matbaza` | 1 | UROKI-FABRIKE.md(mat-kostyak)#69-72 |
| КРТ-122 | `03-matbaza` | 1 | UROKI-FABRIKE.md(mat-kostyak)#73-76 |
| КРТ-123 | `03-matbaza` | 1 | UROKI-FABRIKE.md(mat-kostyak)#77-80 |
| КРТ-124 | `03-matbaza` | 1 | UROKI-FABRIKE.md(mat-kostyak)#81-84 |
| КРТ-125 | `03-matbaza` | 1 | UROKI-FABRIKE.md(mat-kostyak)#109-112 |
| КРТ-126 | `вне-фаз` | 1 | UROKI-FABRIKE.md(mat-kostyak)#113-116 |
| КРТ-127 | `вне-фаз` | 1 | UROKI-FABRIKE.md(mat-kostyak)#125-128 |
| КРТ-128 | `вне-фаз` | 1 | UROKI-FABRIKE.md(mat-kostyak)#129-132 |
| КРТ-129 | `вне-фаз` | 1 | UROKI-FABRIKE.md(mat-kostyak)#137-140 |
| КРТ-130 | `вне-фаз` | 1 | UROKI-FABRIKE.md(mat-kostyak)#141-144 |
| КРТ-131 | `03-matbaza` | 1 | UROKI-FABRIKE.md(mat-kostyak)#169-173 |
| КРТ-132 | `вне-фаз` | 1 | UROKI-FABRIKE.md(mat-kostyak)#174-178 |
| КРТ-133 | `02-reserch` | 1 | kod_napolnit-bazu-l1.md#ВОПРОСЫ:93 |
| КРТ-134 | `02-reserch` | 1 | kod_napolnit-bazu-l1.md#ПЛАН:73 |
| КРТ-135 | `02-reserch` | 1 | kod_polnyj-prohod-vneshnie.md#УРОКИ ФАБРИКЕ:85-87 |
| КРТ-136 | `вне-фаз` | 1 | UROKI-FABRIKE.md(vneshnie-istorii)#42-48 |
| КРТ-137 | `02-reserch` | 1 | kod_brillianty-l1.md#УРОКИ ФАБРИКЕ:329-332 |
| КРТ-138 | `02-reserch` | 1 | kod_konsolidacia-l1.md#УРОКИ ФАБРИКЕ:208-210 |
| КРТ-139 | `02-reserch` | 1 | kod_konsolidacia-l1.md#УРОКИ ФАБРИКЕ:212-214 |
| КРТ-140 | `02-reserch` | 1 | kod_konsolidacia-l1.md#ОТЧЁТ:383 |
| КРТ-141 | `вне-фаз` | 1 | kod_poisk-listochki.md#УРОКИ ФАБРИКЕ:216-219 |
| КРТ-142 | `02-reserch` | 1 | kod_priruchenie-vneshnego.md#УРОКИ ФАБРИКЕ:171-174 |
| КРТ-143 | `02-reserch` | 1 | kod_priruchenie-vneshnego.md#УРОКИ ФАБРИКЕ:176-179 |
| КРТ-144 | `02-reserch` | 1 | kod_priruchenie-vneshnego.md#ОТЧЁТ:273 |
| КРТ-145 | `02-reserch` | 1 | kod_svedenie-i-gejty.md#УРОКИ ФАБРИКЕ:179-181 |
| КРТ-146 | `02-reserch` | 1 | kod_svedenie-i-gejty.md#УРОКИ ФАБРИКЕ:183-185 |
| КРТ-147 | `10-sborka-qa` | 1 | kod_dek-paskal-v2.md#УРОКИ ФАБРИКЕ:253-262 |
| КРТ-148 | `10-sborka-qa` | 1 | kod_dek-paskal-v2.md#УРОКИ ФАБРИКЕ:264-274 |
| КРТ-149 | `09-illustracii` | 1 | kod_dek-paskal-v2.md#УРОКИ ФАБРИКЕ:276-289 |
| КРТ-150 | `06-tekst` | 1 | kod_gejty-shaga-6.md#УРОКИ ФАБРИКЕ:100-103 |
| КРТ-151 | `06-tekst` | 1 | kod_gejty-shaga-6.md#УРОКИ ФАБРИКЕ:105-108 |
| КРТ-152 | `06-tekst` | 1 | kod_gejty-shaga-6.md#ВОПРОСЫ:178-179 |
| КРТ-РАЗН · 02-reserch | `02-reserch` | 10 | kod_zona-c-topos.md; kod_poisk-primerov.md#ОТЧЁТ:267-268; kod_skelet-konspekt-l1.md#УРОКИ ФАБРИКЕ:67-68; kod_biblioteka-dobor.md#ОТЧЁТ:99-106; kod_dobor-skelet.md#ОТЧЁТ:72; kod_dobor-skelet.md#ОТЧЁТ:66; kod_biblioteka-mir1.md#ОТЧЁТ:90-93; kod_dobor-do-10.md#ОТЧЁТ:156-160; kod_dobor-do-10.md#ВОПРОСЫ:148; kod_procedura-poiska.md#ВОПРОСЫ:101 |
| КРТ-РАЗН · 03-matbaza | `03-matbaza` | 5 | kod_shov-l4-l5.md#ЗАДАНИЕ:46; kod_riehl-b.md#ВОПРОСЫ:129-130; kod_skelet-konspekt-l1.md#ВОПРОСЫ:102-103; UROKI-FABRIKE.md(teksty-l1)#43-46; buffon/ZAHOD-04.md#ВОПРОСЫ:153,171 |
| КРТ-РАЗН · 04-gibrid-istochnik | `04-gibrid-istochnik` | 1 | UROKI-FABRIKE.md(paskal-lekcia-sborka)#59-66 |
| КРТ-РАЗН · 05-raskadrovka | `05-raskadrovka` | 1 | UROKI-FABRIKE.md(paskal-lekcia-sborka)#67-71 |
| КРТ-РАЗН · 06-tekst | `06-tekst` | 1 | UROKI-FABRIKE.md(teksty-l1)#47-82 |
| КРТ-РАЗН · 07-verstka | `07-verstka` | 2 | kod_sluzhebnye-slajdy.md#ЗАДАНИЕ:8; kod_sluzhebnye-slajdy.md#ОТЧЁТ:257-258 |
| КРТ-РАЗН · 08-sceny | `08-sceny` | 5 | kod_gejty-shaga-6.md#ОТЧЁТ:231; kod_gejty-shaga-6.md#ОТЧЁТ:232; UROKI-FABRIKE.md(paskal-lekcia-sborka)#54-58; UROKI-FABRIKE.md(paskal-lekcia-sborka)#77-81; UROKI-FABRIKE.md(paskal-lekcia-sborka)#92-96 |
| КРТ-РАЗН · 09-illustracii | `09-illustracii` | 4 | UROKI-FABRIKE.md(paskal-lekcia-sborka)#87-91; UROKI-FABRIKE.md(paskal-lekcia-sborka)#97-101; kod_skelet-konspekt-l1.md#УРОКИ ФАБРИКЕ:70-71; kod_html-L2.md#ОТЧЁТ:180 |
| КРТ-РАЗН · 10-sborka-qa | `10-sborka-qa` | 17 | kod_dek-paskal-v2.md#УРОКИ ФАБРИКЕ:240-251; kod_gejty-shaga-6.md#ОТЧЁТ:225,226,228,229,230,237,239; kod_sluzhebnye-slajdy.md#УРОКИ ФАБРИКЕ:113-115,117-119,125-127; kod_sluzhebnye-slajdy.md#ПЛАН:135; kod_sluzhebnye-slajdy.md#ОТЧЁТ:269; UROKI-FABRIKE.md(paskal-lekcia-sborka)#82-86,102-106,122-126; kod_port-oformlenia-v-build-doc.md#ОТЧЁТ:180-181 |
| КРТ-РАЗН · вне-фаз | `вне-фаз` | 85 | kod_bootstrap.md#ВОПРОСЫ:102; kod_gid.md#ПЛАН:78,80; kod_gid.md#ОТЧЁТ:115; kod_karta-lekciy-8.md#ЗАДАНИЕ:113; kod_khl-kontent.md#ЗАДАНИЕ:100; kod_vneshnyaya-merka.md#ЗАДАНИЕ:6-8; kod_vneshnyaya-merka.md#ОТЧЁТ:319,269-272; UROKI-FABRIKE.md(teorkat-l1)#39-42,65-68,73-76; kod_fib-kategorno.md#УРОКИ ФАБРИКЕ:115-117,119-120; kod_razobrat-git.md#ЗАДАНИЕ:15; kod_vidy-obzor.md#ОТЧЁТ:155-181,311-316; kod_chitaemost.md#ЗАДАНИЕ:144; kod_chitaemost.md#УРОКИ ФАБРИКЕ:157-163,165-171; kod_dvizhok-format.md#ЗАДАНИЕ:32,70-72; kod_kostyak-rez.md#ЗАДАНИЕ:42; kod_resheniya.md#УРОКИ ФАБРИКЕ:168-170,172-174; UROKI-FABRIKE.md(mat-kostyak)#61-64,89-92,93-96,121-124,149-153,154-158; kod_priruchenie-vneshnego.md#ОТЧЁТ:275-276; kod_sluzhebnye-slajdy.md#УРОКИ ФАБРИКЕ:121-123; UROKI-FABRIKE.md(paskal-lekcia-sborka)#39-43,44-48,49-53,107-111,137-140; kod_skelet-konspekt-l1.md#ЗАДАНИЕ:10; kod_skelet-konspekt-l1.md#УРОКИ ФАБРИКЕ:73-74; UROKI-FABRIKE.md(teksty-l1)#39-42; kod_bootstrap-guard.md#ЗАДАНИЕ:6,42(×2); kod_bootstrap-guard.md#ОТЧЁТ:122-123,125; kod_commit-ux.md#ЗАДАНИЕ:37,38,39,40,57-59; kod_commit-ux.md#ВОПРОСЫ:130; kod_tool-contract.md#ЗАДАНИЕ:6(×2),7; buffon/ZAHOD-02.md#ОТЧЁТ:92; kod_skelet-mir2.md#ЗАДАНИЕ:5; kod_statya-mir2.md#ОТЧЁТ:138; kod_vychitano-backfill.md#ЗАДАНИЕ:6; kod_illustracii-build-doc.md#ОТЧЁТ:139-141; kod_port-oformlenia-v-build-doc.md#ОТЧЁТ:186-188; kod_dobor-do-10.md#ОТЧЁТ:192,180; kod_html-v3.md#ЗАДАНИЕ:6; kod_procedura-poiska.md#ОТЧЁТ:142-144,137; kod_progon-subagentami.md#ОТЧЁТ:76,79; kod_razvedka-sborka.md#ОТЧЁТ:89; kod_zapusk-progona-2.md#ОТЧЁТ:73-87; kod_zapusk-progona-2.md#ВОПРОСЫ:60-61; kod_zapusk-progona.md#ОТЧЁТ:73-79; kod_dobor-L2.md#ОТЧЁТ:108; kod_fix-latex.md#ЗАДАНИЕ:9,10-11; kod_fix-latex.md#ОТЧЁТ:147,165-166; kod_fix-latex.md#ПЛАН:116; kod_pravki-L6.md#ОТЧЁТ:158; kod_usilenie-svyazey.md#ОТЧЁТ:116-118; kod_perenos-i-checker.md#ОТЧЁТ:110-112,116-117,143; kod_ekran2.md#ОТЧЁТ:114; kod_uborka-renumber.md#ЗАДАНИЕ:5; kod_uborka-renumber.md#ВОПРОСЫ:84 |

**Сверка охвата Раздела 1:** Σ кратностей = 461 = заявленному корпусу `skelet-ispolnitelej.tsv` (id `I0001`…`I0461`). Пересчёт: `python3 _data_razdel1.py` в этой папке.

**Итог по фазам (Раздел 1):** вне-фаз 250 · 02-reserch 91 · 03-matbaza 49 · 10-sborka-qa 30 · 09-illustracii 13 · 08-sceny 8 · 06-tekst 7 · 05-raskadrovka 5 · 04-gibrid-istochnik 4 · 07-verstka 3 · 01-brief 1 · 04.5-intervyu 0.

## Раздел 2 · корпус «реплики владельца» — предметы недовольства (`KRATNOST-vladelca.md`)

> Источник: `KRATNOST-vladelca.md`, машинная группировка по ПРЕДМЕТУ недовольства, корпус 1379 записей (`V0001`…`V1379`, `skelet-vladelca.tsv`; join адресов со skelet даёт 1144/1379 = 83 % прямого совпадения — 235 адресов ведут на `SESSIYA.md`/иные файлы шире строгого V-корпуса, это честно назвовано, не натянуто). **Разнесено субагентами по фазе A0 этого захода (2026-08-05); группы, разнородные по фазам, разрезаны на подгруппы `a/b/c…`** — этот корпус (топик, не механизм) оказался НАМНОГО более разнородным по фазам, чем Раздел 1: почти каждая из 56 исходных групп разрезалась на 5–11 подгрупп. Адреса сокращены — базовая папка `teorkat-vvedenie/repeticia/` для `akt-1-razbor.md`/`PRAVKI*.md`, `_studio/zhurnal/<арка>/` для `SESSIYA.md`/`RAZBOR-posle-lekcii*.md`, если явно не указан другой корень.

| id | фаза | кратность | адреса (файл:строки; базовая папка `teorkat-vvedenie/repeticia/` для `akt-1-razbor.md`/`PRAVKI*.md`, `_studio/zhurnal/<арка>/` для `SESSIYA.md`/`RAZBOR-posle-lekcii*.md`, если не указано иное) |
|---|---|---|---|
| КРВ-01a | `01-brief` | 17 | teorkat-programma-dizajn/SESSIYA.md:423,975-979; teorkat-motivacia/SESSIYA.md:17-18,96-97,321,365-366,394,1269; mat-kostyak/SESSIYA.md:102-108; teorkat-landshaft/SESSIYA.md:70; teorkat-l1/SESSIYA.md:24,88; vneshnie-istorii/SESSIYA.md:40(×2); osnovanie-vvedenie/SESSIYA.md:23; teorkat-programma/SESSIYA.md:48(a); l3-kodirovanie/SESSIYA.md:58 |
| КРВ-01b | `04-gibrid-istochnik` | 16 | zamechaniya-L1-process-first.md:3,17; l2-skolko-informacii/SESSIYA.md:45; teorkat-programma-dizajn/SESSIYA.md:156-158; lekcia-1/SESSIYA.md:559-566,959-963,1013-1015; teorkat-motivacia/SESSIYA.md:14-15,34-35,261,927; teorkat-l1/SESSIYA.md:87(×2); paskal-lekcia-sborka/SESSIYA.md:23-26; vneshnie-istorii/SESSIYA.md:63(a); l3-kodirovanie/SESSIYA.md:34 |
| КРВ-01c | `04.5-intervyu` | 14 | PRAVKI.md(teorkat-vvedenie):528; zamechaniya-mosty-kartoteka.md:5; teorkat-programma-dizajn/SESSIYA.md:22-28,1015-1018; lekcia-1/SESSIYA.md:35-38,54-62,235-249,317-326; teorkat-motivacia/SESSIYA.md:286-288,621-622,917,1013; vvedenie-sborka/SESSIYA.md:111; teorkat-programma/SESSIYA.md:48(b) |
| КРВ-01d | `05-raskadrovka` | 13 | RAZBOR-posle-lekcii-2026-07-27.md:186-188,190-191,569-571; PRAVKI-sceny-i-animacii.md:40-41; PRAVKI.md:369; l2-skolko-informacii/SESSIYA.md:117; teorkat-programma-dizajn/SESSIYA.md:292,293,491; krivaya-drakona/SESSIYA.md:155,158; teorkat-motivacia/SESSIYA.md:217; teorkat-landshaft/SESSIYA.md:99 |
| КРВ-01e | `06-tekst` | 8 | RAZBOR-posle-lekcii-2026-07-27.md:87-89,274; PRAVKI.md:133-134,256-257,546; krivaya-drakona/SESSIYA.md:136; teksty-l1/SESSIYA.md:53,70 |
| КРВ-01f | `08-sceny` | 8 | akt-1-razbor.md:160-164,204-208,270-278; RAZBOR-posle-lekcii-2026-07-27.md:99-101,229; PRAVKI-sceny-i-animacii.md:65,70-71; PRAVKI.md:323 |
| КРВ-01g | `02-reserch` | 4 | lekcia-1/SESSIYA.md:627-643; teorkat-motivacia/SESSIYA.md:470; vneshnie-istorii/SESSIYA.md:63(b),75 |
| КРВ-01h | `07-verstka` | 2 | RAZBOR-posle-lekcii-2026-07-27.md:45-46,426 |
| КРВ-01i | `03-matbaza` | 2 | zamechaniya-statya-mir2.md:31; teorkat-programma/SESSIYA.md:39 |
| КРВ-01j | `вне-фаз` | 2 | mat-kostyak/SESSIYA.md:34-35; teksty-l1/SESSIYA.md:55 |
| КРВ-02a | `05-raskadrovka` | 16 | akt-1-razbor.md:38; RAZBOR-posle-lekcii-2026-07-27.md:8-10; PRAVKI.md:103-105,184,187-189,442,467-469,591-593,592-593,612; l2-skolko-informacii/SESSIYA.md:67; krivaya-drakona/SESSIYA.md:172; konspekt-l1/SESSIYA.md:41(×2); teorkat-l1/SESSIYA.md:21; paskal-lekcia-sborka/SESSIYA.md:160-162 |
| КРВ-02b | `01-brief` | 15 | l2-skolko-informacii/SESSIYA.md:115,120(a); teorkat-programma-dizajn/SESSIYA.md:162,586-592,1586; krivaya-drakona/SESSIYA.md:82,508; teorkat-motivacia/SESSIYA.md:1217,1227; dovodka-fabriki/SESSIYA.md:409; mat-kostyak/SESSIYA.md:23; teorkat-landshaft/SESSIYA.md:103; osnovanie-vvedenie/SESSIYA.md:32(×2); l3-kodirovanie/SESSIYA.md:34 |
| КРВ-02c | `04-gibrid-istochnik` | 13 | zamechaniya-statya-mir2.md:41; lekcia-1/SESSIYA.md:472-479,481-486,520-524,612-615,674-684,1090-1094; teorkat-motivacia/SESSIYA.md:921,942,1014; mat-kostyak/SESSIYA.md:146-154,200-218,258-271 |
| КРВ-02d | `04.5-intervyu` | 12 | informacia-i-kody/SESSIYA.md:41; teorkat-programma-dizajn/SESSIYA.md:958-962,981-985,1011,1018; lekcia-1/SESSIYA.md:35-38(×3),979-983(a); teorkat-l1/SESSIYA.md:48(a),49; dovodka-l1/SESSIYA.md:35 |
| КРВ-02e | `вне-фаз` | 10 | PRAVKI.md:626; zamechaniya-statya-mir2.md:68; teorkat-programma-dizajn/SESSIYA.md:34; teorkat-motivacia/SESSIYA.md:87-88; dovodka-fabriki/SESSIYA.md:103,435,179,215,398; teksty-l1/SESSIYA.md:45 |
| КРВ-02f | `02-reserch` | 9 | zamechaniya-mosty-kartoteka.md:9,21; l2-skolko-informacii/SESSIYA.md:120(b); krivaya-drakona/SESSIYA.md:272; lekcia-1/SESSIYA.md:215-222,387-393,979-983(b); teorkat-motivacia/SESSIYA.md:1230; l3-kodirovanie/SESSIYA.md:39 |
| КРВ-02g | `08-sceny` | 3 | PRAVKI-final.md:203; PRAVKI-sceny-i-animacii.md:9; krivaya-drakona/SESSIYA.md:328 |
| КРВ-02h | `06-tekst` | 2 | PRAVKI-final.md:32; teorkat-l1/SESSIYA.md:52 |
| КРВ-02i | `09-illustracii` | 1 | RAZBOR-posle-lekcii-2026-07-27.md:207-209 |
| КРВ-02j | `07-verstka` | 1 | mat-kostyak/SESSIYA.md:567-569 |
| КРВ-02k | `10-sborka-qa` | 1 | konspekt-l1/SESSIYA.md:97 |
| КРВ-03a | `07-verstka` | 21 | akt-1-razbor.md:78-86,98-104; RAZBOR-posle-lekcii-2026-07-27.md:132,199; PRAVKI-final.md:26,56,145-146,160; PRAVKI.md:47-48,115-117,228,349,381; fibonacci-kurs/SESSIYA.md:39,41,42; krivaya-drakona/SESSIYA.md:294(b); dovodka-fabriki/SESSIYA.md:81; mat-kostyak/SESSIYA.md:567-569(b); dovodka-l1/SESSIYA.md:201; l3-kodirovanie/SESSIYA.md:50 |
| КРВ-03b | `05-raskadrovka` | 21 | RAZBOR-posle-lekcii-2026-07-27.md:11-12,25-26,144; PRAVKI.md:41-43,50-51,60-63,62-63,76-78,91-92,94-96,143-144,421,457,522,523,536-537,537; sborka-konvejera/SESSIYA.md:79; dovodka-l1/SESSIYA.md:69,182; teksty-l1/SESSIYA.md:35 |
| КРВ-03c | `06-tekst` | 11 | PRAVKI-final.md:58; PRAVKI.md:85-87,107-109,373,506,529; krivaya-drakona/SESSIYA.md:294(a); teorkat-motivacia/SESSIYA.md:28-29; dovodka-fabriki/SESSIYA.md:400,409(b); dovodka-l1/SESSIYA.md:190 |
| КРВ-03d | `08-sceny` | 7 | PRAVKI-final.md:44; PRAVKI-sceny-i-animacii.md:11-12; PRAVKI.md:59-60,335,518,612-613; paskal-lekcia-sborka/SESSIYA.md:177-178 |
| КРВ-03e | `09-illustracii` | 6 | RAZBOR-posle-lekcii-2026-07-27.md:368-370,461-462; PRAVKI.md:351; krivaya-drakona/SESSIYA.md:608; teorkat-motivacia/SESSIYA.md:528-529; dovodka-l1/SESSIYA.md:110 |
| КРВ-03f | `04-gibrid-istochnik` | 6 | zamechaniya-L1-process-first.md:9,25; l2-skolko-informacii/SESSIYA.md:43; teorkat-programma-dizajn/SESSIYA.md:1199-1201; lekcia-1/SESSIYA.md:488-498; vneshnie-istorii/SESSIYA.md:51 |
| КРВ-03g | `01-brief` | 4 | geometria-6-nagliadnaya/SESSIYA.md:11; teorkat-motivacia/SESSIYA.md:157-158,942(b); teorkat-landshaft/SESSIYA.md:173 |
| КРВ-03h | `02-reserch` | 3 | informacia-i-kody/SESSIYA.md:28; teorkat-motivacia/SESSIYA.md:439,657 |
| КРВ-03i | `04.5-intervyu` | 1 | teorkat-programma-dizajn/SESSIYA.md:1010 |
| КРВ-03j | `вне-фаз` | 1 | dovodka-fabriki/SESSIYA.md:4 |
| КРВ-04a | `вне-фаз` | 22 | akt-1-razbor.md:35; PRAVKI.md:556; zamechaniya-statya-mir2.md:41; zamechaniya-disciplina-kartochek.md:1; sborka-konvejera/SESSIYA.md:120; geometria-6-nagliadnaya/SESSIYA.md:16; informacia-i-kody/SESSIYA.md:54; teorkat-programma-dizajn/SESSIYA.md:40,718-722; krivaya-drakona/SESSIYA.md:111,526; lekcia-1/SESSIYA.md:40-42,97-101,265-276,387-393; teorkat-motivacia/SESSIYA.md:222,292,879,917; dovodka-fabriki/SESSIYA.md:278; mat-kostyak/SESSIYA.md:12-14,158-160 |
| КРВ-04b | `04-gibrid-istochnik` | 10 | zamechaniya-L1-process-first.md:11,21; fibonacci-kurs/SESSIYA.md:38; teorkat-programma-dizajn/SESSIYA.md:408-411; lekcia-1/SESSIYA.md:176-180; teorkat-l1/SESSIYA.md:50,87; paskal-lekcia-sborka/SESSIYA.md:105-107; dovodka-l1/SESSIYA.md:72; teksty-l1/SESSIYA.md:33 |
| КРВ-04c | `05-raskadrovka` | 10 | PRAVKI-final.md:156,185,218; PRAVKI.md:102-103,189-191,174,472-473; krivaya-drakona/SESSIYA.md:540; lekcia-1/SESSIYA.md:965-973; dovodka-l1/SESSIYA.md:220 |
| КРВ-04d | `02-reserch` | 8 | mat-kostyak/SESSIYA.md:102-110,158-160,258-264,273-284; vvedenie-sborka/SESSIYA.md:74; vneshnie-istorii/SESSIYA.md:32,76; osnovanie-vvedenie/SESSIYA.md:28 |
| КРВ-04e | `06-tekst` | 5 | RAZBOR-posle-lekcii-2026-07-27.md:276,456-457; PRAVKI.md:350,505; konspekt-l1/SESSIYA.md:44 |
| КРВ-04f | `01-brief` | 5 | mat-kostyak/SESSIYA.md:466-472; teorkat-l1/SESSIYA.md:20; vvedenie-sborka/SESSIYA.md:41; osnovanie-vvedenie/SESSIYA.md:19,24 |
| КРВ-04g | `08-sceny` | 3 | PRAVKI-final.md:191-192,256; krivaya-drakona/SESSIYA.md:255 |
| КРВ-04h | `09-illustracii` | 2 | RAZBOR-posle-lekcii-2026-07-27.md:61,365-366 |
| КРВ-04i | `03-matbaza` | 1 | krivaya-drakona/SESSIYA.md:612 |
| КРВ-04j | `07-verstka` | 1 | krivaya-drakona/SESSIYA.md:717 |
| КРВ-04k | `04.5-intervyu` | 1 | konspekt-l1/SESSIYA.md:152 |
| КРВ-05a | `02-reserch` | 26 | zamechaniya-issledovanie-idei.md:7; informacia-i-kody/SESSIYA.md:30,41,59,66; reserch-zadach/SESSIYA.md:23; l2-skolko-informacii/SESSIYA.md:67,117; krivaya-drakona/SESSIYA.md:138,176; lekcia-1/SESSIYA.md:195-203,224-233,306-315,481-486,803-810; teorkat-motivacia/SESSIYA.md:212,329,415(×2),421; mat-kostyak/SESSIYA.md:476-483(×2); vvedenie-sborka/SESSIYA.md:72; l3-kodirovanie/SESSIYA.md:10(×2),12 |
| КРВ-05b | `вне-фаз` | 26 | l2-skolko-informacii/SESSIYA.md:16,26,67,107(×2),118; krivaya-drakona/SESSIYA.md:107,109,136,187,225,328,392,448,484(×3),606,616,638; teorkat-motivacia/SESSIYA.md:208,267-268,296-297,417-418; l3-kodirovanie/SESSIYA.md:41,47 |
| КРВ-05c | `06-tekst` | 3 | PRAVKI.md(teorkat-vvedenie):521; fibonacci-kurs/SESSIYA.md:29; dovodka-fabriki/SESSIYA.md:52 |
| КРВ-05d | `05-raskadrovka` | 2 | RAZBOR-posle-lekcii-2026-07-27.md:196-197; PRAVKI.md(teorkat-vvedenie):101-102 |
| КРВ-05e | `04-gibrid-istochnik` | 2 | teorkat-motivacia/SESSIYA.md:390,395 |
| КРВ-05f | `04.5-intervyu` | 1 | l2-skolko-informacii/SESSIYA.md:32 |
| КРВ-06a | `вне-фаз` | 31 | zamechaniya-L1-process-first.md:27; informacia-i-kody/SESSIYA.md:28; l2-skolko-informacii/SESSIYA.md:60; teorkat-programma-dizajn/SESSIYA.md:117-119,441-445,492(a),492(b),594-600,596-600; krivaya-drakona/SESSIYA.md:175; teorkat-motivacia/SESSIYA.md:102-103,334,335,388-389,409-410,410,436,459,656-657,783,855,1110,1216; mat-kostyak/SESSIYA.md:8-10(a),8-10(b),102-106,102-108,466-468; teorkat-landshaft/SESSIYA.md:174; vvedenie-sborka/SESSIYA.md:112; teorkat-programma/SESSIYA.md:35 |
| КРВ-06b | `05-raskadrovka` | 8 | RAZBOR-posle-lekcii-2026-07-27.md:578-579; PRAVKI.md(teorkat-vvedenie):179-184,164; krivaya-drakona/SESSIYA.md:154; konspekt-l1/SESSIYA.md:125; dovodka-l1/SESSIYA.md:194; teksty-l1/SESSIYA.md:16,35 |
| КРВ-06c | `01-brief` | 7 | lekcia-1/SESSIYA.md:235-249,1066-1072; teorkat-motivacia/SESSIYA.md:893; teorkat-l1/SESSIYA.md:21,22,23; l3-kodirovanie/SESSIYA.md:60 |
| КРВ-06d | `04-gibrid-istochnik` | 4 | PRAVKI.md(teorkat-vvedenie):480-482; l2-skolko-informacii/SESSIYA.md:42; teorkat-programma-dizajn/SESSIYA.md:402-406; lekcia-1/SESSIYA.md:1074-1084 |
| КРВ-06e | `02-reserch` | 2 | zamechaniya-statya-mir2.md:78; teorkat-motivacia/SESSIYA.md:883 |
| КРВ-06f | `06-tekst` | 1 | PRAVKI-final.md:142 |
| КРВ-07a | `06-tekst` | 24 | akt-1-razbor.md:88-90; RAZBOR-posle-lekcii-2026-07-27.md:227-228; PRAVKI-final.md:72,90; PRAVKI.md:114-115,229(×3),353,404(×3),426,425,434,435,436,441,718,723; zamechaniya-mosty-kartoteka.md:15; paskal-lekcia-sborka/SESSIYA.md:175-176; dovodka-l1/SESSIYA.md:68,111 |
| КРВ-07b | `02-reserch` | 11 | zamechaniya-mosty-kartoteka.md:11; sborka-konvejera/SESSIYA.md:109; l2-skolko-informacii/SESSIYA.md:83; krivaya-drakona/SESSIYA.md:583; mat-kostyak/SESSIYA.md:78-86,146-150,146-156,476-480,567-569; teorkat-l1/SESSIYA.md:95; vneshnie-istorii/SESSIYA.md:80 |
| КРВ-07c | `05-raskadrovka` | 6 | PRAVKI.md:159,171; lekcia-1/SESSIYA.md:44-47,395-399; dovodka-l1/SESSIYA.md:195,218 |
| КРВ-07d | `04-gibrid-istochnik` | 6 | teorkat-motivacia/SESSIYA.md:353-354,480-481; vvedenie-sborka/SESSIYA.md:13; vneshnie-istorii/SESSIYA.md:80,82; l3-kodirovanie/SESSIYA.md:16 |
| КРВ-07e | `04.5-intervyu` | 2 | mat-kostyak/SESSIYA.md:454-456; teksty-l1/SESSIYA.md:12 |
| КРВ-07f | `03-matbaza` | 1 | catalan/zamechaniya-statya-mir2.md:31 |
| КРВ-07g | `08-sceny` | 1 | PRAVKI.md:236 |
| КРВ-07h | `07-verstka` | 1 | PRAVKI-final.md:67 |
| КРВ-08a | `06-tekst` | 25 | akt-1-razbor.md:144-148,164-168,172-184,188-192,262-268,266-270; RAZBOR-posle-lekcii-2026-07-27.md:40-41,86,117,129; PRAVKI.md:227,322,438,508,510,525,547; fibonacci-kurs/SESSIYA.md:38; reserch-zadach/SESSIYA.md:25; lekcia-1/SESSIYA.md:481-486,608-610; paskal-lekcia-sborka/SESSIYA.md:109-110; vneshnie-istorii/SESSIYA.md:59; teorkat-programma/SESSIYA.md:48; l3-kodirovanie/SESSIYA.md:39 |
| КРВ-08b | `02-reserch` | 5 | l2-skolko-informacii/SESSIYA.md:44; teorkat-motivacia/SESSIYA.md:745-746,858; vneshnie-istorii/SESSIYA.md:32,43 |
| КРВ-08c | `04.5-intervyu` | 4 | teorkat-programma-dizajn/SESSIYA.md:701-707; lekcia-1/SESSIYA.md:251-263; teorkat-motivacia/SESSIYA.md:327; konspekt-l1/SESSIYA.md:46 |
| КРВ-08d | `01-brief` | 3 | teorkat-l1/SESSIYA.md:49; vvedenie-sborka/SESSIYA.md:15,54 |
| КРВ-08e | `04-gibrid-istochnik` | 2 | lekcia-1/SESSIYA.md:450-456,985-991 |
| КРВ-08f | `вне-фаз` | 2 | dovodka-fabriki/SESSIYA.md:447; vvedenie-sborka/SESSIYA.md:49 |
| КРВ-08g | `03-matbaza` | 2 | mat-kostyak/SESSIYA.md:146-152,192-194 |
| КРВ-09a | `06-tekst` | 13 | RAZBOR-posle-lekcii-2026-07-27.md:193-195; PRAVKI-final.md:108,159; PRAVKI.md:137-139,237,238,372,396,411,507(×2); dovodka-fabriki/SESSIYA.md:20; teorkat-landshaft/SESSIYA.md:99 |
| КРВ-09b | `03-matbaza` | 6 | PRAVKI.md:521,550; zamechaniya-statya-mir2.md:80; zamechaniya-mosty-kartoteka.md:3; fibonacci-kurs/SESSIYA.md:56; teorkat-motivacia/SESSIYA.md:298 |
| КРВ-09c | `01-brief` | 6 | teorkat-motivacia/SESSIYA.md:876; teorkat-landshaft/SESSIYA.md:89; teorkat-l1/SESSIYA.md:20,23,52; paskal-lekcia-sborka/SESSIYA.md:80-81 |
| КРВ-09d | `вне-фаз` | 4 | sborka-konvejera/SESSIYA.md:109; krivaya-drakona/SESSIYA.md:484,656; l3-kodirovanie/SESSIYA.md:58 |
| КРВ-09e | `02-reserch` | 3 | lekcia-1/SESSIYA.md:645-655; mat-kostyak/SESSIYA.md:30; teorkat-l1/SESSIYA.md:48 |
| КРВ-09f | `08-sceny` | 3 | PRAVKI-sceny-i-animacii.md:89-90; dovodka-fabriki/SESSIYA.md:60; teksty-l1/SESSIYA.md:66 |
| КРВ-09g | `05-raskadrovka` | 2 | PRAVKI.md:341; teksty-l1/SESSIYA.md:37 |
| КРВ-09h | `04-gibrid-istochnik` | 2 | zamechaniya-L1-process-first.md:19; paskal-lekcia-sborka/SESSIYA.md:200-201 |
| КРВ-09i | `04.5-intervyu` | 2 | teorkat-programma-dizajn/SESSIYA.md:998; konspekt-l1/SESSIYA.md:152 |
| КРВ-09j | `07-verstka` | 1 | fibonacci-kurs/SESSIYA.md:63 |
| КРВ-10a | `02-reserch` | 15 | PRAVKI.md:304; zamechaniya-disciplina-kartochek.md:5; teorkat-programma-dizajn/SESSIYA.md:78-80; lekcia-1/SESSIYA.md:224-233,235-249,500-505; teorkat-motivacia/SESSIYA.md:657,700,806,820,1133; mat-kostyak/SESSIYA.md:12-14; teorkat-landshaft/SESSIYA.md:11; vneshnie-istorii/SESSIYA.md:71; teorkat-programma/SESSIYA.md:52 |
| КРВ-10b | `вне-фаз` | 12 | teorkat-programma-dizajn/SESSIYA.md:1170; lekcia-1/SESSIYA.md:224-233,627-643; teorkat-motivacia/SESSIYA.md:466,1277; dovodka-fabriki/SESSIYA.md:215,276,384; dovodka-l1/SESSIYA.md:197; teorkat-programma/SESSIYA.md:18; l3-kodirovanie/SESSIYA.md:39,41 |
| КРВ-10c | `05-raskadrovka` | 4 | RAZBOR-posle-lekcii-2026-07-27.md:239-240; PRAVKI.md:529; lekcia-1/SESSIYA.md:898-900; dovodka-l1/SESSIYA.md:201 |
| КРВ-10d | `01-brief` | 4 | teorkat-programma-dizajn/SESSIYA.md:413; lekcia-1/SESSIYA.md:251-263; teorkat-motivacia/SESSIYA.md:1221; teorkat-landshaft/SESSIYA.md:15 |
| КРВ-10e | `06-tekst` | 3 | lekcia-1/SESSIYA.md:1074-1084(×2); vneshnie-istorii/SESSIYA.md:26 |
| КРВ-10f | `04.5-intervyu` | 1 | lekcia-1/SESSIYA.md:215-222 |
| КРВ-10g | `07-verstka` | 1 | konspekt-l1/SESSIYA.md:181 |
| КРВ-10h | `09-illustracii` | 1 | paskal-lekcia-sborka/SESSIYA.md:180 |
| КРВ-11a | `06-tekst` | 17 | akt-1-razbor.md:68-72,168-170; RAZBOR-posle-lekcii-2026-07-27.md:82-83; PRAVKI.md:172,233(×2),250-251,252,254-256,264-266,294,313,353,502,542; dovodka-fabriki/SESSIYA.md:60,83 |
| КРВ-11b | `02-reserch` | 8 | zamechaniya-L1-process-first.md:25; zamechaniya-issledovanie-idei.md:1; teorkat-programma-dizajn/SESSIYA.md:507; lekcia-1/SESSIYA.md:401-408,515-518,627-643; mat-kostyak/SESSIYA.md:182-184,567-569 |
| КРВ-11c | `01-brief` | 4 | teorkat-programma-dizajn/SESSIYA.md:964; teorkat-motivacia/SESSIYA.md:185-186; konspekt-l1/SESSIYA.md:33; teksty-l1/SESSIYA.md:14 |
| КРВ-11d | `05-raskadrovka` | 3 | PRAVKI.md:511; dovodka-l1/SESSIYA.md:81,167 |
| КРВ-11e | `07-verstka` | 2 | PRAVKI-final.md:224; krivaya-drakona/SESSIYA.md:717 |
| КРВ-11f | `08-sceny` | 2 | PRAVKI.md:74-75,512 |
| КРВ-11g | `10-sborka-qa` | 1 | PRAVKI-final.md:259 |
| КРВ-11h | `04-gibrid-istochnik` | 1 | teorkat-l1/SESSIYA.md:26 |
| КРВ-11i | `03-matbaza` | 1 | teorkat-programma/SESSIYA.md:40 |
| КРВ-12a | `02-reserch` | 15 | zamechaniya-mosty-kartoteka.md:7; teorkat-programma-dizajn/SESSIYA.md:995-997; lekcia-1/SESSIYA.md:583-588,597-601,1086-1088; teorkat-motivacia/SESSIYA.md:255-256,402,613-614; mat-kostyak/SESSIYA.md:78-80; teorkat-l1/SESSIYA.md:34,55,86,89; vneshnie-istorii/SESSIYA.md:27,40 |
| КРВ-12b | `06-tekst` | 7 | PRAVKI-final.md:197; PRAVKI.md:193-195,230,352,450; lekcia-1/SESSIYA.md:902-908,1017-1023 |
| КРВ-12c | `05-raskadrovka` | 6 | fibonacci-kurs/SESSIYA.md:20; lekcia-1/SESSIYA.md:97-101,328-343,568-575; teorkat-motivacia/SESSIYA.md:31-32; teorkat-l1/SESSIYA.md:89 |
| КРВ-12d | `09-illustracii` | 3 | akt-1-razbor.md:230-236,236-240; RAZBOR-posle-lekcii-2026-07-27.md:433-434 |
| КРВ-12e | `01-brief` | 3 | teorkat-motivacia/SESSIYA.md:256; teorkat-landshaft/SESSIYA.md:99; teorkat-l1/SESSIYA.md:21 |
| КРВ-12f | `03-matbaza` | 2 | l2-skolko-informacii/SESSIYA.md:56; mat-kostyak/SESSIYA.md:78-86 |
| КРВ-12g | `04.5-intervyu` | 1 | lekcia-1/SESSIYA.md:358-364 |
| КРВ-12h | `вне-фаз` | 1 | l3-kodirovanie/SESSIYA.md:34 |
| КРВ-13a | `вне-фаз` | 11 | zamechaniya-disciplina-kartochek.md:7; sborka-konvejera/SESSIYA.md:50,83; fibonacci-kurs/SESSIYA.md:34,60; reserch-zadach/SESSIYA.md:17; teorkat-programma-dizajn/SESSIYA.md:353-357; krivaya-drakona/SESSIYA.md:191; lekcia-1/SESSIYA.md:1056-1064; teorkat-motivacia/SESSIYA.md:876; dovodka-fabriki/SESSIYA.md:400 |
| КРВ-13b | `02-reserch` | 9 | lekcia-1/SESSIYA.md:49-52,298-304,410-418,530-538; mat-kostyak/SESSIYA.md:170-176,273-284,454-456,567-569; teorkat-l1/SESSIYA.md:51 |
| КРВ-13c | `09-illustracii` | 5 | RAZBOR-posle-lekcii-2026-07-27.md:381,555-557; PRAVKI-final.md:75; PRAVKI.md:317,332 |
| КРВ-13d | `04-gibrid-istochnik` | 3 | zamechaniya-statya-mir2.md:21,78; lekcia-1/SESSIYA.md:131-133 |
| КРВ-13e | `01-brief` | 3 | teorkat-motivacia/SESSIYA.md:1219; vneshnie-istorii/SESSIYA.md:25,67 |
| КРВ-13f | `06-tekst` | 2 | PRAVKI.md:228; dovodka-fabriki/SESSIYA.md:54 |
| КРВ-13g | `07-verstka` | 1 | PRAVKI-final.md:80 |
| КРВ-13h | `05-raskadrovka` | 1 | zamechaniya-L1-process-first.md:5 |
| КРВ-13i | `04.5-intervyu` | 1 | teorkat-programma-dizajn/SESSIYA.md:989-993 |
| КРВ-14a | `05-raskadrovka` | 18 | RAZBOR-posle-lekcii:28-29,216-217,352-353; PRAVKI-sceny-i-animacii:100; teorkat-vvedenie/PRAVKI:552; fibonacci-kurs/SESSIYA:20; krivaya-drakona/SESSIYA:173,177,199,219,225,312(×3),524,688(×2); dovodka-l1/SESSIYA:113 |
| КРВ-14b | `09-illustracii` | 7 | RAZBOR-posle-lekcii:63-66,416-417,427-428; teorkat-vvedenie/PRAVKI:234; krivaya-drakona/SESSIYA:253; dovodka-fabriki/SESSIYA:82; dovodka-l1/SESSIYA:188 |
| КРВ-14c | `06-tekst` | 2 | teorkat-vvedenie/PRAVKI:434,503 |
| КРВ-14d | `04-gibrid-istochnik` | 1 | fibonacci-kurs/SESSIYA:29 |
| КРВ-14e | `04.5-intervyu` | 1 | krivaya-drakona/SESSIYA:112 |
| КРВ-14f | `вне-фаз` | 1 | krivaya-drakona/SESSIYA:110 (илл. из статьи, не дека — листок) |
| КРВ-15a | `06-tekst` | 7 | RAZBOR-posle-lekcii:225-226,472; konspekt-l1/PRAVKI-final:198; teorkat-vvedenie/PRAVKI:231,386,528; krivaya-drakona/SESSIYA:294 |
| КРВ-15b | `05-raskadrovka` | 5 | RAZBOR-posle-lekcii:328; konspekt-l1/PRAVKI-final:152; teorkat-vvedenie/PRAVKI:144-145,720; paskal-lekcia-sborka/SESSIYA:123-125 |
| КРВ-15c | `02-reserch` | 4 | catalan/zamechaniya-mosty-kartoteka:23; teorkat-programma-dizajn/SESSIYA:316-324; lekcia-1/SESSIYA:458-470; teorkat-motivacia/SESSIYA:445 |
| КРВ-15d | `03-matbaza` | 4 | catalan/zamechaniya-mosty-kartoteka:3; mat-kostyak/SESSIYA:102-110,102-114; paskal-lekcia-sborka/SESSIYA:179 |
| КРВ-15e | `вне-фаз` | 3 | krivaya-drakona/SESSIYA:110 (ссылка на статью — листок); krivaya-drakona/SESSIYA:484 (подсказка в условии листка); vvedenie-sborka/SESSIYA:55 |
| КРВ-15f | `01-brief` | 2 | teorkat-programma-dizajn/SESSIYA:164; teorkat-l1/SESSIYA:10 |
| КРВ-15g | `04.5-intervyu` | 2 | sborka-konvejera/SESSIYA:85; teorkat-motivacia/SESSIYA:1223 |
| КРВ-15h | `10-sborka-qa` | 1 | fibonacci-kurs/SESSIYA:27 |
| КРВ-16a | `09-illustracii` | 16 | RAZBOR-posle-lekcii-2026-07-27.md:297-299,321-322; PRAVKI-final.md:33,45,55,174,208,253; PRAVKI.md:234,351,527,548,551; krivaya-drakona/SESSIYA.md:294,349; dovodka-fabriki/SESSIYA.md:20 |
| КРВ-16b | `07-verstka` | 4 | PRAVKI-final.md:195,255; l2-skolko-informacii/SESSIYA.md:26; dovodka-fabriki/SESSIYA.md:20 |
| КРВ-16c | `05-raskadrovka` | 2 | RAZBOR-posle-lekcii-2026-07-27.md:211-213; PRAVKI-sceny-i-animacii.md:77-82 |
| КРВ-16d | `08-sceny` | 2 | krivaya-drakona/SESSIYA.md:328,349 |
| КРВ-16e | `06-tekst` | 2 | mat-kostyak/SESSIYA.md:499-501; l3-kodirovanie/SESSIYA.md:52 |
| КРВ-16f | `10-sborka-qa` | 1 | dovodka-fabriki/SESSIYA.md:30 |
| КРВ-17a | `02-reserch` | 14 | l2-skolko-informacii/SESSIYA.md:90; teorkat-programma-dizajn/SESSIYA.md:289-291,1060-1063; lekcia-1/SESSIYA.md:235-249,458-470; teorkat-motivacia/SESSIYA.md:291,398,626-627,790,805-806; mat-kostyak/SESSIYA.md:119-121(×2),567-569; vneshnie-istorii/SESSIYA.md:25 |
| КРВ-17b | `01-brief` | 4 | teorkat-programma-dizajn/SESSIYA.md:966-973; teorkat-motivacia/SESSIYA.md:203,410; teorkat-l1/SESSIYA.md:34 |
| КРВ-17c | `04-gibrid-istochnik` | 3 | teorkat-vvedenie/PRAVKI.md:717; catalan/zamechaniya-statya-mir2.md:51; teorkat-motivacia/SESSIYA.md:373-374 |
| КРВ-17d | `05-raskadrovka` | 2 | teorkat-motivacia/SESSIYA.md:116-117; dovodka-l1/SESSIYA.md:201 |
| КРВ-17e | `06-tekst` | 1 | RAZBOR-posle-lekcii-2026-07-27.md:234 |
| КРВ-17f | `09-illustracii` | 1 | RAZBOR-posle-lekcii-2026-07-27.md:424-425 |
| КРВ-17g | `10-sborka-qa` | 1 | teorkat-vvedenie/PRAVKI.md:625-626 |
| КРВ-17h | `04.5-intervyu` | 1 | teorkat-l1/SESSIYA.md:25 |
| КРВ-18a | `08-sceny` | 12 | akt-1-razbor.md:208-216,216-228; PRAVKI-final.md:41,110,157,172,272; teorkat-vvedenie/PRAVKI.md:236,412; dovodka-fabriki/SESSIYA.md:5; konspekt-l1/SESSIYA.md:156; paskal-lekcia-sborka/SESSIYA.md:118-119 |
| КРВ-18b | `05-raskadrovka` | 7 | PRAVKI-sceny-i-animacii.md:56-57; teorkat-vvedenie/PRAVKI.md:53-54,226,433; lekcia-1/SESSIYA.md:1066-1072; konspekt-l1/SESSIYA.md:41; paskal-lekcia-sborka/SESSIYA.md:117 |
| КРВ-18c | `02-reserch` | 2 | lekcia-1/SESSIYA.md:215-222,1056-1064 |
| КРВ-18d | `06-tekst` | 2 | mat-kostyak/SESSIYA.md:27; teksty-l1/SESSIYA.md:45 |
| КРВ-18e | `07-verstka` | 1 | RAZBOR-posle-lekcii-2026-07-27.md:109-110 |
| КРВ-18f | `01-brief` | 1 | paskal-lekcia-sborka/SESSIYA.md:68-72 |
| КРВ-18g | `вне-фаз` | 1 | vvedenie-sborka/SESSIYA.md:57 |
| КРВ-19a | `05-raskadrovka` | 8 | PRAVKI-sceny-i-animacii.md:21; teorkat-vvedenie/PRAVKI.md:170; lekcia-1/SESSIYA.md:902-908; dovodka-l1/SESSIYA.md:70,71,90,96; teksty-l1/SESSIYA.md:65 |
| КРВ-19b | `09-illustracii` | 5 | teorkat-vvedenie/PRAVKI.md:239,544; krivaya-drakona/SESSIYA.md:137,294,312 |
| КРВ-19c | `06-tekst` | 3 | RAZBOR-posle-lekcii-2026-07-27.md:49; teorkat-programma-dizajn/SESSIYA.md:30-32; teorkat-motivacia/SESSIYA.md:163-164 |
| КРВ-19d | `07-verstka` | 2 | teorkat-vvedenie/PRAVKI.md:314,501 |
| КРВ-19e | `02-reserch` | 2 | krivaya-drakona/SESSIYA.md:160; mat-kostyak/SESSIYA.md:78-82 |
| КРВ-19f | `01-brief` | 2 | krivaya-drakona/SESSIYA.md:185; mat-kostyak/SESSIYA.md:25 |
| КРВ-19g | `вне-фаз` | 2 | teorkat-motivacia/SESSIYA.md:824; dovodka-fabriki/SESSIYA.md:103 |
| КРВ-19h | `08-sceny` | 1 | RAZBOR-posle-lekcii-2026-07-27.md:67-68 |
| КРВ-19i | `04-gibrid-istochnik` | 1 | lekcia-1/SESSIYA.md:79-81 |
| КРВ-20a | `06-tekst` | 12 | akt-1-razbor.md:196-202; PRAVKI-final.md:57,133; teorkat-vvedenie/PRAVKI.md:316,342,406,408,409,519,520; lekcia-1/SESSIYA.md:458-470; mat-kostyak/SESSIYA.md:90-92 |
| КРВ-20b | `02-reserch` | 5 | catalan/zamechaniya-L1-process-first.md:23; krivaya-drakona/SESSIYA.md:174,388,612; teorkat-programma/SESSIYA.md:66 |
| КРВ-20c | `05-raskadrovka` | 3 | RAZBOR-posle-lekcii-2026-07-27.md:404; teksty-l1/SESSIYA.md:29; l3-kodirovanie/SESSIYA.md:39 |
| КРВ-20d | `01-brief` | 2 | teorkat-programma-dizajn/SESSIYA.md:999; lekcia-1/SESSIYA.md:159-164 |
| КРВ-20e | `вне-фаз` | 2 | mat-kostyak/SESSIYA.md:244-246; paskal-lekcia-sborka/SESSIYA.md:104 |
| КРВ-21a | `06-tekst` | 10 | RAZBOR-posle-lekcii-2026-07-27.md:56,118,254-255,261,385-386,383-384,441; krivaya-drakona/SESSIYA.md:484; teorkat-motivacia/SESSIYA.md:429; paskal-lekcia-sborka/SESSIYA.md:164-166 |
| КРВ-21b | `05-raskadrovka` | 6 | RAZBOR-posle-lekcii-2026-07-27.md:21-23,168,235-238,387-388,390; paskal-lekcia-sborka/SESSIYA.md:162-164 |
| КРВ-21c | `03-matbaza` | 2 | catalan/zamechaniya-statya-mir2.md:11,76 |
| КРВ-21d | `04-gibrid-istochnik` | 2 | catalan/zamechaniya-statya-mir2.md:82; teorkat-motivacia/SESSIYA.md:939 |
| КРВ-21e | `02-reserch` | 1 | catalan/zamechaniya-L1-process-first.md:3 |
| КРВ-21f | `07-verstka` | 1 | fibonacci-kurs/SESSIYA.md:51 |
| КРВ-21g | `04.5-intervyu` | 1 | lekcia-1/SESSIYA.md:381-383 |
| КРВ-21h | `01-brief` | 1 | teorkat-motivacia/SESSIYA.md:259-260 |
| КРВ-22a | `02-reserch` | 11 | catalan/zamechaniya-statya-mir2.md:82; informacia-i-kody/SESSIYA.md:54; teorkat-programma-dizajn/SESSIYA.md:496-505,612,987; lekcia-1/SESSIYA.md:888-896; teorkat-motivacia/SESSIYA.md:1157; mat-kostyak/SESSIYA.md:78-84; paskal-lekcia-sborka/SESSIYA.md:24-26; vneshnie-istorii/SESSIYA.md:26,68 |
| КРВ-22b | `01-brief` | 4 | teorkat-motivacia/SESSIYA.md:1261,1262; teorkat-landshaft/SESSIYA.md:101; dovodka-l1/SESSIYA.md:195 |
| КРВ-22c | `10-sborka-qa` | 3 | teorkat-vvedenie/PRAVKI.md:500; teorkat-programma-dizajn/SESSIYA.md:415; teorkat-l1/SESSIYA.md:54 |
| КРВ-22d | `вне-фаз` | 3 | dovodka-fabriki/SESSIYA.md:24,34-36; vneshnie-istorii/SESSIYA.md:32 |
| КРВ-22e | `09-illustracii` | 1 | teorkat-vvedenie/PRAVKI.md:320 |
| КРВ-22f | `03-matbaza` | 1 | geometria-6-nagliadnaya/SESSIYA.md:23 |
| КРВ-22g | `08-sceny` | 1 | paskal-lekcia-sborka/SESSIYA.md:107-108 |
| КРВ-23a | `09-illustracii` | 13 | akt-1-razbor.md:244-248,246-248,250; RAZBOR-posle-lekcii-2026-07-27.md:47-48,130; PRAVKI-final.md:120; teorkat-vvedenie/PRAVKI.md:235(закон),235(искл),331; fibonacci-kurs/SESSIYA.md:29,40; l2-skolko-informacii/SESSIYA.md:61; krivaya-drakona/SESSIYA.md:296 |
| КРВ-23b | `06-tekst` | 4 | teorkat-vvedenie/PRAVKI.md:232; fibonacci-kurs/SESSIYA.md:37; paskal-lekcia-sborka/SESSIYA.md:115-116; teksty-l1/SESSIYA.md:80 |
| КРВ-23c | `07-verstka` | 2 | fibonacci-kurs/SESSIYA.md:20; krivaya-drakona/SESSIYA.md:294 |
| КРВ-23d | `вне-фаз` | 2 | l3-kodirovanie/SESSIYA.md:34,50 |
| КРВ-23e | `01-brief` | 1 | teorkat-motivacia/SESSIYA.md:691 |
| КРВ-24a | `вне-фаз` | 7 | krivaya-drakona/SESSIYA.md:412,500,688; lekcia-1/SESSIYA.md:1096-1100; dovodka-fabriki/SESSIYA.md:153,448; vneshnie-istorii/SESSIYA.md:10 |
| КРВ-24b | `04-gibrid-istochnik` | 4 | catalan/zamechaniya-L1-process-first.md:27; lekcia-1/SESSIYA.md:910-914; teorkat-motivacia/SESSIYA.md:525; teorkat-l1/SESSIYA.md:89 |
| КРВ-24c | `05-raskadrovka` | 3 | RAZBOR-posle-lekcii-2026-07-27.md:287-288; teorkat-vvedenie/PRAVKI.md:458,554 |
| КРВ-24d | `01-brief` | 3 | geometria-6-nagliadnaya/SESSIYA.md:22; l2-skolko-informacii/SESSIYA.md:32; teorkat-programma-dizajn/SESSIYA.md:443-445 |
| КРВ-24e | `06-tekst` | 2 | RAZBOR-posle-lekcii-2026-07-27.md:35-36; teorkat-vvedenie/PRAVKI.md:307 |
| КРВ-24f | `02-reserch` | 2 | catalan/zamechaniya-mosty-kartoteka.md:7; l2-skolko-informacii/SESSIYA.md:46 |
| КРВ-24g | `08-sceny` | 1 | PRAVKI-final.md:253 |
| КРВ-25a | `02-reserch` | 16 | RAZBOR-posle-lekcii-2026-07-27.md:244; catalan/zamechaniya-mosty-kartoteka.md:3,7; catalan/zamechaniya-issledovanie-idei.md:15; catalan/zamechaniya-disciplina-kartochek.md:3; reserch-zadach/SESSIYA.md:18,27; l2-skolko-informacii/SESSIYA.md:83,119; lekcia-1/SESSIYA.md:205-213,345-356,993-999; teorkat-motivacia/SESSIYA.md:524-525; mat-kostyak/SESSIYA.md:102-112; teorkat-l1/SESSIYA.md:25; vneshnie-istorii/SESSIYA.md:40 |
| КРВ-25b | `06-tekst` | 2 | RAZBOR-posle-lekcii-2026-07-27.md:177-180; sborka-konvejera/SESSIYA.md:101 |
| КРВ-25c | `04-gibrid-istochnik` | 2 | lekcia-1/SESSIYA.md:888-896; paskal-lekcia-sborka/SESSIYA.md:49-54 |
| КРВ-25d | `вне-фаз` | 1 | lekcia-1/SESSIYA.md:838-844 |
| КРВ-25e | `04.5-intervyu` | 1 | teorkat-motivacia/SESSIYA.md:221-222 |
| КРВ-26a | `06-tekst` | 15 | akt-1-razbor.md:62-64; PRAVKI-final.md:42; teorkat-vvedenie/PRAVKI.md:175,228,230(осмысление),230(манифест),354,379,410,448,460,530,722; sborka-konvejera/SESSIYA.md:78; dovodka-l1/SESSIYA.md:206 |
| КРВ-26b | `04-gibrid-istochnik` | 3 | lekcia-1/SESSIYA.md:374-379; teorkat-motivacia/SESSIYA.md:105; mat-kostyak/SESSIYA.md:258-271 |
| КРВ-26c | `вне-фаз` | 2 | mat-kostyak/SESSIYA.md:324-326; l3-kodirovanie/SESSIYA.md:55 |
| КРВ-26d | `05-raskadrovka` | 1 | teorkat-vvedenie/PRAVKI.md:474-475 |
| КРВ-27a | `06-tekst` | 9 | akt-1-razbor.md:58-62,124-134; PRAVKI-final.md:20,166; teorkat-vvedenie/PRAVKI.md:121-123,123,232,440; vvedenie-sborka/SESSIYA.md:112 |
| КРВ-27b | `01-brief` | 3 | l2-skolko-informacii/SESSIYA.md:28; krivaya-drakona/SESSIYA.md:16; dovodka-l1/SESSIYA.md:40 |
| КРВ-27c | `вне-фаз` | 3 | krivaya-drakona/SESSIYA.md:45,108; mat-kostyak/SESSIYA.md:102-104 |
| КРВ-27d | `02-reserch` | 2 | teorkat-motivacia/SESSIYA.md:749,1022-1023 |
| КРВ-27e | `05-raskadrovka` | 1 | PRAVKI-final.md:178 |
| КРВ-27f | `04-gibrid-istochnik` | 1 | teorkat-motivacia/SESSIYA.md:1013 |
| КРВ-27g | `07-verstka` | 1 | dovodka-fabriki/SESSIYA.md:28 |
| КРВ-28a | `08-sceny` | 11 | RAZBOR-posle-lekcii-2026-07-27.md:93,151-154,446-447,561; PRAVKI-sceny-i-animacii.md:68,80-81; teorkat-vvedenie/PRAVKI.md:236,449; fibonacci-kurs/SESSIYA.md:42; krivaya-drakona/SESSIYA.md:328(a),328(b) |
| КРВ-28b | `01-brief` | 2 | catalan/zamechaniya-L1-process-first.md:15; krivaya-drakona/SESSIYA.md:386 |
| КРВ-28c | `04-gibrid-istochnik` | 2 | lekcia-1/SESSIYA.md:590-595; teorkat-motivacia/SESSIYA.md:927 |
| КРВ-28d | `03-matbaza` | 1 | teorkat-motivacia/SESSIYA.md:605-606 |
| КРВ-28e | `05-raskadrovka` | 1 | konspekt-l1/SESSIYA.md:113 |
| КРВ-28f | `02-reserch` | 1 | teorkat-l1/SESSIYA.md:38 |
| КРВ-28g | `06-tekst` | 1 | teksty-l1/SESSIYA.md:45 |
| КРВ-29a | `06-tekst` | 14 | akt-1-razbor.md:106-108; PRAVKI-final.md:43,114-116,132,280; teorkat-vvedenie/PRAVKI.md:231(не объяснять),231(абзац),297,302,324,420,437,492; fibonacci-kurs/SESSIYA.md:43 |
| КРВ-29b | `01-brief` | 2 | lekcia-1/SESSIYA.md:35-38; paskal-lekcia-sborka/SESSIYA.md:111-112 |
| КРВ-29c | `09-illustracii` | 1 | teorkat-vvedenie/PRAVKI.md:549 |
| КРВ-29d | `вне-фаз` | 1 | informacia-i-kody/SESSIYA.md:58 |
| КРВ-30a | `01-brief` | 7 | geometria-6-nagliadnaya/SESSIYA.md:21; krivaya-drakona/SESSIYA.md:522,585; teorkat-motivacia/SESSIYA.md:336; teorkat-landshaft/SESSIYA.md:89; vvedenie-sborka/SESSIYA.md:52; osnovanie-vvedenie/SESSIYA.md:23 |
| КРВ-30b | `02-reserch` | 4 | lekcia-1/SESSIYA.md:617-623; teorkat-motivacia/SESSIYA.md:305,633-634; vneshnie-istorii/SESSIYA.md:40 |
| КРВ-30c | `06-tekst` | 3 | RAZBOR-posle-lekcii-2026-07-27.md:42-44; teorkat-vvedenie/PRAVKI.md:371; mat-kostyak/SESSIYA.md:567-569 |
| КРВ-30d | `05-raskadrovka` | 2 | l2-skolko-informacii/SESSIYA.md:14; dovodka-l1/SESSIYA.md:60 |
| КРВ-30e | `вне-фаз` | 2 | teorkat-programma-dizajn/SESSIYA.md:1001-1005,1056 |
| КРВ-31a | `вне-фаз` | 4 | sborka-konvejera/SESSIYA.md:96; fibonacci-kurs/SESSIYA.md:56; krivaya-drakona/SESSIYA.md:294; mat-kostyak/SESSIYA.md:273-275 |
| КРВ-31b | `04.5-intervyu` | 3 | catalan/zamechaniya-mosty-kartoteka.md:19; krivaya-drakona/SESSIYA.md:590; lekcia-1/SESSIYA.md:395-399 |
| КРВ-31c | `04-gibrid-istochnik` | 3 | lekcia-1/SESSIYA.md:657-661; teorkat-motivacia/SESSIYA.md:390; vvedenie-sborka/SESSIYA.md:112 |
| КРВ-31d | `10-sborka-qa` | 2 | sborka-konvejera/SESSIYA.md:73; krivaya-drakona/SESSIYA.md:464 |
| КРВ-31e | `02-reserch` | 2 | teorkat-programma-dizajn/SESSIYA.md:624-628; vvedenie-sborka/SESSIYA.md:70 |
| КРВ-31f | `09-illustracii` | 1 | RAZBOR-posle-lekcii-2026-07-27.md:102-106 |
| КРВ-31g | `05-raskadrovka` | 1 | teorkat-vvedenie/PRAVKI.md:484-485 |
| КРВ-31h | `07-verstka` | 1 | krivaya-drakona/SESSIYA.md:270 |
| КРВ-31i | `03-matbaza` | 1 | krivaya-drakona/SESSIYA.md:563 |
| КРВ-32a | `06-tekst` | 10 | RAZBOR-posle-lekcii-2026-07-27.md:309-315,334-335,438-439; teorkat-vvedenie/PRAVKI.md:491,553; catalan/zamechaniya-statya-mir2.md:41(a); teorkat-programma-dizajn/SESSIYA.md:10-14; teorkat-motivacia/SESSIYA.md:89,429,833 |
| КРВ-32b | `03-matbaza` | 3 | teorkat-vvedenie/PRAVKI.md:504; catalan/zamechaniya-statya-mir2.md:41(b),82 |
| КРВ-32c | `вне-фаз` | 2 | krivaya-drakona/SESSIYA.md:612,638 |
| КРВ-32d | `04-gibrid-istochnik` | 2 | dovodka-l1/SESSIYA.md:43; teorkat-programma/SESSIYA.md:42 |
| КРВ-32e | `02-reserch` | 1 | catalan/zamechaniya-issledovanie-idei.md:9 |
| КРВ-33a | `07-verstka` | 3 | teorkat-vvedenie/PRAVKI.md:248-250; fibonacci-kurs/SESSIYA.md:54; dovodka-fabriki/SESSIYA.md:52 |
| КРВ-33b | `02-reserch` | 3 | reserch-zadach/SESSIYA.md:16; lekcia-1/SESSIYA.md:215-222; osnovanie-vvedenie/SESSIYA.md:9 |
| КРВ-33c | `06-tekst` | 2 | akt-1-razbor.md:94-96; teorkat-vvedenie/PRAVKI.md:303 |
| КРВ-33d | `09-illustracii` | 2 | akt-1-razbor.md:240-242; dovodka-l1/SESSIYA.md:120 |
| КРВ-33e | `05-raskadrovka` | 2 | fibonacci-kurs/SESSIYA.md:34; paskal-lekcia-sborka/SESSIYA.md:127 |
| КРВ-33f | `04-gibrid-istochnik` | 1 | l2-skolko-informacii/SESSIYA.md:41 |
| КРВ-33g | `04.5-intervyu` | 1 | teorkat-programma-dizajn/SESSIYA.md:945-947 |
| КРВ-33h | `08-sceny` | 1 | krivaya-drakona/SESSIYA.md:294 |
| КРВ-33i | `вне-фаз` | 1 | l3-kodirovanie/SESSIYA.md:34 |
| КРВ-34a | `08-sceny` | 5 | RAZBOR-posle-lekcii-2026-07-27.md:419-420; PRAVKI-final.md:104; teorkat-vvedenie/PRAVKI.md:492,524; krivaya-drakona/SESSIYA.md:676 |
| КРВ-34b | `04-gibrid-istochnik` | 3 | catalan/zamechaniya-L1-process-first.md:7; lekcia-1/SESSIYA.md:663-672,1001-1005 |
| КРВ-34c | `02-reserch` | 3 | teorkat-programma-dizajn/SESSIYA.md:610-612; mat-kostyak/SESSIYA.md:12-14,182-186 |
| КРВ-34d | `05-raskadrovka` | 2 | teorkat-motivacia/SESSIYA.md:935,934 |
| КРВ-34e | `вне-фаз` | 1 | teorkat-motivacia/SESSIYA.md:1131 |
| КРВ-34f | `06-tekst` | 1 | paskal-lekcia-sborka/SESSIYA.md:113-114 |
| КРВ-34g | `01-brief` | 1 | dovodka-l1/SESSIYA.md:122 |
| КРВ-35a | `вне-фаз` | 12 | fibonacci-kurs/SESSIYA.md:22; geometria-6-nagliadnaya/SESSIYA.md:20,22,25; l2-skolko-informacii/SESSIYA.md:13,28,37; krivaya-drakona/SESSIYA.md:610; teorkat-motivacia/SESSIYA.md:643,1161; teorkat-l1/SESSIYA.md:49; osnovanie-vvedenie/SESSIYA.md:34 |
| КРВ-35b | `02-reserch` | 2 | teorkat-programma-dizajn/SESSIYA.md:1007-1013; mat-kostyak/SESSIYA.md:158-168 |
| КРВ-35c | `01-brief` | 1 | l3-kodirovanie/SESSIYA.md:58 |
| КРВ-36a | `06-tekst` | 9 | RAZBOR-posle-lekcii-2026-07-27.md:121-124,198,265,280,301-302,326-327,448-449,453-454,466 |
| КРВ-36b | `04.5-intervyu` | 1 | akt-1-razbor.md:140-142 |
| КРВ-36c | `09-illustracii` | 1 | teorkat-vvedenie/PRAVKI.md:509 |
| КРВ-36d | `01-brief` | 1 | sborka-konvejera/SESSIYA.md:82 |
| КРВ-36e | `02-reserch` | 1 | krivaya-drakona/SESSIYA.md:45 |
| КРВ-37a | `вне-фаз` | 6 | akt-1-razbor.md:44-46; PRAVKI-final.md:164; teorkat-motivacia/SESSIYA.md:322,855; dovodka-fabriki/SESSIYA.md:18-22,400 |
| КРВ-37b | `02-reserch` | 3 | catalan/zamechaniya-issledovanie-idei.md:13; teorkat-motivacia/SESSIYA.md:758,1171 |
| КРВ-37c | `01-brief` | 2 | teorkat-motivacia/SESSIYA.md:411,439 |
| КРВ-37d | `04-gibrid-istochnik` | 1 | teorkat-motivacia/SESSIYA.md:507 |
| КРВ-38a | `09-illustracii` | 7 | akt-1-razbor.md:252-254; RAZBOR-posle-lekcii-2026-07-27.md:158; krivaya-drakona/SESSIYA.md:185,312(1),563(1),563(2),688 |
| КРВ-38b | `07-verstka` | 3 | RAZBOR-posle-lekcii-2026-07-27.md:128; fibonacci-kurs/SESSIYA.md:38; mat-kostyak/SESSIYA.md:567-569 |
| КРВ-38c | `08-sceny` | 2 | mat-kostyak/SESSIYA.md:499-501; konspekt-l1/SESSIYA.md:31 |
| КРВ-39a | `06-tekst` | 4 | RAZBOR-posle-lekcii-2026-07-27.md:37-39,323-325,513-515; dovodka-l1/SESSIYA.md:176 |
| КРВ-39b | `вне-фаз` | 3 | catalan/zamechaniya-statya-mir2.md:21; teorkat-motivacia/SESSIYA.md:879; teorkat-programma/SESSIYA.md:56 |
| КРВ-39c | `02-reserch` | 2 | teorkat-motivacia/SESSIYA.md:159,961 |
| КРВ-39d | `03-matbaza` | 1 | RAZBOR-posle-lekcii-2026-07-27.md:233 |
| КРВ-39e | `04.5-intervyu` | 1 | lekcia-1/SESSIYA.md:97-101 |
| КРВ-39f | `05-raskadrovka` | 1 | teksty-l1/SESSIYA.md:27 |
| КРВ-40 | `09-illustracii` | 12 | RAZBOR-posle-lekcii-2026-07-27.md:480; PRAVKI-final.md:35,51; PRAVKI-sceny-i-animacii.md:98; teorkat-vvedenie/PRAVKI.md:334,427,545; krivaya-drakona/SESSIYA.md:254,312(2),563(3),563(4); paskal-lekcia-sborka/SESSIYA.md:169-172 |
| КРВ-41a | `10-sborka-qa` | 3 | PRAVKI-final.md:95,124,214 |
| КРВ-41b | `04-gibrid-istochnik` | 3 | catalan/zamechaniya-statya-mir2.md:11,41,76 |
| КРВ-41c | `07-verstka` | 2 | RAZBOR-posle-lekcii-2026-07-27.md:160-161; PRAVKI-final.md:100 |
| КРВ-41d | `05-raskadrovka` | 1 | akt-1-razbor.md:50-54 |
| КРВ-41e | `04.5-intervyu` | 1 | teorkat-vvedenie/PRAVKI.md:615-617 |
| КРВ-41f | `02-reserch` | 1 | teorkat-motivacia/SESSIYA.md:956 |
| КРВ-42a | `04.5-intervyu` | 7 | RAZBOR-posle-lekcii-2026-07-27.md:14-17,395; teorkat-vvedenie/PRAVKI.md:46-48; lekcia-1/SESSIYA.md:35-38,975-977; dovodka-fabriki/SESSIYA.md:409; konspekt-l1/SESSIYA.md:21 |
| КРВ-42b | `05-raskadrovka` | 2 | dovodka-l1/SESSIYA.md:78,115 |
| КРВ-42c | `06-tekst` | 1 | teorkat-vvedenie/PRAVKI.md:194-195 |
| КРВ-42d | `07-verstka` | 1 | teorkat-vvedenie/PRAVKI.md:273-275 |
| КРВ-43a | `вне-фаз` | 10 | teorkat-vvedenie/PRAVKI.md:700-701,725; sborka-konvejera/SESSIYA.md:110; fibonacci-kurs/SESSIYA.md:20,67; teorkat-programma-dizajn/SESSIYA.md:492; lekcia-1/SESSIYA.md:439-444; dovodka-fabriki/SESSIYA.md:42,147; l3-kodirovanie/SESSIYA.md:18 |
| КРВ-43b | `02-reserch` | 1 | teorkat-motivacia/SESSIYA.md:454-455 |
| КРВ-44a | `06-tekst` | 6 | akt-1-razbor.md:134-138,254-260,260-262; teorkat-vvedenie/PRAVKI.md:228,321,413 |
| КРВ-44b | `02-reserch` | 3 | l2-skolko-informacii/SESSIYA.md:46; lekcia-1/SESSIYA.md:450-456,458-470 |
| КРВ-44c | `08-sceny` | 1 | teorkat-vvedenie/PRAVKI.md:715 |
| КРВ-45a | `03-matbaza` | 6 | RAZBOR-posle-lekcii-2026-07-27.md:163-164; catalan/zamechaniya-statya-mir2.md:21(§6),78; informacia-i-kody/SESSIYA.md:28; teorkat-programma-dizajn/SESSIYA.md:1586; teksty-l1/SESSIYA.md:49 |
| КРВ-45b | `04.5-intervyu` | 2 | catalan/zamechaniya-issledovanie-idei.md:3,5 |
| КРВ-45c | `06-tekst` | 1 | teorkat-vvedenie/PRAVKI.md:355 |
| КРВ-45d | `02-reserch` | 1 | teorkat-motivacia/SESSIYA.md:1174 |
| КРВ-46a | `06-tekst` | 4 | akt-1-razbor.md:152-154; RAZBOR-posle-lekcii-2026-07-27.md:537-539; paskal-lekcia-sborka/SESSIYA.md:147-150; teorkat-programma/SESSIYA.md:41 |
| КРВ-46b | `02-reserch` | 3 | catalan/zamechaniya-mosty-kartoteka.md:15; lekcia-1/SESSIYA.md:251-263; l3-kodirovanie/SESSIYA.md:52 |
| КРВ-46c | `04-gibrid-istochnik` | 1 | catalan/zamechaniya-statya-mir2.md:82 |
| КРВ-46d | `01-brief` | 1 | teorkat-l1/SESSIYA.md:20 |
| КРВ-47a | `06-tekst` | 6 | teorkat-vvedenie/PRAVKI.md:111-112,229,407,549; dovodka-fabriki/SESSIYA.md:20; teorkat-l1/SESSIYA.md:23 |
| КРВ-47b | `07-verstka` | 3 | teorkat-vvedenie/PRAVKI.md:131-132,240; krivaya-drakona/SESSIYA.md:294 |
| КРВ-48a | `вне-фаз` | 5 | RAZBOR-posle-lekcii-2026-07-27.md:411-412; sborka-konvejera/SESSIYA.md:27,119; teorkat-motivacia/SESSIYA.md:858; mat-kostyak/SESSIYA.md:523-525 |
| КРВ-48b | `02-reserch` | 2 | l2-skolko-informacii/SESSIYA.md:83; vvedenie-sborka/SESSIYA.md:53 |
| КРВ-48c | `05-raskadrovka` | 1 | lekcia-1/SESSIYA.md:692-695 |
| КРВ-49a | `06-tekst` | 4 | RAZBOR-posle-lekcii-2026-07-27.md:148-149,397; PRAVKI-sceny-i-animacii.md:93; teorkat-vvedenie/PRAVKI.md:442 |
| КРВ-49b | `05-raskadrovka` | 1 | RAZBOR-posle-lekcii-2026-07-27.md:267-268 |
| КРВ-49c | `03-matbaza` | 1 | teorkat-programma-dizajn/SESSIYA.md:602-608 |
| КРВ-50a | `06-tekst` | 2 | RAZBOR-posle-lekcii-2026-07-27.md:507-509,545-546 |
| КРВ-50b | `04.5-intervyu` | 2 | PRAVKI-final.md:13; dovodka-l1/SESSIYA.md:77 |
| КРВ-50c | `вне-фаз` | 1 | sborka-konvejera/SESSIYA.md:73 |
| КРВ-50d | `01-brief` | 1 | krivaya-drakona/SESSIYA.md:80 |
| КРВ-51a | `04.5-intervyu` | 5 | catalan/zamechaniya-mosty-kartoteka.md:25; sborka-konvejera/SESSIYA.md:36; teorkat-motivacia/SESSIYA.md:472,839,1148 |
| КРВ-51b | `02-reserch` | 1 | mat-kostyak/SESSIYA.md:258-267 |
| КРВ-52a | `вне-фаз` | 3 | lekcia-1/SESSIYA.md:507-513; teorkat-motivacia/SESSIYA.md:1020; teorkat-l1/SESSIYA.md:107 |
| КРВ-52b | `02-reserch` | 2 | catalan/zamechaniya-mosty-kartoteka.md:13; vvedenie-sborka/SESSIYA.md:113 |
| КРВ-53 | `вне-фаз` | 5 | teorkat-motivacia/SESSIYA.md:91-92,94,169,202; paskal-lekcia-sborka/SESSIYA.md:93-95 |
| КРВ-54a | `вне-фаз` | 2 | lekcia-1/SESSIYA.md:855-857; konspekt-l1/SESSIYA.md:57 |
| КРВ-54b | `09-illustracii` | 1 | RAZBOR-posle-lekcii-2026-07-27.md:205 |
| КРВ-54c | `02-reserch` | 1 | mat-kostyak/SESSIYA.md:119-129 |
| КРВ-55 | `09-illustracii` | 2 | PRAVKI-final.md:62,148 |
| КРВ-56a | `вне-фаз` | 1 | sborka-konvejera/SESSIYA.md:45 |
| КРВ-56b | `04.5-intervyu` | 1 | lekcia-1/SESSIYA.md:410-418 |

**Сверка охвата Раздела 2:** Σ кратностей = 1379 = заявленному корпусу `KRATNOST-vladelca.md`. Пересчёт: `python3 _data_razdel2.py` в этой папке.

**Итог по фазам (Раздел 2):** 06-tekst 260 · 02-reserch 214 · вне-фаз 208 · 05-raskadrovka 162 · 01-brief 112 · 04-gibrid-istochnik 98 · 09-illustracii 88 · 04.5-intervyu 70 · 08-sceny 64 · 07-verstka 55 · 03-matbaza 35 · 10-sborka-qa 13.

## Раздел 3 · корпус «уроки арок», класс И — переехало в фазу 4.5 (`POKRYTIE.md`)

> Источник: `_studio/konvejer/04.5-intervyu/POKRYTIE.md`, пересчёт 2026-08-05 по 316 урокам 29 арок журнала. **Класс И в этой картотеке закреплён ИСКЛЮЧИТЕЛЬНО за этими 74 записями** (метод — см. шапку файла) — это то самое разбиение, из-за которого критерий №2 (`grep -c` класса И в картотеке == строкам класса И в `POKRYTIE.md`) проверяем «в лоб», а не подгонкой. Per ЧАСТЬ Б захода: всё это уже официально переехало в фазу 4.5 — здесь не копия содержания, а адресный указатель + текущий рычаг из `POKRYTIE.md`.

> **Колонка ФАЗА (часть B этого захода, добавлено 2026-08-05): все 74 строки = `04.5-intervyu` без исключения** — это определение класса И (метод раздела: «И — лечится интервью с владельцем»), не отдельная классификация; разрезать по подгруппам нечего, весь раздел уже гомогенен по фазе по построению. Проверено: 0 записей этого раздела топически относятся к другой фазе (иначе класс И был бы присвоен неверно ещё прошлым заходом — граница уже пройдена в `POKRYTIE.md`).

| id | класс | фаза | подкласс | симптом одной строкой | цена | статус | рычаг (из `POKRYTIE.md`) |
|---|---|---|---|---|---|---|---|
| И-01 | И | `04.5-intervyu` | механика разговора | Правки диктовались номерами слайдов, номера двигались | из 20 сделано 7, из 8 — 4 | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА J6 |
| И-02 | И | `04.5-intervyu` | механика разговора | Приоритет правок сортировали по тяжести, не по цене | владелец за минуты до эфира увидел невыполненными дешёвые правки | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА J7 |
| И-03 | И | `04.5-intervyu` | механика разговора | Пересказ владельца своими словами — три ошибки за один ход | три ошибки, все поймал владелец | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА H2 → см. правку статуса ниже (ГЕЙТ G16.7, вакуумно на живом примере) |
| И-04 | И | `04.5-intervyu` | механика разговора | Претензия записана без ограничителя → обратное действие | снятие цифр 2 и 1, которые велено оставить | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА J15 |
| И-05 | И | `04.5-intervyu` | механика разговора | Непросуженная ставка вынесена как настоящая развилка | 81 минута из 186 — фикцией сутки | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА H1 |
| И-06 | И | `04.5-intervyu` | механика разговора | Рабочая записка отдана как спецификация | 4 дефекта доехали в ленту при зелёных гейтах | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА H5 |
| И-07 | И | `04.5-intervyu` | механика разговора | Диагноз по своему артефакту, не по живым файлам, дважды | урок фабрике записан неверно | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА J4 |
| И-08 | И | `04.5-intervyu` | механика разговора | Шапка итеративного документа дрейфует и врёт телу | документ выдан входом захода | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | ЗАКОН DOK.md «шапка врёт телу» |
| И-09 | И | `04.5-intervyu` | механика разговора | Согласие владельца на выдуманное число | число уехало в критерий готовности | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА H1 |
| И-10 | И | `04.5-intervyu` | механика разговора | Дефект вычитан из расшифровки, владелец его не называл | правка снесла бы верный текст | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА H2 → см. ниже |
| И-11 | И | `04.5-intervyu` | механика разговора | Обсуждали как нерешённые задачи, уже решённые в тексте | два полных круга диалога впустую | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА J4 |
| И-12 | И | `04.5-intervyu` | механика разговора | Вопрос владельцу задан внутренним языком арки | круг потрачен впустую | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА J1 |
| И-13 | И | `04.5-intervyu` | механика разговора | Аналитик заявил математический факт сильнее, чем мог доказать | владелец построил несущий такт и сам спросил «ты уверен?»; повторный прецедент | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | НЕТ РЫЧАГА → предложен H9 |
| И-14 | И | `04.5-intervyu` | механика разговора | Аналитик уходит в верификацию частности вместо расширения пула | раздел переписан, «ты опять уходишь в частности» | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА J3 |
| И-15 | И | `04.5-intervyu` | механика разговора | Трижды заявлено отсутствие без проверки по живым файлам | снятый по фальшивому доводу сюжет | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА J4 |
| И-16 | И | `04.5-intervyu` | механика разговора | Аналитик приписал владельцу авторство своей идеи | кандидат вошёл в хэндофф как «от владельца» | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА H2 → см. ниже |
| И-17 | И | `04.5-intervyu` | механика разговора | Записано «переизобрёл», хотя он услышал | поправка + правка двух файлов | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА H2 → см. ниже |
| И-18 | И | `04.5-intervyu` | механика разговора | Формула выдана без определения операций | владелец не понял результат | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА J2 |
| И-19 | И | `04.5-intervyu` | механика разговора | Аналитик трижды замыкал рамку, владелец трижды открывал | 3 раунда на снятие чужой рамки | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА H4 |
| И-20 | И | `04.5-intervyu` | механика разговора | Два вопроса — прямой anti-scope арки | раунд обсуждения впустую | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА J5 |
| И-21 | И | `04.5-intervyu` | механика разговора | Находка противоречит продиктованной линии | раунд 23 построен вокруг противоречия | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | ЗАКОН DOK.md «двустороннее» п.2 |
| И-22 | И | `04.5-intervyu` | механика разговора | Гипотеза о содержании книги-якоря взята на веру | рамка курса переписана целиком | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА H3 |
| И-23 | И | `04.5-intervyu` | механика разговора | Услышав «без комбинаторики», выбросил счёт исходов | из лекции 1 выпал весь счёт исходов | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА J15 |
| И-24 | И | `04.5-intervyu` | механика разговора | Виджет вопросов оборвался, вопросы не дошли | один потерянный ход | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | ЗАКОН DOK.md «виджет оборвался» |
| И-25 | И | `04.5-intervyu` | механика разговора | Правдоподобная математическая проза прошла как работа | вердикт получен на неверной формулировке | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | НЕТ РЫЧАГА → предложен H9 |
| И-26 | И | `04.5-intervyu` | механика разговора | Сильный материал трижды отложен ради слабого | сильнейший сюжет не предъявлен первым | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА J14 |
| И-27 | И | `04.5-intervyu` | механика разговора | Различение переформулировано трижды, аналитик дважды съехал | ошибка уровня, не оттенка | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА H2 → см. ниже |
| И-28 | И | `04.5-intervyu` | механика разговора | Адреса правок писались по отчёту, не по живому файлу | 2 предписания из 5 — в пустоту | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА J4 |
| И-29 | И | `04.5-intervyu` | механика разговора | «Микшеры направо» → «ползунки налево» — противоположное | один полный прогон не туда | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | АНКЕТА H2 → см. ниже |
| И-30 | И | `04.5-intervyu` | механика разговора | Отрицательный вердикт дан без охвата поиска | чуть не выброшена несущая линия курса | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «механика разговора») | НЕТ РЫЧАГА → предложен H10 |
| И-31 | И | `04.5-intervyu` | форма текста | Маркированный список — главный инструмент, канон говорил обратное | 11 адресов, 8 подряд на одном слайде | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «форма текста») | АНКЕТА E1 |
| И-32 | И | `04.5-intervyu` | форма текста | Перечень-экспонат: пункт — строка, комментария нет | охват «весь дек», 5 адресов | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «форма текста») | АНКЕТА E5 |
| И-33 | И | `04.5-intervyu` | форма текста | Объяснено словами то, что скажет лектор | 6 адресов без ограничителя | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «форма текста») | АНКЕТА E2 |
| И-34 | И | `04.5-intervyu` | форма текста | Служебные пометки лектору попали в публичную зону | 3 акта, 3 слайда со служебными пометками | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «форма текста») | НЕТ РЫЧАГА → предложен J17 |
| И-35 | И | `04.5-intervyu` | форма текста | Жанровых ярлыков «Задача/Определение» в лекции нет | требование повторено дважды | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «форма текста») | АНКЕТА E4 |
| И-36 | И | `04.5-intervyu` | форма текста | «Так не говорят по-русски» — 10 адресов при уже записанных уроках | владелец дважды сослался на уроки | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «форма текста») | АНКЕТА E6 |
| И-37 | И | `04.5-intervyu` | форма текста | Замер регистра: 3 утверждения вместо одного в предложении | 32,7 слова против 18,1 у эталона | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «форма текста») | АНКЕТА E1 |
| И-38 | И | `04.5-intervyu` | форма текста | У слайда нет заголовка / заголовок не как заголовок раздела | 8 адресов, 1 похвала за 6 актов | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «форма текста») | АНКЕТА E3 |
| И-39 | И | `04.5-intervyu` | форма текста | Формулировка непонятна владельцу-математику | пакет «нужен автор, не верстальщик» | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «форма текста») | НЕТ РЫЧАГА → предложен J18 |
| И-40 | И | `04.5-intervyu` | форма текста | Неформальное оформлено как определение, очевидное доказано | врезки съедены впустую | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «форма текста») | АНКЕТА J16 |
| И-41 | И | `04.5-intervyu` | форма текста | Понятие введено определением без мотивировки | главный дефект первой лекции | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «форма текста») | АНКЕТА E7 |
| И-42 | И | `04.5-intervyu` | форма текста | Механические гейты не судят мотивацию, вслух не сказано | 33 врезки написаны и не годны к использованию | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «форма текста») | АНКЕТА E7 |
| И-43 | И | `04.5-intervyu` | единицы выхода | Заход на раскладку запущен БЕЗ раскладки | ≈290 тыс. токенов, два негодных артефакта | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «единицы выхода») | ГЕЙТ G16.2 · анкета C1 |
| И-44 | И | `04.5-intervyu` | единицы выхода | Нет критерия «что такое один слайд» | 7 редакций списка за вечер | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «единицы выхода») | АНКЕТА C2 |
| И-45 | И | `04.5-intervyu` | единицы выхода | Список слайдов ушёл в работу без приёмки | лента 55 разделов, 6 кругов подгонки | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «единицы выхода») | ГЕЙТ G16.1 · анкета C4 |
| И-46 | И | `04.5-intervyu` | единицы выхода | Материал, уже сказанный и написанный, до дека не дошёл | слайд недосчитался половины содержания | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «единицы выхода») | АНКЕТА J12 |
| И-47 | И | `04.5-intervyu` | единицы выхода | Слайд дублирует предыдущий — видно только лентой | 3 адреса снимают слайд целиком | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «единицы выхода») | АНКЕТА J13 |
| И-48 | И | `04.5-intervyu` | единицы выхода | Критерий отбора появился ПОСЛЕ приёмки | доп. заход целиком + ручная доводка | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «единицы выхода») | АНКЕТА C7 |
| И-49 | И | `04.5-intervyu` | единицы выхода | «Одна центральная задача на занятие» завела в тупик | под правила суммы/произведения задачи нет | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «единицы выхода») | АНКЕТА C2 |
| И-50 | И | `04.5-intervyu` | единицы выхода | Три конкурирующие мотивации выданы за богатство выбора | 2 круга непринятия | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «единицы выхода») | АНКЕТА C6 |
| И-51 | И | `04.5-intervyu` | иллюстрации без ТЗ | Иллюстрация заказывается просьбой, не описанием | 34 фигуры → 11, 9 слайдов без иллюстраций | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «иллюстрации без ТЗ») | АНКЕТА G2 |
| И-52 | И | `04.5-intervyu` | иллюстрации без ТЗ | Доля брака дошла до «убрать все» | 11+8 адресов | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «иллюстрации без ТЗ») | АНКЕТА G2 |
| И-53 | И | `04.5-intervyu` | иллюстрации без ТЗ | Пример на картинке не общего положения, лишняя симметрия | 4 адреса, маркер «Опять» | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «иллюстрации без ТЗ») | АНКЕТА G2 |
| И-54 | И | `04.5-intervyu` | иллюстрации без ТЗ | Правило «без подписей» без названных исключений | снятие цифр 2 и 1, которые велено оставить | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «иллюстрации без ТЗ») | АНКЕТА J15 |
| И-55 | И | `04.5-intervyu` | иллюстрации без ТЗ | Коммутативный квадрат написан равенством | повторено дважды в одном акте | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «иллюстрации без ТЗ») | АНКЕТА G2 |
| И-56 | И | `04.5-intervyu` | иллюстрации без ТЗ | Персоналия — пафосная подпись вместо портрета | слайд переписывается целиком | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «иллюстрации без ТЗ») | АНКЕТА G2 |
| И-57 | И | `04.5-intervyu` | иллюстрации без ТЗ | Жёсткая спека+эталон+PNG — то, чего не было в первой попытке | 2 рисунка впустую в первой попытке | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «иллюстрации без ТЗ») | АНКЕТА G2 |
| И-58 | И | `04.5-intervyu` | габарит | Замер живой лекции: 15 слайдов за 1,5ч, расчёты завышены вдвое | половина живой лекции не прозвучала | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «габарит») | ГЕЙТ G16.4 · анкета B1 |
| И-59 | И | `04.5-intervyu` | габарит | Габарит проектировался на глаз при живом эталоне рядом | 3 круга вхолостую + снятие сюжета | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «габарит») | ГЕЙТ G16.4 |
| И-60 | И | `04.5-intervyu` | габарит | Габарит сверен по ЧИСЛУ сцен, не по плотности | лекция на 90 мин прочитана за 50 | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «габарит») | АНКЕТА B2 |
| И-61 | И | `04.5-intervyu` | габарит | Упаковка снимает слайды, не минуты | 48→39 слайдов при росте 178→186 минут | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «габарит») | АНКЕТА J8 |
| И-62 | И | `04.5-intervyu` | габарит | Граница честного сжатия −10%, требовали −30…−38% | на −14,5% найдено 5 сломанных формулировок | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «габарит») | АНКЕТА J9 |
| И-63 | И | `04.5-intervyu` | плотность | Сцены не увеличивают вместимость, слайд = один экран | весь дек, 7 адресов | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «плотность») | АНКЕТА D1 |
| И-64 | И | `04.5-intervyu` | плотность | Гейт задал верхнюю границу объёма и не задал нижнюю | 38 экранов по 195 знаков при медиане ~300 | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «плотность») | АНКЕТА D2 |
| И-65 | И | `04.5-intervyu` | плотность | Плотность — инвариант, нижней границы в каноне нет | отсутствие пола не дало разъезду покраснеть | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «плотность») | АНКЕТА D2 |
| И-66 | И | `04.5-intervyu` | плотность | «Максимально кратко» прочитано как «мало содержания» | объём вырос втрое, 24→78 тыс. знаков | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «плотность») | АНКЕТА D3 |
| И-67 | И | `04.5-intervyu` | плотность | Два захода мерили вместимость в разных единицах | лента 55 разделов вместо 32 за сутки до лекции | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «плотность») | АНКЕТА C2 |
| И-68 | И | `04.5-intervyu` | жанр и зал | Жанр артефакта не установлен до захода | ≈410 тыс. токенов, Часть 0 обесценилась целиком | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «жанр и зал») | АНКЕТА A1 |
| И-69 | И | `04.5-intervyu` | жанр и зал | Вывод аналитика принят как данность, лекционность не проверена | полный прогон Opus впустую | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «жанр и зал») | АНКЕТА A1 |
| И-70 | И | `04.5-intervyu` | жанр и зал | Слайд обязан быть опорой лектору, а не только залу | сбой на репетиции: «забыл, что такое центр» | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «жанр и зал») | АНКЕТА J11 |
| И-71 | И | `04.5-intervyu` | раскладка и сцены | Монотонность раскладок: архетип назначает лента | 44 из 55 слайдов, серия из 9 подряд | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «раскладка и сцены») | АНКЕТА J10 |
| И-72 | И | `04.5-intervyu` | раскладка и сцены | Накопление против замены: по умолчанию — замена | 4 слайда, где текст пропадал | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «раскладка и сцены») | АНКЕТА F3 |
| И-73 | И | `04.5-intervyu` | раскладка и сцены | Такта «вопрос залу» нет — ответ виден сразу | 7 адресов в 3 актах из 6 | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «раскладка и сцены») | АНКЕТА F1 |
| И-74 | И | `04.5-intervyu` | порядок изложения | Порядок изложения: определение до применения, простое до сложного | 9 адресов, порядок продиктован дважды | переехало в фазу 4.5 (04.5-intervyu/POKRYTIE.md, подкласс «порядок изложения») | АНКЕТА C5 |

## Раздел 4 · корпус «автолог git» — классы инцидентов (`_INFRA-git/INCIDENTY.md`, разбор `RAZBOR-povtorov.md`)

> Дата данных разбора: 2026-08-04 (`RAZBOR-povtorov.md`), **кратности ниже пересчитаны на дату сборки этой картотеки** (2026-08-05) командой `RAZBOR-povtorov.md §6` против живого `_INFRA-git/INCIDENTY.md`: `grep -c '^- 20' ...` даёт **107** строк (было 90 на 04.08 — лог растёт непрерывно). Классы A–L устойчивы как id (буквы самого файла-источника). **Колонка ФАЗА (часть B этого захода): все классы = `вне-фаз` без исключения** — по определению корпуса (git-дисциплина монорепо, не привязана ни к одному шагу производства дека; см. A0 «вне-фаз»). Разрезать нечего — гомогенно по построению.

| id | симптом | кратность (05.08) | класс | фаза | статус | рычаг |
|---|---|---|---|---|---|---|
| ГИТ-A | `--no-verify`: регистрация нового `.md` — хук требует, контракт зоны запрещал | 26 | П | `вне-фаз` | закрыт | дверь `register_doc.py` (30.07) |
| ГИТ-G | «коммит прошёл не целиком»: пути не доехали или коммит упал | 21 | П | `вне-фаз` | жив | нет — инструмент не называет, какие пути не доехали |
| ГИТ-B | `--no-verify`: долг окружения песочницы (playwright/chrome-headless) | 12 | П | `вне-фаз` | жив | нет — фикстура краснеет на отсутствующем браузере |
| ГИТ-H | `commit` без плана при грязном дереве | 8 | П | `вне-фаз` | жив | `git_zona.py commit --zone -m` существует, но не дефолт |
| ГИТ-D | merge отбит: грязные пути пересекаются со сливаемыми | 8 | П | `вне-фаз` | жив | нет — инструмент не называет, что именно пересеклось |
| ГИТ-E | merge: конфликт путей | 8 | П | `вне-фаз` | не дефект | конфликты — нормальная жизнь ветвления, чинятся руками |
| ГИТ-I | план не готов или битый (плейсхолдеры `==`) | 5 | П | `вне-фаз` | тихий | нет — черновик плана не имеет срока годности |
| ГИТ-C | `--no-verify`: прочий чужой долг | 5 | П | `вне-фаз` | — | разнородное, класса не образует |
| ГИТ-K | запуск с мусорными аргументами | 4 | П | `вне-фаз` | тихий | нет — ошибка не называет список существующих флагов |
| ГИТ-F | merge не прошёл (без диагноза) | 4 | П | `вне-фаз` | жив | тот же дефект, что G, только на merge |
| ГИТ-L | песочница: запись в `.git` запрещена | 3 | П | `вне-фаз` | закрыт | `doctor` предупреждает первым экраном |
| ГИТ-J | план называет пути, которых нет на диске | 3 | П | `вне-фаз` | тихий | частный случай I |

**Сверка охвата Раздела 4:** Σ кратностей = 26+21+12+8+8+8+5+5+4+4+3+3 = **107** = живому счёту `INCIDENTY.md` на дату сборки. Пересчёт — команда в шапке раздела.

## Раздел 5 (новый, этот заход) · корпус «уроки арок» вне класса И — 243 записи

> **Дефект прошлого захода, который чинит этот раздел** (см. `## ПЛАН`, «Гейт-против-охвата» старой версии файла): из 316 уроков арок только 74 (класс И, Раздел 3) были представлены в картотеке — 242 записи П/Т/Д существовали только суммой в `DOK.md`/`POKRYTIE.md`, ни разу не итемизированы. Скрипт `sobrat_karkas_faz.py urokov` вычел 74 адреса класса И (по совпадению `файл:строка` с `POKRYTIE.md`) из полного списка 316 `### `-секций всех `*/UROKI-FABRIKE.md` — дал **243**, не 242 (на 1 больше: у одного урока арок оказалось ДВЕ разных цитаты класса И внутри одной секции — та самая честно названная «вилка И/П/Д на десятке уроков», не ошибка счёта). Оставшиеся 243 сгруппированы субагентами по МЕХАНИЗМУ (метод `KRATNOST.md`) и размечены по фазе A0.

| симптом (механизм) | фаза | кратность | адреса (файл:строки; базовая папка `_studio/zhurnal/<арка>/UROKI-FABRIKE.md`, если не указано иное) |
|---|---|---|---|
| Число/статус в шапке документа вписаны вручную и устаревают | `вне-фаз` | 3 | teorkat-programma-dizajn/UROKI-FABRIKE.md:78; teorkat-l1/UROKI-FABRIKE.md:57; osnovanie-vvedenie/UROKI-FABRIKE.md:24 |
| Критерий/гейт не может провалиться либо не оспорен до начала работы | `вне-фаз` | 2 | teorkat-programma-dizajn/UROKI-FABRIKE.md:61,199 |
| Гейт ломается на форме вызова (rc неоднозначен/пустой вход/regex проглочен) | `вне-фаз` | 3 | teorkat-programma-dizajn/UROKI-FABRIKE.md:296,308; mat-kostyak/UROKI-FABRIKE.md:61 |
| Механическая проверка структурно не покрывает целую категорию источников/разметки | `вне-фаз` | 2 | teorkat-programma-dizajn/UROKI-FABRIKE.md:138; teorkat-l1/UROKI-FABRIKE.md:69 |
| Греп даёт ложный результат (подстрока/регистр/нулевой греп как доказательство) | `вне-фаз` | 3 | teorkat-programma-dizajn/UROKI-FABRIKE.md:175,323,349 |
| Канал субагента непрозрачен (рвётся/деградирует/обрезает молча) | `вне-фаз` | 4 | teorkat-l1/UROKI-FABRIKE.md:51,65,83; teorkat-motivacia/UROKI-FABRIKE.md:84 |
| Осиротевший git-lock блокирует обязательные коммиты | `вне-фаз` | 2 | teorkat-l1/UROKI-FABRIKE.md:43; teorkat-motivacia/UROKI-FABRIKE.md:79 |
| Контракт зоны предписывает ветку без нужного проекта | `вне-фаз` | 1 | teorkat-l1/UROKI-FABRIKE.md:39 |
| «Зона = папка целиком» ломается при параллельной записи аналитика | `вне-фаз` | 1 | teorkat-l1/UROKI-FABRIKE.md:91 |
| Обязательный пункт критерия стоит последним по приоритету | `вне-фаз` | 1 | teorkat-l1/UROKI-FABRIKE.md:95 |
| Мёртвая URL-ссылка в реестре источников теряет источник молча | `02-reserch` | 1 | teorkat-l1/UROKI-FABRIKE.md:47 |
| Требование дословной цитаты конфликтует с ограничением объёма | `02-reserch/03-matbaza` | 1 | teorkat-l1/UROKI-FABRIKE.md:61 |
| Системная утилита (file) даёт неверное число страниц PDF | `вне-фаз` | 1 | teorkat-l1/UROKI-FABRIKE.md:77 |
| Честная приписка «не читан» глушит гейт | `вне-фаз` | 1 | teorkat-l1/UROKI-FABRIKE.md:73 |
| Защитная мера вписана в канон только после первой потери | `вне-фаз` | 1 | teorkat-l1/UROKI-FABRIKE.md:87 |
| Аналитик передаёт заходу дефектную предпосылку, не пройдя гейт входа | `вне-фаз` | 1 | teorkat-programma-dizajn/UROKI-FABRIKE.md:98 |
| Аналитик сужает буквальный ответ владельца до более узкого факта | `04.5-intervyu` | 1 | teorkat-programma-dizajn/UROKI-FABRIKE.md:116 |
| Контракт зоны запрещает писать в дом получателя, перенос не встроен в приёмку | `вне-фаз` | 1 | teorkat-programma-dizajn/UROKI-FABRIKE.md:149 |
| Отрицательный вердикт без охвата рядом | `вне-фаз` | 1 | teorkat-programma-dizajn/UROKI-FABRIKE.md:165 |
| Аналитик правит файлы во время чужого прогона, не объявив зону | `вне-фаз` | 1 | teorkat-programma-dizajn/UROKI-FABRIKE.md:187 |
| Аналитик задаёт субагенту слишком узкую границу поиска | `вне-фаз` | 1 | teorkat-programma-dizajn/UROKI-FABRIKE.md:365 |
| Аналитик заводит документ-дублёр, не проверив штатный шаблон | `вне-фаз` | 1 | osnovanie-vvedenie/UROKI-FABRIKE.md:14 |
| Новые .md не зарегистрированы в KARTA.md §6 | `вне-фаз` | 1 | osnovanie-vvedenie/UROKI-FABRIKE.md:19 |
| Заход написан руками мимо bootstrap_zahod.py | `вне-фаз` | 1 | osnovanie-vvedenie/UROKI-FABRIKE.md:29 |
| Аналитик утверждает владельцу отрицательный факт, проверив не то место | `вне-фаз` | 1 | osnovanie-vvedenie/UROKI-FABRIKE.md:34 |
| Утверждение канона о среде исполнения опровергается прямой проверкой | `вне-фаз` | 1 | teorkat-motivacia/UROKI-FABRIKE.md:57 |
| Калибровочный гейт сведён из вердиктов на разные вопросы | `вне-фаз` | 1 | teorkat-motivacia/UROKI-FABRIKE.md:65 |
| Обязательный отчёт положен не в файл захода | `вне-фаз` | 1 | teorkat-motivacia/UROKI-FABRIKE.md:69 |
| Критерий «непомеченных утверждений — 0» не различает доказуемость и суждение | `03-matbaza` | 1 | teorkat-motivacia/UROKI-FABRIKE.md:90 |
| Движок build_doc.py/check_view — непроверяемые из песочницы дефекты рендера | `вне-фаз` | 2 | teorkat-motivacia/UROKI-FABRIKE.md:95,100 |
| Приёмщик арки написан под чужой формат вместо назначенного заданием | `03-matbaza` | 1 | mat-kostyak/UROKI-FABRIKE.md:65 |
| Гейт документа и приёмщик оба ломаются на самоцитировании служебных маркеров | `вне-фаз` | 1 | mat-kostyak/UROKI-FABRIKE.md:69 |
| Правило без механизма проверки не дисциплинирует того, кто его записал | `вне-фаз` | 1 | teorkat-programma-dizajn/UROKI-FABRIKE.md:37 |
| Гейт на репо-глобальном файле красит коммиты в чужих зонах | `вне-фаз` | 1 | teorkat-programma-dizajn/UROKI-FABRIKE.md:280 |
| Файл-результат прошлого прогона неотличим от свежего той же командой | `вне-фаз` | 1 | teorkat-programma-dizajn/UROKI-FABRIKE.md:333 |
| Отметка «закрыто, не переоткрывать» без даты доверия пережила устаревший факт | `01-brief` | 1 | osnovanie-vvedenie/UROKI-FABRIKE.md:9 |
| Записанное правило не сверяется автором нового захода/сообщения повторно | `вне-фаз` | 3 | mat-kostyak/UROKI-FABRIKE.md:77,113; lekcia-1/UROKI-FABRIKE.md:154 |
| «Read-only» git-команда на деле переписывает индекс/берёт lock | `вне-фаз` | 1 | mat-kostyak/UROKI-FABRIKE.md:85 |
| Оглавление источника принято достаточной опорой отрицательного вывода | `02-reserch/03-matbaza` | 1 | mat-kostyak/UROKI-FABRIKE.md:89 |
| Диагноз «гейт ошибочен» оказался ложным при перепроверке | `вне-фаз` | 1 | mat-kostyak/UROKI-FABRIKE.md:93 |
| Фоновый авто-коммит хука стейджит всё дерево вопреки строгому pathspec | `вне-фаз` | 2 | mat-kostyak/UROKI-FABRIKE.md:97,105 |
| Счётчик в шапке (не команда) сам протух после переименования поля | `03-matbaza` | 1 | mat-kostyak/UROKI-FABRIKE.md:101 |
| Заход назвал опорной папку с нерелевантным содержимым | `02-reserch/03-matbaza` | 1 | mat-kostyak/UROKI-FABRIKE.md:109 |
| Гейт в форме, дающей ложный красный на здоровом документе, не прогнан до фиксации | `03-matbaza` | 1 | mat-kostyak/UROKI-FABRIKE.md:121 |
| Аналитик принял мидфлайт работающего захода за обрыв | `вне-фаз` | 1 | mat-kostyak/UROKI-FABRIKE.md:125 |
| Гейт «урок без цены» не распознаёт легитимный жирный вариант | `вне-фаз` | 1 | mat-kostyak/UROKI-FABRIKE.md:129 |
| Фикстуры гейта либо игнорируются, либо блокируют весь репозиторий | `вне-фаз` | 2 | mat-kostyak/UROKI-FABRIKE.md:133,137 |
| Сбой окружения (rc/права ФС) прочитан как факт о проверяемом предмете | `вне-фаз` | 1 | mat-kostyak/UROKI-FABRIKE.md:141 |
| Pathspec-коммит матчит только отслеживаемые пути — падает на новом файле | `вне-фаз` | 1 | mat-kostyak/UROKI-FABRIKE.md:145 |
| Производное число вписано вручную вместо пересчёта — разошлось с суммой рядом | `03-matbaza` | 1 | mat-kostyak/UROKI-FABRIKE.md:149 |
| Производное число вписано вручную вместо пересчёта — разошлось с суммой рядом (2) | `05-raskadrovka` | 1 | paskal-lekcia-sborka/UROKI-FABRIKE.md:44 |
| Число сцен слайда в двух представлениях, второе не пересобирается при правке текста | `08-sceny` | 2 | paskal-lekcia-sborka/UROKI-FABRIKE.md:72,77 |
| Рецепт визуального гейта содержит неполную (оборванную) карту разворачивания классов | `09-illustracii/10-sborka-qa` | 1 | paskal-lekcia-sborka/UROKI-FABRIKE.md:82 |
| Кэш формул не пересобирается автоматически при правке формулы в тексте | `06-tekst/10-sborka-qa` | 1 | paskal-lekcia-sborka/UROKI-FABRIKE.md:102 |
| Рендер cairosvg масштабирует превью по width, игнорируя viewBox | `09-illustracii` | 1 | paskal-lekcia-sborka/UROKI-FABRIKE.md:87 |
| Маркер сцены {@N} не распознаётся внутри пункта списка | `08-sceny` | 1 | paskal-lekcia-sborka/UROKI-FABRIKE.md:92 |
| Нет браузера у агента — визуальные дефекты идут кругами правок через владельца | `10-sborka-qa` | 1 | paskal-lekcia-sborka/UROKI-FABRIKE.md:107 |
| Снятие блюра по ошибке засчитано отдельной сценой — объём раскадровки раздут | `08-sceny` | 1 | paskal-lekcia-sborka/UROKI-FABRIKE.md:54 |
| check_view.py даёт неверный рендер (курсив в код-спанах/список схлопнут/ложный матч) | `03-matbaza` | 1 | mat-kostyak/UROKI-FABRIKE.md:159 |
| Гейт битых ссылок матчит любой токен в кавычках, не отличая ссылку от упоминания | `вне-фаз` | 2 | lekcia-1/UROKI-FABRIKE.md:198,207 |
| Консолидация из одного узкого источника теряет легитимный контент из другого места | `вне-фаз` | 1 | lekcia-1/UROKI-FABRIKE.md:74 |
| Консолидация из одного узкого источника теряет легитимный контент (2) | `04-gibrid-istochnik` | 1 | lekcia-1/UROKI-FABRIKE.md:230 |
| Worktree/заход отдан до коммита нужного содержимого в его ветку | `вне-фаз` | 2 | vneshnie-istorii/UROKI-FABRIKE.md:37; lekcia-1/UROKI-FABRIKE.md:180 |
| Путь git-коммита зоны рвётся на разных мелочах несколько раз за сессию | `вне-фаз` | 1 | vneshnie-istorii/UROKI-FABRIKE.md:42 |
| Числовые планки заданы критерием для поискового захода с заранее неизвестным объёмом | `02-reserch` | 1 | lekcia-1/UROKI-FABRIKE.md:54 |
| Верификатор требует объёма, равного полному повтору проверяемой стадии | `02-reserch` | 1 | lekcia-1/UROKI-FABRIKE.md:59 |
| Две обязательные нормы канона взаимно исключают друг друга | `вне-фаз` | 1 | lekcia-1/UROKI-FABRIKE.md:65 |
| Команда коммита зоны называет один каталог, работа шла в двух — часть не закоммичена | `вне-фаз` | 1 | lekcia-1/UROKI-FABRIKE.md:96 |
| Легальный обход гейта физически недоступен из-за запрета shell владельцу | `вне-фаз` | 1 | lekcia-1/UROKI-FABRIKE.md:114 |
| Критерий охвата задан синтаксисом источника, теряет легитимный прозаический контент | `вне-фаз` | 1 | lekcia-1/UROKI-FABRIKE.md:143 |
| Оси классификации прошлого захода не переводятся 1-в-1 в оси текущего | `02-reserch/04-gibrid-istochnik` | 1 | lekcia-1/UROKI-FABRIKE.md:132 |
| Сообщение инструмента не печатает важный факт (успех/хэш) первой строкой | `вне-фаз` | 1 | lekcia-1/UROKI-FABRIKE.md:165 |
| «kod_-заходы регенерируемы» ложно для случая с оплаченными уроками внутри | `вне-фаз` | 1 | lekcia-1/UROKI-FABRIKE.md:189 |
| Regex-класс с кириллицей не матчится на macOS/BSD | `вне-фаз` | 1 | mat-kostyak/UROKI-FABRIKE.md:164 |
| Верификатор отчитался находками, а не охватом | `вне-фаз` | 1 | mat-kostyak/UROKI-FABRIKE.md:169 |
| Скрипт без валидации имени принял CLI-флаг за позиционный аргумент | `вне-фаз` | 1 | mat-kostyak/UROKI-FABRIKE.md:174 |
| Адреса/факты в заходе даны по вторичному источнику, не по живым файлам | `03-matbaza` | 1 | mat-kostyak/UROKI-FABRIKE.md:179 |
| Критерий готовности жёстко привязан к месту, которое заход разрешает переместить | `03-matbaza` | 1 | mat-kostyak/UROKI-FABRIKE.md:154 |
| Число зашито руками в критерий/константу вместо вычисления | `10-sborka-qa` | 2 | paskal-lekcia-sborka/UROKI-FABRIKE.md:117; konspekt-l1/UROKI-FABRIKE.md:100 |
| Число зашито руками в критерий/константу вместо вычисления (брифовые/целевые значения) | `01-brief` | 2 | konspekt-l1/UROKI-FABRIKE.md:245,255 |
| Гейт/правка адресуется порождённому слою вместо источника | `07-verstka` | 1 | paskal-lekcia-sborka/UROKI-FABRIKE.md:137 |
| Гейт/правка адресуется порождённому слою вместо источника (2) | `вне-фаз` | 2 | konspekt-l1/UROKI-FABRIKE.md:213,281 |
| Два предписания канона/задачи взаимно исключают друг друга | `вне-фаз` | 3 | konspekt-l1/UROKI-FABRIKE.md:315,346,364 |
| Гейт технически не может дать красный сигнал | `10-sborka-qa` | 1 | paskal-lekcia-sborka/UROKI-FABRIKE.md:122 |
| Гейт технически не может дать красный сигнал (2) | `вне-фаз` | 1 | konspekt-l1/UROKI-FABRIKE.md:285 |
| Гейт «ничего не потеряно» слеп к неблочному содержимому | `вне-фаз` | 1 | konspekt-l1/UROKI-FABRIKE.md:69 |
| Гейт «ничего не потеряно» слеп к неблочному содержимому (2) | `01-brief` | 1 | konspekt-l1/UROKI-FABRIKE.md:271 |
| Шкала классификации содержит мёртвую/недостающую клетку | `05-raskadrovka` | 2 | konspekt-l1/UROKI-FABRIKE.md:109,118 |
| Автоматика ищет точную строку/регистр, живая формулировка отличается по форме | `вне-фаз` | 2 | konspekt-l1/UROKI-FABRIKE.md:131,370 |
| Новый гейт составлен по памяти, не прогнан на живом эталоне до включения | `10-sborka-qa` | 1 | paskal-lekcia-sborka/UROKI-FABRIKE.md:112 |
| Новый гейт составлен по памяти, не прогнан на живом эталоне до включения (2) | `вне-фаз` | 1 | konspekt-l1/UROKI-FABRIKE.md:289 |
| Нужный файл/шаблон физически отсутствует или устарел в дереве | `07-verstka` | 1 | konspekt-l1/UROKI-FABRIKE.md:204 |
| Нужный файл/шаблон физически отсутствует или устарел в дереве (2) | `вне-фаз` | 1 | konspekt-l1/UROKI-FABRIKE.md:375 |
| Независимый верификатор ловит то, что самопроверка автора систематически пропускает | `03-matbaza` | 2 | konspekt-l1/UROKI-FABRIKE.md:225,332 |
| Адрес, названный в задании захода, неверен/неполон при запрете смотреть по сторонам | `вне-фаз` | 2 | konspekt-l1/UROKI-FABRIKE.md:299,303 |
| Шаблон заход-документа дал путь/значение как пример, использован как инструкция | `вне-фаз` | 2 | konspekt-l1/UROKI-FABRIKE.md:351,355 |
| Реестр гейтов объявляет закрытым долг, которого в коде фактически нет | `10-sborka-qa` | 1 | paskal-lekcia-sborka/UROKI-FABRIKE.md:127 |
| Асимметричная git-дисциплина между аналитиком и исполнителем в одном репо | `вне-фаз` | 1 | paskal-lekcia-sborka/UROKI-FABRIKE.md:132 |
| Движок документа берёт вкладкой любой *.md, включая симлинк | `вне-фаз` | 1 | konspekt-l1/UROKI-FABRIKE.md:78 |
| Список и слитная цветная врезка физически несовместимы внутри одного движка | `вне-фаз` | 1 | konspekt-l1/UROKI-FABRIKE.md:87 |
| Все машинные гейты зелёные, а в браузере видно иначе (теги vs видимость) | `10-sborka-qa` | 1 | konspekt-l1/UROKI-FABRIKE.md:150 |
| Канон фазы имеет незаписанное следствие, противоречащее модели автора захода | `08-sceny` | 1 | konspekt-l1/UROKI-FABRIKE.md:157 |
| Два инструмента измерения одного объекта готовят его по-разному, дают разные числа | `10-sborka-qa` | 1 | konspekt-l1/UROKI-FABRIKE.md:164 |
| Список правок отсортирован по тяжести дефекта, а не заметность×цена | `вне-фаз` | 1 | konspekt-l1/UROKI-FABRIKE.md:195 |
| Ключ файла состояния — позиционный индекс sNN, не устойчивый id | `07-verstka` | 1 | konspekt-l1/UROKI-FABRIKE.md:250 |
| Число, названное потолком, фактически используется как цель подгонки | `06-tekst` | 1 | konspekt-l1/UROKI-FABRIKE.md:259 |
| Греп-критерий задан без ограничивающего пути — шире, чем имелось в виду | `вне-фаз` | 1 | konspekt-l1/UROKI-FABRIKE.md:277 |
| Заход несёт более одного критерия готовности одновременно | `вне-фаз` | 1 | konspekt-l1/UROKI-FABRIKE.md:293 |
| Предпосылка захода уже выполнена на живых файлах, но записана как цель | `вне-фаз` | 1 | konspekt-l1/UROKI-FABRIKE.md:307 |
| Метка «проверено» стоит на факте, который не был проверен командой | `вне-фаз` | 1 | konspekt-l1/UROKI-FABRIKE.md:311 |
| Верификатор состояния ДО работы стоит в шаблоне ПОСЛЕ выполнения | `вне-фаз` | 1 | konspekt-l1/UROKI-FABRIKE.md:328 |
| Отчёт заявляет охват, которого нет в артефакте — приёмка не сверяет | `вне-фаз` | 1 | konspekt-l1/UROKI-FABRIKE.md:336 |
| Вердикт по одному пункту молча распространяется на весь список | `вне-фаз` | 1 | konspekt-l1/UROKI-FABRIKE.md:340 |
| Git-инструмент не поддерживает валидный кейс и не называет причину | `вне-фаз` | 1 | konspekt-l1/UROKI-FABRIKE.md:360 |
| Секция-реестр продублирована внутри документа, счёт противоречив | `вне-фаз` | 1 | konspekt-l1/UROKI-FABRIKE.md:379 |
| Гейт краснеет на верной работе из-за счётчика, привязанного к устаревшей структуре | `10-sborka-qa` | 1 | konspekt-l1/UROKI-FABRIKE.md:385 |
| Инструмент QA нумерует со смещением, отличным от читателя отчёта | `10-sborka-qa` | 1 | konspekt-l1/UROKI-FABRIKE.md:389 |
| Гейт краснеет на намеренном поведении инструмента (спрятанное тело доказательства) | `03-matbaza` | 1 | konspekt-l1/UROKI-FABRIKE.md:393 |
| Гейт судит форму (символы/HTML/маркер), не суть — семантический дефект проходит | `10-sborka-qa` | 5 | konspekt-l1/UROKI-FABRIKE.md:496,542,556,560,564 |
| Гейт судит форму, не суть (2) | `06-tekst` | 1 | konspekt-l1/UROKI-FABRIKE.md:607 |
| Гейт судит форму, не суть (3) | `08-sceny` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:108 |
| Комментарий в коде движка противоречит самому коду и стандарту | `03-matbaza` | 1 | konspekt-l1/UROKI-FABRIKE.md:397 |
| Перевод строки не создаёт новый абзац — инструкция «разбить на абзацы» невыполнима | `03-matbaza` | 1 | konspekt-l1/UROKI-FABRIKE.md:401 |
| Сообщение об ошибке сборки рекомендует нерабочий в этом состоянии инструмент | `10-sborka-qa` | 1 | konspekt-l1/UROKI-FABRIKE.md:405 |
| Семантика тега диапазона сцен {@N-M} расходится между движком/каноном/лентой | `08-sceny` | 1 | konspekt-l1/UROKI-FABRIKE.md:411 |
| Механика раскрытия сцен реализована на частный случай (тег у абзаца, не у списка) | `08-sceny` | 2 | konspekt-l1/UROKI-FABRIKE.md:415; dovodka-fabriki/UROKI-FABRIKE.md:133 |
| Поле/шорткат объявлен выходом фазы, движок следующей фазы его не читает | `06-tekst` | 1 | konspekt-l1/UROKI-FABRIKE.md:419 |
| Поле/шорткат объявлен выходом фазы, движок следующей его не читает (2) | `08-sceny` | 1 | konspekt-l1/UROKI-FABRIKE.md:602 |
| Порог вместимости слайда посчитан по предполагаемому шаблону, не по реальному | `05-raskadrovka` | 1 | konspekt-l1/UROKI-FABRIKE.md:423 |
| Межабзацный отступ не учтён в расчёте вместимости, съедает половину зоны | `07-verstka` | 1 | konspekt-l1/UROKI-FABRIKE.md:427 |
| Правило (опорная точка) в каноне не имеет носителя-исполнителя | `06-tekst` | 1 | konspekt-l1/UROKI-FABRIKE.md:459 |
| Заявленный слой дека (заголовок слайда) физически отсутствует в выводе | `07-verstka` | 1 | konspekt-l1/UROKI-FABRIKE.md:479 |
| Технически присутствующий элемент (номер слайда) визуально не считывается | `07-verstka` | 1 | konspekt-l1/UROKI-FABRIKE.md:483 |
| Выбор ассета матчит буквальную подстроку прозы, не смысл — ассет остаётся сиротой | `09-illustracii` | 2 | konspekt-l1/UROKI-FABRIKE.md:532,611 |
| Стили/классы иллюстраций определены только в одном из двух движков | `09-illustracii` | 1 | konspekt-l1/UROKI-FABRIKE.md:536 |
| Однопроходный движок расшифровки/сводки молча теряет и искажает контент | `04.5-intervyu` | 1 | konspekt-l1/UROKI-FABRIKE.md:585 |
| Скаффолд создаёт файлы-заглушки, выглядящие как выполненный шаг | `вне-фаз` | 1 | teksty-l1/UROKI-FABRIKE.md:39 |
| Число снято с файла, который в этот момент писал другой параллельный заход | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:39 |
| Аналитик объявил вывод, не прочитав собственный отчёт с готовым ответом | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:43 |
| Числовой порог гейта не воспроизводится из живого файла-источника | `08-sceny` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:47 |
| Обязательное поле шаблона пропущено дважды подряд | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:51 |
| Песочница не даёт удалить файлы в смонтированной папке | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:55 |
| Сводное число в отчёте разошлось с собственным артефактом | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:59 |
| Число в критерии готовности не воспроизводится напечатанной командой | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:63 |
| Секция «0 находок» содержит пересказ чужого инцидента с ценой | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:67 |
| Ритуал «дописывать журнал снизу» нарушен | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:71 |
| Два обязательных правила взаимно исключают друг друга — систематический обход хука | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:75 |
| Статусный файл «читать первым» неделю описывает устаревшее состояние | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:79 |
| Счётчик по строкам структурно слеп там, где раздел — одна строка | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:83 |
| Верификатор «найди обход» находит на порядок больше дыр, чем «проверь работу» | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:88 |
| Критерий готовности построен на непроверенном предположении о своей зоне | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:93 |
| Различие поведения shell (zsh не расщепляет $VAR) описано только для одной стороны | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:98 |
| Проверка контракта смотрит в индекс, фикстуры копируют инструмент с диска | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:103 |
| Регистрация шаблоном (1 строка на N файлов) — гейт ищет имя файла, сироты остаются | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:113 |
| Число, снятое аналитиком на момент написания захода, стареет к моменту запуска | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:118 |
| Реестр гейтов объявляет больше проверок, чем исполняет трекер | `10-sborka-qa` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:123 |
| Снимок для визуальной QA сделан с нераскрытым содержимым сцены | `10-sborka-qa` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:128 |
| Флаг генератора захода пишет файл-заход не в ту рабочую копию | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:138 |
| Критерий, посчитанный ДО работы, применён к состоянию ПОСЛЕ | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:143 |
| Инструмент-сторож почти получил ту же болезнь, которую лечит (омоним ветки/тега) | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:150 |
| Изменение engine.js не распространяется на уже собранные деки | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:155 |
| Фильтр путей git-хука не покрывает часть заявленного охвата фикстуры | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:160 |
| Канон/комментарий инструмента описывает несуществующее поведение | `вне-фаз` | 2 | dovodka-fabriki/UROKI-FABRIKE.md:165,170 |
| Гейт против конкретного дефекта не краснеет на нём без нарочного внесения | `вне-фаз` | 2 | dovodka-fabriki/UROKI-FABRIKE.md:175,224 |
| Команда для владельца ломается в его реальной оболочке — неотличимо от зависания | `вне-фаз` | 3 | dovodka-fabriki/UROKI-FABRIKE.md:180; dovodka-l1/UROKI-FABRIKE.md:166; sayt-drakon/UROKI-FABRIKE.md:39 |
| Нет блокировки при параллельной записи в общий файл/зону | `вне-фаз` | 3 | dovodka-fabriki/UROKI-FABRIKE.md:185; dovodka-l1/UROKI-FABRIKE.md:58; sayt-drakon/UROKI-FABRIKE.md:63 |
| Заявленный охват проверки завышен относительно фактически проверенного | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:190 |
| Вход захода, написанный аналитиком, структурно не может быть оспорен | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:195 |
| Инструмент зоны берёт один префикс пути — подметает чужое или не берёт список | `вне-фаз` | 2 | dovodka-fabriki/UROKI-FABRIKE.md:200; dovodka-l1/UROKI-FABRIKE.md:12 |
| Гейт коммита верно блокирует новый инструмент без фикстуры (сработал как задумано) | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:208 |
| Хэндофф не называет стартовую точку — новая сессия начинает с угадывания | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:212 |
| Генератор не различает свой файл и рукописный (риск затереть правку) | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:216 |
| Код использует синтаксис новее среды владельца — падает в его среде | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:220 |
| Хрупкая текстовая эвристика разбора транскрипта переписывалась трижды | `вне-фаз` | 2 | dovodka-fabriki/UROKI-FABRIKE.md:228,232 |
| Правило существует только прозой, без гейта на нарушение | `вне-фаз` | 3 | dovodka-fabriki/UROKI-FABRIKE.md:236,252,256 |
| Служебный/тестовый запуск инструмента рождает документ-сироту | `вне-фаз` | 2 | dovodka-fabriki/UROKI-FABRIKE.md:240; sayt-drakon/UROKI-FABRIKE.md:55 |
| Аналитик берёт дефолт среды владельца вместо того, чтобы спросить | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:244 |
| Отчёт предписано писать туда, куда у читателя (владельца) нет доступа | `вне-фаз` | 1 | dovodka-fabriki/UROKI-FABRIKE.md:248 |
| Число/счётчик устаревает между замером и применением | `вне-фаз` | 2 | dovodka-fabriki/UROKI-FABRIKE.md:260; dovodka-l1/UROKI-FABRIKE.md:107 |
| Поле раскадровки обещает иллюстрацию, которой на свёрстанном слайде нет | `05-raskadrovka` | 1 | dovodka-l1/UROKI-FABRIKE.md:43 |
| Гейт линтера считает сцену по атрибуту на конкретном элементе — валидный список бракуется | `08-sceny` | 1 | dovodka-l1/UROKI-FABRIKE.md:152 |
| Метрика знаков считает HTML-теги, а не текст | `06-tekst` | 1 | dovodka-l1/UROKI-FABRIKE.md:53 |
| Мандат проверять по узкой ленте, вывод требуется про широкий корпус без доступа | `вне-фаз` | 1 | dovodka-l1/UROKI-FABRIKE.md:48 |
| Отметка «✅ сделано» в своде отражает намерение, а не факт на слайде | `10-sborka-qa` | 1 | dovodka-l1/UROKI-FABRIKE.md:159 |
| Заход обещает исполнителю скиллы/инструменты, которых в среде нет | `вне-фаз` | 1 | sayt-drakon/UROKI-FABRIKE.md:43 |
| SVG проходит структурный гейт, но нечитаем глазами — гейт не проверяет ясность | `09-illustracii` | 1 | teorver-plan/UROKI-FABRIKE.md:43 |
| Нет инструмента визуального рендера/аудита — дефекты видны только глазами до показа | `вне-фаз` | 2 | sayt-drakon/UROKI-FABRIKE.md:51; puti-i-volny/UROKI-FABRIKE.md:30 |
| Убедительная гипотеза упрощения доказательства ложна — вскрыто перебором | `03-matbaza` | 1 | sayt-drakon/UROKI-FABRIKE.md:59 |
| Новый формат артефакта не заведён как арка — нет NAVIGATOR/PLAN | `вне-фаз` | 1 | teorver-plan/UROKI-FABRIKE.md:11 |
| Реальное поведение движка (нумерация врезок) не задокументировано | `вне-фаз` | 1 | teorver-plan/UROKI-FABRIKE.md:39 |
| Правка живёт в двух копиях (CSS-правило движка / патч-словарь по id слайда) | `07-verstka` | 2 | puti-i-volny/UROKI-FABRIKE.md:5; dovodka-l1/UROKI-FABRIKE.md:145 |
| Гейт корректно покраснел на реальной регрессии движка | `вне-фаз` | 1 | puti-i-volny/UROKI-FABRIKE.md:10 |
| Починка велась по гипотезе, не по проверенному механизму | `вне-фаз` | 1 | puti-i-volny/UROKI-FABRIKE.md:15 |

**Сверка охвата Раздела 5:** Σ кратностей = 243 = 316 (`### ` секций всех `UROKI-FABRIKE.md`, минус 11 заглушек) − 73 (уникальных секций, покрытых хотя бы одной из 74 цитат класса И). Пересчёт: `python3 sobrat_karkas_faz.py urokov` и `python3 _data_razdel5.py` в этой папке.

**Итог по фазам (Раздел 5, по главной фазе для строк с `/`):** вне-фаз 159 · 10-sborka-qa 19 · 03-matbaza 14 · 08-sceny 12 · 07-verstka 8 · 02-reserch 7 · 09-illustracii 6 · 06-tekst 6 · 05-raskadrovka 5 · 01-brief 4 · 04.5-intervyu 2 · 04-gibrid-istochnik 1.

## Часть Б · вынос класса И в фазу 4.5 — уже сделан по построению

Раздел 3 (74 записи) **уже** несёт статус «переехало в фазу 4.5» для каждой строки — это прямое
следствие решения метода п.3 выше: единственный корпус, которому в этой картотеке присвоен класс И,
физически ЖИВЁТ в `_studio/konvejer/04.5-intervyu/POKRYTIE.md`, и картотека на него ссылается, не
копирует. Смешанных строк (часть И, часть П/Т/Д) в Разделе 3 не найдено: `POKRYTIE.md` уже разрешил
классификацию в момент своей сборки (метод «по механизму починки» не оставляет промежуточных случаев
внутри одной строки-урока). Единственная мнимая «смешанность» — топическое пересечение с Разделом 2
(владелец), и она размечена отдельной колонкой «пересечение», не переносом.


## Часть C · перевод рычагов с анкеты на гейты — вердикт по всем 62 из 62

62 урока класса И держатся на 40 различных пунктах анкеты (несколько уроков нередко делят один пункт — так, `H2` в одиночку несёт 6 уроков). Ниже — вердикт по КАЖДОМУ из 40 пунктов; сумма колонки «уроков» равна 62 (проверено: `40 пунктов, 62 урока` — см. метод в шапке файла). **Рассмотрено 40 из 40, то есть 62 из 62.**

| пункт анкеты | уроков | вердикт | причина |
|---|---|---|---|
| H2 | 6 | КОНВЕРТИРОВАН (с оговоркой) | рычаг уже существует — `ГЕЙТ G16.7` (`GEJTY.md`, живёт вне моей зоны, но уже принят в канон 05.08). 🔴 Прогон его признака по единственному живому `INTERVYU.md` этого репозитория дал **0 круг-заголовков `## Круг ` и 0 строк `> «` при пороге 0≥0 — гейт вакуумно зелёный**, потому что файл записан ТАБЛИЦЕЙ кругов с инлайн-цитатами, а не отдельными `## Круг N` секциями с цитатой строкой `> «…»`. Рычаг назван верно, но не проверен на практике — см. `УРОКИ ФАБРИКЕ` этого захода. |
| G2 | 6 | ПРЕДЛОЖЕН новый гейт (черновик, не внедрён) | признак возможен структурно: поле `ИЛЛЮСТРАЦИЯ: да` + непустое `ТЗ:` (что/сколько/не-рисовать/размер) у карточки части 2 контракта. Грепом по живым проектам (`teorkat-vvedenie`, `buffon`, `dandelin`, `fibonacci`) поля `ИЛЛЮСТРАЦИЯ:`/`ТЗ:` — **0 совпадений везде**: поле ещё не часть формата карточки (`DOK.md` часть 2 сейчас несёт только ВОПРОС/ОТЛИЧИЕ/ОПИРАЕТСЯ/ВВОДИТ/ОТКУДА/ВРЕМЯ). Черновик — ниже в этом файле; сам гейт `G16.9` живёт в `GEJTY.md`, а этот файл вне моей зоны — перенос за аналитиком. |
| J4 | 4 | не переводится | «читал ли я живые файлы перед ответом» — состояние ума интервьюера в моменте; слабый прокси (грепать в `INTERVYU.md` путь-цитату рядом с каждым утверждением) даёт много ложных и пропусков — не признак-на-диске в смысле закона `GEJTY.md`. |
| J15 | 3 | не переводится | где граница отрицательного «без X» — суждение о содержании В МОМЕНТ ответа, не факт на диске. |
| C2 | 3 | не переводится | что считать ОДНОЙ единицей — определение вводится живым ответом владельца, не выводится из файлов до интервью. |
| H1 | 2 | не переводится | отличить «число из команды» от «число из головы» по тексту ответа нельзя без знания, была ли команда прогнана — это факт о процессе мышления, а не о тексте. |
| E1 | 2 | не переводится в этой фазе (чужой дом) | решает регистр текста arc 6 (`06-tekst`); закон должен лечь в `KONTRAKT §1` (уже так и происходит), но верифицировать соблюдение может только гейт G7 самого текстового шага — файл `GEJTY.md`/`06-tekst/DOK.md` вне зоны этого захода. |
| E7 | 2 | не переводится в этой фазе (чужой дом) | мотивировка vs определение — суждение о качестве текста, проверяемое на этапе текста (G3/G7), не в момент интервью. |
| D2 | 2 | не переводится в этой фазе (чужой дом) | нижняя граница плотности — решение владельца, которое лечит `KONTRAKT`; носитель проверки — гейт вёрстки (`G8`), вне зоны. |
| A1 | 2 | частично — структурный гейт уже есть, вопрос по существу нет | сам ЖАНР («глазами или вслух») — суждение, признака-на-диске для него нет. Но G16 УЖЕ печатает `⚠ дек в раскадровке без утверждённого контракта` при начатой арке 5 без `KONTRAKT-*.md` — то есть структурная страховка «поздно спохватились» существует, просто не про САМ вопрос. |
| J6 | 1 | не переводится в этой фазе (чужой дом) | адресация правок заголовком — дисциплина фазы правок (`raskadrovka`/`verstka`), не интервью. |
| J7 | 1 | не переводится в этой фазе (чужой дом) | приоритет правок по цене — дисциплина фазы правок. |
| H5 | 1 | не переводится | записка vs спецификация — суждение о жанре ВХОДЯЩЕГО документа в моменте. |
| J1 | 1 | не переводится | язык вопроса — владельца или внутренний арки — самопроверка интервьюера в реальном времени, следа не оставляет. |
| J3 | 1 | не переводится | ширина vs глубина — суждение о темпе разговора в моменте. |
| J2 | 1 | не переводится | все ли термины определены до показа формулировки — суждение о читателе в моменте предъявления. |
| H4 | 1 | не переводится | кто сузил рамку — вопрос об истории диалога, а не факт на диске. |
| J5 | 1 | не переводится | принадлежит ли вопрос текущей фазе — граница арки, суждение аналитика. |
| H3 | 1 | не переводится | гипотеза проверена или нет — состояние знания интервьюера, не текст. |
| J14 | 1 | не переводится | с чего начинать показ — суждение о драматургии показа в моменте. |
| E5 | 1 | не переводится в этой фазе (чужой дом) | перечень: узнавание или объяснение — вопрос формата текста, проверяется на этапе текста. |
| E2 | 1 | не переводится в этой фазе (чужой дом) | на артефакте vs вслух — решение ложится в `KONTRAKT`, но соблюдение проверяет гейт текстового шага, не интервью. |
| E4 | 1 | не переводится | существуют ли в ЭТОМ артефакте жанровые ярлыки — решение о конкретном жанре, не факт на диске до принятия. |
| E6 | 1 | не переводится | актуальность списка забракованных оборотов — суждение аналитика о релевантности старого списка новому материалу. |
| E3 | 1 | не переводится в этой фазе (чужой дом) | обязателен ли заголовок — решение ложится в `KONTRAKT`, соблюдение проверяет гейт текстового/вёрсточного шага. |
| J16 | 1 | не переводится | что доказываем, что объявляем — граница «очевидно» для ЭТОГО зала, суждение в моменте. |
| J12 | 1 | не переводится в этой фазе (чужой дом) | что из сказанного обязано попасть в дек — сверяется на этапе раскадровки по факту готового текста, не в момент интервью. |
| J13 | 1 | не переводится в этой фазе (чужой дом) | перечитать список вслух на повторы — акт живого чтения на этапе раскадровки, не интервью. |
| C7 | 1 | не переводится | признак попадания/непопадания элемента в перечень — определяется живым ответом, не выводится заранее. |
| C6 | 1 | не переводится | какая ОДНА мотивация у факта — содержательное решение владельца, не факт на диске. |
| B2 | 1 | не переводится | по какой величине сверять габарит (сцены vs плотность) — методологический выбор, не факт для грепа. |
| J8 | 1 | не переводится в этой фазе (чужой дом) | цель сжатия в минутах, не в слайдах — поле-носитель должно жить в `brief.md` арки 6/7 (сжатие), не в контракте интервью. |
| J9 | 1 | не переводится в этой фазе (чужой дом) | граница честного сжатия — измеряется на готовом тексте гейтом арки 6, не на этапе интервью. |
| D1 | 1 | не переводится в этой фазе (чужой дом) | слайд = один экран — закон уже есть в `DOK.md` текстового шага; проверка — гейт вёрстки (`G8`/`G9`), вне зоны. |
| D3 | 1 | не переводится в этой фазе (чужой дом) | «кратко» = мало содержания vs много кирпичиков — решение ложится в `KONTRAKT`, соблюдение проверяет этап текста. |
| J11 | 1 | не переводится | один потребитель артефакта или два (зал и лектор) — содержательное решение о том, что должно быть НА артефакте ради лектора; суждение, не факт. |
| J10 | 1 | не переводится | кто называет раскладку — решение о разделении труда, не факт на диске. |
| F3 | 1 | не переводится в этой фазе (чужой дом) | накопление vs замена по умолчанию — параметр движка вёрстки, гейт для него (если появится) — в `GEJTY.md`/арке 8, не в интервью. |
| F1 | 1 | не переводится в этой фазе (чужой дом) | наличие такта «вопрос залу» — проверяется на готовой раскадровке (кандидат для будущего `G13`-подобного гейта), не в момент интервью. |
| C5 | 1 | не переводится | порядок изложения (определение до применения) — содержательное решение о конкретном материале, не факт на диске. |

**Итог перевода:**

- Конвертирован (с оговоркой, найден побочный дефект рычага): **1 пункт, 6 уроков** (`H2`).
- Предложен новый гейт-черновик, не внедрён (нужен ход аналитика в `GEJTY.md`): **1 пункт, 6 уроков** (`G2`).
- Частичная структурная страховка уже есть, но не про суть вопроса: **1 пункт, 2 урока** (`A1`).
- Не переводится в фазе 4.5 — рычаг честно принадлежит ДРУГОЙ фазе (текст/вёрстка/сжатие/раскадровка), не интервью: **16 пунктов, 19 уроков**.
- Не переводится вовсе — суждение в реальном времени разговора, признака-на-диске нет и выдумывать его запрещено законом `GEJTY.md`: **21 пункт, 29 уроков**.

**Число уроков с рычагом `АНКЕТА` после перевода: 62 − 6 (`H2` → `ГЕЙТ G16.7`) = 56 — строго меньше 62.** Критерий №3 закрыт честно: сокращение на один пункт, не на все 40, — ровно то самое «перевести все 62 нельзя», которое заход называет реалистичным ожиданием сам.

## Часть D-примечание · черновик предлагаемого гейта G16.9 (иллюстрация — ТЗ, а не просьба)

> Не внедрён: `GEJTY.md` — общий реестр гейтов всей фабрики, вне зоны этого захода (`_studio/konvejer/GEJTY.md`,
> сосед `04.5-intervyu/`, не его часть). Черновик — чтобы аналитику не пришлось формулировать заново;
> перенос в `GEJTY.md` и в формат карточки `DOK.md` части 2 — отдельным ходом аналитика.

**G16.9 (черновик) · иллюстрация в KONTRAKT несёт ТЗ, а не просьбу.**
Что проверяет: если карточка части 2 отмечена как нуждающаяся в иллюстрации, у неё заполнено ТЗ —
что изображено · сколько объектов и как подписаны · что происходит · чего рисовать НЕ надо · размер
(пять полей `АНКЕТА G2`, дословно).
Признак-на-диске (предложение): в карточке part2 поле `ИЛЛЮСТРАЦИЯ: да` ⇒ в тех же ~10 строках
непустое поле `ТЗ:`, и внутри него не менее трёх из пяти маркеров-подпунктов (что/сколько/не-рисовать/размер/подписи).
**Замер 2026-08-05, тем же ходом (закон GEJTY.md «признак пишется грепом»):**
`grep -rc '^ИЛЛЮСТРАЦИЯ:\|^ТЗ:' teorkat-vvedenie buffon dandelin fibonacci` → **0 вхождений во всех
четырёх** — поле нигде не существует, формат карточки его пока не предусматривает (`DOK.md` часть 2
несёт только ВОПРОС/ОТЛИЧИЕ/ОПИРАЕТСЯ/ВВОДИТ/ОТКУДА/ВРЕМЯ). Значит на всех живых деках гейт был бы
`N/A` (по образцу N/A у G7/G16 для декоративного случая «поле не существует», не FAIL) — ложных ❌ ноль,
но и толку ноль, пока поле не заведено. Первый шаг — не гейт, а поле в `DOK.md §Контракт часть 2`.


## Гейт-против-охвата (обновлено этим заходом, 2026-08-05) — что закрыто, что осталось честной оговоркой

🔴 **Дыра прошлой версии закрыта.** Прошлая редакция этого раздела называла 242 записи класса П/Т/Д
корпуса «уроки арок» неитемизированными (только сумма из `DOK.md`, без адреса и цены). Это и был
главный дефект охвата, который чинит `## Раздел 5` этого захода: скриптом `sobrat_karkas_faz.py urokov`
из полных 316 `### `-секций `*/UROKI-FABRIKE.md` вычтены 73 уникальные секции, покрытые классом И
(Раздел 3, 74 цитаты — у одной секции их две, отсюда 74 цитаты → 73 секции), остаток **243** разобран
по адресу и сведён в группы по механизму (метод `KRATNOST.md`) — poштучно, как и было условлено критерием
готовности №1 этого захода.

**Охват этой картотеки теперь: 4 из 4 корпусов, все 4 — поштучно.**

| корпус | заявлено | покрыто поштучно | как |
|---|---:|---:|---|
| «кандидаты исполнителей» (`skelet-ispolnitelej.tsv`) | 461 | **461** (100 %) | Раздел 1, join по адресу `KRATNOST.md` ↔ tsv, 0 непроматченных |
| «реплики владельца» (`skelet-vladelca.tsv`) | 1379 | **1379** (100 % по адресу; 1144 = 83 % из них дополнительно сведены к короткому `V`-id — 235 адресов `KRATNOST-vladelca.md` ведут на `SESSIYA.md`/иные файлы шире строгого `V0001…V1379`, что честно названо, не натянуто, и не мешает фазовому разносу: адрес сам по себе — устойчивый id) | Раздел 2 |
| «уроки арок» (`*/UROKI-FABRIKE.md`, минус 11 заглушек) | 316 | **316** (100 %: 73 секции в Разделе 3 + 243 в Разделе 5) | Раздел 3 (класс И, унаследовано) + Раздел 5 (новое) |
| «автолог git» (`_INFRA-git/INCIDENTY.md`) | 107 (на дату сборки; растёт) | **107** (100 %) | Раздел 4, пересчёт `RAZBOR-povtorov.md §6` |
| **ИТОГО (уникальные записи 4 корпусов)** | 461+1379+316+107 | **2263** (100 %) | — |

🔴 **Найдено независимым верификатором (свежий субагент, другой метод — прямой пересчёт из сырых
файлов, а не доверие тексту картотеки): `srez_po_faze.py` без аргументов печатает ИТОГО = 2264, а
не 2263.** Расхождение РЕАЛЬНОЕ и вот его точная причина, не путать со старой (ошибочной)
версией этого абзаца, которая ссылалась на рост git-лога: `srez_po_faze.py` считает Раздел 3 по
СТРОКАМ (74 — сквозная нумерация `И-01`…`И-74` из `POKRYTIE.md`, unit = цитата класса И), а не по
уникальным секциям урока (73 — см. абзац выше «у одной секции их две»). Складывая построчно
Раздел3(74 строк)+Раздел5(243 строки) = 317 вместо истинных 316 уникальных секций «уроки арок»,
скрипт даёт на единицу больше. **Верное число покрытых ИСХОДНЫХ ЗАПИСЕЙ корпуса — 2263** (таблица
выше); **2264 — это число СТРОК-ЦИТАТ** в объединении всех 5 разделов (учитывает одну секцию урока
дважды, потому что она несёт два разных подкласса И). Обе интерпретации законны для разных вопросов
(«сколько исходных записей покрыто» → 2263; «сколько строк в таблицах картотеки» → 2264), но
критерий готовности №2 («сколько записей корпуса покрыто») отвечается числом **2263**.

**Единственная оставшаяся честная оговорка (не «дыра», а огрублённая, а не поштучная разбивка одного
куска):** 131 находка `KRATNOST.md#Разное` в Разделе 1 сведена не в 131 именованную мехническую
подгруппу (как первые 152 группы `KRATNOST.md`), а в 10 групп ПО ФАЗЕ напрямую — полный список всех
131 адреса при этом сохранён (см. `КРТ-РАЗН · <фаза>` строки), ни один не потерян и не задвоен,
просто механизм каждой находки внутри фазы не назван отдельно (он не нужен для задачи «забрать пачку
под фазу»). Если понадобится механизм каждой находки — он есть в `KRATNOST.md#Разное` по тому же
адресу.

## Часть D (этот заход) · Как забрать пачку под фазу

**Инструмент — `srez_po_faze.py`** в этой же папке (не руками, не грепом по одной фазе построчно:
таблицы трёх разных форм — Раздел 3 и 4 несут фазу в другой колонке, чем Раздел 1/2/5).

```bash
cd _studio/zhurnal/2026-07-30_dovodka-fabriki
python3 srez_po_faze.py                 # сводная таблица чисел по всем 12 значениям фазы
python3 srez_po_faze.py 07-verstka      # список строк (всех 5 разделов), относящихся к фазе
```

**Таблица чисел (пересчитано этой командой 2026-08-05):**

| фаза | Σ кратность (сколько исходных записей) |
|---|---:|
| `вне-фаз` | 724 |
| `02-reserch` | 312 |
| `06-tekst` | 273 |
| `05-raskadrovka` | 172 |
| `04.5-intervyu` | **146** (строго больше 74 — критерий готовности №4 закрыт) |
| `01-brief` | 117 |
| `09-illustracii` | 107 |
| `04-gibrid-istochnik` | 103 |
| `03-matbaza` | 98 |
| `08-sceny` | 84 |
| `07-verstka` | 66 |
| `10-sborka-qa` | 62 |
| **ИТОГО (строк-цитат)** | **2264** — см. `## Гейт-против-охвата`: верное число исходных записей **2263**, `04.5-intervyu` в строках-цитатах 146, в исходных записях 145 (74→73 в Разделе 3), разница та же +1 |

Для чистого grep (без питона, если нужен) — таблицы Раздела 1/2/5 несут фазу вторым столбцом в
обратных кавычках: `grep -c '| \`06-tekst\`' KARTOTEKA-problem.md` даёt число СТРОК (групп), не сумму
кратности — для итогового числа записей нужен `srez_po_faze.py` (кратность у групп разная, от 1 до 26).

