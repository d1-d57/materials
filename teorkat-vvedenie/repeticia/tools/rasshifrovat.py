#!/usr/bin/env python3
"""Акт репетиции → дословная расшифровка с таймкодами.

Вход:  audio/akt-N.m4a (или .wav/.mp3 — что угодно, что ест ffmpeg)
Выход: akt-N-syroj.md — сегменты [MM:SS] дословно, ничего не сокращая.

Нарезки по умолчанию НЕТ: whisper сам держит длинный файл и сам ставит
таймкоды, а ручная резка ломает сквозной тайминг (слово на стыке теряется или
задваивается). Резать законно ради устойчивости/параллелизма — тогда --rezat,
и тогда таймкоды пересчитываются в сквозные, а стыки проверяются.

Запуск:
    python3 tools/rasshifrovat.py audio/akt-1.m4a --blok A,B
    python3 tools/rasshifrovat.py audio/akt-1.m4a --rezat   # если движок падает на длине
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPETICIA = os.path.dirname(HERE)
MODEL = os.path.join(REPETICIA, "models", "ggml-large-v3.bin")
RABOTA = os.path.join(REPETICIA, ".rabota")  # промежуточные wav — не в git

# Резать по тишине куском примерно такой длины (сек), стык искать в тишине
# в окне ±KUSOK_LUFT вокруг границы. Перекрытие — чтобы слово на стыке
# попало в оба куска и его можно было сшить, а не потерять.
KUSOK = 600
KUSOK_LUFT = 90
PEREKRYTIE = 2.0

# Галлюцинации whisper на тишине. Модель обучена на субтитрах ютуба и на
# затяжной паузе выдаёт титры вместо молчания. Проверено на тестовом прогоне:
# в хвосте появилось «Редактор субтитров А.Семкин Корректор А.Егорова» —
# речи там не было вовсе. НЕ УДАЛЯЕМ (первичка дословная), а ПОМЕЧАЕМ: удалять
# по шаблону значит однажды вырезать живую фразу владельца.
GALLYUCINACII = [
    r"редактор\s+субтитров",
    r"корректор\s+[А-ЯA-Z]",
    r"субтитры\s+(сделал|подготовил|создал)",
    r"продолжение\s+следует",
    r"спасибо\s+за\s+(просмотр|внимание)\s*$",
    r"подпиш(итесь|ись)\s+на\s+канал",
    r"^\s*(ммм|ага|да)\s*[.!]?\s*$",
    r"^\s*\[?\s*(музыка|тишина|аплодисменты)\s*\]?\s*[.!]?\s*$",
]
RX_GALLYUC = re.compile("|".join(GALLYUCINACII), re.I)


def sh(cmd, **kw):
    """Запуск с обязательным показом кода возврата: 'упало' и 'сработало' снаружи выглядят одинаково."""
    t = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return p, round(time.time() - t, 1)


def mmss(sec):
    sec = max(0.0, float(sec))
    return "%02d:%02d" % (int(sec) // 60, int(sec) % 60)


def hhmmss(sec):
    sec = int(max(0.0, float(sec)))
    return "%d:%02d:%02d" % (sec // 3600, (sec % 3600) // 60, sec % 60)


def dlitelnost(put):
    p, _ = sh(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=nw=1:nk=1", put,
        ]
    )
    if p.returncode != 0:
        sys.exit("ffprobe rc=%d\n%s" % (p.returncode, p.stderr[-800:]))
    return float(p.stdout.strip())


def v_wav(vhod, vyhod, ot=None, skolko=None):
    """16 кГц моно — формат, который whisper.cpp ест напрямую (m4a он не берёт)."""
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    if ot is not None:
        cmd += ["-ss", "%.3f" % ot]
    cmd += ["-i", vhod]
    if skolko is not None:
        cmd += ["-t", "%.3f" % skolko]
    cmd += ["-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", vyhod]
    p, sek = sh(cmd)
    if p.returncode != 0:
        sys.exit("ffmpeg rc=%d\n%s" % (p.returncode, p.stderr[-800:]))
    return sek


def tishina(put):
    """Список моментов тишины (ffmpeg silencedetect) — точки, где резать безопасно."""
    p, _ = sh(
        [
            "ffmpeg", "-i", put, "-af",
            "silencedetect=noise=-32dB:d=0.45", "-f", "null", "-",
        ]
    )
    tochki = []
    for m in re.finditer(r"silence_start:\s*([0-9.]+)", p.stderr):
        tochki.append(float(m.group(1)))
    for m in re.finditer(r"silence_end:\s*([0-9.]+)\s*\|\s*silence_duration:\s*([0-9.]+)", p.stderr):
        # середина тишины — самая безопасная точка разреза
        konec, dlina = float(m.group(1)), float(m.group(2))
        tochki.append(konec - dlina / 2.0)
    return sorted(set(round(t, 2) for t in tochki))


def granicy(vsego, tochki, kusok=KUSOK, luft=KUSOK_LUFT):
    """Границы кусков: целимся в kusok, но садимся на ближайшую тишину."""
    if vsego <= kusok * 1.5:
        return [(0.0, vsego)]
    rezy, cel = [], float(kusok)
    while cel < vsego - kusok * 0.5:
        blizkie = [t for t in tochki if abs(t - cel) <= luft and t > (rezy[-1] if rezy else 0) + min(60, kusok / 4.0)]
        rez = min(blizkie, key=lambda t: abs(t - cel)) if blizkie else cel
        rezy.append(rez)
        cel = rez + kusok
    kraya = [0.0] + rezy + [vsego]
    return [(kraya[i], kraya[i + 1]) for i in range(len(kraya) - 1)]


def promt(bloki):
    """Промпт-словарь: на блок(и), если названы, иначе общий."""
    if bloki:
        chasti = []
        for b in bloki.split(","):
            put = os.path.join(REPETICIA, "prompt-%s.txt" % b.strip().upper())
            if not os.path.exists(put):
                sys.exit("нет промпта: %s" % put)
            chasti.append(open(put, encoding="utf-8").read().strip())
        if len(chasti) == 1:
            return chasti[0], "prompt-%s.txt" % bloki.upper()
        # два блока в одном акте: склейка перельёт 224 токена, поэтому берём общий
        return (
            open(os.path.join(REPETICIA, "prompt-obshchij.txt"), encoding="utf-8").read().strip(),
            "prompt-obshchij.txt (блоков названо %d, склейка перелила бы потолок)" % len(chasti),
        )
    put = os.path.join(REPETICIA, "prompt-obshchij.txt")
    return open(put, encoding="utf-8").read().strip(), "prompt-obshchij.txt"


def whisper(wav, tekst_promta, model, potoki, nesti, ml):
    """Один прогон whisper-cli → список сегментов [(от, до, текст)] в секундах.

    -ml/-sow дробят сегменты по словам до ~ml знаков. Без этого сегмент выходит
    на 10–15 с, и «стоп» садится ВНУТРЬ сегмента вместе с рассказом: граница
    комментария плывёт на десяток секунд, а тайминг — то, ради чего всё.
    """
    osnova = os.path.join(RABOTA, os.path.splitext(os.path.basename(wav))[0])
    cmd = [
        "whisper-cli", "-m", model, "-l", "ru", "-t", str(potoki),
        "--prompt", tekst_promta, "-oj", "-of", osnova, "-np",
        "-ml", str(ml), "-sow",
    ]
    if nesti:
        # промпт действует только на первое окно 30 с; для акта на полтора часа
        # его нужно нести дальше, иначе термины «уплывают» к середине записи
        cmd.append("--carry-initial-prompt")
    cmd.append(wav)  # файл — последним, позиционным
    p, sek = sh(cmd)
    if p.returncode != 0:
        return None, sek, p.returncode, (p.stderr or "")[-1500:]
    dannye = json.load(open(osnova + ".json", encoding="utf-8"))
    segmenty = []
    for s in dannye.get("transcription", []):
        ot = s["offsets"]["from"] / 1000.0
        do = s["offsets"]["to"] / 1000.0
        t = s["text"].strip()
        if t:
            segmenty.append((ot, do, t))
    return segmenty, sek, 0, ""


def slovca(t):
    return re.findall(r"[\wа-яёА-ЯЁ]+", t)


def sshit(kuski, perekrytie):
    """Склейка кусков в сквозную ленту + чистка стыков ПО СЛОВАМ.

    Слово на стыке попало в оба куска: надо убрать один экземпляр, а не оба
    (потеря) и не оставить оба (задвоение).

    Почему по словам, а не по сегментам: сегмент whisper длиннее перекрытия
    (7–12 с против 2 с), поэтому «сегмент целиком лежит в зоне перекрытия»
    почти никогда не выполняется. Проверено: при сегментном дедупе на стыке
    задвоилась фраза «Брауэр тут появляется не случайно» — снято 0 повторов
    из 1. Здесь ищем самое длинное совпадение ХВОСТА уже собранной ленты с
    НАЧАЛОМ нового куска (difflib, ≥3 слова) и срезаем ровно его.
    """
    import difflib

    lenta, otchet = [], []
    for nomer, (sdvig, granica, segmenty) in enumerate(kuski):
        sdvinuto = [(ot + sdvig, do + sdvig, t) for ot, do, t in segmenty]
        if nomer == 0:
            lenta.extend(sdvinuto)
            continue

        # Ход первый — по ВРЕМЕНИ, а не по тексту: предыдущий кусок покрыл звук
        # до granica, значит сегмент нового куска, целиком лежащий раньше неё, —
        # заведомо повторная расшифровка перекрытия. Это правило точное, тогда
        # как текстовое — на глазок (задвоение «естественное преобразование»
        # текстовый порог в 3 слова пропустил).
        po_vremeni = len([1 for _, do, _ in sdvinuto if do <= granica + 0.05])
        sdvinuto = [(ot, do, t) for ot, do, t in sdvinuto if do > granica + 0.05]

        hvost = slovca(" ".join(t for _, _, t in lenta[-8:]))[-60:]
        # головные слова нового куска с привязкой к своему сегменту
        golova, adres = [], []
        for i, (_, _, t) in enumerate(sdvinuto[:8]):
            for w in slovca(t):
                golova.append(w)
                adres.append(i)
                if len(golova) >= 60:
                    break
            if len(golova) >= 60:
                break

        srezat = 0
        if hvost and golova:
            sm = difflib.SequenceMatcher(
                a=[w.lower() for w in hvost], b=[w.lower() for w in golova], autojunk=False
            )
            for i, j, size in sm.get_matching_blocks():
                # совпадение, доходящее до конца хвоста и начинающееся у начала
                # головы, — это и есть перекрытие; всё прочее совпадение случайно
                if not (size >= 1 and i + size >= len(hvost) - 2 and j <= 3):
                    continue
                dlinno = sum(len(w) for w in golova[j:j + size]) >= 12
                if size >= 3 or dlinno:
                    srezat = max(srezat, j + size)

        ostavleno, snyato_slov = [], srezat
        for i, (ot, do, t) in enumerate(sdvinuto):
            if srezat <= 0:
                ostavleno.append((ot, do, t))
                continue
            svoi = slovca(t)
            if len(svoi) <= srezat:
                srezat -= len(svoi)  # сегмент съеден перекрытием целиком
                continue
            # часть сегмента — обрезаем слова и сдвигаем начало пропорционально
            ostatok = svoi[srezat:]
            hvost_teksta = t
            for w in svoi[:srezat]:
                p = hvost_teksta.find(w)
                hvost_teksta = hvost_teksta[p + len(w):]
            dolya = srezat / float(len(svoi))
            ostavleno.append((ot + (do - ot) * dolya, do, hvost_teksta.strip(" ,.—-«»")))
            srezat = 0
        lenta.extend(ostavleno)
        otchet.append(
            "стык %d на %s: перекрытие %.1f с, по времени снято сегментов %d, "
            "по тексту снято задвоенных слов %d, слов до стыка %d, после стыка %d"
            % (nomer, mmss(granica), perekrytie, po_vremeni, snyato_slov, len(hvost),
               len(slovca(" ".join(t for _, _, t in ostavleno[:8]))))
        )
    return lenta, otchet


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--blok", default="", help="A / A,B — какой словарь подать; пусто = общий")
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--rezat", action="store_true", help="резать по тишине (движок падает на длине / нужна устойчивость)")
    ap.add_argument("--potoki", type=int, default=max(4, (os.cpu_count() or 8) - 2))
    ap.add_argument("--bez-nesti", action="store_true", help="не нести промпт через всю запись")
    ap.add_argument("--ml", type=int, default=100, help="макс. длина сегмента в знаках (0 — как решит движок)")
    ap.add_argument("--kusok", type=int, default=KUSOK, help="длина куска при --rezat, с (для проверки нарезки на коротком файле)")
    ap.add_argument("--luft", type=int, default=KUSOK_LUFT, help="окно поиска тишины вокруг границы, с")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    for nuzhno in ("ffmpeg", "ffprobe", "whisper-cli"):
        if not shutil.which(nuzhno):
            sys.exit("нет в PATH: %s" % nuzhno)
    if not os.path.exists(args.audio):
        sys.exit("нет файла: %s" % args.audio)
    if not os.path.exists(args.model):
        sys.exit("нет модели: %s" % args.model)
    os.makedirs(RABOTA, exist_ok=True)

    imya = os.path.splitext(os.path.basename(args.audio))[0]
    vyhod = args.out or os.path.join(REPETICIA, "%s-syroj.md" % imya)
    tekst_promta, chej_promt = promt(args.blok)
    vsego_sek = dlitelnost(args.audio)
    nachalo = time.time()

    print("акт: %s (%s)" % (args.audio, hhmmss(vsego_sek)))
    print("модель: %s" % os.path.basename(args.model))
    print("словарь: %s (%d знаков)" % (chej_promt, len(tekst_promta)))

    kuski_granic = [(0.0, vsego_sek)]
    prichina_rezki = "не резал: whisper держит длинный файл сам, сквозной таймкод целее"
    if args.rezat:
        t = tishina(args.audio)
        kuski_granic = granicy(vsego_sek, t, args.kusok, args.luft)
        prichina_rezki = (
            "резал по тишине (--rezat): кусков %d по ~%d с, найдено точек тишины %d, "
            "перекрытие %.1f с, таймкоды пересчитаны в сквозные"
            % (len(kuski_granic), args.kusok, len(t), PEREKRYTIE)
        )
        print(prichina_rezki)

    kuski, zhurnal = [], []
    for i, (ot, do) in enumerate(kuski_granic):
        rezhem = len(kuski_granic) > 1
        sdvig = max(0.0, ot - (PEREKRYTIE if i > 0 else 0.0))
        dlina = (do - sdvig) if rezhem else None
        wav = os.path.join(RABOTA, "%s-%02d.wav" % (imya, i))
        sek_ff = v_wav(args.audio, wav, ot=(sdvig if rezhem else None), skolko=dlina)
        segmenty, sek_w, rc, oshibka = whisper(
            wav, tekst_promta, args.model, args.potoki, not args.bez_nesti, args.ml
        )
        if segmenty is None:
            print("whisper rc=%d на куске %d\n%s" % (rc, i, oshibka))
            sys.exit("прогон не удался; если дело в длине — перезапусти с --rezat")
        print(
            "  кусок %d/%d %s–%s: сегментов %d, whisper %.0f с (×%.2f к реальному времени)"
            % (i + 1, len(kuski_granic), mmss(sdvig), mmss(do), len(segmenty), sek_w,
               ((do - sdvig) / sek_w) if sek_w else 0)
        )
        zhurnal.append("кусок %d: ffmpeg %.1f с, whisper %.1f с, сегментов %d, rc=0" % (i + 1, sek_ff, sek_w, len(segmenty)))
        kuski.append((sdvig, ot, segmenty))  # ot — истинная граница реза, до неё звук уже расшифрован

    if len(kuski) == 1:
        lenta, styki = [(ot, do, t) for ot, do, t in kuski[0][2]], []
    else:
        lenta, styki = sshit(kuski, PEREKRYTIE)

    slov = len(re.findall(r"\w+", " ".join(t for _, _, t in lenta)))
    podozritelnye = [(ot, t) for ot, _, t in lenta if RX_GALLYUC.search(t)]
    stroki = [
        "# %s — сырая расшифровка (дословно)" % imya,
        "",
        "> Первичка. Ничего не сокращено, не причёсано, не «улучшено» —",
        "> на ней стоит и тайминг, и сводка правок. Правки вносить не здесь.",
        "",
        "- **источник:** `%s`, длительность **%s**" % (args.audio, hhmmss(vsego_sek)),
        "- **движок:** whisper.cpp (`whisper-cli`), модель `%s`, язык ru, потоков %d"
        % (os.path.basename(args.model), args.potoki),
        "- **словарь-промпт:** `%s`%s"
        % (chej_promt, "" if args.bez_nesti else ", несётся через всю запись (`--carry-initial-prompt`)"),
        "- **нарезка:** %s" % prichina_rezki,
        "- **итог:** сегментов **%d**, слов **%d**, прогон **%s** (×%.2f к реальному времени)"
        % (len(lenta), slov, hhmmss(time.time() - nachalo),
           vsego_sek / max(1e-9, time.time() - nachalo)),
    ]
    for z in zhurnal:
        stroki.append("- %s" % z)
    for s in styki:
        stroki.append("- **%s**" % s)
    stroki.append(
        "- **подозрение на галлюцинацию (речи нет, модель дописала титры): %d** — помечены ⚠ в тексте, НЕ удалены%s"
        % (len(podozritelnye), (": " + ", ".join("[%s]" % mmss(o) for o, _ in podozritelnye)) if podozritelnye else "")
    )
    stroki += ["", "---", ""]
    for ot, do, t in lenta:
        metka = "⚠ " if RX_GALLYUC.search(t) else ""
        stroki.append("**[%s]** %s%s" % (mmss(ot), metka, t))
        stroki.append("")
    open(vyhod, "w", encoding="utf-8").write("\n".join(stroki) + "\n")
    print("→ %s (сегментов %d, слов %d)" % (vyhod, len(lenta), slov))
    for s in styki:
        print("  %s" % s)


if __name__ == "__main__":
    main()
