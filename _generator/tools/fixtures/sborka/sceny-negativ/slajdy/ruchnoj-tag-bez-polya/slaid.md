<!--
ЧТО ДАЛЬШЕ С ЭТИМ ФАЙЛОМ (фикстура захода sceny-iz-blokov, Э2 — не порождена
bootstrap_lekcii.py, писана руками ради изоляции: раздел «Текст слайда» несёт
ручной тег {@2}, а поле `sceny_vruchnuyu` в шапке НЕ заполнено — гейт обязан
краснеть Э2-клаузой. Блока [dokazatelstvo] на карточке нет вовсе — изолирует Э2
от Э3; блоков всего два — изолирует от жёлтого Э4.
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
imya: ruchnoj-tag-bez-polya
nazvanie: ruchnoj-tag-bez-polya
zagolovok_na_ekrane: ""
tip_slaida: Т4
zachem: фикстура Э2 — ручной тег без поля-обоснования
akcent: фикстура
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
### [narrativ] первый пункт
Первый пункт нарратива.

### [narrativ] второй пункт
Второй пункт нарратива.

## Текст слайда — сжато
### [narrativ] первый пункт
Первый пункт нарратива, сжато.

### [narrativ] второй пункт
{@2} Второй пункт нарратива, сжато — тег ЕСТЬ, а поля sceny_vruchnuyu НЕТ.

## Правки
- фикстура Э2 sceny-iz-blokov
