# Py2048
This project is an implementation of the classic 2048 game using **pure Python lists**, without relying on external libraries or AI-generated core logic.

## Problem Description

Implement the core sliding and merging mechanics for the 2048 game. The game uses a $4 \times 4$ grid where tiles can slide in four directions (up, down, left, right) and merge when two tiles with the same value collide.

Your task is to implement two fundamental functions that process a single line (a list of four integers) representing either a row or a column of the board.

## Constraints

- The input line always contains exactly 4 integers
- Tile values are powers of 2 (2, 4, 8, 16, 32, ...)
- Zero represents an empty cell

## How to Run

1. Make sure you have Python 3 installed on your system.

2. Navigate to the project directory:
   ```bash
   cd Py2048
   ```

3. Run the game:
   ```bash
   python main.py
   ```

4. Use the following keys to play:
   - **W** - Move tiles up
   - **A** - Move tiles left
   - **S** - Move tiles down
   - **D** - Move tiles right
   - **Q** - Quit the game

5. The game will display the board after each move and add a new tile if the move was valid.