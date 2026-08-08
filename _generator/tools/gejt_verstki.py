#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TOOL-CONTRACT: called-by-hand — ФАЗА 2 конвейера (там решаются `tip_verstki`,
# `liniya`, `zagolovok_na_ekrane`), перед переходом к тексту слайдов.
# 🔴 Маркер здесь НЕ означает «звать необязательно» и взят НЕ как дешёвый: строка
# фазы в `bootstrap_lekcii.LIFECYCLE_TMPL` — ДОЛГ с адресом (заход
# `gigiena-i-svedenie`, `## ВОПРОСЫ` п.1), она лежит в чужой зоне
# `_generator/sborka/**`. И сама по себе она гейт бы не позеленила: охват
# `check_tool_contract.has_live_trigger()` — это `_generator/tools/*.py`, файлы
# ВЕРХНЕГО уровня `_generator/` и `.githooks/*`; подпапка `_generator/sborka/`
# в него не входит. Замер 09.08: у `gejt_vmeshcheniya.py` строка «ФАЗА 3.9» в
# LIFECYCLE есть, а `grep` по охвату даёт 0 — зелёный он тоже маркером.
"""ГЕЙТ ВЁРСТКИ — вёрстка слайда решена и обоснована, а не оставлена «по умолчанию».

    python3 _generator/tools/gejt_verstki.py <лекция>
    python3 _generator/tools/gejt_verstki.py <лекция> --tiho   # только код возврата

Код возврата: 0 — красных нет (предупреждения не валят), 1 — есть красное. Годится в ворота.

ЗАЧЕМ. Разбор Лекции 2 владельцем по слайдам (заход `verstka-v-faze-1`,
`_studio/zhurnal/2026-08-07_arhitektura-slajdov/POMARKI-SBORKA-L2.md`) показал: большинство
претензий были не про текст и не про вёрстку саму по себе, а про решения, которые никто не
принимал — тип вёрстки стоял «по умолчанию» (9 `polosa_vertikalnaya` из 15 слайдов подряд), полоса
стояла пустая (`izomorfizm`: `polosa_vertikalnaya` + `illustracii: []`), заголовок не использовался
НИ РАЗУ (`zagolovok_na_ekrane: ""` 15 из 15). Доктрина — `disciplina/skills/slajdy/SKILL.md`.

Три проверки:
  Д2 (красное) — `tip_verstki` начинается на `polosa_`, а `illustracii: []`: полоса, класть в
      которую нечего;
  Д6 (красное) — `obosnovanie_verstki` пусто или отсутствует при ЛЮБОМ `tip_verstki`: тип
      проставлен, но не сказано, почему именно он;
  Д5 (предупреждение, НЕ красное) — `zagolovok_na_ekrane` пусто без `zagolovok_snyat_namerenno: da`:
      заголовок не решён осознанно, а просто не тронут.

Д1 (выбор типа по объёму текста) НЕ гейтится числом — границ «много/среднее/мало» пока нет (даст
`smeta.py` захода `svedenie-i-smeta`); печатается только справкой — тип вёрстки рядом с числом
блоков «Текст слайда — сжато», чтобы расхождение бросалось в глаза до появления чисел.

Д4 (обложка/визитка/финальный вставляет генератор) — гейтом НЕ проверяется вовсе, ни здесь, ни где
угодно в этом инструменте: раз их вставляет `deck.py`, требовать их от авторских карточек значит
краснеть на здоровой лекции (см. `SKILL.md`, «СПЕКА ДЛЯ ГЕНЕРАТОРА»).

Свой минимальный парсер шапки — той же идиомой, что `gejt_illyustracij.py` (Я5 этого захода): НЕ
импортирует `_generator/sborka/formaty.py` (чужая зона, и идиома семьи — stdlib без сторонних
зависимостей внутри `_generator/tools/`). Разбирает только плоские `key: value` строки шапки —
списковые поля (`illustracii`) легальны ТОЛЬКО инлайн (`SKILL.md`/`formaty.py`), вложенные блоки
(`opiraetsya_na:` и т. п.) этому гейту не нужны и не разбираются.

Идиома семьи (`_generator/DVIZHKI.md`): stdlib, детерминизм, без сети и pip, `exit 1` при красном.

Гейт НЕ встроен в сборку (`deck.py`) — вызывается отдельной командой (см. маркер вверху файла:
ФАЗА 2). Охват тестами — `_generator/tools/fixtures/verstki/PROGNAT.sh` (маркер
`TOOL-CONTRACT-COVERS`, тот же механизм, которым уже пользуется `fixtures/illyustracii/PROGNAT.sh`).
🔴 Охват тестами и живая точка вызова — РАЗНЫЕ вещи, и раньше здесь было написано, что фикстура
служит точкой вызова: `has_live_trigger()` папку `fixtures/` не смотрит вовсе, поэтому гейт был
красным при живой фикстуре (замер 09.08, заход `gigiena-i-svedenie`).
"""
import re
import sys
from pathlib import Path

FRONT_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
LIFECYCLE_RE = re.compile(r"^<!--(.*?)-->\s*", re.S)
ILL_RE = re.compile(r"^\[(.*)\]\s*$")
TEXT_SECTION_RE = re.compile(r"^## Текст слайда — сжато\s*\n(.*?)(?=^## |\Z)", re.M | re.S)
BLOK_RE = re.compile(r"^### ", re.M)

ZAGLUSHKA = "заполнить"


def _read(p):
    return p.read_text(encoding="utf-8")


def _strip_lifecycle(text):
    m = LIFECYCLE_RE.match(text)
    return text[m.end():] if m else text


def _strip_quotes(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] == '"':
        return s[1:-1]
    return s


def parse_card(text):
    """slaid.md → dict плоских полей шапки, нужных этому гейту. Списковые поля — уже разобранный
    список строк (только инлайн-форма, см. докстринг), либо None, если поле в шапке не найдено."""
    text = _strip_lifecycle(text)
    m = FRONT_RE.match(text)
    if not m:
        raise SystemExit("нет YAML-шапки (---...---)")
    raw = {}
    for line in m.group(1).splitlines():
        line = line.rstrip()
        if not line or line[0] in " \t-":  # вложенные строки (списки/словари) — не top-level поле
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        raw.setdefault(key.strip(), val.strip())

    def spisok(key):
        v = raw.get(key)
        if v is None:
            return None
        im = ILL_RE.match(v)
        if not im:
            return None
        inner = im.group(1).strip()
        if not inner:
            return []
        return [x.strip().strip('"') for x in inner.split(",") if x.strip()]

    return {
        "tip_verstki": raw.get("tip_verstki"),
        "obosnovanie_verstki": _strip_quotes(raw["obosnovanie_verstki"]) if "obosnovanie_verstki" in raw else None,
        "zagolovok_na_ekrane": _strip_quotes(raw["zagolovok_na_ekrane"]) if "zagolovok_na_ekrane" in raw else None,
        "zagolovok_snyat_namerenno": raw.get("zagolovok_snyat_namerenno"),
        "illustracii": spisok("illustracii"),
    }


def nezapolneno(val):
    return val is None or val.strip() == "" or val.strip().lower() == ZAGLUSHKA


def blokov_v_tekste(text):
    text = _strip_lifecycle(text)
    sm = TEXT_SECTION_RE.search(text)
    if not sm:
        return None
    return len(BLOK_RE.findall(sm.group(1)))


def proverit(lekcija_dir):
    """→ (krasnye, preduprezhdenia, spravka) | (None, None, None) — папки лекции нет вовсе."""
    lekcija = Path(lekcija_dir)
    if not lekcija.is_dir():
        return None, None, None
    slajdy_dir = lekcija / "slajdy"
    slaid_files = sorted(slajdy_dir.glob("*/slaid.md")) if slajdy_dir.is_dir() else []

    krasnye = []
    zagolovok_pusto = 0
    spravka = []

    for sp in slaid_files:
        sid = sp.parent.name
        text = _read(sp)
        p = parse_card(text)
        tip = p["tip_verstki"]
        ill = p["illustracii"]

        # Д2 — полоса без иллюстрации
        if tip and tip.startswith("polosa_") and ill == []:
            krasnye.append(("Д2", "%s: %s + illustracii: [] — полоса, класть в которую нечего" % (sid, tip)))

        # Д6 — тип проставлен, обоснование нет
        if tip and nezapolneno(p["obosnovanie_verstki"]):
            krasnye.append(("Д6", "%s: tip_verstki '%s' без obosnovanie_verstki" % (sid, tip)))

        # Д5 — заголовок пуст без осознанного снятия
        if nezapolneno(p["zagolovok_na_ekrane"]) and p["zagolovok_snyat_namerenno"] != "da":
            zagolovok_pusto += 1

        spravka.append((sid, tip or "?", blokov_v_tekste(text)))

    preduprezhdenia = []
    if slaid_files and zagolovok_pusto:
        preduprezhdenia.append(
            "Д5: zagolovok_na_ekrane пусто без zagolovok_snyat_namerenno на %d из %d"
            % (zagolovok_pusto, len(slaid_files)))

    return krasnye, preduprezhdenia, spravka


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    tiho = "--tiho" in sys.argv
    if not args:
        print(__doc__.strip().splitlines()[2])
        sys.exit(2)

    krasnye, preduprezhdenia, spravka = proverit(args[0])

    if spravka is None:
        sys.stderr.write("%s: не папка лекции (путь не существует)\n" % args[0])
        sys.exit(2)

    if not tiho:
        print("── ГЕЙТ ВЁРСТКИ (gejt_verstki) ──")
        print("  %s" % args[0])
        print("  слайдов: %d" % len(spravka))
        print("\n  СПРАВКА Д1 (не гейтится — границы объёма ещё не заданы):")
        for sid, tip, bloki in spravka:
            print("     %-28s %-22s блоков в «Текст слайда — сжато»: %s"
                  % (sid, tip, bloki if bloki is not None else "—"))
        if preduprezhdenia:
            print("\n  ⚠ ПРЕДУПРЕЖДЕНИЯ:")
            for p in preduprezhdenia:
                print("     %s" % p)
        print("\n  ЧЕГО ЭТОТ ГЕЙТ НЕ ПРОВЕРЯЕТ:")
        print("     · [Д1] границы «много/среднее/мало» в словах текста — заход svedenie-i-smeta, smeta.py")
        print("     · [Д3] иллюстрация действительно отвечает своему zakaz.md — вкус, не число")
        print("     · [Д4] обложка/визитка/финальный слайд — свойство сборки (deck.py), не карточки")

    if krasnye:
        if not tiho:
            print("\n  ✗ КРАСНЫЙ — замечаний %d:" % len(krasnye))
            for k, v in krasnye:
                print("     %-3s %s" % (k, v))
        sys.exit(1)

    if not tiho:
        print("\n  ✓ ЗЕЛЁНЫЙ")
    sys.exit(0)


if __name__ == "__main__":
    main()
