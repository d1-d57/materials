from collections import Counter
s1="6+7+8 5+6+7 4+5+6 2+4+5 2+5+6 2+6+7 5+7+8 4+5+8 1+6+5 1+5+4 1+4+2 1+7+6 1+8+7 4+6+5 4+7+6 4+8+7 2+5+4 2+6+5 2+7+8 2+4+1 2+6+1 2+7+1 2+8+1".split()
t1=[tuple(map(int,x.split('+'))) for x in s1]
print('s1 visible items',len(t1),'(есть «…» между 2+4+1 и 2+6+1)')
c=Counter(tuple(sorted(t)) for t in t1); print('s1 distinct sets',len(c),'dups:',{k:v for k,v in c.items() if v>1})
for i,t in enumerate(t1): print(i+1,t,'perm-dup' if c[tuple(sorted(t))]>1 else '', 'tri' if sum(sorted(t)[:2])>max(t) else 'NOT-tri', 'max8' if max(t)==8 else '')
s2="871 872 874 875 876 865 864 862 861 851 854 852 842 841 821".split()
t2=[tuple(map(int,x)) for x in s2]; B={1,2,4,5,6,7}
print('s2',len(t2),'pairs with 8 distinct',len({frozenset(t[1:]) for t in t2}),'all pairs of B?',{frozenset(t[1:]) for t in t2}=={frozenset(p) for p in __import__('itertools').combinations(B,2)})
print('s2 triangles',[x for x,t in zip(s2,t2) if t[1]+t[2]>8], 'non',[x for x,t in zip(s2,t2) if t[1]+t[2]<=8])
s3="867 874 872 864 854 875 873 865 863".split()
print('s3',len(s3),'with 3:',[x for x in s3 if '3' in x], 'correct present', sorted({''.join(sorted(x)) for x in s3 if '3' not in x}))
s4="267 357 447 367 467 567 667 167 257 457 557 437".split()
print('s4',len(s4),'repeated stick',[x for x in s4 if len(set(x))<3],'degenerate',[x for x in s4 if len(set(x))==3 and sum(sorted(map(int,x))[:2])<=max(map(int,x))])
