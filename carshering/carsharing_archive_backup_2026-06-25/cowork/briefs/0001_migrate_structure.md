# ЗАХОД для Cladkod — migrate_structure (один заход до конца)

> Скопировать ВСЁ в новый сеанс Claude Code, открытый в папке `carsharing_archive/`. Прикладывать ничего не нужно.
> **Тип захода — ОРГАНИЗАЦИОННЫЙ:** двигаем и переименовываем файлы, правим ссылки. **Содержание файлов НЕ менять** (числа, выводы, прозу не трогать). Перемещение рвёт ссылки → в конце ОБЯЗАТЕЛЕН верификатор (`tools/check_docs.py` зелёный, битых ссылок 0).

**КОНТЕКСТ.** Архив каршеринга реструктурируется из плоской кучи (23 файла в корне) в папки. Новый каркас (`README.md`, `PRINCIPLES.md`, `cowork/`, `tools/check_docs.py`) уже написан Cowork и ссылается на ЦЕЛЕВЫЕ пути. Твоя задача — привести физическую раскладку в соответствие: перенести и переименовать существующие файлы, переписать внутренние ссылки, добиться зелёного `check_docs`. ЦЕЛЬ: после захода дерево совпадает с `README.md §2/§4`, битых ссылок 0.

## 0. ПЕРВЫЙ ХОД

- Сделать точку отката: если папка под git — `git add -A && git commit -m "до миграции"`; иначе скопировать всю папку в `../carsharing_archive_backup_<дата>/`.
- Прочитать `README.md` (§2 карта, §4 структура) и `cowork/GUIDE.md` (раздел про верификатор). Показать план переноса до выполнения.

## 1. ДИСЦИПЛИНА

- Перенос — через `git mv` (если git) либо `mkdir -p` + `mv`. Имена строго по карте ниже.
- Правка ссылок — якорная, по карте «старое имя → новый путь». Содержание абзацев не трогать.
- Сохранять по умолчанию; вопросы — в отчёт, не блокировать.

## 2. ГРАНИЦЫ

- **Не менять содержание** файлов (числа, выводы, текст). Только: расположение, имена, и ССЫЛКИ на переехавшие файлы.
- Не трогать уже написанный Cowork каркас (`README.md`, `PRINCIPLES.md`, `PLAN.md`, `cowork/*`, `tools/check_docs.py`) — он уже целевой; правь в нём ссылки только если `check_docs` укажет на битую.
- `carsharing_pricing.xlsx` руками не трогать; если после переноса `build_model.py` пишет его не туда — поправить путь сохранения в `build_model.py` (он относительный), пересобрать, проверить, что xlsx лёг в `model/`.

## 3. ЗАДАЧА

### 3.1. Создать папки
`spine/`, `research/`, `model/`, `provenance/`. (`cowork/`, `cowork/briefs/`, `cowork/reports/`, `tools/` уже есть.)

### 3.2. Перенести и переименовать (карта старое → новое)

| Старое (в корне) | Новое |
|---|---|
| `00_problem_statement.md` | `spine/00_problem_statement.md` |
| `01_answer.md` | `spine/01_answer.md` |
| `02_problem_and_math.md` | `spine/02_problem_and_math.md` |
| `03_model_anatomy.md` | `spine/03_model_anatomy.md` |
| `04_demand_testing_ops.md` | `spine/04_demand_testing_ops.md` |
| `05_open_questions.md` | `spine/05_open_questions.md` |
| `carsharing_R1_benchmark.md` | `research/R1_benchmark.md` |
| `carsharing_R2_elasticity.md` | `research/R2_elasticity.md` |
| `carsharing_R3_demand_estimation.md` | `research/R3_demand_estimation.md` |
| `carsharing_R4_utilization.md` | `research/R4_utilization.md` |
| `carsharing_R5_marginal_peakload.md` | `research/R5_marginal_peakload.md` |
| `carsharing_R6_screening_markup.md` | `research/R6_screening_markup.md` |
| `carsharing_R7_option_value.md` | `research/R7_option_value.md` |
| `carsharing_R8_econometric_precision.md` | `research/R8_econometric_precision.md` |
| `build_model.py` | `model/build_model.py` |
| `carsharing_pricing.xlsx` | `model/carsharing_pricing.xlsx` |
| `carsharing_data_sources.md` | `data_sources.md` (остаётся в корне, только префикс убрать) |
| `carsharing_build_log.md` | `provenance/journal.md` |
| `carsharing_audit.md` | `provenance/audit.md` |
| `carsharing_pricing_analysis.md` | `provenance/analysis.md` |
| `carsharing_TOOL_BRIEF.md` | `cowork/briefs/0002_html_tool.md` |

### 3.3. Удалить (superseded)
`00_README.md` — его роль индекса перешла к `README.md`. Сверить, что ничего уникального в нём не осталось (всё ушло в `README.md`), и удалить.

### 3.4. Переписать внутренние ссылки
Во ВСЕХ перенесённых файлах (и в любых, что на них ссылаются) обновить ссылки по карте имён выше. Учти относительные пути от новой папки:
- из `spine/` и `research/`: реестр — `../data_sources.md`; принципы — `../PRINCIPLES.md`; модуль R — `../research/Rk_*.md`; соседний спайн — `00_*.md`.
- старые имена `carsharing_Rk_*` → `Rk_*`; `carsharing_data_sources.md` → `data_sources.md`; `carsharing_build_log.md` → `provenance/journal.md` (и `journal`); `carsharing_audit.md`/`carsharing_pricing_analysis.md` → `provenance/audit.md`/`provenance/analysis.md`; упоминания `PLAN.md`, `00_README` — на `README.md`.
Метод: grep по старым именам по всему дереву → заменить на новые с корректным относительным путём.

КРИТЕРИЙ ГОТОВНОСТИ: `python tools/check_docs.py` печатает «OK» (0 сирот, 0 битых ссылок, 0 имён с й/ё); `grep -rl 'carsharing_R\|carsharing_data_sources\|carsharing_build_log\|carsharing_audit\|carsharing_pricing_analysis\|carsharing_TOOL_BRIEF\|00_README' --include=*.md .` пуст; `python model/build_model.py` пересобирает `model/carsharing_pricing.xlsx` без ошибок.

## 4. РЕШЕНИЯ ИЗ ПРОШЛОГО (учесть, не переоткрывать)

- Имена — ASCII, без й/ё (`PRINCIPLES.md §4.5`). Содержание файлов — русское, не трогаем.
- Реестр `data_sources.md` остаётся в КОРНЕ (это дом чисел, его читают рано по Правилу №0), не в `model/`.
- `audit.md` — только датированные поправки, не переписывать (но перенести и поправить ссылки можно).

## 5. ВЕРИФИКАТОР (гейт — отдельным свежим взглядом)

Запусти `tools/check_docs.py` ПОСЛЕ всех правок. Если красный — чини ссылки до зелёного. Дополнительно прогони grep из критерия готовности. Это организационный заход: единственное доказательство успеха — «битых ссылок 0 + дерево = README», а не «вроде перенёс».

## 6. ОТЧЁТ → `cowork/reports/<дата>_migrate_structure.md`

Что перенесено (карта факт), сколько ссылок переписано, вывод `check_docs` (зелёный), пересобрался ли xlsx, что вынесено владельцу. Durable — в существующие дома, новых доков не плодить.

## ВЫХОД
Чек-лист: папки созданы ✓; 21 файл перенесён/переименован по карте ✓; `00_README.md` удалён ✓; ссылки переписаны ✓; `check_docs` зелёный ✓; xlsx пересобран ✓; отчёт в `cowork/reports/` ✓.
