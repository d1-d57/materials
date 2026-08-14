<!--
ЧТО ДАЛЬШЕ С ЭТИМ ФАЙЛОМ (фикстура захода tipologia-odna-os, Э3 — не порождена
bootstrap_lekcii.py, писана руками ради изоляции: тип Т3 с [primer] ПЕРЕД
[utverzhdenie] (у Т3 utverzhdenie обязан быть первым — раскладка, не украшение)
обязан красить гейт клаузой «нарушенный порядок»). `dokazatelstvo_opiraetsya_na`
заполнено НАРОЧНО (заход kod_rebra-blokov.md, Э2) — изолирует от НОВОЙ клаузы
«доказательство без адресата», иначе замечаний стало бы два вместо одного.
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
imya: poryadok
nazvanie: poryadok
zagolovok_na_ekrane: ""
tip_slaida: Т3
zachem: фикстура Э3 — нарушенный порядок блоков
akcent: фикстура
centralnyj_blok: утверждение не первым
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
dokazatelstvo_opiraetsya_na: [poryadok:utverzhdenie]
primer_dlya: []
status: v_deke
---

## Математика — развёрнуто
### [primer] пример раньше утверждения
**Пример (раз).** формула $x=1$.

> поле:mn мораль

### [utverzhdenie] утверждение не первым
**Утверждение (два).** формула $x=1$.

> поле:mn мораль

### [dokazatelstvo] доказательство
*Доказательство.* формула $x=1$.

> поле:mn мораль

## Текст слайда — сжато
### [primer] пример раньше утверждения
Текст. формула $x=1$.

### [utverzhdenie] утверждение не первым
Текст. формула $x=1$.

### [dokazatelstvo] доказательство
Текст. формула $x=1$.

## Правки
- фикстура Э3
