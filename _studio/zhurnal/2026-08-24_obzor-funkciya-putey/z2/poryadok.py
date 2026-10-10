import re, sys
# для каждого блока Утверждение/Теорема: есть ли конкретный числовой пример ДО (в 2 абзацах перед) и сразу ПОСЛЕ («Например»)
num = re.compile(r'\\binom\{?\d+\}?\{?\d+\}?|\d\^\{\\underline|\b\d+\s*[\\\+=·]|\b\d+\\cdot')
for p in sys.argv[1:]:
    t = re.sub(r'\A---\n.*?\n---\n', '', open(p, encoding='utf-8').read(), flags=re.S)
    pars = [x.strip() for x in re.split(r'\n\s*\n', t) if x.strip()]
    before = after_ex = tot = 0
    wpp = []
    for i, x in enumerate(pars):
        if not x.startswith(('#','|','{{','$$')):
            c = re.sub(r'\$[^$]*\$', ' ', x); wpp.append(len(re.findall(r'[А-Яа-яЁё]+', c)))
        if re.match(r'\*\*(Утверждение|Теорема) \d+', x):
            tot += 1
            prev = ' '.join(pars[max(0,i-2):i])
            if num.search(prev) and not prev.lstrip().startswith('*Доказательство'): before += 1
            nxt = pars[i+1] if i+1 < len(pars) else ''
            if nxt.startswith('Например'): after_ex += 1
    print(p.split('/')[-1], f'утв/теорем {tot}: числовой пример в 2 абзацах ДО — {before}; «Например» сразу ПОСЛЕ — {after_ex}; слов/абзац (без формул) ≈ {sum(wpp)/len(wpp):.1f}, макс {max(wpp)}')
