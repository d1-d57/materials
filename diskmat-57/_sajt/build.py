#!/usr/bin/env python3
"""Сайт курса: god.json + rasskaz.json + sajt.json → index.html.

Единственный дом раскладки года — god.json. Карта года, программа и раздел
материалов собираются из него; HTML руками не правится, правится источник.

    python3 build.py            # собрать
    python3 build.py --proverit # собрать и сверить суммы часов
"""
import html
import json
import sys
from pathlib import Path

DOM = Path(__file__).resolve().parent
VYHOD = DOM / "index.html"

CVETA = {
    "A": ("#c8622f", "арифметика"),
    "K": ("#2f6fa8", "комбинаторика"),
    "V": ("#4b8b3b", "вероятность"),
    "D": ("#7a4b9c", "дискретная математика"),
    "O": ("#8a8071", "разгон"),
}


def e(t):
    return html.escape(str(t), quote=False)


def bez_tochki(t):
    """Подписи и перечни точкой не заканчиваются."""
    return t.rstrip().rstrip(".")


def stil():
    peremennye = "\n".join(f"  --d-{k}: {v[0]};" for k, v in CVETA.items())
    return f"""
:root {{
{peremennye}
  --tekst: #1d1b18; --tiho: #6d6459; --linia: #ddd6ca;
  --fon: #faf7f1; --karta: #fff;
}}
* {{ box-sizing: border-box }}
body {{ margin: 0; background: var(--fon); color: var(--tekst);
  font: 17px/1.6 -apple-system, "Segoe UI", "PT Sans", sans-serif;
  -webkit-text-size-adjust: 100% }}
.wrap {{ max-width: 860px; margin: 0 auto; padding: 0 20px 80px }}
header {{ padding: 56px 0 28px; border-bottom: 2px solid var(--tekst) }}
h1 {{ font-size: 34px; margin: 0 0 6px; letter-spacing: -.01em }}
.shapka-sub {{ color: var(--tiho); font-size: 16px }}
nav {{ position: sticky; top: 0; z-index: 5; background: var(--fon);
  border-bottom: 1px solid var(--linia); padding: 10px 0; margin-bottom: 34px;
  display: flex; gap: 20px; flex-wrap: wrap; font-size: 15px }}
nav a {{ color: var(--tiho); text-decoration: none; border-bottom: 1px solid transparent }}
nav a:hover {{ color: var(--tekst); border-bottom-color: var(--tekst) }}
h2 {{ font-size: 25px; margin: 52px 0 4px }}
h2 + .pod {{ color: var(--tiho); font-size: 15px; margin: 0 0 22px }}
h3 {{ font-size: 18px; margin: 30px 0 8px }}
.rasskaz p {{ margin: 0 0 .45em }}
.rasskaz p:last-child {{ margin-bottom: 0 }}
.lid {{ font-size: 19px; color: var(--tiho); margin: 0 0 8px }}

.legenda {{ display: flex; gap: 16px; flex-wrap: wrap; font-size: 14px;
  color: var(--tiho); margin: 0 0 18px }}
.sw {{ display: inline-block; width: 11px; height: 11px; border-radius: 2px;
  margin-right: 5px; vertical-align: baseline }}

.chetvert {{ display: flex; align-items: baseline; gap: 12px; margin: 34px 0 10px;
  padding-bottom: 6px; border-bottom: 1px solid var(--tekst); font-size: 15px }}
.chetvert b {{ font-size: 17px }}
.chetvert .daty {{ color: var(--tiho) }}
.chetvert .ch {{ margin-left: auto; color: var(--tiho) }}

details.blok {{ border-radius: 4px; margin-bottom: 5px; overflow: hidden;
  background: var(--karta); border-left: 5px solid var(--linia) }}
details.blok > summary {{ list-style: none; cursor: pointer; padding: 11px 14px;
  display: flex; align-items: baseline; gap: 12px }}
details.blok > summary::-webkit-details-marker {{ display: none }}
.imya {{ font-weight: 600; min-width: 132px }}
.tema {{ color: var(--tiho); font-size: 14.5px; flex: 1 }}
.chasy {{ color: var(--tiho); font-size: 14px; white-space: nowrap; padding-left: 8px }}
.nutro {{ padding: 4px 14px 16px 14px; border-top: 1px solid var(--linia) }}
.nutro dl {{ margin: 12px 0 0; display: grid;
  grid-template-columns: minmax(120px, 190px) 1fr;
  gap: 4px 16px; font-size: 15px; overflow-wrap: anywhere }}
.nutro dt {{ font-weight: 600 }}
.nutro dd {{ margin: 0; color: #3c372f }}
.opornye, .istochniki {{ margin-top: 14px; font-size: 14.5px; color: var(--tiho) }}
.opornye b, .istochniki b {{ color: var(--tekst); font-weight: 600 }}

.kruzhok {{ background: #f1ece1; border-left-color: #b9ad97 }}
.kr {{ display: flex; align-items: baseline; gap: 12px; padding: 7px 14px;
  margin-bottom: 5px; font-size: 14.5px; color: var(--tiho);
  border-left: 5px solid transparent; background: #f3f0e9; border-radius: 4px }}
.kr.chetvertnaya {{ background: #ece7dc; color: var(--tekst) }}
.kr .imya {{ font-weight: 500 }}

table.utok {{ border-collapse: collapse; font-size: 13px; width: 100%; margin-top: 8px }}
table.utok th {{ font-weight: 500; color: var(--tiho); text-align: center;
  padding: 4px 2px; vertical-align: bottom; font-size: 12px; line-height: 1.25 }}
table.utok th.metod {{ text-align: left; width: 200px }}
table.utok td {{ text-align: center; padding: 5px 2px; border-top: 1px solid var(--linia) }}
table.utok td.metod {{ text-align: left; color: var(--tekst) }}
.dom {{ display: inline-block; width: 13px; height: 13px; border-radius: 50% }}
.vozvrat {{ display: inline-block; width: 6px; height: 6px; border-radius: 50%;
  background: #b6ad9d }}
.obertka-utka {{ overflow-x: auto }}

.material {{ display: flex; gap: 12px; align-items: baseline; padding: 9px 0;
  border-bottom: 1px solid var(--linia); font-size: 15px }}
.material .pusto {{ color: #a79d8c; margin-left: auto; font-size: 14px }}
.zaglushka {{ color: var(--tiho); margin: 0 0 18px }}

footer {{ margin-top: 60px; padding-top: 16px; border-top: 1px solid var(--linia);
  color: var(--tiho); font-size: 14px }}

@media (max-width: 700px) {{
  body {{ font-size: 16px }}
  h1 {{ font-size: 27px }}
  .wrap {{ padding: 0 15px 60px }}
  details.blok > summary {{ flex-wrap: wrap; gap: 4px 10px }}
  .imya {{ min-width: 0 }}
  .tema {{ flex-basis: 100%; font-size: 14px }}
  .nutro dl {{ grid-template-columns: 1fr; gap: 2px }}
  .nutro dt {{ margin-top: 8px }}
  table.utok th.metod {{ width: 130px }}
}}
"""


def sobrat_blok(b):
    cvet = CVETA[b["domen"]][0]
    stroki = "".join(
        f"<dt>{e(p['tema'])}</dt><dd>{e(p['chto'])}</dd>" for p in b["karta"])
    nutro = [f"<dl>{stroki}</dl>"]
    if b.get("opornye"):
        nutro.append(
            f'<p class="opornye"><b>Опорные задачи.</b> {e(bez_tochki(b["opornye"]))}</p>')
    if b.get("istochniki"):
        nutro.append(f'<p class="istochniki"><b>Источники.</b> {e(b["istochniki"])}</p>')
    styk = ' <span class="chasy">· на стыке доменов</span>' if b["na-styke"] else ""
    return (
        f'<details class="blok" style="border-left-color:{cvet}">'
        f'<summary><span class="imya">{e(b["imya"])}</span>'
        f'<span class="tema">{e(b["podzag"])}</span>'
        f'<span class="chasy">{b["chasy"]} ч</span></summary>'
        f'<div class="nutro">{"".join(nutro)}{styk}</div></details>'
    )


def sobrat_kruzhok(k):
    stroki = "".join(
        f"<dt>{e(p['tema'])}</dt><dd>{e(p['chto'])}</dd>" for p in k["karta"])
    return (
        '<details class="blok kruzhok">'
        f'<summary><span class="imya">Кружок</span>'
        f'<span class="tema">{e(k["podzag"])}</span>'
        f'<span class="chasy">{k["chasy"]} ч</span></summary>'
        f'<div class="nutro"><dl>{stroki}</dl></div></details>'
    )


def sobrat_kartu(god):
    kuski = []
    for ch in god["chetverti"]:
        kuski.append(
            f'<div class="chetvert"><b>{e(ch["nomer"])} четверть</b>'
            f'<span class="daty">{e(ch["daty"])}</span>'
            f'<span class="ch">{ch["chasy"]} ч</span></div>')
        for el in ch["elementy"]:
            if el["tip"] == "blok":
                kuski.append(sobrat_blok(el))
            elif el["tip"] == "kruzhok":
                kuski.append(sobrat_kruzhok(el))
            else:
                klass = "kr chetvertnaya" if el.get("chetvertnaya") else "kr"
                kuski.append(
                    f'<div class="{klass}"><span class="imya">{e(el["imya"])}</span>'
                    f'<span class="tema">{e(el["chto"])}</span>'
                    f'<span class="chasy">{el["chasy"]} ч</span></div>')
    return "\n".join(kuski)


def sobrat_utok(god):
    bloki = [(e_["imya"], e_["domen"]) for ch in god["chetverti"]
             for e_ in ch["elementy"] if e_["tip"] == "blok"]
    shapka = "".join(
        f'<th>{e(imya.replace(" ", "<br>"))}</th>'.replace("&lt;br&gt;", "<br>")
        for imya, _ in bloki)
    stroki = []
    for m in god["utok"]:
        yach = []
        for imya, domen in bloki:
            mesto = m["mesta"].get(imya)
            if mesto == "dom":
                yach.append(f'<td><i class="dom" style="background:{CVETA[domen][0]}"></i></td>')
            elif mesto == "vozvrat":
                yach.append('<td><i class="vozvrat"></i></td>')
            else:
                yach.append("<td></td>")
        stroki.append(f'<tr><td class="metod">{e(m["imya"])}</td>{"".join(yach)}</tr>')
    return (f'<div class="obertka-utka"><table class="utok">'
            f'<tr><th class="metod"></th>{shapka}</tr>{"".join(stroki)}</table></div>')


def sobrat_rasskaz(r):
    kuski = [f'<p class="lid">{e(r["lid"])}</p>']
    for razdel in r["razdely"]:
        kuski.append(f'<h3>{e(razdel["imya"])}</h3>')
        kuski.extend(f"<p>{e(a)}</p>" for a in razdel["abzacy"])
    return f'<div class="rasskaz">{"".join(kuski)}</div>'


def sobrat_materialy(god, nastr):
    stroki = []
    for ch in god["chetverti"]:
        for el in ch["elementy"]:
            if el["tip"] == "blok":
                stroki.append(
                    f'<div class="material"><span class="imya">{e(el["imya"])}</span>'
                    f'<span class="tema">{e(el["podzag"])}</span>'
                    f'<span class="pusto">листок появится</span></div>')
    return (f'<p class="zaglushka">{e(bez_tochki(nastr["materialy_zaglushka"]))}</p>'
            + "".join(stroki))


def sobrat(god, rasskaz, nastr):
    legenda = "".join(
        f'<span><i class="sw" style="background:{cvet}"></i>{e(imya)}</span>'
        for cvet, imya in CVETA.values())

    razdely = []
    menyu = []
    if nastr["programma_vidna"]:
        menyu.append('<a href="#kak-ustroen">Как устроен курс</a>')
        razdely.append(
            f'<section id="kak-ustroen"><h2>{e(rasskaz["zagolovok"])}</h2>'
            f'{sobrat_rasskaz(rasskaz)}</section>')
    menyu.append('<a href="#karta">Карта года</a>')
    razdely.append(
        f'<section id="karta"><h2>Карта года</h2>'
        f'<p class="pod">{e(god["kurs"]["podzagolovok"])}</p>'
        f'<div class="legenda">{legenda}</div>{sobrat_kartu(god)}'
        f'<p class="istochniki">{e(god["snoska"])}</p></section>')
    if nastr["programma_vidna"]:
        menyu.append('<a href="#metody">Методы</a>')
        razdely.append(
            '<section id="metody"><h2>Методы сквозь год</h2>'
            '<p class="pod">кружок — блок, где метод дома; точка — возврат '
            'на чужом материале</p>' + sobrat_utok(god) + "</section>")
    if nastr["materialy_vidny"]:
        menyu.append('<a href="#materialy">Материалы</a>')
        razdely.append(
            '<section id="materialy"><h2>Листки и домашние задания</h2>'
            + sobrat_materialy(god, nastr) + "</section>")

    return f"""<!doctype html>
<html lang="ru">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(nastr['titul'])} — {e(nastr['god'])}</title>
<style>{stil()}</style>
<div class="wrap">
<header>
  <h1>{e(nastr['titul'])}</h1>
  <div class="shapka-sub">{e(nastr['shkola'])} · {e(nastr['god'])} · два часа в неделю плюс кружок</div>
</header>
<nav>{''.join(menyu)}</nav>
{''.join(razdely)}
<footer>{e(nastr['podval'])}</footer>
</div>
</html>
"""


def proverit(god):
    itogi = {"blok": 0, "kontrolnaya": 0, "kruzhok": 0, "vne-setki": 0}
    for ch in god["chetverti"]:
        for el in ch["elementy"]:
            itogi[el["tip"]] += el["chasy"]
    v_setke = itogi["blok"] + itogi["kontrolnaya"]
    po_chetvertyam = sum(ch["chasy"] for ch in god["chetverti"])
    bedy = []
    if v_setke != po_chetvertyam:
        bedy.append(f"в сетке {v_setke} ч, а по четвертям заявлено {po_chetvertyam} ч")
    if v_setke != 66:
        bedy.append(f"уроков в сетке {v_setke}, а год считается 66")
    for m in god["utok"]:
        if "dom" not in m["mesta"].values():
            bedy.append(f"метод «{m['imya']}» без дома")
    for beda in bedy:
        print("🔴", beda)
    print(f"содержательных {itogi['blok']} ч · контроля {itogi['kontrolnaya']} ч · "
          f"кружка {itogi['kruzhok']} ч · вне сетки {itogi['vne-setki']} ч")
    return not bedy


def main():
    god = json.loads((DOM / "god.json").read_text(encoding="utf-8"))
    rasskaz = json.loads((DOM / "rasskaz.json").read_text(encoding="utf-8"))
    nastr = json.loads((DOM / "sajt.json").read_text(encoding="utf-8"))
    VYHOD.write_text(sobrat(god, rasskaz, nastr), encoding="utf-8")
    print(f"собрано → {VYHOD.name}, {VYHOD.stat().st_size // 1024} КБ")
    if "--proverit" in sys.argv:
        return 0 if proverit(god) else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
