Below is a complete Python script that implements the convex hull computation (in counterclockwise order) using the monotone chain algorithm. This version excludes collinear points by default. For clarity, we define a simple `Point` class with attributes `x` and `y` and a helper function `cross` to compute the cross product of two vectors. The main function reads input from standard input (as in a Codevita environment), computes the convex hull, and prints the result.

---

```python
import sys

# ----------------------------
# Class: Point
# ----------------------------
# Represents a point in 2D space with x and y coordinates.
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # For sorting and printing purposes.
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)
    
    def __repr__(self):
        return f"({self.x}, {self.y})"

# ----------------------------
# Helper Function: cross
# ----------------------------
def cross(o, a, b):
    """
    Returns the cross product of vectors OA and OB.
    Positive if o->a->b makes a left turn, negative for right turn,
    and zero if the points are collinear.
    """
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

# ----------------------------
# Function: chull
# ----------------------------
def chull(points):
    """
    Computes the convex hull of a list of points in counterclockwise order.
    Excludes collinear points by default.
    
    Parameters:
      points (list of Point): The input list of points.
      
    Returns:
      list of Point: Points on the convex hull in counterclockwise order.
    """
    if len(points) < 3:
        return points[:]
    
    # Sort points by x coordinate, then by y coordinate.
    points.sort()
    
    # Build lower hull.
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) >= 0:
            lower.pop()
        lower.append(p)
    
    # Build upper hull.
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) >= 0:
            upper.pop()
        upper.append(p)
    
    # Remove the last point of each list (it's the same as the starting point of the other list).
    lower.pop()
    upper.pop()
    
    # Concatenate lower and upper hulls to get the full convex hull.
    return lower + upper

# ----------------------------
# Main: I/O and Demonstration
# ----------------------------
def main():
    """
    Reads input from standard input:
      First line: an integer n, the number of points.
      Next n lines: two space-separated numbers representing the x and y coordinates of each point.
    
    It then computes the convex hull and prints the points on the hull in counterclockwise order.
    
    Example Input:
        6
        0 0
        1 1
        2 2
        0 2
        2 0
        1 0
    Example Output (each point on a separate line):
        (0, 0)
        (2, 0)
        (2, 2)
        (0, 2)
    """
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n = int(data[0])
    points = []
    index = 1
    for _ in range(n):
        x = float(data[index])
        y = float(data[index + 1])
        index += 2
        points.append(Point(x, y))
    
    hull = chull(points)
    for p in hull:
        print(f"{p.x} {p.y}")

if __name__ == "__main__":
    main()
```

---

### Explanation

#### What It Does
- **Point Class:**  
  A simple class to represent points with x and y coordinates. It supports sorting based on x first then y.
  
- **Cross Product:**  
  The `cross(o, a, b)` function computes the cross product of vectors \( \overrightarrow{OA} \) and \( \overrightarrow{OB} \). This helps decide if three points make a left turn, right turn, or are collinear.

- **Convex Hull (`chull`):**  
  The function implements the monotone chain algorithm:
  - **Sorting:** The input points are first sorted by x and y.
  - **Lower Hull:** It iterates over points from left to right and keeps only those that maintain a left turn.
  - **Upper Hull:** It then iterates from right to left for the upper side.
  - **Combining:** The two hulls are concatenated (with duplicate endpoints removed) to form the complete convex hull.

#### When to Use It
- **Competitive Programming:**  
  Problems asking for the convex hull of a set of points can be solved using this algorithm.
- **Geometry Applications:**  
  Useful in tasks like collision detection, shape analysis, and more.

#### How to Use It
1. **Input Format:**  
   - First, provide the number of points.
   - Then, each subsequent line should have the x and y coordinates (separated by spaces) of each point.
2. **Execution:**  
   - Paste the code into your Python environment or online judge.
   - Run the code and provide the input via standard input.
3. **Output:**  
   - The script prints each point on the convex hull in counterclockwise order (each point printed as "x y").

This script is a complete, self-contained solution that should help even beginners understand and implement convex hull computation in Python.