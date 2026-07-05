#!/usr/bin/env python3
"""Render harness for ZAHOD-04. Two modes:
  static: shot.py <idx> <scene> <out.png> [waitms]   -> uses ?only=idx&scene=scene
  nav:    shot.py --nav "<js>" <out.png> [waitms]     -> loads deck, runs js (e.g. showSingle(9,3)), screenshots
Always 1440x810, chrome channel, deviceScaleFactor 2."""
import sys, pathlib
from playwright.sync_api import sync_playwright

HTML = pathlib.Path(__file__).resolve().parent.parent / "index.html"

def run():
    a = sys.argv[1:]
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        pg = b.new_page(viewport={"width":1440,"height":810}, device_scale_factor=2)
        if a[0] == "--nav":
            js, out = a[1], a[2]
            wait = int(a[3]) if len(a) > 3 else 1500
            pg.goto(f"file://{HTML}")
            pg.wait_for_timeout(500)
            pg.evaluate(js)
            pg.wait_for_timeout(wait)
        else:
            idx, scene, out = a[0], a[1], a[2]
            wait = int(a[3]) if len(a) > 3 else 1500
            pg.goto(f"file://{HTML}?only={idx}&scene={scene}")
            pg.wait_for_timeout(wait)
        pg.screenshot(path=out)
        # report which slide id is visible + any measure hook result
        info = pg.evaluate("""() => {
          const vis = Array.from(document.querySelectorAll('.slide')).map((s,i)=>[i,s.id,s.style.display]).filter(x=>x[2]!=='none');
          return vis;
        }""")
        print("visible:", info)
        b.close()

run()
