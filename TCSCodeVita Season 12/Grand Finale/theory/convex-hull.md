### **When to Use Convex Hull?**
A **Convex Hull** is the **smallest convex polygon** that encloses a set of points in a 2D plane. It is used in computational geometry when:
1. **You need the outer boundary of a set of points.**
2. **You need to compute distances between extreme points.**
3. **You need to check if a point is inside a convex shape efficiently.**
4. **You are working with geometric optimizations** like:
   - **Collision detection**
   - **Image processing (boundary detection)**
   - **Path planning in robotics**
   - **Convex hull tricks for optimization problems**

💡 **Common Use Cases:**
- **Finding the smallest enclosing polygon around a given set of points.**
- **Checking whether a point lies inside a convex shape.**
- **Computing the diameter of a point set (Farthest pair problem).**
- **Convex hull trick for dynamic programming optimization (linear functions).**

🛑 **Avoid Convex Hull if:**
- You only need **quick distance calculations** (use bounding boxes).
- The points are **always in convex order** (no need for a hull).

---

## **Types of Convex Hulls & When to Use Them**
There are several algorithms to compute convex hulls, each suited to different use cases:

### **1. Graham’s Scan**
   - **Time Complexity:** `O(N log N)`
   - **Best When:** You have a **moderate number** of points (`N < 10^5`).
   - **Worst When:** You need an online or incremental approach.
   - **How It Works:** 
     - Sort points by x-coordinates.
     - Construct hull using **counterclockwise turns**.

   **Python Code:**
   ```python
   def graham_scan(points):
       points.sort()
       def cross_product(o, a, b):
           return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

       lower, upper = [], []
       for p in points:
           while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
               lower.pop()
           lower.append(p)

       for p in reversed(points):
           while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
               upper.pop()
           upper.append(p)

       return lower[:-1] + upper[:-1]
   ```

---

### **2. Jarvis March (Gift Wrapping)**
   - **Time Complexity:** `O(NH)` (where `H` is the number of hull points)
   - **Best When:** **H (hull points) is small**, even if `N` is large.
   - **Worst When:** Hull size is close to `N`, making it `O(N^2)`.
   - **How It Works:** Starts from leftmost point and iterates **wrapping the hull**.

   **Best Use Case:** Small datasets (`N < 5000`), or cases where `H << N`.

   **Python Code:**
   ```python
   def jarvis_march(points):
       def cross_product(a, b, c):
           return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

       hull = []
       start = min(points)
       point = start

       while True:
           hull.append(point)
           next_point = points[0]
           for p in points:
               if cross_product(point, next_point, p) > 0:
                   next_point = p
           point = next_point
           if point == start:
               break

       return hull
   ```

---

### **3. QuickHull**
   - **Time Complexity:** `O(N log N)` (average), `O(N^2)` (worst case)
   - **Best When:** You need a **divide-and-conquer approach**.
   - **Worst When:** Points are distributed in a **line-like** structure.
   - **How It Works:** Uses **divide and conquer** to recursively find the convex hull.

   **Best Use Case:** Large datasets where sorting is fast but iterative approaches are slow.

   **Python Code:**
   ```python
   def quickhull(points):
       def distance(a, b, p):
           return abs((b[0] - a[0]) * (a[1] - p[1]) - (a[0] - p[0]) * (b[1] - a[1]))

       def hull_subset(points, a, b, side):
           if not points:
               return []
           farthest = max(points, key=lambda p: distance(a, b, p))
           left_set = [p for p in points if distance(a, farthest, p) > 0]
           right_set = [p for p in points if distance(farthest, b, p) > 0]

           return hull_subset(left_set, a, farthest, -side) + [farthest] + hull_subset(right_set, farthest, b, -side)

       leftmost, rightmost = min(points), max(points)
       upper_set = [p for p in points if distance(leftmost, rightmost, p) > 0]
       lower_set = [p for p in points if distance(rightmost, leftmost, p) > 0]

       return [leftmost] + hull_subset(upper_set, leftmost, rightmost, 1) + [rightmost] + hull_subset(lower_set, rightmost, leftmost, -1)
   ```

---

### **4. Monotone Chain Algorithm**
   - **Time Complexity:** `O(N log N)`
   - **Best When:** You need a **stable and efficient algorithm**.
   - **Worst When:** `O(N log N)` sorting dominates the computation.
   - **How It Works:** Similar to Graham’s scan but sorts first.

   **Best Use Case:** Large datasets where `O(N log N)` complexity is acceptable.

---

### **5. Dynamic Convex Hull (Online Updates)**
   - **Time Complexity:** `O(log N)` per update.
   - **Best When:** Points **keep changing dynamically**.
   - **Worst When:** All points are known in advance (use a standard hull).
   - **How It Works:** Uses **data structures like balanced BSTs** to maintain hull.

   **Best Use Case:** Real-time simulations, moving objects in **physics simulations, robotics**.

---

### **6. Convex Hull Trick (Optimization Use Case)**
   - **Use Case:** Used in **Dynamic Programming (DP) optimization**.
   - **How It Works:** Stores functions of the form `y = mx + c` in a convex hull to efficiently find the minimum/maximum.
   - **Example:** **Optimizing DP problems involving cost functions.**
   - **Best Use Case:** **Optimization problems in competitive programming.**

---

## **Comparison of Convex Hull Algorithms**
| Algorithm         | Time Complexity | Best For |
|------------------|---------------|---------|
| **Graham's Scan** | `O(N log N)` | General-purpose convex hull |
| **Jarvis March** | `O(NH)` | Few hull points (`H << N`) |
| **QuickHull** | `O(N log N)` (avg), `O(N^2)` (worst) | Divide-and-conquer problems |
| **Monotone Chain** | `O(N log N)` | Alternative to Graham’s scan |
| **Dynamic Convex Hull** | `O(log N)` per update | Real-time updates (moving points) |
| **Convex Hull Trick** | `O(log N)` per query | DP Optimization (Line Enclosure) |

---

### **Final Thoughts**
- **If you need a general-purpose hull:** Use **Graham’s Scan** (`O(N log N)`).
- **If points update dynamically:** Use **Dynamic Convex Hull** (`O(log N)` per update).
- **If you need DP optimization:** Use **Convex Hull Trick**.
- **If `H << N`:** Use **Jarvis March** (`O(NH)`).

🚀 **Final Tip:**  
If you're solving a **contest problem**, **Graham’s Scan or Monotone Chain** will work **99% of the time**!