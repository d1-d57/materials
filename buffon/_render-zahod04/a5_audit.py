#!/usr/bin/env python3
"""A5 canvas-sim lifecycle audit. READ-ONLY (no file edits to deck)."""
import pathlib, json
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
HTML = HERE.parent / "index.html"

# name, idx, maxscene, LAB key
SIMS = [
    ("needles",         3,  3, "sl-sim:needles"),
    ("convergence",     4,  2, "sl-convergence:convergence"),
    ("coin",            5,  2, "sl-coin:coin"),
    ("yellow",          9,  4, "sl-yellow:yellow"),
    ("prob",            11, 2, "sl-prob:prob"),
    ("polygons",        12, 4, "sl-polygons:polygons"),
    ("circle",          13, 4, "sl-circle:circle"),
    ("result",          14, 3, "sl-result:result"),
    ("coords-needles",  17, 2, "sl-coords:coords-needles"),
    ("coords-phase",    17, 2, "sl-coords:coords-phase"),
    ("phase-mass@cond", 18, 3, "sl-condition:phase-mass"),
    ("phase-mass@phase",19, 1, "sl-phase:phase-mass"),
    ("cos-area",        20, 5, "sl-area:cos-area"),
]

SNAP = """(key) => {
  const e = (window.LAB||{})[key];
  if (!e) return {missing:true};
  const o = e.o || {};
  return {
    n: (e.n===undefined?null:e.n),
    running: (e.running===undefined?null:e.running),
    target: (e.target===undefined?null:e.target),
    endless: (o.endless===undefined?null:o.endless),
  };
}"""

def run():
    rows = []
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        pg = b.new_page(viewport={"width":1440,"height":810}, device_scale_factor=2)
        pg.goto(f"file://{HTML}")
        pg.wait_for_timeout(700)
        for name, idx, mx, key in SIMS:
            r = {"name":name,"key":key,"idx":idx,"scene":mx}
            # 1. first enter (from title/current) - go to title first to guarantee hidden->visible
            pg.evaluate("showSingle(0,1)")
            pg.wait_for_timeout(400)
            pg.evaluate(f"showSingle({idx},{mx})")
            pg.wait_for_timeout(1800)
            s1 = pg.evaluate(SNAP, key)
            r["s1_1800"] = s1
            safe = name.replace("@","-")
            pg.screenshot(path=str(HERE/f"a5_{safe}_1enter.png"))
            # 2. after +1200ms
            pg.wait_for_timeout(1200)
            r["s1_3000"] = pg.evaluate(SNAP, key)
            # 3. leave
            pg.evaluate("showSingle(0,1)")
            pg.wait_for_timeout(600)
            # 4. re-enter
            pg.evaluate(f"showSingle({idx},{mx})")
            pg.wait_for_timeout(300)
            r["re_300"] = pg.evaluate(SNAP, key)
            pg.wait_for_timeout(1500)
            r["re_1800"] = pg.evaluate(SNAP, key)
            pg.screenshot(path=str(HERE/f"a5_{safe}_2reenter.png"))
            rows.append(r)
            print(f"[done] {name}: {json.dumps(r['s1_1800'])} | re0={json.dumps(r['re_300'])} re={json.dumps(r['re_1800'])}")
        b.close()
    print("\n=== JSON ===")
    print(json.dumps(rows, indent=1))

run()
