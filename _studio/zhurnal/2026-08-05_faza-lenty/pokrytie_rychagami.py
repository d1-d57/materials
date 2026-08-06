#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сколько записей дома НАКРЫТО рычагом — метрика, которой у домов не было (заход
`kod_pereschet-i-schetchik.md`, §2.2). Дома знали свой счёт и не знали своего покрытия, поэтому
фраза владельца «все инциденты, которые были собраны, — для них теперь работают рычаги» не могла
быть ни подтверждена, ни опровергнута.

ЧТО СЧИТАЕТСЯ ЗАПИСЬЮ. Записи и их кратность берутся ТОЛЬКО из корпуса, через `karta_domov.py`
(`KONSTITUCIYA §10`: число считается командой). Файл дома на счёт не влияет вовсе — иначе дом,
переписавший у себя цифру, поднял бы себе покрытие правкой текста.

ЧТО СЧИТАЕТСЯ НАКРЫТИЕМ — контракт строки, одинаковый для всех домов:

    | <id записи корпуса> | … | <рычаг> |

строка markdown-таблицы, ПЕРВАЯ клетка которой — id корпуса (`КРВ-16a`, `КРТ-081`, `И-51`,
`Р5-3`, `ГИТ-*`), ПОСЛЕДНЯЯ — рычаг. Всё остальное в файле дома метрика не читает: заголовки,
прозу, таблицы ловушек без id. Если в строке есть клетка-число, она сверяется с кратностью
корпуса — расхождение печатается как ⚠, а не подгоняется.

Рычаг разбирается на ЧЕТЫРЕ ВИДА, и три из них — не проценты покрытия:

  МАШИННЫЙ      — назван носитель, который краснеет сам: путь к файлу движка/гейта, id ворот
                  (`G10`, `ворота 5`), команда (`check_*.py`, `--gates`).
  ПРОЦЕДУРНЫЙ   — правило названо, носителя нет («правило: взял примитив — проверь…»).
  НЕ НАКРЫВАЕТСЯ— сказано, что машинного рычага нет И БЫТЬ НЕ МОЖЕТ (КРВ-40: гейта на «читается
                  за три секунды» не существует). Законный вид, считается отдельно.
  НЕ НАКРЫТО    — «ничем», «нет», «—», заготовка не реализована.

🔴 Процентом печатается ТОЛЬКО машинное. `KONSTITUCIYA §11`: правило, которому нечему покраснеть,
— надежда, а не правило; сложить процедурное с машинным значит соврать в приятную сторону.

РАЗОБРАННОСТЬ — отдельная колонка и отдельный смысл: доля записей, у которых вердикт вообще есть,
включая честное «не накрывается». Именно она отличает разобранный дом от неразобранного, и
именно она высока у ИЛЛЮСТРАЦИЙ; машинное покрытие у них низкое ПО УСТРОЙСТВУ ПРЕДМЕТА
(`_illustracii/POKRYTIE.md §2`: три самых частых предмета недовольства машиной не ловятся).

Использование:
    python3 pokrytie_rychagami.py                 # таблица по домам
    python3 pokrytie_rychagami.py --dom ИЛЛЮСТРАЦИИ   # позаписно: id · кратность · вид · рычаг
    python3 pokrytie_rychagami.py --dyry          # только записи без вердикта, по домам
    python3 pokrytie_rychagami.py --doma <путь>   # другой корень `disciplina/doma`
"""
import collections
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MATERIALS = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DOMA_ROOT_DEFAULT = os.path.expanduser("~/Documents/GitHub/disciplina/doma")

# Пять домов карты → четыре дома плагина (решение 7, 2026-08-07: РЕСЁРЧ и ЛЕНТА слиты,
# два дома на один скилл не давали `check_uroki_doma.py` судить, в верный ли дом приехал урок).
KARTA_K_PLAGINU = {
    "РЕСЁРЧ": "reserch-cikl", "ЛЕНТА": "reserch-cikl",
    "СЛАЙДЫ": "slajdy", "ИЛЛЮСТРАЦИИ": "illustracii", "МЕТА": "meta",
}
PLAGIN_DOMA = ["illustracii", "slajdy", "reserch-cikl", "meta"]

# Разбор дома живёт там, где его написали. У ИЛЛЮСТРАЦИЙ он написан в фабрике иллюстраций и
# НЕ дублируется в плагине (`doma/illustracii/POKRYTIE.md §2` прямо отсылает туда) — поэтому
# у дома может быть больше одного файла-источника.
DOP_ISTOCHNIKI = {
    "illustracii": [os.path.join(MATERIALS, "_illustracii", "POKRYTIE.md")],
}

ID_RE = re.compile(r'^(КР[ВТ]-[\w\-]+|И-\d+|Р5-\d+|ГИТ-\w+)$')

# Носитель, который краснеет сам: файл движка/гейта, id ворот, команда-проверка.
MASHINNYJ_RE = re.compile(
    r'`[^`]*\.(?:py|sh|css|js)\b'          # `build_deck.py`, `check_view.py`, `base.css`
    r'|\bG\d+\b|\bГ\d+\b'                  # G10, Г7
    r'|ворот[аи]\s*\d+'                    # ворота 5
    r'|--gates\b'
)
# «Рычага нет и быть не может» — законный вид, а не дыра.
NEVOZMOZHNO_RE = re.compile(r'и\s+не\s+может|не\s+может\s+ловиться|по\s+построению|не\s+существует')
# Названное правило без носителя.
PROCEDURNYJ_RE = re.compile(r'\bправил|\bрецепт|механизм\s+назван|\bдоговорённост')
# Явное «пусто» + заготовки, которые не построены.
PUSTO_RE = re.compile(r'^\s*(—|-|нет|ничем|ничего|\?)\s*[.;]?\s*$', re.I)
NE_POSTROEN_RE = re.compile(r'не\s+реализован|не\s+построен|не\s+заведён|не\s+сделан')
# Машинный рычаг, который по собственному тексту дома НЕ валит сборку. Отрицание снимается ДО
# поиска: у КРВ-23a стоит «структурную ОШИБКУ сборки (не WARN)» — без снятия это давало бы
# ложную пометку «мягкий» ровно на самом жёстком рычаге дома.
OTRICANIE_RE = re.compile(r'\bне\s+(WARN|мягк\w*|предупрежден\w*)', re.I)
MYAGKIJ_RE = re.compile(r'мягк|предупрежден|\bWARN\b')
# Дом сам сказал, что рычаг закрывает не весь класс.
CHASTICHNYJ_RE = re.compile(r'частичн|частично')

VIDY = ["машинный", "процедурный", "не накрывается", "не накрыто"]


def _karta():
    spec = importlib.util.spec_from_file_location("karta", os.path.join(HERE, "karta_domov.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def zapisi_po_domam(k):
    """{дом плагина: (Counter id → Σ кратности, Σ дома по КАРТЕ)}.

    Два числа, а не одно, и это не дублирование. Итог дома берётся у карты (`srez` по фазе) —
    он и есть авторитет счёта. Поимённая раскладка нужна отдельно, чтобы цеплять к ней рычаги, и
    она может оказаться КОРОЧЕ итога: агрегат `КРТ-РАЗН-*` разворачивается в отдельные находки по
    адресам, и на двух фазах разворот не добирает по одной записи (`02-reserch` 311 из 312,
    `03-matbaza` 97 из 98 — дефект разворота, а не этого счётчика: он существует в
    `karta_domov.py` с 06.08 и здесь всплыл впервые, потому что раньше поимённая раскладка всех
    фаз никому не была нужна). Такая запись честно падает в «не разобрано» и объявляется ⚠;
    подгонять итог под раскладку значило бы потерять записи молча.
    """
    po_id = collections.defaultdict(collections.Counter)
    itogo = collections.Counter()
    counts, _ = k._srez().parse()
    for phase, dom in k.PHASE_TO_DOM.items():
        itogo[KARTA_K_PLAGINU[dom]] += counts.get(phase, 0)
        for r in k.extract_groups(phase):
            po_id[KARTA_K_PLAGINU[dom]][r["id"]] += r["kratnost"]
    for r in k.classify_vnefaz():
        cls = k.KLASS_VNEFAZ.get(r["id"])
        if cls is not None and cls != "СПОРНО":
            po_id["meta"][r["id"]] += r["kratnost"]
            itogo["meta"] += r["kratnost"]
    for r in k.classify_intervyu():
        cls = k.KLASS_INTERVYU.get(r["id"])
        if cls is not None and cls != "СПОРНО":
            po_id[KARTA_K_PLAGINU[cls]][r["id"]] += r["kratnost"]
            itogo[KARTA_K_PLAGINU[cls]] += r["kratnost"]
    for a in k.classify_06tekst():
        if a["dom"] != "СПОРНО":
            po_id[KARTA_K_PLAGINU[a["dom"]]][a["id"]] += a["kratnost"]
            itogo[KARTA_K_PLAGINU[a["dom"]]] += a["kratnost"]
    return {dom: (po_id[dom], itogo[dom]) for dom in PLAGIN_DOMA}


def vid_rychaga(cell):
    """Клетка «рычаг» → вид. Порядок проверок — не косметика: «ничем, и не может» это
    НЕ НАКРЫВАЕТСЯ, а «ничем, заготовка не реализована» — НЕ НАКРЫТО."""
    text = cell.strip()
    if NEVOZMOZHNO_RE.search(text):
        return "не накрывается"
    if PUSTO_RE.match(text) or not text:
        return "не накрыто"
    if NE_POSTROEN_RE.search(text):
        return "не накрыто"
    if MASHINNYJ_RE.search(text):
        return "машинный"
    if PROCEDURNYJ_RE.search(text):
        return "процедурный"
    return "не накрыто"


def chitat_dom(path):
    """Файл дома → [(id, кратность-из-файла|None, рычаг, вид)]. Читается только контракт строки."""
    rows = []
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        for ln in f:
            if not ln.lstrip().startswith("|"):
                continue
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) < 2:
                continue
            ident = cells[0].strip("`* ")
            if not ID_RE.match(ident):
                continue
            chisla = [int(c) for c in cells[1:-1] if re.fullmatch(r'\d+', c)]
            rows.append((ident, chisla[0] if chisla else None, cells[-1], vid_rychaga(cells[-1])))
    return rows


def sobrat(doma_root):
    k = _karta()
    zapisi = zapisi_po_domam(k)
    itog = {}
    for dom in PLAGIN_DOMA:
        puti = [os.path.join(doma_root, dom, "POKRYTIE.md")] + DOP_ISTOCHNIKI.get(dom, [])
        stroki, propali = [], []
        for p in puti:
            r = chitat_dom(p)
            if r is None:
                propali.append(p)
            else:
                stroki.extend(r)
        itog[dom] = {"zapisi": zapisi[dom][0], "itogo": zapisi[dom][1],
                     "stroki": stroki, "net_fajla": propali}
    return itog


def svesti(d):
    """Дом → числа. Запись без строки в доме — «не разобрана», это не то же, что «не накрыта»."""
    zapisi, po_vidam, sverka, chuzhie = d["zapisi"], collections.Counter(), [], []
    razobrano, myagkie, chastichnye = 0, [], []
    videno = set()
    for ident, n_fajla, rychag, vid in d["stroki"]:
        if ident not in zapisi:
            chuzhie.append(ident)
            continue
        if ident in videno:
            continue
        videno.add(ident)
        n = zapisi[ident]
        razobrano += n
        po_vidam[vid] += n
        if vid == "машинный" and MYAGKIJ_RE.search(OTRICANIE_RE.sub("", rychag)):
            myagkie.append((ident, n))
        if vid == "машинный" and CHASTICHNYJ_RE.search(rychag):
            chastichnye.append((ident, n))
        if n_fajla is not None and n_fajla != n:
            sverka.append((ident, n_fajla, n))
    vsego = d["itogo"]
    return {"vsego": vsego, "razobrano": razobrano, "ne_razobrano": vsego - razobrano,
            "po_vidam": po_vidam, "sverka": sverka, "chuzhie": chuzhie, "myagkie": myagkie,
            "chastichnye": chastichnye,
            "net_fajla": d["net_fajla"], "ne_razlozheno": vsego - sum(zapisi.values())}


def main():
    argv = sys.argv[1:]
    doma_root = DOMA_ROOT_DEFAULT
    if "--doma" in argv:
        doma_root = os.path.expanduser(argv[argv.index("--doma") + 1])
    itog = sobrat(doma_root)
    svod = {dom: svesti(d) for dom, d in itog.items()}

    if "--dom" in argv:
        want = argv[argv.index("--dom") + 1]
        dom = KARTA_K_PLAGINU.get(want, want)
        if dom not in itog:
            raise SystemExit(f"❌ нет такого дома: {want} (есть: {', '.join(PLAGIN_DOMA)})")
        d = itog[dom]
        print(f"ДОМ {dom} — позаписно ({len(d['zapisi'])} id, Σ кратности {sum(d['zapisi'].values())})")
        po_id = {ident: (rychag, vid) for ident, _n, rychag, vid in d["stroki"]}
        for ident, n in sorted(d["zapisi"].items(), key=lambda x: -x[1]):
            rychag, vid = po_id.get(ident, ("", "НЕ РАЗОБРАНО"))
            print(f"  {ident:12} {n:>4}  {vid:15} {rychag[:90]}")
        return

    if "--dyry" in argv:
        for dom in PLAGIN_DOMA:
            d, s = itog[dom], svod[dom]
            razobrannye = {i for i, _n, _r, _v in d["stroki"]}
            dyry = [(i, n) for i, n in d["zapisi"].items() if i not in razobrannye]
            print(f"\n{dom}: без вердикта {len(dyry)} id, Σ кратности {s['ne_razobrano']}")
            for ident, n in sorted(dyry, key=lambda x: -x[1])[:20]:
                print(f"   {ident:12} {n:>4}")
            if len(dyry) > 20:
                print(f"   … ещё {len(dyry) - 20} id")
        return

    print("ПОКРЫТИЕ РЫЧАГАМИ — Σ кратности, посчитано этим скриптом")
    print(f"{'дом':14} {'записей':>8} {'разобрано':>10} {'машинн.':>8} {'процед.':>8} "
          f"{'не накр-ся':>11} {'не накрыто':>11} {'не разобр.':>11} | {'машинное':>9} {'разобрано':>10}")
    for dom in PLAGIN_DOMA:
        s = svod[dom]
        v, r = s["vsego"], s["po_vidam"]
        m_pct = f"{100 * r['машинный'] / v:.0f}%" if v else "—"
        r_pct = f"{100 * s['razobrano'] / v:.0f}%" if v else "—"
        print(f"{dom:14} {v:>8} {s['razobrano']:>10} {r['машинный']:>8} {r['процедурный']:>8} "
              f"{r['не накрывается']:>11} {r['не накрыто']:>11} {s['ne_razobrano']:>11} | "
              f"{m_pct:>9} {r_pct:>10}")
    vsego = sum(s["vsego"] for s in svod.values())
    print(f"{'ИТОГО':14} {vsego:>8}   (спорные записи в дома не входят — `karta_domov.py --spornye`)")
    print("\n🔴 «машинное» и «разобрано» — РАЗНЫЕ числа и складывать их нельзя. Процедурное в "
          "процент машинного не входит (`KONSTITUCIYA §11`); «не накрывается» — законный вид.")

    for dom in PLAGIN_DOMA:
        s = svod[dom]
        for p in s["net_fajla"]:
            print(f"⚠ {dom}: файла дома нет по пути {p} — записи дома считаются неразобранными",
                  file=sys.stderr)
        for ident, n_f, n_k in s["sverka"]:
            print(f"⚠ {dom}: {ident} — в файле дома кратность {n_f}, в корпусе {n_k}", file=sys.stderr)
        if s["chuzhie"]:
            print(f"⚠ {dom}: рычаг привязан к id, которых в этом доме нет: "
                  f"{', '.join(sorted(set(s['chuzhie'])))}", file=sys.stderr)
        if s["ne_razlozheno"]:
            print(f"⚠ {dom}: {s['ne_razlozheno']} записей итога не разложены поимённо "
                  f"(разворот агрегата `КРТ-РАЗН-*` в `karta_domov.py` не добирает их по адресам) "
                  f"— рычаг к ним прицепить не за что, считаются неразобранными", file=sys.stderr)
        for ident, n in s["myagkie"]:
            print(f"⚠ {dom}: {ident} ({n}) — рычаг машинный, но сам дом называет его мягким "
                  f"(WARN); краснеет ли он на сборке — не проверено", file=sys.stderr)
        for ident, n in s["chastichnye"]:
            print(f"⚠ {dom}: {ident} ({n}) — дом сам называет рычаг ЧАСТИЧНЫМ; в машинное "
                  f"покрытие запись зачтена целиком, доля не замерена", file=sys.stderr)


if __name__ == "__main__":
    main()
