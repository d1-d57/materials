---
opisanie: промпт для ChatGPT — аватарка канала «Пути и волны», концепция К2 «Хребты Каталана» (решение владельца 04.10 02:19–02:25); три картинки-референса и правки для итераций
status: zhivoy
---

# Аватарка — промпт К2 «Хребты Каталана»

**Что прикладывать** (папка `referensy/`, в таком порядке):
1. `1-kompoziciya.png` — базовая композиция, собрана кодом (`kompoziciya.py`): хребты — настоящие пути Дика (шаги под 45°, ни одна точка не ниже воды), под водой — отражение, к низу рассыпается рябью.
2. `2-hokusai-krasnaya-fudzi.jpg` — техника и цвет гор (Хокусай, «Ветер с юга, ясное утро», общественное достояние).
3. `3-hokusai-bolshaya-volna.jpg` — техника воды и цвет неба (Хокусай, «Большая волна в Канагаве», общественное достояние).

Если бесплатная версия не примет три картинки — приложить 1 и 2, а из промпта убрать строки про image 3.

## Промпт

```
I attach three images. Use them in these roles:
– Image 1 is the COMPOSITION. Keep its layout exactly: the waterline position, the mountain silhouettes, their proportions, the reflection below. Re-render it; do not trace its flat colors.
– Image 2 is the TECHNIQUE AND COLOR for the mountains: Japanese woodblock print, flat carved color planes, the warm red slope that darkens to a deep brown crown near the summit, crisp white snow with streaks running down from the peaks, subtle paper grain.
– Image 3 is the TECHNIQUE for the water and the SKY COLOR: layered Prussian-blue water with fine ornamental carved lines, and the pale warm paper sky.

Square 1:1 image, 1024×1024, a Telegram channel avatar. All important content sits inside a centered circle occupying about 85% of the canvas; the corners are expendable.

Subject: a red mountain range above still deep-blue water, made of mathematical lattice paths.
– The mountain ridgelines are piecewise-straight: every slope is a straight segment at exactly 45 degrees, rising and falling in equal steps like a path drawn on squared paper. They start and end on the waterline and NEVER go below it. One tall central peak, smaller peaks on both sides, a paler blue-grey ridge further back.
– Snow caps on the higher peaks: bright white, with a carved jagged lower edge and a few thin streaks running down the slopes.
– A perfectly horizontal waterline slightly below the center.
– Below it: the exact mirror reflection of the mountains, sharp near the waterline, then breaking downward into horizontal ripple bands; at the bottom the reflection is gone and only calm sinusoidal wave lines remain — the mountains turn into waves.
– Sky: pale warm paper, almost empty; at most a faint dotted grid, barely visible.

Palette, strictly: mountains vermilion-red #BE3A22 darkening to #5C2014 at the crowns; snow #F8F4EA; back ridge #7C96B6; water Prussian blue #1E4E8C deepening to #102E5C; sky paper #F1E6CF. Nothing else — no green forest, no blue sky.

Style: an authentic Japanese woodblock print — flat layered color planes, crisp carved edges, slight registration texture and washi paper grain — but strictly geometric and minimal, contemporary in its clarity. Bold large shapes.

Small-size readability: shrunk to 48 px it must still read as a red mountain with a white summit over deep-blue water on a light background.

Do not include: any text, letters, digits, seals, stamps, cartouches or signatures (the reference prints have a title cartouche — leave it out); boats, people, birds, trees, buildings, the sun; foaming claw-like wave crests; clouds; watermark, logo, frame; photographic realism; 3D rendering; lens flare.
```

## Если вышло не то

- **Горы стали «природными»** (скалы, плавные склоны): «Make every slope a perfectly straight 45-degree segment, like a graph on squared paper; remove all rock texture and curves.»
- **Исчезло отражение или оно сразу волны:** «Keep the mirror reflection sharp for the first third below the waterline, then break it into horizontal ripple bands, then only wave lines.»
- **Пестро, в 48 px каша:** «Simplify: fewer peaks, larger shapes, fewer wave lines, keep only red, white, blue and the paper sky.»
- **Слишком похоже на копию Хокусая** (конус Фудзи, пенные когти волн): «It must not imitate any specific print: keep only the stepped lattice-path ridges and calm ripples; no claw-like foam.»
- **Появился текст или печать:** «Remove all text, seals and cartouches.»

## Проверка картинки

Сжать до 48 px (или посмотреть в списке чатов Telegram): читается «красная гора с белой вершиной над синей водой на светлом фоне». Горы не опускаются ниже воды; склоны прямые.

## Добивка к v1 (04.10, 02:40) — отправлять в тот же чат

v1 — `generacii/v1.png`. Получилось: палитра, гравюра, прямые склоны, отражение → волны. Не так: горы сливаются с небом (красный против кремового — слабый контраст по светлоте), снег мелкий и не светлее неба, на холсте нарисован второй круг.

```
Very good — keep the composition, the mountains, the reflection and the water exactly as they are. Change only this:

1. Make the snow the brightest thing in the picture, so it seems to glow by itself, like snow lit by low sun: pure brilliant white, larger caps (the top third of the central peak, the top quarter of the side peaks), crisp jagged lower edges, longer thin streaks down the slopes.
2. Separate the mountains from the sky: make the sky a deeper warm sand tone at the top (#DCC29A), graded down to pale paper near the summits — a soft woodblock bokashi gradation that is lightest directly behind the snowy peaks, so the summits radiate light. Add a thin dark indigo keyline (#1C2340) along every ridge, like the key block of a woodblock print. Slightly more saturated red on the slopes.
3. Remove the drawn inner circle and its border: the paper background must fill the whole square evenly, edge to edge (Telegram crops the circle itself).

Still no text, no seals, no lens flare, no sparkles, no sun.
```
