import itertools, heapq
from math import comb

def qbracket(i): return [1]*(i+1)      # 1+q+...+q^i
def padd(a,b):
    n=max(len(a),len(b)); r=[0]*n
    for k,c in enumerate(a): r[k]+=c
    for k,c in enumerate(b): r[k]+=c
    return r
def pmul(a,b):
    if not a or not b: return []
    r=[0]*(len(a)+len(b)-1)
    for i,c in enumerate(a):
        for j,d in enumerate(b): r[i+j]+=c*d
    return r
def pscale(a,s): return [c*s for c in a]
def ptrim(a):
    a=a[:]
    while len(a)>1 and a[-1]==0: a=a[:-1]
    return a

# P_n(q): displacement enumerator of parking functions of length n
def P_enum(n):
    if n==0: return [1]
    total=n*(n+1)//2; coeffs={}
    for f in itertools.product(range(1,n+1), repeat=n):
        a=sorted(f)
        if all(a[k]<=k+1 for k in range(n)):   # sorted a_i <= i
            D=total-sum(f)
            coeffs[D]=coeffs.get(D,0)+1
    m=max(coeffs); return [coeffs.get(k,0) for k in range(m+1)]

# all labeled trees on {0..m-1} via Prufer
def prufer_trees(m):
    if m==1: yield []; return
    if m==2: yield [(0,1)]; return
    for seq in itertools.product(range(m), repeat=m-2):
        deg=[1]*m
        for x in seq: deg[x]+=1
        leaves=[i for i in range(m) if deg[i]==1]; heapq.heapify(leaves)
        edges=[]; degc=deg[:]
        for x in seq:
            lf=heapq.heappop(leaves); edges.append((lf,x)); degc[x]-=1
            if degc[x]==1: heapq.heappush(leaves,x)
        u=heapq.heappop(leaves); v=heapq.heappop(leaves); edges.append((u,v))
        yield edges

# I_n(q): inversion enumerator of trees on {0..n}, root 0
def I_enum(n):
    if n==0: return [1]
    m=n+1; coeffs={}
    for edges in prufer_trees(m):
        adj=[[] for _ in range(m)]
        for u,v in edges: adj[u].append(v); adj[v].append(u)
        parent=[-1]*m; parent[0]=0; seen=[False]*m; seen[0]=True; st=[0]
        while st:
            x=st.pop()
            for y in adj[x]:
                if not seen[y]: seen[y]=True; parent[y]=x; st.append(y)
        inv=0
        for i in range(1,m):
            x=parent[i]
            while True:
                if 1<=x<=n and x>i: inv+=1
                if x==0: break
                x=parent[x]
        coeffs[inv]=coeffs.get(inv,0)+1
    mx=max(coeffs); return [coeffs.get(k,0) for k in range(mx+1)]

# recurrence X_{n+1}=sum_{i=0}^{n} C(n,i)(1+..+q^i) X_i X_{n-i}, X_0=X_1=1
def X_rec(N):
    X=[[1],[1]]
    for M in range(2,N+1):
        n=M-1; res=[]
        for i in range(0,n+1):
            res=padd(res, pscale(pmul(pmul(qbracket(i),X[i]),X[n-i]), comb(n,i)))
        X.append(ptrim(res))
    return X

N=6; X=X_rec(N)
print("n |  P_n(q) [disp parking]        |  I_n(q) [inv trees]           |  X_n [recurrence]             | P==I==X | (n+1)^(n-1)")
for n in range(1,N+1):
    P=ptrim(P_enum(n)); I=ptrim(I_enum(n)); Xn=ptrim(X[n])
    print(f"{n} | {str(P):30s}| {str(I):30s}| {str(Xn):30s}| {P==I==Xn}    | {(n+1)**(n-1)}  sum={sum(P)}")
