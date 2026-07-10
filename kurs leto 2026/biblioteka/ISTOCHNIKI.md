# Источники — индекс (единственное место для ссылок)

Все внешние материалы курса одной строкой: что это / чем полезно. Новый источник — сперва сюда. Факты в работе **ссылаются** на эту строку, не переписывают (правило дедупа — `00-CHTO-GDE.md`).

> **🪟 Окно.** Единственный источник: внешние ссылки / материалы. Обновлять: новый источник — сперва сюда (факты ссылаются на строку, не переписывают). Приходишь из: ресёрч, `biblioteka/`. Карта — `../NAVIGATION.md`.

> Статус «проверено» — из файлов `fakty/` (две проходки по источникам так помечали факты). Прямых URL в архиве пока нет — добавлять по мере появления.

## Книги
- **Литвак, Райгородский. «Кому нужна математика?»** (МИФ 2017 / МЦНМО 2024) — **ключевой ОРИЕНТИР подачи** (золотой референс, ТЗ К9). 📄 PDF в `biblioteka/` (192 стр., born-digital Adobe InDesign — **чистый текстовый слой**, извлекается мгновенно через `pdftotext`/`pypdf`, без OCR, копирование разрешено; читать напрямую по главам дёшево). **Как пользоваться:** где у лекции есть парная глава — читать её, брать байки, изучать КАК подана тема, держать этот стиль эталоном. Концепция «прикладная математика вокруг».
  - **Карта глав → лекции:** Гл.2 «Менеджмент и многогранники» (ЛП · симплекс · расписания · проклятие размерности) → **Л2 Оптимизация** · Гл.6 «Секретные числа» → **Л4 Криптография** (отсюда байка Logjam «100 млн за число», ~с.112) · Гл.3 «Мир нулей и единиц» (кодирование · коды, исправляющие ошибки) → **Л5 Информация** · Гл.5 «Сила выбора из двух» → **Л6 Случайность** · Гл.4 «Надёжность интернета» (PageRank/сети) → Л6 · Гл.7 «Счётчики с короткой памятью» → Л5/Л6 · Гл.8 «Миллион аукционов в минуту» → прикладное/Л2 · Гл.1 «Кому-то ещё нужна математика?» → интро/манифест.
  - **Математическое приложение** («Приложения для подготовленного читателя», с.153–180 — к главам **2–8**): настоящие выкладки под наши матблоки. Напр. к гл.6 — доказательство схемы Диффи–Хеллмана + дискретный лог / первообразный корень (= наша «карусель вычетов», перестановка $g^k\bmod p$). **Правило работы: читать И главу (научпоп/байки), И её приложение (математика).**
- **Курант, Роббинс. «Что такое математика?»** — референс глубины и честности упрощения.
- **Pickover. "The Math Book"** · **Gowers (ed.). "Princeton Companion to Mathematics"** · **Андреев. «Математическая составляющая»** (МЦНМО) — референсы охвата.
- **Roberts. "Genius at Play"** — Конвей, Игра жизни.
- **Hoffman. "The Man Who Loved Only Numbers"** · **Schechter. "My Brain Is Open"** — Эрдёш.
- **Rosenhouse. "The Monty Hall Problem"** — Монти Холл.
- **Doxiadis. "Uncle Petros and Goldbach's Conjecture"** — драматургия гипотезы.
- **"The Prime Number Conspiracy"** (Quanta / MIT Press) — сборник.
- Русские: **«Дело академика Н. Н. Лузина»** (1999) · **Колмогоров** — юбилейное (Физматлит 2003), «в воспоминаниях учеников» (ред. Ширяев, МЦНМО 2006) · **Арнольд. «Истории давние и недавние»** · **Гельфанд. «Лекции по линейной алгебре»** · **Савватеев. «Математика для гуманитариев»**.

## Видео и медиа
- **Veritasium** — Нептун, нечётные совершенные, Коллатц, мнимые числа.
- **3Blue1Brown** — Борсук–Улам, сталкивающиеся блоки = π, нейросети.
- **Numberphile** · **Quanta Magazine** (+ YouTube) · **Vsauce** · **PBS Infinite Series**.
- Фильмы: «21» (2008), «Игра в имитацию» (2014), «Игры разума».
- Журналы: Quanta, NYT Magazine, New Yorker; русские — «Квант», «Квантик», «Элементы», ПостНаука, N+1.

## Научные / архивные (проверочные)
- **Монте-Карло:** Eckhardt, Los Alamos Science 1987; Metropolis–Ulam 1949.
- **Нейросети:** McCulloch–Pitts 1943; Rosenblatt 1958; Minsky–Papert 1969; Rumelhart–Hinton–Williams 1986; Cybenko/Hornik 1989; LeCun 1989; AlexNet 2012.
- **Марков:** Hayes, "First Links in the Markov Chain" (American Scientist 2013); IEEE Spectrum 2021.
- **ЛП / прочее:** Канторович 1939; Данциг 1947; эссе Вигнера 1960; Колмогоров, «Grundbegriffe» 1933.
- **Оптимальный транспорт:** Монж 1781 (фортификации); Канторович 1942; Бренье 1987/91; Виллани (Филдс 2010); Фигалли (Филдс 2018) — арка Л-оптимизация → ML.
- **Крипто-история:** Diffie–Hellman 1976; RSA 1977 (вызов RSA-129 → разгадан 1994, «Squeamish Ossifrage»); GCHQ — Эллис/Кокс/Уильямсон 1969–73 (рассекречено 1997); Logjam 2015 (Adrian et al.); общие простые ключи 2012 (Heninger; Lenstra–Hughes).

> **Фактчек контента курса (арка «научпоп-черновик», 2026-06-29/30).** Темы выше проверены субагентами при доборе до 10/10; результат осел в `zhurnal/2026-06-28_nauchpop-chernovik/opisanie-kursa-v2/` (`teorii-v2.md` · `dokazatelstvo-v2.md` · `deystvuyushchie-lica-v2.md`) и питает единый источник правды. Исправленные ошибки исходных данных — `2-idei/kotel.md §10` + `…/kod_dobor-do-10.md §ОТЧЁТ`.

## Люди-герои (для «кочующих людей» между лекциями)
Тьюринг · фон Нейман · Шеннон · Колмогоров · Гёдель · Канторович · Нэш · Марков · Кантор · Хэмминг · Улам · Ферми · Нётер · Эрдёш · Мирзахани · June Huh · Виажовска · Понтрягин · Гельфанд · Арнольд · Лузин · Конвей · Башелье · Мандельброт.

## Методология отбора (служебное — арка «гейты-и-баллы», Ф2)
Не материал курса, а как строить инструмент оценки тем.
- **Stage-Gate** — must-meet vs should-meet критерии на гейтах: https://www.stage-gate.com/blog/the-stage-gate-model-an-overview/
- **ASQ — Decision Matrix (Pugh)** — сравнение с эталоном, относительное ранжирование: https://asq.org/quality-resources/decision-matrix
- **Decision-matrix method (Pugh)** — концепт-селекция, шкала −2…+2: https://en.wikipedia.org/wiki/Decision-matrix_method
- **ASU — Designing Effective Rubrics** — 3–5 уровней, якорные дескрипторы: https://teachonline.asu.edu/2019/02/best-practices-for-designing-effective-rubrics/
- **Statsig — Rubric design** — ловушки гало/переобучения, мало критериев, грубые шкалы: https://www.statsig.com/perspectives/rubric-design-effective-grading

## Нарратив-структура (служебное — арка «гейты-и-баллы», Шаг B)
Как строить историю внутри эпизода и серии; питает discovery-fiction-движок и ворот «антология-с-throughline» в `1-START-HERE/sistema-ocenki.md`.
- **М. Нильсен — «Discovery fiction»** — правдоподобная история о том, как результат мог быть открыт (keystone-движок): https://michaelnotebook.com/df/index.html · пример «как открыть биткоин»: https://michaelnielsen.org/ddi/how-the-bitcoin-protocol-actually-works/
- **И. Лакатос — «Proofs and Refutations»** — доказательство как путь догадок-опровержений (родословная DF): https://en.wikipedia.org/wiki/Proofs_and_Refutations
- **Т. Гауэрс — «откуда берётся нормальная подгруппа»** — мат-изложение через переоткрытие: https://gowers.wordpress.com/2011/11/20/normal-subgroups-and-quotient-groups/
- **Б. Виктор — «Explorable Explanations»** — интерактив/вайб-кодинг + предупреждение «форма ради формы» (закон Старджона → граница достаточности): http://worrydream.com/ExplorableExplanations/
- **Г. Сандерсон (3b1b)** — concrete-before-abstract, населить ум примерами до определений: https://www.3blue1brown.com/about/ · интервью Dwarkesh: https://www.dwarkesh.com/p/grant-sanderson
- **Структура серии (TV-крафт)** — антология vs season-arc, «double duty» эпизода: limited series — https://fiveable.me/tv-writing/unit-1/limited-series/study-guide/YNR2zyUJa1t2KgPM · serialized vs episodic — https://fiveable.me/tv-genres/unit-4/serialized-vs-episodic-drama-structures/study-guide/U37Wa9O8t6N3y3cS · anthology — https://fiveable.me/tv-writing/unit-1/anthology-series/study-guide/W8OQ2Kj8RxUv3zRZ

## Единый источник MD→HTML — ресёрч решений (2026-06-30, арка «единый источник»)
> Как мир решает single-source-of-truth → «красивый» HTML под наш масштаб (7 лекций + глубокий банк; правит **агент по протоколу**, не человек руками; выход — один офлайн-HTML в дизайне v3/v4). Три субагента, веб. **Вывод: брать НЕ фреймворк, а тонкий набор скриптов поверх наших plain-MD.**

**Рекомендуемый минимальный стек (вывод ресёрча):**
- **Генератор** — свой тонкий скрипт (Python `markdown-it-py` + `mdit-py-plugins` container + Jinja2-шаблон, снятый с v3/v4). Наш случай требует Python-логики: SVG-инфографика из карты, резолв `→[id]`→портрет/чип/дуга, base64-портреты, рендер с учётом счётчиков. Нулевой-код baseline для сравнения — **Pandoc** `--standalone --embed-resources` + Lua-фильтр + кастомный шаблон (одна команда, детерминизм, без npm). Сборка **двупроходная**: 1-й проход собирает все id, 2-й резолвит ссылки.
- **Бэклинки** (ядро боли «правлю тут — вижу задетое там») — ~60-строчный скрипт инвертирует прямые `→[id]` в обратный индекс `задето[id]=[(файл,цитата)]` → `link_index.json` и/или секция «## Задето» в файле. Паттерн note-link-janitor; без приложения.
- **Целостность как падающий тест** — ~120-строчный линтер читает ЖИВЫЕ файлы и валит сборку (exit 1) на: нерезолвящихся `→[id]`, сиротах, матблоках вне ~20, нарушенных квотах графа (≥3 сквозных через ≥5, ≥10 парных, лицо в 2–5). Счётчики НЕ хранятся — пересчитываются из файлов, поэтому расходиться не могут. Модель — контент-линтер GitHub Docs (60+ правил как hard-fail CI).
- **Привязка HTML↔текст** (комментировать рендер) — генератор ставит `data-source` (файл:блок) на каждый блок (sourcepos markdown-it / позиции remark) → коммент в HTML однозначно ведёт к MD-блоку. Комменты — невидимыми маркерами в MD (паттерн md-redline): агент читает → правит → стирает.
- **Граф-вид** — из индекса генерим Mermaid/DOT (~30 строк); Mermaid встроен в `karta.md` (рендерится на GitHub/в превью). Опц. богатый интерактив — Quartz v4.
- **Протокол правок** (твоё «чёткая инструкция где что править») — расширить CLAUDE/AGENTS-паттерн чек-листом **семантического рипла** по типам правок + «definition of done» + машинные маркеры `@canonical:X`/`@ref:X` (агент грепает все употребления). **Честный предел:** механический рипл автоматизируется (переименовал id → починить ссылки); семантический (сменил рамку лекции → пересмотреть манифест/таймлайн) — агент ФЛАГует «задето §X», но не решает за тебя → нужен ревью-гейт.

**Ландшафт со ссылками.** Генерация MD→офлайн-HTML: Pandoc https://pandoc.org/lua-filters.html · markdown-it-py https://github.com/executablebooks/markdown-it-py + https://mdit-py-plugins.readthedocs.io/ · markdown-customblocks https://github.com/vokimon/markdown-customblocks · remark/rehype-directive https://github.com/remarkjs/remark-rehype · Quarto (Bootstrap-связан) https://quarto.org/docs/output-formats/html-basics.html · vite-plugin-singlefile https://github.com/richardtallent/vite-plugin-singlefile. Бэклинки/DRY: note-link-janitor https://github.com/andymatuschak/note-link-janitor · wikilinks https://python-markdown.github.io/extensions/wikilinks/ · COPE https://www.lullabot.com/articles/understanding-create-once-publish-everywhere-cope · Obsidian-эмбеды ломаются на экспорте https://forum.obsidian.md/t/transclusion-on-export/3193. Линтеры: lychee https://lychee.cli.rs/overview/ · markdown-link-check https://github.com/tcort/markdown-link-check · GitHub Docs linter https://docs.github.com/en/contributing/collaborating-on-github-docs/using-the-content-linter · contextlint https://github.com/nozomi-koborinai/contextlint. Граф/привязка/агент: markdown-it-source-map https://github.com/tylingsoft/markdown-it-source-map · Quartz v4 https://quartz.jzhao.xyz/ · md-review-plus https://github.com/Seiraiyu/md-review-plus · AGENTS.md https://www.infoq.com/news/2025/08/agents-md/ · llms.txt https://limy.ai/blog/llms.txt-in-2026-the-full-guide · Mermaid/Graphviz из MD https://mdedit.ai/blog/complete-guide-to-diagrams-in-markdown.

**Ловушки.** base64-раздувание (жать PNG; SVG держать инлайн-текстом, не base64). Pandoc `--embed-resources` НЕ инлайнит `url()` из CSS — шрифты явным `@font-face{src:url(data:)}` (https://github.com/jgm/pandoc/issues/8362). Резолв `→[id]` требует двупроходной сборки. Бэклинк-индекс/граф пересобирать В сборке, не лениво (иначе фантомные рёбра). Заголовочные якоря слугаются по-разному в рендерах → наш `→[id]`, резолвимый ЛИНТЕРОМ (не рендером), это и чинит — решение об id уже верное. Семантический рипл не автоматизируется — только ревью-гейт.

**НЕ берём (оверкилл под 7 лекций):** Hugo / MkDocs-Material (тема навязана, многостранично) · Astro (JS-билд ради 7 страниц) · Sphinx/MyST (Python-билд-система) · AsciiDoc / DITA (смена тулчейна / enterprise-XML) · Obsidian/Foam/Dendron как инфраструктура (индекс в приложении/VSCode — агент не достанет) · RAG/вектора для консистентности.

## Л4 «Криптография» — hand-gap research (арка «Л4 до идеала», 2026-06-30)
> Сверено по первоисточникам под слоты пересборки Л4. Дистиллят — `zhurnal/2026-06-30_L4-ideal-standart/research-handgap-L4.md`.

**История-вход (Энигма / SIGSALY / Шеннон):**
- Diffie W., Hellman M., «New Directions in Cryptography», IEEE Trans. IT-22(6) (1976) — постановка = проблема доставки ключа (честный мост): https://historyofinformation.com/detail.php?id=1807
- Wikipedia, «SIGSALY» — тепловой шум на пластинках, one-time pad в железе, 15.07.1943: https://en.wikipedia.org/wiki/SIGSALY · NSA: https://media.defense.gov/2021/Jul/13/2002761542/-1/-1/0/SIGSALY.PDF
- Shannon C.E., «Communication Theory of Secrecy Systems», BSTJ (1949), H(K)≥H(M): https://en.wikipedia.org/wiki/Communication_Theory_of_Secrecy_Systems
- GCHQ-trio (Эллис 1969 / Кокс 1973 / рассекр. 1997): https://en.wikipedia.org/wiki/Clifford_Cocks
- ⚠️ Шеннон↔Тьюринг 1943 — чай/мыслящие машины, НЕ криптография; первый сеанс SIGSALY без имён участников.

**ZKP (нулевое разглашение):**
- Goldreich, Micali, Wigderson, «Proofs that Yield Nothing But Their Validity…», J. ACM 38(3) (1991) — протокол 3-раскраски, соундность 1/|E|, ZK для всего NP: https://dl.acm.org/doi/10.1145/116825.116852
- Quisquater, Guillou, Berson, «How to Explain Zero-Knowledge Protocols to Your Children», CRYPTO'89 — пещера Али-Бабы (владелец: сомнительна): https://link.springer.com/chapter/10.1007/0-387-34805-0_60
- Wikipedia, «Zero-knowledge proof» — «два шара/дальтоник» (рекомендованный вход): https://en.wikipedia.org/wiki/Zero-knowledge_proof
- Fiat, Shamir (1986), CRYPTO'86 — ZK-идентификация→подпись. Signal Private Group System (Chase–Perrin–Zaverucha, CCS 2020): https://eprint.iacr.org/2019/1416

**Эллиптические кривые / биткоин (финал):**
- Hankerson, Menezes, Vanstone, «Guide to Elliptic Curve Cryptography», Springer (2004): https://link.springer.com/book/10.1007/b97644 · пример F₁₇ — Paar–Pelzl, «Understanding Cryptography»
- Antonopoulos, «Mastering Bitcoin» 2-е изд., гл.4 — в биткоине НЕТ шифрования, только подпись: https://github.com/bitcoinbook/bitcoinbook · secp256k1: https://en.bitcoin.it/wiki/Secp256k1
- Fersch, Kiltz, Poettering, «Limits in the Provable Security of ECDSA», eprint 2023/914 — граница честности (нет строгой редукции к ECDLP): https://eprint.iacr.org/2023/914.pdf
- NIST SP 800-57 Pt.1 — 256-бит ECC ≈ 3072-бит RSA.

**Logjam (байка, блок 8) — фактчек:**
- Adrian et al., «Imperfect Forward Secrecy: How Diffie-Hellman Fails in Practice», CCS'15 (Best Paper): https://weakdh.org/imperfect-forward-secrecy-ccs15.pdf · обзор: https://en.wikipedia.org/wiki/Logjam_(computer_security)
- Цифры (один общий 1024-бит простой): 66.1% VPN (IKEv1), 25.7% SSH, 17.9% топ-1M HTTPS; предвычисление ~сотни млн $. CVE-2015-4000.
- ⚠️ ПОПРАВКИ к версии Райгородский–Литвак с.112: спецслужба = **NSA, не ЦРУ**; **Диффи–Хеллман, не факторизация RSA**; «1024-бит госуровнем» = **гипотеза** (реально показан 512-бит downgrade). Критика практичности: Ронен–Шамир.

## Л2 «Оптимизация» — research (арка «Л2 Оптимизация/ЛП», 2026-06-30)
> Сверено под слоты `zhurnal/2026-06-30_L2-optimizaciya/research-L2.md`. Математика — proof-self-review субагента + scipy.

**ЛП / симплекс / двойственность:**
- Dantzig G., «Origins of the Simplex Method» (1990), история + дата встречи с фон Нейманом 3.10.1947: https://dl.acm.org/doi/pdf/10.1145/87252.88081 · обзор: https://en.wikipedia.org/wiki/George_Dantzig
- ⚠️ «домашка»-байка: две **нерешённые задачи**, не «нерешаемые»; 2-ю независимо решал **Абрахам Вальд** (соавтор 1951); «Умница Уилл Хантинг» — городская легенда.
- Двойственность ЛП ↔ минимакс фон Неймана (1928): минимакс — **частный случай** сильной двойственности; строгое ЛП-доказательство — **Гейл–Кун–Таккер 1951** (лемма Фаркаша). Не «⇔».
- Симплекс: худший случай — куб **Кли–Минти 1972**; на практике — **smoothed analysis Спилман–Тенг 2001/2004**; Quanta «Researchers Discover the Optimal Way To Optimize» (Steve Nadis, 13.10.2025; Bach–Huiberts, arXiv 2504.04197): https://www.quantamagazine.org/researchers-discover-the-optimal-way-to-optimize-20251013/
- **Рост эффективности ЛП (добор из книги-референса, гл.2 «Математика, обогнавшая компьютер»):** Bixby «A brief history of linear and mixed-integer programming computation», Documenta Mathematica 2012 [11] — CPLEX 1991→2012 алгоритмы ×469 800, с железом ×4 млрд (126 лет→1 сек); Bertsimas–King 2015 (MIT) → ×450 млрд, ЛП в статистике. Целочисленное ЛП NP-трудно (ветви-границы, Гомори). Кейс: премия Эдельмана 2008 — расписание ж/д Нидерландов.

**Диета Стиглера (человек→машина):**
- «The Cost of Subsistence» (Stigler 1945): $39.93/год (цены 1939) → 1947 **Джек Ладерман, NBS**, симплекс, 9 клерков, ~120 чел-дней → $39.69 (промах ≈0,6%). «Stigler's Diet Problem Revisited», Operations Research 2001: https://pubsonline.informs.org/doi/pdf/10.1287/opre.49.1.1.11187 · резюме: https://developers.google.com/optimization/lp/stigler_diet

**Оптимальный транспорт:**
- Канторович: **1939 ЛП-брошюра / 1942 «О перемещении масс» (транспорт) / 1948 связь с Монжем**; блокада — лёд Ладоги; Нобель 1975 (единственный сов.): https://en.wikipedia.org/wiki/Leonid_Kantorovich · https://www.nobelprize.org/prizes/economic-sciences/1975/kantorovich/biographical/
- Монж: мемуар 1781/опубл.1784, военный инженер-фортификатор École de Mézières; «инженер Наполеона» — анахронизм: https://en.wikipedia.org/wiki/Gaspard_Monge
- Бренье 1987/1991: для квадратичной стоимости опт. отображение = ∇φ (φ выпукла). ⚠️ Монж не доказал *существования* (стоимость |x−y|); структуру для |x−y|² раскрыл Бренье.
- Виллани (Филдс 2010), Фигалли (Филдс 2018, ученик Виллани, «в 18 не умел дифференцировать»): https://www.quantamagazine.org/a-traveler-who-finds-stability-in-the-natural-world-20180801/
- WGAN — Arjovsky–Chintala–Bottou 2017 (W₁ + двойственность Канторовича–Рубинштейна; критик = 1-липшицева f): https://arxiv.org/abs/1701.07875 · SD3/rectified flow (Esser 2024). ⚠️ В DDPM (Ho 2020) связь с OT постфактум; явно — WGAN/rectified flow. Обнуляются *расхождения* KL/JS, не «меры».

**Guardrail (не вносить обратно):** **SABRE** — транзакционная БД бронирования, не оптимизатор (https://en.wikipedia.org/wiki/Sabre_(travel_reservation_system)); **UPS ORION** — эвристический решатель TSP, не ЛП (https://pubsonline.informs.org/do/10.1287/orms.2016.03.10/full/); факторизация в NP∩co-NP (→Л3).

## Структура и связи курса — усиление связей (арка, 2026-07-02)
> Все связи с URL и тегами тело/wink/натяжка + вердикт изолированного судьи — в `0-koncept/svyazi-istochniki.md` (не дублирую пофайлово). Ниже — опоры манифеста и ключевые новые связи.

**Опоры манифеста «границы возможного»:**
- Н. Янофски, «The Outer Limits of Reason» — у разных пределов разума общий узор: https://en.wikipedia.org/wiki/The_Outer_Limits_of_Reason
- Д. Дойч, К. Марлетто — constructor theory (законы как карта возможного/невозможного): https://en.wikipedia.org/wiki/Constructor_theory

**Ключевые новые связи (полностью — в `0-koncept/svyazi-istochniki.md`):**
- Тьюринг→оптимизация: «Rounding-off errors in matrix processes» (1948, число обусловленности, LU) — wink на грани натяжки.
- фон Нейман→информация: энтропия фон Неймана (1932) + анекдот «назови это энтропией» (Tribus–McIrvine, Sci Am 1971) — wink.
- Шеннон→сложность: нижняя граница схемной сложности Θ(2ⁿ/n) (BSTJ 1949) — тело, предок circuit lower bounds.
- Тьюринг→случайность: Banburismus, ban/deciban (последовательный анализ, Гуд 1979) — тело.
- Винер: фильтр Винера / кибернетика (оптимальное предсказание) — новый сквозной 4/7.
- Блэкетт / исследование операций (аддитив 03.07, сверено): «цирк Блэкетта» (авг.1940, зенитное командование; расход снарядов на самолёт ~20 000→~4 000 к 1941) — рождение OR; Нобель по физике 1948 (камера Вильсона). Источники: рус. Википедия «Исследование операций» / «Блэкетт, Патрик Мейнард Стюарт», INFORMS.
- Винер-фильтр (уточнение, сверено): секр. отчёт «Yellow Peril» 1942 → монография 1949; ур-е Винера–Хопфа (мин. среднеквадратичной ошибки); предок фильтра Калмана; Колмогоров независимо 1941; отказ — «A Scientist Rebels» (Atlantic, янв.1947). Тьюринг-1948 «Rounding-off errors…» — Oxford QJMAM 1(1):287–308.
- ⚠️ Отклонено (натяжки): Гёдель→крипто (это Нэш-1955, не Гёдель); middle-square→крипто; «Винер-криптограф» (однофамилец Michael J. Wiener).

## Дизайн анонса — типографика/вёрстка (арка «Питч», 2026-07-02)
> Ресёрч под полноширинный HTML-анонс «читаемый текст-герой». Канон — `zhurnal/2026-07-02_pitch/handoff-html/stil-kanon.md`.
- **USWDS Typography** — мера строки, поля; крупный кегль допускает более короткую меру: https://designsystem.digital.gov/components/typography/
- **CSS multi-column** (во всю ширину без длинных строк — колонки): MDN https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_multicol_layout · CSS-Tricks https://css-tricks.com/almanac/properties/c/columns/
- **International Typographic Style (Swiss)** — сетка + асимметрия, флаш-лефт, крупный кегль: https://en.wikipedia.org/wiki/International_Typographic_Style
- **Шрифты:** Lora (OFL) https://fonts.google.com/specimen/Lora · Lato (OFL) https://fonts.google.com/specimen/Lato
- Скиллы-опоры: `web-typography` · `refactoring-ui` (grayscale-first, один акцент) · `design-taste-frontend` (анти-центр, один десатурированный акцент).

---
_Источники собраны из рабочих файлов курса при аудите 2026-06-27 (`2-idei/`, `fakty/`). По мере работы — дополнять строкой и URL._
