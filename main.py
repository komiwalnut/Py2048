import random

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

def display_board(board):
    print("\n----- Py2048 -----")
    max_digits = get_max_digit_length(board)
    
    for row in board:
        formatted_row = []
        for cell in row:
            if cell == 0:
                formatted_cell = " " * max_digits
            else:
                formatted_cell = str(cell).center(max_digits)
            formatted_row.append(formatted_cell)
        print(f"| {' | '.join(formatted_row)} |")
    print("------------------\n")

def add_new_tile(board):
    """Randomly places a '2' in an empty cell."""
    empty_cells = []
    for r in range(4):
        for c in range(4):
            if board[r][c] == 0:
                empty_cells.append((r, c))

    if empty_cells:
        r, c = random.choice(empty_cells)
        board[r][c] = 2
        return True
    return False

def compress(line: list[int]) -> list[int]:
    """Slides all non-zero numbers to the start of the line."""
    non_zero_numbers = [num for num in line if num != 0]
    compressed_line = non_zero_numbers + [0] * (4 - len(non_zero_numbers))
    return compressed_line

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
        column = compress(column)
        
        column = column[::-1]
        for row in range(4):
            board[row][col] = column[row]
    return board

if __name__ == "__main__":
    game_board = initialize_board()
    add_new_tile(game_board)
    add_new_tile(game_board)
    
    print("Welcome to Py2048!")
    print("Use W/A/S/D keys to move (Up/Left/Down/Right)")
    print("Press 'Q' to quit\n")
    
    while True:
        display_board(game_board)
        
        move = input("Enter move (W/A/S/D/Q): ").upper().strip()
        
        if move == 'Q':
            print("Thanks for playing!")
            break
        
        board_before = [row[:] for row in game_board]
        
        if move == 'A':
            game_board = move_left(game_board)
        elif move == 'D':
            game_board = move_right(game_board)
        elif move == 'W':
            game_board = move_up(game_board)
        elif move == 'S':
            game_board = move_down(game_board)
        else:
            print("Invalid move! Use W/A/S/D to move or Q to quit.")
            continue
        
        if game_board != board_before:
            add_new_tile(game_board)
            add_new_tile(game_board)
        else:
            print("That move didn't change the board. Try another direction!")