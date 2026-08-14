#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ФИНАЛЬНЫЕ КОМБИНАЦИИ — собираются из победителей осей, снимаются кадрами.

Победитель оси — не всегда победитель схемы: признаки П1 и П4 считаются по
кадру ЦЕЛИКОМ, а значит средства складываются. Поэтому финал считается заново,
на комбинациях, и на них же снимаются кадры для глаза.
"""
import json
import os
import sys

ZDES = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ZDES)
import shema      # noqa: E402
import zamer      # noqa: E402
import progon     # noqa: E402

FINAL = {
    # имя                        линейка         доказ.     заголовок     что       отступ
    "В1-tihaya":    dict(l="Л2-тонкая",    d="Д3-0.86", z="З6-pol24", s="С-slovo", o="О5-snizu"),
    "В2-srednyaya": dict(l="Л3-srednyaya", d="Д3-0.86", z="З6-pol24", s="С-slovo", o="О5-snizu"),
    "В3-korotkaya": dict(l="Л4-korotkaya", d="Д3-0.86", z="З6-pol24", s="С-slovo", o="О5-snizu"),
    "В4-plyum":     dict(l="Л6-plyum",     d="Д3-0.86", z="З6-pol24", s="С-slovo", o="О5-snizu"),
    "В5-mysl":      dict(l="Л3-srednyaya", d="Д3-0.86", z="З6-pol24", s="С-mysl",  o="О5-snizu"),
    "В6-veb":       dict(l="Л5-veb",       d="Д4-0.80", z="З3-0.78",  s="С-slovo", o="О1-sverh"),
    "В7-bez-slova": dict(l="Л3-srednyaya", d="Д3-0.86", z="З6-pol24", s="С-net",   o="О5-snizu"),
    "В8-bez-pola":  dict(l="Л3-srednyaya", d="Д3-0.86", z="З3-0.78",  s="С-slovo", o="О5-snizu"),
    "В9-snizu-2":   dict(l="Л3-srednyaya", d="Д3-0.86", z="З6-pol24", s="С-slovo", o="О6-snizu-2"),
    "В10-0.90":     dict(l="Л3-srednyaya", d="Д2-0.90", z="З6-pol24", s="С-slovo", o="О5-snizu"),
}


def main():
    titry = progon.zagolovki_slajdov()
    nositel = zamer.sobrat(progon.BAZA, "", os.path.join(progon.VAR, "_nositel.html"))
    ses = zamer.Sessiya(nositel)
    try:
        kontrol = ses.variant(shema.overlay(progon.KONTROL), progon.SNIMKI,
                              os.path.join(progon.SNIM, "В0-kontrol"))
        cena0 = ses.cena_v_kegle()
        shtrih = zamer and __import__("priznaki").shtrih_iz_skrinshota(
            os.path.join(progon.SNIM, "В0-kontrol", "dvojstvennyj-bazis.png"),
            oblast=(160, 180, 1280, 700))
        itog = {}
        print("%-16s %s   СУММА   цена кегля ср/худш %%" %
              ("схема", "  ".join("П%d" % i for i in range(1, 10))))
        for imya, v in FINAL.items():
            css = shema.overlay(v)
            zamer.sobrat(progon.BAZA, css, os.path.join(progon.VAR, imya + ".html"))
            kadry = ses.variant(css, progon.SNIMKI, os.path.join(progon.SNIM, imya))
            b, det = progon.ocenit(kadry, kontrol, shtrih, titry,
                                   ses.cena_v_kegle(), cena0)
            s, n = progon.summa(b)
            itog[imya] = {"variant": v, "bally": b, "detali": det, "summa": s,
                          "iz": n * 3}
            print("%s   %s / %s" % (
                progon.stroka(imya, b, s, n),
                det["П4"].get("цена в кегле, среднее по деке %"),
                det["П4"].get("цена в кегле, худший слайд %")))
        json.dump(itog, open(os.path.join(progon.ZONA, "bally-final.json"), "w",
                             encoding="utf-8"), ensure_ascii=False, indent=1)
        print("\nсохранено: bally-final.json · кадры: skrinshoty/<схема>/*.png")
    finally:
        ses.close()


if __name__ == "__main__":
    main()
