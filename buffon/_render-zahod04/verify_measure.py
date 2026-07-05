import pathlib
from playwright.sync_api import sync_playwright
HTML = pathlib.Path(__file__).resolve().parent.parent / "index.html"
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(viewport={"width":1440,"height":810}, device_scale_factor=2)
    pg.goto(f"file://{HTML}")
    pg.wait_for_timeout(600)
    # activate the four A3 sims
    for idx,sc in [(9,4),(12,4),(13,4),(14,3)]:
        pg.evaluate(f"showSingle({idx},{sc})")
        pg.wait_for_timeout(1200)
    res = pg.evaluate("""() => {
      const out={};
      for (const k of Object.keys(window.LAB||{})){
        const v=window.LAB[k];
        if(v && typeof v.T!=='undefined') out[k]=v.T;
      }
      return out;
    }""")
    print("T values:", res)
    # A6 button bounds on sl-result
    pg.evaluate("showSingle(14,3)")
    pg.wait_for_timeout(1500)
    geo = pg.evaluate("""() => {
      const row=document.querySelector('#sl-result .lab-row');
      const panel=document.querySelector('#sl-result .p-contours');
      if(!row||!panel) return {row:!!row, panel:!!panel};
      const r=row.getBoundingClientRect(), pa=panel.getBoundingClientRect();
      return {row_right:r.right, panel_right:pa.right, row_bottom:r.bottom, panel_bottom:pa.bottom, inside: (r.right<=pa.right && r.bottom<=pa.bottom)};
    }""")
    print("A6 geo:", geo)
    b.close()
