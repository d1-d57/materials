#!/usr/bin/env python3
"""build_listok.py — листок задач из банка.

Вход  — манифест (markdown: фронтматтер + список id задач).
Банк  — _fond/zadachi/bank/<id>.md, одна задача = один файл.
Выход — самодостаточный HTML в авторском стиле (бумага/чернила/рубрика).

    python3 _generator/build_listok.py <манифест.md> [-o out.html] [--lint]

Правило: HTML — артефакт. Правится банк или манифест, не выход.
Канон формата — _fond/zadachi/bank/README.md
"""
from __future__ import annotations
import argparse, html, re, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BANK = REPO / "_fond" / "zadachi" / "bank"

# какие секции задачи попадают в вид при каком режиме показа
REZHIMY = {
    "usloviya":  [],
    "podskazki": ["Подсказка", "Ещё подсказка"],
    "otvety":    ["Ответ"],
    "polnyj":    ["Подсказка", "Ещё подсказка", "Ответ", "Решение"],
}
SPOJLER = {"Ещё подсказка", "Ответ", "Решение"}   # эти — под катом
OTKRYTO = {"Подсказка"}                            # эта — открытым текстом

# в манифесте секцию можно назвать латиницей: `- zhuki-5x5 | podskazka`
ALIASY = {"podskazka": "Подсказка", "eshchyo-podskazka": "Ещё подсказка",
          "otvet": "Ответ", "reshenie": "Решение"}


def imya_sekcii(s: str) -> str:
    s = s.strip()
    return ALIASY.get(s.lower(), s.capitalize())


def razobrat(text: str) -> tuple[dict, dict[str, str]]:
    """Файл → (фронтматтер, {секция: текст}). Секции — по '## '."""
    meta: dict[str, str] = {}
    if text.startswith("---"):
        konec = text.find("\n---", 3)
        if konec == -1:
            raise ValueError("фронтматтер не закрыт")
        for stroka in text[3:konec].strip().splitlines():
            if m := re.match(r"^([a-z_]+):\s*(.*)$", stroka.strip()):
                meta[m[1]] = m[2].strip()
        text = text[konec + 4:]
    sekcii: dict[str, str] = {}
    imya, buf = "", []
    for stroka in text.splitlines():
        if m := re.match(r"^##\s+(.+?)\s*$", stroka):
            if imya:
                sekcii[imya] = "\n".join(buf).strip()
            imya, buf = m[1], []
        else:
            buf.append(stroka)
    if imya:
        sekcii[imya] = "\n".join(buf).strip()
    return meta, sekcii


def v_html(tekst: str) -> str:
    """Абзацы + **жирный** + *курсив*. Больше ничего — намеренно."""
    out = []
    for abzac in re.split(r"\n\s*\n", tekst.strip()):
        s = html.escape(abzac.strip()).replace("\n", " ")
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", s)
        if s:
            out.append(s)
    return "".join(f"<p>{s}</p>" for s in out)


def zadacha_v_html(meta: dict, sekcii: dict[str, str], pokazat: list[str],
                   zvezda: bool, yarlyk: bool) -> str:
    if "Условие" not in sekcii:
        raise ValueError(f"{meta.get('id','?')}: нет секции '## Условие'")
    kuski = []
    if yarlyk:
        tegi = [meta[k].replace("-", " ") for k in ("tema", "priyom") if meta.get(k)]
        if tegi:
            kuski.append(f'<p class="tag">{html.escape(" · ".join(tegi))}</p>')
    kuski.append(f'<div class="cond">{v_html(sekcii["Условие"])}</div>')
    for imya in pokazat:
        if imya not in sekcii:
            continue
        telo = v_html(sekcii[imya])
        if imya in SPOJLER:
            kuski.append(
                f'<details><summary>{html.escape(imya.lower())}</summary>'
                f'<div class="spoiler">{telo}</div></details>')
        else:
            kuski.append(f'<div class="hint">{telo}</div>')
    klass = ' class="zvezda"' if zvezda else ""
    return f"    <li{klass}>\n      " + "\n      ".join(kuski) + "\n    </li>"


STIL = """
  :root{--paper:#f4eede;--panel:#fbf7ec;--ink:#2a2520;--ink-soft:#5d5446;--ink-faint:#8a7f6c;
        --rule:#d8cdb4;--rubric:#9e2b25;--accent:#3a6b5f;}
  *{box-sizing:border-box;margin:0;padding:0;}
  body{background:radial-gradient(1100px 560px at 82% -12%, #f8f2e3 0%, rgba(248,242,227,0) 60%),var(--paper);
       color:var(--ink);font-family:"PT Serif",Georgia,serif;font-size:17px;line-height:1.62;
       -webkit-font-smoothing:antialiased;}
  body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.5;
       background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E");}
  .wrap{position:relative;z-index:1;max-width:680px;margin:0 auto;padding:0 24px 90px;}
  header.mast{padding:58px 0 18px;border-bottom:2px solid var(--ink);margin-bottom:8px;}
  .kicker{font-family:"PT Sans",sans-serif;letter-spacing:.32em;text-transform:uppercase;
       font-size:11px;color:var(--rubric);font-weight:700;margin:0 0 12px;}
  h1{font-family:"Old Standard TT",serif;font-weight:700;font-size:46px;line-height:1.0;margin:0;}
  .date{font-family:"PT Sans",sans-serif;font-size:13px;color:var(--ink-faint);margin:14px 0 0;letter-spacing:.04em;}
  ol{list-style:none;counter-reset:p;margin-top:8px;}
  li{counter-increment:p;padding:26px 0 24px;border-bottom:1px solid var(--rule);
     display:grid;grid-template-columns:46px 1fr;gap:6px 18px;}
  li:last-child{border-bottom:none;}
  li::before{content:counter(p);grid-row:1/3;font-family:"Old Standard TT",serif;font-style:italic;
     font-weight:700;font-size:30px;color:var(--rubric);line-height:1;padding-top:2px;}
  li.zvezda::before{content:"\\2605";font-style:normal;font-size:22px;padding-top:6px;color:var(--accent);}
  li.rubrika{counter-increment:none;display:block;border-bottom:none;padding:34px 0 0;
     font-family:"PT Sans",sans-serif;font-size:11px;font-weight:700;letter-spacing:.28em;
     text-transform:uppercase;color:var(--rubric);}
  li.rubrika::before{content:none;}
  li.rubrika+li{padding-top:14px;}
  .tag,.cond,.hint,details,.spoiler{grid-column:2;}
  .tag{font-family:"PT Sans",sans-serif;font-size:11px;letter-spacing:.14em;text-transform:uppercase;
     color:var(--ink-faint);margin:0 0 8px;}
  .cond p+p{margin-top:10px;}
  .hint{font-family:"PT Serif";font-style:italic;color:var(--ink-soft);font-size:15px;
     margin:12px 0 0;padding-left:14px;border-left:2px solid var(--accent);}
  details{margin:10px 0 0;}
  summary{font-family:"PT Sans",sans-serif;font-size:12px;letter-spacing:.1em;text-transform:uppercase;
     color:var(--ink-faint);cursor:pointer;list-style:none;display:inline-block;
     border:1px solid var(--rule);border-radius:3px;padding:3px 10px;}
  summary::-webkit-details-marker{display:none;}
  summary:hover{color:var(--rubric);border-color:var(--rubric);}
  details[open] summary{margin-bottom:8px;}
  .spoiler{font-family:"PT Serif";font-style:italic;color:var(--ink-soft);font-size:15px;
     padding-left:14px;border-left:2px solid var(--rubric);}
  .spoiler p+p{margin-top:8px;}
"""

STRANICA = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Old+Standard+TT:ital,wght@0,400;0,700;1,400&family=PT+Serif:ital,wght@0,400;0,700;1,400&family=PT+Sans:wght@0,400;0,700&display=swap" rel="stylesheet">
<style>{stil}</style>
</head>
<body>
<div class="wrap">
  <header class="mast">
    <p class="kicker">{kicker}</p>
    <h1>{zagolovok}</h1>
    {data}
  </header>

  <ol>
{zadachi}
  </ol>
</div>
</body>
</html>
"""


def sobrat(manifest: Path, out: Path | None, tolko_lint: bool,
           rezhim_cli: str | None = None, zagolovok_cli: str | None = None) -> int:
    meta, sekcii = razobrat(manifest.read_text(encoding="utf-8"))
    if zagolovok_cli:
        meta["zagolovok"] = zagolovok_cli
    rezhim = rezhim_cli or meta.get("pokazyvat", "usloviya")
    if rezhim not in REZHIMY:
        print(f"❌ pokazyvat: {rezhim} — можно {', '.join(REZHIMY)}", file=sys.stderr)
        return 1
    po_umolchaniyu = REZHIMY[rezhim]

    spisok = sekcii.get("Задачи") or sekcii.get("", "")
    punkty = [s.strip()[1:].strip() for s in spisok.splitlines() if s.strip().startswith("-")]
    if not punkty:
        print("❌ в манифесте нет ни одного пункта списка", file=sys.stderr)
        return 1

    bloki, bedy = [], []
    for punkt in punkty:
        if punkt.startswith("#"):                       # рубрика: `- # Добить с ДЗ`
            bloki.append(f'    <li class="rubrika">{html.escape(punkt.lstrip("#").strip())}</li>')
            continue
        zvezda = punkt.startswith("★")
        punkt = punkt.lstrip("★").strip()
        chasti = [c.strip() for c in punkt.split("|")]
        zid = chasti[0]
        pokazat = po_umolchaniyu
        if len(chasti) > 1:
            pokazat = [] if chasti[1] == "-" else [imya_sekcii(c) for c in chasti[1].split(",")]
            for imya in pokazat:
                if imya not in SPOJLER | OTKRYTO:
                    bedy.append(f"{zid}: неизвестная секция «{imya}» в манифесте")
        fajl = BANK / f"{zid}.md"
        if not fajl.exists():
            bedy.append(f"нет задачи в банке: {zid} ({fajl})")
            continue
        zm, zs = razobrat(fajl.read_text(encoding="utf-8"))
        if not zm.get("otvet") and not zm.get("bez_otveta"):
            bedy.append(f"{zid}: пустое поле otvet (нужно `bez_otveta: da` для «докажите»)")
        if not zm.get("proverka"):
            bedy.append(f"{zid}: пустое поле proverka — ответ не подтверждён")
        try:
            bloki.append(zadacha_v_html(zm, zs, pokazat, zvezda, rezhim == "polnyj"))
        except ValueError as e:
            bedy.append(str(e))

    if bedy:
        for b in bedy:
            print(f"❌ {b}", file=sys.stderr)
        return 1
    zadach = sum(1 for b in bloki if "rubrika" not in b)
    print(f"✅ {zadach} задач(и), режим показа: {rezhim}")
    if tolko_lint:
        return 0

    data = f'<p class="date">{html.escape(meta["data"])}</p>' if meta.get("data") else ""
    stranica = STRANICA.format(
        title=html.escape(meta.get("zagolovok", "Листок")),
        stil=STIL, kicker=html.escape(meta.get("kicker", "Математика")),
        zagolovok=html.escape(meta.get("zagolovok", "Листок")),
        data=data, zadachi="\n\n".join(bloki))
    out = out or manifest.with_suffix(".html")
    out.write_text(stranica, encoding="utf-8")
    print(f"→ {out.relative_to(REPO) if out.is_relative_to(REPO) else out}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Листок задач из банка _fond/zadachi/bank/")
    p.add_argument("manifest", type=Path)
    p.add_argument("-o", "--out", type=Path)
    p.add_argument("--lint", action="store_true", help="только проверить, не собирать")
    p.add_argument("--pokazyvat", choices=list(REZHIMY),
                   help="перебить режим показа из манифеста: один список задач — несколько видов")
    p.add_argument("--zagolovok", help="перебить заголовок из манифеста")
    a = p.parse_args()
    if not a.manifest.exists():
        print(f"❌ нет манифеста: {a.manifest}", file=sys.stderr)
        return 1
    try:
        return sobrat(a.manifest, a.out, a.lint, a.pokazyvat, a.zagolovok)
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
