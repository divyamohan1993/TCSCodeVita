def solve():
    import sys

    line = sys.stdin.readline().strip()
    if not line:
        return

    pieces_input = line.split()
    d = int(sys.stdin.readline().strip())

    def parse_piece(s):
        ptype = s[0]
        col_char = s[1]
        row_char = s[2]
        col = ord(col_char) - ord('A')
        row = int(row_char) - 1
        return (ptype, col, row)

    initial_pieces = [parse_piece(x) for x in pieces_input]

    def canonical(pieces):
        s = sorted(pieces, key=lambda x: (x[0], x[1], x[2]))
        return tuple(s)

    rook_dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    bishop_dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    queen_dirs = rook_dirs + bishop_dirs

    def get_directions(ptype):
        if ptype == 'R':
            return rook_dirs
        elif ptype == 'B':
            return bishop_dirs
        else:
            return queen_dirs

    def one_move_successors(state_tuple):
        current_pieces = list(state_tuple)
        occupied = set((p[1], p[2]) for p in current_pieces)
        successors = []
        n = len(current_pieces)

        for i in range(n):
            ptype, c, r = current_pieces[i]
            dirs = get_directions(ptype)

            for dc, dr in dirs:
                step = 1
                while True:
                    new_c = c + step * dc
                    new_r = r + step * dr

                    if not (0 <= new_c < 8 and 0 <= new_r < 8):
                        break

                    if (new_c, new_r) in occupied:
                        break

                    new_arr = current_pieces[:]
                    new_arr[i] = (ptype, new_c, new_r)
                    successors.append(canonical(new_arr))

                    step += 1

        return successors

    from collections import deque

    start_state = canonical(initial_pieces)
    current_layer = {start_state}

    for depth in range(d):
        next_layer = set()
        for st in current_layer:
            for child in one_move_successors(st):
                next_layer.add(child)
        current_layer = next_layer

    print(len(current_layer))

solve()
