# Tic Tac Toe with Minimax Algorithm

This is a simple implementation of Tic Tac Toe in Python using the Minimax algorithm with optional alpha-beta pruning. The game can be played in the command line.

## How to Run
`python ttt.py`

## Commands
Here are the commands you can use to interact with the game:

- `commands` Displays all commands listed here.
- `show`: Displays the current game board.
- `reset`: Resets the game board to its initial state.
- `move A|B|C 1|2|3 X|O`: Makes a move for the specified piece (X or O) at the specified row (A, B, or C) and column (1, 2, or 3).
- `choose X|O`: Chooses the best move for the specified piece (X or O) using the Minimax algorithm.
- `pruning [on|off]`: Enables or disables alpha-beta pruning. Type \`pruning\` without arguments to check its current state.
- `verbose [on|off]`: Enables or disables verbose output for the Minimax algorithm. Type \`verbose\` without arguments to check its current state.
- `quit`: Exits the game.