<!--
ЧТО ДАЛЬШЕ С ЭТИМ ФАЙЛОМ (вшито bootstrap_lekcii.py — не редактировать руками,
gejt_kartochki.py краснеет на отсутствии этого блока или неполном наборе фаз).
Формат строки: ФАЗА N (имя фазы): что делается :: команда.

ФАЗА 1 (интервью): назвать nazvanie/tip_idei (типы — formaty.TIPY_IDEI)/zachem (идея одной фразой)/minuty, разметить блоки в ОБОИХ разделах — ### [tip] мысль, тела ещё пустые — и назвать centralnyj_blok :: python3 _generator/sborka/gejt_kartochki.py --faza 1 <лекция>
ФАЗА 2 (раскадровка): решить tip_verstki/liniya/akcent/vazhnost/byudzhet_slov в шапке, написать тела блоков «Математика — развёрнуто» по разметке фазы 1 :: python3 _generator/sborka/gejt_kartochki.py --faza 2 <лекция>
ФАЗА 3 (текст слайдов): написать «Текст слайда — сжато» тем же составом блоков, что в «Математике» :: python3 _generator/sborka/gejt_kartochki.py <лекция>
ФАЗА 4 (вёрстка): собрать и посмотреть слайд отдельно :: python3 _generator/sborka/slaid.py <лекция>/slajdy/bazis-i-matricy -o /tmp/bazis-i-matricy.html
ФАЗА 5 (иллюстрации): назвать файлы в illustracii, положить risunok.svg (или risunok.html) в <лекция>/illustracii/<имя>/ :: python3 _generator/sborka/gejt_kartochki.py <лекция>
ФАЗА 6 (сборка и QA): собрать весь дек — типографика подбирается автоматически, явные kegl_px/liniya в шапке не перетираются :: python3 _generator/sborka/deck.py <лекция> -o <лекция>/dist/index.html
-->
---
imya: bazis-i-matricy
nazvanie: Базис и матрицы
zagolovok_na_ekrane: заполнить
tip_idei: proof_step
zachem: вопрос об изоморфности в этой категории решается одним числом — размерностью
akcent: заполнить
centralnyj_blok: изоморфны ровно тогда, когда размерности равны
kommentarij_lektoru: заполнить
minuty: 8
vazhnost: opornyj
byudzhet_slov: заполнить
tip_verstki: заполнить
liniya: заполнить
matematika_iz: []
illustracii: [dva-bazisa]
vvodit: []
opiraetsya_na: []
bez_opredeleniya_namerenno: []
status: v_deke
---

## Математика — развёрнуто
### [utverzhdenie] координаты превращают линейное отображение в матрицу

### [narrativ] изоморфны ровно тогда, когда размерности равны

## Текст слайда — сжато
### [utverzhdenie] координаты превращают линейное отображение в матрицу

### [narrativ] изоморфны ровно тогда, когда размерности равны

## Правки
- 2026-08-08 · разметка фазы 1 внесена из RAZMETKA-L2.md
- 2026-08-09 · пересобрано после разбора владельцем: блоки спаяны вокруг одного центрального, нарративы возвращены отдельными блоками, порядок «сначала утверждение, потом материал»
