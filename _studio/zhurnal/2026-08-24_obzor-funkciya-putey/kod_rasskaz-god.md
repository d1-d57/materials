# Канал исполнителя — rasskaz-god (один заход до конца)
> Твой единственный файл-заход. Читай ТОЛЬКО его и названные якоря; проект не изучай.
<!-- собран bootstrap_zahod.py -->
<!-- гейт сборки заполненного: ЖДЁТ -->
> План/вопросы/отчёт — в секции внизу. Метрика — КАЧЕСТВО. Часы — норма.
> **Модель: Sonnet 5** — a style rewrite of a finished 140 KB popular-science text is judgement produced while writing (paid by construction per the mandate).

## СТАРТОВОЕ СООБЩЕНИЕ ВЛАДЕЛЬЦУ

> Это блок для владельца — то, чем тебя запустили. Исполнителю здесь делать нечего, твоё задание ниже.

```
Модель: Sonnet 5 — <одна фраза почему; см. шапку захода>.

Ты исполнитель в репозитории /Users/ivanyakovlev/Documents/GitHub/materials.

Твой единственный вход — файл-заход:
/Users/ivanyakovlev/Documents/GitHub/materials/_studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_rasskaz-god.md

Прочитай его ЦЕЛИКОМ и работай строго по нему. Он самоценный: в нём назван
контракт зоны, ветка, что читать, задача, критерий готовности и форма отчёта.
Проект самостоятельно НЕ изучай и никаких других файлов по своей инициативе
не открывай — заход сам скажет, что читать.

Ничего сверх задачи не трогай. Оговорка, без которой два указания
противоречат друг другу:
«ничего сверх задачи» относится к СОДЕРЖАНИЮ работы; git-контур §0.1 — законное исключение, он про состояние репозитория и исполняется целиком.

Первым ходом: git branch --show-current, затем чтение захода, затем секция
## ПЛАН внутри него — до всяких действий.

Заход мог быть ПОПРАВЛЕН после того, как ты стартовал: аналитик правит
тот же файл, а ты прочитал его один раз. Смотри секцию ## ПРАВКИ ПОСЛЕ
ВЫДАЧИ в конце файла — при старте и всякий раз, когда владелец пишет
тебе в чат. Правка с номером, которого ты не читал, отменяет любое
противоречащее ей место выше.
```

── СЧЁТ НЕЗАКРЫТОГО (печать, не гейт) ──
ГРАНИЦА ОБЛАСТИ: сырые подстроки в `kod_*.md` (пункт 4) — НЕ парсер очереди `dostavit_urok` (который считает только пары ДОМ:/ДОСТАВЛЕНО:). Разница в числах — законна.
🔴 снимок при сборке 2026-09-19, ПРОВЕРЬ ПЕРВЫМ ХОДОМ: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/schet_nezakrytogo.py _studio/zhurnal/2026-08-24_obzor-funkciya-putey`
Область: «_studio/zhurnal/2026-08-24_obzor-funkciya-putey» — сужены пункты 1, 3, 4; долги (2) глобальны намеренно (DOLG.md не размечен по записям).
Приоритет владельца: разобрать инциденты важнее, потом закрыть долги — неразобранный инцидент это повторяющаяся ошибка, долг может подождать.
  1. инцидентов без вердикта             : 0
  2. долгов СТАТУС: ЖИВ                  : н/д — ни одного skills/*/DOLG.md нет на диске (другой git-репозиторий)
  3. уроков фабрике без ВЕРДИКТ          : 43
  4. пунктов очереди «ДОСТАВЛЕНО: нет»   : 25
     из них разбором очереди (парсер `dostavit_urok`, записи с парой ДОМ:/ДОСТАВЛЕНО:): 4
       живых (чинится доставкой — «дом есть»)  : 2
       к владельцу (решение за человеком)      : 1
       адрес недоступен (нет/папка/код/указат.) : 1
       адрес не разобран                        : 0
       отработавших (машинный след закрытия)    : 0
       доставлено                               : 0
       🔴 не проверяется машиной: содержательная отработанность записей БЕЗ следа закрытия (метки в доме, строки ✅/ЗАКРЫТО) — нужна ревизия человеком; сырой греп сверх разбора — шаблонные строки формы.

🔴 ДВЕРЬ ГЕЙТА СБОРКИ ЗАПОЛНЕННОГО ФАЙЛА ОТКРЫТА КЛАПАНОМ: в арке `_studio/zhurnal/2026-08-24_obzor-funkciya-putey` лежат файлы-заходы со штампом «ЖДЁТ», красные на `check_sborki.py` — `kod_graf-korpusa.md`, `kod_konsolidaciya-korpusa.md`, `kod_pasporta-korpusa.md` — следующий заход в такую арку обычно не собирается, но АНАЛИТИК открыл клапан, причина дословно: «kod_pasporta-korpusa.md (accepted) was assembled in the Cowork sandbox: its reds are sandbox /sessions/ paths in price footnotes and C4 on a file that position created». Отключение видно здесь, в артефакте, а не осталось решением в голове аналитика.

КОНТЕКСТ. The year course «Пути и волны» is one story about one generating function — paths on a board, a weight `q` for area, and the function that specialises to everything. That story is ALREADY WRITTEN: `obzory/funkciya-putey-i-ee-uravneniya/LEKCIYA-v2/`, eight chapters plus an architecture file, ≈140 KB. Its one defect, in the owner's words: he could not read it — it is dull. ЦЕЛЬ: one readable file, `kurs-puti-i-volny/RASSKAZ-god.md`, that the owner reads to the end with pleasure.
Приёмка — по ОТЧЁТУ, без построчной сверки. If you stop early: commit what is rewritten, chapter by chapter; four good chapters committed beat eight uncommitted.

## ЧТО ФИНАЛИЗИРОВАНО НА ИНТЕРВЬЮ

ИНТЕРВЬЮ ПРОВЕДЕНО: да (2026-09-19) — флаг `--intervyu da` при сборке. ⚠ Он доказывает, что аналитик не ЗАБЫЛ про интервью, и НЕ доказывает, что разговор был.

1. The year story already exists (LEKCIYA-v2, eight chapters); its only defect is that the owner could not read it — this is a STYLE rewrite, not a first draft
2. Course mathematics is untouched: no new theorems, nothing re-derived that is already proved
3. Analysis belongs to the second half of the course as a whole (ZAMYSEL id analiz-vo-vtoruyu-polovinu)
4. IWE and any markdown normaliser are not installed: they delete anchors and break KaTeX

## КОНТРАКТ ЗОНЫ (обязателен — не удалять; вписан Cowork)
- **МЕСТО РАБОТЫ:** ветка `arka/mat-kostyak` в основной папке. 🔴 Она должна УЖЕ стоять. НЕ на ней — СТОП, НЕ делай `git checkout`: в общей папке он МОЛЧА откатывает дерево к состоянию ветки (цена 27→28.07: файл сильно откатился ночью, поймал владелец вручную; след в git НЕ остаётся). Тогда заход пересобрать с `--worktree`. Ветку не переключай, в другие НЕ коммить.
- **ЗОНА (можно менять):** `kurs-puti-i-volny/RASSKAZ-god.md` `_studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_rasskaz-god.md`. Всё вне — **READ-ONLY**: не править, не двигать, не удалять, не рефакторить «заодно».
- 🔴 **ЗАВЁЛ НОВЫЙ `.md` — РЕГИСТРИРУЕШЬ ЕГО САМ, ТЕМ ЖЕ ХОДОМ, ОДНОЙ КОМАНДОЙ:** `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/register_doc.py <путь> "<описание>"` (из корня репо). `_studio/docs/` тебе по-прежнему READ-ONLY **для правки руками** — дверь ровно одна, и это она. Дверь идемпотентна (повторный вызов дубля не заведёт) и отказывает на пути вне `_studio/`, на несуществующем файле и на пустом описании. Свой файл-заход регистрировать не нужно: он рождается зарегистрированным из `bootstrap_zahod.py`. **Красный хук на ТВОЁМ новом `.md` — это не повод для `--no-verify`, а повод позвать дверь.** *(история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц1) Обходить больше нечего.*
- **КОММИТ:** два хода — `add` по своим путям, затем `commit` **с теми же путями после `--`** (полная форма и цена каждого хода — §4); коммить ПО ХОДУ работы, не одним последним ходом (§4). НИКОГДА `-A` / `.` / `commit -am`, и никогда `commit` без путей. Субагенты не коммитят. **`--no-optional-locks` обязателен:** обычный git переписывает индекс, берёт `.git/index.lock` и роняет параллельный ручной коммит владельца.
- **SCRATCHPAD — ТОЛЬКО ЛИЧНЫЙ.** Черновики, выкладки, промежуточные версии — в личную папку СВОЕГО захода `scratchpad/rasskaz-god/`. Общие пути (`scratchpad/otchet.md`, любой `scratchpad/*` без имени твоей темы) ЗАПРЕЩЕНЫ: чужой отчёт уедет в твой файл или твой — в чужой, а приёмка читает отчёт без построчной сверки и подмену НЕ ЛОВИТ по построению. (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц2)
- 🔴 **Звал `register_doc.py` — допиши `_studio/docs/KARTA.md` к своим путям В ОБОИХ ходах.** Строка регистрации лежит физически в нём. Ворота 5 читают `§6` **с диска**, а не из индекса: коммит без этого файла пройдёт ЗЕЛЁНЫМ, документ уедет сиротой, а строка умрёт при первом `checkout` (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц3).
- **ЗАПРЕТ:** ничего за пределами зоны, даже если «мешает» или «чинится в одну строку». Нашёл проблему вне зоны → в отчёт, не трогай.

## 0. ПЕРВЫЙ ХОД
### 0.1 🔴 ГИТ-КОНТУР — ДО ВСЕГО ОСТАЛЬНОГО, И ПЕРВЫМ ХОДОМ ЦЕЛИКОМ

🔴 «ничего сверх задачи» относится к СОДЕРЖАНИЮ работы; git-контур §0.1 — законное исключение, он про состояние репозитория и исполняется целиком.

🔴 **ПОРЯДОК ЗДЕСЬ — ЧАСТЬ УСТРОЙСТВА, А НЕ ОФОРМЛЕНИЕ. Сначала САМ прогоняешь две команды самопроверки контура (пункт 1 ниже), и только ПОТОМ заводишь свою рабочую папку** — её ветка отпочковывается от основной такой, какая она есть на момент запуска: контур пуст, доносить инструмент влитием нечего.

**1. ВЕСЬ КОНТУР ПУСТ — САМОПРОВЕРКА ВМЕСТО СУБАГЕНТА.** При сборке проверены три числа контура, и все три нулевые: невлитых `zahod/*`-веток 0 (🔴 снимок при сборке 2026-09-19, ПРОВЕРЬ ПЕРВЫМ ХОДОМ: `git --no-optional-locks branch --no-merged arka/mat-kostyak | grep -c 'zahod/'`); открытых заявок 0 (снимок при сборке 2026-09-19, пересчитать самому: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py zayavki`); названных `--vlit` 0. Звать субагента не за чем — выполни САМ две команды и вставь их вывод в `## ОТЧЁТ` дословно:
```
git --no-optional-locks branch --no-merged arka/mat-kostyak | grep -c 'zahod/'   # снимок при сборке 2026-09-19: 0
python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone kurs-puti-i-volny/RASSKAZ-god.md _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_rasskaz-god.md
```
Первая вернула не 0 — НИЧЕГО чужого не вливай (свою ветку вольёшь последним ходом, см. ниже), назови число строкой в `## ОТЧЁТ` и работай дальше. Вторая красная — сначала приведи в порядок свою зону.

Если при следующей сборке хоть одно из трёх чисел окажется ненулевым, генератор сам вернёт сюда задание субагенту гит-контура — печатает его дверь `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/bootstrap_zahod.py --zadanie-subagentu`; звать его в этом заходе не надо.

🔴 ОТВЕТ ЛЮБОГО субагента, которого ты запускаешь (не только этого), обязан КОНЧАТЬСЯ строкой «выдано N позиций из M найденных»: канал мог оборвать его молча, и без этой строки усечение неотличимо от честного «мало нашлось». Нет строки — ответ усечён, в `## ОТЧЁТ` не вставляй, перезапроси.

**2. ТЕПЕРЬ ЗАВОДИ СВОЮ РАБОЧУЮ ПАПКУ** (команда — в блоке «МЕСТО РАБОТЫ» выше) и работай в ней как обычно. Её ветка отпочкована от свежей основной, поэтому инструмент, которым ты работаешь, уже на диске — отдельного «влить перед работой» больше нет.

вливать нечего, проверено командой `git branch --no-merged` — но проверено ПРИ СБОРКЕ, а не сейчас: невлитых `zahod/*`-веток было 0. 🔴 снимок при сборке 2026-09-19, ПРОВЕРЬ ПЕРВЫМ ХОДОМ: `git --no-optional-locks branch --no-merged arka/mat-kostyak | grep -c 'zahod/'`. Число могло устареть между сборкой и твоим прогоном — 14.08 заход нёс ровно этот ноль, а к прогону невлитых было три.


- деплоя в этом заходе нет.

- Проверь ветку: `git branch --show-current` — обязано быть `arka/mat-kostyak`. Не она — СТОП, `git checkout` НЕ делай (§4 GIT-disciplina), нужен `--worktree`.
- Точка отката: `git add kurs-puti-i-volny/RASSKAZ-god.md _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_rasskaz-god.md` → commit (или zip), если зона не чиста в HEAD (не фабрикуй, если чиста).
- Прочитать ТОЛЬКО: `названные файлы-якоря`. Проект не изучай.
- ПЛАН — в `## ПЛАН` перед действиями.

## 1. ДИСЦИПЛИНА (Карпатов)
🔴 **Код возврата — ПЕРВЫМ, до содержательного вывода команды.** «Отработала» и «упала, а я читаю прошлое состояние» выглядят одинаково; сначала `echo $?`, потом выводы. То же с гейтами. (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц7)
Предпосылки/развилки назвать вслух; минимум без спекуляций; хирургия (строка → к заданию); критерий, который может провалиться. Якорные замены — abort при ≠1. Сохранять по умолчанию. **Оспорить ложную предпосылку — включая КРИТЕРИЙ ГОТОВНОСТИ: считаешь его кривым — скажи в `## ПЛАН`, ДО работы, и предложи поправку.** Субагенты: ≤5, рейт-лимит = отступить + доложить (не слепой ретрай).

🔴 **Пишешь содержательный текст — термин НЕ употребляется раньше, чем определён**, включая заголовки, подводки и формулировки теорем. «Определение в тексте есть» не считается: если оно ниже первого рабочего употребления, читатель встаёт ровно там. Чинится ПЕРЕСТАНОВКОЙ определения вверх, не дописыванием пояснения. Гейт: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/check_termin.py <src>` (exit 1 при нарушении). Канон — `../docs/kak-delat/STANDART-teksta.md` правило 11. (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц8)

## 2. ЗАДАЧА

🔴 **WRITE YOUR `## ОТЧЁТ`, `## ПЛАН` AND `## ВОПРОСЫ` IN ENGLISH, AND EVERY FILE AND EVERY COMMIT MESSAGE YOU PRODUCE TOO.** Owner's decision 30.08. It is a каркас-level rule, not a preference (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц9). Fixed Russian addresses stay Cyrillic: `ЦЕНА:` · `ВЕРДИКТ:` · `ДОМ:` · `ДОСТАВЛЕНО:` · `ПОДЪЁМ:` · `[ДОЛГ: …]` · every `## ` heading of this file · every path and command.
### 🔴 This is a STYLE rewrite. The content exists and is correct.
Keep: the throughline (`LEKCIYA-v2/00-arhitektura.md`, sections «Throughline» and «Разворот»), the eight-chapter order, the two detective knots — **André, who never used the reflection** and **Rogers, unnoticed for twenty-three years** — and the five SVG figures in `LEKCIYA-v2/` (reference them by relative path `../obzory/funkciya-putey-i-ee-uravneniya/LEKCIYA-v2/<name>.svg`; do not redraw). Do not re-derive any mathematics and do not add new theorems. Where the course is honest, stay honest: the fourth view is a promise, not a result — say so in the text.

### Read ONLY these
- `obzory/funkciya-putey-i-ee-uravneniya/LEKCIYA-v2/00-arhitektura.md` in full, then the eight chapters `01-…08-*.md` one at a time, each just before you rewrite it.
- The genre reference is settled: Étienne Ghys, *A Singular Mathematical Promenade* — `kurs-puti-i-volny/ZAMYSEL.md` §1 says why; read only §1.
- If `kurs-puti-i-volny/plan/src/punkty.md` exists (the item list from the previous stage), read only its item ids and coordinates, to link chapters to items.
Do not study the rest of the project.

### Why it is dull — diagnose before you write
Before rewriting, open two chapters and write into `## ПЛАН` five concrete causes of dullness with a quoted example each (e.g. a paragraph that announces instead of shows; a theorem stated before the question that makes it wanted; a list where a scene should be; a term used before it is needed; bureaucratic Russian). Then rewrite against YOUR five causes. The owner's own words about the target: simple, clear, engaging, not dry — a popular-science narrative, not a syllabus.

### What to write
One file `kurs-puti-i-volny/RASSKAZ-god.md`, in Russian:
- YAML header with `opisanie:`, `sloj: 5`, `status: zhivoy`; register it the same move: `python3 ../disciplina/_generator/tools/register_doc.py kurs-puti-i-volny/RASSKAZ-god.md "<one phrase>"`.
- Eight chapters in the same order. Each chapter opens with a QUESTION a curious reader would ask, and only then the mathematics that answers it. Every chapter heading carries an anchor comment with id `rasskaz-gN` (N = 1…8) and, when the item list exists, links `[[p-NN]]` to the items it covers — the only link syntax the index reads.
- **Length: 45 000–65 000 characters** (`wc -m`). The source is ≈140 KB; a readable promenade is shorter. Cut repetition, the scaffolding of announcements and summaries, and side remarks — never the two knots, the throughline or a figure.
- Formulas in KaTeX-safe `$…$` / `$$…$$` exactly as in the source.
- No analysis creep: asymptotics and limits belong to the second half of the course; in the story they appear only where the source chapter already has them (chapter 6 «большие числа» is about that half), not as new remarks elsewhere.

### Russian-editor gate before handing over
Run `python3 ../disciplina/_generator/tools/check_termin.py kurs-puti-i-volny/RASSKAZ-god.md` (a term never used before it is defined) and fix every hit by MOVING the definition up. Then reread one chapter aloud-in-your-head for bureaucratic Russian (отглагольные существительные, «является», «осуществляется», «данный») and fix it.

### Successor context (last move)
Under `## ОТЧЁТ`: the five causes you found, which of them you could not fully remove and where, and one line per chapter «source KB → new KB».

**КРИТЕРИЙ ГОТОВНОСТИ (может ПРОВАЛИТЬСЯ)** — each clause one command, return code first:
1. **Live run on the real file:** `wc -m kurs-puti-i-volny/RASSKAZ-god.md` between 45000 and 65000.
2. `grep -c '<!--id: rasskaz-g' kurs-puti-i-volny/RASSKAZ-god.md` → `8`.
3. Both knots and all five figures survived: `grep -c 'Андре' kurs-puti-i-volny/RASSKAZ-god.md` ≥ 1, `grep -c 'Роджерс' kurs-puti-i-volny/RASSKAZ-god.md` ≥ 1, `grep -c '\.svg' kurs-puti-i-volny/RASSKAZ-god.md` ≥ 5.
4. `python3 ../disciplina/_generator/tools/check_termin.py kurs-puti-i-volny/RASSKAZ-god.md; echo $?` → `0`.
5. `cd kurs-puti-i-volny && python3 tools/indeks.py; echo $?` → `0`, no dangling id, and the new file is not in the «без описания» count.
6. The fresh reader (§3) answers all three questions and its answer to «where is the author leading» names one function whose specialisations give the particular answers — paste its reply verbatim.

**Coverage line in the report:** «chapters rewritten N of 8 · causes of dullness found 5, removed K».
**Отрицательный вердикт несёт ОХВАТ В СЕБЕ:** не «дыр не найдено», а «дыр не найдено, проверено X из Y». Без охвата вердикт не принимается — «проверено 2 из 9» и «проверено 9 из 9» выглядят одинаково.

## 3. ВЕРИФИКАТОР (если двигаем/теряем/жмём)

Верификатор нужен, тип — **ПОСЛЕ-типа** — судит результат, стоит в конце, после задачи. Свежий субагент, ДРУГИМ методом (fresh subagent that has seen neither the corpus nor LEKCIYA-v2 reads RASSKAZ-god.md alone and answers three questions: did it enjoy a finished story; where is the author leading; did it see how these tools help investigate a probability model), не перечитывает свою же правку. Доля сплошной выборки: 1 of 1 text, read in full. Финальная строка ответа обязательна дословно: «выдано N позиций из M найденных» — без неё ответ считается усечённым и в отчёт не вставляется.

## 4. 🔴 КОММИТ СВОЕЙ ЗОНЫ — ПО ХОДУ РАБОТЫ, НЕ ОДНИМ ПОСЛЕДНИМ ХОДОМ
Ты работаешь host-side и в `.git` ПИШЕШЬ — значит коммитишь САМ, никому не передавая. Каждую завершённую часть работы коммить СРАЗУ, теми же двумя ходами — не копи всё к финальному ходу:
```
git --no-optional-locks add -- kurs-puti-i-volny/RASSKAZ-god.md _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_rasskaz-god.md                     # вводит НОВЫЕ пути в индекс
git --no-optional-locks commit -m "<зона>: <что сделано>" -- kurs-puti-i-volny/RASSKAZ-god.md _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_rasskaz-god.md   # отсекает всё чужое
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

**ЗОНА ГИГИЕНЫ:** `kurs-puti-i-volny/RASSKAZ-god.md` `_studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_rasskaz-god.md`

- **Г1. Зона доехала в git.** `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone kurs-puti-i-volny/RASSKAZ-god.md` → ✅; `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_rasskaz-god.md` → ✅. Красное на любой из команд — отчёт не принимается: приёмка гоняет их все первым ходом.
- **Г2. Второй репозиторий.** **неприменимо, и это проверено при сборке, а не предположено:** все пути зоны лежат внутри репозитория `materials` (тот же критерий, что у С2 `check_sborki.py`). Зона расширилась за его пределы по ходу — пункт снова применим; команда та же, что в применимом случае: `cd ../<репозиторий> && git --no-optional-locks status --porcelain` → пусто. *Команда названа и здесь нарочно (находка верификатора): пункт, который объявлен неприменимым и не говорит, ЧТО делать, когда станет применим, исполнить в этот момент нечем.*
- **Г3. Невлитых веток не прибавилось.** `git --no-optional-locks branch --no-merged arka/mat-kostyak` — число сравни с тем, что было на входе. Выросло — назови, чьи ветки и почему они законны.
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
python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py vlit-v-osnovnuyu arka/mat-kostyak --zone <своя зона> \
    --vsyo-ravno "своя рабочая папка ещё жива — влитие последним ходом захода, штатно"
```
Конфликт — ЗАКОННЫЙ исход, не повод форсировать: разрешай по существу, если понимаешь обе
стороны; не понимаешь — `git_zona.py vlit-v-osnovnuyu --abort`, ветка остаётся невлитой,
строка в отчёт и заявка на влитие (`git_zona.py zayavka --rod git-operaciya`).
🔴 Конфликт на `README.md` — только ОБЪЕДИНЕНИЕМ записей реестра, никогда выбором стороны:
параллельные заходы волны дописали по строке — обе записи правы, выбор одной молча уничтожает
регистрацию соседа.

**3 · ПОСТ-ПРОВЕРКА ИЗ ГЛАВНОЙ ПАПКИ.** Отвечает на вопрос «механизм ВСТАЛ», а не «коммит
виден»: прогон изменённого механизма (здесь она же — checkout-режим, папка одна) плюс `grep` по ЖИВОМУ файлу,
который его зовёт (хук, конвейер, генератор):
```
cd /Users/ivanyakovlev/Documents/GitHub/materials && <команда прогона механизма, который заход менял> && echo $?
grep -n '<как механизм назван в вызывающем коде>' <живая точка вызова>
```
🔴 **Красная пост-проверка = ОТКАТ ВЛИТИЯ И СТРОКА В ОТЧЁТ**, а не «доложу, пусть приёмка
решает»: `git_zona.py vlit-v-osnovnuyu --abort`, если слияние ещё не закоммичено, иначе
`git -C /Users/ivanyakovlev/Documents/GitHub/materials --no-optional-locks reset --hard <хэш ДО влития>`. Заход, который влил
и сломал `main`, обязан вернуть `main` сам.

**4 · ГАШЕНИЕ.** Невлитого не осталось: `git --no-optional-locks branch --no-merged arka/mat-kostyak`.
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

**Owner's notes accepted as amendments to this zahod file** (measured today, not written into the file itself, so recorded here instead): run §0.1 myself, no git-contour subagent; the item list `kurs-puti-i-volny/plan/src/punkty.md` exists (33 items `p-01`…`p-33`) — read only ids and coordinates (`doska`/`ves`), the `imya`/`vopros` fields are still empty; `register_doc.py` refuses `kurs-puti-i-volny/RASSKAZ-god.md` (outside `_studio/`) — **registration is skipped by design**, the course index (`kurs-puti-i-volny/tools/indeks.py`) reads the `opisanie:` header directly, which criterion clause 5 below confirms; commit AND push as I go, by explicit path only; the fresh reader (§3) is a haiku subagent given only the file path and the three questions; budget ceiling 250k tokens; do not touch `kurs-puti-i-volny/plan/src/` (a parallel executor's zone).

**Diagnosis — five causes of dullness** (read chapters 1 «Две дроби» and 3 «Зверинец» in full first, as instructed; confirmed systemic by grepping all 8 chapters):

1. **Ritual "checked by counting" footnotes appended after nearly every claim** turn a story into a QA log. E.g. ch3: *«Все четыре ряда посчитаны перебором до $n=7$ и совпадают: $1,1,2,5,14,42,132,429$.»* — a verification ticket, not a sentence a reader wants. All 9 files carry these (18 hits total, grep `Проверено|проверено`).
2. **The `> поле:`/`поле:insight … |` margin-note tag sits between the reader and the best line**, turning discoveries into labelled inserts instead of prose in the narrator's own voice. E.g. ch3: *«поле:insight Формула и соответствие — разные знания | Формула Каталана говорит, сколько маршрутов. Биекция говорит, почему их столько же…»* — the label is genre apparatus from Ghys's margin layout (`ZAMYSEL.md §1`: "вёрстка с боковыми полями"), which the intended two-column `view.html` renders as an actual margin but which reads as bureaucratic markup in plain text. 41 such tags across the 8 chapters.
3. **Every chapter opens with nine lines of production YAML** (`tab`/`status`/`poryadok`/`registr`/`nomera`/`tema`/`oblast`/`data`/`adresat`/`opisanie`) the reader never asked for, sitting before the title itself — e.g. `02-koridor.md` lines 1–11, `adresat: взрослый читатель, владеющий техникой, но не знакомый с q-рядами`. Internal bookkeeping presented as the chapter's first words.
4. **Every chapter ends on a `> поле:foot Черновик 2026-09-03…` draft-status note addressed to the analyst**, landing right after the chapter's dramatic closing line and undercutting it — e.g. after ch2's closing hook *«…посыплются вещи, которые в школьном курсе стоят в разных главах»* comes *«Черновик 2026-09-03. Таблица квадратов проверена счётом; формула… здесь взята вперёд; теорема Нивена — чёрный ящик со ссылкой.»* Same pattern in all 8 files.
5. **Sheer accumulated length turns a good rhetorical shape into a predictable template.** The same three-beat pattern — childlike question → hand-count with a table → counted-by-computer footnote — repeats with almost no variation across all eight 13–18 KB chapters (140 KB total), so by chapter 4 a reader can predict the shape of the next section before reading it (compare ch1 §"Считаем руками" and ch3 §"Одна стенка" — identical shape, different content).

None of these are math problems — the mathematics, the throughline, and the two detective knots (André, Rogers) are already sound and were not touched.

**Rewrite plan against these five causes:** strip all production YAML headers and draft-status footers (causes 3, 4) — the new file carries one clean YAML header per the "What to write" spec, not per chapter. Fold every `поле:`/`поле:insight` box into ordinary flowing prose, keeping the sentence but dropping the label (cause 2). Cut the mechanical "проверено…" tickets; keep a verification detail only where it is itself part of the story (e.g. Ramanujan's fraction matching to forty digits) (cause 1). Compress ruthlessly chapter by chapter rather than trimming evenly, since cause 5 is about accumulated volume, not any one paragraph — target ≈45–55 % of source length per chapter while preserving every formula, both knots, all five figures, and the chapter-to-chapter throughline hooks.

**Figures:** the five `.svg` files in `LEKCIYA-v2/` (`koridor-marshrut.svg`, `mnogougolniki.svg`, `biekcia-derevo-marshrut.svg`, `otrazhenie.svg`, `ploshchad-dva-marshruta.svg`) match the five inline `<svg>` figures in chapters 1–5 by `viewBox` (verified). Referencing them by relative path instead of inlining the raw SVG markup also does a large part of the length-compression work for free, since the inline SVG markup itself ran to 2–3 KB per figure.

**Item links `[[p-NN]]`:** `punkty.md`'s 33 items carry only a board coordinate (`doska`: pryamaya/luch/otrezok/predel) and a weight flag (`ves`) — `imya`/`vopros` are still empty, so there is no way to match items to chapters by content, only by board level. I link each chapter to 2–3 representative item ids at the board level its mathematics operates on (pryamaya p-01…04, luch p-05…14, otrezok p-15…27, predel p-28…33); chapters 7–8 get no item links because the architecture file (`00-arhitektura.md` "Пятое место") and `ZAMYSEL.md` both say this material sits **outside the year's 33 items**, in a planned separate form. This is a coarse, coordinate-based mapping, not a verified one-to-one correspondence — flagged as a queue item below since a future pass that fills in `imya`/`vopros` could re-derive it precisely.

**Length arithmetic:** source ≈140 KB (139 851 bytes) across 9 files; target 45 000–65 000 characters. Aimed for ≈52 000 characters, i.e. roughly 37 % of source length, achieved by the cuts above plus reference-not-inline figures.

## ВОПРОСЫ — (заполняет исполнитель)

1. `[[p-NN]]` links in `kurs-puti-i-volny/RASSKAZ-god.md` are coordinate-based (board level only), not content-verified, because `punkty.md`'s `imya`/`vopros` fields are still empty for all 33 items. Once a future pass fills those fields, the chapter-to-item links should be re-derived from content and could well change.
   ДОМ: kurs-puti-i-volny/plan/src/punkty.md
   ДОСТАВЛЕНО: нет

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

Run by the executor itself per owner's note ("no git-contour subagent"), with `GIT_ZONA_REPO="$PWD"` exported.

```
$ git --no-optional-locks branch --no-merged arka/mat-kostyak | grep -c 'zahod/'
0
$ git --no-optional-locks status --porcelain | wc -l
13   # pre-existing dirt: other people's uncommitted files (PULS-CHASOVOGO log, INCIDENTY.md,
     # diskmat-57 drafts, _fond svg) + this zahod's own new files — none of it mine to touch/commit
$ git --no-optional-locks log --oneline @{u}.. | wc -l
0
$ python3 ../disciplina/_generator/tools/git_zona.py zayavki
... (prints 12 historical "переадресовано" routing entries, none addressed to this arc)
Охват: заявок открыто 0, переадресовано 12, постоянных исключений 1, сторож краснеет на 0, держателей 0, двойной захват на 0
```

**ЧТО СДЕЛАНО** *(с хэшами)*
Nothing to merge/purge/deliver: unmerged `zahod/*` = 0, open заявки addressed to this arc = 0. This is the "contour already empty" case named in §0.1 — no hygiene work needed before starting.

**ВСЕ ДОЛГИ ВХОДА ЗАКРЫТЫ:** `да`
*(there were no debts belonging to this arc's git contour to close — the 13 dirty paths at input are other people's uncommitted work in a shared folder, out of this executor's rights to touch, per contract.)*

## ОТЧЁТ — (заполняет исполнитель)
**АРТЕФАКТ:** `<АБСОЛЮТНЫЙ путь к собранному файлу, который владелец должен открыть>` — `<чем открывать>`
*(собрал HTML, документ, PDF, картинки — путь сюда. Собранного файла нет — напиши «артефакта нет: <почему>». Пустая строка = отчёт не принимается: гейт `check_uroki.py` краснеет на коммите.)*
**РОД АРТЕФАКТА:** `<исходник | собранный>`
*(`собранный` — колода, PDF, картинка, любой файл, ПОРОЖДЁННЫЙ этим заходом: он обязан быть моложе файла-захода, и Г3 приёмки сверяет ВРЕМЯ. `исходник` — заход, чей продукт есть КОД: он коммитится РАНЬШЕ отчёта, потому что отчёт цитирует хэш коммита, и сверка по времени дала бы вечное ложное красное — тогда Г3 сверяет не время, а «доехал ли артефакт в названный §4 коммит». Не заполнено — Г3 работает по времени, как раньше.)*
**КОММИТ:** `<хэш>` — `<сообщение>` · `git_zona.py check --zone <зона>` → ✅
*(нет хэша — назови причину прямо здесь; пустая строка = отчёт не принимается)*

## ПРАВКИ ПОСЛЕ ВЫДАЧИ — (заполняет АНАЛИТИК; исполнитель ЧИТАЕТ)
> 🔴 **Пусто — значит заход не правился с момента выдачи.** Непустой блок читается ПЕРЕД продолжением работы: правка отменяет любое противоречащее ей место выше по файлу, каким бы категоричным оно ни было.
> **Форма строки — жёсткая, по ней судит приёмка:** `### ПРАВКА N · ГГГГ-ММ-ДД ЧЧ:ММ · <что изменилось, одной фразой>`, дальше — что именно перечитать и что откатить, если уже сделано по старой редакции.
> **Аналитик:** внёс правку — обязан ОТДЕЛЬНО послать владельцу короткое сообщение для пересылки исполнителю. Правка, лежащая только в файле, до работающего исполнителя не доезжает: он файл не перечитывает сам.
> **Исполнитель:** прочитал правку — назови её номер в `## ОТЧЁТ` строкой `ПРАВКИ ПРОЧИТАНЫ: 1, 2`. Нет строки при непустом блоке = отчёт не принимается: неизвестно, по какой редакции работали.

<правок нет>

## ФАЗА ПРИЁМКИ — (заполняет АНАЛИТИК, не исполнитель)
> 🔴 **Без этого раздела заход НЕ ЗАКРЫТ.** Гейт — `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/priyomka.py <этот файл>` (Г13): пока раздел пуст или несёт плейсхолдеры, приёмка красная, и это единственное место, где вердикт остаётся ЗАПИСАННЫМ, а не сказанным в чат.
> Заполняется ПОСЛЕ отчёта исполнителя. Исполнителю сюда писать нечего — его половина выше.

**ВЕРДИКТ:** `<принято | доработка | отклонено>` — `<почему именно так, одной фразой: что проверено и чем>`

**ВЕТКА РАБОТЫ:** `arka/mat-kostyak`
*(проверяется фактом, не словом: ветка обязана существовать и быть либо ВЛИТА в основную, либо названа в открытой заявке на влитие. Ни того, ни другого — Г14 краснеет. Снять состояние: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py poteri --branch <ветка>`)*

**ЗАЯВКИ, ПОСТАВЛЕННЫЕ ЭТОЙ ПРИЁМКОЙ — ПРОДУБЛИРУЙ СЮДА ТО, ЧТО УЖЕ ЛЕЖИТ В СПИСКЕ:**
> Адрес списка: `/Users/ivanyakovlev/Documents/GitHub/materials/_studio/zhurnal/_INFRA-git/zayavki`
> Читается командой (из любой папки, в том числе из worktree): `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py zayavki`
> Ставится командой: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py zayavka --rod <git-operaciya|pravka-koda> "<текст>"`
> 🔴 Вопрос здесь НЕ «что ты хочешь сделать», а «что ты УЖЕ положил в очередь». Дубль сверяется с очередью по id машинно; намерение сверить не с чем.

- `<id заявки>` — `<род>` — `<суть одной строкой: влитие / коммит / вывоз / деплой / гашение>`

*(Заявок эта приёмка не ставила — так и напиши строкой «заявок нет: <почему ни одна из пяти операций не понадобилась>». Пустая строка и прочерк не принимаются: молчание неотличимо от «забыл».)*
