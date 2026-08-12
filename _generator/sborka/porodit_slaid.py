#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Порождает карточку слайда фазы 2 ПО РАСКЛАДКЕ ТИПА — несущий принцип фазы 2
(заход porozhdenie-kartochki): «сначала решается что за слайд (тип · про что ·
какой блок центральный · какой вспомогательный), и только потом по этому описанию
порождаются файлы блоков; руками карточка не пишется». Нарушить правила раскладки
(`tipy_slajdov.TIPY`) нечем — не потому что запрещено, а потому что негде: слот,
которого раскладка не предусматривает, инструмент не заводит.

Форма блока (`### [tip] мысль`, три раздела тела) — ЧУЖАЯ зона (`bloki.py`, не
трогается); шапка карточки — ЧУЖОЙ шаблон (`bootstrap_lekcii.LIFECYCLE_TMPL`/
`SLIDE_CARD_TMPL`, не трогается, только используется). Реестр раскладок — свой
модуль `tipy_slajdov.py` (см. импорт ниже), по образцу `tipy.py`.

Тип центрального и вспомогательных блоков указывается ЯВНО (`tip:мысль`), а не
берётся из имени флага умалчиванием: без этого нельзя ни отличить у Т1 вспомогательный
`primer` от вспомогательного `utverzhdenie` (раскладка несёт оба слота), ни
СПРОСИТЬ невозможное — «у Т1 центральным просят не opredelenie» иначе неформулируемо
через CLI, а этого явно требует критерий готовности задачи (пять попыток породить
запрещённое). `--narrativ`/`--dokazatelstvo` — голой мыслью: тип уже в имени флага.

Режим `--sverit <лекция>` — БЕЗ порождения, только чтение: по каждой существующей
карточке резолвит `centralnyj_blok` в блок, определяет тип(ы)-кандидат(ы) по типу
центрального блока и сверяет фактический состав раздела «Математика — развёрнуто» с
раскладкой кандидата — тот же метод, что `TIPOLOGIA-SLAJDOV.md` часть 3.3 применяла
руками к Бюффону, здесь механически. НЕ решает Т2 против Т3 (полярность утверждения
сидит в тексте, не в структуре блоков — названо слепой зоной ниже) и не проверяет
время/вёрстку/содержание тел (Ф2.2/Ф2.4/Ф2.6 — вне зоны этого захода)."""
import argparse
import difflib
import re
import sys
from pathlib import Path

SBORKA = Path(__file__).resolve().parent
_GENERATOR = SBORKA.parent
sys.path.insert(0, str(SBORKA))
sys.path.insert(0, str(_GENERATOR))
import formaty  # noqa: E402
import bloki  # noqa: E402
import tipy_slajdov  # noqa: E402
from bootstrap_lekcii import LIFECYCLE_TMPL, SLIDE_CARD_TMPL  # noqa: E402 (READ-ONLY импорт чужого шаблона)

NE_PROVERYAYU = (
    "время блока (Ф2.2 — минутам сегодня негде лежать в карточке, долг Д56)",
    "вёрстку — tip_verstki/liniya/ярус (Ф2.4/Ф2.6 — вне зоны этого захода)",
    "содержание тел блоков (Ф2.6 — тела здесь заглушки, содержание пишется позже)",
    "разделение Т2 против Т3 в режиме --sverit (полярность утверждения сидит "
    "в тексте, структурой блоков не вычисляется — типологии часть 4 п.2)",
)


class PorozhdenieOtkaz(Exception):
    """Запрос нарушает раскладку типа — печатается ЦЕЛИКОМ (правило + что сделать
    вместо), ничего не пишется на диск, rc=1."""


def _pechat_ne_proveryayu():
    print("НЕ проверяю: %d пункт(ов) — ниже поимённо" % len(NE_PROVERYAYU))
    for p in NE_PROVERYAYU:
        print("  · %s" % p)


def _parse_tip_mysl(znachenie, flag):
    if ":" not in znachenie:
        raise PorozhdenieOtkaz(
            "%s требует форму 'tip:мысль' (tip — один из %s), получено %r без ':'"
            % (flag, ", ".join(bloki.TIPY_BLOKOV), znachenie))
    tip, mysl = znachenie.split(":", 1)
    tip, mysl = tip.strip(), mysl.strip()
    if tip not in bloki.TIPY_BLOKOV:
        raise PorozhdenieOtkaz(
            "%s: тип блока '%s' неизвестен. Допустимы: %s"
            % (flag, tip, ", ".join(bloki.TIPY_BLOKOV)))
    if not mysl:
        raise PorozhdenieOtkaz("%s: мысль блока не может быть пустой" % flag)
    return tip, mysl


def _razlozhit_po_slotam(tip_slaida, centralnyj, vspomogatelnye, narrativy, dokazatelstva):
    """Раскладывает пришедший запрос по слотам `tipy_slajdov.TIPY[tip_slaida]`.
    Возвращает [(tip, mysl)] в порядке слотов раскладки — заполненные слоты несут
    запрошенную мысль, необязательные незаполненные несут `NE_ZAPOLNYAEM` дважды
    (в мысли и в теле — решает `_body_dlya`). Кидает `PorozhdenieOtkaz` на первом
    нарушении, с указанием правила и раскладки типа целиком."""
    slots = tipy_slajdov.TIPY[tip_slaida]["slots"]
    central = tipy_slajdov.central_slot(tip_slaida)
    tip_c, mysl_c = centralnyj
    if tip_c != central.tip:
        raise PorozhdenieOtkaz(
            "запрет: у типа %s центральным блоком просят не [%s] (тип запроса: [%s]). "
            "Раскладка %s — что сделать вместо: смени --tip или смени тип центрального "
            "блока на '%s:<мысль>'" % (tip_slaida, central.tip, tip_c,
                                        tipy_slajdov.opisanie(tip_slaida), central.tip))

    # заполнено[i] — список (tip, mysl) для i-го слота raskladki, в порядке запроса
    zapolneno = [[] for _ in slots]
    idx_po_tipu = {}
    for i, s in enumerate(slots):
        idx_po_tipu.setdefault(s.tip, []).append(i)
    idx_central = next(i for i, s in enumerate(slots) if s.central)
    zapolneno[idx_central].append((tip_c, mysl_c))

    def _polozhit(tip_bloka, mysl, flag):
        idxs = idx_po_tipu.get(tip_bloka)
        if not idxs:
            raise PorozhdenieOtkaz(
                "запрет: раскладка %s не предусматривает блок типа [%s] (%s='%s'). "
                "Раскладка %s — что сделать вместо: убери этот блок или смени --tip"
                % (tip_slaida, tip_bloka, flag, mysl, tipy_slajdov.opisanie(tip_slaida)))
        i = idxs[0]
        slot = slots[i]
        if not slot.multi and zapolneno[i]:
            raise PorozhdenieOtkaz(
                "запрет: два НЕСУЩИХ блока одного типа [%s] на слайде %s — владелец: "
                "«если там два несущих примера/определения — объединить в один блок и "
                "поставить список». Раскладка %s — что сделать вместо: слей мысли '%s' "
                "и '%s' в ОДИН блок со списком"
                % (tip_bloka, tip_slaida, tipy_slajdov.opisanie(tip_slaida),
                   zapolneno[i][0][1], mysl))
        zapolneno[i].append((tip_bloka, mysl))

    for tip_v, mysl_v in vspomogatelnye:
        _polozhit(tip_v, mysl_v, "--vspomogatelnyj")
    for mysl_n in narrativy:
        _polozhit("narrativ", mysl_n, "--narrativ")
    for mysl_d in dokazatelstva:
        _polozhit("dokazatelstvo", mysl_d, "--dokazatelstvo")

    nedostayushchie = [s.bukva for i, s in enumerate(slots) if s.required and not zapolneno[i]]
    if nedostayushchie:
        raise PorozhdenieOtkaz(
            "запрет: у типа %s не задан обязательный блок [%s]. Раскладка %s — "
            "что сделать вместо: добавь блок этого типа (для Т3 --dokazatelstvo обязателен, "
            "в отличие от Т2)"
            % (tip_slaida, ", ".join(nedostayushchie), tipy_slajdov.opisanie(tip_slaida)))

    itog = []
    for i, s in enumerate(slots):
        if zapolneno[i]:
            itog.extend(zapolneno[i])
        else:
            itog.append((s.tip, tipy_slajdov.NE_ZAPOLNYAEM))
    return itog


def _body_dlya(bloki_itog):
    parts = []
    for tip, mysl in bloki_itog:
        telo = tipy_slajdov.NE_ZAPOLNYAEM if mysl == tipy_slajdov.NE_ZAPOLNYAEM else formaty.ZAPOLNIT
        parts.append("### [%s] %s\n%s" % (tip, mysl, telo))
    blok_md = "\n\n".join(parts)
    return ("## Математика — развёрнуто\n%s\n\n"
            "## Текст слайда — сжато\n%s\n\n"
            "## Правки\n- %s\n" % (blok_md, blok_md, formaty.ZAPOLNIT))


def sostavit_kartochku(imya, tip_slaida, bloki_itog):
    idx_central = next(i for i, s in enumerate(tipy_slajdov.TIPY[tip_slaida]["slots"]) if s.central)
    mysl_c = bloki_itog[idx_central][1]
    lifecycle = LIFECYCLE_TMPL % {"imya": imya}
    text = SLIDE_CARD_TMPL % {"imya": imya, "zap": formaty.ZAPOLNIT,
                               "lifecycle": lifecycle, "body": _body_dlya(bloki_itog)}
    text = re.sub(r"^centralnyj_blok: .*$",
                  lambda m: "centralnyj_blok: %s" % mysl_c,
                  text, count=1, flags=re.M)
    return text


def porodit(lekcija_dir, imya, tip_slaida, centralnyj, vspomogatelnye, narrativy, dokazatelstva):
    if tip_slaida not in tipy_slajdov.TIPY:
        raise PorozhdenieOtkaz(
            "тип '%s' неизвестен. Допустимы: %s"
            % (tip_slaida, ", ".join(sorted(tipy_slajdov.TIPY))))
    bloki_itog = _razlozhit_po_slotam(tip_slaida, centralnyj, vspomogatelnye, narrativy, dokazatelstva)
    text = sostavit_kartochku(imya, tip_slaida, bloki_itog)

    lekcija_dir = Path(lekcija_dir)
    slide_dir = lekcija_dir / "slajdy" / imya
    card = slide_dir / "slaid.md"
    if card.is_file():
        staroe = card.read_text(encoding="utf-8")
        if staroe == text:
            print("%s: уже породил бы то же самое, диф пуст" % card)
            return 0
        print("%s: карточка уже существует — НЕ перезаписываю, диф (что породил бы ↔ что лежит):"
              % card)
        diff = difflib.unified_diff(text.splitlines(keepends=True),
                                      staroe.splitlines(keepends=True),
                                      fromfile="породил-бы", tofile="лежит-на-диске")
        sys.stdout.writelines(diff)
        return 0

    slide_dir.mkdir(parents=True, exist_ok=True)
    card.write_text(text, encoding="utf-8")
    print("породил: %s (тип %s, %d блок(ов))" % (card, tip_slaida, len(bloki_itog)))
    for tip, mysl in bloki_itog:
        pometka = " [%s]" % tipy_slajdov.NE_ZAPOLNYAEM if mysl == tipy_slajdov.NE_ZAPOLNYAEM else ""
        print("  · [%s] %s%s" % (tip, mysl, pometka))
    return 0


def _sverit_raskladku(tip_slaida, bloki_matematiki):
    slots = tipy_slajdov.TIPY[tip_slaida]["slots"]
    core_slots = [s for s in slots if s.tip != "narrativ"]
    core_actual = [b.tip for b in bloki_matematiki if b.tip != "narrativ"]
    expected_order = [s.tip for s in core_slots]
    extra = sorted(set(core_actual) - set(expected_order))
    if extra:
        return False, "блок(и) вне раскладки %s: %s" % (tip_slaida, ", ".join(extra))
    missing = [s.tip for s in core_slots if s.required and s.tip not in core_actual]
    if missing:
        return False, "не хватает обязательного блока: %s" % ", ".join(missing)
    present_expected = [t for t in expected_order if t in core_actual]
    schyot = {}
    for t in core_actual:
        schyot[t] = schyot.get(t, 0) + 1
    povtory = sorted(t for t, c in schyot.items() if c > 1)
    if core_actual == present_expected and not povtory:
        return True, None
    if sorted(core_actual) == sorted(present_expected):
        detali = ("повтор блока: %s" % ", ".join(povtory)) if povtory else \
            "порядок ядра: ожидали %s, получили %s" % (present_expected, core_actual)
        return "natyazhka", detali
    return False, "порядок ядра разошёлся: ожидали %s, получили %s" % (present_expected, core_actual)


def sverit(lekcija_dir):
    lekcija_dir = Path(lekcija_dir)
    cards = sorted((lekcija_dir / "slajdy").glob("*/slaid.md"))
    if not cards:
        raise PorozhdenieOtkaz("%s/slajdy: карточек не найдено" % lekcija_dir)
    stroki = []
    for card in cards:
        sid = card.parent.name
        text = card.read_text(encoding="utf-8")
        try:
            params, raw_body = formaty.parse_card(text, sid)
        except formaty.FormatSlaida as e:
            stroki.append((sid, "?", "ошибка чтения: %s" % e))
            continue
        if not raw_body.strip():
            stroki.append((sid, "?", "тело пусто (K3) — раскладку сверить нечем"))
            continue
        try:
            sections = bloki.parse_sections(raw_body, sid=sid)
        except bloki.FormatBlokov as e:
            stroki.append((sid, "?", "ошибка разбора блоков: %s" % e))
            continue
        blocks = sections["matematika"]
        central_val = params.get("centralnyj_blok")
        central_block = next((b for b in blocks if b.mysl == central_val), None)
        if central_block is None:
            stroki.append((sid, "?", "centralnyj_blok '%s' не резолвится в блок «Математики»"
                           % central_val))
            continue
        kandidaty = [t for t in tipy_slajdov.TIPY
                     if tipy_slajdov.central_slot(t).tip == central_block.tip]
        if not kandidaty:
            stroki.append((sid, "не типизирован",
                           "тип центрального блока '%s' central ни у одного типа" % central_block.tip))
            continue
        verdikty = []
        for t in kandidaty:
            sovpalo, primechanie = _sverit_raskladku(t, blocks)
            slovo = {"True": "ЛЁГ", "False": "НЕ ЛЁГ",
                     "natyazhka": "ЛЁГ С НАТЯЖКОЙ"}[str(sovpalo)]
            verdikty.append("%s: %s%s" % (t, slovo, (" (%s)" % primechanie) if primechanie else ""))
        stroki.append((sid, "/".join(kandidaty), "; ".join(verdikty)))
    return stroki


def main():
    ap = argparse.ArgumentParser(
        description="Порождает карточку слайда по раскладке типа (несущий принцип фазы 2) "
                     "или сверяет раскладку существующей деки (--sverit)")
    ap.add_argument("lekcija", help="путь к папке лекции")
    ap.add_argument("--imya", help="id слайда (папка slajdy/<imya>/)")
    ap.add_argument("--tip", choices=sorted(tipy_slajdov.TIPY), help="тип слайда Т1..Т5")
    ap.add_argument("--centralnyj", help="'tip:мысль' центрального блока")
    ap.add_argument("--vspomogatelnyj", action="append", default=[],
                     help="'tip:мысль' вспомогательного несущего блока (можно повторять)")
    ap.add_argument("--narrativ", action="append", default=[],
                     help="мысль нарративного блока (можно повторять)")
    ap.add_argument("--dokazatelstvo", action="append", default=[],
                     help="мысль блока доказательства")
    ap.add_argument("--sverit", action="store_true",
                     help="БЕЗ порождения: сверить раскладку всех карточек <лекция> "
                          "с типологией по centralnyj_blok")
    args = ap.parse_args()

    try:
        if args.sverit:
            stroki = sverit(args.lekcija)
            n = len(stroki)
            print("сверено %d карточек из %d" % (n, n))
            print("%-28s %-14s %s" % ("слайд", "тип-кандидат", "вердикт"))
            for sid, tip, verdikt in stroki:
                print("%-28s %-14s %s" % (sid, tip, verdikt))
            _pechat_ne_proveryayu()
            return 0

        if not (args.imya and args.tip and args.centralnyj):
            raise PorozhdenieOtkaz("для порождения нужны --imya, --tip и --centralnyj "
                                    "(для сверки деки без порождения — флаг --sverit)")
        centralnyj = _parse_tip_mysl(args.centralnyj, "--centralnyj")
        vspomogatelnye = [_parse_tip_mysl(v, "--vspomogatelnyj") for v in args.vspomogatelnyj]
        rc = porodit(args.lekcija, args.imya, args.tip, centralnyj, vspomogatelnye,
                     args.narrativ, args.dokazatelstvo)
        _pechat_ne_proveryayu()
        return rc
    except PorozhdenieOtkaz as e:
        print("❌ %s" % e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
