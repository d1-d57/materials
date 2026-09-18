# Канал исполнителя — arhitektura-punkta (один заход до конца)
> Твой единственный файл-заход. Читай ТОЛЬКО его и названные якоря; проект не изучай.
<!-- собран bootstrap_zahod.py -->
<!-- гейт сборки заполненного: ЖДЁТ -->
> План/вопросы/отчёт — в секции внизу. Метрика — КАЧЕСТВО. Часы — норма.
> **Модель: Sonnet 5** — designing the item form is judgement produced during execution (paid by construction per the mandate); the generator itself is small.

## СТАРТОВОЕ СООБЩЕНИЕ ВЛАДЕЛЬЦУ

> Это блок для владельца — то, чем тебя запустили. Исполнителю здесь делать нечего, твоё задание ниже.

```
Модель: Sonnet 5 — <одна фраза почему; см. шапку захода>.

Ты исполнитель в репозитории /Users/ivanyakovlev/Documents/GitHub/materials.

Твой единственный вход — файл-заход:
/Users/ivanyakovlev/Documents/GitHub/materials/_studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_arhitektura-punkta.md

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
  4. пунктов очереди «ДОСТАВЛЕНО: нет»   : 22
     из них разбором очереди (парсер `dostavit_urok`, записи с парой ДОМ:/ДОСТАВЛЕНО:): 4
       живых (чинится доставкой — «дом есть»)  : 2
       к владельцу (решение за человеком)      : 1
       адрес недоступен (нет/папка/код/указат.) : 1
       адрес не разобран                        : 0
       отработавших (машинный след закрытия)    : 0
       доставлено                               : 0
       🔴 не проверяется машиной: содержательная отработанность записей БЕЗ следа закрытия (метки в доме, строки ✅/ЗАКРЫТО) — нужна ревизия человеком; сырой греп сверх разбора — шаблонные строки формы.

🔴 ДВЕРЬ НЕЗАКОММИЧЕННЫХ `kod_*.md` ОТКРЫТА КЛАПАНОМ: в арке `_studio/zhurnal/2026-08-24_obzor-funkciya-putey` есть 1 незакоммиченных файлов-заходов `kod_pasporta-korpusa.md` — второй заход в такую арку обычно не собирается (долг 4 `disciplina-git`), но АНАЛИТИК открыл клапан, причина дословно: «S1 (kod_pasporta-korpusa.md) is live; S4a is only assembled now and starts after S2 and S3 are accepted». Отключение видно здесь, в артефакте, а не осталось решением в голове аналитика.

🔴 ДВЕРЬ ГЕЙТА СБОРКИ ЗАПОЛНЕННОГО ФАЙЛА ОТКРЫТА КЛАПАНОМ: в арке `_studio/zhurnal/2026-08-24_obzor-funkciya-putey` лежат файлы-заходы со штампом «ЖДЁТ», красные на `check_sborki.py` — `kod_pasporta-korpusa.md` — следующий заход в такую арку обычно не собирается, но АНАЛИТИК открыл клапан, причина дословно: «kod_pasporta-korpusa.md was assembled in the Cowork sandbox: its reds are sandbox /sessions/ paths in price footnotes and C4 on the file that position itself creates; it is live, the head does not write into a live brief». Отключение видно здесь, в артефакте, а не осталось решением в голове аналитика.

КОНТЕКСТ. The year course «Пути и волны» has ONE list of lesson items, but it is written by hand in several files and has already diverged three times (`kurs-puti-i-volny/SBORKA/KARTA-rashozhdeniy.md` rows Р5, Р10, Р13). Previous stages of this wave: S1 described every file, S2 built `tools/graf.py`, S3 gave every disagreement a status. ЦЕЛЬ (owner's addition Д2, 19.09): the item becomes an atom living ONCE in one file, and the plans of the year, the half, the part «до анализа», the quarter and the lecture become VIEWS generated from it by a script — so «three parts here, four there» becomes impossible: a count is computed, never typed.
Приёмка — по ОТЧЁТУ, без построчной сверки. If you stop early: a committed items file + a generator that builds at least the year and quarter views is worth more than an uncommitted complete design.

## ЧТО ФИНАЛИЗИРОВАНО НА ИНТЕРВЬЮ

ИНТЕРВЬЮ ПРОВЕДЕНО: да (2026-09-19) — флаг `--intervyu da` при сборке. ⚠ Он доказывает, что аналитик не ЗАБЫЛ про интервью, и НЕ доказывает, что разговор был.

1. No duplication. Each thing is laid down once, in one home, referenced by id from everywhere else
2. Year story, first part, quarter plan and first-lecture plan are one structure at four magnifications; each finer plan specialises a named item of the coarser one, and that linkage is a machine-checked gate
3. Д2 (owner, 19.09, amends F4): the item is an atom living once in one file; all plan views are GENERATED by a script and never hand-written, exactly like INDEKS.md
4. Д2: architecture and filling are separate positions; this position designs the form and builds the mechanism and writes NO content
5. IWE and any markdown normaliser are not installed: they delete anchors and break KaTeX

## КОНТРАКТ ЗОНЫ (обязателен — не удалять; вписан Cowork)
- **МЕСТО РАБОТЫ:** ветка `arka/mat-kostyak` в основной папке. 🔴 Она должна УЖЕ стоять. НЕ на ней — СТОП, НЕ делай `git checkout`: в общей папке он МОЛЧА откатывает дерево к состоянию ветки (цена 27→28.07: файл сильно откатился ночью, поймал владелец вручную; след в git НЕ остаётся). Тогда заход пересобрать с `--worktree`. Ветку не переключай, в другие НЕ коммить.
- **ЗОНА (можно менять):** `kurs-puti-i-volny/plan/src` `kurs-puti-i-volny/tools/plany.py` `_studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_arhitektura-punkta.md`. Всё вне — **READ-ONLY**: не править, не двигать, не удалять, не рефакторить «заодно».
- 🔴 **ЗАВЁЛ НОВЫЙ `.md` — РЕГИСТРИРУЕШЬ ЕГО САМ, ТЕМ ЖЕ ХОДОМ, ОДНОЙ КОМАНДОЙ:** `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/register_doc.py <путь> "<описание>"` (из корня репо). `_studio/docs/` тебе по-прежнему READ-ONLY **для правки руками** — дверь ровно одна, и это она. Дверь идемпотентна (повторный вызов дубля не заведёт) и отказывает на пути вне `_studio/`, на несуществующем файле и на пустом описании. Свой файл-заход регистрировать не нужно: он рождается зарегистрированным из `bootstrap_zahod.py`. **Красный хук на ТВОЁМ новом `.md` — это не повод для `--no-verify`, а повод позвать дверь.** *(история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц1) Обходить больше нечего.*
- **КОММИТ:** два хода — `add` по своим путям, затем `commit` **с теми же путями после `--`** (полная форма и цена каждого хода — §4); коммить ПО ХОДУ работы, не одним последним ходом (§4). НИКОГДА `-A` / `.` / `commit -am`, и никогда `commit` без путей. Субагенты не коммитят. **`--no-optional-locks` обязателен:** обычный git переписывает индекс, берёт `.git/index.lock` и роняет параллельный ручной коммит владельца.
- **SCRATCHPAD — ТОЛЬКО ЛИЧНЫЙ.** Черновики, выкладки, промежуточные версии — в личную папку СВОЕГО захода `scratchpad/arhitektura-punkta/`. Общие пути (`scratchpad/otchet.md`, любой `scratchpad/*` без имени твоей темы) ЗАПРЕЩЕНЫ: чужой отчёт уедет в твой файл или твой — в чужой, а приёмка читает отчёт без построчной сверки и подмену НЕ ЛОВИТ по построению. (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц2)
- 🔴 **Звал `register_doc.py` — допиши `_studio/docs/KARTA.md` к своим путям В ОБОИХ ходах.** Строка регистрации лежит физически в нём. Ворота 5 читают `§6` **с диска**, а не из индекса: коммит без этого файла пройдёт ЗЕЛЁНЫМ, документ уедет сиротой, а строка умрёт при первом `checkout` (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц3).
- **ЗАПРЕТ:** ничего за пределами зоны, даже если «мешает» или «чинится в одну строку». Нашёл проблему вне зоны → в отчёт, не трогай.

## 0. ПЕРВЫЙ ХОД
### 0.1 🔴 ГИТ-КОНТУР — ДО ВСЕГО ОСТАЛЬНОГО, И ПЕРВЫМ ХОДОМ ЦЕЛИКОМ

🔴 «ничего сверх задачи» относится к СОДЕРЖАНИЮ работы; git-контур §0.1 — законное исключение, он про состояние репозитория и исполняется целиком.

🔴 **ПОРЯДОК ЗДЕСЬ — ЧАСТЬ УСТРОЙСТВА, А НЕ ОФОРМЛЕНИЕ. Сначала САМ прогоняешь две команды самопроверки контура (пункт 1 ниже), и только ПОТОМ заводишь свою рабочую папку** — её ветка отпочковывается от основной такой, какая она есть на момент запуска: контур пуст, доносить инструмент влитием нечего.

**1. ВЕСЬ КОНТУР ПУСТ — САМОПРОВЕРКА ВМЕСТО СУБАГЕНТА.** При сборке проверены три числа контура, и все три нулевые: невлитых `zahod/*`-веток 0 (🔴 снимок при сборке 2026-09-19, ПРОВЕРЬ ПЕРВЫМ ХОДОМ: `git --no-optional-locks branch --no-merged arka/mat-kostyak | grep -c 'zahod/'`); открытых заявок 0 (снимок при сборке 2026-09-19, пересчитать самому: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py zayavki`); названных `--vlit` 0. Звать субагента не за чем — выполни САМ две команды и вставь их вывод в `## ОТЧЁТ` дословно:
```
git --no-optional-locks branch --no-merged arka/mat-kostyak | grep -c 'zahod/'   # снимок при сборке 2026-09-19: 0
python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone kurs-puti-i-volny/plan/src kurs-puti-i-volny/tools/plany.py _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_arhitektura-punkta.md
```
Первая вернула не 0 — НИЧЕГО чужого не вливай (свою ветку вольёшь последним ходом, см. ниже), назови число строкой в `## ОТЧЁТ` и работай дальше. Вторая красная — сначала приведи в порядок свою зону.

Если при следующей сборке хоть одно из трёх чисел окажется ненулевым, генератор сам вернёт сюда задание субагенту гит-контура — печатает его дверь `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/bootstrap_zahod.py --zadanie-subagentu`; звать его в этом заходе не надо.

🔴 ОТВЕТ ЛЮБОГО субагента, которого ты запускаешь (не только этого), обязан КОНЧАТЬСЯ строкой «выдано N позиций из M найденных»: канал мог оборвать его молча, и без этой строки усечение неотличимо от честного «мало нашлось». Нет строки — ответ усечён, в `## ОТЧЁТ` не вставляй, перезапроси.

**2. ТЕПЕРЬ ЗАВОДИ СВОЮ РАБОЧУЮ ПАПКУ** (команда — в блоке «МЕСТО РАБОТЫ» выше) и работай в ней как обычно. Её ветка отпочкована от свежей основной, поэтому инструмент, которым ты работаешь, уже на диске — отдельного «влить перед работой» больше нет.

вливать нечего, проверено командой `git branch --no-merged` — но проверено ПРИ СБОРКЕ, а не сейчас: невлитых `zahod/*`-веток было 0. 🔴 снимок при сборке 2026-09-19, ПРОВЕРЬ ПЕРВЫМ ХОДОМ: `git --no-optional-locks branch --no-merged arka/mat-kostyak | grep -c 'zahod/'`. Число могло устареть между сборкой и твоим прогоном — 14.08 заход нёс ровно этот ноль, а к прогону невлитых было три.


- деплоя в этом заходе нет.

- Проверь ветку: `git branch --show-current` — обязано быть `arka/mat-kostyak`. Не она — СТОП, `git checkout` НЕ делай (§4 GIT-disciplina), нужен `--worktree`.
- Точка отката: `git add kurs-puti-i-volny/plan/src kurs-puti-i-volny/tools/plany.py _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_arhitektura-punkta.md` → commit (или zip), если зона не чиста в HEAD (не фабрикуй, если чиста).
- Прочитать ТОЛЬКО: `названные файлы-якоря`. Проект не изучай.
- ПЛАН — в `## ПЛАН` перед действиями.

## 1. ДИСЦИПЛИНА (Карпатов)
🔴 **Код возврата — ПЕРВЫМ, до содержательного вывода команды.** «Отработала» и «упала, а я читаю прошлое состояние» выглядят одинаково; сначала `echo $?`, потом выводы. То же с гейтами. (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц7)
Предпосылки/развилки назвать вслух; минимум без спекуляций; хирургия (строка → к заданию); критерий, который может провалиться. Якорные замены — abort при ≠1. Сохранять по умолчанию. **Оспорить ложную предпосылку — включая КРИТЕРИЙ ГОТОВНОСТИ: считаешь его кривым — скажи в `## ПЛАН`, ДО работы, и предложи поправку.** Субагенты: ≤5, рейт-лимит = отступить + доложить (не слепой ретрай).

🔴 **Пишешь содержательный текст — термин НЕ употребляется раньше, чем определён**, включая заголовки, подводки и формулировки теорем. «Определение в тексте есть» не считается: если оно ниже первого рабочего употребления, читатель встаёт ровно там. Чинится ПЕРЕСТАНОВКОЙ определения вверх, не дописыванием пояснения. Гейт: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/check_termin.py <src>` (exit 1 при нарушении). Канон — `../docs/kak-delat/STANDART-teksta.md` правило 11. (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц8)

## 2. ЗАДАЧА

🔴 **WRITE YOUR `## ОТЧЁТ`, `## ПЛАН` AND `## ВОПРОСЫ` IN ENGLISH, AND EVERY FILE AND EVERY COMMIT MESSAGE YOU PRODUCE TOO.** Owner's decision 30.08. It is a каркас-level rule, not a preference (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц9). Fixed Russian addresses stay Cyrillic: `ЦЕНА:` · `ВЕРДИКТ:` · `ДОМ:` · `ДОСТАВЛЕНО:` · `ПОДЪЁМ:` · `[ДОЛГ: …]` · every `## ` heading of this file · every path and command.
### 🔴 You design the FORM and build the MECHANISM. You write NO content.
The owner's rule (Д2): «in one position the architecture, in another — filling the structure». A position that designs the form and writes content at the same time always bends the form to what it already wrote. So: every ⭐ field stays EMPTY in your output. The next position (S4б) fills quarter 1.

### Read ONLY these, by name
- `kurs-puti-i-volny/plan/src/karkas.md` — the 32 topics; each has a title, *Объект* and *Ого*. The structure EXISTS: you translate it into machine form and add the missing fields, you do not invent it.
- `kurs-puti-i-volny/SBORKA/KALENDAR-i-sostav.md` — the owner's composition decision of 18.09 (topics 5–6, Euler pentagonal and Franklin, leave the main course for the club).
- `python3 kurs-puti-i-volny/proverki/kalendar_goda.py` — sessions per quarter: I=6, II=8, III=9, IV=10, total 33.
- `kurs-puti-i-volny/SBORKA/SLEDUYUSHCHIY-ZAHOD.md` — the successor context S1 wrote.
- `kurs-puti-i-volny/tools/indeks.py` — ONLY its docstring and the regexes `RE_ЯКОРЬ`, `RE_ССЫЛКА`: anchors are `<!--id: X-->`, links are `[[X]]` and nothing else.
- `kurs-puti-i-volny/tools/graf.py` (from S2) — ONLY its `--help` and section `[c]`.

### The course shape — SETTLED by the owner 19.09; encode it, do not re-derive it
The board advances; the weight is switched on and stays on.

| floor | board | weight | what falls out |
|---|---|---|---|
| lecture 1 | line | `q` off | binomial coefficients — the baby example of the whole course |
| quarter 1 | line | `q` on | Gaussian binomials, partitions. The quarter GENERALISES lecture 1 |
| next | ray | both at once | Catalan and `q`-Catalan together, in one pass |
| then | segment | both | everything above is a substitution in one function |
| last | — | — | analysis: asymptotics, Laplacian, the limit — SECOND HALF only (`kurs-puti-i-volny/ZAMYSEL.md`, id `analiz-vo-vtoruyu-polovinu`) |

Quarter 1 (6 Saturdays, 19.09–24.10) = lecture 1 (line, no `q`) + the `q` line (Young diagrams, Gaussian binomials, the generating function of partitions); the remaining Saturdays begin Catalan. Where karkas disagrees (block 3 and block 4 separate plain and `q` Catalan; topic 1 ends with $\sim1/\sqrt{\pi n}$), the table above wins.

### What to build
**1. `kurs-puti-i-volny/plan/src/punkty.md` — the ONE home of the list.** One section per item, anchored `<!--id: p-NN-->`, fields as plain `field: value` lines (no YAML inside the body, no code fences around items — `indeks.py` ignores text inside code). Fields proposed by the owner — you may add, rename in Latin transliteration if you must, but do not drop:

| field | meaning |
|---|---|
| `id` | `p-NN`, stable; every view refers to it |
| `imya` ⭐ | a title that makes you want to read it as a chapter of a book |
| `vopros` ⭐ | the beautiful question the item opens with |
| `teorema` ⭐ | the beautiful theorem — the «wow» |
| `zadacha` ⭐ | the beautiful problem |
| `doska` · `ves` | coordinate: `pryamaya / luch / otrezok / predel` · `q-vykl / q-vkl` |
| `obobshchaetsya-v` | id of the item this becomes later. **Selection gate: an item with no generalisation does not enter the course** (the last items of the year may point to a named `finish` marker you define) |
| `opiraetsya` | ids of items it cannot be read without — the graph edges |
| `adres` | where the material is: a SKELET statement, a card `[[kart-…]]`, a file |
| `chetvert` · `polovina` · `chast` | quarter 1–4; calendar half 1–2; content part `do-analiza` / `analiz` (the owner warns the part «до анализа» may NOT fit into two quarters — the form must allow it to spill over) |
| `iz-karkasa` | the karkas topic number(s) and a verbatim quote of its *Объект* / *Ого* — translation material for the filler, NOT a ⭐ field |
| `raskadrovka` | optional multi-line field: the minute-by-minute storyboard of a 90-minute session, used by the lecture view. Design its internal form (beats with minutes). Empty everywhere in your output |

Also design **level blocks** — one per level: `god`, `polugodie-1`, `polugodie-2`, `chast-do-analiza`, `chetvert-1` … `chetvert-4` — each with `obobshchenie` (ONE sentence: how this level generalises the finer one — the mandate requires every plan to open with it) and `svod` (a short paragraph that ties its items together). Empty in your output.

Fill the file with **exactly as many items as sessions: 33**, spread I=6, II=8, III=9, IV=10, each with `id`, `doska`, `ves`, `chetvert`, `polovina`, `chast`, `opiraetsya`, `obobshchaetsya-v`, `adres`, `iz-karkasa` — and ALL ⭐ fields and `raskadrovka` EMPTY. Item `imya` stays empty too; a provisional working label may go into `iz-karkasa`. Quarters 2–4 items: coordinate and karkas link only — the owner said filling them now is harmful, the form is not tried yet.

**2. `kurs-puti-i-volny/tools/plany.py` — the generator and the gates.** Standard library only. Parses `punkty.md` and writes these VIEWS, each beginning with a line saying it is generated by `tools/plany.py` from `punkty.md` and must not be edited by hand, plus a YAML header with `opisanie:`:
- `plan/src/god.md` — year: every item one line, `imya` + `vopros`;
- `plan/src/chast-1-do-analiza.md` — part «до анализа»: its items plus `teorema`;
- `plan/src/chetvert-1.md` … `chetvert-4.md` — quarter: all ⭐ fields in full;
- `plan/src/lekciya-1.md` — lecture: item `p-01` unfolded from its `raskadrovka`.
🔴 **Linkage that the existing gates can read.** In each view, every item section carries an anchor per level and a link one level up, in the only syntax `indeks.py` resolves: year sections `<!--id: god-pNN-->` with `[[p-NN]]`; part sections `<!--id: chast-pNN-->` with `[[god-pNN]]`; quarter sections `<!--id: chetvert-pNN-->` with `[[chast-pNN]]` (for items of the part «до анализа»; for items of the analysis part link `[[god-pNN]]` — say in the docstring how graf.py `[c]` must read that, and if graf.py needs a change, write it in `## ВОПРОСЫ` for the head, do not edit graf.py — it is outside your zone); lecture sections `<!--id: lekciya-pNN-->` with `[[chetvert-pNN]]`. Then `cd kurs-puti-i-volny && python3 tools/indeks.py` resolves every id and `graf.py` `[c]` counts zero orphans.
Gates — `python3 kurs-puti-i-volny/tools/plany.py --proverit` exits 1 on any of: an item without `opiraetsya` (except the first); a dangling id in `opiraetsya` / `obobshchaetsya-v`; an item without `obobshchaetsya-v`; items per quarter ≠ sessions per quarter read from `proverki/kalendar_goda.py` (import it or parse its output — do not retype 6/8/9/10); a ⭐ field empty in a quarter marked FILLED (`--napolnennye 1` by default: quarter 1); a generated view that differs from what the generator would write now (hand edit detected).

**3. Retire the hand-written lists — a banner, not a rewrite.** At the top of `plan/src/karkas.md` and `plan/src/plan.md` add a 2–3 line banner: the composition of the course now lives in `punkty.md`; the views are generated by `tools/plany.py`; this file stays as the source of the translation. Do not edit their bodies. Register each new `.md`: `python3 ../disciplina/_generator/tools/register_doc.py <path> "<one phrase>"`.

**4. Make the form beautiful to read.** The owner's requirement: the structure must become SELF-VALUABLE AND BEAUTIFUL, not a service table. `punkty.md` opens with a short human preface (what an item is, why it lives once, how to read the fields) — written in Russian, since the owner reads it.

**5. Successor context (last move).** At the end of this kod file under `## ОТЧЁТ`, and as a section `## Для наполнителя (S4б)` at the end of `punkty.md` preface: exactly what the filler must write, in which fields, for which items, and which gate turns green when done.

**КРИТЕРИЙ ГОТОВНОСТИ (может ПРОВАЛИТЬСЯ)** — each clause one command, return code first:
1. **Live run on the real items file:** `python3 kurs-puti-i-volny/tools/plany.py --proverit; echo $?` → `1`, and the ONLY failures it names are empty ⭐ fields of the 6 quarter-1 items (proves the ⭐ gate reds on the known-empty case; every other gate passes). With `--napolnennye none` → `0`.
2. `python3 kurs-puti-i-volny/tools/plany.py; echo $?` → `0`, and it prints the seven view paths it wrote (year, part «до анализа», quarters 1–4, lecture 1); paste that output.
3. `grep -c '^<!--id: p-' kurs-puti-i-volny/plan/src/punkty.md` → `33`.
4. `cd kurs-puti-i-volny && python3 tools/indeks.py; echo $?` → `0`, no line about a link to a non-existent id, no duplicate id.
5. `python3 kurs-puti-i-volny/tools/graf.py | grep -A3 '^\[c\]'` → orphans 0.

**Coverage line in the report:** «karkas topics mapped N of 32 (each listed with its item id or with the reason it left the main course) · views generated 7 of 7 · gates proven red on mutation 5 of 5».
**Отрицательный вердикт несёт ОХВАТ В СЕБЕ:** не «дыр не найдено», а «дыр не найдено, проверено X из Y». Без охвата вердикт не принимается — «проверено 2 из 9» и «проверено 9 из 9» выглядят одинаково.

## 3. ВЕРИФИКАТОР (если двигаем/теряем/жмём)

Верификатор нужен, тип — **ПОСЛЕ-типа** — судит результат, стоит в конце, после задачи. Свежий субагент, ДРУГИМ методом (fresh subagent that has not seen the work breaks punkty.md on purpose in a temp copy in five ways (empty star field in quarter 1, dangling id, orphan item, wrong quarter count, a hand edit of a generated view) and checks that plany.py goes red on each), не перечитывает свою же правку. Доля сплошной выборки: 5 of 5 mutations. Финальная строка ответа обязательна дословно: «выдано N позиций из M найденных» — без неё ответ считается усечённым и в отчёт не вставляется.

## 4. 🔴 КОММИТ СВОЕЙ ЗОНЫ — ПО ХОДУ РАБОТЫ, НЕ ОДНИМ ПОСЛЕДНИМ ХОДОМ
Ты работаешь host-side и в `.git` ПИШЕШЬ — значит коммитишь САМ, никому не передавая. Каждую завершённую часть работы коммить СРАЗУ, теми же двумя ходами — не копи всё к финальному ходу:
```
git --no-optional-locks add -- kurs-puti-i-volny/plan/src kurs-puti-i-volny/tools/plany.py _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_arhitektura-punkta.md                     # вводит НОВЫЕ пути в индекс
git --no-optional-locks commit -m "<зона>: <что сделано>" -- kurs-puti-i-volny/plan/src kurs-puti-i-volny/tools/plany.py _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_arhitektura-punkta.md   # отсекает всё чужое
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

**ЗОНА ГИГИЕНЫ:** `kurs-puti-i-volny/plan/src` `kurs-puti-i-volny/tools/plany.py` `_studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_arhitektura-punkta.md`

- **Г1. Зона доехала в git.** `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone kurs-puti-i-volny/plan/src` → ✅; `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone kurs-puti-i-volny/tools/plany.py` → ✅; `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_arhitektura-punkta.md` → ✅. Красное на любой из команд — отчёт не принимается: приёмка гоняет их все первым ходом.
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

1. §0.1 git contour self-check myself (wave-head note: the subagent is not launched): `git branch --show-current`, `git --no-optional-locks branch --no-merged arka/mat-kostyak | grep -c 'zahod/'` (→ 0), `GIT_ZONA_REPO="$PWD" git_zona.py check --zone ... --zone ... --zone ...` (repeated `--zone` per path, per the wave-head's note — a single-`--zone` call with three paths is rejected) → rc=0, zone empty (nothing to check yet, expected before building anything).
2. Read the six named anchors only: `karkas.md` (32 topics, blocks 1–7), `KALENDAR-i-sostav.md` (topics 5–6 moved to club, quarter breakdown 6/8/9/10), `kalendar_goda.py` output (confirms 6/8/9/10 = 33), `SLEDUYUSHCHIY-ZAHOD.md`, `indeks.py` docstring + `RE_ЯКОРЬ`/`RE_ССЫЛКА`, `graf.py --help` + the `gate_c` function body (the part of `[c]` I'm told to read).
3. **Challenge a premise, per §1's own rule.** `SLEDUYUSHCHIY-ZAHOD.md`'s "Lecture-by-Lecture Plan (Q1)" lists lectures 1–6 as karkas topics 1–6 (i.e. it still includes topic 5 Pentagonal and topic 6 Franklin in Q1). That contradicts the owner's later, explicitly SETTLED course-shape table in this very brief ("topics 5–6 leave the main course for the club" + "Quarter 1 = lecture 1 + the q-line; the remaining Saturdays begin Catalan"). `SLEDUYUSHCHIY-ZAHOD.md` predates the 18–19.09 club decision and is stale on this one point. I followed the brief's settled table (it explicitly says it wins over karkas where they disagree), not the stale file — flagging this rather than silently picking one.
4. Design the `punkty.md` item→karkas mapping: topics 1,2,3,4,7,8 → Q1 (6); 9–16 → Q2 (8); 17–25 → Q3 (9); 26 + 3 free slots (the "отрезок×вес-включён" gap named in `KALENDAR-i-sostav.md`) + 27–32 → Q4 (10). `doska` by wall count (0/1/2 walls → pryamaya/luch/otrezok; block 7 "Пределы" → predel, matching the owner's literal block name). `ves` per the owner's literal rule "board advances, weight switches on once and stays on": q-vykl only for p-01, q-vkl everywhere after. `opiraetsya`/`obobshchaetsya-v` as the plain linear chain karkas already reads in (translation of an existing order, not invented pedagogy), with a terminal `finish` anchor for `p-33` so the "every item generalises" gate has a legal target.
5. Build `punkty.md` (preface + 8 level blocks + 33 items, all ⭐ empty) via a throwaway assembler script kept in `scratchpad/arhitektura-punkta/` (not part of the deliverable), then hand-build `tools/plany.py` (stdlib only) as the real, lasting generator + `--proverit` gates.
6. Run criterion clauses 1–5 in the order given (they are ordered on purpose: `--proverit` runs BEFORE the plain generate, so "hand-edit / stale view" is correctly not flagged when a view simply doesn't exist yet).
7. **Anticipated, documented gate gap (not fixed — outside my zone):** the brief's own linkage spec requires a `chetvert-pNN` section of an `analiz`-part item (block 7, quarter 4) to link `[[god-pNN]]` instead of `[[chast-pNN]]`, because those items have no `chast-*` level. `graf.py`'s `gate_c` hard-codes `chetvert`'s required parent prefix as `chast-` only, with no exception. I built the spec faithfully and documented the exact gap (and the one-line fix `graf.py` would need) in `plany.py`'s own docstring, then verified live that this produces exactly 6 named orphans (the 6 `analiz` items) and zero unexpected ones — i.e. criterion clause 5 genuinely reds, for a reason I predicted before running it, not a mechanism bug. Flagged as a queue item below rather than edited (read-only zone).
8. Two-legged commit (`add` then `commit -- <paths>`) as soon as the mechanism was green, then push; spawn ONE fresh verifier subagent (mutation-tests `--proverit` five ways on a temp copy); write this report.
9. Register new `.md`? Checked first — `register_doc.py` explicitly refuses any path outside `_studio/`/`obzory/`/`_illustracii/`/`_meta/` and says project/course docs use their OWN index. `korni.карта_для()` returns `None` for every path under `kurs-puti-i-volny/`. So none of the 8 new `.md` files (`punkty.md` + 7 views) register anywhere — they're indexed the course's own way, via `opisanie:` in the YAML header + `tools/indeks.py` (which I ran and confirmed green). No `_studio/docs/KARTA.md` edit was made or needed. Documented as a factory-level finding in `## ВОПРОСЫ` below, since the top-level contract clause about `register_doc.py` reads as unconditional and isn't, for this class of path.

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

1. `graf.py`'s `gate_c` needs a small patch to accept the linkage this brief itself specifies: a `chetvert-pNN` anchor whose item has `chast: analiz` correctly links `[[god-pNN]]` (there is no `chast-pNN` for it — only `do-analiza` items get a `chast-*` level), but `gate_c`'s `parent_map = {'chetvert': 'chast', ...}` accepts ONLY a `chast-` prefixed target for any `chetvert-*` anchor, with no exception. Live-verified: `python3 kurs-puti-i-volny/tools/graf.py | grep -A3 '^[c]'` reads `orphans: 6`, and printing the orphan ids confirms they are exactly `chetvert-p-28`..`chetvert-p-33` (the six `analiz`-part items, quarter 4, block 7 "Пределы") — zero unexpected orphans elsewhere. The fix: in `gate_c`, when `level == 'chetvert'`, also accept a target starting with `god-` (or read the item's own `chast` field to pick the expected parent). `graf.py` is outside this position's zone (read-only) — documented in `tools/plany.py`'s own docstring in full detail, and criterion clause 5 below reports the real `orphans: 6`, not a claimed `0`.
   ДОМ: владелец
   ДОСТАВЛЕНО: нет
2. Factory-level finding, not specific to this task: the top-level contract clause "заВёл новый .md — регистрируешь через `register_doc.py`" reads as unconditional, but `register_doc.py` explicitly refuses any path outside `_studio/`, `obzory/`, `_illustracii/`, `_meta/` — verified live: it refused `kurs-puti-i-volny/plan/src/punkty.md` with the message "документы проектов живут в своих индексах — у курса, у лекции, у арки", and `korni.карта_для()` returns `None` for the same path (`kurs-puti-i-volny` is not one of the six roots in `КОРНИ_MATERIALS`). So for any project/course directory outside those four roots, the correct registration mechanism is the project's own index (here: `tools/indeks.py`, gated on `opisanie:` in the YAML header, which I used instead) — not `register_doc.py`. A future executor briefed with the generic contract clause and a course-internal file will hit the same wall; worth a one-line caveat in the bootstrap template ("register_doc.py only for `_studio/obzory/_illustracii/_meta` — course/project dirs register their own way").
   ДОМ: _studio/zhurnal/2026-08-24_obzor-funkciya-putey/UROKI-FABRIKE.md
   ДОСТАВЛЕНО: нет
3. `kurs-puti-i-volny/INDEKS.md` is left modified-but-uncommitted on disk (`git status --porcelain` shows ` M kurs-puti-i-volny/INDEKS.md`, +137/-1 lines) — a side effect of running `tools/indeks.py` as criterion clause 4 requires. It is outside this position's contracted zone (`plan/src`, `tools/plany.py`, this kod file only), so I did not commit it and did not revert it (both would be touching a path outside the zone in different directions). Whoever next commits inside `kurs-puti-i-volny/` should pick it up — the content is a correct, harmless regeneration reflecting the 8 new files.
   ДОМ: kurs-puti-i-volny/INDEKS.md
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

> **Note:** the §0.1 git-contour subagent was NOT launched this run (wave-head instruction: "run its
> two commands yourself"). This section is filled by the EXECUTOR instead of that subagent, using the
> same commands the contour subagent would run (`<основная>` read as `arka/mat-kostyak`, since that is
> what `zahod/*` branches merge into in this brief's own §0.1/closing-warning usage — there is no local
> `main` branch in this working copy, only `remotes/origin/main`).

**СНИМОК ВХОДА** *(снят до any work, first move of the session)*
```
$ git --no-optional-locks branch --no-merged arka/mat-kostyak
(пусто — 0 строк)
$ git --no-optional-locks status --porcelain | wc -l
       9
$ git --no-optional-locks log --oneline @{u}.. | wc -l
       0
$ GIT_ZONA_REPO="$PWD" python3 .../git_zona.py zayavki
✅ заявок нет
(«ждут захода-разработчика» redirected queue: 12 items, none addressed to this position/zone;
 POSTOYANNYE.md: 0 branches-not-to-merge; охват: заявок открыто 0, переадресовано 12,
 постоянных исключений 1, сторож краснеет на 0)
```
The 9 uncommitted files at input were all OTHER writers' work, none touching my zone: `_studio/zhurnal/_INFRA-git/INCIDENTY.md` (modified) and 8 untracked files under `SBORKA/`, `_fond/zadachi/risunki/`, `diskmat-57/2026-08-18_logika-goda-7/` — none inside `kurs-puti-i-volny/plan/src`, `kurs-puti-i-volny/tools/plany.py`, or this kod file. Left untouched throughout, as required.

**ЧТО СДЕЛАНО**
Nothing for the git-contour half to do: all three contour numbers were already 0 at the snapshot
(matches the brief's own printed snapshot at assembly time) and stayed 0 through the whole session
(reverified at the end: `git --no-optional-locks branch --no-merged arka/mat-kostyak | grep -c 'zahod/'` → `0`).
No merge, no vyvoz-of-someone-else's-branch, no gasheniye, no zayavka needed or created.
My OWN work: committed `4c30d5b9` directly onto `arka/mat-kostyak` (no separate `zahod/*` branch or
worktree was spawned — the wave-head's contract explicitly says to work in the main folder on
`arka/mat-kostyak` itself, not to create one), then pushed it (`origin/arka/mat-kostyak`
`d3bd0803..4c30d5b9`).

**ВСЕ ДОЛГИ ВХОДА ЗАКРЫТЫ:** `да`
*(all three contour numbers were 0 at input and remained 0; the 9 unrelated dirty files belong to other
writers and are not this position's debt to close — named above, left alone.)*

## ОТЧЁТ — (заполняет исполнитель)

**What was done + why.** Built the FORM and MECHANISM for the course's item list, per Д2 (architecture and
filling are separate positions): `kurs-puti-i-volny/plan/src/punkty.md` is now the single home of all 33
session items (id, coordinate `doska`/`ves`, calendar `chetvert`/`polovina`/`chast`, graph edges
`opiraetsya`/`obobshchaetsya-v`, `adres`, `iz-karkasa` translation material — all filled; the four ⭐
fields `imya`/`vopros`/`teorema`/`zadacha` plus `raskadrovka` — empty everywhere, as mandated). Wrote NO
narrative/pedagogical content. `kurs-puti-i-volny/tools/plany.py` (stdlib only) parses `punkty.md` and
generates the seven views (year, part «до анализа», quarters 1–4, lecture 1) plus a `--proverit` gate
family; a view is never hand-written, exactly like `tools/indeks.py`. `karkas.md` and `plan.md` got a
2–4 line banner pointing to the new home; their bodies were not touched.

**How verified.** All 5 readiness-criterion clauses run for real, verbatim (see below); `tools/indeks.py`
green; `tools/graf.py`'s `[c]` gate run and its 6 orphans traced to source (see clause 5 and `## ВОПРОСЫ`
#1); a hand sanity check that `--proverit` actually catches a real hand-edit (appended a line to
`god.md`, confirmed rc=1, then restored it before committing); a FRESH subagent (no context of this
session) mutation-tested `--proverit` five ways on a **temporary copy** — 5 of 5 caught, see below.

**What was NOT touched.** `karkas.md`/`plan.md` bodies (banner only); `ZAMYSEL.md` (not read, not
edited — closed document per the wave-head note, and not in the "read only these" list either);
`graf.py`, `indeks.py` (read-only, per the read list); `_studio/docs/KARTA.md` (no `register_doc.py`
call was made — see `## ВОПРОСЫ` #2 for why); the 9 other writers' dirty files at session start (none
in my zone); `kurs-puti-i-volny/INDEKS.md` (regenerated by the criterion-4 command, left uncommitted —
outside my zone, see `## ВОПРОСЫ` #3); no worktree, no branch switch, no `git checkout`.

**Verifier result (fresh subagent, mutation-tested `--proverit` on a temp copy, 5 of 5):**
```
a) empty ⭐ field, quarter 1 : rc=1 — pass — "⭐ пусто: p-03.teorema"
b) dangling id               : rc=1 — pass — "висячий id в obobshchaetsya-v пункта p-04: 'p-99'"
c) orphan item (no obob.-v)  : rc=1 — pass — "без obobshchaetsya-v (...): p-07"
d) wrong quarter count       : rc=1 — pass — "четверть 1: пунктов 7, занятий по календарю 6" (+ квартал 2)
e) hand-edited generated view: rc=1 — pass — "вид разошёлся с генератором (правка руками?): god.md"
Overall: 5 of 5 mutations caught, no false negatives, no misleading messages.
выдано 5 позиций из 5 найденных
```

**Readiness criterion, clauses 1–5, verbatim (all run from the repo root, after the plain generate for
clauses 3–5, matching the brief's own stated order — `--proverit` before the first plain generate for
clause 1):**
```
$ python3 kurs-puti-i-volny/tools/plany.py --proverit; echo $?
❌ 24 нарушения:
  - ⭐ пусто: p-01.imya
  - ⭐ пусто: p-01.vopros
  - ⭐ пусто: p-01.teorema
  - ⭐ пусто: p-01.zadacha
  [... same 4 fields for p-02 .. p-06, 24 lines total, ALL of them ⭐-empty on quarter-1 items,
       NO other kind of failure named ...]
1

$ python3 kurs-puti-i-volny/tools/plany.py --proverit --napolnennye none; echo $?
✅ punkty.md чист
0

$ python3 kurs-puti-i-volny/tools/plany.py; echo $?
wrote kurs-puti-i-volny/plan/src/god.md
wrote kurs-puti-i-volny/plan/src/chast-1-do-analiza.md
wrote kurs-puti-i-volny/plan/src/chetvert-1.md
wrote kurs-puti-i-volny/plan/src/chetvert-2.md
wrote kurs-puti-i-volny/plan/src/chetvert-3.md
wrote kurs-puti-i-volny/plan/src/chetvert-4.md
wrote kurs-puti-i-volny/plan/src/lekciya-1.md
0

$ grep -c '^<!--id: p-' kurs-puti-i-volny/plan/src/punkty.md
33

$ cd kurs-puti-i-volny && python3 tools/indeks.py; echo $?
✍ INDEKS.md собран: 89 файлов, 223 узлов
документов:          89
узлов графа:         223  (карточек 24, якорей 199)
ссылок:              182
без описания:        1  (унаследованных 1, новых 0)
⚠ унаследованный долг: 1 файлов без описания. Список — tools/DOLG-bez-opisaniya.txt
✅ гейт зелёный
0

$ python3 kurs-puti-i-volny/tools/graf.py | grep -A3 '^[c]'
[c] Plan anchors: 94 · orphans: 6
```
**Clause 5 did NOT reach `orphans 0` — this is a documented, predicted-before-running mismatch, not a
build defect.** Traced live (script printing `gate_c`'s own orphan list): the 6 orphans are exactly
`chetvert-p-28`..`chetvert-p-33` — the six `chast: analiz` items (quarter 4, block 7 «Пределы»). Per
this brief's own linkage spec, an `analiz`-part item's `chetvert-pNN` section links `[[god-pNN]]`
(it has no `chast-pNN`, only `do-analiza` items do); `graf.py`'s `gate_c` hard-codes `chetvert`'s
required parent as `chast-` only, with no `god-` exception, so it counts these 6 as orphans regardless.
Full analysis and the one-line fix `graf.py` needs are in `tools/plany.py`'s own docstring and in
`## ВОПРОСЫ` #1 (`graf.py` is read-only to this position). Clauses 1–4 all pass exactly as specified;
clause 1's `--napolnennye none` variant → `0` as specified.

**Coverage line:** karkas topics mapped 30 of 32 (topics 1–4 → p-01..p-04 · topics 7–8 → p-05..p-06 ·
topics 9–16 → p-07..p-14 · topics 17–25 → p-15..p-23 · topic 26 → p-24 · topics 27–32 → p-28..p-33 ·
topics 5–6 left the main course for the club, `KALENDAR-i-sostav.md`, owner 18.09 · p-25/p-26/p-27 are
the 3 free Q4 slots for the "отрезок×вес-включён" gap, no karkas topic) · views generated 7 of 7 ·
gates proven red on mutation 5 of 5.

**Open "return to."** #1 in `## ВОПРОСЫ` (the `graf.py [c]` gap) is the one item a future pass should
close before anyone treats `orphans: 0` as achievable without it — right now it is structurally
unreachable for the `analiz` part, by design, until `graf.py` gets the one-line fix.

**Repeatability of findings.** None of the three `## ВОПРОСЫ` findings recur on the very next unit of
work (S4б, the filler, only edits `punkty.md` field values for the 6 quarter-1 items — it does not run
`graf.py`, does not create new `.md` files, and does not touch `INDEKS.md`) — legitimately queue items,
not "class NEMEDLENNOE" fixes-before-next-run.

**НЕОБРАТИМОЕ:** необратимого нет. No deletion, overwrite, rename, move, `git reset`/`checkout`
over unsaved work, or edit outside the zone occurred.

**АРТЕФАКТ:** `/Users/ivanyakovlev/Documents/GitHub/materials/kurs-puti-i-volny/plan/src/punkty.md` —
open as plain Markdown (any text editor); the 7 generated views live alongside it in the same
`kurs-puti-i-volny/plan/src/` directory (`god.md`, `chast-1-do-analiza.md`, `chetvert-1.md`..
`chetvert-4.md`, `lekciya-1.md`), and the generator itself is
`/Users/ivanyakovlev/Documents/GitHub/materials/kurs-puti-i-volny/tools/plany.py`.

**РОД АРТЕФАКТА:** `исходник` (this zahod's product is code + the source-of-truth data file, not a
rendered document — committed before this report, per the convention for `исходник`).

**КОММИТ:** `4c30d5b9` — "kurs-puti-i-volny: punkty.md single home + tools/plany.py view generator" ·
`git_zona.py check --zone kurs-puti-i-volny/plan/src` → ✅ · `--zone kurs-puti-i-volny/tools/plany.py`
→ ✅ · `--zone _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_arhitektura-punkta.md` → ✅ (this kod
file itself, with the `## ПЛАН`/`## ВОПРОСЫ`/`## ГИГИЕНА ВХОДА`/`## ОТЧЁТ` sections below, is committed
separately as the session's closing move — see the final git-hygiene numbers above `## ПРАВКИ ПОСЛЕ
ВЫДАЧИ`). Pushed: `origin/arka/mat-kostyak d3bd0803..4c30d5b9`.

**PRAVKI PROCHITANY:** none — `## ПРАВКИ ПОСЛЕ ВЫДАЧИ` was empty (`<правок нет>`) both at start and at
every re-check before writing this report.

**Closing git hygiene (ran the full `## ⚠️🔴 WARNING` block):**
```
1 · ВСЕ КОММИТЫ: git --no-optional-locks status --porcelain -- kurs-puti-i-volny/plan/src kurs-puti-i-volny/tools/plany.py \
    _studio/zhurnal/.../kod_arhitektura-punkta.md → empty (own zone: "вне git 0")
2 · ВЛИТИЕ СВОЕЙ ВЕТКИ В ОСНОВНУЮ: NOT APPLICABLE — per the wave-head's explicit contract ("work in
    this main folder, do not create a worktree, never switch branches"), this position committed
    DIRECTLY onto `arka/mat-kostyak` in the shared main folder; there is no separate `zahod/*` branch
    of its own to merge. `vlit-v-osnovnuyu`'s `branch` argument is a merge SOURCE (verified via
    `--help`) — running it with `arka/mat-kostyak` while `arka/mat-kostyak` is itself the checked-out
    branch would be a merge into itself, not the intended operation. Nothing skipped: the same commit
    that would have been merged IS already on `arka/mat-kostyak`.
3 · ПОСТ-ПРОВЕРКА ИЗ ГЛАВНОЙ ПАПКИ: this session ran everything from that exact folder throughout — the
    5 criterion clauses above ARE the post-check; rerun once more after the final commit, unchanged
    results (`plany.py --proverit --napolnennye none` → 0, `indeks.py` → 0).
4 · ГАШЕНИЕ: `git --no-optional-locks branch --no-merged arka/mat-kostyak | grep -c 'zahod/'` → `0`
    (unchanged from the input snapshot — no branch was created, none needs extinguishing).
5 · ВЫВОЗ: `git --no-optional-locks log --oneline @{u}.. | wc -l` → `0` after the push above.
6 · ПРОВЕРКА ФАКТОМ: вне git (своя зона) 0 · невлитых своих 0 (нет своей ветки) · невлитых чужих
    (unmerged zahod/*) 0 · невывезенных своей ветки 0 · пост-проверка зелёная.
```

**ЗАЯВКИ, ПОСТАВЛЕННЫЕ ЭТИМ ЗАХОДОМ:** заявок нет — ни одна из пяти операций (влитие/коммит/вывоз/
деплой/гашение) не встретила препятствия, требующего заявки.

## ПРАВКИ ПОСЛЕ ВЫДАЧИ — (заполняет АНАЛИТИК; исполнитель ЧИТАЕТ)
> 🔴 **Пусто — значит заход не правился с момента выдачи.** Непустой блок читается ПЕРЕД продолжением работы: правка отменяет любое противоречащее ей место выше по файлу, каким бы категоричным оно ни было.
> **Форма строки — жёсткая, по ней судит приёмка:** `### ПРАВКА N · ГГГГ-ММ-ДД ЧЧ:ММ · <что изменилось, одной фразой>`, дальше — что именно перечитать и что откатить, если уже сделано по старой редакции.
> **Аналитик:** внёс правку — обязан ОТДЕЛЬНО послать владельцу короткое сообщение для пересылки исполнителю. Правка, лежащая только в файле, до работающего исполнителя не доезжает: он файл не перечитывает сам.
> **Исполнитель:** прочитал правку — назови её номер в `## ОТЧЁТ` строкой `ПРАВКИ ПРОЧИТАНЫ: 1, 2`. Нет строки при непустом блоке = отчёт не принимается: неизвестно, по какой редакции работали.

<правок нет>

## ФАЗА ПРИЁМКИ — (заполняет АНАЛИТИК, не исполнитель)
> 🔴 **Без этого раздела заход НЕ ЗАКРЫТ.** Гейт — `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/priyomka.py <этот файл>` (Г13): пока раздел пуст или несёт плейсхолдеры, приёмка красная, и это единственное место, где вердикт остаётся ЗАПИСАННЫМ, а не сказанным в чат.
> Заполняется ПОСЛЕ отчёта исполнителя. Исполнителю сюда писать нечего — его половина выше.

**ВЕРДИКТ:** `принято` — S4a Sonnet: 268k tokens (ceiling 150k exceeded 1.8x), 25 min, commits 4c30d5b9 c73b6ec9. Head re-run: plany.py --proverit rc=1 with exactly 24 empty star fields of p-01..p-06 and nothing else; --napolnennye none rc=0; 33 items; 7 views; owner's 19.09 shape encoded (p-01 line q off, p-02..04 line q on, p-05..06 ray). Clause 5 was red (6 orphans: analysis-part quarter anchors link god directly) — the gate, not the form, was wrong against the mandate's 'upward'; head repaired graf.py in 681b9aec, orphans 0 of 94. Weakness to carry: obobshchaetsya-v is a linear next-item chain, so the selection gate passes by construction. (copied from the mandate's VERDICTS by the wave head at closing, 2026-09-19)

**ВЕТКА РАБОТЫ:** `arka/mat-kostyak`
*(проверяется фактом, не словом: ветка обязана существовать и быть либо ВЛИТА в основную, либо названа в открытой заявке на влитие. Ни того, ни другого — Г14 краснеет. Снять состояние: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py poteri --branch <ветка>`)*

**ЗАЯВКИ, ПОСТАВЛЕННЫЕ ЭТОЙ ПРИЁМКОЙ — ПРОДУБЛИРУЙ СЮДА ТО, ЧТО УЖЕ ЛЕЖИТ В СПИСКЕ:**
> Адрес списка: `/Users/ivanyakovlev/Documents/GitHub/materials/_studio/zhurnal/_INFRA-git/zayavki`
> Читается командой (из любой папки, в том числе из worktree): `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py zayavki`
> Ставится командой: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py zayavka --rod <git-operaciya|pravka-koda> "<текст>"`
> 🔴 Вопрос здесь НЕ «что ты хочешь сделать», а «что ты УЖЕ положил в очередь». Дубль сверяется с очередью по id машинно; намерение сверить не с чем.

заявок нет: the position worked in the main folder on `arka/mat-kostyak` and pushed its own commits; nothing to merge or extinguish.

*(Заявок эта приёмка не ставила — так и напиши строкой «заявок нет: <почему ни одна из пяти операций не понадобилась>». Пустая строка и прочерк не принимаются: молчание неотличимо от «забыл».)*
