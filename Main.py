from flask import Flask, render_template, jsonify, request

# ---------------- IMPORT ALGORITHMS ---------------- #

from app import bfs
from DFS import dfs
from UCS import ucs
from GreedyBFS import greedy
from AStar import astar
from CSP import csp_dfs
from Minmax import best_move
from ConditionalProbability import conditional_probability
from BayesTheorem import bayes_theorem
from BayesianNetwork import bayesian_network

# ---------------- FLASK APP ---------------- #

app = Flask(__name__)


# ---------------- HOME PAGE ---------------- #

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


# ---------------- DFS ROUTE ---------------- #

@app.route('/run_dfs', methods=['POST'])

def run_dfs():

    data = request.get_json()

    current_board = data['board']

    result = dfs(current_board)

    return jsonify(result)


# ---------------- UCS ROUTE ---------------- #

@app.route('/run_ucs', methods=['POST'])

def run_ucs():

    data = request.get_json()

    current_board = data['board']

    result = ucs(current_board)

    return jsonify(result)


# ---------------- GREEDY ROUTE ---------------- #

@app.route('/run_greedy', methods=['POST'])

def run_greedy():

    data = request.get_json()

    current_board = data['board']

    result = greedy(current_board)

    return jsonify(result)


# ---------------- A* ROUTE ---------------- #

@app.route('/run_astar', methods=['POST'])

def run_astar():

    data = request.get_json()

    current_board = data['board']

    result = astar(current_board)

    return jsonify(result)


# ---------------- CSP ROUTE ---------------- #

@app.route('/run_csp', methods=['POST'])

def run_csp():

    data = request.get_json()

    current_board = data['board']

    result = csp_dfs(current_board)

    return jsonify(result)


# ---------------- MINIMAX ROUTE ---------------- #

@app.route('/run_minimax', methods=['POST'])

def run_minimax():

    data = request.get_json()

    current_board = data['board']

    result = best_move(current_board)

    return jsonify(result)
#------------------Alpha - beta-----------#
@app.route('/run_alphabeta', methods=['POST'])

def run_alphabeta():

    data = request.get_json()

    board = data['board']

    result = best_move(board)

    return jsonify(result)

@app.route('/run_conditional_probability', methods=['POST'])
def run_conditional_probability():

    data = request.get_json()

    board = data['board']

    result = conditional_probability(board)

    return jsonify(result)

@app.route('/run_bayes', methods=['POST'])

def run_bayes():

    data = request.get_json()

    board = data['board']

    result = bayes_theorem(board)

    return jsonify(result)


@app.route('/run_bayesian_network',
           methods=['POST'])

def run_bayesian_network():

    data = request.get_json()

    board = data['board']

    result = bayesian_network(board)

    return jsonify(result)

# ---------------- RUN APP ---------------- #

if __name__ == '__main__':

    app.run(debug=True)