#!/usr/bin/env python3
"""ГЕЙТ СОГЛАСОВАННОСТИ КАРТЫ — реестр §5 живой карты против ДИСКА.

    python3 _generator/tools/check_karty.py                 # живое дерево
    python3 _generator/tools/check_karty.py --karta <путь>  # другой файл карты
    python3 _generator/tools/check_karty.py -v              # печатать зелёные подробности

ЗАЧЕМ. Карта живого конвейера протухала дважды, и второй раз — на самой себе:
в ней стояло «ГЕЙТ ВМЕЩЕНИЯ не существует, долг», при том что `gejt_vmeshcheniya.py`
лежал рядом, написанный и подключённый. Карта прочитала ДОКУМЕНТАЦИЮ вместо ДИСКА —
ровно тот грех, ради разоблачения которого писалась. Прозе нечем краснеть; поэтому
описание фабрики переведено в РЕЕСТР (§5 карты), а этот файл его сторожит.

🔴 ЧЕТЫРЕ ИНВАРИАНТА, каждый краснеет ОТДЕЛЬНО и называет виновника поимённо:

  И1  каждый инструмент `_generator/**/*.py` есть в реестре
      (завёл инструмент, не вписал строку → красное)
  И2  каждая строка реестра существует на диске
      (удалил или переименовал файл, забыл строку → красное)
  И3  у каждого ЖИВОГО есть кто-зовёт
      🔴 ЛОГИКА НЕ ПОВТОРЯЕТСЯ, А ЗОВЁТСЯ: ответ даёт `check_tool_contract.py`,
      одним прогоном на все живые пути. Третий источник правды о том же — ровно
      та болезнь, от которой лечит этот гейт.
  И4  каждый гейт, названный в колонке «Гейт» таблицы фаз §1, существует и вызывается
      (этого не было ни у кого, и отсюда пришла ложь про гейт вмещения)

🔴 ЗАКОННАЯ ПУСТОТА ОТЛИЧАЕТСЯ ОТ ДЫРЫ ФОРМОЙ, А НЕ НАМЕРЕНИЕМ. У инструмента может
не быть фикстуры, у фазы — верификатора: это находка, а не ошибка. Но записывается
она ЯВНО — клеткой ровно вида `нет: <причина>`. Пустая клетка или прочерк — красное.
Объявленные дыры печатаются списком ВСЕГДА, включая полный зелёный прогон: гейт,
у которого объявленную дыру не видно, зеленее, чем состояние фабрики.

🔴 ЧЕГО ЭТОТ ГЕЙТ НЕ ПРОВЕРЯЕТ (печатается всегда, чтобы зелёный не читали шире):
- колонка «фаза / роль» машинно не проверяется ничем: сказать, что инструмент отнесён
  не к той фазе, гейт не может;
- «кто зовёт» стоит на текстовой эвристике `check_tool_contract.has_live_trigger()` —
  упомянут ли basename вне своего файла; `import korpus` (имя модуля без `.py`) она не
  видит, а упоминание в докстринге СЧИТАЕТ вызовом;
- `.py` внутри `fixtures/`, `vendor/`, `skeleton/` в охват И1 не входят: это нагрузка
  фикстур и вендор, а не инструменты фабрики (то же исключение, что у
  `check_tool_contract.check_live_trigger`);
- статус `ЖИВ`/`АРХИВ` — решение человека; гейт сверяет его следствия, а не сам статус;
- гейт судит ТОЛЬКО живую карту. Файлы старого конвейера (`GEJTY.md` и стадии,
  помеченные `🗄 АРХИВ`) он не читает вовсе — поэтому 17 архивных гейтов его не красят
  по построению, а не по списку исключений.

Только stdlib. Ничего не исполняет, кроме одного вызова `check_tool_contract.py`.

# TOOL-CONTRACT: called-by-hand — живая точка вызова названа и готова: строка для
# `.githooks/pre-commit` на staged `_generator/**/*.py` выписана в `## ВОПРОСЫ` захода
# `karta-kak-reestr`; сам хук лежит ВНЕ зоны того захода, поэтому строку ставит владелец.
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
# KARTY_REPO — та же дверь, что `GIT_ZONA_REPO` у `git_zona.py`: фикстура гоняет гейт
# на одноразовом дереве, боевой репозиторий при этом не адресуется вовсе.
REPO = Path(os.environ.get("KARTY_REPO") or TOOLS.parent.parent)
KARTA_REL = "_studio/konvejer/KARTA-ZHIVOGO-KONVEJERA.md"
KONTRAKT = TOOLS / "check_tool_contract.py"

# Папки, чьи `.py` инструментами фабрики не являются.
VNE_OHVATA = ("fixtures", "vendor", "skeleton", "__pycache__", "node_modules")

ZAGOLOVOK_REESTRA = re.compile(r'^##\s+5\.\s.*РЕЕСТР\s+ИНСТРУМЕНТОВ', re.M)
ZAGOLOVOK_FAZ = re.compile(r'^##\s+1\.\s', re.M)
SLEDUYUSHCHIJ = re.compile(r'^##\s', re.M)
# Строка реестра: первая клетка — путь в обратных кавычках, остальные — по заголовку.
STROKA_RE = re.compile(r'^\|\s*`[^`]+`\s*\|')
# Строка-разделитель markdown-таблицы: `|---|---|…|`.
RAZDELITEL_RE = re.compile(r'^\|[\s:|-]+\|$')
STATUSY = ("ЖИВ", "АРХИВ")
# Законная пустота: клетка ровно вида `нет: <причина>`, причина непустая.
NET_RE = re.compile(r'^нет:\s*\S')
PUSTO = ("", "—", "-", "–", "нет", "нет:", "н/д", "N/A")
# Имя инструмента внутри клетки таблицы фаз: `что-то.py`.
PY_RE = re.compile(r'`([\w.-]+\.py)`')
# Явное объявление «гейта-инструмента у фазы нет, и вот почему».
NET_GEJTA_RE = re.compile(r'нет\s+\.py-гейта:\s*\S')
# 🔴 Реестр читается ПО ИМЕНИ заголовка колонки, не по позиции и не по счёту клеток
# (заход `final-sessii`): реестр задуман растущим (§5 «ЗАЧЕМ»), рост колонок вправо
# не обязан ронять парсер. Маркер — подстрока в заголовке клетки, без учёта регистра.
IMENA_KOLONOK = {
    "put": ("файл",),
    "rol": ("фаза",),
    "zovut": ("зов",),        # «кто зовёт»
    "proveren": ("провер",),  # «чем проверен»
    "status": ("статус",),
}


def telo_sekcii(text, zagolovok_re):
    """Тело секции после заголовка — до следующего `## `. None, если секции нет."""
    m = zagolovok_re.search(text)
    if not m:
        return None
    hvost = text[m.end():]
    nxt = SLEDUYUSHCHIJ.search(hvost)
    return hvost[:nxt.start()] if nxt else hvost


def zagolovok_kolonok(stroka):
    """Имя→индекс клетки по строке-заголовку таблицы. Нераспознанные клетки не входят."""
    indeksy = {}
    for i, imya in enumerate(kletki(stroka)):
        nizhnyaya = imya.strip().lower()
        for klyuch, markery in IMENA_KOLONOK.items():
            if klyuch not in indeksy and any(m in nizhnyaya for m in markery):
                indeksy[klyuch] = i
    return indeksy


def kletki(stroka):
    """Клетки markdown-строки таблицы. `| a | b |` → `['a', 'b']`."""
    if not stroka.strip().startswith('|'):
        return []
    chasti = stroka.strip().split('|')
    return [c.strip() for c in chasti[1:-1]] if len(chasti) >= 3 else []


def zapolnena(kletka):
    """Клетка несёт содержание либо объявляет пустоту с причиной."""
    return bool(kletka) and kletka not in PUSTO


def obyavlennaya_pustota(kletka):
    return bool(NET_RE.match(kletka))


def chitat_reestr(text):
    """`(строки, ошибки формы)`. Строка — dict с пятью полями и номером строки.

    🔴 Формат судится ДО содержания: реестр, который нельзя разобрать программой, —
    это снова текст, а текст протух уже дважды.

    Колонки читаются ПО ИМЕНИ заголовка таблицы (`zagolovok_kolonok()`), не по позиции
    и не по счёту клеток: реестр задуман растущим (§5 «ЗАЧЕМ»), лишние клетки справа
    (например УРОВЕНЬ) не роняют строку. Требуются только пять семантических колонок
    из `IMENA_KOLONOK`; их порядок в самой таблице неважен.

    🔴 Таблица ищется ПО СОДЕРЖИМОМУ, не по номеру подраздела: заголовок `|...|`
    (называющий все нужные колонки) сразу над строкой-разделителем `|---|...|`. Как
    только строка данных обрывается (первая НЕ-`|`-строка после начала таблицы) —
    чтение таблицы останавливается СРАЗУ, дальше в разделе «## 5.» не ходим. Это же
    решает и ловушку STROKA_RE «где угодно в разделе»: раньше тело секции читалось
    целиком до следующего «## », и строки вида `| \`путь\` | … |` из §5.5 (список,
    похожий на форму реестра) ловились как настоящие — заход `uroven-instrumentov`
    поэтому переписал §5.5 списком. Первая попытка чинить это якорем на «### 5.2»
    сломала фикстуру `fixtures/karty/PROGNAT.sh` — та строит `## 5.` БЕЗ подраздела,
    таблица идёт сразу под заголовком секции; поиск по содержимому таблицы работает
    в обеих формах.
    """
    telo = telo_sekcii(text, ZAGOLOVOK_REESTRA)
    if telo is None:
        return [], ["раздела «## 5. РЕЕСТР ИНСТРУМЕНТОВ» в карте нет — сверять нечего"]
    stroki, oshibki = [], []
    nachalo = text.index(telo)
    # 🔴 КОД-БЛОКИ НЕ ЧИТАЮТСЯ. §5.1 показывает ФОРМУ строки реестра примером внутри
    # ```-блока, и первый же живой прогон принял этот пример за настоящую строку.
    # Тот же закон, что у `check_sborki` («заход, который ЦИТИРУЕТ, ничего не
    # утверждает»): иначе гейт краснеет на собственной документации, а такой отключают.
    v_bloke = False
    indeksy = None
    zhdyom_razdelitel = False
    v_tablice = False
    for sdvig, ln in enumerate(telo.splitlines()):
        if ln.lstrip().startswith("```"):
            v_bloke = not v_bloke
            continue
        if v_bloke:
            continue
        stripped = ln.strip()
        if v_tablice:
            if not stripped.startswith("|"):
                break  # первая НЕ-табличная строка — таблица кончилась, дальше не читаем
            if not STROKA_RE.match(ln):
                continue  # строка-разделитель или иная служебная — не данные
            nomer = text[:nachalo].count('\n') + sdvig + 1
            k = kletki(ln)
            maks_indeks = max(indeksy.values())
            if len(k) <= maks_indeks:
                oshibki.append(f"строка {nomer}: клеток {len(k)}, а по заголовку таблицы "
                               f"нужно хотя бы {maks_indeks + 1}")
                continue
            put = k[indeksy["put"]].strip('`')
            status = k[indeksy["status"]]
            if status not in STATUSY:
                oshibki.append(f"строка {nomer} (`{put}`): статус «{status}» — разрешены "
                               f"только {' и '.join(STATUSY)}")
                continue
            rol, zovut, proveren = (k[indeksy["rol"]], k[indeksy["zovut"]],
                                    k[indeksy["proveren"]])
            for imya, kletka in (("фаза / роль", rol), ("кто зовёт", zovut),
                                 ("чем проверен", proveren)):
                if not zapolnena(kletka):
                    oshibki.append(f"строка {nomer} (`{put}`): клетка «{imya}» пуста МОЛЧА. "
                                   f"Законная пустота пишется явно: `нет: <причина>` — "
                                   f"иначе «мы про это знаем» неотличимо от «мы это забыли»")
            stroki.append({"put": put, "rol": rol, "zovut": zovut, "proveren": proveren,
                           "status": status, "nomer": nomer})
            continue
        if zhdyom_razdelitel:
            zhdyom_razdelitel = False
            if RAZDELITEL_RE.match(stripped):
                v_tablice = True
            else:
                indeksy = None  # ложная тревога — не заголовок таблицы, ищем дальше
            continue
        if stripped.startswith("|"):
            kandidat = zagolovok_kolonok(ln)
            if set(IMENA_KOLONOK) <= set(kandidat):
                indeksy = kandidat
                zhdyom_razdelitel = True
    if indeksy is None or not v_tablice:
        oshibki.append("в §5 не найдена таблица реестра — заголовок со всеми нужными "
                       "колонками, сразу над строкой-разделителем `|---|---|…`; "
                       "сверять нечего")
    return stroki, oshibki


def instrumenty_na_diske():
    """Инструменты фабрики на диске — охват И1."""
    koren = REPO / "_generator"
    if not koren.is_dir():
        return []
    out = []
    for p in sorted(koren.rglob("*.py")):
        if any(chast in VNE_OHVATA for chast in p.relative_to(koren).parts):
            continue
        out.append(str(p.relative_to(REPO)))
    return out


def bez_zovushchego(puti):
    """Пути, у которых `check_tool_contract.py` НЕ видит живой точки вызова.

    🔴 Одним прогоном на все пути и ЧУЖИМ инструментом. Своя копия эвристики была бы
    третьим источником правды о том же самом — ровно диагноз, ради которого гейт писан.
    Возврат — `(множество путей, причина отказа|None)`: не смогли спросить — это НЕ
    зелёное, это «проверить нечем», и оно печатается, а не проглатывается.
    """
    if not puti:
        return set(), None
    if not KONTRAKT.is_file():
        return set(), f"инструмент `{KONTRAKT.name}` не найден рядом"
    try:
        r = subprocess.run([sys.executable, str(KONTRAKT), *puti],
                           capture_output=True, text=True, timeout=180,
                           cwd=str(REPO), shell=False)
    except (OSError, subprocess.TimeoutExpired) as e:
        return set(), f"{KONTRAKT.name} не отработал ({e.__class__.__name__})"
    # 🔴 СВЕРКА ПО РАЗРЕШЁННОМУ ПУТИ, А НЕ ПО СТРОКЕ. `check_tool_contract` печатает
    # путь относительно СВОЕГО корня, и совпадает он не всегда: на macOS `/var` —
    # симлинк на `/private/var`, поэтому у временного дерева фикстуры корень в выводе
    # абсолютный. Сверка строками давала ПУСТОЙ ответ «кто без вызова» — то есть
    # инвариант 3 молча зеленел на любом дереве. Поймано ловушкой 3 фикстуры.
    po_realnomu = {}
    for p in puti:
        try:
            po_realnomu[str((REPO / p).resolve())] = p
        except OSError:
            po_realnomu[str(REPO / p)] = p
    tekushchij, bez = None, set()
    for ln in r.stdout.splitlines():
        if ln.startswith("❌ ") and ln.strip().endswith(".py"):
            syroj = Path(ln[2:].strip())
            if not syroj.is_absolute():
                syroj = REPO / syroj
            try:
                tekushchij = po_realnomu.get(str(syroj.resolve()))
            except OSError:
                tekushchij = None
        elif "живая точка вызова" in ln and tekushchij:
            bez.add(tekushchij)
    return bez, None


def gejty_faz(text):
    """`[(фаза, [инструменты], объявлено_ли_отсутствие, номер строки)]` — из таблицы §1.

    Колонка «Гейт» — пятая по счёту в шапке таблицы фаз; ищется ПО ШАПКЕ, а не по
    номеру наизусть: переставят колонку — гейт обязан сказать об этом, а не молча
    читать соседнюю.
    """
    telo = telo_sekcii(text, ZAGOLOVOK_FAZ)
    if telo is None:
        return None, "раздела «## 1.» (таблица фаз) в карте нет"
    indeks, out = None, []
    nachalo = text.index(telo)
    for sdvig, ln in enumerate(telo.splitlines()):
        k = kletki(ln)
        if not k:
            continue
        if indeks is None:
            if "Гейт" in k:
                indeks = k.index("Гейт")
            continue
        if len(k) <= indeks or set(k[0]) <= set("-: "):
            continue
        if not re.match(r'\*\*\d', k[0]):
            continue
        nomer = text[:nachalo].count('\n') + sdvig + 1
        kletka = k[indeks]
        out.append((k[0].strip('* '), PY_RE.findall(kletka),
                    bool(NET_GEJTA_RE.search(kletka)), nomer))
    if indeks is None:
        return None, "в таблице фаз §1 нет колонки «Гейт» — карта и гейт разъехались"
    return out, None


def sudit(text):
    """`(красные, объявленные дыры)`. Красное — `(код, текст)`."""
    krasnye, obyavleno = [], []
    stroki, oshibki_formy = chitat_reestr(text)
    for o in oshibki_formy:
        krasnye.append(("ФОРМА", o))

    po_puti = {s["put"]: s for s in stroki}
    dubli = len(stroki) - len(po_puti)
    if dubli:
        krasnye.append(("ФОРМА", f"строк реестра {len(stroki)}, различных путей "
                                 f"{len(po_puti)} — {dubli} путь(ей) записан(ы) дважды"))

    # ── И1: каждый .py на диске есть в реестре ────────────────────────────────
    na_diske = instrumenty_na_diske()
    ne_vpisany = [p for p in na_diske if p not in po_puti]
    for p in ne_vpisany:
        krasnye.append(("И1", f"инструмент `{p}` есть на диске, но строки в реестре §5 "
                              f"у него НЕТ — заведён и не вписан"))

    # ── И2: каждая строка реестра существует на диске ─────────────────────────
    for s in stroki:
        if not (REPO / s["put"]).is_file():
            krasnye.append(("И2", f"строка реестра {s['nomer']} называет `{s['put']}`, "
                                  f"а файла на диске НЕТ — удалён или переименован, "
                                  f"строка осталась"))

    # ── И3: у каждого ЖИВОГО есть кто-зовёт ───────────────────────────────────
    zhivye = [s for s in stroki if s["status"] == "ЖИВ" and (REPO / s["put"]).is_file()]
    bez, otkaz = bez_zovushchego([s["put"] for s in zhivye])
    if otkaz:
        krasnye.append(("И3", f"спросить `check_tool_contract.py` не удалось ({otkaz}) — "
                              f"инвариант 3 НЕ проверен, это не зелёное"))
    else:
        for s in zhivye:
            zayavleno_net = obyavlennaya_pustota(s["zovut"])
            if s["put"] in bez and not zayavleno_net:
                krasnye.append(("И3", f"`{s['put']}` числится ЖИВЫМ, а живой точки вызова "
                                      f"у него нет (`check_tool_contract.py` → «живая точка "
                                      f"вызова»). Либо подключи, либо объяви в клетке «кто "
                                      f"зовёт» строкой `нет: <причина>`"))
            elif s["put"] in bez:
                obyavleno.append(f"И3 · `{s['put']}` — зовущего нет, объявлено: {s['zovut']}")
            elif zayavleno_net:
                # 🔴 РАСХОЖДЕНИЕ, А НЕ КРАСНОЕ — и это не смягчение, а вывод из замера.
                # Сначала здесь стояло красное «реестр отстал»: раз гейт находит зовущего,
                # значит объявление устарело. Независимая сверка пяти случайных строк
                # показала обратное: `has_live_trigger` — текстовая эвристика, и она
                # считает вызовом упоминание в докстринге соседа (`priyomka.py`,
                # `podgonka.py`, `korpus.py`). Реестр заполняется ЗАМЕРОМ настоящих
                # вызовов и потому строже. Краснеть на том, что человек точнее машины, —
                # это гейт, который наказывает за правду; такой отключают первым же вечером.
                obyavleno.append(f"И3 · расхождение по `{s['put']}`: реестр говорит "
                                 f"«{s['zovut'][:60]}», а эвристика `check_tool_contract` "
                                 f"зовущего находит. Реестр судит настоящие вызовы, "
                                 f"эвристика — упоминание имени; проверьте, кто прав")

    for s in stroki:
        if obyavlennaya_pustota(s["proveren"]):
            obyavleno.append(f"§5 · `{s['put']}` — не покрыт фикстурой, объявлено: "
                             f"{s['proveren']}")

    # ── И4: гейт, названный в описании фазы, существует и вызывается ──────────
    fazy, beda = gejty_faz(text)
    if beda:
        krasnye.append(("И4", beda))
    else:
        po_imeni = {}
        for put in po_puti:
            po_imeni.setdefault(Path(put).name, []).append(put)
        for faza, imena, obyavlen_nol, nomer in fazy:
            if not imena:
                if obyavlen_nol:
                    obyavleno.append(f"И4 · фаза {faza} — .py-гейта нет, объявлено в карте")
                else:
                    krasnye.append(("И4", f"у фазы «{faza}» (строка {nomer}) в колонке «Гейт» "
                                          f"не назван НИ ОДИН инструмент и не объявлено "
                                          f"«нет .py-гейта: <причина>» — пустая клетка молча"))
                continue
            for imya in imena:
                kandidaty = po_imeni.get(imya, [])
                if not kandidaty:
                    krasnye.append(("И4", f"фаза «{faza}» называет гейтом `{imya}`, а такого "
                                          f"инструмента НЕТ в реестре §5 — отсюда и пришла "
                                          f"ложь про гейт вмещения"))
                    continue
                if len(kandidaty) > 1:
                    krasnye.append(("И4", f"фаза «{faza}» называет гейтом `{imya}`, а в реестре "
                                          f"таких путей {len(kandidaty)} — имя неоднозначно"))
                    continue
                put = kandidaty[0]
                if not (REPO / put).is_file():
                    krasnye.append(("И4", f"фаза «{faza}» называет гейтом `{imya}`, реестр даёт "
                                          f"путь `{put}`, а файла на диске НЕТ"))
                elif otkaz is None and put in bez and \
                        not obyavlennaya_pustota(po_puti[put]["zovut"]):
                    krasnye.append(("И4", f"фаза «{faza}» называет гейтом `{imya}`, файл есть, "
                                          f"но его НИКТО НЕ ЗОВЁТ — написанный и не вызываемый "
                                          f"гейт зелен ровно потому, что его не звали"))
    return krasnye, obyavleno, stroki, na_diske


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Гейт согласованности карты: реестр инструментов §5 против диска. "
                    "Четыре инварианта, каждый краснеет отдельно и называет виновника.")
    ap.add_argument("--karta", default=None,
                    help=f"путь к карте (по умолчанию {KARTA_REL})")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="печатать согласованные строки поимённо")
    a = ap.parse_args(argv)

    put_karty = Path(a.karta) if a.karta else (REPO / KARTA_REL)
    if not put_karty.is_absolute():
        put_karty = (REPO / put_karty)
    try:
        text = put_karty.read_text(encoding="utf-8")
    except OSError as e:
        print(f"❌ карта `{put_karty}` не читается ({e.__class__.__name__})")
        return 1

    krasnye, obyavleno, stroki, na_diske = sudit(text)

    if a.verbose:
        for s in stroki:
            print(f"   ✅ {s['put']} · {s['status']}")

    for kod, soobshch in krasnye:
        print(f"❌ {kod}: {soobshch}")

    print("\n═══ ОХВАТ И ОБЪЯВЛЕННЫЕ ДЫРЫ — печать всегда, не гейт ═══")
    print(f"   строк реестра: {len(stroki)} · инструментов на диске: {len(na_diske)}")
    print(f"   карта: {put_karty}")
    if obyavleno:
        print(f"   объявленных пустот (законные, с причиной): {len(obyavleno)}")
        for o in obyavleno:
            print(f"     · {o}")
    else:
        print("   объявленных пустот нет")
    print("   структурно НЕ проверяется:")
    print("     · колонка «фаза / роль» — машинного ответа у неё нет вовсе")
    print("     · «кто зовёт» стоит на текстовой эвристике check_tool_contract: "
          "`import korpus` (имя модуля без .py) она не видит, а упоминание в "
          "докстринге считает вызовом")
    print("     · .py внутри " + ", ".join(VNE_OHVATA) + " в охват И1 не входят")
    print("     · файлы старого конвейера (`🗄 АРХИВ`) не читаются вовсе")

    if krasnye:
        print(f"\n❌ ГЕЙТ СОГЛАСОВАННОСТИ: красных {len(krasnye)}. "
              f"Реестр и дерево разъехались — правь ту сторону, которая врёт.")
        return 1
    print(f"\n✅ ГЕЙТ СОГЛАСОВАННОСТИ: реестр сходится с диском, "
          f"проверено {len(stroki)} из {len(stroki)} строк и "
          f"{len(na_diske)} из {len(na_diske)} инструментов "
          f"(объявленные дыры выше — они не зелёные).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
