#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ГЕЙТ ЗАКАЗА ИЛЛЮСТРАЦИЙ — иллюстрация без заказа не собирается.

    python3 _generator/tools/gejt_illyustracij.py <лекция>
    python3 _generator/tools/gejt_illyustracij.py <лекция> --tiho   # только код возврата

Код возврата: 0 — чисто, 1 — есть нарушения. Годится в ворота.

ЗАЧЕМ. `zakaz.md` объявлен в `SKILL.md` (`slajdy`) обязательным выходом фазы 2 и входом фазы 5 —
и до этого гейта его не читала ни одна команда (доказано `grep`, заход `provod-illyustracij`,
И0). Класс отказа «заказ и приёмка иллюстрации» — 112 записей на пяти фазах картотеки фабрики,
самый тяжёлый безрычаговый класс. Три проверки ниже целятся ровно в него:

  1. слайд ссылается в `illustracii:` на имя, у которого нет `zakaz.md` в пуле лекции;
  2. `zakaz.md` есть, но не все пять полей заполнены (заглушка «заполнить» — тоже незаполнено);
  3. в пуле лежит `zakaz.md`, на который не ссылается ни один слайд — заказ-сирота.

Пять полей заказа — по ANKETA G2 дословно (`_studio/konvejer/04.5-intervyu/ANKETA.md`), не по
вкусу: что изображено · сколько объектов и как подписаны · что происходит · чего рисовать НЕ
надо · размер. Формат специфицирован в `disciplina/skills/slajdy/SKILL.md`, фаза 2, РЕШЕНИЯ ФАЗЫ
п.4 — канон там, здесь только проверка.

⚠ Обратная совместимость: лекция вообще без иллюстраций (`illustracii: []` у всех слайдов, пул
пуст или отсутствует) — ЗЕЛЁНАЯ, не красная. Такие лекции есть сегодня, ломать их нельзя.

🔴 Сирота пула — здесь жёсткий `rc=1`, не мягкое предупреждение: либо картинку забыли поставить
на слайд, либо заказ устарел, оба случая дорогие (заход `provod-illyustracij`, И3). Это решение
СТРОЖЕ старой заметки в `SKILL.md` фазы 5 ГЕЙТ ВЫХОДА про «мягкое ⚠» — та описывает суждение
верификатора-субагента (стилевое), этот гейт — счётную проверку; расхождение названо в `SKILL.md`
рядом со старой строкой, не тихо переопределено.

Свой минимальный парсер шапки слайда и `zakaz.md` — НЕ импортирует `_generator/sborka/formaty.py`.
Причина «чужая зона, правится параллельным заходом `format-kartochki-faza-1`» отпала: та ветка
влита. Осталась другая, более твёрдая — `formaty.py` тянет за собой `build_deck`/`bloki` (рендер
и разбор блоков), а этот гейт держит идиому «stdlib, без сторонних зависимостей» из абзаца ниже;
импорт `formaty` привязал бы зелёный/красный этого гейта к состоянию совсем другого куска сборки.
Нужно только срезать lifecycle-блок и прочитать поле `illustracii:` в инлайн-списке — единственная
форма, которую `SKILL.md:494-498` объявляет легальной для списковых полей карточки; для этого
достаточно той же регулярки, что и в `formaty.LIFECYCLE_RE`, продублированной здесь одной строкой.

Идиома семьи (`_generator/DVIZHKI.md`): stdlib, детерминизм, без сети и pip, `exit 1` при красном.

Гейт НЕ встроен в сборку (`deck.py`) — вызывается отдельной командой; решение о встраивании не
принято этим заходом (см. отчёт).
"""
import re
import sys
from pathlib import Path

POLYA = [
    ("chto_izobrazheno", "что изображено"),
    ("skolko_i_podpisi", "сколько объектов и как подписаны"),
    ("chto_proishodit", "что происходит"),
    ("chego_ne_nado", "чего рисовать не надо"),
    ("razmer", "размер"),
]
ZAGLUSHKA = "заполнить"

FRONT_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
ILL_RE = re.compile(r"^illustracii:\s*\[(.*)\]\s*$")
# та же форма, что `formaty.LIFECYCLE_RE` — карточка нового формата (bootstrap_lekcii.py)
# несёт этот HTML-комментарий СТРОГО перед шапкой; см. докстринг выше про дубликат.
LIFECYCLE_RE = re.compile(r"^<!--(.*?)-->\s*", re.S)


def _read(p):
    return p.read_text(encoding="utf-8")


def _strip_lifecycle(text):
    """Срезает вшитый bootstrap_lekcii.py блок «что дальше», если он есть. Карточка
    старого формата (блока нет) возвращается без изменений — обратная совместимость."""
    m = LIFECYCLE_RE.match(text)
    return text[m.end():] if m else text


def slide_illustracii(slaid_path):
    """slaid.md → список имён из поля `illustracii:` (инлайн-список), уже нормализованных
    через stem — так же, как компилятор `_generator/sborka/slaid.py:load_illustrations`
    нормализует имя файла до имени папки пула."""
    text = _strip_lifecycle(_read(slaid_path))
    m = FRONT_RE.match(text)
    if not m:
        raise SystemExit("%s: нет YAML-шапки (---...---)" % slaid_path)
    for line in m.group(1).splitlines():
        im = ILL_RE.match(line.strip())
        if im:
            inner = im.group(1).strip()
            if not inner:
                return []
            return [Path(x.strip().strip('"')).stem for x in inner.split(",") if x.strip()]
    return []


def parse_zakaz(zakaz_path):
    """zakaz.md → dict {канон-ключ: значение}. Плоские строки `метка: значение`, без `---`
    (живой формат образцов пула) — метка сопоставляется по началу строки, регистронезависимо."""
    text = _read(zakaz_path)
    najdeno = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        label, val = line.split(":", 1)
        label = label.strip().lower()
        val = val.strip()
        for kod, metka in POLYA:
            if label == metka:
                najdeno[kod] = val
    return najdeno


def nezapolneno(val):
    return val is None or val.strip() == "" or val.strip().lower() == ZAGLUSHKA


def proverit(lekcija_dir):
    """→ (bedy: [(klass, text)], svodka: dict) | (None, None) — папки лекции нет вовсе.
    🔴 Несуществующий путь — это НЕ «лекция без иллюстраций» (тот случай легален и зелёный),
    а кривой вход: не даём ему тихо превратиться в зелёный, дом гейта не проверив (класс
    ошибки — swallowed-флаг `bootstrap_arka.py`, см. докстринг check_tool_contract.py)."""
    lekcija = Path(lekcija_dir)
    if not lekcija.is_dir():
        return None, None
    slajdy_dir = lekcija / "slajdy"
    pool_dir = lekcija / "illustracii"

    slaid_files = sorted(slajdy_dir.glob("*/slaid.md")) if slajdy_dir.is_dir() else []
    ssylki = {}  # имя иллюстрации → [sid, ...]
    for sp in slaid_files:
        sid = sp.parent.name
        for imya in slide_illustracii(sp):
            ssylki.setdefault(imya, []).append(sid)

    zakazy = sorted(p.parent.name for p in pool_dir.glob("*/zakaz.md")) if pool_dir.is_dir() else []

    bedy = []

    # 1. слайд ссылается на имя без zakaz.md в пуле
    for imya, sidy in sorted(ssylki.items()):
        if imya not in zakazy:
            bedy.append(("Z1", "картинка '%s' (слайд %s) — нет zakaz.md в пуле %s"
                          % (imya, ", ".join(sidy), pool_dir)))

    # 2. zakaz.md есть, но не все пять полей заполнены
    for imya in zakazy:
        polya = parse_zakaz(pool_dir / imya / "zakaz.md")
        propuski = [metka for kod, metka in POLYA if nezapolneno(polya.get(kod))]
        if propuski:
            bedy.append(("Z2", "заказ '%s' — не заполнено: %s" % (imya, ", ".join(propuski))))

    # 3. заказ-сирота — никто не ссылается
    for imya in zakazy:
        if imya not in ssylki:
            bedy.append(("Z3", "заказ '%s' в пуле %s — сирота, ни один слайд не ссылается"
                         % (imya, pool_dir)))

    svodka = {
        "slaidov": len(slaid_files),
        "ssylok": len(ssylki),
        "zakazov": len(zakazy),
    }
    return bedy, svodka


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    tiho = "--tiho" in sys.argv
    if not args:
        print(__doc__.strip().splitlines()[2])
        sys.exit(2)

    bedy, svodka = proverit(args[0])

    if svodka is None:
        sys.stderr.write("%s: не папка лекции (путь не существует)\n" % args[0])
        sys.exit(2)

    if not tiho:
        print("── ГЕЙТ ЗАКАЗА ИЛЛЮСТРАЦИЙ (gejt_illyustracij) ──")
        print("  %s" % args[0])
        print("  слайдов: %d · ссылок на иллюстрации: %d · заказов в пуле: %d"
              % (svodka["slaidov"], svodka["ssylok"], svodka["zakazov"]))
        print("\n  ЧЕГО ЭТОТ ГЕЙТ НЕ ПРОВЕРЯЕТ:")
        print("     · [стиль] иллюстрация действительно отвечает своему zakaz.md — верификатор-субагент")
        print("     · [форма] var(--x) внутри рисунка определены в токенах — линтер build_deck.py")
        print("     · [полнота] родовые решения ступени 1 сита прочитаны — вне этого гейта")

    if bedy:
        if not tiho:
            print("\n  ✗ КРАСНЫЙ — замечаний %d:" % len(bedy))
            for k, v in bedy:
                print("     %-3s %s" % (k, v))
        sys.exit(1)

    if not tiho:
        print("\n  ✓ ЗЕЛЁНЫЙ")
    sys.exit(0)


if __name__ == "__main__":
    main()
