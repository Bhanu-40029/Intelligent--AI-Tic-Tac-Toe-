from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# ---------------- POSITIONS ---------------- #

positions = ['A','B','C','D','E','F','G','H','I']

# ---------------- WIN PATTERNS ---------------- #

win_patterns = [

    [0,1,2],
    [3,4,5],
    [6,7,8],

    [0,3,6],
    [1,4,7],
    [2,5,8],

    [0,4,8],
    [2,4,6]
]

# ---------------- CHECK WINNER ---------------- #

def check_winner(state):

    for pattern in win_patterns:

        a, b, c = pattern

        if state[a] != '' and state[a] == state[b] == state[c]:

            return state[a]

    return None

# ---------------- TERMINAL CHECK ---------------- #

def is_terminal(state):

    return check_winner(state) is not None or '' not in state

# ---------------- UTILITY ---------------- #
# X = HUMAN
# O = AI

def utility(state):

    winner = check_winner(state)

    if winner == 'O':
        return 1

    elif winner == 'X':
        return -1

    return 0

# ---------------- CURRENT PLAYER ---------------- #

def get_current_player(board):

    x_count = board.count('X')
    o_count = board.count('O')

    if x_count > o_count:
        return 'O'

    return 'X'

# ---------------- ALPHA BETA ---------------- #

def alphabeta(state, alpha, beta, is_maximizing):

    # TERMINAL STATE

    if is_terminal(state):

        return utility(state)

    # ---------------- AI (MAX) ---------------- #

    if is_maximizing:

        best_score = -999

        for i in range(9):

            if state[i] == '':

                state[i] = 'O'

                score = alphabeta(

                    state,

                    alpha,

                    beta,

                    False
                )

                # BACKTRACK

                state[i] = ''

                best_score = max(best_score, score)

                alpha = max(alpha, best_score)

                # PRUNING

                if beta <= alpha:

                    break

        return best_score

    # ---------------- HUMAN (MIN) ---------------- #

    else:

        best_score = 999

        for i in range(9):

            if state[i] == '':

                state[i] = 'X'

                score = alphabeta(

                    state,

                    alpha,

                    beta,

                    True
                )

                # BACKTRACK

                state[i] = ''

                best_score = min(best_score, score)

                beta = min(beta, best_score)

                # PRUNING

                if beta <= alpha:

                    break

        return best_score

# ---------------- BEST MOVE ---------------- #

def best_move(board):

    traversal = []

    best_score = -999

    move = -1

    for i in range(9):

        if board[i] == '':

            board[i] = 'O'

            score = alphabeta(

                board,

                -999,

                999,

                False
            )

            traversal.append({

                "state": board.copy(),

                "path": [positions[i]],

                "level": 1,

                "score": score
            })

            board[i] = ''

            if score > best_score:

                best_score = score

                move = i

    if move != -1:
        board[move] = 'O'

        traversal.append({

            "best_move": positions[move],

            "best_score": best_score,

            "state": board.copy(),

            "path": [positions[move]],

            "level": 1
        })

    # ALPHA-BETA STATISTICS

    traversal.append({

        "algorithm": "Alpha-Beta",

        "traversal_size": len(traversal)
    })

    return traversal

# ---------------- HOME ---------------- #

@app.route('/')
def home():

    return render_template("index.html")

# ---------------- ALPHA BETA ROUTE ---------------- #

@app.route('/run_alphabeta', methods=['POST'])
def run_alphabeta():

    data = request.get_json()

    board = data['board']

    current_player = get_current_player(board)

    # Human should play first

    if current_player == 'X':

        return jsonify({

            "message": "Human Turn"
        })

    result = best_move(board)

    return jsonify(result)

# ---------------- RUN ---------------- #

if __name__ == '__main__':

    app.run(debug=True)