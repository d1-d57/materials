"""Численная сверка всех тождеств ленты занятия 4 (n до 14) и перечислений из задач."""
from math import comb as C, factorial as f
from itertools import product
N=14; ok=0; bad=[]
def chk(name,cond):
    global ok
    if cond: ok+=1
    else: bad.append(name)
chk('z1', C(8,3)*3*2==8*7*6==336 and C(8,3)==56)
chk('z3', C(5,3)*3==30==5*C(4,2))
for n in range(N+1):
    for k in range(n+1):
        p=1
        for i in range(k): p*=n-i
        chk(f'u2 {n},{k}', C(n,k)*f(k)==p)
        if k>=1: chk(f'u4 {n},{k}', k*C(n,k)==n*C(n-1,k-1))
        if k<n: chk(f'u5 {n},{k}', C(n,k+1)*(k+1)==C(n,k)*(n-k))
        chk(f'u15 {n},{k}', sum(C(m,k) for m in range(k,n+1))==C(n+1,k+1))
    chk(f'u7 {n}', sum(C(n,k) for k in range(n+1))==2**n)
    if n>=1:
        chk(f'u9 {n}', sum((-1)**k*C(n,k) for k in range(n+1))==0)
        chk(f'u11 {n}', sum(k*C(n,k) for k in range(n+1))==n*2**(n-1))
        words=[w for w in product('01',repeat=n) if '00' not in ''.join(w)]
        chk(f'u17 {n}', len(words)==sum(C(n-k+1,k) for k in range(n+2)))
    chk(f'u13 {n}', sum(C(n,k)**2 for k in range(n+1))==C(2*n,n))
    for m in range(n+1):
        for k in range(m+1):
            chk(f'z20 {n},{m},{k}', C(n,m)*C(m,k)==C(n,k)*C(n-k,m-k))
row6=[1];
for k,(a,b) in enumerate([(6,1),(5,2),(4,3),(3,4),(2,5),(1,6)]): row6.append(row6[-1]*a//b)
chk('row6', row6==[C(6,k) for k in range(7)])
chk('z6', [sum(C(n,k) for k in range(n+1)) for n in range(6)]==[1,2,4,8,16,32])
chk('z8', sorted(''.join(w) for w in product('01',repeat=3) if w.count('1')%2==0)==['000','011','101','110'])
chk('z10', sum(''.join(w).count('1') for w in product('01',repeat=3))==12 and 10*2**9==5120)
paths=sorted(''.join(w) for w in product('10',repeat=4) if w.count('1')==2)
chk('z12', paths==sorted(['1100','1010','1001','0110','0101','0011']) and C(10,5)==252)
chk('z12 halves', [C(2,k)*C(2,2-k) for k in range(3)]==[1,4,1])
chk('z14', C(2,2)+C(3,2)+C(4,2)==10==C(5,3))
w4=sorted(''.join(w) for w in product('01',repeat=4) if '00' not in ''.join(w))
chk('z16', w4==sorted(['1111','0111','1011','1101','1110','0101','0110','1010']) and [C(5-k,k) for k in range(3)]==[1,4,3])
a=[None,2,3]
for n in range(3,10): a.append(a[-1]+a[-2])
chk('fib', a[1:7]==[2,3,5,8,13,21])
chk('u13 n5', [C(5,k)**2 for k in range(6)]==[1,25,100,100,25,1])
for p in range(7):
  for q in range(7):
    for r in range(p+q+1):
      chk(f'z21 {p},{q},{r}', sum(C(p,i)*C(q,r-i) for i in range(r+1) if r-i>=0)==C(p+q,r))
exp=sorted(''.join(w) for w in product('ab',repeat=3)); chk('binom3', len(exp)==8 and sum(1 for w in exp if w.count('a')==2)==3)
print(f'проверено {ok} из {ok+len(bad)}; провалов {len(bad)}', bad[:5])
