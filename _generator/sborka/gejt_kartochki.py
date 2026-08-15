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
import re
import sys
from collections import Counter
from pathlib import Path

SBORKA = Path(__file__).resolve().parent
sys.path.insert(0, str(SBORKA))
from formaty import (parse_card, parse_front_matter, OBYAZATELNYE_POLYA, ZAPOLNIT,  # noqa: E402
                      FormatSlaida, strip_lifecycle_block, FAZA_STROKA_RE,
                      TIPY_SLAJDA, TIPY_SLAJDA_BEZ_TREBOVANIYA_SVYAZEJ, CENTRALNYJ_PERECHISLENIE)
import bloki  # noqa: E402
import tipy_slajdov  # noqa: E402


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
FAZA_POLYA = {1: ("imya", "nazvanie", "zachem", "tip_slaida", "minuty")}

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
    "Г-3, вторая половина («список ОБЯЗАТЕЛЕН при двух и более пунктах») — "
    "«сколько понятий несёт блок» суждение, не машинный признак (заход "
    "zakony-v-gejt); ловится только «список из одного пункта запрещён»",
    "все двенадцать законов фазы 2 (А6/А8/А9/А10/Г-1/Г-2/Г-3/Г-6/Г-7/Г-8/Г-12/Г-15) "
    "печатаются ЖЁЛТЫМ, а не красным — держатся без исключений на ОДНОЙ лекции "
    "(teorkat-vvedenie/L2, 18 карточек), не на всём корпусе фабрики",
    "Э3 (sceny-iz-blokov): 'доказательство не в сцене предмета' проверяется "
    "консервативно ПО ТИПУ блока (не смеет делить сцену ни с одним более ранним "
    "несущим блоком раздела) — рёбра `dokazatelstvo_opiraetsya_na`, которые "
    "укажут точный предмет, ещё не заведены (заход kod_rebra-blokov.md); "
    "проверка сузится, когда они появятся",
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


def _check_tip_slaida(sid, params):
    """Гейт выхода Ф1, строка 1: «у каждого слайда назван тип». Пустоту ловит
    `_polya_dlya_fazy`; здесь — ЗНАЧЕНИЕ против закрытого списка (заход
    tipologia-odna-os: одна ось `tip_slaida` вместо `tip_idei`+Т1-Т5 раздельно)."""
    tip = params.get("tip_slaida")
    if _unfilled(tip) or tip in TIPY_SLAJDA:
        return []
    return ["%s: tip_slaida '%s' не из закрытого списка. Допустимы: %s. ⚠ Список закрыт, "
            "но НЕ окончателен: слайд, не ложащийся по СОСТАВУ ни в один тип, — повод "
            "обсудить РАСШИРЕНИЕ типологии с владельцем (временно — %s), а не подобрать "
            "ближайшую полку"
            % (sid, tip, ", ".join(TIPY_SLAJDA), tipy_slajdov.NE_KLASSIFICIROVAN)]


# Заход tipologia-odna-os, Э3 — ЖЁСТКИЙ гейт: состав блоков карточки обязан
# соответствовать раскладке заявленного `tip_slaida`. Владелец дословно: «жёсткость
# нужна ИМЕННО здесь — экзотическая раскладка почти всегда значит, что автор забыл
# блок, дописал лишний или переставил порядок, и это должно быть запрещено машиной».
# Три КРАСНЫХ исхода в одной проверке (недостающий обязательный / лишний блок вне
# раскладки / нарушенный порядок) — три ветки одного и того же
# `tipy_slajdov.proverit_sostav`, см. его докстроку про verdict.
def _check_sostav_tipa(sid, params, sections):
    tip = params.get("tip_slaida")
    if _unfilled(tip) or tip not in tipy_slajdov.TIPY:
        # незаполненное поле красит _polya_dlya_fazy, значение вне закрытого
        # списка — _check_tip_slaida; Т6/NE_KLASSIFICIROVAN сюда не попадают
        # намеренно (у Т6 состав задаёт геометрия, не эта раскладка; на
        # NE_KLASSIFICIROVAN раскладку сверять нечем — это и есть смысл значения)
        return []
    actual = [b.tip for b in sections["matematika"]]
    verdikt, detail = tipy_slajdov.proverit_sostav(tip, actual)
    if verdikt == "OK":
        return []
    opis = tipy_slajdov.opisanie(tip)
    if verdikt == "MISSING":
        return ["%s: тип %s — не хватает обязательного блока [%s]. Раскладка: %s"
                % (sid, tip, detail, opis)]
    if verdikt == "EXTRA":
        return ["%s: тип %s — блок(и) вне раскладки: %s. Раскладка: %s. Слайд, не "
                "ложащийся ни в один тип по составу, — повод обсудить РАСШИРЕНИЕ "
                "типологии с владельцем, а не подобрать ближайшую полку"
                % (sid, tip, detail, opis)]
    return ["%s: тип %s — нарушен порядок блоков (%s). Раскладка: %s"
            % (sid, tip, detail, opis)]


# Заход tipologia-odna-os, Э3 — ЖЁЛТЫЙ (не красит rc): у Т1 слот `primer`
# необязателен, но пропуск примера на определении молча неотличим от осознанного
# решения (цена: на лекции 2 прошла череда определений без примеров именно поэтому).
# Поле-освобождение — по образцу `primer_snyat_namerenno: <почему>`; есть — жёлтый
# гаснет, нет — горит.
PRIMER_SNYAT_POLE = "primer_snyat_namerenno"


def _check_primer_t1(sid, params, sections):
    if params.get("tip_slaida") != "Т1":
        return []
    if any(b.tip == "primer" for b in sections["matematika"]):
        return []
    if not _unfilled(params.get(PRIMER_SNYAT_POLE)):
        return []
    return ["%s: тип Т1 без примера и без поля '%s' — заполни поле обоснованием "
            "(почему пример снят), либо добавь блок [primer]" % (sid, PRIMER_SNYAT_POLE)]


def _check_ne_klassificirovan(sid, params):
    if params.get("tip_slaida") == tipy_slajdov.NE_KLASSIFICIROVAN:
        return ["%s: tip_slaida не назначен (%s) — ждёт решения владельца"
                % (sid, tipy_slajdov.NE_KLASSIFICIROVAN)]
    return []


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


# У12 захода uroki-faz-1-2-v-disciplinu, 🔴 ГЛАВНОЕ: `vvodit`/`opiraetsya_na` —
# единственная машинная проверка порядка понятий («изоморфны ⟺ размерности равны»
# стояло на слайде за два слайда ДО того, где размерность вводится — поймал
# владелец глазами, гейт молчал, потому что оба поля были пустыми у всех карточек
# и заполнять их не требовал никто). Проверка `opiraetsya_na → vvodit` (ниже, в
# check_slide) работает и на пустом списке, но пустой список НИЧЕГО не проверяет —
# «зелёный от промаха мимо входа», тот же класс, что уже стоит в каноне.
#
# Развилка «выбери и обоснуй» (задание Ф1, пункт 1): слайд служебного типа/чисто
# нарративного типа может законно ничего не вводить. Решение — НЕ отдельный
# маркер-заглушка (третий формат сверх уже существующего `CENTRALNYJ_PERECHISLENIE`),
# а условие «оба поля пусты ОДНОВРЕМЕННО» плюс полное освобождение типов, с которых
# связей не требуют (TIPY_SLAJDA_BEZ_TREBOVANIYA_SVYAZEJ — служебные плюс Т4).
# Подробное обоснование — `## ПЛАН` захода.
#
# 🔴 Заход svedenie-i-smeta, Э1.4: освобождение было УЖЕ ЗДЕСЬ ОПИСАНО строкой выше
# («слайд типа narrativ/divider может законно ничего не вводить»), но в коде стоял
# список одних лишь служебных типов — и `--faza 1` красил `napominanie` и `itog`.
# Разошлись не правило и код, а комментарий и его же реализация; чинится списком,
# а не текстом комментария. Цена и список — `formaty.py`. Заход tipologia-odna-os
# перевёл список на новую ось (Т6 + Т4/Т5); заход tipologia-dochistka слил Т5 в
# Т4 — семантика освобождения та же, состав списка сузился на один элемент.
def _check_vvodit_opiraetsya(sid, params, faza):
    if faza != 1:
        return []
    if params.get("tip_slaida") in TIPY_SLAJDA_BEZ_TREBOVANIYA_SVYAZEJ:
        return []
    if not (params.get("vvodit") or params.get("opiraetsya_na")):
        return ["%s: vvodit и opiraetsya_na пусты одновременно — выход фазы 1 обязан "
                "решить, что слайд вводит и на что опирается (единственная машинная "
                "проверка порядка понятий, У12); типы %s освобождены (служебным нечего "
                "вводить, нарративным — нечего опираться на форму), иначе заполни хотя "
                "бы одно поле"
                % (sid, ", ".join(TIPY_SLAJDA_BEZ_TREBOVANIYA_SVYAZEJ))]
    return []


# ═══════════════════════════ Заход `sceny-iz-blokov` (2026-08-14) ═══════════════════════════
# Э1 сделал сцену производной от границы блока (по умолчанию), Э2 оставил ручной
# `{@N}` законным исключением — но исключение обязано быть ВИДНЫМ, не молчаливым:
# карточка, где хоть один блок раздела «Текст слайда» несёт ручной тег, обязана
# нести поле-обоснование `sceny_vruchnuyu` (свободный текст «почему автоматика не
# подходит»). Имя поля назначено заходом и не подлежит обсуждению (см. файл-заход
# Э2). `formaty.py` для этого поля READ-ONLY (проверено при сборке захода:
# валидации «неизвестное поле шапки» там нет — новое поле безопасно без правки).
SCENY_VRUCHNUYU_POLE = "sceny_vruchnuyu"


def _check_sceny_vruchnuyu(sid, params, sections):
    if not bloki.has_manual_scenes(sections["tekst"]):
        return []
    if not _unfilled(params.get(SCENY_VRUCHNUYU_POLE)):
        return []
    return ["%s: раздел «Текст слайда — сжато» несёт ручной тег сцены {@N}, а поле "
            "'%s' в шапке не заполнено — ручной тег ПЕРЕБИВАЕТ автоматику (Э1) и "
            "обязан нести обоснование, иначе он неотличим от забытого (Э2 sceny-iz-blokov)"
            % (sid, SCENY_VRUCHNUYU_POLE)]


# Э3: «доказательство и то, что оно доказывает — никогда не в одной сцене»
# (решение владельца, безусловное). Рёбра (`dokazatelstvo_opiraetsya_na`) заводит
# ОТДЕЛЬНЫЙ заход `kod_rebra-blokov.md` и на сегодня их 0 на живой L2 (проверено
# командой при сборке файла-захода) — без них проверяем по ТИПУ блока, как явно
# разрешил файл-заход (не по ребру, и это НЕ повод стопориться): дока-зательство
# не смеет делить сцену НИ С ОДНИМ более ранним НЕСУЩИМ (не narrativ) блоком
# своего раздела. Это заведомо ШИРЕ точного «предмета доказательства» (тот один
# конкретный блок, на который рёбра однажды укажут точно) — консервативно, без
# ложных зелёных; рёбра появятся — проверку можно сузить до точного предмета.
def _check_dokazatelstvo_scena(sid, sections):
    live = [b for b in sections["tekst"] if b.telo.strip()]
    scenes = bloki.block_start_scenes(live)
    out = []
    for i, b in enumerate(live):
        if b.tip != "dokazatelstvo":
            continue
        for j in range(i):
            subj = live[j]
            if subj.tip == "narrativ" or scenes[j] != scenes[i]:
                continue
            out.append(
                "%s: блок [dokazatelstvo] «%s» (сцена %d) — в той же сцене, что и "
                "более ранний блок [%s] «%s» — доказательство обязано быть на "
                "ДРУГОЙ сцене (Э3 sceny-iz-blokov; рёбер пока нет, проверено по типу "
                "блока, не по предмету — см. ## ПЛАН файла-захода)"
                % (sid, b.mysl, scenes[i], subj.tip, subj.mysl))
    return out


# Заход kod_rebra-blokov.md, Э2: пустота рёбер перестаёт быть незаметной. Доказательство
# без адресата — дефект разметки (владелец назвал жёсткость здесь обязательной, поэтому
# КРАСНЫЙ, в issues); пример без адресата — законный случай (иногда самостоятелен, выборка
# одна лекция) — ЖЁЛТЫЙ, тем же потоком, что и NE_KLASSIFICIROVAN/Т1-без-примера.
def _check_dokazatelstvo_adresat(sid, params, sections):
    if not any(b.tip == "dokazatelstvo" for b in sections["matematika"]):
        return []
    if params.get("dokazatelstvo_opiraetsya_na"):
        return []
    return ["%s: блок [dokazatelstvo] без 'dokazatelstvo_opiraetsya_na' — неизвестно, что "
            "доказывается (Э2 kod_rebra-blokov.md)" % sid]


def _check_primer_adresat(sid, params, sections):
    if not any(b.tip == "primer" for b in sections["matematika"]):
        return []
    if params.get("primer_dlya"):
        return []
    return ["%s: блок [primer] без 'primer_dlya' — пример не адресован ни одной цели "
            "(Э2 kod_rebra-blokov.md)" % sid]


# Э4: «не больше трёх блоков на слайде» — ориентир качества владельца, ЖЁЛТЫЙ,
# не гейт (две карточки живой L2 нарушают его законно уже сегодня). ОТДЕЛЬНЫЙ
# поток `sceny_zheltye` (по образцу `tip_zheltye` захода tipologia-odna-os), а не
# внутрь `ZAKONY_BLOKOV`: тот — явно закрытый список «двенадцати законов фазы 2»
# ДРУГОГО захода (zakony-v-gejt), с зашитой цифрой 12 в докстроках/печати —
# заводить туда тринадцатый закон чужой арки значит смешать две истории правок.
POTOLOK_BLOKOV = 3


def _check_potolok_blokov(sid, sections):
    n = len([b for b in sections["tekst"] if b.telo.strip()])
    if n > POTOLOK_BLOKOV:
        return ["%s: %d блок(ов) на слайде — выше ориентира «не больше %d» (Э4 sceny-iz-blokov)"
                % (sid, n, POTOLOK_BLOKOV)]
    return []


# Заход zakony-v-gejt (2026-08-12, `FAZA-2-PROCEDURA.md §1.1`/§1.1-тер): одиннадцать
# законов фазы 2 держатся БЕЗ ИСКЛЮЧЕНИЙ на живой деке (18 карточек
# teorkat-vvedenie/L2) — владелец признал их годными в гейт 12.08. Плюс Г-3
# (двенадцатая, тем же интервью, переформулирована с Г-8: два однотипных несущих
# блока сливаются в один список) — но у Г-3 машинно проверяется только ПОЛОВИНА
# правила («список из одного пункта запрещён»); вторая половина («список
# обязателен при двух и более пунктах») не вычисляется без оценки смысла текста
# («сколько понятий несёт блок» — суждение, не признак) и объявлена в
# NE_PROVERYAYU_VSEGDA. А2 и А5 ОТМЕНЕНЫ владельцем 12.08 — не вносятся ни в
# каком виде (см. заход).
#
# 🔴 ПОРОГ ВКЛЮЧЕНИЯ — эти законы НИКОГДА не красят гейт. Дословно заход:
# «закон, у которого на живой деке появился нарушитель, выдаёт ЖЁЛТОЕ, а не
# красное, и печатает, на каком слайде». Причина: «держится без исключений»
# проверено на 18 карточках ОДНОЙ лекции 12.08, не на всём корпусе фабрики —
# новый закон обязан начинать жизнь жёлтым, а не ломать сборку немедленно.
# Нарушители Г-1/Г-7/Г-6/Г-2/Г-12/Г-8/А6/А8/А9/Г-15 на сегодняшней L2 — 0 (см.
# отчёт захода); А10 и Г-3 краснеют жёлтым на `inyekcii` — находка, уже названная
# в `AKSIOMY-RAZMETKI.md §7а`/`FAZA-2-PROCEDURA.md §1.1-тер`, не новая.
STATUSNYE_TIPY = ("opredelenie", "utverzhdenie", "primer")  # bloki.TIPY_BLOKOV минус narrativ/dokazatelstvo/itog/uprazhnenie

ZHANROVYJ_YARLYK_RE = {
    "opredelenie": re.compile(r"^\*\*Определение\s*\("),
    "utverzhdenie": re.compile(r"^\*\*Утверждение\s*\("),
    "primer": re.compile(r"^\*\*Пример\s*\("),
}
ZHANROVYJ_YARLYK_ANY_RE = re.compile(r"\*\*(?:Определение|Утверждение|Пример)\s*\(")
DOKAZATELSTVO_YARLYK_RE = re.compile(r"^\*Доказательство\b")
POLE_VREZKA_RE = re.compile(r"^>\s*поле:", re.M)


def zakon_a6(sid, sections):
    """А6: слайд из одного блока — блок обязан быть [narrativ]."""
    b = sections["matematika"]
    if len(b) == 1 and b[0].tip != "narrativ":
        return ["%s: единственный блок слайда — [%s] «%s», должен быть [narrativ]"
                % (sid, b[0].tip, b[0].mysl)]
    return []


def zakon_a8(sid, sections):
    """А8: [dokazatelstvo] — последний блок слайда."""
    b = sections["matematika"]
    return ["%s: [dokazatelstvo] «%s» стоит не последним блоком" % (sid, blk.mysl)
            for i, blk in enumerate(b) if blk.tip == "dokazatelstvo" and i != len(b) - 1]


def zakon_a9(sid, sections):
    """А9: [opredelenie] — первое среди статусных блоков (не narrativ, не
    dokazatelstvo). Нарратив ПЕРЕД определением стоять может — речь о порядке
    среди СТАТУСНЫХ, не среди всех блоков (AKSIOMY-RAZMETKI.md §А9)."""
    stat = [blk for blk in sections["matematika"] if blk.tip in STATUSNYE_TIPY]
    if not stat or not any(blk.tip == "opredelenie" for blk in stat):
        return []
    if stat[0].tip != "opredelenie":
        return ["%s: [opredelenie] не первый среди статусных блоков (первый — [%s] «%s»)"
                % (sid, stat[0].tip, stat[0].mysl)]
    return []


def zakon_a10(sid, sections):
    """А10: [narrativ] не стоит между двумя ненарративными блоками."""
    b = sections["matematika"]
    return ["%s: [narrativ] «%s» стоит между [%s] и [%s]" % (sid, b[i].mysl, b[i-1].tip, b[i+1].tip)
            for i in range(1, len(b) - 1)
            if b[i].tip == "narrativ" and b[i-1].tip != "narrativ" and b[i+1].tip != "narrativ"]


def zakon_g1(sid, sections):
    """Г-1: несущий блок (тип ≠ narrativ) в «Математике» открывается жанровым
    ярлыком — «**Определение (…)**» / «**Утверждение (…)**» / «**Пример (…)**» /
    «*Доказательство…*». 🔴 ТОЛЬКО в «Математике» — на экране («Текст слайда —
    сжато») жанровым словом не открывается ни один блок (ZAMER-BLOKOV-L2.md Г-1:
    0 из 22 несущих на экране), проверка там сломает деку целиком (заход)."""
    out = []
    for blk in sections["matematika"]:
        if blk.tip == "narrativ":
            continue
        telo = blk.telo.lstrip()
        pat = ZHANROVYJ_YARLYK_RE.get(blk.tip, DOKAZATELSTVO_YARLYK_RE)
        if not pat.match(telo):
            out.append("%s: несущий блок [%s] «%s» не открывается жанровым ярлыком в «Математике»"
                        % (sid, blk.tip, blk.mysl))
    return out


def zakon_g2(sid, sections):
    """Г-2: у каждого блока «Математики» ровно одна врезка «> поле:…»."""
    out = []
    for blk in sections["matematika"]:
        n = len(POLE_VREZKA_RE.findall(blk.telo))
        if n != 1:
            out.append("%s: блок [%s] «%s» несёт %d врезок «> поле:», нужна ровно 1"
                        % (sid, blk.tip, blk.mysl, n))
    return out


def _markdown_spisok_bloki(telo):
    """Тело блока → списки пунктов, разбитые ТЕМ ЖЕ приёмом, что
    `build_deck.render_md` (пустая строка разделяет markdown-блоки; блок, где
    КАЖДАЯ строка начинается с «- », — список). Не голый regex по всему телу —
    иначе абзац, где «- » встретилась внутри прозы не на своей строке, ложно
    считался бы списком."""
    out = []
    for block in re.split(r"\n\s*\n", telo.strip("\n")):
        lines = [ln.strip() for ln in block.split("\n") if ln.strip()]
        if lines and all(ln.startswith("- ") for ln in lines):
            out.append(lines)
    return out


def zakon_g3(sid, sections):
    """Г-3 (двенадцатая): список из ОДНОГО пункта в [opredelenie]/[primer] на
    экране («Текст слайда») запрещён. 🔴 Проверяет только эту половину правила —
    «список ОБЯЗАТЕЛЕН при двух и более пунктах» не проверяется здесь намеренно
    (см. докстрока файла выше и NE_PROVERYAYU_VSEGDA)."""
    out = []
    for blk in sections["tekst"]:
        if blk.tip not in ("opredelenie", "primer"):
            continue
        for lst in _markdown_spisok_bloki(blk.telo):
            if len(lst) == 1:
                out.append("%s: [%s] «%s» несёт список из ОДНОГО пункта — запрещён при одном"
                            % (sid, blk.tip, blk.mysl))
    return out


def zakon_g6(sid, sections):
    """Г-6: в [primer]/[utverzhdenie]/[opredelenie] есть формула `$…$` —
    проверено в «Математике», где эти блоки развёрнуты полностью."""
    return ["%s: [%s] «%s» не несёт формулы $…$" % (sid, blk.tip, blk.mysl)
            for blk in sections["matematika"]
            if blk.tip in ("primer", "utverzhdenie", "opredelenie") and "$" not in blk.telo]


def zakon_g7(sid, sections):
    """Г-7: внутри одного блока не бывает двух жанровых ярлыков."""
    out = []
    for blk in sections["matematika"]:
        n = len(ZHANROVYJ_YARLYK_ANY_RE.findall(blk.telo))
        if n >= 2:
            out.append("%s: блок [%s] «%s» несёт %d жанровых ярлыков" % (sid, blk.tip, blk.mysl, n))
    return out


def zakon_g8(sid, sections):
    """Г-8 (переформулирован владельцем 12.08): двух НЕСУЩИХ блоков одного типа
    не бывает; нарративов сколько угодно. Несущий = тип ≠ narrativ."""
    tipy = [blk.tip for blk in sections["matematika"] if blk.tip != "narrativ"]
    dubli = sorted(t for t, n in Counter(tipy).items() if n > 1)
    if dubli:
        return ["%s: несущих блоков типа %s больше одного — сливать в один со списком (Г-8/Г-3)"
                % (sid, ", ".join(dubli))]
    return []


def zakon_g12(sid, params):
    """Г-12: tip_verstki: polosa_* требует непустого illustracii."""
    tv = params.get("tip_verstki") or ""
    if tv.startswith("polosa_") and not (params.get("illustracii") or []):
        return ["%s: tip_verstki '%s' без иллюстрации" % (sid, tv)]
    return []


# Законы, судящие РАЗБОР блоков одной карточки (нужен непустой raw_body, K3 —
# слайд без текста — их не касается вовсе, объявлено в NE_PROVERYAYU).
ZAKONY_BLOKOV = (
    ("А6", "слайд из одного блока — блок обязан быть [narrativ]", zakon_a6),
    ("А8", "[dokazatelstvo] — последний блок слайда", zakon_a8),
    ("А9", "[opredelenie] — первое среди статусных блоков", zakon_a9),
    ("А10", "[narrativ] не стоит между двумя ненарративными блоками", zakon_a10),
    ("Г-1", "несущий блок в «Математике» открывается жанровым ярлыком", zakon_g1),
    ("Г-2", "у каждого блока ровно одна врезка «> поле:mn»", zakon_g2),
    ("Г-3", "список из одного пункта в [opredelenie]/[primer] запрещён", zakon_g3),
    ("Г-6", "в [primer]/[utverzhdenie]/[opredelenie] есть формула $…$", zakon_g6),
    ("Г-7", "внутри блока нет двух жанровых ярлыков", zakon_g7),
    ("Г-8", "двух несущих блоков одного типа не бывает", zakon_g8),
)

# Законы, судящие ПОЛЯ ШАПКИ одной карточки — работают и на K3 (слайд без текста).
ZAKONY_PARAMOV = (
    ("Г-12", "tip_verstki: polosa_* требует непустого illustracii", zakon_g12),
)

# Реестр всех двенадцати ИМЕНОВАННО, в порядке таблицы захода — используется
# только для печати вердикта (все двенадцать поимённо, п.2 критерия готовности);
# сама проверка идёт через ZAKONY_BLOKOV/ZAKONY_PARAMOV/zakon_g15 выше.
VSE_ZAKONY_NAZVANIYA = tuple(name for name, _, _ in ZAKONY_BLOKOV + ZAKONY_PARAMOV) + ("Г-15",)


def zakon_g15(slide_order, info_by_sid):
    """Г-15: слайд с нулём несущих блоков стоит только первым, последним, сам
    несёт tip_verstki: razdelitel, либо стоит внутри непрерывного прогона
    слайдов-без-несущих, который касается границы или содержит разделитель."""
    n = len(slide_order)
    zero = [info_by_sid[sid][0] == 0 for sid in slide_order]
    is_razd = [info_by_sid[sid][1] == "razdelitel" for sid in slide_order]
    out = []
    for i, sid in enumerate(slide_order):
        if not zero[i]:
            continue
        l = i
        while l - 1 >= 0 and zero[l - 1]:
            l -= 1
        r = i
        while r + 1 < n and zero[r + 1]:
            r += 1
        if not (l == 0 or r == n - 1 or any(is_razd[l:r + 1])):
            out.append("%s: слайд без несущих блоков не на границе части и не рядом с разделителем" % sid)
    return out


def check_slide(sid, text, illustracii_pool, uzhe_vvedeno, vvodit_by_sid, faza=None):
    """Одна карточка → (issues: [str] красные — старый гейт как был,
    zakon_warns: {закон: [str]} жёлтые — заход zakony-v-gejt, никогда не красят,
    g15_info: (n_несущих, tip_verstki) — сырьё для Г-15, судится на уровне лекции
    целиком в check_lekcija, не здесь; tip_zheltye: [str] жёлтые находки захода
    tipologia-odna-os — Т1 без примера и без обоснования, NE_KLASSIFICIROVAN;
    sceny_zheltye: [str] жёлтые находки захода sceny-iz-blokov — Э4, потолок
    трёх блоков на слайде)."""
    zakon_warns = {name: [] for name, _, _ in ZAKONY_BLOKOV + ZAKONY_PARAMOV}
    g15_info = (0, None)
    tip_zheltye = []
    sceny_zheltye = []
    issues = _check_lifecycle_block(text, sid)
    try:
        params, raw_body = parse_card(text, sid=sid)
    except FormatSlaida as e:
        issues.append("%s: карточка не парсится: %s" % (sid, e))
        return issues, zakon_warns, g15_info, tip_zheltye, sceny_zheltye

    for f in _polya_dlya_fazy(faza):
        if _unfilled(params.get(f)):
            issues.append("%s: обязательное поле '%s' не заполнено" % (sid, f))

    issues.extend(_check_tip_slaida(sid, params))
    issues.extend(_check_zagolovok_na_ekrane(sid, params, faza))
    issues.extend(_check_vvodit_opiraetsya(sid, params, faza))
    tip_zheltye.extend(_check_ne_klassificirovan(sid, params))

    for name, _, fn in ZAKONY_PARAMOV:
        zakon_warns[name].extend(fn(sid, params))

    for name in params.get("illustracii") or []:
        if name not in illustracii_pool:
            issues.append("%s: иллюстрация '%s' не резолвится в пул лекции (illustracii/)"
                           % (sid, name))

    for item in params.get("opiraetsya_na") or []:
        # У12: инлайн-форма `opiraetsya_na: [{termin: X, vvedeno: Y}]` синтаксически
        # законна для INLINE_LIST_RE (formaty.py), но тот режет по запятой наивно и
        # кладёт СТРОКИ, не словари — `.get()` ниже ронял AttributeError трейсбеком
        # вместо внятного сообщения. Рабочая форма — многострочная (kartochka-slajda.md §2).
        if not isinstance(item, dict):
            issues.append(
                "%s: opiraetsya_na несёт элемент не в форме словаря (%r) — похоже на "
                "инлайн-запись '[{termin: X, vvedeno: Y}]', она не разбирается парсером "
                "шапки; рабочая форма многострочная: 'opiraetsya_na:\\n  - {termin: X, "
                "vvedeno: Y}' (kartochka-slajda.md §2)" % (sid, item))
            continue
        termin, vvedeno = item.get("termin"), item.get("vvedeno")
        vvedeno_na_slajde = termin in vvodit_by_sid.get(vvedeno, ())
        vvedeno_ranee = termin in uzhe_vvedeno
        if not (vvedeno_na_slajde or vvedeno_ranee):
            issues.append(
                "%s: термин '%s' (opiraetsya_na → vvedeno: %s) не введён на "
                "названном слайде (нет в его vvodit) и не перечислен в "
                "uzhe_vvedeno_ranee лекции" % (sid, termin, vvedeno))

    if not raw_body.strip():
        return issues, zakon_warns, g15_info, tip_zheltye, sceny_zheltye  # K3: слайд без текста — легален, дальше нечего проверять

    try:
        sections = bloki.parse_sections(raw_body, sid=sid)
    except bloki.FormatBlokov as e:
        issues.append(str(e))
        return issues, zakon_warns, g15_info, tip_zheltye, sceny_zheltye  # без разобранных секций состав/бюджет не проверить

    if sections["orphan_matematika"]:
        issues.append("%s: в разделе «Математика — развёрнуто» есть абзац вне блока: %r"
                       % (sid, sections["orphan_matematika"][:80]))
    if sections["orphan_tekst"]:
        issues.append("%s: в разделе «Текст слайда — сжато» есть абзац вне блока: %r"
                       % (sid, sections["orphan_tekst"][:80]))

    for m in bloki.check_composition(sections):
        issues.append("%s: состав блоков не совпадает — %s" % (sid, m))

    issues.extend(_check_sostav_tipa(sid, params, sections))
    tip_zheltye.extend(_check_primer_t1(sid, params, sections))

    issues.extend(_check_zapolnit_v_tele(sid, sections, faza))
    issues.extend(_check_centralnyj_blok(sid, params, sections))

    # Заход sceny-iz-blokov: Э2/Э3 красят, Э4 — жёлтый (см. докстроки функций выше).
    issues.extend(_check_sceny_vruchnuyu(sid, params, sections))
    issues.extend(_check_dokazatelstvo_scena(sid, sections))
    sceny_zheltye.extend(_check_potolok_blokov(sid, sections))

    # Заход kod_rebra-blokov.md, Э2: адресат обязателен для dokazatelstvo (красный),
    # желателен для primer (жёлтый).
    issues.extend(_check_dokazatelstvo_adresat(sid, params, sections))
    tip_zheltye.extend(_check_primer_adresat(sid, params, sections))

    budget = params.get("byudzhet_slov")
    if not _unfilled(budget):
        try:
            budget_n = float(budget)
        except ValueError:
            issues.append("%s: byudzhet_slov не число: %r" % (sid, budget))
        else:
            # 🔴 НЕ `render_section_markdown`: та ставит автотеги сцен `{@K}`, и они
            # попадали в счёт слов (16 карточек L2 из 23, +53 слова, на
            # `fundamentalnaya-gruppa` вердикт переворачивался). Счёт идёт по тексту,
            # который лектор произносит, — `bloki.render_section_for_word_count`.
            flat = bloki.render_section_for_word_count(sections["tekst"])
            n_words = len(flat.split())
            if n_words > budget_n:
                issues.append("%s: бюджет слов превышен: %d > %s" % (sid, n_words, budget))

    n_ness = sum(1 for blk in sections["matematika"] if blk.tip != "narrativ")
    g15_info = (n_ness, params.get("tip_verstki"))

    # Законы фазы 2 (заход zakony-v-gejt) судят ТЕЛА блоков — те написаны с выхода
    # фазы 3 (полная проверка, faza is None); на --faza 1/2 тела ещё пустые или
    # частичные, и проверка дала бы шум, а не находку.
    if faza is None:
        for name, _, fn in ZAKONY_BLOKOV:
            zakon_warns[name].extend(fn(sid, sections))

    return issues, zakon_warns, g15_info, tip_zheltye, sceny_zheltye


def check_lekcija(lekcija_dir, faza=None):
    """Папка лекции → (issues: [str], n_slides: int, zakon_warns: {закон: [str]},
    tip_zheltye: [str], tip_counter: Counter, sceny_zheltye: [str]). issues пуст —
    гейт зелёный. zakon_warns — жёлтые находки захода zakony-v-gejt, tip_zheltye —
    жёлтые находки захода tipologia-odna-os (Т1 без примера, NE_KLASSIFICIROVAN),
    sceny_zheltye — жёлтые находки захода sceny-iz-blokov (Э4, потолок трёх
    блоков); ни одни из них не влияют на rc. tip_counter — распределение
    `tip_slaida` по живым карточкам (клауза 4 критерия готовности захода
    tipologia-odna-os: печатать ДО/ПОСЛЕ, нулевую клетку называть явно)."""
    lekcija_dir = Path(lekcija_dir)
    zakon_warns_pusto = {name: [] for name, _, _ in ZAKONY_BLOKOV + ZAKONY_PARAMOV + (("Г-15", "", None),)}
    brief_path = lekcija_dir / "brief.md"
    if not brief_path.is_file():
        return (["%s: brief.md не найден" % lekcija_dir], 0, zakon_warns_pusto, [], Counter(), [])

    brief_params, _ = parse_front_matter(brief_path.read_text(encoding="utf-8"), sid="brief.md")
    uzhe_vvedeno = {item.get("termin") for item in (brief_params.get("uzhe_vvedeno_ranee") or [])
                    if isinstance(item, dict)}
    illustracii_pool = {p.name for p in (lekcija_dir / "illustracii").glob("*") if p.is_dir()} \
        if (lekcija_dir / "illustracii").is_dir() else set()

    slajdy_dir = lekcija_dir / "slajdy"
    slide_paths = sorted(slajdy_dir.glob("*/slaid.md"))
    if not slide_paths:
        return (["%s: нет карточек в %s (ищу */slaid.md)" % (lekcija_dir, slajdy_dir)], 0,
                 zakon_warns_pusto, [], Counter(), [])

    texts, vvodit_by_sid = {}, {}
    tip_counter = Counter()
    for p in slide_paths:
        sid = p.parent.name
        text = p.read_text(encoding="utf-8")
        texts[sid] = text
        try:
            params, _ = parse_card(text, sid=sid)
            vvodit_by_sid[sid] = set(params.get("vvodit") or [])
            tip = params.get("tip_slaida")
            tip_counter[tip if not _unfilled(tip) else "(не заполнено)"] += 1
        except FormatSlaida:
            vvodit_by_sid[sid] = set()
            tip_counter["(не парсится)"] += 1

    issues = []
    zakon_warns = {name: [] for name, _, _ in ZAKONY_BLOKOV + ZAKONY_PARAMOV}
    tip_zheltye = []
    sceny_zheltye = []
    g15_info_by_sid = {}
    for p in slide_paths:
        sid = p.parent.name
        slide_issues, slide_warns, g15_info, slide_tip_zheltye, slide_sceny_zheltye = check_slide(
            sid, texts[sid], illustracii_pool, uzhe_vvedeno, vvodit_by_sid, faza=faza)
        issues.extend(slide_issues)
        for name, warns in slide_warns.items():
            zakon_warns[name].extend(warns)
        tip_zheltye.extend(slide_tip_zheltye)
        sceny_zheltye.extend(slide_sceny_zheltye)
        g15_info_by_sid[sid] = g15_info

    # Г-15 судит ПОРЯДОК слайдов лекции (slide_order), не одну карточку — считаем
    # только при полной проверке, тем же условием, что и остальные ZAKONY_BLOKOV
    # (тела блоков нужны, чтобы посчитать несущие; на --faza 1/2 их ещё нет).
    slide_order = [s for s in (brief_params.get("slide_order") or []) if s in g15_info_by_sid]
    zakon_warns["Г-15"] = zakon_g15(slide_order, g15_info_by_sid) if faza is None and slide_order else []

    return issues, len(slide_paths), zakon_warns, tip_zheltye, tip_counter, sceny_zheltye


def _pechat_slepyh_zon(faza):
    """Слепые зоны — ВСЛУХ и на каждом прогоне, включая зелёный. Молчащий чекер
    читается как «проверено всё»: ровно так `--faza 1` и врал до этого захода."""
    zony = tuple(NE_PROVERYAYU.get(faza, ())) + NE_PROVERYAYU_VSEGDA
    print("НЕ проверяю: %d пункт(ов) — ниже поимённо" % len(zony))
    for z in zony:
        print("  · %s" % z)


ZAKONY_OPISANIYA = {name: opis for name, opis, _ in ZAKONY_BLOKOV + ZAKONY_PARAMOV}
ZAKONY_OPISANIYA["Г-15"] = "слайд с нулём несущих блоков — только на границе части или рядом с разделителем"


def _pechat_zakony(zakon_warns):
    """Все двенадцать законов фазы 2 поимённо, с вердиктом (п.2 критерия
    готовности захода zakony-v-gejt). Никогда не влияют на rc — см. докстрока
    ZAKONY_BLOKOV: порог включения — жёлтое, не красное."""
    print("ЗАКОНЫ ФАЗЫ 2 (жёлтое — находка, не гейт; %d из 12):" % len(VSE_ZAKONY_NAZVANIYA))
    for name in VSE_ZAKONY_NAZVANIYA:
        warns = zakon_warns.get(name, [])
        opis = ZAKONY_OPISANIYA[name]
        if warns:
            print("  ⚠ %s (%s) — нарушителей %d:" % (name, opis, len(warns)))
            for w in warns:
                print("      · %s" % w)
        else:
            print("  ✓ %s (%s) — нарушителей 0" % (name, opis))


def _pechat_tipologiya(tip_zheltye, tip_counter):
    """Заход tipologia-odna-os: Counter распределения по `tip_slaida` (клауза 4
    критерия готовности — нулевую клетку называть явно) + жёлтые находки (Т1 без
    примера/обоснования, NE_KLASSIFICIROVAN) — печатается ВСЕГДА, включая зелёный
    прогон, тем же принципом, что и `_pechat_zakony`/`_pechat_slepyh_zon`."""
    print("ТИПОЛОГИЯ (tip_slaida) — распределение:")
    for tip in tuple(sorted(tipy_slajdov.TIPY)) + (tipy_slajdov.TIP_SLUZHEBNYJ, tipy_slajdov.NE_KLASSIFICIROVAN):
        n = tip_counter.get(tip, 0)
        pometka = " ⚠ мёртвая или непокрытая клетка — назвать в отчёте" if n == 0 else ""
        print("  · %s: %d%s" % (tip, n, pometka))
    for k, n in sorted(tip_counter.items()):
        if k not in tipy_slajdov.TIPY and k not in (tipy_slajdov.TIP_SLUZHEBNYJ, tipy_slajdov.NE_KLASSIFICIROVAN):
            print("  ⚠ %s: %d (вне закрытого списка/не заполнено)" % (k, n))
    ne_klass_n = tip_counter.get(tipy_slajdov.NE_KLASSIFICIROVAN, 0)
    print("ТИПОЛОГИЯ (жёлтое — находка, не гейт; %d):" % len(tip_zheltye))
    if tip_zheltye:
        for w in tip_zheltye:
            print("  ⚠ %s" % w)
    else:
        print("  ✓ нарушителей 0")
    print("  · %s несёт %d карточк(а/и) из %d — норма: ровно 1"
          % (tipy_slajdov.NE_KLASSIFICIROVAN, ne_klass_n, sum(tip_counter.values())))


def _pechat_sceny(sceny_zheltye):
    """Заход sceny-iz-blokov: жёлтые находки Э4 (потолок трёх блоков) — печатается
    ВСЕГДА, включая зелёный прогон, тем же принципом, что и соседние `_pechat_*`."""
    print("СЦЕНЫ ИЗ БЛОКОВ (жёлтое — ориентир, не гейт; Э4, потолок %d блоков; %d):"
          % (POTOLOK_BLOKOV, len(sceny_zheltye)))
    if sceny_zheltye:
        for w in sceny_zheltye:
            print("  ⚠ %s" % w)
    else:
        print("  ✓ нарушителей 0")


def main():
    ap = argparse.ArgumentParser(description="Гейт карточек лекции — краснеет и не пропускает дальше")
    ap.add_argument("lekcija", help="путь к папке лекции (несёт brief.md + slajdy/)")
    ap.add_argument("--faza", type=int, default=None,
                     help="требования зависят от фазы, на выходе которой стоит карточка; "
                          "--faza 1 = выход интервью (тип слайда, имя/название, идея одной "
                          "фразой в zachem, минуты, размеченные блоки с мыслью, ровно один "
                          "центральный блок — ТЕЛО блоков ещё не пишется); остальные "
                          "значения = полная проверка, как без флага")
    args = ap.parse_args()

    issues, n, zakon_warns, tip_zheltye, tip_counter, sceny_zheltye = check_lekcija(
        args.lekcija, faza=args.faza)
    rezhim = "выход фазы %d" % args.faza if args.faza else "полная проверка"
    if issues:
        print("КРАСНЫЙ (%s): проверено %d из %d карточек, замечаний %d" % (rezhim, n, n, len(issues)))
        for it in issues:
            print("  ✗ %s" % it)
    else:
        print("ЗЕЛЁНЫЙ (%s): проверено %d из %d карточек, замечаний 0" % (rezhim, n, n))
    _pechat_zakony(zakon_warns)
    _pechat_tipologiya(tip_zheltye, tip_counter)
    _pechat_sceny(sceny_zheltye)
    _pechat_slepyh_zon(args.faza)
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
