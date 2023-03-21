import sys

class TicTacToe:
    def __init__(self):
        self.board = [['.' for _ in range(3)] for _ in range(3)]
        self.pruning = False
        self.node_count = 0
        self.verbose = True 
        
    def print_board(self):
        for row in self.board:
            print(' '.join(row))
        print()

    def reset_board(self):
        self.board = [['.' for _ in range(3)] for _ in range(3)]

    def get_empty_cells(self):
        empty_cells = []
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == '.':
                    empty_cells.append((r, c))
        return empty_cells

    def is_valid_move(self, r, c):
        return 0 <= r < 3 and 0 <= c < 3 and self.board[r][c] == '.'

    def make_move(self, r, c, piece):
        if self.is_valid_move(r, c):
            self.board[r][c] = piece
            return True
        return False

    def undo_move(self, r, c):
        self.board[r][c] = '.'

    def is_winner(self, piece):
        for r in range(3):
            if all([self.board[r][c] == piece for c in range(3)]):
                return True
        for c in range(3):
            if all([self.board[r][c] == piece for r in range(3)]):
                return True
        if all([self.board[i][i] == piece for i in range(3)]) or all([self.board[i][2 - i] == piece for i in range(3)]):
            return True
        return False

    def is_full(self):
        return all([cell == 'X' or cell == 'O' for row in self.board for cell in row])

    def is_terminal(self):
        return self.is_winner('X') or self.is_winner('O') or self.is_full()

    def utility(self, depth):
        if self.is_winner('X'):
            return 1 - 0.1 * depth
        elif self.is_winner('O'):
            return -1 + 0.1 * depth
        else:
            return 0

    def max_score(self, alpha, beta, depth):
        if self.is_terminal():
            return self.utility(depth)

        value = float('-inf')
        for r, c in self.get_empty_cells():
            self.make_move(r, c, 'X')
            self.node_count += 1
            value = max(value, self.min_score(alpha, beta, depth + 1))
            self.undo_move(r, c)

            if self.pruning:
                if value >= beta:
                    return value
                alpha = max(alpha, value)

        return value

    def min_score(self, alpha, beta, depth):
        if self.is_terminal():
            return self.utility(depth)

        value = float('inf')
        for r, c in self.get_empty_cells():
            self.make_move(r, c, 'O')
            self.node_count += 1
            value = min(value, self.max_score(alpha, beta, depth + 1))
            self.undo_move(r, c)

            if self.pruning:
                if value <= alpha:
                    return value
                beta = min(beta, value)

        return value

    def choose(self, piece):
        best_score = float('-inf') if piece == 'X' else float('inf')
        best_move = None
        self.node_count = 0
        for r, c in self.get_empty_cells():
            self.make_move(r, c, piece)
            self.node_count += 1

            if piece == 'X':
                score = self.min_score(float('-inf'), float('inf'), 0)
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
            else:
                score = self.max_score(float('-inf'), float('inf'), 0)
                if score < best_score:
                    best_score = score
                    best_move = (r, c)

            self.undo_move(r, c)
            
            # Print minimax score for this move
            if self.verbose:
                print(f"move ({chr(r + 65)}, {c + 1}) mm_score: {score}")

        # Print the total number of nodes searched
        if self.verbose:
            print(f"number of nodes searched: {self.node_count}")

        return best_move, best_score
    
    def run(self):
        row_map = {'A': 0, 'B': 1, 'C': 2}
        col_map = {'1': 0, '2': 1, '3': 2}
        print("Welcome to jungle >:)")
        print(f"Pruning: {self.pruning}, Verbose output: {self.verbose}")
        print("Type \'commands\' to see commands")
        
        # self.print_board()

        while True:
            command = input().split()
            if(command[0] == 'commands'):
                print("Commands: ")
                print("---")
                print("show")
                print("reset")
                print("move A|B|C 1|2|3 X|O")
                print("choose X|O")
                print("pruning [on|off]")
                print("verbose [on|off]")
                print("quit")
                print("---")
            if command[0] == 'show':
                self.print_board()
            elif command[0] == 'reset':
                self.reset_board()
            elif command[0] == 'move':
                piece, row, col = command[1], row_map[command[2]], col_map[command[3]]
                if self.is_valid_move(row, col):
                    self.make_move(row, col, piece)
                    self.print_board()
            elif command[0] == 'choose':
                piece = command[1]
                move, score = self.choose(piece)
                self.make_move(move[0], move[1], piece)
                self.print_board()
            elif command[0] == 'pruning' and len(command) == 1:
                print("Pruning is", "on" if self.pruning else "off")
            elif command[0] == 'pruning' and len(command) == 2:
                if command[1] == 'on':
                    self.pruning = True
                elif command[1] == 'off':
                    self.pruning = False
            elif command[0] == 'verbose' and len(command) == 1:
                print("Verbose printing is", "on" if self.verbose else "off")
            elif command[0] == 'verbose' and len(command) == 2:
                if command[1] == 'on':
                    self.verbose = True
                elif command[1] == 'off':
                    self.verbose = False
            elif command[0] == 'quit':
                break
                

game = TicTacToe()
game.run()