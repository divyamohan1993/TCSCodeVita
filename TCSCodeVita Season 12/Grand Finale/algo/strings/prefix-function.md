Below is the Python translation of the given C++ code. It includes:

1. **`prefix_function(s)`:**  
   Computes the prefix function (also called the "failure function") for the string `s`.  
   For every position \( i \), it finds the length of the longest proper prefix of \( s[0:i+1] \) that is also a suffix of that substring.

2. **`compute_automaton(s)`:**  
   First appends a sentinel character (`'#'`) to the string. Then it builds an automaton where for every state \( i \) (from \( 0 \) to \( n-1 \) in the augmented string) and for every letter from `'a'` to `'z'`, the automaton tells you what is the next state if that letter is read. This automaton is built using the prefix function, similarly to the standard KMP automaton construction.

3. **Minimal period comment:**  
   The minimal period \( k \) of a string \( s \) (before adding the sentinel) is given by  
   \[
   k = n - \text{pi}[n-1]
   \]
   If \( k \) divides \( n \) then the string can be partitioned into blocks of length \( k \); otherwise, there is no effective compression and the answer is \( n \).

---

```python
def prefix_function(s):
    """
    Computes the prefix function for string s.
    pi[i] is the length of the longest proper prefix of s[0:i+1]
    which is also a suffix of s[0:i+1].
    """
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi

def compute_automaton(s):
    """
    Computes the automaton for string s, used for fast pattern matching.
    The function returns a 2D list `aut` such that for each state i (0-indexed)
    and each character c (0 for 'a', 1 for 'b', ..., 25 for 'z'),
    aut[i][c] is the next state obtained by reading the character (chr(ord('a')+c)).
    
    Note: A sentinel character '#' is appended to s before computing the automaton.
    """
    s += '#'  # Append sentinel
    n = len(s)
    pi = prefix_function(s)
    aut = [[0] * 26 for _ in range(n)]
    
    for i in range(n):
        for c in range(26):
            j = i
            while j > 0 and chr(ord('a') + c) != s[j]:
                j = pi[j - 1]
            if chr(ord('a') + c) == s[j]:
                j += 1
            aut[i][c] = j
    return aut

# ---------------------------
# Example usage:
if __name__ == '__main__':
    s = "ababa"
    pi = prefix_function(s)
    print("Prefix function:", pi)
    
    # Compute the automaton for s (automaton built on s + '#')
    automaton = compute_automaton(s)
    print("Automaton (for each state, next state for a..z):")
    for state, transitions in enumerate(automaton):
        print(f"State {state}: {transitions}")
    
    # Minimal period example:
    # minimal period k = n - pi[n-1]
    n = len(s)
    k = n - pi[-1]
    if n % k == 0:
        print(f"The string can be partitioned into blocks of length {k}.")
    else:
        print(f"There is no effective compression; answer is {n}.")
```

---

### Explanation

1. **Prefix Function:**  
   - For a given string \( s \), `prefix_function(s)` computes an array `pi` where `pi[i]` is the maximum length \( l \) such that \( s[0:l] \) equals \( s[i-l+1:i+1] \).  
   - This is useful in pattern matching and automata construction.

2. **Automaton Construction:**  
   - The function `compute_automaton(s)` first appends a sentinel `'#'` to the string.  
   - Then for each state \( i \) (from \( 0 \) to \( n-1 \)) and each character from `'a'` to `'z'`, it finds the next state as follows:
     - Start with \( j = i \).  
     - While \( j > 0 \) and the current character does not match \( s[j] \), update \( j \) to \( \text{pi}[j-1] \).  
     - If a match is found, increment \( j \).  
     - Set the automaton’s transition \( \text{aut}[i][c] \) to \( j \).

3. **Minimal Period:**  
   - The minimal period \( k \) of a string is computed by \( k = n - \text{pi}[n-1] \).  
   - If \( k \) divides \( n \), the string is made up of blocks of length \( k \); otherwise, no effective compression is possible.

This Python translation captures the same logic as the C++ version using Python’s list operations and string handling. Happy coding!