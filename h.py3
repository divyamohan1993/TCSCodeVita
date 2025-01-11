import math
import heapq

def solve():
    import sys
    data = sys.stdin.read().strip().split()

    S = int(data[0])
    sx, sy, rv = map(float, data[1:4])
    dx, dy = map(float, data[4:6])
    
    N = int(data[6])
    idx = 7
    buildings = []
    for i in range(N):
        bx = float(data[idx]);   by = float(data[idx+1]);   br = float(data[idx+2])
        idx += 3
        buildings.append((bx, by, br))
    
    T = int(data[idx]); idx += 1
    tax_lines = []
    for _ in range(T):
        i1 = int(data[idx]); i2 = int(data[idx+1])
        idx += 2
        i1 -= 1
        i2 -= 1
        tax_lines.append((i1, i2))
    
    def inside_boundary(x, y, r):
        return (r <= x <= S-r) and (r <= y <= S-r)
    
    def collides_with_any_building(x, y):
        for (bx, by, br) in buildings:
            R = br + rv
            dist_sq = (x - bx)**2 + (y - by)**2
            if dist_sq < R*R:
                return True
        return False
    
    if (not inside_boundary(sx, sy, rv)) or collides_with_any_building(sx, sy):
        print("Impossible")
        return
    if (not inside_boundary(dx, dy, rv)) or collides_with_any_building(dx, dy):
        print("Impossible")
        return
    
    sx_i = int(round(sx))
    sy_i = int(round(sy))
    dx_i = int(round(dx))
    dy_i = int(round(dy))
    
    valid = [[False]*(S+1) for _ in range(S+1)]
    for i in range(S+1):
        for j in range(S+1):
            x_c = float(i)
            y_c = float(j)
            if inside_boundary(x_c, y_c, rv):
                if not collides_with_any_building(x_c, y_c):
                    valid[i][j] = True
    
    if not valid[sx_i][sy_i]:
        print("Impossible")
        return
    if not valid[dx_i][dy_i]:
        print("Impossible")
        return
    
    def segments_intersect(p1, p2, p3, p4):
        def orientation(a, b, c):
            val = (b[1] - a[1])*(c[0] - b[0]) - (b[0] - a[0])*(c[1] - b[1])
            if abs(val) < 1e-12: return 0
            return 1 if val < 0 else 2
        
        def on_segment(a, b, c):
            if min(a[0], c[0]) <= b[0] <= max(a[0], c[0]) and \
               min(a[1], c[1]) <= b[1] <= max(a[1], c[1]):
                return True
            return False
        
        o1 = orientation(p1, p2, p3)
        o2 = orientation(p1, p2, p4)
        o3 = orientation(p3, p4, p1)
        o4 = orientation(p3, p4, p2)
        
        if o1 != o2 and o3 != o4:
            return True
        if o1 == 0 and on_segment(p1, p3, p2): return True
        if o2 == 0 and on_segment(p1, p4, p2): return True
        if o3 == 0 and on_segment(p3, p1, p4): return True
        if o4 == 0 and on_segment(p3, p2, p4): return True
        return False
    
    def count_tax_intersections(x1, y1, x2, y2):
        p1 = (x1, y1)
        p2 = (x2, y2)
        crosses = 0
        for (i1, i2) in tax_lines:
            (bx1, by1, br1) = buildings[i1]
            (bx2, by2, br2) = buildings[i2]
            q1 = (bx1, by1)
            q2 = (bx2, by2)
            if segments_intersect(p1, p2, q1, q2):
                crosses += 1
        return crosses
    
    INF = 10**9
    dist = [[INF]*(S+1) for _ in range(S+1)]
    dist[sx_i][sy_i] = 0
    
    directions = [
        (1,0),(-1,0),(0,1),(0,-1),
        (1,1),(1,-1),(-1,1),(-1,-1)
    ]
    
    pq = [(0, sx_i, sy_i)]
    heapq.heapify(pq)
    
    while pq:
        cur_cost, x, y = heapq.heappop(pq)
        if cur_cost > dist[x][y]:
            continue
        if x == dx_i and y == dy_i:
            print(cur_cost)
            return
        for dx2, dy2 in directions:
            nx, ny = x + dx2, y + dy2
            if 0 <= nx <= S and 0 <= ny <= S:
                if valid[nx][ny]:
                    cross = count_tax_intersections(x, y, nx, ny)
                    new_cost = cur_cost + cross
                    if new_cost < dist[nx][ny]:
                        dist[nx][ny] = new_cost
                        heapq.heappush(pq, (new_cost, nx, ny))
    
    print("Impossible")
solve()
