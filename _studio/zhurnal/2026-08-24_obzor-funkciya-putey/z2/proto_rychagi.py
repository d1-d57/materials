import re,sys
LBL=re.compile(r"^\*\*(Теорема|Лемма|Предложение|Утверждение)\s+\S+?[^*]*\*\*\s*",re.S)
def bloki(t): return [b.strip() for b in re.split(r"\n\s*\n",t) if b.strip()]
def words(s):
    s=re.sub(r"\$[^$]*\$","x",s); s=re.sub(r"<[^>]+>"," ",s)
    return len(re.findall(r"[\wА-Яа-яЁё]+",s))
for p in sys.argv[1:]:
    t=open(p,encoding='utf-8').read(); B=bloki(t); r1=[];r2=[]
    for i,b in enumerate(B):
        m=LBL.match(b)
        if not m: continue
        rest=b[m.end():].strip(); j=i+1
        if not rest and j<len(B): rest=B[j]; j+=1
        if rest.startswith("$$"): r2.append(b[:50].replace("\n"," "))
        # next prose block after statement (skip $$ blocks and поле)
        k=i+1
        while k<len(B) and (B[k].startswith("$$") or B[k].startswith("> поле") or (k==i+1 and not b[m.end():].strip())): k+=1
        if k<len(B) and B[k].startswith("Например"): r1.append(b[:50].replace("\n"," "))
    caps=[c for c in re.findall(r"\{\{R:[^|}]*\|([^}]*)\}\}",t)]+re.findall(r"<figcaption[^>]*>(.*?)</figcaption>",t,re.S)
    cw=sorted(words(c) for c in caps)
    print(p.split('GitHub/')[-1][-70:], "| Например:",len(r1),"| голая формула:",len(r2),"| подписи слов:",cw[-5:], r1[:2], r2[:2])
