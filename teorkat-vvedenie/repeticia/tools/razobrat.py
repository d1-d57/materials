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
    r"(?<![\w-])(продолжаем|продолжим|продолжаю|поехали|возвращаюсь|возвращаемся"
    r"|дальше по тексту|дальше по плану|обратно к рассказу|конец комментария)(?![\w-])",
    re.I,
)

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
                kuski.append((potok, tekushchij))
            tekushchij, potok = [], novyj
        tekushchij.append((ot, do, t))
    if tekushchij:
        kuski.append((potok, tekushchij))
    for i, (p, seg) in enumerate(kuski):
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
    kuski, markery, nezakrytye = razmetit(segmenty)

    rasskaz = sum(do - ot for p, seg in kuski if p == "рассказ" for ot, do, _ in seg)
    komm = sum(do - ot for p, seg in kuski if p == "комментарий" for ot, do, _ in seg)
    vsego = segmenty[-1][1] - segmenty[0][0]

    # ── разбор ───────────────────────────────────────────────────────────────
    L = [
        "# %s — разбор: рассказ / комментарии / тайминг" % imya,
        "",
        "> Собран `tools/razobrat.py` из `%s`. Правки — в `PRAVKI.md`, не здесь."
        % os.path.basename(args.syroj),
        "",
        "**Правило маркера** (подстрой речь под него, если неудобно):",
        "- **«стоп»** отдельным словом в любом регистре и с любыми знаками — рассказ → комментарий. «стоп-кадр» и «стопор» маркером НЕ считаются;",
        "- возврат — словом: «продолжаем», «продолжим», «продолжаю», «поехали», «возвращаюсь», «дальше по тексту», «конец комментария»;",
        "- **молчаливый возврат распознать нечем** — если возврат не назван, комментарием считается всё до следующего маркера. Подозрительно длинные комментарии перечислены в конце.",
        "",
        "## 🔴 ТАЙМИНГ — этого акта",
        "",
        "| | время | доля |",
        "|---|---|---|",
        "| **рассказ (чистый)** | **%s** | %d%% |" % (minuty(rasskaz), round(100 * rasskaz / max(1e-9, vsego))),
        "| комментарии | %s | %d%% |" % (minuty(komm), round(100 * komm / max(1e-9, vsego))),
        "| всего на записи | %s | 100%% |" % minuty(vsego),
        "",
    ]

    # накопительно по всей лекции
    json.dump(
        {"akt": imya, "rasskaz": rasskaz, "komm": komm, "vsego": vsego},
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

    # ── комментарии ──────────────────────────────────────────────────────────
    komm_kuski = [(i, seg) for i, (p, seg) in enumerate(kuski) if p == "комментарий"]
    L += ["## Комментарии — сюда смотреть при правке дека", ""]
    if not komm_kuski:
        L.append("*Ни одного «стоп» не поймано. Либо дефектов не нашлось, либо маркер прозвучал иначе — проверь по сырой расшифровке.*")
        L.append("")
    else:
        L += ["| # | таймкод | длит. | слайд (догадка) | дословно |", "|---|---|---|---|---|"]
        for n, (_, seg) in enumerate(komm_kuski, 1):
            tekst = " ".join(t for _, _, t in seg)
            kand = privyazka(tekst, spisok)
            if kand and kand[0][1] > 0 and (len(kand) < 2 or kand[0][0] >= kand[1][0] * 1.5):
                metka = "%s «%s»" % (kand[0][2]["metka"], kand[0][2]["zagolovok"])
            elif kand:
                metka = "? " + " / ".join("%s «%s»" % (k[2]["metka"], k[2]["zagolovok"]) for k in kand[:2])
            else:
                metka = "?"
            L.append(
                "| %d | **[%s]** | %s | %s | %s |"
                % (n, mmss(seg[0][0]), minuty(seg[-1][1] - seg[0][0]), metka, tekst.replace("|", "/"))
            )
        L.append("")

    # ── рассказ ──────────────────────────────────────────────────────────────
    L += ["## Рассказ — куски между комментариями", "", "| # | таймкод | длит. | слайд (догадка) | начало реплики |", "|---|---|---|---|---|"]
    for n, (p, seg) in enumerate([k for k in kuski if k[0] == "рассказ"], 1):
        tekst = " ".join(t for _, _, t in seg)
        kand = privyazka(tekst, spisok)
        metka = ("%s «%s»" % (kand[0][2]["metka"], kand[0][2]["zagolovok"])) if kand else "?"
        if kand and len(kand) > 1 and kand[0][0] < kand[1][0] * 1.5:
            metka = "? " + metka
        L.append("| %d | **[%s]** | %s | %s | %s… |" % (n, mmss(seg[0][0]), minuty(seg[-1][1] - seg[0][0]), metka, tekst[:90].replace("|", "/")))
    L.append("")

    # ── служебное ────────────────────────────────────────────────────────────
    L += ["## Сработавшие маркеры (проверь, что ни один не ложный)", ""]
    if markery:
        for ot, kuda, pravilo, hvost in markery:
            L.append("- **[%s]** → %s (%s): «%s…»" % (mmss(ot), kuda, pravilo, hvost))
    else:
        L.append("*ни одного*")
    L += ["", "## Непривязанные и сомнительные", ""]
    bez = [n for n, (_, seg) in enumerate(komm_kuski, 1) if not privyazka(" ".join(t for _, _, t in seg), spisok)]
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
           sum(len(seg) for _, seg in kuski),
           len([1 for p, _ in kuski if p == "рассказ"]), len(komm_kuski))
    )

    vyhod = args.out or os.path.join(REPETICIA, "%s-razbor.md" % imya)
    open(vyhod, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("→ %s" % vyhod)
    print("ТАЙМИНГ: рассказ %s | комментарии %s | всего %s" % (minuty(rasskaz), minuty(komm), minuty(vsego)))
    print("маркеров сработало %d, комментариев %d, сегментов %d/%d"
          % (len(markery), len(komm_kuski), sum(len(seg) for _, seg in kuski), len(segmenty)))


if __name__ == "__main__":
    main()
