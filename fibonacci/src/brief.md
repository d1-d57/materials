---
id: fibonacci
title: "Числа Фибоначчи"
canvas: 1440x810
provenance: greenfield
milestone: greenfield (нет provenance_sha256 → render-identity гейт неприменим на 1-й сборке; замена — линтер + audit.py + глаз)
accent_tag: span
register: читаемый
word_budget_per_slide: 40
slide_order:
  - s01-title
  - s02-hook
  - s03-strip
  - s04-recur
  - s08-subset
  - s07-code
  - s09-perm
  - s13-hwalk
  - s10-sum
  - s11-square
  - s12-zeck
---

# fibonacci — источник дека (курс «Числа Фибоначчи»)

Реализуемый ночным прогоном срез из 12 слайдов (сквозная дуга нити). Полный курс (3 лекции) — в `../raskadrovka/PLAN.md`. Раскадровка — стадия 5; наполнение (текст/сцены/интерактив) — Фаза II.

## Регистр и бюджет (контракт 5→6)
- register: читаемый (семинар-разбор; условие с экрана, доказательство — canvas без текста).
- word_budget_per_slide: 40 (доказательства бессловесны → тексты короткие; край 50).

## Единый интерактив
Один canvas-kind `fib-strip` (в `sims/lab.core.js`); режим — `data-mode` (recur/code/subset/perm/sum/cassini). Полоска редактируется (клик по клетке), образ под соответствием обновляется живьём. §4 захода: «придумай один механизм и переиспользуй».

## accent_tag
`span` (buffon-стиль, дефолт канона Р16).
