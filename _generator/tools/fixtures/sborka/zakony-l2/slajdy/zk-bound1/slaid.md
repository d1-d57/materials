<!--
ЧТО ДАЛЬШЕ С ЭТИМ ФАЙЛОМ (фикстура захода zakony-v-gejt — не порождена
bootstrap_lekcii.py, писана руками ради изоляции одного закона на карточку).
ФАЗА 1 (интервью): x :: python3 _generator/sborka/gejt_kartochki.py --faza 1 <лекция>
ФАЗА 2 (раскадровка): x :: python3 _generator/sborka/gejt_kartochki.py --faza 2 <лекция>
ФАЗА 2.5 (смета вмещения): x :: python3 _generator/sborka/smeta.py --byudzhet x x
ФАЗА 3 (текст слайдов): x :: python3 _generator/sborka/gejt_kartochki.py <лекция>
ФАЗА 3.1 (смета по написанному): x :: python3 _generator/sborka/smeta.py <лекция>
ФАЗА 3.5 (кэш формул): x :: node _generator/sborka/kesh_formul.js <лекция>
ФАЗА 3.9 (вмещение): x :: python3 _generator/sborka/gejt_vmeshcheniya.py x
ФАЗА 4 (вёрстка): x :: python3 _generator/sborka/slaid.py <лекция>/slajdy/x -o /tmp/x.html
ФАЗА 5 (иллюстрации): x :: python3 _generator/sborka/gejt_kartochki.py <лекция>
ФАЗА 6 (сборка и QA): x :: python3 _generator/sborka/deck.py <лекция> -o <лекция>/dist/index.html
-->
---
imya: zk-bound1
nazvanie: zk-bound1
zagolovok_na_ekrane: ""
tip_idei: narrative
zachem: фикстура закона
akcent: фикстура закона
centralnyj_blok: perechislenie
kommentarij_lektoru: ""
minuty: 5
vazhnost: opornyj
byudzhet_slov: 200
tip_verstki: tolko_tekst
liniya: 100
matematika_iz: []
illustracii: []
vvodit: []
opiraetsya_na: []
bez_opredeleniya_namerenno: []
status: v_deke
---

## Математика — развёрнуто
### [opredelenie] zk-bound1-о
**Определение (zk-bound1).** формула $x=1$.

> поле:mn мораль

### [utverzhdenie] zk-bound1-у
**Утверждение (zk-bound1).** формула $x=1$.

> поле:mn мораль

## Текст слайда — сжато
### [opredelenie] zk-bound1-о
Текст. формула $x=1$.

### [utverzhdenie] zk-bound1-у
Текст. формула $x=1$.

## Правки
- фикстура
