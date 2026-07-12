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
  - s04-recur
  - s05-cols
  - s03-task2
  - s08-subset
  - s07-code
  - s-modelD
  - s-modelE
  - s09-perm
  - s-modelG
  - s13-hwalk
  - s-langs
  - s10-sum
  - s11-square
  - s12-zeck
---

# fibonacci — источник дека (курс «Числа Фибоначчи»)

Лекция 1 целиком — 16 слайдов (8 моделей A–H + обложка/задачи/обзор/пуанта), роутер и порядок — `../SPEKA.md` слой 2. Полный курс (3 лекции) — в `../raskadrovka/PLAN.md`. Раскадровка — стадия 5; наполнение (текст/сцены/интерактив) — Фаза II.

## Регистр и бюджет (контракт 5→6)
- register: читаемый (семинар-разбор; условие с экрана, доказательство — canvas без текста).
- word_budget_per_slide: 40 (доказательства бессловесны → тексты короткие; край 50; у «Обзора» — named-исключение, 7 определений).

## Единый интерактив
Один canvas-kind `fib-strip` (в `sims/lab.core.js`); режим — `data-mode` (tiling/code/subset/perm/compGE2/compOdd/zigzag/hwalk/sum/firstsq/zeck/cassini). Полоска редактируется (клик по клетке), образ под соответствием обновляется живьём; модели A–H дополнительно шагают по `data-stages` (empty/examples/recur/bijection). §4 захода: «придумай один механизм и переиспользуй».

## accent_tag
`span` (buffon-стиль, дефолт канона Р16).
