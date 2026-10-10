import re, sys, statistics
def load(p):
    t = open(p, encoding='utf-8').read()
    t = re.sub(r'\A---\n.*?\n---\n', '', t, flags=re.S)          # frontmatter
    return t
def sections(t):
    parts = re.split(r'^## (.+)$', t, flags=re.M)
    out = [('(вступление)', parts[0])]
    for i in range(1, len(parts), 2):
        out.append((parts[i].strip(), parts[i+1]))
    return out
def clean(par):
    par = re.sub(r'\$\$.*?\$\$', ' ', par, flags=re.S)            # display math
    par = re.sub(r'\$[^$]*\$', ' ', par)                          # inline math
    par = re.sub(r'<[^>]+>', ' ', par)                            # html
    par = re.sub(r'\{\{.*?\}\}', ' ', par, flags=re.S)            # widgets
    par = re.sub(r'\*\*(Задача|Утверждение|Определение|Теорема) \d+[^*]*\*\*', ' ', par)  # block headers
    return par
def prose_pars(body):
    pars = [p.strip() for p in re.split(r'\n\s*\n', body) if p.strip()]
    res = []
    for p in pars:
        if p.startswith('#') or p.startswith('|') or p.startswith('{{'): continue
        c = clean(p)
        if len(re.findall(r'[А-Яа-яЁё]+', c)) < 3: continue
        res.append(c)
    return res
def sentences(text):
    text = re.sub(r'\s+', ' ', text)
    ss = re.split(r'(?<=[.!?…])\s+(?=[«(А-ЯЁA-Z*0-9])', text)
    return [s for s in ss if re.search(r'[А-Яа-яЁё]', s)]
def words(s): return re.findall(r'[А-Яа-яЁёA-Za-z0-9]+(?:-[А-Яа-яЁё]+)?', s)
for p in sys.argv[1:]:
    t = load(p)
    secs = sections(t)
    allS = []
    print('=='*10, p.split('/')[-1])
    for name, body in secs:
        pp = prose_pars(body)
        for par in pp: allS += sentences(par)
        print(f'  {name[:40]:40s} абзацев {len(pp):2d}')
    L = [len(words(s)) for s in allS]
    print('  разделов', len(secs)-1, '| абзацев прозы', sum(len(prose_pars(b)) for _,b in secs))
    print('  предложений', len(L), '| слов', sum(L), '| средн. длина %.1f' % statistics.mean(L),
          '| медиана', statistics.median(L), '| >25 слов: %d (%.0f%%)' % (sum(x>25 for x in L), 100*sum(x>25 for x in L)/len(L)))
    for kw in ['Задача','Утверждение','Определение','Теорема']:
        print('  блок', kw, len(re.findall(r'^\*\*'+kw+r' \d+', t, flags=re.M)))
    print('  виджетов {{S/R}}', len(re.findall(r'\{\{[SR]:', t)))
    for kw in ['Например','Теперь','Вернёмся','Посчитаем','Разберём','Ответ','Способ','Порядок','С одной стороны','Значит','Так же','Похоже','в общем случае']:
        print('  «%s»: %d' % (kw, len(re.findall(kw, t, flags=re.I))))
