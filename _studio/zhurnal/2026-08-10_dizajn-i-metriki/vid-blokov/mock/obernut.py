#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""МАКЕТ, а не генератор: оборачивает уже собранный HTML деки в блоки.

Зачем это существует. Тип блока и центральность СЕГОДНЯ НЕ ДОЕЗЖАЮТ до HTML
(проверено грепом: `centralnyj_blok` — 0 вхождений в deck.py/tipy.py/slaid.py/
bloki.py; `render_section_markdown` склеивает тела подряд). Заход НИЧЕГО не
внедряет в `_generator/`, поэтому средства показать структуру негде примерить —
кроме как на КОПИИ собранного HTML, в своей папке. Этот файл и делает копию.

Что делает. Читает `baza/L2.html` (штатная сборка `sborka/deck.py`) и карточки
`teorkat-vvedenie/L2/slajdy/*/slaid.md` (READ-ONLY), режет плоский поток `<p>`
текстовой зоны на блоки и оборачивает каждый в

    <div class="blk" data-tip="opredelenie" data-central="1">
      <div class="blk-h"><span class="h-slovo">определение</span
       ><span class="h-mysl">двойственное пространство</span></div>
      …исходные <p> без единого изменения…
    </div>

Оба варианта тихого заголовка печатаются ВСЕГДА, выбор между ними — дело CSS
(`.h-slovo`/`.h-mysl`, ось 3b): так один макет обслуживает обе ветки развилки и
их можно сравнивать, не пересобирая.

🔴 ПОЧЕМУ РЕЗКЕ МОЖНО ВЕРИТЬ. `render_section_markdown` склеивает тела блоков
через пустую строку, поэтому верхнеуровневых элементов у блока ровно столько,
сколько в его теле кусков, разделённых пустой строкой. Это не предположение:
`--sverit` считает обе величины по всем карточкам и печатает расхождения;
на данных 2026-08-14 сходится на 21 карточке из 23, а две оставшиеся
(`razdelitel-*`) текстовой зоны `.zone.copy.t-body` не имеют вовсе — это
слайды-разделители, они и не должны нести блочных средств.

Что НЕ делает: ничего не пишет ни в `_generator/`, ни в `teorkat-vvedenie/`.
Вход только читается, выход кладётся рядом со скриптом.
"""
import argparse
import os
import re
import sys

KOREN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(KOREN, "_generator", "sborka"))
sys.path.insert(0, os.path.join(KOREN, "_generator"))
import bloki  # noqa: E402  (READ-ONLY импорт словаря блоков, как это делает formaty.py)

# слово-заголовок по типу. `narrativ` отсутствует НАМЕРЕННО (правило С1:
# нарратив не помечается ничем и никогда), `dokazatelstvo` — тоже (правило С5).
SLOVO = {
    "opredelenie": "определение",
    "utverzhdenie": "утверждение",
    "primer": "пример",
}
STATUSNYE = tuple(SLOVO)

ZONA_RE = re.compile(r'<div class="zone copy t-body"[^>]*>')


def _sloi(fragment, start):
    """конец парного </div> для тега, открытого перед `start`."""
    depth = 1
    for m in re.finditer(r"<div\b|</div>", fragment[start:]):
        depth += -1 if m.group(0) == "</div>" else 1
        if depth == 0:
            return start + m.start()
    return None


def _verhnie_elementy(inner):
    """[(имя, html)] — верхнеуровневые элементы текстовой зоны, в порядке потока."""
    out, depth, name, start = [], 0, None, 0
    for m in re.finditer(r"<(div|p|ul|ol)\b[^>]*>|</(div|p|ul|ol)>", inner):
        if m.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                out.append((name, inner[start:m.end()]))
        else:
            if depth == 0:
                name, start = m.group(1), m.start()
            depth += 1
    return out


def karta_kartochki(put):
    """slaid.md → (блоки раздела «Текст слайда», значение centralnyj_blok)."""
    raw = open(put, encoding="utf-8").read()
    telo = raw.split("---", 2)[2]
    c = re.search(r"^centralnyj_blok:\s*(.+)$", raw, re.M)
    secs = bloki.parse_sections(telo, os.path.basename(os.path.dirname(put)))
    return secs["tekst"], (c.group(1).strip() if c else None)


def _ekran(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def obernut_slajd(inner, blocks, central_mysl):
    """внутренность текстовой зоны → она же, но с блочными обёртками.

    Возвращает (html, диагностика|None). Диагностика непуста — резать нельзя,
    слайд остаётся как был: молчаливая порча кадра хуже отсутствия средства.
    """
    elems = _verhnie_elementy(inner)
    shapka = [e for e in elems if "zagolovok" in e[1][:70]]
    telo = [e for e in elems if "zagolovok" not in e[1][:70]]
    kuski = [len([c for c in re.split(r"\n\s*\n", b.telo.strip()) if c.strip()])
             for b in blocks]
    if sum(kuski) != len(telo):
        return inner, "элементов %d, кусков %d %s" % (len(telo), sum(kuski), kuski)

    # правило С4: линейка есть признак ЦЕНТРАЛЬНОГО и только его, но
    # «если блок на слайде один — линейки нет: выделять не от чего».
    odin = len(blocks) == 1
    # правило Ц4: доказательство центральным не бывает; Ц3: центральный нарратив
    # средств не получает (правило С1 сильнее).
    out, i = list(shapka), 0
    for b, n in zip(blocks, kuski):
        central = (b.mysl == central_mysl) and not odin and b.tip in STATUSNYE
        h = ""
        if b.tip in STATUSNYE:
            h = ('<div class="blk-h"><span class="h-slovo">%s</span>'
                 '<span class="h-mysl">%s</span></div>'
                 % (SLOVO[b.tip], _ekran(b.mysl)))
        out.append(('blk',
                    '<div class="blk" data-tip="%s" data-central="%d">%s%s</div>'
                    % (b.tip, 1 if central else 0, h,
                       "".join(e[1] for e in telo[i:i + n]))))
        i += n
    return "".join(e[1] for e in out), None


def peredelat(html, lekcia, tolko=None):
    """весь дек → дек с блочными обёртками. (html, [(слайд, диагностика)])."""
    bedy = []
    poz = 0
    novyj = []
    for m in re.finditer(r'<section class="slide" id="([^"]+)"[^>]*>', html):
        sid = m.group(1)
        kart = os.path.join(lekcia, "slajdy", sid, "slaid.md")
        konec = html.find('<section class="slide"', m.end())
        konec = konec if konec > 0 else len(html)
        frag = html[m.start():konec]
        zm = ZONA_RE.search(frag)
        if not os.path.exists(kart) or not zm:
            continue                      # служебные слайды и разделители — не наша забота
        if tolko and sid not in tolko:
            continue
        vnutri_ot = zm.end()
        vnutri_do = _sloi(frag, vnutri_ot)
        if vnutri_do is None:
            bedy.append((sid, "не нашёл конец текстовой зоны"))
            continue
        blocks, central = karta_kartochki(kart)
        novoe, beda = obernut_slajd(frag[vnutri_ot:vnutri_do], blocks, central)
        if beda:
            bedy.append((sid, beda))
            continue
        a = m.start() + vnutri_ot
        b = m.start() + vnutri_do
        novyj.append(html[poz:a]); novyj.append(novoe); poz = b
    novyj.append(html[poz:])
    return "".join(novyj), bedy


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--baza", required=True, help="собранный HTML деки (вход, только чтение)")
    p.add_argument("--lekcia", required=True, help="папка лекции с slajdy/ (только чтение)")
    p.add_argument("-o", "--out", required=True, help="куда положить обёрнутую копию")
    p.add_argument("--sverit", action="store_true",
                   help="только сверка резки по всем карточкам, без записи")
    a = p.parse_args()
    html = open(a.baza, encoding="utf-8").read()
    novyj, bedy = peredelat(html, a.lekcia)
    vsego = len(re.findall(r'<section class="slide" id="', html))
    obernuto = len(re.findall(r'<div class="blk" ', novyj))
    slajdov = len(set(re.findall(r'<section class="slide" id="([^"]+)"[^>]*>', novyj)))
    print("слайдов в деке: %d · блоков обёрнуто: %d · карточек не поддалось: %d"
          % (vsego, obernuto, len(bedy)))
    for sid, beda in bedy:
        print("   ⛔ %s: %s" % (sid, beda))
    if not a.sverit:
        open(a.out, "w", encoding="utf-8").write(novyj)
        print("записано: %s" % a.out)
    return 1 if bedy else 0


if __name__ == "__main__":
    sys.exit(main())
