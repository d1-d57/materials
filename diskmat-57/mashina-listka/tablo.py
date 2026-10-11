# -*- coding: utf-8 -*-
"""ТАБЛО ИТЕРАЦИИ — где мы, куда едем, почему стоим. Один взгляд вместо чтения дневника.

Запуск:  python3 tablo.py <папка итерации> [--bez-zapisi] [--seychas ГГГГ-ММ-ДДTЧЧ:ММ] [--vygruzka <db>]
         → печать + <итерация>/TABLO.md  (--bez-zapisi: только печать, файл не трогать; --seychas: часы для проверки)
Источник: <итерация>/ITERACIYA.json — фазы с полями id, faza, status ('готово'|'сейчас'|'ждёт'|'стоп'|'не нужно'),
          pochemu (для 'стоп' и 'ждёт' — ОБЯЗАТЕЛЬНО: чего ждём и от кого), artefakt (путь или шаблон пути от папки итерации);
          nachalo — начало пары, 'ГГГГ-ММ-ДДTЧЧ:ММ' по Москве (нужно для гейта Ф9).
Рычаг: фаза «готово» без существующего артефакта печатается КРАСНЫМ (❗) — отметка без файла не считается.
Гейт «предсказание → факт» (Ф9 и Ф14; артефакты берутся из FAZY, а не из JSON; молча пропустить нельзя):
  Ф9  ❗ статус «не нужно»; нет `nachalo`; «готово» при красном `predskazanie.py proverit`; пара началась, а предсказания
      PREDSKAZANIE.csv нет, оно не прошло proverit или не доказано гитом (коммит раньше `nachalo`, файл чист против HEAD).
  Ф14 ❗ статус «не нужно»; отметки работ этой итерации в выгрузке бота есть, а SVERKA.md нет.
      Работы итерации — работы выгрузки с датой из имени папки (ГГГГ-ММ-ДД_…). Нет выгрузки — строка «не проверено», не красное.
Выход ≠ 0, если есть красное. Фазы по умолчанию — FAZY; новая итерация получает их из novaya.py.
"""
import argparse, json, sys, glob
from datetime import datetime
from pathlib import Path
FAZY = [
 ('Ф0', 'Вход: интервью владельца — тема, рамка, игровое занятие или нет (чередуем через одно); ответы дословно, решения — в docs/RESHENIYA.md', 'INTERVYU.md'),
 ('Ф1', 'Замер прошлой итерации (svod.py) — отсечка, израсходованные идеи', '../*/SVOD.md'),
 ('Ф2', 'Числа: пункты, минуты, принимающие, целевые доли', 'ITERACIYA.json'),
 ('Ф3', 'Границы темы (объект в ОТВЕТЕ) и словарь идей', 'SLOVAR-idej.md'),
 ('Ф4', 'Пул из источников: карточки с полями', 'PUL.md'),
 ('Ф5', 'Скелет: контрольная · обязательные ○/△ · дополнительные · ДЗ', 'SKELET.md'),
 ('Ф6', 'Отбор (METOD-otbora-zadach) и утверждение блоками: контрольная → ○ → △ → доп → карта → ДЗ → шпаргалка', 'SOSTAV.md'),
 ('Ф7', 'Ответы перебором — скрипты в папке итерации', 'out/kanon.json'),
 ('Ф8', 'Вёрстка: листок А/Б, контрольная, ДЗ (listok_gen.py; перелив ≤ 0; proverka.py зелёный)', 'out/LISTOK-*-A.pdf'),
 ('Ф8к', 'Карта (игровое занятие): граф вверх, один выход у клетки, симуляция (kvest.py)', 'out/*kvest*.json'),
 ('Ф9', 'Предсказание по пунктам и аватарам — ДО урока (predskazanie.py zagotovka → proverit → коммит до nachalo)', 'PREDSKAZANIE.csv'),
 ('Ф10', 'Шпаргалка принимающего', 'out/SHPARGALKA-*.pdf'),
 ('Ф10с', 'Слепая проверка комплекта субагентом (решить сам · условия · шаблоны и карта глазами ребёнка · вёрстка)', 'SLEPAYA-PROVERKA.md'),
 ('Ф11', 'Урок: выдача, приём, скан всех работ', 'SKAN*.pdf'),
 ('Ф12', 'Разметка сканов (razmetka.py → субагенты)', 'RAZMETKA*.jsonl'),
 ('Ф13', 'Свод (svod.py): баллы, разрешение, надёжность, лагерь/вершина', 'SVOD.md'),
 ('Ф14', 'Сверка: предсказание против факта по аватарам (sverka.py), решения, хвост в следующую итерацию', 'SVERKA.md'),
]
GEYT = {i: a for i, f, a in FAZY if i in ('Ф9', 'Ф14')}      # artefacts of the gate phases: fixed here, not read from the JSON
ZNAK = {'готово': '✓', 'сейчас': '▶', 'ждёт': '⏸', 'стоп': '⛔', 'не нужно': '–'}


def _db(vygruzka):
    import sverka
    p = Path(vygruzka or sverka.VYGRUZKA)
    return sverka.otkryt(p) if p.exists() else None


def gejt_f9(it, f, seychas, db):
    """Reasons why phase Ф9 is red (empty list = fine)."""
    import predskazanie
    if f['status'] == 'не нужно':
        return ['статус «не нужно» запрещён: предсказание обязательно к каждой паре']
    n = predskazanie.nachalo(it)
    if n is None:
        return ['в ITERACIYA.json нет `nachalo` (ГГГГ-ММ-ДДTЧЧ:ММ) — без него «до урока» не доказать']
    est = (it / predskazanie.IMYA).exists()
    ok, err, _, _ = predskazanie.proverit(it, db, git=True, pisat_md=False) if est else (False, [f'нет {predskazanie.IMYA}'], [], [])
    if f['status'] == 'готово' and not ok:
        return ['«готово», а `predskazanie.py proverit --git` красный: ' + err[0]]
    if seychas >= n and not ok:
        return [f'пара началась ({n:%Y-%m-%d %H:%M}), а предсказания нет или оно не принято: ' + err[0]]
    return []


def raboty_iteracii(it, db):
    """Works of the export with marks whose date is the date in the folder name."""
    import sverka
    data = it.name[:10]
    return [w['id'] for w in sverka.raboty(db) if w['data'] == data and sverka.otmetki_est(db, w['id'])]


def gejt_f14(it, f, db):
    """(reasons, note): note is printed when the phase cannot be checked."""
    if f['status'] == 'не нужно':
        return ['статус «не нужно» запрещён: сверка обязательна после каждой пары'], ''
    if db is None:
        return [], 'Ф14 не проверена: нет выгрузки бота (bot-7i/data/vygruzka.db) — есть ли отметки работ итерации, неизвестно'
    ws = raboty_iteracii(it, db)
    if ws and not (it / 'SVERKA.md').exists():
        return [f'отметки в выгрузке есть ({", ".join(ws)}), а SVERKA.md нет — `python3 sverka.py <папка итерации>`'], ''
    return [], ''


def main(it, zapis=True, seychas=None, vygruzka=None):
    it = Path(it); J = json.load(open(it / 'ITERACIYA.json', encoding='utf-8'))
    seychas = seychas or datetime.now().astimezone()
    db = _db(vygruzka)
    out = [f"# ТАБЛО · {J.get('tema', it.name)} · {J.get('data', '')}", '',
           f"**Сейчас:** {J.get('seychas', '—')}", '', '| | фаза | что | артефакт | почему стоим |', '|---|---|---|---|---|']
    krasnyh = 0; zametki = []
    for f in J['fazy']:
        art = GEYT.get(f['id'], f.get('artefakt', '')); est = bool(art) and bool(glob.glob(str(it / art)))
        z = ZNAK.get(f['status'], '?')
        if f['status'] == 'готово' and art and not est: z = '❗'; krasnyh += 1
        why = f.get('pochemu', '')
        if f['status'] in ('ждёт', 'стоп') and not why: why = '❗ НЕ УКАЗАНО — дописать, чего ждём и от кого'; krasnyh += 1
        if f['id'] in GEYT:
            if f['id'] == 'Ф9': prich, zam = gejt_f9(it, f, seychas, db), ''
            else: prich, zam = gejt_f14(it, f, db)
            if zam: zametki.append(zam)
            if prich:
                if z != '❗': krasnyh += 1
                z = '❗'; why = (why + ' · ' if why else '') + '❗ ' + '; '.join(prich)
        out.append(f"| {z} | {f['id']} | {f['faza']} | `{art}`{'' if est or not art else ' (нет файла)'} | {why} |")
    if zametki: out += [''] + [f'⚠ {z}' for z in zametki]
    if J.get('otkryto'): out += ['', '## Открытые вопросы владельцу', ''] + [f'- {q}' for q in J['otkryto']]
    txt = '\n'.join(out) + '\n'
    if zapis: (it / 'TABLO.md').write_text(txt, encoding='utf-8')
    print(txt)
    if krasnyh: print(f'❗ красных: {krasnyh}'); sys.exit(1)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('papka'); ap.add_argument('--bez-zapisi', action='store_true')
    ap.add_argument('--seychas', help='ГГГГ-ММ-ДДTЧЧ:ММ по Москве — часы для проверки гейта'); ap.add_argument('--vygruzka')
    a = ap.parse_args()
    sey = None
    if a.seychas:
        import predskazanie
        sey = datetime.fromisoformat(a.seychas); sey = sey if sey.tzinfo else sey.replace(tzinfo=predskazanie.MSK)
    main(a.papka, zapis=not a.bez_zapisi, seychas=sey, vygruzka=a.vygruzka)
