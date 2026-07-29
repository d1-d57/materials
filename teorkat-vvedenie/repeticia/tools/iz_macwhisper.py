#!/usr/bin/env python3
"""Связка MacWhisper / Voice Memos → расшифровка в формате конвейера.

Зачем отдельный вход. Владелец пишет диктофоном и прогоняет через MacWhisper.
Его ТЕКСТОВЫЙ экспорт (`1.txt`) идёт одним куском без переводов строки — таймкоды
там потеряны. Но они не потеряны в самой связке: рядом с `originalAudio` лежит
`metadata.json`, где сегменты хранятся с началом, концом И ПОСЛОВНЫМИ таймингами.
То есть повторно гонять движок ради таймкодов не нужно — их надо просто достать.

Итог: расшифровка получается мгновенно и без счёта на GPU, а пословные тайминги
точнее, чем у моего прогона (там граница внутри сегмента интерполируется).
Слабое место: MacWhisper работает БЕЗ словаря терминов, поэтому редкие имена
(Жуайаль, Маклейн) он ломает чаще. Который источник брать — решается сверкой,
для неё и написан `--sverit`.

Запуск:
    python3 tools/iz_macwhisper.py ~/Downloads/1 --akt 1
    python3 tools/iz_macwhisper.py ~/Downloads/1 --akt 1 --sverit akt-1-syroj.md
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPETICIA = os.path.dirname(HERE)


def mmss(ms):
    s = int(ms / 1000.0)
    return "%02d:%02d" % (s // 60, s % 60)


def hhmmss(ms):
    s = int(ms / 1000.0)
    return "%d:%02d:%02d" % (s // 3600, (s % 3600) // 60, s % 60)


def chitat(put):
    if os.path.isdir(put):
        put = os.path.join(put, "metadata.json")
    if not os.path.exists(put):
        sys.exit("нет metadata.json: %s" % put)
    d = json.load(open(put, encoding="utf-8"))
    t = d.get("transcripts")
    if not isinstance(t, list) or not t:
        sys.exit("в metadata.json нет непустого списка transcripts")
    return d, t


def slova(s):
    return re.findall(r"[\wа-яёА-ЯЁ]+", s.lower())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("svyazka", help="папка связки (где originalAudio) или сам metadata.json")
    ap.add_argument("--akt", required=True, help="номер акта: 1..4")
    ap.add_argument("--sverit", default="", help="сверить с моим прогоном: akt-N-syroj.md")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    d, t = chitat(args.svyazka)
    vyhod = args.out or os.path.join(REPETICIA, "akt-%s-macwhisper-syroj.md" % args.akt)

    slov = sum(len(slova(s.get("text", ""))) for s in t)
    poslovno = sum(1 for s in t if s.get("words"))
    konec = t[-1].get("end", 0)

    L = [
        "# akt-%s — расшифровка из связки MacWhisper (дословно)" % args.akt,
        "",
        "> Первичка. Ничего не сокращено и не причёсано.",
        "> Таймкоды взяты из `metadata.json` связки, а НЕ пересчитаны заново:",
        "> движок там уже отработал, терять его тайминги незачем.",
        "",
        "- **источник:** `%s`" % args.svyazka,
        "- **движок связки:** %s, модель `%s`, язык %s"
        % (d.get("modelEngine", "?"), d.get("modelQualityID", "?"), d.get("modelLanguageID", "?")),
        "- **длительность:** %s" % hhmmss(konec),
        "- **сегментов:** %d, слов %d, из них с пословными таймингами сегментов %d"
        % (len(t), slov, poslovno),
        "- ⚠ **словарь терминов при этом прогоне НЕ подавался** (MacWhisper его не знает) — редкие имена могут быть искажены; сверка с прогоном по словарю: `--sverit`",
        "",
        "---",
        "",
    ]
    for s in t:
        tekst = (s.get("text") or "").strip()
        if tekst:
            L.append("**[%s]** %s" % (mmss(s.get("start", 0)), tekst))
            L.append("")
    open(vyhod, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("→ %s (сегментов %d, слов %d, длительность %s)" % (vyhod, len(t), slov, hhmmss(konec)))

    if args.sverit:
        if not os.path.exists(args.sverit):
            sys.exit("нет файла для сверки: %s" % args.sverit)
        import difflib

        moi = []
        for stroka in open(args.sverit, encoding="utf-8"):
            m = re.match(r"^\*\*\[(\d+):(\d\d)\]\*\*\s*(.+)$", stroka.strip())
            if m:
                moi += slova(re.sub("⚠", "", m.group(3)))
        ih = []
        for s in t:
            ih += slova(s.get("text", ""))
        sm = difflib.SequenceMatcher(a=ih, b=moi, autojunk=False)
        print(
            "\nСВЕРКА ДВУХ ДВИЖКОВ: у MacWhisper слов %d, у моего прогона %d, совпадение %.3f"
            % (len(ih), len(moi), sm.ratio())
        )
        krupnye = []
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != "equal" and max(i2 - i1, j2 - j1) >= 2:
                krupnye.append(
                    "  %-8s MacWhisper=«%s» || мой=«%s»"
                    % (tag, " ".join(ih[i1:i2])[:90], " ".join(moi[j1:j2])[:90])
                )
        print("расхождений в 2+ слова: %d" % len(krupnye))
        for k in krupnye[:40]:
            print(k)
        if len(krupnye) > 40:
            print("  … ещё %d" % (len(krupnye) - 40))


if __name__ == "__main__":
    main()
