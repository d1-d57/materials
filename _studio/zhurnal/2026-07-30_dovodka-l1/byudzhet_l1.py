#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Пересчёт всей таблицы GEOMETRIYA-I-BYUDZHET.md из живой ленты.

    python3 _studio/zhurnal/2026-07-30_dovodka-l1/byudzhet_l1.py

Печатает: гейт 1 (намерение ↔ archetype_lenty) · гейт 2 (распределение архетипов)
· гейт 3 (полнота ТЗ) · гейт 4 (бюджет, строка на раздел) · гейт 5 (сохранность
блоков относительно HEAD). Ничего не пишет на диск. Код возврата: 0 — все зелёные.

⚠ ГЕЙТ 5 КРАСНЕЕТ У ЗАХОДА, КОТОРОМУ ТЕКСТ ПИСАТЬ ЗАКАЗАНО, и это не брак.
Он написан для захода геометрии, которому текст слайда трогать запрещали, и
проверяет ровно это. Заходу текста он служит ДИФФОМ: печатает построчно, какие
блоки ушли и какие пришли. Судить такой заход надо по гейту 4, а список гейта 5
читать как список своих же правок.

🔴 Зачем скрипт существует, а не таблица руками (KONSTITUCIYA §10): числа бюджета
пересчитываются при каждой правке ленты, и вписанное руками верное сегодня число
завтра врёт молча. Таблица в GEOMETRIYA-I-BYUDZHET.md — снимок вывода этой команды.
"""
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "teorkat-vvedenie" / "src" / "tools"))
import porodit as P                                              # noqa: E402

BLOCKS = ["A-krasivaya.md", "B-yazyk.md"]
LENTA_REL = "teorkat-vvedenie/raskadrovka/teksty/"

# ── модель вместимости ────────────────────────────────────────────────────────
# Потолок КАДРА — 650 знаков (_studio/konvejer/06-tekst/DOK.md). Доля площади под
# текст: рейка 344px из 1440 (07-verstka/DOK.md) ⇒ 1096/1440 = 0,761; нижняя
# полоса — прямое слово владельца «на текст меньше половины».
POTOLOK = 650
DOLYA = {"лестница-во-всю-ширину": 1.00, "доска-пустая": 0.92,
         "рейка-справа": 0.76, "илл-полосой-снизу": 0.45}
# Цель = норма минус запас. 0,82 — не вкус: медиана корпуса 45 слов при потолке
# 55 слов на кадр (06-tekst/DOK.md) и есть 0,82 потолка.
ZAPAS = 0.82

# Намерение исполнителя (заход kod_geometria.md). Обложка в привязке НЕ стоит:
# служебный слой, геометрии не имеет (07-verstka/DOK.md §13; porodit.py:481 «в
# slide_order не входит»; gejt_lenty.py:123 требует пометку «кроме обложки»).
#
# 🔴 ПРИВЯЗКА ИДЁТ ПО ЗАГОЛОВКУ РАЗДЕЛА, А НЕ ПО НОМЕРУ, и это не вкусовщина.
# Пока ключом был номер, снятие одного раздела сдвинуло все следующие: аналитик
# убрал «Что теперь стало видно» (14-й) решением владельца — и «Примеры категорий
# и функторов» унаследовали чужое ожидание архетипа (гейт 1 печатал «расхождений
# 1») ВМЕСТЕ с чужой пометкой «содержание не названо». Ни то, ни другое не было
# дефектом ленты. Заголовок при вставке и снятии разделов не сдвигается, поэтому
# ключ — он; а если заголовок ПЕРЕИМЕНУЮТ, скрипт теперь падает вслух (см. main),
# вместо того чтобы молча потерять слайд из проверки.
HOTEL = {
    "Соответствие задач": "илл-полосой-снизу",
    "Комбинаторные тождества": "лестница-во-всю-ширину",
    "Три биекции": "илл-полосой-снизу",
    "Почему это красиво": "илл-полосой-снизу",
    "Комбинаторные виды": "рейка-справа",
    "Примеры": "рейка-справа",
    "Естественное преобразование": "рейка-справа",
    "Чётные и нечётные подмножества": "илл-полосой-снизу",
    "Отмеченные виды": "рейка-справа",
    "Покрашенные виды": "рейка-справа",
    "Итог": "доска-пустая",
    "Категории": "рейка-справа",
    "Примеры категорий и функторов": "рейка-справа",
}
# Разделы, где число бюджета НЕ действующее: решение владельца не принято.
# Пометка «задача не придумана» снята 31.07 — задачи владелец назвал, и текст
# раздела написан по ним. Пометка «содержание не названо» принадлежала снятому
# разделу «Что теперь стало видно», а не справочнику.
NEDEJSTVUYUSHCHIE = {
    "Примеры категорий и функторов":
        "справочник: исключение из потолка кадра владельцем не оформлено "
        "(GEOMETRIYA-I-BYUDZHET.md §4.1)",
}

# ── измеритель: глифы, а не знаки TeX ────────────────────────────────────────
# porodit.visible_chars предупреждает сам: «формула считается своей длиной в TeX».
# `$\mathbf{Set}$` — 13 знаков разметки и 3 знака на экране; на слайде 13 разница
# двукратная, и бюджет по знакам TeX завернул бы слайд с полупустым экраном.
_VYBROS = re.compile(r"\\(displaystyle|left|right|quad|qquad|[,;!: ])")
_SHRIFT = re.compile(r"\\(mathbf|mathrm|mathcal|mathbb|text|operatorname)\s*\{([^{}]*)\}")
_DVUH = re.compile(r"\\(binom|frac|tfrac|dfrac)\s*(\{[^{}]*\}|\S)\s*(\{[^{}]*\}|\S)")
_CMD = re.compile(r"\\[A-Za-z]+")
_MATH = re.compile(r"\$([^$]+)\$")


def _svernut(m):
    t = _VYBROS.sub("", m.group(1))
    for _ in range(4):
        t2 = _SHRIFT.sub(lambda x: x.group(2), t)
        if t2 == t:
            break
        t = t2
    t = _DVUH.sub(lambda x: x.group(2).strip("{}") + x.group(3).strip("{}"), t)
    t = _CMD.sub("\u2022", t)
    return re.sub(r"[{}^_\s]", "", t)


def glif_chars(text):
    t = re.sub(r"^\{\.[\w-]+\}\s*", "", text, flags=re.M)
    t = re.sub(r"^- ", "", t, flags=re.M)
    t = t.replace("**", "").replace("\u2060", "")
    return len(re.sub(r"\s+", " ", _MATH.sub(_svernut, t)).strip())


def kadry_glif(text):
    n = P.scen_count(text)
    bl = []
    for block in re.split(r"\n\s*\n", text.strip("\n")):
        lines = [l for l in block.split("\n") if l.strip()]
        if not lines:
            continue
        m = P.TAG_RE.match(lines[0])
        f, u = P._interval(m.group(1)) if m else (1, P.INF)
        body = "\n".join(lines)
        if m:
            body = body[m.end():] if len(lines) == 1 else body.replace(m.group(0), "", 1)
        bl.append((f, u, glif_chars(body)))
    return [sum(c for f, u, c in bl if f <= k <= u) for k in range(1, n + 1)]


# ── гейт 5: сохранность текстовых блоков ─────────────────────────────────────
# Блок = непустая строка, НЕ заголовок, НЕ фронтматтер, НЕ `> поле:`, НЕ внутри
# фигуры, не `---`. Именно это множество заходу запрещено менять.
_FIG = re.compile(r"<figure\b.*?</figure>", re.S)
_FM = re.compile(r"\A---\n.*?\n---\n", re.S)


def bloki(text):
    t = _FIG.sub("", _FM.sub("", text))
    return [s for s in (l.strip() for l in t.split("\n"))
            if s and s != "---" and not s.startswith("#") and not s.startswith("> поле:")]


def iz_head(rel):
    r = subprocess.run(["git", "--no-optional-locks", "show", "HEAD:" + rel],
                       cwd=ROOT, capture_output=True)
    return r.returncode, (r.stdout.decode("utf-8") if r.returncode == 0 else "")


# ── ТЗ иллюстраций ───────────────────────────────────────────────────────────
PODPOLYA = ["ИЗОБРАЖЕНО:", "ПОДПИСИ:", "ДЕЙСТВИЕ:", "НЕ РИСОВАТЬ:", "РАЗМЕР:"]
TZ_RE = re.compile(r"^> поле:mn 🎨 (.*)$", re.M)


def sobrat():
    out, i = [], 0
    for fname in BLOCKS:
        for title, body in P.split_sections((P.LENTA / fname).read_text(encoding="utf-8")):
            i += 1
            s = P.parse_section(title, body)
            s["n"], s["raw"] = i, body
            out.append(s)
    return out


def main():
    ss = sobrat()
    krasno = []

    # ── ГЕЙТ 0: привязка по заголовку не должна ссылаться в пустоту ──
    # Ключ по заголовку спасает от СДВИГА номеров, но не от ПЕРЕИМЕНОВАНИЯ. Без
    # этой проверки переименованный раздел просто выпал бы из гейтов 1 и 4 молча —
    # то есть та же тихая потеря, от которой уходили, только с другой причиной.
    est = {s["title"] for s in ss}
    poteryany = [t for t in HOTEL if t not in est] + \
                [t for t in NEDEJSTVUYUSHCHIE if t not in est]
    if poteryany:
        print("🔴 ПРИВЯЗКА ССЫЛАЕТСЯ НА ЗАГОЛОВКИ, КОТОРЫХ В ЛЕНТЕ НЕТ:")
        for t in poteryany:
            print("     «%s»" % t)
        print("   Раздел переименован или снят. Поправь HOTEL/NEDEJSTVUYUSHCHIE, "
              "не гейты.")
        return 1

    # ── ГЕЙТ 1 ──
    print("═══ ГЕЙТ 1 — АРХЕТИП ФАКТИЧЕСКИЙ (намерение ↔ archetype_lenty) ═══")
    print("%-3s %-40s %-23s %-23s %s" % ("№", "слайд", "хотел", "вернула функция", ""))
    rash = 0
    for s in ss:
        got = P.archetype_lenty(s)
        if s["title"] not in HOTEL:
            print("%-3d %-40s %-23s %-23s %s"
                  % (s["n"], s["title"][:40], "— служебный", got, "исключён по канону"))
            continue
        ok = HOTEL[s["title"]] == got
        rash += 0 if ok else 1
        print("%-3d %-40s %-23s %-23s %s"
              % (s["n"], s["title"][:40], HOTEL[s["title"]], got,
                 "✅" if ok else "❌ РАСХОЖДЕНИЕ"))
    print("→ расхождений %d, проверено %d из %d (служебных исключено %d)"
          % (rash, len(HOTEL), len(ss), len(ss) - len(HOTEL)))
    if rash:
        krasno.append("гейт 1: расхождений %d" % rash)

    # ── ГЕЙТ 2 ──
    print("\n═══ ГЕЙТ 2 — РАСПРЕДЕЛЕНИЕ (доля выше 2/3 = красный) ═══")
    c = Counter(HOTEL.values())
    for k, v in c.most_common():
        d = v / len(HOTEL)
        print("   %-24s %2d  %3.0f%%%s" % (k, v, 100 * d, "  🔴 КРАСНЫЙ" if d > 2 / 3 else ""))
    mx = max(c.values()) / len(HOTEL)
    print("→ %s: максимум %.0f%% при пороге 67%%"
          % ("🔴 КРАСНЫЙ" if mx > 2 / 3 else "✅ ЗЕЛЁНЫЙ", 100 * mx))
    if mx > 2 / 3:
        krasno.append("гейт 2: доля %.0f%%" % (100 * mx))
    print("   ФАКТИЧЕСКИ, пока картинок в ленте нет (поправка archetype(), строка 460):")
    for s in ss:
        if s["title"] in HOTEL and P.archetype_lenty(s) != P.archetype(s):
            print("     слайд %2d: лента «%s» → факт «%s» (у раздела нет фигуры)"
                  % (s["n"], P.archetype_lenty(s), P.archetype(s)))

    # ── ГЕЙТ 3 ──
    print("\n═══ ГЕЙТ 3 — ПОЛНОТА ТЗ ИЛЛЮСТРАЦИЙ ═══")
    polnyh = zakaz = nepoln = 0
    s_kartinkoj = []
    for s in ss:
        for m in TZ_RE.finditer(s["raw"]):
            t = m.group(1)
            net = [p for p in PODPOLYA if p not in t]
            s_kartinkoj.append(s["n"])
            if "🕳" in t:
                zakaz += 1
                print("   слайд %2d  подполей %d/5  🕳 ЗАКАЗ (дыра названа владельцем)"
                      % (s["n"], 5 - len(net)))
            elif net:
                nepoln += 1
                print("   слайд %2d  подполей %d/5  ❌ НЕПОЛНО, нет: %s"
                      % (s["n"], 5 - len(net), ", ".join(net)))
            else:
                polnyh += 1
                print("   слайд %2d  подполей 5/5  ✅ полно" % s["n"])
    print("→ слайдов с картинкой %d · полных ТЗ %d · ЗАКАЗ %d · неполных %d"
          % (len(s_kartinkoj), polnyh, zakaz, nepoln))
    if nepoln:
        krasno.append("гейт 3: неполных ТЗ %d" % nepoln)

    # ── ГЕЙТ 4 ──
    print("\n═══ ГЕЙТ 4 — БЮДЖЕТ (дефицит по ГЛИФАМ, не по знакам TeX) ═══")
    print("%-3s %-34s %-21s %6s %6s %5s %5s %7s"
          % ("№", "слайд", "архетип", "TeXкдр", "глфкдр", "вмещ", "цель", "дефицит"))
    sum_def = sum_prof = sum_dejstv = 0
    for s in ss:
        gl = max(kadry_glif(s["text"])) if s["text"].strip() else 0
        if s["title"] not in HOTEL:
            print("%-3d %-34s %-21s %6d %6d %5s %5s %7s"
                  % (s["n"], s["title"][:34], "служебный", s["tyazh"], gl, "—", "—", "—"))
            continue
        a = HOTEL[s["title"]]
        vm = round(POTOLOK * DOLYA[a])
        cel = round(vm * ZAPAS)
        d = cel - gl
        met = ("  🕳 %s" % NEDEJSTVUYUSHCHIE[s["title"]]
               if s["title"] in NEDEJSTVUYUSHCHIE else "")
        if gl > vm:
            met += "  🔴 ВЫШЕ «вмещает»"
        if d > 0:
            sum_def += d
            if s["title"] not in NEDEJSTVUYUSHCHIE:
                sum_dejstv += d
        else:
            sum_prof += -d
        print("%-3d %-34s %-21s %6d %6d %5d %5d %+7d%s"
              % (s["n"], s["title"][:34], a, s["tyazh"], gl, vm, cel, d, met))
    print("→ ДОПИСАТЬ всего: %+d глифов · из них ДЕЙСТВУЮЩИХ: %+d "
          "(без слайдов, где решение владельца не принято)" % (sum_def, sum_dejstv))
    print("→ СРЕЗАТЬ всего: -%d глифов" % sum_prof)

    # ── ГЕЙТ 5 ──
    print("\n═══ ГЕЙТ 5 — НИ ОДНОГО ЗНАКА ТЕКСТА СЛАЙДА НЕ ТРОНУТО ═══")
    do, posle = [], []
    for f in BLOCKS:
        rc, h = iz_head(LENTA_REL + f)
        print("   git show HEAD:%s%s → rc=%d" % (LENTA_REL, f, rc))
        if rc:
            krasno.append("гейт 5: HEAD не читается")
            return 1
        do += bloki(h)
        posle += bloki((P.LENTA / f).read_text(encoding="utf-8"))
    sd, sp = set(do), set(posle)
    ushli = [b for b in do if b not in sp]
    prishli = [b for b in posle if b not in sd]
    print("→ блоков %d · изменённых %d (ушло %d · пришло %d)"
          % (len(do), len(ushli) + len(prishli), len(ushli), len(prishli)))
    for b in ushli:
        print("     − %s" % b[:120])
    for b in prishli:
        print("     + %s" % b[:120])
    if ushli or prishli:
        krasno.append("гейт 5: изменённых блоков %d" % (len(ushli) + len(prishli)))

    # ── одно поле «Раскладка.» на раздел ──
    mnogo = [(s["n"], n) for s in ss
             for n in [len(re.findall(r"^> поле:mn \*\*Раскладка\.\*\* ", s["raw"], re.M))]
             if n > 1]
    print("\n   разделов с БОЛЕЕ ЧЕМ одним полем «**Раскладка.**»: %d %s"
          % (len(mnogo), mnogo if mnogo else "✅"))
    if mnogo:
        krasno.append("несколько полей «Раскладка.» в разделе: %s" % mnogo)

    print("\n" + ("🔴 КРАСНОЕ: " + " · ".join(krasno) if krasno else "✅ ВСЕ ГЕЙТЫ ЗЕЛЁНЫЕ"))
    return 1 if krasno else 0


if __name__ == "__main__":
    sys.exit(main())
