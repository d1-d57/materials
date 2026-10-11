import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
from itertools import combinations as C
def circ(n,jit=None,rot=90):
    a=np.deg2rad(rot+np.arange(n)*360/n)
    if jit is not None: a=a+np.deg2rad(jit)
    return np.c_[np.cos(a),np.sin(a)]
sets={
 'K6 правильный':circ(6),
 'K6 по кругу неравномерно':circ(6,jit=np.array([0,12,-8,20,-5,9])),
 'K6 вразброс (невыпукло)':np.array([[0,1],[0.9,0.55],[0.55,-0.85],[-0.7,-0.6],[-0.95,0.4],[0.1,0.05]]),
 'K7 правильный':circ(7),
 'K5 правильный':circ(5),
}
fig,ax=plt.subplots(1,5,figsize=(20,4.4))
for a,(k,P) in zip(ax,sets.items()):
    for i,j in C(range(len(P)),2): a.plot(*P[[i,j]].T,'k-',lw=1.2)
    a.plot(*P.T,'o',ms=9,color='C3'); a.set_title(k,fontsize=13); a.set_aspect('equal'); a.axis('off')
plt.tight_layout(); plt.savefig('fig/variants.png',dpi=80)
# segment-crossing counts: interior intersection points (distinct), and coincidences
def inter(P):
    segs=list(C(range(len(P)),2)); pts=[]
    for (a,b),(c,d) in C(segs,2):
        if len({a,b,c,d})<4: continue
        p,r=P[a],P[b]-P[a]; q,s=P[c],P[d]-P[c]; den=r[0]*s[1]-r[1]*s[0]
        if abs(den)<1e-12: continue
        t=((q-p)[0]*s[1]-(q-p)[1]*s[0])/den; u=((q-p)[0]*r[1]-(q-p)[1]*r[0])/den
        if 1e-9<t<1-1e-9 and 1e-9<u<1-1e-9: pts.append(tuple(np.round(p+t*r,6)))
    from collections import Counter
    c=Counter(pts); return len(pts),len(c),max(c.values()) if c else 0
for k,P in sets.items(): print(k,'пар пересечений, различных точек, макс кратность:',inter(P))
