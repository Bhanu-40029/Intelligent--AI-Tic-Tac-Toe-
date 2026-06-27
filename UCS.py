from flask import Flask, render_template, jsonify, request
import heapq

app = Flask(__name__)

# ---------------- POSITIONS ---------------- #

positions = ['A','B','C','D','E','F','G','H','I']

# ---------------- COST FUNCTION ---------------- #

def get_cost(index):

    # Center
    if index == 4:
        return 1

    # Corners
    elif index in [0,2,6,8]:
        return 2

    # Edges
    else:
        return 3


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


# ---------------- UCS ---------------- #

def ucs(start):

    frontier = []

    counter = 0

    # (cost, counter, state, path, player)
    heapq.heappush(frontier, (

        0,

        counter,

        start,

        [],

        'X'
    ))

    explored = set()

    traversal = []

    while frontier:

        cost_so_far, _, state, path, player = heapq.heappop(frontier)

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

            "level": len(path),

            "cost": cost_so_far
        })

        # STOP IF WIN FOUND
        winner = check_winner(state)

        if winner:

            traversal.append({
                "winner": winner
            })

            break

        next_player = 'O' if player == 'X' else 'X'

        # GENERATE CHILDREN
        for i in range(9):

            if state[i] == '':

                new_state = state.copy()

                new_state[i] = player

                move_cost = get_cost(i)

                new_cost = cost_so_far + move_cost

                new_path = path + [positions[i]]

                counter += 1

                heapq.heappush(frontier, (

                    new_cost,

                    counter,

                    new_state,

                    new_path,

                    next_player
                ))

    return traversal


# ---------------- HOME ---------------- #

@app.route('/')
def home():

    return render_template("index.html")


# ---------------- UCS ROUTE ---------------- #

@app.route('/run_ucs', methods=['POST'])

def run_ucs():

    data = request.get_json()

    current_board = data['board']

    result = ucs(current_board)

    return jsonify(result)


# ---------------- RUN ---------------- #

if __name__ == '__main__':

    app.run(debug=True)