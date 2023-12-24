from flask import Flask, render_template, request, jsonify
import math
import copy

app = Flask(__name__)

class TicTacToe:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]

    def is_winner(self, player):
        # Check rows
        for row in self.board:
            if all(cell == player for cell in row):
                return True

        # Check columns
        for col in range(self.cols):
            if all(self.board[row][col] == player for row in range(self.rows)):
                return True

        # Check diagonals
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if all(self.board[row + i][col + i] == player for i in range(4)):
                    return True

                if all(self.board[row + i][col + 3 - i] == player for i in range(4)):
                    return True

        return False

    def is_full(self):
        return all(cell != ' ' for row in self.board for cell in row)

    def is_terminal(self):
        return self.is_winner('X') or self.is_winner('O') or self.is_full()

    def get_available_moves(self):
        return [col for col in range(self.cols) if self.board[0][col] == ' ']

    def make_move(self, col, player):
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == ' ':
                self.board[row][col] = player
                return

    def evaluate_board(self):
        if self.is_winner('X'):
            return 1
        elif self.is_winner('O'):
            return -1
        else:
            return 0

    def minimax(self, depth, maximizing_player, alpha, beta):
        if depth == 0 or self.is_terminal():
            return self.evaluate_board()

        if maximizing_player:
            max_eval = -math.inf
            for move in self.get_available_moves():
                new_board = copy.deepcopy(self)
                new_board.make_move(move, 'X')
                eval = new_board.minimax(depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in self.get_available_moves():
                new_board = copy.deepcopy(self)
                new_board.make_move(move, 'O')
                eval = new_board.minimax(depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def find_best_move(self):
        best_move = None
        best_eval = -math.inf
        for move in self.get_available_moves():
            new_board = copy.deepcopy(self)
            new_board.make_move(move, 'X')
            eval = new_board.minimax(5, False, -math.inf, math.inf)
            if eval > best_eval:
                best_eval = eval
                best_move = move
        return best_move

game = TicTacToe(rows=6, cols=7)
player_turn = 'O'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/make_move', methods=['POST'])
def make_move():
    global player_turn
    column = int(request.form['column'])

    if game.is_terminal():
        return jsonify({'result': 'Game over'})

    if player_turn == 'O':
        if column not in game.get_available_moves():
            return jsonify({'result': 'Invalid move'})
        game.make_move(column, 'O')
        player_turn = 'X'  # Switch turn to AI
    else:
        if game.is_terminal():
            return jsonify({'result': 'Game over'})
        ai_move = game.find_best_move()
        game.make_move(ai_move, 'X')
        player_turn = 'O'  # Switch turn to player

    result = game.evaluate_board()

    return jsonify({'result': result, 'player_turn': player_turn, 'board': game.board})

if __name__ == '__main__':
    app.run(debug=True)
