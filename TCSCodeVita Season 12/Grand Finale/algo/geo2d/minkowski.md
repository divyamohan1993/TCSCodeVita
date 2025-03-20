Below is the Python translation of the two functions. In this code, we assume that you have a 2D Point class that supports addition, subtraction, and a cross–product method (here defined as `cross`). The first function, `reorder_polygon`, rotates the vertices so that the vertex with the lowest y–coordinate (and lowest x–coordinate in case of ties) comes first. The second function, `minkowski`, computes the Minkowski sum of two convex polygons (given as lists of points in counterclockwise order).

Below the code is an explanation of what each function does and how to use them.

---

```python
import math

EPS = 1e-9

# A simple 2D Point class for our purposes.
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Addition of two points.
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    # Subtraction of two points.
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    # Scalar multiplication.
    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    __rmul__ = __mul__

    # Returns the cross product of self and other (2D cross product).
    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


def reorder_polygon(ps):
    """
    Rotates the list of points 'ps' so that the vertex with the lowest y coordinate,
    and lowest x coordinate in case of tie, comes first.
    Returns the rotated list.
    """
    if not ps:
        return ps
    pos = 0
    for i in range(1, len(ps)):
        # Compare by y, then by x (using EPS to avoid precision issues)
        if (ps[i].y < ps[pos].y - EPS) or (abs(ps[i].y - ps[pos].y) < EPS and ps[i].x < ps[pos].x - EPS):
            pos = i
    # Rotate the polygon so that ps[pos] becomes the first element.
    return ps[pos:] + ps[:pos]


def minkowski(ps, qs):
    """
    Computes the Minkowski sum of two convex polygons ps and qs.
    Both ps and qs must be given in counterclockwise order.
    The function assumes that each polygon's first vertex is the lowest.
    
    Returns a list of points representing the Minkowski sum polygon.
    """
    # Ensure the first vertex is the lowest for each polygon.
    ps = reorder_polygon(ps)
    qs = reorder_polygon(qs)
    
    # Append first two points at the end to allow easy wrap-around.
    ps_extended = ps + [ps[0], ps[1]]
    qs_extended = qs + [qs[0], qs[1]]
    
    result = []
    i = j = 0
    # Process until both polygons have been completely traversed.
    while i < len(ps_extended) - 2 or j < len(qs_extended) - 2:
        # Add the sum of current vertices.
        result.append(ps_extended[i] + qs_extended[j])
        # Compute cross product between the current edges.
        edge_ps = ps_extended[i+1] - ps_extended[i]
        edge_qs = qs_extended[j+1] - qs_extended[j]
        z = edge_ps.cross(edge_qs)
        # Advance in polygon ps if the turn is not "right" (≥0)
        if z >= -EPS and i < len(ps_extended) - 2:
            i += 1
        # Advance in polygon qs if the turn is not "left" (≤0)
        if z <= EPS and j < len(qs_extended) - 2:
            j += 1
    return result


# ----------------------------
# Example usage
# ----------------------------
if __name__ == "__main__":
    # Define two convex polygons (in counterclockwise order)
    poly1 = [Point(0, 0), Point(2, 0), Point(1, 1)]
    poly2 = [Point(0, 0), Point(1, 0), Point(0, 1)]
    
    # Compute their Minkowski sum.
    mink_sum = minkowski(poly1, poly2)
    
    # Print the resulting polygon vertices.
    print("Minkowski Sum Polygon:")
    for p in mink_sum:
        print(p)
```

---

### Explanation

1. **`reorder_polygon(ps)` Function:**  
   - **What It Does:**  
     It scans the list of points to find the vertex with the lowest y–coordinate (using x as a tiebreaker) and then rotates the list so that this vertex becomes the first.
   - **When to Use It:**  
     Before computing operations that assume a canonical ordering (such as Minkowski sums), you must reorder the vertices.
   - **How to Use It:**  
     Pass a list of points (in any order) to get a new list with the lowest vertex first.

2. **`minkowski(ps, qs)` Function:**  
   - **What It Does:**  
     It computes the Minkowski sum of two convex polygons. The sum is obtained by "adding" every point of polygon A with every point of polygon B in a way that preserves the counterclockwise order. The algorithm uses a two–pointer technique based on the cross product of the edges.
   - **When to Use It:**  
     Use this when you need to compute the Minkowski sum, such as in collision detection, robot motion planning, or optimization problems.
   - **How to Use It:**  
     Provide two convex polygons (lists of `Point` objects in counterclockwise order). The function returns a new polygon (also a list of `Point` objects) representing their Minkowski sum.

This complete Python code can be directly integrated into your projects or competitive programming solutions. Enjoy coding!