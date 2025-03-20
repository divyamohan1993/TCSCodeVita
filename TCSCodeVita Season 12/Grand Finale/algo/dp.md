Below is an extensive Python template that not only implements several common dynamic programming (DP) approaches but also explains when and why to use each one. This template is meant to serve as a guide for many DP cases encountered in high‐level competitions. Each section includes inline comments and usage guidelines.

#!/usr/bin/env python3
"""
Dynamic Programming Template: When to Use What

This comprehensive template covers a variety of dynamic programming (DP)
techniques and provides guidance on when to use each approach.

Included Techniques:

1. Top-Down (Memoization) DP:
   - Use when the recursive structure is natural.
   - Ideal for problems with overlapping subproblems.
   - Examples: Fibonacci numbers, grid path counting, recursive knapsack.

2. Bottom-Up (Tabulation) DP:
   - Use when the state can be computed iteratively in an ordered fashion.
   - Often more space efficient and avoids recursion stack issues.
   - Examples: Longest Common Subsequence, Iterative Knapsack, DP on sequences.

3. Bitmask DP:
   - Use for problems with an exponential state space, typically when the number
     of items is small (N ≤ 20).  
   - Common in combinatorial optimization problems like the Traveling Salesman Problem (TSP).

4. Tree DP:
   - Use when the problem is defined on a tree structure.
   - Solve subproblems on subtrees and combine them for the parent.
   - Examples: Maximum Weighted Independent Set on trees, tree-based House Robber.

5. Additional Tips:
   - Analyze the state space; if multidimensional, ensure memoization is feasible.
   - Check dependency order; if the state forms a DAG, bottom-up might be optimal.
   - Use state compression (e.g., bitmasking) when necessary.
   - Optimize space by storing only what’s needed in iterative DP.

Customize the functions below to fit your specific problem requirements.
"""

import sys, math, bisect
from collections import defaultdict, deque
from functools import lru_cache

# Increase recursion limit if needed.
sys.setrecursionlimit(10**7)

# ---------------------------
# Fast I/O & Debugging Helpers
# ---------------------------
def input():
    return sys.stdin.readline().rstrip("\n")

def read_ints():
    return list(map(int, input().split()))

DEBUG = False
def debug(*args, **kwargs):
    if DEBUG:
        print("DEBUG:", *args, **kwargs, file=sys.stderr)

# ---------------------------
# 1. Top-Down DP (Memoization)
# ---------------------------
# Example: Fibonacci numbers using recursion with memoization.
@lru_cache(maxsize=None)
def fib_top_down(n):
    """
    Top-Down DP for Fibonacci sequence.
    Use this approach when the recursive structure is natural.
    Complexity: O(n)
    """
    if n < 2:
        return n
    return fib_top_down(n-1) + fib_top_down(n-2)

# Generic Top-Down DP Template for problems with state parameters.
@lru_cache(maxsize=None)
def dp_top_down(i, state):
    """
    A generic top-down DP function.
    Parameters:
      i: current index/position
      state: additional state information (e.g., remaining capacity, bitmask)
    Returns:
      Optimal value for state starting from index i.
    Note:
      Customize the base case and transition based on your problem.
    """
    # Base Case: Define termination condition.
    if i == 0:
        # Return a base value given the state.
        return 0
    
    # Recursive Case: Calculate result based on transitions.
    result = dp_top_down(i-1, state)  # Example: skip or modify the state.
    # Optionally, update the result based on including the current element.
    # e.g., result = max(result, some_value + dp_top_down(i-1, new_state))
    return result

# ---------------------------
# 2. Bottom-Up DP (Tabulation)
# ---------------------------
def dp_bottom_up(n, initial_state):
    """
    Bottom-Up DP template.
    Use when the state space can be iteratively computed.
    Parameters:
      n: number of states or length of the sequence.
      initial_state: initial value/state for DP.
    Returns:
      dp: a list/array where dp[i] holds the result for state i.
    Example Use-Cases:
      - Longest Common Subsequence (LCS)
      - Knapsack problems
    """
    dp = [0] * (n + 1)
    dp[0] = initial_state  # Set the initial state.
    # Fill the DP table iteratively.
    for i in range(1, n+1):
        # Transition: update dp[i] based on previous states.
        dp[i] = dp[i-1]  # Placeholder transition.
        # Example: dp[i] = max(dp[i], dp[j] + value) for some j < i.
    return dp

# Example: Bottom-Up Fibonacci (iterative version)
def fib_bottom_up(n):
    """
    Bottom-Up DP for Fibonacci sequence.
    Complexity: O(n)
    """
    if n < 2:
        return n
    dp = [0] * (n+1)
    dp[0], dp[1] = 0, 1
    for i in range(2, n+1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

# ---------------------------
# 3. Bitmask DP
# ---------------------------
def tsp_bitmask_dp(distance):
    """
    Bitmask DP template for the Traveling Salesman Problem (TSP).
    distance: 2D list of distances between nodes.
    Use when the number of nodes is small (typically N ≤ 20).
    Returns:
      Minimum cost to visit all nodes and return to the start.
    """
    n = len(distance)
    # dp[mask][i]: minimum cost to reach set of nodes (mask) ending at node i.
    dp = [[math.inf] * n for _ in range(1 << n)]
    dp[1][0] = 0  # Start at node 0 with only node 0 visited (mask = 1).
    
    for mask in range(1 << n):
        for i in range(n):
            if dp[mask][i] == math.inf:
                continue
            # Extend the path to any unvisited node j.
            for j in range(n):
                if mask & (1 << j) == 0:
                    new_mask = mask | (1 << j)
                    dp[new_mask][j] = min(dp[new_mask][j], dp[mask][i] + distance[i][j])
    # Complete the cycle by returning to the starting node.
    full_mask = (1 << n) - 1
    ans = min(dp[full_mask][i] + distance[i][0] for i in range(n))
    return ans

# ---------------------------
# 4. Tree DP
# ---------------------------
def tree_dp(adj, values, root=0):
    """
    Tree DP template.
    Parameters:
      adj: adjacency list representing the tree.
      values: value associated with each node.
    Returns:
      dp: optimal DP value for the tree rooted at 'root'.
    Example Use-Case:
      Maximum sum of non-adjacent nodes (tree version of the House Robber problem).
    """
    n = len(adj)
    dp = [[0, 0] for _ in range(n)]
    # dp[u][0]: optimal value for subtree rooted at u when u is NOT taken.
    # dp[u][1]: optimal value when u IS taken.
    
    def dfs(u, parent):
        dp[u][1] = values[u]
        for v in adj[u]:
            if v == parent:
                continue
            dfs(v, u)
            dp[u][0] += max(dp[v][0], dp[v][1])
            dp[u][1] += dp[v][0]
    
    dfs(root, -1)
    return max(dp[root][0], dp[root][1])

# ---------------------------
# Guidelines on When to Use Each DP Approach
# ---------------------------
"""
Guidelines:

1. Top-Down (Memoization) DP:
   - Use when the problem has a natural recursive structure.
   - Easy to implement with Python's @lru_cache.
   - Example: Fibonacci, grid-based path problems, recursive knapsack.

2. Bottom-Up (Tabulation) DP:
   - Use when states can be computed iteratively.
   - Avoids recursion stack issues and can be more space efficient.
   - Example: LCS, iterative knapsack, or any DP that forms a Directed Acyclic Graph (DAG).

3. Bitmask DP:
   - Use for combinatorial problems with subsets, especially when N is small (N ≤ 20).
   - Common in optimization problems like TSP, subset sum with bitmask states.

4. Tree DP:
   - Use for problems defined on trees where combining child solutions is natural.
   - Example: Maximum weighted independent set on trees, tree path sums.

5. General Tips:
   - Analyze the DP state: if it is multidimensional, ensure that the memoization or table size is manageable.
   - Check the dependency order: if states can be topologically sorted, bottom-up DP may be ideal.
   - Consider state compression (e.g., bitmasking) if the state space is large.
   - Optimize space by retaining only necessary states.
"""

# ---------------------------
# Main Solve Function
# ---------------------------
def solve():
    """
    Main driver function to test various DP techniques.
    Modify the examples below to fit your specific problem requirements.
    """
    # Example: Toggle DEBUG mode (optional).
    # global DEBUG
    # DEBUG = True if input().strip() == "DEBUG" else False
    
    # --- Top-Down DP Example: Fibonacci ---
    n = int(input("Enter n for Fibonacci: "))
    print("Fibonacci (Top-Down) for", n, ":", fib_top_down(n))
    
    # --- Bottom-Up DP Example: Fibonacci ---
    print("Fibonacci (Bottom-Up) for", n, ":", fib_bottom_up(n))
    
    # --- Generic Top-Down DP Example ---
    # Here we call dp_top_down with a dummy state (customize for your problem).
    print("Generic Top-Down DP result (dummy state):", dp_top_down(n, 0))
    
    # --- Bottom-Up DP Example: Generic Template ---
    dp_result = dp_bottom_up(n, 0)
    print("Generic Bottom-Up DP result (last state):", dp_result[-1])
    
    # --- Bitmask DP Example: TSP ---
    # Dummy distance matrix for 4 nodes.
    distance = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    print("TSP Bitmask DP result:", tsp_bitmask_dp(distance))
    
    # --- Tree DP Example ---
    # Construct a tree (using an adjacency list) with 5 nodes.
    # For example, tree structure:
    #         0
    #       /   \
    #      1     2
    #     / \
    #    3   4
    adj_list = [
        [1, 2],  # Node 0
        [0, 3, 4],  # Node 1
        [0],  # Node 2
        [1],  # Node 3
        [1]   # Node 4
    ]
    # Values associated with each node.
    values = [3, 2, 1, 10, 1]
    print("Tree DP result (max sum of non-adjacent nodes):", tree_dp(adj_list, values))
    
    # Add more DP examples as needed for your specific problem.

# ---------------------------
# Entry Point
# ---------------------------
if __name__ == '__main__':
    solve()

Template Overview

Fast I/O & Debug:
Custom input functions and a DEBUG flag for verbose logging during development.

Top-Down DP (Memoization):
Uses Python’s @lru_cache for natural recursion and overlapping subproblems.
Example: Fibonacci, custom recurrences.

Bottom-Up DP (Tabulation):
Iteratively builds up the solution when the state order is well-defined.
Example: Iterative Fibonacci, LCS.

Bitmask DP:
Handles exponential state spaces (e.g., TSP) for small N by encoding subsets as bitmasks.

Tree DP:
Solves problems on trees by combining results from subtrees (e.g., maximizing non-adjacent node sums).

Guidelines:
Inline comments provide advice on choosing the appropriate DP technique based on problem characteristics.


This template should serve as a robust starting point for many dynamic programming challenges. Feel free to extend and modify each section to meet your problem’s specific needs.

