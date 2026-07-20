#!/usr/bin/env python3
"""Генератор: content.md (+ KaTeX) -> index.html.

Выход index.html руками НЕ править — правь content.md / shablon.html и пересобирай:
    python3 build.py
"""
import re, pathlib, html

HERE = pathlib.Path(__file__).parent
src = (HERE / "content.md").read_text(encoding="utf-8")
tpl = (HERE / "shablon.html").read_text(encoding="utf-8")

# --- защита формул от markdown-разметки -------------------------------------
_math = []
def _stash(m):
    _math.append(m.group(0))
    return f"\x00M{len(_math) - 1}\x00"

def protect(t):
    t = re.sub(r"\$\$.+?\$\$", _stash, t, flags=re.S)   # display
    t = re.sub(r"\$.+?\$", _stash, t, flags=re.S)        # inline
    return t

def unstash(t):
    # экранируем &,<,> внутри LaTeX: textContent вернёт их обратно для KaTeX
    return re.sub(r"\x00M(\d+)\x00",
                  lambda m: html.escape(_math[int(m.group(1))], quote=False), t)

def inline(t):
    t = protect(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return unstash(t)

# --- разбор по блокам --------------------------------------------------------
out = []
for block in re.split(r"\n[ \t]*\n", src.strip()):
    b = block.strip("\n")
    if not b.strip():
        continue
    s = b.lstrip()
    if s.startswith("<"):                       # сырой HTML (SVG/figure)
        out.append(b); continue
    if b.strip() == "---":
        out.append('<hr class="rule">'); continue
    if s.startswith("$$"):                       # блочная формула
        out.append(f'<div class="mathblock">{html.escape(b.strip(), quote=False)}</div>'); continue
    lines = b.split("\n")
    if lines[0].startswith("### "):
        out.append(f"<h3>{inline(lines[0][4:])}</h3>"); continue
    if lines[0].startswith("## "):
        out.append(f"<h2>{inline(lines[0][3:])}</h2>"); continue
    if lines[0].startswith("# "):
        out.append(f"<h1>{inline(lines[0][2:])}</h1>"); continue
    if all(l.startswith(">") for l in lines):    # callout
        inner = " ".join(l[1:].strip() for l in lines)
        out.append(f'<blockquote class="callout">{inline(inner)}</blockquote>'); continue
    if all(l.startswith("- ") for l in lines):   # список
        items = "".join(f"<li>{inline(l[2:])}</li>" for l in lines)
        out.append(f"<ul>{items}</ul>"); continue
    joined = " ".join(lines)
    if joined.startswith("*") and not joined.startswith("**") and joined.rstrip().endswith("*"):
        out.append(f'<p class="lead">{inline(joined.strip()[1:-1])}</p>'); continue
    out.append(f"<p>{inline(joined)}</p>")

body = "\n".join(out)
result = tpl.replace("{{BODY}}", body).replace("{{TITLE}}", "Индекс подфактора Джонса — с нуля")
(HERE / "index.html").write_text(result, encoding="utf-8")
print(f"OK -> index.html ({len(result)} bytes, {len(_math)} формул, {len(out)} блоков)")
