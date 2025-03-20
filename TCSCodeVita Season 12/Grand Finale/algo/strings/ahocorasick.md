Below is one way to “translate” the given C++ Aho–Corasick automaton code into Python. In this version, we define a class `Vertex` that stores all the information for each node (or vertex) in the trie. We then use a global list `t` to store all vertices. The functions below add patterns to the trie, compute suffix links (via `get_link`), compute automaton transitions (via `go`), and (optionally) compute exit links and count matches.

In Aho–Corasick, you build a trie of patterns and then compute for every node a suffix link (which points to the longest proper suffix that is also in the trie). This lets you quickly scan through a text and find all pattern occurrences.

Below is the Python code with detailed comments:

---

```python
class Vertex:
    def __init__(self, p=-1, pch='$'):
        # next: direct trie transitions (size 26 for 'a' to 'z')
        self.next = [-1] * 26
        # go: computed automata transitions
        self.go = [-1] * 26
        # p: parent vertex index
        self.p = p
        # link: suffix link (initialized to -1, computed on demand)
        self.link = -1
        # exit: exit link (points to next vertex which is a leaf)
        self.exit = -1
        # cnt: cached value for number of pattern matches ending here
        self.cnt = -1
        # leaf: list of pattern ids ending at this vertex
        self.leaf = []
        # pch: character on the edge from parent to this vertex
        self.pch = pch

# Global list of vertices (the trie); start with the root vertex.
t = [Vertex()]

def add(s, pattern_id):
    """
    Add a pattern string 's' to the trie, and associate it with pattern_id.
    """
    global t
    v = 0
    for ch in s:
        c = ord(ch) - ord('a')
        if t[v].next[c] == -1:
            t[v].next[c] = len(t)
            t.append(Vertex(p=v, pch=ch))
        v = t[v].next[c]
    t[v].leaf.append(pattern_id)

def get_link(v):
    """
    Compute and return the suffix link for vertex 'v'.
    The suffix link of the root and its direct children is 0.
    For other vertices, the link is computed recursively.
    """
    global t
    if t[v].link == -1:
        if v == 0 or t[v].p == 0:
            t[v].link = 0
        else:
            t[v].link = go(get_link(t[v].p), t[v].pch)
    return t[v].link

def go(v, ch):
    """
    Compute and return the automata transition from vertex 'v' with character 'ch'.
    If there is a direct trie transition, use it; otherwise, follow the suffix link.
    """
    global t
    c = ord(ch) - ord('a')
    if t[v].go[c] == -1:
        if t[v].next[c] != -1:
            t[v].go[c] = t[v].next[c]
        else:
            t[v].go[c] = 0 if v == 0 else go(get_link(v), ch)
    return t[v].go[c]

def next_match(v):
    """
    (Optional) Compute and return the exit link for vertex 'v'.
    The exit link points to the next vertex (via the suffix link chain)
    that corresponds to a pattern end (i.e. has non-empty leaf list).
    """
    global t
    if t[v].exit == -1:
        # Check if the suffix link of v has a pattern ending.
        if t[get_link(v)].leaf:
            t[v].exit = get_link(v)
        else:
            t[v].exit = 0 if v == 0 else next_match(get_link(v))
    return t[v].exit

def cnt_matches(v):
    """
    (Optional) Count the number of pattern matches that end at or before vertex 'v'.
    This function computes the total number of patterns ending in the chain of
    suffix links from v.
    """
    global t
    if t[v].cnt == -1:
        t[v].cnt = 0 if v == 0 else len(t[v].leaf) + cnt_matches(get_link(v))
    return t[v].cnt

# ---------------------------
# Example usage:
if __name__ == '__main__':
    # Add some patterns to the trie.
    patterns = ["he", "she", "his", "hers"]
    for idx, pat in enumerate(patterns):
        add(pat, idx)

    # To process a text, we would now simulate the automaton.
    text = "ahishers"
    state = 0
    for i, ch in enumerate(text):
        state = go(state, ch)
        # If there are patterns ending at this state, report them.
        if t[state].leaf:
            print(f"Pattern(s) found at index {i}: {t[state].leaf}")
        # Optionally, follow exit links to find additional matches.
        temp = next_match(state)
        while temp != 0:
            print(f"Additional pattern(s) found at index {i}: {t[temp].leaf}")
            temp = next_match(temp)
```

---

### What Does This Code Do?

1. **Building the Trie:**
   - The `Vertex` class holds transitions (`next`), computed transitions (`go`), suffix links (`link`), exit links (`exit`), and a list of pattern IDs (`leaf`) that end at that vertex.
   - The global list `t` starts with one root vertex.
   - The `add(s, pattern_id)` function inserts a pattern string into the trie and marks its ending vertex with the pattern's identifier.

2. **Computing Suffix and Automata Transitions:**
   - The `get_link(v)` function computes the suffix link for a given vertex recursively. For the root or its direct children, the suffix link is the root (0). Otherwise, it is computed using the parent's suffix link and the character from the parent to this vertex.
   - The `go(v, ch)` function computes the next state when reading character `ch` from vertex `v`. If there is no direct edge, it follows the suffix link.

3. **Optional Functions for Matching:**
   - `next_match(v)` computes an exit link, which helps in finding additional pattern matches (if patterns share common suffixes).
   - `cnt_matches(v)` computes the total number of patterns that end at or in the chain of suffix links from `v`.

4. **When to Use:**
   - This automaton is useful in problems that require searching for multiple patterns simultaneously (like in text matching).
   - Once the trie is built and the links are computed on the fly, you can process any text in O(length of text) time to find all pattern occurrences.

5. **How to Use (for Beginners):**
   - **Adding Patterns:**  
     Call `add(pattern, id)` for every pattern you need to search.
   - **Processing a Text:**  
     Loop over the text, updating the automaton state using `go(state, ch)`. At each position, check `t[state].leaf` (and optionally `next_match(state)`) to see if any patterns end at that state.
   - **Modifications:**  
     Adapt the example usage to suit your problem's input format and output requirements.

This Python code captures the structure and behavior of the original C++ Aho–Corasick implementation while using Python’s classes and lists. Happy coding!