# Роутер сессий в трёх средах Claude: что документировано (исследование)

**Дата данных: 2026-09-25.** Все утверждения проверены по живым страницам документации в этот день, если не помечено иначе.
Пометки: **[НЕ ПРОВЕРЕНО]** — источник косвенный, сторонний или вывод мой; **[МЕНЯЕТСЯ]** — функция в бете или раскатке, либо описание сменилось недавно; **[ЭМПИРИКА]** — видел сам в облачной сессии Claude Code, в которой шло исследование (версия CLI 2.1.42 по `CLAUDE_CODE_VERSION`), в документации этого нет.

Ключевые источники (дальше по тексту ссылки короткие):
- Hooks: https://code.claude.com/docs/en/hooks
- Облачные окружения: https://code.claude.com/docs/en/cloud-environments
- Claude Code в облаке: https://code.claude.com/docs/en/claude-code-on-the-web
- Settings: https://code.claude.com/docs/en/settings
- Memory / CLAUDE.md: https://code.claude.com/docs/en/memory
- Skills: https://code.claude.com/docs/en/skills
- Plugins: https://code.claude.com/docs/en/plugins , https://code.claude.com/docs/en/plugins/install , https://code.claude.com/docs/en/plugins/loading
- Cowork: https://claude.com/docs/cowork/overview , https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork

---

## 0. Сводка: чем можно запустить роутер в каждой среде

| Механизм | Claude Code на Mac (терминал / вкладка Code в Desktop, Local) | Claude Code в облаке (claude.ai/code, Cloud в Desktop) | Cowork (Desktop / web) |
|---|---|---|---|
| `~/.claude/settings.json` (хуки пользователя) | да | **нет** | **нет** (Cowork не читает `~/.claude`) |
| `~/.claude/CLAUDE.md`, `~/.claude/skills/` | да | **нет** | **нет** |
| `.claude/settings.json` в репо (хуки) | да | да, **только в сессии с одним репо** | н/д |
| `CLAUDE.md` и `.claude/skills/` в репо | да | да | Cowork читает папку; про `CLAUDE.md` см. §3 |
| Скиллы, включённые в аккаунте claude.ai | да (синхронизация, v2.1.273+) | да | да |
| Плагины, включённые в аккаунте claude.ai (скиллы + хуки) | да (как `<name>@synced`, v2.1.273+) | **не документировано** (см. §2.4) | да |
| Инструкции аккаунта / проекта в claude.ai | нет | в новых «Projects» Claude Code — инструкции проекта | Global instructions → «Instructions for Claude»; инструкции проекта и папки |

Главный вывод: **ни одного механизма, одинаково работающего во всех трёх средах, нет.** Ближе всего подходят два:
(а) **плагин в аккаунте claude.ai** (скилл-роутер + хук SessionStart) — Cowork и терминал на Mac;
(б) **скилл, включённый в аккаунте claude.ai** — все три среды, но это только скилл без хука, и запускать его приходится инструкцией, а не событием.
Для облачного Claude Code детерминированный запуск даёт только хук, **закоммиченный в `.claude/settings.json` каждого репо**, и только в сессиях с одним репо.

И второй вывод, самый важный: **хук сам не спрашивает пользователя** и не может заставить Claude заговорить первым. Он кладёт в контекст текст, а спрашивает Claude — своим инструментом `AskUserQuestion` — в ответ на **первое сообщение пользователя** (подробности в §1.4).

---

## 1. Хуки Claude Code: SessionStart и UserPromptSubmit

### 1.1 SessionStart: что умеет
- Срабатывает, когда сессия начинается или возобновляется. Матчеры: `startup` (новая сессия), `resume` (`--resume`, `--continue`, `/resume`), `clear` (`/clear`), `compact` (авто- или ручная компакция), `fork` (`--fork-session`, `/fork`, `/branch`). Источник: https://code.claude.com/docs/en/hooks#sessionstart
- Поддерживаются только типы обработчиков `command` и `mcp_tool`. При запуске MCP-серверы ещё не подняты, поэтому хуки `mcp_tool` на SessionStart пропускаются. Выходит, что на практике годится только `command` (тот же раздел).
- Передать контекст можно двумя путями. **Простой stdout** (exit 0) — «Claude Code adds plain-text stdout as context». **JSON** `hookSpecificOutput.additionalContext` — строка попадает в контекст «at the start of the conversation, before the first prompt». Источник: https://code.claude.com/docs/en/hooks#add-context-for-claude
- Дополнительные поля вывода SessionStart:
  - `sessionTitle` — задаёт название сессии (как `/rename`); работает для `startup`, `resume` и `fork`.
  - `initialUserMessage` — первое пользовательское сообщение, **но только в неинтерактивном режиме `-p`**.
  - `reloadSkills: true` — заново сканирует каталоги скиллов после хука, так что скилл, установленный хуком, доступен уже с первого промпта.
  - `watchPaths` — пути для событий FileChanged.

  Источник: https://code.claude.com/docs/en/hooks#sessionstart-decision-control
- Во входе хук получает `source` (startup/resume/…), `model`, `agent_type`, `session_title`, `session_id`, `transcript_path` и `cwd`. При resume добавляются `seconds_since_last_response` и `prompt_cache_likely_expired` (v2.1.251+). Источник: тот же раздел, «SessionStart input».
- `CLAUDE_ENV_FILE`: хук может дописать туда `export`, и переменные сохранятся для последующих Bash-команд сессии. Например, туда можно записать выбранный тип сессии.
- Тайминг: в интерактивной сессии хуки SessionStart идут в фоне, печатать можно сразу, но **первый ответ Claude ждёт завершения хуков**. Источник: https://code.claude.com/docs/en/hooks#sessionstart
- Предупреждение из документации: `additionalContext` лучше писать **констатациями фактов, а не императивными «системными командами»**. Иначе может сработать защита от prompt-injection, и Claude покажет текст пользователю, а не примет его как контекст. Если значение длиннее 10 000 символов, оно уходит в файл, а Claude получает путь к файлу и превью. Источник: https://code.claude.com/docs/en/hooks#add-context-for-claude
- Документация сама советует: статичный контекст держать в CLAUDE.md, а хук использовать для динамического.

### 1.2 Где настраиваются хуки
Таблица «Hook locations» (https://code.claude.com/docs/en/hooks#hook-locations):
- `~/.claude/settings.json` — все ваши проекты на этой машине;
- `.claude/settings.json` — один проект, коммитится в репо;
- `.claude/settings.local.json` — один проект, не коммитится;
- managed policy settings — вся организация;
- плагин, `hooks/hooks.json` — пока плагин включён;
- frontmatter скилла — с момента вызова скилла до конца сессии (можно `once: true`);
- frontmatter субагента — пока работает субагент.

Хуки из разных уровней **складываются**, а не заменяют друг друга.

### 1.3 Работает ли SessionStart в облаке (Claude Code on the web)
- **Да, но только из репо (или из server-managed settings).** Цитата: «If you have SessionStart hooks in your user-level `~/.claude/settings.json`, don't expect them in the cloud… Anthropic-hosted environment: Claude Code runs hooks from the repository and from your organization's server-managed settings.» Источник: https://code.claude.com/docs/en/cloud-environments#setup-scripts-vs-sessionstart-hooks
- Таблица там же: SessionStart hooks запускаются «After Claude Code launches, on every session including resumed», «Local and cloud sessions». Setup script — другое: он выполняется до запуска Claude Code, только в облаке и пропускается, если окружение закэшировано.
- **Ограничение для нескольких репо:** хуки и permission rules из `.claude/settings.json` читаются «Yes, in a session with one repository». Сессия с несколькими репо, в том числе поток (thread) в новых Projects, стартует над клонами и их не читает. Источники: https://code.claude.com/docs/en/cloud-environments#what-carries-over-from-your-setup и https://code.claude.com/docs/en/settings#settings-in-cloud-sessions
- Отличить облако в скрипте можно по `CLAUDE_CODE_REMOTE=true` («Set automatically to true when Claude Code is running as a cloud session»). Источник: https://code.claude.com/docs/en/env-vars
- **[ЭМПИРИКА]** В этой облачной сессии есть ещё `CLAUDE_CODE_ENTRYPOINT=remote_desktop` и `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`. Эти переменные не документированы, опираться на них рискованно.

### 1.4 UserPromptSubmit как альтернатива или дополнение
- Срабатывает на каждый промпт пользователя до того, как Claude его обработает. Матчеров нет. Stdout и `additionalContext` добавляются в контекст рядом с промптом. Можно заблокировать промпт (`decision: "block"`, пользователь видит `reason`) и задать `sessionTitle`. Таймаут по умолчанию 30 с. Если хук не уложился, его вывод отбрасывается, а промпт уходит без контекста. Источник: https://code.claude.com/docs/en/hooks#userpromptsubmit
- Во входе есть текст промпта. Значит, хук видит, **о чём первая просьба**, и может, например, сам предклассифицировать её по словарю синонимов из карточек репо и подложить Claude «кандидатов» в `additionalContext`. **[НЕ ПРОВЕРЕНО — моя идея шаблона]**
- При `--resume` сохранённый `additionalContext` от UserPromptSubmit подставляется из транскрипта заново, хук повторно не запускается. SessionStart же на resume перезапускается.

### 1.5 Может ли хук «заставить интервью»
- **Спросить пользователя сам хук не может.** Он умеет вставить контекст (`additionalContext`/stdout), принять решение allow/block, показать сообщение пользователю (`systemMessage`) или подать сигнал терминалу (`terminalSequence`). Источник: https://code.claude.com/docs/en/hooks (разделы JSON output, Decision control).
- Спрашивает Claude — через инструмент **`AskUserQuestion`**: 1–4 вопроса с вариантами ответа, есть пункт «Other» для свободного текста. По умолчанию вопрос висит, пока пользователь не ответит. Источники: https://code.claude.com/docs/en/tools-reference#askuserquestion-tool-behavior и https://code.claude.com/docs/en/hooks#askuserquestion
- **Claude не может заговорить первым в интерактивной сессии.** Контекст SessionStart ложится «before the first prompt», но ответ Claude появляется только после первого сообщения пользователя. Исключение — режим `-p`, где хук задаёт `initialUserMessage`. Отсюда реальная форма «интервью»: пользователь пишет что угодно, а Claude, видя в контексте факт «сессия не классифицирована, протокол — скилл router», первым делом зовёт `AskUserQuestion`. **Это соблюдение инструкции моделью, а не гарантия.** Документация прямо говорит, что CLAUDE.md и контекст — «context, not enforced configuration». Источник: https://code.claude.com/docs/en/memory#claude-md-vs-auto-memory
- Что даёт детерминизм **[НЕ ПРОВЕРЕНО — вывод из документации, не готовый рецепт Anthropic]**:
  - UserPromptSubmit-хук добавляет напоминание в каждый промпт, пока нет маркера «сессия классифицирована». Маркер — файл по `session_id` или в `scratchpad_dir`.
  - PreToolUse-хук блокирует `Write`/`Edit`/`Bash` (exit 2 или `decision: deny`), пока маркера нет. Так изменения до маршрутизации физически невозможны, и именно это «краснеет» при нарушении.
- Сторонние материалы о режиме «интервью» через `AskUserQuestion` (не Anthropic): https://www.developersdigest.tech/blog/claude-code-interview-mode , https://neonwatty.com/posts/interview-skills-claude-code/ . Открытый feature request о хуке для AskUserQuestion: https://github.com/anthropics/claude-code/issues/12605 **[НЕ ПРОВЕРЕНО: статус issue]**

---

## 2. Скиллы, плагины, CLAUDE.md

### 2.1 Как выбираются скиллы
- В контексте всегда лежит **список имён и описаний** скиллов, а полный текст скилла грузится только при вызове. Claude решает, звать ли скилл, **по `description`** (плюс `when_to_use`). Источник: https://code.claude.com/docs/en/skills#frontmatter-reference
- Лимиты:
  - `description` + `when_to_use` обрезаются на 1 536 символах;
  - общий бюджет списка скиллов — около 1% окна контекста;
  - при переполнении сначала выпадают описания самых редко используемых скиллов.

  Бюджет поднимается через `skillListingBudgetFraction` / `SLASH_COMMAND_TOOL_CHAR_BUDGET`. Источник: https://code.claude.com/docs/en/skills#skill-descriptions-are-cut-short
- Кто может вызвать скилл: `disable-model-invocation: true` — только пользователь (`/name`); `user-invocable: false` — только Claude. Источник: https://code.claude.com/docs/en/skills#control-who-invokes-a-skill
- Во frontmatter скилла можно задать хуки. Они включаются с момента вызова скилла и действуют до конца сессии. Значит, «типовой» скилл после маршрутизации может сам включить гейты своего типа. Источник: https://code.claude.com/docs/en/hooks#hooks-in-skills-and-agents
- Документация признаёт, что скилл может «перестать влиять» после первого ответа. Совет: усилить `description` или применять хуки для детерминизма (раздел «Skill content lifecycle»). Для замера срабатывания есть eval-механизм плагинов (`claude plugin eval`, грейдер `tool_used: Skill`).

### 2.2 Где живут скиллы и куда они доходят
Таблица: https://code.claude.com/docs/en/skills#where-skills-live
- Personal `~/.claude/skills/` — все проекты на машине, «but not Cowork or cloud sessions».
- Project `.claude/skills/` — сессии в этом репо, в том числе облачные. Если сессия запущена в корне монорепо, вложенные `<subdir>/.claude/skills/` подгружаются, когда Claude начинает работать с файлами этой папки.
- Plugin — где включён плагин, под именем `/plugin:skill`.
- **Аккаунт claude.ai** — «Cowork sessions, cloud sessions, and terminal sessions where you sign in with that account». В терминал такие скиллы скачиваются в `~/.claude/skills/synced/` (v2.1.273+) и проверяются примерно раз в 10 минут. Источник: https://code.claude.com/docs/en/skills#how-synced-skills-behave
- **[ЭМПИРИКА]** В этой облачной сессии синхронизированные скиллы аккаунта видны с префиксом `anthropic-skills:`, и каталог `~/.claude/skills/synced` существует. Это согласуется с документацией.

### 2.3 Плагины и маркетплейсы
- Плагин — это каталог со skills, agents, hooks (`hooks/hooks.json`), MCP-серверами и манифестом `.claude-plugin/plugin.json`. Маркетплейс — репо с `.claude-plugin/marketplace.json`, может быть приватным. Источники: https://code.claude.com/docs/en/plugins , https://code.claude.com/docs/en/plugin-marketplaces
- Скоупы установки: user (все проекты на машине), project (через закоммиченный `.claude/settings.json` → `enabledPlugins`/`extraKnownMarketplaces`; каждый участник ставит сам), local.
- **Облачные сессии не загружают плагины**: ни из локальных настроек, ни объявленные в `.claude/settings.json` репо. Цитата: «A cloud session doesn't install the plugins a repository turns on under enabledPlugins». Плагины в облако попадают только через managed settings организации или через «Project settings > Plugins» в новых Projects. Источники: https://code.claude.com/docs/en/cloud-environments#what-carries-over-from-your-setup , https://code.claude.com/docs/en/plugins/install , https://code.claude.com/docs/en/claude-projects#get-skills-plugins-connectors-and-tools-into-threads

### 2.4 Плагины из аккаунта claude.ai (важно для «одного носителя»)
- Плагин, включённый в аккаунте claude.ai, загружается в Claude Code как `<name>@synced`: «In terminal sessions, a synced plugin's skills, agents, hooks, MCP servers, and LSP servers all load». В Cowork он скачивается в окружение сессии при старте. Источник: https://code.claude.com/docs/en/plugins/loading#synced-plugins
- Support-статья: «Plugins enabled for your Claude account also load in Claude Code in your terminal… Hooks and sub-agents run in Cowork and Claude Code, so they appear grayed out in chat». Нужна v2.1.273+. Синхронизация идёт раз при каждом старте Claude Code и **только в одну сторону**, из аккаунта. Источник: https://support.claude.com/en/articles/13837440-use-plugins-in-cowork
- **Подводный камень:** синхронизация в терминале идёт в фоне и может закончиться уже после старта сессии («Plugins changed. Run /reload-plugins»). Поэтому в первой сессии после изменения плагина его SessionStart-хук может не сработать. Это мой вывод из описания тайминга **[НЕ ПРОВЕРЕНО]**.
- **Облако Claude Code:** в списке мест, где грузятся synced-плагины, названы только Cowork и терминал. Для облачных сессий документирована загрузка **скиллов** аккаунта, про **плагины** аккаунта ничего не сказано. **[НЕ ПРОВЕРЕНО — считать, что не грузятся, пока не проверено]**

### 2.5 Как раздать роутер-скилл и хук на много репо (варианты)
1. **Плагин в аккаунте claude.ai** (загрузить через Customize → Plugins). Доходит до Cowork и терминала на Mac одним объектом, хук включён. До облака не доходит (см. 2.4).
2. **Скилл в аккаунте claude.ai.** Доходит везде, но это только скилл без хука. Поводом его вызвать станет описание, инструкция в CLAUDE.md или Instructions for Claude.
3. **Закоммиченные в каждый репо** `.claude/settings.json` (SessionStart) и `.claude/skills/router/`. Работает на Mac и в облаке, но только в сессиях с одним репо. Нужно копировать в N репо. Можно держать канон в одном репо, а в остальных — скрипт-заглушку, которая берёт канон из этого репо. **[НЕ ПРОВЕРЕНО]**
4. **Хук в user-settings `~/.claude/settings.json`** — только Mac.
5. Документированный приём: SessionStart-хук делает `git pull` репо со скиллами в `~/.claude/skills/...` и возвращает `reloadSkills: true`. Пример есть прямо в https://code.claude.com/docs/en/hooks#sessionstart-decision-control

### 2.6 Иерархия CLAUDE.md и импорты
- Порядок загрузки (от широкого к узкому): managed → `~/.claude/CLAUDE.md` → проектный `./CLAUDE.md` или `./.claude/CLAUDE.md` → `./CLAUDE.local.md`. Файлы **в папках выше cwd** грузятся при старте и склеиваются, а не перекрывают друг друга. Файлы в подпапках подгружаются, когда Claude читает там файлы. Источник: https://code.claude.com/docs/en/memory#choose-where-to-put-claudemd-files
- Импорт `@path/to/file`: относительные и абсолютные пути, рекурсия до 4 уровней, внутри code span не срабатывает. Для внешнего импорта в проектном файле спрашивается одобрение. Импорт грузится **при старте** и расходует контекст. Источник: https://code.claude.com/docs/en/memory#import-additional-files
- Совет по размеру: меньше 200 строк на файл; длинные процедуры выносить в скиллы или в `.claude/rules/` с `paths:`.
- **`~/.claude/CLAUDE.md` в облаке не применяется** («Lives on your machine, not in the repo»). Источник: https://code.claude.com/docs/en/cloud-environments#what-carries-over-from-your-setup
- **Cowork на desktop:** импорты из пользовательских файлов, ведущие за пределы рабочей папки, пропускаются. Симлинк `~/.claude/CLAUDE.md` тоже пропускается. Источник: https://code.claude.com/docs/en/memory (Warning в разделе Import).
- AGENTS.md: Claude Code (v2.1.277+) читает `AGENTS.md`, **если нет CLAUDE.md** в cwd и выше. Режим «оба сразу» включается настройкой `claude-md-and-agents-md`. Источник: https://code.claude.com/docs/en/memory#agents-md **[МЕНЯЕТСЯ — функция добавлена недавно]**
- Хук `InstructionsLoaded` срабатывает при загрузке каждого CLAUDE.md или rules-файла, с `load_reason`. Пригоден для аудита «что реально загрузилось».

---

## 3. Cowork: что сейчас документировано

**[МЕНЯЕТСЯ — сильно и прямо сейчас.]** На support-страницах стоит баннер: «Claude Cowork is now just Claude… rolling out gradually to Pro and Max plans». Чат и Cowork сливаются в один разговор без выбора режима. Источник: https://support.claude.com/en/articles/16761823-claude-cowork-and-chat-are-one-claude

- **Где исполняется:** «Cowork runs your sessions remotely in the cloud (in beta)». Работа идёт на серверах Anthropic, а к локальным файлам и браузеру Claude обращается через открытый Claude Desktop. Cowork доступен в Desktop (macOS/Windows), на web, на мобильных и в боковой панели Chrome. Источник: https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork
- **Global instructions:** Settings > Cowork > Global instructions, «apply to every Cowork session». В новом объединённом интерфейсе они становятся частью **Instructions for Claude** (Settings > General) и действуют во всех разговорах. Источники: та же статья и https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features
- **Folder instructions:** «add project-specific context to Cowork when you select a local folder on desktop. Claude can also update these on its own during a session.» Формат и имя файла на support-странице **не указаны**. Changelog Desktop (v2.2553.13, 2026-09-21) для вкладки Code пишет: «in a folder with no CLAUDE.md, Claude reads AGENTS.md». Отсюда косвенно следует, что Desktop читает CLAUDE.md из папки; для Cowork это прямо **[НЕ ПРОВЕРЕНО]**. Сторонние гайды (claudecowork.im, the-ai-corner.com) говорят о CLAUDE.md в папке Cowork; это не Anthropic.
- **Projects в Cowork:** instructions, scheduled tasks, context (локальная папка, привязанный чат-проект, URL) и **memory, привязанная к проекту**. Новые проекты сохраняются в аккаунт, а проекты «из существующей папки» остаются на компьютере. Источник: https://support.claude.com/en/articles/14116274-organize-your-tasks-with-projects-in-claude-cowork . Страница на claude.com описывает старую модель: «Projects live on your computer», а поле Description использует Dispatch при выборе проекта: https://claude.com/docs/cowork/guide/projects **[МЕНЯЕТСЯ: две страницы расходятся]**. Ограничение: «Projects are only available in Cowork, not in Claude Code» (в той же support-статье).
- **Skills / plugins:** управляются через Customize. «Cowork loads the ones enabled for your claude.ai account, synced at session start, and doesn't read the Claude Code CLI's ~/.claude directory». Источник: https://claude.com/docs/cowork/overview
- **Хуки в Cowork: есть, но только внутри плагинов.** Страница «Install plugins»: «Installing one can add skills, MCP connectors, subagents, slash commands, or hooks». Источник: https://claude.com/docs/cowork/guide/plugins . Страница деплоя для 3P: «Cowork sessions run hooks from marketplace plugins, from plugins in the org-plugins/ directory, and from plugins users add themselves». Там же про UserPromptSubmit: блокировка промпта в Desktop показывает reason. Источник: https://claude.com/docs/third-party/claude-desktop/extensions#plugin-hooks (документ про 3P-развёртывание; для обычного аккаунта применимость **[НЕ ПРОВЕРЕНО]**).
- **Отдельного механизма «при старте сессии спросить» в Cowork не документировано.** Нет ни настройки, ни шаблона стартового интервью. Единственный событийный механизм — хуки плагинов. Работает ли SessionStart в **облачном** Cowork так же, как в локальном, прямо не сказано **[НЕ ПРОВЕРЕНО]**. Также есть оговорка: «plugins that include local MCP servers work through the desktop app only».
- **Memory:** общая память чата и Cowork работает **только** когда Cowork идёт в облаке. Локальные Cowork-сессии память не используют. Источник: https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context
- **Dispatch** выбирает проект по его описанию (claude.com/docs/cowork/guide/projects). По сути это встроенный роутер «задача → проект». Однако: «Dispatch isn't available to new users» в новом интерфейсе (статья про «one Claude»). **[МЕНЯЕТСЯ]**
- Для организаций есть `organizationInstructions` (до 3 000 символов, Chat/Cowork/Code). Источник: changelog Desktop, https://claude.com/docs/cowork/changelog

---

## 4. Claude.ai: Projects, инструкции, память (роутер на стороне чата)

- **Instructions for Claude** (Settings) действуют на все разговоры. **Project instructions** — на все чаты проекта. Источники: https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features , https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects
- Имя и описание проекта **Claude не видит** («note that Claude will not have access to these details»). Поэтому карточку для роутера нужно класть в instructions или knowledge, а не в описание. Источник: https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects
- Project knowledge — загружаемые файлы. На платных планах при приближении к лимиту включается RAG. Источник: https://support.claude.com/en/articles/9517075-what-are-projects
- **Память:** сохраняется «as a set of individual topics». У каждого проекта своя память и сводка. Поиск по прошлым чатам (RAG) ведётся либо по чатам вне проектов, либо внутри одного проекта. Источник: https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context
- **[МЕНЯЕТСЯ]** Новая версия Projects (бета) — «a project is one conversation», параллельные облачные threads, у каждого thread свои files, repositories, instructions и memory. Раскатка начинается с Claude Code (claude.ai/code и вкладка Code в Desktop), затем чат и Cowork. Источники: https://support.claude.com/en/articles/9517075-what-are-projects и https://code.claude.com/docs/en/claude-projects
  - В Projects Claude Code: instructions до 16 000 символов «sent to each new thread», память проекта в файлах с индексом `MEMORY.md`, плагины через «Project settings > Plugins». Хуки и permissions из `.claude/settings.json` в проекте с несколькими репо **не применяются**. Источник: https://code.claude.com/docs/en/claude-projects#give-a-project-standing-context
  - Для роутера это важно: **Project instructions здесь и есть «входной бриф» каждого потока**, и карточки репо по синонимам можно держать там.

---

## 5. Общие паттерны «роутер / диспетчер» (цитируемое)

- **Anthropic, «Building effective agents» (19 дек. 2024)**, workflow **Routing**: «Routing classifies an input and directs it to a specialized followup task». Когда применять: «complex tasks with distinct categories that benefit from separate handling, where classification can be performed reliably». В той же статье: «Start with simple prompts… add multi-step agentic systems only when simpler solutions fall short». Источник: https://www.anthropic.com/engineering/building-effective-agents
- **Anthropic, use-case guide «Ticket routing»** — классификация по intent. Даёт список категорий с определениями, метрики вроде consistency ≥95% и «model adaptability… within 50–100 sample tickets». Это прямо применимо к валидации типологии. Источник: https://docs.claude.com/en/docs/about-claude/use-case-guides/ticket-routing (зеркало: https://platform.claude.com/docs/en/about-claude/use-case-guides/ticket-routing)
- **AGENTS.md**: открытый формат «README for agents», теперь под Agentic AI Foundation (Linux Foundation). В монорепо: «Agents automatically read the nearest file in the directory tree, so the closest one takes precedence». Источник: https://agents.md/
- **Cursor Rules**: четыре режима — Always Apply; Apply Intelligently («Agent reads the description and pulls the rule in when relevant», то есть тот же механизм, что у скиллов Claude); по glob; вручную через `@rule`. Правила бывают уровня проекта, пользователя и команды; вложенные AGENTS.md поддерживаются. Источник: https://cursor.com/docs/context/rules
- Общий знаменатель всех трёх систем: **список «когда применять» (описание или триггеры) всегда в контексте, полный текст подгружается по решению модели.** Отсюда практическое правило для типологии: у каждого типа — короткое различающее описание и синонимы. Это и есть поле `description` скилла.

---

## 6. Разбор прошлых сессий для выведения типологии

### 6.1 Claude Code (локально)
- Транскрипты лежат в `~/.claude/projects/<project>/<session>.jsonl` («Full conversation transcript: every message, tool call, and tool result»). Субагенты — в `<session>/subagents/`, большие выводы — в `<session>/tool-results/`. Имя `<project>` — путь cwd со слешами, заменёнными на `-` (пример в документации: `-home-user-work-my-repo`). Все промпты с путём проекта есть в `~/.claude/history.jsonl`. Источник: https://code.claude.com/docs/en/claude-directory
- **Внимание: по умолчанию транскрипты удаляются через 30 дней** (`cleanupPeriodDays`, минимум 1). Если нужна история для типологии, этот порог надо поднять **до** анализа. Транскрипты сессий, начатых в Claude Desktop и Cowork, хранятся бессрочно, срок задаёт `desktopSessionCleanupPeriodDays`. Источник: тот же раздел «Cleaned up automatically».
- Формат JSONL официально **не описан**. **[ЭМПИРИКА, v2.1.42]** Каждая строка — объект с `type`: `user`, `assistant`, `system`, `attachment`, `mode`, `last-prompt`, `queue-operation`, `cost-state` и др. У сообщений есть поля `uuid`, `parentUuid` (граф, а не список), `sessionId`, `timestamp`, `cwd`, `gitBranch`, `entrypoint`, `version` и `message` (сообщение API). Поля `cwd` и `gitBranch` дают готовую привязку «сессия → репо». Формат меняется между версиями.
- Встроенный **`/insights`** генерирует HTML-отчёт по недавним сессиям **на этой машине**: чем занимаетесь, трения, советы. За прогон анализирует до 200 новых сессий. Отчёт пишется в `~/.claude/usage-data/report.html` и тоже удаляется по `cleanupPeriodDays`. В облачных сессиях недоступен; сессии с других устройств и claude.ai не включает. Источники: https://code.claude.com/docs/en/costs#analyze-your-usage-patterns , https://code.claude.com/docs/en/commands
- `/export` — текущий разговор в текст. Из сессии это тоже файл транскрипта: во входе каждого хука есть `transcript_path`.
- Сторонние инструменты (не Anthropic, качество **[НЕ ПРОВЕРЕНО]**):
  - https://github.com/simonw/claude-code-transcripts — JSONL в HTML;
  - https://github.com/daaain/claude-code-log — весь `~/.claude/projects` в HTML/MD;
  - https://github.com/ly4096x/ClaudeCodeTranscriptViewer — просмотрщик;
  - https://github.com/cj-mills/cjm-harness-transcripts — парсер с разбором DAG `parentUuid`;
  - https://pypi.org/project/claude-code-analytics/0.1.0

### 6.2 Облачные сессии Claude Code
- Живут в аккаунте на claude.ai/code. Их можно перетянуть в терминал через `claude --teleport`, и тогда они окажутся в локальной истории. Массового экспорта облачных сессий в документации **нет** **[НЕ ПРОВЕРЕНО: покрывает ли их «Export data»]**. Источник: https://code.claude.com/docs/en/claude-code-on-the-web#from-cloud-to-terminal

### 6.3 claude.ai и Cowork
- **Export data:** Settings > Privacy > Export data. Доступно на Free/Pro/Max; ссылка приходит на почту и живёт 24 часа. Экспорт включает «conversation data and the user data». На Team/Enterprise экспорт делает только Primary Owner. Источник: https://support.claude.com/en/articles/9450526-export-your-claude-data . Попадают ли в экспорт Cowork-задачи и сессии Claude Code **не указано [НЕ ПРОВЕРЕНО]**.
- Память выгружается отдельно (Settings > Memory; или попросить «Write out your memories of me verbatim»). Все записи памяти входят в data export. Источник: https://support.claude.com/en/articles/12123587-import-and-export-your-memory-from-claude
- Локальные Cowork-сессии пишут транскрипты Claude Code на машине (см. `desktopSessionCleanupPeriodDays` выше); точный путь **[НЕ ПРОВЕРЕНО]**.

### 6.4 Методика кластеризации (цитируемый образец)
- **Anthropic Clio (12 дек. 2024)** — автоматический анализ реальных разговоров. Этапы: извлечение facets (тема, число реплик, язык), семантическая кластеризация, описание кластеров с названием и сводкой, иерархическая организация кластеров. Источники: https://www.anthropic.com/research/clio , статья https://arxiv.org/abs/2412.13678 . Эту схему можно перенести на свою историю один в один: facet «что делали / тип артефакта / репо (`cwd`)» → кластеры → названия типов → иерархия. Далее — повторная классификация новых сессий и подсчёт «не подошло ни в один тип» как сигнал пересмотреть типологию. **[НЕ ПРОВЕРЕНО — перенос мой]**
- Метрики из Ticket routing (consistency, adaptability на 50–100 примерах) подходят как критерий «типология устоялась».

---

## 7. Что из этого следует для роутера (мои выводы, не документация)

1. **Интервью ведёт Claude, запускает его текст.** Хук или инструкция кладёт факт «сессия не классифицирована; протокол — скилл `router`», а скилл задаёт через `AskUserQuestion` три вопроса: над чем работаем, тип (варианты из типологии), репо (варианты из карточек). Писать в `additionalContext` лучше фактами, а не приказами (§1.1).
2. **Гарантию «не пропустили» даёт только хук-гейт** (PreToolUse блокирует правки до маркера классификации) плюс UserPromptSubmit, который напоминает. Всё остальное — просьба к модели. Это работает на Mac и в облаке при хуке из репо, и в Cowork при хуке из плагина.
3. **Раскладка по средам:**
   - Mac — user-hook или synced-плагин;
   - Cowork — плагин аккаунта;
   - облако — хук в `.claude/settings.json` каждого репо (только сессии с одним репо) и скилл аккаунта;
   - новые Projects Claude Code — project instructions.
4. **Карточки репо** лучше держать в одном месте, которое доходит до всех сред, — внутри самого скилла-роутера (supporting files). Тогда синонимы едут вместе со скиллом через аккаунт claude.ai. Импорт `@` из чужой папки в Cowork блокируется (§2.6).
5. **История для типологии** по умолчанию хранится 30 дней: поднять `cleanupPeriodDays` сейчас. Для облака и чата — Export data плюс teleport.
6. Лимит описания скилла — 1 536 символов, бюджет списка — около 1% окна. Типов порядка десяти: либо одно описание роутера плюс таблица типов внутри скилла, либо по скиллу на тип с жёстко различающимися описаниями.
