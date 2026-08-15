#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TOOL-CONTRACT: called-by-build — режим `--dek` зовёт `sborka/deck.py` (main())
# на каждой сборке дека; режим по отдельным слайдам остался called-by-hand и
# закрывает ФАЗУ 3 (заход svedenie-i-smeta, Э2.5).
# Автоматическим ХУКОМ гейт быть по-прежнему НЕ МОЖЕТ: требует живого браузера,
# на pre-commit это минуты и падение без Chrome. Точка вызова ручного режима
# названа в конвейере — `bootstrap_lekcii.LIFECYCLE_TMPL`, строка «ФАЗА 3.9».
# До 08.08 гейт был написан и не звался НИ НА ОДНОМ шаге; до 16.08 сборка дека
# не звала его тоже — пересборка проходила, не проверяя ничего.
"""Гейт вмещения — краснеет, если содержимое слайда обрезано.

ДВА РЕЖИМА, и они мерят РАЗНОЕ.

`<slide.html> ...` (Э4 захода solver-vmeshcheniya) — отдельные скомпилированные
слайды, мера `fill = 100·scrollHeight/clientHeight` по зоне `.zone.t-body`, то
есть ПЕРЕПОЛНЕНИЕ БОКСА зоны. Режим оставлен как есть: на нём стоит ФАЗА 3.9.

`--dek <index.html>` (Э4 захода sloi-i-obrez) — собранный дек целиком, мера
ВИДИМЫЙ ОБРЕЗ. 🔴 Второй режим появился потому, что первая мера перестала что-либо
значить: заход снял `overflow` с `.zone.copy` (Э2 — «нижняя линия есть фон, текст
идёт поверх неё»), и с этого момента переполненный бокс НЕ РАВЕН обрезанному
тексту. Мера «запас бокса» замолчала бы ровно там, где раньше хоть что-то ловила.
Видимый обрез считается честно: прямоугольник каждого содержательного элемента
против ПЕРЕСЕЧЕНИЯ клип-прямоугольников всех его предков, режущих содержимое
(`overflow ≠ visible`), включая сам `.slide`. Что не попало внутрь — того зритель
не увидит, каким бы здоровым ни был бокс вокруг.

  python3 _generator/sborka/gejt_vmeshcheniya.py <slide.html> [<slide.html> ...]
  python3 _generator/sborka/gejt_vmeshcheniya.py --dek <index.html>
  exit 0 — ничего не обрезано
  exit 1 — обрезан хотя бы один слайд (в обоих режимах слайды названы поимённо)
"""
import argparse
import re
import sys
from pathlib import Path

SBORKA = Path(__file__).resolve().parent
sys.path.insert(0, str(SBORKA))
from vmeshchenie import izmerit  # noqa: E402

# 🔴 Найдено живым прогоном (заплатка sborka-l2-fazy-4-7): не у каждого слайда
# есть текстовая зона — `tip_verstki: polnyj_ekran` с непустым `illustracii`
# рендерит ТОЛЬКО картинки (`tipy.py: polnyj_ekran`), без `.zone.t-body`. Мерить
# там нечего — раньше гейт падал `RuntimeError` и ронял ВЕСЬ прогон ради одного
# бестекстового слайда, даже если он последний в списке. Тот же приём, что уже
# стоит в `deck.py:_podobrat_tipografiku` — пропуск ДО вызова измерителя.
T_BODY_RE = re.compile(r'class="[^"]*\bt-body\b[^"]*"')

# 🔴 Порог обреза по ШИРИНЕ, px. Не ноль: `scrollWidth`/`clientWidth` целые, и
# субпиксельная вёрстка (KaTeX ставит дроби) регулярно даёт 1–2px шума на
# заведомо влезающих строках. Живые обрезы Л2 были +93…+724px — на два порядка
# выше шума, так что порог различает их без спора.
PORAG_SHIRINY = 4


def check_slide(page, html_path):
    """Один скомпилированный слайд → (ok: bool, fill: float, clipped: bool)."""
    r = izmerit(page, html_path)
    return r


# ═════════════════ РЕЖИМ `--dek`: ВИДИМЫЙ ОБРЕЗ (Э4 захода sloi-i-obrez) ═════════════════

SLIDE_RE = re.compile(r'<section class="slide"[^>]*id="([^"]+)"')

# Порог видимого обреза, px. Та же природа, что у `PORAG_SHIRINY` выше: кадр
# масштабируется дробным коэффициентом (`scaleSlide`, pad 0.997), KaTeX ставит
# субпиксельные дроби, и на заведомо целых строках стабильно набегает 1–2px шума.
PORAG_OBREZA = 4

# 🔴 Что считается СОДЕРЖИМЫМ. Не «все элементы»: у слайда есть намеренные
# декорации, вылезающие за свой бокс (`.blk-rule` — линейка центрального блока,
# `base.css:339`, стоит левее зоны СПЕЦИАЛЬНО). Содержимое — это то, что зритель
# читает и смотрит: элементы с собственным непустым текстом плюс `.panel`
# (единственный контейнер иллюстрации, `tipy._ill_zone`). Признак структурный, не
# список типов вёрстки — новый тип попадает под него сам.
_JS_OBREZ = r"""
(a) => {
  const POROG = a.porog;
  const slide = document.getElementById(a.sid);
  if (!slide) return {error: 'слайда нет в деке: ' + a.sid};
  // Последняя сцена: на промежуточных часть содержимого намеренно скрыта, и
  // мерить надо самый полный кадр — тот же приём, что в `vmeshchenie.izmerit`.
  if (typeof applyScene === 'function' && typeof scenesOf === 'function') {
    applyScene(slide, scenesOf(slide));
  }
  const svoj_tekst = el => Array.from(el.childNodes).some(
        n => n.nodeType === 3 && n.textContent.trim().length);
  const soderzhimoe = Array.from(slide.querySelectorAll('*')).filter(el => {
    if (!svoj_tekst(el) && !el.classList.contains('panel')) return false;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return false;
    const r = el.getBoundingClientRect();
    return r.width > 0.5 && r.height > 0.5;
  });
  // Клип-предки: все, кто режет, до `.slide` включительно. `.slide` режет всегда
  // (`base.css`, overflow:hidden) — это и есть КАДР, дальше него зрителя нет.
  //
  // 🔴 ВЫРОЖДЕННЫЙ КЛИПЕР = НАМЕРЕННО СПРЯТАННОЕ, А НЕ ОБРЕЗАННОЕ, и это найдено
  // первым же прогоном по здоровому эталону, где гейт покраснел на 20 слайдах из
  // 26 «обрезом справа на 300–780px». Резали не слайды: KaTeX кладёт рядом с
  // видимой формулой её MathML-дубль для скринридеров и прячет его коробкой
  // 1×1px с `overflow:hidden` (`.katex-mathml`). Внутри той коробки лежит
  // полноразмерное дерево `mi/mo/mn` — формально «обрезанное» на сотни пикселей,
  // фактически невидимое обоим: и зрителю, и владельцу.
  // Признак взят СТРУКТУРНЫЙ, а не по имени класса KaTeX: клипер меньше 3px по
  // любой стороне — это идиома «спрятать от глаз, оставить ассистивным
  // технологиям», а не вёрстка слайда. Назови я здесь `.katex-mathml`, гейт
  // краснел бы на следующей же библиотеке с тем же приёмом.
  // ⚠ Если бы этот случай не был отсечён, гейт обходили бы целиком — и защита,
  // ради которой он написан, пропала бы вся разом (ограничитель Э4 захода).
  const klipery = el => {
    const out = [];
    for (let e = el.parentElement; e; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.overflowX !== 'visible' || cs.overflowY !== 'visible') {
        const cr = e.getBoundingClientRect();
        if (cr.width < 3 || cr.height < 3) return null;   // спрятано, не обрезано
        out.push(cr);
      }
      if (e === slide) break;
    }
    return out;
  };
  // 🔴 ДОПУСК СЧИТАЕТСЯ ОТ ИНТЕРЛИНЬЯЖА, А НЕ НАЗНАЧАЕТСЯ ЧИСЛОМ. Бокс строки шире
  // своих чернил на полулидинг: сверху и снизу у него пустая полоса высотой
  // (интерлиньяж − кегль)/2, где нет ни одного пикселя буквы. Срезанный кусок
  // МЕНЬШЕ этой полосы зритель увидеть не может физически — там нечего видеть.
  // Найдено прогоном по здоровому эталону: подпись `X` внутри SVG-иллюстрации
  // `funktor` торчала над клипером на 5.6px пустого лидинга, и плоский порог в
  // 4px честно назвал это обрезом. Красный гейт на здоровом эталоне обходят
  // целиком — и защита пропадает вся разом, а не только в этом месте.
  const dopusk = el => {
    const cs = getComputedStyle(el);
    const kegl = parseFloat(cs.fontSize) || 0;
    const lh = parseFloat(cs.lineHeight) || kegl * 1.2;   // 'normal' → примерно 1.2
    return Math.max(POROG, 0.4 * lh);
  };
  // `izbytok` — насколько срез ПРЕВЫШАЕТ допуск; по нему и краснеем. В отчёт при
  // этом уходит сырой `obrez`, а не разность: владельцу нужна величина, которую он
  // сможет увидеть на кадре линейкой, а не внутренняя мера гейта.
  let izbytok = 0, obrez = 0, kto = null, storona = null;
  for (const el of soderzhimoe) {
    const r = el.getBoundingClientRect();
    const kl = klipery(el);
    if (kl === null) continue;
    const d = el.classList.contains('panel') ? POROG : dopusk(el);
    for (const c of kl) {
      const nedobor = {'снизу': r.bottom - c.bottom, 'сверху': c.top - r.top,
                       'справа': r.right - c.right, 'слева': c.left - r.left};
      for (const [s, v] of Object.entries(nedobor)) {
        if (v - d > izbytok) {
          izbytok = v - d; obrez = v; storona = s;
          // `className` у SVG-узлов — SVGAnimatedString, а не строка: без
          // `getAttribute` в отчёт уезжало «[object SVGAnimatedString]» вместо
          // имени элемента, то есть гейт называл слайд, но не место в нём.
          const cls = (el.getAttribute && el.getAttribute('class') || '').trim();
          kto = el.tagName.toLowerCase() + (cls ? '.' + cls.split(/\s+/).join('.') : '')
                + ' ⟨' + (el.textContent || '').trim().slice(0, 24) + '⟩';
        }
      }
    }
  }
  return {izbytok: +izbytok.toFixed(1), obrez: +obrez.toFixed(1),
          kto, storona, n: soderzhimoe.length};
}
"""


def slaidy_deka(html):
    """id слайдов дека В ПОРЯДКЕ ПОКАЗА (= индекс `?only=N` движка).

    `[data-skip]` исключены ровно так же, как их исключает `engine.js`, иначе
    индекс разъедется и гейт будет мерить не тот слайд, который называет."""
    starts = [(m.start(), m.group(1)) for m in SLIDE_RE.finditer(html)]
    out = []
    for i, (pos, sid) in enumerate(starts):
        end = starts[i + 1][0] if i + 1 < len(starts) else len(html)
        tag = html[pos:pos + html[pos:end].find(">") + 1]
        if "data-skip" not in tag:
            out.append(sid)
    return out


def proverit_dek(dist_html, pechat=print):
    """Собранный дек → список обрезанных `(sid, обрез_px, кто, сторона)`.

    Возвращает список, а не код возврата: звать эту функцию будет и `deck.py`,
    которому решать за владельца, ронять ли сборку, не положено (ограничитель Э4)."""
    from urllib.parse import quote
    from playwright.sync_api import sync_playwright

    dist = Path(dist_html)
    sids = slaidy_deka(dist.read_text(encoding="utf-8"))
    url = "file://" + quote(str(dist.resolve()))
    plohie = []
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        page = b.new_page(viewport={"width": 1440, "height": 810}, device_scale_factor=1)
        for i, sid in enumerate(sids):
            page.goto("%s?only=%d" % (url, i))
            page.wait_for_timeout(200)   # шрифты/KaTeX — тот же приём, что в kadry.py
            r = page.evaluate(_JS_OBREZ, {"sid": sid, "porog": PORAG_OBREZA})
            if r.get("error"):
                raise RuntimeError(r["error"])
            if r["izbytok"] > 0:
                plohie.append((sid, r["obrez"], r["kto"], r["storona"]))
        b.close()
    if plohie:
        pechat("❌ ГЕЙТ ВМЕЩЕНИЯ КРАСНЫЙ: видимый обрез на %d слайд(ах) из %d"
               % (len(plohie), len(sids)))
        for sid, obrez, kto, storona in plohie:
            pechat("   · %-32s обрезано %s на %.1fpx — «%s»" % (sid, storona, obrez, kto))
    else:
        pechat("✅ гейт вмещения: видимого обреза нет, проверено %d из %d слайдов"
               % (len(sids), len(sids)))
    return plohie


def main():
    ap = argparse.ArgumentParser(description="Гейт вмещения — краснеет на обрезанном тексте")
    ap.add_argument("html", nargs="*", help="скомпилированные HTML слайдов (slaid.py -o ...)")
    ap.add_argument("--dek", metavar="INDEX.HTML",
                     help="собранный дек целиком: мера — ВИДИМЫЙ обрез относительно кадра, "
                          "а не запас бокса зоны (Э4 захода sloi-i-obrez). Этот режим зовёт "
                          "`deck.py` сам на каждой сборке")
    args = ap.parse_args()

    if args.dek:
        if args.html:
            print("ОШИБКА: --dek и список слайдов вместе не имеют смысла — это разные меры",
                  file=sys.stderr)
            return 2
        if not Path(args.dek).is_file():
            print("ОШИБКА: не существует или не файл — %s" % args.dek, file=sys.stderr)
            return 2
        return 1 if proverit_dek(args.dek) else 0

    if not args.html:
        ap.error("нужен либо список слайдов, либо --dek")

    # 🔴 Кривой вход отвергается ДО запуска браузера: несуществующий путь раньше
    # давал `FileNotFoundError` из середины прогона, уже подняв Chrome, и вердикт
    # по остальным слайдам терялся вместе с трейсбеком.
    net = [h for h in args.html if not Path(h).is_file()]
    if net:
        print("ОШИБКА: не существует или не файл — %s" % ", ".join(net), file=sys.stderr)
        return 2

    from playwright.sync_api import sync_playwright
    bad = []
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        page = b.new_page(viewport={"width": 1440, "height": 810}, device_scale_factor=1)
        skipped = 0
        for html in args.html:
            if not T_BODY_RE.search(Path(html).read_text(encoding="utf-8")):
                print("⚪ БЕЗ ТЕКСТА  %-40s текстовой зоны на слайде нет — не мерю" % html)
                skipped += 1
                continue
            r = check_slide(page, html)
            fill = r["fill"]
            clipped = fill is not None and fill > 100
            perelivX = r.get("pereliv_x") or 0
            plohо = clipped or perelivX > PORAG_SHIRINY
            status = "❌ ОБРЕЗАНО" if plohо else "✅ влезло"
            hvost = ("  ⟵ за правый край +%dpx: %s" % (perelivX, r.get("pereliv_chto"))
                     if perelivX > PORAG_SHIRINY else "")
            print("%s  %-40s заполнение %.1f%%%s"
                  % (status, html, fill if fill is not None else -1, hvost))
            if plohо:
                bad.append((html, fill, perelivX, r.get("pereliv_chto")))
        b.close()

    if bad:
        print("\nГЕЙТ КРАСНЫЙ: %d слайд(ов) обрезано:" % len(bad), file=sys.stderr)
        for html, fill, perelivX, chto in bad:
            if fill is not None and fill > 100:
                print("  %s — заполнение %.1f%%, не влезает %.1f%% высоты зоны"
                      % (html, fill, fill - 100), file=sys.stderr)
            if perelivX > PORAG_SHIRINY:
                print("  %s — уезжает за правый край на %dpx: «%s». Кегль тут не спасёт: "
                      "неразрывный атом шире колонки — разбить строку в карточке"
                      % (html, perelivX, chto), file=sys.stderr)
        return 1
    print("\nГЕЙТ ЗЕЛЁНЫЙ: все %d слайд(ов) с текстом влезли (%d без текстовой зоны — не мерены)."
          % (len(args.html) - skipped, skipped))
    return 0


if __name__ == "__main__":
    sys.exit(main())
