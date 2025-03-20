Below is the equivalent Python code for the given persistent segment tree without lazy propagation. This implementation is generic and uses nodes that store an aggregate value (here, a sum) along with indices to the left and right children. At the end, you'll also find an explanation of what the algorithm is used for and when to use it.

---

### Python Code

```python
class Node:
    def __init__(self, x=0, l=-1, r=-1):
        self.x = x      # Aggregate value stored at this node.
        self.l = l      # Index of the left child in the node list.
        self.r = r      # Index of the right child in the node list.

    @classmethod
    def merge(cls, left_node, right_node, l=-1, r=-1):
        """
        Merge two nodes by adding their aggregate values.
        The merged node's left and right children are set to l and r.
        """
        return cls(left_node.x + right_node.x, l, r)

    def __repr__(self):
        return f"Node(x={self.x}, l={self.l}, r={self.r})"


class Pst:
    def __init__(self, N):
        """
        Initialize the persistent segment tree for an array of size N.
        It builds the initial tree (version 0) and stores its root index.
        """
        self.N = N
        self.a = []       # List to store all nodes across all versions.
        self.head = []    # List of root indices for each version.
        self.head.append(self.build(0, N))

    def build(self, vl, vr):
        """
        Recursively build the segment tree for the interval [vl, vr).
        Returns the index of the created node.
        """
        if vr - vl == 1:
            # Leaf node: use the default Node (which stores 0).
            self.a.append(Node())
        else:
            vm = (vl + vr) // 2
            left_index = self.build(vl, vm)
            right_index = self.build(vm, vr)
            merged_node = Node.merge(self.a[left_index], self.a[right_index],
                                     left_index, right_index)
            self.a.append(merged_node)
        return len(self.a) - 1

    def query_rec(self, l, r, v, vl, vr):
        """
        Recursively answer the query on the interval [l, r) using the version
        whose root is at index v, which covers the interval [vl, vr).
        """
        if l >= vr or r <= vl:
            # No overlap; return the neutral element.
            return Node()
        if l <= vl and vr <= r:
            # Total overlap; return this node.
            return self.a[v]
        vm = (vl + vr) // 2
        left_res = self.query_rec(l, r, self.a[v].l, vl, vm)
        right_res = self.query_rec(l, r, self.a[v].r, vm, vr)
        return Node.merge(left_res, right_res)

    def query(self, t, l, r):
        """
        Public query function.
        For version t, returns the aggregate (sum) on the interval [l, r).
        """
        return self.query_rec(l, r, self.head[t], 0, self.N)

    def update_rec(self, i, new_node, v, vl, vr):
        """
        Recursively update the tree by replacing the leaf at index i with new_node,
        starting from node index v covering interval [vl, vr). This function creates
        new copies of nodes along the path (persistence) and returns the new node index.
        """
        # Make a new copy of node v.
        self.a.append(self.a[v])
        new_v = len(self.a) - 1
        if vr - vl == 1:
            # Leaf: update with new_node.
            self.a[new_v] = new_node
        else:
            vm = (vl + vr) // 2
            if i < vm:
                self.a[new_v].l = self.update_rec(i, new_node, self.a[new_v].l, vl, vm)
            else:
                self.a[new_v].r = self.update_rec(i, new_node, self.a[new_v].r, vm, vr)
            # After updating a child, merge the children to update the current node.
            self.a[new_v] = Node.merge(self.a[self.a[new_v].l], self.a[self.a[new_v].r],
                                        self.a[new_v].l, self.a[new_v].r)
        return new_v

    def update(self, t, i, new_node):
        """
        Public update function.
        Starting from version t, update index i with new_node.
        Returns the version number (index in self.head) of the new version.
        
        Usage example:
          new_version = pst.update(time, index, Node(new_value))
        """
        new_root = self.update_rec(i, new_node, self.head[t], 0, self.N)
        self.head.append(new_root)
        return len(self.head) - 1
```

---

### Explanation

#### **What the Code Does:**

- **Persistent Segment Tree:**  
  This data structure creates a new version of the segment tree with every update while sharing most of the unchanged nodes between versions. It is called *persistent* because it retains all historical versions.

- **Node Structure:**  
  Each node stores an aggregate value (here, the sum of a segment) and indices to its left and right children. The merge function combines two child nodes by summing their aggregate values.

- **Build Function:**  
  The tree is built recursively over an interval. Leaf nodes are initialized with the neutral element (0 for sum), and internal nodes are built by merging their children.

- **Query Function:**  
  Queries on a specific version are answered recursively. If the query range fully covers a node's segment, that node is returned; otherwise, results from the left and right children are merged.

- **Update Function:**  
  When updating a value, a new copy is made along the path from the root to the target leaf, ensuring previous versions remain unchanged. This "persistent" update creates a new version with the updated value.

#### **When to Use This Algorithm:**

- **Versioned Data Access:**  
  When you need to maintain and query historical versions of an array or dataset. This is common in scenarios such as undo functionality, time-travel queries, or functional programming.

- **Range Queries:**  
  It efficiently supports range queries (like sum, minimum, or maximum) on static or updated arrays.

- **Competitive Programming:**  
  Problems that require multiple updates and queries on historical data benefit from persistence. The persistent segment tree allows you to answer queries on any version of the data in logarithmic time.

- **Memory Efficiency with Immutability:**  
  Although each update creates a new version, the shared structure means that the memory overhead is minimized compared to rebuilding the entire tree for each update.

---

### Usage Example

```python
# Initialize a persistent segment tree for an array of size N.
N = 10
pst = Pst(N)

# Suppose we want to update the value at index 3 to 5 in version 0.
new_version = pst.update(0, 3, Node(5))

# Query the sum in the range [2, 6) on the new version.
result_node = pst.query(new_version, 2, 6)
print("Queried sum:", result_node.x)
```

This code snippet shows how you can create an initial persistent segment tree, update a value in a specific version, and then query a range on the updated version.

---

This persistent segment tree is a powerful tool when you need to perform efficient range queries and updates on data that maintains historical versions, allowing you to "time travel" and query previous states without losing the current state.