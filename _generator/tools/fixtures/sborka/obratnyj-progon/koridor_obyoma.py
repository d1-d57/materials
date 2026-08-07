#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Заход dovodka-solvera, Часть Б: КОРИДОР ОБЪЁМА — тот же измеритель, обратный
вопрос. Известно (тип вёрстки + линия + состав блоков — решаются на интервью,
ДО текста), искомое — знаков: печатает «от N до M», не текст.

Типографика ЗАФИКСИРОВАНА в корпусной норме — БУКВАЛЬНО, ОДНА точка (kegl=
медиана корпуса, lh=медиана, blok=медиана blok_koef×kegl), не диапазон/решётка:
`vmeshchenie.izmerit()` (уже был — «разовый промер без перебора»), не
`podobrat_slide` (тот перебирает рунги/кегль и САМ подбирает кегль под
максимальное заполнение — проверено фактом первой пробой этого захода: на
`podobrat_slide` `fill` выходил 100% что при N=10, что при N=430, потому что
солвер тянет кегль вверх, пока не влезет — переменная N становится
ненаблюдаемой). При буквально зафиксированной типографике N — единственное,
что меняет геометрию, и `izmerit()` (расширен этим заходом: `content_fill`,
`dyhanie`) её честно ловит.

🔴 НАЙДЕНО ЭТИМ ЗАХОДОМ (не было известно заранее): `.zone` растянута CSS-
гридом до высоты ряда — `scrollHeight` при непереполненном контенте ВСЕГДА
равен `clientHeight` (это высота РАСТЯНУТОГО БОКСА, не текста), значит
готовый `fill` из `izmerit()` НЕПРИГОДЕН для «мельчит и пусто внизу» — нужен
`content_fill` (реальный нижний край текста относительно верха зоны).
`fill`/`fits` остаются пригодны для ВЕРХНЕЙ границы (переполнение — это
`scrollHeight>clientHeight`, стретч тут ни при чём).

Дыхание при зафиксированной типографике — НЕ функция N (то же самое найдено
этим заходом, прямое следствие CSS: промежуток между блоками — margin-top в
px, не зависит от того, сколько текста внутри абзаца). Значит «дыхание≥p25»
— это ПОРОГ НА САМУ ТОЧКУ (типографика-норма + состав блоков + zona-высота),
не на N: меряется ОДИН раз, до бинарного поиска, а не переизмеряется на
каждом N.

Синтетический наполнитель — строго по СТРУКТУРЕ (число/типы блоков), не текст
ни одного реального слайда — критерий 3 захода («коридор без знания текста»).

  python3 koridor_obyoma.py --axis horizontal --liniya 49.2 --sostav p,p,p
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SBORKA = REPO / "_generator" / "sborka"
sys.path.insert(0, str(SBORKA))
sys.path.insert(0, str(REPO / "_generator"))
import slaid  # noqa: E402
import korpus  # noqa: E402
import vmeshchenie  # noqa: E402

FILLER_WORDS = ["текст", "коридор", "объём", "знаков", "строка", "слово", "абзац",
                "линия", "заполнение", "содержание", "структура", "плотность",
                "поле", "проба", "запас", "решётка"]

_SOSTAV_TOKEN = re.compile(r"^(p|ul(\d+))$")


def parse_sostav(spec):
    """`p,p,ul3` → [("p",1), ("p",1), ("ul",3)]. Кривой токен — падает громко
    (ValueError), не молчит и не угадывает."""
    units = []
    for tok in spec.split(","):
        tok = tok.strip()
        m = _SOSTAV_TOKEN.match(tok)
        if not m:
            raise ValueError("токен состава не распознан: %r (ожидается 'p' или 'ulN')" % tok)
        if tok == "p":
            units.append(("p", 1))
        else:
            k = int(m.group(2))
            if k < 1:
                raise ValueError("список из %d пунктов бессмыслен: %r" % (k, tok))
            units.append(("ul", k))
    if not units:
        raise ValueError("состав пуст")
    return units


def filler(target_chars):
    """Слова-заполнители до ~target_chars знаков (не текст слайда — структура
    роли не играет, важна средняя длина слова для переноса строк, Cyrillic)."""
    if target_chars <= 0:
        return ""
    words, total, i = [], 0, 0
    while total < target_chars:
        w = FILLER_WORDS[i % len(FILLER_WORDS)]
        words.append(w)
        total += len(w) + 1
        i += 1
    s = " ".join(words)
    return s[:target_chars] if len(s) > target_chars else s


def synthetic_markdown(n_chars, units):
    total_units = sum(k for _, k in units)
    chars_per_unit = max(1, n_chars // total_units)
    blocks = []
    for kind, k in units:
        if kind == "p":
            blocks.append(filler(chars_per_unit))
        else:
            items = [filler(chars_per_unit) for _ in range(k)]
            blocks.append("\n".join("- %s" % it for it in items))
    return "\n\n".join(blocks)


def build_synthetic_card(n_chars, units, axis, liniya, out_root):
    tip = "polosa_gorizontalnaya" if axis == "horizontal" else "polosa_vertikalnaya"
    lekcija_dir = out_root / "koridor-proba"
    slajd_dir = lekcija_dir / "slajdy" / "proba"
    slajd_dir.mkdir(parents=True, exist_ok=True)
    body = synthetic_markdown(n_chars, units)
    card = (
        "---\n"
        "imya: proba\n"
        "tip_verstki: %s\n"
        "liniya: %g\n"
        "illustracii: []\n"
        "---\n"
        "## Математика — развёрнуто\n"
        "### [narrativ] синтетический наполнитель коридора\n"
        "%s\n\n"
        "## Текст слайда — сжато\n"
        "### [narrativ] синтетический наполнитель коридора\n"
        "%s\n\n"
        "## Правки\n"
    ) % (tip, liniya, body, body)
    (slajd_dir / "slaid.md").write_text(card, encoding="utf-8")
    out_html = lekcija_dir / "dist" / "proba.html"
    out_html.parent.mkdir(parents=True, exist_ok=True)
    _, doc = slaid.compile_slide_html(slajd_dir / "slaid.md", title="proba")
    out_html.write_text(doc, encoding="utf-8")
    return out_html


def norma_tipografiki(corpus):
    kegl = corpus["кегль_px"]["median"]
    lh = corpus["lh_отношение_к_кеглю"]["median"]
    koef = corpus["blok_koef_k_keglyu"]["median"]
    return {"kegl": kegl, "lh": lh, "blok": round(kegl * koef, 3), "blok_koef": koef}


def probe(page, n_chars, units, axis, liniya, norma, out_root):
    html = build_synthetic_card(n_chars, units, axis, liniya, out_root)
    return vmeshchenie.izmerit(page, html, kegl=norma["kegl"], lh=norma["lh"], blok=norma["blok"])


def find_max(page, units, axis, liniya, norma, out_root, lo=20, hi=4000, iters=12):
    """Верхняя граница: `fits` (scrollHeight<=clientHeight — переполнение,
    stretch-бокс тут не искажает) монотонно ложное с ростом N."""
    if not probe(page, lo, units, axis, liniya, norma, out_root)["fits"]:
        return None  # даже минимум переполняет зону при этой типографике
    if probe(page, hi, units, axis, liniya, norma, out_root)["fits"]:
        return hi
    best, a, b = lo, lo, hi
    for _ in range(iters):
        mid = (a + b) // 2
        if mid == a:
            break
        if probe(page, mid, units, axis, liniya, norma, out_root)["fits"]:
            best, a = mid, mid
        else:
            b = mid
    return best


def find_min(page, units, axis, liniya, norma, out_root, fill_lo, n_max, lo=5, iters=12):
    """Нижняя граница: `content_fill` (реальный край текста, НЕ scrollHeight —
    см. докстринг модуля) монотонно растёт с N до тех пор, пока не влезает."""
    r_lo = probe(page, lo, units, axis, liniya, norma, out_root)
    if r_lo["content_fill"] is not None and r_lo["content_fill"] >= fill_lo:
        return lo
    a, b = lo, n_max
    for _ in range(iters):
        mid = (a + b) // 2
        if mid == b:
            break
        r = probe(page, mid, units, axis, liniya, norma, out_root)
        if r["content_fill"] is not None and r["content_fill"] >= fill_lo:
            b = mid
        else:
            a = mid
    return b


def izmerit_dyhanie_normy(page, units, axis, liniya, norma, out_root, n_probe=400):
    """Дыхание при зафиксированной типографике — НЕ функция N (см. докстринг
    модуля), меряется ОДИН раз на представительном N (довольно текста, чтобы
    было ≥2 блоков не-пустыми — `n_probe` с запасом)."""
    r = probe(page, n_probe, units, axis, liniya, norma, out_root)
    return r.get("dyhanie")


def main():
    ap = argparse.ArgumentParser(description="Коридор объёма — знаков от N до M "
                                              "БЕЗ знания текста слайда")
    ap.add_argument("--axis", choices=("horizontal", "vertical"), required=True)
    ap.add_argument("--liniya", type=float, required=True)
    ap.add_argument("--sostav", required=True, help="'p,p,ul3' — абзацы и списки")
    ap.add_argument("--out-root", default=str(HERE))
    args = ap.parse_args()

    units = parse_sostav(args.sostav)
    corpus = korpus.corpus_stats()
    norma = norma_tipografiki(corpus)

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        page = b.new_page(viewport={"width": 1440, "height": 810}, device_scale_factor=1)
        out_root = Path(args.out_root)

        dyhanie_norm = izmerit_dyhanie_normy(page, units, args.axis, args.liniya, norma, out_root)
        if dyhanie_norm is not None and dyhanie_norm < vmeshchenie.DYHANIE_P25:
            print(json.dumps({"коридор": None, "норма": norma,
                              "дыхание_при_норме": round(dyhanie_norm, 3),
                              "причина": "типографика-норма при этом составе блоков и этой зоне "
                                         "не проходит пол дыхания (≥p25=%.3f) НИ ПРИ КАКОМ N — "
                                         "дыхание тут не функция объёма текста, это свойство "
                                         "самой типографики+состава" % vmeshchenie.DYHANIE_P25},
                              ensure_ascii=False, indent=2))
            print("КОРИДОРА НЕТ: пол дыхания недостижим при данной норме/составе/liniya",
                  file=sys.stderr)
            b.close()
            return 1

        n_max = find_max(page, units, args.axis, args.liniya, norma, out_root)
        if n_max is None:
            print(json.dumps({"коридор": None, "норма": norma,
                              "причина": "даже минимальный текст (20 знаков) переполняет зону "
                                         "при типографике-норме — эта комбинация axis/liniya/"
                                         "состава непригодна для нормы вовсе"},
                              ensure_ascii=False, indent=2))
            print("КОРИДОРА НЕТ: даже минимум переполняет зону при норме", file=sys.stderr)
            b.close()
            return 1
        n_min = find_min(page, units, args.axis, args.liniya, norma, out_root,
                          fill_lo=vmeshchenie.FILL_LO, n_max=n_max)
        b.close()

    out = {"axis": args.axis, "liniya": args.liniya, "sostav": args.sostav,
           "норма_типографики": norma, "дыхание_при_норме": round(dyhanie_norm, 3)
           if dyhanie_norm is not None else None,
           "min_znakov": n_min, "max_znakov": n_max}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    print("\nот %d до %d знаков" % (n_min, n_max), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
