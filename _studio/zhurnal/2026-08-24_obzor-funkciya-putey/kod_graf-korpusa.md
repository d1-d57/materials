# Канал исполнителя — graf-korpusa (один заход до конца)
> Твой единственный файл-заход. Читай ТОЛЬКО его и названные якоря; проект не изучай.
<!-- собран bootstrap_zahod.py -->
<!-- гейт сборки заполненного: ЖДЁТ -->
> План/вопросы/отчёт — в секции внизу. Метрика — КАЧЕСТВО. Часы — норма.
> **Модель: openrouter/thinkingmachines/inkling:free** — one tool on top of existing graph primitives, machine criterion; free model by the wave mandate (tokens are the binding constraint), the runner swaps in a live free model.

## СТАРТОВОЕ СООБЩЕНИЕ ВЛАДЕЛЬЦУ

> Это блок для владельца — то, чем тебя запустили. Исполнителю здесь делать нечего, твоё задание ниже.

```
python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py worktree add graf-korpusa --branch zahod/graf-korpusa && cd /Users/ivanyakovlev/Documents/GitHub/materials-wt/graf-korpusa && opencode run --auto --model openrouter/thinkingmachines/inkling:free 'Твой заход — файл _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_graf-korpusa.md. Прочитай ТОЛЬКО его и то, что он называет; остальной проект не изучай. План/вопросы/отчёт пиши в этот же файл внизу (## ПЛАН / ## ВОПРОСЫ / ## ОТЧЁТ). Ничего сверх задачи не трогай — «ничего сверх задачи» относится к СОДЕРЖАНИЮ работы; git-контур §0.1 — законное исключение, он про состояние репозитория и исполняется целиком.' < /dev/null 2>&1 | tee /tmp/zahod-graf-korpusa.log
```

🔴 БЛОК ВЫШЕ — МАШИННЫЙ: его достаёт и запускает надзорный оркестратор, подменив в нём модель на живую. РУКАМИ ЕГО НЕ ЗАПУСКАЮТ — запуск без надзора и был тем, чем оплатили ночь на 05.09 (три позиции из шести не изменили ни байта: модели выгорели по квоте, а перевыбирать их было нечему).

ЗАПУСКАТЬ — ЭТИМ (проба живости и перевыбор модели внутри):
```
cd /Users/ivanyakovlev/Documents/GitHub/materials-wt/graf-korpusa && python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/orkestr.py _studio/zhurnal/2026-08-24_obzor-funkciya-putey --rezhim progon --dvizhok opencode --rod instrumenty --model openrouter/thinkingmachines/inkling:free --zahody kod_graf-korpusa.md 2>&1 | tee /tmp/nadzor-graf-korpusa.log
```

── СЧЁТ НЕЗАКРЫТОГО (печать, не гейт) ──
ГРАНИЦА ОБЛАСТИ: сырые подстроки в `kod_*.md` (пункт 4) — НЕ парсер очереди `dostavit_urok` (который считает только пары ДОМ:/ДОСТАВЛЕНО:). Разница в числах — законна.
🔴 снимок при сборке 2026-09-19, ПРОВЕРЬ ПЕРВЫМ ХОДОМ: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/schet_nezakrytogo.py _studio/zhurnal/2026-08-24_obzor-funkciya-putey`
Область: «_studio/zhurnal/2026-08-24_obzor-funkciya-putey» — сужены пункты 1, 3, 4; долги (2) глобальны намеренно (DOLG.md не размечен по записям).
Приоритет владельца: разобрать инциденты важнее, потом закрыть долги — неразобранный инцидент это повторяющаяся ошибка, долг может подождать.
  1. инцидентов без вердикта             : 0
  2. долгов СТАТУС: ЖИВ                  : н/д — ни одного skills/*/DOLG.md нет на диске (другой git-репозиторий)
  3. уроков фабрике без ВЕРДИКТ          : 39
  4. пунктов очереди «ДОСТАВЛЕНО: нет»   : 16
     из них разбором очереди (парсер `dostavit_urok`, записи с парой ДОМ:/ДОСТАВЛЕНО:): 4
       живых (чинится доставкой — «дом есть»)  : 2
       к владельцу (решение за человеком)      : 1
       адрес недоступен (нет/папка/код/указат.) : 1
       адрес не разобран                        : 0
       отработавших (машинный след закрытия)    : 0
       доставлено                               : 0
       🔴 не проверяется машиной: содержательная отработанность записей БЕЗ следа закрытия (метки в доме, строки ✅/ЗАКРЫТО) — нужна ревизия человеком; сырой греп сверх разбора — шаблонные строки формы.

🔴 ДВЕРЬ НЕЗАКОММИЧЕННЫХ `kod_*.md` ОТКРЫТА КЛАПАНОМ: в арке `_studio/zhurnal/2026-08-24_obzor-funkciya-putey` есть 1 незакоммиченных файлов-заходов `kod_pasporta-korpusa.md` — второй заход в такую арку обычно не собирается (долг 4 `disciplina-git`), но АНАЛИТИК открыл клапан, причина дословно: «S1 (kod_pasporta-korpusa.md) is live and writes its own kod file; S2 is only assembled now and starts after S1 is committed». Отключение видно здесь, в артефакте, а не осталось решением в голове аналитика.

🔴 ДВЕРЬ ГЕЙТА СБОРКИ ЗАПОЛНЕННОГО ФАЙЛА ОТКРЫТА КЛАПАНОМ: в арке `_studio/zhurnal/2026-08-24_obzor-funkciya-putey` лежат файлы-заходы со штампом «ЖДЁТ», красные на `check_sborki.py` — `kod_pasporta-korpusa.md` — следующий заход в такую арку обычно не собирается, но АНАЛИТИК открыл клапан, причина дословно: «kod_pasporta-korpusa.md was assembled in the Cowork sandbox: its 4 reds are 3 sandbox /sessions/ paths in price footnotes (not work addresses) and C4 on SLEDUYUSHCHIY-ZAHOD.md, the file that position itself creates; it is live, the head does not write into a live brief». Отключение видно здесь, в артефакте, а не осталось решением в голове аналитика.

КОНТЕКСТ. The year course «Пути и волны» lives in three homes (`kurs-puti-i-volny/`, `obzory/funkciya-putey-i-ee-uravneniya/`, `catalan/kartoteka/`); `kurs-puti-i-volny/tools/indeks.py` already collects its nodes and links into `INDEKS.md`. Previous stage (S1 of this wave) wrote descriptions into every file header and links `[[kart-…]]` from the corpus into the card index. ЦЕЛЬ: one tool that makes this graph MEASURABLE — six questions nobody answers today, plus the orphan check the next four writing stages will be judged by.
Приёмка — по ОТЧЁТУ, без построчной сверки. If you stop early: a committed `graf.py` answering some of the six questions is worth more than an uncommitted one answering all six — commit after each question that works.

## ЧТО ФИНАЛИЗИРОВАНО НА ИНТЕРВЬЮ

ИНТЕРВЬЮ ПРОВЕДЕНО: да (2026-09-19) — флаг `--intervyu da` при сборке. ⚠ Он доказывает, что аналитик не ЗАБЫЛ про интервью, и НЕ доказывает, что разговор был.

1. The knowledge index is the OUTPUT of tools/indeks.py built from file headers; never hand-edited
2. IWE and any markdown normaliser are not installed: they delete anchors and break KaTeX
3. The link year -> quarter -> lecture must be a machine-checkable id reference [[id]], not prose
4. Every position prepares its successor: its last move writes the successor context

## КОНТРАКТ ЗОНЫ (обязателен — не удалять; вписан Cowork)
- **МЕСТО РАБОТЫ:** **рабочая папка `/Users/ivanyakovlev/Documents/GitHub/materials-wt/graf-korpusa`** — МЕСТО ВСЕЙ РАБОТЫ (worktree захода, ветка `zahod/graf-korpusa` в ней уже стоит). 🔴 **ПЕРВЫЙ ХОД — `cd /Users/ivanyakovlev/Documents/GitHub/materials-wt/graf-korpusa`; ДАЛЬШЕ — ТОЛЬКО ПУТИ ОТНОСИТЕЛЬНО ЭТОЙ ПАПКИ** (или `cd` в неё безусловно, каждым ходом): `python3 _generator/tools/…` зовёт копию инструмента в ней же, пути зоны и арки — её файлы. Абсолютный путь в главную папку репозитория здесь — типичная ошибка, правка утекает МИМО worktree и найдётся только на коммите («вне git» в `git_zona.py check --zone` из рабочей папки, на файле, который уже правил, — цена, оплаченная живьём: 5 файлов, ручное копирование и откат главной папки). 🔴 `git checkout` в основной папке ЗАПРЕЩЁН: рядом идут другие заходы, переключение подменит файлы у них под ногами. 🔴 **Файл-заход — КОПИЯ `_studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_graf-korpusa.md` в твоей рабочей папке**: ПЛАН/ВОПРОСЫ/ОТЧЁТ/УРОКИ пишешь в неё и коммитишь её в свою ветку вместе с зоной (путь копии в зоне уже есть). Копии в папке нет — перенеси её из основной ветки: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py adopt --branch arka/mat-kostyak --zone _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_graf-korpusa.md --yes` (дирижёр волны кладёт её сам при старте). Существующую копию не затирай: в ней твоя работа. Отчёт читают в ней: дирижёр — сразу, приёмка — после влития ветки. При влитии копия может дать конфликт add/add с файлом-заходом основной ветки (ветка заведена раньше, чем заход попал в git) — это законно и разрешается объединением: план, вопросы и отчёт — из копии, правки после выдачи — из основного файла. 🔴 **Ветку в конце вливаешь САМ, последним ходом, после коммита зоны** (решение владельца 25.08; полный порядок печатает WARNING-блок ниже).
- **ЗОНА (можно менять):** `kurs-puti-i-volny/tools/graf.py` `kurs-puti-i-volny/SBORKA/ZAMER-grafa.md` `kurs-puti-i-volny/SBORKA/graf-rebra.tsv` `_studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_graf-korpusa.md`. Всё вне — **READ-ONLY**: не править, не двигать, не удалять, не рефакторить «заодно».
- 🔴 **ЗАВЁЛ НОВЫЙ `.md` — РЕГИСТРИРУЕШЬ ЕГО САМ, ТЕМ ЖЕ ХОДОМ, ОДНОЙ КОМАНДОЙ:** `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/register_doc.py <путь> "<описание>"` (из корня репо). `_studio/docs/` тебе по-прежнему READ-ONLY **для правки руками** — дверь ровно одна, и это она. Дверь идемпотентна (повторный вызов дубля не заведёт) и отказывает на пути вне `_studio/`, на несуществующем файле и на пустом описании. Свой файл-заход регистрировать не нужно: он рождается зарегистрированным из `bootstrap_zahod.py`. **Красный хук на ТВОЁМ новом `.md` — это не повод для `--no-verify`, а повод позвать дверь.** *(история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц1) Обходить больше нечего.*
- **КОММИТ:** два хода — `add` по своим путям, затем `commit` **с теми же путями после `--`** (полная форма и цена каждого хода — §4); коммить ПО ХОДУ работы, не одним последним ходом (§4). НИКОГДА `-A` / `.` / `commit -am`, и никогда `commit` без путей. Субагенты не коммитят. **`--no-optional-locks` обязателен:** обычный git переписывает индекс, берёт `.git/index.lock` и роняет параллельный ручной коммит владельца.
- **SCRATCHPAD — ТОЛЬКО ЛИЧНЫЙ.** Черновики, выкладки, промежуточные версии — в личную папку СВОЕГО захода `scratchpad/graf-korpusa/`. Общие пути (`scratchpad/otchet.md`, любой `scratchpad/*` без имени твоей темы) ЗАПРЕЩЕНЫ: чужой отчёт уедет в твой файл или твой — в чужой, а приёмка читает отчёт без построчной сверки и подмену НЕ ЛОВИТ по построению. (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц2)
- 🔴 **Звал `register_doc.py` — допиши `_studio/docs/KARTA.md` к своим путям В ОБОИХ ходах.** Строка регистрации лежит физически в нём. Ворота 5 читают `§6` **с диска**, а не из индекса: коммит без этого файла пройдёт ЗЕЛЁНЫМ, документ уедет сиротой, а строка умрёт при первом `checkout` (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц3).
- **ЗАПРЕТ:** ничего за пределами зоны, даже если «мешает» или «чинится в одну строку». Нашёл проблему вне зоны → в отчёт, не трогай.

## 0. ПЕРВЫЙ ХОД
### 0.1 🔴 ГИТ-КОНТУР — ДО ВСЕГО ОСТАЛЬНОГО, И ПЕРВЫМ ХОДОМ ЦЕЛИКОМ

🔴 «ничего сверх задачи» относится к СОДЕРЖАНИЮ работы; git-контур §0.1 — законное исключение, он про состояние репозитория и исполняется целиком.

🔴 **ПОРЯДОК ЗДЕСЬ — ЧАСТЬ УСТРОЙСТВА, А НЕ ОФОРМЛЕНИЕ. Сначала САМ прогоняешь две команды самопроверки контура (пункт 1 ниже), и только ПОТОМ заводишь свою рабочую папку** — её ветка отпочковывается от основной такой, какая она есть на момент запуска: контур пуст, доносить инструмент влитием нечего.

**1. ВЕСЬ КОНТУР ПУСТ — САМОПРОВЕРКА ВМЕСТО СУБАГЕНТА.** При сборке проверены три числа контура, и все три нулевые: невлитых `zahod/*`-веток 0 (🔴 снимок при сборке 2026-09-19, ПРОВЕРЬ ПЕРВЫМ ХОДОМ: `git --no-optional-locks branch --no-merged arka/mat-kostyak | grep -c 'zahod/'`); открытых заявок 0 (снимок при сборке 2026-09-19, пересчитать самому: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py zayavki`); названных `--vlit` 0. Звать субагента не за чем — выполни САМ две команды и вставь их вывод в `## ОТЧЁТ` дословно:
```
git --no-optional-locks branch --no-merged arka/mat-kostyak | grep -c 'zahod/'   # снимок при сборке 2026-09-19: 0
python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone kurs-puti-i-volny/tools/graf.py kurs-puti-i-volny/SBORKA/ZAMER-grafa.md kurs-puti-i-volny/SBORKA/graf-rebra.tsv _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_graf-korpusa.md
```
Первая вернула не 0 — НИЧЕГО чужого не вливай (свою ветку вольёшь последним ходом, см. ниже), назови число строкой в `## ОТЧЁТ` и работай дальше. Вторая красная — сначала приведи в порядок свою зону.

Если при следующей сборке хоть одно из трёх чисел окажется ненулевым, генератор сам вернёт сюда задание субагенту гит-контура — печатает его дверь `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/bootstrap_zahod.py --zadanie-subagentu`; звать его в этом заходе не надо.

🔴 ОТВЕТ ЛЮБОГО субагента, которого ты запускаешь (не только этого), обязан КОНЧАТЬСЯ строкой «выдано N позиций из M найденных»: канал мог оборвать его молча, и без этой строки усечение неотличимо от честного «мало нашлось». Нет строки — ответ усечён, в `## ОТЧЁТ` не вставляй, перезапроси.

**2. ТЕПЕРЬ ЗАВОДИ СВОЮ РАБОЧУЮ ПАПКУ** (команда — в блоке «МЕСТО РАБОТЫ» выше) и работай в ней как обычно. Её ветка отпочкована от свежей основной, поэтому инструмент, которым ты работаешь, уже на диске — отдельного «влить перед работой» больше нет.

вливать нечего, проверено командой `git branch --no-merged` — но проверено ПРИ СБОРКЕ, а не сейчас: невлитых `zahod/*`-веток было 0. 🔴 снимок при сборке 2026-09-19, ПРОВЕРЬ ПЕРВЫМ ХОДОМ: `git --no-optional-locks branch --no-merged arka/mat-kostyak | grep -c 'zahod/'`. Число могло устареть между сборкой и твоим прогоном — 14.08 заход нёс ровно этот ноль, а к прогону невлитых было три.


- деплоя в этом заходе нет.

- `cd /Users/ivanyakovlev/Documents/GitHub/materials-wt/graf-korpusa` — ПЕРВЫЙ ХОД: рабочая папка, все пути захода — от неё. Ветку НЕ переключай: `zahod/graf-korpusa` в ней уже стоит.
- Проверить, что на месте: `git rev-parse --abbrev-ref HEAD` → должно быть `zahod/graf-korpusa`.
- ПЛАН/ВОПРОСЫ/ОТЧЁТ/УРОКИ ФАБРИКЕ пиши в КОПИЮ этого файла в рабочей папке — `_studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_graf-korpusa.md` — и коммить её в свою ветку вместе с зоной.
- Точка отката: `git add kurs-puti-i-volny/tools/graf.py kurs-puti-i-volny/SBORKA/ZAMER-grafa.md kurs-puti-i-volny/SBORKA/graf-rebra.tsv _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_graf-korpusa.md` → commit (или zip), если зона не чиста в HEAD (не фабрикуй, если чиста).
- Прочитать ТОЛЬКО: `названные файлы-якоря`. Проект не изучай.
- ПЛАН — в `## ПЛАН` перед действиями.

## 1. ДИСЦИПЛИНА (Карпатов)
🔴 **Код возврата — ПЕРВЫМ, до содержательного вывода команды.** «Отработала» и «упала, а я читаю прошлое состояние» выглядят одинаково; сначала `echo $?`, потом выводы. То же с гейтами. (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц7)
Предпосылки/развилки назвать вслух; минимум без спекуляций; хирургия (строка → к заданию); критерий, который может провалиться. Якорные замены — abort при ≠1. Сохранять по умолчанию. **Оспорить ложную предпосылку — включая КРИТЕРИЙ ГОТОВНОСТИ: считаешь его кривым — скажи в `## ПЛАН`, ДО работы, и предложи поправку.** Субагенты: ≤5, рейт-лимит = отступить + доложить (не слепой ретрай).

🔴 **Пишешь содержательный текст — термин НЕ употребляется раньше, чем определён**, включая заголовки, подводки и формулировки теорем. «Определение в тексте есть» не считается: если оно ниже первого рабочего употребления, читатель встаёт ровно там. Чинится ПЕРЕСТАНОВКОЙ определения вверх, не дописыванием пояснения. Гейт: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/check_termin.py <src>` (exit 1 при нарушении). Канон — `../docs/kak-delat/STANDART-teksta.md` правило 11. (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц8)

## 2. ЗАДАЧА

🔴 **WRITE YOUR `## ОТЧЁТ`, `## ПЛАН` AND `## ВОПРОСЫ` IN ENGLISH, AND EVERY FILE AND EVERY COMMIT MESSAGE YOU PRODUCE TOO.** Owner's decision 30.08. It is a каркас-level rule, not a preference (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц9). Fixed Russian addresses stay Cyrillic: `ЦЕНА:` · `ВЕРДИКТ:` · `ДОМ:` · `ДОСТАВЛЕНО:` · `ПОДЪЁМ:` · `[ДОЛГ: …]` · every `## ` heading of this file · every path and command.
### What to build

**One file: `kurs-puti-i-volny/tools/graf.py`**, standard library only, run from the repo root. It answers six questions about the corpus graph and one gate question. It STANDS ON existing code and does not re-implement it:

- **Nodes and links come from `kurs-puti-i-volny/tools/indeks.py`** — import it and call its function `собрать()`, which returns `(файлы, узлы, ссылки, дубли)`: files of the three homes, id-nodes (cards `id: X · род: … · суть: …` and anchors `<!--id: X-->`), links (`[[X]]` and `связи:` fields). Do NOT write a second parser. Do NOT edit `indeks.py` — it is outside your zone.
- **Graph primitives come from `../disciplina/_generator/tools/reserch/topsort_karty.py`** — import `komponenty`, `najti_cikl`, `kan_poryadok` (add its folder to `sys.path`). Do NOT write these again. Read their docstrings only (`grep -n -A6 "^def " <file>`), not the whole file.

**The graph.** Node = a file (id = its path relative to repo root) or an id-node. Edge kinds: `contains` (file → each anchor/card it defines) and `links` (source → target id for every link). 🔴 **The source of a link is the NEAREST PRECEDING anchor `<!--id: …-->` in the same file, or the file itself if no anchor precedes it.** That rule is the whole point for the plans: a section `<!--id: chast-02-->` that contains `[[god-03]]` must give the edge `chast-02 → god-03`. `indeks.py` returns links per FILE only, so graf.py re-reads each file's text once to attribute each link to its enclosing anchor (use `indeks.без_кода` and the regexes `indeks.RE_ЯКОРЬ`, `indeks.RE_ССЫЛКА` — do not copy the regexes).

**The six questions, each a labelled section of the output `[1]`…`[6]`:**
1. **Degrees** — in/out-degree histogram over `links` edges; top-10 nodes by in-degree and by out-degree.
2. **Cascade** — `--kaskad X` prints every node that depends on X transitively (reverse reachability over `links`): «if I rewrite X, what falls downstream». Without the flag, section [2] prints the cascade size for the top-5 in-degree nodes.
3. **Depth** — condense cycles (`najti_cikl`/`komponenty`), then the longest chain over `links`; print its length and the chain itself.
4. **Reachability from the entry point** — entry = `kurs-puti-i-volny/ZAMYSEL.md` (the course's «read first» file). Print reachable/total over `contains`+`links`, and list the unreachable FILES by path.
5. **One graph over the whole corpus** — node and edge counts by kind, number of components, the first cycle if any.
6. **Export** — write every edge to `kurs-puti-i-volny/SBORKA/graf-rebra.tsv` as `source<TAB>target<TAB>kind`, one per line, header line first.

**`[c]` — the plan-linkage gate (clause (c) of the wave mandate).** For every anchor whose id matches `^(god|chast|chetvert|lekciya)-`, print whether it has an outgoing `links` edge to an anchor ONE level up: `chast-* → god-*`, `chetvert-* → chast-*`, `lekciya-* → chetvert-*`. `god-*` is the top and is exempt. Print `plan anchors: N · orphans: K` and the orphans by id. With `--siroty-gate`, exit 1 when K > 0. Today there are no plan anchors yet, so on the live corpus it prints `plan anchors: 0 · orphans: 0` — that is why the gate MUST be proven red on a broken fixture (criterion 3).

**`--koren DIR`** — run over an arbitrary folder instead of the three homes (for fixtures): treat DIR as the only home by overriding `indeks.MATERIALS` and `indeks.ДОМА` for that run. Say in the docstring that this is how it works.

**Default run** (no flags) prints all sections and writes the report to `kurs-puti-i-volny/SBORKA/ZAMER-grafa.md` (with a YAML header carrying `opisanie:`) and the edges to `graf-rebra.tsv`. `SBORKA/` is skipped by `indeks.py` on purpose, so these outputs do not pollute the index. Register the new `.md` in the same move: `python3 ../disciplina/_generator/tools/register_doc.py kurs-puti-i-volny/SBORKA/ZAMER-grafa.md "<one phrase>"`.

**Successor context (your last move).** At the end of `ZAMER-grafa.md` add a section `## For the writing stages` — 5–10 lines, in plain words: which documents are the hubs (highest in-degree), which files are unreachable from `ZAMYSEL.md`, the depth, and anything you learned that is not written in the files. The next positions write the year story and three plans and will read this.

### What NOT to do
- Do not edit `indeks.py`, `dubli.py`, `INDEKS.md`, `topsort_karty.py`, or any corpus document. Zone = the three output paths and this kod file.
- No third-party packages (no networkx). No markdown normalisers.
- Do not read the corpus documents themselves — the tool reads them.

**КРИТЕРИЙ ГОТОВНОСТИ (может ПРОВАЛИТЬСЯ)** — every clause is one command, return code FIRST:
1. **Live run on the real corpus:** `python3 kurs-puti-i-volny/tools/graf.py; echo $?` → `0`, and the output contains all seven labels: `python3 kurs-puti-i-volny/tools/graf.py | grep -cE '^\[(1|2|3|4|5|6|c)\]'` → `7`.
2. **Export covers the links:** `grep -c 'links' kurs-puti-i-volny/SBORKA/graf-rebra.tsv` is not below the `ссылок:` number printed by `cd kurs-puti-i-volny && python3 tools/indeks.py --proverit`.
3. **The gate goes red on a known-broken case (I1: a probe is trusted only after it reds):** make a temporary folder with `mktemp -d`; in it, one markdown file whose only content is an anchor comment (the form described under «The graph» above) with id `chast-01` and no link. Run graf.py on that folder with `--koren` and `--siroty-gate`, then `echo $?` → `1`. Then add a `god-01` anchor on the first line and the link `[[god-01]]` under the chast anchor; the same command → `0`. Paste both outputs verbatim.
4. **Cascade answers:** run `--kaskad` with the id of the top in-degree node that section [1] printed; it lists at least one dependant.
5. `ls -la kurs-puti-i-volny/SBORKA/ZAMER-grafa.md` non-empty and `register_doc.py` on it returned `rc=0`.

**Coverage line in the report:** «questions answered: N of 6, gate [c] proven red on fixture: yes/no».
**Отрицательный вердикт несёт ОХВАТ В СЕБЕ:** не «дыр не найдено», а «дыр не найдено, проверено X из Y». Без охвата вердикт не принимается — «проверено 2 из 9» и «проверено 9 из 9» выглядят одинаково.

## 3. ВЕРИФИКАТОР (если двигаем/теряем/жмём)

Верификатор нужен, тип — **ПОСЛЕ-типа** — судит результат, стоит в конце, после задачи. Свежий субагент, ДРУГИМ методом (fresh subagent runs graf.py itself on two hand-made fixture folders (a 3-node chain and a 2-node cycle) and compares printed depth/cascade/cycle with values it computes by hand; never reads the tool's own tests), не перечитывает свою же правку. Доля сплошной выборки: 2 of 2 fixtures, 6 of 6 questions on each. Финальная строка ответа обязательна дословно: «выдано N позиций из M найденных» — без неё ответ считается усечённым и в отчёт не вставляется.

## 4. 🔴 КОММИТ СВОЕЙ ЗОНЫ — ПО ХОДУ РАБОТЫ, НЕ ОДНИМ ПОСЛЕДНИМ ХОДОМ
Ты работаешь host-side и в `.git` ПИШЕШЬ — значит коммитишь САМ, никому не передавая. Каждую завершённую часть работы коммить СРАЗУ, теми же двумя ходами — не копи всё к финальному ходу:
```
git --no-optional-locks add -- kurs-puti-i-volny/tools/graf.py kurs-puti-i-volny/SBORKA/ZAMER-grafa.md kurs-puti-i-volny/SBORKA/graf-rebra.tsv _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_graf-korpusa.md                     # вводит НОВЫЕ пути в индекс
git --no-optional-locks commit -m "<зона>: <что сделано>" -- kurs-puti-i-volny/tools/graf.py kurs-puti-i-volny/SBORKA/ZAMER-grafa.md kurs-puti-i-volny/SBORKA/graf-rebra.tsv _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_graf-korpusa.md   # отсекает всё чужое
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

**ЗОНА ГИГИЕНЫ:** `kurs-puti-i-volny/tools/graf.py` `kurs-puti-i-volny/SBORKA/ZAMER-grafa.md` `kurs-puti-i-volny/SBORKA/graf-rebra.tsv` `_studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_graf-korpusa.md`

- **Г1. Зона доехала в git.** `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone kurs-puti-i-volny/tools/graf.py` → ✅; `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone kurs-puti-i-volny/SBORKA/ZAMER-grafa.md` → ✅; `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone kurs-puti-i-volny/SBORKA/graf-rebra.tsv` → ✅; `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_graf-korpusa.md` → ✅. Красное на любой из команд — отчёт не принимается: приёмка гоняет их все первым ходом.
- **Г2. Второй репозиторий.** **неприменимо, и это проверено при сборке, а не предположено:** все пути зоны лежат внутри репозитория `materials` (тот же критерий, что у С2 `check_sborki.py`). Зона расширилась за его пределы по ходу — пункт снова применим; команда та же, что в применимом случае: `cd ../<репозиторий> && git --no-optional-locks status --porcelain` → пусто. *Команда названа и здесь нарочно (находка верификатора): пункт, который объявлен неприменимым и не говорит, ЧТО делать, когда станет применим, исполнить в этот момент нечем.*
- **Г3. Невлитых веток не прибавилось.** `git --no-optional-locks branch --no-merged arka/mat-kostyak` — число сравни с тем, что было на входе. Выросло — назови, чьи ветки и почему они законны.
- **Г4. Новый инструмент имеет живую точку вызова.** Завёл `.py` в `_generator/**` — `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/check_tool_contract.py <свои новые файлы>` → rc=0. Ни одного нового `.py` — так и напиши. *Инструмент без точки вызова зелен ровно потому, что его никто не звал.*
- **Г5. Новый `.md` зарегистрирован.** Завёл — звал ли ты `register_doc.py` и лежит ли строка на диске: `grep -c '<имя файла>' <карта своего корня>` → 1. Карту своего корня называет `korni.карта_для('<путь>')`, руками её не угадывай.
- **Г6. В коммите нет чужих путей.** `git --no-optional-locks show --stat` — только твои пути. Чужой путь в своём коммите — это чужая работа, унесённая твоим `commit` без `--`.

## 5. ОТЧЁТ → секция `## ОТЧЁТ` внизу
Что сделал + ЗАЧЕМ / как проверил / что НЕ трогал / вопросы / результат верификатора / открытое «возвращаться» / **время прогона + токены — НЕПРИМЕНИМО: движок `opencode`, счётчика стоимости в логе нет** (лог `.log` — обычный текст без `result`-строки, число снимать неоткуда; строку не заполнять числом и не извиняться за его отсутствие) / **ПОВТОРЯЕМОСТЬ находок (строка обязательна — см. ниже)** / **АРТЕФАКТ (строка обязательна)** / **КОММИТ (строка обязательна, см. §4)**.

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
python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py vlit-v-osnovnuyu zahod/graf-korpusa --zone <своя зона> \
    --vsyo-ravno "своя рабочая папка ещё жива — влитие последним ходом захода, штатно"
```
Конфликт — ЗАКОННЫЙ исход, не повод форсировать: разрешай по существу, если понимаешь обе
стороны; не понимаешь — `git_zona.py vlit-v-osnovnuyu --abort`, ветка остаётся невлитой,
строка в отчёт и заявка на влитие (`git_zona.py zayavka --rod git-operaciya`).
🔴 Конфликт на `README.md` — только ОБЪЕДИНЕНИЕМ записей реестра, никогда выбором стороны:
параллельные заходы волны дописали по строке — обе записи правы, выбор одной молча уничтожает
регистрацию соседа.

**3 · ПОСТ-ПРОВЕРКА ИЗ ГЛАВНОЙ ПАПКИ.** Отвечает на вопрос «механизм ВСТАЛ», а не «коммит
виден»: прогон изменённого механизма из основной папки `../../materials` (путь от корня рабочей папки), НЕ из рабочей папки `/Users/ivanyakovlev/Documents/GitHub/materials-wt/graf-korpusa` плюс `grep` по ЖИВОМУ файлу,
который его зовёт (хук, конвейер, генератор):
```
cd ../../materials && <команда прогона механизма, который заход менял> && echo $?
grep -n '<как механизм назван в вызывающем коде>' <живая точка вызова>
```
🔴 **Красная пост-проверка = ОТКАТ ВЛИТИЯ И СТРОКА В ОТЧЁТ**, а не «доложу, пусть приёмка
решает»: `git_zona.py vlit-v-osnovnuyu --abort`, если слияние ещё не закоммичено, иначе
`git -C ../../materials --no-optional-locks reset --hard <хэш ДО влития>`. Заход, который влил
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
<сюда — вывод, дословно>

**ЧТО СДЕЛАНО** *(с хэшами)*
<влито / закоммичено / вывезено / погашено / заявки закрыты — поимённо>

**ВСЕ ДОЛГИ ВХОДА ЗАКРЫТЫ:** `<да | нет>`
*(`нет` законно — но ТОЛЬКО со списком поимённо: что осталось и почему это непроходимо ТВОИМИ
правами (чужая живая рабочая папка, нужно решение владельца, конфликт, обеих сторон которого
не понимаешь). «Сложно» и «не моя тема» причинами не являются. `нет` без списка = красный.)*

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

**ВЕТКА РАБОТЫ:** `zahod/graf-korpusa`
*(проверяется фактом, не словом: ветка обязана существовать и быть либо ВЛИТА в основную, либо названа в открытой заявке на влитие. Ни того, ни другого — Г14 краснеет. Снять состояние: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py poteri --branch <ветка>`)*

**ЗАЯВКИ, ПОСТАВЛЕННЫЕ ЭТОЙ ПРИЁМКОЙ — ПРОДУБЛИРУЙ СЮДА ТО, ЧТО УЖЕ ЛЕЖИТ В СПИСКЕ:**
> Адрес списка: `_studio/zhurnal/_INFRA-git/zayavki`
> Читается командой (из любой папки, в том числе из worktree): `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py zayavki`
> Ставится командой: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py zayavka --rod <git-operaciya|pravka-koda> "<текст>"`
> 🔴 Вопрос здесь НЕ «что ты хочешь сделать», а «что ты УЖЕ положил в очередь». Дубль сверяется с очередью по id машинно; намерение сверить не с чем.

- `<id заявки>` — `<род>` — `<суть одной строкой: влитие / коммит / вывоз / деплой / гашение>`

*(Заявок эта приёмка не ставила — так и напиши строкой «заявок нет: <почему ни одна из пяти операций не понадобилась>». Пустая строка и прочерк не принимаются: молчание неотличимо от «забыл».)*
