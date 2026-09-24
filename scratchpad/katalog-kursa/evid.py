import re, sys, pathlib
KEY = re.compile(r'(УСТАРЕЛ|устарел|ЗАБРАКОВАН|забракован|отменён|Отменён|ОТМЕНЁН|отменено|МИШЕНЬ|порожда|генерир|Сгенерир|сгенерир|собирается|АРХИВ|ядовит|нельзя читать|принят|Принят|chernovik|zhivoy|status:|Состояние|СОСТОЯНИЕ|дубль|Дубль)')
files = [l.strip() for l in sys.stdin if l.strip()]
for f in files:
    p = pathlib.Path(f)
    t = p.read_text(encoding='utf-8', errors='replace').splitlines()
    print('=' * 100)
    print(f, '|', p.stat().st_size, 'bytes |', len(t), 'lines')
    for i, l in enumerate(t[:9], 1):
        print('  H%02d| %s' % (i, l[:150]))
    n = 0
    for i, l in enumerate(t[9:], 10):
        if KEY.search(l):
            print('  L%03d| %s' % (i, l[:190]))
            n += 1
            if n >= 7: break
