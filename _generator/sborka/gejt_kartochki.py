#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Гейт карточек лекции — краснеет и не пропускает дальше (Э4 захода
kartochka-i-sborka). Скриптовый слой Я1 §6, дословно:

  · обязательные поля шапки заполнены (не пусты и не несут пометку «заполнить»):
    imya, nazvanie, zachem, akcent, minuty, vazhnost, tip_verstki, liniya, byudzhet_slov;
  · каждый абзац тела принадлежит блоку (текст ДО первого '### [tip]' в разделе —
    нарушение), тип блока — из закрытого списка (bloki.py поднимает ошибку сам);
  · состав блоков «Текст слайда» совпадает с «Математикой» (bloki.check_composition);
  · бюджет слов не превышен — считается по разделу «Текст слайда — сжато»;
  · каждое имя из illustracii резолвится в пул лекции (illustracii/<имя>/);
  · каждый термин из opiraetsya_na либо введён (числится в vvodit) на названном
    слайде, либо перечислен в uzhe_vvedeno_ranee карточки лекции (brief.md).

⚠ K3 (kartochka-slajda.md): слайд БЕЗ текста — законный случай, бюджет слов на
нём не проверяется вовсе (raw_body пуст → секции не разбираются).

Верификатор-LLM (второй слой Я1 §6 — регистр по типу блока, запрещённые обороты,
формулировка несёт заявленную мысль) этот скрипт НЕ реализует и не вызывает —
только скриптовая часть. Где вызывается LLM-слой — назван в протоколе Э7.

  python3 _generator/sborka/gejt_kartochki.py <лекция-dir>     # exit 0 — зелёный, 1 — красный
"""
import argparse
import sys
from pathlib import Path

SBORKA = Path(__file__).resolve().parent
sys.path.insert(0, str(SBORKA))
from formaty import parse_card, parse_front_matter, OBYAZATELNYE_POLYA, ZAPOLNIT, FormatSlaida  # noqa: E402
import bloki  # noqa: E402


def _unfilled(val):
    return val is None or val == "" or val == ZAPOLNIT


def check_slide(sid, text, illustracii_pool, uzhe_vvedeno, vvodit_by_sid):
    """Одна карточка → список замечаний (пустой — карточка чиста)."""
    issues = []
    try:
        params, raw_body = parse_card(text, sid=sid)
    except FormatSlaida as e:
        return ["%s: карточка не парсится: %s" % (sid, e)]

    for f in OBYAZATELNYE_POLYA:
        if _unfilled(params.get(f)):
            issues.append("%s: обязательное поле '%s' не заполнено" % (sid, f))

    for name in params.get("illustracii") or []:
        if name not in illustracii_pool:
            issues.append("%s: иллюстрация '%s' не резолвится в пул лекции (illustracii/)"
                           % (sid, name))

    for item in params.get("opiraetsya_na") or []:
        termin, vvedeno = item.get("termin"), item.get("vvedeno")
        vvedeno_na_slajde = termin in vvodit_by_sid.get(vvedeno, ())
        vvedeno_ranee = termin in uzhe_vvedeno
        if not (vvedeno_na_slajde or vvedeno_ranee):
            issues.append(
                "%s: термин '%s' (opiraetsya_na → vvedeno: %s) не введён на "
                "названном слайде (нет в его vvodit) и не перечислен в "
                "uzhe_vvedeno_ranee лекции" % (sid, termin, vvedeno))

    if not raw_body.strip():
        return issues  # K3: слайд без текста — легален, дальше нечего проверять

    try:
        sections = bloki.parse_sections(raw_body, sid=sid)
    except bloki.FormatBlokov as e:
        issues.append(str(e))
        return issues  # без разобранных секций состав/бюджет не проверить

    if sections["orphan_matematika"]:
        issues.append("%s: в разделе «Математика — развёрнуто» есть абзац вне блока: %r"
                       % (sid, sections["orphan_matematika"][:80]))
    if sections["orphan_tekst"]:
        issues.append("%s: в разделе «Текст слайда — сжато» есть абзац вне блока: %r"
                       % (sid, sections["orphan_tekst"][:80]))

    for m in bloki.check_composition(sections):
        issues.append("%s: состав блоков не совпадает — %s" % (sid, m))

    budget = params.get("byudzhet_slov")
    if not _unfilled(budget):
        try:
            budget_n = float(budget)
        except ValueError:
            issues.append("%s: byudzhet_slov не число: %r" % (sid, budget))
        else:
            flat = bloki.render_section_markdown(sections["tekst"])
            n_words = len(flat.split())
            if n_words > budget_n:
                issues.append("%s: бюджет слов превышен: %d > %s" % (sid, n_words, budget))

    return issues


def check_lekcija(lekcija_dir):
    """Папка лекции → (issues: [str], n_slides: int). issues пуст — гейт зелёный."""
    lekcija_dir = Path(lekcija_dir)
    brief_path = lekcija_dir / "brief.md"
    if not brief_path.is_file():
        return (["%s: brief.md не найден" % lekcija_dir], 0)

    brief_params, _ = parse_front_matter(brief_path.read_text(encoding="utf-8"), sid="brief.md")
    uzhe_vvedeno = {item.get("termin") for item in (brief_params.get("uzhe_vvedeno_ranee") or [])
                    if isinstance(item, dict)}
    illustracii_pool = {p.name for p in (lekcija_dir / "illustracii").glob("*") if p.is_dir()} \
        if (lekcija_dir / "illustracii").is_dir() else set()

    slajdy_dir = lekcija_dir / "slajdy"
    slide_paths = sorted(slajdy_dir.glob("*/slaid.md"))
    if not slide_paths:
        return (["%s: нет карточек в %s (ищу */slaid.md)" % (lekcija_dir, slajdy_dir)], 0)

    texts, vvodit_by_sid = {}, {}
    for p in slide_paths:
        sid = p.parent.name
        text = p.read_text(encoding="utf-8")
        texts[sid] = text
        try:
            params, _ = parse_card(text, sid=sid)
            vvodit_by_sid[sid] = set(params.get("vvodit") or [])
        except FormatSlaida:
            vvodit_by_sid[sid] = set()

    issues = []
    for p in slide_paths:
        sid = p.parent.name
        issues.extend(check_slide(sid, texts[sid], illustracii_pool, uzhe_vvedeno, vvodit_by_sid))
    return issues, len(slide_paths)


def main():
    ap = argparse.ArgumentParser(description="Гейт карточек лекции — краснеет и не пропускает дальше")
    ap.add_argument("lekcija", help="путь к папке лекции (несёт brief.md + slajdy/)")
    args = ap.parse_args()

    issues, n = check_lekcija(args.lekcija)
    if not issues:
        print("ЗЕЛЁНЫЙ: %d карточек проверено, замечаний 0" % n)
        return 0
    print("КРАСНЫЙ: %d карточек проверено, замечаний %d" % (n, len(issues)))
    for it in issues:
        print("  ✗ %s" % it)
    return 1


if __name__ == "__main__":
    sys.exit(main())
