# Канал исполнителя — predskazanie-fakt (один заход до конца)
> Твой единственный файл-заход. Читай ТОЛЬКО его и названные якоря; проект не изучай.
<!-- собран bootstrap_zahod.py -->
<!-- гейт сборки заполненного: ЖДЁТ -->
> План/вопросы/отчёт — в секции внизу. Метрика — КАЧЕСТВО. Часы — норма.
> **Модель: Sonnet 5** — два скрипта и гейт табло по полной спецификации, проверка живым прогоном и регрессией табло.

## СТАРТОВОЕ СООБЩЕНИЕ ВЛАДЕЛЬЦУ

> Это блок для владельца — то, чем тебя запустили. Исполнителю здесь делать нечего, твоё задание ниже.

```
Модель: Sonnet 5 — два скрипта и гейт табло по полной спецификации, проверка живым прогоном и регрессией табло.

Ты исполнитель в репозитории /Users/ivanyakovlev/Documents/GitHub/materials.

Твой единственный вход — файл-заход:
/Users/ivanyakovlev/Documents/GitHub/materials/diskmat-57/2026-10-11_bank-zadach/kod_predskazanie-fakt.md

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
🔴 снимок при сборке 2026-10-11, ПРОВЕРЬ ПЕРВЫМ ХОДОМ: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/schet_nezakrytogo.py diskmat-57/2026-10-11_bank-zadach`
Область: «diskmat-57/2026-10-11_bank-zadach» — сужены пункты 1, 3, 4; долги (2) глобальны намеренно (DOLG.md не размечен по записям).
Приоритет владельца: разобрать инциденты важнее, потом закрыть долги — неразобранный инцидент это повторяющаяся ошибка, долг может подождать.
  1. инцидентов без вердикта             : 0
  2. долгов СТАТУС: ЖИВ                  : н/д — ни одного skills/*/DOLG.md нет на диске (другой git-репозиторий)
  3. уроков фабрике без ВЕРДИКТ          : 1
  4. пунктов очереди «ДОСТАВЛЕНО: нет»   : 0

КОНТЕКСТ. У каждого занятия 7И есть папка итерации `diskmat-57/2026-08-18_logika-goda-7/iteracii/<дата>_<тема>/` с табло этапов (`mashina-listka/tablo.py` по `ITERACIYA.json`). В табло есть «Ф9 прогноз по пунктам ДО урока» и «Ф14 разбор: прогноз против факта», но они необязательные и не машинные: 29.09 прогноз «не записан (пропуск)», 6.10 не было ни прогноза, ни сверки. Цель занятия — каждому аватару (СН · Ни · Ц · В) решаемость 50–80 %. Аватары и отметки живут в выгрузке бота (`bot-7i/data/vygruzka.db`, таблицы `otmetki` и `avatary` — последнюю вводит заход `diskmat-57/2026-10-11_bot-7i/kod_avatary-v-bote.md`). ЦЕЛЬ: процедура «ПРЕДСКАЗАНИЕ до урока → автоматическая сверка с фактом после», которую нельзя пропустить молча; шкала решаемости в банке, начиная с истории.
Приёмка — по ОТЧЁТУ, без построчной сверки. Если стоп до цели: порядок — (1) шкала из истории → (2) ПРЕДСКАЗАНИЕ → (3) сверка → (4) гейт табло и описание процедуры; стоп после (1) — шкала есть, процедуры нет.

## ЧТО ФИНАЛИЗИРОВАНО НА ИНТЕРВЬЮ

ИНТЕРВЬЮ ПРОВЕДЕНО: да (2026-10-11) — флаг `--intervyu da` при сборке. ⚠ Он доказывает, что аналитик не ЗАБЫЛ про интервью, и НЕ доказывает, что разговор был.

1. На каждое занятие — папка; ПРЕДСКАЗАНИЕ собирается генератором до урока; результаты после урока — в ту же папку, сверка «где ошиблись» автоматически; оформить процедурой (владелец 21:36)
2. Цель — решаемость 50–80 % для каждого аватара СН · Ни · Ц · В (владелец 21:10, 21:24)
3. Шкала трудности должна быть уже сейчас — из первого месяца (владелец 21:24)

## КОНТРАКТ ЗОНЫ (обязателен — не удалять; вписан Cowork)
- **МЕСТО РАБОТЫ:** ветка `arka/mat-kostyak` в основной папке. 🔴 Она должна УЖЕ стоять. НЕ на ней — СТОП, НЕ делай `git checkout`: в общей папке он МОЛЧА откатывает дерево к состоянию ветки (цена 27→28.07: файл сильно откатился ночью, поймал владелец вручную; след в git НЕ остаётся). Тогда заход пересобрать с `--worktree`. Ветку не переключай, в другие НЕ коммить.
- **ЗОНА (можно менять):** `diskmat-57/mashina-listka/tablo.py` `diskmat-57/mashina-listka/novaya.py` `diskmat-57/mashina-listka/predskazanie.py` `diskmat-57/mashina-listka/sverka.py` `diskmat-57/mashina-listka/MASHINA.md` `diskmat-57/bank-7i/reshaemost.csv` `diskmat-57/2026-10-11_bank-zadach/kod_predskazanie-fakt.md`. Всё вне — **READ-ONLY**: не править, не двигать, не удалять, не рефакторить «заодно».
- 🔴 **ЗАВЁЛ НОВЫЙ `.md` — РЕГИСТРИРУЕШЬ ЕГО САМ, ТЕМ ЖЕ ХОДОМ, ОДНОЙ КОМАНДОЙ:** `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/register_doc.py <путь> "<описание>"` (из корня репо). `_studio/docs/` тебе по-прежнему READ-ONLY **для правки руками** — дверь ровно одна, и это она. Дверь идемпотентна (повторный вызов дубля не заведёт) и отказывает на пути вне `_studio/`, на несуществующем файле и на пустом описании. Свой файл-заход регистрировать не нужно: он рождается зарегистрированным из `bootstrap_zahod.py`. **Красный хук на ТВОЁМ новом `.md` — это не повод для `--no-verify`, а повод позвать дверь.** *(история цены — `/sessions/rcw-01xfpyot2jrsvxhgj5h3pmvp/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц1) Обходить больше нечего.*
- **КОММИТ:** два хода — `add` по своим путям, затем `commit` **с теми же путями после `--`** (полная форма и цена каждого хода — §4); коммить ПО ХОДУ работы, не одним последним ходом (§4). НИКОГДА `-A` / `.` / `commit -am`, и никогда `commit` без путей. Субагенты не коммитят. **`--no-optional-locks` обязателен:** обычный git переписывает индекс, берёт `.git/index.lock` и роняет параллельный ручной коммит владельца.
- **SCRATCHPAD — ТОЛЬКО ЛИЧНЫЙ.** Черновики, выкладки, промежуточные версии — в личную папку СВОЕГО захода `scratchpad/predskazanie-fakt/`. Общие пути (`scratchpad/otchet.md`, любой `scratchpad/*` без имени твоей темы) ЗАПРЕЩЕНЫ: чужой отчёт уедет в твой файл или твой — в чужой, а приёмка читает отчёт без построчной сверки и подмену НЕ ЛОВИТ по построению. (история цены — `/sessions/rcw-01xfpyot2jrsvxhgj5h3pmvp/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц2)
- 🔴 **Звал `register_doc.py` — допиши `_studio/docs/KARTA.md` к своим путям В ОБОИХ ходах.** Строка регистрации лежит физически в нём. Ворота 5 читают `§6` **с диска**, а не из индекса: коммит без этого файла пройдёт ЗЕЛЁНЫМ, документ уедет сиротой, а строка умрёт при первом `checkout` (история цены — `/sessions/rcw-01xfpyot2jrsvxhgj5h3pmvp/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц3).
- **ЗАПРЕТ:** ничего за пределами зоны, даже если «мешает» или «чинится в одну строку». Нашёл проблему вне зоны → в отчёт, не трогай.

## 0. ПЕРВЫЙ ХОД
### 0.1 🔴 ГИТ-КОНТУР — ДО ВСЕГО ОСТАЛЬНОГО, И ПЕРВЫМ ХОДОМ ЦЕЛИКОМ

🔴 «ничего сверх задачи» относится к СОДЕРЖАНИЮ работы; git-контур §0.1 — законное исключение, он про состояние репозитория и исполняется целиком.

🔴 **ПОРЯДОК ЗДЕСЬ — ЧАСТЬ УСТРОЙСТВА, А НЕ ОФОРМЛЕНИЕ. Сначала субагент вливает названные через `--vlit` ЧУЖИЕ ветки В ОСНОВНУЮ, и только ПОТОМ ты заводишь свою рабочую папку; СВОЮ ветку он не трогает никогда — её вливаешь ты сам последним ходом (граница прав ниже).** (история цены — `/sessions/rcw-01xfpyot2jrsvxhgj5h3pmvp/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц5) Заводя ветку ПОСЛЕ влития, ты отпочковываешь её от основной, которая уже всё содержит: инструмент оказывается на диске сам, дотаскивать нечего.

🔴 Очередь заявок подметена на входе волны, твоё дело здесь — только своя зона: закрывает и вливает очередь роль коммитера (`agents/kommiter.md`), один раз на входе волны и один раз на выходе (`python3 _generator/tools/bootstrap_zahod.py --podmetanie-volny vhod|vyhod`), не сборка этой позиции.

**1. ВЕСЬ КОНТУР — В СУБАГЕНТА, ОДНИМ ХОДОМ, ДО СВОЕЙ ПАПКИ.** Влитие названных веток в ОСНОВНУЮ, что забрать в git по ходу и что погасить после — на содержание твоей задачи не влияют. Запусти ОДНОГО субагента, дождись его и вставь его пять строк в `## ОТЧЁТ` дословно; сам эти пункты не исполняй. 🔴 ПОРЯДОК ПРИ ПАДЕНИИ ЭТОГО ВЫЗОВА — исполняй, не изобретай (движок роняет `network_error` на вызове субагента и уносит с собой ВЕСЬ заход, замер волны 3A — 4 захода из 13). Пауза 45 секунд, до трёх попыток; время меряй `date`, не суммой своих `sleep`. После третьей — работай БЕЗ субагента: контур остаётся неразобранным, и это ОТДЕЛЬНАЯ строка в `## ОТЧЁТ`, а не молчание. У него ОТДЕЛЬНЫЕ ПРАВА, объявленные в его же промпте: главная папка, основная ветка, вывоз — и ничего сверх; зону захода он не коммитит, её коммитишь ты сам, по ходу работы (§4). 🔴 ОТВЕТ ЛЮБОГО субагента, которого ты запускаешь (не только этого), обязан КОНЧАТЬСЯ строкой «выдано N позиций из M найденных»: канал мог оборвать его молча, и без этой строки усечение неотличимо от честного «мало нашлось». Нет строки — ответ усечён, в `## ОТЧЁТ` не вставляй, перезапроси. Полный текст задания печатает команда:
```
python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/bootstrap_zahod.py --zadanie-subagentu --zone diskmat-57/mashina-listka/tablo.py --zone diskmat-57/mashina-listka/novaya.py --zone diskmat-57/mashina-listka/predskazanie.py --zone diskmat-57/mashina-listka/sverka.py --zone diskmat-57/mashina-listka/MASHINA.md --zone diskmat-57/bank-7i/reshaemost.csv --zone diskmat-57/2026-10-11_bank-zadach/kod_predskazanie-fakt.md --kommitit 'свою зону в materials по ходу' --zakryt 'ничего: ветка arka/mat-kostyak остаётся'
```

🔴 ГРАНИЦА ПРАВ, ТРИ ОТВЕТА (та же, что в самом задании субагенту — одно место в тексте, а не пересказ): **кто вливает ЧУЖИЕ названные (`--vlit`) ветки** — субагент, в ОСНОВНУЮ ветку, до заведения твоей папки; **кто вливает СВОЮ ветку этого захода** — ты сам, последним ходом, после коммита зоны (`git_zona.py vlit-v-osnovnuyu`; (история цены — `/sessions/rcw-01xfpyot2jrsvxhgj5h3pmvp/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц6)); **кто коммитит пути ВНЕ зоны захода** — субагент (хвост Cowork и что назовёт пункт 3 его задания). Очередь заявок эту границу больше не касается — её закрывает роль коммитера на границе волны, не субагент этой позиции. Ты коммитишь ТОЛЬКО зону этого захода, по ходу работы (§4). 🔴 Конфликт на `README.md` при ЛЮБОМ слиянии разрешается ОБЪЕДИНЕНИЕМ записей реестра, НИКОГДА выбором стороны: параллельные заходы волны дописали в реестр по строке — обе записи правы, выбор одной молча уничтожает регистрацию соседа.

**2. ТЕПЕРЬ ЗАВОДИ СВОЮ РАБОЧУЮ ПАПКУ** (команда — в блоке «МЕСТО РАБОТЫ» выше) и работай в ней как обычно. Её ветка отпочкована от свежей основной, поэтому инструмент, которым ты работаешь, уже на диске — отдельного «влить перед работой» больше нет.

Невлитых `zahod/*`-веток, НЕ покрытых `--vlit`, — 1: `zahod/istoriya-sessij` — 🔴 снимок при сборке 2026-10-11, ПРОВЕРЬ ПЕРВЫМ ХОДОМ: `git --no-optional-locks branch --no-merged arka/mat-kostyak | grep -c 'zahod/'`. 🔴 КЛАПАН ОТКРЫТ АНАЛИТИКОМ, причина дословно: «zahod/istoriya-sessij — чужой заход другой темы». Заход собран ВОПРЕКИ невлитому этой веткой — отключение видно здесь, в артефакте, а не осталось решением в голове аналитика (§79 канона: невлитая ветка законна, рядом может идти чужой заход).


- деплоя в этом заходе нет.

- Проверь ветку: `git branch --show-current` — обязано быть `arka/mat-kostyak`. Не она — СТОП, `git checkout` НЕ делай (§4 GIT-disciplina), нужен `--worktree`.
- Точка отката: `git add diskmat-57/mashina-listka/tablo.py diskmat-57/mashina-listka/novaya.py diskmat-57/mashina-listka/predskazanie.py diskmat-57/mashina-listka/sverka.py diskmat-57/mashina-listka/MASHINA.md diskmat-57/bank-7i/reshaemost.csv diskmat-57/2026-10-11_bank-zadach/kod_predskazanie-fakt.md` → commit (или zip), если зона не чиста в HEAD (не фабрикуй, если чиста).
- Прочитать ТОЛЬКО:
  - `/Users/ivanyakovlev/Documents/GitHub/materials/diskmat-57/mashina-listka/MASHINA.md`, `/Users/ivanyakovlev/Documents/GitHub/materials/diskmat-57/mashina-listka/tablo.py`, `/Users/ivanyakovlev/Documents/GitHub/materials/diskmat-57/mashina-listka/novaya.py`, `/Users/ivanyakovlev/Documents/GitHub/materials/diskmat-57/mashina-listka/svod.py` (как сейчас сводится сдача);
  - пример итерации: `/Users/ivanyakovlev/Documents/GitHub/materials/diskmat-57/2026-08-18_logika-goda-7/iteracii/2026-10-06_kontrolnaya-i-chetnost/ITERACIYA.json` и `TABLO.md`; старый прогноз в другом формате — `/Users/ivanyakovlev/Documents/GitHub/materials/diskmat-57/2026-08-18_logika-goda-7/prognoz.py`;
  - бот (READ-ONLY): `/Users/ivanyakovlev/Documents/GitHub/bot-7i/bot7i/db.py` (таблицы `punkty`, `otmetki`, `sdacha`, `avatary`), `/Users/ivanyakovlev/Documents/GitHub/bot-7i/katalog.yaml` (работы и их даты);
  - канон: `/Users/ivanyakovlev/Documents/GitHub/materials/diskmat-57/2026-10-11_bank-zadach/KANON-podbora-zadach.md` §3–§6; аналитический скрипт-образец сверки по аватарам (только как образец счёта, не копировать как есть): `/Users/ivanyakovlev/Documents/GitHub/bot-7i/tmp-skriny/avatary_analiz.py`.
- ПЛАН — в `## ПЛАН` перед действиями.

## 1. ДИСЦИПЛИНА (Карпатов)
🔴 **Развилку ВНУТРИ своей зоны решаешь сам** — называешь решение в `## ПЛАН` и идёшь дальше; спрашивать и ЖДАТЬ ответа владельца — только там, где любой выбор делает работу опасной или бессмысленной. Целый прогон уже вставал на вопросе, ответ на который лежал в собственном контракте зоны исполнителя (урок арки `2026-08-20_poryadok-v-metaskillah`).
🔴 **Не собирай `rm` с путём из переменных.** Защитный слой перехватывает такие команды НЕЗАВИСИМО от Bypass permissions и останавливает работу до ответа человека — замер 20.09: 5 ч 48 мин при работающей машине. Вместо `cp X Y && rm X` пиши `mv X Y`; где не подходит — питон-скрипт ФАЙЛОМ, не однострочник с `rm`.
🔴 **Код возврата — ПЕРВЫМ, до содержательного вывода команды.** «Отработала» и «упала, а я читаю прошлое состояние» выглядят одинаково; сначала `echo $?`, потом выводы. То же с гейтами. (история цены — `/sessions/rcw-01xfpyot2jrsvxhgj5h3pmvp/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц7)
Предпосылки/развилки назвать вслух; минимум без спекуляций; хирургия (строка → к заданию); критерий, который может провалиться. Якорные замены — abort при ≠1. Сохранять по умолчанию. **Оспорить ложную предпосылку — включая КРИТЕРИЙ ГОТОВНОСТИ: считаешь его кривым — скажи в `## ПЛАН`, ДО работы, и предложи поправку.** Субагенты: ≤5, рейт-лимит = отступить + доложить (не слепой ретрай).

🔴 **Пишешь содержательный текст — термин НЕ употребляется раньше, чем определён**, включая заголовки, подводки и формулировки теорем. «Определение в тексте есть» не считается: если оно ниже первого рабочего употребления, читатель встаёт ровно там. Чинится ПЕРЕСТАНОВКОЙ определения вверх, не дописыванием пояснения. Гейт: `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/check_termin.py <src>` (exit 1 при нарушении). Канон — `../docs/kak-delat/STANDART-teksta.md` правило 11. (история цены — `/sessions/rcw-01xfpyot2jrsvxhgj5h3pmvp/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц8)

## 2. ЗАДАЧА

🔴 **WRITE YOUR `## ОТЧЁТ`, `## ПЛАН` AND `## ВОПРОСЫ` IN ENGLISH, AND EVERY FILE AND EVERY COMMIT MESSAGE YOU PRODUCE TOO.** Owner's decision 30.08. It is a каркас-level rule, not a preference (история цены — `/sessions/rcw-01xfpyot2jrsvxhgj5h3pmvp/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц9). Fixed Russian addresses stay Cyrillic: `ЦЕНА:` · `ВЕРДИКТ:` · `ДОМ:` · `ДОСТАВЛЕНО:` · `ПОДЪЁМ:` · `[ДОЛГ: …]` · every `## ` heading of this file · every path and command.
**Порядок запуска:** этот заход — ПОСЛЕ `kod_avatary-v-bote.md`. Нет таблицы `avatary` в выгрузке — СТОП, строка в ОТЧЁТ.

**Часть 1. Шкала решаемости из истории — `diskmat-57/bank-7i/reshaemost.csv`.**
- Колонки: `rabota_id, punkt, uroven_punkta, avatar, reshili, pisali, dolya, popytki_sred, na_datu, istochnik`. `pisali` — дети аватара, писавшие работу (КР/ДЗ — статус «сдал»; листок — хотя бы один «+» на листке); `dolya = reshili / pisali`; пустые клетки листка — «не решил» (строгий режим), это записать в шапке файла-описания.
- Заполняется скриптом `/Users/ivanyakovlev/Documents/GitHub/materials/diskmat-57/mashina-listka/sverka.py --shkala` по выгрузке бота для всех работ с 22.09; идемпотентно (повторный прогон не дублирует строки). Детей в файле нет — только агрегаты по аватару.

**Часть 2. ПРЕДСКАЗАНИЕ — `/Users/ivanyakovlev/Documents/GitHub/materials/diskmat-57/mashina-listka/predskazanie.py`.**
- `predskazanie.py zagotovka <папка итерации> <rabota_id> …` кладёт в папку `PREDSKAZANIE.csv`: по строке на пункт работы (`rabota_id, punkt, uroven, СН, Ни, Ц, В, istochnik_ocenki, kommentarij`), колонки аватаров пустые; список пунктов — из `katalog.yaml`/выгрузки или, если работы там ещё нет, из файла пунктов, который аналитик положит в папку (формат назови в MASHINA.md). Если в `reshaemost.csv` есть тот же пункт (якорь) — подставляет факт как подсказку в `kommentarij`.
- `predskazanie.py proverit <папка>`: все доли заполнены числами 0–1, у каждого пункта; печатает по аватару ожидаемую решаемость трека ○ и трека △ и предупреждает, если вне 50–80 %. Рядом генерирует `PREDSKAZANIE.md` (читаемая таблица).
- Предсказание «до урока» доказывается гитом: коммит `PREDSKAZANIE.csv` раньше начала пары (`nachalo` в `ITERACIYA.json`, например `"2026-10-13T15:30"`; поля нет — `proverit` требует его завести).

**Часть 3. Сверка — `/Users/ivanyakovlev/Documents/GitHub/materials/diskmat-57/mashina-listka/sverka.py <папка итерации>`.**
- Читает `PREDSKAZANIE.csv` и выгрузку бота (путь по умолчанию — `bot-7i/data/vygruzka.db` рядом с `materials`; ключ `--vygruzka`). Пишет в ту же папку `SVERKA.csv` (пункт × аватар: прогноз, факт, писали, ошибка) и `SVERKA.md`: по аватару средняя ошибка и сдвиг (прогноз выше/ниже факта), доля пунктов в 50–80 % по факту, список промахов больше 20 п. п.; дописывает факт в `reshaemost.csv`.
- Мало писавших в аватаре (< 2) — клетка «нет данных», не 0 и не 100 %.

**Часть 4. Гейт и процедура.**
- `tablo.py`: Ф9 — артефакт `PREDSKAZANIE.csv`, «готово» только при зелёном `predskazanie.py proverit`; Ф14 — артефакт `SVERKA.md`. Красное (выход ≠ 0, строка ❗): пара началась (`nachalo` прошло), а предсказания нет; отметки работ итерации в выгрузке есть, а сверки нет. Статус «не нужно» для Ф9/Ф14 запрещён (табло краснеет) — пропустить молча нельзя.
- `novaya.py`: новая итерация получает поле `nachalo` и новые артефакты Ф9/Ф14.
- Раздел в `/Users/ivanyakovlev/Documents/GitHub/materials/diskmat-57/mashina-listka/MASHINA.md` «Занятие: предсказание → факт» — процедура по шагам (кто, когда, какой командой): собрали листок → `zagotovka` → аналитик ставит доли по аватарам (опираясь на `reshaemost.csv` и якоря) → `proverit` → коммит до пары → урок → выгрузка бота → `sverka.py` → табло зелёное.
- Папку `iteracii/2026-10-13_arifmetika/` НЕ трогать (в ней работает параллельная сессия).

**Чего НЕ делать:** не придумывать прогнозы задним числом для прошлых работ (сверка прошлого — только тестом, вне папок итераций); не трогать бот; не класть детей в `reshaemost.csv` и в любые файлы materials.

**КРИТЕРИЙ ГОТОВНОСТИ (может ПРОВАЛИТЬСЯ):** живой прогон на реальном объекте:
1. `sverka.py --shkala` по живой выгрузке → `reshaemost.csv` со строками для всех пунктов 7 работ с 22.09 × 4 аватара; повторный прогон — то же число строк (команда и числа в ОТЧЁТ);
2. тестовый прогон в личном scratchpad: копия папки итерации 6.10 + синтетический `PREDSKAZANIE.csv` (помечен ТЕСТ) по КР2 → `SVERKA.md` с ошибками по аватарам, числа перепроверены вторым независимым счётом;
3. `tablo.py` на копии итерации без предсказания после `nachalo` → выход ≠ 0 и ❗; с предсказанием и сверкой → зелёное;
4. регрессия: `tablo.py` на реальных итерациях 29.09 и 6.10 печатает то же, что раньше, кроме новых строк Ф9/Ф14 (их красное — ожидаемо, это прошлые пропуски; назвать в ОТЧЁТ).
**Отрицательный вердикт несёт ОХВАТ В СЕБЕ:** не «дыр не найдено», а «дыр не найдено, проверено X из Y». Без охвата вердикт не принимается — «проверено 2 из 9» и «проверено 9 из 9» выглядят одинаково.

## 3. ВЕРИФИКАТОР (если двигаем/теряем/жмём)

Верификатор нужен, тип — **ПОСЛЕ-типа** — судит результат, стоит в конце, после задачи. Свежий субагент, ДРУГИМ методом (живой прогон на реальном объекте: шкала по живой выгрузке бота, тестовая сверка КР2 пересчитана вторым независимым счётом свежим субагентом; гейт табло — красный без предсказания и зелёный с ним), не перечитывает свою же правку. Доля сплошной выборки: все пункты 7 работ × 4 аватара в шкале; тестовая сверка — все 21 пункт КР2. Финальная строка ответа обязательна дословно: «выдано N позиций из M найденных» — без неё ответ считается усечённым и в отчёт не вставляется.

## 4. 🔴 КОММИТ СВОЕЙ ЗОНЫ — ПО ХОДУ РАБОТЫ, НЕ ОДНИМ ПОСЛЕДНИМ ХОДОМ
Ты работаешь host-side и в `.git` ПИШЕШЬ — значит коммитишь САМ, никому не передавая. Каждую завершённую часть работы коммить СРАЗУ, теми же двумя ходами — не копи всё к финальному ходу:
```
git --no-optional-locks add -- diskmat-57/mashina-listka/tablo.py diskmat-57/mashina-listka/novaya.py diskmat-57/mashina-listka/predskazanie.py diskmat-57/mashina-listka/sverka.py diskmat-57/mashina-listka/MASHINA.md diskmat-57/bank-7i/reshaemost.csv diskmat-57/2026-10-11_bank-zadach/kod_predskazanie-fakt.md                     # вводит НОВЫЕ пути в индекс
git --no-optional-locks commit -m "<зона>: <что сделано>" -- diskmat-57/mashina-listka/tablo.py diskmat-57/mashina-listka/novaya.py diskmat-57/mashina-listka/predskazanie.py diskmat-57/mashina-listka/sverka.py diskmat-57/mashina-listka/MASHINA.md diskmat-57/bank-7i/reshaemost.csv diskmat-57/2026-10-11_bank-zadach/kod_predskazanie-fakt.md   # отсекает всё чужое
python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone <зона>   # из корня репо; должен быть ✅
git --no-optional-locks show --stat                        # обязаны быть ТОЛЬКО твои пути
```
🔴 **КОММИТЬ ПО ХОДУ — РЕШЕНИЕ ВЛАДЕЛЬЦА 25.08 (В11), ПЕРЕВЕРНУВШЕЕ прежний канон «одним последним ходом».** (история цены — `/sessions/rcw-01xfpyot2jrsvxhgj5h3pmvp/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц10) Закончил кусок — закоммитил его; последний ход только ПРОВЕРЯЕТ, что коммитить нечего (`git status --porcelain` пуст, `git_zona.py check --zone` ✅).
🔴 **ОБА хода обязательны, ни один не лишний** (полное «почему» и цена — `../docs/kak-delat/GIT-disciplina.md §3`):
- **`add`** — pathspec-коммит знает только **отслеживаемые** пути; новый файл без `add` даёт `did not match any file(s) known to git`.
- **`-- <пути>` в самом `commit`** — иначе `commit` забирает индекс ЦЕЛИКОМ, вместе с чужим, застейдженным кем угодно рядом с тобой (репо `materials/` общий, писателей трое). (история цены — `/sessions/rcw-01xfpyot2jrsvxhgj5h3pmvp/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц11)
⚠ **Хук `pre-commit` покраснел — сначала посмотри, на ЧЬИХ путях.**
- Красное на ТВОИХ путях (новый `.md` не зарегистрирован в `../../docs/KARTA.md §6`, битая ссылка) — **чини, не обходи**: там только твоё, обходить нечего.
- Красное на ЧУЖОМ, унаследованном долге (ворота дают сотни ❌ старых нарушений) — законный обход, но ТОЛЬКО с причиной; голый `--no-verify` инструмент отклонит, а причина сама уедет в `INCIDENTY.md`:
```
python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py commit --zone <зона> \
    --no-verify "чужой долг: <что именно покраснело>" -m "<что и зачем>" --push
```
Ту же причину назови отдельной строкой отчёта долгом. (история цены — `/sessions/rcw-01xfpyot2jrsvxhgj5h3pmvp/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц12)
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
> (история цены — `/sessions/rcw-01xfpyot2jrsvxhgj5h3pmvp/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц13)

**ЗОНА ГИГИЕНЫ:** `diskmat-57/mashina-listka/tablo.py` `diskmat-57/mashina-listka/novaya.py` `diskmat-57/mashina-listka/predskazanie.py` `diskmat-57/mashina-listka/sverka.py` `diskmat-57/mashina-listka/MASHINA.md` `diskmat-57/bank-7i/reshaemost.csv` `diskmat-57/2026-10-11_bank-zadach/kod_predskazanie-fakt.md`

- **Г1. Зона доехала в git.** `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone diskmat-57/mashina-listka/tablo.py` → ✅; `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone diskmat-57/mashina-listka/novaya.py` → ✅; `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone diskmat-57/mashina-listka/predskazanie.py` → ✅; `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone diskmat-57/mashina-listka/sverka.py` → ✅; `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone diskmat-57/mashina-listka/MASHINA.md` → ✅; `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone diskmat-57/bank-7i/reshaemost.csv` → ✅; `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/git_zona.py check --zone diskmat-57/2026-10-11_bank-zadach/kod_predskazanie-fakt.md` → ✅. Красное на любой из команд — отчёт не принимается: приёмка гоняет их все первым ходом.
- **Г2. Второй репозиторий.** **неприменимо, и это проверено при сборке, а не предположено:** все пути зоны лежат внутри репозитория `materials` (тот же критерий, что у С2 `check_sborki.py`). Зона расширилась за его пределы по ходу — пункт снова применим; команда та же, что в применимом случае: `cd ../<репозиторий> && git --no-optional-locks status --porcelain` → пусто. *Команда названа и здесь нарочно (находка верификатора): пункт, который объявлен неприменимым и не говорит, ЧТО делать, когда станет применим, исполнить в этот момент нечем.*
- **Г3. Невлитых веток не прибавилось.** `git --no-optional-locks branch --no-merged arka/mat-kostyak` — число сравни с тем, что было на входе. Выросло — назови, чьи ветки и почему они законны.
- **Г4. Новый инструмент имеет живую точку вызова.** Завёл `.py` в `_generator/**` — `python3 /Users/ivanyakovlev/Documents/GitHub/disciplina/_generator/tools/check_tool_contract.py <свои новые файлы>` → rc=0. Ни одного нового `.py` — так и напиши. *Инструмент без точки вызова зелен ровно потому, что его никто не звал.*
- **Г5. Новый `.md` зарегистрирован.** Завёл — звал ли ты `register_doc.py` и лежит ли строка на диске: `grep -c '<имя файла>' <карта своего корня>` → 1. Карту своего корня называет `korni.карта_для('<путь>')`, руками её не угадывай.
- **Г6. В коммите нет чужих путей.** `git --no-optional-locks show --stat` — только твои пути. Чужой путь в своём коммите — это чужая работа, унесённая твоим `commit` без `--`.

## 5. ОТЧЁТ → секция `## ОТЧЁТ` внизу
Что сделал + ЗАЧЕМ / как проверил / что НЕ трогал / вопросы / результат верификатора / открытое «возвращаться» / **время прогона + токены — на канале `app` НЕПРИМЕНИМО, снимать неоткуда** (лог прогона существует только на канале `terminal`, где его кладёт `tee`; сессия в приложении Claude Code такого следа не оставляет). Строку не заполнять числом и не извиняться за его отсутствие — это не недосмотр исполнителя, а свойство канала) / **ПОВТОРЯЕМОСТЬ находок (строка обязательна — см. ниже)** / **АРТЕФАКТ (строка обязательна)** / **КОММИТ (строка обязательна, см. §4)**.

🔴 **АРТЕФАКТ — АБСОЛЮТНЫЙ ПУТЬ К СОБРАННОМУ ФАЙЛУ, отдельной строкой.** Не «колода пересобрана», не «см. `dist/`», а путь, который владелец скопирует и откроет. *(история цены — `/sessions/rcw-01xfpyot2jrsvxhgj5h3pmvp/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц14) Отчёт без адреса артефакта — это отчёт о работе, которую нельзя посмотреть.*

🔴 **НЕОБРАТИМОЕ — ОТДЕЛЬНЫМ СПИСКОМ, даже если оно стояло в задании.** Удаление, перезапись, переименование, перемещение, `git reset`/`checkout` поверх несохранённого, любая правка, вышедшая за зону, — каждое ОДНОЙ строкой: **что · где · чем восстанавливается** (хэш коммита, путь к бэкапу). Ты запущен без запроса разрешений (`--dangerously-skip-permissions`): владелец НЕ видел ни одного из этих действий в момент, когда оно происходило, и этот список — единственное место, где он о них узнаёт. **Необратимого не было — напиши «необратимого нет».** Молчание от пустоты не отличается, и приёмка прочитает его как пустоту.

🔴 **ПОВТОРЯЕМОСТЬ находок — назови, какие из них повторятся на СЛЕДУЮЩЕЙ единице работы** (лекция/слайд/заход). Критерий вычислимый, не про приоритет: повторится — это НЕ пункт очереди, а заход ДО следующего прогона (правило «класс НЕМЕДЛЕННОЕ», `../../docs/kak-delat/RUKOVODSTVO-zahodami.md`). Не повторится — законно уходит в `## ВОПРОСЫ` пунктом очереди. *Пример владельца: белый фон иллюстраций повторился бы тринадцать раз, каждый раз ценой переделки картинки — заход, а не запись; число, вписанное аналитиком не глядя, на следующих слайдах не повторяется — запись, а не заход.* Находка сделана ПРОБНЫМ прогоном — чинится ДО следующего прогона: «проба, после которой ничего не починили, — потраченные токены».

## ⚠️🔴 WARNING · ПОСЛЕДНИЙ ХОД ПЕРЕД ОТЧЁТОМ — ПОЛНАЯ ГИТ-ГИГИЕНА. НЕ ПРОПУСКАТЬ 🔴⚠️

**СТОП. Прежде чем писать хоть строку в `## ОТЧЁТ` — прогони это целиком.** (история цены — `/sessions/rcw-01xfpyot2jrsvxhgj5h3pmvp/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц15) Гит-контур §0.1 стоит в НАЧАЛЕ и разбирает то, что накопилось ДО тебя; этот блок
стоит в КОНЦЕ и разбирает то, что накопил ты сам. Один другого не заменяет.

**ПОРЯДОК ЖЁСТКИЙ, ОН НАЗВАН ВЛАДЕЛЬЦЕМ: коммит → влитие своей ветки в основную → пост-проверка
ИЗ ГЛАВНОЙ ПАПКИ → гашение → вывоз.** Обратный порядок не работает технически: влитие отказывает
на грязном дереве, пост-проверка неисполнима до влития, вывоз — на невлитом. (история цены — `/sessions/rcw-01xfpyot2jrsvxhgj5h3pmvp/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц16) — теперь вливает САМ заход, но только при зелёной пост-проверке.

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
Start state (checked): branch `arka/mat-kostyak`; `avatary` table exists in `bot-7i/data/vygruzka.db` (26 real children: СН 3 · Ни 7 · Ц 7 · В 9; `Н` and test child `t1` excluded); no ПРАВКИ. Entry git-contour done by the subagent (nothing to merge, no Cowork tail).

Decisions inside my zone (named before work):
1. **One shared core.** `sverka.py` holds the single fact function (`fakt(db, rabota_id)` → reshili/pisali per punkt × avatar); `--shkala`, the sverka proper and `reshaemost.csv` all use it, so history scale and post-lesson fact cannot diverge. `predskazanie.py` / `tablo.py` import from it.
2. **`pisali`** per spec: КР/ДЗ — `sdacha.status='sdal'`; sheet / mini-sheet — child with ≥1 «+» on it; empty cell = not solved (strict). **Refinement for works with `alternativy` (КР2 ○/△):** `pisali` of a punkt = those who handed in AND have ≥1 mark («+»/«-») in the same part, otherwise ○ items are diluted by children who chose only △. Marked in `istochnik` (`vygruzka:strogo` / `vygruzka:chast`); strict-only number is not lost (it is a one-line switch). Written in MASHINA.md header of the scale.
3. **`reshaemost.csv` rows** = every punkt of every work since 22.09 with punkty (7 works, 125 punkty ⇒ expect 500 rows) × 4 avatars; `pisali<2` ⇒ row kept, `dolya` empty (not 0). Upsert by key (rabota_id, punkt, avatar), deterministic order ⇒ idempotent. `popytki_sred` stays empty (attempts are not recorded yet, canon §5.6). No children in files, only aggregates.
4. **PREDSKAZANIE.csv** as in the spec; `zagotovka` merges (never overwrites filled values); item list from `punkty` in the db, else from `PUNKTY.csv` in the folder (`rabota_id,punkt,uroven[,yakor]`, format written to MASHINA.md); anchor hint into `kommentarij` from `reshaemost.csv` (same work+punkt, or the `yakor` column `rabota:punkt`).
5. **`proverit`**: content check (numbers 0–1 everywhere, no duplicate/missing punkt, `nachalo` present) ⇒ rc; git proof (the last commit touching the file is earlier than `nachalo`, file clean vs HEAD, naive `nachalo` = Europe/Moscow) is a separate verdict printed by it and demanded with `--git` (the table gate uses it). Per-avatar mean for ○ and △ track with warnings outside 50–80 %.
6. **`tablo.py` gate.** Ф9/Ф14 artefacts forced to `PREDSKAZANIE.csv` / `SVERKA.md` regardless of the old JSON value. Red (❗, rc=1): status «не нужно» on Ф9/Ф14; Ф9 «готово» without a green proverit; no `nachalo` field; `nachalo` passed and no proven prediction; Ф14: works of the iteration (db works with `data` = folder date prefix) have marks and no `SVERKA.md`. Db missing ⇒ visible «не проверено» line, not red. Added only: `--bez-zapisi` (do not rewrite TABLO.md — used for regression on real folders so I do not touch files outside the zone) and `--seychas` (test clock).
7. **`novaya.py`**: new iteration gets `nachalo` (optional 5th arg, default `<date>T15:30`, owner edits) and the new Ф9/Ф14 artefacts (via `tablo.FAZY`).
8. Real iteration folders (29.09, 6.10, 13.10) are not modified; tests run in my scratchpad `scratchpad/predskazanie-fakt/` (copies, own tiny git repo with `GIT_COMMITTER_DATE` for the pre-lesson commit proof).

Criterion remarks: (1) 7 works × 125 punkty × 4 = 500 rows, checked by command; (2) the second independent count — a fresh subagent recomputes all 21 КР2 punkty × 4 avatars from the raw db with its own code; (4) regression run old-vs-new on 29.09 and 6.10 with writes disabled. I see no reason to change the criterion.

Commit order (§4, by parts): (a) sverka.py + shkala + reshaemost.csv · (b) predskazanie.py · (c) tablo/novaya + MASHINA.md · (d) report.

## ВОПРОСЫ — (заполняет исполнитель)
> Нашёл вещь, которая принадлежит чужому дому (термин/источник/урок/следующий заход) — не только вопрос владельцу? Оформи ПУНКТОМ ОЧЕРЕДИ, тремя строками:
> ```
> N. <текст находки>
>    ДОМ: <путь от корня репозитория | владелец>
>    ДОСТАВЛЕНО: нет
> ```
> 🔴 **`ДОМ:` — ОБЯЗАТЕЛЬНОЕ ПОЛЕ, И АДРЕС В НЁМ ОБЯЗАН СУЩЕСТВОВАТЬ В МОМЕНТ, КОГДА ТЫ ЕГО ПИШЕШЬ.** Путь, которого нет на диске, — не адрес: такую запись нельзя ни доставить, ни спросить, и она не чинится ничем. (история цены — `/sessions/rcw-01xfpyot2jrsvxhgj5h3pmvp/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц17) Проверить СВОЙ файл до отчёта — одна команда:
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
> с заявленным; расходится — красный НЕЗАВИСИМО от галочки. (история цены — `/sessions/rcw-01xfpyot2jrsvxhgj5h3pmvp/mnt/GitHub/disciplina/_studio/docs/kak-delat/ISTORII-CEN-zahoda.md` Ц18)
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
rod=instrumenty · putey_zony=7 · simvolov=34919 · rc=0
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
   (--simvolov 34919 sits below 141 of 143 measured task sizes; it does NOT narrow the cluster - task length did not separate the outcome on this corpus, see --analiz)
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
