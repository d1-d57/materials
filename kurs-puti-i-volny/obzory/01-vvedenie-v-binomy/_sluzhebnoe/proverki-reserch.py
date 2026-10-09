from math import comb as C
from itertools import combinations, product
# P1 diagonals intersections of convex 15-gon
print("P1 C(15,4)", C(15,4), "C(8,4)",C(8,4))
# P2 rectangles 8x8 brute
cnt=sum(1 for x1 in range(9) for x2 in range(x1+1,9) for y1 in range(9) for y2 in range(y1+1,9))
print("P2", cnt, C(9,2)**2)
# P3
n=100; print("P3", sum(range(1,n+1)), C(n+1,2))
# P4 hockey stick
print("P4", sum(C(k,2) for k in range(2,11)), C(11,3))
# P5 Moser
print("P5", [1+C(n,2)+C(n,4) for n in range(1,11)])
# P6 polygon diagonals regions
print("P6", [C(n,4)+C(n-1,2) for n in range(3,9)], C(17,4)+C(16,2))
# P7 central even
print("P7", [C(2*n,n) for n in range(1,8)])
# P8 even/odd subsets n=5
ev=sum(C(5,k) for k in range(0,6,2)); od=sum(C(5,k) for k in range(1,6,2)); print("P8",ev,od)
# P9 words 5 zeros 3 ones no adjacent ones
w=[s for s in product('01',repeat=8) if s.count('1')==3 and '11' not in ''.join(s)]; print("P9",len(w),C(6,3))
# P10 3 nonadjacent from 1..10
print("P10", sum(1 for a,b,c in combinations(range(1,11),3) if b-a>1 and c-b>1), C(8,3))
# P11
print("P11", [n for n in range(2,40) if C(n,2) in (45,66)])
# P12
print("P12", C(10,2)-5)
# P13
print("P13",[n for n in range(3,50) if n*(n-3)//2==n],[n for n in range(3,50) if n*(n-3)//2==2*n])
# P14 triangles 10 and 11 points on parallel lines
print("P14", 10*C(11,2)+11*C(10,2))
# P15 numbers <10^6 digit sum 2
print("P15", sum(1 for k in range(1,10**6) if sum(map(int,str(k)))==2), C(6,2)+C(6,1), C(7,2))
# P16 committee with chair
print("P16", 4*C(10,4), 10*C(9,3), 7*C(10,4)/... if False else (4*C(10,4), 10*C(9,3), (10-3)*C(10,3), 4*3*C(10,4), 10*9*C(8,2)))
# P17 committee/subcommittee
print("P17", C(10,5)*C(5,2), C(10,2)*C(8,3))
# P18 first row with number >1000
for n in range(30):
    if max(C(n,k) for k in range(n+1))>1000: print("P18 row",n, C(n,n//2), C(n-1,(n-1)//2)); break
# P19 Lilavati windows
print("P19", 2**8-1)
# P20 Caraka
print("P20", [C(6,k) for k in range(7)], 2**6-1)
# P21 Varahamihira, P22 Mersenne
print("P21", C(16,4), C(16,4)*24, "P22", C(36,12))
# P23 pairs a<=b<=n
n=10; print("P23", sum(1 for a in range(1,n+1) for b in range(a,n+1)), C(n+1,2))
# P24 two staircases = square
print("P24", [C(n,2)+C(n+1,2)==n*n for n in range(1,20)].count(False))
# P25 Pascal's problem
print("P25", 3*4*5*6//(1*2*3*4), C(6,2))
# arcs on circle 12 points, segments 10 points
print("arcs", 2*C(12,2), "segments", C(10,2))
# 3x3 grid lines and triangles
pts=[(x,y) for x in range(3) for y in range(3)]
def col(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])==0
tri=sum(1 for a,b,c in combinations(pts,3) if not col(a,b,c))
lines=set()
for a,b in combinations(pts,2):
    lines.add(frozenset(p for p in pts if col(a,b,p)))
print("grid3x3 triangles",tri,"lines",len(lines))
# chess: two squares not in same row/col
print("rooks", 64*49//2, sum(1 for a,b in combinations(range(64),2) if a//8!=b//8 and a%8!=b%8))
# Gayatri 3 long of 6
print("gayatri", [C(6,k) for k in range(7)], sum(C(6,k) for k in range(7)))
# ibn Ezra conjunctions of 7 planets, 2..7
print("ibnEzra", sum(C(7,k) for k in range(2,8)))
# diagonals 100-gon
print("diag100", 100*97//2)
# Llull
print("Llull", C(9,2), C(16,2))
# sum of three from 1..20 even
print("even3", sum(1 for t in combinations(range(1,21),3) if sum(t)%2==0), C(10,3)+10*C(10,2))
