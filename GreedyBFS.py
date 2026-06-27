from flask import Flask, render_template, jsonify, request
import heapq

app = Flask(__name__)

# ---------------- POSITIONS ---------------- #

positions = ['A','B','C','D','E','F','G','H','I']


# ---------------- HEURISTIC ---------------- #

def heuristic(state):

    # fewer empty cells -> closer to goal
    return state.count('')


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


# ---------------- GREEDY BFS ---------------- #

def greedy(start):

    frontier = []

    counter = 0

    # (heuristic, counter, level, state, path, player)
    heapq.heappush(frontier, (

        heuristic(start),

        counter,

        0,

        start,

        [],

        'X'
    ))

    explored = set()

    traversal = []

    while frontier:

        h, _, level, state, path, player = heapq.heappop(frontier)

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

            "level": level,

            "heuristic": h
        })

        # STOP IF WIN FOUND
        winner = check_winner(state)

        if winner:

            traversal.append({
                "winner": winner
            })

            break

        next_player = 'O' if player == 'X' else 'X'

        children = []

        # GENERATE CHILDREN
        for i in range(9):

            if state[i] == '':

                new_state = state.copy()

                new_state[i] = player

                new_path = path + [positions[i]]

                children.append((

                    heuristic(new_state),

                    i,

                    new_state,

                    new_path,

                    next_player
                ))

        # LEFT TO RIGHT ORDER
        children.sort(key=lambda x: x[1])

        for h_value, _, child_state, child_path, child_player in children:

            counter += 1

            heapq.heappush(frontier, (

                h_value,

                counter,

                level + 1,

                child_state,

                child_path,

                child_player
            ))

    return traversal


# ---------------- HOME ---------------- #

@app.route('/')
def home():

    return render_template("index.html")


# ---------------- GREEDY ROUTE ---------------- #

@app.route('/run_greedy', methods=['POST'])

def run_greedy():

    data = request.get_json()

    current_board = data['board']

    result = greedy(current_board)

    return jsonify(result)


# ---------------- RUN ---------------- #

if __name__ == '__main__':

    app.run(debug=True)