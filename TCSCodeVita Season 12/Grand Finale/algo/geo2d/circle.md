Below is a complete Python script that “translates” the given C++ competitive‐programming templates into Python. It defines three classes:

- **Point:** A 2D point (or vector) with common operations (addition, subtraction, scaling, dot product, cross product, rotation by 90° etc.).
- **Line:** A line defined by a point (its “origin”) and a direction vector.
- **Circle:** A circle (with center and radius) along with many methods that compute intersections with lines or other circles, tangents, circumcircles of triangles, and even the area of intersection with a triangle.

A beginner can run this code in a Codevita‐like environment (reading from standard input) and choose an operation by specifying an operation code and the needed parameters.

Below the code you’ll find an explanation of what each part does, when you might use these functions, and how to use the code.

---

```python
import sys
import math

# A small epsilon to deal with floating‐point comparisons
EPS = 1e-9

# ----------------------------
# Class: Point
# ----------------------------
# Represents a point in 2D space. Also used for vector arithmetic.
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Addition of two points/vectors
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    # Subtraction of two points/vectors
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    # Multiplication by a scalar
    def __mul__(self, value):
        return Point(self.x * value, self.y * value)

    # Right multiplication supports scalar * Point
    def __rmul__(self, value):
        return self.__mul__(value)

    # Division by a scalar
    def __truediv__(self, value):
        return Point(self.x / value, self.y / value)

    # Returns the square of the magnitude (length) of the vector
    def magsq(self):
        return self.x * self.x + self.y * self.y

    # Returns the magnitude (length) of the vector
    def mag(self):
        return math.sqrt(self.magsq())

    # Another name for magnitude
    def norm(self):
        return self.mag()

    # Returns the unit (normalized) vector
    def unit(self):
        m = self.mag()
        if m < EPS:
            return Point(0, 0)
        return self / m

    # Dot product of two vectors
    def dot(self, other):
        return self.x * other.x + self.y * other.y

    # Cross product (in 2D, returns a scalar)
    def cross(self, other):
        return self.x * other.y - self.y * other.x

    # Rotate the point by 90 degrees counterclockwise: (x, y) -> (-y, x)
    def rot(self):
        return Point(-self.y, self.x)

    # Returns the angle (in radians) between self and another vector
    def angle(self, other):
        dot_val = self.dot(other)
        mags = self.mag() * other.mag()
        if mags < EPS:
            return 0
        # Clamp value between -1 and 1 to avoid precision issues.
        cos_theta = max(min(dot_val / mags, 1), -1)
        return math.acos(cos_theta)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

# ----------------------------
# Class: Line
# ----------------------------
# Represents a line in 2D. A line is defined by an origin point and a direction vector.
class Line:
    def __init__(self, o, d):
        self.o = o  # A point on the line
        self.d = d  # Direction vector (need not be unit)

    # Finds the point on the line that is closest to point p.
    def closest_to(self, p):
        # Projection formula: o + d * ((p - o)·d / |d|²)
        t = (p - self.o).dot(self.d) / self.d.magsq()
        return self.o + self.d * t

    # Returns the unit vector of the line's direction.
    def unit_direction(self):
        return self.d.unit()

    def __repr__(self):
        return f"Line(origin={self.o}, direction={self.d})"

# ----------------------------
# Class: Circle
# ----------------------------
# Represents a circle with center (o) and radius (r).
# Contains methods for various geometric operations.
class Circle:
    def __init__(self, o, r):
        self.o = o  # Center of the circle (a Point)
        self.r = r  # Radius of the circle (a float)

    # 1. Intersection between a circle and a line.
    def line_inter(self, l):
        """
        Computes the intersection points between the circle and a line 'l'.
        Assumes the line does intersect the circle.
        Returns a tuple (point1, point2) sorted along the direction of the line.
        """
        c = l.closest_to(self.o)
        c2 = (c - self.o).magsq()
        factor = math.sqrt(max(self.r * self.r - c2, 0) / l.d.magsq())
        e = l.d * factor
        return (c - e, c + e)

    # 2. Determines the type of collision between a line and the circle.
    def line_collide(self, l):
        """
        Returns:
          < 0 : two intersection points (line cuts the circle),
          = 0 : one intersection point (line is tangent),
          > 0 : no intersection.
        It computes (distance from center to line)² - r².
        """
        c = l.closest_to(self.o)
        c2 = (c - self.o).magsq()
        return c2 - self.r * self.r

    # 3. Intersection between two circles.
    def inter(self, h):
        """
        Computes the intersection points between this circle and another circle 'h'.
        Assumes the circles intersect in one or two points.
        """
        d = h.o - self.o
        c_val = (self.r * self.r - h.r * h.r) / d.magsq()
        new_origin = ((1 + c_val) / 2) * d
        line = Line(new_origin, d.rot())
        return h.line_inter(line)

    # 4. Check if two circles collide (touch or intersect).
    def collide(self, h):
        """
        Returns True if this circle and circle 'h' intersect or touch.
        """
        return (h.o - self.o).magsq() <= (h.r + self.r) * (h.r + self.r)

    # 5. Get one of the two tangents from a point to the circle.
    def point_tangent(self, p, a):
        """
        Given an external point 'p' and a parameter 'a' (-1 for clockwise,
        1 for counterclockwise), returns the point of tangency on the circle.
        """
        c_val = self.r * self.r / p.magsq()
        return self.o + c_val * (p - self.o) - a * math.sqrt(c_val * (1 - c_val)) * (p - self.o).rot()

    # 6. Get one of the four tangents between two circles.
    def tangent(self, c_circle, a, b):
        """
        Returns a line representing one of the tangents between this circle and another circle 'c_circle'.
        Parameters:
          a = 1 for exterior tangents, a = -1 for interior tangents.
          b = 1 for counterclockwise tangent, b = -1 for clockwise tangent.
        The returned Line's origin is on the circle's circumference and its direction is a unit vector.
        """
        dr = a * self.r - c_circle.r
        d = c_circle.o - self.o
        n = (d * dr + b * d.rot() * math.sqrt(max(d.magsq() - dr * dr, 0))).unit()
        return Line(self.o + n * self.r, -b * n.rot())

    # 7. Construct the circumcircle (circle through three points).
    @staticmethod
    def thru_points(a, b, c):
        """
        Given three non-collinear points a, b, c, computes the unique circle that passes through them.
        """
        b_vec = b - a
        c_vec = c - a
        numerator = (b_vec * c_vec.magsq() - c_vec * b_vec.magsq()).rot()
        denominator = 2 * b_vec.cross(c_vec)
        p = numerator / denominator
        center = a + p
        return Circle(center, p.mag())

    # 8. Find the two circles that go through a given point and are tangent to a given line.
    @staticmethod
    def thru_point_line_r(a, t, r):
        """
        Given a point 'a', a line 't', and a radius 'r' (with the point-line distance ≤ r),
        returns two circles (as a tuple) that go through 'a' and are tangent to 't'.
        The two circles are sorted along the direction of the line.
        """
        d = t.d.rot().unit()
        if d.dot(a - t.o) < 0:
            d = d * -1
        temp_circle = Circle(a, r)
        inter_line = Line(t.o + d * r, t.d)
        p1, p2 = temp_circle.line_inter(inter_line)
        return (Circle(p1, r), Circle(p2, r))

    # 9. Find the two circles that go through two given points and have a fixed radius.
    @staticmethod
    def thru_points_r(a, b, r):
        """
        Given two points 'a' and 'b' (which must be at most 2*r apart) and a radius 'r',
        returns two circles that pass through both points.
        """
        mid = (a + b) * 0.5
        inter_line = Line(mid, (b - a).rot())
        p1, p2 = Circle(a, r).line_inter(inter_line)
        return (Circle(p1, r), Circle(p2, r))

    # 10. Find intersection points between a circle and a line.
    def linecol(self, l):
        """
        Returns a list of intersection points between the circle and line 'l'.
        The list will be empty (no intersection), contain one point (tangent), or two points.
        """
        points = []
        p = l.closest_to(self.o)
        d = (p - self.o).mag()
        if d - self.r > EPS:
            return points
        if abs(d - self.r) <= EPS:
            points.append(p)
            return points
        diff = math.sqrt(self.r * self.r - d * d)
        points.append(p + l.unit_direction() * diff)
        points.append(p - l.unit_direction() * diff)
        return points

    # Helper: Check if a point is inside or on the circle.
    def has(self, p):
        return (p - self.o).magsq() <= self.r * self.r + EPS

    # 11. Compute the area of intersection between the circle and a triangle formed by the circle's center and two points.
    def intertriangle(self, a, b):
        """
        Computes the area of the intersection between the circle and the triangle with vertices: circle center, a, and b.
        This is useful when you want to know how much of a triangle (or sector) is inside the circle.
        """
        if abs((self.o - a).cross(self.o - b)) <= EPS:
            return 0.0
        q = [a]
        # Get intersection points of the edge from a towards b
        w = self.linecol(Line(a, b - a))
        if len(w) == 2:
            for p in w:
                if (a - p).dot(b - p) < -EPS:
                    q.append(p)
        q.append(b)
        if len(q) == 4 and (q[0] - q[1]).dot(q[2] - q[1]) > EPS:
            q[1], q[2] = q[2], q[1]
        s = 0.0
        for i in range(len(q) - 1):
            if not self.has(q[i]) or not self.has(q[i + 1]):
                angle = (q[i] - self.o).angle(q[i + 1] - self.o)
                s += self.r * self.r * angle / 2.0
            else:
                s += abs((q[i] - self.o).cross(q[i + 1] - self.o) / 2.0)
        return s

    def __repr__(self):
        return f"Circle(center={self.o}, radius={self.r})"

# ----------------------------
# Main: Demonstration & I/O
# ----------------------------
# This main function is set up for a Codevita-like environment.
# The first number in the input indicates the number of test cases.
# Each test case starts with an operation code (an integer from 1 to 11) that selects which function to run.
#
# The operations are as follows:
# 1. Circle-line intersection:
#      Input: cx cy r lx ly dx dy
#      (Circle center, radius, line origin, line direction)
# 2. Line-circle collision test:
#      Same input as (1). Prints (distance from center to line)² - r².
# 3. Intersection points of two circles:
#      Input: c1x c1y r1 c2x c2y r2
# 4. Check if two circles collide:
#      Same input as (3); prints "YES" or "NO".
# 5. Point tangent:
#      Input: cx cy r px py a
#      (Finds the tangent point from point (px,py) to the circle;
#       a = -1 for clockwise, a = 1 for counterclockwise.)
# 6. Tangent between two circles:
#      Input: c1x c1y r1 c2x c2y r2 a b
# 7. Circumcircle of three points:
#      Input: ax ay bx by cx cy
# 8. Two circles through a point and tangent to a line:
#      Input: ax ay lx ly dx dy r
# 9. Two circles through two points with radius:
#      Input: ax ay bx by r
# 10. Intersection points (linecol) between circle and line:
#       Input: cx cy r lx ly dx dy
# 11. Intersection area between circle and triangle (center, a, b):
#       Input: cx cy r ax ay bx by
#
# Each test case prints its result to standard output.
def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    t = int(data[0])
    index = 1
    for _ in range(t):
        op = int(data[index])
        index += 1
        if op == 1:
            # Circle-line intersection
            cx = float(data[index]); cy = float(data[index+1]); r = float(data[index+2])
            lx = float(data[index+3]); ly = float(data[index+4]); dx = float(data[index+5]); dy = float(data[index+6])
            index += 7
            circle = Circle(Point(cx, cy), r)
            line = Line(Point(lx, ly), Point(dx, dy))
            p1, p2 = circle.line_inter(line)
            print(f"{p1.x:.6f} {p1.y:.6f} {p2.x:.6f} {p2.y:.6f}")
        elif op == 2:
            # Line-circle collision type test
            cx = float(data[index]); cy = float(data[index+1]); r = float(data[index+2])
            lx = float(data[index+3]); ly = float(data[index+4]); dx = float(data[index+5]); dy = float(data[index+6])
            index += 7
            circle = Circle(Point(cx, cy), r)
            line = Line(Point(lx, ly), Point(dx, dy))
            val = circle.line_collide(line)
            print(f"{val:.6f}")
        elif op == 3:
            # Intersection between two circles
            c1x = float(data[index]); c1y = float(data[index+1]); r1 = float(data[index+2])
            c2x = float(data[index+3]); c2y = float(data[index+4]); r2 = float(data[index+5])
            index += 6
            circle1 = Circle(Point(c1x, c1y), r1)
            circle2 = Circle(Point(c2x, c2y), r2)
            p1, p2 = circle1.inter(circle2)
            print(f"{p1.x:.6f} {p1.y:.6f} {p2.x:.6f} {p2.y:.6f}")
        elif op == 4:
            # Check if two circles collide
            c1x = float(data[index]); c1y = float(data[index+1]); r1 = float(data[index+2])
            c2x = float(data[index+3]); c2y = float(data[index+4]); r2 = float(data[index+5])
            index += 6
            circle1 = Circle(Point(c1x, c1y), r1)
            circle2 = Circle(Point(c2x, c2y), r2)
            result = circle1.collide(circle2)
            print("YES" if result else "NO")
        elif op == 5:
            # Point tangent from an external point to the circle.
            cx = float(data[index]); cy = float(data[index+1]); r = float(data[index+2])
            px = float(data[index+3]); py = float(data[index+4]); a = float(data[index+5])
            index += 6
            circle = Circle(Point(cx, cy), r)
            p = circle.point_tangent(Point(px, py), a)
            print(f"{p.x:.6f} {p.y:.6f}")
        elif op == 6:
            # Tangent between two circles.
            c1x = float(data[index]); c1y = float(data[index+1]); r1 = float(data[index+2])
            c2x = float(data[index+3]); c2y = float(data[index+4]); r2 = float(data[index+5])
            a = float(data[index+6]); b = float(data[index+7])
            index += 8
            circle1 = Circle(Point(c1x, c1y), r1)
            circle2 = Circle(Point(c2x, c2y), r2)
            line = circle1.tangent(circle2, a, b)
            print(f"{line.o.x:.6f} {line.o.y:.6f} {line.d.x:.6f} {line.d.y:.6f}")
        elif op == 7:
            # Circumcircle through three points.
            ax = float(data[index]); ay = float(data[index+1])
            bx = float(data[index+2]); by = float(data[index+3])
            cx = float(data[index+4]); cy = float(data[index+5])
            index += 6
            circle = Circle.thru_points(Point(ax, ay), Point(bx, by), Point(cx, cy))
            print(f"{circle.o.x:.6f} {circle.o.y:.6f} {circle.r:.6f}")
        elif op == 8:
            # Two circles through a point and tangent to a line (with a given radius).
            ax = float(data[index]); ay = float(data[index+1])
            lx = float(data[index+2]); ly = float(data[index+3]); dx = float(data[index+4]); dy = float(data[index+5])
            r = float(data[index+6])
            index += 7
            point = Point(ax, ay)
            line = Line(Point(lx, ly), Point(dx, dy))
            c1, c2 = Circle.thru_point_line_r(point, line, r)
            print(f"{c1.o.x:.6f} {c1.o.y:.6f} {c1.r:.6f}")
            print(f"{c2.o.x:.6f} {c2.o.y:.6f} {c2.r:.6f}")
        elif op == 9:
            # Two circles through two points with a fixed radius.
            ax = float(data[index]); ay = float(data[index+1])
            bx = float(data[index+2]); by = float(data[index+3])
            r = float(data[index+4])
            index += 5
            c1, c2 = Circle.thru_points_r(Point(ax, ay), Point(bx, by), r)
            print(f"{c1.o.x:.6f} {c1.o.y:.6f} {c1.r:.6f}")
            print(f"{c2.o.x:.6f} {c2.o.y:.6f} {c2.r:.6f}")
        elif op == 10:
            # Intersection points between circle and line (linecol)
            cx = float(data[index]); cy = float(data[index+1]); r = float(data[index+2])
            lx = float(data[index+3]); ly = float(data[index+4]); dx = float(data[index+5]); dy = float(data[index+6])
            index += 7
            circle = Circle(Point(cx, cy), r)
            line = Line(Point(lx, ly), Point(dx, dy))
            pts = circle.linecol(line)
            if not pts:
                print("NO INTERSECTION")
            elif len(pts) == 1:
                p = pts[0]
                print(f"{p.x:.6f} {p.y:.6f}")
            else:
                p1, p2 = pts
                print(f"{p1.x:.6f} {p1.y:.6f} {p2.x:.6f} {p2.y:.6f}")
        elif op == 11:
            # Area of intersection between the circle and the triangle formed by the circle center and points a and b.
            cx = float(data[index]); cy = float(data[index+1]); r = float(data[index+2])
            ax = float(data[index+3]); ay = float(data[index+4])
            bx = float(data[index+5]); by = float(data[index+6])
            index += 7
            circle = Circle(Point(cx, cy), r)
            area = circle.intertriangle(Point(ax, ay), Point(bx, by))
            print(f"{area:.6f}")
        else:
            print("Invalid operation")

if __name__ == "__main__":
    main()
```

---

### Explanation

#### What Does This Code Do?

- **Geometric Classes:**  
  The script defines classes to work with basic geometry:
  - **Point:** Handles 2D coordinates and common vector operations.
  - **Line:** Represents a line using a point and a direction.
  - **Circle:** Contains methods to compute intersections (with lines and other circles), check for collisions, compute tangents, form the circle through three points (circumcircle), and even compute the area of intersection with a triangle.

- **Operations:**  
  Each method in the `Circle` class implements a common geometric calculation useful in many competitive programming problems (especially those involving computational geometry).

#### When to Use This Code

- **Competitive Programming:**  
  When a contest problem involves circles, lines, intersections, tangents, or related geometry, you can use these templates to quickly compute the needed values.

- **Learning Geometry Algorithms:**  
  Beginners can study these methods to learn how basic geometry operations are implemented (such as calculating intersection points, testing collisions, etc.).

#### How to Use This Code

1. **Input Format (Codevita Environment):**  
   The first number in the input is the number of test cases. Each test case begins with an operation code (1–11) followed by the parameters needed for that operation. For example:
   - To compute the intersection between a circle and a line (operation 1), the input should contain:
     ```
     1
     1        # number of test cases
     1        # operation code 1
     cx cy r lx ly dx dy   (7 numbers)
     ```
2. **Running the Script:**  
   In your Codevita (or any competitive programming) environment, simply paste the code into the editor. The program reads from standard input (`stdin`), processes each test case according to the operation code, and prints the output.
   
3. **Understanding the Output:**  
   The printed output is formatted with six decimal places. For example, if the operation returns a point or area, the result is printed accordingly.

4. **Extending the Code:**  
   You can add more operations or modify the input format as needed. Each function is commented so that even a beginner can understand what is happening.

This script is a self-contained library of geometric routines along with a sample main routine for testing. It serves both as a learning tool and as a ready-to-use template for many geometry problems in competitive programming.