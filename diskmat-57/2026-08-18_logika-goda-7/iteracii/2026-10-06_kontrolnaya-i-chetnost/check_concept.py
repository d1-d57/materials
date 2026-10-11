from math import gcd
def rng(a,b): return list(range(a,b+1))
two=rng(10,99); three=rng(100,999)
ds=lambda n: sum(map(int,str(n)))
r={}
r['17..23']=len(rng(17,23))
r['even 20..80']=len([n for n in rng(20,80) if n%2==0])
r['3d mult 9']=len([n for n in three if n%9==0])
r['3d mult 15']=len([n for n in three if n%15==0])
r['3d mult 45']=len([n for n in three if n%45==0])
r['3d mult 135']=len([n for n in three if n%135==0])
r['3d 9 or 15']=len([n for n in three if n%9==0 or n%15==0])
r['2d sum7']=[n for n in two if ds(n)==7]
r['2d sum13']=[n for n in two if ds(n)==13]
pr={2,3,5,7,11,13,17}
r['2d prime sum']=len([n for n in two if ds(n) in pr])
r['2d has 7']=len([n for n in two if '7' in str(n)])
r['sevens printed 10..99']=sum(str(n).count('7') for n in two)
r['70..79']=len(rng(70,79)); r['x7']=len([n for n in two if n%10==7])
import itertools
fl=[f for f in itertools.product('БКС',repeat=3) if f[0]!=f[1] and f[1]!=f[2]]
r['flags']=len(fl)
r['floors 1->10 flights']=len(rng(2,10))
# 3-digit with digit 5 (R5)
r['3d has 5']=len([n for n in three if '5' in str(n)])
# leaves 87..214
r['leaves 87..214']=len([p for p in rng(87,214) if p%2==1])
for k,v in r.items(): print(k, v if not isinstance(v,list) else (len(v),v))
assert r['17..23']==7 and r['3d 9 or 15']==140 and r['2d prime sum']==33 and r['2d has 7']==18 and r['sevens printed 10..99']==19 and r['flags']==12
print('asserts ok')
# --- все числа страницы KONCEPCIYA-uroka-6-10-v1.html ---
assert len(rng(30,45))==16 and r['even 20..80']==31 and r['3d mult 9']==100 and r['3d mult 15']==60
assert r['3d mult 45']==20 and r['3d mult 135']==7 and len(r['2d sum7'])==7 and 70 in r['2d sum7']
assert len(r['2d sum13'])==6 and 9-4==5 and r['70..79']==10 and r['x7']==9 and r['floors 1->10 flights']==9
assert [n//9 for n in three if n%9==0][::99]==[12,111] and [n//15 for n in three if n%15==0][::59]==[7,66]
assert 2*60+15==9*15 and 60//4==15
print('page numbers ok')
