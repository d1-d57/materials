#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сборщик кэша формул: из готовой колоды достаёт каждый <span class="katex">…</span>
и его TeX-исходник (из <annotation encoding="application/x-tex">), строит карту
{tex: rendered_html} и пишет её в JSON. Так текст слайда хранит формулу как $tex$,
а генератор подставляет ГОТОВЫЙ рендер из кэша — без запуска KaTeX (stdlib).

  python3 harvest_katex.py <deck.html> <out.json>

Работает для УЖЕ отрендеренных формул (round-trip существующей колоды). Новые
формулы (которых нет в колоде) — задача будущего «math-арка» с настоящим KaTeX.
"""
import re, json, sys, html as html_mod
from pathlib import Path

KATEX_OPEN = '<span class="katex">'


def balanced_span(s, start):
    """Вернуть подстроку сбалансированного <span>…</span>, начиная с индекса открытия."""
    depth, k = 0, start
    while k < len(s):
        nt, ct = s.find("<span", k), s.find("</span>", k)
        if ct < 0:
            return s[start:]
        if nt != -1 and nt < ct:
            depth += 1
            k = nt + 5
        else:
            depth -= 1
            k = ct + 7
            if depth == 0:
                return s[start:k]
    return s[start:k]


def harvest(html):
    cache, i = {}, 0
    while True:
        j = html.find(KATEX_OPEN, i)
        if j < 0:
            break
        block = balanced_span(html, j)
        m = re.search(r'<annotation encoding="application/x-tex">(.*?)</annotation>', block, re.S)
        if m:
            tex = html_mod.unescape(m.group(1))       # ключ = TeX, как его пишут в $…$
            if tex in cache and cache[tex] != block:
                # один и тот же TeX всегда рендерится одинаково; расхождение — сигнал
                sys.stderr.write("⚠ разный HTML для одного TeX: %r\n" % tex)
            cache[tex] = block
        i = j + len(KATEX_OPEN)
    return cache


def main():
    if len(sys.argv) != 3:
        print(__doc__); return 1
    html = Path(sys.argv[1]).read_text(encoding="utf-8")
    cache = harvest(html)
    out = Path(sys.argv[2])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(cache, ensure_ascii=False, indent=0), encoding="utf-8")
    print("формул уникальных: %d → %s" % (len(cache), out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
