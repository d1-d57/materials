#!/usr/bin/env python3
"""Одноразовый перенос: INFOGRAFIKA-goda.html → god.json.

Написан на один запуск, чтобы раскладка года переехала из вёрстки в данные
без ручного перепечатывания. После переезда правится god.json, а не HTML;
этот файл остаётся как след того, откуда данные взялись.
"""
import json
import re
import sys
from pathlib import Path

ARKA = Path(__file__).resolve().parents[1] / "2026-08-18_logika-goda-7"
SRC = ARKA / "INFOGRAFIKA-goda.html"
OUT = Path(__file__).resolve().parent / "god.json"

DOMENY = {"A": "арифметика", "K": "комбинаторика", "V": "вероятность",
          "D": "дискретная математика", "O": "разгон"}


def snyat_kartu(kusok):
    """dl-список «понятие → что внутри» и две подписи под ним."""
    karta = [{"tema": dt.strip(), "chto": dd.strip()}
             for dt, dd in re.findall(r"<dt>(.*?)</dt><dd>(.*?)</dd>", kusok, re.S)]
    opornye = re.search(r'<div class="ex">(.*?)</div>', kusok, re.S)
    istochniki = re.search(r'<div class="sr">(.*?)</div>', kusok, re.S)
    return karta, opornye, istochniki


def razobrat_element(tag, telo):
    if tag == "kr":
        klass = re.search(r'class="kr([^"]*)"', telo).group(1).strip()
        imya = re.search(r'<span class="nm">(.*?)</span>', telo).group(1)
        chasy = int(re.search(r'<span class="hr">(\d+)</span>', telo).group(1))
        chto = re.search(r'<span class="tt">(.*?)</span>', telo).group(1)
        return {"tip": "vne-setki" if "out" in klass else "kontrolnaya",
                "imya": imya, "chasy": chasy, "chto": chto,
                "chetvertnaya": "big" in klass}

    klass = re.search(r'class="row([^"]*)"', telo).group(1).strip()
    imya = re.search(r'<span class="nm">(.*?)</span>', telo).group(1)
    chasy = int(re.search(r'<span class="hr">(\d+)</span>', telo).group(1))
    podzag = re.search(r'<span class="tt">(.*?)</span>', telo, re.S).group(1).strip()
    karta, opornye, istochniki = snyat_kartu(telo)

    if "club" in klass:
        return {"tip": "kruzhok", "chasy": chasy, "podzag": podzag, "karta": karta}

    domen = re.search(r'data-d="([A-Z])"', telo).group(1)
    blok = {"tip": "blok", "imya": imya, "chasy": chasy, "domen": domen,
            "na-styke": bool(re.search(r"tri\d", klass)),
            "podzag": podzag, "karta": karta}
    if opornye:
        blok["opornye"] = opornye.group(1).replace("Опорные: ", "").strip()
    if istochniki:
        blok["istochniki"] = istochniki.group(1).strip()
    return blok


def razobrat_chetverti(html):
    """Четверти идут подряд; всё между двумя .qt принадлежит первой из них."""
    chetverti = []
    kuski = re.split(r'<div class="qt">', html)[1:]
    for kusok in kuski:
        kusok = kusok.split("<!--\n  СЛУЖЕБНОЕ")[0]
        nom = re.search(r"<b>(.*?) четверть</b>", kusok).group(1)
        daty = re.search(r"</b><span>(.*?)</span>", kusok).group(1)
        chasy = int(re.search(r'<span class="h">(\d+) ч</span>', kusok).group(1))
        elementy = []
        for m in re.finditer(
                r'(<details class="row.*?</details>)|(<div class="kr.*?</div>)',
                kusok, re.S):
            telo = m.group(0)
            elementy.append(razobrat_element("kr" if m.group(2) else "row", telo))
        chetverti.append({"nomer": nom, "daty": daty, "chasy": chasy,
                          "elementy": elementy})
    return chetverti


def razobrat_utok(html, imena_blokov):
    """Второй экран: метод × блок, «дом» или «возврат»."""
    tabl = html.split("<h1>Методы сквозь год</h1>")[1]
    metody = []
    for stroka in re.findall(r'<tr><td class="lead">(.*?)</tr>', tabl, re.S):
        imya = re.match(r"(.*?)</td>", stroka, re.S).group(1).strip()
        # открывающий <td class="lead"> уже съеден регуляркой строки,
        # поэтому первый найденный td — это уже первый блок года
        yacheyki = re.findall(r"<td[^>]*>(.*?)</td>", stroka, re.S)
        mesta = {}
        for i, y in enumerate(yacheyki):
            if "home" in y:
                mesta[imena_blokov[i]] = "dom"
            elif "dot" in y:
                mesta[imena_blokov[i]] = "vozvrat"
        metody.append({"imya": imya, "mesta": mesta})
    return metody


def main():
    html = SRC.read_text(encoding="utf-8")
    chetverti = razobrat_chetverti(html)
    imena_blokov = [e["imya"] for ch in chetverti for e in ch["elementy"]
                    if e["tip"] == "blok"]
    god = {
        "kurs": {
            "nazvanie": "Спецмат, 7 класс",
            "podzagolovok": re.search(r'<p class="sub">(.*?)</p>', html).group(1),
            "domeny": DOMENY,
        },
        "chetverti": chetverti,
        "utok": razobrat_utok(html, imena_blokov),
        "snoska": re.search(r'<div class="foot">\s*(.*?)\s*</div>', html, re.S).group(1),
        "sluzhebnoe": re.search(r"СЛУЖЕБНОЕ.*?автора карты\.\s*(.*?)-->", html, re.S)
                        .group(1).strip(),
    }
    OUT.write_text(json.dumps(god, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")

    chasy_blokov = sum(e["chasy"] for ch in god["chetverti"] for e in ch["elementy"]
                       if e["tip"] == "blok")
    chasy_kruzhka = sum(e["chasy"] for ch in god["chetverti"] for e in ch["elementy"]
                        if e["tip"] == "kruzhok")
    chasy_kr = sum(e["chasy"] for ch in god["chetverti"] for e in ch["elementy"]
                   if e["tip"] == "kontrolnaya")
    vne = sum(e["chasy"] for ch in god["chetverti"] for e in ch["elementy"]
              if e["tip"] == "vne-setki")
    print(f"блоков {len(imena_blokov)} · содержательных {chasy_blokov} ч · "
          f"контроля {chasy_kr} ч · кружка {chasy_kruzhka} ч · вне сетки {vne} ч")
    print(f"в сетке {chasy_blokov + chasy_kr} ч · методов в утке {len(god['utok'])}")
    return 0 if (chasy_blokov == 51 and chasy_kr == 15 and chasy_kruzhka == 33) else 1


if __name__ == "__main__":
    sys.exit(main())
