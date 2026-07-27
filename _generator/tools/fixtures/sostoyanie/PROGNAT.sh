#!/bin/sh
# Фикстуры трекера sostoyanie.py — гоняй ПОСЛЕ любой его правки.
#
# Запуск:  sh _generator/tools/fixtures/sostoyanie/PROGNAT.sh
# Ожидание: ФИКСТУРЫ ЗЕЛЁНЫЕ, exit 0.
#
# ЗАЧЕМ. Закон фабрики: у гейта, который может ПРОЙТИ, обязана быть фикстура, на
# которой он ПАДАЕТ, — иначе зелёный ничего не доказывает (KONSTITUCIYA §11).
# G7 был переписан под ленту, G12–G15 заведены с нуля 27.07.2026; до этих папок
# каждая из шести проверок могла молча выродиться в «всегда PASS».
#
# ВТОРАЯ ПОЛОВИНА, не менее важная: папки `g7-zelenyj`, `g7-staraya-shema` и
# `zdorovyj` — это фикстуры на ЛОЖНОЕ СРАБАТЫВАНИЕ. Трекер судит коммиты троих
# писателей; гейт, краснеющий на здоровом деке, обходят через --no-verify, и
# тогда пропадает вся защита, а не одна проверка. Поэтому здесь проверяется не
# только «краснеет, где должен», но и «зеленеет, где должен».
#
# Гейты вне проверяемого в каждой папке — красные, и это норма: фикстура несёт
# ровно тот минимум файлов, который нужен её проверке, а не полную лекцию.
# Поэтому судим статус КОНКРЕТНОЙ строки отчёта, а не exit-код скрипта.
#
# ⚠ mtime. Случай `g7-view-ustarel` держится на том, что `*.md` свежее
#   `view.html`, а git времена файлов не хранит — после клона они совпадают.
#   Порядок здесь выставляется явным `touch` перед прогоном; без него фикстура
#   печатала бы ложный зелёный на чужой машине.

cd "$(dirname "$0")/../../../.." || exit 1
FIX=_generator/tools/fixtures/sostoyanie
fail=0

# view.html намеренно старше ленты (лента правилась, build_doc.py не гоняли)
touch "$FIX/g7-view-ustarel/raskadrovka/teksty/view.html"
sleep 1
touch "$FIX/g7-view-ustarel/raskadrovka/teksty/blok-1.md"
# а здесь наоборот — вид пересобран последним
touch "$FIX/g7-zelenyj/raskadrovka/teksty/blok-1.md"
touch "$FIX/zdorovyj-neobychnyj/raskadrovka/teksty/blok-1.md"
sleep 1
touch "$FIX/g7-zelenyj/raskadrovka/teksty/view.html"
touch "$FIX/zdorovyj-neobychnyj/raskadrovka/teksty/view.html"

expect() {  # expect <папка> <гейт> <ожидаемый статус> <зачем>
    line=$(python3 _generator/tools/sostoyanie.py "$FIX/$1" 2>&1 | grep -E "^$2[[:space:]]")
    if [ -z "$line" ]; then
        echo "  ❌ $1 · $2: строки гейта в отчёте НЕТ — проверка не зарегистрирована"
        fail=1
        return
    fi
    if printf '%s\n' "$line" | grep -qE "[[:space:]]$3([[:space:]]|$)"; then
        echo "  ✅ $1 · $2 = $3 — $4"
    else
        echo "  ❌ $1 · $2: ожидался $3, отчёт говорит:"
        echo "     $line"
        fail=1
    fi
}

echo "── краснеет там, где долг ──"
expect g7-pokrytie     G7  FAIL "разделов ленты меньше, чем slide_order"
expect g7-raskladka    G7  FAIL "раздел без «поле:mn **Раскладка.**»"
expect g7-view-ustarel G7  FAIL "view.html не пересобран после правки ленты"
expect g7-lenta-pusta  G7  FAIL "teksty/ заведена, но ни одного *.md с tab:"
expect g12-oblozhka    G12 FAIL "обложка на 32 слова и с двумя иллюстрациями"
expect g13-scena       G13 FAIL "илл. привязана к сцене 5, которой у слайда нет"
expect g14-sceny       G14 FAIL "текст требует сцену 5, слайд объявил три"
expect g14-diapazon    G14 FAIL "диапазон {@-8} при трёх сценах — верхняя граница не проспана"
expect g15-kaskad      G15 FAIL "каскад блюра оборван на .scene-3 при {blur@4} (урок 8)"
expect g12-tekst-v-karkase G12 FAIL "текст обложки в каркасе слайда, а content/ пуст"
expect g12-porozhdenie  G12 FAIL "дек на порождении, а рядом рукописный sl-title — он перебивает канон"
expect g12-rasshirenie  G12 FAIL "рукописная обложка под расширением .html~ перебивает порождение так же, как .html"
expect g12-peregruz-polej G12 FAIL "обложка перегружена через санкционированные поля brief.md — счёт слов перенацелен на них"

echo "── зеленеет там, где долга нет (защита от --no-verify) ──"
expect g7-zelenyj      G7  PASS "лента покрывает деку, вид свежий, раскладка везде"
expect g7-staraya-shema G7 N/A  "папки teksty/ нет — шаг 6 по старой схеме, не FAIL"
expect zdorovyj        G12 PASS "обложка и финал в норме"
expect zdorovyj-porozhdenie G12 PASS "дек на порождении без рукописных служебных — счётом слов не судится"
expect zdorovyj        G13 PASS "илл. на своей сцене"
expect zdorovyj        G14 PASS "data-scenes сходится с разметкой"
expect zdorovyj        G15 PASS "оба каскада покрывают свои сцены"

# Дек, устроенный НЕ как четыре имеющихся. Каждая строка ниже — закрытый класс
# ложного красного, найденный верификатором 28.07: `## ` внутри кодового забора
# ленты · многострочная врезка `> поле:mn` в бюджете слов · `**Раскладка:**` вместо
# `**Раскладка.**` · `}` внутри TeX внутри {blur@…} · слайд БЕЗ `data-scenes`
# (целевое состояние H6) · `data-scene-until` за пределом каскада (его прячет JS).
expect zdorovyj-neobychnyj G7  PASS "лента с забором, многострочной врезкой и формулой"
expect zdorovyj-neobychnyj G13 PASS "нет data-scenes — верхней границы не существует"
expect zdorovyj-neobychnyj G14 PASS "нет data-scenes — сверять не с чем, не FAIL"
expect zdorovyj-neobychnyj G15 PASS "data-scene-until каскада не требует"

echo "── хук H6 ──"
expect zdorovyj        H6  WARN "data-scenes выписан руками — так и должно быть до генерации"

[ $fail = 0 ] && echo "ФИКСТУРЫ ЗЕЛЁНЫЕ" || echo "ФИКСТУРЫ КРАСНЫЕ — трекер сломан правкой"
exit $fail
