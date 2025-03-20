
Below is one way to “translate” the C++ LineContainer into Python. In competitive programming this structure is used for the “convex‐hull trick” (or dynamic programming optimization) to maintain a set of lines of the form

  **f(x) = a·x + b**

so that you can quickly (in O(log N) time per operation) insert a new line and later query for the maximum value at any given x. (There is a “dual” version for finding minimum values.)  

The original C++ code uses a clever multiset with custom comparators and “mutable” members to keep track of intersection points between lines. In Python we can implement a similar idea using a data structure called a **LiChao Tree**. (A LiChao Tree is one popular way to implement a dynamic convex-hull trick.) It may be a bit easier to understand for a beginner since it uses a recursive segment‐tree style approach rather than tricky iterator manipulation.

Below is the full Python code with detailed comments. It reads from standard input (as in a CodeVita environment) and supports two types of operations:
 
- **Add a line:** with two integers `a` and `b` (representing the line *a·x + b*)
- **Query:** given an x, output the maximum value among all inserted lines at that x.

You can test the program by providing input such as:
 
```
5
1 2 3
1 -1 10
2 0
2 2
2 5
```

Here, the first line is the number of queries (5). Each subsequent line starts with an operation code:
 
- Code `1` means “add line” followed by `a b`
- Code `2` means “query” followed by an x value

---

```python
import sys

# We choose a range for x. In many contests x values are within a known bound.
# Here we assume queries satisfy: lo <= x <= hi.
lo_bound = -10**9
hi_bound = 10**9

class LiChaoTree:
    """
    A LiChaoTree dynamically stores lines (of form a*x + b) so that:
      - Insertion of a new line is O(log N)
      - Query for maximum value at any x is O(log N)
    """
    def __init__(self, lo=lo_bound, hi=hi_bound):
        self.lo = lo       # left bound of this segment
        self.hi = hi       # right bound of this segment
        self.mid = (lo + hi) // 2  # middle point
        self.line = None   # stored line, represented as a tuple (a, b)
        self.left = None   # left child (covering [lo, mid])
        self.right = None  # right child (covering [mid+1, hi])
    
    def eval_line(self, line, x):
        """Evaluate the line (a, b) at a given x."""
        a, b = line
        return a * x + b
    
    def add_line(self, new_line):
        """
        Insert a new line into the tree.
        The idea is to maintain at each segment the line that is best (gives maximum value)
        for some x in that segment.
        """
        lo, hi, mid = self.lo, self.hi, self.mid
        
        # If there is no line stored here yet, store new_line and return.
        if self.line is None:
            self.line = new_line
            return
        
        # At the mid point of the current segment, compare the new line with the current line.
        # If the new line gives a better value at mid, swap them.
        if self.eval_line(new_line, mid) > self.eval_line(self.line, mid):
            self.line, new_line = new_line, self.line

        # Now, decide whether to update the left or right segment.
        # If new_line is better at the left end, update the left child.
        if self.eval_line(new_line, lo) > self.eval_line(self.line, lo):
            if self.left is None:
                self.left = LiChaoTree(lo, mid)
            self.left.add_line(new_line)
        # Else if new_line is better at the right end, update the right child.
        elif self.eval_line(new_line, hi) > self.eval_line(self.line, hi):
            if self.right is None:
                self.right = LiChaoTree(mid+1, hi)
            self.right.add_line(new_line)
        # Otherwise, new_line does not improve the value at either end of the current segment,
        # so it is completely dominated and we do nothing.
    
    def query(self, x):
        """
        Return the maximum value among all stored lines at x.
        """
        # Start with the value of the line stored at this node (if any).
        res = self.eval_line(self.line, x) if self.line is not None else -float('inf')
        # Traverse to the left or right child depending on x.
        if x <= self.mid and self.left is not None:
            res = max(res, self.left.query(x))
        elif x > self.mid and self.right is not None:
            res = max(res, self.right.query(x))
        return res


def fast_input():
    """Read all input at once and split into tokens."""
    return sys.stdin.read().strip().split()


def main():
    tokens = fast_input()
    if not tokens:
        return
    
    # The first token is the number of queries Q.
    Q = int(tokens[0])
    index = 1

    # Create the LiChaoTree covering the x-range we expect.
    tree = LiChaoTree()
    
    output_lines = []
    for _ in range(Q):
        # Each query starts with a type indicator:
        # 1 => add a line; 2 => query maximum value at x.
        op = tokens[index]
        index += 1
        if op == '1':
            # "add line" operation: next two tokens are a and b.
            a = int(tokens[index])
            b = int(tokens[index + 1])
            index += 2
            tree.add_line((a, b))
        elif op == '2':
            # "query" operation: next token is x.
            x = int(tokens[index])
            index += 1
            result = tree.query(x)
            output_lines.append(str(result))
    
    # Print all query results.
    sys.stdout.write("\n".join(output_lines))


if __name__ == '__main__':
    main()
```

---

### What Does This Code Do?

1. **Purpose:**  
   It dynamically stores a set of linear functions (lines) of the form *a·x + b* so that later you can query “what is the maximum value among all these lines at a given x?” This technique is very useful when solving certain dynamic programming or optimization problems in competitive programming.

2. **How It Works:**  
   - **LiChaoTree Class:**  
     - The tree covers a given range of x-values (here, from –10⁹ to 10⁹).  
     - Each node of the tree stores one “best” line for that segment.  
     - The method `add_line(new_line)` inserts a new line by comparing values at the middle of the segment and recursively updating the left or right child if the new line improves the answer.
   - **Query:**  
     - The `query(x)` method traverses the tree to find the maximum value at the specific x by comparing the stored line at each node.

3. **When to Use It:**  
   - Use this structure when you have many lines (or linear functions) and you need to frequently ask “what is the best (maximum or minimum) value at this x?”  
   - It is especially useful in optimization problems and some dynamic programming challenges where you need to optimize a recurrence relation.

4. **How to Use It (for a Beginner):**  
   - **Input Format:**  
     - The program reads from standard input. The first number indicates the number of operations.
     - Each following operation is on a separate line.
       - For **adding a line**, write:  
         `1 a b`  
         (meaning add the line *a·x + b*).
       - For **querying**, write:  
         `2 x`  
         (meaning query for the maximum value at x).
   - **Running the Code:**  
     - Save the code in a file (for example, `solution.py`).
     - Run it in an environment that supports standard input. For instance, if you have a text file named `input.txt` with your test cases, run:
       ```
       python solution.py < input.txt
       ```
     - The program will output the result of each query, one per line.

This Python implementation provides the essential ideas behind the C++ LineContainer. As you practice, you may adjust the x-range, add more comments, or modify the input format to suit the specific problem you are trying to solve.

Happy coding!

```cpp
struct Line {
    mutable ll a, b, c;

    bool operator<(Line r) const { return a < r.a; }
    bool operator<(ll x) const { return c < x; }
};
// dynamically insert `a*x + b` lines and query for maximum
// at any x all operations have complexity O(log N)
struct LineContainer : multiset<Line, less<>> {
    ll div(ll a, ll b) {
        return a / b - ((a ^ b) < 0 && a % b);
    }

    bool isect(iterator x, iterator y) {
        if (y == end()) return x->c = INF, 0;
        if (x->a == y->a) x->c = x->b > y->b ? INF : -INF;
        else x->c = div(y->b - x->b, x->a - y->a);
        return x->c >= y->c;
    }

    void add(ll a, ll b) {
        // a *= -1, b *= -1 // for min
        auto z = insert({a, b, 0}), y = z++, x = y;
        while (isect(y, z)) z = erase(z);
        if (x != begin() && isect(--x, y)) isect(x, y = erase(y));
        while ((y = x) != begin() && (--x)->c >= y->c) isect(x, erase(y));
    }

    ll query(ll x) {
        if (empty()) return -INF; // INF for min
        auto l = *lower_bound(x);
        return l.a * x + l.b;
        // return -l.a * x - l.b; // for min
    }
};
```
