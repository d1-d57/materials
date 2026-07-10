# Handoff: Illustration-aware генератор слайд-колод + папочная архитектура источника

## Session Metadata
- Created: 2026-07-09 20:22:29
- Project: /Users/ivanyakovlev/Documents/GitHub/materials
- Branch: buffon-zahod-01 (вся работа этой сессии — НОВЫЕ, неотслеживаемые файлы; существующие не трогались)
- Session duration: одна длинная сессия

> Ветка/коммиты выше относятся к ПРЕДЫДУЩЕЙ работе над buffon и к делу этой сессии отношения не имеют.

## Handoff Chain
- **Continues from**: None (fresh start)
- **Supersedes**: None

## Current State Summary

Построен `_generator/build_deck.py` — генератор на чистой stdlib, который собирает
папку-источник `<lecture>/src/` (текст слайдов в markdown + иллюстрации по файлу + палитра/шрифты
в одном месте + каркас) в один самодостаточный `index.html` канона `html-slides-studio`, с линтер-гейтом.
Две реальные лекции распилены в такие папки-источники как ЭТАЛОННЫЕ модельные проекты:
`dandelin/src/` (19 слайдов, SVG + 3D-главы three.js) и `buffon/src/` (23 слайда, canvas-симуляции lab.js
+ KaTeX). Обе пересобираются **рендер-идентично** оригиналу (доказано; пользователь подтвердил глазами).
Текст 17/23 слайдов Бюффона и 12/19 Дандалена вынесен в редактируемый markdown со сценами и формулами.
Задача по сути ЗАВЕРШЕНА; дальше — переработка скилла html-slides-studio под эту архитектуру.

## Codebase Understanding

## Architecture Overview

Колоды канона — самодостаточный HTML из 4 блоков: `[1]` токены+шрифты(base64), `[2]` слайды
(`<section class="slide" id data-scenes>` с зонами-грид, текст в `.copy`/`.t-body`, иллюстрации — пустые
`<div data-ill>`), `[3]` реестр ассетов (`<template id="ill-*">`), `[4]` движок (fit/сцены/клавиши), копируется дословно.

**Идея генератора (проста и без потерь):** он — верный ассемблер + один «умный» рендер текста + линтер.
`shablon.html` = оригинал колоды, где каждый извлечённый кусок заменён НА МЕСТЕ плейсхолдером `{{TOKEN}}`;
сборка = обратная подстановка байтами файлов (иллюстрации/движок/шрифты/симуляции — дословно), и ТОЛЬКО
текст зон рендерится из `content/*.md` (`render_md`). Поэтому всё, кроме текста, round-trip'ится побайтово.
Формулы KaTeX в тексте пишутся как `$\boldsymbol{p}$`, а их готовый HTML берётся из кэша `buffon/src/math/katex.json`,
собранного `harvest_katex.py` из самой колоды (никакого KaTeX-рантайма — stdlib).

## Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| `_generator/build_deck.py` | Генератор (src → index.html) + линтер. ~300 стр stdlib | ГЛАВНЫЙ |
| `_generator/DESIGN.md` | Контракт папки-источника, блоки, линтер, границы | Спека |
| `_generator/SLIDE-FORMAT.md` | Диалект текста слайда (сцены/формулы/шторки/списки) | Спека формата |
| `_generator/harvest_katex.py` | Собирает `{tex: html}` кэш формул из готовой колоды | Инструмент |
| `_generator/render.py` | Локальная пиксельная сверка (Chrome+playwright — на машине пользователя) | Проверка |
| `_generator/README.md` | Как пользоваться, рабочий цикл правок | Док |
| `_generator/_snapshots/*.tar.gz` | Снапшоты оригиналов dandelin/buffon до работы | Бэкап |
| `dandelin/src/` | Эталон 1: content/, illustrations/, chapters/, drivers/, lib/three, engine.js, tokens.css, shablon.html, brief.md | Модель |
| `buffon/src/` | Эталон 2: то же + sims/(lab.js+ext), math/katex.json; без 3D | Модель |
| `dandelin/index.html`, `buffon/index.html` | ОРИГИНАЛЫ (не трогать, эталон сверки) | Только чтение |

## Key Patterns Discovered

- Проверка «рендер-идентичности» БЕЗ браузера: снять HTML-комментарии + схлопнуть пробелы (`re.sub(r'>\s+<','><')`,
  `re.sub(r'\s+',' ')`) в обоих файлах и сравнить как строки. Это строже пиксельной сверки (тот же DOM на входе).
- Плейсхолдеры в `shablon.html` разрешаются несколькими проходами (вложенность: глава несёт `{{DRIVER:NN}}`).
- Инвариант канона: КАЖДАЯ `var(--x)` должна быть в `tokens.css`, иначе SVG зальётся чёрным (линтер это ловит).
- `_attrs_from_tag` печатает атрибуты В ПОРЯДКЕ токенов тега → можно воспроизвести и `class="x" data-scene-*` и наоборот.

## Work Completed

## Tasks Finished

- [x] Разведка: реальный формат — не matema-fest/v-poiskah (это отдельный сайт), а materials/{dandelin,buffon}
- [x] DESIGN.md — контракт источника и генератора (Opus-проектирование)
- [x] build_deck.py — генератор + линтер-гейт (stdlib)
- [x] Dandelin: M1 дословный распил (byte-identical, sha `69812415…`) → M2 текст в markdown; render-neutral PASS
- [x] Buffon: M1 (byte-identical, sha `c0c9b846…`) → M2 текст в markdown (3 параллельных субагента); render-neutral PASS
- [x] Формат текста со сценами (`{@N}`, `{@N|…}`, `{fill@K|…|…}`, `\`-переносы, `{.cls}`-списки)
- [x] Кэш формул `$tex$` (harvest_katex.py, 38 формул) + рендер из кэша в генераторе
- [x] Полиш генератора: сохранение порядка атрибутов → дожаты sl-yellow, sl-circle; обе колоды render-neutral

## Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| (только НОВЫЕ файлы под `_generator/`, `dandelin/src/`, `buffon/src/`) | созданы с нуля | эталоны + инструмент |
| существующие файлы репо | НЕ трогались | оригиналы — эталон сверки |

## Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| Иллюстрации инлайнятся при сборке, но живут как отдельные файлы | инлайн vs подгрузка | выход обязан быть самодостаточным; правка одной илл. = один файл |
| Текст в markdown, сомнительное — дословным HTML (escape-hatch) | md-пуризм vs верность | верность (пиксель-гейт) важнее охвата |
| Формулы: `$tex$` + кэш из колоды | сырой KaTeX-HTML inline / opaque-маркер / рантайм | чисто для правок Claude'ом, self-describing, stdlib |
| Гейт = рендер-идентичность по нормализации | скриншоты | в песочнице нет браузера; нормализация строже и быстрее |

## Pending Work

## Immediate Next Steps

1. **Переработать скилл `html-slides-studio` под эту архитектуру** — папка-конвейер, где каждый шаг (идея → research →
   раскладка на слайды → сценарий → стиль → вёрстка → текст → иллюстрации) даёт свои файлы и свой скилл. Опираться на
   два готовых эталона (`dandelin/src`, `buffon/src`) как на «как должно выглядеть в финале».
2. (Опц.) Дожать остаток охвата Бюффона: sl-polygons p2/p3 (формуло-плотные) и «span-acc» акценты — для чистоты нужен
   шорткат `blur-reveal` и настраиваемый тег акцента (`<span class="acc">` vs `<b class="acc">`) в brief.md.
3. (Будущее, не срочно) Отдельная программа-редактор «слева рендер — справа текст» для правок без Claude.

## Blockers/Open Questions

- [ ] Нет: задача-ядро закрыта. Открытый архитектурный вопрос — форма конвейера скилла (шаги/арки и их скиллы).

## Deferred Items

- Шорткаты формата для нестандартных `blur-reveal`-шторок и `<span class="acc">` — отложены (работают через escape-hatch).
- Настоящий KaTeX-рендер новых формул (которых нет в колоде) — это будущий «math-арк» конвейера.

## Context for Resuming Agent

## Important Context

Право на правки текста в этой системе — у CLAUDE, не у пользователя вручную: пользователь смотрит собранные слайды и
говорит «поменяй это слово / сократи здесь», а Claude правит `content/*.md` и пересобирает. Поэтому главное требование —
чтобы правка слова НЕ требовала лезть в код, не относящийся к содержанию. Формат ровно на это и заточен: проза + короткие
`$tex$` + `{@N}`-сцены в маленьком файле на слайд. Рабочий цикл: правишь `content/<id>.md` (или `illustrations/<имя>.svg`,
или палитру в `tokens.css`) → `python3 _generator/build_deck.py <lecture>/src` → `<lecture>/src/dist/index.html`.

## Assumptions Made

- Задеплоенные версии лекций совпадают с `dandelin/index.html` / `buffon/index.html` в репо (эталон сверки).
- «Рендер-идентичность» (тот же DOM после нормализации) достаточна как критерий «выглядит так же».

## Potential Gotchas

- Колоды по ~3 МБ — НИКОГДА не читать целиком (контекст); только `sed -n`/`grep -n`, исключая base64.
- Байт-в-байт оригинал воспроизводит `build_deck.py <src> --no-banner`; по умолчанию добавляется render-neutral баннер-коммент.
- Порядок атрибутов важен для строгой сверки — использовать `{.cls @N}` vs `{@N .cls}` по факту оригинала.
- В оригинале Бюффона есть баг — лишний `</span>` в sl-yellow; он ВОСПРОИЗВЕДЁН дословно (не «чинить»).
- Акцент Бюффона — `<span class="acc">` (не `<b class="acc">`); в md он пишется сырым HTML.
- `$tex$` работает только для формул, которые ЕСТЬ в `buffon/src/math/katex.json` (собран из колоды). Новые — линтер пометит MISSING-MATH.

## Verification

- Финальная сверка: `python3 _generator/build_deck.py <src>` собирает, затем нормализованное сравнение с оригиналом → PASS.
- Пиксельно (на машине пользователя, есть Chrome+playwright): `python3 _generator/render.py --compare <orig> <rebuilt> _render`.

## Environment State

## Tools/Services Used
- Python 3 stdlib только (re, json, base64, pathlib, argparse). Ни pip, ни сети, ни фреймворков.
- Песочница генератора БЕЗ браузера — скриншоты только на машине пользователя.

## Active Processes
- Нет.

## Environment Variables
- Нет (секретов не используется).

## Related Resources
- `_generator/DESIGN.md`, `_generator/SLIDE-FORMAT.md`, `_generator/README.md`
- Скилл `html-slides-studio` (канон формата; кандидат на переработку под эту архитектуру)
- Снапшоты: `_generator/_snapshots/`
