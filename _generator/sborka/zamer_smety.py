#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TOOL-CONTRACT: called-by-hand — снимает константы для `smeta.py`. Зовётся
# ОСОЗНАННО при перекалибровке (смена шрифта, padding'ов, холста), а не на
# каждой сборке: держит браузер и меряет весь корпус.
"""Замерщик исходных чисел сметы вмещения (Э2.1 + Э2.2 захода svedenie-i-smeta).

🔴 ЗАЧЕМ ОТДЕЛЬНЫЙ ФАЙЛ, а не число в `smeta.py`. Заход дословно: «формулу НЕ
ПРИДУМЫВАЮТ, её КАЛИБРУЮТ по тому же браузеру, которым меряет солвер», и
«каждая константа снимается замером и записывается ВМЕСТЕ с командой, которая
её сняла» (`KONSTITUCIYA §10`). Константа без живой команды рядом — то же
вписанное руками число, из-за которого весь заход и случился. Этот файл И ЕСТЬ
та команда: `smeta.py` цитирует его вывод, а не хранит независимое знание.

Второго замерщика тут не заводится: геометрия зоны снимается `vmeshchenie.izmerit()`
(Я1) — тем же `page.evaluate`, которым меряет солвер. Шрифтовые константы снимаются
в том же браузере, на тех же скомпилированных слайдах.

  python3 _generator/sborka/zamer_smety.py --geometriya          # Э2.1: W и H зоны по типам × liniya
  python3 _generator/sborka/zamer_smety.py --konstanty <лекция>  # Э2.2: k_znak, h_formula, k_inline
  python3 _generator/sborka/zamer_smety.py --vse <лекция>        # и то, и другое
"""
import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

SBORKA = Path(__file__).resolve().parent
sys.path.insert(0, str(SBORKA))

import vmeshchenie  # noqa: E402
from slaid import compile_slide_html  # noqa: E402

VIEWPORT = {"width": 1440, "height": 810}

# Сетка `liniya`, на которой снимается геометрия. Границы — из жёстких зон Я1
# (`build_zones`), не выдуманы здесь: солвер за них не выходит, значит и мерить
# снаружи нечего.
LINIYA_STEPS = (15, 25, 35, 45, 55, 65, 75, 85, 92)

# Типы вёрстки с текстовой зоной, которые смета обязана уметь. `polnyj_ekran`
# с иллюстрациями текстовой зоны не имеет вовсе (`tipy.py`), `oblozhka`/`vizitka`/
# `finalnyj`/`razdelitel` — служебные без корпусного текста.
TIPY_S_TEKSTOM = ("polosa_gorizontalnaya", "polosa_vertikalnaya", "tolko_tekst")

# Синтетическая карточка для замера ГЕОМЕТРИИ: текст нужен только чтобы зона
# существовала и была непустой; ни одно число сметы из его содержания не берётся.
KARTOCHKA = """---
imya: %(sid)s
nazvanie: Замер
zagolovok_na_ekrane: %(zagolovok)s
tip_slaida: Т4
zachem: замер геометрии зоны
akcent: замер
centralnyj_blok: замер
kommentarij_lektoru: ""
minuty: 1
vazhnost: opornyj
byudzhet_slov: 10
tip_verstki: %(tip)s
liniya: %(liniya)s
matematika_iz: []
illustracii: []
vvodit: []
opiraetsya_na: []
bez_opredeleniya_namerenno: []
status: v_deke
---

## Математика — развёрнуто
### [narrativ] замер
Строка для замера.

## Текст слайда — сжато
### [narrativ] замер
Строка для замера.

## Правки
- замер
"""


def _kartochka(tmp, sid, tip, liniya, zagolovok=""):
    """Синтетический слайд на диске → путь к `slaid.md` (структура папок ровно
    такая, какую ждёт `compile_slide_html`: <лекция>/slajdy/<sid>/slaid.md)."""
    d = Path(tmp) / "lek" / "slajdy" / sid
    d.mkdir(parents=True, exist_ok=True)
    (d / "slaid.md").write_text(
        KARTOCHKA % {"sid": sid, "tip": tip, "liniya": liniya,
                     "zagolovok": zagolovok or '""'}, encoding="utf-8")
    return d / "slaid.md"


_JS_SHRIFT = r"""
(cfg) => {
  const zone = document.querySelector('.zone.t-body') || document.querySelector('.t-body');
  if (!zone) return {error: 'зоны нет'};
  const cs = getComputedStyle(zone);
  const kegl = parseFloat(cs.fontSize);
  const lh = parseFloat(cs.lineHeight);

  // ── k_znak: средняя ширина знака / кегль ────────────────────────────────
  // Меряется НЕ по готовым абзацам (там перенос уже случился и последняя
  // строка короче — среднее поехало бы), а одной неразрывной пробной строкой
  // в ТОЙ ЖЕ зоне, тем же шрифтом и кеглем: ширина / число знаков / кегль.
  function proba_shirina(cls) {
    const probe = document.createElement('span');
    probe.style.cssText = 'white-space:pre;position:absolute;visibility:hidden;left:-99999px';
    if (cls) probe.className = cls;
    probe.textContent = cfg.proba;
    zone.appendChild(probe);
    const w = probe.getBoundingClientRect().width;
    probe.remove();
    return w;
  }
  const probeW = proba_shirina('');
  // `.acc{font-weight:700}` (base.css:144) — жирный акцент ШИРЕ обычного знака,
  // и смета, считавшая его обычным, занижала длину абзаца.
  const probeAccW = proba_shirina('acc');

  const znakW = probeW / cfg.proba.length;

  // Длина ИСХОДНОГО TeX берётся из mathml-аннотации KaTeX, а не из textContent
  // элемента: textContent склеивает html-рендер И текст аннотации, и «длина
  // формулы» выходит вдвое-втрое завышенной (наступил на это первым прогоном —
  // k_inline вышел отрицательным, −17 знаков «надбавки»).
  function texLen(e) {
    const a = e.querySelector('annotation[encoding="application/x-tex"]');
    return a ? (a.textContent || '').length : null;
  }
  // ГЛИФЫ: текст `.katex-html` — это ровно те знаки, которые видны на экране
  // (mathml-ветка `.katex-mathml` — дубль для скринридеров, её брать нельзя).
  // Прокси заведомо лучше длины TeX: `\mathbb R^{n+1}` — 15 знаков исходника и
  // 4 глифа на экране.
  function glifLen(e) {
    const h = e.querySelector('.katex-html');
    return h ? (h.textContent || '').replace(/\s+/g, '').length : null;
  }

  // ── h_formula: высота ВЫНОСНОЙ формулы в долях СТРОКИ ────────────────────
  // 🔴 «Выносная» в этой фабрике — НЕ `\[…\]`/`$$…$$`: такого синтаксиса в
  // конвейере нет вовсе (`build_deck.render_inline_md` знает ровно `$…$`), и
  // `.katex-display` в корпусе не встречается ни разу. Выносная формула здесь —
  // АБЗАЦ, состоящий из одной формулы и ничего больше: он и занимает
  // собственную строку (или несколько). Меряем именно его.
  // 🔴 ИСКЛЮЧЕНИЕ ИЗ ЗАПРЕТА «солвер не трогать» (заход vid-blokov-vnedrenie,
  // см. `## ОТЧЁТ` файла-захода) — тот же ремонт, что в `vmeshchenie.py`:
  // формула НИЖЕ не меняется, меняется только то, какие узлы DOM считаются
  // «верхнеуровневым абзацем зоны». До этого захода абзацы были ПРЯМЫМИ детьми
  // `.t-body`; теперь между ними и зоной стоит обёртка `.blk` (Э2) — без этой
  // правки инструмент находит НОЛЬ абзацев-формул на любой карточке с блоками,
  // и калибровка `H_FORMULA`/`K_GLIF_*` при следующем перезапуске молча
  // выйдет на пустом множестве (найдено верификатором захода: n=33→n=0 на
  // живой L2, не било по текущему гейту только потому, что числа уже запечены
  // константами и не пересчитывались в рамках этого захода).
  const paras = Array.from(zone.querySelectorAll(
    ':scope > p, :scope > ul.tlist li, :scope > .blk > p, :scope > .blk > ul.tlist li'));
  const formulaOnly = paras.filter(p => {
    const k = p.querySelectorAll('.katex');
    if (k.length !== 1) return false;
    // текст абзаца без текста формулы — только пробелы/пунктуация
    const own = (p.textContent || '').replace(k[0].textContent || '', '').trim();
    return own.length <= 2;
  });
  const formulaLines = formulaOnly.map(p => p.getBoundingClientRect().height / lh)
                                   .filter(v => v > 0);

  // ── k_inline: во сколько раз отрендеренная формула ШИРЕ своего TeX ────────
  // Смета читает КАРТОЧКУ, где формула стоит как `$<tex>$`. Ей нужно знать, во
  // сколько знаков превращается TeX длины L при вёрстке. Отсюда отношение
  // «знаков-эквивалентов на экране / знаков TeX в источнике» — коэффициент, на
  // который смета домножает длину исходного TeX.
  const inl = Array.from(zone.querySelectorAll('.katex'));
  const ratios = [];
  const pary = [];   // [длина TeX, ширина в знаках-эквивалентах] — сырьё под подгонку
  for (const e of inl) {
    const L = texLen(e);
    const w = e.getBoundingClientRect().width;
    const G = glifLen(e);
    if (L && w > 0) { ratios.push((w / znakW) / L); pary.push([L, w / znakW, G || 0]); }
  }

  return {kegl_px: kegl, line_height_px: lh, zone_w: zone.clientWidth, zone_h: zone.clientHeight,
          proba_width: probeW, proba_len: cfg.proba.length,
          k_acc: probeAccW / probeW,
          n_inline: inl.length, n_formula_only: formulaOnly.length,
          formula_lines: formulaLines, inline_ratios: ratios, inline_pary: pary};
}
"""

# Проба для `k_znak` — не «алфавит», а РЕАЛЬНАЯ русская проза корпуса: средняя
# ширина знака зависит от частотности букв и пробелов, и на равномерном алфавите
# она систематически шире живого текста.
PROBA = ("Пространство и его двойственное связаны отображением, которое не зависит "
         "от выбора базиса; именно это и делает изоморфизм каноническим, а не "
         "случайным совпадением размерностей в конечномерном случае")


def zamer_geometrii(page, tmp):
    """Э2.1: W и H текстовой зоны по типам × сетке `liniya`, плюс цена заголовка."""
    out = {"tipy": {}, "zagolovok_px": None, "viewport": VIEWPORT}
    for tip in TIPY_S_TEKSTOM:
        steps = LINIYA_STEPS if tip.startswith("polosa_") else (0,)
        rows = []
        for liniya in steps:
            md = _kartochka(tmp, "z_%s_%s" % (tip, liniya), tip, liniya)
            _, html = compile_slide_html(md)
            p = Path(tmp) / "s.html"
            p.write_text(html, encoding="utf-8")
            r = vmeshchenie.izmerit(page, p)
            rows.append({"liniya": liniya, "W": r["content_w"], "H": r["content_h"],
                         "client_w": r["clientWidth"], "client_h": r["clientHeight"],
                         "lh_px": r["line_height_px"], "kegl_px": r["kegl_px"]})
        out["tipy"][tip] = rows

    # цена заголовка на экране — та же зона, тот же тип, разница только в поле.
    # Меряется ТЕМ ЖЕ `izmerit` (он теперь отдаёт `zagolovok_h`), а не отдельным
    # evaluate по уже загруженной странице — иначе замер молча считает предыдущий
    # слайд (наступил на это в первом же прогоне: вышло 0).
    md1 = _kartochka(tmp, "z_zag", "tolko_tekst", 0, zagolovok="Заголовок замера")
    _, html = compile_slide_html(md1)
    p = Path(tmp) / "s.html"
    p.write_text(html, encoding="utf-8")
    out["zagolovok_px"] = round(vmeshchenie.izmerit(page, p)["zagolovok_h"], 2)

    # 🔴 У заголовка ДВЕ роли, а не одна: `tipy._zag_uzkij` включает
    # `--t-frametitle-n` (64/1.4) на всех типах с иллюстрацией, а полнотекстовый
    # `tolko_tekst` берёт широкую `--t-frametitle` (76/1.333). Смета до этого
    # знала одну константу и завышала цену заголовка узких типов на ~11px —
    # слепая зона была ОБЪЯВЛЕНА в `smeta.py` и здесь закрывается замером.
    # Снимается цена СТРОКИ (`line-height`) и отбивка (`margin-bottom`), а не
    # высота пробного заголовка целиком: на узкой зоне проба сама переносится в
    # две строки, и «высота» замерила бы не роль, а длину пробного текста.
    for tip in TIPY_S_TEKSTOM:
        md = _kartochka(tmp, "z_zag_%s" % tip, tip, 50, zagolovok="Замер")
        _, html = compile_slide_html(md)
        p.write_text(html, encoding="utf-8")
        page.goto("file://" + p.resolve().as_posix())
        page.wait_for_timeout(80)
        out.setdefault("zagolovok_po_tipam", {})[tip] = page.evaluate(_JS_ZAG_ROL)

    # 🔴 ПЕРЕНОС заголовка. Одной цены за строку недостаточно: на живой Л2 два
    # заголовка из двенадцати переносятся в ДВЕ строки («Двойственное
    # пространство», «Естественный изоморфизм»), и смета их считала одной —
    # занижение на 1.3–2.4 строки, то есть в опасную сторону (пропуск
    # переполнения). Считать перенос средней шириной знака нельзя: у дисплейного
    # шрифта разброс `ширина/кегль` по живым заголовкам 0.598–0.700, а граница
    # «одна строка или две» лежит РОВНО в этом интервале. Поэтому снимается
    # таблица ширин глифов (canvas `measureText` на 100px, тот же шрифт, что
    # применён к `.zagolovok`) — сумма по таблице воспроизвела ширину живой
    # строки с точностью 1.6% в сторону завышения (безопасную) и угадала число
    # строк на всех 12 заголовках корпуса.
    ALFAVIT = ("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
               "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
               "0123456789"
               " ,.;:!?-—–«»()[]*/+=&№%")
    out["glif_zagolovka"] = page.evaluate(_JS_GLIFY, ALFAVIT)
    return out


_JS_ZAG_ROL = r"""
() => {
  const zone = document.querySelector('.zone.t-body');
  const zag = zone && zone.querySelector('.zagolovok');
  if (!zag) return {error: 'заголовка нет на пробе'};
  const cs = getComputedStyle(zag);
  const pz = getComputedStyle(zone);
  const okr = (x) => Math.round(x * 100) / 100;
  return {kegl: parseFloat(cs.fontSize), stroka_px: okr(parseFloat(cs.lineHeight)),
          otbivka_px: okr(parseFloat(cs.marginBottom)),
          W: okr(zone.clientWidth - parseFloat(pz.paddingLeft) - parseFloat(pz.paddingRight))};
}
"""

# Заголовок `text-transform:uppercase` — меряем ВЕРХНИЙ регистр, тот, что на экране.
_JS_GLIFY = r"""
(chars) => {
  const zag = document.querySelector('.zagolovok');
  if (!zag) return {error: 'заголовка нет на пробе'};
  const cs = getComputedStyle(zag);
  const cv = document.createElement('canvas').getContext('2d');
  cv.font = cs.fontStyle + ' ' + cs.fontWeight + ' 100px ' + cs.fontFamily;
  const t = {};
  for (const ch of chars) t[ch] = Math.round(cv.measureText(ch).width * 100) / 100;
  return {font: cv.font, na_100px: t};
}
"""


def zamer_konstant(page, lekcija):
    """Э2.2: k_znak, h_formula, k_inline — по ЖИВЫМ слайдам лекции (там есть
    настоящие формулы; на синтетике мерить нечего)."""
    lek = Path(lekcija)
    if not (lek / "slajdy").is_dir():
        raise SystemExit("ОШИБКА: %s — не папка лекции (нет подпапки slajdy/)" % lek)
    slides = sorted((lek / "slajdy").glob("*/slaid.md"))
    if not slides:
        raise SystemExit("ОШИБКА: в %s/slajdy нет ни одной карточки slaid.md" % lek)
    znak_ratios, disp_ratios, inline_nadbavki = [], [], []
    n_inline_vsego = 0
    n_formula_only = 0
    pary = []
    acc_ratios = []
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "s.html"
        for md in slides:
            try:
                _, html = compile_slide_html(md)
            except Exception:
                continue
            if not re.search(r'class="[^"]*\bt-body\b[^"]*"', html):
                continue
            p.write_text(html, encoding="utf-8")
            page.goto("file://" + str(p.resolve()))
            page.wait_for_timeout(120)
            r = page.evaluate(_JS_SHRIFT, {"proba": PROBA})
            if r.get("error"):
                continue
            kegl = r["kegl_px"]
            if kegl:
                znak_ratios.append((r["proba_width"] / r["proba_len"]) / kegl)
            acc_ratios.append(r["k_acc"])
            disp_ratios.extend(r["formula_lines"])
            inline_nadbavki.extend(r["inline_ratios"])
            pary.extend(r["inline_pary"])
            n_inline_vsego += r["n_inline"]
            n_formula_only += r["n_formula_only"]
    return {"k_znak": _svodka(znak_ratios), "k_acc": _svodka(acc_ratios),
            "h_formula": _svodka(disp_ratios),
            "k_inline": _svodka(inline_nadbavki),
            "k_inline_podgonka": _podgonka([(L, w) for L, w, _ in pary]),
            "k_glif_podgonka": _podgonka([(g, w) for _, w, g in pary if g]),
            "ohvat": {"слайдов_с_текстом": len(znak_ratios),
                       "инлайн_формул_всего": n_inline_vsego,
                       "абзацев_из_одной_формулы": n_formula_only}}


def _podgonka(pary):
    """Знаков-эквивалентов формулы как ФУНКЦИЯ длины её TeX, а не одно число.

    🔴 Почему функция. Одна медиана отношения (`k_inline`) даёт разброс 0.11–2.02:
    короткий TeX (`V`, `f`) рендерится почти в себя, длинный (`\\mathbb R^{n+1}`)
    сжимается втрое — управляющие последовательности занимают знаки в источнике и
    ноль на экране. Медиана посередине врёт в обе стороны, и именно она давала
    промах в 2 строки на `inyekcii` и `nekanonicheskij-izomorfizm` (найдено
    сверкой `smeta.py --sverit`, не рассуждением). МНК по (длина TeX → знаки на
    экране) — та же калибровка по браузеру, только двумя числами вместо одного."""
    if len(pary) < 3:
        return {"n": len(pary)}
    n = len(pary)
    sx = sum(L for L, _ in pary)
    sy = sum(w for _, w in pary)
    sxx = sum(L * L for L, _ in pary)
    sxy = sum(L * w for L, w in pary)
    den = n * sxx - sx * sx
    if den == 0:
        return {"n": n}
    b = (n * sxy - sx * sy) / den
    a = (sy - b * sx) / n
    ost = [abs(a + b * L - w) for L, w in pary]
    ost.sort()
    return {"n": n, "a": round(a, 4), "b": round(b, 4),
            "ostatok_median": round(ost[n // 2], 3), "ostatok_p95": round(ost[int(n * 0.95)], 3),
            "formula": "знаков ≈ %.4f + %.4f × длина_TeX" % (a, b)}


def _svodka(vals):
    if not vals:
        return {"n": 0}
    s = sorted(vals)
    n = len(s)
    return {"n": n, "min": round(s[0], 4), "median": round(s[n // 2], 4),
            "max": round(s[-1], 4), "mean": round(sum(s) / n, 4)}


def main():
    ap = argparse.ArgumentParser(description="Замер исходных чисел сметы (Э2.1, Э2.2)")
    ap.add_argument("lekcija", nargs="?", help="папка лекции для шрифтовых констант")
    ap.add_argument("--geometriya", action="store_true")
    ap.add_argument("--konstanty", action="store_true")
    ap.add_argument("--vse", action="store_true")
    a = ap.parse_args()
    do_geom = a.geometriya or a.vse or not (a.geometriya or a.konstanty or a.vse)
    do_const = a.konstanty or a.vse

    from playwright.sync_api import sync_playwright
    res = {}
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="chrome", headless=True)
        page = b.new_page(viewport=VIEWPORT, device_scale_factor=1)
        if do_geom:
            with tempfile.TemporaryDirectory() as tmp:
                res["geometriya"] = zamer_geometrii(page, tmp)
        if do_const:
            if not a.lekcija:
                ap.error("--konstanty требует папку лекции")
            res["konstanty"] = zamer_konstant(page, a.lekcija)
        b.close()
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
