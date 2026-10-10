# -*- coding: utf-8 -*-
"""ГЕЙТЫ ПЕРЕД ПЕЧАТЬЮ комплекта итерации. Запуск: python3 proverka.py <папка итерации>
Краснеет (код выхода 1), если:
  Г1  у обязательного пункта ответы вариантов А и Б совпадают (кроме пунктов из SOVPADENIE_OK в ITERACIYA.json);
  Г2  PDF листка/контрольной/ДЗ не того числа страниц (ITERACIYA.json → stranic) или колонка переливает за лист;
  Г3  условие новой задачи почти дословно встречается в уже выданных листках (difflib ≥ 0,82) — проверить глазами;
  Г4  у пункта нет ответа в каноне;
  Г5  контрольная или ДЗ свёрстаны НЕ на пол-листа (Р209, железно): по маскам ITERACIYA.json → POLULIST
      (по умолчанию KONTROLNAYA-*.html, DZ-*.html) в HTML должна быть раскладка polulist (две половины на A4);
  Г6  шпаргалка — не «номер, вариант, ответ» (А14, железно): больше трёх колонок или слова пояснений
      («ошибк», «наводящ», «→», «принима», «карта», «помощь»).
Г3 печатает пары, а не решает сам: повтор внешней формы при другом содержании — норма (сквозные правила процедуры).
"""
import json, sys, re, glob, difflib, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
def norm(s): return re.sub(r'[^а-яёa-z0-9]+', ' ', re.sub(r'<[^>]+>', ' ', s.lower())).strip()
def teksty_vydannyh(arka, krome):
    T = []
    for f in glob.glob(str(arka / '*.tex')) + glob.glob(str(arka / 'iteracii' / '*' / 'out' / 'LISTOK-*.html')):
        if krome in f: continue
        s = open(f, encoding='utf-8', errors='ignore').read()
        for kus in re.split(r'\\item|\\zad|<div class="z', s):
            n = norm(kus)
            if len(n) > 60: T.append((Path(f).name, n[:400]))
    return T
def main(it):
    it = Path(it).resolve(); J = json.load(open(it / 'ITERACIYA.json', encoding='utf-8'))
    K = json.load(open(it / 'out' / 'kanon.json', encoding='utf-8')); red = 0
    ok = set(J.get('SOVPADENIE_OK', []))
    A = {p['punkt']: p for p in K['punkty']['А']}; B = {p['punkt']: p for p in K['punkty']['Б']}
    for pn, p in A.items():
        if p['razdel'] in '○△' and pn in B and p['otvet'] == B[pn]['otvet'] and pn not in ok:
            print(f'Г1 ❗ пункт {pn}: ответ А = ответ Б ({p["otvet"]})'); red += 1
    for pn, p in list(A.items()) + list(B.items()):
        if not str(p.get('otvet', '')).strip(): print(f'Г4 ❗ пункт {pn}: нет ответа'); red += 1
    from listok_gen import fit_report
    for mask, n in J.get('stranic', {}).items():
        for pdf in glob.glob(str(it / 'out' / mask)):
            k = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
            if k != n: print(f'Г2 ❗ {Path(pdf).name}: страниц {k}, ждали {n}'); red += 1
            h = pdf[:-4] + '.html'
            if Path(h).exists():
                over = [x for x in fit_report(h) if x > 0.5]
                if over: print(f'Г2 ❗ {Path(h).name}: перелив {over} мм'); red += 1
    for mask in J.get('POLULIST', ['KONTROLNAYA-*.html', 'DZ-*.html']):
        for h in glob.glob(str(it / 'out' / mask)):
            if 'class="list"' not in open(h, encoding='utf-8').read():
                print(f'Г5 ❗ {Path(h).name}: не пол-листа на человека (собрать через listok_gen.polulist)'); red += 1
    for h in glob.glob(str(it / 'out' / 'SHPARGALKA-*.html')):
        t = open(h, encoding='utf-8').read(); tl = re.sub(r'<[^>]+>', ' ', t.split('<body>')[-1]).lower()
        lish = [w for w in ('ошибк', 'наводящ', '→', 'принима', 'карта', 'помощь') if w in tl]
        shir = max((len(re.findall(r'<th', tr)) for tr in re.findall(r'<tr>.*?</tr>', t)), default=0)
        if lish or shir > 3:
            print(f'Г6 ❗ {Path(h).name}: шпаргалка — только номер, вариант, ответ; лишнее: {lish or f"{shir} колонок"}'); red += 1
    arka = it.parent.parent; stary = teksty_vydannyh(arka, it.name)
    novye = []
    for h in glob.glob(str(it / 'out' / 'LISTOK-*-A.html')) + glob.glob(str(it / 'out' / 'DZ-*.html')):
        for kus in open(h, encoding='utf-8').read().split('<div class="z')[1:]:
            n = norm(kus)
            if len(n) > 60: novye.append(n[:400])
    for n in novye:
        for f, s in stary:
            r = difflib.SequenceMatcher(None, n, s).ratio()
            if r >= 0.82: print(f'Г3 ? похоже ({r:.2f}) на {f}: «{n[:90]}…»')
    print('гейты: ' + ('ЗЕЛЁНЫЕ' if not red else f'КРАСНЫХ {red}')); sys.exit(1 if red else 0)
if __name__ == '__main__':
    main(sys.argv[1])
