# PRAJOR-ART — находки ресёрча (что украсть / чего избежать)

> **КОГДА читать:** нужно обоснование архитектурных решений или прайор-арт по теме. · **ЧТО дописывать сюда:** новые находки ресёрча со ссылками. · **КУДА дальше:** решения — `../pochemu-i-videnie/RESHENIYA.md`.

Пресс-тест нашей схемы против мира (5 углов). Вывод: фундамент верный — наша схема совпала с конвергенцией зрелых систем.

## 1. Slides-as-code
Ближайший близнец — **Quarto**: тема из двух слоёв (`defaults`=токены / `rules`=структура) + `embed-resources` инлайнит в один самодостаточный HTML. reveal — скоупинг стилей под `.reveal`; Marp — global (headmatter) vs per-slide; Typst — set/show, но выход PDF; Slidev — Vue/Vite SPA с недетерминированными хэшами (враг render-identity).
→ **ADOPT** слой-токенов vs слой-правил, скоупинг, global/per-slide. **AVOID** фреймворк-движки. Наш stdlib-инлайнер — преимущество.

## 2. Math → static HTML (→ Р7)
Чистого stdlib-пути НЕТ. Прагматика — Node `katex.renderToString`, версия pinned, тот же `{tex→html}` кэш, уже вшитые css+woff.
→ **ADOPT** изолированный Node+katex, батчем только промахи, стабильный JSON. **AVOID** рантайм KaTeX/MathJax; SVG-движки (несовместимый markup).

## 3. Design-tokens (→ Р8)
Модель Style Dictionary 1:1: include(канон)+source(оверрайд) → deep-merge → resolve alias → CSS `:root`. Тиры primitive→semantic→component; деки читают ТОЛЬКО semantic. Merged `:root` инлайнить (не `<link>`).
→ **ADOPT** primitive→semantic + свой ~50-строчный stdlib-эмиттер + DTCG-подобная форма. **AVOID** Style Dictionary/npm, внешний tokens.css.

## 4. Agent-пайплайны (→ Р9)
Наша схема на линии конвергенции. Уточнения: трёхуровневый арк-файл (SKILL.md); reference-not-inline; REPORT-дистиллят 1–2k; явный `next`+checkpoint, готовые заходы = чекпойнты; гейт внутри арки.
→ **ADAPT** дома = durable Store, заход = ephemeral checkpointer. **AVOID** инлайн апстрим-контекста вниз, память сессии как канал, тяжёлый walker, тихий «done».

## 5. Иллюстрации (→ Р10)
Каждая илл. — свой `.svg`, инлайн живой `<svg>` (не base64): до неё дотягиваются `var()`/`currentColor`; в `<img>`/data-URI изолирован → чёрная заливка (наш баг).
→ **ADOPT** inline-`<svg>` + SVGO (pinned + per-file id-prefix) + headless-гейт (пустая/одноцветная зона). **AVOID** base64 для SVG; `var()` внутри `<img>`; «нет ошибки = отрисовалось».

## Источники
- Quarto [embed-resources](https://quarto.org/docs/output-formats/html-publishing.html) · Typst [set/show](https://typst.app/docs/reference/styling/)
- KaTeX [Node/renderToString](https://katex.org/docs/node) · [common issues](https://katex.org/docs/issues)
- [Style Dictionary](https://styledictionary.com/info/architecture/) · [W3C DTCG](https://www.designtokens.org/tr/drafts/format/)
- [Anthropic — context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) · [Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) · [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) · [12-factor agents](https://github.com/humanlayer/12-factor-agents)
- [Base64 SVG (CSS-Tricks)](https://css-tricks.com/probably-dont-base64-svg/) · [SVGO](https://svgo.dev/) · [reproducible builds](https://reproducible-builds.org/docs/deterministic-build-systems/)

## Источники для научпоп-геометрии (6 кл, кружковый формат) — арка geometria-6
Проверено в арке `2026-07-11_geometria-6-nagliadnaya`.
- **Кружки МЦНМО** — `old.mccme.ru/circles/mccme/<год>/<класс>/` — листки по классам/темам (6 кл, geom_7); базовый источник простых наглядных задач.
- **Квантик** — `kvantik.com` — журнал 4–8 кл, визуально, целевой возраст; рубрикатор статей Квант+Квантик по темам.
- **Квант** — `kvant.mccme.ru` (зеркало `kvant.digital`) — наглядные научпоп-статьи.
- **Математические этюды** — `etudes.ru`, `en.etudes.ru/models` — визуальные модели (Мёбиус, Рёло, конические, многогранники, паркеты). «Математическая составляющая» — `book.etudes.ru` — вау-эссе (напр. Рёло).
- **Книги:** **Шарыгин-Ерганжиева «Наглядная геометрия 5–6»** (МИРОС 1992) — якорь, покрывает почти все наглядные темы; **Мерзон-Ященко «Длина, площадь, объём»** (МЦНМО) — масштаб/размерность, готовые листки; Гарднер (головоломки); Кадзуо Хага «Оригамика».
- **Готовые листки с решениями:** «Математический театр» (sch2000).
- **Тематически:** `elementy.ru/problems`, `n+1`, Habr; Г. Мерзон «Оптическое свойство» (`dev.mccme.ru/~merzon`).

Метод: рус. приоритет, по темам, гейт доступности 6 кл, регистрация в реестре зоны. Как искать — `../kak-delat/RESERCH-ZADACH.md` (метод) + `BAZY-ZADACH.md` (общая карта задачных баз — этот геосписок входит в неё частным случаем) + `../kak-delat/PROGRAMMA-KURSA.md`.

---
*Находки ресёрча. Что из них решено — `../pochemu-i-videnie/RESHENIYA.md` (Р7–Р10).*
