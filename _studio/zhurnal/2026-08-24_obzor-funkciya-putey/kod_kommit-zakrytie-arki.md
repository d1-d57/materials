# Канал исполнителя — kommit-zakrytie-arki (один заход до конца)
> Твой единственный файл-заход. Читай ТОЛЬКО его и названные якоря; проект не изучай.
<!-- собран bootstrap_zahod.py -->
<!-- гейт сборки заполненного: ЗЕЛЁНЫЙ 2026-10-10 -->
> План/вопросы/отчёт — в секции внизу. Метрика — КАЧЕСТВО. Часы — норма.
> **Модель: Sonnet 5** — механика расписана до путей: пять коммитов поименными pathspec, одна строка в .gitignore, вывоз, проверка числами.

## СТАРТОВОЕ СООБЩЕНИЕ ВЛАДЕЛЬЦУ

> Это блок для владельца — то, чем тебя запустили. Исполнителю здесь делать нечего, твоё задание ниже.

```
Модель: Sonnet 5 — механика расписана до путей: три коммита в materials и один в disciplina, одна строка в .gitignore, вывоз, проверка числами.

Ты исполнитель в репозитории /Users/ivanyakovlev/Documents/GitHub/materials.

Твой единственный вход — файл-заход:
/Users/ivanyakovlev/Documents/GitHub/materials/_studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_kommit-zakrytie-arki.md

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
🔴 снимок при сборке 2026-10-10, ПРОВЕРЬ ПЕРВЫМ ХОДОМ: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/schet_nezakrytogo.py _studio/zhurnal/2026-08-24_obzor-funkciya-putey`
Область: «_studio/zhurnal/2026-08-24_obzor-funkciya-putey» — сужены пункты 1, 3, 4; долги (2) глобальны намеренно (DOLG.md не размечен по записям).
Приоритет владельца: разобрать инциденты важнее, потом закрыть долги — неразобранный инцидент это повторяющаяся ошибка, долг может подождать.
  1. инцидентов без вердикта             : 0
  2. долгов СТАТУС: ЖИВ                  : н/д — ни одного skills/*/DOLG.md нет на диске (другой git-репозиторий)
  3. уроков фабрике без ВЕРДИКТ          : 55
  4. пунктов очереди «ДОСТАВЛЕНО: нет»   : 61
     из них разбором очереди (парсер `dostavit_urok`, записи с парой ДОМ:/ДОСТАВЛЕНО:): 26
       живых (чинится доставкой — «дом есть»)  : 14
       к владельцу (решение за человеком)      : 6
       адрес недоступен (нет/папка/код/указат.) : 4
       адрес не разобран                        : 0
       отработавших (машинный след закрытия)    : 0
       доставлено                               : 2
       🔴 не проверяется машиной: содержательная отработанность записей БЕЗ следа закрытия (метки в доме, строки ✅/ЗАКРЫТО) — нужна ревизия человеком; сырой греп сверх разбора — шаблонные строки формы.

🔴 ДВЕРЬ НЕЗАКОММИЧЕННЫХ `kod_*.md` ОТКРЫТА КЛАПАНОМ: в арке `_studio/zhurnal/2026-08-24_obzor-funkciya-putey` есть 1 незакоммиченных файлов-заходов `kod_kommit-binomy-sayt.md` — второй заход в такую арку обычно не собирается (долг 4 `disciplina-git`), но АНАЛИТИК открыл клапан, причина дословно: «цель захода — закоммитить именно эту грязь: kod_kommit-binomy-sayt.md (дописана приёмка) входит в зону коммита». Отключение видно здесь, в артефакте, а не осталось решением в голове аналитика.

🔴 ДВЕРЬ ГЕЙТА СБОРКИ ЗАПОЛНЕННОГО ФАЙЛА ОТКРЫТА КЛАПАНОМ: в арке `_studio/zhurnal/2026-08-24_obzor-funkciya-putey` лежат файлы-заходы со штампом «ЖДЁТ», красные на `check_sborki.py` — `kod_arhitektura-punkta.md`, `kod_graf-korpusa.md`, `kod_katalog-kursa.md`, `kod_konsolidaciya-korpusa.md`, `kod_napolnenie-chetverti.md`, `kod_otrisovka-vidov.md`, `kod_pasporta-korpusa.md`, `kod_rasskaz-god.md`, `kod_zakon-zakrytiya-noch-puti-i-volny.md` — следующий заход в такую арку обычно не собирается, но АНАЛИТИК открыл клапан, причина дословно: «арка закрыта 10.10 (баннер в PLAN.md): девять августовских заходов со штампом ЖДЁТ — мёртвые каркасы ночной волны, исполняться не будут; этот заход их не трогает». Отключение видно здесь, в артефакте, а не осталось решением в голове аналитика.

КОНТЕКСТ. Арка `_studio/zhurnal/2026-08-24_obzor-funkciya-putey` (курс владельца «Пути и волны», статья-обзор 01 «Биномиальные коэффициенты») закрыта 10.10. Статья v6 и страница сайта УЖЕ в git, вывезены и опубликованы (коммиты `fdb4ba4a`, `aa7e5878`, публикация `19b12215` на `origin/main`) — их не трогай. Прошлый этап: аналитик Cowork (коммитить не может по построению) закрыл арку на диске — консолидация решений по домам курса (10 файлов `kurs-puti-i-volny/`), сводки состояния, баннер закрытия, дневник, выгрузка сессии, дословное сырьё владельца `syroe-2026-10-04/` (9 файлов), правка движка `disciplina/_generator/build_doc.py` (кнопки на телефоне, 2 строки CSS). ЦЕЛЬ: забрать всё это в git и вывезти. Содержание файлов НЕ правится — только одна строка-исключение в `.gitignore` и git.
Приёмка — по ОТЧЁТУ, без построчной сверки. Стоп до цели: получишь всё в git, кроме `UROKI-FABRIKE.md` (на нём законно красный `check_uroki.py`; его забирает следующий заход уроков), — этот файл обязан остаться незакоммиченным.

## ЧТО ФИНАЛИЗИРОВАНО НА ИНТЕРВЬЮ

ИНТЕРВЬЮ ПРОВЕДЕНО: да (2026-10-10) — флаг `--intervyu da` при сборке. ⚠ Он доказывает, что аналитик не ЗАБЫЛ про интервью, и НЕ доказывает, что разговор был.

1. Сырьё владельца (syroe-2026-10-04/) — в git: владелец 10.10 10:39 «все в гит» на прямой вопрос «в публичный git или на диске вне git»
2. Арка obzor-funkciya-putey закрыта (владелец 10.10 10:39); всё сделанное при закрытии — одним коммит-заходом исполнителя (Ф6 плана спасения, «начинай» 15:39)
3. UROKI-FABRIKE.md в этот заход НЕ входит: его коммитит отдельный заход уроков (решение владельца 10.10 «отдельный бриф исполнителю»)

## КОНТРАКТ ЗОНЫ (обязателен — не удалять; вписан Cowork)
- **МЕСТО РАБОТЫ:** ветка `arka/mat-kostyak` в основной папке. 🔴 Она должна УЖЕ стоять. НЕ на ней — СТОП, НЕ делай `git checkout`: в общей папке он МОЛЧА откатывает дерево к состоянию ветки (цена 27→28.07: файл сильно откатился ночью, поймал владелец вручную; след в git НЕ остаётся). Тогда заход пересобрать с `--worktree`. Ветку не переключай, в другие НЕ коммить.
- **ВТОРОЙ РЕПОЗИТОРИЙ:** `/Users/ivanyakovlev/Documents/GitHub/disciplina` (ветка `main`) — ровно один файл `_generator/build_doc.py`, только коммит и вывоз. Остальная грязь disciplina — чужая.
- **ЗОНА (можно менять):** `_studio/zhurnal/2026-08-24_obzor-funkciya-putey/` `_studio/docs/KARTA.md` `_studio/docs/sostoyanie/SVODKI.md` `_studio/docs/sostoyanie/OTKRYTYE-ZADACHI.md` `kurs-puti-i-volny/` `./.gitignore` `_studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_kommit-zakrytie-arki.md`. Всё вне — **READ-ONLY**: не править, не двигать, не удалять, не рефакторить «заодно».
- 🔴 **ЗАВЁЛ НОВЫЙ `.md` — РЕГИСТРИРУЕШЬ ЕГО САМ, ТЕМ ЖЕ ХОДОМ, ОДНОЙ КОМАНДОЙ:** `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/register_doc.py <путь> "<описание>"` (из корня репо). `_studio/docs/` тебе по-прежнему READ-ONLY **для правки руками** — дверь ровно одна, и это она. Дверь идемпотентна (повторный вызов дубля не заведёт) и отказывает на пути вне `_studio/`, на несуществующем файле и на пустом описании. Свой файл-заход регистрировать не нужно: он рождается зарегистрированным из `bootstrap_zahod.py`. **Красный хук на ТВОЁМ новом `.md` — это не повод для `--no-verify`, а повод позвать дверь.** *(история цены — `/sessions/rcw-018aaowdc3vczyubvpqz3dee/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц1) Обходить больше нечего.*
- **КОММИТ:** два хода — `add` по своим путям, затем `commit` **с теми же путями после `--`** (полная форма и цена каждого хода — §4); коммить ПО ХОДУ работы, не одним последним ходом (§4). НИКОГДА `-A` / `.` / `commit -am`, и никогда `commit` без путей. Субагенты не коммитят. **`--no-optional-locks` обязателен:** обычный git переписывает индекс, берёт `.git/index.lock` и роняет параллельный ручной коммит владельца.
- **SCRATCHPAD — ТОЛЬКО ЛИЧНЫЙ.** Черновики, выкладки, промежуточные версии — в личную папку СВОЕГО захода `scratchpad/kommit-zakrytie-arki/`. Общие пути (`scratchpad/otchet.md`, любой `scratchpad/*` без имени твоей темы) ЗАПРЕЩЕНЫ: чужой отчёт уедет в твой файл или твой — в чужой, а приёмка читает отчёт без построчной сверки и подмену НЕ ЛОВИТ по построению. (история цены — `/sessions/rcw-018aaowdc3vczyubvpqz3dee/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц2)
- 🔴 **Звал `register_doc.py` — допиши `_studio/docs/KARTA.md` к своим путям В ОБОИХ ходах.** Строка регистрации лежит физически в нём. Ворота 5 читают `§6` **с диска**, а не из индекса: коммит без этого файла пройдёт ЗЕЛЁНЫМ, документ уедет сиротой, а строка умрёт при первом `checkout` (история цены — `/sessions/rcw-018aaowdc3vczyubvpqz3dee/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц3).
- **ЗАПРЕТ:** ничего за пределами зоны, даже если «мешает» или «чинится в одну строку». Нашёл проблему вне зоны → в отчёт, не трогай.

## 0. ПЕРВЫЙ ХОД
### 0.1 🔴 ГИТ-КОНТУР — ДО ВСЕГО ОСТАЛЬНОГО, И ПЕРВЫМ ХОДОМ ЦЕЛИКОМ

🔴 «ничего сверх задачи» относится к СОДЕРЖАНИЮ работы; git-контур §0.1 — законное исключение, он про состояние репозитория и исполняется целиком.

🔴 **ПОРЯДОК ЗДЕСЬ — ЧАСТЬ УСТРОЙСТВА, А НЕ ОФОРМЛЕНИЕ. Сначала субагент вливает названные через `--vlit` ЧУЖИЕ ветки В ОСНОВНУЮ, и только ПОТОМ ты заводишь свою рабочую папку; СВОЮ ветку он не трогает никогда — её вливаешь ты сам последним ходом (граница прав ниже).** (история цены — `/sessions/rcw-018aaowdc3vczyubvpqz3dee/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц5) Заводя ветку ПОСЛЕ влития, ты отпочковываешь её от основной, которая уже всё содержит: инструмент оказывается на диске сам, дотаскивать нечего.

🔴 Очередь заявок подметена на входе волны, твоё дело здесь — только своя зона: закрывает и вливает очередь роль коммитера (`agents/kommiter.md`), один раз на входе волны и один раз на выходе (`python3 _generator/tools/bootstrap_zahod.py --podmetanie-volny vhod|vyhod`), не сборка этой позиции.

**1. ВЕСЬ КОНТУР — В СУБАГЕНТА, ОДНИМ ХОДОМ, ДО СВОЕЙ ПАПКИ.** Влитие названных веток в ОСНОВНУЮ, что забрать в git по ходу и что погасить после — на содержание твоей задачи не влияют. Запусти ОДНОГО субагента, дождись его и вставь его пять строк в `## ОТЧЁТ` дословно; сам эти пункты не исполняй. 🔴 ПОРЯДОК ПРИ ПАДЕНИИ ЭТОГО ВЫЗОВА — исполняй, не изобретай (движок роняет `network_error` на вызове субагента и уносит с собой ВЕСЬ заход, замер волны 3A — 4 захода из 13). Пауза 45 секунд, до трёх попыток; время меряй `date`, не суммой своих `sleep`. После третьей — работай БЕЗ субагента: контур остаётся неразобранным, и это ОТДЕЛЬНАЯ строка в `## ОТЧЁТ`, а не молчание. У него ОТДЕЛЬНЫЕ ПРАВА, объявленные в его же промпте: главная папка, основная ветка, вывоз — и ничего сверх; зону захода он не коммитит, её коммитишь ты сам, по ходу работы (§4). 🔴 ОТВЕТ ЛЮБОГО субагента, которого ты запускаешь (не только этого), обязан КОНЧАТЬСЯ строкой «выдано N позиций из M найденных»: канал мог оборвать его молча, и без этой строки усечение неотличимо от честного «мало нашлось». Нет строки — ответ усечён, в `## ОТЧЁТ` не вставляй, перезапроси. Полный текст задания печатает команда:
```
python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/bootstrap_zahod.py --zadanie-subagentu --zone _studio/zhurnal/2026-08-24_obzor-funkciya-putey/ --zone _studio/docs/KARTA.md --zone _studio/docs/sostoyanie/SVODKI.md --zone _studio/docs/sostoyanie/OTKRYTYE-ZADACHI.md --zone kurs-puti-i-volny/ --zone .gitignore --kommitit 'журнал арки _studio/zhurnal/2026-08-24_obzor-funkciya-putey/ кроме UROKI-FABRIKE.md, включая kod_kommit-binomy-sayt.md и этот файл-заход' --kommitit 'syroe-2026-10-04/ после строки-исключения в .gitignore' --kommitit 'kurs-puti-i-volny/ — 10 правленых файлов консолидации' --kommitit '_studio/docs/KARTA.md и _studio/docs/sostoyanie/{SVODKI,OTKRYTYE-ZADACHI}.md' --kommitit 'в disciplina: _generator/build_doc.py' --zakryt 'веток не гасить: arka/mat-kostyak живая, работа идёт на ней; worktree не заводится'
```

🔴 ГРАНИЦА ПРАВ, ТРИ ОТВЕТА (та же, что в самом задании субагенту — одно место в тексте, а не пересказ): **кто вливает ЧУЖИЕ названные (`--vlit`) ветки** — субагент, в ОСНОВНУЮ ветку, до заведения твоей папки; **кто вливает СВОЮ ветку этого захода** — ты сам, последним ходом, после коммита зоны (`git_zona.py vlit-v-osnovnuyu`; (история цены — `/sessions/rcw-018aaowdc3vczyubvpqz3dee/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц6)); **кто коммитит пути ВНЕ зоны захода** — субагент (хвост Cowork и что назовёт пункт 3 его задания). Очередь заявок эту границу больше не касается — её закрывает роль коммитера на границе волны, не субагент этой позиции. Ты коммитишь ТОЛЬКО зону этого захода, по ходу работы (§4). 🔴 Конфликт на `README.md` при ЛЮБОМ слиянии разрешается ОБЪЕДИНЕНИЕМ записей реестра, НИКОГДА выбором стороны: параллельные заходы волны дописали в реестр по строке — обе записи правы, выбор одной молча уничтожает регистрацию соседа.

**2. ТЕПЕРЬ ЗАВОДИ СВОЮ РАБОЧУЮ ПАПКУ** (команда — в блоке «МЕСТО РАБОТЫ» выше) и работай в ней как обычно. Её ветка отпочкована от свежей основной, поэтому инструмент, которым ты работаешь, уже на диске — отдельного «влить перед работой» больше нет.

Невлитых `zahod/*`-веток, НЕ покрытых `--vlit`, — 1: `zahod/istoriya-sessij` — 🔴 снимок при сборке 2026-10-10, ПРОВЕРЬ ПЕРВЫМ ХОДОМ: `git --no-optional-locks branch --no-merged arka/mat-kostyak | grep -c 'zahod/'`. 🔴 КЛАПАН ОТКРЫТ АНАЛИТИКОМ, причина дословно: «zahod/istoriya-sessij — чужая работа другой арки, к закрытию этой арки отношения не имеет; вливать — решение её приёмки». Заход собран ВОПРЕКИ невлитому этой веткой — отключение видно здесь, в артефакте, а не осталось решением в голове аналитика (§79 канона: невлитая ветка законна, рядом может идти чужой заход).


- задеплоить: деплоя в этом заходе нет: страница v6 уже опубликована (origin/main 19b12215)

- Проверь ветку: `git branch --show-current` — обязано быть `arka/mat-kostyak`. Не она — СТОП, `git checkout` НЕ делай (§4 GIT-disciplina), нужен `--worktree`.
- Точка отката: `git add _studio/zhurnal/2026-08-24_obzor-funkciya-putey/ _studio/docs/KARTA.md _studio/docs/sostoyanie/SVODKI.md _studio/docs/sostoyanie/OTKRYTYE-ZADACHI.md kurs-puti-i-volny/ .gitignore _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_kommit-zakrytie-arki.md` → commit (или zip), если зона не чиста в HEAD (не фабрикуй, если чиста).
- Прочитать ТОЛЬКО: этот файл и строки 170–176 `/Users/ivanyakovlev/Documents/GitHub/materials/.gitignore` (блок «Ученик Миша»). Проект не изучай.
- ПЛАН — в `## ПЛАН` перед действиями.

## 1. ДИСЦИПЛИНА (Карпатов)
🔴 **Развилку ВНУТРИ своей зоны решаешь сам** — называешь решение в `## ПЛАН` и идёшь дальше; спрашивать и ЖДАТЬ ответа владельца — только там, где любой выбор делает работу опасной или бессмысленной. Целый прогон уже вставал на вопросе, ответ на который лежал в собственном контракте зоны исполнителя (урок арки `2026-08-20_poryadok-v-metaskillah`).
🔴 **Не собирай `rm` с путём из переменных.** Защитный слой перехватывает такие команды НЕЗАВИСИМО от Bypass permissions и останавливает работу до ответа человека — замер 20.09: 5 ч 48 мин при работающей машине. Вместо `cp X Y && rm X` пиши `mv X Y`; где не подходит — питон-скрипт ФАЙЛОМ, не однострочник с `rm`.
🔴 **Код возврата — ПЕРВЫМ, до содержательного вывода команды.** «Отработала» и «упала, а я читаю прошлое состояние» выглядят одинаково; сначала `echo $?`, потом выводы. То же с гейтами. (история цены — `/sessions/rcw-018aaowdc3vczyubvpqz3dee/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц7)
Предпосылки/развилки назвать вслух; минимум без спекуляций; хирургия (строка → к заданию); критерий, который может провалиться. Якорные замены — abort при ≠1. Сохранять по умолчанию. **Оспорить ложную предпосылку — включая КРИТЕРИЙ ГОТОВНОСТИ: считаешь его кривым — скажи в `## ПЛАН`, ДО работы, и предложи поправку.** Субагенты: ≤5, рейт-лимит = отступить + доложить (не слепой ретрай).

🔴 **Пишешь содержательный текст — термин НЕ употребляется раньше, чем определён**, включая заголовки, подводки и формулировки теорем. «Определение в тексте есть» не считается: если оно ниже первого рабочего употребления, читатель встаёт ровно там. Чинится ПЕРЕСТАНОВКОЙ определения вверх, не дописыванием пояснения. Гейт: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/check_termin.py <src>` (exit 1 при нарушении). Канон — `../docs/kak-delat/STANDART-teksta.md` правило 11. (история цены — `/sessions/rcw-018aaowdc3vczyubvpqz3dee/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц8)

## 2. ЗАДАЧА

🔴 **WRITE YOUR `## ОТЧЁТ`, `## ПЛАН` AND `## ВОПРОСЫ` IN ENGLISH, AND EVERY FILE AND EVERY COMMIT MESSAGE YOU PRODUCE TOO.** Owner's decision 30.08. It is a каркас-level rule, not a preference (история цены — `/sessions/rcw-018aaowdc3vczyubvpqz3dee/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц9). Fixed Russian addresses stay Cyrillic: `ЦЕНА:` · `ВЕРДИКТ:` · `ДОМ:` · `ДОСТАВЛЕНО:` · `ПОДЪЁМ:` · `[ДОЛГ: …]` · every `## ` heading of this file · every path and command.
🔴 **Поправки к шаблону выше — для ЭТОГО захода (иначе два указания противоречат):** (а) рабочей папки (worktree) НЕТ — §0.1 п.2 к тебе не относится: работаешь в основной папке `/Users/ivanyakovlev/Documents/GitHub/materials` на УЖЕ текущей `arka/mat-kostyak`, ветку не переключаешь и не заводишь; генератор предупредил о 5 живых рабочих папках — это ЧУЖИЕ параллельные заходы, поэтому только поимённые pathspec, никогда `-A`/`.`; (б) вливать нечего; (в) список «что забрать в git» из §0.1 — ТВОИ коммиты ниже, субагент гит-контура эти пути НЕ коммитит (прошлый заход арки поймал это противоречие шаблона, урок в его `## УРОКИ ФАБРИКЕ`); (г) строки шаблона §4 — образец формы; исполняй ТОЧНЫЕ команды ниже: шаблонный `add -- _studio/zhurnal/2026-08-24_obzor-funkciya-putey/` забрал бы `UROKI-FABRIKE.md`; (д) Г2 гигиены для тебя ПРИМЕНИМ — второй репозиторий в зоне одним файлом; (е) этот файл-заход коммитишь ты (в коммите 1), без отчёта; отчёт докоммитит приёмка.

**Шаги (по порядку, код возврата — первым):**
0. `cd /Users/ivanyakovlev/Documents/GitHub/materials`; `git branch --show-current` → `arka/mat-kostyak` (иначе СТОП). Мёртвые локи: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py clean`.
1. **Сверка, что в зоне только работа этой арки** (чужие строки — в `## ВОПРОСЫ`, молча не коммить): `git --no-optional-locks diff -- _studio/docs/sostoyanie/SVODKI.md _studio/docs/sostoyanie/OTKRYTYE-ZADACHI.md` — все добавленные блоки про арку `2026-08-24_obzor-funkciya-putey` или курс «Пути и волны» (при сборке +10 и +29 строк); `git --no-optional-locks diff -- _studio/docs/KARTA.md` — только строки регистрации файлов `_studio/zhurnal/2026-08-24_obzor-funkciya-putey/` и `kurs-puti-i-volny/`; `git -C /Users/ivanyakovlev/Documents/GitHub/disciplina --no-optional-locks diff --stat -- _generator/build_doc.py` → `1 file changed, 2 insertions(+), 2 deletions(-)`.
2. **`.gitignore` — одна вставка.** Строка `_studio/zhurnal/*/syroe-*/` в файле ровно одна (`grep -c '^_studio/zhurnal/\*/syroe-\*/$' .gitignore` → 1, иначе СТОП). СРАЗУ ПОСЛЕ неё вставь две строки дословно:
   `# Исключение: дословные тексты ВЛАДЕЛЬЦА (не ученика) арки obzor-funkciya-putey — в git по его решению 10.10 «все в гит».`
   `!_studio/zhurnal/2026-08-24_obzor-funkciya-putey/syroe-2026-10-04/`
   Проверка: `git check-ignore -q _studio/zhurnal/2026-08-24_obzor-funkciya-putey/syroe-2026-10-04/README.md; echo $?` → **1** (больше не игнорируется); `git check-ignore -q _studio/zhurnal/2026-09-13_uchenik-misha/syroe-2026-10-04; echo $?` → **0** (данные ученика по-прежнему вне git — если 1, СТОП и откат строки: это персональные данные несовершеннолетнего).
3. **Коммит 1 — журнал арки, сырьё, `.gitignore`:**
   `git --no-optional-locks add -- _studio/zhurnal/2026-08-24_obzor-funkciya-putey/ .gitignore ':(exclude)_studio/zhurnal/2026-08-24_obzor-funkciya-putey/UROKI-FABRIKE.md'`
   `git --no-optional-locks commit -m "arc obzor-funkciya-putey closed: consolidation, rescue plan, session export, owner raw texts (syroe-2026-10-04), closing banner, diary; .gitignore re-includes this arc's owner raw folder" -- _studio/zhurnal/2026-08-24_obzor-funkciya-putey/ .gitignore ':(exclude)_studio/zhurnal/2026-08-24_obzor-funkciya-putey/UROKI-FABRIKE.md'`
   Проверка счётом: `git --no-optional-locks show --name-only --format= HEAD | grep -c -v -e '^_studio/zhurnal/2026-08-24_obzor-funkciya-putey/' -e '^.gitignore$'` → **0**; `git --no-optional-locks show --name-only --format= HEAD | grep -c -e 'UROKI-FABRIKE' -e 'uchenik-misha'` → **0**; `git --no-optional-locks show --name-only --format= HEAD | grep -c 'syroe-2026-10-04/'` → **9**.
   Хук покраснел: на `check_uroki` — значит в индекс попал `UROKI-FABRIKE.md`, убери его из коммита (не правь файл); на чужом долге — клапан шаблона §4 с причиной; на СВОЁМ содержании — СТОП, в `## ВОПРОСЫ`, содержание не правь.
4. **Коммит 2 — курс (консолидация по домам):**
   `git --no-optional-locks add -- kurs-puti-i-volny/`
   `git --no-optional-locks commit -m "kurs-puti-i-volny: arc closure consolidation - interview decisions 19.09/23.09 into ZAMYSEL (axis, quarter = one object, club format), OBEKT, ARHITEKTURA, SLOVAR, PAMYAT-PROEKTA, karkas, REESTR, AVATARKA, lesson 01, review 01 README" -- kurs-puti-i-volny/`
   Проверка: `git --no-optional-locks show --name-only --format= HEAD | grep -c -v '^kurs-puti-i-volny/'` → **0**.
5. **Коммит 3 — состояние и регистрация:**
   `git --no-optional-locks add -- _studio/docs/KARTA.md _studio/docs/sostoyanie/SVODKI.md _studio/docs/sostoyanie/OTKRYTYE-ZADACHI.md`
   `git --no-optional-locks commit -m "state: arc obzor-funkciya-putey closed - summary, open tasks, successor decision; KARTA registrations" -- _studio/docs/KARTA.md _studio/docs/sostoyanie/SVODKI.md _studio/docs/sostoyanie/OTKRYTYE-ZADACHI.md`
   Проверка: `git --no-optional-locks show --name-only --format= HEAD` → ровно 3 пути.
6. **Вывоз materials:** `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py vyvezti` (предпросмотр), затем `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py vyvezti --yes`. Код 3 «ВЫВОЗ ОТЛОЖЕН» — законный исход, впиши дословно в отчёт.
7. **Коммит 4 — движок в disciplina:** `cd /Users/ivanyakovlev/Documents/GitHub/disciplina`; `git branch --show-current` → `main` (иначе СТОП).
   `git --no-optional-locks add -- _generator/build_doc.py`
   `git --no-optional-locks commit -m "build_doc: statya overlay - content/topic buttons pinned top-right on phones (<=900px), page top padding for them (review 'Binomial coefficients' v6)" -- _generator/build_doc.py`
   Проверка: `git --no-optional-locks show --name-only --format= HEAD` → ровно `_generator/build_doc.py`. Чужие незакоммиченные правки disciplina — НЕ трогать, не коммитить, не прятать.
   Вывоз: `GIT_ZONA_REPO=/Users/ivanyakovlev/Documents/GitHub/disciplina python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py vyvezti`, затем то же с `--yes`.

**КРИТЕРИЙ ГОТОВНОСТИ (может ПРОВАЛИТЬСЯ) — пять чисел, команды из корня materials; значения ПРИ СБОРКЕ 2026-10-10 15:5x рядом:**
- `git --no-optional-locks ls-files --others --exclude-standard -- _studio/zhurnal/2026-08-24_obzor-funkciya-putey kurs-puti-i-volny | wc -l` → **0**; при сборке **6** (до строки в `.gitignore`; после неё станет 15 — 6 + 9 файлов сырья).
- `git --no-optional-locks diff --name-only -- _studio/zhurnal/2026-08-24_obzor-funkciya-putey kurs-puti-i-volny .gitignore _studio/docs/KARTA.md _studio/docs/sostoyanie/SVODKI.md _studio/docs/sostoyanie/OTKRYTYE-ZADACHI.md` → ровно **одна** строка `_studio/zhurnal/2026-08-24_obzor-funkciya-putey/UROKI-FABRIKE.md`; при сборке **17** строк.
- `git --no-optional-locks ls-files -- _studio/zhurnal/2026-08-24_obzor-funkciya-putey/syroe-2026-10-04 | wc -l` равно `ls _studio/zhurnal/2026-08-24_obzor-funkciya-putey/syroe-2026-10-04 | wc -l`; при сборке **0** против **9**.
- `git --no-optional-locks rev-list --count origin/arka/mat-kostyak..HEAD` → **0** (либо код 3 вывоза, названный в отчёте).
- `git -C /Users/ivanyakovlev/Documents/GitHub/disciplina --no-optional-locks diff --name-only -- _generator/build_doc.py | wc -l` → **0** (при сборке **1**) и `git -C /Users/ivanyakovlev/Documents/GitHub/disciplina --no-optional-locks rev-list --count origin/main..HEAD` → **0**.
**Отрицательный вердикт несёт ОХВАТ В СЕБЕ:** не «дыр не найдено», а «дыр не найдено, проверено X из Y». Без охвата вердикт не принимается — «проверено 2 из 9» и «проверено 9 из 9» выглядят одинаково.

## 3. ВЕРИФИКАТОР (если двигаем/теряем/жмём)

Верификатор не нужен: операция не лоссовая: только git add/commit/push поименных путей и одна строка-исключение в .gitignore; содержание файлов не меняется.

## 4. 🔴 КОММИТ СВОЕЙ ЗОНЫ — ПО ХОДУ РАБОТЫ, НЕ ОДНИМ ПОСЛЕДНИМ ХОДОМ
Ты работаешь host-side и в `.git` ПИШЕШЬ — значит коммитишь САМ, никому не передавая. Каждую завершённую часть работы коммить СРАЗУ, теми же двумя ходами — не копи всё к финальному ходу:
```
git --no-optional-locks add -- _studio/zhurnal/2026-08-24_obzor-funkciya-putey/ _studio/docs/KARTA.md _studio/docs/sostoyanie/SVODKI.md _studio/docs/sostoyanie/OTKRYTYE-ZADACHI.md kurs-puti-i-volny/ .gitignore _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_kommit-zakrytie-arki.md                     # вводит НОВЫЕ пути в индекс
git --no-optional-locks commit -m "<зона>: <что сделано>" -- _studio/zhurnal/2026-08-24_obzor-funkciya-putey/ _studio/docs/KARTA.md _studio/docs/sostoyanie/SVODKI.md _studio/docs/sostoyanie/OTKRYTYE-ZADACHI.md kurs-puti-i-volny/ .gitignore _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_kommit-zakrytie-arki.md   # отсекает всё чужое
python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone <зона>   # из корня репо; должен быть ✅
git --no-optional-locks show --stat                        # обязаны быть ТОЛЬКО твои пути
```
🔴 **КОММИТЬ ПО ХОДУ — РЕШЕНИЕ ВЛАДЕЛЬЦА 25.08 (В11), ПЕРЕВЕРНУВШЕЕ прежний канон «одним последним ходом».** (история цены — `/sessions/rcw-018aaowdc3vczyubvpqz3dee/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц10) Закончил кусок — закоммитил его; последний ход только ПРОВЕРЯЕТ, что коммитить нечего (`git status --porcelain` пуст, `git_zona.py check --zone` ✅).
🔴 **ОБА хода обязательны, ни один не лишний** (полное «почему» и цена — `../docs/kak-delat/GIT-disciplina.md §3`):
- **`add`** — pathspec-коммит знает только **отслеживаемые** пути; новый файл без `add` даёт `did not match any file(s) known to git`.
- **`-- <пути>` в самом `commit`** — иначе `commit` забирает индекс ЦЕЛИКОМ, вместе с чужим, застейдженным кем угодно рядом с тобой (репо `materials/` общий, писателей трое). (история цены — `/sessions/rcw-018aaowdc3vczyubvpqz3dee/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц11)
⚠ **Хук `pre-commit` покраснел — сначала посмотри, на ЧЬИХ путях.**
- Красное на ТВОИХ путях (новый `.md` не зарегистрирован в `../../docs/KARTA.md §6`, битая ссылка) — **чини, не обходи**: там только твоё, обходить нечего.
- Красное на ЧУЖОМ, унаследованном долге (ворота дают сотни ❌ старых нарушений) — законный обход, но ТОЛЬКО с причиной; голый `--no-verify` инструмент отклонит, а причина сама уедет в `INCIDENTY.md`:
```
python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py commit --zone <зона> \
    --no-verify "чужой долг: <что именно покраснело>" -m "<что и зачем>" --push
```
Ту же причину назови отдельной строкой отчёта долгом. (история цены — `/sessions/rcw-018aaowdc3vczyubvpqz3dee/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц12)
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
> (история цены — `/sessions/rcw-018aaowdc3vczyubvpqz3dee/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц13)

**ЗОНА ГИГИЕНЫ:** `_studio/zhurnal/2026-08-24_obzor-funkciya-putey/` `_studio/docs/KARTA.md` `_studio/docs/sostoyanie/SVODKI.md` `_studio/docs/sostoyanie/OTKRYTYE-ZADACHI.md` `kurs-puti-i-volny/` `.gitignore` `_studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_kommit-zakrytie-arki.md`

- **Г1. Зона доехала в git.** `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone _studio/zhurnal/2026-08-24_obzor-funkciya-putey/` → ✅; `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone _studio/docs/KARTA.md` → ✅; `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone _studio/docs/sostoyanie/SVODKI.md` → ✅; `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone _studio/docs/sostoyanie/OTKRYTYE-ZADACHI.md` → ✅; `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone kurs-puti-i-volny/` → ✅; `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone .gitignore` → ✅; `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone _studio/zhurnal/2026-08-24_obzor-funkciya-putey/kod_kommit-zakrytie-arki.md` → ✅. Красное на любой из команд — отчёт не принимается: приёмка гоняет их все первым ходом.
- **Г2. Второй репозиторий.** **ПРИМЕНИМ в этом заходе** (поправка аналитика: зона включает `/Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/build_doc.py`; генератор зону второго репозитория не видит): `git -C /Users/ivanyakovlev/Documents/GitHub/disciplina --no-optional-locks diff --name-only -- _generator/build_doc.py` → пусто. Текст генератора ниже — для заходов без второго репозитория: все пути зоны лежат внутри репозитория `materials` (тот же критерий, что у С2 `check_sborki.py`). Зона расширилась за его пределы по ходу — пункт снова применим; команда та же, что в применимом случае: `cd ../<репозиторий> && git --no-optional-locks status --porcelain` → пусто. *Команда названа и здесь нарочно (находка верификатора): пункт, который объявлен неприменимым и не говорит, ЧТО делать, когда станет применим, исполнить в этот момент нечем.*
- **Г3. Невлитых веток не прибавилось.** `git --no-optional-locks branch --no-merged arka/mat-kostyak` — число сравни с тем, что было на входе. Выросло — назови, чьи ветки и почему они законны.
- **Г4. Новый инструмент имеет живую точку вызова.** Завёл `.py` в `_generator/**` — `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/check_tool_contract.py <свои новые файлы>` → rc=0. Ни одного нового `.py` — так и напиши. *Инструмент без точки вызова зелен ровно потому, что его никто не звал.*
- **Г5. Новый `.md` зарегистрирован.** Завёл — звал ли ты `register_doc.py` и лежит ли строка на диске: `grep -c '<имя файла>' <карта своего корня>` → 1. Карту своего корня называет `korni.карта_для('<путь>')`, руками её не угадывай.
- **Г6. В коммите нет чужих путей.** `git --no-optional-locks show --stat` — только твои пути. Чужой путь в своём коммите — это чужая работа, унесённая твоим `commit` без `--`.

## 5. ОТЧЁТ → секция `## ОТЧЁТ` внизу
Что сделал + ЗАЧЕМ / как проверил / что НЕ трогал / вопросы / результат верификатора / открытое «возвращаться» / **время прогона + токены — на канале `app` НЕПРИМЕНИМО, снимать неоткуда** (лог прогона существует только на канале `terminal`, где его кладёт `tee`; сессия в приложении Claude Code такого следа не оставляет). Строку не заполнять числом и не извиняться за его отсутствие — это не недосмотр исполнителя, а свойство канала) / **ПОВТОРЯЕМОСТЬ находок (строка обязательна — см. ниже)** / **АРТЕФАКТ (строка обязательна)** / **КОММИТ (строка обязательна, см. §4)**.

🔴 **АРТЕФАКТ — АБСОЛЮТНЫЙ ПУТЬ К СОБРАННОМУ ФАЙЛУ, отдельной строкой.** Не «колода пересобрана», не «см. `dist/`», а путь, который владелец скопирует и откроет. *(история цены — `/sessions/rcw-018aaowdc3vczyubvpqz3dee/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц14) Отчёт без адреса артефакта — это отчёт о работе, которую нельзя посмотреть.*

🔴 **НЕОБРАТИМОЕ — ОТДЕЛЬНЫМ СПИСКОМ, даже если оно стояло в задании.** Удаление, перезапись, переименование, перемещение, `git reset`/`checkout` поверх несохранённого, любая правка, вышедшая за зону, — каждое ОДНОЙ строкой: **что · где · чем восстанавливается** (хэш коммита, путь к бэкапу). Ты запущен без запроса разрешений (`--dangerously-skip-permissions`): владелец НЕ видел ни одного из этих действий в момент, когда оно происходило, и этот список — единственное место, где он о них узнаёт. **Необратимого не было — напиши «необратимого нет».** Молчание от пустоты не отличается, и приёмка прочитает его как пустоту.

🔴 **ПОВТОРЯЕМОСТЬ находок — назови, какие из них повторятся на СЛЕДУЮЩЕЙ единице работы** (лекция/слайд/заход). Критерий вычислимый, не про приоритет: повторится — это НЕ пункт очереди, а заход ДО следующего прогона (правило «класс НЕМЕДЛЕННОЕ», `../../docs/kak-delat/RUKOVODSTVO-zahodami.md`). Не повторится — законно уходит в `## ВОПРОСЫ` пунктом очереди. *Пример владельца: белый фон иллюстраций повторился бы тринадцать раз, каждый раз ценой переделки картинки — заход, а не запись; число, вписанное аналитиком не глядя, на следующих слайдах не повторяется — запись, а не заход.* Находка сделана ПРОБНЫМ прогоном — чинится ДО следующего прогона: «проба, после которой ничего не починили, — потраченные токены».

## ⚠️🔴 WARNING · ПОСЛЕДНИЙ ХОД ПЕРЕД ОТЧЁТОМ — ПОЛНАЯ ГИТ-ГИГИЕНА. НЕ ПРОПУСКАТЬ 🔴⚠️

**СТОП. Прежде чем писать хоть строку в `## ОТЧЁТ` — прогони это целиком.** (история цены — `/sessions/rcw-018aaowdc3vczyubvpqz3dee/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц15) Гит-контур §0.1 стоит в НАЧАЛЕ и разбирает то, что накопилось ДО тебя; этот блок
стоит в КОНЦЕ и разбирает то, что накопил ты сам. Один другого не заменяет.

**ПОРЯДОК ЖЁСТКИЙ, ОН НАЗВАН ВЛАДЕЛЬЦЕМ: коммит → влитие своей ветки в основную → пост-проверка
ИЗ ГЛАВНОЙ ПАПКИ → гашение → вывоз.** Обратный порядок не работает технически: влитие отказывает
на грязном дереве, пост-проверка неисполнима до влития, вывоз — на невлитом. (история цены — `/sessions/rcw-018aaowdc3vczyubvpqz3dee/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц16) — теперь вливает САМ заход, но только при зелёной пост-проверке.

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
Branch is `arka/mat-kostyak` (checked). No amendments (ПРАВКИ: «<правок нет>»). Entry: 122 dirty lines, 0 unpushed, 1 unmerged `zahod/*` (`zahod/istoriya-sessij`, valve open by analyst).
1. Launch ONE git-contour subagent with the printed task. Decision on the template conflict (поправка (в)): I tell it NOT to commit anything from the item-2 list nor `KARTA.md`/`UROKI-FABRIKE.md` (those are my commits 1–4 and must stay out of its hands); it only takes the Cowork tail outside my zone, merges nothing, closes nothing.
2. Steps 0–7 exactly as written: diff sanity check, one `.gitignore` insertion with both check-ignore probes (stop+revert if student path not ignored), commits 1–3 in materials with exclude of `UROKI-FABRIKE.md`, export, commit 4 in disciplina (`build_doc.py` only), export.
3. Hygiene Г1–Г6 + final block, then report. Own branch is the working branch (no worktree), so the «merge own branch» step is a no-op: branch == main working branch; I will state that in the report.
No objections to the readiness criterion.

## ВОПРОСЫ — (заполняет исполнитель)
> Нашёл вещь, которая принадлежит чужому дому (термин/источник/урок/следующий заход) — не только вопрос владельцу? Оформи ПУНКТОМ ОЧЕРЕДИ, тремя строками:
> ```
> N. <текст находки>
>    ДОМ: <путь от корня репозитория | владелец>
>    ДОСТАВЛЕНО: нет
> ```
> 🔴 **`ДОМ:` — ОБЯЗАТЕЛЬНОЕ ПОЛЕ, И АДРЕС В НЁМ ОБЯЗАН СУЩЕСТВОВАТЬ В МОМЕНТ, КОГДА ТЫ ЕГО ПИШЕШЬ.** Путь, которого нет на диске, — не адрес: такую запись нельзя ни доставить, ни спросить, и она не чинится ничем. (история цены — `/sessions/rcw-018aaowdc3vczyubvpqz3dee/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц17) Проверить СВОЙ файл до отчёта — одна команда:
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
> с заявленным; расходится — красный НЕЗАВИСИМО от галочки. (история цены — `/sessions/rcw-018aaowdc3vczyubvpqz3dee/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц18)
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
```
<сюда — вывод, дословно>
```

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

## СОВЕТ ПРИ СБОРКЕ (`statistika_zahodov.py --sovet`, М-2)
rod=instrumenty · putey_zony=7 · simvolov=36827 · rc=0
```
MODEL: besplatnaya
   принято 4 of 7 in the cluster «rod=instrumenty, zone paths 4+» = 57%
   OBSERVATIONS: 7 (on besplatnaya passes inside the cluster)   95% interval 25-84%
   whole cluster: принято 8 of 16 = 50%
      besplatnaya  принято   4 of 7    57.1%  <- advised
      sonnet       принято   3 of 7    42.9%
      opus         принято   1 of 2    50.0%  (too few to rest on)
   the cheapest class is also the best-scoring one here.
   caveat: rod is the tool's own inference, not a declared value, for 8 of the 16 passes in this cluster (rule: zone has a .py/.sh path or lives in _generator/tools -> instrumenty; otherwise a skills/ path -> suzhdenie; otherwise -> mehanika)
   🔴 THE MODEL IS NOT THE BINDING CONSTRAINT HERE. This cluster accepts at 50% against a corpus base rate of 80%, and no model class inside it does better than the others. On this corpus the feature that moves the outcome is the SIZE OF THE ZONE, so the lever is to split the pass, not to buy a more expensive model.
   (--simvolov 36827 sits below 132 of 143 measured task sizes; it does NOT narrow the cluster - task length did not separate the outcome on this corpus, see --analiz)
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

**ВЕТКА РАБОТЫ:** `arka/mat-kostyak`
ветки не было: <почему работа шла прямо на основной ветке `arka/mat-kostyak`>
*(проверяется фактом, не словом: ветка обязана существовать и быть либо ВЛИТА в основную, либо названа в открытой заявке на влитие. Ни того, ни другого — Г14 краснеет. Снять состояние: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py poteri --branch <ветка>`)*

**ЗАЯВКИ, ПОСТАВЛЕННЫЕ ЭТОЙ ПРИЁМКОЙ — ПРОДУБЛИРУЙ СЮДА ТО, ЧТО УЖЕ ЛЕЖИТ В СПИСКЕ:**
> Адрес списка: `/Users/ivanyakovlev/Documents/GitHub/materials/_studio/zhurnal/_INFRA-git/zayavki`
> Читается командой (из любой папки, в том числе из worktree): `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py zayavki`
> Ставится командой: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py zayavka --rod <git-operaciya|pravka-koda> "<текст>"`
> 🔴 Вопрос здесь НЕ «что ты хочешь сделать», а «что ты УЖЕ положил в очередь». Дубль сверяется с очередью по id машинно; намерение сверить не с чем.

- `<id заявки>` — `<род>` — `<суть одной строкой: влитие / коммит / вывоз / деплой / гашение>`

*(Заявок эта приёмка не ставила — так и напиши строкой «заявок нет: <почему ни одна из пяти операций не понадобилась>». Пустая строка и прочерк не принимаются: молчание неотличимо от «забыл».)*
