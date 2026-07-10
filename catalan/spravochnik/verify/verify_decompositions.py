"""Verify recurrence decompositions for all Catalan models."""

# =============================================
# Model 1: Dyck paths (= balanced parentheses)
# =============================================
def dyck_decompose(word):
    """First-return decomposition: w = ( w1 ) w2
    where w1 and w2 are Dyck words (possibly empty).
    w[0] = '(' always. Find matching ')' at position 2k+1.
    w1 = w[1:2k+1], w2 = w[2k+2:]."""
    if len(word) == 0:
        return None  # empty word, n=0
    assert word[0] == '('
    depth = 0
    for i, c in enumerate(word):
        depth += 1 if c == '(' else -1
        if depth == 0:
            w1 = word[1:i]
            w2 = word[i+1:]
            return w1, w2
    assert False, "Unbalanced"

def dyck_compose(w1, w2):
    """Inverse: (w1, w2) -> ( w1 ) w2"""
    return '(' + w1 + ')' + w2

# Test
print("=== Model 1: Dyck paths (balanced parentheses) ===")
# All Dyck words of length 6 (n=3)
dyck_3 = ['((()))', '(()())', '(())()', '()(())', '()()()']
for w in dyck_3:
    w1, w2 = dyck_decompose(w)
    recovered = dyck_compose(w1, w2)
    k = len(w1) // 2
    m = len(w2) // 2
    print(f"  {w} -> w1={w1 or 'ε'} (k={k}), w2={w2 or 'ε'} (m={m}), recovered={recovered}, {'✓' if recovered == w else '✗'}")

# =============================================
# Model 2: Full binary trees with n+1 leaves
# =============================================
# Representation: tree as tuple. Leaf = None. Internal node = (left, right).
def fbt_decompose(tree):
    """Root decomposition: tree = (left, right).
    left has k+1 leaves (size k), right has m+1 leaves (size m), k+m = n-1."""
    if tree is None:
        return None  # single leaf, n=0
    left, right = tree
    return left, right

def fbt_compose(left, right):
    return (left, right)

def fbt_size(tree):
    """Number of internal nodes."""
    if tree is None: return 0
    return 1 + fbt_size(tree[0]) + fbt_size(tree[1])

def fbt_leaves(tree):
    if tree is None: return 1
    return fbt_leaves(tree[0]) + fbt_leaves(tree[1])

def gen_fbt(n):
    """Generate all full binary trees with n internal nodes (n+1 leaves)."""
    if n == 0:
        return [None]
    result = []
    for k in range(n):
        for left in gen_fbt(k):
            for right in gen_fbt(n - 1 - k):
                result.append((left, right))
    return result

def fbt_to_str(tree):
    if tree is None: return '•'
    return f"({fbt_to_str(tree[0])},{fbt_to_str(tree[1])})"

print("\n=== Model 2: Full binary trees ===")
trees_3 = gen_fbt(3)
print(f"  C_3 = {len(trees_3)} trees")
for t in trees_3:
    left, right = fbt_decompose(t)
    k, m = fbt_size(left), fbt_size(right)
    recovered = fbt_compose(left, right)
    print(f"  {fbt_to_str(t)} -> left={fbt_to_str(left)} (k={k}), right={fbt_to_str(right)} (m={m}), {'✓' if recovered == t else '✗'}")

# =============================================
# Model 3: Triangulations of (n+2)-gon
# =============================================
# Base = edge {0, n+1}. Base triangle = triangle containing base.
# Third vertex of base triangle is some vertex v, 1 <= v <= n.
# Left: triangulation of polygon {0, 1, ..., v} (v+1 sides) = (v-1)-gon... 
# Actually: base triangle = {0, v, n+1}. 
# Left sub-polygon: vertices {0, 1, ..., v} with base {0, v} -> (v+1)-gon = C_{v-1}
# Right sub-polygon: vertices {v, v+1, ..., n+1} with base {v, n+1} -> (n+2-v)-gon = C_{n-v}
# k = v-1, m = n-v, k + m = n - 1. ✓

from itertools import combinations

def triangulations(m):
    """All triangulations of convex m-gon, vertices 0..m-1."""
    sides = {(min(i,(i+1)%m), max(i,(i+1)%m)) for i in range(m)}
    if m <= 3: return [sides]
    possible = [(i,j) for i in range(m) for j in range(i+2,m) if not(i==0 and j==m-1)]
    results = []
    for diags in combinations(possible, m-3):
        ok = True
        for x in range(len(diags)):
            for y in range(x+1, len(diags)):
                a,b = diags[x]; c,d = diags[y]
                if (a<c<b<d) or (c<a<d<b): ok = False
        if ok:
            edges = sides | set(diags)
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

def triang_decompose(edges, m):
    """Base-triangle decomposition of triangulation of m-gon.
    Base = {0, m-1}. Find third vertex v of base triangle.
    Returns (v, left_edges, right_edges) where:
    - left_edges: triangulation of (v+1)-gon {0,...,v}
    - right_edges: triangulation of (m-v)-gon {v,...,m-1}
    """
    # Find triangle containing base {0, m-1}
    adj = {i:set() for i in range(m)}
    for u,w in edges: adj[u].add(w); adj[w].add(u)
    base_thirds = adj[0] & adj[m-1] - {0, m-1}
    # There should be exactly one (for the base edge in a triangulation)
    # Actually the base is a polygon side, so it belongs to exactly 1 triangle
    assert len(base_thirds) == 1, f"Expected 1 base triangle, got {base_thirds}"
    v = base_thirds.pop()
    
    # Left sub-triangulation: vertices 0..v
    left_edges = set()
    for u, w in edges:
        if u <= v and w <= v:
            left_edges.add((u, w))
    
    # Right sub-triangulation: vertices v..m-1, renumber to 0..m-1-v
    right_edges = set()
    for u, w in edges:
        if u >= v and w >= v:
            right_edges.add((u - v, w - v))
    
    return v, left_edges, right_edges

print("\n=== Model 3: Triangulations of (n+2)-gon ===")
n = 3
m = n + 2  # pentagon
tri_list = triangulations(m)
print(f"  C_{n} = {len(tri_list)} triangulations of {m}-gon")
for T in tri_list:
    diags = sorted([e for e in T if abs(e[0]-e[1]) > 1 and not(min(e)==0 and max(e)==m-1)])
    v, left, right = triang_decompose(T, m)
    k = v - 1  # left has (v+1)-gon, Catalan index = v-1
    mm = n - v  # right has (m-v)-gon = (n+2-v)-gon, Catalan index = n-v
    print(f"  diags={diags}: base triangle apex v={v}, left C_{k} ({v+1}-gon), right C_{mm} ({m-v}-gon)")

# =============================================
# Model 4: Plane trees with n+1 vertices
# =============================================
# Representation: tree as list of children subtrees. 
# Root + children [T1, T2, ..., Tk] where each Ti is a plane tree.
# Single vertex = [].
# Size = number of edges = sum of sizes of children + number of children... no.
# n edges = n+1 vertices. 

def gen_plane_trees(n_edges):
    """Generate all plane trees with n_edges edges (n_edges+1 vertices).
    A plane tree with 0 edges = single vertex = [].
    Decomposition: first child subtree has k edges, remaining forest has n-1-k edges.
    """
    if n_edges == 0:
        return [[]]  # single vertex
    result = []
    # A non-empty plane tree: root has >= 1 child.
    # First-child/next-sibling decomposition:
    # The leftmost subtree of root has k edges (k >= 0).
    # The "rest" is a plane tree where root has the remaining children.
    # This is equivalent to: first child has k edges, rest of children form tree with n-1-k edges.
    # But actually the standard Catalan decomposition for plane trees:
    # Remove the root. The root has children T1, T2, ..., Td.
    # Encode as: T1 is a plane tree with k edges. 
    # The root with children T2, ..., Td is a plane tree with n-k-1 edges? No...
    
    # Standard bijection: plane tree with n+1 vertices <-> Dyck word of length 2n.
    # DFS traversal: go down = (, go up = ).
    # Decomposition aligned with Dyck: first return = first child subtree.
    
    # Let me use: root's first child has subtree with k edges (k >= 0).
    # "Remaining tree" = root with all other children (T2, ..., Td). This has n-1-k edges.
    # This matches Dyck decomposition: w = (w1)w2.
    for k in range(n_edges):
        for first_child in gen_plane_trees(k):
            for remaining in gen_plane_trees(n_edges - 1 - k):
                # New tree: root's children = [first_child] + remaining's root's children
                new_tree = [first_child] + remaining
                result.append(new_tree)
    return result

def pt_to_str(tree):
    if len(tree) == 0: return '•'
    return 'r[' + ','.join(pt_to_str(c) for c in tree) + ']'

def pt_edges(tree):
    if len(tree) == 0: return 0
    return len(tree) + sum(pt_edges(c) for c in tree)

print("\n=== Model 4: Plane trees with n+1 vertices ===")
n = 3
ptrees = gen_plane_trees(n)
print(f"  C_{n} = {len(ptrees)} plane trees with {n} edges ({n+1} vertices)")
for t in ptrees:
    if len(t) == 0:
        print(f"  {pt_to_str(t)}: single vertex (n=0 case, shouldn't appear for n=3)")
    else:
        first_child = t[0]
        remaining_children = t[1:]  # this is the "remaining tree" (root + rest)
        k = pt_edges([first_child])  # edges in first subtree... 
        # Actually k = edges of first_child subtree = pt_edges(first_child) + 1? No.
        # first_child is a plane tree rooted at the first child. Edge count = pt_edges(first_child).
        # But we also count the edge from root to first_child: +1.
        # Total edges in "first child branch" = 1 + pt_edges(first_child)... hmm.
        # Actually in the Catalan decomposition:
        # w = (w1)w2 -> first child subtree gives w1 (k steps), rest gives w2 (m steps)
        # k + m = n - 1. First child subtree has k+1 vertices = k edges in the subtree + 1 edge to root.
        # So first child contributes k+1 edges total? No, k edges in the subtree.
        # n = (1 + k) + m where 1 is the edge root->first_child, k = edges inside first_child tree, m = edges in rest.
        # Hmm this is getting confusing. Let me just count.
        k_first = pt_edges(first_child)  # edges in first child's subtree (not counting edge to root)
        # remaining_children: these are children of root (not counting first child)
        # The "remaining tree" root[remaining_children] has pt_edges(root[remaining_children]) edges
        remaining_tree = remaining_children
        m_rest = pt_edges(remaining_tree)  # edges from root to remaining children + their subtrees
        # k_first + 1 (edge to first child) + m_rest = n
        print(f"  {pt_to_str(t)}: first_child={pt_to_str(first_child)} (k={k_first}), rest has {m_rest} edges, total={k_first + 1 + m_rest}")

