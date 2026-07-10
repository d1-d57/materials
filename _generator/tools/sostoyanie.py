#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Трекер состояния лекции по реестру гейтов (_studio/konvejer/GEJTY.md).

    python3 sostoyanie.py <папка-лекции>

Read-only: ничего в папке лекции не меняет. По каждому из 16 гейтов/хуков
GEJTY.md считает PASS/FAIL/WARN/N-A по «признаку-на-диске», печатает таблицу,
вычисляет ⏺ ТЫ ЗДЕСЬ (первый жёсткий гейт не-PASS) и сверяет журнал
(<лекция>/dnevnik/zhurnal.md, см. ZHURNAL.md) с диском — молчаливый недобор:
строка журнала говорит PASS, а сам гейт на диске FAIL.

Реестр гейтов (GEJTY.md) — проза, не машиночитаема; поэтому 16 записей
(G1-G11, H1-H5) закодированы здесь как структуры Python с одной
check-функцией на гейт. Функции пишут в терминах grep/regex — буквально то,
что называет «признак-на-диске» в GEJTY.md; где признак неоднозначен —
проверка ослаблена до WARN/advisory с пометкой (см. kod_treker.md #ВОПРОСЫ).

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


# ───────────────────────── Фаза II: G7-G11 ─────────────────────────

def check_g7(lek, ctx):
    if ctx.get("slides_flag") == "нет":
        return GateResult(NA, "слайды: нет — доска")
    src = lek / "src"
    meta = _load_src_brief(src)
    order = meta.get("slide_order") or []
    budget_raw = meta.get("word_budget_per_slide")
    budget_n = int(budget_raw) if budget_raw and str(budget_raw).isdigit() else None
    empty, has_html, over_acc, over_budget = [], [], [], []
    touched = False
    for sid in order:
        p = src / "content" / (sid + ".md")
        text = read(p)
        if not text or not text.strip():
            empty.append(sid)
            continue
        touched = True
        if re.search(r"<[a-zA-Z]", text):
            has_html.append(sid)
        if text.count("**") // 2 > 1:
            over_acc.append(sid)
        if budget_n:
            words = len(text.split())
            if words > budget_n * 1.2:
                over_budget.append("%s(%d)" % (sid, words))
    ok = not empty and not has_html and not over_acc
    detail = []
    if empty:
        detail.append("нет/пуст content/: %s" % empty)
    if has_html:
        detail.append("html-теги в content/ (запрещено): %s" % has_html)
    if over_acc:
        detail.append(">1 acc-блока: %s" % over_acc)
    status = PASS if ok else FAIL
    extra = ["автор-чекпоинт: голос/архетип/законченность мысли — вкус, не грепается"]
    if not budget_n:
        extra.append("word_budget_per_slide не число — бюджет слов не проверен")
    elif over_budget:
        extra.append("допуск бюджета слов не задан числом в GEJTY.md — эвристика +20%%: превышают %s" % over_budget)
    return GateResult(status, "; ".join(detail) or "%d слайдов в бюджете, без html, ≤1 acc" % len(order),
                       touched, extra)


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


# ───────────────────────── дисциплина-хуки H1-H5 ─────────────────────────

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


GATE_ORDER = ["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11"]
GATES = {
    "G1": ("бриф закрыт", "граница 1→2", check_g1),
    "G2": ("ресёрч закрыт", "граница 2→3", check_g2),
    "G3": ("математика верна", "граница 3→4", check_g3),
    "G4": ("источник закрыт", "граница 4→5", check_g4),
    "G5": ("раскадровка закрыта", "граница 5→вход Фазы II", check_g5),
    "G6": ("вход Фазы II готов", "precondition", check_g6),
    "G7": ("плакатный баланс", "граница 6→7", check_g7),
    "G8": ("вёрстка", "граница 7→8", check_g8),
    "G9": ("сцены без дед-кликов", "граница 8→9/10", check_g9),
    "G10": ("иллюстрации", "граница 9→10", check_g10),
    "G11": ("сборка + QA", "финальный", check_g11),
}
HOOK_ORDER = ["H1", "H2", "H3", "H4", "H5"]
HOOKS = {
    "H1": ("карточка без источника", check_h1),
    "H2": ("источник без дайджеста VYCHITANO", check_h2),
    "H3": ("висячее ребро в KARTA-OBLASTI", check_h3),
    "H4": ("открытый ⚑ Флаг (раннее предупреждение)", check_h4),
    "H5": ("slide_order-сироты/дубли (раннее предупреждение)", check_h5),
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
    for i in range(len(GATE_ORDER) - 1):
        cur, nxt = GATE_ORDER[i], GATE_ORDER[i + 1]
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
