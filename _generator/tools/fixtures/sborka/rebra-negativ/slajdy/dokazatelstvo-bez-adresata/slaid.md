<!--
ЧТО ДАЛЬШЕ С ЭТИМ ФАЙЛОМ (фикстура захода kod_rebra-blokov.md, Э2 — не порождена
bootstrap_lekcii.py, писана руками ради изоляции: блок [dokazatelstvo] есть, а
'dokazatelstvo_opiraetsya_na' пусто — гейт обязан краснеть Э2-клаузой «доказательство
без адресата». Изоляция та же, что у ловушки 42 (tipologia-e3-negativ)/43 (sceny-negativ).
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
imya: dokazatelstvo-bez-adresata
nazvanie: dokazatelstvo-bez-adresata
zagolovok_na_ekrane: ""
tip_slaida: Т3
zachem: фикстура Э2 — доказательство без адресата
akcent: фикстура
centralnyj_blok: утверждение
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
### [utverzhdenie] утверждение
**Утверждение (раз).** формула $x=1$.

> поле:mn мораль

### [dokazatelstvo] доказательство
*Доказательство.* подставим $x=1$.

## Текст слайда — сжато
### [utverzhdenie] утверждение
Текст утверждения. формула $x=1$.

### [dokazatelstvo] доказательство
Текст доказательства.

## Правки
- фикстура Э2 kod_rebra-blokov.md
