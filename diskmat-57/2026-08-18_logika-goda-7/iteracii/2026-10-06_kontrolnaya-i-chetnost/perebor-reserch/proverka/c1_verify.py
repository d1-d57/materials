import itertools, random
def isprime(n): return n>1 and all(n%d for d in range(2,int(n**.5)+1))
# 1. sum 7
s7=[n for n in range(10,100) if sum(map(int,str(n)))==7]; print("sum7",s7,len(s7))
# HW4
hw=[n for n in range(10,100) if isprime(sum(map(int,str(n))))]; print("hw4",len(hw))
from collections import Counter
print("groups",sorted(Counter(sum(map(int,str(n))) for n in hw).items()))
# 2. flags: cyclic shift from BKS
def shift(w): return w[1:]+w[0]
w="БКС"; seen=[w]
while True:
    w=shift(w)
    if w in seen: print("shift: first repeat at throw",len(seen)+1,"->",w,"; got",seen); break
    seen.append(w)
allf=["".join(p) for p in itertools.permutations("БКС")]; print("flags",len(allf),"missing after shift",sorted(set(allf)-set(seen)))
# odometer-by-top flags: groups
for t in "БКС": print(t,[f for f in sorted(allf) if f[0]==t])
# alternating swaps
w=list("БКС"); seq=["".join(w)]; i=0
while True:
    j=i%2; w[j],w[j+1]=w[j+1],w[j]; s="".join(w)
    if s in seq: break
    seq.append(s); i+=1
print("alt swaps 3 colors:",len(seq),seq)
# 3. pairs of 5
P="АБВГД"
ordered=[a+b for a in P for b in P if a!=b]; print("ordered pairs",len(ordered))
nf=[a+b for i,a in enumerate(P) for b in P[i+1:]]; print("nf pairs",len(nf),nf)
# naive odometer without NF: first repeat
seen=set(); 
for x in ordered:
    k=frozenset(x)
    if k in seen: print("naive odometer first repeat:",x,"at position",ordered.index(x)+1); break
    seen.add(k)
# 'по алфавиту' sorted ordered pairs as words
print("alphabetical ordered words:",sorted(ordered)[:6],"... total",len(ordered))
# 4. sticks largest 6
tr=[(6,m,s) for m in range(5,0,-1) for s in range(m-1,0,-1) if m+s>6]; print("sticks6",tr,len(tr))
deg=[(6,m,s) for m in range(5,0,-1) for s in range(m-1,0,-1) if m+s==6]; print("degenerate",deg)
print("all triples with 6:",len([(m,s) for m in range(1,6) for s in range(1,m)]))
# by smallest as alternative cut
by_small={}
for (_,m,s) in tr: by_small.setdefault(s,[]).append((6,m,s))
print("cut by smallest",by_small)
# grid middle x small
for m in range(5,1,-1):
    print("mid",m," ".join(("#" if m+s>6 else "x") for s in range(m-1,0,-1)), "(small", list(range(m-1,0,-1)),")")
# 5. Vasya list: 33 numbers, 70 missing, 25 duplicated
random.seed(6)
v=[n for n in hw if n!=70]+[25]; random.shuffle(v)
print("vasya",len(v),v)
c=Counter(v); print("dups",[k for k in c if c[k]>1],"missing",sorted(set(hw)-set(v)),"extra",sorted(set(v)-set(hw)))
print("vasya sum7 subseq",[n for n in v if sum(map(int,str(n)))==7])
