"""Final verification of inflation/deflation bijection."""
from itertools import combinations

def triangulations(m):
    sides = {(min(i,(i+1)%m), max(i,(i+1)%m)) for i in range(m)}
    if m == 3: return [sides]
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

def find_third_vertex(edges, a, b):
    adj = {}
    for u,v in edges: adj.setdefault(u,set()).add(v); adj.setdefault(v,set()).add(u)
    return list(adj.get(a,set()) & adj.get(b,set()))

def deflate(T_edges, m, side):
    """Deflation: (triang of m-gon, non-base side {i,i+1}) -> (triang of (m-1)-gon, oriented edge (merged->r'))"""
    i, j = side  # j = i+1
    thirds = find_third_vertex(T_edges, i, j)
    assert len(thirds) == 1
    r = thirds[0]
    
    # Merge j into i, remove side
    new_edges = set()
    for e in T_edges:
        u, v = e
        if (min(u,v), max(u,v)) == (min(i,j), max(i,j)): continue  # skip marked side
        nu = i if u == j else u
        nv = i if v == j else v
        if nu != nv:
            # Renumber: vertices > j shift down by 1
            rnu = nu if nu < j else nu - 1
            rnv = nv if nv < j else nv - 1
            new_edges.add((min(rnu,rnv), max(rnu,rnv)))
    
    r_new = r if r < j else r - 1
    merged = i  # i < j, so i doesn't shift
    return new_edges, (merged, r_new)  # oriented edge: merged -> r_new

# === Verify n=1 ===
print("=== n=1: (4*1+2)*C1=6 <-> (1+2)*C2=6 ===")
T3 = triangulations(3); T4 = triangulations(4)
non_base_4 = [(0,1),(1,2),(2,3)]

left_images = []
for T in T4:
    for s in non_base_4:
        new_edges, oe = deflate(T, 4, s)
        diags = sorted([e for e in T if abs(e[0]-e[1])>1 and not(min(e)==0 and max(e)==3)])
        left_images.append(oe)
        print(f"  T4(diags={diags}), side={s} -> oriented edge {oe}")

assert len(set(left_images)) == 6, f"Not bijective! Got {len(set(left_images))} distinct"
print("  All 6 distinct -> BIJECTION ✓\n")

# === Verify n=2 ===
print("=== n=2: (4*2+2)*C2=20 <-> (2+2)*C3=20 ===")
T4_src = triangulations(4)  # C2 = 2
T5 = triangulations(5)  # C3 = 5
print(f"  C2={len(T4_src)}, C3={len(T5)}")
non_base_5 = [(0,1),(1,2),(2,3),(3,4)]  # base of 5-gon = (0,4)

left_images = []
for T in T5:
    for s in non_base_5:
        new_edges, oe = deflate(T, 5, s)
        left_images.append(oe)

print(f"  Total right elements: {len(left_images)}")
print(f"  Distinct oriented edges: {len(set(left_images))}")

# Left set size should be 10*C2 = 10*2 = 20
# Wait: left set = oriented edges on triangulations of 4-gon
# Each 4-gon triangulation has 5 edges (4 sides + 1 diagonal), so 10 oriented edges per triangulation
# Total = 2 * 10 = 20
left_set_expected = set()
for T in T4_src:
    for e in T:
        u, v = e
        left_set_expected.add((u, v))
        left_set_expected.add((v, u))
print(f"  Expected left set size: {len(left_set_expected)}")

# Check that all images are valid oriented edges on some triangulation of 4-gon
for T in T5:
    for s in non_base_5:
        new_edges, oe = deflate(T, 5, s)
        # Verify new_edges is a valid triangulation of 4-gon
        is_valid = new_edges in T4_src
        e_tuple = (min(oe[0],oe[1]), max(oe[0],oe[1]))
        edge_in_triang = any(e_tuple in T for T in T4_src if new_edges == T) or e_tuple in new_edges
        if not edge_in_triang:
            diags5 = sorted([e for e in T if abs(e[0]-e[1])>1 and not(min(e)==0 and max(e)==4)])
            print(f"  WARNING: edge {e_tuple} not in resulting triangulation. T5 diags={diags5}, side={s}")

# Check bijectivity: each (triangulation, oriented edge) pair should appear exactly once
full_left_images = []
for T in T5:
    for s in non_base_5:
        new_edges, oe = deflate(T, 5, s)
        # The result is (new_edges as triangulation, oe as oriented edge)
        full_left_images.append((frozenset(new_edges), oe))

if len(set(full_left_images)) == 20:
    print("  All 20 distinct (triang, oriented edge) pairs -> BIJECTION ✓")
else:
    print(f"  Only {len(set(full_left_images))} distinct. Checking...")
    from collections import Counter
    c = Counter(full_left_images)
    for item, count in c.items():
        if count > 1:
            print(f"  DUPLICATE: {item} appears {count} times")

# Verify round-trip for a few cases
print("\n=== Round-trip check (deflate then inflate) ===")

def inflate(T_edges, m, oriented_edge):
    """Inflation: (triang of m-gon, oriented edge (a->b)) -> (triang of (m+1)-gon, marked side)"""
    a, b = oriented_edge
    assert (min(a,b), max(a,b)) in T_edges
    
    pred_a = (a - 1) % m
    new_m = m + 1
    
    def relabel(v):
        return v if v < a else v + 1
    
    v_prime = a
    a_new = a + 1
    
    # Get clockwise-ordered neighbors of a
    adj_a = sorted([v for v in range(m) if (min(a,v), max(a,v)) in T_edges])
    
    def cw_key(v):
        return (a - v) % m
    
    neighbors_cw = sorted(adj_a, key=cw_key)
    b_idx = neighbors_cw.index(b)
    group_A = set(neighbors_cw[:b_idx])  # transfer to v'
    
    new_edges = set()
    for e in T_edges:
        u, v = e
        if a in {u, v}:
            other = v if u == a else u
            if other == b:
                new_edges.add((min(v_prime, relabel(b)), max(v_prime, relabel(b))))
                new_edges.add((min(a_new, relabel(b)), max(a_new, relabel(b))))
            elif other in group_A:
                new_edges.add((min(v_prime, relabel(other)), max(v_prime, relabel(other))))
            else:
                new_edges.add((min(a_new, relabel(other)), max(a_new, relabel(other))))
        else:
            new_edges.add((min(relabel(u), relabel(v)), max(relabel(u), relabel(v))))
    
    # New polygon side {v_prime, a_new} and {pred_new, v_prime}
    pred_new = relabel(pred_a)
    new_edges.add((min(v_prime, a_new), max(v_prime, a_new)))
    new_edges.add((min(pred_new, v_prime), max(pred_new, v_prime)))
    
    marked = (min(v_prime, a_new), max(v_prime, a_new))
    return new_edges, marked

# Round-trip test for n=2
success = 0
total = 0
for T in T5:
    for s in non_base_5:
        total += 1
        defl_edges, oe = deflate(T, 5, s)
        infl_edges, marked = inflate(defl_edges, 4, oe)
        
        if infl_edges == T and marked == (min(s),max(s)):
            success += 1
        else:
            diags5 = sorted([e for e in T if abs(e[0]-e[1])>1 and not(min(e)==0 and max(e)==4)])
            print(f"  MISMATCH: T5(diags={diags5}), side={s}")
            print(f"    deflate -> edges={sorted(defl_edges)}, oe={oe}")
            print(f"    inflate -> edges match: {infl_edges==T}, marked match: {marked==(min(s),max(s))}")
            if infl_edges != T:
                print(f"      expected: {sorted(T)}")
                print(f"      got:      {sorted(infl_edges)}")

print(f"\n  Round-trip: {success}/{total} passed")

