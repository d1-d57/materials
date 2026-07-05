#!/usr/bin/env python3
"""Measure effective line spacing (CSS px) of the 4 side sims via live registry."""
import pathlib, sys
from playwright.sync_api import sync_playwright
HTML = pathlib.Path(__file__).resolve().parent.parent / "index.html"
TARGETS = [("sl-yellow","yellow",9,4),("sl-polygons","polygons",12,4),
           ("sl-circle","circle",13,4),("sl-result","result",14,3)]
tag = sys.argv[1] if len(sys.argv)>1 else "before"
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(viewport={"width":1440,"height":810}, device_scale_factor=2)
    pg.goto(f"file://{HTML}")
    pg.wait_for_timeout(500)
    for sid,kind,idx,sc in TARGETS:
        pg.evaluate(f"showSingle({idx},{sc})")
        pg.wait_for_timeout(1600)
        info = pg.evaluate("""(args)=>{const [sid,kind]=args;const id=sid+':'+kind;
          const e=window.LAB&&window.LAB[id];const cv=document.querySelector('#'+sid+' canvas[data-sim=\"'+kind+'\"]');
          const r=cv?cv.getBoundingClientRect():null;
          return e?{T:e.T,H:e.H,W:e.W,r:e.r||null,cssH:r?+r.height.toFixed(1):null,cssW:r?+r.width.toFixed(1):null,
                   nlines:Math.round(e.H/e.T),n:e.n,endless:!!(e.o&&e.o.endless)}:{err:'no reg '+id};}""",[sid,kind])
        # CSS-px spacing = T * (cssH / e.H); but e.H == cssH (clientHeight in CSS px) so spacing==T
        css_spacing = None
        if info.get('T') and info.get('H'):
            css_spacing = round(info['T'] * (info['cssH']/info['H']),1) if info.get('cssH') else info['T']
        print(f"{sid:12} T={info.get('T')!s:>7}  H={info.get('H')!s:>5}  cssH={info.get('cssH')!s:>6}  "
              f"lines={info.get('nlines')!s:>3}  CSSpx_spacing={css_spacing!s:>6}  r={info.get('r')}")
        pg.screenshot(path=str(pathlib.Path(__file__).parent/f"a3_{kind}_{tag}.png"))
    b.close()
