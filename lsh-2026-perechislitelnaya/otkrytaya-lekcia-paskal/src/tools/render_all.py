#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ПЕТЛЯ «ПЕРЕСОБРАЛ → ПОСМОТРЕЛ». Снимает дек пачкой и кладёт контактный лист.

  python3 src/tools/render_all.py                 # все слайды в финальной сцене + лист
  python3 src/tools/render_all.py --scenes 3      # все сцены слайда 3 по одной
  python3 src/tools/render_all.py --scenes all    # все сцены всех слайдов (медленно)
  python3 src/tools/render_all.py --svg           # все illustrations/*.svg на доске дека
  python3 src/tools/render_all.py --svg domiki    # только названные рисунки
  python3 src/tools/render_all.py --out DIR       # куда класть (по умолчанию _render/)

🔴 ЗАЧЕМ ОТДЕЛЬНЫЙ ИНСТРУМЕНТ, РАЗ ЕСТЬ `_generator/render.py`.
Тот ходит по адресу `?only=N&scene=99`. Движок вешает слайду класс `.scene-99`,
а каскады раскрытия сцен кончаются на `.scene-9` (`base.css`) и `.scene-9`
(блюр-каскад в `shablon.html`). Совпадений нет ⇒ ВЕСЬ материал под `data-scene-from`
остаётся невидимым: из 15 слайдов старого дека 10 снимались с ПУСТОЙ доской.
Здесь номер сцены не передаётся вовсе — движок сам берёт `data-scenes` слайда,
то есть финальную сцену. Проверено попарно на слайде 2.

Рисунки смотрим НЕ через cairosvg (он не понимает классы `.s-*` и заливает всё
чёрным, а по атрибуту `width` ещё и врёт про пропорцию) — а браузером, на том же
фоне и с тем же CSS, что в деке. Класс, которого нет в движке, тут виден сразу.
"""
import re, sys, math, pathlib, tempfile

SRC = pathlib.Path(__file__).resolve().parent.parent
DECK = SRC / "dist" / "index.html"
W, H, DSR = 1440, 810, 2


def _args():
    a = sys.argv[1:]
    out = SRC / "_render"
    if "--out" in a:
        out = pathlib.Path(a[a.index("--out") + 1])
    return a, out


def deck_css():
    """Токены + правила .s-* из shablon.html — чтобы рисунок смотрелся как в деке."""
    tokens = (SRC / "tokens.css").read_text(encoding="utf-8")
    shab = (SRC / "shablon.html").read_text(encoding="utf-8")
    m = re.search(r"/\* -+ иллюстрации.*?\*/(.*?)\n/\*", shab, re.S)
    rules = m.group(1) if m else ""
    if ".s-line" not in rules:      # шаблон переставили — берём все .s-* правила подряд
        rules = "\n".join(re.findall(r"^\.s-[\w-]+\s*\{[^}]*\}", shab, re.M))
    fonts = (SRC / "fonts" / "faces.css").read_text(encoding="utf-8")
    return fonts + "\n" + tokens + "\n" + rules


def sheet(files, dest, cols=3, tile_w=620):
    from PIL import Image
    ims = [Image.open(f).convert("RGB") for f in files]
    if not ims:
        return
    th = int(tile_w * ims[0].height / ims[0].width)
    rows = math.ceil(len(ims) / cols)
    out = Image.new("RGB", (cols * tile_w, rows * th), "white")
    for i, im in enumerate(ims):
        out.paste(im.resize((tile_w, th)), ((i % cols) * tile_w, (i // cols) * th))
    out.save(dest)
    print("  ✓ контактный лист %s (%d кадров)" % (dest, len(ims)))


def main():
    from playwright.sync_api import sync_playwright
    a, out = _args()
    out.mkdir(parents=True, exist_ok=True)

    if "--svg" in a:
        names = [x for x in a[a.index("--svg") + 1:] if not x.startswith("-")]
        files = ([SRC / "illustrations" / (n + ".svg") for n in names] if names
                 else sorted((SRC / "illustrations").glob("*.svg")))
        css = deck_css()
        shots = []
        with sync_playwright() as p:
            b = p.chromium.launch(channel="chrome", headless=True)
            pg = b.new_page(viewport={"width": 1100, "height": 620}, device_scale_factor=2)
            for f in files:
                page = ("<meta charset='utf-8'>"      # без него О и Р приезжают мохнатыми
                        "<style>%s\nhtml,body{margin:0}"
                        "body{background:var(--board);display:grid;place-items:center;height:620px}"
                        ".panel{background:var(--card);width:1000px;height:540px;"
                        "display:grid;place-items:center;padding:26px}"
                        ".panel>svg{width:100%%;height:100%%;display:block}</style>"
                        "<div class='panel'>%s</div>"
                        % (css, f.read_text(encoding="utf-8")))
                tmp = pathlib.Path(tempfile.mkdtemp()) / "v.html"
                tmp.write_text(page, encoding="utf-8")
                pg.goto("file://" + str(tmp))
                pg.wait_for_timeout(320)
                dst = out / ("ill-%s.png" % f.stem)
                pg.screenshot(path=str(dst))
                shots.append(dst)
                print("  ✓ %s" % dst.name)
            b.close()
        sheet(shots, out / "sheet-ill.png", cols=2, tile_w=700)
        return 0

    if not DECK.is_file():
        print("нет %s — сначала build_deck.py" % DECK)
        return 1
    url = "file://" + str(DECK)

    if "--fit" in a:
        """Сколько ИМЕННО пикселей текста не влезло — чтобы резать по мерке,
        а не на глаз. audit.py говорит «overflow», но не говорит «на 74px»."""
        with sync_playwright() as p:
            b = p.chromium.launch(channel="chrome", headless=True)
            pg = b.new_page(viewport={"width": W, "height": H})
            pg.goto(url)
            pg.wait_for_timeout(400)
            n = pg.evaluate("() => document.querySelectorAll('.slide').length")
            rows = []
            for i in range(n):
                pg.goto("%s?only=%d" % (url, i))
                pg.wait_for_timeout(700)
                rows.append(pg.evaluate("""() => {
                  const s = document.querySelector('.slide:not([style*="display: none"])');
                  const z = s.querySelector('.zone.copy');
                  const brd = s.querySelector('.board');
                  return { id: s.id,
                           over: z ? z.scrollHeight - z.clientHeight : 0,
                           zh: z ? z.clientHeight : 0,
                           board: brd ? Math.round(brd.getBoundingClientRect().height) : 0 };
                }"""))
            b.close()
        print("%-18s %8s %8s %8s" % ("слайд", "не влез", "зона", "доска"))
        for r in rows:
            flag = "  ← режем" if r["over"] > 0 else ""
            print("%-18s %8d %8d %8d%s" % (r["id"], r["over"], r["zh"], r["board"], flag))
        bad = [r for r in rows if r["over"] > 0]
        print("\nпереполнено %d из %d" % (len(bad), len(rows)))
        return 0

    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=DSR)
        pg.goto(url)
        pg.wait_for_timeout(500)
        meta = pg.evaluate("() => Array.from(document.querySelectorAll('.slide'))"
                           ".map(s => ({id: s.id, n: +(s.dataset.scenes || 1)}))")
        shots = []
        if "--scenes" in a:
            which = a[a.index("--scenes") + 1]
            idxs = range(len(meta)) if which == "all" else [int(which)]
            for i in idxs:
                for k in range(1, meta[i]["n"] + 1):
                    pg.goto("%s?only=%d&scene=%d" % (url, i, k))
                    pg.wait_for_timeout(900)
                    dst = out / ("%02d-%s-s%d.png" % (i, meta[i]["id"], k))
                    pg.screenshot(path=str(dst))
                    shots.append(dst)
                    print("  ✓ %s" % dst.name)
        else:
            for i, m in enumerate(meta):
                pg.goto("%s?only=%d" % (url, i))     # БЕЗ scene= → движок берёт data-scenes
                pg.wait_for_timeout(900)
                dst = out / ("%02d-%s.png" % (i, m["id"]))
                pg.screenshot(path=str(dst))
                shots.append(dst)
                print("  ✓ %s  (сцен %d)" % (dst.name, m["n"]))
        b.close()
    sheet(shots, out / "sheet.png")
    print("готово: %d кадров в %s" % (len(shots), out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
