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

        a,b,c = pattern

        if state[a] != '' and state[a] == state[b] == state[c]:

            return state[a]

    return None

# ---------------- TERMINAL ---------------- #

def is_terminal(state):

    return check_winner(state) is not None or '' not in state

# ---------------- CURRENT PLAYER ---------------- #

def get_current_player(state):

    x_count = state.count('X')

    o_count = state.count('O')

    if x_count > o_count:

        return 'O'

    return 'X'

# ---------------- COUNT OUTCOMES ---------------- #

def count_outcomes(state):

    # TERMINAL STATE

    if is_terminal(state):

        winner = check_winner(state)

        if winner == 'O':

            return (1,0,0)

        elif winner == 'X':

            return (0,1,0)

        else:

            return (0,0,1)

    player = get_current_player(state)

    ai_wins = 0

    human_wins = 0

    draws = 0

    for i in range(9):

        if state[i] == '':

            new_state = state.copy()

            new_state[i] = player

            a,h,d = count_outcomes(new_state)

            ai_wins += a

            human_wins += h

            draws += d

    return (ai_wins,human_wins,draws)

# ---------------- CONDITIONAL PROBABILITY ---------------- #

def conditional_probability(board):

    ai_wins, human_wins, draws = count_outcomes(board)

    total = ai_wins + human_wins + draws

    if total == 0:

        probability = 0

    else:

        probability = ai_wins / total

    return {

        "ai_wins": ai_wins,

        "human_wins": human_wins,

        "draws": draws,

        "total_outcomes": total,

        "probability": round(probability,4),

        "percentage": round(probability*100,2)
    }

# ---------------- HOME ---------------- #

@app.route('/')
def home():

    return render_template("index.html")

# ---------------- CONDITIONAL PROBABILITY ROUTE ---------------- #

@app.route('/run_conditional_probability',
           methods=['POST'])

def run_conditional_probability():

    data = request.get_json()

    board = data['board']

    result = conditional_probability(board)

    return jsonify(result)

# ---------------- RUN ---------------- #

if __name__ == '__main__':

    app.run(debug=True)