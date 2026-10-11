# Сводный анализ сдачи 29.09: ДЗ к 29.09 + контрольная 29.09. Запуск: python3 analiz_29-09.py <папка итерации>
# Вход: RAZMETKA-DZ-k-29-09.jsonl (+ правила svod_dz.py), OTSENKA-KR-29-09.json, ../../SPISOK-7I.txt
import json,re,sys,collections,os
D=sys.argv[1]; K={'1':8,'2':14,'3':34,'4':22,'5':12}
def num(s):
    m=re.findall(r'\d+',str(s).split('|')[-1]); return int(m[-1]) if m else None
dz={}
for l in open(f'{D}/RAZMETKA-DZ-k-29-09.jsonl'):
    r=json.loads(l); z=''
    for p in '12345':
        v=num(r['n'][p]) if p in r.get('n',{}) else None; sp=(r.get('spisok') or {}).get(p)
        ok=(sp==K[p]) if (p in '45' and sp) else (v==K[p])
        z+='+' if ok else ('.' if p not in r.get('n',{}) and not sp else '-')
    dz[r['imya']]=z
LS={}
if os.path.exists(f'{D}/SDACHA.csv'):
    import csv
    H=None; rows_=[]
    for row in csv.reader(open(f'{D}/SDACHA.csv',encoding='utf-8'),delimiter=';'):
        if row and row[0]=='фамилия_имя': H=row; continue
        if H and row: rows_.append(dict(zip(H,row)))
    for r in rows_:
        ok=lambda k: r.get(k,'') in ('+','в')
        LS[r['фамилия_имя']]={'vsego':int(r['зачтено']),'o':sum(ok(k) for k in ['1','2а','2б','2в','3а','3б','3в','4а','4б','5']),
            't':sum(ok(k) for k in ['6','7','8']),'per':ok('1') and ok('5'),'ie':ok('3в'),'ie8':ok('8')}
KR=json.load(open(f'{D}/OTSENKA-KR-29-09.json'))['deti']
spisok=[' '.join(l.split()[:2]).replace('Федор','Фёдор') for l in open(f'{D}/../../SPISOK-7I.txt') if l.strip() and not l.startswith('#')]
print('класс',len(spisok),'| сдали ДЗ',len(dz),'| писали КР',len(KR))
print('не сдали ДЗ:',', '.join(x for x in spisok if x not in dz))
print('нет листка:',', '.join(x for x in spisok if LS and x not in LS))
print('не писали КР:',', '.join(x for x in spisok if x not in KR))
P=['1','2а','2б','3а','3б','4а','4б']
print('\nКР, верно по пунктам (из писавших):')
for i,p in enumerate(P):
    c=collections.Counter(v[1][i] for v in KR.values()); print(f'  {p:3s} +{c["+"]:2d}  −{c["-"]:2d}  пусто {c["."]:2d}')
print('\nДЗ, верно по задачам:',{p:sum(z[i]=='+' for z in dz.values()) for i,p in enumerate('12345')},'из',len(dz))
# пары «одинаковый приём»: ДЗ-задача → пункт КР
PARY=[('1','2б','включения-исключения'),('2','3а','квадраты на доске'),('3','4а','палочки: перебор троек')]
print('\nОдин приём в ДЗ и КР (только сдавшие оба):')
for d,k,t in PARY:
    i=P.index(k); both=[x for x in dz if x in KR]
    c=collections.Counter((dz[x][int(d)-1]=='+', KR[x][1][i]=='+') for x in both)
    print(f'  {t:22s} ДЗ+КР+ {c[(True,True)]:2d} | ДЗ+КР− {c[(True,False)]:2d} | ДЗ−КР+ {c[(False,True)]:2d} | ДЗ−КР− {c[(False,False)]:2d}')
print('\nДети: листок (○ из 10, △ из 3, всего из 33) · ДЗ (из 5) · КР (из 7) · «ДЗ+, КР−» по парам приёмов')
rows=[]
for x in spisok:
    a=dz.get(x); b=KR.get(x)
    sa=a.count('+') if a else None; sb=b[1].count('+') if b else None
    drop=[t for d,k,t in PARY if a and b and a[int(d)-1]=='+' and b[1][P.index(k)]!='+']
    rows.append((x,a,sa,b[1] if b else None,sb,drop))
for x,a,sa,b,sb,drop in sorted(rows,key=lambda r:(-(r[4] if r[4] is not None else -1),-(r[2] or 0))):
    l=LS.get(x); lt=f"Л ○{l['o']:2d} △{l['t']} Σ{l['vsego']:2d}" if l else 'Л —          '
    print(f'  {x:26s} {lt}  ДЗ {a or "—":5s} {sa if sa is not None else "—"}  КР {b or "—":7s} {sb if sb is not None else "—"}  {"; ".join(drop)}')

if LS:
    both=[x for x in LS if x in KR]
    print('\nЛисток (на уроке, с помощью принимающих) → КР (сам), по приёму:')
    for t,lk,ki in (('включения-исключения: листок 3в → КР 2б','ie',2),('перебор-список: листок 1 и 5 → КР 4а','per',5)):
        c=collections.Counter((LS[x][lk], KR[x][1][ki]=='+') for x in both)
        print(f'  {t:44s} Л+К+ {c[(True,True)]:2d} | Л+К− {c[(True,False)]:2d} | Л−К+ {c[(False,True)]:2d} | Л−К− {c[(False,False)]:2d}')
