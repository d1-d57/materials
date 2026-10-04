import itertools,random,json
n=4
perms=list(itertools.permutations(range(1,5)))
def solve(giv,boxes,ineq,limit=2):
    sols=[]
    def ok(rows):
        k=len(rows)
        for c in range(n):
            col=[r[c] for r in rows]
            if len(set(col))<k: return False
        if boxes and k%2==0:
            for br in range(0,k,2):
                for bc in (0,2):
                    s={rows[br+i][bc+j] for i in (0,1) for j in (0,1)}
                    if len(s)<4: return False
        for (a,b) in ineq:
            if a[0]<k and b[0]<k and not rows[a[0]][a[1]]<rows[b[0]][b[1]]: return False
        return True
    def rec(rows):
        if len(sols)>=limit: return
        if len(rows)==n: sols.append([list(r) for r in rows]); return
        i=len(rows)
        for p in perms:
            if any(giv[i][j] and giv[i][j]!=p[j] for j in range(n)): continue
            rows.append(p)
            if ok(rows): rec(rows)
            rows.pop()
    rec([]); return sols
def gen_sudoku(seed,keep):
    random.seed(seed); full=solve([[0]*4 for _ in range(4)],True,[],limit=10**6); sol=random.choice(full)
    g=[r[:] for r in sol]; cells=[(i,j) for i in range(4) for j in range(4)]; random.shuffle(cells)
    for (i,j) in cells:
        if sum(x!=0 for r in g for x in r)<=keep: break
        v=g[i][j]; g[i][j]=0
        if len(solve(g,True,[]))!=1: g[i][j]=v
    return [''.join(str(x) if x else '.' for x in r) for r in g]
def gen_futo(seed,ngiv,nineq):
    random.seed(seed); full=solve([[0]*4 for _ in range(4)],False,[],limit=10**6)
    while True:
        sol=random.choice(full)
        pairs=[((i,j),(i,j+1)) for i in range(4) for j in range(3)]+[((i,j),(i+1,j)) for i in range(3) for j in range(4)]
        random.shuffle(pairs); ineq=[]
        for a,b in pairs[:nineq]:
            ineq.append((a,b) if sol[a[0]][a[1]]<sol[b[0]][b[1]] else (b,a))
        g=[[0]*4 for _ in range(4)]; cells=[(i,j) for i in range(4) for j in range(4)]; random.shuffle(cells)
        for (i,j) in cells[:ngiv]: g[i][j]=sol[i][j]
        if len(solve(g,False,ineq))==1:
            return [''.join(str(x) if x else '.' for x in r) for r in g], [[list(a),list(b)] for a,b in ineq]
print(json.dumps({'s1':gen_sudoku(1,9),'s2':gen_sudoku(2,8),'s3':gen_sudoku(3,7),'f1':gen_futo(4,4,5),'f2':gen_futo(5,3,6)}))
