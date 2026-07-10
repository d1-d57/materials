# НАВИГАТОР арки «сборка конвейера»

## Концепция
Собрать реальный `_studio`-конвейер: 10 арк-файлов (паттерн SKILL.md) с контрактами вход→выход и гейтами, поверх замороженного канона и генератора. Цель-дедлайн — рабочая фабрика к завтрашним 4 лекциям (одна — многогранники); критичен путь ОТ готового содержания вниз.

## Границы (anti-scope)
Визуал/канон НЕ трогаем. Внешний скилл — только 3D/код/термины. Не строить вслепую: сперва дистилляты → потом сборка арк-файлов → потом проверка на реальном деке.

## Указатели в долгую
- План по классам + все задачи → `../../docs/sostoyanie/OTKRYTYE-ZADACHI.md`
- Дизайн + карта 10 шагов → `../../docs/spravka/ARHITEKTURA-FABRIKI.md`
- Блюпринт Фазы I (стадии 0–4, гибрид-источник) → `../../docs/spravka/FAZA-1-BLUEPRINT.md`
- Решения (Р1–Р14) → `../../docs/pochemu-i-videnie/RESHENIYA.md`
- Прайор-арт → `../../docs/spravka/PRAJOR-ART.md`

## Внешние источники (проверено 2026-07-10 — ЖИВЫ)
- **text-корпус** (эталон стиля, 5073 стр, 6 деков) → `content-studio/assets/corpus/texts-corpus.md` + `content-studio/references/slide-voice.md`. Философия корпуса = наш Р4.
- **Вёрстка/канон/QA** → `html-slides-studio/references/{per-slide-algorithm,slide-engine,style-core,images,simulations,typography,math-render}.md`; 7 деков-разборов → `references/decks/*.md`; `assets/deck-skeleton.html`, `scripts/audit.py`.
- **Ресёрч/нарратив** → `popsci-research`, `popsci-narrative`; **иллюстрации 3D** → `threejs`; **термины** → `math-russian-terminology`.
- Эталоны финала → `../../../dandelin`, `../../../buffon`; генератор → `../../../_generator/build_deck.py`.

## Скиллы арки
general-purpose субагенты с инлайн-ролью (кастомные subagent_type в харнессе недоступны); `math-video-studio`/`manim` при нужде.

## Процедуры
вход в сессию → `../../docs/kak-delat/ARKA.md §3` · план → §4 · заход исполнителю → `../../docs/kak-delat/RUKOVODSTVO-zahodami.md` · хэндофф → §6 · закрытие → §7.
