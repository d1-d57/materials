#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ГЕЙТ ФОРМЫ ЛЕНТЫ — проверяет ДОКУМЕНТ, а не файл.

    python3 _generator/tools/check_lenta.py <лента.md>
    python3 _generator/tools/check_lenta.py <лента.md> --vid <view.html>
    python3 _generator/tools/check_lenta.py <лента.md> --edinic 13   # сверить с перечнем
    python3 _generator/tools/check_lenta.py <лента.md> --tiho        # только код возврата

Код возврата: 0 — чисто, 1 — есть нарушения. Годится в ворота.

ЗАЧЕМ. Гейт `G7` проверяет ФАЙЛ: есть ли лента, свежий ли `view.html`, покрыт ли `slide_order`,
стоит ли строка раскладки. Ни один его пункт не смотрит на СОДЕРЖИМОЕ. Цена этого зазора снята
командой по картотеке фабрики (`_studio/zhurnal/2026-08-05_faza-lenty/klassy_otkazov.py`):
на фазе ленты 445 записей кратности в 16 классах отказов, из них 149 (33 %) — без единого рычага,
и ещё 239 (54 %) держатся на прозе `DOK.md`, то есть на том, что исполнитель её прочитает и
вспомнит. По собственному закону репозитория запись правила в канон не лечит.

Каждый пункт ниже привязан к классу отказа. Спецификация, откуда взяты требования, —
`_studio/konvejer/06-tekst/FORMA.md`; живой образец, на котором гейт обязан быть зелёным, —
`_studio/konvejer/06-tekst/ETALON.md`.

🔴 ПОРЯДОК ПРОГОНА, а не пожелание: СНАЧАЛА на эталоне, потом на работе. Красное на эталоне =
ложный гейт, а не больной эталон; чинится гейт. Гейт, краснеющий на здоровом документе, обходят
`--no-verify`, и тогда пропадает вся защита, а не одна проверка (`_studio/konvejer/GEJTY.md`).

Идиома семьи (`_generator/DVIZHKI.md`): stdlib, детерминизм, без сети и pip, `exit 1` при красном.
"""
import html as _html
import importlib.util
import os
import re
import sys
from pathlib import Path

# ───────────────────────── что проверяем и какой класс отказа этим закрываем ─────────────────────────
# Классы — из `klassy_otkazov.py` (разнос живой картотеки по фазе ленты, Σ кратности 445).
PUNKTY = {
    "L1":  ("фронтматтер ленты полон, `nomera: da` стоит",                    "J · носителя нет"),
    "L2":  ("словарь обозначений есть до первой единицы",                     "C · математика и статус"),
    "L3":  ("у каждой врезки есть `Статус:`",                                 "C · математика и статус"),
    "L4":  ("у каждого утверждения есть кат-доказательство либо «объявляем»",  "C · математика и статус"),
    "L5":  ("«Зачем и что дальше» у каждой единицы, кроме последней",          "D · мотивировка и порядок"),
    "L6":  ("нумерация врезок сквозная, без пропусков и дублей, имя в скобках", "C · математика и статус"),
    "L7":  ("раздел-единица помечен `· ~N мин`; число единиц сходится",        "A · единица и бюджет"),
    "L8":  ("нет двух единиц с одинаковым заголовком",                        "H · повтор и потеря"),
    "L9":  ("термин не работает раньше своего определения (`check_termin`)",   "C · математика и статус"),
    "L10": ("в собранном виде ноль склеек `<p>- пункт - пункт</p>`",           "J · носителя нет"),
    "L11": ("у каждой `<figure>` есть `<svg>` и `<figcaption>`; классы `s-*` движку известны", "G · иллюстрации"),
    "L12": ("ПОСТРОЧНАЯ сверка источник ↔ вид, не только хвост блока",         "J · носителя нет"),
    "L13": ("у каждого `<svg>` есть PNG-рендер не старше источника",           "G · иллюстрации"),
}

# 🔴 СЛЕПАЯ ЗОНА ПЕЧАТАЕТСЯ ВСЕГДА, а не только когда красно: зелёный чекер с необъявленной
# слепой зоной опаснее красного — ему верят. Список закрыт: что здесь не названо, то проверяется.
NE_PROVERYAEM = [
    ("C · математика и статус", "ВЕРНОСТЬ математики. Ни одна проверка ниже не смотрит, правда ли "
                                "написанное. `Статус: выверено` — это КТО, а не СИЛА."),
    ("F · два адресата", "что именно ушло на поле лектору, а что осталось залу. Машинно "
                         "различимо только НАЛИЧИЕ `> поле:mn`, а не уместность содержимого."),
    ("B · плотность", "пол плотности. Потолок объявлен каноном, пола нет ни в каноне, ни здесь."),
    ("M · раскладка", "строка `поле:mn **Раскладка.**` — её уже проверяет `G7` в `sostoyanie.py`; "
                      "дублировать значит завести два хозяина у одного правила."),
    ("C · словарь обозначений", "СОВПАДЕНИЕ обозначений по документу (L2 проверяет только наличие "
                                "словаря): без списка синонимов это грепом не решается."),
    ("—", "понятность текста. Самопроверка автора даёт ноль, потому что автор достраивает из "
           "головы; ловится только читателем, не видевшим источника."),
]

VREZKA_RE = re.compile(
    r"^\*\*(Определение|Теорема|Лемма|Предложение|Утверждение|Пример|Задача|Замечание)"
    r"(?:\s+(\S+?))?\s*(\([^)]*\))?\s*\.?\s*(Статус\s*:[^*]*?)?\*\*", re.M)
UTV_TIPY = ("Теорема", "Лемма", "Предложение", "Утверждение")
KAT_RE = re.compile(r"^\*(Доказательство|Логика|Идея|Решение)[^*]*\*", re.M)
EDINICA_RE = re.compile(r"^##\s+(.*?)\s*·\s*~\s*\d+\s*мин\s*$", re.M)
RAZDEL_RE = re.compile(r"^##\s+(.*)$", re.M)
FIGURE_RE = re.compile(r"<figure\b.*?</figure>", re.S | re.I)
SVG_RE = re.compile(r"<svg\b.*?</svg>", re.S | re.I)
SKLEJKA_RE = re.compile(r"<p>\s*[-–—•]\s")
STATUS_V_METKE = re.compile(r"\.?\s*Статус\s*:[^*]*?\.\*\*")
# Зачин ката движок печатает подписью кнопки: строчными и без хвостовой точки
# (`proof_details`: `kw.lower() + " — " + tail.strip(" .—-")`). Приводим ИСТОЧНИК к той же форме,
# иначе построчная сверка краснеет на здоровом документе — ровно та ошибка, за которую `GEJTY.md`
# уже заплатил «12 ложных ❌ из 14».
KAT_ZACHIN = re.compile(r"^\*(Доказательство|Логика|Идея|Решение)([^*]*)\*")
# Без `nomera: da` движок СРЕЗАЕТ номер из отображаемой метки. Это настройка, а не потеря текста,
# и путать их нельзя: иначе построчная сверка выдаёт по замечанию на каждую врезку и прячет
# настоящую съеденную строку в шуме. Отсутствие флага — отдельное замечание L1, ровно одно.
METKA_S_NOMEROM = re.compile(
    r"^\*\*(Определение|Теорема|Лемма|Предложение|Утверждение|Пример|Задача|Замечание)\s+\S+?(\s*\()")


def kak_v_vide(ln, nomera=True):
    """Строка источника → та же строка, какой её напечатает движок."""
    ln = STATUS_V_METKE.sub(".**", ln)
    m = KAT_ZACHIN.match(ln)
    if m:
        hvost = m.group(2).strip(" .—-")
        podpis = m.group(1).lower() + (" — " + hvost if hvost else "")
        return podpis + ln[m.end():]
    if not nomera:
        ln = METKA_S_NOMEROM.sub(r"**\1\2", ln)
    return ln
# строки источника, которые в вид не идут по устройству движка либо сами являются разметкой
PROPUSK_BLOKA = ("---", "#", ">", "🖼", "<", "|", "```", "tab:", "status:", "poryadok:",
                 "registr:", "nomera:", "format:")


def norm(s):
    """Нормализация ОБЕИХ сторон сверки: снять разметку, маркеры, сущности и все пробелы."""
    s = _html.unescape(s)
    s = re.sub(r"^[-*+]\s+", "", s, flags=re.M)
    s = re.sub(r"[*_`$\\]", "", s)
    return re.sub(r"\s+", "", s)


def najti_vid(src, yavno):
    """Где лежит собранный вид. Порядок: явный `--vid` → соседний `view.html` →
    `<стем>-vid/view.html` → `<стем>/view.html`. Не найден — HTML-проверки честно снимаются."""
    if yavno:
        p = Path(yavno)
        return p if p.is_file() else None
    for kand in (src.parent / "view.html",
                 src.parent / (src.stem + "-vid") / "view.html",
                 src.parent / src.stem / "view.html"):
        if kand.is_file():
            return kand
    return None


def klassy_dvizhka():
    """Множество классов `s-*`, которые движок-носитель действительно определяет."""
    dv = Path(__file__).resolve().parent.parent / "build_doc.py"
    if not dv.is_file():
        return None
    return set(re.findall(r"\.(s-[a-z0-9-]+)", dv.read_text(encoding="utf-8")))


def termin_gejt(put):
    """Переиспользуем `check_termin.py`, а не переписываем его: у него своя цена и свои фикстуры."""
    p = Path(__file__).resolve().parent / "check_termin.py"
    if not p.is_file():
        return None, "check_termin.py рядом не найден"
    spec = importlib.util.spec_from_file_location("check_termin", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    bad = mod.proverit_text(Path(put).read_text(encoding="utf-8"), Path(put).name)
    return bad, None


def bloki(text):
    return [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]


def proverit(put, vid_put=None, edinic=None):
    src = Path(put)
    if not src.is_file():
        return None, [("ВХОД", "нет файла: %s" % put)], {}, []
    text = src.read_text(encoding="utf-8")

    # ── Y считается ДО работы и ПО ИСТОЧНИКУ ──
    # Объект = то, что гейт способен просудить поштучно: единица выхода, врезка, иллюстрация.
    edinicy = EDINICA_RE.findall(text)
    razdely = RAZDEL_RE.findall(text)
    vrezki = [(m.group(1), m.group(2), m.group(3), m.group(4), m.start())
              for m in VREZKA_RE.finditer(text)]
    figury = FIGURE_RE.findall(text)
    Y = len(edinicy) + len(vrezki) + len(figury)

    bedy, sdelano, prosuzheno = [], set(), set()

    def krasnyj(pid, chto):
        bedy.append((pid, chto))

    # ── L1 · фронтматтер ──
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    nomera_da = bool(fm and re.search(r"^nomera\s*:\s*(da|да|1|yes|true)\s*$", fm.group(1), re.M))
    sdelano.add("L1")
    if not fm:
        krasnyj("L1", "фронтматтера нет вовсе — движок не соберёт вкладку")
    else:
        head = fm.group(1)
        for pole in ("tab", "status", "poryadok"):
            if not re.search(r"^%s\s*:\s*\S" % pole, head, re.M):
                krasnyj("L1", "во фронтматтере нет непустого `%s:`" % pole)
        if not re.search(r"^nomera\s*:\s*(da|да|1|yes|true)\s*$", head, re.M):
            krasnyj("L1", "нет `nomera: da` — движок срежет номер из метки врезки, "
                          "и короткая врезка покраснеет в check_view (FORMA §3.1)")

    # ── L2 · словарь обозначений ──
    sdelano.add("L2")
    do_pervoj = text.split("\n## ", 1)[0] if "\n## " in text else text
    pervaya_edinica = EDINICA_RE.search(text)
    do_edinicy = text[:pervaya_edinica.start()] if pervaya_edinica else text
    if not re.search(r"словар", do_edinicy, re.I) or not re.search(r"^\|[ :|-]+\|$", do_edinicy, re.M):
        krasnyj("L2", "до первой единицы нет словаря обозначений таблицей "
                      "(«одно понятие — одно обозначение», FORMA §3.2)")

    # ── L3 · Статус в метке · L4 · кат или «объявляем» · L6 · нумерация ──
    sdelano.update(("L3", "L4", "L6"))
    nomera, bez_imeni = [], 0
    blks = bloki(text)
    for i, (tip, nom, imya, status, poz) in enumerate(vrezki):
        prosuzheno.add(("врезка", poz))
        metka = "%s %s" % (tip, nom or "—")
        if not status:
            krasnyj("L3", "врезка «%s» без `Статус:` в метке" % metka)
        if not imya:
            bez_imeni += 1
        if nom and re.fullmatch(r"\d+", nom.strip()):
            nomera.append(int(nom))
        elif nom:
            krasnyj("L6", "врезка «%s»: номер не сквозной. Лента нумеруется одним рядом "
                          "1..N — иначе check_termin.py врезку не видит (FORMA §3.3)" % metka)
        else:
            krasnyj("L6", "врезка «%s» без номера" % metka)
        if tip in UTV_TIPY:
            hvost = text[poz:vrezki[i + 1][4]] if i + 1 < len(vrezki) else text[poz:]
            obyavl = bool(status and re.search(r"объявляем", status, re.I))
            # Доказательство живёт либо под катом (один блок), либо в потоке шагами — второе
            # не прихоть: движок прячет под кат ровно ОДИН блок, а разбор по шагам это блоки
            # (`FORMA.md §3.4`, п. 3). Машинный признак разбора в потоке — `**Шаг 1`.
            v_potoke = bool(re.search(r"^\*\*Шаг\s*1\b", hvost, re.M))
            if not obyavl and not KAT_RE.search(hvost) and not v_potoke:
                krasnyj("L4", "утверждение «%s» без доказательства: нет ни ката "
                              "`*Доказательство…*`, ни разбора в потоке с `**Шаг 1`, "
                              "ни ярлыка «объявляем»" % metka)
    if bez_imeni:
        krasnyj("L6", "врезок без имени в скобках: %d — check_termin.py их не увидит "
                      "(регулярка требует `N (имя)`)" % bez_imeni)
    if nomera and sorted(nomera) != list(range(1, len(nomera) + 1)):
        propushcheno = sorted(set(range(1, max(nomera) + 1)) - set(nomera))
        dubli = sorted({n for n in nomera if nomera.count(n) > 1})
        krasnyj("L6", "нумерация врезок не сквозная: пропущены %s, задвоены %s"
                      % (propushcheno or "—", dubli or "—"))

    # ── L5 · «Зачем и что дальше» ──
    sdelano.add("L5")
    kuski = re.split(r"^##\s+", text, flags=re.M)[1:]
    edinic_kuski = [k for k in kuski if EDINICA_RE.match("## " + k.split("\n", 1)[0])]
    for j, k in enumerate(edinic_kuski):
        zag = k.split("\n", 1)[0].strip()
        prosuzheno.add(("единица", zag))
        if j == len(edinic_kuski) - 1:
            continue
        if "Зачем и что дальше" not in k:
            krasnyj("L5", "единица «%s» без строки «Зачем и что дальше»" % zag[:60])

    # ── L7 · единица помечена временем; число сходится ──
    sdelano.add("L7")
    sluzhebnye = len(razdely) - len(edinicy)
    if not edinicy:
        krasnyj("L7", "ни один раздел не помечен `· ~N мин` — единиц выхода не опознать "
                      "(FORMA §3.10)")
    # Служебный раздел (словарь, охват) законен только ДО первой единицы — там шапка ленты.
    # Раздел без `· ~N мин` ПОСЛЕ первой единицы — это единица, потерявшая свою метку времени,
    # и она молча выпадает из счёта. Молчаливое выпадение хуже красного: охват перестаёт сходиться
    # с перечнем, а гейт печатает зелёное.
    if pervaya_edinica:
        for m in RAZDEL_RE.finditer(text):
            if m.start() > pervaya_edinica.start() and not EDINICA_RE.match(m.group(0)):
                krasnyj("L7", "раздел «%s» стоит среди единиц, но не помечен `· ~N мин` — "
                              "он молча выпадает из счёта единиц" % m.group(1).strip()[:60])
    if edinic is not None and len(edinicy) != edinic:
        krasnyj("L7", "единиц в ленте %d, в перечне %d — расхождение чинится в перечне, "
                      "а не «примерно по смыслу»" % (len(edinicy), edinic))

    # ── L8 · повтор заголовка ──
    sdelano.add("L8")
    vidno = {}
    for z in edinicy:
        klyuch = norm(z).lower()
        if klyuch in vidno:
            krasnyj("L8", "две единицы с одинаковым заголовком: «%s»" % z[:60])
        vidno[klyuch] = True

    # ── L9 · термин не раньше определения ──
    sdelano.add("L9")
    bad_t, err_t = termin_gejt(put)
    if err_t:
        bedy.append(("L9", err_t))
    else:
        for imya, stroka, num, termin, gde in bad_t:
            krasnyj("L9", "%s:%d — «%s» (определение %d) работает раньше, во врезке %d"
                          % (imya, stroka, termin, num, gde))

    # ── HTML-часть: L10, L11, L12, L13 ──
    vid = najti_vid(src, vid_put)
    snyato = []
    if vid is None:
        snyato.append("L10, L11, L12 — собранного вида рядом нет. Собери: "
                      "`python3 _generator/build_doc.py <папка>` и повтори")
    else:
        plain_raw = re.sub(r"<[^>]+>", " ", vid.read_text(encoding="utf-8"))
        plain = norm(plain_raw)
        html_text = vid.read_text(encoding="utf-8")

        # L10 · склейки списка
        sdelano.add("L10")
        n_skl = len(SKLEJKA_RE.findall(html_text))
        if n_skl:
            krasnyj("L10", "склеек списка в абзац: %d — пункт списка потерял свой `<li>`" % n_skl)

        # L11 · фигуры
        sdelano.add("L11")
        izvestnye = klassy_dvizhka()
        for nf, f in enumerate(figury):
            prosuzheno.add(("фигура", nf))
            if not SVG_RE.search(f):
                krasnyj("L11", "`<figure>` без живого `<svg>` — иллюстрация обещана, "
                               "а не сделана: %s" % norm(f)[:50])
            if "<figcaption" not in f:
                krasnyj("L11", "`<figure>` без `<figcaption>` — не сказано, что рисунок "
                               "доказывает: %s" % norm(f)[:50])
            if izvestnye is not None:
                for cls in set(re.findall(r'class="([^"]*)"', f)):
                    for c in cls.split():
                        if c.startswith("s-") and c not in izvestnye:
                            krasnyj("L11", "класс `%s` движку-носителю неизвестен" % c)
        if izvestnye is None:
            snyato.append("L11 (часть про классы `s-*`) — рядом нет `build_doc.py`")

        # L12 · ПОСТРОЧНАЯ сверка, не только хвост
        sdelano.add("L12")
        propalo = 0
        hidden = False
        for blk in bloki(text):
            pervaya = blk.split("\n", 1)[0]
            if pervaya.startswith("## "):
                hidden = "{скрыть}" in pervaya
            if hidden or "⚑" in blk or "Флаг закрыт" in blk:
                continue
            if blk.startswith(PROPUSK_BLOKA):
                continue
            for ln in blk.split("\n"):
                ln = ln.strip()
                if not ln or ln.startswith(PROPUSK_BLOKA):
                    continue
                kus = norm(kak_v_vide(ln, nomera_da))
                if len(kus) > 12 and kus not in plain:
                    propalo += 1
                    if propalo <= 8:
                        krasnyj("L12", "строка источника не доехала до вида: …%s" % kus[-45:])
        if propalo > 8:
            krasnyj("L12", "…и ещё %d таких строк" % (propalo - 8))

        # L13 · PNG-рендер
        sdelano.add("L13")
        svgs = SVG_RE.findall(text)
        if svgs:
            pngdir = src.parent / (src.stem + "-png")
            mtime_src = src.stat().st_mtime
            if not pngdir.is_dir():
                krasnyj("L13", "нет папки `%s/` с PNG-рендерами %d рисунк(а/ов). Картинка, "
                               "которую не смотрели, негодна в четырёх случаях из пяти — "
                               "отрисуй: `rsvg-convert -w 900 …`" % (pngdir.name, len(svgs)))
            else:
                pngs = sorted(pngdir.glob("*.png"))
                if len(pngs) < len(svgs):
                    krasnyj("L13", "PNG-рендеров %d, а `<svg>` в источнике %d"
                                   % (len(pngs), len(svgs)))
                stary = [p.name for p in pngs if p.stat().st_mtime < mtime_src]
                if stary:
                    krasnyj("L13", "PNG старше источника (рисунок правили после рендера): %s"
                                   % ", ".join(stary[:5]))

    X = len(prosuzheno)
    svodka = {"Y": Y, "X": X, "edinic": len(edinicy), "sluzhebnyh": sluzhebnye,
              "vrezok": len(vrezki), "figur": len(figury), "vid": str(vid) if vid else None,
              "punktov": len(sdelano)}
    return svodka, bedy, {"snyato": snyato}, sorted(sdelano)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    tiho = "--tiho" in sys.argv
    vid_put = None
    edinic = None
    for i, a in enumerate(sys.argv):
        if a == "--vid" and i + 1 < len(sys.argv):
            vid_put = sys.argv[i + 1]
        if a == "--edinic" and i + 1 < len(sys.argv):
            edinic = int(sys.argv[i + 1])
    if not args:
        print(__doc__.strip().splitlines()[2])
        sys.exit(2)

    svodka, bedy, extra, sdelano = proverit(args[0], vid_put, edinic)
    if svodka is None:
        if not tiho:
            for k, v in bedy:
                print("  ✗ %s: %s" % (k, v))
        sys.exit(1)

    if not tiho:
        print("── ГЕЙТ ФОРМЫ ЛЕНТЫ (check_lenta) ──")
        print("  %s" % args[0])
        print("  проверено %d из %d объектов источника "
              "(единиц %d + врезок %d + иллюстраций %d; служебных разделов %d вне счёта)"
              % (svodka["X"], svodka["Y"], svodka["edinic"], svodka["vrezok"],
                 svodka["figur"], svodka["sluzhebnyh"]))
        print("  пунктов гейта отработало: %d из %d — %s"
              % (svodka["punktov"], len(PUNKTY), ", ".join(sdelano)))
        print("  собранный вид: %s" % (svodka["vid"] or "НЕ НАЙДЕН"))

        # 🔴 слепая зона печатается ВСЕГДА, а не только когда красно
        print("\n  ЧЕГО ЭТОТ ГЕЙТ НЕ ПРОВЕРЯЕТ — список закрытый:")
        for klass, chto in NE_PROVERYAEM:
            print("     · [%s] %s" % (klass, chto))
        for s in extra["snyato"]:
            print("     · СНЯТО В ЭТОМ ПРОГОНЕ: %s" % s)

    # X = 0 при непустом источнике — КРАСНЫЙ, а не зелёный.
    # Цена 16.07: «проверено 0 уроков из 14» прочиталось как зелёный верификатор.
    if svodka["Y"] > 0 and svodka["X"] == 0:
        if not tiho:
            print("\n  ✗ КРАСНЫЙ: просужено 0 объектов из %d — гейт не увидел ленту, "
                  "а не лента чиста" % svodka["Y"])
        sys.exit(1)

    if bedy:
        if not tiho:
            print("\n  ✗ КРАСНЫЙ — замечаний %d:" % len(bedy))
            for k, v in bedy:
                print("     %-4s %s" % (k, v))
            print("\n  расшифровка пунктов:")
            for k in sorted({k for k, _ in bedy}):
                chto, klass = PUNKTY.get(k, ("—", "—"))
                print("     %-4s %s  [класс отказа %s]" % (k, chto, klass))
        sys.exit(1)

    if not tiho:
        print("\n  ✓ ЗЕЛЁНЫЙ: все %d пунктов формы выполнены" % len(sdelano))
    sys.exit(0)


if __name__ == "__main__":
    main()
