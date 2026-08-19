#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка внутренних ссылок собранного сайта.

    python3 check_ssylki.py     # rc=0 при нуле битых, rc=1 иначе

Считаются направления перехода, названные ТЗ §3, §7 и доводкой П8/П9:
  год  → блок / год → контрольная    (с календаря на мини-курс и на её тему)
  блок → занятие / блок → контрольная / блок → блок (кружок соседней строки)
  занятие → блок / занятие → год     (обратный ход)

Битой считается ссылка на несуществующий файл в dist/. Внешних ссылок на
страницах нет — если появится, будет названа отдельно, а не молча пропущена.
Отдельно (П8, критерий готовности §2 п.2): ни одна плашка контрольной
(class="ktr") не должна вести на nedelya-NN.html — только на её тему.
"""
import json, os, re, sys, collections

TUT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(TUT, 'dist')
IST = os.path.join(TUT, 'god.json')

SSYLKA = re.compile(r'<a\b[^>]*\bhref\s*=\s*"([^"]+)"', re.I)
# П8: клик по плашке контрольной обязан вести на её тему (kontrolnaya-NN.html),
# а не на страницу недели — ищем именно ссылки с class="ktr…".
KTR_SSYLKA = re.compile(r'<a\s+class="ktr[^"]*"[^>]*\bhref\s*=\s*"([^"]+)"', re.I)


def rod(imya):
    if imya == 'index.html':
        return 'god'
    if imya.startswith('blok-'):
        return 'blok'
    if imya.startswith('nedelya-'):
        return 'nedelya'
    if imya.startswith('kontrolnaya-'):
        return 'kontrolnaya'
    return 'inoe'


def main():
    fajly = sorted(f for f in os.listdir(DIST) if f.endswith('.html'))
    est = set(fajly)
    if not fajly:
        print('в %s нет собранных страниц' % DIST)
        return 1

    napravlenia = collections.Counter()
    bitye, vneshnie = [], []
    vsego = 0
    dostignuty = collections.Counter()
    ktr_na_nedelyu = []

    for f in fajly:
        soder = open(os.path.join(DIST, f), encoding='utf-8').read()
        for h in SSYLKA.findall(soder):
            vsego += 1
            if re.match(r'^(https?:|mailto:|//)', h):
                vneshnie.append((f, h))
                continue
            cel = h.split('#')[0].split('?')[0]
            if not cel:
                continue
            if cel not in est:
                bitye.append((f, h))
                continue
            napravlenia['%s → %s' % (rod(f), rod(cel))] += 1
            dostignuty[cel] += 1
        for h in KTR_SSYLKA.findall(soder):
            cel = h.split('#')[0].split('?')[0]
            if cel.startswith('nedelya-'):
                ktr_na_nedelyu.append((f, h))

    # охват: до каждой ли страницы вообще можно дойти
    sirotstvo = [f for f in fajly if f != 'index.html' and not dostignuty.get(f)]

    g = json.load(open(IST, encoding='utf-8'))
    y_blok = sum(1 for c in g['chetverti'] for e in c['elementy'] if e['tip'] == 'blok')
    y_kruzhok = sum(1 for c in g['chetverti'] for e in c['elementy'] if e['tip'] == 'kruzhok')
    y_ned = sum(c['chasy'] for c in g['chetverti']) // 2
    y_ktr = sum(1 for c in g['chetverti'] for e in c['elementy'] if e['tip'] == 'kontrolnaya')

    print('страниц в dist   : %d (блоков %d из %d, кружка %d из %d, занятий %d из %d, контрольных %d из %d)'
          % (len(fajly),
             sum(1 for f in fajly if rod(f) == 'blok' and 'kruzhok' not in f), y_blok,
             sum(1 for f in fajly if 'kruzhok' in f), y_kruzhok,
             sum(1 for f in fajly if rod(f) == 'nedelya'), y_ned,
             sum(1 for f in fajly if rod(f) == 'kontrolnaya'), y_ktr))
    print('ссылок всего     : %d' % vsego)
    for k in sorted(napravlenia):
        print('   %-22s %d' % (k, napravlenia[k]))
    print('битых внутренних ссылок: %d' % len(bitye))
    for f, h in bitye[:20]:
        print('   БИТАЯ %s -> %s' % (f, h))
    print('внешних ссылок   : %d' % len(vneshnie))
    for f, h in vneshnie[:10]:
        print('   ВНЕШНЯЯ %s -> %s' % (f, h))
    print('страниц, до которых нельзя дойти ни по одной ссылке: %d' % len(sirotstvo))
    for f in sirotstvo[:20]:
        print('   НЕДОСТИЖИМА %s' % f)
    print('плашек контрольной, ведущих на страницу недели (П8, должно быть 0): %d'
          % len(ktr_na_nedelyu))
    for f, h in ktr_na_nedelyu[:20]:
        print('   КОНТРОЛЬНАЯ→НЕДЕЛЯ %s -> %s' % (f, h))

    plohо = len(bitye) + len(sirotstvo) + len(ktr_na_nedelyu)
    return 1 if plohо else 0


if __name__ == '__main__':
    sys.exit(main())
