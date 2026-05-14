"""CLI entry point for Py2048."""

from game import (
    add_new_tile,
    apply_move,
    get_max_digit_length,
    new_game,
)


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


if __name__ == "__main__":
    game_board = new_game()

    print("Welcome to Py2048!")
    print("Use W/A/S/D keys to move (Up/Left/Down/Right)")
    print("Press 'Q' to quit\n")

    while True:
        display_board(game_board)

        move = input("Enter move (W/A/S/D/Q): ").upper().strip()

        if move == "Q":
            print("Thanks for playing!")
            break

        if move not in ("W", "A", "S", "D"):
            print("Invalid move! Use W/A/S/D to move or Q to quit.")
            continue

        direction = {"W": "w", "A": "a", "S": "s", "D": "d"}[move]
        game_board, changed = apply_move(game_board, direction)

        if changed:
            add_new_tile(game_board)
        else:
            print("That move didn't change the board. Try another direction!")
