# Карточка репозитория, жизненный цикл, папки и связи: как это устроено в мире

Веб-исследование, 25.09.2026. Всё читалось с живых страниц в этот день. Пометки:
- **[сверено]**: цитата или факт сняты со страницы по указанному URL в этот день;
- **[вторичный источник]**: пересказ третьей стороны, не первоисточник;
- **[не сверено]**: по памяти или выведено мной, по источнику не проверялось.

---

## 1. Файлы-описатели проекта в корне репозитория

### 1.1 Backstage `catalog-info.yaml` (Spotify / CNCF)
Источник: https://backstage.io/docs/features/software-catalog/descriptor-format , https://backstage.io/docs/features/software-catalog/

- Идея: «the source of truth for the components in your software catalog are metadata YAML files stored in source control». Каталог сам собирает эти файлы и показывает их; изменения в репо попадают в каталог автоматически **[сверено]**.
- Где лежит: «Usually the metadata file is located in the repository root. This is not a formal requirement» **[сверено]**.
- Верхний уровень: `apiVersion` (напр. `backstage.io/v1alpha1`), `kind`, `metadata`, `spec` **[сверено]**.
- `kind`: Component, API, Resource, System, Domain, Group, User, Location, Template **[сверено]**.
- `metadata`:
  - `name` (обязательно): от 1 до 63 символов, `[a-z0-9A-Z]` с разделителями `-_.`; уникален в пределах kind+namespace **[сверено]**;
  - `namespace` (по умолчанию `default`), `title` (отображаемое имя), `description`;
  - `labels` (ключ-значение, для классификации), `annotations` (ссылки во внешние системы, строки);
  - `tags`: список строк `[a-z0-9:+#]` через `-`, не длиннее 63 символов **[сверено]**;
  - `links`: список `{url (обяз.), title, icon, type}` **[сверено]**.
- `spec` (для Component): `type` (свободная строка: «organizations should establish proper classification»), `lifecycle`, `owner`, `system`, `dependsOn` **[сверено]**.
- `owner`: ссылка на сущность-владельца, «the singular entity (commonly a team) that bears ultimate responsibility» **[сверено]**.
- Ссылки между сущностями записываются строкой `[<kind>:][<namespace>/]<name>`, напр. `group:pet-managers` (https://backstage.io/docs/features/software-catalog/references) **[сверено]**.
- `relations` вычисляет сам каталог и хранит `{targetRef, type}`. Типы связей (https://backstage.io/docs/features/software-catalog/well-known-relations): `ownedBy/ownerOf`, `partOf/hasPart`, `dependsOn/dependencyOf`, `memberOf/hasMember`, `parentOf/childOf`, `providesApi`, `consumesApi` **[сверено]**.

Главный урок: в файле пишут только **прямые** связи (`owner`, `system`, `dependsOn`), а **обратные** (`ownerOf`, `hasPart`) строит агрегатор. Для личного портфеля это значит: `related:` пишем в одном репо, а обратную ссылку вычисляет скрипт, а не человек.

### 1.2 `publiccode.yml` (стандарт для открытого ПО госсектора, Италия и др.)
Источник: https://publiccodeyml.readthedocs.io/en/latest/schema.core.html , https://github.com/publiccodenet/publiccode.yml
- Ключи: `publiccodeYmlVersion`, `name`, `url` (URL репозитория и есть уникальный идентификатор), `landingURL`, `isBasedOn`, `softwareVersion`, `releaseDate`, `platforms`, `categories` (из **контролируемого словаря**), `developmentStatus`, `softwareType`, `description.<язык>.{shortDescription (≤150 символов), longDescription, features}`, `legal`, `maintenance.{type, contacts}`, `localisation`, `dependsOn`, `usedBy`, `roadmap` **[сверено]**.
- `developmentStatus`: `concept | development | beta | stable | obsolete` **[сверено]**. У `obsolete` определение такое: «no longer maintained… source code is archived and kept for historical reasons» (по выдаче поиска, цитата из спецификации) **[сверено по двум источникам]**.
- `maintenance.type`: `internal | contract | community | none` **[сверено]**.
- Полезно взять: краткое описание с жёстким лимитом длины, описания по языкам и **категории из закрытого списка**.

### 1.3 CodeMeta `codemeta.json`
Источник: https://codemeta.github.io/terms/
- Это JSON-LD на основе словаря schema.org. Термины: `name`, `description`, `dateCreated`, `dateModified`, `datePublished`, `author`, `contributor`, `maintainer`, `keywords`, `codeRepository`, `relatedLink`, `isPartOf`, `hasPart`, `license`, `identifier`, `applicationCategory`, `funder` **[сверено]**.
- `developmentStatus`: «See repostatus.org», то есть словарь статусов CodeMeta берёт из repostatus **[сверено]**.
- Полезно: `dateCreated` и `dateModified` отдельными полями, `isPartOf`/`hasPart` для связи «курс → лекция», `relatedLink`.

### 1.4 `CITATION.cff`
Источник: https://citation-file-format.github.io/ , https://github.com/citation-file-format/citation-file-format/blob/main/schema-guide.md
- «plain text file with human- and machine-readable citation information for software (and datasets)» **[сверено]**.
- Базовые ключи (по примеру на сайте): `cff-version`, `message`, `title`, `authors`. Список обязательных полей по спецификации **[не сверено]** (страница схемы при чтении обрезалась).
- Необязательные ключи: `abstract`, `keywords`, `date-released`, `repository-code`, `url`, `license`, `identifiers`, `references`, `type`, `preferred-citation`. У человека есть поля `given-names`, `family-names`, `alias`, `orcid`, `affiliation`, `email` **[сверено]**.
- GitHub сам показывает на странице репо файл из корня основной ветки и генерирует BibTeX **[сверено]**.

### 1.5 `.github/`
Источник: https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file
- Здесь лежат CODE_OF_CONDUCT, CONTRIBUTING, FUNDING.yml, SECURITY, SUPPORT, шаблоны issue и PR. Описательных метаданных проекта в `.github/` **нет** **[сверено]**. Для карточки эта папка не подходит.
- «Темы» (topics) GitHub хранятся не в файле, а в настройках репо: «lowercase letters, numbers, and hyphens», не длиннее 50 символов, не больше 20 штук (https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics) **[сверено]**.
- Флаг «archived» тоже хранится только на стороне GitHub (см. §2.3).

### 1.6 `package.json` и похожие манифесты
Источник: https://docs.npmjs.com/cli/v10/configuring-npm/package-json
- Описательные поля: `name` (строчные буквы, безопасен для URL, не длиннее 214 символов), `version`, `description`, `keywords`, `homepage`, `bugs`, `license`, `author`, `contributors`, `funding`, `repository`. Человек записывается как `{name, email, url}` или строкой `"Name <email> (url)"` **[сверено]**.

### 1.7 Front matter в README
Источник: https://jekyllrb.com/docs/front-matter/
- YAML-блок между строками `---`, который «must be the first thing in the file» **[сверено]**. Есть готовые поля (`date`, `tags`, `categories`), можно добавлять свои.
- Плюс: карточка и README становятся одним файлом. Минус: GitHub покажет этот YAML как часть README. Про yq: «only processes the first passed in file for front-matter» (https://mikefarah.gitbook.io/yq/usage/front-matter) **[сверено]**, так что массово собирать данные удобнее из отдельного `.yaml`.

### 1.8 Какие поля повторяются

| Смысл | Backstage | publiccode | CodeMeta | CFF | package.json |
|---|---|---|---|---|---|
| машинное имя / ID | metadata.name | url | identifier | (doi в identifiers) | name |
| человекочитаемое название | title | name | name | title | — |
| краткое описание | description | shortDescription | description | abstract | description |
| теги / ключевые слова | tags | categories | keywords | keywords | keywords |
| тип | spec.type | softwareType | applicationCategory | type | — |
| статус | spec.lifecycle | developmentStatus | developmentStatus | — | — |
| владелец / автор | spec.owner | maintenance.contacts | author/maintainer | authors | author |
| соавторы | (группы) | — | contributor | authors | contributors |
| ссылки | links | landingURL | relatedLink | url | homepage |
| часть чего / связи | system, dependsOn | dependsOn, isBasedOn | isPartOf, hasPart | references | — |
| даты | — | releaseDate | dateCreated/Modified | date-released | — |

Источники в строках таблицы те же, что в §1.1–1.6. Сводка моя.

**Что из этого годится для личного портфеля, где много не-программных проектов (курсы, лекции, исследования, сайты):** ID, название, краткое описание (с лимитом длины), тип работы, статус, теги из закрытого словаря, владелец и соавторы, ссылки, «часть чего» и связанные проекты, даты. Лицензия, версия, платформы, зависимости и API для такого портфеля в основном шум. Их можно добавить только сайтам и инструментам **[вывод мой]**.

---

## 2. Словари статусов жизненного цикла

### 2.1 repostatus.org (8 состояний)
Источник: https://www.repostatus.org/ **[сверено, дословно]**
- **Concept**: «Minimal or no implementation has been done yet, or the repository is only intended to be a limited example, demo, or proof-of-concept.»
- **WIP**: «Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.»
- **Suspended**: «Initial development has started, but there has not yet been a stable, usable release; work has been stopped for the time being but the author(s) intend on resuming work.»
- **Abandoned**: «Initial development has started, but there has not yet been a stable, usable release; the project has been abandoned and the author(s) do not intend on continuing development.»
- **Active**: «The project has reached a stable, usable state and is being actively developed.»
- **Inactive**: «The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.»
- **Unsupported**: «The project has reached a stable, usable state but the author(s) have ceased all work on it. A new maintainer may be desired.»
- **Moved**: «The project has been moved to a new location, and the version at that location should be considered authoritative.»
- Статус предлагают показывать бейджем в README.

Устройство: статусы сидят на двух осях, «достигнут ли пригодный результат» × «идёт ли работа / есть ли намерение продолжать». Отдельного статуса **«завершено, всё сделано»** нет. Поиск по issues репозитория jantman/repostatus.org по слову «complete» нашёл только #33 (метрики устаревания, открыт) и #19 («non project» repos, закрыт) (https://github.com/jantman/repostatus.org/issues?q=is%3Aissue+complete) **[сверено]**. Ближайшие к «сделано» статусы: **Inactive** (результат есть, развитие остановлено, поддержка по мере сил) и **Unsupported** (результат есть, работа прекращена) **[вывод мой]**.

### 2.2 Backstage `spec.lifecycle` (3 значения)
Источник: https://backstage.io/docs/features/software-catalog/descriptor-format **[сверено]**
- **experimental**: «An experiment or early, non-production component…»
- **production**: «An established, owned, maintained component»
- **deprecated**: «A component that is at the end of its lifecycle, and may disappear at a later point»
- Набор для эксплуатации сервисов. Паузы здесь нет, есть только «ранний / рабочий / уходящий».

### 2.3 Флаг «archived» на GitHub
Источник: https://docs.github.com/en/repositories/archiving-a-github-repository/archiving-repositories **[сверено]**
- Репо становится только для чтения: issues, PR, код, метки, релизы, ветки и т. д. Изменения возможны только после разархивации: «To make changes in an archived repository, you must unarchive the repository first.» Архивные репо находятся поиском.
- Флаг бинарный и живёт на сервере. Отличить «сделано» от «брошено» он не может, это только замок от записи.

### 2.4 Другие словари
- schema.org `creativeWorkStatus`: «The status of a creative work in terms of its stage in a lifecycle. Example terms include Incomplete, Draft, Published, Obsolete.» Тип значения `DefinedTerm` или `Text`, словарь выбирается свой (https://schema.org/creativeWorkStatus) **[сверено]**. Из всех словарей этот ближе всего к лекциям и курсам.
- publiccode `developmentStatus`: concept / development / beta / stable / obsolete (§1.2).
- GTD, «Someday/Maybe»: список идей и проектов, которые «not currently active but worth revisiting», его просматривают на еженедельном обзоре (https://hamberg.no/gtd , https://www.any.do/blog/getting-things-done-gtd-a-complete-beginners-guide-to-david-allens-system/) **[вторичный источник]**.

### 2.5 Сведение к трём состояниям владельца

| Три состояния | repostatus | Backstage | publiccode | GitHub | schema.org creativeWorkStatus |
|---|---|---|---|---|---|
| **активен сейчас** | WIP, Active (и Concept, если реально работаешь) | experimental, production | development, beta, stable | не archived | Draft / Incomplete |
| **завершён и в архиве** (сделано) | Inactive / Unsupported (с оговоркой, см. ниже) | deprecated (тоже не точно) | obsolete (с оговоркой) | archived = true | Published |
| **начат, на паузе, может вернуться** | **Suspended** (точное совпадение), иногда Concept | нет аналога | нет аналога | не archived | Incomplete |
| (брошен без намерения вернуться) | Abandoned | — | — | обычно archived | — |

Выводы **[вывод мой, опирается на определения выше]**:
1. **«Сделано» и «брошено» в стандартах разделены, и это нужно сохранить.** В repostatus граница проходит по признаку «достигнут пригодный результат»: Abandoned бывает только *до* пригодного результата, Inactive и Unsupported только *после*. У лекции, курса или сайта, прочитанного либо запущенного и закрытого, результат есть, значит это «сделано». «Брошено» бывает только у проекта без результата.
2. Точное соответствие «паузе» есть только у repostatus: **Suspended**, где решающее условие — «intend on resuming». У Backstage и publiccode паузы нет, их модель — работающий сервис.
3. Архивный флаг GitHub нельзя считать источником статуса. Он бинарный, живёт на сервере и не отличает «сделано» от «брошено». Правильнее сделать наоборот: статус записан в карточке, а флаг на GitHub (если вообще нужен) выставляется по нему.
4. Кроме статуса стоит завести поле **`status_reason` / `resume_when`** для паузы: условие или дату возврата. Без него «пауза» тихо превращается в «брошено». Это аналог обзора Someday/Maybe в GTD.
5. Словари repostatus и Backstage заточены под программы. Для лекций и курсов разумнее собственный маленький закрытый словарь из трёх значений, где у каждого значения записано соответствие repostatus (как `developmentStatus` в CodeMeta ссылается на repostatus).

---

## 3. Личные системы раскладки по папкам

### 3.1 PARA (Тьяго Форте)
Источники: https://fortelabs.com/blog/para/ **[сверено]**, https://thomasjfrank.com/productivity/books/the-para-method-by-tiago-forte-summary-and-book-notes/ **[вторичный источник]**
- **Projects**: «short-term efforts… that you take on with a certain goal in mind». В книге критерий такой: «A goal with a deadline» (вторичный источник).
- **Areas**: «important parts of your work and life that require ongoing attention».
- **Resources**: темы, которые интересны и изучаются.
- **Archives**: «anything from the previous three categories that is no longer active, but you might want to save for future reference». В архив идут «Projects you've completed **or put on hold**», переставшие быть актуальными области и ресурсы, к которым пропал интерес **[сверено]**.
- Принцип: раскладка «по степени готовности к действию» (actionability), а не по теме. Из архива проекты возвращают («Unarchive dormant projects that have become relevant again», вторичный источник).
- **Слабое место для нашей задачи:** PARA кладёт в одну корзину «завершённое» и «приостановленное». Три состояния владельца папками PARA не различаются, различить их можно только полем статуса.

### 3.2 Johnny.Decimal (Джонни Нобл)
Источники: https://johnnydecimal.com/10-19-concepts/11-core/11.01-introduction/ , https://forum.johnnydecimal.com/t/active-vs-inactive-vs-archives/1561 **[сверено]**
- Три уровня: **области** `10–19`, `20–29`…, **категории** `11`, `12`…, **ID** `11.01`. Предел: не больше 10 областей, 10 категорий в области и 100 ID в категории. Глубже трёх уровней не вкладывают: «When you start looking for something, there's no more than 10 area folders to choose from.»
- Для каждого места ведут индекс (JDex).
- Архив: автор советует держать в каждой категории ID **`.09 Archive`** и складывать туда «Just find the closest category and dump it in the `.09` folder… will, therefore, be a mess. That's okay.» Номер-адрес при этом не меняется, вещь остаётся внутри своей категории (сверено по пересказу ветки форума).
- Пользователи жалуются, что в чистом JD «there is not an obvious way to archive older files» и готовый проект так и висит наверху списка. Поэтому JD часто совмещают с PARA (https://help.noteplan.co/article/155-how-to-organize-your-notes-and-folders-using-johnny-decimal-and-para , https://lucaf.eu/2023/02/23/luca-decimal.html) **[вторичный источник]**.

### 3.3 Раскладка «по типу работы или инструменту»
- Ближайший классический аналог — **контексты GTD** (`@computer`, `@calls`, `@errands`). Дэвид Аллен объясняет их так: «most of those actions require a specific tool or location… Context is also the first criterion that limits your options and keeps you from being reminded of things you simply can't do» (https://gettingthingsdone.com/2010/09/david-allen-on-why-sorting-your-lists-by-contexts-even-matters/) **[сверено]**. Контексты можно делить и по режиму работы, например `@Coding` (по пересказу в выдаче) **[вторичный источник]**.
- Это ровно логика «сайты (код + вёрстка + дизайн) отдельно от математики (книги, программы курсов)»: папка отвечает на вопрос «что я могу делать сейчас с этим набором инструментов и в этом режиме головы».
- Для сравнения: инструменты вроде **ghq** раскладывают клоны механически, `~/ghq/<host>/<owner>/<repo>` (https://github.com/x-motemen/ghq) **[сверено]**. Смысла в такой раскладке ноль, зато нет ни одного решения и не бывает споров, куда класть.

### 3.4 Плюсы и минусы для папки с git-репозиториями [вывод мой]

| Схема | Плюсы | Минусы | Пауза |
|---|---|---|---|
| PARA | простая; активное сверху | «сделано» и «на паузе» в одной корзине; переезд между папками = переезд репо на диске (ломаются пути, скрипты, закладки IDE) | в Archives, неотличимо от завершённых |
| Johnny.Decimal | стабильные короткие номера-адреса; предел 10×10 держит порядок | номер надо назначать вручную; нужен индекс; архив внутри категории | остаётся на месте или в `.09` |
| По типу работы (контексты) | совпадает с тем, как реально садишься работать; одна ось, спорных случаев мало | проект смешанного типа (сайт курса) требует решения; статус из папки не виден | не видна по папке |
| ghq-подобная (по хосту) | ноль решений | ничего не говорит о содержании | не видна |

**Главный вывод для репозиториев:** git-репо дорого перемещать, в отличие от заметок: ломаются пути в скриптах, remote-настройки, закладки, `worktree`. Поэтому **папка должна кодировать то, что почти не меняется (тип работы), а меняющееся (статус) хранить в карточке.** Это прямо следует из принципа «Cool URIs don't change» (§6.1): статус, тему и автора не зашивают в адрес.

---

## 4. Теги против папок: фасеты и словари синонимов

### 4.1 Фасетная классификация
- Вики́ри (1960), цит. по ISKO: фасетный анализ — «The sorting of terms in a given field of knowledge into homogeneous, mutually exclusive facets, each derived from single characteristic of division» (https://www.isko.org/cyclo/facet_analysis) **[сверено]**.
- Ранганатан и Classification Research Group: у Ранганатана формула PMEST (Personality, Matter, Energy, Space, Time) и принцип «only one characteristic of division should be applied at a time» (там же) **[сверено]**.
- Wikipedia: фасеты — это «clearly defined, mutually exclusive, and collectively exhaustive aspects of a subject». Плюсы: объект можно классифицировать сразу по нескольким осям, фасеты фильтруют быстро, новый фасет добавляется без ломки старых. Минусы: некоторые понятия подходят под несколько фасетов, нотация усложняется (https://en.wikipedia.org/wiki/Faceted_classification) **[сверено]**.
- Для нашей задачи это значит следующее. Одна иерархия папок = **одна** ось деления. Всё остальное (предмет, аудитория, статус, люди) — **отдельные фасеты-поля карточки**, по одному признаку деления в каждом. Возможные оси: `kind` (тип работы), `subject` (предмет), `audience` (для кого), `status`, `venue/org` (где) **[вывод мой]**.

### 4.2 Контролируемый словарь и синонимы
- **ANSI/NISO Z39.19**: эквивалентность записывается связями USE / UF («Used For»). Каждое понятие обозначается **одним** предпочтительным термином, остальные варианты хранятся как непредпочтительные со ссылкой USE. Кроме эквивалентности есть иерархия BT/NT и ассоциация RT (https://www.luciehaskins.com/resources/Z39-19-2005.pdf , https://marciazeng.metadataetc.org/Z3919/52display.htm) **[по выдаче поиска; PDF стандарта целиком не читал]**.
- **SKOS** (W3C), https://www.w3.org/TR/skos-reference/ **[сверено]**:
  - `skos:prefLabel` бывает не больше одного на язык: «A resource has no more than one value of skos:prefLabel per language tag» (S14);
  - `prefLabel`, `altLabel`, `hiddenLabel` попарно не пересекаются (S13);
  - `hiddenLabel` нужен для опечаток и поисковых вариантов, которые не показывают;
  - `skos:broader/narrower` означают иерархию (только прямую), `skos:related` — ассоциацию, и она не пересекается с иерархией.
- SKOS Primer §2.2.2 и §2.2.3: altLabel для синонимов («creatures») и аббревиатур («FAO»), hiddenLabel для написания без диакритики («betes» при «bêtes») (https://www.w3.org/TR/skos-primer/) **[сверено]**.
- Для примера «спецмат / 179 / matclass» на SKOS это выглядит так **[иллюстрация моя]**:
  ```yaml
  # vocab/topics.yaml: один концепт, одна запись
  - id: school179-specmath        # стабильный ID, в карточках пишут только его
    prefLabel: {ru: "Спецматематика в 179"}
    altLabel:  {ru: ["спецмат", "179", "матклас"], en: ["matclass"]}
    hiddenLabel: ["specmat", "спец-мат"]
    broader: [school179]
  ```
  Карточка ссылается на `school179-specmath`. Нормализатор переводит любой altLabel или hiddenLabel в ID при генерации карточки и падает на незнакомом слове, чтобы новое слово попало в словарь, а не расползлось по карточкам.
- Риск свободных тегов: в классической работе Golder & Huberman (2006) о коллаборативном тегировании разобраны синонимия и полисемия тегов (https://journals.sagepub.com/doi/10.1177/0165551506062337). **[не сверено: наличие именно этого разбора в статье помню, по тексту не проверял]**.

### 4.3 Практика [вывод мой, опирается на источники выше]
- Для каждой оси (фасета) заводится свой закрытый список значений. Это уже делают `publiccode.categories` (контролируемый словарь) и Backstage `spec.type` («organizations should establish proper classification»).
- Формат тегов стоит сделать машинным (строчные буквы, латиница, дефис), как у GitHub topics и Backstage tags, а людям показывать prefLabel по-русски.
- Словарь синонимов живёт в **одном** файле вне репозиториев, карточки хранят только ID.

---

## 5. Как собрать карточки в одну таблицу

- **Backstage**: полноценный центральный каталог, который сам собирает `catalog-info.yaml` из репо (https://backstage.io/docs/features/software-catalog/) **[сверено]**. Для одного человека и нескольких десятков репо это тяжело: нужны сервер, БД, Node **[вывод мой]**.
- **yq**: `yq -o=csv file.yml` превращает массив объектов в CSV, заголовок берётся из ключей первого объекта (https://mikefarah.gitbook.io/yq/usage/csv-tsv) **[сверено]**. Front matter читается только у первого переданного файла, значит нужен цикл по файлам (https://mikefarah.gitbook.io/yq/usage/front-matter) **[сверено]**.
- **Python-скрипт**: обходит `~/repos/**/<card>.yaml`, проверяет по схеме, раскрывает синонимы, строит обратные связи и пишет CSV/HTML/статистику. Это самый простой вариант, который полностью контролируешь **[вывод мой; источника нет, это типовая практика]**.
- **Obsidian Dataview**: «a live index and query engine over your personal knowledge base». Читает YAML front matter и инлайн-поля `[key:: value]`, умеет `TABLE … FROM #tag / "folder" WHERE … GROUP BY`, файлы при этом не меняет (https://blacksmithgu.github.io/obsidian-dataview/) **[сверено]**. Подходит, если карточки (или их копии) лежат внутри хранилища Obsidian.
- **GitHub**: поиск по topics, у archived-репо есть фильтр. Про поиск по имени файла (`filename:`) **[не сверено]**. Работает только для того, что запушено на GitHub.

---

## 6. Задел под связи: люди, темы, связанные проекты

### 6.1 Стабильные идентификаторы
- Tim Berners-Lee, «Cool URIs don't change» (https://www.w3.org/Provider/Style/URI) **[сверено]**: из идентификатора убирают то, что меняется, а именно имя автора («authorship can change»), тему и классификацию, статус («Documents change status—or there would be no point in producing drafts»), уровень доступа, расширения файлов и названия дисков. «Designing mostly means leaving information out.»
- Следствие: у проекта ID постоянный и короткий. В нём нет статуса, года, папки и темы, всё это живёт полями. Имя папки на диске может меняться, ID в карточке остаётся тем же **[вывод мой]**.
- Формат ссылки можно взять у Backstage: `kind:name` (`person:ivanov-a`, `project:fractal-odyssey`, `topic:fractals`) (https://backstage.io/docs/features/software-catalog/references) **[сверено для формата]**.

### 6.2 Люди
- schema.org `Person`: `name`, `givenName`, `familyName`, `alternateName`, `identifier`, `sameAs`, `url`, `affiliation`, `knows`, `email` (https://schema.org/Person) **[сверено]**.
- `sameAs`: «URL of a reference Web page that unambiguously indicates the item's identity. E.g. the URL of the item's Wikipedia page, Wikidata entry, or official website.» `identifier`: «any kind of identifier… such as ISBNs, GTIN codes, UUIDs» **[сверено]**.
- CFF у автора держит `orcid` и `alias`, package.json — `{name, email, url}` (§1.4, §1.6).
- Практика **[вывод мой]**: в карточке писать только `person:<id>` и роль, а сам человек (имя, варианты написания, sameAs) описывается один раз в общем `people.yaml`. Такой справочник работает как словарь синонимов из §4.2, только для людей: «Ваня», «И. Яковлев», «ivanyakovlev» ведут к одному ID.

### 6.3 Темы и проекты
- schema.org `about`: «The subject matter of an object», ожидаемый тип `Thing` (https://schema.org/about) **[сверено]**. Значит, темой может быть сущность со своим ID, а не строка.
- `CreativeWork` задаёт связи `isBasedOn`, `isPartOf`, `hasPart`, `translationOfWork` и учебные поля `educationalLevel`, `learningResourceType` (https://schema.org/CreativeWork) **[сверено]**.
- CodeMeta: `isPartOf`, `hasPart`, `relatedLink` (§1.3). Backstage: `partOf/hasPart`, `dependsOn` (§1.1). SKOS разводит иерархию (`broader`) и ассоциацию (`related`) (§4.2).
- Минимум, который стоит зарезервировать сейчас **[вывод мой]**:
  1. `id` проекта, стабильный;
  2. `people:` — список `{ref: person:<id>, role: <из закрытого списка>}`;
  3. `topics:` — список ID из словаря тем;
  4. `part_of:` — ID родителя (курс → лекция, фестиваль → станция);
  5. `related:` — список `{ref: project:<id>, rel: <тип>}`, где тип берётся из малого закрытого списка (`based_on`, `continues`, `reuses`, `same_audience`, `see_also`);
  6. обратные связи (`has_part`, «на меня ссылаются») в карточку **не пишутся**, их строит агрегатор, как `relations` в Backstage.
  Пустые списки допустимы: поле зарезервировано, заполнение потом.

---

## 7. ЧЕРНОВИК полей карточки (для обсуждения, не решение)

> Всё ниже **черновик для обсуждения**. Названия полей, словари и набор обязательных полей не утверждены. Колонка «кто заполняет»: **авто** = скрипт вычисляет из git и файлов; **агент** = ИИ-агент предлагает по содержимому репо; **владелец** = решает человек (агент может предложить, но решение за владельцем).

| Поле | Тип | Кто заполняет | Зачем / на что похоже |
|---|---|---|---|
| `card_version` | строка (`"0.1"`) | авто | версия схемы карточки, для будущих миграций (как `apiVersion`, `cff-version`) |
| `id` | строка `[a-z0-9-]`, ≤63 | владелец (агент предлагает) | стабильный ID, не меняется при переименовании папки (Backstage `name`, «Cool URIs») |
| `title` | строка | агент → владелец | человекочитаемое название (Backstage `title`) |
| `summary` | строка ≤150 символов | агент | одна фраза «что это», жёсткий лимит (publiccode `shortDescription`) |
| `kind` | enum из словаря | агент → владелец | тип работы, одна ось: `site`, `tool`, `course`, `lecture`, `research`, `event`, `sheet-set`… (Backstage `spec.type`). **Из этого поля выводится папка на диске** |
| `status` | enum: `active` / `done` / `paused` (+ `dropped`?) | владелец | три состояния владельца; вопрос, нужен ли четвёртый `dropped` (repostatus Abandoned) |
| `status_repostatus` | enum repostatus | авто (из `status`+`outcome`) | совместимость: `active`→Active/WIP, `done`→Inactive, `paused`→Suspended, `dropped`→Abandoned |
| `status_since` | дата | авто (при смене статуса) | когда статус поставлен, это «дата данных» отметки |
| `resume_when` | строка / дата | владелец | только для `paused`: условие или дата возврата (аналог обзора Someday/Maybe) |
| `outcome` | строка / ссылка | агент → владелец | что получилось (прочитан курс, запущен сайт). Отличает `done` от `dropped` (граница «stable, usable» в repostatus) |
| `created` | дата | авто (первый коммит) | CodeMeta `dateCreated` |
| `last_commit` | дата | авто | CodeMeta `dateModified`. Лучше не хранить в файле, а вычислять при агрегации (иначе устаревает) |
| `subjects` | список ID из словаря тем | агент | фасет «предмет» (schema.org `about`, SKOS concepts) |
| `audience` | список enum | агент → владелец | фасет «для кого»: школьники N класса, студенты, взрослые-научпоп, коллеги… (schema.org `educationalLevel`) |
| `tools` | список enum | агент (по файлам) | чем делается: `latex`, `python`, `html-css`, `manim`, `figma`… Помогает раскладке по типу работы |
| `org` / `venue` | список ID | агент → владелец | где или для кого: школа, фестиваль, кружок (фасет «место») |
| `owner` | `person:<id>` | авто (по умолчанию владелец) | Backstage `owner` |
| `people` | список `{ref, role}` | агент → владелец | соавторы, заказчики, лекторы; роль из закрытого списка (schema.org `contributor`) |
| `part_of` | `project:<id>` | владелец | родитель (CodeMeta/schema.org `isPartOf`) |
| `related` | список `{ref, rel}` | агент предлагает, владелец утверждает | связанные проекты с типом связи (`isBasedOn`, SKOS `related`) |
| `links` | список `{url, title, type}` | агент | сайт, презентация, запись, публикация (Backstage `links`) |
| `remote` | URL | авто (`git remote`) | CodeMeta `codeRepository` |
| `tags` | список строк `[a-z0-9-]` | агент | свободные метки сверх фасетов; нормализуются через словарь синонимов |
| `notes_for_agent` | строка | владелец | оговорки, которые агенту нельзя «исправлять» |
| `filled_by` | map поле → `auto`/`agent`/`owner` + дата | авто | происхождение значения: видно, что предложил агент и что подтвердил человек |

Открытые вопросы к черновику:
1. Нужен ли четвёртый статус `dropped` («брошено без результата»), или он растворяется в `done` + пустом `outcome`? Стандарты (repostatus) эти два состояния разделяют.
2. Какой формат: отдельный `PROJECT.yaml` (или `.card.yaml`) в корне или front matter в README? В пользу отдельного файла говорят массовая агрегация и то, что GitHub не показывает YAML в README.
3. Хранить ли `last_commit` в файле или только вычислять при агрегации? Вычислять надёжнее: не устаревает, не требует коммита.
4. Словари (`kind`, `subjects`, `audience`, `tools`, `people`) лежат в одном месте вне репо, карточки хранят только ID. Где это место?
5. Папка на диске выводится из `kind` или из группы `kind`-ов (например, «сайты и инструменты» / «математика: курсы и исследования» / «события и научпоп»)? Статус в имени папки не кодируется.
