#!/usr/bin/env python3
"""ПРИЁМКА ОТЧЁТА — механизм, а не проза, которую произносят вслух каждый раз.

    python3 _generator/tools/priyomka.py <путь к kod_*.md> [--zone <префикс>]

ЗАЧЕМ ЭТОТ ФАЙЛ СУЩЕСТВУЕТ (причина дороже кода — не удалять).

Приёмка отчёта в каноне (`RUKOVODSTVO-zahodami.md §Приёмка отчёта`) расписана
на ШЕСТЬ шагов, и носитель есть ровно у одного — шага 0 (`git_zona.py check
--zone`). Остальные пять — проза, которую владелец проговаривает вслух на
каждом отчёте. Само это измерено каноном: из 8 вопросов исполнителей до
владельца дошло 0, из 17 уроков до канона дошёл 1. Правило, которое
приходится произносить вслух на каждом применении, механизмом не является.

Этот инструмент НЕ ЗАМЕНЯЕТ аналитика — он отбирает у него возможность
забыть. Делает два разных дела, и они разделены в выводе:

1. МАШИННЫЕ ГЕЙТЫ (Г0-Г6) — проверяет сам, exit 1 при любом красном.
2. ПЕЧАТЬ ДЛЯ РУК — то, что машина проверить не может (вопросы исполнителя,
   уроки фабрике, числовые утверждения отчёта, чек-лист оставшихся шагов
   канона), но обязана положить аналитику на стол. Печатается ВСЕГДА, даже
   когда все гейты зелёные — то же решение, что у `zakryt_sessiyu.py`:
   инструмент не решает, что важно, и ничего не резюмирует.

🔴 Г3 «артефакт не старше источника»: «источник» здесь — САМ файл-заход
(другого универсально доступного ориентира у generic-инструмента, работающего
с любым `kod_*.md`, нет). Известный острый угол: файл-заход часто дописывается
ОТЧЁТОМ последним ходом, и тогда его mtime может стать позже, чем у
кодового артефакта, собранного раньше в сессии — читай про это в `## ВОПРОСЫ`
файла-захода, которым эта версия построена.

🔴 Г6 «урок без пары в доме уроков»: точное семантическое сопоставление
строки дневника с записью `UROKI-FABRIKE.md` этим инструментом не делается —
только stdlib, без NLP. Реализовано терпимо: печатаются ВСЕ совпадения
`урок` в `SESSIYA.md` регистронезависимо и по одному слову (та же форма,
что канон явно требует после истории с «Урок фабрике» через заглавную,
давшей ложное зелёное на старой форме грепа), а красным Г6 становится
только когда совпадения ЕСТЬ, а `UROKI-FABRIKE.md` арки отсутствует или не
содержит ни одной записи `### `. Терпимая сторона ошибки — ловит лишнее —
и это ПРАВИЛЬНАЯ сторона: ложное срабатывание стоит одного взгляда, пропуск
стоит урока.

Только stdlib.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
REPO = TOOLS.parent.parent

# Тот же приём, что в dnevnik.py: гейт зовут и из корня репо, и из хука, и из
# фикстуры — явная вставка пути надёжнее неявного sys.path[0].
sys.path.insert(0, str(TOOLS))
import dnevnik  # noqa: E402


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore")


def sekciya(tekst: str, zagolovok: str):
    """Текст секции `## <zagolovok>` до следующего `## ` или конца файла.

    None, если секции нет вовсе; иначе — тело ПОСЛЕ строки заголовка (сама
    строка заголовка в тело не входит, иначе «(заполняет исполнитель)» в
    шаблонной шапке секции всегда бы читался как «заполнено»).
    """
    # 🔴 `[^\n]*\n`, А НЕ `.*$` — под `re.S` (DOTALL) `.` пересекает переводы
    # строк ВЕЗДЕ в паттерне, и `.*$` для «остатка строки заголовка» жадно
    # проглатывал файл до последнего `$` во всём тексте, а не до конца своей
    # строки. Поймано живым прогоном: `## ОТЧЁТ` схлопывался в пустое тело.
    m = re.search(r'^##\s+' + re.escape(zagolovok) + r'[^\n]*\n(.*?)(?=^##\s|\Z)',
                  tekst, re.M | re.S)
    return m.group(1).strip() if m else None


def pole_otcheta(tekst: str, nazvanie: str):
    """Значение строки `**<nazvanie>:** ...` — весь остаток строки.

    🔴 ЯКОРЬ НА НАЧАЛО СТРОКИ (`^`, `re.M`) ОБЯЗАТЕЛЕН. Без него первое
    попавшееся упоминание `**КОММИТ:**` ГДЕ УГОДНО в тексте (например, внутри
    прозы отчёта, описывающей этот же баг цитатой) читается как строка поля.
    Поймано на живом прогоне ПРИЁМКИ ПО СОБСТВЕННОМУ ОТЧЁТУ этого захода:
    предложение «Г1 брал первый попавшийся `**КОММИТ:**` по всему файлу» само
    стало ложным совпадением. Настоящая строка поля всегда начинает строку.
    """
    m = re.search(r'^\*\*' + re.escape(nazvanie) + r':\*\*\s*(.*)', tekst, re.M)
    return m.group(1).strip() if m else None


def izvlech_zonu(tekst: str):
    """Зона для `git_zona.py check --zone` — из шаблонной строки §4 захода.

    Каждый файл-заход несёт в секции КОММИТ ровно эту команду (см. контракт
    зоны и §4 в этом самом файле) — префикс из неё и есть зона захода.
    Многосписочная «ЗОНА (можно менять):» в контракте не парсится нарочно:
    она перечисляет ПУТИ, а `git_zona.py check --zone` принимает ОДИН
    префикс, который уже выбрал исполнитель, и он же напечатан в §4.

    🔴 `[^\s\`]+`, А НЕ `\S+` — В ОТЧЁТЕ ЭТА КОМАНДА ОБЫЧНО В BACKTICKS БЕЗ
    ПРОБЕЛА ПЕРЕД ЗАКРЫВАЮЩИМ ` ` ` (например «`git_zona.py check --zone
    _generator/tools` → ✅»), и `\S+` жадно захватывал закрывающий backtick
    В СОСТАВ зоны. Зона с лишним символом не совпадала ни с одним реальным
    путём — и потому ВСЕГДА проверялась как пустая (полностью проверена),
    Г0 давал ✅ по ПРАВИЛЬНОМУ ВИДУ, но по НЕПРАВИЛЬНОЙ ПРИЧИНЕ. Поймано на
    живом прогоне приёмки по собственному отчёту этого захода.
    """
    m = re.search(r'git_zona\.py\s+check\s+--zone\s+([^\s`]+)', tekst)
    return m.group(1) if m else None


def fmt_time(mtime: float) -> str:
    import datetime
    return datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")


# ─────────────────────────── МАШИННЫЕ ГЕЙТЫ ────────────────────────────

def gate_g0(zona: str):
    if not zona:
        return False, ("зона не определена: нет `--zone` и в отчёте не найдена строка "
                        "`git_zona.py check --zone <префикс>` (обычно она в §4 КОММИТ)")
    r = subprocess.run(
        ["python3", str(TOOLS / "git_zona.py"), "check", "--zone", zona],
        cwd=REPO, capture_output=True, text=True,
    )
    vyvod = (r.stdout.strip() + ("\n" + r.stderr.strip() if r.stderr.strip() else "")).strip()
    if r.returncode != 0:
        return False, f"git_zona.py check --zone {zona} → красный (код {r.returncode})\n{vyvod}"
    return True, f"git_zona.py check --zone {zona} → ✅\n{vyvod}" if vyvod else f"git_zona.py check --zone {zona} → ✅"


def gate_g1(stroka_kommit):
    if not stroka_kommit:
        return False, "строка **КОММИТ:** не найдена в отчёте"
    m = re.search(r'\b[0-9a-f]{6,40}\b', stroka_kommit)
    if not m:
        return False, f"в строке КОММИТ нет хэша: {stroka_kommit!r}"
    khash = m.group(0)
    r = subprocess.run(["git", "--no-optional-locks", "show", "--stat", khash],
                        cwd=REPO, capture_output=True, text=True)
    if r.returncode != 0:
        return False, f"хэш {khash} не найден в репозитории (git show --stat упал, код {r.returncode})"
    pervaya = r.stdout.splitlines()[0] if r.stdout else ""
    return True, f"хэш {khash} существует: {pervaya}"


def gate_g2(stroka_artefakt):
    if not stroka_artefakt or not stroka_artefakt.strip():
        return False, "строка **АРТЕФАКТ:** пустая или отсутствует", None
    prime = stroka_artefakt.strip()
    put_chast = re.split(r'\s+—\s+|\s+-\s+', prime, maxsplit=1)[0].strip().strip('`').strip()
    if not put_chast or (put_chast.startswith('<') and put_chast.endswith('>')):
        return False, f"АРТЕФАКТ — плейсхолдер в угловых скобках или пусто: {prime!r}", None
    return True, f"путь заполнен: {put_chast}", put_chast


def git_commit_time(put_otnositelnyj: str):
    """Время последнего коммита, тронувшего путь. None — путь не в git."""
    r = subprocess.run(["git", "--no-optional-locks", "log", "-1", "--format=%ct", "--", put_otnositelnyj],
                        cwd=REPO, capture_output=True, text=True)
    stroka = r.stdout.strip()
    return int(stroka) if stroka else None


def gate_g3(put_str, zahod_path: Path):
    if put_str is None:
        return False, "Г2 не дал пути — сверка свежести пропущена"
    p = Path(put_str).expanduser()
    if not p.is_absolute():
        p = (REPO / p).resolve()
    if not p.exists():
        return False, f"артефакт не найден на диске: {p}"
    if not p.is_file():
        return True, f"артефакт {p} — не обычный файл (папка/ссылка), свежесть не сверяется"

    # 🔴 СРАВНИВАЕМ ВРЕМЯ ПОСЛЕДНЕГО КОММИТА, А НЕ mtime ФАЙЛА НАПРЯМУЮ.
    # Живой прогон на `kod_dnevnik-gejt.md` поймал это вживую: у файлов чужой
    # арки оказался ОДИН общий mtime от постороннего checkout/merge, никак не
    # связанный с реальным временем сборки — сравнение mtime было бы систематически
    # неверным. Коммит-время устойчиво: артефакт и файл-заход обычно едут ОДНИМ
    # и тем же коммитом зоны (§4 «КОММИТ»), и тогда время равно — гейт зелёный.
    def otnositelno_repo(put: Path):
        try:
            return str(put.relative_to(REPO))
        except ValueError:
            return None  # путь вне репозитория (например, фикстура во /tmp)

    put_otn_art = otnositelno_repo(p)
    put_otn_src = otnositelno_repo(zahod_path)
    art_t = git_commit_time(put_otn_art) if put_otn_art else None
    src_t = git_commit_time(put_otn_src) if put_otn_src else None
    if art_t is None or src_t is None:
        # Артефакт вне репозитория или ещё не закоммичен — коммит-время
        # недоступно, единственный оставшийся ориентир — mtime на диске.
        art_m, src_m = p.stat().st_mtime, zahod_path.stat().st_mtime
        if art_m < src_m:
            return False, (f"артефакт {p} СТАРШЕ файла-захода по mtime "
                            f"(коммит-время недоступно: артефакт вне git или не закоммичен) — "
                            f"(артефакт: {fmt_time(art_m)}, файл-заход: {fmt_time(src_m)})")
        return True, (f"артефакт не старше файла-захода по mtime "
                       f"(коммит-время недоступно: артефакт вне git или не закоммичен)")
    if art_t < src_t:
        return False, (f"артефакт {p} СТАРШЕ файла-захода по коммит-времени — сборка молча "
                        f"не запускалась или артефакт не доехал в тот же коммит "
                        f"(артефакт: {fmt_time(art_t)}, файл-заход: {fmt_time(src_t)})")
    return True, (f"артефакт не старше файла-захода по коммит-времени "
                   f"(артефакт: {fmt_time(art_t)}, файл-заход: {fmt_time(src_t)})")


def gate_g4(tekst):
    otchet = sekciya(tekst, "ОТЧЁТ")
    plan = sekciya(tekst, "ПЛАН")
    problemy = []
    if not otchet:
        problemy.append("## ОТЧЁТ пуста")
    if not plan:
        problemy.append("## ПЛАН пуста")
    if problemy:
        return False, "; ".join(problemy)
    return True, "## ОТЧЁТ и ## ПЛАН заполнены"


def gate_g5(tekst):
    uroki = sekciya(tekst, "УРОКИ ФАБРИКЕ")
    if not uroki:
        return True, "секция УРОКИ ФАБРИКЕ пуста — законный исход"
    zagolovki = re.findall(r'^###\s+(.+)$', uroki, re.M)
    if not zagolovki:
        return True, "секция УРОКИ ФАБРИКЕ есть, но без записей `### ` — законный исход"
    bloki = re.split(r'^###\s+.+$', uroki, flags=re.M)[1:]
    bez_ceny = [zag.strip() for zag, blok in zip(zagolovki, bloki) if not re.search(r'ЦЕНА:', blok)]
    if bez_ceny:
        return False, f"урок(и) без `ЦЕНА:`: {'; '.join(bez_ceny)}"
    return True, f"{len(zagolovki)} урок(ов), у каждого есть `ЦЕНА:`"


def posle_otsechki(tekst: str) -> str:
    """Текст SESSIYA.md ПОСЛЕ последней отсечки `<!-- РАЗНЕСЕНО ДО СЮДА: ... -->`.

    Без отсечки Г6 перечитывает файл целиком на каждой приёмке и печатает одни
    и те же старые совпадения «урок» из разнесённого прошлого — 49 строк на
    каждый прогон в одной живой арке. Гейт, который печатает 49 строк, читать
    перестанут (та же судьба, что у любого шумного гейта). Отсечку ставит
    аналитик рукой после разноса; нет отсечки — компромисс в пользу «поймать
    лишнее», как и раньше (терпимая сторона ошибки для Г6, см. докстринг файла).
    """
    sovpadeniya_otsechek = list(re.finditer(r'<!--\s*РАЗНЕСЕНО ДО СЮДА:.*?-->', tekst))
    if not sovpadeniya_otsechek:
        return tekst
    return tekst[sovpadeniya_otsechek[-1].end():]


def gate_g6(arka: Path):
    sessiya = arka / "SESSIYA.md"
    if not sessiya.is_file():
        return True, "в арке нет SESSIYA.md — Г6 неприменим", []
    tekst = posle_otsechki(read(sessiya))
    sovpadeniya = [ln.strip() for ln in tekst.splitlines() if re.search(r'урок', ln, re.I)]
    if not sovpadeniya:
        return True, "упоминаний «урок» в SESSIYA.md нет", []
    uroki_file = arka / "UROKI-FABRIKE.md"
    zapisej = len(re.findall(r'^###\s+', read(uroki_file), re.M)) if uroki_file.is_file() else 0
    ok = zapisej > 0
    soobshch = (f"{len(sovpadeniya)} упоминани(й/е) «урок» в SESSIYA.md, "
                f"в UROKI-FABRIKE.md записей `### `: {zapisej}"
                + ("" if ok else " — дома уроков нет или он пуст, пары быть не может"))
    return ok, soobshch, sovpadeniya


def parse_ochered(voprosy_tekst: str):
    """Пункты `## ВОПРОСЫ` с полями `ДОМ:`/`ДОСТАВЛЕНО:` (Ф1 этого захода).

    Формат пункта (шапка секции документирует его для исполнителя):
        N. <текст находки>
           ДОМ: <путь от корня репо | владелец>
           ДОСТАВЛЕНО: нет | <метка>

    Пункт без `ДОМ:` — обычный вопрос без чужого дома, очередь его не касается.
    Возвращает список dict: {"n": int, "tekst": str, "dom": str, "dostavleno": str}.
    """
    if not voprosy_tekst:
        return []
    punkty = re.split(r'^(\d+)\.\s+', voprosy_tekst, flags=re.M)
    # re.split с группой отдаёт [преамбула, num1, telo1, num2, telo2, ...]
    ochered = []
    for i in range(1, len(punkty), 2):
        n = int(punkty[i])
        telo = punkty[i + 1]
        # тело пункта — до следующего пронумерованного пункта (уже отрезано split)
        m_dom = re.search(r'^\s*ДОМ:\s*(.+)$', telo, re.M)
        if not m_dom:
            continue  # обычный вопрос без адреса — не пункт очереди
        m_dost = re.search(r'^\s*ДОСТАВЛЕНО:\s*(.+)$', telo, re.M)
        tekst_nahodki = telo.split('\n', 1)[0].strip()
        ochered.append({
            "n": n,
            "tekst": tekst_nahodki,
            "dom": m_dom.group(1).strip(),
            "dostavleno": m_dost.group(1).strip() if m_dost else "нет",
        })
    return ochered


def gate_g7(ochered):
    """Красный ТОЛЬКО когда пункт помечен доставленным, а по адресу нет метки.

    Ложное «сделано» опаснее честного «не сделано» (Ф1, часть B): недоставленный
    пункт (`ДОСТАВЛЕНО: нет`) не гейт вообще — он в печати для рук ниже. Дом
    «владелец» — не файл, факт передачи механически не проверить (Ф1 вопрос 2:
    у этого типа находки адрес — человек, а не путь) — вне гейта принципиально,
    тоже только печать.
    """
    problemy = []
    for p in ochered:
        if p["dostavleno"].strip().lower() == "нет":
            continue
        if p["dom"].strip().lower() == "владелец":
            continue
        put_doma = (REPO / p["dom"]).resolve() if not Path(p["dom"]).is_absolute() else Path(p["dom"])
        if not put_doma.is_file():
            problemy.append(f"пункт {p['n']} помечен доставленным (`{p['dostavleno']}`), "
                             f"а дом `{p['dom']}` не найден на диске")
            continue
        if p["dostavleno"] not in read(put_doma):
            problemy.append(f"пункт {p['n']} помечен доставленным (`{p['dostavleno']}`), "
                             f"а метки в доме `{p['dom']}` нет")
    if problemy:
        return False, "; ".join(problemy)
    if not ochered:
        return True, "пунктов очереди (ДОМ/ДОСТАВЛЕНО) нет"
    return True, f"{len(ochered)} пункт(ов) очереди, ложной доставки не найдено"


KONTRAKTNAYA_ZONA_RE = re.compile(r'^-\s*\*?\*?ЗОНА[^:]*:\*?\*?\s*(.+)$', re.M)


def granicy_zony(tekst: str, khash: str):
    """Печать (НЕ гейт): пути коммита за пределами `## КОНТРАКТ ЗОНЫ`.

    Формат контракта неоднороден (Ф1/часть C1) — ложное красное здесь дороже
    пропуска, поэтому только печать для рук, не гейт.
    """
    m = KONTRAKTNAYA_ZONA_RE.search(tekst)
    if not m:
        return "строка «ЗОНА» в контракте не найдена — сверка границ пропущена"
    prefiksy = [p.strip('`').strip() for p in re.findall(r'`([^`]+)`', m.group(1))]
    if not prefiksy:
        return "в строке «ЗОНА» нет путей в backticks — сверка границ пропущена"
    r = subprocess.run(["git", "--no-optional-locks", "show", "--stat", "--format=", khash],
                        cwd=REPO, capture_output=True, text=True)
    if r.returncode != 0:
        return f"git show --stat {khash} упал — сверка границ пропущена"
    puti = [ln.split('|')[0].strip() for ln in r.stdout.splitlines() if '|' in ln]
    za_predelami = [p for p in puti if not any(p == pref or p.startswith(pref.rstrip('/') + '/')
                                                for pref in prefiksy)]
    if not za_predelami:
        return f"все пути коммита внутри зоны ({len(puti)} из {len(puti)})"
    return (f"ВНЕ зоны контракта: {', '.join(za_predelami)} "
            f"(зона по контракту: {', '.join(prefiksy)})")


def tihij_nedobor(otchet_tekst):
    """Печать (НЕ гейт): формы «не успел/частично/осталось/не сделал» в ## ОТЧЁТ."""
    if not otchet_tekst:
        return []
    return [ln.strip() for ln in otchet_tekst.splitlines()
            if re.search(r'не успел|частично|осталось|не сделал', ln, re.I) and ln.strip()]


def ohvat_polozhitelnogo(otchet_tekst):
    """True, если среди числовых строк отчёта есть форма «X из Y» (охват)."""
    if not otchet_tekst:
        return False
    return re.search(r'\d+\s+из\s+\d+', otchet_tekst) is not None


# ────────────────────────── ПЕЧАТЬ ДЛЯ РУК ──────────────────────────

def chislovye_stroki(otchet_tekst):
    if not otchet_tekst:
        return []
    return [ln.strip() for ln in otchet_tekst.splitlines() if re.search(r'\d', ln) and ln.strip()]


CHEKLIST = (
    "  · разнести по домам (глоссарий / источники / канон / вопросы владельцу / СЛЕДУЮЩИЙ ЗАХОД)\n"
    "  · пересказать владельцу человеческим языком\n"
    "  · короткая рефлексия (что было не так и что поправить)\n"
    "  · строка в UROKI-FABRIKE.md арки"
)


def main() -> int:
    ap = argparse.ArgumentParser(description="Приёмка отчёта — машинные гейты + печать для рук")
    ap.add_argument("zahod", help="путь к файлу-заходу kod_*.md с дописанным отчётом")
    ap.add_argument("--zone", help="префикс зоны для git_zona.py check (иначе — из отчёта)")
    args = ap.parse_args()

    zahod_path = Path(args.zahod).resolve()
    if not zahod_path.is_file():
        print(f"❌ файл-заход не найден: {zahod_path}")
        return 1
    tekst = read(zahod_path)
    arka = zahod_path.parent

    zona = args.zone or izvlech_zonu(tekst)
    # 🔴 ИЩЕМ **КОММИТ:**/**АРТЕФАКТ:** ТОЛЬКО ВНУТРИ `## ОТЧЁТ`, А НЕ ПО ВСЕМУ
    # ФАЙЛУ. Живой прогон на `kod_dnevnik-gejt.md` поймал баг вживую: файл
    # обсуждает дисциплину коммита в других разделах, и первый попавшийся
    # `**КОММИТ:**` по всему тексту оказался цитатой из §4, а не строкой
    # отчёта — Г1 читал не то и красил ложно.
    otchet_dlya_polej = sekciya(tekst, "ОТЧЁТ") or tekst
    stroka_kommit = pole_otcheta(otchet_dlya_polej, "КОММИТ")
    stroka_artefakt = pole_otcheta(otchet_dlya_polej, "АРТЕФАКТ")

    gates = []
    gates.append(("Г0 зона доехала в git", *gate_g0(zona)))
    gates.append(("Г1 хэш коммита существует", *gate_g1(stroka_kommit)))
    g2_ok, g2_msg, g2_put = gate_g2(stroka_artefakt)
    gates.append(("Г2 строка АРТЕФАКТ заполнена", g2_ok, g2_msg))
    gates.append(("Г3 артефакт не старше источника", *gate_g3(g2_put if g2_ok else None, zahod_path)))
    gates.append(("Г4 секции отчёта заполнены", *gate_g4(tekst)))
    gates.append(("Г5 уроки исполнителя имеют ЦЕНА:", *gate_g5(tekst)))
    g6_ok, g6_msg, g6_sovpadeniya = gate_g6(arka)
    gates.append(("Г6 урок в дневнике без пары в доме уроков", g6_ok, g6_msg))
    voprosy_dlya_ocheredi = sekciya(tekst, "ВОПРОСЫ")
    ochered = parse_ochered(voprosy_dlya_ocheredi or "")
    gates.append(("Г7 пункт очереди отмечен доставленным, а следа нет", *gate_g7(ochered)))

    print("═══ МАШИННЫЕ ГЕЙТЫ ═══")
    krasnyh = 0
    for nazvanie, ok, msg in gates:
        znak = "✅" if ok else "❌"
        if not ok:
            krasnyh += 1
        for i, stroka in enumerate(str(msg).splitlines() or [""]):
            print(f"{znak} {nazvanie}: {stroka}" if i == 0 else f"   {stroka}")

    if g6_sovpadeniya:
        print("\n   Совпадения «урок» в SESSIYA.md (для сверки, все — не только красные):")
        for s in g6_sovpadeniya:
            print(f"   · {s}")

    print(f"\nГейтов зелёных: {len(gates) - krasnyh} из {len(gates)}.")

    print("\n═══ ПЕЧАТЬ ДЛЯ РУК — не гейт, список к разнесению ═══")

    # Часть A: отставание дневника — ВСЕГДА печатается, включая полный зелёный
    # прогон и случай недоступного транскрипта (молчание неотличимо от «всё
    # разнесено» — ровно тот класс потерь, против которого механизм строится).
    print("\n-- Дневник арки: отставание от транскрипта (печать всегда, не гейт) --")
    sost = dnevnik.sostoyanie(str(arka))
    if not sost["dostupno"]:
        print(f"   сверка недоступна: {sost['prichina']}")
    elif not sost["nepokrytye"]:
        print(f"   дневник полон: покрыто {sost['pokryto']} из {sost['vsego']} реплик владельца")
    else:
        print(f"   дневник неполон: покрыто {sost['pokryto']} из {sost['vsego']} реплик владельца")
        for nom, t in sost["nepokrytye"]:
            print(f"   · {nom}: {t[:200]}")

    voprosy = sekciya(tekst, "ВОПРОСЫ")
    print("\n-- ВОПРОСЫ исполнителя --")
    print(voprosy if voprosy else "(пусто)")

    nedostavlennye = [p for p in ochered if p["dostavleno"].strip().lower() == "нет"]
    print(f"\n-- Пункты очереди (ДОМ/ДОСТАВЛЕНО), недоставленные ({len(nedostavlennye)}) --")
    if nedostavlennye:
        for p in nedostavlennye:
            print(f"   · {p['n']}. {p['tekst']} — ДОМ: {p['dom']}")
    else:
        print("   (пунктов очереди без доставки не найдено)")

    uroki = sekciya(tekst, "УРОКИ ФАБРИКЕ")
    print("\n-- УРОКИ ФАБРИКЕ исполнителя (переносить не надо — прочитать обязан) --")
    print(uroki if uroki else "(пусто)")

    otchet = sekciya(tekst, "ОТЧЁТ")
    chisla = chislovye_stroki(otchet)
    print(f"\n-- Числовые утверждения отчёта об артефакте ({len(chisla)}) — воспроизвести командой на живом файле --")
    if chisla:
        for s in chisla:
            print(f"   · {s}")
    else:
        print("   (числовых утверждений не найдено)")

    print("\n-- Охват у вердикта (часть C3, печать) --")
    if ohvat_polozhitelnogo(otchet):
        print("   форма «X из Y» в ## ОТЧЁТ найдена")
    else:
        print("   ⚠ в ## ОТЧЁТ нет ни одной формы «X из Y» — напомнить: и положительный вердикт несёт охват в себе")

    tihoe = tihij_nedobor(otchet)
    print(f"\n-- Тихий недобор (часть C2, печать) — слов «не успел/частично/осталось/не сделал»: {len(tihoe)} --")
    for s in tihoe:
        print(f"   · {s}")

    if stroka_kommit:
        m_khash = re.search(r'\b[0-9a-f]{6,40}\b', stroka_kommit)
        if m_khash:
            print("\n-- Соблюдение границ зоны (часть C1, печать) --")
            print(f"   {granicy_zony(tekst, m_khash.group(0))}")

    print("\n-- Чек-лист оставшихся шагов канона --")
    print(CHEKLIST)

    if krasnyh:
        print(f"\n❌ ПРИЁМКА: {krasnyh} гейт(ов) из {len(gates)} красные — отчёт не принят.")
        return 1
    print(f"\n✅ ПРИЁМКА: все {len(gates)} машинных гейтов зелёные. "
          f"Печать для рук выше — разнести руками.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
