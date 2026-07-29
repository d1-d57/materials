#!/usr/bin/env python3
"""Гейт предвёрсточной ленты (арка 6, G7). Печатает то, что заход требует напечатать,
и НЕ принимает на веру ни одного числа, вписанного руками.

    python3 teorkat-vvedenie/raskadrovka/gejt_lenty.py                       # наша лента
    python3 teorkat-vvedenie/raskadrovka/gejt_lenty.py --etalon              # эталон Паскаля из git

Линейка объявлена здесь, а не в отчёте, потому что в каноне её нет: замер «медиана 50 слов /
324 знака» снят неизвестным счётчиком, и сравнивать с ним можно только прогнав ТОТ ЖЕ счётчик
по эталону. Поэтому у скрипта два режима, и оба печатают одну и ту же линейку.

ЛИНЕЙКА (видимый текст слайда):
  - выбрасывается: фронтматтер, `# `-заголовок файла, все боковые поля `> поле:…`,
    блоки `<figure>…</figure>` и `<table>…</table>` целиком (в деке подписей не будет,
    а таблица — это иллюстрация слайда, не его проза);
  - `$$…$$` отдельной строкой считается за 3 слова и 120 знаков (две строки экрана с воздухом:
    длина исходника формулы к её месту на экране отношения не имеет);
  - `$…$` внутри строки считается за 1 слово, знаки — по длине без знаков доллара;
  - маркеры разметки (`**`, ведущий `- `, `·`) в знаки не идут.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEKSTY = ROOT / "teorkat-vvedenie" / "raskadrovka" / "teksty"
ETALON_COMMIT = "4833841"
ETALON_PATHS = [
    "lsh-2026-perechislitelnaya/otkrytaya-lekcia-paskal/raskadrovka/teksty/blok-1.md",
    "lsh-2026-perechislitelnaya/otkrytaya-lekcia-paskal/raskadrovka/teksty/blok-2.md",
]

DISPLAY_WORDS, DISPLAY_CHARS = 3, 120


def strip_blocks(lines):
    """Выбрасывает <figure>…</figure> и <table>…</table> целиком, вместе с содержимым."""
    out, depth = [], 0
    for ln in lines:
        low = ln.strip().lower()
        if depth == 0 and (low.startswith("<figure") or low.startswith("<table")):
            depth = 1
            if "</figure>" in low or "</table>" in low:
                depth = 0
            continue
        if depth:
            if "</figure>" in low or "</table>" in low:
                depth = 0
            continue
        out.append(ln)
    return out


SCENE_TAG = re.compile(r"^\{@([-\d]+)\}\s*")


def unscene(s):
    """Снимает сценовую разметку Р2, оставляя ровно тот текст, который будет ВИДЕН.
    Ведущий тег `{@N}`/`{@N-M}`/`{@-M}` уходит целиком; из инлайновых шторок остаётся
    их видимое содержимое (`{@N|x}`→`x`, `{fill@N|бланк|ответ}`→`ответ`, `{blur@N|x}`→`x`).
    Без этого метка сцены попадала бы в счёт слов и знаков слайда."""
    s = SCENE_TAG.sub("", s)
    s = re.sub(r"\{fill@[-\d]+\|[^|}]*\|([^}]*)\}", r"\1", s)
    s = re.sub(r"\{(?:blur)?@[-\d]+\|([^}]*)\}", r"\1", s)
    return s


def measure(lines):
    """→ (слов, знаков, число предложений, число блоков **acc**, число тире, плакатных единиц).

    Плакатная единица — второй срез длины фразы, заведённый заходом сжатия. `[.!?]`-сплиттер
    один по себе врёт на плакатном тексте: канон 06-tekst запрещает финальную точку, поэтому
    две соседние строки без точек склеиваются в одно «предложение» на 40 слов. Единица =
    строка, а внутри строки — ещё и каждое законченное точкой предложение."""
    words = chars = units = 0
    text_for_sent = []
    for ln in lines:
        s = unscene(ln.strip())
        if not s:
            continue
        if s.startswith(">") or s.startswith("<") or s.startswith("#"):
            continue
        if s.startswith("$$") and s.endswith("$$") and len(s) > 4:
            words += DISPLAY_WORDS
            chars += DISPLAY_CHARS
            units += 1
            continue
        inline = re.findall(r"\$[^$]+\$", s)
        bare = re.sub(r"\$[^$]+\$", " ", s)
        bare = bare.replace("**", "").replace("·", " ")
        bare = re.sub(r"^-\s+", "", bare)
        words += len([w for w in bare.split() if w]) + len(inline)
        chars += len(bare.strip()) + sum(len(f) - 2 for f in inline)
        units += max(1, len([x for x in re.split(r"[.!?]+", bare) if x.strip()]))
        text_for_sent.append(bare)
    joined = " ".join(text_for_sent)
    sentences = len([x for x in re.split(r"[.!?]+\s+|[.!?]+$", joined) if x.strip()])
    accents = sum(len(re.findall(r"\*\*[^*]+\*\*", ln)) for ln in lines if not ln.strip().startswith(">"))
    dashes = joined.count("—")
    return words, chars, sentences, accents, dashes, units


def parse(md_text, fname):
    """→ (tab, poryadok, [ {name, lines, layout, figures} ])."""
    body = md_text
    tab, order = fname, 999
    if body.startswith("---"):
        fm, _, body = body[3:].partition("\n---")
        for ln in fm.splitlines():
            if ln.startswith("tab:"):
                tab = ln.split(":", 1)[1].strip()
            if ln.startswith("poryadok:"):
                order = int(ln.split(":", 1)[1].strip())
    secs, cur = [], None
    for ln in body.splitlines():
        if ln.startswith("## "):
            cur = {"name": ln[3:].strip(), "raw": [], "file": fname, "tab": tab}
            secs.append(cur)
        elif cur is not None:
            cur["raw"].append(ln)
    for s in secs:
        s["layout"] = any(re.search(r"поле:mn\s+\*\*Раскладка\.\*\*", l) for l in s["raw"])
        s["split"] = any(re.search(r"поле:mn\s+\*\*SPLIT\.\*\*", l) for l in s["raw"])
        s["figures"] = sum(1 for l in s["raw"] if "<svg" in l or "🖼" in l)
        s["lines"] = strip_blocks(s["raw"])
        s["w"], s["c"], s["sent"], s["acc"], s["dash"], s["units"] = measure(s["lines"])
        s["scenes"] = scenes_of(s["lines"])
    return tab, order, secs


# ───────────────────────── сцены (арка 8, синтаксис Р2) ─────────────────────────
def blocks_of(lines):
    """Абзацы раздела: разделитель — пустая строка. → [ {lines, frm, until, w, c} ].
    Сценовый тег читается ТОЛЬКО у первой строки абзаца — ровно как у движка
    (`build_deck.py` SCENE_PREFIX: у списка `- ` ведущего тега нет вовсе)."""
    out, cur = [], []
    for ln in list(lines) + [""]:
        if ln.strip():
            cur.append(ln)
            continue
        if cur:
            frm, until = 1, None
            m = SCENE_TAG.match(cur[0].strip())
            if m:
                body = m.group(1)
                if "-" in body:
                    a, _, b = body.partition("-")
                    frm = int(a) if a else 1
                    until = int(b) if b else None
                else:
                    frm = int(body)
            w, c = measure(cur)[0], measure(cur)[1]
            out.append({"lines": cur, "frm": frm, "until": until, "w": w, "c": c})
            cur = []
    return out


def scenes_of(lines):
    """→ {n, кадры[{ k, w, c, видимые-индексы-абзацев }], дефекты[…]}.
    Кадр k показывает абзацы с frm ≤ k ≤ until. Дефекты: пустой клик (кадр не отличается
    от предыдущего) и «последняя вернулась в первую» (ловушка, названная владельцем)."""
    blocks = [b for b in blocks_of(lines) if b["w"] > 0]
    n = 1
    for b in blocks:
        n = max(n, b["frm"], b["until"] or 0)
    frames = []
    for k in range(1, n + 1):
        vis = [i for i, b in enumerate(blocks) if b["frm"] <= k and (b["until"] is None or k <= b["until"])]
        frames.append({"k": k, "vis": set(vis),
                       "w": sum(blocks[i]["w"] for i in vis),
                       "c": sum(blocks[i]["c"] for i in vis)})
    bad = []
    for k in range(1, len(frames)):
        if frames[k]["vis"] == frames[k - 1]["vis"]:
            bad.append("дед-клик на сцене %d" % (k + 1))
    if n > 1 and frames[0]["vis"] == frames[-1]["vis"]:
        bad.append("последняя сцена совпала с первой")
    return {"n": n, "frames": frames, "bad": bad}


def groups_of(secs):
    """Обратная склейка предвёрстки: раздел + идущие за ним ПОДРЯД разделы со
    `> поле:mn **SPLIT.**` = один слайд. На сжатой ленте групп ровно столько же,
    сколько разделов, — и именно это гейт и обязан показывать."""
    groups = []
    for s in secs:
        if s["split"] and groups:
            groups[-1].append(s)
        else:
            groups.append([s])
    return groups


def load_ours():
    files = sorted(TEKSTY.glob("*.md"))
    got = [parse(p.read_text(encoding="utf-8"), p.name) for p in files]
    got.sort(key=lambda x: x[1])
    return got


def load_etalon():
    got = []
    for p in ETALON_PATHS:
        txt = subprocess.run(
            ["git", "--no-optional-locks", "show", "%s:%s" % (ETALON_COMMIT, p)],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout
        got.append(parse(txt, Path(p).name))
    got.sort(key=lambda x: x[1])
    return got


def median(xs):
    xs = sorted(xs)
    if not xs:
        return 0
    m = len(xs) // 2
    return xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2


def main():
    etalon = "--etalon" in sys.argv
    got = load_etalon() if etalon else load_ours()
    secs = [s for _, _, ss in got for s in ss]

    print("=" * 78)
    print("ЛЕНТА:", "ЭТАЛОН ПАСКАЛЯ (%s)" % ETALON_COMMIT if etalon else TEKSTY)
    print("=" * 78)
    print("%-4s %-34s %5s %6s %5s %4s %4s %4s" %
          ("#", "раздел", "слов", "знаков", "предл", "acc", "тире", "илл"))
    for i, s in enumerate(secs, 1):
        print("%-4d %-34s %5d %6d %5d %4d %4d %4d" %
              (i, s["name"][:34], s["w"], s["c"], s["sent"], s["acc"], s["dash"], s["figures"]))

    ws = [s["w"] for s in secs]
    cs = [s["c"] for s in secs]
    print("-" * 78)
    print("РАЗДЕЛОВ: %d   МЕДИАНА: %g слов / %g знаков   макс %d/%d   мин %d/%d"
          % (len(secs), median(ws), median(cs), max(ws), max(cs), min(ws), min(cs)))

    print("\nГИСТОГРАММА СЛОВ (шаг 15):")
    for lo in range(0, (max(ws) // 15 + 1) * 15, 15):
        n = len([w for w in ws if lo <= w < lo + 15])
        print("  %3d–%3d | %s %d" % (lo, lo + 14, "#" * n, n))

    print("\nВНЕ КОРИДОРА 45–57 СЛОВ (читаемый регистр):")
    out = [s for s in secs if not (45 <= s["w"] <= 57)]
    for s in out:
        print("   %-36s %4d слов  (%s)" % (s["name"][:36], s["w"], s["file"]))
    print("   ИТОГО вне коридора: %d из %d" % (len(out), len(secs)))

    print("\nАРХЕТИПНЫЕ ПОТОЛКИ (односторонние — обязаны быть 0):")
    print("   обложка (первый раздел) > 25 слов:",
          "❌ %d" % secs[0]["w"] if secs[0]["w"] > 25 else "✅ 0  (обложка: %d слов)" % secs[0]["w"])
    heavy = [s for s in secs[1:] if s["figures"] == 0 and s["c"] > 650]
    print("   text-only (без илл.) > 650 знаков:",
          "❌ %d — %s" % (len(heavy), ", ".join(s["name"][:24] for s in heavy)) if heavy else "✅ 0")

    print("\nРАСКЛАДКА:")
    nolay = [s for s in secs[1:] if not s["layout"]]
    print("   разделов без «поле:mn **Раскладка.**» (кроме обложки): %d %s"
          % (len(nolay), "— " + ", ".join(s["name"][:28] for s in nolay) if nolay else "✅"))

    print("\nИЛЛЮСТРАЦИИ:")
    noill = [s for s in secs[1:] if s["figures"] == 0]
    print("   слайдов без единой картинки: %d из %d" % (len(noill), len(secs) - 1))
    for s in noill:
        print("     · %s" % s["name"])

    sent = sum(s["sent"] for s in secs)
    units = sum(s["units"] for s in secs)
    print("\nДЛИНА ФРАЗЫ (две линейки; вторая — плакатная единица, см. measure):")
    print("   на предложение `[.!?]`: %5.1f слова  (%d слов / %d предложений)" % (sum(ws) / sent, sum(ws), sent))
    print("   на плакатную единицу : %5.1f слова  (%d слов / %d единиц)" % (sum(ws) / units, sum(ws), units))

    groups = groups_of(secs)
    print("\nОБРАТНАЯ СКЛЕЙКА ПО SPLIT (групп = слайдов; обязано быть 33 = обложка + 32):")
    gw = [sum(x["w"] for x in g) for g in groups]
    gc = [sum(x["c"] for x in g) for g in groups]
    print("   ГРУПП: %d %s   медиана %g слов / %g знаков   макс %d/%d"
          % (len(groups), "✅" if len(groups) == 33 else "❌", median(gw), median(gc), max(gw), max(gc)))
    multi = [g for g in groups if len(g) > 1]
    print("   групп из >1 раздела (несхлопнутых): %d %s"
          % (len(multi), "✅" if not multi else "— " + ", ".join(g[0]["name"][:22] for g in multi)))

    print("\nСЦЕНЫ (бюджет — на КАДР, не на слайд: ≤650 знаков видимого разом):")
    print("%-4s %-38s %5s %6s %6s  %s" % ("#", "слайд", "сцен", "макс w", "макс c", "дефекты"))
    over, deadclicks, withscenes = [], [], []
    for i, s in enumerate(secs, 1):
        sc = s["scenes"]
        mw = max(f["w"] for f in sc["frames"])
        mc = max(f["c"] for f in sc["frames"])
        if sc["n"] > 1:
            withscenes.append(s)
        if mc > 650:
            over.append((s["name"], mc))
        if sc["bad"]:
            deadclicks.append((s["name"], sc["bad"]))
        print("%-4d %-38s %5d %6d %6d  %s"
              % (i, s["name"][:38], sc["n"], mw, mc, "; ".join(sc["bad"]) or ""))
    scene_ws = [f["w"] for s in secs for f in s["scenes"]["frames"]]
    scene_cs = [f["c"] for s in secs for f in s["scenes"]["frames"]]
    print("   кадров всего %d   МЕДИАНА НА КАДР %g слов / %g знаков"
          % (len(scene_ws), median(scene_ws), median(scene_cs)))
    print("   слайдов со ≥2 сценами: %d" % len(withscenes))
    print("   кадров > 650 знаков: %s" % ("✅ 0" if not over else "❌ %d — %s" % (len(over), over)))
    print("   пустых кликов / откатов на первую сцену: %s"
          % ("✅ 0" if not deadclicks else "❌ %s" % deadclicks))

    print("\nСЦЕНОВЫЕ ШОРТКАТЫ (заход сжатия ввёл их В ЛЕНТУ — контракт арки 6, `06-tekst/DOK.md` стр. 19):")
    joined = "\n".join(l for s in secs for l in s["raw"])
    for pat in (r"\{@\d", r"\{@\d+-", r"\{@-", r"\{blur@", r"\{fill@"):
        print("   %-10s %d" % (pat, len(re.findall(pat, joined))))

    print("\nПО ФАЙЛАМ:")
    for tab, order, ss in got:
        print("   %-2s %-34s разделов %2d · медиана %g слов"
              % (order, tab, len(ss), median([s["w"] for s in ss])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
