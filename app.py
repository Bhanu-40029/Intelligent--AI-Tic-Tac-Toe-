from flask import Flask, render_template, jsonify, request
from collections import deque

app = Flask(__name__)

# ---------------- POSITIONS ---------------- #

positions = ['A','B','C','D','E','F','G','H','I']

# ---------------- WIN CHECK ---------------- #

def check_winner(state):

    win = [

        [0,1,2],
        [3,4,5],
        [6,7,8],

        [0,3,6],
        [1,4,7],
        [2,5,8],

        [0,4,8],
        [2,4,6]
    ]

    for comb in win:

        if state[comb[0]] != '' and all(state[i] == state[comb[0]] for i in comb):

            return state[comb[0]]

    return None


# ---------------- NEXT STATES ---------------- #

def get_next_states(state, player, path):

    next_nodes = []

    for i in range(9):

        if state[i] == '':

            new_state = state.copy()

            new_state[i] = player

            new_path = path + [positions[i]]

            next_nodes.append((
                new_state,
                new_path
            ))

    return next_nodes


# ---------------- AVAILABLE MOVES ---------------- #

def get_available_moves(state):

    return [
        positions[i]
        for i in range(9)
        if state[i] == ''
    ]

def get_current_player(state):

    x_count = state.count('X')

    o_count = state.count('O')

    if x_count > o_count:
        return 'O'

    return 'X'
# ---------------- BFS ---------------- #

def bfs(start):
    frontier = deque([
        (start, [], get_current_player(start))
    ])

    explored = set()

    traversal = []

    while frontier:

        state, path, player = frontier.popleft()

        key = tuple(state)

        if key in explored:
            continue

        explored.add(key)

        traversal.append({

            "state": state,

            "path": path,

            "next_moves": get_available_moves(state),

            "level": len(path)
        })

        # STOP WHEN WIN FOUND
        winner = check_winner(state)

        if winner:

            traversal.append({
                "winner": winner
            })

            break

        next_player = 'O' if player == 'X' else 'X'

        for child_state, child_path in get_next_states(
            state,
            player,
            path
        ):

            frontier.append((
                child_state,
                child_path,
                next_player
            ))

    return traversal


# ---------------- HOME ---------------- #

@app.route('/')
def home():

    return render_template("index.html")


# ---------------- BFS ROUTE ---------------- #

@app.route('/run_bfs', methods=['POST'])

def run_bfs():

    data = request.get_json()

    current_board = data['board']

    result = bfs(current_board)

    return jsonify(result)


# ---------------- RUN ---------------- #

if __name__ == '__main__':

    app.run(debug=True)