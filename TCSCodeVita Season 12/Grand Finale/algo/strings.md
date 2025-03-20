Below is an extensive Python template tailored for extreme world‐level string programming. This template combines fast I/O, debugging support, and a suite of advanced string algorithms—from classical pattern matching (KMP and Z‑algorithm) to palindrome search (Manacher’s algorithm), rolling hash for fast substring comparisons, and even a full Suffix Automaton for complex substring queries. You can use, test, and extend these components as needed for challenging competitive programming problems on strings.

#!/usr/bin/env python3
"""
Extensive Python Template for Extreme World-Level String Programming

Features:
-----------
1. Fast I/O & Debugging:
   - Fast input functions and a toggleable debugging routine.

2. Classical String Algorithms:
   - KMP (Knuth-Morris-Pratt) algorithm:
     * compute_prefix() to build prefix arrays.
     * kmp_search() for finding all pattern occurrences.
   - Z-Algorithm:
     * compute_z() function computes Z-array for pattern matching.

3. Palindrome Algorithms:
   - Manacher's algorithm to find the longest palindromic substring.

4. Rolling Hash:
   - A RollingHash class for efficient substring hash computations.
     (Can be used for pattern matching, checking substring equality, etc.)

5. Suffix Automaton:
   - A SuffixAutomaton class to support advanced substring queries,
     count distinct substrings, or solve related problems.

6. Main solve() Function:
   - A driver function that shows examples and serves as the entry point.
   - Adapt the reading and processing logic to your specific string problem.
"""

import sys, math, bisect
from collections import defaultdict, deque, Counter
import heapq
import itertools
from functools import reduce, lru_cache

# Increase recursion limit (if using deep recursion in some algorithms)
sys.setrecursionlimit(10**7)

# ---------------------------
# Fast Input & I/O Helpers
# ---------------------------
def input():
    return sys.stdin.readline().rstrip("\n")

def read_ints():
    return list(map(int, input().split()))

def read_strs():
    return input().split()

# ---------------------------
# Debugging Functionality
# ---------------------------
DEBUG = False  # Set to True for verbose debugging output.
def debug(*args, **kwargs):
    if DEBUG:
        print("DEBUG:", *args, **kwargs, file=sys.stderr)

# ---------------------------
# KMP (Knuth-Morris-Pratt) Algorithm
# ---------------------------
def compute_prefix(s):
    """
    Compute the prefix (or "failure") function for string s.
    prefix[i] = length of the longest proper prefix of s[:i+1] which is also a suffix.
    Time Complexity: O(len(s))
    """
    n = len(s)
    prefix = [0] * n
    for i in range(1, n):
        j = prefix[i - 1]
        while j > 0 and s[i] != s[j]:
            j = prefix[j - 1]
        if s[i] == s[j]:
            j += 1
        prefix[i] = j
    debug("Prefix array:", prefix)
    return prefix

def kmp_search(text, pattern):
    """
    Use the KMP algorithm to search for all occurrences of pattern in text.
    Returns a list of starting indices (0-indexed) where pattern occurs in text.
    Time Complexity: O(len(text) + len(pattern))
    """
    if pattern == "":
        return list(range(len(text)+1))
    prefix = compute_prefix(pattern)
    result = []
    j = 0  # index in pattern
    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = prefix[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == len(pattern):
            result.append(i - j + 1)
            j = prefix[j - 1]
    debug("KMP search result:", result)
    return result

# ---------------------------
# Z-Algorithm for Pattern Matching
# ---------------------------
def compute_z(s):
    """
    Compute the Z-array for string s.
    Z[i] = length of the longest substring starting from s[i] that is also a prefix of s.
    Time Complexity: O(len(s))
    """
    n = len(s)
    z = [0] * n
    l, r = 0, 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    debug("Z array:", z)
    return z

# ---------------------------
# Manacher's Algorithm (Longest Palindromic Substring)
# ---------------------------
def manacher(s):
    """
    Finds longest palindromic substring in s using Manacher's algorithm.
    Returns (start_index, length) of the palindrome in the original string.
    Time Complexity: O(len(s))
    """
    # Transform s to add boundaries (#) between characters.
    t = "#" + "#".join(s) + "#"
    n = len(t)
    p = [0] * n
    center = right = 0
    max_len = 0
    max_center = 0
    for i in range(n):
        mirror = 2 * center - i
        if i < right:
            p[i] = min(right - i, p[mirror])
        # Expand around center i
        while i + p[i] + 1 < n and i - p[i] - 1 >= 0 and t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1
        if i + p[i] > right:
            center, right = i, i + p[i]
        if p[i] > max_len:
            max_len = p[i]
            max_center = i
    # Convert back to original string indices.
    start = (max_center - max_len) // 2
    debug("Manacher result: start =", start, "length =", max_len)
    return start, max_len

# ---------------------------
# Rolling Hash for Strings
# ---------------------------
class RollingHash:
    """
    Rolling Hash class for string s.
    Provides O(1) substring hash queries after O(n) precomputation.
    Can be used to compare substrings or for pattern matching.
    """
    def __init__(self, s, base=257, mod=10**9+7):
        self.s = s
        self.n = len(s)
        self.base = base
        self.mod = mod
        self.prefix = [0] * (self.n + 1)
        self.power = [1] * (self.n + 1)
        for i in range(self.n):
            self.prefix[i + 1] = (self.prefix[i] * base + ord(s[i])) % mod
            self.power[i + 1] = (self.power[i] * base) % mod
        debug("RollingHash prefix:", self.prefix)
        debug("RollingHash power:", self.power)
    
    def get_hash(self, l, r):
        """
        Return hash of the substring s[l:r] (0-indexed, r is exclusive).
        """
        h = (self.prefix[r] - self.prefix[l] * self.power[r - l]) % self.mod
        return h

# ---------------------------
# Suffix Automaton
# ---------------------------
class SuffixAutomaton:
    """
    Suffix Automaton for a given string.
    It efficiently stores all substrings of the string and can be used to answer
    queries such as the number of distinct substrings.
    """
    class State:
        def __init__(self):
            self.length = 0         # max length of substring in this state
            self.link = -1          # suffix link
            self.next = {}          # transitions: char -> state index

    def __init__(self, s):
        self.states = [self.State()]
        self.size = 1
        self.last = 0  # index of the state representing the whole string
        for c in s:
            self._extend(c)
        debug("Suffix Automaton built with", self.size, "states.")

    def _extend(self, c):
        cur = self.size
        self.states.append(self.State())
        self.states[cur].length = self.states[self.last].length + 1
        self.size += 1

        p = self.last
        while p != -1 and c not in self.states[p].next:
            self.states[p].next[c] = cur
            p = self.states[p].link
        if p == -1:
            self.states[cur].link = 0
        else:
            q = self.states[p].next[c]
            if self.states[p].length + 1 == self.states[q].length:
                self.states[cur].link = q
            else:
                clone = self.size
                self.states.append(self.State())
                self.size += 1
                self.states[clone].length = self.states[p].length + 1
                self.states[clone].next = self.states[q].next.copy()
                self.states[clone].link = self.states[q].link
                while p != -1 and self.states[p].next.get(c, -1) == q:
                    self.states[p].next[c] = clone
                    p = self.states[p].link
                self.states[q].link = self.states[cur].link = clone
        self.last = cur

    def count_distinct_substrings(self):
        """
        Returns the total number of distinct substrings in the string.
        Formula: sum(state.length - state.link_length) for all states except the initial.
        """
        total = 0
        for i in range(1, self.size):
            link = self.states[i].link
            total += self.states[i].length - self.states[link].length
        return total

# ---------------------------
# Main Solve Function
# ---------------------------
def solve():
    """
    Main function to process input and produce output.
    Adapt the following examples to your specific string problem.
    """
    # Example: Toggle debugging mode if needed.
    # global DEBUG
    # DEBUG = True if input().strip() == "DEBUG" else False

    # Example: Read input string.
    s = input().strip()
    debug("Input string:", s)

    # Example 1: KMP Pattern Matching
    pattern = input().strip()
    occurrences = kmp_search(s, pattern)
    print("KMP Occurrences at indices:", " ".join(map(str, occurrences)))

    # Example 2: Z-Algorithm Pattern Matching
    # To find pattern occurrences, we combine pattern and text with a special separator.
    combined = pattern + "$" + s
    z_array = compute_z(combined)
    result = []
    pat_len = len(pattern)
    for i in range(pat_len + 1, len(combined)):
        if z_array[i] >= pat_len:
            result.append(i - pat_len - 1)
    print("Z-Algorithm Occurrences at indices:", " ".join(map(str, result)))

    # Example 3: Manacher's Algorithm for Longest Palindromic Substring
    start, length = manacher(s)
    longest_palindrome = s[start:start+length]
    print("Longest Palindromic Substring:", longest_palindrome)

    # Example 4: Rolling Hash
    rh = RollingHash(s)
    # For demonstration: Compare hash of two substrings (if indices are valid)
    # (Adjust indices as necessary for your problem.)
    l1, r1 = 0, len(s)//2
    l2, r2 = len(s)//2, len(s)
    hash1 = rh.get_hash(l1, r1)
    hash2 = rh.get_hash(l2, r2)
    print("Hash of first half:", hash1)
    print("Hash of second half:", hash2)

    # Example 5: Suffix Automaton usage
    sam = SuffixAutomaton(s)
    distinct_count = sam.count_distinct_substrings()
    print("Total distinct substrings:", distinct_count)

# ---------------------------
# Entry Point
# ---------------------------
if __name__ == '__main__':
    solve()

Template Overview

Fast I/O & Debug:
Custom input functions and a DEBUG flag help you quickly test with detailed internal state messages.

KMP & Z-Algorithm:
Functions to compute prefix arrays and Z-arrays support efficient pattern matching and substring search.

Manacher’s Algorithm:
Find the longest palindromic substring in linear time.

Rolling Hash:
The RollingHash class allows O(1) substring hash queries after an O(n) precomputation step.

Suffix Automaton:
Build a suffix automaton to answer advanced substring queries and count distinct substrings.

Main Function:
The solve() function demonstrates sample usage. Adapt it to fit the specific requirements of your extreme string programming problems.


This comprehensive template is designed for high-level string problems seen in international programming contests. Modify and extend its components as needed for your challenges.

