# Канал исполнителя — chistka-github (один заход до конца)
> Твой единственный файл-заход. Читай ТОЛЬКО его и названные якоря; проект не изучай.
<!-- собран bootstrap_zahod.py -->
<!-- гейт сборки заполненного: КЛАПАН 2026-09-25 -->
> 🔴 ГЕЙТ СБОРКИ ЗАПОЛНЕННОГО ФАЙЛА ОТКРЫТ КЛАПАНОМ (2026-09-25): `check_sborki.py` вернул rc=1 на заполненном файле, заход выдан вопреки красному, причина дословно: «межмашинный заход: собран в облаке, исполняется на Mac; С3 краснеет только на путях /Users/ivanyakovlev/..., которых нет на машине сборки; п.99, п.112 SPISOK-DEL». Отключение видно здесь, в артефакте, а не осталось решением в голове аналитика.
> План/вопросы/отчёт — в секции внизу. Метрика — КАЧЕСТВО. Часы — норма.
> **Модель: Opus 5** — на каждой невлитой удалённой ветке суждение 'влита / в метку и удалить / оставить'; удаление на GitHub видно всем.

## СТАРТОВОЕ СООБЩЕНИЕ ВЛАДЕЛЬЦУ

> Это блок для владельца — то, чем тебя запустили. Исполнителю здесь делать нечего, твоё задание ниже.

```
Модель: Opus 5.

Ты исполнитель на Mac владельца. Владелец недоступен; полные права по правилам захода; репозиторий vanya не трогать. Открой Claude Code в папке ~/Documents/GitHub/materials и сделай три хода:

1. git --no-optional-locks fetch origin claude/bold-faraday-wq09ql
2. git --no-optional-locks worktree add ../materials-wt/chistka-github -b zahod/chistka-github origin/claude/bold-faraday-wq09ql
   (папка или ветка уже есть — не пересоздавай, просто перейди в неё)
3. cd ../materials-wt/chistka-github и прочитай ЦЕЛИКОМ файл-заход:
   _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/kod_chistka-github.md

Работай строго по нему, проект сам не изучай. Вопросов владельцу не задавай: неясное — пропусти, запиши в chistka-github/VOPROSY.md, иди дальше.
Пушь после каждого шага; с аналитиком — канал из §2.1 захода.
```

── СЧЁТ НЕЗАКРЫТОГО (печать, не гейт) ──
ГРАНИЦА ОБЛАСТИ: сырые подстроки в `kod_*.md` (пункт 4) — НЕ парсер очереди `dostavit_urok` (который считает только пары ДОМ:/ДОСТАВЛЕНО:). Разница в числах — законна.
🔴 снимок при сборке 2026-09-25, ПРОВЕРЬ ПЕРВЫМ ХОДОМ: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/schet_nezakrytogo.py _studio/zhurnal/2026-09-24_arhitektura-repozitoriev`
Область: «_studio/zhurnal/2026-09-24_arhitektura-repozitoriev» — сужены пункты 1, 3, 4; долги (2) глобальны намеренно (DOLG.md не размечен по записям).
Приоритет владельца: разобрать инциденты важнее, потом закрыть долги — неразобранный инцидент это повторяющаяся ошибка, долг может подождать.
  1. инцидентов без вердикта             : 0
  2. долгов СТАТУС: ЖИВ                  : н/д — ни одного skills/*/DOLG.md нет на диске (другой git-репозиторий)
  3. уроков фабрике без ВЕРДИКТ          : 0
  4. пунктов очереди «ДОСТАВЛЕНО: нет»   : 19
     из них разбором очереди (парсер `dostavit_urok`, записи с парой ДОМ:/ДОСТАВЛЕНО:): 10
       живых (чинится доставкой — «дом есть»)  : 4
       к владельцу (решение за человеком)      : 6
       адрес недоступен (нет/папка/код/указат.) : 0
       адрес не разобран                        : 0
       отработавших (машинный след закрытия)    : 0
       доставлено                               : 0
       🔴 не проверяется машиной: содержательная отработанность записей БЕЗ следа закрытия (метки в доме, строки ✅/ЗАКРЫТО) — нужна ревизия человеком; сырой греп сверх разбора — шаблонные строки формы.

КОНТЕКСТ. <проект в 1–2 фразы>. Прошлый этап: <состояние>. ЦЕЛЬ: <что закрыть>.
Приёмка — по ОТЧЁТУ, без построчной сверки. <Если стоп до цели: получишь X, но НЕ Y.>

## ЧТО ФИНАЛИЗИРОВАНО НА ИНТЕРВЬЮ

ИНТЕРВЬЮ ПРОВЕДЕНО: да (2026-09-25) — флаг `--intervyu da` при сборке. ⚠ Он доказывает, что аналитик не ЗАБЫЛ про интервью, и НЕ доказывает, что разговор был.

1. Владелец явно разрешил удалять ветки на GitHub: влитые — удалить; парковки и закрываемые невлитые — сперва метка arhiv/, потом удалить; 46 парковок — единственная копия, только через метку
2. Остаются: ствол каждого репозитория, main-сайт materials, ветка аналитика claude/bold-faraday-wq09ql, ветки Pages, matemdigest rabota и stil-noch; sayt tagging влить в main

## КОНТРАКТ ЗОНЫ (обязателен — не удалять; вписан Cowork)
- **МЕСТО РАБОТЫ:** **рабочая папка `/Users/ivanyakovlev/Documents/GitHub/materials-wt/chistka-github`** — МЕСТО ВСЕЙ РАБОТЫ (worktree захода, ветка `zahod/chistka-github` в ней уже стоит). 🔴 **ПЕРВЫЙ ХОД — `cd /Users/ivanyakovlev/Documents/GitHub/materials-wt/chistka-github`; ДАЛЬШЕ — ТОЛЬКО ПУТИ ОТНОСИТЕЛЬНО ЭТОЙ ПАПКИ** (или `cd` в неё безусловно, каждым ходом): `python3 _generator/tools/…` зовёт копию инструмента в ней же, пути зоны и арки — её файлы. Абсолютный путь в главную папку репозитория здесь — типичная ошибка, правка утекает МИМО worktree и найдётся только на коммите («вне git» в `git_zona.py check --zone` из рабочей папки, на файле, который уже правил, — цена, оплаченная живьём: 5 файлов, ручное копирование и откат главной папки). 🔴 `git checkout` в основной папке ЗАПРЕЩЁН: рядом идут другие заходы, переключение подменит файлы у них под ногами. 🔴 **Файл-заход — КОПИЯ `_studio/zhurnal/2026-09-24_arhitektura-repozitoriev/kod_chistka-github.md` в твоей рабочей папке**: ПЛАН/ВОПРОСЫ/ОТЧЁТ/УРОКИ пишешь в неё и коммитишь её в свою ветку вместе с зоной (путь копии в зоне уже есть). Копии в папке нет — перенеси её из основной ветки: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py adopt --branch claude/bold-faraday-wq09ql --zone _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/kod_chistka-github.md --yes` (дирижёр волны кладёт её сам при старте). Существующую копию не затирай: в ней твоя работа. Отчёт читают в ней: дирижёр — сразу, приёмка — после влития ветки. При влитии копия может дать конфликт add/add с файлом-заходом основной ветки (ветка заведена раньше, чем заход попал в git) — это законно и разрешается объединением: план, вопросы и отчёт — из копии, правки после выдачи — из основного файла. 🔴 **Ветку в конце вливаешь САМ, последним ходом, после коммита зоны** (решение владельца 25.08; полный порядок печатает WARNING-блок ниже).
- **ЗОНА (можно менять):** `_studio/zhurnal/2026-09-24_arhitektura-repozitoriev/chistka-github/` `_studio/zhurnal/2026-09-24_arhitektura-repozitoriev/kod_chistka-github.md`. Всё вне — **READ-ONLY**: не править, не двигать, не удалять, не рефакторить «заодно».
- 🔴 **ЗАВЁЛ НОВЫЙ `.md` — РЕГИСТРИРУЕШЬ ЕГО САМ, ТЕМ ЖЕ ХОДОМ, ОДНОЙ КОМАНДОЙ:** `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/register_doc.py <путь> "<описание>"` (из корня репо). `_studio/docs/` тебе по-прежнему READ-ONLY **для правки руками** — дверь ровно одна, и это она. Дверь идемпотентна (повторный вызов дубля не заведёт) и отказывает на пути вне `_studio/`, на несуществующем файле и на пустом описании. Свой файл-заход регистрировать не нужно: он рождается зарегистрированным из `bootstrap_zahod.py`. **Красный хук на ТВОЁМ новом `.md` — это не повод для `--no-verify`, а повод позвать дверь.** *(история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц1) Обходить больше нечего.*
- **КОММИТ:** два хода — `add` по своим путям, затем `commit` **с теми же путями после `--`** (полная форма и цена каждого хода — §4); коммить ПО ХОДУ работы, не одним последним ходом (§4). НИКОГДА `-A` / `.` / `commit -am`, и никогда `commit` без путей. Субагенты не коммитят. **`--no-optional-locks` обязателен:** обычный git переписывает индекс, берёт `.git/index.lock` и роняет параллельный ручной коммит владельца.
- **SCRATCHPAD — ТОЛЬКО ЛИЧНЫЙ.** Черновики, выкладки, промежуточные версии — в личную папку СВОЕГО захода `scratchpad/chistka-github/`. Общие пути (`scratchpad/otchet.md`, любой `scratchpad/*` без имени твоей темы) ЗАПРЕЩЕНЫ: чужой отчёт уедет в твой файл или твой — в чужой, а приёмка читает отчёт без построчной сверки и подмену НЕ ЛОВИТ по построению. (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц2)
- 🔴 **Звал `register_doc.py` — допиши `_studio/docs/KARTA.md` к своим путям В ОБОИХ ходах.** Строка регистрации лежит физически в нём. Ворота 5 читают `§6` **с диска**, а не из индекса: коммит без этого файла пройдёт ЗЕЛЁНЫМ, документ уедет сиротой, а строка умрёт при первом `checkout` (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц3).
- **ЗАПРЕТ:** ничего за пределами зоны, даже если «мешает» или «чинится в одну строку». Нашёл проблему вне зоны → в отчёт, не трогай.

## 0. ПЕРВЫЙ ХОД
### 0.1 🔴 ГИТ-КОНТУР — ДО ВСЕГО ОСТАЛЬНОГО, И ПЕРВЫМ ХОДОМ ЦЕЛИКОМ

🔴 «ничего сверх задачи» относится к СОДЕРЖАНИЮ работы; git-контур §0.1 — законное исключение, он про состояние репозитория и исполняется целиком.

🔴 **ПОРЯДОК ЗДЕСЬ — ЧАСТЬ УСТРОЙСТВА, А НЕ ОФОРМЛЕНИЕ. Сначала САМ прогоняешь две команды самопроверки контура (пункт 1 ниже), и только ПОТОМ заводишь свою рабочую папку** — её ветка отпочковывается от основной такой, какая она есть на момент запуска: контур пуст, доносить инструмент влитием нечего.

🔴 Очередь заявок подметена на входе волны, твоё дело здесь — только своя зона: закрывает и вливает очередь роль коммитера (`agents/kommiter.md`), один раз на входе волны и один раз на выходе (`python3 _generator/tools/bootstrap_zahod.py --podmetanie-volny vhod|vyhod`), не сборка этой позиции.

**1. ВЕСЬ КОНТУР ПУСТ — САМОПРОВЕРКА ВМЕСТО СУБАГЕНТА.** При сборке проверены два числа ПОЗИЦИОННОГО контура, и оба нулевые: невлитых `zahod/*`-веток 0 (🔴 снимок при сборке 2026-09-25, ПРОВЕРЬ ПЕРВЫМ ХОДОМ: `git --no-optional-locks branch --no-merged claude/bold-faraday-wq09ql | grep -c 'zahod/'`); названных `--vlit` 0. Звать субагента не за чем — выполни САМ две команды и вставь их вывод в `## ОТЧЁТ` дословно:
```
git --no-optional-locks branch --no-merged claude/bold-faraday-wq09ql | grep -c 'zahod/'   # снимок при сборке 2026-09-25: 0
python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/chistka-github/
```
Первая вернула не 0 — НИЧЕГО чужого не вливай (свою ветку вольёшь последним ходом, см. ниже), назови число строкой в `## ОТЧЁТ` и работай дальше. Вторая красная — сначала приведи в порядок свою зону.

Если при следующей сборке невлитых веток или названных `--vlit` окажется хоть одна, генератор сам вернёт сюда задание субагенту гит-контура — печатает его дверь `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/bootstrap_zahod.py --zadanie-subagentu`; звать его в этом заходе не надо.

🔴 ОТВЕТ ЛЮБОГО субагента, которого ты запускаешь (не только этого), обязан КОНЧАТЬСЯ строкой «выдано N позиций из M найденных»: канал мог оборвать его молча, и без этой строки усечение неотличимо от честного «мало нашлось». Нет строки — ответ усечён, в `## ОТЧЁТ` не вставляй, перезапроси.

**2. ТЕПЕРЬ ЗАВОДИ СВОЮ РАБОЧУЮ ПАПКУ** (команда — в блоке «МЕСТО РАБОТЫ» выше) и работай в ней как обычно. Её ветка отпочкована от свежей основной, поэтому инструмент, которым ты работаешь, уже на диске — отдельного «влить перед работой» больше нет.

вливать нечего, проверено командой `git branch --no-merged` — но проверено ПРИ СБОРКЕ, а не сейчас: невлитых `zahod/*`-веток было 0. 🔴 снимок при сборке 2026-09-25, ПРОВЕРЬ ПЕРВЫМ ХОДОМ: `git --no-optional-locks branch --no-merged claude/bold-faraday-wq09ql | grep -c 'zahod/'`. Число могло устареть между сборкой и твоим прогоном — 14.08 заход нёс ровно этот ноль, а к прогону невлитых было три.


- деплоя в этом заходе нет.

- `cd /Users/ivanyakovlev/Documents/GitHub/materials-wt/chistka-github` — ПЕРВЫЙ ХОД: рабочая папка, все пути захода — от неё. Ветку НЕ переключай: `zahod/chistka-github` в ней уже стоит.
- Проверить, что на месте: `git rev-parse --abbrev-ref HEAD` → должно быть `zahod/chistka-github`.
- ПЛАН/ВОПРОСЫ/ОТЧЁТ/УРОКИ ФАБРИКЕ пиши в КОПИЮ этого файла в рабочей папке — `_studio/zhurnal/2026-09-24_arhitektura-repozitoriev/kod_chistka-github.md` — и коммить её в свою ветку вместе с зоной.
- Точка отката: `git add _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/chistka-github/ _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/kod_chistka-github.md` → commit (или zip), если зона не чиста в HEAD (не фабрикуй, если чиста).
- Прочитать ТОЛЬКО: `названные файлы-якоря`. Проект не изучай.
- ПЛАН — в `## ПЛАН` перед действиями.

## 1. ДИСЦИПЛИНА (Карпатов)
🔴 **Развилку ВНУТРИ своей зоны решаешь сам** — называешь решение в `## ПЛАН` и идёшь дальше; спрашивать и ЖДАТЬ ответа владельца — только там, где любой выбор делает работу опасной или бессмысленной. Целый прогон уже вставал на вопросе, ответ на который лежал в собственном контракте зоны исполнителя (урок арки `2026-08-20_poryadok-v-metaskillah`).
🔴 **Не собирай `rm` с путём из переменных.** Защитный слой перехватывает такие команды НЕЗАВИСИМО от Bypass permissions и останавливает работу до ответа человека — замер 20.09: 5 ч 48 мин при работающей машине. Вместо `cp X Y && rm X` пиши `mv X Y`; где не подходит — питон-скрипт ФАЙЛОМ, не однострочник с `rm`.
🔴 **Код возврата — ПЕРВЫМ, до содержательного вывода команды.** «Отработала» и «упала, а я читаю прошлое состояние» выглядят одинаково; сначала `echo $?`, потом выводы. То же с гейтами. (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц7)
Предпосылки/развилки назвать вслух; минимум без спекуляций; хирургия (строка → к заданию); критерий, который может провалиться. Якорные замены — abort при ≠1. Сохранять по умолчанию. **Оспорить ложную предпосылку — включая КРИТЕРИЙ ГОТОВНОСТИ: считаешь его кривым — скажи в `## ПЛАН`, ДО работы, и предложи поправку.** Субагенты: ≤5, рейт-лимит = отступить + доложить (не слепой ретрай).

🔴 **Пишешь содержательный текст — термин НЕ употребляется раньше, чем определён**, включая заголовки, подводки и формулировки теорем. «Определение в тексте есть» не считается: если оно ниже первого рабочего употребления, читатель встаёт ровно там. Чинится ПЕРЕСТАНОВКОЙ определения вверх, не дописыванием пояснения. Гейт: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/check_termin.py <src>` (exit 1 при нарушении). Канон — `../docs/kak-delat/STANDART-teksta.md` правило 11. (история цены — `/Users/ivanyakovlev/Documents/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц8)

## 2. ЗАДАЧА

🔴 **WRITE YOUR `## ОТЧЁТ`, `## ПЛАН` AND `## ВОПРОСЫ` IN ENGLISH, AND EVERY FILE AND EVERY COMMIT MESSAGE YOU PRODUCE TOO.** Fixed Russian addresses stay Cyrillic: `ЦЕНА:` · `ВЕРДИКТ:` · `ДОМ:` · `ДОСТАВЛЕНО:` · `ПОДЪЁМ:` · `[ДОЛГ: …]` · every `## ` heading of this file · every path and command.

### 2.0 Context — the last pass of arc A

Three passes were accepted: the census, the overnight cleanup (`uborka-materials/`) and the integration (`svedenie/`). The disk and GitHub now hold one version; the uncommitted work is committed; small unmerged edits are merged; the default branch of `materials` is `arka/mat-kostyak`. **What is left is clutter on GitHub itself**, counted by the previous pass (`svedenie/REPORT.md` point 7): branches already merged into their trunk (disciplina 456, spetsmat-bot 100, materials 60, others about 14), and about 209 park branches `park/2026-09-25/*`. **46 of those park branches are the ONLY copy of edits from worktrees that were removed** (`svedenie/VOPROSY.md` question 17), so they must be kept as tags. Re-measure everything live.

**The owner explicitly allowed deleting branches on GitHub (2026-09-25)**, under one law: **no work may be lost**. So every branch you delete must satisfy, checked by command right before the deletion: *its tip commit is reachable on GitHub either from the trunk or from a tag `arhiv/…` that you pushed and verified.*

**Nothing else runs on this Mac**, except that a parallel owner session may be working in `vanya` (it started new work there on 25.09). **Do not touch `vanya` at all in this pass.**

Mechanics by scripts in `/tmp/chistka/`, not by models; Opus judgement only for unmerged branches. Keep your context under about 150k tokens; at the limit — `STOPPED: budget …`, push, stop.

### 2.1 Channel with the analyst — same as before

The log is `chistka-github/DNEVNIK-chistka-github.md`, in the entry form `## <date '+%Y-%m-%d %H:%M'> — <step>`, with **done** · **next** · **surprise** · **question**. Commit and push after every entry (`git --no-optional-locks push -u origin zahod/chistka-github`). Pulse if you go 45 minutes without a push.

When you want the analyst's input, write `QUESTION-FOR-ANALYST: … DEFAULT: …` and carry on with the default. Keep a background watcher on `origin/claude/bold-faraday-wq09ql` (the command is in `kod_svedenie.md` §2.1; the corrections section is in THIS file). The last entry starts `FINAL:` or `STOPPED:`.

`chistka-github/actions.tsv` holds one row per branch: `time · repo · branch · class · action (delete | tag+delete | keep | merge | skip) · tag · tip · verified · restore (the command to recreate the branch: git push origin <tip>:refs/heads/<branch>) · note`.

### 2.2 Steps

**Step 1 — measure.** For each repository on GitHub that has more than one branch (`materials`, `disciplina`, `spetsmat-179` (the local folder is `spetsmat-bot`), `matproekty-179`, `matproekty-179-stranica`, `ankety`, `moskva`, `matema-fest`, `digest` (the local folder is `matemdigest-map`), `arhiv-london-avgust-2026`, `sayt-sistemy-konstantinova`), take the local main checkout and run `git fetch --prune --tags origin`. Then write `chistka-github/before.tsv`, one row per repo: `repo · remote_branches (git ls-remote --heads origin | wc -l) · trunk`. The trunk is the default branch (`git ls-remote --symref origin HEAD`); for `materials` it is `arka/mat-kostyak`.

**Step 2 — classify every remote branch** into exactly one class:
- `keep-trunk`: the default branch.
- `keep-named`, which never gets deleted:
  - `materials`: `main` (the published site) and `claude/bold-faraday-wq09ql` (the analyst's working branch);
  - `arhiv-london-avgust-2026`: `pages`;
  - `digest`: `rabota` and `zahod/stil-noch` (owner: two independent lines, site and workspace; they stay until the repository is split);
  - any branch named `gh-pages`.
- `merged`: `git merge-base --is-ancestor origin/<b> origin/<trunk>`.
- `park`: the name starts with `park/`.
- `unmerged`: everything else.

**Step 3 — `sayt-sistemy-konstantinova`: merge `tagging` into `main`** (owner, 25.09: yes). The merge is clean, per the previous pass. In its main checkout, check out `main`, then run `git merge --no-ff tagging -m "влита ветка tagging (решение владельца 25.09)"`, then `git push origin main`. A conflict means `git merge --abort`, and you write a question. After the merge, `tagging` falls into class `merged`.

**Step 4 — tags first.** For every `park` branch and every `unmerged` branch you decide to close (step 6): `git tag arhiv/<branch name> origin/<branch>`, then `git push origin refs/tags/arhiv/<branch name>`, then verify with `git ls-remote --tags origin arhiv/<branch name>` that the tag points to the tip. Do this as batch scripts per repository.

**Step 5 — delete.** Delete `merged` branches, and `park` branches whose tag is verified: `git push origin --delete <branch>`. Do it in batches of up to 50 per repository. After each batch, the verifier (step 7) runs before the next batch.

**Step 6 — `unmerged` branches: judge each one.** Read the commit messages (`git log --oneline origin/<trunk>..origin/<b>`), the diff stat, and the brief if one exists. The questions of `svedenie/VOPROSY.md` already carry the owner-accepted proposals for several of them:
- CLOSE (tag + delete): disciplina `zahod/git-bez-zamkov` and its park (q3), `zahod/git-zona-zona-shire-kontrakta` (q8), `zahod/snimok-nazyvaet-avtora` (q9); spetsmat `zahod/B1-v14-vid` (q13).
- The owner stopped these unfinished, so CLOSE them the same way, since the tag keeps the work: disciplina `zahod/byudzhety-i-rashod` (q5), `zahod/roli-i-dver-brifa` (q6), `zahod/dobor-s-mesta` (q7).
- For every other `unmerged` branch:
  - it is old (last commit more than 7 days ago), and its work is superseded or abandoned per its messages → tag + delete;
  - it is recent, or you cannot tell → `keep`, with one line in `chistka-github/VOPROSY.md` giving what it is and a proposal.

  Small finished edits that merge clean may be merged through the door `git_zona.py vlit-v-osnovnuyu`, as in the previous pass. In `materials`, merge with `git_zona.py merge` into `arka/mat-kostyak`, because the door there mistakes `main` for the trunk.

**Step 7 — verifier (a separate subagent) after each batch.** Its mandate is wider than yours. For every `delete` / `tag+delete` row, it checks that the `tip` is reachable on GitHub from `origin/<trunk>` or from the recorded tag (fetch, then `git merge-base --is-ancestor` or `git rev-parse arhiv/<name>`). It writes `chistka-github/verifier.md`, which ends with "checked N of M, K failures". If K > 0: stop deleting, and recreate the missing branch with the `restore` command.

**Step 8 — local leftovers, cheap.**
- Local branches that are fully merged into their trunk: `git branch -d <b>`. The `-d` refuses unmerged ones, so this is safe; it covers the 40 refused by `zakryt-vetku`, svedenie q2.
- The two container folders `disciplina-wt/` and `matproekty-179-wt/` → `mv` to `~/.Trash/`. Their worktrees are all gone; svedenie q15.
- The worktree `/private/tmp/baseline-759ef40` of spetsmat-bot → first check that its HEAD is reachable on GitHub, then `git worktree remove --force`.
- `disciplina/--help/` → `~/.Trash/`. It is a test artifact, svedenie q1; check first that it holds no tracked file.

**Step 9 — report.** `chistka-github/REPORT.md` opens with **"GITHUB AFTER THE CLEANUP"**, at most 15 lines in plain words:
- per repository, branches before → after, and which branches remain, with one reason each;
- how many `arhiv/*` tags were created, and how to find them (`git tag -l 'arhiv/*'`);
- what was merged;
- what is left for later.

Finally, merge your own branch into `arka/mat-kostyak` with `git_zona.py merge` (not `vlit-v-osnovnuyu`, because of the `main` trap), and push.

### 2.3 Forbidden — each line names its enemy

- deleting any branch whose tip is not verified reachable from the trunk or from a pushed `arhiv/` tag — **enemy: the only real loss possible in this pass**;
- deleting or moving any TAG, `--force` push, `reset --hard` on a trunk, rebasing anything pushed — **enemy: rewriting the recovery itself**;
- touching the `keep-named` branches, or the repository `vanya` — **enemy: breaking the site, the analyst's channel, or the owner's live work**;
- content edits — **enemy: a cleanup that rewrites work**.

**КРИТЕРИЙ ГОТОВНОСТИ (может ПРОВАЛИТЬСЯ):**
The whole criterion is a живой прогон на реальном объекте: GitHub itself, with no fixture.
1. `chistka-github/` holds `DNEVNIK-chistka-github.md`, `before.tsv`, `actions.tsv`, `VOPROSY.md`, `verifier.md` and `REPORT.md` (`ls _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/chistka-github/ | wc -l` → 6 or more).
2. **Coverage**: every remote branch counted in `before.tsv` has exactly one row in `actions.tsv` ("checked X of Y", X = the sum of `remote_branches`).
3. **Zero loss**: `verifier.md` ends with K = 0.
4. **Result**: for each repository, `git ls-remote --heads origin | wc -l` after the pass equals `keep-trunk + keep-named + keep` rows for it (printed in `REPORT.md`).
5. **Tags**: `git ls-remote --tags origin 'arhiv/*' | wc -l` equals the number of `tag+delete` rows plus park tags, per repository.
6. `sayt-sistemy-konstantinova`: `git merge-base --is-ancestor <old tagging tip> origin/main` holds, or a question explains why not.
7. `origin/arka/mat-kostyak` contains `zahod/chistka-github`.

**Отрицательный вердикт несёт ОХВАТ В СЕБЕ:** не «дыр не найдено», а «дыр не найдено, проверено X из Y». Без охвата вердикт не принимается — «проверено 2 из 9» и «проверено 9 из 9» выглядят одинаково.

### 2.4 Delivery

The WARNING block below applies, except that its step 2 ("влитие") is the merge into `arka/mat-kostyak` from step 9, done with `git_zona.py merge`. Base comparisons use `origin/claude/bold-faraday-wq09ql`. Do not drop your own worktree.

## 3. ВЕРИФИКАТОР (если двигаем/теряем/жмём)

Верификатор нужен, тип — **ПОСЛЕ-типа** — судит результат, стоит в конце, после задачи. Свежий субагент, ДРУГИМ методом (отдельный субагент после каждой пачки: кончик каждой удалённой ветки достижим на GitHub из ствола или из метки arhiv/), не перечитывает свою же правку. Доля сплошной выборки: все 100% удалённого. Финальная строка ответа обязательна дословно: «выдано N позиций из M найденных» — без неё ответ считается усечённым и в отчёт не вставляется.

## 4. 🔴 КОММИТ СВОЕЙ ЗОНЫ — ПО ХОДУ РАБОТЫ, НЕ ОДНИМ ПОСЛЕДНИМ ХОДОМ
Ты работаешь host-side и в `.git` ПИШЕШЬ — значит коммитишь САМ, никому не передавая. Каждую завершённую часть работы коммить СРАЗУ, теми же двумя ходами — не копи всё к финальному ходу:
```
git --no-optional-locks add -- _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/chistka-github/ _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/kod_chistka-github.md                     # вводит НОВЫЕ пути в индекс
git --no-optional-locks commit -m "<зона>: <что сделано>" -- _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/chistka-github/ _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/kod_chistka-github.md   # отсекает всё чужое
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

**ЗОНА ГИГИЕНЫ:** `_studio/zhurnal/2026-09-24_arhitektura-repozitoriev/chistka-github/` `_studio/zhurnal/2026-09-24_arhitektura-repozitoriev/kod_chistka-github.md`

- **Г1. Зона доехала в git.** `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/chistka-github/` → ✅; `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone _studio/zhurnal/2026-09-24_arhitektura-repozitoriev/kod_chistka-github.md` → ✅. Красное на любой из команд — отчёт не принимается: приёмка гоняет их все первым ходом.
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
python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py vlit-v-osnovnuyu zahod/chistka-github --zone <своя зона> \
    --vsyo-ravno "своя рабочая папка ещё жива — влитие последним ходом захода, штатно"
```
Конфликт — ЗАКОННЫЙ исход, не повод форсировать: разрешай по существу, если понимаешь обе
стороны; не понимаешь — `git_zona.py vlit-v-osnovnuyu --abort`, ветка остаётся невлитой,
строка в отчёт и заявка на влитие (`git_zona.py zayavka --rod git-operaciya`).
🔴 Конфликт на `README.md` — только ОБЪЕДИНЕНИЕМ записей реестра, никогда выбором стороны:
параллельные заходы волны дописали по строке — обе записи правы, выбор одной молча уничтожает
регистрацию соседа.

**3 · ПОСТ-ПРОВЕРКА ИЗ ГЛАВНОЙ ПАПКИ.** Отвечает на вопрос «механизм ВСТАЛ», а не «коммит
виден»: прогон изменённого механизма из основной папки `../../materials` (путь от корня рабочей папки), НЕ из рабочей папки `/Users/ivanyakovlev/Documents/GitHub/materials-wt/chistka-github` плюс `grep` по ЖИВОМУ файлу,
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

Executor: Claude Code (Opus 5.5), channel `app`, started 2026-09-25.

**Premises checked before work (named aloud):**
- P1. The §0.1 self-check command `git branch --no-merged claude/bold-faraday-wq09ql` is broken as written in this worktree: there is no local branch of that name, git prints `fatal: malformed object name` and `grep -c` prints a false `0`. Per §2.4 ("base comparisons use `origin/claude/bold-faraday-wq09ql`") I run every base comparison against `origin/claude/bold-faraday-wq09ql`. Both outputs go to `## ОТЧЁТ`.
- P2. `## ГИГИЕНА ВХОДА` says it is filled by the git-contour subagent, but §0.1 says no subagent is needed (contour empty). I fill the entry snapshot myself with command output; recorded in `chistka-github/VOPROSY.md`.
- P3. The brief copy already exists in the worktree (it came with `origin/claude/bold-faraday-wq09ql`), so no `adopt` is needed.

**Decisions inside my remit:**
- D1. Class precedence when a branch fits two classes: `keep-trunk` > `keep-named` > `merged` > `park` > `unmerged` (the order the brief lists them). A `park/*` branch whose tip is already in the trunk is `merged` and is deleted without a tag (it is reachable from the trunk, so nothing is lost); criterion 5 counts park tags only for class `park`.
- D2. Step 3 (sayt `tagging` → `main`): the main checkout of `sayt-sistemy-konstantinova` has `tagging` checked out. Instead of switching the owner's checkout to `main`, I do the merge in a temporary worktree of `main` under `/tmp/chistka/`, push, and remove that worktree. Same commit, same push; the owner's checkout is not switched under them. If `main` is already checked out somewhere, I fall back to the literal instruction after checking the checkout is clean.
- D3. Mechanics as scripts in `/tmp/chistka/` (per §2.1 of the task); console output kept to summaries so the context stays under budget. Every tag is verified with `git ls-remote --tags` against the branch tip before that branch is deleted; the delete script refuses any branch whose tip is not reachable from `origin/<trunk>` or from a verified `arhiv/` tag, right before the delete.
- D4. Batches of at most 50 deletions per repository; after each batch a fresh verifier subagent (Agent tool, different method: independent fetch + `rev-parse`/`merge-base`) checks every `delete`/`tag+delete` row so far, and deletion stops if K > 0.
- D5. Unmerged branches: the brief's named CLOSE list is applied as given; every other unmerged branch gets a one-line judgement from `git log --oneline trunk..b`, diff stat and age. When in doubt → `keep` + a line in `VOPROSY.md`.
- D6. `vanya` is not touched by any command (not even fetch).

**Criterion check:** the readiness criterion is measurable as written; one note — criterion 4 compares the final `ls-remote --heads` count with `keep-trunk + keep-named + keep` rows, which also has to include branches that failed a step and were left in place (they will be recorded as `skip` and counted separately in `REPORT.md`).

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
Filled by the executor: no git-contour subagent ran, because the contour was empty (§0.1; VOPROSY 1). Taken 2026-09-25 11:40, before any work, in the worktree:
```
$ git --no-optional-locks branch --no-merged claude/bold-faraday-wq09ql | grep -c 'zahod/'
fatal: malformed object name claude/bold-faraday-wq09ql
0
$ git --no-optional-locks branch --no-merged origin/claude/bold-faraday-wq09ql      # rc=0
  main
$ … | grep -c 'zahod/'
0
$ git --no-optional-locks status --porcelain | wc -l
       0
$ git --no-optional-locks log --oneline @{u}.. | wc -l
       0
$ python3 …/git_zona.py zayavki | tail -1
Охват: заявок открыто 0, переадресовано 12, закрыто недавно (sdelano) 89, постоянных исключений 1, сторож краснеет на 0, держателей 0, двойной захват на 0
```

**ЧТО СДЕЛАНО** *(с хэшами)*
Nothing to merge, commit, push or close at entry: every count above is 0. The only unmerged local branch was `main`, the published site, which is a named keep.

**ВСЕ ДОЛГИ ВХОДА ЗАКРЫТЫ:** `да`
*(`нет` законно — но ТОЛЬКО со списком поимённо: что осталось и почему это непроходимо ТВОИМИ
правами (чужая живая рабочая папка, нужно решение владельца, конфликт, обеих сторон которого
не понимаешь). «Сложно» и «не моя тема» причинами не являются. `нет` без списка = красный.)*

## ОТЧЁТ — (заполняет исполнитель)

**What was done, and why.** GitHub clutter was cleaned in 11 repositories under one law: no work may be lost. Branches went from **868 to 19**: 632 deleted because they were already merged into their trunk, 217 deleted after an `arhiv/<branch>` tag was pushed and verified, and 19 kept. `sayt-sistemy-konstantinova` `tagging` was merged into `main` (014d18a). On the Mac: 40 fully merged local branches were deleted, three leftover folders went to the Trash, and a stray worktree was removed. Details and the per-repo table are in `chistka-github/REPORT.md`.

**How it was checked.** Right before every deletion, the delete script checked that the live tip was unchanged and reachable on GitHub, from the trunk or from a verified tag. After each of the 14 rounds, an independent verifier subagent ran its own script over all deletions so far (`/tmp/chistka/verifier/verify.py`), and K was 0 every time. The final verifier run printed `checked 849 of 849, 0 failures` and ended with «выдано 849 позиций из 849 найденных».

**Readiness criterion:**
1. `ls chistka-github/ | wc -l` → 9 (DNEVNIK, before.tsv, actions.tsv, VOPROSY, verifier.md, REPORT.md + classes.tsv, tags.tsv, local.tsv).
2. Coverage: checked 868 of 868. `actions.tsv` has 868 rows, all unique; the sum of `remote_branches` in `before.tsv` is 868.
3. Zero loss: `verifier.md` ends with `checked 849 of 849, 0 failures`.
4. For each repo, the live `ls-remote --heads` count equals its keep rows. All 11 repos match; the verifier's table is in `verifier.md` and `REPORT.md`.
5. For each repo, the live `arhiv/*` tag count equals its tag+delete rows (217 = 208 park + 9 unmerged). All 11 match.
6. `git merge-base --is-ancestor 35f31bf1f origin/main` in sayt → rc=0.
7. `origin/arka/mat-kostyak` contains `zahod/chistka-github`: shown after the merge in the WARNING-block entry below.

**§0.1 self-check output:** it is in `## ГИГИЕНА ВХОДА` above. The literal command failed and printed a false `0`; the command against `origin/…` gives 0 unmerged `zahod/*`. `git_zona.py check --zone chistka-github/` at entry returned rc=0, because the zone did not exist yet.

**Not touched:** `vanya` (no command at all), the 5 keep-named branches, and every existing tag (none moved or deleted, no `--force`, no rebase). No content edits were made outside the zone. The only file outside the zone that changed is `_studio/docs/KARTA.md`, through `register_doc.py`.

**НЕОБРАТИМОЕ** (what · where · how it is restored):
- 632 GitHub branches deleted as merged, in 10 repos. Restore: the per-row `git push origin <tip>:refs/heads/<branch>` in `actions.tsv`; every tip is in the trunk.
- 217 GitHub branches deleted after tagging, in 6 repos. Restore: the same per-row command; every tip is held by `arhiv/<branch>` on GitHub.
- sayt `main` got merge commit 014d18a (pushed). Restore: `git push origin 60a0e7d:refs/heads/main` would need a force push, so it is the owner's decision only.
- 40 local branches deleted with `git branch -d` (in disciplina, materials, spetsmat-bot). Restore: `local.tsv` has one command per row (`git branch <b> <tip>`).
- `/private/tmp/baseline-759ef40` worktree removed (HEAD 759ef40 is in spetsmat `origin/main`, 0 dirty lines). Restore: `git -C spetsmat-bot worktree add /private/tmp/baseline-759ef40 759ef40`.
- `~/Documents/GitHub/disciplina-wt/`, `~/Documents/GitHub/matproekty-179-wt/`, `~/Documents/GitHub/disciplina/--help/` moved to `~/.Trash/` (the last one as `disciplina--help`). Restore: move them back from the Trash.

**Questions:** see `chistka-github/VOPROSY.md` 1–4. Nothing was sent to the analyst as `QUESTION-FOR-ANALYST`, because nothing was blocking.

**Verifier result:** `checked 849 of 849, 0 failures`; rows 868 of 868; heads and tags match in 11 of 11 repos.

**Open, to come back to:** VOPROSY 3 (materials `zahod/vid-blokov-vnedrenie`) and VOPROSY 4 (disciplina `zahod/generator-rychaga`); the proposal for both is tag + delete.

**Время прогона + токены:** on the `app` channel НЕПРИМЕНИМО — there is nowhere to read them from.

**ПОВТОРЯЕМОСТЬ находок:** VOPROSY 2, the §0.1 command that turns `malformed object name` into a green `0`, will repeat in every brief built from a worktree whose base exists only as `origin/…`. That makes it a fix to `bootstrap_zahod.py` before the next pass, not a queue item. VOPROSY 1 (who fills `## ГИГИЕНА ВХОДА` when no subagent runs) will also repeat on every brief with an empty contour. VOPROSY 3–4 will not repeat: they are one-off branch decisions.

**ПРАВКИ ПРОЧИТАНЫ:** none; the block is `<правок нет>`, and the watcher on `origin/claude/bold-faraday-wq09ql` did not fire.

**АРТЕФАКТ:** `/Users/ivanyakovlev/Documents/GitHub/materials-wt/chistka-github/_studio/zhurnal/2026-09-24_arhitektura-repozitoriev/chistka-github/REPORT.md` — открывать в любом просмотрщике Markdown
*(собрал HTML, документ, PDF, картинки — путь сюда. Собранного файла нет — напиши «артефакта нет: <почему>». Пустая строка = отчёт не принимается: гейт `check_uroki.py` краснеет на коммите.)*
**РОД АРТЕФАКТА:** `собранный`
*(`собранный` — колода, PDF, картинка, любой файл, ПОРОЖДЁННЫЙ этим заходом: он обязан быть моложе файла-захода, и Г3 приёмки сверяет ВРЕМЯ. `исходник` — заход, чей продукт есть КОД: он коммитится РАНЬШЕ отчёта, потому что отчёт цитирует хэш коммита, и сверка по времени дала бы вечное ложное красное — тогда Г3 сверяет не время, а «доехал ли артефакт в названный §4 коммит». Не заполнено — Г3 работает по времени, как раньше.)*
**КОММИТ:** work commits up to `4f6359c4` — `chistka-github: step 5 done (849 deleted) + step 8 local leftovers`; the report commit and the merge into `arka/mat-kostyak` are in the last DNEVNIK entry (`FINAL:`) · `git_zona.py check --zone chistka-github/` → ✅
*(нет хэша — назови причину прямо здесь; пустая строка = отчёт не принимается)*

## СОВЕТ ПРИ СБОРКЕ (`statistika_zahodov.py --sovet`, М-2)
rod=instrumenty · putey_zony=2 · simvolov=33542 · rc=0
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
   (--simvolov 33542 sits below 142 of 143 measured task sizes; it does NOT narrow the cluster - task length did not separate the outcome on this corpus, see --analiz)
```

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

**ВЕТКА РАБОТЫ:** `zahod/chistka-github`
*(проверяется фактом, не словом: ветка обязана существовать и быть либо ВЛИТА в основную, либо названа в открытой заявке на влитие. Ни того, ни другого — Г14 краснеет. Снять состояние: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py poteri --branch <ветка>`)*

**ЗАЯВКИ, ПОСТАВЛЕННЫЕ ЭТОЙ ПРИЁМКОЙ — ПРОДУБЛИРУЙ СЮДА ТО, ЧТО УЖЕ ЛЕЖИТ В СПИСКЕ:**
> Адрес списка: `_studio/zhurnal/_INFRA-git/zayavki`
> Читается командой (из любой папки, в том числе из worktree): `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py zayavki`
> Ставится командой: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py zayavka --rod <git-operaciya|pravka-koda> "<текст>"`
> 🔴 Вопрос здесь НЕ «что ты хочешь сделать», а «что ты УЖЕ положил в очередь». Дубль сверяется с очередью по id машинно; намерение сверить не с чем.

- `<id заявки>` — `<род>` — `<суть одной строкой: влитие / коммит / вывоз / деплой / гашение>`

*(Заявок эта приёмка не ставила — так и напиши строкой «заявок нет: <почему ни одна из пяти операций не понадобилась>». Пустая строка и прочерк не принимаются: молчание неотличимо от «забыл».)*
