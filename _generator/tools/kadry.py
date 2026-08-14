#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TOOL-CONTRACT: called-by-hand
# Зовёт исполнитель/приёмка руками после правок вёрстки, не хук и не шаг
# сборки — кадры разово смотрят глазами, не гоняют на каждый коммит.
"""Скриншотер характерных слайдов дека (заход pravila-kadra, Э6).

Владелец нашёл шесть дефектов ВИДА, листая дек ГЛАЗАМИ — ни замер вмещения,
ни посимвольное сравнение текста, ни верификатор их не поймали по построению:
они мерят «влезает ли», а не «как выглядит». Инструмент кладёт PNG характерных
кадров на диск, чтобы такие дефекты в следующий раз видела приёмка, а не
только владелец на живой презентации.

Характерные слайды — НЕ «первые N», а по ТИПАМ (см. _vybrat_harakternye):
плотный слайд с доказательством · разреженный (мало текста) · с иллюстрацией
у кромки (зона `.ill-row`) · из одних нарративов (все `.blk` — `data-tip=
"narrativ"`) · с самым длинным заголовком на экране · со сценами (сняты
первая И последняя). Отбор —
эвристикой по СОБРАННОМУ HTML, не по жёстко вписанным id: инструмент годится
для любой лекции этого пайплайна, а не только для `teorkat-vvedenie/L2`.

Сборка дека и headless-браузер — тем же способом, что `sborka/smeta.py:sverit`
(Playwright, `channel=chrome`, headless): второй способ гонять браузер этот
репозиторий не заводит.

ИСПОЛЬЗОВАНИЕ:
    python3 _generator/tools/kadry.py <папка-лекции> [--out <папка kadry/>]

Без `--out` кадры уходят в `<папка-лекции>/../_kadry_tmp/` — годится для
разовой проверки; для сдачи в отчёт всегда указывать `--out` на `kadry/`
зоны захода.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
GENERATOR = TOOLS.parent
REPO = GENERATOR.parent
HOLST_W, HOLST_H = 1440, 810

SLIDE_RE = re.compile(r'<section class="slide[^"]*"[^>]*id="([a-zA-Z0-9_-]+)"[^>]*>')
SCENES_RE = re.compile(r'data-scenes="(\d+)"')
ZAGOLOVOK_RE = re.compile(r'<div class="zagolovok">(.*?)</div>', re.S)
BLK_RE = re.compile(r'<div class="blk"[^>]*data-tip="([a-zA-Z]+)"')
ILL_ROW_RE = re.compile(r'class="zone board ill-row')
COPY_ZONE_RE = re.compile(r'class="zone copy')
TAG_RE = re.compile(r'<[^>]+>')


def sobrat_dek(lekcia, out_html):
    """`sborka/deck.py` тем же способом, что владелец/CI — subprocess, не импорт:
    deck.py не задуман библиотекой (свой argparse, свой sys.exit)."""
    cmd = [sys.executable, str(GENERATOR / "sborka" / "deck.py"), str(lekcia),
           "-o", str(out_html)]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO))
    if r.returncode != 0:
        raise RuntimeError("сборка дека упала (rc=%d):\n%s" % (r.returncode, r.stderr[-3000:]))
    return r.stdout


def razobrat_slaidy(html):
    """Список слайдов В ПОРЯДКЕ ДЕКИ (= порядок `.slide:not([data-skip])` в
    `engine.js`, тот же индекс, что `?only=N`) с признаками для отбора
    характерных. `[data-skip]` слайды из этого списка ИСКЛЮЧЕНЫ — ровно как их
    исключает сам движок (`engine.js:4`), иначе индекс `?only=N` разъедется."""
    starts = [(m.start(), m.group(1)) for m in SLIDE_RE.finditer(html)]
    out = []
    idx = 0
    for i, (pos, sid) in enumerate(starts):
        end = starts[i + 1][0] if i + 1 < len(starts) else len(html)
        chunk = html[pos:end]
        head_end = chunk.find('>')
        tag = chunk[:head_end + 1]
        if "data-skip" in tag:
            continue
        zag_m = ZAGOLOVOK_RE.search(chunk)
        zag_text = TAG_RE.sub("", zag_m.group(1)) if zag_m else ""
        scenes_m = SCENES_RE.search(tag)
        tips = BLK_RE.findall(chunk)
        out.append({
            "id": sid,
            "index": idx,
            "scenes": int(scenes_m.group(1)) if scenes_m else 1,
            "zag_len": len(zag_text),
            "ill_row": bool(ILL_ROW_RE.search(chunk)),
            "copy_zone": bool(COPY_ZONE_RE.search(chunk)),
            "n_blk": len(tips),
            "n_dokazatelstvo": sum(1 for t in tips if t == "dokazatelstvo"),
            "vse_narrativ": bool(tips) and all(t == "narrativ" for t in tips),
            "chunk_len": len(chunk),
        })
        idx += 1
    return out


def _vybrat_harakternye(slaidy):
    """Один представитель на категорию — эвристика, не список id. Пересечения
    легальны (слайд может быть и «плотный», и «с иллюстрацией у кромки») —
    захід просил кадр НА КАЖДЫЙ характерный случай, не гарантировал их
    непересечение."""
    vybor = {}
    s_dok = [s for s in slaidy if s["n_dokazatelstvo"] > 0]
    if s_dok:
        vybor["plotnyj-s-dokazatelstvom"] = max(s_dok, key=lambda s: s["chunk_len"])
    # `copy_zone` — отсекает служебные слайды (обложка/финал/разделитель): у них
    # НЕТ `.zone.copy` вовсе (свой `_wrap`/`_thx-wrap`/`_head`), Э3 их не касается,
    # а «разреженный»/«из одних нарративов» без фильтра ловили именно их (замерено
    # первым прогоном инструмента: получил `oblozhka`/`finalnyj` вместо контентных).
    s_text = [s for s in slaidy if s["copy_zone"] and not s["ill_row"] and s["chunk_len"] > 200]
    if s_text:
        vybor["razrezhennyj"] = min(s_text, key=lambda s: s["chunk_len"])
    s_ill = [s for s in slaidy if s["ill_row"]]
    if s_ill:
        vybor["illustraciya-u-kromki"] = s_ill[len(s_ill) // 2]
    # «из одних нарративов» — не «ни одного .blk» (у КАЖДОГО контентного слайда
    # есть хотя бы один `.blk`, словарь тегов `_bloki_slajda`), а ВСЕ теги блоков
    # slide'а это `data-tip="narrativ"` (второй тег словаря, наряду с opredelenie/
    # utverzhdenie/primer/dokazatelstvo — снят грепом `data-tip=` по собранной деке).
    s_narr = [s for s in slaidy if s["copy_zone"] and s["vse_narrativ"]]
    if s_narr:
        vybor["odni-narrativy"] = max(s_narr, key=lambda s: s["chunk_len"])
    s_zag = [s for s in slaidy if s["zag_len"] > 0]
    if s_zag:
        vybor["dlinnyj-zagolovok"] = max(s_zag, key=lambda s: s["zag_len"])
    s_sc = [s for s in slaidy if s["scenes"] > 1]
    if s_sc:
        vybor["so-scenami"] = max(s_sc, key=lambda s: s["scenes"])
    return vybor


def skrinshotit(dist_html, vybor, out_dir, lek_name):
    from playwright.sync_api import sync_playwright
    out_dir.mkdir(parents=True, exist_ok=True)
    sdelano = []
    url_base = "file://%s" % dist_html.resolve()
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="chrome", headless=True)
        page = b.new_page(viewport={"width": HOLST_W, "height": HOLST_H}, device_scale_factor=1)
        for kategoriya, s in vybor.items():
            scenes = [1, s["scenes"]] if kategoriya == "so-scenami" and s["scenes"] > 1 else [None]
            for scene in scenes:
                url = "%s?only=%d" % (url_base, s["index"])
                if scene is not None:
                    url += "&scene=%d" % scene
                page.goto(url)
                page.wait_for_timeout(200)  # шрифты/KaTeX/фонты — тот же приём, что document.fonts.ready
                fname = "%s_%s_%s%s.png" % (lek_name, kategoriya, s["id"],
                                             ("_scene%d" % scene) if scene is not None else "")
                fpath = out_dir / fname
                page.screenshot(path=str(fpath))
                sdelano.append((kategoriya, s["id"], s["index"], scene, fpath))
        b.close()
    return sdelano


def main():
    ap = argparse.ArgumentParser(description="Скриншоты характерных слайдов дека (Э6 захода pravila-kadra)")
    ap.add_argument("lekcia", help="папка лекции (содержит slajdy/, brief.md)")
    ap.add_argument("--out", help="папка для PNG (по умолчанию <лекция>/../_kadry_tmp/)")
    ap.add_argument("--dist", help="путь готового index.html — если задан, дек НЕ пересобирается")
    args = ap.parse_args()

    lekcia = Path(args.lekcia)
    # rc=2 — позвали НЕВЕРНО (нет папки/файла), не «инструмент нашёл проблему».
    # Снаружи иначе неотличимо от опечатки в пути (§5 GIT-disciplina, RC_MISUSE).
    if not lekcia.is_dir():
        print("ОШИБКА ВЫЗОВА: папки лекции нет: %s" % lekcia, file=sys.stderr)
        return 2
    lek_name = lekcia.name
    out_dir = Path(args.out) if args.out else lekcia.parent / "_kadry_tmp"

    if args.dist:
        dist_html = Path(args.dist)
        if not dist_html.exists():
            print("ОШИБКА ВЫЗОВА: --dist указан, но файла нет: %s" % dist_html, file=sys.stderr)
            return 2
    else:
        dist_html = lekcia / "dist" / "index.html"
        try:
            log = sobrat_dek(lekcia, dist_html)
        except RuntimeError as e:
            print("ОШИБКА: %s" % e, file=sys.stderr)
            return 1
        print(log.strip())

    html = dist_html.read_text(encoding="utf-8")
    slaidy = razobrat_slaidy(html)
    if not slaidy:
        print("ОШИБКА: в %s не нашлось ни одного слайда без data-skip" % dist_html, file=sys.stderr)
        return 1
    vybor = _vybrat_harakternye(slaidy)
    if not vybor:
        print("ОШИБКА: ни одна категория характерных слайдов не нашла кандидата "
              "(деку из %d слайдов не удалось классифицировать)" % len(slaidy), file=sys.stderr)
        return 1

    sdelano = skrinshotit(dist_html, vybor, out_dir, lek_name)

    print("\nкадры (%d шт.) в %s:" % (len(sdelano), out_dir))
    for kategoriya, sid, idx, scene, fpath in sdelano:
        scene_str = (" сцена %d" % scene) if scene is not None else ""
        print("  %-24s slide=%-28s index=%-3d%-10s -> %s" % (kategoriya, sid, idx, scene_str, fpath.name))
    nedostalos = sorted(set(["plotnyj-s-dokazatelstvom", "razrezhennyj", "illustraciya-u-kromki",
                              "odni-narrativy", "dlinnyj-zagolovok", "so-scenami"]) - set(vybor))
    if nedostalos:
        print("\nНЕ НАЙДЕНО кандидатов для категорий: %s (в этой лекции таких слайдов нет — не брак "
              "инструмента, отбор эвристикой)" % ", ".join(nedostalos))
    return 0


if __name__ == "__main__":
    sys.exit(main())
