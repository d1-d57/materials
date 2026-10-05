import re,json
figs=json.load(open('figs.json'))
s=open('istochnik.md').read()
def rep(m):
    name,cap,st=m.group(1).split('::')
    svg=figs[name].replace('<svg','<svg',1)
    return '<figure>\n<!-- %s -->\n%s\n<figcaption>%s</figcaption>\n</figure>'%(st.strip(),svg,cap)
s=re.sub(r'\{\{FIG:(.*?)\}\}',rep,s)
assert '{{' not in s
open('lenta.md','w').write(s)
print(len(s))
