Below is a Python translation of the C++ double-hashing structure. This class precomputes two different hash arrays (with two mod values) and power arrays for a given string so that later you can obtain the hash of any substring in O(1) time. In the C++ version, the hash of a substring is computed as

  **h[j] – h[i] * p[j-i] mod MOD**

for each modulus. We do the same in Python.

---

```python
class Hash:
    # Two mod values and the base (P)
    MOD = [999727999, 1070777777]
    P = 1777771

    def __init__(self, s):
        """
        Precompute prefix hashes and power arrays for the given string s.
        The string is processed character by character (using ord() to get an integer).
        """
        self.n = len(s)
        # Initialize hash and power arrays for each mod
        self.h = [[0] * (self.n + 1) for _ in range(2)]
        self.p = [[1] * (self.n + 1) for _ in range(2)]
        
        for k in range(2):
            for i in range(1, self.n + 1):
                self.h[k][i] = (self.h[k][i-1] * Hash.P + ord(s[i-1])) % Hash.MOD[k]
                self.p[k][i] = (self.p[k][i-1] * Hash.P) % Hash.MOD[k]

    def get(self, i, j):
        """
        Return the hash values of the substring s[i:j] for both mod values.
        The hash is computed as:
           (h[j] - h[i] * p[j-i]) mod MOD
        """
        res = [0, 0]
        for k in range(2):
            res[k] = (self.h[k][j] - self.h[k][i] * self.p[k][j - i]) % Hash.MOD[k]
            # Ensuring a non-negative value (though Python's modulo already does)
            res[k] = (res[k] + Hash.MOD[k]) % Hash.MOD[k]
        return res

# ---------------------------
# Example usage:
if __name__ == '__main__':
    s = "abracadabra"
    hasher = Hash(s)
    # Get hash of substring "abra" (s[0:4])
    substring_hash = hasher.get(0, 4)
    print("Hash of 'abra':", substring_hash)
    
    # Get hash of substring "cad" (s[4:7])
    substring_hash2 = hasher.get(4, 7)
    print("Hash of 'cad':", substring_hash2)
```

---

### What Does This Code Do?

1. **Precomputation:**
   - The `__init__` method computes prefix hash arrays (`self.h`) and power arrays (`self.p`) for two different mod values.  
   - The hash at index `i` represents the hash of the prefix ending at `s[i-1]`.

2. **Substring Hashing:**
   - The `get(i, j)` method returns a list of two hash values (one per modulus) for the substring `s[i:j]`.
   - This uses the formula  
     \[
     \text{hash} = (h[j] - h[i] \times p[j-i]) \mod \text{MOD}
     \]
     ensuring that every substring’s hash can be computed in constant time.

3. **When to Use:**
   - Use this structure in problems that require comparing or quickly hashing substrings (such as in string matching or detecting duplicates).

4. **How to Use It (for Beginners):**
   - Create an instance of `Hash` with the string you wish to process.
   - Call the `get(i, j)` method with the starting index `i` and ending index `j` (with Python’s half-open interval semantics, where `j` is not included) to obtain the hash of that substring.
   - The returned list contains two hash values corresponding to the two mod values.

This Python implementation mimics the C++ structure while using Python’s list comprehensions and built-in arithmetic. Happy coding!