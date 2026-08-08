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

🔴 Гейт ЗНАЕТ ФАЗЫ (заход format-kartochki-faza-1). `--faza 1` — выход интервью:
тип идеи из закрытого списка · идея одной фразой (`zachem`) · минуты · блоки,
размеченные типом и МЫСЛЬЮ · ровно один блок помечен центральным. Тело блоков на
Ф1 ещё не пишется и не судится. Полная проверка (без флага) требует всего разом и
применима с выхода Ф3.

Чего гейт НЕ проверяет — печатается ВСЛУХ на каждом прогоне (`NE_PROVERYAYU`),
включая зелёный: сумма минут, бюджет слайдов/иллюстраций, слайд-хозяин термина.

  python3 _generator/sborka/gejt_kartochki.py <лекция-dir>              # полная проверка
  python3 _generator/sborka/gejt_kartochki.py --faza 1 <лекция-dir>     # выход фазы 1
  # exit 0 — зелёный, 1 — красный
"""
import argparse
import sys
from pathlib import Path

SBORKA = Path(__file__).resolve().parent
sys.path.insert(0, str(SBORKA))
from formaty import (parse_card, parse_front_matter, OBYAZATELNYE_POLYA, ZAPOLNIT,  # noqa: E402
                      FormatSlaida, strip_lifecycle_block, FAZA_STROKA_RE,
                      TIPY_IDEI, CENTRALNYJ_PERECHISLENIE)
import bloki  # noqa: E402


# Заглушка, доехавшая до зрителя (POMARKI-2026-08-09 §4, разбор centr-gruppy):
# `zagolovok_na_ekrane: заполнить` рендерился на экран буквально («ЗАПОЛНИТЬ»
# крупным капсом), а поле не входило в `OBYAZATELNYE_POLYA` (`formaty.py`, вне
# зоны этого захода) — карточка была зелёной, слайд «успешно» собран, заглушка
# доехала до зрителя. Пустая строка `""` ЛЕГАЛЬНА (слайд без заголовка на
# экране — законный случай, так уже стоит в нескольких фикстурах); красит
# ТОЛЬКО буквальное значение ZAPOLNIT. 🔴 На выходе ФАЗЫ 1 не проверяется —
# `zagolovok_na_ekrane` не в `FAZA_POLYA[1]` (та же фаза, где решается
# `tip_verstki`/`liniya`, а не интервью): красить `--faza 1` за поле, которое
# эта фаза не обязана заполнять, значит повторить регрессию `--faza 1`,
# описанную выше в этом файле (ловушка 29 `PROGNAT.sh`).
def _check_zagolovok_na_ekrane(sid, params, faza):
    if faza == 1:
        return []
    if params.get("zagolovok_na_ekrane") == ZAPOLNIT:
        return ["%s: поле 'zagolovok_na_ekrane' несёт незаполненную пометку "
                "'%s' — она рендерится на экран буквально" % (sid, ZAPOLNIT)]
    return []


def _unfilled(val):
    return val is None or val == "" or val == ZAPOLNIT


# Р захода format-kartochki-faza-1 (был долг Д38, до него — Р2 захода
# porcia-1-zamknut-konvejer): набор обязательных полей зависит от фазы, на выходе
# которой стоит карточка.
#
# 🔴 ФАЗА 1 ПЕРЕВЁРНУТА. Прежняя редакция несла `FAZA_POLYA = {1: ()}` с
# комментарием «карточка ЕЩЁ НЕ ТРОНУТА, все поля решает Ф2» — и `--faza 1` давал
# ЗЕЛЁНЫЙ на свежепорождённой карточке, где нет ни типа идеи, ни блоков, ни
# центрального блока. Это прямо противоречило гейту выхода фазы 1 в спецификации
# (`fazy-1-2-plan.md §3`) и дословной формулировке владельца: «результатом
# интервью является разбиение на слайды и у каждого слайда разбиение на блоки».
# Опаснее отсутствия флага: флаг с правильным именем существовал, отвечал зелёным,
# и ему верили — «зелёный чекер с необъявленной слепой зоной», RUKOVODSTVO кл. 4½.
#
# Что решает Ф1 (интервью, единственная авторская фаза): имя и название слайда ·
# ТИП ИДЕИ · идею одной фразой (её несёт `zachem`, отдельного поля нет — Я1 §2
# дословно «зритель должен увидеть, что…») · минуты (гейт Ф1 требует сходимости
# суммы минут, значит минуты назначаются ЗДЕСЬ, а не на Ф2). Вёрстка, акцент,
# важность и бюджет слов остаются за Ф2 — на них Ф1 не смотрит.
# Остальные значения `--faza` явной спецификации не несут и сознательно падают на
# полную проверку — минимум, а не гадание за несуществующее требование.
FAZA_POLYA = {1: ("imya", "nazvanie", "zachem", "tip_idei", "minuty")}

# Р1б (П0: «дисциплина, невозможная игнорировать физически») — блок «что дальше»
# обязан быть в КАЖДОЙ карточке (`bootstrap_lekcii.py` его вшивает) и называть
# все фазы Ф1-Ф6 хотя бы одной командой. Критерий 3 Р1: убрали блок — гейт
# краснеет, а не молчит (иначе это украшение, не дисциплина).
# 🔴 Ф1 добавлена заходом format-kartochki-faza-1: прежний набор начинался с Ф2 и
# тем самым УТВЕРЖДАЛ, что карточки фаза 1 не касается. Касается — она их и
# размечает; старые карточки поднимает `bootstrap_lekcii.py --migraciya`.
FAZY_OBYAZATELNY_V_BLOKE = (1, 2, 3, 4, 5, 6)

# Слепые зоны, объявляемые ВСЛУХ на каждом прогоне (RUKOVODSTVO кл. 4½: чекер,
# который молчит про то, чего не смотрит, читается как «проверено всё»). Ключ —
# фаза, значение — что именно из гейта выхода этой фазы скрипт НЕ проверяет и
# почему. Строка печатается всегда, и на зелёном тоже.
NE_PROVERYAYU = {
    1: (
        "сумма минут против dlitelnost_minut лекции (допуск владельцем не назван; "
        "точное равенство покраснело бы на живой лекции)",
        "число слайдов и иллюстраций против byudzhet карточки лекции "
        "(byudzhet.slajdov порождается нулём и ходом «досыпать» не обновляется)",
        "слайд-хозяин каждого вводимого термина (списка терминов лекции нет ни в одном файле)",
        "центральный блок на слайде БЕЗ текста (K3 — законный случай, блоков нет вовсе)",
        "регистр текста и соответствие мысли заявленной — это слой LLM-верификатора (Я1 §6)",
    ),
}
NE_PROVERYAYU_VSEGDA = (
    "matematika_iz и zamer_tempa — покрытие ленты и замер темпа (долги Д51/Д38, "
    "поля порождаются, но гейта на них ещё нет)",
    "верен ли акцент и та ли это вообще лекция — только человек (Я1 §6)",
)


def _check_lifecycle_block(text, sid):
    blok, _ = strip_lifecycle_block(text)
    if blok is None:
        return ["%s: блок «что дальше» (жизнь карточки) отсутствует — должен быть "
                "HTML-комментарием строго до YAML-шапки, см. bootstrap_lekcii.py" % sid]
    nazvano = {int(m.group(1)) for m in FAZA_STROKA_RE.finditer(blok)}
    ne_nazvano = [f for f in FAZY_OBYAZATELNY_V_BLOKE if f not in nazvano]
    if ne_nazvano:
        return ["%s: блок «что дальше» не называет фазу(ы) %s (нужны все: %s)"
                 % (sid, ", ".join("Ф%d" % f for f in ne_nazvano),
                    ", ".join("Ф%d" % f for f in FAZY_OBYAZATELNY_V_BLOKE))]
    return []


def _polya_dlya_fazy(faza):
    if faza is None:
        return OBYAZATELNYE_POLYA
    return FAZA_POLYA.get(faza, OBYAZATELNYE_POLYA)


# Дочистка приёмки (тот же заход porcia-1-zamknut-konvejer): полный гейт молчал
# на теле-заглушке (`### [narrativ] заполнить` / `заполнить`, ровно то, что
# порождает `bootstrap_lekcii.py`, Р1а) — слово ZAPOLNIT в поле шапки ловилось,
# в блоке тела — нет.
#
# 🔴 Заход format-kartochki-faza-1 развёл ОДИН вопрос на ДВА, и в этом вся суть Ф1.
# «Блок размечен» и «блок написан» — разные события разных фаз:
#   · МЫСЛЬ блока (`### [tip] мысль`) — выход ФАЗЫ 1. Дословно владелец: «на седьмом
#     слайде 4 блока, а третий из них — нарратив, объясняющий такую-то идею». Текста
#     ещё нет, разметка уже есть;
#   · ТЕЛО блока — «Математика» с выхода Ф2, «Текст слайда» с выхода Ф3.
# Прежде `_razdely_dlya_fazy(1)` возвращал пустой кортеж — тело на Ф1 не судилось
# ВОВСЕ, то есть главное действие фазы 1 (заменить заглушку настоящими блоками) не
# проверялось ничем. Прочие `faza` (как и у `_polya_dlya_fazy`) падают на полную
# проверку — минимум, не гадание за неспецифицированное требование.
RAZDELY_TELA = {"matematika": bloki.KEY_MATEMATIKA, "tekst": bloki.KEY_TEKST}


def _razdely_dlya_fazy(faza):
    """Разделы, в которых на выходе этой фазы обязано стоять настоящее ТЕЛО."""
    if faza == 1:
        return ()
    if faza == 2:
        return ("matematika",)
    return ("matematika", "tekst")


# Разделы, в которых настоящая МЫСЛЬ блока обязана стоять уже с выхода Ф1 — оба:
# состав блоков сверяется между разделами (`bloki.check_composition`), поэтому
# разметка живёт в обоих сразу, от фазы этот набор не зависит.
RAZDELY_S_MYSLYU = ("matematika", "tekst")


def _check_zapolnit_v_tele(sid, sections, faza):
    issues = []
    for razdel in RAZDELY_S_MYSLYU:
        for b in sections[razdel]:
            if b.mysl == ZAPOLNIT:
                issues.append("%s: раздел «%s» несёт блок с незаполненной мыслью («%s») — "
                               "разметка блоков это выход ФАЗЫ 1, а не украшение шаблона"
                               % (sid, RAZDELY_TELA[razdel], ZAPOLNIT))
    for razdel in _razdely_dlya_fazy(faza):
        for b in sections[razdel]:
            # 🔴 ПУСТОЕ тело ловится наравне с «заполнить», и это прямое следствие
            # перевода фазы 1 на разметку блоков: до него бутстрап всегда клал в
            # тело слово ZAPOLNIT, и пустого тела просто не бывало. Теперь выход
            # Ф1 — блок с мыслью и БЕЗ тела, то есть законное промежуточное
            # состояние; не лови его на Ф2/Ф3 — и размеченный, но ненаписанный
            # блок проедет полный гейт зелёным. Найдено фикстурой 29, не глазами.
            if b.telo.strip() in ("", ZAPOLNIT):
                issues.append("%s: раздел «%s» несёт ненаписанное тело блока «%s» — "
                               "разметка блока это выход Ф1, а содержание пишется здесь"
                               % (sid, RAZDELY_TELA[razdel], b.mysl))
    return issues


def _check_tip_idei(sid, params):
    """Гейт выхода Ф1, строка 1: «у каждого слайда назван тип идеи». Пустоту ловит
    `_polya_dlya_fazy`; здесь — ЗНАЧЕНИЕ против закрытого списка."""
    tip = params.get("tip_idei")
    if _unfilled(tip) or tip in TIPY_IDEI:
        return []
    return ["%s: tip_idei '%s' не из закрытого списка. Допустимы: %s. ⚠ Список закрыт, "
            "но НЕ окончателен (fazy-1-2-plan.md §2): слайд, не ложащийся ни в один тип, — "
            "повод обсудить НОВЫЙ тип с владельцем, а не подобрать ближайший"
            % (sid, tip, ", ".join(TIPY_IDEI))]


def _check_centralnyj_blok(sid, params, sections):
    """Гейт выхода Ф1, строка 3: «ровно один блок помечен центральным (исключение —
    слайд-перечисление, помечается явно)». Носитель пометки — поле шапки
    `centralnyj_blok`, несущее МЫСЛЬ центрального блока; маркер внутри заголовка
    блока отвергнут: он лёг бы внутрь группы «мысль» у `bloki.BLOCK_RE`, а её
    `check_composition` сверяет между разделами — маркер пришлось бы дублировать.

    🔴 Поле обязано РЕЗОЛВИТЬСЯ ровно в один блок раздела «Математика», иначе оно
    декоративно: копия мысли с опечаткой давала бы зелёный, а «ровно один» не
    проверялся бы ничем — та самая болезнь, которую чинит этот заход.

    K3 (Я1 §4): слайд БЕЗ текста законен, блоков у него нет вовсе — сюда не
    попадает (вызывается только при непустом теле) и объявлен в слепых зонах."""
    val = params.get("centralnyj_blok")
    if _unfilled(val):
        return ["%s: centralnyj_blok не заполнен — гейт выхода Ф1 требует, чтобы ровно один "
                "блок был помечен центральным (или '%s' для слайда-перечисления)"
                % (sid, CENTRALNYJ_PERECHISLENIE)]
    if val == CENTRALNYJ_PERECHISLENIE:
        return []
    mysli = [b.mysl for b in sections["matematika"]]
    n = mysli.count(val)
    if n == 1:
        return []
    if n == 0:
        return ["%s: centralnyj_blok '%s' не совпал ни с одной мыслью блока раздела «%s». "
                "Мысли блоков: %s" % (sid, val, bloki.KEY_MATEMATIKA,
                                      ", ".join("«%s»" % m for m in mysli) or "(блоков нет)")]
    return ["%s: centralnyj_blok '%s' совпал с %d блоками раздела «%s» — центральный обязан "
            "быть РОВНО один; различите мысли блоков"
            % (sid, val, n, bloki.KEY_MATEMATIKA)]


def check_slide(sid, text, illustracii_pool, uzhe_vvedeno, vvodit_by_sid, faza=None):
    """Одна карточка → список замечаний (пустой — карточка чиста)."""
    issues = _check_lifecycle_block(text, sid)
    try:
        params, raw_body = parse_card(text, sid=sid)
    except FormatSlaida as e:
        issues.append("%s: карточка не парсится: %s" % (sid, e))
        return issues

    for f in _polya_dlya_fazy(faza):
        if _unfilled(params.get(f)):
            issues.append("%s: обязательное поле '%s' не заполнено" % (sid, f))

    issues.extend(_check_tip_idei(sid, params))
    issues.extend(_check_zagolovok_na_ekrane(sid, params, faza))

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

    issues.extend(_check_zapolnit_v_tele(sid, sections, faza))
    issues.extend(_check_centralnyj_blok(sid, params, sections))

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


def check_lekcija(lekcija_dir, faza=None):
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
        issues.extend(check_slide(sid, texts[sid], illustracii_pool, uzhe_vvedeno, vvodit_by_sid, faza=faza))
    return issues, len(slide_paths)


def _pechat_slepyh_zon(faza):
    """Слепые зоны — ВСЛУХ и на каждом прогоне, включая зелёный. Молчащий чекер
    читается как «проверено всё»: ровно так `--faza 1` и врал до этого захода."""
    zony = tuple(NE_PROVERYAYU.get(faza, ())) + NE_PROVERYAYU_VSEGDA
    print("НЕ проверяю: %d пункт(ов) — ниже поимённо" % len(zony))
    for z in zony:
        print("  · %s" % z)


def main():
    ap = argparse.ArgumentParser(description="Гейт карточек лекции — краснеет и не пропускает дальше")
    ap.add_argument("lekcija", help="путь к папке лекции (несёт brief.md + slajdy/)")
    ap.add_argument("--faza", type=int, default=None,
                     help="требования зависят от фазы, на выходе которой стоит карточка; "
                          "--faza 1 = выход интервью (тип идеи, имя/название, идея одной "
                          "фразой в zachem, минуты, размеченные блоки с мыслью, ровно один "
                          "центральный блок — ТЕЛО блоков ещё не пишется); остальные "
                          "значения = полная проверка, как без флага")
    args = ap.parse_args()

    issues, n = check_lekcija(args.lekcija, faza=args.faza)
    rezhim = "выход фазы %d" % args.faza if args.faza else "полная проверка"
    if issues:
        print("КРАСНЫЙ (%s): проверено %d из %d карточек, замечаний %d" % (rezhim, n, n, len(issues)))
        for it in issues:
            print("  ✗ %s" % it)
    else:
        print("ЗЕЛЁНЫЙ (%s): проверено %d из %d карточек, замечаний 0" % (rezhim, n, n))
    _pechat_slepyh_zon(args.faza)
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
