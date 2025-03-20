Below is an extensive Python template aimed at tackling advanced problems on numbers and sequences. It combines fast I/O, debugging utilities, core arithmetic functions, combinatorial precomputation, prime sieves and factorization, dynamic programming (including longest increasing subsequence), as well as several powerful data structures (Segment Tree, Fenwick Tree, Sparse Table) and even matrix exponentiation for recurrences. You can adapt and extend each section as needed.

#!/usr/bin/env python3
"""
Extensive Python Template for Numbers and Sequences

This template provides a robust framework for solving advanced problems involving numbers,
sequences, combinatorics, and dynamic programming. It includes:

1. Fast I/O and debugging utilities.
2. Fundamental math functions: GCD, LCM, modular exponentiation, modular inverses.
3. Combinatorial precomputation: Factorials, inverse factorials, nCr.
4. Sieve of Eratosthenes for prime generation and a prime factorization routine.
5. Extended Euclidean algorithm.
6. Dynamic Programming helpers:
   - Generic DP examples.
   - Longest Increasing Subsequence (LIS) using binary search.
7. Data Structures for sequence queries:
   - Segment Tree for range queries.
   - Fenwick Tree (Binary Indexed Tree) for prefix sums.
   - Sparse Table for static range minimum/maximum queries.
8. Matrix Exponentiation for recurrences.
9. A main solve() function demonstrating sample usage.

Customize each section as per your problem requirements.
"""

import sys, math, bisect
from collections import defaultdict, deque, Counter
import heapq
import itertools
from functools import lru_cache, reduce

# Increase recursion limit for deep recursions if needed.
sys.setrecursionlimit(10**7)

# ---------------------------
# Fast I/O and Debugging
# ---------------------------
def input():
    return sys.stdin.readline().rstrip("\n")

def read_ints():
    return list(map(int, input().split()))

def read_strs():
    return input().split()

DEBUG = False  # Toggle this flag for verbose debugging output.
def debug(*args, **kwargs):
    if DEBUG:
        print("DEBUG:", *args, **kwargs, file=sys.stderr)

# ---------------------------
# Math Utilities
# ---------------------------
def gcd(a, b):
    """Compute the greatest common divisor (GCD) of a and b."""
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Compute the least common multiple (LCM) of a and b."""
    return a // gcd(a, b) * b

def modinv(a, mod=10**9+7):
    """Compute the modular inverse of a modulo mod (mod must be prime)."""
    return pow(a, mod-2, mod)

def binpow(a, b, mod=10**9+7):
    """Efficiently compute a^b modulo mod using binary exponentiation."""
    res = 1
    while b:
        if b & 1:
            res = res * a % mod
        a = a * a % mod
        b //= 2
    return res

# ---------------------------
# Combinatorics Utilities
# ---------------------------
MOD = 10**9+7

def precompute_factorials(n, mod=MOD):
    """
    Precompute factorials and inverse factorials up to n.
    Returns two lists: fact and inv_fact.
    """
    fact = [1] * (n+1)
    inv_fact = [1] * (n+1)
    for i in range(2, n+1):
        fact[i] = fact[i-1] * i % mod
    inv_fact[n] = modinv(fact[n], mod)
    for i in range(n, 0, -1):
        inv_fact[i-1] = inv_fact[i] * i % mod
    return fact, inv_fact

def nCr(n, r, fact, inv_fact, mod=MOD):
    """Compute combination nCr modulo mod using precomputed factorials."""
    if r < 0 or r > n:
        return 0
    return fact[n] * inv_fact[r] % mod * inv_fact[n-r] % mod

# ---------------------------
# Sieve of Eratosthenes and Prime Factorization
# ---------------------------
def sieve(n):
    """
    Generate primes up to n (inclusive) using the Sieve of Eratosthenes.
    Returns a list of primes and an is_prime list.
    """
    is_prime = [True] * (n+1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5)+1):
        if is_prime[i]:
            for j in range(i*i, n+1, i):
                is_prime[j] = False
    primes = [i for i, prime in enumerate(is_prime) if prime]
    return primes, is_prime

def prime_factors(n):
    """
    Compute the prime factorization of n.
    Returns a dictionary where keys are prime factors and values are their exponents.
    """
    factors = {}
    # Count factors of 2.
    while n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n //= 2
    # Check odd factors.
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors[i] = factors.get(i, 0) + 1
            n //= i
        i += 2
    if n > 2:
        factors[n] = 1
    return factors

# ---------------------------
# Extended Euclidean Algorithm
# ---------------------------
def extended_gcd(a, b):
    """
    Extended Euclidean Algorithm.
    Returns a tuple (g, x, y) such that ax + by = g = gcd(a, b).
    """
    if b == 0:
        return (a, 1, 0)
    else:
        g, x, y = extended_gcd(b, a % b)
        return (g, y, x - (a // b) * y)

# ---------------------------
# Dynamic Programming and Sequence Algorithms
# ---------------------------
def dp_template(seq):
    """
    A generic dynamic programming example over a sequence.
    (For instance, computing the length of an increasing subsequence.)
    """
    n = len(seq)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if seq[j] < seq[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

def longest_increasing_subsequence(seq):
    """
    Compute the length of the longest increasing subsequence (LIS)
    in O(n log n) using binary search.
    """
    sub = []
    for x in seq:
        pos = bisect.bisect_left(sub, x)
        if pos == len(sub):
            sub.append(x)
        else:
            sub[pos] = x
    return len(sub)

# ---------------------------
# Data Structures for Sequences
# ---------------------------
# Segment Tree: Supports range queries (min, max, sum, etc.)
class SegmentTree:
    def __init__(self, data, func=min, default=float('inf')):
        self.n = len(data)
        self.func = func
        self.default = default
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [default] * (2 * self.size)
        for i in range(self.n):
            self.tree[self.size + i] = data[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = func(self.tree[2*i], self.tree[2*i+1])
    
    def update(self, idx, value):
        idx += self.size
        self.tree[idx] = value
        while idx > 1:
            idx //= 2
            self.tree[idx] = self.func(self.tree[2*idx], self.tree[2*idx+1])
    
    def query(self, l, r):
        """
        Query in the interval [l, r) (l inclusive, r exclusive).
        """
        res = self.default
        l += self.size
        r += self.size
        while l < r:
            if l & 1:
                res = self.func(res, self.tree[l])
                l += 1
            if r & 1:
                r -= 1
                res = self.func(res, self.tree[r])
            l //= 2
            r //= 2
        return res

# Fenwick Tree (Binary Indexed Tree): For efficient prefix sum queries.
class FenwickTree:
    def __init__(self, size):
        self.size = size
        self.tree = [0] * (size + 1)
    
    def update(self, idx, delta):
        """
        Increase the value at index idx (0-indexed) by delta.
        """
        idx += 1
        while idx <= self.size:
            self.tree[idx] += delta
            idx += idx & -idx
    
    def query(self, idx):
        """
        Compute prefix sum for index idx (0-indexed, inclusive).
        """
        idx += 1
        s = 0
        while idx:
            s += self.tree[idx]
            idx -= idx & -idx
        return s
    
    def range_query(self, l, r):
        """
        Compute the sum over the range [l, r] (inclusive).
        """
        return self.query(r) - (self.query(l-1) if l > 0 else 0)

# Sparse Table: For static range queries (e.g., minimum, maximum) in O(1) after O(n log n) preprocessing.
class SparseTable:
    def __init__(self, data, func=min):
        self.n = len(data)
        self.func = func
        self.log = [0] * (self.n + 1)
        for i in range(2, self.n + 1):
            self.log[i] = self.log[i//2] + 1
        k = self.log[self.n] + 1
        self.st = [[0] * self.n for _ in range(k)]
        self.st[0] = data[:]
        for j in range(1, k):
            i = 0
            while i + (1 << j) <= self.n:
                self.st[j][i] = func(self.st[j-1][i], self.st[j-1][i + (1 << (j-1))])
                i += 1
    
    def query(self, l, r):
        """
        Answer query on the interval [l, r] (inclusive).
        """
        j = self.log[r - l + 1]
        return self.func(self.st[j][l], self.st[j][r - (1 << j) + 1])

# ---------------------------
# Matrix Exponentiation for Recurrences
# ---------------------------
def mat_mult(A, B, mod=MOD):
    """
    Multiply two matrices A and B under modulo mod.
    Both A and B are lists of lists.
    """
    n, m, p = len(A), len(B), len(B[0])
    res = [[0]*p for _ in range(n)]
    for i in range(n):
        for j in range(p):
            for k in range(m):
                res[i][j] = (res[i][j] + A[i][k] * B[k][j]) % mod
    return res

def mat_pow(A, power, mod=MOD):
    """
    Compute the matrix A raised to the power 'power' under modulo mod.
    """
    n = len(A)
    res = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    while power:
        if power & 1:
            res = mat_mult(res, A, mod)
        A = mat_mult(A, A, mod)
        power //= 2
    return res

# ---------------------------
# Main Solve Function
# ---------------------------
def solve():
    """
    Main function to process input and output.
    Adapt the examples below to your specific problem involving numbers and sequences.
    """
    # Example: Toggle DEBUG mode if needed.
    # global DEBUG
    # DEBUG = True if input().strip() == "DEBUG" else False

    # Read the size of the sequence and the sequence itself.
    n = int(input())
    seq = read_ints()  # Sequence of numbers
    debug("Input sequence:", seq)

    # Example 1: Compute the length of the longest increasing subsequence.
    lis_length = longest_increasing_subsequence(seq)
    print("Longest Increasing Subsequence length:", lis_length)

    # Example 2: Precompute factorials up to a limit (adjust limit as required).
    limit = max(n, max(seq)) + 10
    fact, inv_fact = precompute_factorials(limit)
    # Compute a sample combination, e.g., nCr(10, 3)
    n_val, r_val = 10, 3
    comb = nCr(n_val, r_val, fact, inv_fact)
    print(f"nCr({n_val}, {r_val}) =", comb)

    # Example 3: Generate primes up to a limit using the sieve.
    sieve_limit = 100
    primes, is_prime = sieve(sieve_limit)
    print("Primes up to", sieve_limit, ":", primes)

    # Example 4: Prime factorization of the first element in the sequence (if valid).
    if seq and seq[0] > 1:
        factors = prime_factors(seq[0])
        print("Prime factors of", seq[0], ":", factors)

    # Example 5: Use a Segment Tree to answer a range minimum query.
    seg_tree = SegmentTree(seq, func=min, default=float('inf'))
    range_min = seg_tree.query(1, n)  # Query from index 1 to n-1 (0-indexed)
    print("Minimum in sequence (excluding first element):", range_min)

    # Example 6: Build a Fenwick Tree for prefix sum queries.
    fenw = FenwickTree(n)
    for i, x in enumerate(seq):
        fenw.update(i, x)
    prefix_sum = fenw.query(n-1)
    print("Prefix sum of entire sequence:", prefix_sum)

    # Example 7: Build a Sparse Table for range minimum queries.
    st = SparseTable(seq, func=min)
    range_min_st = st.query(0, n-1)
    print("Sparse Table minimum over entire sequence:", range_min_st)

    # Example 8: Matrix Exponentiation to compute recurrences.
    # For instance, compute the nth Fibonacci number.
    if n > 0:
        F = [[1, 1], [1, 0]]
        F_power = mat_pow(F, n-1, MOD)
        fib_n = F_power[0][0]  # Fibonacci(n) with F(1)=1, F(0)=0
        print(f"{n}th Fibonacci number:", fib_n)

# ---------------------------
# Entry Point
# ---------------------------
if __name__ == '__main__':
    solve()

Template Overview

Fast I/O & Debug:
Custom input functions and a DEBUG flag let you quickly test with verbose internal state messages.

Math & Combinatorics:
Includes GCD, LCM, modular arithmetic, factorial precomputation, and combination calculations.

Prime Algorithms:
Sieve for generating primes and routines for prime factorization.

Dynamic Programming & Sequences:
Contains a generic DP template and an efficient binary search–based solution for the longest increasing subsequence.

Data Structures:
Segment Tree, Fenwick Tree, and Sparse Table implementations help you process sequence queries rapidly.

Matrix Exponentiation:
Useful for solving linear recurrences like the Fibonacci numbers.

Main Function:
Demonstrates sample usage and serves as the entry point for problem-specific logic.


This comprehensive template should serve as a strong foundation for tackling extreme world-level problems on numbers and sequences. Feel free to modify and extend each section based on the problem requirements.

