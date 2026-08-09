#!/bin/sh
# TOOL-CONTRACT-COVERS: deck.py vmeshchenie.py bootstrap_lekcii.py
# Фикстуры ДВУХ ПРОВОДОК захода `tri-provodki`: солвер видит полосы (П1) и
# генератор порождает служебные слайды (П2). Гоняй после любой правки
# `deck.py`/`vmeshchenie.py`. Строка COVERS выше — не украшение: по ней хук решает,
# поднимать ли фикстуру (класс «триггер уже охвата», check_tool_contract.py).
#
# Запуск:  sh _generator/tools/fixtures/provodka/PROGNAT.sh
# Ожидание: ФИКСТУРЫ ЗЕЛЁНЫЕ, exit 0.
#
# ЗАЧЕМ. Оба механизма БЫЛИ ПОСТРОЕНЫ и не подключены, и оба провода рвались
# молча — то есть ровно так, как гейт не ловит, а глаз не замечает:
#
#   П1. Развилка `deck.py` читала непустую `liniya` как «автор сам решил ширину
#       полосы — не лезь». Но `liniya` ОБЯЗАТЕЛЬНА (`formaty.OBYAZATELNYE_POLYA`;
#       `tipy._require_liniya` роняет компиляцию без числа) ⇒ у любой полосы,
#       прошедшей гейт, условие истинно ВСЕГДА. Замер на живой Л2 до правки:
#       подобрано 0 полос из 9, при том что `kegl_px` в шапках не было вовсе.
#       ЦЕНА: 6 из 9 обрезанных слайдов — полосы; вместимость добиралась ручным
#       промером через браузер, около половины времени того захода.
#   П1-бис. `apply_to_card` дописывал `kegl_px` в шапку — и на следующей сборке
#       он читался как «явный». Подбор был ОДНОРАЗОВЫМ: любая правка текста молча
#       ехала на старом кегле. Поймало живого исполнителя.
#   П2. `tipy.oblozhka/vizitka/finalnyj` существуют, `_order` ставит обложку
#       первой — а шага, который их ПОРОДИТ, не было. Служебные слайды появлялись,
#       только если автор заводил папку слайда руками.
#
# ЛОВУШЕК ВОСЕМЬ. Первые пять — на решении о подборе (без браузера: судится
# ЧИСТАЯ функция `deck.reshenie_o_podbore`, ровно та, которую зовёт живой цикл),
# три последние — на порождении служебных (`deck.plan_sluzhebnyh`).
#   1. 🔴 ГЛАВНАЯ: полоса с заполненной `liniya` и без `kegl_px` ОБЯЗАНА
#      подбираться. Это буквально дефект П1 — ловушка красная до правки.
#   2. Намерение автора (`verstka_reshena: da`) солвер не трогает — в том числе
#      когда текст изменился. Сторожит ПРОТИВОПОЛОЖНУЮ ошибку: солвер, который
#      после починки трогает слишком много, хуже молчащего.
#   3. Метка солвера + тот же текст → пропуск (вход не менялся).
#   4. 🔴 Метка солвера + ИЗМЕНЁННЫЙ текст → переподбор. Это П1-бис.
#   5. Метка солвера, а значения в шапке ДРУГИЕ (правил человек) → не трогать.
#   6. Лекция без служебных слайдов → порождаются все три, обложка безусловна.
#   7. `bez_vizitki` снимает визитку, `bez_finalnogo` — финальный; обложку не
#      снимает ничто.
#   8. 🔴 Служебный слайд заведён РУКАМИ → генератор молчит. Проверка по ТИПУ, а
#      не по имени папки: обложка автора может называться как угодно.
cd "$(dirname "$0")/../../.." || exit 1
fail=0
ok() { echo "  ✅ $1"; }
no() { echo "  ❌ $1"; fail=1; }

echo "── П1: решение о подборе (deck.reshenie_o_podbore, без браузера)"
python3 - <<'PY' || fail=1
import sys
sys.path.insert(0, "sborka")
import deck, vmeshchenie

fail = 0
def je(opis, dano, zhdem):
    global fail
    if dano == zhdem:
        print("  ✅ %s" % opis)
    else:
        print("  ❌ %s: получено %r, ожидалось %r" % (opis, dano, zhdem)); fail = 1

TELO = "текст слайда, каким он был при подборе"
OTP = vmeshchenie.otpechatok(TELO)

# 1 — ГЛАВНАЯ: полоса, `liniya` заполнена (она обязательна), `kegl_px` нет.
nado, prichina = deck.reshenie_o_podbore(
    {"tip_verstki": "polosa_gorizontalnaya", "liniya": "66"}, OTP)
je("1. полоса с обязательной `liniya` и без kegl_px — ПОДБИРАЕТСЯ", nado, True)

# 1б — то же для вертикальной полосы и для не-полосы
for tip in ("polosa_vertikalnaya", "tolko_tekst"):
    n, _ = deck.reshenie_o_podbore({"tip_verstki": tip, "liniya": "100"}, OTP)
    je("1б. %s без kegl_px — подбирается" % tip, n, True)

# 2 — намерение автора: не трогать даже при изменившемся тексте
n, p = deck.reshenie_o_podbore(
    {"tip_verstki": "polosa_gorizontalnaya", "liniya": "66", "kegl_px": "44",
     "verstka_reshena": "da",
     "podbor_avto": vmeshchenie.sobrat_metku(OTP, {"kegl_px": 44.0})},
    vmeshchenie.otpechatok("СОВСЕМ другой текст"))
je("2. `verstka_reshena: da` — солвер не трогает", n, False)
je("2. …и причина названа намерением", "намерение" in p, True)

# 3 — метка солвера, текст не менялся → пропуск
metka = vmeshchenie.sobrat_metku(OTP, {"kegl_px": 38.0, "mezhstrochye": 1.2,
                                       "otstup_bloka": 8.7, "liniya": 66.0})
shapka = {"tip_verstki": "polosa_gorizontalnaya", "liniya": "66.0", "kegl_px": "38.0",
          "mezhstrochye": "1.2", "otstup_bloka": "8.7", "podbor_avto": metka}
n, _ = deck.reshenie_o_podbore(dict(shapka), OTP)
je("3. метка солвера + тот же текст — пропуск", n, False)

# 4 — метка солвера, ТЕКСТ ИЗМЕНИЛСЯ → переподбор (второй дефект П1)
n, p = deck.reshenie_o_podbore(dict(shapka), vmeshchenie.otpechatok(TELO + " и ещё абзац"))
je("4. метка солвера + изменённый текст — ПЕРЕПОДБОР", n, True)
je("4. …и причина названа текстом", "текст изменился" in p, True)

# 5 — метка есть, а значения в шапке другие: после солвера правил человек
chuzhaya = dict(shapka, kegl_px="42")
n, p = deck.reshenie_o_podbore(chuzhaya, OTP)
je("5. значения правили руками поверх метки — не трогать", n, False)
je("5. …и причина названа рукой человека", "руками" in p, True)

# 5б — легаси (значения без метки): по умолчанию не трогаем, с --zanovo подбираем
legasi = {"tip_verstki": "polosa_gorizontalnaya", "liniya": "66", "kegl_px": "40"}
n, p = deck.reshenie_o_podbore(dict(legasi), OTP)
je("5б. легаси без метки — по умолчанию не трогаем", n, False)
je("5б. …и сказано, чем размораживать", "--zanovo" in p, True)
n, _ = deck.reshenie_o_podbore(dict(legasi), OTP, zanovo=True)
je("5в. --zanovo размораживает легаси", n, True)
n, _ = deck.reshenie_o_podbore(dict(legasi, verstka_reshena="da"), OTP, zanovo=True)
je("5г. …но НЕ переигрывает намерение автора", n, False)

# метка, которую никто не писал / мусор — читается как «метки нет»
je("5д. мусор вместо метки не притворяется меткой",
   vmeshchenie.razobrat_metku("не метка вовсе|kegl_px=ой")[0], None)

sys.exit(fail)
PY
[ $? -eq 0 ] || no "П1: ловушки решения о подборе"

echo "── П2: порождение служебных слайдов (deck.plan_sluzhebnyh)"
python3 - <<'PY' || fail=1
import sys
sys.path.insert(0, "sborka")
import deck

fail = 0
def je(opis, dano, zhdem):
    global fail
    if dano == zhdem:
        print("  ✅ %s" % opis)
    else:
        print("  ❌ %s: получено %r, ожидалось %r" % (opis, dano, zhdem)); fail = 1

NA_DISKE = {"s01": "tolko_tekst", "s02": "polosa_gorizontalnaya", "s03": "razdelitel"}

# 6 — ничего служебного в лекции нет: порождаются все три
plan = deck.plan_sluzhebnyh({"title": "Функторы"}, NA_DISKE)
je("6. порождены все три служебных", [p[1]["tip_verstki"] for p in plan],
   ["oblozhka", "vizitka", "finalnyj"])
je("6. заголовок обложки взят из title", plan[0][1]["zagolovok_na_ekrane"], "Функторы")
je("6. разделитель НЕ порождается", any(p[1]["tip_verstki"] == "razdelitel" for p in plan), False)

# 6б — заголовок обложки не обязан совпадать с внутренним title
plan = deck.plan_sluzhebnyh({"title": "Функторы", "oblozhka_zagolovok": "Что запрещает функтор",
                             "oblozhka_illustracii": "pustoj-kvadrat"}, NA_DISKE)
je("6б. на экран идёт oblozhka_zagolovok, не title",
   plan[0][1]["zagolovok_na_ekrane"], "Что запрещает функтор")
je("6б. иллюстрация обложки доехала", plan[0][1]["illustracii"], ["pustoj-kvadrat"])

# 7 — флаги снимают визитку и финальный; обложку не снимает ничто
plan = deck.plan_sluzhebnyh({"title": "T", "bez_vizitki": "da", "bez_finalnogo": "true"}, NA_DISKE)
je("7. bez_vizitki/bez_finalnogo сняли оба", [p[1]["tip_verstki"] for p in plan], ["oblozhka"])
plan = deck.plan_sluzhebnyh({"title": "T", "bez_oblozhki": "da"}, NA_DISKE)
je("7б. обложка безусловна — выключателя у неё нет",
   plan[0][1]["tip_verstki"], "oblozhka")

# 8 — 🔴 автор завёл служебные слайды РУКАМИ: дубля нет, и решает ТИП, а не имя
svoi = dict(NA_DISKE, moya_oblozhka="oblozhka", spasibo="finalnyj")
plan = deck.plan_sluzhebnyh({"title": "T"}, svoi)
je("8. заведённые руками не дублируются (по ТИПУ, не по имени)",
   [p[1]["tip_verstki"] for p in plan], ["vizitka"])
plan = deck.plan_sluzhebnyh({"title": "T"}, dict(NA_DISKE, oblozhka="oblozhka",
                                                 vizitka="vizitka", finalnyj="finalnyj"))
je("8б. все три заведены руками — генератор молчит", plan, [])

sys.exit(fail)
PY
[ $? -eq 0 ] || no "П2: ловушки порождения служебных"

echo "── П2 живьём: сборка синтетической лекции (без браузера, --bez-podbora)"
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
python3 - "$T" <<'PY' || exit 1
import pathlib, sys
lek = pathlib.Path(sys.argv[1], "lekciya")
(lek / "slajdy" / "odin").mkdir(parents=True)
(lek / "illustracii").mkdir()
(lek / "brief.md").write_text("---\nid: proba\ncanvas: 1440x810\nslide_order:\n  - odin\n"
                              "title: Проба\n---\n", encoding="utf-8")
(lek / "slajdy" / "odin" / "slaid.md").write_text("""<!--
ЧТО ДАЛЬШЕ С ЭТИМ ФАЙЛОМ (вшито bootstrap_lekcii.py).
ФАЗА 1 (интервью): … :: команда
ФАЗА 2 (раскадровка): … :: команда
ФАЗА 3 (текст слайдов): … :: команда
ФАЗА 4 (вёрстка): … :: команда
ФАЗА 5 (иллюстрации): … :: команда
ФАЗА 6 (сборка и QA): … :: команда
-->
---
imya: odin
nazvanie: Один слайд
zagolovok_na_ekrane: Один слайд
tip_idei: perehod
zachem: единственный содержательный слайд пробы
akcent: —
centralnyj_blok: проба
minuty: 1
vazhnost: fon
byudzhet_slov: 10
tip_verstki: tolko_tekst
liniya: 100
---

## Математика — развёрнуто
### [narrativ] проба
Тело блока.

## Текст слайда — сжато
### [narrativ] проба
Тело блока.

## Правки
- 2026-08-09 · заведён фикстурой provodka
""", encoding="utf-8")
PY
python3 sborka/deck.py "$T/lekciya" -o "$T/dek.html" --bez-podbora >"$T/log" 2>&1
if [ $? -ne 0 ]; then no "живая сборка синтетической лекции упала"; cat "$T/log"; fi
N=$(grep -c 'class="slide"' "$T/dek.html" 2>/dev/null)
[ "$N" = "4" ] && ok "живьём: 1 авторский слайд + 3 служебных = 4" \
                || no "живьём: слайдов в деке $N, ожидалось 4"
# 🔴 грепать ВЕСЬ файл, не первые килобайты: в голове дека сидят шрифты и katex.css,
# и любое «посмотрим начало» упирается в них, а не в слайды (поймано первым прогоном).
grep -q 'id="oblozhka"' "$T/dek.html" \
  && ok "живьём: обложка в деке есть" || no "живьём: обложки в деке НЕТ"
FIRST=$(grep -o 'section class="slide" id="[^"]*"' "$T/dek.html" | head -1)
echo "$FIRST" | grep -q 'id="oblozhka"' && ok "живьём: обложка ПЕРВАЯ" \
                                        || no "живьём: первым идёт $FIRST"
LAST=$(grep -o 'section class="slide" id="[^"]*"' "$T/dek.html" | tail -1)
echo "$LAST" | grep -q 'id="finalnyj"' && ok "живьём: финальный ПОСЛЕДНИЙ" \
                                       || no "живьём: последним идёт $LAST"

[ $fail -eq 0 ] && echo "ФИКСТУРЫ ЗЕЛЁНЫЕ" || echo "ФИКСТУРЫ КРАСНЫЕ"
exit $fail
