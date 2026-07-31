---
id: teorkat-l1
title: "Зачем нужны категории?"
canvas: 1440x810
provenance: greenfield
milestone: greenfield (нет provenance_sha256 → render-identity неприменим на 1-й сборке; замена — линтер + audit.py + глаз)
accent_tag: span
register: читаемый
word_budget_per_slide: 50
cover_sub: "Лекция 1"
cover_date: "29 июля 2026"
vizitka: da
slide_order:
  - sl-title
  - sl-vizitka
  - s01
  - s02
  - s03
  - s04
  - s05
  - s06
  - s07
  - s08
  - s09
  - s10
  - s11
  - s12
  - sl-thanks
---

# Дек лекции 1 курса «Зачем нужны категории?»

Манифест собран аналитиком 28.07.2026 как вход Фазы II (гейт G6). Скелет скопирован из `_generator/skeleton/`.

**Решения владельца, отражённые в полях.** Регистр **читаемый** — зал просил плотный текст ⇒ `word_budget_per_slide: 50`, это медиана эталонной ленты Паскаля, а не потолок. `accent_tag: span` — дефолт канона (Р16).

⚑ **`slide_order` пуст намеренно.** Порядок рождается в ленте (арка 6, `raskadrovka/teksty/*.md`) и переносится сюда заходом вёрстки `kod_verstka.md`: один `id` на каждый `## `-раздел ленты, в том же порядке. Служебные слайды (обложка, визитка, финал) в `slide_order` **не входят** — их порождает генератор из полей выше (G12).

⚑ **`cover_place` не заполнено** — название зала аналитику не известно. По правилу «нет поля — нет элемента» строки на обложке не будет; вписывает владелец.

Сборка: `python3 _generator/build_deck.py teorkat-vvedenie/src` → `dist/index.html`.
