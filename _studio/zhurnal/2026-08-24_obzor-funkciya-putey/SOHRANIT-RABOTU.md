# СОХРАНИТЬ РАБОТУ СЕССИИ 03.09 — команды владельцу

> **Зачем этот файл.** Сессия шла в песочнице Cowork, а оттуда **коммитить нельзя**: запись в `.git` проходит, удаление — нет, поэтому `git commit` оставит мёртвый `index.lock` и положит репозиторий (урок У44). Работа целого дня лежит на диске вне git и умрёт от `git clean`. Команды ниже выполняете вы, в своём терминале.
>
> Файл одноразовый: выполнили — удалили.

## Шаг 0. Убрать мину

При проверке прав я создал в `.git` пустой файл и не смог удалить. Для git он безвреден, но пусть не лежит:

```bash
rm ~/Documents/GitHub/materials/.git/_proba_zapisi
```

## Шаг 1. Репозиторий `materials` — три зоны

Ветка сейчас `arka/mat-kostyak`, отставания от origin нет.

```bash
cd ~/Documents/GitHub/materials

python3 ~/Documents/GitHub/disciplina/_generator/tools/git_zona.py commit \
  --zone kurs-puti-i-volny/ \
  --zone obzory/funkciya-putey-i-ee-uravneniya/ \
  --zone _studio/zhurnal/2026-08-24_obzor-funkciya-putey/ \
  -m "сессия 03.09: слой документации курса (ZAMYSEL, OBOZNACHENIYA, SLOVAR, PERESTROYKA) и прогулка в восьми главах — главы 2-8, пять иллюстраций, архитектура на восемь глав; разбор нормировок площади, координаты 32 тем, разбор расхождения по пятиугольной теореме; дневник, план, навигатор, урок У44"
```

Что войдёт: 4 новых документа курса + правленый `KOSTYAK.md`; 7 новых глав, 5 SVG, `view.html`, правленые `00-arhitektura.md` и `01-dve-drobi.md`; `SESSIYA.md`, `PLAN.md`, `NAVIGATOR.md`, `UROKI-FABRIKE.md`.

⚠ В зоне окажется и `VYGRUZKA-2026-09-02-6.md` — выгрузка прошлой сессии, тоже вне git. Это законно, она принадлежит арке.

⚠ `kod_matbaza-skeleta.md` числится изменённым, но эта сессия его не трогала — правка чужая, из прошлого прогона. Если не хотите её везти, добавьте её в отдельный коммит либо проверьте `git diff` перед командой.

## Шаг 2. Репозиторий `disciplina` — инструмент и предложение

```bash
cd ~/Documents/GitHub/disciplina

python3 _generator/tools/git_zona.py commit \
  --zone _generator/tools/ \
  --zone doma/ \
  -m "гейт словаря check_slovar.py с фикстурой на 8 ловушек: ловит запрещённое слово, след отменённого решения и смешение объявленной пары синонимов в одном файле; предложение архитектуры для больших research-проектов"
```

⚠ **Перед этим шагом** три новых документа `disciplina` **не зарегистрированы** в индексе своего корня: `register_doc.py` в песочнице не работает (нужны `ripgrep` и `bubblewrap`). Ворота 5 могут покраснеть. Регистрация — по одной команде на файл:

```bash
python3 _generator/tools/register_doc.py doma/PREDLOZHENIE-arhitektura-issledovatelskogo-proekta.md "предложение архитектуры для больших research-проектов: реестр решений с адресом, следы отменённого, транзитивная проверка опор"
```

`_generator/tools/` регистрации не требует — это код, а не документ корня `doma/`.

## Шаг 2а. Собрать заход (вы выбрали оформить вывоз заходом)

🔴 **Из песочницы `bootstrap_zahod.py` не работает** — сначала печатает «репозиторий `materials` не в реестре `КОРНИ_ПО_РЕПО`» и молча не создаёт файл, а с `KORNI_TABLICA_PO_UMOLCHANIYU=da` виснет по таймауту. Это тот же дефект, что у `register_doc.py` (ваш урок У9): инструменты `disciplina` не знают корней `materials`. В вашем терминале он должен отработать.

Готовая команда — параметры уже подобраны и проверены на всех воротах инструмента, кроме последнего:

```bash
cd ~/Documents/GitHub/materials

python3 ~/Documents/GitHub/disciplina/_generator/tools/bootstrap_zahod.py \
  _studio/zhurnal/2026-08-24_obzor-funkciya-putey vyvoz-raboty-0209 \
  --branch arka/mat-kostyak \
  --zone "kurs-puti-i-volny/ obzory/funkciya-putey-i-ee-uravneniya/ _studio/zhurnal/2026-08-24_obzor-funkciya-putey/" \
  --kanal terminal --intervyu da --rod-raboty mehanika \
  --opisanie "вывоз работы сессии 02.09 в git: слой документации курса, восемь глав прогулки, гейт словаря" \
  --finalizirovano "владелец выбрал вывоз заходом в терминал, а не руками" \
  --finalizirovano "обещание про два доказательства невыводимости Эйлера снято из архитектуры" \
  --finalizirovano "гейт check_slovar подключается в pre-commit в режиме --staged" \
  --kommitit "три зоны materials одним коммитом; disciplina — отдельным, там же регистрация трёх новых документов дверью register_doc.py" \
  --zakryt "ветку не гасить: arka/mat-kostyak живёт дальше" \
  --verifikator-ne-nuzhen "операция не лоссовая: заход только переносит уже написанные файлы в git, ничего не переписывает и не удаляет; критерий проверяется командой git_zona.py check" \
  --grjaznaya-arka-prichina "ЦЕЛЬ этого захода и есть разбор грязи: kod_matbaza-skeleta.md лежит правленым вне git с прошлого прогона и входит в вывозимую зону наравне с работой сессии 02.09"
```

Два клапана здесь открыты сознательно и с причинами: верификатор не нужен (перенос ничего не теряет), и дверь незакоммиченных `kod_*.md` открыта, потому что разбор этой самой грязи и есть цель.

**Если заход собирать не хотите** — шаги 1 и 2 выше делают ровно то же самое напрямую, и работа будет в git.

## Шаг 3. Проверить, что доехало

```bash
python3 ~/Documents/GitHub/disciplina/_generator/tools/git_zona.py check
```

Должен сказать, что в названных зонах вне git ничего не осталось. Остальное вне git — чужой долг других арок (`_fond`, `spetsmat-2026`, `2026-08-27_matproekty-179`), эта сессия его не трогала.

## Шаг 4. Прогнать гейты на всякий случай

```bash
cd ~/Documents/GitHub/materials
D=~/Documents/GitHub/disciplina/_generator/tools
python3 $D/../build_doc.py obzory/funkciya-putey-i-ee-uravneniya/LEKCIYA-v2
python3 $D/check_view.py   obzory/funkciya-putey-i-ee-uravneniya/LEKCIYA-v2
python3 $D/check_termin.py obzory/funkciya-putey-i-ee-uravneniya/LEKCIYA-v2
python3 $D/check_slovar.py obzory/funkciya-putey-i-ee-uravneniya/LEKCIYA-v2 --doma kurs-puti-i-volny
cd ~/Documents/GitHub/disciplina && sh _generator/tools/fixtures/check_slovar/PROGNAT.sh
```

На момент закрытия сессии все пять были зелёными: сборка 9 вкладок, вид не съеден, порядок терминов чист, словарь чист, фикстура 8 из 8.

---
*Собран 2026-09-02 (машинная дата; документы сессии датированы 03.09 — расхождение названо в `SESSIYA.md`). Удалить после выполнения.*
