from itertools import combinations as C
from math import comb
K=0
def ok(name,val,exp):
    global K; K+=1; print(('OK ' if val==exp else 'FAIL'),name,val,exp)
ok('C(6,2)',comb(6,2),15); ok('C(6,3)',comb(6,3),20)
ok('6+6+3',6+6+3,15); ok('10+6+3+1',10+6+3+1,20); ok('5+4+3+2+1',5+4+3+2+1,15)
ok('C(7,2)',comb(7,2),21); ok('7+7+7',7+7+7,21); ok('C(5,2)',comb(5,2),10); ok('5+5',5+5,10)
ok('6*5',6*5,30); ok('30/2',30//2,15); ok('6*5*4',6*5*4,120); ok('120/6',120//6,20)
ok('C(5,2)=tri at vertex in K6',comb(5,2),10); ok('6*10/3',6*10//3,20)
ok('C(5,3)',comb(5,3),10); ok('C(7,3)',comb(7,3),35); ok('C(4,2) block B',comb(4,2),6)
# blocks by first letter for triples of 6
L='ABCDEF'; tr=list(C(L,3)); bl=[sum(1 for t in tr if t[0]==x) for x in L]; print(bl); ok('blocks',bl[:4],[10,6,3,1])
def tri(S,cmax=None):
    return [t for t in C(sorted(S),3) if t[0]+t[1]>t[2] and (cmax is None or t[2]==cmax)]
ok('sticks1-6 longest6',len(tri(range(1,7),6)),4); print(tri(range(1,7),6))
ok('sticks1-6 total',len(tri(range(1,7))),7); print(tri(range(1,7)))
B=[1,2,4,5,6,7,8]
ok('varB longest8',len(tri(B,8)),7); print(tri(B,8))
print('varB total', len(tri(B)), tri(B))
A=list(range(1,8))
ok('varA longest7',len(tri(A,7)),6); print(tri(A,7))
print('varA total',len(tri(A)))
ok('pairs of 6 sticks for B',comb(6,2),15)
# distinct sums of 8 partitions
def parts(n,m=None):
    if m is None:m=n
    if n==0: return [[]]
    return [[k]+p for k in range(min(n,m),0,-1) for p in parts(n-k,k)]
ok('partitions of 8',len(parts(8)),22)
ok('partitions of 8 into exactly 3 parts',len([p for p in parts(8) if len(p)==3]),5)
print('K',K)
