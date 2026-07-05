#!/usr/bin/env python3
"""Probe the 3 null/missing sims: dump their actual object fields + canvas pixel non-blankness."""
import pathlib, json
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
HTML = HERE.parent / "index.html"

PROBE = """(arg) => {
  const [key, idx, scene] = arg;
  const e = (window.LAB||{})[key];
  const out = {key, present: !!e};
  if (e) {
    out.keys = Object.keys(e);
    const flat = {};
    for (const k of Object.keys(e)) {
      const v = e[k];
      const t = typeof v;
      if (v===null||['number','boolean','string'].includes(t)) flat[k]=v;
      else flat[k]='['+t+']';
    }
    out.flat = flat;
    if (e.o) out.o = Object.fromEntries(Object.entries(e.o).filter(([k,v])=>['number','boolean','string'].includes(typeof v)));
  }
  // canvas non-blank check for the slide
  const slide = document.getElementById(key.split(':')[0]);
  out.canvases = [];
  if (slide) slide.querySelectorAll('canvas[data-sim]').forEach(cv=>{
    let painted=false, w=cv.width, h=cv.height;
    try {
      const ctx=cv.getContext('2d');
      const d=ctx.getImageData(0,0,w,h).data;
      let nonzero=0;
      for(let i=3;i<d.length;i+=4*997){ if(d[i]!==0){nonzero++;} }
      painted = nonzero>0;
    } catch(err){ painted='err:'+err.message; }
    out.canvases.push({sim:cv.dataset.sim, w, h, painted});
  });
  return out;
}"""

TARGETS = [
    ("sl-coords:coords-needles", 17, 2),
    ("sl-coords:coords-phase",   17, 2),
    ("sl-area:cos-area",         20, 5),
]
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(viewport={"width":1440,"height":810}, device_scale_factor=2)
    pg.goto(f"file://{HTML}"); pg.wait_for_timeout(700)
    for key, idx, scene in TARGETS:
        pg.evaluate("showSingle(0,1)"); pg.wait_for_timeout(400)
        pg.evaluate(f"showSingle({idx},{scene})"); pg.wait_for_timeout(1800)
        print(json.dumps(pg.evaluate(PROBE, [key, idx, scene]), indent=1, ensure_ascii=False))
        print("---")
    b.close()
