<!--
ЧТО ДАЛЬШЕ С ЭТИМ ФАЙЛОМ (вшито bootstrap_lekcii.py — не редактировать руками,
gejt_kartochki.py краснеет на отсутствии этого блока или неполном наборе фаз).
Формат строки: ФАЗА N (имя фазы): что делается :: команда.

ФАЗА 1 (интервью): назвать nazvanie/tip_idei (типы — formaty.TIPY_IDEI)/zachem (идея одной фразой)/minuty, разметить блоки в ОБОИХ разделах — ### [tip] мысль, тела ещё пустые — и назвать centralnyj_blok :: python3 _generator/sborka/gejt_kartochki.py --faza 1 <лекция>
ФАЗА 2 (раскадровка): решить tip_verstki/liniya/akcent/vazhnost/byudzhet_slov в шапке, написать тела блоков «Математика — развёрнуто» по разметке фазы 1 :: python3 _generator/sborka/gejt_kartochki.py --faza 2 <лекция>
ФАЗА 3 (текст слайдов): написать «Текст слайда — сжато» тем же составом блоков, что в «Математике» :: python3 _generator/sborka/gejt_kartochki.py <лекция>
ФАЗА 4 (вёрстка): собрать и посмотреть слайд отдельно :: python3 _generator/sborka/slaid.py <лекция>/slajdy/zamena-bazisa -o /tmp/zamena-bazisa.html
ФАЗА 5 (иллюстрации): назвать файлы в illustracii, положить risunok.svg (или risunok.html) в <лекция>/illustracii/<имя>/ :: python3 _generator/sborka/gejt_kartochki.py <лекция>
ФАЗА 6 (сборка и QA): собрать весь дек — типографика подбирается автоматически, явные kegl_px/liniya в шапке не перетираются :: python3 _generator/sborka/deck.py <лекция> -o <лекция>/dist/index.html
-->
---
imya: zamena-bazisa
nazvanie: Замена базиса
zagolovok_na_ekrane: заполнить
tip_idei: definition
zachem: школьная формула замены базиса оказывается квадратом, и у этого есть имя
akcent: заполнить
centralnyj_blok: формула перехода есть квадрат, и это естественный изоморфизм
kommentarij_lektoru: заполнить
minuty: 7
vazhnost: opornyj
byudzhet_slov: заполнить
tip_verstki: заполнить
liniya: заполнить
matematika_iz: []
illustracii: []
vvodit: []
opiraetsya_na: []
bez_opredeleniya_namerenno: []
status: v_deke
---

## Математика — развёрнуто
### [narrativ] выбор базиса как конструкция на всей категории

### [utverzhdenie] эта конструкция есть функтор

### [narrativ] другой базис даёт другой функтор

### [opredelenie] формула перехода есть квадрат, и это естественный изоморфизм

## Текст слайда — сжато
### [narrativ] выбор базиса как конструкция на всей категории

### [utverzhdenie] эта конструкция есть функтор

### [narrativ] другой базис даёт другой функтор

### [opredelenie] формула перехода есть квадрат, и это естественный изоморфизм

## Правки
- 2026-08-08 · разметка фазы 1 внесена из RAZMETKA-L2.md
