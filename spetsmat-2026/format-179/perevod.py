#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Наш .tex листка → тело листка в формате школы 179 (Overleaf, macros.tex).

    python3 perevod.py НАШ.tex ИХ.tex

Что делает. Берёт тело нашего листка (между \\begin{document} и
\\end{document}) и переписывает его командами их стиля: \\ListokName,
\\shapkaUstnoA, \\zp, \\z, \\lett. Преамбулы в результате нет: её даёт их
мастер-файл. Словарь команд и то, что в нём выведено, а что угадано, — в
SLOVAR.md рядом.

Обратный перевод (их → наш) пока не написан.
"""
import re
import sys
from pathlib import Path


def chitat_skobki(s, i):
    """s[i] == '{'. Вернуть (содержимое, индекс после закрывающей)."""
    assert s[i] == "{", s[i:i + 30]
    glub = 0
    for j in range(i, len(s)):
        c = s[j]
        if c == "\\":
            continue
        if c == "{" and (j == 0 or s[j - 1] != "\\"):
            glub += 1
        elif c == "}" and s[j - 1] != "\\":
            glub -= 1
            if glub == 0:
                return s[i + 1:j], j + 1
    raise ValueError("незакрытая скобка: " + s[i:i + 60])


def argumenty(s, i, n):
    out = []
    for _ in range(n):
        while s[i] in " \n":
            i += 1
        a, i = chitat_skobki(s, i)
        out.append(a)
    return out, i


# Порог «пункты короткие»: самый длинный пункт не длиннее стольких символов.
KOROTKO = 50


def tekst(t):
    """Наша разметка внутри текста → совместимая с любым стилем."""
    t = t.replace(r"\term{", r"\textit{")
    t = t.replace(r"\geqslant", r"\ge").replace(r"\leqslant", r"\le")
    t = t.replace(r"\varnothing", r"\emptyset")
    return t.strip()


def marker(m):
    """◦ † ⋆ у них командой не выражены (в образце 17 их нет) — ставим
    надстрочным знаком сразу после номера, как у нас."""
    # \\unskip снимает пробел, который их \\zp / \\lett ставят после номера или
    # буквы, — знак прилипает к номеру, как у нас.
    return "\\unskip$^{%s}$\\ " % m if m else ""


def perevesti(nash):
    telo = nash.split(r"\begin{document}", 1)[1].split(r"\end{document}", 1)[0]
    # Уровень берётся из заголовка нашего листка: 18$\alpha$ или 18$\aleph$
    # (А пишет Стрелкова в своём формате, нам его переводить не нужно).
    zagolovok = re.search(r"\\textbf\{(\d+)\$\\(alpha|aleph)\$\. \\textsc\{([^}]*)\}\}", telo)
    if not zagolovok:
        # Шапка по стандарту коллег: {\LARGE$\aleph$} справа, в заголовке только номер (18ℵ v10, 01.10)
        z2 = re.search(r"\{\\LARGE\$\\(alpha|aleph)\$\}.*?\\textbf\{(\d+)\. \\textsc\{([^}]*)\}\}", telo, re.S)
        if z2:
            class _Z:
                def __init__(s, m): s.m = m
                def group(s, i): return {1: s.m.group(2), 2: s.m.group(1), 3: s.m.group(3)}[i]
                def end(s): return s.m.end()
            zagolovok = _Z(z2)
    if not zagolovok:
        sys.exit("не нашёл заголовок вида \\textbf{18$\\alpha$. \\textsc{Имя}} (или \\aleph)")
    nomer, uroven, imya = zagolovok.group(1), zagolovok.group(2), zagolovok.group(3)
    out = []
    if r"\begin{tikzpicture}" in telo:
        out += [r"% В листке есть картинки TikZ: в преамбуле нужен \usepackage{tikz}.", ""]
    # Поле «Фамилия, имя» на третьей странице (владелец, 01.10: 4 страницы печатают на двух листах).
    # Переносим, только если оно есть в нашем листке, — перевод двухстраничных листков не меняется.
    m_fam = re.search(r"^\\AddToHook\{shipout/foreground\}.*Фамилия, имя.*$", nash, re.M)
    if m_fam:
        out += [r"% Поле для подписи вверху третьей страницы (нужен LaTeX 2020 или новее; в Overleaf есть).", m_fam.group(0), ""]
    out += [
        r"\providecommand{\divby}{\par\smallskip\noindent\hrulefill\par\smallskip} % разделитель частей; если в стиле он есть, возьмётся стилевой",
        "",
        r"\ListokName{%s. %s}" % (nomer, imya),
        "",
        # Шапки уровня α в их стиле мы не видели (\shapkaUstnoA печатает «A»,
        # \shapkaUstno — без буквы), поэтому шапка набрана обычным LaTeX
        # по образцу 17А, с буквой уровня (α или ℵ) справа.
        r"% Шапка: набрана вручную, потому что команды шапки для уровней α и ℵ нам неизвестны.",
        r"% Если в стиле есть своя (как \shapkaUstnoA для уровня А), замените ею эти три строки.",
        r"\noindent\rlap{\makebox[\linewidth]{\itshape 2026/2027. Школа 179. КЛ 25-29}}\hfill{\LARGE$\%s$}\par\medskip" % uroven,
        r"\centerline{\rule{0.62\linewidth}{0.4pt}}\par\smallskip",
        r"\centerline{\large\bfseries\scshape %s. %s}\par\medskip" % (nomer, imya),
        "",
    ]
    # Всё до заголовка включительно — наша шапка, у них её делает стиль.
    # (Раньше тело начиналось с первого \tekst: листок, открывающийся задачей, терял её — 18ℵ, 30.09.)
    i = zagolovok.end()
    out += perevesti_kuski(telo, i)
    return "\n".join(out).rstrip() + "\n"


NERAZRYV_NACH = r"\par\noindent\begin{minipage}{\linewidth}"
NERAZRYV_KON = r"\end{minipage}\par\vspace{6pt}"
RISUNOK = r"\par\medskip\centerline{%s}\par\smallskip"
# Текст и картинка рядом — две minipage (стандартный LaTeX, от стиля не зависит).
RYADOM_NACH = r"\par\noindent\begin{minipage}[t]{\dimexpr\linewidth-%s-1.2em\relax}\vspace{0pt}"
RYADOM_KON = r"\end{minipage}\hfill\begin{minipage}[t]{%s}\vspace{0pt}\centering %s\end{minipage}\par\vspace{6pt}"


def perevesti_kuski(s, i=0):
    """Кусок нашего тела → строки их формата: \\tekst, \\zad, samepage-блоки, \\zvezdy, \\sboku."""
    out = []
    while i < len(s):
        if s.startswith(r"\tekst{", i):
            (a,), i = argumenty(s, i + len(r"\tekst"), 1)
            out += [tekst(a), ""]
        elif s.startswith(r"\zad{", i):
            (n, m, a), i = argumenty(s, i + len(r"\zad"), 3)
            out += [r"\zp %s%s" % (marker(m), tekst(a)), ""]
        elif s.startswith(r"\begin{samepage}", i):
            konec = s.index(r"\end{samepage}", i)
            blok = s[i + len(r"\begin{samepage}"):konec]
            jz = blok.find(r"\zadp{")
            if jz >= 0 and (blok.find(r"\blok{") < 0 or jz < blok.find(r"\blok{")):
                # \zadp{n}{маркер}: задача без общего условия — номер и сразу пункт а).
                (n, m), j = argumenty(blok, jz + len(r"\zadp"), 2)
                uslovie = ""
            else:
                j = blok.index(r"\blok{")
                (golova,), j = argumenty(blok, j + len(r"\blok"), 1)
                k = golova.index(r"\nomer{")
                (n, m), k = argumenty(golova, k + len(r"\nomer"), 2)
                uslovie = golova[k:].replace(r"\hspace{\zazor}", "", 1)
            punkty = []
            while True:
                p = blok.find(r"\punkt{", j)
                if p < 0:
                    break
                (bukva, pm, pt), j = argumenty(blok, p + len(r"\punkt"), 3)
                punkty.append((pm, tekst(pt)))
            # Короткие пункты — в строку (\leth), как задача 8 в листке 17А:
            # окно у каждого пункта остаётся, клеток столько же, строк меньше.
            hvost = blok[j:].strip()  # то, что стоит после последнего \punkt (например, картинка)
            v_stroku = max(len(t) for _, t in punkty) <= KOROTKO and not hvost
            komanda = r"\leth" if v_stroku else r"\lett"
            mk = marker(m) if uslovie.strip() else marker(m).rstrip("\\ ")
            stroki = [r"\z %s%s" % (mk, tekst(uslovie))]
            stroki += [r"%s %s%s" % (komanda, marker(pm), t) for pm, t in punkty]
            out += [("\n" if not v_stroku else " ").join(stroki), ""]
            if hvost:
                out += [hvost.replace(r"\par\nopagebreak\smallskip\nopagebreak", r"\par\smallskip"), ""]
            i = konec + len(r"\end{samepage}")
        elif s.startswith(r"\zvezdy", i):
            out += [r"\divby", ""]
            i += len(r"\zvezdy")
        elif s.startswith(r"\sboku{", i):
            # Текст и картинка рядом: у коллег так же, двумя minipage.
            (shir, kartinka, tekst_bloka), i = argumenty(s, i + len(r"\sboku"), 3)
            out += [RYADOM_NACH % shir] + perevesti_kuski(tekst_bloka) + [RYADOM_KON % (shir, kartinka.strip()), ""]
        elif s.startswith(r"\celoe{", i):
            # Неразрывный блок: задача вместе с картинкой переносится целиком.
            (blok_celoe,), i = argumenty(s, i + len(r"\celoe"), 1)
            out += [NERAZRYV_NACH] + perevesti_kuski(blok_celoe) + [NERAZRYV_KON, ""]
        elif s.startswith(r"\risunok{", i):
            (kartinka,), i = argumenty(s, i + len(r"\risunok"), 1)
            out += [RISUNOK % kartinka.strip(), ""]
        elif s.startswith(r"\obtek", i):
            # Обтекание (wrapfig) у нас. У коллег их \z может оказаться списком, где wrapfig ломается,
            # поэтому картинка встаёт под следующий блок, и оба — неразрывно.
            j = i + len(r"\obtek")
            if s[j] == "[":
                j = s.index("]", j) + 1
            (shir, kartinka), i = argumenty(s, j, 2)
            sled = []
            k = i
            while k < len(s) and s[k] in " \n":
                k += 1
            if s.startswith(r"\begin{samepage}", k):
                konec = s.index(r"\end{samepage}", k) + len(r"\end{samepage}")
                sled = perevesti_kuski(s[k:konec]); i = konec
            out += [RYADOM_NACH % shir] + sled + [RYADOM_KON % (shir, kartinka.strip()), ""]
        else:
            i += 1
    return out


if __name__ == "__main__":
    vhod, vyhod = Path(sys.argv[1]), Path(sys.argv[2])
    rez = perevesti(vhod.read_text(encoding="utf-8"))
    vyhod.write_text(rez, encoding="utf-8")
    print("задач: %d (\\zp %d, \\z %d) → %s" % (
        rez.count("\\zp ") + rez.count("\\z "), rez.count("\\zp "),
        rez.count("\\z "), vyhod.name))
