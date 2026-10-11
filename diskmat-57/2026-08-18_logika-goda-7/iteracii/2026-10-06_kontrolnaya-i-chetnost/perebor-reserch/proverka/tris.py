import numpy as np
from itertools import combinations as C
exec(open('fig.py').read().split("fig,ax")[0])
def count(P):
    segs=list(C(range(len(P)),2)); pts=[tuple(np.round(p,6)) for p in P]
    on={s:set() for s in segs}
    for k,(a,b) in enumerate(segs): on[(a,b)]|={pts[a],pts[b]}
    for (a,b),(c,d) in C(segs,2):
        if len({a,b,c,d})<4: continue
        p,r=P[a],P[b]-P[a]; q,s=P[c],P[d]-P[c]; den=r[0]*s[1]-r[1]*s[0]
        if abs(den)<1e-12: continue
        t=((q-p)[0]*s[1]-(q-p)[1]*s[0])/den; u=((q-p)[0]*r[1]-(q-p)[1]*r[0])/den
        if 1e-9<t<1-1e-9 and 1e-9<u<1-1e-9:
            x=tuple(np.round(p+t*r,6)); on[(a,b)].add(x); on[(c,d)].add(x)
    allp=set().union(*on.values())
    def link(x,y): return [s for s in segs if x in on[s] and y in on[s]]
    n=0
    for x,y,z in C(allp,3):
        l1,l2,l3=link(x,y),link(y,z),link(x,z)
        if l1 and l2 and l3 and not (set(l1)&set(l2)&set(l3)): n+=1
    return n
for k,P in sets.items(): print(k,'треугольников на рисунке (любые вершины):',count(P))
