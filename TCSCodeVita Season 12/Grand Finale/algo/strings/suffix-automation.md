Below is a complete Python script that implements the suffix automaton template from the provided C++ code. The code is designed so that even someone with no prior coding experience can follow along. It reads input from standard input (like in CodeVita), builds the suffix automaton for a given string, and then prints some basic information about the constructed automaton.

---

```python
import sys

# A class to represent a state (node) in the suffix automaton.
class State:
    def __init__(self, length=0, link=-1):
        # 'len' is the length of the longest string in this equivalence class.
        self.len = length
        # 'link' is the suffix link (points to the next smaller state).
        self.link = link
        # 'next' is a dictionary mapping characters to state indices.
        self.next = {}

# A class to build and store the suffix automaton.
class SuffixAutomaton:
    def __init__(self, s=""):
        # List of states. In a suffix automaton, number of states is at most 2*n - 1.
        self.st = []
        # 'sz' tracks the current number of states.
        self.sz = 0
        # 'last' stores the index of the state corresponding to the entire string so far.
        self.last = 0
        self.sa_init()  # initialize the automaton
        # If a string is provided, extend the automaton with each character.
        for c in s:
            self.sa_extend(c)
    
    def sa_init(self):
        """
        Initialize the suffix automaton.
        - Create the initial state (state 0) with length 0.
        - Set its link to -1 (meaning no suffix link).
        """
        self.st = [State()]  # create state 0
        self.st[0].len = 0
        self.st[0].link = -1
        self.sz = 1
        self.last = 0

    def sa_extend(self, c):
        """
        Extend the automaton by adding a new character 'c'.
        
        This function builds the automaton in O(n log alphabet_size) time.
        It does the following:
          1. Creates a new state for the new substring ending with 'c'.
          2. Propagates transitions from previous states that do not have 'c'.
          3. Fixes suffix links to maintain the automaton structure.
        
        Comments in the code explain each step.
        """
        # Create new state 'cur' with length = last state's length + 1.
        cur = self.sz
        self.st.append(State(self.st[self.last].len + 1))
        self.sz += 1
        
        p = self.last
        # Add transition for character 'c' for all states in the suffix chain
        while p != -1 and c not in self.st[p].next:
            self.st[p].next[c] = cur
            p = self.st[p].link
        
        if p == -1:
            # No state has a transition with 'c', so link new state to state 0.
            self.st[cur].link = 0
        else:
            q = self.st[p].next[c]
            if self.st[p].len + 1 == self.st[q].len:
                # The new state can be linked directly to state 'q'.
                self.st[cur].link = q
            else:
                # We need to create a clone of state 'q' to maintain correct lengths.
                clone = self.sz
                self.st.append(State(self.st[p].len + 1))
                self.sz += 1
                # Copy transitions from state 'q' to the clone.
                self.st[clone].next = self.st[q].next.copy()
                # Set the clone's link same as q's link.
                self.st[clone].link = self.st[q].link
                # Redirect transitions that pointed to q to point to the clone.
                while p != -1 and self.st[p].next.get(c) == q:
                    self.st[p].next[c] = clone
                    p = self.st[p].link
                # Update the suffix links of q and the current state.
                self.st[q].link = self.st[cur].link = clone
        # Update 'last' to the current state.
        self.last = cur

def main():
    """
    Main function:
      1. Reads input from standard input (expects a single string).
      2. Builds the suffix automaton for the input string.
      3. Prints the number of states and details for each state.
    
    Input format (example):
        banana
    """
    # Read input from stdin and strip any extra whitespace
    input_data = sys.stdin.read().strip()
    if not input_data:
        print("No input provided. Please enter a string.")
        return
    s = input_data.split()[0]  # consider first token as the string
    
    # Build the suffix automaton for the string s.
    automaton = SuffixAutomaton(s)
    
    # Print the total number of states built.
    print("Total number of states in the suffix automaton:", automaton.sz)
    print("\nState details:")
    print("State Index: [Length, Link, Transitions]")
    for idx, state in enumerate(automaton.st):
        print(f"{idx}: [len={state.len}, link={state.link}, next={state.next}]")
    
    # Extra info:
    print("\nNote:")
    print("Following the suffix links from the 'last' state to state 0 gives the terminal states (i.e., ending positions).")
    print("The number of different substrings in the original string can be calculated by summing (len - link_length) for each state.")

if __name__ == "__main__":
    main()
```

---

### What Does This Code Do?

1. **Suffix Automaton Construction**  
   - **States:** Each state represents a set of end positions of substrings.  
   - **Transitions:** The `next` dictionary in each state stores transitions for different characters.  
   - **Suffix Links:** The `link` of a state points to the next state that represents the longest proper suffix of the substring.
   
2. **Building Process**  
   - **Initialization (`sa_init`):** Sets up the initial state (state 0) with length 0 and no suffix link.
   - **Extension (`sa_extend`):** For every character in the input string, the automaton is extended. It adds a new state and adjusts transitions and suffix links to maintain the automaton's structure.
   - **Clone States:** When needed, the algorithm creates a clone state to ensure that all transitions remain consistent.

3. **Properties**  
   - The number of states is at most `2n - 1` for a string of length `n`.
   - It allows efficient queries regarding substrings and can be used to count the number of different substrings.

### When and How to Use This Code

- **When to use it:**  
  Use this code when solving string processing problems in competitive programming, such as finding all unique substrings, pattern matching, or solving problems that require efficient substring queries.

- **How to use it:**  
  1. **Input:**  
     - Provide a single string (e.g., `"banana"`) as input via standard input.
  2. **Execution:**  
     - The script builds the suffix automaton for the input string.
  3. **Output:**  
     - It prints the total number of states and detailed information for each state (length, suffix link, and transitions).

This implementation is ideal for a beginner: it is written in clear, commented Python code, and it explains each step so that even someone new to programming can follow along.