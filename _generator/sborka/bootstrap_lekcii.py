#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Порождает структуру лекции — карточку лекции и по карточке на слайд, СО ВСЕМИ
полями и пометкой «заполнить» (Э3 захода kartochka-i-sborka). Требование владельца
дословно: «скрипт создаёт документ, в котором есть конкретные строки — анкету.
И поставить гейт: если что-то не заполнено, дальше не идём» (`gejt_kartochki.py`).

  python3 _generator/sborka/bootstrap_lekcii.py <лекция-dir> --slajdy id1,id2,id3

Раскладка — Я2: `<лекция>/brief.md` (манифест порядка + карточка лекции, Я1 §1) +
`<лекция>/slajdy/<id>/slaid.md` на каждый слайд (Я1 §2).

Вход — явный список ИМЁН слайдов через CLI, НЕ парсинг `INTERVYU.md`: формат этого
файла нигде в якорях захода (Я1–Я6) не специфицирован — это фаза 1 (Cowork+владелец,
СКИЛЛ.md Н2), сюда не относится и не додумывается. Названо строкой в `## ВОПРОСЫ`
захода как долг для следующего.

Идемпотентно по слайдам: существующий `slaid.md` НЕ перезаписывается (не теряет
работу владельца), считается «уже есть», не «создано». `brief.md` целиком
перезаписать может ТОЛЬКО `--force` (иначе отказ — не затирать лекцию, которая уже
что-то накопила по фазам)."""
import argparse
import sys
from pathlib import Path

SBORKA = Path(__file__).resolve().parent
sys.path.insert(0, str(SBORKA))
from formaty import ZAPOLNIT  # noqa: E402

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
    lekcija_dir = Path(lekcija_dir)
    lekcija_dir.mkdir(parents=True, exist_ok=True)
    brief = lekcija_dir / "brief.md"
    if brief.is_file() and not force:
        raise SystemExit(
            "%s уже существует — не трогаю (лекция может уже нести правки по фазам "
            "1-2, шапка растёт, а не переписывается, Я2 §3). Явно перезаписать: --force" % brief)
    brief.write_text(_brief_text(lekcija_dir.name, slide_ids), encoding="utf-8")

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


def main():
    ap = argparse.ArgumentParser(
        description="Порождает анкету лекции: brief.md + slajdy/<id>/slaid.md на каждый слайд")
    ap.add_argument("lekcija", help="путь к папке лекции (создаётся, если её нет)")
    ap.add_argument("--slajdy", required=True,
                     help="имена слайдов через запятую, ПОРЯДОК = порядок в деке")
    ap.add_argument("--force", action="store_true",
                     help="перезаписать существующий brief.md (слайды всё равно не трогаются)")
    args = ap.parse_args()

    slide_ids = [s.strip() for s in args.slajdy.split(",") if s.strip()]
    if not slide_ids:
        raise SystemExit("--slajdy пуст — нечего создавать")
    if len(set(slide_ids)) != len(slide_ids):
        raise SystemExit("--slajdy несёт повторы имён — имена должны быть уникальны")

    created, total, brief = bootstrap(args.lekcija, slide_ids, force=args.force)
    print("создано: %d карточек слайдов + 1 карточка лекции (%s, из них новых слайдов %d/%d)"
          % (created, brief, created, total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
