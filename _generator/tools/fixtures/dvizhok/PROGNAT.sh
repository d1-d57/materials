#!/bin/sh
# TOOL-CONTRACT-COVERS: engine.js base.css build_deck.py render.py bootstrap_zahod.py
# ↑ ОХВАТ, а не список авторства. Пять файлов — один механизм: сцена, её каскад,
# кадр этой сцены и генератор, печатающий стартовую команду.
#
# ⚠ ЗАЗОР ЗАКРЫТ (дата данных 2026-07-30, долг 1 захода kod_melkie-dolgi). Хук
# поднимал эту фикстуру только на `bootstrap_zahod.py` — четыре других имени были
# объявлены ВЕРНО и не срабатывали никогда: `.githooks/pre-commit:62-63` отбирал
# staged-пути шаблоном ДО вызова `--fixtures-for`, и `skeleton/engine.js`,
# `skeleton/base.css`, `build_deck.py`, `render.py` не подходили ни под один.
# Починено: хук спрашивает `--fixtures-for` по ВСЕМ staged-путям, шаблон остался
# только для запуска AST-гейта над python-инструментами. Ловушка 5 ниже держит
# именно ЭТОТ маршрут (путь под охватом, но вне старых шаблонов).
#
# Запуск:  sh _generator/tools/fixtures/dvizhok/PROGNAT.sh
# Ожидание: ФИКСТУРЫ ЗЕЛЁНЫЕ, exit 0.
#
# ЗАЧЕМ. Через движок проходит КАЖДЫЙ слайд каждого дека, и характерный дефект
# класса — правка, которая выглядит эквивалентной и меняет поведение на краю.
# Обе поломки, которые здесь сторожатся, прожили месяц при зелёных линтере,
# check_view и audit --scene-diff: гейты смотрели не туда.
#
# ПЯТЬ ЛОВУШЕК, каждая оплаченная:
#   1. КАДР НЕРАСКРЫТОГО СЛАЙДА. `render.py` снимал `?only=N&scene=99` с
#      комментарием «показать в финальной сцене». Сцены раскрываются КЛАССОМ
#      `.scene-K`, каскад шёл до `.scene-5`, правила `.scene-99` нет ни в одном
#      деке ⇒ на PNG всё пошаговое содержимое было невидимым, и зрительная петля
#      месяц смотрела на пустые слайды. Диагноз поставили в чужом проекте и там же
#      залатали (`.scene-99` в overlay) — фабрика не всосала ни диагноза, ни заплаты.
#   2. КАСКАД ДО ПЯТОЙ. Пары «сцена × шаг» были выписаны в `base.css` РУКАМИ до
#      `.scene-5`. Цена оплачена в арке Паскаля: «на шестой оставалась первая сцена».
#   2б. ШАГ 1 НЕ РАСКРЫВАЛСЯ ВОВСЕ. Рукописный каскад начинался с `[data-scene-from="2"]`,
#      а генератор на тег `{@1}` пишет `data-scene-from="1"`, и базовое правило
#      прячет ВСЁ с этим атрибутом. Цена: 49 абзацев ленты Л1 не показывались ни в
#      одной сцене — при зелёных гейтах.
#   3. ЗАХОД НЕ В ТОЙ ПАПКЕ. `--worktree` отправлял исполнителя в рабочую папку, а
#      файл писал в основную: единственный законный способ вести два захода разом
#      был сломан на старте.
#   4. СТАРТОВАЯ КОМАНДА. Заход запускается ею дословно; ошибка здесь стоит целого
#      прогона. Плюс требование `KONSTITUCIYA §10`: время и токены обязана печатать
#      КОМАНДА, а не рука исполнителя (в корпусе 17 записей «даны оценкой»).
#   5. ХУК ГОНИТ ФИКСТУРУ ПО ОХВАТУ, А НЕ ПО ШАБЛОНУ ПУТИ. Эта фикстура честно
#      объявляла охват над `engine.js`/`base.css`/`build_deck.py`/`render.py`, а хук
#      отбирал staged-пути шаблоном каталогов ДО вызова `--fixtures-for` — три из
#      пяти покрытых имён никогда не попадали на проверку. Ловушка гоняет РЕАЛЬНЫЙ
#      `.githooks/pre-commit` в одноразовом репо: путь под охватом, но вне старых
#      шаблонов, останавливает коммит, когда фикстура красная, и не мешает, когда
#      зелёная; путь без охвата коммитится молча.
#
# 🔴 СУДИМ РЕЗУЛЬТАТ, НЕ ПОДСТРОКУ. Ловушки 1-2 гоняют НАСТОЯЩИЙ браузер и
# спрашивают вычисленную видимость элемента (`getComputedStyle`), а не наличие
# текста в HTML: нераскрытый шаг физически присутствует в разметке — грепом он
# неотличим от раскрытого, и ровно поэтому дефект жил месяц. Ловушка 4 не ищет
# `stream-json` в строке, а СКАРМЛИВАЕТ фильтру настоящую `result`-строку и
# проверяет, что напечаталась стоимость.

set -e
TOOLS=$(cd "$(dirname "$0")/../.." && pwd)
GEN=$(cd "$TOOLS/.." && pwd)
REPO=$(cd "$GEN/.." && pwd)

# 🔴 ОБЯЗАТЕЛЬНО ПЕРВЫМ ХОДОМ: вычистить окружение git. Внутри хука git экспортирует
# GIT_DIR/GIT_INDEX_FILE и прочие GIT_* АБСОЛЮТНЫМИ путями на БОЕВОЙ репозиторий —
# без этой строки `git init` создаёт папку в /tmp, а add/commit идут в боевой индекс.
# ЦЕНА (21.07, поймано на владельце): фикстура, запущенная хуком, СОЗДАЛА КОММИТ В
# БОЕВОМ РЕПОЗИТОРИИ и уронила коммит владельца ложным красным. Список даёт сам git,
# поэтому он не разъедется с версией.
unset $(git rev-parse --local-env-vars)

T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
FAIL=0
BROWSER_OK=0

# ── ЛОВУШКИ 1 и 2: движок и каскад в НАСТОЯЩЕМ браузере ───────────────────────
# Страница собирается из ЖИВЫХ артефактов: `skeleton/engine.js` дословно и
# `skeleton/base.css` с реально порождённым каскадом (зовём `scene_cascade_css`,
# а не переписываем её здесь — иначе фикстура сторожила бы свою копию логики).
python3 - "$GEN" "$T" <<'PY'
import sys, pathlib, importlib.util
gen, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("bd", gen / "build_deck.py")
bd = importlib.util.module_from_spec(spec); spec.loader.exec_module(bd)

engine = (gen / "skeleton" / "engine.js").read_text(encoding="utf-8")
base = (gen / "skeleton" / "base.css").read_text(encoding="utf-8")
# Слайд 0 — три сцены, слайд 1 — СЕМЬ: седьмая и есть проверка «каскад дошёл
# дальше пятой». Максимум берём из самой разметки той же дверью, что и сборка.
# Слайд 2 — атрибуты в ОДИНАРНЫХ кавычках, слайд 3 — отрицательное `data-scenes`.
# Обе формы найдены верификатором и обе давали ПУСТОЙ слайд при rc=0 линтера.
razmetka = """
<section class="slide" id="s0" data-scenes="3">
  <div class="zone">
    <p id="a1" data-scene-from="1">шаг один</p>
    <p id="a2" data-scene-from="2">шаг два</p>
    <p id="a3" data-scene-from="3">шаг три</p>
  </div>
</section>
<section class="slide" id="s1" data-scenes="7">
  <div class="zone">
    <p id="b1" data-scene-from="1">шаг 1</p>
    <p id="b6" data-scene-from="6">шаг 6</p>
    <p id="b7" data-scene-from="7">шаг 7</p>
  </div>
</section>
<section class='slide' id='s2' data-scenes='9'>
  <div class='zone'>
    <p id='c1' data-scene-from='1'>одинарные, шаг 1</p>
    <p id='c9' data-scene-from='9'>одинарные, шаг 9</p>
  </div>
</section>
<section class="slide" id="s3" data-scenes="-3">
  <div class="zone">
    <p id="d1" data-scene-from="1">шаг 1 при отрицательном data-scenes</p>
  </div>
</section>
<section class="slide" data-skip id="s-skip">
  <div class="zone"><p>черновик, движок его НЕ показывает</p></div>
</section>
<section class="slide" id="s4" data-scenes="2">
  <div class="zone">
    <p id="e2" data-scene-from="2">после пропущенного слайда</p>
  </div>
</section>
"""
base = base.replace("{{SCENE_CASCADE}}", bd.scene_cascade_css(bd.max_scenes(razmetka)))
if "{{" in base:
    print("ОСТАЛСЯ ПЛЕЙСХОЛДЕР В base.css", file=sys.stderr); raise SystemExit(2)
(out / "deck.html").write_text(
    "<!DOCTYPE html>\n<html lang=\"ru\"><head><meta charset=\"utf-8\">\n<style>\n"
    + base + "\n</style></head><body>\n<div id=\"stage\"><div id=\"deck\">\n"
    + razmetka + "\n</div></div>\n<div id=\"hint\"></div>\n<script>\n"
    + engine + "\n</script></body></html>\n", encoding="utf-8")
PY

# 🔴 Проверяем НЕ импорт пакета, а РЕАЛЬНЫЙ запуск браузера: `pip install
# playwright` кладёт python-пакет, а `chrome-headless-shell` тянется отдельной
# командой (`playwright install`) — импорт молча проходит и без него, а запуск
# падает. Проверка импортом маскировала ИМЕННО этот разрыв (класс B, RAZBOR
# §2: 4 обхода `--no-verify` подряд — фикстура краснела на отсутствующем
# браузере неотличимо от настоящей регрессии).
if python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    p.chromium.launch().close()
" > /dev/null 2>&1; then
    BROWSER_OK=1
else
    echo "  ⚠ пропущено: нет playwright (поставить: playwright install). Ядро"
    echo "    захода (движок и каскад) осталось без гейта в ЭТОМ прогоне."
    echo "    Красным это не делаю сознательно: гейт, валящий коммит из-за"
    echo "    отсутствующей у соседа dev-зависимости, отключают целиком (Р31),"
    echo "    и тогда пропадают и ловушки 3-4. Зазор назван, а не проглочен."
fi

if [ "$BROWSER_OK" = "1" ]; then
if python3 - "$T" "$GEN" > "$T/browser.txt" 2>&1 <<'PY'
import sys, pathlib, importlib.util
from playwright.sync_api import sync_playwright
T, GEN = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
url = "file://" + str(T / "deck.html")
fails = []


def check(name, ok, chto=""):
    print(("  OK  " if ok else "  BAD ") + name + ("" if ok else "  <- " + str(chto)))
    if not ok:
        fails.append(name)


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 810})

    def sostoyanie(qs, sel):
        pg.goto(url + qs)
        pg.wait_for_timeout(320)
        return pg.evaluate(
            """(sel) => {
                 const s = document.querySelector(sel).closest(".slide");
                 const st = getComputedStyle(document.querySelector(sel));
                 return { klassy: Array.from(s.classList),
                          vidim: st.visibility === "visible" && +st.opacity > 0.9 };
               }""", sel)

    # ── ЛОВУШКА 1: ?scene=99 на слайде с 3 сценами показывает ТРЕТЬЮ ──
    r = sostoyanie("?only=0&scene=99", "#a3")
    check("scene=99 на 3-сценовом даёт класс scene-3", "scene-3" in r["klassy"], r["klassy"])
    check("scene=99: класса scene-99 НЕТ", "scene-99" not in r["klassy"], r["klassy"])
    check("scene=99: третий шаг ВИДЕН (а не пустой кадр)", r["vidim"], r)

    # ── ЛОВУШКА 1б: кадр БЕЗ параметра scene — так теперь просит render.py ──
    r = sostoyanie("?only=0", "#a3")
    check("?only=0 без scene: финальная сцена (scene-3)", "scene-3" in r["klassy"], r["klassy"])
    check("?only=0 без scene: третий шаг ВИДЕН", r["vidim"], r)

    # ── ЛОВУШКА 2: слайд с 7 сценами раскрывает СЕДЬМОЙ шаг ──
    r = sostoyanie("?only=1", "#b7")
    check("7 сцен: класс scene-7", "scene-7" in r["klassy"], r["klassy"])
    check("7 сцен: СЕДЬМОЙ шаг виден (каскад дошёл дальше пятой)", r["vidim"], r)
    r = sostoyanie("?only=1&scene=6", "#b6")
    check("сцена 6: шестой шаг виден", r["vidim"], r)
    r = sostoyanie("?only=1&scene=6", "#b7")
    check("сцена 6: седьмой шаг ЕЩЁ скрыт (каскад не раскрывает лишнего)",
          not r["vidim"], r)

    # ── ЛОВУШКА 2б: шаг 1 виден на ПЕРВОЙ сцене ──
    r = sostoyanie("?only=1&scene=1", "#b1")
    check("сцена 1: шаг с data-scene-from=1 ВИДЕН (49 абзацев Л1)", r["vidim"], r)

    # ── ЛОВУШКА 2в: атрибуты в ОДИНАРНЫХ кавычках не схлопывают каскад ──
    # Порождение не имеет права быть хрупче того, что оно заменило: рукописный
    # список от разбора разметки не зависел вовсе.
    # ⚠ Слайд s2 несёт 9 сцен — БОЛЬШЕ, чем любой слайд с двойными кавычками (7).
    # Это не украшение фикстуры: при 6 сценах максимум всё равно давал слайд s1, и
    # проверка оставалась ЗЕЛЁНОЙ на строгом регекспе (поймано мутацией). Схлопывание
    # видно только тогда, когда максимум ОПРЕДЕЛЯЕТ сам одинарно-кавычный слайд.
    r = sostoyanie("?only=2", "#c9")
    check("одинарные кавычки: шаг 9 виден (каскад не схлопнулся до чужого максимума)",
          r["vidim"] and "scene-9" in r["klassy"], r)
    r = sostoyanie("?only=2&scene=8", "#c1")
    check("одинарные кавычки: сцена 8 существует и раскрывает шаг 1", r["vidim"], r)

    # ── ЛОВУШКА 2г: отрицательное data-scenes не рождает класс `scene--3` ──
    # `parseInt("-3")` — число, и `|| 1` его не отсекает.
    # ⚠ Спрашиваем сцену ЯВНО (`&scene=1`), а не `?only=3`. Без scene экспорт сам
    # передаёт k = scenesOf = −3, оно падает в ветку «иначе 1» и дефект МАСКИРУЕТСЯ —
    # проверка была зелёной на мутации (поймано). Дефект рождается на НОРМАЛЬНОМ k
    # при отрицательном n: `1 > −3` истинно, и k становится −3.
    r = sostoyanie("?only=3&scene=1", "#d1")
    check("data-scenes=-3 при scene=1: класс scene-1, а не scene--3",
          "scene-1" in r["klassy"], r["klassy"])
    check("data-scenes=-3 при scene=1: шаг 1 ВИДЕН (слайд не пустой)", r["vidim"], r)
    r = pg.evaluate("""() => Array.from(document.getElementById("s3").classList)
                            .filter(c => c.indexOf("scene--") === 0)""")
    check("data-scenes=-3: класса вида scene--N нет вовсе", r == [], r)

    # ── край: 0, отрицательное, мусор ──
    for qs, ozhid in [("?only=0&scene=0", "scene-1"), ("?only=0&scene=-1", "scene-1"),
                      ("?only=0&scene=abc", "scene-1")]:
        r = sostoyanie(qs, "#a1")
        check("край " + qs + " -> " + ozhid, ozhid in r["klassy"], r["klassy"])

    # ── hash-роутинг #sN.K зажимается тем же местом ──
    pg.goto(url + "#s0.99")
    pg.wait_for_timeout(320)
    r = pg.evaluate("""() => ({
          klassy: Array.from(document.getElementById("s0").classList),
          hash: location.hash })""")
    check("#s0.99 -> scene-3", "scene-3" in r["klassy"], r["klassy"])
    check("#s0.99: адрес не врёт про показанную сцену", r["hash"] == "#s0.3", r["hash"])

    # ── залипший класс: applyScene снимает ФАКТИЧЕСКИЕ, а не 1..9 ──
    pg.goto(url + "?only=0")
    pg.wait_for_timeout(220)
    r = pg.evaluate("""() => {
          const s = document.getElementById("s0");
          s.classList.add("scene-42");
          applyScene(s, 2);
          return Array.from(s.classList).filter(c => /^scene-\\d+$/.test(c));
        }""")
    check("залипший scene-42 снят (не только диапазон 1..9)", r == ["scene-2"], r)
    b.close()

# ── render.py: какой URL он ПРОСИТ. Судим результат, а не текст файла ──
spec = importlib.util.spec_from_file_location("rnd", GEN / "render.py")
rnd = importlib.util.module_from_spec(spec); spec.loader.exec_module(rnd)


class Stub:
    def __init__(self):
        self.urls = []

    def goto(self, u):
        self.urls.append(u)

    def wait_for_timeout(self, *a):
        pass

    def screenshot(self, **k):
        pass


st = Stub()
rnd._shot(st, "file:///deck.html", 4, T / "x.png", wait=0)
check("render.py НЕ просит scene=99", "scene=99" not in st.urls[0], st.urls)
check("render.py просит только ?only=N", st.urls == ["file:///deck.html?only=4"], st.urls)

# ── ЛОВУШКА 1в: render.py считает слайды ТЕМ ЖЕ селектором, что движок ──
# У дека с `data-skip` (в репо это dandelin) документ несёт на слайд БОЛЬШЕ, чем
# массив движка. Промах двойной и оба раза тихий: последний кадр снимается с
# несуществующего индекса (пустой PNG), а каждый индекс после пропущенного слайда
# показывает СОСЕДА — файл NN.png называет не тот слайд, который на нём. Найдено
# верификатором. Судим РЕЗУЛЬТАТ: сравниваем счёт render.py с длиной slides движка.
class RealPage:
    """Настоящая страница нужна потому, что оба счёта живут в браузере."""

    def __init__(self, pg):
        self.pg = pg

    def goto(self, u):
        self.pg.goto(u)

    def wait_for_timeout(self, ms):
        self.pg.wait_for_timeout(ms)

    def evaluate(self, js):
        return self.pg.evaluate(js)


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 810})
    schet = rnd._count_slides(RealPage(pg), url)
    dvizhok = pg.evaluate("() => slides.length")
    vsego = pg.evaluate("() => document.querySelectorAll('.slide').length")
    check("render.py считает столько же слайдов, сколько движок",
          schet == dvizhok, {"render.py": schet, "движок": dvizhok, ".slide": vsego})
    check("в стенде ЕСТЬ слайд с data-skip (иначе ловушка проверяет пустоту)",
          vsego == dvizhok + 1, {".slide": vsego, "движок": dvizhok})
    # последний индекс, который снимет render.py, обязан быть НЕПУСТЫМ кадром
    pg.goto(url + "?only=" + str(schet - 1))
    pg.wait_for_timeout(320)
    # ⚠ ВЫЧИСЛЕННЫЙ стиль, а не `style.display`. Инлайновый display движок ставит
    # только слайдам ИЗ массива, а `[data-skip]` в массив не входит — по инлайну он
    # выглядит видимым, даже когда его прячет CSS. На этом проверка краснела на
    # здоровом коде (поймано прогоном).
    posl = pg.evaluate("""() => {
        const v = Array.from(document.querySelectorAll(".slide"))
                       .filter(s => getComputedStyle(s).display !== "none");
        return { vidno: v.length, id: v.length ? v[0].id : null };
    }""")
    check("последний кадр render.py показывает РЕАЛЬНЫЙ слайд, а не пустоту",
          posl["vidno"] == 1 and posl["id"] is not None, posl)
    # И черновой слайд не попадает в кадр вместе с текущим
    check("слайд с data-skip скрыт КАНОНОМ (не лезет в кадр рядом с текущим)",
          posl["id"] != "s-skip", posl)
    b.close()

print("ОШИБОК:", len(fails))
sys.exit(1 if fails else 0)
PY
then
    grep -e "  OK  " -e "  BAD " "$T/browser.txt" | sed "s/^  OK  /  ✅ /; s/^  BAD /  ❌ /"
    echo "  ✅ ловушки 1-2 (движок, каскад, кадр) — зелёные на живом браузере"
else
    grep -e "  OK  " -e "  BAD " "$T/browser.txt" | sed "s/^  OK  /  ✅ /; s/^  BAD /  ❌ /" || true
    echo "  ❌ ЛОВУШКИ 1-2 КРАСНЫЕ — движок/каскад/кадр сломаны (подробности выше)"
    sed -n '/Traceback/,$p' "$T/browser.txt" | head -20
    FAIL=1
fi
fi

# ── ЛОВУШКА 3: --worktree держит файл-заход В ОСНОВНОЙ ПАПКЕ, не в рабочей ────
# Действующее правило — `GIT-disciplina §4` (дата данных 2026-08-03): файл-заход
# живёт В ОДНОМ ЭКЗЕМПЛЯРЕ в основной папке репозитория; `--worktree` заводит
# рабочую папку ТОЛЬКО ДЛЯ КОДА, а стартовая команда ведёт туда `cd` (там код,
# не заход). Прежняя версия этой ловушки требовала ПРОТИВОПОЛОЖНОГО («заход
# лёг в рабочую папку») — то самое отменённое правило; гейт красил ПРАВИЛЬНОЕ
# поведение и будет краснеть всегда, пока не перевёрнут. Гоняется на
# ОДНОРАЗОВОМ репо в /tmp: `worktree add` пишет в .git, и делать это в боевом
# репозитории гейт не смеет (урок 1.7).
podgotovit() {
    R="$1"
    mkdir -p "$R/_studio/docs" "$R/_studio/zhurnal/arka" "$R/_generator/tools"
    # 🔴 Реестр корней кладём В КАЖДЫЙ поддельный репозиторий: инструменты берут
    # корни только из него и без него не импортируются вовсе. Забыть его здесь —
    # значит получить не «фикстура покраснела», а «фикстура упала на импорте»,
    # то есть шум вместо сигнала.
    cp "$TOOLS/korni.py" "$R/_generator/tools/korni.py"
    # 🔴 ДЕКЛАРАЦИЯ КАНОНИЧЕСКОГО КОРНЯ (заход `kanon-put`, 14.08): без неё
    # `bootstrap_zahod.py` ОТКАЗЫВАЕТСЯ собирать заход — путь в секции-носителе
    # больше не берётся от места запуска. Поддельный репозиторий объявляет
    # каноническим СЕБЯ: он существует, значит подмены путей не будет вовсе.
    printf '# синтетика фикстуры\n%s\n' "$R" > "$R/_generator/tools/KANON-KOREN"
    # 🔴 Секции-заготовки И строка ЗОНЫ — ОБЯЗАТЕЛЬНЫ дословно (`check_zahod.py`
    # З3/З7, часть `STRUCTURAL_CHECKS`, которой гейтит сам `bootstrap_zahod.py`
    # ДО записи файла на диск): без них генератор отказывает на КАЖДОМ вызове
    # этой фикстуры независимо от --kanal и backticks — ловушка 3 никогда не
    # доходила до своих проверок (живой прогон 2026-08-04 это поймал: старая
    # строка `ЗОНА: {{ЗОНА}}` не матчилась регэкспом З3, который требует
    # `**ЗОНА (можно менять):**`). ВОПРОСЫ/УРОКИ — ДОСЛОВНО якоря генератора
    # (`ЯКОРЬ_ВОПРОСЫ`/`ЯКОРЬ_UROKI`), иначе анкорная замена их не найдёт.
    printf '%s\n' '{{ТЕМА}} {{МОДЕЛЬ}} {{ВЕТКА}}' \
        '- **ЗОНА (можно менять):** {{ЗОНА}}.' \
        '{{КОНТРАКТ_МЕСТО}}' '{{ПЕРВЫЙ_ХОД}}' \
        '## ПЛАН — (заполняет исполнитель)' \
        '## ВОПРОСЫ — (заполняет исполнитель)' \
        '## ОТЧЁТ — (заполняет исполнитель)' \
        'отчёт: **время прогона + токены** / КОММИТ' \
        '## УРОКИ ФАБРИКЕ — (заполняет исполнитель; пусто — нормальный исход)' \
        > "$R/_studio/zhurnal/_TEMPLATE-zahod.md"
    printf '%s\n' '## §6. Индекс' '' '- `_studio/zhurnal/` — журнал' '' '## §7. Дальше' \
        > "$R/_studio/docs/KARTA.md"
    git init -q "$R"
    git -C "$R" config user.email fixture@test
    git -C "$R" config user.name fixture
    git -C "$R" add -A > /dev/null 2>&1
    git -C "$R" commit -qm "база фикстуры"
    git -C "$R" branch -M osnova
}

# Скрипт-обёртка: подменяет корень генератора на одноразовый репо и зовёт main().
# Именно боевой код, а не его копия, — иначе фикстура проверяет саму себя.
cat > "$T/zvat.py" <<'PY'
import importlib.util, pathlib, sys
gen, root, argv = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3:] + ["--intervyu", "da"]
spec = importlib.util.spec_from_file_location("bz", gen / "tools" / "bootstrap_zahod.py")
bz = importlib.util.module_from_spec(spec); spec.loader.exec_module(bz)
bz.REPO_ROOT = root
bz.TEMPLATE = root / "_studio" / "zhurnal" / "_TEMPLATE-zahod.md"
bz.GIT_ZONA = root / "_generator" / "tools" / "git_zona.py"
bz.register_doc.REPO = root
sys.exit(bz.main(argv))
PY
cp "$TOOLS/git_zona.py" "$T/gz-src.py"

R1="$T/repo-plain"
podgotovit "$R1"
# --kanal terminal: обычный режим, рабочая папка не проверяется — разницы для
# ловушки нет, выбор канала на исход не влияет.
GIT_ZONA_REPO="$R1" python3 "$T/zvat.py" "$GEN" "$R1" \
    _studio/zhurnal/arka bez-wt --branch osnova --zone "_generator/" \
    --finalizirovano "ф1" --finalizirovano "ф2" \
    --kanal terminal --opisanie "проба обычного режима" > "$T/plain.txt" 2>&1 || true

[ -f "$R1/_studio/zhurnal/arka/kod_bez-wt.md" ] \
    && echo "  ✅ БЕЗ --worktree заход лёг в основное дерево (режим не сломан)" \
    || { echo "  ❌ ОБЫЧНЫЙ РЕЖИМ СЛОМАН — захода нет в основном дереве"; FAIL=1; }

V=$(grep -c 'kod_bez-wt.md' "$R1/_studio/docs/KARTA.md" || true)
[ "$V" = "1" ] && echo "  ✅ БЕЗ --worktree регистрация ушла в KARTA.md основного дерева" \
              || { echo "  ❌ регистрация не дошла до KARTA.md основного дерева"; FAIL=1; }

R2="$T/repo-wt"
podgotovit "$R2"
cp "$T/gz-src.py" "$R2/_generator/tools/git_zona.py"
# --kanal app: здесь проверяется РАБОЧАЯ ПАПКА (--worktree) — канал app.
GIT_ZONA_REPO="$R2" python3 "$T/zvat.py" "$GEN" "$R2" \
    _studio/zhurnal/arka s-wt --branch zahod/proba --zone "_generator/" \
    --finalizirovano "ф1" --finalizirovano "ф2" \
    --worktree probnaya --kanal app > "$T/wt.txt" 2>&1 || true
WT="$T/repo-wt-wt/probnaya"

[ -d "$WT" ] && echo "  ✅ --worktree завёл рабочую папку" \
             || { echo "  ❌ рабочая папка не завелась — дальше проверять нечего"; FAIL=1;
                  cat "$T/wt.txt"; }

if [ -d "$WT" ]; then
    [ -f "$R2/_studio/zhurnal/arka/kod_s-wt.md" ] \
        && echo "  ✅ С --worktree заход лёг В ОСНОВНУЮ ПАПКУ (действующее правило, GIT-disciplina §4, 2026-08-03)" \
        || { echo "  ❌ ЗАХОДА НЕТ В ОСНОВНОЙ ПАПКЕ — файл не там, где его будет искать приёмка"; FAIL=1; }

    # «Нет тени» — теперь ГЛАВНАЯ проверка ловушки (соседняя не удалена, а
    # перевёрнута вместе с ожиданием выше): копии в РАБОЧЕЙ папке быть не должно.
    [ ! -f "$WT/_studio/zhurnal/arka/kod_s-wt.md" ] \
        && echo "  ✅ В РАБОЧЕЙ папке копии НЕТ (нет тени)" \
        || { echo "  ❌ ТЕНЬ В РАБОЧЕЙ ПАПКЕ — ровно та тень, из которой расходятся версии"; FAIL=1; }

    # Путь в стартовой команде обязан вести в РАБОЧУЮ папку — там код, не заход
    V=$(grep -c "cd $WT" "$T/wt.txt" || true)
    [ "$V" -ge 1 ] && echo "  ✅ стартовая команда ведёт в рабочую папку (там код)" \
                   || { echo "  ❌ стартовая команда ведёт не туда"; FAIL=1; }

    # Зона — РЕПО-ОТНОСИТЕЛЬНАЯ и в backticks (правка 1, `check_zahod.py` З3);
    # читаем файл ТАМ, где он теперь лежит по действующему правилу — в R2, не в WT.
    V=$(grep -c '\*\*ЗОНА (можно менять):\*\* `_generator/`' \
            "$R2/_studio/zhurnal/arka/kod_s-wt.md" || true)
    [ "$V" = "1" ] && echo "  ✅ зона репо-относительная и в backticks (заход входит в свою зону)" \
                   || { echo "  ❌ зона не репо-относительная или не в backticks"; FAIL=1; }

    V=$(grep -c 'kod_s-wt.md' "$R2/_studio/docs/KARTA.md" || true)
    [ "$V" = "1" ] && echo "  ✅ регистрация ушла в KARTA.md ОСНОВНОЙ папки (там же, где сам файл)" \
                   || { echo "  ❌ регистрации нет в KARTA.md основной папки — документ уедет сиротой"; FAIL=1; }
fi

# ── ЛОВУШКА 4: стартовая команда — валидна и ДАЁТ ЧИСЛО ───────────────────────
# Не «содержит нужное слово», а: (а) shell её разбирает; (б) фильтр, накормленный
# настоящей `result`-строкой, печатает стоимость и токены.
SROKA=$(sed -n '/^cd .*claude -p/,/^```$/p' "$T/plain.txt" | sed '$d')
[ -n "$SROKA" ] && echo "  ✅ стартовая команда напечатана" \
                || { echo "  ❌ стартовой команды в выводе НЕТ"; FAIL=1; }

printf '%s\n' "$SROKA" > "$T/start.sh"
if sh -n "$T/start.sh" 2>"$T/synt.txt"; then
    echo "  ✅ стартовая команда РАЗБИРАЕТСЯ шеллом (sh -n)"
else
    echo "  ❌ СТАРТОВАЯ КОМАНДА НЕ РАЗБИРАЕТСЯ — прогон не стартует вовсе:"
    cat "$T/synt.txt"; FAIL=1
fi

V=$(grep -c -- '--output-format stream-json' "$T/start.sh" || true)
[ "$V" = "1" ] && echo "  ✅ запрошен формат, который несёт стоимость (stream-json)" \
              || { echo "  ❌ формат вывода не stream-json — числа в логе не будет"; FAIL=1; }

# Настоящая `result`-строка (форма снята с живого прогона claude -p 2026-07-30).
cat > "$T/result.jsonl" <<'JSONL'
{"type":"system","subtype":"init","session_id":"x"}
это не JSON, а предупреждение — фильтр обязан пропустить его насквозь
{"type":"assistant","message":{"content":[{"type":"text","text":"Готово"},{"type":"tool_use","name":"Bash"}]}}
{"type":"result","subtype":"success","duration_ms":2832,"total_cost_usd":0.0037759,"usage":{"input_tokens":10,"output_tokens":121,"cache_read_input_tokens":25439},"modelUsage":{"claude-opus-5":{"inputTokens":537,"outputTokens":139,"costUSD":0.0037759}}}
JSONL

# Достаём из напечатанной строки РОВНО тот фильтр, который уедет владельцу:
# всё от `python3 -u -c ` до конца. Проверяется исполнением, не чтением.
python3 - "$T/start.sh" "$T/filtr.sh" <<'PY'
import sys, pathlib
s = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
kl = "python3 -u -c "
i = s.find(kl)
if i < 0:
    print("В стартовой команде нет фильтра python3 -u -c", file=sys.stderr)
    raise SystemExit(2)
pathlib.Path(sys.argv[2]).write_text(s[i:].rstrip() + "\n", encoding="utf-8")
PY

sh "$T/filtr.sh" < "$T/result.jsonl" > "$T/pokaz.txt" 2>&1 || true
# 🔴 Судим ИТОГОВУЮ СТРОКУ фильтра, а не число где угодно в выводе. Первая
# постановка искала `0.0037759` в файле целиком и осталась ЗЕЛЁНОЙ на мутации
# «фильтр падает на result-строке»: падение перехватывается и сырая строка
# печатается насквозь — а в ней это число есть. То есть проверка мерила
# присутствие подстроки, ровно чего заход и запрещает. Теперь: строка `== ПРОГОН`
# обязана существовать И нести в себе стоимость и токены.
ITOG=$(grep '== ПРОГОН' "$T/pokaz.txt" || true)
[ -n "$ITOG" ] && echo "  ✅ фильтр напечатал ИТОГОВУЮ строку прогона" \
              || { echo "  ❌ ИТОГОВОЙ СТРОКИ НЕТ — фильтр не разобрал result:"; \
                   cat "$T/pokaz.txt"; FAIL=1; }
V=$(printf '%s\n' "$ITOG" | grep -c '0.0037759' || true)
[ "$V" -ge 1 ] && echo "  ✅ в итоговой строке СТОИМОСТЬ прогона (число, а не обещание)" \
              || { echo "  ❌ ФИЛЬТР НЕ ДАЛ ЧИСЛА — токены снова придётся писать рукой:"; \
                   cat "$T/pokaz.txt"; FAIL=1; }
V=$(printf '%s\n' "$ITOG" | grep -c '25439' || true)
[ "$V" -ge 1 ] && echo "  ✅ в итоговой строке токены (вход/выход/кэш)" \
              || { echo "  ❌ токенов в итоговой строке нет"; FAIL=1; }
V=$(grep -c 'Готово' "$T/pokaz.txt" || true)
[ "$V" -ge 1 ] && echo "  ✅ фильтр показывает ход работы (текст ответа читаем)" \
              || { echo "  ❌ ход работы не показан — прогон снова непрозрачен"; FAIL=1; }
V=$(grep -c 'не JSON' "$T/pokaz.txt" || true)
[ "$V" = "1" ] && echo "  ✅ НЕ-JSON строка пропущена насквозь, а не съедена молча" \
              || { echo "  ❌ фильтр съел неразобранную строку — потеря следа"; FAIL=1; }

# Команда приёмки — тоже исполнением, а не глазами
KOM=$(sed -n "/^python3 -c 'import sys,json/,/^.*costUSD.*$/p" "$T/plain.txt")
printf '%s\n' "$KOM" > "$T/priemka.sh"
if sh -n "$T/priemka.sh" 2>/dev/null; then
    echo "  ✅ команда приёмки разбирается шеллом"
else
    echo "  ❌ команда приёмки не разбирается — приёмка не снимет число"; FAIL=1
fi
python3 - "$T/priemka.sh" "$T/result.jsonl" "$T/priemka-run.sh" <<'PY'
import sys, pathlib
s = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8").rstrip()
# путь в напечатанной команде — от прогона; подставляем фикстурный лог
i = s.rfind("'")
pathlib.Path(sys.argv[3]).write_text(s[:i + 1] + " " + sys.argv[2] + "\n", encoding="utf-8")
PY
sh "$T/priemka-run.sh" > "$T/priemka.txt" 2>&1 || true
V=$(grep -c 'стоимость USD: 0.0037759' "$T/priemka.txt" || true)
[ "$V" = "1" ] && echo "  ✅ команда приёмки СНИМАЕТ число из лога (§10 удовлетворён командой)" \
              || { echo "  ❌ команда приёмки числа не дала:"; cat "$T/priemka.txt"; FAIL=1; }
V=$(grep -c 'claude-opus-5' "$T/priemka.txt" || true)
[ "$V" -ge 1 ] && echo "  ✅ команда приёмки даёт разбивку по моделям" \
              || { echo "  ❌ разбивки по моделям нет"; FAIL=1; }

# ── ЛОВУШКА 4б: МЕТАСИМВОЛЫ В ТЕМЕ НЕ МЕНЯЮТ СМЫСЛ СТРОКИ ────────────────────
# Найдено верификатором живым запуском, и худшая форма была ТИХОЙ: `&` в теме
# давал `tee /tmp/zahod-a &` — прогон уходил в ФОН, фильтр обходился, владелец
# видел вернувшийся промпт и ноль вывода. `*` в zsh отменял строку целиком
# несовпавшим глобом. Одинарная кавычка спаривалась с кавычкой фильтра и
# переворачивала цитирование — а прежняя «защита» МЕНЯЛА двойную кавычку на
# одинарную, то есть сама создавала эту поломку, обещая обратное.
# 🔴 Судим не «есть ли кавычка в выводе», а РАЗБОР строки шеллом и ОТСУТСТВИЕ
# фонового запуска: `sh -n` метасимвол пропускает — он синтаксически законен.
# 🔴 СУДИМ ИСПОЛНЕНИЕ, А НЕ ЛЕКСИКУ. Первая постановка искала «одиночный `&`»
# регуляркой и краснела на ЗДОРОВОЙ строке: амперсанд внутри УЖЕ ЗАЦИТИРОВАННОГО
# пути (`'/tmp/zahod-a&b.jsonl'`) для шелла безобиден, а регулярка про кавычки не
# знает. Поэтому здесь подставной `claude`, реальный прогон строки и три
# утверждения о РЕЗУЛЬТАТЕ: дошёл ли поток до фильтра, синхронно ли это
# случилось, лёг ли лог туда, куда указывает команда приёмки.
mkdir -p "$T/stub"
cat > "$T/stub/claude" <<'STUB'
#!/bin/sh
printf '%s\n' '{"type":"assistant","message":{"content":[{"type":"text","text":"подстава"}]}}'
printf '%s\n' '{"type":"result","subtype":"success","duration_ms":1000,"total_cost_usd":0.5,"usage":{"input_tokens":1,"output_tokens":2,"cache_read_input_tokens":3}}'
STUB
chmod +x "$T/stub/claude"

for TEMA in "fixt-a&b" "fixt-a;b" "fixt-a*b" "fixt-a\$b" "fixt-a|b" "fixt-it's" 'fixt-ka"vy'; do
    R4="$T/repo-meta"
    rm -rf "$R4"; podgotovit "$R4" > /dev/null 2>&1
    GIT_ZONA_REPO="$R4" python3 "$T/zvat.py" "$GEN" "$R4" \
        _studio/zhurnal/arka "$TEMA" --branch osnova --zone "_generator/" \
        --finalizirovano "ф1" --finalizirovano "ф2" \
        --kanal terminal --opisanie "проба метасимволов" > "$T/meta.txt" 2>&1 || true
    S=$(sed -n '/^cd .*claude -p/,/^```$/p' "$T/meta.txt" | sed '$d')
    if [ -z "$S" ]; then
        # Генератор ОТКАЗАЛ на кривом имени — законный и даже лучший исход
        printf '  ✅ тема [%s]: генератор отказал, строки нет (кривой вход отбит)\n' "$TEMA"
        continue
    fi
    printf '%s\n' "$S" > "$T/meta.sh"
    LOG="/tmp/zahod-$TEMA.jsonl"
    rm -f "$LOG"
    OK=1
    sh -n "$T/meta.sh" 2>/dev/null || OK=0
    if command -v zsh > /dev/null 2>&1; then
        zsh -n "$T/meta.sh" 2>/dev/null || OK=0
    fi
    # Прогон подставным claude. Уйди строка в фон — к моменту возврата ни итоговой
    # строки на stdout, ни готового лога не будет.
    PATH="$T/stub:$PATH" sh "$T/meta.sh" > "$T/meta-run.txt" 2>&1 || true
    ITG=$(grep -c '== ПРОГОН' "$T/meta-run.txt" || true)
    [ -f "$LOG" ] && LG=1 || LG=0
    if [ "$OK" = "1" ] && [ "$ITG" = "1" ] && [ "$LG" = "1" ]; then
        printf '  ✅ тема [%s]: строка разбирается, прогон синхронный, лог на месте\n' "$TEMA"
    else
        printf '  ❌ ТЕМА [%s] ЛОМАЕТ ЗАПУСК (разбор=%s, итог=%s, лог=%s)\n' \
            "$TEMA" "$OK" "$ITG" "$LG"
        echo "     — прогон не стартует, уходит в фон или пишет лог не туда"
        head -3 "$T/meta-run.txt"
        FAIL=1
    fi
    rm -f "$LOG"
done

# ── ЛОВУШКА 4в: имя рабочей папки валидируется, побег из дома `-wt` невозможен ─
# `--worktree "../../pobeg"` создавал папку ВНЕ дома `<репо>-wt` и заводил там
# заход с регистрацией — тот класс, для которого validate_slug и существует.
# ⚠ Ветка НЕ `osnova`, а новая. С `osnova` `git worktree add` отказывает сам
# («already used by worktree») — и проверка оставалась ЗЕЛЁНОЙ на снятой валидации,
# потому что побег ломался о постороннюю причину (поймано мутацией). На новой
# ветке папка заводится, и защитой остаётся ровно validate_slug.
for WTN in "../../pobeg" ".skrytaya" "s probelom" "-flag"; do
    R5="$T/repo-wtname"
    rm -rf "$R5"; podgotovit "$R5" > /dev/null 2>&1
    cp "$T/gz-src.py" "$R5/_generator/tools/git_zona.py"
    GIT_ZONA_REPO="$R5" python3 "$T/zvat.py" "$GEN" "$R5" \
        _studio/zhurnal/arka wtn --branch zahod/wtn-proba --zone "_generator/" \
        --finalizirovano "ф1" --finalizirovano "ф2" \
        --worktree "$WTN" --kanal app --opisanie "проба имени папки" > "$T/wtn.txt" 2>&1 && G=proshlo || G=otkaz
    if [ "$G" = "otkaz" ]; then
        printf '  ✅ имя рабочей папки [%s] отвергнуто\n' "$WTN"
    else
        printf '  ❌ ИМЯ ПАПКИ [%s] ПРОШЛО — заход мог уехать вне дома -wt\n' "$WTN"
        FAIL=1
    fi
    if [ ! -f "$T/pobeg/_studio/zhurnal/arka/kod_wtn.md" ] && [ ! -d "$T/../pobeg" ]; then
        printf '  ✅ имя [%s]: за пределами дома -wt ничего не создано\n' "$WTN"
    else
        echo "  ❌ ФАЙЛ СОЗДАН ВНЕ ДОМА -wt — побег из дома рабочих папок"
        FAIL=1
    fi
done

# ── ЛОВУШКА 4г: существующая папка на ЧУЖОЙ ветке — отказ, а не молчание ──────
# Заход утверждает «ветка уже стоит, checkout ЗАПРЕЩЁН». Если в папке другая
# ветка, это утверждение — ложь при зелёном выводе, и исполнитель работает не там,
# где думает. Пока файл ложился в основную папку, промах был безобиден.
R6="$T/repo-vetka"
podgotovit "$R6"
cp "$T/gz-src.py" "$R6/_generator/tools/git_zona.py"
GIT_ZONA_REPO="$R6" python3 "$T/zvat.py" "$GEN" "$R6" \
    _studio/zhurnal/arka pervyj --branch zahod/pervaya --zone "_generator/" \
    --finalizirovano "ф1" --finalizirovano "ф2" \
    --worktree obshaya --kanal app --opisanie "первый заход" > /dev/null 2>&1 || true
if [ -d "$T/repo-vetka-wt/obshaya" ]; then
    if GIT_ZONA_REPO="$R6" python3 "$T/zvat.py" "$GEN" "$R6" \
        _studio/zhurnal/arka vtoroj --branch zahod/sovsem-drugaya --zone "_generator/" \
        --finalizirovano "ф1" --finalizirovano "ф2" \
        --worktree obshaya --kanal app --opisanie "второй заход" > "$T/vetka.txt" 2>&1
    then
        echo "  ❌ ПАПКА НА ЧУЖОЙ ВЕТКЕ ВЗЯТА МОЛЧА — заход соврёт про ветку при зелёном выводе"
        FAIL=1
    else
        echo "  ✅ папка на чужой ветке — ОТКАЗ (заход не соврёт про ветку)"
    fi
    [ ! -f "$T/repo-vetka-wt/obshaya/_studio/zhurnal/arka/kod_vtoroj.md" ] \
        && echo "  ✅ при несовпадении ветки заход не создан" \
        || { echo "  ❌ заход создан в папке с чужой веткой"; FAIL=1; }
else
    echo "  ⚠ ловушка 4г пропущена: папка obshaya не завелась"
fi

# ── ЛОВУШКА 5: ХУК ГОНИТ ФИКСТУРУ ПО ОХВАТУ, А НЕ ПО ШАБЛОНУ ПУТИ ─────────────
# Гоняет РЕАЛЬНЫЙ .githooks/pre-commit и check_tool_contract.py (копия файлов,
# не пересказ логики) в одноразовом репо. Подсадная фикстура объявляет охват над
# файлом ВНЕ старых каталоговых шаблонов хука (`_generator/tools/*.py` и т.п.) —
# ровно класс, которым была `skeleton/engine.js` до починки долга 1.
R7="$T/repo-ohvat"
mkdir -p "$R7/.githooks" "$R7/_generator/tools/fixtures/mnimaya" "$R7/mnimyj-modul"
cp "$REPO/.githooks/pre-commit" "$R7/.githooks/pre-commit"
cp "$TOOLS/check_tool_contract.py" "$R7/_generator/tools/check_tool_contract.py"
cp "$TOOLS/check_uroki.py" "$R7/_generator/tools/check_uroki.py"
cp "$TOOLS/check_ves.py" "$R7/_generator/tools/check_ves.py"
cp "$TOOLS/check_marker.py" "$R7/_generator/tools/check_marker.py"
chmod +x "$R7/.githooks/pre-commit"

# Флаг красный/зелёный — файл на диске, не переменная окружения: хук зовёт
# фикстуру отдельным процессом `sh`, и переменная до него не доедет.
cat > "$R7/_generator/tools/fixtures/mnimaya/PROGNAT.sh" <<SH
#!/bin/sh
# TOOL-CONTRACT-COVERS: mnimyj-instrument.js
[ -f "$R7/.mnimaya-fail" ] && exit 1
exit 0
SH
chmod +x "$R7/_generator/tools/fixtures/mnimaya/PROGNAT.sh"

git init -q "$R7"
git -C "$R7" config user.email fixture@test
git -C "$R7" config user.name fixture
git -C "$R7" config core.hooksPath .githooks
echo "исходный" > "$R7/mnimyj-modul/mnimyj-instrument.js"
echo "исходный" > "$R7/mnimyj-modul/nikto-ne-pokryvaet.js"
# `add` — ТОЛЬКО тестовый модуль. Хук/check_tool_contract.py/фикстура-подсадка
# нужны на ДИСКЕ (хук читает их как файлы), но не в индексе: застейдженные, они
# сами стали бы «правленым инструментом» без охвата и гейт судил бы СЕБЯ.
git -C "$R7" add mnimyj-modul > /dev/null 2>&1
if ! git -C "$R7" commit -qm "база" > "$T/ohvat-baza.txt" 2>&1; then
    echo "  ❌ БАЗОВЫЙ КОММИТ СТЕНДА НЕ ПРОШЁЛ — ловушка 5 не запустится:"
    cat "$T/ohvat-baza.txt"; FAIL=1
fi

# (а) путь под охватом, вне старых шаблонов, фикстура КРАСНАЯ — коммит ОБЯЗАН встать
echo "правка" >> "$R7/mnimyj-modul/mnimyj-instrument.js"
: > "$R7/.mnimaya-fail"
git -C "$R7" add mnimyj-modul/mnimyj-instrument.js > /dev/null 2>&1
if git -C "$R7" commit -qm "правка покрытого, фикстура красная" > "$T/ohvat-a.txt" 2>&1
then
    echo "  ❌ ПОКРЫТЫЙ ПУТЬ ВНЕ ШАБЛОНА ПРОШЁЛ ПРИ КРАСНОЙ ФИКСТУРЕ — охват не сработал"
    FAIL=1
else
    echo "  ✅ покрытый путь вне старых шаблонов: красная фикстура ОСТАНОВИЛА коммит"
fi

# (б) тот же путь, фикстура ЗЕЛЁНАЯ — коммит обязан пройти (хук не шумит попусту)
rm -f "$R7/.mnimaya-fail"
if git -C "$R7" commit -qm "правка покрытого, фикстура зелёная" > "$T/ohvat-b.txt" 2>&1
then
    echo "  ✅ покрытый путь вне старых шаблонов: зелёная фикстура НЕ мешает коммиту"
else
    echo "  ❌ ЗЕЛЁНАЯ ФИКСТУРА ВСЁ РАВНО ОСТАНОВИЛА — хук стал шумным"
    FAIL=1
    cat "$T/ohvat-b.txt"
fi

# (в) путь БЕЗ объявленного охвата — коммитится молча, фикстура не поднимается
echo "правка" >> "$R7/mnimyj-modul/nikto-ne-pokryvaet.js"
git -C "$R7" add mnimyj-modul/nikto-ne-pokryvaet.js > /dev/null 2>&1
if git -C "$R7" commit -qm "правка без охвата" > "$T/ohvat-v.txt" 2>&1
then
    echo "  ✅ путь без охвата коммитится молча (фикстура не поднята зря)"
else
    echo "  ❌ ПУТЬ БЕЗ ОХВАТА ЗАБЛОКИРОВАН — хук стал шумным на здоровом пути"
    FAIL=1
    cat "$T/ohvat-v.txt"
fi
if grep -q 'mnimaya' "$T/ohvat-v.txt"; then
    echo "  ❌ ФИКСТУРА mnimaya ПОДНЯТА НА ПУТИ БЕЗ ОХВАТА — ложное срабатывание"
    FAIL=1
fi

# ── Шаблон отчёта: исполнителю сказано, что счётчик снимает ПРИЁМКА ───────────
V=$(grep -c 'снимает ПРИЁМКА из лога' "$R1/_studio/zhurnal/arka/kod_bez-wt.md" || true)
[ "$V" = "1" ] && echo "  ✅ в шаблоне отчёта сказано: время и токены снимает приёмка из лога" \
              || { echo "  ❌ строки про приёмку нет — исполнители снова будут извиняться"; FAIL=1; }

# Обратная сторона якорной замены: якоря НЕТ — генератор обязан ОТКАЗАТЬ, а не
# молча выдать заход без строки. Без этой половины «замена не сработала» и
# «замену не просили» неразличимы, а разъезд шаблона с генератором обнаружится
# только тем, что исполнитель снова извинится за счётчик.
R3="$T/repo-bez-yakorya"
podgotovit "$R3"
printf '%s\n' '{{ТЕМА}} {{МОДЕЛЬ}} {{ВЕТКА}}' 'ЗОНА: {{ЗОНА}}' '{{КОНТРАКТ_МЕСТО}}' \
    '{{ПЕРВЫЙ_ХОД}}' 'отчёт: без якоря / КОММИТ' \
    > "$R3/_studio/zhurnal/_TEMPLATE-zahod.md"
if GIT_ZONA_REPO="$R3" python3 "$T/zvat.py" "$GEN" "$R3" \
        _studio/zhurnal/arka net-yakorya --branch osnova --zone "_generator/" \
        --finalizirovano "ф1" --finalizirovano "ф2" \
        --kanal terminal --opisanie "проба без якоря" > "$T/net-yak.txt" 2>&1
then
    echo "  ❌ ШАБЛОН БЕЗ ЯКОРЯ ПРОШЁЛ — заход уедет без строки про счётчик, молча"; FAIL=1
else
    echo "  ✅ шаблон без якоря токенов ОТКЛОНЁН (разъезд не проходит молча)"
fi
[ ! -f "$R3/_studio/zhurnal/arka/kod_net-yakorya.md" ] \
    && echo "  ✅ при отказе по якорю файл НЕ создан (кривой заход хуже отсутствующего)" \
    || { echo "  ❌ файл создан несмотря на отказ"; FAIL=1; }

# ── ОХВАТ на любом исходе: зелёное без охвата читается как «всё в порядке» ────
if [ "$BROWSER_OK" = "1" ]; then
    echo "Охват: ловушки 1-5 проверены, 5 из 5 (браузер поднялся)"
else
    echo "Охват: проверены ловушки 3-5, 3 из 5 — ЛОВУШКИ 1-2 ПРОПУЩЕНЫ (нет playwright)"
fi

[ "$FAIL" = "0" ] && { echo "ФИКСТУРЫ ЗЕЛЁНЫЕ"; exit 0; } || { echo "ФИКСТУРЫ КРАСНЫЕ"; exit 1; }
