from itertools import combinations, permutations
R=[]
def ok(i,c,msg=''): R.append((i,bool(c),msg)); print(('OK ' if c else 'XX ')+i, msg)
isp=lambda n:n>1 and all(n%d for d in range(2,n))
ds=lambda n:n//10+n%10
two=range(10,100)
P=[n for n in two if isp(ds(n))]
ok('V1',len(P)==33,len(P))
g=[sum(1 for n in two if ds(n)==s) for s in (2,3,5,7,11,13,17)]
ok('V2',g==[2,3,5,7,8,6,2],g)
ok('E1',len(two)==90)
rows=["85 76 38 43 20 58 14 50 89 49 83","65 56 30 94 16 41 23 67 92 25 32","34 47 52 61 25 11 12 29 74 98 21"]
L=[[int(x) for x in r.split()] for r in rows]; F=sum(L,[])
ok('V3',len(F)==33 and all(len(r)==11 for r in L))
from collections import Counter
c=Counter(F); dup=[k for k,v in c.items() if v>1]
ok('V4',dup==[25] and c[25]==2 and len(c)==32,(dup,len(c)))
miss=sorted(set(P)-set(F)); extra=sorted(set(F)-set(P))
ok('V5',miss==[70] and extra==[],(miss,extra))
pos=[(i+1,j+1) for i,r in enumerate(L) for j,x in enumerate(r) if x==25]
ok('V6',pos==[(2,10),(3,5)],pos)
s7=[x for x in F if ds(x)==7]
ok('V7',s7==[43,16,25,34,52,61,25],s7)
srt=sorted(set(F)); i=srt.index(67)
ok('V8',srt[i+1]==74)
rw=[sum(1 for n in P if n//10==d) for d in range(1,10)]
ok('V9',rw==[4,5,4,4,4,3,3,3,3] and sum(rw)==33,rw)
v2=sorted(x for x in F if x//10==2); v7=sorted(x for x in F if x//10==7)
ok('V10',v2==[20,21,23,25,25,29] and v7==[74,76],(v2,v7))
bad=[d for d in range(1,10) if sorted(x for x in F if x//10==d)!=[n for n in P if n//10==d]]
ok('V10b(only rows 2,7 wrong)',bad==[2,7],bad)
ok('V11',[n for n in P if n//10==2]==[20,21,23,25,29] and [n for n in P if n//10==7]==[70,74,76])
S=[n for n in two if ds(n)==7]
ok('S1',S==[16,25,34,43,52,61,70])
ok('S2',all(S[k+1]-S[k]==9 for k in range(6)) and len(range(62,71))==9)
ok('S3',len(range(71,100))==29 and not any(ds(n)==7 for n in range(71,100)))
rev=[n for n in S if n%10!=0 and (n%10)*10+n//10 in S]
ok('S4',len(rev)==6 and 70 not in rev,rev)
ok('S5',[ (a,7-a) for a in range(1,10) if 0<=7-a<=9]==[(a,7-a) for a in range(1,8)])
D6=[n for n in two if abs(n//10-n%10)==6]
ok('S6',D6==[17,28,39,60,71,82,93],D6)
seq=[17,28,39,50]; ok('S7',[x for x in seq if x in D6]==[17,28,39] and abs(5-0)==5 and len(D6)-3==4)
cut={a:[b for b in range(10) if abs(a-b)==6] for a in range(1,10)}
ok('S8',cut=={1:[7],2:[8],3:[9],4:[],5:[],6:[0],7:[1],8:[2],9:[3]},cut)
A4='АБВГ'; A5='АБВГД'
pairs4=[''.join(p) for p in combinations(A4,2)]
ok('P1',pairs4==['АБ','АВ','АГ','БВ','БГ','ВГ'])
robot=[x+y for x in A4 for y in A4 if x!=y]
ok('P2',' '.join(robot)=='АБ АВ АГ БА БВ БГ ВА ВБ ВГ ГА ГБ ГВ' and len(robot)==12 and robot[3]=='БА' and all(len(set(frozenset(r) for r in robot[:k]))==k for k in (1,2,3)),robot)
ok('P3',all(v==2 for v in Counter(frozenset(r) for r in robot).values()))
fix=[x+y for x in A4 for y in A4 if A4.index(y)>A4.index(x)]
ok('P4',fix==pairs4 and [sum(1 for p in fix if p[0]==x) for x in 'АБВ']==[3,2,1])
ok('P5',len(list(permutations(A4,2)))==12)
# P6 "по кругу" on 4: neighbors around circle AB BV VG GA
circ=['АБ','БВ','ВГ','ГА']; missing=[p for p in pairs4 if frozenset(p) not in {frozenset(x) for x in circ}]
ok('P6',len(circ)==4 and missing==['АВ','БГ'],missing)
pairs5=[''.join(p) for p in combinations(A5,2)]
ok('P7',len(pairs5)==10 and [sum(1 for p in pairs5 if p[0]==x) for x in 'АБВГ']==[4,3,2,1])
nx=lambda lst,x: lst[lst.index(x)+1] if lst.index(x)+1<len(lst) else 'END'
ok('P8',[nx(pairs5,x) for x in ['АГ','АД','БГ','ВД','ГД']]==['АД','БВ','БД','ГД','END'])
Fl=[''.join(p) for p in permutations('БКС')]
ok('F1',Fl==['БКС','БСК','КБС','КСБ','СБК','СКБ'])
ok('F2',sum(1 for a in 'БКС' for b in 'БКС' if a!=b)==6)
ok('F3',[nx(Fl,x) for x in ['БСК','КСБ','СКБ']]==['КБС','СБК','END'])
sh=['БКС']; 
for _ in range(3): s=sh[-1]; sh.append(s[1:]+s[0])
ok('F4',sh==['БКС','КСБ','СБК','БКС'],sh)
ok('F5','КБС'!='БКС')
T=[''.join(p) for p in combinations(A5,3)]
ok('T1',' '.join(T)=='АБВ АБГ АБД АВГ АВД АГД БВГ БВД БГД ВГД')
ok('T2',[sum(1 for t in T if t[0]==x) for x in 'АБВ']==[6,3,1])
ok('T3',[nx(T,x) for x in ['АБД','АГД','АВД','БВД','БГД','ВГД']]==['АВГ','БВГ','АГД','БГД','ВГД','END'])
rest=lambda drop:[p for p in pairs5 if not set(p)&set(drop)]
ok('T4',['А'+p for p in rest('А')]==T[:6] and rest('АБ')==['ВГ','ВД','ГД'] and rest('АБВ')==['ГД'])
# T5 hold two first, vary third -> same lex list
ok('T5',sorted(T)==T)
comp={t:''.join(x for x in A5 if x not in t) for t in T}
ok('T6',len(T)==len(pairs5)==10 and len(set(comp.values()))==10)
ok('T7',sorted('ВБА')==sorted('АБВ'))
K=[(6,b,a) for b in range(1,6) for a in range(1,b) if a+b>6]
ok('K1',K==[(6,5,4),(6,5,3),(6,5,2),(6,4,3)],K)
flat=[(6,b,a) for b in range(1,6) for a in range(1,b) if a+b==6]
ok('K2',flat==[(6,5,1),(6,4,2)],flat)
ok('K3',len([1 for b in range(1,6) for a in range(1,b)])==10)
ok('K4',2*len(K)==8)
ok('K5',[sum(1 for t in K if t[1]==m) for m in (5,4,3)]==[3,1,0])
ok('K6',sorted(tuple(sorted(t)) for t in K)==[(2,5,6),(3,4,6),(3,5,6),(4,5,6)])
K7=[(5,b,a) for b in range(1,5) for a in range(1,b) if a+b>5]
ok('K7',K7==[(5,4,3),(5,4,2)],K7)
ok('K8',sorted((6,4,5))==sorted((6,5,4)))
ok('G1',[len(S),len(pairs4),len(pairs5),6,len(T),len(K),len(K7),len(D6)]==[7,6,10,6,10,4,2,7])
m=[1.5,3.5,5.5,2,5,1.5,4]; import itertools
cum=list(itertools.accumulate(m))
ok('H1',sum(m)==23 and cum==[1.5,5,10.5,12.5,17.5,19,23],cum)
# extras
ok('E2(4 броска с АГД)', len(T)-1-T.index('АГД'), 'objects named after АГД = %d (+1 бросок "всё")'%(len(T)-1-T.index('АГД')))
print('   E2 detail: objects after АГД =',len(T)-1-T.index('АГД'))
print('   E3 detail: pairs of 4 throws from АБ given =',len(pairs4)-1,'+ всё')
pairs5_throws=len(pairs5)-1+1+2; flags=len(Fl)-1+1+1; tr=len(T)-1+1+2
print('   E4 throws: pairs5',pairs5_throws,'flags',flags,'triples',tr,'sum',pairs5_throws+flags+tr)
ok('E9',21+3+0.5<=25 and 0.25+3+0.5<=4)
ok('E10',(10+40+15+120+10+120)/60<=5.5,(10+40+15+120+10+120)/60)
