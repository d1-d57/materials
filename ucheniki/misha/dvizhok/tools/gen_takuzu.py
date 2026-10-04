import itertools,random
def pats(n):
    out=[]
    for p in itertools.product([0,1],repeat=n):
        if sum(p)!=n//2: continue
        if any(p[i]==p[i+1]==p[i+2] for i in range(n-2)): continue
        out.append(p)
    return out
def solve(n,clue,limit=2):
    P=pats(n); sols=[]
    def ok_cols(rows,final=False):
        k=len(rows)
        for c in range(n):
            col=[r[c] for r in rows]
            if col.count(0)>n//2 or col.count(1)>n//2: return False
            if any(col[i]==col[i+1]==col[i+2] for i in range(k-2)): return False
        if final:
            cols=[tuple(r[c] for r in rows) for c in range(n)]
            if len(set(cols))<n: return False
        return True
    def rec(rows):
        if len(sols)>=limit: return
        if len(rows)==n:
            if ok_cols(rows,True): sols.append([r[:] for r in rows])
            return
        i=len(rows)
        for p in P:
            if p in [tuple(r) for r in rows]: continue
            if any(clue[i][j] is not None and clue[i][j]!=p[j] for j in range(n)): continue
            rows.append(list(p))
            if ok_cols(rows): rec(rows)
            rows.pop()
    rec([]); return sols
def gen(n,seed,target):
    random.seed(seed)
    full=solve(n,[[None]*n for _ in range(n)],limit=10**6)
    sol=random.choice(full)
    clue=[r[:] for r in sol]
    cells=[(i,j) for i in range(n) for j in range(n)]; random.shuffle(cells)
    for (i,j) in cells:
        v=clue[i][j]; clue[i][j]=None
        if len(solve(n,clue))!=1: clue[i][j]=v
    cnt=sum(x is not None for r in clue for x in r)
    return sol,clue,cnt
for n,seed in [(4,3),(6,7),(6,11)]:
    s,c,k=gen(n,seed,0)
    print(n,k,'SOL',[''.join(map(str,r)) for r in s])
    print('CLUE',[''.join('.' if x is None else str(x) for x in r) for r in c])

def withclues(n,seed,target):
    s,c,k=gen(n,seed,0)
    random.seed(seed+100)
    empty=[(i,j) for i in range(n) for j in range(n) if c[i][j] is None]; random.shuffle(empty)
    for (i,j) in empty[:max(0,target-k)]: c[i][j]=s[i][j]
    assert len(solve(n,c))==1
    return [''.join('.' if x is None else str(x) for x in r) for r in c]
print('EXTRA')
print(withclues(4,5,7)); print(withclues(6,21,16)); print(withclues(6,33,13))
