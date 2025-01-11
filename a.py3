import sys
from heapq import heappush, heappop

def solve():
    data = sys.stdin.read().strip().split()
    # data pointer
    idx = 0
    
    # 1) Parse N, M
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    
    # 2) Read the "shark strength" grid (N lines, each M entries)
    shark_strength = [[0]*M for _ in range(N)]
    s_r = s_c = -1
    d_r = d_c = -1
    
    for r in range(N):
        for c in range(M):
            val = data[idx]
            idx += 1
            if val == 'S':
                s_r, s_c = r, c
                shark_strength[r][c] = 0   # treat 'S' as 0
            elif val == 'D':
                d_r, d_c = r, c
                shark_strength[r][c] = 0   # treat 'D' as 0
            else:
                # integer
                shark_strength[r][c] = int(val)
    
    # 3) Read the time matrix (N lines, each M integers)
    time_cost = [[0]*M for _ in range(N)]
    for r in range(N):
        for c in range(M):
            time_cost[r][c] = int(data[idx])
            idx += 1
            
    # 4) Read K
    K = int(data[idx])
    idx += 1
    
    # Basic checks
    if s_r < 0 or d_r < 0:
        print("Not Possible")
        return
    
    # Edge case: if source == destination
    if s_r == d_r and s_c == d_c:
        # Then the time = time_cost[s_r][s_c], finalStrength=K (no steps?).
        # Usually you wouldn't do any moves, so steps=0, sumSharks=0 -> finalStrength=K
        print(time_cost[s_r][s_c], K)
        return

    # Directions for adjacency (up/down/left/right)
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    
    # We will run a Dijkstra on (timeSoFar, r, c, sumSharkSoFar, stepsSoFar).
    # Priority queue (min-heap) keyed on timeSoFar.
    pq = []
    # Start from (s_r, s_c).  sumSharks = 0, steps = 0, time = time_cost[s_r][s_c].
    start_time = time_cost[s_r][s_c]
    heappush(pq, (start_time, s_r, s_c, 0, 0))  # (time, r, c, sumSharks, steps)
    
    # visited[r][c][strengthCost] = minimal time we found with that strengthCost
    # but strengthCost can go up to K, which could be large. 
    # For safety in CodeVita constraints (N, M typically up to 10 or 20), we can do a dictionary.
    visited = {}
    # store visited[(r,c, sumSharks, steps)] = best_time
    visited[(s_r, s_c, 0, 0)] = start_time
    
    answer_time = None
    answer_strength = None
    
    while pq:
        curr_time, r, c, sum_sharks, steps = heappop(pq)
        
        # If this state is stale compared to visited, skip
        if visited.get((r, c, sum_sharks, steps), 10**15) < curr_time:
            continue
        
        # Check if we've reached D
        if r == d_r and c == d_c:
            # This is the minimal time to get here. Compute final strength:
            final_strength = K - (sum_sharks + steps)
            answer_time = curr_time
            answer_strength = final_strength
            break
        
        # Expand neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < M:
                # Next cell's cost in sharks
                new_sum_sharks = sum_sharks + shark_strength[nr][nc]
                new_steps = steps + 1
                # Check if strength is still >= 0
                if new_sum_sharks + new_steps <= K:
                    new_time = curr_time + time_cost[nr][nc]
                    # Check if we have visited
                    if (nr, nc, new_sum_sharks, new_steps) not in visited or \
                       visited[(nr, nc, new_sum_sharks, new_steps)] > new_time:
                        visited[(nr, nc, new_sum_sharks, new_steps)] = new_time
                        heappush(pq, (new_time, nr, nc, new_sum_sharks, new_steps))
    
    if answer_time is None:
        print("Not Possible")
    else:
        # We have found a path
        if answer_strength < 0:
            # theoretically shouldn't happen because we checked while expanding
            print("Not Possible")
        else:
            print(answer_time, answer_strength)


# For CodeVita-style: Usually we just define solve() and read from stdin.
# If you want to test locally with some sample input, you can do so like:
if __name__ == "__main__":
    solve()
