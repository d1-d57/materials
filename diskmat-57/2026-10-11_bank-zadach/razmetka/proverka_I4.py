# -*- coding: utf-8 -*-
"""И4: предсказывают ли теги операций исход пункта лучше «силы ребёнка» и «лёгкости задачи».

python3 proverka_I4.py <NABLYUDENIYA-50.csv> <Q-A.csv> <Q-B.csv>

Для каждой клетки «ребёнок × пункт» с известным исходом прячем её и предсказываем по ДРУГИМ ЗАДАЧАМ того же
ребёнка (пункты той же задачи не используются — иначе утечка «а» → «б») и по ДРУГИМ детям для этого пункта.
Правила:
  a  сила ребёнка — доля плюсов ребёнка на других задачах
  b  лёгкость пункта — доля плюсов других детей на этом пункте
  ab сила + лёгкость: logit(a) + logit(b) − logit(общая доля)
  qX теги операций (X = A, B, AB∩, AB∪): владение операцией = доля плюсов ребёнка на других задачах с этой
     операцией; пункт = среднее по его операциям (решение 1); затем + лёгкость, как ab
  gX то же по группам (идеи 1–3)
  nn ближайшие пункты по данным: 5 пунктов других задач, сильнее всего совпадающих с этим у других детей
Режимы исхода: «строгий» — пусто на листке = не решил; «только известное» — пусто на листке выбрасывается.
Мера: логарифмическая потеря (меньше — лучше) и AUC; интервал — бутстреп по детям для разности с ab."""
import csv, sys, math, random, collections

GR = {'R1': 1, 'R2': 1, 'R3': 1, 'D1': 1, 'N1': 2, 'N2': 2, 'K1': 2, 'S1': 2, 'S2': 2, 'P1': 3, 'P2': 3, 'P3': 3}
EPS = 0.02


def lg(p):
    p = min(max(p, EPS), 1 - EPS)
    return math.log(p / (1 - p))


def sg(x):
    return 1 / (1 + math.exp(-x))


def loadQ(f):
    q = {}
    for r in csv.DictReader(open(f, encoding='utf-8')):
        if r['reshenie'].strip() != '1':
            continue
        ops = [o.strip() for o in r['operacii'].split(';') if o.strip() and not o.strip().startswith('X:')]
        q[(r['rabota'], r['punkt'])] = set(ops)
    return q


def main():
    nab, fa, fb = sys.argv[1:4]
    QA, QB = loadQ(fa), loadQ(fb)
    Q = {'A': QA, 'B': QB,
         'AB∩': {k: QA.get(k, set()) & QB.get(k, set()) for k in set(QA) | set(QB)},
         'AB∪': {k: QA.get(k, set()) | QB.get(k, set()) for k in set(QA) | set(QB)}}
    # отрицательный контроль: те же наборы операций, случайно переставленные между пунктами
    kl = sorted(Q['AB∩'])
    sh = [Q['AB∩'][k] for k in kl]
    random.Random(7).shuffle(sh)
    Q['Слч'] = dict(zip(kl, sh))
    rows = list(csv.DictReader(open(nab, encoding='utf-8')))
    for rezhim in ('строгий', 'только известное'):
        Y = {}
        for r in rows:
            if r['ishod'] == 'net':
                continue
            if r['ishod'] == 'pusto' and rezhim == 'только известное':
                continue
            Y[(r['rebyonok'], r['rabota'], r['punkt'])] = 1 if r['ishod'] == 'plus' else 0
        zad = {k: (k[1], k[2].rstrip('абвгд')) for k in Y}
        po_det = collections.defaultdict(list)
        po_p = collections.defaultdict(list)
        for k, y in Y.items():
            po_det[k[0]].append((k, y))
            po_p[(k[1], k[2])].append((k[0], y))
        glob = sum(Y.values()) / len(Y)
        # корреляция пунктов по детям (для nn)
        punkty = sorted(po_p)
        vec = {p: dict(po_p[p]) for p in punkty}

        def sovp(p, q, bez):
            obs = [(vec[p][d], vec[q][d]) for d in vec[p] if d in vec[q] and d != bez]
            if len(obs) < 6:
                return None
            return sum(1 for x, y in obs if x == y) / len(obs)

        pred = collections.defaultdict(dict)
        for k, y in Y.items():
            d, rab, pu = k
            z = zad[k]
            drugie = [(kk, yy) for kk, yy in po_det[d] if zad[kk] != z]
            a = (sum(yy for _, yy in drugie) + glob) / (len(drugie) + 1)
            oth = [yy for dd, yy in po_p[(rab, pu)] if dd != d]
            b = (sum(oth) + glob) / (len(oth) + 1)
            pred['a'][k] = a
            pred['b'][k] = b
            pred['ab'][k] = sg(lg(a) + lg(b) - lg(glob))
            for nm, q in Q.items():
                for uroven in ('q', 'g'):
                    ops = q.get((rab, pu), set())
                    keys = ops if uroven == 'q' else {GR[o] for o in ops if o in GR}
                    ms = []
                    for o in keys:
                        ev = [yy for kk, yy in drugie
                              if (o in q.get((kk[1], kk[2]), set()) if uroven == 'q'
                                  else o in {GR[x] for x in q.get((kk[1], kk[2]), set()) if x in GR})]
                        if ev:
                            ms.append((sum(ev) + a) / (len(ev) + 1))
                    m = sum(ms) / len(ms) if ms else a
                    pred[uroven + nm][k] = sg(lg(m) + lg(b) - lg(glob))
            # остатки: несут ли теги что-то СВЕРХ ab? поправка = λ · средний остаток (y − p_ab) ребёнка
            # на других задачах с той же операцией (группой); p_ab этих клеток — без утечки текущей
            for nm, q in Q.items():
                for uroven in ('r', 'h'):
                    ops = q.get((rab, pu), set())
                    keys = ops if uroven == 'r' else {GR[o] for o in ops if o in GR}
                    res = []
                    for kk, yy in drugie:
                        okk = q.get((kk[1], kk[2]), set())
                        okk = okk if uroven == 'r' else {GR[x] for x in okk if x in GR}
                        if keys & okk:
                            o2 = [y2 for dd, y2 in po_p[(kk[1], kk[2])] if dd != d]
                            b2 = (sum(o2) + glob) / (len(o2) + 1)
                            res.append(yy - sg(lg(a) + lg(b2) - lg(glob)))
                    r_ = sum(res) / (len(res) + 3) if res else 0.0   # усадка к нулю: +3 фиктивных нуля
                    for lam in (2, 4):
                        pred[f'{uroven}{nm}λ{lam}'][k] = sg(lg(pred['ab'][k]) + lam * r_)
            # nn
            sc = []
            for kk, yy in drugie:
                s = sovp((rab, pu), (kk[1], kk[2]), d)
                if s is not None:
                    sc.append((s, yy))
            sc.sort(reverse=True)
            top = sc[:5]
            m = (sum(yy for _, yy in top) + a) / (len(top) + 1) if top else a
            pred['nn'][k] = sg(lg(m) + lg(b) - lg(glob))

        def ll(ks, p):
            return -sum(math.log(p[k] if Y[k] else 1 - p[k]) for k in ks) / len(ks)

        def auc(ks, p):
            pos = [p[k] for k in ks if Y[k]]
            neg = [p[k] for k in ks if not Y[k]]
            if not pos or not neg:
                return float('nan')
            s = sum((x > z) + 0.5 * (x == z) for x in pos for z in neg)
            return s / (len(pos) * len(neg))

        ks = list(Y)
        deti = sorted({k[0] for k in ks})
        po_d = collections.defaultdict(list)
        for k in ks:
            po_d[k[0]].append(k)
        random.seed(1)
        boots = [[x for d in random.choices(deti, k=len(deti)) for x in po_d[d]] for _ in range(300)]
        print(f'\n== режим «{rezhim}»: клеток {len(ks)}, детей {len(deti)}, доля плюсов {glob:.2f}')
        print(f'{"правило":10} {"потеря":>7} {"AUC":>6}   разность потерь с ab [95%]  (минус = лучше ab)')
        imena = ['a', 'b', 'ab', 'qA', 'qB', 'qAB∩', 'qAB∪', 'gA', 'gB', 'gAB∩', 'gAB∪', 'nn']
        imena += [f'{u}{nm}λ{l}' for u in ('r', 'h') for nm in ('A', 'B', 'AB∩', 'Слч') for l in (2, 4)]
        for nm in imena:
            p = pred[nm]
            diffs = sorted(ll(bk, p) - ll(bk, pred['ab']) for bk in boots)
            print(f'{nm:10} {ll(ks, p):7.4f} {auc(ks, p):6.3f}   {ll(ks, p) - ll(ks, pred["ab"]):+.4f} '
                  f'[{diffs[7]:+.4f}; {diffs[292]:+.4f}]')


if __name__ == '__main__':
    main()
