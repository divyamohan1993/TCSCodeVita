import sys
import heapq

def solve():
    data = sys.stdin.read().strip().split()
    idx = 0

    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1

    # Read the shark grid
    shark_grid = [[0]*M for _ in range(N)]
    source = None
    destination = None

    for i in range(N):
        for j in range(M):
            token = data[idx]
            idx += 1
            if token == 'S':
                source = (i, j)
                shark_grid[i][j] = 0
            elif token == 'D':
                destination = (i, j)
                shark_grid[i][j] = 0
            else:
                shark_grid[i][j] = int(token)

    # Read the time grid
    time_grid = [[0]*M for _ in range(N)]
    for i in range(N):
        for j in range(M):
            time_grid[i][j] = int(data[idx])
            idx += 1

    # Initial strength
    K = int(data[idx])
    idx += 1

    if source is None or destination is None:
        print("Not Possible")
        return

    sx, sy = source
    dx, dy = destination

    # Each cell (r,c) will store a small list of (time, leftover) states
    # that are "non-dominated."
    labels = [[[] for _ in range(M)] for _ in range(N)]

    # We'll push (time, r, c, leftover) into a min-heap, keyed by time
    pq = []

    # Insert the starting position: time=0, leftover=K
    labels[sx][sy].append((0, K))
    heapq.heappush(pq, (0, sx, sy, K))

    def is_dominated(r, c, newT, newS):
        """
        Returns True if (newT, newS) is dominated by an existing (t, s) in labels[r][c].
        We say (t, s) dominates (newT, newS) if t <= newT and s >= newS (with at least one strict).
        """
        for (t, s) in labels[r][c]:
            if t <= newT and s >= newS:
                return True
        return False

    def remove_dominated(r, c, newT, newS):
        """
        Remove any (t, s) in labels[r][c] that is dominated by (newT, newS).
        i.e. if newT <= t and newS >= s.
        """
        non_dom = []
        for (t, s) in labels[r][c]:
            # Keep (t, s) if it isn't dominated by (newT, newS).
            if not (newT <= t and newS >= s):
                non_dom.append((t, s))
        labels[r][c] = non_dom

    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    INF = float('inf')

    best_time = INF
    best_strength = -1

    while pq:
        curr_time, r, c, s = heapq.heappop(pq)

        # If we've already found a time better than curr_time to get to D, we can break early.
        # But to ensure we catch a tie in time with better leftover, we can't break at first arrival
        # unless we check the leftover tie carefully. We'll keep it simple: keep going,
        # we only stop if curr_time > best_time.
        if curr_time > best_time:
            break

        # If this label doesn't exist in labels[r][c] anymore, it's outdated
        # (meaning it got dominated or replaced). Skip it.
        # (We check if (curr_time, s) is still in the labels list. 
        #  If not, that means it was pruned.)
        if (curr_time, s) not in labels[r][c]:
            continue

        # If we've reached destination, possibly update best_time/strength
        if (r, c) == (dx, dy):
            # We have a new or equal minimal time solution
            if curr_time < best_time:
                best_time = curr_time
                best_strength = s
            elif curr_time == best_time and s > best_strength:
                best_strength = s
            # We don't break because we might find an equal time with higher leftover
            continue

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < M:
                cost_in_strength = 1 + shark_grid[nr][nc]  # 0 if it's S or D
                newS = s - cost_in_strength
                if newS < 0:
                    continue

                newT = curr_time + time_grid[nr][nc]

                # If newT already exceeds best_time found at D, no need to proceed
                if newT > best_time:
                    continue

                # Check if (newT, newS) is dominated by any existing label at (nr, nc).
                if is_dominated(nr, nc, newT, newS):
                    continue

                # If not dominated, remove those it dominates, then add & push
                remove_dominated(nr, nc, newT, newS)
                labels[nr][nc].append((newT, newS))
                heapq.heappush(pq, (newT, nr, nc, newS))

    # After the loop, check if we found a feasible solution
    if best_time == INF:
        print("Not Possible")
    else:
        print(best_time, best_strength)

if __name__ == "__main__":
    solve()
