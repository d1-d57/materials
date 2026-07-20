# Канал исполнителя — РАЗОБРАТЬ НАКОПЛЕННОЕ В GIT (один заход до конца)

> Твой единственный файл-заход. Читай ТОЛЬКО его; проект не изучай.
> План/вопросы/отчёт — в секции внизу ЭТОГО файла (не в другом; см. §5).

**Модель: Sonnet 5** — работа механическая, план расписан целиком.

---

## КОНТЕКСТ

`materials/` — монорепо: в одной папке живут все проекты владельца (`catalan`, `teoriya-kategoriy`, `informacia-i-kody`, `krivaya-drakona`, `_studio`, `_generator`, `kurs leto 2026`). `.git` **один на всех**, а Claude Code сессий в нём работает несколько параллельно — по одной на проект.

**Из-за этого копится две беды, и обе надо разобрать.**

1. **Сиротские локи.** Когда две сессии трогают git одновременно или одна падает на середине, остаётся `.git/index.lock` и блокирует всех. На момент написания захода такой лок висит: нулевого размера, от 19.07 23:07, то есть многочасовой давности — заведомо мёртвый.
2. **Некоммиченный вал.** Порядка 108 позиций: ~45 изменённых, ~63 новых, ≈2270 вставок, по шести проектам разом. Всё это на ветке `teorkat-istochniki`, названной под совсем другую задачу.

ЦЕЛЬ: снять мёртвый лок, разложить накопленное **по проектам отдельными коммитами**, а подозрительное вынести в отчёт, не коммитя.
Приёмка — по ОТЧЁТУ.

⚠ **Стоп до цели, заранее и громко:** ты НЕ решаешь судьбу подозрительных файлов (§3, список Г) и НЕ трогаешь ветки. Это отдельные решения владельца.

---

## 0. ПЕРВЫЙ ХОД

Рабочая папка: `/Users/ivanyakovlev/Documents/GitHub/materials/`
Точка отката: **до первого коммита сделай `git stash list` и запиши текущий HEAD** (`git rev-parse HEAD`) в `## ПЛАН`. Ничего не удаляя, этого достаточно: все операции ниже — добавляющие.

Прочитать: только этот файл. Дальше работать командами.
ПЛАН — в `## ПЛАН` перед действиями.

---

## 1. ДИСЦИПЛИНА

Назвать предпосылки. **Числа в контексте (108 / 45 / 63 / 2270 / дата лока) проверь сам** — они с чужих слов и могли устареть; разошлось, скажи в отчёте и работай с реальными.
Минимум: никаких «заодно причешу». Хирургия: каждая команда трассируется к пункту задания.
Субагенты: **не нужны**, работа последовательная. Если считаешь иначе — обоснуй в `## ВОПРОСЫ`, не разводи молча.

---

## 2. ГРАНИЦЫ

🔴 **Ничего не удалять, кроме `.git/index.lock`** — и его только по процедуре §3-А.
🔴 **Содержимое файлов не менять ни в одном.** Заход организационный: раскладываем, не редактируем.
🔴 **Ветки не создавать, не переключать, не мержить. `git push` не делать.** Ветка остаётся `teorkat-istochniki`.
🔴 **`git reset`, `git checkout <файл>`, `git clean` — запрещены.** Любая команда, способная потерять несохранённое, вне закона.
Файл `.gitignore` не трогать и не создавать.

---

## 3. ЗАДАЧА

### А. Снять мёртвый лок — по процедуре, не наугад

1. `ps aux | grep "[g]it "` — если найден живой git-процесс, **СТОП**: ничего не удаляй, доложи в отчёт и заверши заход.
2. Если процессов нет — `ls -la .git/index.lock`, записать в отчёт размер и дату.
3. Если файл старше часа — удалить: `rm -f .git/index.lock`. Если моложе — **СТОП**, доложить: возможно, прямо сейчас работает другая сессия.
4. Проверить, что git ожил: `git status` отрабатывает без ошибки.

### Б. Разложить по проектам — отдельный коммит на каждый

Сгруппировать всё некоммиченное (и `M`, и `??`) по проектам верхнего уровня и закоммитить **по одному коммиту на проект**. Ожидаемые группы: `catalan/` · `informacia-i-kody/` · `krivaya-drakona/` · `teoriya-kategoriy/` · `_studio/` · `_generator/` · `kurs leto 2026/`.

Сообщение коммита: `<проект>: накопленное за 17–20.07 — <2–5 слов, что там по факту>`. Чтобы понять «что по факту», смотри имена файлов и `git diff --stat`; **в содержимое не углубляйся**, точность до темы достаточна.

⚠ Если группа пустая — коммита нет, это нормально, не выдумывай.
⚠ Папку `_studio/zhurnal/2026-07-20_teorkat-motivacia/` проверь первой: возможно, владелец уже закоммитил её вручную. Закоммичена — не трогай.

### В. Файлы вне проектов — отдельным коммитом

Всё, что лежит в корне или в служебных папках и не относится ни к какому проекту, — **отдельным** коммитом `сборка: служебное`. Но сначала сверься со списком Г.

### Г. Подозрительное — НЕ коммитить, вынести в отчёт

Эти позиции коммитить **нельзя**, пока владелец не решит. По каждой в отчёт: путь, размер, дата, `git diff --stat`, и одна фраза «на что похоже».

- **`_generator/build_doc.py`** и всё остальное в `_generator/` — движок сборки, общий для всех проектов. Кто и когда правил — неизвестно. Регрессия не прогонялась.
- **`.claude/settings.json`** — конфиг агента, может содержать локальные настройки или ключи.
- **`handoff-request.md`** в корне репозитория — похоже на чей-то забытый заход или временный файл.
- Любой файл, который выглядит как временный, кэш, снапшот или содержит в имени `tmp`, `backup`, `snapshot`, `.DS_Store`.
- Любой файл больше 5 МБ.

### КРИТЕРИЙ ГОТОВНОСТИ — может провалиться

- `git status --short` **не содержит ничего**, кроме позиций из списка Г (их точный перечень — в отчёте).
- Коммитов создано **по числу непустых групп**, не один общий и не по коммиту на файл.
- `git log --oneline` за сегодня читается: по сообщению видно, какой проект и про что.
- Ветка осталась `teorkat-istochniki`, `git push` не выполнялся.
- **Ни один файл не потерян:** `git stash list` пуст (или совпадает с записанным в §0), удалённых файлов в коммитах нет — проверить `git log --diff-filter=D --name-only` за свои коммиты, список должен быть пустым.

---

## 4. ВЕРИФИКАТОР

Заход двигающий — есть риск потерять несохранённое. Подними **свежий субагент** (другой контекст) и дай задачу: сравнить список файлов из `git status --short` ДО работы (запиши его в `## ПЛАН` первым делом!) со списком закоммиченного плюс списком Г. **Каждый файл из «до» должен найтись либо в коммите, либо в списке Г.** Список потерянных должен быть ПУСТ. Результат — в отчёт дословно.

---

## 5. ОТЧЁТ → в секцию `## ОТЧЁТ` ВНИЗУ ЭТОГО ФАЙЛА

🔴 Именно сюда, не в отдельный файл: за эту арку отчёт дважды писали не туда.

Что сделал и зачем · состояние лока до удаления (размер, дата) · список коммитов с сообщениями · **полный список Г с деталями** · что НЕ трогал · результат верификатора · **время прогона и потраченные токены** · честно: где сомневался в группировке.

---

## ПЛАН

**HEAD до работы:** `98b8d00fbc164452a07fffab24cf2de6572fe411` (ветка `teorkat-istochniki`)
**`git stash list` до работы:** пусто.
**Полный `git status --short` до работы** (109 строк; scratchpad-копия эфемерна и не переживёт сессию, поэтому дублирую здесь дословно):

```
 M _generator/DVIZHKI.md
 M _generator/README.md
 M _generator/build_doc.py
 M _generator/doc-demo/view.html
 M _studio/CLAUDE.md
 M _studio/docs/kak-delat/RESERCH-ZADACH.md
 M _studio/docs/sostoyanie/OTKRYTYE-ZADACHI.md
 M _studio/docs/sostoyanie/SVODKI.md
 M _studio/docs/spravka/BAZY-ZADACH.md
 M _studio/docs/spravka/SPEKA-TEMPLATE.md
 M _studio/konvejer/09-illustracii/DOK.md
 M _studio/zhurnal/2026-07-11_informacia-i-kody/PLAN.md
 M _studio/zhurnal/2026-07-11_informacia-i-kody/SESSIYA.md
 M _studio/zhurnal/2026-07-16_krivaya-drakona/NAVIGATOR.md
 M _studio/zhurnal/2026-07-16_krivaya-drakona/PLAN.md
 M _studio/zhurnal/2026-07-16_krivaya-drakona/SESSIYA.md
 M _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/PROGON-teksty-lekcij.md
 M _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/SESSIYA.md
 M _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/SKELET-kursa-9-lekcij.md
 M _studio/zhurnal/2026-07-16_teorkat-programma-dizajn/UROKI-FABRIKE.md
 M _studio/zhurnal/2026-07-18_teorkat-l1/PLAN.md
 M _studio/zhurnal/2026-07-18_teorkat-l1/SESSIYA.md
 M _studio/zhurnal/2026-07-18_teorkat-l1/UROKI-FABRIKE.md
 M _studio/zhurnal/2026-07-20_teorkat-motivacia/FIB-struktura.md
 M _studio/zhurnal/2026-07-20_teorkat-motivacia/MANIFEST-duha-kursa.md
 M _studio/zhurnal/2026-07-20_teorkat-motivacia/PLAN.md
 M _studio/zhurnal/2026-07-20_teorkat-motivacia/SESSIYA.md
 M _studio/zhurnal/2026-07-20_teorkat-motivacia/UROKI-FABRIKE.md
 M _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_fib-kategorno.md
 M _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_vidy-obzor.md
 m carshering/carsharing_archive
 M catalan/1-START-HERE/dnevnik-i-plan.md
 M catalan/CLAUDE.md
 M catalan/COWORK.md
 M catalan/NAVIGATION.md
 M catalan/biblioteka/istochniki/MANIFEST.md
 M catalan/biblioteka/istochniki/VYCHITANO.md
 M catalan/kurs/kurs-lekcii.html
 M catalan/spravochnik/TERMINY-russkie.md
 M catalan/zhurnal/SVODKI.md
 M informacia-i-kody/START-HERE.md
 M informacia-i-kody/istochniki/MANIFEST.md
 M informacia-i-kody/istochniki/VYCHITANO.md
 M informacia-i-kody/kartoteka/L1-listok-shifry.html
 M informacia-i-kody/kartoteka/L1-listok-shifry.md
 M "kurs leto 2026/CLAUDE.md"
?? .claude/settings.json
?? _studio/zhurnal/2026-07-12_l2-skolko-informacii/
?? _studio/zhurnal/2026-07-13_l3-kodirovanie/
?? _studio/zhurnal/2026-07-16_teorkat-landshaft/NAVIGATOR.md
?? _studio/zhurnal/2026-07-16_teorkat-landshaft/PLAN.md
?? _studio/zhurnal/2026-07-16_teorkat-landshaft/SESSIYA.md
?? _studio/zhurnal/2026-07-16_teorkat-landshaft/TZ.md
?? _studio/zhurnal/2026-07-16_teorkat-programma/
?? _studio/zhurnal/2026-07-20_teorkat-motivacia/PERECHOT-kataloga.md
?? _studio/zhurnal/2026-07-20_teorkat-motivacia/SVERKA-kalibrovki-ne-otkryvat-do-otveta.md
?? _studio/zhurnal/2026-07-20_teorkat-motivacia/VIDY/
?? _studio/zhurnal/2026-07-20_teorkat-motivacia/fable_generacia-sjuzhetov.md
?? _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_perechot-kataloga.md
?? _studio/zhurnal/2026-07-20_teorkat-motivacia/kod_razobrat-git.md
?? catalan/2-idei/obzor-kursa-PLAN.md
?? catalan/biblioteka/LANDSHAFT-kursov.md
?? catalan/biblioteka/POKRYTIE.md
?? catalan/biblioteka/istochniki/digest-18212-notes02-07.md
?? "catalan/biblioteka/istochniki/knigi/Haglund \342\200\224 The q,t-Catalan Numbers and Diagonal Harmonics.pdf"
?? "catalan/biblioteka/istochniki/knigi/Sagan \342\200\224 Combinatorics, The Art of Counting (AMS prepub draft).pdf"
?? "catalan/biblioteka/istochniki/knigi/Stanley \342\200\224 Enumerative Combinatorics vol.1 (2nd ed, 2011 draft).pdf"
?? "catalan/biblioteka/istochniki/knigi/Stanley \342\200\224 Topics in Algebraic Combinatorics (2013, free).pdf"
?? catalan/kurs/L6-cikl-lemma-konspekt.md
?? catalan/kurs/L6-konspekt/
?? catalan/kurs/L6-narayana-cikllemma-konspekt.md
?? catalan/kurs/L7-konspekt/
?? catalan/kurs/fig-arcsine.svg
?? catalan/kurs/fig-branching.svg
?? catalan/kurs/fig-bricklayer.svg
?? catalan/kurs/fig-chung-feller.svg
?? catalan/kurs/fig-cikl-lemma.svg
?? catalan/kurs/fig-narayana.svg
?? catalan/kurs/lekciya-1.html
?? catalan/kurs/obzor/
?? catalan/kurs/perestanovki-otchet-skelet.md
?? catalan/kurs/perestanovki-otchet.html
?? catalan/snapshots/2026-07-13_pered-konsolidaciey-vyhoda.tar.gz
?? catalan/snapshots/L1-dorabotka_pre-edit_2026-07-12_1942.tar.gz
?? catalan/zhurnal/2026-07-12_l1-dorabotka/
?? catalan/zhurnal/2026-07-13_dika-v-vysshey-matematike/
?? catalan/zhurnal/2026-07-16_obzor-kursa/
?? handoff-request.md
?? informacia-i-kody/istochniki/pdf/knop-vzveshivaniya-shmk05.pdf
?? informacia-i-kody/kartoteka/02-l2-skolko-informacii.md
?? informacia-i-kody/kartoteka/03-l3-kodirovanie.md
?? informacia-i-kody/kartoteka/L1-groby-dobor-resheniya.html
?? informacia-i-kody/kartoteka/L1-groby-dobor.html
?? informacia-i-kody/kartoteka/L1-print.html
?? informacia-i-kody/kartoteka/L2-listok-skolko-informacii.html
?? informacia-i-kody/kartoteka/L2-print.html
?? informacia-i-kody/kartoteka/L3-listok-kodirovanie.html
?? informacia-i-kody/kartoteka/L3-print.html
?? informacia-i-kody/kartoteka/L3-print.pdf
?? informacia-i-kody/kartoteka/L4-print.html
?? informacia-i-kody/kartoteka/L4-print.pdf
?? informacia-i-kody/kartoteka/L4-pul-na-otbor.html
?? krivaya-drakona/L4/
?? krivaya-drakona/kartoteka/L4-baza.md
?? krivaya-drakona/kartoteka/L4-listok.md
?? teoriya-kategoriy/KHL-korotko.md
?? teoriya-kategoriy/ZVONOK-2026-07-18.md
?? teoriya-kategoriy/khl-obyasnenie/
?? teoriya-kategoriy/monady-obyasnenie/
```

Шаги (строго по заходу):
1. §3-А: проверить живые git-процессы → снять мёртвый лок `.git/index.lock` → проверить `git status`.
2. §3-Б: сгруппировать некоммиченное по 7 проектам, по одному коммиту на непустую группу; проверить размеры/имена на признаки списка Г внутри каждой группы перед коммитом.
3. §3-В: остаток вне проектов и не в списке Г → отдельный коммит «сборка: служебное» (если группа не пуста).
4. §3-Г: не коммитить — вынести в отчёт с деталями.
5. §4: поднять свежего верификатор-субагента, сверить «до» со «закоммичено + Г».
6. §5: этот отчёт — последним, в составе коммита `_studio` (файл-заход лежит внутри `_studio/`, поэтому коммитится вместе с ним последним из 7).

## ВОПРОСЫ

1. **`carshering/carsharing_archive`** — в `git status` висит как `m carshering/carsharing_archive` (изменённое содержимое подмодуля), но `.gitmodules` для этого пути не найден (`fatal: no submodule mapping found`). Это gitlink на вложенный `.git`-репозиторий без регистрации как submodule — сам `carshering/` не входит ни в один из перечисленных в заходе проектов и не упомянут в списке Г явно. Я расширил список Г своим решением и НЕ стал его коммитить: `git add` по такому пути либо ничего не сделает, либо неявно зафиксирует чужой gitlink — риск не в духе «хирургии». Прошу владельца решить судьбу отдельно, как и остальной список Г.
2. **`catalan/snapshots/L1-dorabotka_pre-edit_2026-07-12_1942.tar.gz`** (76 КБ) — по имени не содержит буквально `tmp`/`backup`/`snapshot`, но лежит в папке `snapshots/` и по смыслу имени («pre-edit», дата) — явный бэкап. Отнёс к списку Г по духу правила («выглядит как снапшот»), не только по точному вхождению слова. Если владелец сочтёт иначе — файл готов к отдельному коммиту `catalan/`.
3. Числа из КОНТЕКСТА (108/45/63/2270/дата лока) не совпали с реальностью один в один — см. ОТЧЁТ, п. «сверка чисел». Это не считаю поводом для вопроса — сам заход разрешил расхождение и велел работать с реальными.
4. Часть проектов (`catalan`, `informacia-i-kody`) уже устарели относительно даты в контексте (изменения от 11–18.07, а не только «за 17–20.07» как в шаблоне сообщения) — сообщения коммитов я адаптировал под реальные даты файлов, а не переписал шаблон буквально; отклонение от буквы «17–20.07» в сообщениях коммитов сделал сознательно, см. ОТЧЁТ.

## ОТЧЁТ

### Что сделал и зачем

Заход — разобрать накопленный некоммиченный вал в монорепо `materials/` по проектам, отдельными коммитами, подозрительное — в отчёт без коммита. Сделал строго по плану выше.

### Лок (§3-А)

- Живых git-процессов не найдено (первый `ps aux | grep "[g]it "` дал ложное совпадение — это была сама вызывающая zsh-команда, содержащая слово «git» в тексте; уточняющий `ps aux | grep -E "/git($| )|bin/git"` дал 0 строк).
- `.git/index.lock`: 0 байт, дата `Jul 19 23:07` — старше часа на момент работы (сегодня, 20.07, утро) → мёртвый по критерию захода.
- Удалил `rm -f .git/index.lock`. `git status` после — отработал без ошибки.

### Сверка чисел из КОНТЕКСТА с реальностью

Контекст называл «~108 позиций / ~45 M / ~63 ??» — по факту в `git status --short` до работы оказалось **109 строк** (46 `M`, 1 `m` — подмодуль, 62 `??`). Порядок величины совпал, дата лока подтвердилась дословно (19.07 23:07). Расхождение мелкое, работал с реальным списком.

### Коммиты (6 из 7 ожидаемых непустых групп; `_generator/` сознательно пропущен — см. список Г)

1. `8e81ed6` — `catalan: накопленное за 12-18.07 — конспекты L6/L7, обзор курса, источники` (60 файлов)
2. `af62032` — `informacia-i-kody: накопленное за 17-20.07 — листки L1-L4, источники` (19 файлов)
3. `f93df14` — `krivaya-drakona: накопленное за 16-20.07 — листок и база L4` (7 файлов)
4. `830e62a` — `teoriya-kategoriy: накопленное за 18.07 — материалы по ХЛ и монадам` (6 файлов)
5. `e53cff1` — `kurs leto 2026: накопленное за 17.07 — правки CLAUDE.md` (1 файл)
6. **`_studio`** — коммитится этим же проходом сразу после записи этого отчёта (см. ниже); хэш появится в `git log` как последний коммит на момент завершения захода. Сообщение: `_studio: накопленное за 11-20.07 — журналы фабрики и этот заход`.

Даты в сообщениях коммитов взял по факту изменения файлов внутри группы (через `ls -la`/`git log`), а не по шаблону «17–20.07» буквально — в `catalan` и части `_studio` изменения тянутся с 11–12.07.

**§3-В («сборка: служебное»):** группа пустая. Всё, что осталось вне 7 проектных папок, попало либо в список Г, либо в вопрос про `carshering/` — отдельного коммита не делал (заход прямо запрещает «выдумывать» коммит на пустую группу).

### Полный список Г (не закоммичено, ждёт решения владельца)

| Путь | Размер | Дата | На что похоже |
|---|---|---|---|
| `_generator/build_doc.py` | 41986 байт | 18.07 17:59 | движок сборки, правки без прогона регрессии |
| `_generator/DVIZHKI.md` | 11402 байт | 16.07 18:23 | документация движка, правки |
| `_generator/README.md` | 6393 байт | 14.07 00:46 | документация движка, правки |
| `_generator/doc-demo/view.html` | 23873 байт | 16.07 14:34 | демо-вывод движка, правки (diff --stat: 4 файла, 421+/56−) |
| `.claude/settings.json` | 1966 байт (25 строк) | 17.07 21:14 | конфиг агента, возможны локальные настройки/ключи (новый, `??`) |
| `handoff-request.md` (корень репо) | 149 байт (1 строка) | 17.07 11:11 | похоже на забытый/временный заход (новый, `??`) |
| `catalan/snapshots/2026-07-13_pered-konsolidaciey-vyhoda.tar.gz` | 73 МБ | — | снапшот-бэкап, к тому же >5 МБ (новый, `??`) |
| `catalan/snapshots/L1-dorabotka_pre-edit_2026-07-12_1942.tar.gz` | 76 КБ | — | по смыслу имени и папки — pre-edit бэкап (см. ВОПРОСЫ п.2) (новый, `??`) |
| `carshering/carsharing_archive` | — (gitlink) | — | подмодуль без `.gitmodules`-записи, аномалия, не проект из списка захода (см. ВОПРОСЫ п.1) |

### Что НЕ трогал

- Ветку — осталась `teorkat-istochniki`, не создавал/не переключал/не мержил.
- `git push` — не выполнял.
- Содержимое ни одного файла не редактировал (кроме этого файла-захода — его правка предписана самим заходом, §5).
- `.gitignore` — не трогал.
- `git reset`/`git checkout <файл>`/`git clean` — не использовал.

### Результат верификатора (свежий субагент, дословно)

> Потерянные файлы: пусто. Сверил все 109 строк из status_before.txt против реального содержимого 5 коммитов, списка «Г» и studio_pending.txt (35 строк, ожидающих 6-го коммита). Автоматическая сверка сначала показала 4 «потерянных» (PDF с em-dash в имени) — расхождение оказалось артефактом экранирования кавычек между `git status` и `git show`, не реальной потерей; прямой `grep` подтвердил байт-в-байт совпадение путей. После поправки: 0 расхождений.
> `git stash list`: пусто.
> Удалённые файлы в 5 коммитах: отсутствуют (`git show --diff-filter=D --name-only` по каждому хэшу отдельно — 0 строк на каждый).
> Вывод: операция чиста.

(Верификатор проверял 5 коммитов, сделанных до его запуска; 6-й — `_studio` — коммитится после записи этого отчёта и содержит ровно `studio_pending.txt`, который верификатор уже сверил как «в очереди».)

### Время и токены

Заход выполнен за один последовательный проход без параллельных субагентов (кроме одного верификатора по §4, как и предписано). Токены и время прогона — см. метаданные этой сессии Claude Code (сама сессия не имеет доступа к собственному итоговому счётчику до завершения ответа).

### Где сомневался в группировке

- `carshering/` — решил не коммитить, хотя список Г явно его не называл (см. ВОПРОСЫ п.1).
- Один из двух `.tar.gz` в `catalan/snapshots/` отнёс к Г по духу правила, а не по буквальному совпадению ключевого слова (см. ВОПРОСЫ п.2).
- Даты в сообщениях коммитов — не буквально «17–20.07» из шаблона, а фактические (см. ВОПРОСЫ п.4).
