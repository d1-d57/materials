#!/usr/bin/env python3
"""ГЕЙТ РАЗБОРА: неразобранные КЛАССЫ инцидентов коммита краснеют сами.

    python3 _generator/tools/check_incidenty.py
    python3 _generator/tools/check_incidenty.py --incidenty <путь> --verdikty <путь>
    python3 _generator/tools/check_incidenty.py --status      # одна строка для doctor

Код возврата: 0 — все живые классы разобраны, 1 — есть класс без вердикта
(или вердикт сломан), 2 — гейт не отработал (файл не читается).

ЗАЧЕМ. `git_zona.py` сам пишет строку в `INCIDENTY.md` при каждом сорванном
коммите — сбор работает. Разгрузки не было: 90 строк за 10 дней, 89 висят
«открыт», ни один инструмент не спрашивал «а разобрали?». Разбор владелец
попросил вести по КЛАССАМ (12 штук), а не по строкам (их будет всё больше) —
дом вердиктов класса `_studio/zhurnal/_INFRA-git/VERDIKTY.md`, формат там же.

Классификация — функция `cls()` ниже — взята ДОСЛОВНО из `RAZBOR-povtorov.md
§6` и НЕ переизобретена: разойдись ключи — разойдутся и вердикты, и гейт станет
сверять несуществующие классы. Известный баг классификатора (падеж «путей»
вместо «пути» в проверке для класса J) сохранён как есть — см. `## ВОПРОСЫ`
захода `kod_gejt-razbora.md`; исправление вне зоны этого захода.
"""
import argparse
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

REPO = Path(os.environ.get("GIT_ZONA_REPO") or Path(__file__).resolve().parents[2])
INCIDENTY_REL = "_studio/zhurnal/_INFRA-git/INCIDENTY.md"
VERDIKTY_REL = "_studio/zhurnal/_INFRA-git/VERDIKTY.md"
ZAHODY_DOM = "_studio/zhurnal"          # где искать файлы заходов по имени
NE_SOBRAN = "<не собран>"

SVEZHEST_DNEJ = 7    # владелец: пять дней между разборами — нормальный ритм
MOLCHANIE_DNEJ = 21  # три недели молчания — уже не «руки не дошли»


def cls(s):
    """ДОСЛОВНО из RAZBOR-povtorov.md §6 — не переизобретать (см. докстринг)."""
    b = s.split('·')[2].strip(); low = s.lower()
    if b.startswith('коммит с --no-verify'):
        if 'karta' in low and ('read-only' in low or 'регистр' in low): return 'A регистрация .md vs зона'
        if 'playwright' in low or 'chrome-headless' in low: return 'B окружение песочницы'
        return 'C прочий чужой долг'
    if b.startswith('merge'):
        if 'грязные пути' in b: return 'D merge отбит грязным деревом'
        if 'конфликт' in b: return 'E конфликт путей'
        return 'F merge без диагноза'
    if 'не целиком' in b: return 'G коммит не целиком'
    if 'без плана при грязном' in b: return 'H commit без плана'
    if 'план не готов' in b: return 'I план битый'
    if 'путей, которых нет' in b: return 'J пути не существуют'
    if 'мусорными аргументами' in b: return 'K мусорные аргументы'
    if 'запись в .git' in b: return 'L песочница'
    return b


def klassifikaciya(text):
    """`{класс: [ГГГГ-ММ-ДД, ...]}` по всем строкам-инцидентам."""
    rows = [l for l in text.splitlines(keepends=True) if l.startswith('- 20')]
    d = {}
    for r in rows:
        d.setdefault(cls(r), []).append(r[2:12])
    return d


VERDIKT_RE = re.compile(
    r"^-\s+(?P<klyuch>.+?)\s+·\s+вердикт:\s+(?P<verdikt>.+?)\s+·\s+"
    r"дата данных:\s+(?P<data>\d{4}-\d{2}-\d{2})\s*$"
)


class Verdikt:
    __slots__ = ("tip", "zahod", "prichina", "zakryt_data", "data_dannyh", "syraya")

    def __init__(self, tip, data_dannyh, syraya, zahod=None, prichina=None, zakryt_data=None):
        self.tip = tip
        self.zahod = zahod
        self.prichina = prichina
        self.zakryt_data = zakryt_data
        self.data_dannyh = data_dannyh
        self.syraya = syraya


def razobrat_verdikt(telo, data_dannyh, syraya):
    """`телo` — часть после `вердикт: `. Пустая причина/имя — сломанный вердикт (None)."""
    if telo.startswith('дефект → заход '):
        imya = telo[len('дефект → заход '):].strip().strip('`')
        if not imya:
            return None
        return Verdikt('дефект', data_dannyh, syraya, zahod=imya)
    if telo.startswith('шум: '):
        prichina = telo[len('шум: '):].strip()
        if not prichina:
            return None
        return Verdikt('шум', data_dannyh, syraya, prichina=prichina)
    if telo.startswith('закрыт '):
        d = telo[len('закрыт '):].strip()
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
            return None
        return Verdikt('закрыт', data_dannyh, syraya, zakryt_data=d)
    return None


def parse_verdikty(text):
    """`{класс: Verdikt}`. Строка не разбирается — класс просто отсутствует
    в словаре (равносильно «вердикта нет», гейт увидит его сам)."""
    out = {}
    for ln in text.splitlines():
        m = VERDIKT_RE.match(ln.rstrip())
        if not m:
            continue
        v = razobrat_verdikt(m.group('verdikt'), m.group('data'), ln)
        if v is not None:
            out[m.group('klyuch').strip()] = v
    return out


def najti_zahod(imya):
    """Первый файл с таким именем под `_studio/zhurnal/` — заходы живут в разных арках."""
    dom = REPO / ZAHODY_DOM
    if not dom.exists():
        return None
    hits = sorted(dom.rglob(imya))
    return hits[0] if hits else None


def zahod_prinyat(put):
    """Заход принят — в файле есть `## ОТЧЁТ` и непустая строка `**КОММИТ:**`."""
    try:
        text = put.read_text(encoding="utf-8")
    except OSError:
        return False
    if '## ОТЧЁТ' not in text:
        return False
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith('**КОММИТ:**'):
            ostatok = s[len('**КОММИТ:**'):].strip()
            if ostatok:
                return True
    return False


def dnej_nazad(data_str, segodnya):
    return (segodnya - datetime.strptime(data_str, "%Y-%m-%d").date()).days


def ocenit(incidenty_text, verdikty_text, segodnya=None):
    """Возвращает (rc, [строки находок]) — три случая из ## ЗАДАЧА §2, ничего сверх."""
    segodnya = segodnya or date.today()
    klassy = klassifikaciya(incidenty_text)
    verdikty = parse_verdikty(verdikty_text)
    findings = []

    for klyuch, daty in klassy.items():
        starejshaya = min(daty)
        vozrast = dnej_nazad(starejshaya, segodnya)
        v = verdikty.get(klyuch)

        if v is None:
            if vozrast > SVEZHEST_DNEJ:
                findings.append(
                    f"класс «{klyuch}»: {len(daty)} повтор(ов), старейшая строка "
                    f"{vozrast} дней назад, вердикта нет — строка для VERDIKTY.md:\n"
                    f"   - {klyuch} · вердикт: дефект → заход {NE_SOBRAN} · "
                    f"дата данных: {segodnya.isoformat()}"
                )
            continue

        if v.tip != 'дефект':
            continue

        if v.zahod == NE_SOBRAN:
            continue

        put = najti_zahod(v.zahod)
        if put is None:
            findings.append(
                f"класс «{klyuch}»: вердикт «дефект → заход {v.zahod}» — "
                f"файла {v.zahod} нет на диске под {ZAHODY_DOM}/"
            )
            continue

        vozrast_verdikta = dnej_nazad(v.data_dannyh, segodnya)
        if vozrast_verdikta > MOLCHANIE_DNEJ and not zahod_prinyat(put):
            findings.append(
                f"класс «{klyuch}»: вердикт «дефект → заход {v.zahod}» старше "
                f"{MOLCHANIE_DNEJ} дней ({vozrast_verdikta} дн., дата данных "
                f"{v.data_dannyh}), а заход не принят (нет ## ОТЧЁТ с непустой "
                f"строкой **КОММИТ:**)"
            )

    return (1 if findings else 0), findings


def status_line(incidenty_text, verdikty_text, segodnya=None):
    """Одна строка для `git_zona.py doctor` — печать, не гейт."""
    segodnya = segodnya or date.today()
    klassy = klassifikaciya(incidenty_text)
    verdikty = parse_verdikty(verdikty_text)
    bez = [(k, min(d)) for k, d in klassy.items() if k not in verdikty]
    if not bez:
        return "классов инцидентов без вердикта: 0"
    starejshij = max(dnej_nazad(d, segodnya) for _, d in bez)
    return f"классов инцидентов без вердикта: {len(bez)}, старейшему {starejshij} дней"


def citat(put):
    try:
        return put.read_text(encoding="utf-8")
    except OSError as e:
        print(f"❌ {put}: не читается ({e.__class__.__name__}) — гейт не отработал")
        sys.exit(2)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--incidenty", default=str(REPO / INCIDENTY_REL))
    ap.add_argument("--verdikty", default=str(REPO / VERDIKTY_REL))
    ap.add_argument("--status", action="store_true",
                     help="печатает одну строку для doctor и выходит с rc=0")
    args = ap.parse_args()

    incidenty_text = citat(Path(args.incidenty))
    verdikty_text = citat(Path(args.verdikty))

    if args.status:
        print(status_line(incidenty_text, verdikty_text))
        return 0

    rc, findings = ocenit(incidenty_text, verdikty_text)
    if not findings:
        klassy = klassifikaciya(incidenty_text)
        print(f"✅ разбор инцидентов: {len(klassy)} класс(ов), вердиктов не хватает у 0")
        return 0

    print(f"🔴 РАЗБОР ИНЦИДЕНТОВ: {len(findings)} находк(и/у) — "
          f"пополни {VERDIKTY_REL}:")
    for f in findings:
        print(f"\n- {f}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
