<!--
ЧТО ДАЛЬШЕ С ЭТИМ ФАЙЛОМ (фикстура захода kod_rebra-blokov.md, Э2 — не порождена
bootstrap_lekcii.py, писана руками ради изоляции: блок [primer] есть, а
'primer_dlya' пусто — гейт обязан дать ЖЁЛТУЮ (не красную) Э2-клаузу «пример без
адресата». Изоляция та же, что у соседней карточки этой фикстуры.
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
imya: primer-bez-adresata
nazvanie: primer-bez-adresata
zagolovok_na_ekrane: ""
tip_slaida: Т1
zachem: фикстура Э2 — пример без адресата
akcent: фикстура
centralnyj_blok: определение
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
dokazatelstvo_opiraetsya_na: []
primer_dlya: []
status: v_deke
---

## Математика — развёрнуто
### [opredelenie] определение
**Определение (раз).** формула $x=1$.

> поле:mn мораль

### [primer] пример
**Пример (раз).** формула $x=1$.

> поле:mn мораль

## Текст слайда — сжато
### [opredelenie] определение
Текст определения. формула $x=1$.

### [primer] пример
Текст примера. формула $x=1$.

## Правки
- фикстура Э2 kod_rebra-blokov.md
