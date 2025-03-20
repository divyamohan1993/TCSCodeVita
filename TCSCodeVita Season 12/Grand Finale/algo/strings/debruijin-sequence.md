Below is a Python translation of the C++ de Bruijn sequence generator using the FKM algorithm. This function generates a cyclic sequence (as a list of integers) over an alphabet \([0, k)\) of length \(k^n\) that contains every possible substring of length \(n\) exactly once.

---

```python
def de_bruijn_seq(k, n):
    """
    Generate a de Bruijn sequence for alphabet [0, k) and subsequences of length n.
    
    A de Bruijn sequence is a cyclic sequence of a given alphabet where every possible
    subsequence of length n appears exactly once.
    
    Parameters:
      k : int - size of the alphabet (elements 0 through k-1)
      n : int - length of the substrings
      
    Returns:
      A list of integers representing the de Bruijn sequence.
      
    Example:
      For k = 2 and n = 3, one possible de Bruijn sequence is [0, 0, 0, 1, 0, 1, 1, 1].
    """
    # Special case: if alphabet has only one symbol, return that symbol.
    if k == 1:
        return [0]
    
    seq = []            # List to store the sequence
    aux = [0] * (n + 1) # Auxiliary list for building Lyndon words

    def gen(t, p):
        """
        Recursive function that builds the de Bruijn sequence using the FKM algorithm.
        
        Parameters:
          t: current index in the auxiliary array
          p: current period (length of the current Lyndon word)
        """
        if t > n:
            # When we complete a Lyndon word of length p,
            # if n is divisible by p, add it to the sequence.
            if n % p == 0:
                # Append the Lyndon word (ignoring index 0)
                seq.extend(aux[1:p+1])
        else:
            # Set the current value to that from the position t-p
            aux[t] = aux[t - p]
            gen(t + 1, p)
            # Increment the current value until it reaches k-1
            for j in range(aux[t] + 1, k):
                aux[t] = j
                gen(t + 1, t)
    
    # Start the recursive generation process.
    gen(1, 1)
    return seq

# ---------------------------
# Example usage:
if __name__ == '__main__':
    k = 2
    n = 3
    seq = de_bruijn_seq(k, n)
    print("de Bruijn sequence for k =", k, "n =", n, "is:")
    print(seq)
    # For a cyclic sequence, you might also want to see the sequence wrapped around:
    print("Cyclic sequence (wrapped):")
    print(seq + seq[:n-1])
```

---

### What Does This Code Do?

1. **Purpose:**  
   - It constructs a de Bruijn sequence—a cyclic string that contains every possible substring of length \(n\) over the alphabet \([0, k)\) exactly once.
   
2. **How It Works:**  
   - **Base Case:** If \(k = 1\), the sequence is trivial (just `[0]`).
   - **Auxiliary Array:** An auxiliary list `aux` of length \(n+1\) is used to store the current sequence fragment.
   - **Recursive Function (`gen`):**  
     - The function builds Lyndon words (minimal cyclic strings) of length \(p\).
     - When \(t > n\), if \(n\) is a multiple of the current period \(p\), the word is appended to the final sequence.
     - Otherwise, it recursively builds the sequence by setting `aux[t]` to a value from a previous position and then trying larger values.
   
3. **When to Use It:**  
   - Use this function when you need to generate de Bruijn sequences, for example, in problems related to combinatorial generation, testing, or coding theory.
   
4. **How to Use It (for Beginners):**  
   - **Input:**  
     Call `de_bruijn_seq(k, n)` with your desired alphabet size \(k\) and substring length \(n\).
   - **Output:**  
     The function returns a list of integers representing the de Bruijn sequence.
   - **Example:**  
     Running the example with `k = 2` and `n = 3` produces a binary sequence of length \(2^3 = 8\) that contains every possible 3-bit binary number as a substring.

This Python code closely follows the logic of the C++ version while using Python's features such as recursion and list operations. Happy coding!