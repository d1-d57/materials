# -*- coding: utf-8 -*-
"""ШАБЛОН ДАННЫХ ЛИСТКА — копируется novaya.py в папку новой итерации как dannye.py. Заполнить ЗАДАЧИ, собрать:
    python3 dannye.py          → out/LISTOK-<дата>-A/B.html/.pdf, out/kanon.json (+ перелив по страницам)
Правила (FORMAT-listka-po-otvetu.md): стр. 1 «Обязательные задачи» (○ кружки / △ треугольники), стр. 2 «Дополнительные задачи»
(номера без значков, ★ — звёздочки); ответ — ВЫРАЖЕНИЕ; у каждой задачи источник; ответ считается ПЕРЕБОРОМ здесь же (функция otvet),
а не переписывается из книги; варианты А и Б изоморфны, ответы различаются (proverka.py Г1).
Карта (игровое занятие, через одно): задать KARTA — см. kvest.py и listok_29-09_dannye.py как образец раскладки.
"""
import json, os, sys, pathlib
_H = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(next(p / 'mashina-listka' for p in _H.parents if (p / 'mashina-listka').is_dir())))
from listok_gen import document, to_pdf, fit_report, shen
DATA = '6 октября'; SLUG = '06-10'; META = dict(title='ТЕМА', date=DATA, klass='7И')

# ── ЗАДАЧИ ────────────────────────────────────────────────────────────────────────────────────────────────
# Каждая задача: razdel ('○'|'△'|'доп'|'★'), src (источник), text(v) → условие для варианта, punkty(v) → [(буква, ответ-выражение)],
# pole: 'blok' (узкое поле слева, короткий ответ) | 'stroka' (во всю ширину, h мм) | ('shablon', ['_','+','_','=','_']).
def pr_dvuznachnye(pred):                                  # пример проверки перебором
    return sum(1 for x in range(10, 100) if pred(x))
ZADACHI = [
    dict(razdel='○', src='ИСТОЧНИК, №', pole='blok',
         text=lambda v: f"Сколько двузначных чисел делятся на {dict(А=7, Б=8)[v]}?",
         punkty=lambda v: [('', f"{pr_dvuznachnye(lambda x: x % dict(А=7, Б=8)[v] == 0)}")]),
    dict(razdel='доп', src='ИСТОЧНИК, №', pole='blok',
         text=lambda v: "Условие дополнительной задачи.",
         punkty=lambda v: [('а', '1'), ('б', '2')]),
]
PORYADOK_DOP = {'А': [1], 'Б': [1]}      # индексы дополнительных задач в ZADACHI по вариантам (номера в Б переставить)
KARTA = None                            # игровое занятие: dict для map_svg + граф для kvest (см. образец 29.09)

def items(v, razdely):
    out = []; n = 0
    obyaz = [z for z in ZADACHI if z['razdel'] in '○△']
    dop = [ZADACHI[i] for i in PORYADOK_DOP[v]]
    for z in (obyaz if razdely == 'obyaz' else dop):
        n = (obyaz.index(z) + 1) if razdely == 'obyaz' else len(obyaz) + dop.index(z) + 1
        ps = z['punkty'](v); bukvy = [b for b, _ in ps]
        it = dict(mark=z['razdel'] if z['razdel'] in '○△★' else '', num=n, text=z['text'](v), block=bukvy)
        if z['pole'] != 'blok':
            it['block'] = None
            it['rows'] = [dict(tpl=z['pole'][1])] if isinstance(z['pole'], tuple) else [dict(h=z.get('h', 8.5))]
        out.append(it)
    return out
def kanon():
    K = {}
    for v in ('А', 'Б'):
        rows = []
        for razd in ('obyaz', 'dop'):
            for it, z in zip(items(v, razd), [z for z in ZADACHI if z['razdel'] in '○△'] if razd == 'obyaz' else [ZADACHI[i] for i in PORYADOK_DOP[v]]):
                for b, a in z['punkty'](v): rows.append(dict(punkt=f"{it['num']}{b}", razdel=z['razdel'], otvet=a, kletka=f"{it['num']}:{b}"))
        K[v] = rows
    return dict(punkty=K, karta=KARTA)
if __name__ == '__main__':
    outs = []
    for v, f in (('А', 'A'), ('Б', 'B')):
        pages = [dict(heading='Обязательные задачи', items=items(v, 'obyaz')), dict(heading='Дополнительные задачи', items=items(v, 'dop'), abw='64mm')]
        p = f'{_H}/out/LISTOK-{SLUG}-{f}.html'; os.makedirs(_H / 'out', exist_ok=True); open(p, 'w').write(document(META, v, pages)); outs.append(p)
    to_pdf(outs); json.dump(kanon(), open(_H / 'out' / 'kanon.json', 'w'), ensure_ascii=False, indent=1)
    for p in outs: print(os.path.basename(p), 'перелив, мм:', fit_report(p))
