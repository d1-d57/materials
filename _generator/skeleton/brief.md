---
id: novyj-dek
title: "Новый дек"
canvas: 1440x810
provenance: greenfield
milestone: greenfield (нет provenance_sha256 → render-identity гейт неприменим на 1-й сборке; замена — линтер + audit.py + глаз)
accent_tag: span
slide_order:
---

# <дек> — источник (скелет greenfield)

Стартовая папка нового дека Фазы II. Скопирована из `_generator/skeleton/`
(шаг 0 «скопируй скелет», выход раскадровки арки 5).

## Что заполнить
- `accent_tag`: `span` (buffon-стиль, дефолт канона — Р16) или `b` (dandelin-стиль) — тег для `**acc**`.
- `slide_order`: перечислить id СОДЕРЖАТЕЛЬНЫХ слайдов В ПОРЯДКЕ показа (по одному `- <id>` на строку).
  Обязан ТОЧНО покрывать `slides/` + `content/` (линтер-гейт, без сирот/дублей).
  Обложку, визитку и финал сюда НЕ вписывают — их вставляет генератор (см. ниже).
- **служебные слайды — полями, а не вёрсткой** (опц., «нет поля — нет элемента»):
  `cover_ill` — одна иллюстрация обложки · `cover_sub` — подзаголовок · `cover_date` · `cover_place` ·
  `final_ill` — одна иллюстрация финала · `vizitka: net` — единственный способ убрать визитку.
- `content/<id>.md` — текст слайда (маркдаун-диалект, `_generator/SLIDE-FORMAT.md`).
- `slides/<id>.html` — `<section class="slide" id="<id>" data-scenes="N">` с зонами и `{{MD:<id>}}`.
- пер-слайдовый грид `#<id> .grid{…}` — в `<style>` `shablon.html` (bespoke; общий канон — в `base.css`).
- `illustrations/<name>.svg|.html` — иллюстрации (арка 9); `tokens.css` — палитра при нужде.

## Что уже канон (не трогать без причины)
- `sluzhebnye/` (в `_generator/skeleton/`, НЕ копируется в дек) — обложка, визитка «Про меня» и финал
  «Спасибо за внимание»: порождаются генератором, руками их файлов не заводят. Правка биографии/фото/QR —
  в каноне, то есть сразу во всех деках. Рукописный `slides/sl-title|sl-vizitka|sl-thanks.html` перебьёт
  порождение и покраснеет гейтом G12.
- `base.css` — общий канон-CSS (структура `#stage/.slide/.zone/.fit`, сцены, `#hint`, роли текста `t-body/t-display/t-math`, `.panel/.lab-row/.sim-controls`).
- `engine.js` — движок дословно. `tokens.css` — канон-палитра. `fonts/faces.css` — 5 @font-face.

Сборка: `python3 ../disciplina/_generator/build_deck.py <дек>/src` → `dist/index.html`.
Гейт greenfield (1-я сборка): линтер + `audit.py` (браузер) + глаз (render.py). render-identity — со 2-й сборки.
