Below is one Python translation of the given C++ “line” (or segment) structure. In our version, we assume you already have a basic 2D point class (named here as `Point`) that supports arithmetic, dot product, cross product, rotation (by 90° counterclockwise), and magnitude–squared calculations. (See the short Point class below for reference.) 

In the translated code, the class `L` represents either an infinite line or a line segment. (Note that—as in the C++ code—it is not designed to handle “point segments” as input.) The methods perform operations such as converting from a line equation, computing which side of the line a point lies on, finding intersections between lines, testing whether segments intersect, and so on.

Below is the complete Python code with inline comments explaining each method:

---

```python
import math

EPS = 1e-9
INF = 10**18

# A simple 2D point class for use with our line routines.
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Vector addition
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    # Vector subtraction
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    # Scalar multiplication (from right or left)
    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)
    __rmul__ = __mul__

    # Scalar division
    def __truediv__(self, scalar):
        return Point(self.x / scalar, self.y / scalar)

    # Dot product (using the '*' operator for clarity)
    def dot(self, other):
        return self.x * other.x + self.y * other.y

    # Cross product (returns a scalar in 2D)
    def cross(self, other):
        return self.x * other.y - self.y * other.x

    # Returns the squared magnitude
    def magsq(self):
        return self.x * self.x + self.y * self.y

    # Rotate 90 degrees counterclockwise: (x,y) -> (-y,x)
    def rot(self):
        return Point(-self.y, self.x)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


# The line (or segment) class.
class L:
    def __init__(self, o, d):
        """
        Initializes a line (or segment) with origin o and direction d.
        For segments, the endpoints are taken to be o and o+d.
        """
        self.o = o  # Origin point
        self.d = d  # Direction vector

    @staticmethod
    def from_eq(ab, c):
        """
        Constructs a line from the equation: ab.rot() • x = c.
        In other words, given vector ab and constant c, returns the line
        with direction = ab.rot() and origin = ab * (-c / |ab|²).
        """
        return L(ab.rot(), ab * (-c / ab.magsq()))

    def line_eq(self):
        """
        Returns a tuple (A, B) representing the line equation A • x = B,
        where A is the normal vector (here, -d.rot()) and B = A.dot(o).
        """
        A = -self.d.rot()
        B = A.dot(self.o)
        return (A, B)

    def side(self, r):
        """
        Returns the signed value indicating the side of point r relative to the line.
        (Calculated as (r - o).cross(d))
          Negative value: r is to the left.
          Positive value: r is to the right.
        """
        return (r - self.o).cross(self.d)

    def inter(self, r):
        """
        Returns the intersection coefficient for the line r.
        (Computed as (r.o - o).cross(r.d))
        """
        return (r.o - self.o).cross(r.d)

    def intersection(self, r):
        """
        Returns the intersection point of this line with line r.
        Lines must not be parallel (i.e. d.cross(r.d) should not be 0).
        """
        denom = self.d.cross(r.d)
        if abs(denom) <= EPS:
            raise ValueError("Lines are parallel; no unique intersection.")
        t = self.inter(r) / denom
        return self.o + self.d * t

    def parallel(self, r):
        """
        Checks if this line is parallel to line r.
        """
        return abs(self.d.cross(r.d)) <= EPS

    def seg_collide(self, r):
        """
        Checks if the segments (self from o to o+d, and r from r.o to r.o+r.d) intersect.
        (Note: does not handle degenerate point segments correctly.)
        """
        z = self.d.cross(r.d)
        if abs(z) <= EPS:
            # Lines are collinear.
            if abs(self.side(r.o)) > EPS:
                return False
            # Compute the projections onto self.d.
            s = (r.o - self.o).dot(self.d)
            e = s + r.d.dot(self.d)
            if s > e:
                s, e = e, s
            return (s <= self.d.magsq() + EPS) and (e >= -EPS)
        # For non-collinear segments:
        s_val = self.inter(r)
        t_val = -r.inter(self)
        if z < 0:
            s_val, t_val, z = -s_val, -t_val, -z
        return (s_val >= -EPS and s_val <= z + EPS and
                t_val >= -EPS and t_val <= z + EPS)

    def seg_inter(self, r):
        """
        Computes the full segment intersection between two segments.
        If the intersection is a single point, returns a “point segment” (with zero direction).
        Returns a tuple (bool, result) where bool indicates if an intersection exists,
        and result is:
            - For collinear segments: a segment L representing the overlapping portion.
            - For non-collinear segments: a segment L whose origin is the intersection point
              and whose direction is Point(0, 0).
        Does not handle point segments as input.
        """
        z = self.d.cross(r.d)
        if abs(z) <= EPS:
            if abs(self.side(r.o)) > EPS:
                return (False, None)
            # Orient r so that its direction aligns with self.d.
            if r.d.dot(self.d) < 0:
                r = L(r.o + r.d, r.d * -1)
            # Choose the later starting point as the start of the intersection.
            s = r.o if self.o.dot(self.d) < r.o.dot(self.d) else self.o
            # Choose the earlier ending point.
            end1 = self.o + self.d
            end2 = r.o + r.d
            e = end1 if end1.dot(self.d) < end2.dot(self.d) else end2
            if s.dot(self.d) > e.dot(self.d) + EPS:
                return (False, None)
            return (True, L(s, e - s))
        s_val = self.inter(r)
        t_val = -r.inter(self)
        if z < 0:
            s_val, t_val, z = -s_val, -t_val, -z
        if (s_val >= -EPS and s_val <= z + EPS and
            t_val >= -EPS and t_val <= z + EPS):
            inter_pt = self.o + self.d * (s_val / z)
            return (True, L(inter_pt, Point(0, 0)))
        return (False, None)

    def point_on_seg(self, r):
        """
        Checks if point r lies on the segment (from o to o+d).
        """
        if abs(self.side(r)) > EPS:
            return False
        if (r - self.o).dot(self.d) < -EPS:
            return False
        # Check that r is not beyond the endpoint.
        if ((r - self.o) - self.d).dot(self.d) > EPS:
            return False
        return True

    def closest_to(self, r):
        """
        Returns the point on the infinite line that is closest to the given point r.
        (Computed using a rotated version of d.)
        """
        dr = self.d.rot()
        return r + dr * ((self.o - r).dot(dr)) / self.d.magsq()

    def __repr__(self):
        return f"L(o={self.o}, d={self.d})"
```

---

### Explanation

1. **from_eq:**  
   Constructs a line from a normal–form equation. Given a vector `ab` and constant `c`, it returns a line with direction `ab.rot()` and an origin calculated as  
   \[
   \text{origin} = ab \times \left(-\frac{c}{|ab|^2}\right).
   \]

2. **line_eq:**  
   Returns a tuple representing the line’s equation in the form \( A \cdot x = B \), where  
   \[
   A = -\text{d.rot()} \quad \text{and} \quad B = A \cdot o.
   \]

3. **side:**  
   Determines on which side of the line a point lies. It computes the cross product of \((r - o)\) with the direction \( d \).  
   (Negative means “left”; positive means “right”.)

4. **inter & intersection:**  
   The method `inter` computes a scalar coefficient (using a cross product) that is later used in `intersection` to compute the intersection point of two lines. (If the cross product of the direction vectors is zero, the lines are parallel.)

5. **parallel:**  
   Checks whether two lines are parallel by comparing the cross product of their direction vectors to EPS.

6. **seg_collide:**  
   Determines if two segments (from \( o \) to \( o+d \) and from \( r.o \) to \( r.o+r.d \)) collide.  
   For collinear segments it compares their projections onto \( d \); for non-collinear segments it uses the intersection coefficients.

7. **seg_inter:**  
   Computes the full intersection between two segments. In the collinear case, it returns the overlapping segment. In the non-collinear case, it returns a point (as a segment with zero direction).  
   (The function returns a tuple: a boolean indicating success and the intersection as an `L` object if found.)

8. **point_on_seg:**  
   Checks if a given point lies on the segment.

9. **closest_to:**  
   Returns the point on the infinite line closest to a given external point.

---

### How to Use

- **Integration with a Point Class:**  
  Ensure that you have a compatible `Point` class (as shown above) that supports addition, subtraction, multiplication, dot and cross products, and a `rot()` method.

- **Creating Lines and Segments:**  
  Create a line (or segment) by specifying its origin and direction. For example:
  ```python
  A = Point(0, 0)
  B = Point(5, 5)
  seg = L(A, B - A)  # A segment from (0,0) to (5,5)
  ```

- **Performing Operations:**  
  Use methods such as `intersection`, `seg_collide`, or `closest_to` to perform geometric queries. For example, to compute the intersection of two lines:
  ```python
  L1 = L(Point(0, 0), Point(1, 1))
  L2 = L(Point(0, 1), Point(1, -1))
  inter_pt = L1.intersection(L2)
  print("Intersection at:", inter_pt)
  ```

This Python code is designed for competitive programming settings (or similar applications) where robust geometric primitives are needed. Happy coding!