import re,json,sys
figs=json.load(open('figs.json'))
s=open('asimptota.md').read()
s=re.sub(r'\{\{FIG:(\w+)\}\}',lambda m: figs[m.group(1)],s)
assert '{{' not in s
open('lenta-asimptota.md','w').write(s); print(len(s))
