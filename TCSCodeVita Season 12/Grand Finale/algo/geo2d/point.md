Below is the Python version of the given C++ point (P) structure. This implementation defines a 2D point with many geometric operations including addition, subtraction, scalar‐multiplication and division, dot and “cross” products (with the cross operator defined via `%`), rotation, magnitude calculations, angular comparisons, and more. (In this code, we assume that “T” is a floating–point number and use a global EPS for precision comparisons.)

---

```python
import math

EPS = 1e-9

class P:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    # String representation (similar to overloaded << in C++).
    def __repr__(self):
        return f"{self.x} {self.y}"

    # Addition: self + other
    def __add__(self, other):
        return P(self.x + other.x, self.y + other.y)

    # Subtraction: self - other
    def __sub__(self, other):
        return P(self.x - other.x, self.y - other.y)

    # Multiplication:
    # If other is a number, scale the point.
    # If other is a P, compute the dot product.
    def __mul__(self, other):
        if isinstance(other, P):
            return self.x * other.x + self.y * other.y  # dot product
        else:
            return P(self.x * other, self.y * other)
    __rmul__ = __mul__

    # True division by a scalar.
    def __truediv__(self, other):
        return P(self.x / other, self.y / other)

    # Unary negation.
    def __neg__(self):
        return P(-self.x, -self.y)

    # Cross product is defined as:
    # self % other  :=  self.rot() dot other
    def __mod__(self, other):
        return self.rot() * other  # here, '*' is dot product

    # Rotate the point 90° counterclockwise: (x, y) -> (-y, x)
    def rot(self):
        return P(-self.y, self.x)

    # "Left" test: returns (b - a) cross (self - a)
    # (i.e. tells how much the vector from a to self is to the left of a->b)
    def left(self, a, b):
        return (b - a) % (self - a)

    # Returns the square of the magnitude.
    def magsq(self):
        return self.x * self.x + self.y * self.y

    # Returns the Euclidean norm (length).
    def mag(self):
        return math.sqrt(self.magsq())

    # Returns the unit (normalized) vector.
    def unit(self):
        m = self.mag()
        if m < EPS:
            return P(0, 0)
        return self / m

    # Returns True if this point (treated as a vector) is in the "lower half"
    # as defined by: (abs(y)<=EPS and x < -EPS) or (y < -EPS)
    def half(self):
        return (abs(self.y) <= EPS and self.x < -EPS) or (self.y < -EPS)

    # Angular comparison.
    # Returns a value analogous to C++ strcmp: negative, zero, or positive.
    # Here we compute h = int(self.half()) - int(r.half())
    # If h != 0, return h; otherwise, return (r % self)
    # Note: r % self means: r.rot() dot self.
    def angcmp(self, r):
        h = (1 if self.half() else 0) - (1 if r.half() else 0)
        if h != 0:
            return h
        # Using our definition of %, r % self = r.rot() dot self.
        return r % self

    # Angular comparison relative to two given vectors a and b.
    # This function is modeled on the C++ version.
    def angcmp_rel(self, a, b):
        z = P(self.x, self.y)  # copy of self
        # Compute a small "flag" value for a and b.
        ha = (1 if (z % a <= 0 and z * a < 0) or (z % a < 0) else 0)
        hb = (1 if (z % b <= 0 and z * b < 0) or (z % b < 0) else 0)
        h = ha - hb
        if h != 0:
            return h
        # Otherwise, return b % a = b.rot() dot a.
        return b % a

    # Equality comparison, with tolerance EPS.
    def __eq__(self, other):
        return abs(self.x - other.x) <= EPS and abs(self.y - other.y) <= EPS

    # Returns the angle (in radians) of this vector (from the x–axis).
    def angle(self):
        return math.atan2(self.y, self.x)

    # Construct a unit vector from an angle (in radians).
    @staticmethod
    def from_angle(a):
        return P(math.cos(a), math.sin(a))
```

---

### Explanation

1. **Constructors and I/O:**  
   - The constructor (`__init__`) initializes a point with coordinates (x, y).  
   - The `__repr__` method provides a string representation similar to the overloaded output operator in C++.

2. **Arithmetic Operators:**  
   - `__add__` and `__sub__` implement vector addition and subtraction.  
   - The multiplication operator (`__mul__`) is overloaded: if the other operand is a `P` instance, it computes the dot product; otherwise, it performs scalar multiplication.  
   - `__truediv__` performs scalar division.  
   - `__neg__` gives the negation of a point.

3. **Rotation and Cross Product:**  
   - The `rot()` method rotates the point 90° counterclockwise.  
   - The cross product is defined via the `%` operator: `p % q` equals `p.rot() * q`, which is the dot product of the rotated vector with q.

4. **Additional Methods:**  
   - `left(a, b)` computes the cross product between `(b - a)` and `(self - a)`—useful for determining turn direction.  
   - `magsq()`, `mag()`, and `unit()` provide the squared magnitude, magnitude, and unit vector.  
   - `half()` determines if the point lies in the “lower half” (used for angular comparisons).  
   - `angcmp(r)` and `angcmp_rel(a, b)` perform angular comparisons similar to C++’s `strcmp`–style comparisons.  
   - `angle()` returns the polar angle and `from_angle()` constructs a point from an angle.

This translation captures the functionality of the original C++ code while following Python’s conventions. Happy coding!