<!--
ЧТО ДАЛЬШЕ С ЭТИМ ФАЙЛОМ (фикстура захода sceny-iz-blokov, Э3 — не порождена
bootstrap_lekcii.py, писана руками ради изоляции: доказательство размечено НА
ТОЙ ЖЕ сцене, что и утверждение, которое оно доказывает — гейт обязан краснеть
Э3-клаузой. `sceny_vruchnuyu` заполнено НАРОЧНО, чтобы карточка НЕ красила Э2 —
изоляция та же, что у ловушки 42 (tipologia-e3-negativ) для трёх клауз Э3.
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
imya: dokazatelstvo-v-scene-predmeta
nazvanie: dokazatelstvo-v-scene-predmeta
zagolovok_na_ekrane: ""
tip_slaida: Т3
zachem: фикстура Э3 — доказательство в сцене предмета
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
sceny_vruchnuyu: фикстура нарочно держит ручной тег {@1} на доказательстве — изолирует Э3 от Э2
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
{@1} Текст доказательства — тег СОВПАДАЕТ со сценой утверждения нарочно.

## Правки
- фикстура Э3 sceny-iz-blokov
