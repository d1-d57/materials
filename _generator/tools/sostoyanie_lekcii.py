#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sostoyanie_lekcii.py — ПРЕДСТАВЛЕНИЕ (VIEW) над markdown-базой курса.

Зачем. Владелец 17.07: «у нас нет базы данных в прямом смысле слова — придумай формат,
который имитирует базу данных и позволит СО ВСЕХ КОНЦОВ собрать информацию про каждую лекцию».

Ответ: «со всех концов собрать» — это не файл, это ЗАПРОС. Файлы = таблицы, этот скрипт = SELECT..JOIN.
Представление на диске не лежит: сохранённая копия устаревает молча — на этом проект горел 5 раз.

Таблицы (все — markdown, все — единственные дома своих фактов):
  kartoteka/KARTA-LEKCIY.md    сущность «лекция»            (нативные поля + FK)
  kartoteka/KARTA-OBLASTI.md   сущность «карточка»          (137)
  SPEKA.md §Слой 2             связь лекция ↔ карточка      (строки `Лn: id id id`)
  CHEGO-NET.md §2.3-полный     на чём лекция молча стоит
  VNESHNYAYA-MERKA.md          расхождение с 7 чужими курсами
  STYKOVKA-s-kursom-tipov.md   календарь против курса типов

Использование:
  python3 _generator/tools/sostoyanie_lekcii.py Л5        # полная карточка лекции
  python3 _generator/tools/sostoyanie_lekcii.py --all     # сводка по девяти
  python3 _generator/tools/sostoyanie_lekcii.py --card cayley   # обратный поиск: где карточка играет
  python3 _generator/tools/sostoyanie_lekcii.py --gates   # гейты 3/4 — вычислимо, впервые

Только stdlib, детерминизм, ничего не пишет на диск.
"""
import re, sys, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
P = lambda *a: os.path.join(ROOT, 'teoriya-kategoriy', *a)

def read(p):
    try:
        return open(p, encoding='utf-8').read()
    except FileNotFoundError:
        return ''

# ---------- ТАБЛИЦЫ ----------
def cards():
    """KARTA-OBLASTI.md → {id: {род, суть, статус, приборы, связи, body}}"""
    out = {}
    for cid, body in re.findall(r'^id: ([\w\-]+)\n(.*?)(?=^id: |\Z)', read(P('kartoteka', 'KARTA-OBLASTI.md')), re.M | re.S):
        g = lambda f: (re.search(r'^' + f + r': (.*)', body, re.M) or [None, ''])[1]
        out[cid] = {'род': g('род'), 'суть': g('суть'), 'статус': g('статус'),
                    'прибор': 'проверено-на-приборе' in body, 'body': body}
    return out

def lecture_map():
    """SPEKA §Слой 2 → {'Л5': [ids]} — таблица связи лекция ↔ карточка"""
    return {m.group(1): m.group(2).split()
            for m in re.finditer(r'^(Л[1-9]):\s*(.+)$', read(P('SPEKA.md')), re.M)}

def lectures():
    """KARTA-LEKCIY.md → {'Л5': {поля}} — сущность «лекция»"""
    out = {}
    for body in re.findall(r'^id: L(\d)\n(?:.*?)(?=^id: L\d|\Z)', read(P('kartoteka', 'KARTA-LEKCIY.md')), re.M | re.S):
        pass
    txt = read(P('kartoteka', 'KARTA-LEKCIY.md'))
    for m in re.finditer(r'^id: (L\d)\n(.*?)^status: (\S+)\s*$', txt, re.M | re.S):
        lid, body, st = m.group(1), m.group(2), m.group(3)
        def g(f):
            r = re.search(r'^' + f + r': (.*?)(?=\n[a-z_0-9]+: |\Z)', body, re.M | re.S)
            return r.group(1).strip() if r else ''
        out['Л' + lid[1]] = {'id': lid, 'nomer': g('nomer'), 'nazvanie': g('nazvanie'),
                             'zamysel': g('zamysel'), 'hook': g('hook'), 'razvyazka': g('razvyazka'),
                             'izobretenie': g('izobretenie'), 'gejt5': g('gejt5'), 'flagi': g('flagi'),
                             'programma': g('programma').lstrip('|').strip(), 'status': st}
    return out

def opory(lek):
    """CHEGO-NET §2.3-полный → секция лекции (на чём молча стоит)"""
    txt = read(P('CHEGO-NET.md'))
    m = re.search(r'^### ' + lek + r' —(.*?)(?=^### |^## |\Z)', txt, re.M | re.S)
    return (m.group(1).strip() if m else '')

def merka(lek):
    """VNESHNYAYA-MERKA → строка лекции"""
    for l in read(P('VNESHNYAYA-MERKA.md')).split('\n'):
        if l.startswith('| **' + lek + '**'):
            return l
    return ''

def kalendar(lek):
    """STYKOVKA → дата + что зал видел у себя"""
    txt = read(P('STYKOVKA-s-kursom-tipov.md'))
    m = re.search(r'`(Л1 [\d.]+ · .*?)`', txt, re.S)
    date = ''
    if m:
        for chunk in m.group(1).split('·'):
            if chunk.strip().startswith(lek + ' '):
                date = chunk.strip()
    return date

# ---------- ПРЕДСТАВЛЕНИЕ ----------
def view(lek):
    C, M, L = cards(), lecture_map(), lectures()
    rec = L.get(lek)
    ids = M.get(lek, [])
    print('=' * 100)
    if not rec:
        print(f'{lek} — ЗАПИСИ В KARTA-LEKCIY НЕТ. Карточек в карте: {len(ids)}. ⇒ таблица `лекция` не заполнена.')
        print('=' * 100); return
    print(f"{lek}. {rec['nazvanie']}   [запись: {rec['status']}]")
    print('=' * 100)
    print(f"\n▸ ЗАМЫСЕЛ\n  {rec['zamysel']}")
    d = kalendar(lek)
    if d: print(f"\n▸ КОГДА (JOIN ← STYKOVKA)\n  {d}")

    print(f"\n▸ ГЕЙТЫ 3/4 — вычислимо (JOIN ← KARTA-LEKCIY × KARTA-OBLASTI × SPEKA)")
    for f, name in [('hook', 'гейт 3: вопрос в начале'), ('razvyazka', 'гейт 3: ответ в конце'),
                    ('izobretenie', 'гейт 4: зал изобретает')]:
        cid = rec[f]
        if not cid: print(f"  ❌ {name:26} — поле пустое"); continue
        c = C.get(cid)
        if not c: print(f"  ❌ {name:26} = {cid} — ФАНТОМ, карточки нет"); continue
        problems = []
        if cid not in ids: problems.append(f'НЕ в карте {lek}')
        if c['статус'] == 'seed': problems.append('seed')
        mark = '✅' if not problems else '❌'
        print(f"  {mark} {name:26} = {cid}  [{c['род']}]" + (f"  ⚠ {', '.join(problems)}" if problems else ''))
        print(f"      «{c['суть'][:88]}»")

    print(f"\n▸ ГЕЙТ 5 (прибор)\n  {rec['gejt5']}")

    print(f"\n▸ КАРТОЧКИ — {len(ids)} (JOIN ← SPEKA §Слой 2)")
    by = {}
    for i in ids: by.setdefault(C.get(i, {}).get('род', '?'), []).append(i)
    for rod in sorted(by):
        for i in by[rod]:
            c = C.get(i, {})
            fl = ('🔬' if c.get('прибор') else '  ') + ('🌱' if c.get('статус') == 'seed' else '  ')
            print(f"  {fl} [{rod:11}] {i}")

    pr = [i for i in ids if C.get(i, {}).get('прибор')]
    if pr:
        print(f"\n▸ ВЕРДИКТЫ ПРИБОРА — {len(pr)} (JOIN ← KARTA-OBLASTI)")
        for i in pr:
            t = re.search(r'^проверено-на-приборе: (.*?)(?=\n[а-я\-]+: |\Z)', C[i]['body'], re.M | re.S)
            print(f"  · {i}: {' '.join(t.group(1).split())[:150]}…" if t else f"  · {i}")

    o = opory(lek)
    if o: print(f"\n▸ НА ЧЁМ СТОИТ (JOIN ← CHEGO-NET §2.3)\n  {o.splitlines()[0][:96]}\n  …таблица опор: {len([l for l in o.splitlines() if l.startswith('|')])} строк")
    mk = merka(lek)
    if mk: print(f"\n▸ ПРОТИВ ЧУЖИХ КУРСОВ (JOIN ← VNESHNYAYA-MERKA)\n  {mk[:190]}…")
    if rec['flagi']: print(f"\n▸ ФЛАГИ\n  {rec['flagi']}")
    print(f"\n▸ ПРОГРАММА (в текст заказчику) — {len(rec['programma'].split())} слов")
    print()

def all_lectures():
    C, M, L = cards(), lecture_map(), lectures()
    print(f"{'ЛЕК':5} {'карт':5} {'запись':10} {'гейт3-хук':11} {'гейт3-разв':11} {'гейт4':8} {'гейт5':6} название")
    print('-' * 118)
    for n in range(1, 10):
        lek = f'Л{n}'; rec = L.get(lek); ids = M.get(lek, [])
        if not rec:
            print(f"{lek:5} {len(ids):<5} {'—':10} {'—':11} {'—':11} {'—':8} {'—':6} ЗАПИСИ НЕТ")
            continue
        ok = lambda f: '✅' if (rec[f] and rec[f] in C and rec[f] in ids and C[rec[f]]['статус'] != 'seed') else '❌'
        g5 = '❌' if 'НЕ СПРАШИВАЛИ' in rec['gejt5'] else '✅'
        print(f"{lek:5} {len(ids):<5} {rec['status']:10} {ok('hook'):11} {ok('razvyazka'):11} {ok('izobretenie'):8} {g5:6} {rec['nazvanie'][:44]}")
    done = sum(1 for n in range(1, 10) if f'Л{n}' in L)
    print('-' * 118)
    print(f"Записей в таблице `лекция`: {done}/9 · ⚠ гейты 3/4/5 — вычислимы ТОЛЬКО там, где запись есть")

def by_card(cid):
    C, M, L = cards(), lecture_map(), lectures()
    if cid not in C: print(f'Карточки {cid} нет.'); return
    print(f"{cid}  [{C[cid]['род']}] статус: {C[cid]['статус']}\n  «{C[cid]['суть']}»\n")
    for lek, ids in sorted(M.items()):
        if cid in ids: print(f"  ▸ входит в {lek}")
    for lek, rec in sorted(L.items()):
        for f in ('hook', 'razvyazka', 'izobretenie'):
            if rec[f] == cid: print(f"  ⭐ {lek}: несёт роль `{f}` (гейт {'3' if f != 'izobretenie' else '4'})")

def gates():
    C, M, L = cards(), lecture_map(), lectures()
    print('ГЕЙТЫ 3/4 — впервые вычислимо (были 0/9 «суждение, не скрипт»)\n')
    bad = 0
    for n in range(1, 10):
        lek = f'Л{n}'; rec = L.get(lek)
        if not rec: print(f'  {lek}: ❌ записи нет — гейты 3/4 проверить нечем'); bad += 1; continue
        for f in ('hook', 'razvyazka', 'izobretenie'):
            cid = rec[f]
            if not cid or cid not in C or cid not in M.get(lek, []) or C[cid]['статус'] == 'seed':
                print(f'  {lek}.{f}: ❌ {cid or "пусто"}'); bad += 1
    print(f'\n{"✅ все зелёные" if not bad else f"❌ проблем: {bad}"}')

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__)
    elif a[0] == '--all': all_lectures()
    elif a[0] == '--gates': gates()
    elif a[0] == '--card': by_card(a[1])
    else: view(a[0])
