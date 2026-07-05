#!/usr/bin/env python3
"""Lifecycle probe on the correct state fields: coords (activeIdx) + cos-area (t, running)."""
import pathlib, json
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
HTML = HERE.parent / "index.html"

def snap(pg, key, fields):
    return pg.evaluate("""(a)=>{const[k,fs]=a;const e=(window.LAB||{})[k];if(!e)return{missing:1};
      const o={};for(const f of fs)o[f]=(e[f]===undefined?null:e[f]);return o;}""", [key, fields])

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(viewport={"width":1440,"height":810}, device_scale_factor=2)
    pg.goto(f"file://{HTML}"); pg.wait_for_timeout(700)

    # COORDS (idx17 scene2): state=activeIdx (advances 0..T), running not present
    print("== coords-needles (activeIdx, T) ==")
    pg.evaluate("showSingle(0,1)"); pg.wait_for_timeout(400)
    pg.evaluate("showSingle(17,2)"); pg.wait_for_timeout(1800)
    print(" 1e@1.8:", snap(pg,"sl-coords:coords-needles",["activeIdx","T"]))
    pg.wait_for_timeout(1200)
    print(" 1e@3.0:", snap(pg,"sl-coords:coords-needles",["activeIdx","T"]))
    pg.evaluate("showSingle(0,1)"); pg.wait_for_timeout(600)
    pg.evaluate("showSingle(17,2)"); pg.wait_for_timeout(300)
    print(" re@0.3:", snap(pg,"sl-coords:coords-needles",["activeIdx","T"]))
    pg.wait_for_timeout(1500)
    print(" re@1.8:", snap(pg,"sl-coords:coords-needles",["activeIdx","T"]))

    # COS-AREA (idx20 scene5): state=t (0->1 then self-stop), running
    print("\n== cos-area (t, running, reveal) ==")
    pg.evaluate("showSingle(0,1)"); pg.wait_for_timeout(400)
    pg.evaluate("showSingle(20,5)"); pg.wait_for_timeout(1800)
    print(" 1e@1.8:", snap(pg,"sl-area:cos-area",["t","running","reveal"]))
    pg.wait_for_timeout(1200)
    print(" 1e@3.0:", snap(pg,"sl-area:cos-area",["t","running","reveal"]))
    pg.wait_for_timeout(4000)  # let it reach t>=1 and self-stop (dur~6s)
    print(" 1e@7.0:", snap(pg,"sl-area:cos-area",["t","running","reveal"]))
    pg.evaluate("showSingle(0,1)"); pg.wait_for_timeout(600)
    pg.evaluate("showSingle(20,5)"); pg.wait_for_timeout(300)
    print(" re@0.3:", snap(pg,"sl-area:cos-area",["t","running","reveal"]))
    pg.wait_for_timeout(1500)
    print(" re@1.8:", snap(pg,"sl-area:cos-area",["t","running","reveal"]))
    b.close()
