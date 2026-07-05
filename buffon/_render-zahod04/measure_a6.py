import pathlib
from playwright.sync_api import sync_playwright
HTML = pathlib.Path(__file__).resolve().parent.parent / "index.html"
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(viewport={"width":1440,"height":810}, device_scale_factor=2)
    pg.goto(f"file://{HTML}?only=14&scene=3")
    pg.wait_for_timeout(2000)
    info = pg.evaluate("""() => {
      const lab = document.querySelector('#sl-result .lab-row');
      const pan = document.querySelector('#sl-result .p-contours');
      const r = e => e ? (()=>{const b=e.getBoundingClientRect();return {x:b.x,y:b.y,w:b.width,h:b.height,right:b.right,bottom:b.bottom}})() : null;
      return {
        lab: r(lab),
        panel: r(pan),
        labOffsetParent: lab ? (lab.offsetParent ? lab.offsetParent.id + '.' + lab.offsetParent.className : 'NULL') : 'NO-LAB',
        labHTML: lab ? lab.outerHTML.slice(0,200) : null,
        labStyleRight: lab ? getComputedStyle(lab).right : null,
        labStyleBottom: lab ? getComputedStyle(lab).bottom : null,
        labStyleTransform: lab ? getComputedStyle(lab).transform : null,
        labStyleLeft: lab ? getComputedStyle(lab).left : null,
      };
    }""")
    import json; print(json.dumps(info, indent=2))
    b.close()
