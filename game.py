"""Core 2048 game logic (shared by CLI and web)."""

import random
from copy import deepcopy


def initialize_board():
    """Initializes the 4x4 board with zeros."""
    return [[0] * 4 for _ in range(4)]


def get_max_digit_length(board):
    """Finds the longest digit length in the board."""
    max_length = 1
    for row in board:
        for cell in row:
            if cell > 0:
                digit_length = len(str(cell))
                max_length = max(max_length, digit_length)
    return max_length


def add_new_tile(board):
    """Randomly places a 2 or 4 in an empty cell (90% / 10% like classic 2048).

    Returns ``(row, col, value)`` of the placed tile, or ``None`` if the board is full.
    """
    empty_cells = []
    for r in range(4):
        for c in range(4):
            if board[r][c] == 0:
                empty_cells.append((r, c))

    if empty_cells:
        r, c = random.choice(empty_cells)
        v = 2 if random.random() < 0.9 else 4
        board[r][c] = v
        return (r, c, v)
    return None


def compress(line: list[int]) -> list[int]:
    """Slides all non-zero numbers to the start of the line."""
    non_zero_numbers = [num for num in line if num != 0]
    return non_zero_numbers + [0] * (4 - len(non_zero_numbers))


def merge(line: list[int]) -> list[int]:
    """Merges adjacent, equal, non-zero numbers."""
    for i in range(3):
        if line[i] == line[i + 1] and line[i] != 0:
            line[i] *= 2
            line[i + 1] = 0
    return compress(line)


def move_left(board: list[list[int]]) -> list[list[int]]:
    """Applies the full move logic (Compress -> Merge -> Compress) to every row."""
    for i in range(4):
        board[i] = compress(board[i])
        board[i] = merge(board[i])
        board[i] = compress(board[i])
    return board


def move_right(board: list[list[int]]) -> list[list[int]]:
    """Moves tiles to the right by reversing rows, applying move logic, then reversing back."""
    for i in range(4):
        row = board[i][::-1]
        row = compress(row)
        row = merge(row)
        row = compress(row)
        board[i] = row[::-1]
    return board


def move_up(board: list[list[int]]) -> list[list[int]]:
    """Moves tiles up by working on columns (extract, process, put back)."""
    for col in range(4):
        column = [board[row][col] for row in range(4)]
        column = compress(column)
        column = merge(column)
        column = compress(column)
        for row in range(4):
            board[row][col] = column[row]
    return board


def move_down(board: list[list[int]]) -> list[list[int]]:
    """Moves tiles down by reversing columns, applying move logic, then reversing back."""
    for col in range(4):
        column = [board[row][col] for row in range(4)][::-1]
        column = compress(column)
        column = merge(column)
        column = column[::-1]
        for row in range(4):
            board[row][col] = column[row]
    return board


def boards_equal(a: list[list[int]], b: list[list[int]]) -> bool:
    return a == b


def _trace_line_compress_merge_compress(
    line_vals: list[int], line_sources: list[list[tuple[int, int]]]
) -> tuple[list[int], list[list[tuple[int, int]]]]:
    """
    Mirrors one row/column of ``move_left`` / ``move_up`` logic (compress → merge → compress)
    while tracking which source cells contribute to each slot.

    ``line_sources[i]`` lists ``(row, col)`` origins for ``line_vals[i]``.
    """
    line = line_vals[:]
    srcs = [list(s) for s in line_sources]

    def compress_phase() -> None:
        nonlocal line, srcs
        nz = [(line[i], srcs[i]) for i in range(4) if line[i] != 0]
        while len(nz) < 4:
            nz.append((0, []))
        line = [nz[i][0] for i in range(4)]
        srcs = [nz[i][1] for i in range(4)]

    compress_phase()
    for i in range(3):
        if line[i] == line[i + 1] and line[i] != 0:
            line[i] *= 2
            line[i + 1] = 0
            srcs[i] = srcs[i] + srcs[i + 1]
            srcs[i + 1] = []
    compress_phase()
    compress_phase()
    return line, srcs


def slide_move_transitions(before: list[list[int]], direction: str) -> list[dict]:
    """
    For animating a move, returns one entry per source tile:

    ``{"fr", "fc", "tr", "tc", "v"}`` where ``v`` is the value **before** the move at ``(fr, fc)``.
    Multiple entries may share the same ``(tr, tc)`` when tiles merge.
    """
    d = direction.lower()
    moves: list[dict] = []
    if d not in ("w", "a", "s", "d"):
        return moves

    if d == "a":
        for r in range(4):
            order = [0, 1, 2, 3]
            vals = [before[r][c] for c in order]
            srcs = [[(r, c)] if before[r][c] else [] for c in order]
            line, out_srcs = _trace_line_compress_merge_compress(vals, srcs)
            for j in range(4):
                if line[j] == 0:
                    continue
                tc = order[j]
                for fr, fc in out_srcs[j]:
                    moves.append(
                        {"fr": fr, "fc": fc, "tr": r, "tc": tc, "v": before[fr][fc]}
                    )
        return moves

    if d == "d":
        for r in range(4):
            order = [3, 2, 1, 0]
            vals = [before[r][c] for c in order]
            srcs = [[(r, c)] if before[r][c] else [] for c in order]
            line, out_srcs = _trace_line_compress_merge_compress(vals, srcs)
            for j in range(4):
                if line[j] == 0:
                    continue
                tc = order[j]
                for fr, fc in out_srcs[j]:
                    moves.append(
                        {"fr": fr, "fc": fc, "tr": r, "tc": tc, "v": before[fr][fc]}
                    )
        return moves

    if d == "w":
        for c in range(4):
            order = [0, 1, 2, 3]
            vals = [before[r][c] for r in order]
            srcs = [[(r, c)] if before[r][c] else [] for r in order]
            line, out_srcs = _trace_line_compress_merge_compress(vals, srcs)
            for j in range(4):
                if line[j] == 0:
                    continue
                tr = order[j]
                for fr, fc in out_srcs[j]:
                    moves.append(
                        {"fr": fr, "fc": fc, "tr": tr, "tc": c, "v": before[fr][fc]}
                    )
        return moves

    # d == "s"
    for c in range(4):
        order = [3, 2, 1, 0]
        vals = [before[r][c] for r in order]
        srcs = [[(r, c)] if before[r][c] else [] for r in order]
        line, out_srcs = _trace_line_compress_merge_compress(vals, srcs)
        for j in range(4):
            if line[j] == 0:
                continue
            tr = order[j]
            for fr, fc in out_srcs[j]:
                moves.append(
                    {"fr": fr, "fc": fc, "tr": tr, "tc": c, "v": before[fr][fc]}
                )
    return moves


def apply_move(board: list[list[int]], direction: str) -> tuple[list[list[int]], bool]:
    """
    Returns (new_board, changed).
    direction: 'a' left, 'd' right, 'w' up, 's' down.
    """
    before = deepcopy(board)
    d = direction.lower()
    if d == "a":
        move_left(board)
    elif d == "d":
        move_right(board)
    elif d == "w":
        move_up(board)
    elif d == "s":
        move_down(board)
    else:
        return board, False
    return board, not boards_equal(before, board)


def has_valid_moves(board: list[list[int]]) -> bool:
    """True if there is an empty cell or any adjacent equal tiles."""
    for r in range(4):
        for c in range(4):
            if board[r][c] == 0:
                return True
            v = board[r][c]
            if c + 1 < 4 and board[r][c + 1] == v:
                return True
            if r + 1 < 4 and board[r + 1][c] == v:
                return True
    return False


def new_game() -> list[list[int]]:
    board = initialize_board()
    add_new_tile(board)
    add_new_tile(board)
    return board
