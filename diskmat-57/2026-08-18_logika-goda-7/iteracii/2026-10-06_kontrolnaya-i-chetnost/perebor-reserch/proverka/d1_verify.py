import itertools
from collections import Counter
def isprime(n): return n>1 and all(n%d for d in range(2,int(n**.5)+1))
ds=lambda n: sum(map(int,str(n)))
hw=[n for n in range(10,100) if isprime(ds(n))]
# R1. Vasya list exactly as printed in C1_ladder.md
md="""25 76 38 43 25 58 14 50 89 49 83
65 56 30 94 16 41 23 67 92 85 32
34 47 52 61 20 11 12 29 74 98 21"""
v=list(map(int,md.split()))
c=Counter(v)
print("R1 md-vasya len",len(v),"dups",[k for k in c if c[k]>1],"missing",sorted(set(hw)-set(v)),"extra",sorted(set(v)-set(hw)))
sv=sorted(v); i=sv.index(67); print("R1 sorted around 70:",sv[i-1:i+3])
# R2. rows by first digit: correct vs Vasya
print("R2 correct rows by first digit:")
tot=0
for d in range(1,10):
    row=[n for n in hw if n//10==d]; vr=sorted(n for n in v if n//10==d); tot+=len(row)
    flag="" if row==vr else "  <-- Vasya: "+str(vr)
    print("   ",d,":",row,len(row),flag)
print("R2 total",tot)
# R3. sum 7 by increasing order: how many numbers must be checked to get 'next'
s7=[n for n in range(10,100) if ds(n)==7]
gaps=[(a,b,b-a) for a,b in zip(s7,s7[1:])]
print("R3 sum7",s7,"checks between consecutive:",[g[2] for g in gaps],"; after 70 to 99 checks",99-70,"-> none")
# R3b backup: sum 9 (contains 90)
s9=[n for n in range(10,100) if ds(n)==9]; print("R3b sum9",s9,len(s9))
# R3c backup: digits differ by 6
d6=[n for n in range(10,100) if abs(n//10-n%10)==6]; print("R3c diff6",d6,len(d6))
plus11=[n for n in range(17,100,11) if abs(n//10-n%10)==6]; print("R3c '+11 from 17' gives",[17,28,39],"then 50 has diff",abs(5-0))
# R4. pairs from 4: naive odometer first repeat
P="АБВГ"; ordered=[a+b for a in P for b in P if a!=b]; seen=set()
for k,x in enumerate(ordered,1):
    if frozenset(x) in seen: print("R4 pairs-of-4 naive first repeat",x,"at position",k); break
    seen.add(frozenset(x))
print("R4 nf pairs of 4",[a+b for i,a in enumerate(P) for b in P[i+1:]])
# R5. flags: shift and alt swaps re-check; order-inside-column ambiguity
allf=["".join(p) for p in itertools.permutations("БКС")]
def valid_top_chain(ch):
    # 'держим верх' rule: tops form contiguous blocks, each block complete, no repeats
    if len(set(ch))!=6: return False
    tops=[f[0] for f in ch]; blocks=[t for i,t in enumerate(tops) if i==0 or tops[i-1]!=t]
    return len(blocks)==3
chains=[ch for ch in itertools.permutations(allf) if valid_top_chain(ch)]
print("R5 chains satisfying 'держим верх, меняем остальное' (any order inside / of columns):",len(chains),
      "; starting with БКС:",sum(1 for ch in chains if ch[0]=="БКС"))
# R6. sticks largest 6: permutation-duplicates possible if no normal form
tr=[(6,m,s) for m in range(5,0,-1) for s in range(m-1,0,-1) if m+s>6]
print("R6 sticks6",tr,len(tr),"; writings with 6 first, any order of other two:",2*len(tr))
# R7. Vasya list with the duplicate 25 moved away from the first row (25 at positions 1 and 5 is visible at a glance)
v2=v[:]; i5=4; j=v2.index(20)   # swap 2nd 25 (pos 5) with 20 (row 3)
v2[i5],v2[j]=v2[j],v2[i5]
rows=[v2[k:k+11] for k in range(0,33,11)]
for r in rows: print("R7 row:"," ".join(map(str,r)))
c2=Counter(v2); pos=[k+1 for k,x in enumerate(v2) if x==25]
print("R7 len",len(v2),"dups",[k for k in c2 if c2[k]>1],"positions of 25",pos,"missing",sorted(set(hw)-set(v2)),"extra",sorted(set(v2)-set(hw)))
print("R7 sum7 subseq",[n for n in v2 if ds(n)==7])
