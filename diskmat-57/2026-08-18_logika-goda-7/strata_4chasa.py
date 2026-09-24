#!/usr/bin/env python3
# Есть ли в 7И страты? Надёжность каждого листка, связь между листками, проверка хвостов перестановками.
import csv, json, re, random, statistics as st
from pathlib import Path
H = Path(__file__).resolve().parent
NORM = lambda n: re.sub(r'\s*\(.*', '', n).replace('ё', 'е').strip()
num = lambda k: int(re.match(r'\d+', k).group())
def s15(fn):
    R = list(csv.DictReader(open(H/fn, encoding='utf-8'), delimiter=';'))
    Z = [k for k in R[0] if re.fullmatch(r'з\d+', k)]
    return {NORM(r['фамилия_имя']): [int(r[k] in ('+', 'в')) for k in Z] for r in R if r['зачтено'].isdigit()}
OH, LG = s15('SDACHA-15-09_obratnyj-hod.csv'), s15('SDACHA-15-09_logika.csv')
# 22.09: пункты по правилу svod_4chasa (плюс или верный ответ, кружки четверым) — берём оттуда
import importlib.util, io, contextlib
spec = importlib.util.spec_from_file_location('svod', H/'svod_4chasa.py'); sv = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(sv)
KB, KO = sv.ITEMS22, {n: [v for k, v in sorted(d.items(), key=lambda x: (num(x[0]), x[0])) if num(k) <= 9] for n, d in sv.ITEMS22_D.items()}
names = sorted(set(OH) & set(LG) & set(KB))
def kr20(M):  # надёжность листка по пунктам
    k = len(M[0]); tot = [sum(r) for r in M]; vt = st.pvariance(tot)
    pq = sum((p := sum(r[j] for r in M) / len(M)) * (1 - p) for j in range(k))
    return k / (k - 1) * (1 - pq / vt) if vt else float('nan')
S = {'ОХ': OH, 'логика': LG, 'комб весь': KB, 'комб обяз': KO}
print(f'детей со всеми тремя листками: {len(names)}')
rel = {}
for t, d in S.items():
    M = [d[n] for n in names]; rel[t] = kr20(M)
    print(f'{t:10} пунктов {len(M[0]):2} | надёжность KR-20 {rel[t]:.2f} | медиана {st.median(sum(r) for r in M)}')
tot = {t: [sum(d[n]) for n in names] for t, d in S.items()}
print('\nсвязь между листками: наблюдаемая → с поправкой на ненадёжность (1.0 = одна и та же способность)')
for a, b in (('ОХ', 'логика'), ('ОХ', 'комб весь'), ('логика', 'комб весь'), ('ОХ', 'комб обяз'), ('логика', 'комб обяз')):
    r = st.correlation(tot[a], tot[b]); print(f'  {a:7} – {b:10} r={r:+.2f} → {r / (rel[a] * rel[b]) ** .5:+.2f}')
# хвосты: сколько детей в нижней/верхней трети на ВСЕХ трёх листках — против случайной перетасовки
def rank(v): return [(sum(x < y for x in v) + 0.5 * (sum(x == y for x in v) - 1)) / (len(v) - 1) for y in v]  # средний ранг при ничьих
P = [rank(tot[t]) for t in ('ОХ', 'логика', 'комб весь')]
cnt = lambda P, f: sum(all(f(P[j][i]) for j in range(3)) for i in range(len(names)))
lo, hi = (lambda p: p <= 1 / 3), (lambda p: p >= 2 / 3)
obs_lo, obs_hi = cnt(P, lo), cnt(P, hi)
random.seed(1); N = 20000; ge_lo = ge_hi = 0
for _ in range(N):
    Q = [P[0]] + [random.sample(p, len(p)) for p in P[1:]]
    ge_lo += cnt(Q, lo) >= obs_lo; ge_hi += cnt(Q, hi) >= obs_hi
print(f'\nснизу на всех трёх: {obs_lo} (случайно ожидалось бы ~{len(names) / 27:.1f}; p={ge_lo / N:.3f})')
print(f'сверху на всех трёх: {obs_hi} (p={ge_hi / N:.3f})')
m12 = [(a + b) / 2 for a, b in zip(P[0], P[1])]
print(f'\nпредсказание: место по двум листкам 15.09 → место 22.09: r={st.correlation(m12, P[2]):.2f}')
sr = sorted(((sum(p[i] for p in P) / 3, names[i]) for i in range(len(names))), reverse=True)
gaps = sorted(((sr[i][0] - sr[i + 1][0], sr[i][1], sr[i + 1][1]) for i in range(len(sr) - 1)), reverse=True)[:3]
print('среднее место (0..1), по убыванию:', ' '.join(f'{n.split()[0]}:{v:.2f}' for v, n in sr))
print('три самых больших разрыва в ряду:', [(round(g, 2), a.split()[0], b.split()[0]) for g, a, b in gaps])
