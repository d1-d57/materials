from itertools import combinations

def path_to_string(positions_of_R, length):
    """Convert set of R-positions (0-indexed) to string like RRURUU."""
    return ''.join('R' if i in positions_of_R else 'U' for i in range(length))

def is_good(path):
    """Check if path never goes above diagonal (prefix U count never exceeds R count)."""
    r, u = 0, 0
    for step in path:
        if step == 'R': r += 1
        else: u += 1
        if u > r:
            return False
    return True

def reflect_bad_path(path, n):
    """Apply reflection bijection to a bad path from (0,0) to (n,n).
    Returns path from (0,0) to (n-1, n+1)."""
    r, u = 0, 0
    first_bad = None
    for i, step in enumerate(path):
        if step == 'R': r += 1
        else: u += 1
        if u > r:  # first time path goes above diagonal, touching y = x + 1
            first_bad = i
            break
    
    if first_bad is None:
        return None  # not a bad path
    
    # Keep prefix up to and including position first_bad
    prefix = path[:first_bad + 1]
    suffix = path[first_bad + 1:]
    
    # Reflect suffix: swap R <-> U
    reflected_suffix = ''.join('U' if c == 'R' else 'R' for c in suffix)
    
    return prefix + reflected_suffix

def reflect_inverse(path, n):
    """Apply inverse: path from (0,0) to (n-1, n+1) -> bad path to (n,n)."""
    r, u = 0, 0
    first_touch = None
    for i, step in enumerate(path):
        if step == 'R': r += 1
        else: u += 1
        # y = x + 1 means u = r + 1
        if u == r + 1:
            first_touch = i
            break
    
    if first_touch is None:
        return None
    
    prefix = path[:first_touch + 1]
    suffix = path[first_touch + 1:]
    
    reflected_suffix = ''.join('U' if c == 'R' else 'R' for c in suffix)
    
    return prefix + reflected_suffix

# Enumerate all paths for n=3
n = 3
length = 2 * n

# All paths from (0,0) to (3,3): choose 3 positions for R among 6
all_paths_nn = []
for r_pos in combinations(range(length), n):
    all_paths_nn.append(path_to_string(set(r_pos), length))

good_paths = [p for p in all_paths_nn if is_good(p)]
bad_paths = [p for p in all_paths_nn if not is_good(p)]

print(f"n = {n}")
print(f"Total paths (0,0)->(3,3): {len(all_paths_nn)}")
print(f"Good paths (Catalan): {len(good_paths)}")
print(f"Bad paths: {len(bad_paths)}")
print()
print("Good paths:", good_paths)
print()

# All paths from (0,0) to (2,4): choose 2 positions for R among 6
all_paths_target = []
for r_pos in combinations(range(length), n - 1):
    all_paths_target.append(path_to_string(set(r_pos), length))

print(f"Paths (0,0)->(2,4): {len(all_paths_target)}")
print()

# Apply reflection to each bad path
print("=== Reflection bijection: bad path -> path to (2,4) ===")
images = {}
for bp in bad_paths:
    img = reflect_bad_path(bp, n)
    images[bp] = img
    # Verify image is a path to (2,4)
    r_count = img.count('R')
    u_count = img.count('U')
    assert r_count == n - 1 and u_count == n + 1, f"Bad image for {bp}: {img} (R={r_count}, U={u_count})"

# Check surjectivity
image_set = set(images.values())
target_set = set(all_paths_target)
assert image_set == target_set, f"Image set != target set. Missing: {target_set - image_set}, Extra: {image_set - target_set}"
print("Surjectivity check: PASSED (image set = full target set)")

# Check injectivity
assert len(image_set) == len(bad_paths), "Injectivity failed"
print("Injectivity check: PASSED")
print()

# Verify inverse
print("=== Inverse verification ===")
all_ok = True
for bp in bad_paths:
    img = images[bp]
    recovered = reflect_inverse(img, n)
    if recovered != bp:
        print(f"FAIL: {bp} -> {img} -> {recovered}")
        all_ok = False

if all_ok:
    print("All inverse checks PASSED")
print()

# Print full table
print("=== Full bijection table for n=3 ===")
print(f"{'Bad path':<10} {'First bad pos':<14} {'Image (to (2,4))':<18} {'Inverse check'}")
for bp in sorted(bad_paths):
    img = images[bp]
    inv = reflect_inverse(img, n)
    ok = "✓" if inv == bp else "✗"
    
    # Find first bad position
    r, u = 0, 0
    fb = -1
    for i, step in enumerate(bp):
        if step == 'R': r += 1
        else: u += 1
        if u > r:
            fb = i
            break
    
    print(f"{bp:<10} step {fb} (pos {fb}){'':<4} {img:<18} {ok}")

