"""
Verify the Cycle Lemma and its application to Catalan numbers.

Cycle Lemma (Dvoretzky-Motzkin): A sequence of m X's and k Y's with m > k
has exactly (m - k) dominating cyclic shifts.
(Dominating = every prefix has strictly more X's than Y's.)

Application to Catalan: m = n+1, k = n. Exactly 1 dominating shift.
Each of C(2n+1, n) sequences of (n+1) X's and n Y's has exactly 1 dominating shift.
Removing the first X from the dominating shift gives a Dyck word.
So: C_n = C(2n+1, n) / (2n+1) = C(2n, n) / (n+1).
"""
from itertools import combinations
from collections import Counter

def is_dominating(seq):
    """Check if sequence is dominating: every prefix has #X > #Y."""
    x_count, y_count = 0, 0
    for c in seq:
        if c == 'X': x_count += 1
        else: y_count += 1
        if x_count <= y_count:
            return False
    return True

def is_dyck(seq):
    """Check if sequence is a Dyck word: #X = #Y and every prefix has #X >= #Y."""
    x_count, y_count = 0, 0
    for c in seq:
        if c == 'X': x_count += 1
        else: y_count += 1
        if x_count < y_count:
            return False
    return x_count == y_count

def cyclic_shift(seq, k):
    """Return the k-th cyclic shift: seq[k:] + seq[:k]."""
    return seq[k:] + seq[:k]

def find_dominating_shift(seq):
    """Find the unique dominating cyclic shift. Returns shift index or None."""
    n = len(seq)
    results = []
    for k in range(n):
        shifted = cyclic_shift(seq, k)
        if is_dominating(shifted):
            results.append(k)
    return results

def seq_to_dyck(seq):
    """Convert sequence of (n+1) X's and n Y's to Dyck word.
    Find dominating shift, remove first X."""
    shifts = find_dominating_shift(seq)
    assert len(shifts) == 1, f"Expected 1 dominating shift, got {len(shifts)} for {seq}"
    k = shifts[0]
    dom = cyclic_shift(seq, k)
    assert dom[0] == 'X', f"Dominating shift should start with X: {dom}"
    dyck = dom[1:]  # remove first X
    assert is_dyck(dyck), f"Result should be Dyck word: {dyck}"
    return dyck, k

def dyck_to_seq(dyck, orig_len, shift_index):
    """Inverse: given Dyck word and shift index, recover original sequence.
    Prepend X to get dominating sequence, then un-shift by shift_index."""
    dom = 'X' + dyck
    # Un-shift: if we shifted by k to get dom, then original = shift(dom, -k) = shift(dom, len-k)
    n = len(dom)
    orig = cyclic_shift(dom, n - shift_index)
    return orig

# ======= Verify for n=2 =======
print("=" * 60)
print("Cycle Lemma verification for n=2")
print("=" * 60)
n = 2
m = n + 1  # 3 X's
k = n      # 2 Y's
total_len = m + k  # 5

# Generate all sequences of 3 X's and 2 Y's
all_seqs = []
for y_pos in combinations(range(total_len), k):
    seq = ['X'] * total_len
    for p in y_pos:
        seq[p] = 'Y'
    all_seqs.append(''.join(seq))

print(f"\nAll C({total_len},{k}) = {len(all_seqs)} sequences of {m} X's and {k} Y's:")

dyck_counter = Counter()  # count how many seqs map to each Dyck word

print(f"\n{'Sequence':<10} {'Dom shift':<10} {'Dominating':<12} {'Dyck word':<10}")
for seq in all_seqs:
    shifts = find_dominating_shift(seq)
    assert len(shifts) == 1, f"FAIL: {seq} has {len(shifts)} dominating shifts"
    k_shift = shifts[0]
    dom = cyclic_shift(seq, k_shift)
    dyck = dom[1:]
    dyck_counter[dyck] += 1
    print(f"  {seq:<10} k={k_shift:<8} {dom:<12} {dyck}")

print(f"\nDyck words and their multiplicities:")
for dyck_word, count in sorted(dyck_counter.items()):
    print(f"  {dyck_word}: {count} sequences")

print(f"\nNumber of distinct Dyck words: {len(dyck_counter)} (should be C_{n} = {[1,1,2,5,14][n]})")
print(f"Each Dyck word appears exactly {total_len} times (should be {total_len}): ", end="")
print("✓" if all(c == total_len for c in dyck_counter.values()) else "✗")

# ======= Verify round-trip =======
print(f"\n=== Round-trip verification ===")
all_ok = True
for seq in all_seqs:
    dyck, k_shift = seq_to_dyck(seq)
    recovered = dyck_to_seq(dyck, total_len, k_shift)
    if recovered != seq:
        print(f"  FAIL: {seq} -> dyck={dyck}, k={k_shift} -> {recovered}")
        all_ok = False
print(f"Round-trip: {'ALL PASSED ✓' if all_ok else 'FAILED ✗'}")

# ======= Also verify for n=3 =======
print(f"\n{'='*60}")
print(f"Cycle Lemma verification for n=3")
print(f"{'='*60}")
n = 3
m = n + 1; k = n; total_len = m + k
all_seqs = []
for y_pos in combinations(range(total_len), k):
    seq = ['X'] * total_len
    for p in y_pos:
        seq[p] = 'Y'
    all_seqs.append(''.join(seq))

print(f"C({total_len},{k}) = {len(all_seqs)} sequences")
dyck_counter = Counter()
for seq in all_seqs:
    shifts = find_dominating_shift(seq)
    assert len(shifts) == 1
    dyck, _ = seq_to_dyck(seq)
    dyck_counter[dyck] += 1

print(f"Distinct Dyck words: {len(dyck_counter)} (C_3 = 5)")
print(f"Each appears {total_len} times: ", end="")
print("✓" if all(c == total_len for c in dyck_counter.values()) else "✗")

# Round-trip
all_ok = True
for seq in all_seqs:
    dyck, k_shift = seq_to_dyck(seq)
    recovered = dyck_to_seq(dyck, total_len, k_shift)
    if recovered != seq: all_ok = False
print(f"Round-trip: {'ALL PASSED ✓' if all_ok else 'FAILED ✗'}")

# ======= Algorithm for finding dominating shift efficiently =======
print(f"\n{'='*60}")
print(f"Efficient algorithm: XY-cancellation method")
print(f"{'='*60}")

def find_dominating_shift_efficient(seq):
    """Find dominating shift by XY-cancellation on the circular sequence.
    
    Algorithm:
    1. Arrange sequence on a circle.
    2. Repeatedly remove adjacent XY pairs (X immediately followed by Y).
    3. What remains is (m-k) consecutive X's on the circle.
    4. Each remaining X marks the start of a dominating shift.
    For m-k=1 (Catalan case): exactly one X remains.
    """
    n = len(seq)
    # Work with indices to track which X survives
    chars = list(seq)
    indices = list(range(n))
    
    # Repeatedly remove XY pairs until no more can be removed
    changed = True
    while changed:
        changed = False
        new_chars = []
        new_indices = []
        i = 0
        while i < len(chars):
            if i + 1 < len(chars) and chars[i] == 'X' and chars[i+1] == 'Y':
                # Remove this XY pair
                changed = True
                i += 2
            else:
                new_chars.append(chars[i])
                new_indices.append(indices[i])
                i += 1
        # Also check wrap-around: last char is X, first is Y
        if len(new_chars) >= 2 and new_chars[-1] == 'X' and new_chars[0] == 'Y':
            new_chars = new_chars[1:-1]
            new_indices = new_indices[1:-1]
            changed = True
        chars = new_chars
        indices = new_indices
    
    # Remaining should be exactly (m-k) X's
    return indices

# Test efficient algorithm
print("\nTesting efficient algorithm on n=2 sequences:")
n = 2; m = n+1; k = n; total_len = m + k
all_seqs_2 = []
for y_pos in combinations(range(total_len), k):
    seq = ['X'] * total_len
    for p in y_pos: seq[p] = 'Y'
    all_seqs_2.append(''.join(seq))

all_match = True
for seq in all_seqs_2:
    brute = find_dominating_shift(seq)
    efficient = find_dominating_shift_efficient(seq)
    if brute != efficient:
        print(f"  MISMATCH: {seq}: brute={brute}, efficient={efficient}")
        all_match = False
print(f"Efficient vs brute-force: {'ALL MATCH ✓' if all_match else 'MISMATCH ✗'}")

# Also test n=3
all_seqs_3 = []
n = 3; m = n+1; k = n; total_len = m + k
for y_pos in combinations(range(total_len), k):
    seq = ['X'] * total_len
    for p in y_pos: seq[p] = 'Y'
    all_seqs_3.append(''.join(seq))

all_match = True
for seq in all_seqs_3:
    brute = find_dominating_shift(seq)
    efficient = find_dominating_shift_efficient(seq)
    if brute != efficient:
        print(f"  MISMATCH: {seq}: brute={brute}, efficient={efficient}")
        all_match = False
print(f"Efficient vs brute-force (n=3): {'ALL MATCH ✓' if all_match else 'MISMATCH ✗'}")

