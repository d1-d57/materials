# МАШИНА ЛИСТКА — спецмат 7И, одна пара в неделю

> **Что это.** Капсула, в которую загружается новая тема, а на выходе получается комплект к паре — контрольная, листок А/Б
> с картой (через занятие), ДЗ, шпаргалка — и после урока свод сдачи. Собрана ночью 29.09 по четырём полным итерациям
> (обратный ход 15.09, логика 23.09, «Комбинаторика 1» 22.09, «Комбинаторика 2» 29.09).
> **Здесь:** как запустить, какая команда на какую фазу, где смотреть «где мы». **Не здесь:** правила формата листка
> (`../2026-08-18_logika-goda-7/FORMAT-listka-po-otvetu.md`), механика карты (`…/KVEST-mehanika.md`), отбор задач
> (`…/METOD-otbora-zadach.md`), процедура по фазам с ценами ошибок (`GitHub/disciplina/zagotovki/listok-7i/SKILL.md`).
> У каждой сущности один дом; здесь — только указатели и команды.
> **Аксиомы вёрстки А1–А13** (приняты владельцем 29.09) — `FORMAT-listka-po-otvetu.md`, раздел «Формат листка — аксиомы»;
> что можно вшить — вшито в `listok_gen.py` (поток с обтеканием, поле по длине ответа, автоподжатие строк, подвал, карта без 4/5,
> контрольная и ДЗ — пол-листа на человека `polulist`, шпаргалка — только номер, вариант, ответ `shpargalka`).

## Через неделю: новая тема за три шага

1. `python3 novaya.py ../2026-08-18_logika-goda-7 2026-10-06 <слаг> "<Тема>"` — заводит папку итерации
   `iteracii/<дата>_<слаг>/`, в ней `ITERACIYA.json` (все фазы, статус «ждёт») и `dannye.py` (шаблон листка).
   Игровое занятие ставится само — **противоположно прошлому** (решение 29.09: геймификация через одно).
2. `python3 tablo.py <папка итерации>` — табло: где мы, что следующее, почему стоим. Печатает `TABLO.md`.
3. Идти по фазам сверху вниз (таблица ниже), после каждой — поправить статус фазы в `ITERACIYA.json` и снова табло.

**Табло — единственный ответ на «где мы».** Фаза «ждёт» или «стоп» без записанного `pochemu` — красная; «готово» без
файла-артефакта — красная (❗). Отметка без файла не считается.

## Фазы → команда → что должно появиться

| фаза | что делаем | команда / инструмент | артефакт | гейт |
|---|---|---|---|---|
| Ф0 | интервью владельца: тема, рамка, числа, игровое ли | вопросы с полными условиями, по одной строке ответа | ответы дословно → `INTERVYU.md` итерации; решения → `docs/RESHENIYA.md` | решения записаны в момент ответа |
| Ф1 | замер прошлой итерации | `svod.py <прошлая итерация>` | `SVOD.md` прошлой | прогноз против факта поштучно |
| Ф2–Ф3 | числа; границы темы: объект в ОТВЕТЕ; словарь идей | `METOD-otbora-zadach.md` | `SLOVAR-idej.md` | запрещённое проверяется по РЕШЕНИЮ |
| Ф4–Ф6 | пул → скелет → отбор → **утверждение блоками** | карточки, жадное покрытие словаря | состав в дневнике | владелец видит полные условия; блоки: контрольная → ○ → △ → доп → карта → ДЗ → шпаргалка |
| Ф7 | ответы перебором | функции в `dannye.py` итерации | `out/kanon.json` | ответ не переписан из книги |
| Ф8 | вёрстка комплекта | `python3 sobrat.py` в папке итерации (или `dannye.py`) | `out/*.pdf` | `proverka.py`: А≠Б, страниц сколько надо, перелив ≤ 0, похожие на выданные, **контрольная и ДЗ — пол-листа на человека** (Г5) |
| Ф8к | карта (игровое занятие) | `kvest.validate / kvest.report` | граф в `out/` | один выход у клетки, всё вверх, ☠ на каждой дороге |
| Ф9 | предсказание по аватарам | `predskazanie.py zagotovka` → доли → `proverit` → коммит до `nachalo` (см. «Занятие: предсказание → факт») | `PREDSKAZANIE.csv` | табло красное, пока пара началась, а предсказания нет или оно не доказано гитом; «не нужно» запрещён |
| Ф10 | шпаргалка | `shpargalka_*_dannye.py` итерации → `listok_gen.shpargalka` | `out/SHPARGALKA-*.pdf` | **только номер, вариант, ответ** (А11, гейт Г6) |
| Ф10с | **слепая проверка** | субагент с пустым контекстом (промпт — ниже) | `SLEPAYA-PROVERKA.md` | «совпало N из M»; дефекты по важности |
| Ф11 | урок, приём, **скан всех работ** | — | `SKAN*.pdf` | пусто ≠ крест |
| Ф12 | разметка сканов | `python3 razmetka.py <итерация> <скан> <стр.> <выход.jsonl>` → текст задания субагенту | `RAZMETKA*.jsonl` | по 4–5 работ на разметчика; запись после каждой работы |
| Ф13 | свод | `python3 svod.py <итерация>` | `SVOD.md`, `SDACHA.csv`, `out/SVOD.json` | зачтено = плюс ИЛИ верный ответ; поправки владельца — списком имён в `POPRAVKI.json` |
| Ф14 | сверка и разбор | `python3 sverka.py <итерация>` после загрузки отметок в бот | `SVERKA.md` (+ `SVERKA.csv`) | табло красное, пока отметки работ итерации в выгрузке есть, а сверки нет; хвост → вход следующей итерации |

## Занятие: предсказание → факт

*English on purpose (owner's rule for files written by executors); commands and file names are as they are.*

**Why.** The goal of a lesson is 50–80 % solvability for every avatar (СН · Ни · Ц · В). Until now the forecast lived in the analyst's head and the check was optional. Now the prediction is a file, proved by git to be made BEFORE the pair, and the comparison with the fact is generated. The table (`tablo.py`) turns red if either step is skipped; the status «не нужно» for Ф9/Ф14 is forbidden.

**Steps (who · when · command).** Every command runs from `diskmat-57/mashina-listka/`; `<it>` is the iteration folder.

1. *Machine · after the sheet is assembled (Ф8)* — `python3 predskazanie.py zagotovka <it> <rabota_id> [<rabota_id> ...]` writes `<it>/PREDSKAZANIE.csv`: one row per item (`rabota_id, punkt, uroven, СН, Ни, Ц, В, istochnik_ocenki, kommentarij`), the four share columns empty. Items come from the bot export (`punkty`); a work that is not in the export yet needs `<it>/PUNKTY.csv` (`rabota_id,punkt,uroven[,yakor]`, `yakor` = `<rabota_id>:<punkt>` of a past item with a known fact). Where `bank-7i/reshaemost.csv` knows the item (same work and item, or the anchor) its fact is put into `kommentarij` as a hint. Re-running merges: filled shares are never overwritten.
2. *Analyst · before the pair* — fills the shares (0–1, e.g. `0.65`) for each item and avatar, relying on `reshaemost.csv` and the 2–3 anchors; writes where the estimate comes from into `istochnik_ocenki`.
3. *Analyst · same sitting* — `python3 predskazanie.py proverit <it>`: all shares are numbers in [0, 1], the item list equals the work's, `nachalo` is set in `ITERACIYA.json`. It prints the expected solvability of the ○ and △ tracks per avatar and warns outside 50–80 %, and writes `PREDSKAZANIE.md`. Fix the shares or the sheet until it is acceptable.
4. *Analyst · before `nachalo`* — commit `PREDSKAZANIE.csv` (the zone commit as usual). `predskazanie.py proverit <it> --git` then prints `git ✓`: the last commit of the file is earlier than `nachalo` and the file is clean against HEAD. A later edit makes it red again — the prediction cannot be improved after the fact.
5. *Lesson (Ф11–Ф12)* — marks go to the bot; the export is refreshed.
6. *Machine · after the lesson* — `python3 sverka.py <it>`: writes `SVERKA.csv` (item × avatar: forecast, fact, writers, error) and `SVERKA.md` (per avatar: mean absolute error, shift = forecast above/below the fact, share of items in 50–80 % by fact, misses over 20 p.p.), and appends the fact to `reshaemost.csv`. Cells with fewer than two writers are «нет данных», never 0 or 100 %.
7. *Table* — `python3 tablo.py <it>` is green (rc = 0) when Ф9 and Ф14 are in order.

**New iteration.** `python3 novaya.py <arc> <date> <slug> "<theme>" [<nachalo>]` sets `nachalo` (default `<date>T14:00`, Moscow time — correct it if the pair starts otherwise) and the Ф9/Ф14 artefacts. An old iteration without `nachalo` shows Ф9 red: that is the past gap, not a bug.

**The gate in one place** (`tablo.py`). Ф9 is red when: status «не нужно»; no `nachalo`; status «готово» but `proverit --git` is red; the pair has started and `PREDSKAZANIE.csv` is missing, not accepted or not proved by git. Ф14 is red when: status «не нужно»; the export has marks of this iteration's works (works whose date is the date in the folder name) and `SVERKA.md` is missing. No export on the machine ⇒ a visible «не проверено» line, not red. `--bez-zapisi` prints without rewriting `TABLO.md`; `--seychas ГГГГ-ММ-ДДTЧЧ:ММ` sets the clock for tests.

**Do not.** Do not invent predictions for past works (their sverka is only a test, outside iteration folders); do not put children into `reshaemost.csv` or any file here — only aggregates per avatar.

### Шкала решаемости — `../bank-7i/reshaemost.csv`

`python3 sverka.py --shkala` (idempotent) fills it from the bot export for every work since 22.09 that has items: one row per `rabota_id × punkt × avatar`, columns `rabota_id, punkt, uroven_punkta, avatar, reshili, pisali, dolya, popytki_sred, na_datu, istochnik`. Rules (they are the file's header — a CSV cannot hold comments):

- `pisali` — children of the avatar who wrote the work: test / homework — status «сдал»; sheet / mini-sheet — at least one «+» on the sheet. `dolya = reshili / pisali`, empty if `pisali` < 2 («нет данных»).
- **Strict mode: an empty cell of a sheet is «не решил».** «Не брался» and «пробовал, не сдал» are not told apart yet (canon §5.6), so sheets are underestimated and the number is a lower bound.
- A work with two alternative parts (КР2: ○ and △) counts an item only for those who handed in AND marked something in the item's part (`istochnik` = `vygruzka:chast`; otherwise `vygruzka:strogo`) — else the ○ items would be diluted by children who chose only △.
- The avatar of a child is the one he had FOR THIS WORK (owner 11.10 23:05: the level is dynamic, built before every lesson): the row of the table `avatary` (one row per child and checkpoint) with the last `na_datu` **strictly earlier** than the work's date — the level the lesson was planned for; `na_datu` of the row is that checkpoint. A work of the first day of the theme has no earlier checkpoint: everyone is `Н`, its cells are «нет данных» (the run prints how many). `istochnik` = `vygruzka:<strogo|chast>:tochka-ranshe` (`…:net-tochki-ranshe` for such a work). `Н` and the test child are out. `popytki_sred` is empty until attempts are recorded.
- `sverka.py <it>` upserts by the same key with the same function, so the scale and the sverka cannot disagree.

## Капсула — что в ней лежит

| файл | что делает |
|---|---|
| `listok_gen.py` | генератор: поля ответа формата 22.09, картинки по Шеню, карта-восхождение, шапки, PDF через Chromium, `fit_report` (перелив в мм); `polulist` — две половины A4 с линией реза (контрольная А/Б, ДЗ ×2) |
| `kvest.py` | граф карты: проверка (один выход, без циклов, всё достижимо) и симуляция «лагерь/вершина» по типам детей |
| `proverka.py` | гейты перед печатью Г1–Г7 (Г5 — контрольная и ДЗ на пол-листа, Г6 — шпаргалка только «номер, вариант, ответ», Г7 — у каждого PDF рядом `.md` с текстом; отдельно: `python3 proverka.py --teksty <out/>`) |
| `razmetka.py` | задание разметчикам из канона: пункты, эталон, словарь плюсов, формат JSONL |
| `svod.py` | свод сдачи: баллы, разрешение (разных баллов, доля ничьих), KR-20, тропы, лагерь, вершина, пункты: сдано / крест / пусто |
| `predskazanie.py` | предсказание до урока: `zagotovka` (заготовка `PREDSKAZANIE.csv`), `proverit` (числа 0–1, `nachalo`, доказательство гитом, ○/△ по аватарам) |
| `sverka.py` | факт и сверка: `--shkala` (шкала решаемости из истории), `<итерация>` (предсказание против факта по аватарам) |
| `tablo.py` | табло итерации и гейт Ф9/Ф14; фазы по умолчанию — `FAZY` |
| `novaya.py` | новая итерация из шаблона, чередование игрового занятия, поле `nachalo` |
| `vlozheniya.py` | все ли наговоры владельца (вложения сессии) лежат на диске дословно — гонять перед хэндоффом; краснеет, если нет |
| `shablon/dannye_shablon.py` | шаблон данных листка: задачи с источником, ответ — функцией-перебором, поля ответа |

Образец полной итерации с картой — `../2026-08-18_logika-goda-7/iteracii/2026-09-29_kombinatorika-2/` (`sobrat.py` собирает всё).

## Текст рядом с PDF (с 10.10, решение владельца)

Каждый PDF, который собирает `to_pdf`, остаётся с двумя соседями: исходным HTML и `<имя>.md` — чистым текстом, из которого берут условия (боту, поиску, проверке), не разбирая PDF. Формат `.md` один на всю машину и задан функцией `listok_gen.html_v_md`: заголовок `# <название>` и под ним строка шапки `<дата> · <класс> · вариант <В>`; `## <раздел>`, если он есть; каждая задача — абзац `**<значок><номер>.** <условие>`, пункты (а), (б)… стоят в условии как есть (нет в условии, но полей ответа несколько — строка «Пункты: а, б»); картинки — `[рисунок: …]`; правила, «Стоп» и подвал — абзацами на своём месте; две одинаковые половины пол-листа (ДЗ) дают текст один раз; вёрстки нет. `SHPARGALKA-*` и `SKAN*` без `.md` — это ответы и сканы, не условия. Гейт Г7 `proverka.py` краснеет, если у `out/*.pdf` нет соседнего `.md`, и печатает «PDF с текстом рядом X из Y». Итерации, собранные раньше, дописываются без пересборки PDF: `python3 listok_gen.py --teksty <папка out/>` (читает лежащий рядом HTML, PDF не трогает).

## Промпт слепой проверки (Ф10с) — дословно, менять только список документов

> Ты — слепой проверяющий комплекта к уроку. Материалы — только PNG страниц и .txt в папке <…>. 1) Реши САМ все задачи
> (перебором на Python; картинки считай по изображению), только потом открой шпаргалку и сверь: «совпало N из M» +
> расхождения. 2) Дефекты условий: двусмысленность, текст ≠ картинке, разная трудность А/Б. 3) Шаблоны-прочерки глазами
> семиклассника, который не очень понимает. 4) Карта и правила глазами ребёнка: откуда начать, куда можно, что значат
> знаки, у каждой ли клетки понятно «куда дальше», совпадают ли клетки с пунктами. 5) Вёрстка. 6) ДЗ: разнообразие, повторы,
> посильность. Сначала сверка, потом дефекты по важности, каждый одной-двумя строками. Файлы не меняй.

*Замер 29.09:* первый прогон 68/68 ответов и 12 дефектов карты и правил; после правок второй прогон 86/86 и 11 дефектов,
из них 4 про правила карты — все исправлены (Р201); третий прогон (после вёрстки) — 86/86. Проверка **меняет** результат, а не подтверждает.

## Где собирать PDF

Генератору нужен Chromium: `python3 -m pip install playwright && python3 -m playwright install chromium`. В облачной
сессии он есть; на Маке 29.09 его не было — табло, свод, разметка и проверка графа работают без него (чистый Python).

## Чего машина пока НЕ умеет — честно

- **Раскладка карты** (координаты клеток) делается руками в данных итерации; образец — `POS` в `listok_29-09_dannye.py`.
  Проверка графа и симуляция — машинные.
- **Сами доли предсказания** ставит аналитик; машина даёт заготовку, подсказки по якорям, проверку и сверку. Попытки (галочка за попытку, канон §5.6) пока не ведутся — `popytki_sred` пуст.
- **Г3 (повторы)** сравнивает только тексты `.tex` арки и HTML итераций; ДЗ и контрольные прошлых лет не видит.
- **Инфографика для коллег** (`infografika.py` 22.09) не обобщена: зашиты имена пунктов 22.09.
- **Модель симуляции** откалибрована по одному уроку; перекалибровать по `SVOD.json` после каждой пары с картой.

## Дизайн-код значков (владелец 05.10 22:37, Р267)
- ○ — кружок: базовые задачи («техника», лабораторная работа: метод назван или подсказан действием).
- △ — треугольник: продвинутые задачи («идея», нормальная контрольная для сильных).
- Ромб ◇ — только клетки карты-восхождения (дополнительные задачи листка), не раздел контрольной.
- Разделы не подписываются текстом («для всех», «по желанию» и т. п.) — значок и есть подпись. Минимализм.
- В контрольной поле подписи принимающего не нужно: ответ проверяет машина; сложные пункты — общее поле, короткий пункт — квадратик в углу того же поля.
- Баллы: максимум по ○ и по △ одинаковый (школьник выбирает путь); у △ балл стоит у задачи.
