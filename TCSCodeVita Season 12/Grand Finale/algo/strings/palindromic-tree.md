Below is a Python translation of the EerTree (palindromic tree) implementation. This data structure efficiently stores all distinct palindromic substrings of a given string and counts their occurrences.

In this code:

- Each **Node** represents a palindrome. It stores:
  - **len**: length of the palindrome.
  - **to**: a list of 26 integers (one per lowercase letter) giving the child node index for an extension with that character.
  - **link**: suffix link (points to the longest proper palindromic suffix).
  - **i**: starting index (in the original string) where this palindrome occurs (optional).
  - **cnt**: the number of occurrences of this palindrome.

- **EerTree** (or palindromic tree) is built by processing the string character by character via the **add** method. After building the tree, counts are aggregated along the suffix links.

Below is the complete code with comments and an example usage:

---

```python
class Node:
    def __init__(self, length, link=0, i=0, cnt=1):
        """
        A Node in the palindromic tree.
        :param length: Length of the palindrome represented by this node.
        :param link: Suffix link (index of the longest proper palindromic suffix).
        :param i: Starting index of the palindrome in the original string (optional).
        :param cnt: Occurrence count (initially 1 when the palindrome is created).
        """
        self.len = length
        self.link = link
        self.i = i
        self.cnt = cnt
        # 'to' is a list of 26 integers (one for each letter 'a'-'z').
        # In our implementation, 0 means no transition.
        self.to = [0] * 26


class EerTree:
    def __init__(self, s):
        """
        Build a palindromic tree (EerTree) for string s.
        The tree will store all distinct palindromic substrings of s.
        """
        self.s = s
        self.t = []  # List of nodes (the tree). Maximum size is len(s)+2.
        # Create two root nodes:
        # Node 0: length = -1 (imaginary node), serves as a "guard".
        # Node 1: length = 0, represents the empty string.
        self.t.append(Node(-1, link=0, i=-1, cnt=0))  # root with len = -1
        self.t.append(Node(0, link=0, i=-1, cnt=0))    # root with len = 0
        self.last = 1  # Current node (start with empty string node)
        
        # Process each character in s
        for i in range(len(s)):
            self.add(i)
        
        # Propagate the occurrence counts along the suffix links.
        # Process nodes in reverse order (excluding the two roots).
        for i in range(len(self.t) - 1, 1, -1):
            self.t[self.t[i].link].cnt += self.t[i].cnt

    def add(self, i):
        """
        Add the character s[i] to the palindromic tree.
        """
        c = ord(self.s[i]) - ord('a')  # Map character to index 0..25
        p = self.last

        # Find the largest palindrome 'p' that can be extended with s[i]
        while True:
            # Check the character before the current palindrome
            if i - self.t[p].len - 1 >= 0 and self.s[i - self.t[p].len - 1] == self.s[i]:
                break
            p = self.t[p].link

        # If there is already an edge with character c from node p,
        # the palindrome already exists; update last and increase count.
        if self.t[p].to[c]:
            self.last = self.t[p].to[c]
            self.t[self.last].cnt += 1
            return

        # Otherwise, create a new node.
        # First, find the suffix link for the new node.
        q = self.t[p].link
        while True:
            if i - self.t[q].len - 1 >= 0 and self.s[i - self.t[q].len - 1] == self.s[i]:
                break
            q = self.t[q].link

        # t[q].to[c] might be zero if not created; in that case, we default to node 1.
        new_link = self.t[q].to[c] if self.t[q].to[c] else 1

        # Create new node with length = t[p].len + 2.
        self.last = len(self.t)
        new_node = Node(self.t[p].len + 2, link=new_link, i=i - self.t[p].len - 1, cnt=1)
        self.t.append(new_node)
        self.t[p].to[c] = self.last  # Set the edge from node p with letter c

# ---------------------------
# Example usage:
if __name__ == '__main__':
    s = "abcbab"
    pt = EerTree(s)
    
    # List all distinct palindromic substrings (skip nodes 0 and 1 which are roots)
    print("Distinct palindromes and their counts:")
    for node in pt.t[2:]:
        # The palindrome is s[node.i : node.i + node.len]
        substring = s[node.i: node.i + node.len]
        print(f"'{substring}' occurs {node.cnt} time(s)")
```

---

### Explanation

1. **Node Class:**  
   - Stores the length, suffix link, starting index, occurrence count, and transitions for each palindrome.

2. **EerTree Building:**  
   - Two root nodes are created: one for a “virtual” palindrome of length -1 and one for the empty string (length 0).
   - For each character in the string, the **add** method finds the longest palindrome that can be extended with that character. If the resulting palindrome does not exist yet, it creates a new node.
   - Finally, the occurrence counts are propagated along the suffix links.

3. **Example Usage:**  
   - The string `"abcbab"` is processed.
   - All distinct palindromic substrings (except the two roots) are printed along with their occurrence counts.

This Python implementation mirrors the original C++ code while using Python’s classes and list management. Happy coding!