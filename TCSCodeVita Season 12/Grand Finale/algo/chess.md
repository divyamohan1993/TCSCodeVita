Below is an extensive Python template tailored for solving chess‐related competitive programming problems. This template covers everything from fast I/O and debugging to board representation, coordinate conversions (algebraic notation ↔ board indices), precomputed move directions for each piece, move generation routines, attack detection, board simulation functions, and even placeholders for advanced data structures if needed. You can modify or extend the functions based on the specific chess problem requirements.

#!/usr/bin/env python3
"""
Chess Competitive Programming Template

This template provides a comprehensive framework for solving chess-related problems.
It includes:

1. Fast I/O and debugging functionality.
2. Board representation and initialization utilities.
3. Conversion functions between algebraic chess notation (e.g., "e4") and 0-indexed board coordinates.
4. Precomputed move directions for various pieces:
   - King, Knight, Bishop, Rook, and Queen.
5. Utility functions:
   - Checking if coordinates are within board bounds.
   - Generating moves for sliding pieces (bishop, rook, queen) and for non-sliding pieces (king, knight).
   - (Optional) Pawn moves and attack generation – can be adapted as needed.
6. Functions to simulate board moves and revert moves.
7. An attack detection routine to check if a given square is under attack.
8. Placeholders for advanced data structures (DSU, Segment Tree) for problems that might combine chess with other algorithmic challenges.
9. A main solve() function that ties everything together.

Feel free to extend this template with further algorithms (e.g., minimax, bitboard techniques, etc.) as required.
"""

import sys
import math
import bisect
from collections import defaultdict, deque, Counter
import heapq
import itertools
from functools import reduce, lru_cache

# Increase recursion limit (useful for deep recursive searches, if needed)
sys.setrecursionlimit(10**7)

# ---------------------------
# Fast Input & I/O Helpers
# ---------------------------
def input():
    return sys.stdin.readline().rstrip("\n")

def read_ints():
    return list(map(int, input().split()))

def read_strs():
    return input().split()

# ---------------------------
# Debugging Functionality
# ---------------------------
DEBUG = False  # Set to True for additional debug output.
def debug(*args, **kwargs):
    if DEBUG:
        print("DEBUG:", *args, **kwargs, file=sys.stderr)

# ---------------------------
# Chess Board & Coordinate Utilities
# ---------------------------
BOARD_SIZE = 8  # Standard chess board dimensions (8x8)

def in_bounds(x, y):
    """Check if (x, y) lies within the chess board."""
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

def chess_to_index(pos):
    """
    Convert algebraic notation (e.g., 'e4') to 0-indexed board coordinates.
    Convention: (0,0) is top-left corresponding to 'a8'; (7,7) is bottom-right ('h1').
    """
    if len(pos) < 2:
        raise ValueError("Invalid chess coordinate")
    col = ord(pos[0].lower()) - ord('a')
    row = BOARD_SIZE - int(pos[1])
    return row, col

def index_to_chess(x, y):
    """
    Convert board coordinates (x, y) to algebraic notation.
    Using the same convention: (0,0) -> 'a8', (7,7) -> 'h1'
    """
    return f"{chr(y + ord('a'))}{BOARD_SIZE - x}"

def init_empty_board():
    """
    Create an empty chess board with '.' denoting empty squares.
    Board is represented as a list of lists (rows).
    """
    return [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def init_standard_board():
    """
    Initialize a standard chess starting position.
    White pieces are in lowercase; Black pieces in uppercase.
    Modify as necessary for your problem.
    """
    board = init_empty_board()
    # Black pieces (top of board)
    board[0] = list("RNBQKBNR")
    board[1] = ['P'] * BOARD_SIZE
    # Empty rows
    for i in range(2, 6):
        board[i] = ['.'] * BOARD_SIZE
    # White pieces (bottom of board)
    board[6] = ['p'] * BOARD_SIZE
    board[7] = list("rnbqkbnr")
    return board

def print_board(board):
    """Print the board in a readable format."""
    for row in board:
        print(" ".join(row))
    print()  # Blank line for separation

# ---------------------------
# Piece Move Directions & Generators
# ---------------------------
# Knight moves: 8 possible L-shaped moves.
KNIGHT_MOVES = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                (1, 2), (1, -2), (-1, 2), (-1, -2)]

# King moves: 8 surrounding squares.
KING_MOVES = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),          (0, 1),
              (1, -1),  (1, 0), (1, 1)]

# Sliding piece directions (Bishop, Rook, Queen)
BISHOP_DIRS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
ROOK_DIRS   = [(-1, 0), (1, 0), (0, -1), (0, 1)]
QUEEN_DIRS  = BISHOP_DIRS + ROOK_DIRS

def get_knight_moves(x, y):
    """Return a list of valid moves for a knight at position (x, y)."""
    moves = []
    for dx, dy in KNIGHT_MOVES:
        nx, ny = x + dx, y + dy
        if in_bounds(nx, ny):
            moves.append((nx, ny))
    return moves

def get_king_moves(x, y):
    """Return a list of valid moves for a king at position (x, y)."""
    moves = []
    for dx, dy in KING_MOVES:
        nx, ny = x + dx, y + dy
        if in_bounds(nx, ny):
            moves.append((nx, ny))
    return moves

def get_sliding_moves(x, y, board, directions, own_pieces):
    """
    Generate moves for sliding pieces (bishop, rook, queen).
    board: current board state.
    directions: list of (dx, dy) directions.
    own_pieces: set of characters representing your own pieces (to stop movement).
    Returns list of (nx, ny) coordinates the piece can move to.
    """
    moves = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        while in_bounds(nx, ny):
            if board[nx][ny] == '.':
                moves.append((nx, ny))
            else:
                # Stop if encountering any piece; you may capture if it is opponent's.
                if board[nx][ny] not in own_pieces:
                    moves.append((nx, ny))
                break
            nx += dx
            ny += dy
    return moves

def generate_moves_for_piece(board, x, y):
    """
    Given a board and a position (x, y), return a list of possible moves.
    This function handles different piece types. Modify as per problem requirements.
    
    Convention:
      - Lowercase pieces (e.g., 'p', 'n', 'b', 'r', 'q', 'k') represent one color (e.g., white).
      - Uppercase pieces represent the opposite color (e.g., black).
    """
    piece = board[x][y]
    moves = []
    if piece == '.':
        return moves  # No piece to move

    # Define own piece set for simplicity.
    if piece.islower():
        own = set("pnbrqk")
        enemy = set("PNBRQK")
    else:
        own = set("PNBRQK")
        enemy = set("pnbrqk")

    # Knight moves
    if piece.lower() == 'n':
        for nx, ny in get_knight_moves(x, y):
            if board[nx][ny] == '.' or board[nx][ny] in enemy:
                moves.append(((x, y), (nx, ny)))
    
    # King moves (note: castling not handled by default)
    elif piece.lower() == 'k':
        for nx, ny in get_king_moves(x, y):
            if board[nx][ny] == '.' or board[nx][ny] in enemy:
                moves.append(((x, y), (nx, ny)))
    
    # Bishop moves
    elif piece.lower() == 'b':
        moves.extend([((x, y), (nx, ny)) for nx, ny in get_sliding_moves(x, y, board, BISHOP_DIRS, own)])
    
    # Rook moves
    elif piece.lower() == 'r':
        moves.extend([((x, y), (nx, ny)) for nx, ny in get_sliding_moves(x, y, board, ROOK_DIRS, own)])
    
    # Queen moves
    elif piece.lower() == 'q':
        moves.extend([((x, y), (nx, ny)) for nx, ny in get_sliding_moves(x, y, board, QUEEN_DIRS, own)])
    
    # Pawn moves: basic forward moves and captures (adjust based on color and initial position)
    elif piece.lower() == 'p':
        direction = -1 if piece.islower() else 1  # Lowercase (white) moves up; uppercase (black) moves down.
        start_row = 6 if piece.islower() else 1
        # Forward move
        nx, ny = x + direction, y
        if in_bounds(nx, ny) and board[nx][ny] == '.':
            moves.append(((x, y), (nx, ny)))
            # Double move from starting position
            if x == start_row:
                nx2 = nx + direction
                if in_bounds(nx2, ny) and board[nx2][ny] == '.':
                    moves.append(((x, y), (nx2, ny)))
        # Diagonal captures
        for dy in [-1, 1]:
            nx, ny = x + direction, y + dy
            if in_bounds(nx, ny) and board[nx][ny] in enemy:
                moves.append(((x, y), (nx, ny)))
        # (Promotion, en passant, etc. can be added as needed)
    
    return moves

# ---------------------------
# Attack Detection & Board Evaluation
# ---------------------------
def is_square_attacked(board, x, y, attacker_color):
    """
    Determine if square (x, y) is attacked by any piece of the attacker_color.
    attacker_color: 'white' or 'black'
    This function checks knight, pawn, king, and sliding piece attacks.
    """
    # Define piece sets based on color.
    if attacker_color == 'white':
        pawn, knight, bishop, rook, queen, king = 'p', 'n', 'b', 'r', 'q', 'k'
        own = set("pnbrqk")
    else:
        pawn, knight, bishop, rook, queen, king = 'P', 'N', 'B', 'R', 'Q', 'K'
        own = set("PNBRQK")

    # Pawn attacks (diagonals depend on pawn direction)
    pawn_dir = -1 if attacker_color == 'white' else 1
    for dy in [-1, 1]:
        nx, ny = x + pawn_dir, y + dy
        if in_bounds(nx, ny) and board[nx][ny] == pawn:
            return True

    # Knight attacks
    for dx, dy in KNIGHT_MOVES:
        nx, ny = x + dx, y + dy
        if in_bounds(nx, ny) and board[nx][ny] == knight:
            return True

    # King attacks (usually only needed for move validation)
    for dx, dy in KING_MOVES:
        nx, ny = x + dx, y + dy
        if in_bounds(nx, ny) and board[nx][ny] == king:
            return True

    # Sliding pieces: Bishop/Queen diagonals
    for dx, dy in BISHOP_DIRS:
        nx, ny = x + dx, y + dy
        while in_bounds(nx, ny):
            cell = board[nx][ny]
            if cell != '.':
                if cell == bishop or cell == queen:
                    return True
                break
            nx += dx
            ny += dy

    # Sliding pieces: Rook/Queen straight lines
    for dx, dy in ROOK_DIRS:
        nx, ny = x + dx, y + dy
        while in_bounds(nx, ny):
            cell = board[nx][ny]
            if cell != '.':
                if cell == rook or cell == queen:
                    return True
                break
            nx += dx
            ny += dy

    return False

# ---------------------------
# Move Simulation & Undo
# ---------------------------
def make_move(board, move):
    """
    Simulate making a move on the board.
    move: ((from_x, from_y), (to_x, to_y))
    Returns a tuple (captured_piece, updated_board) so that the move can be undone.
    Note: This is a simple simulation. Advanced rules (castling, en passant, promotion) need additional handling.
    """
    (x, y), (nx, ny) = move
    captured = board[nx][ny]
    piece = board[x][y]
    board[nx][ny] = piece
    board[x][y] = '.'
    return captured

def undo_move(board, move, captured):
    """
    Undo a move on the board.
    move: ((from_x, from_y), (to_x, to_y))
    captured: the piece that was originally on the target square (or '.' if none).
    """
    (x, y), (nx, ny) = move
    piece = board[nx][ny]
    board[x][y] = piece
    board[nx][ny] = captured

# ---------------------------
# Advanced Data Structures (Optional)
# ---------------------------
# DSU / Union-Find: Useful in problems where connectivity on board regions is needed.
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, a):
        if self.parent[a] != a:
            self.parent[a] = self.find(self.parent[a])
        return self.parent[a]

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.rank[a] < self.rank[b]:
            a, b = b, a
        self.parent[b] = a
        if self.rank[a] == self.rank[b]:
            self.rank[a] += 1
        return True

# Segment Tree: For range queries (e.g., evaluating board segments or move sequences)
class SegmentTree:
    def __init__(self, data, func=min, default=float('inf')):
        self.n = len(data)
        self.func = func
        self.default = default
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [default] * (2 * self.size)
        # Build the tree
        for i in range(self.n):
            self.tree[self.size + i] = data[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.func(self.tree[2 * i], self.tree[2 * i + 1])
    
    def update(self, idx, value):
        idx += self.size
        self.tree[idx] = value
        while idx > 1:
            idx //= 2
            self.tree[idx] = self.func(self.tree[2 * idx], self.tree[2 * idx + 1])
    
    def query(self, l, r):
        res = self.default
        l += self.size
        r += self.size
        while l < r:
            if l & 1:
                res = self.func(res, self.tree[l])
                l += 1
            if r & 1:
                r -= 1
                res = self.func(res, self.tree[r])
            l //= 2
            r //= 2
        return res

# ---------------------------
# Main Solve Function
# ---------------------------
def solve():
    """
    Main function to process input and produce output.
    Adapt the reading and processing logic to your specific chess problem.

    Examples:
      - Reading a board configuration.
      - Generating all legal moves for a given side.
      - Checking if a given move leaves the king in check.
      - Simulating moves and backtracking for search problems.
    """
    # Example: Toggle debugging mode based on input (optional)
    # global DEBUG
    # DEBUG = True if input().strip() == "DEBUG" else False

    # Example Input: number of test cases
    t = 1
    # Uncomment if multiple test cases:
    # t = int(input())

    for _ in range(t):
        # Read board configuration
        # Option 1: Standard board (if problem uses starting position)
        board = init_standard_board()

        # Option 2: Read custom board from input (example: 8 lines each containing 8 characters)
        # board = [list(input().strip()) for _ in range(BOARD_SIZE)]
        
        debug("Initial board:")
        debug("\n".join("".join(row) for row in board))
        
        # Example: Generate all moves for a specific piece given its position in algebraic notation.
        pos = input().strip()  # e.g., "e2"
        try:
            x, y = chess_to_index(pos)
        except ValueError:
            print("Invalid position")
            return
        
        moves = generate_moves_for_piece(board, x, y)
        debug(f"Possible moves for piece at {pos} ({x}, {y}):", moves)
        
        # Example: Print moves in algebraic notation
        for move in moves:
            (fx, fy), (tx, ty) = move
            move_str = f"{index_to_chess(fx, fy)} -> {index_to_chess(tx, ty)}"
            print(move_str)
        
        # Example: Check if a square is attacked by white
        square = input().strip()  # e.g., "e4"
        try:
            sx, sy = chess_to_index(square)
        except ValueError:
            print("Invalid square")
            return
        
        attacked = is_square_attacked(board, sx, sy, attacker_color='white')
        print(f"Square {square} is {'attacked' if attacked else 'safe'} by white.")

        # (Optional) You can add further simulation, search, or evaluation routines here.
        # For example, iterate over all pieces, simulate moves, and use backtracking to search for checkmates.
        # Also, DSU or SegmentTree may be employed in problems that combine chess with connectivity or range queries.

# ---------------------------
# Entry Point
# ---------------------------
if __name__ == '__main__':
    solve()

Template Overview

Fast I/O & Debug: Quickly read inputs and toggle detailed logging via the DEBUG flag.

Board Utilities: Functions to initialize boards (both standard and custom) and convert between chess notation and board indices.

Move Generation: Predefined move sets for knights, kings, sliding pieces (bishop, rook, queen), plus a basic pawn move generator.

Attack Detection: Check if a square is attacked by a given color—a common requirement in chess puzzles.

Move Simulation: Functions to apply and undo moves (helpful for search/backtracking algorithms).

Advanced Structures: Optional DSU and Segment Tree classes for problems that may require extra data structure support.

Main Solve Function: A driver function that reads input, processes the board, generates moves, and demonstrates usage of key functions.


This comprehensive template should serve as a robust starting point for any chess problem in competitive programming. Adjust and expand each section as needed for specific contest problems.

