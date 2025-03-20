Below is a complete Python script that implements the three template functions from competitive programming—building the suffix array, creating the longest common prefix (LCP) array, and lexicographically comparing two suffixes using an RMQ (range‐minimum query) via a “sparse table.” Comments and print statements explain what each part does and when to use it. You can run this script in a CodeVita‐like environment (it reads input from standard input).

---

```python
import math
import sys

def build_suffix_array(s):
    """
    Build the suffix array for string s using the "doubling" algorithm.
    A suffix array is an array of starting positions of all suffixes of s,
    sorted in lexicographical order.
    
    How it works:
    1. Append a special character (here '$') that is lexicographically smallest.
    2. Initially sort the suffixes by their first character.
    3. Then iteratively sort by 2^k length prefixes (using previously computed classes).
    
    When to use:
    - When you need to quickly answer queries about the lexicographical order of suffixes.
    - Useful in many string processing problems like substring search, pattern matching, etc.
    
    How to use:
    - Call build_suffix_array(your_string) and it returns a list of indices.
    """
    s += "$"  # Append a terminal character (must be smallest lexicographically)
    n = len(s)
    # Initial sorting by the first character
    sa = sorted(range(n), key=lambda i: s[i])
    
    # equivalence classes: assign a class (or rank) to each suffix based on its first character
    classes = [0] * n
    for i in range(1, n):
        classes[sa[i]] = classes[sa[i-1]]
        if s[sa[i]] != s[sa[i-1]]:
            classes[sa[i]] += 1
    
    k = 0
    while (1 << k) < n:
        # Sort by (current class, class of index + 2^k) for each suffix
        sa = sorted(range(n), key=lambda i: (classes[i], classes[(i + (1 << k)) % n]))
        new_classes = [0] * n
        for i in range(1, n):
            prev = (classes[sa[i-1]], classes[(sa[i-1] + (1 << k)) % n])
            curr = (classes[sa[i]], classes[(sa[i] + (1 << k)) % n])
            new_classes[sa[i]] = new_classes[sa[i-1]]
            if curr != prev:
                new_classes[sa[i]] += 1
        classes = new_classes
        k += 1
    # Remove the added terminal suffix (at index 0)
    return sa[1:]

def build_lcp(s, sa):
    """
    Build the LCP (Longest Common Prefix) array using Kasai's algorithm.
    lcp[i] is the length of the longest common prefix of suffixes starting at 
    positions sa[i] and sa[i+1].
    
    When to use:
    - When you need to know how many characters two consecutive suffixes share.
    - This is used in many string problems such as counting different substrings.
    
    How to use:
    - Call build_lcp(your_string, suffix_array) and it returns an array lcp.
    """
    n = len(s)
    rank = [0] * n
    for i, pos in enumerate(sa):
        rank[pos] = i
    lcp = [0] * (n - 1)
    k = 0
    for i in range(n):
        if rank[i] == n - 1:
            k = 0
            continue
        j = sa[rank[i] + 1]
        while i + k < n and j + k < n and s[i + k] == s[j + k]:
            k += 1
        lcp[rank[i]] = k
        if k:
            k -= 1
    return lcp

class SparseTable:
    """
    Sparse Table for range minimum queries (RMQ) on the LCP array.
    After precomputation, it can answer the query for the minimum value
    in any interval of the LCP array in O(1) time.
    
    When to use:
    - When you need to quickly query the minimum (or maximum) in a range.
    - Useful for comparing suffixes in O(1) time after O(n log n) precomputation.
    """
    def __init__(self, arr):
        self.n = len(arr)
        # Precompute logarithms for query time.
        self.log = [0] * (self.n + 1)
        for i in range(2, self.n + 1):
            self.log[i] = self.log[i // 2] + 1
        self.k = self.log[self.n] + 1
        # Build the sparse table st[k][i] holds the minimum of arr[i...i+2^k-1]
        self.st = [[0] * self.n for _ in range(self.k)]
        for i in range(self.n):
            self.st[0][i] = arr[i]
        j = 1
        while (1 << j) <= self.n:
            i = 0
            while i + (1 << j) - 1 < self.n:
                self.st[j][i] = min(self.st[j-1][i], self.st[j-1][i + (1 << (j-1))])
                i += 1
            j += 1

    def query(self, L, R):
        """ Return the minimum value in the interval [L, R] of the array. """
        j = self.log[R - L + 1]
        return min(self.st[j][L], self.st[j][R - (1 << j) + 1])

def compute_inverse(sa, n):
    """
    Compute the inverse suffix array.
    For each index i in the original string, inv[i] is the position of suffix i in the sorted suffix array.
    """
    inv = [0] * n
    for i, pos in enumerate(sa):
        inv[pos] = i
    return inv

def lcp_cmp(inv, st, i, j, K):
    """
    Lexicographically compare the suffixes of the original string starting at i and j,
    considering only up to K characters.
    
    How it works:
    1. Uses the inverse suffix array (inv) to know the order of each suffix.
    2. Uses the sparse table (st) on the LCP array to quickly find the common prefix length.
    3. If the common prefix length is at least K, they are considered equal up to K characters.
       Otherwise, the lexicographical order is determined by the order in the suffix array.
       
    When to use:
    - When you need to compare two suffixes lexicographically (up to K characters) quickly.
    
    How to use:
    - Provide the inverse suffix array (inv), a SparseTable built on the LCP array, the two indices (i and j)
      to compare, and K (number of characters to compare).
    """
    if i == j:
        return 0
    # Get positions in the suffix array for i and j
    pos_i = inv[i]
    pos_j = inv[j]
    # Ensure pos_i is less than pos_j to query the LCP array (which is built between adjacent suffixes in sa)
    L = min(pos_i, pos_j)
    R = max(pos_i, pos_j) - 1  # query in LCP array from L to R (inclusive)
    l = st.query(L, R) if L <= R else 0
    if l >= K:
        return 0
    # If not equal up to K characters, compare their order in the suffix array
    return -1 if pos_i < pos_j else 1

def main():
    """
    Main function to:
    1. Read input from standard input.
    2. Build the suffix array.
    3. Build the LCP array.
    4. Demonstrate lexicographical comparison between two suffixes.
    
    Input format (for demonstration purposes):
      - First line: the string.
      - Second line: two integers i and j (the starting indices of two suffixes to compare).
      - Third line: integer K (the number of characters to compare).
    
    Example input:
        banana
        1 3
        2
    """
    # Read input from standard input (CodeVita style)
    data = sys.stdin.read().strip().split()
    if not data:
        print("No input provided.")
        return
    s = data[0]
    # Build suffix array for string s
    sa = build_suffix_array(s)
    print("Suffix Array (starting indices of sorted suffixes):")
    print(sa)
    
    # Build LCP array using the suffix array
    # Note: For the LCP algorithm, we use the string with the added terminal '$'
    s_with_term = s + "$"
    lcp = build_lcp(s_with_term, [0] + sa)  # we add 0 to simulate the terminal suffix at position 0
    # Since our build_suffix_array removed the '$' suffix, we adjust by ignoring the first LCP value.
    print("\nLCP Array (lengths of common prefixes between adjacent suffixes):")
    print(lcp[1:])  # print from second element onward (optional adjustment)
    
    # For lexicographical comparison, we need the inverse suffix array
    n = len(s)
    inv = compute_inverse(sa, n)
    # Build Sparse Table for LCP array (using our computed lcp array without the extra terminal)
    # Here we build the table on the lcp array corresponding to suffixes in sa.
    # For simplicity, we compute the LCP array for s (without the terminal) using Kasai's algorithm.
    lcp2 = build_lcp(s, sa)
    if lcp2:
        st = SparseTable(lcp2)
    else:
        st = None

    # Check if extra parameters were provided for comparing two suffixes
    if len(data) >= 4 and st is not None:
        i = int(data[1])
        j = int(data[2])
        K = int(data[3])
        cmp_result = lcp_cmp(inv, st, i, j, K)
        comp_text = ("equal" if cmp_result == 0 
                     else "less than" if cmp_result < 0 
                     else "greater than")
        print(f"\nComparing suffixes starting at index {i} and {j} up to {K} characters:")
        print(f"Suffix at index {i} is {comp_text} the suffix at index {j} (lexicographically).")
    else:
        print("\nTo use the lexicographical comparison function, provide two indices and a value K as additional input.")

if __name__ == "__main__":
    main()
```

---

### What Does This Code Do?

1. **Suffix Array Construction**  
   The `build_suffix_array` function creates a list of starting indices of all the suffixes of a given string, sorted in lexicographical (dictionary) order. This is useful when you need to quickly locate or compare parts of a string.

2. **LCP Array Construction**  
   The `build_lcp` function computes the longest common prefix lengths between consecutive suffixes in the sorted suffix array. This information is often used in string search and matching problems.

3. **Sparse Table for RMQ**  
   The `SparseTable` class precomputes answers for range minimum queries on the LCP array. It allows quick queries to find the smallest LCP in any interval, which is needed for efficient lexicographical comparisons.

4. **Lexicographical Suffix Comparison**  
   The `lcp_cmp` function compares two suffixes (starting at indices i and j) by checking if they match for at least K characters. If they do, they’re considered equal up to K; otherwise, their order is determined based on their positions in the suffix array.

### When and How to Use This Code

- **When to use it:**  
  Use these routines when solving problems that involve string processing, such as pattern matching, substring search, or determining the lexicographical order of substrings. These techniques are common in competitive programming contests.

- **How to use it:**  
  - Input your string on the first line.
  - Optionally, on the second line, provide two indices (separated by space) representing the starting positions of suffixes you wish to compare.
  - On the third line, provide an integer K (number of characters to compare).
  - Run the script. It prints the suffix array and LCP array, and if additional parameters are provided, it also prints the result of the lexicographical comparison.

This script is written with clear comments and print statements so that even a beginner with zero coding experience can follow along and implement it in a competitive programming environment like CodeVita.