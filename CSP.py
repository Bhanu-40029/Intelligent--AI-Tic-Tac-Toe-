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


# ---------------- GET CURRENT PLAYER ---------------- #

def get_current_player(state):

    x_count = state.count('X')

    o_count = state.count('O')

    if x_count > o_count:
        return 'O'

    return 'X'


# ---------------- CSP CONSTRAINT CHECK ---------------- #

def is_valid_state(state):

    x_count = state.count('X')

    o_count = state.count('O')


    # Constraint 1
    # alternate turns

    if abs(x_count - o_count) > 1:
        return False


    # Constraint 2
    # both players cannot win together

    x_win = False

    o_win = False

    for pattern in win_patterns:

        values = [state[i] for i in pattern]

        if values == ['X','X','X']:
            x_win = True

        if values == ['O','O','O']:
            o_win = True

    if x_win and o_win:
        return False


    # Constraint 3
    # board size

    if len(state) != 9:
        return False


    return True


# ---------------- DFS + CSP ---------------- #

def csp_dfs(start):

    stack = [(start, [])]

    explored = set()

    traversal = []

    while stack:

        state, path = stack.pop()

        key = tuple(state)

        if key in explored:
            continue

        explored.add(key)

        traversal.append({

            "state": state,

            "path": path,

            "next_moves": [
                positions[i]
                for i in range(9)
                if state[i] == ''
            ],

            "level": len(path)
        })


        # ---------------- GOAL CHECK ---------------- #

        winner = check_winner(state)

        if winner:

            traversal.append({
                "winner": winner
            })

            break


        # ---------------- CURRENT PLAYER ---------------- #

        player = get_current_player(state)


        children = []


        # ---------------- GENERATE VALID STATES ---------------- #

        for i in range(9):

            # valid move constraint
            if state[i] == '':

                new_state = state.copy()

                new_state[i] = player


                # CSP VALIDATION

                if is_valid_state(new_state):

                    new_path = path + [positions[i]]

                    children.append((
                        new_state,
                        new_path
                    ))


        # reverse for proper DFS order
        for child_state, child_path in reversed(children):

            stack.append((
                child_state,
                child_path
            ))

    return traversal


# ---------------- HOME ---------------- #

@app.route('/')
def home():

    return render_template("index.html")


# ---------------- CSP ROUTE ---------------- #

@app.route('/run_csp', methods=['POST'])

def run_csp():

    data = request.get_json()

    current_board = data['board']

    result = csp_dfs(current_board)

    return jsonify(result)


# ---------------- RUN ---------------- #

if __name__ == '__main__':

    app.run(debug=True)