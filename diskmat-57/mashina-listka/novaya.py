# -*- coding: utf-8 -*-
"""НОВАЯ ИТЕРАЦИЯ — завести папку под новую тему одной командой.
Запуск:  python3 novaya.py <папка арки> <ГГГГ-ММ-ДД> <слаг-темы> "<Тема полностью>" [<начало пары ГГГГ-ММ-ДДTЧЧ:ММ>]
Создаёт  <арка>/iteracii/<дата>_<слаг>/ : ITERACIYA.json (все фазы из tablo.FAZY, статус «ждёт», поле nachalo — начало пары,
         по умолчанию <дата>T15:30 — владелец поправляет; от него считается гейт Ф9 «предсказание до урока»), dannye.py (шаблон),
         и печатает табло. Игровое занятие чередуется САМО: igrovoe = не(igrovoe прошлой итерации) — решение владельца
         29.09 «геймификация через одно»; владелец может переопределить на Ф0.
"""
import json, sys, shutil, glob
from pathlib import Path
M = Path(__file__).resolve().parent
sys.path.insert(0, str(M)); import tablo
def main(arka, data, slug, tema, nachalo=None):
    arka = Path(arka); it = arka / 'iteracii' / f'{data}_{slug}'
    assert not it.exists(), f'уже есть: {it}'
    prev = sorted(p for p in (arka / 'iteracii').glob('*_*') if p.is_dir())
    igr_prev = json.load(open(prev[-1] / 'ITERACIYA.json', encoding='utf-8')).get('igrovoe', False) if prev else False
    (it / 'out').mkdir(parents=True)
    shutil.copy(M / 'shablon' / 'dannye_shablon.py', it / 'dannye.py')
    J = dict(tema=tema, data=data, nachalo=nachalo or f'{data}T15:30', igrovoe=not igr_prev, seychas='Ф0: интервью владельца — тема, рамка, числа.',
             stranic={}, SOVPADENIE_OK=[],
             fazy=[dict(id=i, faza=f, status='ждёт', pochemu='не начато', artefakt=a) for i, f, a in tablo.FAZY],
             otkryto=[f'Игровое занятие: по чередованию — {"да" if not igr_prev else "нет"} (прошлое: {"да" if igr_prev else "нет"}). Подтвердить.'])
    J['fazy'][0].update(status='сейчас', pochemu='')
    if not J['igrovoe']: J['fazy'][[f['id'] for f in J['fazy']].index('Ф8к')].update(status='не нужно', pochemu='занятие без карты')
    json.dump(J, open(it / 'ITERACIYA.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'заведено: {it}'); tablo.main(it)
if __name__ == '__main__':
    main(*sys.argv[1:])
