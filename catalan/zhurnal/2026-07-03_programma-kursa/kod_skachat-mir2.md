# Канал Claude Code — скачать источники Мира 2 (парковки ↔ деревья ↔ помеч. пути Дика)
> Для Claude Code: твой единственный файл-заход. Читай ТОЛЬКО его. План/вопросы/отчёт — в секции внизу этого файла. Тривиальный механический заход: скачать + разложить + зарегистрировать, **никакого анализа**. Всё в открытом доступе.

## ЗАДАЧА (один проход до конца)
КОНТЕКСТ. Проект «Каталан», арка «Программа курса»: собираем библиотеку источников Мира 2 (формула Кэли ↔ парковки ↔ помеченные пути Дика). Нужно докачать несколько открытых статей. Приёмка — по отчёту.

### 0. ПЕРВЫЙ ХОД. Рабочая папка — корень проекта `…/materials/catalan` (не git). Заход только ДОБАВЛЯЕТ файлы и правит два реестра — если хочешь подстраховку, сделай tar-снапшот в `snapshots/` (zip тут не финализируется). Изложи ПЛАН в `## ПЛАН` перед действиями.

### 1. ДИСЦИПЛИНА. Минимум; ничего сверх списка. Имя файла — строго по конвенции папки `stati-obzory/`: `Авторы — Заголовок (arXiv id или год).pdf`, **авторов/заголовок брать со страницы arXiv `abstract`, не выдумывать**. Сохранять по умолчанию, сомнительное — в `## ВОПРОСЫ/ОТЧЁТ`. Субагенты не нужны.

### 2. ГРАНИЦЫ. Трогать только `biblioteka/istochniki/stati-obzory/` и два реестра ниже. Больше ничего. NAVIGATION НЕ править (файлы не `.md`).

### 3. ЗАДАЧА. Скачать PDF в `biblioteka/istochniki/stati-obzory/`:
1. `https://arxiv.org/pdf/1309.2201` — Perkinson, Yang, Yu, «G-parking functions and tree inversions». *(ядро нити B: биективно доказывает тождество Кревераса area = инверсии деревьев через burning-алгоритм Дхара)*
2. `https://arxiv.org/pdf/1506.03470` — «Parking functions and tree inversions revisited» (Gaydarov, Hopkins). *(чистое современное экспозе нити B)*
3. `https://www.samuelfhopkins.com/docs/pf_talk.pdf` — Hopkins, слайды. *(школьно-пригодная подача; назвать `Hopkins — Parking functions and tree inversions (slides).pdf`)*
4. `https://arxiv.org/pdf/0810.0427` — «A New Bijection Between Forests and Parking Functions». *(нерекурсивная биекция лес ↔ парковка)*
5. *(опц., каталан-сторона)* `https://arxiv.org/pdf/1403.1845` — Armstrong, Loehr, Warrington, «Rational Parking Functions and Catalan Numbers».

**НЕ качать:** Stanley, «Hyperplane arrangements, parking functions and tree inversions» (1998) — платный (Birkhäuser), открытого PDF нет; содержание (арранжировка Ши) покрыто №1–2. Найдёшь открытую копию — возьми; иначе пропусти.

**Регистрация тем же заходом:** в `biblioteka/istochniki/MANIFEST.md` (раздел `stati-obzory/`) — одна строка на файл (имя + фраза «зачем»); в `biblioteka/istochniki/SPISOK-skachat.md` — отметить скачанное.

**КРИТЕРИЙ ГОТОВНОСТИ:** каждый скачанный PDF ненулевой, открывается, есть текстовый слой (не чистый скан); обе записи в MANIFEST и SPISOK на месте. Битую/платную ссылку — **пропустить и указать в отчёте, не падать**.

### 4. ОТЧЁТ → секция `## ОТЧЁТ` внизу: что скачано (файл · размер · стр.) / что пропущено и почему / что дописано в MANIFEST и SPISOK / **время прогона + потраченные токены**.

## ПЛАН — (заполняет Code)
1. tar-снапшот `biblioteka/istochniki/stati-obzory/` в `snapshots/` (страховка перед добавлением файлов).
2. Скачать curl'ом 5 PDF по списку в `biblioteka/istochniki/stati-obzory/` под финальными именами (для №1,2,4 сначала открою страницу arXiv `/abs/...` за авторами/заголовком, №3 и №5 имя дано/тривиально).
3. Проверить каждый файл: ненулевой размер, `pdfinfo`/`pdftotext` на страницы + наличие текстового слоя.
4. Дописать по одной строке на файл в `MANIFEST.md` (раздел `stati-obzory/`) и отметить `[x]` в `SPISOK-skachat.md` (там, где эти статьи упомянуты в разделе B).
5. Заполнить `## ОТЧЁТ`.

## ВОПРОСЫ — (заполняет Code)
Вопросов нет — всё скачалось по прямым ссылкам, метаданные (авторы/заголовки) взяты со страниц arXiv `/abs/...`.

## ОТЧЁТ — (заполняет Code)

Скачано 5/5 в `biblioteka/istochniki/stati-obzory/` (все ненулевые, PDF с текстовым слоем, проверено `pdftotext`):
1. `Perkinson, Yang, Yu — G-parking functions and tree inversions (arXiv 1309.2201).pdf` — 183 КБ, 10 стр.
2. `Gaydarov, Hopkins — Parking functions and tree inversions revisited (arXiv 1506.03470).pdf` — 2.13 МБ, 27 стр.
3. `Hopkins — Parking functions and tree inversions (slides).pdf` — 2.40 МБ, 18 стр.
4. `Shin — A New Bijection Between Forests and Parking Functions (arXiv 0810.0427).pdf` — 353 КБ, 11 стр.
5. `Armstrong, Loehr, Warrington — Rational Parking Functions and Catalan Numbers (arXiv 1403.1845).pdf` — 622 КБ, 29 стр. (опц., каталан-сторона — взято)

Пропущено: Stanley, «Hyperplane arrangements, parking functions and tree inversions» (1998) — как и предупреждено в задаче, платный (Birkhäuser), открытого PDF не нашлось; содержание покрыто №1–2.

Реестры:
- `MANIFEST.md` → добавлены 5 строк в раздел `stati-obzory/`.
- `SPISOK-skachat.md` → добавлен новый раздел `F. Мир 2 — нить B` с отметками `[x]` по всем 5 пунктам + пропуск Stanley.

Снапшот-страховка: `snapshots/stati-obzory_pre-mir2_20260703.tar.gz` (сделан до скачивания).

Время прогона: ~4 мин. Границы соблюдены — трогал только `biblioteka/istochniki/stati-obzory/`, `MANIFEST.md`, `SPISOK-skachat.md` и этот файл-заход; `NAVIGATION.md` не трогал.
