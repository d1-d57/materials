"""Verify hub bijections: each model <-> Dyck paths (balanced parentheses)."""

# ==========================================
# Hub: Dyck paths as balanced parentheses
# ==========================================
def dyck_decompose(w):
    if not w: return None
    depth = 0
    for i, c in enumerate(w):
        depth += 1 if c == '(' else -1
        if depth == 0: return w[1:i], w[i+1:]

def dyck_compose(w1, w2):
    return '(' + w1 + ')' + w2

# ==========================================
# Model 2: Full binary trees
# ==========================================
# Leaf = None, Internal = (left, right)

def fbt_to_dyck(tree):
    """Full binary tree -> Dyck word. Recursive: leaf -> '', (L,R) -> '(' + fbt_to_dyck(L) + ')' + fbt_to_dyck(R)."""
    if tree is None: return ''
    return '(' + fbt_to_dyck(tree[0]) + ')' + fbt_to_dyck(tree[1])

def dyck_to_fbt(w):
    """Dyck word -> full binary tree."""
    if not w: return None
    w1, w2 = dyck_decompose(w)
    return (dyck_to_fbt(w1), dyck_to_fbt(w2))

def gen_fbt(n):
    if n == 0: return [None]
    result = []
    for k in range(n):
        for L in gen_fbt(k):
            for R in gen_fbt(n-1-k):
                result.append((L, R))
    return result

def fbt_str(t):
    if t is None: return '•'
    return f"({fbt_str(t[0])},{fbt_str(t[1])})"

# ==========================================
# Model 3: Triangulations
# ==========================================
# Represented as list of diagonals (pairs). Vertices 0..n+1, base = {0, n+1}.

def triang_to_dyck(diags, n):
    """Triangulation of (n+2)-gon -> Dyck word. 
    Recursive via base-triangle decomposition."""
    if n == 0: return ''
    m = n + 2  # number of vertices
    # Find base triangle: vertex v adjacent to both 0 and m-1 via edges
    all_edges = set(diags)
    # Add polygon sides
    for i in range(m): all_edges.add((min(i,(i+1)%m), max(i,(i+1)%m)))
    
    adj = {i:set() for i in range(m)}
    for u,v in all_edges: adj[u].add(v); adj[v].add(u)
    
    thirds = adj[0] & adj[m-1] - {0, m-1}
    v = min(thirds)  # should be unique for base edge in triangulation
    # Actually for a triangulation, base edge belongs to exactly 1 triangle
    # But adj[0] & adj[m-1] might have multiple if there are diags from 0 and from m-1
    # Need to find the actual triangle
    for candidate in sorted(thirds):
        # Check if {0, candidate, m-1} is a triangle (all three edges exist)
        if (min(0,candidate), max(0,candidate)) in all_edges and \
           (min(candidate,m-1), max(candidate,m-1)) in all_edges:
            v = candidate
            break
    
    # Left: vertices 0..v, diags within
    left_diags = [(a,b) for a,b in diags if a <= v and b <= v]
    # Right: vertices v..m-1, renumber to 0..m-1-v
    right_diags = [(a-v, b-v) for a,b in diags if a >= v and b >= v]
    
    k = v - 1  # left is C_{v-1}
    w1 = triang_to_dyck(left_diags, k)
    w2 = triang_to_dyck(right_diags, n - v)
    return dyck_compose(w1, w2)

def dyck_to_triang(w, offset=0):
    """Dyck word -> triangulation of (n+2)-gon.
    Returns list of diagonal pairs (global vertex numbering starting from offset).
    Vertices: offset, offset+1, ..., offset+n+1. Base = {offset, offset+n+1}."""
    n = len(w) // 2
    if n == 0: return []
    w1, w2 = dyck_decompose(w)
    k = len(w1) // 2
    v = k + 1  # apex of base triangle (local), global = offset + v
    
    # Base triangle: {offset, offset+v, offset+n+1}
    # Add diagonals {offset, offset+v} and {offset+v, offset+n+1} if they're not polygon sides
    diags = []
    # {offset, offset+v} is a polygon side only if v == 1
    if v > 1:
        diags.append((offset, offset + v))
    # {offset+v, offset+n+1} is a polygon side only if v == n
    if v < n:
        diags.append((offset + v, offset + n + 1))
    
    # Left sub-triangulation: vertices offset..offset+v
    diags += dyck_to_triang(w1, offset)
    # Right sub-triangulation: vertices offset+v..offset+n+1
    diags += dyck_to_triang(w2, offset + v)
    
    return sorted(diags)

# ==========================================
# Model 4: Plane trees
# ==========================================
# Represented as list of children subtrees. [] = leaf.

def ptree_to_dyck(tree):
    """Plane tree -> Dyck word via DFS traversal.
    For each child: '(' + recurse(child) + ')'."""
    result = ''
    for child in tree:
        result += '(' + ptree_to_dyck(child) + ')'
    return result

def dyck_to_ptree(w):
    """Dyck word -> plane tree."""
    if not w: return []
    # Parse: each '(' ... ')' at depth 0 is one child
    children = []
    depth = 0
    start = -1
    for i, c in enumerate(w):
        if c == '(':
            if depth == 0: start = i
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                # child content is w[start+1:i]
                child = dyck_to_ptree(w[start+1:i])
                children.append(child)
    return children

def ptree_str(t):
    if not t: return '•'
    return 'r[' + ','.join(ptree_str(c) for c in t) + ']'

def gen_ptrees(n):
    """Generate all plane trees with n edges."""
    if n == 0: return [[]]
    result = []
    for k in range(n):
        for fc in gen_ptrees(k):
            for rest in gen_ptrees(n-1-k):
                result.append([fc] + rest)
    return result

# ==========================================
# VERIFICATION
# ==========================================
n = 3
print(f"=== Verification for n = {n} ===\n")

# Generate all objects
dyck_words = []
def gen_dyck(n):
    if n == 0: return ['']
    result = []
    for k in range(n):
        for w1 in gen_dyck(k):
            for w2 in gen_dyck(n-1-k):
                result.append(dyck_compose(w1, w2))
    return result

dycks = gen_dyck(n)
fbts = gen_fbt(n)
ptrees = gen_ptrees(n)

print(f"Dyck words ({len(dycks)}): {dycks}")
print()

# === FBT <-> Dyck ===
print("--- FBT <-> Dyck ---")
fbt_dyck_map = {}
for t in fbts:
    w = fbt_to_dyck(t)
    t_back = dyck_to_fbt(w)
    ok = t_back == t
    fbt_dyck_map[fbt_str(t)] = w
    print(f"  {fbt_str(t):<25} -> {w:<12} -> {fbt_str(t_back):<25} {'✓' if ok else '✗'}")

images = set(fbt_dyck_map.values())
print(f"  Bijective: {len(images)} distinct images out of {len(fbts)} trees: {'✓' if len(images)==len(fbts) else '✗'}")

# === Plane trees <-> Dyck ===
print("\n--- Plane trees <-> Dyck ---")
pt_dyck_map = {}
for t in ptrees:
    w = ptree_to_dyck(t)
    t_back = dyck_to_ptree(w)
    ok = t_back == t
    pt_dyck_map[ptree_str(t)] = w
    print(f"  {ptree_str(t):<25} -> {w:<12} -> {ptree_str(t_back):<25} {'✓' if ok else '✗'}")

images = set(pt_dyck_map.values())
print(f"  Bijective: {len(images)} distinct images out of {len(ptrees)} trees: {'✓' if len(images)==len(ptrees) else '✗'}")

# === Triangulations <-> Dyck ===
print("\n--- Triangulations <-> Dyck ---")
from itertools import combinations
def triangulations(m):
    sides = {(min(i,(i+1)%m), max(i,(i+1)%m)) for i in range(m)}
    if m <= 3: return [sides]
    possible = [(i,j) for i in range(m) for j in range(i+2,m) if not(i==0 and j==m-1)]
    results = []
    for ds in combinations(possible, m-3):
        ok = True
        for x in range(len(ds)):
            for y in range(x+1, len(ds)):
                a,b = ds[x]; c,d = ds[y]
                if (a<c<b<d) or (c<a<d<b): ok = False
        if ok:
            edges = sides | set(ds)
            adj = {v:set() for v in range(m)}
            for u,v in edges: adj[u].add(v); adj[v].add(u)
            tris = set()
            for v in range(m):
                for u in adj[v]:
                    for w in adj[v]:
                        if u<w and w in adj[u]:
                            tris.add((min(v,u,w), sorted([v,u,w])[1], max(v,u,w)))
            if len(tris) == m-2: results.append(edges)
    return results

tri_list = triangulations(n+2)
for T in tri_list:
    diags = sorted([e for e in T if abs(e[0]-e[1])>1 and not(min(e)==0 and max(e)==n+1)])
    w = triang_to_dyck(diags, n)
    diags_back = dyck_to_triang(w)
    ok = sorted(diags_back) == sorted(diags)
    print(f"  diags={diags} -> {w:<12} -> {diags_back} {'✓' if ok else '✗'}")

# === Commutativity check ===
print("\n=== COMMUTATIVITY CHECK ===")
print("For each FBT: decompose -> translate parts -> reassemble = translate whole?")
all_ok = True
for t in fbts:
    # Translate whole
    w_whole = fbt_to_dyck(t)
    
    # Decompose tree
    if t is None: continue
    L, R = t
    # Translate parts
    w_L = fbt_to_dyck(L)
    w_R = fbt_to_dyck(R)
    # Reassemble in hub
    w_composed = dyck_compose(w_L, w_R)
    
    ok = w_whole == w_composed
    if not ok:
        print(f"  FAIL: {fbt_str(t)} -> whole={w_whole}, composed={w_composed}")
        all_ok = False

print(f"FBT commutativity: {'ALL PASSED ✓' if all_ok else 'FAILED ✗'}")

all_ok = True
for t in ptrees:
    w_whole = ptree_to_dyck(t)
    if not t: continue  # empty tree
    # Decompose: first child + rest
    fc = t[0]
    rest = t[1:]
    w_fc = ptree_to_dyck(fc)
    w_rest = ptree_to_dyck(rest)  # rest treated as tree with root having remaining children
    w_composed = dyck_compose(w_fc, w_rest)
    
    ok = w_whole == w_composed
    if not ok:
        print(f"  FAIL: {ptree_str(t)} -> whole={w_whole}, composed={w_composed}")
        all_ok = False

print(f"Plane tree commutativity: {'ALL PASSED ✓' if all_ok else 'FAILED ✗'}")

all_ok = True
for T in tri_list:
    diags = sorted([e for e in T if abs(e[0]-e[1])>1 and not(min(e)==0 and max(e)==n+1)])
    w_whole = triang_to_dyck(diags, n)
    
    # Decompose: find base triangle apex
    all_edges = set(diags)
    m = n + 2
    for i in range(m): all_edges.add((min(i,(i+1)%m), max(i,(i+1)%m)))
    adj = {i:set() for i in range(m)}
    for u,v in all_edges: adj[u].add(v); adj[v].add(u)
    v = min(adj[0] & adj[m-1] - {0, m-1})
    
    left_diags = [(a,b) for a,b in diags if a <= v and b <= v]
    right_diags = [(a-v, b-v) for a,b in diags if a >= v and b >= v]
    
    w_left = triang_to_dyck(left_diags, v-1)
    w_right = triang_to_dyck(right_diags, n-v)
    w_composed = dyck_compose(w_left, w_right)
    
    ok = w_whole == w_composed
    if not ok:
        print(f"  FAIL: diags={diags}, v={v}, whole={w_whole}, composed={w_composed}")
        all_ok = False

print(f"Triangulation commutativity: {'ALL PASSED ✓' if all_ok else 'FAILED ✗'}")

# === Cross-model bijection via hub ===
print("\n=== Full correspondence table (n=3) ===")
print(f"{'Dyck':<12} {'FBT':<25} {'Plane tree':<20} {'Triang diags'}")
for w in sorted(dycks):
    t_fbt = dyck_to_fbt(w)
    t_pt = dyck_to_ptree(w)
    t_tri = dyck_to_triang(w)
    print(f"  {w:<12} {fbt_str(t_fbt):<25} {ptree_str(t_pt):<20} {t_tri}")

