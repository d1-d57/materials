# одноразовый: собирает новый текст ленты, рисунки берёт из текущего lenta.md без изменений
import re
s=open('lenta.md',encoding='utf-8').read()
figs=re.findall(r'<figure>.*?</figure>', s, flags=re.S)
assert len(figs)==5, len(figs)
T=open('_novyj_tekst.md',encoding='utf-8').read()
out=[]; i=0
while True:
    j=T.find('{{FIG',i)
    if j<0: out.append(T[i:]); break
    k=T.find('}}',j); n=int(T[j+5]); cap=T[j+7:k]
    f=re.sub(r'<figcaption>.*?</figcaption>', lambda m:'<figcaption>'+cap+'</figcaption>', figs[n-1], flags=re.S)
    out.append(T[i:j]); out.append(f); i=k+2
R=''.join(out); assert R.count('<figure>')==5
open('lenta.md','w',encoding='utf-8').write(R); print('ok')
