#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Трекер состояния лекции по реестру гейтов (_studio/konvejer/GEJTY.md).

    python3 sostoyanie.py <папка-лекции>

Read-only: ничего в папке лекции не меняет. По каждому гейту/хуку GEJTY.md
считает PASS/FAIL/WARN/N-A по «признаку-на-диске», печатает таблицу,
вычисляет ⏺ ТЫ ЗДЕСЬ (первый жёсткий гейт не-PASS) и сверяет журнал
(<лекция>/dnevnik/zhurnal.md, см. ZHURNAL.md) с диском — молчаливый недобор:
строка журнала говорит PASS, а сам гейт на диске FAIL.

Число записей руками не выписываем (KONSTITUCIYA §10) — оно считается по файлу:
    grep -c '^### G' _studio/konvejer/GEJTY.md
    grep -c '^### H' _studio/konvejer/GEJTY.md
Реестр гейтов (GEJTY.md) — проза, не машиночитаема; поэтому каждая запись
закодирована здесь как структура Python с одной check-функцией на гейт.
Функции пишут в терминах grep/regex — буквально то, что называет
«признак-на-диске» в GEJTY.md; где признак неоднозначен — проверка ослаблена
до WARN/advisory с пометкой (см. kod_treker.md #ВОПРОСЫ).

⚠ Калибровка (27.07.2026, заход `kod_gejty-shaga-6.md`). Там, где буква
GEJTY.md красит здоровый дек, реализовано не буквально, и КАЖДОЕ отступление
названо у своей функции числом ложных ❌, которое буква давала на живых деках.
Причина не в удобстве: гейт, краснеющий на здоровом деке, обходят через
--no-verify — и пропадает вся защита, а не одна проверка.

Гейты src/-слоя (G6, G10, линтер-часть G11) переиспользуют функции
_generator/build_deck.py импортом — не копируют логику линтера.

stdlib only.
"""
import argparse
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
GENERATOR_DIR = TOOLS_DIR.parent
sys.path.insert(0, str(GENERATOR_DIR))
import build_deck as bd  # noqa: E402  (импорт после sys.path — переиспользуем линтер, не дублируем)

BUILD_DECK_PY = GENERATOR_DIR / "build_deck.py"

PASS, FAIL, WARN, NA, BROWSER = "PASS", "FAIL", "WARN", "N/A", "[браузерный]"
HARD_STATUSES = (PASS, FAIL)  # статусы, которые считаются «жёстко посчитанными» для ты-здесь


class GateResult:
    __slots__ = ("status", "detail", "touched", "extra_warns")

    def __init__(self, status, detail="", touched=False, extra_warns=None):
        self.status = status
        self.detail = detail
        self.touched = touched
        self.extra_warns = extra_warns or []


# ───────────────────────── общие разборщики ─────────────────────────

def read(path):
    return path.read_text(encoding="utf-8") if path.is_file() else None


def slugify(heading):
    h = heading.strip().lstrip("#").strip().lower()
    h = "".join(c for c in unicodedata.normalize("NFKD", h) if not unicodedata.combining(c))
    h = re.sub(r"[^\w\s-]", "", h, flags=re.UNICODE)
    return re.sub(r"[\s_]+", "-", h).strip("-")


def flag_balance(text):
    """(открыто_на_выходе, всего_флагов) построчным сканированием ⚑ Флаг / Флаг закрыт:."""
    open_n = total = 0
    for line in text.splitlines():
        if "⚑ Флаг" in line:
            open_n += 1
            total += 1
        if "Флаг закрыт" in line:
            open_n -= 1
    return open_n, total


CARD_ID_RE = re.compile(r"^id:\s*(\S+)", re.M)
ROD_OK = {"находка", "утверждение", "биекция", "мостик"}


def parse_cards(text):
    """Блок карточки = от строки `id:` до следующей `id:` (или конца файла).
    Поля названы в GEJTY.md буквально: id:/род:/источник:/связи:[...]/статус:.
    Формат карточки (STANDART-uzla.md) этим заходом не читан — см. ВОПРОСЫ."""
    idxs = [m.start() for m in CARD_ID_RE.finditer(text)] + [len(text)]
    cards = []
    for i in range(len(idxs) - 1):
        block = text[idxs[i]:idxs[i + 1]]
        cid = CARD_ID_RE.match(block).group(1)
        rod = re.search(r"^род:\s*(\S+)", block, re.M)
        istochnik = re.search(r"^источник:\s*(.+)$", block, re.M)
        svyazi = re.search(r"^связи:\s*\[(.*?)\]", block, re.M)
        status = re.search(r"^статус:\s*(.+)$", block, re.M)
        cards.append(dict(
            id=cid,
            rod=rod.group(1) if rod else None,
            istochnik=istochnik.group(1).strip() if istochnik else None,
            svyazi=[s.strip() for s in svyazi.group(1).split(",") if s.strip()] if svyazi else [],
            status=status.group(1).strip() if status else None,
        ))
    return cards


# ───────────────────────── Фаза I: G1-G4 ─────────────────────────

FIELD_RE = re.compile(r"^\s*(\d)\.\s*(.+\S)\s*$", re.M)
SLIDES_CANON = {"да": "да", "нет": "нет", "yes": "да", "no": "нет"}


def check_g1(lek, ctx):
    p = lek / "brief.md"
    text = read(p)
    if text is None:
        return GateResult(FAIL, "нет brief.md")
    fields = {int(m.group(1)): m.group(2) for m in FIELD_RE.finditer(text) if m.group(1) in "123456789"}
    missing = [n for n in range(1, 10) if n not in fields]
    placeholder = [n for n in fields if n not in missing and ("<...>" in fields[n] or "<выбрать>" in fields[n])]
    filled_any = any(n not in missing and n not in placeholder for n in range(1, 10))

    budget_ok, budget_detail = True, ""
    if 3 in fields and 3 not in placeholder:
        m = re.search(r"бюджет\s*слайдов:\s*(\S+)", fields[3], re.I)
        if not m or not re.fullmatch(r"\d+", m.group(1)):
            budget_ok = False
            budget_detail = "поле 3: «бюджет слайдов» не целое число"

    slides_flag = None
    slides_raw_mismatch = False
    if 9 in fields and 9 not in placeholder:
        raw = fields[9]
        v = raw[raw.rfind(":") + 1:].strip().lower() if ":" in raw else raw.strip().lower()
        if v in SLIDES_CANON:
            slides_flag = SLIDES_CANON[v]
            if v in ("yes", "no"):
                slides_raw_mismatch = True
    ctx["slides_flag"] = slides_flag

    bad = list(missing) + list(placeholder)
    detail = []
    if missing:
        detail.append("нет полей №%s" % missing)
    if placeholder:
        detail.append("плейсхолдер не убран в №%s" % placeholder)
    if not budget_ok:
        detail.append(budget_detail)
    if slides_flag is None:
        detail.append("поле 9 (слайды) не да|нет")
    ok = not bad and budget_ok and slides_flag is not None
    status = PASS if ok else FAIL
    extra = ["арифметика «бюджет кратен длительности/2» не проверена жёстко — "
             "точная формула не задана в GEJTY.md (advisory, см. ВОПРОСЫ)"]
    if slides_raw_mismatch:
        extra.append("поле 9 записано yes/no (bootstrap_lekcia.py), контракт ждёт да/нет — принято как синоним")
    return GateResult(status, "; ".join(detail) or "9/9 полей заполнены", filled_any, extra)


def check_g2(lek, ctx):
    p = lek / "kartoteka" / "KARTA-OBLASTI.md"
    text = read(p)
    if text is None:
        return GateResult(FAIL, "нет kartoteka/KARTA-OBLASTI.md")
    cards = [c for c in parse_cards(text) if c["rod"] in ROD_OK]
    no_source = [c["id"] for c in cards if not c["istochnik"]]
    unique_sources = {c["istochnik"] for c in cards if c["istochnik"]}
    ok = not no_source and len(unique_sources) >= 5
    detail = []
    if no_source:
        detail.append("без источника: %s" % no_source)
    if len(unique_sources) < 5:
        detail.append("уникальных источников %d < 5" % len(unique_sources))
    status = PASS if ok else FAIL
    has_razvorot_signal = any(c["status"] == "на-сверку" for c in cards)
    extra = []
    if not has_razvorot_signal:
        extra.append("автор-чекпоинт: не найден статус:на-сверку — честность разворота «но» сверить вручную")
    return GateResult(status, "; ".join(detail) or "%d карточек, %d источников" % (len(cards), len(unique_sources)),
                       bool(cards), extra)


LEVEL_BLOCK_RE = re.compile(r"^(Утверждение|Определение|Лемма|Следствие|Теорема)\b", re.M)


def check_g3(lek, ctx):
    p = lek / "kotly" / "matematika.md"
    text = read(p)
    if text is None:
        return GateResult(FAIL, "нет kotly/matematika.md")
    open_n, total_flags = flag_balance(text)
    lines = text.splitlines()
    blocks = list(LEVEL_BLOCK_RE.finditer(text))
    missing_level = []
    for m in blocks:
        start = text.count("\n", 0, m.start())
        window = lines[start:start + 6]
        if not any(re.search(r"^>.*уровень", l) for l in window):
            missing_level.append("%s@стр.%d" % (m.group(0), start + 1))
    ok = open_n == 0 and not missing_level
    detail = []
    if open_n:
        detail.append("непарных ⚑ Флаг: %d" % open_n)
    if missing_level:
        detail.append("без уровень-тега: %s" % missing_level[:5])
    status = PASS if ok else FAIL
    return GateResult(status, "; ".join(detail) or "0 непарных флагов (%d всего), уровни на месте" % total_flags,
                       bool(blocks) or total_flags > 0,
                       ["автор-чекпоинт: adversarial ре-ревью + единообразие нотации — не автоматизируется"])


def check_g4(lek, ctx):
    p = lek / "chernovik" / "rasskaz.md"
    text = read(p)
    if text is None:
        return GateResult(FAIL, "нет chernovik/rasskaz.md")
    open_n, total_flags = flag_balance(text)
    img_count = text.count("🖼")
    quotes = re.findall(r"\[skelet#([^\]]+)\]", text)
    skelet_text = read(lek / "kotly" / "matematika.md") or ""
    anchors = {slugify(h) for h in re.findall(r"^#{1,6}\s+(.+)$", skelet_text, re.M)}
    dangling = [q for q in quotes if q not in anchors]
    ok = open_n == 0 and not dangling
    detail = []
    if open_n:
        detail.append("непарных ⚑ Флаг: %d" % open_n)
    if dangling:
        detail.append("висячие цитаты-сноски: %s" % dangling)
    status = PASS if ok else FAIL
    touched = total_flags > 0 or img_count > 0 or bool(quotes)
    extra = [
        "🖼 (%d вхождений) не сверено с числом тактов нити — «список тактов» не найден среди читаных файлов" % img_count,
        "синтаксис skelet-якоря не задан явно в GEJTY.md — использован эвристический slug заголовков "
        "kotly/matematika.md, точность не гарантирована",
    ]
    return GateResult(status, "; ".join(detail) or "0 непарных флагов, %d 🖼, 0 висячих цитат" % img_count,
                       touched, extra)


# ───────────────────────── Фаза I→II: G5-G6 ─────────────────────────

def _load_src_brief(src):
    p = src / "brief.md"
    text = read(p)
    return bd.parse_brief(text) if text is not None else {}


def check_g5(lek, ctx):
    if ctx.get("slides_flag") == "нет":
        return GateResult(NA, "слайды: нет — доска")
    src = lek / "src"
    meta = _load_src_brief(src)
    if not meta:
        return GateResult(FAIL, "нет src/brief.md", touched=src.is_dir())
    order = meta.get("slide_order") or []
    slides_dir = src / "slides"
    present = {p.stem for p in slides_dir.glob("*.html")} if slides_dir.is_dir() else set()
    missing, extra_files = set(order) - present, present - set(order)
    register_ok = bool(meta.get("register"))
    budget_ok = bool(meta.get("word_budget_per_slide"))
    ok = bool(order) and not missing and not extra_files and register_ok and budget_ok
    detail = []
    if not order:
        detail.append("slide_order пуст")
    if missing:
        detail.append("нет файлов слайдов: %s" % sorted(missing))
    if extra_files:
        detail.append("слайды вне slide_order: %s" % sorted(extra_files))
    if not register_ok:
        detail.append("register: не задан")
    if not budget_ok:
        detail.append("word_budget_per_slide: не задан")
    status = PASS if ok else FAIL
    return GateResult(status, "; ".join(detail) or "slide_order покрывает slides/, register+budget заданы",
                       bool(order) or bool(present),
                       ["признак G5 в GEJTY.md указывает на src/, а PAPKA-LEKCII.md относит раскадровку к "
                        "отдельной Фазы-I папке raskadrovka/ — нестыковка заходов ①/②, реализовано дословно "
                        "по GEJTY.md (src/), см. ВОПРОСЫ"])


def check_g6(lek, ctx):
    if ctx.get("slides_flag") == "нет":
        return GateResult(NA, "слайды: нет — доска")
    src = lek / "src"
    core = ["shablon.html", "engine.js", "tokens.css"]
    missing_core = [f for f in core if not (src / f).is_file()]
    if not (src / "fonts").is_dir():
        missing_core.append("fonts/")
    if not src.is_dir():
        return GateResult(FAIL, "нет src/", touched=False)
    meta = _load_src_brief(src)
    need = ["id", "title", "canvas", "accent_tag", "slide_order"]
    missing_keys = [k for k in need if not meta.get(k)]
    canvas_ok = meta.get("canvas") == "1440x810"
    order = meta.get("slide_order") or []
    frame_missing = []
    for sid in order:
        sp = src / "slides" / (sid + ".html")
        stext = read(sp)
        if stext is None or '<section class="slide"' not in stext:
            frame_missing.append(sid)
    ill_missing = []
    for sp in (src / "slides").glob("*.html") if (src / "slides").is_dir() else []:
        stext = read(sp) or ""
        for name in re.findall(r'data-ill="([^"]+)"', stext):
            if not list((src / "illustrations").glob(name + ".*")):
                ill_missing.append(name)
    ok = not missing_core and not missing_keys and canvas_ok and not frame_missing and not ill_missing
    detail = []
    if missing_core:
        detail.append("нет: %s" % missing_core)
    if missing_keys:
        detail.append("brief.md без ключей: %s" % missing_keys)
    if not canvas_ok:
        detail.append("canvas != 1440x810 (%r)" % meta.get("canvas"))
    if frame_missing:
        detail.append("нет каркаса <section class=\"slide\"> у: %s" % frame_missing)
    if ill_missing:
        detail.append("нет файла иллюстрации под data-ill: %s" % ill_missing)
    status = PASS if ok else FAIL
    return GateResult(status, "; ".join(detail) or "канон-скелет + brief-ключи + каркасы + иллюстрации на месте",
                       bool(order) or bool(meta))


# ───────────── Фаза I, конец: G7 (предвёрсточный документ = лента) ─────────────
# Признак переписан 27.07.2026: шаг 6 переехал в Фазу I, его выход — лента
# <лекция>/raskadrovka/teksty/*.md + собранный view.html, а src/content/*.md стал
# ПОРОЖДАЕМЫМ слоем Фазы II (GEJTY.md §G7, 06-tekst/DOK.md, FORMAT-ISTOCHNIKA.md).

BUDGET_TOLERANCE = 0.25  # допуск бюджета слов числом в GEJTY.md не задан — назван здесь явно
# «Раскладка» распознаётся не дословно: `**Раскладка.**`, `**Раскладка:**`, `**Раскладка**.`
# — одно и то же для человека, и требовать одну форму значит краснеть на здоровой ленте.
RASKLADKA_RE = re.compile(r"^\s*>?\s*поле:\s*mn\s*\**\s*Раскладка", re.M)
TAB_FM_RE = re.compile(r"^tab\s*:\s*\S", re.M)
ACC_RE = re.compile(r"\*\*(.+?)\*\*", re.S)
FIGURE_RE = re.compile(r"<figure\b.*?</figure>", re.S | re.I)
SVG_RE = re.compile(r"<svg\b.*?</svg>", re.S | re.I)
FENCE_RE = re.compile(r"(?ms)^```.*?^```\s*$")
QUOTE_LINE_RE = re.compile(r"(?m)^\s*>.*$")
MATH_RE = re.compile(r"\$\$.*?\$\$|\$[^$\n]*\$", re.S)


def strip_shortcodes(text):
    """Снять шорткаты Р2, СОХРАНИВ их полезный текст (он живёт на слайде).

    Формулы снимаются ПЕРВЫМИ, и это не косметика: `}` внутри TeX иначе рвёт
    разбор — `{blur@2|$\\binom{2n}{n}$ путей}` схлопывается в мусор (build_deck.py
    обходит то же место приёмом stash→parse→unstash). Заодно снимается перекос
    счёта слов: `\\binom`/`\\quad` словами не являются."""
    text = MATH_RE.sub(" ", text)
    text = re.sub(r"\{fill@\d+\|([^|}]*)\|([^}]*)\}", r"\2", text)
    text = re.sub(r"\{blur@\d+\|([^}]*)\}", r"\1", text)
    text = re.sub(r"\{@[\d-]+[^|}]*\|([^}]*)\}", r"\1", text)
    return re.sub(r"\{[@.][^}]*\}", " ", text)


WORDLIKE_RE = re.compile(r"[^\W_]", re.UNICODE)


def count_words(text):
    """Слова, а не токены: одиночные `—`, `·`, `…`, `→` словами не считаются.

    Через `str.split()` разделитель-глиф идёт в счёт наравне со словом, и слайд с
    тремя пунктами через `·` получает +3 к объёму из ниоткуда. На пределе в 25
    слов этого хватает, чтобы покраснеть без единого лишнего слова."""
    return sum(1 for t in text.split() if WORDLIKE_RE.search(t))


MARK_RE = re.compile(r"\{(?:@|blur@|fill@)(\d+)")
RANGE_RE = re.compile(r"\{@(\d*)-(\d+)")


def marks_all(content_md):
    """Все номера сцен, упомянутые шорткатами, ВКЛЮЧАЯ диапазоны.

    `{@5-8}` и `{@-6}` — законные формы (build_deck.py._attrs_from_tag); брать из
    них только первое число значит проспать ровно урок 7 на верхней границе."""
    nums = {int(x) for x in MARK_RE.findall(content_md)}
    for lo, hi in RANGE_RE.findall(content_md):
        if lo:
            nums.add(int(lo))
        nums.add(int(hi))
    return nums


def marks_revealing(content_md):
    """Только «раскрывающая» сторона — ей и нужен каскад `.scene-N [data-scene-from]`.

    `{@-6}` (=`data-scene-until`) сюда НЕ входит: сокрытие делает JS классом
    `scene-off` (engine.js), правил `.scene-N` для него не существует ни в одном
    живом деке — требовать их значит краснеть на здоровой вёрстке."""
    nums = {int(x) for x in re.findall(r"\{(?:@|fill@)(\d+)", content_md)}
    for lo, _hi in RANGE_RE.findall(content_md):
        if lo:
            nums.add(int(lo))
    return nums


def lenta_files(lek):
    """(все *.md ленты, файлы без фронтматтера `tab:`) или None, если teksty/ нет вовсе.

    Файл без `tab:` НЕ выбрасывается молча: молчаливое исключение превращается в
    ложное обвинение «лента не покрывает деку» — виноват один опечатанный
    фронтматтер, а трекер показывает пальцем на всю ленту. Он считается, а про
    него говорится отдельной ⚠-строкой.
    Пустой список ≠ None: `raskadrovka/teksty/` заведена, но не наполнена — недобор,
    а отсутствие папки — «шаг 6 шёл по старой схеме» (bootstrap_lekcia.py заводит
    raskadrovka/ с .gitkeep, но teksty/ не создаёт)."""
    d = lek / "raskadrovka" / "teksty"
    if not d.is_dir():
        return None
    files = sorted(d.glob("*.md"))
    return files, [p.name for p in files if not TAB_FM_RE.search(read(p) or "")]


def lenta_sections(text):
    """[(заголовок, тело)] по `^## ` — раздел ленты = слайд (06-tekst/DOK.md).

    Кодовые заборы снимаются до разбиения: `## ` внутри ``` — не раздел, а строка
    примера, и фантомный раздел ломает сверку с длиной slide_order."""
    text = FENCE_RE.sub("\n", text)
    out = []
    heads = list(re.finditer(r"^## +(.+?)\s*$", text, re.M))
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        out.append((m.group(1), text[m.end():end]))
    return out


def _lenta_clean(body):
    """Тело раздела без того, что на слайд НЕ едет: <figure> с подписью, голый
    <svg>, боковые врезки `> поле:mn …` (снимается вся блок-цитата, а не первая
    её строка — многострочная врезка иначе уходит в счёт слов)."""
    return QUOTE_LINE_RE.sub(" ", SVG_RE.sub(" ", FIGURE_RE.sub(" ", body)))


def check_g7(lek, ctx):
    if ctx.get("slides_flag") == "нет":
        return GateResult(NA, "слайды: нет — доска")
    src = lek / "src"
    meta = _load_src_brief(src)
    order = meta.get("slide_order") or []
    found = lenta_files(lek)
    files, no_tab = (None, []) if found is None else found

    if files is None:
        extra = ["ленты нет: папка raskadrovka/teksty/ не заведена. bootstrap_lekcia.py создаёт "
                 "raskadrovka/ без teksty/, значит её появление — намеренный акт шага 6 по новой схеме"]
        if (src / "slides").is_dir() and list((src / "slides").glob("*.html")):
            extra.append("дек уже в Фазе II, а предвёрсточного документа нет — шаг 6 по новой схеме "
                         "не проходили (N/A не должен это прятать)")
        return GateResult(NA, "шаг 6 шёл по старой схеме (конвейер до 27.07.2026)", False, extra)
    if not files or len(no_tab) == len(files):
        return GateResult(FAIL, "raskadrovka/teksty/ заведена, но ни одного *.md с фронтматтером tab:", True)

    sections = []
    for p in files:
        sections.extend(lenta_sections(read(p) or ""))
    detail, extra = [], []
    if no_tab:
        extra.append("в ленте есть *.md без фронтматтера `tab:` — их разделы всё равно посчитаны, "
                     "но вид build_doc.py их не покажет: %s" % no_tab)

    view = lek / "raskadrovka" / "teksty" / "view.html"
    if not view.is_file():
        detail.append("нет teksty/view.html — лента не собрана build_doc.py")
    else:
        stale = [p.name for p in files if p.stat().st_mtime > view.stat().st_mtime]
        if stale:
            detail.append("view.html не пересобран, свежее его: %s" % stale)

    if not order:
        detail.append("src/brief.md без slide_order — покрытие не с чем сверить")
    elif len(sections) != len(order):
        detail.append("разделов ленты %d, а slide_order %d — лента не покрывает деку "
                      "(раздел = слайд, 06-tekst/DOK.md)" % (len(sections), len(order)))

    no_layout = [h for h, b in sections if not RASKLADKA_RE.search(b)]
    if no_layout:
        detail.append("без «поле:mn **Раскладка.**»: %s" % no_layout)

    budget_raw = meta.get("word_budget_per_slide")
    budget_n = int(budget_raw) if budget_raw and str(budget_raw).isdigit() else None
    if budget_n:
        limit = budget_n * (1 + BUDGET_TOLERANCE)
        over = []
        for h, b in sections:
            words = count_words(re.sub(r"<[^>]+>", " ", strip_shortcodes(_lenta_clean(b))))
            if words > limit:
                over.append("%s(%d)" % (h, words))
        if over:
            detail.append("сверх word_budget_per_slide=%d +%d%%: %s"
                          % (budget_n, round(BUDGET_TOLERANCE * 100), over))
    else:
        extra.append("word_budget_per_slide в src/brief.md не задан числом — объём разделов не судится")

    over_acc = [h for h, b in sections if len(ACC_RE.findall(_lenta_clean(b))) > 1]
    if over_acc:
        extra.append("эвристика «≤1 акцент-блок на раздел» (GEJTY сам помечает её эвристикой и не "
                     "включает в список жёстких пунктов поля «тип»): >1 `**…**` в %d разделах — %s"
                     % (len(over_acc), over_acc[:6]))
    extra.append("автор-чекпоинт: лента прочитана целиком, нарратив между слайдами не провисает — "
                 "вкус, механически не решается")

    status = FAIL if detail else PASS
    return GateResult(status, "; ".join(detail) or
                      "разделов ленты %d == slide_order, view.html свежий, раскладка везде" % len(sections),
                      True, extra)


# ───────────────────────── Фаза II: G8-G11 ─────────────────────────


def check_g8(lek, ctx):
    if ctx.get("slides_flag") == "нет":
        return GateResult(NA, "слайды: нет — доска")
    src = lek / "src"
    tokens_text = read(src / "tokens.css")
    if tokens_text is None:
        return GateResult(FAIL, "нет src/tokens.css")
    tbody_m = re.search(r"--t-body:\s*([\d.]+)px", tokens_text)
    tbody_val = float(tbody_m.group(1)) if tbody_m else None
    bad_hex = []
    for p in (src / "slides").glob("*.html") if (src / "slides").is_dir() else []:
        for h in re.findall(r"#[0-9a-fA-F]{3,6}\b", read(p) or ""):
            bad_hex.append("%s:%s" % (p.name, h))
    small_tbody = []
    candidates = list((src / "slides").glob("*.html")) if (src / "slides").is_dir() else []
    if (src / "shablon.html").is_file():
        candidates.append(src / "shablon.html")
    if tbody_val is not None:
        for p in candidates:
            for m in re.finditer(r"--t-body:\s*([\d.]+)px", read(p) or ""):
                if float(m.group(1)) < tbody_val:
                    small_tbody.append("%s:%spx" % (p.name, m.group(1)))
    ok = not bad_hex and not small_tbody
    detail = []
    if bad_hex:
        detail.append("hex вне tokens.css: %s" % bad_hex[:5])
    if small_tbody:
        detail.append("--t-body занижен: %s" % small_tbody)
    status = PASS if ok else FAIL
    return GateResult(status, "; ".join(detail) or "палитра только токенами, --t-body не занижен",
                       bool(candidates),
                       ["[браузерный] overflow .zone — прогнать локально: "
                        "python3 _generator/audit.py <лекция>/src/dist/index.html",
                        "автор-чекпоинт: глаз (render.py) — не автоматизируется"])


BLUR_RE = re.compile(r"\{blur@\d+\|(.*?)\}")
CONNECTIVE_LEADING = tuple("≈=⇒→")


def check_g9(lek, ctx):
    if ctx.get("slides_flag") == "нет":
        return GateResult(NA, "слайды: нет — доска")
    src = lek / "src"
    content_dir = src / "content"
    bad = []
    touched = False
    for p in content_dir.glob("*.md") if content_dir.is_dir() else []:
        text = read(p) or ""
        for m in BLUR_RE.finditer(text):
            touched = True
            body = m.group(1).lstrip()
            if body[:1] in CONNECTIVE_LEADING:
                bad.append("%s: %s" % (p.name, m.group(0)[:40]))
    status = WARN if bad else PASS
    return GateResult(status, ("связка внутри blur (дисциплина-хук): %s" % bad) if bad else "связки вне blur",
                       touched,
                       ["[браузерный — жёсткая часть] --scene-diff (заморож. геометрия, 0 дед-кликов) — "
                        "прогнать локально: python3 _generator/audit.py <лекция>/src/dist/index.html --scene-diff"])


def check_g10(lek, ctx):
    if ctx.get("slides_flag") == "нет":
        return GateResult(NA, "слайды: нет — доска")
    src = lek / "src"
    if not (src / "shablon.html").is_file():
        return GateResult(FAIL, "нет src/")
    shablon, filemap, meta, names = bd.load_source(src)
    errors, warns, _assembled = bd.lint(shablon, filemap, meta, names)
    var_errors = [e for e in errors if "var(--" in e]
    id_map = {}
    for p in (src / "illustrations").glob("*.svg"):
        for idv in re.findall(r'id="([^"]+)"', read(p) or ""):
            id_map.setdefault(idv, []).append(p.stem)
    conflicts = [(idv, files) for idv, files in id_map.items() if len(files) > 1]
    ok = not var_errors and not conflicts
    detail = []
    if var_errors:
        detail.append("; ".join(var_errors[:5]))
    if conflicts:
        detail.append("id-конфликт между иллюстрациями: %s" % conflicts)
    status = PASS if ok else FAIL
    return GateResult(status, "; ".join(detail) or "var(--x) определены, 0 id-конфликтов",
                       bool(names.get("illustrations")),
                       ["[браузерный] svgOverflow — прогнать локально: "
                        "python3 _generator/audit.py <лекция>/src/dist/index.html"])


def check_g11(lek, ctx):
    if ctx.get("slides_flag") == "нет":
        return GateResult(NA, "слайды: нет — доска")
    src = lek / "src"
    if not (src / "shablon.html").is_file():
        return GateResult(FAIL, "нет src/")
    try:
        r = subprocess.run([sys.executable, str(BUILD_DECK_PY), str(src), "--lint"],
                            capture_output=True, text=True, timeout=60)
    except Exception as e:  # noqa: BLE001 — печатаем как FAIL-деталь, не роняем трекер
        return GateResult(FAIL, "build_deck.py не запустился: %s" % e, touched=True)
    ok = r.returncode == 0
    tail = (r.stdout or r.stderr or "").strip().splitlines()
    detail = "" if ok else "; ".join(tail[-3:])
    status = PASS if ok else FAIL
    return GateResult(status, detail or "линтер (слой 1) зелёный", touched=True, extra_warns=[
        "[браузерный] слой 2 render-identity (правка) — python3 _generator/render.py --compare orig rebuilt "
        "(greenfield без provenance_sha256 → N/A)",
        "[браузерный] слой 3 audit.py, слой 4 --scene-diff — прогнать локально",
        "автор-чекпоинт: слой 5, глаз владельца на render.py-PNG — не автоматизируется",
    ])


# ───────────────── Фаза II: G12-G15 (заведены 27.07.2026) ─────────────────
# Калибровка ниже — не вольность, а замер: см. `_studio/zhurnal/
# 2026-07-27_paskal-lekcia-sborka/kod_gejty-shaga-6.md` §ПЛАН п.4, где по каждому
# отступлению от буквы GEJTY.md названо, сколько ложных ❌ давала буква на живых деках.
# Ложное срабатывание тут дороже пропуска: гейт, краснеющий на здоровом деке,
# обходят через --no-verify — и тогда пропадает вся защита, а не одна проверка.

G12_WORD_LIMIT = 25
SCENES_ATTR_RE = re.compile(r'data-scenes="(\d+)"')
SCENE_BIND_RE = re.compile(r'data-scene(?:-from|-until)?="(\d+)"')
ILL_TAG_RE = re.compile(r'<[^>]*\bdata-ill="[^"]*"[^>]*>')
ILL_NAME_RE = re.compile(r'data-ill="([^"]+)"')
STAGES_RE = re.compile(r'data-stages="([^"]*)"')
SCENE_ANY_ATTR_RE = re.compile(r'data-scene-(?:from|until)="(\d+)"')
SCENE_FROM_ATTR_RE = re.compile(r'data-scene-from="(\d+)"')


def _slide_pair(src, sid):
    """(html слайда, md текста) — оба могут быть пустой строкой."""
    return read(src / "slides" / (sid + ".html")) or "", read(src / "content" / (sid + ".md")) or ""


def _order_of(lek, ctx):
    return _load_src_brief(lek / "src").get("slide_order") or []


def _scene_sources(slide_html, content_md):
    """Номера сцен, ТРЕБУЕМЫЕ разметкой слайда: маркеры текста + `data-scene-from/until`.

    Стадии канваса (`data-stages`) сюда не входят намеренно: стадия ≠ клик,
    несколько стадий законно проигрываются внутри одной сцены, и приравнивать их
    номеру сцены значит краснеть на здоровом sim-слайде. Их учитывает
    `_stages_hint` — только чтобы ОБЪЯСНИТЬ избыток объявленных сцен, никогда
    чтобы обвинить."""
    return marks_all(content_md) | {int(x) for x in SCENE_ANY_ATTR_RE.findall(slide_html)}


def _stages_hint(slide_html):
    return max([len(s.split()) for s in STAGES_RE.findall(slide_html) if s.split()] or [0])


def _slide_own_text(slide_html):
    """Текст, напечатанный прямо в каркасе слайда (мимо `content/<id>.md`).

    У обложек и финалов канонного устройства текст живёт именно здесь, а
    `content/<id>.md` пуст — считать слова только по нему значит, что G12
    беспрепятственно пропустит ровно ту перегруженную обложку, ради которой заведён."""
    body = re.sub(r"(?s)<(script|style)\b.*?</\1>", " ", slide_html)
    body = re.sub(r"\{\{[^}]*\}\}", " ", body)
    return re.sub(r"<[^>]+>", " ", body)


def check_g12(lek, ctx):
    if ctx.get("slides_flag") == "нет":
        return GateResult(NA, "слайды: нет — доска")
    order = _order_of(lek, ctx)
    if len(order) < 2:
        return GateResult(NA, "в slide_order меньше двух слайдов — обложки и финала нет")
    src = lek / "src"
    detail = []
    for role, sid in (("обложка", order[0]), ("финал", order[-1])):
        slide_html, content_md = _slide_pair(src, sid)
        text = strip_shortcodes(content_md)
        if not text.strip():
            text = _slide_own_text(slide_html)
        words = count_words(re.sub(r"<[^>]+>", " ", text))
        if words > G12_WORD_LIMIT:
            detail.append("%s %s: %d слов > %d" % (role, sid, words, G12_WORD_LIMIT))
        ills = ILL_NAME_RE.findall(slide_html)
        if len(ills) > 1:
            detail.append("%s %s: иллюстраций %d > 1 (%s)" % (role, sid, len(ills), ills))
        marks = marks_all(content_md)
        if marks:
            detail.append("%s %s: сцен на обложке и финале не бывает (сцены %s)"
                          % (role, sid, sorted(marks)))
    status = FAIL if detail else PASS
    return GateResult(status, "; ".join(detail) or
                      "обложка %s и финал %s не перегружены" % (order[0], order[-1]), True,
                      ["автор-чекпоинт: сильный ли образ финала — вкус, механически не решается"])


def check_g13(lek, ctx):
    if ctx.get("slides_flag") == "нет":
        return GateResult(NA, "слайды: нет — доска")
    src = lek / "src"
    detail, soft = [], []
    touched = False
    for sid in _order_of(lek, ctx):
        slide_html, content_md = _slide_pair(src, sid)
        if not slide_html:
            continue
        m = SCENES_ATTR_RE.search(slide_html)
        # без объявленного data-scenes верхней границы не существует — а не «равна 1»:
        # к этому состоянию ведёт сам H6 (величина порождается сборкой, в src/ её нет),
        # и красить за достижение объявленной цели гейт не должен
        n_scenes = int(m.group(1)) if m else None
        tags = ILL_TAG_RE.findall(slide_html)
        bound = [(t, int(SCENE_BIND_RE.search(t).group(1))) for t in tags if SCENE_BIND_RE.search(t)]
        if tags:
            touched = True
        for tag, k in bound:
            # жёсткая часть признака: привязка ведёт к СУЩЕСТВУЮЩЕЙ сцене, не к «сцене 0».
            # Требовать вдобавок маркер `{@k}` в тексте нельзя: илл. вправе занимать
            # собственную сцену, где текстовой дельты нет (fibonacci/s02-hook, paskal/sl-pairs).
            if k < 2 or (n_scenes is not None and k > n_scenes):
                detail.append("%s: илл. %s привязана к сцене %d вне 2..%s"
                              % (sid, ILL_NAME_RE.search(tag).group(1), k,
                                 n_scenes if n_scenes is not None else "?"))
        if "{blur@" in content_md and tags and not bound:
            soft.append("%s (%s)" % (sid, ", ".join(ILL_NAME_RE.findall(slide_html))))
    extra = ["автор-чекпоинт: является ли рисунок ответом на вопрос слайда — вкус"]
    if soft:
        extra.append("рисунок показан с первой сцены, а в тексте есть {blur@ (спрятанный ответ): %s. "
                     "Оставлено WARN, не FAIL: признак опирается на суждение «рисунок и есть ответ», "
                     "которое GEJTY относит к автор-чекпоинту" % soft)
    status = FAIL if detail else PASS
    return GateResult(status, "; ".join(detail) or "привязки илл. ведут к существующим сценам",
                      touched, extra)


def check_g14(lek, ctx):
    if ctx.get("slides_flag") == "нет":
        return GateResult(NA, "слайды: нет — доска")
    src = lek / "src"
    detail, soft = [], []
    touched = False
    for sid in _order_of(lek, ctx):
        slide_html, content_md = _slide_pair(src, sid)
        m = SCENES_ATTR_RE.search(slide_html)
        if not m:
            continue  # каркаса слайда нет — это предмет G6, не G14
        touched = True
        declared = int(m.group(1))
        nums = _scene_sources(slide_html, content_md)
        need = max(nums) if nums else 1
        if need > declared:
            # урок 7: блюр не раскрывается, кликер уходит на следующий слайд
            detail.append("%s: data-scenes=%d, а разметка требует %d (сцены %s)"
                          % (sid, declared, need, sorted(nums)))
        elif need < declared and not ("data-sim=" in slide_html or "data-iframe=" in slide_html
                                      or _stages_hint(slide_html) >= declared):
            soft.append("%s: data-scenes=%d, статически видно %d" % (sid, declared, need))
    extra = ["правильная починка — не сверка, а генерация: data-scenes должен вычисляться сборкой "
             "из текста (GEJTY §G14, см. H6)"]
    if soft:
        extra.append("объявлено больше сцен, чем видно статически: %s — WARN, не FAIL "
                     "(дед-клик ловит браузерный слой G9 --scene-diff)" % soft)
    status = FAIL if detail else PASS
    return GateResult(status, "; ".join(detail) or "data-scenes согласован с разметкой сцен",
                      touched, extra)


def _css_text(src):
    """Весь статический CSS источника: собственные *.css + <style> шаблона."""
    parts = [read(p) or "" for p in sorted(src.glob("*.css"))]
    parts.append(read(src / "shablon.html") or "")
    return "\n".join(parts)


def check_g15(lek, ctx):
    if ctx.get("slides_flag") == "нет":
        return GateResult(NA, "слайды: нет — доска")
    src = lek / "src"
    css = _css_text(src)
    if not css.strip():
        # без CSS источника обвинять каскад не в чем — это предмет G8, не G15
        return GateResult(NA, "CSS источника не найден (нет src/*.css и shablon.html)", False)
    cover_any = {int(m.group(1)) for m in re.finditer(r"\.scene-(\d+)", css)}
    if not cover_any:
        # каскада нет ни в одном src/*.css и ни в shablon.html. Это либо дек без
        # сцен, либо каскад порождается сборкой (цель H6) — обвинять его в дырах
        # нельзя, дыр не с чем сверять. Предел проверки назван вслух, а не замолчан.
        return GateResult(NA, "правил `.scene-N` нет ни в src/*.css, ни в shablon.html — "
                              "каскад либо не нужен, либо порождается сборкой", False,
                          ["если каскад живёт вне src/ (в slides/*.html или в dist/), "
                           "G15 его не видит и полноту НЕ подтверждает"])
    cover = {
        # семейство «раскладка»: {@N}/{fill@N} и data-scene-from/until
        "data-scene-from": {int(m.group(1)) for m in
                            re.finditer(r"\.scene-(\d+)\s*\[data-scene-(?:from|until)", css)} or cover_any,
        # семейство «блюр»: {blur@N} → <span class="blur-reveal" data-reveal="N">
        "blur-reveal": {int(m.group(1)) for m in
                        re.finditer(r"\.scene-(\d+)[^,{]*(?:blur-reveal|data-reveal)", css)} or cover_any,
    }
    used = {"data-scene-from": set(), "blur-reveal": set()}
    touched = bool(cover_any)
    for sid in _order_of(lek, ctx):
        slide_html, content_md = _slide_pair(src, sid)
        used["data-scene-from"] |= marks_revealing(content_md)
        used["data-scene-from"] |= {int(x) for x in SCENE_FROM_ATTR_RE.findall(slide_html)}
        used["blur-reveal"] |= {int(x) for x in re.findall(r"\{blur@(\d+)", content_md)}
        if slide_html:
            touched = True
    detail = []
    for family, ks in used.items():
        if not ks:
            continue
        # с 2, не с 1: сцена 1 — базовое состояние, раскрывать в каскаде нечего.
        holes = sorted(k for k in range(2, max(ks) + 1) if k not in cover[family])
        if holes:
            detail.append("каскад %s оборван: сцены %s используются, правил .scene-N нет "
                          "(урок 8 — последняя сцена начнёт повторять первую)" % (family, holes))
    status = FAIL if detail else PASS
    return GateResult(status, "; ".join(detail) or
                      "каскады .scene-N покрывают все используемые сцены обоих семейств",
                      touched,
                      ["каскад судится по семействам (раскладка / блюр) отдельно: объединение "
                       "`.scene-\\d+` проспало бы обрыв одного семейства при полном другом"])


# ───────────────────────── дисциплина-хуки H1-H6 ─────────────────────────

def check_h1(lek, ctx):
    text = read(lek / "kartoteka" / "KARTA-OBLASTI.md")
    if text is None:
        return GateResult(WARN, "нет kartoteka/KARTA-OBLASTI.md")
    cards = [c for c in parse_cards(text) if c["rod"] in ROD_OK]
    no_source = [c["id"] for c in cards if not c["istochnik"]]
    return GateResult(WARN if no_source else PASS,
                       "карточки без источника: %s" % no_source if no_source else "0 карточек без источника",
                       bool(cards))


def check_h2(lek, ctx):
    karta_text = read(lek / "kartoteka" / "KARTA-OBLASTI.md")
    vychitano_text = read(lek / "istochniki" / "VYCHITANO.md") or ""
    if karta_text is None:
        return GateResult(WARN, "нет kartoteka/KARTA-OBLASTI.md")
    cards = [c for c in parse_cards(karta_text) if c["rod"] in ROD_OK]
    sources = {c["istochnik"] for c in cards if c["istochnik"]}
    missing = [s for s in sources if ("### " + s) not in vychitano_text]
    return GateResult(WARN if missing else PASS,
                       "источники без дайджеста VYCHITANO: %s" % missing if missing else "все источники продайджестены",
                       bool(sources),
                       ["формат заголовка дайджеста в VYCHITANO.md проверен по шаблону bootstrap "
                        "(`### <файл или ссылка>`), не по живому файлу Каталана — сверить при первом реальном деке"])


def check_h3(lek, ctx):
    text = read(lek / "kartoteka" / "KARTA-OBLASTI.md")
    if text is None:
        return GateResult(WARN, "нет kartoteka/KARTA-OBLASTI.md")
    cards = parse_cards(text)
    known_ids = {c["id"] for c in cards}
    referenced = {e for c in cards for e in c["svyazi"]}
    dangling = sorted(referenced - known_ids)
    return GateResult(WARN if dangling else PASS,
                       "висячие рёбра: %s" % dangling if dangling else "0 висячих рёбер",
                       bool(cards))


def check_h4(lek, ctx):
    text = read(lek / "kotly" / "matematika.md")
    if text is None:
        return GateResult(WARN, "нет kotly/matematika.md")
    open_n, total = flag_balance(text)
    return GateResult(WARN if open_n > 0 else PASS,
                       "непарных ⚑ Флаг: %d (раннее предупреждение)" % open_n if open_n else "0 непарных флагов",
                       total > 0)


def check_h5(lek, ctx):
    if ctx.get("slides_flag") == "нет":
        return GateResult(NA, "слайды: нет — доска")
    src = lek / "src"
    meta = _load_src_brief(src)
    order = set(meta.get("slide_order") or [])
    present = {p.stem for p in (src / "slides").glob("*.html")} if (src / "slides").is_dir() else set()
    diff = (order ^ present)
    return GateResult(WARN if diff else PASS,
                       "slide_order/slides разошлись: %s" % sorted(diff) if diff else "slide_order == slides/",
                       bool(order) or bool(present))


def check_h6(lek, ctx):
    """Величина, обязанная совпадать с другой, выписана руками (GEJTY §H6).

    WARN здесь — норма, а не поломка: пока data-scenes и каскад .scene-N пишутся
    руками, а не порождаются сборкой, хук обязан говорить. Ноль совпадений —
    цель, при которой G14/G15 становятся бессодержательными."""
    if ctx.get("slides_flag") == "нет":
        return GateResult(NA, "слайды: нет — доска")
    src = lek / "src"
    slides_dir = src / "slides"
    hand_scenes = []
    for p in sorted(slides_dir.glob("*.html")) if slides_dir.is_dir() else []:
        n = len(SCENES_ATTR_RE.findall(read(p) or ""))
        if n:
            hand_scenes.append("%s×%d" % (p.stem, n))
    hand_css = len(re.findall(r"\.scene-\d+", _css_text(src)))
    if not hand_scenes and not hand_css:
        return GateResult(PASS, "вычислимых величин, выписанных руками, нет",
                          bool(list(slides_dir.glob("*.html"))) if slides_dir.is_dir() else False)
    parts = []
    if hand_scenes:
        parts.append("data-scenes руками в %d слайдах (%s%s)"
                     % (len(hand_scenes), ", ".join(hand_scenes[:5]),
                        ", …" if len(hand_scenes) > 5 else ""))
    if hand_css:
        parts.append("рукописных `.scene-N` в CSS: %d" % hand_css)
    return GateResult(WARN, "; ".join(parts) + " — должно вычисляться сборкой из текста", True,
                      ["лечение — генерация в build_deck.py, не сверка; до неё G14/G15 лечат симптом"])


# Порядок прохождения — из GEJTY.md: G1 → … → G5 → G7 → G6 → G8 → …
# (G7 переехал в конец Фазы I 27.07.2026, id сохранён). G12–G15 живут внутри
# арок 7–10; в цепочке «прыжков вперёд» участвуют только гейты-границы.
GATE_ORDER = ["G1", "G2", "G3", "G4", "G5", "G7", "G6", "G8", "G9", "G10", "G11",
              "G12", "G13", "G14", "G15"]
STAGE_CHAIN = ["G1", "G2", "G3", "G4", "G5", "G7", "G6", "G8", "G9", "G10", "G11"]
GATES = {
    "G1": ("бриф закрыт", "граница 1→2", check_g1),
    "G2": ("ресёрч закрыт", "граница 2→3", check_g2),
    "G3": ("математика верна", "граница 3→4", check_g3),
    "G4": ("источник закрыт", "граница 4→5", check_g4),
    "G5": ("раскадровка закрыта", "граница 5→вход Фазы II", check_g5),
    "G6": ("вход Фазы II готов", "precondition", check_g6),
    "G7": ("предвёрсточный документ принят", "граница 6→вход Фазы II", check_g7),
    "G8": ("вёрстка", "граница 7→8", check_g8),
    "G9": ("сцены без дед-кликов", "граница 8→9/10", check_g9),
    "G10": ("иллюстрации", "граница 9→10", check_g10),
    "G11": ("сборка + QA", "финальный", check_g11),
    "G12": ("обложка и финал", "внутри арки 7", check_g12),
    "G13": ("илл.-ответ не раньше сцены", "границы 8→9, 9→10", check_g13),
    "G14": ("data-scenes согласован", "внутри арки 8", check_g14),
    "G15": ("каскады сцен полны", "границы 8→9, 10", check_g15),
}
HOOK_ORDER = ["H1", "H2", "H3", "H4", "H5", "H6"]
HOOKS = {
    "H1": ("карточка без источника", check_h1),
    "H2": ("источник без дайджеста VYCHITANO", check_h2),
    "H3": ("висячее ребро в KARTA-OBLASTI", check_h3),
    "H4": ("открытый ⚑ Флаг (раннее предупреждение)", check_h4),
    "H5": ("slide_order-сироты/дубли (раннее предупреждение)", check_h5),
    "H6": ("величина выписана руками в двух местах", check_h6),
}


# ───────────────────────── журнал: сверка журнал↔диск ─────────────────────────

JOURNAL_RE = re.compile(
    r"^\s*(?P<data>\S+)\s*·\s*(?P<funkcia>[^·]+?)\s*·\s*(?P<volna>[^·]+?)\s*·\s*(?P<geit>[^·]+?)\s*·\s*"
    r"(?P<rezultat>PASS|недобор)\s*·\s*(?P<vremya>[^·]+?)\s*·\s*(?P<tokeny>[^·]+?)\s*$")


def parse_journal(text):
    rows, bad = [], 0
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith(">"):
            continue
        m = JOURNAL_RE.match(line)
        if m:
            rows.append(m.groupdict())
        elif "·" in line:
            bad += 1
    return rows, bad


def check_journal(lek, results, ctx):
    p = lek / "dnevnik" / "zhurnal.md"
    text = read(p)
    if text is None:
        return None
    rows, bad_lines = parse_journal(text)
    print("\n── ЖУРНАЛ (%s) ──" % p)
    if bad_lines:
        print("  ⚠ %d строк(и) не разобрано (формат не ` · ` × 7 полей) — пропущены" % bad_lines)
    if not rows:
        print("  (нет разобранных строк)")
        return rows
    for r in rows:
        print("  %s · %s · волна%s · %s · %s · %s · %s" % (
            r["data"], r["funkcia"], r["volna"], r["geit"], r["rezultat"], r["vremya"], r["tokeny"]))
    silent_gaps = []
    for r in rows:
        gid = r["geit"].strip()
        if r["rezultat"] == "PASS" and gid in results:
            actual = results[gid].status
            if actual == FAIL:
                silent_gaps.append((gid, r["data"], actual, results[gid].detail))
    if silent_gaps:
        print("  ⚠ МОЛЧАЛИВЫЙ НЕДОБОР:")
        for gid, data, actual, detail in silent_gaps:
            print("     %s (запись %s: журнал=PASS, диск=%s) — %s" % (gid, data, actual, detail))
    else:
        print("  ✓ расхождений журнал↔диск не найдено")
    return rows


# ───────────────────────── прогон + печать ─────────────────────────

def run(lek):
    ctx = {}
    results = {}
    # G1 первым — заполняет ctx['slides_flag'] для остальных
    for gid in GATE_ORDER:
        _name, _stage, fn = GATES[gid]
        results[gid] = fn(lek, ctx)
    hook_results = {hid: fn(lek, ctx) for hid, (_name, fn) in HOOKS.items()}
    return ctx, results, hook_results


def find_here(results):
    for gid in GATE_ORDER:
        if results[gid].status == FAIL:
            return gid
    for gid in reversed(GATE_ORDER):
        if results[gid].status == PASS:
            return gid + " (пройден)"
    return GATE_ORDER[0]


def print_report(lek, ctx, results, hook_results):
    print("СОСТОЯНИЕ: %s\n" % lek)
    print("слайды: %s\n" % (ctx.get("slides_flag") or "?"))
    print("── ГЕЙТЫ ──")
    for gid in GATE_ORDER:
        name, stage, _fn = GATES[gid]
        r = results[gid]
        print("%-4s %-24s %-5s  %s" % (gid, name, r.status, r.detail))
        for w in r.extra_warns:
            print("     ⚠ %s" % w)

    print("\n── ДИСЦИПЛИНА-ХУКИ (WARN, continuous) ──")
    for hid in HOOK_ORDER:
        name, _fn = HOOKS[hid]
        r = hook_results[hid]
        print("%-4s %-40s %-5s  %s" % (hid, name, r.status, r.detail))

    print("\n── ПРЫЖКИ ВПЕРЁД (артефакт стадии N+1 тронут, гейт N не PASS/N-A) ──")
    jumps = []
    for i in range(len(STAGE_CHAIN) - 1):
        cur, nxt = STAGE_CHAIN[i], STAGE_CHAIN[i + 1]
        if results[nxt].touched and results[cur].status not in (PASS, NA):
            jumps.append((nxt, cur))
    if jumps:
        for nxt, cur in jumps:
            print("  ⚠ %s тронут, а %s ещё не PASS" % (nxt, cur))
    else:
        print("  (нет)")

    here = find_here(results)
    print("\n⏺ ТЫ ЗДЕСЬ: %s" % here)

    hard_fail = [gid for gid in GATE_ORDER if results[gid].status == FAIL]
    print("\nИтог: %s жёстких FAIL: %s" % (len(hard_fail), hard_fail or "—"))
    return 1 if hard_fail else 0


def main():
    ap = argparse.ArgumentParser(description="Трекер состояния лекции по GEJTY.md (read-only)")
    ap.add_argument("lekcia", help="путь к папке лекции")
    args = ap.parse_args()
    lek = Path(args.lekcia)
    if not lek.is_dir():
        print("ОШИБКА: не папка — %s" % lek, file=sys.stderr)
        return 1

    ctx, results, hook_results = run(lek)
    exit_code = print_report(lek, ctx, results, hook_results)
    check_journal(lek, results, ctx)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
