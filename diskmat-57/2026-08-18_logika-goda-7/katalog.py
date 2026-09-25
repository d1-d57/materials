import re, json, glob, os, unicodedata
from collections import Counter, defaultdict

FILES = sorted(glob.glob('SYRYO-22-09_*.md'))
FIELDS = ['УСЛОВИЕ','ОТВЕТ','МЕТОД','ПРОИЗВЕДЕНИЕ','ПУНКТЫ','ДОЛЯ','ХОД','НЕ ВЫГЛЯДИТ','ТОВАР','КАРТИНКА','ПРИМЕЧАНИЕ']

def parse(path):
    txt = open(path, encoding='utf-8').read()
    cards = []
    chunks = re.split(r'\n(?=### )', txt)
    for ch in chunks:
        if not ch.startswith('### '): continue
        head = ch.split('\n',1)[0][4:].strip()
        body = ch.split('\n',1)[1] if '\n' in ch else ''
        card = {'src': path.replace('SYRYO-22-09_','').replace('.md',''), 'id': head}
        cur = None
        for line in body.split('\n'):
            m = re.match(r'^\*{0,2}([А-ЯЁ][А-ЯЁ ]{2,30})\*{0,2}\s*:\s*(.*)$', line)
            if m and any(m.group(1).strip().startswith(f) for f in FIELDS):
                cur = m.group(1).strip()
                card[cur] = m.group(2).strip()
            elif cur and line.strip():
                card[cur] = card.get(cur,'') + ' ' + line.strip()
        cards.append(card)
    return cards

def get(card, *prefixes):
    for k,v in card.items():
        if any(k.startswith(p) for p in prefixes): return v
    return ''

def norm_dolya(v):
    v = v.lower()
    if 'почти все' in v or 'почти всё' in v: return 'почти все'
    if 'больше половины' in v: return 'больше половины'
    if 'меньше половины' in v: return 'меньше половины'
    if 'никто' in v: return 'никто'
    if 'единиц' in v: return 'единицы'
    return '?'

def norm_yn(v):
    v = v.strip().lower()
    if v.startswith('да'): return 'да'
    if v.startswith('нет'): return 'нет'
    return '?'

def norm_metod(v):
    v = v.lower()
    for key in ['переход к дополнению','конструктив и оценка','таблица и группы','перечисление']:
        if key in v: return key
    return 'иное'

def has_punkty(v):
    v = v.strip().lower()
    return not (v.startswith('монолит') or v == '' or v.startswith('нет'))

all_cards = []
for f in FILES:
    cs = parse(f)
    for c in cs:
        c['dolya']  = norm_dolya(get(c,'ДОЛЯ'))
        c['hod']    = norm_yn(get(c,'ХОД'))
        c['neko']   = norm_yn(get(c,'НЕ ВЫГЛЯДИТ'))
        c['metod']  = norm_metod(get(c,'МЕТОД'))
        c['punkty'] = has_punkty(get(c,'ПУНКТЫ'))
        c['uslovie']= get(c,'УСЛОВИЕ')
    all_cards += cs
    print(f'{f:42s} карточек {len(cs):3d}')

print(f'\nВСЕГО КАРТОЧЕК: {len(all_cards)}')

# дубли по началу условия
def key(u):
    u = unicodedata.normalize('NFKC', u).lower()
    u = re.sub(r'[^а-яёa-z0-9 ]',' ', u)
    return ' '.join(u.split())[:70]
seen = defaultdict(list)
for c in all_cards: seen[key(c['uslovie'])].append(f"{c['src']}/{c['id']}")
dup = {k:v for k,v in seen.items() if len(v)>1 and k}
print(f'ПОХОЖИХ ПАР (первые 70 знаков условия совпали): {len(dup)}')
for k,v in list(dup.items())[:8]: print('   ', ' == '.join(v), '|', k[:50])

print('\n=== ПО ДОЛЕ КЛАССА ==='); 
for k,n in Counter(c['dolya'] for c in all_cards).most_common(): print(f'  {k:18s} {n:3d}')
print('=== ПО МЕТОДУ ===')
for k,n in Counter(c['metod'] for c in all_cards).most_common(): print(f'  {k:22s} {n:3d}')
print('=== ХОД ВИДЕН СРАЗУ ===')
for k,n in Counter(c['hod'] for c in all_cards).most_common(): print(f'  {k:6s} {n:3d}')
print('=== РАЗБИВАЕТСЯ НА ПУНКТЫ ===')
for k,n in Counter(c['punkty'] for c in all_cards).most_common(): print(f'  {str(k):6s} {n:3d}')
print('=== НЕ ВЫГЛЯДИТ КОМБИНАТОРНОЙ ===')
for k,n in Counter(c['neko'] for c in all_cards).most_common(): print(f'  {k:6s} {n:3d}')

# ПРЕДВАРИТЕЛЬНАЯ РАСКЛАДКА ПО ТИПАМ (механическая, по критериям владельца)
def tip(c):
    d, h, p = c['dolya'], c['hod'], c['punkty']
    if d in ('единицы','никто'): return 'ГРОБ'
    if d == 'меньше половины': return 'РОМБ' if p else 'ромб-монолит'
    if d in ('почти все','больше половины'):
        return 'КРУЖОК' if h == 'да' else 'ТРЕУГОЛЬНИК'
    return '?'
for c in all_cards: c['tip'] = tip(c)
print('\n=== ПРЕДВАРИТЕЛЬНАЯ РАСКЛАДКА ===')
need = {'КРУЖОК':5,'ТРЕУГОЛЬНИК':5,'РОМБ':7,'ГРОБ':3}
for k,n in Counter(c['tip'] for c in all_cards).most_common():
    print(f'  {k:16s} {n:3d}   надо {need.get(k,"-")}')
print('\n=== ИСТОЧНИКИ ПО ТИПАМ ===')
for t in ['КРУЖОК','ТРЕУГОЛЬНИК','РОМБ','ГРОБ']:
    src = Counter(c['src'] for c in all_cards if c['tip']==t)
    print(f'  {t:12s}: ' + ', '.join(f'{k} {v}' for k,v in src.most_common()))
json.dump(all_cards, open('/tmp/pul.json','w'), ensure_ascii=False, indent=1)
print('\nJSON пула: /tmp/pul.json')
