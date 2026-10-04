#!/usr/bin/env python3
"""Сборка занятия Миши: content-модуль (python, словарь LESSON) + engine.js/.css -> один html.
Запуск: python3 build.py <content.py> <out.html>"""
import sys, json, runpy, pathlib
H = pathlib.Path(__file__).parent
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;500;600;700&family=Rubik:wght@600;700&display=swap">'

def euler(sets, points, w=620, h=380):
    """sets: [(cx,cy,rx,ry,label,lx,ly)], points: [(text,x,y)] — диаграмма Эйлера–Венна."""
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img">']
    for cx, cy, rx, ry, lab, lx, ly in sets:
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#18202e" stroke-width="3"/>')
        o.append(f'<text x="{lx}" y="{ly}" font-size="34" font-style="italic" font-family="Golos Text,sans-serif" fill="#2f5fd0">{lab}</text>')
    for t, x, y in points:
        o.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#18202e"/><text x="{x+10}" y="{y+10}" font-size="30" font-family="Golos Text,sans-serif">{t}</text>')
    o.append('</svg>')
    return ''.join(o)

def build(content, out):
    L = runpy.run_path(content)['LESSON']
    css = (H / 'engine.css').read_text(); js = (H / 'engine.js').read_text()
    html = (f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{L["title"]}</title>{FONTS}<style>{css}</style></head><body>'
            f'<script>window.LESSON={json.dumps(L, ensure_ascii=False)};</script><script>{js}</script></body></html>')
    pathlib.Path(out).write_text(html)
    n = sum(1 for s in L['sections'] for it in s['items'] if it.get('type') != 'cover')
    print(f'{out}: разделов {len(L["sections"])}, задач {n}')

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])
