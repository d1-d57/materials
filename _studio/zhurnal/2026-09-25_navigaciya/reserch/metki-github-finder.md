# Метки репозиториев: GitHub topics ⇄ Finder tags ⇄ Google Drive — результаты веб-исследования

Дата данных: 2026-09-25 (все URL открыты в этот день). Пометки:
- **[офиц.]** — официальная документация вендора;
- **[вторичн.]** — надёжный вторичный источник (Eclectic Light, ss64, README инструмента);
- **[косвенно]** — вывод из косвенного эксперимента/наблюдения;
- **[НЕ ПРОВЕРЕНО]** — утверждение не удалось подтвердить источником; считать открытым вопросом.

---

## 1. GitHub topics

### 1.1 Формат

| Правило | Значение | Источник |
|---|---|---|
| Алфавит | «Use lowercase letters, numbers, and hyphens.» | [офиц.] https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics |
| Длина | «Use 50 characters or less.» | там же |
| Количество | «Add no more than 20 topics.» | там же |
| Регистр | API приводит к нижнему: «Note: Topic names will be saved as lowercase.» | [офиц.] https://docs.github.com/en/rest/repos/repos#replace-all-repository-topics |
| Первый символ | Сообщение валидации в UI: «Topics must start with a lowercase letter or number, consist of 35 characters or less, and can include hyphens» (35 — старый лимит, сейчас 50). Т. е. дефис первым символом нельзя. | [вторичн., community] https://github.com/orgs/community/discussions/21592 ; https://github.com/orgs/community/discussions/142207 |
| Пробелы, `_`, `.`, `#`, `/` | Не входят в алфавит (lowercase, digits, hyphens). | [офиц.] — выводится из правила алфавита |
| Кириллица / не-ASCII | Документация прямо не говорит. Поиск через GitHub Search API `topic:русский` и `topic:中文` вернул **0 репозиториев** (при том что китайских и русских разработчиков миллионы) — сильный косвенный признак, что не-ASCII topics не принимаются. | [косвенно] проверено 2026-09-25 через `search/repositories`; **[НЕ ПРОВЕРЕНО]** прямым PUT — не делали (задача read-only) |
| Двойной дефис, дефис в конце | Документация молчит. | **[НЕ ПРОВЕРЕНО]** — избегать |

Итоговая безопасная регулярка для topic: `^[a-z0-9][a-z0-9-]{0,49}$`, не более 20 штук.

### 1.2 Приватность
- «Public and private repositories can have topics, although you will only see private repositories that you have access to in topic search results.» [офиц.] https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics
- **Важно:** «Topic names are always public, even if you create the topic from within a private repository.» (там же). Значит, имя метки на приватном репо становится видимым глобально как topic (github.com/topics/<имя>) — чувствительных слов в метки не класть.
- «Private repository content is not analyzed and does not receive topic suggestions.» (там же).
- Менять topics могут админы репозитория: «Repository admins can add any topics they'd like to a repository.» (там же).

### 1.3 REST API
- Чтение: `GET /repos/{owner}/{repo}/topics` → `{"names": [...]}`; пагинация `per_page` (max 100). [офиц.] https://docs.github.com/en/rest/repos/repos#get-all-repository-topics
- Запись: `PUT /repos/{owner}/{repo}/topics`, тело `{"names": [...]}` — **заменяет весь набор** («Pass one or more topics to replace the set of existing topics. Send an empty array ([]) to clear all topics»). Коды: 200, 404, 422 («Validation failed, or the endpoint has been spammed»). [офиц.] https://docs.github.com/en/rest/repos/repos#replace-all-repository-topics
- Также поле `topics` есть в ответе `GET /repos/{owner}/{repo}` и в списках репозиториев; в `PATCH /repos/...` topics менять нельзя: «To edit a repository's topics, use the Replace all repository topics endpoint.» [офиц.] там же (раздел Update a repository).
- Права fine-grained PAT: `PUT .../topics` — Repository permission **"Administration": write**; `GET .../topics` — **"Metadata": read**. [офиц.] https://docs.github.com/en/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens
- PUT идемпотентен и декларативен — идеален для синхронизации «из манифеста»: отправить полный список, лишнее само удалится.

### 1.4 gh CLI
- `gh repo edit [<repository>] --add-topic <strings>` / `--remove-topic <strings>` [офиц.] https://cli.github.com/manual/gh_repo_edit
- Полная замена набора — через `gh api -X PUT repos/OWNER/REPO/topics -f 'names[]=a' -f 'names[]=b'` (обёртка над REST из 1.3; синтаксис `-f 'x[]=…'` — из `gh api --help`) [офиц.] https://cli.github.com/manual/gh_api
- Список репо с фильтром: `gh repo list <owner> --topic <strings> --archived/--no-archived --visibility {public|private|internal} --limit N --json name,repositoryTopics,isArchived` [офиц.] https://cli.github.com/manual/gh_repo_list — в `--json` есть поле `repositoryTopics`. Это самый дешёвый способ одним запросом (GraphQL) получить topics всех своих репо, включая приватные.
- Поиск: `gh search repos --owner=<user> --topic=a,b --archived=false --visibility=private` [офиц.] https://cli.github.com/manual/gh_search_repos
- Архив: отдельные команды `gh repo archive` / `gh repo unarchive` [офиц.] https://cli.github.com/manual/gh_repo_edit (ссылки в «See also»).

### 1.5 Лимиты запросов
- Аутентифицированный пользователь: 5000 запросов/час (primary). Без токена — 60/час. [офиц.] https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api
- Secondary: ≤100 одновременных; ≤80 «content-generating» запросов в минуту и ≤500 в час; PUT/PATCH/POST/DELETE стоят 5 «points», GET — 1. [офиц.] там же
- Search API: 30 запросов/мин с токеном (кроме code search — 10/мин), 10/мин без токена. [офиц.] https://docs.github.com/en/rest/search/search
- Для «десятков» репо лимиты не мешают: полный проход = 1 GraphQL-запрос (`gh repo list`) + по одному PUT на реально разошедшийся репо.

### 1.6 Поиск по своим репо
- Квалификаторы: `topic:<TOPIC>`, `topics:N` / `topics:>3`, `user:<USERNAME>`, `is:private` («matches private repositories you can access»), `archived:true|false`. [офиц.] https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories
- Пример: `user:<me> topic:math is:private archived:false`.
- Оговорка: поиск — индекс, может отставать от только что сделанного PUT; для гейта «сверка» надёжнее читать `GET .../topics` или `gh repo list --json repositoryTopics`, а не search. (Общая практика; конкретной задержки индекса в документации **[НЕ ПРОВЕРЕНО]**.)

---

## 2. Custom properties, архив и другие поля GitHub

### 2.1 Custom properties — только организации
- «With custom properties, you can add metadata to repositories in your organization. You can use those properties to target repositories with rulesets.» [офиц.] https://docs.github.com/en/organizations/managing-organization-settings/managing-custom-properties-for-repositories-in-your-organization
- REST: `GET/PATCH /repos/{owner}/{repo}/properties/values` — «view the custom properties that were assigned to a repository by the organization that owns the repository». [офиц.] https://docs.github.com/en/rest/repos/custom-properties
- Типы: «text string, a single select field, a multi select field, or a true/false boolean». Имена: `a-z, A-Z, 0-9, _, -, $, #`, ≤75 символов; значения: печатный ASCII кроме `"`, ≤75 символов. [офиц.] managing-custom-properties-… (ссылка выше). Т. е. single-select «status» с фиксированным списком значений — ровно то, что нужно, но…
- …**для личного аккаунта недоступно**: вся документация и API сформулированы через «organization that owns the repository»; у user-owned репо некому определить схему свойств. Прямой фразы «not available for personal accounts» в доках нет — вывод из формулировок [офиц., вывод].
- История: repo custom properties — GA 14.02.2024 [офиц.] https://github.blog/changelog/2024-02-14-repository-custom-properties-ga-and-ruleset-improvements/ ; отдельно «organization custom properties» (свойства самих организаций внутри enterprise) — GA 13.01.2026 [офиц.] https://github.blog/changelog/2026-01-13-organization-custom-properties-now-generally-available/
- Тариф: страница планов https://docs.github.com/en/get-started/learning-about-github/githubs-plans custom properties не упоминает. Доступность на бесплатной организации (GitHub Free for organizations) — **[НЕ ПРОВЕРЕНО]** по официальному источнику. Rulesets, для которых свойства в первую очередь и задуманы, на приватных репо требуют Pro/Team/Enterprise: «Rulesets are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, and GitHub Enterprise Cloud» [офиц.] https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- Обходной путь — перенести репо в свою (бесплатную) организацию. Это меняет URL/владельца; для задачи «метки» избыточно.

### 2.2 Что есть у личного аккаунта (кроме topics)
- `description`, `homepage` — свободные строки, `PATCH /repos/{owner}/{repo}` [офиц.] https://docs.github.com/en/rest/repos/repos#update-a-repository. Типизации нет; можно использовать как «человеческое» описание, не как метку.
- `archived` (bool) — нативный флаг, фильтруется `archived:true`, `gh repo list --archived`.
- `visibility` private/public.
- Нет ни типизированных свойств, ни «статуса». Единственный структурированный классификатор у личного аккаунта — topics.

### 2.3 Archive repository
- «When a repository is archived, its issues, pull requests, code, labels, milestones, projects, wiki, releases, commits, tags, branches, reactions, code scanning alerts, comments and permissions become read-only.» «To make changes in an archived repository, you must unarchive the repository first.» Разархивация — Settings → Danger Zone. [офиц.] https://docs.github.com/en/repositories/archiving-a-github-repository/archiving-repositories
- Можно ли менять topics/description у заархивированного репо: официальная страница прямо **не говорит**; community-ответ: «If your repository is archived, it becomes read-only, so you can't edit the description or any other settings» [вторичн.] https://github.com/orgs/community/discussions/54372 . Практически исходить из того, что PUT topics на архивном репо упадёт → **сначала синхронизировать метки, потом архивировать** (или гейт должен знать: архивный репо + расхождение = нужно unarchive → sync → archive). **[НЕ ПРОВЕРЕНО]** прямым вызовом.
- Для состояния «done/архив» естественно использовать нативный `archived`, а не topic `status-archived`: он виден в UI (баннер «read-only»), фильтруется поиском и защищает от случайных правок. Finder-тег для него можно генерировать из флага (однонаправленно GitHub → Finder).

---

## 3. Finder tags (macOS)

### 3.1 Хранение
- Расширенный атрибут `com.apple.metadata:_kMDItemUserTags`: «binary property list containing a little UTF-8 text. An NSArray consisting of Strings, each containing a tag name, followed by \n, followed by the colour number». Цвета: 0 none, 1 grey, 2 green, 3 purple, 4 blue, 5 yellow, 6 red, 7 orange. Пример строки: `Red\n6`. [вторичн.] https://eclecticlight.co/2017/12/27/xattr-com-apple-metadata_kmditemusertags-finder-tags/ ; то же — https://ss64.com/mac/xattr.html
- Finder при установке тега добавляет пустой (32 байта) `com.apple.FinderInfo`, если его не было; при снятии всех тегов атрибут удаляется целиком. Старая система цветных меток живёт в `FinderInfo` с другой кодировкой цветов. [вторичн.] https://eclecticlight.co/2020/10/31/finder-tags-commonplace-metadata/ ; https://eclecticlight.co/2024/12/24/solving-finder-tag-problems/
- Цвет в имени тега хранится суффиксом `\nN`; в «чистом» имени (как его видит `mdls`) суффикса нет. При сверке с topics сравнивать **имена без суффикса цвета**.
- Официальная справка Apple: теги «work with all your files and folders, whether you store them on your Mac or keep them in iCloud»; общего лимита нет, лимит «up to seven» касается только избранных в контекстном меню. [офиц.] https://support.apple.com/guide/mac-help/tag-files-and-folders-mchlp15236/mac

### 3.2 Командная строка
- **`tag`** (jdberry/tag), `brew install tag`, текущая формула 0.10 (не deprecated, по formulae.brew.sh API на 2026-09-25) [вторичн.] https://github.com/jdberry/tag ; https://formulae.brew.sh/formula/tag
  - `tag -a|--add <tags> <path>` · `-r|--remove` · `-s|--set` (заменить набор) · `-l|--list` · `-m|--match` · `-f|--find` (через Spotlight, с `--home/--local/--network`) · `-N` без имени файла · `-g` по строке на тег.
  - «Tag names may include spaces, but the entire tag list must be provided as one parameter: 'tag1,a multiword tag name,tag3'» — список через **запятую**, значит запятая в имени тега для этого инструмента проблемна.
  - `tag --remove \* file` — снять все теги.
- **`mdls`**: `mdls -raw -name kMDItemUserTags <path>` — чтение (из индекса Spotlight). [вторичн.] https://brettterpstra.com/2017/08/22/tagging-files-from-the-command-line/
- **`mdfind`**: `mdfind "kMDItemUserTags = Green"` [вторичн.] https://ss64.com/mac/mdfind.html . Работает только по проиндексированным томам; Sequoia исключает из индекса папки `~/Library` и `/Library` [вторичн.] https://eclecticlight.co/2024/12/24/solving-finder-tag-problems/ .
- **`xattr`**: `xattr -px com.apple.metadata:_kMDItemUserTags <path>` даёт hex бинарного plist; запись `xattr -w com.apple.metadata:_kMDItemUserTags '<xml plist>' <path>` — **целиком заменяет** набор. [вторичн.] https://brettterpstra.com/2017/08/22/tagging-files-from-the-command-line/
- **Python**:
  - `osxmetadata` (RhetTbull), v1.4.1 от 2026-02-16, Python ≥3.10, **только macOS**: `md = OSXMetaData(path); md.tags = [Tag("math", FINDER_COLOR_NONE)]`; CLI `osxmetadata --set tags Foo,red file`, `--append`, `--remove`, `--list`. [вторичн.] https://github.com/RhetTbull/osxmetadata ; https://pypi.org/project/osxmetadata/
  - Без зависимостей: `plistlib` (stdlib) + `os.getxattr/os.setxattr` (есть в Python на macOS? — **[НЕ ПРОВЕРЕНО]**: в CPython `os.getxattr` объявлен «Availability: Linux», на macOS его нет) → на macOS надёжнее пакет `xattr` (PyPI) или вызов `/usr/bin/xattr` через subprocess + `plistlib.loads/dumps(fmt=FMT_BINARY)`.
- Для гейта «надёжнее читать xattr, чем mdls»: `mdls`/`mdfind` отражают индекс Spotlight (может отставать или быть выключен); xattr — истина на диске. (Вывод из устройства хранения, см. 3.1.)

### 3.3 Переживают ли теги операции
| Операция | Результат | Источник |
|---|---|---|
| git clone / push / pull | **Теряются**: «git does not include those extended attributes in a repository so they will be lost.» | [вторичн.] https://info.michael-simons.eu/2013/10/25/archiving-os-x-mavericks-tags-and-other-data-with-git/ ; решения-хуки вроде https://github.com/sooham/xattr.hooks |
| Тег на **корневой папке** репо при обычной работе (commit, pull, checkout) | Git сам каталог-корень не пересоздаёт, поэтому тег на нём локально живёт; теряется при свежем clone и при переносе без сохранения xattr. | [косвенно] вывод из того, что git не трогает xattr; **[НЕ ПРОВЕРЕНО]** экспериментом |
| Копирование в macOS между томами, Time Machine | Сохраняются; исключения — NFS, некоторые сетевые/облачные ФС и CLI-утилиты. | [вторичн.] https://eclecticlight.co/2020/10/31/finder-tags-commonplace-metadata/ |
| iCloud Drive | Синхронизируются («Tags should sync immediately when added to files in iCloud Drive folders»). iCloud/File Provider синкают только xattr с флагом `XATTR_FLAG_SYNCABLE` (суффикс `#S`), лимит ~32 КиБ на объект. | [вторичн.] https://eclecticlight.co/2024/12/24/solving-finder-tag-problems/ ; https://eclecticlight.co/2025/12/17/which-extended-attributes-does-macos-tahoe-preserve/ ; [офиц. форум] https://developer.apple.com/forums/thread/783229 |
| Google Drive | См. §4 — **не сохраняются** (по данным 2018–2019), текущий статус Drive for desktop не подтверждён. | |
| ZIP через Archive Utility / `ditto` | Сохраняет xattr (AppleDouble). | [вторичн.] https://eclecticlight.co/2018/01/12/which-file-systems-and-cloud-services-preserve-extended-attributes/ |
| `zip` (Info-ZIP) из терминала | Скорее всего теряет. | **[НЕ ПРОВЕРЕНО]** |
| rsync | На macOS ≥ Sequoia (15.4) системный `rsync` = **openrsync**; у него `-E, --extended-attributes` — «Apple specific option to copy extended attributes, resource forks, and ACLs». **Ловушка:** в upstream rsync 3.x (Homebrew) `-E` = `--executability`, а xattr — это `-X/--xattrs`. | [вторичн.] https://manp.gs/mac/1/openrsync ; https://ss64.com/mac/openrsync.html ; https://derflounder.wordpress.com/2025/04/06/rsync-replaced-with-openrsync-on-macos-sequoia/ |

### 3.4 Алфавит и лимиты Finder-тегов
- Строки UTF-8 → **кириллица и пробелы допустимы** (tag CLI явно поддерживает «multiword tag name»). [вторичн.] https://github.com/jdberry/tag ; формат — https://eclecticlight.co/2017/12/27/xattr-com-apple-metadata_kmditemusertags-finder-tags/
- Запятая — конфликтует с синтаксисом `tag` (разделитель).
- Лимита на число тегов у файла нет по документации Apple (см. 3.1); практический потолок — ~32 КиБ на синкаемые xattr в iCloud.
- Максимальная длина имени тега — **[НЕ ПРОВЕРЕНО]** (Apple не документирует).
- Регистр: Finder, по наблюдениям пользователей, объединяет теги без учёта регистра — **[НЕ ПРОВЕРЕНО]**. GitHub в любом случае всё приведёт к нижнему регистру → писать только нижним.
- Unicode-нормализация (NFC/NFD) для кириллицы с «й/ё» может давать разные байты у «одинаковых» тегов — **[НЕ ПРОВЕРЕНО]**; аргумент в пользу чистого ASCII.

---

## 4. Google Drive

### 4.1 Метки (labels) — только Workspace
- Поддерживаемые редакции для classification labels: «Frontline Starter, Frontline Standard, and Frontline Plus; Business Standard and Business Plus; Enterprise Standard and Enterprise Plus; Education Standard and Education Plus; Essentials, Enterprise Essentials, and Enterprise Essentials Plus; G Suite Business.» Личного (@gmail.com) аккаунта в списке нет. [офиц.] https://knowledge.workspace.google.com/admin/security/get-started-as-a-classification-labels-admin
- Drive Labels API: создание admin-owned меток требует «account administrator with the Manage Labels privilege»; shared labels — «closed beta that isn't currently accepting new customers». [офиц.] https://developers.google.com/workspace/drive/labels/guides/overview
- Вывод: **для личного аккаунта Drive labels недоступны** [офиц., вывод из списка редакций].

### 4.2 Что есть у личного аккаунта
- **Custom file properties** Drive API v3: `properties` (видны всем приложениям) и `appProperties` (приватные для приложения). Лимиты: ≤100 на файл, ≤30 публичных, ≤30 приватных на приложение, **≤124 байта на пару key+value**. [офиц.] https://developers.google.com/workspace/drive/api/guides/properties
- Поиск: `properties has { key='mass' and value='1.3kg' }`, папки — `mimeType = 'application/vnd.google-apps.folder'`. [офиц.] https://developers.google.com/workspace/drive/api/guides/search-files
- Ограничений по типу аккаунта для properties документация не называет [офиц.] (там же). Применимость к папкам прямо не описана — **[НЕ ПРОВЕРЕНО]** (папка — это file resource с mimeType folder, так что должно работать).
- Минус: properties **не видны в UI Drive** — только через API. Для человека в веб-интерфейсе Drive остаются только название, описание (`description`) и цвет папки. Отображение описания/цвета как «меток» — **[НЕ ПРОВЕРЕНО]** как удобный UX.

### 4.3 Сохраняет ли Drive for desktop Finder-теги
- 2018: «Google Drive … do not support extended attributes» [вторичн.] https://eclecticlight.co/2018/01/12/which-file-systems-and-cloud-services-preserve-extended-attributes/
- 2019 (Drive File Stream): теги на файлах в Drive не появлялись в разделе тегов Finder; ответ: «if the latest release of Google Drive for the Mac still drops tag information, then that is on Google». [вторичн.] https://discussions.apple.com/thread/250545995 ; также https://discussions.apple.com/thread/8267961
- Сейчас Drive for desktop в режиме streaming на macOS 12.1+ работает через Apple File Provider [офиц.] https://support.google.com/drive/answer/12178485 . File Provider умеет синхронизировать xattr с флагом `#S`, но синхронизирует ли их именно провайдер Google в облако — **[НЕ ПРОВЕРЕНО]**; свежих (2024–2026) официальных заявлений Google не нашёл.
- Практический вывод: считать, что теги на папках в Google Drive **могут локально показываться, но не доходят до облака и не переживут переустановку/другой Mac**. Проверка у себя — поставить тег, отключить/подключить аккаунт или посмотреть с другого Mac.

---

## 5. Готовые инструменты / паттерны

- **Синхронизатора Finder tags ⇄ GitHub topics не найдено.** Поиск по GitHub и вебу («sync Finder tags GitHub topics», «"GitHub topics" "Finder tags"») ничего подходящего не дал (2026-09-25).
- Декларативные GitHub-стороны (topics из файла):
  - **repository-settings/app** (Probot): `.github/settings.yml`, секция `repository:` → «A comma-separated list of topics to set on the repository: `topics: github, probot`». Синхронизирует при пуше в default-ветку. [вторичн.] https://github.com/repository-settings/app ; https://github.com/repository-settings/app/blob/master/docs/plugins/repository.md . Требует установки GitHub App; Finder не трогает.
  - **Terraform** `github_repository.topics` («The list of topics of the repository») или отдельный `github_repository_topics` (взаимоисключающие). [офиц. провайдер] https://registry.terraform.io/providers/integrations/github/latest/docs/resources/repository ; https://registry.terraform.io/providers/integrations/github/latest/docs/resources/repository_topics . Для десятков личных репо тяжеловесно.
- Мультирепо-манифесты с тегами: **mani** (`mani.yaml`: `projects: <name>: tags: [dev]`, фильтр `--tags`, `tags_expr: (prod || dev) && !test`) — теги только для выбора проектов при запуске команд, в GitHub/Finder не пишет. [вторичн.] https://github.com/alajmo/mani ; https://github.com/alajmo/mani/blob/main/docs/filtering-projects.md
- Finder-стороны: `tag`, `osxmetadata`, gist «save and restore tags» https://gist.github.com/posoo/146f97697d885bf4d6f060ccb96c5539 ; git-хуки для xattr https://github.com/sooham/xattr.hooks .
- Вывод: паттерн «манифест → оба мира» придётся писать самим (~100 строк: читать карточку, `gh api PUT topics`, `tag --set`, сверка).

---

## 6. Рекомендация

### 6.1 Источник истины — карточка внутри репо
Аргументы (по фактам выше):
1. Finder-теги **не едут с git** (§3.3) и **не едут через Google Drive** (§4.3) → не могут быть источником истины: на новом Mac / после клона их нет.
2. GitHub topics — живут на сервере, но **публичны по имени даже у приватного репо** (§1.2), не имеют истории изменений и замораживаются при архивации (§2.3).
3. Файл-карточка в репо (например `.meta/tags` или ключ `tags:` в существующем YAML) версионируется git, ревьюится, едет с клоном и доступен скрипту без сети.

Поток: `карточка → (PUT /topics) GitHub` и `карточка → (tag --set / xattr) Finder`. Гейт — три множества должны совпасть: `card == topics(GitHub) == userTags(Finder, без суффикса цвета)`; любое расхождение → красный с диффом. `archived` — отдельный нативный флаг GitHub, из карточки не пишется, а читается (или карточка лишь утверждает `status: archived`, а гейт сверяет с `isArchived`). Порядок: sync меток → потом архивирование.

Бонус: `PUT /topics` и `tag --set` — оба **заменяют набор целиком**, т. е. идемпотентны: sync = «записать полный список», без вычисления add/remove.

### 6.2 Алфавит, работающий в обоих мирах
Пересечение ограничений (GitHub строже во всём):
- регулярка: **`^[a-z0-9][a-z0-9-]{0,49}$`** (латиница в нижнем регистре, цифры, дефис; первый символ не дефис) [офиц. §1.1 + community про первый символ];
- **≤ 20** меток на репо [офиц.];
- без кириллицы (GitHub, [косвенно]), без пробелов/подчёркиваний/точек (GitHub), без запятых (tag CLI);
- рекомендуем дополнительно: без `--` и без дефиса в конце ([НЕ ПРОВЕРЕНО] — страховка), без чувствительных слов (topic публичен);
- цвет Finder-тегов в GitHub не отражается → либо не использовать цвета, либо выводить цвет детерминированно из префикса (напр. `status-*` → красный) и в сверке игнорировать суффикс `\nN`.
- Для человекочитаемости по-русски — держать словарь `slug → русская подпись` в карточке/общем реестре, а в обе системы писать только slug.
- Префиксы-пространства имён (`status-active`, `kind-deck`, `area-math`) эмулируют «single-select» custom properties, которых у личного аккаунта нет (§2.1); гейт может проверять «ровно одна метка с префиксом `status-`».

### 6.3 Google Drive
Если нужны те же метки в Drive (личный аккаунт): единственный механизм — Drive API `properties` на папке (§4.2), напр. `tags=math,deck` (≤124 байта на пару → длинный список резать на несколько ключей `tag1..tagN` или хранить по ключу на метку `t-math=1`). В UI Drive не видно; для человека — только поиск по API. Finder-теги на папках внутри Google Drive полагать ненадёжными (§4.3).

---

### Сводка непроверенного
- Приём/отказ GitHub на кириллицу в topic прямым PUT (есть только косвенный признак: 0 репо с `topic:русский`/`topic:中文`).
- Запрет `--` / дефиса в конце topic.
- Можно ли менять topics у архивного репо (есть только community-ответ «нельзя»).
- Доступность custom properties на бесплатной организации.
- Максимальная длина имени Finder-тега; регистронезависимость Finder-тегов; нормализация Unicode.
- Текущее (2024–2026) поведение Drive for desktop (File Provider) с Finder-тегами.
- Поддержка properties Drive API на папках (скорее да, прямо не описано).
- Поведение `/usr/bin/zip` с xattr.
