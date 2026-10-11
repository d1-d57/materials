import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    for n in sys.argv[1:]:
        pg.goto('file:///tmp/claude-0/k2/out/'+n+'.html'); pg.wait_for_timeout(300)
        pg.pdf(path='out/'+n+'.pdf',format='A4',print_background=True,prefer_css_page_size=True)
    b.close()
