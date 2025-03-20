Below is a Python version of Manacher’s algorithm that computes two lists:

- **odd:** For each index in the original string, the length of the longest odd‐length palindrome centered at that character.
- **even:** For each “gap” between characters, the length of the longest even‐length palindrome centered there.

This version first builds a transformed string (with sentinels) so that every palindrome becomes “centered” at a character, then it computes the radius array and finally extracts the odd and even palindrome lengths.

---

```python
def manacher(s, odd, even):
    """
    Compute longest palindromic substring lengths in s:
      odd[i]:  length of the longest odd palindrome centered at i (in s)
      even[i]: length of the longest even palindrome centered between i and i+1 (in s)

    The function fills the provided lists `odd` and `even` with the results.
    
    This implementation uses a transformed string with sentinels:
      t = "$#" + (for each character: c + "#") + "^"
    so that every palindrome in s corresponds to a palindrome in t.
    """
    # Build transformed string.
    # For example, if s = "aba", then t becomes: "$#a#b#a#^"
    t = "$#" + "".join(c + "#" for c in s) + "^"
    n = len(t)
    
    # p[i] will store the radius (half-length) of the palindrome centered at t[i]
    p = [0] * n
    l, r = 1, 1  # Current palindrome boundaries (centered at some position in t)
    
    # Compute the palindrome radii using the Manacher algorithm.
    for i in range(1, n - 1):
        if i < r:
            # Mirror index for i with respect to current center.
            p[i] = min(r - i, p[l + r - i])
        else:
            p[i] = 0
        
        # Expand palindrome centered at i.
        while t[i - p[i]] == t[i + p[i]]:
            p[i] += 1
        
        # Update current palindrome boundaries if expanded past r.
        if i + p[i] > r:
            l = i - p[i]
            r = i + p[i]
    
    # Extract palindrome lengths for odd and even centers.
    # Note: In the transformed string, positions with even index correspond to characters of s,
    # and odd positions correspond to the "gaps" between characters.
    for i in range(2, n - 2):
        # p[i] counts how many characters (including sentinels) match on both sides.
        # We subtract one to get the effective length in the original string context.
        if i % 2:  # odd index in t corresponds to an even-length palindrome in s.
            even.append(p[i] - 1)
        else:      # even index in t corresponds to an odd-length palindrome in s.
            odd.append(p[i] - 1)

# ---------------------------
# Example usage:
if __name__ == '__main__':
    s = "abacaba"
    odd = []
    even = []
    manacher(s, odd, even)
    print("Original string:", s)
    print("Odd-length palindromes (centered at each character):", odd)
    print("Even-length palindromes (centered between characters):", even)
```

---

### Explanation

1. **Transformed String:**  
   We build a new string `t` by surrounding the original string with special characters. For example, for `s = "abacaba"`, we get:
   ```
   t = "$#a#b#a#c#a#b#a#^"
   ```
   This ensures every palindrome (even or odd length) has a center in `t`.

2. **Computing p Array:**  
   The list `p` holds the "radius" of the palindrome around each center in `t`. We use two pointers (`l` and `r`) to keep track of the rightmost palindrome currently known.  
   For each position `i` in `t`, we initialize `p[i]` using its mirror if possible, then expand as long as the characters at symmetric positions match.

3. **Extracting Results:**  
   After computing `p`, we loop over indices \(2 \leq i \leq n-3\) in `t` (skipping sentinels) and:
   - If `i` is even, the corresponding value (after subtracting 1) is the length of the longest odd-length palindrome centered at that character in `s`.
   - If `i` is odd, the value corresponds to the longest even-length palindrome centered between characters in `s`.

4. **How to Use:**  
   - Prepare empty lists `odd` and `even`.
   - Call `manacher(s, odd, even)` with your input string.
   - The lists `odd` and `even` are filled with the palindrome lengths.

This Python version closely mimics the provided C++ code and should help you understand how Manacher’s algorithm works in practice. Happy coding!