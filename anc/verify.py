#!/usr/bin/env python3
"""Exact verification of the theorems and constants in the paper.

Runs in a few seconds with the Python standard library only:

    python3 verify.py

Each check prints PASS or raises an AssertionError.
"""
from fractions import Fraction as Fr
from itertools import combinations


def permanent(M):
    """Exact permanent by dynamic programming over column subsets."""
    n = len(M)
    dp = {0: Fr(1)}
    for i in range(n):
        new = {}
        for mask, val in dp.items():
            for j in range(n):
                if M[i][j] != 0 and not mask & (1 << j):
                    key = mask | (1 << j)
                    new[key] = new.get(key, 0) + val * M[i][j]
        dp = new
    return dp.get((1 << n) - 1, Fr(0))


def minor(M, i, j):
    return [[M[r][c] for c in range(len(M)) if c != j]
            for r in range(len(M)) if r != i]


def support(M):
    return [[1 if x != 0 else 0 for x in row] for row in M]


def fully_indecomposable(S):
    """S (0/1, n >= 2) is fully indecomposable via Brualdi-Ryser Theorem 4.2.2."""
    n = len(S)
    rows = [sum(1 << j for j, x in enumerate(row) if x) for row in S]
    if any(r == 0 or (r & (r - 1)) == 0 for r in rows):
        return False
    col_to_row = [-1] * n
    for r in range(n):
        seen = 0

        def aug(u):
            nonlocal seen
            m = rows[u]
            while m:
                lb = m & -m
                c = lb.bit_length() - 1
                m ^= lb
                if not (seen >> c) & 1:
                    seen |= 1 << c
                    if col_to_row[c] == -1 or aug(col_to_row[c]):
                        col_to_row[c] = u
                        return True
            return False

        if not aug(r):
            return False
    fwd, rev = [0] * n, [0] * n
    for u in range(n):
        m = rows[u]
        while m:
            lb = m & -m
            c = lb.bit_length() - 1
            m ^= lb
            v = col_to_row[c]
            if u != v:
                fwd[u] |= 1 << v
                rev[v] |= 1 << u
    full = (1 << n) - 1
    for adj in (fwd, rev):
        vis = frontier = 1
        while frontier:
            lb = frontier & -frontier
            u = lb.bit_length() - 1
            frontier ^= lb
            nxt = adj[u] & ~vis
            vis |= nxt
            frontier |= nxt
        if vis != full:
            return False
    return True


def nearly_decomposable(S):
    if not fully_indecomposable(S):
        return False
    n = len(S)
    for i in range(n):
        if sum(S[i]) < 3:
            continue
        for j in range(n):
            if S[i][j]:
                S[i][j] = 0
                ok = fully_indecomposable(S)
                S[i][j] = 1
                if ok:
                    return False
    return True


def doubly_stochastic(M):
    n = len(M)
    return (all(x >= 0 for row in M for x in row)
            and all(sum(row) == 1 for row in M)
            and all(sum(M[i][j] for i in range(n)) == 1 for j in range(n)))


def necklace(m, k, q):
    """The matrix N(m, k, q) of Section 2: m blocks, each followed by k ear rows."""
    q = Fr(q)
    a = (1 + q) / 4
    c = (1 - q) / 2
    size = 3 + k
    n = m * size
    M = [[Fr(0)] * n for _ in range(n)]
    for t in range(m):
        o = t * size                      # offset of block t
        nxt = ((t + 1) % m) * size        # offset of the next block
        for i in (0, 1):
            for j in (0, 1):
                M[o + i][o + j] = a
            M[o + i][o + 2] = c
            M[o + 2][o + i] = c
        # ear: row o+2 -> ear columns -> ... -> column 2 of the next block
        if k == 0:
            M[o + 2][nxt + 2] = q
        else:
            M[o + 2][o + 3] = q
            for e in range(k):
                M[o + 3 + e][o + 3 + e] = 1 - q
                if e < k - 1:
                    M[o + 3 + e][o + 4 + e] = q
            M[o + 3 + k - 1][nxt + 2] = q
    return M


def formula(m, k, q):
    q = Fr(q)
    through = q ** (k + 1) * (1 + q) ** 2 / 8
    idle = (1 - q) ** (k + 2) * (1 + q) / 4
    return through ** m + idle ** m


def nnz(M):
    return sum(1 for row in M for x in row if x != 0)


# ---------------------------------------------------------------- Theorem 1
A = necklace(1, 3, Fr(1, 2))
B = [[int(8 * x) for x in row] for row in A]
assert B == [[3, 3, 2, 0, 0, 0],
             [3, 3, 2, 0, 0, 0],
             [2, 2, 0, 4, 0, 0],
             [0, 0, 0, 4, 4, 0],
             [0, 0, 0, 0, 4, 4],
             [0, 0, 4, 0, 0, 4]], B
assert doubly_stochastic(A)
assert nnz(A) == 15 == 3 * 6 - 3
assert permanent(B) == 7680 and 8 ** 6 // 2 ** 5 == 8192
assert permanent(A) == Fr(15, 512) < Fr(1, 32)
assert fully_indecomposable(support(A)) and not nearly_decomposable(support(A))
print("PASS  Theorem 1: the 6x6 matrix (15 entries, per = 15/512 < 16/512)")

# ------------------------------------------------- Theorem 2 (every n >= 3)
for k in range(0, 9):
    n = 3 + k
    M = necklace(1, k, Fr(1, 2))
    assert doubly_stochastic(M)
    assert nnz(M) == 2 * n + 3
    assert (2 * n + 3 <= 3 * n - 3) == (n >= 6)
    assert {x for row in M for x in row if x} <= {Fr(1, 4), Fr(3, 8), Fr(1, 2)}
    assert permanent(M) == Fr(15, 16) / 2 ** (n - 1)
    assert fully_indecomposable(support(M)) and not nearly_decomposable(support(M))
print("PASS  Theorem 2: n = 3..11, 2n+3 entries, per = (15/16) 2^(1-n)")

# ------------------------------------------------ Lemma (permanent formula)
count = 0
for (m, k) in [(1, 0), (1, 1), (1, 2), (1, 3), (1, 5), (2, 1), (2, 2), (3, 1), (4, 1), (2, 3)]:
    for q in (Fr(1, 2), Fr(6, 13), Fr(2, 7), Fr(47, 100)):
        M = necklace(m, k, q)
        assert doubly_stochastic(M)
        assert permanent(M) == formula(m, k, q), (m, k, q)
        assert nnz(M) == m * (9 + 2 * k)
        count += 1
assert count == 40
print(f"PASS  Lemma: per N(m,k,q) = through^m + idle^m on {count} instances")

# ------------------------------------------ Theorem 3 (exponential failure)
q = Fr(6, 13)
alpha = 16 * q ** 2 * (1 + q) ** 2 / 8        # 2^4 * through-factor (k = 1)
beta = 16 * (1 - q) ** 3 * (1 + q) / 4        # 2^4 * idle-factor   (k = 1)
assert alpha == Fr(25992, 28561) and beta == Fr(26068, 28561)
assert alpha < beta < 1
assert beta < Fr(978, 1000) ** 4
for m in (3, 4, 5):
    n = 4 * m
    M = necklace(m, 1, q)
    assert doubly_stochastic(M)
    assert nnz(M) == 11 * m <= 3 * n - 3
    rho = permanent(M) * 2 ** (n - 1)
    assert rho == (alpha ** m + beta ** m) / 2 < beta ** m
    assert fully_indecomposable(support(M)) and not nearly_decomposable(support(M))
    print(f"      m = {m}, n = {n}: 2^(n-1) per = {float(rho):.6f} (FI, not ND)")
print("PASS  Theorem 3: q = 6/13, 2^(n-1) per < (26068/28561)^(n/4)")

# ------------------------------------------------ Remark on constants
best = min((formula(1, 3, Fr(i, 10000)) * 32, Fr(i, 10000)) for i in range(4000, 5500))
assert abs(best[1] - Fr(4723, 10000)) < Fr(1, 1000) and abs(best[0] - Fr(9134, 10000)) < Fr(1, 10000)
g3 = Fr(2, 3) ** 2
assert g3 == Fr(4, 9) and 2 * g3 == Fr(8, 9)
print(f"PASS  Remark: for n = 6 the best q is about {float(best[1]):.4f}, "
      f"2^5 per = {float(best[0]):.4f}; g(3) = 4/9 gives the rate 8/9")
