"""
Verify exceedance bijection for Catalan numbers.

Setting: monotonic lattice paths from (0,0) to (n,n) on n×n grid.
Steps: R = (1,0) right, U = (0,1) up.
A path is a sequence of n R's and n U's.

Exceedance = number of U-steps (vertical edges) that lie strictly above the diagonal y = x.
A U-step at position going from (x,y) to (x,y+1) is "above diagonal" if y >= x (i.e., the step is at or above the diagonal, ending above it: y+1 > x).

Actually, let me be precise. The diagonal goes from (0,0) to (n,n).
A vertical edge from (x,y) to (x,y+1) is above the diagonal if its midpoint is above y=x,
i.e., y + 0.5 > x, i.e., y >= x.

Exceedance = number of U-steps where, at the moment of taking the step, we are at (x,y) with y >= x.

Wait, let me re-read Wikipedia: "the exceedance of the path is defined to be the number of vertical edges above the diagonal."

A vertical edge goes from (x,y) to (x,y+1). It is "above the diagonal" if the edge is entirely above or on the line y=x. Since the edge goes from y to y+1 at fixed x, the edge is above diagonal if y >= x (the bottom of the edge is on or above the diagonal).

Exceedance ranges from 0 (path entirely below/on diagonal = Dyck path) to n (path entirely above diagonal).

Algorithm to decrease exceedance by 1:
1. Starting from (0,0), follow the path until it first goes above the diagonal.
   This means: find the first U-step where y >= x (making y+1 > x).
2. Continue following until the path returns to the diagonal.
   "Returns to diagonal" = reaches a point (k,k) for some k.
3. Let X be the first edge at this return point. X must be a horizontal (R) step starting on the diagonal.
4. Swap: the portion before X becomes the portion after, and vice versa.

Let me implement this carefully.
"""
from itertools import combinations

def path_from_R_positions(r_positions, n):
    """Create path string from positions of R-steps (0-indexed) among 2n steps."""
    path = []
    for i in range(2*n):
        path.append('R' if i in r_positions else 'U')
    return ''.join(path)

def compute_exceedance(path):
    """Compute exceedance: number of U-steps where y >= x at start of step."""
    x, y = 0, 0
    exc = 0
    for step in path:
        if step == 'U':
            if y >= x:  # this U-step is above or on diagonal
                exc += 1
            y += 1
        else:
            x += 1
    return exc

def decrease_exceedance(path, n):
    """Apply the exceedance-decreasing bijection.
    
    Algorithm (from Wikipedia):
    1. Follow path from (0,0) until it first travels above the diagonal.
       "Above diagonal" = first U-step where y >= x.
    2. Continue until path touches the diagonal again.
       "Touches diagonal" = reaches point (k,k).
    3. Denote by X the first edge at this return point.
       This edge X starts at (k,k) and is the first step after the return.
    4. Swap: portion before X with portion after X.
    
    Returns: new path with exceedance decreased by 1, or None if exceedance is 0.
    """
    x, y = 0, 0
    
    # Step 1: Find first U-step above diagonal (y >= x)
    first_above = None
    for i, step in enumerate(path):
        if step == 'U' and y >= x:
            first_above = i
            break
        if step == 'R': x += 1
        else: y += 1
    
    if first_above is None:
        return None  # exceedance is 0
    
    # Step 2: Continue from first_above, tracking position, until we return to diagonal
    # Reset position tracking to the point just before first_above
    x, y = 0, 0
    for i in range(first_above):
        if path[i] == 'R': x += 1
        else: y += 1
    
    # Now at position (x, y) just before step first_above
    # Take the step
    if path[first_above] == 'R': x += 1
    else: y += 1
    
    # Continue until we hit diagonal y == x
    split_pos = None
    for i in range(first_above + 1, len(path)):
        if path[i] == 'R': x += 1
        else: y += 1
        if y == x:
            # Found return to diagonal. The edge X is the NEXT edge (at position i+1)
            # Wait: actually, the edge that *arrives* at (x,y) with y==x is edge i.
            # The point (x,x) is reached after step i.
            # "Denote by X the first such edge that is reached" - I think X is the edge at position i.
            # Actually re-reading: "Continue to follow the path until it touches the diagonal again. 
            # Denote by X the first such edge that is reached."
            # So X = edge at position i (the edge that brings us back to diagonal).
            # But actually wait: "Swap the portion of the path occurring before X with the portion occurring after X."
            # If X is at position i, then:
            #   before X = path[0:i]
            #   X itself = path[i]  
            #   after X = path[i+1:]
            # The swap puts after X first, then X, then before X? Or just swap before and after?
            
            # From Wikipedia: "Swap the portion of the path occurring before X with the portion occurring after X."
            # So: new path = path[i+1:] + path[i] + path[0:i]
            # Wait, that's not right either. Let me re-read more carefully.
            
            # Actually, looking at the Wikipedia figure description:
            # "we place the last lattice point of the red portion in the top-right corner, 
            #  and the first lattice point of the green portion in the bottom-left corner, 
            #  and place X accordingly"
            # 
            # The split is AT edge X. Before X = path[0:i], X = path[i], After X = path[i+1:]
            # New path = After X + X + Before X = path[i+1:] ... no wait.
            #
            # Actually I think the swap is simpler:
            # Split at the point where the path returns to diagonal.
            # Before the return point: path[0:i+1] (includes the return edge)
            # After the return point: path[i+1:]
            # Swap: new = path[i+1:] + path[0:i+1]
            # 
            # Hmm, but that would just be a cyclic shift. Let me think again.
            
            # From the Berkeley Math Circle handout: 
            # "Mark this second step red, everything before it blue and everything after it green.
            #  Now move the green part to the beginning."
            # 
            # So: X is at position i. 
            # Blue = path[0:i], Red = path[i], Green = path[i+1:]
            # New path = Green + Red + Blue = path[i+1:] + path[i] + path[0:i]
            # But that's just a cyclic rotation by (i+1) positions!
            # No wait: Green + Red + Blue = path[i+1:] + path[i:i+1] + path[0:i]
            # = path[i+1:] + path[i:i+1] + path[0:i]
            # Hmm, but that's cyclic shift starting at i+1? No:
            # path[i+1:] has length 2n-(i+1)
            # path[i:i+1] has length 1
            # path[0:i] has length i
            # Total = 2n. ✓
            # 
            # Actually maybe it's just: new = path[i:] + path[:i]  (cyclic shift by i)?
            # No: that would be path[i], path[i+1:], path[0:i-1], path[i-1]
            # = Red + Green + (most of Blue)
            # 
            # I think it's: new = path[i+1:] + path[0:i+1]
            # = Green + Blue + Red
            # = path after the return point + path up to and including return point
            # But that's cyclic shift by (i+1).
            
            # Let me try the "swap before and after X" literally:
            # path = [before X] [X] [after X]
            # new = [after X] [X] [before X]
            
            split_pos = i
            break
    
    if split_pos is None:
        # Path never returns to diagonal after going above
        # This shouldn't happen for exceedance > 0
        return None
    
    # Swap: before X | X | after X → after X | X | before X
    before = path[:split_pos]
    edge_X = path[split_pos]
    after = path[split_pos+1:]
    
    new_path = after + edge_X + before
    return new_path

def increase_exceedance(path, n):
    """Inverse: increase exceedance by 1.
    
    The inverse operation: find the LAST R-step that starts on the diagonal,
    and swap portions.
    
    More precisely: find the last horizontal edge (R-step) that starts on 
    the diagonal y=x. Split there and swap.
    """
    x, y = 0, 0
    last_R_on_diag = None
    
    for i, step in enumerate(path):
        if step == 'R' and y == x:
            last_R_on_diag = i
        if step == 'R': x += 1
        else: y += 1
    
    if last_R_on_diag is None:
        return None  # exceedance is n (maximum)
    
    i = last_R_on_diag
    # Same swap: before | X | after → after | X | before
    before = path[:i]
    edge_X = path[i]
    after = path[i+1:]
    
    new_path = after + edge_X + before
    return new_path

# ======= Full verification for n=3 =======
n = 3
print(f"Exceedance bijection verification for n={n}")
print(f"Total paths C(6,3) = 20, classes = n+1 = 4, each of size C_3 = 5")
print()

# Generate all paths
all_paths = []
for r_pos in combinations(range(2*n), n):
    all_paths.append(path_from_R_positions(set(r_pos), n))

# Compute exceedance for each
exc_classes = {k: [] for k in range(n+1)}
for p in all_paths:
    e = compute_exceedance(p)
    exc_classes[e].append(p)

print("Exceedance classes:")
for k in range(n+1):
    print(f"  exc={k}: {len(exc_classes[k])} paths: {exc_classes[k]}")

print()

# Apply decrease_exceedance from exc=k to exc=k-1
print("=== Decrease exceedance (exc k -> exc k-1) ===")
all_ok = True
for k in range(1, n+1):
    print(f"\n  exc={k} -> exc={k-1}:")
    images = []
    for p in exc_classes[k]:
        new_p = decrease_exceedance(p, n)
        new_exc = compute_exceedance(new_p)
        ok = (new_exc == k - 1)
        images.append(new_p)
        print(f"    {p} (exc={k}) -> {new_p} (exc={new_exc}) {'✓' if ok else '✗'}")
        if not ok: all_ok = False
    
    # Check images = exc_classes[k-1]
    if sorted(images) == sorted(exc_classes[k-1]):
        print(f"  Images = exc class {k-1}: ✓ (bijective)")
    else:
        print(f"  Images ≠ exc class {k-1}: ✗")
        all_ok = False

print(f"\nAll decrease checks: {'PASSED ✓' if all_ok else 'FAILED ✗'}")

# Apply increase_exceedance (inverse)
print("\n=== Increase exceedance (inverse, exc k -> exc k+1) ===")
inv_ok = True
for k in range(n):
    for p in exc_classes[k]:
        new_p = increase_exceedance(p, n)
        new_exc = compute_exceedance(new_p)
        if new_exc != k + 1:
            print(f"  FAIL: {p} (exc={k}) -> {new_p} (exc={new_exc}), expected {k+1}")
            inv_ok = False

print(f"All increase checks: {'PASSED ✓' if inv_ok else 'FAILED ✗'}")

# Round-trip
print("\n=== Round-trip ===")
rt_ok = True
for k in range(1, n+1):
    for p in exc_classes[k]:
        decreased = decrease_exceedance(p, n)
        recovered = increase_exceedance(decreased, n)
        if recovered != p:
            print(f"  FAIL: {p} -> {decreased} -> {recovered}")
            rt_ok = False

for k in range(n):
    for p in exc_classes[k]:
        increased = increase_exceedance(p, n)
        recovered = decrease_exceedance(increased, n)
        if recovered != p:
            print(f"  FAIL inv: {p} -> {increased} -> {recovered}")
            rt_ok = False

print(f"Round-trip: {'ALL PASSED ✓' if rt_ok else 'FAILED ✗'}")

# Print full table as in Wikipedia
print("\n=== Full table for n=3 (Wikipedia style) ===")
print(f"{'exc=3':<10} {'exc=2':<10} {'exc=1':<10} {'exc=0 (Dyck)':<10}")
for i in range(5):
    row = []
    for k in [3, 2, 1, 0]:
        row.append(exc_classes[k][i])
    print(f"  {row[0]:<10} {row[1]:<10} {row[2]:<10} {row[3]}")

# Verify the chain: applying decrease from exc=3 gives exc=2, etc.
print("\n=== Chain verification: exc=3 -> exc=2 -> exc=1 -> exc=0 ===")
for p3 in exc_classes[3]:
    p2 = decrease_exceedance(p3, n)
    p1 = decrease_exceedance(p2, n)
    p0 = decrease_exceedance(p1, n)
    print(f"  {p3} -> {p2} -> {p1} -> {p0}")

