import random

class Item:
    def __init__(self, k):
        self.k = k                   # The key
        self.p = random.randrange(1 << 30)  # Random priority (to allow duplicates, you can mix key with priority)
        self.n = 1                   # Subtree size (number of nodes in this subtree)
        self.l = None                # Left child
        self.r = None                # Right child

    def __repr__(self):
        return f"Item(k={self.k}, p={self.p}, n={self.n})"

def getn(x):
    """Return the size of the subtree rooted at x."""
    return x.n if x else 0

def recalc(x):
    """Recalculate the subtree size of node x based on its children."""
    if x:
        x.n = getn(x.l) + 1 + getn(x.r)

def split(x, k):
    """
    Splits the treap rooted at x into two treaps:
      - l: all nodes with key <= k (if duplicate keys should go one way, adjust the inequality)
      - r: all nodes with key > k
    Returns a tuple (l, r).
    """
    if not x:
        return (None, None)
    if k < x.k:
        # The key to split by is less than the current node's key.
        l, x.l = split(x.l, k)
        recalc(x)
        return (l, x)
    else:
        # k is greater than or equal to x.k
        x.r, r = split(x.r, k)
        recalc(x)
        return (x, r)

def merge(l, r):
    """
    Merges two treaps l and r into one treap.
    All keys in l must be less than or equal to those in r.
    """
    if not l or not r:
        return l if l else r
    if l.p > r.p:
        l.r = merge(l.r, r)
        recalc(l)
        return l
    else:
        r.l = merge(l, r.l)
        recalc(r)
        return r

def insert(x, y):
    """
    Inserts node y into the treap rooted at x and returns the new root.
    """
    if not x:
        return y
    if y.p > x.p:
        y.l, y.r = split(x, y.k)
        recalc(y)
        return y
    else:
        if y.k < x.k:
            x.l = insert(x.l, y)
        else:
            x.r = insert(x.r, y)
        recalc(x)
        return x

def erase(x, k):
    """
    Erases one occurrence of the key k from the treap rooted at x and returns the new root.
    """
    if not x:
        return None
    if x.k == k:
        # Merge the left and right subtrees, effectively removing x.
        return merge(x.l, x.r)
    elif k < x.k:
        x.l = erase(x.l, k)
    else:
        x.r = erase(x.r, k)
    recalc(x)
    return x

# Example usage:
if __name__ == '__main__':
    # Create an empty treap (None represents an empty treap)
    root = None
    
    # Insert some keys
    for key in [5, 3, 8, 1, 4, 7, 9]:
        root = insert(root, Item(key))
    
    # Print the treap's root (the entire treap is stored in this tree structure)
    print("Treap after insertions:", root)
    
    # Erase a key (for example, key 4)
    root = erase(root, 4)
    print("Treap after erasing key 4:", root)
    
    # To demonstrate splitting:
    left, right = split(root, 5)
    print("Treap after splitting by key 5:")
    print("Left treap:", left)
    print("Right treap:", right)
