#!/usr/bin/env python3
"""Сырая расшифровка → два потока (рассказ / комментарий) + ТАЙМИНГ.

Владелец рассказывает лекцию как залу; увидев на слайде дефект, говорит «стоп»
и переходит к комментарию, потом возвращается к рассказу. Скрипт делит поток по
этому маркеру, привязывает реплики к слайдам ленты и считает время — тайминг и
есть то, ради чего всё: сколько минут занял рассказ ОТДЕЛЬНО от комментариев.

Вход:  akt-N-syroj.md
Выход: akt-N-razbor.md + tajming-akt-N.json (для накопительного итога)

Запуск: python3 tools/razobrat.py akt-1-syroj.md
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPETICIA = os.path.dirname(HERE)
LENTA = os.path.join(os.path.dirname(REPETICIA), "raskadrovka", "teksty")

BLOKI = [
    ("A", "A-krasivaya.md"),
    ("B", "B-yazyk.md"),
    ("C", "C-zapret-retrakt.md"),
    ("D", "D-zapret-estestvennost.md"),
    ("E", "E-dva-mira.md"),
]

# ─────────────────────────────────────────────────────────────────────────────
# ПРАВИЛО РАСПОЗНАВАНИЯ МАРКЕРА — печатается в разбор, чтобы владелец подстроил
# речь под него, если надо.
#
# СТОП (рассказ → комментарий). Ловим терпимо, потому что whisper напишет
# «стоп», «Стоп.», «стоп,», «Стоп!»:
#   1. отдельное слово «стоп» в любом регистре, знаки препинания вокруг любые;
#   2. «стоп», слипшееся со следующим словом В НАЧАЛЕ сегмента («Стопэто»);
#   НЕ ловим «стоп-кадр», «стопор» — дефис и продолжение слова гасят маркер
#   (кроме случая 2, где слипание именно в начале реплики).
#
# ВОЗВРАТ (комментарий → рассказ) — только явным словом. Молчаливый возврат
# распознать нечем: продолжение рассказа и продолжение комментария в тексте
# выглядят одинаково. Поэтому если возврат не назван, всё до следующего
# маркера считается комментарием — и такие места печатаются отдельным списком.
# ─────────────────────────────────────────────────────────────────────────────

RX_STOP = re.compile(r"(?<![\w-])стоп(?![\w-])", re.I)
RX_STOP_SLIPSHIJSYA = re.compile(r"^\W*стоп(?=[а-яё])", re.I)
RX_VOZVRAT = re.compile(
    r"(?<![\w-])(старт|продолжаем|продолжим|продолжаю|поехали|возвращаюсь|возвращаемся"
    r"|дальше по тексту|дальше по плану|обратно к рассказу|конец комментария)(?![\w-])",
    re.I,
)
# «старт» стоит первым не по алфавиту: в акте 1 владелец сам его завёл на ходу
# («сначала, наверное, старт слайда, а потом комментарий») и сказал трижды, тогда
# как ни одного «продолжаем» в записи нет. Маркер возврата задаёт говорящий, а не
# автор скрипта, — правило догоняет речь, а не наоборот.

RX_SEGMENT = re.compile(r"^\*\*\[(\d+):(\d\d)\]\*\*\s*(.+)$")

STOP_SLOVA = set(
    """и в во не что он на я с со как а то все она так его но да ты к у же вы за бы
по только ее мне было вот от меня еще нет о из ему теперь когда даже ну вдруг ли
если уже или ни быть был него до вас нибудь опять уж вам ведь там потом себя
ничего ей может они тут где есть надо ней для мы тебя их чем была сам чтоб без
будто чего раз тоже себе под будет ж тогда кто этот того потому этого какой
совсем ним здесь этом один почти мой тем чтобы нее сейчас были куда зачем всех
никогда можно при наконец два об другой хоть после над больше тот через эти нас
про всего них какая много разве три эту моя впрочем хорошо свою этой перед
иногда лучше чуть том нельзя такой им более всегда конечно всю между это""".split()
)


def slova(s):
    return [w for w in re.findall(r"[а-яёa-z0-9]+", s.lower()) if w not in STOP_SLOVA and len(w) > 2]


def osnova(w):
    """Грубый стем: русские окончания сбивают совпадение «функтора» и «функтор»."""
    return w[:6] if len(w) > 7 else w[: max(4, len(w) - 2)] if len(w) > 5 else w


def slajdy():
    """33 раздела ленты = 33 слайда. Нумерация — блок+номер («A3»), не номер в деке.

    Почему так: лента даёт 33 раздела, а дек по заходу — 32 содержательных
    слайда; чей счёт верен, отсюда не видно, а угадывать номер нельзя.
    Метка «A3 «Три состояния элемента»» однозначна при любом счёте.
    """
    spisok = []
    for kod, imya in BLOKI:
        put = os.path.join(LENTA, imya)
        if not os.path.exists(put):
            sys.exit("НЕТ файла ленты: %s" % put)
        tekst = open(put, encoding="utf-8").read()
        chasti = re.split(r"^## ", tekst, flags=re.M)[1:]
        for i, ch in enumerate(chasti, 1):
            zagolovok = ch.splitlines()[0].strip()
            telo = ch[:4000]
            spisok.append(
                {
                    "metka": "%s%d" % (kod, i),
                    "zagolovok": zagolovok,
                    "klyuchi_zagolovka": set(osnova(w) for w in slova(zagolovok)),
                    "klyuchi_tela": set(osnova(w) for w in slova(telo)),
                }
            )
    return spisok


def privyazka(tekst, spisok):
    """Кандидаты-слайды по совпадению лексики. Заголовок весит вчетверо: владелец
    обещал называть слайд, а не пересказывать его. Возвращает top-3 с очками."""
    k = set(osnova(w) for w in slova(tekst))
    if not k:
        return []
    ochki = []
    for s in spisok:
        z = len(k & s["klyuchi_zagolovka"])
        t = len(k & s["klyuchi_tela"])
        ochki.append((z * 4 + t * 1.0 / max(1, len(s["klyuchi_tela"]) / 12.0), z, s))
    ochki.sort(key=lambda x: -x[0])
    return [(round(o, 1), z, s) for o, z, s in ochki[:3] if o > 0]


def raskroit(segmenty):
    """Разрезает сегмент ПО МАРКЕРУ, если маркер сидит внутри него.

    Зачем: whisper выдаёт сегмент на 5–15 с, и «стоп» запросто окажется в
    середине — вместе с рассказом до него и, бывает, со словом возврата после.
    Без раскроя весь сегмент уходит в один поток, и тайминг врёт на десяток
    секунд в каждую сторону (проверено на тестовом прогоне: рассказ 12 с /
    комментарии 12 с вместо 17 / 7).

    Граница внутри сегмента интерполируется ПО ДОЛЕ СИМВОЛОВ — точных
    таймкодов слов в сыром .md нет, и это честная оценка, а не измерение;
    такие границы помечаются, чтобы их было видно в разборе.
    """
    gotovo = []
    for ot, do, t in segmenty:
        rezy = sorted(
            set(
                [m.start() for m in RX_STOP.finditer(t)]
                + [m.start() for m in RX_VOZVRAT.finditer(t)]
            )
        )
        rezy = [r for r in rezy if r > 0]
        if not rezy:
            gotovo.append((ot, do, t, False))
            continue
        kraya = [0] + rezy + [len(t)]
        for i in range(len(kraya) - 1):
            a, b = kraya[i], kraya[i + 1]
            kusok = t[a:b].strip()
            if not kusok:
                continue
            gotovo.append(
                (
                    ot + (do - ot) * a / len(t),
                    ot + (do - ot) * b / len(t),
                    kusok,
                    i > 0,  # граница получена интерполяцией, а не от движка
                )
            )
    return gotovo


def chitat_granicy(put):
    """Границы потоков, поставленные СУЖДЕНИЕМ, — как данные для скрипта.

    Зачем это есть. Маркеры ловят не всё: в акте 1 владелец сказал «стоп» трижды,
    возврат обозначил словом «старт» (которого правило не знало), а на слайде 4
    начал рассказ вообще без маркера. Механическая разметка дала бы «комментарий
    с 18:00 до конца» — то есть соврала бы вдвое там, где тайминг и есть цель.

    Но из того, что границу ставит человек, НЕ следует, что человек вписывает
    минуты. Числа считает скрипт из этих границ — иначе в отчёт попадает не
    измерение, а впечатление.

    Формат строки:  MM:SS <поток> [метка слайда]
    Поток: рассказ | комментарий | служебное. Пустые строки и # — комментарии.
    """
    granicy = []
    for nomer, stroka in enumerate(open(put, encoding="utf-8"), 1):
        s = stroka.strip()
        if not s or s.startswith("#"):
            continue
        m = re.match(r"^(\d+):(\d\d)\s+(рассказ|комментарий|служебное)\s*(.*)$", s)
        if not m:
            sys.exit("границы, строка %d: не разобрана — «%s»" % (nomer, s))
        granicy.append(
            (int(m.group(1)) * 60 + int(m.group(2)), m.group(3), m.group(4).strip())
        )
    if not granicy:
        sys.exit("в %s нет ни одной границы" % put)
    granicy.sort(key=lambda g: g[0])
    return granicy


def razmetit_po_granicam(segmenty, granicy):
    """Раскладывает сегменты по потокам из файла границ. Ни один не теряется."""
    kuski = []
    for ot, potok, metka in granicy:
        kuski.append({"ot": ot, "potok": potok, "metka": metka, "seg": []})
    for ot, do, t, _ in segmenty:
        podhodit = [k for k in kuski if k["ot"] <= ot + 0.5]
        (podhodit[-1] if podhodit else kuski[0])["seg"].append((ot, do, t))
    return [k for k in kuski if k["seg"]]


def razmetit(segmenty):
    """Поток → куски (потok, сегменты). Возвращает также журнал сработавших маркеров."""
    potok = "рассказ"
    kuski, tekushchij, markery, nezakrytye = [], [], [], []
    for nomer, (ot, do, t, interp) in enumerate(segmenty):
        novyj, pravilo = potok, None
        if RX_STOP.search(t) or RX_STOP_SLIPSHIJSYA.search(t):
            novyj, pravilo = "комментарий", ("слипшийся «стоп»" if RX_STOP_SLIPSHIJSYA.search(t) and not RX_STOP.search(t) else "отдельное слово «стоп»")
        elif potok == "комментарий" and RX_VOZVRAT.search(t):
            novyj, pravilo = "рассказ", "слово возврата"
        if pravilo:
            markery.append((ot, novyj, pravilo + (", граница внутри сегмента — интерполирована" if interp else ""), t[:70]))
        if novyj != potok:
            if tekushchij:
                kuski.append((potok, tekushchij, ""))
            tekushchij, potok = [], novyj
        tekushchij.append((ot, do, t))
    if tekushchij:
        kuski.append((potok, tekushchij, ""))
    for i, (p, seg, _) in enumerate(kuski):
        # комментарий, за которым нет возврата и который не последний — возврат
        # был молчаливым, и граница у него угадана, а не распознана
        if p == "комментарий" and i + 1 < len(kuski) and len(seg) > 12:
            nezakrytye.append((seg[0][0], seg[-1][1], len(seg)))
    return kuski, markery, nezakrytye


def mmss(sec):
    return "%02d:%02d" % (int(sec) // 60, int(sec) % 60)


def minuty(sec):
    return "%d мин %02d с" % (int(sec) // 60, int(sec) % 60)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("syroj")
    ap.add_argument("--granicy", default="", help="файл границ потоков, поставленных суждением (см. chitat_granicy)")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    if not os.path.exists(args.syroj):
        sys.exit("нет файла: %s" % args.syroj)
    imya = os.path.basename(args.syroj).replace("-syroj.md", "")

    segmenty = []
    for stroka in open(args.syroj, encoding="utf-8"):
        m = RX_SEGMENT.match(stroka.strip())
        if m:
            ot = int(m.group(1)) * 60 + int(m.group(2))
            segmenty.append([float(ot), None, m.group(3).strip()])
    if not segmenty:
        sys.exit("в %s не нашлось сегментов вида **[MM:SS]** текст" % args.syroj)
    # конец сегмента = начало следующего: в сыром .md хранится только начало,
    # и это единственная согласованная оценка длительности
    for i in range(len(segmenty) - 1):
        segmenty[i][1] = segmenty[i + 1][0]
    segmenty[-1][1] = segmenty[-1][0] + max(
        2.0, (segmenty[-1][0] - segmenty[0][0]) / max(1, len(segmenty) - 1)
    )
    segmenty_syrye = [(a, b, c) for a, b, c in segmenty]
    segmenty = raskroit(segmenty_syrye)
    raskroeno = len(segmenty) - len(segmenty_syrye)

    spisok = slajdy()
    # маркеры считаем ВСЕГДА — даже когда границы заданы суждением: их журнал
    # показывает, что правило поймало, а что пропустило, и как править правило
    kuski_avto, markery, nezakrytye = razmetit(segmenty)
    if args.granicy:
        granicy = chitat_granicy(args.granicy)
        kuski = [(k["potok"], k["seg"], k["metka"]) for k in razmetit_po_granicam(segmenty, granicy)]
        chej_razbor = "границы поставлены СУЖДЕНИЕМ (`%s`), числа посчитаны из них скриптом" % os.path.basename(args.granicy)
    else:
        kuski = kuski_avto
        chej_razbor = "границы распознаны автоматически по маркерам «стоп»/«старт»"

    rasskaz = sum(do - ot for p, seg, _ in kuski if p == "рассказ" for ot, do, _ in seg)
    komm = sum(do - ot for p, seg, _ in kuski if p == "комментарий" for ot, do, _ in seg)
    sluzh = sum(do - ot for p, seg, _ in kuski if p == "служебное" for ot, do, _ in seg)
    vsego = segmenty[-1][1] - segmenty[0][0]

    # ── разбор ───────────────────────────────────────────────────────────────
    L = [
        "# %s — разбор: рассказ / комментарии / тайминг" % imya,
        "",
        "> Собран `tools/razobrat.py` из `%s`. Правки — в `PRAVKI.md`, не здесь."
        % os.path.basename(args.syroj),
        "",
        "**Как размечено:** %s." % chej_razbor,
        "",
        "**Правило маркера** (подстрой речь под него, если неудобно):",
        "- **«стоп»** отдельным словом — рассказ → комментарий. «стоп-кадр» и «стопор» маркером НЕ считаются;",
        "- **«старт»** — обратно к рассказу (годятся также «продолжаем», «продолжим», «поехали», «возвращаюсь», «дальше по тексту», «конец комментария»);",
        "- **молчаливый возврат распознать нечем** — не назвали, и комментарием считается всё до следующего маркера. Именно поэтому существуют границы суждением.",
        "",
        "## 🔴 ТАЙМИНГ — этого акта",
        "",
        "| | время | доля |",
        "|---|---|---|",
        "| **рассказ (чистый)** | **%s** | %d%% |" % (minuty(rasskaz), round(100 * rasskaz / max(1e-9, vsego))),
        "| комментарии | %s | %d%% |" % (minuty(komm), round(100 * komm / max(1e-9, vsego))),
        "| служебное (разговор о процессе, не лекция) | %s | %d%% |" % (minuty(sluzh), round(100 * sluzh / max(1e-9, vsego))),
        "| всего на записи | %s | 100%% |" % minuty(vsego),
        "",
    ]

    # накопительно по всей лекции
    json.dump(
        {"akt": imya, "rasskaz": rasskaz, "komm": komm, "sluzh": sluzh, "vsego": vsego},
        open(os.path.join(REPETICIA, "tajming-%s.json" % imya), "w", encoding="utf-8"),
        ensure_ascii=False,
    )
    vse = []
    for f in sorted(os.listdir(REPETICIA)):
        if f.startswith("tajming-") and f.endswith(".json"):
            vse.append(json.load(open(os.path.join(REPETICIA, f), encoding="utf-8")))
    if len(vse) > 1:
        L += ["### накопительно по лекции (актов сведено: %d)" % len(vse), "", "| акт | рассказ | комментарии | всего |", "|---|---|---|---|"]
        for v in vse:
            L.append("| %s | %s | %s | %s |" % (v["akt"], minuty(v["rasskaz"]), minuty(v["komm"]), minuty(v["vsego"])))
        L.append(
            "| **ИТОГО** | **%s** | **%s** | **%s** |"
            % (minuty(sum(v["rasskaz"] for v in vse)), minuty(sum(v["komm"] for v in vse)), minuty(sum(v["vsego"] for v in vse)))
        )
        L.append("")
    else:
        L += ["*Накопительный итог появится со второго акта.*", ""]

    def metka_kuska(seg, gotovaya):
        """Метка слайда: поставленная суждением — как есть; иначе догадка с `?`."""
        if gotovaya:
            return gotovaya
        kand = privyazka(" ".join(t for _, _, t in seg), spisok)
        if kand and kand[0][1] > 0 and (len(kand) < 2 or kand[0][0] >= kand[1][0] * 1.5):
            return "%s «%s»" % (kand[0][2]["metka"], kand[0][2]["zagolovok"])
        if kand:
            return "? " + " / ".join("%s «%s»" % (k[2]["metka"], k[2]["zagolovok"]) for k in kand[:2])
        return "?"

    # ── ход записи целиком: видно чередование потоков ────────────────────────
    L += ["## Ход записи — чем сменялось что", "", "| # | таймкод | длит. | поток | слайд | начало реплики |", "|---|---|---|---|---|---|"]
    for n, (p, seg, gotovaya) in enumerate(kuski, 1):
        znak = {"рассказ": "🎙 рассказ", "комментарий": "💬 комментарий", "служебное": "⚙️ служебное"}[p]
        tekst = " ".join(t for _, _, t in seg)
        L.append(
            "| %d | **[%s]** | %s | %s | %s | %s… |"
            % (n, mmss(seg[0][0]), minuty(seg[-1][1] - seg[0][0]), znak,
               metka_kuska(seg, gotovaya) if p != "служебное" else "—",
               tekst[:80].replace("|", "/"))
        )
    L.append("")

    # ── комментарии ──────────────────────────────────────────────────────────
    komm_kuski = [(i, seg, g) for i, (p, seg, g) in enumerate(kuski) if p == "комментарий"]
    L += ["## Комментарии дословно — сюда смотреть при правке дека", ""]
    if not komm_kuski:
        L.append("*Ни одного комментария не выделено. Либо дефектов не нашлось, либо маркер прозвучал иначе — проверь по сырой расшифровке.*")
        L.append("")
    else:
        for n, (_, seg, gotovaya) in enumerate(komm_kuski, 1):
            L.append(
                "### Комментарий %d — **[%s]**, %s, слайд: %s"
                % (n, mmss(seg[0][0]), minuty(seg[-1][1] - seg[0][0]), metka_kuska(seg, gotovaya))
            )
            L.append("")
            for ot, _, t in seg:
                L.append("**[%s]** %s" % (mmss(ot), t))
                L.append("")

    # ── рассказ ──────────────────────────────────────────────────────────────
    L += ["## Рассказ — куски и их длительность (это и есть калибровка лекции)", "", "| # | таймкод | длит. | слайд | начало реплики |", "|---|---|---|---|---|"]
    for n, (p, seg, gotovaya) in enumerate([k for k in kuski if k[0] == "рассказ"], 1):
        tekst = " ".join(t for _, _, t in seg)
        L.append("| %d | **[%s]** | %s | %s | %s… |" % (n, mmss(seg[0][0]), minuty(seg[-1][1] - seg[0][0]), metka_kuska(seg, gotovaya), tekst[:90].replace("|", "/")))
    L.append("")

    # ── служебное ────────────────────────────────────────────────────────────
    L += ["## Сработавшие маркеры (проверь, что ни один не ложный)", ""]
    if markery:
        for ot, kuda, pravilo, hvost in markery:
            L.append("- **[%s]** → %s (%s): «%s…»" % (mmss(ot), kuda, pravilo, hvost))
    else:
        L.append("*ни одного*")
    L += ["", "## Непривязанные и сомнительные", ""]
    bez = [
        n for n, (_, seg, g) in enumerate(komm_kuski, 1)
        if not g and not privyazka(" ".join(t for _, _, t in seg), spisok)
    ]
    L.append("- комментариев без привязки к слайду: **%d**%s" % (len(bez), (" (номера: %s)" % ", ".join(map(str, bez))) if bez else ""))
    L.append("- комментариев с привязкой под вопросом (`?`): смотри таблицу выше")
    if nezakrytye:
        L.append("- **комментарии без явного возврата** (граница угадана, проверь): %s" % ", ".join("[%s]–[%s], сегментов %d" % (mmss(a), mmss(b), n) for a, b, n in nezakrytye))
    else:
        L.append("- комментариев без явного возврата: 0")
    L.append("")
    L.append(
        "*Охват: сегментов в сырой расшифровке **%d**, после раскроя по маркерам **%d** "
        "(добавлено границ: %d), разобрано **%d** — ни один не потерян; "
        "кусков рассказа %d, комментариев %d.*"
        % (len(segmenty_syrye), len(segmenty), raskroeno,
           sum(len(seg) for _, seg, _ in kuski),
           len([1 for p, _, _ in kuski if p == "рассказ"]), len(komm_kuski))
    )

    vyhod = args.out or os.path.join(REPETICIA, "%s-razbor.md" % imya)
    open(vyhod, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("→ %s" % vyhod)
    print("ТАЙМИНГ: рассказ %s | комментарии %s | всего %s" % (minuty(rasskaz), minuty(komm), minuty(vsego)))
    print("маркеров сработало %d, комментариев %d, сегментов %d/%d"
          % (len(markery), len(komm_kuski), sum(len(seg) for _, seg, _ in kuski), len(segmenty)))


if __name__ == "__main__":
    main()
