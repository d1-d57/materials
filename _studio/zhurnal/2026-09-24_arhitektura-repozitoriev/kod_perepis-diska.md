# Канал исполнителя — perepis-diska (один заход до конца)
> Твой единственный файл-заход. Читай ТОЛЬКО его и названные якоря; проект не изучай.
<!-- собран bootstrap_zahod.py -->
<!-- гейт сборки заполненного: ЖДЁТ -->
> План/вопросы/отчёт — в секции внизу. Метрика — КАЧЕСТВО. Часы — норма.
> **Модель: Opus 5** — продукт захода — диагноз незнакомого диска: классификация и летопись рождаются по ходу, ошибка суждения «мусор или единственная копия» дорогая.

## СТАРТОВОЕ СООБЩЕНИЕ ВЛАДЕЛЬЦУ

> Это блок для владельца — то, чем тебя запустили. Исполнителю здесь делать нечего, твоё задание ниже.

```
Модель: Opus 5.

Ты исполнитель на Mac владельца. Открой Claude Code в папке ~/Documents/GitHub/materials и сделай три хода:

1. git --no-optional-locks fetch origin claude/bold-faraday-wq09ql
2. git --no-optional-locks worktree add ../materials-wt/perepis-diska -b zahod/perepis-diska origin/claude/bold-faraday-wq09ql
   (папка или ветка уже есть — не пересоздавай, просто перейди в неё)
3. cd ../materials-wt/perepis-diska и прочитай ЦЕЛИКОМ файл-заход:
   _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/kod_perepis-diska.md

Работай строго по нему: он самоценный, проект сам не изучай. Заход только ЧИТАЕТ диск —
ничего не коммить, не пушь и не удаляй нигде, кроме своей папки perepis/.
Если заход поправлен после старта — смотри секцию ## ПРАВКИ ПОСЛЕ ВЫДАЧИ в конце файла.
```

── СЧЁТ НЕЗАКРЫТОГО (печать, не гейт) ──
ГРАНИЦА ОБЛАСТИ: сырые подстроки в `kod_*.md` (пункт 4) — НЕ парсер очереди `dostavit_urok` (который считает только пары ДОМ:/ДОСТАВЛЕНО:). Разница в числах — законна.
🔴 снимок при сборке 2026-09-24, ПРОВЕРЬ ПЕРВЫМ ХОДОМ: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/schet_nezakrytogo.py _studio/zhurnal/2026-09-24_arhitektura-repozitoriev`
Область: «_studio/zhurnal/2026-09-24_arhitektura-repozitoriev» — сужены пункты 1, 3, 4; долги (2) глобальны намеренно (DOLG.md не размечен по записям).
Приоритет владельца: разобрать инциденты важнее, потом закрыть долги — неразобранный инцидент это повторяющаяся ошибка, долг может подождать.
  1. инцидентов без вердикта             : 0
  2. долгов СТАТУС: ЖИВ                  : н/д — ни одного skills/*/DOLG.md нет на диске (другой git-репозиторий)
  3. уроков фабрике без ВЕРДИКТ          : 0
  4. пунктов очереди «ДОСТАВЛЕНО: нет»   : 0

КОНТЕКСТ. <проект в 1–2 фразы>. Прошлый этап: <состояние>. ЦЕЛЬ: <что закрыть>.
Приёмка — по ОТЧЁТУ, без построчной сверки. <Если стоп до цели: получишь X, но НЕ Y.>

## ЧТО ФИНАЛИЗИРОВАНО НА ИНТЕРВЬЮ

ИНТЕРВЬЮ ПРОВЕДЕНО: да (2026-09-24) — флаг `--intervyu da` при сборке. ⚠ Он доказывает, что аналитик не ЗАБЫЛ про интервью, и НЕ доказывает, что разговор был.

1. Подметание Mac делаем воронкой массовых правил, не разбором каждого проекта по содержанию; первый заход — только перепись и летопись, ничего не меняет
2. Области обхода: ~/Documents/GitHub, папка книг в ~/Documents, ~/Downloads, корень домашней папки, папка Claude; исполнитель — Opus; владелец в цикле не участвует, отчёт читает аналитик

## КОНТРАКТ ЗОНЫ (обязателен — не удалять; вписан Cowork)
- **МЕСТО РАБОТЫ:** **рабочая папка `/Users/ivanyakovlev/Documents/GitHub/materials-wt/perepis-diska`** — МЕСТО ВСЕЙ РАБОТЫ (worktree захода, ветка `zahod/perepis-diska` в ней уже стоит). 🔴 **ПЕРВЫЙ ХОД — `cd /Users/ivanyakovlev/Documents/GitHub/materials-wt/perepis-diska`; ДАЛЬШЕ — ТОЛЬКО ПУТИ ОТНОСИТЕЛЬНО ЭТОЙ ПАПКИ** (или `cd` в неё безусловно, каждым ходом): `python3 _generator/tools/…` зовёт копию инструмента в ней же, пути зоны и арки — её файлы. Абсолютный путь в главную папку репозитория здесь — типичная ошибка, правка утекает МИМО worktree и найдётся только на коммите («вне git» в `git_zona.py check --zone` из рабочей папки, на файле, который уже правил, — цена, оплаченная живьём: 5 файлов, ручное копирование и откат главной папки). 🔴 `git checkout` в основной папке ЗАПРЕЩЁН: рядом идут другие заходы, переключение подменит файлы у них под ногами. 🔴 **Файл-заход — КОПИЯ `_studio/zhurnal/2026-09-24_arhitektura-repozitoriev/kod_perepis-diska.md` в твоей рабочей папке**: ПЛАН/ВОПРОСЫ/ОТЧЁТ/УРОКИ пишешь в неё и коммитишь её в свою ветку вместе с зоной (путь копии в зоне уже есть). Копии в папке нет — перенеси её из основной ветки: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py adopt --branch claude/bold-faraday-wq09ql --zone _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/kod_perepis-diska.md --yes` (дирижёр волны кладёт её сам при старте). Существующую копию не затирай: в ней твоя работа. Отчёт читают в ней: дирижёр — сразу, приёмка — после влития ветки. При влитии копия может дать конфликт add/add с файлом-заходом основной ветки (ветка заведена раньше, чем заход попал в git) — это законно и разрешается объединением: план, вопросы и отчёт — из копии, правки после выдачи — из основного файла. 🔴 **Ветку в конце вливаешь САМ, последним ходом, после коммита зоны** (решение владельца 25.08; полный порядок печатает WARNING-блок ниже).
- **ЗОНА (можно менять):** `_studio/zhurnal/2026-09-24_arhitektura-repozitoriev/perepis/` `_studio/zhurnal/2026-09-24_arhitektura-repozitoriev/kod_perepis-diska.md`. Всё вне — **READ-ONLY**: не править, не двигать, не удалять, не рефакторить «заодно».
- 🔴 **ЗАВЁЛ НОВЫЙ `.md` — РЕГИСТРИРУЕШЬ ЕГО САМ, ТЕМ ЖЕ ХОДОМ, ОДНОЙ КОМАНДОЙ:** `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/register_doc.py <путь> "<описание>"` (из корня репо). `_studio/docs/` тебе по-прежнему READ-ONLY **для правки руками** — дверь ровно одна, и это она. Дверь идемпотентна (повторный вызов дубля не заведёт) и отказывает на пути вне `_studio/`, на несуществующем файле и на пустом описании. Свой файл-заход регистрировать не нужно: он рождается зарегистрированным из `bootstrap_zahod.py`. **Красный хук на ТВОЁМ новом `.md` — это не повод для `--no-verify`, а повод позвать дверь.** *(история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц1) Обходить больше нечего.*
- **КОММИТ:** два хода — `add` по своим путям, затем `commit` **с теми же путями после `--`** (полная форма и цена каждого хода — §4); коммить ПО ХОДУ работы, не одним последним ходом (§4). НИКОГДА `-A` / `.` / `commit -am`, и никогда `commit` без путей. Субагенты не коммитят. **`--no-optional-locks` обязателен:** обычный git переписывает индекс, берёт `.git/index.lock` и роняет параллельный ручной коммит владельца.
- **SCRATCHPAD — ТОЛЬКО ЛИЧНЫЙ.** Черновики, выкладки, промежуточные версии — в личную папку СВОЕГО захода `scratchpad/perepis-diska/`. Общие пути (`scratchpad/otchet.md`, любой `scratchpad/*` без имени твоей темы) ЗАПРЕЩЕНЫ: чужой отчёт уедет в твой файл или твой — в чужой, а приёмка читает отчёт без построчной сверки и подмену НЕ ЛОВИТ по построению. (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц2)
- 🔴 **Звал `register_doc.py` — допиши `_studio/docs/KARTA.md` к своим путям В ОБОИХ ходах.** Строка регистрации лежит физически в нём. Ворота 5 читают `§6` **с диска**, а не из индекса: коммит без этого файла пройдёт ЗЕЛЁНЫМ, документ уедет сиротой, а строка умрёт при первом `checkout` (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц3).
- **ЗАПРЕТ:** ничего за пределами зоны, даже если «мешает» или «чинится в одну строку». Нашёл проблему вне зоны → в отчёт, не трогай.

## 0. ПЕРВЫЙ ХОД
### 0.1 🔴 ГИТ-КОНТУР — ДО ВСЕГО ОСТАЛЬНОГО, И ПЕРВЫМ ХОДОМ ЦЕЛИКОМ

🔴 «ничего сверх задачи» относится к СОДЕРЖАНИЮ работы; git-контур §0.1 — законное исключение, он про состояние репозитория и исполняется целиком.

🔴 **ПОРЯДОК ЗДЕСЬ — ЧАСТЬ УСТРОЙСТВА, А НЕ ОФОРМЛЕНИЕ. Сначала САМ прогоняешь две команды самопроверки контура (пункт 1 ниже), и только ПОТОМ заводишь свою рабочую папку** — её ветка отпочковывается от основной такой, какая она есть на момент запуска: контур пуст, доносить инструмент влитием нечего.

🔴 Очередь заявок подметена на входе волны, твоё дело здесь — только своя зона: закрывает и вливает очередь роль коммитера (`agents/kommiter.md`), один раз на входе волны и один раз на выходе (`python3 _generator/tools/bootstrap_zahod.py --podmetanie-volny vhod|vyhod`), не сборка этой позиции.

**1. ВЕСЬ КОНТУР ПУСТ — САМОПРОВЕРКА ВМЕСТО СУБАГЕНТА.** При сборке проверены два числа ПОЗИЦИОННОГО контура, и оба нулевые: невлитых `zahod/*`-веток 0 (🔴 снимок при сборке 2026-09-24, ПРОВЕРЬ ПЕРВЫМ ХОДОМ: `git --no-optional-locks branch --no-merged claude/bold-faraday-wq09ql | grep -c 'zahod/'`); названных `--vlit` 0. Звать субагента не за чем — выполни САМ две команды и вставь их вывод в `## ОТЧЁТ` дословно:
```
git --no-optional-locks branch --no-merged claude/bold-faraday-wq09ql | grep -c 'zahod/'   # снимок при сборке 2026-09-24: 0
python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/perepis/
```
Первая вернула не 0 — НИЧЕГО чужого не вливай (свою ветку вольёшь последним ходом, см. ниже), назови число строкой в `## ОТЧЁТ` и работай дальше. Вторая красная — сначала приведи в порядок свою зону.

Если при следующей сборке невлитых веток или названных `--vlit` окажется хоть одна, генератор сам вернёт сюда задание субагенту гит-контура — печатает его дверь `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/bootstrap_zahod.py --zadanie-subagentu`; звать его в этом заходе не надо.

🔴 ОТВЕТ ЛЮБОГО субагента, которого ты запускаешь (не только этого), обязан КОНЧАТЬСЯ строкой «выдано N позиций из M найденных»: канал мог оборвать его молча, и без этой строки усечение неотличимо от честного «мало нашлось». Нет строки — ответ усечён, в `## ОТЧЁТ` не вставляй, перезапроси.

**2. ТЕПЕРЬ ЗАВОДИ СВОЮ РАБОЧУЮ ПАПКУ** (команда — в блоке «МЕСТО РАБОТЫ» выше) и работай в ней как обычно. Её ветка отпочкована от свежей основной, поэтому инструмент, которым ты работаешь, уже на диске — отдельного «влить перед работой» больше нет.

вливать нечего, проверено командой `git branch --no-merged` — но проверено ПРИ СБОРКЕ, а не сейчас: невлитых `zahod/*`-веток было 0. 🔴 снимок при сборке 2026-09-24, ПРОВЕРЬ ПЕРВЫМ ХОДОМ: `git --no-optional-locks branch --no-merged claude/bold-faraday-wq09ql | grep -c 'zahod/'`. Число могло устареть между сборкой и твоим прогоном — 14.08 заход нёс ровно этот ноль, а к прогону невлитых было три.


- деплоя в этом заходе нет.

- `cd /Users/ivanyakovlev/Documents/GitHub/materials-wt/perepis-diska` — ПЕРВЫЙ ХОД: рабочая папка, все пути захода — от неё. Ветку НЕ переключай: `zahod/perepis-diska` в ней уже стоит.
- Проверить, что на месте: `git rev-parse --abbrev-ref HEAD` → должно быть `zahod/perepis-diska`.
- ПЛАН/ВОПРОСЫ/ОТЧЁТ/УРОКИ ФАБРИКЕ пиши в КОПИЮ этого файла в рабочей папке — `_studio/zhurnal/2026-09-24_arhitektura-repozitoriev/kod_perepis-diska.md` — и коммить её в свою ветку вместе с зоной.
- Точка отката: `git add _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/perepis/ _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/kod_perepis-diska.md` → commit (или zip), если зона не чиста в HEAD (не фабрикуй, если чиста).
- Прочитать ТОЛЬКО: `названные файлы-якоря`. Проект не изучай.
- ПЛАН — в `## ПЛАН` перед действиями.

## 1. ДИСЦИПЛИНА (Карпатов)
🔴 **Развилку ВНУТРИ своей зоны решаешь сам** — называешь решение в `## ПЛАН` и идёшь дальше; спрашивать и ЖДАТЬ ответа владельца — только там, где любой выбор делает работу опасной или бессмысленной. Целый прогон уже вставал на вопросе, ответ на который лежал в собственном контракте зоны исполнителя (урок арки `2026-08-20_poryadok-v-metaskillah`).
🔴 **Не собирай `rm` с путём из переменных.** Защитный слой перехватывает такие команды НЕЗАВИСИМО от Bypass permissions и останавливает работу до ответа человека — замер 20.09: 5 ч 48 мин при работающей машине. Вместо `cp X Y && rm X` пиши `mv X Y`; где не подходит — питон-скрипт ФАЙЛОМ, не однострочник с `rm`.
🔴 **Код возврата — ПЕРВЫМ, до содержательного вывода команды.** «Отработала» и «упала, а я читаю прошлое состояние» выглядят одинаково; сначала `echo $?`, потом выводы. То же с гейтами. (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц7)
Предпосылки/развилки назвать вслух; минимум без спекуляций; хирургия (строка → к заданию); критерий, который может провалиться. Якорные замены — abort при ≠1. Сохранять по умолчанию. **Оспорить ложную предпосылку — включая КРИТЕРИЙ ГОТОВНОСТИ: считаешь его кривым — скажи в `## ПЛАН`, ДО работы, и предложи поправку.** Субагенты: ≤5, рейт-лимит = отступить + доложить (не слепой ретрай).

🔴 **Пишешь содержательный текст — термин НЕ употребляется раньше, чем определён**, включая заголовки, подводки и формулировки теорем. «Определение в тексте есть» не считается: если оно ниже первого рабочего употребления, читатель встаёт ровно там. Чинится ПЕРЕСТАНОВКОЙ определения вверх, не дописыванием пояснения. Гейт: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/check_termin.py <src>` (exit 1 при нарушении). Канон — `../docs/kak-delat/STANDART-teksta.md` правило 11. (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц8)

## 2. ЗАДАЧА

🔴 **WRITE YOUR `## ОТЧЁТ`, `## ПЛАН` AND `## ВОПРОСЫ` IN ENGLISH, AND EVERY FILE AND EVERY COMMIT MESSAGE YOU PRODUCE TOO.** Owner's decision 30.08. Fixed Russian addresses stay Cyrillic: `ЦЕНА:` · `ВЕРДИКТ:` · `ДОМ:` · `ДОСТАВЛЕНО:` · `ПОДЪЁМ:` · `[ДОЛГ: …]` · every `## ` heading of this file · every path and command.

### 2.0 Why this pass exists — the whole context you need

The owner is moving work to cloud Claude Code sessions. A cloud session sees only what is committed and pushed to GitHub. The Mac holds work that never reached GitHub: uncommitted files, unpushed branches, whole local-only projects. On 2026-09-24 the project `moskva` turned out to be such a project; the old Cowork project "Готовимся к ЕГЭ" lives outside GitHub entirely. The cleanup ("подметание") is done as a FUNNEL of mass rules, never by reading projects one by one. **This pass is step 0 of the funnel: a READ-ONLY census.** It produces the numbers from which the analyst writes pass 2 (the actions).

🔴 **СТОП ДО ЦЕЛИ: you deliver the census, the chronology and the proposed funnel shares — NOT any cleanup.** Nothing is committed, pushed, deleted, moved, merged or stashed anywhere except your own zone. The cleanup is pass 2, written by the analyst from your numbers.

### 2.1 Where to look — roots, checked by `ls` as your first measuring move

| root | what | depth |
|---|---|---|
| R1 | `~/Documents/GitHub` — every git working tree: a folder with a `.git` DIRECTORY (main checkout) or a `.git` FILE (linked worktree) | up to 4 levels |
| R2 | `~/Documents` top level, except `GitHub` — including the books folder (its exact name is unknown: find it by listing) | top level + sizes |
| R3 | `~/Downloads` top level | top level + sizes |
| R4 | `~` top-level FILES (not dotfiles), and any folder named like `Claude` (case-insensitive) in `~` or `~/Documents` | top level |
| R5 | `~/.claude/projects` — one subfolder per Claude Code project; count `*.jsonl`, oldest and newest mtime. DO NOT read the jsonl content | one level |

Skip `~/Library`, system folders and every other dotfolder. A root that does not exist → a line in the report, not an error.

### 2.2 What to collect — five TSV files and one report, all in `_studio/zhurnal/2026-09-24_arhitektura-repozitoriev/perepis/`

Write the collecting script in `/tmp/perepis-diska/` (NOT in the repository: code does not belong in `materials`). The script is disposable; attach its final version to the report as a fenced block so the analyst can rerun it.

1. **`repos.tsv`** — one row per git working tree found in R1. Columns: `path` · `kind` (main | worktree) · `origin_url` (or `none`) · `head_branch` · `default_branch` (from `origin/HEAD`, or `none`) · `dirty_tracked` · `untracked` · `porcelain_before` · `porcelain_after` · `size_mb` · `first_commit_date` · `last_commit_date` · `commit_count` · `newest_file_mtime` (excluding `.git`) · `readme_title` (first `#` heading of `README.md` or `CLAUDE.md`, or empty) · `funnel_rule` (see 2.3).
2. **`branches.tsv`** — one row per LOCAL branch of every main checkout. Columns: `repo_path` · `branch` · `has_upstream` · `ahead` · `behind` · `in_default` (is the branch tip an ancestor of `origin/<default_branch>`: yes | no | n/a) · `last_commit_date`.
3. **`folders.tsv`** — one row per non-git folder in R1–R4 (and per non-git top-level folder inside R1). Columns: `path` · `size_mb` · `file_count` · `oldest_mtime` · `newest_mtime` · `n_books` (pdf, djvu, epub) · `n_images` · `n_text` (md, html, tex, txt) · `n_code` (py, sh, js) · `n_other` · `funnel_rule`.
4. **`sessions.tsv`** — R5. Columns: `project_dir` · `jsonl_count` · `oldest_mtime` · `newest_mtime`.
5. **`big-files.tsv`** — the 100 largest files over 1 MB across R1–R4 (inside git trees too, excluding `.git`). Columns: `path` · `size_mb` · `ext` · `tracked_in_git` (yes | no | not-a-repo).
6. **`REPORT.md`** — sections: census summary · funnel distribution · chronology · duplicates · surprises. Details in 2.3–2.4.

Git commands: always `git --no-optional-locks`. **`git fetch --prune origin` in each repo is ALLOWED and REQUIRED before computing ahead/behind/in_default** — it only updates remote-tracking refs, it touches no work. A fetch that fails (no network, no access) → the row gets `fetch_failed` in `in_default`, and the report counts such repos.

`porcelain_before` / `porcelain_after`: the number of lines of `git --no-optional-locks status --porcelain` at the START of your pass and at the END. They must be equal in every row: this is the machine proof that the pass changed nothing.

### 2.3 The funnel — assign every repo and every folder exactly ONE candidate rule

These are the analyst's draft rules (arc diary, 2026-09-24, seventh round). You do not act on them; you COUNT them. If a better mass rule is visible in the data, add it as a new code and say so — that is a welcome result.

| code | rule (first match wins, top to bottom) |
|---|---|
| `R1-ok` | repo clean, every local branch pushed and `in_default=yes` (or pushed with upstream equal) — nothing to save |
| `R2-push` | clean, but some branch has `ahead>0` or no upstream — needs only a push |
| `R3-park` | dirty or untracked files — needs a park commit on a `park/<date>` branch |
| `R4-dup` | same `origin_url` as another row — an extra checkout of one repo (mark ALL rows of the group; the report names which one looks primary and why) |
| `R5-norepo` | non-git folder with owner content (text/code) — candidate for a private archive repo |
| `R6-books` | folder dominated by books/scans (`n_books` largest class) |
| `R7-junk` | Downloads/home-root/Claude-folder leftovers generated by sessions |
| `R8-unclear` | none of the above — the only class where content will have to be read |

Also: a repo with `origin_url=none` is a separate flag column-worthy fact — say how many.

**Distribution is printed as a Counter, not a paragraph:** `Counter(funnel_rule)` over `repos.tsv` and over `folders.tsv` separately, plus for each code: how many objects and how many MB.

### 2.4 Chronology — dates, not prose

From `first_commit_date`, `last_commit_date` (repos) and `oldest_mtime`/`newest_mtime` (sessions): a month-by-month table since 2026-01 — repos started, repos last touched, Claude Code projects active. Then check the owner's recollection against the data (**refutation is a full success; "the data cannot say" is lawful if you name what is missing; the only defect is an invented date**):
- Cowork in use since about early June 2026;
- the `disciplina` plugin and skills about a month later;
- the orchestrator and waves since about late August.
Also list: projects started and abandoned within ≤2 days of first commit; projects active for more than a month.

### 2.5 What NOT to do — each line kills a named failure

- no `commit`, `push`, `stash`, `checkout`, `reset`, `worktree prune`, `gc`, `branch -d` in ANY repository except your own zone in your own worktree — **enemy: a census that silently changes what it measures**;
- no reading of file CONTENT beyond the first `#` heading of `README.md`/`CLAUDE.md` — **enemy: the pass turning into a per-project review, which the owner explicitly refused**;
- no judgement of personal data: student names or profiles in a repository are NOT a finding (owner, 2026-09-24: not critical, do not raise it) — **enemy: a recurring false alarm the owner has asked executors to stop raising**;
- no writing into `materials` outside the zone, including the script — **enemy: code in `materials`**.

### 2.6 Delivery — this pass does NOT merge

The generic WARNING block below orders "влитие своей ветки в основную" and "пост-проверка из главной папки" (its steps 2 and 3). **For this pass they are CANCELLED:** the branch is read by the analyst from GitHub, and whether the arc's documents go into `arka/mat-kostyak` is decided in pass 2. Your delivery is: commit your zone (§4) → `git --no-optional-locks push -u origin zahod/perepis-diska` → steps 1, 4, 5, 6 of the WARNING block as written. Do NOT run `worktree drop`: the analyst may send a correction.

Subagents: up to 3, for example one per root group; each writes its TSV to disk along the way (a dying subagent hands over nothing) and ends its answer with "delivered N rows of M found".

**КРИТЕРИЙ ГОТОВНОСТИ (может ПРОВАЛИТЬСЯ):**
The whole criterion is a живой прогон на реальном объекте — the Mac disk itself, there is no fixture. All six files exist in `_studio/zhurnal/2026-09-24_arhitektura-repozitoriev/perepis/` (`ls _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/perepis/ | wc -l` → 6 or more); **coverage**: Y = `find ~/Documents/GitHub -maxdepth 4 -name .git | wc -l`, counted and written into `## ПЛАН` BEFORE the census starts; `repos.tsv` has exactly Y data rows, and the report states "checked X of Y" with X = Y; **nothing changed**: `porcelain_before == porcelain_after` in every row of `repos.tsv` (`awk -F'\t' 'NR>1 && $8!=$9' repos.tsv | wc -l` → 0, column numbers adjusted if you reorder); **distribution**: every row of `repos.tsv` and `folders.tsv` has a non-empty `funnel_rule`, and the two Counters in `REPORT.md` sum to the row counts; the branch `zahod/perepis-diska` is on GitHub (`git --no-optional-locks ls-remote origin zahod/perepis-diska` prints one line).
**Отрицательный вердикт несёт ОХВАТ В СЕБЕ:** не «дыр не найдено», а «дыр не найдено, проверено X из Y». Без охвата вердикт не принимается — «проверено 2 из 9» и «проверено 9 из 9» выглядят одинаково.

## 3. ВЕРИФИКАТОР (если двигаем/теряем/жмём)

Верификатор не нужен: заход только читает диск и пишет отчёт; сверку делает приёмка аналитика по сырым TSV, которые заход обязан приложить.

## 4. 🔴 КОММИТ СВОЕЙ ЗОНЫ — ПО ХОДУ РАБОТЫ, НЕ ОДНИМ ПОСЛЕДНИМ ХОДОМ
Ты работаешь host-side и в `.git` ПИШЕШЬ — значит коммитишь САМ, никому не передавая. Каждую завершённую часть работы коммить СРАЗУ, теми же двумя ходами — не копи всё к финальному ходу:
```
git --no-optional-locks add -- _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/perepis/ _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/kod_perepis-diska.md                     # вводит НОВЫЕ пути в индекс
git --no-optional-locks commit -m "<зона>: <что сделано>" -- _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/perepis/ _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/kod_perepis-diska.md   # отсекает всё чужое
python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone <зона>   # из корня репо; должен быть ✅
git --no-optional-locks show --stat                        # обязаны быть ТОЛЬКО твои пути
```
🔴 **КОММИТЬ ПО ХОДУ — РЕШЕНИЕ ВЛАДЕЛЬЦА 25.08 (В11), ПЕРЕВЕРНУВШЕЕ прежний канон «одним последним ходом».** (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц10) Закончил кусок — закоммитил его; последний ход только ПРОВЕРЯЕТ, что коммитить нечего (`git status --porcelain` пуст, `git_zona.py check --zone` ✅).
🔴 **ОБА хода обязательны, ни один не лишний** (полное «почему» и цена — `../docs/kak-delat/GIT-disciplina.md §3`):
- **`add`** — pathspec-коммит знает только **отслеживаемые** пути; новый файл без `add` даёт `did not match any file(s) known to git`.
- **`-- <пути>` в самом `commit`** — иначе `commit` забирает индекс ЦЕЛИКОМ, вместе с чужим, застейдженным кем угодно рядом с тобой (репо `materials/` общий, писателей трое). (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц11)
⚠ **Хук `pre-commit` покраснел — сначала посмотри, на ЧЬИХ путях.**
- Красное на ТВОИХ путях (новый `.md` не зарегистрирован в `../../docs/KARTA.md §6`, битая ссылка) — **чини, не обходи**: там только твоё, обходить нечего.
- Красное на ЧУЖОМ, унаследованном долге (ворота дают сотни ❌ старых нарушений) — законный обход, но ТОЛЬКО с причиной; голый `--no-verify` инструмент отклонит, а причина сама уедет в `INCIDENTY.md`:
```
python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py commit --zone <зона> \
    --no-verify "чужой долг: <что именно покраснело>" -m "<что и зачем>" --push
```
Ту же причину назови отдельной строкой отчёта долгом. (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц12)
**Коммит не прошёл по ВНЕШНЕЙ причине** (чужой лок, конфликт, detached HEAD) — чужое состояние репозитория НЕ чини: зафиксируй файлы и напиши в отчёт отдельной строкой «коммита нет, причина такая-то, нужно ваше действие». Это законный отчёт. Молчаливое «сделано» при незакоммиченной зоне — брак: приёмка гоняет тот же гейт первым ходом и завернёт отчёт, не читая (`RUKOVODSTVO §Приёмка`, гейт 0).

## 4.1 🔴 ГИГИЕНА — ПРОВЕРКИ ПЕРЕД СДАЧЕЙ (вшито `bootstrap_zahod.py`; исполнителю НЕ удалять)
> Раздел про СОСТОЯНИЕ РЕПОЗИТОРИЯ после твоей работы, а не про правильность
> этого файла и не про планы: правильность файла судят С1/С3/С7 `check_sborki.py`
> ДО прогона, намерение «что влить/коммитить/закрыть» — блок §0.1 ГИТ-КОНТУР.
> Здесь не повторяется ни то, ни другое. Каждый пункт — КОМАНДА; её вывод, а не
> пересказ, уходит в `## ОТЧЁТ`. Пункт неприменим — так и напиши: «неприменимо,
> потому что …». **Молчание читается как «не сделано», а не как «всё чисто».**
> ⚠ `Г1`–`Г6` ниже — пункты ЭТОГО раздела. Гейты `priyomka.py` (`Г7` в секции
> `## ВОПРОСЫ`) — ЧУЖАЯ семья с той же буквой: их гоняет приёмка, не ты.
> (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц13)

**ЗОНА ГИГИЕНЫ:** `_studio/zhurnal/2026-09-24_arhitektura-repozitoriev/perepis/` `_studio/zhurnal/2026-09-24_arhitektura-repozitoriev/kod_perepis-diska.md`

- **Г1. Зона доехала в git.** `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/perepis/` → ✅; `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/kod_perepis-diska.md` → ✅. Красное на любой из команд — отчёт не принимается: приёмка гоняет их все первым ходом.
- **Г2. Второй репозиторий.** **неприменимо, и это проверено при сборке, а не предположено:** все пути зоны лежат внутри репозитория `materials` (тот же критерий, что у С2 `check_sborki.py`). Зона расширилась за его пределы по ходу — пункт снова применим; команда та же, что в применимом случае: `cd ../<репозиторий> && git --no-optional-locks status --porcelain` → пусто. *Команда названа и здесь нарочно (находка верификатора): пункт, который объявлен неприменимым и не говорит, ЧТО делать, когда станет применим, исполнить в этот момент нечем.*
- **Г3. Невлитых веток не прибавилось.** `git --no-optional-locks branch --no-merged claude/bold-faraday-wq09ql` — число сравни с тем, что было на входе. Выросло — назови, чьи ветки и почему они законны.
- **Г4. Новый инструмент имеет живую точку вызова.** Завёл `.py` в `_generator/**` — `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/check_tool_contract.py <свои новые файлы>` → rc=0. Ни одного нового `.py` — так и напиши. *Инструмент без точки вызова зелен ровно потому, что его никто не звал.*
- **Г5. Новый `.md` зарегистрирован.** Завёл — звал ли ты `register_doc.py` и лежит ли строка на диске: `grep -c '<имя файла>' <карта своего корня>` → 1. Карту своего корня называет `korni.карта_для('<путь>')`, руками её не угадывай.
- **Г6. В коммите нет чужих путей.** `git --no-optional-locks show --stat` — только твои пути. Чужой путь в своём коммите — это чужая работа, унесённая твоим `commit` без `--`.

## 5. ОТЧЁТ → секция `## ОТЧЁТ` внизу
Что сделал + ЗАЧЕМ / как проверил / что НЕ трогал / вопросы / результат верификатора / открытое «возвращаться» / **время прогона + токены — на канале `app` НЕПРИМЕНИМО, снимать неоткуда** (лог прогона существует только на канале `terminal`, где его кладёт `tee`; сессия в приложении Claude Code такого следа не оставляет). Строку не заполнять числом и не извиняться за его отсутствие — это не недосмотр исполнителя, а свойство канала) / **ПОВТОРЯЕМОСТЬ находок (строка обязательна — см. ниже)** / **АРТЕФАКТ (строка обязательна)** / **КОММИТ (строка обязательна, см. §4)**.

🔴 **АРТЕФАКТ — АБСОЛЮТНЫЙ ПУТЬ К СОБРАННОМУ ФАЙЛУ, отдельной строкой.** Не «колода пересобрана», не «см. `dist/`», а путь, который владелец скопирует и откроет. *(история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц14) Отчёт без адреса артефакта — это отчёт о работе, которую нельзя посмотреть.*

🔴 **НЕОБРАТИМОЕ — ОТДЕЛЬНЫМ СПИСКОМ, даже если оно стояло в задании.** Удаление, перезапись, переименование, перемещение, `git reset`/`checkout` поверх несохранённого, любая правка, вышедшая за зону, — каждое ОДНОЙ строкой: **что · где · чем восстанавливается** (хэш коммита, путь к бэкапу). Ты запущен без запроса разрешений (`--dangerously-skip-permissions`): владелец НЕ видел ни одного из этих действий в момент, когда оно происходило, и этот список — единственное место, где он о них узнаёт. **Необратимого не было — напиши «необратимого нет».** Молчание от пустоты не отличается, и приёмка прочитает его как пустоту.

🔴 **ПОВТОРЯЕМОСТЬ находок — назови, какие из них повторятся на СЛЕДУЮЩЕЙ единице работы** (лекция/слайд/заход). Критерий вычислимый, не про приоритет: повторится — это НЕ пункт очереди, а заход ДО следующего прогона (правило «класс НЕМЕДЛЕННОЕ», `../../docs/kak-delat/RUKOVODSTVO-zahodami.md`). Не повторится — законно уходит в `## ВОПРОСЫ` пунктом очереди. *Пример владельца: белый фон иллюстраций повторился бы тринадцать раз, каждый раз ценой переделки картинки — заход, а не запись; число, вписанное аналитиком не глядя, на следующих слайдах не повторяется — запись, а не заход.* Находка сделана ПРОБНЫМ прогоном — чинится ДО следующего прогона: «проба, после которой ничего не починили, — потраченные токены».

## ⚠️🔴 WARNING · ПОСЛЕДНИЙ ХОД ПЕРЕД ОТЧЁТОМ — ПОЛНАЯ ГИТ-ГИГИЕНА. НЕ ПРОПУСКАТЬ 🔴⚠️

**СТОП. Прежде чем писать хоть строку в `## ОТЧЁТ` — прогони это целиком.** (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц15) Гит-контур §0.1 стоит в НАЧАЛЕ и разбирает то, что накопилось ДО тебя; этот блок
стоит в КОНЦЕ и разбирает то, что накопил ты сам. Один другого не заменяет.

**ПОРЯДОК ЖЁСТКИЙ, ОН НАЗВАН ВЛАДЕЛЬЦЕМ: коммит → влитие своей ветки в основную → пост-проверка
ИЗ ГЛАВНОЙ ПАПКИ → гашение → вывоз.** Обратный порядок не работает технически: влитие отказывает
на грязном дереве, пост-проверка неисполнима до влития, вывоз — на невлитом. (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц16) — теперь вливает САМ заход, но только при зелёной пост-проверке.

**1 · ВСЕ КОММИТЫ.** Ничего не осталось вне git — ни в рабочем репозитории, ни в соседних, до
которых ты дотянулся по ходу работы:
```
for R in <репозитории, которых ты касался>; do
  echo "== $R"; git -C $R --no-optional-locks status --porcelain
done
```
Своя зона — своими путями (`add` + `commit -- <пути>`). Чужая содержательная работа — НЕ твоя:
называешь строкой в отчёте и оставляешь. Пусто у всех — так и напиши числом «вне git 0».

**2 · ВЛИТИЕ СВОЕЙ ВЕТКИ В ОСНОВНУЮ.** Только после того, как шаг 1 дал «вне git 0» на своей
зоне — влитие отказывает на грязном дереве:
```
python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py vlit-v-osnovnuyu zahod/perepis-diska --zone <своя зона> \
    --vsyo-ravno "своя рабочая папка ещё жива — влитие последним ходом захода, штатно"
```
Конфликт — ЗАКОННЫЙ исход, не повод форсировать: разрешай по существу, если понимаешь обе
стороны; не понимаешь — `git_zona.py vlit-v-osnovnuyu --abort`, ветка остаётся невлитой,
строка в отчёт и заявка на влитие (`git_zona.py zayavka --rod git-operaciya`).
🔴 Конфликт на `README.md` — только ОБЪЕДИНЕНИЕМ записей реестра, никогда выбором стороны:
параллельные заходы волны дописали по строке — обе записи правы, выбор одной молча уничтожает
регистрацию соседа.

**3 · ПОСТ-ПРОВЕРКА ИЗ ГЛАВНОЙ ПАПКИ.** Отвечает на вопрос «механизм ВСТАЛ», а не «коммит
виден»: прогон изменённого механизма из основной папки `../../materials` (путь от корня рабочей папки), НЕ из рабочей папки `/Users/ivanyakovlev/Documents/GitHub/materials-wt/perepis-diska` плюс `grep` по ЖИВОМУ файлу,
который его зовёт (хук, конвейер, генератор):
```
cd ../../materials && <команда прогона механизма, который заход менял> && echo $?
grep -n '<как механизм назван в вызывающем коде>' <живая точка вызова>
```
🔴 **Красная пост-проверка = ОТКАТ ВЛИТИЯ И СТРОКА В ОТЧЁТ**, а не «доложу, пусть приёмка
решает»: `git_zona.py vlit-v-osnovnuyu --abort`, если слияние ещё не закоммичено, иначе
`git -C ../../materials --no-optional-locks reset --hard <хэш ДО влития>`. Заход, который влил
и сломал `main`, обязан вернуть `main` сам.

**4 · ГАШЕНИЕ.** Невлитого не осталось: `git --no-optional-locks branch --no-merged claude/bold-faraday-wq09ql`.
Каждая оставшаяся ветка названа поимённо с причиной, почему она жива. 🔴 Ветку-витрину (`main`
там, где с неё публикуется сайт) НЕ вливать — влитие туда есть публикация и решение владельца.

**5 · ВЫВОЗ.** Вывези СВОЮ ветку; `main` НЕ вывози: если после работы в нём есть невывезенное,
поставь заявку `--rod git-operaciya` и назови число в отчёте. Команда для своей ветки:
`git --no-optional-locks log --oneline @{u}.. | wc -l` → 0.
Ненулевое на своей ветке означает, что работа существует только на этом диске.

**6 · ПРОВЕРКА ФАКТОМ, А НЕ ПАМЯТЬЮ.** Числа по каждому репозиторию — вне git · невлитых своих
и чужих; невывезенных СВОЕЙ ВЕТКИ, не по каждому репозиторию · результат пост-проверки
(зелёная/откачена) — печатаются командой и уходят в `## ОТЧЁТ` дословно. Ненулевое число или
красная пост-проверка без объяснения — приёмка читает как несделанную работу: она гоняет те же
команды первым ходом.

🔴 **Отчёт без этих чисел не принимается.** «Я закоммитил» — не то же самое, что `status --porcelain`
пустой: за одну сессию работа не доезжала трижды, каждый раз с честным «сделано» в отчёте.
## УРОКИ ФАБРИКЕ — (заполняет исполнитель; пусто — нормальный исход)
> Находка не про эту сессию, а закономерность про саму фабрику, годная другим заходам, — оформи как пункт очереди в `## ВОПРОСЫ` (формат там же) с `ДОМ: <эта арка>/UROKI-FABRIKE.md`, а не пиши прямо сюда неструктурированной строкой.
> **Не про задачу — про САМУ ФАБРИКУ.** Ты работаешь с пустым контекстом и потому видишь то, чего не видит аналитик: он писал этот заход и ему приятно, что заход хорош. Сломался ВХОД (издание не то, id врёт, зона не содержит файла с ответом)? Критерий готовности кривой? Инструкция канона противоречит живому файлу? — сюда, строкой.
> Формат жёсткий (по нему гейт): `### <что произошло>` / `ЦЕНА: <что сломалось и сколько стоило>`.
> **ЦЕНА обязательна.** Без неё это наблюдение, а не урок, и в канон оно не пойдёт. Не знаешь цены — не пиши.
> **Не сочиняй.** Пустая секция — законный отчёт. Выдуманный урок хуже отсутствующего: он попадёт в канон, который читают ВСЕ будущие проекты.

## ПЛАН — (заполняет исполнитель)

Written 2026-09-25 before the census starts.

**Coverage target, measured before the census.** `find ~/Documents/GitHub -maxdepth 4 -name .git | wc -l` → **Y = 352** (13 `.git` directories = main checkouts, 339 `.git` files = linked worktrees). The same `find` prints `Permission denied` on `~/Documents/GitHub/proba-dolg-nedostupnaya-fixture`: it contributes nothing to Y, and I list it as a folder row that could not be read.

**Premises I checked and found false or off (stated before work, per §1):**
1. The base ref `claude/bold-faraday-wq09ql` does not exist as a LOCAL branch in the worktree (`fatal: malformed object name`), so the §0.1 command literally returns 0 by failing. I ran it against `origin/claude/bold-faraday-wq09ql` instead: `zahod/*` not merged = 0; all not-merged local branches = 1 (`main`, the showcase/default branch, not mine).
2. `schet_nezakrytogo.py _studio/zhurnal/2026-09-24_arhitektura-repozitoriev` refuses with rc=1: "under the area not a single file" (the tool reads the main checkout, where the arc folder does not exist yet; it only exists on the brief's branch). The 0/0/0/0 numbers in the header could therefore NOT be re-verified; this is reported, not fixed (outside zone).
3. §2.2 says `R1-ok` needs "every local branch pushed". With 339 worktrees, every branch that is checked out in a worktree also exists as a local branch of its main checkout. **Decision:** a branch checked out in a linked worktree is judged on that worktree's row; a main checkout is judged on its own HEAD plus the branches NOT checked out anywhere else. Otherwise every main would count the same unpushed branch as its worktree, and the numbers would double.
4. `R4-dup` ("same origin_url as another row") would, taken literally, tag all 339 worktrees, because a worktree shares the origin of its main by construction. **Decision:** `R4-dup` compares main checkouts only. For worktrees I propose a new code, `R9-wt-done`: a clean worktree whose HEAD commit is already in `origin/<default>`. It can be dropped with `worktree remove` and nothing is lost. The strict analyst version (no R9) is also written, as an extra last column `funnel_rule_strict`, so the analyst can compare both Counters. Columns 8/9 (`porcelain_before/after`) stay where the criterion expects them.
5. `R5-norepo` vs `R6-books` vs `R7-junk` with "first match wins" would make a books folder holding one `.md` into R5. **Decision:** R5 = text+code is the LARGEST content class and the root is R1/R2; R6 = books is the largest class (any root); R7 = remaining rows in R3/R4 (Downloads, home root, `~/Claude`) whose newest mtime is ≥ 2026-06-01 (the Claude-session era; this is a heuristic on dates and names, because the brief forbids reading content); everything else = R8. A folder under R1 that holds only git trees (the `*-wt` containers, `spetsmat` holding `spetsmat_db`) gets a new code `R0-holder`: its content is already in `repos.tsv`. Loose top-level files in R3 and R4 get one pseudo-row each (`<root>/[loose files]`), so that they are counted.

**Method.**
- One disposable Python script, `/tmp/perepis-diska/perepis.py` (the brief names `/tmp` explicitly), with a thread pool. No subagents: one script covers all five roots in one pass and keeps `porcelain_before` and `porcelain_after` in one process, so the "nothing changed" proof holds together.
- Order inside the script: (1) `porcelain_before` for all 352 trees FIRST; (2) `git fetch --prune origin` once per main checkout, because worktrees share refs with their main; (3) all other measurements; (4) `porcelain_after` LAST. Outputs go to `/tmp/perepis-diska/out/` and are copied into the zone only after the script ends, so my own worktree's row does not change during the measurement. The plan commit lands BEFORE the run for the same reason.
- File sizes and mtimes: one filesystem walk that skips `.git` and gives every file to the git tree it is nearest to, so a nested tree (`materials/carshering/carsharing_archive`) is not counted twice.
- Content is never read, except the first `#` line of `README.md`/`CLAUDE.md`. Session `*.jsonl` files: mtimes only.
- Chronology uses commit dates (`git log --all --format=%cI`) and `.git`-file mtimes (worktree creation). What the data cannot see (Cowork's own storage lives in `~/Library`, which is skipped) is named in the report, not guessed.

**Readiness criterion:** accepted as written; the run can fail it (X≠Y, porcelain mismatch, a missing push).

## ВОПРОСЫ — (заполняет исполнитель)
> Нашёл вещь, которая принадлежит чужому дому (термин/источник/урок/следующий заход) — не только вопрос владельцу? Оформи ПУНКТОМ ОЧЕРЕДИ, тремя строками:
> ```
> N. <текст находки>
>    ДОМ: <путь от корня репозитория | владелец>
>    ДОСТАВЛЕНО: нет
> ```
> 🔴 **`ДОМ:` — ОБЯЗАТЕЛЬНОЕ ПОЛЕ, И АДРЕС В НЁМ ОБЯЗАН СУЩЕСТВОВАТЬ В МОМЕНТ, КОГДА ТЫ ЕГО ПИШЕШЬ.** Путь, которого нет на диске, — не адрес: такую запись нельзя ни доставить, ни спросить, и она не чинится ничем. (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц17) Проверить СВОЙ файл до отчёта — одна команда:
> ```
> python3 _generator/tools/bootstrap_zahod.py --proverit-doma <этот файл>
> ```
> rc=0 — все дома достижимы; rc=1 — назван дом, которого нет (команда печатает какой именно). Тот же разбор гоняет `Г7` приёмки, и у него храповик: у ЭТОГО захода база 0, поэтому первый же недостижимый дом здесь — красный на приёмке, а не запись, которую через неделю никто не найдёт.
> `ДОМ: владелец` — законный адрес и НЕ недостижимый дом: он значит «дома-файла нет вовсе, решение за человеком». Не знаешь пути — пиши его, а не выдуманный путь. Для урока фабрике дом почти всегда `<эта арка>/UROKI-FABRIKE.md`. Аналитик при переносе меняет `ДОСТАВЛЕНО: нет` на `ДОСТАВЛЕНО: <имя-захода>#<N>` И дописывает ЭТУ ЖЕ строку-метку в файл по адресу ДОМ — `priyomka.py` (Г7) красным ловит и «доставлено» без метки на месте, и недостижимый дом сверх базы; достижимое-недоставленное печатает.
> 🔴 **Метку ставь ТОЛЬКО одним ходом вместе с самим переносом содержания, никогда раньше.** Гейт проверяет факт «строка-метка на месте», а не смысл «содержание перенесено верно» — метка без содержания рядом даст ложно-зелёный Г7.

1. The §0.1 self-check `git --no-optional-locks branch --no-merged claude/bold-faraday-wq09ql | grep -c 'zahod/'` can never be red in a worktree made by the starter message. The base exists there only as `origin/claude/bold-faraday-wq09ql`, so `git` fails with `fatal: malformed object name`, and `grep -c` still prints `0`. The generator should emit the `origin/…` form, or check that the ref exists. The same false green hits Г3 and step 4 of the WARNING block.
   ДОМ: _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/UROKI-FABRIKE.md
   ДОСТАВЛЕНО: нет
2. `schet_nezakrytogo.py _studio/zhurnal/2026-09-24_arhitektura-repozitoriev` (the brief's "check first" command) refuses with rc=1 ("under the area not a single file"). The arc folder exists only on the brief's branch, not where the tool reads. As a result, the header's 0/0/0/0 for this pass could not be re-verified.
   ДОМ: _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/UROKI-FABRIKE.md
   ДОСТАВЛЕНО: нет
3. For pass 2, rules. (a) `R4-dup` is unreachable under "first match wins": every repository is R1/R2 (clean) or R3 (dirty) before R4 is ever tested. Also, no two main checkouts share an origin. It is better as a flag column. (b) Proposed new codes, with counts in `perepis/REPORT.md` §2: `R9-wt-done` (110 worktrees), `R10-wt-residue` (44), `R0-holder` (4), `R0-empty` (2).
   ДОМ: _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/PLAN.md
   ДОСТАВЛЕНО: нет
4. Tracked files that tools rewrite in every worktree make finished worktrees look dirty:
   - `disciplina`: `_generator/tools/.hook-otkaz-chuzhoj-volny.log`, `doma/zahody/MODELI-ZHIVOST.json`, `.githooks/zamer-skillov.json`;
   - `spetsmat-bot`: `docs/index.html`;
   - `materials`: `teorkat-vvedenie/L2/dist/index.html`.

   Under the strict rules they add 44 worktrees to R3-park. Candidates: untrack plus `.gitignore`, or write the files outside the tree. This will repeat on every new worktree, so it is a pass, not a queue entry (see ОТЧЁТ, repeatability).
   ДОМ: _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/PLAN.md
   ДОСТАВЛЕНО: нет
5. Three repositories have no remote and exist only on this disk: `london-avgust-2026`, `materials/carshering/carsharing_archive` (nested inside `materials`) and `spetsmat/spetsmat_db`. Also, `materials/kurs leto 2026/6-lending/lendingi` has its own `.git` at depth 6, outside the census predicate. Where these four should live is the owner's decision.
   ДОМ: владелец
   ДОСТАВЛЕНО: нет

## ГИГИЕНА ВХОДА — (заполняет СУБАГЕНТ гит-контура, не исполнитель)
> 🔴 **Каждый заход — ДВЕ независимые работы.** Первая — навести полную гигиену со всем, что
> накопилось к этому моменту. Вторая — собственно заход. Друг от друга они не зависят, но
> **первая обязательна ВСЕГДА**: без заполненной секции отчёт не принимается (гейт Г12 `priyomka.py`).
>
> 🔴 **ГАЛОЧКА — НЕ ИСТОЧНИК ИСТИНЫ.** Приёмка прогоняет те же команды заново и сравнивает
> с заявленным; расходится — красный НЕЗАВИСИМО от галочки. (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц18)
>
> 🔴 **СНИМОК ВХОДА снимается ДО работы.** Без него «все долги закрыты» непроверяемо: неизвестно,
> какие были. Пустой снимок = красный.

**СНИМОК ВХОДА** *(команды и их ВЫВОД, а не пересказ; снять ПЕРВЫМ ходом, до всякой работы)*
```
git --no-optional-locks branch --no-merged <основная>     # невлитые
git --no-optional-locks status --porcelain | wc -l        # не закоммичено
git --no-optional-locks log --oneline @{u}.. | wc -l      # не вывезено
python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py zayavki              # открытые заявки
```
Taken by the executor (no git-contour subagent was called: §0.1 says the contour was empty at build time). Worktree `materials-wt/perepis-diska`, before any work. The base is given as `origin/claude/bold-faraday-wq09ql`, because the local form fails (see ВОПРОСЫ 1).
```
$ git --no-optional-locks branch --no-merged origin/claude/bold-faraday-wq09ql
  main
$ git --no-optional-locks status --porcelain | wc -l
       0
$ git --no-optional-locks log --oneline @{u}.. | wc -l
       0
$ python3 …/git_zona.py zayavki     (last line)
Охват: заявок открыто 13, переадресовано 12, закрыто недавно (sdelano) 76, постоянных исключений 1, сторож краснеет на 0, держателей 0, двойной захват на 0
```

**ЧТО СДЕЛАНО** *(с хэшами)*
Nothing was merged, pushed or closed at entry. This pass is read-only outside its zone (§2.5), so the 13 open requests belong to other people and are not mine to close.

**ВСЕ ДОЛГИ ВХОДА ЗАКРЫТЫ:** `нет`. Here is what remains and why:
- The 13 open requests of `git_zona.py zayavki`: closing them is the committer role's job at the wave entry/exit (§0.1), and this pass is forbidden to change any repository.
- The branch `main` is not merged into the base: it is the showcase/default branch, and merging it is the owner's decision (WARNING step 4).
*(`нет` законно — но ТОЛЬКО со списком поимённо: что осталось и почему это непроходимо ТВОИМИ
правами (чужая живая рабочая папка, нужно решение владельца, конфликт, обеих сторон которого
не понимаешь). «Сложно» и «не моя тема» причинами не являются. `нет` без списка = красный.)*

## ОТЧЁТ — (заполняет исполнитель)
ПРАВКИ ПРОЧИТАНЫ: 1

**АРТЕФАКТ:** `/Users/ivanyakovlev/Documents/GitHub/materials-wt/perepis-diska/_studio/zhurnal/2026-09-24_arhitektura-repozitoriev/perepis/REPORT.md`. Open it in any Markdown viewer. The raw rows are in the five `*.tsv` files next to it; open them in Numbers or Excel.
*(собрал HTML, документ, PDF, картинки — путь сюда. Собранного файла нет — напиши «артефакта нет: <почему>». Пустая строка = отчёт не принимается: гейт `check_uroki.py` краснеет на коммите.)*
**РОД АРТЕФАКТА:** `собранный`
*(`собранный` — колода, PDF, картинка, любой файл, ПОРОЖДЁННЫЙ этим заходом: он обязан быть моложе файла-захода, и Г3 приёмки сверяет ВРЕМЯ. `исходник` — заход, чей продукт есть КОД: он коммитится РАНЬШЕ отчёта, потому что отчёт цитирует хэш коммита, и сверка по времени дала бы вечное ложное красное — тогда Г3 сверяет не время, а «доехал ли артефакт в названный §4 коммит». Не заполнено — Г3 работает по времени, как раньше.)*
**КОММИТ:** `b6c409b5` — `perepis-diska: census TSVs (352 of 352 trees) and REPORT.md`. The other commits are `6e01325c` (plan), `3e2afe3a` (queue items), the DNEVNIK commit, and this report commit. Every commit was pushed to `origin/zahod/perepis-diska` (ПРАВКА 1). · `git_zona.py check --zone` on both zone paths → ✅
*(нет хэша — назови причину прямо здесь; пустая строка = отчёт не принимается)*

### What was done, and why
- **A READ-ONLY census of the five roots, R1–R5**, done by one disposable script, `/tmp/perepis-diska/perepis.py` (the full text is below). The script collects five TSV files and `REPORT.md` into `perepis/`. Why: pass 2 (the cleanup) is to be written from numbers, not from reading projects.
- **Coverage: checked 352 of 352.** Y = `find ~/Documents/GitHub -maxdepth 4 -name .git | wc -l` = 352. It was written into `## ПЛАН` before the census (commit `6e01325c`). `awk -F'\t' 'NR>1' perepis/repos.tsv | wc -l` → 352.
- **Nothing changed:** `awk -F'\t' 'NR>1 && $8!=$9' perepis/repos.tsv | wc -l` → 0. Two full runs of the script both gave 0.
- **Distribution:** `repos.tsv` Counter sums to 352 and `folders.tsv` Counter sums to 28, equal to the row counts. No row has an empty `funnel_rule` (`REPORT.md` §2).
- **Pushed:** `git --no-optional-locks ls-remote origin zahod/perepis-diska` prints one line.

### Main findings (details in REPORT.md)
- **Worktrees dominate the disk.** 339 of the 352 trees are linked worktrees. `disciplina-wt` alone is 52 GB out of 65 GB (`du -sh`).
- **154 worktrees, about 19 GB, can go by two mass rules:** `R9-wt-done` (110, clean and merged) and the proposed `R10-wt-residue` (44, only scratchpad or generated residue).
- **`R4-dup` never fires under "first match wins", and it has no data anyway:** no two main checkouts share an origin.
- **Three repositories have no remote:**
  - `london-avgust-2026`;
  - `carsharing_archive`, nested in `materials`;
  - `spetsmat_db`, nested in `spetsmat`.

  One more git tree lies at depth 6, outside Y: `materials/kurs leto 2026/6-lending/lendingi`.
- **Branches:** 57 local branches are neither in the default branch nor pushed.
- **The owner's recollection, checked against the data:**
  - Early-June start: consistent (first commit 2026-06-06).
  - "Disciplina about a month later": refuted. The first commit is 2026-08-06, about two months after the start.
  - Waves since late August: confirmed (the first `volna` file appears 08-30; 10 worktrees were created on 08-25; 307 in September).
  - Orchestrator: a path containing `orkestr` already exists on 07-10.

### How it was checked
Each check was run as a command, not remembered:
- the criterion commands above;
- `git_zona.py check --zone` on both zone paths → ✅;
- `bootstrap_zahod.py --proverit-doma` → rc=0 (5 items, 0 unreachable).

### What was NOT touched
- **No other repository was changed.** No `commit`, `push`, `stash`, `checkout`, `reset`, `prune`, `gc` or `branch -d` anywhere except my own branch.
- **The only change in other repositories was `git fetch --prune origin`**, which §2.2 allows. It ran once in each of the 10 repositories that have an origin, and it updated only remote-tracking refs.
- **No file content was read**, except the first `#` line of `README.md`/`CLAUDE.md`. Residue classes come from `git status` path names only.
- **The script lives in `/tmp`, not in `materials`.**

### Other required lines
- **Outside the zone:** only `_studio/docs/KARTA.md`, two registration lines written by `register_doc.py`, as the zone contract requires.
- **Verifier:** not needed (§3).
- **Time and tokens:** n/a on the `app` channel.
- **ПОВТОРЯЕМОСТЬ.** ВОПРОСЫ 1 (the false green from the local base ref) repeats on EVERY brief built with the same starter message, so it is a pass before the next wave, not a queue entry. ВОПРОСЫ 4 (tracked files that tools rewrite) repeats on every new worktree. The census numbers themselves do not repeat.
- **НЕОБРАТИМОЕ:** none. The only side effect outside my zone is `git fetch --prune origin` in 10 repositories. It deleted only remote-tracking refs of branches that no longer exist on GitHub, and `git fetch` restores any ref that comes back.

### WARNING block, as amended by §2.6 (steps 2 and 3 cancelled: no merge)
```
step 1  vne git:  git -C materials-wt/perepis-diska status --porcelain | wc -l   →  0   (the only repository I wrote to)
step 4  git --no-optional-locks branch --no-merged origin/claude/bold-faraday-wq09ql  →  main, * zahod/perepis-diska
        main — the showcase/default branch, not mine to merge; zahod/perepis-diska — deliberately NOT merged (§2.6), read by the analyst from GitHub
step 5  git --no-optional-locks log --oneline @{u}.. | wc -l  →  0
step 6  post-check: cancelled by §2.6 (no merge happened)
Г1 ✅ ✅ · Г2 not applicable (the zone is inside materials) · Г3 not-merged count unchanged apart from my own branch · Г4 no new .py in the repository (the script is in /tmp) · Г5 grep -c perepis/REPORT.md KARTA.md → 1, perepis/DNEVNIK.md → 1 · Г6 my commits touch only the zone plus _studio/docs/KARTA.md
worktree drop: NOT run (§2.6)
```

### The script (final version, rerun with `python3 /tmp/perepis-diska/perepis.py <outdir>`)
```python
#!/usr/bin/env python3
"""Read-only census of the owner's Mac disk (pass kod_perepis-diska).

Order: porcelain_before for every tree -> fetch --prune per repository ->
all other measurements -> porcelain_after. Outputs go to OUT (not into any repo).
Never reads file content except the first '#' line of README.md / CLAUDE.md.
"""
import os, sys, subprocess, json, datetime, collections, concurrent.futures as cf

HOME = os.path.expanduser('~')
R1 = os.path.join(HOME, 'Documents/GitHub')
R2 = os.path.join(HOME, 'Documents')
R3 = os.path.join(HOME, 'Downloads')
R4 = HOME
R5 = os.path.join(HOME, '.claude/projects')
OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp/perepis-diska/out'
os.makedirs(OUT, exist_ok=True)

BOOKS = {'pdf', 'djvu', 'epub'}
IMAGES = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp', 'heic', 'tif', 'tiff', 'bmp'}
TEXT = {'md', 'html', 'htm', 'tex', 'txt'}
CODE = {'py', 'sh', 'js'}
CLAUDE_ERA = datetime.datetime(2026, 6, 1).timestamp()
ENV = dict(os.environ, GIT_TERMINAL_PROMPT='0', GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=15')
LOG = open(os.path.join(OUT, 'run.log'), 'w')


def log(*a):
    print(*a, file=LOG, flush=True)


def git(path, *args, timeout=120):
    try:
        p = subprocess.run(['git', '-C', path, '--no-optional-locks', *args], capture_output=True,
                           text=True, timeout=timeout, env=ENV)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return 124, '', 'timeout'


def ts(t):
    return datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%dT%H:%M') if t else ''


def ext_of(name):
    return name.rsplit('.', 1)[1].lower() if '.' in name[1:] else ''


def klass(ext):
    if ext in BOOKS: return 'n_books'
    if ext in IMAGES: return 'n_images'
    if ext in TEXT: return 'n_text'
    if ext in CODE: return 'n_code'
    return 'n_other'


def write_tsv(name, cols, rows):
    with open(os.path.join(OUT, name), 'w') as f:
        f.write('\t'.join(cols) + '\n')
        for r in rows:
            f.write('\t'.join(str(r.get(c, '')).replace('\t', ' ').replace('\n', ' ') for c in cols) + '\n')


# ---------- discovery (same predicate as the coverage command) ----------
p = subprocess.run(['find', R1, '-maxdepth', '4', '-name', '.git'], capture_output=True, text=True)
dot_gits = sorted(l for l in p.stdout.splitlines() if l)
find_errors = [l for l in p.stderr.splitlines() if l]
trees = [os.path.dirname(g) for g in dot_gits]
kind = {os.path.dirname(g): ('main' if os.path.isdir(g) else 'worktree') for g in dot_gits}
log('Y =', len(trees), 'find stderr:', find_errors)


def porcelain(t):
    rc, out, err = git(t, 'status', '--porcelain')
    if rc != 0:
        return {'n': 'err', 'dirty': 'err', 'untr': 'err', 'err': err.strip()[:200]}
    lines = [l for l in out.splitlines() if l]
    u = sum(1 for l in lines if l.startswith('??'))
    return {'n': len(lines), 'dirty': len(lines) - u, 'untr': u, 'err': '', 'lines': lines}


# residue = names only (status paths), never content. Proposed R10 rule.
GEN_NAMES = ('.log', 'MODELI-ZHIVOST.json', 'zamer-skillov.json', '/dist/', 'docs/index.html')


def residue_class(lines):
    if not lines:
        return ''
    kinds = set()
    for l in lines:
        code, path = l[:2], l[3:].strip('"')
        if code == '??' and 'scratchpad' in path:
            kinds.add('scratch')
        elif code.strip() in ('M', '??') and any(g in path for g in GEN_NAMES):
            kinds.add('generated')
        else:
            return 'work'
    return '+'.join(sorted(kinds)) + '-only'


with cf.ThreadPoolExecutor(12) as ex:
    before = dict(zip(trees, ex.map(porcelain, trees)))
log('porcelain_before done')

# ---------- per-tree static facts ----------


def facts(t):
    f = {}
    rc, out, _ = git(t, 'rev-parse', '--path-format=absolute', '--git-common-dir')
    f['common'] = os.path.realpath(out.strip()) if rc == 0 else ''
    rc, out, _ = git(t, 'config', '--get', 'remote.origin.url')
    f['origin_url'] = out.strip() if rc == 0 and out.strip() else 'none'
    rc, out, _ = git(t, 'symbolic-ref', '--short', '-q', 'HEAD')
    f['head_branch'] = out.strip() if rc == 0 else '(detached)'
    rc, out, _ = git(t, 'rev-parse', '-q', '--verify', 'HEAD')
    f['head_sha'] = out.strip() if rc == 0 else ''
    return f


with cf.ThreadPoolExecutor(12) as ex:
    F = dict(zip(trees, ex.map(facts, trees)))

# one fetch per repository (worktrees share refs with their main)
repos = {}
for t in trees:
    c = F[t]['common']
    if c and (c not in repos or kind[t] == 'main'):
        repos[c] = t


def fetch(c):
    t = repos[c]
    if F[t]['origin_url'] == 'none':
        return c, 'no-origin'
    rc, _, err = git(t, 'fetch', '--prune', 'origin', timeout=180)
    return c, 'ok' if rc == 0 else 'failed: ' + err.strip().splitlines()[-1][:150] if err.strip() else 'failed'


with cf.ThreadPoolExecutor(6) as ex:
    FETCH = dict(ex.map(fetch, list(repos)))
log('fetch:', json.dumps(FETCH, indent=1))


def repo_facts(c):
    t = repos[c]
    r = {}
    rc, out, _ = git(t, 'symbolic-ref', '-q', '--short', 'refs/remotes/origin/HEAD')
    d = out.strip()
    r['default'] = d[len('origin/'):] if rc == 0 and d.startswith('origin/') else 'none'
    fmt = '%(refname:short)\t%(upstream:short)\t%(upstream:track,nobracket)\t%(committerdate:iso-strict)\t%(worktreepath)'
    rc, out, _ = git(t, 'for-each-ref', '--format=' + fmt, 'refs/heads')
    merged = set()
    if r['default'] != 'none':
        rc2, o2, _ = git(t, 'for-each-ref', '--merged=origin/' + r['default'], '--format=%(refname:short)', 'refs/heads')
        merged = set(o2.split()) if rc2 == 0 else set()
    br = []
    for line in out.splitlines():
        name, up, track, date, wtp = (line.split('\t') + [''] * 5)[:5]
        ahead = behind = 'n/a'
        has_up = 'no'
        if up:
            if track == 'gone':
                has_up = 'gone'
            else:
                has_up = 'yes'
                ahead = behind = 0
                for part in track.split(','):
                    part = part.strip()
                    if part.startswith('ahead '): ahead = int(part[6:])
                    if part.startswith('behind '): behind = int(part[7:])
        if not FETCH.get(c, '').startswith('ok') and FETCH.get(c) != 'no-origin':
            ind = 'fetch_failed'
        elif r['default'] == 'none':
            ind = 'n/a'
        else:
            ind = 'yes' if name in merged else 'no'
        br.append({'branch': name, 'has_upstream': has_up, 'ahead': ahead, 'behind': behind,
                   'in_default': ind, 'last_commit_date': date[:16], 'wtp': os.path.realpath(wtp) if wtp else ''})
    r['branches'] = br
    # all-ref commit dates for chronology
    rc, out, _ = git(t, 'log', '--all', '--format=%cI', timeout=300)
    r['all_dates'] = [l[:10] for l in out.splitlines() if l]
    return c, r


with cf.ThreadPoolExecutor(8) as ex:
    RF = dict(ex.map(repo_facts, list(repos)))


def history(t):
    h = {}
    rc, out, _ = git(t, 'log', '--max-parents=0', '--format=%cI', 'HEAD')
    ds = sorted(l[:16] for l in out.splitlines() if l)
    h['first_commit_date'] = ds[0] if ds else ''
    rc, out, _ = git(t, 'log', '-1', '--format=%cI', 'HEAD')
    h['last_commit_date'] = out.strip()[:16]
    rc, out, _ = git(t, 'rev-list', '--count', 'HEAD')
    h['commit_count'] = out.strip() if rc == 0 else '0'
    c = F[t]['common']
    d = RF.get(c, {}).get('default', 'none')
    h['head_in_default'] = ''
    if d != 'none' and F[t]['head_sha']:
        rc, _, _ = git(t, 'merge-base', '--is-ancestor', 'HEAD', 'origin/' + d)
        h['head_in_default'] = 'yes' if rc == 0 else 'no'
    if F[t]['head_branch'] == '(detached)' and F[t]['head_sha']:
        rc, out, _ = git(t, 'branch', '-r', '--contains', 'HEAD')
        h['detached_on_remote'] = 'yes' if out.strip() else 'no'
    title = ''
    for fn in ('README.md', 'CLAUDE.md'):
        fp = os.path.join(t, fn)
        if os.path.isfile(fp):
            try:
                with open(fp, encoding='utf-8', errors='replace') as fh:
                    for line in fh:
                        if line.startswith('#'):
                            title = line.lstrip('#').strip()
                            break
            except OSError:
                pass
        if title:
            break
    h['readme_title'] = title
    try:
        st = os.stat(os.path.join(t, '.git'))
        h['dotgit_birth'] = ts(getattr(st, 'st_birthtime', st.st_mtime))
    except OSError:
        h['dotgit_birth'] = ''
    return t, h


with cf.ThreadPoolExecutor(12) as ex:
    H = dict(ex.map(history, trees))
log('history done')

# ---------- filesystem walk ----------
tree_set = set(trees)
extra_trees = []          # git trees found by the walk beyond the Y predicate
stat_tree = collections.defaultdict(lambda: {'size': 0, 'newest': 0})
bigs = []                 # (size, path, owner-tree-or-None)
walk_errors = []


def walk(root, cb, prune_trees=False, owner=None):
    """Iterative walk, skips .git, does not follow symlinks. cb(path, st, owner)."""
    stack = [(root, owner)]
    while stack:
        d, own = stack.pop()
        try:
            it = list(os.scandir(d))
        except OSError as e:
            walk_errors.append(f'{d}: {e.strerror}')
            continue
        names = {e.name for e in it}
        if '.git' in names and d != root:
            if d in tree_set:
                own = d
            else:
                extra_trees.append(d)
                own = d
            if prune_trees:
                continue
        for e in it:
            if e.name == '.git':
                continue
            try:
                if e.is_symlink():
                    continue
                if e.is_dir(follow_symlinks=False):
                    stack.append((e.path, own))
                elif e.is_file(follow_symlinks=False):
                    cb(e.path, e.stat(follow_symlinks=False), own)
            except OSError as ex_:
                walk_errors.append(f'{e.path}: {ex_.strerror}')


def big(path, st, own):
    if st.st_size > 1024 * 1024:
        bigs.append((st.st_size, path, own))


def r1cb(path, st, own):
    if own:
        s = stat_tree[own]
        s['size'] += st.st_size
        s['newest'] = max(s['newest'], st.st_mtime)
    big(path, st, own)


walk(R1, r1cb)
log('R1 walk done; extra trees', len(extra_trees))


def folder_row(path, root_tag, files_only=None, prune_trees=True):
    row = {'path': path, 'root': root_tag, 'size_b': 0, 'file_count': 0, 'oldest': 0, 'newest': 0,
           'n_books': 0, 'n_images': 0, 'n_text': 0, 'n_code': 0, 'n_other': 0, 'n_trees': 0}
    nt_before = len(extra_trees)

    def cb(p_, st, own):
        if own and prune_trees:
            return
        row['size_b'] += st.st_size
        row['file_count'] += 1
        row['oldest'] = min(row['oldest'] or st.st_mtime, st.st_mtime)
        row['newest'] = max(row['newest'], st.st_mtime)
        row[klass(ext_of(os.path.basename(p_)))] += 1
        if root_tag != 'R1':
            big(p_, st, None)

    if files_only is not None:
        for fp in files_only:
            try:
                cb(fp, os.stat(fp, follow_symlinks=False), None)
            except OSError as e:
                walk_errors.append(f'{fp}: {e.strerror}')
    else:
        walk(path, cb, prune_trees=prune_trees)
    row['n_trees'] = sum(1 for t in trees if t.startswith(path + '/'))
    return row


folders = []
# R1: non-git top-level folders
for e in sorted(os.scandir(R1), key=lambda e: e.name):
    if e.is_dir(follow_symlinks=False) and e.path not in tree_set and not e.name.startswith('.'):
        folders.append(folder_row(e.path, 'R1'))
# R2: ~/Documents top level except GitHub
loose = []
for e in sorted(os.scandir(R2), key=lambda e: e.name):
    if e.name.startswith('.') or e.name == 'GitHub':
        continue
    if e.is_dir(follow_symlinks=False):
        folders.append(folder_row(e.path, 'R2', prune_trees=False))
    elif e.is_file(follow_symlinks=False):
        loose.append(e.path)
if loose:
    folders.append(folder_row(R2 + '/[loose files]', 'R2', files_only=loose))
# R3: ~/Downloads
if os.path.isdir(R3):
    loose = []
    for e in sorted(os.scandir(R3), key=lambda e: e.name):
        if e.name.startswith('.'):
            continue
        if e.is_dir(follow_symlinks=False):
            folders.append(folder_row(e.path, 'R3', prune_trees=False))
        elif e.is_file(follow_symlinks=False):
            loose.append(e.path)
    folders.append(folder_row(R3 + '/[loose files]', 'R3', files_only=loose))
# R4: ~ top-level files (not dotfiles) + folders named like Claude in ~ and ~/Documents
loose = [e.path for e in os.scandir(R4) if not e.name.startswith('.') and e.is_file(follow_symlinks=False)]
folders.append(folder_row(R4 + '/[loose files]', 'R4', files_only=sorted(loose)))
for base in (R4, R2):
    for e in sorted(os.scandir(base), key=lambda e: e.name):
        if 'claude' in e.name.lower() and not e.name.startswith('.') and e.is_dir(follow_symlinks=False):
            folders.append(folder_row(e.path, 'R4', prune_trees=False))
log('folders done', len(folders))

# ---------- funnel ----------
origin_groups = collections.defaultdict(list)
for t in trees:
    if kind[t] == 'main' and F[t]['origin_url'] != 'none':
        origin_groups[F[t]['origin_url']].append(t)
dup_of = {t: u for u, ts_ in origin_groups.items() if len(ts_) > 1 for t in ts_}


def branch_ok(b):
    return b['in_default'] == 'yes' or (b['has_upstream'] == 'yes' and b['ahead'] == 0)


rows = []
for t in trees:
    f, h, pb = F[t], H[t], before[t]
    c = f['common']
    rf = RF.get(c, {'default': 'none', 'branches': []})
    brs = rf['branches']
    rt = os.path.realpath(t)
    if kind[t] == 'main':
        rel = [b for b in brs if not b['wtp'] or b['wtp'] == rt]
    else:
        rel = [b for b in brs if b['branch'] == f['head_branch']]
    if f['head_branch'] == '(detached)':
        head_ok = h.get('head_in_default') == 'yes' or h.get('detached_on_remote') == 'yes'
    else:
        head_ok = all(branch_ok(b) for b in brs if b['branch'] == f['head_branch'])
    all_ok = head_ok and all(branch_ok(b) for b in rel)
    dirty = pb['n'] == 'err' or pb['n'] > 0
    if dirty:
        strict = 'R3-park'
    elif all_ok:
        strict = 'R1-ok'
    else:
        strict = 'R2-push'
    rule = strict
    res = residue_class(pb.get('lines', []))
    if kind[t] == 'worktree' and not dirty and h.get('head_in_default') == 'yes':
        rule = 'R9-wt-done'
    elif kind[t] == 'worktree' and dirty and res != 'work' and h.get('head_in_default') == 'yes':
        rule = 'R10-wt-residue'
    rows.append({
        'path': t, 'kind': kind[t], 'origin_url': f['origin_url'], 'head_branch': f['head_branch'],
        'default_branch': rf['default'], 'dirty_tracked': pb['dirty'], 'untracked': pb['untr'],
        'porcelain_before': pb['n'], 'porcelain_after': '',
        'size_mb': round(stat_tree[t]['size'] / 2**20, 1), 'first_commit_date': h['first_commit_date'],
        'last_commit_date': h['last_commit_date'], 'commit_count': h['commit_count'],
        'newest_file_mtime': ts(stat_tree[t]['newest']), 'readme_title': h['readme_title'],
        'funnel_rule': rule, 'funnel_rule_strict': strict, 'dup_group': dup_of.get(t, ''),
        'fetch': FETCH.get(c, ''), 'head_in_default': h.get('head_in_default', ''),
        'dirty_class': res, 'common_dir': c, 'dotgit_birth': h['dotgit_birth'], 'status_err': pb['err'],
    })

branch_rows = []
for t in trees:
    if kind[t] != 'main':
        continue
    for b in RF.get(F[t]['common'], {}).get('branches', []):
        branch_rows.append({'repo_path': t, **b, 'checked_out_in': b['wtp']})

for r in folders:
    order = sorted(['n_books', 'n_images', 'n_text', 'n_code', 'n_other'], key=lambda k: -r[k])
    top = order[0] if r[order[0]] > 0 else None
    textcode = r['n_text'] + r['n_code']
    biggest = max(r['n_books'], r['n_images'], r['n_other'])
    if r['root'] == 'R1' and r['n_trees'] > 0 and r['file_count'] <= 10 and r['size_b'] < 2**20:
        rule = 'R0-holder'
    elif r['file_count'] == 0 and not any(e.startswith(r['path'] + ':') for e in walk_errors):
        rule = 'R0-empty'
    elif r['root'] in ('R1', 'R2') and textcode > 0 and textcode >= biggest:
        rule = 'R5-norepo'
    elif top == 'n_books':
        rule = 'R6-books'
    elif r['root'] in ('R3', 'R4') and r['newest'] >= CLAUDE_ERA:
        rule = 'R7-junk'
    else:
        rule = 'R8-unclear'
    r['funnel_rule'] = rule
    r['size_mb'] = round(r['size_b'] / 2**20, 1)
    r['oldest_mtime'] = ts(r['oldest'])
    r['newest_mtime'] = ts(r['newest'])

# ---------- sessions ----------
sessions = []
if os.path.isdir(R5):
    for e in sorted(os.scandir(R5), key=lambda e: e.name):
        if not e.is_dir(follow_symlinks=False):
            continue
        ms = []
        for j in os.scandir(e.path):
            if j.name.endswith('.jsonl') and j.is_file(follow_symlinks=False):
                ms.append(j.stat().st_mtime)
        sessions.append({'project_dir': e.name, 'jsonl_count': len(ms),
                         'oldest_mtime': ts(min(ms)) if ms else '', 'newest_mtime': ts(max(ms)) if ms else ''})

# ---------- big files ----------
bigs.sort(reverse=True)
big_rows = []
seen = set()
for size, path, own in bigs:
    if path in seen:
        continue
    seen.add(path)
    if own:
        rc, _, _ = git(own, 'ls-files', '--error-unmatch', '--', os.path.relpath(path, own))
        tr = 'yes' if rc == 0 else 'no'
    else:
        tr = 'not-a-repo'
    big_rows.append({'path': path, 'size_mb': round(size / 2**20, 1), 'ext': ext_of(os.path.basename(path)),
                     'tracked_in_git': tr})
    if len(big_rows) == 100:
        break
# duplicate groups by (basename, size) over ALL >1MB files, for the report
dupgroups = collections.defaultdict(list)
for size, path, own in bigs:
    dupgroups[(os.path.basename(path), size)].append(path)

# ---------- porcelain_after LAST ----------
with cf.ThreadPoolExecutor(12) as ex:
    after = dict(zip(trees, ex.map(porcelain, trees)))
for r in rows:
    r['porcelain_after'] = after[r['path']]['n']

REPO_COLS = ['path', 'kind', 'origin_url', 'head_branch', 'default_branch', 'dirty_tracked', 'untracked',
             'porcelain_before', 'porcelain_after', 'size_mb', 'first_commit_date', 'last_commit_date',
             'commit_count', 'newest_file_mtime', 'readme_title', 'funnel_rule',
             'funnel_rule_strict', 'dup_group', 'fetch', 'head_in_default', 'dotgit_birth', 'status_err', 'dirty_class']
write_tsv('repos.tsv', REPO_COLS, rows)
write_tsv('branches.tsv', ['repo_path', 'branch', 'has_upstream', 'ahead', 'behind', 'in_default',
                           'last_commit_date', 'checked_out_in'], branch_rows)
write_tsv('folders.tsv', ['path', 'size_mb', 'file_count', 'oldest_mtime', 'newest_mtime', 'n_books', 'n_images',
                          'n_text', 'n_code', 'n_other', 'funnel_rule', 'root', 'n_trees'], folders)
write_tsv('sessions.tsv', ['project_dir', 'jsonl_count', 'oldest_mtime', 'newest_mtime'], sessions)
write_tsv('big-files.tsv', ['path', 'size_mb', 'ext', 'tracked_in_git'], big_rows)

# side data for the report (not one of the six deliverables)
json.dump({
    'Y': len(trees), 'find_errors': find_errors, 'walk_errors': walk_errors[:200], 'n_walk_errors': len(walk_errors),
    'extra_trees': sorted(set(extra_trees)), 'fetch': FETCH,
    'all_dates': {c: collections.Counter(d[:7] for d in RF[c]['all_dates']) for c in RF},
    'repo_of_common': repos,
    'dup_files': [{'name': k[0], 'size_mb': round(k[1] / 2**20, 1), 'n': len(v), 'paths': v[:6]}
                  for k, v in sorted(dupgroups.items(), key=lambda kv: -kv[0][1] * len(kv[1])) if len(v) > 1][:60],
    'n_big_total': len(bigs),
}, open(os.path.join(OUT, 'side.json'), 'w'), ensure_ascii=False, indent=1, default=list)
log('done')
print('rows', len(rows), 'branches', len(branch_rows), 'folders', len(folders), 'sessions', len(sessions),
      'big', len(big_rows))
```

## СОВЕТ ПРИ СБОРКЕ (`statistika_zahodov.py --sovet`, М-2)
rod=instrumenty · putey_zony=2 · simvolov=32552 · rc=0
```
MODEL: besplatnaya
   принято 24 of 29 in the cluster «rod=instrumenty, zone paths 2-3» = 83%
   OBSERVATIONS: 29 (on besplatnaya passes inside the cluster)   95% interval 65-92%
   whole cluster: принято 52 of 59 = 88%
      besplatnaya  принято  24 of 29   82.8%  <- advised
      sonnet       принято  14 of 14  100.0%
      opus         принято  14 of 16   87.5%
   why not sonnet: its rate is higher (100% on 14), but the intervals overlap - the difference is not measured, and an unmeasured difference is not worth paying for.
   caveat: rod is the tool's own inference, not a declared value, for 18 of the 59 passes in this cluster (rule: zone has a .py/.sh path or lives in _generator/tools -> instrumenty; otherwise a skills/ path -> suzhdenie; otherwise -> mehanika)
   (--simvolov 32552 sits below 143 of 143 measured task sizes; it does NOT narrow the cluster - task length did not separate the outcome on this corpus, see --analiz)
```

## ПРАВКИ ПОСЛЕ ВЫДАЧИ — (заполняет АНАЛИТИК; исполнитель ЧИТАЕТ)
> 🔴 **Пусто — значит заход не правился с момента выдачи.** Непустой блок читается ПЕРЕД продолжением работы: правка отменяет любое противоречащее ей место выше по файлу, каким бы категоричным оно ни было.
> **Форма строки — жёсткая, по ней судит приёмка:** `### ПРАВКА N · ГГГГ-ММ-ДД ЧЧ:ММ · <что изменилось, одной фразой>`, дальше — что именно перечитать и что откатить, если уже сделано по старой редакции.
> **Аналитик:** внёс правку — обязан ОТДЕЛЬНО послать владельцу короткое сообщение для пересылки исполнителю. Правка, лежащая только в файле, до работающего исполнителя не доезжает: он файл не перечитывает сам.
> **Исполнитель:** прочитал правку — назови её номер в `## ОТЧЁТ` строкой `ПРАВКИ ПРОЧИТАНЫ: 1, 2`. Нет строки при непустом блоке = отчёт не принимается: неизвестно, по какой редакции работали.

### ПРАВКА 1 · 2026-09-24 21:23 (UTC) · пушить после каждого коммита и вести дневник хода в perepis/DNEVNIK.md

**Зачем.** Аналитик работает в облаке и видит только то, что лежит на GitHub. По редакции захода до этой правки ты пушишь один раз, в конце, и до этого момента работа не видна никому. Владелец хочет следить за ходом, а аналитик — вмешиваться по ходу, а не только принимать итог. Враг, которого убивает правка: **ошибка, замеченная через шесть часов, вместо ошибки, замеченной через двадцать минут**.

**Что меняется — четыре пункта, каждый отменяет противоречащее место выше.**

1. **Пушь после КАЖДОГО коммита**, а не только в конце:
   ```
   git --no-optional-locks push -u origin zahod/perepis-diska
   ```
   Первый пуш — СРАЗУ после того, как `## ПЛАН` написан и в нём стоит число Y (`find ~/Documents/GitHub -maxdepth 4 -name .git | wc -l`). Пуш не удался (сеть, доступ) — строка в `DNEVNIK.md` с текстом ошибки, работа продолжается, следующий пуш повторяет попытку.

2. **Коммить промежуточные результаты по мере готовности**, не дожидаясь полного набора: готов `repos.tsv` по первому корню — коммит и пуш; готов `sessions.tsv` — коммит и пуш. Незаконченный TSV помечай первой строкой-комментарием `# PARTIAL: <что уже покрыто> of <что всего>`; при окончательной версии строку убери.

3. **Веди дневник хода** — новый файл `_studio/zhurnal/2026-09-24_arhitektura-repozitoriev/perepis/DNEVNIK.md` (он внутри твоей зоны). Английский, как весь твой текст. Новая запись — снизу, заголовок `## <вывод `date '+%Y-%m-%d %H:%M'`> — <этап>`. Время бери из `date`, не из памяти. Запись пишется на КАЖДОМ из этих моментов, и не реже чем раз в 30 минут работы:
   - начало и конец каждого корня R1–R5 и каждого файла из 2.2;
   - любая неожиданность (корня нет, команда упала, число не сходится, найдено то, что не ложится ни в одно правило воронки);
   - любое решение, которое ты принял сам на развилке, — с причиной;
   - любой вопрос аналитику.
   Каждая запись — четыре строки, не больше: **done** (что сделано, с числами) · **next** (что дальше) · **surprise** (неожиданное или «none») · **question** (вопрос или «none»). Число без команды, которой оно снято, не пиши: рядом с числом — команда.
   Файл новый и лежит в `_studio/` — регистрируй его тем же ходом: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/register_doc.py _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/perepis/DNEVNIK.md "running log of the census pass"` и добавь `_studio/docs/KARTA.md` к путям обоих ходов коммита (так велит КОНТРАКТ ЗОНЫ выше).
   Каждая запись дневника — коммит и пуш (пункт 1).

4. **Вопросы не ждут ответа.** Вопрос пишешь в `DNEVNIK.md` и в `## ВОПРОСЫ`, называешь в `## ПЛАН` ветку, которую выбрал сам, и работаешь дальше по ней. Ответ аналитик кладёт СЮДА, следующей правкой. **Твоя копия захода сама не обновится**: аналитик правит файл в ветке `claude/bold-faraday-wq09ql`. Поэтому на каждом этапе из пункта 3 проверяй, нет ли новой правки:
   ```
   git --no-optional-locks fetch origin claude/bold-faraday-wq09ql
   git --no-optional-locks show origin/claude/bold-faraday-wq09ql:_studio/zhurnal/2026-09-24_arhitektura-repozitoriev/kod_perepis-diska.md | sed -n '/^## ПРАВКИ ПОСЛЕ ВЫДАЧИ/,/^## ФАЗА ПРИЁМКИ/p'
   ```
   Нашёл правку с номером, которого не читал, — запись в дневник «read ПРАВКА N» и работаешь по ней. В `## ОТЧЁТ` — строка `ПРАВКИ ПРОЧИТАНЫ: 1, …`.

**Критерий готовности дополняется, не заменяется:** в `perepis/` теперь не меньше 7 файлов (шесть из 2.2 плюс `DNEVNIK.md`); в `DNEVNIK.md` есть запись на начало и конец каждого из корней R1–R5 (`grep -c '^## ' perepis/DNEVNIK.md` → не меньше 10); `git --no-optional-locks log origin/zahod/perepis-diska --oneline | wc -l` на GitHub растёт по ходу, а не один раз в конце — приёмка сверит время коммитов с временем записей дневника.

**Если ты это читаешь, уже закончив часть работы по старой редакции:** ничего не переделывай. Закоммить и запушь то, что есть, напиши в `DNEVNIK.md` одну задним числом помеченную запись «before ПРАВКА 1: done …» и дальше работай по правке.

## ФАЗА ПРИЁМКИ — (заполняет АНАЛИТИК, не исполнитель)
> 🔴 **Без этого раздела заход НЕ ЗАКРЫТ.** Гейт — `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/priyomka.py <этот файл>` (Г13): пока раздел пуст или несёт плейсхолдеры, приёмка красная, и это единственное место, где вердикт остаётся ЗАПИСАННЫМ, а не сказанным в чат.
> Заполняется ПОСЛЕ отчёта исполнителя. Исполнителю сюда писать нечего — его половина выше.

**ВЕРДИКТ:** `<принято | доработка | отклонено>` — `<почему именно так, одной фразой: что проверено и чем>`

**ВЕТКА РАБОТЫ:** `zahod/perepis-diska`
*(проверяется фактом, не словом: ветка обязана существовать и быть либо ВЛИТА в основную, либо названа в открытой заявке на влитие. Ни того, ни другого — Г14 краснеет. Снять состояние: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py poteri --branch <ветка>`)*

**ЗАЯВКИ, ПОСТАВЛЕННЫЕ ЭТОЙ ПРИЁМКОЙ — ПРОДУБЛИРУЙ СЮДА ТО, ЧТО УЖЕ ЛЕЖИТ В СПИСКЕ:**
> Адрес списка: `_studio/zhurnal/_INFRA-git/zayavki`
> Читается командой (из любой папки, в том числе из worktree): `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py zayavki`
> Ставится командой: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py zayavka --rod <git-operaciya|pravka-koda> "<текст>"`
> 🔴 Вопрос здесь НЕ «что ты хочешь сделать», а «что ты УЖЕ положил в очередь». Дубль сверяется с очередью по id машинно; намерение сверить не с чем.

- `<id заявки>` — `<род>` — `<суть одной строкой: влитие / коммит / вывоз / деплой / гашение>`

*(Заявок эта приёмка не ставила — так и напиши строкой «заявок нет: <почему ни одна из пяти операций не понадобилась>». Пустая строка и прочерк не принимаются: молчание неотличимо от «забыл».)*

### ПРАВКА 2 · 2026-09-24 21:29 (UTC) · ответ на вопрос дневника: ретро-запись засчитана, решения ПЛАНа приняты

1. **Your DNEVNIK question — answer: yes.** One retroactive entry plus entries from now on is accepted. The clause of ПРАВКА 1 "`grep -c '^## ' perepis/DNEVNIK.md` → не меньше 10" is **cancelled** for this pass: ПРАВКА 1 arrived after the census was done, and inventing entries would be the only defect here. Do not add filler entries.
2. **Your four decisions in `## ПЛАН` are accepted as made** (worktree branches judged on the worktree row; `R4-dup` among main checkouts only; `R5/R6/R7` by the largest content class; new codes `R9-wt-done`, `R10-wt-residue`, `R0-holder`, `R0-empty`). The analyst spot-checked `materials` chronology against GitHub (`git log --remotes=origin --format=%cI | cut -c1-7 | sort | uniq -c`): June 5 and July 529 match your table exactly; first commit 2026-06-13 matches.
3. **The false green you found in §0.1** (`branch --no-merged claude/bold-faraday-wq09ql` fails, `grep -c` prints 0) is accepted as a factory lesson; your workaround against `origin/…` is the right one. Nothing to fix inside this pass.
4. **What is still owed:** `## ОТЧЁТ` (with the lines `ПРАВКИ ПРОЧИТАНЫ: 1, 2`, АРТЕФАКТ, КОММИТ, НЕОБРАТИМОЕ, ПОВТОРЯЕМОСТЬ), the hygiene block §4.1, the WARNING steps 1, 4, 5, 6 (steps 2–3 stay cancelled by §2.6), and a final push. Then stop: do not start any cleanup.
