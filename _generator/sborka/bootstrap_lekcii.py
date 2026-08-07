#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Порождает структуру лекции — карточку лекции и по карточке на слайд, СО ВСЕМИ
полями и пометкой «заполнить» (Э3 захода kartochka-i-sborka). Требование владельца
дословно: «скрипт создаёт документ, в котором есть конкретные строки — анкету.
И поставить гейт: если что-то не заполнено, дальше не идём» (`gejt_kartochki.py`).

🔴 ДВА ХОДА (заход `vhod-fazy-1`, Э2 — разрыв цикла фазы 1). Шаг 3 процедуры фазы 1
(«породить анкеты скриптом») идёт ДО подфаз 5.1–5.4: имена слайдов ещё не названы
(они рождаются в 5.2, адрес — `slide_order` в `brief.md`, не `INTERVYU.md`), а
`--slajdy` требовал их СРАЗУ — цикл, а не вход. Разорван на два вызова ОДНОГО и
того же скрипта, без флага:

  ход «каркас» (шаг 3, ДО разговора):
    python3 _generator/sborka/bootstrap_lekcii.py <лекция-dir>
    → brief.md с пустым `slide_order` + INTERVYU.md со скелетом разделов;
      slajdy/ не заводится — имён ещё нет.

  ход «досыпать» (после подфазы 5.2, когда `slide_order` в brief.md заполнен):
    python3 _generator/sborka/bootstrap_lekcii.py <лекция-dir>
    → та же команда: увидев brief.md на месте, читает его `slide_order` и
      дописывает НЕДОСТАЮЩИЕ папки слайдов. Идемпотентно — существующий
      `slaid.md` не трогает.

`--slajdy id1,id2,id3` остаётся ЗАКОННЫМ входом (фикстуры, случай, когда список
известен заранее целиком) — тогда всё делается ОДНИМ вызовом, как раньше.

Раскладка — Я2: `<лекция>/brief.md` (манифест порядка + карточка лекции, Я1 §1) +
`<лекция>/slajdy/<id>/slaid.md` на каждый слайд (Я1 §2) + `<лекция>/INTERVYU.md`
(раздел `## Части` — выход 5.1, `## Предполагаемые иллюстрации` — выход 5.4;
формат специфицирован частично в `SKILL.md` ФАЗА 1 и грепается верификатором
`verifikatory/faza-1-intervyu.md` — переиспользуем эти два заголовка дословно, не
изобретаем формат заново).

Идемпотентно по слайдам: существующий `slaid.md` НЕ перезаписывается (не теряет
работу владельца), считается «уже есть», не «создано». `brief.md` и `INTERVYU.md`
целиком перезаписать может ТОЛЬКО `--force`, и только на ходе «каркас» (иначе отказ
— не затирать лекцию, которая уже что-то накопила по фазам)."""
import argparse
import sys
from pathlib import Path

SBORKA = Path(__file__).resolve().parent
_GENERATOR = SBORKA.parent
sys.path.insert(0, str(SBORKA))
sys.path.insert(0, str(_GENERATOR))
from formaty import ZAPOLNIT  # noqa: E402
from build_deck import parse_brief  # noqa: E402 (READ-ONLY импорт — единый парсер brief.md)

# Поля лекции — Я1 §1 целиком (кроме двух, вычисляемых при бутстрапе: id/slide_order
# несут структуру, не замысел, заполняются ЗДЕСЬ, а не владельцем).
POLYA_LEKCII = ("title", "dlya_kogo", "zhanr", "dlitelnost_minut",
                "skvoznaya_liniya")

SLIDE_CARD_TMPL = """---
imya: %(imya)s
nazvanie: %(zap)s
zagolovok_na_ekrane: %(zap)s
zachem: %(zap)s
akcent: %(zap)s
kommentarij_lektoru: %(zap)s
minuty: %(zap)s
vazhnost: %(zap)s
byudzhet_slov: %(zap)s
tip_verstki: %(zap)s
liniya: %(zap)s
illustracii: []
vvodit: []
opiraetsya_na: []
bez_opredeleniya_namerenno: []
status: v_deke
---
"""


def _slide_card_text(imya):
    return SLIDE_CARD_TMPL % {"imya": imya, "zap": ZAPOLNIT}


INTERVYU_TMPL = """## Части

%(zap)s

## Предполагаемые иллюстрации

%(zap)s
"""


def _intervyu_text():
    return INTERVYU_TMPL % {"zap": ZAPOLNIT}


def _brief_text(lekcija_id, slide_ids):
    order = "\n".join("  - %s" % s for s in slide_ids)
    polya = "\n".join("%s: %s" % (k, ZAPOLNIT) for k in POLYA_LEKCII)
    return (
        "---\n"
        "id: %(id)s\n"
        "canvas: 1440x810\n"
        "slide_order:\n%(order)s\n"
        "%(polya)s\n"
        "byudzhet: {slajdov: %(n)d, slov_vsego: %(zap)s, illustracij: %(zap)s}\n"
        "uzhe_vvedeno_ranee: []\n"
        "tochno_ne_pokazyvaem: []\n"
        "---\n"
    ) % {"id": lekcija_id, "order": order, "polya": polya,
         "n": len(slide_ids), "zap": ZAPOLNIT}


def bootstrap(lekcija_dir, slide_ids, force=False):
    """Ход «каркас» (`slide_ids` пуст — шаг 3 процедуры, до разговора) или
    легаси-путь `--slajdy` (`slide_ids` дан целиком — фикстуры / список известен
    заранее). НЕ читает существующий `brief.md` — это дело `dosypat()`."""
    lekcija_dir = Path(lekcija_dir)
    lekcija_dir.mkdir(parents=True, exist_ok=True)
    brief = lekcija_dir / "brief.md"
    if brief.is_file() and not force:
        raise SystemExit(
            "%s уже существует — не трогаю (лекция может уже нести правки по фазам "
            "1-2, шапка растёт, а не переписывается, Я2 §3). Явно перезаписать: --force" % brief)
    brief.write_text(_brief_text(lekcija_dir.name, slide_ids), encoding="utf-8")

    intervyu = lekcija_dir / "INTERVYU.md"
    if not intervyu.is_file() or force:
        intervyu.write_text(_intervyu_text(), encoding="utf-8")

    slajdy_dir = lekcija_dir / "slajdy"
    created = 0
    for imya in slide_ids:
        slide_dir = slajdy_dir / imya
        slide_dir.mkdir(parents=True, exist_ok=True)
        card = slide_dir / "slaid.md"
        if card.is_file():
            continue  # не затираем накопленную работу — идемпотентность по слайду
        card.write_text(_slide_card_text(imya), encoding="utf-8")
        created += 1

    (lekcija_dir / "illustracii").mkdir(exist_ok=True)
    return created, len(slide_ids), brief


def dosypat(lekcija_dir):
    """Ход «досыпать» (после подфазы 5.2): `brief.md` уже существует и несёт
    заполненный владельцем `slide_order` — дописывает НЕДОСТАЮЩИЕ папки слайдов.
    `brief.md` и `INTERVYU.md` не трогает — это работа владельца, не бутстрапа
    (Я2 §3: шапка растёт по фазам, чужие поля не переписываются, Н1)."""
    lekcija_dir = Path(lekcija_dir)
    brief = lekcija_dir / "brief.md"
    meta = parse_brief(brief.read_text(encoding="utf-8"))
    slide_ids = [s for s in meta.get("slide_order", []) if s]
    if not slide_ids:
        raise SystemExit(
            "%s: slide_order пуст — подфаза 5.2 ещё не прошла (владелец не назвал "
            "слайды), дописывать пока нечего" % brief)
    if len(set(slide_ids)) != len(slide_ids):
        raise SystemExit("%s: slide_order несёт повторы имён — имена должны быть уникальны" % brief)

    slajdy_dir = lekcija_dir / "slajdy"
    created = 0
    for imya in slide_ids:
        slide_dir = slajdy_dir / imya
        slide_dir.mkdir(parents=True, exist_ok=True)
        card = slide_dir / "slaid.md"
        if card.is_file():
            continue  # не затираем накопленную работу — идемпотентность по слайду
        card.write_text(_slide_card_text(imya), encoding="utf-8")
        created += 1

    (lekcija_dir / "illustracii").mkdir(exist_ok=True)
    return created, len(slide_ids)


def main():
    ap = argparse.ArgumentParser(
        description="Порождает анкету лекции: каркас (без аргументов) → досыпать "
                     "(без аргументов, повторный вызов) → либо --slajdy целиком")
    ap.add_argument("lekcija", help="путь к папке лекции (создаётся, если её нет)")
    ap.add_argument("--slajdy", default=None,
                     help="легаси-путь: имена слайдов через запятую целиком, "
                          "ПОРЯДОК = порядок в деке (список известен заранее)")
    ap.add_argument("--force", action="store_true",
                     help="ход «каркас»: перезаписать существующий brief.md/INTERVYU.md "
                          "(слайды всё равно не трогаются)")
    args = ap.parse_args()

    if args.slajdy is not None:
        slide_ids = [s.strip() for s in args.slajdy.split(",") if s.strip()]
        if not slide_ids:
            raise SystemExit("--slajdy пуст — нечего создавать")
        if len(set(slide_ids)) != len(slide_ids):
            raise SystemExit("--slajdy несёт повторы имён — имена должны быть уникальны")
        created, total, brief = bootstrap(args.lekcija, slide_ids, force=args.force)
        print("создано: %d карточек слайдов + 1 карточка лекции (%s, из них новых слайдов %d/%d)"
              % (created, brief, created, total))
        return 0

    brief_path = Path(args.lekcija) / "brief.md"
    if not brief_path.is_file():
        created, total, brief = bootstrap(args.lekcija, [], force=args.force)
        print("каркас: %s (slide_order пуст, INTERVYU.md со скелетом разделов) — "
              "владелец называет слайды на подфазе 5.2, затем этот же вызов без "
              "--slajdy досыпает недостающие папки" % brief)
        return 0

    created, total = dosypat(args.lekcija)
    print("досыпано: %d новых карточек слайдов из %d в slide_order (новых слайдов %d/%d)"
          % (created, total, created, total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
