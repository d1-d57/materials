#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ПРОГОН: перебор по осям → баллы → распределение. Один вход, всё остальное считается.

Устройство перебора — сперва ось за осью при остальных на нейтрали (так виден
вклад ОДНОЙ переменной и выполняется клауза 3 критерия готовности: не менее трёх
вариантов по каждой оси), затем финальные комбинации из победителей.

Печатает РАСПРЕДЕЛЕНИЕ баллов по вариантам, а не только победителя: признак, по
которому все варианты получили одинаково, — мёртвый, и он называется поимённо.
"""
import json
import os
import re
import sys

ZDES = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ZDES)
import shema      # noqa: E402
import zamer      # noqa: E402
import priznaki   # noqa: E402

ZONA = os.path.dirname(ZDES)
BAZA = os.path.join(ZONA, "baza", "L2-blocked.html")
VAR = os.path.join(ZONA, "varianty")
SNIM = os.path.join(ZONA, "skrinshoty")
PAPER = (247, 244, 236)   # --paper #F7F4EC
INK = (48, 51, 49)        # --ink   #303331

# кадры, на которых схема реально нагружена (§Э4 захода)
KADRY_SYEMKI = [
    ("dvojstvennyj-bazis", "с доказательством: определение+пример+утверждение+доказательство"),
    ("dvojstvennoe-prostranstvo", "три блока, все статусные — красный флаг §8.1 спецификации"),
    ("fundamentalnaya-gruppa", "иллюстрация у кромки + три блока"),
    ("itogi", "ИЗ ОДНИХ НАРРАТИВОВ — средств быть не должно вовсе"),
    ("centr-gruppy", "доказательство + иллюстрация"),
]
NARRATIV_TOLKO = {"itogi", "napominanie", "anons-dvojstvennogo", "anons-retraktov",
                  "teorema-brauera"}

KONTROL = dict(l="Л0-net", d="Д0-net", z="З2-0.68", s="С-net", o="О0-baza")
SNIMKI = [c[0] for c in KADRY_SYEMKI]


def zagolovki_slajdov():
    h = open(BAZA, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r'<section class="slide" id="([^"]+)"[^>]*>(.{0,3000}?)'
                         r'<div class="zagolovok">(.*?)</div>', h, re.S):
        out[m.group(1)] = re.sub(r"<[^>]+>", " ", m.group(3))
    return out


def kontrast_zagolovka(kadry):
    for k in kadry:
        for b in k["bloki"]:
            z = b.get("zag")
            if z and z["h"] > 1:
                c = zamer._rgb(z["color"])
                if not c:
                    return None
                a = c[3] * z["op"]
                return zamer.kontrast(zamer.svesti(c, PAPER, a), PAPER)
    return None


def ocenit(kadry, kontrol, shtrih, titry, cena=None, cena_kontrolya=None):
    b, det = {}, {}
    b["П1"], det["П1"] = priznaki.p1(kadry)
    b["П2"], det["П2"] = priznaki.p2(kadry)
    b["П3"], det["П3"] = priznaki.p3(kadry, shtrih)
    b["П4"], det["П4"] = priznaki.p4(kadry, kontrol, cena, cena_kontrolya)
    kz = kontrast_zagolovka(kadry)
    b["П5"], det["П5"] = priznaki.p5(kadry, kz, zamer.kontrast(INK, PAPER))
    b["П6"], det["П6"] = priznaki.p6(kadry, titry)
    b["П7"], det["П7"] = priznaki.p7(kadry, NARRATIV_TOLKO)
    b["П8"], det["П8"] = priznaki.p8(kadry)
    b["П9"], det["П9"] = priznaki.p9(kadry)
    return b, det


def summa(b):
    est = [x for x in b.values() if x is not None]
    return sum(est), len(est)


def stroka(imya, b, s, n):
    return "%-16s %s   %2d/%2d" % (
        imya, "  ".join((" –" if b["П%d" % i] is None else " %d" % b["П%d" % i])
                        for i in range(1, 10)), s, n * 3)


def main():
    titry = zagolovki_slajdov()
    os.makedirs(VAR, exist_ok=True)
    # страница-носитель: пустой <style id="overlay">, дальше меняется на месте
    nositel = zamer.sobrat(BAZA, "", os.path.join(VAR, "_nositel.html"))
    ses = zamer.Sessiya(nositel)
    try:
        print("═══ КОНТРОЛЬ В0: обёртка без единого средства ═══")
        kontrol = ses.variant(shema.overlay(KONTROL), SNIMKI,
                              os.path.join(SNIM, "В0-kontrol"))
        cena0 = ses.cena_v_kegle()
        print("   кадров измерено:", len(kontrol))
        print("   контроль: слайдов, уже не влезающих в свой кегль:",
              sum(1 for x in cena0 if (x["s"] or 1) < 0.999))
        shtrih = priznaki.shtrih_iz_skrinshota(
            os.path.join(SNIM, "В0-kontrol", "dvojstvennyj-bazis.png"),
            oblast=(160, 180, 1280, 700))
        print("   штрих шрифта тела на кадре, px:", shtrih)
        print("   контраст тела к холсту:", round(zamer.kontrast(INK, PAPER), 2))
        print()

        osi = [("1 · линейка центрального блока", "l", list(shema.LINEJKA)),
               ("2 · доказательство", "d", list(shema.DOKAZ)),
               ("3a · вид тихого заголовка", "z", list(shema.ZAGOLOVOK)),
               ("3b · что печатать в заголовке", "s", list(shema.SODERZHIMOE)),
               ("4 · межблочный отступ", "o", list(shema.OTSTUP))]

        itog = {}
        shapka = "%-16s %s   СУММА" % ("вариант", "  ".join("П%d" % i for i in range(1, 10)))
        for imya_osi, klyuch, znacheniya in osi:
            print("═══ ОСЬ %s ═══" % imya_osi)
            print(shapka)
            for zn in znacheniya:
                v = dict(shema.NEJTRAL); v[klyuch] = zn
                kadry = ses.variant(shema.overlay(v))
                b, det = ocenit(kadry, kontrol, shtrih, titry,
                                ses.cena_v_kegle(), cena0)
                s, n = summa(b)
                itog["%s|%s" % (klyuch, zn)] = {"bally": b, "detali": det, "summa": s}
                print(stroka(zn, b, s, n))
            print()

        json.dump(itog, open(os.path.join(ZONA, "bally-po-osyam.json"), "w",
                             encoding="utf-8"), ensure_ascii=False, indent=1)
        print("баллы по осям сохранены: bally-po-osyam.json")
    finally:
        ses.close()


if __name__ == "__main__":
    main()
