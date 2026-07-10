#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_docs — baseline-гейт целостности CANON-доков курса (НЕ ручной субагент).

ЗАЧЕМ. Контент-память курса (концепт, тезисы, кросс-линки) держится на дисциплине
регистрации в `NAVIGATION.md`, но дисциплину никто не проверял детерминированно.
Этот инструмент делает то же, что живой аудит, но бесплатно и с точным адресом
нарушения. Идиома и метод — порт `spetsmat/spetsmat_db/tools/check_docs.py`
(адаптирован под структуру этого проекта, пути не копировались).

МЕТОД: только stdlib, БЕЗ исполнения чужого кода, БЕЗ сети/БД, детерминированно
(всё сортируется). Запуск: `python3 tools/check_docs.py` (из любого каталога —
корень репо вычисляется от файла). Ненулевой выход при ЛЮБОМ нарушении.

CANON-доки (скоуп проверок 1/2/4): root `*.md`, `1-START-HERE/*.md`, `0-koncept/**`,
`2-idei/*.md`, `biblioteka/*.md`, `istochnik/*.md`. Исключены: `zhurnal/**`,
`snapshots/**`, `_arhiv/**`, `**/_out/**`, `tools/**` — история/генерат, эти доки
живут по своим правилам (арки не ревизуются задним числом).

ПРОВЕРКИ:
  1. НЕТ СИРОТ: каждый CANON `.md` упомянут строкой в `NAVIGATION.md`.
  2. ССЫЛКИ ЦЕЛЫ: все repo-относительные пути в CANON-доках резолвятся
     (backtick-пути и markdown-ссылки).
  3. NFC-ИМЕНА: имена файлов нормализованы NFC; коллизия NFD/NFC = fail
     (у проекта translit-правило именно против бага «й/ё» — критично).
  4. НЕТ АБС-ПУТЕЙ ПЕСОЧНИЦЫ (`/Users/`, `/sessions/`, `/mnt/`) в CANON `.md`.
  5. КАРТА↔ФС: папки верхнего уровня из блока «Карта папок» `NAVIGATION.md`
     существуют на диске, и наоборот (каждая реальная папка верхнего уровня
     описана в карте).
"""
import fnmatch
import os
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAVIGATION = ROOT / 'NAVIGATION.md'

# Папки/паттерны — история/генерат, вне скоупа CANON-проверок 1/2/4.
EXCLUDE_DIRS = ('zhurnal', 'snapshots', '_arhiv', 'tools')
EXCLUDE_DIR_NAMES_ANYWHERE = ('_out', '_arhiv')

# CANON-наборы: (базовая папка относительно ROOT или '' для корня, рекурсивно?)
CANON_SPECS = [
    ('', False),            # root *.md
    ('1-START-HERE', False),
    ('0-koncept', True),
    ('2-idei', False),
    ('biblioteka', False),
    ('istochnik', False),
]

PATH_EXTS = ('md', 'py', 'json', 'html', 'svg', 'css', 'yml', 'yaml', 'txt', 'js')


def _excluded(rel_parts):
    return any(p in EXCLUDE_DIR_NAMES_ANYWHERE for p in rel_parts)


def canon_md_files():
    """Все CANON `.md` (POSIX-relpath от ROOT), сортировано."""
    out = []
    for base, recursive in CANON_SPECS:
        d = ROOT / base if base else ROOT
        if not d.exists():
            continue
        it = d.rglob('*.md') if recursive else d.glob('*.md')
        for p in it:
            rel = p.relative_to(ROOT)
            parts = rel.parts
            if not base and (parts[0] in EXCLUDE_DIRS or parts[0].startswith('.')):
                continue  # root-скан не должен цеплять zhurnal/snapshots/_arhiv/tools верхнего уровня
            if _excluded(parts):
                continue
            out.append(rel.as_posix())
    return sorted(set(out))


def lineno(text, idx):
    return text.count('\n', 0, idx) + 1


def section(text, start_marker, *end_markers):
    s = text.find(start_marker)
    if s < 0:
        return ''
    rest = text[s + len(start_marker):]
    ends = [rest.find(m) for m in end_markers if rest.find(m) >= 0]
    return rest if not ends else rest[:min(ends)]


# ──────────────────────────────────────────────────────────────────────────────
# 1. НЕТ СИРОТ
# ──────────────────────────────────────────────────────────────────────────────
def check_orphans():
    """Регистрация в NAVIGATION.md — не всегда «файл дословно»: индекс легально
    покрывает лекции глобом (`istochnik/L*.md`) и историю списком голых имён без
    расширения в прозе. Признаём зарегистрированным, если basename/stem
    встречается ГДЕ-ЛИБО в тексте (backtick или голым текстом), ИЛИ путь/basename
    подпадает под backtick-токен с `*` (glob)."""
    problems = []
    nav = NAVIGATION.read_text(encoding='utf-8')
    nav_no_fences = re.sub(r'```.*?```', ' ', nav, flags=re.DOTALL)  # ``` карта-блок не путать с инлайн `code`
    glob_patterns = [t for t in re.findall(r'`([^`]+)`', nav_no_fences) if '*' in t]
    for rel in canon_md_files():
        base = rel.split('/')[-1]
        stem = base.rsplit('.', 1)[0]
        if base in nav or stem in nav:
            continue
        if any(fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(base, pat.split('/')[-1])
               for pat in glob_patterns):
            continue
        problems.append(f'{rel}: документ НЕ упомянут в NAVIGATION.md (сирота)')
    return problems


# ──────────────────────────────────────────────────────────────────────────────
# 2. ССЫЛКИ ЦЕЛЫ
# ──────────────────────────────────────────────────────────────────────────────
_URL_RE = re.compile(r'https?://\S+|mailto:\S+|/(?:mnt|sessions|home)/\S+')
_PATH_RE = re.compile(
    r'(?<![\w/.])((?:\.\./)*[\w.\-А-Яа-яЁё]+(?:/[\w.\-А-Яа-яЁё]+)+\.(?:' +
    '|'.join(PATH_EXTS) + r'))(?!\w)')
_BARE_HOST_RE = re.compile(r'^(?:\.\./)*[a-z0-9-]+(?:\.[a-z0-9-]+)*\.[a-z]{2,}/', re.IGNORECASE)


def _resolves(token, docdir):
    """Путь резолвится относительно корня репо, каталога дока или любой папки
    верхнего уровня (доки часто пишут путь сокращённо)."""
    bases = [ROOT, docdir] + [ROOT / n for n in os.listdir(ROOT)
                               if (ROOT / n).is_dir() and not n.startswith('.')]
    for base in bases:
        if os.path.exists(os.path.normpath(os.path.join(str(base), token))):
            return True
    return False


def _is_url_text(token, line):
    return any(token in u for u in _URL_RE.findall(line))


def _is_bare_domain_citation(token):
    return bool(_BARE_HOST_RE.match(token))


def check_links():
    problems = []
    for rel in canon_md_files():
        src = ROOT / rel
        text = src.read_text(encoding='utf-8')
        lines = text.splitlines()
        clean = _URL_RE.sub(' ', text)
        docdir = src.parent
        seen = set()
        for m in _PATH_RE.finditer(clean):
            token = m.group(1)
            if any(c in token for c in '<>*,…{}()') or '...' in token:
                continue
            if token in seen:
                continue
            seen.add(token)
            if _is_bare_domain_citation(token):
                continue
            ln = lineno(text, text.find(token) if token in text else m.start())
            if 0 < ln <= len(lines) and _is_url_text(token, lines[ln - 1]):
                continue
            if not _resolves(token, docdir):
                problems.append(f'{rel}:{ln}: битый путь `{token}` '
                                 '(не резолвится от корня/каталога дока/папки верхнего уровня)')
    return sorted(problems)


# ──────────────────────────────────────────────────────────────────────────────
# 3. ИМЕНА ФАЙЛОВ — СТРОГО NFC (анти-фантом-дубли)
# ──────────────────────────────────────────────────────────────────────────────
# macOS раскладывает «й»/«ё» в NFD → git/скрипты видят ДРУГУЮ цепочку байт →
# фантомные дубли-сироты. Скоуп: CANON `.md` (доковая целостность — не файлы-
# источники вроде PDF-книг в biblioteka/, те вне мандата этого захода).
def _name_guard_files():
    return sorted((rel, rel.split('/')[-1]) for rel in canon_md_files())


def check_nfc_names():
    problems = []
    seen = {}
    for disp, base in _name_guard_files():
        nfc = unicodedata.normalize('NFC', base)
        if nfc != base:
            problems.append(f'{disp}: имя файла в форме NFD (разложенные «й»/«ё») — перекодировать в NFC')
        key = (os.path.dirname(disp), nfc)
        if key in seen:
            problems.append(f'{disp}: дубль-по-нормализации с `{seen[key]}` (совпадают после NFC) — оставить одно')
        else:
            seen[key] = disp
    return sorted(problems)


# ──────────────────────────────────────────────────────────────────────────────
# 4. НЕТ АБС-ПУТЕЙ ПЕСОЧНИЦЫ
# ──────────────────────────────────────────────────────────────────────────────
_ABS_PATH_RE = re.compile(r'/(?:mnt/user-data|Users|sessions|home)/[\w.\-]+')
_WEB_URL_RE = re.compile(r'https?://\S+|mailto:\S+')


def check_abs_paths():
    problems = []
    for rel in canon_md_files():
        src = ROOT / rel
        text = src.read_text(encoding='utf-8')
        for i, ln in enumerate(text.splitlines(), 1):
            m = _ABS_PATH_RE.search(_WEB_URL_RE.sub(' ', ln))
            if m:
                problems.append(f'{rel}:{i}: захардкоженный абсолютный путь `{m.group(0)}` '
                                 '(машинно-зависимый — заменить на относительный)')
    return sorted(problems)


# ──────────────────────────────────────────────────────────────────────────────
# 6. ID-ЦЕЛОСТНОСТЬ: KONCEPT ↔ ЛЕКЦИИ (блок-синхрон, `sync-koncept-lekcii.md`)
# ──────────────────────────────────────────────────────────────────────────────
KONCEPT = ROOT / '0-koncept' / 'KONCEPT.md'
ISTOCHNIK = ROOT / 'istochnik'
_ANCHOR_RE = re.compile(r'\{L:([\w-]+)\}')
_FRONTMATTER_ID_RE = re.compile(r'^id:\s*(\S+)\s*$', re.MULTILINE)
_FRONTMATTER_PORYADOK_RE = re.compile(r'^poryadok:\s*(\d+)\s*$', re.MULTILINE)


def _lecture_frontmatter():
    """(id, poryadok, rel_path) для каждого istochnik/L*.md."""
    out = []
    for p in sorted(ISTOCHNIK.glob('L*.md')):
        text = p.read_text(encoding='utf-8')
        m_id = _FRONTMATTER_ID_RE.search(text)
        m_por = _FRONTMATTER_PORYADOK_RE.search(text)
        rel = p.relative_to(ROOT).as_posix()
        out.append((m_id.group(1) if m_id else None, m_por.group(1) if m_por else None, rel))
    return out


def check_id_sync():
    problems = []
    if not KONCEPT.exists():
        return [f'{KONCEPT.relative_to(ROOT)}: файл не найден']
    koncept_text = KONCEPT.read_text(encoding='utf-8')
    koncept_ids = _ANCHOR_RE.findall(koncept_text)
    lectures = _lecture_frontmatter()
    lecture_ids = [lid for lid, _, _ in lectures if lid]
    id_to_path = {lid: rel for lid, _, rel in lectures if lid}

    # (1) множества id — точное совпадение 7↔7
    koncept_set, lecture_set = set(koncept_ids), set(lecture_ids)
    missing_in_koncept = sorted(lecture_set - koncept_set)
    extra_in_koncept = sorted(koncept_set - lecture_set)
    if missing_in_koncept:
        problems.append(f'{KONCEPT.relative_to(ROOT)}: нет якоря {{L:id}} для лекций {missing_in_koncept}')
    if extra_in_koncept:
        problems.append(f'{KONCEPT.relative_to(ROOT)}: якорь(я) {extra_in_koncept} не резолвятся ни в одну лекцию')
    if len(koncept_ids) != len(set(koncept_ids)):
        dupes = sorted({x for x in koncept_ids if koncept_ids.count(x) > 1})
        problems.append(f'{KONCEPT.relative_to(ROOT)}: дублирующиеся якоря {{L:id}} для {dupes}')

    # (2) poryadok уникальны в 1..7
    poryadki = [por for _, por, _ in lectures if por is not None]
    expected = {str(n) for n in range(1, 8)}
    got = set(poryadki)
    if len(poryadki) != len(set(poryadki)):
        dupes = sorted({x for x in poryadki if poryadki.count(x) > 1})
        problems.append(f'istochnik/L*.md: дублирующиеся poryadok {dupes}')
    if got != expected:
        problems.append(f'istochnik/L*.md: poryadok должны быть 1..7 без пропусков, получено {sorted(got, key=lambda x: int(x))}')
    missing_por = [rel for lid, por, rel in lectures if por is None]
    if missing_por:
        problems.append(f'istochnik/L*.md: нет поля poryadok в {sorted(missing_por)}')

    # (3) каждый {L:id} резолвится в реально существующий файл лекции
    unresolved = sorted(a for a in koncept_ids if a not in id_to_path)
    if unresolved:
        problems.append(f'{KONCEPT.relative_to(ROOT)}: якорь(я) {unresolved} не резолвятся в файл лекции')

    return problems


# ──────────────────────────────────────────────────────────────────────────────
# 5. КАРТА↔ФС
# ──────────────────────────────────────────────────────────────────────────────
def _real_top_dirs():
    skip = {'__pycache__'}
    return sorted(p.name for p in ROOT.iterdir()
                  if p.is_dir() and p.name not in skip and not p.name.startswith('.'))


def check_map_vs_fs():
    problems = []
    nav = NAVIGATION.read_text(encoding='utf-8')
    layout = section(nav, '## Карта папок', '## ')
    block = section(layout, '```', '```')
    if not block:
        return [f'{NAVIGATION.relative_to(ROOT)}: не найден код-блок «Карта папок»']

    mapped = set()
    for ln in block.splitlines():
        mm = re.match(r'^(\S+)/', ln)
        if not mm:
            continue
        mapped.add(mm.group(1))

    for name in mapped:
        if not (ROOT / name).exists():
            problems.append(f'{NAVIGATION.relative_to(ROOT)} «Карта папок»: `{name}/` описана, но НЕ существует')

    for d in _real_top_dirs():
        if d not in mapped:
            problems.append(f'{NAVIGATION.relative_to(ROOT)} «Карта папок»: реальная папка `{d}/` НЕ описана')
    return sorted(problems)


CHECKS = [
    ('сироты (CANON ↔ NAVIGATION.md)', check_orphans),
    ('ссылки целы', check_links),
    ('имена файлов NFC (нет NFD/дублей-по-нормализации)', check_nfc_names),
    ('нет абс. путей песочницы (CANON-доки)', check_abs_paths),
    ('карта папок ↔ реальность', check_map_vs_fs),
    ('id-целостность KONCEPT ↔ лекции', check_id_sync),
]


def main():
    total = 0
    for title, fn in CHECKS:
        probs = fn()
        if probs:
            total += len(probs)
            print(f'✗ {title}: {len(probs)} нарушени(й)')
            for p in probs:
                print(f'    {p}')
        else:
            print(f'✓ {title}')
    if total:
        print(f'\nИТОГ: {total} нарушени(й) — доки разошлись с реальностью.')
        raise SystemExit(1)
    print('\nИТОГ: доки соответствуют реальности ✓')


if __name__ == '__main__':
    main()
