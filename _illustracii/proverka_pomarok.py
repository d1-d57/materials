#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверки иллюстраций из POMARKI-2026-08-09.md §3 (заход pomarki-slajd) —
нагружают верификатор, который включается при СОЗДАНИИ иллюстрации (см.
`fazy/ZAHOD.md §4`), а не гейт собранного слайда: дефекты рождаются в картинке,
и ловить их надо там же, до того как их одиннадцать штук уедут на слайды.

  П9.  Вопросительные знаки на иллюстрации — ЗАПРЕЩЕНЫ. Дословно владельца:
       «лишних подписей вот этих вопросительных знаков вообще не нужно,
       это запрещено просто».
  П12. Фон иллюстрации — прозрачный, не белый и не залитый.
  П10/П11. Равенство композиции не пишется подписью поверх стрелки — рисуется
       ДУГОЙ. Признак нарушения: <text> несёт одновременно '∘' и '=' — то есть
       уравнение записано текстом, а не изображено дугой с подписью-меткой.

И правило СК1 из DISCIPLINA.md §СТРЕЛКА (разбор владельца 2026-08-09):

  СК1. Наконечник строится ИЗ НАПРАВЛЕНИЯ ЛИНИИ. Ось наконечника — продолжение
       луча, треугольник равнобедренный (высота 9, основание 8), вершина на
       конце луча (или основание на конце — обе привязки законны). Ловится
       механически: ось отклонена больше чем на 5°, основание дальше 9,5 px от
       конца линии, боковые стороны разной длины.
       ⚠ СК2 (палочка «↦» между элементами) машиной НЕ проверяется вовсе:
       машина не знает, элементы на рисунке или объекты. Это глазу.

  python3 _illustracii/proverka_pomarok.py <file.svg|file.html> [ещё файлы...]
  exit 0 — зелёный (нарушений нет), 1 — красный (нарушение хотя бы в одном файле)
"""
import math
import re
import sys
from pathlib import Path

TEXT_RE = re.compile(r"<text\b[^>]*>(.*?)</text>", re.S)
INNER_TAG_RE = re.compile(r"<[^>]+>")
BG_FILL_RE = re.compile(r'fill\s*=\s*["\']?\s*(#fff(?:fff)?|white|var\(--card\))\s*["\']?', re.I)


def _text_contents(svg):
    return [INNER_TAG_RE.sub("", t) for t in TEXT_RE.findall(svg)]


def check_p9_voprositelnye(svg):
    return ["П9: <text> несёт «?» — вопросительные знаки на иллюстрации запрещены: %r" % t
            for t in _text_contents(svg) if "?" in t]


def check_p12_fon(svg):
    m = BG_FILL_RE.search(svg)
    if m:
        return ["П12: заливка фона (%s) — фон обязан быть прозрачным, не белым и не залитым"
                % m.group(1)]
    return []


def check_p10_p11_podpis_nad_strelkoj(svg):
    return ["П10/П11: <text> несёт равенство композиции текстом (%r) — рисуется ДУГОЙ, не "
            "подписью поверх стрелки" % t
            for t in _text_contents(svg) if "∘" in t and "=" in t]


# ─────────────────────────── СК1: геометрия наконечника ────────────────────────────
# Канон (DISCIPLINA.md §СТРЕЛКА): равнобедренный треугольник, высота 9, основание 8,
# ось — продолжение линии, вершина (или основание) на конце луча. Пропорция важнее
# абсолютного размера: рисунок могут собрать в другом масштабе.

CANON_H, CANON_BASE = 9.0, 8.0
DOP_PROPORCIYA = 0.04    # отклонение base/h от канонных 8/9
DOP_RAVNOBEDR = 0.03     # разница боковых сторон
DOP_UGOL = 5.0           # градусов между осью наконечника и направлением линии
DOP_PRIVYAZKA = 9.5      # px от конца линии до середины основания
DOP_VYSOTA = (5.0, 20.0)  # осмысленный диапазон высоты
DOP_POISK = 26.0         # дальше этого линии-хозяина считаем, что не нашли

TAG_RE = re.compile(r"<(line|path)\b([^>]*?)/?>", re.S)
ATTR_RE = re.compile(r'([\w:.-]+)\s*=\s*"([^"]*)"')
TOK_RE = re.compile(r"[MmLlHhVvCcSsQqTtAaZz]|-?\d*\.?\d+(?:[eE]-?\d+)?")


def _hypot(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])


def _path_points(d):
    """Грубый разбор d= в список ('L'|'C'|'A', конечная_точка, [опора]).
    Возвращает None, если разбор не удался — вызывающий обязан назвать это
    слепой зоной, а не считать зелёным."""
    toks = TOK_RE.findall(d)
    pts, cur, start, i, cmd = [], (0.0, 0.0), None, 0, None
    try:
        while i < len(toks):
            t = toks[i]
            if t.isalpha():
                cmd, i = t, i + 1
                continue
            if cmd is None:
                return None
            rel, C = cmd.islower(), cmd.upper()
            need = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7}.get(C)
            if need is None:
                return None
            v = [float(x) for x in toks[i:i + need]]
            if len(v) < need:
                return None
            i += need
            if C == "M":
                cur = (cur[0] + v[0], cur[1] + v[1]) if rel else (v[0], v[1])
                start = cur
                pts.append(("M", cur, None))
                cmd = "l" if rel else "L"
            elif C in ("L", "T"):
                cur = (cur[0] + v[0], cur[1] + v[1]) if rel else (v[0], v[1])
                pts.append(("L", cur, None))
            elif C == "H":
                cur = (cur[0] + v[0], cur[1]) if rel else (v[0], cur[1])
                pts.append(("L", cur, None))
            elif C == "V":
                cur = (cur[0], cur[1] + v[0]) if rel else (cur[0], v[0])
                pts.append(("L", cur, None))
            elif C in ("C", "S", "Q"):
                pairs = [(v[k], v[k + 1]) for k in range(0, need, 2)]
                abspairs = [(cur[0] + p[0], cur[1] + p[1]) if rel else p for p in pairs]
                pts.append(("C", abspairs[-1], abspairs[-2]))
                cur = abspairs[-1]
            elif C == "A":
                end = (cur[0] + v[5], cur[1] + v[6]) if rel else (v[5], v[6])
                pts.append(("A", end, cur))
                cur = end
            if i < len(toks) and toks[i] in "Zz":
                pts.append(("Z", start or cur, None))
                cur = start or cur
                i += 1
    except ValueError:
        return None
    return pts or None


def _treugolnik(d):
    pts = _path_points(d)
    if not pts:
        return None
    verts = []
    for kind, p, _ in pts:
        if kind in ("M", "L") and (not verts or _hypot(p, verts[-1]) > 1e-9):
            verts.append(p)
    return verts[:3] if len(verts) >= 3 else None


def _os_nakonechnika(tri):
    """Вершина треугольника — та, от которой боковые стороны равны и высота максимальна."""
    best = None
    for k in range(3):
        apex, a, b = tri[k], tri[(k + 1) % 3], tri[(k + 2) % 3]
        s1, s2 = _hypot(apex, a), _hypot(apex, b)
        iso = abs(s1 - s2) / max(1e-9, (s1 + s2) / 2)
        mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        h = _hypot(apex, mid)
        score = iso - 0.02 * h
        if best is None or score < best[0]:
            best = (score, apex, mid, h, _hypot(a, b), iso)
    _, apex, mid, h, base, iso = best
    return apex, mid, h, base, iso


def _koncy(svg):
    """Все концы линий и кривых: (точка, единичное направление ВХОДА в этот конец)."""
    out = []
    for m in TAG_RE.finditer(svg):
        tag, raw = m.group(1), m.group(2)
        a = dict(ATTR_RE.findall(raw))
        if tag == "line":
            try:
                p1 = (float(a["x1"]), float(a["y1"]))
                p2 = (float(a["x2"]), float(a["y2"]))
            except (KeyError, ValueError):
                continue
            L = _hypot(p1, p2)
            if L < 1e-9:
                continue
            u = ((p2[0] - p1[0]) / L, (p2[1] - p1[1]) / L)
            out.append((p2, u))
            out.append((p1, (-u[0], -u[1])))
            continue
        if "s-ar-" in a.get("class", ""):
            continue                      # сам наконечник хозяином не бывает
        pts = _path_points(a.get("d", ""))
        if not pts:
            continue
        tail = [p for p in pts if p[0] != "Z"]
        if len(tail) < 2:
            continue
        kind, end, opora = tail[-1]
        if kind in ("C", "A") and opora:
            v = (end[0] - opora[0], end[1] - opora[1])
        else:
            v = (end[0] - tail[-2][1][0], end[1] - tail[-2][1][1])
        L = math.hypot(*v)
        if L > 1e-9:
            out.append((end, (v[0] / L, v[1] / L)))
        first, nxt = tail[0][1], tail[1][1]
        v = (first[0] - nxt[0], first[1] - nxt[1])
        L = math.hypot(*v)
        if L > 1e-9:
            out.append((first, (v[0] / L, v[1] / L)))
    return out


def check_sk1_nakonechnik(svg):
    """СК1: наконечник строится из направления линии (DISCIPLINA.md §СТРЕЛКА)."""
    koncy = _koncy(svg)
    issues = []
    for m in TAG_RE.finditer(svg):
        if m.group(1) != "path":
            continue
        a = dict(ATTR_RE.findall(m.group(2)))
        if "s-ar-" not in a.get("class", ""):
            continue
        d = a.get("d", "")
        tri = _treugolnik(d)
        if not tri:
            issues.append("СК1 (СЛЕПАЯ ЗОНА): наконечник %r не разобран как треугольник — "
                          "проверить глазом" % d[:60])
            continue
        apex, mid, h, base, iso = _os_nakonechnika(tri)
        if not koncy:
            issues.append("СК1 (СЛЕПАЯ ЗОНА): наконечник %r есть, а линий в файле нет" % d[:60])
            continue
        p, u = min(koncy, key=lambda e: min(_hypot(e[0], apex), _hypot(e[0], mid)))
        if min(_hypot(p, apex), _hypot(p, mid)) > DOP_POISK:
            issues.append("СК1 (СЛЕПАЯ ЗОНА): наконечнику %r не нашлось линии ближе %.0f px — "
                          "проверить глазом" % (d[:60], DOP_POISK))
            continue
        os_ = (apex[0] - mid[0], apex[1] - mid[1])
        L = math.hypot(*os_) or 1e-9
        os_ = (os_[0] / L, os_[1] / L)
        ugol = math.degrees(math.acos(max(-1.0, min(1.0, os_[0] * u[0] + os_[1] * u[1]))))
        prop = base / h if h > 1e-9 else 0.0
        bad = []
        if ugol > DOP_UGOL:
            bad.append("ось отклонена от линии на %.1f° (можно %.0f°)" % (ugol, DOP_UGOL))
        if iso > DOP_RAVNOBEDR:
            bad.append("треугольник не равнобедренный (боковые расходятся на %.0f%%)" % (iso * 100))
        if abs(prop - CANON_BASE / CANON_H) > DOP_PROPORCIYA:
            bad.append("пропорция основание/высота %.2f вместо %.2f" % (prop, CANON_BASE / CANON_H))
        if not (DOP_VYSOTA[0] <= h <= DOP_VYSOTA[1]):
            bad.append("высота %.1f вне диапазона %.0f–%.0f" % (h, *DOP_VYSOTA))
        if _hypot(p, mid) > DOP_PRIVYAZKA:
            bad.append("основание в %.1f px от конца линии (можно %.1f) — наконечник не на конце"
                       % (_hypot(p, mid), DOP_PRIVYAZKA))
        if bad:
            issues.append("СК1: наконечник %r — %s. Строить по формуле из DISCIPLINA.md §СТРЕЛКА"
                          % (d[:60], "; ".join(bad)))
    return issues


CHECKS = (check_p9_voprositelnye, check_p12_fon, check_p10_p11_podpis_nad_strelkoj,
          check_sk1_nakonechnik)


def check_file(path):
    svg = Path(path).read_text(encoding="utf-8")
    issues = []
    for c in CHECKS:
        issues.extend(c(svg))
    return issues


def main():
    if len(sys.argv) < 2:
        print("использование: proverka_pomarok.py <file.svg|file.html> [ещё файлы...]")
        return 2
    all_issues = []
    for f in sys.argv[1:]:
        issues = check_file(f)
        if issues:
            print("КРАСНЫЙ — %s:" % f)
            for i in issues:
                print("  ✗ %s" % i)
        else:
            print("ЗЕЛЁНЫЙ — %s" % f)
        all_issues.extend(issues)
    return 1 if all_issues else 0


if __name__ == "__main__":
    sys.exit(main())
