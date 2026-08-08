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
import re
import sys
from pathlib import Path

SBORKA = Path(__file__).resolve().parent
_GENERATOR = SBORKA.parent
sys.path.insert(0, str(SBORKA))
sys.path.insert(0, str(_GENERATOR))
from formaty import ZAPOLNIT, FRONT_RE, strip_lifecycle_block  # noqa: E402
from build_deck import parse_brief  # noqa: E402 (READ-ONLY импорт — единый парсер brief.md)

# Поля лекции — Я1 §1 целиком (кроме двух, вычисляемых при бутстрапе: id/slide_order
# несут структуру, не замысел, заполняются ЗДЕСЬ, а не владельцем).
POLYA_LEKCII = ("title", "dlya_kogo", "zhanr", "dlitelnost_minut", "zamer_tempa",
                "skvoznaya_liniya")

# Р1б захода porcia-1-zamknut-konvejer (П0: «дисциплина, которую невозможно
# игнорировать физически») — блок «что дальше» вшивается СТРОГО до шапки, одним
# HTML-комментарием; `gejt_kartochki.py` его требует (Я1 §6-бис, `formaty.py`
# режет перед разбором шапки). Формат строки — Я4-образец `bootstrap_zahod.py`,
# перенесённый на карточку слайда: `ФАЗА N (имя): что :: команда`, команды —
# из живого кода (`--help`), не из захода. `slaid.py` уже принимает и папку
# слайда, и файл `slaid.md` (Р4); `deck.py` уже подбирает типографику сам,
# пока явные kegl_px/liniya в шапке не проставлены руками (Р3).
LIFECYCLE_TMPL = """<!--
ЧТО ДАЛЬШЕ С ЭТИМ ФАЙЛОМ (вшито bootstrap_lekcii.py — не редактировать руками,
gejt_kartochki.py краснеет на отсутствии этого блока или неполном наборе фаз).
Формат строки: ФАЗА N (имя фазы): что делается :: команда.

ФАЗА 1 (интервью): назвать nazvanie/tip_idei (типы — formaty.TIPY_IDEI)/zachem (идея одной фразой)/minuty, разметить блоки в ОБОИХ разделах — ### [tip] мысль, тела ещё пустые — назвать centralnyj_blok и заполнить vvodit/opiraetsya_na (какие термины слайд вводит и на какие уже введённые опирается — единственная машинная проверка порядка понятий; типы divider/cover/vizitka/closing освобождены) :: python3 _generator/sborka/gejt_kartochki.py --faza 1 <лекция>
ФАЗА 2 (раскадровка): решить tip_verstki/liniya/akcent/vazhnost/byudzhet_slov/zagolovok_na_ekrane в шапке (zagolovok_na_ekrane — пустая строка легальна, слайд может быть без заголовка на экране, но пометку 'заполнить' обязана снять здесь), написать тела блоков «Математика — развёрнуто» по разметке фазы 1 :: python3 _generator/sborka/gejt_kartochki.py --faza 2 <лекция>
ФАЗА 2.5 (смета вмещения): УЗНАТЬ БЮДЖЕТ В СТРОКАХ ДО ТОГО, КАК ТЕКСТ НАПИСАН — сколько строк даёт выбранная пара tip_verstki/liniya и сколько блоков в них влезет; браузер не нужен :: python3 _generator/sborka/smeta.py --byudzhet <tip_verstki> <liniya>
ФАЗА 3 (текст слайдов): написать «Текст слайда — сжато» тем же составом блоков, что в «Математике» :: python3 _generator/sborka/gejt_kartochki.py <лекция>
ФАЗА 3.1 (смета по написанному): проверить чистым питоном, влезает ли НАПИСАННЫЙ текст — до всякой сборки и без браузера :: python3 _generator/sborka/smeta.py <лекция>
ФАЗА 3.5 (кэш формул): собрать <лекция>/math/katex.json из карточек ДО первой сборки — без него slaid.py/deck.py откажутся молча собирать с MISSING-MATH (заплатка sborka-l2-fazy-4-7, П2/П3) :: node _generator/sborka/kesh_formul.js <лекция>
ФАЗА 3.9 (ЗАКРЫТИЕ ФАЗЫ 3 — вмещение): текст физически не обрезан `overflow:hidden` на скомпилированном слайде. Гейт бюджета слов краснеть тут НЕ УМЕЕТ: он считает знаки, а не вёрстку, и был зелёным ровно там, где со слайда пропало четыре абзаца из семи. Требует скомпилированных слайдов и браузера — потому стоит ЗДЕСЬ, а не на фазе 2 :: python3 _generator/sborka/slaid.py <лекция>/slajdy/<sid> -o /tmp/<sid>.html && python3 _generator/sborka/gejt_vmeshcheniya.py /tmp/*.html
ФАЗА 4 (вёрстка): собрать и посмотреть слайд отдельно :: python3 _generator/sborka/slaid.py <лекция>/slajdy/%(imya)s -o /tmp/%(imya)s.html
ФАЗА 5 (иллюстрации): назвать файлы в illustracii, положить risunok.svg (или risunok.html) в <лекция>/illustracii/<имя>/ :: python3 _generator/sborka/gejt_kartochki.py <лекция>
ФАЗА 6 (сборка и QA): собрать весь дек — типографика подбирается автоматически, явные kegl_px/liniya в шапке не перетираются :: python3 _generator/sborka/deck.py <лекция> -o <лекция>/dist/index.html
-->
"""


def _lifecycle_text(imya):
    return LIFECYCLE_TMPL % {"imya": imya}


# Р1а — тело порождается тремя каноническими разделами (bloki.ZAGOLOVKI) сразу,
# «Математика» и «Текст слайда» — ОДИНАКОВЫМ единственным блоком-пометкой:
# `bloki.check_composition` сравнивает состав (tip, mysl) между разделами, и
# идентичная пара проходит гейт БЕЗ единой правки тела (Р1 критерий 1) — автор
# трогает только шапку, пока не берётся за содержание. Голая пометка без блочной
# обёртки (`### [tip] …`) недопустима: bloki.py считает любой текст вне блока
# осиротевшим абзацем и красит гейт даже на свежем бутстрапе — это разнесло бы
# Р1 и Р2 (там нужен зелёный `--faza 1` на нетронутой карточке).
BODY_TMPL = """## Математика — развёрнуто
### [narrativ] %(zap)s
%(zap)s

## Текст слайда — сжато
### [narrativ] %(zap)s
%(zap)s

## Правки
- %(zap)s
"""


def _body_text():
    return BODY_TMPL % {"zap": ZAPOLNIT}


SLIDE_CARD_TMPL = """%(lifecycle)s---
imya: %(imya)s
nazvanie: %(zap)s
zagolovok_na_ekrane: %(zap)s
tip_idei: %(zap)s
zachem: %(zap)s
akcent: %(zap)s
centralnyj_blok: %(zap)s
kommentarij_lektoru: %(zap)s
minuty: %(zap)s
vazhnost: %(zap)s
byudzhet_slov: %(zap)s
tip_verstki: %(zap)s
liniya: %(zap)s
matematika_iz: []
illustracii: []
vvodit: []
opiraetsya_na: []
bez_opredeleniya_namerenno: []
status: v_deke
---
%(body)s"""

# Поля, которые заход format-kartochki-faza-1 добавил в шапку, и якорь, ПОСЛЕ
# которого каждое вставляется миграцией в уже существующие карточки. Порядок и
# соседство значат: `tip_idei` рядом с названием (что это за слайд),
# `centralnyj_blok` рядом с акцентом (что на нём главное), `matematika_iz` —
# рядом с иллюстрациями, обе ссылки наружу карточки. Якоря нет в старой карточке
# → поле дописывается в конец шапки, а не теряется.
NOVYE_POLYA_SLAJDA = (
    ("tip_idei", "zagolovok_na_ekrane", ZAPOLNIT),
    ("centralnyj_blok", "akcent", ZAPOLNIT),
    ("matematika_iz", "liniya", "[]"),
)
NOVYE_POLYA_LEKCII = (
    ("zamer_tempa", "dlitelnost_minut", ZAPOLNIT),
)


def _slide_card_text(imya):
    return SLIDE_CARD_TMPL % {"imya": imya, "zap": ZAPOLNIT,
                               "lifecycle": _lifecycle_text(imya), "body": _body_text()}


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


def _vstavit_polya(text, novye, sid):
    """Дописать недостающие поля в YAML-шапку ТЕКСТОМ, не круг через парсер.
    Круг через `parse_front_matter` → сериализация потерял бы порядок полей,
    кавычки и всё, чего парсер не хранит; шапку живой карточки владелец читает
    глазами, и переставленные поля — это переделка, которой Д-6 и запрещает.
    Возвращает (новый текст, [имена дописанных полей])."""
    m = FRONT_RE.match(text)
    if not m:
        raise SystemExit("%s: нет YAML-шапки (---...---) — мигрировать нечего" % sid)
    head_lines = m.group(1).split("\n")
    dopisano = []
    for key, yakor, znachenie in novye:
        if any(re.match(r"^%s\s*:" % re.escape(key), ln) for ln in head_lines):
            continue  # поле уже есть — не трогаем ЗНАЧЕНИЕ, каким бы оно ни было
        stroka = "%s: %s" % (key, znachenie)
        idx = next((i for i, ln in enumerate(head_lines)
                    if re.match(r"^%s\s*:" % re.escape(yakor), ln)), None)
        head_lines.insert(len(head_lines) if idx is None else idx + 1, stroka)
        dopisano.append(key)
    if not dopisano:
        return text, []
    return "---\n%s\n---\n%s" % ("\n".join(head_lines), m.group(2)), dopisano


def migrirovat(lekcija_dir):
    """Д-6 захода format-kartochki-faza-1 — поднять УЖЕ СУЩЕСТВУЮЩЕЕ дерево лекции
    до формата, который требует гейт выхода фазы 1. Ровно два действия:

      · дописать недостающие поля шапки со значением-заглушкой (заполненного НЕ
        трогаем — ни в одном поле, ни при повторном прогоне);
      · перешить машинный блок «что дальше» на текущий `LIFECYCLE_TMPL` (он
        объявлен «вшито bootstrap_lekcii.py — не редактировать руками», значит
        его дом здесь; теперь он обязан начинаться с ФАЗЫ 1).

    Тело карточки не трогается вовсе: разметка блоков — работа владельца на
    интервью, а не бутстрапа. Идемпотентно: второй прогон даёт нулевой диф.
    Зачем это команда, а не инструкция «допишите поле»: формат меняется, пока
    интервью по живой лекции уже идёт, и цель владельца дословно — «не
    переделывать слайды»."""
    lekcija_dir = Path(lekcija_dir)
    brief = lekcija_dir / "brief.md"
    if not brief.is_file():
        raise SystemExit("%s: brief.md не найден — это не дерево лекции" % lekcija_dir)

    tronuto = []
    t = brief.read_text(encoding="utf-8")
    t2, dopisano = _vstavit_polya(t, NOVYE_POLYA_LEKCII, "brief.md")
    if t2 != t:
        brief.write_text(t2, encoding="utf-8")
        tronuto.append("brief.md: +%s" % ", ".join(dopisano))

    for card in sorted((lekcija_dir / "slajdy").glob("*/slaid.md")):
        sid = card.parent.name
        t = card.read_text(encoding="utf-8")
        blok_ustarel = not t.startswith(_lifecycle_text(sid))
        # Поля вставляются в шапку ДО того, как впереди встанет блок «что дальше»:
        # `FRONT_RE` требует `---` в самом начале текста, а блок — HTML-комментарий
        # перед ним. Поэтому режем блок, правим шапку, пришиваем блок заново.
        _, bez_bloka = strip_lifecycle_block(t)
        bez_bloka, dopisano = _vstavit_polya(bez_bloka, NOVYE_POLYA_SLAJDA, sid)
        novyj = _lifecycle_text(sid) + bez_bloka
        if novyj == t:
            continue
        card.write_text(novyj, encoding="utf-8")
        chto = ["+%s" % k for k in dopisano]
        if blok_ustarel:
            chto.append("блок «что дальше» перешит")
        tronuto.append("%s: %s" % (sid, ", ".join(chto)))
    return tronuto


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
    ap.add_argument("--migraciya", action="store_true",
                     help="поднять УЖЕ СУЩЕСТВУЮЩЕЕ дерево до текущего формата: дописать "
                          "недостающие поля шапки заглушкой и перешить машинный блок «что "
                          "дальше». Заполненного не трогает, тело карточки не трогает вовсе, "
                          "идемпотентно (второй прогон — нулевой диф)")
    args = ap.parse_args()

    if args.migraciya:
        tronuto = migrirovat(args.lekcija)
        if not tronuto:
            print("миграция: дерево уже в текущем формате, изменений 0")
            return 0
        print("миграция: тронуто файлов %d" % len(tronuto))
        for s in tronuto:
            print("  · %s" % s)
        return 0

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
